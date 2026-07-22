"""Focused contract and input-boundary tests for RIA-001."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPOSITORY_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from reference_information_architecture import (  # noqa: E402
    ContractError,
    load_contract,
    parse_git_sha1,
    validate_reference_architecture,
)


FIXTURE = (
    REPOSITORY_ROOT
    / "tests/fixtures/reference-information-architecture/minimal-valid.json"
)
SCHEMA = (
    REPOSITORY_ROOT
    / "docs/90.references/data/reference-information-architecture.schema.json"
)
CLI = REPOSITORY_ROOT / "scripts/validate-reference-information-architecture.py"


class ReferenceInformationArchitectureTests(unittest.TestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.contract_path = (
            self.root
            / "docs/90.references/data/reference-information-architecture.json"
        )
        self.contract_path.parent.mkdir(parents=True, exist_ok=True)
        self._write_contract(self._minimal_contract())
        self._write_registry(
            ["audits/2026-07-11-weia", "research/2026-07-07-wer"]
        )
        schema_path = self.contract_path.with_name(
            "reference-information-architecture.schema.json"
        )
        schema_path.write_bytes(SCHEMA.read_bytes())

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def _minimal_contract(self) -> dict[str, object]:
        return json.loads(FIXTURE.read_text(encoding="utf-8"))

    def _write_contract(self, contract: dict[str, object]) -> None:
        self.contract_path.write_text(
            json.dumps(contract, indent=2) + "\n", encoding="utf-8"
        )

    def _write_registry(self, pack_ids: list[str]) -> None:
        registry = self.root / "docs/99.templates/support/document-profiles.json"
        registry.parent.mkdir(parents=True, exist_ok=True)
        registry.write_text(
            json.dumps(
                {
                    "referenceCurrentPacks": {
                        "packs": [{"id": pack_id} for pack_id in pack_ids]
                    }
                }
            ),
            encoding="utf-8",
        )

    def _load(self) -> dict[str, object]:
        return load_contract(self.root, self.contract_path)

    def test_minimal_contract_loads_and_references_registered_current_packs(self) -> None:
        contract = self._minimal_contract()
        snapshot_guard = contract["snapshotGuard"]
        assert isinstance(snapshot_guard, dict)
        snapshot_guard["currentPackIds"] = [
            "audits/2026-07-11-weia",
            "research/2026-07-07-wer",
        ]
        self._write_contract(contract)

        findings = validate_reference_architecture(self.root, self._load())

        self.assertEqual(findings, [])

    def test_duplicate_json_key_is_a_contract_error(self) -> None:
        self.contract_path.write_text(
            '{"$schema":"./reference-information-architecture.schema.json",'
            '"schemaVersion":1,"schemaVersion":1}',
            encoding="utf-8",
        )

        with self.assertRaisesRegex(ContractError, "RIA-CONTRACT"):
            self._load()

    def test_unknown_top_level_key_and_schema_version_fail_closed(self) -> None:
        for mutation in (
            lambda contract: contract.update({"unknown": True}),
            lambda contract: contract.update({"schemaVersion": 2}),
        ):
            with self.subTest(mutation=mutation):
                contract = self._minimal_contract()
                mutation(contract)
                self._write_contract(contract)
                with self.assertRaisesRegex(ContractError, "RIA-CONTRACT"):
                    self._load()

    def test_contract_paths_require_allowlisted_clean_posix_segments(self) -> None:
        invalid_paths = (
            "/docs/99.templates/support/document-profiles.json",
            "docs/../document-profiles.json",
            "./docs/99.templates/support/document-profiles.json",
            "docs//99.templates/support/document-profiles.json",
            "_workspace/private.json",
        )
        for path in invalid_paths:
            with self.subTest(path=path):
                contract = self._minimal_contract()
                contract["currentPackRegistry"] = path
                self._write_contract(contract)
                with self.assertRaisesRegex(ContractError, "RIA-BOUNDARY"):
                    self._load()

    def test_duplicate_pack_ids_output_paths_and_mutable_paths_fail_closed(self) -> None:
        cases: list[tuple[str, dict[str, object]]] = []

        duplicate_pack = self._minimal_contract()
        guard = duplicate_pack["snapshotGuard"]
        assert isinstance(guard, dict)
        guard["currentPackIds"] = ["audits/2026-07-11-weia"] * 2
        cases.append(("pack", duplicate_pack))

        duplicate_output = self._minimal_contract()
        duplicate_output["generatedAssets"] = [
            {"id": "first", "outputPath": "docs/90.references/data/first.md"},
            {"id": "second", "outputPath": "docs/90.references/data/first.md"},
        ]
        cases.append(("output", duplicate_output))

        duplicate_mutable = self._minimal_contract()
        duplicate_mutable["mutableIndexProjections"] = [
            {"path": "docs/90.references/audits/README.md"},
            {"path": "docs/90.references/audits/README.md"},
        ]
        cases.append(("mutable", duplicate_mutable))

        for name, contract in cases:
            with self.subTest(name=name):
                self._write_contract(contract)
                with self.assertRaisesRegex(ContractError, "RIA-CONTRACT"):
                    self._load()

    def test_symlink_and_non_regular_contract_inputs_are_rejected(self) -> None:
        symlink = self.contract_path.with_name("contract-link.json")
        symlink.symlink_to(self.contract_path)
        with self.assertRaisesRegex(ContractError, "RIA-BOUNDARY"):
            load_contract(self.root, symlink)

        registry = self.root / "docs/99.templates/support/document-profiles.json"
        registry.unlink()
        registry.mkdir()
        with self.assertRaisesRegex(ContractError, "RIA-BOUNDARY"):
            validate_reference_architecture(self.root, self._load())

    def test_unknown_registry_pack_is_a_validation_finding(self) -> None:
        contract = self._minimal_contract()
        guard = contract["snapshotGuard"]
        assert isinstance(guard, dict)
        guard["currentPackIds"] = ["research/not-registered"]
        self._write_contract(contract)

        findings = validate_reference_architecture(self.root, self._load())

        self.assertEqual([finding.rule_id for finding in findings], ["RIA-CONTRACT"])
        self.assertIn("currentPackIds", findings[0].path)

    def test_snapshot_commit_parser_accepts_only_the_encoded_lowercase_sha1(self) -> None:
        accepted = "git-sha1:8fb9821497aaa93d9ed5fc1a69b60c628b047b47"
        rejected = (
            "8fb9821497aaa93d9ed5fc1a69b60c628b047b47",
            "git-sha1:",
            "git-sha1:git-sha1:8fb9821497aaa93d9ed5fc1a69b60c628b047b47",
            "git-sha1:8FB9821497AAA93D9ED5FC1A69B60C628B047B47",
            "git-sha1:zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz",
            "git-sha1:" + "a" * 64,
            accepted + " trailing",
            " " + accepted,
            accepted + " ",
        )

        self.assertEqual(parse_git_sha1(accepted), accepted.removeprefix("git-sha1:"))
        for value in rejected:
            with self.subTest(value=value):
                with self.assertRaisesRegex(ContractError, "RIA-SNAPSHOT"):
                    parse_git_sha1(value)

    def test_cli_self_test_and_production_skeleton(self) -> None:
        self_test = subprocess.run(
            [sys.executable, str(CLI), "--self-test"],
            cwd=REPOSITORY_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        production = subprocess.run(
            [sys.executable, str(CLI), "--root", str(REPOSITORY_ROOT)],
            cwd=REPOSITORY_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(self_test.returncode, 0, self_test.stderr)
        self.assertEqual(production.returncode, 0, production.stderr)


if __name__ == "__main__":
    unittest.main()
