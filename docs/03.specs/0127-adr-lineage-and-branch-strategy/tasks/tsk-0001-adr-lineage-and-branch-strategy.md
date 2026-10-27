---
title: "ADR Lineage and Branch Strategy"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-10-27"
layer: "specs"
artifact_id: "SPEC-0127-TSK-0001"
parent_ids: ["SPEC-0127-PLAN-0001"]
---

# Task: ADR Lineage and Branch Strategy

## Overview

Reject supersession chains without a current decision, add the ADR form
prompts and numbering rule, and record the branch strategy. It executes
[SPEC-0127](../spec.md) through [WORK-001–004](../plan.md#work-breakdown).

## Inputs

- Request: the operator said on 2026-10-27 to proceed as recommended; slice
  B of the SPEC-0125 status table covers CR-09.06 and CR-13.07.
- Research read on 2026-10-27: adr.github.io template overview, Nygard
  (2011-11-15), MADR 4.0.0 (`adr/madr` HEAD `ba75bb1b`), the Y-statement
  form, Trunk-Based Development, GitHub flow and Driessen's git-flow with its
  2020 note.
- Start: main `0058fe3c`, branch `feat/adr-lineage-and-branch-strategy`.

### ADR Form Comparison

| Field or rule | Nygard | MADR 4.0.0 | Y-statement | This repository |
| --- | --- | --- | --- | --- |
| Context, decision, consequences | yes | yes | one sentence | Required sections |
| Considered alternatives | no | Considered Options, Pros and Cons | neglected options (long form) | Required `Alternatives` |
| Status and supersession | proposed, accepted, deprecated or superseded, old record kept | status string such as `superseded by ADR-0123` | none | `status` plus reciprocal `supersedes` and `superseded_by` |
| Decision makers, consulted, informed | no | optional front matter | no | `owner` only; prompt added |
| Decision date | no | optional `date` | no | `updated` only; prompt added |
| Confirmation | no | optional section | no | Prompt added |
| Numbering | sequential, never reused | not stated | none | Never reused, now stated in the ADR log |
| Explicit non-goals, `retired` status | no | no | no | Repository conventions without a source basis |

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-AB-001](../spec.md#success-criteria--verification-plan) | Reject supersession chains without a current decision | platform | ready | NOT_RUN | Pending named repository evidence |
| WORK-002 | [VAL-AB-002](../spec.md#success-criteria--verification-plan) | Add the template prompt and the numbering rule | platform | ready | NOT_RUN | Pending named repository evidence |
| WORK-003 | [VAL-AB-003](../spec.md#success-criteria--verification-plan) | Record ADR-0052 and link it from `git.md` | platform | ready | NOT_RUN | Pending named repository evidence |
| WORK-004 | [VAL-AB-004](../spec.md#success-criteria--verification-plan) | Run staged QA and observe the hosted checks | platform | ready | NOT_RUN | Pending named repository evidence |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-AB-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Supersession tests and strict validation | Exact revision | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-AB-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Template tests and review | Exact revision | NOT_RUN | Pending | yes | none |
| EVD-003 | [VAL-AB-003](../spec.md#success-criteria--verification-plan) | WORK-003 | ADR review and acceptance | Exact revision | NOT_RUN | Pending | yes | none |
| EVD-004 | [VAL-AB-004](../spec.md#success-criteria--verification-plan) | WORK-004 | Staged QA and hosted checks | Exact pull request head | NOT_RUN | Pending | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-AB-001](../spec.md#success-criteria--verification-plan) | pending | none | Validator change and tests remain | platform |
| [VAL-AB-002](../spec.md#success-criteria--verification-plan) | pending | none | Template prompt and rule remain | platform |
| [VAL-AB-003](../spec.md#success-criteria--verification-plan) | pending | none | ADR-0052 and operator decision remain | platform |
| [VAL-AB-004](../spec.md#success-criteria--verification-plan) | pending | none | Staged QA and hosted checks remain | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: this package, the Stage 03 README index,
  `docs/01.requirements/0003-workspace-agent-governance-platform.md`,
  `scripts/document_lifecycle.py`,
  `tests/test_document_lifecycle_archive_cutover.py`,
  `docs/99.templates/templates/architecture/decision.template.md`,
  `docs/02.architecture/decisions/README.md`,
  `docs/02.architecture/decisions/0052-single-main-trunk-branch-strategy.md`
  and `.agents/governance/git.md`.
- **Forbidden Paths**: branch protection, rulesets, GitHub settings,
  provider settings and credentials.
- **Approval Required**: the operator said on 2026-10-27 to proceed as
  recommended; accepting ADR-0052 is a separate operator decision. Push,
  pull request and merge follow RUN-0013.
- **Static Validation**: focused tests, strict lifecycle validation and
  `qa.py staged`.
- **Live Validation**: none.
- **Secret / Vault Handling**: no secret is read or written.
- **Rollback Plan**: revert the pull request.
- **Evidence Location**: this Task.

## Verification Summary

Not run yet.
