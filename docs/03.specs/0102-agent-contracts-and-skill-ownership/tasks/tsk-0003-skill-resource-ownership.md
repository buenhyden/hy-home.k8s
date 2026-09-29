---
title: "Skill resource and central gate ownership"
version: "0.1.2"
type: "sdlc/task"
status: "completed"
owner: "platform"
updated: "2026-09-29"
layer: "specs"
artifact_id: "SPEC-0102-TSK-0003"
---

# Task: Skill resource and central gate ownership

## Overview

Execute WP-002 of the approved [Plan](../plan.md). The request owner approved
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
| WORK-003 | VAL-ACS-002, VAL-ACS-012, VAL-ACS-024, VAL-ACS-025, VAL-ACS-026 | WP-002: Skill resource and central gate ownership | platform | Completed | Focused, affected and staged QA passed | This Task |

## Approval and Safety Boundaries

- **Allowed Paths**: exact files and owner delegation in WP-002 of the linked Plan; this Task
- **Forbidden Paths**: retained historical bodies, personal/global configuration, credentials, live resources, unrelated changes
- **Approval Required**: Plan execution and logical local commits approved; push, PR, merge, live changes and governance-steward self-entry remain separately operator-owned
- **Static Validation**: Plan command set C2, affected QA, exact-index staged QA, normal Git hooks; final full QA in TSK-0008
- **Live Validation**: DEFER; no authorized runtime session
- **Secret / Vault Handling**: no secret values read, printed or retained
- **Rollback Plan**: reverse this unit's reviewed logical commit together with its consumers, after dependent changes are reversed; preserve unrelated work
- **Evidence Location**: this Task

## Verification Summary

Integration follow-up: two RED route cases showed that the document registry still rejected nested references and dedicated output templates. Quality ownership extends the existing native resource routes in `docs/99.templates/registry.json` with matching `tests/test_common_agents_document_routes.py` cases; Stage 99 form authority and all other routes remain intact. This is the required consumer repair for the approved WP-002 layout, not a new workflow surface. Final aggregate evidence for this correction will be recorded with WP-003.

RED: 19 focused tests executed; three expected feature-rejection errors demonstrated the dedicated-template, transitive-resource and skill-owned-gate restrictions. Existing negative cases remain in scope. GREEN: command set C2 passed 101 tests; an additional nested symlink case passed. Actual governance validation passed: 2 providers, 17 roles, 4 permission classes, 17 skills, 67 handoffs and 51 projections. Ruff check passed; formatter changes were applied explicitly. Registered-owner and regular-file RED was demonstrated before its shared-helper implementation; no parallel gate selector was added. Affected QA and exact-index staged QA both passed, exit 0. The 7-file logical commit is `f9e0dafa`; actual-message Commitizen and normal Git invocation passed. The source index excluded later WP-003 preparation. Branch `codex/agent-contracts`, initial base
`efc3643fdce17e0c5f454c3046e7ec8a3c37d13d`. Next owner: the assigned
Plan implementer, followed by independent branch review. Static evidence
never establishes hosted, provider, account-limit or live behavior.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-003](../plan.md#work-breakdown) | Completed | Focused and aggregate QA passed; independent branch review remains in TSK-0008 |
