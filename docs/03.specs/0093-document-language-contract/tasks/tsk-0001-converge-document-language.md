---
title: "Converge Document Language"
version: "0.3.0"
type: "sdlc/task"
status: "done"
owner: "platform"
updated: "2026-09-26"
layer: "specs"
artifact_id: "SPEC-0093-TSK-0001"
---

# Task: Converge Document Language

## Overview

Execute [SPEC-0093-PLAN-0001](../plan.md). On 2026-09-25 the request owner
approved the three-part program. On 2026-09-26 they approved this part's
design, its boundaries, and the Spec. Push, merge, and live actions are not
authorized.

## Inputs

- [Owning Spec](../spec.md)
- [Owning Plan](../plan.md)
- [Stage 99 registry](../../../99.templates/registry.json)

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | VAL-DLC-007 | Propose the package | platform | Done | Committed `cacd0094` | Staged QA PASS |
| WORK-002 | VAL-DLC-001, VAL-DLC-002, VAL-DLC-003 | Contract, module, validator, tests; replace the `quality.py` blocks | platform | Done | Committed `b470e2a1`; 66 documents pending | Focused tests PASS; whole suite 1206 tests, 6 environment failures; staged QA PASS |
| WORK-003 | VAL-DLC-004 | Korean author prompts | platform | Done | Committed `9f334da8`; 52 documents pending | Profile gate PASS, staged QA PASS |
| WORK-004 | VAL-DLC-005 | READMEs to Korean | platform | Done | `7074f928`, `f8b5f0d5`, `84ba3172`, `dae50ee0`; no README pending; 21 documents pending | Archive tests 360 OK, link gate, staged QA PASS |
| WORK-005 | VAL-DLC-005 | Operations documents to Korean | platform | Done | No operations body was pending; the five operations READMEs converted under WORK-004 | Profile gate |
| WORK-006 | VAL-DLC-005 | Requirements to English | platform | Done | Committed `77d4820a`; 17 documents pending | Digest guard 485 OK, whole suite, staged QA PASS |
| WORK-007 | VAL-DLC-005 | Architecture and remainder to English | platform | Done | Committed `16a9cc9b`; no document pending | Whole suite, lifecycle gate, staged QA PASS |
| WORK-008 | VAL-DLC-006, VAL-DLC-007 | Governance sentence, evidence, closure | platform | Done | Review fixes `6d3ada1e` and `504b3c13`; this closure commit | Full QA, whole suite |

## Approval and Safety Boundaries

- **Allowed Paths**:
  - `docs/99.templates/registry.json` and
    `docs/99.templates/contracts/document-profile.schema.json`
  - `docs/99.templates/templates/**`
  - `scripts/document_language.py`, `scripts/document_contracts.py`,
    `scripts/document_authority.py`, and `scripts/validate-markdown-profiles.py`
  - `scripts/validation/repository/quality.py`
  - the tests these files own, and the fixture registries the Plan names
  - the current documents that `pending_paths` names
  - `.agents/governance/document-authoring.md`
  - REQ-0003, the Stage 03 index, and this package
- **Forbidden Paths**:
  - retained bodies and frozen records under `docs/98.archive/`
  - sealed ledgers
  - lifecycle states and edges
  - manifests under `gitops/` and `infrastructure/`
  - `.github/` workflows
- **Approval Required**: push, pull request, merge, and any live action
- **Static Validation**: focused tests; the registry, profile, and link gates;
  staged QA per commit; the whole suite for code, requirement, and
  architecture commits; full QA at closure
- **Live Validation**: none
- **Secret / Vault Handling**: no secret value is read
- **Rollback Plan**: revert the local commits in reverse order
- **Evidence Location**: this Task

## Verification Summary

### Survey (2026-09-26, branch head `87de7188`)

A word-ratio survey of tracked Markdown sorted documents by the Spec's
language rules and found these off their target language:
- English-first profiles written mostly in Korean: four requirements, twelve
  accepted decisions, and four architecture descriptions.
- Korean-first READMEs written in English: about ten.
- READMEs carrying an English governance-hub blockquote: fifteen.

The survey is approximate. The initial `pending_paths` that WP-002 produces
is the exact list.

### WORK-002 (2026-09-26)

- The validator reported 66 pending documents. English-first counts any
  Hangul line, tables included, so the count exceeds the survey.
- English-only files are read from `git ls-files --stage`. The shared tracked
  path helper fails closed on the `.claude/skills` symlinks.
- Whole suite on a clean checkout of the staged tree: 1206 tests, 6 failures,
  none caused by this change:
  - Gitleaks is not installed (two `test_qa_runner` cases).
  - Two host-only cases: the escaped descendant signal and the file reader
    change race.
  - One known flaky case: equal size same inode restore.
  - The archive Git budget is one call over on a detached checkout. It fails
    identically on a clean detached checkout of `cacd0094` and passes on the
    branch checkout.
- The branch checkout also fails the agent governance tests. The cause is an
  unstaged request-owner edit to `.claude/settings.json` that removes one deny
  entry. That edit is outside this Task and left untouched; staged QA reads
  the index and is unaffected.

### WORK-004 (2026-09-26)

- READMEs that were mostly English are translated in full: paragraphs, list
  items, and descriptive table cells. READMEs that were mostly Korean change
  only the paragraphs the contract flags.
- A table whose cells a validator matches by English phrase stays English.
  The `.github/repository-surface.md` Workflow Responsibility Matrix is one;
  tables are not judged by the contract.
- Two `quality.py` phrase pins on `.github/repository-surface.md` prose now
  name the Korean sentences that replace the English ones.
- Korean prose is drafted, then polished by the humanize skill in its
  conservative light route; each batch passes its change-rate gate.
- The Stage 90 research pack 0001 README keeps its Requirement Coverage Matrix
  in English. The matrix rows are observation-dated evidence that the pack
  itself keeps at observation-time wording until its next refresh.

### WORK-006 (2026-09-26)

- REQ-0001 to REQ-0004 are English. Identifiers, links, code spans, and
  required headings are unchanged; a script compared them between the source
  and the translation for every file.
- Digest guard: after REQ-0001 changed, the archive, strict cutover, generic
  migration recovery, and lifecycle migration suites ran 485 tests, all OK.
  No sealed or frozen proof pins a converted body, so nothing was deferred.
- Whole suite on a clean checkout of the staged tree holding every WORK-006
  and WORK-007 conversion: 1206 tests, 5 failures, all known environment
  failures (Gitleaks absent twice, two host-only cases, the detached-checkout
  archive Git budget).

### WORK-007 (2026-09-26)

- Thirteen accepted decisions and four architecture descriptions are English.
  Translation keeps each decision's text and meaning; no decision, status, or
  lifecycle edge changed, and the staged lifecycle gate passes.
- ADR-0042 lists editing accepted ADR bodies as a non-goal and warns that
  changing one erases the record of the decision. That concerns the decision
  as recorded. These conversions change only the language, so the recorded
  decision, its context, and its alternatives stay as they were decided. The
  request owner approved converting the accepted decisions in the Spec.
- `pending_paths` is empty.

### Full QA (2026-09-26, branch head `504b3c13` plus the WORK-008 sentence)

`timeout 3500 python3 scripts/qa.py full` ran on a clean checkout of that
tree: 19 gates PASS, 3 FAIL, all environment limits observed before this
package:

- `archive-cutover`: `ARCHIVE-SECRET-CLASSIFIER-UNAVAILABLE`; Gitleaks is not
  installed.
- `pre-commit`: required tool unavailable on the trusted `PATH`.
- `unit-tests`: 1210 tests, five failures, none in a module this package
  changed: two Gitleaks-dependent `test_qa_runner` cases, the host-only
  `test_escaped_descendant_is_failed_without_post_reap_group_signal` and
  `test_file_reader_rejects_changes_during_read`, and the archive Git budget,
  which is one call over on a detached checkout and fails identically on a
  clean detached checkout of `cacd0094`.

Hosted `ci-summary` is not observed.

### Full QA (2026-09-26, branch head `45c71134`)

After the settings commit, full QA ran on the branch checkout: 19 gates PASS,
3 FAIL. `agent-governance` now passes on the branch checkout. The failures are
the same environment limits:

- `archive-cutover`: `ARCHIVE-SECRET-CLASSIFIER-UNAVAILABLE` and
  `ARCHIVE-CUTOVER-INCOMPLETE`; Gitleaks is not installed.
- `pre-commit`: required tool unavailable on the trusted `PATH`.
- `unit-tests`: three failures, the two Gitleaks-dependent `test_qa_runner`
  cases and the host-only
  `test_escaped_descendant_is_failed_without_post_reap_group_signal`.

### Review, Deferrals, and Residual Risk

- An independent review of the whole range found that the English-section
  rule judged only plain paragraphs and missed qualified headings. It also
  found fence, blockquote, and HTML parsing gaps and a phrase pin that lost its
  object. `6d3ada1e` fixes these with regression tests that fail on the
  previous module.
- The review compared translations with their sources. Five requirement
  statements had shifted in normative force; `504b3c13` restores them.
- Not fixed, as minor:
  - pipeless tables, setext headings, and CRLF frontmatter are judged as
    prose, which errs toward a loud false positive;
  - an HTML block ends at its start line rather than at the next blank line;
  - a template serving profiles of both languages would take the last one,
    though no template does today.
- Converted documents changed only `updated`, not `version`, because a
  translation keeps meaning; `document-authoring.md` moves to 1.9.0 because its
  language rule changed.
- The request owner's `.claude/settings.json` edit, which drops the
  `cat .env.*` deny entry, was committed at their request as `45c71134`,
  together with removing the matching validator pin. The other `.env` read
  denies remain.
- No conversion was deferred, and `pending_paths` is empty.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-001](../plan.md#work-breakdown) | Proposed | Staged QA |
| [WORK-002](../plan.md#work-breakdown) | Done | Focused tests, whole suite, and staged QA |
| [WORK-003](../plan.md#work-breakdown) | Done | Profile gate and staged QA |
| [WORK-004](../plan.md#work-breakdown) | Done | Staged QA |
| [WORK-005](../plan.md#work-breakdown) | Done | Profile gate |
| [WORK-006](../plan.md#work-breakdown) | Done | Whole suite and staged QA |
| [WORK-007](../plan.md#work-breakdown) | Done | Whole suite and staged QA |
| [WORK-008](../plan.md#work-breakdown) | Done | Full QA |
