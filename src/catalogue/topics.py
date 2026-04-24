"""Load and summarize the FEP topic catalogue (YAML source of truth).

This is the canonical module for the catalogue data model.
Importable as ``from catalogue.topics import FEPTopicCatalogue``.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

_MATURITY_ORDER = ("real", "partial", "aspirational")


@dataclass(frozen=True)
class TopicEntry:
    """One catalogue row."""

    id: str
    title: str
    area: str
    mathlib: str
    mathlib_status: str
    nl: str
    lean_sketch: str
    latex_equations: tuple[str, ...] = ()

    @property
    def lean_chars(self) -> int:
        """Character count of the Lean sketch (for catalogue metrics)."""
        return len(self.lean_sketch)


class FEPTopicCatalogue:
    """In-memory view of ``config/topics.yaml``."""

    def __init__(self, topics: list[TopicEntry], source_path: Path) -> None:
        """Initialize from parsed TopicEntry list (used by from_yaml classmethod)."""
        self._topics = topics
        self.source_path = source_path

    @classmethod
    def from_yaml(cls, path: Path | None = None) -> "FEPTopicCatalogue":
        """Load catalogue from YAML. Default: ``<project>/config/topics.yaml`` next to ``src/``."""
        resolved = path if path is not None else _default_topics_path()
        data = yaml.safe_load(resolved.read_text(encoding="utf-8"))
        raw: list[dict[str, Any]] = data.get("topics") or []
        topics: list[TopicEntry] = []
        for row in raw:
            raw_latex = row.get("latex_equations")
            if isinstance(raw_latex, list):
                latex_eqs = tuple(str(x) for x in raw_latex)
            else:
                latex_eqs = ()
            topics.append(
                TopicEntry(
                    id=str(row["id"]),
                    title=str(row.get("title", "")),
                    area=str(row.get("area", "")),
                    mathlib=str(row.get("mathlib", "")),
                    mathlib_status=str(row.get("mathlib_status", "partial")).strip().lower(),
                    nl=str(row.get("nl", "")),
                    lean_sketch=str(row.get("lean_sketch", "")),
                    latex_equations=latex_eqs,
                )
            )
        return cls(topics, resolved)

    @property
    def topics(self) -> list[TopicEntry]:
        return list(self._topics)

    def summary(self) -> dict[str, Any]:
        """Counts by area and global maturity tallies."""
        areas: dict[str, int] = {}
        maturity_totals = {k: 0 for k in _MATURITY_ORDER}
        area_maturity: dict[str, dict[str, int]] = {}

        for t in self._topics:
            areas[t.area] = areas.get(t.area, 0) + 1
            st = t.mathlib_status if t.mathlib_status in maturity_totals else "partial"
            maturity_totals[st] = maturity_totals.get(st, 0) + 1
            if t.area not in area_maturity:
                area_maturity[t.area] = {k: 0 for k in _MATURITY_ORDER}
            area_maturity[t.area][st] = area_maturity[t.area].get(st, 0) + 1

        return {
            "total_topics": len(self._topics),
            "areas": dict(sorted(areas.items(), key=lambda x: x[0])),
            "maturity": maturity_totals,
            "area_maturity": area_maturity,
        }


def _default_topics_path() -> Path:
    # Project root is parent of ``src/``
    here = Path(__file__).resolve().parent.parent.parent
    return here / "config" / "topics.yaml"
