"""Integration with [math-inc/OpenGauss](https://github.com/math-inc/OpenGauss) ``gauss`` CLI."""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

_DOCTOR_TIMEOUT_S = 120.0


def _require_gauss_from_env() -> bool:
    v = os.environ.get("FEP_LEAN_REQUIRE_GAUSS", "").strip().lower()
    return v in ("1", "true", "yes", "on")


def check_gauss_cli(project_root: Path | None, *, require: bool | None = None) -> tuple[bool, str]:
    """Run ``gauss doctor`` when the CLI exists.

    If ``gauss`` is missing: fails only when ``require`` is True or the
    explicit ``FEP_LEAN_REQUIRE_GAUSS`` setting is truthy.
    """
    if require is None:
        require = _require_gauss_from_env()

    exe = shutil.which("gauss")
    if not exe:
        return (False, "gauss: executable is unavailable") if require else (True, "gauss: not configured")

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
        return (False, msg) if require else (True, msg)

    out = (proc.stdout or "").strip()
    err = (proc.stderr or "").strip()
    if proc.returncode != 0:
        snippet = (err or out)[:400]
        msg = f"gauss doctor: exit {proc.returncode} — {snippet}"
        return (False, msg) if require else (True, msg)

    line = out.splitlines()[0] if out else "gauss doctor: ok"
    return True, f"gauss doctor: ok ({line[:120]})"
