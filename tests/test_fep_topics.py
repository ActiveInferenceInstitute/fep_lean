"""Catalogue load and summary invariants."""

from __future__ import annotations

from pathlib import Path

import pytest
from catalogue.topics import CatalogueValidationError, FEPTopicCatalogue

PROJ = Path(__file__).resolve().parent.parent
TOPICS = PROJ / "config" / "topics.yaml"

_EXPECTED_AREAS = {
    "FEP": 14,
    "ActiveInference": 11,
    "BayesianMechanics": 10,
    "InfoGeometry": 8,
    "Thermodynamics": 7,
}


def test_catalogue_loads_50_topics() -> None:
    c = FEPTopicCatalogue.from_yaml(TOPICS)
    assert len(c.topics) == 50
    assert c.source_path == TOPICS
    ids = [t.id for t in c.topics]
    assert ids == [f"fep-{i:03d}" for i in range(1, 51)]


def test_summary_totals_match_manual_rollups() -> None:
    c = FEPTopicCatalogue.from_yaml(TOPICS)
    s = c.summary()
    assert s["total_topics"] == 50
    assert sum(s["areas"].values()) == 50
    assert s["areas"] == dict(sorted(_EXPECTED_AREAS.items(), key=lambda x: x[0]))
    mat = s["maturity"]
    assert mat["real"] + mat["partial"] + mat["aspirational"] == 50
    assert mat["real"] == 50
    assert mat["partial"] == 0
    assert mat["aspirational"] == 0
    for area, count in s["areas"].items():
        am = s["area_maturity"][area]
        assert am["real"] + am["partial"] + am["aspirational"] == count
        assert am["real"] == count
        assert am["partial"] == 0
        assert am["aspirational"] == 0


def test_topic_lean_chars_non_negative() -> None:
    c = FEPTopicCatalogue.from_yaml(TOPICS)
    for t in c.topics:
        assert t.lean_chars >= 0
        assert t.id.startswith("fep-")


def test_unknown_yaml_raises_or_empty() -> None:
    p = PROJ / "config" / "nonexistent_topics.yaml"
    with pytest.raises(CatalogueValidationError):
        FEPTopicCatalogue.from_yaml(p)


def test_from_yaml_default_path(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(PROJ)
    c = FEPTopicCatalogue.from_yaml()
    assert len(c.topics) == 50


def test_all_topics_mathlib_real() -> None:
    c = FEPTopicCatalogue.from_yaml(TOPICS)
    assert all(t.mathlib_status == "real" for t in c.topics)
    assert {t.id for t in c.topics} == {f"fep-{i:03d}" for i in range(1, 51)}
