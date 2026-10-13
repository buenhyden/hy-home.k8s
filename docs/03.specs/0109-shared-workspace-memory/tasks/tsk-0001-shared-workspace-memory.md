---
title: "Shared Workspace Memory Store"
version: "1.0.0"
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
| WORK-001 | [VAL-MEMORY-001](../spec.md#success-criteria--verification-plan) | Store module, CLI and Git ignore entry | platform | completed | PASS | EVD-005, EVD-008 in commit `9b4bd50043fea1f6575bcd9c553b04e341a77c0c` |
| WORK-002 | [VAL-MEMORY-002](../spec.md#success-criteria--verification-plan) | Native memory disablement and validation | platform | blocked | DEFER | EVD-006 in commit `8586346f445394fe2c7f1043c1569b13a3b62c35`. Reason: VAL-MEMORY-002 needs two real provider sessions reading the same memory and showing no native memory write. Next owner: operator, to run the observation commands in the Verification Summary |
| WORK-003 | [VAL-MEMORY-001](../spec.md#success-criteria--verification-plan) | Memory policy and requirement revision | platform | completed | PASS | EVD-007 in commit `aeafdebbb0b004807809d00931150fa3dd284e58` |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-MEMORY-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Store tests and staged QA | WORK-001 commit index | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-MEMORY-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Native settings tests and staged QA | WORK-002 commit index | NOT_RUN | Pending | yes | none |
| EVD-003 | [VAL-MEMORY-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Cross-provider session observation | Two real provider sessions in two worktrees | NOT_RUN | Pending | yes | none |
| EVD-004 | [VAL-MEMORY-001](../spec.md#success-criteria--verification-plan) | WORK-003 | Policy validators and staged QA | WORK-003 commit index | NOT_RUN | Pending | yes | none |
| EVD-005 | [VAL-MEMORY-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Store tests and staged QA | `tests.test_workspace_memory` failed to import before the module existed, then 11 tests passed: implicit-creation refusal, linked-worktree identity, tier schema and Task-state rejection, revision conflict retention, four concurrent writers with one winner, idempotent retry, capacity refusal without loss, stale-source exclusion with history kept, no delete API, verified backup kept on replacement failure, rollback journal and CLI round trip. `qa.py staged` from the validation environment passed all 12 selected gates. Local SQLite 3.45.1 | PASS | This Task; commit `9b4bd50043fea1f6575bcd9c553b04e341a77c0c` | yes | EVD-001 |
| EVD-006 | [VAL-MEMORY-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Native settings tests and staged QA | `tests.test_agent_governance` errored on the absent `.codex/config.toml` fixture before repair, then 59 tests passed, including rejection of a missing, true, null, zero or string `autoMemoryEnabled` and of a Codex config that is missing, enables memories, or adds `[hooks]` or another key. `qa.py staged` passed all 10 selected gates. This is repository-static evidence; client behavior is not observed | PASS | This Task; commit `8586346f445394fe2c7f1043c1569b13a3b62c35` | yes | EVD-002 |
| EVD-007 | [VAL-MEMORY-001](../spec.md#success-criteria--verification-plan) | WORK-003 | Policy validators and staged QA | First staged run failed `links-and-owners` on a README deep link and a policy-to-Spec link; both were replaced by stage-index routing and the rerun passed all 9 selected gates, including knowledge surface and document lifecycle | PASS | This Task; commit `aeafdebbb0b004807809d00931150fa3dd284e58` | yes | EVD-004 |
| EVD-008 | [VAL-MEMORY-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Real store smoke check | `scripts/workspace_memory.py init` created the Git-ignored store at the main root with workspace ID `83ced050-f616-4b01-8a20-e3e61c9acea9`; a long-term memory written from the main worktree was read back with the same ID, revision and body from a temporary linked worktree, then marked current. One process and one provider only, so it does not satisfy VAL-MEMORY-002 | PASS | `.workspace-memory/memory.sqlite3` (ignored runtime data) | no | none |
| EVD-009 | [VAL-MEMORY-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Codex session read observation | Operator-relayed output on 2026-10-13 from a Codex session running `resolve` and `get mem-e71dedf07add48d5`: same store path, workspace ID `83ced050-f616-4b01-8a20-e3e61c9acea9`, revision 1, body and source hash as the Claude-side read. The Codex worktree, session freshness and project trust were not stated, no new Claude session was observed, and native memory non-write was not checked | PASS | This Task (operator-relayed transcript) | no | none |
| EVD-010 | [VAL-MEMORY-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Claude session read observation | Operator-relayed output on 2026-10-13 from a new Claude Code session started after `autoMemoryEnabled: false` was committed: `resolve` and `get mem-e71dedf07add48d5` returned the same store path, workspace ID, revision 1, body and unchanged source as EVD-009. The project native memory directory files were last modified at 11:51 KST, before that session (about 14:23 KST), so it wrote no native memory. Both sessions resolved the main root; the worktree each ran from was not stated | PASS | This Task (operator-relayed transcript; file times observed 14:24 KST) | no | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-MEMORY-001](../spec.md#success-criteria--verification-plan) | accepted | EVD-005, EVD-007 | Accept the store, its limits and the policy on focused local evidence; the area limit is observed only | platform |
| [VAL-MEMORY-002](../spec.md#success-criteria--verification-plan) | pending | EVD-006, EVD-009, EVD-010 | Both providers read the same memory (EVD-009, EVD-010) and Claude wrote no native memory; still open: one session from a linked worktree and Codex native memory non-write | operator |

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
  implementation on 2026-10-13, and the Plan the same day; push, pull request and merge await the
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

WORK-001 and WORK-003 are complete and VAL-MEMORY-001 is accepted. WORK-002
is committed but blocked on its acceptance observation, so this Task stays
blocked rather than completed. Every commit passed `qa.py staged` from the
documented validation environment.

To close VAL-MEMORY-002, start a new Claude session and a new trusted Codex
session in two different worktrees of this repository and in each run
`python3 scripts/workspace_memory.py resolve` and
`python3 scripts/workspace_memory.py get mem-e71dedf07add48d5`; the
workspace ID, revision and body must match. Then confirm that neither
session wrote native memory (no new Claude project memory entry, no Codex
memory generation). Record the clients, worktrees and results here.

Limitations: the 4 GiB area limit is observed, not enforced; hosted CI,
push and pull request are not executed. Next owner: the operator for the
observation, SPEC-0109 Plan approval, push and pull request.
