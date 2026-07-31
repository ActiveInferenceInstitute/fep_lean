#!/usr/bin/env python3
"""Inject manuscript_vars.yaml values directly into manuscript/*.md files in-place.

Reads manuscript/manuscript_vars.yaml, flattens all keys to dotted notation,
then replaces every {{variable}} placeholder in manuscript/*.md files.

Skipped files (contain literal {{}} syntax as documentation or are auto-generated):
  09z_unified_formalism_catalogue.md, manuscript_vars.yaml,
  AGENTS.md, README.md, preamble.md

Usage:
    uv run python scripts/_inject_manuscript_vars.py [--dry-run]
"""
import re
import sys
from pathlib import Path
from typing import Any

import yaml

project_root = Path(__file__).resolve().parents[1]
vars_path = project_root / "manuscript" / "manuscript_vars.yaml"
manuscript_dir = project_root / "manuscript"

SKIP = {
    "09z_unified_formalism_catalogue.md",
    "manuscript_vars.yaml",
    "AGENTS.md",
    "README.md",
    "preamble.md",
    # Stale from older runs
    "09z_appendix_b_lean_catalogue.md",
    "09zc_appendix_c_lean_equations.md",
}

DRY_RUN = "--dry-run" in sys.argv
PLACEHOLDER_RE = re.compile(r"\{\{([^}]+)\}\}")


def flatten(data: Any, prefix: str = "") -> dict[str, str]:
    flat: dict[str, str] = {}
    if isinstance(data, dict):
        for k, v in data.items():
            key = f"{prefix}.{k}" if prefix else str(k)
            if isinstance(v, dict):
                flat.update(flatten(v, key))
            elif isinstance(v, list):
                flat[key] = ", ".join(str(x) for x in v)
            elif isinstance(v, bool):
                flat[key] = str(v).lower()
            elif v is None:
                flat[key] = ""
            else:
                flat[key] = str(v)
    return flat


def main() -> None:
    raw = yaml.safe_load(vars_path.read_text(encoding="utf-8"))
    flat = flatten(raw)

    maturity_summary = (
        f"{flat.get('maturity.real', '?')} real, "
        f"{flat.get('maturity.partial', '?')} partial, "
        f"{flat.get('maturity.aspirational', '?')} aspirational"
    )
    verify_parts = [f"{k}={flat[k]}" for k in sorted(flat) if k.startswith("verify.")]
    verify_summary = "; ".join(verify_parts) if verify_parts else "(no verify metrics)"

    total_subs = 0
    files_changed = 0

    for md_file in sorted(manuscript_dir.glob("*.md")):
        if md_file.name in SKIP:
            continue
        content = md_file.read_text(encoding="utf-8")
        counter = [0]

        def repl(m: re.Match[str], counter=counter) -> str:
            key = m.group(1).strip()
            if key == "maturity.*":
                counter[0] += 1
                return maturity_summary
            if key == "verify.*":
                counter[0] += 1
                return verify_summary
            if key in flat:
                counter[0] += 1
                return flat[key]
            return m.group(0)

        new_content = PLACEHOLDER_RE.sub(repl, content)
        n_subs = counter[0]
        if n_subs > 0:
            files_changed += 1
            total_subs += n_subs
            if DRY_RUN:
                print(f"  [dry-run] {md_file.name}: {n_subs} substitutions")
            else:
                md_file.write_text(new_content, encoding="utf-8")
                print(f"  updated   {md_file.name}: {n_subs} substitutions")

    print(f"\nDone: {files_changed} files, {total_subs} total substitutions")
    if DRY_RUN:
        print("(dry-run — no files written)")


if __name__ == "__main__":
    main()
