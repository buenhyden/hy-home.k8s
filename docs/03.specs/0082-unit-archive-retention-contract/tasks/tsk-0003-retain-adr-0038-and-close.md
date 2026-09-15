---
title: "Retain ADR-0038 and Close the Package"
version: "0.1.0"
type: "sdlc/task"
status: "queued"
owner: "platform"
updated: "2026-09-15"
layer: "specs"
artifact_id: "SPEC-0082-TSK-0003"
---

# Task: Retain ADR-0038 and Close the Package

## Overview

This Task records the third integration: retaining ADR-0038 as the first exact
disposition and closing this package. It records observed results only and
never promotes a repository-static result to hosted, provider-runtime, or live
evidence.

## Inputs

- [Spec](../spec.md) owns the contract, and [Plan](../plan.md) owns order.
- Entry gate: the cutover integration has merged, ADR-0038 is `superseded` at
  the comparison base, and the request owner has approved its disposition.
- ADR-0039 links ADR-0038 in its `Decision lineage` cell, as the body contract
  requires of a proposed decision. The retention replaces that link with the
  identifier, because a current document cites a successor, not a
  `superseded/` body.

## Task Table

| ID       | Upstream criterion | Work item                                                                         | Owner    | Status | Result       | Evidence                    |
| -------- | ------------------ | --------------------------------------------------------------------------------- | -------- | ------ | ------------ | --------------------------- |
| WORK-001 | VAL-UAR-010        | Repoint current documents that cite ADR-0038 to ADR-0039 or name it by identifier | platform | Queued | Not executed | Link gate                   |
| WORK-002 | VAL-UAR-010        | Retain ADR-0038 exactly with one catalog row                                      | platform | Queued | Not executed | Lifecycle and archive gates |
| WORK-003 | VAL-UAR-010        | Close this package and record the evidence                                        | platform | Queued | Not executed | Staged and full QA          |

## Approval and Safety Boundaries

- **Allowed Paths**: the retention scope named in the [Spec](../spec.md).
- **Forbidden Paths**: frozen records, ledgers, and retained packages under
  `docs/98.archive/`, the sixteen ADR-0038 retained bodies, `scripts/`,
  `gitops/`, `infrastructure/`, `policy/`, `secrets/`, `.github/`.
- **Approval Required**: the ADR-0038 disposition before any work item starts.
  Push, pull request, and merge are not approved.
- **Static Validation**: `python3 scripts/qa.py staged` per logical commit and
  one `python3 scripts/qa.py full` on the final tree.
- **Live Validation**: DEFER. No live cluster, provider runtime, or network
  action is authorized.
- **Secret / Vault Handling**: No secret, credential, or private configuration
  file is read or printed.
- **Rollback Plan**: Revert before integration; after integration only a forward
  fix, never deletion of the retained unit.
- **Evidence Location**: This Task record.

## Verification Summary

Not executed. The entry gate has not been met.

## Traceability

Each work item carries its observed result.

### Lifecycle Traceability

| Criterion / work item                 | Result        | Evidence                     |
| ------------------------------------- | ------------- | ---------------------------- |
| [WORK-001](../plan.md#work-breakdown) | Not executed. | Link gate.                   |
| [WORK-002](../plan.md#work-breakdown) | Not executed. | Lifecycle and archive gates. |
| [WORK-003](../plan.md#work-breakdown) | Not executed. | Staged and full QA.          |
