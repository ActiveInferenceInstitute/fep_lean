"""Strict pipeline contract tests."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest
from pipeline.core import FEPPipeline, PipelineResult, StepResult, _max_topics_from_env

PROJ = Path(__file__).resolve().parent.parent


def test_pipeline_instantiates() -> None:
    assert FEPPipeline(PROJ) is not None


def test_catalogue_mode_is_complete_but_unverified(tmp_path: Path) -> None:
    result = FEPPipeline(PROJ, output_root=tmp_path / "output").run(mode="catalogue", topic_filter=["fep-001", "fep-002"])
    assert isinstance(result, PipelineResult)
    assert result.mode == "catalogue"
    assert result.complete is True
    assert result.catalogue_topics == 2
    assert result.verified_topics == 0
    assert result.capabilities["verification"] is False
    assert next(stage for stage in result.stages if stage.name == "Gauss Sessions").status == "not_run"


def test_full_mode_fails_without_capabilities(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    result = FEPPipeline(PROJ, output_root=tmp_path / "output").run(mode="full", topic_filter=["fep-001"])
    assert result.complete is False
    assert result.status == "error"
    assert result.run_dir == ""
    assert result.failure_reason
    assert not (tmp_path / "output" / "reports").exists()


def test_result_fields_are_explicit(tmp_path: Path) -> None:
    result = FEPPipeline(PROJ, output_root=tmp_path / "output").run(mode="catalogue")
    assert result.duration_s > 0
    assert isinstance(result.topic_results, list)
    assert isinstance(result.capabilities, dict)
    assert "mode" in result.as_dict()
    assert "complete" in result.as_dict()
    assert "failure_reason" in result.as_dict()
    assert not hasattr(result, "steps")


def test_step_result_dataclass() -> None:
    step = StepResult("test_step", "ok", "all fine", 0.5)
    assert step.name == "test_step"
    assert step.status == "ok"
    assert step.message == "all fine"
    assert step.duration_s == 0.5


def test_filters_and_topic_cap(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FEP_LEAN_MAX_TOPICS", "2")
    result = FEPPipeline(PROJ, output_root=tmp_path / "output").run(mode="catalogue", area_filter="FEP")
    load = next(stage for stage in result.stages if stage.name == "Load Catalogue")
    assert len(load.payload["topics"]) == 2


def test_unknown_topic_is_an_error(tmp_path: Path) -> None:
    result = FEPPipeline(PROJ, output_root=tmp_path / "output").run(mode="catalogue", topic_filter=["fep-999"])
    assert result.status == "error"
    assert "unknown topic" in result.failure_reason


def test_max_topics_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("FEP_LEAN_MAX_TOPICS", raising=False)
    assert _max_topics_from_env() is None
    monkeypatch.setenv("FEP_LEAN_MAX_TOPICS", "3")
    assert _max_topics_from_env() == 3
    monkeypatch.setenv("FEP_LEAN_MAX_TOPICS", "0")
    with pytest.raises(ValueError):
        _max_topics_from_env()


def test_stats_never_counts_catalogue_as_verified() -> None:
    result = PipelineResult(status="ok", mode="catalogue", complete=True, catalogue_topics=50)
    assert result.stats["topics_total"] == 50
    assert result.stats["topics_verified"] == 0
    assert result.lean_compile_ok == 0


def test_topic_metrics_use_clean_compilation() -> None:
    result = PipelineResult(status="ok", mode="full", catalogue_topics=2)
    result.topic_results = [
        SimpleNamespace(hermes_success=True, lean_compiles=True, lean_has_sorry=False),
        SimpleNamespace(hermes_success=True, lean_compiles=True, lean_has_sorry=True),
    ]
    assert result.hermes_count == 2
    assert result.lean_verified_count == 2
    assert result.lean_compile_ok == 1


def test_invalid_mode_rejected() -> None:
    with pytest.raises(ValueError):
        FEPPipeline(PROJ).run(mode="invalid")  # type: ignore[arg-type]
