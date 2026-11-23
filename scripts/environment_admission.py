"""Account-host admission for selected test clusters and command workers.

The database records intent before any external resource starts. Reservations
are accounting, not a filesystem or process sandbox; a caller releases one
only after its own resource probe confirms absence.
"""

from __future__ import annotations

import fcntl
import hashlib
import json
import os
import pwd
import re
import secrets
import sqlite3
import stat
import subprocess
import time
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Any

APP_LIMIT = 4
HOST_BUDGET = {"cpu": 4, "memory_mib": 8192, "disk_mib": 8192, "instances": 2}
RUN_BUDGET = {"cpu": 2, "memory_mib": 4096, "disk_mib": 4096, "instances": 1}
BUDGET_KEYS = frozenset({*HOST_BUDGET, "seconds"})
ID = re.compile(r"[a-z0-9][a-z0-9-]{0,63}\Z")
TOKEN = re.compile(r"[0-9a-f]{32}\Z")
DB_LIMIT = 4 * 1024 * 1024
ROW_LIMIT = 4096


class AdmissionError(ValueError):
    """A stable ENV_LIMIT, ENV_STATE, or ENV_BINDING diagnostic."""


def _fail(code: str, detail: str) -> AdmissionError:
    return AdmissionError(f"{code}: {detail}")


def _private_dir(path: Path) -> None:
    # A private final directory keeps another UID from replacing the DB path.
    for ancestor in (path, *path.parents):
        try:
            mode = ancestor.lstat().st_mode
        except FileNotFoundError:
            continue
        except OSError as exc:
            raise _fail("ENV_STATE", "state path is unavailable") from exc
        if stat.S_ISLNK(mode):
            raise _fail("ENV_STATE", "state path contains a symlink")
    try:
        path.mkdir(parents=True, mode=0o700, exist_ok=True)
        meta = path.lstat()
    except OSError as exc:
        raise _fail("ENV_STATE", "private state directory is unavailable") from exc
    if (
        not stat.S_ISDIR(meta.st_mode)
        or meta.st_uid != os.geteuid()
        or meta.st_mode & 0o077
    ):
        raise _fail("ENV_STATE", "state directory must be private and owned")


def _private_db(path: Path) -> None:
    try:
        if not path.exists():
            try:
                descriptor = os.open(
                    path, os.O_RDWR | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600
                )
            except FileExistsError:
                pass
            else:
                os.close(descriptor)
        meta = path.lstat()
    except OSError as exc:
        raise _fail("ENV_STATE", "private state database is unavailable") from exc
    if (
        not stat.S_ISREG(meta.st_mode)
        or meta.st_uid != os.geteuid()
        or meta.st_mode & 0o077
    ):
        raise _fail("ENV_STATE", "state database must be private and regular")
    if meta.st_size > DB_LIMIT:
        raise _fail("ENV_STATE", "state database exceeds its size limit")


def _binding(root: Path) -> tuple[str, str]:
    try:
        result = subprocess.run(
            [
                "/usr/bin/git",
                "-C",
                str(root),
                "rev-parse",
                "--path-format=absolute",
                "--git-common-dir",
                "--show-toplevel",
            ],
            capture_output=True,
            text=True,
            timeout=5,
            check=True,
            env={
                "PATH": "/usr/bin:/bin",
                "GIT_CONFIG_NOSYSTEM": "1",
                "GIT_CONFIG_GLOBAL": "/dev/null",
                "GIT_OPTIONAL_LOCKS": "0",
            },
        ).stdout.splitlines()
    except (OSError, subprocess.SubprocessError) as exc:
        raise _fail("ENV_BINDING", "Git workspace identity is unavailable") from exc
    if len(result) != 2 or Path(result[1]).resolve() != root.resolve():
        raise _fail("ENV_BINDING", "root is not the selected Git worktree")
    common = Path(result[0]).resolve()
    if not common.is_dir():
        raise _fail("ENV_BINDING", "Git common directory is unavailable")

    def digest(value: Path) -> str:
        return hashlib.sha256(str(value).encode()).hexdigest()[:24]

    return digest(common), digest(root.resolve())


def _available_memory_mib() -> int:
    try:
        for line in Path("/proc/meminfo").read_text(encoding="ascii").splitlines():
            if line.startswith("MemAvailable:"):
                return int(line.split()[1]) // 1024
    except (OSError, ValueError, IndexError) as exc:
        raise _fail("ENV_STATE", "host available memory is unavailable") from exc
    raise _fail("ENV_STATE", "host available memory is unavailable")


def _process_start(pid: int) -> int | None:
    try:
        fields = (
            Path(f"/proc/{pid}/stat")
            .read_text(encoding="ascii")
            .rsplit(") ", 1)[1]
            .split()
        )
        return int(fields[19])
    except (OSError, ValueError, IndexError):
        return None


class Admission:
    def __init__(
        self,
        root: Path,
        state_dir: Path | None = None,
        *,
        memory_margin_mib: int = 1024,
        disk_margin_mib: int = 1024,
    ) -> None:
        if any(
            type(value) is not int or not 0 <= value <= 1024
            for value in (memory_margin_mib, disk_margin_mib)
        ):
            raise _fail("ENV_LIMIT", "invalid host safety margin")
        self.memory_margin_mib = memory_margin_mib
        self.disk_margin_mib = disk_margin_mib
        self.root = Path(root).resolve()
        try:
            home = Path(pwd.getpwuid(os.geteuid()).pw_dir)
        except KeyError as exc:
            raise _fail("ENV_STATE", "account home is unavailable") from exc
        self.state_dir = (
            Path(state_dir)
            if state_dir is not None
            else home / ".local/state/hy-home.k8s/environment-admission"
        )
        _private_dir(self.state_dir)
        self.db = self.state_dir / "leases.sqlite3"
        _private_db(self.db)
        self.workspace_id, self.binding_id = _binding(self.root)
        try:
            with self._connect() as connection:
                connection.execute(
                    "CREATE TABLE IF NOT EXISTS leases (token TEXT PRIMARY KEY, workspace_id TEXT NOT NULL, binding_id TEXT NOT NULL, run_id TEXT NOT NULL, kind TEXT NOT NULL, closure TEXT NOT NULL, budget TEXT NOT NULL, intent TEXT NOT NULL, pid INTEGER, start_ticks INTEGER, created_at INTEGER NOT NULL)"
                )
        except sqlite3.Error as exc:
            raise _fail("ENV_STATE", "shared admission schema is unavailable") from exc

    def _connect(self) -> sqlite3.Connection:
        _private_db(self.db)
        try:
            connection = sqlite3.connect(self.db, timeout=5)
        except sqlite3.Error as exc:
            raise _fail(
                "ENV_STATE", "shared admission database is unavailable"
            ) from exc
        connection.row_factory = sqlite3.Row
        return connection

    def child_receipt_path(self, token: str, phase: str | None = None) -> Path:
        if not TOKEN.fullmatch(token):
            raise _fail("ENV_STATE", "invalid lease token")
        if phase not in {None, "network"}:
            raise _fail("ENV_STATE", "invalid child receipt phase")
        suffix = ".receipt" if phase is None else ".network.receipt"
        return self.state_dir / f"{token}{suffix}"

    def _gate(self, token: str) -> Path:
        return self.state_dir / f"{token}.gate"

    def reserve(
        self,
        run_id: str,
        kind: str,
        closure: Sequence[str],
        budget: dict[str, int],
        intent: dict[str, Any],
    ) -> str:
        if (
            not isinstance(run_id, str)
            or not ID.fullmatch(run_id)
            or kind not in {"cluster", "native", "worker", "integration"}
        ):
            raise _fail("ENV_BINDING", "invalid run or environment kind")
        if not isinstance(closure, (list, tuple)) or any(
            not isinstance(name, str) or not ID.fullmatch(name) for name in closure
        ):
            raise _fail("ENV_BINDING", "invalid selected component closure")
        if (
            not isinstance(budget, dict)
            or set(budget) != BUDGET_KEYS
            or any(
                type(v) is not int or v < (0 if k == "instances" else 1)
                for k, v in budget.items()
            )
        ):
            raise _fail(
                "ENV_LIMIT", "resource budget must contain positive integer values"
            )
        if any(budget[k] > RUN_BUDGET[k] for k in RUN_BUDGET) or budget["seconds"] > (
            600 if kind in {"cluster", "native"} else 86400
        ):
            raise _fail("ENV_LIMIT", "per-run resource budget exceeded")
        if (kind == "cluster") != (budget["instances"] == 1):
            raise _fail("ENV_LIMIT", "cluster instance reservation does not match kind")
        if not isinstance(intent, dict) or len(intent) > 16:
            raise _fail("ENV_BINDING", "invalid owner intent")
        try:
            encoded_intent = json.dumps(
                intent, ensure_ascii=True, separators=(",", ":")
            )
        except (TypeError, ValueError) as exc:
            raise _fail("ENV_BINDING", "owner intent cannot be encoded") from exc
        if len(encoded_intent) > 2048:
            raise _fail("ENV_BINDING", "owner intent exceeds its size limit")
        selected = sorted(set(closure))
        if len(selected) > APP_LIMIT:
            raise _fail("ENV_LIMIT", "selected component closure exceeds limit")
        token = secrets.token_hex(16)
        connection = self._connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            rows = connection.execute(
                "SELECT run_id,kind,closure,budget FROM leases LIMIT ?",
                (ROW_LIMIT + 1,),
            ).fetchall()
            if len(rows) > ROW_LIMIT:
                raise _fail("ENV_STATE", "too many active leases to verify")
            if kind == "cluster" and any(
                row["kind"] == "cluster" and row["run_id"] == run_id for row in rows
            ):
                raise _fail("ENV_BINDING", "cluster run ID already has an active lease")
            union = set(selected)
            total = {key: budget[key] for key in HOST_BUDGET}
            for row in rows:
                union.update(json.loads(row["closure"]))
                prior = json.loads(row["budget"])
                for key in total:
                    total[key] += prior[key]
            if len(union) > APP_LIMIT or any(
                total[key] > HOST_BUDGET[key] for key in total
            ):
                raise _fail("ENV_LIMIT", "active runs exceed shared host budget")
            if total["memory_mib"] > max(
                0, _available_memory_mib() - self.memory_margin_mib
            ):
                raise _fail("ENV_LIMIT", "insufficient currently available host memory")
            if total["disk_mib"] * 2**20 > max(
                0,
                os.statvfs(self.state_dir).f_bavail
                * os.statvfs(self.state_dir).f_frsize
                - self.disk_margin_mib * 2**20,
            ):
                raise _fail("ENV_LIMIT", "insufficient currently available host disk")
            connection.execute(
                "INSERT INTO leases VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                (
                    token,
                    self.workspace_id,
                    self.binding_id,
                    run_id,
                    kind,
                    json.dumps(selected),
                    json.dumps(budget),
                    encoded_intent,
                    None,
                    None,
                    int(time.time()),
                ),
            )
            if kind in {"cluster", "worker", "integration", "native"}:
                descriptor = os.open(
                    self._gate(token),
                    os.O_RDWR | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                    0o600,
                )
                os.write(descriptor, b"active\n")
                os.fsync(descriptor)
                os.close(descriptor)
            connection.commit()
        except (AdmissionError, OSError, sqlite3.Error, ValueError, KeyError) as exc:
            connection.rollback()
            self._gate(token).unlink(missing_ok=True)
            if isinstance(exc, AdmissionError):
                raise
            raise _fail("ENV_STATE", "shared admission transaction failed") from exc
        finally:
            connection.close()
        return token

    def _get(self, connection: sqlite3.Connection, token: str) -> dict[str, Any]:
        try:
            row = connection.execute(
                "SELECT * FROM leases WHERE token=?", (token,)
            ).fetchone()
        except sqlite3.Error as exc:
            raise _fail("ENV_STATE", "lease record is unavailable") from exc
        if row is None:
            raise _fail("ENV_STATE", "lease token is not active")
        value = dict(row)
        try:
            value["closure"] = json.loads(value["closure"])
            value["budget"] = json.loads(value["budget"])
            value["intent"] = json.loads(value["intent"])
        except (TypeError, ValueError) as exc:
            raise _fail("ENV_STATE", "lease record is invalid") from exc
        return value

    def mark_started(self, token: str, pid: int, start_ticks: int) -> None:
        if (
            not TOKEN.fullmatch(token)
            or type(pid) is not int
            or pid <= 0
            or type(start_ticks) is not int
            or start_ticks <= 0
        ):
            raise _fail("ENV_STATE", "invalid process identity")
        with self._connect() as connection:
            self._get(connection, token)
            connection.execute(
                "UPDATE leases SET pid=?,start_ticks=? WHERE token=?",
                (pid, start_ticks, token),
            )

    def active_for_run(self, run_id: str) -> list[dict[str, Any]]:
        if not isinstance(run_id, str) or not ID.fullmatch(run_id):
            raise _fail("ENV_BINDING", "invalid run ID")
        with self._connect() as connection:
            tokens = [
                row[0]
                for row in connection.execute(
                    "SELECT token FROM leases WHERE run_id=? LIMIT ?",
                    (run_id, ROW_LIMIT + 1),
                )
            ]
            if len(tokens) > ROW_LIMIT:
                raise _fail("ENV_STATE", "too many leases for one run")
            return [self._get(connection, token) for token in tokens]

    def active_for_binding(self) -> list[dict[str, Any]]:
        """Snapshot only leases for this exact Git common directory and worktree."""
        try:
            with self._connect() as connection:
                rows = connection.execute(
                    "SELECT token FROM leases WHERE workspace_id=? AND binding_id=? LIMIT ?",
                    (self.workspace_id, self.binding_id, ROW_LIMIT + 1),
                ).fetchall()
                if len(rows) > ROW_LIMIT:
                    raise _fail("ENV_STATE", "too many leases for this binding")
                return [self._get(connection, row[0]) for row in rows]
        except sqlite3.Error as exc:
            raise _fail("ENV_STATE", "bound lease inventory is unavailable") from exc

    def write_child_receipt(self, token: str, phase: str | None = None) -> None:
        """In a child preexec: publish identity before the actual command starts."""
        gate = os.open(self._gate(token), os.O_RDWR | os.O_NOFOLLOW)
        try:
            fcntl.flock(gate, fcntl.LOCK_EX)
            if os.pread(gate, 16, 0) != b"active\n":
                os._exit(125)
            start = _process_start(os.getpid())
            if start is None:
                os._exit(125)
            payload = f"{os.getpid()} {start} {os.getpgid(0)} {os.geteuid()}\n".encode()
            receipt = os.open(
                self.child_receipt_path(token, phase),
                os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                0o600,
            )
            try:
                os.write(receipt, payload)
                os.fsync(receipt)
            finally:
                os.close(receipt)
            directory = os.open(self.state_dir, os.O_RDONLY | os.O_DIRECTORY)
            try:
                os.fsync(directory)
            finally:
                os.close(directory)
        finally:
            os.close(gate)

    def release(
        self, token: str, absent: Callable[[dict[str, Any]], bool | None]
    ) -> None:
        if not TOKEN.fullmatch(token):
            raise _fail("ENV_STATE", "invalid lease token")
        gate_path = self._gate(token)
        try:
            gate = os.open(gate_path, os.O_RDWR | os.O_NOFOLLOW)
        except FileNotFoundError:
            gate = None
        except OSError as exc:
            raise _fail("ENV_STATE", "lease gate is unavailable") from exc
        try:
            if gate is not None:
                fcntl.flock(gate, fcntl.LOCK_EX)
            with self._connect() as connection:
                connection.execute("BEGIN IMMEDIATE")
                value = self._get(connection, token)
                if (
                    value["kind"] in {"cluster", "worker", "integration", "native"}
                    and gate is None
                ):
                    raise _fail("ENV_STATE", "process lease gate is missing")
                if absent(value) is not True:
                    raise _fail("ENV_STATE", "owned resource absence is unverified")
                if gate is not None:
                    os.ftruncate(gate, 0)
                    os.pwrite(gate, b"cancelled\n", 0)
                    os.fsync(gate)
                connection.execute("DELETE FROM leases WHERE token=?", (token,))
            gate_path.unlink(missing_ok=True)
            self.child_receipt_path(token).unlink(missing_ok=True)
            self.child_receipt_path(token, "network").unlink(missing_ok=True)
        finally:
            if gate is not None:
                os.close(gate)

    def recover(self, absent: Callable[[dict[str, Any]], bool | None]) -> list[str]:
        with self._connect() as connection:
            tokens = [
                row[0]
                for row in connection.execute(
                    "SELECT token FROM leases LIMIT ?", (ROW_LIMIT + 1,)
                )
            ]
        if len(tokens) > ROW_LIMIT:
            raise _fail("ENV_STATE", "too many active leases to recover")
        removed = []
        for token in tokens:
            try:
                self.release(token, absent)
            except AdmissionError:
                continue
            removed.append(token)
        return removed


__all__ = ["Admission", "AdmissionError", "APP_LIMIT", "HOST_BUDGET", "RUN_BUDGET"]
