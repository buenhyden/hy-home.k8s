#!/usr/bin/env python3
"""Focused regressions for the closed AGQC-003 legacy cutover contract."""

from __future__ import annotations

import copy
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = REPO_ROOT / "scripts/validate-agent-legacy-cutover.py"
CONTRACT_PATH = (
    REPO_ROOT
    / "docs/00.agent-governance/contracts/agent-legacy-cutover.json"
)
SCHEMA_PATH = CONTRACT_PATH.with_name("agent-legacy-cutover.schema.json")
FIXTURE_PATH = REPO_ROOT / "tests/fixtures/agent-legacy-cutover.json"

RETIRED_CONTRACT = Path(
    "docs/00.agent-governance/contracts/agent-role-semantics.json"
)
HARNESS_CONTRACT = Path(
    "docs/00.agent-governance/contracts/harness-contract.json"
)
REPLACEMENTS = (
    HARNESS_CONTRACT,
    Path("docs/00.agent-governance/contracts/harness-contract.schema.json"),
    Path("scripts/validate-agent-harness-semantics.py"),
    Path("tests/fixtures/agent-harness-semantics.json"),
    Path(".github/README.md"),
)


def load_validator():
    spec = importlib.util.spec_from_file_location(
        "validate_agent_legacy_cutover",
        VALIDATOR_PATH,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load validator: {VALIDATOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class AgentLegacyCutoverArtifactTests(unittest.TestCase):
    def test_core_artifacts_exist(self) -> None:
        missing = [
            path.relative_to(REPO_ROOT).as_posix()
            for path in (CONTRACT_PATH, SCHEMA_PATH, VALIDATOR_PATH, FIXTURE_PATH)
            if not path.is_file()
        ]
        self.assertEqual(missing, [])


@unittest.skipUnless(
    VALIDATOR_PATH.is_file() and CONTRACT_PATH.is_file() and SCHEMA_PATH.is_file(),
    "validator is intentionally absent at the RED gate",
)
class AgentLegacyCutoverValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_validator()
        cls.fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

    def make_valid_root(self) -> Path:
        directory = tempfile.TemporaryDirectory(prefix="agent-legacy-cutover-")
        self.addCleanup(directory.cleanup)
        root = Path(directory.name)
        for relative_text in dict.fromkeys(
            self.validator.PACKAGE_REFERENCES
            + self.validator.MIGRATION_REFERENCES
        ):
            relative = Path(relative_text)
            source = REPO_ROOT / relative
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
        for record in self.validator.PROTECTED_EVIDENCE_FILES:
            relative = Path(record["path"])
            source = REPO_ROOT / relative
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
        for relative in REPLACEMENTS:
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            if relative == HARNESS_CONTRACT:
                target.write_text(
                    json.dumps(
                        {
                            "consumers": [
                                {
                                    "id": "harness-semantics-validator",
                                    "path": (
                                        "scripts/"
                                        "validate-agent-harness-semantics.py"
                                    ),
                                }
                            ]
                        },
                        indent=2,
                    )
                    + "\n",
                    encoding="utf-8",
                )
            elif relative.suffix == ".json":
                target.write_text("{}\n", encoding="utf-8")
            else:
                target.write_text("canonical replacement\n", encoding="utf-8")
        subprocess.run(
            ["git", "init", "--quiet"],
            cwd=root,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return root

    def assert_rule(self, root: Path, rule_id: str) -> None:
        with self.assertRaises(self.validator.ContractError) as raised:
            self.validator.validate_repository(root)
        self.assertEqual(raised.exception.rule_id, rule_id)

    def test_valid_cutover_root_passes(self) -> None:
        counts = self.validator.validate_repository(self.make_valid_root())
        self.assertEqual(counts["retiredSurfaces"], 5)
        self.assertEqual(counts["replacementSurfaces"], 5)
        self.assertEqual(counts["activeConsumers"], 0)

    def test_self_test_is_deterministic_and_repo_is_unchanged(self) -> None:
        before = CONTRACT_PATH.read_bytes()
        self.assertEqual(self.validator.run_self_test(REPO_ROOT), (3, 23))
        self.assertEqual(CONTRACT_PATH.read_bytes(), before)

    def test_closed_schema_rejects_unknown_contract_key(self) -> None:
        root = self.make_valid_root()
        contract, schema = self.validator.load_contract_documents(root)
        mutated = copy.deepcopy(contract)
        mutated["unexpected"] = True
        with self.assertRaises(self.validator.ContractError) as raised:
            self.validator.validate_contract_data(mutated, schema)
        self.assertEqual(raised.exception.rule_id, "AGQC-LEGACY-SCHEMA")

        mutated = copy.deepcopy(contract)
        mutated["scanPolicy"]["scanAllRegularFiles"] = True
        with self.assertRaises(self.validator.ContractError) as raised:
            self.validator.validate_contract_data(mutated, schema)
        self.assertEqual(raised.exception.rule_id, "AGQC-LEGACY-SCHEMA")

    def test_repository_root_and_candidate_paths_fail_closed(self) -> None:
        directory = tempfile.TemporaryDirectory(prefix="agent-legacy-nongit-")
        self.addCleanup(directory.cleanup)
        with self.assertRaises(self.validator.ContractError) as raised:
            self.validator.validate_repository(Path(directory.name))
        self.assertEqual(raised.exception.rule_id, "AGQC-LEGACY-INPUT")

        root = self.make_valid_root()
        nested = root / "nested"
        nested.mkdir()
        with self.assertRaises(self.validator.ContractError) as raised:
            self.validator.validate_repository(nested)
        self.assertEqual(raised.exception.rule_id, "AGQC-LEGACY-INPUT")

        for payload in (b"../outside\0", b"unterminated", b"invalid-\xff\0"):
            with self.subTest(payload=payload):
                with self.assertRaises(self.validator.ContractError) as raised:
                    self.validator._parse_git_candidates(payload)
                self.assertEqual(
                    raised.exception.rule_id,
                    "AGQC-LEGACY-INPUT",
                )

    def test_nul_safe_candidate_and_candidate_types_fail_closed(self) -> None:
        root = self.make_valid_root()
        proposed = root / "proposed\nconsumer.txt"
        proposed.write_text(
            f"use {RETIRED_CONTRACT.as_posix()}\n",
            encoding="utf-8",
        )
        self.assert_rule(root, "AGQC-LEGACY-CONSUMER")

        proposed.unlink()
        link = root / "proposed-link"
        link.symlink_to("AGENTS.md")
        self.assert_rule(root, "AGQC-LEGACY-INPUT")

        link.unlink()
        fifo = root / "proposed-fifo"
        os.mkfifo(fifo)
        with self.assertRaises(self.validator.ContractError) as raised:
            self.validator._candidate_payload(
                root,
                fifo.name,
                read=True,
            )
        self.assertEqual(raised.exception.rule_id, "AGQC-LEGACY-INPUT")

    def test_retained_surface_is_rejected(self) -> None:
        root = self.make_valid_root()
        path = root / RETIRED_CONTRACT
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("{}\n", encoding="utf-8")
        self.assert_rule(root, "AGQC-LEGACY-RETIRED")

    def test_missing_replacement_is_rejected(self) -> None:
        root = self.make_valid_root()
        (root / ".github/README.md").unlink()
        self.assert_rule(root, "AGQC-LEGACY-REPLACEMENT")

    def test_stale_current_consumer_is_rejected(self) -> None:
        root = self.make_valid_root()
        (root / "AGENTS.md").write_text(
            f"use {RETIRED_CONTRACT.as_posix()}\n",
            encoding="utf-8",
        )
        self.assert_rule(root, "AGQC-LEGACY-CONSUMER")

    def test_ignored_unreadable_file_is_not_opened_or_counted(self) -> None:
        root = self.make_valid_root()
        (root / ".gitignore").write_text(
            "ignored-private/\n",
            encoding="utf-8",
        )
        baseline = self.validator.validate_repository(root)
        sentinel = root / "ignored-private/retired-token.txt"
        sentinel.parent.mkdir()
        sentinel.write_text(
            f"private {RETIRED_CONTRACT.as_posix()}\n",
            encoding="utf-8",
        )
        sentinel.chmod(0)
        self.addCleanup(sentinel.chmod, 0o600)

        ignored = self.validator.validate_repository(root)
        self.assertEqual(ignored, baseline)

        proposed = root / "proposed-consumer.txt"
        proposed.write_text(
            f"use {RETIRED_CONTRACT.as_posix()}\n",
            encoding="utf-8",
        )
        self.assert_rule(root, "AGQC-LEGACY-CONSUMER")

    def test_terminal_and_digest_pinned_evidence_are_not_active_consumers(
        self,
    ) -> None:
        root = self.make_valid_root()
        terminal = root / "docs/04.execution/plans/completed.md"
        terminal.parent.mkdir(parents=True, exist_ok=True)
        terminal.write_text(
            "---\nstatus: Done\n---\n"
            f"historical: {RETIRED_CONTRACT.as_posix()}\n",
            encoding="utf-8",
        )
        protected_relative = Path(
            "docs/90.references/data/active-corpus-retention-census.json"
        )
        protected = root / protected_relative
        protected.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(REPO_ROOT / protected_relative, protected)
        self.validator.validate_repository(root)

    def test_digest_pinned_draft_reference_is_rejected(self) -> None:
        root = self.make_valid_root()
        contract, schema = self.validator.load_contract_documents(root)
        mutated = copy.deepcopy(contract)
        record = mutated["referencePolicy"]["protectedEvidenceFiles"][0]
        record["path"] = (
            "docs/90.references/audits/draft-stale-reference.md"
        )
        record["evidenceKind"] = "authored-document"
        record["lifecycleStatus"] = "draft"
        with self.assertRaises(self.validator.ContractError) as raised:
            self.validator.validate_contract_data(mutated, schema)
        self.assertEqual(raised.exception.rule_id, "AGQC-LEGACY-SCHEMA")

    def test_missing_protected_evidence_is_rejected(self) -> None:
        root = self.make_valid_root()
        protected = root / self.validator.PROTECTED_EVIDENCE_FILES[0]["path"]
        protected.unlink()
        self.assert_rule(root, "AGQC-LEGACY-CONSUMER")

    def test_protected_reference_removal_is_rejected(self) -> None:
        root = self.make_valid_root()
        record = self.validator.PROTECTED_EVIDENCE_FILES[0]
        protected = root / record["path"]
        raw = protected.read_bytes()
        retired = record["retiredReference"].encode("utf-8")
        replacement = record["supersededBy"].encode("utf-8")
        self.assertEqual(raw.count(retired), record["count"])
        protected.write_bytes(raw.replace(retired, replacement))
        self.assert_rule(root, "AGQC-LEGACY-CONSUMER")

    def test_active_and_accepted_reference_documents_are_consumers(self) -> None:
        for status in ("active", "accepted"):
            with self.subTest(status=status):
                root = self.make_valid_root()
                reference = (
                    root
                    / "docs/90.references/research/2026-07-07-wer"
                    / f"unowned-{status}.md"
                )
                reference.parent.mkdir(parents=True, exist_ok=True)
                reference.write_text(
                    "---\n"
                    "title: 'Current reference'\n"
                    "type: content/reference\n"
                    f"status: {status}\n"
                    "owner: platform\n"
                    "updated: 2026-07-30\n"
                    "---\n\n"
                    f"use {RETIRED_CONTRACT.as_posix()}\n",
                    encoding="utf-8",
                )
                self.assert_rule(root, "AGQC-LEGACY-CONSUMER")

    def test_old_harness_consumer_and_compatibility_are_rejected(self) -> None:
        for mutation in ("consumer", "compatibility"):
            with self.subTest(mutation=mutation):
                root = self.make_valid_root()
                harness = root / HARNESS_CONTRACT
                value = json.loads(harness.read_text(encoding="utf-8"))
                if mutation == "consumer":
                    value["consumers"] = [
                        {
                            "id": "role-semantics-validator",
                            "path": "scripts/validate-agent-role-semantics.py",
                        }
                    ]
                else:
                    value["compatibility"] = {
                        "removalOwnerSpec": (
                            "docs/03.specs/"
                            "045-agent-governance-ci-qa-cutover/spec.md"
                        )
                    }
                harness.write_text(
                    json.dumps(value, indent=2) + "\n",
                    encoding="utf-8",
                )
                self.assert_rule(root, "AGQC-LEGACY-HARNESS")

    def test_symlink_replacement_is_rejected(self) -> None:
        root = self.make_valid_root()
        hub = root / ".github/README.md"
        target = hub.with_name("hub-copy.md")
        shutil.copyfile(hub, target)
        hub.unlink()
        hub.symlink_to(target.name)
        self.assert_rule(root, "AGQC-LEGACY-INPUT")

    def test_malformed_and_duplicate_json_are_rejected(self) -> None:
        for text in ('{"consumers": [', '{"consumers": [], "consumers": []}\n'):
            with self.subTest(text=text):
                root = self.make_valid_root()
                (root / HARNESS_CONTRACT).write_text(text, encoding="utf-8")
                self.assert_rule(root, "AGQC-LEGACY-JSON")

    def test_undeclared_allowlist_growth_is_rejected(self) -> None:
        root = self.make_valid_root()
        contract, schema = self.validator.load_contract_documents(root)
        for key, value, expected_rule in (
            ("migrationReferences", "docs/unreviewed.md", "AGQC-LEGACY-SCHEMA"),
            (
                "protectedEvidenceFiles",
                {
                    "path": "docs/current.md",
                    "sha256": "0" * 64,
                },
                "AGQC-LEGACY-SCHEMA",
            ),
        ):
            with self.subTest(key=key):
                mutated = copy.deepcopy(contract)
                mutated["referencePolicy"][key].append(value)
                with self.assertRaises(self.validator.ContractError) as raised:
                    self.validator.validate_contract_data(mutated, schema)
                self.assertEqual(
                    raised.exception.rule_id,
                    expected_rule,
                )

    def test_path_escape_is_rejected(self) -> None:
        root = self.make_valid_root()
        contract, schema = self.validator.load_contract_documents(root)
        mutated = copy.deepcopy(contract)
        mutated["replacementSurfaces"][4] = "../outside.md"
        with self.assertRaises(self.validator.ContractError) as raised:
            self.validator.validate_contract_data(mutated, schema)
        self.assertEqual(raised.exception.rule_id, "AGQC-LEGACY-SCHEMA")

    def test_fixture_payload_path_changes_are_rejected_before_execution(
        self,
    ) -> None:
        for value in ("/tmp/outside", "../../outside"):
            with self.subTest(value=value):
                directory = tempfile.TemporaryDirectory(
                    prefix="agent-legacy-fixture-"
                )
                self.addCleanup(directory.cleanup)
                root = Path(directory.name)
                fixture = copy.deepcopy(self.fixture)
                fixture["mutationCases"][0]["mutation"]["path"] = value
                path = root / "tests/fixtures/agent-legacy-cutover.json"
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(
                    json.dumps(fixture, indent=2) + "\n",
                    encoding="utf-8",
                )
                with self.assertRaises(
                    self.validator.ContractError
                ) as raised:
                    self.validator._load_fixture(root)
                self.assertEqual(
                    raised.exception.rule_id,
                    "AGQC-LEGACY-FIXTURE",
                )

    def test_fixture_write_rejects_symlink_parent(self) -> None:
        directory = tempfile.TemporaryDirectory(prefix="agent-legacy-parent-")
        outside = tempfile.TemporaryDirectory(prefix="agent-legacy-outside-")
        self.addCleanup(directory.cleanup)
        self.addCleanup(outside.cleanup)
        root = Path(directory.name)
        (root / "safe").symlink_to(Path(outside.name), target_is_directory=True)
        with self.assertRaises(self.validator.ContractError) as raised:
            self.validator._write_text(root, "safe/escape.md", "blocked\n")
        self.assertEqual(raised.exception.rule_id, "AGQC-LEGACY-FIXTURE")
        self.assertFalse((Path(outside.name) / "escape.md").exists())

    def test_every_allowed_reference_rejects_occurrence_growth(self) -> None:
        for relative, _counts in self.validator.ALLOWED_REFERENCE_COUNTS:
            with self.subTest(relative=relative):
                root = self.make_valid_root()
                path = root / relative
                path.write_bytes(
                    path.read_bytes()
                    + b"\n"
                    + self.validator.RETIRED_SURFACES[0].encode("utf-8")
                    + b"\n"
                )
                _scanned, _evidence, consumers = (
                    self.validator._scan_consumers(root)
                )
                self.assertTrue(
                    any(
                        consumer.startswith(
                            f"{relative}:allowed-reference-count-drift"
                        )
                        for consumer in consumers
                    ),
                    consumers,
                )


if __name__ == "__main__":
    unittest.main()
