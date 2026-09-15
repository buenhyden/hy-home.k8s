---
title: "Superseded Decision Retention Technical Specification"
version: "0.1.0"
type: "sdlc/spec"
status: "active"
owner: "platform"
updated: "2026-09-15"
layer: "specs"
artifact_id: "SPEC-0081"
---

# Superseded Decision Retention Technical Specification (Spec)

## Overview

This Spec retains the fifteen superseded architecture decisions that stayed in
the decision log after the ADR-0032 pilot: ADR-0013, ADR-0015 through ADR-0025,
ADR-0027, ADR-0034, and ADR-0035. The request owner approved each disposition on
2026-09-15. After this change the decision log holds only current decisions.

## Strategic Boundaries & Non-goals

Authorized scope is the fifteen decisions and their retained paths, the current
documents that linked them, the decision, architecture, documentation, Stage 03,
and Stage 98 indexes, REQ-0003, the SPEC-0054 decision-log rule, the lifecycle
regression fixture that read ADR-0035, and this package.

Explicit non-goals. No frozen record, ledger, retained package, or frozen index
row changes. A statement that names one of these decisions as history keeps its
text; only the link syntax goes. No validator changes. No live cluster, provider
runtime, or network action is authorized.

## Contracts

- Each decision is retained at its mirrored path under `superseded/` with its
  profile, identity, and terminal state, and differs from its source by relative
  link prefixes alone, compared through the fifteen moves together.
- The Retention Catalog carries one row per decision naming
  `<commit>:<original path>` for the comparison base.
- A current document names a retained decision by identifier and reaches it
  through the archive index; no current rule says a superseded decision stays in
  the decision log.

## Core Design

The fifteen move in one change, so links among them re-base to their retained
siblings. Every link found in a current document was lineage or history, so the
consumer change drops the link and keeps its text.

## Data Modeling & Storage Strategy

Fifteen catalog rows and fifteen retained bodies. No new data form.

## Interfaces & Data Structures

No interface changes; the ADR-0038 machinery from SPEC-0079 and SPEC-0080
proves the dispositions.

## Edge Cases & Error Handling

A historical constant in the validators that names one of the old paths keeps
working, because it applies only when that path is present in a comparison.

## Failure Modes & Fallback / Human Escalation

If a gate needs frozen content rewritten, the change stops and returns to the
request owner. The retention reverts with its commit.

## Verification Commands

```bash
python3 scripts/validate-document-lifecycle.py --root . --mode strict
python3 scripts/validate-links-and-owners.py --root . --mode strict
python3 scripts/archive_cutover.py --root .
python3 scripts/qa.py full
```

`full` owns unit discovery. No command here proves provider runtime or live
cluster behavior.

## Success Criteria & Verification Plan

| ID          | Criterion                                                                                      | Evidence                               |
| ----------- | ---------------------------------------------------------------------------------------------- | -------------------------------------- |
| VAL-SDR-001 | The fifteen decisions are retained with one catalog row each, and the lifecycle gate admits them | Lifecycle and archive gates            |
| VAL-SDR-002 | Current documents name them by identifier, and no current rule keeps a superseded decision in Stage 02 | Link gate and census                   |
| VAL-SDR-003 | The disposition evidence is recorded with no frozen byte changed                               | Task handoff record and full QA        |

## Traceability

[Implementation Plan](plan.md) owns order and risk, and the
[retention Task](tasks/tsk-0001-retain-superseded-decisions.md) owns the evidence.

### Lifecycle Traceability

| Requirement ID                              | Spec criterion | Verification method                        |
| ------------------------------------------- | -------------- | ------------------------------------------ |
| [REQ-0003-FR-0020](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-SDR-001    | Dispositions admitted by the lifecycle gate |
| [REQ-0003-FR-0012](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-SDR-002    | Consumer review                            |
| [REQ-0003-FR-0015](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-SDR-003    | Recorded evidence                          |
