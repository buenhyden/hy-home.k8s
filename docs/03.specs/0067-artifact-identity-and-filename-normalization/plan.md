---
title: 'Artifact Identity and Filename Normalization Implementation Plan'
version: "1.0"
type: sdlc/plan
layer: "03.specs"
status: done
owner: platform
updated: 2026-09-01
artifact_id: "SPEC-0067-PLAN-0001"
---

# Artifact Identity and Filename Normalization Implementation Plan

## Global Constraints

- Change declaration and naming only. No stage membership, ownership,
  lifecycle status, or rule meaning changes as a side effect.
- One convention is live at a time. A partially applied identity change is a
  `FAIL`, never a staged intermediate state.
- Do not restate an identity pattern in a second owner. The registry profile
  owns the per-type pattern and the frontmatter schema owns the union.
- Preserve reachable Git history: perform renames as Git renames.
- Do not edit a sealed Stage 98 payload. A tombstone envelope may change only
  where its derivation owner changes with it.
- Do not change any machine-loaded path: Stage 00 governance documents, Stage
  99 template files, hook targets, and provider configuration paths stay.
- Retire a legacy or deprecated identity form only after its last current
  consumer moves, and prove the retirement rather than asserting it.

## Overview

The work replaces four identity patterns, introduces three, normalizes the
numbered leaf filenames that carry them, and updates the templates and
validators that own those forms. It then removes the retired forms and
verifies that no drift between owner, template, corpus, and test remains.

## Context

Stage 05 guides, policies, runbooks, and Stage 98 migrations already satisfy
the target and need verification only. Stage 03 Plans and Tasks, Stage 90
reference members, and Stage 98 tombstones do not. Stage 90 members carry no
identity at all, and tombstone identity is a content digest that
`scripts/archive_recovery.py` derives as part of its archive recovery proof.

## Goals & In-Scope

- One identity pattern per governed profile, declared at a single owner.
- Composite identities that name the parent and the sequence within it.
- Numbered leaf filenames that begin with their number, preserving the Task
  `tsk-####-` and Stage 90 `m####-` authoring prefixes.
- Templates that show each stage the form it must author.
- Retirement of the superseded identity forms and their prose references.

## Non-Goals & Out-of-Scope

- Renaming Stage 00 governance documents or Stage 99 template files.
- Renumbering an existing parent artifact or closing a numbering gap.
- Changing validation rule semantics beyond identity and filename.
- Re-sealing, rewriting, or re-deriving archived payload bytes.

## Work Breakdown

| ID | Work package | Depends on | Acceptance |
| --- | --- | --- | --- |
| WP-001 | Capture the point-in-time identity and filename baseline, and confirm which stages already conform | None | Per-stage conforming and non-conforming counts, machine-loaded path inventory, and no mutation |
| WP-002 | Move the Stage 03 Plan and Task identity patterns and the corpus that presents them | WP-001 | Registry, schema, 54 Plans, and 343 Tasks present the target form; no retired form remains |
| WP-003 | Move the Stage 05 incident and postmortem patterns and verify the already-conforming forms | WP-001 | Target incident and postmortem patterns declared; guide, policy, and runbook identities unchanged and still valid |
| WP-004 | Introduce Stage 90 pack member identity | WP-001 | Every pack member presents a unique member identity within its pack |
| WP-005 | Move Stage 98 tombstone identity and its derivation owner | WP-001 | Derivation emits the parent-derived identity, collisions fail closed, and recovery still proves the pinned legacy tree |
| WP-006 | Normalize numbered leaf filenames | WP-002, WP-004, WP-005 | Numbered leaf filenames begin with their number, the two authoring prefixes are preserved, and Git recognizes renames |
| WP-007 | Update Stage 99 templates to the target authoring forms | WP-002, WP-003, WP-004, WP-005 | Each template presents its stage's identity form and domain key as placeholders under one frontmatter guide; no template restates a validator rule |
| WP-008 | Retire legacy and deprecated identity forms, remove identifiers from titles, and reconcile prose references | WP-002..WP-007 | No current document, validator, test, or contract names a retired form outside a sealed payload, and no title repeats its own identifier |
| WP-009 | Sweep for drift between owner, template, corpus, and test, then complete the ordered validation sequence | All | One owner per pattern, no second constant, and the complete ordered sequence passes over the final bytes |

## Verification Plan

Each work package runs its focused validator or suite first, then the affected
lane for its changed paths. WP-009 runs the complete ordered sequence from the
quality policy over the final bytes and records each lane result separately.

Renames are verified as Git renames, not as delete-and-add pairs. Tombstone
work additionally re-runs the archive recovery and validation suites, because
identity there is a recovery proof rather than a label.

## Risks & Mitigations

| Risk | Mitigation |
| --- | --- |
| A tombstone derivation collides for two archived versions of one original | Fail closed in the derivation and escalate; never invent a disambiguator |
| A prose reference to a retired identity survives silently | Make the retirement sweep a diagnostic, not a manual read |
| A rename breaks a machine-loaded path | Keep Stage 00 and Stage 99 paths out of scope and assert their stability |
| A pattern is restated in a validator constant and drifts | WP-009 sweeps for a second owner rather than trusting review |
| A partially applied change leaves two conventions live | Treat any retired form outside a sealed payload as `FAIL` |

## Completion Criteria

Every Spec criterion holds, the retired forms are gone with proof, no drift
remains between the registry, schema, templates, corpus, validators, and tests,
and the complete ordered validation sequence passes over the final bytes in a
clean checkout. Renames are reachable through Git. This Plan and its Task then
move to their terminal states.

## Traceability

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-AIF-001](spec.md#success-criteria--verification-plan) | WP-001 | [SPEC-0067-TSK-0001](tasks/tsk-0001-aif-000.md) |
| [VAL-AIF-002](spec.md#success-criteria--verification-plan) | WP-002 | [SPEC-0067-TSK-0001](tasks/tsk-0001-aif-000.md) |
| [VAL-AIF-003](spec.md#success-criteria--verification-plan) | WP-003 | [SPEC-0067-TSK-0001](tasks/tsk-0001-aif-000.md) |
| [VAL-AIF-004](spec.md#success-criteria--verification-plan) | WP-004 | [SPEC-0067-TSK-0001](tasks/tsk-0001-aif-000.md) |
| [VAL-AIF-005](spec.md#success-criteria--verification-plan) | WP-005 | [SPEC-0067-TSK-0001](tasks/tsk-0001-aif-000.md) |
| [VAL-AIF-006](spec.md#success-criteria--verification-plan) | WP-006 | [SPEC-0067-TSK-0001](tasks/tsk-0001-aif-000.md) |
| [VAL-AIF-007](spec.md#success-criteria--verification-plan) | WP-001, WP-006 | [SPEC-0067-TSK-0001](tasks/tsk-0001-aif-000.md) |
| [VAL-AIF-008](spec.md#success-criteria--verification-plan) | WP-007 | [SPEC-0067-TSK-0001](tasks/tsk-0001-aif-000.md) |
| [VAL-AIF-009](spec.md#success-criteria--verification-plan) | WP-008 | [SPEC-0067-TSK-0001](tasks/tsk-0001-aif-000.md) |
| [VAL-AIF-010](spec.md#success-criteria--verification-plan) | WP-009 | [SPEC-0067-TSK-0001](tasks/tsk-0001-aif-000.md) |
| [VAL-AIF-011](spec.md#success-criteria--verification-plan) | WP-003, WP-004, WP-007, WP-008 | [SPEC-0067-TSK-0001](tasks/tsk-0001-aif-000.md) |
| [VAL-AIF-012](spec.md#success-criteria--verification-plan) | WP-007, WP-008 | [SPEC-0067-TSK-0001](tasks/tsk-0001-aif-000.md) |

### Related Documents

- [Spec](spec.md)
- [Package router](README.md)
- [Quality Policy](../../00.agent-governance/policies/quality.md)
- [Git Policy](../../00.agent-governance/policies/git.md)
