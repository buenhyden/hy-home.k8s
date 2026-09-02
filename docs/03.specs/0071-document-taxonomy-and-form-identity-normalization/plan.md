---
title: 'Document Taxonomy and Form Identity Normalization Implementation Plan'
version: "1.0.0"
type: sdlc/plan
layer: "specs"
status: draft
owner: platform
updated: 2026-09-02
artifact_id: "SPEC-0071-PLAN-0001"
---

# Document Taxonomy and Form Identity Normalization Implementation Plan

## Global Constraints

- Change declaration and naming only. No document's stage, owner, lifecycle
  status, path, or meaning changes as a side effect.
- One taxonomy is live at a time. A partially applied rename is a `FAIL`, never
  a staged intermediate state, because the registry classifies every tracked
  Markdown file exactly once.
- Do not restate a grammar in a second owner. The registry owns per-profile key
  sets and order; the frontmatter schema owns per-key value grammar.
- A version normalization appends a patch component. It never renumbers,
  resets, or increments a document.
- Do not edit a sealed Stage 98 payload. Only the envelope frontmatter changes,
  and only where its generation contract changes with it.
- Perform every form relocation as a Git rename so history stays reachable.
- Retire a profile identity only after its last current consumer moves, and
  prove the retirement rather than asserting it.

## Overview

The work renames thirteen profiles, splits one into six, adds one runtime
binding profile, relocates twelve Stage 99 forms, rewrites three frontmatter
keys across the tracked corpus, makes the frontmatter value contract executable,
and re-pins the Stage 98 generation contracts that the frontmatter change
invalidates.

## Context

The identity work of SPEC-0067
already landed: `artifact_id` grammars, the `updated` key spelling, and the
absence of a `stage` key were verified as satisfied before this work began and
required no corpus change. What remained was the taxonomy above those
identities and the forms that produce them.

`frontmatter.schema.json` had no consumer. Two of the grammars it declared —
the `version` shape and the `layer` shape — had already drifted from the corpus
it governs, which is the direct evidence that a declared-only contract does not
hold.

## Goals & In-Scope

- One `family/kind` identity per profile, with `class` equal to family.
- A three-component `version` on every frontmatter-bearing document, and a
  stage-free `layer` slug wherever a numbered stage owns the document.
- One shared frontmatter key set and order, with the contractual exclusions
  stated rather than assumed: Stage 00 and Stage 99 declare no `layer`,
  `governance/*` declares no `artifact_id`, and a provider binding declares
  only the keys its runtime reads.
- Stage 99 forms named for their output, in one directory per owning stage,
  with the extension the consuming runtime reads.
- An executed frontmatter value contract with rejected-sample proof.
- Sealed Stage 98 records that parse against their own generation.

## Non-Goals & Out-of-Scope

- Renaming or renumbering any authored document outside Stage 99.
- Changing lifecycle state domains, transitions, or supersession semantics.
- Rendering agent projections from the registry — SPEC-0068.
- Retired-provider residue — SPEC-0070.
- Re-sealing, rewriting, or re-deriving archived payload bytes.

## Work Breakdown

| ID | Work package | Depends on | Entry gate | Exit evidence |
| --- | --- | --- | --- | --- |
| WP-001 | Audit the current corpus against every target contract and record what already holds | None | Approved Spec contracts C1–C10 | Measured identity, key, and grammar census |
| WP-002 | Rewrite profile identities, classes, form bindings, and lifecycle domain membership in the registry; widen the profile class domain | WP-001 | Census names every profile to rename | Registry projection over all profiles |
| WP-003 | Move the `version`, `layer`, and supersession grammars into the frontmatter schema and make `version` required there | WP-001 | Target grammars approved | Schema pattern assertions |
| WP-004 | Relocate and rewrite the Stage 99 forms, split the governance form into six, and author the Codex TOML form | WP-002 | Registry names each form's owning profile | Template parity check |
| WP-005 | Rewrite `type`, `layer`, `version`, and supersession values across the tracked corpus | WP-002, WP-003 | Registry and schema declare the targets | Strict profile and schema run over the corpus |
| WP-006 | Make the frontmatter value contract executable in the Markdown profile validator | WP-003 | Schema declares every authored key | Rejected-sample assertions for each retired grammar |
| WP-007 | Move every executable owner, comparison alias, and test onto the current identities | WP-002 | Registry identities are final | Retired-identity absence sweep and full suite |
| WP-008 | Make the Stage 98 generation contracts generation-aware, re-pin superseded digests, and seal the form moves as MIG-0010 | WP-004, WP-005 | Stage 98 frontmatter is final | Strict lifecycle run and sealed migration parse |
| WP-009 | Update the human owners: Stage 99 author guide, authoring policy, and the routers that name a form | WP-004 | Forms and identities are final | Strict link and owner run |
| WP-010 | Retire the Stage 03 package router: move Spec 0054's shared execution contract into its Plan, repoint every citation, derive the Task inventory from `tasks/`, and seal the retirement as MIG-0011 | WP-005, WP-008 | Approved Spec contract C11 | Package inventory sweep, strict link run, and delegated-execution projection check |
| WP-011 | Complete the Stage 90 structure: author the audits and data collection routers so all three collections carry the same three levels, each with one Stage 99 form | WP-004 | Approved Spec contract C12 | Reference-pack topology check and template parity |
| WP-012 | Correct the retirement controls to compare retired bytes instead of banning the retired path, and author the Stage 99 form catalog the corrected rule admits | WP-008 | Approved Spec contract C13 | Focused admission and resurrection cases plus the archive gate |

## Verification Plan

| Work package | Deterministic check | Lane |
| --- | --- | --- |
| WP-002, WP-004 | `scripts/validate-document-contract-registry.py --root . --mode strict` | repo-static |
| WP-004, WP-005, WP-006 | `scripts/validate-markdown-profiles.py --root . --mode strict` | repo-static |
| WP-009 | `scripts/validate-links-and-owners.py --root . --mode strict` | repo-static |
| WP-008 | `scripts/validate-document-lifecycle.py --root . --mode strict` | repo-static |
| WP-007 | `python3 -m unittest discover --start-directory tests --top-level-directory tests` | repo-static |
| WP-010 | `scripts/validate-agent-legacy-cutover.py --root .` | repo-static |
| WP-010, WP-011 | `bash scripts/validate-repo-quality-gates.sh .` | repo-static |
| All | `bash scripts/validate-repo-quality-gates.sh .` | repo-static |

No live cluster, provider runtime, or hosted CI evidence is claimed by this
work. Every check above reads tracked repository bytes only.

## Risks & Mitigations

| Risk | Mitigation | Owner |
| --- | --- | --- |
| A partially applied rename leaves documents unclassifiable | Registry, corpus, and executable owners land as one change; verification runs against the whole change | platform |
| A sealed Stage 98 digest is invalidated by the frontmatter change | Each prior digest moves into the superseded set and each parser selects the generation the digest names | platform |
| MIG-0004 pins a Stage 99 target that this work relocates | MIG-0010 seals the twelve moves; a sealed row naming a target as its own legacy path releases it | platform |
| A base-commit lifecycle comparison sees unknown profiles | The comparison alias table gains one entry per retired identity | platform |
| Enforcing a previously dead schema surfaces unrelated latent violations | Enforcement is scoped to authored profiles; template and provider-binding profiles are exempt by mode and class | platform |

## Completion Criteria

- Every criterion VAL-DTF-001 through VAL-DTF-009 has recorded evidence.
- Every verification command above has been run against the final change and
  its exact result recorded in the owning Task.
- No current document, executable owner, or test names a retired profile
  identity except as declared history.

## Traceability

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-DTF-001](spec.md#success-criteria--verification-plan) | WP-002 | [tsk-0001-dtf-000.md](tasks/tsk-0001-dtf-000.md) |
| [VAL-DTF-002](spec.md#success-criteria--verification-plan) | WP-005 | [tsk-0001-dtf-000.md](tasks/tsk-0001-dtf-000.md) |
| [VAL-DTF-003](spec.md#success-criteria--verification-plan) | WP-003, WP-005 | [tsk-0001-dtf-000.md](tasks/tsk-0001-dtf-000.md) |
| [VAL-DTF-004](spec.md#success-criteria--verification-plan) | WP-002 | [tsk-0001-dtf-000.md](tasks/tsk-0001-dtf-000.md) |
| [VAL-DTF-005](spec.md#success-criteria--verification-plan) | WP-004 | [tsk-0001-dtf-000.md](tasks/tsk-0001-dtf-000.md) |
| [VAL-DTF-006](spec.md#success-criteria--verification-plan) | WP-006 | [tsk-0001-dtf-000.md](tasks/tsk-0001-dtf-000.md) |
| [VAL-DTF-007](spec.md#success-criteria--verification-plan) | WP-008 | [tsk-0001-dtf-000.md](tasks/tsk-0001-dtf-000.md) |
| [VAL-DTF-008](spec.md#success-criteria--verification-plan) | WP-008 | [tsk-0001-dtf-000.md](tasks/tsk-0001-dtf-000.md) |
| [VAL-DTF-009](spec.md#success-criteria--verification-plan) | WP-007 | [tsk-0001-dtf-000.md](tasks/tsk-0001-dtf-000.md) |
| [VAL-DTF-010](spec.md#success-criteria--verification-plan) | WP-010 | [tsk-0001-dtf-000.md](tasks/tsk-0001-dtf-000.md) |
| [VAL-DTF-011](spec.md#success-criteria--verification-plan) | WP-010 | [tsk-0001-dtf-000.md](tasks/tsk-0001-dtf-000.md) |
| [VAL-DTF-012](spec.md#success-criteria--verification-plan) | WP-011 | [tsk-0001-dtf-000.md](tasks/tsk-0001-dtf-000.md) |
| [VAL-DTF-013](spec.md#success-criteria--verification-plan) | WP-012 | [tsk-0001-dtf-000.md](tasks/tsk-0001-dtf-000.md) |

### Related Documents

- [Technical contract](spec.md)
- [Current Spec Index](../README.md#current-spec-index)
- [Document Authoring Policy](../../00.agent-governance/policies/document-authoring.md)
- [Quality Policy](../../00.agent-governance/policies/quality.md)
