---
title: "Cut Over the Registry and Validators"
version: "0.1.0"
type: "sdlc/task"
status: "in-progress"
owner: "platform"
updated: "2026-09-15"
layer: "specs"
artifact_id: "SPEC-0082-TSK-0002"
---

# Task: Cut Over the Registry and Validators

## Overview

This Task records the second integration: accepting ADR-0039 and moving the
registry, validators, forms, and governance prose to the unit retention
contract. It records observed results only and never promotes a
repository-static result to hosted, provider-runtime, or live evidence.

## Inputs

- [Spec](../spec.md) owns the contract, and [Plan](../plan.md) owns order.
- Entry gate: the proposal integration has merged, and the request owner has
  accepted ADR-0039.
- On 2026-09-15 the request owner approved accepting ADR-0039 once the
  proposal merged. Pull request #64 merged as `b16f23f9`, and the proposal
  commits `c07ee272`, `cd3139e6`, `97a2101b`, and `b7ba5db2` are reachable from
  `origin/main`. The cutover branch is `feat/archive-unit-retention-cutover`.
- The proposal Task records the survey findings each regression starts from.

## Task Table

| ID       | Upstream criterion | Work item                                                                                        | Owner    | Status | Result       | Evidence                     |
| -------- | ------------------ | ------------------------------------------------------------------------------------------------ | -------- | ------ | ------------ | ---------------------------- |
| WORK-001 | VAL-UAR-011        | Accept ADR-0039, supersede ADR-0038, activate this package, and close SPEC-0080 and SPEC-0081    | platform | Done   | ADR-0039 accepted, ADR-0038 superseded, SPEC-0080 and SPEC-0081 done | Lifecycle gate               |
| WORK-002 | VAL-UAR-004        | Declare units, modes, the citation table, and the legacy set in the registry, schema, and loader | platform | Queued | Not executed | Registry regressions         |
| WORK-003 | VAL-UAR-006        | Decide citation in the shared resolver and remove the duplicate current-link loop                | platform | Queued | Not executed | Link and archive regressions |
| WORK-004 | VAL-UAR-005        | Compare units as Git objects and admit a class by anchor state                                   | platform | Queued | Not executed | Lifecycle regressions        |
| WORK-005 | VAL-UAR-007        | Admit identity-preserving moves between active stages                                            | platform | Queued | Not executed | Lifecycle regressions        |
| WORK-006 | VAL-UAR-008        | Re-verify every catalog row on the full lane                                                     | platform | Queued | Not executed | Archive cutover regressions  |
| WORK-007 | VAL-UAR-009        | State the adopted contract in governance, indexes, the skill, and forms, and add the fast gate   | platform | Queued | Not executed | Staged and full QA           |

## Approval and Safety Boundaries

- **Allowed Paths**: the cutover scope named in the [Spec](../spec.md).
- **Forbidden Paths**: frozen records, ledgers, and retained packages under
  `docs/98.archive/`, the sixteen ADR-0038 retained bodies, `gitops/`,
  `infrastructure/`, `policy/`, `secrets/`, `.github/`.
- **Approval Required**: accepting ADR-0039 before any work item starts. Push,
  pull request, and merge are not approved.
- **Static Validation**: focused regressions per work item,
  `python3 scripts/qa.py staged` per logical commit, and one
  `python3 scripts/qa.py full` on the final tree.
- **Live Validation**: DEFER. No live cluster, provider runtime, or network
  action is authorized.
- **Secret / Vault Handling**: No secret, credential, or private configuration
  file is read or printed.
- **Rollback Plan**: Revert the cutover commits before integration.
- **Evidence Location**: This Task record.

## Verification Summary

Not executed. The entry gate has not been met.

## Traceability

Each work item carries its observed result.

### Lifecycle Traceability

| Criterion / work item                 | Result        | Evidence                      |
| ------------------------------------- | ------------- | ----------------------------- |
| [WORK-001](../plan.md#work-breakdown) | Done. | Lifecycle gate.               |
| [WORK-002](../plan.md#work-breakdown) | Not executed. | Registry regressions.         |
| [WORK-003](../plan.md#work-breakdown) | Not executed. | Link and archive regressions. |
| [WORK-004](../plan.md#work-breakdown) | Not executed. | Lifecycle regressions.        |
| [WORK-005](../plan.md#work-breakdown) | Not executed. | Lifecycle regressions.        |
| [WORK-006](../plan.md#work-breakdown) | Not executed. | Archive cutover regressions.  |
| [WORK-007](../plan.md#work-breakdown) | Not executed. | Staged and full QA.           |
