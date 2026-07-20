"""Tests for the canonical fep-lean command-line entrypoint."""

from __future__ import annotations

from pathlib import Path

import cli


class _Result:
    def __init__(self, complete: bool) -> None:
        self.complete = complete

    def as_dict(self) -> dict[str, bool]:
        return {"complete": self.complete}


def test_build_parser_registers_all_commands() -> None:
    parser = cli.build_parser()
    assert parser.parse_args(["catalogue", "--area", "FEP", "--topic", "fep-001"]).command == "catalogue"
    assert parser.parse_args(["run", "--workflow", "review"]).workflow == "review"
    assert parser.parse_args(["topic", "fep-001"]).topic_id == "fep-001"
    assert parser.parse_args(["report"]).command == "report"


def test_print_result_handles_complete_and_incomplete_results() -> None:
    assert cli._print_result(_Result(True)) == 0
    assert cli._print_result(_Result(False)) == 1
    assert cli._print_result({"status": "error"}) == 1


def test_setup_requires_lake(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.delenv("FEP_LEAN_LAKE_EXE", raising=False)
    monkeypatch.setenv("PATH", "")
    assert cli._setup(tmp_path) == 1


def test_setup_runs_cache_and_build(monkeypatch, tmp_path: Path) -> None:
    (tmp_path / "lean").mkdir()
    lake = tmp_path / "lake"
    lake.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    lake.chmod(0o755)
    monkeypatch.setenv("FEP_LEAN_LAKE_EXE", str(lake))
    assert cli._setup(tmp_path) == 0


def test_setup_returns_lake_failure(monkeypatch, tmp_path: Path) -> None:
    (tmp_path / "lean").mkdir()
    lake = tmp_path / "lake"
    lake.write_text("#!/bin/sh\nexit 7\n", encoding="utf-8")
    lake.chmod(0o755)
    monkeypatch.setenv("FEP_LEAN_LAKE_EXE", str(lake))
    assert cli._setup(tmp_path) == 7


def test_main_dispatches_pipeline_commands(monkeypatch) -> None:
    calls: list[tuple[str, dict[str, object]]] = []

    def fake_pipeline(**kwargs):
        calls.append(("pipeline", kwargs))
        return _Result(True)

    def fake_topic(topic_id: str, **kwargs):
        calls.append((topic_id, kwargs))
        return _Result(True)

    monkeypatch.setattr(cli, "run_pipeline", fake_pipeline)
    monkeypatch.setattr(cli, "run_single_topic", fake_topic)

    assert cli.main(["catalogue", "--area", "FEP", "--topic", "fep-001"]) == 0
    assert cli.main(["run", "--workflow", "review"]) == 0
    assert cli.main(["topic", "fep-001", "--workflow", "prove"]) == 0
    assert cli.main(["report"]) == 0

    assert calls[0] == (
        "pipeline",
        {"mode": "catalogue", "area_filter": "FEP", "topic_filter": ["fep-001"]},
    )
    assert calls[1][1]["workflow"] == "review"
    assert calls[2] == ("fep-001", {"mode": "full", "workflow": "prove"})
    assert calls[3] == ("pipeline", {"mode": "catalogue"})


def test_main_preflight_returns_error_for_incomplete_root(monkeypatch, tmp_path: Path) -> None:
    assert cli.main(["--project-root", str(tmp_path), "--verbose", "preflight"]) == 1
