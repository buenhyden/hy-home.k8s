---
title: "W01 3.0.1 Follow-up"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-15"
artifact_id: "SPEC-0218-TSK-0001"
parent_ids: ["SPEC-0218-PLAN-0001"]
---

# Task: W01 3.0.1 Follow-up

## Scope

### Objective and Parent

This Task executes WORK-001 to WORK-003 of the [Plan](../plan.md) for [SPEC-0218](../spec.md) criteria VAL-W01F-001 to VAL-W01F-003.

### Inputs and Authority

- **Request:** on 2026-11-15 (Asia/Seoul) the user asked to re-audit the W01 prompt for remaining, unverified, unreviewed, unconfirmed, unrun, conflicting and missing items, fix them with the requirements first, and then commit, push, open a PR and merge. The original wording is quoted in the session. This approves no Spec or Plan bytes and no criterion.
- **Base:** `main` at `c0af5a76`; branch `claude/w01-followup`.
- **Survey:** a read-only `docs-researcher` subagent audited roles, workflows, skills, provider notes and gateways; this session verified the cited lines. The named evidence checks ran once on `c0af5a76` in the background (registered commands, pinned `hyhome-validation` environment).
- **Design summary:**
  - Reference designs: D00, D01 and D15, edition 3.0.1.
  - Current difference: the step 1 surfaces were not audited, the docs99 vocabulary form differs from the glossary, and the rule fit was text-level.
  - Choice: link to one canon and record the executed evidence.
  - Rejected alternatives: leave the reminders as they are, which breaks GOV-06; add a new governance rule for each reminder, which is an extra control with no new consumer.
  - Interface: the policy, skill, role and form text that agents read.
  - Failure: the validators refuse a broken link or a projection drift.
  - Acceptance: VAL-W01F-001 to VAL-W01F-003.

- **Allowed Paths**: `.agents/governance/agent-execution.md`, `.agents/skills/*/SKILL.md`, `AGENTS.md`, `.agents/workflows/work-lifecycle.md`, `.agents/workflows/delegated-development.md`, `.claude/provider.md`, `.agents/roles/incident-responder.md`, `.agents/roles/observability-reviewer.md`, projections under `.claude/agents/` and `.codex/agents/` only if their validator requires a regenerated copy, `docs/99.templates/registry.json` (the vocabulary Policy Owner meaning only), `docs/99.templates/templates/governance/vocabulary.template.md`, `docs/03.specs/0218-w01-followup/`, `docs/03.specs/README.md`, `docs/03.specs/0161-w00-v14-7-delta-intake/tasks/tsk-0001-w00-v14-7-delta-intake.md` (appended table and row, frontmatter `version` and `updated`), `.secrets.baseline` (reviewed entries only)
- **Forbidden Paths**: `_workspace/`, `scripts/`, `tests/`, `docs/03.specs/work-residue-ledger.json`, `.claude/settings.json`, `.codex/config.toml`
- **Approval Required**: Spec and Plan approval with an independent review; criterion acceptance
- **Static Validation**: governance, knowledge, four strict document, ledger and `document` contract-test checks; `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface in scope
- **Secret / Vault Handling**: no secret read or printed
- **Rollback Plan**: delete the branch `claude/w01-followup`; `main` is unchanged
- **Evidence Location**: this Task

## Execution Log

### Work Performed

Read-only survey and the background evidence run on 2026-11-15. No file outside this package is edited yet.

### Blockers and Decisions

Waiting for Spec and Plan approval after the independent review.

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-W01F-001](../spec.md#criteria) | One canon for the skill-authority, progress-ledger and intake rules and the provider and role links. | platform | draft | NOT_RUN | EVD-001 |
| WORK-002 | [VAL-W01F-002](../spec.md#criteria) | Vocabulary form to the link form. | platform | draft | NOT_RUN | EVD-002 |
| WORK-003 | [VAL-W01F-003](../spec.md#criteria) | Follow-up record in the SPEC-0161 Task. | platform | draft | NOT_RUN | EVD-003 |

## Verification Evidence

### Results

| Evidence ID | Consumer | Work Unit | Command | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-W01F-001](../spec.md#criteria) | WORK-001 | Governance, profile and link validators | Implementation snapshot | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-W01F-002](../spec.md#criteria) | WORK-002 | Contract registry, `document` contract tests and links validators | Implementation snapshot | NOT_RUN | Pending | yes | none |
| EVD-003 | [VAL-W01F-003](../spec.md#criteria) | WORK-003 | Ledger gate and strict document validators | Implementation snapshot | NOT_RUN | Pending | yes | none |

### Resolution Links

No earlier failure is open.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-W01F-001](../spec.md#criteria) | pending | none | Run WORK-001 after approval | platform |
| [VAL-W01F-002](../spec.md#criteria) | pending | none | Run WORK-002 after approval | platform |
| [VAL-W01F-003](../spec.md#criteria) | pending | none | Run WORK-003 after approval | platform |

### Remaining Conditions

Spec and Plan approval, the three work units and criterion acceptance remain.

## Handoff

### Promotion Receipt

The Plan promotes none.

### Next Owner

The independent reviewer and the user, for Spec and Plan review and approval; then platform.
