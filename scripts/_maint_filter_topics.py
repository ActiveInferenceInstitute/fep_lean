#!/usr/bin/env python3
"""Destructive: rewrite config/topics.yaml to a subset of topic ids.

Prefer the full 50-topic catalogue from _maint_build_topics_catalogue.py.
This tool exists only for local experiments.

Usage:
  uv run python scripts/_maint_filter_topics.py --ids fep-008,fep-014
  uv run python scripts/_maint_filter_topics.py --apply --ids fep-008,fep-014
"""

from __future__ import annotations

import argparse
from pathlib import Path

import yaml


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--apply", action="store_true", help="Write topics.yaml (default is dry-run)"
    )
    p.add_argument(
        "--ids",
        required=True,
        help="Comma-separated topic ids to keep (e.g. fep-008,fep-014)",
    )
    args = p.parse_args()
    keep_ids = {x.strip() for x in args.ids.split(",") if x.strip()}
    cfg = project_root() / "config" / "topics.yaml"
    data = yaml.safe_load(cfg.read_text(encoding="utf-8"))
    topics = data.get("topics") or []
    new_topics = [t for t in topics if t.get("id") in keep_ids]
    if len(new_topics) != len(keep_ids):
        found = {t.get("id") for t in new_topics}
        missing = keep_ids - found
        raise SystemExit(f"Some ids not in catalogue: {sorted(missing)}")
    data["topics"] = new_topics
    out = yaml.dump(data, sort_keys=False, allow_unicode=True, width=120)
    if not args.apply:
        print(f"dry-run: would keep {len(new_topics)} topics -> {cfg}")
        print(out[:2000])
        return
    hdr = (
        f"# Subset catalogue ({len(new_topics)} topics) — DO NOT COMMIT as canonical 50\n"
        "# Restore: uv run python scripts/_maint_build_topics_catalogue.py\n\n"
    )
    cfg.write_text(hdr + out, encoding="utf-8")
    print(f"Wrote {len(new_topics)} topics to {cfg}")


if __name__ == "__main__":
    main()
