"""Tests for the canonical fep-lean command-line entrypoint."""

from __future__ import annotations

import json
from pathlib import Path

import cli


class _Result:
    def __init__(self, complete: bool) -> None:
        self.complete = complete

    def as_dict(self) -> dict[str, bool]:
        return {"complete": self.complete}


def test_build_parser_registers_all_commands() -> None:
    parser = cli.build_parser()
    assert (
        parser.parse_args(["catalogue", "--area", "FEP", "--topic", "fep-001"]).command
        == "catalogue"
    )
    assert (
        parser.parse_args(["verify", "--area", "FEP", "--topic", "fep-001"]).command
        == "verify"
    )
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
    monkeypatch.setenv("ELAN_HOME", str(tmp_path / "elan"))
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


def test_setup_bootstraps_when_lake_is_not_on_path(monkeypatch, tmp_path: Path) -> None:
    (tmp_path / "scripts").mkdir()
    bootstrap = tmp_path / "scripts" / "_maint_bootstrap_lean_toolchain.sh"
    bootstrap.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    bootstrap.chmod(0o755)
    monkeypatch.delenv("FEP_LEAN_LAKE_EXE", raising=False)
    monkeypatch.setattr(cli, "find_executable", lambda *_args: None)
    calls: list[list[str]] = []

    def fake_run(command, **kwargs):
        calls.append(command)
        return type("Completed", (), {"returncode": 0})()

    monkeypatch.setattr(cli.subprocess, "run", fake_run)
    assert cli._setup(tmp_path) == 0
    assert calls == [["bash", str(bootstrap)]]


def test_setup_rejects_invalid_timeout(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("FEP_LEAN_SETUP_TIMEOUT_SEC", "not-an-int")
    assert cli._setup(tmp_path) == 1


def test_verify_command_is_lean_only(monkeypatch, tmp_path: Path, capsys) -> None:
    class Topic:
        def __init__(self) -> None:
            self.id = "fep-001"
            self.area = "FEP"
            self.lean_sketch = "theorem fixture : True := True.intro"

    class Catalogue:
        def __init__(self) -> None:
            self.topics = [Topic()]

    class VerifyResult:
        compiles = True
        has_sorry = False

        def as_dict(self) -> dict[str, object]:
            return {"topic_id": "fep-001", "compiles": True, "has_sorry": False}

    class FakeVerifier:
        def __init__(self, **kwargs) -> None:
            self.kwargs = kwargs

        def check_mathlib_built(self) -> tuple[bool, str]:
            return True, "fixture Mathlib cache"

        def verify_batch(self, items: list[tuple[str, str]]) -> list[VerifyResult]:
            assert items == [("fep-001", "theorem fixture : True := True.intro")]
            return [VerifyResult()]

    monkeypatch.setattr(
        cli.FEPTopicCatalogue, "from_yaml", staticmethod(lambda _path: Catalogue())
    )
    monkeypatch.setattr(cli, "LeanVerifier", FakeVerifier)
    assert (
        cli.main(["--project-root", str(tmp_path), "verify", "--topic", "fep-001"]) == 0
    )
    payload = json.loads(capsys.readouterr().out)
    assert payload["mode"] == "lean-only"
    assert payload["complete"] is True
    assert payload["verified_topics"] == 1
    assert payload["results"][0]["lean_file"] is None


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


def test_main_preflight_returns_error_for_incomplete_root(
    monkeypatch, tmp_path: Path
) -> None:
    assert cli.main(["--project-root", str(tmp_path), "--verbose", "preflight"]) == 1


def test_verify_rejects_unknown_topics(monkeypatch, tmp_path: Path, capsys) -> None:
    """Verify --topic with IDs not in the catalogue returns error."""

    class Topic:
        def __init__(self) -> None:
            self.id = "fep-001"
            self.area = "FEP"
            self.lean_sketch = "theorem fixture : True := True.intro"

    class Catalogue:
        def __init__(self) -> None:
            self.topics = [Topic()]

    mkdir = tmp_path / "config"
    mkdir.mkdir()
    monkeypatch.setattr(
        cli.FEPTopicCatalogue, "from_yaml", staticmethod(lambda _path: Catalogue())
    )
    result = cli.main(["--project-root", str(tmp_path), "verify", "--topic", "fep-999"])
    assert result == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "error"
    assert "unknown topic id" in payload["failure_reason"]


def test_verify_returns_error_when_no_topics_match(
    monkeypatch, tmp_path: Path, capsys
) -> None:
    """Verify with an area filter that matches nothing returns error."""

    class Topic:
        def __init__(self) -> None:
            self.id = "fep-001"
            self.area = "FEP"
            self.lean_sketch = "theorem fixture : True := True.intro"

    class Catalogue:
        def __init__(self) -> None:
            self.topics = [Topic()]

    mkdir = tmp_path / "config"
    mkdir.mkdir()
    monkeypatch.setattr(
        cli.FEPTopicCatalogue, "from_yaml", staticmethod(lambda _path: Catalogue())
    )
    result = cli.main(["--project-root", str(tmp_path), "verify", "--area", "AI"])
    assert result == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "error"
    assert "no catalogue topics matched" in payload["failure_reason"]


def test_print_result_returns_1_for_incomplete_object_without_as_dict() -> None:
    """_print_result returns 1 for objects lacking as_dict and complete=False fallback."""

    class Incomplete:
        pass

    assert cli._print_result(Incomplete()) == 1


def test_main_returns_2_for_unsupported_command(monkeypatch, tmp_path: Path) -> None:
    """An unrecognised subcommand returns exit code 2 via argparse error."""
    monkeypatch.setenv("FEP_LEAN_SETUP_TIMEOUT_SEC", "1800")
    try:
        cli.main(["--project-root", str(tmp_path), "nonexistent"])
        assert False, "expected SystemExit"
    except SystemExit as exc:
        assert exc.code == 2
