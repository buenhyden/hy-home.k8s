#!/usr/bin/env python3
"""Local session capture for Claude and Codex sessions in this workspace (W08-CAPTURE).

Each transcript line keeps its structure: provider, session and event IDs, the
transcript path, byte offset, line digest, record kind, time, tool name,
ordinal and tool-failure flag. Q02/D10 (SPEC-0233) adds selected content in
the same transaction: the visible user prompt, the visible response and the
tool result, never hidden reasoning, tool arguments or injected meta lines.
Each value is redacted whole, then abridged, re-checked and capped in UTF-8
bytes before it is stored; a value that cannot be cleaned becomes a gap. A
turn keeps its final response and a failed tool result as selected content;
earlier responses and successful results become a bounded summary. Selected
content expires after 30 days, summaries and metadata after 90. A transcript
is read only inside the provider's own session directory. A lifecycle hook
only records one event row; `scan` reads transcripts by cursor in batches.
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

SCHEMA_VERSION = 2
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
CODEX_TOOL_OUTPUTS = frozenset({"function_call_output", "custom_tool_call_output"})
# Q02/D10 session-retention-policy 1.1.0, measured in UTF-8 bytes.
SELECTED_LIMIT = 16 * 1024
SUMMARY_TURN_LIMIT = 4 * 1024
BODY_STORE_LIMIT = 256 * 1024 * 1024
SELECTED_DAYS = 30
SUMMARY_DAYS = 90
METADATA_DAYS = 90
PARSER_EDITION = 1
REDACTION_EDITION = 1
MIN_SUMMARY = 64
# A `keep` group survives redaction; `(?!\[REDACTED)` keeps a placeholder
# from looking like a fresh secret on the re-check.
SECRETS = (
    (
        "private-key",
        r"-----BEGIN [A-Z ]*PRIVATE KEY-----[\s\S]*?(?:-----END [A-Z ]*PRIVATE KEY-----|\Z)",
    ),
    ("key", r"\b(?:sk|rk|pk)-[A-Za-z0-9_-]{16,}"),
    ("key", r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})"),
    ("key", r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"),
    ("key", r"\bxox[abprs]-[A-Za-z0-9-]{10,}"),
    ("jwt", r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}"),
    (
        "credential",
        r"(?i)(?P<keep>\b(?:authorization|bearer)\b[:=\s]+)(?!\[REDACTED)[A-Za-z0-9._~+/-]{12,}=*",
    ),
    ("credential", r"(?P<keep>://)(?!\[REDACTED)[^/\s:@]+:[^/\s@]+(?=@)"),
    (
        "credential",
        r"(?i)(?P<keep>\b(?:password|passwd|pwd|secret|token|api[_-]?key|access[_-]?key"
        r"|client[_-]?secret)[\"']?\s*[:=]\s*)(?!\[REDACTED)(?:\"[^\"\n]*\"|'[^'\n]*'|[^\s,;]+)",
    ),
    ("email", r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
)
SECRET_PATTERNS = tuple((kind, re.compile(rule)) for kind, rule in SECRETS)

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
  kind text not null, occurred_at text, ordinal integer, tool text, error integer,
  primary key (provider, session_id, path, offset));
create table if not exists content (
  provider text not null, session_id text not null, path text not null,
  offset integer not null, part integer not null, role text not null,
  selection text not null, call_id text, failure_class text, text text,
  bytes integer not null, truncated integer not null, gap text,
  turn integer not null, event_time text not null, expires_at text not null,
  editions text not null, primary key (provider, session_id, path, offset, part));
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
    """Structure of one transcript line: identifiers, times and flags, never text."""

    shape: dict[str, Any] = {
        "kind": "unparsable",
        "occurred_at": None,
        "ordinal": None,
        "tool": None,
        "error": None,
    }
    try:
        data = json.loads(line)
    except ValueError:
        return shape
    if not isinstance(data, dict):
        return shape
    shape["kind"] = _match(KIND, data.get("type")) or "other"
    shape["occurred_at"] = _match(ISO_TIME, data.get("timestamp"))
    if provider == "codex":
        payload = data.get("payload") if isinstance(data.get("payload"), dict) else {}
        if "type" in payload:
            shape["kind"] += f"/{_match(KIND, payload['type']) or 'other'}"
        if payload.get("type") in CODEX_TOOL_ITEMS:
            shape["tool"] = _match(TOOL, payload.get("name")) or "other"
        code = payload.get("exit_code")
        if payload.get("type") == "exec_command_end" and type(code) is int:
            shape["error"] = int(code != 0)
        if type(data.get("ordinal")) is int:
            shape["ordinal"] = data["ordinal"]
        return shape
    message = data.get("message") if isinstance(data.get("message"), dict) else {}
    content = message.get("content")
    for part in content if isinstance(content, list) else ():
        if not isinstance(part, dict):
            continue
        if part.get("type") == "tool_use":
            shape["tool"] = _match(TOOL, part.get("name")) or "other"
            break
        if part.get("type") == "tool_result":
            shape["error"] = int(part.get("is_error") is True)
            break
    return shape


def redact(text: str) -> str:
    """Replace every secret or personal value; the whole value, before any cut."""

    for kind, pattern in SECRET_PATTERNS:
        text = pattern.sub(
            lambda match, kind=kind: (
                (match.groupdict().get("keep") or "") + f"[REDACTED:{kind}]"
            ),
            text,
        )
    return text


def _secret_left(text: str) -> bool:
    return any(pattern.search(text) for _, pattern in SECRET_PATTERNS)


def _cut(data: bytes, size: int) -> str:
    return data[: max(0, size)].decode("utf-8", errors="ignore")


def abridge(text: str, limit: int) -> str:
    """Keep the head and tail of a redacted value within `limit` UTF-8 bytes."""

    data = text.encode("utf-8")
    if len(data) <= limit:
        return text
    marker = f"\n…[abridged {len(data)} bytes]…\n"
    room = limit - len(marker.encode("utf-8"))
    head = _cut(data, room * 2 // 3)
    tail_size = room - len(head.encode("utf-8"))
    tail = (
        data[len(data) - tail_size :].decode("utf-8", errors="ignore")
        if tail_size > 0
        else ""
    )
    return head + marker + tail


def clean(text: str, limit: int) -> tuple[str | None, bool]:
    """Redact, abridge, re-check and cap; None when the value cannot be cleaned."""

    redacted = redact(text)
    shortened = abridge(redacted, limit)
    rechecked = redact(shortened)
    if _secret_left(rechecked) or len(rechecked.encode("utf-8")) > limit:
        return None, shortened != redacted
    return rechecked, shortened != redacted


def failure_class(text: str, error: bool) -> str | None:
    """Tell a permission refusal and a hook refusal from a failed command."""

    if not error:
        return None
    if re.search(r"Permission to use .{0,400}? has been denied", text, re.S):
        return "permission_denied"
    if re.search(r"hook error|PreToolUse:|\[FAIL\] [A-Z][A-Z0-9_-]+:", text):
        return "hook_rejected"
    return "command_failed"


def _texts(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "\n".join(
            part["text"]
            for part in value
            if isinstance(part, dict) and isinstance(part.get("text"), str)
        )
    return ""


def select(provider: str, line: bytes) -> list[tuple[str, str, str | None, bool]]:
    """Visible prompt, visible response and tool result parts of one line.

    Hidden reasoning, tool arguments, developer and injected meta lines are
    never selected.
    """

    try:
        data = json.loads(line)
    except ValueError:
        return []
    if not isinstance(data, dict):
        return []
    parts: list[tuple[str, str, str | None, bool]] = []
    if provider == "codex":
        payload = data.get("payload") if isinstance(data.get("payload"), dict) else {}
        kind = payload.get("type")
        if data.get("type") == "response_item" and kind == "message":
            role = {"user": "prompt", "assistant": "response"}.get(payload.get("role"))
            for part in payload.get("content") or []:
                text = part.get("text") if isinstance(part, dict) else None
                # Injected context arrives as tagged user text, not a typed prompt.
                if (
                    role
                    and isinstance(text, str)
                    and text.strip()
                    and not (role == "prompt" and text.lstrip().startswith("<"))
                ):
                    parts.append((role, text, None, False))
        elif kind in CODEX_TOOL_OUTPUTS:
            output = payload.get("output")
            text = (
                output
                if isinstance(output, str)
                else _texts(output.get("content") if isinstance(output, dict) else None)
            )
            code = re.search(r"(?m)^Exit code: (-?\d+)", text)
            parts.append(
                (
                    "tool_result",
                    text,
                    _match(TOKEN, payload.get("call_id")),
                    bool(code and code.group(1) != "0"),
                )
            )
        return parts
    if data.get("isMeta") is True:
        return []
    message = data.get("message") if isinstance(data.get("message"), dict) else {}
    content = message.get("content")
    if data.get("type") == "user":
        if isinstance(content, str) and content.strip():
            parts.append(("prompt", content, None, False))
        for part in content if isinstance(content, list) else ():
            if not isinstance(part, dict):
                continue
            if part.get("type") == "text" and isinstance(part.get("text"), str):
                parts.append(("prompt", part["text"], None, False))
            elif part.get("type") == "tool_result":
                parts.append(
                    (
                        "tool_result",
                        _texts(part.get("content")),
                        _match(TOKEN, part.get("tool_use_id")),
                        part.get("is_error") is True,
                    )
                )
    elif data.get("type") == "assistant":
        for part in content if isinstance(content, list) else ():
            if isinstance(part, dict) and part.get("type") == "text":
                if isinstance(part.get("text"), str) and part["text"].strip():
                    parts.append(("response", part["text"], None, False))
    return parts


def _event_time(occurred_at: str | None, now: str) -> dt.datetime:
    for value in (occurred_at, now):
        with contextlib.suppress(TypeError, ValueError):
            stamp = dt.datetime.fromisoformat(value)
            return (
                stamp if stamp.tzinfo else stamp.replace(tzinfo=dt.timezone.utc)
            ).astimezone(dt.timezone.utc)
    return dt.datetime.now(dt.timezone.utc)


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
                        "insert into record values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (
                            *key,
                            position,
                            len(line),
                            digest,
                            shape["kind"],
                            shape["occurred_at"],
                            shape["ordinal"],
                            shape["tool"],
                            shape["error"],
                        ),
                    )
                    self._store_content(
                        connection, key, position, line, shape["occurred_at"]
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

    def _store_content(
        self,
        connection: sqlite3.Connection,
        key: tuple[str, str, str],
        offset: int,
        line: bytes,
        occurred_at: str | None,
    ) -> None:
        """Select, redact, abridge, re-check, cap and store one line's content."""

        provider = key[0]
        now = _now()
        when = _event_time(occurred_at, now)
        editions = json.dumps(
            {"parser": PARSER_EDITION, "redaction": REDACTION_EDITION},
            sort_keys=True,
        )
        where = "provider = ? and session_id = ? and path = ?"
        for part, (role, raw, call_id, error) in enumerate(select(provider, line)):
            turn = (
                offset
                if role == "prompt"
                else connection.execute(
                    f"select coalesce(max(offset), 0) from content where {where}"
                    " and role = 'prompt' and offset < ?",
                    (*key, offset),
                ).fetchone()[0]
            )
            redacted = redact(raw)
            failure = failure_class(redacted, error)

            def spent() -> int:
                return connection.execute(
                    f"select coalesce(sum(bytes), 0) from content where {where}"
                    " and turn = ? and selection = 'summary'",
                    (*key, turn),
                ).fetchone()[0]

            if role == "response":
                # A later response makes the earlier one of the turn a summary.
                for row_offset, row_part, text in connection.execute(
                    f"select offset, part, text from content where {where} and turn = ?"
                    " and role = 'response' and selection = 'selected'",
                    (*key, turn),
                ).fetchall():
                    room = SUMMARY_TURN_LIMIT - spent()
                    short, cut = (
                        clean(text, room) if room >= MIN_SUMMARY else (None, True)
                    )
                    connection.execute(
                        f"update content set selection = ?, text = ?, bytes = ?,"
                        " truncated = max(truncated, ?), gap = ?, expires_at = ?"
                        f" where {where} and offset = ? and part = ?",
                        (
                            "summary" if short is not None else "gap",
                            short,
                            len(short.encode("utf-8")) if short is not None else 0,
                            int(cut),
                            None if short is not None else "summary_cap",
                            _iso_days(when, SUMMARY_DAYS),
                            *key,
                            row_offset,
                            row_part,
                        ),
                    )
            summary = role == "tool_result" and not error
            limit = SUMMARY_TURN_LIMIT - spent() if summary else SELECTED_LIMIT
            text, truncated = (
                clean(raw, limit) if limit >= MIN_SUMMARY else (None, True)
            )
            gap = None
            if text is None:
                gap = "summary_cap" if summary and limit < MIN_SUMMARY else "redaction"
            elif (
                self._body_bytes(connection, now) + len(text.encode("utf-8"))
                > BODY_STORE_LIMIT
            ):
                text, gap = None, "capacity"
            selection = "gap" if gap else ("summary" if summary else "selected")
            days = SELECTED_DAYS if selection == "selected" else SUMMARY_DAYS
            connection.execute(
                "insert or ignore into content values"
                " (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    *key,
                    offset,
                    part,
                    role,
                    selection,
                    call_id,
                    failure,
                    text,
                    len(text.encode("utf-8")) if text is not None else 0,
                    int(truncated),
                    gap,
                    turn,
                    when.isoformat(timespec="seconds"),
                    _iso_days(when, days),
                    editions,
                ),
            )

    @staticmethod
    def _body_bytes(connection: sqlite3.Connection, now: str) -> int:
        # Capacity pressure first drops expired content (D10).
        connection.execute("delete from content where expires_at <= ?", (now,))
        return connection.execute(
            "select coalesce(sum(bytes), 0) from content"
        ).fetchone()[0]

    def contents(self, provider: str, session_id: str) -> list[dict[str, Any]]:
        """Stored content of one session, oldest first; data, never instructions."""

        columns = (
            "offset",
            "part",
            "role",
            "selection",
            "call_id",
            "failure_class",
            "text",
            "bytes",
            "truncated",
            "gap",
            "turn",
            "event_time",
            "expires_at",
        )
        with self._connect() as connection:
            rows = connection.execute(
                f"select {', '.join(columns)} from content"
                " where provider = ? and session_id = ? order by offset, part",
                (provider, session_id),
            ).fetchall()
        return [dict(zip(columns, row)) | {"truncated": bool(row[8])} for row in rows]

    def expire(self, *, now: dt.datetime | None = None) -> dict[str, int]:
        """Drop expired content; drop sessions whose metadata passed 90 days.

        Cursors stay, so a later scan cannot store the expired lines again.
        """

        now = now or dt.datetime.now(dt.timezone.utc)
        stamp = now.isoformat(timespec="seconds")
        cutoff = (now - dt.timedelta(days=METADATA_DAYS)).isoformat(timespec="seconds")
        with self._write() as connection:
            removed = {
                "content": connection.execute(
                    "delete from content where expires_at <= ?", (stamp,)
                ).rowcount
            }
            old = connection.execute(
                "select provider, session_id from session where first_seen <= ?",
                (cutoff,),
            ).fetchall()
            sessions = 0
            for provider, session_id in old:
                for table in ("content", "record", "event", "session"):
                    connection.execute(
                        f"delete from {table} where provider = ? and session_id = ?",
                        (provider, session_id),
                    )
                sessions += 1
            removed["sessions"] = sessions
        return removed

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
                "select r.offset, r.length, r.sha256, r.kind, r.occurred_at, r.ordinal,"
                " r.tool, r.error, c.failure_class, c.call_id from record r"
                " left join content c on c.provider = r.provider"
                " and c.session_id = r.session_id and c.path = r.path"
                " and c.offset = r.offset and c.role = 'tool_result' and c.part = 0"
                " where r.provider = ? and r.session_id = ? and r.path = ?"
                " order by r.offset",
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
                            "error",
                            "failure_class",
                            "call_id",
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
                for table in ("content", "record", "cursor", "event", "session")
            }
            connection.execute(
                "insert or replace into forgotten values (?, ?, ?, ?, ?)",
                (provider, session_id, _now(), owner, approval_ref),
            )
        return {"provider": provider, "session_id": session_id, "removed": counts}


def _iso_days(when: dt.datetime, days: int) -> str:
    return (when + dt.timedelta(days=days)).isoformat(timespec="seconds")


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
    commands.add_parser("expire")
    contents = commands.add_parser("contents")
    contents.add_argument("--provider", required=True, choices=sorted(PROVIDERS))
    contents.add_argument("--session", required=True)
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
        elif args.command == "expire":
            result = capture.expire()
        elif args.command == "contents":
            result = capture.contents(args.provider, args.session)
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
