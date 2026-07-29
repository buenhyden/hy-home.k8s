"""Focused immutable-snapshot, overlay, and lineage tests for RIA-002."""

from __future__ import annotations

import json
import hashlib
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import tracemalloc
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
AGGREGATE = REPOSITORY_ROOT / "scripts/validate-repo-quality-gates.sh"
SNAPSHOT_MUTATION = (
    REPOSITORY_ROOT
    / "tests/fixtures/reference-information-architecture/snapshot-mutation.json"
)
OVERLAY_MUTATION = (
    REPOSITORY_ROOT
    / "tests/fixtures/reference-information-architecture/overlay-mutation.json"
)
SOURCE_FRESHNESS = (
    REPOSITORY_ROOT
    / "tests/fixtures/reference-information-architecture/source-freshness.json"
)
GENERATOR_COLLISION = (
    REPOSITORY_ROOT
    / "tests/fixtures/reference-information-architecture/generator-collision.json"
)
CURRENT_OWNER = (
    REPOSITORY_ROOT
    / "tests/fixtures/reference-information-architecture/current-owner.json"
)
POLICY_COPY = (
    REPOSITORY_ROOT
    / "tests/fixtures/reference-information-architecture/policy-copy.json"
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

    def _source_contract(self) -> dict[str, object]:
        fixture = json.loads(SOURCE_FRESHNESS.read_text(encoding="utf-8"))
        contract = self._minimal_contract()
        contract["evidenceCutoff"] = fixture["evidenceCutoff"]
        contract["dataAssets"] = [fixture["dataAsset"]]
        return contract

    def _write_source_evidence(self, *, tracked: bool) -> None:
        path = self.root / "docs/90.references/data/source-ledger-fixture.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("{}\n", encoding="utf-8")
        if not (self.root / ".git").exists():
            self._git_in(self.root, "init", "--quiet")
        if tracked:
            self._git_in(
                self.root,
                "add",
                "--",
                "docs/90.references/data/source-ledger-fixture.json",
            )

    def _generator_fixture(self) -> dict[str, object]:
        return json.loads(GENERATOR_COLLISION.read_text(encoding="utf-8"))

    def _generator_contract(
        self, relations: list[dict[str, object]]
    ) -> dict[str, object]:
        contract = self._minimal_contract()
        contract["generatedAssets"] = relations
        return contract

    def _generator_repository(self) -> Path:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        paths = (
            Path("scripts/generate-llm-wiki-index.sh"),
            Path("docs/90.references/llm-wiki/README.md"),
            Path("docs/90.references/llm-wiki/wiki-index.md"),
            Path("docs/00.agent-governance/README.md"),
            Path("docs/00.agent-governance/harness-catalog.md"),
            Path("docs/00.agent-governance/rules/document-stage-routing.md"),
            Path("docs/README.md"),
            Path("scripts/README.md"),
            Path("docs/90.references/README.md"),
            Path("docs/90.references/data/README.md"),
        )
        for path in paths:
            destination = root / path
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes((REPOSITORY_ROOT / path).read_bytes())
        self._git_in(root, "init", "--quiet")
        self._git_in(root, "add", "--", *(path.as_posix() for path in paths))
        return root

    def _replace_generator(self, root: Path, payload: bytes) -> None:
        path = Path("scripts/generate-llm-wiki-index.sh")
        (root / path).write_bytes(payload)
        self._git_in(root, "add", "--", path.as_posix())

    def _duplicate_repository(
        self,
        *,
        audit_index: str | None = None,
        extra_current_members: dict[str, str] | None = None,
    ) -> tuple[Path, dict[str, object], dict[str, object], dict[str, object]]:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        owners = json.loads(CURRENT_OWNER.read_text(encoding="utf-8"))
        copies = json.loads(POLICY_COPY.read_text(encoding="utf-8"))
        extra_current_members = extra_current_members or {}
        audit_members = [
            "stage00-copy.md",
            "policy-copy.md",
            *(
                Path(path).name
                for path in extra_current_members
                if "/audits/2026-07-11-weia/" in path
            ),
        ]
        research_members = [
            "runbook-copy.md",
            *(
                Path(path).name
                for path in extra_current_members
                if "/research/2026-07-07-wer/" in path
            ),
        ]
        payloads = {
            "docs/99.templates/support/document-profiles.json": json.dumps(
                {
                    "referenceCurrentPacks": {
                        "profileId": "content/reference",
                        "packs": [
                            {
                                "id": "audits/2026-07-11-weia",
                                "members": audit_members,
                                "allowedStates": ["done"],
                            },
                            {
                                "id": "research/2026-07-07-wer",
                                "members": research_members,
                                "allowedStates": ["active", "accepted"],
                            },
                        ],
                    }
                },
                indent=2,
            )
            + "\n",
            "docs/90.references/audits/README.md": audit_index
            if audit_index is not None
            else owners["auditIndex"],
            "docs/90.references/research/README.md": owners["researchIndex"],
            "docs/90.references/audits/2026-07-11-weia/README.md": "# Audit pack\n",
            "docs/90.references/research/2026-07-07-wer/README.md": "# Research pack\n",
            copies["stage00"]["canonicalPath"]: copies["stage00"][
                "canonicalParagraph"
            ]
            + "\n",
            copies["stage00"]["referencePath"]: "No copied policy text.\n",
            copies["policy"]["canonicalPath"]: copies["policy"][
                "canonicalParagraph"
            ]
            + "\n",
            copies["policy"]["referencePath"]: "No copied policy text.\n",
            copies["runbook"]["canonicalPath"]: copies["runbook"][
                "canonicalParagraph"
            ]
            + "\n",
            copies["runbook"]["referencePath"]: "No copied runbook text.\n",
            **extra_current_members,
        }
        for relative, payload in payloads.items():
            destination = root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(payload, encoding="utf-8")
        self._git_in(root, "init", "--quiet")
        self._git_in(root, "add", "--", *sorted(payloads))
        return root, self._minimal_contract(), owners, copies

    def _assert_generator_failure(
        self, findings: list[ria.Finding], *secret_values: str
    ) -> None:
        self.assertTrue(findings)
        self.assertEqual({finding.rule_id for finding in findings}, {"RIA-GENERATOR"})
        rendered = repr(findings)
        for value in secret_values:
            if value:
                self.assertNotIn(value, rendered)

    @staticmethod
    def _git_in(
        root: Path, *arguments: str, input_payload: bytes | None = None
    ) -> bytes:
        environment = {
            "HOME": str(root),
            "PATH": "/usr/bin:/bin",
            "LANG": "C",
            "LC_ALL": "C",
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": "/dev/null",
            "GIT_TERMINAL_PROMPT": "0",
            "GIT_OPTIONAL_LOCKS": "0",
        }
        completed = subprocess.run(
            [ria.GIT_EXECUTABLE, *arguments],
            cwd=root,
            env=environment,
            input=input_payload,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if completed.returncode != 0:
            raise AssertionError(
                f"isolated Git command failed: {arguments!r}: "
                f"{completed.stderr.decode('utf-8', 'replace')}"
            )
        return completed.stdout

    def _load(self) -> dict[str, object]:
        return ria._load_contract_for_self_test(  # noqa: SLF001
            self.root, self.contract_path
        )

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
        contract_path = Path(
            "docs/alternate/reference-information-architecture.json"
        )
        schema_path = contract_path.with_name(
            "reference-information-architecture.schema.json"
        )
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
                    if path == contract_path:
                        oid, mode = contract_oid, "100644"
                    elif path == schema_path:
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
                contract_path,
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
                        contract_path,
                        runner=commit_runner(
                            schema_payload, schema_mode, schema_size
                        ),
                    )

    def test_cli_and_validation_thread_selected_contract_authority_path(
        self,
    ) -> None:
        selected = Path(
            "docs/alternate/reference-information-architecture.json"
        )
        contract = self._minimal_contract()
        cli = _load_cli_module()
        with (
            mock.patch.object(
                cli, "load_contract", return_value=contract
            ) as loader,
            mock.patch.object(
                cli, "validate_reference_architecture", return_value=[]
            ) as validator,
        ):
            self.assertEqual(
                cli.main(
                    [
                        "--root",
                        str(self.root),
                        "--contract",
                        selected.as_posix(),
                    ]
                ),
                0,
            )
        loader.assert_called_once_with(self.root.absolute(), selected)
        self.assertEqual(
            validator.call_args.kwargs["contract_path"], selected
        )

        with (
            mock.patch.object(
                ria, "_contract_authority_finding", return_value=None
            ) as authority,
            mock.patch.object(ria, "validate_snapshot_guards", return_value=[]),
            mock.patch.object(ria, "validate_overlay_guards", return_value=[]),
            mock.patch.object(ria, "validate_data_assets", return_value=[]),
            mock.patch.object(ria, "validate_generated_assets", return_value=[]),
            mock.patch.object(ria, "validate_duplicate_rules", return_value=[]),
            mock.patch.object(
                ria, "validate_baseline_transitions", return_value=[]
            ) as transitions,
        ):
            self.assertEqual(
                ria.validate_reference_architecture(
                    self.root,
                    contract,
                    contract_path=selected,
                ),
                [],
            )
        self.assertEqual(authority.call_args.kwargs["contract_path"], selected)
        self.assertEqual(
            transitions.call_args.kwargs["contract_path"], selected
        )

        payload = json.dumps(contract, separators=(",", ":")).encode()
        with mock.patch.object(
            ria, "read_proposed_regular_file", return_value=payload
        ) as reader:
            self.assertIsNone(
                ria._contract_authority_finding(  # noqa: SLF001
                    self.root.absolute(),
                    contract,
                    contract_path=selected,
                    commit=None,
                    runner=None,
                )
            )
        reader.assert_called_once_with(self.root.absolute(), selected, None)

        commit_oid = "c" * 40
        with mock.patch.object(
            ria, "_read_commit_path", return_value=payload
        ) as commit_reader:
            self.assertIsNone(
                ria._contract_authority_finding(  # noqa: SLF001
                    self.root.absolute(),
                    contract,
                    contract_path=selected,
                    commit="git-sha1:" + commit_oid,
                    runner=None,
                )
            )
        commit_reader.assert_called_once_with(
            self.root.absolute(),
            commit_oid,
            selected,
            None,
        )

    def test_normal_schema_requires_stage_zero_index_worktree_authority(
        self,
    ) -> None:
        def repository() -> tuple[tempfile.TemporaryDirectory, Path, Path]:
            temporary = tempfile.TemporaryDirectory()
            root = Path(temporary.name)
            contract_path = root / ria.DEFAULT_CONTRACT_PATH
            schema_path = root / ria.CANONICAL_SCHEMA_PATH
            contract_path.parent.mkdir(parents=True)
            contract_path.write_text(
                json.dumps(self._minimal_contract()), encoding="utf-8"
            )
            schema_path.write_bytes(SCHEMA.read_bytes())
            self._git_in(root, "init", "--quiet")
            self._git_in(
                root, "add", "--", ria.CANONICAL_SCHEMA_PATH.as_posix()
            )
            return temporary, root, contract_path

        for mutation in ("drift", "missing", "special-mode", "unmerged"):
            with self.subTest(mutation=mutation):
                temporary, root, contract_path = repository()
                try:
                    self.assertEqual(
                        ria.load_contract(root, contract_path),
                        self._minimal_contract(),
                    )
                    schema_path = root / ria.CANONICAL_SCHEMA_PATH
                    if mutation == "drift":
                        schema_path.write_bytes(SCHEMA.read_bytes() + b"\n")
                    elif mutation == "missing":
                        self._git_in(
                            root,
                            "rm",
                            "--cached",
                            "--quiet",
                            "--",
                            ria.CANONICAL_SCHEMA_PATH.as_posix(),
                        )
                    else:
                        oid = self._git_in(
                            root,
                            "hash-object",
                            "-w",
                            "--",
                            ria.CANONICAL_SCHEMA_PATH.as_posix(),
                        ).strip().decode("ascii")
                        self._git_in(
                            root,
                            "update-index",
                            "--force-remove",
                            ria.CANONICAL_SCHEMA_PATH.as_posix(),
                        )
                        if mutation == "special-mode":
                            self._git_in(
                                root,
                                "update-index",
                                "--add",
                                "--cacheinfo",
                                f"120000,{oid},{ria.CANONICAL_SCHEMA_PATH.as_posix()}",
                            )
                        else:
                            rows = "".join(
                                f"100644 {oid} {stage}\t"
                                f"{ria.CANONICAL_SCHEMA_PATH.as_posix()}\n"
                                for stage in (1, 2, 3)
                            ).encode()
                            self._git_in(
                                root,
                                "update-index",
                                "--index-info",
                                input_payload=rows,
                            )
                    with self.assertRaisesRegex(ContractError, "RIA-CONTRACT"):
                        ria.load_contract(root, contract_path)
                finally:
                    temporary.cleanup()

        with self.subTest(mutation="isolated-self-test-loader"):
            self.assertTrue(hasattr(ria, "_load_contract_for_self_test"))
            cli = _load_cli_module()
            self.assertIs(cli.load_contract, ria.load_contract)
            self.assertNotIn("_load_contract_for_self_test", vars(cli))
            for mode in ((), ("--staged",)):
                with self.subTest(cli_mode=mode), mock.patch.object(
                    cli,
                    "load_contract",
                    side_effect=ContractError(
                        "RIA-CONTRACT", "$schema", "schema authority unavailable"
                    ),
                ) as production_loader, redirect_stderr(StringIO()):
                    self.assertEqual(
                        cli.main(["--root", str(self.root), *mode]), 2
                    )
                production_loader.assert_called_once()

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

    def test_data_asset_requires_source_scope_date_and_trigger(self) -> None:
        self._write_source_evidence(tracked=True)
        mutations = (
            ("missing-url", lambda asset, source: source.pop("url")),
            (
                "non-https-url",
                lambda asset, source: source.update(
                    {"url": "http://example.invalid/source"}
                ),
            ),
            ("invalid-date", lambda asset, source: source.update({"checkedOn": "2026-02-30"})),
            ("empty-adopted", lambda asset, source: source.update({"adoptedScope": []})),
            ("empty-rejected", lambda asset, source: source.update({"rejectedScope": []})),
            ("empty-trigger", lambda asset, source: asset.update({"refreshTrigger": ""})),
            ("unknown-asset-field", lambda asset, source: asset.update({"authority": "invented"})),
            ("unknown-source-field", lambda asset, source: source.update({"status": "PASS"})),
            ("duplicate-source", lambda asset, source: asset["sources"].append(dict(source))),
        )
        for name, mutate in mutations:
            with self.subTest(case=name):
                contract = self._source_contract()
                asset = contract["dataAssets"][0]
                source = asset["sources"][0]
                mutate(asset, source)
                findings = ria.validate_data_assets(self.root, contract)
                self.assertTrue(findings)
                self.assertEqual({finding.rule_id for finding in findings}, {"RIA-SOURCE"})

        with self.subTest(case="missing-asset"):
            contract = self._source_contract()
            contract["dataAssets"][0]["repositoryEvidence"] = [
                "docs/90.references/data/missing-source-ledger-fixture.json"
            ]
            findings = ria.validate_data_assets(self.root, contract)
            self.assertEqual({finding.rule_id for finding in findings}, {"RIA-SOURCE"})

        with self.subTest(case="empty-ledger"):
            contract = self._source_contract()
            contract["dataAssets"] = []
            findings = ria.validate_data_assets(self.root, contract)
            self.assertEqual({finding.rule_id for finding in findings}, {"RIA-SOURCE"})

    def test_data_asset_rejects_after_cutoff_and_untracked_evidence(self) -> None:
        self._write_source_evidence(tracked=True)
        contract = self._source_contract()
        contract["dataAssets"][0]["sources"][0]["checkedOn"] = "2026-07-23"
        findings = ria.validate_data_assets(self.root, contract)
        self.assertEqual({finding.rule_id for finding in findings}, {"RIA-SOURCE"})

        contract = self._source_contract()
        contract["evidenceCutoff"] = "2026-02-30"
        findings = ria.validate_data_assets(self.root, contract)
        self.assertEqual({finding.rule_id for finding in findings}, {"RIA-SOURCE"})

        self._git_in(
            self.root,
            "rm",
            "--cached",
            "--quiet",
            "--",
            "docs/90.references/data/source-ledger-fixture.json",
        )
        findings = ria.validate_data_assets(self.root, self._source_contract())
        self.assertEqual({finding.rule_id for finding in findings}, {"RIA-SOURCE"})

    def test_data_asset_accepts_closed_source_ledger(self) -> None:
        self._write_source_evidence(tracked=True)
        self.assertEqual(
            ria.validate_data_assets(self.root, self._source_contract()),
            [],
        )

    def test_generator_requires_unique_owner_relation(self) -> None:
        fixture = self._generator_fixture()
        duplicate = fixture["duplicateOwnerRelations"]
        identity = fixture["generatorOutputIdentity"]
        assert isinstance(duplicate, list) and isinstance(identity, dict)

        root = self._generator_repository()
        self._assert_generator_failure(
            ria.validate_generated_assets(root, self._generator_contract(duplicate))
        )

        root = self._generator_repository()
        self._assert_generator_failure(
            ria.validate_generated_assets(root, self._generator_contract([identity]))
        )

        relation = dict(fixture["validRelation"])
        relation["executable"] = "/tmp/contract-controlled"
        root = self._generator_repository()
        self._assert_generator_failure(
            ria.validate_generated_assets(root, self._generator_contract([relation])),
            "/tmp/contract-controlled",
        )

        relation = dict(fixture["validRelation"])
        relation["id"] = "alternate-wiki-index"
        root = self._generator_repository()
        self._assert_generator_failure(
            ria.validate_generated_assets(root, self._generator_contract([relation]))
        )

        for owner in (
            "docs/README.md",
            "docs/00.agent-governance/README.md",
            "scripts/README.md",
        ):
            with self.subTest(case="wrong-linked-owner", owner=owner):
                relation = dict(fixture["validRelation"])
                relation["canonicalOwnerPath"] = owner
                root = self._generator_repository()
                self._assert_generator_failure(
                    ria.validate_generated_assets(
                        root, self._generator_contract([relation])
                    )
                )

        expected_inputs = list(fixture["validRelation"]["inputRoots"])
        input_mutations = (
            ("arbitrary", ["docs/README.md"]),
            ("missing", []),
            (
                "extra",
                [*expected_inputs, "docs/90.references/data/README.md"],
            ),
            ("reordered", list(reversed(expected_inputs))),
            ("duplicate", [*expected_inputs, expected_inputs[0]]),
        )
        for name, input_roots in input_mutations:
            with self.subTest(case="input-relation", mutation=name):
                relation = dict(fixture["validRelation"])
                relation["inputRoots"] = input_roots
                root = self._generator_repository()
                self._assert_generator_failure(
                    ria.validate_generated_assets(
                        root, self._generator_contract([relation])
                    )
                )

        for path in (
            "scripts/generate-llm-wiki-index.sh",
            "docs/90.references/llm-wiki/README.md",
            "docs/90.references/llm-wiki/wiki-index.md",
        ):
            with self.subTest(case="untracked", path=path):
                root = self._generator_repository()
                self._git_in(root, "rm", "--cached", "--quiet", "--", path)
                relation = dict(fixture["validRelation"])
                self._assert_generator_failure(
                    ria.validate_generated_assets(
                        root, self._generator_contract([relation])
                    )
                )

        output = Path("docs/90.references/llm-wiki/wiki-index.md")
        for kind in ("directory", "symlink", "fifo"):
            with self.subTest(case="nonregular-output", kind=kind):
                root = self._generator_repository()
                target = root / output
                target.unlink()
                if kind == "directory":
                    target.mkdir()
                elif kind == "symlink":
                    target.symlink_to("README.md")
                else:
                    os.mkfifo(target)
                relation = dict(fixture["validRelation"])
                self._assert_generator_failure(
                    ria.validate_generated_assets(
                        root, self._generator_contract([relation])
                    )
                )

    def test_generator_rejects_unmapped_command_and_stale_output(self) -> None:
        fixture = self._generator_fixture()
        unmapped = fixture["unmappedCommand"]
        assert isinstance(unmapped, dict)
        root = self._generator_repository()
        marker = root / "docs/90.references/llm-wiki/command-injection"
        self._assert_generator_failure(
            ria.validate_generated_assets(root, self._generator_contract([unmapped])),
            "command-injection",
        )
        self.assertFalse(marker.exists())

        root = self._generator_repository()
        output = root / "docs/90.references/llm-wiki/wiki-index.md"
        output.write_bytes(output.read_bytes() + b"\nSENSITIVE-STALE-BYTES\n")
        self._git_in(
            root,
            "add",
            "--",
            "docs/90.references/llm-wiki/wiki-index.md",
        )
        relation = dict(fixture["validRelation"])
        self._assert_generator_failure(
            ria.validate_generated_assets(root, self._generator_contract([relation])),
            "SENSITIVE-STALE-BYTES",
        )

        process_cases = (
            (
                "timeout",
                b"#!/usr/bin/env bash\nsleep 1\n",
                "GENERATOR_TIMEOUT_SECONDS",
                0.05,
                "",
            ),
            (
                "stdout-overflow",
                b"#!/usr/bin/env bash\nprintf 'SENSITIVE-STDOUT-OVERFLOW'\n",
                "GENERATOR_STDOUT_BYTES",
                8,
                "SENSITIVE-STDOUT-OVERFLOW",
            ),
            (
                "stderr-overflow",
                b"#!/usr/bin/env bash\nprintf 'SENSITIVE-STDERR-OVERFLOW' >&2\n",
                "GENERATOR_STDERR_BYTES",
                8,
                "SENSITIVE-STDERR-OVERFLOW",
            ),
        )
        for name, payload, setting, limit, secret in process_cases:
            with self.subTest(case=name):
                root = self._generator_repository()
                self._replace_generator(root, payload)
                relation = dict(fixture["validRelation"])
                with mock.patch.object(ria, setting, limit):
                    findings = ria.validate_generated_assets(
                        root, self._generator_contract([relation])
                    )
                self._assert_generator_failure(findings, secret)

    def test_generator_accepts_llm_wiki_relation(self) -> None:
        fixture = self._generator_fixture()
        relation = fixture["validRelation"]
        assert isinstance(relation, dict)
        root = self._generator_repository()
        real_popen = subprocess.Popen
        with mock.patch.object(ria.subprocess, "Popen", wraps=real_popen) as popen:
            self.assertEqual(
                ria.validate_generated_assets(
                    root, self._generator_contract([dict(relation)])
                ),
                [],
            )
        expected_argv = [
            "/usr/bin/bash",
            "scripts/generate-llm-wiki-index.sh",
            "--check",
        ]
        generator_calls = [
            call
            for call in popen.call_args_list
            if call.args and call.args[0] == expected_argv
        ]
        self.assertEqual(len(generator_calls), 1)
        invocation = generator_calls[0]
        self.assertEqual(invocation.kwargs["cwd"], root.absolute())
        self.assertEqual(invocation.kwargs["env"], ria.CLOSED_GENERATOR_ENVIRONMENT)
        self.assertIs(invocation.kwargs["stdin"], subprocess.DEVNULL)
        self.assertIs(invocation.kwargs["stdout"], subprocess.PIPE)
        self.assertIs(invocation.kwargs["stderr"], subprocess.PIPE)
        self.assertIs(invocation.kwargs["shell"], False)

        root = self._generator_repository()
        stale_owner = dict(relation)
        stale_owner["canonicalOwnerPath"] = "docs/90.references/data/README.md"
        self._assert_generator_failure(
            ria.validate_generated_assets(
                root, self._generator_contract([stale_owner])
            )
        )

    def test_duplicate_current_and_generated_manual_owners_fail(self) -> None:
        root, contract, owners, _copies = self._duplicate_repository()
        self.assertEqual(ria.validate_duplicate_rules(root, contract), [])

        self._git_in(
            root,
            "-c",
            "user.name=RIA Fixture",
            "-c",
            "user.email=ria-fixture@example.invalid",
            "commit",
            "--quiet",
            "-m",
            "fixture baseline",
        )
        commit_oid = self._git_in(root, "rev-parse", "HEAD").decode().strip()
        audit_index_path = root / "docs/90.references/audits/README.md"
        audit_index_path.write_text(owners["duplicateAuditIndex"], encoding="utf-8")
        self._git_in(root, "add", "--", "docs/90.references/audits/README.md")
        self.assertTrue(ria.validate_duplicate_rules(root, contract))
        self.assertEqual(
            ria.validate_duplicate_rules(
                root, contract, proposed_commit=f"git-sha1:{commit_oid}"
            ),
            [],
        )
        audit_index_path.write_text(owners["auditIndex"], encoding="utf-8")
        self.assertTrue(ria.validate_duplicate_rules(root, contract))

        root, contract, _owners, _copies = self._duplicate_repository(
            audit_index=owners["duplicateAuditIndex"]
        )
        findings = ria.validate_duplicate_rules(root, contract)
        self.assertTrue(findings)
        self.assertEqual({finding.rule_id for finding in findings}, {"RIA-DUPLICATE"})
        self.assertIn(
            "docs/90.references/audits/README.md",
            {finding.path for finding in findings},
        )

        duplicate_heading = (
            owners["auditIndex"]
            + "\n### Audit Pack Registry\n\n"
            + "| Pack | Pack role |\n| --- | --- |\n"
            + "| [rogue](./2026-07-12-weia/README.md) | Current pack |\n"
        )
        root, contract, _owners, _copies = self._duplicate_repository(
            audit_index=duplicate_heading
        )
        findings = ria.validate_duplicate_rules(root, contract)
        self.assertIn(
            "docs/90.references/audits/README.md",
            {finding.path for finding in findings},
        )

        output_path = owners["manualGeneratedOutputPath"]
        root, contract, _owners, _copies = self._duplicate_repository(
            extra_current_members={output_path: "# Manually authored current report\n"}
        )
        contract["generatedAssets"] = [
            {
                "id": "manual-generated-collision",
                "generatorPath": "scripts/generate-llm-wiki-index.sh",
                "inputRoots": ["docs/90.references/llm-wiki/README.md"],
                "outputPath": output_path,
                "checkCommand": "bash scripts/generate-llm-wiki-index.sh --check",
                "canonicalOwnerPath": "docs/90.references/llm-wiki/README.md",
            }
        ]
        findings = ria.validate_duplicate_rules(root, contract)
        self.assertIn(output_path, {finding.path for finding in findings})

    def test_duplicate_rules_require_one_current_owner_per_collection(self) -> None:
        for collection, second_pack in (
            ("audits", "2026-07-12-weia"),
            ("research", "2026-07-08-wer"),
        ):
            with self.subTest(collection=collection):
                root, contract, owners, _copies = self._duplicate_repository()
                registry_path = root / ria.REGISTRY_PATH
                registry = json.loads(registry_path.read_text(encoding="utf-8"))
                registry["referenceCurrentPacks"]["packs"].append(
                    {
                        "id": f"{collection}/{second_pack}",
                        "members": [],
                        "allowedStates": ["active"],
                    }
                )
                registry_path.write_text(
                    json.dumps(registry, indent=2) + "\n",
                    encoding="utf-8",
                )
                second_readme = (
                    root
                    / "docs/90.references"
                    / collection
                    / second_pack
                    / "README.md"
                )
                second_readme.parent.mkdir(parents=True)
                second_readme.write_text("# Second Current pack\n", encoding="utf-8")
                if collection == "audits":
                    index_path = root / "docs/90.references/audits/README.md"
                    index_path.write_text(
                        owners["duplicateAuditIndex"], encoding="utf-8"
                    )
                else:
                    index_path = root / "docs/90.references/research/README.md"
                    index_path.write_text(
                        owners["researchIndex"]
                        + (
                            "| [2026-07-08-wer/README.md]"
                            "(./2026-07-08-wer/README.md) | Current pack |\n"
                        ),
                        encoding="utf-8",
                    )
                self._git_in(
                    root,
                    "add",
                    "--",
                    ria.REGISTRY_PATH.as_posix(),
                    index_path.relative_to(root).as_posix(),
                    second_readme.relative_to(root).as_posix(),
                )

                findings = ria.validate_duplicate_rules(root, contract)
                self.assertTrue(findings)
                self.assertEqual(
                    {finding.rule_id for finding in findings},
                    {"RIA-DUPLICATE"},
                )

    def test_policy_paragraph_copy_fails(self) -> None:
        copies = json.loads(POLICY_COPY.read_text(encoding="utf-8"))
        ignored_path = (
            "docs/90.references/research/2026-07-07-wer/ignored-structures.md"
        )
        short_path = "docs/90.references/research/2026-07-07-wer/short-copy.md"
        copied = copies["stage00"]["canonicalParagraph"]
        ignored = (
            f"# {copied}\n\n"
            f"```text\n{copied}\n```\n\n"
            f"<!-- {copied} -->\n\n"
            f"<pre>\n{copied}\n</pre>\n\n"
            f"| {copied} | Route |\n| --- | --- |\n\n"
            "- [Policy](../../../../00.agent-governance/README.md)\n"
            "- [Runbook](../../../../05.operations/runbooks/README.md)\n\n"
            f"> This file is generated; do not edit. {copied}\n\n"
            f"    {copied}\n"
        )
        short = "x" * 159
        root, contract, _owners, copies = self._duplicate_repository(
            extra_current_members={
                ignored_path: ignored,
                short_path: short + "\n",
            }
        )
        short_source = root / "docs/00.agent-governance/rules/short-policy.md"
        short_source.parent.mkdir(parents=True, exist_ok=True)
        short_source.write_text(short + "\n", encoding="utf-8")
        self._git_in(
            root,
            "add",
            "--",
            "docs/00.agent-governance/rules/short-policy.md",
        )
        for family in ("stage00", "policy", "runbook"):
            (root / copies[family]["referencePath"]).write_text(
                copies[family]["referenceParagraph"] + "\n", encoding="utf-8"
            )
            self._git_in(root, "add", "--", copies[family]["referencePath"])

        findings = ria.validate_duplicate_rules(root, contract)
        self.assertEqual(
            {finding.path for finding in findings},
            {
                copies["stage00"]["referencePath"],
                copies["policy"]["referencePath"],
                copies["runbook"]["referencePath"],
            },
        )
        self.assertEqual({finding.rule_id for finding in findings}, {"RIA-DUPLICATE"})
        self.assertNotIn(ignored_path, {finding.path for finding in findings})
        self.assertNotIn(short_path, {finding.path for finding in findings})

        list_path = "docs/90.references/audits/2026-07-11-weia/list-copy.md"
        source_prefix, source_suffix = copies["stage00"]["canonicalParagraph"].split(
            " retain", 1
        )
        reference_prefix, reference_suffix = copies["stage00"][
            "referenceParagraph"
        ].split(" retain", 1)
        root, contract, _owners, _copies = self._duplicate_repository(
            extra_current_members={
                list_path: (
                    "- This reference-only parent supplies unrelated dated analysis.\n"
                    f"  - {reference_prefix}\n"
                    f"    retain{reference_suffix}\n"
                    "  - This reference-only sibling records a different observation.\n"
                )
            }
        )
        list_source = root / "docs/00.agent-governance/rules/list-policy.md"
        list_source.write_text(
            "- This canonical-only parent supplies a different routing rule.\n"
            f"  - {source_prefix}\n"
            f"    retain{source_suffix}\n"
            "  - This canonical-only sibling records another policy rule.\n",
            encoding="utf-8",
        )
        self._git_in(
            root,
            "add",
            "--",
            "docs/00.agent-governance/rules/list-policy.md",
        )
        findings = ria.validate_duplicate_rules(root, contract)
        self.assertIn(list_path, {finding.path for finding in findings})
        diagnostics = "\n".join(
            f"{finding.rule_id} {finding.path} {finding.message}"
            for finding in findings
        )
        self.assertNotIn(copies["stage00"]["canonicalParagraph"], diagnostics)
        self.assertNotIn(copies["stage00"]["referenceParagraph"], diagnostics)

        started = time.monotonic()
        normalized = ria._markdown_visible_text("[" * 8_000 + "x" * 160)  # noqa: SLF001
        elapsed = time.monotonic() - started
        self.assertTrue(normalized.endswith("x" * 160))
        self.assertLess(elapsed, 1.0)

    def test_duplicate_parser_normalization_edges_fail_closed(self) -> None:
        copies = json.loads(POLICY_COPY.read_text(encoding="utf-8"))
        policy = copies["policy"]
        policy_reference = policy["referenceParagraph"]
        paths = {
            "html": "docs/90.references/audits/2026-07-11-weia/html-copy.md",
            "link-label": (
                "docs/90.references/audits/2026-07-11-weia/link-label-copy.md"
            ),
            "table-cell": (
                "docs/90.references/audits/2026-07-11-weia/table-cell-copy.md"
            ),
            "pipe-table": (
                "docs/90.references/audits/2026-07-11-weia/pipe-table-copy.md"
            ),
            "invisible": "docs/90.references/audits/2026-07-11-weia/invisible-copy.md",
            "blockquote-code": (
                "docs/90.references/audits/2026-07-11-weia/blockquote-code.md"
            ),
            "pure-links": "docs/90.references/audits/2026-07-11-weia/pure-links.md",
        }
        root, contract, _owners, _copies = self._duplicate_repository(
            extra_current_members={
                paths["html"]: f"<span>{policy_reference}</span>\n",
                paths["link-label"]: (
                    policy_reference.replace(
                        "documented rollback boundary",
                        "[documented **rollback** boundary](../rollback.md)",
                    )
                    + "\n"
                ),
                paths["table-cell"]: (
                    f"| Context | Copy |\n| --- | --- |\n"
                    f"| Route | {policy_reference} |\n"
                ),
                paths["pipe-table"]: (
                    f"Context | Copy\n--- | ---\nRoute | {policy_reference}\n"
                ),
                paths["invisible"]: (
                    policy_reference.replace("rollback", "roll\u200bback") + "\n"
                ),
                paths["blockquote-code"]: f">     {policy_reference}\n",
                paths["pure-links"]: (
                    "- [Policy][policy]\n"
                    "- [Guide](../folder/(nested)/guide.md)\n\n"
                    "[policy]: ../../../../05.operations/policies/README.md\n"
                ),
            }
        )

        findings = ria.validate_duplicate_rules(root, contract)
        finding_paths = {finding.path for finding in findings}
        self.assertTrue(
            {
                paths["html"],
                paths["link-label"],
                paths["table-cell"],
                paths["pipe-table"],
                paths["invisible"],
            }.issubset(finding_paths)
        )
        self.assertNotIn(paths["blockquote-code"], finding_paths)
        self.assertNotIn(paths["pure-links"], finding_paths)

        started = time.monotonic()
        paragraphs = ria._visible_paragraphs(  # noqa: SLF001
            ("[" * 32_000 + "x" * 160).encode("utf-8")
        )
        elapsed = time.monotonic() - started
        self.assertEqual(len(paragraphs), 1)
        self.assertLess(elapsed, 1.0)

        started = time.monotonic()
        ria._visible_paragraphs(("<" * 200_000).encode("utf-8"))  # noqa: SLF001
        self.assertLess(time.monotonic() - started, 1.0)
        self.assertNotEqual(
            ria._markdown_visible_text("\\a" * 160),  # noqa: SLF001
            ria._markdown_visible_text("a" * 160),  # noqa: SLF001
        )
        self.assertNotEqual(
            ria._markdown_visible_text("`*x*`" * 80),  # noqa: SLF001
            ria._markdown_visible_text("**x**" * 80),  # noqa: SLF001
        )

    def test_structural_exception_is_pair_scoped(self) -> None:
        copies = json.loads(POLICY_COPY.read_text(encoding="utf-8"))
        structural = copies["structural"]
        members = {
            structural["referencePath"]: structural["referenceParagraph"] + "\n",
            structural["secondReferencePath"]: "No copied structural text.\n",
        }
        root, contract, _owners, _copies = self._duplicate_repository(
            extra_current_members=members
        )
        source = root / structural["canonicalPath"]
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_text(structural["canonicalParagraph"] + "\n", encoding="utf-8")
        self._git_in(root, "add", "--", structural["canonicalPath"])
        exception = {
            "canonicalOwnerPath": structural["canonicalPath"],
            "referencePath": structural["referencePath"],
            "paragraphSha256": hashlib.sha256(
                structural["normalizedVisible"].encode("utf-8")
            ).hexdigest(),
            "structuralRole": "navigation",
            "reason": "Exact canonical-owner navigation repeated for routing",
        }
        contract["duplicateRules"]["structuralExceptions"] = [exception]
        self.assertEqual(ria.validate_duplicate_rules(root, contract), [])

        mutations = {
            "wrong-source": {
                **exception,
                "canonicalOwnerPath": "docs/00.agent-governance/README.md",
            },
            "wrong-destination": {
                **exception,
                "referencePath": structural["secondReferencePath"],
            },
            "wrong-digest": {**exception, "paragraphSha256": "b" * 64},
            "wrong-role": {**exception, "structuralRole": "prose"},
            "unknown-role": {**exception, "structuralRole": "unknown"},
            "blank-reason": {**exception, "reason": ""},
        }
        for name, mutation in mutations.items():
            with self.subTest(name=name):
                changed = json.loads(json.dumps(contract))
                changed["duplicateRules"]["structuralExceptions"] = [mutation]
                self.assertTrue(ria.validate_duplicate_rules(root, changed))

        duplicate = json.loads(json.dumps(contract))
        duplicate["duplicateRules"]["structuralExceptions"] = [exception, exception]
        self.assertTrue(ria.validate_duplicate_rules(root, duplicate))

        blanket = json.loads(json.dumps(contract))
        blanket["duplicateRules"]["paragraphSha256s"] = [
            exception["paragraphSha256"]
        ]
        self.assertTrue(ria.validate_duplicate_rules(root, blanket))

        (root / structural["referencePath"]).write_text(
            "No copied structural text.\n", encoding="utf-8"
        )
        self._git_in(root, "add", "--", structural["referencePath"])
        self.assertTrue(ria.validate_duplicate_rules(root, contract))

        (root / structural["referencePath"]).write_text(
            structural["referenceParagraph"] + "\n", encoding="utf-8"
        )
        (root / structural["secondReferencePath"]).write_text(
            structural["referenceParagraph"] + "\n", encoding="utf-8"
        )
        self._git_in(
            root,
            "add",
            "--",
            structural["referencePath"],
            structural["secondReferencePath"],
        )
        findings = ria.validate_duplicate_rules(root, contract)
        self.assertEqual(
            {finding.path for finding in findings},
            {structural["secondReferencePath"]},
        )

    def test_policy_parser_preserves_visible_structures(self) -> None:
        copies = json.loads(POLICY_COPY.read_text(encoding="utf-8"))
        paragraph = copies["policy"]["canonicalParagraph"]
        prefix, suffix = paragraph.split(" verification", 1)
        flat_item = f"- {paragraph}\n"
        continued_item = f"- {prefix}\n    verification{suffix}\n"
        quoted_continued_item = f"> - {prefix}\n>     verification{suffix}\n"
        ordinary_continuation = f"{prefix}\n    verification{suffix}\n"
        quoted_continuation = f"> {prefix}\n>     verification{suffix}\n"
        self.assertEqual(
            ria._visible_paragraphs(flat_item.encode()),  # noqa: SLF001
            ria._visible_paragraphs(continued_item.encode()),  # noqa: SLF001
        )
        self.assertEqual(
            ria._visible_paragraphs(flat_item.encode()),  # noqa: SLF001
            ria._visible_paragraphs(quoted_continued_item.encode()),  # noqa: SLF001
        )
        self.assertEqual(
            ria._visible_paragraphs((paragraph + "\n").encode()),  # noqa: SLF001
            ria._visible_paragraphs(ordinary_continuation.encode()),  # noqa: SLF001
        )
        self.assertEqual(
            ria._visible_paragraphs((paragraph + "\n").encode()),  # noqa: SLF001
            ria._visible_paragraphs(quoted_continuation.encode()),  # noqa: SLF001
        )
        self.assertEqual(
            ria._visible_paragraphs(f">     {paragraph}\n".encode()),  # noqa: SLF001
            (),
        )

        plain = ria._visible_paragraphs((paragraph + "\n").encode())  # noqa: SLF001
        self.assertEqual(
            ria._visible_paragraphs(  # noqa: SLF001
                f"<span>{paragraph}</span>\n".encode()
            ),
            plain,
        )
        for tag in (
            "script",
            "style",
            "pre",
            "textarea",
            "div",
            "section",
            "article",
        ):
            with self.subTest(raw_html=tag):
                self.assertEqual(
                    ria._visible_paragraphs(  # noqa: SLF001
                        f"<{tag}>\n{paragraph}\n</{tag}>\n".encode()
                    ),
                    (),
                )

        linked = paragraph.replace(
            "documented rollback boundary",
            "[documented **rollback** boundary]"
            "(https://example.invalid/policy_(current))",
        )
        self.assertEqual(
            ria._markdown_visible_text(linked),  # noqa: SLF001
            ria._markdown_visible_text(paragraph),  # noqa: SLF001
        )
        long_label = "Canonical owner navigation " + "route " * 35
        pure_navigation = (
            f"- [{long_label}][policy-owner]\n"
            f"- [{long_label}](https://example.invalid/a_(nested))\n"
            f"\n[policy-owner]: https://example.invalid/policy\n"
        )
        self.assertEqual(
            ria._visible_paragraphs(pure_navigation.encode()),  # noqa: SLF001
            (),
        )

        expected_cell = plain[0].digest
        for bordered in (False, True):
            with self.subTest(bordered=bordered):
                def row(first: str, second: str) -> str:
                    body = f"{first} | {second}"
                    return f"| {body} |" if bordered else body

                source_table = (
                    row("Policy", "Note")
                    + "\n"
                    + row("---", "---")
                    + "\n"
                    + row(
                        copies["policy"]["canonicalParagraph"],
                        "source-only sibling",
                    )
                    + "\n"
                )
                reference_table = (
                    row("Policy", "Note")
                    + "\n"
                    + row("---", "---")
                    + "\n"
                    + row(
                        copies["policy"]["referenceParagraph"],
                        "reference-only sibling",
                    )
                    + "\n"
                )
                source_digests = {
                    item.digest
                    for item in ria._visible_paragraphs(  # noqa: SLF001
                        source_table.encode()
                    )
                }
                reference_digests = {
                    item.digest
                    for item in ria._visible_paragraphs(  # noqa: SLF001
                        reference_table.encode()
                    )
                }
                self.assertIn(expected_cell, source_digests)
                self.assertIn(expected_cell, reference_digests)

        left = "leftword " * 14
        right = "rightword " * 13
        expected_pipe = ria._visible_paragraphs(  # noqa: SLF001
            f"{left}| {right}\n".encode()
        )[0].digest
        for separator in (r"\|", "`|`"):
            with self.subTest(table_separator=separator):
                table = (
                    "Policy | Note\n"
                    "--- | ---\n"
                    f"{left}{separator} {right} | short context\n"
                )
                self.assertIn(
                    expected_pipe,
                    {
                        item.digest
                        for item in ria._visible_paragraphs(  # noqa: SLF001
                            table.encode()
                        )
                    },
                )

        obfuscated = paragraph.replace("platform", "plat\u200bform")
        self.assertEqual(
            ria._markdown_visible_text(obfuscated),  # noqa: SLF001
            ria._markdown_visible_text(paragraph),  # noqa: SLF001
        )
        self.assertNotEqual(
            ria._markdown_visible_text(r"policy\name"),  # noqa: SLF001
            ria._markdown_visible_text("policyname"),  # noqa: SLF001
        )
        self.assertNotEqual(
            ria._markdown_visible_text("`**rollback**`"),  # noqa: SLF001
            ria._markdown_visible_text("**rollback**"),  # noqa: SLF001
        )

    def test_policy_parser_preserves_commonmark_line_boundaries(self) -> None:
        copies = json.loads(POLICY_COPY.read_text(encoding="utf-8"))
        paragraph = copies["policy"]["canonicalParagraph"]
        prefix, suffix = paragraph.split(" verification", 1)
        plain = ria._visible_paragraphs((paragraph + "\n").encode())  # noqa: SLF001

        for separator in ("\n", "  \n", "\\\n"):
            with self.subTest(line_break=repr(separator)):
                wrapped = f"{prefix}{separator}verification{suffix}\n"
                self.assertEqual(
                    ria._visible_paragraphs(wrapped.encode()),  # noqa: SLF001
                    plain,
                )
        for separated_container in (
            f"{prefix}\n>     verification{suffix}\n",
            f"> {prefix}\n    verification{suffix}\n",
        ):
            with self.subTest(container_boundary=separated_container[:8]):
                self.assertEqual(
                    ria._visible_paragraphs(  # noqa: SLF001
                        separated_container.encode()
                    ),
                    (),
                )

    def test_policy_parser_preserves_literal_emphasis_characters(self) -> None:
        self.assertEqual(
            ria._markdown_visible_text("policy_name"),  # noqa: SLF001
            ria._markdown_visible_text(r"policy\_name"),  # noqa: SLF001
        )
        self.assertEqual(
            ria._markdown_visible_text("policy*name"),  # noqa: SLF001
            ria._markdown_visible_text(r"policy\*name"),  # noqa: SLF001
        )
        self.assertEqual(
            ria._markdown_visible_text("*policy* **owner** ~~retired~~"),  # noqa: SLF001
            "policy owner retired",
        )
        self.assertEqual(
            ria._markdown_visible_text("policy~name"),  # noqa: SLF001
            "policy~name",
        )
        for source, expected in (
            ("*a**a*", "a**a"),
            ("*a***a*", "a*a"),
            ("**a*a**", "a*a"),
        ):
            with self.subTest(delimiter_rule=source):
                self.assertEqual(
                    ria._markdown_visible_text(source),  # noqa: SLF001
                    expected,
                )

    def test_policy_parser_keeps_emphasis_within_link_labels(self) -> None:
        for source, expected in (
            ("*[policy*](https://example.invalid/policy)", "*policy*"),
            ("[**_*](https://example.invalid/policy)", "**_*"),
            ("[*a_**](https://example.invalid/policy)", "a_*"),
        ):
            with self.subTest(source=source):
                self.assertEqual(
                    ria._markdown_visible_text(source),  # noqa: SLF001
                    expected,
                )

    def test_policy_parser_decodes_only_commonmark_character_references(
        self,
    ) -> None:
        self.assertEqual(
            ria._markdown_visible_text("&copy; &#169; &#xA9;"),  # noqa: SLF001
            "© © ©",
        )
        self.assertNotEqual(
            ria._markdown_visible_text("&copy &#169 &#xA9"),  # noqa: SLF001
            "© © ©",
        )
        self.assertEqual(
            ria._markdown_visible_text("`&amp;`"),  # noqa: SLF001
            ria._markdown_visible_text("&amp;amp;"),  # noqa: SLF001
        )

    def test_policy_parser_requires_resolved_reference_links(self) -> None:
        copies = json.loads(POLICY_COPY.read_text(encoding="utf-8"))
        paragraph = copies["policy"]["canonicalParagraph"]
        unresolved = f"- [{paragraph}]\n"
        missing_full = f"- [{paragraph}][missing]\n"
        missing_collapsed = f"- [{paragraph}][]\n"
        for document in (unresolved, missing_full, missing_collapsed):
            with self.subTest(unresolved=document[-12:]):
                self.assertTrue(
                    ria._visible_paragraphs(document.encode())  # noqa: SLF001
                )
        resolved = (
            f"- [{paragraph}][policy]\n\n"
            "[policy]: https://example.invalid/policy\n"
        )
        self.assertEqual(
            ria._visible_paragraphs(resolved.encode()),  # noqa: SLF001
            (),
        )
        for reference, definition in (
            (r"policy\]", r"policy\]"),
            ("p&p", "P&amp;P"),
        ):
            with self.subTest(resolved_reference=reference):
                document = (
                    f"- [{paragraph}][{reference}]\n\n"
                    f"[{definition}]: https://example.invalid/policy\n"
                )
                self.assertEqual(
                    ria._visible_paragraphs(document.encode()),  # noqa: SLF001
                    (),
                )
        fenced_definition = (
            f"- [{paragraph}][policy]\n\n"
            "```\n[policy]: https://example.invalid/policy\n```\n"
        )
        self.assertTrue(
            ria._visible_paragraphs(fenced_definition.encode())  # noqa: SLF001
        )

    def test_policy_parser_requires_complete_link_target_grammar(self) -> None:
        for link in (
            r"[policy](foo bar)",
            r"[policy](foo\ bar)",
            '[policy](foo "unterminated)',
        ):
            with self.subTest(invalid_inline_link=link):
                self.assertFalse(
                    ria._pure_link_list((link,), frozenset())  # noqa: SLF001
                )

        copies = json.loads(POLICY_COPY.read_text(encoding="utf-8"))
        paragraph = copies["policy"]["canonicalParagraph"]
        cases = (
            (
                "invalid-nested-destination",
                f"- [{paragraph}][policy]\n\n[policy]: foo(bar\n",
                True,
            ),
            (
                "valid-multiline-destination",
                (
                    f"- [{paragraph}][policy]\n\n"
                    "[policy]:\n  https://example.invalid/policy\n"
                ),
                False,
            ),
        )
        for name, document, visible in cases:
            with self.subTest(reference_definition=name):
                self.assertEqual(
                    bool(
                        ria._visible_paragraphs(  # noqa: SLF001
                            document.encode()
                        )
                    ),
                    visible,
                )

    def test_policy_parser_handles_quoted_html_and_email_autolinks(self) -> None:
        copies = json.loads(POLICY_COPY.read_text(encoding="utf-8"))
        paragraph = copies["policy"]["canonicalParagraph"]
        plain = ria._visible_paragraphs((paragraph + "\n").encode())  # noqa: SLF001
        self.assertEqual(
            ria._visible_paragraphs(  # noqa: SLF001
                f'<span title=">">{paragraph}</span>\n'.encode()
            ),
            plain,
        )
        self.assertEqual(
            ria._markdown_visible_text("<operator@example.com>"),  # noqa: SLF001
            "operator@example.com",
        )
        self.assertEqual(
            ria._markdown_visible_text("<o'connor@example.com>"),  # noqa: SLF001
            "o'connor@example.com",
        )
        self.assertEqual(
            ria._markdown_visible_text(  # noqa: SLF001
                "<https://example.invalid/operator's-guide>"
            ),
            "https://example.invalid/operator's-guide",
        )
        self.assertEqual(
            ria._markdown_visible_text(  # noqa: SLF001
                "[operator@example.com](mailto:operator@example.com)"
            ),
            "operator@example.com",
        )

    def test_policy_parser_preserves_fence_and_raw_html_boundaries(self) -> None:
        copies = json.loads(POLICY_COPY.read_text(encoding="utf-8"))
        paragraph = copies["policy"]["canonicalParagraph"]
        invalid_close = f"```\nignored\n``` trailing\n{paragraph}\n"
        self.assertEqual(
            ria._visible_paragraphs(invalid_close.encode()),  # noqa: SLF001
            (),
        )
        self.assertEqual(
            ria._visible_paragraphs(  # noqa: SLF001
                f"<!--\n-->{paragraph}\n".encode()
            ),
            (),
        )
        self.assertEqual(
            ria._markdown_visible_text(  # noqa: SLF001
                ria._mask_markdown_comments("visible <!-- hidden --> text")
            ),
            "visible text",
        )
        for raw_block in (
            f"<?target\n{paragraph}\n?>\n",
            f"<!DECLARATION\n{paragraph}\n>\n",
            f"<![CDATA[\n{paragraph}\n]]>\n",
            f"<span>\n{paragraph}\n</span>\n",
            f"<custom-element>\n{paragraph}\n</custom-element>\n",
        ):
            with self.subTest(raw_block=raw_block.splitlines()[0]):
                self.assertEqual(
                    ria._visible_paragraphs(raw_block.encode()),  # noqa: SLF001
                    (),
                )

    def test_policy_parser_rejects_backticks_in_fence_info(self) -> None:
        copies = json.loads(POLICY_COPY.read_text(encoding="utf-8"))
        paragraph = copies["policy"]["canonicalParagraph"]
        document = (
            "``` invalid`\n"
            "```\n"
            "[policy]: https://example.invalid/policy\n"
            "```\n"
            f"- [{paragraph}][policy]\n"
            "```\n"
        )
        self.assertTrue(
            ria._visible_paragraphs(document.encode())  # noqa: SLF001
        )

    def test_policy_parser_preserves_comment_literals_in_code_spans(self) -> None:
        masked = ria._mask_markdown_comments(  # noqa: SLF001
            "`<!-- visible policy literal -->`"
        )
        self.assertEqual(
            ria._markdown_visible_text(masked),  # noqa: SLF001
            "<!-- visible policy literal -->",
        )

    def test_policy_parser_does_not_pair_links_across_code_spans(self) -> None:
        manufactured_link = "[policy `](u`)"
        self.assertFalse(
            ria._pure_link_list(  # noqa: SLF001
                (manufactured_link,),
                frozenset(),
            )
        )

    def test_policy_parser_comments_respect_code_blocks(self) -> None:
        copies = json.loads(POLICY_COPY.read_text(encoding="utf-8"))
        paragraph = copies["policy"]["canonicalParagraph"]
        documents = (
            ("tilde-fence", f"~~~\n<!--\n~~~\n{paragraph}\n"),
            ("indented-code", f"    <!--\n\n{paragraph}\n"),
        )
        for name, document in documents:
            with self.subTest(code_block=name):
                self.assertTrue(
                    ria._visible_paragraphs(  # noqa: SLF001
                        document.encode()
                    )
                )

        self.assertEqual(
            ria._visible_paragraphs(  # noqa: SLF001
                f"<!--\n-->{paragraph}\n".encode()
            ),
            (),
        )

    def test_policy_parser_uses_commonmark_line_and_space_rules(self) -> None:
        copies = json.loads(POLICY_COPY.read_text(encoding="utf-8"))
        paragraph = copies["policy"]["canonicalParagraph"]
        non_line_endings = (
            "\v",
            "\f",
            "\x1c",
            "\x1d",
            "\x1e",
            "\x85",
            "\u2028",
            "\u2029",
        )
        for separator in non_line_endings:
            with self.subTest(non_line_ending=hex(ord(separator))):
                document = (
                    f"- [{paragraph}][policy]{separator}{separator}"
                    "[policy]: https://example.invalid/policy\n"
                )
                self.assertTrue(
                    ria._visible_paragraphs(  # noqa: SLF001
                        document.encode()
                    )
                )

        non_link_whitespace = ("\v", "\f", "\x1c", "\x1d", "\x1e")
        for separator in non_link_whitespace:
            with self.subTest(non_link_whitespace=hex(ord(separator))):
                self.assertFalse(
                    ria._pure_link_list(  # noqa: SLF001
                        (f'[policy](target{separator}"title")',),
                        frozenset(),
                    )
                )

    def test_policy_parser_rejects_nested_reference_labels(self) -> None:
        with self.subTest(surface="definition"):
            self.assertIsNone(
                ria._parse_reference_definition("[a[b]]: u")  # noqa: SLF001
            )
        with self.subTest(surface="reference-suffix"):
            self.assertFalse(
                ria._pure_link_list(  # noqa: SLF001
                    ("[policy][a[b]]",),
                    frozenset({"a[b]"}),
                )
            )

        self.assertEqual(
            ria._parse_reference_definition(  # noqa: SLF001
                r"[a\[b\]]: u"
            ),
            "a[b]",
        )
        self.assertTrue(
            ria._pure_link_list(  # noqa: SLF001
                (r"[policy][a\[b\]]",),
                frozenset({"a[b]"}),
            )
        )

    def test_policy_parser_does_not_pair_links_across_opaque_tokens(
        self,
    ) -> None:
        manufactured_links = (
            '[policy <span title="](u">)',
            "[policy <https://example.invalid/](u>)",
        )
        for source in manufactured_links:
            with self.subTest(source=source):
                self.assertFalse(
                    ria._pure_link_list((source,), frozenset())  # noqa: SLF001
                )

    def test_policy_parser_comments_respect_list_code_blocks(self) -> None:
        copies = json.loads(POLICY_COPY.read_text(encoding="utf-8"))
        paragraph = copies["policy"]["canonicalParagraph"]
        documents = (
            ("unordered-tilde", f"- ~~~\n  <!--\n  ~~~\n\n{paragraph}\n"),
            ("unordered-backtick", f"- ```\n  <!--\n  ```\n\n{paragraph}\n"),
            ("unordered-indented", f"- item\n\n      <!--\n\n{paragraph}\n"),
            ("ordered-tilde", f"1. ~~~\n   <!--\n   ~~~\n\n{paragraph}\n"),
            ("ordered-backtick", f"1. ```\n   <!--\n   ```\n\n{paragraph}\n"),
            ("ordered-indented", f"1. item\n\n       <!--\n\n{paragraph}\n"),
            (
                "quote-list-tilde",
                f"> - ~~~\n>   <!--\n>   ~~~\n\n{paragraph}\n",
            ),
            (
                "quote-list-backtick",
                f"> - ```\n>   <!--\n>   ```\n\n{paragraph}\n",
            ),
            (
                "quote-list-indented",
                f"> - item\n>\n>       <!--\n\n{paragraph}\n",
            ),
        )
        for name, document in documents:
            with self.subTest(list_code=name):
                self.assertTrue(
                    ria._visible_paragraphs(  # noqa: SLF001
                        document.encode()
                    )
                )

    def test_policy_parser_preserves_invalid_inline_comments(self) -> None:
        copies = json.loads(POLICY_COPY.read_text(encoding="utf-8"))
        paragraph = copies["policy"]["canonicalParagraph"]
        invalid_inline = (
            f"prefix <!-- unclosed {paragraph}\n",
            f"prefix <!-- invalid -- {paragraph} -->\n",
            f"prefix <!-- invalid {paragraph}--->\n",
        )
        for document in invalid_inline:
            with self.subTest(invalid_inline=document[:32]):
                self.assertTrue(
                    ria._visible_paragraphs(  # noqa: SLF001
                        document.encode()
                    )
                )

        self.assertEqual(
            ria._visible_paragraphs(  # noqa: SLF001
                f"prefix <!-- {paragraph} --> tail\n".encode()
            ),
            (),
        )
        self.assertEqual(
            ria._visible_paragraphs(  # noqa: SLF001
                f"<!--\n{paragraph}\n".encode()
            ),
            (),
        )

    def test_policy_parser_excludes_only_single_non_image_links(self) -> None:
        copies = json.loads(POLICY_COPY.read_text(encoding="utf-8"))
        paragraph = copies["policy"]["canonicalParagraph"]
        cases = (
            ("image", f"![{paragraph}](https://example.invalid/image)"),
            ("nested", "[outer [inner](https://example.invalid/i)](u)"),
            ("multiple", "[one](u), [two](v)"),
        )
        for name, source in cases:
            with self.subTest(non_navigation=name):
                self.assertFalse(
                    ria._pure_link_list((source,), frozenset())  # noqa: SLF001
                )

        self.assertTrue(
            ria._visible_paragraphs(  # noqa: SLF001
                f"- ![{paragraph}](https://example.invalid/image)\n".encode()
            )
        )
        self.assertTrue(
            ria._pure_link_list(  # noqa: SLF001
                ("[policy](https://example.invalid/policy)",),
                frozenset(),
            )
        )

    def test_policy_parser_removes_only_curated_format_controls(self) -> None:
        removable = (
            "\u061c",
            "\u200e",
            "\u202a",
            "\u202e",
            "\u2061",
            "\u2063",
            "\u2066",
            "\u2069",
            "\U000e0001",
        )
        for control in removable:
            with self.subTest(removable=hex(ord(control))):
                self.assertEqual(
                    ria._markdown_visible_text(  # noqa: SLF001
                        f"roll{control}back"
                    ),
                    "rollback",
                )

        for significant in ("\u200c", "\u200d"):
            with self.subTest(significant=hex(ord(significant))):
                self.assertNotEqual(
                    ria._markdown_visible_text(  # noqa: SLF001
                        f"roll{significant}back"
                    ),
                    "rollback",
                )
        self.assertNotEqual(
            ria._markdown_visible_text("❤\ufe0f"),  # noqa: SLF001
            ria._markdown_visible_text("❤"),  # noqa: SLF001
        )

    def test_policy_parser_applies_ordered_list_interruption_rules(self) -> None:
        first = "policy ownership remains explicit " * 3
        continuation = "continued verification remains reviewable " * 3
        self.assertGreater(len(first + continuation), 160)
        self.assertTrue(
            ria._visible_paragraphs(  # noqa: SLF001
                f"{first}\n2. {continuation}\n".encode()
            )
        )
        self.assertEqual(
            ria._visible_paragraphs(  # noqa: SLF001
                f"{first}\n1. {continuation}\n".encode()
            ),
            (),
        )

        copies = json.loads(POLICY_COPY.read_text(encoding="utf-8"))
        paragraph = copies["policy"]["canonicalParagraph"]
        self.assertTrue(
            ria._visible_paragraphs(  # noqa: SLF001
                f"short\n\n2. {paragraph}\n".encode()
            )
        )

    def test_angle_token_storage_is_compact_at_blob_boundary(self) -> None:
        token_count = 450_000
        payload = "<i>x" * token_count
        payload += "x" * (ria.MAX_BLOB_BYTES - len(payload))
        self.assertEqual(len(payload), ria.MAX_BLOB_BYTES)

        tracemalloc.start()
        started = time.monotonic()
        try:
            tokens = ria._inline_angle_tokens(payload)  # noqa: SLF001
            intervals = ria._inline_opaque_intervals(  # noqa: SLF001
                payload,
                angle_tokens=tokens,
            )
            _current, peak = tracemalloc.get_traced_memory()
        finally:
            tracemalloc.stop()
        elapsed = time.monotonic() - started

        self.assertEqual(len(tokens), token_count)
        self.assertEqual(len(intervals), token_count)
        self.assertLess(peak, 48_000_000)
        self.assertLess(elapsed, 12.0)

    def test_policy_parser_preserves_zero_width_inline_comment_semantics(
        self,
    ) -> None:
        self.assertEqual(
            ria._markdown_visible_text(  # noqa: SLF001
                ria._mask_markdown_comments(  # noqa: SLF001
                    "roll<!-- hidden -->back"
                )
            ),
            "rollback",
        )
        for source in (
            "roll <!-- hidden -->back",
            "roll<!-- hidden --> back",
            "roll <!-- hidden --> back",
        ):
            with self.subTest(source=source):
                self.assertEqual(
                    ria._markdown_visible_text(  # noqa: SLF001
                        ria._mask_markdown_comments(source)  # noqa: SLF001
                    ),
                    "roll back",
                )

    def test_policy_parser_preserves_multiline_zero_width_comment_semantics(
        self,
    ) -> None:
        self.assertEqual(
            ria._markdown_visible_text(  # noqa: SLF001
                ria._mask_markdown_comments(  # noqa: SLF001
                    "roll<!--\n-->back"
                )
            ),
            "rollback",
        )
        self.assertEqual(
            ria._markdown_visible_text(  # noqa: SLF001
                ria._mask_markdown_comments(  # noqa: SLF001
                    "roll <!--\n--> back"
                )
            ),
            "roll back",
        )

        copies = json.loads(POLICY_COPY.read_text(encoding="utf-8"))
        paragraph = copies["policy"]["canonicalParagraph"]
        commented = paragraph.replace("rollback", "roll<!--\n-->back")
        plain_digest = ria._visible_paragraphs(  # noqa: SLF001
            (paragraph + "\n").encode("utf-8")
        )
        self.assertEqual(
            ria._visible_paragraphs(  # noqa: SLF001
                (commented + "\n").encode("utf-8")
            ),
            plain_digest,
        )

        block_comment = f"<!--\n{paragraph}\n-->\n{paragraph}\n"
        self.assertEqual(
            ria._visible_paragraphs(  # noqa: SLF001
                block_comment.encode("utf-8")
            ),
            plain_digest,
        )

    def test_policy_parser_preserves_noninterrupting_ordered_marker_text(
        self,
    ) -> None:
        copies = json.loads(POLICY_COPY.read_text(encoding="utf-8"))
        paragraph = copies["policy"]["canonicalParagraph"]
        document = f"This context remains in the open paragraph.\n2. {paragraph}\n"
        visible = ria._markdown_visible_text(document.rstrip("\n"))  # noqa: SLF001
        expected = ria.VisibleParagraph(
            hashlib.sha256(visible.encode("utf-8")).hexdigest(),
            "prose",
        )
        self.assertEqual(
            ria._visible_paragraphs(document.encode("utf-8")),  # noqa: SLF001
            (expected,),
        )

    def test_policy_parser_hides_multiline_reference_titles(self) -> None:
        copies = json.loads(POLICY_COPY.read_text(encoding="utf-8"))
        paragraph = copies["policy"]["canonicalParagraph"]
        title = "t" * 180
        valid = (
            f"- [{paragraph}][policy]\n\n"
            "[policy]: https://example.invalid/policy\n"
            f'  "{title}"\n'
        )
        self.assertEqual(
            ria._visible_paragraphs(valid.encode("utf-8")),  # noqa: SLF001
            (),
        )
        for malformed_title in (
            f'  "{title}\n',
            f"  '{title}\"\n",
        ):
            with self.subTest(malformed_title=malformed_title[-4:]):
                malformed = (
                    f"- [{paragraph}][policy]\n\n"
                    "[policy]: https://example.invalid/policy\n"
                    + malformed_title
                )
                self.assertTrue(
                    ria._visible_paragraphs(  # noqa: SLF001
                        malformed.encode("utf-8")
                    )
                )

    def test_backtick_run_storage_is_compact_at_blob_boundary(self) -> None:
        token_count = 1_000_000
        payload = "`x" * token_count
        self.assertEqual(len(payload), ria.MAX_BLOB_BYTES)

        tracemalloc.start()
        started = time.monotonic()
        try:
            run_lengths, next_backtick = ria._backtick_runs(  # noqa: SLF001
                payload
            )
            _current, peak = tracemalloc.get_traced_memory()
        finally:
            tracemalloc.stop()
        elapsed = time.monotonic() - started

        middle = token_count
        last = len(payload) - 2
        self.assertEqual(len(run_lengths), token_count)
        self.assertEqual(run_lengths.get(0), 1)
        self.assertEqual(run_lengths.get(middle), 1)
        self.assertEqual(run_lengths.get(last), 1)
        self.assertEqual(next_backtick.get(0), 2)
        self.assertEqual(next_backtick.get(middle), middle + 2)
        self.assertIsNone(next_backtick.get(last))
        self.assertLess(peak, 48_000_000)
        self.assertNotIsInstance(run_lengths, dict)
        self.assertNotIsInstance(next_backtick, dict)
        self.assertLess(elapsed, 12.0)

    def test_policy_parser_preserves_joiner_semantics(self) -> None:
        self.assertEqual(
            ria._markdown_visible_text("roll\u200bback"),  # noqa: SLF001
            ria._markdown_visible_text("rollback"),  # noqa: SLF001
        )
        self.assertNotEqual(
            ria._markdown_visible_text("👩\u200d💻"),  # noqa: SLF001
            ria._markdown_visible_text("👩💻"),  # noqa: SLF001
        )

    def test_policy_parser_and_duplicate_matching_are_bounded(self) -> None:
        copies = json.loads(POLICY_COPY.read_text(encoding="utf-8"))
        paragraph = copies["policy"]["canonicalParagraph"]

        class CountingString(str):
            find_calls = 0

            def find(
                self,
                sub: str,
                start: int = 0,
                end: int | None = None,
            ) -> int:
                self.find_calls += 1
                return super().find(
                    sub,
                    start,
                    len(self) if end is None else end,
                )

        counted_angles = CountingString("<a" * 2_048 + ">" + paragraph)
        ria._markdown_visible_text(counted_angles)  # noqa: SLF001
        self.assertLessEqual(counted_angles.find_calls, 1)

        counted_ticks = CountingString("`" * 2_048 + paragraph)
        ria._markdown_visible_text(counted_ticks)  # noqa: SLF001
        self.assertLessEqual(counted_ticks.find_calls, 1)

        started = time.monotonic()
        ria._markdown_visible_text("*_*_" * 30_000)  # noqa: SLF001
        self.assertLess(time.monotonic() - started, 1.5)

        deeply_nested_label = "[" * 1_200 + paragraph + "]" * 1_200
        normalized_nested = ria._markdown_visible_text(  # noqa: SLF001
            deeply_nested_label
        )
        self.assertEqual(normalized_nested.count("["), 1_200)
        self.assertEqual(normalized_nested.count("]"), 1_200)
        self.assertIn(
            ria._markdown_visible_text(paragraph),  # noqa: SLF001
            normalized_nested,
        )

        started = time.monotonic()
        bracket_paragraphs = ria._visible_paragraphs(  # noqa: SLF001
            ("[" * 32_000 + paragraph).encode()
        )
        bracket_elapsed = time.monotonic() - started
        self.assertTrue(bracket_paragraphs)
        self.assertLess(bracket_elapsed, 1.0)

        started = time.monotonic()
        angle_paragraphs = ria._visible_paragraphs(  # noqa: SLF001
            ("<" * 1_000_000 + paragraph).encode()
        )
        angle_elapsed = time.monotonic() - started
        self.assertTrue(angle_paragraphs)
        self.assertLess(angle_elapsed, 4.0)

        started = time.monotonic()
        shared_closer = ria._visible_paragraphs(  # noqa: SLF001
            (("<a" * 320_000) + ">" + paragraph).encode()
        )
        shared_closer_elapsed = time.monotonic() - started
        self.assertTrue(shared_closer)
        self.assertLess(shared_closer_elapsed, 2.0)

        root, contract, _owners, copies = self._duplicate_repository()
        repetitions = 350
        source_path = root / copies["stage00"]["canonicalPath"]
        source_path.write_text(
            (copies["stage00"]["canonicalParagraph"] + "\n\n") * repetitions,
            encoding="utf-8",
        )
        reference_path = root / copies["stage00"]["referencePath"]
        reference_path.write_text(
            (copies["stage00"]["referenceParagraph"] + "\n\n") * repetitions,
            encoding="utf-8",
        )
        self._git_in(
            root,
            "add",
            "--",
            copies["stage00"]["canonicalPath"],
            copies["stage00"]["referencePath"],
        )
        started = time.monotonic()
        findings = ria.validate_duplicate_rules(root, contract)
        duplicate_elapsed = time.monotonic() - started
        self.assertIn(
            copies["stage00"]["referencePath"],
            {finding.path for finding in findings},
        )
        self.assertLess(duplicate_elapsed, 1.5)

    def test_emphasis_storage_is_compact_at_blob_boundary(self) -> None:
        marker_count = 400_000
        payload = "*a" * marker_count
        payload += "x" * (ria.MAX_BLOB_BYTES - len(payload))
        self.assertEqual(len(payload), ria.MAX_BLOB_BYTES)

        started = time.monotonic()
        mask = ria._emphasis_marker_positions(  # noqa: SLF001
            payload,
            reference_labels=frozenset(),
            square_pairs={},
            parenthesis_pairs={},
            angle_closers={},
            autolink_closers={},
            run_lengths={},
            next_backtick={},
        )
        elapsed = time.monotonic() - started
        self.assertIsInstance(mask, bytearray)
        self.assertEqual(len(mask), len(payload))
        self.assertEqual(sum(mask), marker_count)
        self.assertFalse(hasattr(ria, "_EmphasisDelimiter"))
        self.assertLess(elapsed, 8.0)

    def test_data_asset_text_fields_reject_controls_and_preserve_unicode(
        self,
    ) -> None:
        self._write_source_evidence(tracked=True)
        representative_controls = (
            "\0",
            "\t",
            "\n",
            "\r",
            "\x1f",
            "\x7f",
            "\x80",
        )
        for field in ("refreshTrigger", "adoptedScope", "rejectedScope"):
            for control in representative_controls:
                with self.subTest(field=field, codepoint=ord(control)):
                    contract = self._source_contract()
                    asset = contract["dataAssets"][0]
                    if field == "refreshTrigger":
                        asset[field] = f"before{control}after"
                    else:
                        asset["sources"][0][field] = [f"before{control}after"]
                    findings = ria.validate_data_assets(self.root, contract)
                    self.assertEqual(
                        {finding.rule_id for finding in findings},
                        {"RIA-SOURCE"},
                    )
                    self.assertNotIn(f"before{control}after", repr(findings))

        for codepoint in (*range(0x20), *range(0x7F, 0xA0)):
            with self.subTest(predicate_codepoint=codepoint):
                self.assertFalse(
                    ria._closed_single_line_text(  # noqa: SLF001
                        f"before{chr(codepoint)}after"
                    )
                )
        self.assertTrue(
            ria._closed_single_line_text("정상적인 한국어 범위")  # noqa: SLF001
        )

        contract = self._source_contract()
        asset = contract["dataAssets"][0]
        asset["refreshTrigger"] = "저장소 또는 공식 소스 범위 변경"
        asset["sources"][0]["adoptedScope"] = ["채택한 정상 범위"]
        asset["sources"][0]["rejectedScope"] = ["제외한 정상 범위"]
        self.assertEqual(ria.validate_data_assets(self.root, contract), [])

    def test_production_source_ledger_covers_each_tracked_data_asset(self) -> None:
        contract = ria._decode_json_bytes(  # noqa: SLF001
            (REPOSITORY_ROOT / ria.DEFAULT_CONTRACT_PATH).read_bytes(),
            field=ria.DEFAULT_CONTRACT_PATH.as_posix(),
        )
        listed = self._git_in(
            REPOSITORY_ROOT,
            "ls-files",
            "-z",
            "--",
            "docs/90.references/data",
        ).split(b"\0")
        expected = {
            path.decode("utf-8")
            for path in listed
            if path and path != b"docs/90.references/data/README.md"
        }
        observed: set[str] = set()
        for asset in contract["dataAssets"]:
            evidence = asset["repositoryEvidence"]
            self.assertEqual(len(evidence), 1)
            observed.add(evidence[0])
        self.assertEqual(observed, expected)

        contract["dataAssets"] = [
            asset
            for asset in contract["dataAssets"]
            if asset["id"] != "tech-stack-version-inventory"
        ]
        findings = ria.validate_data_assets(REPOSITORY_ROOT, contract)
        self.assertEqual({finding.rule_id for finding in findings}, {"RIA-SOURCE"})

        contract = ria._decode_json_bytes(  # noqa: SLF001
            (REPOSITORY_ROOT / ria.DEFAULT_CONTRACT_PATH).read_bytes(),
            field=ria.DEFAULT_CONTRACT_PATH.as_posix(),
        )
        contract["dataAssets"][0]["repositoryEvidence"].append(
            "docs/90.references/README.md"
        )
        findings = ria.validate_data_assets(REPOSITORY_ROOT, contract)
        self.assertEqual({finding.rule_id for finding in findings}, {"RIA-SOURCE"})

    def test_data_asset_inventory_records_are_closed_and_bounded(self) -> None:
        oid = b"a" * 40
        valid_index = (
            b"100644 "
            + oid
            + b" 0\tdocs/90.references/data/asset.json\0"
        )
        valid_tree = (
            b"100644 blob "
            + oid
            + b"\tdocs/90.references/data/asset.json\0"
        )
        self.assertEqual(
            ria._parse_index_listing(valid_index),  # noqa: SLF001
            (Path("docs/90.references/data/asset.json"),),
        )
        self.assertEqual(
            ria._parse_tree_listing(valid_tree),  # noqa: SLF001
            (Path("docs/90.references/data/asset.json"),),
        )
        hostile_index = (
            valid_index.removesuffix(b"\0"),
            b"not-an-index-record\0",
            b"120000 " + oid + b" 0\tdocs/90.references/data/asset.json\0",
            b"100644 " + oid + b" 2\tdocs/90.references/data/asset.json\0",
            valid_index + valid_index,
            b"100644 " + oid + b" 0\tdocs/90.references/outside.json\0",
        )
        for payload in hostile_index:
            with self.subTest(kind="index", payload=payload[:16]):
                with self.assertRaises(ria._GitError):  # noqa: SLF001
                    ria._parse_index_listing(payload)  # noqa: SLF001
        hostile_tree = (
            valid_tree.removesuffix(b"\0"),
            b"not-a-tree-record\0",
            b"120000 blob " + oid + b"\tdocs/90.references/data/asset.json\0",
            b"100644 tree " + oid + b"\tdocs/90.references/data/asset.json\0",
            valid_tree + valid_tree,
            b"100644 blob " + oid + b"\tdocs/90.references/outside.json\0",
        )
        for payload in hostile_tree:
            with self.subTest(kind="tree", payload=payload[:16]):
                with self.assertRaises(ria._GitError):  # noqa: SLF001
                    ria._parse_tree_listing(payload)  # noqa: SLF001
        self.assertTrue(
            ria._git_arguments_allowed(  # noqa: SLF001
                (
                    "ls-tree",
                    "-rz",
                    "--full-tree",
                    "a" * 40,
                    "--",
                    "docs/90.references/data",
                )
            )
        )
        self.assertFalse(
            ria._git_arguments_allowed(  # noqa: SLF001
                (
                    "ls-tree",
                    "-rz",
                    "--full-tree",
                    "a" * 40,
                    "--",
                    "docs/90.references/research",
                )
            )
        )

        calls: list[tuple[str, ...]] = []

        def index_runner(
            root: Path, arguments: tuple[str, ...], limit: int
        ) -> bytes:
            del root, limit
            calls.append(arguments)
            return valid_index

        self.assertEqual(
            ria._tracked_data_asset_paths(  # noqa: SLF001
                self.root, commit_oid=None, runner=index_runner
            ),
            {Path("docs/90.references/data/asset.json")},
        )
        self.assertEqual(
            calls,
            [("ls-files", "-z", "--stage", "--", "docs/90.references/data")],
        )

        calls.clear()

        def tree_runner(
            root: Path, arguments: tuple[str, ...], limit: int
        ) -> bytes:
            del root, limit
            calls.append(arguments)
            if arguments == ("cat-file", "-t", "a" * 40):
                return b"commit\n"
            return valid_tree

        self.assertEqual(
            ria._tracked_data_asset_paths(  # noqa: SLF001
                self.root, commit_oid="a" * 40, runner=tree_runner
            ),
            {Path("docs/90.references/data/asset.json")},
        )
        self.assertEqual(
            calls,
            [
                ("cat-file", "-t", "a" * 40),
                (
                    "ls-tree",
                    "-rz",
                    "--full-tree",
                    "a" * 40,
                    "--",
                    "docs/90.references/data",
                ),
            ],
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
        self.assertEqual(non_git.returncode, 2)
        self.assertIn("RIA-CONTRACT", non_git.stderr)

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

    def test_literal_replacement_projection_is_exact_and_directional(
        self,
    ) -> None:
        projection = {
            "path": (
                "docs/90.references/research/2026-07-07-wer/"
                "automation-pipeline-workflow-qa.md"
            ),
            "literalReplacements": [
                {
                    "from": ".github/ABOUT.md",
                    "to": ".github/README.md",
                    "count": 2,
                }
            ],
        }
        path = Path(projection["path"])
        baseline = b".github/ABOUT.md and .github/ABOUT.md\n"
        proposed = b".github/README.md and .github/README.md\n"
        self.assertEqual(
            ria._projection_mask(  # noqa: SLF001
                baseline,
                path,
                projection,
                state="baseline",
            ),
            ria._projection_mask(  # noqa: SLF001
                proposed,
                path,
                projection,
                state="proposed",
            ),
        )
        for payload, state in (
            (baseline, "proposed"),
            (proposed, "baseline"),
            (b".github/ABOUT.md and .github/README.md\n", "either"),
            (b".github/README.md\n", "proposed"),
        ):
            with self.subTest(payload=payload, state=state):
                with self.assertRaises(ria._GitError):  # noqa: SLF001
                    ria._projection_mask(  # noqa: SLF001
                        payload,
                        path,
                        projection,
                        state=state,
                    )

    def test_agent_cutover_projection_authority_is_fully_pinned(self) -> None:
        projections = ria.load_agent_cutover_projections(
            REPOSITORY_ROOT,
            None,
        )
        self.assertEqual(
            tuple(path.as_posix() for path in projections),
            tuple(
                path
                for path, _count in ria.AGENT_CUTOVER_CURRENT_PATH_COUNTS
            ),
        )
        for digest_name in (
            "AGENT_LEGACY_CUTOVER_SHA256",
            "AGENT_LEGACY_CUTOVER_SCHEMA_SHA256",
        ):
            with self.subTest(digest_name=digest_name):
                with mock.patch.object(
                    ria,
                    digest_name,
                    "0" * 64,
                ):
                    with self.assertRaises(ria._GitError):  # noqa: SLF001
                        ria.load_agent_cutover_projections(
                            REPOSITORY_ROOT,
                            None,
                        )

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

    def test_selected_contract_controls_settlement_staged_and_explicit_paths(
        self,
    ) -> None:
        selected = Path(
            "docs/alternate/reference-information-architecture.json"
        )
        c2 = "b" * 40
        c3 = "c" * 40
        target = b"settled target"
        contract = self._settled_contract("git-sha1:" + c2, target)
        open_contract = self._minimal_contract()
        open_contract["baselineTransitions"] = [self._transition(target)]
        audit = ria.Pack("audits/2026-07-11-weia", ("done",), ())
        research = ria.Pack(
            "research/2026-07-07-wer",
            ("active", "accepted"),
            ("document-migration-evidence-ledger.md",),
        )
        registry = ria.RegistryProjection(
            "content/reference", (audit, research)
        )
        target_path = research.member_paths[0]
        context = ria.ValidationContext(
            registry,
            {target_path: target},
            {ROOT_BASELINE: registry, "git-sha1:" + c2: registry},
            {},
            {
                ROOT_BASELINE: ROOT_BASELINE.removeprefix("git-sha1:"),
                "git-sha1:" + c2: c2,
            },
            None,
        )
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
            (c2, selected): json.dumps(
                open_contract, separators=(",", ":")
            ).encode(),
            (c2, ria.REGISTRY_PATH): registry_payload,
            (c2, target_path): target,
            (
                ROOT_BASELINE.removeprefix("git-sha1:"),
                target_path,
            ): b"root target",
        }
        for path in (audit.readme_path, research.readme_path):
            payload = f"same:{path.as_posix()}".encode()
            payloads[(c2, path)] = payload
            payloads[
                (ROOT_BASELINE.removeprefix("git-sha1:"), path)
            ] = payload

        def commit_path(
            root: Path,
            commit_oid: str,
            path: Path,
            runner,
        ) -> bytes:
            del root, runner
            return payloads[(commit_oid, path)]

        with (
            mock.patch.object(
                ria, "_read_commit_path", side_effect=commit_path
            ) as reader,
            mock.patch.object(ria, "_validate_schema_at_commit") as schema,
        ):
            self.assertEqual(
                ria._settlement_proof(  # noqa: SLF001
                    self.root,
                    contract,
                    context,
                    None,
                    contract_path=selected,
                ),
                [],
            )
        self.assertIn(
            mock.call(self.root, c2, selected, None),
            reader.call_args_list,
        )
        schema.assert_called_once_with(
            self.root,
            c2,
            open_contract,
            selected,
            None,
        )

        selected_row = f"M\0{selected.as_posix()}\0".encode()
        default_row = (
            f"M\0{ria.DEFAULT_CONTRACT_PATH.as_posix()}\0".encode()
        )

        def staged_runner(rows: bytes):
            def runner(
                root: Path, arguments: tuple[str, ...], limit: int
            ) -> bytes:
                del root, limit
                if arguments == ("rev-parse", "--verify", "HEAD"):
                    return f"{c2}\n".encode()
                if arguments == ("cat-file", "-t", c2):
                    return b"commit\n"
                if arguments[0] == "diff-index":
                    return rows
                raise AssertionError(arguments)

            return runner

        def explicit_runner(rows: bytes):
            def runner(
                root: Path, arguments: tuple[str, ...], limit: int
            ) -> bytes:
                del root, limit
                if arguments == ("cat-file", "-t", c3):
                    return b"commit\n"
                if arguments == ("cat-file", "commit", c3):
                    return (
                        f"tree {'d' * 40}\nparent {c2}\n\nmessage\n"
                    ).encode()
                if arguments[0] == "diff-tree":
                    return rows
                raise AssertionError(arguments)

            return runner

        self.assertEqual(
            ria.validate_staged_settlement_lineage(
                self.root,
                contract,
                contract_path=selected,
                runner=staged_runner(selected_row),
            ),
            [],
        )
        self.assertEqual(
            ria.validate_explicit_commit_lineage(
                self.root,
                contract,
                "git-sha1:" + c3,
                contract_path=selected,
                runner=explicit_runner(selected_row),
            ),
            [],
        )
        self.assertEqual(
            [
                finding.rule_id
                for finding in ria.validate_staged_settlement_lineage(
                    self.root,
                    contract,
                    contract_path=selected,
                    runner=staged_runner(default_row),
                )
            ],
            ["RIA-TRANSITION"],
        )
        self.assertEqual(
            [
                finding.rule_id
                for finding in ria.validate_explicit_commit_lineage(
                    self.root,
                    contract,
                    "git-sha1:" + c3,
                    contract_path=selected,
                    runner=explicit_runner(default_row),
                )
            ],
            ["RIA-TRANSITION"],
        )

        with (
            mock.patch.object(
                ria, "_build_context", return_value=context
            ),
            mock.patch.object(
                ria, "_settlement_proof", return_value=[]
            ) as settlement,
            mock.patch.object(
                ria, "validate_staged_settlement_lineage", return_value=[]
            ) as staged_lineage,
            mock.patch.object(
                ria, "validate_explicit_commit_lineage", return_value=[]
            ) as explicit_lineage,
        ):
            self.assertEqual(
                ria.validate_baseline_transitions(
                    self.root,
                    contract,
                    staged=True,
                    contract_path=selected,
                ),
                [],
            )
            self.assertEqual(
                ria.validate_baseline_transitions(
                    self.root,
                    contract,
                    commit="git-sha1:" + c3,
                    contract_path=selected,
                ),
                [],
            )
        self.assertTrue(
            all(
                call.kwargs["contract_path"] == selected
                for call in settlement.call_args_list
            )
        )
        self.assertEqual(
            staged_lineage.call_args.kwargs["contract_path"], selected
        )
        self.assertEqual(
            explicit_lineage.call_args.kwargs["contract_path"], selected
        )

    def test_selected_contract_path_mismatch_and_unsafe_path_fail_closed(
        self,
    ) -> None:
        selected = Path(
            "docs/alternate/reference-information-architecture.json"
        )
        contract = self._minimal_contract()
        mismatched = self._minimal_contract()
        mismatched["evidenceCutoff"] = "2026-07-23"
        with mock.patch.object(
            ria,
            "read_proposed_regular_file",
            return_value=json.dumps(mismatched).encode(),
        ):
            finding = ria._contract_authority_finding(  # noqa: SLF001
                self.root.absolute(),
                contract,
                contract_path=selected,
                commit=None,
                runner=None,
            )
        self.assertIsNotNone(finding)
        assert finding is not None
        self.assertEqual(finding.rule_id, "RIA-BOUNDARY")
        self.assertEqual(finding.path, selected.as_posix())

        hostile = self.root.parent / "outside-secret-contract.json"
        with self.assertRaises(ContractError) as raised:
            ria.normalize_contract_path(self.root, hostile)
        self.assertEqual(raised.exception.finding.rule_id, "RIA-BOUNDARY")
        self.assertNotIn(hostile.name, str(raised.exception))

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
                    "-r",
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
                    "-r",
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

    def test_explicit_lineage_recurses_real_git_tree_deltas(self) -> None:
        c2_placeholder = "b" * 40
        c3_placeholder = "c" * 40
        recursive_arguments = (
            "diff-tree",
            "-r",
            "--no-commit-id",
            "--name-status",
            "-z",
            "--no-renames",
            c2_placeholder,
            c3_placeholder,
            "--",
        )
        with self.subTest(case="fixed-argv"):
            self.assertTrue(
                ria._git_arguments_allowed(recursive_arguments)  # noqa: SLF001
            )
            self.assertFalse(
                ria._git_arguments_allowed(  # noqa: SLF001
                    tuple(argument for argument in recursive_arguments if argument != "-r")
                )
            )

        contract_path = ria.DEFAULT_CONTRACT_PATH
        overlay_path = Path("docs/90.references/audits/README.md")
        extra_path = Path("docs/unrelated.md")
        contract_file = self.root / contract_path
        overlay_file = self.root / overlay_path
        overlay_file.parent.mkdir(parents=True, exist_ok=True)
        contract_file.write_bytes(b"C2 contract\n")
        overlay_file.write_bytes(b"C2 overlay\n")
        self._git_in(self.root, "init", "--quiet")
        self._git_in(self.root, "config", "--local", "user.name", "RIA Test")
        self._git_in(
            self.root,
            "config",
            "--local",
            "user.email",
            "ria-test@example.invalid",
        )
        self._git_in(
            self.root,
            "add",
            "--",
            contract_path.as_posix(),
            overlay_path.as_posix(),
        )
        self._git_in(self.root, "commit", "--quiet", "-m", "C2")
        c2 = self._git_in(self.root, "rev-parse", "HEAD").strip().decode("ascii")

        def child_commit(
            message: str, changes: tuple[tuple[Path, bytes], ...]
        ) -> str:
            self._git_in(self.root, "checkout", "--detach", "--quiet", c2)
            paths: list[str] = []
            for path, payload in changes:
                target = self.root / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(payload)
                paths.append(path.as_posix())
            self._git_in(self.root, "add", "--", *paths)
            self._git_in(self.root, "commit", "--quiet", "-m", message)
            return self._git_in(self.root, "rev-parse", "HEAD").strip().decode(
                "ascii"
            )

        exact = child_commit(
            "C3 exact", ((contract_path, b"C3 exact contract\n"),)
        )
        extra = child_commit(
            "C3 extra",
            (
                (contract_path, b"C3 extra contract\n"),
                (extra_path, b"unrelated\n"),
            ),
        )
        overlay = child_commit(
            "C3 overlay",
            (
                (contract_path, b"C3 overlay contract\n"),
                (overlay_path, b"allowed overlay also changed\n"),
            ),
        )
        contract = self._settled_contract("git-sha1:" + c2)
        cases = (("exact", exact, []), ("extra", extra, ["RIA-TRANSITION"]), ("overlay", overlay, ["RIA-TRANSITION"]))
        for name, c3, expected in cases:
            with self.subTest(case=name):
                self.assertEqual(
                    [
                        finding.rule_id
                        for finding in ria.validate_explicit_commit_lineage(
                            self.root, contract, "git-sha1:" + c3
                        )
                    ],
                    expected,
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

    def test_aggregate_runs_self_test_before_production(self) -> None:
        aggregate = AGGREGATE.read_text(encoding="utf-8")
        self_test = (
            'python3 "$ROOT_DIR/scripts/validate-reference-information-architecture.py" '
            "--self-test"
        )
        production = (
            'python3 "$ROOT_DIR/scripts/validate-reference-information-architecture.py" '
            '--root "$ROOT_DIR"'
        )

        self.assertEqual(aggregate.count(self_test), 1)
        self.assertEqual(aggregate.count(production), 1)
        self.assertLess(aggregate.index(self_test), aggregate.index(production))


if __name__ == "__main__":
    unittest.main()
