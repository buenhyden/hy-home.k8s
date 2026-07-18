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

PROPOSED_THIRD_BATCH = {
    "sequence": 3,
    "batchId": "ACER-003-003",
    "pairKey": "2026-07-14-template-lifecycle-contract-normalization",
    "status": "complete",
    "completedOn": "2026-07-18",
    "upstreamSpec": "docs/03.specs/033-template-lifecycle-contract-normalization/spec.md",
    "program": {
        "prd": "005",
        "ard": "0008",
        "lineage": "follow-up",
    },
    "currentClosureOwner": "docs/03.specs/033-template-lifecycle-contract-normalization/spec.md",
    "archiveNavigationBoundary": "docs/98.archive/README.md#document-index",
    "rollbackParentCommit": "22ad025ed7beb0725095d1ab413a2d5c49f8561c",  # pragma: allowlist secret
    "repairedConsumers": [
        "docs/03.specs/033-template-lifecycle-contract-normalization/spec.md",
        "docs/04.execution/plans/README.md",
        "docs/04.execution/tasks/README.md",
        "docs/90.references/audits/2026-07-11-weia/remediation-roadmap.md",
        "docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md",
    ],
    "validationResult": "PASS",
    "records": [
        {
            "kind": "plan",
            "originalPath": "docs/04.execution/plans/2026-07-14-template-lifecycle-contract-normalization.md",
            "archivePath": "docs/98.archive/04.execution/plans/2026-07-14-template-lifecycle-contract-normalization.md",
            "originalType": "plan",
            "sourceCommit": "a12aedfb71ccabd329dabc83bd2863474d1126b0",  # pragma: allowlist secret
            "sourceBlob": "3a49ac07d7d2808e63a8550f67786d69a451c6df",  # pragma: allowlist secret
            "payloadBytes": 51960,
            "payloadSha256": "102ffdabc9e0b839c449f00dd511355bd857ce49f8c423ffd8cfcef8491ffdcc",  # pragma: allowlist secret
            "historicalLinks": 25,
            "archiveReason": "completed-lineage",
            "replacement": None,
            "validationResult": "PASS",
        },
        {
            "kind": "task",
            "originalPath": "docs/04.execution/tasks/2026-07-14-template-lifecycle-contract-normalization.md",
            "archivePath": "docs/98.archive/04.execution/tasks/2026-07-14-template-lifecycle-contract-normalization.md",
            "originalType": "task",
            "sourceCommit": "a12aedfb71ccabd329dabc83bd2863474d1126b0",  # pragma: allowlist secret
            "sourceBlob": "424658d865205523f066de87428b96c2aee9926a",  # pragma: allowlist secret
            "payloadBytes": 8415,
            "payloadSha256": "717c445c3b51db3ef286f342ad3a997063285fc170afe214af306cc0d8d48381",  # pragma: allowlist secret
            "historicalLinks": 17,
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
    def test_first_three_atomic_batches_are_complete_and_additive(self) -> None:
        validator = load_validator()

        counts = validator.validate_active_corpus_migrations(ROOT)

        self.assertEqual(
            counts,
            {
                "batches": 3,
                "records": 6,
                "baseRecords": 31,
                "archiveRecords": 37,
                "baseHistoricalLinks": 202,
                "addedHistoricalLinks": 73,
                "historicalLinks": 275,
                "secretClean": 6,
                "repairedConsumers": 8,
            },
        )

    def test_exact_proposed_third_prefix_is_accepted(self) -> None:
        validator = load_validator()
        eligibility, migration = validator.load_documents(ROOT)
        proposed = copy.deepcopy(migration)
        proposed["batches"] = [
            *copy.deepcopy(migration["batches"][:2]),
            copy.deepcopy(PROPOSED_THIRD_BATCH),
        ]
        proposed["counts"] = {
            "batches": 3,
            "records": 6,
            "archiveRecords": 37,
            "historicalLinksAdded": 73,
            "historicalLinks": 275,
        }

        self.assertEqual(
            validator.validate_ledger_document(proposed, eligibility),
            {
                "batches": 3,
                "records": 6,
                "archiveRecords": 37,
                "historicalLinksAdded": 73,
                "historicalLinks": 275,
                "repairedConsumers": 17,
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
                "reordered-eligible-batches",
                "prior-batch-evidence-drift",
                "prior-second-batch-drift",
                "source-still-current",
                "archive-payload-byte-drift",
                "wrong-first-rollback-parent",
                "wrong-second-rollback-parent",
                "wrong-third-rollback-parent",
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

    def test_committed_two_batch_prefix_semantics_remain_stable(self) -> None:
        validator = load_validator()
        _eligibility, migration = validator.load_documents(ROOT)
        canonical = json.dumps(
            migration["batches"][:2], sort_keys=True, separators=(",", ":")
        ).encode("utf-8")

        self.assertEqual(
            hashlib.sha256(canonical).hexdigest(),
            "07a94683e8980ab6c7a39e183826fe8c56cc0ff3a3d173327935eafead478364",  # pragma: allowlist secret
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
