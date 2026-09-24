---
title: "Observe Provider Native Runtime"
version: "0.1.0"
type: "sdlc/task"
status: "queued"
owner: "platform"
updated: "2026-09-24"
layer: "specs"
artifact_id: "SPEC-0086-TSK-0001"
---

# Task: Observe Provider Native Runtime

## Overview

Own the operator-authorized native-runtime observation for Claude and Codex
that [SPEC-0072-TSK-0001](../../0072-agent-governance-and-quality-gate-consolidation/tasks/tsk-0001-consolidate-governance-and-quality-gates.md)
transferred here on 2026-09-24 rather than claiming as passed. This record is
append-only evidence of what an operator-authorized session actually observed;
it never promotes a repository-static or hosted-CI result to runtime evidence.

## Inputs

- [Owning Spec](../spec.md)
- [Owning Plan](../plan.md)
- [SPEC-0072-TSK-0001](../../0072-agent-governance-and-quality-gate-consolidation/tasks/tsk-0001-consolidate-governance-and-quality-gates.md), which recorded `WORK-009` and transferred it here
- `.claude/provider.md` and `.codex/provider.md`

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | VAL-PNRO-001, VAL-PNRO-003, VAL-PNRO-005, VAL-PNRO-007 | Obtain an operator-authorized Claude session and observe discovery, invocation/model access, sandbox enforcement, and event delivery | operator | Queued | Not executed | Dated session record naming client version, exact command, and observed result |
| WORK-002 | VAL-PNRO-002, VAL-PNRO-004, VAL-PNRO-006, VAL-PNRO-008 | Obtain an operator-authorized Codex session and observe the same four properties | operator | Queued | Not executed | Dated session record naming client version, exact command, and observed result |

## Approval and Safety Boundaries

- **Allowed Paths**: this Task, the owning Spec and Plan, and this package's index rows
- **Forbidden Paths**: live credentials, secret values, private configuration, session logs beyond the recorded client identity and result
- **Approval Required**: any native Provider session; the operator alone authorizes it. No agent may authorize, simulate, or infer it.
- **Static Validation**: none satisfies this Task's criteria; see the owning Spec's Verification Commands
- **Live Validation**: the operator-authorized native session itself, recorded per provider
- **Secret / Vault Handling**: no credential, token, or private configuration is read, printed, or recorded
- **Rollback Plan**: no mutation occurs; a recorded observation is append-only evidence and needs no rollback
- **Evidence Location**: this Task

## Verification Summary

No repository-static command exists for this Task's acceptance criteria. Each
row closes only on a dated, attributed operator-authorized session record.

## Traceability

- Stable Task: `SPEC-0086-TSK-0001`
- Predecessor: `SPEC-0072-TSK-0001` `WORK-009`, transferred here on 2026-09-24

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-001](../plan.md#work-breakdown) | Not executed | Queued; requires an operator-authorized Claude session |
| [WORK-002](../plan.md#work-breakdown) | Not executed | Queued; requires an operator-authorized Codex session |
