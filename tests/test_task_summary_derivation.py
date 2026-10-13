"""Shared Task row summary derivation (readers derive an omitted multi-row summary)."""

from __future__ import annotations

import sys
import unittest
from dataclasses import replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import document_contracts as contracts  # noqa: E402



class TaskSummaryDerivationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        registry = contracts.load_registry(ROOT)
        cls.binding = next(
            p for p in registry.profiles if p.profile_id == "sdlc/task"
        ).body_contract.task_execution

    def derive(self, states, binding=None):
        helper = getattr(contracts, "derive_task_summary", None)
        self.assertTrue(
            callable(helper), "shared derive_task_summary helper is required"
        )
        return helper(states, binding or self.binding)

    def test_current_aggregation_priority_and_terminal_mixtures(self):
        cases = [
            (["draft"], "draft"),
            (["ready"], "ready"),
            (["ready", "draft"], "ready"),
            (["completed", "draft"], "in-progress"),
            (["completed", "ready"], "in-progress"),
            (["in-progress", "cancelled"], "in-progress"),
            (["blocked", "completed"], "blocked"),
            (["completed", "completed"], "completed"),
            (["completed", "cancelled"], "cancelled"),
            (["cancelled", "draft"], "draft"),
        ]
        for states, expected in cases:
            with self.subTest(states=states):
                original = tuple(states)
                self.assertEqual(self.derive(states), expected)
                self.assertEqual(tuple(states), original)

    def test_historical_queued_summary_is_preserved(self):
        binding = replace(
            self.binding,
            summary_rule="task-items-v1",
            result_states={
                "draft": ("NOT_RUN",),
                "queued": ("NOT_RUN",),
                "in-progress": ("PASS",),
                "blocked": ("DEFER",),
                "completed": ("PASS",),
                "cancelled": ("NOT_RUN",),
            },
        )
        for states, expected in [
            (["queued", "draft"], "queued"),
            (["completed", "queued"], "in-progress"),
            (["blocked", "queued"], "blocked"),
            (["cancelled", "completed"], "cancelled"),
        ]:
            with self.subTest(states=states):
                self.assertEqual(self.derive(states, binding), expected)

    def test_empty_and_unknown_states_fail(self):
        for states in ([], ["invented"], ["frontmatter"]):
            with self.subTest(states=states):
                with self.assertRaises(ValueError):
                    self.derive(states)


if __name__ == "__main__":
    unittest.main()
