"""Read-only capability validation for the standalone fep_lean project."""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Callable

from gauss.cli import check_gauss_cli
from verification._toolchain import find_toolchain_bin, get_writable_elan_home, subprocess_env

EXPECTED_LEAN_TOOLCHAIN = "leanprover/lean4:v4.29.0"
EXPECTED_MATHLIB_TAG = "v4.29.0"


def _get_elan_home() -> str:
    return get_writable_elan_home()


def _lean_subprocess_env() -> dict[str, str]:
    return subprocess_env()


def _find_toolchain_lean(lean_dir: Path | None = None) -> str | None:
    toolchain = find_toolchain_bin(lean_dir)
    candidate = toolchain / "lean" if toolchain else None
    return str(candidate) if candidate and candidate.is_file() else None


def _version_line(exe: str, cwd: Path | None = None) -> tuple[bool, str]:
    try:
        proc = subprocess.run([exe, "--version"], cwd=cwd, env=_lean_subprocess_env(), capture_output=True, text=True, timeout=5, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return False, str(exc)
    output = (proc.stdout or proc.stderr or "").strip().splitlines()
    return proc.returncode == 0, output[0] if output else f"{exe}: no version output"


def _check_lean_cli(project_root: Path | None = None) -> tuple[bool, str]:
    lean_dir = project_root / "lean" if project_root else None
    explicit = os.environ.get("FEP_LEAN_LEAN_EXE", "")
    lean = explicit if explicit and Path(explicit).is_file() else _find_toolchain_lean(lean_dir) or shutil.which("lean")
    if not lean:
        return False, "lean executable is unavailable"
    ok, line = _version_line(lean, lean_dir)
    if not ok:
        return False, f"lean invocation failed: {line}"
    if "4.29.0" not in line:
        return False, f"wrong Lean version: {line}; expected 4.29.0"
    return True, line


def _check_toolchain_pin(project_root: Path) -> tuple[bool, str]:
    path = project_root / "lean" / "lean-toolchain"
    if not path.is_file():
        return False, "lean/lean-toolchain is missing"
    actual = path.read_text(encoding="utf-8").strip()
    if actual != EXPECTED_LEAN_TOOLCHAIN:
        return False, f"toolchain pin {actual!r} does not equal {EXPECTED_LEAN_TOOLCHAIN!r}"
    lakefile = project_root / "lean" / "lakefile.lean"
    text = lakefile.read_text(encoding="utf-8") if lakefile.is_file() else ""
    if EXPECTED_MATHLIB_TAG not in text:
        return False, f"lakefile does not pin Mathlib {EXPECTED_MATHLIB_TAG}"
    return True, f"Lean {actual}; Mathlib {EXPECTED_MATHLIB_TAG}"


def _check_mathlib_built(project_root: Path) -> tuple[bool, str]:
    """Check the existing Mathlib build without downloading or compiling."""
    build_root = project_root / "lean" / ".lake" / "build" / "lib" / "lean"
    root_olean = build_root / "Mathlib.olean"
    if not root_olean.is_file():
        return False, f"Mathlib build artifact missing: {root_olean}"
    required = [build_root / "Mathlib" / "MeasureTheory" / "Measure" / "MeasureSpace.olean"]
    missing = [str(p) for p in required if not p.is_file()]
    if missing:
        return False, f"Mathlib build is incomplete; missing {missing[0]}"
    return True, f"Mathlib build present ({root_olean})"


def _check_lake(project_root: Path) -> tuple[bool, str]:
    lake_dir = project_root / "lean"
    explicit = os.environ.get("FEP_LEAN_LAKE_EXE", "")
    lake = explicit if explicit and Path(explicit).is_file() else shutil.which("lake")
    if not lake:
        return False, "lake executable is unavailable"
    ok, line = _version_line(lake, lake_dir)
    return (ok, line if ok else f"lake invocation failed: {line}")


def _check_gauss_config(project_root: Path) -> tuple[bool, str]:
    configured = os.environ.get("GAUSS_HOME", "").strip()
    path = Path(configured).expanduser() if configured else Path.home() / ".gauss"
    parent = path if path.is_dir() else path.parent
    if not parent.is_dir():
        return False, f"OpenGauss state directory parent is missing: {parent}"
    if not os.access(parent, os.W_OK):
        return False, f"OpenGauss state directory is not writable: {path}"
    return True, f"OpenGauss state directory available: {path}"


def _check_topics_yaml(project_root: Path) -> tuple[bool, str]:
    try:
        from catalogue.topics import FEPTopicCatalogue
        catalogue = FEPTopicCatalogue.from_yaml(project_root / "config" / "topics.yaml")
    except Exception as exc:
        return False, str(exc)
    return True, f"topics.yaml validated ({len(catalogue.topics)} topics)"


def _check_dirs(project_root: Path) -> tuple[bool, str]:
    required = ("manuscript", "config", "src", "lean", "scripts", "tests")
    missing = [rel for rel in required if not (project_root / rel).is_dir()]
    return (not missing, f"missing {', '.join(missing)}" if missing else "project layout present")


def _check_lean_workspace(project_root: Path) -> tuple[bool, str]:
    lean = project_root / "lean"
    if not (lean / "lakefile.lean").is_file():
        return False, "lean/lakefile.lean is missing"
    aggregate = lean / "FepSketches" / "fep_all.lean"
    if not aggregate.is_file():
        return False, "lean/FepSketches/fep_all.lean is missing"
    return True, "Lean workspace and canonical aggregate present"


def _check_python_stack() -> tuple[bool, str]:
    try:
        import matplotlib
        import numpy
        import yaml
        matplotlib.use("Agg")
    except Exception as exc:
        return False, str(exc)
    return True, f"Python {sys.version_info.major}.{sys.version_info.minor}; scientific stack present"


def _check_output_writable(project_root: Path) -> tuple[bool, str]:
    output = project_root / "output"
    parent = output if output.is_dir() else output.parent
    if not parent.is_dir():
        return False, f"output/ parent is missing: {parent}"
    if not os.access(parent, os.W_OK):
        return False, "output/ is not writable"
    return True, "output/ writable"


def _check_file(project_root: Path, relative: str) -> tuple[bool, str]:
    path = project_root / relative
    return (path.is_file(), f"{relative} present" if path.is_file() else f"{relative} missing")


def _check_references_bib(project_root: Path) -> tuple[bool, str]:
    return True, "references.bib optional"


# Focused check functions remain available for direct unit coverage. The
# pipeline itself uses the mode-aware dispatcher below.
def _check_catalogue_import(project_root: Path) -> tuple[bool, str]:
    return _check_topics_yaml(project_root)


def _check_dot_gauss_writable(project_root: Path | None = None) -> tuple[bool, str]:
    return _check_gauss_config(project_root or Path.cwd())


def _check_python_numpy_matplotlib() -> tuple[bool, str]:
    return _check_python_stack()


def _check_manuscript_config(project_root: Path) -> tuple[bool, str]:
    return _check_file(project_root, "manuscript/config.yaml")


def _check_scripts_tests(project_root: Path) -> tuple[bool, str]:
    return _check_dirs(project_root)


def run_validation_checks(project_root: Path, *, mode: str = "full") -> dict[str, Any]:
    """Run bounded, read-only checks for ``full`` or ``catalogue`` mode."""
    if mode not in {"full", "catalogue"}:
        raise ValueError(f"unsupported validation mode: {mode}")
    checks: list[dict[str, Any]] = []

    def run(name: str, fn: Callable[[], tuple[bool, str]]) -> None:
        started = time.perf_counter()
        try:
            ok, message = fn()
        except Exception as exc:
            ok, message = False, f"{type(exc).__name__}: {exc}"
        checks.append({"name": name, "ok": ok, "message": message, "duration_s": round(time.perf_counter() - started, 4)})

    run("topics_yaml", lambda: _check_topics_yaml(project_root))
    run("project_layout", lambda: _check_dirs(project_root))
    run("python_scientific_stack", _check_python_stack)
    run("output_writable", lambda: _check_output_writable(project_root))
    run("manuscript_config", lambda: _check_file(project_root, "manuscript/config.yaml"))
    run("catalogue_loader", lambda: _check_topics_yaml(project_root))
    run("references_bib", lambda: _check_references_bib(project_root))
    if mode == "full":
        run("gauss_cli", lambda: check_gauss_cli(project_root, require=True))
        run("gauss_state", lambda: _check_gauss_config(project_root))
        run("toolchain_pin", lambda: _check_toolchain_pin(project_root))
        run("lean_cli", lambda: _check_lean_cli(project_root))
        run("lake_cli", lambda: _check_lake(project_root))
        run("lean_workspace", lambda: _check_lean_workspace(project_root))
        run("mathlib_built", lambda: _check_mathlib_built(project_root))
        if not os.environ.get("OPENROUTER_API_KEY") and not os.environ.get("ANTHROPIC_API_KEY"):
            checks.append({"name": "hermes_credentials", "ok": False, "message": "OPENROUTER_API_KEY or ANTHROPIC_API_KEY is required for full mode", "duration_s": 0.0})
        else:
            checks.append({"name": "hermes_credentials", "ok": True, "message": "Hermes credentials configured", "duration_s": 0.0})
    failed = [check for check in checks if not check["ok"]]
    return {"status": "ok" if not failed else "error", "mode": mode, "checks": checks, "failed_count": len(failed)}
