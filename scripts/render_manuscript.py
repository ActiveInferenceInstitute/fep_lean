#!/usr/bin/env python3
"""Validate or render manuscript variables without mutating authored sources.

Usage:
    uv run python scripts/render_manuscript.py --check
    uv run python scripts/render_manuscript.py
    uv run python scripts/render_manuscript.py --output-dir output/manuscript
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# A direct check/render invocation must not update checkout-local bytecode.
if __name__ == "__main__":
    sys.dont_write_bytecode = True

from fep_lean.catalogue import FEPTopicCatalogue
from fep_lean.output.manuscript import (
    build_manuscript_vars,
    manuscript_projection_drift,
)
from fep_lean.output.rendering import (
    ManuscriptRenderError,
    render_manuscript,
    unresolved_placeholders,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="fail-closed source-to-build manuscript rendering"
    )
    parser.add_argument(
        "--check",
        "--dry-run",
        dest="check",
        action="store_true",
        help="validate that every placeholder resolves without writing output",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="render destination (default: output/manuscript)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    project_root = Path(__file__).resolve().parents[1]
    source_dir = project_root / "manuscript"
    try:
        catalogue = FEPTopicCatalogue.from_yaml(project_root / "config" / "topics.yaml")
        variables = build_manuscript_vars(
            catalogue,
            project_root,
            cache_test_count=not args.check,
        )
        drift = manuscript_projection_drift(
            project_root,
            catalogue,
            expected_variables=variables,
        )
    except (OSError, ValueError) as exc:
        print(f"ERROR: cannot validate manuscript projections: {exc}")
        return 1
    if drift:
        print("ERROR: stale manuscript projections")
        for path in drift:
            try:
                display_path = path.relative_to(project_root)
            except ValueError:
                display_path = path
            print(f"  {display_path}")
        return 1
    unresolved = unresolved_placeholders(source_dir, variables)
    if unresolved:
        print("ERROR: unresolved manuscript placeholders")
        for item in unresolved:
            print(f"  {item}")
        return 1
    if args.check:
        print(
            "OK: manuscript projections are current and every authored "
            "placeholder resolves"
        )
        return 0
    destination = (
        args.output_dir
        if args.output_dir is not None
        else project_root / "output" / "manuscript"
    )
    try:
        rendered = render_manuscript(source_dir, destination, variables)
    except ManuscriptRenderError as exc:
        print(f"ERROR: {exc}")
        return 1
    print(f"Rendered {len(rendered)} manuscript files to {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
