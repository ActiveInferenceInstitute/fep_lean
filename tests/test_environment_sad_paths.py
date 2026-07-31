"""Capability failure cases using real temporary files and executables."""

from pathlib import Path

from verification.environment import (
    _check_catalogue_import,
    _check_dirs,
    _check_lean_cli,
    _check_lean_workspace,
    _check_mathlib_built,
    _check_output_writable,
    _check_python_numpy_matplotlib,
    _check_topics_yaml,
    _find_toolchain_lean,
)

PROJ = Path(__file__).resolve().parent.parent


def test_missing_lean_is_error(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("PATH", str(tmp_path))
    monkeypatch.setenv("ELAN_HOME", str(tmp_path / "elan"))
    ok, message = _check_lean_cli(tmp_path)
    assert not ok
    assert "unavailable" in message


def test_mathlib_check_is_read_only(tmp_path: Path) -> None:
    ok, message = _check_mathlib_built(tmp_path)
    assert not ok
    assert "missing" in message
    assert not (tmp_path / "lean" / ".lake").exists()


def test_missing_catalogue_is_error(tmp_path: Path) -> None:
    ok, message = _check_topics_yaml(tmp_path)
    assert not ok
    assert "cannot read" in message or "missing" in message


def test_malformed_catalogue_is_error(tmp_path: Path) -> None:
    (tmp_path / "config").mkdir()
    (tmp_path / "config" / "topics.yaml").write_text("invalid: [", encoding="utf-8")
    ok, message = _check_topics_yaml(tmp_path)
    assert not ok
    assert message


def test_layout_requires_all_directories(tmp_path: Path) -> None:
    ok, message = _check_dirs(tmp_path)
    assert not ok
    assert "missing" in message


def test_workspace_requires_tracked_aggregate(tmp_path: Path) -> None:
    (tmp_path / "lean").mkdir()
    (tmp_path / "lean" / "lakefile.lean").write_text("package fep", encoding="utf-8")
    ok, message = _check_lean_workspace(tmp_path)
    assert not ok
    assert "fep_all.lean" in message


def test_output_write_probe(tmp_path: Path) -> None:
    ok, message = _check_output_writable(tmp_path)
    assert ok
    assert "writable" in message


def test_scientific_stack_is_present() -> None:
    ok, message = _check_python_numpy_matplotlib()
    assert ok
    assert "Python" in message


def test_catalogue_import_uses_strict_loader() -> None:
    ok, message = _check_catalogue_import(PROJ)
    assert ok
    assert "50" in message


def test_catalogue_import_missing_root(tmp_path: Path) -> None:
    ok, _ = _check_catalogue_import(tmp_path)
    assert not ok


def test_gauss_state_path_is_writable(monkeypatch, tmp_path: Path) -> None:
    from verification.environment import _check_gauss_config
    path = tmp_path / "gauss"
    monkeypatch.setenv("GAUSS_HOME", str(path))
    ok, _ = _check_gauss_config(tmp_path)
    assert ok


def test_find_toolchain_without_pin_returns_none(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("ELAN_HOME", str(tmp_path / "elan"))
    assert _find_toolchain_lean(tmp_path) is None
