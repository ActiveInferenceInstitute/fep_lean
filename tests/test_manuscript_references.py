"""Manuscript theorem identifiers resolve to canonical Lean declarations."""

from __future__ import annotations

from pathlib import Path

from fep_lean.catalogue.references import unresolved_manuscript_references
from fep_lean.formal.declarations import composed_theorem_declarations

PROJ = Path(__file__).resolve().parent.parent


def test_all_fep_declaration_references_resolve() -> None:
    composed = {
        declaration.rsplit(".", 1)[-1]
        for declaration in composed_theorem_declarations()
    }
    assert (
        unresolved_manuscript_references(
            PROJ / "manuscript", additional_declarations=composed
        )
        == ()
    )
