#!/usr/bin/env python3
"""Project packaged cross-topic Lean modules into the Lake workspace."""

from __future__ import annotations

import argparse
from pathlib import Path

from fep_lean.formal import (
    formal_aggregate_drift,
    formal_projection_drift,
    write_formal_aggregate,
    write_formal_projections,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    if args.check:
        drift = (*formal_aggregate_drift(root), *formal_projection_drift(root))
        if drift:
            for path in drift:
                print(f"STALE: {path.relative_to(root)}")
            return 1
        print("OK: formal Lean workspace projections are current")
        return 0
    aggregate = write_formal_aggregate(root)
    print(f"Wrote {aggregate.relative_to(root)}")
    for path in write_formal_projections(root):
        print(f"Wrote {path.relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
