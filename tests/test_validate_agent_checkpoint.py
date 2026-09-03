#!/usr/bin/env python3
"""Focused tests for the synthetic checkpoint and memory lifecycle contract."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import os
import stat
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest import mock

from tests.agent_checkpoint_mutations import (
    apply_duplicate_key_mutation,
    apply_mutation,
)


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPOSITORY_ROOT / "scripts/validate-agent-checkpoint.py"
SCHEMA_PATH = (
    REPOSITORY_ROOT / "docs/00.agent-governance/contracts/agent-checkpoint.schema.json"
)
FIXTURE_PATH = REPOSITORY_ROOT / "tests/fixtures/agent-checkpoint.json"


def load_module():
    spec = importlib.util.spec_from_file_location(
        "validate_agent_checkpoint", SCRIPT_PATH
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {SCRIPT_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class AgentCheckpointContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_module()
        cls.fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))

    def checkpoint_copy(self):
        return copy.deepcopy(self.fixture["syntheticCheckpoint"])

    def repository_state_copy(self):
        return copy.deepcopy(self.fixture["repositoryState"])

    def assert_rule(
        self,
        checkpoint,
        repository_state,
        expected_rule: str,
    ) -> None:
        with self.assertRaises(self.validator.CheckpointError) as raised:
            self.validator.validate_checkpoint(
                REPOSITORY_ROOT,
                checkpoint,
                repository_state,
                check_repository_contracts=False,
            )
        self.assertEqual(raised.exception.code, expected_rule)

    def test_validator_is_import_safe_and_exposes_checkpoint_api(self) -> None:
        for name in (
            "CheckpointError",
            "decode_json_text",
            "validate_checkpoint",
            "validate_resume",
            "validate_memory_lifecycle",
            "scan_sensitive_payload",
        ):
            self.assertTrue(hasattr(self.validator, name), name)
        self.assertFalse(hasattr(self.validator, "apply_mutation"))
        self.assertFalse(hasattr(self.validator, "main"))

    def test_schema_is_draft_2020_12_and_closed_at_every_object(self) -> None:
        self.assertEqual(
            self.schema["$schema"],
            "https://json-schema.org/draft/2020-12/schema",
        )

        def visit(node):
            if isinstance(node, dict):
                if node.get("type") == "object":
                    self.assertIs(
                        node.get("additionalProperties"),
                        False,
                        node,
                    )
                for value in node.values():
                    visit(value)
            elif isinstance(node, list):
                for value in node:
                    visit(value)

        visit(self.schema)

    def test_valid_synthetic_checkpoint_and_resume_pass(self) -> None:
        self.assertEqual(self.fixture["fixtureVersion"], 2)
        self.assertEqual(self.fixture["syntheticCheckpoint"]["schemaVersion"], 2)
        self.assertEqual(
            self.fixture["syntheticCheckpoint"]["contractVersion"], "1.0.0"
        )
        counts = self.validator.validate_checkpoint(
            REPOSITORY_ROOT,
            self.checkpoint_copy(),
            self.repository_state_copy(),
            check_repository_contracts=False,
        )
        self.assertEqual(counts["memoryClasses"], 4)
        self.assertEqual(counts["completedWork"], 2)
        self.assertEqual(counts["remainingWork"], 2)
        self.assertEqual(counts["validationRecords"], 2)

    def test_only_supported_provider_ids_are_accepted(self) -> None:
        for provider in ("local", "gemini", "antigravity"):
            with self.subTest(provider=provider):
                checkpoint = self.checkpoint_copy()
                checkpoint["identity"]["providerSurfaceId"] = provider
                checkpoint["executor"]["providerId"] = provider
                self.assert_rule(
                    checkpoint, self.repository_state_copy(), "AHLL-CP-SCHEMA"
                )

    def test_executor_membership_comes_from_agent_registry(self) -> None:
        registry = self.validator.load_json(
            REPOSITORY_ROOT, self.validator.REGISTRY_PATH
        )
        role_id = self.fixture["syntheticCheckpoint"]["executor"]["roleId"]
        for mutation in ("missing-role", "unsupported-provider", "duplicate-role"):
            with self.subTest(mutation=mutation):
                changed = copy.deepcopy(registry)
                role = next(row for row in changed["roles"] if row["id"] == role_id)
                if mutation == "missing-role":
                    changed["roles"].remove(role)
                elif mutation == "unsupported-provider":
                    role["supported_providers"] = ["claude"]
                else:
                    changed["roles"].append(copy.deepcopy(role))
                original_load = self.validator.load_json

                def load_contract(root, path):
                    if path == self.validator.REGISTRY_PATH:
                        return changed
                    return original_load(root, path)

                with mock.patch.object(
                    self.validator, "load_json", side_effect=load_contract
                ):
                    with self.assertRaises(self.validator.CheckpointError) as raised:
                        self.validator.validate_checkpoint(
                            REPOSITORY_ROOT,
                            self.checkpoint_copy(),
                            self.repository_state_copy(),
                        )
                self.assertEqual(raised.exception.code, "AHLL-CP-REGISTRY")

    def test_import_api_accepts_supplied_non_synthetic_checkpoint(self) -> None:
        checkpoint = self.checkpoint_copy()
        repository_state = self.repository_state_copy()
        checkpoint["synthetic"] = False
        repository_state["synthetic"] = False
        checkpoint["redaction"]["syntheticMarker"] = None
        counts = self.validator.validate_checkpoint(
            REPOSITORY_ROOT,
            checkpoint,
            repository_state,
            check_repository_contracts=False,
        )
        self.assertEqual(counts["memoryClasses"], 4)

    def test_missing_loop_contract_fails_closed(self) -> None:
        required_inputs = (
            self.validator.SCHEMA_PATH,
            self.validator.REGISTRY_PATH,
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            for relative in required_inputs:
                source = REPOSITORY_ROOT / Path(relative)
                target = root / Path(relative)
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(
                    source.read_text(encoding="utf-8"),
                    encoding="utf-8",
                )
            (root / ".gitignore").write_text(
                ".agent-work/\n",
                encoding="utf-8",
            )

            with self.assertRaises(self.validator.CheckpointError) as raised:
                self.validator.validate_checkpoint(
                    root,
                    self.checkpoint_copy(),
                    self.repository_state_copy(),
                    check_repository_contracts=True,
                )
        self.assertEqual(
            raised.exception.code,
            "AHLL-CP-MISSING-FILE",
        )
        self.assertEqual(raised.exception.exit_code, 2)

    def test_json_read_uses_opened_descriptor_after_final_path_swap(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            nested = root / "nested"
            nested.mkdir()
            payload = nested / "input.json"
            payload.write_text('{"source":"inside"}\n', encoding="utf-8")
            outside = root / "outside.json"
            outside.write_text('{"source":"outside"}\n', encoding="utf-8")
            payload_inode = payload.stat().st_ino
            original_fstat = os.fstat
            swapped = False

            def swap_after_check(descriptor: int):
                nonlocal swapped
                metadata = original_fstat(descriptor)
                if (
                    not swapped
                    and stat.S_ISREG(metadata.st_mode)
                    and metadata.st_ino == payload_inode
                ):
                    swapped = True
                    payload.rename(nested / "input-original.json")
                    payload.symlink_to(outside)
                return metadata

            with mock.patch.object(
                self.validator.os,
                "fstat",
                side_effect=swap_after_check,
            ):
                loaded = self.validator.load_json(
                    root,
                    self.validator.PurePosixPath("nested/input.json"),
                )

            self.assertTrue(swapped)
            self.assertEqual(loaded, {"source": "inside"})

    def test_fixture_covers_all_four_memory_classes_in_order(self) -> None:
        classes = [
            item["classId"]
            for item in self.fixture["syntheticCheckpoint"]["memoryLifecycle"]
        ]
        self.assertEqual(classes, list(self.validator.MEMORY_CLASS_IDS))

    def test_checkpoint_declares_atomic_replace_without_partial_write(self) -> None:
        declaration = self.fixture["syntheticCheckpoint"]["atomicWrite"]
        self.assertTrue(declaration["required"])
        self.assertEqual(
            declaration["strategy"],
            "same-directory-temp-fsync-replace",
        )
        self.assertFalse(declaration["partialWriteAllowed"])
        self.assertEqual(
            declaration["targetPath"],
            ".agent-work/checkpoint.json",
        )

    def test_resume_reobserves_every_repository_identity_axis(self) -> None:
        expected = {
            "repositoryId",
            "taskId",
            "specRef",
            "worktreeId",
            "providerSurfaceId",
            "providerSessionInstanceDigest",
            "namespaceDigest",
            "writerId",
            "writeGeneration",
            "previousCheckpointDigest",
            "writerClaimDigest",
            "branchRef",
            "baseRevision",
            "headRevision",
            "contractVersion",
            "workingStateDigest",
            "ownedPathsDigest",
        }
        self.assertEqual(
            set(self.fixture["repositoryState"]["identity"]),
            expected,
        )
        resume = self.fixture["syntheticCheckpoint"]["resume"]
        self.assertTrue(resume["repositoryStateWins"])
        self.assertEqual(
            tuple(resume["conflictOrder"]),
            self.validator.CONFLICT_ORDER,
        )
        self.assertTrue(resume["rediscoveryRequired"])
        self.assertTrue(resume["recomputeRemainingWork"])
        self.assertFalse(resume["terminalReplayAllowed"])
        self.assertTrue(resume["identityTupleRequired"])
        self.assertTrue(resume["singleWriterRequired"])
        self.assertFalse(resume["duplicateWriterAllowed"])
        self.assertFalse(resume["duplicateResumeAllowed"])
        self.assertEqual(
            resume["overwritePolicy"],
            "compare-generation-and-previous-checkpoint-digest",
        )
        self.assertEqual(resume["acceptedIdentity"], "exact-match-only")
        self.assertEqual(self.fixture["repositoryState"]["activeWriterCount"], 1)
        self.assertEqual(self.fixture["repositoryState"]["activeResumeCount"], 1)

    def test_namespace_and_writer_claim_digests_are_recomputed(self) -> None:
        identity = self.fixture["syntheticCheckpoint"]["identity"]

        def digest(*values):
            payload = "\n".join(str(value) for value in values).encode()
            return "sha256:" + hashlib.sha256(payload).hexdigest()

        self.assertEqual(
            identity["namespaceDigest"],
            digest(
                identity["repositoryId"],
                identity["worktreeId"],
                identity["taskId"],
                identity["providerSurfaceId"],
                identity["providerSessionInstanceDigest"],
            ),
        )
        self.assertEqual(
            identity["writerClaimDigest"],
            digest(
                identity["namespaceDigest"],
                identity["writerId"],
                identity["writeGeneration"],
                identity["previousCheckpointDigest"],
                identity["baseRevision"],
                identity["headRevision"],
            ),
        )
        self.assertEqual(
            identity["providerSurfaceId"],
            self.fixture["syntheticCheckpoint"]["executor"]["providerId"],
        )

    def test_all_terminal_states_are_rejected_for_replay(self) -> None:
        for state in self.validator.TERMINAL_STATES:
            with self.subTest(state=state):
                checkpoint = self.checkpoint_copy()
                checkpoint["repository"]["loopState"] = state
                self.assert_rule(
                    checkpoint,
                    self.repository_state_copy(),
                    "AHLL-CP-TERMINAL-REPLAY",
                )

    def test_all_declared_negative_mutations_fail_with_expected_rule(self) -> None:
        names = set()
        for case in self.fixture["negativeMutations"]:
            with self.subTest(case=case["name"]):
                self.assertNotIn(case["name"], names)
                names.add(case["name"])
                checkpoint = self.checkpoint_copy()
                repository_state = self.repository_state_copy()
                if case["name"] == "duplicate-json-key":
                    with self.assertRaises(self.validator.CheckpointError) as raised:
                        apply_duplicate_key_mutation(self.validator)
                    self.assertEqual(
                        raised.exception.code,
                        case["expectedRule"],
                    )
                    continue
                apply_mutation(
                    checkpoint,
                    repository_state,
                    case["name"],
                )
                self.assert_rule(
                    checkpoint,
                    repository_state,
                    case["expectedRule"],
                )

    def test_mutation_matrix_covers_required_acceptance_boundaries(self) -> None:
        names = {case["name"] for case in self.fixture["negativeMutations"]}
        required = {
            "duplicate-json-key",
            "unknown-checkpoint-field",
            "stale-repository",
            "stale-task",
            "stale-spec",
            "stale-worktree",
            "stale-provider-surface",
            "stale-provider-session",
            "namespace-digest-drift",
            "writer-id-collision",
            "writer-claim-drift",
            "write-generation-stale",
            "previous-checkpoint-overwrite",
            "duplicate-writer",
            "duplicate-resume",
            "provider-executor-surface-mismatch",
            "stale-branch",
            "stale-base",
            "stale-head",
            "stale-contract",
            "stale-working-state",
            "checkpoint-timestamp-order",
            "checkpoint-timestamp-future",
            "checkpoint-timestamp-stale",
            "terminal-replay-completed",
            "terminal-replay-blocked",
            "terminal-replay-escalated",
            "terminal-replay-aborted",
            "completed-work-overflow",
            "validation-summary-overflow",
            "atomic-write-disabled",
            "resume-conflict-order-drift",
            "resume-identity-tuple-disabled",
            "resume-single-writer-disabled",
            "resume-duplicate-writer-enabled",
            "resume-duplicate-resume-enabled",
            "resume-overwrite-policy-drift",
            "resume-accepted-identity-drift",
            "resume-synthetic-mode-mismatch",
            "promotion-evidence-missing",
            "promotion-owner-missing",
            "promotion-review-missing",
            "promotion-redaction-failed",
            "promotion-direct-write",
            "provider-local-not-reobserved",
            "provider-local-direct-canonical",
            "refresh-revision-stale",
            "refresh-basis-drift",
            "refresh-due-before-update",
            "expiry-disposition-missing",
            "archive-gc-provenance-missing",
            "archive-gc-reason-missing",
            "archive-gc-date-missing",
            "archive-gc-original-owner-missing",
            "archive-gc-replacement-owner-missing",
            "repository-conflict-loses",
            "memory-sensitivity-drift",
            "memory-retention-drift",
            "memory-retention-evidence-missing",
            "memory-handoff-owner-missing",
            "memory-handoff-evidence-missing",
            "compaction-retains-transcript",
            "compaction-source-evidence-missing",
            "compaction-replacement-evidence-missing",
            "compaction-identical-digests",
            "compaction-source-owner-missing",
            "compaction-replacement-owner-missing",
            "compaction-review-unapproved",
            "handoff-owner-missing",
            "sensitive-credential-key",
            "sensitive-credential-value",
            "sensitive-secret-key",
            "sensitive-token-key",
            "sensitive-token-value",
            "sensitive-sk-proj-value",
            "sensitive-gho-value",
            "sensitive-xoxp-value",
            "sensitive-aiza-value",
            "sensitive-auth-path-key",
            "sensitive-auth-path-value",
            "sensitive-account-id-key",
            "sensitive-account-id-value",
            "sensitive-raw-prompt-key",
            "sensitive-raw-prompt-value",
            "sensitive-transcript-key",
            "sensitive-transcript-value",
            "sensitive-provider-body-key",
            "sensitive-provider-body-value",
            "sensitive-stdout-key",
            "sensitive-stdout-value",
            "sensitive-stderr-key",
            "sensitive-stderr-value",
            "sensitive-shell-history-key",
            "sensitive-shell-history-value",
            "sensitive-environment-dump-key",
            "sensitive-environment-dump-value",
            "sensitive-private-diagnostics-key",
            "sensitive-private-diagnostics-value",
            "sensitive-user-config-key",
            "sensitive-user-config-value",
        }
        self.assertTrue(required.issubset(names), sorted(required - names))

    def test_provider_local_promotion_requires_repository_reobservation(self) -> None:
        provider_local = next(
            item
            for item in self.fixture["syntheticCheckpoint"]["memoryLifecycle"]
            if item["classId"] == "provider-local-auxiliary"
        )
        promotion = provider_local["promotion"]
        self.assertEqual(promotion["targetClass"], "working-short-term")
        self.assertTrue(promotion["repositoryReobserved"])
        self.assertFalse(promotion["directCanonicalWrite"])
        self.assertEqual(
            promotion["reobservationEvidenceClass"],
            "repo-static",
        )

    def test_lifecycle_records_are_reviewed_redacted_and_provenanced(self) -> None:
        updated = datetime.fromisoformat(
            self.fixture["syntheticCheckpoint"]["identity"]["updatedAtUtc"].replace(
                "Z", "+00:00"
            )
        )
        for record in self.fixture["syntheticCheckpoint"]["memoryLifecycle"]:
            with self.subTest(memory_class=record["classId"]):
                self.assertEqual(record["redactionStatus"], "PASS")
                self.assertEqual(
                    record["sensitivity"]["classification"],
                    "non-sensitive-redacted",
                )
                self.assertFalse(record["sensitivity"]["restrictedContextAllowed"])
                self.assertFalse(record["sensitivity"]["rawContextAllowed"])
                self.assertFalse(record["sensitivity"]["providerPayloadAllowed"])
                self.assertEqual(record["sensitivity"]["reviewStatus"], "approved")
                self.assertTrue(record["canonicalOwner"])
                self.assertTrue(record["refresh"]["basis"])
                self.assertTrue(record["refresh"]["evidenceRefs"])
                due = datetime.fromisoformat(
                    record["refresh"]["refreshDueAtUtc"].replace("Z", "+00:00")
                )
                self.assertGreaterEqual(due, updated)
                self.assertTrue(record["expiry"]["disposition"])
                self.assertTrue(record["retention"]["policy"])
                self.assertEqual(
                    record["retention"]["canonicalDecisionOwner"],
                    record["canonicalOwner"],
                )
                self.assertTrue(record["retention"]["evidenceRefs"])
                self.assertEqual(
                    record["handoff"]["currentOwner"],
                    record["canonicalOwner"],
                )
                self.assertEqual(
                    record["handoff"]["nextOwner"],
                    record["canonicalOwner"],
                )
                self.assertTrue(record["handoff"]["evidenceRefs"])
                self.assertTrue(record["archiveGc"]["reason"])
                self.assertTrue(record["archiveGc"]["originalOwner"])
                self.assertTrue(record["archiveGc"]["provenanceRefs"])
                if record["archiveGc"]["disposition"] == "discard":
                    self.assertIsNone(record["archiveGc"]["currentOrReplacementOwner"])
                else:
                    self.assertTrue(record["archiveGc"]["currentOrReplacementOwner"])
                if record["archiveGc"]["disposition"] in {
                    "archive",
                    "garbage-collect",
                }:
                    self.assertTrue(record["archiveGc"]["archivedAtUtc"])
                self.assertTrue(record["conflict"]["repositoryWins"])
                if record["promotion"]["targetClass"] is not None:
                    self.assertTrue(record["promotion"]["evidenceRefs"])
                    self.assertEqual(
                        record["promotion"]["review"]["status"],
                        "approved",
                    )

    def test_compaction_closes_source_replacement_and_review(self) -> None:
        compaction = self.fixture["syntheticCheckpoint"]["compaction"]
        self.assertNotEqual(
            compaction["source"]["digest"],
            compaction["replacement"]["digest"],
        )
        for record in (compaction["source"], compaction["replacement"]):
            self.assertTrue(record["owner"])
            self.assertTrue(record["evidenceRefs"])
        self.assertEqual(compaction["reviewStatus"], "approved")

    def test_checkpoint_freshness_is_fixed_synthetic_and_ordered(self) -> None:
        identity = self.fixture["syntheticCheckpoint"]["identity"]
        repository_state = self.fixture["repositoryState"]
        created = datetime.fromisoformat(
            identity["createdAtUtc"].replace("Z", "+00:00")
        )
        updated = datetime.fromisoformat(
            identity["updatedAtUtc"].replace("Z", "+00:00")
        )
        observed = datetime.fromisoformat(
            repository_state["observedAtUtc"].replace("Z", "+00:00")
        )
        self.assertLessEqual(created, updated)
        self.assertLessEqual(updated, observed)

    def test_sensitive_policy_declarations_are_not_payloads(self) -> None:
        self.validator.scan_sensitive_payload(
            {
                "redaction": {
                    "credentialsStored": False,
                    "rawPromptStored": False,
                    "transcriptStored": False,
                    "providerBodyStored": False,
                    "stdoutStored": False,
                    "stderrStored": False,
                    "syntheticMarker": "[REDACTED-SYNTHETIC]",
                }
            }
        )

    def test_modern_token_shapes_are_rejected_with_synthetic_markers(
        self,
    ) -> None:
        synthetic_values = {
            "openai-project": ("sk" + "-proj-" + "synthetic_marker_only"),
            "github-personal": "gh" + "p_" + "syntheticmarkeronly",
            "github-oauth": "gh" + "o_" + "syntheticmarkeronly",
            "github-user": "gh" + "u_" + "syntheticmarkeronly",
            "github-server": "gh" + "s_" + "syntheticmarkeronly",
            "github-refresh": "gh" + "r_" + "syntheticmarkeronly",
            "github-uppercase": "GH" + "S_" + "SyntheticMarkerOnly",
            "slack-bot": "xox" + "b-" + "synthetic-marker-only",
            "slack-app": "xox" + "a-" + "synthetic-marker-only",
            "slack-user": "xox" + "p-" + "synthetic-marker-only",
            "slack-refresh": "xox" + "r-" + "synthetic-marker-only",
            "slack-service": "xox" + "s-" + "synthetic-marker-only",
            "slack-uppercase": "XOX" + "A-" + "Synthetic-Marker-Only",
            "google-api": "AI" + "za" + "SyntheticMarkerOnly",
        }
        for token_class, value in synthetic_values.items():
            with self.subTest(token_class=token_class):
                with self.assertRaises(self.validator.CheckpointError) as raised:
                    self.validator.scan_sensitive_payload({"nextAction": value})
                self.assertEqual(
                    raised.exception.code,
                    "AHLL-CP-SENSITIVE",
                )

        self.validator.scan_sensitive_payload(
            {"nextAction": "bounded synthetic marker only"}
        )

    def test_fixture_is_consumed_only_by_the_independent_test(self) -> None:
        counts = self.validator.validate_checkpoint(
            REPOSITORY_ROOT,
            self.checkpoint_copy(),
            self.repository_state_copy(),
            check_repository_contracts=True,
            require_synthetic=True,
        )
        self.assertTrue(self.fixture["syntheticCheckpoint"]["synthetic"])
        self.assertEqual(
            self.fixture["syntheticCheckpoint"]["checkpointPath"],
            ".agent-work/checkpoint.json",
        )
        self.assertEqual(counts["memoryClasses"], 4)


if __name__ == "__main__":
    unittest.main()
