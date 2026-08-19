#!/usr/bin/env python3
"""Maintenance: rewrite hard-coded topic counts in markdown under this project.

Previously used to change '50' -> '8'. With the canonical 50-topic catalogue,
this script can align text to a target total (default 50).

Usage:
  uv run python scripts/_maint_fix_manuscript_counts.py --total 50 --dry-run
  uv run python scripts/_maint_fix_manuscript_counts.py --total 50 --apply
"""

from __future__ import annotations

import argparse
import os
import re
from pathlib import Path


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _fix_table(content: str, total: int) -> str:
    """Drop markdown table rows for FEP-xxx not in 1..total (rough heuristic)."""
    lines = content.split("\n")
    new_lines: list[str] = []
    pat = re.compile(r"fep-(\d+)", re.IGNORECASE)
    for line in lines:
        stripped = line.strip()
        if stripped.startswith(("| FEP-", "| fep-")):
            m = pat.search(line)
            if m and int(m.group(1)) > total:
                continue
        new_lines.append(line)
    return "\n".join(new_lines)


def process_file(path: Path, total: int, *, old_totals: tuple[int, ...]) -> str | None:
    text = path.read_text(encoding="utf-8")
    orig = text
    for old in old_totals:
        if old != total:
            text = text.replace(f"of {old} topics", f"of {total} topics")
            text = text.replace(f" {old} topics", f" {total} topics")
            text = text.replace(f" {old}-topic", f" {total}-topic")
            text = text.replace(f"{old}-topic", f"{total}-topic")
            text = text.replace("{{total_topics}}", str(total))
    text = re.sub(r"\(.*partial.*?topics\)", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\(.*aspirational.*?topics\)", "", text, flags=re.IGNORECASE)
    text = _fix_table(text, total)
    if text != orig:
        return text
    return None


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--total", type=int, default=50)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    root = project_root()
    old_totals = (8, 50) if args.total == 50 else (50, 8)

    targets: list[Path] = []
    for sub in ("manuscript", "docs"):
        d = root / sub
        if d.is_dir():
            for fn in os.listdir(d):
                if fn.endswith(".md"):
                    targets.append(d / fn)
    for name in ("README.md", "AGENTS.md", "SPEC.md", "PAI.md", "index.md"):
        p = root / name
        if p.is_file():
            targets.append(p)

    changed = 0
    for path in targets:
        new = process_file(path, args.total, old_totals=old_totals)
        if new is None:
            continue
        changed += 1
        if args.apply:
            path.write_text(new, encoding="utf-8")
            print(f"updated {path.relative_to(root)}")
        else:
            print(f"would update {path.relative_to(root)}")
    print(f"done: {changed} files" + ("" if args.apply else " (dry-run)"))


if __name__ == "__main__":
    main()
