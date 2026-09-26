---
title: "Converge Document Language"
version: "0.2.0"
type: "sdlc/task"
status: "in-progress"
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
| WORK-004 | VAL-DLC-005 | READMEs to Korean | platform | Done | `7074f928`, `f8b5f0d5`, `84ba3172`, and the Stage 90 commit; no README pending; 21 documents pending | Archive tests 360 OK, link gate, staged QA PASS |
| WORK-005 | VAL-DLC-005 | Operations documents to Korean | platform | Done | No operations body was pending; the five operations READMEs converted under WORK-004 | Profile gate |
| WORK-006 | VAL-DLC-005 | Requirements to English | platform | Queued | Not started | Staged QA, whole suite |
| WORK-007 | VAL-DLC-005 | Architecture and remainder to English | platform | Queued | Not started | Staged QA, whole suite |
| WORK-008 | VAL-DLC-006, VAL-DLC-007 | Governance sentence, evidence, closure | platform | Queued | Not started | Full QA |

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

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-001](../plan.md#work-breakdown) | Proposed | Staged QA |
| [WORK-002](../plan.md#work-breakdown) | Done | Focused tests, whole suite, and staged QA |
| [WORK-003](../plan.md#work-breakdown) | Done | Profile gate and staged QA |
| [WORK-004](../plan.md#work-breakdown) | Done | Staged QA |
| [WORK-005](../plan.md#work-breakdown) | Done | Profile gate |
| [WORK-006](../plan.md#work-breakdown) | Not started | Whole suite and staged QA |
| [WORK-007](../plan.md#work-breakdown) | Not started | Whole suite and staged QA |
| [WORK-008](../plan.md#work-breakdown) | Not started | Full QA |
