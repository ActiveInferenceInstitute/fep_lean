"""Environment validation against the real project tree."""

from __future__ import annotations

from pathlib import Path

import pytest

import verification.environment as ec
from verification.environment import run_validation_checks

PROJ = Path(__file__).resolve().parent.parent

pytestmark = pytest.mark.timeout(180)


def test_run_validation_all_ok_on_project() -> None:
    r = run_validation_checks(PROJ)
    failed = [c for c in r["checks"] if not c["ok"]]
    assert r["status"] == "ok", f"Checks failed: {failed}"
    assert len(r["checks"]) == 13
    assert r["failed_count"] == 0
    names = [c["name"] for c in r["checks"]]
    assert "math_inc_gauss_cli" in names
    assert "lean_workspace" in names
    assert "lean_cli" in names
    assert "sqlite_session_store" not in names
