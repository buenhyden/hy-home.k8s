---
title: "Closed Spec Package Retention Technical Specification"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "platform"
updated: "2026-09-28"
layer: "specs"
artifact_id: "SPEC-0101"
---

# Closed Spec Package Retention Technical Specification (Spec)

## Overview

On 2026-09-28 the request owner asked for SPEC-0098, SPEC-0099, and SPEC-0100
to be reviewed, closed, and then retained. SPEC-0098 closed in PR #110, and
SPEC-0099 and SPEC-0100 closed in PR #111. All three are `completed`, and the
default branch holds their final trees.

## Strategic Boundaries & Non-goals

In scope: the three packages as whole units, their Retention Catalog rows,
their current citations, the Stage 03 index, and this package.

Out of scope: any change to a retained body; SPEC-0008, which stays `active` by
design; the follow-ups SPEC-0100 handed to other owners.

## Contracts

- Retention follows [ADR-0040](../../02.architecture/decisions/0040-archive-reappraisal-and-verifiable-sources.md):
  each `completed` package moves whole to `completed/` under an envelope that
  the default branch reaches, with one catalog row each, and current citations
  are repointed.
- The moved trees are identical to the envelope trees.

## Core Design

| Unit | Before | After |
| --- | --- | --- |
| SPEC-0098, SPEC-0099, SPEC-0100 | `docs/03.specs/` | `docs/98.archive/completed/03.specs/`, one envelope on the default branch |

## Data Modeling & Storage Strategy

Git holds the retained bytes, and the catalog row is the only recovery
reference.

## Interfaces & Data Structures

The Stage 98 index gains three catalog rows, and the Stage 03 index loses three
entries. REQ-0003 repoints its two package links.

## Edge Cases & Error Handling

If the envelope is not yet on the default branch, the move waits. A retained
body keeps its original relative links; the archive gates treat them as
historical.

## Failure Modes & Fallback / Human Escalation

If a gate rejects the move, the packages stay in Stage 03 and the finding goes
to the request owner. No gate is relaxed to admit the move.

## Verification Commands

```bash
python3 scripts/qa.py staged
python3 scripts/run-archive-contract-tests.py --root .
python3 scripts/archive_cutover.py --root .
```

## Success Criteria & Verification Plan

| ID | Criterion | Evidence |
| --- | --- | --- |
| VAL-CSP-001 | SPEC-0098, SPEC-0099, and SPEC-0100 are retained as exact units with one catalog row each | Tree comparison, lifecycle and archive gates |
| VAL-CSP-002 | No current document links to a moved path | Links-and-owners gate |

## Traceability

The [Implementation Plan](plan.md) owns order and risk. The
[Task](tasks/tsk-0001-retain-closed-packages.md) owns the evidence.

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0003-FR-0020](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-CSP-001 | Lifecycle and archive gates |
| [REQ-0003-FR-0020](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-CSP-002 | Links-and-owners gate |
