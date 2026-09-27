---
title: "Closed Package Retention Technical Specification"
version: "0.2.0"
type: "sdlc/spec"
status: "done"
owner: "platform"
updated: "2026-09-27"
layer: "specs"
artifact_id: "SPEC-0095"
---

# Closed Package Retention Technical Specification (Spec)

## Overview

[SPEC-0094](../../98.archive/completed/03.specs/0094-finished-package-retention/spec.md) retained eight finished
packages and deferred SPEC-0086, because SPEC-0086 closed in the same pull
request and had no default-branch envelope yet. PR #102 merged both on
2026-09-27. SPEC-0086 and SPEC-0094 are now `done`, with every member terminal,
and the default branch holds their final trees. This Spec retains both, under
the request owner's 2026-09-27 approval to archive the finished packages.

## Strategic Boundaries & Non-goals

In scope: SPEC-0086 and SPEC-0094, one Retention Catalog row each, the current
consumers each move proves wrong, and this package.

Out of scope: SPEC-0008, which stays `active` by design; any change to a frozen
record, a sealed ledger, or a retained body; any registry, profile, state, or
edge change; any live cluster, provider runtime, or network action.

## Contracts

Retention follows [ADR-0040](../../02.architecture/decisions/0040-archive-reappraisal-and-verifiable-sources.md).
A unit leaves as one whole package, its anchor state decides the class, and it
equals its source Git object entry for entry. Each catalog row names a commit
that the default branch already reaches. A `done` package goes to
`completed/`, and each current citation of it is repointed to the retained
path.

## Core Design

Both packages move to `completed/03.specs/` in one commit, and the envelope is
`576a8927`, the PR #102 merge on the default branch. The provider notes name
the SPEC-0086 Task path in code spans, so those spans follow the retained
path.

## Data Modeling & Storage Strategy

Git holds the bytes. The catalog row is the only recovery reference. No digest,
blob pin, redirect, or path ledger is added.

## Interfaces & Data Structures

The Stage 98 index gains two catalog rows. The Stage 03 index loses both
entries. No machine interface changes.

## Edge Cases & Error Handling

A unit whose members are not all terminal stays. A retained body's links are
read at its original path in the envelope commit.

## Failure Modes & Fallback / Human Escalation

A failing gate stops the round, and no gate, test pin, or allowlist is weakened
to pass.

## Verification Commands

```bash
python3 scripts/qa.py staged
python3 scripts/run-archive-contract-tests.py --root .
python3 scripts/archive_cutover.py --root .
```

## Success Criteria & Verification Plan

| ID | Criterion | Evidence |
| --- | --- | --- |
| VAL-CPR-001 | The approval and each unit's members and consumers are recorded before the move | Retention Task |
| VAL-CPR-002 | SPEC-0086 and SPEC-0094 are retained in `completed/` as exact units with one catalog row each | Lifecycle and archive gates |
| VAL-CPR-003 | Every current citation of a moved package resolves to its retained path | Link gate |

## Traceability

The [Implementation Plan](plan.md) owns order and risk. The
[retention Task](tasks/tsk-0001-retain-closed-packages.md) owns the evidence.

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0003-FR-0020](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-CPR-001 | Survey recorded in the Task |
| [REQ-0003-FR-0020](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-CPR-002 | Lifecycle and archive gates |
| [REQ-0003-FR-0015](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-CPR-003 | Citation decision over the corpus |
