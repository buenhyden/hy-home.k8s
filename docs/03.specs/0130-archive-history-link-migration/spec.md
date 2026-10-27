---
title: "Archive History Link Migration"
version: "0.1.0"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-10-28"
layer: "specs"
artifact_id: "SPEC-0130"
---

# Archive History Link Migration Technical Specification (Spec)

## Overview

SPEC-0122 removed seven consumer-free Archive units and left 57 `retained`
because each still had a consumer. A census on 2026-10-28 found twelve of the
57 whose only consumers are history links in two Requirements and one
architecture description. This Spec turns those links into plain package
identifiers, which ends the consumer dependency. It then removes the twelve
units under
[ADR-0040](../../02.architecture/decisions/0040-archive-reappraisal-and-verifiable-sources.md)
as `git-history-only`. The [Plan](plan.md) orders the work and
[Task 0001](tasks/tsk-0001-archive-history-link-migration.md) records it.

## Strategic Boundaries & Non-goals

- In scope:
  - the history links to the twelve units in REQ-0003, REQ-0004 and AD-0007;
  - removing the twelve whole units from `docs/98.archive/completed/03.specs/`;
  - one Retention Assessment row per removed unit.
- Non-goals:
  - the other 45 retained units, including those that own provider runtime
    evidence or are named by the registry, validators or tests;
  - rewriting links inside other Archive payloads, which are history;
  - reappraising whether a removed unit's historical claims are still true;
  - any change to validators, the registry or `.github/workflows/**`.

## Contracts

- A history link is replaced by the package identifier as plain text. The
  sentence keeps its meaning, and the document names where the bodies are
  recovered.
- A unit is removed only whole, only with Hold `none`, only when no tracked
  file outside Stage 98 links to its path, and only when its catalog envelope
  still resolves from `main`.
- Each removed unit gets assessment `unreviewed` and availability
  `git-history-only`. Catalog rows and envelopes stay unchanged.
- Availability never returns to `retained`.

## Core Design

The disposition reuses the ADR-0040 table and validators that SPEC-0122 used.
The consumer test is a path search for each unit directory over tracked
`.md`, `.json`, `.py`, `.yml`, `.yaml` and `.toml` files outside Stage 98.
Plain identifier mentions such as `SPEC-0088` remain as history, not as
consumers.

## Data Modeling & Storage Strategy

Twelve rows in the Retention Assessment table of `docs/98.archive/README.md`.

## Interfaces & Data Structures

Row columns follow the registry `archive_assessment` contract, as in
SPEC-0122.

## Edge Cases & Error Handling

- A unit with a consumer outside this repository cannot be observed; removal
  is still recoverable from Git history.
- Links from other Archive payloads to a removed unit are historical links
  read at their source commit, as after SPEC-0122.
- A removal row whose unit is still present fails
  `ARCHIVE-ASSESSMENT-AVAILABILITY`.

## Failure Modes & Fallback / Human Escalation

If a removed unit is needed again, it returns as a new unit under a new
decision, recovered with `git archive <envelope commit> <original path>`.

## Verification Commands

- `git grep` for each unit path outside Stage 98.
- `git rev-parse` equality between each current unit tree and its envelope.
- `git archive <commit> <path>` into a scratch directory per unit.
- `python3 scripts/qa.py staged` on the exact index.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-AM-001 | No tracked file outside Stage 98 links to any of the twelve units, and the edited sentences keep their meaning and name the recovery route. |
| VAL-AM-002 | Each unit's envelope tree equals its current tree and restores into a scratch directory with the expected file count. |
| VAL-AM-003 | The twelve units are absent, each has a valid `git-history-only` row, and staged QA passes on every commit. |
| VAL-AM-004 | An independent reviewer confirms the link edits and removals, and the pull request's hosted checks pass. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0003-FR-0024](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-AM-001 | Consumer path search and review |
| [REQ-0003-FR-0024](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-AM-002 | Isolated recovery |
| [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-AM-003 | Assessment validation and staged QA |
| [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-AM-004 | Independent review and hosted checks |
