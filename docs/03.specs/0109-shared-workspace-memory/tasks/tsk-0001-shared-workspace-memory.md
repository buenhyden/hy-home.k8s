---
title: "Shared Workspace Memory Store"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-10-13"
layer: "specs"
artifact_id: "SPEC-0109-TSK-0001"
parent_ids: ["SPEC-0109-PLAN-0001"]
---

# Task: Shared Workspace Memory Store

## Overview

Execute the three work units of the [Plan](../plan.md) for
[SPEC-0109](../spec.md) and record their evidence here.

## Inputs

- [SPEC-0109](../spec.md) and its [Plan](../plan.md).
- Operator approval on 2026-10-13 of the revised SPEC-0109 design and its
  implementation, including native memory disablement.
- Branch head `fc8f468c` before this package's Plan.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-MEMORY-001](../spec.md#success-criteria--verification-plan) | Store module, CLI and Git ignore entry | platform | in-progress | NOT_RUN | Pending named repository evidence |
| WORK-002 | [VAL-MEMORY-002](../spec.md#success-criteria--verification-plan) | Native memory disablement and validation | platform | in-progress | NOT_RUN | Pending named repository evidence |
| WORK-003 | [VAL-MEMORY-001](../spec.md#success-criteria--verification-plan) | Memory policy and requirement revision | platform | in-progress | NOT_RUN | Pending named repository evidence |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-MEMORY-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Store tests and staged QA | WORK-001 commit index | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-MEMORY-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Native settings tests and staged QA | WORK-002 commit index | NOT_RUN | Pending | yes | none |
| EVD-003 | [VAL-MEMORY-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Cross-provider session observation | Two real provider sessions in two worktrees | NOT_RUN | Pending | yes | none |
| EVD-004 | [VAL-MEMORY-001](../spec.md#success-criteria--verification-plan) | WORK-003 | Policy validators and staged QA | WORK-003 commit index | NOT_RUN | Pending | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-MEMORY-001](../spec.md#success-criteria--verification-plan) | pending | none | Run WORK-001 and WORK-003 checks | platform |
| [VAL-MEMORY-002](../spec.md#success-criteria--verification-plan) | pending | none | Run WORK-002 checks and observe two sessions | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: this package, `scripts/workspace_memory.py`,
  `tests/test_workspace_memory.py`, `.gitignore`, `.claude/settings.json`,
  `.codex/config.toml`, `scripts/validate-agent-governance.py`,
  `tests/test_agent_governance.py`, `.claude/provider.md`,
  `.codex/provider.md`, `.codex/README.md`, `.claude/README.md`,
  `.agents/README.md`, `.agents/governance/context-and-memory.md`,
  `docs/01.requirements/0003-workspace-agent-governance-platform.md`,
  `docs/03.specs/README.md`.
- **Forbidden Paths**: existing native memory directories under the user's
  home, user or managed provider configuration, frozen Archive payloads,
  live cluster, Vault and secret material.
- **Approval Required**: the operator approved the design and its
  implementation on 2026-10-13; push, pull request and merge await the
  operator.
- **Static Validation**: focused store and governance tests, document
  validators and staged QA from the documented validation environment.
- **Live Validation**: DEFER until two real provider sessions are observed.
- **Secret / Vault Handling**: the store rejects secret sensitivity; no
  secret is read or printed.
- **Rollback Plan**: forward revert of the package commits; the ignored
  store file is left for the operator to keep or remove.
- **Evidence Location**: this Task and Git history.

## Verification Summary

Pending execution.
