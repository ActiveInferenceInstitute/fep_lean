"""Capability validation contract."""

from pathlib import Path

from verification.environment import run_validation_checks

PROJ = Path(__file__).resolve().parent.parent


def test_catalogue_validation_is_read_only_capability_check() -> None:
    result = run_validation_checks(PROJ, mode="catalogue")
    assert result["status"] == "ok"
    assert result["mode"] == "catalogue"
    assert result["failed_count"] == 0
    assert all(check["ok"] for check in result["checks"])


def test_full_validation_reports_missing_capabilities_without_building(
    monkeypatch,
) -> None:
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    result = run_validation_checks(PROJ, mode="full")
    assert result["status"] == "error"
    assert any(
        check["name"] == "hermes_credentials" and not check["ok"]
        for check in result["checks"]
    )
    assert any(check["name"] == "mathlib_built" for check in result["checks"])
