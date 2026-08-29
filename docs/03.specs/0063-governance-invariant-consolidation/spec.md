---
title: 'Governance Invariant Consolidation Technical Specification'
type: sdlc/spec
status: active
owner: platform
updated: 2026-08-30
artifact_id: "SPEC-0063"
---

# Governance Invariant Consolidation Technical Specification (Spec)

## Overview

Direct human approval on 2026-08-29 authorizes this standalone execution relation.
No separate PRD or Architecture Description is required or part of this standalone lifecycle.

The repository spends more code proving its documents than it has documents.
Measured on 2026-08-29: 796 Markdown files under `docs/`, against 68,282 lines
in `scripts/`, 35,464 in `tests/`, 253 distinct 40-hex commit pins across 18
script files, and a single validator of 8,501 lines. Of that, 141 constants are
bound to migrations that already completed, 49 of them commit, blob, or digest
pins.

That imbalance is not merely cost. A pin fixed to a past commit fails when
history advances past it, so the checks most likely to break are the ones that
protect work already finished. Every gate failure observed during the
2026-08-29 convergence cycle belonged to that class: an append-only ledger
pinned to exact bytes in three separate owners, a file pinned by line position,
a sealed-tree comparison, and a date duplicated between frontmatter and a
router index.

This specification consolidates those invariants. It retires the machinery that
proves completed migrations, keeps and relocates the rules that examine the
current tree, executes the Stage 98 boundary ADR-0030 already accepted, and
makes the divergence between the declared contract and the executed gate
structurally impossible rather than merely detected.

## Strategic Boundaries & Non-goals

In scope: the seven validators bound to completed migrations, the 76 full-body
copies under `docs/98.archive/changes/`, the wiring between
`docs/00.agent-governance/contracts/validation-surfaces.json` and
`scripts/validate-repo-quality-gates.sh`, and the authored documents whose
claims the diagnosis proves stale.

Not in scope: the invariants that examine the current tree. Secret handling,
GitOps and manifest structure, document profiles and registry routing, link and
owner integrity, agent roster and harness contracts, the CI Python contract,
Actions security, Vault/ESO contracts, and the workspace boundary all remain.
This work reduces what is proved about the past, never what is proved about the
present.

Also not in scope: completed Spec, Plan, and Task records, dated research and
audit snapshots, and pinned evidence ledgers. These describe a past state, so
differing from the present is correct rather than stale.

## Contracts

`docs/00.agent-governance/contracts/validation-surfaces.json` becomes the sole
owner of which validators run. `scripts/validate-repo-quality-gates.sh` becomes
a projection of that declaration rather than a parallel authority.

ADR-0030 governs the Stage 98 boundary and is executed, not amended: Stage 98
holds README, Migration, and necessary Tombstone records, and Git history is
the full-content archive.

## Core Design

### Classification rule

One question decides each rule: does it examine the current tree, or a past
migration. The question reduces to a mechanical test on the rule's inputs, so
judgment does not enter.

| Verdict | Mechanical test | Disposition |
| --- | --- | --- |
| Completed-migration proof | Reads a hardcoded commit, blob, or digest constant, or reads a fixed past commit through Git | Retire |
| Current invariant | Reads only the working tree, index, `HEAD`, or a current contract | Relocate to a standing validator |
| Mixed | Reads both | Split, relocate the current half |

### Coverage narrowing

Classifying 376 rule identifiers by reading is not reproducible. Each candidate
rule is disabled and the suite is run: a rule whose removal fails no test is
already dead and retires without further argument. A rule whose removal fails a
test is read together with that test, and the test states what it protects.

### Single-owner principle

Every defect this cycle found had the same shape: one fact owned in two places
with manual synchronization between them. The consolidation removes the second
owner rather than adding a check that compares them.

## Data Modeling & Storage Strategy

The 76 documents under `docs/98.archive/changes/` appear in the migration
ledgers only as `stable_path`, and all 76 rows carry both `source_commit` and
`source_blob`. Deleting the copies therefore cannot lose content: the recovery
coordinates remain in the ledger and Git holds the bodies. The rows are kept
with `stable_path` set to null, because `legacy_path`, `source_commit`, and
`source_blob` are the recovery contract.

Tombstones are created only for paths that need a durable replacement owner.
ADR-0030 forbids one Tombstone per source where a Migration and Git recovery
suffice.

## Interfaces & Data Structures

The gate script reads the validator declarations from the contract and executes
them. A validator is added or removed by editing the contract alone.

## Edge Cases & Error Handling

A retirement that removes a current invariant is the primary risk. The discard
list is an approval gate: implementation of the retirement does not begin until
the classified list is approved.

The `retired_document_owner` guard in `scripts/validate-agent-legacy-cutover.py`
maps retired document forms to their successor profile and rejects edits to
them. It holds zero live targets by design, which is its success condition and
not evidence that it is dead. It is retained.

Documents that already carry an explicit non-authoritative disclaimer, such as
`docs/01.requirements/0003-workspace-agent-governance-platform.md` and
`docs/02.architecture/descriptions/0006-workspace-agent-governance-platform.md`,
are preserved records with removal already deferred to WP-003. Treating them as
stale would destroy a deliberate record.

## Failure Modes & Fallback / Human Escalation

Each retirement is one commit naming the rule identifiers it removes, so
reversal is a single `git revert`. Deleted validators remain in Git history.

If a retirement turns out to have removed a current invariant, the failure
surfaces as a gate or suite failure on the next cycle, and the revert restores
it. If a retirement instead removes a rule nothing tested and nothing protected,
no signal appears, which is the intended outcome.

Verification runs in a clean checkout. The 2026-08-29 cycle established that a
linked worktree can retain untracked residue that masks filesystem-existence
checks, so results obtained in a worktree are not evidence for the main
checkout.

## Verification Commands

```bash
bash scripts/validate-repo-quality-gates.sh .
python3 scripts/validate-agent-governance-closure.py --root .
python3 -m unittest discover -s tests
```

## Success Criteria & Verification Plan

| ID | Criterion |
| --- | --- |
| VAL-GIC-001 | The diagnosis records every finding with the machine fact it contradicts |
| VAL-GIC-002 | The discard list classifies each candidate rule and is approved before retirement |
| VAL-GIC-003 | Commit-bound constants for completed migrations are removed |
| VAL-GIC-004 | `docs/98.archive/changes/` holds no full-body copies and no ledger row loses its recovery coordinates |
| VAL-GIC-005 | Every validator the contract declares required is executed by at least one runner, and a required validator with no runner is refused |
| VAL-GIC-006 | Gates and the full suite pass in a clean checkout after every commit |

VAL-GIC-005 was revised during execution. As first written it required the gate
to execute exactly the contract's validator set. Two measurements disproved that
premise. The contract is a lane-selection contract, not a validator registry:
the gate runs six validators it does not declare, including
`validate-affected-surfaces.py`, which validates the contract itself. And CI
runs three validator jobs behind separate path filters, so sixteen validators
appear in two runners deliberately — a validator listed in only one would leave
a hole for one class of change. The revised criterion states the invariant that
actually protects coverage, and `SURFACE-VALIDATOR-RUNNER` enforces it.

## Traceability

This Spec has no PRD or AD. Its authority is the direct human approval recorded
in `## Overview`.

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| N/A — standalone, direct approval | VAL-GIC-001 | Diagnosis table reviewed against the cited contracts |
| N/A — standalone, direct approval | VAL-GIC-002 | Approval recorded in the Task before retirement begins |
| N/A — standalone, direct approval | VAL-GIC-003 | Count of 40-hex constants in `scripts/` compared to the baseline |
| N/A — standalone, direct approval | VAL-GIC-004 | Ledger rows parsed for recovery coordinates after deletion |
| N/A — standalone, direct approval | VAL-GIC-005 | `SURFACE-VALIDATOR-RUNNER` fails when a required validator has no runner |
| N/A — standalone, direct approval | VAL-GIC-006 | Gate and suite output recorded in the reciprocal Task |

### Related Documents

- [Plan](plan.md)
- [Task](tasks/tsk-0001-gic-000.md)
- [ADR 0022 — direct-approval standalone execution lineage](../../02.architecture/decisions/0022-direct-approval-standalone-execution-lineage.md)
- [ADR 0030 — authority-first SDLC and agent governance convergence](../../02.architecture/decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md)
