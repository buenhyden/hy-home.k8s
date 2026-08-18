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
    FRONTIER_LINEAGE = "2026-07-27-contract-cutover-and-program-closure"
    FRONTIER_SPEC = "docs/03.specs/040-contract-cutover-and-program-closure/spec.md"
    FRONTIER_PLAN = f"docs/04.execution/plans/{FRONTIER_LINEAGE}.md"
    FRONTIER_TASK = f"docs/04.execution/tasks/{FRONTIER_LINEAGE}.md"
    SUCCESSOR_LINEAGE = "2026-07-26-github-ci-qa-evidence"
    SUCCESSOR_PLAN = f"docs/04.execution/plans/{SUCCESSOR_LINEAGE}.md"
    SUCCESSOR_TASK = f"docs/04.execution/tasks/{SUCCESSOR_LINEAGE}.md"

    @classmethod
    def setUpClass(cls) -> None:
        if not RESIDUE_VALIDATOR_PATH.is_file():
            return
        cls.validator = load_residue_validator()
        try:
            cls.ledger = cls.validator.load_ledger(REPOSITORY_ROOT)
        except cls.validator.ClosureError as error:
            if error.code != "CLOSURE-WORKTREE-INDEX-DRIFT":
                raise
            cls.ledger = cls.validator._load_json_bytes(
                cls.validator._read_descriptor_bytes(
                    str(REPOSITORY_ROOT), cls.validator.LEDGER_PATH
                ),
                cls.validator.LEDGER_PATH,
            )
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
        cls.observed.update(
            {
                "activeControlRows": [],
                "activeControlPairCardinality": [],
                "terminalControlRows": [],
                "terminalControlPairCardinality": [],
                "terminalSpecRows": [],
                "terminalProgramClosureAuthority": [],
            }
        )

    def fixture(self):
        return copy.deepcopy(self.ledger)

    def assert_closure_error(self, fixture, code: str) -> None:
        with self.assertRaises(self.validator.ClosureError) as raised:
            self.validator.validate_ledger(fixture, self.observed)
        self.assertEqual(raised.exception.code, code)
        self.assertEqual(str(raised.exception).splitlines(), [str(raised.exception)])

    @classmethod
    def git_blob_identity(cls, payload: bytes) -> str:
        object_id = hashlib.sha1(
            f"blob {len(payload)}\0".encode("ascii") + payload
        ).hexdigest()
        return cls.validator._git_identity(object_id)

    def index_object_identities(self, paths: set[str]) -> dict[str, str]:
        result = subprocess.run(
            [
                self.validator.GIT_EXECUTABLE,
                "ls-files",
                "-z",
                "--stage",
                "--",
                *sorted(paths),
            ],
            cwd=REPOSITORY_ROOT,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            env=self.validator.CLOSED_GIT_ENVIRONMENT,
            timeout=self.validator.GIT_TIMEOUT_SECONDS,
            shell=False,
            check=False,
        )
        self.assertEqual(result.returncode, 0)
        index = self.validator._parse_modes(
            result.stdout,
            allowed_paths=paths,
        )
        self.assertEqual(set(index), paths)
        return {
            path: self.validator._git_identity(object_id)
            for path, object_id in index.items()
        }

    def assert_production_observed(
        self,
        observed: dict[str, object],
        *,
        expected_object_ids: dict[str, str] | None = None,
    ) -> str:
        actual = copy.deepcopy(observed)
        rows = actual.pop("activeControlRows")
        pairs = actual.pop("activeControlPairCardinality")
        terminal_rows = actual.pop("terminalControlRows")
        terminal_pairs = actual.pop("terminalControlPairCardinality")
        terminal_specs = actual.pop("terminalSpecRows")
        terminal_authority = actual.pop("terminalProgramClosureAuthority")
        current_spec_paths = [self.validator.TERMINAL_SPEC]
        advanced_spec_paths = [
            self.validator.TERMINAL_SPEC,
            self.validator.TERMINAL_SUCCESSOR_SPEC,
        ]
        terminal_spec_paths_expected = [
            self.validator.TERMINAL_SPEC,
            self.validator.TERMINAL_SUCCESSOR_SPEC,
            self.FRONTIER_SPEC,
        ]
        terminal_spec_paths = [row["path"] for row in terminal_specs]
        if terminal_spec_paths == current_spec_paths:
            mode = "current"
        elif terminal_spec_paths == advanced_spec_paths:
            mode = "advanced"
        elif terminal_spec_paths == terminal_spec_paths_expected:
            mode = "terminal"
        else:
            self.fail(
                "production terminal Spec frontier must be exactly current, "
                "advanced, or terminal"
            )
        expected_terminal_authority = (
            [
                {
                    "path": self.validator.TERMINAL_PROGRAM_CLOSURE_ADR,
                    "profile": "sdlc/adr",
                    "status": "accepted",
                    "owner": "platform",
                    "objectMode": "index-stage-zero",
                    "authorityRole": "terminal-program-closure-decision",
                    "frontierSpecPath": self.FRONTIER_SPEC,
                }
            ]
            if mode == "terminal"
            else []
        )
        self.assertEqual(len(terminal_authority), len(expected_terminal_authority))
        for row, expected_row in zip(
            terminal_authority, expected_terminal_authority, strict=True
        ):
            self.assertEqual(
                {key: row[key] for key in expected_row},
                expected_row,
            )
            self.assertEqual(
                set(row),
                {*expected_row, "objectId"},
            )
            self.assertRegex(
                row["objectId"],
                r"\Agit:(?:sha1:[0-9a-f]{40}|sha256:[0-9a-f]{64})\Z",
            )

        current_plan = "docs/04.execution/plans/2026-07-26-github-ci-qa-evidence.md"
        current_task = "docs/04.execution/tasks/2026-07-26-github-ci-qa-evidence.md"
        terminal_plan = (
            "docs/04.execution/plans/2026-07-22-reference-information-architecture.md"
        )
        terminal_task = (
            "docs/04.execution/tasks/2026-07-22-reference-information-architecture.md"
        )
        active_rows_by_mode = {
            "current": [
                (
                    current_plan,
                    "plan",
                    self.SUCCESSOR_LINEAGE,
                    "sdlc/plan",
                    "platform",
                    "active",
                ),
                (
                    current_task,
                    "task",
                    self.SUCCESSOR_LINEAGE,
                    "sdlc/task",
                    "platform",
                    "active",
                ),
            ],
            "advanced": [
                (
                    self.FRONTIER_PLAN,
                    "plan",
                    self.FRONTIER_LINEAGE,
                    "sdlc/plan",
                    "platform",
                    "active",
                ),
                (
                    self.FRONTIER_TASK,
                    "task",
                    self.FRONTIER_LINEAGE,
                    "sdlc/task",
                    "platform",
                    "active",
                ),
            ],
            "terminal": [],
        }
        active_pairs_by_mode = {
            "current": [
                {
                    "lineageId": self.SUCCESSOR_LINEAGE,
                    "owner": "platform",
                    "planPath": current_plan,
                    "state": "complete",
                    "status": "active",
                    "taskPath": current_task,
                }
            ],
            "advanced": [
                {
                    "lineageId": self.FRONTIER_LINEAGE,
                    "owner": "platform",
                    "planPath": self.FRONTIER_PLAN,
                    "state": "complete",
                    "status": "active",
                    "taskPath": self.FRONTIER_TASK,
                }
            ],
            "terminal": [],
        }
        terminal_rows_by_mode = {
            "current": [
                (
                    terminal_plan,
                    "plan",
                    self.validator.TERMINAL_LINEAGE,
                    "sdlc/plan",
                    "platform",
                    "done",
                ),
                (
                    terminal_task,
                    "task",
                    self.validator.TERMINAL_LINEAGE,
                    "sdlc/task",
                    "platform",
                    "done",
                ),
            ],
            "advanced": [
                (
                    terminal_plan,
                    "plan",
                    self.validator.TERMINAL_LINEAGE,
                    "sdlc/plan",
                    "platform",
                    "done",
                ),
                (
                    current_plan,
                    "plan",
                    self.SUCCESSOR_LINEAGE,
                    "sdlc/plan",
                    "platform",
                    "done",
                ),
                (
                    terminal_task,
                    "task",
                    self.validator.TERMINAL_LINEAGE,
                    "sdlc/task",
                    "platform",
                    "done",
                ),
                (
                    current_task,
                    "task",
                    self.SUCCESSOR_LINEAGE,
                    "sdlc/task",
                    "platform",
                    "done",
                ),
            ],
            "terminal": [
                (
                    terminal_plan,
                    "plan",
                    self.validator.TERMINAL_LINEAGE,
                    "sdlc/plan",
                    "platform",
                    "done",
                ),
                (
                    current_plan,
                    "plan",
                    self.SUCCESSOR_LINEAGE,
                    "sdlc/plan",
                    "platform",
                    "done",
                ),
                (
                    self.FRONTIER_PLAN,
                    "plan",
                    self.FRONTIER_LINEAGE,
                    "sdlc/plan",
                    "platform",
                    "done",
                ),
                (
                    terminal_task,
                    "task",
                    self.validator.TERMINAL_LINEAGE,
                    "sdlc/task",
                    "platform",
                    "done",
                ),
                (
                    current_task,
                    "task",
                    self.SUCCESSOR_LINEAGE,
                    "sdlc/task",
                    "platform",
                    "done",
                ),
                (
                    self.FRONTIER_TASK,
                    "task",
                    self.FRONTIER_LINEAGE,
                    "sdlc/task",
                    "platform",
                    "done",
                ),
            ],
        }
        terminal_pairs_by_mode = {
            "current": [
                {
                    "lineageId": self.validator.TERMINAL_LINEAGE,
                    "owner": "platform",
                    "planPath": terminal_plan,
                    "state": "complete",
                    "status": "done",
                    "taskPath": terminal_task,
                }
            ],
            "advanced": [
                {
                    "lineageId": self.validator.TERMINAL_LINEAGE,
                    "owner": "platform",
                    "planPath": terminal_plan,
                    "state": "complete",
                    "status": "done",
                    "taskPath": terminal_task,
                },
                {
                    "lineageId": self.SUCCESSOR_LINEAGE,
                    "owner": "platform",
                    "planPath": current_plan,
                    "state": "complete",
                    "status": "done",
                    "taskPath": current_task,
                },
            ],
            "terminal": [
                {
                    "lineageId": self.validator.TERMINAL_LINEAGE,
                    "owner": "platform",
                    "planPath": terminal_plan,
                    "state": "complete",
                    "status": "done",
                    "taskPath": terminal_task,
                },
                {
                    "lineageId": self.SUCCESSOR_LINEAGE,
                    "owner": "platform",
                    "planPath": current_plan,
                    "state": "complete",
                    "status": "done",
                    "taskPath": current_task,
                },
                {
                    "lineageId": self.FRONTIER_LINEAGE,
                    "owner": "platform",
                    "planPath": self.FRONTIER_PLAN,
                    "state": "complete",
                    "status": "done",
                    "taskPath": self.FRONTIER_TASK,
                },
            ],
        }
        terminal_specs_by_mode = {
            "current": [
                (
                    self.validator.TERMINAL_SPEC,
                    "038",
                    5,
                    "Reference information architecture",
                    "done",
                    "done",
                )
            ],
            "advanced": [
                (
                    self.validator.TERMINAL_SPEC,
                    "038",
                    5,
                    "Reference information architecture",
                    "done",
                    "done",
                ),
                (
                    self.validator.TERMINAL_SUCCESSOR_SPEC,
                    "039",
                    6,
                    "GitHub CI and QA evidence",
                    "done",
                    "done",
                ),
            ],
            "terminal": [
                (
                    self.validator.TERMINAL_SPEC,
                    "038",
                    5,
                    "Reference information architecture",
                    "done",
                    "done",
                ),
                (
                    self.validator.TERMINAL_SUCCESSOR_SPEC,
                    "039",
                    6,
                    "GitHub CI and QA evidence",
                    "done",
                    "done",
                ),
                (
                    self.FRONTIER_SPEC,
                    "040",
                    7,
                    "Contract cutover and program closure",
                    "done",
                    "done",
                ),
            ],
        }
        expected_paths = {
            row[0]
            for row in (
                *active_rows_by_mode[mode],
                *terminal_rows_by_mode[mode],
                *terminal_specs_by_mode[mode],
            )
        }
        row_paths = {row["path"] for row in (*rows, *terminal_rows, *terminal_specs)}
        self.assertEqual(row_paths, expected_paths)
        if expected_object_ids is None:
            expected_object_ids = self.index_object_identities(expected_paths)
        self.assertEqual(set(expected_object_ids), expected_paths)

        control_row_keys = {
            "kind",
            "lineageId",
            "objectId",
            "objectMode",
            "owner",
            "path",
            "profile",
            "status",
        }
        for row in (*rows, *terminal_rows):
            self.assertEqual(set(row), control_row_keys)
            self.assertEqual(row["objectMode"], "index-stage-zero")
            self.assertEqual(row["objectId"], expected_object_ids[row["path"]])
        self.assertEqual(
            [
                (
                    row["path"],
                    row["kind"],
                    row["lineageId"],
                    row["profile"],
                    row["owner"],
                    row["status"],
                )
                for row in rows
            ],
            active_rows_by_mode[mode],
        )
        self.assertEqual(pairs, active_pairs_by_mode[mode])
        self.assertEqual(
            [
                (
                    row["path"],
                    row["kind"],
                    row["lineageId"],
                    row["profile"],
                    row["owner"],
                    row["status"],
                )
                for row in terminal_rows
            ],
            terminal_rows_by_mode[mode],
        )
        self.assertEqual(terminal_pairs, terminal_pairs_by_mode[mode])

        terminal_spec_keys = {
            "decision",
            "objectId",
            "objectMode",
            "order",
            "owner",
            "path",
            "profile",
            "programArd",
            "programPrd",
            "reason",
            "registryPath",
            "relationClass",
            "spec",
            "state",
            "status",
        }
        for row in terminal_specs:
            self.assertEqual(set(row), terminal_spec_keys)
            self.assertEqual(row["objectMode"], "index-stage-zero")
            self.assertEqual(row["objectId"], expected_object_ids[row["path"]])
            self.assertEqual(row["profile"], "sdlc/spec")
            self.assertEqual(row["owner"], "platform")
            self.assertEqual(row["programPrd"], "006")
            self.assertEqual(row["programArd"], "0009")
            self.assertEqual(row["decision"], "0017")
            self.assertEqual(row["relationClass"], "original-tranche")
            self.assertEqual(row["registryPath"], self.validator.REGISTRY_PATH)
        self.assertEqual(
            [
                (
                    row["path"],
                    row["spec"],
                    row["order"],
                    row["reason"],
                    row["state"],
                    row["status"],
                )
                for row in terminal_specs
            ],
            terminal_specs_by_mode[mode],
        )
        frozen = copy.deepcopy(self.observed)
        frozen.pop("activeControlRows")
        frozen.pop("activeControlPairCardinality")
        frozen.pop("terminalControlRows")
        frozen.pop("terminalControlPairCardinality")
        frozen.pop("terminalSpecRows")
        frozen.pop("terminalProgramClosureAuthority")
        self.assertEqual(actual, frozen)
        return mode

    def terminal_payloads(
        self,
        state: str,
        *,
        successor_state: str = "active",
        frontier_state: str = "active",
        plan_type: str = "sdlc/plan",
        task_type: str = "sdlc/task",
        plan_owner: str = "platform",
        task_owner: str = "platform",
        successor_plan_type: str = "sdlc/plan",
        successor_task_type: str = "sdlc/task",
        successor_plan_owner: str = "platform",
        successor_task_owner: str = "platform",
        successor_plan_state: str | None = None,
        successor_task_state: str | None = None,
        frontier_type: str = "sdlc/spec",
        frontier_owner: str = "platform",
    ) -> dict[str, bytes]:
        successor_plan_status = successor_plan_state or successor_state
        successor_task_status = successor_task_state or successor_state
        return {
            self.validator.TERMINAL_SPEC: (
                f"---\ntype: sdlc/spec\nstatus: {state}\nowner: platform\n---\n"
            ).encode(),
            self.validator.TERMINAL_PLAN: (
                f"---\ntype: {plan_type}\nstatus: {state}\nowner: {plan_owner}\n---\n"
            ).encode(),
            self.validator.TERMINAL_TASK: (
                f"---\ntype: {task_type}\nstatus: {state}\nowner: {task_owner}\n---\n"
            ).encode(),
            self.validator.TERMINAL_SUCCESSOR_SPEC: (
                "---\n"
                "type: sdlc/spec\n"
                f"status: {successor_state}\n"
                "owner: platform\n"
                "---\n"
            ).encode(),
            self.SUCCESSOR_PLAN: (
                "---\n"
                f"type: {successor_plan_type}\n"
                f"status: {successor_plan_status}\n"
                f"owner: {successor_plan_owner}\n"
                "---\n"
            ).encode(),
            self.SUCCESSOR_TASK: (
                "---\n"
                f"type: {successor_task_type}\n"
                f"status: {successor_task_status}\n"
                f"owner: {successor_task_owner}\n"
                "---\n"
            ).encode(),
            self.FRONTIER_SPEC: (
                "---\n"
                f"type: {frontier_type}\n"
                f"status: {frontier_state}\n"
                f"owner: {frontier_owner}\n"
                "---\n"
            ).encode(),
        } | (
            {
                self.FRONTIER_PLAN: (
                    "---\n"
                    "type: sdlc/plan\n"
                    f"status: {frontier_state}\n"
                    "owner: platform\n"
                    "---\n"
                ).encode(),
                self.FRONTIER_TASK: (
                    "---\n"
                    "type: sdlc/task\n"
                    f"status: {frontier_state}\n"
                    "owner: platform\n"
                    "---\n"
                ).encode(),
            }
            if successor_state == "done" or frontier_state == "done"
            else {}
        )

    @staticmethod
    def terminal_registry(
        state: str,
        *,
        successor_state: str = "active",
        frontier_state: str = "active",
    ) -> dict[str, object]:
        return {
            "programLineage": {
                "programs": [
                    {
                        "prd": "006",
                        "ard": "0009",
                        "tranches": [
                            {
                                "spec": "038",
                                "order": 5,
                                "state": state,
                                "reason": "Reference information architecture",
                                "decision": "0017",
                            },
                            {
                                "spec": "039",
                                "order": 6,
                                "state": successor_state,
                                "reason": "GitHub CI and QA evidence",
                                "decision": "0017",
                            },
                            {
                                "spec": "040",
                                "order": 7,
                                "state": frontier_state,
                                "reason": "Contract cutover and program closure",
                                "decision": "0017",
                            },
                        ],
                        "followUps": [],
                    }
                ]
            }
        }

    def terminal_partition(
        self,
        state: str,
        *,
        payloads: dict[str, bytes] | None = None,
        registry: dict[str, object] | None = None,
        plan_paths: list[str] | None = None,
        task_paths: list[str] | None = None,
        spec_paths: list[str] | None = None,
    ):
        actual_payloads = payloads or self.terminal_payloads(state)
        default_plan_paths = [self.validator.TERMINAL_PLAN]
        default_task_paths = [self.validator.TERMINAL_TASK]
        if state == "done":
            default_plan_paths.append(self.SUCCESSOR_PLAN)
            default_task_paths.append(self.SUCCESSOR_TASK)
        if self.FRONTIER_PLAN in actual_payloads:
            default_plan_paths.append(self.FRONTIER_PLAN)
        if self.FRONTIER_TASK in actual_payloads:
            default_task_paths.append(self.FRONTIER_TASK)
        return self.validator._partition_terminal_controls(
            plan_paths or default_plan_paths,
            task_paths or default_task_paths,
            spec_paths
            or [
                self.validator.TERMINAL_SPEC,
                self.validator.TERMINAL_SUCCESSOR_SPEC,
                self.FRONTIER_SPEC,
            ],
            {},
            actual_payloads,
            registry or self.terminal_registry(state),
        )

    def test_required_validator_and_ledger_targets_exist(self) -> None:
        self.assertTrue(RESIDUE_VALIDATOR_PATH.is_file())
        self.assertTrue(RESIDUE_LEDGER_PATH.is_file())

    def test_production_closure_matches_exact_repository_state(self) -> None:
        observed = self.validator.build_observed(REPOSITORY_ROOT)
        mode = self.assert_production_observed(observed)
        self.validator.validate_ledger(self.ledger, observed)
        frontier_counts = {
            "current": {
                "activeControlRows": 2,
                "activeControlPairs": 1,
                "terminalControlRows": 2,
                "terminalControlPairs": 1,
                "terminalSpecs": 1,
            },
            "advanced": {
                "activeControlRows": 2,
                "activeControlPairs": 1,
                "terminalControlRows": 4,
                "terminalControlPairs": 2,
                "terminalSpecs": 2,
            },
            "terminal": {
                "activeControlRows": 0,
                "activeControlPairs": 0,
                "terminalControlRows": 6,
                "terminalControlPairs": 3,
                "terminalSpecs": 3,
            },
        }[mode]
        expected = {
            "migratedClosed": 12,
            "currentRows": 100,
            "defer": 100,
            "retain": 0,
            "pairKeys": 52,
            "completePairs": 48,
            "planOnly": 1,
            "taskOnly": 3,
            "acceptedAdrs": 13,
            "doneSpecs": 29,
            "findings": 0,
            **frontier_counts,
        }
        self.assertEqual(
            {
                "activeControlRows": len(observed["activeControlRows"]),
                "activeControlPairs": len(observed["activeControlPairCardinality"]),
                "terminalControlRows": len(observed["terminalControlRows"]),
                "terminalControlPairs": len(observed["terminalControlPairCardinality"]),
                "terminalSpecs": len(observed["terminalSpecRows"]),
            },
            frontier_counts,
        )
        counts = self.validator.validate_active_corpus_residue_closure(REPOSITORY_ROOT)
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

    def test_terminal_owner_paths_require_stage_zero_index(self) -> None:
        cases = (
            (self.validator.SPEC_ROOT, self.validator.OWNER_SPEC),
            (self.validator.PLAN_ROOT, self.validator.EXECUTION_PLAN),
            (self.validator.TASK_ROOT, self.validator.EXECUTION_TASK),
        )
        for scope, missing in cases:
            with self.subTest(missing=missing):

                def runner(_root: str, arguments: tuple[str, ...]):
                    if arguments[1:6] == (
                        "-z",
                        "--cached",
                        "--others",
                        "--exclude-standard",
                        "--",
                    ):
                        payload = f"{missing}\0".encode()
                    else:
                        payload = b""
                    return subprocess.CompletedProcess(arguments, 0, payload, b"")

                with self.assertRaises(self.validator.ClosureError) as raised:
                    self.validator._inventory(str(REPOSITORY_ROOT), scope, runner)
                self.assertEqual(raised.exception.code, "CLOSURE-OWNER-INVENTORY")
                self.assertEqual(raised.exception.path, missing)

    def test_control_paths_require_stage_zero_index(self) -> None:
        listed = "\0".join(self.validator.CONTROL_PATHS).encode() + b"\0"
        for missing in self.validator.CONTROL_PATHS:
            with self.subTest(missing=missing):
                present = [
                    path for path in self.validator.CONTROL_PATHS if path != missing
                ]
                staged = b"".join(
                    (
                        f"{'100755' if path == self.validator.AGGREGATE_PATH else '100644'} "
                        f"{'a' * 40} 0\t{path}\0"
                    ).encode()
                    for path in present
                )

                def runner(_root: str, arguments: tuple[str, ...]):
                    payload = listed if "--others" in arguments else staged
                    return subprocess.CompletedProcess(arguments, 0, payload, b"")

                with self.assertRaises(self.validator.ClosureError) as raised:
                    self.validator._control_inventory(str(REPOSITORY_ROOT), runner)
                self.assertEqual(raised.exception.code, "CLOSURE-CONTROL-INVENTORY")
                self.assertEqual(raised.exception.path, missing)

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

    def test_ledger_prebinds_terminal_lineage_worktree_blobs_for_parent_staging(
        self,
    ) -> None:
        rows = {
            row["path"]: row
            for row in (
                *self.ledger["currentRows"],
                *self.ledger["authorityGuards"]["doneSpecs"],
            )
        }
        for path in (
            self.validator.OWNER_SPEC,
            self.validator.EXECUTION_PLAN,
            self.validator.EXECUTION_TASK,
        ):
            payload = self.validator._read_descriptor_bytes(str(REPOSITORY_ROOT), path)
            object_id = hashlib.sha1(
                f"blob {len(payload)}\0".encode("ascii") + payload
            ).hexdigest()
            self.assertEqual(rows[path]["objectMode"], "index-stage-zero")
            self.assertEqual(rows[path]["objectId"], f"git:sha1:{object_id}")

    def test_terminal_spec037_controls_become_owned_defer_without_source_rewrite(
        self,
    ) -> None:
        plan_path = (
            "docs/04.execution/plans/"
            "2026-07-18-active-corpus-and-execution-retention.md"
        )
        task_path = self.validator.EXECUTION_TASK
        payloads = {
            plan_path: b"---\ntype: sdlc/plan\nstatus: done\nowner: platform\n---\n",
            task_path: b"---\ntype: sdlc/task\nstatus: done\nowner: platform\n---\n",
        }
        controls = [
            {
                "path": path,
                "kind": kind,
                "pairKey": "2026-07-18-active-corpus-and-execution-retention",
                "disposition": "retain",
                "reason": "active-spec-037-control",
                "owner": "platform",
                "refreshTrigger": "Spec037 closure",
            }
            for path, kind in ((plan_path, "plan"), (task_path, "task"))
        ]

        rows = self.validator._build_current_rows(
            [plan_path],
            [task_path],
            {},
            payloads,
            {"candidateRows": [], "controls": controls},
        )

        self.assertEqual(len(rows), 2)
        for row in rows:
            self.assertEqual(row["status"], "done")
            self.assertEqual(row["sourceDisposition"], "retain")
            self.assertEqual(row["sourceReason"], "active-spec-037-control")
            self.assertEqual(row["sourceOwner"], "platform")
            self.assertEqual(row["sourceRefreshTrigger"], "Spec037 closure")
            self.assertEqual(row["disposition"], "DEFER")
            self.assertEqual(row["owner"], "platform")
            self.assertEqual(row["reason"], self.validator.TERMINAL_CONTROL_REASON)
            self.assertEqual(
                row["currentEvidenceRole"],
                self.validator.TERMINAL_CONTROL_EVIDENCE_ROLE,
            )
            self.assertEqual(
                row["successorRefreshTrigger"],
                self.validator.TERMINAL_CONTROL_REFRESH_TRIGGER,
            )
            self.assertNotIn("currentAuthority", row)
            self.assertNotIn("closureTrigger", row)

    def test_partial_or_incorrect_terminal_control_state_fails(self) -> None:
        plan_path = (
            "docs/04.execution/plans/"
            "2026-07-18-active-corpus-and-execution-retention.md"
        )
        task_path = self.validator.EXECUTION_TASK
        controls = [
            {
                "path": path,
                "kind": kind,
                "pairKey": "2026-07-18-active-corpus-and-execution-retention",
                "disposition": "retain",
                "reason": "active-spec-037-control",
                "owner": "platform",
                "refreshTrigger": "Spec037 closure",
            }
            for path, kind in ((plan_path, "plan"), (task_path, "task"))
        ]
        payloads = {
            plan_path: b"---\ntype: sdlc/plan\nstatus: done\nowner: platform\n---\n",
            task_path: b"---\ntype: sdlc/task\nstatus: active\nowner: platform\n---\n",
        }
        with self.assertRaises(self.validator.ClosureError) as raised:
            self.validator._build_current_rows(
                [plan_path],
                [task_path],
                {},
                payloads,
                {"candidateRows": [], "controls": controls},
            )
        self.assertEqual(raised.exception.code, "CLOSURE-CONTROL-STATUS")

    def test_post_closure_active_pair_is_admitted_outside_frozen_rows(self) -> None:
        plan_path = self.validator.EXECUTION_PLAN
        task_path = self.validator.EXECUTION_TASK
        active_plan = "docs/04.execution/plans/2099-01-01-active-control.md"
        active_task = "docs/04.execution/tasks/2099-01-01-active-control.md"
        controls = [
            {
                "path": path,
                "kind": kind,
                "pairKey": "2026-07-18-active-corpus-and-execution-retention",
                "disposition": "retain",
                "reason": "active-spec-037-control",
                "owner": "platform",
                "refreshTrigger": "Spec037 closure",
            }
            for path, kind in ((plan_path, "plan"), (task_path, "task"))
        ]
        payloads = {
            plan_path: b"---\ntype: sdlc/plan\nstatus: done\nowner: platform\n---\n",
            task_path: b"---\ntype: sdlc/task\nstatus: done\nowner: platform\n---\n",
            active_plan: b"---\ntype: sdlc/plan\nstatus: active\nowner: platform\n---\n",
            active_task: b"---\ntype: sdlc/task\nstatus: active\nowner: platform\n---\n",
        }

        frozen_rows = self.validator._build_current_rows(
            [plan_path, active_plan],
            [task_path, active_task],
            {},
            payloads,
            {"candidateRows": [], "controls": controls},
        )
        active_rows = self.validator._build_active_control_rows(
            [active_plan], [active_task], {}, payloads
        )
        active_pairs = self.validator._build_active_control_pairs(active_rows)

        self.assertEqual(len(frozen_rows), 2)
        self.assertTrue(all(row["status"] == "done" for row in frozen_rows))
        self.assertEqual(
            [row["lineageId"] for row in active_rows],
            ["2099-01-01-active-control", "2099-01-01-active-control"],
        )
        self.assertEqual(len(active_pairs), 1)
        self.assertEqual(active_pairs[0]["state"], "complete")

    def test_terminal_program_scope_excludes_later_execution_controls(self) -> None:
        later_plan = "docs/04.execution/plans/2099-01-01-later-program.md"
        later_task = "docs/04.execution/tasks/2099-01-01-later-program.md"

        self.assertEqual(
            self.validator._terminal_program_control_scope(
                [
                    self.validator.TERMINAL_PLAN,
                    later_plan,
                    self.validator.TERMINAL_SUCCESSOR_PLAN,
                    self.validator.TERMINAL_FRONTIER_PLAN,
                ],
                kind="plan",
            ),
            [
                self.validator.TERMINAL_PLAN,
                self.validator.TERMINAL_SUCCESSOR_PLAN,
                self.validator.TERMINAL_FRONTIER_PLAN,
            ],
        )
        self.assertEqual(
            self.validator._terminal_program_control_scope(
                [
                    self.validator.TERMINAL_TASK,
                    later_task,
                    self.validator.TERMINAL_SUCCESSOR_TASK,
                    self.validator.TERMINAL_FRONTIER_TASK,
                ],
                kind="task",
            ),
            [
                self.validator.TERMINAL_TASK,
                self.validator.TERMINAL_SUCCESSOR_TASK,
                self.validator.TERMINAL_FRONTIER_TASK,
            ],
        )
        with self.assertRaisesRegex(ValueError, "unsupported terminal control kind"):
            self.validator._terminal_program_control_scope([], kind="spec")

    def test_frozen_authority_scope_excludes_later_program_authority(self) -> None:
        expected_future_adrs = [
            "docs/02.architecture/decisions/"
            "0019-provider-native-agent-harness-and-loop-model.md",
            "docs/02.architecture/decisions/"
            "0021-canonical-surface-routing-and-evidence-depth.md",
            "docs/02.architecture/decisions/"
            "0022-direct-approval-standalone-execution-lineage.md",
            "docs/02.architecture/decisions/"
            "0023-argo-cd-source-integrity-non-adoption.md",
        ]
        expected_future_specs = [
            "docs/03.specs/041-stage-00-agent-governance-contract/spec.md",
            "docs/03.specs/042-provider-native-runtime-and-model-evidence/spec.md",
            "docs/03.specs/043-agent-harness-loop-lifecycle/spec.md",
            "docs/03.specs/044-agent-roster-evaluation-and-admission/spec.md",
            "docs/03.specs/045-agent-governance-ci-qa-cutover/spec.md",
            "docs/03.specs/046-agent-governance-program-closure/spec.md",
            "docs/03.specs/053-workspace-engineering-research-pack-consolidation/spec.md",
            "docs/03.specs/054-workspace-governance-audit-and-remediation/spec.md",
            "docs/03.specs/055-workspace-engineering-gap-only-refresh/spec.md",
            "docs/03.specs/"
            "056-workspace-engineering-partial-defer-incremental-refresh/spec.md",
            "docs/03.specs/"
            "057-workspace-research-consistency-and-partial-refresh/spec.md",
            "docs/03.specs/058-workspace-research-full-corpus-refresh/spec.md",
            "docs/03.specs/059-platform-currency-defect-closure/spec.md",
            "docs/03.specs/060-workload-security-context-baseline/spec.md",
        ]
        future_adrs = sorted(self.validator.POST_CLOSURE_ADR_AUTHORITY_PATHS)
        future_specs = sorted(self.validator.POST_CLOSURE_SPEC_AUTHORITY_PATHS)
        self.assertEqual(future_adrs, expected_future_adrs)
        self.assertEqual(future_specs, expected_future_specs)
        accepted_payload = (
            b"---\ntype: sdlc/adr\nstatus: accepted\nowner: platform\n---\n"
        )
        done_payload = b"---\ntype: sdlc/spec\nstatus: done\nowner: platform\n---\n"
        payloads = {
            **{
                path: accepted_payload
                for path in self.validator.FROZEN_ACCEPTED_ADR_PATHS
            },
            **{path: done_payload for path in self.validator.FROZEN_DONE_SPEC_PATHS},
            **{path: accepted_payload for path in future_adrs},
            **{path: done_payload for path in future_specs},
        }

        adr_scope = self.validator._frozen_authority_scope(
            [*self.validator.FROZEN_ACCEPTED_ADR_PATHS, *future_adrs],
            kind="adr",
        )
        spec_scope = self.validator._frozen_authority_scope(
            [*self.validator.FROZEN_DONE_SPEC_PATHS, *future_specs],
            kind="spec",
        )
        self.assertEqual(adr_scope, list(self.validator.FROZEN_ACCEPTED_ADR_PATHS))
        self.assertEqual(spec_scope, list(self.validator.FROZEN_DONE_SPEC_PATHS))
        self.assertEqual(
            [
                row["path"]
                for row in self.validator._frozen_authority_entries(
                    [*adr_scope, *future_adrs], {}, payloads, kind="adr"
                )
            ],
            list(self.validator.FROZEN_ACCEPTED_ADR_PATHS),
        )
        self.assertEqual(
            [
                row["path"]
                for row in self.validator._frozen_authority_entries(
                    [*spec_scope, *future_specs], {}, payloads, kind="spec"
                )
            ],
            list(self.validator.FROZEN_DONE_SPEC_PATHS),
        )
        for kind, frozen, future in (
            ("adr", self.validator.FROZEN_ACCEPTED_ADR_PATHS, future_adrs),
            ("spec", self.validator.FROZEN_DONE_SPEC_PATHS, future_specs),
        ):
            for frozen_path in frozen:
                with self.subTest(kind=kind, path=frozen_path, mutation="missing"):
                    with self.assertRaises(self.validator.ClosureError) as raised:
                        self.validator._frozen_authority_scope(
                            [
                                *(path for path in frozen if path != frozen_path),
                                *future,
                            ],
                            kind=kind,
                        )
                    self.assertEqual(raised.exception.code, "CLOSURE-AUTHORITY-SCOPE")
                    self.assertEqual(raised.exception.path, frozen_path)
                with self.subTest(kind=kind, path=frozen_path, mutation="duplicate"):
                    with self.assertRaises(self.validator.ClosureError) as raised:
                        self.validator._frozen_authority_scope(
                            [*frozen, frozen_path, *future],
                            kind=kind,
                        )
                    self.assertEqual(raised.exception.code, "CLOSURE-AUTHORITY-SCOPE")
                    self.assertEqual(raised.exception.path, frozen_path)
                with self.subTest(kind=kind, path=frozen_path, mutation="status"):
                    mutated_payloads = dict(payloads)
                    expected_type = f"sdlc/{kind}"
                    mutated_payloads[frozen_path] = (
                        "---\n"
                        f"type: {expected_type}\n"
                        "status: active\n"
                        "owner: platform\n"
                        "---\n"
                    ).encode()
                    with self.assertRaises(self.validator.ClosureError) as raised:
                        self.validator._frozen_authority_entries(
                            [*frozen, *future],
                            {},
                            mutated_payloads,
                            kind=kind,
                        )
                    self.assertEqual(raised.exception.code, "CLOSURE-AUTHORITY-SCOPE")
                    self.assertEqual(raised.exception.path, frozen_path)
        rogue_adr = "docs/02.architecture/decisions/2099-rogue-accepted-decision.md"
        rogue_spec = "docs/03.specs/999-rogue-done-spec/spec.md"
        for kind, frozen, future, rogue_path, rogue_payload in (
            (
                "adr",
                self.validator.FROZEN_ACCEPTED_ADR_PATHS,
                future_adrs,
                self.validator.TERMINAL_PROGRAM_CLOSURE_ADR,
                accepted_payload,
            ),
            (
                "adr",
                self.validator.FROZEN_ACCEPTED_ADR_PATHS,
                future_adrs,
                rogue_adr,
                accepted_payload,
            ),
            (
                "spec",
                self.validator.FROZEN_DONE_SPEC_PATHS,
                future_specs,
                rogue_spec,
                done_payload,
            ),
        ):
            with self.subTest(kind=kind, rogue_path=rogue_path):
                rogue_payloads = {**payloads, rogue_path: rogue_payload}
                with self.assertRaises(self.validator.ClosureError) as raised:
                    self.validator._frozen_authority_entries(
                        [*frozen, *future, rogue_path],
                        {},
                        rogue_payloads,
                        kind=kind,
                    )
                self.assertEqual(raised.exception.code, "CLOSURE-AUTHORITY-SCOPE")
                self.assertEqual(raised.exception.path, rogue_path)
        with self.assertRaisesRegex(ValueError, "unsupported frozen authority kind"):
            self.validator._frozen_authority_scope([], kind="plan")

    def test_spec038_active_and_terminal_states_use_disjoint_partitions(self) -> None:
        active = self.terminal_partition("active")
        active_rows = self.validator._build_active_control_rows(
            active["planPaths"],
            active["taskPaths"],
            {},
            self.terminal_payloads("active"),
        )
        active_pairs = self.validator._build_active_control_pairs(active_rows)
        self.assertEqual(len(active_rows), 2)
        self.assertEqual(len(active_pairs), 1)
        self.assertEqual(active["terminalControlRows"], [])
        self.assertEqual(active["terminalControlPairCardinality"], [])
        self.assertEqual(active["terminalSpecRows"], [])

        terminal = self.terminal_partition("done")
        self.assertEqual(terminal["planPaths"], [self.SUCCESSOR_PLAN])
        self.assertEqual(terminal["taskPaths"], [self.SUCCESSOR_TASK])
        self.assertEqual(
            terminal["specPaths"],
            [self.validator.TERMINAL_SUCCESSOR_SPEC, self.FRONTIER_SPEC],
        )
        self.assertEqual(len(terminal["terminalControlRows"]), 2)
        self.assertEqual(
            [row["path"] for row in terminal["terminalControlRows"]],
            [self.validator.TERMINAL_PLAN, self.validator.TERMINAL_TASK],
        )
        self.assertEqual(len(terminal["terminalControlPairCardinality"]), 1)
        self.assertEqual(len(terminal["terminalSpecRows"]), 1)
        self.assertEqual(
            terminal["terminalSpecRows"][0]["path"], self.validator.TERMINAL_SPEC
        )
        self.assertEqual(
            len(self.observed["authorityGuards"]["doneSpecs"]),
            self.validator.EXPECTED_COUNTS["doneSpecs"],
        )
        self.assertNotIn(
            self.validator.TERMINAL_SPEC,
            {row["path"] for row in self.observed["authorityGuards"]["doneSpecs"]},
        )

    def test_post_closure_active_controls_fail_closed_when_malformed(self) -> None:
        plan_path = "docs/04.execution/plans/2099-01-01-active-control.md"
        task_path = "docs/04.execution/tasks/2099-01-01-active-control.md"
        cases = (
            (
                "done",
                plan_path,
                task_path,
                b"---\ntype: sdlc/plan\nstatus: done\nowner: platform\n---\n",
                b"---\ntype: sdlc/task\nstatus: active\nowner: platform\n---\n",
                "CLOSURE-ACTIVE-CONTROL-STATUS",
            ),
            (
                "draft",
                plan_path,
                task_path,
                b"---\ntype: sdlc/plan\nstatus: draft\nowner: platform\n---\n",
                b"---\ntype: sdlc/task\nstatus: active\nowner: platform\n---\n",
                "CLOSURE-ACTIVE-CONTROL-STATUS",
            ),
            (
                "wrong-owner",
                plan_path,
                task_path,
                b"---\ntype: sdlc/plan\nstatus: active\nowner: product\n---\n",
                b"---\ntype: sdlc/task\nstatus: active\nowner: platform\n---\n",
                "CLOSURE-ACTIVE-CONTROL-AUTHORITY",
            ),
            (
                "wrong-type",
                plan_path,
                task_path,
                b"---\ntype: sdlc/task\nstatus: active\nowner: platform\n---\n",
                b"---\ntype: sdlc/task\nstatus: active\nowner: platform\n---\n",
                "CLOSURE-ACTIVE-CONTROL-AUTHORITY",
            ),
            (
                "malformed-lineage",
                "docs/04.execution/plans/.md",
                "docs/04.execution/tasks/.md",
                b"---\ntype: sdlc/plan\nstatus: active\nowner: platform\n---\n",
                b"---\ntype: sdlc/task\nstatus: active\nowner: platform\n---\n",
                "CLOSURE-ACTIVE-CONTROL-LINEAGE",
            ),
        )
        for _name, plan, task, plan_payload, task_payload, code in cases:
            with self.subTest(case=_name):
                with self.assertRaises(self.validator.ClosureError) as raised:
                    self.validator._build_active_control_rows(
                        [plan], [task], {}, {plan: plan_payload, task: task_payload}
                    )
                self.assertEqual(raised.exception.code, code)

    def test_post_closure_active_controls_require_one_complete_pair(self) -> None:
        plan_path = "docs/04.execution/plans/2099-01-01-active-control.md"
        task_path = "docs/04.execution/tasks/2099-01-01-active-control.md"
        payloads = {
            plan_path: b"---\ntype: sdlc/plan\nstatus: active\nowner: platform\n---\n",
            task_path: b"---\ntype: sdlc/task\nstatus: active\nowner: platform\n---\n",
        }
        rows = self.validator._build_active_control_rows([plan_path], [], {}, payloads)
        with self.assertRaises(self.validator.ClosureError) as incomplete:
            self.validator._build_active_control_pairs(rows)
        self.assertEqual(incomplete.exception.code, "CLOSURE-ACTIVE-CONTROL-PAIR")

        duplicate = self.validator._build_active_control_rows(
            [plan_path, plan_path], [task_path], {}, payloads
        )
        with self.assertRaises(self.validator.ClosureError) as duplicated:
            self.validator._build_active_control_pairs(duplicate)
        self.assertEqual(duplicated.exception.code, "CLOSURE-ACTIVE-CONTROL-DUPLICATE")

    def test_spec038_terminal_partition_rejects_adversarial_states(self) -> None:
        cases = []

        cases.append(
            (
                "incomplete",
                {
                    "task_paths": ["docs/04.execution/tasks/other-active.md"],
                },
                "CLOSURE-TERMINAL-INCOMPLETE",
            )
        )
        cases.append(
            (
                "duplicate",
                {
                    "plan_paths": [
                        self.validator.TERMINAL_PLAN,
                        self.validator.TERMINAL_PLAN,
                    ],
                },
                "CLOSURE-TERMINAL-DUPLICATE",
            )
        )
        mixed = self.terminal_payloads("done")
        mixed[self.validator.TERMINAL_TASK] = (
            b"---\ntype: sdlc/task\nstatus: active\nowner: platform\n---\n"
        )
        cases.append(
            (
                "mixed-state",
                {"payloads": mixed},
                "CLOSURE-TERMINAL-STATE",
            )
        )
        cases.extend(
            (
                name,
                {"payloads": payloads},
                "CLOSURE-TERMINAL-AUTHORITY",
            )
            for name, payloads in (
                (
                    "wrong-type",
                    self.terminal_payloads("done", plan_type="sdlc/task"),
                ),
                (
                    "wrong-owner",
                    self.terminal_payloads("done", task_owner="product"),
                ),
            )
        )
        for field, value in (
            ("prd", "005"),
            ("ard", "0008"),
            ("order", 6),
            ("decision", "0016"),
            ("reason", "Wrong authority"),
        ):
            registry = self.terminal_registry("done")
            program = registry["programLineage"]["programs"][0]
            if field in {"prd", "ard"}:
                program[field] = value
            else:
                program["tranches"][0][field] = value
            cases.append(
                (
                    f"wrong-{field}",
                    {"registry": registry},
                    "CLOSURE-TERMINAL-REGISTRY-AUTHORITY",
                )
            )
        mismatch = self.terminal_registry("active")
        cases.append(
            (
                "registry-mismatch",
                {"registry": mismatch},
                "CLOSURE-TERMINAL-STATE",
            )
        )
        missing_relation = self.terminal_registry("done")
        missing_relation["programLineage"]["programs"][0]["tranches"].pop(0)
        cases.append(
            (
                "missing-relation",
                {"registry": missing_relation},
                "CLOSURE-TERMINAL-REGISTRY-AUTHORITY",
            )
        )
        malformed_registry = self.terminal_registry("done")
        malformed_registry["programLineage"]["programs"] = {}
        cases.append(
            (
                "malformed-registry",
                {"registry": malformed_registry},
                "CLOSURE-TERMINAL-REGISTRY-MALFORMED",
            )
        )
        duplicate_relation = self.terminal_registry("done")
        duplicate_relation["programLineage"]["programs"][0]["tranches"].append(
            copy.deepcopy(
                duplicate_relation["programLineage"]["programs"][0]["tranches"][0]
            )
        )
        cases.append(
            (
                "duplicate-relation",
                {"registry": duplicate_relation},
                "CLOSURE-TERMINAL-REGISTRY-DUPLICATE",
            )
        )
        duplicate_program = self.terminal_registry("done")
        duplicate_program["programLineage"]["programs"].append(
            copy.deepcopy(duplicate_program["programLineage"]["programs"][0])
        )
        cases.append(
            (
                "duplicate-prd006-program",
                {"registry": duplicate_program},
                "CLOSURE-TERMINAL-REGISTRY-DUPLICATE",
            )
        )
        cases.extend(
            (
                name,
                kwargs,
                "CLOSURE-TERMINAL-FRONTIER",
            )
            for name, kwargs in (
                (
                    "successor-document-relation-mismatch",
                    {
                        "payloads": self.terminal_payloads(
                            "done", successor_state="done"
                        )
                    },
                ),
                (
                    "successor-relation-document-mismatch",
                    {
                        "registry": self.terminal_registry(
                            "done", successor_state="done"
                        )
                    },
                ),
            )
        )

        for name, kwargs, code in cases:
            with self.subTest(case=name):
                with self.assertRaises(self.validator.ClosureError) as raised:
                    self.terminal_partition("done", **kwargs)
                self.assertEqual(raised.exception.code, code)

    def test_spec039_frontier_accepts_active_and_exact_advanced_states(self) -> None:
        active = self.terminal_partition("done")
        self.assertEqual(
            active["specPaths"],
            [self.validator.TERMINAL_SUCCESSOR_SPEC, self.FRONTIER_SPEC],
        )
        self.assertEqual(
            [row["path"] for row in active["terminalSpecRows"]],
            [self.validator.TERMINAL_SPEC],
        )

        retained_spec = "docs/03.specs/fixture-retained/spec.md"
        payloads = self.terminal_payloads("done", successor_state="done")
        payloads[retained_spec] = (
            b"---\ntype: sdlc/spec\nstatus: done\nowner: platform\n---\n"
        )
        advanced = self.terminal_partition(
            "done",
            payloads=payloads,
            registry=self.terminal_registry("done", successor_state="done"),
            spec_paths=[
                self.validator.TERMINAL_SPEC,
                self.validator.TERMINAL_SUCCESSOR_SPEC,
                self.FRONTIER_SPEC,
                retained_spec,
            ],
        )

        self.assertEqual(advanced["specPaths"], [self.FRONTIER_SPEC, retained_spec])
        self.assertEqual(
            [row["path"] for row in advanced["terminalSpecRows"]],
            [self.validator.TERMINAL_SPEC, self.validator.TERMINAL_SUCCESSOR_SPEC],
        )
        self.assertEqual(
            [row["spec"] for row in advanced["terminalSpecRows"]],
            ["038", "039"],
        )
        generic_done = self.validator._authority_entries(
            advanced["specPaths"], {}, payloads, kind="spec"
        )
        self.assertEqual([row["path"] for row in generic_done], [retained_spec])
        self.assertNotIn(
            self.validator.TERMINAL_SUCCESSOR_SPEC,
            {row["path"] for row in generic_done},
        )

    def test_spec039_advanced_frontier_partitions_reciprocal_controls(
        self,
    ) -> None:
        payloads = self.terminal_payloads("done", successor_state="done")
        advanced = self.terminal_partition(
            "done",
            payloads=payloads,
            registry=self.terminal_registry("done", successor_state="done"),
        )

        self.assertEqual(advanced["planPaths"], [self.FRONTIER_PLAN])
        self.assertEqual(advanced["taskPaths"], [self.FRONTIER_TASK])
        self.assertEqual(
            [row["path"] for row in advanced["terminalControlRows"]],
            [
                self.validator.TERMINAL_PLAN,
                self.SUCCESSOR_PLAN,
                self.validator.TERMINAL_TASK,
                self.SUCCESSOR_TASK,
            ],
        )
        self.assertEqual(
            [
                (row["lineageId"], row["status"])
                for row in advanced["terminalControlPairCardinality"]
            ],
            [
                (self.validator.TERMINAL_LINEAGE, "done"),
                (self.SUCCESSOR_LINEAGE, "done"),
            ],
        )
        self.assertEqual(
            [row["path"] for row in advanced["terminalSpecRows"]],
            [self.validator.TERMINAL_SPEC, self.validator.TERMINAL_SUCCESSOR_SPEC],
        )
        active_rows = self.validator._build_active_control_rows(
            advanced["planPaths"],
            advanced["taskPaths"],
            {},
            payloads,
        )
        self.assertEqual(
            [(row["path"], row["lineageId"], row["status"]) for row in active_rows],
            [
                (self.FRONTIER_PLAN, self.FRONTIER_LINEAGE, "active"),
                (self.FRONTIER_TASK, self.FRONTIER_LINEAGE, "active"),
            ],
        )
        self.assertEqual(
            self.validator._build_active_control_pairs(active_rows),
            [
                {
                    "lineageId": self.FRONTIER_LINEAGE,
                    "state": "complete",
                    "planPath": self.FRONTIER_PLAN,
                    "taskPath": self.FRONTIER_TASK,
                    "owner": "platform",
                    "status": "active",
                }
            ],
        )

    def test_spec040_final_frontier_partitions_reciprocal_controls(
        self,
    ) -> None:
        payloads = self.terminal_payloads(
            "done", successor_state="done", frontier_state="done"
        )
        terminal = self.terminal_partition(
            "done",
            payloads=payloads,
            registry=self.terminal_registry(
                "done", successor_state="done", frontier_state="done"
            ),
        )

        self.assertEqual(terminal["planPaths"], [])
        self.assertEqual(terminal["taskPaths"], [])
        self.assertEqual(terminal["specPaths"], [])
        self.assertEqual(
            [row["path"] for row in terminal["terminalControlRows"]],
            [
                self.validator.TERMINAL_PLAN,
                self.SUCCESSOR_PLAN,
                self.FRONTIER_PLAN,
                self.validator.TERMINAL_TASK,
                self.SUCCESSOR_TASK,
                self.FRONTIER_TASK,
            ],
        )
        self.assertEqual(
            [
                (row["lineageId"], row["status"])
                for row in terminal["terminalControlPairCardinality"]
            ],
            [
                (self.validator.TERMINAL_LINEAGE, "done"),
                (self.SUCCESSOR_LINEAGE, "done"),
                (self.FRONTIER_LINEAGE, "done"),
            ],
        )
        self.assertEqual(
            [row["path"] for row in terminal["terminalSpecRows"]],
            [
                self.validator.TERMINAL_SPEC,
                self.validator.TERMINAL_SUCCESSOR_SPEC,
                self.FRONTIER_SPEC,
            ],
        )
        self.assertEqual(
            [row["spec"] for row in terminal["terminalSpecRows"]],
            ["038", "039", "040"],
        )
        self.assertEqual(
            self.validator._build_active_control_rows(
                terminal["planPaths"],
                terminal["taskPaths"],
                {},
                payloads,
            ),
            [],
        )
        closure_payload = (
            b"---\ntype: sdlc/adr\nstatus: accepted\nowner: platform\n---\n"
        )
        closure_authority = self.validator._terminal_program_closure_authority(
            [self.validator.TERMINAL_PROGRAM_CLOSURE_ADR],
            {},
            {
                self.validator.TERMINAL_PROGRAM_CLOSURE_ADR: closure_payload,
            },
            terminal["terminalSpecRows"],
        )
        self.assertEqual(
            [
                (
                    row["path"],
                    row["profile"],
                    row["status"],
                    row["owner"],
                    row["authorityRole"],
                    row["frontierSpecPath"],
                )
                for row in closure_authority
            ],
            [
                (
                    self.validator.TERMINAL_PROGRAM_CLOSURE_ADR,
                    "sdlc/adr",
                    "accepted",
                    "platform",
                    "terminal-program-closure-decision",
                    self.FRONTIER_SPEC,
                )
            ],
        )
        for field, value in (
            ("type", "sdlc/ard"),
            ("status", "active"),
            ("owner", "product"),
        ):
            invalid = {
                "type": "sdlc/adr",
                "status": "accepted",
                "owner": "platform",
            }
            invalid[field] = value
            invalid_payload = (
                "---\n"
                f"type: {invalid['type']}\n"
                f"status: {invalid['status']}\n"
                f"owner: {invalid['owner']}\n"
                "---\n"
            ).encode()
            with self.subTest(terminal_closure_authority=field):
                with self.assertRaises(self.validator.ClosureError) as raised:
                    self.validator._terminal_program_closure_authority(
                        [self.validator.TERMINAL_PROGRAM_CLOSURE_ADR],
                        {},
                        {
                            self.validator.TERMINAL_PROGRAM_CLOSURE_ADR: invalid_payload,
                        },
                        terminal["terminalSpecRows"],
                    )
                self.assertEqual(
                    raised.exception.code,
                    "CLOSURE-TERMINAL-AUTHORITY",
                )
        early = self.terminal_partition(
            "done",
            payloads=self.terminal_payloads(
                "done",
                successor_state="done",
                frontier_state="active",
            ),
            registry=self.terminal_registry(
                "done",
                successor_state="done",
                frontier_state="active",
            ),
        )
        self.assertEqual(
            self.validator._terminal_program_closure_authority(
                [self.validator.TERMINAL_PROGRAM_CLOSURE_ADR],
                {},
                {
                    self.validator.TERMINAL_PROGRAM_CLOSURE_ADR: closure_payload,
                },
                early["terminalSpecRows"],
            ),
            [],
        )
        rogue_adr = "docs/02.architecture/decisions/2099-rogue-accepted-decision.md"
        self.assertEqual(
            self.validator._generic_adr_authority_paths(
                [self.validator.TERMINAL_PROGRAM_CLOSURE_ADR, rogue_adr],
                [],
            ),
            [self.validator.TERMINAL_PROGRAM_CLOSURE_ADR, rogue_adr],
        )
        self.assertEqual(
            self.validator._generic_adr_authority_paths(
                [self.validator.TERMINAL_PROGRAM_CLOSURE_ADR, rogue_adr],
                closure_authority,
            ),
            [rogue_adr],
        )
        rogue_entries = self.validator._authority_entries(
            [rogue_adr],
            {},
            {rogue_adr: closure_payload},
            kind="adr",
        )
        self.assertEqual(
            [row["path"] for row in rogue_entries],
            [rogue_adr],
        )

    def test_spec039_reciprocal_controls_reject_malformed_frontiers(self) -> None:
        base_payloads = self.terminal_payloads("done", successor_state="done")
        base_registry = self.terminal_registry("done", successor_state="done")
        cases = (
            (
                "mixed-plan-state",
                {
                    "payloads": self.terminal_payloads(
                        "done",
                        successor_state="done",
                        successor_plan_state="active",
                    )
                },
                "CLOSURE-TERMINAL-FRONTIER",
            ),
            (
                "mixed-task-state",
                {
                    "payloads": self.terminal_payloads(
                        "done",
                        successor_state="done",
                        successor_task_state="active",
                    )
                },
                "CLOSURE-TERMINAL-FRONTIER",
            ),
            (
                "missing-plan",
                {"plan_paths": [self.validator.TERMINAL_PLAN]},
                "CLOSURE-TERMINAL-FRONTIER",
            ),
            (
                "duplicate-task",
                {
                    "task_paths": [
                        self.validator.TERMINAL_TASK,
                        self.SUCCESSOR_TASK,
                        self.SUCCESSOR_TASK,
                    ]
                },
                "CLOSURE-TERMINAL-DUPLICATE",
            ),
            (
                "wrong-plan-profile",
                {
                    "payloads": self.terminal_payloads(
                        "done",
                        successor_state="done",
                        successor_plan_type="sdlc/task",
                    )
                },
                "CLOSURE-TERMINAL-AUTHORITY",
            ),
            (
                "wrong-task-owner",
                {
                    "payloads": self.terminal_payloads(
                        "done",
                        successor_state="done",
                        successor_task_owner="product",
                    )
                },
                "CLOSURE-TERMINAL-AUTHORITY",
            ),
        )
        for name, overrides, code in cases:
            with self.subTest(case=name):
                parameters = {
                    "payloads": base_payloads,
                    "registry": base_registry,
                }
                parameters.update(overrides)
                with self.assertRaises(self.validator.ClosureError) as raised:
                    self.terminal_partition("done", **parameters)
                self.assertEqual(raised.exception.code, code)

    def test_spec040_frontier_rejects_closed_missing_and_duplicate_states(
        self,
    ) -> None:
        missing_document_paths = [
            self.validator.TERMINAL_SPEC,
            self.validator.TERMINAL_SUCCESSOR_SPEC,
        ]
        missing_relation = self.terminal_registry("done", successor_state="done")
        missing_relation["programLineage"]["programs"][0]["tranches"].pop()
        duplicate_relation = self.terminal_registry("done", successor_state="done")
        duplicate_relation["programLineage"]["programs"][0]["tranches"].append(
            copy.deepcopy(
                duplicate_relation["programLineage"]["programs"][0]["tranches"][-1]
            )
        )
        active_missing_relation = self.terminal_registry("done")
        active_missing_relation["programLineage"]["programs"][0]["tranches"].pop()
        active_duplicate_relation = self.terminal_registry("done")
        active_duplicate_relation["programLineage"]["programs"][0]["tranches"].append(
            copy.deepcopy(
                active_duplicate_relation["programLineage"]["programs"][0]["tranches"][
                    -1
                ]
            )
        )
        cases = (
            (
                "active-missing-document",
                {
                    "spec_paths": missing_document_paths,
                },
                "CLOSURE-TERMINAL-FRONTIER",
            ),
            (
                "active-missing-relation",
                {
                    "registry": active_missing_relation,
                },
                "CLOSURE-TERMINAL-FRONTIER",
            ),
            (
                "active-duplicate-relation",
                {
                    "registry": active_duplicate_relation,
                },
                "CLOSURE-TERMINAL-REGISTRY-DUPLICATE",
            ),
            (
                "closed-missing-plan",
                {
                    "payloads": {
                        path: payload
                        for path, payload in self.terminal_payloads(
                            "done",
                            successor_state="done",
                            frontier_state="done",
                        ).items()
                        if path != self.FRONTIER_PLAN
                    },
                    "registry": self.terminal_registry(
                        "done",
                        successor_state="done",
                        frontier_state="done",
                    ),
                    "plan_paths": [
                        self.validator.TERMINAL_PLAN,
                        self.SUCCESSOR_PLAN,
                    ],
                },
                "CLOSURE-TERMINAL-FRONTIER",
            ),
            (
                "closed-missing-task",
                {
                    "payloads": {
                        path: payload
                        for path, payload in self.terminal_payloads(
                            "done",
                            successor_state="done",
                            frontier_state="done",
                        ).items()
                        if path != self.FRONTIER_TASK
                    },
                    "registry": self.terminal_registry(
                        "done",
                        successor_state="done",
                        frontier_state="done",
                    ),
                    "task_paths": [
                        self.validator.TERMINAL_TASK,
                        self.SUCCESSOR_TASK,
                    ],
                },
                "CLOSURE-TERMINAL-FRONTIER",
            ),
            (
                "missing-document",
                {
                    "payloads": self.terminal_payloads(
                        "done",
                        successor_state="done",
                    ),
                    "registry": self.terminal_registry(
                        "done",
                        successor_state="done",
                    ),
                    "spec_paths": missing_document_paths,
                },
                "CLOSURE-TERMINAL-FRONTIER",
            ),
            (
                "missing-relation",
                {
                    "payloads": self.terminal_payloads(
                        "done",
                        successor_state="done",
                    ),
                    "registry": missing_relation,
                },
                "CLOSURE-TERMINAL-FRONTIER",
            ),
            (
                "duplicate-relation",
                {
                    "payloads": self.terminal_payloads(
                        "done",
                        successor_state="done",
                    ),
                    "registry": duplicate_relation,
                },
                "CLOSURE-TERMINAL-REGISTRY-DUPLICATE",
            ),
        )
        for name, kwargs, code in cases:
            with self.subTest(case=name):
                with self.assertRaises(self.validator.ClosureError) as raised:
                    self.terminal_partition("done", **kwargs)
                self.assertEqual(raised.exception.code, code)

    def test_spec040_frontier_rejects_wrong_relation_and_document_authority(
        self,
    ) -> None:
        cases: list[tuple[str, dict[str, object], str]] = []
        for field, value in (
            ("order", 8),
            ("reason", "Wrong frontier"),
            ("decision", "0018"),
            ("spec", "041"),
        ):
            registry = self.terminal_registry("done", successor_state="done")
            registry["programLineage"]["programs"][0]["tranches"][-1][field] = value
            cases.append(
                (
                    f"wrong-{field}",
                    {"registry": registry},
                    "CLOSURE-TERMINAL-FRONTIER",
                )
            )
        follow_up_registry = self.terminal_registry("done", successor_state="done")
        program = follow_up_registry["programLineage"]["programs"][0]
        program["followUps"].append(program["tranches"].pop())
        cases.append(
            (
                "wrong-relation-class",
                {"registry": follow_up_registry},
                "CLOSURE-TERMINAL-FRONTIER",
            )
        )
        for name, payloads in (
            (
                "wrong-profile",
                self.terminal_payloads(
                    "done",
                    successor_state="done",
                    frontier_type="sdlc/guide",
                ),
            ),
            (
                "wrong-owner",
                self.terminal_payloads(
                    "done",
                    successor_state="done",
                    frontier_owner="product",
                ),
            ),
            (
                "wrong-status",
                self.terminal_payloads(
                    "done",
                    successor_state="done",
                    frontier_state="draft",
                ),
            ),
        ):
            cases.append(
                (
                    name,
                    {"payloads": payloads},
                    "CLOSURE-TERMINAL-AUTHORITY"
                    if name != "wrong-status"
                    else "CLOSURE-TERMINAL-FRONTIER",
                )
            )

        for name, kwargs, code in cases:
            with self.subTest(case=name):
                parameters = {
                    "payloads": self.terminal_payloads("done", successor_state="done"),
                    "registry": self.terminal_registry("done", successor_state="done"),
                }
                parameters.update(kwargs)
                with self.assertRaises(self.validator.ClosureError) as raised:
                    self.terminal_partition("done", **parameters)
                self.assertEqual(raised.exception.code, code)

    def test_terminal_frontier_self_test_covers_active_advanced_final_and_blocked(
        self,
    ) -> None:
        self.assertEqual(self.validator._self_test_terminal_frontier(), 4)
        self.assertEqual(self.validator.run_self_test(), 25)

    def test_spec038_terminal_partition_rejects_rogue_done_stage04(self) -> None:
        rogue_plan = "docs/04.execution/plans/2099-01-01-rogue-done.md"
        payloads = self.terminal_payloads("done")
        payloads[rogue_plan] = (
            b"---\ntype: sdlc/plan\nstatus: done\nowner: platform\n---\n"
        )
        partition = self.terminal_partition(
            "done",
            payloads=payloads,
            plan_paths=[
                self.validator.TERMINAL_PLAN,
                self.SUCCESSOR_PLAN,
                rogue_plan,
            ],
        )
        with self.assertRaises(self.validator.ClosureError) as raised:
            self.validator._build_active_control_rows(
                partition["planPaths"],
                partition["taskPaths"],
                {},
                payloads,
            )
        self.assertEqual(raised.exception.code, "CLOSURE-ACTIVE-CONTROL-STATUS")

    def test_spec038_registry_authority_is_exact_tracked_stage_zero(self) -> None:
        path = self.validator.REGISTRY_PATH
        listed = f"{path}\0".encode()
        staged = f"100644 {'a' * 40} 0\t{path}\0".encode()
        cases = (
            ("missing", b"", b"", "CLOSURE-REGISTRY-INVENTORY"),
            ("untracked", listed, b"", "CLOSURE-REGISTRY-INVENTORY"),
            (
                "duplicate",
                listed + listed,
                staged,
                "CLOSURE-INVENTORY-DUPLICATE",
            ),
            ("malformed", path.encode(), staged, "CLOSURE-GIT-MALFORMED"),
            (
                "unsafe",
                b"../document-profiles.json\0",
                staged,
                "CLOSURE-INVENTORY-PATH",
            ),
            (
                "non-stage-zero",
                listed,
                f"100644 {'a' * 40} 1\t{path}\0".encode(),
                "CLOSURE-INVENTORY-OBJECT",
            ),
        )
        for name, paths_payload, modes_payload, code in cases:
            with self.subTest(case=name):

                def runner(_root: str, arguments: tuple[str, ...]):
                    payload = (
                        paths_payload if "--others" in arguments else modes_payload
                    )
                    return subprocess.CompletedProcess(arguments, 0, payload, b"")

                with self.assertRaises(self.validator.ClosureError) as raised:
                    self.validator._registry_inventory(str(REPOSITORY_ROOT), runner)
                self.assertEqual(raised.exception.code, code)

        with (
            mock.patch.object(
                self.validator, "_registry_inventory", return_value={path: "a" * 40}
            ),
            mock.patch.object(
                self.validator, "_read_descriptor_bytes", return_value=b"worktree"
            ),
            mock.patch.object(
                self.validator, "_index_blob", return_value=b"staged registry"
            ),
        ):
            with self.assertRaises(self.validator.ClosureError) as raised:
                self.validator._load_registry_authority(str(REPOSITORY_ROOT))
        self.assertEqual(raised.exception.code, "CLOSURE-WORKTREE-INDEX-DRIFT")
        self.assertEqual(raised.exception.path, path)

    def test_production_rejects_unadmitted_stage04_artifacts(self) -> None:
        original_inventory = self.validator._inventory
        original_payload = self.validator._proposed_or_index_bytes
        cases = (
            "docs/04.execution/plans/rogue.txt",
            "docs/04.execution/plans/nested/rogue.txt",
        )
        for rogue_path in cases:
            with self.subTest(rogue_path=rogue_path):

                def inventory(root: str, scope: str, runner):
                    paths, modes = original_inventory(root, scope, runner)
                    if scope == self.validator.PLAN_ROOT:
                        return [*paths, rogue_path], modes
                    return paths, modes

                def payload(root: str, path: str, index, runner):
                    if path == rogue_path:
                        return b"unadmitted fixture"
                    return original_payload(root, path, index, runner)

                with (
                    mock.patch.object(
                        self.validator, "_inventory", side_effect=inventory
                    ),
                    mock.patch.object(
                        self.validator,
                        "_proposed_or_index_bytes",
                        side_effect=payload,
                    ),
                ):
                    with self.assertRaises(self.validator.ClosureError) as raised:
                        self.validator.build_observed(REPOSITORY_ROOT)
                self.assertEqual(raised.exception.code, "CLOSURE-STAGE04-PATH")
                self.assertEqual(
                    str(raised.exception), f"CLOSURE-STAGE04-PATH {rogue_path}"
                )

    def test_production_allows_existing_stage04_support_readmes(self) -> None:
        observed = self.validator.build_observed(REPOSITORY_ROOT)
        self.assert_production_observed(observed)

    def test_production_validator_accepts_only_exact_frontier_shapes(self) -> None:
        def observed_for(
            *, successor_state: str, frontier_state: str = "active"
        ) -> tuple[dict[str, object], dict[str, str]]:
            payloads = self.terminal_payloads(
                "done",
                successor_state=successor_state,
                frontier_state=frontier_state,
            )
            partition = self.terminal_partition(
                "done",
                payloads=payloads,
                registry=self.terminal_registry(
                    "done",
                    successor_state=successor_state,
                    frontier_state=frontier_state,
                ),
            )
            active_rows = self.validator._build_active_control_rows(
                partition["planPaths"],
                partition["taskPaths"],
                {},
                payloads,
            )
            observed = copy.deepcopy(self.observed)
            observed.update(
                {
                    "activeControlRows": active_rows,
                    "activeControlPairCardinality": self.validator._build_active_control_pairs(
                        active_rows
                    ),
                    "terminalControlRows": partition["terminalControlRows"],
                    "terminalControlPairCardinality": partition[
                        "terminalControlPairCardinality"
                    ],
                    "terminalSpecRows": partition["terminalSpecRows"],
                    "terminalProgramClosureAuthority": [],
                }
            )
            if frontier_state == "done":
                closure_payload = (
                    b"---\ntype: sdlc/adr\nstatus: accepted\nowner: platform\n---\n"
                )
                observed["terminalProgramClosureAuthority"] = (
                    self.validator._terminal_program_closure_authority(
                        [self.validator.TERMINAL_PROGRAM_CLOSURE_ADR],
                        {},
                        {
                            self.validator.TERMINAL_PROGRAM_CLOSURE_ADR: closure_payload,
                        },
                        partition["terminalSpecRows"],
                    )
                )
                for row in observed["terminalProgramClosureAuthority"]:
                    row["objectMode"] = "index-stage-zero"
                    row["objectId"] = self.git_blob_identity(closure_payload)
            expected_object_ids: dict[str, str] = {}
            for key in (
                "activeControlRows",
                "terminalControlRows",
                "terminalSpecRows",
            ):
                for row in observed[key]:
                    row["objectMode"] = "index-stage-zero"
                    identity = self.git_blob_identity(payloads[row["path"]])
                    row["objectId"] = identity
                    expected_object_ids[row["path"]] = identity
            return observed, expected_object_ids

        current, current_object_ids = observed_for(successor_state="active")
        advanced, advanced_object_ids = observed_for(successor_state="done")
        terminal, terminal_object_ids = observed_for(
            successor_state="done", frontier_state="done"
        )
        self.assert_production_observed(
            current,
            expected_object_ids=current_object_ids,
        )
        self.assert_production_observed(
            advanced,
            expected_object_ids=advanced_object_ids,
        )
        self.assert_production_observed(
            terminal,
            expected_object_ids=terminal_object_ids,
        )

        wrong_oid = copy.deepcopy(current)
        wrong_oid_path = wrong_oid["activeControlRows"][0]["path"]
        self.assertEqual(
            wrong_oid["activeControlRows"][0]["objectId"],
            current_object_ids[wrong_oid_path],
        )
        wrong_oid["activeControlRows"][0]["objectId"] = self.validator._git_identity(
            "0" * 40
        )
        with self.assertRaises(AssertionError):
            self.assert_production_observed(
                wrong_oid,
                expected_object_ids=current_object_ids,
            )

        hybrid = copy.deepcopy(advanced)
        hybrid["activeControlRows"] = copy.deepcopy(current["activeControlRows"])
        hybrid["activeControlPairCardinality"] = copy.deepcopy(
            current["activeControlPairCardinality"]
        )
        with self.assertRaises(AssertionError):
            hybrid_object_ids = copy.deepcopy(advanced_object_ids)
            hybrid_object_ids.update(
                {row["path"]: row["objectId"] for row in hybrid["activeControlRows"]}
            )
            self.assert_production_observed(
                hybrid, expected_object_ids=hybrid_object_ids
            )

        rogue = copy.deepcopy(terminal)
        rogue_plan = "docs/04.execution/plans/2099-01-01-rogue-active.md"
        rogue_task = "docs/04.execution/tasks/2099-01-01-rogue-active.md"
        rogue_lineage = "2099-01-01-rogue-active"
        rogue["activeControlRows"] = [
            {
                "path": path,
                "kind": kind,
                "lineageId": rogue_lineage,
                "profile": f"sdlc/{kind}",
                "status": "active",
                "owner": "platform",
                "objectMode": "index-stage-zero",
                "objectId": self.validator._git_identity("9" * 40),
            }
            for path, kind in ((rogue_plan, "plan"), (rogue_task, "task"))
        ]
        rogue["activeControlPairCardinality"] = [
            {
                "lineageId": rogue_lineage,
                "state": "complete",
                "planPath": rogue_plan,
                "taskPath": rogue_task,
                "owner": "platform",
                "status": "active",
            }
        ]
        with (
            mock.patch.object(self.validator, "verify_entrypoints", return_value={}),
            mock.patch.object(self.validator, "build_observed", return_value=rogue),
            mock.patch.object(self.validator, "load_ledger", return_value=self.ledger),
            mock.patch.object(self.validator, "validate_ledger"),
            self.assertRaises(self.validator.ClosureError) as raised,
        ):
            self.validator.validate_active_corpus_residue_closure(REPOSITORY_ROOT)
        self.assertEqual(raised.exception.code, "CLOSURE-TERMINAL-FRONTIER")
        self.assertEqual(raised.exception.path, rogue_plan)

    def test_frozen_terminal_path_cannot_be_promoted_to_active(self) -> None:
        plan_path = self.validator.EXECUTION_PLAN
        task_path = self.validator.EXECUTION_TASK
        controls = [
            {
                "path": path,
                "kind": kind,
                "pairKey": "2026-07-18-active-corpus-and-execution-retention",
                "disposition": "retain",
                "reason": "active-spec-037-control",
                "owner": "platform",
                "refreshTrigger": "Spec037 closure",
            }
            for path, kind in ((plan_path, "plan"), (task_path, "task"))
        ]
        payloads = {
            plan_path: b"---\ntype: sdlc/plan\nstatus: active\nowner: platform\n---\n",
            task_path: b"---\ntype: sdlc/task\nstatus: done\nowner: platform\n---\n",
        }
        with self.assertRaises(self.validator.ClosureError) as raised:
            self.validator._build_current_rows(
                [plan_path],
                [task_path],
                {},
                payloads,
                {"candidateRows": [], "controls": controls},
            )
        self.assertEqual(raised.exception.code, "CLOSURE-CONTROL-STATUS")

    def test_production_and_cli_report_active_control_counts_separately(self) -> None:
        observed = self.validator.build_observed(REPOSITORY_ROOT)
        self.assert_production_observed(observed)
        expected = {
            "activeControlRows": len(observed["activeControlRows"]),
            "activeControlPairs": len(observed["activeControlPairCardinality"]),
            "terminalControlRows": len(observed["terminalControlRows"]),
            "terminalControlPairs": len(observed["terminalControlPairCardinality"]),
            "terminalSpecs": len(observed["terminalSpecRows"]),
        }
        with (
            mock.patch.object(self.validator, "verify_entrypoints", return_value={}),
            mock.patch.object(self.validator, "build_observed", return_value=observed),
            mock.patch.object(self.validator, "load_ledger", return_value=self.ledger),
            mock.patch.object(self.validator, "validate_ledger"),
        ):
            counts = self.validator.validate_active_corpus_residue_closure(
                REPOSITORY_ROOT
            )
            for key, value in expected.items():
                self.assertEqual(counts[key], value)
            stdout = io.StringIO()
            with (
                redirect_stderr(io.StringIO()),
                mock.patch.object(
                    self.validator,
                    "validate_active_corpus_residue_closure",
                    return_value=counts,
                ),
                mock.patch("sys.stdout", stdout),
            ):
                self.assertEqual(self.validator.main(["--root", "."]), 0)
        self.assertIn(
            "active_controls="
            f"{expected['activeControlRows']}/{expected['activeControlPairs']}",
            stdout.getvalue(),
        )
        self.assertIn(
            "terminal_controls="
            f"{expected['terminalControlRows']}/{expected['terminalControlPairs']}",
            stdout.getvalue(),
        )
        self.assertIn(f"terminal_specs={expected['terminalSpecs']}", stdout.getvalue())

    def test_cli_reports_exact_spec038_terminal_partition_counts(self) -> None:
        counts = {
            "migratedClosed": 12,
            "currentRows": 100,
            "defer": 100,
            "retain": 0,
            "pairKeys": 52,
            "completePairs": 48,
            "planOnly": 1,
            "taskOnly": 3,
            "acceptedAdrs": 13,
            "doneSpecs": 29,
            "findings": 0,
            "activeControlRows": 0,
            "activeControlPairs": 0,
            "terminalControlRows": 2,
            "terminalControlPairs": 1,
            "terminalSpecs": 1,
        }
        stdout = io.StringIO()
        with (
            mock.patch.object(
                self.validator,
                "validate_active_corpus_residue_closure",
                return_value=counts,
            ),
            mock.patch("sys.stdout", stdout),
        ):
            self.assertEqual(self.validator.main(["--root", "."]), 0)
        line = stdout.getvalue()
        self.assertIn("migrated=12 current=100 dispositions=100/0", line)
        self.assertIn("pairs=52:48/1/3", line)
        self.assertIn("active_controls=0/0", line)
        self.assertIn("terminal_controls=2/1", line)
        self.assertIn("terminal_specs=1", line)
        self.assertIn("guards=13/29 findings=0", line)

    def test_terminal_pair_and_done_spec_guard_match_exact_counts(self) -> None:
        terminal_paths = {
            self.validator.EXECUTION_PLAN,
            self.validator.EXECUTION_TASK,
        }
        terminal_rows = [
            row for row in self.ledger["currentRows"] if row["path"] in terminal_paths
        ]
        self.assertEqual(len(terminal_rows), 2)
        self.assertTrue(all(row["disposition"] == "DEFER" for row in terminal_rows))
        self.assertEqual(self.ledger["counts"]["currentDefer"], 100)
        self.assertEqual(self.ledger["counts"]["currentRetain"], 0)
        self.assertEqual(self.ledger["counts"]["doneSpecs"], 29)
        self.assertIn(
            self.validator.OWNER_SPEC,
            {row["path"] for row in self.ledger["authorityGuards"]["doneSpecs"]},
        )

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
            self.assert_production_observed(observed)
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
