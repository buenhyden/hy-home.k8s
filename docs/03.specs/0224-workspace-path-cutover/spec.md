---
title: "Workspace Path Cutover"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "platform"
updated: "2026-11-19"
artifact_id: "SPEC-0224"
---

# Workspace Path Cutover Technical Specification (Spec)

## Overview

### Goal

On 2026-11-19 the user asked to apply the governance redesign package of the
same date to this checkout: give `docs/00.workspace/`, `.agents/`, the
provider folders, the product stages, the request records and Stage 99 one
owner each, keep one active source per meaning, and number the category
folders of `docs/`. Locally this is the path part of Q07-CUTOVER: the W owner
move of SDLC-H01 and the category moves of DOC-H01 (SDD-PATHS), which the user
adopted on 2026-11-18 and 2026-11-19.

#### Owning Requirements

[REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md)
FR-0015 (consumer succession), FR-0020 (disposition) and FR-0032 (one
vocabulary owner). [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md)
describes the resulting structure.

### Consumers

- The Stage 99 registry, its schemas and every reader of a profile path.
- The lifecycle comparison, which follows a moved document (DOCLIFE-R023).
- The knowledge, link, Markdown profile, ledger, review-delta and pre-edit
  guards, the validation routing registry and their tests.
- Every current link to a moved document.

## Scope

### In Scope

- Move the W policies (SDLC, document authoring and lifecycle, Git, quality,
  formatting and linting, approval and safety), the glossary, AD-0006,
  ADR-0058, GDE-0010, RUN-0011 and RUN-0012 to `docs/00.workspace/`.
- Split approval and safety along SAFE-R001 to SAFE-R010, SAFE-R013 to
  SAFE-R016, SAFE-R020 and SAFE-R021 (W) and SAFE-R011, SAFE-R012 and
  SAFE-R017 to SAFE-R019 (A), and Git along GIT-R011 to GIT-R013 (A), keeping
  every rule ID with one owner.
- Number the category folders: `01.descriptions`, `02.decisions`, `01.tasks`,
  `01.guides` to `04.incidents`, `01.research` to `03.data`, `01.contracts`,
  `02.templates` and its numbered form groups.
- Update profiles, schemas, readers, tests and current links in the same
  change, and teach the lifecycle comparison to follow a moved document.
- Separate the work-system architecture from the product architecture: move
  the work-system ADRs (0030, 0031, 0033, 0036, 0047, 0048, 0052, 0053, 0055
  to 0063) to `docs/00.workspace/02.architecture/02.decisions/`, keep the
  platform ADRs and ADs in `docs/02.architecture/`, and state each area's
  purpose in its README and `AGENTS.md`.
- Give `docs/00.workspace/` its `AGENTS.md` and `CLAUDE.md`, a collection
  README for each category, and a project entry that links SDLC-R036 and
  REQ-0003.

### Out of Scope

- History rewrite, document ID renumbering (DOC-12), Stage 98 disposal and the
  history-dependent checks of Q07-H01.
- Historical bodies: accepted ADR text, published reference members, Archived
  Lineage rows and completed Task evidence keep their wording; only link
  destinations move.
- Push, pull request and merge.

## Behavior Contract

### Inputs and Outputs

The input is the tree at `4b2b670d`. The output is a tree in which every moved
document keeps its profile, artifact ID and rule IDs at its new path, no
current link names an old path, and the selected checks pass.

### Failure Behavior

A rename that changes the profile or the artifact ID stays refused
(LIFECYCLE-RENAME). A rule ID listed by two policies, or a split code record
without its rule list, fails the registry check. No check or test is weakened
to finish.

## Acceptance Criteria

### Criteria

| Criterion ID | Expected Result |
| --- | --- |
| VAL-CUTOVER-001 | The W documents live under `docs/00.workspace/` with their IDs and rule IDs; SAFE and GIT rule IDs each have exactly one owner, and the registry refuses a rule ID with two owners. Work-system AD and ADRs live in `docs/00.workspace/02.architecture/` and product ones in `docs/02.architecture/`, each area stating its purpose; the stage has its agent gateway and category indexes. |
| VAL-CUTOVER-002 | The category folders of `docs/` are numbered, every profile, reader and current link uses the new paths, and the lifecycle comparison admits a move only when the profile and artifact ID are unchanged. |
| VAL-CUTOVER-003 | The knowledge check reads the workspace glossary, and every selected check passes on the staged change. |

### Verification Strategy

| Check ID | Guarantee | Input | Trust Boundary | Required When | Evidence |
| --- | --- | --- | --- | --- | --- |
| qa-staged | Every selected gate passes on the exact index | Staged index against HEAD | Repository-static only | Every commit | Staged QA result |

#### Normative and Evidence

The [document lifecycle policy](../../00.workspace/03.process/document-lifecycle.md)
DOCLIFE-R023 sets the move rule. Evidence is in the [Task](01.tasks/tsk-0001-workspace-path-cutover.md).

#### Historical and Navigation

Old paths stay recoverable from Git history at `4b2b670d`.

### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0015](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-CUTOVER-001 | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) | Registry and policy rule checks in staged QA |
| [REQ-0003-FR-0020](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-CUTOVER-002 | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) | Lifecycle check and its tests in staged QA |
| [REQ-0003-FR-0032](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-CUTOVER-003 | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) | Knowledge check and staged QA |
