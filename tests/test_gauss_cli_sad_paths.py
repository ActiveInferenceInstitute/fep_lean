"""Tests for gauss.cli sad paths using genuine filesystem and environment mutation."""

from __future__ import annotations

from pathlib import Path

import pytest

from gauss.cli import _require_gauss_from_env, check_gauss_cli

PROJ = Path(__file__).resolve().parent.parent


def test_require_gauss_from_env(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("FEP_LEAN_REQUIRE_GAUSS", "1")
    assert _require_gauss_from_env() is True
    monkeypatch.setenv("FEP_LEAN_REQUIRE_GAUSS", "false")
    assert _require_gauss_from_env() is False


def test_check_gauss_cli_missing_not_required(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
):
    # Ensure gauss is not on path
    monkeypatch.setenv("PATH", str(tmp_path))
    ok, msg = check_gauss_cli(PROJ, require=False)
    assert ok is True
    assert "not configured" in msg


def test_check_gauss_cli_missing_required(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
):
    monkeypatch.setenv("PATH", str(tmp_path))
    ok, msg = check_gauss_cli(PROJ, require=True)
    assert ok is False
    assert "unavailable" in msg


def test_check_gauss_cli_exit_error(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    # Create a temporary gauss binary that exits with error
    temporary_gauss = tmp_path / "gauss"
    temporary_gauss.write_text("#!/bin/sh\necho 'doctor failed' >&2\nexit 1\n")
    temporary_gauss.chmod(0o755)

    monkeypatch.setenv("PATH", str(tmp_path))

    ok, msg = check_gauss_cli(PROJ, require=True)
    assert ok is False
    assert "doctor failed" in msg

    ok, msg = check_gauss_cli(PROJ, require=False)
    assert ok is True
    assert "doctor: exit 1" in msg


def test_check_gauss_cli_ok(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    temporary_gauss = tmp_path / "gauss"
    temporary_gauss.write_text("#!/bin/sh\necho 'everything is fine'\nexit 0\n")
    temporary_gauss.chmod(0o755)

    monkeypatch.setenv("PATH", str(tmp_path))

    # Needs a temporary PROJ to write the report to
    root = tmp_path / "proj"
    root.mkdir()

    ok, msg = check_gauss_cli(root, require=True)
    assert ok is True
    assert "everything is fine" in msg
