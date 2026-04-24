"""Integration with [math-inc/OpenGauss](https://github.com/math-inc/OpenGauss) ``gauss`` CLI."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any

_DOCTOR_TIMEOUT_S = 120.0


def _require_gauss_from_env() -> bool:
    v = os.environ.get("FEP_LEAN_REQUIRE_GAUSS", "").strip().lower()
    return v in ("1", "true", "yes", "on")


def check_gauss_cli(project_root: Path | None, *, require: bool | None = None) -> tuple[bool, str]:
    """Run ``gauss doctor`` when the CLI exists.

    If ``gauss`` is missing: fails only when ``require`` is True or
    ``FEP_LEAN_REQUIRE_GAUSS`` is set in the environment.

    On success and ``project_root`` set, writes ``output/reports/gauss_doctor_last.json``.
    """
    if require is None:
        require = _require_gauss_from_env()

    # Check PATH first; also probe known install locations used by fep_lean setup.
    _FALLBACK_PATHS = [
        os.path.expanduser("~/.local/bin/gauss"),
        "/tmp/gauss",  # assessment-installed wrapper (math-inc/OpenGauss)
        os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", ".bin", "gauss")),
    ]
    exe = shutil.which("gauss")
    skip_fallbacks = os.environ.get("FEP_LEAN_SKIP_FALLBACKS", "").lower() in ("1", "true", "yes")

    if not exe and not skip_fallbacks:
        for _fp in _FALLBACK_PATHS:
            if os.path.isfile(_fp) and os.access(_fp, os.X_OK):
                exe = _fp
                break
    if not exe:
        if require:
            return False, "gauss: not on PATH (set FEP_LEAN_REQUIRE_GAUSS=0 or install Open Gauss)"
        return (
            True,
            "gauss: not on PATH (optional; install: https://github.com/math-inc/OpenGauss)",
        )

    try:
        proc = subprocess.run(
            [exe, "doctor"],
            capture_output=True,
            text=True,
            timeout=_DOCTOR_TIMEOUT_S,
            check=False,
            env=os.environ.copy(),
        )
    except (OSError, subprocess.TimeoutExpired) as e:
        msg = f"gauss doctor: failed ({e})"
        if require:
            return False, msg
        return True, msg + " (non-fatal; FEP_LEAN_REQUIRE_GAUSS not set)"

    out = (proc.stdout or "").strip()
    err = (proc.stderr or "").strip()
    if proc.returncode != 0:
        snippet = (err or out)[:400]
        msg = f"gauss doctor: exit {proc.returncode} — {snippet}"
        if require:
            return False, msg
        return True, msg + " (non-fatal)"

    line = out.splitlines()[0] if out else "gauss doctor: ok"
    summary: dict[str, Any] = {
        "gauss_path": exe,
        "returncode": proc.returncode,
        "stdout_lines": len(out.splitlines()) if out else 0,
        "stderr_preview": err[:2000] if err else "",
    }
    if project_root is not None:
        reports = project_root / "output" / "reports"
        reports.mkdir(parents=True, exist_ok=True)
        dest = reports / "gauss_doctor_last.json"
        dest.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    return True, f"gauss doctor: ok ({line[:120]})"


def workflows_enabled() -> bool:
    """True when ``FEP_LEAN_GAUSS_WORKFLOWS=1`` (opt-in heavy Gauss steps)."""
    v = os.environ.get("FEP_LEAN_GAUSS_WORKFLOWS", "").strip().lower()
    return v in ("1", "true", "yes", "on")
