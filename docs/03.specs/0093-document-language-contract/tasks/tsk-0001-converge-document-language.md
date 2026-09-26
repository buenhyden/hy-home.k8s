---
title: "Converge Document Language"
version: "0.1.0"
type: "sdlc/task"
status: "queued"
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
| WORK-001 | VAL-DLC-007 | Propose the package | platform | In progress | Proposal written | Staged QA |
| WORK-002 | VAL-DLC-001, VAL-DLC-002, VAL-DLC-003 | Contract, module, validator, tests; replace the `quality.py` blocks | platform | Queued | Not started | Focused tests, whole suite, staged QA |
| WORK-003 | VAL-DLC-004 | Korean author prompts | platform | Queued | Not started | Profile gate, staged QA |
| WORK-004 | VAL-DLC-005 | READMEs to Korean | platform | Queued | Not started | Staged QA |
| WORK-005 | VAL-DLC-005 | Operations documents to Korean | platform | Queued | Not started | Staged QA |
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

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-001](../plan.md#work-breakdown) | Proposal written | Staged QA |
| [WORK-002](../plan.md#work-breakdown) | Not started | Focused tests and staged QA |
| [WORK-003](../plan.md#work-breakdown) | Not started | Profile gate |
| [WORK-004](../plan.md#work-breakdown) | Not started | Staged QA |
| [WORK-005](../plan.md#work-breakdown) | Not started | Staged QA |
| [WORK-006](../plan.md#work-breakdown) | Not started | Whole suite and staged QA |
| [WORK-007](../plan.md#work-breakdown) | Not started | Whole suite and staged QA |
| [WORK-008](../plan.md#work-breakdown) | Not started | Full QA |
