---
title: "Role and provider contract alignment"
version: "0.1.0"
type: "sdlc/task"
status: "queued"
owner: "platform"
updated: "2026-09-29"
layer: "specs"
artifact_id: "SPEC-0102-TSK-0006"
---

# Task: Role and provider contract alignment

## Overview

Execute WP-005 of the approved [Plan](../plan.md). The request owner approved
the Spec and ADR, then approved Plan execution on 2026-09-29.
The current session implements this bounded unit under its assigned role;
the final branch receives independent review.

## Inputs

- [Spec](../spec.md)
- [Plan and work breakdown](../plan.md#work-breakdown)
- [ADR-0047](../../../02.architecture/decisions/0047-agent-contract-and-resource-ownership.md)

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-006 | VAL-ACS-001, VAL-ACS-004, VAL-ACS-005, VAL-ACS-008, VAL-ACS-009, VAL-ACS-010, VAL-ACS-013, VAL-ACS-015, VAL-ACS-016, VAL-ACS-017, VAL-ACS-018, VAL-ACS-019, VAL-ACS-020, VAL-ACS-021, VAL-ACS-028, VAL-ACS-029, VAL-ACS-031 | WP-005: Role and provider contract alignment | platform | Queued | Not executed | This Task |

## Approval and Safety Boundaries

- **Allowed Paths**: exact files and owner delegation in WP-005 of the linked Plan; this Task
- **Forbidden Paths**: retained historical bodies, personal/global configuration, credentials, live resources, unrelated changes
- **Approval Required**: Plan execution and logical local commits approved; push, PR, merge, live changes and governance-steward self-entry remain separately operator-owned
- **Static Validation**: Plan command set C5, affected QA, exact-index staged QA, normal Git hooks; final full QA in TSK-0008
- **Live Validation**: DEFER; no authorized runtime session
- **Secret / Vault Handling**: no secret values read, printed or retained
- **Rollback Plan**: reverse this unit's reviewed logical commit together with its consumers, after dependent changes are reversed; preserve unrelated work
- **Evidence Location**: this Task

## Verification Summary

Not executed. Branch `codex/agent-contracts`, initial base
`efc3643fdce17e0c5f454c3046e7ec8a3c37d13d`. Next owner: the assigned
Plan implementer, followed by independent branch review. Static evidence
never establishes hosted, provider, account-limit or live behavior.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-006](../plan.md#work-breakdown) | Queued | No implementation or verification yet |
