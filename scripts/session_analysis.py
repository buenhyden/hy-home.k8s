#!/usr/bin/env python3
"""Scheduled, deterministic analysis of the local session capture (W08-ANALYSIS).

A run scans the capture archive, then analyzes each Asia/Seoul day up to
yesterday whose input changed since its last analysis, so a missed day is
caught up and an unchanged one is never analyzed twice. One lease with a
fencing token admits one writer; a busy store is retried a bounded number of
times; cancellation and failure are recorded and release the lease. Rules turn
counts into improvement candidates with fixed wording: no transcript text and
no model call, so the cost is a known zero. A candidate is only a proposal; it
reaches memory or a Task only after review, and never changes a policy, skill,
check or the analyzer itself.
"""

from __future__ import annotations

import argparse
import contextlib
import datetime as dt
import hashlib
import json
import os
import signal
import sqlite3
import subprocess
import sys
import threading
import time
import uuid
from pathlib import Path
from typing import Any, Iterator, Sequence
from zoneinfo import ZoneInfo

import session_capture as capture
import workspace_memory as memory

SCHEMA_VERSION = 1
RULES_EDITION = 1
STATE_NAME = "analysis.sqlite3"
ZONE = ZoneInfo("Asia/Seoul")
LEASE_TTL = dt.timedelta(minutes=15)
ATTEMPTS = 3
BACKOFF_SECONDS = (5, 15)
FAILURE_THRESHOLD = 3
COMPACTION_THRESHOLD = 2
SOURCE_REF_LIMIT = 20
UNIT_NAME = "hy-home-k8s-session-analysis"

SCHEMA = """
create table if not exists meta (key text primary key, value text not null);
create table if not exists lease (
  name text primary key, holder text not null, token integer not null,
  expires_at text not null);
create table if not exists run (
  run_id integer primary key, trigger text not null, started_at text not null,
  finished_at text, state text not null, attempts integer not null,
  windows text not null, token integer, error text, backend text not null,
  cost_usd real);
create table if not exists window (
  window text primary key, watermark text not null, rules_edition integer not null,
  analyzed_at text not null, run_id integer not null);
create table if not exists candidate (
  candidate_id integer primary key, window text not null, pattern text not null,
  subject text not null, problem text not null, source_refs text not null,
  frequency integer not null, condition text not null, proposal text not null,
  risk text not null, acceptance_test text not null, decision text not null,
  reviewer text, reviewed_at text, promoted_to text, promoted_ref text,
  unique (window, pattern, subject));
create table if not exists recheck (
  candidate_id integer not null, window text not null, outcome text not null,
  frequency integer not null, sessions integer not null, observed_at text not null,
  primary key (candidate_id, window));
"""

RULES = {
    "repeated-tool-failure": {
        "problem": "Tool results failed {n} times in one day.",
        "condition": "At least {threshold} failed tool results on {window}.",
        "proposal": "Find the shared cause of these failures and record its fix as reviewed memory or a Task change.",
        "risk": "Unrelated failures can share a tool; counts alone do not prove one cause.",
        "acceptance_test": "A comparable later day shows fewer than {threshold} failed tool results.",
    },
    "session-without-end": {
        "problem": "{n} session(s) started on {window} had recorded no end when the day was analyzed.",
        "condition": "A session start without a session end by the analysis after its day.",
        "proposal": "Check whether these sessions were cancelled, crashed or ran where the end hook is not delivered.",
        "risk": "A session can legitimately stay open; the end hook is advisory.",
        "acceptance_test": "Later days record an end for each started session or explain its absence.",
    },
    "capture-incomplete": {
        "problem": "{n} ended session(s) on {window} were captured incompletely.",
        "condition": "An ended session whose capture is partial or unavailable.",
        "proposal": "Inspect the capture status of these sessions for gaps, rewrites or missing transcripts.",
        "risk": "A transcript written after the scan reads as partial until the next scan.",
        "acceptance_test": "A rescan reports these sessions complete, or the cause is recorded.",
    },
    "frequent-compaction": {
        "problem": "{n} session(s) on {window} compacted at least {threshold} times.",
        "condition": "At least {threshold} compaction events in one session.",
        "proposal": "Review whether these tasks load more context than needed and split or narrow them.",
        "risk": "Long tasks compact by design; frequency alone is not a defect.",
        "acceptance_test": "Comparable later tasks compact fewer times.",
    },
}


class AnalysisError(Exception):
    """A stable analysis diagnostic: CODE: detail."""


class Cancelled(Exception):
    """The run was cancelled by a signal."""


def _iso(moment: dt.datetime) -> str:
    return moment.astimezone(dt.timezone.utc).isoformat(timespec="seconds")


def _day(stamp: str) -> dt.date:
    return dt.datetime.fromisoformat(stamp).astimezone(ZONE).date()


class Analysis:
    def __init__(self, path: Path, root: Path):
        self.path = path
        self.root = root

    @classmethod
    def open(cls, cwd: Path) -> "Analysis":
        store = memory.Store.open(cwd)
        analysis = cls(store.path.parent / STATE_NAME, store.root)
        if analysis.path.is_symlink():
            raise AnalysisError("ANALYSIS_UNAVAILABLE: state path is linked")
        with analysis._connect() as connection:
            connection.executescript(SCHEMA)
            connection.execute(
                "insert or ignore into meta values ('schema_version', ?)",
                (str(SCHEMA_VERSION),),
            )
            version = connection.execute(
                "select value from meta where key = 'schema_version'"
            ).fetchone()
        if version != (str(SCHEMA_VERSION),):
            raise AnalysisError("ANALYSIS_UNAVAILABLE: state schema differs")
        return analysis

    @contextlib.contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(self.path, isolation_level=None)
        try:
            connection.execute("pragma busy_timeout=5000")
            if (
                connection.execute("pragma journal_mode=delete").fetchone()[0]
                != "delete"
            ):
                raise AnalysisError(
                    "ANALYSIS_UNAVAILABLE: rollback journal is unavailable"
                )
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

    def acquire(self, holder: str, *, now: dt.datetime) -> int | None:
        """Take the lease if it is free or expired; return the new fencing token."""

        with self._write() as connection:
            row = connection.execute(
                "select holder, token, expires_at from lease where name = 'analysis'"
            ).fetchone()
            held = row and row[0] and row[0] != holder
            if held and dt.datetime.fromisoformat(row[2]) > now:
                return None
            token = (row[1] if row else 0) + 1
            connection.execute(
                "insert or replace into lease values ('analysis', ?, ?, ?)",
                (holder, token, _iso(now + LEASE_TTL)),
            )
        return token

    def check_token(
        self, token: int, connection: sqlite3.Connection | None = None
    ) -> None:
        with contextlib.ExitStack() as stack:
            if connection is None:
                connection = stack.enter_context(self._connect())
            row = connection.execute(
                "select token from lease where name = 'analysis'"
            ).fetchone()
        if row is None or row[0] != token:
            raise AnalysisError("ANALYSIS_FENCED: another run holds a newer lease")

    def release(self, token: int) -> None:
        with self._write() as connection:
            # Keep the row so the next token stays larger than every earlier one.
            connection.execute(
                "update lease set holder = '', expires_at = ?"
                " where name = 'analysis' and token = ?",
                (_iso(dt.datetime.fromtimestamp(0, dt.timezone.utc)), token),
            )

    def run(self, *, trigger: str, now: dt.datetime | None = None) -> dict[str, Any]:
        now = now or dt.datetime.now(dt.timezone.utc)
        holder = f"{os.getpid()}-{uuid.uuid4().hex[:8]}"
        token = self.acquire(holder, now=now)
        attempts, windows, error, state = 0, [], None, "failed"
        try:
            with self._write() as connection:
                if token is not None:
                    connection.execute(
                        "update run set state = 'abandoned', finished_at = ?"
                        " where state = 'running' and token < ?",
                        (_iso(now), token),
                    )
                run_id = connection.execute(
                    "insert into run (trigger, started_at, state, attempts, windows,"
                    " token, backend, cost_usd)"
                    " values (?, ?, ?, 0, '[]', ?, 'deterministic', 0)",
                    (trigger, _iso(now), "running" if token else "busy", token),
                ).lastrowid
            if token is None:
                return self._finish(run_id, "busy", 0, [], None, now)
            try:
                while attempts < ATTEMPTS:
                    attempts += 1
                    _check_cancel()
                    try:
                        self._analyze(run_id, token, now, windows)
                        state = "completed"
                        break
                    except sqlite3.OperationalError as exc:
                        error = f"{type(exc).__name__}: {exc}"
                        if attempts < ATTEMPTS:
                            time.sleep(
                                BACKOFF_SECONDS[
                                    min(attempts - 1, len(BACKOFF_SECONDS) - 1)
                                ]
                            )
            except Cancelled:
                state, error = "cancelled", "cancelled by signal"
            except (AnalysisError, memory.MemoryError_) as exc:
                error = str(exc)
            except Exception as exc:  # noqa: BLE001 - every failure must end the run row
                error = f"{type(exc).__name__}: {exc}"
            if state == "completed":
                error = None
            return self._finish(run_id, state, attempts, windows, error, now)
        finally:
            if token is not None:
                with contextlib.suppress(sqlite3.Error):
                    self.release(token)

    def _finish(
        self,
        run_id: int,
        state: str,
        attempts: int,
        windows: list[str],
        error: str | None,
        now: dt.datetime,
    ) -> dict[str, Any]:
        with self._write() as connection:
            connection.execute(
                "update run set state = ?, attempts = ?, windows = ?, error = ?,"
                " finished_at = ? where run_id = ? and state in ('running', 'busy')",
                (state, attempts, json.dumps(windows), error, _iso(now), run_id),
            )
        return {
            "run_id": run_id,
            "state": state,
            "attempts": attempts,
            "windows": windows,
            "error": error,
            "backend": "deterministic",
            "cost_usd": 0,
        }

    def _analyze(
        self, run_id: int, token: int, now: dt.datetime, analyzed: list[str]
    ) -> None:
        archive = capture.Capture.open(self.root)
        archive.scan()
        sessions = self._sessions(archive)
        last = now.astimezone(ZONE).date() - dt.timedelta(days=1)
        with self._connect() as connection:
            done = dict(
                connection.execute(
                    "select window, watermark from window where rules_edition = ?",
                    (RULES_EDITION,),
                ).fetchall()
            )
        # A day stays in range after its sessions are forgotten, so it is reanalyzed.
        days = sorted(
            {s["day"] for s in sessions} | {dt.date.fromisoformat(w) for w in done}
        )
        if not days or days[0] > last:
            return
        live = {f"{s['provider']}:{s['session_id']}" for s in sessions}
        day = days[0]
        while day <= last:
            _check_cancel()
            window = day.isoformat()
            members = [s for s in sessions if s["day"] == day]
            watermark = hashlib.sha256(
                json.dumps(
                    [
                        (
                            s["provider"],
                            s["session_id"],
                            s["events"],
                            s["records"],
                            s["status"]["ended"],
                            s["status"]["completeness"],
                        )
                        for s in members
                    ]
                ).encode()
            ).hexdigest()
            if done.get(window) != watermark:
                found = self._analyze_window(window, members, now)
                with self._write() as connection:
                    self.check_token(token, connection)
                    connection.execute(
                        "delete from candidate where window = ?"
                        " and decision = 'proposed' and promoted_to is null",
                        (window,),
                    )
                    for item in found:
                        connection.execute(
                            "insert into candidate (window, pattern, subject, problem,"
                            " source_refs, frequency, condition, proposal, risk,"
                            " acceptance_test, decision) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'proposed')"
                            " on conflict (window, pattern, subject) do update set"
                            " problem = excluded.problem, source_refs = excluded.source_refs,"
                            " frequency = excluded.frequency, condition = excluded.condition,"
                            " proposal = excluded.proposal, risk = excluded.risk,"
                            " acceptance_test = excluded.acceptance_test",
                            (
                                window,
                                item["pattern"],
                                item["subject"],
                                item["problem"],
                                json.dumps(item["source_refs"]),
                                item["frequency"],
                                item["condition"],
                                item["proposal"],
                                item["risk"],
                                item["acceptance_test"],
                            ),
                        )
                    self._recheck(connection, window, members, found, now)
                    for identifier, refs in connection.execute(
                        "select candidate_id, source_refs from candidate where window = ?",
                        (window,),
                    ).fetchall():
                        kept = [
                            ref
                            for ref in json.loads(refs)
                            if any(ref == k or ref.startswith(k + ":") for k in live)
                        ]
                        connection.execute(
                            "update candidate set source_refs = ? where candidate_id = ?",
                            (json.dumps(kept), identifier),
                        )
                    connection.execute(
                        "insert or replace into window values (?, ?, ?, ?, ?)",
                        (window, watermark, RULES_EDITION, _iso(now), run_id),
                    )
                if window not in analyzed:
                    analyzed.append(window)
            day += dt.timedelta(days=1)
        return

    @staticmethod
    def _sessions(archive: Any) -> list[dict[str, Any]]:
        """Each captured session with its first-event day and structural counts."""

        with archive._connect() as connection:
            rows = connection.execute(
                "select provider, session_id, min(captured_at), count(*),"
                " sum(event = 'PreCompact') from event group by provider, session_id"
            ).fetchall()
        sessions = []
        for provider, session_id, first, events, compactions in rows:
            status = archive.status(provider, session_id)
            sessions.append(
                {
                    "provider": provider,
                    "session_id": session_id,
                    "day": _day(first),
                    "started": dt.datetime.fromisoformat(first),
                    "events": events,
                    "compactions": compactions or 0,
                    "records": len(status["records"]),
                    "status": status,
                }
            )
        return sessions

    @staticmethod
    def _measure(members: list[dict[str, Any]]) -> dict[str, list[str]]:
        """Every pattern's matching refs for one day, matched or not."""
        # A failed result is not tied to its tool call here, so failures are counted
        # for the day as a whole rather than attributed to one tool.
        return {
            "repeated-tool-failure": [
                f"{session['provider']}:{session['session_id']}:{record['offset']}"
                for session in members
                for record in session["status"]["records"]
                if record["error"] == 1
            ],
            "session-without-end": [
                f"{s['provider']}:{s['session_id']}"
                for s in members
                if not s["status"]["ended"]
            ],
            "capture-incomplete": [
                f"{s['provider']}:{s['session_id']}"
                for s in members
                if s["status"]["ended"] and s["status"]["completeness"] != "complete"
            ],
            "frequent-compaction": [
                f"{s['provider']}:{s['session_id']}"
                for s in members
                if s["compactions"] >= COMPACTION_THRESHOLD
            ],
        }

    def _analyze_window(
        self, window: str, members: list[dict[str, Any]], now: dt.datetime
    ) -> list[dict[str, Any]]:
        found = []
        for pattern, refs in self._measure(members).items():
            subject = "tools" if pattern == "repeated-tool-failure" else "sessions"
            limit = FAILURE_THRESHOLD if subject == "tools" else 1
            if len(refs) >= limit:
                found.append(self._candidate(pattern, window, subject, refs))
        return found

    @staticmethod
    def _recheck(connection, window, members, found, now) -> None:
        """Test each accepted candidate's acceptance on a later day that has sessions.

        This is the re-evaluation step of the improvement loop. A day records
        `recurred` when the pattern shows up again; `met` only when it stays
        below its condition on at least as many sessions as the candidate's own
        evidence named; otherwise the day was too thin and is `inconclusive`.
        A reanalyzed day replaces its rechecks, so a day that lost its sessions
        keeps none.
        """
        connection.execute("delete from recheck where window = ?", (window,))
        if not members:
            return
        seen = {(item["pattern"], item["subject"]) for item in found}
        measured = Analysis._measure(members)
        day = dt.date.fromisoformat(window)
        for identifier, pattern, subject, reviewed_at, refs in connection.execute(
            "select candidate_id, pattern, subject, reviewed_at, source_refs"
            " from candidate where decision = 'accepted' and window < ?",
            (window,),
        ).fetchall():
            if reviewed_at is None or _day(reviewed_at) >= day:
                continue
            floor = len({":".join(ref.split(":")[:2]) for ref in json.loads(refs)})
            if (pattern, subject) in seen:
                outcome = "recurred"
            elif len(members) >= max(1, floor):
                outcome = "met"
            else:
                outcome = "inconclusive"
            connection.execute(
                "insert into recheck values (?, ?, ?, ?, ?, ?)",
                (
                    identifier,
                    window,
                    outcome,
                    len(measured.get(pattern, [])),
                    len(members),
                    _iso(now),
                ),
            )

    @staticmethod
    def _candidate(
        pattern: str, window: str, subject: str, refs: list[str]
    ) -> dict[str, Any]:
        values = {
            "n": len(refs),
            "subject": subject,
            "window": window,
            "threshold": FAILURE_THRESHOLD
            if pattern == "repeated-tool-failure"
            else COMPACTION_THRESHOLD,
        }
        text = {key: value.format(**values) for key, value in RULES[pattern].items()}
        return {
            "pattern": pattern,
            "subject": subject,
            "frequency": len(refs),
            "source_refs": refs[:SOURCE_REF_LIMIT],
            **text,
        }

    def candidates(self) -> list[dict[str, Any]]:
        with self._connect() as connection:
            connection.row_factory = sqlite3.Row
            rows = connection.execute(
                "select * from candidate order by window, pattern, subject"
            ).fetchall()
            checks: dict[int, list[dict[str, Any]]] = {}
            for check in connection.execute(
                "select * from recheck order by window"
            ).fetchall():
                checks.setdefault(check["candidate_id"], []).append(
                    {
                        k: check[k]
                        for k in ("window", "outcome", "frequency", "sessions")
                    }
                )
        result = []
        for row in rows:
            rechecks = checks.get(row["candidate_id"], [])
            outcomes = {check["outcome"] for check in rechecks}
            result.append(
                dict(row)
                | {
                    "source_refs": json.loads(row["source_refs"]),
                    "rechecks": rechecks,
                    # A recurrence is never hidden by a later met day; unverified
                    # until a later comparable day is observed.
                    "acceptance": "recurred"
                    if "recurred" in outcomes
                    else "met"
                    if "met" in outcomes
                    else "unverified",
                }
            )
        return result

    def status(self) -> dict[str, Any]:
        with self._connect() as connection:
            connection.row_factory = sqlite3.Row
            last = connection.execute(
                "select * from run order by run_id desc limit 1"
            ).fetchone()
            lease = connection.execute("select * from lease").fetchone()
        return {
            "last_run": dict(last) if last else None,
            "lease": dict(lease) if lease else None,
        }

    def review(
        self,
        candidate_id: int,
        *,
        decision: str,
        owner: str,
        now: dt.datetime | None = None,
    ) -> dict[str, Any]:
        if decision not in ("accepted", "rejected"):
            raise AnalysisError("ANALYSIS_SCHEMA: decision is accepted or rejected")
        with self._write() as connection:
            row = connection.execute(
                "select promoted_to from candidate where candidate_id = ?",
                (candidate_id,),
            ).fetchone()
            if row is not None and row[0] is not None:
                raise AnalysisError("ANALYSIS_PROMOTED: a promoted candidate is final")
            changed = connection.execute(
                "update candidate set decision = ?, reviewer = ?, reviewed_at = ?"
                " where candidate_id = ?",
                (
                    decision,
                    owner,
                    _iso(now or dt.datetime.now(dt.timezone.utc)),
                    candidate_id,
                ),
            ).rowcount
        if not changed:
            raise AnalysisError("ANALYSIS_NOT_FOUND: unknown candidate")
        return {"candidate_id": candidate_id, "decision": decision}

    def promote(
        self, candidate_id: int, *, to: str, owner: str, ref: str | None = None
    ) -> dict[str, Any]:
        """An accepted candidate becomes a memory candidate or a Task reference."""

        with self._connect() as connection:
            connection.row_factory = sqlite3.Row
            row = connection.execute(
                "select * from candidate where candidate_id = ?", (candidate_id,)
            ).fetchone()
        if row is None:
            raise AnalysisError("ANALYSIS_NOT_FOUND: unknown candidate")
        if row["decision"] != "accepted":
            raise AnalysisError("ANALYSIS_NOT_ACCEPTED: review the candidate first")
        if row["promoted_to"] is not None:
            raise AnalysisError("ANALYSIS_PROMOTED: the candidate is already promoted")
        if to == "memory":
            written = memory.Store.open(self.root).write(
                tier="short-term",
                owner=owner,
                body={
                    "context": row["problem"],
                    "narrative": f"{row['proposal']} Acceptance: {row['acceptance_test']}",
                },
                idempotency_key=f"session-analysis-{candidate_id}",
            )
            target = written["memory_id"]
        elif to == "task" and isinstance(ref, str) and ref.strip():
            target = ref
        else:
            raise AnalysisError(
                "ANALYSIS_SCHEMA: promote to memory, or to task with a ref"
            )
        with self._write() as connection:
            connection.execute(
                "update candidate set promoted_to = ?, promoted_ref = ? where candidate_id = ?",
                (to, target, candidate_id),
            )
        result = {
            "candidate_id": candidate_id,
            "promoted_to": to,
            "promoted_ref": target,
        }
        return result | ({"memory_id": target} if to == "memory" else {})


def unit_text(root: Path) -> tuple[str, str]:
    """Timer and service text; paths are quoted and `%` is escaped for systemd."""

    def escape(value: object) -> str:
        return str(value).replace("%", "%%")

    script = escape((root / "scripts" / "session_analysis.py").resolve())
    python = escape(
        Path("/usr/bin/python3")
        if Path("/usr/bin/python3").exists()
        else sys.executable
    )
    timer = f"""[Unit]
Description=Daily session analysis for {escape(root)}

[Timer]
OnCalendar=*-*-* 03:00:00 Asia/Seoul
Persistent=true
AccuracySec=1min

[Install]
WantedBy=timers.target
"""
    service = f"""[Unit]
Description=Session analysis for {escape(root)}

[Service]
Type=oneshot
WorkingDirectory={escape(root)}
ExecStart="{python}" "{script}" run --trigger scheduled
TimeoutStartSec=600
Nice=10
"""
    return timer, service


def install_timer(root: Path) -> dict[str, Any]:
    directory = Path.home() / ".config" / "systemd" / "user"
    directory.mkdir(parents=True, exist_ok=True)
    timer, service = unit_text(root)
    (directory / f"{UNIT_NAME}.timer").write_text(timer, encoding="utf-8")
    (directory / f"{UNIT_NAME}.service").write_text(service, encoding="utf-8")
    for command in (
        ["systemctl", "--user", "daemon-reload"],
        ["systemctl", "--user", "enable", "--now", f"{UNIT_NAME}.timer"],
    ):
        subprocess.run(command, check=True, capture_output=True, text=True, timeout=30)
    return {"timer": f"{UNIT_NAME}.timer", "directory": str(directory)}


CANCEL = threading.Event()


def request_cancel(signum: int, frame: Any) -> None:
    """Signal handler: only request cancellation; the run stops at a safe point."""

    CANCEL.set()


def _check_cancel() -> None:
    if CANCEL.is_set():
        raise Cancelled()


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    commands = parser.add_subparsers(dest="command", required=True)
    run = commands.add_parser("run")
    run.add_argument("--trigger", choices=("scheduled", "manual"), default="manual")
    commands.add_parser("status")
    commands.add_parser("candidates")
    review = commands.add_parser("review")
    review.add_argument("candidate_id", type=int)
    review.add_argument("--decision", required=True)
    review.add_argument("--owner", required=True)
    promote = commands.add_parser("promote")
    promote.add_argument("candidate_id", type=int)
    promote.add_argument("--to", required=True, choices=("memory", "task"))
    promote.add_argument("--owner", required=True)
    promote.add_argument("--ref")
    commands.add_parser("units")
    commands.add_parser("install-timer")
    args = parser.parse_args(argv)
    try:
        if args.command == "units":
            print("\n".join(unit_text(memory.Store.open(args.root).root)))
            return 0
        if args.command == "install-timer":
            result: Any = install_timer(memory.Store.open(args.root).root)
        else:
            analysis = Analysis.open(args.root)
            if args.command == "run":
                for signum in (signal.SIGTERM, signal.SIGINT):
                    signal.signal(signum, request_cancel)
                result = analysis.run(trigger=args.trigger)
            elif args.command == "status":
                result = analysis.status()
            elif args.command == "candidates":
                result = analysis.candidates()
            elif args.command == "review":
                result = analysis.review(
                    args.candidate_id, decision=args.decision, owner=args.owner
                )
            else:
                result = analysis.promote(
                    args.candidate_id, to=args.to, owner=args.owner, ref=args.ref
                )
    except (
        AnalysisError,
        memory.MemoryError_,
        OSError,
        sqlite3.Error,
        subprocess.SubprocessError,
    ) as exc:
        message = (
            str(exc)
            if isinstance(exc, (AnalysisError, memory.MemoryError_))
            else f"ANALYSIS_ERROR: {type(exc).__name__}"
        )
        print(message, file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if isinstance(result, dict) and result.get("state") == "failed" else 0


if __name__ == "__main__":
    raise SystemExit(main())
