#!/usr/bin/env python3
"""Audit cross-reference integrity in the manuscript.

For every ``*.md`` under ``projects/fep_lean/manuscript/`` the script:

1. Collects pandoc anchor definitions (``{#id}``).
2. Collects LaTeX label definitions (``\\label{id}``) inside displayed-equation
   environments (``\\begin{equation}...\\label{eq:foo}``) and elsewhere.
3. Collects every reference (``\\ref{id}``, ``\\eqref{id}``, ``\\Cref{id}``).
4. Reports references that resolve to neither a pandoc anchor nor a LaTeX label.

This freezes the audit shape used in the Tier 8 hygiene closeout so a future
``\\ref{eq:foo}`` lacking either a ``{#eq:foo}`` anchor or an inline
``\\label{eq:foo}`` fails CI loudly. Both definition styles are accepted because
pandoc-citeproc + ``pandoc-crossref`` resolve both at PDF render time.

Exit codes
----------

- ``0`` -- every reference resolves.
- ``1`` -- at least one unresolved reference (CI-friendly).

Usage
-----

.. code-block:: bash

    uv run python xref_audit.py            # default
    uv run python xref_audit.py --verbose  # list every defined anchor/label
    uv run python xref_audit.py --root path/to/manuscript
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

DOCS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = DOCS_DIR.parent
DEFAULT_ROOT = PROJECT_ROOT / "manuscript"

_RE_PANDOC_ANCHOR = re.compile(r"\{#([\w:_-]+)\}")
_RE_LATEX_LABEL = re.compile(r"\\label\{([\w:_-]+)\}")
_RE_REF = re.compile(r"\\(?:ref|eqref|Cref|cref)\{([\w:_-]+)\}")


def _scan(text: str) -> tuple[set[str], set[str], set[str]]:
    pandoc = set(_RE_PANDOC_ANCHOR.findall(text))
    labels = set(_RE_LATEX_LABEL.findall(text))
    refs = set(_RE_REF.findall(text))
    return pandoc, labels, refs


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    parser.add_argument(
        "--root",
        type=Path,
        default=DEFAULT_ROOT,
        help="Manuscript directory to scan (default: projects/fep_lean/manuscript).",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Also list every anchor/label definition found.",
    )
    args = parser.parse_args(argv)

    root: Path = args.root.resolve()
    if not root.exists():
        print(f"FAIL: manuscript root does not exist: {root}")
        return 1

    files = sorted(root.glob("*.md"))
    if not files:
        print(f"FAIL: no *.md files under {root}")
        return 1

    pandoc_anchors: set[str] = set()
    latex_labels: set[str] = set()
    referenced: set[str] = set()
    ref_origin: dict[str, list[tuple[Path, int]]] = defaultdict(list)
    for path in files:
        text = path.read_text(encoding="utf-8")
        p, line, r = _scan(text)
        pandoc_anchors |= p
        latex_labels |= line
        referenced |= r
        for i, line in enumerate(text.splitlines(), start=1):
            for m in _RE_REF.finditer(line):
                ref_origin[m.group(1)].append((path, i))

    defined = pandoc_anchors | latex_labels
    unresolved = sorted(referenced - defined)

    if unresolved:
        for ref_id in unresolved:
            origins = ref_origin.get(ref_id, [])
            for path, line in origins:
                rel = path.relative_to(PROJECT_ROOT)
                print(f"{rel}:{line}: unresolved \\ref{{{ref_id}}}")
        print()
        print(
            f"FAIL: {len(unresolved)} unresolved reference(s); "
            f"{len(referenced)} referenced, {len(defined)} defined "
            f"({len(pandoc_anchors)} pandoc + {len(latex_labels)} \\label)"
        )
        return 1

    if args.verbose:
        print(f"Pandoc anchors ({len(pandoc_anchors)}):")
        for a in sorted(pandoc_anchors):
            print(f"  {a}")
        print(f"\\label definitions ({len(latex_labels)}):")
        for a in sorted(latex_labels):
            print(f"  {a}")

    print(
        f"OK: {len(defined)} defined "
        f"({len(pandoc_anchors)} pandoc + {len(latex_labels)} \\label), "
        f"{len(referenced)} referenced — all resolve."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
