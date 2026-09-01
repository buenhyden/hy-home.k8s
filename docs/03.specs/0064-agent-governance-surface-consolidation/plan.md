---
title: 'Agent Governance Surface Consolidation Implementation Plan'
type: sdlc/plan
status: done
owner: platform
updated: 2026-08-30
artifact_id: "SPEC-0064-PLAN-0001"
---

# Agent Governance Surface Consolidation Implementation Plan (Plan)

## Overview

This Plan executes [Spec 0064](spec.md) in four work packages plus verification.
Each package names the owner that states the wrong fact, the machine check that
proves the correction, and the point at which the package stops if the proof
fails.

## Context

Spec 0063 consolidated the document stages and left the agent-governance
surfaces untouched. This execution audits those surfaces on the same six axes
and corrects what it finds. Two lessons from that execution bind this one. A
sweep is reported with its rejected candidates, because the first form of a
sweep is usually wrong. And a validator that refuses a change is the authority
on whether the change was correct, not the prose that motivated it.

## Goals & In-Scope

- Retire the progress ledger to a minimal Stage 98 tombstone.
- Remove instructions that name unowned paths.
- Remove unreferenced scaffolding.
- Record the diagnosis, including the rejected candidates.

## Non-Goals & Out-of-Scope

- The eight rejected candidates listed in the Spec.
- Spec 0054's remaining retirement scope beyond the ledger artifact.
- Any push, merge, or remote operation.
- Any change that proves provider runtime behavior.

## Work Breakdown

### WP-001 Diagnosis

Record the audit in [SPEC-0064-TSK-0001](tasks/tsk-0001-ags-000.md): three defects
and eight rejected candidates, each with the command whose output decided it.
The rejected candidates carry the reason the first sweep form was wrong, being
a basename match that missed composed paths, and a per-module constant read that
missed cross-module imports.

Verify: the Task table lists eight rejected candidates with their deciding fact.

### WP-002 Progress ledger retirement

This package is two changes, because a migration document may only be created
mutable and `LIFECYCLE-DELETE` reads only sealed rows.

1. Prove the redirect first. Author
   `docs/98.archive/migrations/0007-progress-ledger-retirement.md` in `draft`
   with one ledger row carrying `legacy_path`, the source commit, the source
   blob, and the content digest of the ledger.
2. Seal the row and delete `docs/00.agent-governance/memory/progress.md` in the
   same change. Run the link validator before staging the deletion and confirm
   the eight terminal citations resolve through the sealed row.
3. Update `docs/00.agent-governance/memory/README.md` and
   `docs/00.agent-governance/policies/context-and-memory.md` to name the
   tombstone as the historical owner.
4. Repoint the four Stage 90 audit references, which are `draft` and mutable.
5. Record the ownership transfer in Spec 0054's Task, which is `active`.

Stop condition: if the link validator still reports a broken citation from a
terminal document, do not stage the deletion. Correct the ledger contradiction
only, keep the body, and record the residual.

Verify: `validate-links-and-owners.py` and `validate-document-lifecycle.py` both
pass with the deletion staged, and no `LINK-BROKEN` names the retired path.

### WP-003 Unowned path instruction

Remove `docs/05.operations/playbooks/` from
`.agents/skills/ops-runbook/skill.md` at both offering sites, leaving
`docs/05.operations/runbooks/` as the only save location.

Verify: no tracked file under the four surfaces cites a `docs/` path that the
tree does not contain, excluding placeholder patterns and the archived ledger.

### WP-004 Unreferenced scaffolding

Remove `.codex/rules/`, which holds one `.gitkeep` and has no reference in the
repository.

Verify: the consumer sweep reports no unreferenced tracked artifact in the four
surfaces.

### WP-005 Verification

Run the gate and the full suite from a clean clone of the branch tip rather than
from the linked worktree, and record both results in the Task with their counts.

## Verification Plan

| Work package | Command | Expected |
| --- | --- | --- |
| WP-001 | Diagnosis review against the Task table | Eight rejected candidates recorded |
| WP-002 | `python3 scripts/validate-links-and-owners.py --root . --mode strict --body-contracts registry` | `PASS CROSS-DOCUMENT` with the deletion staged |
| WP-002 | `python3 scripts/validate-document-lifecycle.py --root . --mode strict` | `PASS lifecycle validation mode=strict` |
| WP-003 | Cited-path resolution over the four surfaces | No unowned `docs/` target |
| WP-004 | Consumer sweep over the four surfaces | No unreferenced artifact |
| WP-005 | `bash scripts/validate-repo-quality-gates.sh .` | exit 0, no failures |
| WP-005 | `python3 -m unittest discover --start-directory tests --top-level-directory tests --pattern 'test_*.py'` | exit 0 |

## Risks & Mitigations

The eight terminal citations are the material risk. They cannot be edited, so
the redirect is proved before the deletion is staged and the package stops if
the proof fails.

Spec 0054 owns the wider progress-owner retirement. The transfer of this one
artifact is recorded in both Specs rather than assumed.

The tombstone must not become a body copy or a redirect document. It carries
recovery coordinates only, because Git history is the archive.

## Completion Criteria

All five criteria in [Spec 0064](spec.md#success-criteria--verification-plan)
are met, or an unmet criterion is recorded in
[SPEC-0064-TSK-0001](tasks/tsk-0001-ags-000.md) with the fact that blocked it.

## Traceability

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-AGS-001](spec.md#success-criteria--verification-plan) | WP-001 diagnosis | [SPEC-0064-TSK-0001](tasks/tsk-0001-ags-000.md) |
| [VAL-AGS-002](spec.md#success-criteria--verification-plan) | WP-002 ledger retirement | [SPEC-0064-TSK-0001](tasks/tsk-0001-ags-000.md) |
| [VAL-AGS-003](spec.md#success-criteria--verification-plan) | WP-003 unowned path | [SPEC-0064-TSK-0001](tasks/tsk-0001-ags-000.md) |
| [VAL-AGS-004](spec.md#success-criteria--verification-plan) | WP-004 scaffolding | [SPEC-0064-TSK-0001](tasks/tsk-0001-ags-000.md) |
| [VAL-AGS-005](spec.md#success-criteria--verification-plan) | WP-005 verification | [SPEC-0064-TSK-0001](tasks/tsk-0001-ags-000.md) |

### Related Documents

- [Spec](spec.md)
- [Task](tasks/tsk-0001-ags-000.md)
