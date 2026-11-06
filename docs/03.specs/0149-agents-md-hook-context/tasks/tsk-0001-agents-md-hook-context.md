---
title: "Hook-Delivered Folder Agent Rules"
version: "0.2.0"
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
- Approval (2026-11-06): the operator's request to review the hook supplement and proceed approves SPEC-0149 and its Plan, drafted in `80641719`; merge is separate and criterion acceptance stays the operator's.
- Start: branch `feat/agents-md-hook-context` from `main` at `296e3379`.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-HOOK-001](../spec.md#success-criteria--verification-plan) | Guard chain and model-context output | platform | completed | PASS | EVD-005, EVD-009 |
| WORK-002 | [VAL-HOOK-002](../spec.md#success-criteria--verification-plan) | Observed Claude delivery | platform | completed | PASS | EVD-006 |
| WORK-003 | [VAL-HOOK-003](../spec.md#success-criteria--verification-plan) | Provider notes, policy and audit addendum | platform | completed | PASS | EVD-008 |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-HOOK-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Focused tests red then green | Pending Spec approval | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-HOOK-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Observed Claude delivery | Pending Spec approval | NOT_RUN | Pending | yes | none |
| EVD-003 | [VAL-HOOK-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Strict checks and review | Pending Spec approval | NOT_RUN | Pending | yes | none |
| EVD-004 | [VAL-HOOK-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Focused tests red then green | Working tree on `7bfff20b` with the new tests and the old guard | FAIL | Local run, 2026-11-06T07:47Z: `FolderAgentRulesTests` 3 failures and 1 error; the guard emitted no `hookSpecificOutput` | no | none |
| EVD-005 | [VAL-HOOK-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Focused tests red then green | Working tree on `7bfff20b` with the guard change | PASS | Local run, 2026-11-06T07:48Z to 07:50Z: `FolderAgentRulesTests` 5 OK; `tests.test_k8s_pre_edit_hook` OK after one count test was rewritten to check each output field; ruff check and format clean | yes | EVD-001 |
| EVD-006 | [VAL-HOOK-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Observed Claude delivery | Claude Code 2.1.319, this session, the edited guard behind the unchanged `.claude/hooks/k8s-pre-edit.sh` | PASS | 2026-11-06 about 07:51Z: a `Write` of the AUD-0001 m0002 member returned PreToolUse `additionalContext` to the model with the Template-First guidance and the full text of `docs/AGENTS.md` and `docs/90.references/AGENTS.md`, without the root gateway; the retry in the same session returned the guidance only; a later Bash call supplied `scripts/AGENTS.md` once | yes | EVD-002 |
| EVD-007 | [VAL-HOOK-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Observed Codex delivery | codex-cli 0.166.0 | DEFER | 2026-11-06: the read-only probe stopped at the usage limit until 2026-11-09 18:37; next owner operator | no | none |
| EVD-008 | [VAL-HOOK-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Strict checks and review | Staged index on `7bfff20b` with the provider notes, policy and m0002 | PASS | Local run, 2026-11-06: `python3 scripts/qa.py staged` 11 gates PASS including tooling-tests and agent-governance; `validate-agent-governance.py` PASS | yes | EVD-003 |
| EVD-009 | [VAL-HOOK-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Focused tests red then green | Working tree on `7bfff20b` after the review fixes | PASS | Local run, 2026-11-06T07:56Z: the independent review reproduced two BLOCK paths (a nested state file raised `RecursionError`, a lone-surrogate `session_id` raised `UnicodeEncodeError`, both exit 2; the reviewer re-ran both repros after the fix and they exit 0); fixed by catching every folder-context failure, treating corrupt state as empty, ignoring a state directory not private to the user, reading `AGENTS.md` with `O_NOFOLLOW`, recording delivery only after the selector allows the write, and re-raising the guard deadline `TimeoutError`; `FolderAgentRulesTests` 7 OK with two new regressions; `tests.test_k8s_pre_edit_hook` OK; ruff clean | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-HOOK-001](../spec.md#success-criteria--verification-plan) | accepted | EVD-005, EVD-009 | Operator accepted on 2026-11-06 after review | platform |
| [VAL-HOOK-002](../spec.md#success-criteria--verification-plan) | accepted | EVD-006 | Operator accepted on 2026-11-06 after review | platform |
| [VAL-HOOK-003](../spec.md#success-criteria--verification-plan) | accepted | EVD-008 | Operator accepted on 2026-11-06 after review | platform |

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

- Tests: the focused tests failed on the old guard (EVD-004) and pass with
  the change; the whole hook module passes (EVD-005).
- Claude runtime: observed in this session; folder rules reached the model
  once per session and the root gateway was excluded (EVD-006).
- Codex runtime: DEFER until the usage limit resets on 2026-11-09 (EVD-007).
- Static: staged QA 11 gates PASS (EVD-008).
- Review: two BLOCK paths found and fixed with regressions (EVD-009).
- Residual risk: read-only tools are not hooked; the shell heuristic can
  supply a folder's rules for a command that only runs a script there; a
  context compaction is not detected, so rules supplied before it are not
  supplied again; Codex acceptance of the new field is unverified.
- Next owner: operator, for criterion acceptance, merge and the Codex probe.
  Rollback: revert the implementing commit.
