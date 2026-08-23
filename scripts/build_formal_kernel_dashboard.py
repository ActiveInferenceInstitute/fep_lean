#!/usr/bin/env python3
"""Generate or drift-check the deterministic formal-kernel dashboard."""

from __future__ import annotations

import argparse
from pathlib import Path

from fep_lean.output.formal_kernel_dashboard import (
    formal_kernel_dashboard_drift,
    write_formal_kernel_dashboard,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    if args.check:
        drift = formal_kernel_dashboard_drift(root)
        if drift:
            for path in drift:
                print(f"STALE: {path.relative_to(root)}")
            return 1
        print("OK: formal-kernel dashboard projections are current")
        return 0
    paths = write_formal_kernel_dashboard(root)
    for path in paths:
        print(f"Wrote {path.relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
