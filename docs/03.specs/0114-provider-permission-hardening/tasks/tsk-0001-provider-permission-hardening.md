---
title: "Provider Native Permission and Hook Hardening"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-10-13"
layer: "specs"
artifact_id: "SPEC-0114-TSK-0001"
parent_ids: ["SPEC-0114-PLAN-0001"]
---

# Task: Provider Native Permission and Hook Hardening

## Overview

Execute the nine work units of the [Plan](../plan.md) for
[SPEC-0114](../spec.md) and record their evidence here.

## Inputs

- [SPEC-0114](../spec.md) and its [Plan](../plan.md).
- Operator requests on 2026-10-13: allow the needed commands in
  `.claude/settings.json`; review deletion denies; review the whole
  permission set for security and risk; check that `.agents`, `.claude`
  and `.codex` fulfil their roles; review `.codex/config.toml` and both
  hooks and apply the changes. The operator chose to allow push, pull
  request creation and merge on Claude and network access in the Codex
  workspace sandbox.
- Read-only reviews on main `3897353ebc815410eed2a3e3606d3cfa3149b97b`:
  the governance validator passed (17 roles, 18 skills, 51 projections);
  the write guard exited 0 for a `NotebookEdit` payload and for a
  Bash-carried `apply_patch` envelope.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-PERM-001](../spec.md#success-criteria--verification-plan) | Claude secret read and secret-output denies | platform | ready | NOT_RUN | Pending named repository evidence |
| WORK-002 | [VAL-PERM-002](../spec.md#success-criteria--verification-plan) | Claude option-first cluster and tool mutation denies | platform | ready | NOT_RUN | Pending named repository evidence |
| WORK-003 | [VAL-PERM-003](../spec.md#success-criteria--verification-plan) | Claude deletion and history-destroying denies | platform | ready | NOT_RUN | Pending named repository evidence |
| WORK-004 | [VAL-PERM-005](../spec.md#success-criteria--verification-plan) | Fail-closed shared guard and adapters | platform | ready | NOT_RUN | Pending named repository evidence |
| WORK-005 | [VAL-PERM-004](../spec.md#success-criteria--verification-plan) | Claude allow, ask and bypass mode | platform | ready | NOT_RUN | Pending named repository evidence |
| WORK-006 | [VAL-PERM-006](../spec.md#success-criteria--verification-plan) | Codex config security keys | platform | ready | NOT_RUN | Pending named repository evidence |
| WORK-007 | [VAL-PERM-007](../spec.md#success-criteria--verification-plan) | Codex forbidden rules | platform | ready | NOT_RUN | Pending named repository evidence |
| WORK-008 | [VAL-PERM-008](../spec.md#success-criteria--verification-plan) | Codex hook path independent of the session directory | platform | ready | NOT_RUN | Pending named repository evidence |
| WORK-009 | [VAL-PERM-009](../spec.md#success-criteria--verification-plan) | Provider notes, READMEs, REQ-0003 links and session probes | platform | ready | NOT_RUN | Pending named repository evidence |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-PERM-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Focused checks and staged QA | WORK-001 commit index | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-PERM-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Focused checks and staged QA | WORK-002 commit index | NOT_RUN | Pending | yes | none |
| EVD-003 | [VAL-PERM-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Focused checks and staged QA | WORK-003 commit index | NOT_RUN | Pending | yes | none |
| EVD-004 | [VAL-PERM-005](../spec.md#success-criteria--verification-plan) | WORK-004 | Focused checks and staged QA | WORK-004 commit index | NOT_RUN | Pending | yes | none |
| EVD-005 | [VAL-PERM-004](../spec.md#success-criteria--verification-plan) | WORK-005 | Focused checks and staged QA | WORK-005 commit index | NOT_RUN | Pending | yes | none |
| EVD-006 | [VAL-PERM-006](../spec.md#success-criteria--verification-plan) | WORK-006 | Focused checks and staged QA | WORK-006 commit index | NOT_RUN | Pending | yes | none |
| EVD-007 | [VAL-PERM-007](../spec.md#success-criteria--verification-plan) | WORK-007 | Focused checks and staged QA | WORK-007 commit index | NOT_RUN | Pending | yes | none |
| EVD-008 | [VAL-PERM-008](../spec.md#success-criteria--verification-plan) | WORK-008 | Focused checks and staged QA | WORK-008 commit index | NOT_RUN | Pending | yes | none |
| EVD-009 | [VAL-PERM-009](../spec.md#success-criteria--verification-plan) | WORK-009 | Focused checks and staged QA | WORK-009 commit index | NOT_RUN | Pending | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-PERM-001](../spec.md#success-criteria--verification-plan) | pending | none | Run WORK-001 checks | platform |
| [VAL-PERM-002](../spec.md#success-criteria--verification-plan) | pending | none | Run WORK-002 checks | platform |
| [VAL-PERM-003](../spec.md#success-criteria--verification-plan) | pending | none | Run WORK-003 checks | platform |
| [VAL-PERM-004](../spec.md#success-criteria--verification-plan) | pending | none | Run WORK-005 checks | platform |
| [VAL-PERM-005](../spec.md#success-criteria--verification-plan) | pending | none | Run WORK-004 checks | platform |
| [VAL-PERM-006](../spec.md#success-criteria--verification-plan) | pending | none | Run WORK-006 checks | platform |
| [VAL-PERM-007](../spec.md#success-criteria--verification-plan) | pending | none | Run WORK-007 checks | platform |
| [VAL-PERM-008](../spec.md#success-criteria--verification-plan) | pending | none | Run WORK-008 checks | platform |
| [VAL-PERM-009](../spec.md#success-criteria--verification-plan) | pending | none | Run WORK-009 checks | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: this package; `docs/03.specs/README.md`;
  `docs/01.requirements/0003-workspace-agent-governance-platform.md`;
  `.claude/settings.json`, `.claude/hooks/k8s-pre-edit.sh`,
  `.claude/provider.md`, `.claude/README.md`; `.codex/config.toml`,
  `.codex/hooks.json`, `.codex/hooks/pre-tool-use.sh`,
  `.codex/rules/default.rules`, `.codex/provider.md`, `.codex/README.md`;
  `scripts/validate-agent-governance.py`,
  `scripts/provider_write_guard.py`; their tests under `tests/`.
- **Forbidden Paths**: removal of any existing deny entry; personal,
  user-level or managed settings; project trust; workflows; live cluster,
  Vault and secret material.
- **Approval Required**: SPEC-0114 and Plan approval; push, pull request
  and merge are run only on an operator request.
- **Static Validation**: governance and guard tests, the governance
  validator, `codex execpolicy check` and staged QA from the documented
  validation environment.
- **Live Validation**: DEFER — probes use dry-run or missing targets and
  touch no live surface.
- **Secret / Vault Handling**: no secret is read or printed.
- **Rollback Plan**: forward revert of the package commits.
- **Evidence Location**: this Task and Git history.

## Verification Summary

Pending execution.
