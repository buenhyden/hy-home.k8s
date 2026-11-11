"""Each front-matter rule of the Markdown profile validator fires on its own fault."""

from __future__ import annotations

import datetime as dt
import importlib.util
import re
import sys
import unittest
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
SPEC = importlib.util.spec_from_file_location(
    "frontmatter_negatives_markdown_profiles",
    SCRIPTS / "validate-markdown-profiles.py",
)
if SPEC is None or SPEC.loader is None:  # pragma: no cover - import boundary
    raise RuntimeError("cannot load markdown profile validator")
PROFILES = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = PROFILES
SPEC.loader.exec_module(PROFILES)

from document_contracts import classify_path, load_registry  # noqa: E402

TODAY = dt.date(2026, 11, 11)
RULE = PurePosixPath(".agents/governance/document-lifecycle.md")
FOLDER_AGENTS = PurePosixPath("docs/AGENTS.md")
AUDIT_FORM = ROOT / "docs/99.templates/templates/references/audit.template.md"
AUDIT_COLUMNS = [
    "ID",
    "Finding or gap",
    "Requirement",
    "Fact or hypothesis",
    "Severity",
    "Evidence",
    "Action",
    "Acceptance",
]


class FrontmatterNegativeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = load_registry(ROOT)
        cls.source = (ROOT / RULE).read_text(encoding="utf-8")

    def rules(self, text: str, path: PurePosixPath = RULE) -> set[str]:
        profile = next(
            item
            for item in self.registry.profiles
            if item.profile_id == classify_path(self.registry, path).profile_id
        )
        found = PROFILES.validate_document_text(
            text, path, profile, "strict", today=TODAY, include_body=False
        )
        return {item.rule_id for item in found if item.rule_id.startswith("FM-")}

    def mutate(self, pattern: str, replacement) -> str:
        text, count = re.subn(pattern, replacement, self.source, count=1, flags=re.M)
        self.assertEqual(count, 1, pattern)
        return text

    def test_valid_control_has_no_frontmatter_finding(self) -> None:
        self.assertEqual(self.rules(self.source), set())

    def test_duplicate_key(self) -> None:
        text = self.mutate(r'^(owner: "platform")$', r'\1\nowner: "platform"')
        self.assertEqual(self.rules(text), {"FM-DUPLICATE-KEY"})

    def test_invalid_date(self) -> None:
        text = self.mutate(r'^updated: ".*"$', 'updated: "2026-13-40"')
        self.assertEqual(self.rules(text), {"FM-DATE"})

    def test_future_date(self) -> None:
        text = self.mutate(r'^updated: ".*"$', 'updated: "2999-01-01"')
        self.assertEqual(self.rules(text), {"FM-FUTURE-DATE"})

    def test_unregistered_key(self) -> None:
        text = self.mutate(r'^(owner: "platform")$', r'\1\nreviewer: "someone"')
        self.assertEqual(self.rules(text), {"FM-KEYSET"})

    def test_key_order(self) -> None:
        text = self.mutate(
            r'^(version: ".*")\n(type: ".*")$', lambda m: f"{m[2]}\n{m[1]}"
        )
        self.assertEqual(self.rules(text), {"FM-KEY-ORDER"})

    def test_forbidden_frontmatter(self) -> None:
        source = (ROOT / FOLDER_AGENTS).read_text(encoding="utf-8")
        self.assertEqual(self.rules(source, FOLDER_AGENTS), set())
        text = '---\ntitle: "x"\n---\n' + source
        self.assertEqual(self.rules(text, FOLDER_AGENTS), {"FM-FORBIDDEN"})


class AuditFormColumnsTest(unittest.TestCase):
    def test_findings_table_has_the_finding_columns(self) -> None:
        text = AUDIT_FORM.read_text(encoding="utf-8")
        section = text.split("### Findings and Gaps", 1)[1]
        lines = section.splitlines()
        index = next(i for i, line in enumerate(lines) if line.startswith("|"))
        columns = [cell.strip() for cell in lines[index].strip("|").split("|")]
        self.assertEqual(columns, AUDIT_COLUMNS)
        self.assertEqual(lines[index + 2].count("Author prompt"), len(AUDIT_COLUMNS))


if __name__ == "__main__":
    unittest.main()
