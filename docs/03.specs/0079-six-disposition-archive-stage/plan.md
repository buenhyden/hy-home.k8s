---
title: "Six-Disposition Archive Stage Implementation Plan"
version: "1.1.0"
type: "sdlc/plan"
status: "done"
owner: "platform"
updated: "2026-09-15"
layer: "specs"
artifact_id: "SPEC-0079-PLAN-0001"
---

# Six-Disposition Archive Stage Implementation Plan

## Global Constraints

No frozen Stage 98 record, ledger, retained package, manifest comment, or record
table row changes. No lifecycle state or edge is added. A document created in a
change keeps its initial state in that change. No live cluster, provider
runtime, or network action is authorized.

## Overview

This Plan executes [Spec 0079](spec.md) in two steps. The governance step states
the six-disposition contract where its owners live. The machine step moves the
registry, archive forms, validators, and tests together once ADR-0038 is
accepted.

## Context

The retention-class list is hardcoded as `completed` in the archive validator,
the lifecycle validator, and the link validator. The archive record profile's
path pattern matches every Stage 98 path outside `migrations/` and
`completed/`, and twenty-five frozen records occupy `superseded/`. Changing the
registry without the validators would add routes no gate admits, and adding an
original-profile route under `superseded/` would make each frozen record match
two profiles. The lifecycle gate compares a change with its base, so ADR-0038
can only be created as proposed, and ADR-0032 cannot move in the same change.

## Goals & In-Scope

State the contract in common governance, the hub, and the stage indexes with the
transition boundary explicit; record the decision and its consumers; then cut
the machine surfaces over atomically.

## Non-Goals & Out-of-Scope

No rewrite of frozen content, no move of the superseded decisions already in
Stage 02, and no rewrite of citations that predate acceptance. Push, pull
request, merge, and branch cleanup follow the request owner's approval.

## Work Breakdown

| ID     | Work package                                                                                              | Depends on                                 | Entry gate                          | Exit evidence                                  |
| ------ | --------------------------------------------------------------------------------------------------------- | ------------------------------------------ | ----------------------------------- | ---------------------------------------------- |
| WP-001 | Record ADR-0038 as proposed, add ADR-0032's dated successor note, and index the decision                  | None                                       | Request owner's model and decisions | Lifecycle gate accepts the proposed decision   |
| WP-002 | State the contract in the lifecycle, authoring, and SDLC policies and the documentation hub               | WP-001                                     | ADR-0038 exists                     | Strict profile and link gates pass             |
| WP-003 | Rewrite the Stage 98 index prose around its unchanged manifest and record table                           | WP-001                                     | ADR-0038 exists                     | Archive gate passes with an unchanged manifest |
| WP-004 | Align the Stage 01, 02, and 03 indexes, AD-0006, and REQ-0003-FR-0020                                     | WP-002                                     | Policies state the contract         | Index and strict document gates pass           |
| WP-005 | Move registry routes and profiles, archive forms, validators, tests, and lint configuration in one change | WP-001 to WP-004 merged; ADR-0038 accepted | Accepted decision                   | Staged and full QA on the cutover commit       |
| WP-006 | Enumerate pending dispositions and pre-acceptance consumers with owners                                   | WP-001                                     | Consumer census                     | Task handoff record                            |

## Verification Plan

WP-001 to WP-004 and WP-006 run the strict profile, link, lifecycle, and archive
gates and one `python3 scripts/qa.py full` on the final tree. WP-005 runs
`python3 scripts/qa.py staged` over its exact index and `full` on its final
tree. Hosted CI is recorded only for an observed commit.

## Risks & Mitigations

| Risk                                                     | Mitigation                                                                                      |
| -------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| Governance prose runs ahead of what the validators admit | Every statement of the new contract carries the transition boundary, and WP-005 owns closing it |
| A frozen record matches two profiles after the cutover   | WP-005 classifies by generation before path, with a negative test for each frozen form          |
| ADR-0038 is rejected                                     | Revert the governance commit; ADR-0032 remains the contract                                     |
| A pre-acceptance citation is read as a violation         | WP-006 enumerates each consumer and its owner                                                   |

## Completion Criteria

WP-001 to WP-004 and WP-006 pass the strict document gates and full QA. WP-005
is complete only when the registry, forms, validators, and tests agree under
full QA with every frozen record unmodified, after which a later change may
accept dispositions into the new families.

## Traceability

[Spec](spec.md) owns the contract and criteria.

### Lifecycle Traceability

| Spec criterion                                             | Work package | Expected Task                                                    |
| ---------------------------------------------------------- | ------------ | ---------------------------------------------------------------- |
| [VAL-SDA-001](spec.md#success-criteria--verification-plan) | WP-001       | [tsk-0001](tasks/tsk-0001-state-the-six-disposition-contract.md) |
| [VAL-SDA-002](spec.md#success-criteria--verification-plan) | WP-002       | [tsk-0001](tasks/tsk-0001-state-the-six-disposition-contract.md) |
| [VAL-SDA-003](spec.md#success-criteria--verification-plan) | WP-003       | [tsk-0001](tasks/tsk-0001-state-the-six-disposition-contract.md) |
| [VAL-SDA-004](spec.md#success-criteria--verification-plan) | WP-004       | [tsk-0001](tasks/tsk-0001-state-the-six-disposition-contract.md) |
| [VAL-SDA-005](spec.md#success-criteria--verification-plan) | WP-005       | [tsk-0002](tasks/tsk-0002-move-registry-and-validators.md)       |
| [VAL-SDA-006](spec.md#success-criteria--verification-plan) | WP-006       | [tsk-0001](tasks/tsk-0001-state-the-six-disposition-contract.md) |
