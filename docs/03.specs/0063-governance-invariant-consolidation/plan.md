---
title: 'Governance Invariant Consolidation Implementation Plan'
type: sdlc/plan
status: draft
owner: platform
updated: 2026-08-29
artifact_id: "PLAN-0063"
---

# Governance Invariant Consolidation Implementation Plan (Plan)

## Overview

This plan sequences the consolidation designed in
[Spec 0063](spec.md). The order is set by dependency, not by the order the
constraints were stated: the machinery that pins the archived copies is retired
before the copies are deleted, because deleting them first would fail the
validators still holding those pins.

## Context

Measured baseline on 2026-08-29, in a clean `main` checkout:

| Measure | Value |
| --- | --- |
| Markdown under `docs/` | 796 |
| `scripts/` lines | 68,282 |
| `tests/` lines | 35,464 |
| Distinct 40-hex pins in `scripts/` | 253 across 18 files |
| Constants bound to completed migrations | 141, of which 49 are pins |
| Rule identifiers in the retirement candidates | 376 |
| Retirement-candidate validator lines | 13,631 |
| Corresponding test lines | 9,795 |
| Full-body copies under `docs/98.archive/changes/` | 76 (1.4 MB) |
| Validators declared in the contract but not run by the gate | 2 |
| Validators run by the gate but not declared | 11 |

## Goals & In-Scope

Retire completed-migration machinery, relocate the current invariants inside it,
execute the ADR-0030 Stage 98 boundary, unify the contract and the gate, and
correct the authored documents the diagnosis proves stale.

## Non-Goals & Out-of-Scope

No reduction of invariants over the current tree. No change to completed Spec,
Plan, or Task records, dated research and audit snapshots, or pinned evidence
ledgers. No amendment of ADR-0030.

## Work Breakdown

### WP-001 — Diagnosis

Run the axes the 2026-08-29 measurement proved productive: contract-to-gate
wiring, path references inside governance JSON, prose enumerations against the
machine declaration, references to surfaces ADR-0030 removed, facts owned in
more than one place, and current documents citing superseded decisions.

Excluded as unproductive: template declarations and stage indexes, which the
standing validators already keep consistent, and `updated:` drift, which showed
548 of 667 files and carries no signal.

Output: a table of document, claim, machine fact, verdict, and disposition.
Verdicts are correct, archive, or preserve.

### WP-002 — Discard list

Classify each of the 376 rule identifiers by the mechanical test in the Spec.
Narrow the candidates by disabling each and running the suite. Record, for every
rule proposed to stay, the failure it prevents. This work package ends at an
approval gate.

### WP-003 — Retirement

One commit per validator, in dependency order: eligibility, retention,
migrations, role audit, residue closure. Relocate the current invariants first,
then delete. Reduce `validate-agent-legacy-cutover.py` to its retained guard
without disturbing its contract wiring.

### WP-004 — Stage 98 execution

Delete the 76 full-body copies, set their ledger `stable_path` to null, and
create Tombstones only where a durable replacement owner is needed.

### WP-005 — Contract and gate unification

Make the gate read the declared validator set from the contract, and add the
standing invariant that the executed set equals the declared set.

### WP-006 — Document and template correction

Apply the WP-001 dispositions and align SDLC terms and templates with the
consolidated contract.

## Verification Plan

After every commit, in a clean checkout, not a linked worktree:

```bash
bash scripts/validate-repo-quality-gates.sh .
python3 scripts/validate-agent-governance-closure.py --root .
python3 -m unittest discover -s tests
```

Source files are frozen for the duration of a suite run. The archive owner
loads its sibling link validator from disk at call time, so editing a validator
mid-run pairs a new file against an already-imported module and produces
import errors that are not regressions.

## Risks & Mitigations

| Risk | Mitigation |
| --- | --- |
| A retirement removes a current invariant | WP-002 approval gate; one commit per retirement; single-commit revert |
| A deletion loses content | All 76 rows carry `source_commit` and `source_blob`; Git holds the bodies |
| A worktree masks a filesystem check | Verify in a clean checkout only |
| Editing a byte-pinned consumer | Identify pinned paths before editing; move the pin or leave the file alone |
| Verification cost | One gate-and-suite pass takes about 20 minutes; batching per commit is cheaper than reverting a batch |

## Completion Criteria

The Spec criteria VAL-GIC-001 through VAL-GIC-006 hold, and the final commit
passes gates and the full suite in a clean checkout.

## Traceability

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-GIC-001](spec.md#success-criteria--verification-plan) | WP-001 diagnosis | [TSK-0063-0001](tasks/tsk-0001-gic-000.md) |
| [VAL-GIC-002](spec.md#success-criteria--verification-plan) | WP-002 discard list | [TSK-0063-0001](tasks/tsk-0001-gic-000.md) |
| [VAL-GIC-003](spec.md#success-criteria--verification-plan) | WP-003 retirement | [TSK-0063-0001](tasks/tsk-0001-gic-000.md) |
| [VAL-GIC-004](spec.md#success-criteria--verification-plan) | WP-004 Stage 98 execution | [TSK-0063-0001](tasks/tsk-0001-gic-000.md) |
| [VAL-GIC-005](spec.md#success-criteria--verification-plan) | WP-005 contract unification | [TSK-0063-0001](tasks/tsk-0001-gic-000.md) |
| [VAL-GIC-006](spec.md#success-criteria--verification-plan) | WP-006 document correction | [TSK-0063-0001](tasks/tsk-0001-gic-000.md) |

### Related Documents

- [Spec](spec.md)
- [Task](tasks/tsk-0001-gic-000.md)
