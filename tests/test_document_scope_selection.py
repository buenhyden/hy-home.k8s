"""Changed document readers select their own contract gates."""

from __future__ import annotations

import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "document_scope_routes", ROOT / "scripts/validate-affected-surfaces.py"
)
assert SPEC is not None and SPEC.loader is not None
ROUTES = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = ROUTES
SPEC.loader.exec_module(ROUTES)
import document_contracts as DOCUMENTS  # noqa: E402
from validation import document_content as CONTENT  # noqa: E402

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

    def test_reader_helpers_have_the_document_gate_owner(self) -> None:
        for path in (
            "scripts/document_language.py",
            "scripts/validation/document_content.py",
        ):
            with self.subTest(path=path):
                surface = ROUTES.classify_path(CONTRACT, path)
                self.assertEqual(surface["id"], "document-reader-implementation")
                self.assertIn("markdown-profiles", surface["validators"])

    def test_english_only_provider_sources_select_language_reader(self) -> None:
        for path in (
            ".agents/roles/registry.json",
            ".claude/agents/quality-engineer.md",
            ".codex/agents/quality-engineer.toml",
        ):
            with self.subTest(path=path):
                selected = ROUTES.select_paths(CONTRACT, (path,), "affected")
                self.assertIn("markdown-profiles", selected["validators"])

    def test_non_markdown_matrix_producers_select_document_content_gate(self) -> None:
        examples = (
            "examples/new-service/kustomization.yaml",
            ".github/workflows/new.yml",
            "gitops/platform/new-service/kustomization.yaml",
            "gitops/workloads/new-service/kustomization.yaml",
            "infrastructure/new-area/config.yaml",
            "infrastructure/verify/new-check.sh",
            "gitops/platform/eso/vault-secret-store.yaml",
            "infrastructure/vault/policies/eso-read.hcl",
            "gitops/clusters/local/kustomization.yaml",
            "gitops/apps/root/kustomization.yaml",
        )
        for path in examples:
            with self.subTest(path=path):
                selected = ROUTES.select_paths(CONTRACT, (path,), "affected")
                self.assertIn("markdown-profiles", selected["validators"])

    def test_operation_record_paths_select_the_content_reader(self) -> None:
        for path in (
            "docs/05.operations/guides/0010-ci-cd-qa-reference-guide.md",
            "docs/05.operations/policies/0003-service-mesh-cert-manager-policy.md",
            "docs/05.operations/runbooks/0012-main-release-preparation-runbook.md",
            "docs/05.operations/incidents/2026/inc-2026-new/incident.md",
        ):
            with self.subTest(path=path):
                selected = ROUTES.select_paths(CONTRACT, (path,), "affected")
                self.assertIn("markdown-profiles", selected["validators"])

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


class DocumentContentClosureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = DOCUMENTS.load_registry(ROOT)
        cls.current = DOCUMENTS.enumerate_target_markdown(ROOT).current_paths

    def test_changed_producer_includes_exact_current_matrix_owner(self) -> None:
        cases = (
            ("examples/new-service/kustomization.yaml", "examples/README.md"),
            (".github/workflows/new.yml", ".github/repository-surface.md"),
            (
                "gitops/platform/new-service/kustomization.yaml",
                "gitops/platform/README.md",
            ),
            (
                "gitops/workloads/new-service/kustomization.yaml",
                "gitops/workloads/README.md",
            ),
            ("infrastructure/new-area/config.yaml", "infrastructure/README.md"),
            ("infrastructure/verify/new-check.sh", "infrastructure/verify/README.md"),
            ("gitops/clusters/local/kustomization.yaml", "gitops/README.md"),
            ("gitops/apps/root/kustomization.yaml", "gitops/README.md"),
            (
                "docs/05.operations/guides/0010-ci-cd-qa-reference-guide.md",
                "docs/05.operations/guides/README.md",
            ),
            (
                "docs/05.operations/policies/0003-service-mesh-cert-manager-policy.md",
                "docs/05.operations/policies/README.md",
            ),
            (
                "docs/05.operations/runbooks/0012-main-release-preparation-runbook.md",
                "docs/05.operations/runbooks/README.md",
            ),
            (
                "docs/05.operations/incidents/2026/inc-2026-new/incident.md",
                "docs/05.operations/incidents/README.md",
            ),
        )
        for producer, owner in cases:
            with self.subTest(producer=producer):
                scope = DOCUMENTS.scoped_document_content_paths(
                    self.registry, (producer,), self.current
                )
                self.assertIn(
                    Path(owner).as_posix(), {path.as_posix() for path in scope}
                )

    def test_contract_template_or_reader_change_expands_to_full_document_body(
        self,
    ) -> None:
        for path in (
            "docs/99.templates/registry.json",
            "docs/99.templates/contracts/frontmatter.schema.json",
            "docs/99.templates/templates/specs/task.template.md",
            "scripts/document_language.py",
            "scripts/validation/document_content.py",
        ):
            with self.subTest(path=path):
                self.assertIsNone(
                    DOCUMENTS.scoped_document_content_paths(
                        self.registry, (path,), self.current
                    )
                )

    def test_ordinary_document_limits_body_to_current_changed_path(self) -> None:
        selected = "docs/03.specs/0107-local-qa-and-release/tasks/tsk-0003-purpose-qa-and-ci.md"
        scope = DOCUMENTS.scoped_document_content_paths(
            self.registry, (selected,), self.current
        )
        self.assertEqual({path.as_posix() for path in scope}, {selected})

    def test_new_workload_directory_makes_selected_parent_matrix_fail(self) -> None:
        owner = PurePosixPath("gitops/workloads/README.md")
        reader_spec = importlib.util.spec_from_file_location(
            "p05_matrix_markdown_reader", ROOT / "scripts/validate-markdown-profiles.py"
        )
        assert reader_spec is not None and reader_spec.loader is not None
        reader = importlib.util.module_from_spec(reader_spec)
        sys.modules[reader_spec.name] = reader
        reader_spec.loader.exec_module(reader)
        current_text = (ROOT / owner).read_text(encoding="utf-8")
        source = ROOT / "gitops/workloads"
        with tempfile.TemporaryDirectory() as temporary:
            temporary_root = Path(temporary)
            target = temporary_root / "gitops/workloads"
            target.mkdir(parents=True)
            for child in source.iterdir():
                if child.is_dir():
                    (target / child.name).mkdir()
            matrix = CONTENT.MATRIXES[owner.as_posix()][0]
            baseline = CONTENT._matrix_findings(
                temporary_root, matrix, current_text, reader._document_content_table
            )
            self.assertNotIn("DOC-MATRIX-PARITY", {item[0] for item in baseline})
            (target / "new-workload").mkdir()
            stale = CONTENT._matrix_findings(
                temporary_root, matrix, current_text, reader._document_content_table
            )
            self.assertIn("DOC-MATRIX-PARITY", {item[0] for item in stale})
            scope = DOCUMENTS.scoped_document_content_paths(
                self.registry,
                ("gitops/workloads/new-workload/kustomization.yaml",),
                self.current,
            )
            self.assertIn(owner, scope)

    def test_deleted_last_cluster_child_exposes_missing_service_directory(self) -> None:
        owner = PurePosixPath("gitops/README.md")
        reader_spec = importlib.util.spec_from_file_location(
            "p05_service_matrix_reader", ROOT / "scripts/validate-markdown-profiles.py"
        )
        assert reader_spec is not None and reader_spec.loader is not None
        reader = importlib.util.module_from_spec(reader_spec)
        sys.modules[reader_spec.name] = reader
        reader_spec.loader.exec_module(reader)
        text = (ROOT / owner).read_text(encoding="utf-8")
        matrix = CONTENT.GITOPS_MATRIXES[0]
        with tempfile.TemporaryDirectory() as temporary:
            temporary_root = Path(temporary)
            local = temporary_root / "gitops/clusters/local"
            local.mkdir(parents=True)
            (temporary_root / "gitops/apps/root").mkdir(parents=True)
            baseline = CONTENT._matrix_findings(
                temporary_root, matrix, text, reader._document_content_table
            )
            self.assertNotIn("DOC-MATRIX-TARGET", {item[0] for item in baseline})
            shutil.rmtree(local)
            missing = CONTENT._matrix_findings(
                temporary_root, matrix, text, reader._document_content_table
            )
            self.assertIn("DOC-MATRIX-TARGET", {item[0] for item in missing})
        scope = DOCUMENTS.scoped_document_content_paths(
            self.registry,
            ("gitops/clusters/local/kustomization.yaml",),
            self.current,
        )
        self.assertIn(owner, scope)

    def test_deleted_last_guide_fails_unchanged_collection_index(self) -> None:
        owner = PurePosixPath("docs/05.operations/guides/README.md")
        reader_spec = importlib.util.spec_from_file_location(
            "p05_guide_index_reader", ROOT / "scripts/validate-markdown-profiles.py"
        )
        assert reader_spec is not None and reader_spec.loader is not None
        reader = importlib.util.module_from_spec(reader_spec)
        sys.modules[reader_spec.name] = reader
        reader_spec.loader.exec_module(reader)
        text = (ROOT / owner).read_text(encoding="utf-8")
        changed = "docs/05.operations/guides/0010-ci-cd-qa-reference-guide.md"
        with tempfile.TemporaryDirectory() as temporary:
            temporary_root = Path(temporary)
            folder = temporary_root / owner.parent
            folder.mkdir(parents=True)
            for path in (ROOT / owner.parent).glob("*.md"):
                (folder / path.name).write_text("", encoding="utf-8")
            navigation = self.registry.readme_navigation

            def findings():
                return CONTENT._index_findings(
                    temporary_root,
                    owner,
                    text,
                    reader._document_content_table,
                    navigation.index_columns,
                    navigation.optional_index_columns,
                )

            self.assertNotIn("DOC-INDEX-PARITY", {item[0] for item in findings()})
            (temporary_root / changed).unlink()
            self.assertIn("DOC-INDEX-PARITY", {item[0] for item in findings()})
        scope = DOCUMENTS.scoped_document_content_paths(
            self.registry, (changed,), self.current
        )
        self.assertIn(owner, scope)

    def test_new_incident_fails_unchanged_absence_router(self) -> None:
        owner = PurePosixPath("docs/05.operations/incidents/README.md")
        text = (ROOT / owner).read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as temporary:
            temporary_root = Path(temporary)
            folder = temporary_root / owner.parent
            folder.mkdir(parents=True)
            (folder / "README.md").write_text(text, encoding="utf-8")
            record = folder / "2026/inc-2026-new/incident.md"
            record.parent.mkdir(parents=True)
            record.write_text("incident evidence", encoding="utf-8")
            findings = CONTENT.validate_document_content(
                temporary_root,
                owner,
                text,
                lambda _text, _title: None,
                index_columns=(),
                optional_index_columns=(),
            )
            self.assertIn("DOC-INCIDENT-STATE", {item[0] for item in findings})
        scope = DOCUMENTS.scoped_document_content_paths(
            self.registry,
            ("docs/05.operations/incidents/2026/inc-2026-new/incident.md",),
            self.current,
        )
        self.assertIn(owner, scope)


if __name__ == "__main__":
    unittest.main()
