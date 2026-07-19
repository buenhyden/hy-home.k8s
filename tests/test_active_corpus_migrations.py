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

PROPOSED_FIFTH_BATCH = {
    "sequence": 5,
    "batchId": "ACER-003-005",
    "pairKey": "2026-07-16-document-schema-and-lifecycle-contract",
    "status": "complete",
    "completedOn": "2026-07-18",
    "upstreamSpec": "docs/03.specs/035-document-schema-and-lifecycle-contract/spec.md",
    "program": {
        "prd": "006",
        "ard": "0009",
        "lineage": "tranche",
    },
    "currentClosureOwner": "docs/03.specs/035-document-schema-and-lifecycle-contract/spec.md",
    "archiveNavigationBoundary": "docs/98.archive/README.md#document-index",
    "rollbackParentCommit": "4de4c3e9ddb44949157399a1c71de788511d8a56",  # pragma: allowlist secret
    "repairedConsumers": [
        "docs/03.specs/035-document-schema-and-lifecycle-contract/spec.md",
        "docs/04.execution/plans/README.md",
        "docs/04.execution/tasks/2026-07-17-archive-record-and-workspace-boundary.md",
        "docs/04.execution/tasks/README.md",
        "docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md",
    ],
    "validationResult": "PASS",
    "records": [
        {
            "kind": "plan",
            "originalPath": "docs/04.execution/plans/2026-07-16-document-schema-and-lifecycle-contract.md",
            "archivePath": "docs/98.archive/04.execution/plans/2026-07-16-document-schema-and-lifecycle-contract.md",
            "originalType": "plan",
            "sourceCommit": "a12aedfb71ccabd329dabc83bd2863474d1126b0",  # pragma: allowlist secret
            "sourceBlob": "156f5954d0be9985d1c730380892d079163d33f4",  # pragma: allowlist secret
            "payloadBytes": 33047,
            "payloadSha256": "21196dd188f3d5400b65ccd8b8d837f7209a6f34b901d2082a5c9d0de5db1d9d",  # pragma: allowlist secret
            "historicalLinks": 8,
            "archiveReason": "completed-lineage",
            "replacement": None,
            "validationResult": "PASS",
        },
        {
            "kind": "task",
            "originalPath": "docs/04.execution/tasks/2026-07-16-document-schema-and-lifecycle-contract.md",
            "archivePath": "docs/98.archive/04.execution/tasks/2026-07-16-document-schema-and-lifecycle-contract.md",
            "originalType": "task",
            "sourceCommit": "a12aedfb71ccabd329dabc83bd2863474d1126b0",  # pragma: allowlist secret
            "sourceBlob": "cfc97978ee1217ff34b7bc823a2da172098e2209",  # pragma: allowlist secret
            "payloadBytes": 26367,
            "payloadSha256": "2e3ad60792196d7918e7909f9bb8e275194f0100922cd1f767cf779f906d7b08",  # pragma: allowlist secret
            "historicalLinks": 14,
            "archiveReason": "completed-lineage",
            "replacement": None,
            "validationResult": "PASS",
        },
    ],
}

PROPOSED_SIXTH_BATCH = {
    "sequence": 6,
    "batchId": "ACER-003-006",
    "pairKey": "2026-07-17-archive-record-and-workspace-boundary",
    "status": "complete",
    "completedOn": "2026-07-18",
    "upstreamSpec": "docs/03.specs/036-archive-record-and-workspace-boundary/spec.md",
    "program": {"prd": "006", "ard": "0009", "lineage": "tranche"},
    "currentClosureOwner": "docs/03.specs/036-archive-record-and-workspace-boundary/spec.md",
    "archiveNavigationBoundary": "docs/98.archive/README.md#document-index",
    "rollbackParentCommit": "420f8a582dee69f3c0902026b49667af803a96c1",  # pragma: allowlist secret
    "repairedConsumers": [
        "docs/03.specs/036-archive-record-and-workspace-boundary/spec.md",
        "docs/03.specs/README.md",
        "docs/04.execution/plans/README.md",
        "docs/04.execution/tasks/2026-07-18-active-corpus-and-execution-retention.md",
        "docs/04.execution/tasks/README.md",
        "docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md",
    ],
    "validationResult": "PASS",
    "records": [
        {
            "kind": "plan",
            "originalPath": "docs/04.execution/plans/2026-07-17-archive-record-and-workspace-boundary.md",
            "archivePath": "docs/98.archive/04.execution/plans/2026-07-17-archive-record-and-workspace-boundary.md",
            "originalType": "plan",
            "sourceCommit": "a12aedfb71ccabd329dabc83bd2863474d1126b0",  # pragma: allowlist secret
            "sourceBlob": "01f31e78e6a74491211b2c4d65282fa992af28ee",  # pragma: allowlist secret
            "payloadBytes": 21539,
            "payloadSha256": "dff92c9051c654604c46e40fe8188d068c6f4d7eacb83877b485eb6925312b23",  # pragma: allowlist secret
            "historicalLinks": 14,
            "archiveReason": "completed-lineage",
            "replacement": None,
            "validationResult": "PASS",
        },
        {
            "kind": "task",
            "originalPath": "docs/04.execution/tasks/2026-07-17-archive-record-and-workspace-boundary.md",
            "archivePath": "docs/98.archive/04.execution/tasks/2026-07-17-archive-record-and-workspace-boundary.md",
            "originalType": "task",
            "sourceCommit": "a12aedfb71ccabd329dabc83bd2863474d1126b0",  # pragma: allowlist secret
            "sourceBlob": "e40edd14c8bef4983907a75d7cc7b823412163e6",  # pragma: allowlist secret
            "payloadBytes": 36397,
            "payloadSha256": "f3badfc88f43281138d82ace386316e0d3f69bbc5a31ea9ea210f9b6597524fb",  # pragma: allowlist secret
            "historicalLinks": 19,
            "archiveReason": "completed-lineage",
            "replacement": None,
            "validationResult": "PASS",
        },
    ],
}


def load_validator():
    spec = importlib.util.spec_from_file_location("active_corpus_migrations", VALIDATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError("migration validator is unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ActiveCorpusMigrationTests(unittest.TestCase):
    def test_all_six_atomic_batches_are_complete_and_additive(self) -> None:
        validator = load_validator()

        counts = validator.validate_active_corpus_migrations(ROOT)

        self.assertEqual(
            counts,
            {
                "batches": 6,
                "records": 12,
                "baseRecords": 31,
                "archiveRecords": 43,
                "baseHistoricalLinks": 202,
                "addedHistoricalLinks": 160,
                "historicalLinks": 362,
                "secretClean": 12,
                "repairedConsumers": 15,
            },
        )

    def test_staged_consumer_retirement_is_closed_to_migrated_originals(self) -> None:
        validator = load_validator()
        _eligibility, migration = validator.load_documents(ROOT)
        retired_repaired_by_batch_six = {
            "docs/04.execution/plans/2026-07-16-document-schema-and-lifecycle-contract.md",
            "docs/04.execution/tasks/2026-07-16-document-schema-and-lifecycle-contract.md",
            "docs/04.execution/tasks/2026-07-17-archive-record-and-workspace-boundary.md",
        }
        staged_paths = set(validator._git_paths(ROOT)) - retired_repaired_by_batch_six

        repaired = validator._validate_repaired_consumer_inventory(
            migration, staged_paths
        )

        self.assertTrue(retired_repaired_by_batch_six <= repaired)
        migrated_originals = {
            str(row["originalPath"])
            for row in validator._record_rows(migration)
        }
        self.assertTrue(retired_repaired_by_batch_six <= migrated_originals)

        missing_current = staged_paths - {
            "docs/04.execution/tasks/2026-07-18-active-corpus-and-execution-retention.md"
        }
        with self.assertRaises(validator.MigrationError) as missing:
            validator._validate_repaired_consumer_inventory(
                migration, missing_current
            )
        self.assertEqual(
            str(missing.exception),
            "MIGRATION-CONSUMERS docs/90.references/data/active-corpus-migration-results.json",
        )

        rogue = copy.deepcopy(migration)
        rogue["batches"][5]["repairedConsumers"].append(
            "docs/04.execution/tasks/rogue-missing-consumer.md"
        )
        with self.assertRaises(validator.MigrationError) as raised:
            validator._validate_repaired_consumer_inventory(rogue, staged_paths)

        self.assertEqual(
            str(raised.exception),
            "MIGRATION-CONSUMERS docs/90.references/data/active-corpus-migration-results.json",
        )

    def test_incomplete_five_batch_prefix_is_rejected(self) -> None:
        validator = load_validator()
        eligibility, migration = validator.load_documents(ROOT)
        proposed = copy.deepcopy(migration)
        proposed["batches"] = [
            *copy.deepcopy(migration["batches"][:4]),
            copy.deepcopy(PROPOSED_FIFTH_BATCH),
        ]
        proposed["counts"] = {
            "batches": 5,
            "records": 10,
            "archiveRecords": 41,
            "historicalLinksAdded": 127,
            "historicalLinks": 329,
        }

        with self.assertRaises(validator.MigrationError) as raised:
            validator.validate_ledger_document(proposed, eligibility)
        self.assertEqual(
            str(raised.exception),
            "MIGRATION-ELIGIBLE-PREFIX docs/90.references/data/active-corpus-migration-results.json",
        )

    def test_exact_proposed_sixth_prefix_is_accepted(self) -> None:
        validator = load_validator()
        eligibility, migration = validator.load_documents(ROOT)
        proposed = copy.deepcopy(migration)
        proposed["batches"] = [
            *copy.deepcopy(migration["batches"][:5]),
            copy.deepcopy(PROPOSED_SIXTH_BATCH),
        ]
        proposed["counts"] = {
            "batches": 6,
            "records": 12,
            "archiveRecords": 43,
            "historicalLinksAdded": 160,
            "historicalLinks": 362,
        }

        self.assertEqual(
            validator.validate_ledger_document(proposed, eligibility),
            {
                "batches": 6,
                "records": 12,
                "archiveRecords": 43,
                "historicalLinksAdded": 160,
                "historicalLinks": 362,
                "repairedConsumers": 34,
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
                "skipped-third-eligible-batch",
                "skipped-fourth-eligible-batch",
                "skipped-fifth-eligible-batch",
                "skipped-sixth-eligible-batch",
                "reordered-eligible-batches",
                "prior-batch-evidence-drift",
                "prior-second-batch-drift",
                "prior-third-batch-drift",
                "prior-fourth-batch-drift",
                "prior-fifth-batch-drift",
                "partial-fourth-pair",
                "partial-fifth-pair",
                "partial-sixth-pair",
                "source-still-current",
                "archive-payload-byte-drift",
                "wrong-first-rollback-parent",
                "wrong-second-rollback-parent",
                "wrong-third-rollback-parent",
                "wrong-fourth-rollback-parent",
                "wrong-fifth-rollback-parent",
                "wrong-sixth-rollback-parent",
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

    def test_committed_five_batch_prefix_semantics_remain_stable(self) -> None:
        validator = load_validator()
        _eligibility, migration = validator.load_documents(ROOT)
        canonical = json.dumps(
            migration["batches"][:5], sort_keys=True, separators=(",", ":")
        ).encode("utf-8")

        self.assertEqual(
            hashlib.sha256(canonical).hexdigest(),
            "5e5e4eea447ac514734aacaa9d6bcd3a26824c3a88a1daa8343094034babb50b",  # pragma: allowlist secret
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

    def test_wrong_third_rollback_parent_fails_closed(self) -> None:
        validator = load_validator()
        eligibility, migration = validator.load_documents(ROOT)
        mutated = copy.deepcopy(migration)
        mutated["batches"][2]["rollbackParentCommit"] = "0" * 40

        with self.assertRaises(validator.MigrationError) as raised:
            validator.validate_ledger_document(mutated, eligibility)

        self.assertEqual(
            str(raised.exception),
            "MIGRATION-ROLLBACK docs/90.references/data/active-corpus-migration-results.json",
        )

    def test_wrong_fourth_rollback_parent_fails_closed(self) -> None:
        validator = load_validator()
        eligibility, migration = validator.load_documents(ROOT)
        proposed = copy.deepcopy(migration)
        proposed["batches"][3]["rollbackParentCommit"] = "0" * 40

        with self.assertRaises(validator.MigrationError) as raised:
            validator.validate_ledger_document(proposed, eligibility)

        self.assertEqual(
            str(raised.exception),
            "MIGRATION-ROLLBACK docs/90.references/data/active-corpus-migration-results.json",
        )

    def test_wrong_fifth_rollback_parent_fails_closed(self) -> None:
        validator = load_validator()
        eligibility, migration = validator.load_documents(ROOT)
        proposed = copy.deepcopy(migration)
        proposed["batches"][4]["rollbackParentCommit"] = "0" * 40

        with self.assertRaises(validator.MigrationError) as raised:
            validator.validate_ledger_document(proposed, eligibility)

        self.assertEqual(
            str(raised.exception),
            "MIGRATION-ROLLBACK docs/90.references/data/active-corpus-migration-results.json",
        )

    def test_wrong_sixth_rollback_parent_fails_closed(self) -> None:
        validator = load_validator()
        eligibility, migration = validator.load_documents(ROOT)
        proposed = copy.deepcopy(migration)
        proposed["batches"][5]["rollbackParentCommit"] = "0" * 40

        with self.assertRaises(validator.MigrationError) as raised:
            validator.validate_ledger_document(proposed, eligibility)

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
