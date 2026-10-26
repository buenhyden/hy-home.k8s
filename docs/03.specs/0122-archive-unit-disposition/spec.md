---
title: "Archive Unit Disposition"
version: "0.1.0"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-10-27"
layer: "specs"
artifact_id: "SPEC-0122"
---

# Archive Unit Disposition Technical Specification (Spec)

## Overview

[ADR-0040](../../02.architecture/decisions/0040-archive-reappraisal-and-verifiable-sources.md)
admits one change to a retained Archive unit: an approved removal of the whole
unit from the current tree, after which its availability is
`git-history-only`. No unit has used that path, and the Retention Assessment
table is empty. A dry-run on main `0a9e8062` found seven Retention Catalog
units with no consumer outside Stage 98. This Spec removes exactly those seven.
The [Plan](plan.md) orders the work and
[Task 0001](tasks/tsk-0001-archive-unit-disposition.md) records it.

## Strategic Boundaries & Non-goals

- In scope:
  - removing seven whole units from `docs/98.archive/`;
  - one Retention Assessment row per removed unit.
- Non-goals:
  - the 57 retained catalog units that still have a registry, validator,
    test or current-document consumer;
  - the frozen ADR-0032 generation, sealed records and migration ledgers,
    which ADR-0040 does not reappraise;
  - reappraising whether a removed unit's historical claims are still true;
  - the archive validator's handling of the ignored `graphify-out/` paths;
  - any change to validators, registry or `.github/workflows/**`.

## Contracts

- A unit is removed only whole, only with Hold `none`, and only when its
  catalog envelope still resolves from `main`.
- Each removed unit gets assessment `unreviewed` and availability
  `git-history-only`, because only removal eligibility was judged.
- Catalog rows and envelopes stay unchanged, so Git still recovers each unit.
- Availability never returns to `retained`.

## Core Design

The disposition uses the existing ADR-0040 table and validators; no code
changes. Consumers were searched by unit directory name and by `SPEC-####`
identifier across tracked `.md`, `.json`, `.py`, `.yml`, `.yaml` and `.toml`
files outside Stage 98.

## Data Modeling & Storage Strategy

Seven rows in the Retention Assessment table of `docs/98.archive/README.md`.

## Interfaces & Data Structures

Row columns follow the registry `archive_assessment` contract: Disposition
Record, Assessment, Availability, Current Owner, Decision, Assessed, Hold.

## Edge Cases & Error Handling

- A unit with a consumer outside this repository cannot be observed; removal
  is still recoverable from Git history.
- A removal row whose unit is still present fails
  `ARCHIVE-ASSESSMENT-AVAILABILITY`.

## Failure Modes & Fallback / Human Escalation

If a removed unit turns out to be needed, it comes back as a new unit under a
new decision, recovered with `git archive <envelope commit> <original path>`.

## Verification Commands

- `git rev-parse` equality between each current unit tree and its envelope.
- `git archive <commit> <path>` into a scratch directory per unit.
- `python3 scripts/qa.py staged` on the exact index.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-AD-001 | Each of the seven units has zero consumers outside Stage 98, an envelope tree equal to its current tree, and a scratch restore with the expected file count. |
| VAL-AD-002 | The seven units are absent, each has a valid `git-history-only` row, and staged QA passes on the exact index. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0003-FR-0024](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-AD-001 | Consumer census and isolated recovery |
| [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-AD-002 | Assessment validation and staged QA |
