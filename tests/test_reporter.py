"""Tests for reporter — Markdown + JSON report generation.

All tests use real PipelineResult objects and tmp_path file writes.
No direct execution.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from catalogue.topics import FEPTopicCatalogue
from output.manuscript import _verify_block_from_manifest
from output.reporter import Reporter, ReportPaths, validate_report_receipt
from pipeline.core import FEPPipeline, PipelineResult, StepResult

PROJ = Path(__file__).resolve().parent.parent


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


def test_validate_report_receipt_accepts_catalogue_bundle(tmp_path: Path) -> None:
    result = PipelineResult(
        status="ok",
        mode="catalogue",
        complete=True,
        catalogue_topics=50,
        verified_topics=0,
    )
    result.stages = [
        StepResult(name="Load Catalogue", status="ok"),
        StepResult(name="Environment Validation", status="ok", payload={"status": "ok", "checks": []}),
        StepResult(name="Gauss Sessions", status="not_run"),
        StepResult(name="Manuscript Artifacts", status="ok"),
    ]
    rep = Reporter(tmp_path, run_id="run_catalogue_receipt")
    paths = rep.generate(TOPICS, result)

    receipt = validate_report_receipt(paths.root)

    assert receipt["valid"] is True
    assert receipt["claim_ready"] is False
    assert receipt["mode"] == "catalogue"
    assert receipt["selected_topics"] == 50
    assert receipt["checked_artifacts"] >= 6


def test_validate_report_receipt_accepts_complete_full_bundle(tmp_path: Path) -> None:
    rows = [{
        "topic_id": "fep-001",
        "success": True,
        "hermes_success": True,
        "lean_compiles": True,
        "lean_has_sorry": False,
        "verification_source": "hermes_refined",
    }]
    result = _result_with_gauss(rows)
    result.complete = True
    result.catalogue_topics = 1
    result.verified_topics = 1
    rep = Reporter(tmp_path, run_id="run_full_receipt")
    paths = rep.generate(TOPICS, result)

    receipt = validate_report_receipt(paths.root, require_complete=True)

    assert receipt["valid"] is True
    assert receipt["claim_ready"] is True
    assert receipt["mode"] == "full"
    assert receipt["selected_topics"] == receipt["verified_topics"] == 1
    assert receipt["errors"] == []


def test_validate_report_receipt_rejects_string_verification_flags(tmp_path: Path) -> None:
    rows = [{
        "topic_id": "fep-001",
        "success": True,
        "hermes_success": True,
        "lean_compiles": True,
        "lean_has_sorry": False,
        "verification_source": "hermes_refined",
    }]
    result = _result_with_gauss(rows)
    result.complete = True
    result.catalogue_topics = 1
    result.verified_topics = 1
    rep = Reporter(tmp_path, run_id="run_string_flags_receipt")
    paths = rep.generate(TOPICS, result)

    summary = json.loads(paths.summary_json.read_text(encoding="utf-8"))
    verification = json.loads((paths.root / "verification_manifest.json").read_text(encoding="utf-8"))
    summary["topics"][0].update({"success": "true", "lean_compiles": "true", "lean_has_sorry": "false"})
    verification["results"][0].update({"compiles": "true", "lean_has_sorry": "false"})
    paths.summary_json.write_text(json.dumps(summary), encoding="utf-8")
    (paths.root / "verification_manifest.json").write_text(json.dumps(verification), encoding="utf-8")

    receipt = validate_report_receipt(paths.root, require_complete=True)

    assert receipt["valid"] is False
    assert any("summary topic fep-001 success must be a boolean" in error for error in receipt["errors"])
    assert any("summary topic fep-001 lean_compiles must be a boolean" in error for error in receipt["errors"])
    assert any("summary topic fep-001 lean_has_sorry must be a boolean" in error for error in receipt["errors"])
    assert any("verification topic fep-001 compiles must be a boolean" in error for error in receipt["errors"])
    assert any("verification topic fep-001 lean_has_sorry must be a boolean" in error for error in receipt["errors"])
    assert "complete full-mode receipt is required" in receipt["errors"]


def test_validate_report_receipt_detects_tampering_and_path_escape(tmp_path: Path) -> None:
    rep = Reporter(tmp_path, run_id="run_tamper_receipt")
    paths = rep.generate(TOPICS, _minimal_result(tmp_path))
    root = paths.root

    paths.index_md.write_text(paths.index_md.read_text(encoding="utf-8") + "tampered\n", encoding="utf-8")
    summary = json.loads(paths.summary_json.read_text(encoding="utf-8"))
    summary["artifact_hashes"]["../outside.txt"] = "0" * 64
    paths.summary_json.write_text(json.dumps(summary), encoding="utf-8")

    receipt = validate_report_receipt(root)

    assert receipt["valid"] is False
    assert any("hash mismatch" in error for error in receipt["errors"])
    assert any("escapes report directory" in error for error in receipt["errors"])


def test_validate_report_receipt_rejects_missing_and_malformed_manifests(tmp_path: Path) -> None:
    missing = validate_report_receipt(tmp_path / "missing_receipt")
    assert missing["valid"] is False
    assert any("report directory is missing" in error for error in missing["errors"])

    root = tmp_path / "malformed_receipt"
    root.mkdir()
    (root / "summary.json").write_text("{", encoding="utf-8")
    (root / "run_manifest.json").write_text("[]", encoding="utf-8")

    receipt = validate_report_receipt(root)

    assert receipt["valid"] is False
    assert any("invalid summary.json" in error for error in receipt["errors"])
    assert any("run_manifest.json must contain a JSON object" in error for error in receipt["errors"])
    assert any("missing verification_manifest.json" in error for error in receipt["errors"])


def test_validate_report_receipt_checks_summary_types_and_required_hashes(tmp_path: Path) -> None:
    rep = Reporter(tmp_path, run_id="run_invalid_summary_receipt")
    paths = rep.generate(
        TOPICS,
        PipelineResult(status="ok", mode="catalogue", complete=True, catalogue_topics=50),
    )
    summary = json.loads(paths.summary_json.read_text(encoding="utf-8"))
    summary.update(
        {
            "mode": "unsupported",
            "complete": "yes",
            "catalogue_topics": True,
            "verified_topics": -1,
            "topics": "not-a-list",
            "source_digest": "bad",
            "config_digest": None,
            "toolchain": [],
            "artifact_hashes": [],
        }
    )
    paths.summary_json.write_text(json.dumps(summary), encoding="utf-8")

    receipt = validate_report_receipt(paths.root)

    assert receipt["valid"] is False
    expected_errors = (
        "summary mode is unsupported",
        "summary complete must be a boolean",
        "summary catalogue_topics must be a non-negative integer",
        "summary verified_topics must be a non-negative integer",
        "summary topics must be a list of objects",
        "summary source_digest must be a lowercase SHA-256 digest",
        "summary config_digest must be a lowercase SHA-256 digest",
        "summary toolchain must be an object",
        "summary artifact_hashes must be an object",
        "required artifacts are not hashed",
    )
    assert all(any(expected in error for error in receipt["errors"]) for expected in expected_errors), receipt["errors"]


def test_validate_report_receipt_rejects_invalid_artifact_entries(tmp_path: Path) -> None:
    rep = Reporter(tmp_path, run_id="run_invalid_artifact_receipt")
    paths = rep.generate(TOPICS, _minimal_result(tmp_path))
    summary = json.loads(paths.summary_json.read_text(encoding="utf-8"))
    hashes = summary["artifact_hashes"]
    hashes[""] = "0" * 64
    hashes["/absolute.txt"] = "0" * 64
    hashes["."] = "0" * 64
    hashes["missing.txt"] = "0" * 64
    hashes["index.md"] = "not-a-digest"
    paths.summary_json.write_text(json.dumps(summary), encoding="utf-8")

    receipt = validate_report_receipt(paths.root)

    assert receipt["valid"] is False
    assert any("non-empty strings" in error for error in receipt["errors"])
    assert sum("escapes report directory" in error for error in receipt["errors"]) >= 2
    assert any("hashed artifact is missing: missing.txt" in error for error in receipt["errors"])
    assert any("invalid SHA-256 digest for artifact: index.md" in error for error in receipt["errors"])
    assert any("required artifacts are not hashed" in error for error in receipt["errors"])


def test_validate_report_receipt_reconciles_rows_and_verification_counters(tmp_path: Path) -> None:
    rows = [
        {
            "topic_id": "fep-001",
            "success": True,
            "hermes_success": True,
            "lean_compiles": True,
            "lean_has_sorry": False,
            "verification_source": "hermes_refined",
        }
    ]
    result = _result_with_gauss(rows)
    result.catalogue_topics = 1
    result.verified_topics = 1
    rep = Reporter(tmp_path, run_id="run_inconsistent_rows_receipt")
    paths = rep.generate(TOPICS, result)

    summary = json.loads(paths.summary_json.read_text(encoding="utf-8"))
    run_manifest = json.loads((paths.root / "run_manifest.json").read_text(encoding="utf-8"))
    verification = json.loads((paths.root / "verification_manifest.json").read_text(encoding="utf-8"))
    summary["topics"] = [{"topic_id": "fep-001"}, {}]
    run_manifest["topics"] = {"topic_id": "fep-001"}
    verification["results"] = [{"topic_id": "fep-001", "compiles": True, "lean_has_sorry": True}]
    verification.update(
        {
            "verify_lean_ran": False,
            "topics_with_result": 0,
            "compiles_true": 0,
            "compiles_false": 1,
        }
    )
    paths.summary_json.write_text(json.dumps(summary), encoding="utf-8")
    (paths.root / "run_manifest.json").write_text(json.dumps(run_manifest), encoding="utf-8")
    (paths.root / "verification_manifest.json").write_text(json.dumps(verification), encoding="utf-8")

    receipt = validate_report_receipt(paths.root)

    assert receipt["valid"] is False
    expected_errors = (
        "run manifest topics must be a list of objects",
        "summary topics contains a row without a topic_id",
        "summary and run manifest topic rows disagree",
        "full-mode summary topic rows do not match selected-topic count",
        "run manifest topic rows do not match the mode contract",
        "verification manifest verify_lean_ran disagrees with its rows",
        "verification manifest topics_with_result disagrees with its rows",
        "verification manifest compiles_true disagrees with its rows",
        "verification manifest compiles_false disagrees with its rows",
        "verification compile flag disagrees for fep-001",
        "verification sorry flag disagrees for fep-001",
    )
    assert all(any(expected in error for error in receipt["errors"]) for expected in expected_errors)


def test_validate_report_receipt_keeps_full_mode_claim_boundary_explicit(tmp_path: Path) -> None:
    rows = [
        {
            "topic_id": "fep-001",
            "success": True,
            "hermes_success": True,
            "lean_compiles": True,
            "lean_has_sorry": False,
            "verification_source": "hermes_refined",
        }
    ]
    result = _result_with_gauss(rows)
    result.complete = True
    result.catalogue_topics = 1
    result.verified_topics = 1
    rep = Reporter(tmp_path, run_id="run_incomplete_full_receipt")
    paths = rep.generate(TOPICS, result)

    summary = json.loads(paths.summary_json.read_text(encoding="utf-8"))
    run_manifest = json.loads((paths.root / "run_manifest.json").read_text(encoding="utf-8"))
    summary["topics"] = []
    summary["catalogue_topics"] = 0
    summary["verified_topics"] = 0
    summary["status"] = "error"
    run_manifest["topics"] = []
    run_manifest["catalogue_topics"] = 0
    run_manifest["verified_topics"] = 0
    run_manifest["verification_source"] = "unexpected"
    run_manifest["lean_clean"] = False
    paths.summary_json.write_text(json.dumps(summary), encoding="utf-8")
    (paths.root / "run_manifest.json").write_text(json.dumps(run_manifest), encoding="utf-8")

    receipt = validate_report_receipt(paths.root, require_complete=True)

    assert receipt["valid"] is False
    assert receipt["claim_ready"] is False
    assert any("must select at least one topic" in error for error in receipt["errors"])
    assert any("summary must have status ok" in error for error in receipt["errors"])
    assert any("wrong verification source" in error for error in receipt["errors"])
    assert any("must mark lean_clean true" in error for error in receipt["errors"])
    assert "complete full-mode receipt is required" in receipt["errors"]


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
