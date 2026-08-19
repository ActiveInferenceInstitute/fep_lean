"""gauss_cli helpers (math-inc Open Gauss) — real ``gauss doctor`` only."""

from __future__ import annotations

import os

import pytest

import gauss.cli as gauss_cli

pytestmark = pytest.mark.timeout(180)


@pytest.mark.skipif(
    "gauss" in os.environ.get("FEP_LEAN_TOOLS_MISSING", ""), reason="gauss CLI missing"
)
def test_gauss_doctor_real_without_project_root() -> None:
    ok, msg = gauss_cli.check_gauss_cli(None, require=True)
    assert ok is True
    assert "gauss" in msg.lower()
