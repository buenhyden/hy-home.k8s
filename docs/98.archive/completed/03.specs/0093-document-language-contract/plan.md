---
title: "Document Language Contract Implementation Plan"
version: "0.3.0"
type: "sdlc/plan"
status: "done"
owner: "platform"
updated: "2026-09-26"
layer: "specs"
artifact_id: "SPEC-0093-PLAN-0001"
---

# Document Language Contract Implementation Plan

## Global Constraints

- Goal: every current document is written in the language its profile
  names, under one registry contract that one validator enforces.
- Spec: [SPEC-0093](spec.md). Every work package implicitly includes these
  constraints.
- The request owner approved the design and the Spec on 2026-09-26. Work runs
  on the local branch `readme-navigation-contract` after `87de7188`. Push,
  pull request, merge, and live actions are not authorized.
- Each commit runs `python3 scripts/qa.py staged` over its exact index and
  `git diff --check`. A commit that changes Python first runs the whole suite
  (`python3 -m unittest discover -s tests -t .`). No hook bypass, no
  `--no-verify`, and no weakened assertion.
- Contract values are exact:
  - English-only roots: `.agents/`, `.claude/`, `.codex/`.
  - English-only suffixes: `.md`, `.toml`, `.json`, `.sh`, `.yaml`, `.yml`.
  - Korean-first profiles: the nine `common/readme-*` router profiles and the
    five `operation/*` profiles.
  - English sections: `AI Agent Requirements`, `Agent Execution Notes`,
    `Agent Harness Requirements`.
  - `min_latin_words`: `8`.
- Hangul means the ranges `U+AC00`-`U+D7A3`, `U+1100`-`U+11FF`, and
  `U+3130`-`U+318F`.
- A conversion changes prose only. Identifiers, required headings, tables of
  record, links, commands, paths, code, and meaning stay the same.
- The author prompt marker stays `Author prompt:`, which `quality.py` pins.
  Only the prompt text after the marker changes language.
- Out of scope: retained bodies under `docs/98.archive/`, terminal-state
  documents, native, non-target, and evidence profiles, and lifecycle states
  and edges.

## Overview

The Plan first adds the `document_language` registry contract and its
validator, with every current violator in `pending_paths`. The same commit
deletes the three language blocks in `quality.py`. Each later work package
converts one area and removes it from `pending_paths`, so every commit is
green and the list only shrinks.

## Context

**Profile validator.** The per-document loop lives in
`scripts/validate-markdown-profiles.py`.
- `main` enumerates every tracked target Markdown file through
  `enumerate_target_markdown`, resolves each profile with `classify_path`, and
  builds `identity_documents` as `(path, profile, text)` triples.
- The language check reads those triples, so it always sees the whole corpus,
  even under `--include-path`.

**Registry types.** In `scripts/document_contracts.py`:
- `DocumentProfile` carries `profile_id`, `mode`, and `template`.
- `Registry.lifecycle_domains` carries each domain's `profile_ids` and
  `validation_class(state)`.
- Registry contracts are typed and loaded here. `readme_navigation`, with
  `_readme_navigation_from_mapping` and
  `_readme_navigation_registry_diagnostics`, is the pattern to copy.
- Top-level registry keys are admitted by `OPTIONAL_TOP_LEVEL_KEYS` in
  `scripts/document_authority.py`.

**Blocks being replaced.** All three live in
`scripts/validation/repository/quality.py`:
1. `english_first_terminal_states` and the Stage 03 loop after it.
2. The `tracked_language_roots` loop.
3. `agent_section_headings`, `current_agent_language_scan_text`, the
   `archive_language_probe` checks, and the agent-section loop.

**Tests that pin them:**
- `tests/test_repository_quality_rules.py`, through
  `english_first_terminal_states` and
  `test_english_first_scope_skips_only_terminal_stage03_documents`.
- `tests/test_common_agents_document_routes.py`, through
  `test_common_agent_documents_and_native_sidecars_stay_english_only`.

**Fixture registries.** These prune profiles and pop or name
`readme_navigation`; the new key needs the same treatment at each site:
- `tests/archive_generation_fixture.py`
- `tests/test_document_lifecycle_cumulative_history.py`
- `tests/test_document_strict_cutover.py` (two closed key sets)
- `tests/test_generic_migration_recovery.py`

## Goals & In-Scope

Deliver WP-001 to WP-008 below:
- the contract, the module, and the validator;
- the replacement of the three `quality.py` blocks;
- the template prompts;
- the README, operations, requirement, and architecture conversions, plus any
  remaining path;
- the governance sentence and the evidence.

## Non-Goals & Out-of-Scope

No new QA lane, no archive body edit, no change to the meaning of a decision
or requirement, no lifecycle change, and no push.

## Work Breakdown

| ID | Work package | Depends on | Entry gate | Exit evidence |
| --- | --- | --- | --- | --- |
| WP-001 | Propose the package | None | Spec approved | Staged QA |
| WP-002 | Contract, module, validator, tests; initial `pending_paths`; remove the `quality.py` blocks; activation | WP-001 | Plan approved | Focused tests, whole suite, staged QA |
| WP-003 | Korean author prompts in Korean-output templates | WP-002 | Validator green | Profile gate, staged QA |
| WP-004 | READMEs to Korean | WP-003 | Validator green | Staged QA |
| WP-005 | Operations documents to Korean | WP-004 | Validator green | Staged QA |
| WP-006 | Requirements to English | WP-005 | Validator green | Staged QA, whole suite |
| WP-007 | Architecture decisions, descriptions, and any remaining path | WP-006 | Validator green | Staged QA, whole suite |
| WP-008 | Governance sentence, evidence, full QA, close | WP-007 | `pending_paths` is empty | Full QA |

Every work package runs directly, in order. WP-002 shares code with every
later check. The conversions are prose work, one area per commit, and one
reviewer checks each against the source meaning.

### WP-001: Propose the package

**Files:**
- Create `spec.md`, `plan.md`, and
  `tasks/tsk-0001-converge-document-language.md` in this package.
- Modify `docs/03.specs/README.md`: add a tree entry and an index row after
  the 0091 entries, with a Korean purpose that reads
  "document language contract".
- Modify `docs/01.requirements/0003-workspace-agent-governance-platform.md`:
  add one reciprocal sentence after the SPEC-0091 sentence.

- [ ] Add to REQ-0003, after the SPEC-0091 sentence:
  `Stating each document's language in one registry contract is owned by
  [SPEC-0093](../03.specs/0093-document-language-contract/spec.md).`
- [ ] Run `python3 scripts/qa.py staged`. Expected: every selected gate PASS.
- [ ] Commit `docs(specs): propose SPEC-0093 for a document language contract`.

### WP-002: Contract, validator, and tests

**Files:**
- Create: `scripts/document_language.py`, `tests/test_document_language.py`
- Modify: `docs/99.templates/contracts/document-profile.schema.json` (top-level `properties`)
- Modify: `docs/99.templates/registry.json` (new top-level `document_language`)
- Modify: `scripts/document_authority.py` (`OPTIONAL_TOP_LEVEL_KEYS`)
- Modify: `scripts/document_contracts.py` (dataclass, `Registry` field, loader, self-check)
- Modify: `scripts/validate-markdown-profiles.py` (diagnostics and `main` wiring)
- Modify: `scripts/validation/repository/quality.py` (delete three blocks)
- Modify: `tests/test_repository_quality_rules.py`, `tests/test_common_agents_document_routes.py`
- Modify: the four fixture files named in Context
- Modify: this package's Spec, Plan, and Task (`draft` to `active`, `queued` to `in-progress`)

**Interfaces produced:**
- `document_contracts.DocumentLanguage(english_only_roots: tuple[str, ...], english_only_suffixes: frozenset[str], korean_first_profiles: frozenset[str], english_sections: frozenset[str], min_latin_words: int, pending_paths: frozenset[PurePosixPath])`
- `Registry.document_language: DocumentLanguage | None`
- `document_language.classify(path: PurePosixPath, profile_id: str, mode: str, template_output: str | None, terminal: bool, contract) -> str | None`.
  It returns `english-only`, `english-first`, `korean-first`,
  `template-korean`, `template-english`, or `None`.
- `document_language.findings(text: str, language: str, contract) -> list[tuple[str, str]]`,
  which returns `(rule_id, detail)` pairs.
- `validate-markdown-profiles.document_language_diagnostics(registry, documents: Sequence[tuple[PurePosixPath, DocumentProfile, str]], english_only_texts: Mapping[PurePosixPath, str]) -> list[Diagnostic]`

- [ ] **Step 1: Write the failing tests** in `tests/test_document_language.py`:

```python
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
        "validate_markdown_profiles_lang", ROOT / "scripts/validate-markdown-profiles.py"
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
        korean_first_profiles=frozenset({"common/readme-stage-index", "operation/runbook"}),
        english_sections=frozenset({"AI Agent Requirements"}),
        min_latin_words=8,
        pending_paths=frozenset(PurePosixPath(p) for p in pending),
    )


def found(text, kind):
    return sorted({code for code, _ in language.findings(text, kind, contract())})


class ClassifyTests(unittest.TestCase):
    def kind(self, path, profile="sdlc/spec", mode="authored", output=None, terminal=False):
        return language.classify(PurePosixPath(path), profile, mode, output, terminal, contract())

    def test_english_only_root_wins_over_readme_profile(self):
        self.assertEqual(
            self.kind(".agents/roles/README.md", "common/readme-stage-index", "router"),
            "english-only",
        )

    def test_profiles_pick_the_language(self):
        self.assertEqual(
            self.kind("docs/README.md", "common/readme-stage-index", "router"), "korean-first"
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
            self.kind("docs/98.archive/README.md", "common/readme-stage-index", "router"),
            "korean-first",
        )
        self.assertIsNone(self.kind("docs/03.specs/x/spec.md", terminal=True))
        self.assertIsNone(self.kind("AGENTS.md", "common/root-provider-shim", "native"))
        self.assertIsNone(self.kind("t.md", "common/template-x", "template", None))


class EnglishTests(unittest.TestCase):
    def test_hangul_in_prose_fails_and_code_passes(self):
        self.assertEqual(found(f"# T\n\n{EN} {KO}\n", "english-first"), ["LANG-ENGLISH-FIRST"])
        code = f"# T\n\nUse `\uc0c1\ud0dc` here.\n\n{FENCE}\n\ud55c\uae00\n{FENCE}\n"
        self.assertEqual(found(code, "english-first"), [])

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
        self.assertEqual(found(f"# T\n\n> {EN}\n", "korean-first"), ["LANG-KOREAN-FIRST"])

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
        registry = dataclasses.replace(self.registry, document_language=contract(pending))
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
        self.assertEqual(self.codes([fixed], pending=("docs/README.md",)), ["LANG-PENDING"])

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
```

- [ ] **Step 2: Run to verify failure.** Run
  `python3 -m unittest tests.test_document_language`. Expected:
  `ModuleNotFoundError: No module named 'document_language'`.

- [ ] **Step 3: Create `scripts/document_language.py`:**

```python
"""SPEC-0093: pure rules that judge a document's language."""

from __future__ import annotations

import re
from pathlib import PurePosixPath
from typing import Any

HANGUL = re.compile(r"[\uac00-\ud7a3\u1100-\u11ff\u3130-\u318f]")
LATIN_WORD = re.compile(r"[A-Za-z][A-Za-z'’-]*")
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
CODE_SPAN = re.compile(r"(`+)(?!`).*?(?<!`)\1(?!`)")
LINK_DESTINATION = re.compile(r"\]\([^)]*\)|\]\[[^\]]*\]")
BARE_URL = re.compile(r"<?https?://[^\s>]+>?")
COMMENT = re.compile(r"<!--.*?-->", re.S)
HEADING = re.compile(r"^ {0,3}(#{1,6})\s+(.*?)\s*#*\s*$")
LIST_ITEM = re.compile(r"^ {0,3}(?:[-*+]|\d{1,9}[.)])(?:\s|$)")
REFERENCE_DEFINITION = re.compile(r"^ {0,3}\[[^\]]+\]:\s")
AUTHOR_PROMPT = re.compile(r"<!--\s*Author prompt:(.*?)-->", re.S)
ARCHIVE_PREFIX = "docs/98.archive/"
ARCHIVE_INDEX = "docs/98.archive/README.md"


def _body(text: str) -> str:
    """Blank the frontmatter so line numbers stay true."""

    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            return "\n" * text[: end + 4].count("\n") + text[end + 4 :]
    return text


def _blank_comments(text: str) -> str:
    return COMMENT.sub(lambda match: "\n" * match.group(0).count("\n"), text)


def _outside_code(text: str) -> list[str]:
    """Lines with fenced blocks blanked and code spans removed."""

    lines: list[str] = []
    fence: str | None = None
    for line in text.split("\n"):
        opener = FENCE.match(line)
        if fence is None and opener:
            fence = opener.group(1)[0] * 3
            lines.append("")
            continue
        if fence is not None:
            if line.strip().startswith(fence):
                fence = None
            lines.append("")
            continue
        lines.append(CODE_SPAN.sub("", line))
    return lines


def _hangul_lines(lines: list[str]) -> list[str]:
    return [
        f"line {number}: {line.strip()[:60]}"
        for number, line in enumerate(lines, start=1)
        if HANGUL.search(line)
    ]


def _paragraphs(lines: list[str]) -> list[tuple[str | None, str]]:
    """Plain and blockquote paragraphs, each with its H2 section."""

    found: list[tuple[str | None, str]] = []
    section: str | None = None
    buffer: list[str] = []
    in_list = False
    after_blank = True

    def flush() -> None:
        if buffer:
            found.append((section, " ".join(buffer)))
            buffer.clear()

    for line in lines:
        stripped = line.strip()
        heading = HEADING.match(line)
        if heading:
            flush()
            in_list = False
            level = len(heading.group(1))
            if level == 1:
                section = None
            elif level == 2:
                section = heading.group(2)
            after_blank = True
            continue
        if not stripped:
            flush()
            after_blank = True
            continue
        if LIST_ITEM.match(line):
            flush()
            in_list, after_blank = True, False
            continue
        if in_list:
            # An indented line, or a lazy line right after the item, continues it.
            if line.startswith((" ", "\t")) or not after_blank:
                after_blank = False
                continue
            in_list = False
        after_blank = False
        if (
            stripped.startswith(("|", "<"))
            or REFERENCE_DEFINITION.match(line)
            or line.startswith(("    ", "\t"))
        ):
            flush()
            continue
        buffer.append(stripped.lstrip(">").strip() if stripped.startswith(">") else stripped)
    flush()
    return found


def _latin_words(paragraph: str) -> int:
    text = BARE_URL.sub("", LINK_DESTINATION.sub("]", paragraph))
    return len(LATIN_WORD.findall(text))


def classify(
    path: PurePosixPath,
    profile_id: str,
    mode: str,
    template_output: str | None,
    terminal: bool,
    contract: Any,
) -> str | None:
    """Name the language rule a document answers to, or None when unchecked."""

    value = path.as_posix()
    if value.startswith(contract.english_only_roots):
        return "english-only"
    if value.startswith(ARCHIVE_PREFIX) and value != ARCHIVE_INDEX:
        return None
    if mode == "template":
        if template_output is None:
            return None
        korean = template_output in contract.korean_first_profiles
        return "template-korean" if korean else "template-english"
    if mode not in {"authored", "router"} or terminal:
        return None
    if profile_id in contract.korean_first_profiles:
        return "korean-first"
    return "english-first"


def findings(text: str, language: str, contract: Any) -> list[tuple[str, str]]:
    """Return (rule_id, detail) pairs for one document under one language."""

    if language == "english-only":
        return [("LANG-ENGLISH-ONLY", item) for item in _hangul_lines(text.split("\n"))]
    body = _body(text)
    if language == "template-korean":
        return [
            ("LANG-TEMPLATE", f"author prompt without Hangul: {prompt.strip()[:60]}")
            for prompt in AUTHOR_PROMPT.findall(body)
            if not HANGUL.search(prompt)
        ]
    if language == "template-english":
        return [("LANG-TEMPLATE", item) for item in _hangul_lines(_outside_code(body))]
    if language == "english-first":
        return [("LANG-ENGLISH-FIRST", item) for item in _hangul_lines(_outside_code(body))]
    result: list[tuple[str, str]] = []
    for section, paragraph in _paragraphs(_outside_code(_blank_comments(body))):
        if section in contract.english_sections:
            if HANGUL.search(paragraph):
                result.append(("LANG-ENGLISH-FIRST", f"{section}: {paragraph[:60]}"))
            continue
        if not HANGUL.search(paragraph) and _latin_words(paragraph) >= contract.min_latin_words:
            result.append(("LANG-KOREAN-FIRST", paragraph[:60]))
    return result
```

- [ ] **Step 4: Add the contract type, loader, and self-check** in
  `scripts/document_contracts.py`, after `class ReadmeNavigation`:

```python
@dataclass(frozen=True)
class DocumentLanguage:
    """SPEC-0093: which language each document is written in."""

    english_only_roots: tuple[str, ...]
    english_only_suffixes: frozenset[str]
    korean_first_profiles: frozenset[str]
    english_sections: frozenset[str]
    min_latin_words: int
    pending_paths: frozenset[PurePosixPath]
```

  Then:
  1. Add `document_language: DocumentLanguage | None = None` as the last
     field of `Registry`.
  2. In the typed-registry builder, add
     `document_language=_document_language_from_mapping(raw.get("document_language")),`.
  3. Add these two functions after `_readme_navigation_registry_diagnostics`:

```python
def _document_language_from_mapping(
    raw: Mapping[str, Any] | None,
) -> DocumentLanguage | None:
    if raw is None:
        return None
    return DocumentLanguage(
        english_only_roots=tuple(raw["english_only_roots"]),
        english_only_suffixes=frozenset(raw["english_only_suffixes"]),
        korean_first_profiles=frozenset(raw["korean_first_profiles"]),
        english_sections=frozenset(raw["english_sections"]),
        min_latin_words=raw["min_latin_words"],
        pending_paths=frozenset(PurePosixPath(value) for value in raw["pending_paths"]),
    )


def _document_language_registry_diagnostics(
    raw_registry: Mapping[str, Any],
    profiles_by_id: Mapping[str, Mapping[str, Any]],
) -> list[Diagnostic]:
    """Require the language contract to name real, checked profiles and paths."""

    contract = raw_registry.get("document_language")
    if contract is None:
        return []
    faults: list[str] = []
    for profile_id in contract["korean_first_profiles"]:
        profile = profiles_by_id.get(profile_id)
        if profile is None:
            faults.append(f"unknown profile {profile_id}")
        elif profile.get("mode") not in {"authored", "router"}:
            faults.append(f"{profile_id} is not an authored or router profile")
    roots = tuple(contract["english_only_roots"])
    for root in roots:
        if not root.endswith("/"):
            faults.append(f"english-only root {root} does not end in /")
    for suffix in contract["english_only_suffixes"]:
        if not suffix.startswith("."):
            faults.append(f"suffix {suffix} does not start with .")
    sections = contract["english_sections"]
    if any(not name.strip() for name in sections) or len(set(sections)) != len(sections):
        faults.append("english sections are empty or repeated")
    if contract["min_latin_words"] < 1:
        faults.append("min_latin_words is below one")
    for value in contract["pending_paths"]:
        if value.startswith(roots):
            faults.append(f"pending path {value} is under an English-only root")
    return [
        _diagnostic(
            "REGISTRY_DOCUMENT_LANGUAGE",
            expected="checked profiles, well-formed roots and suffixes, convertible paths",
            actual=fault,
        )
        for fault in faults
    ]
```

  Then add `*_document_language_registry_diagnostics(raw_registry, profiles_by_id),`
  to the diagnostics list in `validate_registry`, after the navigation entry.
  In `scripts/document_authority.py`, add `"document_language"` to
  `OPTIONAL_TOP_LEVEL_KEYS` with the comment
  `# SPEC-0093 adds the document language contract.`

- [ ] **Step 5: Declare the schema** in `document-profile.schema.json` under
  top-level `properties`:

```json
"document_language": {
  "type": "object",
  "additionalProperties": false,
  "required": ["english_only_roots", "english_only_suffixes", "korean_first_profiles", "english_sections", "min_latin_words", "pending_paths"],
  "properties": {
    "english_only_roots": {"type": "array", "uniqueItems": true, "items": {"type": "string", "pattern": "^[^/].*/$"}},
    "english_only_suffixes": {"type": "array", "uniqueItems": true, "items": {"type": "string", "pattern": "^\\.[a-z0-9]+$"}},
    "korean_first_profiles": {"type": "array", "uniqueItems": true, "items": {"type": "string", "minLength": 1}},
    "english_sections": {"type": "array", "uniqueItems": true, "items": {"type": "string", "minLength": 1}},
    "min_latin_words": {"type": "integer", "minimum": 1},
    "pending_paths": {"type": "array", "uniqueItems": true, "items": {"type": "string", "pattern": "\\.md$"}}
  }
}
```

- [ ] **Step 6: Add the validator** to `scripts/validate-markdown-profiles.py`.
  Import `document_language` beside the other script-local imports, then add:

```python
def _terminal(registry: Any, profile: DocumentProfile, text: str) -> bool:
    try:
        _, metadata, _ = extract_frontmatter(text)
    except ContractError:
        return False
    status = metadata.get("status")
    if not isinstance(status, str):
        return False
    return any(
        profile.profile_id in domain.profile_ids
        and domain.validation_class(status) == "terminal"
        for domain in registry.lifecycle_domains
    )


def document_language_diagnostics(
    registry: Any,
    documents: Sequence[tuple[PurePosixPath, DocumentProfile, str]],
    english_only_texts: Mapping[PurePosixPath, str],
) -> list[Diagnostic]:
    """SPEC-0093: each document is written in the language its profile names."""

    contract = getattr(registry, "document_language", None)
    if contract is None:
        return []
    outputs = {
        profile.template: profile.profile_id
        for profile in registry.profiles
        if profile.template is not None and profile.mode != "template"
    }
    diagnostics: list[Diagnostic] = []
    checked: set[PurePosixPath] = set()
    for path, profile, text in documents:
        kind = document_language.classify(
            path,
            profile.profile_id,
            profile.mode,
            outputs.get(path),
            _terminal(registry, profile, text),
            contract,
        )
        if kind is None or kind == "english-only":
            continue
        checked.add(path)
        found = document_language.findings(text, kind, contract)
        if path in contract.pending_paths:
            if not found:
                diagnostics.append(
                    _diagnostic(
                        "LANG-PENDING",
                        path,
                        profile,
                        "a pending document that still violates the contract",
                        "it passes; remove it from pending_paths",
                    )
                )
            continue
        diagnostics.extend(
            _diagnostic(code, path, profile, f"{kind} language", detail)
            for code, detail in found
        )
    for path, text in sorted(english_only_texts.items()):
        diagnostics.extend(
            Diagnostic(code, path, "", "english-only", detail, OWNER)
            for code, detail in document_language.findings(text, "english-only", contract)
        )
    for pending in sorted(contract.pending_paths - checked, key=PurePosixPath.as_posix):
        diagnostics.append(
            Diagnostic(
                "LANG-PENDING",
                pending,
                "",
                "a tracked, checked document",
                "pending path is untracked or unchecked",
                OWNER,
            )
        )
    return diagnostics
```

  In `main`, after the `identity_documents` loop, add:

```python
        language = getattr(registry, "document_language", None)
        english_only_texts: dict[PurePosixPath, str] = {}
        if language is not None:
            entries = _parse_ls_files_stage_z(_run_git(root, ("ls-files", "--stage", "-z")))
            for entry in entries:
                if (
                    entry.stage == 0
                    and entry.mode.startswith("100")
                    and entry.path.as_posix().startswith(language.english_only_roots)
                    and entry.path.suffix in language.english_only_suffixes
                ):
                    english_only_texts[entry.path] = read_repository_text(root, entry.path)
        diagnostics.extend(
            document_language_diagnostics(registry, identity_documents, english_only_texts)
        )
```

  Import `_parse_ls_files_stage_z` and `_run_git` from `document_contracts` if
  the module does not already. `.claude/settings.local.json` is untracked, so
  `ls-files` never returns it, and the exclusion the old check made is not
  needed.

- [ ] **Step 7: Run to verify the unit tests pass.** Run
  `python3 -m unittest tests.test_document_language`. Expected: `OK`.

- [ ] **Step 8: Remove the replaced blocks and rewrite their tests.**
  - In `quality.py`, delete:
    - `english_first_terminal_states` through the end of the Stage 03 loop;
    - the `tracked_language_roots` assignment and its loop;
    - `agent_section_headings`, `current_agent_language_scan_text`, the three
      `archive_language_probe` checks, and the agent-section loop.

    Keep the `docs/README.md` phrase check.
  - In `tests/test_repository_quality_rules.py`, drop
    `english_first_terminal_states` from `names` and delete
    `test_english_first_scope_skips_only_terminal_stage03_documents`.
    `ValidatorTests.test_terminal_document_is_not_checked` replaces it.
  - Rewrite
    `test_common_agent_documents_and_native_sidecars_stay_english_only` so it
    maps the same six paths to the same text and passes the mapping to
    `MARKDOWN.document_language_diagnostics(contracts.load_registry(ROOT), [], texts)`.
    It asserts one `LANG-ENGLISH-ONLY` diagnostic per path.

- [ ] **Step 9: Keep fixtures consistent.** At each fixture site named in
  Context, add `"document_language"` wherever `"readme_navigation"` is named
  or popped, with the comment
  `# The language contract names profiles this selection drops.`

- [ ] **Step 10: Register the contract.**
  1. Add the Spec's `document_language` object to `registry.json`, with an
     empty `pending_paths`.
  2. Run `python3 scripts/validate-markdown-profiles.py --root . --mode strict --format json`
     and collect every path that reports `LANG-ENGLISH-FIRST`,
     `LANG-KOREAN-FIRST`, or `LANG-TEMPLATE`.
  3. Before listing them, inspect ten findings across profiles. A finding
     that is not real prose is a validator defect: fix it with a failing
     fixture first.
  4. Put the sorted list in `pending_paths`.
  5. A `LANG-ENGLISH-ONLY` diagnostic is a validator defect, because the
     replaced check guaranteed there were none.
  6. Re-run the gate. Expected: PASS.

- [ ] **Step 11: Activate.** Set this package's Spec and Plan to `active` and
  its Task to `in-progress`, with minor version bumps.

- [ ] **Step 12: Verify.** Run:
  - `python3 scripts/validate-document-contract-registry.py --root . --mode strict`
  - `python3 -m unittest tests.test_document_language tests.test_repository_quality_rules tests.test_common_agents_document_routes`
  - the whole suite
  - `python3 scripts/qa.py staged`

  Expected: PASS, apart from the known environment failures that WP-008
  lists.

- [ ] **Step 13: Commit** `feat(validation): add the document language contract and validator`.

### WP-003: Template prompts

**Files:** the `pending_paths` entries under `docs/99.templates/templates/`,
which are the README, pack, and operations templates.

- [ ] Rewrite the text after each `Author prompt:` marker in Korean, keeping
  the marker and each prompt's instruction, including the SPEC-0091
  navigation wording.
- [ ] Remove the paths from `pending_paths`. Run
  `python3 scripts/validate-markdown-profiles.py --root . --mode strict` and
  `python3 scripts/qa.py staged`. Expected: PASS.
- [ ] Commit `docs(templates): write Korean-output author prompts in Korean`.

### WP-004: READMEs

**Files:** every pending `README.md`, and `.github/repository-surface.md` if
it is pending.

- [ ] Translate English prose and blockquote paragraphs into Korean. The
  governance-hub line becomes
  a Korean blockquote stating that every AI agent action in the folder
  follows the Agent Governance Hub, linking `.agents/README.md` at the depth
  each file already uses.
- [ ] Keep every required H2, table, link, and path.
- [ ] Remove the paths from `pending_paths`, run `python3 scripts/qa.py staged`,
  and commit `docs(readme): write README prose in Korean`. When the files
  split into disjoint areas, commit one area at a time.

### WP-005: Operations documents

**Files:** every pending path under `docs/05.operations/`.

- [ ] Translate each English prose paragraph into Korean. Commands, tables,
  and agent sections stay as they are.
- [ ] Remove the paths from `pending_paths`, run staged QA, and commit
  `docs(operations): write operations prose in Korean`.

### WP-006: Requirements

**Files:** every pending path under `docs/01.requirements/`.

- [ ] Translate each requirement's prose into English, one file at a time.
  Keep every requirement ID, its order and meaning, and every table row.
- [ ] After each file, run the whole suite and
  `python3 scripts/validate-links-and-owners.py --root . --mode strict`.
  If a sealed or frozen proof reports a digest change:
  1. Restore the file with `git show HEAD:<path> > <path>`.
  2. Keep it pending.
  3. Record the deferral in the Task.
- [ ] Remove the converted paths from `pending_paths`, run staged QA, and
  commit `docs(requirements): write requirement prose in English`.

### WP-007: Architecture and remainder

**Files:** every pending path under `docs/02.architecture/`, then every other
pending path except those WP-006 deferred.

- [ ] Translate prose into English. Keep each decision, its alternatives and
  consequences, and every identifier and link.
- [ ] Apply the same digest guard and whole-suite run as WP-006.
- [ ] Remove the paths from `pending_paths`, run staged QA, and commit
  `docs(architecture): write decision and description prose in English`.
  Commit any remainder separately, one area per commit.

### WP-008: Governance sentence, evidence, and closure

- [ ] In `.agents/governance/document-authoring.md`, replace the sentences
  that begin `Governance and agent execution sections remain English.` and
  end at `remain English-first.` with:
  "The registry's `document_language` contract owns each document's
  language: README and operations profiles are Korean-first, files under
  `.agents/`, `.claude/`, and `.codex/` are English only, every other current
  document is English-first, agent requirement sections stay English, and a
  template writes its author prompts in its output's language."
- [ ] Confirm that `pending_paths` is empty, or holds only WP-006 or WP-007
  deferrals that the Task names.
- [ ] Run `timeout 3500 python3 scripts/qa.py full` and record every gate.
  Separate the known environment failures from new ones:
  - Gitleaks absent;
  - `pre-commit` off the trusted `PATH`;
  - the two Gitleaks-dependent `test_qa_runner` cases;
  - the two host-only tests;
  - the intermittent same-inode restore test.
- [ ] Record commits, results, deferrals, and residual risk in the Task. Set
  the Spec, Plan, and Task to `done` and commit
  `docs(specs): record SPEC-0093 evidence and close the package`.

## Verification Plan

- Every work package runs its focused tests, the gate it touches, and
  `python3 scripts/qa.py staged`.
- WP-002, WP-006, and WP-007 also run the whole suite.
- WP-008 runs `python3 scripts/qa.py full`.
- Hosted `ci-summary` is not observed.

### Review Focus

- **Nested lists and list continuations** must not count as prose. Pinned by
  `test_headings_tables_lists_comments_and_code_are_not_judged` and
  `test_paragraph_after_a_list_is_judged`.
- **A Korean paragraph dense with English terms** passes because it has
  Hangul. Pinned by `test_english_paragraph_fails_and_korean_passes`.
- **A template whose output profile has no `template` link** is unchecked,
  not failed. Pinned by `test_unchecked_documents`.
- **A staged run, whose index differs from the worktree,** reads the tracked
  index, as `enumerate_target_markdown` does. Pinned by each commit's staged
  QA.
- **A translation that changes a sealed digest** is caught by the whole-suite
  run after each file in WP-006 and WP-007.

## Risks & Mitigations

| Risk | Mitigation |
| --- | --- |
| Translation drifts from the source meaning | One file per step, identifiers and tables unchanged, review against `HEAD` |
| `pending_paths` becomes a permanent exception list | `LANG-PENDING` fails a pending path that passes, and WP-008 requires an empty list or named deferrals |
| The paragraph rule misjudges Markdown shapes | Unit fixtures for each shape, and WP-002 Step 10 inspects findings before listing them |
| Fixture registries drift from the contract | WP-002 Step 9 updates every site that names `readme_navigation`, and the whole suite runs before the commit |

## Completion Criteria

WP-001 to WP-008 meet their exit evidence, VAL-DLC-001 to VAL-DLC-007 hold,
and full QA ran on the final tree with only known environment failures.

## Traceability

The [Spec](spec.md) owns the contract and criteria.

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-DLC-001](spec.md#success-criteria--verification-plan) | WP-002 | [tsk-0001](tasks/tsk-0001-converge-document-language.md) |
| [VAL-DLC-002](spec.md#success-criteria--verification-plan) | WP-002 | [tsk-0001](tasks/tsk-0001-converge-document-language.md) |
| [VAL-DLC-003](spec.md#success-criteria--verification-plan) | WP-002 | [tsk-0001](tasks/tsk-0001-converge-document-language.md) |
| [VAL-DLC-004](spec.md#success-criteria--verification-plan) | WP-003 | [tsk-0001](tasks/tsk-0001-converge-document-language.md) |
| [VAL-DLC-005](spec.md#success-criteria--verification-plan) | WP-004 to WP-007 | [tsk-0001](tasks/tsk-0001-converge-document-language.md) |
| [VAL-DLC-006](spec.md#success-criteria--verification-plan) | WP-008 | [tsk-0001](tasks/tsk-0001-converge-document-language.md) |
| [VAL-DLC-007](spec.md#success-criteria--verification-plan) | WP-008 | [tsk-0001](tasks/tsk-0001-converge-document-language.md) |
