#!/usr/bin/env python3
"""Join the run facts this workspace already keeps for one Task key (P13).

Read-only. Forecast records, parallel run reports and analysis candidates are
read where their owners keep them; nothing is copied into a new store, and no
transcript, prompt or provider output is read. A key is an artifact ID such as
`SPEC-0235`, optionally narrowed (`SPEC-0235 WORK-001`); a record matches when
its task reference equals the key or continues it after a space. A source with
nothing for the key is null with its reason, never zero. Cost stays split into
the CLI's estimate and the account's charge, which is never observed here, and
hosted CI timing stays in its run log, cited by run ID.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

SCRIPTS = Path(__file__).resolve().parent
STORE_DIR = ".workspace-memory"
RUNTIME = ".workspace-test/parallel"
REPORT_LIMIT = 4 * 1024 * 1024
UNIT_FIELDS = (
    "provider",
    "state",
    "reason",
    "attempts",
    "started",
    "finished",
    "scope",
    "session",
    "cost_estimate_usd",
    "charge_usd",
    "cost_note",
    "turns",
    "changed",
)
CANDIDATE_FIELDS = (
    "candidate_id",
    "window",
    "pattern",
    "subject",
    "frequency",
    "decision",
    "promoted_to",
    "promoted_ref",
    "acceptance_test",
    "rechecks",
    "effect",
)


def _load(name: str, file: str):
    if str(SCRIPTS) not in sys.path:
        sys.path.insert(0, str(SCRIPTS))
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / file)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def matches(ref: Any, key: str) -> bool:
    return isinstance(ref, str) and (ref == key or ref.startswith(key + " "))


def _forecasts(root: Path, key: str) -> list[dict[str, Any]] | None:
    path = root / STORE_DIR / "forecast.sqlite3"
    if not path.is_file():
        return None
    forecast = _load("_work_observe_forecast", "work_forecast.py")
    # records() recomputes every digest, so an edited row is refused, not shown.
    rows = forecast.Forecasts(path).records()
    return [row for row in rows if matches(row["task_ref"], key)]


def _parallel(root: Path, key: str) -> list[dict[str, Any]] | None:
    runtime = root / RUNTIME
    if not runtime.is_dir():
        return None
    found = []
    for report_path in sorted(runtime.glob("*/report.json")):
        try:
            with report_path.open("rb") as handle:
                report = json.loads(handle.read(REPORT_LIMIT))
        except (OSError, ValueError):
            continue  # unreadable or partial: not a fact
        if not isinstance(report, dict) or not matches(report.get("task_ref"), key):
            continue
        units = report.get("units")
        found.append(
            {
                "run": report.get("run"),
                "task_ref": report.get("task_ref"),
                "base": report.get("base"),
                "state": report.get("state"),
                "integration": report.get("integration"),
                "timing": report.get("timing"),
                "units": {
                    uid: {k: unit.get(k) for k in UNIT_FIELDS}
                    for uid, unit in (units if isinstance(units, dict) else {}).items()
                    if isinstance(unit, dict)
                },
            }
        )
    return found


def _candidates(root: Path, key: str) -> list[dict[str, Any]] | None:
    path = root / STORE_DIR / "analysis.sqlite3"
    if not path.is_file():
        return None
    analysis = _load("_work_observe_analysis", "session_analysis.py")
    return [
        {k: candidate[k] for k in CANDIDATE_FIELDS}
        for candidate in analysis.Analysis(path, root).candidates()
        if matches(candidate["promoted_ref"], key)
    ]


def report(root: Path, key: str) -> dict[str, Any]:
    if not key.strip() or key != key.strip():
        raise ValueError("OBSERVE_KEY: a key is a trimmed, non-empty task reference")
    sources = {
        "forecasts": (_forecasts, "work_forecast.py"),
        "parallel_runs": (_parallel, "work_parallel.py"),
        "candidates": (_candidates, "session_analysis.py"),
    }
    result: dict[str, Any] = {"key": key}
    unobserved: dict[str, str] = {}
    for name, (read, owner) in sources.items():
        rows = read(root, key)
        if rows is None:
            unobserved[name] = f"{owner} has no local store or runtime here"
        elif not rows:
            unobserved[name] = f"{owner} holds no record for this key"
        result[name] = rows or None
    result["unobserved"] = unobserved
    result["limits"] = [
        "Only facts already kept locally are joined; hosted CI timing stays in "
        "its run log and is cited by run ID.",
        "cost_estimate_usd is the CLI's own estimate; the actual charge is null.",
        "Counts are not summed across sources, and a missing source is not zero.",
    ]
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    commands = parser.add_subparsers(dest="command", required=True)
    joined = commands.add_parser("report")
    joined.add_argument("--root", type=Path, default=Path("."))
    joined.add_argument("--key", required=True)
    args = parser.parse_args(argv)
    try:
        output = report(args.root.resolve(), args.key)
    except Exception as exc:  # noqa: BLE001 - each owner's refusal, as one line
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 2
    print(json.dumps(output, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
