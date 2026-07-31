"""Regression checks for the maintained semantic theorem audit."""

from __future__ import annotations

import sys
from pathlib import Path

PROJ = Path(__file__).resolve().parent.parent
SCRIPTS = PROJ / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))


def test_theorem_maturity_audit_covers_native_source() -> None:
    from theorem_maturity_audit import validate_audit

    data = validate_audit(PROJ)

    assert len(data["topics"]) == 50
    assert data["topics"][0]["id"] == "fep-001"
    assert data["topics"][-1]["id"] == "fep-050"
    assert all("native Lean compile" in row["acceptance_probe"] for row in data["topics"])
    assert any(row["disposition"] == "scope_gap" for row in data["topics"])
    assert any(row["disposition"] == "assumption_gap" for row in data["topics"])


def test_generated_theorem_maturity_projection_is_current() -> None:
    from theorem_maturity_audit import OUTPUT_PATH, render_markdown, validate_audit

    data = validate_audit(PROJ)

    assert OUTPUT_PATH.is_file()
    assert OUTPUT_PATH.read_text(encoding="utf-8") == render_markdown(data)
    text = OUTPUT_PATH.read_text(encoding="utf-8")
    assert "AUTO-GENERATED" in text
    assert text.count("| fep-") == 50
