---
title: "Finished Package Retention Technical Specification"
version: "0.2.0"
type: "sdlc/spec"
status: "done"
owner: "platform"
updated: "2026-09-27"
layer: "specs"
artifact_id: "SPEC-0094"
---

# Finished Package Retention Technical Specification (Spec)

## Overview

Eight Stage 03 packages are `done`, with every member terminal, and still sit
in the current tree: SPEC-0072, SPEC-0085, SPEC-0087, SPEC-0088, SPEC-0089,
SPEC-0090, SPEC-0091, and SPEC-0093. On 2026-09-27 the request owner asked for
every blocked, deferred, or unstarted Stage 03 item to be completed or disposed
of, and approved retaining the finished packages in the same round (chooser:
request owner; choice: "move to the archive together"). This Spec owns that
round.

## Strategic Boundaries & Non-goals

In scope: the eight packages above, one Retention Catalog row per unit, the
current consumers each move proves wrong, and this package.

Out of scope: SPEC-0008, which stays `active` by design; SPEC-0086, which
closed in the same pull request and so has no default-branch envelope yet;
any change to a frozen record, a sealed ledger, or a retained body; any
registry, profile, state, or edge change; any live cluster, provider runtime,
or network action.

## Contracts

Retention follows [ADR-0040](../../02.architecture/decisions/0040-archive-reappraisal-and-verifiable-sources.md).
A unit leaves as one whole package, its anchor state decides the class, and it
equals its source Git object entry for entry. Each catalog row names a commit
that the default branch already reaches. A `done` package goes to
`completed/`, and each current citation of it is repointed to the retained
path.

## Core Design

All eight packages move to `completed/03.specs/` in one commit, because they
link to one another and a retained body is never edited to make a link
resolve. The envelope is `fbcafca1`, the default-branch tip this round starts
from. SPEC-0086 follows in a later round, once its closure commit is on the
default branch.

## Data Modeling & Storage Strategy

Git holds the bytes. The catalog row is the only recovery reference. No digest,
blob pin, redirect, or path ledger is added. No migration record is written,
because no consumer outside this repository reads a moved path.

## Interfaces & Data Structures

The Stage 98 index gains one catalog row per unit. The Stage 03 index loses
the tree entry and the index row of each moved package. No machine interface
changes.

## Edge Cases & Error Handling

A unit whose members are not all terminal stays. A retained body's links are
read at its original path in the envelope commit.

## Failure Modes & Fallback / Human Escalation

A failing gate stops the round, and no gate, test pin, or allowlist is weakened
to pass. A unit that cannot move is recorded as a named deferral in the Task.

## Verification Commands

```bash
python3 scripts/validate-document-lifecycle.py --root . --mode strict
python3 scripts/validate-links-and-owners.py --root . --mode strict
python3 scripts/run-archive-contract-tests.py --root .
python3 scripts/qa.py staged
```

## Success Criteria & Verification Plan

| ID | Criterion | Evidence |
| --- | --- | --- |
| VAL-FPR-001 | The approval and each unit's anchor state, members, and consumers are recorded before any move | Retention Task |
| VAL-FPR-002 | The eight packages are retained in `completed/` as exact units with one catalog row each | Lifecycle and archive gates |
| VAL-FPR-003 | Every current citation of a moved package resolves to its retained path | Link gate |
| VAL-FPR-004 | This package closes with observed staged results, and hosted `qa` is handed to the request owner | Staged QA |

## Traceability

The [Implementation Plan](plan.md) owns order and risk. The
[retention Task](tasks/tsk-0001-retain-finished-packages.md) owns the evidence.

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0003-FR-0020](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-FPR-001 | Survey recorded in the Task |
| [REQ-0003-FR-0020](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-FPR-002 | Lifecycle and archive gates |
| [REQ-0003-FR-0015](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-FPR-003 | Citation decision over the corpus |
| [REQ-0003-FR-0018](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-FPR-004 | Staged QA |
