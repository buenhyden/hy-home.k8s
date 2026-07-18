"""Focused contract tests for the ACER-002 eligibility ledger."""

from __future__ import annotations

import importlib.util
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate-active-corpus-eligibility.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("active_corpus_eligibility", VALIDATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError("eligibility validator is unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ActiveCorpusEligibilityTests(unittest.TestCase):
    def test_pinned_ledger_is_complete_and_fail_closed(self) -> None:
        validator = load_validator()

        counts = validator.validate_active_corpus_eligibility(ROOT)

        self.assertEqual(
            counts,
            {"candidates": 110, "eligible": 12, "defer": 98, "controls": 2},
        )

    def test_rejects_unsafe_path_without_echoing_payload(self) -> None:
        validator = load_validator()

        with self.assertRaises(validator.EligibilityError) as raised:
            validator.validate_path("../forged\nPASS")

        self.assertEqual(str(raised.exception), "ELIGIBILITY-PATH docs/90.references/data/active-corpus-eligibility-ledger.json")

    def test_closed_self_test_matrix_covers_the_required_negative_boundaries(self) -> None:
        validator = load_validator()

        executed = validator.self_test_case_names(ROOT)
        self.assertTrue(validator.REQUIRED_SELF_TEST_CASES <= executed)
        self.assertEqual(len(executed), 53)

    def test_eligible_consumer_enumeration_includes_pinned_non_markdown_authority(self) -> None:
        validator = load_validator()
        ledger = validator.build_expected_ledger(ROOT)
        row = next(
            item
            for item in ledger["candidateRows"]
            if item["path"]
            == "docs/04.execution/plans/2026-07-12-affected-surface-agent-qa.md"
        )

        self.assertIn(validator.CENSUS_PATH, row["trackedCurrentConsumers"])
        self.assertIn(validator.MIGRATION_LEDGER_PATH, row["trackedCurrentConsumers"])
        self.assertNotIn(
            "docs/04.execution/tasks/2026-07-12-affected-surface-agent-qa.md",
            row["trackedCurrentConsumers"],
        )

    def test_defer_axes_distinguish_orphan_zero_link_and_owner_key_gap(self) -> None:
        validator = load_validator()
        rows = {
            item["path"]: item
            for item in validator.build_expected_ledger(ROOT)["candidateRows"]
        }

        orphan = rows["docs/04.execution/plans/2026-06-02-phase-1-decision-follow-up.md"]
        zero_link = rows["docs/04.execution/plans/2026-05-09-github-qa-ci-remediation.md"]
        owner_gap = rows["docs/04.execution/plans/2026-07-12-document-contract-registry.md"]
        self.assertIn("pair-completeness", orphan["missingAxes"])
        self.assertIn("authoritative-upstream-spec", zero_link["missingAxes"])
        self.assertIn("ledger-current-owner-lineage", owner_gap["missingAxes"])
        self.assertNotEqual(orphan["missingAxes"], zero_link["missingAxes"])

    def test_owner_key_gap_rows_have_resolved_partial_evidence(self) -> None:
        validator = load_validator()
        rows = {
            item["path"]: item
            for item in validator.build_expected_ledger(ROOT)["candidateRows"]
        }
        for key, (spec, prd, ard) in validator.OWNER_KEY_GAP_LINEAGE.items():
            for root, kind in (("plans", "plan"), ("tasks", "task")):
                path = f"docs/04.execution/{root}/{key}.md"
                row = rows[path]
                self.assertEqual(row["kind"], kind)
                self.assertEqual(
                    row["upstream"],
                    {"prd": prd, "ard": ard, "spec": spec, "state": "tranche", "completion": "done"},
                )
                self.assertEqual(row["missingAxes"], ["ledger-current-owner-lineage"])
                self.assertEqual(row["authority"], "owner-key-gap-resolved-partial-evidence")
                self.assertEqual(len(row["reciprocalLinks"]), 1)
                self.assertEqual(len(row["specLinks"]), 1)
                self.assertEqual(len(row["closureReferences"]), 2)

    def test_targeted_runner_cases_reach_distinct_expected_diagnostics(self) -> None:
        validator = load_validator()

        results = validator.targeted_runner_case_results(ROOT)

        expected = {
            "missing-eligible-reverse-spec": (
                "ELIGIBILITY-REVERSE-SPEC",
                "docs/04.execution/plans/2026-07-12-affected-surface-agent-qa.md",
            ),
            "missing-eligible-migration-row": (
                "ELIGIBILITY-MIGRATION-MISSING",
                "docs/04.execution/plans/2026-07-12-affected-surface-agent-qa.md",
            ),
            "wrong-eligible-migration-decision": (
                "ELIGIBILITY-MIGRATION-SCHEMA",
                "docs/04.execution/plans/2026-07-12-affected-surface-agent-qa.md",
            ),
            "empty-eligible-owner-relation": (
                "ELIGIBILITY-MIGRATION-SCHEMA",
                "docs/04.execution/plans/2026-07-12-affected-surface-agent-qa.md",
            ),
            "wrong-control-activation-identity": (
                "ELIGIBILITY-CONTROLS",
                "docs/90.references/data/active-corpus-eligibility-ledger.json",
            ),
        }
        self.assertEqual(results, expected)
        self.assertEqual(set(validator.TARGETED_RUNNER_CASES), set(expected))
        self.assertEqual(
            {case.expected_code for case in validator.TARGETED_RUNNER_CASES.values()},
            {code for code, _path in expected.values()},
        )
        self.assertEqual(
            len({id(case.mutate) for case in validator.TARGETED_RUNNER_CASES.values()}),
            len(expected),
        )


if __name__ == "__main__":
    unittest.main()
