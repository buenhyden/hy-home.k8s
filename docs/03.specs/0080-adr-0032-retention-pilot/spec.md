---
title: "ADR-0032 Retention Pilot Technical Specification"
version: "0.1.0"
type: "sdlc/spec"
status: "active"
owner: "platform"
updated: "2026-09-15"
layer: "specs"
artifact_id: "SPEC-0080"
---

# ADR-0032 Retention Pilot Technical Specification (Spec)

## Overview

This Spec owns the first disposition under
[ADR-0038](../../02.architecture/decisions/0038-six-disposition-archive-stage.md):
ADR-0032, superseded by ADR-0038, leaves the decision log for `superseded/`.
It uses one real document to prove the machine path SPEC-0079 built, and it
closes the gaps the pilot exposed: a frozen Stage 98 link to the retained
source, and current consumers that still cited ADR-0032 as authority.

## Strategic Boundaries & Non-goals

Authorized scope is ADR-0032 and its current consumers (REQ-0003 and the
requirements index, AD-0006, AD-0007, ADR-0014, ADR-0030, ADR-0038, the SPEC-0054
Spec, Plan, and TSK-0013, the decision, Stage 03, and Stage 98 indexes, and the
`archive-cutover` skill), the link validator's historical-link admission, the
lifecycle regression fixture that read ADR-0032, and this package.

Explicit non-goals. The other fifteen superseded decisions stay in Stage 02, and
each needs its own disposition. No frozen record, ledger, retained package, or
frozen index row changes. Citations that predate ADR-0038 acceptance and do not
name ADR-0032 are not rewritten. No live cluster, provider runtime, or network
action is authorized.

## Contracts

- ADR-0032 is retained at its mirrored path under `superseded/` with its
  profile, identity, and terminal state, and its body differs from the source
  by relative link prefixes alone.
- The Stage 98 index carries one Retention Catalog row naming the record and
  `<commit>:<original path>` for the comparison base.
- A current document cites ADR-0038 as the successor or names ADR-0032 by
  identifier; the decision index names it by identifier and routes to the
  archive index. A statement that uses ADR-0032 as a present rule or a future
  directive moves to ADR-0038, while dated history, past commit lists, and
  finished work-package dependencies keep naming ADR-0032.
- A link held by frozen Stage 98 content to a path a catalog row retained is
  historical evidence and resolves through that row; a current document gets no
  such admission.

## Core Design

Frozen ledgers MIG-0017, MIG-0018, and MIG-0022 link ADR-0032 and cannot be
rewritten. The link validator admits such a link only when the source is under
Stage 98, a catalog row names the target as its original path, and the record
the row names exists. The catalog already names that path, so the admission
adds no second ledger.

## Data Modeling & Storage Strategy

The only new data is one catalog row. The retained body keeps its frontmatter
and its content, with relative link prefixes re-based.

## Interfaces & Data Structures

`_catalog_retained_link` in the link validator and the Retention Catalog parser
in `scripts/archive_dispositions.py`. No rule identifier is added.

## Edge Cases & Error Handling

A catalog with a structure error proves no link. A link from a current document
to the retained source still fails, so the consumer must cite the successor.

## Failure Modes & Fallback / Human Escalation

If the pilot cannot pass the gates without rewriting frozen content, it stops
and returns to the request owner. The disposition reverts with its commit.

## Verification Commands

```bash
python3 scripts/validate-links-and-owners.py --root . --mode strict
python3 scripts/validate-document-lifecycle.py --root . --mode strict
python3 scripts/archive_cutover.py --root .
python3 scripts/qa.py full
```

`full` owns unit discovery. No command here proves provider runtime or live
cluster behavior.

## Success Criteria & Verification Plan

| ID          | Criterion                                                                                                            | Evidence                              |
| ----------- | -------------------------------------------------------------------------------------------------------------------- | ------------------------------------- |
| VAL-ARP-001 | ADR-0032 is retained under `superseded/` with one catalog row, and the lifecycle gate admits it                      | Lifecycle and archive gates           |
| VAL-ARP-002 | Frozen Stage 98 links to the retained source resolve through the catalog, and current links do not                   | Link gate and link regressions        |
| VAL-ARP-003 | No current document cites ADR-0032 as its present rule, dated history stays, and the `archive-cutover` skill follows ADR-0038 | Link gate and plain-text citation census |
| VAL-ARP-004 | Link-rebase equivalence and the derived frozen-generation fixture close the SPEC-0079 residual risks, with evidence | Task handoff record and unit discovery |

## Traceability

[Implementation Plan](plan.md) owns order and risk, and the
[pilot Task](tasks/tsk-0001-retain-adr-0032.md) owns the execution evidence.

### Lifecycle Traceability

| Requirement ID                            | Spec criterion | Verification method                        |
| ----------------------------------------- | -------------- | ------------------------------------------ |
| [REQ-0003-FR-0020](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ARP-001    | Disposition admitted by the lifecycle gate |
| [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ARP-002    | Frozen links resolved without rewriting    |
| [REQ-0003-FR-0012](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ARP-003    | Consumer and skill review                  |
| [REQ-0003-FR-0015](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ARP-004    | Recorded residual-risk closure             |
