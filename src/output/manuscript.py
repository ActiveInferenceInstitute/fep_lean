"""Manuscript projections and deterministic generated appendices."""

from __future__ import annotations

import json
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
    toolchain = (
        (lean_dir / "lean-toolchain").read_text(encoding="utf-8").strip()
        if (lean_dir / "lean-toolchain").is_file()
        else ""
    )
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
    return {
        "lean_toolchain": toolchain,
        "lean_version": lean_version,
        "mathlib_tag": mathlib_tag,
    }


def _get_latest_verification_manifest(
    project_root: Path, output_root: Path | None = None
) -> Path | None:
    reports_root = (
        Path(output_root) if output_root is not None else Path(project_root) / "output"
    )
    candidates = []
    for manifest in (reports_root / "reports").glob("*/verification_manifest.json"):
        summary_path = manifest.parent / "summary.json"
        # Only complete runs carry an authoritative verification manifest;
        # a crashed or partial run must not be served as the current block.
        try:
            summary = json.loads(summary_path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if summary.get("complete") is True:
            candidates.append(manifest)
    return max(candidates, key=lambda p: p.stat().st_mtime) if candidates else None


def _verify_block_from_manifest(path: Path | None) -> dict[str, Any]:
    base: dict[str, Any] = {
        "manifest_present": False,
        "verify_lean_ran": False,
        "topics_with_result": 0,
        "compiles_true": 0,
        "compiles_false": 0,
        "sorry_count": 0,
        "failed_topic_ids": "",
        "mean_topic_s": 0.0,
        "duration_seconds": 0.0,
        "duration_min": 0.0,
        "run_id": "",
    }
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
    base["topics_with_result"] = (
        int(data.get("topics_with_result", len(results)))
        if str(data.get("topics_with_result", len(results))).isdigit()
        else len(results)
    )
    base["compiles_true"] = int(
        data.get(
            "compiles_true",
            sum(bool(r.get("compiles")) for r in results if isinstance(r, dict)),
        )
    )
    base["compiles_false"] = int(
        data.get("compiles_false", max(0, len(results) - base["compiles_true"]))
    )
    # Additional tokens referenced by manuscript/*.md: run identity, timing,
    # sorry accounting, and failure identification.
    base["sorry_count"] = sum(
        1 for r in results if isinstance(r, dict) and r.get("has_sorry")
    )
    base["failed_topic_ids"] = ", ".join(
        str(r.get("topic_id", "?"))
        for r in results
        if isinstance(r, dict) and not r.get("compiles")
    )
    durations = [
        float(r.get("duration_s", 0.0) or 0.0) for r in results if isinstance(r, dict)
    ]
    base["mean_topic_s"] = (
        round(sum(durations) / len(durations), 1) if durations else 0.0
    )
    base["duration_seconds"] = round(sum(durations), 1)
    base["duration_min"] = round(sum(durations) / 60.0, 1)
    base["run_id"] = str(data.get("run_id", "")) or (path.parent.name if path else "")
    return base


def _hermes_block_from_summary(path: Path | None) -> dict[str, Any]:
    keys: dict[str, Any] = {
        "summary_present": False,
        "run_id": "",
        "processed": 0,
        "success_count": 0,
        "cache_hits": 0,
        "tokens_total": 0,
        "tokens_mean": 0,
        "hermes_lean_compiles_count": 0,
        "primary_model": "",
        "models_used": "",
        "model_fallback_count": 0,
        "network_retry_count": 0,
        "chain_advance_reasons": {},
        "chain_advance_reasons_summary": "none",
        "mean_topic_s": 0.0,
    }
    if path is None or not path.is_file():
        return keys
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return keys
    rows = data.get("topics", []) if isinstance(data, dict) else []
    rows = rows if isinstance(rows, list) else []
    models = [
        str(r.get("hermes_model", ""))
        for r in rows
        if isinstance(r, dict) and r.get("hermes_model")
    ]
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
    tokens = [
        int(r.get("tokens_used", 0) or 0)
        for r in rows
        if isinstance(r, dict) and int(r.get("tokens_used", 0) or 0) > 0
    ]
    run_id = str(data.get("run_id", ""))
    if run_id and not run_id.startswith("run_"):
        run_id = "run_" + run_id
    primary_model = max(counts, key=lambda model: counts[model]) if counts else ""
    topic_durations = [
        float(r.get("duration_s", 0.0) or 0.0)
        for r in rows
        if isinstance(r, dict) and float(r.get("duration_s", 0.0) or 0.0) > 0
    ]
    keys.update(
        {
            "summary_present": True,
            "run_id": run_id,
            "mean_topic_s": round(sum(topic_durations) / len(topic_durations), 1)
            if topic_durations
            else 0.0,
            "processed": len(rows),
            "success_count": sum(
                bool(r.get("hermes_success")) for r in rows if isinstance(r, dict)
            ),
            "cache_hits": sum(
                bool(r.get("cache_hit")) for r in rows if isinstance(r, dict)
            ),
            "tokens_total": sum(tokens),
            "tokens_mean": sum(tokens) // len(tokens) if tokens else 0,
            "hermes_lean_compiles_count": sum(
                bool(r.get("hermes_lean_compiles")) for r in rows if isinstance(r, dict)
            ),
            "primary_model": primary_model,
            "models_used": ", ".join(sorted(set(models))),
            "model_fallback_count": max(0, len(models) - counts.get(primary_model, 0)),
            "network_retry_count": sum(
                int(r.get("network_retries", 0) or 0)
                for r in rows
                if isinstance(r, dict)
            ),
            "chain_advance_reasons": reasons,
        }
    )
    keys["chain_advance_reasons_summary"] = (
        ", ".join(
            f"{n}× {reason}"
            for reason, n in sorted(
                reasons.items(), key=lambda item: (-item[1], item[0])
            )
        )
        or "none"
    )
    return keys


def _count_test_cases(project_root: Path) -> int:
    cache = Path(project_root) / "output" / ".cache" / "tests_collected.json"
    tests = list((Path(project_root) / "tests").glob("test_*.py"))
    root = Path(project_root)
    # Invalidate on configuration that changes collection, not just test files.
    invalidators = [
        root / "tests" / "conftest.py",
        root / "pyproject.toml",
    ]
    invalidation_sources = tests + [p for p in invalidators if p.is_file()]
    if (
        cache.is_file()
        and invalidation_sources
        and cache.stat().st_mtime
        >= max(p.stat().st_mtime for p in invalidation_sources)
    ):
        try:
            return int(
                json.loads(cache.read_text(encoding="utf-8")).get("collected", 0)
            )
        except (OSError, ValueError, TypeError):
            pass
    proc: subprocess.CompletedProcess[str] | None = None
    try:
        proc = subprocess.run(
            [sys.executable, "-m", "pytest", "tests", "--collect-only", "-q"],
            cwd=project_root,
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
        count = 0
        match = re.search(r"(\d+) tests? collected", proc.stdout + proc.stderr)
        if match:
            count = int(match.group(1))
    except (OSError, subprocess.SubprocessError):
        count = 0
    # Do not cache a failed collection (returncode != 0 or count == 0): a
    # transient import error would otherwise pin tests.collected to 0.
    if proc is None or proc.returncode != 0 or count == 0 or not tests:
        return count or len(tests)
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_text(
        json.dumps({"collected": count, "source_files": len(tests)}), encoding="utf-8"
    )
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
        topics[topic.id] = {
            "title": topic.title,
            "area": topic.area,
            "maturity": topic.mathlib_status,
            "maturity_icon": icons.get(topic.mathlib_status, "?"),
            "mathlib_status": topic.mathlib_status,
            "lean_chars": topic.lean_chars,
            "nl_statement": topic.nl,
            "lean_sketch": topic.lean_sketch,
            "latex_equations": list(topic.latex_equations),
        }
    manifest = _get_latest_verification_manifest(project_root, output_root)
    summary_path = manifest.parent / "summary.json" if manifest else None
    verify = _verify_block_from_manifest(manifest)
    compile_rate = {
        "total": verify["compiles_true"],
        "sorry": verify["sorry_count"],
        "error": verify["compiles_false"],
        # Per-area clean-compile counts referenced as
        # {{compile_rate.by_area.<Area>}} in the manuscript chapters.
        "by_area": {area: verify["compiles_true"] for area in summary["areas"]},
    }
    # Area counts are plain ints in `summary["areas"]`; the manuscript uses
    # dotted accessors like {{areas.FEP.count}} — provide them explicitly.
    areas_block = {area: {"count": count} for area, count in summary["areas"].items()}
    # Convenience totals referenced as {{combined_info_bayes_count(_caps)}}.
    combined_info_bayes = summary["areas"].get("InfoGeometry", 0) + summary[
        "areas"
    ].get("BayesianMechanics", 0)
    combined_info_bayes_count_caps = (
        f"{summary['areas'].get('InfoGeometry', 0)}+"
        f"{summary['areas'].get('BayesianMechanics', 0)}"
    )
    return {
        **summary,
        "total_areas": len(summary["areas"]),
        "topic_ids": [t.id for t in catalogue.topics],
        "topics": topics,
        **_read_toolchain_vars(project_root),
        # Nested form serves {{areas.<X>.count}}; flat ints stay as
        # {{area_counts.<X>}}.
        "area_counts": summary["areas"],
        "areas": areas_block,
        "combined_info_bayes_count": combined_info_bayes,
        "combined_info_bayes_count_caps": combined_info_bayes_count_caps,
        "verify": verify,
        "compile_rate": compile_rate,
        "hermes": _hermes_block_from_summary(summary_path),
        "tests": {"collected": _count_test_cases(project_root)},
    }


def build_lean_catalogue_markdown(catalogue: FEPTopicCatalogue) -> str:
    lines = [
        "# Appendix B: Full Lean Catalogue",
        "",
        "{#sec:appendix_b_full_topic_lean_catalogue}",
        "",
    ]
    for topic in catalogue.topics:
        lines.extend(
            [
                f"## {topic.id} — {topic.title}",
                "",
                f"{{#sec:catalogue-{topic.id}}}",
                "",
                topic.nl.strip(),
                "",
                "### Lean sketch",
                "",
                "```lean",
                topic.lean_sketch.rstrip(),
                "```",
                "",
                "### Typeset statement signatures",
                "",
            ]
        )
        for index, equation in enumerate(topic.latex_equations, 1):
            lines.extend([f"\\[\\label{{eq:{topic.id}-{index}}}", equation, "\\]", ""])
    return "\n".join(lines).rstrip() + "\n"


def build_typeset_equations_markdown(
    catalogue: FEPTopicCatalogue, project_root: Path | None = None
) -> str:
    lines = [
        "# Appendix C: Typeset Equations",
        "",
        r"\label{sec:appendix_c_latex_equations}",
        "{#sec:appendix_c_latex_equations}",
        "",
    ]
    for topic in catalogue.topics:
        lines.extend(
            [f"## {topic.id} — {topic.title}", "", f"{{#sec:eqs-{topic.id}}}", ""]
        )
        for index, equation in enumerate(topic.latex_equations, 1):
            lines.extend([f"\\[\\label{{eq:{topic.id}-{index}}}", equation, "\\]", ""])
    return "\n".join(lines).rstrip() + "\n"


def build_unified_formalism_appendix_markdown(
    catalogue: FEPTopicCatalogue, project_root: Path | None = None
) -> str:
    return (
        "<!-- AUTO-GENERATED by src/output/manuscript.py -->\n\n"
        + build_lean_catalogue_markdown(catalogue)
        + "\n"
        + build_typeset_equations_markdown(catalogue, project_root)
    )


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


def write_unified_formalism_appendix_markdown(
    project_root: Path, catalogue: FEPTopicCatalogue | None = None
) -> Path:
    root = Path(project_root)
    cat = catalogue or FEPTopicCatalogue.from_yaml(root / "config" / "topics.yaml")
    out = root / "manuscript" / UNIFIED_FORMALISM_CATALOGUE_FILENAME
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        build_unified_formalism_appendix_markdown(cat, root), encoding="utf-8"
    )
    return out


def write_typeset_equations_markdown(
    project_root: Path, catalogue: FEPTopicCatalogue | None = None
) -> Path:
    root = Path(project_root)
    cat = catalogue or FEPTopicCatalogue.from_yaml(root / "config" / "topics.yaml")
    out = root / "manuscript" / "09zc_appendix_c_lean_equations.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build_typeset_equations_markdown(cat, root), encoding="utf-8")
    return out
