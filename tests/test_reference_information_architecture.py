"""Focused contract and input-boundary tests for RIA-001."""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from io import StringIO
import importlib.util
from unittest import mock

from jsonschema import Draft202012Validator


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPOSITORY_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import reference_information_architecture as ria  # noqa: E402

from reference_information_architecture import (  # noqa: E402
    ContractError,
    RIA_RULE_IDS,
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


def _load_cli_module():
    specification = importlib.util.spec_from_file_location("ria_cli", CLI)
    assert specification is not None and specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


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

    @staticmethod
    def _asset() -> dict[str, object]:
        return {
            "id": "asset",
            "repositoryEvidence": ["docs/90.references/data/README.md"],
            "refreshTrigger": "contract changes",
            "sources": [
                {
                    "url": "https://example.invalid/source",
                    "checkedOn": "2026-07-22",
                    "adoptedScope": ["contract"],
                    "rejectedScope": ["runtime"],
                }
            ],
        }

    @staticmethod
    def _generated(asset_id: str, output_path: str) -> dict[str, object]:
        return {
            "id": asset_id,
            "generatorPath": "scripts/generate.py",
            "inputRoots": ["docs/90.references"],
            "outputPath": output_path,
            "checkCommand": "bash scripts/generate.py --check",
            "canonicalOwnerPath": "docs/90.references/README.md",
        }

    @staticmethod
    def _structural_exception() -> dict[str, object]:
        return {
            "canonicalOwnerPath": "docs/00.agent-governance/README.md",
            "referencePath": "docs/90.references/README.md",
            "paragraphSha256": "a" * 64,
            "structuralRole": "navigation",
            "reason": "bounded structural copy",
        }

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
            self._generated("first", "docs/90.references/data/first.md"),
            self._generated("second", "docs/90.references/data/first.md"),
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

    def test_every_path_family_uses_semantic_boundary_validation(self) -> None:
        mutations = []

        mutations.append(("registry", lambda contract: contract.update({"currentPackRegistry": "docs/../registry.json"})))
        mutations.append(("mutable", lambda contract: contract.update({"mutableIndexProjections": [{"path": "docs/../mutable.md"}]})))
        mutations.append(("navigation", lambda contract: contract.update({"mutableIndexProjections": [{"path": "docs/90.references/README.md", "navigationReplacement": {"visibleText": "Current", "destination": "docs/../target.md"}}]})))
        mutations.append(("evidence", lambda contract: contract.update({"dataAssets": [{**self._asset(), "repositoryEvidence": ["docs/../evidence.md"]}]})))
        mutations.append(("generator", lambda contract: contract.update({"generatedAssets": [{**self._generated("generated", "docs/90.references/data/output.md"), "generatorPath": "scripts/../generator.py"}]})))
        mutations.append(("inputs", lambda contract: contract.update({"generatedAssets": [{**self._generated("generated", "docs/90.references/data/output.md"), "inputRoots": ["docs/../inputs"]}]})))
        mutations.append(("output", lambda contract: contract.update({"generatedAssets": [self._generated("generated", "docs/../output.md")]})))
        mutations.append(("owner", lambda contract: contract.update({"generatedAssets": [{**self._generated("generated", "docs/90.references/data/output.md"), "canonicalOwnerPath": "docs/../owner.md"}]})))
        mutations.append(("roots", lambda contract: contract.update({"duplicateRules": {**contract["duplicateRules"], "canonicalOwnerRoots": ["docs/../owner"]}})))
        mutations.append(("exception-owner", lambda contract: contract.update({"duplicateRules": {**contract["duplicateRules"], "structuralExceptions": [{**self._structural_exception(), "canonicalOwnerPath": "docs/../owner.md"}]}})))
        mutations.append(("exception-reference", lambda contract: contract.update({"duplicateRules": {**contract["duplicateRules"], "structuralExceptions": [{**self._structural_exception(), "referencePath": "docs/../reference.md"}]}})))

        for name, mutate in mutations:
            with self.subTest(name=name):
                contract = self._minimal_contract()
                mutate(contract)
                self._write_contract(contract)
                with self.assertRaisesRegex(ContractError, "RIA-BOUNDARY"):
                    self._load()

    def test_registry_is_closed_exact_and_roles_are_disjoint(self) -> None:
        contract = self._minimal_contract()
        guard = contract["snapshotGuard"]
        assert isinstance(guard, dict)
        guard["currentPackIds"] = ["audits/2026-07-11-weia"]
        self._write_contract(contract)
        findings = validate_reference_architecture(self.root, self._load())
        self.assertEqual([finding.rule_id for finding in findings], ["RIA-CONTRACT"])

        for name, packs in (
            ("missing-id", [{}]),
            ("malformed", ["audits/2026-07-11-weia"]),
            ("duplicate", [{"id": "audits/2026-07-11-weia"}] * 2),
        ):
            with self.subTest(name=name):
                self._write_registry([])
                registry = self.root / "docs/99.templates/support/document-profiles.json"
                registry.write_text(json.dumps({"referenceCurrentPacks": {"packs": packs}}), encoding="utf-8")
                with self.assertRaisesRegex(ContractError, "RIA-CONTRACT"):
                    validate_reference_architecture(self.root, self._load())

        contract = self._minimal_contract()
        guard = contract["snapshotGuard"]
        assert isinstance(guard, dict)
        guard["historicalPackIds"] = ["audits/2026-07-11-weia"]
        guard["currentPackIds"] = ["audits/2026-07-11-weia"]
        self._write_contract(contract)
        with self.assertRaisesRegex(ContractError, "RIA-CONTRACT"):
            self._load()

    def test_rule_vocabulary_and_nonempty_scope_schema_are_closed(self) -> None:
        self.assertIsInstance(RIA_RULE_IDS, frozenset)
        self.assertEqual(
            RIA_RULE_IDS,
            frozenset({"RIA-CONTRACT", "RIA-BOUNDARY", "RIA-SNAPSHOT", "RIA-OVERLAY", "RIA-SOURCE", "RIA-GENERATOR", "RIA-DUPLICATE"}),
        )
        contract = self._minimal_contract()
        asset = self._asset()
        source = asset["sources"]
        assert isinstance(source, list) and isinstance(source[0], dict)
        source[0]["adoptedScope"] = []
        contract["dataAssets"] = [asset]
        self._write_contract(contract)
        with self.assertRaisesRegex(ContractError, "RIA-CONTRACT"):
            self._load()

        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        dot_segment_contract = self._minimal_contract()
        dot_segment_contract["currentPackRegistry"] = "docs/../registry.json"
        self.assertTrue(
            list(Draft202012Validator(schema).iter_errors(dot_segment_contract))
        )

    def test_special_file_replacement_after_lstat_fails_closed_without_blocking(self) -> None:
        registry = self.root / "docs/99.templates/support/document-profiles.json"
        original_open = os.open
        replaced = False

        def replace_before_open(path: object, flags: int, *args: object, **kwargs: object) -> int:
            nonlocal replaced
            if path == registry.name and not replaced:
                replaced = True
                required_flags = os.O_NOFOLLOW | os.O_NONBLOCK | os.O_CLOEXEC
                if flags & required_flags != required_flags:
                    raise AssertionError("FIFO open did not use all safe flags")
                registry.unlink()
                os.mkfifo(registry)
            return original_open(path, flags, *args, **kwargs)

        with mock.patch("reference_information_architecture.os.open", side_effect=replace_before_open):
            with self.assertRaisesRegex(ContractError, "RIA-BOUNDARY"):
                validate_reference_architecture(self.root, self._load())
        self.assertTrue(replaced)

    def test_self_test_uses_canonical_schema_and_full_contract_shape(self) -> None:
        self.assertFalse(hasattr(ria, "_SELF_TEST_SCHEMA"))
        self.assertEqual(
            ria._canonical_schema_bytes(),  # noqa: SLF001
            SCHEMA.read_bytes(),
        )
        ria.run_self_test()

    def test_cli_self_test_io_failure_is_payload_safe_exit_two(self) -> None:
        cli = _load_cli_module()
        captured = StringIO()
        with mock.patch.object(cli, "run_self_test", side_effect=OSError("secret-path/token")):
            with redirect_stderr(captured):
                self.assertEqual(cli._self_test(), 2)  # noqa: SLF001
        self.assertIn("RIA-CONTRACT", captured.getvalue())
        self.assertNotIn("secret-path", captured.getvalue())

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

    def test_cli_exit_contract_and_payload_safe_diagnostics(self) -> None:
        contract = self._minimal_contract()
        guard = contract["snapshotGuard"]
        assert isinstance(guard, dict)
        guard["currentPackIds"] = [
            "audits/2026-07-11-weia",
            "research/2026-07-07-wer",
        ]
        self._write_contract(contract)
        clean = subprocess.run([sys.executable, str(CLI), "--root", str(self.root)], capture_output=True, text=True, check=False)
        self.assertEqual(clean.returncode, 0, clean.stderr)

        guard["currentPackIds"] = ["research/not-registered"]
        self._write_contract(contract)
        findings = subprocess.run([sys.executable, str(CLI), "--root", str(self.root)], capture_output=True, text=True, check=False)
        self.assertEqual(findings.returncode, 1)
        self.assertIn("RIA-CONTRACT", findings.stdout)
        self.assertNotIn("not-registered", findings.stdout + findings.stderr)

        contract["currentPackRegistry"] = "/unsafe/secret-value"
        self._write_contract(contract)
        malformed = subprocess.run([sys.executable, str(CLI), "--root", str(self.root)], capture_output=True, text=True, check=False)
        self.assertEqual(malformed.returncode, 2)
        self.assertIn("RIA-BOUNDARY", malformed.stderr)
        self.assertNotIn("secret-value", malformed.stdout + malformed.stderr)


if __name__ == "__main__":
    unittest.main()
