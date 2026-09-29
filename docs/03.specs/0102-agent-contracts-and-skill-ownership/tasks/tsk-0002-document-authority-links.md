---
title: "Document authority and normalized links"
version: "0.1.1"
type: "sdlc/task"
status: "completed"
owner: "platform"
updated: "2026-09-29"
layer: "specs"
artifact_id: "SPEC-0102-TSK-0002"
---

# Task: Document authority and normalized links

## Overview

Execute WP-001 of the approved [Plan](../plan.md). The request owner approved
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
| WORK-002 | VAL-ACS-003, VAL-ACS-023 | WP-001: Document authority and normalized links | platform | Completed | C1 and exact-index QA passed | This Task |

## Approval and Safety Boundaries

- **Allowed Paths**: exact files and owner delegation in WP-001 of the linked Plan; this Task
- **Forbidden Paths**: retained historical bodies, personal/global configuration, credentials, live resources, unrelated changes
- **Approval Required**: Plan execution and logical local commits approved; push, PR, merge, live changes and governance-steward self-entry remain separately operator-owned
- **Static Validation**: Plan command set C1, affected QA, exact-index staged QA, normal Git hooks; final full QA in TSK-0008
- **Live Validation**: DEFER; no authorized runtime session
- **Secret / Vault Handling**: no secret values read, printed or retained
- **Rollback Plan**: reverse this unit's reviewed logical commit together with its consumers, after dependent changes are reversed; preserve unrelated work
- **Evidence Location**: this Task

## Verification Summary

Final exact-index QA passed all 14 gates for 25 paths, exit 0; logical commit `1a6e089e` passed actual-message Commitizen and normal Git invocation. An earlier staged session lost its output handle on context restoration; its result was not claimed and the same index was rerun with a captured log. Independent branch review remains assigned to TSK-0008.

WP-000 passed six staged gates for each of commits `8e811506` and `79c97514`; both actual messages passed Commitizen. Additional RED/GREEN: unquoted HTML href was missed, then rejected; the same 65-test suite passed again. Ruff explicitly formatted only the two edited Python files. R23 RED: six failures exposed rejected README navigation and missing normalization/exception handling. GREEN: `python3 -m unittest tests.test_documentation_link_boundary tests.test_common_agents_document_routes tests.test_readme_navigation` passed 65 tests. Quick QA first attempt: 12/14 gates passed; link/navigation and repository-quality exposed stale current-owner checks and a staging README template reference. Ruling: update those exact consumers and required current-owner checks, preserving failure semantics; do not waive them. Second quick result: 13/14 PASS; the only remaining error was my reference to a nonexistent governance README. Corrected it to the actual governance directory; final exact-index validation covers that repair. Manual audit converted current Markdown consumers; synthetic evaluation responses and retained documents remain data/history. Shared policy, archive procedure, GitHub and scripts guidance now name current owners instead of historical decisions as execution prerequisites. Branch `codex/agent-contracts`, initial base
`efc3643fdce17e0c5f454c3046e7ec8a3c37d13d`. Next owner: the assigned
Plan implementer, followed by independent branch review. Static evidence
never establishes hosted, provider, account-limit or live behavior.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-002](../plan.md#work-breakdown) | Completed | C1: 65 tests; staged QA: 14/14 PASS; commit `1a6e089e` |
