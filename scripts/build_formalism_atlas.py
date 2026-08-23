#!/usr/bin/env python3
"""Generate or drift-check the deterministic formalism atlas."""

from __future__ import annotations

import argparse
from pathlib import Path

from fep_lean.output.formalism_atlas import (
    atlas_projection_drift,
    write_formalism_atlas,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    if args.check:
        drift = atlas_projection_drift(root)
        if drift:
            for path in drift:
                print(f"STALE: {path.relative_to(root)}")
            return 1
        print("OK: formalism atlas projections are current")
        return 0
    paths = write_formalism_atlas(root)
    for path in paths:
        print(f"Wrote {path.relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
