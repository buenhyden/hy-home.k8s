---
title: "State the Six-Disposition Contract"
version: "0.1.0"
type: "sdlc/task"
status: "queued"
owner: "platform"
updated: "2026-09-15"
layer: "specs"
artifact_id: "SPEC-0079-TSK-0001"
---

# Task: State the Six-Disposition Contract

## Overview

This Task owns the governance step of Spec 0079: the proposed decision, the
contract in common governance and the documentation hub, the Stage 98 index
prose, the aligned stage indexes, and the enumeration of pending dispositions
and pre-acceptance consumers. It records observed results only and never
promotes a repository-static result to hosted, provider-runtime, or live
evidence.

## Inputs

- [Spec](../spec.md) owns the contract, boundaries, and criteria, and
  [Plan](../plan.md) owns order and risk.
- On 2026-09-15 the request owner supplied the six-disposition model and
  decided: frozen Stage 98 content keeps its generation and the model applies
  forward; the decision-log exception for superseded decisions is withdrawn;
  governance goes first and the registry moves with the validators; the
  citation rule applies forward; the Retention Envelope names one
  `<commit>:<original path>`.
- Snapshot: branch `claude/stage98-six-disposition-archive` from `main` at
  `c652331c`.

## Task Table

| ID       | Upstream criterion | Work item                                                                                   | Owner    | Status | Result                                                                                                 | Evidence                   |
| -------- | ------------------ | ------------------------------------------------------------------------------------------- | -------- | ------ | ------------------------------------------------------------------------------------------------------ | -------------------------- |
| WORK-001 | VAL-SDA-001        | Record ADR-0038, ADR-0032's dated successor note, and the decision index row                | platform | Done   | ADR-0038 created as proposed; ADR-0032 stays accepted                                                  | Working tree; strict gates |
| WORK-002 | VAL-SDA-002        | State the contract in the lifecycle, authoring, and SDLC policies and the documentation hub | platform | Done   | Six dispositions, derived citation, one Retention Envelope, and the transition boundary stated         | Working tree; strict gates |
| WORK-003 | VAL-SDA-003        | Rewrite the Stage 98 index prose                                                            | platform | Done   | Two kinds, catalog envelope, and frozen generation stated; manifest comment and record table unchanged | Working tree; archive gate |
| WORK-004 | VAL-SDA-004        | Align the Stage 01, 02, and 03 indexes, AD-0006, and REQ-0003-FR-0020                       | platform | Done   | ADR-0032's four directories and the decision-log exception no longer restated as the target            | Working tree; strict gates |
| WORK-006 | VAL-SDA-006        | Enumerate pending dispositions and pre-acceptance consumers                                 | platform | Done   | Recorded below with owners                                                                             | This record                |

## Approval and Safety Boundaries

- **Allowed Paths**: `.agents/governance/document-lifecycle.md`,
  `.agents/governance/document-authoring.md`, `.agents/governance/sdlc.md`,
  `docs/README.md`, the prose of `docs/98.archive/README.md` outside its manifest
  comment and record table, `docs/01.requirements/README.md`,
  `docs/01.requirements/0003-workspace-agent-governance-platform.md`,
  `docs/02.architecture/README.md`, `docs/02.architecture/decisions/`,
  `docs/02.architecture/descriptions/README.md`, `.agents/roles/README.md`,
  `docs/02.architecture/descriptions/0006-workspace-agent-governance-platform.md`,
  `docs/03.specs/README.md`, and this package.
- **Forbidden Paths**: frozen records, ledgers, and retained packages under
  `docs/98.archive/`, `docs/99.templates/`, `.markdownlint-cli2.yaml`,
  `scripts/`, `tests/`, `gitops/`, `infrastructure/`, `policy/`, `secrets/`,
  `.github/`.
- **Approval Required**: The request owner approved the model and the decisions
  above. Commit, push, pull request, merge, ADR-0038 acceptance, and executing
  any disposition were not requested and are not approved.
- **Static Validation**: the strict profile, link, lifecycle, and archive gates
  and one `python3 scripts/qa.py full` on the final tree, with
  `git diff --check`.
- **Live Validation**: DEFER. No live cluster, provider runtime, or network
  action is authorized.
- **Secret / Vault Handling**: No secret, credential, or private configuration
  file is read or printed.
- **Rollback Plan**: Discard the uncommitted working-tree changes on this
  branch, or revert the commit once one exists.
- **Evidence Location**: This Task record.

## Verification Summary

Baseline: `python3 scripts/qa.py full` returned `EXIT=0` with 22 of 22 gates
`PASS` on the tree of `c652331c`. Final: `python3 scripts/qa.py full` returned
`EXIT=0` with 22 of 22 gates `PASS` on this branch's final working tree, before
this summary was written; `git diff --check` was clean, and `python3
scripts/qa.py quick` passed 7 of 7 gates after each repair and after this
Task-only summary. Staged QA and commit-message evidence are N/A because no
commit was requested.

Repairs during the work: `BODY-LINK-RECIPROCAL` required REQ-0003 to name
SPEC-0079 as an owner; `ARCHIVE-INDEX-STRUCTURE` rejected two Markdown tables
added to the Stage 98 index, because the index parser treats table rows as
record-index structure, so they were rewritten as lists. No validator changed.

Limitation: direct working-tree runs of `scripts/archive_cutover.py` and
`tests.test_archive_cutover` fail with index drift diagnostics while the
changes are uncommitted, because they compare the Git index with the working
tree; the isolated QA snapshot run passed.

Review: an independent read-only review reported three HIGH findings and one
MEDIUM finding, and each was verified against the tree. The HIGH findings (a
present-tense catalog envelope in the Stage 98 index, and the architect
responsibility and the descriptions index restating the decision-log
exception) were fixed with the transition boundary. The MEDIUM finding, the
active SPEC-0054 body, is enumerated below rather than edited.

Residual risk: the governance prose states a contract that the validators do
not enforce until tsk-0002, and ADR-0038 is still proposed.

Pending, with owners:

- Fifteen superseded architecture decisions remain in Stage 02: ADR-0013,
  ADR-0015, ADR-0016, ADR-0017, ADR-0018, ADR-0019, ADR-0020, ADR-0021,
  ADR-0022, ADR-0023, ADR-0024, ADR-0025, ADR-0027, ADR-0034, and ADR-0035. Each
  move to `superseded/` needs its own authorization after
  [tsk-0002](tsk-0002-move-registry-and-validators.md). Next owner: the
  architecture decision owner.
- Documents citing `migrations/` before acceptance: SPEC-0054 TSK-0012 and
  TSK-0013, SPEC-0072 TSK-0001, and SPEC-0073 TSK-0001. Documents citing
  `superseded/`: ADR-0032 and SPEC-0072 TSK-0001. The active SPEC-0054 Spec body
  still states that all ADRs remain in the Stage 02 decision log. They stay as
  they are. Next owner: each document's owning Spec when it is next revised.
- Machine references to Stage 98 paths in `scripts/` and `tests/` belong to
  tsk-0002.
- ADR-0038 acceptance and ADR-0032's move to `superseded` are the first reviewed
  change after merge. Next owner: the architecture decision owner.
- SPEC-0054 TSK-0009, TSK-0013, and TSK-0014 dispositions, which SPEC-0078
  recorded as depending on the retention policy, now depend on ADR-0038 and
  remain with SPEC-0054.

This record, its Spec, and its Plan stay in their creation states because the
lifecycle gate compares a change with its base, where this package does not
exist.

## Traceability

Each work item carries its observed result and durable evidence.

### Lifecycle Traceability

| Criterion / work item                 | Result | Evidence                                                               |
| ------------------------------------- | ------ | ---------------------------------------------------------------------- |
| [WORK-001](../plan.md#work-breakdown) | Done.  | Decision record and index in the working tree.                         |
| [WORK-002](../plan.md#work-breakdown) | Done.  | Policy and hub changes in the working tree.                            |
| [WORK-003](../plan.md#work-breakdown) | Done.  | Stage 98 index prose in the working tree.                              |
| [WORK-004](../plan.md#work-breakdown) | Done.  | Stage index, description, and requirement changes in the working tree. |
| [WORK-006](../plan.md#work-breakdown) | Done.  | Pending dispositions and consumers in this record.                     |
