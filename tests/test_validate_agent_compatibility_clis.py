from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_ROOT = REPOSITORY_ROOT / "scripts"
HELPER_PATH = SCRIPTS_ROOT / "agent_registry_compat.py"
CLI_CASES = {
    "admission": ("validate-agent-roster-admission.py", ("--root", ".")),
    "currentness": ("validate-agent-roster-currentness.py", (".",)),
    "model-fitness": ("validate-agent-model-fitness.py", ("--root", ".")),
    "evaluations": ("validate-agent-evaluations.py", ("--root", ".")),
    "closure": ("validate-agent-governance-closure.py", ("--root", ".")),
}


def load_helper():
    specification = importlib.util.spec_from_file_location(
        "agent_registry_compat_test_target", HELPER_PATH
    )
    if specification is None or specification.loader is None:
        raise AssertionError("compatibility helper could not be loaded")
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


class AgentRegistryCompatibilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # Compatibility calls load the terminal validator lazily throughout the
        # class, so keep its sibling import context until class cleanup.
        cls.enterClassContext(
            mock.patch.object(sys, "path", [str(SCRIPTS_ROOT), *sys.path])
        )
        cls.helper = load_helper()
        cls.terminal = cls.helper.load_terminal_validator()
        cls.registry = cls.terminal.load_json(
            REPOSITORY_ROOT, cls.terminal.REGISTRY_PATH
        )

    def test_all_compatibility_clis_delegate_to_the_registry(self) -> None:
        expected = self.terminal.validate_registry(REPOSITORY_ROOT)
        for mode in CLI_CASES:
            with self.subTest(mode=mode):
                self.assertEqual(self.helper.validate(REPOSITORY_ROOT, mode), expected)

    def test_each_compatibility_mode_has_one_bounded_fail_closed_mutation(self) -> None:
        for mode in CLI_CASES:
            with self.subTest(mode=mode):
                mutated = copy.deepcopy(self.registry)
                expected_code = self.helper._apply_bounded_mutation(mutated, mode)
                with self.assertRaises(self.terminal.HarnessError) as raised:
                    self.terminal.validate_registry(
                        REPOSITORY_ROOT, mutated, check_files=False
                    )
                self.assertEqual(raised.exception.code, expected_code)

    def test_production_and_self_test_cli_surfaces_pass(self) -> None:
        for mode, (script_name, root_args) in CLI_CASES.items():
            for self_test in (False, True):
                with self.subTest(mode=mode, self_test=self_test):
                    command = [sys.executable, str(SCRIPTS_ROOT / script_name)]
                    command.extend(root_args)
                    if self_test:
                        command.append("--self-test")
                    result = subprocess.run(
                        command,
                        cwd=REPOSITORY_ROOT,
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertIn("providers=2", result.stdout)
                    self.assertIn(f"roles={len(self.registry['roles'])}", result.stdout)

    def test_snapshot_contracts_and_finite_fixture_matrices_are_retired(self) -> None:
        retired = (
            "docs/00.agent-governance/contracts/agent-roster-admission.json",
            "docs/00.agent-governance/contracts/agent-roster-admission.schema.json",
            "docs/00.agent-governance/contracts/agent-model-fitness.json",
            "docs/00.agent-governance/contracts/agent-model-fitness.schema.json",
            "docs/00.agent-governance/contracts/agent-evaluations.json",
            "docs/00.agent-governance/contracts/agent-evaluations.schema.json",
            "tests/fixtures/agent-roster-admission.json",
            "tests/fixtures/agent-roster-currentness.json",
            "tests/fixtures/agent-model-fitness.json",
            "tests/fixtures/agent-evaluations.json",
        )
        self.assertEqual(
            [path for path in retired if (REPOSITORY_ROOT / path).exists()], []
        )

    def test_unknown_compatibility_mode_fails_closed(self) -> None:
        with self.assertRaises(self.helper.CompatibilityError) as raised:
            self.helper.validate(REPOSITORY_ROOT, "unknown")
        self.assertEqual(raised.exception.code, "AGENT-COMPAT-MODE")

    def test_every_public_mode_redacts_unexpected_input_errors(self) -> None:
        sentinel = "synthetic-private-key-do-not-disclose"
        registry = copy.deepcopy(self.registry)
        registry["roles"][0]["projections"][sentinel] = registry["roles"][0][
            "projections"
        ]["neutral"]
        self.assert_cli_input(registry, {}, "AGENT-COMPAT-VALIDATION", sentinel)

    def test_every_public_mode_preserves_typed_evidence_diagnostics(self) -> None:
        registry = copy.deepcopy(self.registry)
        registry["roles"][0]["responsibility"] = (
            "Authenticated provider execution was discovered and verified."
        )
        schema = self.terminal.load_json(
            REPOSITORY_ROOT, self.terminal.REGISTRY_SCHEMA_PATH
        )
        self.assert_cli_input(registry, schema, "AGENT-REGISTRY-EVIDENCE")

    def assert_cli_input(self, registry, schema, code, sentinel=None) -> None:
        with tempfile.TemporaryDirectory(prefix="compat-cli-input-") as directory:
            root = Path(directory)
            (root / ".agents/contracts").mkdir(parents=True)
            (root / ".agents/registry.json").write_text(json.dumps(registry))
            (root / ".agents/contracts/agent-registry.schema.json").write_text(
                json.dumps(schema)
            )
            for mode, (script_name, _) in CLI_CASES.items():
                root_args = (
                    [str(root)] if mode == "currentness" else ["--root", str(root)]
                )
                for arguments in ([], ["--self-test"]):
                    with self.subTest(mode=mode, arguments=arguments):
                        result = subprocess.run(
                            [
                                sys.executable,
                                "-B",
                                str(SCRIPTS_ROOT / script_name),
                                *root_args,
                                *arguments,
                            ],
                            capture_output=True,
                            text=True,
                            check=False,
                            timeout=30,
                        )
                        self.assertEqual(result.returncode, 1)
                        self.assertIn(code, result.stderr)
                        self.assertNotIn("Traceback", result.stdout + result.stderr)
                        if sentinel is not None:
                            self.assertNotIn(sentinel, result.stdout + result.stderr)
                            self.assertEqual(
                                result.stderr,
                                "ERR AGENT-COMPAT-VALIDATION invalid input\n",
                            )


if __name__ == "__main__":
    unittest.main()
