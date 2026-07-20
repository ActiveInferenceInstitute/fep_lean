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
_AREAS = {"FEP", "ActiveInference", "BayesianMechanics", "InfoGeometry", "Thermodynamics"}


class CatalogueValidationError(ValueError):
    """Raised when the catalogue cannot be trusted as a verification input."""


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
        """Load and validate the complete catalogue from YAML.

        Validation is deliberately strict because downstream Lean and report
        stages use this file as their source of truth. Missing or extra rows,
        malformed identifiers, absent theorem bodies, and mismatched equation
        signatures are rejected before any external service is contacted.
        """
        resolved = path if path is not None else _default_topics_path()
        try:
            data = yaml.safe_load(resolved.read_text(encoding="utf-8"))
        except (OSError, yaml.YAMLError) as exc:
            raise CatalogueValidationError(f"cannot read catalogue {resolved}: {exc}") from exc
        if not isinstance(data, dict) or not isinstance(data.get("topics"), list):
            raise CatalogueValidationError("catalogue must contain a top-level topics list")
        raw = data["topics"]
        if len(raw) != 50:
            raise CatalogueValidationError(f"catalogue must contain exactly 50 topics, found {len(raw)}")
        topics: list[TopicEntry] = []
        required = {"id", "title", "area", "mathlib", "mathlib_status", "nl", "lean_sketch", "latex_equations"}
        for index, row in enumerate(raw, 1):
            if not isinstance(row, dict):
                raise CatalogueValidationError(f"topic row {index} must be a mapping")
            missing = required - set(row)
            if missing:
                raise CatalogueValidationError(f"topic row {index} missing fields: {', '.join(sorted(missing))}")
            expected_id = f"fep-{index:03d}"
            if row["id"] != expected_id:
                raise CatalogueValidationError(f"topic row {index} must have id {expected_id!r}")
            if row["area"] not in _AREAS:
                raise CatalogueValidationError(f"{expected_id}: unsupported area {row['area']!r}")
            if str(row["mathlib_status"]).strip().lower() not in _MATURITY_ORDER:
                raise CatalogueValidationError(f"{expected_id}: unsupported mathlib_status")
            if not all(isinstance(row[key], str) and row[key].strip() for key in ("title", "mathlib", "nl", "lean_sketch")):
                raise CatalogueValidationError(f"{expected_id}: title, mathlib, nl, and lean_sketch must be non-empty strings")
            raw_latex = row.get("latex_equations")
            if not isinstance(raw_latex, list) or not raw_latex or not all(isinstance(x, str) and x.strip() for x in raw_latex):
                raise CatalogueValidationError(f"{expected_id}: latex_equations must be a non-empty list of strings")
            latex_eqs = tuple(raw_latex)
            theorem_count = sum(1 for line in str(row["lean_sketch"]).splitlines() if line.lstrip().startswith("theorem "))
            if theorem_count != len(latex_eqs):
                raise CatalogueValidationError(f"{expected_id}: {theorem_count} theorem declarations but {len(latex_eqs)} equations")
            topics.append(
                TopicEntry(
                    id=row["id"], title=row["title"], area=row["area"], mathlib=row["mathlib"],
                    mathlib_status=str(row["mathlib_status"]).strip().lower(), nl=row["nl"],
                    lean_sketch=row["lean_sketch"],
                    latex_equations=latex_eqs,
                )
            )
        ids = [topic.id for topic in topics]
        if len(set(ids)) != len(ids):
            raise CatalogueValidationError("catalogue topic identifiers must be unique")
        _validate_sketch_source_parity(resolved, topics)
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


def _validate_sketch_source_parity(path: Path, topics: list[TopicEntry]) -> None:
    """Ensure the YAML sketches match the maintained Python sketch source."""
    project_root = path.resolve().parent.parent
    scripts_dir = project_root / "scripts"
    if not scripts_dir.is_dir():
        return
    if str(scripts_dir) not in __import__("sys").path:
        __import__("sys").path.insert(0, str(scripts_dir))
    try:
        from catalogue_sketches import SKETCHES  # type: ignore[import-not-found]
    except (ImportError, AttributeError):
        return
    for topic in topics:
        source = SKETCHES.get(topic.id)
        if source is not None and source.strip() != topic.lean_sketch.strip():
            raise CatalogueValidationError(f"{topic.id}: YAML lean_sketch differs from scripts/catalogue_sketches.py")
