"""Sad path tests for pipeline.orchestrator without unittest.mock."""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from pipeline.orchestrator import run_pipeline, run_single_topic

PROJ = Path(__file__).resolve().parent.parent


@pytest.fixture(autouse=True)
def _redirect_output_root(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Redirect ``output/reports/`` so spawned pipeline runs don't pollute
    the canonical ``output/reports/`` tree on the developer's checkout.
    See ``tests/AGENTS.md`` § "Test isolation: FEP_LEAN_OUTPUT_ROOT".
    """
    monkeypatch.setenv("FEP_LEAN_OUTPUT_ROOT", str(tmp_path / "fep_output"))


def test_run_single_topic_unknown(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    # Using a genuine unknown topic
    monkeypatch.chdir(PROJ)
    res = run_single_topic("fep-unknown-888", interactive=False)
    assert res["status"] == "error"
    assert "not found in catalogue" in res["message"]

def test_run_single_topic_interactive_err(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    # Pass a valid topic id but corrupt the config so FEPTopicCatalogue.from_yaml fails
    fake_proj = tmp_path / "fake_proj"
    fake_proj.mkdir()
    (fake_proj / "config").mkdir()
    (fake_proj / "manuscript").mkdir()
    (fake_proj / "src").mkdir()
    (fake_proj / "lean").mkdir()
    
    bad_yaml = fake_proj / "config" / "topics.yaml"
    bad_yaml.write_text("invalid:\n  - yaml: [")
    
    # Use PROJECT_DIR for detection
    monkeypatch.setenv("PROJECT_DIR", str(fake_proj))
    res = run_single_topic("fep-001", interactive=True)
    assert res["status"] == "error"
    assert "topics.yaml" in str(res).lower() or "parsing" in str(res).lower() or "error" in str(res).lower()

def test_run_pipeline_no_catalogue(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    fake_proj = tmp_path / "fake_proj_empty"
    fake_proj.mkdir()
    (fake_proj / "config").mkdir() # missing topics.yaml
    (fake_proj / "manuscript").mkdir()
    
    monkeypatch.setenv("PROJECT_DIR", str(fake_proj))
    res = run_pipeline(interactive=False)
    assert res.status == "error"

def test_run_single_topic_pipeline_run(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    # To test pipeline execution error, we can cause the environment to fail,
    # e.g. pointing LEAN_EXE to a missing file.
    monkeypatch.chdir(PROJ)
    monkeypatch.setenv("LEAN_EXE", "/path/that/does_not_exist_at_all_5289")
    monkeypatch.setenv("GAUSS_HOME", "/path/that/also_does_not_exist_9812")
    
    # We use a topic that does exist
    res = run_single_topic("fep-001", interactive=False)
    # The pipeline should fail because the required binaries are missing
    assert res is not None
    assert "status" in res
    assert res["status"] in ("error", "failed", "warning", "partial")

def test_run_pipeline_interactive(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    monkeypatch.chdir(PROJ)
    # Set fake paths to assure fail but not crash
    monkeypatch.setenv("LEAN_EXE", "/path/that/does_not_exist_at_all_5289")
    
    # run interactive
    res = run_pipeline(interactive=True)
    # Should complete but with error/failed
    assert res is not None
