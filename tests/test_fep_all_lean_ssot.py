"""Verify ``lean/FepSketches/fep_all.lean`` covers all topics in ``config/topics.yaml``.

The persistent Lean workspace file should contain a ``namespace fep_fepNNN`` block
for every topic ID in the YAML catalogue.  This test catches gaps where new topics
are added to the catalogue but not to the persistent Lean file.
"""

from __future__ import annotations

import re
from pathlib import Path

import yaml

PROJ = Path(__file__).resolve().parent.parent
FEP_ALL = PROJ / "lean" / "FepSketches" / "fep_all.lean"
TOPICS_YAML = PROJ / "config" / "topics.yaml"

_NS_RE = re.compile(r"^namespace fep_fep(\d+)", re.MULTILINE)


def _extract_lean_topic_ids(text: str) -> set[str]:
    """Extract topic IDs from namespace declarations in fep_all.lean."""
    return {f"fep-{m.group(1)}" for m in _NS_RE.finditer(text)}


def _load_yaml_topic_ids() -> set[str]:
    """Load topic IDs from topics.yaml."""
    with open(TOPICS_YAML, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return {t["id"] for t in data["topics"]}


def test_fep_all_lean_covers_all_yaml_topics() -> None:
    """Every topic in topics.yaml has a corresponding namespace in fep_all.lean."""
    lean_ids = _extract_lean_topic_ids(FEP_ALL.read_text(encoding="utf-8"))
    yaml_ids = _load_yaml_topic_ids()

    missing_from_lean = yaml_ids - lean_ids
    extra_in_lean = lean_ids - yaml_ids

    errors: list[str] = []
    if missing_from_lean:
        errors.append(
            f"In topics.yaml but not in fep_all.lean: {sorted(missing_from_lean)}"
        )
    if extra_in_lean:
        errors.append(
            f"In fep_all.lean but not in topics.yaml: {sorted(extra_in_lean)}"
        )

    assert not errors, "\n".join(errors)


def test_fep_all_lean_has_the_sealed_topic_count() -> None:
    """The aggregate must contain exactly the generated catalogue namespaces."""
    lean_ids = _extract_lean_topic_ids(FEP_ALL.read_text(encoding="utf-8"))
    expected_ids = _load_yaml_topic_ids()
    assert len(lean_ids) == len(expected_ids), (
        f"Expected {len(expected_ids)} topics, found {len(lean_ids)}: {sorted(lean_ids)}"
    )


def test_fep_all_lean_has_no_sorry() -> None:
    """fep_all.lean must not contain any non-comment sorry."""
    text = FEP_ALL.read_text(encoding="utf-8")
    sorry_lines = []
    for i, line in enumerate(text.splitlines(), 1):
        stripped = line.lstrip()
        if stripped.startswith("--"):
            continue
        if re.search(r"\bsorry\b", line):
            sorry_lines.append(f"  line {i}: {line.rstrip()}")

    assert not sorry_lines, "sorry found in fep_all.lean:\n" + "\n".join(sorry_lines)
