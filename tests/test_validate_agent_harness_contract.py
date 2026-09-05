"""Focused tests for the registry-backed harness compatibility command."""

from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
import types
from unittest import mock
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate-agent-governance.py"


def load_validator():
    specification = importlib.util.spec_from_file_location(
        "agent_harness_registry_test_target", SCRIPT
    )
    if specification is None or specification.loader is None:
        raise AssertionError("registry validator could not be loaded")
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    sys.path.insert(0, str(SCRIPT.parent))
    try:
        specification.loader.exec_module(module)
    finally:
        sys.path.pop(0)
    return module


class AgentHarnessRegistryContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_validator()

    def test_compatibility_command_validates_only_the_terminal_registry(self) -> None:
        counts = self.validator.validate_registry(ROOT)
        self.assertEqual(counts["providers"], 2)
        self.assertEqual(counts["projections"], counts["roles"] * 3)

        source = SCRIPT.read_text(encoding="utf-8")
        self.assertNotIn("harness-contract.json", source)
        self.assertNotIn("agent-model-fitness.json", source)
        self.assertNotIn("canonicalRoles", source)

    def test_retired_parallel_harness_authority_and_fixture_are_absent(self) -> None:
        retired = (
            "docs/00.agent-governance/contracts/harness-contract.json",
            "docs/00.agent-governance/contracts/harness-contract.schema.json",
            "tests/fixtures/agent-harness-contract.json",
        )
        self.assertEqual([path for path in retired if (ROOT / path).exists()], [])

    def test_root_cli_path_remains_green_without_a_production_self_test(self) -> None:
        # Full CLI also checks index/history parity, exercised in QA's finalized
        # Git snapshot. This test isolates CLI dispatch from that external owner.
        consumer = types.SimpleNamespace(validate_repository=mock.Mock())
        with mock.patch.dict(sys.modules, {"agent_governance_consumers": consumer}):
            self.assertEqual(self.validator.main(["--root", str(ROOT)]), 0)
        consumer.validate_repository.assert_called_once_with(ROOT)

        unsupported = subprocess.run(
            [sys.executable, str(SCRIPT), "--root", ".", "--self-test"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertNotEqual(unsupported.returncode, 0)

    def test_duplicate_json_keys_fail_closed(self) -> None:
        with self.assertRaises(self.validator.HarnessError) as raised:
            self.validator.decode_json_text('{"roles": [], "roles": []}')
        self.assertEqual(raised.exception.code, "AGENT-REGISTRY-INPUT")

    def test_normalized_json_paths_remain_readable(self) -> None:
        with tempfile.TemporaryDirectory(prefix="agent-registry-path-") as directory:
            root = Path(directory)
            (root / "inputs").mkdir()
            (root / "inputs" / "registry.json").write_text("{}", encoding="utf-8")
            for relative in (
                "inputs/registry.json",
                PurePosixPath("inputs/registry.json"),
            ):
                with self.subTest(relative=relative):
                    self.assertEqual(self.validator.load_json(root, relative), {})

    def test_non_normalized_json_paths_fail_with_a_registry_error(self) -> None:
        with tempfile.TemporaryDirectory(prefix="agent-registry-path-") as directory:
            root = Path(directory)
            (root / "inputs").mkdir()
            (root / "inputs" / "registry.json").write_text("{}", encoding="utf-8")
            for relative in (
                "inputs//registry.json",
                "inputs/./registry.json",
                "inputs/registry.json/",
                "inputs/../inputs/registry.json",
                "/inputs/registry.json",
                "",
                ".",
                "inputs/registry.json\x00",
            ):
                with self.subTest(relative=relative):
                    with self.assertRaises(self.validator.HarnessError) as raised:
                        self.validator.load_json(root, relative)
                    self.assertEqual(raised.exception.code, "AGENT-REGISTRY-INPUT")
                    self.assertEqual(
                        raised.exception.detail, "agent registry validation failed"
                    )

    def test_symlink_repository_root_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory(prefix="agent-registry-root-") as directory:
            link = Path(directory) / "repository-link"
            link.symlink_to(ROOT, target_is_directory=True)
            with self.assertRaises(self.validator.HarnessError) as raised:
                self.validator.validate_registry(link)
        self.assertEqual(raised.exception.code, "AGENT-REGISTRY-INPUT")

    def test_symlink_json_input_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory(prefix="agent-registry-input-") as directory:
            temporary_root = Path(directory)
            target = temporary_root / "target.json"
            target.write_text("{}", encoding="utf-8")
            (temporary_root / "registry.json").symlink_to(target)
            with self.assertRaises(self.validator.HarnessError) as raised:
                self.validator.load_json(
                    temporary_root,
                    PurePosixPath("registry.json"),
                )
        self.assertEqual(raised.exception.code, "AGENT-REGISTRY-INPUT")

    def test_oversized_json_input_fails_before_decode(self) -> None:
        with tempfile.TemporaryDirectory(prefix="agent-registry-size-") as directory:
            temporary_root = Path(directory)
            oversized = temporary_root / "registry.json"
            oversized.write_bytes(b" " * (self.validator.MAX_JSON_BYTES + 1))
            with self.assertRaises(self.validator.HarnessError) as raised:
                self.validator.load_json(
                    temporary_root,
                    PurePosixPath("registry.json"),
                )
        self.assertEqual(raised.exception.code, "AGENT-REGISTRY-INPUT")
        self.assertIn("exceeds", raised.exception.detail)

    def test_invalid_utf8_json_input_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory(prefix="agent-registry-utf8-") as directory:
            root = Path(directory)
            (root / "registry.json").write_bytes(b"{\xff}")
            with self.assertRaises(self.validator.HarnessError) as raised:
                self.validator.load_json(root, PurePosixPath("registry.json"))
        self.assertEqual(raised.exception.code, "AGENT-REGISTRY-INPUT")

    def test_final_directory_json_input_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="agent-registry-directory-"
        ) as directory:
            root = Path(directory)
            (root / "registry.json").mkdir()
            with self.assertRaises(self.validator.HarnessError) as raised:
                self.validator.load_json(root, PurePosixPath("registry.json"))
        self.assertEqual(raised.exception.code, "AGENT-REGISTRY-INPUT")

    def test_projection_symlink_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="agent-registry-projection-"
        ) as directory:
            temporary_root = Path(directory)
            projection_root = temporary_root / "agents"
            projection_root.mkdir()
            target = temporary_root / "target.md"
            target.write_text("# target\n", encoding="utf-8")
            (projection_root / "role.md").symlink_to(target)
            with self.assertRaises(self.validator.HarnessError) as raised:
                self.validator._projection_files(
                    temporary_root,
                    PurePosixPath("agents"),
                    ".md",
                )
        self.assertEqual(raised.exception.code, "AGENT-REGISTRY-PROJECTION")


if __name__ == "__main__":
    unittest.main()
