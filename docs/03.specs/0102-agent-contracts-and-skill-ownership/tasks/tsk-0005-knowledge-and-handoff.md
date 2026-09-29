---
title: "Knowledge, resume and bounded prompt input"
version: "0.1.1"
type: "sdlc/task"
status: "in-progress"
owner: "platform"
updated: "2026-09-29"
layer: "specs"
artifact_id: "SPEC-0102-TSK-0005"
---

# Task: Knowledge, resume and bounded prompt input

## Overview

Execute WP-004 of the approved [Plan](../plan.md). The request owner approved
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
| WORK-005 | VAL-ACS-006, VAL-ACS-007, VAL-ACS-014, VAL-ACS-022 | WP-004: Knowledge, resume and bounded prompt input | platform | In Progress | Prompt bounded-capture RED reproduced | This Task |

## Approval and Safety Boundaries

- **Allowed Paths**: exact files and owner delegation in WP-004 of the linked Plan; this Task
- **Forbidden Paths**: retained historical bodies, personal/global configuration, credentials, live resources, unrelated changes
- **Approval Required**: Plan execution and logical local commits approved; push, PR, merge, live changes and governance-steward self-entry remain separately operator-owned
- **Static Validation**: Plan command set C4, affected QA, exact-index staged QA, normal Git hooks; final full QA in TSK-0008
- **Live Validation**: DEFER; no authorized runtime session
- **Secret / Vault Handling**: no secret values read, printed or retained
- **Rollback Plan**: reverse this unit's reviewed logical commit together with its consumers, after dependent changes are reversed; preserve unrelated work
- **Evidence Location**: this Task

## Verification Summary

RED: the oversized Git diff produced a partial draft instead of refusing; the bounded-runner timeout seam was absent. The existing bounded I/O helper is now used during capture with redacted explicit failure and no draft. GREEN: 30 prompt/knowledge tests pass. Fact metadata RED produced nine failures, then missing fields, expiry, sensitivity, stale/deleted source and review-state cases passed; a separate untracked-source RED failed before tracked-source enforcement. An intermediate test edit had an indentation error and was corrected, not counted as behavioral RED. The existing bounded reader rejects source symlinks and prevents reading untracked/private source files. Actual knowledge validation passed for both current documents. C4 initially ran 126 tests and exposed the new external-service gate missing from the runner expectation; that owning WP-003 consumer is corrected. Final C4 passed 126 tests. Affected QA passed all selected gates on the 32-path working-tree snapshot. The exact WP-004 index and independent final review remain pending. Branch `codex/agent-contracts`, initial base
`efc3643fdce17e0c5f454c3046e7ec8a3c37d13d`. Next owner: the assigned
Plan implementer, followed by independent branch review. Static evidence
never establishes hosted, provider, account-limit or live behavior.

### Resume contract review

The context policy is the single resume-decision owner. Work lifecycle,
delegated development and the handoff prompt now consume it. Under the existing
quality snapshot/approval/limitation fields, the receiving agent must re-observe
worktree, branch, HEAD/base, file hashes, staged/unstaged scope, changed consumers,
authorization/revocation, writer ownership and incomplete output.

| Reviewed condition | Required decision / evidence limit |
| --- | --- |
| Matching branch/HEAD but changed relevant hash | Stop dependent writes; refresh the affected evidence. |
| Different branch or HEAD/base | Stop and reconcile the current Task snapshot. |
| Missing or revoked approval | Stop; next owner is the request owner/operator. |
| Concurrent writer conflict | Preserve work; resolve ownership before another write. |
| Expired/deleted fact source | Invalidate observation/cache; re-read current owner. |
| Partial/over-limit input | No assembled draft; retain only separately verified evidence. |

These are static contract review cases. The prompt assembler collects read-only
inputs and cannot authenticate user approval or enforce another provider's
mutation boundary. Native enforcement remains DEFER; no generic resume engine
or fabricated approval state was added.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-005](../plan.md#work-breakdown) | In Progress | C4 and affected QA passed; exact index and independent final review pending |
