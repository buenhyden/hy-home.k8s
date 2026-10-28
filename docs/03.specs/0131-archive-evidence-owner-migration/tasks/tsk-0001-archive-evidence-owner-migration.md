---
title: "Archive Evidence Owner Migration"
version: "0.2.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-10-28"
layer: "specs"
artifact_id: "SPEC-0131-TSK-0001"
parent_ids: ["SPEC-0131-PLAN-0001"]
---

# Task: Archive Evidence Owner Migration

## Overview

Move the current-document consumers of ten retained Archive units to plain
identifiers and the Git recovery route, correct the sentences that say
removed Specs are kept in `98.archive/retired/`, and remove the ten units as
`git-history-only`. It executes [SPEC-0131](../spec.md) through
[WORK-001–004](../plan.md#work-breakdown). This Task is the Decision document
that the ten Retention Assessment rows name.

## Inputs

- Request: on 2026-10-28 the operator chose to draft the second Archive batch
  while PR #184 and PR #185 wait for their review checks.
- Approval: on 2026-10-28 the operator approved migrating and disposing of
  exactly these ten units, and no other:
  - `retired/03.specs/0049-platform-validation-and-security-evidence`
  - `retired/03.specs/0050-example-iac-and-validator-qa`
  - `completed/03.specs/0075-common-knowledge-and-prompt-surfaces`
  - `completed/03.specs/0076-agent-role-coverage-and-contract-completion`
  - `completed/03.specs/0083-finished-package-retention`
  - `completed/03.specs/0084-stage03-backlog-closeout`
  - `completed/03.specs/0086-provider-native-runtime-observation`
  - `completed/03.specs/0087-stage03-terminal-package-retention`
  - `completed/03.specs/0096-codex-model-tier-rebinding`
  - `completed/03.specs/0097-claude-model-and-effort-binding`
- Kept: SPEC-0104 stays `retained` as current REQ-0004 acceptance evidence.
- Start: `0d5d491e`, branch `docs/archive-evidence-owner-migration`.

### Consumer Map

Observed on `0d5d491e` by path and identifier search outside Stage 98.

| Unit | Consumers | Move |
| --- | --- | --- |
| SPEC-0049 | REQ-0003, REQ-0004 and AD-0007 say it is kept in `retired/` | Say it was withdrawn and left the tree |
| SPEC-0050 | REQ-0003, REQ-0004 and AD-0007 say it is kept in `retired/`; AWS and Azure example READMEs mention it | Same correction; the example mentions stay as history |
| SPEC-0075 | REQ-0003 and ADR-0036 links; m0009 cites a head its Task recorded | Plain identifier; m0009 names the recovery route |
| SPEC-0076 | REQ-0003 and m0009 links; m0009 refresh trigger | Plain identifier; the trigger stays as written |
| SPEC-0083, SPEC-0084 | REQ-0003 and architecture-description README links; AD-0006 history sentence | Plain identifier |
| SPEC-0086 | REQ-0003 link; `.claude/provider.md` and `.codex/provider.md` name its Task as evidence owner | The notes keep each fact and say the Task recorded it |
| SPEC-0087 | REQ-0003, REQ-0004 and AD-0007 links; operations guide 0010 and runbook 0011 history mentions | Plain identifier |
| SPEC-0096 | REQ-0003 link; `.codex/provider.md` names its Task as evidence owner | As for SPEC-0086 |
| SPEC-0097 | REQ-0003 link; `.claude/provider.md` names it with the retained SPEC-0098 Task | SPEC-0098 keeps ownership |

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-EO-001](../spec.md#success-criteria--verification-plan) | Move the consumers to identifiers and the recovery route | platform | completed | PASS | EVD-005 closes EVD-001 |
| WORK-002 | [VAL-EO-002](../spec.md#success-criteria--verification-plan) | Isolated recovery of the ten units | platform | completed | PASS | EVD-006 closes EVD-002 |
| WORK-003 | [VAL-EO-003](../spec.md#success-criteria--verification-plan) | Remove the ten units and add their assessment rows | platform | completed | PASS | EVD-007 closes EVD-003 |
| WORK-004 | [VAL-EO-004](../spec.md#success-criteria--verification-plan) | Independent review and hosted checks | platform | completed | PASS | EVD-008 closes EVD-004 |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-EO-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Consumer search | Exact revision | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-EO-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Isolated recovery | Exact revision | NOT_RUN | Pending | yes | none |
| EVD-003 | [VAL-EO-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Canonical staged QA | Exact disposition index | NOT_RUN | Pending | yes | none |
| EVD-004 | [VAL-EO-004](../spec.md#success-criteria--verification-plan) | WORK-004 | Review and hosted checks | Exact pull request head | NOT_RUN | Pending | yes | none |
| EVD-005 | [VAL-EO-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Consumer search | Branch `docs/archive-evidence-owner-migration`: `git grep` for each unit path, for `SPEC-#### Task(s) own` and for `kept in \`98.archive/retired/\`` outside Stage 98 and this package, after the edits to REQ-0003, REQ-0004, AD-0007, the architecture-description README, ADR-0036, m0009 and both provider notes | PASS | No current document links to the ten units or names their Tasks as owners; each provider note keeps its observed facts and says the Task recorded them; no sentence says a removed Spec is kept in `retired/`. Plain mentions remain in AD-0006, the example READMEs, operations guide 0010 and runbook 0011 | yes | EVD-001 |
| EVD-006 | [VAL-EO-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Isolated recovery | Base `44e654dd`: per unit, `git rev-parse` of the current tree against the envelope tree, then `git archive` of the envelope into a scratch directory | PASS | 10/10 equal trees; restored 9, 9, 3, 3, 3, 3, 3, 3, 3 and 3 files, 42 in total, matching the current trees | yes | EVD-002 |
| EVD-007 | [VAL-EO-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Canonical staged QA | Commit `f5a46cfc`, committed from a worktree without `graphify-out/`, CI-lock environment first on `PATH` | PASS | The pre-commit `Validate Staged QA Snapshot`, `commitizen check` and generated-message hooks passed in 402 seconds; the ten units are absent, 42 files removed, and their ten rows validate | yes | EVD-003 |
| EVD-008 | [VAL-EO-004](../spec.md#success-criteria--verification-plan) | WORK-004 | Review and hosted checks | PR #186 independent review of `f5a46cfc` and re-review of `8d13c5bf`; heads `f5a46cfc` (CI run `40604469510`) and `8d13c5bf` (CI run `40605551303`) | PASS | The reviewer re-verified all ten envelope trees and the provider-note facts and approved. Two low findings were fixed in `8d13c5bf` and approved on re-review: the SPEC-0049 retention sentence is now history, and the Spec scope names the documents that were checked and left unchanged. `ci-summary`, `style-pr`, `label` and GitGuardian passed on both heads | yes | EVD-004 |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-EO-001](../spec.md#success-criteria--verification-plan) | accepted | EVD-005 | Accepted by the operator on 2026-10-28: no current document links to the ten units or names their Tasks as owners, and every stated fact is kept | platform |
| [VAL-EO-002](../spec.md#success-criteria--verification-plan) | accepted | EVD-006 | Accepted by the operator on 2026-10-28: all ten envelope trees equal the removed trees and restore 42 files | platform |
| [VAL-EO-003](../spec.md#success-criteria--verification-plan) | accepted | EVD-007 | Accepted by the operator on 2026-10-28: the ten units left the tree with valid `git-history-only` rows and staged QA passed | platform |
| [VAL-EO-004](../spec.md#success-criteria--verification-plan) | accepted | EVD-008 | Accepted by the operator on 2026-10-28: the independent review approved and the hosted checks passed | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: this package, the Stage 03 README index, REQ-0003,
  REQ-0004, AD-0006, AD-0007, the architecture-description README, ADR-0036,
  research note m0009,
  `.claude/provider.md`, `.codex/provider.md`, the ten unit directories and
  the Retention Assessment table in `docs/98.archive/README.md`.
- **Forbidden Paths**: every other Stage 98 payload, the frozen generation,
  catalog rows and envelopes, validators, the registry, provider settings and
  bindings, and completed Task facts.
- **Approval Required**: the ten removals are approved (Inputs). Push, pull
  request and merge follow RUN-0013 after PR #184 and PR #185 merge.
- **Static Validation**: `python3 scripts/qa.py staged` on each exact index.
- **Live Validation**: not applicable; no cluster or host state changes.
- **Secret / Vault Handling**: no secret-bearing content is read or printed.
- **Rollback Plan**: availability never returns to `retained` (ADR-0040).
  Content is recovered with `git archive <envelope commit> <original path>`;
  bringing it back is a new unit under a new decision. The consumer edits
  revert with the pull request.
- **Evidence Location**: this Task.
- **Acceptance**: on 2026-10-28 the operator accepted VAL-EO-001 to
  VAL-EO-004.

## Verification Summary

WORK-001 passed (EVD-005): the consumers name the ten packages as plain
identifiers with a recovery route, the provider notes keep their facts, and
no sentence says a removed Spec is kept in `retired/`. WORK-002 passed
(EVD-006). WORK-003 passed (EVD-007): commit `f5a46cfc` removed the ten units.
WORK-004 passed (EVD-008). The operator accepted all four criteria.
Residual items: the m0009 refresh trigger still names SPEC-0076, and retained
Archive payloads such as SPEC-0098 keep historical links to removed units.
SPEC-0104 and the 34 units with registry, validator or test consumers stay
`retained`.
