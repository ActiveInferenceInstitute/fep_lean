"""Pytest configuration for fep_lean tests.

Setup:
- Adds ``src/`` to ``sys.path`` so test imports resolve without installation.
- Sets ``MPLBACKEND=Agg`` for headless matplotlib.
- Probes for ``gauss``, ``lake``, ``lean`` on PATH (or ``~/.elan/bin``).
- Sets ``FEP_LEAN_TOOLS_MISSING`` env var (comma-separated) when tools are absent.

Coverage notes:
    Remaining branches include live Lean and provider paths. Provider calls run
    only under explicit live-test selection with configured credentials.
"""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

import pytest

os.environ.setdefault("MPLBACKEND", "Agg")

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


def pytest_configure(config: pytest.Config) -> None:
    """Warn (not hard-exit) when gauss / lake / lean are not on PATH.

    Individual tests that require these tools use ``pytest.skip`` themselves.
    Sets FEP_LEAN_TOOLS_MISSING env var listing any absent tools.
    """
    missing = [name for name in ("gauss", "lake", "lean") if not shutil.which(name)]
    # Also probe ~/.elan/bin (elan-managed lean may not be on PATH in sandboxed shells)
    elan_bin = Path.home() / ".elan" / "bin"
    still_missing = [m for m in missing if not (elan_bin / m).is_file()]
    if still_missing:
        # Don't hard-exit — let tests that gracefully handle missing tools still run.
        os.environ["FEP_LEAN_TOOLS_MISSING"] = ",".join(still_missing)
    else:
        os.environ.setdefault("FEP_LEAN_REQUIRE_GAUSS", "1")
