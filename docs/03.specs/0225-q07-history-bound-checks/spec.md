---
title: "Q07 History-Bound Check Conversion"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "platform"
updated: "2026-11-19"
artifact_id: "SPEC-0225"
---

# Q07 History-Bound Check Conversion Technical Specification (Spec)

## Overview

### Goal

Residue Q07-H01 requires that before Q07-CUTOVER rewrites history and
renumbers documents, no check, test or generator depends on a past SHA, Task,
reserved number or old registry generation. The 2026-11-19 read (SPEC-0223
EVD-008) found the `historical_tables` path already gone and seven checks
still bound. On 2026-11-19 the user asked to convert them and chose how:
an explicit form marker for the retained ADR form, a declared baseline for
the reserved policy codes, and the lineage reservations and `git show`
citations handled as data at the cutover.

#### Owning Requirements

[REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md)
FR-0015 (consumer succession) and FR-0020 (disposition).

### Consumers

- The Stage 99 registry, its schema and the readers of retained forms and
  policy rule codes.
- The lifecycle comparison and its cumulative history replay.
- The contract tests that read requirement documents by path.
- Residue Q07-H01 and Q07-CUTOVER.

## Scope

### In Scope

- Read only the current registry MAJOR, removing the older-generation
  compatibility (`historical_major` and the readable MAJOR list below 21).
- Build the tests that read requirement files 0001 to 0004 from synthetic or
  registry-derived inputs instead of fixed paths.
- Add a registry baseline for policy rule codes: the never-shrink and
  code-change comparisons apply only while base and proposed share it.
- Select the retained ADR form by an explicit frontmatter marker on the
  accepted ADRs that keep it, instead of an ADR ID range.
- Record in Q07-H01 what stays as cutover data: the Archived Lineage
  reservations, the `git show <sha>:` citations, and the reference retained
  forms bound to RES-0001 and AUD-0001, whose published members cannot take a
  marker.

### Out of Scope

- The history rewrite, document renumbering and Stage 98 disposal.
- Removing the dormant `historical_tables` key, which names no Task.
- Accepted ADR bodies: only their frontmatter gains the marker.

## Behavior Contract

### Inputs and Outputs

The input is `main` `cabab987`. The output is a tree whose checks pass with
no dependency on a registry older than MAJOR 21, on an ADR number range or on
an unchanged reserved-code list across a declared baseline.

### Failure Behavior

A registry from an older MAJOR is classified with the current registry. An
accepted ADR without the marker takes the current form tree; the marker on a
non-accepted ADR or on another profile is refused. Dropping a reserved code
without a new baseline is still refused. No check or test is weakened to
finish.

## Acceptance Criteria

### Criteria

| Criterion ID | Expected Result |
| --- | --- |
| VAL-HISTORY-001 | No reader keeps a registry generation below the current MAJOR, and no test reads a fixed requirement path. |
| VAL-HISTORY-002 | A reserved code may leave the registry only in a change that declares a new baseline; within one baseline the never-shrink and code-change refusals hold. |
| VAL-HISTORY-003 | The retained ADR form applies to an accepted ADR exactly when it carries the marker; no ADR ID range remains in code or registry. |
| VAL-HISTORY-004 | Q07-H01 records the converted checks and the data left for the cutover, and every selected check passes. |

### Verification Strategy

| Check ID | Guarantee | Input | Trust Boundary | Required When | Evidence |
| --- | --- | --- | --- | --- | --- |
| qa-staged | Every selected gate passes on the exact index | Staged index against HEAD | Repository-static only | Every commit | Staged QA result |

#### Normative and Evidence

The [document lifecycle policy](../../00.workspace/03.process/document-lifecycle.md)
DOCLIFE-R022 states the reserved-code rule. Evidence is in the [Task](01.tasks/tsk-0001-q07-history-bound-checks.md).

#### Historical and Navigation

The read of the eight checks is SPEC-0223 Task EVD-008.

### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0015](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-HISTORY-001 | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) | Contract suites in staged QA |
| [REQ-0003-FR-0020](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-HISTORY-002 | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) | Policy rule history tests in staged QA |
| [REQ-0003-FR-0020](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-HISTORY-003 | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) | Form tree tests in staged QA |
| [REQ-0003-FR-0015](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-HISTORY-004 | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) | Ledger gate and staged QA |
