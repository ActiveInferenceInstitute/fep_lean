"""Shared Lean toolchain path resolution helpers.

Both ``lean_verifier.py`` and ``environment.py`` need to locate the Lean/Lake
binaries and set up a writable ELAN_HOME for sandboxed environments.  This
module provides the common primitives so the resolution logic is defined once.
"""

from __future__ import annotations

import os
import tempfile
from pathlib import Path


def get_elan_home() -> Path:
    """Return the ELAN_HOME directory, respecting environment overrides."""
    return Path(os.environ.get("ELAN_HOME", str(Path.home() / ".elan")))


def get_elan_toolchains() -> Path:
    """Return ``<ELAN_HOME>/toolchains``."""
    return get_elan_home() / "toolchains"


def get_writable_elan_home() -> str:
    """Return a writable ELAN_HOME for sandboxed sub-processes.

    If ``ELAN_HOME`` is already set, returns that value. Otherwise falls back
    to a temp directory so the elan proxy can initialise without writing to
    ``~/.elan/settings.toml``.
    """
    if env := os.environ.get("ELAN_HOME"):
        return env
    return str(Path(tempfile.gettempdir()) / "fep_lean_elan")


def ensure_writable_elan_home() -> None:
    """Create the writable ELAN_HOME directory if it doesn't exist."""
    try:
        Path(get_writable_elan_home()).mkdir(parents=True, exist_ok=True)
    except OSError:
        pass


def read_toolchain_name(lean_dir: Path) -> str | None:
    """Read ``lean-toolchain`` and return the elan-style toolchain name.

    E.g. ``leanprover/lean4:v4.29.0`` → ``leanprover--lean4---v4.29.0``.
    Returns ``None`` if the file is missing.
    """
    tc_file = lean_dir / "lean-toolchain"
    if not tc_file.is_file():
        return None
    raw = tc_file.read_text(encoding="utf-8").strip()
    return raw.replace("/", "--").replace(":", "---")


def find_toolchain_bin(lean_dir: Path | None = None) -> Path | None:
    """Return the ``bin/`` directory of the matching (or newest) toolchain.

    Resolution order:
      1. Match the name in ``lean-toolchain`` if *lean_dir* is given.
      2. Fall back to the newest toolchain in ``~/.elan/toolchains/``.

    All filesystem access is wrapped in try/except to handle macOS sandbox
    ``PermissionError`` when the agent shell cannot stat ``~/.elan``.
    """
    toolchains = get_elan_toolchains()
    try:
        if not toolchains.is_dir():
            return None
    except (OSError, PermissionError):
        return None

    if lean_dir:
        tc_name = read_toolchain_name(lean_dir)
        if tc_name:
            try:
                candidate = toolchains / tc_name / "bin"
                if candidate.is_dir():
                    return candidate
            except (OSError, PermissionError):
                pass

    try:
        candidates = sorted(
            (d / "bin" for d in toolchains.iterdir() if (d / "bin").is_dir()),
            key=lambda p: p.parent.stat().st_mtime,
            reverse=True,
        )
        return candidates[0] if candidates else None
    except (OSError, PermissionError):
        return None


def subprocess_env(lean_dir: Path | None = None) -> dict[str, str]:
    """Build an environment dict for lean/lake sub-processes.

    Sets ``ELAN_HOME`` to a writable location and optionally prepends the
    direct toolchain ``bin/`` to ``PATH``.
    """
    env = dict(os.environ)
    env["ELAN_HOME"] = get_writable_elan_home()
    ensure_writable_elan_home()

    tc_bin = find_toolchain_bin(lean_dir)
    if tc_bin:
        env["PATH"] = str(tc_bin) + ":" + env.get("PATH", "")

    return env
