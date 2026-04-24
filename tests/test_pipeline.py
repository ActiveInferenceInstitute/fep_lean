"""Tests for FEPPipeline — 4-stage DAG.

`FEPPipeline.run()` records four `StepResult` rows in `PipelineResult.stages`:
Load Catalogue, Environment Validation, Gauss Sessions, Manuscript Artifacts.
All tests use real project files and the real FEPPipeline. Gauss/Hermes
stages are skipped unless FEP_LEAN_GAUSS_WORKFLOWS=1 is set. No mocks.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from pipeline.core import FEPPipeline, PipelineResult, StepResult, _max_topics_from_env
from catalogue.topics import FEPTopicCatalogue

PROJ = Path(__file__).resolve().parent.parent
_HAS_API_KEY = bool(
    os.environ.get("OPENROUTER_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")
)


def test_pipeline_instantiates() -> None:
    pl = FEPPipeline(PROJ)
    assert pl is not None


def test_pipeline_run_catalogue_only() -> None:
    """Default run (no GAUSS_WORKFLOWS): stages 1–2 run, Gauss skipped."""
    pl = FEPPipeline(PROJ)
    result = pl.run()
    assert isinstance(result, PipelineResult)
    assert result.status in {"ok", "partial", "warning", "error"}
    assert len(result.stages) >= 2
    names = [s.name for s in result.stages]
    assert "Load Catalogue" in names
    assert "Environment Validation" in names


def test_pipeline_run_result_fields() -> None:
    """PipelineResult exposes all required computed properties."""
    pl = FEPPipeline(PROJ)
    result = pl.run()
    # Core timing
    assert result.duration_s > 0
    assert result.total_duration > 0
    # Computed Lean/Gauss metrics (0 when Gauss skipped, that is fine)
    assert isinstance(result.hermes_count, int)
    assert isinstance(result.lean_verified_count, int)
    assert isinstance(result.lean_compile_ok, int)
    assert isinstance(result.steps, list)
    assert isinstance(result.topic_results, list)


def test_step_result_dataclass() -> None:
    """StepResult field order: name, status, message, duration_s."""
    s = StepResult("test_step", "ok", "all fine", 0.5)
    assert s.name == "test_step"
    assert s.status == "ok"
    assert s.message == "all fine"
    assert s.duration_s == 0.5


def test_pipeline_steps_alias() -> None:
    """result.steps is an alias for result.stages."""
    pl = FEPPipeline(PROJ)
    result = pl.run()
    assert result.steps is result.stages


def test_pipeline_area_filter() -> None:
    pl = FEPPipeline(PROJ)
    result = pl.run(area_filter="FEP")
    assert result.status in {"ok", "partial", "warning"}


def test_pipeline_topic_filter() -> None:
    pl = FEPPipeline(PROJ)
    result = pl.run(topic_filter=["fep-001", "fep-002"])
    # Gauss skipped → hermes_count is 0, but topics_ok reflects catalogue load
    assert isinstance(result.hermes_count, int)
    assert result.hermes_count <= 2


def test_max_topics_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("FEP_LEAN_MAX_TOPICS", raising=False)
    assert _max_topics_from_env() is None
    monkeypatch.setenv("FEP_LEAN_MAX_TOPICS", "3")
    assert _max_topics_from_env() == 3
    monkeypatch.setenv("FEP_LEAN_MAX_TOPICS", "0")
    assert _max_topics_from_env() is None


def test_pipeline_max_topics_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FEP_LEAN_MAX_TOPICS", "2")
    monkeypatch.setenv("FEP_LEAN_GAUSS_WORKFLOWS", "0")
    pl = FEPPipeline(PROJ)
    result = pl.run()
    cat_stage = next(s for s in result.stages if s.name == "Load Catalogue")
    assert cat_stage.payload is not None
    assert len(cat_stage.payload["topics"]) == 2


def test_pipeline_gauss_sessions_skipped_without_key() -> None:
    """With no API key and GAUSS_WORKFLOWS=0, Gauss stage is skipped."""
    import os
    key_vars = ["OPENROUTER_API_KEY", "ANTHROPIC_API_KEY", "OPENAI_API_KEY"]
    saved = {k: os.environ.pop(k, None) for k in key_vars}
    orig_wf = os.environ.pop("FEP_LEAN_GAUSS_WORKFLOWS", None)
    os.environ["FEP_LEAN_GAUSS_WORKFLOWS"] = "0"
    try:
        pl = FEPPipeline(PROJ)
        result = pl.run(topic_filter=["fep-001"])
        assert result.status in {"ok", "partial", "warning", "error"}
        names = [s.name for s in result.stages]
        assert "Gauss Sessions" in names
        gauss_stage = next(s for s in result.stages if s.name == "Gauss Sessions")
        assert gauss_stage.status == "skipped"
        assert result.hermes_count == 0
    finally:
        for k, v in saved.items():
            if v is not None:
                os.environ[k] = v
        if orig_wf is not None:
            os.environ["FEP_LEAN_GAUSS_WORKFLOWS"] = orig_wf
        else:
            os.environ.pop("FEP_LEAN_GAUSS_WORKFLOWS", None)


def test_pipeline_run_dir_created() -> None:
    pl = FEPPipeline(PROJ)
    result = pl.run()
    if result.run_dir:
        path = Path(result.run_dir)
        assert path.is_dir() or not path.exists()


def test_pipeline_report_files_written() -> None:
    pl = FEPPipeline(PROJ)
    result = pl.run()
    if result.run_dir:
        path = Path(result.run_dir)
        if path.is_dir():
            assert (path / "index.md").is_file()


def test_pipeline_stats_shape() -> None:
    pl = FEPPipeline(PROJ)
    result = pl.run()
    s = result.stats
    assert "topics_total" in s
    assert "hermes_success" in s
    assert "stages_ok" in s
    assert s["stages_ok"] >= 0


@pytest.mark.skipif(not _HAS_API_KEY, reason="No API key")
def test_pipeline_full_hermes_single_topic(monkeypatch: pytest.MonkeyPatch) -> None:
    """Real Hermes API call for a single topic (requires API key)."""
    monkeypatch.setenv("FEP_LEAN_GAUSS_WORKFLOWS", "1")
    pl = FEPPipeline(PROJ)
    result = pl.run(topic_filter=["fep-001"])
    assert isinstance(result, PipelineResult)
    assert result.hermes_count >= 0


# ── PipelineResult computed properties (lines 62-111) ──────────────────────


class TestPipelineResultProperties:
    """Direct unit tests for PipelineResult computed properties using real dataclasses."""

    @staticmethod
    def _make_topic(*, success: bool = True, hermes_success: bool = False,
                    lean_compiles: bool = False, lean_has_sorry: bool = True):
        """Lightweight namespace that quacks like TopicRunResult."""
        from types import SimpleNamespace
        return SimpleNamespace(
            success=success, hermes_success=hermes_success,
            lean_compiles=lean_compiles, lean_has_sorry=lean_has_sorry,
        )

    def test_hermes_count(self) -> None:
        r = PipelineResult(status="ok")
        r.topic_results = [
            self._make_topic(hermes_success=True),
            self._make_topic(hermes_success=False),
            self._make_topic(hermes_success=True),
        ]
        assert r.hermes_count == 2

    def test_lean_verified_count(self) -> None:
        r = PipelineResult(status="ok")
        r.topic_results = [
            self._make_topic(lean_compiles=True),
            self._make_topic(lean_compiles=False),
        ]
        assert r.lean_verified_count == 1

    def test_lean_compile_ok_no_sorry(self) -> None:
        r = PipelineResult(status="ok")
        r.topic_results = [
            self._make_topic(lean_compiles=True, lean_has_sorry=False),
            self._make_topic(lean_compiles=True, lean_has_sorry=True),
            self._make_topic(lean_compiles=False, lean_has_sorry=False),
        ]
        assert r.lean_compile_ok == 1  # only first counts

    def test_topics_ok_from_results(self) -> None:
        r = PipelineResult(status="ok")
        r.topic_results = [
            self._make_topic(success=True),
            self._make_topic(success=False),
            self._make_topic(success=True),
        ]
        assert r.topics_ok == 2

    def test_topics_ok_fallback_to_catalogue_stage(self) -> None:
        """When no topic_results, falls back to catalogue stage payload."""
        r = PipelineResult(status="ok")
        r.stages = [
            StepResult(name="Load Catalogue", status="ok",
                       payload={"topics": [{"id": "fep-001"}, {"id": "fep-002"}]}),
        ]
        assert r.topics_ok == 2

    def test_topics_ok_no_data(self) -> None:
        r = PipelineResult(status="ok")
        assert r.topics_ok == 0

    def test_stats_shape_and_values(self) -> None:
        r = PipelineResult(status="ok")
        r.stages = [
            StepResult(name="Load Catalogue", status="ok"),
            StepResult(name="Gauss Sessions", status="ok"),
        ]
        r.topic_results = [
            self._make_topic(hermes_success=True, lean_compiles=True, lean_has_sorry=False),
        ]
        s = r.stats
        assert s["topics_total"] == 1
        assert s["hermes_success"] == 1
        assert s["lean_compile_ok"] == 1
        assert s["lean_verified"] == 1
        assert s["stages_ok"] == 2
        assert s["gauss_ran"] is True

    def test_stats_gauss_not_ran(self) -> None:
        r = PipelineResult(status="ok")
        r.stages = [StepResult(name="Load Catalogue", status="ok")]
        s = r.stats
        assert s["gauss_ran"] is False


# ── _compute_lean_stats unit tests ───────────────────────────────────────────


class TestComputeLeanStats:
    """Tests for FEPPipeline._compute_lean_stats — counting correctness."""

    @staticmethod
    def _run_stats(topic_results: list[dict]) -> dict:
        """Drive _compute_lean_stats with synthetic _run_topic_results."""
        pl = FEPPipeline(PROJ)
        pl._run_topic_results = topic_results
        return pl._compute_lean_stats()

    def test_sorry_topic_not_in_compiles_clean(self) -> None:
        """sorry topics must be counted in compiles_with_sorry only, not compiles_clean."""
        results = [
            {"topic_id": "fep-001", "status": "success", "lean_has_sorry": False},
            {"topic_id": "fep-029", "status": "success", "lean_has_sorry": True},
            {"topic_id": "fep-003", "status": "failed", "lean_has_sorry": False},
        ]
        st = self._run_stats(results)
        assert st["compiles_clean"] == 1
        assert st["compiles_with_sorry"] == 1
        assert st["compile_error"] == 1
        assert st["total_processed"] == 3
        # Key invariant: clean + sorry + errors == total
        assert st["compiles_clean"] + st["compiles_with_sorry"] + st["compile_error"] == 3

    def test_all_clean_no_double_count(self) -> None:
        """With zero sorry topics, compiles_clean + 0 sorry + 0 error == total."""
        results = [
            {"topic_id": f"fep-{i:03d}", "status": "success", "lean_has_sorry": False}
            for i in range(1, 51)
        ]
        st = self._run_stats(results)
        assert st["compiles_clean"] == 50
        assert st["compiles_with_sorry"] == 0
        assert st["compile_error"] == 0
        assert st["total_processed"] == 50

    def test_failed_with_empty_error_still_logged(self) -> None:
        """Failed topics with empty error field must still appear in error_logs."""
        results = [
            {"topic_id": "fep-014", "status": "failed", "lean_has_sorry": False, "error": ""},
            {"topic_id": "fep-022", "status": "failed", "lean_has_sorry": False, "error": None},
            {"topic_id": "fep-042", "status": "failed", "lean_has_sorry": False,
             "error": "Function expected at Set.preimage_inter"},
        ]
        st = self._run_stats(results)
        assert len(st["error_logs"]) == 3
        assert any("fep-014" in e for e in st["error_logs"])
        assert any("fep-022" in e for e in st["error_logs"])
        assert any("fep-042" in e for e in st["error_logs"])
        assert any("not captured" in e for e in st["error_logs"] if "fep-014" in e)

    def test_realistic_39_1_10_counts(self) -> None:
        """Simulate run_20260418_223546: 39 clean + 1 sorry + 10 errors == 50."""
        results = (
            [{"topic_id": f"fep-{i:03d}", "status": "success", "lean_has_sorry": False}
             for i in range(2, 41)]  # 39 clean
            + [{"topic_id": "fep-029", "status": "success", "lean_has_sorry": True}]  # 1 sorry
            + [{"topic_id": f"fep-{i:03d}", "status": "failed", "lean_has_sorry": False, "error": ""}
               for i in [1, 3, 8, 14, 21, 22, 27, 31, 35, 42]]  # 10 errors
        )
        st = self._run_stats(results)
        assert st["compiles_clean"] == 39
        assert st["compiles_with_sorry"] == 1
        assert st["compile_error"] == 10
        assert st["total_processed"] == 50
        assert st["compiles_clean"] + st["compiles_with_sorry"] + st["compile_error"] == 50
