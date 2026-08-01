#!/usr/bin/env python3
"""Run contract-approved repository-static validators for a NUL path set."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import os
import pwd
import selectors
import signal
import shutil
import stat
import subprocess
import sys
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


def cleanup_process_group(
    process: subprocess.Popen[bytes], cleanup_seconds: float
) -> bool:
    """Kill one owned group, close pipes, and reap under one total deadline.

    Group signaling intentionally precedes the only direct-leader reap.  A
    deferred asynchronous exception is re-raised only after every cleanup step
    received a best-effort attempt.
    """

    cleanup_complete = True
    deferred: BaseException | None = None

    # Idempotent finalization must never signal a numeric process-group ID
    # after its direct leader has already been reaped.
    if getattr(process, "returncode", None) is not None:
        for pipe in (process.stdout, process.stderr):
            try:
                if not _close_pipe(pipe):
                    cleanup_complete = False
            except BaseException as exc:
                cleanup_complete = False
                deferred = deferred or exc
        if deferred is not None:
            raise deferred
        return cleanup_complete

    try:
        deadline = time.monotonic() + max(0.0, cleanup_seconds)
    except Exception:
        deadline = None
        cleanup_complete = False
    except BaseException as exc:
        deadline = None
        cleanup_complete = False
        deferred = exc

    group_signal_succeeded = False
    try:
        os.killpg(process.pid, signal.SIGKILL)
        group_signal_succeeded = True
    except ProcessLookupError:
        # A caller may provide an already-reaped synthetic process.  The
        # absence is safe only when a return code is already recorded.
        if getattr(process, "returncode", None) is None:
            cleanup_complete = False
    except Exception:
        cleanup_complete = False
    except BaseException as exc:
        cleanup_complete = False
        deferred = deferred or exc

    if not group_signal_succeeded:
        try:
            process.kill()
        except ProcessLookupError:
            pass
        except Exception:
            cleanup_complete = False
        except BaseException as exc:
            cleanup_complete = False
            deferred = deferred or exc

    for pipe in (process.stdout, process.stderr):
        try:
            if not _close_pipe(pipe):
                cleanup_complete = False
        except BaseException as exc:
            # A custom/test pipe may close successfully and then interrupt.
            # Continue so the other pipe and leader are still finalized.
            cleanup_complete = False
            deferred = deferred or exc

    if getattr(process, "returncode", None) is None:
        try:
            if deadline is None:
                remaining = max(0.0, cleanup_seconds)
            else:
                remaining = max(0.0, deadline - time.monotonic())
        except Exception:
            remaining = 0.0
            cleanup_complete = False
        except BaseException as exc:
            remaining = 0.0
            cleanup_complete = False
            deferred = deferred or exc
        try:
            process.wait(timeout=remaining)
        except Exception:
            cleanup_complete = False
        except BaseException as exc:
            cleanup_complete = False
            deferred = deferred or exc

    if deferred is not None:
        raise deferred
    return cleanup_complete


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
    process: subprocess.Popen[bytes] | None = None
    status = "start_failure"
    cleanup_complete = True
    try:
        try:
            process = subprocess.Popen(
                list(argv),
                cwd=cwd,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=False,
                env=env,
                text=False,
                bufsize=0,
                close_fds=True,
                start_new_session=True,
            )
        except OSError:
            selector_ok, deferred = _close_selector(selector)
            if deferred is not None:
                raise deferred
            return BoundedCommandResult(
                status="start_failure" if selector_ok else "pipe_failure",
                returncode=None,
                stdout=accumulators["stdout"].result(complete=False),
                stderr=accumulators["stderr"].result(complete=False),
                cleanup_complete=selector_ok,
            )

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
        cleanup_complete = cleanup_process_group(process, cleanup_seconds)
        if status == "ready_for_completion":
            status = "completed" if cleanup_complete else "cleanup_failure"
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
                cleanup_process_group(process, cleanup_seconds)
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
