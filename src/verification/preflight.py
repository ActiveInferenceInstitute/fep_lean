"""Preflight: optional ``gauss doctor``, ``lean``/``lake`` versions, Mathlib build check.

When invoked as a CLI (``__main__``) the output is rendered to ``stdout`` via
``print()`` so the user sees clean ``[lake] …`` / ``[mathlib] …`` lines.  When
imported as a library, the same status lines are routed through ``logging`` so
they integrate with the host application's log handlers instead of polluting
``stdout``.
"""

from __future__ import annotations

import argparse
import logging
import subprocess
import sys

from _paths import project_root
from gauss.cli import check_gauss_cli
from verification.lean_verifier import LeanVerifier

log = logging.getLogger(__name__)
# Routed to logging when ``run_preflight`` is called from another module; reset
# to ``print`` by ``main()`` for CLI invocation so the existing UX is unchanged.
_emit = log.info  # type: ignore[assignment]


def _run_version(cmd: list[str], cwd=None) -> tuple[int, str]:
    """Capture the first stdout/stderr line of ``cmd``.

    ``cwd`` is forwarded to ``subprocess.run`` so callers can resolve the
    workspace-pinned toolchain (``lean/lean-toolchain`` via Elan) instead of
    whichever default ``lean``/``lake`` happens to be on the ambient PATH.
    """
    try:
        proc = subprocess.run(
            cmd, capture_output=True, text=True, timeout=60, check=False, cwd=cwd
        )
        out = (proc.stdout or proc.stderr or "").strip()
        return proc.returncode, out.splitlines()[0] if out else "(no output)"
    except (OSError, subprocess.TimeoutExpired) as e:
        return 1, str(e)


def run_preflight(*, require_gauss: bool | None = None) -> int:
    """Return 0 if all required checks pass; 1 otherwise."""
    root = project_root()
    lean_dir = root / "lean"
    verifier = LeanVerifier(lean_dir, root)

    _emit("fep_lean preflight — project root: %s", root)

    ok, msg = check_gauss_cli(root, require=require_gauss)
    _emit("[gauss] %s", msg)
    if not ok:
        return 1

    lake_ok = verifier.check_lake_available()
    _emit("[lake] %s", "available" if lake_ok else "not available or not working in lean/")
    if not lake_ok:
        return 1

    code, line = _run_version(["lean", "--version"], cwd=lean_dir)
    _emit("[lean] %s", line if code == 0 else f"failed ({line})")
    if code != 0:
        return 1

    code, line = _run_version(["lake", "--version"], cwd=lean_dir)
    _emit("[lake] %s", line if code == 0 else f"failed ({line})")
    if code != 0:
        return 1

    mathlib_ok, mathlib_msg = verifier.check_mathlib_built()
    _emit("[mathlib] %s", mathlib_msg)
    if not mathlib_ok:
        _emit(
            "[mathlib] Run: bash projects/fep_lean/scripts/_maint_bootstrap_lean_toolchain.sh "
            "(or `uv run python scripts/00_setup_environment.py --project fep_lean` from repo root)"
        )
        return 1

    _emit("Preflight OK.")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description="Check gauss (optional), lean/lake, and Mathlib oleans.")
    parser.add_argument(
        "--require-gauss",
        action="store_true",
        help="Fail if gauss is missing or gauss doctor fails (same as FEP_LEAN_REQUIRE_GAUSS=1).",
    )
    args = parser.parse_args()
    require = True if args.require_gauss else None
    global _emit
    _emit = lambda fmt, *a: print(fmt % a if a else fmt)  # noqa: E731
    sys.exit(run_preflight(require_gauss=require))


if __name__ == "__main__":
    main()
