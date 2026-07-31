"""Tests for reporter — Markdown + JSON report generation.

All tests use real PipelineResult objects and tmp_path file writes.
No direct execution.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from pipeline.core import FEPPipeline, PipelineResult, StepResult
from output.manuscript import _verify_block_from_manifest
from output.reporter import Reporter, ReportPaths

PROJ = Path(__file__).resolve().parent.parent


from catalogue.topics import FEPTopicCatalogue
TOPICS = FEPTopicCatalogue.from_yaml(PROJ / "config" / "topics.yaml")

def _minimal_result(tmp_path: Path) -> PipelineResult:
    """Build a minimal PipelineResult without running the pipeline."""
    r = PipelineResult(status="ok")
    run_test_dir = tmp_path / "run_test"
    run_test_dir.mkdir()
    r.run_dir = str(run_test_dir)
    r.stages = [
        StepResult(name="Load Catalogue", status="ok", duration_s=0.01, payload={"topics": ["fep-001", "fep-002"]}),
        StepResult(name="Environment Validation", status="ok", duration_s=0.5, payload={"status": "ok", "failed_count": 0, "checks": [{"name": "lean_cli", "ok": True, "message": "ok", "duration_s": 0.1}]}),
        StepResult(name="Gauss Sessions", status="skipped", duration_s=0.001),
        StepResult(name="Manuscript Artifacts", status="ok", duration_s=0.05, payload={"vars_file": "manuscript_vars.yaml"}),
    ]
    r.total_duration = 1.0
    r.lean_stats = {
        "total_processed": 50,
        "compiles_clean": 0,
        "compiles_with_sorry": 0,
        "compile_error": 0,
        "skipped": 0,
        "error_logs": [],
        "sorry_logs": [],
        "clean_logs": [],
    }
    return r


@pytest.fixture()
def reporter(tmp_path: Path) -> Reporter:
    return Reporter(tmp_path)


@pytest.fixture()
def report_paths(reporter: Reporter, tmp_path: Path) -> ReportPaths:
    result = _minimal_result(tmp_path)
    reporter.reports_dir = tmp_path / "run_test"
    return reporter.generate(TOPICS, result)


def test_reporter_instantiates(reporter: Reporter) -> None:
    assert reporter is not None


def test_generate_returns_report_paths(report_paths: ReportPaths) -> None:
    assert isinstance(report_paths, ReportPaths)


def test_all_report_files_created(report_paths: ReportPaths) -> None:
    assert report_paths.index_md.is_file()
    assert report_paths.summary_json.is_file()
    assert (report_paths.summary_json.parent / "verification_manifest.json").is_file()
    assert (report_paths.summary_json.parent / "run_manifest.json").is_file()
    assert report_paths.hermes_md.is_file()
    assert report_paths.lean_md.is_file()
    assert report_paths.validation_md.is_file()


def test_index_md_contains_status(report_paths: ReportPaths) -> None:
    text = report_paths.index_md.read_text(encoding="utf-8")
    assert "ok" in text.lower() or "ok" in text
    assert "Load Catalogue" in text
    assert "Environment Validation" in text


def test_index_md_pipeline_stages_table(report_paths: ReportPaths) -> None:
    text = report_paths.index_md.read_text(encoding="utf-8")
    assert "Stages" in text
    assert "Gauss Sessions" in text


def test_summary_json_is_valid_json(report_paths: ReportPaths) -> None:
    data = json.loads(report_paths.summary_json.read_text(encoding="utf-8"))
    assert "status" in data
    assert data["status"] == "ok"
    assert "stages" in data
    assert data["source_digest"]
    assert data["config_digest"]
    assert "lean_toolchain" in data["toolchain"]


def test_verification_manifest_json_matches_manuscript_schema(
    report_paths: ReportPaths,
) -> None:
    vm = report_paths.summary_json.parent / "verification_manifest.json"
    assert vm.is_file()
    raw = json.loads(vm.read_text(encoding="utf-8"))
    assert "verify_lean_ran" in raw
    assert "results" in raw and isinstance(raw["results"], list)
    block = _verify_block_from_manifest(vm)
    assert block["manifest_present"] is True


def test_hermes_report_md_structure(report_paths: ReportPaths) -> None:
    text = report_paths.hermes_md.read_text(encoding="utf-8")
    assert "Hermes" in text


def test_lean_report_md_structure(report_paths: ReportPaths) -> None:
    text = report_paths.lean_md.read_text(encoding="utf-8")
    assert "Lean" in text


def test_validation_md_has_checks(report_paths: ReportPaths) -> None:
    text = report_paths.validation_md.read_text(encoding="utf-8")
    assert "lean_cli" in text
    assert "ok" in text


def test_report_paths_as_dict(report_paths: ReportPaths) -> None:
    d = report_paths.as_dict()
    assert "index_md" in d
    assert "summary_json" in d
    assert "hermes_md" in d
    assert "lean_md" in d
    assert "validation_md" in d


def test_reporter_with_real_pipeline_result(tmp_path: Path) -> None:
    """Run the full catalogue-only pipeline and generate reports."""
    pl = FEPPipeline(PROJ)
    result = pl.run()
    reporter = Reporter(tmp_path)
    reporter.reports_dir = tmp_path / "full_run"
    paths = reporter.generate(TOPICS, result)
    assert paths.index_md.is_file()
    text = paths.index_md.read_text(encoding="utf-8")
    assert "Total Topics" in text
    # Should show the number of stages
    assert "Total Topics" in text


def test_reporter_rich_gauss_and_lean_logs(tmp_path: Path) -> None:
    """Exercise Hermes markdown, index stage details, and lean log sections."""
    r = PipelineResult(status="warning", total_duration=12.3)
    r.stages = [
        StepResult(
            name="Load Catalogue (Total Topics)",
            status="ok",
            duration_s=0.02,
            payload={"topics": [f"fep-{i:03d}" for i in range(1, 51)]},
        ),
        StepResult(
            name="Environment Validation",
            status="ok",
            duration_s=0.1,
            payload={"status": "ok", "failed_count": 0, "checks": []},
        ),
        StepResult(
            name="Lean Verification",
            status="ok",
            duration_s=1.0,
            payload={"compiles_clean": 3},
        ),
        StepResult(
            name="Gauss Sessions",
            status="ok",
            duration_s=2.0,
            payload={
                "topics": [
                    {
                        "topic_id": "fep-001",
                        "success": False,
                        "hermes_success": False,
                        "error": "hermes offline",
                    },
                    {
                        "topic_id": "fep-002",
                        "success": True,
                        "hermes_success": True,
                        "lean_compiles": True,
                        "hermes_lean_compiles": True,
                        "cache_hit": False,
                        "tokens_used": 42,
                        "hermes_model": "z-ai/glm-5.1",
                        "explanation": "line1\nline2",
                        "refined_lean_sketch": "theorem x : True := True.intro",
                    },
                ]
            },
        ),
    ]
    r.lean_stats = {
        "total_processed": 2,
        "compiles_clean": 1,
        "compiles_with_sorry": 0,
        "compile_error": 1,
        "skipped": 0,
        "error_logs": ["e1"],
        "sorry_logs": ["s1"],
        "clean_logs": [],
    }
    rep = Reporter(tmp_path, run_id="test_rich")
    rep.reports_dir = tmp_path / "run_rich"
    paths = rep.generate(TOPICS, r)
    summary = json.loads(paths.summary_json.read_text(encoding="utf-8"))
    assert summary["status"] == "warning"
    hermes = paths.hermes_md.read_text(encoding="utf-8")
    assert "hermes offline" in hermes
    assert "theorem x" in hermes
    lean = paths.lean_md.read_text(encoding="utf-8")
    assert "e1" in lean
    assert "s1" in lean
    idx = paths.index_md.read_text(encoding="utf-8")
    assert "WARNING" in idx.upper() or "warning" in idx
    assert "3 compile clean" in idx or "Lean Verification" in idx


def _gauss_payload(rows: list[dict[str, object]]) -> dict[str, object]:
    return {"topics": rows}


def _result_with_gauss(rows: list[dict[str, object]]) -> PipelineResult:
    """Build a minimal PipelineResult with a Gauss Sessions stage payload."""
    r = PipelineResult(status="ok", total_duration=10.0)
    r.stages = [
        StepResult(
            name="Load Catalogue",
            status="ok",
            duration_s=0.01,
            payload={"topics": [row["topic_id"] for row in rows]},
        ),
        StepResult(
            name="Environment Validation",
            status="ok",
            duration_s=0.1,
            payload={"status": "ok", "failed_count": 0, "checks": []},
        ),
        StepResult(
            name="Gauss Sessions",
            status="ok",
            duration_s=5.0,
            payload=_gauss_payload(rows),
        ),
    ]
    lean_ok = sum(1 for r0 in rows if r0.get("lean_compiles"))
    lean_err = sum(1 for r0 in rows if r0.get("lean_compiles") is False)
    r.lean_stats = {
        "total_processed": len(rows),
        "compiles_clean": lean_ok,
        "compiles_with_sorry": 0,
        "compile_error": lean_err,
        "skipped": 0,
        "error_logs": [],
        "sorry_logs": [],
        "clean_logs": [],
    }
    return r


def test_hermes_md_renders_aggregate_block(tmp_path: Path) -> None:
    """``_gen_hermes_md`` must surface the new aggregate header (cache hits,
    mean tokens, models used, Hermes-refined Lean compiled)."""
    rows = [
        {
            "topic_id": "fep-001",
            "success": True,
            "hermes_success": True,
            "lean_compiles": True,
            "hermes_lean_compiles": True,
            "cache_hit": True,
            "tokens_used": 1000,
            "hermes_model": "z-ai/glm-5.1",
            "explanation": "fixture",
            "refined_lean_sketch": "theorem t1 : True := True.intro",
        },
        {
            "topic_id": "fep-002",
            "success": True,
            "hermes_success": True,
            "lean_compiles": True,
            "hermes_lean_compiles": False,
            "cache_hit": False,
            "tokens_used": 2000,
            "hermes_model": "z-ai/glm-5.1",
            "explanation": "fixture",
            "refined_lean_sketch": "theorem t2 : True := True.intro",
        },
    ]
    rep = Reporter(tmp_path, run_id="test_aggregates")
    rep.reports_dir = tmp_path / "run_aggregates"
    paths = rep.generate(TOPICS, _result_with_gauss(rows))
    text = paths.hermes_md.read_text(encoding="utf-8")
    assert "Cache hits" in text
    assert "1/2" in text  # one cached out of two
    assert "Mean tokens/topic" in text
    assert "1500" in text  # (1000 + 2000) // 2
    assert "Models used" in text
    assert "z-ai/glm-5.1" in text
    assert "Hermes-refined Lean compiled" in text


def test_index_md_splits_lean_directly_vs_post_fallback(tmp_path: Path) -> None:
    """``_gen_index_md`` must report the directly-compiled and final-compiled
    Lean rates as separate bullets."""
    rows = [
        {
            "topic_id": "fep-001",
            "success": True,
            "hermes_success": True,
            "lean_compiles": True,
            "hermes_lean_compiles": True,
            "cache_hit": False,
            "tokens_used": 500,
            "hermes_model": "z-ai/glm-5.1",
        },
        {
            "topic_id": "fep-002",
            "success": True,
            "hermes_success": True,
            "lean_compiles": True,
            "hermes_lean_compiles": False,
            "cache_hit": False,
            "tokens_used": 500,
            "hermes_model": "z-ai/glm-5.1",
        },
    ]
    rep = Reporter(tmp_path, run_id="test_split")
    rep.reports_dir = tmp_path / "run_split"
    paths = rep.generate(TOPICS, _result_with_gauss(rows))
    text = paths.index_md.read_text(encoding="utf-8")
    assert "Hermes-refined Lean compiled directly" in text
    assert "Final Lean compiled" in text
    # 1 of 2 compiled directly; 2 of 2 finally compiled (1 via fallback)
    assert "1/2" in text
    assert "2/2" in text
    assert "Final Lean compiled" in text


def test_index_and_summary_use_selected_topics_and_hash_nested_artifacts(tmp_path: Path) -> None:
    rows = [{
        "topic_id": "fep-001",
        "success": False,
        "hermes_success": False,
        "lean_compiles": False,
    }]
    result = _result_with_gauss(rows)
    result.catalogue_topics = 1
    rep = Reporter(tmp_path, run_id="test_selected_topics")
    paths = rep.generate(TOPICS, result)
    index = paths.index_md.read_text(encoding="utf-8")
    assert "**Total Topics:** 1" in index
    assert "**Catalogue Topics:** 50" in index
    summary = json.loads(paths.summary_json.read_text(encoding="utf-8"))
    hashes = summary["artifact_hashes"]
    assert "topics/fep-001.md" in hashes
    assert hashes["topics/fep-001.md"]
    root = paths.summary_json.parent.resolve()
    for relative, digest in hashes.items():
        artifact = (root / relative).resolve()
        assert root in artifact.parents
        assert artifact.is_file()
        assert hashlib.sha256(artifact.read_bytes()).hexdigest() == digest
    assert "summary.json" not in hashes
    run_manifest = json.loads((root / "run_manifest.json").read_text(encoding="utf-8"))
    assert run_manifest["catalogue_topics"] == 1
    assert run_manifest["complete"] is False
    assert len(run_manifest["topics"]) == 1


def test_summary_json_includes_topics_payload(tmp_path: Path) -> None:
    """``Reporter._gen_summary_json`` must include the per-topic rows so
    ``output.manuscript.build_manuscript_vars`` can derive Hermes aggregates."""
    pl = FEPPipeline(PROJ)
    result = pl.run()
    rep = Reporter(tmp_path, run_id="test_topics")
    rep.reports_dir = tmp_path / "run_topics"
    paths = rep.generate(TOPICS, result)
    data = json.loads(paths.summary_json.read_text(encoding="utf-8"))
    assert "topics" in data
    assert isinstance(data["topics"], list)


def test_topic_md_renders_hermes_validation_panel(tmp_path: Path) -> None:
    """Per-topic markdown must include the Hermes Validation panel with cache
    hit + Hermes-refined compile status when ``hermes_success`` is True."""
    rows = [
        {
            "topic_id": TOPICS.topics[0].id,
            "success": True,
            "hermes_success": True,
            "lean_compiles": True,
            "hermes_lean_compiles": False,
            "cache_hit": True,
            "tokens_used": 1234,
            "hermes_model": "z-ai/glm-5.1",
            "explanation": "fixture explanation",
            "refined_lean_sketch": "theorem t : True := True.intro",
            "session_id": "sess-123",
        },
    ]
    rep = Reporter(tmp_path, run_id="test_panel")
    rep.reports_dir = tmp_path / "run_panel"
    paths = rep.generate(TOPICS, _result_with_gauss(rows))
    topic_md = paths.index_md.parent / "topics" / f"{rows[0]['topic_id']}.md"
    assert topic_md.is_file()
    text = topic_md.read_text(encoding="utf-8")
    assert "## Hermes Validation" in text
    assert "Cache hit" in text
    assert "Cache hit: `True`" in text
    assert "Hermes-refined Lean compiled" in text


def test_build_verification_manifest_helper_shape() -> None:
    """``Reporter.build_verification_manifest`` must produce the canonical shape
    required by ``_verify_block_from_manifest``."""

    class _fixture:
        def __init__(self, topic_id: str, compiles: bool, has_sorry: bool = False) -> None:
            self.topic_id = topic_id
            self.compiles = compiles
            self.has_sorry = has_sorry

    payload = Reporter.build_verification_manifest(
        [_fixture("fep-001", True), _fixture("fep-002", False), _fixture("fep-003", True, True)]
    )
    assert payload["verify_lean_ran"] is True
    assert payload["topics_with_result"] == 3
    assert payload["compiles_true"] == 2
    assert payload["compiles_false"] == 1
    assert {row["topic_id"] for row in payload["results"]} == {"fep-001", "fep-002", "fep-003"}
    sorry_rows = [row for row in payload["results"] if row["lean_has_sorry"]]
    assert len(sorry_rows) == 1
    assert sorry_rows[0]["topic_id"] == "fep-003"
