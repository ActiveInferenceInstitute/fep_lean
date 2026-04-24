"""Test FEPPipeline exception paths with real missing files (Zero-Mock policy)."""

import pytest
from pathlib import Path
from pipeline.core import FEPPipeline



def test_pipeline_missing_catalogue(tmp_path: Path) -> None:
    # A totally empty directory will cause FEPTopicCatalogue to fail
    pl = FEPPipeline(project_root=tmp_path)
    res = pl.run()
    
    # The pipeline should abort at stage 1 or 2 with an error status
    assert res.status == "error"
    
    # We should have an error step
    assert any(s.status == "error" for s in res.stages)

def test_pipeline_validation_warning(tmp_path: Path) -> None:
    from pipeline.core import FEPPipeline
    
    # Create config dir but missing other environment files
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    topics_yaml = config_dir / "topics.yaml"
    topics_yaml.write_text("topics:\n  - id: fep-001\n    area: FEP\n")
    
    pl = FEPPipeline(project_root=tmp_path)
    # the environment validation will fail (missing manuscript config, etc.)
    # which causes the pipeline status to demote to "warning"
    res = pl.run()
    
    # It runs fine but with warning
    assert res.status == "warning"

def test_pipeline_gauss_skips(tmp_path: Path) -> None:
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    topics_yaml = config_dir / "topics.yaml"
    topics_yaml.write_text("topics: []\n")
    
    pl = FEPPipeline(project_root=tmp_path)
    res = pl.run()
    assert res.status in {"ok", "warning"}
    
    # Check that Gauss Sessions was skipped or handled OK
    names = [s.name for s in res.stages]
    # "Gauss Sessions" is present
    assert "Gauss Sessions" in names
