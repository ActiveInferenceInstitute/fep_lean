"""Programmatic entry-point tests."""

from __future__ import annotations

from pathlib import Path

import pytest
from pipeline.core import PipelineResult
from pipeline.orchestrator import project_root, run_pipeline, run_single_topic

PROJ = Path(__file__).resolve().parent.parent


@pytest.fixture(autouse=True)
def isolate(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.delenv("PROJECT_DIR", raising=False)
    monkeypatch.setenv("FEP_LEAN_OUTPUT_ROOT", str(tmp_path / "output"))
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)


def test_project_root_default() -> None:
    assert project_root().resolve() == PROJ.resolve()


def test_project_root_uses_project_dir(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("PROJECT_DIR", str(tmp_path))
    assert project_root().resolve() == tmp_path.resolve()


def test_run_single_topic_unknown() -> None:
    result = run_single_topic("fep-999", mode="catalogue")
    assert isinstance(result, PipelineResult)
    assert result.status == "error"
    assert "unknown topic" in result.failure_reason


def test_run_pipeline_writes_catalogue_report() -> None:
    result = run_pipeline(mode="catalogue")
    assert result.complete is True
    assert result.mode == "catalogue"
    assert result.run_dir
    report = Path(result.run_dir)
    assert (report / "summary.json").is_file()
    assert (report / "index.md").is_file()


def test_run_pipeline_area_filter() -> None:
    result = run_pipeline(mode="catalogue", area_filter="FEP")
    assert result.complete is True
    assert result.catalogue_topics == 14


def test_run_pipeline_full_fails_without_capabilities() -> None:
    result = run_pipeline(mode="full", topic_filter=["fep-001"])
    assert result.complete is False
    assert result.status == "error"
    assert result.run_dir == ""
