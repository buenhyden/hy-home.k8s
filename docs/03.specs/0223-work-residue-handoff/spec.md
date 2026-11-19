---
title: "Work Residue Handoff"
version: "0.1.0"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-11-19"
artifact_id: "SPEC-0223"
---

# Work Residue Handoff Technical Specification (Spec)

## Overview

### Goal

On 2026-11-19 the user asked to analyze the Stage 03 Specs, Plans and Tasks and
delete what conflicts or differs with the current implementation. Three
packages remained:

- SPEC-0221 and SPEC-0222 are completed, with every criterion accepted, so the
  document lifecycle requires their exit (DOCLIFE-R008).
- The SPEC-0161 Spec covers the W00 v14.7 delta intake, while its Task grew
  into the log of every later work package and the only live residue table.
  The package is completed, and its scope no longer matches its Task.

The user chose to delete all three now and move the open residue to a new,
small host. This package is that host. Its Task holds only the open work
residue and the evidence of the move and of the three exits.

#### Owning Requirements

[REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md)
FR-0015 and FR-0020 own consumer succession and ordinary package disposition;
its Archived Lineage receives the three summaries and recovery proofs. The
[document lifecycle policy](../../../.agents/governance/document-lifecycle.md)
DOCLIFE-R008 requires the exit. No architecture decision changes.

### Consumers

- The work residue ledger gate, which reads the live `Residue Handoff` table.
- The lifecycle and registry checks, which read the package exit, the
  registry `work_residue` block and the retained-form exceptions.
- The owners named in each residue row, and Q07-CUTOVER.

## Scope

### In Scope

- A new live `Residue Handoff` table here with every open entry of the three
  packages, and the ledger sources moved to it.
- The exit of SPEC-0161, SPEC-0221 and SPEC-0222: frozen Task decisions,
  Archived Lineage rows with recovery proof, the Stage 03 README, and the
  deletion of their terminal ledger entries.
- The consumers that read those package files: the registry
  `historical_tables` and the retained Spec and Plan form exceptions
  (`spec-approved-retained-form` and its Plan twin), ADR-0063's link, four
  `.secrets.baseline` entries, the Stage 03 README, and the tests that read the
  package paths (`tests/test_common_form_tree.py` `RetainedSpecPlanTests` and
  the retained Plan cases, `tests/test_task_execution_contract.py` for
  SPEC-0221).
- The Task header transition adapter (`TASK_RECORDED_HEADERS` and its helpers
  in `scripts/document_contracts.py`), whose own removal condition is these
  exits, with its readers in `scripts/validate-markdown-profiles.py` and
  `scripts/validate-links-and-owners.py` and its tests.

### Out of Scope

- Changing any residue's owner, state or resume condition.
- Renumbering, path moves and history removal, which stay with Q07-CUTOVER.
- Rewriting citations by ID, such as `SPEC-0161 EVD-191` in the provider
  notes or the registry `meaning_map` and `rollback` strings that name
  SPEC-0221 and SPEC-0222. An ID stays reserved by its lineage row and the
  text stays recoverable from Git history until Q07-H01 converts it.

## Behavior Contract

### Inputs and Outputs

The input is the tree at `93f130a8`. The output is a tree where `docs/03.specs/`
holds only this package and the ledger, every open ledger entry names this
Task as its source, and no registry entry, test or link names a deleted
package file.

### Failure Behavior

A consumer found after the freeze defers that package's deletion. A failing
check is fixed at its cause; no check or test is weakened to finish.

## Acceptance Criteria

### Criteria

| Criterion ID | Expected Result |
| --- | --- |
| VAL-RESIDUE-001 | The 30 open ledger entries of the three packages each have one open row in this Task's live table with their ID, Residue, Owner and Resume condition unchanged, and the ledger gate passes. |
| VAL-RESIDUE-002 | The three packages leave the tree with Archived Lineage rows and recovery proof, no tracked file reads a deleted package path, and every selected check passes on the exit commit. |
| VAL-RESIDUE-003 | No reader of `TASK_RECORDED_HEADERS` or the recorded Task header remains, and the document and Task contract suites pass before and after the removal. |

### Verification Strategy

| Check ID | Guarantee | Input | Trust Boundary | Required When | Evidence |
| --- | --- | --- | --- | --- | --- |
| work-residue-ledger | Each open entry matches one live row | Ledger and Tasks | Reads the tree, not the meaning of a residue | Every commit | Staged QA result |
| document-lifecycle | The exit shape and lineage are valid | Staged index against HEAD | Cannot prove recovery from another clone | The exit commit | Staged QA result |

#### Normative and Evidence

The [document lifecycle policy](../../../.agents/governance/document-lifecycle.md)
and REQ-0003 FR-0020 set the exit. Evidence is in the [Task](tasks/tsk-0001-work-residue-handoff.md).

#### Historical and Navigation

The deleted packages are summarized in the REQ-0003
[Archived Lineage](../../01.requirements/0003-workspace-agent-governance-platform.md#archived-lineage).

### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0015](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-RESIDUE-001 | N/A — no architecture decision changes | Ledger gate in staged QA |
| [REQ-0003-FR-0020](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-RESIDUE-002 | N/A — no architecture decision changes | Lifecycle check in staged QA |
| [REQ-0003-FR-0020](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-RESIDUE-003 | N/A — no architecture decision changes | Document contract suite before and after |
