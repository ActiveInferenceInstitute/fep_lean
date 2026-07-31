"""Manuscript projections and deterministic generated appendices."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

from catalogue.topics import FEPTopicCatalogue

UNIFIED_FORMALISM_CATALOGUE_FILENAME = "09z_unified_formalism_catalogue.md"


def _read_toolchain_vars(project_root: Path) -> dict[str, str]:
    lean_dir = Path(project_root) / "lean"
    toolchain = (lean_dir / "lean-toolchain").read_text(encoding="utf-8").strip() if (lean_dir / "lean-toolchain").is_file() else ""
    lean_version = toolchain.rsplit(":", 1)[-1].removeprefix("v") if toolchain else ""
    mathlib_tag = ""
    lakefile = lean_dir / "lakefile.lean"
    if lakefile.is_file():
        text = lakefile.read_text(encoding="utf-8")
        match = re.search(r'@\s*"([^"]+)"', text)
        if match:
            mathlib_tag = match.group(1)
    manifest = lean_dir / "lake-manifest.json"
    if not mathlib_tag and manifest.is_file():
        try:
            data = json.loads(manifest.read_text(encoding="utf-8"))
            for package in data.get("packages", []):
                if package.get("name") == "mathlib":
                    mathlib_tag = str(package.get("inputRev", ""))
                    break
        except (OSError, ValueError, TypeError):
            pass
    return {"lean_toolchain": toolchain, "lean_version": lean_version, "mathlib_tag": mathlib_tag}


def _get_latest_verification_manifest(project_root: Path, output_root: Path | None = None) -> Path | None:
    reports_root = Path(output_root) if output_root is not None else Path(project_root) / "output"
    candidates = list((reports_root / "reports").glob("*/verification_manifest.json"))
    return max(candidates, key=lambda p: p.stat().st_mtime) if candidates else None


def _verify_block_from_manifest(path: Path | None) -> dict[str, Any]:
    base = {"manifest_present": False, "verify_lean_ran": False, "topics_with_result": 0, "compiles_true": 0, "compiles_false": 0}
    if path is None or not path.is_file():
        return base
    base["manifest_present"] = True
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return base
    results = data.get("results") if isinstance(data, dict) else []
    if not isinstance(results, list):
        results = []
    base["verify_lean_ran"] = bool(data.get("verify_lean_ran", False))
    base["topics_with_result"] = int(data.get("topics_with_result", len(results))) if str(data.get("topics_with_result", len(results))).isdigit() else len(results)
    base["compiles_true"] = int(data.get("compiles_true", sum(bool(r.get("compiles")) for r in results if isinstance(r, dict))))
    base["compiles_false"] = int(data.get("compiles_false", max(0, len(results) - base["compiles_true"])))
    return base


def _hermes_block_from_summary(path: Path | None) -> dict[str, Any]:
    keys: dict[str, Any] = {"summary_present": False, "run_id": "", "processed": 0, "success_count": 0, "cache_hits": 0, "tokens_total": 0, "tokens_mean": 0, "hermes_lean_compiles_count": 0, "primary_model": "", "models_used": "", "model_fallback_count": 0, "network_retry_count": 0, "chain_advance_reasons": {}, "chain_advance_reasons_summary": "none"}
    if path is None or not path.is_file():
        return keys
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return keys
    rows = data.get("topics", []) if isinstance(data, dict) else []
    rows = rows if isinstance(rows, list) else []
    models = [str(r.get("hermes_model", "")) for r in rows if isinstance(r, dict) and r.get("hermes_model")]
    counts: dict[str, int] = {}
    reasons: dict[str, int] = {}
    for row in rows:
        if not isinstance(row, dict):
            continue
        model = str(row.get("hermes_model", ""))
        if model:
            counts[model] = counts.get(model, 0) + 1
        reason = str(row.get("chain_advance_reason", ""))
        if reason:
            reasons[reason] = reasons.get(reason, 0) + 1
    tokens = [int(r.get("tokens_used", 0) or 0) for r in rows if isinstance(r, dict) and int(r.get("tokens_used", 0) or 0) > 0]
    run_id = str(data.get("run_id", ""))
    if run_id and not run_id.startswith("run_"):
        run_id = "run_" + run_id
    primary_model = max(counts, key=lambda model: counts[model]) if counts else ""
    keys.update({
        "summary_present": True,
        "run_id": run_id,
        "processed": len(rows),
        "success_count": sum(bool(r.get("hermes_success")) for r in rows if isinstance(r, dict)),
        "cache_hits": sum(bool(r.get("cache_hit")) for r in rows if isinstance(r, dict)),
        "tokens_total": sum(tokens),
        "tokens_mean": sum(tokens) // len(tokens) if tokens else 0,
        "hermes_lean_compiles_count": sum(bool(r.get("hermes_lean_compiles")) for r in rows if isinstance(r, dict)),
        "primary_model": primary_model,
        "models_used": ", ".join(sorted(set(models))),
        "model_fallback_count": max(0, len(models) - counts.get(primary_model, 0)),
        "network_retry_count": sum(int(r.get("network_retries", 0) or 0) for r in rows if isinstance(r, dict)),
        "chain_advance_reasons": reasons,
    })
    keys["chain_advance_reasons_summary"] = ", ".join(f"{n}× {reason}" for reason, n in sorted(reasons.items(), key=lambda item: (-item[1], item[0]))) or "none"
    return keys


def _count_test_cases(project_root: Path) -> int:
    cache = Path(project_root) / "output" / ".cache" / "tests_collected.json"
    tests = list((Path(project_root) / "tests").glob("test_*.py"))
    if cache.is_file() and tests and cache.stat().st_mtime >= max(p.stat().st_mtime for p in tests):
        try:
            return int(json.loads(cache.read_text(encoding="utf-8")).get("collected", 0))
        except (OSError, ValueError, TypeError):
            pass
    try:
        proc = subprocess.run([sys.executable, "-m", "pytest", "tests", "--collect-only", "-q"], cwd=project_root, capture_output=True, text=True, timeout=120)
        count = 0
        match = re.search(r"(\d+) tests? collected", proc.stdout + proc.stderr)
        if match:
            count = int(match.group(1))
    except (OSError, subprocess.SubprocessError):
        count = len(tests)
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_text(json.dumps({"collected": count, "source_files": len(tests)}), encoding="utf-8")
    return count


def build_manuscript_vars(
    catalogue: FEPTopicCatalogue,
    project_root: Path,
    *,
    output_root: Path | None = None,
) -> dict[str, Any]:
    summary = catalogue.summary()
    topics = {}
    icons = {"real": "✅", "partial": "◐", "aspirational": "○"}
    for topic in catalogue.topics:
        topics[topic.id] = {"title": topic.title, "area": topic.area, "maturity": topic.mathlib_status, "maturity_icon": icons.get(topic.mathlib_status, "?"), "mathlib_status": topic.mathlib_status, "lean_chars": topic.lean_chars, "nl_statement": topic.nl, "lean_sketch": topic.lean_sketch, "latex_equations": list(topic.latex_equations)}
    manifest = _get_latest_verification_manifest(project_root, output_root)
    summary_path = manifest.parent / "summary.json" if manifest else None
    return {**summary, "total_areas": len(summary["areas"]), "topic_ids": [t.id for t in catalogue.topics], "topics": topics, **_read_toolchain_vars(project_root), "verify": _verify_block_from_manifest(manifest), "hermes": _hermes_block_from_summary(summary_path), "tests": {"collected": _count_test_cases(project_root)}}


def build_lean_catalogue_markdown(catalogue: FEPTopicCatalogue) -> str:
    lines = ["# Appendix B: Full Lean Catalogue", "", "{#sec:appendix_b_full_topic_lean_catalogue}", ""]
    for topic in catalogue.topics:
        lines.extend([f"## {topic.id} — {topic.title}", "", f"{{#sec:catalogue-{topic.id}}}", "", topic.nl.strip(), "", "### Lean sketch", "", "```lean", topic.lean_sketch.rstrip(), "```", "", "### Typeset statement signatures", ""])
        for index, equation in enumerate(topic.latex_equations, 1):
            lines.extend([f"\\[\\label{{eq:{topic.id}-{index}}}", equation, "\\]", ""])
    return "\n".join(lines).rstrip() + "\n"


def build_typeset_equations_markdown(catalogue: FEPTopicCatalogue, project_root: Path | None = None) -> str:
    lines = ["# Appendix C: Typeset Equations", "", r"\label{sec:appendix_c_latex_equations}", "{#sec:appendix_c_latex_equations}", ""]
    for topic in catalogue.topics:
        lines.extend([f"## {topic.id} — {topic.title}", "", f"{{#sec:eqs-{topic.id}}}", ""])
        for index, equation in enumerate(topic.latex_equations, 1):
            lines.extend([f"\\[\\label{{eq:{topic.id}-{index}}}", equation, "\\]", ""])
    return "\n".join(lines).rstrip() + "\n"


def build_unified_formalism_appendix_markdown(catalogue: FEPTopicCatalogue, project_root: Path | None = None) -> str:
    return "<!-- AUTO-GENERATED by src/output/manuscript.py -->\n\n" + build_lean_catalogue_markdown(catalogue) + "\n" + build_typeset_equations_markdown(catalogue, project_root)


def write_manuscript_vars(
    project_root: Path,
    catalogue: FEPTopicCatalogue | None = None,
    *,
    output_root: Path | None = None,
) -> Path:
    root = Path(project_root)
    cat = catalogue or FEPTopicCatalogue.from_yaml(root / "config" / "topics.yaml")
    out = root / "manuscript" / "manuscript_vars.yaml"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        yaml.safe_dump(
            build_manuscript_vars(cat, root, output_root=output_root),
            sort_keys=False,
            allow_unicode=True,
        ),
        encoding="utf-8",
    )
    return out


def write_unified_formalism_appendix_markdown(project_root: Path, catalogue: FEPTopicCatalogue | None = None) -> Path:
    root = Path(project_root)
    cat = catalogue or FEPTopicCatalogue.from_yaml(root / "config" / "topics.yaml")
    out = root / "manuscript" / UNIFIED_FORMALISM_CATALOGUE_FILENAME
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build_unified_formalism_appendix_markdown(cat, root), encoding="utf-8")
    return out


def write_typeset_equations_markdown(project_root: Path, catalogue: FEPTopicCatalogue | None = None) -> Path:
    root = Path(project_root)
    cat = catalogue or FEPTopicCatalogue.from_yaml(root / "config" / "topics.yaml")
    out = root / "manuscript" / "09zc_appendix_c_lean_equations.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build_typeset_equations_markdown(cat, root), encoding="utf-8")
    return out
