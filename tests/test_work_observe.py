"""Regressions for the read-only run fact join (SPEC-0236, P13)."""

from __future__ import annotations

import datetime as dt
import importlib.util
import json
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))


def _load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


OBSERVE = _load("work_observe", "scripts/work_observe.py")
FORECAST = _load("work_forecast_for_observe", "scripts/work_forecast.py")
ANALYSIS = _load("session_analysis_for_observe", "scripts/session_analysis.py")
T0 = dt.datetime(2026, 11, 24, 3, 0, tzinfo=dt.timezone.utc)


class ObserveTest(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory(prefix="work-observe-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.store = self.root / ".workspace-memory"
        self.ticks = iter(T0 + dt.timedelta(minutes=m) for m in range(0, 600, 5))

    def forecast(self, task_ref: str) -> None:
        store = FORECAST.Forecasts(
            self.store / "forecast.sqlite3", clock=lambda: next(self.ticks)
        )
        record = store.forecast(
            task_ref=task_ref,
            task_type="governance-prompt",
            time_basis="elapsed",
            unit="minutes",
            p30=10,
            p50=20,
            p80=30,
            start_def="start",
            end_def="merge",
            reference_class="fixture",
            assumptions="none",
            risks="none",
        )
        store.start(record["id"])
        store.finish(record["id"], "completed")

    def parallel(self, run: str, task_ref: str) -> None:
        directory = self.root / ".workspace-test" / "parallel" / run
        directory.mkdir(parents=True)
        unit = {
            "provider": "claude",
            "state": "promoted",
            "session": "s-1",
            "cost_estimate_usd": 0.07,
            "charge_usd": None,
            "cost_note": "estimate",
            "started": 0.5,
            "finished": 13.3,
            "prompt": "never copied",
        }
        (directory / "report.json").write_text(
            json.dumps(
                {
                    "run": run,
                    "task_ref": task_ref,
                    "state": "completed",
                    "units": {"router": unit},
                    "timing": {"elapsed": 49.0},
                }
            )
        )

    def candidate(self, promoted_ref: str) -> None:
        self.store.mkdir(exist_ok=True)
        with sqlite3.connect(self.store / "analysis.sqlite3") as connection:
            connection.executescript(ANALYSIS.SCHEMA)
            connection.execute(
                "insert into candidate (window, pattern, subject, problem,"
                " source_refs, frequency, condition, proposal, risk,"
                " acceptance_test, decision, reviewer, reviewed_at, promoted_to,"
                " promoted_ref) values ('2026-11-18', 'repeated-tool-failure',"
                " 'tools', 'p', '[]', 3, 'c', 'x', 'r', 't', 'accepted', 'r',"
                " '2026-11-19T00:00:00+00:00', 'task', ?)",
                (promoted_ref,),
            )

    def test_facts_for_the_key_are_joined_and_others_are_not(self) -> None:
        self.forecast("SPEC-0235 WORK-001 request a")
        self.forecast("SPEC-02350 WORK-001 request b")
        self.parallel("aaaa1111", "SPEC-0235 WORK-001 request a")
        self.parallel("bbbb2222", "SPEC-0234 WORK-001 request c")
        self.candidate("SPEC-0235 TSK-0001 EVD-005")
        result = OBSERVE.report(self.root, "SPEC-0235")
        self.assertEqual(
            [f["task_ref"] for f in result["forecasts"]],
            ["SPEC-0235 WORK-001 request a"],
        )
        self.assertEqual(result["forecasts"][0]["outcome"], "completed")
        (run,) = result["parallel_runs"]
        self.assertEqual(run["run"], "aaaa1111")
        unit = run["units"]["router"]
        self.assertEqual((unit["session"], unit["cost_estimate_usd"]), ("s-1", 0.07))
        self.assertIsNone(unit["charge_usd"])
        self.assertNotIn("prompt", unit, "only the listed facts are joined")
        (candidate,) = result["candidates"]
        self.assertEqual(candidate["effect"]["state"], "unobserved")
        self.assertEqual(result["unobserved"], {})

    def test_a_missing_source_is_null_with_a_reason_and_never_created(self) -> None:
        result = OBSERVE.report(self.root, "SPEC-0235")
        for name in ("forecasts", "parallel_runs", "candidates"):
            self.assertIsNone(result[name])
            self.assertIn("no local store", result["unobserved"][name])
        self.assertFalse(self.store.exists(), "a read created a store")
        self.forecast("SPEC-0234 WORK-001 request x")
        result = OBSERVE.report(self.root, "SPEC-0235")
        self.assertIsNone(result["forecasts"])
        self.assertIn("no record for this key", result["unobserved"]["forecasts"])

    def test_a_blank_key_is_refused(self) -> None:
        for key in ("", " SPEC-0235", "SPEC-0235 "):
            with self.subTest(key=key), self.assertRaises(ValueError):
                OBSERVE.report(self.root, key)

    def test_the_cli_prints_the_join(self) -> None:
        self.parallel("aaaa1111", "SPEC-0235 WORK-001 request a")
        output = []
        original = sys.stdout.write
        sys.stdout.write = output.append  # type: ignore[assignment]
        try:
            code = OBSERVE.main(
                ["report", "--root", str(self.root), "--key", "SPEC-0235"]
            )
        finally:
            sys.stdout.write = original  # type: ignore[assignment]
        self.assertEqual(code, 0)
        self.assertEqual(json.loads("".join(output))["key"], "SPEC-0235")


if __name__ == "__main__":
    unittest.main()
