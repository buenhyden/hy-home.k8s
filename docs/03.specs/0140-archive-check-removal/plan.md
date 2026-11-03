---
title: "Archive Check Removal Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "platform"
updated: "2026-11-03"
layer: "specs"
artifact_id: "SPEC-0140-PLAN-0001"
parent_ids: ["SPEC-0140"]
---

# Archive Check Removal Implementation Plan

## Global Constraints

- Every work unit inherits the [Spec](spec.md) contracts and non-goals.
- Removed code is deleted, not disabled; Git history keeps it.

## Overview

This plan executes [SPEC-0140](spec.md) on branch
`refactor/archive-check-removal` from main `69445fca`.

## Context

ADR-0040 kept the archive frozen and verified by dedicated gates. The
operator asked on 2026-11-03 to remove those checks and the archived files.

## Goals & In-Scope

Close VAL-ARC-001 to VAL-ARC-005.

## Non-Goals & Out-of-Scope

The non-goals listed in the Spec.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-ARC-001](spec.md#success-criteria--verification-plan) | Remove archive and migration checks, their tests, registry entries and policy text | None | [Task](tasks/tsk-0001-archive-check-removal.md) | Validators, test suites and QA |
| WORK-002 | [VAL-ARC-002](spec.md#success-criteria--verification-plan) | Delete archived files, keep README and structure, repoint current links, summarize them in Stage 01 and 02 owners | WORK-001 | [Task](tasks/tsk-0001-archive-check-removal.md) | Tree listing and link check |
| WORK-003 | [VAL-ARC-003](spec.md#success-criteria--verification-plan) | Independent review and hosted checks | WORK-001, WORK-002, WORK-004, WORK-005 | [Task](tasks/tsk-0001-archive-check-removal.md) | Review and hosted checks |
| WORK-005 | [VAL-ARC-005](spec.md#success-criteria--verification-plan) | Delete legacy, deprecated and one-time QA and CI/CD items and retire SPEC-0105 to SPEC-0107 | WORK-001 | [Task](tasks/tsk-0001-archive-check-removal.md) | Contract suites, validators and QA |
| WORK-004 | [VAL-ARC-004](spec.md#success-criteria--verification-plan) | Separate README (human) and AGENTS.md (agent) audiences | None | [Task](tasks/tsk-0001-archive-check-removal.md) | README search, registry and link checks |

## Verification Plan

Run each changed validator in strict mode, the affected contract-test
suites, and `python3 scripts/qa.py staged` on each commit.

## Risks & Mitigations

- A removed branch also guarded current documents. The non-archive suites
  and strict runs must stay green.
- The comparison base still holds the old registry and archive files. The
  lifecycle gate is run in staged mode against it before commit.

## Completion Criteria

All five criteria have PASS evidence and an accepted decision in the Task.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| Unvalidated archive | [Document lifecycle](../../../.agents/governance/document-lifecycle.md) | Current Contract, archive rules |
| README and AGENTS.md audiences | [Document authoring](../../../.agents/governance/document-authoring.md) | Current Contract, item 9 |
