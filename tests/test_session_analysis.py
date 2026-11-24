"""Scheduled session analysis contract (W08-ANALYSIS): deterministic and bounded."""

from __future__ import annotations

import datetime as dt
import importlib.util
import json
import os
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]


def _load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


MEMORY = _load("workspace_memory", "scripts/workspace_memory.py")
CAPTURE = _load("session_capture", "scripts/session_capture.py")
ANALYSIS = _load("session_analysis", "scripts/session_analysis.py")
SEOUL = dt.timezone(dt.timedelta(hours=9))
PRIVATE_TEXT = "private words that must never reach a candidate"


def at(day: int, hour: int = 3) -> dt.datetime:
    return dt.datetime(2026, 11, day, hour, 0, tzinfo=SEOUL)


class SessionAnalysisTest(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory(prefix="session-analysis-")
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name)
        self.root = self.base / "repo"
        self.root.mkdir()
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        MEMORY.Store.init(self.root)
        self.home = self.base / "claude-home"
        environment = mock.patch.dict(os.environ, {"CLAUDE_CONFIG_DIR": str(self.home)})
        environment.start()
        self.addCleanup(environment.stop)
        self.capture = CAPTURE.Capture.open(self.root)
        self.analysis = ANALYSIS.Analysis.open(self.root)

    def session(self, session_id: str, day: int, failures: int = 0, end: bool = True):
        path = self.home / "projects" / "repo" / f"{session_id}.jsonl"
        path.parent.mkdir(parents=True, exist_ok=True)
        lines = [{"type": "user", "message": {"content": PRIVATE_TEXT}}]
        lines += [
            {
                "type": "user",
                "message": {
                    "content": [
                        {
                            "type": "tool_result",
                            "is_error": True,
                            "content": PRIVATE_TEXT,
                        }
                    ]
                },
            }
            for _ in range(failures)
        ]
        lines += [
            {
                "type": "assistant",
                "message": {"content": [{"type": "tool_use", "name": "Bash"}]},
            }
            for _ in range(failures)
        ]
        path.write_text("".join(json.dumps(x) + "\n" for x in lines), encoding="utf-8")
        events = ["SessionStart", "Stop"] + (["SessionEnd"] if end else [])
        stamp = at(day, 12).astimezone(dt.timezone.utc).isoformat(timespec="seconds")
        with mock.patch.object(CAPTURE, "_now", return_value=stamp):
            for event in events:
                self.capture.hook(
                    "claude",
                    {
                        "hook_event_name": event,
                        "session_id": session_id,
                        "transcript_path": str(path),
                        "cwd": str(self.root),
                    },
                )

    def run_at(self, now: dt.datetime, trigger: str = "scheduled"):
        return self.analysis.run(trigger=trigger, now=now)

    def candidates(self):
        return self.analysis.candidates()

    def test_a_scheduled_run_analyzes_the_previous_day_from_capture(self) -> None:
        self.session("s-1", 17, failures=3)
        result = self.run_at(at(18))
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["windows"], ["2026-11-17"])
        self.assertEqual(result["cost_usd"], 0)
        patterns = {c["pattern"]: c for c in self.candidates()}
        failure = patterns["repeated-tool-failure"]
        self.assertEqual(failure["frequency"], 3)
        self.assertEqual(failure["decision"], "proposed")
        self.assertTrue(failure["source_refs"])
        for field in ("problem", "condition", "proposal", "risk", "acceptance_test"):
            self.assertTrue(failure[field])
        stored = (
            self.analysis.path.read_bytes() + json.dumps(self.candidates()).encode()
        )
        self.assertNotIn(PRIVATE_TEXT.encode(), stored)

    def test_an_unchanged_window_is_not_analyzed_twice(self) -> None:
        self.session("s-1", 17, failures=3)
        self.run_at(at(18))
        again = self.run_at(at(18, 4))
        self.assertEqual((again["state"], again["windows"]), ("completed", []))
        self.assertEqual(len(self.candidates()), 1)

    def test_late_input_reanalyzes_its_window_without_duplicates(self) -> None:
        self.session("s-1", 17, failures=3)
        self.run_at(at(18))
        self.session("s-2", 17, failures=3)
        result = self.run_at(at(18, 5))
        self.assertEqual(result["windows"], ["2026-11-17"])
        (failure,) = [
            c for c in self.candidates() if c["pattern"] == "repeated-tool-failure"
        ]
        self.assertEqual(failure["frequency"], 6)

    def test_missed_windows_are_caught_up_in_order(self) -> None:
        self.session("s-1", 14, failures=3)
        self.session("s-2", 16, failures=3)
        self.run_at(at(14, 4), trigger="manual")
        result = self.run_at(at(18))
        self.assertEqual(
            result["windows"], ["2026-11-14", "2026-11-15", "2026-11-16", "2026-11-17"]
        )
        self.assertEqual(
            sorted(c["window"] for c in self.candidates()), ["2026-11-14", "2026-11-16"]
        )

    def test_a_held_lease_refuses_a_second_run(self) -> None:
        self.session("s-1", 17, failures=3)
        token = self.analysis.acquire("other-holder", now=at(18))
        self.assertIsNotNone(token)
        self.assertEqual(self.run_at(at(18))["state"], "busy")
        self.assertEqual(self.candidates(), [])

    def test_an_expired_lease_is_taken_over_and_the_old_holder_is_fenced(self) -> None:
        self.session("s-1", 17, failures=3)
        stale = self.analysis.acquire("crashed-holder", now=at(18))
        later = at(18) + ANALYSIS.LEASE_TTL + dt.timedelta(seconds=1)
        self.assertEqual(self.run_at(later)["state"], "completed")
        with self.assertRaisesRegex(ANALYSIS.AnalysisError, "ANALYSIS_FENCED"):
            self.analysis.check_token(stale)

    def test_a_busy_store_is_retried_a_bounded_number_of_times(self) -> None:
        self.session("s-1", 17, failures=3)
        original = ANALYSIS.Analysis._analyze_window
        calls = []

        def flaky(self, *args, **kwargs):
            calls.append(1)
            if len(calls) < 3:
                raise sqlite3.OperationalError("database is locked")
            return original(self, *args, **kwargs)

        with (
            mock.patch.object(ANALYSIS.Analysis, "_analyze_window", flaky),
            mock.patch.object(ANALYSIS.time, "sleep"),
        ):
            self.assertEqual(self.run_at(at(18))["state"], "completed")
        self.assertEqual(len(calls), 3)

    def test_a_persistent_failure_ends_failed_and_releases_the_lease(self) -> None:
        self.session("s-1", 17, failures=3)
        with (
            mock.patch.object(
                ANALYSIS.Analysis,
                "_analyze_window",
                side_effect=sqlite3.OperationalError("database is locked"),
            ),
            mock.patch.object(ANALYSIS.time, "sleep"),
        ):
            result = self.run_at(at(18))
        self.assertEqual((result["state"], result["attempts"]), ("failed", 3))
        self.assertEqual(self.analysis.status()["last_run"]["state"], "failed")
        self.assertIsNotNone(self.analysis.acquire("next", now=at(18)))

    def test_cancellation_is_recorded_and_releases_the_lease(self) -> None:
        self.session("s-1", 17, failures=3)
        with mock.patch.object(
            ANALYSIS.Analysis, "_analyze_window", side_effect=ANALYSIS.Cancelled()
        ):
            result = self.run_at(at(18))
        self.assertEqual((result["state"], result["windows"]), ("cancelled", []))
        self.assertEqual(self.candidates(), [])
        self.assertIsNotNone(self.analysis.acquire("next", now=at(18)))

    def test_a_signal_only_requests_cancellation_at_a_safe_point(self) -> None:
        self.session("s-1", 17, failures=3)
        ANALYSIS.request_cancel(15, None)
        self.addCleanup(ANALYSIS.CANCEL.clear)
        result = self.run_at(at(18))
        self.assertEqual((result["state"], result["windows"]), ("cancelled", []))
        self.assertEqual(self.analysis.status()["last_run"]["state"], "cancelled")
        self.assertIsNotNone(self.analysis.acquire("next", now=at(18)))

    def test_a_cancelled_run_reports_the_windows_it_committed(self) -> None:
        self.session("s-1", 15, failures=3)
        self.session("s-2", 17, failures=3)
        original = ANALYSIS.Analysis._analyze_window
        calls = []

        def stop_on_second(self, *args, **kwargs):
            calls.append(1)
            if len(calls) == 2:
                raise ANALYSIS.Cancelled()
            return original(self, *args, **kwargs)

        with mock.patch.object(ANALYSIS.Analysis, "_analyze_window", stop_on_second):
            result = self.run_at(at(18))
        self.assertEqual(
            (result["state"], result["windows"]), ("cancelled", ["2026-11-15"])
        )
        resumed = self.run_at(at(18, 4))
        self.assertEqual(resumed["windows"], ["2026-11-16", "2026-11-17"])

    def test_a_killed_run_is_marked_abandoned_by_the_next_holder(self) -> None:
        self.session("s-1", 17, failures=3)
        token = self.analysis.acquire("killed", now=at(18))
        with self.analysis._write() as connection:
            connection.execute(
                "insert into run (trigger, started_at, state, attempts, windows, token,"
                " backend, cost_usd) values ('scheduled', ?, 'running', 1, '[]', ?,"
                " 'deterministic', 0)",
                (at(18).isoformat(), token),
            )
        later = at(18) + ANALYSIS.LEASE_TTL + dt.timedelta(seconds=1)
        self.assertEqual(self.run_at(later)["state"], "completed")
        with self.analysis._connect() as connection:
            states = [
                r[0]
                for r in connection.execute("select state from run order by run_id")
            ]
        self.assertEqual(states, ["abandoned", "completed"])

    def test_tokens_stay_monotonic_after_release(self) -> None:
        first = self.analysis.acquire("a", now=at(18))
        self.analysis.release(first)
        second = self.analysis.acquire("b", now=at(18))
        self.assertGreater(second, first)
        with self.assertRaisesRegex(ANALYSIS.AnalysisError, "ANALYSIS_FENCED"):
            self.analysis.check_token(first)

    def test_an_unexpected_error_ends_failed_and_is_recorded(self) -> None:
        self.session("s-1", 17, failures=3)
        with mock.patch.object(
            ANALYSIS.Analysis, "_analyze_window", side_effect=ValueError("bad shape")
        ):
            result = self.run_at(at(18))
        self.assertEqual(result["state"], "failed")
        self.assertIn("ValueError", result["error"])
        with self.analysis._connect() as connection:
            states = [r[0] for r in connection.execute("select state from run")]
        self.assertEqual(states, ["failed"])
        self.assertIsNotNone(self.analysis.acquire("next", now=at(18)))

    def test_a_reanalyzed_day_withdraws_unreviewed_candidates(self) -> None:
        self.session("s-1", 17, end=False)
        self.run_at(at(18))
        self.assertEqual(
            [c["pattern"] for c in self.candidates()], ["session-without-end"]
        )
        self.capture.hook(
            "claude",
            {
                "hook_event_name": "SessionEnd",
                "session_id": "s-1",
                "transcript_path": str(self.home / "projects" / "repo" / "s-1.jsonl"),
                "cwd": str(self.root),
            },
        )
        self.assertEqual(self.run_at(at(18, 4))["windows"], ["2026-11-17"])
        self.assertEqual(self.candidates(), [])

    def test_a_forgotten_session_leaves_no_pointer_in_the_analysis(self) -> None:
        self.session("s-1", 17, failures=3)
        self.run_at(at(18))
        (candidate,) = self.candidates()
        self.analysis.review(candidate["candidate_id"], decision="accepted", owner="r")
        self.capture.forget("claude", "s-1", owner="platform", approval_ref="user")
        self.assertEqual(self.run_at(at(18, 4))["windows"], ["2026-11-17"])
        self.assertNotIn(b"s-1", self.analysis.path.read_bytes())
        (kept,) = self.candidates()
        self.assertEqual((kept["decision"], kept["source_refs"]), ("accepted", []))

    def test_promotion_happens_once_and_review_is_then_fixed(self) -> None:
        self.session("s-1", 17, failures=3)
        self.run_at(at(18))
        (candidate,) = self.candidates()
        identifier = candidate["candidate_id"]
        self.analysis.review(identifier, decision="accepted", owner="r")
        self.analysis.promote(identifier, to="task", owner="p", ref="tsk#EVD-1")
        with self.assertRaisesRegex(ANALYSIS.AnalysisError, "ANALYSIS_PROMOTED"):
            self.analysis.promote(identifier, to="task", owner="p", ref="tsk#EVD-2")
        with self.assertRaisesRegex(ANALYSIS.AnalysisError, "ANALYSIS_PROMOTED"):
            self.analysis.review(identifier, decision="rejected", owner="r")

    def test_an_accepted_candidate_is_rechecked_on_later_days(self) -> None:
        self.session("s-1", 17, failures=3)
        self.run_at(at(18))
        (candidate,) = self.candidates()
        self.assertEqual(candidate["acceptance"], "unverified")
        self.analysis.review(
            candidate["candidate_id"], decision="accepted", owner="r", now=at(18, 5)
        )
        self.session("s-2", 19, failures=1)  # below the threshold: met
        # The review day itself is mixed, so day 19 is the first later day.
        self.run_at(at(20))
        (kept,) = [c for c in self.candidates() if c["decision"] == "accepted"]
        self.assertEqual(kept["acceptance"], "met")
        self.assertEqual(
            [(r["window"], r["outcome"], r["frequency"]) for r in kept["rechecks"]],
            [("2026-11-19", "met", 1)],
        )
        self.session("s-3", 20, failures=4)  # recurred
        self.run_at(at(21))
        (kept,) = [c for c in self.candidates() if c["decision"] == "accepted"]
        self.assertEqual(kept["acceptance"], "recurred")
        self.assertEqual(kept["rechecks"][-1]["frequency"], 4)

    def test_a_day_without_sessions_or_before_review_is_not_a_recheck(self) -> None:
        self.session("s-1", 17, failures=3)
        self.run_at(at(18))
        (candidate,) = self.candidates()
        self.session("s-2", 18, failures=0)
        self.run_at(at(19))  # day 18 is analyzed before the review
        self.analysis.review(
            candidate["candidate_id"], decision="accepted", owner="r", now=at(19, 5)
        )
        self.run_at(at(21))  # day 20 has no session
        (kept,) = [c for c in self.candidates() if c["decision"] == "accepted"]
        self.assertEqual((kept["acceptance"], kept["rechecks"]), ("unverified", []))
        rejected = self.candidates()[0]
        self.assertNotIn("met", json.dumps(rejected["rechecks"]))

    def test_a_thin_day_is_inconclusive_and_a_recurrence_is_kept(self) -> None:
        self.session("s-1", 17, failures=2)
        self.session("s-2", 17, failures=2)
        self.run_at(at(18))
        (candidate,) = self.candidates()
        self.analysis.review(
            candidate["candidate_id"], decision="accepted", owner="r", now=at(18, 5)
        )
        self.session("s-3", 19, failures=0)  # one session against two: too thin
        self.run_at(at(20))
        (kept,) = [c for c in self.candidates() if c["decision"] == "accepted"]
        self.assertEqual(kept["rechecks"][-1]["outcome"], "inconclusive")
        self.assertEqual(kept["rechecks"][-1]["sessions"], 1)
        self.assertEqual(kept["acceptance"], "unverified")
        for name in ("s-4", "s-5"):
            self.session(name, 20, failures=2)  # four failures: recurred
        self.run_at(at(21))
        for name in ("s-6", "s-7"):
            self.session(name, 21, failures=0)
        self.run_at(at(22))
        (kept,) = [c for c in self.candidates() if c["decision"] == "accepted"]
        self.assertEqual(
            [r["outcome"] for r in kept["rechecks"]],
            ["inconclusive", "recurred", "met"],
        )
        # A later met day never hides an earlier recurrence.
        self.assertEqual(kept["acceptance"], "recurred")

    def test_a_day_that_loses_its_sessions_loses_its_recheck(self) -> None:
        self.session("s-1", 17, failures=3)
        self.run_at(at(18))
        (candidate,) = self.candidates()
        self.analysis.review(
            candidate["candidate_id"], decision="accepted", owner="r", now=at(18, 5)
        )
        self.session("s-2", 19, failures=0)
        self.run_at(at(20))
        self.assertEqual(self.candidates()[0]["acceptance"], "met")
        self.capture.forget("claude", "s-2", owner="platform", approval_ref="user")
        self.run_at(at(20, 4))
        (kept,) = self.candidates()
        self.assertEqual((kept["acceptance"], kept["rechecks"]), ("unverified", []))

    def test_capture_quality_and_missing_end_are_candidates(self) -> None:
        self.session("s-1", 17, end=False)
        self.run_at(at(18))
        patterns = {c["pattern"] for c in self.candidates()}
        self.assertIn("session-without-end", patterns)

    def test_promotion_needs_review_and_never_makes_a_current_memory(self) -> None:
        self.session("s-1", 17, failures=3)
        self.run_at(at(18))
        (candidate,) = self.candidates()
        with self.assertRaisesRegex(ANALYSIS.AnalysisError, "ANALYSIS_NOT_ACCEPTED"):
            self.analysis.promote(
                candidate["candidate_id"], to="memory", owner="platform"
            )
        self.analysis.review(
            candidate["candidate_id"], decision="accepted", owner="reviewer"
        )
        promoted = self.analysis.promote(
            candidate["candidate_id"], to="memory", owner="platform"
        )
        memory = MEMORY.Store.open(self.root).get(promoted["memory_id"])
        self.assertEqual(memory["eligibility"], "candidate")
        self.assertNotIn(PRIVATE_TEXT, json.dumps(memory))

    def accepted(self):
        self.session("s-1", 17, failures=3)
        self.run_at(at(18))
        (candidate,) = self.candidates()
        identifier = candidate["candidate_id"]
        self.analysis.review(identifier, decision="accepted", owner="reviewer")
        return identifier

    def memories(self):
        with sqlite3.connect(MEMORY.Store.open(self.root).path) as connection:
            return connection.execute("select count(*) from memory").fetchone()[0]

    def test_promotion_needs_the_content_that_was_reviewed(self) -> None:
        identifier = self.accepted()
        self.session("s-2", 17, failures=2)  # the same day now counts five
        self.run_at(at(18, 6))
        with self.assertRaisesRegex(ANALYSIS.AnalysisError, "ANALYSIS_REVIEW_STALE"):
            self.analysis.promote(identifier, to="memory", owner="platform")
        self.assertEqual(self.memories(), 0)

    def test_an_interrupted_promotion_finishes_once(self) -> None:
        identifier = self.accepted()
        real = ANALYSIS.Analysis._finish_promotion
        with mock.patch.object(
            ANALYSIS.Analysis, "_finish_promotion", side_effect=OSError("crash")
        ):
            with self.assertRaises(OSError):
                self.analysis.promote(identifier, to="memory", owner="platform")
        self.assertEqual(self.memories(), 1)
        with self.assertRaisesRegex(ANALYSIS.AnalysisError, "ANALYSIS_PROMOTING"):
            self.analysis.review(identifier, decision="rejected", owner="reviewer")
        self.assertIs(ANALYSIS.Analysis._finish_promotion, real)
        first = self.analysis.promote(identifier, to="memory", owner="platform")
        self.assertEqual(self.memories(), 1)
        with self.assertRaisesRegex(ANALYSIS.AnalysisError, "ANALYSIS_PROMOTED"):
            self.analysis.promote(identifier, to="memory", owner="platform")
        self.assertTrue(first["memory_id"].startswith("mem-"))

    def test_an_erased_memory_is_not_promoted_again(self) -> None:
        identifier = self.accepted()
        with mock.patch.object(
            ANALYSIS.Analysis, "_finish_promotion", side_effect=OSError("crash")
        ):
            with self.assertRaises(OSError):
                self.analysis.promote(identifier, to="memory", owner="platform")
        store = MEMORY.Store.open(self.root)
        with sqlite3.connect(store.path) as connection:
            (memory_id,) = connection.execute("select memory_id from memory").fetchone()
        store.erase(memory_id, owner="platform", approval_ref="user:test")
        for _ in range(2):
            with self.assertRaisesRegex(
                ANALYSIS.AnalysisError, "ANALYSIS_PROMOTION_ERASED"
            ):
                self.analysis.promote(identifier, to="memory", owner="platform")
        self.assertEqual(self.memories(), 0)
        (candidate,) = self.candidates()
        self.assertIsNone(candidate["promoted_to"])

    def test_timer_units_schedule_daily_with_catch_up(self) -> None:
        timer, service = ANALYSIS.unit_text(self.root)
        self.assertIn("OnCalendar=*-*-* 03:00:00 Asia/Seoul", timer)
        self.assertIn("Persistent=true", timer)
        self.assertIn("Type=oneshot", service)
        self.assertIn("run --trigger scheduled", service)
        self.assertIn('"', service.split("ExecStart=", 1)[1].splitlines()[0])
        odd = self.base / "a b%c"
        _, quoted = ANALYSIS.unit_text(odd)
        self.assertIn("a b%%c", quoted)
        self.assertIn("TimeoutStartSec=", service)
        self.assertNotIn("claude", service + timer)


if __name__ == "__main__":
    unittest.main()
