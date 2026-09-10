---
title: "Retire Dead Contracts and Duplicate Execution"
version: "0.1.0"
type: "sdlc/task"
status: "queued"
owner: "platform"
updated: "2026-09-11"
layer: "specs"
artifact_id: "SPEC-0077-TSK-0001"
---

# Task: Retire Dead Contracts and Duplicate Execution

## Overview

This Task owns the ordered execution of the eight approved packages, the
per-package focused evidence, the staged evidence for each logical commit, the
final full result, and the handoff record. It records observed results only and
never promotes a repository-static result to hosted, provider-runtime or live
evidence.

## Inputs

- [Spec](../spec.md) owns the approved contract, boundaries and criteria.
- [Plan](../plan.md) owns package order, ownership and rollback.
- Recorded baseline: `python3 scripts/qa.py full` at `EXIT=0`, 22 of 22 gates
  `PASS`, `snapshot=working-tree`, `paths=1126`, on `HEAD` `7d75e680`.
- Shared execution policy, approval boundary and quality policy under
  `.agents/governance/`.

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | VAL-DCR-001 | Retire the unreachable cross-document subtree and its single reaching test | platform | Queued | Not executed | Focused cross-document run and reference sweep |
| WORK-002 | VAL-DCR-002 | Add the collector-shape guard, remove never-collected classes, repair the empty ledger traversal | platform | Queued | Not executed | RED then GREEN on the guard and the traversal |
| WORK-003 | VAL-DCR-003 | Remove absent-subject cutover pins with their importing tests | platform | Queued | Not executed | Lifecycle gate result and importer sweep |
| WORK-004 | VAL-DCR-004 | Add the single-execution guard and remove pass-through assertions | platform | Queued | Not executed | RED then GREEN on the guard; `full` verdict unchanged |
| WORK-005 | VAL-DCR-005 | Resolve duplicated helpers to the shared bounded-input owner | platform | Queued | Not executed | Per-call-site focused tests and bounded-input tests |
| WORK-006 | VAL-DCR-006 | Consolidate the skill roster and admit the archive cutover skill | platform | Queued | Not executed | Governance gate, registry and projection validation |
| WORK-007 | VAL-DCR-007 | Close the routing, evaluation-root and unreachable-selector gaps | platform | Queued | Not executed | Contract validator and affected-surface tests |
| WORK-008 | VAL-DCR-008 | Record the link boundary rationale at its rule owner | platform | Queued | Not executed | Rule-owner review; boundary regressions unchanged |

## Approval and Safety Boundaries

- **Allowed Paths**: `scripts/`, `tests/`, `.agents/skills/`,
  `.agents/roles/registry.json`,
  `.agents/governance/document-authoring.md`, `.claude/skills/`,
  `.claude/agents/`, `.codex/agents/`,
  `docs/03.specs/0077-dead-contract-and-duplicate-execution-retirement/`,
  `docs/01.requirements/0003-workspace-agent-governance-platform.md`
  for reciprocal traceability only.
- **Forbidden Paths**: `docs/98.archive/`, `docs/99.templates/`,
  `gitops/`, `infrastructure/`, `policy/`, `secrets/`, `.github/workflows/`,
  and every other Stage 03 package.
- **Approval Required**: The request owner approved depth, the skill roster
  change, and withdrawal of the link boundary relaxation. Push, PR, merge and
  branch cleanup are not approved.
- **Static Validation**: focused `python3 -B -m unittest` per package, staged
  QA per logical commit, one `python3 scripts/qa.py full` on the final tree,
  and `git diff --check`.
- **Live Validation**: DEFER. No live cluster, provider runtime or network
  action is authorized by this Task.
- **Secret / Vault Handling**: No secret, credential or private configuration
  file is read or printed. Secret scanning stays with its existing gates.
- **Rollback Plan**: Each package is one commit that reverts alone; the
  recorded baseline commit is the restore point for the whole sequence.
- **Evidence Location**: This Task record.

## Verification Summary

Not executed. Per-package focused results, staged results per logical commit,
the final full result, limitations, review disposition, residual risk and next
owner are recorded here as work advances. Hosted results are recorded only
when observed for a named commit, and are otherwise DEFER.

## Traceability

Each work item below carries its observed result and durable evidence.

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-001](../plan.md#work-breakdown) | Not executed. | Pending focused cross-document evidence. |
| [WORK-002](../plan.md#work-breakdown) | Not executed. | Pending collector-shape and traversal evidence. |
| [WORK-003](../plan.md#work-breakdown) | Not executed. | Pending lifecycle gate evidence. |
| [WORK-004](../plan.md#work-breakdown) | Not executed. | Pending single-execution guard evidence. |
| [WORK-005](../plan.md#work-breakdown) | Not executed. | Pending shared-owner adoption evidence. |
| [WORK-006](../plan.md#work-breakdown) | Not executed. | Pending governance gate evidence. |
| [WORK-007](../plan.md#work-breakdown) | Not executed. | Pending routing and coverage evidence. |
| [WORK-008](../plan.md#work-breakdown) | Not executed. | Pending rule-owner review evidence. |
