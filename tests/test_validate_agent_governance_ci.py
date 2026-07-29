#!/usr/bin/env python3
"""Focused regressions for the closed agent-governance CI contract."""

from __future__ import annotations

import copy
import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = REPO_ROOT / "scripts/validate-agent-governance-ci.py"
CONTRACT_PATH = (
    REPO_ROOT
    / "docs/00.agent-governance/contracts/agent-governance-ci.json"
)
SCHEMA_PATH = CONTRACT_PATH.with_name("agent-governance-ci.schema.json")
FIXTURE_PATH = REPO_ROOT / "tests/fixtures/agent-governance-ci.json"
WORKFLOW_PATH = REPO_ROOT / ".github/workflows/ci.yml"
AFFECTED_PATH = (
    REPO_ROOT
    / "docs/00.agent-governance/contracts/validation-surfaces.json"
)
AGGREGATE_PATH = REPO_ROOT / "scripts/validate-repo-quality-gates.sh"
PRE_COMMIT_PATH = REPO_ROOT / ".pre-commit-config.yaml"

SELF_TEST_COMMAND = (
    "python3 scripts/validate-agent-governance-ci.py --root . --self-test"
)
PRODUCTION_COMMAND = "python3 scripts/validate-agent-governance-ci.py --root ."
REQUIRED_ROUTE_CLASSES = {
    "root-config",
    "provider-gateways",
    "agent-shared",
    "agent-claude",
    "agent-codex",
    "agent-gemini",
    "github-automation",
    "governance-documents",
    "template-documents",
    "authored-documents",
    "scripts",
    "tests",
}
REQUIRED_INPUTS = (
    Path("docs/00.agent-governance/contracts/agent-governance-ci.json"),
    Path("docs/00.agent-governance/contracts/agent-governance-ci.schema.json"),
    Path("docs/00.agent-governance/contracts/validation-surfaces.json"),
    Path("tests/fixtures/agent-governance-ci.json"),
    Path(".github/workflows/ci.yml"),
    Path(".pre-commit-config.yaml"),
    Path("scripts/validate-repo-quality-gates.sh"),
)


def load_validator():
    spec = importlib.util.spec_from_file_location(
        "validate_agent_governance_ci",
        VALIDATOR_PATH,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load validator: {VALIDATOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class AgentGovernanceCiArtifactTests(unittest.TestCase):
    def test_core_artifacts_exist(self) -> None:
        missing = [
            path.relative_to(REPO_ROOT).as_posix()
            for path in (CONTRACT_PATH, SCHEMA_PATH, VALIDATOR_PATH, FIXTURE_PATH)
            if not path.is_file()
        ]
        self.assertEqual(missing, [])

    def test_workflow_invokes_self_test_before_production(self) -> None:
        text = WORKFLOW_PATH.read_text(encoding="utf-8")
        lines = [line.strip() for line in text.splitlines()]
        self.assertIn(SELF_TEST_COMMAND, lines)
        self.assertIn(PRODUCTION_COMMAND, lines)
        self.assertLess(lines.index(SELF_TEST_COMMAND), lines.index(PRODUCTION_COMMAND))

    def test_aggregate_invokes_self_test_before_production(self) -> None:
        text = AGGREGATE_PATH.read_text(encoding="utf-8")
        self.assertIn(
            'python3 "$ROOT_DIR/scripts/validate-agent-governance-ci.py" '
            '--root "$ROOT_DIR" --self-test',
            text,
        )
        self.assertIn(
            'python3 "$ROOT_DIR/scripts/validate-agent-governance-ci.py" '
            '--root "$ROOT_DIR"',
            text,
        )

    def test_pre_commit_registers_both_gate_modes(self) -> None:
        text = PRE_COMMIT_PATH.read_text(encoding="utf-8")
        entries = [
            line.strip().removeprefix("entry: ")
            for line in text.splitlines()
            if line.strip().startswith("entry: ")
        ]
        self.assertIn(SELF_TEST_COMMAND, entries)
        self.assertIn(PRODUCTION_COMMAND, entries)
        self.assertLess(entries.index(SELF_TEST_COMMAND), entries.index(PRODUCTION_COMMAND))

    def test_affected_contract_registers_required_validator(self) -> None:
        contract = json.loads(AFFECTED_PATH.read_text(encoding="utf-8"))
        registrations = {
            row["id"]: row for row in contract.get("validators", [])
        }
        self.assertIn("agent-governance-ci", registrations)
        self.assertEqual(
            registrations["agent-governance-ci"],
            {
                "id": "agent-governance-ci",
                "argv": [
                    "python3",
                    "scripts/validate-agent-governance-ci.py",
                    "--root",
                    ".",
                ],
                "lanes": ["affected", "staged", "all-files", "ci"],
                "optional": False,
                "fallback": {
                    "status": "FAIL",
                    "reason": "Agent-governance CI topology validation is required.",
                },
                "evidenceLane": "repo-static",
            },
        )

    def test_required_route_classes_select_gate(self) -> None:
        contract = json.loads(AFFECTED_PATH.read_text(encoding="utf-8"))
        surfaces = {row["id"]: row for row in contract.get("surfaces", [])}
        self.assertTrue(REQUIRED_ROUTE_CLASSES.issubset(surfaces))
        for surface_id in sorted(REQUIRED_ROUTE_CLASSES):
            with self.subTest(surface=surface_id):
                self.assertIn(
                    "agent-governance-ci",
                    surfaces[surface_id]["validators"],
                )
                self.assertIn(
                    "agent-governance-static",
                    surfaces[surface_id]["ciJobs"],
                )


@unittest.skipUnless(
    VALIDATOR_PATH.is_file() and CONTRACT_PATH.is_file() and SCHEMA_PATH.is_file(),
    "production contract is intentionally absent at the RED gate",
)
class AgentGovernanceCiValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_validator()
        cls.fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

    def make_valid_root(self) -> Path:
        directory = tempfile.TemporaryDirectory(prefix="agent-governance-ci-")
        self.addCleanup(directory.cleanup)
        root = Path(directory.name)
        for relative in REQUIRED_INPUTS:
            source = REPO_ROOT / relative
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
        return root

    def assert_rule(self, root: Path, rule_id: str) -> None:
        with self.assertRaises(self.validator.ContractError) as raised:
            self.validator.validate_repository(root)
        self.assertEqual(raised.exception.rule_id, rule_id)

    def test_repository_root_passes(self) -> None:
        counts = self.validator.validate_repository(REPO_ROOT)
        self.assertEqual(counts["routeClasses"], 12)
        self.assertEqual(counts["delegatedChecks"], 13)

    def test_truth_table_is_fail_closed(self) -> None:
        for case in self.fixture["truthTableCases"]:
            with self.subTest(case=case["name"]):
                self.assertEqual(
                    self.validator.classify_conditional(
                        case["selected"],
                        case["conclusion"],
                    ),
                    case["expected"],
                )
        root = self.make_valid_root()
        workflow = root / WORKFLOW_PATH.relative_to(REPO_ROOT)
        text = workflow.read_text(encoding="utf-8")
        workflow.write_text(
            text.replace(
                "              *)\n"
                "                verdict=\"FAIL\"\n",
                "              true:failure)\n"
                "                verdict=\"PASS\"\n"
                "                ;;\n"
                "              *)\n"
                "                verdict=\"FAIL\"\n",
                1,
            ),
            encoding="utf-8",
        )
        self.assert_rule(root, "AGQC-CI-TRUTH")

    def test_self_test_executes_closed_fixture(self) -> None:
        self.assertEqual(
            self.validator.run_self_test(REPO_ROOT),
            (6, 38),
        )

    def test_unknown_contract_key_is_rejected(self) -> None:
        contract = self.validator.load_json_document(
            CONTRACT_PATH,
            "AGQC-CI-JSON",
        )
        mutated = copy.deepcopy(contract)
        mutated["unexpected"] = True
        with self.assertRaises(self.validator.ContractError) as raised:
            self.validator.validate_contract_data(REPO_ROOT, mutated)
        self.assertEqual(raised.exception.rule_id, "AGQC-CI-SCHEMA")

    def test_vocabulary_drift_is_rejected(self) -> None:
        contract = self.validator.load_json_document(
            CONTRACT_PATH,
            "AGQC-CI-JSON",
        )
        mutated = copy.deepcopy(contract)
        mutated["resultVocabulary"] = ["PASS", "FAIL", "SKIP"]
        with self.assertRaises(self.validator.ContractError) as raised:
            self.validator.validate_contract_data(REPO_ROOT, mutated)
        self.assertEqual(raised.exception.rule_id, "AGQC-CI-VOCABULARY")

    def test_contract_input_must_not_be_a_symlink(self) -> None:
        root = self.make_valid_root()
        contract = root / CONTRACT_PATH.relative_to(REPO_ROOT)
        copy_path = contract.with_name("contract-copy.json")
        shutil.copyfile(contract, copy_path)
        contract.unlink()
        contract.symlink_to(copy_path)
        self.assert_rule(root, "AGQC-CI-INPUT")

    def test_schema_input_must_be_regular(self) -> None:
        root = self.make_valid_root()
        schema = root / SCHEMA_PATH.relative_to(REPO_ROOT)
        schema.unlink()
        schema.mkdir()
        self.assert_rule(root, "AGQC-CI-INPUT")

    def test_duplicate_json_key_is_rejected(self) -> None:
        root = self.make_valid_root()
        contract = root / CONTRACT_PATH.relative_to(REPO_ROOT)
        text = contract.read_text(encoding="utf-8")
        contract.write_text(
            text.replace(
                '"schemaVersion": 1,',
                '"schemaVersion": 1,\n  "schemaVersion": 1,',
                1,
            ),
            encoding="utf-8",
        )
        self.assert_rule(root, "AGQC-CI-JSON")

    def test_duplicate_yaml_key_is_rejected(self) -> None:
        root = self.make_valid_root()
        workflow = root / WORKFLOW_PATH.relative_to(REPO_ROOT)
        text = workflow.read_text(encoding="utf-8")
        workflow.write_text(
            text.replace("name: CI\n", "name: CI\nname: Duplicate\n", 1),
            encoding="utf-8",
        )
        self.assert_rule(root, "AGQC-CI-YAML")

    def test_provider_secret_is_rejected(self) -> None:
        root = self.make_valid_root()
        workflow = root / WORKFLOW_PATH.relative_to(REPO_ROOT)
        text = workflow.read_text(encoding="utf-8")
        workflow.write_text(
            text.replace(
                "  agent-governance-static:\n",
                "  agent-governance-static:\n"
                "    env:\n"
                "      PROVIDER_TOKEN: ${{ secrets.PROVIDER_TOKEN }}\n",
                1,
            ),
            encoding="utf-8",
        )
        self.assert_rule(root, "AGQC-CI-SECURITY")

    def test_id_token_permission_is_rejected(self) -> None:
        root = self.make_valid_root()
        workflow = root / WORKFLOW_PATH.relative_to(REPO_ROOT)
        text = workflow.read_text(encoding="utf-8")
        workflow.write_text(
            text.replace(
                "  agent-governance-static:\n",
                "  agent-governance-static:\n"
                "    permissions:\n"
                "      contents: read\n"
                "      id-token: write\n",
                1,
            ),
            encoding="utf-8",
        )
        self.assert_rule(root, "AGQC-CI-SECURITY")

    def test_provider_canary_command_is_rejected(self) -> None:
        root = self.make_valid_root()
        workflow = root / WORKFLOW_PATH.relative_to(REPO_ROOT)
        text = workflow.read_text(encoding="utf-8")
        workflow.write_text(
            text.replace(
                "          python3 scripts/validate-agent-harness-contract.py --root .\n",
                "          python3 scripts/validate-agent-provider-canaries.py --root .\n"
                "          python3 scripts/validate-agent-harness-contract.py --root .\n",
                1,
            ),
            encoding="utf-8",
        )
        self.assert_rule(root, "AGQC-CI-SECURITY")

    def test_inherited_secret_and_continue_on_error_are_rejected(self) -> None:
        cases = (
            (
                "workflow-secret",
                "name: CI\n",
                "name: CI\n"
                "env:\n"
                "  PROVIDER_TOKEN: ${{ secrets.PROVIDER_TOKEN }}\n",
                "AGQC-CI-SECURITY",
            ),
            (
                "agent-job-continue-on-error",
                "  agent-governance-static:\n"
                "    needs: changes\n",
                "  agent-governance-static:\n"
                "    continue-on-error: true\n"
                "    needs: changes\n",
                "AGQC-CI-SECURITY",
            ),
            (
                "validation-step-continue-on-error",
                "      - name: Run agent governance static checks\n"
                "        run: |\n",
                "      - name: Run agent governance static checks\n"
                "        continue-on-error: true\n"
                "        run: |\n",
                "AGQC-CI-SECURITY",
            ),
            (
                "summary-job-continue-on-error",
                "  ci-summary:\n"
                "    needs:\n",
                "  ci-summary:\n"
                "    continue-on-error: true\n"
                "    needs:\n",
                "AGQC-CI-TRUTH",
            ),
            (
                "summary-step-continue-on-error",
                "      - name: Summarize CI result\n"
                "        env:\n",
                "      - name: Summarize CI result\n"
                "        continue-on-error: true\n"
                "        env:\n",
                "AGQC-CI-TRUTH",
            ),
        )
        for name, old, new, expected_rule in cases:
            with self.subTest(case=name):
                root = self.make_valid_root()
                workflow = root / WORKFLOW_PATH.relative_to(REPO_ROOT)
                text = workflow.read_text(encoding="utf-8")
                mutated = text.replace(old, new, 1)
                self.assertNotEqual(mutated, text)
                workflow.write_text(mutated, encoding="utf-8")
                self.assert_rule(root, expected_rule)

    def test_validation_execution_controls_and_run_lines_are_closed(self) -> None:
        cases = (
            (
                "validation-step-if",
                "      - name: Run agent governance static checks\n"
                "        run: |\n",
                "      - name: Run agent governance static checks\n"
                "        if: false\n"
                "        run: |\n",
                "AGQC-CI-SECURITY",
            ),
            (
                "validation-step-shell",
                "      - name: Run agent governance static checks\n"
                "        run: |\n",
                "      - name: Run agent governance static checks\n"
                "        shell: bash {0}\n"
                "        run: |\n",
                "AGQC-CI-SECURITY",
            ),
            (
                "workflow-default-shell",
                "permissions:\n"
                "  contents: read\n",
                "permissions:\n"
                "  contents: read\n"
                "\n"
                "defaults:\n"
                "  run:\n"
                "    shell: bash {0}\n",
                "AGQC-CI-SECURITY",
            ),
            (
                "agent-job-default-shell",
                "  agent-governance-static:\n"
                "    needs: changes\n",
                "  agent-governance-static:\n"
                "    defaults:\n"
                "      run:\n"
                "        shell: bash {0}\n"
                "    needs: changes\n",
                "AGQC-CI-SECURITY",
            ),
            (
                "extra-run-command",
                "          python3 scripts/validate-agent-governance-ci.py --root .\n",
                "          python3 scripts/validate-agent-governance-ci.py --root .\n"
                "          touch .agent-governance-ci-bypass\n",
                "AGQC-CI-DELEGATION",
            ),
        )
        for name, old, new, expected_rule in cases:
            with self.subTest(case=name):
                root = self.make_valid_root()
                workflow = root / WORKFLOW_PATH.relative_to(REPO_ROOT)
                text = workflow.read_text(encoding="utf-8")
                mutated = text.replace(old, new, 1)
                self.assertNotEqual(mutated, text)
                workflow.write_text(mutated, encoding="utf-8")
                self.assert_rule(root, expected_rule)

    def test_summary_job_and_verdict_step_are_exact(self) -> None:
        cases = (
            (
                "summary-step-if",
                "      - name: Summarize CI result\n"
                "        env:\n",
                "      - name: Summarize CI result\n"
                "        if: false\n"
                "        env:\n",
                "AGQC-CI-TRUTH",
            ),
            (
                "summary-step-shell",
                "      - name: Summarize CI result\n"
                "        env:\n",
                "      - name: Summarize CI result\n"
                "        shell: bash {0}\n"
                "        env:\n",
                "AGQC-CI-TRUTH",
            ),
            (
                "summary-job-default-shell",
                "  ci-summary:\n"
                "    needs:\n",
                "  ci-summary:\n"
                "    defaults:\n"
                "      run:\n"
                "        shell: bash {0}\n"
                "    needs:\n",
                "AGQC-CI-TRUTH",
            ),
            (
                "summary-job-write-permissions",
                "  ci-summary:\n"
                "    needs:\n",
                "  ci-summary:\n"
                "    permissions:\n"
                "      contents: write\n"
                "    needs:\n",
                "AGQC-CI-SECURITY",
            ),
            (
                "summary-step-secret-env",
                "      - name: Summarize CI result\n"
                "        env:\n"
                "          EVENT_NAME: ${{ github.event_name }}\n",
                "      - name: Summarize CI result\n"
                "        env:\n"
                "          PROVIDER_TOKEN: ${{ secrets.PROVIDER_TOKEN }}\n"
                "          EVENT_NAME: ${{ github.event_name }}\n",
                "AGQC-CI-SECURITY",
            ),
            (
                "summary-run-bypass",
                "          set -euo pipefail\n"
                "          failed=0\n",
                "          set -euo pipefail\n"
                "          set +e\n"
                "          failed=0\n",
                "AGQC-CI-TRUTH",
            ),
        )
        for name, old, new, expected_rule in cases:
            with self.subTest(case=name):
                root = self.make_valid_root()
                workflow = root / WORKFLOW_PATH.relative_to(REPO_ROOT)
                text = workflow.read_text(encoding="utf-8")
                mutated = text.replace(old, new, 1)
                self.assertNotEqual(mutated, text)
                workflow.write_text(mutated, encoding="utf-8")
                self.assert_rule(root, expected_rule)

    def test_deferred_owners_remain_exact(self) -> None:
        contract = self.validator.load_json_document(
            CONTRACT_PATH,
            "AGQC-CI-JSON",
        )
        self.assertEqual(
            [row["owner"] for row in contract["deferredEvidence"]],
            ["AGQC-003", "AGQC-005", "Spec046"],
        )
        self.assertEqual(
            {row["result"] for row in contract["deferredEvidence"]},
            {"DEFER"},
        )


if __name__ == "__main__":
    unittest.main()
