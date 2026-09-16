---
title: "Retire Dead Contracts and Duplicate Execution"
version: "0.2.1"
type: "sdlc/task"
status: "done"
owner: "platform"
updated: "2026-09-14"
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

**Closure (2026-09-16).** Six of eight work items are executed with commit evidence, WORK-005 in this round. WORK-006 and WORK-007 stay unfinished on authority the request owner did not grant here: retiring the two remaining skills needs a new sealed migration, and routing `evals` needs a Stage 99 route first. Both are recorded above as deferrals with named owners rather than claimed, which is the pattern SPEC-0073 and SPEC-0076 used to close. This change takes the declared `in-progress` to `done` edge under [SPEC-0084](../../0084-stage03-backlog-closeout/spec.md).

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
| WORK-001 | VAL-DCR-001 | Retire the unreachable cross-document subtree and its single reaching test | platform | Done | Unreachable validation symbols removed in four commits; every registered Python validator output byte-identical | `8c043fda`, `f8f92d42`, `4d349c2c`; staged QA PASS per commit |
| WORK-002 | VAL-DCR-002 | Add the collector-shape guard, remove never-collected classes, repair the empty ledger traversal | platform | Done | Guard RED on two classes, then GREEN; traversal iterates the sealed ledgers | `e09acd85`; staged QA PASS |
| WORK-003 | VAL-DCR-003 | Remove absent-subject cutover pins with their importing tests | platform | Done | Rehome and normalization admissions and WP-004A pins removed; lifecycle output unchanged | `c9cd53b7`; staged QA PASS |
| WORK-004 | VAL-DCR-004 | Add the single-execution guard and remove pass-through assertions | platform | Done | Guard RED on four re-executions, then GREEN | `bcf28058`; staged QA PASS |
| WORK-005 | VAL-DCR-005 | Resolve duplicated helpers to the shared bounded-input owner | platform | Done | Two of the seven frontmatter helpers were true duplicates and resolved to the public owner; the other five differ in their failure contract and were left apart | `fade5b9b`; validator stdout byte-identical at `e1925925356b`, 87 archive contract tests and 182 dependent tests pass |
| WORK-006 | VAL-DCR-006 | Consolidate the skill roster and admit the archive cutover skill | platform | Partial | Archive cutover skill admitted; unpractised marker removed; two merges deferred on authority | `c200cf4f`; staged QA PASS |
| WORK-007 | VAL-DCR-007 | Close the routing, evaluation-root and unreachable-selector gaps | platform | Deferred | Evaluation-root change blocked on authority; no unreachable selector proven | Read-only probe recorded below |
| WORK-008 | VAL-DCR-008 | Record the link boundary rationale at its rule owner | platform | Done | Rationale added; boundary regressions unchanged | `33e77550`; staged QA PASS |

## Approval and Safety Boundaries

- **Allowed Paths**: `scripts/`, `tests/`, `.agents/skills/`,
  `.agents/roles/registry.json`,
  `.agents/governance/document-authoring.md`, `.claude/skills/`,
  `.claude/agents/`, `.codex/agents/`,
  `docs/03.specs/0077-dead-contract-and-duplicate-execution-retirement/`,
  `docs/01.requirements/0003-workspace-agent-governance-platform.md`
  for reciprocal traceability only, and the `docs/03.specs/README.md` status
  cell for this package.
- **Forbidden Paths**: `docs/98.archive/`, `docs/99.templates/`,
  `gitops/`, `infrastructure/`, `policy/`, `secrets/`, `.github/workflows/`,
  and every other Stage 03 package.
- **Approval Required**: The request owner approved depth, the skill roster
  change, withdrawal of the link boundary relaxation, remediation of separate
  defects found during the work, and push, merge and branch cleanup after
  completion. Authoring a sealed Stage 98 record or a Stage 99 route is not
  approved.
- **Static Validation**: focused `python3 -m unittest` per package, staged QA
  per logical commit, one `python3 scripts/qa.py full` on the final tree, and
  `git diff --check`.
- **Live Validation**: DEFER. No live cluster, provider runtime or network
  action is authorized by this Task.
- **Secret / Vault Handling**: No secret, credential or private configuration
  file is read or printed. Secret scanning stays with its existing gates.
- **Rollback Plan**: Each package is one commit that reverts alone; the
  recorded baseline commit is the restore point for the whole sequence.
- **Evidence Location**: This Task record.

## Verification Summary

Every removal was checked by capturing the output and exit code of each
registered Python validator before the change and comparing the bytes after
it. All fifteen matched in every comparison, except that `agent-governance`
labels a dirty working tree `working-tree snapshot` instead of
`current indexed tree`, which is a snapshot label and not a verdict.

Focused results: the modules importing the edited library validators ran 619
tests OK; the modules loading the edited command-line validators ran 439 OK;
the lifecycle validator's importers ran 161 OK; the single-execution modules
ran 164 OK. Each logical commit passed `python3 scripts/qa.py staged` over its
exact index.

The final `python3 scripts/qa.py full` runs once on the tree that contains this
record, so its verdict cannot be written into it; the handoff for the merge
records it. Hosted CI is recorded only for a named observed commit and is
otherwise DEFER.

Deferred on authority:

- The WORK-006 merges of `task-breakdown` into `execution-plan` and of
  `k8s-security-audit` into `vulnerability-patterns`. Sealed `MIG-0021` names
  both retired skill paths as live successors, so deleting them fails the
  generic migration recovery proof. Retiring them needs a new sealed Stage 98
  migration, which this Task forbids. Next owner: the request owner decides
  whether to authorize that migration.
- The WORK-007 evaluation root. Adding `evals` to the document target roots
  makes nineteen synthetic response fixtures under `evals/responses/`
  unrouted, so it needs a Stage 99 route first, which this Task forbids. Next
  owner: the Stage 99 registry owner.

Executed on 2026-09-16 under
[SPEC-0084](../../0084-stage03-backlog-closeout/spec.md): WORK-005, narrower than
the item proposed. Reading all seven frontmatter helpers showed that only two were
duplicates, `archive_dispositions.frontmatter_mapping` and the private copy in
`scripts/validate-links-and-owners.py`, with the same body and the same result.
The private copy is gone and its one call site uses the public owner. The other
five were left apart on purpose: they differ in what they do when parsing fails,
one emitting a diagnostic and stopping, one raising, and three returning
defaults, so merging them would move each gate's failure contract rather than
remove duplication. Two helpers in that group even share the name
`_frontmatter` while returning different shapes.

Residual risk, unchanged: duplication among the link, process and mapping
helpers, which this round did not examine. Next owner: a follow-up Task.

Not proven dead and therefore kept: the `ci` selector lane. The hosted workflow
calls `qa.py ci`, which maps it to the all-files lane.

## Traceability

Each work item below carries its observed result and durable evidence.

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-001](../plan.md#work-breakdown) | Done. | Byte-identical validator outputs; commits `8c043fda`, `f8f92d42`, `4d349c2c`. |
| [WORK-002](../plan.md#work-breakdown) | Done. | Collector guard RED then GREEN; commit `e09acd85`. |
| [WORK-003](../plan.md#work-breakdown) | Done. | Lifecycle output unchanged; commit `c9cd53b7`. |
| [WORK-004](../plan.md#work-breakdown) | Done. | Single-execution guard RED on four, then GREEN; commit `bcf28058`. |
| [WORK-005](../plan.md#work-breakdown) | Done; narrower than proposed. | Byte-identical validator output `e1925925356b`; commit `fade5b9b`. |
| [WORK-006](../plan.md#work-breakdown) | Partial; merges deferred on authority. | Governance gate PASS with seventeen skills; commit `c200cf4f`. |
| [WORK-007](../plan.md#work-breakdown) | Deferred on authority. | Route probe: nineteen unrouted fixtures under `evals/responses/`. |
| [WORK-008](../plan.md#work-breakdown) | Done. | Boundary regressions unchanged; commit `33e77550`. |
