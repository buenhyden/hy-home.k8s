#!/usr/bin/env python3
"""Local P30/P50/P80 work forecasts fixed before a run and scored after (W10-FORECAST).

A forecast is recorded with the tool's own clock and must precede the start it
is scored against; the start itself is the caller's declaration, so a record
made after the work is visible in the Task that cites it. Numbers are never
rewritten: only an unstarted forecast may be superseded, by a new revision for
the same task reference, and the store refuses updates, deletes and replacing
inserts. Each row carries a digest chained to its forecast, and every read
recomputes it, so an edit made around the triggers is detected; an account that
can write the file can still forge rows, so the Task cites the digest in Git.

A run's start and outcome are recorded once with a clock that may not go
backwards. An elapsed actual comes from the clock; an active actual is
self-reported and bounded by the elapsed time. Verification, runner wait and
user wait stay separate. A cancelled, failed or incomplete run is censored, and
the score counts it, unstarted forecasts, open runs and superseded revisions per
task type, time basis and unit beside the coverage and pinball loss of the
completed runs and their N. The tool never labels a forecast calibrated, never
sums quantiles, and is no approval, deadline or timeout. Tokens and cost stay
null unless observed. Claude and Codex share one store per workspace under
`.workspace-memory/`, which Git ignores.
"""

from __future__ import annotations

import argparse
import contextlib
import datetime as dt
import hashlib
import json
import math
import re
import sqlite3
import sys
from collections import Counter, defaultdict
from pathlib import Path
from statistics import fmean
from typing import Any, Callable, Iterator

STORE_DIR = ".workspace-memory"
STORE_NAME = "forecast.sqlite3"
QUANTILES = {"p30": 0.3, "p50": 0.5, "p80": 0.8}
TIME_BASES = ("active", "elapsed")
UNITS = {"seconds": 1, "minutes": 60, "hours": 3600}
OUTCOMES = ("completed", "cancelled", "failed", "incomplete")
TASK_TYPE = re.compile(r"[a-z0-9][a-z0-9-]{0,62}")
TEXT_LIMIT = 2000
FORECAST_COLUMNS = (
    "id",
    "task_ref",
    "task_type",
    "time_basis",
    "unit",
    "p30",
    "p50",
    "p80",
    "start_def",
    "end_def",
    "reference_class",
    "assumptions",
    "risks",
    "sample_size",
    "confidence",
    "revision",
    "supersedes",
    "forecasted_at",
)
OUTCOME_COLUMNS = (
    "forecast_id",
    "finished_at",
    "outcome",
    "actual",
    "verify",
    "runner_wait",
    "user_wait",
    "tokens",
    "cost",
)

SCHEMA = """
create table if not exists forecast (
  id integer primary key,
  task_ref text not null,
  task_type text not null,
  time_basis text not null,
  unit text not null,
  p30 real not null,
  p50 real not null,
  p80 real not null,
  start_def text not null,
  end_def text not null,
  reference_class text not null,
  assumptions text not null,
  risks text not null,
  sample_size integer not null,
  confidence text not null,
  revision integer not null,
  supersedes integer unique references forecast(id),
  forecasted_at text not null,
  digest text not null
);
create table if not exists start (
  forecast_id integer primary key references forecast(id),
  started_at text not null,
  digest text not null
);
create table if not exists outcome (
  forecast_id integer primary key references start(forecast_id),
  finished_at text not null,
  outcome text not null,
  actual real,
  verify real,
  runner_wait real,
  user_wait real,
  tokens integer,
  cost real,
  digest text not null
);
"""
# Rows are append-only: no update, no delete, and no insert over an existing
# key, which `insert or replace` would otherwise turn into a silent rewrite.
SCHEMA += "".join(
    f"create trigger if not exists {table}_no_{op} before {op} on {table} "
    f"begin select raise(abort, 'FORECAST_STATE: {table} rows are immutable'); end;\n"
    for table in ("forecast", "start", "outcome")
    for op in ("update", "delete")
)
SCHEMA += "".join(
    f"create trigger if not exists {table}_no_replace before insert on {table} "
    f"when exists(select 1 from {table} where {key} = new.{key}) "
    f"begin select raise(abort, 'FORECAST_STATE: {table} rows are immutable'); end;\n"
    for table, key in (
        ("forecast", "id"),
        ("start", "forecast_id"),
        ("outcome", "forecast_id"),
    )
)


class ForecastError(ValueError):
    """A refused forecast operation; the message starts with its code."""


def _utc_now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def _digest(*parts: object) -> str:
    return hashlib.sha256(json.dumps(parts, sort_keys=True).encode()).hexdigest()


def _text(name: str, value: object) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > TEXT_LIMIT:
        raise ForecastError(f"FORECAST_FIELD: {name} needs bounded non-empty text")
    return value.strip()


def _amount(name: str, value: object, code: str = "FORECAST_ACTUAL") -> float | None:
    if value is None:
        return None
    if (
        isinstance(value, bool)
        or not isinstance(value, (int, float))
        or not math.isfinite(value)
        or value < 0
    ):
        raise ForecastError(f"{code}: {name} must be a finite non-negative number")
    return float(value)


class Forecasts:
    def __init__(self, path: Path, clock: Callable[[], dt.datetime] = _utc_now) -> None:
        self.path = path
        self.clock = clock
        if path.is_symlink() or path.parent.is_symlink():
            raise ForecastError("FORECAST_STORE: the store path is linked")
        path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        with self._connect() as connection:
            connection.executescript(SCHEMA)

    @contextlib.contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(self.path, isolation_level=None)
        connection.row_factory = sqlite3.Row
        try:
            connection.execute("pragma busy_timeout=5000")
            connection.execute("pragma foreign_keys=on")
            yield connection
        finally:
            connection.close()

    @contextlib.contextmanager
    def _write(self) -> Iterator[tuple[sqlite3.Connection, str]]:
        """One immediate transaction whose clock reading is not behind the store."""
        now = self.clock()
        if now.utcoffset() is None:
            raise ForecastError("FORECAST_CLOCK: the clock has no time zone")
        # One zone and one precision keep stored times ordered as text.
        stamp = now.astimezone(dt.timezone.utc).isoformat(timespec="microseconds")
        with self._connect() as connection:
            connection.execute("begin immediate")
            try:
                latest = connection.execute(
                    "select max(t) from (select max(forecasted_at) t from forecast "
                    "union all select max(started_at) from start "
                    "union all select max(finished_at) from outcome)"
                ).fetchone()[0]
                if latest is not None and stamp < latest:
                    raise ForecastError("FORECAST_CLOCK: the clock moved backwards")
                yield connection, stamp
                connection.execute("commit")
            except BaseException:
                connection.execute("rollback")
                raise

    def forecast(
        self,
        *,
        task_ref: str,
        task_type: str,
        time_basis: str,
        unit: str,
        p30: float,
        p50: float,
        p80: float,
        start_def: str,
        end_def: str,
        reference_class: str,
        assumptions: str,
        risks: str,
        supersedes: int | None = None,
    ) -> dict[str, Any]:
        if not isinstance(task_type, str) or not TASK_TYPE.fullmatch(task_type):
            raise ForecastError("FORECAST_FIELD: task_type is a lowercase identifier")
        if time_basis not in TIME_BASES or unit not in UNITS:
            raise ForecastError("FORECAST_FIELD: unknown time basis or unit")
        texts = {
            name: _text(name, value)
            for name, value in (
                ("task_ref", task_ref),
                ("start_def", start_def),
                ("end_def", end_def),
                ("reference_class", reference_class),
                ("assumptions", assumptions),
                ("risks", risks),
            )
        }
        values = [
            _amount(name, value, "FORECAST_QUANTILES")
            for name, value in (("p30", p30), ("p50", p50), ("p80", p80))
        ]
        if any(value is None for value in values) or not (
            values[0] <= values[1] <= values[2]
        ):
            raise ForecastError("FORECAST_QUANTILES: need p30 <= p50 <= p80")
        with self._write() as (connection, now):
            live = connection.execute(
                "select f.id, f.revision, "
                "exists(select 1 from start s where s.forecast_id = f.id) as started "
                "from forecast f where f.task_ref = ? and not exists("
                "select 1 from forecast n where n.supersedes = f.id)",
                (texts["task_ref"],),
            ).fetchone()
            revision = 1
            if supersedes is None:
                if live is not None:
                    raise ForecastError(
                        "FORECAST_STATE: the task reference already has a forecast"
                    )
            elif live is None or live["id"] != supersedes or live["started"]:
                raise ForecastError(
                    "FORECAST_STATE: only the unstarted live forecast of the same "
                    "task reference is superseded"
                )
            else:
                revision = live["revision"] + 1
            sample = connection.execute(
                "select count(*) from outcome o join forecast f on f.id = o.forecast_id "
                "where o.outcome = 'completed' and f.task_type = ? and f.time_basis = ? "
                "and f.unit = ? and o.finished_at < ?",
                (task_type, time_basis, unit, now),
            ).fetchone()[0]
            identifier = connection.execute(
                "select coalesce(max(id), 0) + 1 from forecast"
            ).fetchone()[0]
            row = {
                **texts,
                "id": identifier,
                "task_type": task_type,
                "time_basis": time_basis,
                "unit": unit,
                "p30": values[0],
                "p50": values[1],
                "p80": values[2],
                "sample_size": sample,
                "confidence": "uncalibrated",
                "revision": revision,
                "supersedes": supersedes,
                "forecasted_at": now,
            }
            connection.execute(
                f"insert into forecast ({', '.join(FORECAST_COLUMNS)}, digest) "
                f"values ({', '.join('?' * len(FORECAST_COLUMNS))}, ?)",
                (*(row[name] for name in FORECAST_COLUMNS), _digest(row)),
            )
        return self.record(identifier)

    def start(self, forecast_id: int) -> dict[str, Any]:
        with self._write() as (connection, now):
            row = connection.execute(
                "select f.forecasted_at, f.digest, s.forecast_id as started, "
                "exists(select 1 from forecast n where n.supersedes = f.id) "
                "as replaced from forecast f "
                "left join start s on s.forecast_id = f.id where f.id = ?",
                (forecast_id,),
            ).fetchone()
            if row is None or row["started"] is not None or row["replaced"]:
                raise ForecastError(
                    "FORECAST_STATE: start needs a live forecast that has not started"
                )
            if not row["forecasted_at"] < now:
                raise ForecastError("FORECAST_STATE: a run starts after its forecast")
            connection.execute(
                "insert into start values (?, ?, ?)",
                (forecast_id, now, _digest(row["digest"], now)),
            )
        return self.record(forecast_id)

    def finish(
        self,
        forecast_id: int,
        outcome: str,
        *,
        actual: float | None = None,
        verify: float | None = None,
        runner_wait: float | None = None,
        user_wait: float | None = None,
        tokens: int | None = None,
        cost: float | None = None,
    ) -> dict[str, Any]:
        if outcome not in OUTCOMES:
            raise ForecastError("FORECAST_FIELD: unknown outcome")
        given = _amount("actual", actual)
        extra = {
            name: _amount(name, value)
            for name, value in (
                ("verify", verify),
                ("runner_wait", runner_wait),
                ("user_wait", user_wait),
                ("cost", cost),
            )
        }
        if tokens is not None and (
            isinstance(tokens, bool) or not isinstance(tokens, int) or tokens < 0
        ):
            raise ForecastError(
                "FORECAST_ACTUAL: tokens must be a non-negative integer"
            )
        with self._write() as (connection, now):
            row = connection.execute(
                "select f.time_basis, f.unit, s.started_at, s.digest, "
                "o.forecast_id as finished from forecast f "
                "join start s on s.forecast_id = f.id "
                "left join outcome o on o.forecast_id = f.id where f.id = ?",
                (forecast_id,),
            ).fetchone()
            if row is None or row["finished"] is not None:
                raise ForecastError("FORECAST_STATE: finish needs a started, open run")
            if not row["started_at"] < now:
                raise ForecastError("FORECAST_CLOCK: a run finishes after its start")
            elapsed = (
                dt.datetime.fromisoformat(now)
                - dt.datetime.fromisoformat(row["started_at"])
            ).total_seconds() / UNITS[row["unit"]]
            result = {
                "forecast_id": forecast_id,
                "finished_at": now,
                "outcome": outcome,
                "actual": self._actual(outcome, row["time_basis"], given, elapsed),
                "verify": extra["verify"],
                "runner_wait": extra["runner_wait"],
                "user_wait": extra["user_wait"],
                "tokens": tokens,
                "cost": extra["cost"],
            }
            connection.execute(
                f"insert into outcome ({', '.join(OUTCOME_COLUMNS)}, digest) "
                f"values ({', '.join('?' * len(OUTCOME_COLUMNS))}, ?)",
                (
                    *(result[name] for name in OUTCOME_COLUMNS),
                    _digest(row["digest"], result),
                ),
            )
        return self.record(forecast_id)

    @staticmethod
    def _actual(
        outcome: str, time_basis: str, given: float | None, elapsed: float
    ) -> float | None:
        if outcome != "completed":
            if given is not None:
                raise ForecastError(
                    "FORECAST_ACTUAL: a censored run keeps a null actual"
                )
            return None
        if time_basis == "elapsed":
            if given is not None:
                raise ForecastError(
                    "FORECAST_ACTUAL: an elapsed actual comes from the clock"
                )
            return round(elapsed, 6)
        if given is None or given > elapsed:
            raise ForecastError(
                "FORECAST_ACTUAL: an active actual is given and within elapsed time"
            )
        return given

    def record(self, forecast_id: int) -> dict[str, Any]:
        for row in self.records():
            if row["id"] == forecast_id:
                return row
        raise ForecastError("FORECAST_STATE: no such forecast")

    def records(self) -> list[dict[str, Any]]:
        """Every record, after its digests are recomputed and compared."""
        with self._connect() as connection:
            forecasts = connection.execute(
                "select * from forecast order by id"
            ).fetchall()
            starts = {
                row["forecast_id"]: row
                for row in connection.execute("select * from start")
            }
            outcomes = {
                row["forecast_id"]: row
                for row in connection.execute("select * from outcome")
            }
        replaced = {row["supersedes"] for row in forecasts}
        result = []
        for row in forecasts:
            body = {name: row[name] for name in FORECAST_COLUMNS}
            begun = starts.get(row["id"])
            ended = outcomes.get(row["id"])
            done = None if ended is None else {k: ended[k] for k in OUTCOME_COLUMNS}
            if (
                _digest(body) != row["digest"]
                or (
                    begun
                    and _digest(row["digest"], begun["started_at"]) != begun["digest"]
                )
                or (
                    ended
                    and (not begun or _digest(begun["digest"], done) != ended["digest"])
                )
            ):
                raise ForecastError(
                    f"FORECAST_TAMPERED: record {row['id']} differs from its digest"
                )
            result.append(
                {
                    **body,
                    "digest": row["digest"],
                    "started_at": begun["started_at"] if begun else None,
                    **{k: (done or {}).get(k) for k in OUTCOME_COLUMNS[1:]},
                    "replaced": row["id"] in replaced,
                }
            )
        return result

    def score(self) -> dict[str, Any]:
        empty = {"rows": [], "censored": Counter(), "unstarted": 0, "open": 0}
        groups: dict[tuple[str, str, str], dict[str, Any]] = defaultdict(
            lambda: {**empty, "rows": [], "censored": Counter(), "superseded": 0}
        )
        for row in self.records():
            group = groups[(row["task_type"], row["time_basis"], row["unit"])]
            if row["replaced"]:
                group["superseded"] += 1
            elif row["outcome"] == "completed":
                group["rows"].append(row)
            elif row["outcome"] is not None:
                group["censored"][row["outcome"]] += 1
            elif row["started_at"] is not None:
                group["open"] += 1
            else:
                group["unstarted"] += 1
        result = []
        for key in sorted(groups):
            group = groups[key]
            rows = group["rows"]
            entry: dict[str, Any] = {
                "task_type": key[0],
                "time_basis": key[1],
                "unit": key[2],
                "n": len(rows),
                "censored": dict(sorted(group["censored"].items())),
                "open": group["open"],
                "unstarted": group["unstarted"],
                "superseded": group["superseded"],
            }
            if rows:
                entry["coverage"] = {
                    name: fmean(1.0 if r["actual"] <= r[name] else 0.0 for r in rows)
                    for name in QUANTILES
                }
                entry["pinball"] = {
                    name: fmean(
                        (p - (1.0 if r["actual"] < r[name] else 0.0))
                        * (r["actual"] - r[name])
                        for r in rows
                    )
                    for name, p in QUANTILES.items()
                }
            result.append(entry)
        return {
            "assessment": "DESCRIPTIVE_ONLY",
            "groups": result,
            "limits": [
                "Statistics cover completed runs only; censored, open and unstarted "
                "records are counted apart, so the coverage carries selection bias.",
                "A small N is never a calibration; no threshold turns it into one.",
                "P30 to P80 is not an 80% interval, and quantiles are never summed.",
                "An active actual is self-reported within the elapsed time.",
            ],
        }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=Path("."))
    commands = parser.add_subparsers(dest="command", required=True)
    new = commands.add_parser("forecast")
    for name in (
        "task-ref",
        "task-type",
        "start-def",
        "end-def",
        "reference-class",
        "assumptions",
        "risks",
    ):
        new.add_argument(f"--{name}", required=True)
    new.add_argument("--time-basis", choices=TIME_BASES, required=True)
    new.add_argument("--unit", choices=tuple(UNITS), required=True)
    for name in QUANTILES:
        new.add_argument(f"--{name}", type=float, required=True)
    new.add_argument("--supersedes", type=int)
    begin = commands.add_parser("start")
    begin.add_argument("id", type=int)
    end = commands.add_parser("finish")
    end.add_argument("id", type=int)
    end.add_argument("outcome", choices=OUTCOMES)
    for name in ("actual", "verify", "runner-wait", "user-wait", "cost"):
        end.add_argument(f"--{name}", type=float)
    end.add_argument("--tokens", type=int)
    commands.add_parser("list")
    commands.add_parser("score")
    args = parser.parse_args(argv)
    try:
        store = Forecasts(args.root.resolve() / STORE_DIR / STORE_NAME)
        if args.command == "forecast":
            output: Any = store.forecast(
                task_ref=args.task_ref,
                task_type=args.task_type,
                time_basis=args.time_basis,
                unit=args.unit,
                p30=args.p30,
                p50=args.p50,
                p80=args.p80,
                start_def=args.start_def,
                end_def=args.end_def,
                reference_class=args.reference_class,
                assumptions=args.assumptions,
                risks=args.risks,
                supersedes=args.supersedes,
            )
        elif args.command == "start":
            output = store.start(args.id)
        elif args.command == "finish":
            output = store.finish(
                args.id,
                args.outcome,
                actual=args.actual,
                verify=args.verify,
                runner_wait=args.runner_wait,
                user_wait=args.user_wait,
                tokens=args.tokens,
                cost=args.cost,
            )
        elif args.command == "list":
            output = store.records()
        else:
            output = store.score()
    except (ForecastError, sqlite3.DatabaseError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 2
    print(json.dumps(output, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
