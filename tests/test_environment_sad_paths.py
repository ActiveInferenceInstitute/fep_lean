"""Mock-free tests to trigger sad paths in verification.environment to ensure coverage."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

import verification.environment as ec
from verification.environment import (
    _check_catalogue_import,
    _check_dirs,
    _check_dot_gauss_writable,
    _check_lean_cli,
    _check_lean_workspace,
    _check_manuscript_config,
    _check_mathlib_built,
    _check_output_writable,
    _check_python_numpy_matplotlib,
    _check_references_bib,
    _check_scripts_tests,
    _check_topics_yaml,
    _find_toolchain_lean,
    _lean_subprocess_env,
)

PROJ = Path(__file__).resolve().parent.parent

def test_lean_subprocess_env_mkdir_error(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    unwritable_home = tmp_path / "home"
    unwritable_home.mkdir()
    unwritable_home.chmod(0o555)  # read and execute but not write
    
    monkeypatch.setenv("HOME", str(unwritable_home))
    
    # This will fail to mkdir .elan, caught by OSError and falls back to adding to PATH
    env = _lean_subprocess_env()
    assert "ELAN_HOME" in env
    unwritable_home.chmod(0o755)

def test_find_toolchain_elan_unreadable(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Cover PermissionError branch when ~/.elan/toolchains is unreadable."""
    fake_home = tmp_path / "fake_home"
    fake_home.mkdir()
    # _get_elan_toolchains() reads Path.home() / ".elan" / "toolchains"
    fake_toolchains = fake_home / ".elan" / "toolchains"
    fake_toolchains.mkdir(parents=True)
    fake_toolchains.chmod(0o000)

    monkeypatch.setenv("HOME", str(fake_home))
    monkeypatch.setenv("ELAN_HOME", str(fake_home / ".elan"))
    try:
        assert _find_toolchain_lean(PROJ) is None
    finally:
        # Recursively restore write+read+execute on every child so pytest
        # can clean tmp_path without rm_rf warnings.
        for p in sorted(tmp_path.rglob("*"), reverse=True):
            try:
                p.chmod(0o755)
            except OSError:
                pass

def test_check_lean_cli_not_found(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    fake_proj = tmp_path / "fake_proj"
    fake_proj.mkdir()
    
    monkeypatch.setenv("HOME", str(tmp_path)) # No ~/.elan
    monkeypatch.setenv("PATH", str(tmp_path))
    monkeypatch.setenv("ELAN_HOME", str(tmp_path / "elan_home"))
    
    ok, msg = _check_lean_cli(fake_proj)
    assert ok is True
    assert "not on PATH" in msg

def test_check_lean_cli_exit_error(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    fake_proj = tmp_path / "fake_proj"
    fake_proj.mkdir()
    fake_lean = tmp_path / "lean"
    fake_lean.write_text("#!/bin/sh\necho 'Segmentation fault' >&2\nexit 1\n")
    fake_lean.chmod(0o755)
    
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setenv("PATH", str(tmp_path))
    
    ok, msg = _check_lean_cli(fake_proj)
    assert ok is False
    assert "exit 1" in msg

def test_check_lean_cli_sandbox_proxy(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    fake_proj = tmp_path / "fake_proj"
    fake_proj.mkdir()
    fake_lean = tmp_path / "lean"
    fake_lean.write_text("#!/bin/sh\necho 'settings.toml: operation not permitted' >&2\nexit 1\n")
    fake_lean.chmod(0o755)
    
    monkeypatch.setenv("HOME", str(tmp_path)) # No ~/.elan
    monkeypatch.setenv("PATH", str(tmp_path))
    
    ok, msg = _check_lean_cli(fake_proj)
    assert ok is True
    assert "elan sandbox proxy restriction" in msg

def test_check_mathlib_built_error(tmp_path: Path):
    mathlib = tmp_path / "lean" / ".lake" / "packages" / "mathlib"
    mathlib.mkdir(parents=True)
    # Pass an empty directory
    ok, msg = _check_mathlib_built(tmp_path)
    assert ok is False
    assert "Failed to auto-build" in msg or "lake" in msg

def test_check_dot_gauss_writable_error(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    unwritable = tmp_path / "unwritable"
    unwritable.mkdir()
    unwritable.chmod(0o555)
    
    monkeypatch.setenv("GAUSS_HOME", str(unwritable / ".gauss"))
    ok, msg = _check_dot_gauss_writable(PROJ)
    assert ok is False
    assert "Permission denied" in msg or "Read-only" in msg or "Errno 13" in msg or "not permitted" in msg
    
    unwritable.chmod(0o755)

def test_check_topics_yaml_errors(tmp_path: Path):
    ok, msg = _check_topics_yaml(tmp_path)
    assert ok is False
    assert "missing" in msg

    # Create invalid yaml
    bad_yaml = tmp_path / "config"
    bad_yaml.mkdir()
    (bad_yaml / "topics.yaml").write_text(":")
    ok, msg = _check_topics_yaml(tmp_path)
    assert ok is False
    assert "parse error" in msg

def test_check_dirs_errors(tmp_path: Path):
    ok, msg = _check_dirs(tmp_path)
    assert ok is False
    assert "missing manuscript/" in msg

def test_check_lean_workspace_errors(tmp_path: Path):
    lean_dir = tmp_path / "lean"
    lean_dir.mkdir()
    (lean_dir / "lakefile.toml").write_text("")
    ok, msg = _check_lean_workspace(tmp_path)
    assert ok is False
    assert "FepSketches/: missing" in msg

def test_check_manuscript_config_errors(tmp_path: Path):
    ok, msg = _check_manuscript_config(tmp_path)
    assert ok is False
    assert "missing" in msg

def test_check_scripts_tests_errors(tmp_path: Path):
    (tmp_path / "scripts").mkdir()
    # explicitly leave out 'tests'
    ok, msg = _check_scripts_tests(tmp_path)
    assert ok is False
    assert "missing tests/" in msg

def test_check_references_bib_missing(tmp_path: Path):
    ok, msg = _check_references_bib(tmp_path)
    assert ok is True
    assert "absent" in msg

def test_check_output_writable_errors(tmp_path: Path):
    unwritable = tmp_path / "unwritable"
    unwritable.mkdir()
    unwritable.chmod(0o555)

    ok, msg = _check_output_writable(unwritable)
    assert ok is False
    assert "Permission denied" in msg or "Read-only" in msg or "Errno 13" in msg or "not permitted" in msg

    unwritable.chmod(0o755)


def test_lean_subprocess_env_sets_elan_home(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    """Cover lines 35-40: ELAN_HOME set and directory created."""
    custom = str(tmp_path / "custom_elan")
    monkeypatch.setenv("ELAN_HOME", custom)
    env = _lean_subprocess_env()
    assert env["ELAN_HOME"] == custom
    assert Path(custom).is_dir()


def test_check_mathlib_built_with_oleans(tmp_path: Path):
    """Cover lines 150-157: mathlib dir with .olean files."""
    mathlib = tmp_path / "lean" / ".lake" / "packages" / "mathlib"
    build_lib = mathlib / ".lake" / "build" / "lib"
    build_lib.mkdir(parents=True)
    (build_lib / "Mathlib.olean").touch()
    (build_lib / "sub").mkdir()
    (build_lib / "sub" / "Other.olean").touch()
    ok, msg = _check_mathlib_built(tmp_path)
    assert ok is True
    assert "cache present" in msg


def test_check_python_numpy_matplotlib():
    """Cover lines 234-244: verify real scientific stack imports."""
    ok, msg = _check_python_numpy_matplotlib()
    assert ok is True
    assert "python" in msg.lower() or "numpy" in msg.lower()


def test_check_catalogue_import_real(tmp_path: Path):
    """Cover lines 271-279: catalogue import with real YAML."""
    # Use the actual project's topics.yaml
    ok, msg = _check_catalogue_import(PROJ)
    assert ok is True
    assert "50" in msg


def test_check_catalogue_import_missing_yaml(tmp_path: Path):
    """Cover lines 271-279: catalogue import with missing file."""
    ok, msg = _check_catalogue_import(tmp_path)
    assert ok is False


def test_check_dot_gauss_writable_success(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    """Cover lines 183-185: writable GAUSS_HOME."""
    gauss = tmp_path / ".gauss"
    monkeypatch.setenv("GAUSS_HOME", str(gauss))
    ok, msg = _check_dot_gauss_writable(PROJ)
    assert ok is True
    assert gauss.is_dir()


def test_check_topics_yaml_valid(tmp_path: Path):
    """Cover lines 203-212: valid topics.yaml."""
    cfg = tmp_path / "config"
    cfg.mkdir()
    (cfg / "topics.yaml").write_text("topics:\n  - id: fep-001\n  - id: fep-002\n")
    ok, msg = _check_topics_yaml(tmp_path)
    assert ok is True
    assert "2 topics" in msg


def test_find_toolchain_lean_with_toolchain_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Cover lines 57-65: lean-toolchain file matched to a real toolchain dir."""
    elan = tmp_path / ".elan"
    toolchains = elan / "toolchains"
    tc_dir = toolchains / "leanprover--lean4---v4.14.0" / "bin"
    tc_dir.mkdir(parents=True)
    fake_lean = tc_dir / "lean"
    fake_lean.write_text("#!/bin/sh\necho lean")
    fake_lean.chmod(0o755)

    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setenv("ELAN_HOME", str(elan))

    lean_dir = tmp_path / "lean"
    lean_dir.mkdir()
    (lean_dir / "lean-toolchain").write_text("leanprover/lean4:v4.14.0")

    result = _find_toolchain_lean(lean_dir)
    assert result is not None
    assert "lean" in result
