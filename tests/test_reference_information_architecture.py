"""Focused immutable-snapshot, overlay, and lineage tests for RIA-002."""

from __future__ import annotations

import json
import hashlib
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
SNAPSHOT_MUTATION = (
    REPOSITORY_ROOT
    / "tests/fixtures/reference-information-architecture/snapshot-mutation.json"
)
OVERLAY_MUTATION = (
    REPOSITORY_ROOT
    / "tests/fixtures/reference-information-architecture/overlay-mutation.json"
)
ROOT_BASELINE = "git-sha1:15bba3d436ee2818f29d6f6880c7d5c4901aa0fe"
HISTORICAL_BASELINE = "git-sha1:8fb9821497aaa93d9ed5fc1a69b60c628b047b47"


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
        self._write_registry(["audits/2026-07-11-weia", "research/2026-07-07-wer"])
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
                        "profileId": "reference-current-pack",
                        "packs": [
                            {
                                "id": pack_id,
                                "members": [],
                                "allowedStates": ["active"],
                            }
                            for pack_id in pack_ids
                        ],
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

    @staticmethod
    def _transition(target: bytes = b"x") -> dict[str, object]:
        return {
            "id": "ria-007-postflight-ledger",
            "packId": "research/2026-07-07-wer",
            "fromCommit": ROOT_BASELINE,
            "subject": "document-migration-evidence-ledger",
            "targetSha256": hashlib.sha256(target).hexdigest(),
            "targetByteLength": len(target),
            "reason": "postflight evidence",
        }

    def _settled_contract(
        self, transition_commit: str = "git-sha1:" + "b" * 40, target: bytes = b"x"
    ) -> dict[str, object]:
        contract = self._minimal_contract()
        contract["currentPackBaselines"]["research/2026-07-07-wer"] = (
            transition_commit
        )
        contract["baselineTransitions"] = []
        contract["baselineSettlements"] = [
            {**self._transition(target), "transitionCommit": transition_commit}
        ]
        return contract

    def test_minimal_contract_loads_and_references_registered_current_packs(
        self,
    ) -> None:
        loaded = self._load()
        self.assertEqual(
            tuple(loaded["currentPackBaselines"]),
            ("audits/2026-07-11-weia", "research/2026-07-07-wer"),
        )
        self.assertEqual(
            loaded["snapshotGuard"]["historicalPackIds"],
            [
                "audits/2026-05-24-whga",
                "audits/2026-07-02-whia",
                "audits/2026-07-03-wdgh",
                "audits/2026-07-04-wdcn",
                "audits/2026-07-05-wea",
                "research/2026-07-04-wer",
            ],
        )

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
            lambda contract: contract.update({"schemaVersion": 1}),
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

    def test_repository_paths_reject_unsafe_bytes_before_git(self) -> None:
        hostile_paths = (
            "docs/line\nfeed.md",
            "docs/nul\0byte.md",
            "docs/control\x1fbyte.md",
            "docs/delete\x7fbyte.md",
            "docs/c1\x80byte.md",
            "docs/non-ascii-한글.md",
        )
        for hostile in hostile_paths:
            with self.subTest(path=repr(hostile)):
                with self.assertRaises(ContractError) as captured:
                    ria.parse_repository_path(hostile, field="contract.path")
                self.assertEqual(captured.exception.finding.path, "contract.path")
                self.assertNotIn(hostile, str(captured.exception))
                with mock.patch.object(ria.subprocess, "Popen") as popen:
                    with self.assertRaises(ContractError):
                        ria._run_git(  # noqa: SLF001
                            self.root,
                            ("ls-files", "-z", "--stage", "--", hostile),
                        )
                popen.assert_not_called()

                registry = {
                    "referenceCurrentPacks": {
                        "profileId": "reference-current-pack",
                        "packs": [
                            {
                                "id": "research/2026-07-07-wer",
                                "members": [hostile.removeprefix("docs/")],
                                "allowedStates": ["active"],
                            }
                        ],
                    }
                }
                with self.assertRaises(ContractError) as registry_error:
                    ria._registry_projection(registry)  # noqa: SLF001
                self.assertNotIn(hostile, str(registry_error.exception))

    def test_named_contract_uses_schema_from_the_same_commit(self) -> None:
        commit_oid = "c" * 40
        contract_oid = "1" * 40
        schema_oid = "2" * 40
        contract_payload = json.dumps(self._minimal_contract()).encode()
        rejecting_schema = json.dumps(
            {
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "not": {},
            }
        ).encode()

        def commit_runner(
            schema_payload: bytes,
            schema_mode: str = "100644",
            schema_size: int | None = None,
        ):
            payloads = {contract_oid: contract_payload, schema_oid: schema_payload}

            def runner(
                root: Path, arguments: tuple[str, ...], limit: int
            ) -> bytes:
                del root, limit
                if arguments == ("cat-file", "-t", commit_oid):
                    return b"commit\n"
                if arguments[:3] == ("ls-tree", "-z", "--full-tree"):
                    path = Path(arguments[5])
                    if path == ria.DEFAULT_CONTRACT_PATH:
                        oid, mode = contract_oid, "100644"
                    elif path == ria.CANONICAL_SCHEMA_PATH:
                        oid, mode = schema_oid, schema_mode
                    else:
                        raise AssertionError(path)
                    return f"{mode} blob {oid}\t{path.as_posix()}\0".encode()
                oid = arguments[2]
                if arguments[:2] == ("cat-file", "-t"):
                    return b"blob\n"
                if arguments[:2] == ("cat-file", "-s"):
                    if oid == schema_oid and schema_size is not None:
                        return f"{schema_size}\n".encode()
                    return f"{len(payloads[oid])}\n".encode()
                if arguments[:2] == ("cat-file", "blob"):
                    return payloads[oid]
                raise AssertionError(arguments)

            return runner

        self.assertEqual(
            ria.load_contract_at_commit(
                self.root,
                "git-sha1:" + commit_oid,
                runner=commit_runner(SCHEMA.read_bytes()),
            ),
            self._minimal_contract(),
        )
        cases = (
            (rejecting_schema, "100644", None),
            (b"{", "100644", None),
            (SCHEMA.read_bytes(), "120000", None),
            (SCHEMA.read_bytes(), "100644", ria.MAX_BLOB_BYTES + 1),
        )
        for schema_payload, schema_mode, schema_size in cases:
            with self.subTest(
                schema_mode=schema_mode,
                size=schema_size if schema_size is not None else len(schema_payload),
            ):
                with self.assertRaisesRegex(ContractError, "RIA-CONTRACT"):
                    ria.load_contract_at_commit(
                        self.root,
                        "git-sha1:" + commit_oid,
                        runner=commit_runner(
                            schema_payload, schema_mode, schema_size
                        ),
                    )

    def test_duplicate_pack_ids_output_paths_and_mutable_paths_fail_closed(
        self,
    ) -> None:
        cases: list[tuple[str, dict[str, object]]] = []

        duplicate_pack = self._minimal_contract()
        guard = duplicate_pack["snapshotGuard"]
        assert isinstance(guard, dict)
        historical = guard["historicalPackIds"]
        assert isinstance(historical, list)
        historical.append(historical[0])
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
            ria._read_regular_file(  # noqa: SLF001
                self.root,
                Path("docs/99.templates/support/document-profiles.json"),
                field="currentPackRegistry",
            )

    def test_unknown_registry_pack_is_a_validation_finding(self) -> None:
        contract = self._minimal_contract()
        contract["currentPackBaselines"] = {
            "audits/2026-07-11-weia": ROOT_BASELINE,
            "research/not-registered": ROOT_BASELINE,
        }
        self._write_contract(contract)
        loaded = self._load()
        state, finding = ria._fsm_state(loaded)  # noqa: SLF001
        self.assertIsNone(state)
        self.assertEqual(finding.rule_id, "RIA-TRANSITION")
        self.assertEqual(finding.path, "currentPackBaselines")

    def test_every_path_family_uses_semantic_boundary_validation(self) -> None:
        mutations = []

        mutations.append(
            (
                "registry",
                lambda contract: contract.update(
                    {"currentPackRegistry": "docs/../registry.json"}
                ),
            )
        )
        mutations.append(
            (
                "mutable",
                lambda contract: contract.update(
                    {"mutableIndexProjections": [{"path": "docs/../mutable.md"}]}
                ),
            )
        )
        mutations.append(
            (
                "navigation",
                lambda contract: contract.update(
                    {
                        "mutableIndexProjections": [
                            {
                                "path": "docs/90.references/README.md",
                                "navigationReplacement": {
                                    "visibleText": "Current",
                                    "destination": "docs/../target.md",
                                },
                            }
                        ]
                    }
                ),
            )
        )
        mutations.append(
            (
                "evidence",
                lambda contract: contract.update(
                    {
                        "dataAssets": [
                            {
                                **self._asset(),
                                "repositoryEvidence": ["docs/../evidence.md"],
                            }
                        ]
                    }
                ),
            )
        )
        mutations.append(
            (
                "generator",
                lambda contract: contract.update(
                    {
                        "generatedAssets": [
                            {
                                **self._generated(
                                    "generated", "docs/90.references/data/output.md"
                                ),
                                "generatorPath": "scripts/../generator.py",
                            }
                        ]
                    }
                ),
            )
        )
        mutations.append(
            (
                "inputs",
                lambda contract: contract.update(
                    {
                        "generatedAssets": [
                            {
                                **self._generated(
                                    "generated", "docs/90.references/data/output.md"
                                ),
                                "inputRoots": ["docs/../inputs"],
                            }
                        ]
                    }
                ),
            )
        )
        mutations.append(
            (
                "output",
                lambda contract: contract.update(
                    {
                        "generatedAssets": [
                            self._generated("generated", "docs/../output.md")
                        ]
                    }
                ),
            )
        )
        mutations.append(
            (
                "owner",
                lambda contract: contract.update(
                    {
                        "generatedAssets": [
                            {
                                **self._generated(
                                    "generated", "docs/90.references/data/output.md"
                                ),
                                "canonicalOwnerPath": "docs/../owner.md",
                            }
                        ]
                    }
                ),
            )
        )
        mutations.append(
            (
                "roots",
                lambda contract: contract.update(
                    {
                        "duplicateRules": {
                            **contract["duplicateRules"],
                            "canonicalOwnerRoots": ["docs/../owner"],
                        }
                    }
                ),
            )
        )
        mutations.append(
            (
                "exception-owner",
                lambda contract: contract.update(
                    {
                        "duplicateRules": {
                            **contract["duplicateRules"],
                            "structuralExceptions": [
                                {
                                    **self._structural_exception(),
                                    "canonicalOwnerPath": "docs/../owner.md",
                                }
                            ],
                        }
                    }
                ),
            )
        )
        mutations.append(
            (
                "exception-reference",
                lambda contract: contract.update(
                    {
                        "duplicateRules": {
                            **contract["duplicateRules"],
                            "structuralExceptions": [
                                {
                                    **self._structural_exception(),
                                    "referencePath": "docs/../reference.md",
                                }
                            ],
                        }
                    }
                ),
            )
        )

        for name, mutate in mutations:
            with self.subTest(name=name):
                contract = self._minimal_contract()
                mutate(contract)
                self._write_contract(contract)
                with self.assertRaisesRegex(ContractError, "RIA-BOUNDARY"):
                    self._load()

    def test_registry_is_closed_exact_and_roles_are_disjoint(self) -> None:
        for name, packs in (
            ("missing-id", [{}]),
            ("malformed", ["audits/2026-07-11-weia"]),
            (
                "duplicate",
                [
                    {
                        "id": "audits/2026-07-11-weia",
                        "members": [],
                        "allowedStates": ["active"],
                    }
                ]
                * 2,
            ),
        ):
            with self.subTest(name=name):
                with self.assertRaisesRegex(ContractError, "RIA-CONTRACT"):
                    ria._registry_projection(  # noqa: SLF001
                        {
                            "referenceCurrentPacks": {
                                "profileId": "reference-current-pack",
                                "packs": packs,
                            }
                        }
                    )

        contract = self._minimal_contract()
        guard = contract["snapshotGuard"]
        assert isinstance(guard, dict)
        guard["historicalPackIds"] = [
            "audits/2026-06-14-active-corpus-role-audit",
            "audits/2026-06-15-repository-structure-audit",
            "audits/2026-06-18-agentic-structure-audit",
            "research/2026-06-18-agentic-capabilities-research",
            "research/2026-06-19-agentic-documentation-research",
            "audits/2026-07-11-weia",
        ]
        self._write_contract(contract)
        with self.assertRaisesRegex(ContractError, "RIA-SNAPSHOT"):
            self._load()

    def test_rule_vocabulary_and_nonempty_scope_schema_are_closed(self) -> None:
        self.assertIsInstance(RIA_RULE_IDS, frozenset)
        self.assertEqual(
            RIA_RULE_IDS,
            frozenset(
                {
                    "RIA-CONTRACT",
                    "RIA-BOUNDARY",
                    "RIA-SNAPSHOT",
                    "RIA-OVERLAY",
                    "RIA-SOURCE",
                    "RIA-GENERATOR",
                    "RIA-DUPLICATE",
                    "RIA-TRANSITION",
                }
            ),
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

    def test_special_file_replacement_after_lstat_fails_closed_without_blocking(
        self,
    ) -> None:
        registry = self.root / "docs/99.templates/support/document-profiles.json"
        original_open = os.open
        replaced = False

        def replace_before_open(
            path: object, flags: int, *args: object, **kwargs: object
        ) -> int:
            nonlocal replaced
            if path == registry.name and not replaced:
                replaced = True
                required_flags = os.O_NOFOLLOW | os.O_NONBLOCK | os.O_CLOEXEC
                if flags & required_flags != required_flags:
                    raise AssertionError("FIFO open did not use all safe flags")
                registry.unlink()
                os.mkfifo(registry)
            return original_open(path, flags, *args, **kwargs)

        with mock.patch(
            "reference_information_architecture.os.open",
            side_effect=replace_before_open,
        ):
            with self.assertRaisesRegex(ContractError, "RIA-BOUNDARY"):
                ria._read_regular_file(  # noqa: SLF001
                    self.root,
                    Path("docs/99.templates/support/document-profiles.json"),
                    field="currentPackRegistry",
                )
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
        with mock.patch.object(
            cli, "run_self_test", side_effect=OSError("secret-path/token")
        ):
            with redirect_stderr(captured):
                self.assertEqual(cli._self_test(), 2)  # noqa: SLF001
        self.assertIn("RIA-CONTRACT", captured.getvalue())
        self.assertNotIn("secret-path", captured.getvalue())

    def test_snapshot_commit_parser_accepts_only_the_encoded_lowercase_sha1(
        self,
    ) -> None:
        accepted = "git-sha1:8fb9821497aaa93d9ed5fc1a69b60c628b047b47"
        bare_oid = accepted.removeprefix("git-sha1:")
        rejected = (
            bare_oid,
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
        self.assertNotEqual(bare_oid, accepted)
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
        non_git = subprocess.run(
            [sys.executable, str(CLI), "--root", str(self.root)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(non_git.returncode, 1)
        self.assertIn("RIA-BOUNDARY", non_git.stdout)

        cli = _load_cli_module()
        captured = StringIO()
        with mock.patch.object(cli, "load_contract", return_value=self._minimal_contract()), mock.patch.object(
            cli,
            "validate_reference_architecture",
            return_value=[ria.Finding("RIA-CONTRACT", "contract", "closed finding")],
        ), mock.patch("sys.stdout", captured):
            self.assertEqual(cli.main(["--root", str(self.root)]), 1)
        self.assertIn("RIA-CONTRACT", captured.getvalue())

        contract = self._minimal_contract()
        contract["currentPackRegistry"] = "/unsafe/secret-value"
        self._write_contract(contract)
        malformed = subprocess.run(
            [sys.executable, str(CLI), "--root", str(self.root)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(malformed.returncode, 2)
        self.assertIn("RIA-BOUNDARY", malformed.stderr)
        self.assertNotIn("secret-value", malformed.stdout + malformed.stderr)

    def test_schema_v2_exact_current_baseline_map(self) -> None:
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        self.assertEqual(schema["properties"]["schemaVersion"]["const"], 2)
        self.assertIn("currentPackBaselines", schema["required"])
        self.assertIn("baselineTransitions", schema["required"])
        self.assertIn("baselineSettlements", schema["required"])
        snapshot_properties = schema["properties"]["snapshotGuard"]["properties"]
        self.assertNotIn("currentPackIds", snapshot_properties)

        contract = self._minimal_contract()
        self._write_contract(contract)
        loaded = self._load()
        self.assertEqual(
            set(loaded["currentPackBaselines"]),
            {"audits/2026-07-11-weia", "research/2026-07-07-wer"},
        )

    def test_original_and_corrected_current_research_baselines(self) -> None:
        contract = json.loads(
            (
                REPOSITORY_ROOT
                / "docs/90.references/data/reference-information-architecture.json"
            ).read_text(encoding="utf-8")
        )
        stale = json.loads(json.dumps(contract))
        stale["currentPackBaselines"]["research/2026-07-07-wer"] = (
            HISTORICAL_BASELINE
        )
        stale_findings = ria.validate_overlay_guards(REPOSITORY_ROOT, stale)
        corrected = json.loads(json.dumps(contract))
        corrected_findings = ria.validate_overlay_guards(REPOSITORY_ROOT, corrected)
        self.assertTrue(
            any(
                finding.rule_id == "RIA-OVERLAY"
                and "document-migration-evidence-ledger.md" in finding.path
                for finding in stale_findings
            )
        )
        self.assertEqual(corrected_findings, [])

    def test_snapshot_mutation_fixture_requires_immutable_body_guard(self) -> None:
        mutation = json.loads(SNAPSHOT_MUTATION.read_text(encoding="utf-8"))
        self.assertEqual(mutation["expectedRule"], "RIA-SNAPSHOT")
        cases = (
            (
                Path(mutation["path"]),
                mutation["replacement"].encode("utf-8"),
            ),
            (
                Path("docs/90.references/audits/2026-05-24-whga/README.md"),
                b"historical README mutation\n",
            ),
        )
        for target, replacement in cases:
            with self.subTest(target=target):

                def proposed(
                    root: Path,
                    path: Path,
                    proposed_oid: str | None,
                    runner: ria.GitRunner | None,
                ) -> bytes:
                    if path == target:
                        return replacement
                    return ria._read_commit_path(  # noqa: SLF001
                        root,
                        HISTORICAL_BASELINE.removeprefix("git-sha1:"),
                        path,
                        runner,
                    )

                with mock.patch.object(ria, "_proposed_path", side_effect=proposed):
                    findings = ria.validate_snapshot_guards(
                        REPOSITORY_ROOT, self._minimal_contract()
                    )
                self.assertEqual(
                    [
                        finding
                        for finding in findings
                        if finding.path == target.as_posix()
                    ],
                    [
                        ria.Finding(
                            "RIA-SNAPSHOT",
                            target.as_posix(),
                            "protected snapshot bytes differ",
                        )
                    ],
                )

    def test_current_overlay_fixture_requires_projection_bounds(self) -> None:
        mutation = json.loads(OVERLAY_MUTATION.read_text(encoding="utf-8"))
        self.assertEqual(mutation["expectedRule"], "RIA-OVERLAY")
        target = Path(mutation["path"])
        replacement = mutation["replacement"].encode("utf-8")
        contract = json.loads(
            (
                REPOSITORY_ROOT
                / "docs/90.references/data/reference-information-architecture.json"
            ).read_text(encoding="utf-8")
        )

        def proposed(
            root: Path,
            path: Path,
            proposed_oid: str | None,
            runner: ria.GitRunner | None,
        ) -> bytes:
            if path == target:
                return replacement
            pack_id = (
                "audits/2026-07-11-weia"
                if path.parts[2] == "audits"
                else "research/2026-07-07-wer"
            )
            oid = contract["currentPackBaselines"][pack_id].removeprefix(
                "git-sha1:"
            )
            return ria._read_commit_path(root, oid, path, runner)  # noqa: SLF001

        with mock.patch.object(ria, "_proposed_path", side_effect=proposed):
            findings = ria.validate_overlay_guards(REPOSITORY_ROOT, contract)
        self.assertTrue(
            any(
                finding.rule_id == "RIA-OVERLAY"
                and finding.path == target.as_posix()
                for finding in findings
            )
        )

        projection = {
            "path": "docs/90.references/audits/README.md",
            "table": {
                "section": "Audit Pack Registry",
                "columns": ["Pack role"],
            },
        }
        baseline = b"## Audit Pack Registry\n\n| Pack | Pack role | Scope |\n| --- | --- | --- |\n| one | Current | exact |\n"
        allowed = baseline.replace(b" Current ", b" Historical ")
        protected = baseline.replace(b" exact ", b"  exact ")
        self.assertEqual(
            ria._projection_mask(  # noqa: SLF001
                baseline, Path(projection["path"]), projection
            ),
            ria._projection_mask(  # noqa: SLF001
                allowed, Path(projection["path"]), projection
            ),
        )
        self.assertNotEqual(
            ria._projection_mask(  # noqa: SLF001
                baseline, Path(projection["path"]), projection
            ),
            ria._projection_mask(  # noqa: SLF001
                protected, Path(projection["path"]), projection
            ),
        )
        wrong_section = baseline.replace(
            b"\n\n| Pack", b"\n\n## Other Section\n\n| Pack"
        )
        with self.assertRaises(ria._GitError):  # noqa: SLF001
            ria._projection_mask(  # noqa: SLF001
                wrong_section, Path(projection["path"]), projection
            )

    def test_complete_body_projection_preserves_frontmatter(self) -> None:
        projection = {
            "path": "docs/90.references/audits/2026-07-11-weia/README.md",
            "completeBody": True,
        }
        path = Path(projection["path"])
        baseline = b"---\ntitle: Audit\nstatus: done\n---\n# Baseline body\n"
        body_change = b"---\ntitle: Audit\nstatus: done\n---\n# Rewritten body\n"
        metadata_change = b"---\ntitle: Audit\nstatus: active\n---\n# Baseline body\n"
        self.assertEqual(
            ria._projection_mask(baseline, path, projection),  # noqa: SLF001
            ria._projection_mask(body_change, path, projection),  # noqa: SLF001
        )
        self.assertNotEqual(
            ria._projection_mask(baseline, path, projection),  # noqa: SLF001
            ria._projection_mask(metadata_change, path, projection),  # noqa: SLF001
        )
        for malformed in (
            b"# Missing frontmatter\n",
            b"---\ntitle: Missing closing delimiter\n",
            b"--- \ntitle: Malformed opening delimiter\n---\nbody\n",
        ):
            with self.subTest(payload=malformed):
                with self.assertRaises(ria._GitError):  # noqa: SLF001
                    ria._projection_mask(malformed, path, projection)  # noqa: SLF001

    def test_open_transition_matrix_is_closed(self) -> None:
        contract = self._minimal_contract()
        contract["baselineTransitions"] = [self._transition()]
        target_path = Path(
            "docs/90.references/research/2026-07-07-wer/"
            "document-migration-evidence-ledger.md"
        )
        research = ria.Pack(
            "research/2026-07-07-wer",
            ("active",),
            ("document-migration-evidence-ledger.md",),
        )
        context = ria.ValidationContext(
            ria.RegistryProjection("content/reference", (research,)),
            {target_path: b"x", research.readme_path: b"readme"},
            {},
            {
                (ROOT_BASELINE, target_path): b"root target",
                (ROOT_BASELINE, research.readme_path): b"readme",
            },
            {},
            None,
        )
        with mock.patch.object(ria, "_build_context", return_value=context):
            self.assertEqual(
                ria.validate_baseline_transitions(self.root, contract), []
            )
        wrong_bytes = ria.ValidationContext(
            context.proposed_registry,
            {target_path: b"wrong"},
            {},
            {},
            {},
            None,
        )
        with mock.patch.object(ria, "_build_context", return_value=wrong_bytes):
            self.assertEqual(
                [
                    finding.rule_id
                    for finding in ria.validate_baseline_transitions(
                        self.root, contract
                    )
                ],
                ["RIA-TRANSITION"],
            )
        no_op = ria.ValidationContext(
            context.proposed_registry,
            context.proposed_bytes,
            context.baseline_registries,
            {**context.baseline_bytes, (ROOT_BASELINE, target_path): b"x"},
            context.baseline_oids,
            context.proposed_commit_oid,
        )
        with mock.patch.object(ria, "_build_context", return_value=no_op):
            self.assertEqual(
                [
                    finding.rule_id
                    for finding in ria.validate_baseline_transitions(
                        self.root, contract
                    )
                ],
                ["RIA-TRANSITION"],
            )
            self.assertEqual(
                [
                    finding.rule_id
                    for finding in ria.validate_overlay_guards(self.root, contract)
                ],
                ["RIA-OVERLAY"],
            )
        nonmember = ria.ValidationContext(
            ria.RegistryProjection(
                "content/reference",
                (ria.Pack("research/2026-07-07-wer", ("active",), ()),),
            ),
            {},
            {},
            {},
            {},
            None,
        )
        with mock.patch.object(ria, "_build_context", return_value=nonmember):
            self.assertEqual(
                [
                    finding.rule_id
                    for finding in ria.validate_baseline_transitions(
                        self.root, contract
                    )
                ],
                ["RIA-TRANSITION"],
            )
        with mock.patch.object(
            ria, "_build_context", side_effect=ria._GitError("registry drift")
        ):
            self.assertEqual(
                [
                    finding.rule_id
                    for finding in ria.validate_baseline_transitions(
                        self.root, contract
                    )
                ],
                ["RIA-TRANSITION"],
            )
        findings = ria.validate_baseline_transitions(
            self.root,
            contract,
            require_settled_baselines=True,
        )
        self.assertEqual([finding.rule_id for finding in findings], ["RIA-TRANSITION"])

    def test_direct_baseline_jump_is_rejected(self) -> None:
        contract = self._minimal_contract()
        contract["currentPackBaselines"]["research/2026-07-07-wer"] = (
            "git-sha1:" + "c" * 40
        )
        findings = ria.validate_baseline_transitions(self.root, contract)
        self.assertEqual([finding.rule_id for finding in findings], ["RIA-TRANSITION"])

    def test_settlement_proof_chain_requires_explicit_lineage(self) -> None:
        c2 = "b" * 40
        target = b"settled target"
        contract = self._settled_contract("git-sha1:" + c2, target)
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        self.assertEqual(
            list(Draft202012Validator(schema).iter_errors(contract)), []
        )

        audit = ria.Pack("audits/2026-07-11-weia", ("done",), ())
        research = ria.Pack(
            "research/2026-07-07-wer",
            ("active", "accepted"),
            ("document-migration-evidence-ledger.md",),
        )
        registry = ria.RegistryProjection("content/reference", (audit, research))
        transition_path = research.member_paths[0]
        non_targets = (audit.readme_path, research.readme_path)
        baseline_bytes = {
            (ROOT_BASELINE, path): f"root:{path}".encode() for path in non_targets
        }
        context = ria.ValidationContext(
            registry,
            {transition_path: target},
            {ROOT_BASELINE: registry, "git-sha1:" + c2: registry},
            {},
            {ROOT_BASELINE: ROOT_BASELINE.removeprefix("git-sha1:"), "git-sha1:" + c2: c2},
            None,
        )

        open_contract = self._minimal_contract()
        open_contract["baselineTransitions"] = [self._transition(target)]
        registry_payload = json.dumps(
            {
                "referenceCurrentPacks": {
                    "profileId": registry.profile_id,
                    "packs": [
                        {
                            "id": pack.pack_id,
                            "allowedStates": list(pack.allowed_states),
                            "members": list(pack.members),
                        }
                        for pack in registry.packs
                    ],
                }
            },
            separators=(",", ":"),
        ).encode()
        payloads = {
            ria.DEFAULT_CONTRACT_PATH: json.dumps(
                open_contract, separators=(",", ":")
            ).encode(),
            ria.CANONICAL_SCHEMA_PATH: SCHEMA.read_bytes(),
            ria.REGISTRY_PATH: registry_payload,
            transition_path: target,
            **{path: baseline_bytes[(ROOT_BASELINE, path)] for path in non_targets},
        }
        root_payloads = {**payloads, transition_path: b"immutable root target"}

        def proof_runner(current_payloads: dict[Path, bytes]):
            by_oid: dict[str, bytes] = {}
            by_commit_path: dict[tuple[str, Path], str] = {}
            trees = (
                (c2, current_payloads),
                (ROOT_BASELINE.removeprefix("git-sha1:"), root_payloads),
            )
            index = 0
            for commit_oid, tree_payloads in trees:
                for path, payload in tree_payloads.items():
                    index += 1
                    oid = f"{index:040x}"
                    by_commit_path[(commit_oid, path)] = oid
                    by_oid[oid] = payload

            def runner(
                root: Path, arguments: tuple[str, ...], limit: int
            ) -> bytes:
                del root, limit
                if arguments in {
                    ("cat-file", "-t", c2),
                    (
                        "cat-file",
                        "-t",
                        ROOT_BASELINE.removeprefix("git-sha1:"),
                    ),
                }:
                    return b"commit\n"
                if arguments[:3] == ("ls-tree", "-z", "--full-tree"):
                    commit_oid = arguments[3]
                    path = Path(arguments[5])
                    oid = by_commit_path[(commit_oid, path)]
                    return f"100644 blob {oid}\t{path.as_posix()}\0".encode()
                oid = arguments[2]
                if arguments[:2] == ("cat-file", "-t"):
                    return b"blob\n"
                if arguments[:2] == ("cat-file", "-s"):
                    return f"{len(by_oid[oid])}\n".encode()
                if arguments[:2] == ("cat-file", "blob"):
                    return by_oid[oid]
                raise AssertionError(arguments)

            return runner

        self.assertEqual(
            ria._settlement_proof(  # noqa: SLF001
                self.root, contract, context, proof_runner(dict(payloads))
            ),
            [],
        )
        no_op_root = root_payloads[transition_path]
        no_op_contract = self._settled_contract("git-sha1:" + c2, no_op_root)
        no_op_payloads = dict(payloads)
        no_op_open = self._minimal_contract()
        no_op_open["baselineTransitions"] = [self._transition(no_op_root)]
        no_op_payloads[ria.DEFAULT_CONTRACT_PATH] = json.dumps(
            no_op_open, separators=(",", ":")
        ).encode()
        no_op_payloads[transition_path] = no_op_root
        no_op_context = ria.ValidationContext(
            registry,
            {transition_path: no_op_root},
            context.baseline_registries,
            context.baseline_bytes,
            context.baseline_oids,
            None,
        )
        self.assertEqual(
            [
                finding.rule_id
                for finding in ria._settlement_proof(  # noqa: SLF001
                    self.root,
                    no_op_contract,
                    no_op_context,
                    proof_runner(no_op_payloads),
                )
            ],
            ["RIA-TRANSITION"],
        )
        changed_contract = json.loads(json.dumps(contract))
        changed_contract["evidenceCutoff"] = "2026-07-23"
        self.assertEqual(
            [
                finding.rule_id
                for finding in ria._settlement_proof(  # noqa: SLF001
                    self.root,
                    changed_contract,
                    context,
                    proof_runner(dict(payloads)),
                )
            ],
            ["RIA-TRANSITION"],
        )
        mutations = []
        mismatched_contract = dict(payloads)
        bad_open = json.loads(json.dumps(open_contract))
        bad_open["baselineTransitions"][0]["reason"] = "different"
        mismatched_contract[ria.DEFAULT_CONTRACT_PATH] = json.dumps(bad_open).encode()
        mutations.append(mismatched_contract)
        mismatched_target = dict(payloads)
        mismatched_target[transition_path] = b"different target"
        mutations.append(mismatched_target)
        mismatched_non_target = dict(payloads)
        mismatched_non_target[non_targets[0]] = b"different non-target"
        mutations.append(mismatched_non_target)
        for current_payloads in mutations:
            with self.subTest(paths=tuple(current_payloads)):
                findings = ria._settlement_proof(  # noqa: SLF001
                    self.root,
                    contract,
                    context,
                    proof_runner(current_payloads),
                )
                self.assertEqual(
                    [finding.rule_id for finding in findings], ["RIA-TRANSITION"]
                )

    def test_fixed_git_runner_contract_is_closed(self) -> None:
        self.assertEqual(ria.GIT_EXECUTABLE, "/usr/bin/git")
        self.assertEqual(ria.GIT_TIMEOUT_SECONDS, 10)
        self.assertEqual(ria.MAX_BLOB_BYTES, 2_000_000)
        self.assertNotIn("GIT_DIR", ria.CLOSED_GIT_ENVIRONMENT)
        self.assertEqual(ria.CLOSED_GIT_ENVIRONMENT["GIT_NO_LAZY_FETCH"], "1")
        self.assertTrue(
            ria._git_arguments_allowed(  # noqa: SLF001
                (
                    "diff-tree",
                    "--no-commit-id",
                    "--name-status",
                    "-z",
                    "--no-renames",
                    "b" * 40,
                    "c" * 40,
                    "--",
                )
            )
        )
        self.assertFalse(
            ria._git_arguments_allowed(  # noqa: SLF001
                (
                    "diff-tree",
                    "--name-status",
                    "-z",
                    "--no-renames",
                    "b" * 40,
                    "c" * 40,
                    "--",
                )
            )
        )
        with self.assertRaises(ContractError):
            ria._run_git(REPOSITORY_ROOT, ("show", "HEAD"))  # noqa: SLF001

    def test_fixed_git_runner_hostile_process_matrix(self) -> None:
        hostile_environment = {"GIT_DIR": "/secret", "GIT_CONFIG_COUNT": "1"}
        with mock.patch.dict(os.environ, hostile_environment), mock.patch.object(
            ria.subprocess, "Popen", side_effect=OSError("missing")
        ) as popen:
            with self.assertRaisesRegex(ria._GitError, "unavailable"):  # noqa: SLF001
                ria._run_git(  # noqa: SLF001
                    self.root, ("rev-parse", "--verify", "HEAD")
                )
        kwargs = popen.call_args.kwargs
        self.assertEqual(kwargs["env"], ria.CLOSED_GIT_ENVIRONMENT)
        self.assertFalse(kwargs["shell"])
        self.assertNotIn("GIT_DIR", kwargs["env"])

        with self.assertRaisesRegex(ria._GitError, "failed"):  # noqa: SLF001
            ria._run_git(  # noqa: SLF001
                self.root, ("rev-parse", "--verify", "HEAD")
            )
        with mock.patch.object(ria, "GIT_TIMEOUT_SECONDS", 0):
            with self.assertRaisesRegex(ria._GitError, "timed out"):  # noqa: SLF001
                ria._run_git(  # noqa: SLF001
                    REPOSITORY_ROOT,
                    (
                        "cat-file",
                        "commit",
                        ROOT_BASELINE.removeprefix("git-sha1:"),
                    ),
                )
        with self.assertRaisesRegex(ria._GitError, "exceeded"):  # noqa: SLF001
            ria._run_git(  # noqa: SLF001
                REPOSITORY_ROOT,
                (
                    "cat-file",
                    "commit",
                    ROOT_BASELINE.removeprefix("git-sha1:"),
                ),
                stdout_limit=1,
            )
        with mock.patch.object(ria, "MAX_STDERR_BYTES", 0):
            with self.assertRaisesRegex(ria._GitError, "exceeded"):  # noqa: SLF001
                ria._run_git(  # noqa: SLF001
                    self.root, ("rev-parse", "--verify", "HEAD")
                )

    def test_fixed_git_runner_retries_nonblocking_reads_and_reaps_on_oserror(
        self,
    ) -> None:
        stdout = mock.Mock()
        stdout.fileno.return_value = 10
        stderr = mock.Mock()
        stderr.fileno.return_value = 11
        process = mock.Mock(stdout=stdout, stderr=stderr)
        process.wait.return_value = 0
        stdout_key = mock.Mock(data="stdout", fileobj=stdout)
        stderr_key = mock.Mock(data="stderr", fileobj=stderr)
        selector = mock.Mock()
        selector.get_map.side_effect = ({1: stdout}, {1: stdout}, {2: stderr}, {})
        selector.select.side_effect = (
            [(stdout_key, ria.selectors.EVENT_READ)],
            [(stdout_key, ria.selectors.EVENT_READ)],
            [(stderr_key, ria.selectors.EVENT_READ)],
        )
        with mock.patch.object(ria.subprocess, "Popen", return_value=process), mock.patch.object(
            ria.selectors, "DefaultSelector", return_value=selector
        ), mock.patch.object(ria.os, "set_blocking"), mock.patch.object(
            ria.os, "read", side_effect=(BlockingIOError(), b"", b"")
        ):
            self.assertEqual(
                ria._run_git(  # noqa: SLF001
                    self.root, ("rev-parse", "--verify", "HEAD")
                ),
                b"",
            )

        failing_stdout = mock.Mock()
        failing_stdout.fileno.return_value = 12
        failing_stderr = mock.Mock()
        failing_stderr.fileno.return_value = 13
        failing_process = mock.Mock(stdout=failing_stdout, stderr=failing_stderr)
        failing_process.poll.return_value = None
        failing_process.wait.return_value = -9
        failing_key = mock.Mock(data="stdout", fileobj=failing_stdout)
        failing_selector = mock.Mock()
        failing_selector.get_map.return_value = {1: failing_stdout}
        failing_selector.select.return_value = [
            (failing_key, ria.selectors.EVENT_READ)
        ]
        with mock.patch.object(
            ria.subprocess, "Popen", return_value=failing_process
        ), mock.patch.object(
            ria.selectors, "DefaultSelector", return_value=failing_selector
        ), mock.patch.object(ria.os, "set_blocking"), mock.patch.object(
            ria.os, "read", side_effect=OSError("hostile payload")
        ):
            with self.assertRaisesRegex(ria._GitError, "read failed"):  # noqa: SLF001
                ria._run_git(  # noqa: SLF001
                    self.root, ("rev-parse", "--verify", "HEAD")
                )
        failing_process.kill.assert_called_once_with()
        failing_process.wait.assert_called()

        selector_failure_process = mock.Mock(
            stdout=mock.Mock(), stderr=mock.Mock()
        )
        selector_failure_process.poll.return_value = None
        selector_failure_process.wait.return_value = -9
        with mock.patch.object(
            ria.subprocess, "Popen", return_value=selector_failure_process
        ), mock.patch.object(
            ria.selectors,
            "DefaultSelector",
            side_effect=OSError("selector unavailable"),
        ):
            with self.assertRaisesRegex(
                ria._GitError, "operation failed"  # noqa: SLF001
            ):
                ria._run_git(  # noqa: SLF001
                    self.root, ("rev-parse", "--verify", "HEAD")
                )
        selector_failure_process.kill.assert_called_once_with()
        selector_failure_process.wait.assert_called()

    def test_tree_blob_and_size_hostile_matrix(self) -> None:
        oid = "a" * 40
        path = Path("docs/example.md")
        valid = f"100644 blob {oid}\tdocs/example.md\0".encode()
        self.assertEqual(ria._parse_tree_record(valid, path), oid)  # noqa: SLF001
        tree_cases = (
            b"",
            valid + valid,
            f"100644 blob {oid}\tdocs/other.md\0".encode(),
            f"120000 blob {oid}\tdocs/example.md\0".encode(),
            f"160000 commit {oid}\tdocs/example.md\0".encode(),
            f"100644 tree {oid}\tdocs/example.md\0".encode(),
            f"100644 blob {'A' * 40}\tdocs/example.md\0".encode(),
        )
        for payload in tree_cases:
            with self.subTest(payload=payload[:30]):
                with self.assertRaises(ria._GitError):  # noqa: SLF001
                    ria._parse_tree_record(payload, path)  # noqa: SLF001

        for payload in (b"00\n", b"01\n", b"+1\n", b"1", b"2000001\n"):
            with self.subTest(size=payload):
                with self.assertRaises(ria._GitError):  # noqa: SLF001
                    ria._parse_canonical_size(payload)  # noqa: SLF001

        def blob_runner(
            root: Path, arguments: tuple[str, ...], limit: int
        ) -> bytes:
            del root, limit
            if arguments[:2] == ("cat-file", "-t"):
                return b"blob\n"
            if arguments[:2] == ("cat-file", "-s"):
                return b"3\n"
            return b"xx"

        with self.assertRaisesRegex(ria._GitError, "length"):  # noqa: SLF001
            ria._read_blob(self.root, oid, blob_runner)  # noqa: SLF001

        def extra_blob_runner(
            root: Path, arguments: tuple[str, ...], limit: int
        ) -> bytes:
            del root, limit
            if arguments[:2] == ("cat-file", "-t"):
                return b"blob\n"
            if arguments[:2] == ("cat-file", "-s"):
                return b"1\n"
            return b"xx"

        with self.assertRaisesRegex(ria._GitError, "length"):  # noqa: SLF001
            ria._read_blob(self.root, oid, extra_blob_runner)  # noqa: SLF001

    def test_proposed_index_authority_hostile_matrix(self) -> None:
        oid = "a" * 40
        path = Path("docs/example.md")
        valid = f"100644 {oid} 0\tdocs/example.md\0".encode()
        self.assertEqual(ria._parse_index_record(valid, path), oid)  # noqa: SLF001
        index_cases = (
            b"",  # staged delete with an untracked replacement
            valid + valid,
            f"100644 {oid} 1\tdocs/example.md\0".encode(),
            f"100644 {oid} 2\tdocs/example.md\0".encode(),
            f"100644 {oid} 3\tdocs/example.md\0".encode(),
            f"120000 {oid} 0\tdocs/example.md\0".encode(),
            f"160000 {oid} 0\tdocs/example.md\0".encode(),
            f"100644 {oid} 0\tdocs/other.md\0".encode(),
        )
        for payload in index_cases:
            with self.subTest(payload=payload[:30]):
                with self.assertRaises(ria._GitError):  # noqa: SLF001
                    ria._parse_index_record(payload, path)  # noqa: SLF001

        absolute = self.root / path
        absolute.parent.mkdir(parents=True, exist_ok=True)
        absolute.write_bytes(b"worktree replacement")

        def deleted_runner(
            root: Path, arguments: tuple[str, ...], limit: int
        ) -> bytes:
            del root, arguments, limit
            return b""

        with self.assertRaises(ria._GitError):  # noqa: SLF001
            ria.read_proposed_regular_file(self.root, path, deleted_runner)

        def drift_runner(
            root: Path, arguments: tuple[str, ...], limit: int
        ) -> bytes:
            del root, limit
            if arguments[0] == "ls-files":
                return valid
            if arguments[:2] == ("cat-file", "-t"):
                return b"blob\n"
            if arguments[:2] == ("cat-file", "-s"):
                return b"7\n"
            return b"indexed"

        with self.assertRaisesRegex(ContractError, "index and worktree"):
            ria.read_proposed_regular_file(self.root, path, drift_runner)

    def test_transition_fsm_rejects_every_noncanonical_state(self) -> None:
        cases: list[dict[str, object]] = []
        forged_root = self._minimal_contract()
        forged_root["currentPackBaselines"]["audits/2026-07-11-weia"] = (
            "git-sha1:" + "a" * 40
        )
        cases.append(forged_root)
        audit_transition = self._minimal_contract()
        audit_transition["baselineTransitions"] = [
            {**self._transition(), "packId": "audits/2026-07-11-weia"}
        ]
        cases.append(audit_transition)
        multiple = self._minimal_contract()
        multiple["baselineTransitions"] = [self._transition(), self._transition()]
        cases.append(multiple)
        stale = self._minimal_contract()
        stale["baselineTransitions"] = [
            {**self._transition(), "fromCommit": "git-sha1:" + "a" * 40}
        ]
        cases.append(stale)
        arbitrary_subject = self._minimal_contract()
        arbitrary_subject["baselineTransitions"] = [
            {**self._transition(), "subject": "other-member"}
        ]
        cases.append(arbitrary_subject)
        reused = self._settled_contract()
        reused["baselineTransitions"] = [self._transition()]
        cases.append(reused)
        for contract in cases:
            with self.subTest(contract=contract):
                state, finding = ria._fsm_state(contract)  # noqa: SLF001
                self.assertIsNone(state)
                self.assertEqual(finding.rule_id, "RIA-TRANSITION")

    def test_staged_and_explicit_lineage_hostile_matrix(self) -> None:
        c2 = "b" * 40
        c3 = "c" * 40
        contract = self._settled_contract("git-sha1:" + c2)

        def explicit_runner(
            parents: tuple[str, ...],
            rows: bytes = b"M\0docs/90.references/data/reference-information-architecture.json\0",
        ):
            def runner(
                root: Path, arguments: tuple[str, ...], limit: int
            ) -> bytes:
                del root, limit
                if arguments == ("cat-file", "-t", c3):
                    return b"commit\n"
                if arguments == ("cat-file", "commit", c3):
                    headers = [f"tree {'d' * 40}", *[f"parent {p}" for p in parents]]
                    return ("\n".join(headers) + "\n\nmessage\n").encode()
                if arguments[0] == "diff-tree":
                    return rows
                raise AssertionError(arguments)

            return runner

        self.assertEqual(
            ria.validate_explicit_commit_lineage(
                self.root, contract, "git-sha1:" + c3, runner=explicit_runner((c2,))
            ),
            [],
        )
        for parents in ((), ("a" * 40,), (c2, "a" * 40)):
            with self.subTest(parents=parents):
                findings = ria.validate_explicit_commit_lineage(
                    self.root,
                    contract,
                    "git-sha1:" + c3,
                    runner=explicit_runner(parents),
                )
                self.assertEqual(
                    [finding.rule_id for finding in findings], ["RIA-TRANSITION"]
                )
        extra_tree_change = explicit_runner(
            (c2,),
            b"M\0docs/90.references/data/reference-information-architecture.json\0"
            b"M\0docs/other.md\0",
        )
        self.assertEqual(
            [
                finding.rule_id
                for finding in ria.validate_explicit_commit_lineage(
                    self.root,
                    contract,
                    "git-sha1:" + c3,
                    runner=extra_tree_change,
                )
            ],
            ["RIA-TRANSITION"],
        )

        def staged_runner(
            head: str, rows: bytes = b"M\0docs/90.references/data/reference-information-architecture.json\0"
        ):
            def runner(
                root: Path, arguments: tuple[str, ...], limit: int
            ) -> bytes:
                del root, limit
                if arguments == ("rev-parse", "--verify", "HEAD"):
                    return f"{head}\n".encode()
                if arguments == ("cat-file", "-t", head):
                    return b"commit\n"
                if arguments[0] == "diff-index":
                    return rows
                raise AssertionError(arguments)

            return runner

        self.assertEqual(
            ria.validate_staged_settlement_lineage(
                self.root, contract, runner=staged_runner(c2)
            ),
            [],
        )
        staged_cases = (
            staged_runner("a" * 40),
            staged_runner(
                c2,
                b"M\0docs/90.references/data/reference-information-architecture.json\0"
                b"M\0docs/other.md\0",
            ),
        )
        for runner in staged_cases:
            findings = ria.validate_staged_settlement_lineage(
                self.root, contract, runner=runner
            )
            self.assertEqual(
                [finding.rule_id for finding in findings], ["RIA-TRANSITION"]
            )

    def test_proposed_stage_zero_authority_is_required(self) -> None:
        self.assertTrue(callable(ria.read_proposed_regular_file))
        self.assertTrue(callable(ria.validate_proposed_registry_authority))

    def test_cli_modes_are_mutually_exclusive_and_terminal_is_orthogonal(self) -> None:
        terminal = subprocess.run(
            [
                sys.executable,
                str(CLI),
                "--root",
                str(REPOSITORY_ROOT),
                "--require-settled-baselines",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        conflict = subprocess.run(
            [
                sys.executable,
                str(CLI),
                "--staged",
                "--commit",
                ROOT_BASELINE,
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        malformed = subprocess.run(
            [sys.executable, str(CLI), "--commit", "HEAD"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(terminal.returncode, 0, terminal.stderr)
        self.assertEqual(conflict.returncode, 2)
        self.assertEqual(malformed.returncode, 2)


if __name__ == "__main__":
    unittest.main()
