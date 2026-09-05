"""Select retired inputs through complete, current Git migration proof only."""

from __future__ import annotations

import hashlib
import dataclasses
import importlib.machinery
import importlib.util
import subprocess
import sys
import types
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SELECTOR_PATH = ROOT / "scripts/validate-affected-surfaces.py"


def load_selector():
    spec = importlib.util.spec_from_file_location(
        "affected_migration_test", SELECTOR_PATH
    )
    if spec is None or spec.loader is None:
        raise AssertionError("affected selector is unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class RetiredSurfaceSelectionTest(unittest.TestCase):
    def setUp(self):
        self.selector = load_selector()
        self.contract = self.selector.validate_contract(ROOT)
        # Retain the fixture's real Git proof, without leaking its sys.path
        # adjustment or exporting an imported TestCase for discovery.
        with mock.patch.object(sys, "path", list(sys.path)):
            from tests import test_generic_migration_recovery as fixtures

        self.fixture = fixtures.GenericMigrationRecoveryTest()
        self.addCleanup(self.fixture.doCleanups)
        self.fixture.setUp()
        self.root = self.fixture.root
        self.source = "retired-policy.md"
        self.target = ".agents/roles/quality-engineer.md"
        self.payload = b"# Previous policy\n"
        commit, blobs = self.fixture.git.commit_many({self.source: self.payload})
        self.row = dict(
            legacy_path=self.source,
            stable_path=None,
            artifact_id=None,
            action="merged",
            replacement=self.target,
            source_commit=commit,
            source_blob=blobs[self.source],
            content_sha256=hashlib.sha256(self.payload).hexdigest(),
            reason="Consolidate current policy authority",
        )
        self.fixture.git.run("rm", "--quiet", "--", self.source)
        target = self.root / self.target
        target.parent.mkdir(parents=True)
        target.write_bytes(b"# Current policy\n")
        self.fixture.git.run("add", "--", self.target)
        self.write()

    def write(self, rows=None):
        return self.fixture.write(
            [self.fixture.row, self.row] if rows is None else rows
        )

    def select(self, paths=None, **options):
        return self.selector.select_paths(
            self.contract,
            [self.source] if paths is None else paths,
            "affected",
            self.root,
            **options,
        )

    def assert_failure(self, code, paths=None):
        with self.assertRaises(self.selector.ContractError) as raised:
            self.select(paths)
        self.assertEqual(raised.exception.code, code)
        return raised.exception

    def test_merged_source_uses_current_terminal_contract(self):
        self.assertEqual(self.select(), self.select([self.target]))
        with self.assertRaises(self.selector.ContractError) as raised:
            self.selector.classify_path(self.contract, self.source)
        self.assertEqual(raised.exception.code, "SURFACE-PATH-UNMATCHED")

    def test_composed_successor_is_classified_once_at_its_terminal(self):
        middle = "retired-intermediate.md"
        commit, blobs = self.fixture.git.commit_many({middle: self.payload})
        self.fixture.git.run("rm", "--quiet", "--", middle)
        self.write(
            [
                self.fixture.row,
                dict(self.row, replacement=middle),
                dict(
                    self.row,
                    legacy_path=middle,
                    source_commit=commit,
                    source_blob=blobs[middle],
                ),
            ]
        )
        self.assertEqual(self.select([self.source, middle]), self.select([self.target]))

    def test_deleted_source_uses_proved_archive_boundary_and_one_lookup(self):
        deleted = "retired-instructions.md"
        commit, blobs = self.fixture.git.commit_many({deleted: self.payload})
        self.fixture.git.run("rm", "--quiet", "--", deleted)
        archive = "docs/98.archive/README.md"
        (self.root / archive).write_bytes(b"# Archive\n")
        self.fixture.git.run("add", "--", archive)
        self.write(
            [
                self.fixture.row,
                self.row,
                dict(
                    self.row,
                    legacy_path=deleted,
                    action="deleted",
                    replacement=None,
                    source_commit=commit,
                    source_blob=blobs[deleted],
                ),
            ]
        )
        with mock.patch.object(
            self.selector,
            "_repository_migration_proof",
            wraps=self.selector._repository_migration_proof,
        ) as proof:
            actual = self.select([self.source, deleted, self.source])
        self.assertEqual(proof.call_count, 1)
        self.assertEqual(actual, self.select([self.target, archive]))

    def test_current_contract_and_held_owner_queries_never_obtain_proof(self):
        with mock.patch.object(
            self.selector,
            "_repository_migration_proof",
            create=True,
            side_effect=AssertionError("unexpected recovery lookup"),
        ) as proof:
            self.select([self.target])
            self.selector.validate_contract(ROOT)
            self.selector.validator_script_paths(ROOT)
            self.selector.classify_path(self.contract, "README.md")
            with self.assertRaises(self.selector.ContractError) as raised:
                self.selector.select_paths(self.contract, [self.source], "affected")
            self.assertEqual(raised.exception.code, "SURFACE-PATH-UNMATCHED")
        proof.assert_not_called()

    def test_each_call_preserves_its_lane_without_caching_proof(self):
        with mock.patch.object(
            self.selector,
            "_repository_migration_proof",
            wraps=self.selector._repository_migration_proof,
        ) as proof:
            for lane in self.selector.SELECTOR_LANES:
                with self.subTest(lane=lane):
                    self.assertEqual(
                        self.selector.select_paths(
                            self.contract, [self.source], lane, self.root
                        ),
                        self.selector.select_paths(
                            self.contract, [self.target], lane, self.root
                        ),
                    )
        self.assertEqual(proof.call_count, len(self.selector.SELECTOR_LANES))

    def test_unregistered_absence_remains_unmatched(self):
        unknown = "unregistered-retirement.md"
        self.assert_failure("SURFACE-PATH-UNMATCHED", [unknown])
        self.assertEqual(
            self.select([unknown], collect_unmatched=True)["unmatchedPaths"], [unknown]
        )

    def test_failed_proof_is_not_collected_or_retried(self):
        with (
            mock.patch.object(
                self.selector,
                "_repository_migration_proof",
                side_effect=self.selector.ContractError(
                    "SURFACE-MIGRATION-PROOF",
                    "canonical migration proof is unavailable",
                ),
            ) as proof,
            self.assertRaises(self.selector.ContractError) as raised,
        ):
            self.select([self.source, "other-retired.md"], collect_unmatched=True)
        self.assertEqual(raised.exception.code, "SURFACE-MIGRATION-PROOF")
        proof.assert_called_once_with(self.root)

    def test_existing_unmatched_source_never_obtains_proof(self):
        (self.root / self.source).write_bytes(self.payload)
        with mock.patch.object(
            self.selector,
            "_repository_migration_proof",
            create=True,
            side_effect=AssertionError("unexpected recovery lookup"),
        ) as proof:
            self.assert_failure("SURFACE-PATH-UNMATCHED")
        proof.assert_not_called()

    def test_unsafe_source_and_case_alias_never_obtain_proof(self):
        (self.root / self.source).symlink_to(self.target)
        with mock.patch.object(
            self.selector,
            "_repository_migration_proof",
            create=True,
            side_effect=AssertionError("unexpected recovery lookup"),
        ) as proof:
            self.assert_failure("SURFACE-PATH-SYMLINK")
            self.assert_failure("SURFACE-PATH-CASE-ALIAS", ["readme.md"])
            self.assert_failure("SURFACE-PATH-NORMALIZATION", ["../retired-policy.md"])
        proof.assert_not_called()

    def test_recreated_source_after_proof_is_not_selected(self):
        original = self.selector._repository_migration_proof

        def recreate(root):
            proof = original(root)
            (root / self.source).write_bytes(self.payload)
            return proof

        with mock.patch.object(self.selector, "_repository_migration_proof", recreate):
            self.assert_failure("SURFACE-PATH-UNMATCHED")

    def test_source_digest_target_index_and_cycle_fail_closed(self):
        self.write([self.fixture.row, dict(self.row, content_sha256="0" * 64)])
        self.assert_failure("SURFACE-MIGRATION-PROOF")
        self.write()
        target = self.root / self.target
        original = target.read_bytes()
        target.write_bytes(b"# Unsynchronized target\n")
        self.assert_failure("SURFACE-MIGRATION-PROOF")
        self.fixture.git.run("add", "--", self.target)
        target.write_bytes(original)
        self.assert_failure("SURFACE-MIGRATION-PROOF")
        self.fixture.git.run("add", "--", self.target)
        middle = "retired-cycle.md"
        commit, blobs = self.fixture.git.commit_many({middle: self.payload})
        self.fixture.git.run("rm", "--quiet", "--", middle)
        self.write(
            [
                self.fixture.row,
                dict(self.row, replacement=middle),
                dict(
                    self.row,
                    legacy_path=middle,
                    replacement=self.source,
                    source_commit=commit,
                    source_blob=blobs[middle],
                ),
            ]
        )
        self.assert_failure("SURFACE-MIGRATION-PROOF")

    def test_selection_requires_exact_disposition_and_composed_target(self):
        proof = self.selector._repository_migration_proof(self.root)
        for changed in (
            dataclasses.replace(proof, dispositions={}),
            dataclasses.replace(proof, records={}),
            dataclasses.replace(proof, targets={self.source: "README.md"}),
        ):
            with (
                self.subTest(changed=changed),
                mock.patch.object(
                    self.selector, "_repository_migration_proof", return_value=changed
                ),
            ):
                self.assert_failure("SURFACE-MIGRATION-PROOF")

    def test_proved_unmatched_target_does_not_gain_a_route(self):
        target = "unregistered-successor.md"
        (self.root / target).write_bytes(b"# Current replacement\n")
        self.fixture.git.run("add", "--", target)
        self.write([self.fixture.row, dict(self.row, replacement=target)])
        self.assert_failure("SURFACE-MIGRATION-TARGET")

    def test_loader_restores_aliases_on_success_import_and_proof_failure(self):
        aliases = {
            name: types.ModuleType(name)
            for name in (
                "json_schema_validation",
                "document_authority",
                "archive_cutover_manifest",
                "archive_recovery",
                "document_contracts",
                "archive_validation",
            )
        }
        execute = importlib.machinery.SourceFileLoader.exec_module
        before_path = sys.path[:]
        for failure in (None, "import", "proof"):
            with self.subTest(failure=failure), mock.patch.dict(sys.modules, aliases):
                before_modules = dict(sys.modules)

                def checked_execute(loader, module):
                    if (
                        failure == "import"
                        and Path(loader.path).name == "document_contracts.py"
                    ):
                        raise ImportError("private import payload")
                    execute(loader, module)
                    if (
                        failure == "proof"
                        and Path(loader.path).name == "archive_validation.py"
                    ):
                        module.repository_migration_proof = mock.Mock(
                            side_effect=ValueError("private proof payload")
                        )

                with mock.patch.object(
                    importlib.machinery.SourceFileLoader, "exec_module", checked_execute
                ):
                    if failure is None:
                        self.assertEqual(self.select(), self.select([self.target]))
                    else:
                        error = self.assert_failure("SURFACE-MIGRATION-PROOF")
                        self.assertNotIn("private", str(error))
                for name, module in aliases.items():
                    self.assertIs(sys.modules[name], module)
                self.assertEqual(sys.path, before_path)
                self.assertEqual(
                    {
                        name
                        for name in sys.modules
                        if name.startswith("_affected_migration_")
                    },
                    {
                        name
                        for name in before_modules
                        if name.startswith("_affected_migration_")
                    },
                )

    def test_normal_and_isolated_loader_execute_real_fallback(self):
        code = """
import importlib.util, json, pathlib, sys
path = pathlib.Path(sys.argv[1])
spec = importlib.util.spec_from_file_location('isolated_affected', path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
before = sys.path[:]
names = ('json_schema_validation', 'document_authority', 'archive_cutover_manifest',
         'archive_recovery', 'document_contracts', 'archive_validation',
         )
owners_before = {name: sys.modules[name] for name in names if name in sys.modules}
contract = module.validate_contract(path.parent.parent)
result = module.select_paths(contract, [sys.argv[3]], 'affected', pathlib.Path(sys.argv[2]))
assert sys.path == before
assert {name: sys.modules[name] for name in names if name in sys.modules} == owners_before
assert not any(name.startswith('_affected_migration_') for name in sys.modules)
print(json.dumps(result, sort_keys=True))
"""
        for flags in ([], ["-I"]):
            with self.subTest(flags=flags):
                result = subprocess.run(
                    [
                        sys.executable,
                        *flags,
                        "-c",
                        code,
                        str(SELECTOR_PATH),
                        str(self.root),
                        self.source,
                    ],
                    cwd=self.root,
                    capture_output=True,
                    text=True,
                    timeout=30,
                    check=False,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn('"unmatchedPaths": []', result.stdout)

    def test_direct_cli_fallback_preserves_nul_inputs_and_output(self):
        for relative in (self.selector.CONTRACT_PATH, self.selector.SCHEMA_PATH):
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((ROOT / relative).read_bytes())
        paths = self.root / "selection.nul"
        payload = (self.source + "\0" + self.source + "\0").encode()
        paths.write_bytes(payload)
        for flags, cwd in (([], ROOT), (["-I"], self.root)):
            with self.subTest(flags=flags):
                result = subprocess.run(
                    [
                        sys.executable,
                        *flags,
                        str(ROOT / "scripts/select-affected-surfaces.py"),
                        "--root",
                        str(self.root),
                        "--lane",
                        "affected",
                        "--paths-file",
                        str(paths),
                        "--delimiter",
                        "nul",
                        "--format",
                        "json",
                    ],
                    cwd=cwd,
                    capture_output=True,
                    text=True,
                    timeout=30,
                    check=False,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(
                    result.stdout.strip(), self.selector.json_output(self.select())
                )
                self.assertEqual(paths.read_bytes(), payload)


if __name__ == "__main__":
    unittest.main()
