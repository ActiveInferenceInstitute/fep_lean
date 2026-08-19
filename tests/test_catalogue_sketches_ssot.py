"""Enforce ``config/topics.yaml`` ``lean_sketch`` matches ``scripts/catalogue_sketches.SKETCHES``.

The catalogue bodies are authored in ``catalogue_sketches.py``; ``topics.yaml`` is
regenerated via ``scripts/_maint_build_topics_catalogue.py``. This test catches
accidental YAML-only edits that drift from ``SKETCHES`` without a full Lean run.
"""

from __future__ import annotations

import sys
from pathlib import Path

from catalogue.topics import FEPTopicCatalogue

PROJ = Path(__file__).resolve().parent.parent
SCRIPTS = PROJ / "scripts"
TOPICS = PROJ / "config" / "topics.yaml"


def _load_sketches() -> dict[str, str]:
    if str(SCRIPTS) not in sys.path:
        sys.path.insert(0, str(SCRIPTS))
    from catalogue_sketches import SKETCHES

    return SKETCHES


def _load_latex_equations() -> dict[str, list[str]]:
    if str(SCRIPTS) not in sys.path:
        sys.path.insert(0, str(SCRIPTS))
    from catalogue_sketches import LATEX_EQUATIONS

    return LATEX_EQUATIONS


def test_yaml_lean_sketch_matches_sketches_module() -> None:
    sketches = _load_sketches()
    cat = FEPTopicCatalogue.from_yaml(TOPICS)
    assert len(cat.topics) == 50

    mismatches: list[str] = []
    for t in cat.topics:
        expected = sketches.get(t.id)
        if expected is None:
            mismatches.append(f"{t.id}: missing key in SKETCHES")
            continue
        yaml_body = t.lean_sketch.rstrip("\n")
        sk_body = expected.rstrip("\n")
        if yaml_body != sk_body:
            mismatches.append(f"{t.id}: topics.yaml lean_sketch != SKETCHES[{t.id!r}]")

    assert not mismatches, "SKETCHES vs topics.yaml drift:\n" + "\n".join(mismatches)


def test_yaml_latex_equations_matches_sketches_module() -> None:
    expected = _load_latex_equations()
    cat = FEPTopicCatalogue.from_yaml(TOPICS)
    for t in cat.topics:
        want = expected.get(t.id)
        assert want is not None, f"{t.id}: missing in LATEX_EQUATIONS"
        assert list(t.latex_equations) == want, (
            f"{t.id}: topics.yaml latex_equations != LATEX_EQUATIONS"
        )
