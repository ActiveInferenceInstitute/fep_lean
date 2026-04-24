"""Tests for gauss.cli sad paths using genuine filesystem/env mutation (no unittest.mock)."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest

from gauss.cli import _require_gauss_from_env, check_gauss_cli, workflows_enabled

PROJ = Path(__file__).resolve().parent.parent

def test_require_gauss_from_env(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("FEP_LEAN_REQUIRE_GAUSS", "1")
    assert _require_gauss_from_env() is True
    monkeypatch.setenv("FEP_LEAN_REQUIRE_GAUSS", "false")
    assert _require_gauss_from_env() is False

def test_workflows_enabled(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("FEP_LEAN_GAUSS_WORKFLOWS", "yes")
    assert workflows_enabled() is True
    monkeypatch.setenv("FEP_LEAN_GAUSS_WORKFLOWS", "0")
    assert workflows_enabled() is False

def test_check_gauss_cli_missing_not_required(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    # Ensure gauss is not on path
    monkeypatch.setenv("PATH", str(tmp_path))
    monkeypatch.setenv("FEP_LEAN_SKIP_FALLBACKS", "1")
    ok, msg = check_gauss_cli(PROJ, require=False)
    assert ok is True
    assert "not on PATH" in msg

def test_check_gauss_cli_missing_required(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    monkeypatch.setenv("PATH", str(tmp_path))
    monkeypatch.setenv("FEP_LEAN_SKIP_FALLBACKS", "1")
    ok, msg = check_gauss_cli(PROJ, require=True)
    assert ok is False
    assert "not on PATH" in msg

def test_check_gauss_cli_exit_error(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    # Create a fake gauss binary that exits with error
    fake_gauss = tmp_path / "gauss"
    fake_gauss.write_text("#!/bin/sh\necho 'doctor failed' >&2\nexit 1\n")
    fake_gauss.chmod(0o755)
    
    monkeypatch.setenv("PATH", str(tmp_path))
    
    ok, msg = check_gauss_cli(PROJ, require=True)
    assert ok is False
    assert "doctor failed" in msg

    ok, msg = check_gauss_cli(PROJ, require=False)
    assert ok is True
    assert "non-fatal" in msg

def test_check_gauss_cli_fallback_path(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    """Cover the fallback path loop (lines 41-44) when gauss is not on PATH but exists at a fallback."""
    # Clear PATH so shutil.which("gauss") returns None
    monkeypatch.setenv("PATH", str(tmp_path / "empty_bin"))
    (tmp_path / "empty_bin").mkdir()
    # Don't skip fallbacks
    monkeypatch.delenv("FEP_LEAN_SKIP_FALLBACKS", raising=False)

    # Create a fake gauss at /tmp/gauss (a known fallback location)
    fake = Path("/tmp/gauss")
    created = False
    if not fake.is_file():
        fake.write_text("#!/bin/sh\necho 'fallback ok'\nexit 0\n")
        fake.chmod(0o755)
        created = True
    try:
        ok, msg = check_gauss_cli(tmp_path, require=False)
        assert ok is True
    finally:
        if created:
            fake.unlink(missing_ok=True)

def test_check_gauss_cli_ok(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    fake_gauss = tmp_path / "gauss"
    fake_gauss.write_text("#!/bin/sh\necho 'everything is fine'\nexit 0\n")
    fake_gauss.chmod(0o755)
    
    monkeypatch.setenv("PATH", str(tmp_path))
    
    # Needs a fake PROJ to write the report to
    root = tmp_path / "proj"
    root.mkdir()
    
    ok, msg = check_gauss_cli(root, require=True)
    assert ok is True
    assert "everything is fine" in msg
