"""Shared process-group-safe runner for Lake/Lean compile probes.

Each readiness test file historically defined its own ``_run_lean`` using
``subprocess.run(..., timeout=N)``. On timeout, ``subprocess.run`` kills only
the direct child (``lake``); the grandchild ``lean`` process survives, holds
memory and the .olean lock region, and accumulates across a suite run until
the machine thrashes. Running through a new process group and killing the whole
group on timeout closes that leak (fep-tests HANDOFF, 2026-08-28/29).
"""

from __future__ import annotations

import os
import signal
import subprocess
from pathlib import Path

__all__ = ["run_lean_probe"]


def run_lean_probe(
    probe_path: Path,
    *,
    import_root: Path,
    cwd: Path,
    timeout_s: int = 300,
) -> subprocess.CompletedProcess[str]:
    """Compile ``probe_path`` via ``lake env lean -R import_root`` in its own process group."""
    command = [
        os.environ.get("FEP_LAKE_BIN", "lake"),
        "env",
        "lean",
        "-R",
        str(import_root),
        str(probe_path),
    ]
    process = subprocess.Popen(
        command,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        start_new_session=True,
    )
    try:
        stdout, stderr = process.communicate(timeout=timeout_s)
    except subprocess.TimeoutExpired:
        os.killpg(os.getpgid(process.pid), signal.SIGKILL)
        try:
            process.communicate(timeout=30)
        except Exception:
            pass
        raise
    return subprocess.CompletedProcess(command, process.returncode, stdout, stderr)
