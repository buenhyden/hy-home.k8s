---
title: "Document Language Contract Technical Specification"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "platform"
updated: "2026-09-26"
layer: "specs"
artifact_id: "SPEC-0093"
---

# Document Language Contract Technical Specification (Spec)

## Overview

The workspace writes documents in two languages, but no machine rule says
which document uses which. Three hard-coded checks in
`scripts/validation/repository/quality.py` enforce parts of the policy:
current Stage 03 Spec, Plan, and Task files carry no Hangul, tracked files
under `.agents/`, `.claude/`, and `.codex/` carry no Hangul, and agent
requirement sections in `docs/` carry no Hangul. Nothing states
that READMEs and operations documents are written in Korean, and the prose rule
in `.agents/governance/document-authoring.md` lets requirements use Korean.
A survey on 2026-09-26 found four requirements, twelve accepted decisions, and
four architecture descriptions written mostly in Korean, and about ten READMEs
written in English. The survey measured a word ratio, so the validator's
initial `pending_paths`, not this count, is the exact list.

The request owner approved a three-part program on 2026-09-25:
1. the README navigation contract
   ([SPEC-0091](../0091-readme-navigation-contract/spec.md)),
2. an archive ledger split, which was later withdrawn,
3. this document language contract.

On 2026-09-26 the request owner approved the design of this part:
- convert every current document through a shrinking pending list,
- judge language paragraph by paragraph,
- write each template's author prompts in the language of the document it
  creates.

The SPEC-0092 number stays with the withdrawn ledger proposal in Git history.

## Strategic Boundaries & Non-goals

In scope:
- one registry contract for document language, with its schema, loader, and
  self-consistency check;
- one validator that replaces the three hard-coded language checks;
- the author prompts of every template whose output is Korean-first;
- every current document the contract finds in violation;
- the language sentence in the document-authoring rule.

Out of scope:
- retained bodies under `docs/98.archive/`, which keep the bytes they were
  frozen with;
- documents in a terminal lifecycle state;
- native, non-target, and evidence profiles;
- identifiers, profile-required headings, commands, paths, and code, which
  keep their English form;
- any change to the meaning of a decision or requirement;
- any lifecycle state or edge;
- any live cluster or provider action.

## Contracts

- A document's language comes from its profile, not its path, with one
  exception: every tracked text file under an English-only root is English
  only, whatever its profile.
- English only: the file contains no Hangul anywhere. The roots are
  `.agents/`, `.claude/`, and `.codex/`. The text suffixes are `.md`,
  `.toml`, `.json`, `.sh`, `.yaml`, and `.yml`.
- Korean-first profiles are every `common/readme-*` router profile and every
  `operation/*` profile.
  - A Korean-first document fails on any prose paragraph or blockquote
    paragraph that has at least `min_latin_words` Latin words and no Hangul.
  - Headings, tables, list items, HTML comments, code spans, fenced blocks,
    and frontmatter are not judged.
  - Link destinations are removed before counting; link labels count.
  - An H2 section named in `english_sections` is English-first inside a
    Korean-first document, because it carries agent execution requirements.
- Every other `authored` or `router` profile is English-first. The document
  has no Hangul outside frontmatter, code spans, and fenced blocks.
- A template takes the language of the profile whose `template_source` names
  it.
  - A Korean-output template writes every author prompt comment with Hangul.
  - An English-output template has no Hangul outside code.
- These documents are not checked:
  - paths under `docs/98.archive/`, except `docs/98.archive/README.md`;
  - a document whose `status` is a `terminal` state of its lifecycle domain;
  - the `native`, `non-target`, and `evidence` modes.
- `pending_paths` names a current document whose language is not yet
  converted. It starts with every document in violation, shrinks with each
  conversion commit, and ends empty.

## Core Design

- The registry gains a top-level `document_language` object.
  `scripts/document_contracts.py` loads it the same way it loads
  `readme_navigation`.
- A new module, `scripts/document_language.py`, holds the pure rules:
  paragraph extraction, Latin word counting, author prompt extraction, and the
  verdict for each document.
- `scripts/validate-markdown-profiles.py` already resolves each document's
  profile and status. It calls the new module and emits `LANG-*`
  diagnostics, so the rules run in the existing `markdown-profiles` gate and
  no lane is added.
- The commit that activates the contract also deletes the three language
  blocks in `quality.py`.

Conversion keeps meaning. Only the prose language changes; identifiers,
tables, links, commands, paths, and the substance of each decision and
requirement stay as they are. A term with no faithful translation stays in a
code span.

## Data Modeling & Storage Strategy

```json
"document_language": {
  "english_only_roots": [".agents/", ".claude/", ".codex/"],
  "english_only_suffixes": [".md", ".toml", ".json", ".sh", ".yaml", ".yml"],
  "korean_first_profiles": [
    "common/readme-repository", "common/readme-stage-index",
    "common/readme-collection-index", "common/readme-implementation",
    "common/readme-audit-pack", "common/readme-data-pack",
    "common/readme-research-pack", "common/readme-workspace-staging",
    "common/readme-runtime-governance",
    "operation/guide", "operation/policy", "operation/runbook",
    "operation/incident", "operation/postmortem"
  ],
  "english_sections": [
    "AI Agent Requirements", "Agent Execution Notes", "Agent Harness Requirements"
  ],
  "min_latin_words": 8,
  "pending_paths": []
}
```

The `pending_paths` value above is the final state.

The registry self-consistency check requires:
- every Korean-first profile to exist, with mode `authored` or `router`;
- every root to end in `/`;
- every suffix to start with `.`;
- every English section name to be non-empty and unique;
- `min_latin_words` to be at least one;
- no pending path under an English-only root, where no conversion is ever
  pending.

The validator sees the tracked tree. It requires every pending path to be a
tracked, checked document that still violates the contract.

## Interfaces & Data Structures

| Code | Failure |
| --- | --- |
| `LANG-ENGLISH-ONLY` | A tracked text file under an English-only root contains Hangul |
| `LANG-ENGLISH-FIRST` | An English-first document, or an English section of a Korean-first document, has Hangul outside frontmatter and code |
| `LANG-KOREAN-FIRST` | A Korean-first paragraph has at least `min_latin_words` Latin words and no Hangul |
| `LANG-TEMPLATE` | A Korean-output template has an author prompt with no Hangul, or an English-output template has Hangul outside code |
| `LANG-PENDING` | A pending path is untracked, not checked, or already passes |
| `REGISTRY_DOCUMENT_LANGUAGE` | The registry contract contradicts its own profiles, roots, or paths |

Replaced checks in `scripts/validation/repository/quality.py`: the
English-first Stage 03 block, the English-only `tracked_language_roots`
block, and the agent-section block with its archive scope probes.
Tests that pinned them are rewritten to assert the codes that replace them.

## Edge Cases & Error Handling

- **README under an English-only root.** A README such as
  `.agents/roles/README.md` is English only: the root rule wins over its README
  profile. The Korean-output README template still serves these READMEs; the
  author replaces its prompts.
- **Link-only paragraph.** A paragraph of links alone, such as
  `[RUN-0001](...)`, rarely reaches the word threshold and is not a violation.
- **Governance-hub blockquote.** The English governance-hub blockquote in
  fifteen READMEs is a blockquote paragraph, so it is converted.
- **Stage 98 README.** `docs/98.archive/README.md` is Korean-first. Its
  machine tables are tables, so they are not judged.
- **No resolved profile.** A document without a resolved profile is not
  checked.
- **Unicode escapes.** An escape such as `\uc0c1\ud0dc` inside JSON code is
  ASCII, not Hangul.

## Failure Modes & Fallback / Human Escalation

A failing gate stops the commit; no assertion is weakened.

If a conversion changes a digest that a sealed or frozen proof pins:
- the conversion stops;
- the document stays in `pending_paths`;
- the Task records a named deferral for the request owner.

A translation whose meaning is uncertain is raised in review, not guessed.

## Verification Commands

```bash
python3 -m unittest tests.test_document_language
python3 scripts/validate-document-contract-registry.py --root . --mode strict
python3 scripts/validate-markdown-profiles.py --root . --mode strict
python3 scripts/validate-links-and-owners.py --root . --mode strict
python3 scripts/qa.py staged
python3 scripts/qa.py full
git diff --check
```

## Success Criteria & Verification Plan

| ID | Criterion | Evidence |
| --- | --- | --- |
| VAL-DLC-001 | The registry contract, schema, loader, and self-consistency check exist and reject contradictions | Focused tests and the registry gate |
| VAL-DLC-002 | Each `LANG-*` rule passes its allowed fixtures and fails its forbidden ones, including blockquotes, link-only paragraphs, code spans, terminal states, and English-only roots | Focused tests |
| VAL-DLC-003 | The three `quality.py` language checks are removed and their tests assert the replacing codes | Focused tests and review |
| VAL-DLC-004 | Every template's author prompts use its output language | Profile gate |
| VAL-DLC-005 | Every checked current document passes, and `pending_paths` is empty | Profile gate over the whole corpus |
| VAL-DLC-006 | The document-authoring rule states the contract and names the registry as its owner | Review |
| VAL-DLC-007 | Each commit passes staged QA and the final tree runs full QA | Staged and full QA |

## Traceability

The [Implementation Plan](plan.md) owns order and risk. The
[language Task](tasks/tsk-0001-converge-document-language.md) owns the
evidence.

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0003-FR-0012](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-DLC-001 | Focused tests and the registry gate |
| [REQ-0003-FR-0012](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-DLC-002 | Focused tests |
| [REQ-0003-FR-0012](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-DLC-003 | Focused tests and review |
| [REQ-0003-FR-0013](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-DLC-004 | Profile gate |
| [REQ-0003-FR-0014](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-DLC-005 | Profile gate over the whole corpus |
| [REQ-0003-FR-0012](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-DLC-006 | Review |
| [REQ-0003-FR-0018](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-DLC-007 | Staged and full QA |
