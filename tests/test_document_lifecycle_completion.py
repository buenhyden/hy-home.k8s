"""Completion-mode rejections over a mutated current package snapshot."""

from __future__ import annotations

import importlib.util
import json
import re
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
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
        cls.documents, cls.texts = VALIDATOR._snapshot_projection(
            ROOT, cls.registry, blobs
        )
        specs = sorted(
            path
            for path, document in cls.documents.items()
            if path.parts[:2] == ("docs", "03.specs")
            and path.name == "spec.md"
            and document.profile_id == "sdlc/spec"
        )
        if not specs:
            raise unittest.SkipTest("no current Spec package in the index")
        cls.spec = specs[0]
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
