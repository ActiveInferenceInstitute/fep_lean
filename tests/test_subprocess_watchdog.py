"""The timeout backstop kills live probes and cancels after normal completion."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from fep_lean.verification import _subprocess
from tests._support import lean_runner


@pytest.mark.parametrize("owner", [_subprocess, lean_runner])
@pytest.mark.parametrize("deadline_first", [False, True])
def test_watchdog_cancellation_and_deadline(
    owner: Any, deadline_first: bool, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    callbacks: list[Any] = []
    kills: list[tuple[int, int]] = []

    class Thread:
        def __init__(self, *, target: Any, daemon: bool) -> None:
            self.target = target

        def start(self) -> None:
            if deadline_first:
                self.target()
            else:
                callbacks.append(self.target)

        def join(self) -> None:
            for callback in callbacks:
                callback()
            callbacks.clear()

    class Process:
        pid = 456
        returncode = 0

        def communicate(self, **kwargs: Any) -> tuple[str, str]:
            if deadline_first:
                assert kills == [(456, owner.signal.SIGKILL)]
            return "compiled", ""

    monkeypatch.setattr(owner.threading, "Thread", Thread)
    monkeypatch.setattr(owner.subprocess, "Popen", lambda *a, **kw: Process())
    monkeypatch.setattr(owner.os, "getpgid", lambda pid: pid)
    monkeypatch.setattr(owner.os, "killpg", lambda pid, sig: kills.append((pid, sig)))

    def run() -> Any:
        if owner is _subprocess:
            return owner.run_process_group(["fake"], cwd=tmp_path, timeout=0)
        return owner.run_lean_probe(
            tmp_path / "Probe.lean", import_root=tmp_path, cwd=tmp_path, timeout_s=0
        )

    if deadline_first:
        with pytest.raises(owner.subprocess.TimeoutExpired):
            run()
    else:
        assert run().stdout == "compiled"
    for callback in callbacks:
        callback()
    if not deadline_first:
        assert kills == [], "normal completion must cancel the group-kill backstop"


@pytest.mark.parametrize("check", [False, True])
def test_deadline_before_communicate_is_still_a_timeout(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, check: bool
) -> None:
    import subprocess
    import sys
    import time

    start = _subprocess.threading.Thread.start

    def delayed_start(thread: Any) -> None:
        start(thread)
        time.sleep(0.2)

    monkeypatch.setattr(_subprocess.threading.Thread, "start", delayed_start)
    with pytest.raises(subprocess.TimeoutExpired):
        _subprocess.run_process_group(
            [sys.executable, "-c", "import time; time.sleep(2)"],
            cwd=tmp_path,
            timeout=0.05,
            check=check,
        )
