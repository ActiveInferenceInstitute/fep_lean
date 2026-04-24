"""gauss_cli helpers (math-inc Open Gauss) — real ``gauss doctor`` only."""

from __future__ import annotations

from pathlib import Path

import pytest

import gauss.cli as gauss_cli

PROJ = Path(__file__).resolve().parent.parent

pytestmark = pytest.mark.timeout(180)


def test_workflows_enabled_false(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("FEP_LEAN_GAUSS_WORKFLOWS", raising=False)
    assert gauss_cli.workflows_enabled() is False


def test_workflows_enabled_true(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FEP_LEAN_GAUSS_WORKFLOWS", "1")
    assert gauss_cli.workflows_enabled() is True


import os

@pytest.mark.skipif("gauss" in os.environ.get("FEP_LEAN_TOOLS_MISSING", ""),
                    reason="gauss CLI missing")
def test_gauss_doctor_real(tmp_path: Path) -> None:
    """Runs the installed ``gauss doctor``; writes JSON when project_root is set."""
    root = tmp_path / "proj"
    (root / "output" / "reports").mkdir(parents=True)
    ok, msg = gauss_cli.check_gauss_cli(root, require=True)
    assert ok is True
    assert "gauss" in msg.lower()
    assert (root / "output" / "reports" / "gauss_doctor_last.json").is_file()


@pytest.mark.skipif("gauss" in os.environ.get("FEP_LEAN_TOOLS_MISSING", ""),
                    reason="gauss CLI missing")
def test_gauss_doctor_real_without_project_root() -> None:
    ok, msg = gauss_cli.check_gauss_cli(None, require=True)
    assert ok is True
    assert "gauss" in msg.lower()
