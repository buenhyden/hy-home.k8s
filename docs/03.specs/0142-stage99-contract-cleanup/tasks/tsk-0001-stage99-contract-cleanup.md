---
title: "Stage 99 Contract Cleanup"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-05"
layer: "specs"
artifact_id: "SPEC-0142-TSK-0001"
parent_ids: ["SPEC-0142-PLAN-0001"]
---

# Task: Stage 99 Contract Cleanup

## Overview

Remove the stale and unused items the 2026-11-05 Stage 99 audits found. It
executes [SPEC-0142](../spec.md) through [WORK-001–004](../plan.md#work-breakdown).

## Inputs

- Request (2026-11-05): check `docs/99.templates/` against its governance,
  forms and the current repository, correct conflicts, and remove
  contradictions and repetition inside each file.
- Operator choice (2026-11-05): commit the Stage 05 and Stage 90 work first
  (`c1bbde2e`, `90c15f94`) and take the low-risk cleanup scope.
- Start: branch `docs/requirements-conformance` at `90c15f94`.
- Approval (2026-11-05): the operator's choice of the low-risk cleanup scope
  approves SPEC-0142 and its Plan after review of the draft in `6442183c`. It
  authorizes the repository change only.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-S99-001](../spec.md#success-criteria--verification-plan) | Stage 00 promotion target and wording | platform | ready | NOT_RUN | EVD-001 |
| WORK-002 | [VAL-S99-002](../spec.md#success-criteria--verification-plan) | ADR form trace cells | platform | ready | NOT_RUN | EVD-002 |
| WORK-003 | [VAL-S99-003](../spec.md#success-criteria--verification-plan) | Unused modes, branches, definition and language entry | platform | ready | NOT_RUN | EVD-003 |
| WORK-004 | [VAL-S99-004](../spec.md#success-criteria--verification-plan) | Stage 99 README and AGENTS prose | platform | ready | NOT_RUN | EVD-004 |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-S99-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Lifecycle regression test | Pending | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-S99-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Template and profile checks | Pending | NOT_RUN | Pending | yes | none |
| EVD-003 | [VAL-S99-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Schema regression test and code search | Pending | NOT_RUN | Pending | yes | none |
| EVD-004 | [VAL-S99-004](../spec.md#success-criteria--verification-plan) | WORK-004 | Document contract suite and strict document checks | Pending | NOT_RUN | Pending | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-S99-001](../spec.md#success-criteria--verification-plan) | pending | none | Run EVD-001 | platform |
| [VAL-S99-002](../spec.md#success-criteria--verification-plan) | pending | none | Run EVD-002 | platform |
| [VAL-S99-003](../spec.md#success-criteria--verification-plan) | pending | none | Run EVD-003 | platform |
| [VAL-S99-004](../spec.md#success-criteria--verification-plan) | pending | none | Run EVD-004 | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: `docs/99.templates/`, `scripts/validate-document-lifecycle.py`,
  `scripts/validate-markdown-profiles.py`, `scripts/validate-links-and-owners.py`,
  `scripts/document_contracts.py`, `scripts/document_authority.py`, `tests/`,
  `.secrets.baseline`, `.agents/governance/document-lifecycle.md`,
  `docs/03.specs/`, `docs/01.requirements/0003-workspace-agent-governance-platform.md`
- **Forbidden Paths**: current document bodies outside the Allowed Paths
- **Approval Required**: the operator's 2026-11-05 request authorizes the
  repository change; push and merge are separate.
- **Static Validation**: document contract suite, strict document checks,
  `python3 scripts/qa.py staged`
- **Live Validation**: not applicable
- **Secret / Vault Handling**: none; only a baseline line number moves
- **Rollback Plan**: revert the implementing commits
- **Evidence Location**: this Task

## Verification Summary

Not run yet.
