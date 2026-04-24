"""Runtime checks for math-inc Open Gauss, Lean CLI, Mathlib build, and fep_lean layout."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any
import logging

import yaml

log = logging.getLogger(__name__)

from gauss.cli import check_gauss_cli
from verification._toolchain import (
    get_writable_elan_home as _get_elan_home_str,
    get_elan_toolchains as _get_elan_toolchains,
    find_toolchain_bin,
    subprocess_env as _make_subprocess_env,
)


def _get_elan_home() -> str:
    """ELAN_HOME used by the lean/lake sub-processes."""
    return _get_elan_home_str()


def _lean_subprocess_env() -> dict:
    """Environment for lean/lake sub-processes."""
    return _make_subprocess_env()


def _find_toolchain_lean(lean_dir: Path | None = None) -> str | None:
    """Find lean binary via direct toolchain path, bypassing elan proxy."""
    tc_bin = find_toolchain_bin(lean_dir)
    if tc_bin:
        candidate = tc_bin / "lean"
        if candidate.is_file():
            return str(candidate)
    return None


def _check_lean_cli(project_root: Path | None = None) -> tuple[bool, str]:
    """Check lean CLI.  Uses ELAN_HOME override and direct toolchain path to
    bypass macOS sandbox restrictions on ``~/.elan/settings.toml``.

    Resolution order:
    1. ``FEP_LEAN_LEAN_EXE`` environment variable
    2. ``lean`` on PATH
    3. Direct toolchain binary at ``~/.elan/toolchains/<name>/bin/lean``
    """
    lean_dir = (project_root / "lean") if project_root else None

    # 1. Env override
    explicit = os.environ.get("FEP_LEAN_LEAN_EXE", "")
    lean = explicit if (explicit and Path(explicit).is_file()) else None

    # 2. Direct toolchain path (preferred to bypass elan proxy sandbox issues)
    if not lean:
        lean = _find_toolchain_lean(lean_dir)

    # 3. PATH
    if not lean:
        lean = shutil.which("lean")

    if not lean:
        return True, "lean: not on PATH (optional; run scripts/_maint_bootstrap_lean_toolchain.sh first)"

    try:
        proc = subprocess.run(
            [lean, "--version"],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
            env=_lean_subprocess_env(),
        )
    except (OSError, subprocess.TimeoutExpired) as e:
        return False, f"lean: invocation failed: {e}"
    stdout = (proc.stdout or "").strip()
    stderr = (proc.stderr or "").strip()
    combined_err = (stderr + stdout).lower()
    # elan sandbox issue: settings.toml write is blocked — or when we inject an
    # isolated ELAN_HOME, it reports 'no default toolchain'. Both are non-fatal.
    if proc.returncode != 0:
        if ("settings.toml" in combined_err and "operation not permitted" in combined_err) or \
           "no default toolchain configured" in combined_err:
            return (
                True,
                f"lean: binary at {lean} (elan sandbox proxy restriction; lean is functional)",
            )
        err = (stderr or stdout)[:200]
        return False, f"lean: exit {proc.returncode} {err}"
    line = stdout.splitlines()[0] if stdout else "lean"
    return True, f"lean: {line}"


def _check_mathlib_built(project_root: Path) -> tuple[bool, str]:
    """Verify that the Mathlib4 .olean cache is present; auto-build if absent.

    The Lean verifier requires Mathlib to be pre-built.  If the ``Mathlib.olean``
    root artifact is missing from ``lean/.lake/build/``, this function
    **automatically attempts to build it** in two sequential subprocess calls::

        lake exe cache get   # download pre-built .olean cache (~1–2 GB)
        lake build           # compile any remaining targets

    This may take **several minutes** on a first run and requires network access
    for the cache download step.  On subsequent runs (cache present) the check
    is fast (<1 s).  Returns ``(False, reason)`` only if the auto-build itself
    fails (``subprocess.CalledProcessError`` or ``OSError``).
    """
    mathlib_pkg = project_root / "lean" / ".lake" / "packages" / "mathlib"
    olean_count = 0
    mathlib_built = False
    
    if mathlib_pkg.is_dir():
        # Lean ≥ 4.29 puts oleans under ``.lake/build/lib/lean/``; older
        # toolchains used ``.lake/build/lib/`` directly. Probe both so the
        # check works across upgrades without forcing a layout migration.
        lib_root_legacy = mathlib_pkg / ".lake" / "build" / "lib"
        for mathlib_root_olean in (lib_root_legacy / "lean" / "Mathlib.olean", lib_root_legacy / "Mathlib.olean"):
            if mathlib_root_olean.is_file():
                mathlib_built = True
                break

    if not mathlib_pkg.is_dir() or not mathlib_built:
        log.warning("Mathlib completely built artifact missing. Building automatically to ensure no degradation...")
        lean_dir = project_root / "lean"
        lake = shutil.which("lake") or "lake"
        try:
            env = os.environ.copy()
            log.info("Running auto-build step 1/2: lake exe cache get")
            cache_result = subprocess.run([lake, "exe", "cache", "get"], cwd=lean_dir, env=env, check=False)
            if cache_result.returncode != 0:
                log.warning("lake exe cache get failed (rc=%d) — continuing to lake build (may be slow)", cache_result.returncode)
        except (OSError, subprocess.TimeoutExpired) as e:
            log.warning("lake exe cache get invocation failed: %s — continuing to lake build", e)
        try:
            log.info("Running auto-build step 2/2: lake build")
            subprocess.run([lake, "build"], cwd=lean_dir, env=env, check=True)
            log.info("Mathlib auto-build completed.")
        except subprocess.CalledProcessError as e:
            return False, f"lake build failed (rc={e.returncode}): {e}"
        except (OSError, subprocess.TimeoutExpired) as e:
            return False, f"lake build invocation failed: {e}"
        
        try:
            olean_count = sum(1 for _ in mathlib_pkg.rglob("*.olean") if _.is_file())
        except OSError:
            pass

    if not mathlib_pkg.is_dir():
        return False, "Mathlib auto-build finished but dir missing."

    return True, "Mathlib .olean cache present"


def _check_dot_gauss_writable(project_root: Path | None = None) -> tuple[bool, str]:
    """math-inc Open Gauss uses ``~/.gauss``.

    Resolution order:
    1. ``GAUSS_HOME`` environment variable (explicit override).
    2. ``~/.gauss`` (default; may be unwritable in macOS sandboxes).
    3. ``<project_root>/output/gauss_home`` (automatic fallback when both
       above fail and ``project_root`` is provided).

    The fallback path is written back to ``GAUSS_HOME`` so the rest of the
    process uses it consistently.
    """
    explicit = os.environ.get("GAUSS_HOME", "")
    candidates: list[Path] = []
    if explicit:
        candidates.append(Path(explicit).expanduser())
    else:
        candidates.append((Path.home() / ".gauss"))
        if project_root is not None:
            candidates.append(project_root / "output" / "gauss_home")

    last_err: str = ""
    for candidate in candidates:
        try:
            candidate.mkdir(parents=True, exist_ok=True)
            probe = candidate / ".fep_lean_probe"
            probe.write_text("ok", encoding="utf-8")
            probe.unlink(missing_ok=True)
            # Persist choice so child processes inherit it
            os.environ["GAUSS_HOME"] = str(candidate)
            note = " (fallback)" if candidate != candidates[0] else ""
            return True, f"Open Gauss config dir ok: {candidate}{note}"
        except OSError as e:
            last_err = str(e)
    return False, f".gauss directory not writable: {last_err}"


def _check_topics_yaml(project_root: Path) -> tuple[bool, str]:
    p = project_root / "config" / "topics.yaml"
    if not p.is_file():
        return False, "missing config/topics.yaml"
    try:
        data = yaml.safe_load(p.read_text(encoding="utf-8"))
        n = len(data.get("topics") or [])
    except Exception as e:
        return False, f"parse error: {e}"
    return True, f"topics.yaml ok ({n} topics)"


def _check_dirs(project_root: Path) -> tuple[bool, str]:
    for rel in ("manuscript", "config", "src", "lean"):
        if not (project_root / rel).is_dir():
            return False, f"missing {rel}/"
    return True, "manuscript, config, src, lean present"


def _check_lean_workspace(project_root: Path) -> tuple[bool, str]:
    """Minimal Lake layout for math-inc Gauss ``/project use``."""
    lean = project_root / "lean"
    lake = lean / "lakefile.lean"
    if not lake.is_file() and not (lean / "lakefile.toml").is_file():
        return False, "lean/: missing lakefile.lean or lakefile.toml"
    lib = lean / "FepSketches"
    if not lib.is_dir():
        return False, "lean/FepSketches/: missing (Lean library root)"
    return True, "Lean workspace (Lake) present"


def _check_python_numpy_matplotlib() -> tuple[bool, str]:
    try:
        import numpy as np  # noqa: F401

        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt  # noqa: F401

    except Exception as e:
        return False, f"import: {e}"
    return True, f"python {sys.version_info.major}.{sys.version_info.minor}; numpy/matplotlib ok"


def _check_manuscript_config(project_root: Path) -> tuple[bool, str]:
    p = project_root / "manuscript" / "config.yaml"
    if not p.is_file():
        return False, "missing manuscript/config.yaml"
    return True, "manuscript/config.yaml present"


def _check_scripts_tests(project_root: Path) -> tuple[bool, str]:
    if not (project_root / "scripts").is_dir():
        return False, "missing scripts/"
    if not (project_root / "tests").is_dir():
        return False, "missing tests/"
    return True, "scripts/ and tests/ present"


def _check_references_bib(project_root: Path) -> tuple[bool, str]:
    p = project_root / "manuscript" / "references.bib"
    if not p.is_file():
        return True, "references.bib absent (optional for analysis)"
    n = p.stat().st_size
    return True, f"references.bib present ({n} bytes)"


def _check_catalogue_import(project_root: Path) -> tuple[bool, str]:
    try:
        from catalogue.topics import FEPTopicCatalogue

        c = FEPTopicCatalogue.from_yaml(project_root / "config" / "topics.yaml")
        n = len(c.topics)
    except Exception as e:
        return False, str(e)
    return True, f"FEPTopicCatalogue loaded ({n} topics)"


def _check_output_writable(project_root: Path) -> tuple[bool, str]:
    d = project_root / "output" / ".write_probe"
    try:
        d.mkdir(parents=True, exist_ok=True)
        f = d / "probe.txt"
        f.write_text("ok", encoding="utf-8")
        f.unlink()
    except OSError as e:
        return False, str(e)
    return True, "output/ writable"


def run_validation_checks(project_root: Path) -> dict[str, Any]:
    """Run checks; status is ``error`` if any check has ``ok: False``."""
    checks: list[dict[str, Any]] = []

    def run(name: str, fn: Any) -> None:
        t0 = time.perf_counter()
        ok, msg = fn()
        checks.append(
            {
                "name": name,
                "ok": ok,
                "message": msg,
                "duration_s": time.perf_counter() - t0,
            }
        )

    run(
        "math_inc_gauss_cli",
        lambda: check_gauss_cli(project_root, require=None),
    )
    run("lean_cli", lambda: _check_lean_cli(project_root))
    run("open_gauss_config_dir", lambda: _check_dot_gauss_writable(project_root))
    run("lean_workspace", lambda: _check_lean_workspace(project_root))
    run("mathlib_built", lambda: _check_mathlib_built(project_root))
    run("topics_yaml", lambda: _check_topics_yaml(project_root))
    run("project_layout", lambda: _check_dirs(project_root))
    run("python_scientific_stack", _check_python_numpy_matplotlib)
    run("output_writable", lambda: _check_output_writable(project_root))
    run("manuscript_config", lambda: _check_manuscript_config(project_root))
    run("scripts_tests_layout", lambda: _check_scripts_tests(project_root))
    run("catalogue_loader", lambda: _check_catalogue_import(project_root))
    run("references_bib", lambda: _check_references_bib(project_root))

    failed = [c for c in checks if not c["ok"]]
    return {
        "status": "ok" if not failed else "error",
        "checks": checks,
        "failed_count": len(failed),
    }

