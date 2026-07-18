"""Focused contracts for ACER-003 migration-result validation."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
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
    def test_first_two_atomic_batches_are_complete_and_additive(self) -> None:
        validator = load_validator()

        counts = validator.validate_active_corpus_migrations(ROOT)

        self.assertEqual(
            counts,
            {
                "batches": 2,
                "records": 4,
                "baseRecords": 31,
                "archiveRecords": 35,
                "baseHistoricalLinks": 202,
                "addedHistoricalLinks": 31,
                "historicalLinks": 233,
                "secretClean": 4,
                "repairedConsumers": 7,
            },
        )

    def test_closed_negative_matrix_covers_required_batch_boundaries(self) -> None:
        validator = load_validator()

        executed = validator.self_test_case_names(ROOT)

        self.assertEqual(executed, validator.REQUIRED_SELF_TEST_CASES)
        self.assertEqual(
            executed,
            {
                "partial-second-pair",
                "skipped-first-eligible-batch",
                "skipped-second-eligible-batch",
                "reordered-eligible-batches",
                "prior-batch-evidence-drift",
                "source-still-current",
                "archive-payload-byte-drift",
                "wrong-first-rollback-parent",
                "wrong-second-rollback-parent",
                "missing-index-row",
                "duplicate-index-row",
                "direct-current-link",
                "duplicate-original-owner",
                "rogue-extra-archive",
                "unsafe-path",
                "hostile-git-steering",
                "self-referential-batch-commit",
            },
        )

    def test_committed_first_batch_semantics_remain_stable(self) -> None:
        validator = load_validator()
        _eligibility, migration = validator.load_documents(ROOT)
        canonical = json.dumps(
            migration["batches"][0], sort_keys=True, separators=(",", ":")
        ).encode("utf-8")

        self.assertEqual(
            hashlib.sha256(canonical).hexdigest(),
            "6c984f882f245fb40c02e0d5875064bd899cac2d94194c3a99fc2fca26961a70",  # pragma: allowlist secret
        )

    def test_wrong_second_rollback_parent_fails_closed(self) -> None:
        validator = load_validator()
        eligibility, migration = validator.load_documents(ROOT)
        mutated = copy.deepcopy(migration)
        mutated["batches"][1]["rollbackParentCommit"] = "0" * 40

        with self.assertRaises(validator.MigrationError) as raised:
            validator.validate_ledger_document(mutated, eligibility)

        self.assertEqual(
            str(raised.exception),
            "MIGRATION-ROLLBACK docs/90.references/data/active-corpus-migration-results.json",
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
