"""Synthetic cases for the document language contract (SPEC-0093)."""

from __future__ import annotations

import dataclasses
import importlib.util
import sys
import unittest
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import document_contracts as contracts  # noqa: E402
import document_language as language  # noqa: E402


def load_profiles_validator():
    spec = importlib.util.spec_from_file_location(
        "validate_markdown_profiles_lang",
        ROOT / "scripts/validate-markdown-profiles.py",
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


PROFILES = load_profiles_validator()
FENCE = "`" * 3
KO = "\uc774 \ubb38\uc11c\ub294 \ud50c\ub7ab\ud3fc\uc744 \uc124\uba85\ud55c\ub2e4."
EN = "This paragraph explains the platform bootstrap order in plain English words."


def contract(pending=()):
    return contracts.DocumentLanguage(
        english_only_roots=(".agents/", ".claude/", ".codex/"),
        english_only_suffixes=frozenset({".md", ".json", ".yaml"}),
        korean_first_profiles=frozenset(
            {"common/readme-stage-index", "operation/runbook"}
        ),
        english_sections=frozenset({"AI Agent Requirements"}),
        min_latin_words=8,
        pending_paths=frozenset(PurePosixPath(p) for p in pending),
    )


def found(text, kind):
    return sorted({code for code, _ in language.findings(text, kind, contract())})


class ClassifyTests(unittest.TestCase):
    def kind(
        self, path, profile="sdlc/spec", mode="authored", output=None, terminal=False
    ):
        return language.classify(
            PurePosixPath(path), profile, mode, output, terminal, contract()
        )

    def test_english_only_root_wins_over_readme_profile(self):
        self.assertEqual(
            self.kind(".agents/roles/README.md", "common/readme-stage-index", "router"),
            "english-only",
        )

    def test_profiles_pick_the_language(self):
        self.assertEqual(
            self.kind("docs/README.md", "common/readme-stage-index", "router"),
            "korean-first",
        )
        self.assertEqual(self.kind("docs/03.specs/x/spec.md"), "english-first")

    def test_templates_take_their_output_language(self):
        self.assertEqual(
            self.kind(
                "docs/99.templates/templates/operations/runbook.template.md",
                "common/template-operation-runbook",
                "template",
                "operation/runbook",
            ),
            "template-korean",
        )
        self.assertEqual(
            self.kind(
                "docs/99.templates/templates/specs/spec.template.md",
                "common/template-sdlc-spec",
                "template",
                "sdlc/spec",
            ),
            "template-english",
        )

    def test_unchecked_documents(self):
        self.assertIsNone(self.kind("docs/98.archive/retired/x.md"))
        self.assertEqual(
            self.kind(
                "docs/98.archive/README.md", "common/readme-stage-index", "router"
            ),
            "korean-first",
        )
        self.assertIsNone(self.kind("docs/03.specs/x/spec.md", terminal=True))
        self.assertIsNone(self.kind("AGENTS.md", "common/root-provider-shim", "native"))
        self.assertIsNone(self.kind("t.md", "common/template-x", "template", None))


class EnglishTests(unittest.TestCase):
    def test_hangul_in_prose_fails_and_code_passes(self):
        self.assertEqual(
            found(f"# T\n\n{EN} {KO}\n", "english-first"), ["LANG-ENGLISH-FIRST"]
        )
        code = f"# T\n\nUse `\uc0c1\ud0dc` here.\n\n{FENCE}\n\ud55c\uae00\n{FENCE}\n"
        self.assertEqual(found(code, "english-first"), [])

    def test_a_longer_fence_closes_only_on_its_own_length(self):
        text = f"{FENCE}`md\n{FENCE}\n{FENCE}`\n\n{KO}\n"
        self.assertEqual(found(text, "english-first"), ["LANG-ENGLISH-FIRST"])
        info = f"{FENCE}\n{FENCE}bash\n{KO}\n{FENCE}\n"
        self.assertEqual(found(info, "english-first"), [])

    def test_frontmatter_is_not_judged(self):
        text = f'---\ntitle: "\ud55c\uae00"\n---\n\n{EN}\n'
        self.assertEqual(found(text, "english-first"), [])

    def test_english_only_counts_every_byte(self):
        self.assertEqual(found("x: `\ud55c`\n", "english-only"), ["LANG-ENGLISH-ONLY"])


class KoreanTests(unittest.TestCase):
    def test_english_paragraph_fails_and_korean_passes(self):
        self.assertEqual(found(f"# T\n\n{EN}\n", "korean-first"), ["LANG-KOREAN-FIRST"])
        mixed = f"# T\n\n{KO} ArgoCD bootstrap order and GitOps sync waves.\n"
        self.assertEqual(found(mixed, "korean-first"), [])

    def test_blockquote_paragraph_is_judged(self):
        self.assertEqual(
            found(f"# T\n\n> {EN}\n", "korean-first"), ["LANG-KOREAN-FIRST"]
        )

    def test_headings_tables_lists_comments_and_code_are_not_judged(self):
        text = (
            f"# {EN}\n\n## Overview\n\n| {EN} |\n| --- |\n\n"
            f"- {EN}\n  {EN}\n{EN}\n\n  {EN}\n\n"
            f"1. {EN}\n\n<!-- {EN} -->\n\n{FENCE}\n{EN}\n{FENCE}\n\n{KO}\n"
        )
        self.assertEqual(found(text, "korean-first"), [])

    def test_paragraph_after_a_list_is_judged(self):
        text = f"# T\n\n- {KO}\n\n{EN}\n"
        self.assertEqual(found(text, "korean-first"), ["LANG-KOREAN-FIRST"])

    def test_link_destinations_do_not_count(self):
        link = "[RUN-0001](./runbooks/0001-argocd-platform-bootstrap-runbook-with-long-name.md)"
        self.assertEqual(found(f"# T\n\n{link}\n", "korean-first"), [])

    def test_short_english_line_passes(self):
        self.assertEqual(found("# T\n\nSee the runbook.\n", "korean-first"), [])

    def test_english_section_inside_korean_document(self):
        text = f"# T\n\n{KO}\n\n## AI Agent Requirements\n\n{EN}\n"
        self.assertEqual(found(text, "korean-first"), [])
        bad = f"# T\n\n{KO}\n\n## AI Agent Requirements\n\n{KO}\n"
        self.assertEqual(found(bad, "korean-first"), ["LANG-ENGLISH-FIRST"])

    def test_english_section_judges_lists_tables_and_qualified_headings(self):
        for body in (f"- {KO}\n", f"| a | {KO} |\n| --- | --- |\n"):
            with self.subTest(body=body):
                text = f"# T\n\n## AI Agent Requirements\n\n{body}"
                self.assertEqual(found(text, "korean-first"), ["LANG-ENGLISH-FIRST"])
        qualified = f"# T\n\n## AI Agent Requirements (Optional)\n\n{KO}\n"
        self.assertEqual(found(qualified, "korean-first"), ["LANG-ENGLISH-FIRST"])
        other = f"# T\n\n## AI Agent Requirementsx\n\n{KO}\n"
        self.assertEqual(found(other, "korean-first"), [])

    def test_blockquote_holds_lists_and_fences(self):
        self.assertEqual(found(f"> - {EN}\n", "korean-first"), [])
        fenced = f"> {FENCE}\n> {EN}\n> {FENCE}\n"
        self.assertEqual(found(fenced, "korean-first"), [])

    def test_autolink_and_inline_html_lines_are_prose(self):
        for line in (f"<https://example.com> {EN}", f"<kbd>Ctrl</kbd> {EN}"):
            with self.subTest(line=line):
                self.assertEqual(
                    found(line + "\n", "korean-first"), ["LANG-KOREAN-FIRST"]
                )
        self.assertEqual(found(f"<div>{EN}</div>\n", "korean-first"), [])


class TemplateTests(unittest.TestCase):
    def test_korean_template_prompts_need_hangul(self):
        good = f"## Overview\n\n<!-- Author prompt: {KO} -->\n"
        bad = "## Overview\n\n<!-- Author prompt: explain the reader. -->\n"
        self.assertEqual(found(good, "template-korean"), [])
        self.assertEqual(found(bad, "template-korean"), ["LANG-TEMPLATE"])

    def test_english_template_rejects_hangul(self):
        bad = f"## Overview\n\n<!-- Author prompt: {KO} -->\n"
        self.assertEqual(found(bad, "template-english"), ["LANG-TEMPLATE"])


class ValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = contracts.load_registry(ROOT)
        cls.profiles = {p.profile_id: p for p in cls.registry.profiles}

    def codes(self, docs, pending=(), english_only=None):
        registry = dataclasses.replace(
            self.registry, document_language=contract(pending)
        )
        items = [
            (PurePosixPath(path), self.profiles[profile], text)
            for path, profile, text in docs
        ]
        return sorted(
            {
                item.rule_id
                for item in PROFILES.document_language_diagnostics(
                    registry, items, english_only or {}
                )
            }
        )

    def test_pending_document_is_skipped_until_it_passes(self):
        doc = ("docs/README.md", "common/readme-stage-index", f"# D\n\n{EN}\n")
        self.assertEqual(self.codes([doc]), ["LANG-KOREAN-FIRST"])
        self.assertEqual(self.codes([doc], pending=("docs/README.md",)), [])
        fixed = ("docs/README.md", "common/readme-stage-index", f"# D\n\n{KO}\n")
        self.assertEqual(
            self.codes([fixed], pending=("docs/README.md",)), ["LANG-PENDING"]
        )

    def test_untracked_or_unchecked_pending_path_fails(self):
        self.assertEqual(self.codes([], pending=("docs/missing.md",)), ["LANG-PENDING"])

    def test_terminal_document_is_not_checked(self):
        doc = (
            "docs/03.specs/0001-x/spec.md",
            "sdlc/spec",
            f'---\ntitle: "X"\nstatus: "done"\n---\n\n{KO}\n',
        )
        self.assertEqual(self.codes([doc]), [])

    def test_english_only_texts_are_checked(self):
        texts = {PurePosixPath(".agents/x.yaml"): "a: \ud55c\n"}
        self.assertEqual(self.codes([], english_only=texts), ["LANG-ENGLISH-ONLY"])


class RegistryTests(unittest.TestCase):
    def raw(self, **changes):
        value = {
            "english_only_roots": [".agents/"],
            "english_only_suffixes": [".md"],
            "korean_first_profiles": ["common/readme-stage-index"],
            "english_sections": ["AI Agent Requirements"],
            "min_latin_words": 8,
            "pending_paths": [],
        }
        value.update(changes)
        return {"document_language": value}

    def faults(self, **changes):
        profiles = {
            "common/readme-stage-index": {"mode": "router"},
            "common/root-provider-shim": {"mode": "native"},
        }
        return [
            item.rule_id
            for item in contracts._document_language_registry_diagnostics(
                self.raw(**changes), profiles
            )
        ]

    def test_consistent_contract_passes(self):
        self.assertEqual(self.faults(), [])

    def test_contradictions_fail(self):
        for changes in (
            {"korean_first_profiles": ["missing/profile"]},
            {"korean_first_profiles": ["common/root-provider-shim"]},
            {"english_only_roots": [".agents"]},
            {"english_only_suffixes": ["md"]},
            {"english_sections": [""]},
            {"min_latin_words": 0},
            {"pending_paths": [".agents/README.md"]},
        ):
            with self.subTest(changes=changes):
                self.assertEqual(self.faults(**changes), ["REGISTRY_DOCUMENT_LANGUAGE"])

    def test_repository_registry_loads_the_contract(self):
        loaded = contracts.load_registry(ROOT).document_language
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded.min_latin_words, 8)


if __name__ == "__main__":
    unittest.main()
