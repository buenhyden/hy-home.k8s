"""Regressions for the local work forecast store (W10-FORECAST, D09)."""

from __future__ import annotations

import datetime as dt
import importlib.util
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


FORECAST = _load("work_forecast", "scripts/work_forecast.py")
T0 = dt.datetime(2026, 11, 19, 6, 0, tzinfo=dt.timezone.utc)


class Clock:
    def __init__(self) -> None:
        self.now = T0

    def __call__(self) -> dt.datetime:
        return self.now

    def advance(self, seconds: float) -> None:
        self.now += dt.timedelta(seconds=seconds)


class WorkForecastTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.clock = Clock()
        self.store = FORECAST.Forecasts(
            Path(self.tmp.name) / "forecast.sqlite3", clock=self.clock
        )

    def make(self, **change):
        self.serial = getattr(self, "serial", 0) + 1
        values = dict(
            task_ref=f"SPEC-0161 run {self.serial}",
            task_type="qa-staged",
            time_basis="elapsed",
            unit="seconds",
            p30=60.0,
            p50=90.0,
            p80=150.0,
            start_def="qa.py staged starts",
            end_def="qa.py staged exits",
            reference_class="none",
            assumptions="warm cache",
            risks="lifecycle tests are slow",
        )
        values.update(change)
        return self.store.forecast(**values)

    def run_one(self, seconds: float, outcome: str = "completed", **finish):
        record = self.make()
        self.clock.advance(1)
        self.store.start(record["id"])
        self.clock.advance(seconds)
        return self.store.finish(record["id"], outcome, **finish)

    def assertRefused(self, code: str, call, *args, **kwargs) -> None:
        with self.assertRaises(FORECAST.ForecastError) as caught:
            call(*args, **kwargs)
        self.assertTrue(str(caught.exception).startswith(code), str(caught.exception))

    def test_a_forecast_is_fixed_with_the_tool_clock_and_marked_uncalibrated(self):
        record = self.make()
        self.assertEqual(record["forecasted_at"], T0.isoformat(timespec="microseconds"))
        self.assertEqual(record["sample_size"], 0)
        self.assertEqual(record["confidence"], "uncalibrated")
        self.assertEqual(record["revision"], 1)
        self.assertEqual(len(record["digest"]), 64)

    def test_bad_quantiles_units_and_types_are_refused(self):
        self.assertRefused("FORECAST_QUANTILES", self.make, p50=200.0)
        self.assertRefused("FORECAST_QUANTILES", self.make, p30=-1.0)
        self.assertRefused("FORECAST_QUANTILES", self.make, p80=float("nan"))
        self.assertRefused("FORECAST_FIELD", self.make, unit="days")
        self.assertRefused("FORECAST_FIELD", self.make, time_basis="wall")
        self.assertRefused("FORECAST_FIELD", self.make, task_type="QA staged!")
        self.assertRefused("FORECAST_FIELD", self.make, end_def=" ")

    def test_elapsed_actual_comes_from_the_clock_and_waits_stay_separate(self):
        result = self.run_one(80, runner_wait=5.0, user_wait=0.0)
        self.assertEqual(result["actual"], 80.0)
        self.assertEqual(result["runner_wait"], 5.0)
        self.assertIsNone(result["tokens"])
        self.assertIsNone(result["cost"])
        record = self.make()
        self.clock.advance(1)
        self.store.start(record["id"])
        self.clock.advance(5)
        self.assertRefused(
            "FORECAST_ACTUAL", self.store.finish, record["id"], "completed", actual=3
        )
        self.assertRefused(
            "FORECAST_ACTUAL", self.store.finish, record["id"], "completed", verify=-1
        )

    def test_active_time_needs_an_actual_within_the_elapsed_time(self):
        record = self.make(time_basis="active", unit="minutes", p30=1, p50=2, p80=3)
        self.clock.advance(1)
        self.store.start(record["id"])
        self.clock.advance(120)
        self.assertRefused(
            "FORECAST_ACTUAL", self.store.finish, record["id"], "completed"
        )
        self.assertRefused(
            "FORECAST_ACTUAL",
            self.store.finish,
            record["id"],
            "completed",
            actual=5,
        )
        done = self.store.finish(record["id"], "completed", actual=1.5)
        self.assertEqual(done["actual"], 1.5)

    def test_order_is_enforced_and_records_are_never_rewritten(self):
        record = self.make()
        self.assertRefused("FORECAST_STATE", self.store.finish, record["id"], "failed")
        self.assertRefused("FORECAST_STATE", self.store.start, record["id"])
        self.clock.advance(1)
        self.store.start(record["id"])
        self.assertRefused("FORECAST_STATE", self.store.start, record["id"])
        self.clock.advance(10)
        self.store.finish(record["id"], "completed")
        self.assertRefused(
            "FORECAST_STATE", self.store.finish, record["id"], "completed"
        )
        self.assertRefused("FORECAST_STATE", self.store.start, 999)
        connection = sqlite3.connect(self.store.path)
        self.addCleanup(connection.close)
        for statement in (
            "update forecast set p80 = 999",
            "delete from forecast",
            "update outcome set actual = 1",
            "delete from start",
        ):
            with self.subTest(statement=statement):
                with self.assertRaises(sqlite3.DatabaseError):
                    connection.execute(statement)

    def test_cancelled_and_failed_runs_are_censored_not_scored(self):
        self.run_one(80)
        self.run_one(200, outcome="cancelled")
        self.run_one(30, outcome="failed")
        self.assertRefused(
            "FORECAST_ACTUAL", self.run_one, 30, outcome="cancelled", actual=30
        )
        score = self.store.score()
        (group,) = score["groups"]
        self.assertEqual(group["n"], 1)
        # The refused finish leaves its run open instead of censoring it.
        self.assertEqual(group["censored"], {"cancelled": 1, "failed": 1})
        self.assertEqual(group["open"], 1)
        self.assertEqual(score["assessment"], "DESCRIPTIVE_ONLY")

    def test_score_reports_coverage_and_pinball_per_group(self):
        self.run_one(80)  # under p50, over p30
        self.run_one(200)  # over p80
        group = self.store.score()["groups"][0]
        self.assertEqual(group["coverage"], {"p30": 0.0, "p50": 0.5, "p80": 0.5})
        # L_p(y, q) = (p - 1[y < q]) * (y - q), averaged over the two runs.
        expected_p80 = ((0.8 - 1) * (80 - 150) + 0.8 * (200 - 150)) / 2
        self.assertAlmostEqual(group["pinball"]["p80"], expected_p80)
        self.make(time_basis="active", unit="minutes", p30=1, p50=2, p80=3)
        groups = self.store.score()["groups"]
        self.assertEqual([g["n"] for g in groups], [0, 2])
        self.assertEqual(groups[0]["unstarted"], 1)

    def test_sample_size_counts_only_earlier_completed_runs_of_the_group(self):
        self.run_one(80)
        self.run_one(10, outcome="cancelled")
        later = self.make()
        self.assertEqual(later["sample_size"], 1)
        # The tool never labels itself calibrated; N is reported instead.
        self.assertEqual(later["confidence"], "uncalibrated")
        other = self.make(task_type="lifecycle-tests")
        self.assertEqual(other["sample_size"], 0)

    def test_a_new_revision_supersedes_without_changing_the_first(self):
        first = self.make()
        second = self.make(
            p80=300.0, supersedes=first["id"], task_ref=first["task_ref"]
        )
        self.assertEqual(second["revision"], 2)
        self.assertRefused("FORECAST_STATE", self.store.start, first["id"])
        self.assertRefused(
            "FORECAST_STATE",
            self.make,
            supersedes=first["id"],
            task_ref=first["task_ref"],
        )
        kept = {row["id"]: row for row in self.store.records()}
        self.assertEqual(kept[first["id"]]["p80"], 150.0)
        self.clock.advance(1)
        self.store.start(second["id"])
        self.clock.advance(5)
        self.store.finish(second["id"], "completed")
        self.assertRefused(
            "FORECAST_STATE",
            self.make,
            supersedes=second["id"],
            task_ref=first["task_ref"],
        )
        self.assertEqual(self.store.score()["groups"][0]["superseded"], 1)

    def test_a_started_forecast_cannot_be_superseded_or_hidden(self):
        record = self.make()
        self.clock.advance(1)
        self.store.start(record["id"])
        self.clock.advance(100)
        self.assertRefused(
            "FORECAST_STATE",
            self.make,
            supersedes=record["id"],
            task_ref=record["task_ref"],
        )
        other = self.make()
        self.assertRefused(
            "FORECAST_STATE", self.make, supersedes=other["id"], task_ref="elsewhere"
        )

    def test_one_task_ref_has_one_live_forecast(self):
        record = self.make()
        self.assertRefused("FORECAST_STATE", self.make, task_ref=record["task_ref"])

    def test_a_clock_that_moves_backwards_is_refused(self):
        record = self.make()
        self.clock.advance(10)
        self.store.start(record["id"])
        self.clock.advance(-500)
        self.assertRefused(
            "FORECAST_CLOCK", self.store.finish, record["id"], "completed"
        )
        self.assertRefused("FORECAST_CLOCK", self.make)
        self.clock.advance(600)
        done = self.store.finish(record["id"], "completed")
        self.assertEqual(done["actual"], 100.0)

    def test_replaced_rows_are_refused_and_edits_are_detected(self):
        record = self.make()
        self.clock.advance(1)
        self.store.start(record["id"])
        self.clock.advance(80)
        self.store.finish(record["id"], "completed")
        connection = sqlite3.connect(self.store.path, isolation_level=None)
        self.addCleanup(connection.close)
        for statement in (
            "insert or replace into outcome (forecast_id, finished_at, outcome, "
            "actual, digest) select forecast_id, finished_at, outcome, 1, digest "
            "from outcome",
            "insert or replace into start select * from start",
            "insert or replace into forecast select * from forecast",
        ):
            with self.subTest(statement=statement):
                with self.assertRaises(sqlite3.DatabaseError):
                    connection.execute(statement)
        connection.execute("drop trigger outcome_no_update")
        connection.execute("update outcome set actual = 1")
        self.assertRefused("FORECAST_TAMPERED", self.store.score)
        self.assertRefused("FORECAST_TAMPERED", self.store.records)

    def test_unstarted_open_and_superseded_records_are_counted_per_group(self):
        self.make()
        opened = self.make()
        self.clock.advance(1)
        self.store.start(opened["id"])
        self.run_one(50)
        self.make(task_type="lifecycle-tests")
        groups = {g["task_type"]: g for g in self.store.score()["groups"]}
        self.assertEqual(groups["qa-staged"]["unstarted"], 1)
        self.assertEqual(groups["qa-staged"]["open"], 1)
        self.assertEqual(groups["qa-staged"]["n"], 1)
        self.assertEqual(groups["lifecycle-tests"]["unstarted"], 1)
        self.assertNotIn("coverage", groups["lifecycle-tests"])


if __name__ == "__main__":
    unittest.main()
