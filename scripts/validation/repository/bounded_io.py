"""Strict bounded file and subprocess I/O for repository validators."""

from __future__ import annotations

import os
import selectors
import stat
import subprocess
import time
from pathlib import Path
from typing import Mapping, Sequence


class BoundedInputError(ValueError):
    """A repository input is unsafe, oversized, or not strict UTF-8."""


class BoundedOutputError(ValueError):
    """A child process exceeded its declared output budget."""


def read_bytes(path: Path, *, max_bytes: int) -> bytes:
    """Read one non-symlink regular file without exceeding ``max_bytes``."""

    if max_bytes < 0:
        raise ValueError("max_bytes must be non-negative")
    flags = (
        os.O_RDONLY
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0)
        | getattr(os, "O_NONBLOCK", 0)
    )
    try:
        descriptor = os.open(path, flags)
    except OSError as exc:
        raise BoundedInputError("input is unavailable or unsafe") from exc
    try:
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode):
            raise BoundedInputError("input is not a regular file")
        if metadata.st_size > max_bytes:
            raise BoundedInputError("input exceeds its byte budget")
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(descriptor, min(65536, max_bytes + 1 - total))
            if not chunk:
                break
            chunks.append(chunk)
            total += len(chunk)
            if total > max_bytes:
                raise BoundedInputError("input exceeds its byte budget")
        return b"".join(chunks)
    except OSError as exc:
        raise BoundedInputError("input could not be read safely") from exc
    finally:
        os.close(descriptor)


def read_text(path: Path, *, max_bytes: int) -> str:
    """Read one bounded regular file as strict UTF-8."""

    try:
        return read_bytes(path, max_bytes=max_bytes).decode(
            "utf-8", errors="strict"
        )
    except UnicodeError as exc:
        raise BoundedInputError("input is not strict UTF-8") from exc


def run(
    argv: Sequence[str],
    *,
    timeout: float,
    stdout_limit: int,
    stderr_limit: int,
    cwd: Path | None = None,
    env: Mapping[str, str] | None = None,
    input_bytes: bytes | None = None,
) -> subprocess.CompletedProcess[bytes]:
    """Run a child with a deadline and independent streaming output budgets."""

    if timeout <= 0 or stdout_limit < 0 or stderr_limit < 0:
        raise ValueError("process budgets must be positive")
    process = subprocess.Popen(
        list(argv),
        cwd=cwd,
        env=None if env is None else dict(env),
        stdin=subprocess.PIPE if input_bytes is not None else subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert process.stdout is not None and process.stderr is not None
    selector = selectors.DefaultSelector()
    buffers = {"stdout": bytearray(), "stderr": bytearray()}
    limits = {"stdout": stdout_limit, "stderr": stderr_limit}
    deadline = time.monotonic() + timeout
    try:
        for name, stream in (("stdout", process.stdout), ("stderr", process.stderr)):
            os.set_blocking(stream.fileno(), False)
            selector.register(stream, selectors.EVENT_READ, name)

        pending_input = memoryview(input_bytes or b"")
        if process.stdin is not None:
            os.set_blocking(process.stdin.fileno(), False)
            if pending_input:
                selector.register(process.stdin, selectors.EVENT_WRITE, "stdin")
            else:
                process.stdin.close()

        while selector.get_map():
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise subprocess.TimeoutExpired(list(argv), timeout)
            events = selector.select(remaining)
            if not events:
                raise subprocess.TimeoutExpired(list(argv), timeout)
            for key, _mask in events:
                stream = key.fileobj
                name = key.data
                if name == "stdin":
                    try:
                        written = os.write(stream.fileno(), pending_input)
                    except BlockingIOError:
                        continue
                    pending_input = pending_input[written:]
                    if not pending_input:
                        selector.unregister(stream)
                        stream.close()
                    continue
                try:
                    chunk = os.read(stream.fileno(), 65536)
                except BlockingIOError:
                    continue
                if not chunk:
                    selector.unregister(stream)
                    stream.close()
                    continue
                buffers[name].extend(chunk)
                if len(buffers[name]) > limits[name]:
                    raise BoundedOutputError(f"{name} exceeds its byte budget")

        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise subprocess.TimeoutExpired(list(argv), timeout)
        returncode = process.wait(timeout=remaining)
        return subprocess.CompletedProcess(
            list(argv),
            returncode,
            bytes(buffers["stdout"]),
            bytes(buffers["stderr"]),
        )
    except Exception:
        process.kill()
        process.wait()
        raise
    finally:
        selector.close()
        for stream in (process.stdin, process.stdout, process.stderr):
            if stream is not None and not stream.closed:
                stream.close()
