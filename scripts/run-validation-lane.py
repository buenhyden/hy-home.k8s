#!/usr/bin/env python3
"""Run contract-approved repository-static validators for a NUL path set."""

from __future__ import annotations

import argparse
import ctypes
import hashlib
import importlib.util
import json
import math
import os
import pwd
import select
import selectors
import signal
import shutil
import stat
import subprocess
import sys
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from typing import Any, BinaryIO, Sequence


LOCAL_LANES = ("affected", "staged", "all-files")
TRUSTED_SEARCH_DIRECTORIES = (
    "/usr/local/sbin",
    "/usr/local/bin",
    "/usr/sbin",
    "/usr/bin",
    "/sbin",
    "/bin",
)
QUALITY_SUCCESS_MARKER = "[PASS] repository quality gates passed"
GITLEAKS_EXECUTABLE_ENV = "HY_HOME_K8S_GITLEAKS_EXECUTABLE"
VALIDATOR_TIMEOUT_SECONDS = 1_200.0
VALIDATOR_STDOUT_LIMIT_BYTES = 4 * 1024 * 1024
VALIDATOR_STDERR_LIMIT_BYTES = 1 * 1024 * 1024
VALIDATOR_CLEANUP_SECONDS = 2.0
VALIDATOR_PIPE_POLL_SECONDS = 0.05
VALIDATOR_READ_CHUNK_BYTES = 64 * 1024
VALIDATOR_OWNED_PROCESS_POLL_SECONDS = 0.01
PR_GET_CHILD_SUBREAPER = 37
PR_SET_CHILD_SUBREAPER = 36
_INTERRUPT_SIGNALS = tuple(
    sig
    for sig in (
        getattr(signal, "SIGINT", None),
        getattr(signal, "SIGTERM", None),
        getattr(signal, "SIGHUP", None),
        getattr(signal, "SIGQUIT", None),
    )
    if sig is not None
)
_PROCESS_OWNERSHIP_LOCK = threading.Lock()
SYSTEM_GITLEAKS_CANDIDATES = tuple(
    Path(directory) / "gitleaks" for directory in TRUSTED_SEARCH_DIRECTORIES
)


@dataclass(frozen=True)
class StreamObservation:
    """Bounded internal bytes plus non-secret metadata for one child pipe."""

    observed_bytes: int
    sha256: str
    retained: bytes = field(repr=False)
    complete: bool = True


@dataclass(frozen=True)
class BoundedCommandResult:
    """Result of one finite, process-group-isolated validator execution."""

    status: str
    returncode: int | None
    stdout: StreamObservation
    stderr: StreamObservation
    cleanup_complete: bool


class _StreamAccumulator:
    def __init__(self, limit_bytes: int):
        self.limit_bytes = limit_bytes
        self.observed_bytes = 0
        self.retained = bytearray()
        self.digest = hashlib.sha256()

    def add(self, payload: bytes) -> bool:
        """Add one bounded read and return whether the stream exceeded its limit."""

        self.observed_bytes += len(payload)
        self.digest.update(payload)
        remaining = max(0, self.limit_bytes - len(self.retained))
        if remaining:
            self.retained.extend(payload[:remaining])
        return self.observed_bytes > self.limit_bytes

    def result(self, *, complete: bool) -> StreamObservation:
        return StreamObservation(
            observed_bytes=self.observed_bytes,
            sha256=self.digest.hexdigest(),
            retained=bytes(self.retained),
            complete=complete,
        )


def load_contract_module():
    module_path = Path(__file__).with_name("validate-affected-surfaces.py")
    spec = importlib.util.spec_from_file_location(
        "affected_surface_contract", module_path
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load affected-surface contract from {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def encoded(value: Any) -> str:
    return json.dumps(value, ensure_ascii=True, separators=(",", ":"), sort_keys=True)


def result_line(
    status: str,
    identifier: str,
    *,
    command: Sequence[str],
    tool: str,
    scope: str,
    limitation: str,
    evidence: str,
) -> str:
    return (
        f"[{status}] {identifier} command={encoded(list(command))} "
        f"tool={encoded(tool)} scope={encoded(scope)} "
        f"limitation={encoded(limitation)} evidence={encoded(evidence)}"
    )


def bounded_metadata(label: str, value: str) -> str:
    payload = value.encode("utf-8", errors="replace")
    return (
        f"{label}_bytes={len(payload)};"
        f"{label}_sha256={hashlib.sha256(payload).hexdigest()}"
    )


def stream_metadata(label: str, stream: StreamObservation) -> str:
    return ";".join(
        (
            f"{label}_bytes={stream.observed_bytes}",
            f"{label}_sha256={stream.sha256}",
            f"{label}_complete={str(stream.complete).lower()}",
        )
    )


def observation(completed: BoundedCommandResult) -> str:
    if completed.status == "completed":
        status = "completed" if completed.returncode == 0 else "failed"
    else:
        status = completed.status
    returncode = "unknown" if completed.returncode is None else str(completed.returncode)
    return ";".join(
        (
            f"status={status}",
            f"rc={returncode}",
            stream_metadata("stdout", completed.stdout),
            stream_metadata("stderr", completed.stderr),
            f"cleanup_complete={str(completed.cleanup_complete).lower()}",
        )
    )


def trusted_search_path() -> str:
    """Build one fixed absolute PATH without caller-controlled search entries."""

    directories: list[str] = []
    for raw_path in TRUSTED_SEARCH_DIRECTORIES:
        try:
            resolved = Path(raw_path).resolve(strict=True)
        except OSError:
            continue
        value = resolved.as_posix()
        if resolved.is_dir() and value not in directories:
            directories.append(value)
    return os.pathsep.join(directories)


def validate_gitleaks_candidate(
    candidate: Path,
    root: Path,
    *,
    owner_uid: int,
    required_chain: Sequence[Path],
) -> bool:
    """Validate one exact non-search-path Gitleaks candidate without dereference."""

    candidate = Path(candidate)
    root = Path(root)
    if (
        not candidate.is_absolute()
        or candidate.name != "gitleaks"
        or not required_chain
        or candidate.parent != required_chain[-1]
        or candidate.is_relative_to(root)
        or candidate.is_relative_to(Path("/tmp"))
    ):
        return False

    try:
        effective_uid = os.geteuid()
        effective_groups = frozenset((*os.getgroups(), os.getegid()))
    except OSError:
        return False

    def can_execute(metadata: os.stat_result, *, directory: bool) -> bool:
        if effective_uid == 0:
            return directory or bool(metadata.st_mode & 0o111)
        if metadata.st_uid == effective_uid:
            execute_bit = stat.S_IXUSR
        elif metadata.st_gid in effective_groups:
            execute_bit = stat.S_IXGRP
        else:
            execute_bit = stat.S_IXOTH
        return bool(metadata.st_mode & execute_bit)

    for directory in required_chain:
        try:
            metadata = os.lstat(directory)
        except OSError:
            return False
        if (
            stat.S_ISLNK(metadata.st_mode)
            or not stat.S_ISDIR(metadata.st_mode)
            or metadata.st_uid != owner_uid
            or metadata.st_mode & 0o022
            or not can_execute(metadata, directory=True)
        ):
            return False

    try:
        metadata = os.lstat(candidate)
    except OSError:
        return False
    return (
        not stat.S_ISLNK(metadata.st_mode)
        and stat.S_ISREG(metadata.st_mode)
        and metadata.st_uid == owner_uid
        and not metadata.st_mode & 0o022
        and can_execute(metadata, directory=False)
    )


def secure_gitleaks_executable(root: Path) -> str | None:
    """Return the first exact secure system or passwd-home Gitleaks candidate."""

    for candidate in SYSTEM_GITLEAKS_CANDIDATES:
        if validate_gitleaks_candidate(
            candidate,
            root,
            owner_uid=0,
            required_chain=(candidate.parent,),
        ):
            return candidate.as_posix()

    try:
        account = pwd.getpwuid(os.geteuid())
    except (KeyError, OSError):
        return None
    home = Path(account.pw_dir)
    candidate = home / ".local" / "bin" / "gitleaks"
    if validate_gitleaks_candidate(
        candidate,
        root,
        owner_uid=account.pw_uid,
        required_chain=(home, home / ".local", home / ".local" / "bin"),
    ):
        return candidate.as_posix()
    return None


def closed_subprocess_environment() -> dict[str, str]:
    """Return the complete validator environment; ambient startup state is absent."""

    return {
        "GIT_TERMINAL_PROMPT": "0",
        "HOME": "/nonexistent",
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "NO_COLOR": "1",
        "PATH": trusted_search_path(),
        "PYTHONNOUSERSITE": "1",
        "TZ": "UTC",
    }


def exact_success_marker_count(stdout: str | bytes, marker: str) -> int:
    """Count exact complete success-marker lines without exposing child output."""

    if isinstance(stdout, bytes):
        try:
            stdout = stdout.decode("utf-8", errors="strict")
        except UnicodeDecodeError:
            return 0
    return sum(line == marker for line in stdout.splitlines())


def _close_pipe(pipe: BinaryIO | None) -> bool:
    """Close one pipe without letting an ordinary close failure escape."""

    if pipe is None:
        return True
    try:
        pipe.close()
    except Exception:
        return False
    return True


def _close_selector(selector: selectors.BaseSelector) -> tuple[bool, BaseException | None]:
    """Close a selector after child cleanup and defer asynchronous exceptions."""

    try:
        selector.close()
    except Exception:
        return False, None
    except BaseException as exc:
        return False, exc
    return True, None


def _leader_exited_without_reap(process: subprocess.Popen[bytes]) -> bool:
    """Observe direct-child exit while retaining its PID/process-group identity."""

    flags = os.WEXITED | os.WNOHANG | os.WNOWAIT
    return os.waitid(os.P_PID, process.pid, flags) is not None


def _recorded_returncode(process: subprocess.Popen[bytes]) -> int | None:
    """Read only Popen's recorded state; polling here would reap the leader."""

    return getattr(process, "returncode", None)


def _remaining_seconds(deadline: float) -> float:
    return max(0.0, deadline - time.monotonic())


def _status_ppid(pid: int) -> int | None:
    try:
        with open(Path("/proc") / str(pid) / "status", encoding="utf-8") as handle:
            for line in handle:
                if line.startswith("PPid:"):
                    return int(line.split()[1])
    except (FileNotFoundError, ProcessLookupError, PermissionError, OSError, ValueError):
        return None
    return None


def _direct_child_pids() -> set[int]:
    parent_pid = os.getpid()
    children: set[int] = set()
    try:
        entries = os.scandir("/proc")
    except OSError:
        return children
    with entries:
        for entry in entries:
            if not entry.name.isdecimal():
                continue
            pid = int(entry.name)
            if _status_ppid(pid) == parent_pid:
                children.add(pid)
    return children


def _process_children_map() -> dict[int, set[int]]:
    children: dict[int, set[int]] = {}
    try:
        entries = os.scandir("/proc")
    except OSError:
        return children
    with entries:
        for entry in entries:
            if not entry.name.isdecimal():
                continue
            pid = int(entry.name)
            ppid = _status_ppid(pid)
            if ppid is not None:
                children.setdefault(ppid, set()).add(pid)
    return children


def _discover_owned_pids(leader_pid: int, baseline_direct_children: set[int]) -> set[int]:
    """Find the leader, its descendants, and subreaper-adopted owned children."""

    children = _process_children_map()
    roots = {leader_pid}
    roots.update(_direct_child_pids() - baseline_direct_children)
    owned: set[int] = set()
    stack = list(roots)
    while stack:
        pid = stack.pop()
        if pid <= 0 or pid in owned:
            continue
        if not (Path("/proc") / str(pid)).exists():
            continue
        owned.add(pid)
        stack.extend(children.get(pid, ()))
    return owned


def _process_group_id(pid: int) -> int | None:
    try:
        return os.getpgid(pid)
    except (ProcessLookupError, PermissionError, OSError):
        return None


def _process_group_absent(process_group_id: int) -> bool:
    """Observe group absence without signaling a possibly recycled identity."""

    try:
        entries = os.scandir("/proc")
    except OSError:
        return False
    with entries:
        for entry in entries:
            if not entry.name.isdecimal():
                continue
            if _process_group_id(int(entry.name)) == process_group_id:
                return False
    return True


def _has_cross_session_owned_descendant(
    leader_pid: int, baseline_direct_children: set[int]
) -> bool:
    owned = _discover_owned_pids(leader_pid, baseline_direct_children)
    for pid in owned - {leader_pid}:
        if _process_group_id(pid) not in (None, leader_pid):
            return True
    return False


def _close_pidfds(pidfds: dict[int, int]) -> None:
    for fd in pidfds.values():
        try:
            os.close(fd)
        except OSError:
            pass
    pidfds.clear()


def _signal_pidfd(fd: int, sig: signal.Signals) -> bool:
    """Signal one stable process identity; numeric-PID fallback is forbidden."""

    sender = getattr(signal, "pidfd_send_signal", None)
    if sender is None:
        return False
    try:
        sender(fd, sig)
    except ProcessLookupError:
        return True
    except OSError:
        return False
    return True


def _pidfds_exited(pidfds: dict[int, int]) -> bool:
    if not pidfds:
        return True
    try:
        readable, _writable, _exceptional = select.select(
            list(pidfds.values()), (), (), 0.0
        )
    except (OSError, ValueError):
        return False
    return len(readable) == len(pidfds)


def _reap_direct_children(candidate_pids: set[int]) -> bool:
    complete = True
    for pid in candidate_pids:
        try:
            while True:
                reaped, _status = os.waitpid(pid, os.WNOHANG)
                if reaped == 0:
                    break
                if reaped == pid:
                    break
        except ChildProcessError:
            continue
        except OSError:
            complete = False
    return complete


def _get_subreaper_state() -> int | None:
    try:
        state = ctypes.c_int()
        result = ctypes.CDLL(None, use_errno=True).prctl(
            PR_GET_CHILD_SUBREAPER, ctypes.byref(state), 0, 0, 0
        )
    except (AttributeError, OSError):
        return None
    if result != 0:
        return None
    return int(state.value)


def _set_subreaper_state(enabled: int) -> bool:
    try:
        result = ctypes.CDLL(None, use_errno=True).prctl(
            PR_SET_CHILD_SUBREAPER, int(bool(enabled)), 0, 0, 0
        )
    except (AttributeError, OSError):
        return False
    return result == 0


def _block_interrupt_signals() -> set[signal.Signals] | None:
    masker = getattr(signal, "pthread_sigmask", None)
    if masker is None or not _INTERRUPT_SIGNALS:
        return None
    return masker(signal.SIG_BLOCK, _INTERRUPT_SIGNALS)


def _restore_interrupt_signals(previous_mask: set[signal.Signals] | None) -> None:
    masker = getattr(signal, "pthread_sigmask", None)
    if masker is None or previous_mask is None:
        return
    masker(signal.SIG_SETMASK, previous_mask)


def _ownership_primitives_available() -> bool:
    return (
        sys.platform.startswith("linux")
        and Path("/proc/self/fd").is_dir()
        and callable(getattr(os, "pidfd_open", None))
        and callable(getattr(signal, "pidfd_send_signal", None))
        and callable(getattr(signal, "pthread_sigmask", None))
        and _get_subreaper_state() is not None
    )


def _close_fd(fd: int | None) -> bool:
    if fd is None:
        return True
    try:
        os.close(fd)
    except OSError:
        return False
    return True


def cleanup_process_group(
    process: subprocess.Popen[bytes],
    cleanup_seconds: float,
    *,
    deadline: float | None = None,
    baseline_direct_children: set[int] | None = None,
) -> bool:
    """Terminate and prove absence of one owned process tree.

    Retries reuse the caller-provided absolute deadline.  The original numeric
    process group is signaled only before direct-leader reap; descendants that
    escape the session are held by pidfds and reaped through the subreaper.
    """

    cleanup_complete = True
    deferred: BaseException | None = None
    baseline_direct_children = set(baseline_direct_children or ())
    if deadline is None:
        try:
            deadline = time.monotonic() + max(0.0, cleanup_seconds)
        except BaseException as exc:
            deadline = 0.0
            cleanup_complete = False
            deferred = exc

    previous_mask: set[signal.Signals] | None = None
    pidfds: dict[int, int] = {}
    leader_pidfd = getattr(process, "_validation_leader_pidfd", None)
    if isinstance(leader_pidfd, int):
        pidfds[process.pid] = leader_pidfd
        process._validation_leader_pidfd = None
    try:
        try:
            previous_mask = _block_interrupt_signals()
        except BaseException as exc:
            cleanup_complete = False
            deferred = deferred or exc

        for pipe in (process.stdout, process.stderr):
            while pipe is not None and not getattr(pipe, "closed", False):
                try:
                    if not _close_pipe(pipe):
                        cleanup_complete = False
                    break
                except BaseException as exc:
                    cleanup_complete = False
                    deferred = deferred or exc
                    if _remaining_seconds(deadline) <= 0:
                        break

        group_signal_effective = False
        group_signal_failed = False
        while _remaining_seconds(deadline) > 0:
            owned = _discover_owned_pids(process.pid, baseline_direct_children)
            for pid in owned - set(pidfds):
                try:
                    pidfds[pid] = os.pidfd_open(pid, 0)
                except ProcessLookupError:
                    continue
                except (AttributeError, OSError):
                    cleanup_complete = False

            leader_reaped = _recorded_returncode(process) is not None
            if not leader_reaped and not group_signal_effective:
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                    group_signal_effective = True
                except ProcessLookupError:
                    group_signal_effective = _process_group_absent(process.pid)
                except Exception:
                    cleanup_complete = False
                    group_signal_failed = True
                except BaseException as exc:
                    cleanup_complete = False
                    deferred = deferred or exc
                    continue

            for pid, pidfd in tuple(pidfds.items()):
                if pid != process.pid and not _signal_pidfd(pidfd, signal.SIGKILL):
                    cleanup_complete = False

            if (
                _recorded_returncode(process) is None
                and (group_signal_effective or group_signal_failed)
            ):
                if group_signal_failed:
                    leader_pidfd = pidfds.get(process.pid)
                    if leader_pidfd is not None and not _signal_pidfd(
                        leader_pidfd, signal.SIGKILL
                    ):
                        cleanup_complete = False
                try:
                    process.wait(
                        timeout=min(
                            VALIDATOR_OWNED_PROCESS_POLL_SECONDS,
                            _remaining_seconds(deadline),
                        )
                    )
                except subprocess.TimeoutExpired:
                    pass
                except InterruptedError as exc:
                    cleanup_complete = False
                    deferred = deferred or exc
                    continue
                except Exception:
                    cleanup_complete = False
                except BaseException as exc:
                    cleanup_complete = False
                    deferred = deferred or exc
                    continue

            try:
                if not _reap_direct_children(set(pidfds) - {process.pid}):
                    cleanup_complete = False
            except BaseException as exc:
                cleanup_complete = False
                deferred = deferred or exc
                continue

            owned = _discover_owned_pids(process.pid, baseline_direct_children)
            if (
                _recorded_returncode(process) is not None
                and _process_group_absent(process.pid)
                and not owned
                and _pidfds_exited(pidfds)
            ):
                _close_pidfds(pidfds)
                if deferred is not None:
                    raise deferred
                return cleanup_complete and not group_signal_failed

            try:
                time.sleep(
                    min(
                        VALIDATOR_OWNED_PROCESS_POLL_SECONDS,
                        _remaining_seconds(deadline),
                    )
                )
            except InterruptedError as exc:
                cleanup_complete = False
                deferred = deferred or exc
            except BaseException as exc:
                cleanup_complete = False
                deferred = deferred or exc

        if _recorded_returncode(process) is None:
            try:
                process.wait(timeout=0)
            except Exception:
                cleanup_complete = False
            except BaseException as exc:
                cleanup_complete = False
                deferred = deferred or exc
        if deferred is not None:
            raise deferred
        return False
    finally:
        _close_pidfds(pidfds)
        _restore_interrupt_signals(previous_mask)


def cleanup_spawn_failure(
    *,
    deadline: float,
    baseline_direct_children: set[int],
) -> bool:
    """Kill and reap children created before a Popen handle was acquired."""

    cleanup_complete = True
    pidfds: dict[int, int] = {}
    try:
        while _remaining_seconds(deadline) > 0:
            owned = _discover_owned_pids(0, baseline_direct_children)
            for pid in owned - set(pidfds):
                try:
                    pidfds[pid] = os.pidfd_open(pid, 0)
                except ProcessLookupError:
                    continue
                except (AttributeError, OSError):
                    cleanup_complete = False
            for fd in tuple(pidfds.values()):
                if not _signal_pidfd(fd, signal.SIGKILL):
                    cleanup_complete = False
            try:
                if not _reap_direct_children(set(pidfds)):
                    cleanup_complete = False
            except BaseException:
                cleanup_complete = False
                continue
            owned = _discover_owned_pids(0, baseline_direct_children)
            if not owned and _pidfds_exited(pidfds):
                return cleanup_complete
            try:
                time.sleep(
                    min(
                        VALIDATOR_OWNED_PROCESS_POLL_SECONDS,
                        _remaining_seconds(deadline),
                    )
                )
            except BaseException:
                cleanup_complete = False
    finally:
        _close_pidfds(pidfds)
    return False


def _run_bounded_command_locked(
    argv: Sequence[str],
    *,
    cwd: Path,
    env: dict[str, str],
    timeout_seconds: float = VALIDATOR_TIMEOUT_SECONDS,
    stdout_limit_bytes: int = VALIDATOR_STDOUT_LIMIT_BYTES,
    stderr_limit_bytes: int = VALIDATOR_STDERR_LIMIT_BYTES,
    cleanup_seconds: float = VALIDATOR_CLEANUP_SECONDS,
) -> BoundedCommandResult:
    """Run one validator with finite execution, pipe, and cleanup resources."""

    if (
        not math.isfinite(timeout_seconds)
        or timeout_seconds <= 0
        or stdout_limit_bytes < 0
        or stderr_limit_bytes < 0
        or not math.isfinite(cleanup_seconds)
        or cleanup_seconds < 0
    ):
        raise ValueError("validator execution limits must be finite and non-negative")

    accumulators = {
        "stdout": _StreamAccumulator(stdout_limit_bytes),
        "stderr": _StreamAccumulator(stderr_limit_bytes),
    }
    stream_complete = {"stdout": False, "stderr": False}
    try:
        selector = selectors.DefaultSelector()
    except OSError:
        return BoundedCommandResult(
            status="pipe_failure",
            returncode=None,
            stdout=accumulators["stdout"].result(complete=False),
            stderr=accumulators["stderr"].result(complete=False),
            cleanup_complete=True,
        )
    if not _ownership_primitives_available():
        selector_ok, deferred = _close_selector(selector)
        if deferred is not None:
            raise deferred
        return BoundedCommandResult(
            status="ownership_unavailable",
            returncode=None,
            stdout=accumulators["stdout"].result(complete=False),
            stderr=accumulators["stderr"].result(complete=False),
            cleanup_complete=selector_ok,
        )

    process: subprocess.Popen[bytes] | None = None
    baseline_direct_children = _direct_child_pids()
    subreaper_previous = _get_subreaper_state()
    subreaper_enabled = bool(
        subreaper_previous is not None and _set_subreaper_state(1)
    )
    stdout_read: BinaryIO | None = None
    stderr_read: BinaryIO | None = None
    stdout_read_fd: int | None = None
    stderr_read_fd: int | None = None
    stdout_write_fd: int | None = None
    stderr_write_fd: int | None = None
    cleanup_deadline: float | None = None
    status = "start_failure"
    cleanup_complete = True
    try:
        if not subreaper_enabled:
            return BoundedCommandResult(
                status="ownership_unavailable",
                returncode=None,
                stdout=accumulators["stdout"].result(complete=False),
                stderr=accumulators["stderr"].result(complete=False),
                cleanup_complete=True,
            )

        spawn_exception: BaseException | None = None
        try:
            previous_mask = _block_interrupt_signals()
            try:
                stdout_read_fd, stdout_write_fd = os.pipe2(os.O_CLOEXEC)
                stdout_read = os.fdopen(stdout_read_fd, "rb", buffering=0)
                stdout_read_fd = None
                stderr_read_fd, stderr_write_fd = os.pipe2(os.O_CLOEXEC)
                stderr_read = os.fdopen(stderr_read_fd, "rb", buffering=0)
                stderr_read_fd = None
                process = subprocess.Popen(
                    list(argv),
                    cwd=cwd,
                    stdin=subprocess.DEVNULL,
                    stdout=stdout_write_fd,
                    stderr=stderr_write_fd,
                    shell=False,
                    env=env,
                    text=False,
                    bufsize=0,
                    close_fds=True,
                    start_new_session=True,
                )
                _close_fd(stdout_write_fd)
                stdout_write_fd = None
                _close_fd(stderr_write_fd)
                stderr_write_fd = None
                process.stdout = stdout_read
                process.stderr = stderr_read
                # Pin the leader identity before unmasking.  Cleanup assumes
                # ownership of this descriptor and closes it exactly once.
                process._validation_leader_pidfd = os.pidfd_open(process.pid, 0)
            finally:
                _restore_interrupt_signals(previous_mask)
        except BaseException as exc:
            spawn_exception = exc

        if spawn_exception is not None and process is None:
            _close_pipe(stdout_read)
            _close_pipe(stderr_read)
            _close_fd(stdout_read_fd)
            stdout_read_fd = None
            _close_fd(stderr_read_fd)
            stderr_read_fd = None
            _close_fd(stdout_write_fd)
            stdout_write_fd = None
            _close_fd(stderr_write_fd)
            stderr_write_fd = None
            cleanup_deadline = time.monotonic() + max(0.0, cleanup_seconds)
            spawn_cleanup = cleanup_spawn_failure(
                deadline=cleanup_deadline,
                baseline_direct_children=baseline_direct_children,
            )
            selector_ok, deferred = _close_selector(selector)
            if deferred is not None:
                raise deferred
            if not isinstance(spawn_exception, OSError):
                raise spawn_exception
            return BoundedCommandResult(
                status="start_failure" if selector_ok else "pipe_failure",
                returncode=None,
                stdout=accumulators["stdout"].result(complete=False),
                stderr=accumulators["stderr"].result(complete=False),
                cleanup_complete=selector_ok and spawn_cleanup,
            )
        if spawn_exception is not None:
            raise spawn_exception

        # The ownership bracket is already active before this first
        # interruptible post-spawn operation.
        execution_deadline = time.monotonic() + timeout_seconds
        status = "collecting"
        for name, pipe in (("stdout", process.stdout), ("stderr", process.stderr)):
            if pipe is None:
                status = "pipe_failure"
                break
            try:
                selector.register(pipe, selectors.EVENT_READ, name)
            except (OSError, ValueError):
                status = "pipe_failure"
                break

        while status == "collecting":
            try:
                active_streams = bool(selector.get_map())
            except (OSError, ValueError):
                status = "pipe_failure"
                break
            if not active_streams:
                break

            remaining = execution_deadline - time.monotonic()
            if remaining <= 0:
                status = "timeout"
                break
            try:
                events = selector.select(
                    min(VALIDATOR_PIPE_POLL_SECONDS, remaining)
                )
            except InterruptedError:
                status = "collection_interrupted"
                break
            except (OSError, ValueError):
                status = "pipe_failure"
                break

            if not events:
                try:
                    leader_exited = _leader_exited_without_reap(process)
                except InterruptedError:
                    status = "collection_interrupted"
                    break
                except (ChildProcessError, OSError, ValueError):
                    status = "pipe_failure"
                    break
                if leader_exited:
                    status = "descendant_pipe_hold"
                    break
                continue

            for key, _mask in events:
                name = key.data
                pipe = key.fileobj
                accumulator = accumulators[name]
                unread_capacity = max(
                    1, accumulator.limit_bytes - accumulator.observed_bytes + 1
                )
                read_size = min(VALIDATOR_READ_CHUNK_BYTES, unread_capacity)
                try:
                    payload = os.read(pipe.fileno(), read_size)
                except BlockingIOError:
                    continue
                except InterruptedError:
                    status = "collection_interrupted"
                    break
                except (OSError, ValueError):
                    status = "pipe_failure"
                    break

                if not payload:
                    try:
                        selector.unregister(pipe)
                    except (KeyError, OSError, ValueError):
                        status = "pipe_failure"
                        break
                    if not _close_pipe(pipe):
                        status = "pipe_failure"
                        break
                    stream_complete[name] = True
                    continue

                if accumulator.add(payload):
                    status = f"{name}_overflow"
                    break

        if status == "collecting":
            while status == "collecting":
                remaining = execution_deadline - time.monotonic()
                if remaining <= 0:
                    status = "timeout"
                    break
                try:
                    leader_exited = _leader_exited_without_reap(process)
                except InterruptedError:
                    status = "collection_interrupted"
                    break
                except (ChildProcessError, OSError, ValueError):
                    status = "pipe_failure"
                    break
                if leader_exited:
                    status = "ready_for_completion"
                    break
                try:
                    time.sleep(min(VALIDATOR_PIPE_POLL_SECONDS, remaining))
                except InterruptedError:
                    status = "collection_interrupted"
                    break

        # Every path, including normal leader exit, closes the owned process
        # group while the unreaped leader still pins its numeric identity.
        cross_session_descendant = _has_cross_session_owned_descendant(
            process.pid, baseline_direct_children
        )
        cleanup_deadline = time.monotonic() + max(0.0, cleanup_seconds)
        cleanup_complete = cleanup_process_group(
            process,
            cleanup_seconds,
            deadline=cleanup_deadline,
            baseline_direct_children=baseline_direct_children,
        )
        if status == "ready_for_completion":
            if cleanup_complete and not cross_session_descendant:
                status = "completed"
            elif cleanup_complete:
                status = "descendant_cleanup"
            else:
                status = "cleanup_failure"
        elif status == "descendant_pipe_hold":
            # A pipe holder can deliberately escape the owned group.  The
            # command is already failing, and cleanup completeness cannot be
            # promoted solely from the original-group kill.
            cleanup_complete = False

        selector_ok, deferred = _close_selector(selector)
        if not selector_ok:
            cleanup_complete = False
            status = "pipe_failure"
        if deferred is not None:
            raise deferred
    except BaseException:
        if process is not None:
            try:
                if cleanup_deadline is None:
                    cleanup_deadline = time.monotonic() + max(
                        0.0, cleanup_seconds
                    )
                cleanup_process_group(
                    process,
                    cleanup_seconds,
                    deadline=cleanup_deadline,
                    baseline_direct_children=baseline_direct_children,
                )
            except BaseException:
                pass
        _close_selector(selector)
        raise
    finally:
        _close_selector(selector)
        if process is not None:
            for pipe in (process.stdout, process.stderr):
                try:
                    _close_pipe(pipe)
                except BaseException:
                    pass
            leader_pidfd = getattr(process, "_validation_leader_pidfd", None)
            if isinstance(leader_pidfd, int):
                _close_fd(leader_pidfd)
                process._validation_leader_pidfd = None
        _close_pipe(stdout_read)
        _close_pipe(stderr_read)
        _close_fd(stdout_read_fd)
        _close_fd(stderr_read_fd)
        _close_fd(stdout_write_fd)
        _close_fd(stderr_write_fd)
        if subreaper_previous is not None and subreaper_enabled:
            _set_subreaper_state(subreaper_previous)

    return BoundedCommandResult(
        status=status,
        returncode=process.returncode,
        stdout=accumulators["stdout"].result(
            complete=stream_complete["stdout"]
        ),
        stderr=accumulators["stderr"].result(
            complete=stream_complete["stderr"]
        ),
        cleanup_complete=cleanup_complete,
    )


def run_bounded_command(
    argv: Sequence[str],
    *,
    cwd: Path,
    env: dict[str, str],
    timeout_seconds: float = VALIDATOR_TIMEOUT_SECONDS,
    stdout_limit_bytes: int = VALIDATOR_STDOUT_LIMIT_BYTES,
    stderr_limit_bytes: int = VALIDATOR_STDERR_LIMIT_BYTES,
    cleanup_seconds: float = VALIDATOR_CLEANUP_SECONDS,
) -> BoundedCommandResult:
    """Serialize the process-wide subreaper ownership boundary."""

    with _PROCESS_OWNERSHIP_LOCK:
        return _run_bounded_command_locked(
            argv,
            cwd=cwd,
            env=env,
            timeout_seconds=timeout_seconds,
            stdout_limit_bytes=stdout_limit_bytes,
            stderr_limit_bytes=stderr_limit_bytes,
            cleanup_seconds=cleanup_seconds,
        )


def validator_argv(
    root: Path,
    lane: str,
    paths: Sequence[str],
    validator: dict[str, Any],
    contract: dict[str, Any],
    contract_module: Any,
) -> list[str]:
    argv = list(validator["argv"])
    if (
        lane not in ("affected", "staged")
        or validator.get("pathInput") != "include-existing-markdown"
    ):
        return argv

    include_candidates = list(paths)
    archive_form = "docs/99.templates/templates/common/archive-record.template.md"
    if (root / archive_form).is_file() and archive_form not in include_candidates:
        include_candidates.append(archive_form)

    for raw_path in include_candidates:
        if not raw_path.endswith(".md"):
            continue
        surface = contract_module.classify_path(contract, raw_path)
        if validator["id"] not in surface["validators"]:
            continue
        target = root.joinpath(*PurePosixPath(raw_path).parts)
        if target.exists() or target.is_symlink():
            argv.extend(("--include-path", raw_path))
    return argv


def run_selected(
    root: Path,
    lane: str,
    paths: Sequence[str],
    contract: dict[str, Any],
    contract_module: Any,
) -> int:
    scope = f"{lane}:paths={len(paths)}"
    if not paths:
        print(
            result_line(
                "SKIP",
                "validation-lane",
                command=(),
                tool="none",
                scope=scope,
                limitation="no paths supplied",
                evidence="repo-static",
            )
        )
        return 0

    selected = contract_module.select_paths(contract, paths, lane, root)
    validators = {row["id"]: row for row in contract["validators"]}
    if not selected["validators"]:
        print(
            result_line(
                "SKIP",
                "validation-lane",
                command=(),
                tool="none",
                scope=scope,
                limitation="matched surfaces select no local validators",
                evidence="repo-static",
            )
        )
        return 0

    failed = False
    subprocess_environment = closed_subprocess_environment()
    gitleaks_executable = secure_gitleaks_executable(root)
    if gitleaks_executable is not None:
        subprocess_environment[GITLEAKS_EXECUTABLE_ENV] = gitleaks_executable
    for identifier in selected["validators"]:
        validator = validators[identifier]
        argv = validator_argv(root, lane, paths, validator, contract, contract_module)
        tool_token = argv[0]
        evidence = validator["evidenceLane"]
        if evidence == "remote/live":
            print(
                result_line(
                    "DEFER",
                    identifier,
                    command=argv,
                    tool=tool_token,
                    scope=scope,
                    limitation="remote/live commands are never executed by the local runner",
                    evidence=evidence,
                )
            )
            continue

        resolved_tool = shutil.which(tool_token, path=subprocess_environment["PATH"])
        if resolved_tool is None:
            fallback = validator["fallback"]
            if validator["optional"]:
                print(
                    result_line(
                        "SKIP",
                        identifier,
                        command=argv,
                        tool=tool_token,
                        scope=scope,
                        limitation="optional tool unavailable",
                        evidence=evidence,
                    )
                )
                print(
                    result_line(
                        fallback["status"],
                        f"{identifier}-fallback",
                        command=(),
                        tool="none",
                        scope=scope,
                        limitation=fallback["reason"],
                        evidence=evidence,
                    )
                )
                continue
            print(
                result_line(
                    "FAIL",
                    identifier,
                    command=argv,
                    tool=tool_token,
                    scope=scope,
                    limitation=f"required tool unavailable; fallback: {fallback['reason']}",
                    evidence=evidence,
                )
            )
            failed = True
            continue

        tool = Path(resolved_tool).resolve(strict=True).as_posix()
        argv[0] = tool

        completed = run_bounded_command(
            argv,
            cwd=root,
            env=subprocess_environment,
        )
        marker = QUALITY_SUCCESS_MARKER if identifier == "repository-quality" else None
        marker_count = (
            exact_success_marker_count(completed.stdout.retained, marker)
            if marker is not None and completed.status == "completed"
            else None
        )
        passed = (
            completed.status == "completed"
            and completed.returncode == 0
            and completed.cleanup_complete
            and (marker_count == 1 if marker is not None else True)
        )
        status = "PASS" if passed else "FAIL"
        limitation = observation(completed)
        if marker is not None:
            rendered_marker_count = (
                "unavailable" if marker_count is None else str(marker_count)
            )
            limitation += f";success_marker_count={rendered_marker_count}"
        print(
            result_line(
                status,
                identifier,
                command=argv,
                tool=tool,
                scope=scope,
                limitation=limitation,
                evidence=evidence,
            )
        )
        failed = failed or not passed
    return 1 if failed else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--lane", choices=LOCAL_LANES, required=True)
    parser.add_argument("--paths-file", type=Path, required=True)
    parser.add_argument("--delimiter", choices=("nul",), required=True)
    args = parser.parse_args()

    contract_module = load_contract_module()
    root = args.root.resolve()
    scope = f"{args.lane}:paths=unknown"
    try:
        contract = contract_module.validate_contract(root)
        paths = contract_module.read_nul_paths(args.paths_file)
        return run_selected(root, args.lane, paths, contract, contract_module)
    except contract_module.ContractError as exc:
        detail_metadata = bounded_metadata("detail", exc.detail)
        print(
            result_line(
                "FAIL",
                "validation-lane",
                command=(),
                tool="none",
                scope=scope,
                limitation=f"contract_error={exc.code};{detail_metadata}",
                evidence="repo-static",
            ),
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
