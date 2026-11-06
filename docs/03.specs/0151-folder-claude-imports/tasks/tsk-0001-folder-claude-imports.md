---
title: "Folder CLAUDE.md Imports"
version: "0.2.0"
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
[WORK-001–004](../plan.md#work-breakdown).

## Inputs

- Request (2026-11-06): review the folder `CLAUDE.md` with `@AGENTS.md`
  approach and proceed.
- Review (2026-11-06): native nested loading covers reads and compaction
  reloads, which the SPEC-0149 hook path does not.
- Approval (2026-11-06): the operator's request to review the folder `CLAUDE.md` approach and proceed approves SPEC-0151 and its Plan, drafted in `a8b2e941`; merge is separate and criterion acceptance stays the operator's.
- Scope change (2026-11-06): the operator chose to add a Claude `SessionStart`
  hook on `compact|resume`; the Spec and Plan returned to `in-review` in `c9a45252` and the operator's choice re-approves them; the operator then asked for a per-edit path line, reviewed in `3432d0d9` and re-approved by that request.
- Start: branch `feat/folder-claude-imports` from `main` at `8be06a16`.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-CLI-001](../spec.md#success-criteria--verification-plan) | Pairing check and Codex-only folder chain | platform | completed | PASS | EVD-006 |
| WORK-002 | [VAL-CLI-002](../spec.md#success-criteria--verification-plan) | Files, profile and documentation | platform | completed | PASS | EVD-007 |
| WORK-003 | [VAL-CLI-003](../spec.md#success-criteria--verification-plan) | Observed read-only Claude session | platform | completed | PASS | EVD-008, EVD-011 |
| WORK-004 | [VAL-CLI-004](../spec.md#success-criteria--verification-plan) | Session-start hook, per-provider event rule and per-edit path line | platform | completed | PASS | EVD-009, EVD-012 |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-CLI-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Focused tests red then green | Pending Spec approval | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-CLI-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Strict checks and staged QA | Pending Spec approval | NOT_RUN | Pending | yes | none |
| EVD-003 | [VAL-CLI-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Observed read-only Claude session | Pending Spec approval | NOT_RUN | Pending | yes | none |
| EVD-004 | [VAL-CLI-004](../spec.md#success-criteria--verification-plan) | WORK-004 | Focused tests red then green | Pending Spec approval | NOT_RUN | Pending | yes | none |
| EVD-005 | [VAL-CLI-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Focused tests red then green | Working tree on `28eb59d7` (after `e665bc1f`) with the new tests and the old code | FAIL | Local run, 2026-11-06T09:24Z: `tests.test_repository_quality_rules` setUpClass error (`folder_claude_import_gaps` missing) and `tests.test_agent_governance` errors (`.claude/hooks/session-start.sh` missing) | no | none |
| EVD-006 | [VAL-CLI-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Focused tests red then green | Working tree on `28eb59d7` (after `e665bc1f`) with the change | PASS | Local run, 2026-11-06T09:25Z to 09:30Z: hook, quality-rule, agent-governance, reference-pack and tooling-ownership suites OK; Claude gets the path line on every edit and no folder text, Codex gets the text once per session | yes | EVD-001 |
| EVD-007 | [VAL-CLI-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Strict checks and staged QA | Staged index on `28eb59d7` with 15 folder `CLAUDE.md` files, the profile and the documentation | PASS | Local run, 2026-11-06T09:30Z: strict contract-registry, profile, link and lifecycle PASS after the consumers that enumerate folder entries were updated (Stage 90 root entry allowlist, infrastructure coverage matrix row, the `folder-agents-guides` surface route and two route exclusions in `scripts/validation/registry.json`, the Stage 01 and 03 filename allowlists in `quality.py`, and the seven `docs/` stage README indexes); full `python3 scripts/qa.py staged` exit 0 with only the existing live `platform-assurance-depth` DEFER rows; `test_document*` OK; `validate-agent-governance.py` PASS | yes | EVD-002 |
| EVD-008 | [VAL-CLI-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Observed read-only Claude session | `claude -p --model haiku --allowedTools Read`, Claude Code 2.1.319, working tree with the 15 files | PASS | 2026-11-06T09:26Z: before any tool the session reported the `docs/05.operations/AGENTS.md` sentence absent; after one Read of `docs/05.operations/README.md` it reported `docs/CLAUDE.md`, `docs/AGENTS.md`, `docs/05.operations/CLAUDE.md` and `docs/05.operations/AGENTS.md` loaded and quoted line 3 of that `AGENTS.md`, which the README does not contain; this session also loaded `scripts/` and `infrastructure/` imports with full text on access | yes | EVD-003 |
| EVD-009 | [VAL-CLI-004](../spec.md#success-criteria--verification-plan) | WORK-004 | Focused tests red then green | Working tree on `28eb59d7` (after `e665bc1f`) with the change | PASS | Local run, 2026-11-06T09:25Z: `test_session_start_is_claude_only_and_compact_or_resume`, `test_session_start_hook_reinjects_the_reading_instruction` and `test_claude_gets_the_path_line_on_every_edit_and_no_text` OK; a Codex `SessionStart` and a Claude `startup` matcher are refused | yes | EVD-004 |
| EVD-010 | [VAL-CLI-004](../spec.md#success-criteria--verification-plan) | WORK-004 | Focused tests red then green | Working tree on `28eb59d7` (after `e665bc1f`) with the new tests and the old code | FAIL | Local run, 2026-11-06T09:24Z: the session-start and per-edit path tests fail before `.claude/hooks/session-start.sh` and the path line exist (same run as EVD-005) | no | none |
| EVD-011 | [VAL-CLI-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Observed read-only Claude session | `claude -p --model haiku --allowedTools Write`, Claude Code 2.1.319, Write-first with no prior Read | PASS | 2026-11-06T09:46Z: a first run's Write was blocked by the user-level GateGuard hook, so no folder file loaded and only the guard's path line arrived; a second run retried after the GateGuard facts and, after the successful Write of the ignored `tests/__pycache__/agents-md-probe.txt`, reported `tests/CLAUDE.md` and `tests/AGENTS.md` loaded and quoted line 3 of `tests/AGENTS.md`; the folder text arrives with the tool result, after the write | yes | none |
| EVD-012 | [VAL-CLI-004](../spec.md#success-criteria--verification-plan) | WORK-004 | Focused tests red then green | Working tree on `28eb59d7` after the review fixes | PASS | Local run, 2026-11-06: the review found one BLOCK (Write-first unobserved, closed by EVD-011) and advisories; the validator now pins the SessionStart command to `.claude/hooks/session-start.sh`, the path-line test covers Edit and Write, and the compaction reload is stated as documented and unobserved; suites OK | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-CLI-001](../spec.md#success-criteria--verification-plan) | accepted | EVD-006 | Operator accepted on 2026-11-06 after review | platform |
| [VAL-CLI-002](../spec.md#success-criteria--verification-plan) | accepted | EVD-007 | Operator accepted on 2026-11-06 after review | platform |
| [VAL-CLI-003](../spec.md#success-criteria--verification-plan) | accepted | EVD-008, EVD-011 | Operator accepted on 2026-11-06 after review | platform |
| [VAL-CLI-004](../spec.md#success-criteria--verification-plan) | accepted | EVD-009, EVD-012 | Operator accepted on 2026-11-06 after review | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: the 15 folder `CLAUDE.md` files beside folder
  `AGENTS.md` files, `docs/99.templates/registry.json`, `.secrets.baseline`,
  `scripts/validation/repository/quality.py`, `scripts/provider_write_guard.py`,
  `scripts/validate-document-contract-registry.py` (Stage 90 root entry),
  `infrastructure/README.md` (coverage matrix row),
  `tests/test_repository_quality_rules.py`, `tests/test_k8s_pre_edit_hook.py`,
  `.claude/provider.md`, `.codex/provider.md`, `.claude/settings.json`
  (`SessionStart` only), `.claude/hooks/session-start.sh`,
  `scripts/validate-agent-governance.py`, `tests/test_agent_governance.py`,
  `.agents/governance/agent-execution.md`, `docs/03.specs/`,
  `docs/01.requirements/0003-workspace-agent-governance-platform.md`,
  `docs/90.references/audits/0001-sdlc-governance/m0002-agents-md-loading-addendum.md`
- **Forbidden Paths**: root `CLAUDE.md` and `AGENTS.md`, `.claude/CLAUDE.md`,
  `.codex/hooks.json`, `docs/98.archive/`, `secrets/`
- **Approval Required**: Spec and Plan approval by the operator; merge is
  separate
- **Static Validation**: the Spec's Verification Commands
- **Live Validation**: provider-runtime only: a new Claude session
- **Secret / Vault Handling**: none
- **Rollback Plan**: revert the implementing commits
- **Evidence Location**: this Task

## Verification Summary

- Tests: red on the old code (EVD-005), green after (EVD-006, EVD-009).
- Static: strict checks and suites PASS; two consumers updated (EVD-007).
- Claude runtime: new sessions loaded folder `CLAUDE.md` imports with the
  `AGENTS.md` text after a Read (EVD-008) and after a Write-first (EVD-011);
  this session loaded them on access too. A write blocked by another hook
  loads nothing, but the guard's path line still arrives.
- Not run: the session-start hook in a real compaction or resume, which
  needs a later session; Codex delivery stays DEFER.
- Residual risk: whether an `AGENTS.md` edited mid-session is reloaded is
  undocumented; the shell heuristic can name a folder's rules for a command
  that only runs a script there.
- Acceptance: the operator accepted VAL-CLI-001 to 004 on 2026-11-06.
- Next owner: operator, for merge and a later compaction observation. Rollback: revert
  the implementing commits.
