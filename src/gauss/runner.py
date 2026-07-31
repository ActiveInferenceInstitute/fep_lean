"""gauss_runner — formalization orchestrator combining Hermes and Lean 4.

Provides ``GaussRunner``, which executes a single topic formalization session:
1. Opens an SQLite session via ``OpenGaussClient``.
2. Calls ``HermesExplainer`` to refine the Lean sketch.
3. Tests the refined sketch via ``LeanVerifier``.
4. Saves all results and artifacts.
"""

from __future__ import annotations

import hashlib as _hashlib
import json as _json
import logging
import os
import time
from concurrent.futures import Future, ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any

from gauss.cli import check_gauss_cli
from gauss.client import OpenGaussClient
from llm.hermes import HermesConfig, HermesExplainer, HermesResult, restore_lean_structure
from verification.lean_verifier import LeanVerifier, VerifyResult

if TYPE_CHECKING:
    from catalogue.topics import TopicEntry

log = logging.getLogger(__name__)

# ── Workflow stage directives ─────────────────────────────────────────────────

_WORKFLOW_PREAMBLES: dict[str, str] = {
    "verify": "",
    "draft": (
        "TASK: Draft a new Lean 4 theorem skeleton. "
        "Focus on correctly typing the statement and naming hypotheses. "
        "Use sorry freely for all sub-goals."
    ),
    "prove": (
        "TASK: Attempt a full Lean 4 proof. "
        "Fill in as many sorry-holes as possible using Mathlib4 tactics. "
        "Prefer `exact`, `apply`, `simp`, `ring`, `linarith` over sorry."
    ),
    "review": (
        "TASK: Review the compiled Lean 4 sketch and provide: "
        "(1) correctness assessment, (2) suggested Mathlib lemma improvements, "
        "(3) clarity improvements. Do NOT produce a new ```lean block."
    ),
}


def _prefetch_enabled() -> bool:
    """True when ``FEP_LEAN_PREFETCH=1`` (Hermes for next topic while Lean verifies current)."""
    v = os.environ.get("FEP_LEAN_PREFETCH", "").lower().strip()
    return v in ("1", "true", "yes", "on")


def _hermes_cache_key(topic_id: str, lean_sketch: str, model: str, stage: str) -> str:
    """SHA-256 of the inputs that determine a unique Hermes response."""
    raw = f"{topic_id}:{lean_sketch}:{model}:{stage}"
    return _hashlib.sha256(raw.encode()).hexdigest()


@dataclass
class TopicRunResult:
    """Result of running one topic through the full Hermes + Lean workflow.

    Hermes-derived fields (``explanation``, ``refined_lean_sketch``, ``tokens_used``,
    ``hermes_model``, ``cache_hit``, ``hermes_lean_compiles``) are surfaced here
    so downstream reporters render the LLM payload without re-reading SQLite.
    """
    topic_id: str
    session_id: str
    success: bool
    status: str
    hermes_success: bool = False
    lean_compiles: bool = False
    lean_has_sorry: bool = False
    duration_s: float = 0.0
    error: str = ""
    workflow: str = "verify"
    stage_results: list[dict[str, Any]] = field(default_factory=list)
    explanation: str = ""
    refined_lean_sketch: str = ""
    final_lean_sketch: str = ""
    verification_source: str = "none"
    tokens_used: int = 0
    hermes_model: str = ""
    cache_hit: bool = False
    hermes_lean_compiles: bool = False
    # Same-model 429/transport retries summed across every model attempted
    # for this topic.  Distinct from chain advances (which switch models).
    network_retries: int = 0
    # Empty when the primary model produced the final answer; otherwise a
    # short label (``empty_content``, ``wall_clock_timeout``,
    # ``transport_error``, ``non_retriable_http``, ``parse_error``)
    # describing why the OpenRouter chain advanced past the primary.
    chain_advance_reason: str = ""

    def as_dict(self) -> dict[str, Any]:
        """Return serializable dict excluding internal state for JSON persistence."""
        return {
            "topic_id": self.topic_id,
            "session_id": self.session_id,
            "success": self.success,
            "status": self.status,
            "hermes_success": self.hermes_success,
            "lean_compiles": self.lean_compiles,
            "lean_has_sorry": self.lean_has_sorry,
            "duration_s": round(self.duration_s, 3),
            "error": self.error,
            "workflow": self.workflow,
            "stage_results": self.stage_results,
            "explanation": self.explanation,
            "refined_lean_sketch": self.refined_lean_sketch,
            "final_lean_sketch": self.final_lean_sketch,
            "verification_source": self.verification_source,
            "tokens_used": self.tokens_used,
            "hermes_model": self.hermes_model,
            "cache_hit": self.cache_hit,
            "hermes_lean_compiles": self.hermes_lean_compiles,
            "network_retries": self.network_retries,
            "chain_advance_reason": self.chain_advance_reason,
        }


class GaussRunner:
    """Orchestrates topic formalization, wiring together LLM + Lean + SQLite.

    Parameters
    ----------
    lean_verifier:
        Configured ``LeanVerifier`` instance.
    hermes:
        Configured ``HermesExplainer`` instance.
    client:
        Configured ``OpenGaussClient`` (for SQLite persistence).
    project_root:
        Root path (for saving artifacts).
    """

    def __init__(
        self,
        lean_verifier: LeanVerifier,
        hermes: HermesExplainer,
        client: OpenGaussClient,
        project_root: Path,
    ) -> None:
        self.lean = lean_verifier
        self.hermes = hermes
        self.client = client
        self.project_root = project_root
        # Prune stale Hermes cache entries on startup
        ttl = getattr(self.hermes._cfg, "cache_ttl_hours", 24.0)
        pruned = self.client.prune_hermes_cache(ttl_hours=ttl)
        if pruned:
            log.debug("Pruned %d stale Hermes cache entries (ttl=%.1fh)", pruned, ttl)
        self._prefetch_executor: ThreadPoolExecutor | None = None
        self._prefetch_future: Future[HermesResult] | None = None
        self._prefetch_hermes: HermesExplainer | None = None
        self._prefetch_next_topic: TopicEntry | None = None
        self._closed = False

    def close(self) -> None:
        """Release the prefetch worker and SQLite client resources."""
        if self._closed:
            return
        executor = self._prefetch_executor
        self._clear_prefetch_state()
        if executor is not None:
            executor.shutdown(wait=True)
        self.client.close()
        self._closed = True

    def __enter__(self) -> GaussRunner:
        return self

    def __exit__(self, exc_type: Any, exc: Any, traceback: Any) -> None:
        self.close()

    def _clear_prefetch_state(self) -> None:
        self._prefetch_executor = None
        self._prefetch_future = None
        self._prefetch_hermes = None
        self._prefetch_next_topic = None

    def run_topics_batch(
        self,
        topics: list[TopicEntry],
        *,
        max_topics: int | None = None,
        workflow: str = "verify",
    ) -> list[TopicRunResult]:
        """Run formalization over multiple topics sequentially.

        Parameters
        ----------
        workflow:
            Workflow stage to use for each topic.  See ``_WORKFLOW_PREAMBLES``
            for supported values.  Defaults to ``"verify"``.
        """
        self._clear_prefetch_state()
        results: list[TopicRunResult] = []
        subset = topics[:max_topics] if max_topics else topics
        if _prefetch_enabled() and workflow == "verify" and len(subset) > 1:
            return self._run_topics_batch_prefetch(subset, workflow=workflow)
        log.info(
            "GaussRunner: processing %d topic(s) [workflow=%s]",
            len(subset), workflow,
        )
        for i, t in enumerate(subset, 1):
            log.info("GaussRunner [%d/%d]: starting %s (workflow=%s)", i, len(subset), t.id, workflow)
            try:
                res = self.run_topic(t, workflow=workflow)
                results.append(res)
                hermes_str = "hermes=ok" if res.hermes_success else "hermes=skip"
                lean_str = (
                    "lean=ok" if (res.lean_compiles and not res.lean_has_sorry)
                    else ("lean=sorry" if res.lean_has_sorry else "lean=fail")
                )
                done = len(results)
                avg_s = sum(r.duration_s for r in results) / done
                eta_s = avg_s * (len(subset) - done)
                log.info(
                    "GaussRunner [%d/%d] %s  %s  %s  %.1fs  ETA ~%.0fs",
                    i, len(subset), t.id, hermes_str, lean_str, res.duration_s, eta_s,
                )
            except Exception as e:
                log.exception("GaussRunner: unhandled exception in %s", t.id)
                results.append(
                    TopicRunResult(
                        topic_id=t.id,
                        session_id="",
                        success=False,
                        status="error",
                        error=f"Unhandled runner exception: {e}",
                    )
                )
        return results

    def _run_topics_batch_prefetch(
        self,
        subset: list[TopicEntry],
        *,
        workflow: str,
    ) -> list[TopicRunResult]:
        """Same as ``run_topics_batch`` but overlap Hermes for topic N+1 with Lean on topic N."""
        executor = ThreadPoolExecutor(max_workers=1)
        self._prefetch_executor = executor
        self._prefetch_hermes = HermesExplainer(self.hermes._cfg)
        self._prefetch_future = None
        results: list[TopicRunResult] = []
        try:
            for i, t in enumerate(subset):
                self._prefetch_next_topic = subset[i + 1] if i + 1 < len(subset) else None
                log.info(
                    "GaussRunner [%d/%d] prefetch-mode: starting %s (workflow=%s)",
                    i + 1,
                    len(subset),
                    t.id,
                    workflow,
                )
                try:
                    res = self.run_topic(t, workflow=workflow)
                    results.append(res)
                    hermes_str = "hermes=ok" if res.hermes_success else "hermes=skip"
                    lean_str = (
                        "lean=ok" if (res.lean_compiles and not res.lean_has_sorry)
                        else ("lean=sorry" if res.lean_has_sorry else "lean=fail")
                    )
                    done = len(results)
                    avg_s = sum(r.duration_s for r in results) / done
                    eta_s = avg_s * (len(subset) - done)
                    log.info(
                        "GaussRunner [%d/%d] %s  %s  %s  %.1fs  ETA ~%.0fs",
                        i + 1, len(subset), t.id, hermes_str, lean_str, res.duration_s, eta_s,
                    )
                except Exception as e:
                    log.exception("GaussRunner: unhandled exception in %s", t.id)
                    results.append(
                        TopicRunResult(
                            topic_id=t.id,
                            session_id="",
                            success=False,
                            status="error",
                            error=f"Unhandled runner exception: {e}",
                        )
                    )
        finally:
            executor.shutdown(wait=True)
            self._clear_prefetch_state()
        return results

    def _start_prefetch_next_hermes(
        self,
        current_topic: TopicEntry,
        workflow: str,
        preamble: str,
        model: str,
    ) -> None:
        """Schedule Hermes for the next topic while the current topic's Lean verify runs."""
        if (
            self._prefetch_executor is None
            or self._prefetch_hermes is None
            or workflow != "verify"
            or self._prefetch_next_topic is None
        ):
            return
        nt = self._prefetch_next_topic
        if nt.id == current_topic.id:
            return
        lean_next = getattr(nt, "lean_sketch", "") or ""
        nk = _hermes_cache_key(nt.id, lean_next, model, workflow)
        if self.client.get_cached_hermes(nk) is not None:
            return
        log.debug("Prefetch Hermes for %s while verifying %s", nt.id, current_topic.id)
        self._prefetch_future = self._prefetch_executor.submit(
            self._prefetch_hermes.explain_topic, nt, preamble=preamble
        )

    def run_topic(
        self, topic: TopicEntry, *, workflow: str = "verify"
    ) -> TopicRunResult:
        """Run one topic and finalize any session left open by an exception."""
        self._active_session_id: str | None = None
        try:
            return self._run_topic(topic, workflow=workflow)
        except Exception as exc:
            if self._active_session_id:
                self.client.close_open_session(
                    self._active_session_id,
                    error=f"{type(exc).__name__}: {exc}",
                )
            raise

    def _run_topic(
        self, topic: TopicEntry, *, workflow: str = "verify"
    ) -> TopicRunResult:
        """Run the full Hermes + Lean workflow for a single topic.

        Parameters
        ----------
        workflow:
            Workflow stage controlling the Hermes task directive:
            - ``"verify"`` (default) — refine sketch and verify compilation.
            - ``"draft"`` — produce a new typed skeleton (sorry ok in sub-goals).
            - ``"prove"`` — attempt a full proof minimising sorry usage.
            - ``"review"`` — verify then request a post-compile review commentary.
        """
        if workflow not in _WORKFLOW_PREAMBLES:
            raise ValueError(f"unsupported workflow: {workflow}")

        preamble = _WORKFLOW_PREAMBLES.get(workflow, "")
        lean_sketch = getattr(topic, "lean_sketch", "") or ""
        model = self.hermes._cfg.model
        cache_key = _hermes_cache_key(topic.id, lean_sketch, model, workflow)
        stage_results: list[dict[str, Any]] = []

        t0 = time.time()
        session_id = self.client.create_session(
            topic.id,
            topic.area,
            lean_sketch,
        )
        self._active_session_id = session_id
        self.client.log_event("evaluation_started", session_id=session_id, workflow=workflow)

        # ── Hermes call with cache (prefetch result from prior topic's verify phase) ─
        cached = self.client.get_cached_hermes(cache_key)
        if self._prefetch_future is not None:
            log.debug("Hermes prefetch result for %s (workflow=%s)", topic.id, workflow)
            hermes_res = self._prefetch_future.result()
            self._prefetch_future = None
            # Require BOTH content and a non-empty refined sketch to cache.
            # A partial response (e.g. truncated mid-fence) leaves
            # ``refined_lean_sketch=""`` even though ``success=bool(content)`` is
            # True; persisting that row poisons the cache and forces every
            # subsequent run through the same dead-end. See fep-019 (2026-04-22).
            if hermes_res.success and hermes_res.refined_lean_sketch:
                self.client.set_cached_hermes(
                    cache_key,
                    topic_id=topic.id,
                    stage=workflow,
                    model=hermes_res.model_used,
                    result_json=_json.dumps(hermes_res.as_dict()),
                    lean_sketch_hash=_hashlib.sha256(lean_sketch.encode()).hexdigest(),
                )
        elif cached is not None:
            log.debug("Hermes cache hit: %s (workflow=%s)", topic.id, workflow)
            hermes_res = HermesResult(
                success=cached.get("success", False),
                model_used=cached.get("model_used", model),
                explanation=cached.get("explanation", ""),
                refined_lean_sketch=cached.get("refined_lean_sketch", ""),
                reasoning=cached.get("reasoning", ""),
                tokens_used=cached.get("tokens_used", 0),
                duration_s=cached.get("duration_s", 0.0),
                error=cached.get("error", ""),
                topic_id=cached.get("topic_id", topic.id),
                cache_hit=True,
                network_retries=cached.get("network_retries", 0),
                chain_advance_reason=cached.get("chain_advance_reason", ""),
            )
        else:
            hermes_res = self.hermes.explain_topic(topic, preamble=preamble)
            # See cache-write comment above: refusing to persist responses
            # without an extracted ``lean`` block prevents silent reuse of
            # truncated / fence-omitted model output on the next run.
            if hermes_res.success and hermes_res.refined_lean_sketch:
                self.client.set_cached_hermes(
                    cache_key,
                    topic_id=topic.id,
                    stage=workflow,
                    model=hermes_res.model_used,
                    result_json=_json.dumps(hermes_res.as_dict()),
                    lean_sketch_hash=_hashlib.sha256(lean_sketch.encode()).hexdigest(),
                )

        self._record_hermes_turns(session_id, topic, hermes_res, preamble=preamble)

        if not hermes_res.success:
            self.client.close_session(session_id, status="error", hermes_success=False)
            return TopicRunResult(
                topic_id=topic.id,
                session_id=session_id,
                success=False,
                status="hermes_error",
                error=hermes_res.error or "hermes returned empty",
                duration_s=time.time() - t0,
                workflow=workflow,
                explanation=hermes_res.explanation,
                refined_lean_sketch=hermes_res.refined_lean_sketch,
                tokens_used=hermes_res.tokens_used,
                hermes_model=hermes_res.model_used,
                cache_hit=hermes_res.cache_hit,
                network_retries=hermes_res.network_retries,
                chain_advance_reason=hermes_res.chain_advance_reason,
            )

        refined = hermes_res.refined_lean_sketch
        if not refined:
            self.client.close_session(session_id, status="failed", hermes_success=False)
            return TopicRunResult(
                topic_id=topic.id,
                session_id=session_id,
                success=False,
                status="no_lean_sketch",
                error="LLM did not output a ```lean block",
                duration_s=time.time() - t0,
                workflow=workflow,
                explanation=hermes_res.explanation,
                refined_lean_sketch=hermes_res.refined_lean_sketch,
                tokens_used=hermes_res.tokens_used,
                hermes_model=hermes_res.model_used,
                cache_hit=hermes_res.cache_hit,
                network_retries=hermes_res.network_retries,
                chain_advance_reason=hermes_res.chain_advance_reason,
            )

        # Restore import lines and namespace wrapper that LLMs commonly strip.
        refined = restore_lean_structure(refined, lean_sketch)
        self.client.set_refined_sketch(session_id, refined)

        # Overlap Hermes for the next catalogue row with Lean verify (prefetch mode only).
        self._start_prefetch_next_hermes(topic, workflow, preamble, model)

        if not self.lean.check_lake_available():
            verify_res = VerifyResult(
                topic_id=topic.id,
                compiles=False,
                has_sorry=False,
                lean_version=self.lean.lean_version() or "unknown",
                skip_reason="lake is unavailable or failed its bounded version probe",
            )
        else:
            verify_res = self.lean.verify_sketch(topic.id, refined)

        _hermes_lean_compiles = verify_res.compiles

        # ── Optional review pass (workflow="review") ──────────────────────────
        if workflow == "review" and verify_res.compiles:
            review_preamble = _WORKFLOW_PREAMBLES["review"]
            extra_ctx = (
                f"The sketch compiled successfully (has_sorry={verify_res.has_sorry}). "
                f"Errors: {verify_res.errors or 'none'}."
            )
            review_cache_key = _hermes_cache_key(
                topic.id, refined, model, "review_commentary"
            )
            review_cached = self.client.get_cached_hermes(review_cache_key)
            if review_cached is not None:
                # Explicit field reconstruction from cache dict — avoids fragile
                # **kwargs unpacking.  cache_hit is forced True regardless of
                # whatever value was stored in the dict.
                review_res = HermesResult(
                    success=review_cached.get("success", False),
                    model_used=review_cached.get("model_used", model),
                    explanation=review_cached.get("explanation", ""),
                    refined_lean_sketch=review_cached.get("refined_lean_sketch", ""),
                    reasoning=review_cached.get("reasoning", ""),
                    tokens_used=int(review_cached.get("tokens_used", 0)),
                    duration_s=float(review_cached.get("duration_s", 0.0)),
                    error=review_cached.get("error", ""),
                    topic_id=review_cached.get("topic_id", topic.id),
                    cache_hit=True,
                    network_retries=int(review_cached.get("network_retries", 0)),
                    chain_advance_reason=review_cached.get("chain_advance_reason", ""),
                )
            else:
                review_res = self.hermes.explain_topic(
                    topic, preamble=f"{review_preamble}\n\n{extra_ctx}"
                )
                if review_res.success:
                    self.client.set_cached_hermes(
                        review_cache_key,
                        topic_id=topic.id,
                        stage="review_commentary",
                        model=review_res.model_used,
                        result_json=_json.dumps(review_res.as_dict()),
                        lean_sketch_hash=_hashlib.sha256(refined.encode()).hexdigest(),
                    )
            stage_results.append({
                "stage": "review_commentary",
                "success": review_res.success,
                "explanation": review_res.explanation,
                "cache_hit": review_res.cache_hit,
            })

        artifact = self._build_artifact_payload(topic, hermes_res, verify_res)
        self.client.write_artifact(session_id, artifact)

        is_success = verify_res.compiles and not verify_res.has_sorry
        status = "success" if is_success else "failed"

        self.client.close_session(
            session_id,
            status=status,
            hermes_success=True,
            lean_compiles=1 if verify_res.compiles else 0,
        )

        return TopicRunResult(
            topic_id=topic.id,
            session_id=session_id,
            success=is_success,
            status=status,
            hermes_success=True,
            lean_compiles=verify_res.compiles,
            lean_has_sorry=verify_res.has_sorry,
            duration_s=time.time() - t0,
            error=("; ".join(verify_res.errors) if verify_res.errors
                   else (verify_res.skip_reason or (verify_res.stdout[:300] if verify_res.stdout else ""))),
            workflow=workflow,
            stage_results=stage_results,
            explanation=hermes_res.explanation,
            refined_lean_sketch=refined,
            final_lean_sketch=refined,
            verification_source="hermes_refined",
            tokens_used=hermes_res.tokens_used,
            hermes_model=hermes_res.model_used,
            cache_hit=hermes_res.cache_hit,
            hermes_lean_compiles=_hermes_lean_compiles,
            network_retries=hermes_res.network_retries,
            chain_advance_reason=hermes_res.chain_advance_reason,
        )

    # ── Internal helpers ──────────────────────────────────────────────────────

    def _record_hermes_turns(
        self,
        session_id: str,
        topic: TopicEntry,
        res: HermesResult,
        *,
        preamble: str = "",
    ) -> None:
        """Write the prompt and response blocks as dialogue turns to SQLite."""
        # Record the system/user prompt matching what HermesExplainer sent
        msgs = self.hermes.build_messages(topic, preamble=preamble)  # pure function
        sys_msg = next((m["content"] for m in msgs if m["role"] == "system"), "")
        usr_msg = next((m["content"] for m in msgs if m["role"] == "user"), "")
        if sys_msg:
            self.client.update_session(session_id, 0, "system", sys_msg, 0)
        self.client.update_session(session_id, 1, "user", usr_msg, 0)

        if not res.success:
            self.client.update_session(
                session_id, 2, "assistant", f"[ERROR] {res.error}", 0
            )
            return

        out = ""
        if res.explanation:
            out += f"Explanation:\n{res.explanation}\n\n"
        if res.refined_lean_sketch:
            out += "```lean\n" + res.refined_lean_sketch + "\n```"

        self.client.update_session(session_id, 2, "assistant", out, res.tokens_used)

        if res.reasoning:
            self.client.update_session(
                session_id, 3, "assistant_reasoning", res.reasoning, 0
            )

    def _build_artifact_payload(
        self,
        topic: TopicEntry,
        hermes_res: HermesResult,
        verify_res: VerifyResult,
    ) -> dict[str, Any]:
        """Combine all topic data into a comprehensive JSON artifact payload."""
        return {
            "topic": {
                "id": topic.id,
                "title": getattr(topic, "title", topic.id),
                "area": getattr(topic, "area", "unknown"),
                "mathlib_status": getattr(topic, "mathlib_status", "unknown"),
            },
            "hermes": hermes_res.as_dict(),
            "lean": verify_res.as_dict(),
            "timestamp": time.time(),
        }

    @classmethod
    def create_default(
        cls, project_root: Path, *, require_cli: bool = False
    ) -> GaussRunner:
        """Convenience constructor using defaults for the FEP project.

        If ``require_cli`` is True and `gauss` is missing, raises RuntimeError.
        """
        ok, msg = check_gauss_cli(project_root, require=require_cli)
        if not ok:
            raise RuntimeError(msg)

        lean = LeanVerifier(project_root / "lean", project_root)
        hermes = HermesExplainer(HermesConfig.from_settings(project_root))
        gauss_home: str | Path | None = os.environ.get("GAUSS_HOME")
        if not gauss_home:
            try:
                import yaml

                settings = yaml.safe_load((project_root / "config" / "settings.yaml").read_text(encoding="utf-8")) or {}
                gauss_home = settings.get("gauss", {}).get("home")
            except (OSError, yaml.YAMLError, AttributeError):
                gauss_home = None
        client = OpenGaussClient(gauss_home=gauss_home)
        return cls(lean, hermes, client, project_root)
