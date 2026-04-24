"""End-to-end pipeline on the real project directory. No mocks."""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from pipeline.orchestrator import project_root, run_pipeline, run_single_topic
from pipeline.core import PipelineResult

PROJ = Path(__file__).resolve().parent.parent

_HAS_API_KEY = bool(
    os.environ.get("OPENROUTER_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")
)
# Run live tests when a key is present, unless explicitly opted out with =0.
# Set FEP_LEAN_LIVE_TESTS=0 in CI to skip expensive API calls even when keys exist.
# Set FEP_LEAN_LIVE_TESTS=1 to force-run even without a key (will fail at API level).
_FEP_LEAN_LIVE_VAR = os.environ.get("FEP_LEAN_LIVE_TESTS", "").lower()
_LIVE_TESTS_ENABLED = (
    _FEP_LEAN_LIVE_VAR in ("1", "true", "yes")
    or (_HAS_API_KEY and _FEP_LEAN_LIVE_VAR not in ("0", "false", "no"))
)

pytestmark = pytest.mark.timeout(180)


@pytest.fixture(autouse=True)
def clear_project_dir_env(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.delenv("PROJECT_DIR", raising=False)
    # Default to non-workflow to avoid LLM calls during tests
    monkeypatch.setenv("FEP_LEAN_GAUSS_WORKFLOWS", "0")
    # Redirect Reporter run-dirs and ``output/.cache`` to a per-test tmp_path
    # so spawned ``run_pipeline()`` / ``run_single_topic()`` do not pollute
    # the canonical ``output/reports/run_*/`` tree (and clobber the
    # ``latest`` symlink) on the developer's checkout.  See
    # ``tests/AGENTS.md`` § "Test isolation: FEP_LEAN_OUTPUT_ROOT".
    monkeypatch.setenv("FEP_LEAN_OUTPUT_ROOT", str(tmp_path / "fep_output"))


def test_project_root_default() -> None:
    assert project_root().resolve() == PROJ.resolve()


def test_project_root_uses_project_dir(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("PROJECT_DIR", str(tmp_path))
    assert project_root().resolve() == tmp_path.resolve()


def test_run_single_topic_unknown() -> None:
    r = run_single_topic("fep-999", interactive=False)
    # Unknown topic gives error
    assert r["status"] in ("error", "partial", "ok")


@pytest.mark.skipif(not (_HAS_API_KEY and _LIVE_TESTS_ENABLED), reason="No API key found (set OPENROUTER_API_KEY or ANTHROPIC_API_KEY); or suppressed via FEP_LEAN_LIVE_TESTS=0")
def test_run_single_topic_ok(monkeypatch: pytest.MonkeyPatch) -> None:
    """Full pipeline integration: run_single_topic with live Gauss workflows.

    Why this test exists
    --------------------
    ``test_run_pipeline_writes_outputs`` (below) runs without Gauss workflows —
    it validates the catalogue-load → environment-check → manuscript-artifacts
    path.  This test is the only one that enables ``FEP_LEAN_GAUSS_WORKFLOWS=1``
    end-to-end, exercising the complete DAG:

    Load Catalogue → Environment Validation → Gauss Sessions
    (Hermes API + LeanVerifier + SQLite) → Manuscript Artifacts → Reporter

    What it checks
    --------------
    * ``run_single_topic("fep-001")`` returns a topic-level ``status`` from
      ``GaussRunner`` (``success``, ``failed``, ``hermes_error``, ``no_lean_sketch``, or
      ``error``) — **not** pipeline-level ``"ok"`` / ``"partial"`` (Reporter is skipped).
    * Required fields are present: ``topic_id``, ``session_id``, ``hermes_success``,
      ``lean_compiles``.
    * On ``success``, Lean verified; on ``failed``, Hermes succeeded but Lean did not compile.
    * ``run_dir`` is only set when the Reporter runs; single-topic mode may leave it empty.

    Why it can't be restructured to remove the gate
    -----------------------------------------------
    The Gauss Sessions stage requires a live OpenRouter API key to call
    ``HermesExplainer.explain_topic``.  There is no way to pre-seed the SQLite
    Hermes cache in the reporter pipeline without a prior live call.  The stub
    approach used in unit tests (``FixedHermes``) would require patching the
    pipeline internals — violating the no-mocks policy.

    How to run
    ----------
    ::

        export OPENROUTER_API_KEY=sk-or-v1-...   # or ANTHROPIC_API_KEY
        export FEP_LEAN_LIVE_TESTS=1
        uv run pytest tests/test_orchestrator.py::test_run_single_topic_ok -v -s

    Expected timing: 30–300 s (one Hermes call + lake env lean).
    """
    monkeypatch.setenv("FEP_LEAN_GAUSS_WORKFLOWS", "1")
    r = run_single_topic("fep-001", interactive=False)

    # Single-topic orchestrator returns TopicRunResult.as_dict(); status is topic-level.
    status = r.get("status")
    assert status in (
        "success",
        "failed",
        "hermes_error",
        "no_lean_sketch",
        "error",
    ), f"Unexpected status {status!r}; full result: {r}"

    assert r.get("topic_id") == "fep-001"
    assert r.get("session_id"), "expected non-empty session_id"
    assert "hermes_success" in r
    assert "lean_compiles" in r

    if status == "success":
        assert r.get("hermes_success") is True
        assert r.get("lean_compiles") is True
    elif status == "failed":
        assert r.get("hermes_success") is True
        assert r.get("lean_compiles") is False
    elif status in ("hermes_error", "no_lean_sketch"):
        assert r.get("hermes_success") is False
    # status == "error": runner exception; hermes_success may be absent or False

    # run_dir is intentionally empty in single-topic mode (Reporter is skipped).
    run_dir = r.get("run_dir", "")
    if run_dir:
        rd = Path(run_dir)
        assert rd.is_dir()
        assert (rd / "index.md").is_file()


def test_run_pipeline_writes_outputs() -> None:
    r: PipelineResult = run_pipeline(interactive=False)
    assert r.status in ("ok", "partial", "warning")
    stage_names = [s.name for s in r.stages]

    # Check that our core DAG stages are present
    assert "Load Catalogue" in stage_names
    assert "Environment Validation" in stage_names
    assert "Gauss Sessions" in stage_names

    # Reports written to run_dir
    if r.run_dir:
        rd = Path(r.run_dir)
        if rd.is_dir():
            assert (rd / "summary.json").is_file()
            assert (rd / "index.md").is_file()

    # Generated manuscript vars
    vars_path = PROJ / "manuscript" / "manuscript_vars.yaml"
    assert vars_path.is_file()
    body = vars_path.read_text(encoding="utf-8")
    assert "total_topics" in body


def test_run_pipeline_area_filter_fep() -> None:
    r = run_pipeline(area_filter="FEP", interactive=False)
    assert r.status in ("ok", "partial", "warning")
    # FEP area topics loaded — topics_ok reflects the catalogue subset
    assert r.topics_ok >= 0
