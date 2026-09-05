"""Observable persistence and subprocess failures preserve their public contracts."""

from __future__ import annotations

import sqlite3
import subprocess
import sys
import threading
import time
from contextlib import closing
from pathlib import Path
from typing import Any

import pytest

from fep_lean.gauss.client import OpenGaussClient, resolve_gauss_home
from fep_lean.verification import _subprocess


def test_failed_artifact_registration_leaves_no_published_file(tmp_path: Path) -> None:
    home = tmp_path / "nested" / "gauss"
    with OpenGaussClient(gauss_home=home) as store:
        session = store.create_session("fep-001", "FEP")
        with closing(sqlite3.connect(home / "fep_lean_state.db")) as db, db:
            db.execute(
                "CREATE TRIGGER reject_artifact BEFORE INSERT ON artifacts "
                "BEGIN SELECT RAISE(FAIL, 'registration unavailable'); END"
            )
        with pytest.raises(sqlite3.IntegrityError, match="registration unavailable"):
            store.write_artifact(session, {"claim": "unregistered"})
        assert list((home / "fep_artifacts").iterdir()) == []
        with closing(sqlite3.connect(home / "fep_lean_state.db")) as db:
            assert db.execute("SELECT count(*) FROM artifacts").fetchone() == (0,)
        assert store.export_session(session)["topic_id"] == "fep-001"


@pytest.mark.parametrize("payload", ["[]", '"plain text"', "null", "42"])
def test_non_object_cache_entries_are_misses(tmp_path: Path, payload: str) -> None:
    with OpenGaussClient(gauss_home=tmp_path / "gauss") as store:
        store.set_cached_hermes("key", "fep-001", "explain", "local", payload, "hash")
        assert store.get_cached_hermes("key") is None
        store.set_cached_hermes(
            "key", "fep-001", "explain", "local", '{"ok":true}', "hash"
        )
        assert store.get_cached_hermes("key") == {"ok": True}


@pytest.mark.parametrize(
    "settings", ["{unterminated", "- unexpected", "gauss: [unexpected]"]
)
def test_malformed_home_configuration_cannot_override_default(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, settings: str
) -> None:
    monkeypatch.delenv("GAUSS_HOME", raising=False)
    config = tmp_path / "config"
    config.mkdir()
    (config / "settings.yaml").write_text(settings)
    assert resolve_gauss_home(tmp_path) is None


def test_unsafe_topic_id_does_not_create_session(tmp_path: Path) -> None:
    with OpenGaussClient(gauss_home=tmp_path / "gauss") as store:
        with pytest.raises(ValueError, match="unsafe characters"):
            store.create_session("../../outside", "FEP")
        assert store.export_all_sessions() == []


def test_communicate_deadline_kills_group_when_watchdog_is_delayed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The main timeout path must work even if its backstop cannot be scheduled."""
    callbacks: list[Any] = []
    kills: list[int] = []
    kill_group = _subprocess.os.killpg

    class DelayedThread:
        def __init__(self, *, target: Any, daemon: bool) -> None:
            callbacks.append(target)

        def start(self) -> None:
            pass

        def join(self) -> None:
            for callback in callbacks:
                callback()

    def record_kill(group: int, sig: int) -> None:
        kills.append(group)
        kill_group(group, sig)

    monkeypatch.setattr(threading, "Thread", DelayedThread)
    monkeypatch.setattr(_subprocess.os, "killpg", record_kill)
    child = "import time; time.sleep(30)"
    parent = (
        "import subprocess,sys,time; "
        f"subprocess.Popen([sys.executable,'-c',{child!r}]); "
        "print('started',flush=True); time.sleep(30)"
    )
    started = time.monotonic()
    with pytest.raises(subprocess.TimeoutExpired) as error:
        _subprocess.run_process_group(
            [sys.executable, "-c", parent], cwd=tmp_path, timeout=0.5
        )
    assert error.value.timeout == 0.5
    assert len(kills) == 1
    assert time.monotonic() - started < 10, "descendants must not retain the pipes"


def test_nonzero_exit_preserves_command_and_return_code(tmp_path: Path) -> None:
    command = [sys.executable, "-c", "raise SystemExit(7)"]
    with pytest.raises(subprocess.CalledProcessError) as error:
        _subprocess.run_process_group(command, cwd=tmp_path, timeout=None, check=True)
    assert error.value.returncode == 7
    assert error.value.cmd == command


def test_uncaptured_unlimited_process_inherits_output(
    tmp_path: Path, capfd: pytest.CaptureFixture[str]
) -> None:
    result = _subprocess.run_process_group(
        [sys.executable, "-c", "print('probe finished')"],
        cwd=tmp_path,
        timeout=None,
        capture=False,
        check=True,
    )
    assert result.returncode == 0
    assert result.stdout is None and result.stderr is None
    assert capfd.readouterr().out == "probe finished\n"
