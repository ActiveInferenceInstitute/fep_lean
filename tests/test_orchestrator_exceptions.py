import pytest
from pathlib import Path

def test_run_pipeline_orchestrator_exceptions(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    import pipeline.orchestrator as orchestrator
    
    # Set PROJECT_DIR so FEPPipeline organically targets tmp_path
    monkeypatch.setenv("PROJECT_DIR", str(tmp_path))
    
    # We trigger an organic exception from the reporting stage instead of monkeypatching.
    # Write a valid stub catalogue so pipeline.run succeeds gracefully up to the Reporter.
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "topics.yaml").write_text("topics:\n  - id: fep-001\n    title: Test\n    nl: test\n    lean_sketch: test\n")
    
    # Make the output dir unwritable so reporter.generate() throws PermissionError natively
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    output_dir.chmod(0o555)
    
    try:
        res = orchestrator.run_pipeline()
        pytest.fail("Expected PermissionError from Reporter to bubble up out of run_pipeline")
    except (PermissionError, OSError):
        pass # Expected
    finally:
        output_dir.chmod(0o755)

