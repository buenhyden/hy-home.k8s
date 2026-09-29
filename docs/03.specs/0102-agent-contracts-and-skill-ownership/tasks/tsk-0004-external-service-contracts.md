---
title: "External service contract audit"
version: "0.1.2"
type: "sdlc/task"
status: "completed"
owner: "platform"
updated: "2026-09-29"
layer: "specs"
artifact_id: "SPEC-0102-TSK-0004"
---

# Task: External service contract audit

## Overview

Execute WP-003 of the approved [Plan](../plan.md). The request owner approved
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
| WORK-004 | VAL-ACS-027 | WP-003: External service contract audit | platform | Completed | Static checker, consumer tests and final index passed | This Task |

## Approval and Safety Boundaries

- **Allowed Paths**: exact files and owner delegation in WP-003 of the linked Plan; this Task
- **Forbidden Paths**: retained historical bodies, personal/global configuration, credentials, live resources, unrelated changes
- **Approval Required**: Plan execution and logical local commits approved; push, PR, merge, live changes and governance-steward self-entry remain separately operator-owned
- **Static Validation**: Plan command set C3, affected QA, exact-index staged QA, normal Git hooks; final full QA in TSK-0008
- **Live Validation**: DEFER; no authorized runtime session
- **Secret / Vault Handling**: no secret values read, printed or retained
- **Rollback Plan**: reverse this unit's reviewed logical commit together with its consumers, after dependent changes are reversed; preserve unrelated work
- **Evidence Location**: this Task

## Verification Summary

RED import failed because the dedicated checker did not exist. GREEN: the first eight tests passed, including real repository manifests, split Alloy slices, repeated endpoints, Valkey frontend/backend mapping, malformed/redacted input and unsafe paths. The CLI additionally passed new-nonignored-YAML coverage. Unroutable-address RED produced four failures, then the standard-library fix passed all 10 checker tests. Combined C3, routing and profile tests passed 49 cases. Actual registry validation passed with 18 skills and unchanged 17 roles/51 projections. Ruff check passed. The optional system skill-creator quick validator rejects the repository-required `disable-model-invocation` key; its generic frontmatter schema is incompatible with this approved native package contract. The repository governance and Stage 99 validators remain the owning checks; no native invocation control was removed to satisfy that optional tool. Consumer regression initially found test-generated Python bytecode inside the closed skill package and a held-owner snapshot reopening the registry. The test import now suppresses bytecode, task-created cache was removed, and supplied contract facts retain their read-free validation path; normal QA still checks the registered skill owner and regular checker path. The 95-test registry/consumer/tooling/checker suite then passed. First affected and staged QA each passed 13/14 gates; repository-quality exposed a skill-local relative executable link being interpreted as root scripts. Added RED/GREEN coverage in `tests/test_current_executable_references.py` (10 tests PASS) and repaired the shared extractor `scripts/validation/current_executable_references.py`, including missing full skill-script detection. This necessary caller repair is delegated to the existing quality owner. The repaired 20-path index passed all 14 gates. Further negative review found that empty non-mapping selectors were silently classified as selectorless; three RED cases now fail closed and all 11 checker tests pass. The manifest runner expectation now includes the deliberately registered eighth gate. The 21-path selector-repair index passed all 14 gates. Broader routing tests then identified six selection fixtures requiring the newly selected gate; their exact expected sets were updated. The 28-test selector/runner/checker suite passed. The complete unit, including those fixture consumers, receives its final exact-index check; The final 22-path index passed all 14 gates and commit `025ada90` passed Commitizen and normal hooks. Independent final review remains in TSK-0008. Branch `codex/agent-contracts`, initial base
`efc3643fdce17e0c5f454c3046e7ec8a3c37d13d`. Next owner: the assigned
Plan implementer, followed by independent branch review. Static evidence
never establishes hosted, provider, account-limit or live behavior.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-004](../plan.md#work-breakdown) | Completed | 11 checker tests, 28 routing/runner tests, 95 owner tests, final staged QA 14/14; commit `025ada90` |
