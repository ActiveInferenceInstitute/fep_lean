#!/usr/bin/env python3
"""Fail when manuscript ``fepNNN_*`` names are not canonical declarations."""

from __future__ import annotations

from pathlib import Path

from fep_lean.catalogue.references import unresolved_manuscript_references
from fep_lean.formal.declarations import composed_theorem_declarations


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    composed = {
        declaration.rsplit(".", 1)[-1]
        for declaration in composed_theorem_declarations()
    }
    failures = unresolved_manuscript_references(
        root / "manuscript", additional_declarations=composed
    )
    if failures:
        for failure in failures:
            print(f"manuscript/{failure}")
        print(f"FAIL: {len(failures)} unresolved canonical declaration reference(s)")
        return 1
    print("OK: all manuscript topic and composed declaration references resolve")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
