---
title: "SDLC Cross-Artifact Conformance"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-06"
layer: "specs"
artifact_id: "SPEC-0146-TSK-0001"
parent_ids: ["SPEC-0146-PLAN-0001"]
---

# Task: SDLC Cross-Artifact Conformance

## Overview

Close the governance gaps the [audit](../../../90.references/audits/0001-sdlc-governance/m0001-sdlc-governance-audit.md)
found. It executes [SPEC-0146](../spec.md) through
[WORK-001–003](../plan.md#work-breakdown).

## Inputs

- Request (2026-11-06): audit the workspace engineering governance and apply
  the well-founded improvements directly, without remote Git, deployment or
  deletion.
- Approval (2026-11-06): that request authorizes this scope. The lifecycle
  gate requires the Spec and Plan to be created `draft` and approved in a
  separate commit; no commit was requested, so both stay `draft` and the
  approval commit is pending (audit D-2). Criterion acceptance stays the
  operator's.
- Start: branch `docs/sdlc-cross-artifact-conformance` from `main` at
  `3ec90be8`, clean worktree.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-SDLC-001](../spec.md#success-criteria--verification-plan) | `sdlc.md` Cross-artifact conformance | platform | draft | NOT_RUN | EVD-001 |
| WORK-002 | [VAL-SDLC-002](../spec.md#success-criteria--verification-plan) | Spec, Plan and ADR template prompts | platform | draft | NOT_RUN | EVD-002 |
| WORK-003 | [VAL-SDLC-003](../spec.md#success-criteria--verification-plan) | Audit pack AUD-0001 | platform | draft | NOT_RUN | EVD-003 |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-SDLC-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Strict document and link checks | Pending Spec approval | NOT_RUN | Pending; pre-approval observation in the audit Verification State | yes | none |
| EVD-002 | [VAL-SDLC-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Strict profile checks and document unit tests | Pending Spec approval | NOT_RUN | Pending; pre-approval observation in the audit Verification State | yes | none |
| EVD-003 | [VAL-SDLC-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Strict checks and independent review | Pending Spec approval | NOT_RUN | Pending; pre-approval observation in the audit Verification State | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-SDLC-001](../spec.md#success-criteria--verification-plan) | pending | none | Awaiting Spec approval commit and operator acceptance | platform |
| [VAL-SDLC-002](../spec.md#success-criteria--verification-plan) | pending | none | Awaiting Spec approval commit and operator acceptance | platform |
| [VAL-SDLC-003](../spec.md#success-criteria--verification-plan) | pending | none | Awaiting Spec approval commit and operator acceptance | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: `.agents/governance/sdlc.md`,
  `docs/99.templates/templates/specs/`,
  `docs/99.templates/templates/architecture/decision.template.md`,
  `docs/90.references/audits/`, `docs/03.specs/`,
  `docs/01.requirements/0003-workspace-agent-governance-platform.md`
- **Forbidden Paths**: `docs/99.templates/registry.json` and contracts,
  `scripts/`, `tests/`, product manifests, `secrets/`, provider settings
- **Approval Required**: commits, push and merge each need a separate request
- **Static Validation**: the Spec's Verification Commands
- **Live Validation**: not applicable
- **Secret / Vault Handling**: none
- **Rollback Plan**: delete the branch, or revert its commits
- **Evidence Location**: this Task

## Verification Summary

Not yet run under an approved Spec. Pre-approval observations (strict checks,
unit tests, independent review) are in the
[audit Verification State](../../../90.references/audits/0001-sdlc-governance/m0001-sdlc-governance-audit.md#verification-state);
rerun and record them here after the approval commit. Next owner: operator.
Rollback: delete the branch.
