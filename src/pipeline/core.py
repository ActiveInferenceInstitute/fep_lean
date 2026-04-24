"""FEP pipeline core: four recorded `StepResult` rows in `PipelineResult.stages`.

`FEPPipeline.run` records Load Catalogue, Environment Validation, Gauss Sessions
(skipped when workflows are disabled), and Manuscript Artifacts. Run reporting
(`Reporter.generate`) is invoked from `pipeline.orchestrator.run_pipeline` after
`run()` returns — it is not a fifth entry in `PipelineResult.stages`.

Usage:
    pipeline = FEPPipeline(project_root)
    result = pipeline.run(topic_filter=["fep-001", "fep-002"])
"""

from __future__ import annotations

import logging
import os
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# Use subpackage imports
from catalogue.topics import FEPTopicCatalogue
from verification.environment import run_validation_checks
from gauss.cli import workflows_enabled
from gauss.runner import GaussRunner
from output.manuscript import write_manuscript_vars

log = logging.getLogger(__name__)


def _max_topics_from_env() -> int | None:
    """If ``FEP_LEAN_MAX_TOPICS`` is a positive integer, cap the catalogue batch size."""
    raw = (os.environ.get("FEP_LEAN_MAX_TOPICS") or "").strip()
    if not raw:
        return None
    try:
        n = int(raw, 10)
    except ValueError:
        return None
    return n if n >= 1 else None


@dataclass
class StepResult:
    """Result record for one pipeline stage execution."""
    name: str
    status: str  # 'ok', 'warning', 'error', 'skipped'
    message: str = ""
    duration_s: float = 0.0
    payload: Any = None
    error: str | None = None


@dataclass
class PipelineResult:
    """Aggregated result of an FEPPipeline run, with computed properties for reporting."""
    status: str  # 'ok', 'warning', 'partial', 'error'
    total_duration: float = 0.0
    run_dir: str = ""
    stages: list[StepResult] = field(default_factory=list)
    lean_stats: dict[str, Any] = field(default_factory=dict)
    # Populated by orchestrator after reporter runs
    _topic_results: list[Any] = field(default_factory=list)

    # ── Computed properties exposing Lean/Gauss metrics ─────────────────────

    @property
    def steps(self) -> list[StepResult]:
        """Alias for stages — exposes the DAG step list."""
        return self.stages

    @property
    def topic_results(self) -> list[Any]:
        """List of TopicRunResult from GaussRunner, populated post-run."""
        return self._topic_results

    @topic_results.setter
    def topic_results(self, value: list[Any]) -> None:
        self._topic_results = value

    @property
    def hermes_count(self) -> int:
        """Number of topics where Hermes LLM succeeded."""
        return sum(1 for t in self._topic_results if getattr(t, "hermes_success", False))

    @property
    def lean_verified_count(self) -> int:
        """Number of topics where Lean compilation succeeded (any)."""
        return sum(1 for t in self._topic_results if getattr(t, "lean_compiles", False))

    @property
    def lean_compile_ok(self) -> int:
        """Number of topics where Lean compiled clean (no sorry)."""
        return sum(
            1 for t in self._topic_results
            if getattr(t, "lean_compiles", False) and not getattr(t, "lean_has_sorry", True)
        )

    @property
    def topics_ok(self) -> int:
        """Number of topics with overall success status."""
        if self._topic_results:
            return sum(1 for t in self._topic_results if getattr(t, "success", False))
        # Fall back to catalogue count loaded by stage 1 if Gauss didn't run
        cat_stage = next((s for s in self.stages if s.name == "Load Catalogue"), None)
        if cat_stage and isinstance(cat_stage.payload, dict):
            return len(cat_stage.payload.get("topics", []))
        return 0

    @property
    def duration_s(self) -> float:
        """Total pipeline duration alias."""
        return self.total_duration

    @property
    def stats(self) -> dict[str, Any]:
        """Aggregate pipeline statistics for tests and reporting."""
        gauss_stage = next((s for s in self.stages if "Gauss" in s.name), None)
        return {
            "topics_total": self.topics_ok,
            "hermes_success": self.hermes_count,
            "lean_compile_ok": self.lean_compile_ok,
            "lean_verified": self.lean_verified_count,
            "stages_ok": sum(1 for s in self.stages if s.status == "ok"),
            "gauss_ran": gauss_stage is not None and gauss_stage.status == "ok",
            **self.lean_stats,
        }

    def as_dict(self) -> dict[str, Any]:
        """Return serializable dict for JSON reporting and tests (excludes computed properties)."""
        return {
            "total_duration": round(self.total_duration, 3),
            "status": self.status,
            "run_dir": self.run_dir,
            "stages": [
                {
                    "name": s.name,
                    "status": s.status,
                    "duration_s": round(s.duration_s, 3),
                    "error": s.error,
                }
                for s in self.stages
            ],
            "lean_stats": self.lean_stats,
        }


def _resolve_output_root(project_root: Path, output_root: Path | None) -> Path:
    """Resolve the directory that holds ``reports/``, ``.cache/``, etc.

    Resolution order:
      1. Explicit ``output_root`` argument (if given).
      2. ``FEP_LEAN_OUTPUT_ROOT`` environment variable (used by tests so
         pytest-spawned runs do not pollute the live ``output/reports/``).
      3. ``project_root / "output"`` (the canonical default).
    """
    if output_root is not None:
        return Path(output_root)
    env_val = os.environ.get("FEP_LEAN_OUTPUT_ROOT")
    if env_val:
        return Path(env_val)
    return project_root / "output"


class FEPPipeline:
    """The formalization DAG executing ordered build stages.

    ``output_root`` controls where Reporter run-dirs and the manuscript
    cache live; it defaults to ``project_root / "output"`` but tests
    typically override it (or set ``FEP_LEAN_OUTPUT_ROOT``) so spawned
    runs do not mutate the canonical ``output/reports/`` tree.
    """

    def __init__(
        self,
        project_root: Path,
        *,
        output_root: Path | None = None,
    ) -> None:
        self.project_root = project_root
        self.config_dir = project_root / "config"
        self.topics_file = self.config_dir / "topics.yaml"
        self.output_root = _resolve_output_root(project_root, output_root)
        self._catalogue: FEPTopicCatalogue | None = None
        self._check_result: dict[str, Any] | None = None
        self._run_topic_results: list[dict[str, Any]] = []

    def run(
        self,
        topic_filter: list[str] | None = None,
        area_filter: str | None = None,
    ) -> PipelineResult:
        """Run the DAG; append four stages to ``PipelineResult.stages``.

        Stages: Load Catalogue, Environment Validation, Gauss Sessions, Manuscript
        Artifacts. If ``FEP_LEAN_GAUSS_WORKFLOWS`` is unset, **Gauss Sessions** is
        recorded as ``skipped``. Markdown/JSON reporting is **not** part of
        ``stages``; see ``orchestrator.run_pipeline``.
        """
        t_start = time.time()
        stages: list[StepResult] = []
        pipeline_status = "ok"

        def _run_stage(
            name: str, fn: Any, *, skip: bool = False, skip_reason: str = ""
        ) -> StepResult | None:
            nonlocal pipeline_status
            if skip:
                log.info("Skipping stage: %s (%s)", name, skip_reason)
                r = StepResult(name=name, status="skipped", message=skip_reason, duration_s=0.0)
                stages.append(r)
                return r

            log.info("Stage: %s", name)
            t0 = time.time()
            try:
                payload = fn()
                status = "ok"
            except Exception as e:
                log.exception("Stage %s failed: %s", name, e)
                status = "error"
                pipeline_status = "error"
                payload = None
            dur = time.time() - t0
            r = StepResult(name=name, status=status, duration_s=dur, payload=payload)
            stages.append(r)
            icon = "✓" if status == "ok" else ("⚠" if status == "warning" else "✗")
            log.info("Stage '%s' %s %s (%.1fs)", name, icon, status, dur)
            return r

        # Stage 1: Load Catalogue
        def _stage_catalogue() -> dict[str, Any]:
            self._catalogue = FEPTopicCatalogue.from_yaml(self.topics_file)
            topics = self._catalogue.topics
            if topic_filter:
                topics = [t for t in topics if t.id in topic_filter]
            if area_filter:
                topics = [t for t in topics if getattr(t, "area", "") == area_filter]
            cap = _max_topics_from_env()
            if cap is not None and len(topics) > cap:
                n_before = len(topics)
                log.info(
                    "FEP_LEAN_MAX_TOPICS=%s: running first %d of %d catalogue rows",
                    os.environ.get("FEP_LEAN_MAX_TOPICS", ""),
                    cap,
                    n_before,
                )
                topics = topics[:cap]
            # store filtered subset locally for later stages
            self._topics_to_run = topics
            return {"topics": [t.id for t in topics]}

        sr1 = _run_stage("Load Catalogue", _stage_catalogue)
        if sr1.status == "error":
            return PipelineResult(status="error", total_duration=time.time() - t_start, stages=stages)

        # Stage 2: Validation
        def _stage_validation() -> dict[str, Any]:
            res = run_validation_checks(self.project_root)
            self._check_result = res
            if res.get("status") != "ok":
                raise RuntimeError("Environment checks failed.")
            return res

        sr2 = _run_stage("Environment Validation", _stage_validation)
        if sr2.status == "error":
            # Demote pipeline state to warning if validation fails gracefully
            # (allowing catalogue & reporting to still run safely)
            pipeline_status = "warning"

        # Stage 3: LLM + Lean (GaussRunner)
        _raw_topic_results: list[Any] = []

        def _stage_gauss() -> dict[str, Any]:
            if not self._topics_to_run:
                log.info("Gauss Sessions: no topics to process (filter produced empty set)")
                return {"topics": [], "note": "no_topics_after_filter"}
            runner = GaussRunner.create_default(self.project_root, require_cli=False)
            # Preflight once: surface credential failures (e.g. OpenRouter
            # "Key limit exceeded") before the long Lean batch starts.
            if getattr(runner, "hermes", None) is not None and runner.hermes.is_live:
                runner.hermes.preflight()
            res_list = runner.run_topics_batch(self._topics_to_run)
            _raw_topic_results.extend(res_list)  # store raw objects for computed props
            self._run_topic_results = [r.as_dict() for r in res_list]
            return {"topics": self._run_topic_results}

        run_heavy = workflows_enabled()
        skip_msg = "workflows disabled (set FEP_LEAN_GAUSS_WORKFLOWS=1)"
        _run_stage("Gauss Sessions", _stage_gauss, skip=not run_heavy, skip_reason=skip_msg)

        # Stage 4: Artifacts (manuscript vars + appendix in one thread; figures in parallel)
        def _stage_artifacts() -> dict[str, Any]:
            from output.manuscript import (
                write_unified_formalism_appendix_markdown,
            )
            from output.figures import write_all_catalogue_figures

            def _manuscript_block() -> tuple[Path, Path]:
                p = write_manuscript_vars(self.project_root, self._catalogue)
                apx = write_unified_formalism_appendix_markdown(
                    self.project_root, self._catalogue
                )
                return p, apx

            with ThreadPoolExecutor(max_workers=2) as ex:
                f_ms = ex.submit(_manuscript_block)
                f_fig = ex.submit(write_all_catalogue_figures, self._catalogue, self.project_root)
                path, apx_unified = f_ms.result()
                f_fig.result()
            return {
                "vars_file": str(path),
                "unified_formalism_md": str(apx_unified),
                "lean_catalogue_md": str(apx_unified),
                "latex_equations_md": str(apx_unified),
            }

        _run_stage("Manuscript Artifacts", _stage_artifacts)

        # Compute lean stats for result bundle
        l_stats = self._compute_lean_stats()

        # Reporting runs in orchestrator.run_pipeline after this method returns.
        total_dur = time.time() - t_start
        log.info(
            "FEPPipeline complete: %s  %d stages  %.1fs total",
            pipeline_status, len(stages), total_dur,
        )

        return PipelineResult(
            total_duration=total_dur,
            status=pipeline_status,
            stages=stages,
            lean_stats=l_stats,
            _topic_results=_raw_topic_results,
        )

    def _compute_lean_stats(self) -> dict[str, Any]:
        """Aggregate verification metrics across all executed topics."""
        from collections import defaultdict
        st: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for r in self._run_topic_results:
            st[r.get("status", "unknown")].append(r)

        return {
            "total_processed": len(self._run_topic_results),
            "compiles_clean": sum(1 for r in st.get("success", []) if not r.get("lean_has_sorry")),
            "compiles_with_sorry": sum(1 for r in st.get("success", []) if r.get("lean_has_sorry")),
            "compile_error": len(st.get("failed", [])),
            "skipped": len(st.get("skipped", [])),
            "error_logs": [
                f"{r['topic_id']}: {r.get('error') or 'error details not captured'}"
                for r in st.get("failed", [])
            ],
            "sorry_logs": [
                f"{r['topic_id']} compiles, but sketch contains 'sorry'"
                for r in st.get("success", [])
                if r.get("lean_has_sorry")
            ],
            "clean_logs": [
                f"{r['topic_id']} successfully verified"
                for r in st.get("success", [])
                if not r.get("lean_has_sorry")
            ],
        }
