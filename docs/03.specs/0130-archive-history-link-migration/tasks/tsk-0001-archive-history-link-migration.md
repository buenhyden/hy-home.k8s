---
title: "Archive History Link Migration"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-10-28"
layer: "specs"
artifact_id: "SPEC-0130-TSK-0001"
parent_ids: ["SPEC-0130-PLAN-0001"]
---

# Task: Archive History Link Migration

## Overview

Replace the history links to twelve retained Archive units with plain
identifiers and remove the twelve units as `git-history-only`. It executes
[SPEC-0130](../spec.md) through [WORK-001–004](../plan.md#work-breakdown).
This Task is the Decision document that the twelve Retention Assessment rows
name.

## Inputs

- Request: the operator chose Archive consumer migration on 2026-10-28.
- Approval: on 2026-10-28 the operator approved migrating and disposing of
  exactly these twelve units under `completed/03.specs/`, and no other:
  `0073-provider-native-enforcement-parity`,
  `0074-provider-write-guard-ownership-and-enforcement-honesty`,
  `0077-dead-contract-and-duplicate-execution-retirement`,
  `0078-document-currency-reconciliation`,
  `0079-six-disposition-archive-stage`,
  `0081-superseded-decision-retention`,
  `0088-operations-corpus-convergence`,
  `0089-deferred-conflict-resolution`, `0090-spec0049-retirement`,
  `0094-finished-package-retention`,
  `0100-archive-lifecycle-standardization` and
  `0101-closed-spec-retention`.
- Start: `26d3da3f`, branch `docs/archive-history-link-migration`.

### Retained Unit Census

Observed on main `3e922d51` by searching each unit's directory name and
identifier over tracked `.md`, `.json`, `.py`, `.yml`, `.yaml` and
`.toml` files outside Stage 98.

| Group | Units | Consumers | Disposition |
| --- | --- | --- | --- |
| History links only | 12 | REQ-0003, REQ-0004 and AD-0007 history sentences | This Task |
| Documents with evidence or identifier mentions | 11 | Provider notes naming an evidence owner, research, operations, examples and Stage 03 packages | Kept: evidence or meaning must move first |
| Registry, validators or tests | 18 | `registry.json`, `validate-links-and-owners.py` and lifecycle or archive tests | Kept: a validator or contract change is needed |
| Tests or scripts with documents | 16 | Archive, link-boundary and lifecycle tests, and the scripts that read them | Kept: a test or script change is needed |

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-AM-001](../spec.md#success-criteria--verification-plan) | Replace the history links with plain identifiers | platform | in-progress | PASS | EVD-005 closes EVD-001 |
| WORK-002 | [VAL-AM-002](../spec.md#success-criteria--verification-plan) | Isolated recovery of the twelve units | platform | in-progress | PASS | EVD-006 closes EVD-002 |
| WORK-003 | [VAL-AM-003](../spec.md#success-criteria--verification-plan) | Remove the twelve units and add their assessment rows | platform | ready | NOT_RUN | Pending named repository evidence |
| WORK-004 | [VAL-AM-004](../spec.md#success-criteria--verification-plan) | Independent review and hosted checks | platform | ready | NOT_RUN | Pending named repository evidence |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-AM-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Consumer path search | Exact revision | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-AM-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Isolated recovery | Exact revision | NOT_RUN | Pending | yes | none |
| EVD-003 | [VAL-AM-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Canonical staged QA | Exact disposition index | NOT_RUN | Pending | yes | none |
| EVD-004 | [VAL-AM-004](../spec.md#success-criteria--verification-plan) | WORK-004 | Review and hosted checks | Exact pull request head | NOT_RUN | Pending | yes | none |
| EVD-005 | [VAL-AM-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Consumer path search | Branch `docs/archive-history-link-migration`: `git grep` for each unit path outside Stage 98 after replacing 14 links in REQ-0003, 4 in REQ-0004 and 2 in AD-0007 | PASS | No current document links to the twelve units; only synthetic test fixture paths `0079-x`, `0090-x` and `0090-example` match. Each edited document names the Retention Catalog envelope as the recovery route | yes | EVD-001 |
| EVD-006 | [VAL-AM-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Isolated recovery | Base `21f68dde`: per unit, `git rev-parse` of the current tree against the envelope `<commit>:<original path>` tree, then `git archive` of the envelope into a scratch directory | PASS | 12/12 equal trees; restored 3 files per unit except 4 for `0079`, 37 in total, matching the current trees | yes | EVD-002 |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-AM-001](../spec.md#success-criteria--verification-plan) | pending | none | Link edits remain | platform |
| [VAL-AM-002](../spec.md#success-criteria--verification-plan) | pending | none | Recovery remains | platform |
| [VAL-AM-003](../spec.md#success-criteria--verification-plan) | pending | none | Removal remains | platform |
| [VAL-AM-004](../spec.md#success-criteria--verification-plan) | pending | none | Review and hosted checks remain | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: this package, the Stage 03 README index,
  `docs/01.requirements/0003-workspace-agent-governance-platform.md`,
  `docs/01.requirements/0004-current-local-gitops-platform.md`,
  `docs/02.architecture/descriptions/0007-current-local-gitops-platform.md`,
  the twelve unit directories and the Retention Assessment table in
  `docs/98.archive/README.md`.
- **Forbidden Paths**: every other Stage 98 payload, the frozen generation,
  catalog rows and envelopes, validators, the registry and completed Task
  facts.
- **Approval Required**: the twelve removals are approved (Inputs). Push,
  pull request and merge follow RUN-0013.
- **Static Validation**: `python3 scripts/qa.py staged` on each exact index.
- **Live Validation**: not applicable; no cluster or host state changes.
- **Secret / Vault Handling**: no secret-bearing content is read or printed.
- **Rollback Plan**: availability never returns to `retained` (ADR-0040).
  Content is recovered with `git archive <envelope commit> <original path>`;
  bringing it back is a new unit under a new decision. The link edits revert
  with the pull request.
- **Evidence Location**: this Task.

## Verification Summary

Not run yet.
