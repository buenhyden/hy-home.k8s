---
title: "Stage 03 Terminal Package Retention Technical Specification"
version: "0.1.0"
type: "sdlc/spec"
status: "active"
owner: "platform"
updated: "2026-09-24"
layer: "specs"
artifact_id: "SPEC-0087"
---

# Stage 03 Terminal Package Retention Technical Specification (Spec)

## Overview

Seven Stage 03 packages are terminal and still sit in the current tree. SPEC-0047,
SPEC-0048, SPEC-0050, and SPEC-0051 are `withdrawn` with every Task terminal.
SPEC-0054, SPEC-0062, and SPEC-0084 are `done`.
[SPEC-0084](../0084-stage03-backlog-closeout/spec.md) left the withdrawn pair in
place because the `retired` class had no directory, and deferred SPEC-0054 and
SPEC-0062 with named owners because a test pin and a secret-scan allowlist entry
name paths inside them.

The request owner approved retaining all seven on 2026-09-24 (chooser: request
owner; choice: "Approve archive, separate package"). This Spec owns that round.

## Strategic Boundaries & Non-goals

In scope: the seven packages above; the first `retired/` retention class
directory; one Retention Catalog row per unit; the current consumers each move
proves wrong; the SPEC-0054 test pin and the SPEC-0062 secret-scan allowlist
entry; and this package.

Out of scope: any other package, including SPEC-0008, SPEC-0049, SPEC-0072,
SPEC-0085, and SPEC-0086; any change to a frozen record, a sealed ledger, or a
retained body; any registry, profile, state, or edge change; any live cluster,
provider runtime, or network action.

## Contracts

Retention follows [ADR-0040](../../02.architecture/decisions/0040-archive-reappraisal-and-verifiable-sources.md).
A unit leaves as one whole package, its anchor state decides the class, and it
equals its source Git object entry for entry. Each catalog row names a commit
that the default branch already reaches. A `withdrawn` package goes to
`retired/`, which may not be cited, so every current citation of it becomes
plain text naming the package and its disposition. A `done` package goes to
`completed/`, and a current citation of it is repointed to the retained path.

## Core Design

The round runs in two integrations, because each move must name a commit that
the default branch already holds and because the two deferred units carry
protected pins.

1. The four withdrawn packages move to `retired/03.specs/` in one commit, with
   the current consumers that link to them rewritten in the same commit.
2. SPEC-0054, SPEC-0062, and SPEC-0084 move to `completed/03.specs/` together,
   after the SPEC-0054 test pin is rewritten to read the retained path and the
   SPEC-0062 allowlist entry is moved with its test. SPEC-0084 moves in the same
   commit because the other bodies link to it.

## Data Modeling & Storage Strategy

Git holds the bytes. The catalog row is the only recovery reference. No digest,
blob pin, redirect, or path ledger is added. No migration record is written,
because no consumer outside this repository reads a moved path.

## Interfaces & Data Structures

The Stage 98 index gains one catalog row per unit. The Stage 03 index loses
the tree entry and the index row of each moved package. No machine interface
changes, except that the SPEC-0054 test and the secret-scan allowlist read the
retained paths.

## Edge Cases & Error Handling

A unit whose members are not all terminal stays. A consumer that cannot cite a
retired unit names it by identifier without a link. A retained body is never
edited to make a link resolve; its links are read at its original path in the
envelope commit.

## Failure Modes & Fallback / Human Escalation

A failing gate stops the round, and no gate, test pin, or allowlist is weakened
to pass. A unit that cannot move in this round is recorded as a named deferral
in the Task. A retention already merged is frozen, and a later correction needs
its own decision.

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
| VAL-STR-001 | The disposition approval and each unit's anchor state, members, and consumers are recorded before any move | Retention Task |
| VAL-STR-002 | SPEC-0047, SPEC-0048, SPEC-0050, and SPEC-0051 are retained in `retired/` as exact units with one catalog row each | Lifecycle and archive gates |
| VAL-STR-003 | No current document links to a retired unit | Link gate |
| VAL-STR-004 | SPEC-0054, SPEC-0062, and SPEC-0084 are retained in `completed/` as exact units with one catalog row each, or recorded as named deferrals | Lifecycle and archive gates, or the Task |
| VAL-STR-005 | The SPEC-0054 test pin and the SPEC-0062 allowlist entry read the retained paths, and no assertion is weakened | Unit tests and the secret-scan gate |
| VAL-STR-006 | This package closes with observed staged and hosted results | Staged QA and hosted CI |

## Traceability

The [Implementation Plan](plan.md) owns order and risk. The
[retention Task](tasks/tsk-0001-retain-terminal-stage-03-packages.md) owns the
evidence.

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0003-FR-0020](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-STR-001 | Survey recorded in the Task |
| [REQ-0003-FR-0020](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-STR-002 | Lifecycle and archive gates |
| [REQ-0003-FR-0015](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-STR-003 | Citation decision over the corpus |
| [REQ-0003-FR-0020](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-STR-004 | Lifecycle and archive gates |
| [REQ-0003-FR-0028](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-STR-005 | Unit tests and secret-scan gate |
| [REQ-0003-FR-0018](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-STR-006 | Staged QA and hosted CI |
