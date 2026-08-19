from __future__ import annotations

import copy
import importlib.util
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = REPOSITORY_ROOT / "scripts" / "validate-active-corpus-role-audit.py"
AGGREGATE_PATH = REPOSITORY_ROOT / "scripts" / "validate-repo-quality-gates.sh"


def load_validator():
    specification = importlib.util.spec_from_file_location(
        "active_corpus_role_audit_test_target", VALIDATOR_PATH
    )
    if specification is None or specification.loader is None:
        raise AssertionError("active corpus role audit validator could not be loaded")
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


class ActiveCorpusRoleAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_validator()
        cls.observed = cls.validator.build_observed(
            REPOSITORY_ROOT, enforce_index=False
        )
        cls.ledger = cls.validator.load_ledger(REPOSITORY_ROOT, enforce_index=False)

    def fixture(self):
        return copy.deepcopy(self.ledger)

    def assert_audit_error(self, fixture, code: str) -> None:
        with self.assertRaises(self.validator.RoleAuditError) as raised:
            self.validator.validate_ledger(fixture, self.observed)
        self.assertEqual(raised.exception.code, code)

    def write_git_corpus(self, root: Path, *, proposed_symlink: bool = False) -> Path:
        for collection, count in (("guides", 8), ("policies", 7), ("runbooks", 9)):
            contract = self.validator.STAGE_KINDS[collection]
            sections = "\n".join(
                f"## {section}\nFixture." for section in contract["sections"]
            )
            for index in range(count):
                path = f"docs/05.operations/{collection}/{index + 1:04d}-fixture.md"
                target = root / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(
                    "---\n"
                    f"type: {contract['profile']}\nstatus: active\nowner: platform\n"
                    "---\n# Fixture\n"
                    f"{sections}\n",
                    encoding="utf-8",
                )

        helper_paths = sorted(
            [
                *self.validator.FROZEN_HELPER_PATHS,
                *self.validator.POST_CLOSURE_HELPER_MANIFEST,
                *self.validator.TRANSITION_ONLY_HELPER_MANIFEST,
            ]
        )
        proposal_path = "tests/test_reference_information_architecture.py"
        proposal = root / proposal_path
        for path in helper_paths:
            if path in {"tests/README.md", proposal_path}:
                continue
            target = root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(
                "{}\n" if path.endswith(".json") else "fixture\n",
                encoding="utf-8",
            )
        readme = root / "tests/README.md"
        readme.parent.mkdir(parents=True, exist_ok=True)
        readme.write_text(
            "# tests\n\n## Structure\n\n```text\n"
            + "\n".join(helper_paths)
            + "\n```\n",
            encoding="utf-8",
        )
        subprocess.run(
            [self.validator.GIT_EXECUTABLE, "init", "-q"], cwd=root, check=True
        )
        if proposed_symlink:
            subprocess.run(
                [self.validator.GIT_EXECUTABLE, "add", "--", "docs", "tests"],
                cwd=root,
                check=True,
            )
            outside = root / "outside"
            outside.write_text("unsafe proposal\n", encoding="utf-8")
            proposal.symlink_to(outside)
        else:
            proposal.write_text("fixture\n", encoding="utf-8")
            subprocess.run(
                [self.validator.GIT_EXECUTABLE, "add", "--", "docs", "tests"],
                cwd=root,
                check=True,
            )
        return proposal

    def test_production_exact_counts_and_zero_findings(self) -> None:
        counts = self.validator.validate_active_corpus_role_audit(
            REPOSITORY_ROOT,
            enforce_index=False,
            enforce_entrypoints=False,
        )
        self.assertEqual(
            counts,
            {
                "stage05": 24,
                "guides": 8,
                "policies": 7,
                "runbooks": 9,
                "incidents": 0,
                "postmortems": 0,
                "helpers": 69,
                "frozenHelpers": 33,
                "postClosureHelpers": 36,
                "python": 31,
                "json": 31,
                "yaml": 6,
                "readme": 1,
                "findings": 0,
            },
        )

    def test_stage05_role_sections_are_separated_by_type(self) -> None:
        expected = {
            "guide": ["Overview", "Guide Type", "Target Audience", "Prerequisites"],
            "policy": ["Overview", "Policy Scope", "Applies To", "Controls"],
            "runbook": [
                "Overview",
                "Runbook Type",
                "When to Use",
                "Procedure or Checklist",
            ],
        }
        for entry in self.observed["stage05"]["entries"]:
            self.assertEqual(entry["requiredSections"], expected[entry["kind"]])
            self.assertEqual(entry["role"], "authored-operation")
            self.assertEqual(entry["owner"], "platform")
            self.assertEqual(entry["status"], "active")

    def test_empty_incident_and_postmortem_collections_are_valid(self) -> None:
        counts = self.observed["stage05"]["counts"]
        self.assertEqual((counts["incident"], counts["postmortem"]), (0, 0))
        self.assertFalse(
            any(
                entry["kind"] in {"incident", "postmortem"}
                for entry in self.observed["stage05"]["entries"]
            )
        )

    def test_helper_roles_are_support_only(self) -> None:
        roles = {entry["role"] for entry in self.observed["helperTests"]["entries"]}
        self.assertEqual(
            roles,
            {
                "regression-test",
                "closed-fixture",
                "manifest-fixture",
                "validation-evidence-boundary",
            },
        )
        self.assertNotIn("execution-tracker", roles)
        self.assertIs(self.ledger["helperTests"]["executionTracker"], False)

    def test_frozen_authority_routes_project_through_mig_0002(self) -> None:
        self.assertEqual(
            self.ledger["authority"]["ownerSpec"],
            "docs/03.specs/037-active-corpus-and-execution-retention/spec.md",
        )
        self.assertEqual(
            self.ledger["inventoryBoundary"]["executionTracker"],
            "docs/04.execution/tasks/"
            "2026-07-18-active-corpus-and-execution-retention.md",
        )
        migration = (REPOSITORY_ROOT / self.validator.MIGRATION_PATH).read_text(
            encoding="utf-8"
        )
        projection = self.validator.validate_authority_projection(
            migration,
            {
                self.validator.CURRENT_OWNER_SPEC,
                self.validator.CURRENT_EXECUTION_TRACKER,
            },
        )
        self.assertEqual(
            projection,
            {
                self.validator.FROZEN_OWNER_SPEC: self.validator.CURRENT_OWNER_SPEC,
                self.validator.FROZEN_EXECUTION_TRACKER: (
                    self.validator.CURRENT_EXECUTION_TRACKER
                ),
            },
        )

    def test_missing_or_drifted_mig_0002_authority_projection_fails(self) -> None:
        migration = (REPOSITORY_ROOT / self.validator.MIGRATION_PATH).read_text(
            encoding="utf-8"
        )
        owner_row = (
            '"legacy_path": "docs/03.specs/037-active-corpus-and-execution-retention/'
            'spec.md"'
        )
        current_owner = (
            '"stable_path": "docs/03.specs/0037-active-corpus-and-execution-'
            'retention/spec.md"'
        )
        candidates = {
            "missing legacy authority": migration.replace(
                owner_row, owner_row.replace("037-", "038-"), 1
            ),
            "drifted current authority": migration.replace(
                current_owner, current_owner.replace("0037-", "0038-"), 1
            ),
        }
        for name, candidate in candidates.items():
            with self.subTest(name=name):
                with self.assertRaises(self.validator.RoleAuditError) as raised:
                    self.validator.validate_authority_projection(
                        candidate,
                        {
                            self.validator.CURRENT_OWNER_SPEC,
                            self.validator.CURRENT_EXECUTION_TRACKER,
                        },
                    )
                self.assertEqual(raised.exception.code, "ROLE-AUDIT-AUTHORITY")

        with self.assertRaises(self.validator.RoleAuditError) as raised:
            self.validator.validate_authority_projection(
                migration,
                {self.validator.CURRENT_OWNER_SPEC},
            )
        self.assertEqual(raised.exception.code, "ROLE-AUDIT-AUTHORITY")

    def test_readme_inventory_is_exact_and_closed(self) -> None:
        actual = [entry["path"] for entry in self.observed["helperTests"]["entries"]]
        self.assertEqual(self.observed["readmeInventory"], actual)
        self.assertEqual(len(actual), 69)
        self.assertEqual(len(self.ledger["readmeRemediation"]["finalInventory"]), 33)

    def test_post_closure_manifest_is_exact_and_identity_bound(self) -> None:
        self.assertEqual(
            self.validator.POST_CLOSURE_HELPER_MANIFEST,
            {
                "tests/fixtures/agent-checkpoint.json": (
                    "json",
                    "closed-fixture",
                ),
                "tests/fixtures/agent-evaluations.json": (
                    "json",
                    "closed-fixture",
                ),
                "tests/fixtures/agent-governance-ci.json": (
                    "json",
                    "closed-fixture",
                ),
                "tests/fixtures/agent-governance-closure.json": (
                    "json",
                    "closed-fixture",
                ),
                "tests/fixtures/agent-harness-contract.json": (
                    "json",
                    "closed-fixture",
                ),
                "tests/fixtures/agent-legacy-cutover.json": (
                    "json",
                    "closed-fixture",
                ),
                "tests/fixtures/agent-loop-lifecycle.json": (
                    "json",
                    "closed-fixture",
                ),
                "tests/fixtures/agent-model-fitness.json": (
                    "json",
                    "closed-fixture",
                ),
                "tests/fixtures/agent-provider-runtime-evidence.json": (
                    "json",
                    "closed-fixture",
                ),
                "tests/fixtures/agent-roster-admission.json": (
                    "json",
                    "closed-fixture",
                ),
                "tests/fixtures/reference-information-architecture/current-owner.json": (
                    "json",
                    "closed-fixture",
                ),
                "tests/fixtures/reference-information-architecture/generator-collision.json": (
                    "json",
                    "closed-fixture",
                ),
                "tests/fixtures/reference-information-architecture/minimal-valid.json": (
                    "json",
                    "closed-fixture",
                ),
                "tests/fixtures/reference-information-architecture/overlay-mutation.json": (
                    "json",
                    "closed-fixture",
                ),
                "tests/fixtures/reference-information-architecture/policy-copy.json": (
                    "json",
                    "closed-fixture",
                ),
                "tests/fixtures/reference-information-architecture/snapshot-mutation.json": (
                    "json",
                    "closed-fixture",
                ),
                "tests/fixtures/reference-information-architecture/source-freshness.json": (
                    "json",
                    "closed-fixture",
                ),
                "tests/test_document_lifecycle_agent_roster_cutover.py": (
                    "python",
                    "regression-test",
                ),
                "tests/test_document_strict_cutover.py": (
                    "python",
                    "regression-test",
                ),
                "tests/test_k8s_pre_edit_hook.py": (
                    "python",
                    "regression-test",
                ),
                "tests/test_reference_information_architecture.py": (
                    "python",
                    "regression-test",
                ),
                "tests/test_validate_agent_checkpoint.py": (
                    "python",
                    "regression-test",
                ),
                "tests/test_validate_agent_evaluations.py": (
                    "python",
                    "regression-test",
                ),
                "tests/test_validate_agent_governance_ci.py": (
                    "python",
                    "regression-test",
                ),
                "tests/test_validate_agent_governance_closure.py": (
                    "python",
                    "regression-test",
                ),
                "tests/test_validate_agent_harness_contract.py": (
                    "python",
                    "regression-test",
                ),
                "tests/test_validate_agent_harness_semantics.py": (
                    "python",
                    "regression-test",
                ),
                "tests/test_validate_agent_legacy_cutover.py": (
                    "python",
                    "regression-test",
                ),
                "tests/test_validate_agent_loop_lifecycle.py": (
                    "python",
                    "regression-test",
                ),
                "tests/test_validate_agent_model_fitness.py": (
                    "python",
                    "regression-test",
                ),
                "tests/test_validate_agent_provider_canaries.py": (
                    "python",
                    "regression-test",
                ),
                "tests/test_validate_agent_provider_config.py": (
                    "python",
                    "regression-test",
                ),
                "tests/test_validate_agent_roster_admission.py": (
                    "python",
                    "regression-test",
                ),
                "tests/test_validate_ci_python_contract.py": (
                    "python",
                    "regression-test",
                ),
                "tests/test_validate_gitops_change_set.py": (
                    "python",
                    "regression-test",
                ),
            },
        )
        self.assertEqual(
            self.validator.TRANSITION_ONLY_HELPER_MANIFEST,
            {
                "tests/test_migrate_document_work_units.py": (
                    "python",
                    "regression-test",
                )
            },
        )

    def test_frozen_helpers_are_an_exact_subset_with_safe_post_closure_additions(
        self,
    ) -> None:
        partition = self.validator.validate_ledger(self.ledger, self.observed)
        self.assertEqual(partition, {"frozen": 33, "postClosure": 36})
        self.assertEqual(
            self.ledger["helperTests"]["entries"],
            self.validator._expected_frozen_helper_entries(),
        )
        self.assertEqual(len(self.validator.FROZEN_HELPER_PATHS), 33)
        frozen_paths = set(self.validator.FROZEN_HELPER_PATHS)
        post_closure = [
            entry
            for entry in self.observed["helperTests"]["entries"]
            if entry["path"] not in frozen_paths
        ]
        self.assertEqual(
            post_closure,
            [
                {
                    "path": "tests/fixtures/agent-checkpoint.json",
                    "format": "json",
                    "role": "closed-fixture",
                },
                {
                    "path": "tests/fixtures/agent-evaluations.json",
                    "format": "json",
                    "role": "closed-fixture",
                },
                {
                    "path": "tests/fixtures/agent-governance-ci.json",
                    "format": "json",
                    "role": "closed-fixture",
                },
                {
                    "path": "tests/fixtures/agent-governance-closure.json",
                    "format": "json",
                    "role": "closed-fixture",
                },
                {
                    "path": "tests/fixtures/agent-harness-contract.json",
                    "format": "json",
                    "role": "closed-fixture",
                },
                {
                    "path": "tests/fixtures/agent-legacy-cutover.json",
                    "format": "json",
                    "role": "closed-fixture",
                },
                {
                    "path": "tests/fixtures/agent-loop-lifecycle.json",
                    "format": "json",
                    "role": "closed-fixture",
                },
                {
                    "path": "tests/fixtures/agent-model-fitness.json",
                    "format": "json",
                    "role": "closed-fixture",
                },
                {
                    "path": "tests/fixtures/agent-provider-runtime-evidence.json",
                    "format": "json",
                    "role": "closed-fixture",
                },
                {
                    "path": "tests/fixtures/agent-roster-admission.json",
                    "format": "json",
                    "role": "closed-fixture",
                },
                {
                    "path": "tests/fixtures/reference-information-architecture/current-owner.json",
                    "format": "json",
                    "role": "closed-fixture",
                },
                {
                    "path": "tests/fixtures/reference-information-architecture/generator-collision.json",
                    "format": "json",
                    "role": "closed-fixture",
                },
                {
                    "path": "tests/fixtures/reference-information-architecture/minimal-valid.json",
                    "format": "json",
                    "role": "closed-fixture",
                },
                {
                    "path": "tests/fixtures/reference-information-architecture/overlay-mutation.json",
                    "format": "json",
                    "role": "closed-fixture",
                },
                {
                    "path": "tests/fixtures/reference-information-architecture/policy-copy.json",
                    "format": "json",
                    "role": "closed-fixture",
                },
                {
                    "path": "tests/fixtures/reference-information-architecture/snapshot-mutation.json",
                    "format": "json",
                    "role": "closed-fixture",
                },
                {
                    "path": "tests/fixtures/reference-information-architecture/source-freshness.json",
                    "format": "json",
                    "role": "closed-fixture",
                },
                {
                    "path": "tests/test_document_lifecycle_agent_roster_cutover.py",
                    "format": "python",
                    "role": "regression-test",
                },
                {
                    "path": "tests/test_document_strict_cutover.py",
                    "format": "python",
                    "role": "regression-test",
                },
                {
                    "path": "tests/test_k8s_pre_edit_hook.py",
                    "format": "python",
                    "role": "regression-test",
                },
                {
                    "path": "tests/test_migrate_document_work_units.py",
                    "format": "python",
                    "role": "regression-test",
                },
                {
                    "path": "tests/test_reference_information_architecture.py",
                    "format": "python",
                    "role": "regression-test",
                },
                {
                    "path": "tests/test_validate_agent_checkpoint.py",
                    "format": "python",
                    "role": "regression-test",
                },
                {
                    "path": "tests/test_validate_agent_evaluations.py",
                    "format": "python",
                    "role": "regression-test",
                },
                {
                    "path": "tests/test_validate_agent_governance_ci.py",
                    "format": "python",
                    "role": "regression-test",
                },
                {
                    "path": "tests/test_validate_agent_governance_closure.py",
                    "format": "python",
                    "role": "regression-test",
                },
                {
                    "path": "tests/test_validate_agent_harness_contract.py",
                    "format": "python",
                    "role": "regression-test",
                },
                {
                    "path": "tests/test_validate_agent_harness_semantics.py",
                    "format": "python",
                    "role": "regression-test",
                },
                {
                    "path": "tests/test_validate_agent_legacy_cutover.py",
                    "format": "python",
                    "role": "regression-test",
                },
                {
                    "path": "tests/test_validate_agent_loop_lifecycle.py",
                    "format": "python",
                    "role": "regression-test",
                },
                {
                    "path": "tests/test_validate_agent_model_fitness.py",
                    "format": "python",
                    "role": "regression-test",
                },
                {
                    "path": "tests/test_validate_agent_provider_canaries.py",
                    "format": "python",
                    "role": "regression-test",
                },
                {
                    "path": "tests/test_validate_agent_provider_config.py",
                    "format": "python",
                    "role": "regression-test",
                },
                {
                    "path": "tests/test_validate_agent_roster_admission.py",
                    "format": "python",
                    "role": "regression-test",
                },
                {
                    "path": "tests/test_validate_ci_python_contract.py",
                    "format": "python",
                    "role": "regression-test",
                },
                {
                    "path": "tests/test_validate_gitops_change_set.py",
                    "format": "python",
                    "role": "regression-test",
                },
            ],
        )

    def test_readme_remediation_records_exact_delta(self) -> None:
        self.assertEqual(
            self.ledger["readmeRemediation"]["addedInventoryRows"],
            self.validator.README_ADDITIONS,
        )
        self.assertEqual(
            self.ledger["readmeRemediation"]["removedInventoryRows"],
            self.validator.README_REMOVALS,
        )

    def test_missing_stage_row_fails(self) -> None:
        fixture = self.fixture()
        fixture["stage05"]["entries"].pop()
        self.assert_audit_error(fixture, "ROLE-AUDIT-STAGE05-DRIFT")

    def test_duplicate_stage_row_fails(self) -> None:
        fixture = self.fixture()
        fixture["stage05"]["entries"].append(
            copy.deepcopy(fixture["stage05"]["entries"][0])
        )
        self.assert_audit_error(fixture, "ROLE-AUDIT-STAGE05-DUPLICATE")

    def test_wrong_stage_profile_status_owner_and_role_fail(self) -> None:
        for key, value in (
            ("profile", "sdlc/policy"),
            ("status", "draft"),
            ("owner", "unowned"),
            ("role", "execution-tracker"),
        ):
            with self.subTest(key=key):
                fixture = self.fixture()
                fixture["stage05"]["entries"][0][key] = value
                self.assert_audit_error(fixture, "ROLE-AUDIT-STAGE05-DRIFT")

    def test_missing_extra_and_duplicate_helper_rows_fail(self) -> None:
        fixture = self.fixture()
        fixture["helperTests"]["entries"].pop()
        self.assert_audit_error(fixture, "ROLE-AUDIT-HELPER-DRIFT")

        fixture = self.fixture()
        extra = copy.deepcopy(fixture["helperTests"]["entries"][0])
        extra["path"] = "tests/extra.py"
        fixture["helperTests"]["entries"].append(extra)
        fixture["helperTests"]["entries"].sort(key=lambda row: row["path"])
        self.assert_audit_error(fixture, "ROLE-AUDIT-HELPER-DRIFT")

        fixture = self.fixture()
        fixture["helperTests"]["entries"].append(
            copy.deepcopy(fixture["helperTests"]["entries"][0])
        )
        self.assert_audit_error(fixture, "ROLE-AUDIT-HELPER-DUPLICATE")

    def test_missing_or_changed_frozen_observed_helper_fails(self) -> None:
        frozen_path = self.validator.FROZEN_HELPER_PATHS[-1]
        for mutation in ("missing", "role", "path"):
            with self.subTest(mutation=mutation):
                observed = copy.deepcopy(self.observed)
                entry = next(
                    row
                    for row in observed["helperTests"]["entries"]
                    if row["path"] == frozen_path
                )
                if mutation == "missing":
                    observed["helperTests"]["entries"].remove(entry)
                    observed["readmeInventory"].remove(frozen_path)
                    observed["helperTests"]["counts"]["total"] -= 1
                    observed["helperTests"]["counts"][entry["format"]] -= 1
                elif mutation == "role":
                    entry["role"] = "execution-tracker"
                else:
                    entry["path"] = "tests/zz-renamed.py"
                    observed["helperTests"]["entries"].sort(key=lambda row: row["path"])
                    observed["readmeInventory"] = [
                        row["path"] for row in observed["helperTests"]["entries"]
                    ]
                with self.assertRaises(self.validator.RoleAuditError) as raised:
                    self.validator.validate_ledger(self.ledger, observed)
                self.assertIn(
                    raised.exception.code,
                    {
                        "ROLE-AUDIT-HELPER-ADMISSION",
                        "ROLE-AUDIT-HELPER-DRIFT",
                        "ROLE-AUDIT-HELPER-TRACKER",
                    },
                )

    def test_post_closure_helper_cannot_use_unsupported_format(self) -> None:
        paths = ["tests/README.md", "tests/post-closure.txt"]
        readme = "# tests\n\n## Structure\n\n```text\n" + "\n".join(paths) + "\n```\n"
        with self.assertRaises(self.validator.RoleAuditError) as raised:
            self.validator._helper_entries(
                paths, lambda path: readme if path == "tests/README.md" else "fixture\n"
            )
        self.assertEqual(raised.exception.code, "ROLE-AUDIT-HELPER-FORMAT")

    def test_harness_checkpoint_and_loop_helpers_are_exactly_admitted(self) -> None:
        exact = {
            "tests/fixtures/agent-checkpoint.json": (
                "json",
                "closed-fixture",
            ),
            "tests/fixtures/agent-harness-contract.json": (
                "json",
                "closed-fixture",
            ),
            "tests/fixtures/agent-loop-lifecycle.json": (
                "json",
                "closed-fixture",
            ),
            "tests/test_validate_agent_checkpoint.py": (
                "python",
                "regression-test",
            ),
            "tests/test_validate_agent_harness_contract.py": (
                "python",
                "regression-test",
            ),
            "tests/test_validate_agent_loop_lifecycle.py": (
                "python",
                "regression-test",
            ),
        }
        for path, expected in exact.items():
            with self.subTest(path=path):
                self.assertEqual(
                    self.validator._helper_format_role(path),
                    expected,
                )

        for unmanifested in (
            "tests/fixtures/agent-checkpoint-copy.json",
            "tests/fixtures/agent-harness-contract-copy.json",
            "tests/fixtures/agent-loop-lifecycle-copy.json",
            "tests/test_validate_agent_checkpoint_copy.py",
            "tests/test_validate_agent_harness_contract_copy.py",
            "tests/test_validate_agent_loop_lifecycle_copy.py",
        ):
            with self.subTest(unmanifested=unmanifested):
                with self.assertRaises(self.validator.RoleAuditError) as raised:
                    self.validator._helper_format_role(unmanifested)
                self.assertEqual(
                    raised.exception.code,
                    "ROLE-AUDIT-HELPER-ADMISSION",
                )

    def test_post_closure_helper_cannot_bypass_readme_inventory(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.write_git_corpus(root)
            omitted = "tests/test_reference_information_architecture.py"
            readme = root / "tests/README.md"
            inventory = self.validator._readme_inventory(
                readme.read_text(encoding="utf-8")
            )
            inventory.remove(omitted)
            readme.write_text(
                "# tests\n\n## Structure\n\n```text\n"
                + "\n".join(inventory)
                + "\n```\n",
                encoding="utf-8",
            )
            subprocess.run(
                [self.validator.GIT_EXECUTABLE, "add", "--", "tests/README.md"],
                cwd=root,
                check=True,
            )
            with self.assertRaises(self.validator.RoleAuditError) as raised:
                self.validator.build_observed(root)
            self.assertEqual(raised.exception.code, "ROLE-AUDIT-README-DRIFT")

    def test_readme_listed_supported_tracker_helper_fails_production_build(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.write_git_corpus(root)
            hostile_path = "tests/zz-execution-tracker.py"
            hostile = root / hostile_path
            hostile.write_text(
                "## Task Table\nTask status: In Progress\n", encoding="utf-8"
            )
            readme = root / "tests/README.md"
            inventory = sorted(
                [
                    *self.validator._readme_inventory(
                        readme.read_text(encoding="utf-8")
                    ),
                    hostile_path,
                ]
            )
            readme.write_text(
                "# tests\n\n## Structure\n\n```text\n"
                + "\n".join(inventory)
                + "\n```\n",
                encoding="utf-8",
            )
            subprocess.run(
                [
                    self.validator.GIT_EXECUTABLE,
                    "add",
                    "--",
                    hostile_path,
                    "tests/README.md",
                ],
                cwd=root,
                check=True,
            )
            with self.assertRaises(self.validator.RoleAuditError) as raised:
                self.validator.build_observed(root)
            self.assertEqual(raised.exception.code, "ROLE-AUDIT-HELPER-ADMISSION")

    def test_unmanifested_ria_fixture_fails_production_build(self) -> None:
        for name in ("current-owner-copy.json", "policy-copy-2.json"):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                self.write_git_corpus(root)
                hostile_path = (
                    "tests/fixtures/reference-information-architecture/" + name
                )
                hostile = root / hostile_path
                hostile.write_text("{}\n", encoding="utf-8")
                readme = root / "tests/README.md"
                inventory = sorted(
                    [
                        *self.validator._readme_inventory(
                            readme.read_text(encoding="utf-8")
                        ),
                        hostile_path,
                    ]
                )
                readme.write_text(
                    "# tests\n\n## Structure\n\n```text\n"
                    + "\n".join(inventory)
                    + "\n```\n",
                    encoding="utf-8",
                )
                subprocess.run(
                    [
                        self.validator.GIT_EXECUTABLE,
                        "add",
                        "--",
                        hostile_path,
                        "tests/README.md",
                    ],
                    cwd=root,
                    check=True,
                )
                with self.assertRaises(self.validator.RoleAuditError) as raised:
                    self.validator.build_observed(root)
                self.assertEqual(
                    raised.exception.code, "ROLE-AUDIT-HELPER-ADMISSION"
                )

    def test_helper_tracker_promotion_fails(self) -> None:
        fixture = self.fixture()
        fixture["helperTests"]["executionTracker"] = True
        self.assert_audit_error(fixture, "ROLE-AUDIT-HELPER-TRACKER")

    def test_helper_readme_tracker_semantics_fail_on_production_parser(self) -> None:
        for text in (
            "---\ntype: sdlc/task\nstatus: active\n---\n# tests\n",
            "# tests\n\n## Task Table\n",
            "# tests\n\n## Task: ACER helper execution\n",
            "# tests\n\nTask status: In Progress\n",
            "# tests\n\n| Work item | Status |\n| --- | --- |\n| X | Done |\n",
        ):
            with self.subTest(text=text.splitlines()[0]):
                with self.assertRaises(self.validator.RoleAuditError) as raised:
                    self.validator._helper_entries(
                        ["tests/README.md"], lambda _path, value=text: value
                    )
                self.assertEqual(raised.exception.code, "ROLE-AUDIT-HELPER-TRACKER")

    def test_approved_post_closure_negative_strings_remain_fixture_data(
        self,
    ) -> None:
        paths = [
            "tests/README.md",
            "tests/fixtures/reference-information-architecture/minimal-valid.json",
            "tests/test_reference_information_architecture.py",
        ]
        readme = "# tests\n\n## Structure\n\n```text\n" + "\n".join(paths) + "\n```\n"
        reads: list[str] = []

        def read_text(path: str) -> str:
            reads.append(path)
            if path == "tests/README.md":
                return readme
            return "## Task Table\nRuntime status: PASS\n<!-- describe result -->\n"

        entries, counts, inventory = self.validator._helper_entries(paths, read_text)
        self.assertEqual(len(entries), 3)
        self.assertEqual(counts["total"], 3)
        self.assertEqual(inventory, paths)
        self.assertEqual(reads, paths)

    def test_missing_or_stale_readme_inventory_fails(self) -> None:
        fixture = self.fixture()
        fixture["readmeRemediation"]["finalInventory"].pop()
        self.assert_audit_error(fixture, "ROLE-AUDIT-README-REMEDIATION")

    def test_nonzero_and_unowned_findings_fail(self) -> None:
        for key, owner in (("roleOverlap", "platform"), ("unownedException", None)):
            with self.subTest(key=key):
                fixture = self.fixture()
                fixture["findings"][key].append(
                    {"path": "tests/fixture.py", "owner": owner}
                )
                self.assert_audit_error(fixture, "ROLE-AUDIT-FINDINGS")

    def test_malformed_and_duplicate_json_fail(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            target = root / self.validator.LEDGER_PATH
            target.parent.mkdir(parents=True)
            target.write_text('{"$schema": 1, "$schema": 2}\n', encoding="utf-8")
            with self.assertRaises(self.validator.RoleAuditError) as raised:
                self.validator.load_ledger(root, enforce_index=False)
            self.assertEqual(raised.exception.code, "ROLE-AUDIT-JSON-DUPLICATE")

    def test_unsafe_paths_are_value_free(self) -> None:
        for hostile in (
            "../outside",
            "/absolute",
            "_workspace/token",
            "tests/x\nFORGED",
        ):
            with self.subTest(hostile=repr(hostile)):
                fixture = self.fixture()
                fixture["helperTests"]["entries"][0]["path"] = hostile
                with self.assertRaises(self.validator.RoleAuditError) as raised:
                    self.validator.validate_ledger(fixture, self.observed)
                self.assertEqual(
                    str(raised.exception).splitlines(),
                    [f"ROLE-AUDIT-HELPER-PATH {self.validator.LEDGER_PATH}"],
                )
                self.assertNotIn(hostile, str(raised.exception))

    def test_git_query_allowlist_rejects_head_and_steering(self) -> None:
        for arguments in (
            ("ls-files", "HEAD", "--", "tests"),
            ("-c", "core.fsmonitor=true", "ls-files", "--", "tests"),
            (
                "ls-files",
                "-z",
                "--cached",
                "--others",
                "--exclude-standard",
                "--",
                "_workspace",
            ),
        ):
            with self.subTest(arguments=arguments):
                with self.assertRaises(self.validator.RoleAuditError) as raised:
                    self.validator._run_git(str(REPOSITORY_ROOT), arguments)
                self.assertEqual(raised.exception.code, "ROLE-AUDIT-GIT-QUERY")

    def test_git_runner_uses_closed_environment_and_no_head(self) -> None:
        completed = subprocess.CompletedProcess([], 0, b"", b"")
        with mock.patch.object(
            self.validator.subprocess, "run", return_value=completed
        ) as run:
            arguments = (
                "ls-files",
                "-z",
                "--cached",
                "--others",
                "--exclude-standard",
                "--",
                "tests",
            )
            self.validator._run_git(str(REPOSITORY_ROOT), arguments)
        kwargs = run.call_args.kwargs
        self.assertEqual(kwargs["env"], self.validator.CLOSED_GIT_ENVIRONMENT)
        self.assertIs(kwargs["shell"], False)
        self.assertNotIn("HEAD", run.call_args.args[0])

    def test_git_startup_and_timeout_fail_closed(self) -> None:
        arguments = (
            "ls-files",
            "-z",
            "--cached",
            "--others",
            "--exclude-standard",
            "--",
            "tests",
        )
        for effect, code in (
            (OSError("missing"), "ROLE-AUDIT-GIT-STARTUP"),
            (subprocess.TimeoutExpired(["git"], 10), "ROLE-AUDIT-GIT-TIMEOUT"),
        ):
            with self.subTest(code=code):
                with mock.patch.object(
                    self.validator.subprocess, "run", side_effect=effect
                ):
                    with self.assertRaises(self.validator.RoleAuditError) as raised:
                        self.validator._run_git(str(REPOSITORY_ROOT), arguments)
                self.assertEqual(raised.exception.code, code)

    def test_nondeterministic_ledger_order_fails(self) -> None:
        fixture = self.fixture()
        fixture["helperTests"]["entries"].reverse()
        self.assert_audit_error(fixture, "ROLE-AUDIT-HELPER-ORDER")

    def test_staged_worktree_divergence_fails_on_production_reader(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            target = root / "tests/README.md"
            target.parent.mkdir(parents=True)
            target.write_text("staged\n", encoding="utf-8")
            subprocess.run(
                [self.validator.GIT_EXECUTABLE, "init", "-q"], cwd=root, check=True
            )
            subprocess.run(
                [self.validator.GIT_EXECUTABLE, "add", "--", "tests/README.md"],
                cwd=root,
                check=True,
            )
            paths, index = self.validator.inventory_scope(str(root), "tests")
            self.assertEqual(paths, ["tests/README.md"])
            target.write_text("unstaged divergence\n", encoding="utf-8")
            with self.assertRaises(self.validator.RoleAuditError) as raised:
                self.validator._authoritative_text(
                    str(root), "tests/README.md", index, self.validator._run_git
                )
            self.assertEqual(raised.exception.code, "ROLE-AUDIT-WORKTREE-INDEX-DRIFT")

    def test_non_readme_helper_drift_fails_through_build_observed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            helper = self.write_git_corpus(root)
            helper.write_text("unstaged divergence\n", encoding="utf-8")
            with self.assertRaises(self.validator.RoleAuditError) as raised:
                self.validator.build_observed(root)
            self.assertEqual(raised.exception.code, "ROLE-AUDIT-WORKTREE-INDEX-DRIFT")
            self.assertEqual(
                raised.exception.path,
                "tests/test_reference_information_architecture.py",
            )

    def test_proposed_nonregular_helper_fails_through_build_observed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.write_git_corpus(root, proposed_symlink=True)
            with self.assertRaises(self.validator.RoleAuditError) as raised:
                self.validator.build_observed(root)
            self.assertEqual(raised.exception.code, "ROLE-AUDIT-INVENTORY-OBJECT")
            self.assertEqual(
                raised.exception.path,
                "tests/test_reference_information_architecture.py",
            )

    def test_entrypoint_verifier_rejects_validator_and_aggregate_drift(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            files = {
                self.validator.LEDGER_PATH: "{}\n",
                self.validator.SCRIPT_PATH: "#!/usr/bin/env python3\n",
                self.validator.AGGREGATE_PATH: (
                    'python3 "$ROOT_DIR/scripts/validate-active-corpus-role-audit.py" '
                    '--root "$ROOT_DIR" --self-test\n'
                    'python3 "$ROOT_DIR/scripts/validate-active-corpus-role-audit.py" '
                    '--root "$ROOT_DIR"\n'
                ),
            }
            for path, text in files.items():
                target = root / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(text, encoding="utf-8")
                if path == self.validator.AGGREGATE_PATH:
                    target.chmod(0o755)
            subprocess.run(
                [self.validator.GIT_EXECUTABLE, "init", "-q"], cwd=root, check=True
            )
            subprocess.run(
                [self.validator.GIT_EXECUTABLE, "add", "--", *files],
                cwd=root,
                check=True,
            )
            self.validator.verify_entrypoints(root)
            for path in (self.validator.SCRIPT_PATH, self.validator.AGGREGATE_PATH):
                with self.subTest(path=path):
                    target = root / path
                    target.write_text(files[path] + "# unstaged\n", encoding="utf-8")
                    with self.assertRaises(self.validator.RoleAuditError) as raised:
                        self.validator.verify_entrypoints(root)
                    self.assertEqual(
                        raised.exception.code, "ROLE-AUDIT-WORKTREE-INDEX-DRIFT"
                    )
                    target.write_text(files[path], encoding="utf-8")

    def test_descriptor_reader_rejects_symlink_and_nonregular(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            tests = root / "tests"
            tests.mkdir()
            link = tests / "link.py"
            link.symlink_to(root / "outside")
            with self.assertRaises(self.validator.RoleAuditError) as raised:
                self.validator._read_worktree_bytes(str(root), "tests/link.py")
            self.assertEqual(raised.exception.code, "ROLE-AUDIT-INVENTORY-OBJECT")

            fifo = tests / "fifo.py"
            os.mkfifo(fifo)
            with self.assertRaises(self.validator.RoleAuditError) as raised:
                self.validator._read_worktree_bytes(str(root), "tests/fifo.py")
            self.assertEqual(raised.exception.code, "ROLE-AUDIT-INVENTORY-OBJECT")

    def test_descriptor_reader_remains_bound_when_path_is_replaced(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            target = root / "tests/fixture.py"
            target.parent.mkdir(parents=True)
            target.write_bytes(b"trusted staged candidate\n")
            outside = root / "outside"
            outside.write_bytes(b"hostile replacement\n")
            moved = root / "tests/original.py"
            real_read = os.read
            replaced = False

            def replace_then_read(descriptor: int, length: int) -> bytes:
                nonlocal replaced
                if not replaced:
                    target.rename(moved)
                    target.symlink_to(outside)
                    replaced = True
                return real_read(descriptor, length)

            with mock.patch.object(
                self.validator.os, "read", side_effect=replace_then_read
            ):
                payload = self.validator._read_worktree_bytes(
                    str(root), "tests/fixture.py"
                )
            self.assertEqual(payload, b"trusted staged candidate\n")

    def test_self_test_matrix_is_closed(self) -> None:
        self.assertGreaterEqual(self.validator.run_self_test(), 20)

    def test_aggregate_invokes_both_validator_modes(self) -> None:
        text = AGGREGATE_PATH.read_text(encoding="utf-8")
        command = 'validate-active-corpus-role-audit.py" --root "$ROOT_DIR"'
        self.assertIn(command + " --self-test", text)
        self.assertIn(command + "\n", text)


if __name__ == "__main__":
    unittest.main()
