"""Pytest configuration for fep_lean tests.

Setup:
- Adds ``src/`` to ``sys.path`` so test imports resolve without installation.
- Sets ``MPLBACKEND=Agg`` for headless matplotlib.
- Probes for ``gauss``, ``lake``, ``lean`` on PATH (or ``~/.elan/bin``).
- Sets ``FEP_LEAN_TOOLS_MISSING`` env var (comma-separated) when tools are absent.
- Defaults ``FEP_LEAN_GAUSS_WORKFLOWS=0`` so unit tests skip LLM/Lean calls.

Coverage notes:
    ~8% of src/ is uncovered because it requires live Lean toolchain (lake/lean)
    or network access (Hermes API). These paths are tested when
    FEP_LEAN_GAUSS_WORKFLOWS=1 and FEP_LEAN_LIVE_TESTS=1 are set.
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


def pytest_configure(config: pytest.Config) -> None:  # noqa: ARG001
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
    # Force catalogue-only mode at session start so inherited shell env does not
    # accidentally enable live Hermes/Lean workflows for offline tests.
    os.environ["FEP_LEAN_GAUSS_WORKFLOWS"] = "0"
