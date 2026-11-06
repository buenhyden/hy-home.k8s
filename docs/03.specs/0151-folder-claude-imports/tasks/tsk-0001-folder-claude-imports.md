---
title: "Folder CLAUDE.md Imports"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-06"
layer: "specs"
artifact_id: "SPEC-0151-TSK-0001"
parent_ids: ["SPEC-0151-PLAN-0001"]
---

# Task: Folder CLAUDE.md Imports

## Overview

Give Claude every folder `AGENTS.md` through native folder `CLAUDE.md`
imports. It executes [SPEC-0151](../spec.md) through
[WORK-001–003](../plan.md#work-breakdown).

## Inputs

- Request (2026-11-06): review the folder `CLAUDE.md` with `@AGENTS.md`
  approach and proceed.
- Review (2026-11-06): native nested loading covers reads and compaction
  reloads, which the SPEC-0149 hook path does not.
- Approval (2026-11-06): the operator's request to review the folder `CLAUDE.md` approach and proceed approves SPEC-0151 and its Plan, drafted in `a8b2e941`; merge is separate and criterion acceptance stays the operator's.
- Start: branch `feat/folder-claude-imports` from `main` at `8be06a16`.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-CLI-001](../spec.md#success-criteria--verification-plan) | Pairing check and Codex-only folder chain | platform | ready | NOT_RUN | EVD-001 |
| WORK-002 | [VAL-CLI-002](../spec.md#success-criteria--verification-plan) | Files, profile and documentation | platform | ready | NOT_RUN | EVD-002 |
| WORK-003 | [VAL-CLI-003](../spec.md#success-criteria--verification-plan) | Observed read-only Claude session | platform | ready | NOT_RUN | EVD-003 |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-CLI-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Focused tests red then green | Pending Spec approval | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-CLI-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Strict checks and staged QA | Pending Spec approval | NOT_RUN | Pending | yes | none |
| EVD-003 | [VAL-CLI-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Observed read-only Claude session | Pending Spec approval | NOT_RUN | Pending | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-CLI-001](../spec.md#success-criteria--verification-plan) | pending | none | Run the focused tests | platform |
| [VAL-CLI-002](../spec.md#success-criteria--verification-plan) | pending | none | Run the strict checks | platform |
| [VAL-CLI-003](../spec.md#success-criteria--verification-plan) | pending | none | Observe a new session | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: the 15 folder `CLAUDE.md` files beside folder
  `AGENTS.md` files, `docs/99.templates/registry.json`, `.secrets.baseline`,
  `scripts/validation/repository/quality.py`, `scripts/provider_write_guard.py`,
  `tests/test_repository_quality_rules.py`, `tests/test_k8s_pre_edit_hook.py`,
  `.claude/provider.md`, `.codex/provider.md`,
  `.agents/governance/agent-execution.md`, `docs/03.specs/`,
  `docs/01.requirements/0003-workspace-agent-governance-platform.md`,
  `docs/90.references/audits/0001-sdlc-governance/m0002-agents-md-loading-addendum.md`
- **Forbidden Paths**: root `CLAUDE.md` and `AGENTS.md`, `.claude/CLAUDE.md`,
  `.claude/settings.json`, `.codex/hooks.json`, `docs/98.archive/`, `secrets/`
- **Approval Required**: Spec and Plan approval by the operator; merge is
  separate
- **Static Validation**: the Spec's Verification Commands
- **Live Validation**: provider-runtime only: a new Claude session
- **Secret / Vault Handling**: none
- **Rollback Plan**: revert the implementing commits
- **Evidence Location**: this Task

## Verification Summary

Pending.
