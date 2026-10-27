---
title: "Archive Evidence Owner Migration"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "platform"
updated: "2026-10-28"
layer: "specs"
artifact_id: "SPEC-0131"
---

# Archive Evidence Owner Migration Technical Specification (Spec)

## Overview

[SPEC-0130](../0130-archive-history-link-migration/spec.md) removed twelve
retained Archive units whose only consumers were history links. Ten more units
are named only by current documents: history links, identifier mentions, and
provider-note sentences that name a Task as the owner of evidence whose facts
the note already states. This Spec moves those consumers to plain identifiers
and a Git recovery route. It also corrects sentences that still say removed
Specs are kept in `98.archive/retired/`. It then removes the ten units under
[ADR-0040](../../02.architecture/decisions/0040-archive-reappraisal-and-verifiable-sources.md)
as `git-history-only`. The [Plan](plan.md) orders the work and
[Task 0001](tasks/tsk-0001-archive-evidence-owner-migration.md) records it.

## Strategic Boundaries & Non-goals

- In scope:
  - consumers of the ten units in REQ-0003, REQ-0004, AD-0006, AD-0007,
    ADR-0036, research note m0009, `.claude/provider.md`, `.codex/provider.md`,
    `examples/aws/README.md` and `examples/azure/README.md`;
  - the sentences that say SPEC-0047, 0048, 0049, 0050 or 0051 are kept in
    `98.archive/retired/`;
  - removing the ten whole units and adding one Retention Assessment row each.
- Non-goals:
  - SPEC-0104, whose Tasks are the acceptance evidence that REQ-0004
    FR-0008 and FR-0010 and AD-0007 cite;
  - SPEC-0098 and the other retained units with registry, validator or test
    consumers;
  - rewriting links inside other Archive payloads, which are history;
  - changing any observed fact a provider note states, or any validator,
    registry or workflow.

## Contracts

- A history link becomes the package identifier as plain text, and each
  edited document names the Retention Catalog as the recovery route.
- A sentence that names a removed Task as an evidence owner keeps the fact it
  states and says that the Task recorded the evidence and is recovered from
  Git.
- A unit is removed only whole, only with Hold `none`, only when no tracked
  file outside Stage 98 links to its path or names it as a current owner, and
  only when its catalog envelope still resolves from `main`.
- Each removed unit gets assessment `unreviewed` and availability
  `git-history-only`. Catalog rows and envelopes stay unchanged, and
  availability never returns to `retained`.

## Core Design

The disposition reuses the ADR-0040 table and validators that SPEC-0122 and
SPEC-0130 used. The consumer test is a path and identifier search for each
unit over tracked `.md`, `.json`, `.py`, `.yml`, `.yaml` and `.toml` files
outside Stage 98, read sentence by sentence.

## Data Modeling & Storage Strategy

Ten rows in the Retention Assessment table of `docs/98.archive/README.md`.

## Interfaces & Data Structures

Row columns follow the registry `archive_assessment` contract, as in
SPEC-0122.

## Edge Cases & Error Handling

- A unit with a consumer outside this repository cannot be observed; removal
  is still recoverable from Git history.
- A sentence that names both a removed and a retained Task keeps the retained
  Task as owner.
- A removal row whose unit is still present fails
  `ARCHIVE-ASSESSMENT-AVAILABILITY`.

## Failure Modes & Fallback / Human Escalation

If a removed unit is needed again, it returns as a new unit under a new
decision, recovered with `git archive <envelope commit> <original path>`.

## Verification Commands

- `git grep` for each unit path and identifier outside Stage 98.
- `git rev-parse` equality between each current unit tree and its envelope.
- `git archive <commit> <path>` into a scratch directory per unit.
- `python3 scripts/qa.py staged` on the exact index.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-EO-001 | No tracked file outside Stage 98 links to the ten units or names their Tasks as current evidence owners, every stated fact is kept, and no sentence says a removed Spec is kept in `98.archive/retired/`. |
| VAL-EO-002 | Each unit's envelope tree equals its current tree and restores into a scratch directory with the expected file count. |
| VAL-EO-003 | The ten units are absent, each has a valid `git-history-only` row, and staged QA passes on every commit. |
| VAL-EO-004 | An independent reviewer confirms the consumer edits and removals, and the pull request's hosted checks pass. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0003-FR-0024](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-EO-001 | Consumer search and review |
| [REQ-0003-FR-0024](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-EO-002 | Isolated recovery |
| [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-EO-003 | Assessment validation and staged QA |
| [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-EO-004 | Independent review and hosted checks |
