---
title: 'Transition Residue Retirement Technical Specification'
version: "1.0"
type: sdlc/spec
layer: "03.specs"
status: done
owner: platform
updated: 2026-08-31
artifact_id: "SPEC-0065"
---

# Transition Residue Retirement Technical Specification (Spec)

## Overview

Direct human approval on 2026-08-30 authorizes this standalone execution relation.
No separate PRD or Architecture Description is required or part of this standalone lifecycle.

Spec 0054 WP-012 closed with three residuals, each diagnosed and each refused by
a named clause. This Spec executes all three.

Two of them share one cause. `docs/99.templates/templates/governance/progress.template.md`
and `docs/99.templates/templates/governance/memory.template.md` are `moved`
targets of the sealed `MIG-0004`. `validate_mig0004_historical_targets` already
proves those moves against the pinned `WP004C_SEALED_TARGET_COMMIT`, which is
the recovery evidence. `_validate_mig0004_rows_and_targets` additionally
requires every Stage 99 target to be present in the current staged inventory,
so deleting either form raises `RECOVERY-MIGRATION-TARGET: current staged target
set differs`.

The third is independent. `Registry` declares no `route_state` field, so
`getattr(registry, "route_state", "terminal")` resolves to `"terminal"` on every
run. Five functions in `scripts/validate-links-and-owners.py` open with
`if context.route_state != "transition": return ...`, and five further branches
run only when it equals `"transition"`. None of them can execute.

## Strategic Boundaries & Non-goals

In scope: the three residuals Task SPEC-0054-TSK-0012 recorded, and only the owners
that state them.

Not in scope: `_document_taxonomy_transition_manifest` and
`scripts/document-taxonomy-migration.json`. Despite the manifest's `"state":
"transition"` field, the function is called unconditionally and its
`move_targets` output is one of the eight live projections composed in
`_historical_migration_proof`. It is a current redirect owner, not transition
residue.

Not in scope: the `MIG-0004` row census, its Stage 99 action-target map, or any
other pinned constant that proves the move itself. This work removes one
redundant current-tree requirement layered above that proof; it removes no
recovery evidence.

Not in scope: any other `governance/` profile, template, or Stage 00 directory.

## Contracts

- ADR-0030 places full archive content in Git history and admits a Tombstone
  only for a deleted path that needs a durable replacement owner.
- `docs/99.templates/registry.json` owns profiles and their routes. A profile
  that can route no path is not a classification, which is the ground MIG-0006
  used to retire three reference profiles.
- `scripts/document_lifecycle.py` refuses a governed Markdown deletion that no
  sealed migration admits.
- `validate_mig0004_historical_targets` remains the proof that each `MIG-0004`
  Stage 99 move was byte-identical, read at its pinned commit.

## Core Design

### The Stage 99 target release

A `MIG-0004` Stage 99 target that a later sealed migration row retires is
released from the current-staged-inventory requirement. Its move stays proved at
`WP004C_SEALED_TARGET_COMMIT`, and the retiring row carries its own source
commit, blob, and content digest. The requirement that it also remain checked
out proves nothing further about the past.

This is the third instance of one shape. MIG-0007 released a historical consumer
and this releases a move target; in both, a Git-side proof was paired with a
current-tree presence requirement that only froze the present.

### The retirement set

`progress.template.md` is the append fragment for the ledger MIG-0007 retired.
`memory.template.md` is the form for `docs/00.agent-governance/memory/`, whose
only document was that ledger. Three registry profiles route nothing once both
forms are gone: `governance/progress-ledger`, whose route matched exactly the
retired ledger; `governance/progress-entry`, whose route matched
`progress.template.md` and whose `appendContract` names the first as its parent;
and `governance/memory`, whose route matched only `memory/` documents.

`docs/00.agent-governance/memory/` is removed with them. Its README stated that
the directory holds no progress ledger and no memory document, and
`policies/context-and-memory.md` already owns the routing rule it repeated.

### Coverage narrowing

Each candidate is disabled and the suite is run. A rule whose removal fails no
test is already dead. A rule whose removal fails a test is read together with
that test, because the test states what it protects. The classification below is
an approval gate: the diagnosis is recorded before any retirement is staged.

## Data Modeling & Storage Strategy

`MIG-0008` is extended while still in draft to carry both forms, then sealed
together with their deletion. Each row records `source_commit`, `source_blob`,
and `content_sha256`, which is the recovery contract. No body is copied and no
Tombstone is created: ADR-0030 forbids one where a Migration and Git recovery
suffice, and neither form has a successor document.

## Interfaces & Data Structures

The registry's append-template parity rule names `governance/progress-entry` by
identity. With that profile retired the rule has no subject, so it becomes a
structural check over whatever append template a future registry declares.

## Edge Cases & Error Handling

Removing a `route_state` branch that is reachable is the primary risk. The
condition is proved structurally, by the absence of the field on the `Registry`
dataclass, rather than by inspection of call sites.

Removing the memory directory while a memory document exists would lose an
owner. The directory holds only its README, which this work rewrites away.

`_document_taxonomy_transition_manifest` reads a file whose `state` field says
`"transition"`. That field is data inside the manifest, not the registry's route
state, and the function is not gated on it.

## Failure Modes & Fallback / Human Escalation

Each retirement is one commit naming what it removes, so reversal is one
`git revert`. Deleted bytes remain in Git history at the commits MIG-0008
records.

If the Stage 99 release turns out to have removed a current invariant, the
failure surfaces as a gate or suite failure on the next cycle. If a retirement
removes a rule nothing tested and nothing protected, no signal appears, which is
the intended outcome.

Verification runs in a clean checkout. Results obtained in a linked worktree are
not evidence for the main checkout.

## Verification Commands

```bash
bash scripts/validate-repo-quality-gates.sh .
python3 scripts/validate-links-and-owners.py --root . --mode strict
python3 scripts/validate-document-lifecycle.py --root . --mode strict
python3 -m unittest discover --start-directory tests --top-level-directory tests --pattern 'test_*.py'
```

## Success Criteria & Verification Plan

| ID | Criterion |
| --- | --- |
| VAL-TRR-001 | Every retirement candidate is classified against the machine fact that decides it, and the classification is recorded before any retirement is staged |
| VAL-TRR-002 | No `route_state`-gated function or branch that cannot execute remains, and no live redirect owner is removed with them |
| VAL-TRR-003 | A `MIG-0004` Stage 99 target that a later sealed row retires is released from the current-inventory requirement, with every Git-side proof unchanged |
| VAL-TRR-004 | Both governance forms are retired through one sealed migration that keeps their recovery coordinates, and no inbound link breaks |
| VAL-TRR-005 | No registry profile routes zero paths, and `docs/00.agent-governance/memory/` is gone |
| VAL-TRR-006 | Gates and the full suite pass in a clean checkout at the branch tip |

## Traceability

This Spec has no PRD or AD. Its authority is the direct human approval recorded
in `## Overview`.

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| N/A — standalone, direct approval | VAL-TRR-001 | Classification table reviewed in the Task before retirement begins |
| N/A — standalone, direct approval | VAL-TRR-002 | `grep` for `route_state` compared against the `Registry` dataclass fields |
| N/A — standalone, direct approval | VAL-TRR-003 | RED-first case against the unreleased validator, then its passing result |
| N/A — standalone, direct approval | VAL-TRR-004 | Link validator run before and after deletion, with counts recorded |
| N/A — standalone, direct approval | VAL-TRR-005 | Registry route census and a tracked-path check for the directory |
| N/A — standalone, direct approval | VAL-TRR-006 | Gate and suite output recorded in the reciprocal Task |

### Related Documents

- [Plan](plan.md)
- [Task](tasks/tsk-0001-trr-000.md)
- [ADR 0022 — direct-approval standalone execution lineage](../../02.architecture/decisions/0022-direct-approval-standalone-execution-lineage.md)
- [ADR 0030 — authority-first SDLC and agent governance convergence](../../02.architecture/decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md)
