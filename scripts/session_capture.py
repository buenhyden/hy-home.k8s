#!/usr/bin/env python3
"""Local session capture for Claude and Codex sessions in this workspace (W08-CAPTURE).

The archive holds pointers and structure only: provider, session and event
IDs, the transcript path, byte offsets, line digests, record kinds, times,
tool names and ordinals. Values that are not identifiers or ISO times are
replaced, so no prompt, response, tool argument or output text is copied; the
text stays in the provider's own transcript file. A transcript is read only
inside the provider's own session directory. A lifecycle hook only records one
event row and returns; `scan` reads transcripts by cursor in bounded batches.
"""

from __future__ import annotations

import argparse
import contextlib
import datetime as dt
import hashlib
import json
import os
import re
import sqlite3
import stat
import sys
from pathlib import Path
from typing import Any, Iterator, Sequence

import workspace_memory as memory

SCHEMA_VERSION = 1
CAPTURE_NAME = "sessions.sqlite3"
HOOK_EVENTS = frozenset(
    {"SessionStart", "Stop", "PreCompact", "SubagentStop", "SessionEnd"}
)
PROVIDERS = frozenset({"claude", "codex"})
HOOK_INPUT_LIMIT = 1024 * 1024
HOOK_BUSY_TIMEOUT_MS = 2000
SCAN_BUSY_TIMEOUT_MS = 5000
SCAN_CHUNK_LIMIT = 4 * 1024 * 1024
DATABASE_LIMIT = 256 * 1024 * 1024
TOKEN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:/-]{0,127}")
LABEL = re.compile(r"[a-z][a-z0-9_-]{0,31}")
KIND = re.compile(r"[A-Za-z][A-Za-z0-9_.-]{0,63}")
TOOL = re.compile(r"[A-Za-z][A-Za-z0-9_.:-]{0,63}")
ISO_TIME = re.compile(
    r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,9})?(?:Z|[+-]\d{2}:\d{2})?"
)
CODEX_TOOL_ITEMS = frozenset({"function_call", "custom_tool_call", "local_shell_call"})

SCHEMA = """
create table if not exists meta (key text primary key, value text not null);
create table if not exists session (
  provider text not null, session_id text not null, parent_id text,
  transcript_path text, first_seen text not null, ended integer not null default 0,
  primary key (provider, session_id));
create table if not exists event (
  provider text not null, session_id text not null, event text not null,
  detail text not null, transcript_bytes integer not null, captured_at text not null,
  primary key (provider, session_id, event, detail, transcript_bytes));
create table if not exists cursor (
  provider text not null, session_id text not null, path text not null,
  device integer not null, inode integer not null, offset integer not null,
  last_line_sha256 text, last_line_bytes integer, last_ordinal integer,
  ordinal_gaps integer not null default 0, partial_tail integer not null default 0,
  oversized_line integer not null default 0, modified integer not null default 0,
  scanned_at text not null, primary key (provider, session_id, path));
create table if not exists record (
  provider text not null, session_id text not null, path text not null,
  offset integer not null, length integer not null, sha256 text not null,
  kind text not null, occurred_at text, ordinal integer, tool text,
  primary key (provider, session_id, path, offset));
create table if not exists forgotten (
  provider text not null, session_id text not null, forgotten_at text not null,
  owner text not null, approval_ref text not null, primary key (provider, session_id));
"""


def _now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def _match(pattern: re.Pattern[str], value: Any) -> str | None:
    return value if isinstance(value, str) and pattern.fullmatch(value) else None


def session_root(provider: str) -> Path:
    """The provider's own session directory; nothing outside it is read."""

    if provider == "codex":
        return Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex") / "sessions"
    home = os.environ.get("CLAUDE_CONFIG_DIR") or Path.home() / ".claude"
    return Path(home) / "projects"


def transcript_path(provider: str, value: Any) -> str | None:
    """An unlinked `.jsonl` path inside the provider's session directory, or None."""

    if not isinstance(value, str) or not value or len(value) > 4096:
        return None
    if not os.path.isabs(value) or not value.endswith(".jsonl"):
        return None
    resolved = os.path.realpath(value)
    root = os.path.realpath(session_root(provider))
    if resolved != os.path.normpath(value) or not resolved.startswith(root + os.sep):
        return None
    return resolved


def describe(provider: str, line: bytes) -> dict[str, Any]:
    """Structure of one transcript line: identifiers and times only, never text."""

    try:
        data = json.loads(line)
    except ValueError:
        data = None
    if not isinstance(data, dict):
        return {
            "kind": "unparsable",
            "occurred_at": None,
            "ordinal": None,
            "tool": None,
        }
    kind = _match(KIND, data.get("type")) or "other"
    tool, ordinal = None, None
    if provider == "codex":
        payload = data.get("payload") if isinstance(data.get("payload"), dict) else {}
        if "type" in payload:
            kind = f"{kind}/{_match(KIND, payload['type']) or 'other'}"
        if payload.get("type") in CODEX_TOOL_ITEMS:
            tool = _match(TOOL, payload.get("name")) or "other"
        if isinstance(data.get("ordinal"), int) and not isinstance(
            data["ordinal"], bool
        ):
            ordinal = data["ordinal"]
    else:
        message = data.get("message") if isinstance(data.get("message"), dict) else {}
        content = message.get("content")
        for part in content if isinstance(content, list) else ():
            if isinstance(part, dict) and part.get("type") == "tool_use":
                tool = _match(TOOL, part.get("name")) or "other"
                break
    return {
        "kind": kind,
        "occurred_at": _match(ISO_TIME, data.get("timestamp")),
        "ordinal": ordinal,
        "tool": tool,
    }


def _lines(chunk: bytes) -> list[bytes]:
    """Whole newline-terminated lines; a lone carriage return never splits."""

    return [part + b"\n" for part in chunk.split(b"\n")[:-1]]


def _selector(session_id: str) -> tuple[str, tuple[Any, ...]]:
    prefix = session_id + "/agent/"
    return (
        "provider = ? and (session_id = ? or substr(session_id, 1, ?) = ?)",
        (session_id, len(prefix), prefix),
    )


class Capture:
    busy_ms = SCAN_BUSY_TIMEOUT_MS

    def __init__(self, path: Path, root: Path, workspace_id: str):
        self.path = path
        self.root = root
        self.workspace_id = workspace_id

    @classmethod
    def open(cls, cwd: Path, *, busy_ms: int = SCAN_BUSY_TIMEOUT_MS) -> "Capture":
        store = memory.Store.open(cwd)
        capture = cls(store.path.parent / CAPTURE_NAME, store.root, store.workspace_id)
        capture.busy_ms = busy_ms
        if capture.path.is_symlink():
            raise memory.MemoryError_("MEMORY_UNAVAILABLE: capture path is linked")
        with capture._connect() as connection:
            connection.executescript(SCHEMA)
            connection.execute(
                "insert or ignore into meta values ('schema_version', ?), ('workspace_id', ?)",
                (str(SCHEMA_VERSION), store.workspace_id),
            )
            identity = dict(
                connection.execute("select key, value from meta").fetchall()
            )
        if identity != {
            "schema_version": str(SCHEMA_VERSION),
            "workspace_id": store.workspace_id,
        }:
            raise memory.MemoryError_("MEMORY_UNAVAILABLE: capture identity differs")
        return capture

    @contextlib.contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(self.path, isolation_level=None)
        try:
            connection.execute(f"pragma busy_timeout={self.busy_ms}")
            if (
                connection.execute("pragma journal_mode=delete").fetchone()[0]
                != "delete"
            ):
                raise memory.MemoryError_(
                    "MEMORY_UNAVAILABLE: rollback journal is unavailable"
                )
            page_size = connection.execute("pragma page_size").fetchone()[0]
            connection.execute(f"pragma max_page_count={DATABASE_LIMIT // page_size}")
            yield connection
        finally:
            connection.close()

    @contextlib.contextmanager
    def _write(self) -> Iterator[sqlite3.Connection]:
        with self._connect() as connection:
            connection.execute("pragma secure_delete=on")
            connection.execute("begin immediate")
            try:
                yield connection
            except BaseException:
                connection.execute("rollback")
                raise
            connection.execute("commit")

    @staticmethod
    def _forgotten(
        connection: sqlite3.Connection, provider: str, session_id: str
    ) -> bool:
        candidates = {session_id, session_id.split("/agent/", 1)[0]}
        return any(
            connection.execute(
                "select 1 from forgotten where provider = ? and session_id = ?",
                (provider, candidate),
            ).fetchone()
            for candidate in candidates
        )

    def hook(self, provider: str, payload: dict[str, Any]) -> dict[str, str]:
        """Record one lifecycle event; ignore anything outside this workspace."""

        if provider not in PROVIDERS or not isinstance(payload, dict):
            return {"outcome": "ignored"}
        event = payload.get("hook_event_name")
        session_id = _match(TOKEN, payload.get("session_id"))
        cwd = payload.get("cwd")
        if event not in HOOK_EVENTS or session_id is None or not isinstance(cwd, str):
            return {"outcome": "ignored"}
        try:
            if memory.representative_root(Path(cwd)) != self.root:
                return {"outcome": "ignored"}
        except memory.MemoryError_:
            return {"outcome": "ignored"}
        transcript = transcript_path(provider, payload.get("transcript_path"))
        detail = next(
            (
                label
                for key in ("source", "reason", "trigger")
                if (label := _match(LABEL, payload.get(key)))
            ),
            "",
        )
        size = -1
        with contextlib.suppress(OSError):
            info = os.lstat(transcript) if transcript else None
            if info is not None and stat.S_ISREG(info.st_mode):
                size = info.st_size
        ended = {"SessionEnd": True, "SessionStart": False}.get(event)
        now = _now()
        with self._write() as connection:
            if self._forgotten(connection, provider, session_id):
                return {"outcome": "ignored"}
            inserted = connection.execute(
                "insert or ignore into event values (?, ?, ?, ?, ?, ?)",
                (provider, session_id, event, detail, size, now),
            ).rowcount
            self._session(
                connection, provider, session_id, None, transcript, now, ended
            )
            agent = _match(TOKEN, payload.get("agent_id"))
            agent_transcript = transcript_path(
                provider, payload.get("agent_transcript_path")
            )
            child = f"{session_id}/agent/{agent}"
            if (
                event == "SubagentStop"
                and agent
                and agent_transcript
                and not self._forgotten(connection, provider, child)
            ):
                self._session(
                    connection, provider, child, session_id, agent_transcript, now, True
                )
        return {"outcome": "recorded" if inserted else "duplicate"}

    @staticmethod
    def _session(
        connection: sqlite3.Connection,
        provider: str,
        session_id: str,
        parent: str | None,
        transcript: str | None,
        now: str,
        ended: bool | None,
    ) -> None:
        connection.execute(
            "insert into session values (?, ?, ?, ?, ?, ?)"
            " on conflict (provider, session_id) do update set"
            " transcript_path = coalesce(excluded.transcript_path, transcript_path),"
            " ended = coalesce(?, ended)",
            (
                provider,
                session_id,
                parent,
                transcript,
                now,
                int(bool(ended)),
                None if ended is None else int(ended),
            ),
        )

    def sessions(self) -> list[dict[str, Any]]:
        with self._connect() as connection:
            rows = connection.execute(
                "select provider, session_id, parent_id, transcript_path, ended"
                " from session order by provider, session_id"
            ).fetchall()
        return [
            {
                "provider": row[0],
                "session_id": row[1],
                "parent_id": row[2],
                "transcript_path": row[3],
                "ended": bool(row[4]),
            }
            for row in rows
        ]

    def scan(self) -> dict[str, str]:
        """Advance every cursor; records and their cursor commit together."""

        return {
            f"{session['provider']}:{session['session_id']}": self._scan_file(
                session["provider"], session["session_id"], session["transcript_path"]
            )
            for session in self.sessions()
            if session["transcript_path"]
        }

    def _scan_file(self, provider: str, session_id: str, path: str) -> str:
        if transcript_path(provider, path) != path:
            return "unavailable"
        try:
            handle = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
        except OSError:
            return "unavailable"
        with os.fdopen(handle, "rb") as source:
            info = os.fstat(source.fileno())
            if not stat.S_ISREG(info.st_mode):
                return "unavailable"
            while True:
                outcome = self._scan_batch(provider, session_id, path, source, info)
                if outcome != "more":
                    return outcome

    def _scan_batch(
        self,
        provider: str,
        session_id: str,
        path: str,
        source: Any,
        info: os.stat_result,
    ) -> str:
        """One bounded transaction: re-check the session, then advance its cursor."""

        key = (provider, session_id, path)
        with self._write() as connection:
            live = connection.execute(
                "select 1 from session where provider = ? and session_id = ?",
                (provider, session_id),
            ).fetchone()
            if live is None or self._forgotten(connection, provider, session_id):
                return "forgotten"
            cursor = connection.execute(
                "select device, inode, offset, last_line_sha256, last_line_bytes,"
                " last_ordinal, ordinal_gaps, modified from cursor"
                " where provider = ? and session_id = ? and path = ?",
                key,
            ).fetchone()
            (
                device,
                inode,
                offset,
                last_sha,
                last_bytes,
                last_ordinal,
                gaps,
                modified,
            ) = cursor or (info.st_dev, info.st_ino, 0, None, None, None, 0, 0)
            rewritten = (device, inode) != (
                info.st_dev,
                info.st_ino,
            ) or info.st_size < offset
            if not rewritten and last_sha and last_bytes and offset >= last_bytes:
                source.seek(offset - last_bytes)
                rewritten = (
                    hashlib.sha256(source.read(last_bytes)).hexdigest() != last_sha
                )
            if rewritten:
                modified, offset, last_sha, last_bytes, last_ordinal = (
                    1,
                    0,
                    None,
                    None,
                    None,
                )
            source.seek(offset)
            chunk = source.read(min(info.st_size - offset, SCAN_CHUNK_LIMIT))
            lines = _lines(chunk)
            oversized = int(not lines and len(chunk) == SCAN_CHUNK_LIMIT)
            position = offset
            for line in lines:
                digest = hashlib.sha256(line).hexdigest()
                shape = describe(provider, line)
                existing = connection.execute(
                    "select sha256 from record where provider = ? and session_id = ?"
                    " and path = ? and offset = ?",
                    (*key, position),
                ).fetchone()
                if existing is None:
                    connection.execute(
                        "insert into record values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (
                            *key,
                            position,
                            len(line),
                            digest,
                            shape["kind"],
                            shape["occurred_at"],
                            shape["ordinal"],
                            shape["tool"],
                        ),
                    )
                    if (
                        shape["ordinal"] is not None
                        and last_ordinal is not None
                        and shape["ordinal"] != last_ordinal + 1
                    ):
                        gaps += 1
                elif existing[0] != digest:
                    modified = 1
                if shape["ordinal"] is not None:
                    last_ordinal = shape["ordinal"]
                position += len(line)
                last_sha, last_bytes = digest, len(line)
            at_end = offset + len(chunk) >= info.st_size
            partial = int(at_end and position < info.st_size)
            connection.execute(
                "insert or replace into cursor values"
                " (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    *key,
                    info.st_dev,
                    info.st_ino,
                    position,
                    last_sha,
                    last_bytes,
                    last_ordinal,
                    gaps,
                    partial,
                    oversized,
                    modified,
                    _now(),
                ),
            )
        return "more" if lines and not at_end else "scanned"

    def status(self, provider: str, session_id: str) -> dict[str, Any]:
        with self._connect() as connection:
            session = connection.execute(
                "select transcript_path, ended from session"
                " where provider = ? and session_id = ?",
                (provider, session_id),
            ).fetchone()
            if session is None:
                raise memory.MemoryError_("MEMORY_NOT_FOUND: unknown session")
            path, ended = session
            key = (provider, session_id, path)
            events = connection.execute(
                "select event, detail, transcript_bytes, captured_at from event"
                " where provider = ? and session_id = ? order by rowid",
                (provider, session_id),
            ).fetchall()
            cursor = connection.execute(
                "select device, inode, offset, ordinal_gaps, partial_tail,"
                " oversized_line, modified from cursor"
                " where provider = ? and session_id = ? and path = ?",
                key,
            ).fetchone()
            records = connection.execute(
                "select offset, length, sha256, kind, occurred_at, ordinal, tool"
                " from record where provider = ? and session_id = ? and path = ?"
                " order by offset",
                key,
            ).fetchall()
        current = None
        with contextlib.suppress(OSError, TypeError):
            current = os.stat(path)
        device, inode, offset, gaps, partial, oversized, modified = cursor or (
            None,
            None,
            0,
            0,
            0,
            0,
            0,
        )
        if path is None or current is None:
            completeness = "unavailable"
        elif (
            ended
            and cursor
            and (device, inode, offset)
            == (current.st_dev, current.st_ino, current.st_size)
            and not (gaps or partial or oversized or modified)
        ):
            completeness = "complete"
        else:
            completeness = "partial"
        return {
            "provider": provider,
            "session_id": session_id,
            "transcript_path": path,
            "ended": bool(ended),
            "completeness": completeness,
            "scanned_bytes": offset,
            "transcript_bytes": None if current is None else current.st_size,
            "ordinal_gaps": gaps,
            "partial_tail": bool(partial),
            "oversized_line": bool(oversized),
            "modified": bool(modified),
            "events": [
                dict(zip(("event", "detail", "transcript_bytes", "captured_at"), e))
                for e in events
            ],
            "records": [
                dict(
                    zip(
                        (
                            "offset",
                            "length",
                            "sha256",
                            "kind",
                            "occurred_at",
                            "ordinal",
                            "tool",
                        ),
                        r,
                    )
                )
                for r in records
            ],
        }

    def forget(
        self, provider: str, session_id: str, *, owner: str, approval_ref: str
    ) -> dict[str, Any]:
        """Remove one session and its sub-agents on approval; never capture them again."""

        if not isinstance(approval_ref, str) or not approval_ref.strip():
            raise memory.MemoryError_(
                "MEMORY_SCHEMA: forget needs the approval reference"
            )
        selector, values = _selector(session_id)
        keys = (provider, *values)
        with self._write() as connection:
            counts = {
                table: connection.execute(
                    f"delete from {table} where {selector}", keys
                ).rowcount
                for table in ("record", "cursor", "event", "session")
            }
            connection.execute(
                "insert or replace into forgotten values (?, ?, ?, ?, ?)",
                (provider, session_id, _now(), owner, approval_ref),
            )
        return {"provider": provider, "session_id": session_id, "removed": counts}


def checkout_root() -> Path:
    return Path(__file__).resolve().parents[1]


def run_hook(provider: str, text: str, *, root: Path | None = None) -> dict[str, str]:
    """Hook entry: only the adapter's own workspace is captured; never raises."""

    try:
        payload = json.loads(text)
        cwd = payload.get("cwd") if isinstance(payload, dict) else None
        if not isinstance(cwd, str):
            return {"outcome": "ignored"}
        expected = memory.representative_root(root or checkout_root())
        try:
            if memory.representative_root(Path(cwd)) != expected:
                return {"outcome": "ignored"}
        except memory.MemoryError_:
            return {"outcome": "ignored"}
        capture = Capture.open(expected, busy_ms=HOOK_BUSY_TIMEOUT_MS)
        return capture.hook(provider, payload)
    except Exception as exc:  # noqa: BLE001 - a capture failure must not stop the session
        return {"outcome": "failed", "error": type(exc).__name__}


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path)
    commands = parser.add_subparsers(dest="command", required=True)
    hook = commands.add_parser("hook")
    hook.add_argument("--provider", required=True, choices=sorted(PROVIDERS))
    commands.add_parser("scan")
    commands.add_parser("sessions")
    status = commands.add_parser("status")
    status.add_argument("--provider", required=True, choices=sorted(PROVIDERS))
    status.add_argument("--session", required=True)
    forget = commands.add_parser("forget")
    forget.add_argument("--provider", required=True, choices=sorted(PROVIDERS))
    forget.add_argument("--session", required=True)
    forget.add_argument("--owner", required=True)
    forget.add_argument("--approval-ref", required=True)
    args = parser.parse_args(argv)
    if args.command == "hook":
        try:
            text = sys.stdin.read(HOOK_INPUT_LIMIT)
        except (OSError, ValueError):
            return 0
        result = run_hook(args.provider, text, root=args.root)
        if result["outcome"] == "failed":
            print(f"CAPTURE_FAILED: {result['error']}", file=sys.stderr)
        return 0
    try:
        capture = Capture.open(args.root or Path.cwd())
        if args.command == "scan":
            result: Any = capture.scan()
        elif args.command == "sessions":
            result = capture.sessions()
        elif args.command == "status":
            result = capture.status(args.provider, args.session)
        else:
            result = capture.forget(
                args.provider,
                args.session,
                owner=args.owner,
                approval_ref=args.approval_ref,
            )
    except (memory.MemoryError_, OSError, sqlite3.Error) as exc:
        message = (
            str(exc)
            if isinstance(exc, memory.MemoryError_)
            else f"MEMORY_ERROR: {type(exc).__name__}"
        )
        print(message, file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
