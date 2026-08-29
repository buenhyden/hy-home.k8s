"""Closure is a compatibility view of the terminal registry, not a snapshot."""

from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
import unittest
import tempfile
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/validate-agent-governance-closure.py"


class AgentGovernanceClosureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.enterClassContext(
            mock.patch.object(sys, "path", [str(SCRIPT.parent), *sys.path])
        )
        specification = importlib.util.spec_from_file_location(
            "closure_test_target", SCRIPT
        )
        cls.module = importlib.util.module_from_spec(specification)
        specification.loader.exec_module(cls.module)

    def test_closure_uses_the_public_registry_compatibility_owner(self):
        expected = self.module.compat.validate(ROOT, "closure")
        self.assertEqual(self.module.validate_repository(ROOT), expected)

    def test_both_existing_cli_modes_validate_the_registry(self):
        for arguments in ([], ["--self-test"]):
            with self.subTest(arguments=arguments):
                result = subprocess.run(
                    [
                        sys.executable,
                        "-B",
                        str(SCRIPT),
                        "--root",
                        str(ROOT),
                        *arguments,
                    ],
                    capture_output=True,
                    text=True,
                    check=False,
                    timeout=30,
                )
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn("providers=2", result.stdout)

    def test_closure_does_not_promote_runtime_claims(self):
        terminal = self.module.compat.load_terminal_validator()
        registry = copy.deepcopy(terminal.load_json(ROOT, terminal.REGISTRY_PATH))
        registry["roles"][0]["responsibility"] = (
            "Authenticated provider execution was discovered and verified."
        )
        with mock.patch.object(
            terminal, "load_json", wraps=terminal.load_json
        ) as loader:
            loader.side_effect = lambda root, path: (
                registry
                if path == terminal.REGISTRY_PATH
                else loader._mock_wraps(root, path)
            )
            with mock.patch.object(
                self.module.compat, "load_terminal_validator", return_value=terminal
            ):
                with self.assertRaises(terminal.HarnessError) as raised:
                    self.module.validate_repository(ROOT)
        self.assertEqual(raised.exception.code, "AGENT-REGISTRY-EVIDENCE")

    def test_both_cli_modes_redact_unexpected_input_errors(self):
        terminal = self.module.compat.load_terminal_validator()
        sentinel = "synthetic-private-key-do-not-disclose"
        registry = copy.deepcopy(terminal.load_json(ROOT, terminal.REGISTRY_PATH))
        registry["roles"][0]["projections"][sentinel] = registry["roles"][0][
            "projections"
        ]["neutral"]
        self.assert_cli_input(registry, {}, "AGENT-COMPAT-VALIDATION", sentinel)

    def test_both_cli_modes_preserve_typed_runtime_claim_diagnostics(self):
        terminal = self.module.compat.load_terminal_validator()
        registry = copy.deepcopy(terminal.load_json(ROOT, terminal.REGISTRY_PATH))
        registry["roles"][0]["responsibility"] = (
            "Authenticated provider execution was discovered and verified."
        )
        schema = terminal.load_json(ROOT, terminal.REGISTRY_SCHEMA_PATH)
        self.assert_cli_input(registry, schema, "AGENT-REGISTRY-EVIDENCE")

    def assert_cli_input(self, registry, schema, code, sentinel=None):
        with tempfile.TemporaryDirectory(prefix="closure-cli-input-") as directory:
            root = Path(directory)
            (root / ".agents/contracts").mkdir(parents=True)
            (root / ".agents/registry.json").write_text(json.dumps(registry))
            (root / ".agents/contracts/agent-registry.schema.json").write_text(
                json.dumps(schema)
            )
            for arguments in ([], ["--self-test"]):
                with self.subTest(arguments=arguments):
                    result = subprocess.run(
                        [
                            sys.executable,
                            "-B",
                            str(SCRIPT),
                            "--root",
                            str(root),
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
                            result.stderr, "ERR AGENT-COMPAT-VALIDATION invalid input\n"
                        )


if __name__ == "__main__":
    unittest.main()
