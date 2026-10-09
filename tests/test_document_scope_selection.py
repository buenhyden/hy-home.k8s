"""Changed document readers select their own contract gates."""

from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "document_scope_routes", ROOT / "scripts/validate-affected-surfaces.py"
)
assert SPEC is not None and SPEC.loader is not None
ROUTES = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = ROUTES
SPEC.loader.exec_module(ROUTES)
CONTRACT = json.loads((ROOT / "scripts/validation/registry.json").read_text())

DOCUMENT_READERS = (
    "scripts/validate-markdown-profiles.py",
    "scripts/validate-links-and-owners.py",
    "scripts/validate-document-contract-registry.py",
    "tests/test_operations_section_contract.py",
    "tests/test_operations_lineage_contract.py",
    "tests/test_shared_contract_binding.py",
    "tests/test_document_scope_selection.py",
    "scripts/sync-task-status.py",
    "tests/test_task_acceptance_boundaries.py",
)
HISTORY_READERS = (
    "scripts/document_authority.py",
    "scripts/document_contracts.py",
    "scripts/document_lifecycle.py",
    "scripts/validate-document-lifecycle.py",
    "tests/test_task_acceptance_contract.py",
    "tests/test_task_execution_contract.py",
)
DOCUMENT_GATES = {
    "affected-surface-contract",
    "document-contract-registry",
    "document-lifecycle",
    "links-and-owners",
    "markdown-profiles",
    "repository-quality",
}
ARCHIVE_GATES = {"archive-contract-tests", "archive-integrity"}


class DocumentScopeSelectionTests(unittest.TestCase):
    def test_document_reader_paths_have_one_explicit_owner(self) -> None:
        ROUTES.validate_contract(ROOT, CONTRACT)
        for path in DOCUMENT_READERS:
            with self.subTest(path=path):
                self.assertEqual(
                    ROUTES.classify_path(CONTRACT, path)["id"],
                    "document-reader-implementation",
                )

    def test_document_only_paths_skip_unrelated_product_gates(self) -> None:
        affected = ROUTES.select_paths(CONTRACT, DOCUMENT_READERS, "affected")
        self.assertEqual(set(affected["validators"]), DOCUMENT_GATES)
        self.assertEqual(affected["protectedLevel"], "protected")

        staged = ROUTES.select_paths(CONTRACT, DOCUMENT_READERS, "staged")
        self.assertEqual(
            set(staged["validators"]),
            DOCUMENT_GATES | {"selected-nonstyle", "selected-style"},
        )

    def test_shared_history_readers_keep_archive_contract_guards(self) -> None:
        for path in HISTORY_READERS:
            with self.subTest(path=path):
                self.assertEqual(
                    ROUTES.classify_path(CONTRACT, path)["id"],
                    "shared-document-history-readers",
                )
                selected = ROUTES.select_paths(CONTRACT, (path,), "affected")
                self.assertEqual(
                    set(selected["validators"]), DOCUMENT_GATES | ARCHIVE_GATES
                )
                self.assertNotIn("k8s-manifests", selected["validators"])

    def test_registry_definition_has_its_own_selector_gate(self) -> None:
        surface = ROUTES.classify_path(CONTRACT, "scripts/validation/registry.json")
        self.assertEqual(surface["id"], "validation-surface-contract")
        selected = ROUTES.select_paths(
            CONTRACT, ("scripts/validation/registry.json",), "affected"
        )
        self.assertEqual(
            set(selected["validators"]),
            {"affected-surface-contract", "repository-quality"},
        )

    def test_qa_entrypoint_and_its_regression_have_the_selector_owner(self) -> None:
        for path in ("scripts/qa.py", "tests/test_qa_runner.py"):
            with self.subTest(path=path):
                surface = ROUTES.classify_path(CONTRACT, path)
                self.assertEqual(surface["id"], "validation-surface-contract")
                selected = ROUTES.select_paths(CONTRACT, (path,), "affected")
                self.assertEqual(
                    set(selected["validators"]),
                    {"affected-surface-contract", "repository-quality"},
                )

    def test_shared_validation_consumers_keep_broad_gate_closure(self) -> None:
        for path in (
            "scripts/run-validation-lane.py",
            "scripts/validate-affected-surfaces.py",
            "scripts/select-affected-surfaces.py",
        ):
            with self.subTest(path=path):
                surface = ROUTES.classify_path(CONTRACT, path)
                self.assertEqual(surface["id"], "scripts")
                self.assertIn("k8s-manifests", surface["validators"])

    def test_mixed_infrastructure_change_adds_its_product_gates(self) -> None:
        selected = ROUTES.select_paths(
            CONTRACT,
            ("scripts/validate-markdown-profiles.py", "gitops/platform/sample.yaml"),
            "affected",
        )
        self.assertTrue(DOCUMENT_GATES <= set(selected["validators"]))
        self.assertTrue(
            {"gitops-structure", "k8s-manifests", "secret-handling"}
            <= set(selected["validators"])
        )

    def test_other_scripts_and_tests_keep_broad_registered_routes(self) -> None:
        for path in (
            "scripts/validate-gitops-structure.py",
            "scripts/document_contracts.py.backup",
            "scripts/document_lifecycle.py.backup",
        ):
            with self.subTest(path=path):
                surface = ROUTES.classify_path(CONTRACT, path)
                self.assertEqual(surface["id"], "scripts")
                self.assertIn("k8s-manifests", surface["validators"])
        for path in (
            "tests/test_k8s_contract.py",
            "tests/test_operations_section_contract.py.backup",
            "tests/test_task_acceptance_contract.py.backup",
        ):
            with self.subTest(path=path):
                surface = ROUTES.classify_path(CONTRACT, path)
                self.assertEqual(surface["id"], "tests")
                self.assertIn("archive-contract-tests", surface["validators"])


if __name__ == "__main__":
    unittest.main()
