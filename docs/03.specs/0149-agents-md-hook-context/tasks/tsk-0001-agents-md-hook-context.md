---
title: "Hook-Delivered Folder Agent Rules"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-06"
layer: "specs"
artifact_id: "SPEC-0149-TSK-0001"
parent_ids: ["SPEC-0149-PLAN-0001"]
---

# Task: Hook-Delivered Folder Agent Rules

## Overview

Make the shared guard supply folder `AGENTS.md` text to the model on writes
for both providers. It executes [SPEC-0149](../spec.md) through
[WORK-001–003](../plan.md#work-breakdown).

## Inputs

- Request (2026-11-06): review the AGENTS.md check and the hook supplement
  and proceed; each folder's `AGENTS.md` must be read by Codex and Claude.
- Review (2026-11-06): the shared guard is the one owner that sees both
  providers' writes; nested `CLAUDE.md` and user settings were not chosen.
- Start: branch `feat/agents-md-hook-context` from `main` at `296e3379`.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-HOOK-001](../spec.md#success-criteria--verification-plan) | Guard chain and model-context output | platform | draft | NOT_RUN | EVD-001 |
| WORK-002 | [VAL-HOOK-002](../spec.md#success-criteria--verification-plan) | Observed Claude delivery | platform | draft | NOT_RUN | EVD-002 |
| WORK-003 | [VAL-HOOK-003](../spec.md#success-criteria--verification-plan) | Provider notes, policy and audit addendum | platform | draft | NOT_RUN | EVD-003 |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-HOOK-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Focused tests red then green | Pending Spec approval | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-HOOK-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Observed Claude delivery | Pending Spec approval | NOT_RUN | Pending | yes | none |
| EVD-003 | [VAL-HOOK-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Strict checks and review | Pending Spec approval | NOT_RUN | Pending | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-HOOK-001](../spec.md#success-criteria--verification-plan) | pending | none | Run the focused tests | platform |
| [VAL-HOOK-002](../spec.md#success-criteria--verification-plan) | pending | none | Observe a Claude write | platform |
| [VAL-HOOK-003](../spec.md#success-criteria--verification-plan) | pending | none | Run the strict checks and review | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: `scripts/provider_write_guard.py`,
  `tests/test_k8s_pre_edit_hook.py`, `.claude/provider.md`,
  `.codex/provider.md`, `.agents/governance/agent-execution.md`,
  `docs/03.specs/`, `docs/01.requirements/0003-workspace-agent-governance-platform.md`,
  `docs/90.references/audits/0001-sdlc-governance/`
- **Forbidden Paths**: `.claude/settings.json`, `.codex/hooks.json`,
  `.codex/config.toml`, both hook adapters, user-level settings, `secrets/`
- **Approval Required**: Spec and Plan approval by the operator; merge is
  separate; Codex runtime observation waits for the usage limit reset
- **Static Validation**: the Spec's Verification Commands
- **Live Validation**: provider-runtime only: Claude in this session, Codex
  DEFER to 2026-11-09
- **Secret / Vault Handling**: none; `AGENTS.md` files hold no secrets
- **Rollback Plan**: revert the implementing commit
- **Evidence Location**: this Task

## Verification Summary

Pending.
