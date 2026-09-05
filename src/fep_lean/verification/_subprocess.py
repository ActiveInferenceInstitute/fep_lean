"""Process-group-safe subprocess execution for Lean/Lake probes.

``subprocess.run(..., timeout=N)`` kills only the direct child. ``lake env
lean`` spawns ``lean`` (or elan spawns the real toolchain binary) as a
grandchild; on timeout the surviving grandchild holds the pipes open and the
caller blocks in a second ``communicate()`` past the advertised deadline while
the orphan keeps its memory and the ``.olean`` lock region. This module runs
every external probe in its own process group and kills the whole group on
deadline, mirroring ``tests/_support/lean_runner.py``.
"""

from __future__ import annotations

import contextlib
import os
import signal
import subprocess
import threading
from collections.abc import Mapping, Sequence
from typing import Final, Literal, overload

__all__ = ["run_process_group"]

_REAP_TIMEOUT_S: Final = 30.0


@overload
def run_process_group(
    command: Sequence[str],
    *,
    cwd: str | os.PathLike[str],
    env: Mapping[str, str] | None = ...,
    timeout: float | None,
    check: bool = ...,
    capture: Literal[True] = ...,
) -> subprocess.CompletedProcess[str]: ...


@overload
def run_process_group(
    command: Sequence[str],
    *,
    cwd: str | os.PathLike[str],
    env: Mapping[str, str] | None = ...,
    timeout: float | None,
    check: bool = ...,
    capture: Literal[False],
) -> subprocess.CompletedProcess[None]: ...


def run_process_group(
    command: Sequence[str],
    *,
    cwd: str | os.PathLike[str],
    env: Mapping[str, str] | None = None,
    timeout: float | None,
    check: bool = False,
    capture: bool = True,
) -> subprocess.CompletedProcess[str] | subprocess.CompletedProcess[None]:
    """Run ``command`` in its own process group with a group-kill timeout.

    Mirrors ``subprocess.run(..., text=True, timeout=timeout, check=check)``
    for callers that only need the completed process (streams are captured
    when ``capture`` is set and inherited otherwise), except that on deadline
    the entire process group receives ``SIGKILL`` before the
    ``subprocess.TimeoutExpired`` is raised. That keeps wedged
    ``lean``/``elan`` grandchildren from outliving the timeout while
    preserving the caller-visible exception contract.
    """
    process = subprocess.Popen(
        list(command),
        cwd=str(cwd),
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.PIPE if capture else None,
        text=True,
        start_new_session=True,
        env=dict(env) if env is not None else None,
    )
    timed_out = threading.Event()
    deadline_expired = threading.Event()

    def _watchdog() -> None:
        # Backstop for callers that die between deadline and the except block
        # (e.g. a test framework terminating this thread): the group must not
        # survive as orphans holding the lock region. ``timed_out.set()``
        # after a normal exit cancels the kill before the PGID can be
        # recycled.
        if timed_out.wait(timeout):
            return
        deadline_expired.set()
        with contextlib.suppress(ProcessLookupError, PermissionError):
            os.killpg(os.getpgid(process.pid), signal.SIGKILL)

    watchdog = threading.Thread(target=_watchdog, daemon=True)
    watchdog.start()
    try:
        stdout, stderr = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out.set()
        with contextlib.suppress(ProcessLookupError, PermissionError):
            os.killpg(os.getpgid(process.pid), signal.SIGKILL)
        with contextlib.suppress(Exception):
            process.communicate(timeout=_REAP_TIMEOUT_S)
        raise
    finally:
        timed_out.set()
        watchdog.join()
    if deadline_expired.is_set() and timeout is not None:
        raise subprocess.TimeoutExpired(
            list(command), timeout, output=stdout, stderr=stderr
        )
    completed: subprocess.CompletedProcess[str] | subprocess.CompletedProcess[None] = (
        subprocess.CompletedProcess(list(command), process.returncode, stdout, stderr)
    )
    if check and process.returncode:
        raise subprocess.CalledProcessError(process.returncode, list(command))
    return completed
