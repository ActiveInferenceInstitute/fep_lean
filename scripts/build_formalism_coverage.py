#!/usr/bin/env python3
"""Generate or drift-check formalism breadth/depth projections."""

from __future__ import annotations

import argparse
from pathlib import Path

from fep_lean.catalogue.coverage import (
    formalism_coverage_drift,
    write_formalism_coverage,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    if args.check:
        drift = formalism_coverage_drift(root)
        if drift:
            for path in drift:
                print(f"STALE: {path.relative_to(root)}")
            return 1
        print("OK: formalism coverage projections are current")
        return 0
    paths = write_formalism_coverage(root)
    for path in paths:
        print(f"Wrote {path.relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
