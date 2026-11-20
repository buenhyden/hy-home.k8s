from __future__ import annotations

import importlib.util
import hashlib
import json
import subprocess
from datetime import date, timedelta
import sys
import tempfile
import unittest
from pathlib import Path

from tests.form_headings import common_shell, form_body


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = REPOSITORY_ROOT / "scripts" / "validate-knowledge-surface.py"
REGISTRY_PATH = REPOSITORY_ROOT / "scripts" / "validation" / "registry.json"

FRONTMATTER = (
    "---\n"
    'title: "Sample Map"\n'
    'version: "0.1.0"\n'
    'type: "governance/knowledge"\n'
    'status: "active"\n'
    'owner: "platform"\n'
    'updated: "2026-09-07"\n'
    "---\n\n"
)

OWNER_TEXT = (
    "# Owner\n\n"
    "The reconciliation boundary keeps declarative desired state under version "
    "control so that every applied change arrives through a reviewed pull "
    "request rather than a direct cluster mutation.\n"
)

# The knowledge README is read only for its links; no registered form owns these headings.
README_TEMPLATE = (
    "# Common Knowledge\n\n"
    "## Item Index\n\n"
    "{entries}\n\n"
    "## Related Documents\n\n"
    "- nothing\n"
)


def load_validator():
    specification = importlib.util.spec_from_file_location(
        "knowledge_surface_validator_test_target", VALIDATOR_PATH
    )
    if specification is None or specification.loader is None:
        raise AssertionError("knowledge surface validator could not be loaded")
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


def document(
    rows: str,
    prose: str = "This map points at owners and states no policy of its own.",
    *,
    common_envelope: bool = False,
) -> str:
    sections = {
        "Overview": [prose],
        "Authority Boundary": ["Every row points; none decides."],
        "Pointer Index": [
            "| Area | Owner path | Entry path | Stays valid while |\n"
            "| --- | --- | --- | --- |\n" + rows
        ],
        "Validation and Refresh": ["The validator judges this file."],
        "Related Documents": ["- none"],
    }
    body = form_body("knowledge-map", sections)
    return (
        FRONTMATTER
        + "# Sample Map\n\n"
        + "\n\n".join(common_shell(body) if common_envelope else body)
        + "\n"
    )


class KnowledgeSurfaceValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.module = load_validator()
        self._directory = tempfile.TemporaryDirectory(prefix="knowledge-surface-")
        self.addCleanup(self._directory.cleanup)
        self.root = Path(self._directory.name)
        surface = self.root / ".agents" / "knowledge"
        surface.mkdir(parents=True)
        (self.root / "owner").mkdir()
        (self.root / "owner" / "README.md").write_text(OWNER_TEXT, encoding="utf-8")
        self.surface = surface

    def test_common_shell_preserves_pointer_rows_and_rejects_empty_table(self):
        self.write_readme("sample.md")
        sample = self.surface / "sample.md"
        row = "| Domain | `owner/README.md` | `owner/README.md` | Owner exists |"
        sample.write_text(document(row, common_envelope=True), encoding="utf-8")
        self.assertNotIn("KNOWLEDGE-POINTER-EMPTY", self.codes())
        sample.write_text(document("", common_envelope=True), encoding="utf-8")
        self.assertIn("KNOWLEDGE-POINTER-EMPTY", self.codes())

    def test_bounded_fact_metadata_invalidates_stale_and_sensitive_observations(self):
        owner = self.root / "owner/README.md"
        subprocess.run(
            ["git", "init", "-q", str(self.root)], check=True, capture_output=True
        )
        subprocess.run(
            ["git", "-C", str(self.root), "add", "owner/README.md"],
            check=True,
            capture_output=True,
        )
        record = {
            "owner": "platform",
            "scope": "owner navigation",
            "source": {
                "path": "owner/README.md",
                "sha256": hashlib.sha256(owner.read_bytes()).hexdigest(),
            },
            "observed_at": date.today().isoformat(),
            "valid_for": (date.today() + timedelta(days=30)).isoformat(),
            "invalidated_by": ["source", "scope", "approval", "validity"],
            "review_status": "advisory",
            "sensitivity": "public",
        }
        self.write_readme("sample.md")
        base = document(
            "| Domain | `owner/README.md` | `owner/README.md` | Owner exists |"
        )

        def findings(value):
            (self.surface / "sample.md").write_text(
                base + "\n```knowledge-fact\n" + json.dumps(value) + "\n```\n"
            )
            return self.module.validate_knowledge_surface(self.root)

        self.assertEqual(findings(record), [])
        private = self.root / "private.md"
        private.write_text("private-payload")
        self.assertTrue(
            findings(
                {
                    **record,
                    "source": {
                        "path": "private.md",
                        "sha256": hashlib.sha256(private.read_bytes()).hexdigest(),
                    },
                }
            )
        )
        for key in record:
            with self.subTest(missing=key):
                self.assertTrue(
                    findings(
                        {name: value for name, value in record.items() if name != key}
                    )
                )
        self.assertTrue(findings({**record, "valid_for": "2000-01-01"}))
        self.assertTrue(findings({**record, "sensitivity": "secret"}))
        self.assertTrue(findings({**record, "review_status": "expired"}))
        owner.write_text("Changed owner")
        self.assertTrue(findings(record))
        owner.unlink()
        self.assertTrue(findings(record))

    def write_readme(self, *names: str) -> None:
        entries = "\n".join(f"- [Sample]({name}): a map." for name in names)
        (self.surface / "README.md").write_text(
            README_TEMPLATE.format(entries=entries), encoding="utf-8"
        )

    def codes(self):
        return [
            finding.code
            for finding in self.module.validate_knowledge_surface(self.root)
        ]

    def test_valid_document_passes(self) -> None:
        self.write_readme("map.md")
        (self.surface / "map.md").write_text(
            document(
                "| Owner | `owner/` | `owner/README.md` | The owner keeps its scope |"
            ),
            encoding="utf-8",
        )
        self.assertEqual(self.codes(), [])

    def test_missing_owner_path_fails(self) -> None:
        self.write_readme("map.md")
        (self.surface / "map.md").write_text(
            document(
                "| Owner | `absent/` | `owner/README.md` | The owner keeps its scope |"
            ),
            encoding="utf-8",
        )
        self.assertIn("KNOWLEDGE-PATH-MISSING", self.codes())

    def test_missing_entry_path_fails(self) -> None:
        self.write_readme("map.md")
        (self.surface / "map.md").write_text(
            document(
                "| Owner | `owner/` | `owner/ABSENT.md` | The owner keeps its scope |"
            ),
            encoding="utf-8",
        )
        self.assertIn("KNOWLEDGE-PATH-MISSING", self.codes())

    def test_reproduced_policy_span_fails(self) -> None:
        self.write_readme("map.md")
        borrowed = (
            "The reconciliation boundary keeps declarative desired state under "
            "version control so that every applied change arrives through a "
            "reviewed pull request rather than a direct cluster mutation."
        )
        (self.surface / "map.md").write_text(
            document(
                "| Owner | `owner/` | `owner/README.md` | The owner keeps its scope |",
                prose=borrowed,
            ),
            encoding="utf-8",
        )
        self.assertIn("KNOWLEDGE-DUPLICATED-SPAN", self.codes())

    def test_index_membership_belongs_to_the_navigation_contract(self) -> None:
        self.write_readme()
        (self.surface / "map.md").write_text(
            document(
                "| Owner | `owner/` | `owner/README.md` | The owner keeps its scope |"
            ),
            encoding="utf-8",
        )
        self.assertNotIn("KNOWLEDGE-INDEX-MISSING", self.codes())

    def write_glossary(
        self,
        common: str,
        local: str = "",
        path: str = "docs/00.workspace/01.project/glossary.md",
    ) -> None:
        header = (
            "| Term ID | Term | Korean | Definition | Not to Confuse | Policy Owner "
            "| Contract Version |\n| --- | --- | --- | --- | --- | --- | --- |\n"
        )
        self.write_readme()
        glossary = self.root / path
        glossary.parent.mkdir(parents=True, exist_ok=True)
        glossary.write_text(
            FRONTMATTER.replace("governance/knowledge", "governance/vocabulary")
            + "# Repository Vocabulary\n\n## Purpose\n\nTerm meanings.\n\n"
            + "## Repository Vocabulary\n\n"
            + header
            + common
            + "\n\n## Local Extensions\n\n"
            + (header + local if local else "None.")
            + "\n\n## Maintenance\n\nOwners change rules.\n",
            encoding="utf-8",
        )

    def term(self, term_id: str, owner: str = "owner/README.md") -> str:
        return f"| {term_id} | Term | 용어 | A short meaning. | Other | `{owner}` | 1.0.0 |"

    def test_workspace_glossary_is_checked_where_it_lives(self) -> None:
        # Local definitions still need the same validation as common terms.
        self.write_glossary(self.term("TERM-ONE"), self.term("TERM-ONE"))
        self.assertIn("KNOWLEDGE-TERM-DUPLICATE", self.codes())

    def test_common_glossary_is_checked_as_vocabulary(self) -> None:
        self.write_glossary(
            self.term("TERM-COMMON", "absent/POLICY.md"),
            path=".agents/knowledge/glossary.md",
        )
        self.assertIn("KNOWLEDGE-PATH-MISSING", self.codes())
        self.assertNotIn("KNOWLEDGE-POINTER-EMPTY", self.codes())

    def test_duplicate_term_id_across_physical_glossaries_fails(self) -> None:
        self.write_glossary(self.term("TERM-SHARED"))
        self.write_glossary(
            self.term("TERM-SHARED"), path=".agents/knowledge/glossary.md"
        )
        self.assertIn("KNOWLEDGE-TERM-DUPLICATE", self.codes())

    def test_common_glossary_rejects_malformed_contract_version(self) -> None:
        self.write_glossary(
            self.term("TERM-COMMON").replace("1.0.0", "v1.0"),
            path=".agents/knowledge/glossary.md",
        )
        self.assertIn("KNOWLEDGE-CONTRACT-VERSION", self.codes())

    def test_valid_vocabulary_passes(self) -> None:
        self.write_glossary(self.term("TERM-ONE"), self.term("TERM-LOCAL-TWO"))
        self.assertEqual(self.codes(), [])

    def test_contract_version_requires_the_numeric_triplet_in_both_tables(self) -> None:
        common = self.term("TERM-ONE")
        local = self.term("TERM-LOCAL-TWO")
        for value in (
            "",
            "v14.7",
            "1.02.0",
            "1.2.0-rc.1",
            "1.2.0+custom",
            "\u00a01.0.0",
        ):
            for rows in (
                (common.replace("1.0.0", value), local),
                (common, local.replace("1.0.0", value)),
            ):
                with self.subTest(value=value, rows=rows):
                    self.write_glossary(*rows)
                    self.assertIn("KNOWLEDGE-CONTRACT-VERSION", self.codes())

    def test_overflow_cannot_supply_the_contract_version(self) -> None:
        common = self.term("TERM-ONE").replace("short meaning", r"short \| meaning")
        local = self.term("TERM-LOCAL-TWO")
        self.write_glossary(common, local)
        self.assertEqual(self.codes(), [])
        for common_row, local_row in (
            (common + " 1.0.0 |", local),
            (common, local + " 1.0.0 |"),
        ):
            with self.subTest(common=common_row, local=local_row):
                self.write_glossary(
                    common_row.replace("1.0.0 | 1.0.0", "v14.7 | 1.0.0"),
                    local_row.replace("1.0.0 | 1.0.0", "v14.7 | 1.0.0"),
                )
                self.assertIn("KNOWLEDGE-CONTRACT-VERSION", self.codes())

    def test_a_fenced_example_does_not_supply_a_contract_version(self) -> None:
        example = self.term("TERM-EXAMPLE").replace("1.0.0", "v14.7")
        self.write_glossary(f"{self.term('TERM-ONE')}\n\n```md\n{example}\n```")
        self.assertEqual(self.codes(), [])

    def test_vocabulary_without_terms_fails(self) -> None:
        self.write_glossary("")
        self.assertIn("KNOWLEDGE-VOCABULARY-EMPTY", self.codes())

    def test_malformed_term_id_fails(self) -> None:
        self.write_glossary(self.term("term-one"))
        self.assertIn("KNOWLEDGE-TERM-ID", self.codes())

    def test_duplicate_term_id_across_tables_fails(self) -> None:
        self.write_glossary(self.term("TERM-ONE"), self.term("TERM-ONE"))
        self.assertIn("KNOWLEDGE-TERM-DUPLICATE", self.codes())

    def test_missing_policy_owner_fails(self) -> None:
        self.write_glossary(self.term("TERM-ONE", "absent/POLICY.md"))
        self.assertIn("KNOWLEDGE-PATH-MISSING", self.codes())

    def test_definition_copying_its_owner_fails(self) -> None:
        borrowed = (
            "| TERM-ONE | Term | 용어 | The reconciliation boundary keeps declarative "
            "desired state under version control so that every applied change "
            "arrives through a reviewed pull request. | Other | "
            "`owner/README.md` | 1.0.0 |"
        )
        self.write_glossary(borrowed)
        self.assertIn("KNOWLEDGE-DUPLICATED-SPAN", self.codes())

    def test_definition_copying_korean_owner_text_fails(self) -> None:
        korean = (
            "선언된 원하는 상태는 버전 관리 아래에 두고 모든 적용 변경은 "
            "검토된 풀 요청을 거쳐 들어오며 클러스터를 직접 바꾸지 않는다"
        )
        (self.root / "owner" / "KO.md").write_text(korean + "\n", encoding="utf-8")
        self.write_glossary(
            f"| TERM-ONE | Term | 용어 | {korean} | Other | `owner/KO.md` | 1.0.0 |"
        )
        self.assertIn("KNOWLEDGE-DUPLICATED-SPAN", self.codes())

    def test_absent_surface_reports_nothing(self) -> None:
        empty = Path(self._directory.name) / "empty"
        empty.mkdir()
        self.assertEqual(self.module.validate_knowledge_surface(empty), [])


class KnowledgeSurfaceRepositoryTests(unittest.TestCase):
    # Whether this repository passes the validator is the gate's own result,
    # reported once per profile run over the snapshot the profile selected.
    # Asserting it again here would run the same check on the same bytes under
    # a second name. What belongs here is that the gate exists at all.

    def test_validator_is_registered(self) -> None:
        import json

        registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
        commands = [
            " ".join(str(part) for part in validator.get("argv", []))
            for validator in registry["validators"]
        ]
        self.assertTrue(
            any("validate-knowledge-surface.py" in command for command in commands),
            "the knowledge surface validator is not routed by the validation registry",
        )


if __name__ == "__main__":
    unittest.main()
