from __future__ import annotations

import builtins
import copy
import hashlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from unittest import mock


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = REPOSITORY_ROOT / "scripts" / "validate-active-corpus-retention.py"
AGGREGATE_PATH = REPOSITORY_ROOT / "scripts" / "validate-repo-quality-gates.sh"
RESIDUE_VALIDATOR_PATH = (
    REPOSITORY_ROOT / "scripts" / "validate-active-corpus-residue-closure.py"
)
RESIDUE_LEDGER_PATH = (
    REPOSITORY_ROOT
    / "docs"
    / "90.references"
    / "data"
    / "active-corpus-residue-closure.json"
)


def load_validator():
    specification = importlib.util.spec_from_file_location(
        "active_corpus_retention_test_target", VALIDATOR_PATH
    )
    if specification is None or specification.loader is None:
        raise AssertionError("active corpus retention validator could not be loaded")
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


def load_residue_validator():
    specification = importlib.util.spec_from_file_location(
        "active_corpus_residue_closure_test_target", RESIDUE_VALIDATOR_PATH
    )
    if specification is None or specification.loader is None:
        raise AssertionError(
            "active corpus residue closure validator could not be loaded"
        )
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


class ActiveCorpusRetentionContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_validator()
        cls.snapshot = cls.validator.load_snapshot(REPOSITORY_ROOT)
        cls.expected = cls.validator.build_expected_snapshot(REPOSITORY_ROOT)

    def fixture(self):
        return copy.deepcopy(self.snapshot)

    def assert_census_error(self, fixture, code: str) -> None:
        with self.assertRaises(self.validator.CensusError) as raised:
            self.validator.validate_snapshot(fixture, self.expected)
        self.assertEqual(raised.exception.code, code)
        self.assertNotIn("eligibility-evidence-pending", str(raised.exception))

    def assert_path_error_is_payload_free(
        self, fixture, code: str, hostile_path: str
    ) -> None:
        with self.assertRaises(self.validator.CensusError) as raised:
            self.validator.validate_snapshot(fixture, self.expected)
        rendered = str(raised.exception)
        expected = f"{code} {self.validator.SNAPSHOT_PATH}"
        self.assertEqual(rendered, expected)
        self.assertEqual(rendered.splitlines(), [expected])
        self.assertNotIn(hostile_path, rendered)

        stderr = io.StringIO()
        with (
            mock.patch.object(self.validator, "load_snapshot", return_value=fixture),
            mock.patch.object(
                self.validator, "build_expected_snapshot", return_value=self.expected
            ),
            redirect_stderr(stderr),
        ):
            self.assertEqual(self.validator.main(["--root", str(REPOSITORY_ROOT)]), 1)
        cli_error = stderr.getvalue()
        self.assertEqual(cli_error, f"ERR {expected}\n")
        self.assertEqual(cli_error.splitlines(), [f"ERR {expected}"])
        self.assertNotIn(hostile_path, cli_error)

    def test_production_snapshot_matches_pinned_git_objects(self) -> None:
        self.validator.validate_snapshot(self.snapshot, self.expected)
        counts = self.validator.validate_active_corpus_retention(REPOSITORY_ROOT)
        self.assertEqual(
            counts,
            {
                "candidates": 110,
                "controls": 2,
                "stage05": 24,
                "helpersInput": 29,
                "helpersProposed": 30,
            },
        )

    def test_missing_candidate_fails(self) -> None:
        fixture = self.fixture()
        fixture["candidateBaseline"]["entries"].pop()
        self.assert_census_error(fixture, "CENSUS-CANDIDATE-DRIFT")

    def test_extra_candidate_fails(self) -> None:
        fixture = self.fixture()
        extra = copy.deepcopy(fixture["candidateBaseline"]["entries"][0])
        extra["path"] = "docs/04.execution/plans/2099-01-01-extra.md"
        fixture["candidateBaseline"]["entries"].append(extra)
        self.assert_census_error(fixture, "CENSUS-CANDIDATE-DRIFT")

    def test_duplicate_candidate_fails(self) -> None:
        fixture = self.fixture()
        fixture["candidateBaseline"]["entries"][1]["path"] = fixture[
            "candidateBaseline"
        ]["entries"][0]["path"]
        self.assert_census_error(fixture, "CENSUS-CANDIDATE-DUPLICATE")

    def test_wrong_candidate_counts_fail(self) -> None:
        fixture = self.fixture()
        fixture["candidateBaseline"]["candidateCounts"]["total"] = 109
        self.assert_census_error(fixture, "CENSUS-CANDIDATE-DRIFT")

    def test_wrong_delta_fails(self) -> None:
        fixture = self.fixture()
        fixture["candidateBaseline"]["deltaPaths"].pop()
        self.assert_census_error(fixture, "CENSUS-CANDIDATE-DRIFT")

    def test_wrong_pair_state_fails(self) -> None:
        fixture = self.fixture()
        fixture["candidateBaseline"]["entries"][0]["pairState"] = "task-only"
        self.assert_census_error(fixture, "CENSUS-CANDIDATE-DRIFT")

    def test_premature_eligible_fails(self) -> None:
        fixture = self.fixture()
        fixture["candidateBaseline"]["entries"][0]["disposition"] = "eligible"
        self.assert_census_error(fixture, "CENSUS-PREMATURE-ELIGIBLE")

    def test_missing_defer_evidence_fails(self) -> None:
        fixture = self.fixture()
        fixture["candidateBaseline"]["entries"][0]["refreshTrigger"] = ""
        self.assert_census_error(fixture, "CENSUS-DEFER-EVIDENCE")

    def test_unsafe_candidate_paths_are_payload_free(self) -> None:
        for hostile_path in (
            "docs/04.execution/plans/injected.md\nFORGED PASS",
            "docs/04.execution/plans/injected.md\x1b[31m",
            "../outside.md",
        ):
            with self.subTest(hostile_path=repr(hostile_path)):
                fixture = self.fixture()
                fixture["candidateBaseline"]["entries"][0]["path"] = hostile_path
                self.assert_path_error_is_payload_free(
                    fixture, "CENSUS-CANDIDATE-PATH", hostile_path
                )

    def test_unreviewed_lineage_evidence_cannot_be_inferred(self) -> None:
        fixture = self.fixture()
        evidence = fixture["candidateBaseline"]["entries"][0]["eligibilityEvidence"]
        evidence["upstreamSpec"] = {
            "state": "known",
            "value": "docs/03.specs/inferred/spec.md",
            "refreshTrigger": "ACER-002",
        }
        self.assert_census_error(fixture, "CENSUS-ELIGIBILITY-EVIDENCE")

    def test_wrong_blob_fails(self) -> None:
        fixture = self.fixture()
        fixture["candidateBaseline"]["entries"][0]["sourceBlob"] = "f" * 40
        self.assert_census_error(fixture, "CENSUS-CANDIDATE-DRIFT")

    def test_wrong_ledger_membership_fails(self) -> None:
        fixture = self.fixture()
        row = fixture["candidateBaseline"]["entries"][0]
        row["ledgerRowPresent"] = not row["ledgerRowPresent"]
        self.assert_census_error(fixture, "CENSUS-CANDIDATE-DRIFT")

    def test_wrong_spec_link_evidence_fails(self) -> None:
        fixture = self.fixture()
        fixture["candidateBaseline"]["entries"][0]["bodySpecLinkCount"] += 1
        self.assert_census_error(fixture, "CENSUS-SPEC-LINK-EVIDENCE")

    def test_wrong_control_fails(self) -> None:
        fixture = self.fixture()
        fixture["activation"]["activeControls"].pop()
        self.assert_census_error(fixture, "CENSUS-ACTIVATION-DRIFT")

    def test_active_control_cannot_be_candidate_eligible(self) -> None:
        fixture = self.fixture()
        fixture["activation"]["activeControls"][0]["candidateEligible"] = True
        self.assert_census_error(fixture, "CENSUS-CONTROL-DISPOSITION")

    def test_fake_event_record_fails(self) -> None:
        fixture = self.fixture()
        fixture["activation"]["stage05"]["entries"][0]["kind"] = "incident"
        self.assert_census_error(fixture, "CENSUS-FAKE-EVENT")

    def test_wrong_stage05_counts_fail(self) -> None:
        fixture = self.fixture()
        fixture["activation"]["stage05"]["counts"]["incident"] = 1
        self.assert_census_error(fixture, "CENSUS-ACTIVATION-DRIFT")

    def test_unsafe_stage05_paths_are_payload_free(self) -> None:
        for hostile_path in (
            "docs/05.operations/guides/injected.md\nFORGED PASS",
            "docs/05.operations/guides/injected.md\x00suffix",
            "docs/05.operations/../outside.md",
        ):
            with self.subTest(hostile_path=repr(hostile_path)):
                fixture = self.fixture()
                fixture["activation"]["stage05"]["entries"][0]["path"] = hostile_path
                self.assert_path_error_is_payload_free(
                    fixture, "CENSUS-STAGE05-PATH", hostile_path
                )

    def test_helper_cannot_be_execution_tracker(self) -> None:
        fixture = self.fixture()
        fixture["activation"]["helperTests"]["executionTracker"] = True
        self.assert_census_error(fixture, "CENSUS-HELPER-ROLE")

    def test_wrong_helper_inventory_fails(self) -> None:
        fixture = self.fixture()
        fixture["activation"]["helperTests"]["entries"].pop()
        self.assert_census_error(fixture, "CENSUS-ACTIVATION-DRIFT")

    def test_unsafe_control_and_helper_paths_fail_closed(self) -> None:
        for section, hostile_path, code in (
            ("control", "_workspace/control.md", "CENSUS-CONTROL-PATH"),
            ("helper", "tests//helper.py", "CENSUS-HELPER-PATH"),
            ("helper-delta", "tests/../helper.py", "CENSUS-HELPER-DELTA-PATH"),
        ):
            with self.subTest(section=section):
                fixture = self.fixture()
                if section == "control":
                    fixture["activation"]["activeControls"][0]["path"] = hostile_path
                elif section == "helper":
                    fixture["activation"]["helperTests"]["entries"][0]["path"] = (
                        hostile_path
                    )
                else:
                    fixture["activation"]["helperTests"]["proposalDelta"]["entries"][0][
                        "path"
                    ] = hostile_path
                self.assert_path_error_is_payload_free(fixture, code, hostile_path)

    def test_helper_observation_cannot_infer_worktree(self) -> None:
        fixture = self.fixture()
        fixture["activation"]["helperTests"]["observationBoundary"][
            "worktreeInference"
        ] = True
        self.assert_census_error(fixture, "CENSUS-HELPER-BOUNDARY")

    def test_helper_proposal_delta_is_exact(self) -> None:
        fixture = self.fixture()
        fixture["activation"]["helperTests"]["proposalDelta"]["entries"].clear()
        self.assert_census_error(fixture, "CENSUS-HELPER-DELTA")

    def test_helper_proposed_count_drift_fails(self) -> None:
        fixture = self.fixture()
        fixture["activation"]["helperTests"]["proposedCounts"]["python"] = 8
        self.assert_census_error(fixture, "CENSUS-ACTIVATION-DRIFT")

    def test_unknown_schema_keys_fail_closed(self) -> None:
        fixture = self.fixture()
        fixture["candidateBaseline"]["entries"][0]["unknown"] = True
        self.assert_census_error(fixture, "CENSUS-CANDIDATE-SCHEMA")

    def test_diagnostic_path_sanitizes_non_string_values(self) -> None:
        error = self.validator.CensusError("CENSUS-TEST", ["unhashable"])
        self.assertEqual(str(error), f"CENSUS-TEST {self.validator.SNAPSHOT_PATH}")

    def test_wrong_schema_version_fails(self) -> None:
        fixture = self.fixture()
        fixture["schemaVersion"] = 2
        self.assert_census_error(fixture, "CENSUS-SCHEMA")

    def test_methodology_source_freshness_fails(self) -> None:
        fixture = self.fixture()
        fixture["methodologySources"][0]["observedAt"] = "2026-07-17"
        self.assert_census_error(fixture, "CENSUS-SOURCE-FRESHNESS")

    def test_duplicate_json_key_fails(self) -> None:
        with self.assertRaises(self.validator.CensusError) as raised:
            self.validator._duplicate_key([("a", 1), ("a", 2)])
        self.assertEqual(raised.exception.code, "CENSUS-JSON-DUPLICATE")

    def test_wrong_commit_object_type_fails(self) -> None:
        def runner(_root: str, arguments: tuple[str, ...]):
            return subprocess.CompletedProcess(arguments, 0, b"blob\n", b"")

        with self.assertRaises(self.validator.CensusError) as raised:
            self.validator._verify_commit(
                str(REPOSITORY_ROOT), self.validator.CANDIDATE_COMMIT, runner
            )
        self.assertEqual(raised.exception.code, "CENSUS-COMMIT-TYPE")

    def test_wrong_blob_object_type_fails(self) -> None:
        def runner(_root: str, arguments: tuple[str, ...]):
            return subprocess.CompletedProcess(arguments, 0, b"commit\n", b"")

        with self.assertRaises(self.validator.CensusError) as raised:
            self.validator._blob(
                str(REPOSITORY_ROOT), "a" * 40, "tests/README.md", runner
            )
        self.assertEqual(raised.exception.code, "CENSUS-BLOB-TYPE")

    def test_missing_pinned_tree_ref_fails(self) -> None:
        def runner(_root: str, arguments: tuple[str, ...]):
            return subprocess.CompletedProcess(arguments, 1, b"", b"hidden")

        with self.assertRaises(self.validator.CensusError) as raised:
            self.validator._tree(
                str(REPOSITORY_ROOT),
                self.validator.CANDIDATE_COMMIT,
                (self.validator.PLAN_ROOT,),
                runner,
            )
        self.assertEqual(raised.exception.code, "CENSUS-TREE-QUERY")
        self.assertNotIn("hidden", str(raised.exception))

    def test_parent_relative_tree_paths_fail(self) -> None:
        for raw_path in (b"..", b"../outside"):
            with self.subTest(raw_path=raw_path):
                with self.assertRaises(self.validator.CensusError) as raised:
                    self.validator._safe_path(raw_path)
                self.assertEqual(raised.exception.code, "CENSUS-TREE-PATH")

    def test_git_runner_ignores_hostile_environment(self) -> None:
        query = ("cat-file", "-t", self.validator.CANDIDATE_COMMIT)
        completed = subprocess.CompletedProcess(query, 0, b"commit\n", b"")
        hostile = {
            "GIT_DIR": "/attacker/git",
            "GIT_WORK_TREE": "/attacker/tree",
            "GIT_OBJECT_DIRECTORY": "/attacker/objects",
            "GIT_ALTERNATE_OBJECT_DIRECTORIES": "/attacker/alternates",
            "GIT_REPLACE_REF_BASE": "refs/evil/",
        }
        with mock.patch.dict(os.environ, hostile, clear=False):
            with mock.patch.object(
                self.validator.subprocess, "run", return_value=completed
            ) as invoked:
                self.validator._run_git(str(REPOSITORY_ROOT), query)
        arguments, keyword = invoked.call_args
        self.assertEqual(arguments[0][0], "/usr/bin/git")
        self.assertEqual(keyword["env"], self.validator.LITERAL_GIT_ENVIRONMENT)
        self.assertFalse(set(hostile) & set(keyword["env"]))
        self.assertIs(keyword["shell"], False)
        self.assertEqual(keyword["timeout"], 10)

    def test_pinned_snapshot_queries_never_use_head_or_worktree_inventory(self) -> None:
        calls: list[tuple[str, ...]] = []

        def recording(root: str, arguments: tuple[str, ...]):
            calls.append(arguments)
            return self.validator._run_git(root, arguments)

        expected = self.validator.build_expected_snapshot(REPOSITORY_ROOT, recording)
        self.assertEqual(expected, self.expected)
        self.assertTrue(calls)
        self.assertFalse(any("HEAD" in argument for call in calls for argument in call))
        self.assertFalse(
            any(call and call[0] in {"status", "ls-files"} for call in calls)
        )
        self.assertTrue(
            all(
                self.validator.CANDIDATE_COMMIT in call
                or self.validator.ACTIVATION_COMMIT in call
                or call[0] == "cat-file"
                for call in calls
            )
        )

    def test_ignored_workspace_access_sentinel(self) -> None:
        original_open = builtins.open

        def guarded_open(value, *args, **kwargs):
            path = os.fspath(value)
            if path == "_workspace" or f"{os.sep}_workspace{os.sep}" in path:
                raise AssertionError("ignored workspace access attempted")
            return original_open(value, *args, **kwargs)

        with mock.patch.object(builtins, "open", guarded_open):
            self.validator.validate_active_corpus_retention(REPOSITORY_ROOT)

    def test_aggregate_invokes_self_test_and_production(self) -> None:
        text = AGGREGATE_PATH.read_text(encoding="utf-8")
        self.assertIn(
            'python3 "$ROOT_DIR/scripts/validate-active-corpus-retention.py" --root "$ROOT_DIR" --self-test',
            text,
        )
        self.assertIn(
            'python3 "$ROOT_DIR/scripts/validate-active-corpus-retention.py" --root "$ROOT_DIR"',
            text,
        )


class ActiveCorpusResidueClosureContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if not RESIDUE_VALIDATOR_PATH.is_file():
            return
        cls.validator = load_residue_validator()
        cls.ledger = cls.validator.load_ledger(REPOSITORY_ROOT)
        cls.observed = {
            key: copy.deepcopy(cls.ledger[key])
            for key in (
                "sourceLedgers",
                "counts",
                "migratedClosed",
                "currentRows",
                "pairCardinality",
                "authorityGuards",
                "acer004Dependency",
            )
        }

    def fixture(self):
        return copy.deepcopy(self.ledger)

    def assert_closure_error(self, fixture, code: str) -> None:
        with self.assertRaises(self.validator.ClosureError) as raised:
            self.validator.validate_ledger(fixture, self.observed)
        self.assertEqual(raised.exception.code, code)
        self.assertEqual(str(raised.exception).splitlines(), [str(raised.exception)])

    def test_required_validator_and_ledger_targets_exist(self) -> None:
        self.assertTrue(RESIDUE_VALIDATOR_PATH.is_file())
        self.assertTrue(RESIDUE_LEDGER_PATH.is_file())

    def test_production_closure_matches_exact_repository_state(self) -> None:
        self.validator.validate_ledger(self.ledger, self.observed)
        expected = {
            "migratedClosed": 12,
            "currentRows": 100,
            "defer": 98,
            "retain": 2,
            "pairKeys": 52,
            "completePairs": 48,
            "planOnly": 1,
            "taskOnly": 3,
            "acceptedAdrs": 13,
            "doneSpecs": 28,
            "findings": 0,
        }
        try:
            counts = self.validator.validate_active_corpus_residue_closure(
                REPOSITORY_ROOT
            )
        except self.validator.ClosureError as error:
            self.assertEqual(error.code, "CLOSURE-WORKTREE-INDEX-DRIFT")
            self.assertIn(
                error.path,
                {self.validator.AGGREGATE_PATH, self.validator.EXECUTION_TASK},
            )
        else:
            self.assertEqual(counts, expected)

    def test_tracked_inventory_requires_descriptor_and_index_equality(self) -> None:
        path = "docs/04.execution/plans/tracked.md"
        oid = "a" * 40

        def runner(_root: str, arguments: tuple[str, ...]):
            payload = {
                ("cat-file", "-t", oid): b"blob\n",
                ("cat-file", "-s", oid): b"5\n",
                ("cat-file", "blob", oid): b"index",
            }[arguments]
            return subprocess.CompletedProcess(arguments, 0, payload, b"")

        with mock.patch.object(
            self.validator, "_read_descriptor_bytes", return_value=b"worktree"
        ):
            with self.assertRaises(self.validator.ClosureError) as raised:
                self.validator._proposed_or_index_bytes(
                    str(REPOSITORY_ROOT), path, {path: oid}, runner
                )
        self.assertEqual(raised.exception.code, "CLOSURE-WORKTREE-INDEX-DRIFT")
        self.assertEqual(raised.exception.path, path)

    def test_tracked_aggregate_entrypoint_requires_index_equality(self) -> None:
        script_oid = "a" * 40
        aggregate_oid = "b" * 40
        script = b"#!/usr/bin/env python3\n"
        aggregate = (
            b'python3 "$ROOT_DIR/scripts/validate-active-corpus-residue-closure.py" '
            b'--root "$ROOT_DIR" --self-test\n'
            b'python3 "$ROOT_DIR/scripts/validate-active-corpus-residue-closure.py" '
            b'--root "$ROOT_DIR"\n'
        )

        def descriptor(_root: str, path: str) -> bytes:
            return script if path == self.validator.SCRIPT_PATH else aggregate

        def staged(_root: str, _oid: str, path: str, _runner) -> bytes:
            return (
                script if path == self.validator.SCRIPT_PATH else b"staged aggregate\n"
            )

        with (
            mock.patch.object(
                self.validator,
                "_control_inventory",
                return_value={
                    self.validator.SCRIPT_PATH: script_oid,
                    self.validator.AGGREGATE_PATH: aggregate_oid,
                },
            ),
            mock.patch.object(
                self.validator, "_read_descriptor_bytes", side_effect=descriptor
            ),
            mock.patch.object(self.validator, "_index_blob", side_effect=staged),
        ):
            with self.assertRaises(self.validator.ClosureError) as raised:
                self.validator.verify_entrypoints(REPOSITORY_ROOT)
        self.assertEqual(raised.exception.code, "CLOSURE-WORKTREE-INDEX-DRIFT")
        self.assertEqual(raised.exception.path, self.validator.AGGREGATE_PATH)

    def test_ledger_prebinds_final_task_worktree_blob_for_parent_staging(self) -> None:
        payload = self.validator._read_descriptor_bytes(
            str(REPOSITORY_ROOT), self.validator.EXECUTION_TASK
        )
        object_id = hashlib.sha1(
            f"blob {len(payload)}\0".encode("ascii") + payload
        ).hexdigest()
        task_row = next(
            row
            for row in self.ledger["currentRows"]
            if row["path"] == self.validator.EXECUTION_TASK
        )
        self.assertEqual(task_row["objectMode"], "index-stage-zero")
        self.assertEqual(task_row["objectId"], f"git:sha1:{object_id}")

    def test_missing_bounded_defer_field_fails(self) -> None:
        fixture = self.fixture()
        row = next(
            row for row in fixture["currentRows"] if row["disposition"] == "DEFER"
        )
        row["closureReason"] = ""
        self.assert_closure_error(fixture, "CLOSURE-CURRENT-FIELDS")

    def test_active_eligible_row_fails(self) -> None:
        fixture = self.fixture()
        fixture["currentRows"][0]["disposition"] = "eligible"
        self.assert_closure_error(fixture, "CLOSURE-ACTIVE-ELIGIBLE")

    def test_duplicate_current_owner_fails(self) -> None:
        fixture = self.fixture()
        fixture["currentRows"].append(copy.deepcopy(fixture["currentRows"][0]))
        self.assert_closure_error(fixture, "CLOSURE-CURRENT-DUPLICATE")

    def test_partial_pair_must_be_explicit_owned_defer(self) -> None:
        fixture = self.fixture()
        pair = next(
            row for row in fixture["pairCardinality"] if row["state"] != "complete"
        )
        pair["disposition"] = "retain"
        self.assert_closure_error(fixture, "CLOSURE-PAIR-PARTIAL")

    def test_stale_unjoined_eligible_row_fails(self) -> None:
        fixture = self.fixture()
        fixture["migratedClosed"].pop()
        self.assert_closure_error(fixture, "CLOSURE-MIGRATION-STALE")

    def test_reintroduced_migrated_source_fails(self) -> None:
        fixture = self.fixture()
        fixture["migratedClosed"][0]["currentSourcePresent"] = True
        self.assert_closure_error(fixture, "CLOSURE-MIGRATION-SOURCE")

    def test_authority_guard_cannot_move_terminal_record(self) -> None:
        fixture = self.fixture()
        fixture["authorityGuards"]["acceptedAdrs"][0]["disposition"] = "migrated-closed"
        self.assert_closure_error(fixture, "CLOSURE-AUTHORITY-GUARD")

    def test_draft_adr_is_admissible_but_not_an_authority_guard(self) -> None:
        draft_path = "docs/02.architecture/decisions/9998-draft.md"
        accepted_path = "docs/02.architecture/decisions/9999-accepted.md"
        payloads = {
            draft_path: (
                b"---\ntype: sdlc/adr\nstatus: draft\nowner: platform\n---\n# Draft\n"
            ),
            accepted_path: (
                b"---\ntype: sdlc/adr\nstatus: accepted\nowner: platform\n---\n"
                b"# Accepted\n"
            ),
        }
        index = {draft_path: "a" * 40, accepted_path: "b" * 40}

        guards = self.validator._authority_entries(
            [draft_path, accepted_path], index, payloads, kind="adr"
        )

        self.assertEqual(len(guards), 1)
        self.assertEqual(guards[0]["path"], accepted_path)
        self.assertEqual(guards[0]["status"], "accepted")
        self.assertEqual(guards[0]["currentAuthority"], self.validator.ADR_AUTHORITY)

    def test_closure_schema_normalizes_pair_keys_to_lineage_ids(self) -> None:
        raw = RESIDUE_LEDGER_PATH.read_text(encoding="utf-8")
        self.assertNotIn('"pairKey":', raw)
        self.assertNotIn("\\u002d", raw)
        parsed = json.loads(raw)
        closure_rows = [
            row
            for collection in ("migratedClosed", "currentRows", "pairCardinality")
            for row in parsed[collection]
        ]
        self.assertEqual(len(closure_rows), 12 + 100 + 52)
        self.assertTrue(all("pairKey" not in row for row in closure_rows))
        self.assertTrue(
            all(isinstance(row.get("lineageId"), str) for row in closure_rows)
        )

        eligibility_path = (
            REPOSITORY_ROOT
            / "docs"
            / "90.references"
            / "data"
            / "active-corpus-eligibility-ledger.json"
        )
        eligibility = json.loads(eligibility_path.read_text(encoding="utf-8"))
        eligible_by_path = {
            row["path"]: row["pairKey"]
            for row in eligibility["candidateRows"]
            if row["disposition"] == "eligible"
        }
        current_by_path = {
            row["path"]: row["pairKey"]
            for row in eligibility["candidateRows"]
            if row["disposition"] == "DEFER"
        }
        current_by_path.update(
            {row["path"]: row["pairKey"] for row in eligibility["controls"]}
        )

        self.assertEqual(
            {row["path"]: row["lineageId"] for row in parsed["migratedClosed"]},
            eligible_by_path,
        )
        self.assertEqual(
            {row["path"]: row["lineageId"] for row in parsed["currentRows"]},
            current_by_path,
        )
        self.assertEqual(
            [row["lineageId"] for row in parsed["pairCardinality"]],
            sorted(set(current_by_path.values())),
        )
        self.validator.validate_ledger(parsed, self.observed)

    def test_nonempty_finding_fails(self) -> None:
        fixture = self.fixture()
        fixture["findings"]["unexplainedResidue"].append({"path": "docs/x.md"})
        self.assert_closure_error(fixture, "CLOSURE-FINDINGS")

    def test_duplicate_json_key_fails(self) -> None:
        with self.assertRaises(self.validator.ClosureError) as raised:
            self.validator._reject_duplicate_pairs([("a", 1), ("a", 2)])
        self.assertEqual(raised.exception.code, "CLOSURE-JSON-DUPLICATE")

    def test_git_runner_is_literal_bounded_and_ignores_hostile_environment(
        self,
    ) -> None:
        query = ("cat-file", "-t", self.validator.FIXED_INPUT_COMMIT)
        completed = subprocess.CompletedProcess(query, 0, b"commit\n", b"")
        hostile = {
            "GIT_DIR": "/attacker/git",
            "GIT_WORK_TREE": "/attacker/tree",
            "GIT_OBJECT_DIRECTORY": "/attacker/objects",
            "GIT_REPLACE_REF_BASE": "refs/evil/",
        }
        with mock.patch.dict(os.environ, hostile, clear=False):
            with mock.patch.object(
                self.validator.subprocess, "run", return_value=completed
            ) as invoked:
                self.validator._run_git(str(REPOSITORY_ROOT), query)
        arguments, keyword = invoked.call_args
        self.assertEqual(arguments[0][0], "/usr/bin/git")
        self.assertEqual(keyword["env"], self.validator.CLOSED_GIT_ENVIRONMENT)
        self.assertFalse(set(hostile) & set(keyword["env"]))
        self.assertIs(keyword["shell"], False)
        self.assertEqual(keyword["timeout"], 10)

    def test_malformed_git_nul_and_mode_data_fail_closed(self) -> None:
        with self.assertRaises(self.validator.ClosureError) as nul_error:
            self.validator._parse_nul_paths(
                b"docs/04.execution/plans/x.md", "docs/04.execution/plans"
            )
        self.assertEqual(nul_error.exception.code, "CLOSURE-GIT-MALFORMED")
        with self.assertRaises(self.validator.ClosureError) as mode_error:
            self.validator._parse_modes(b"120000 deadbeef 0\tdocs/x\0")
        self.assertEqual(mode_error.exception.code, "CLOSURE-GIT-MALFORMED")

    def test_unsafe_path_diagnostic_is_value_free(self) -> None:
        hostile = "../outside\nFORGED PASS"
        error = self.validator.ClosureError("CLOSURE-PATH", hostile)
        self.assertEqual(str(error), f"CLOSURE-PATH {self.validator.LEDGER_PATH}")
        self.assertNotIn(hostile, str(error))

    def test_production_queries_never_use_head_or_walk_ignored_paths(self) -> None:
        calls: list[tuple[str, ...]] = []

        def recording(root: str, arguments: tuple[str, ...]):
            calls.append(arguments)
            return self.validator._run_git(root, arguments)

        try:
            observed = self.validator.build_observed(REPOSITORY_ROOT, recording)
        except self.validator.ClosureError as error:
            self.assertEqual(error.code, "CLOSURE-WORKTREE-INDEX-DRIFT")
        else:
            self.assertEqual(observed, self.observed)
        self.assertTrue(calls)
        self.assertFalse(any("HEAD" in argument for call in calls for argument in call))
        self.assertFalse(
            any("_workspace" in argument for call in calls for argument in call)
        )
        self.assertTrue(all(call[0] in {"ls-files", "cat-file"} for call in calls))

    def test_ignored_workspace_descriptor_sentinel(self) -> None:
        original_open = self.validator.os.open

        def guarded_open(value, *args, **kwargs):
            path = os.fspath(value)
            if path == "_workspace" or f"{os.sep}_workspace{os.sep}" in path:
                raise AssertionError("ignored workspace access attempted")
            return original_open(value, *args, **kwargs)

        with mock.patch.object(self.validator.os, "open", guarded_open):
            try:
                self.validator.validate_active_corpus_residue_closure(REPOSITORY_ROOT)
            except self.validator.ClosureError as error:
                self.assertEqual(error.code, "CLOSURE-WORKTREE-INDEX-DRIFT")

    def test_aggregate_invokes_residue_self_test_and_production_once(self) -> None:
        text = AGGREGATE_PATH.read_text(encoding="utf-8")
        for command in (
            'python3 "$ROOT_DIR/scripts/validate-active-corpus-residue-closure.py" --root "$ROOT_DIR" --self-test',
            'python3 "$ROOT_DIR/scripts/validate-active-corpus-residue-closure.py" --root "$ROOT_DIR"',
        ):
            self.assertEqual(text.splitlines().count(command), 1)


if __name__ == "__main__":
    unittest.main()
