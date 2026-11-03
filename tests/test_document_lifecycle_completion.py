"""Completion-mode rejections over a mutated current package snapshot."""

from __future__ import annotations

import importlib.util
import json
import re
import sys
import unittest
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
FIXTURE = ROOT / "tests/fixtures/completion-package.json"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
SPEC = importlib.util.spec_from_file_location(
    "validate_document_lifecycle_completion_tested",
    SCRIPTS / "validate-document-lifecycle.py",
)
if SPEC is None or SPEC.loader is None:  # pragma: no cover - import boundary
    raise RuntimeError("cannot load document lifecycle validator")
VALIDATOR = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = VALIDATOR
SPEC.loader.exec_module(VALIDATOR)

from document_contracts import load_registry  # noqa: E402


class CompletionDiagnosticsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = load_registry(ROOT)
        blobs = VALIDATOR._index_blob_map(ROOT)
        documents, texts = VALIDATOR._snapshot_projection(ROOT, cls.registry, blobs)
        cls.documents, cls.texts = dict(documents), dict(texts)
        # A completed package leaves the tree, so a fixed accepted package is
        # injected instead of depending on whichever package is current.
        fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        for raw, text in fixture.items():
            path = PurePosixPath(raw)
            cls.texts[path] = text
            cls.documents[path] = VALIDATOR.document_from_text(cls.registry, path, text)
        cls.spec = next(
            path for path in map(PurePosixPath, fixture) if path.name == "spec.md"
        )
        schema_path = ROOT / "docs/99.templates/contracts/frontmatter.schema.json"
        cls.schema = json.loads(schema_path.read_text(encoding="utf-8"))

    def rules(self, documents, texts) -> set[str]:
        diagnostics = VALIDATOR._completion_document_diagnostics(
            ROOT,
            self.registry,
            (self.spec,),
            documents,
            texts,
            self.schema,
            base_mode="completion",
        )
        return {diagnostic.rule_id for diagnostic in diagnostics}

    def without(self, keep) -> tuple[dict, dict]:
        documents = {p: d for p, d in self.documents.items() if keep(p)}
        texts = {p: t for p, t in self.texts.items() if keep(p)}
        return documents, texts

    def test_complete_fixture_package_passes(self):
        self.assertFalse(
            self.rules(self.documents, self.texts)
            & {"COMPLETION-PLAN", "COMPLETION-TASK", "COMPLETION-CRITERIA"}
        )

    def test_missing_plan_is_rejected(self):
        plan = self.spec.parent / "plan.md"
        self.assertIn("COMPLETION-PLAN", self.rules(*self.without(lambda p: p != plan)))

    def test_missing_task_is_rejected(self):
        tasks = self.spec.parent / "tasks"
        documents, texts = self.without(lambda p: p.parent != tasks)
        self.assertIn("COMPLETION-TASK", self.rules(documents, texts))

    def test_missing_criteria_table_is_rejected(self):
        documents, texts = dict(self.documents), dict(self.texts)
        texts[self.spec] = re.sub(
            r"## Success Criteria & Verification Plan\n.*?(?=\n## )",
            "## Success Criteria & Verification Plan\n\nNone.\n",
            texts[self.spec],
            flags=re.S,
        )
        self.assertIn("COMPLETION-CRITERIA", self.rules(documents, texts))


if __name__ == "__main__":
    unittest.main()
