from __future__ import annotations

import builtins
import copy
import importlib.util
import io
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


if __name__ == "__main__":
    unittest.main()
