"""Figure files exist and are non-empty."""

from __future__ import annotations

from pathlib import Path

import pytest
from catalogue.topics import FEPTopicCatalogue
from output.figures import (
    _write_bar_chart,
    _write_maturity_heatmap,
    _write_pipeline_dag,
    _write_sequence_diagram,
    _write_sorry_distribution,
    write_all_catalogue_figures,
)

PROJ = Path(__file__).resolve().parent.parent


def test_write_all_catalogue_figures(tmp_path: Path) -> None:
    c = FEPTopicCatalogue.from_yaml(PROJ / "config" / "topics.yaml")
    paths = write_all_catalogue_figures(c, tmp_path)
    assert len(paths) == 9
    for p in paths:
        assert p.stat().st_size > 2000


def test_write_all_catalogue_figures_serial_env(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """``FEP_LEAN_FIGURES_MP=0`` exercises in-process sequential path."""
    monkeypatch.setenv("FEP_LEAN_FIGURES_MP", "0")
    c = FEPTopicCatalogue.from_yaml(PROJ / "config" / "topics.yaml")
    paths = write_all_catalogue_figures(c, tmp_path)
    assert len(paths) == 9
    for p in paths:
        assert p.stat().st_size > 2000


def test_write_bar_chart_show_pct(tmp_path: Path) -> None:
    """Percentage labels rendered when show_pct=True without error."""
    out = tmp_path / "pct.png"
    _write_bar_chart({"real": 50, "partial": 0, "aspirational": 0}, "Test", out, show_pct=True)
    assert out.stat().st_size > 1000


def test_write_bar_chart_subtitle(tmp_path: Path) -> None:
    """Subtitle text path renders without error."""
    out = tmp_path / "subtitle.png"
    _write_bar_chart(
        {"a": 10, "b": 5},
        "Title",
        out,
        subtitle="All topics sorry-free",
    )
    assert out.stat().st_size > 1000


def test_write_maturity_heatmap_all_real(tmp_path: Path) -> None:
    """All-real corpus uses Greens cmap and annotation without error."""
    area_maturity = {
        "FEP": {"real": 14, "partial": 0, "aspirational": 0},
        "ActiveInference": {"real": 11, "partial": 0, "aspirational": 0},
    }
    out = tmp_path / "heatmap_real.png"
    _write_maturity_heatmap(area_maturity, out)
    assert out.stat().st_size > 1000


def test_write_maturity_heatmap_mixed(tmp_path: Path) -> None:
    """Mixed maturity uses Blues cmap (non-all-real path)."""
    area_maturity = {
        "FEP": {"real": 5, "partial": 3, "aspirational": 2},
        "ActiveInference": {"real": 4, "partial": 2, "aspirational": 1},
    }
    out = tmp_path / "heatmap_mixed.png"
    _write_maturity_heatmap(area_maturity, out)
    assert out.stat().st_size > 1000


def test_write_sorry_distribution_all_real(tmp_path: Path) -> None:
    """All-real corpus produces single-slice donut with center label."""
    out = tmp_path / "donut_real.png"
    _write_sorry_distribution({"real": 50, "partial": 0, "aspirational": 0}, out)
    assert out.stat().st_size > 1000


def test_write_sorry_distribution_mixed(tmp_path: Path) -> None:
    """Mixed maturity corpus produces multi-slice donut."""
    out = tmp_path / "donut_mixed.png"
    _write_sorry_distribution({"real": 30, "partial": 12, "aspirational": 8}, out)
    assert out.stat().st_size > 1000


def test_write_pipeline_dag_creates_file(tmp_path: Path) -> None:
    """DAG with subtitle and duration hints renders without error."""
    out = tmp_path / "dag.png"
    _write_pipeline_dag(out)
    assert out.stat().st_size > 1000


def test_write_sequence_diagram_four_actors(tmp_path: Path) -> None:
    """Sequence diagram with 4 actors and 7 steps renders without error."""
    out = tmp_path / "seq.png"
    _write_sequence_diagram(out)
    assert out.stat().st_size > 1000
