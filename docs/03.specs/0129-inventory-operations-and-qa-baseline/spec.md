---
title: "Inventory, Operations and QA Baseline"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "platform"
updated: "2026-10-28"
layer: "specs"
artifact_id: "SPEC-0129"
---

# Inventory, Operations and QA Baseline Technical Specification (Spec)

## Overview

SPEC-0125 left three partial CRs that need no operator decision: a
classified inventory of tracked files (CR-01.07), a survey of operations
documents for repeated procedures (CR-07.05), and reproducible QA timing
figures (CR-11.04). This Spec records the three results in its Task and
makes the two operations edits the survey supports. The [Plan](plan.md)
orders the work and [Task 0001](tasks/tsk-0001-inventory-operations-and-qa-baseline.md)
records it.

## Strategic Boundaries & Non-goals

- In scope: this package, the Stage 03 README index, RUN-0002 step 9 and
  POL-0007 section 2-2.
- Non-goals:
  - optimizing QA; the figures are a baseline, not a before-and-after claim;
  - consolidating overlaps the survey judged harmless;
  - changing tracked file modes, links or the secret baseline.

## Contracts

- The inventory counts tracked files by kind and names every symlink,
  submodule, large-file pointer and binary, with a disposition for each kind.
- Each operations edit removes a verbatim repeat or an ambiguity without
  changing a procedure's effect.
- Each timing figure names the commit, profile, gate count, exit code,
  seconds, UTC time, Python version and core count, and replays one real
  commit on its parent.

## Core Design

The inventory uses `git ls-files` modes and content checks. The operations
survey reads each document's role, age, consumers and validity. The timing
replays one commit's diff into its parent's index in a detached worktree and
runs `scripts/qa.py staged`.

## Data Modeling & Storage Strategy

No stored data.

## Interfaces & Data Structures

None.

## Edge Cases & Error Handling

- Replaying a whole pull request as one index jumps Task states and fails by
  design, so the timing replays single commits.

## Failure Modes & Fallback / Human Escalation

Reverting the pull request restores the two operations documents.

## Verification Commands

- `git ls-files -s` and content checks for the inventory.
- `python3 scripts/qa.py staged` for each replayed commit.
- `python3 scripts/qa.py staged` on the exact index of each commit here.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-SV-001 | The Task records the classified inventory with a disposition for every special kind. |
| VAL-SV-002 | The Task records the operations survey, RUN-0002 step 9 no longer repeats RUN-0001's gate, POL-0007 names the Traefik-served `nginx` class, and an independent reviewer confirms both edits. |
| VAL-SV-003 | The Task records reproducible staged QA figures for one document commit and one validator commit. |
| VAL-SV-004 | Staged QA passes on every commit and the pull request's hosted checks pass. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0003-FR-0021](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-SV-001 | Inventory record |
| [REQ-0003-FR-0014](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-SV-002 | Survey record and review |
| [REQ-0003-FR-0018](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-SV-003 | Timing record |
| [REQ-0003-FR-0018](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-SV-004 | Staged QA and hosted checks |
