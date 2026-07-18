"""Focused contracts for ACER-003 migration-result validation."""

from __future__ import annotations

import copy
import importlib.util
import os
import pathlib
import unittest
from unittest import mock


ROOT = pathlib.Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate-active-corpus-migrations.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("active_corpus_migrations", VALIDATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError("migration validator is unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ActiveCorpusMigrationTests(unittest.TestCase):
    def test_first_atomic_batch_is_complete_and_additive(self) -> None:
        validator = load_validator()

        counts = validator.validate_active_corpus_migrations(ROOT)

        self.assertEqual(
            counts,
            {
                "batches": 1,
                "records": 2,
                "baseRecords": 31,
                "archiveRecords": 33,
                "baseHistoricalLinks": 202,
                "addedHistoricalLinks": 16,
                "historicalLinks": 218,
                "secretClean": 2,
                "repairedConsumers": 6,
            },
        )

    def test_closed_negative_matrix_covers_required_batch_boundaries(self) -> None:
        validator = load_validator()

        executed = validator.self_test_case_names(ROOT)

        self.assertEqual(executed, validator.REQUIRED_SELF_TEST_CASES)
        self.assertEqual(
            executed,
            {
                "partial-pair",
                "wrong-eligible-batch",
                "reordered-eligible-batch",
                "source-still-current",
                "archive-payload-byte-drift",
                "wrong-rollback-parent",
                "missing-index-row",
                "extra-index-row",
                "direct-current-link",
                "duplicate-original-owner",
                "unsafe-path",
                "hostile-git-steering",
                "self-referential-batch-commit",
            },
        )

    def test_ledger_is_closed_and_forbids_a_batch_commit_identity(self) -> None:
        validator = load_validator()
        eligibility, migration = validator.load_documents(ROOT)
        mutated = copy.deepcopy(migration)
        mutated["batches"][0]["batchCommit"] = "0" * 40

        with self.assertRaises(validator.MigrationError) as raised:
            validator.validate_ledger_document(mutated, eligibility)

        self.assertEqual(
            str(raised.exception),
            "MIGRATION-SCHEMA docs/90.references/data/active-corpus-migration-results.json",
        )

    def test_eligible_prefix_rejects_a_skipped_first_pair(self) -> None:
        validator = load_validator()
        eligibility, migration = validator.load_documents(ROOT)
        mutated = copy.deepcopy(migration)
        mutated["batches"][0]["pairKey"] = (
            "2026-07-12-protected-surface-supply-chain-hardening"
        )

        with self.assertRaises(validator.MigrationError) as raised:
            validator.validate_ledger_document(mutated, eligibility)

        self.assertEqual(
            str(raised.exception),
            "MIGRATION-ELIGIBLE-PREFIX docs/90.references/data/active-corpus-migration-results.json",
        )

    def test_unsafe_path_is_value_free(self) -> None:
        validator = load_validator()

        with self.assertRaises(validator.MigrationError) as raised:
            validator.validate_path("../forged\nPASS")

        self.assertEqual(
            str(raised.exception),
            "MIGRATION-PATH docs/90.references/data/active-corpus-migration-results.json",
        )

    def test_git_environment_drops_hostile_steering(self) -> None:
        validator = load_validator()
        hostile = {
            "GIT_CONFIG_GLOBAL": "sentinel-global",
            "GIT_OBJECT_DIRECTORY": "sentinel-object",
            "GIT_ALTERNATE_OBJECT_DIRECTORIES": "sentinel-alternate",
            "GIT_TERMINAL_PROMPT": "1",
        }

        with mock.patch.dict(os.environ, hostile, clear=False):
            environment = validator.safe_git_environment()

        self.assertNotIn("GIT_OBJECT_DIRECTORY", environment)
        self.assertNotIn("GIT_ALTERNATE_OBJECT_DIRECTORIES", environment)
        self.assertEqual(environment["GIT_CONFIG_GLOBAL"], os.devnull)
        self.assertEqual(environment["GIT_CONFIG_SYSTEM"], os.devnull)
        self.assertEqual(environment["GIT_GRAFT_FILE"], os.devnull)
        self.assertEqual(environment["GIT_CONFIG_NOSYSTEM"], "1")
        self.assertEqual(environment["GIT_NO_LAZY_FETCH"], "1")
        self.assertEqual(environment["GIT_NO_REPLACE_OBJECTS"], "1")
        self.assertEqual(environment["GIT_OPTIONAL_LOCKS"], "0")
        self.assertEqual(environment["GIT_TERMINAL_PROMPT"], "0")
        self.assertEqual(environment["LC_ALL"], "C")


if __name__ == "__main__":
    unittest.main()
