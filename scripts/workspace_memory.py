#!/usr/bin/env python3
"""Shared workspace memory store for Claude and Codex sessions (SPEC-0109).

One SQLite file at the representative worktree root keeps every memory
revision and conflict. Memory is decision context, never Task status,
evidence, approval or acceptance. Nothing here deletes a memory body.
"""

from __future__ import annotations

import argparse
import contextlib
import datetime as dt
import fcntl
import hashlib
import json
import os
import re
import sqlite3
import stat
import subprocess
import sys
import tempfile
import uuid
from pathlib import Path
from typing import Any, Iterator, Sequence

SCHEMA_VERSION = 1
STORE_DIR = ".workspace-memory"
STORE_NAME = "memory.sqlite3"
BACKUP_NAME = "memory.backup.sqlite3"
MIB = 1024 * 1024
# Initial limits accepted in the SPEC-0109 Task; logical bytes count every revision
# and conflict. The 4 GiB store area is observed only (no filesystem quota).
TIER_LIMITS = {"short-term": 64 * MIB, "long-term": 128 * MIB, "domain": 256 * MIB}
DOMAIN_LIMIT = 64 * MIB
REVISION_LIMIT = 256 * 1024
DATABASE_LIMIT = 1024 * MIB
AREA_OBSERVED_LIMIT = 4096 * MIB
RUNTIME_FILE_LIMIT = 8
BUSY_TIMEOUT_MS = 5000
GIT_TIMEOUT_SECONDS = 10

REQUIRED_BODY = {
    "short-term": ("context", "narrative"),
    "long-term": ("claim", "reason", "applicability"),
    "domain": ("symptom", "cause", "resolution"),
}
# Task execution state has one owner; memory must not copy it.
FORBIDDEN_BODY = frozenset({"status", "result", "acceptance", "approval", "evidence"})
ELIGIBILITY = ("candidate", "current", "needs-review", "superseded", "withdrawn")
SENSITIVITY = ("public", "internal")
IDENTIFIER = re.compile(r"[a-z][a-z0-9-]{0,63}")

SCHEMA = """
create table if not exists meta (key text primary key, value text not null);
create table if not exists memory (
  memory_id text primary key, tier text not null, domain_id text,
  owner text not null, created_at text not null, eligibility text not null,
  sensitivity text not null, current_revision integer not null);
create table if not exists revision (
  memory_id text not null references memory(memory_id), revision integer not null,
  created_at text not null, owner text not null, source_refs text not null,
  body text not null, payload_bytes integer not null,
  primary key (memory_id, revision));
create table if not exists conflict (
  conflict_id integer primary key, memory_id text not null references memory(memory_id),
  expected_revision integer not null, current_revision integer not null,
  created_at text not null, owner text not null, source_refs text not null,
  body text not null, payload_bytes integer not null);
create table if not exists idempotency (
  key text primary key, result text not null, request_hash text);
"""


class MemoryError_(Exception):
    """A stable store diagnostic: CODE: detail."""


def _now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def _canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def representative_root(cwd: Path) -> Path:
    """The main worktree owning the Git common directory, never a linked one."""

    try:
        common = subprocess.run(
            [
                "git",
                "-C",
                str(cwd),
                "rev-parse",
                "--path-format=absolute",
                "--git-common-dir",
            ],
            check=True,
            capture_output=True,
            text=True,
            timeout=GIT_TIMEOUT_SECONDS,
        ).stdout.strip()
    except subprocess.TimeoutExpired as exc:
        raise MemoryError_("MEMORY_UNAVAILABLE: Git did not answer in time") from exc
    except (OSError, subprocess.CalledProcessError) as exc:
        raise MemoryError_("MEMORY_UNAVAILABLE: not inside a Git worktree") from exc
    common_path = Path(common)
    if common_path.name != ".git":
        raise MemoryError_("MEMORY_UNAVAILABLE: no representative worktree root")
    return common_path.parent


def caller_root(cwd: Path) -> Path:
    try:
        return Path(
            subprocess.run(
                ["git", "-C", str(cwd), "rev-parse", "--show-toplevel"],
                check=True,
                capture_output=True,
                text=True,
                timeout=GIT_TIMEOUT_SECONDS,
            ).stdout.strip()
        )
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        raise MemoryError_(
            "MEMORY_UNAVAILABLE: caller worktree is unavailable"
        ) from exc


class Store:
    def __init__(self, path: Path, root: Path, source_root: Path):
        self.path = path
        self.root = root
        self.source_root = source_root
        with self._connect() as connection:
            row = connection.execute(
                "select value from meta where key = 'workspace_id'"
            ).fetchone()
            version = connection.execute(
                "select value from meta where key = 'schema_version'"
            ).fetchone()
        if row is None or version is None or int(version[0]) != SCHEMA_VERSION:
            raise MemoryError_("MEMORY_UNAVAILABLE: store identity is missing")
        self.workspace_id = row[0]

    @classmethod
    def init(cls, cwd: Path) -> "Store":
        root = representative_root(cwd)
        source_root = caller_root(cwd)
        path = root / STORE_DIR / STORE_NAME
        if path.parent.is_symlink() or path.is_symlink():
            raise MemoryError_("MEMORY_UNAVAILABLE: store path is linked")
        if path.exists():
            raise MemoryError_("MEMORY_EXISTS: the workspace store already exists")
        path.parent.mkdir(mode=0o700, exist_ok=True)
        connection = sqlite3.connect(path)
        try:
            page_size = connection.execute("pragma page_size").fetchone()[0]
            connection.execute("pragma journal_mode=delete")
            connection.execute(f"pragma max_page_count={DATABASE_LIMIT // page_size}")
            connection.executescript(SCHEMA)
            connection.executemany(
                "insert into meta values (?, ?)",
                [
                    ("schema_version", str(SCHEMA_VERSION)),
                    ("workspace_id", str(uuid.uuid4())),
                ],
            )
            connection.commit()
        finally:
            connection.close()
        return cls(path, root, source_root)

    @classmethod
    def open(cls, cwd: Path) -> "Store":
        root = representative_root(cwd)
        path = root / STORE_DIR / STORE_NAME
        if path.parent.is_symlink() or path.is_symlink() or not path.is_file():
            raise MemoryError_("MEMORY_UNAVAILABLE: run init at the workspace root")
        return cls(path, root, caller_root(cwd))

    @contextlib.contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        if self.path.parent.is_symlink() or self.path.is_symlink():
            raise MemoryError_("MEMORY_UNAVAILABLE: store path is linked")
        connection = sqlite3.connect(
            self.path.as_uri() + "?mode=rw", uri=True, isolation_level=None
        )
        try:
            connection.execute(f"pragma busy_timeout={BUSY_TIMEOUT_MS}")
            connection.execute("pragma journal_mode=delete")
            connection.execute("pragma foreign_keys=on")
            page_size = connection.execute("pragma page_size").fetchone()[0]
            limit = DATABASE_LIMIT // page_size
            if (
                connection.execute(f"pragma max_page_count={limit}").fetchone()[0]
                != limit
            ):
                raise MemoryError_("MEMORY_CAPACITY_EXCEEDED: database page limit")
            yield connection
        finally:
            connection.close()

    @contextlib.contextmanager
    def _write(self) -> Iterator[sqlite3.Connection]:
        with self._connect() as connection:
            connection.execute("begin immediate")
            try:
                yield connection
            except BaseException:
                connection.execute("rollback")
                raise
            connection.execute("commit")

    def _source_digest(self, raw: str) -> str:
        if not isinstance(raw, str):
            raise MemoryError_("MEMORY_SCHEMA: source ref is not a path")
        relative = Path(raw)
        if not relative.parts or relative.is_absolute() or ".." in relative.parts:
            raise MemoryError_("MEMORY_SCHEMA: source refs are repository-relative")
        try:
            directory = os.open(
                self.source_root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
            )
            try:
                for part in relative.parts[:-1]:
                    child = os.open(
                        part,
                        os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                        dir_fd=directory,
                    )
                    os.close(directory)
                    directory = child
                file_fd = os.open(
                    relative.parts[-1],
                    os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK,
                    dir_fd=directory,
                )
                with os.fdopen(file_fd, "rb") as source:
                    if not stat.S_ISREG(os.fstat(source.fileno()).st_mode):
                        raise MemoryError_(
                            "MEMORY_SCHEMA: source is not a regular file"
                        )
                    digest = hashlib.sha256()
                    for chunk in iter(lambda: source.read(1024 * 1024), b""):
                        digest.update(chunk)
                    return digest.hexdigest()
            finally:
                os.close(directory)
        except (OSError, ValueError) as exc:
            raise MemoryError_(
                "MEMORY_SCHEMA: source is unavailable or linked"
            ) from exc

    def _source_ref(self, raw: str) -> dict[str, str]:
        digest = self._source_digest(raw)
        return {
            "path": Path(raw).as_posix(),
            "sha256": digest,
        }

    @staticmethod
    def _validate(
        tier: str, body: Any, sensitivity: str, domain_id: str | None
    ) -> None:
        if tier not in REQUIRED_BODY:
            raise MemoryError_("MEMORY_SCHEMA: unknown tier")
        if not isinstance(body, dict) or any(
            not isinstance(body.get(key), str) or not body[key].strip()
            for key in REQUIRED_BODY[tier]
        ):
            raise MemoryError_(
                f"MEMORY_SCHEMA: {tier} body needs {REQUIRED_BODY[tier]}"
            )
        if FORBIDDEN_BODY & set(body):
            raise MemoryError_("MEMORY_SCHEMA: Task state belongs to the Task")
        if sensitivity not in SENSITIVITY:
            raise MemoryError_("MEMORY_SCHEMA: secret material is never stored")
        if (tier == "domain") != (domain_id is not None) or (
            domain_id is not None and not IDENTIFIER.fullmatch(domain_id)
        ):
            raise MemoryError_("MEMORY_SCHEMA: domain tier needs one domain_id")

    @staticmethod
    def _usage(
        connection: sqlite3.Connection, tier: str, domain: str | None
    ) -> tuple[int, int]:
        query = """select coalesce(sum(p), 0) from (
            select r.payload_bytes p, m.tier t, m.domain_id d from revision r join memory m using (memory_id)
            union all
            select c.payload_bytes, m.tier, m.domain_id from conflict c join memory m using (memory_id))
            where t = ? {}"""
        tier_bytes = connection.execute(query.format(""), (tier,)).fetchone()[0]
        domain_bytes = (
            connection.execute(query.format("and d = ?"), (tier, domain)).fetchone()[0]
            if domain is not None
            else 0
        )
        return tier_bytes, domain_bytes

    def _fits(
        self, connection: sqlite3.Connection, tier: str, domain: str | None, size: int
    ) -> bool:
        tier_bytes, domain_bytes = self._usage(connection, tier, domain)
        return tier_bytes + size <= TIER_LIMITS[tier] and (
            domain is None or domain_bytes + size <= DOMAIN_LIMIT
        )

    def write(
        self,
        *,
        tier: str,
        body: dict[str, Any],
        owner: str,
        source_refs: Sequence[str] = (),
        sensitivity: str = "internal",
        memory_id: str | None = None,
        expected_revision: int | None = None,
        idempotency_key: str | None = None,
        domain_id: str | None = None,
    ) -> dict[str, Any]:
        self._validate(tier, body, sensitivity, domain_id)
        refs = [self._source_ref(raw) for raw in source_refs]
        payload = _canonical({"body": body, "source_refs": refs, "owner": owner})
        size = len(payload.encode("utf-8"))
        request_hash = hashlib.sha256(
            _canonical(
                {
                    "tier": tier,
                    "domain_id": domain_id,
                    "owner": owner,
                    "body": body,
                    "source_refs": refs,
                    "sensitivity": sensitivity,
                    "memory_id": memory_id,
                    "expected_revision": expected_revision,
                }
            ).encode("utf-8")
        ).hexdigest()
        if size > REVISION_LIMIT:
            raise MemoryError_("MEMORY_CAPACITY_EXCEEDED: revision payload limit")
        with self._write() as connection:
            if idempotency_key is not None:
                if "request_hash" not in {
                    column[1]
                    for column in connection.execute("pragma table_info(idempotency)")
                }:
                    connection.execute(
                        "alter table idempotency add column request_hash text"
                    )
                seen = connection.execute(
                    "select result, request_hash from idempotency where key = ?",
                    (idempotency_key,),
                ).fetchone()
                if seen is not None:
                    if seen[1] != request_hash:
                        raise MemoryError_(
                            "MEMORY_CONFLICT: idempotency key belongs to another request"
                        )
                    return json.loads(seen[0])
            if memory_id is None:
                if expected_revision is not None:
                    raise MemoryError_("MEMORY_SCHEMA: a new memory has no revision")
                if not self._fits(connection, tier, domain_id, size):
                    raise MemoryError_("MEMORY_CAPACITY_EXCEEDED: tier or domain limit")
                memory_id = f"mem-{uuid.uuid4().hex[:16]}"
                connection.execute(
                    "insert into memory values (?, ?, ?, ?, ?, 'candidate', ?, 1)",
                    (memory_id, tier, domain_id, owner, _now(), sensitivity),
                )
                revision = 1
            else:
                row = connection.execute(
                    "select tier, domain_id, current_revision from memory where memory_id = ?",
                    (memory_id,),
                ).fetchone()
                if row is None:
                    raise MemoryError_("MEMORY_NOT_FOUND: unknown memory_id")
                if (row[0], row[1]) != (tier, domain_id):
                    raise MemoryError_("MEMORY_SCHEMA: tier and domain never change")
                if expected_revision != row[2]:
                    stored = self._fits(connection, tier, domain_id, size)
                    if stored:
                        connection.execute(
                            "insert into conflict (memory_id, expected_revision, current_revision,"
                            " created_at, owner, source_refs, body, payload_bytes)"
                            " values (?, ?, ?, ?, ?, ?, ?, ?)",
                            (
                                memory_id,
                                expected_revision or 0,
                                row[2],
                                _now(),
                                owner,
                                _canonical(refs),
                                _canonical(body),
                                size,
                            ),
                        )
                    result = {
                        "outcome": "conflict",
                        "memory_id": memory_id,
                        "expected_revision": expected_revision,
                        "current_revision": row[2],
                        "stored": stored,
                    }
                    return result
                if not self._fits(connection, tier, domain_id, size):
                    raise MemoryError_("MEMORY_CAPACITY_EXCEEDED: tier or domain limit")
                revision = row[2] + 1
                connection.execute(
                    "update memory set current_revision = ? where memory_id = ?",
                    (revision, memory_id),
                )
            connection.execute(
                "insert into revision values (?, ?, ?, ?, ?, ?, ?)",
                (
                    memory_id,
                    revision,
                    _now(),
                    owner,
                    _canonical(refs),
                    _canonical(body),
                    size,
                ),
            )
            result = {
                "outcome": "written",
                "memory_id": memory_id,
                "revision": revision,
                "workspace_id": self.workspace_id,
            }
            if idempotency_key is not None:
                connection.execute(
                    "insert into idempotency (key, result, request_hash) values (?, ?, ?)",
                    (idempotency_key, _canonical(result), request_hash),
                )
            return result

    def set_eligibility(
        self, memory_id: str, eligibility: str, *, expected_revision: int
    ) -> dict[str, Any]:
        if eligibility not in ELIGIBILITY:
            raise MemoryError_("MEMORY_SCHEMA: unknown eligibility")
        with self._write() as connection:
            row = connection.execute(
                "select current_revision from memory where memory_id = ?", (memory_id,)
            ).fetchone()
            if row is None:
                raise MemoryError_("MEMORY_NOT_FOUND: unknown memory_id")
            if row[0] != expected_revision:
                raise MemoryError_("MEMORY_CONFLICT: revision changed")
            connection.execute(
                "update memory set eligibility = ? where memory_id = ?",
                (eligibility, memory_id),
            )
        return {"memory_id": memory_id, "eligibility": eligibility}

    def _record(self, row: sqlite3.Row | tuple) -> dict[str, Any]:
        (
            memory_id,
            tier,
            domain_id,
            owner,
            eligibility,
            sensitivity,
            revision,
            refs,
            body,
        ) = row
        refs = json.loads(refs)
        stale = []
        for ref in refs:
            try:
                changed = self._source_digest(ref["path"]) != ref["sha256"]
            except MemoryError_:
                changed = True
            if changed:
                stale.append(ref["path"])
        return {
            "memory_id": memory_id,
            "tier": tier,
            "domain_id": domain_id,
            "owner": owner,
            "eligibility": eligibility,
            "sensitivity": sensitivity,
            "revision": revision,
            "source_refs": refs,
            "stale_sources": stale,
            "body": json.loads(body),
            "workspace_id": self.workspace_id,
        }

    _CURRENT = """select m.memory_id, m.tier, m.domain_id, m.owner, m.eligibility, m.sensitivity,
        r.revision, r.source_refs, r.body from memory m join revision r
        on r.memory_id = m.memory_id and r.revision = m.current_revision"""

    def get(self, memory_id: str) -> dict[str, Any]:
        with self._connect() as connection:
            row = connection.execute(
                self._CURRENT + " where m.memory_id = ?", (memory_id,)
            ).fetchone()
        if row is None:
            raise MemoryError_("MEMORY_NOT_FOUND: unknown memory_id")
        return self._record(row)

    def query(
        self, *, tier: str | None = None, include_stale: bool = False
    ) -> list[dict[str, Any]]:
        """Default reuse view: current eligibility and unchanged sources only."""

        with self._connect() as connection:
            rows = connection.execute(
                self._CURRENT + " where m.eligibility = 'current'"
                " and (? is null or m.tier = ?) order by m.memory_id",
                (tier, tier),
            ).fetchall()
        records = [self._record(row) for row in rows]
        return (
            records if include_stale else [r for r in records if not r["stale_sources"]]
        )

    def history(self, memory_id: str) -> dict[str, Any]:
        """Every retained revision and conflict, labelled as history."""

        with self._connect() as connection:
            revisions = connection.execute(
                "select revision, created_at, owner, source_refs, body from revision"
                " where memory_id = ? order by revision",
                (memory_id,),
            ).fetchall()
            conflicts = connection.execute(
                "select expected_revision, current_revision, created_at, owner, body from conflict"
                " where memory_id = ? order by conflict_id",
                (memory_id,),
            ).fetchall()
        if not revisions:
            raise MemoryError_("MEMORY_NOT_FOUND: unknown memory_id")
        return {
            "memory_id": memory_id,
            "view": "history",
            "revisions": [
                {
                    "revision": r[0],
                    "created_at": r[1],
                    "owner": r[2],
                    "source_refs": json.loads(r[3]),
                    "body": json.loads(r[4]),
                }
                for r in revisions
            ],
            "conflicts": [
                {
                    "expected_revision": c[0],
                    "current_revision": c[1],
                    "created_at": c[2],
                    "owner": c[3],
                    "body": json.loads(c[4]),
                }
                for c in conflicts
            ],
        }

    def usage(self) -> dict[str, Any]:
        with self._connect() as connection:
            tiers = {}
            for tier, limit in TIER_LIMITS.items():
                used, _ = self._usage(connection, tier, None)
                count = connection.execute(
                    "select count(*) from revision join memory using (memory_id) where tier = ?",
                    (tier,),
                ).fetchone()[0]
                tiers[tier] = {"bytes": used, "limit": limit, "revisions": count}
        files = [entry for entry in self.path.parent.iterdir() if entry.is_file()]
        return {
            "workspace_id": self.workspace_id,
            "tiers": tiers,
            "area_bytes": sum(entry.stat().st_size for entry in files),
            "area_limit_observed_only": AREA_OBSERVED_LIMIT,
            "runtime_files": len(files),
            "runtime_file_limit": RUNTIME_FILE_LIMIT,
            "sqlite_version": sqlite3.sqlite_version,
        }

    def backup(self) -> dict[str, Any]:
        """Refresh the single backup container; keep the old one on failure."""

        target = self.path.parent / BACKUP_NAME
        temporary: Path | None = None
        try:
            if self.path.parent.is_symlink() or self.path.is_symlink():
                raise OSError("store path is linked")
            with os.fdopen(
                os.open(self.path, os.O_RDONLY | os.O_NOFOLLOW), "rb"
            ) as lock:
                if not stat.S_ISREG(os.fstat(lock.fileno()).st_mode):
                    raise OSError("store is not a regular file")
                fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
                if target.is_symlink() or (target.exists() and not target.is_file()):
                    raise OSError("backup target is linked or not a regular file")
                fd, name = tempfile.mkstemp(
                    prefix=BACKUP_NAME + ".", dir=self.path.parent
                )
                os.close(fd)
                temporary = Path(name)
                with (
                    self._connect() as source,
                    contextlib.closing(sqlite3.connect(temporary)) as copy,
                ):

                    def state(connection: sqlite3.Connection) -> tuple[Any, ...]:
                        return (
                            connection.execute(
                                "select key, value from meta order by key"
                            ).fetchall(),
                            connection.execute(
                                "select type, name, sql from sqlite_master"
                                " where name not like 'sqlite_%' order by type, name"
                            ).fetchall(),
                            tuple(
                                connection.execute(
                                    f"select count(*) from {table}"
                                ).fetchone()[0]
                                for table in (
                                    "memory",
                                    "revision",
                                    "conflict",
                                    "idempotency",
                                )
                            ),
                        )

                    expected = state(source)
                    if source.execute(
                        "select value from meta where key = 'workspace_id'"
                    ).fetchone() != (self.workspace_id,):
                        raise OSError("backup workspace identity differs")
                    source.backup(copy)
                    if copy.execute("pragma integrity_check").fetchone()[0] != "ok":
                        raise OSError("backup integrity check failed")
                    if state(copy) != expected or state(source) != expected:
                        raise OSError("backup schema, identity or records differ")
                    revisions = expected[2][1]
                if target.is_symlink():
                    raise OSError("backup target became linked")
                os.replace(temporary, target)
        except (OSError, sqlite3.Error) as exc:
            raise MemoryError_("MEMORY_BACKUP_FAILED: previous backup kept") from exc
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)
        return {"path": str(target), "revisions": revisions}


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("init")
    commands.add_parser("resolve")
    commands.add_parser("usage")
    commands.add_parser("backup")
    write = commands.add_parser("write")
    write.add_argument("--tier", required=True)
    write.add_argument("--owner", required=True)
    write.add_argument("--body-file", type=Path, required=True)
    write.add_argument("--source-ref", action="append", default=[])
    write.add_argument("--sensitivity", default="internal")
    write.add_argument("--memory-id")
    write.add_argument("--expected-revision", type=int)
    write.add_argument("--idempotency-key")
    write.add_argument("--domain-id")
    get = commands.add_parser("get")
    get.add_argument("memory_id")
    history = commands.add_parser("history")
    history.add_argument("memory_id")
    query = commands.add_parser("query")
    query.add_argument("--tier")
    query.add_argument("--include-stale", action="store_true")
    eligibility = commands.add_parser("eligibility")
    eligibility.add_argument("memory_id")
    eligibility.add_argument("value")
    eligibility.add_argument("--expected-revision", type=int, required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "init":
            store = Store.init(args.root)
            result: Any = {"path": str(store.path), "workspace_id": store.workspace_id}
        else:
            store = Store.open(args.root)
            if args.command == "resolve":
                result = {"path": str(store.path), "workspace_id": store.workspace_id}
            elif args.command == "usage":
                result = store.usage()
            elif args.command == "backup":
                result = store.backup()
            elif args.command == "get":
                result = store.get(args.memory_id)
            elif args.command == "history":
                result = store.history(args.memory_id)
            elif args.command == "query":
                result = store.query(tier=args.tier, include_stale=args.include_stale)
            elif args.command == "eligibility":
                result = store.set_eligibility(
                    args.memory_id, args.value, expected_revision=args.expected_revision
                )
            else:
                result = store.write(
                    tier=args.tier,
                    owner=args.owner,
                    body=json.loads(args.body_file.read_text(encoding="utf-8")),
                    source_refs=args.source_ref,
                    sensitivity=args.sensitivity,
                    memory_id=args.memory_id,
                    expected_revision=args.expected_revision,
                    idempotency_key=args.idempotency_key,
                    domain_id=args.domain_id,
                )
    except (MemoryError_, OSError, ValueError, sqlite3.Error) as exc:
        message = (
            str(exc)
            if isinstance(exc, MemoryError_)
            else f"MEMORY_ERROR: {type(exc).__name__}"
        )
        print(message, file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
