"""Edge-case tests for uncovered code paths.

Tests input validation, wrap-code logic, empty-catalogue handling,
and malformed data resilience.  All real objects — no direct execution.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from catalogue.topics import CatalogueValidationError, FEPTopicCatalogue
from gauss.client import OpenGaussClient
from verification.lean_verifier import LeanVerifier

PROJ = Path(__file__).resolve().parent.parent
LEAN_DIR = PROJ / "lean"


# ── OpenGaussClient input validation ────────────────────────────────────────


@pytest.fixture()
def client(tmp_path: Path) -> OpenGaussClient:
    return OpenGaussClient(gauss_home=tmp_path / "gauss_home")


def test_create_session_empty_topic_id_raises(client: OpenGaussClient) -> None:
    with pytest.raises(ValueError, match="topic_id cannot be empty"):
        client.create_session("", "FEP")


def test_create_session_whitespace_topic_id_raises(client: OpenGaussClient) -> None:
    with pytest.raises(ValueError, match="topic_id cannot be empty"):
        client.create_session("   ", "FEP")


def test_create_session_valid_topic_id_ok(client: OpenGaussClient) -> None:
    sid = client.create_session("fep-001", "FEP")
    assert "fep-001" in sid


# ── LeanVerifier._wrap_lean_code ─────────────────────────────────────────────


def test_wrap_lean_code_no_import_adds_preamble() -> None:
    v = LeanVerifier(lean_dir=LEAN_DIR, project_root=PROJ)
    code = "theorem foo : True := trivial"
    wrapped = v._wrap_lean_code(code)
    assert wrapped.startswith("import Mathlib")
    assert "theorem foo" in wrapped


def test_wrap_lean_code_with_import_preserves() -> None:
    v = LeanVerifier(lean_dir=LEAN_DIR, project_root=PROJ)
    code = "import Mathlib\ntheorem bar : True := trivial"
    wrapped = v._wrap_lean_code(code)
    assert wrapped == code


def test_wrap_lean_code_whitespace_before_import() -> None:
    """Whitespace-prefixed imports should still get preamble (strip() handles it)."""
    v = LeanVerifier(lean_dir=LEAN_DIR, project_root=PROJ)
    code = "  import Mathlib\ntheorem baz : True := trivial"
    wrapped = v._wrap_lean_code(code)
    # strip() sees "import" so no preamble added
    assert wrapped == code


def test_wrap_lean_code_open_without_import_gets_preamble() -> None:
    v = LeanVerifier(lean_dir=LEAN_DIR, project_root=PROJ)
    code = "open MeasureTheory\ntheorem qux : True := trivial"
    wrapped = v._wrap_lean_code(code)
    assert wrapped.startswith("import Mathlib")
    assert "open MeasureTheory\ntheorem qux" in wrapped


def test_wrap_lean_code_empty_string() -> None:
    v = LeanVerifier(lean_dir=LEAN_DIR, project_root=PROJ)
    wrapped = v._wrap_lean_code("")
    assert "import Mathlib" in wrapped


def test_wrap_lean_code_multiline_imports() -> None:
    v = LeanVerifier(lean_dir=LEAN_DIR, project_root=PROJ)
    code = "import Mathlib\nimport Mathlib.MeasureTheory\ntheorem t : True := trivial"
    wrapped = v._wrap_lean_code(code)
    assert wrapped == code


# ── Empty catalogue handling ─────────────────────────────────────────────────


def test_empty_catalogue_is_rejected(tmp_path: Path) -> None:
    """An empty source cannot be used as a verification catalogue."""
    yaml_path = tmp_path / "topics.yaml"
    yaml_path.write_text("topics: []\n", encoding="utf-8")
    with pytest.raises(CatalogueValidationError):
        FEPTopicCatalogue.from_yaml(yaml_path)


def test_catalogue_from_yaml_real() -> None:
    c = FEPTopicCatalogue.from_yaml(PROJ / "config" / "topics.yaml")
    assert len(c.topics) == 50
    s = c.summary()
    assert s["total_topics"] == 50
    assert sum(s["areas"].values()) == 50


# ── PipelineResult computed properties ───────────────────────────────────────


def test_pipeline_result_with_empty_stages() -> None:
    from pipeline.core import PipelineResult

    pr = PipelineResult(status="ok", total_duration=1.0, stages=[])
    assert pr.status == "ok"
    assert pr.stats["stages_ok"] == 0
    assert pr.stats["topics_total"] == 0


def test_step_result_creation() -> None:
    from pipeline.core import StepResult

    sr = StepResult(name="Test", status="ok", message="done", duration_s=0.1)
    assert sr.name == "Test"
    assert sr.status == "ok"
    assert sr.error is None


def test_step_result_with_error() -> None:
    from pipeline.core import StepResult

    sr = StepResult(name="Test", status="error", message="fail", duration_s=0.0, error="boom")
    assert sr.error == "boom"
    assert sr.status == "error"


# ── Verify manifest edge cases ──────────────────────────────────────────────


def test_verify_block_missing_keys(tmp_path: Path) -> None:
    from output.manuscript import _verify_block_from_manifest

    p = tmp_path / "manifest.json"
    p.write_text(json.dumps({"random_key": 42}), encoding="utf-8")
    b = _verify_block_from_manifest(p)
    assert b["manifest_present"] is True
    # Missing topics_with_result and results → defaults to 0
    assert b["topics_with_result"] == 0


def test_verify_block_non_integer_topics(tmp_path: Path) -> None:
    from output.manuscript import _verify_block_from_manifest

    p = tmp_path / "manifest.json"
    p.write_text(json.dumps({"topics_with_result": "fifty"}), encoding="utf-8")
    b = _verify_block_from_manifest(p)
    assert b["manifest_present"] is True


# ── Hermes config edge cases ────────────────────────────────────────────────


def test_hermes_config_defaults() -> None:
    from llm.hermes import HermesConfig

    cfg = HermesConfig()
    assert cfg.model != ""
    assert cfg.timeout_s > 0
    assert cfg.max_tokens > 0


def test_hermes_config_disabled_without_key() -> None:
    from llm.hermes import HermesConfig

    cfg = HermesConfig(api_key="", enabled=False)
    assert cfg.enabled is False


def test_hermes_result_dataclass() -> None:
    from llm.hermes import HermesResult

    r = HermesResult(
        success=False,
        model_used="test",
        error="no key",
        duration_s=0.0,
        topic_id="fep-001",
    )
    assert r.success is False
    assert r.topic_id == "fep-001"
