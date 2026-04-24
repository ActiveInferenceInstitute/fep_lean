"""Tests for verification.preflight — real subprocesses, no mocks."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from verification.preflight import _run_version, run_preflight

PROJ = Path(__file__).resolve().parent.parent


def test_run_version_missing_binary() -> None:
    code, line = _run_version(["/nonexistent/fep_lean_preflight_binary", "--version"])
    assert code == 1
    assert isinstance(line, str)
    assert len(line) > 0


def test_run_preflight_returns_zero_or_one() -> None:
    c = run_preflight(require_gauss=False)
    assert c in (0, 1)


def test_run_preflight_require_gauss_when_missing(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Cover the gauss-missing path by hiding gauss from PATH."""
    monkeypatch.setenv("PATH", str(tmp_path))
    monkeypatch.setenv("FEP_LEAN_SKIP_FALLBACKS", "1")
    assert run_preflight(require_gauss=True) == 1


def test_run_version_with_real_binary() -> None:
    """Cover the success branch of _run_version with a real binary."""
    code, line = _run_version([sys.executable, "--version"])
    assert code == 0
    assert "Python" in line or "python" in line.lower()


def test_run_preflight_gauss_required_missing_with_env(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Cover the gauss-fail early return in run_preflight with isolated PATH."""
    monkeypatch.setenv("PATH", str(tmp_path))
    monkeypatch.setenv("FEP_LEAN_SKIP_FALLBACKS", "1")
    assert run_preflight(require_gauss=True) == 1


def test_preflight_main_cli_smoke() -> None:
    """Exercise ``main()`` (argparse + sys.exit) without mocking."""
    code = (
        "import sys\n"
        "sys.path.insert(0, 'src')\n"
        "sys.argv = ['fep-lean-preflight']\n"
        "from verification.preflight import main\n"
        "main()\n"
    )
    r = subprocess.run(
        [sys.executable, "-c", code],
        cwd=str(PROJ),
        capture_output=True,
        text=True,
        timeout=180,
        check=False,
    )
    assert r.returncode in (0, 1)


def test_preflight_main_require_gauss(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Exercise main() directly, failing via missing gauss."""
    monkeypatch.setenv("PATH", str(tmp_path))
    monkeypatch.setenv("FEP_LEAN_SKIP_FALLBACKS", "1")
    monkeypatch.setattr(sys, "argv", ["fep-lean-preflight", "--require-gauss"])
    from verification.preflight import main
    with pytest.raises(SystemExit) as exc:
        main()
    assert exc.value.code == 1


def test_run_preflight_happy_path(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Use dummy scripts in a fake project root to cover the final success paths (lines 50-61)."""
    # 1. Create a fake project layout
    fake_root = tmp_path / "proj"
    fake_lean = fake_root / "lean"
    fake_lean.mkdir(parents=True)
    
    # Fake Mathlib.olean and the leaf .olean files probed by check_mathlib_built
    # (see LeanVerifier.check_mathlib_built — partial caches are now treated as
    # "not built" so a stub root alone is no longer sufficient).
    mathlib_dir = fake_lean / ".lake" / "packages" / "mathlib" / ".lake" / "build" / "lib"
    mathlib_dir.mkdir(parents=True)
    (mathlib_dir / "Mathlib.olean").write_text("dummy")
    for leaf in (
        "Mathlib/Data/Real/Basic.olean",
        "Mathlib/Algebra/Order/Ring/Basic.olean",
        "Mathlib/MeasureTheory/Measure/MeasureSpace.olean",
    ):
        leaf_path = mathlib_dir / leaf
        leaf_path.parent.mkdir(parents=True, exist_ok=True)
        leaf_path.write_text("dummy")

    # Override project_root using monkeypatch so we don't mutate global state or use unittest.mock
    from verification import preflight
    monkeypatch.setattr(preflight, "project_root", lambda: fake_root)

    # 2. Provide dummy binaries for `lean` and `lake` that exit 0
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    
    lean_bin = bin_dir / "lean"
    lean_bin.write_text("#!/bin/sh\necho Lean\nexit 0\n")
    lean_bin.chmod(0o755)

    lake_bin = bin_dir / "lake"
    lake_bin.write_text("#!/bin/sh\necho Lake\nexit 0\n")
    lake_bin.chmod(0o755)

    monkeypatch.setenv("PATH", str(bin_dir))

    # We also need a dummy gauss OR we can just pass require_gauss=False
    # (since require_gauss=False doesn't hard-fail if missing)
    status = preflight.run_preflight(require_gauss=False)
    assert status == 0
