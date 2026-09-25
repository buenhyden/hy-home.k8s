---
title: "SPEC-0049 Retirement Technical Specification"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "platform"
updated: "2026-09-25"
layer: "specs"
artifact_id: "SPEC-0090"
---

# SPEC-0049 Retirement Technical Specification (Spec)

## Overview

[SPEC-0089](../0089-deferred-conflict-resolution/spec.md) withdrew SPEC-0049
and cancelled its seven Tasks, and deferred the move into `retired/` until the
withdrawal reached the default branch. The request owner pushed that state and
approved the move on 2026-09-25. This Spec owns that move.

## Strategic Boundaries & Non-goals

In scope: the SPEC-0049 package as one unit; one Retention Catalog row; the
current documents that link to it; and this package.

Out of scope: any other package; any change to a retained body, frozen record,
or sealed ledger; any registry, profile, state, or edge change; any live
cluster or provider action.

## Contracts

Retention follows [ADR-0040](../../02.architecture/decisions/0040-archive-reappraisal-and-verifiable-sources.md).
The unit leaves whole, its `withdrawn` anchor with every member terminal
selects `retired/`, and it equals its envelope tree entry for entry. The
catalog row names a commit that the default branch already reaches. `retired/`
may not be cited, so every current link to the package becomes plain text
naming it and its disposition in the same commit.

## Core Design

Three local commits: propose this package; activate it and move the unit with
its consumers rewritten; record the results and close.

## Data Modeling & Storage Strategy

Git holds the bytes. The catalog row is the only recovery reference. No
digest, redirect, path ledger, or migration record is added, because no
consumer outside this repository reads the moved path.

## Interfaces & Data Structures

The Stage 98 index gains one catalog row. The Stage 03 index loses the
package's row. No machine interface changes.

## Edge Cases & Error Handling

The envelope commit must be on the default branch before the move commit
passes the archive gate, so the move is validated after that commit is pushed.
A retained body is never edited to make a link resolve.

## Failure Modes & Fallback / Human Escalation

A failing gate stops the move, and no gate is weakened. A move already on the
default branch is frozen, and a later correction needs its own decision.

## Verification Commands

```bash
python3 scripts/validate-document-lifecycle.py --root . --mode strict
python3 scripts/validate-links-and-owners.py --root . --mode strict
python3 scripts/archive_cutover.py --root .
python3 scripts/qa.py staged
```

## Success Criteria & Verification Plan

| ID | Criterion | Evidence |
| --- | --- | --- |
| VAL-SRT-001 | The approval, anchor state, members, and consumers are recorded before the move | Retirement Task |
| VAL-SRT-002 | SPEC-0049 is retained in `retired/` as an exact unit with one catalog row | Lifecycle and archive gates |
| VAL-SRT-003 | No current document links to the retired unit | Link gate |
| VAL-SRT-004 | Each commit passes staged QA | Staged QA |

## Traceability

The [Implementation Plan](plan.md) owns order and risk. The
[retirement Task](tasks/tsk-0001-retire-spec-0049.md) owns the evidence.

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0003-FR-0020](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-SRT-001 | Survey recorded in the Task |
| [REQ-0003-FR-0020](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-SRT-002 | Lifecycle and archive gates |
| [REQ-0003-FR-0015](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-SRT-003 | Citation decision over the corpus |
| [REQ-0003-FR-0018](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-SRT-004 | Staged QA |
