---
title: 'Artifact Identity and Filename Normalization Technical Specification'
version: "1.0.0"
type: sdlc/spec
layer: "specs"
status: done
owner: platform
updated: 2026-09-01
artifact_id: "SPEC-0067"
---

# Artifact Identity and Filename Normalization Technical Specification (Spec)

## Overview

Current artifact identity is inconsistent across stages. A Stage 03 Task
identity encodes its parent Spec number positionally but not by type, a Stage
03 Plan identity omits its parent entirely, Stage 90 reference members carry no
identity at all, and Stage 98 tombstones carry a content-addressed digest that
no reader can relate to the document it replaces.

This Spec makes every governed identity name its own type and its parent, and
makes numbered leaf filenames start with the number they carry. It changes
declaration and naming only. No stage gains or loses a document, and no
validation rule changes meaning beyond the identity and filename contracts.

Measured counts below are point-in-time audit evidence. They are not permanent
governance invariants.

## Strategic Boundaries & Non-goals

In scope: the identity pattern for Stage 03 Plans and Tasks, Stage 05
operations documents, Stage 90 reference packs, and Stage 98 archive records;
the filename rule for numbered leaf documents; the owning registry profiles,
frontmatter schema, Stage 99 templates, validators, and tests; and the existing
corpus that those contracts govern.

Out of scope: document content, stage membership, ownership, lifecycle status,
approval routing, the Stage 00 governance corpus and Stage 99 template files
themselves, which carry no artifact identity and whose paths are loaded by
machine configuration.

### Authority and Ownership

| Concern | Owner |
| --- | --- |
| Identity pattern per profile | `docs/99.templates/registry.json` |
| Union frontmatter identity pattern | `docs/99.templates/contracts/frontmatter.schema.json` |
| Per-stage authoring form | `docs/99.templates/templates/**` |
| Tombstone identity derivation and recovery proof | `scripts/archive_recovery.py` |
| Corpus conformance diagnostics | document contract and Markdown validators |
| Execution evidence and rollback | this package's Task and reachable Git |

## Contracts

### Identity

| Stage | Profile | Current | Target |
| --- | --- | --- | --- |
| 03.specs | `sdlc/plan` | `PLAN-####` | `SPEC-####-PLAN-####` |
| 03.specs | `sdlc/task` | `TSK-####-####` | `SPEC-####-TSK-####` |
| 05.operations | `sdlc/guide` | `GDE-####` | `GDE-####` |
| 05.operations | `sdlc/incident` | `INC-####-####` | `inc-<year>-####` |
| 05.operations | `sdlc/postmortem` | `POSTMORTEM-####-####` | `inc-<year>-####-PM` |
| 05.operations | `sdlc/policy` | `POL-####` | `POL-####` |
| 05.operations | `sdlc/runbook` | `RUN-####` | `RUN-####` |
| 90.references | audit pack member | none | `AUD-####-m####` |
| 90.references | research pack member | none | `RES-####-m####` |
| 90.references | data pack member | none | `DATA-####-m####` |
| 98.archive | migration | `MIG-####` | `MIG-####` |
| 98.archive | tombstone | `TMB-<TYPE>-LEGACY-<digest>` | `tomb-<TYPE>-####` |

The trailing group in a composite identity is the sequence inside the parent,
not a repetition of the parent number. A parent owns its own numbering.

### Domain identity keys

A family whose documents are addressed by a domain identifier presents that
identifier beside `artifact_id` and carries the same value. Stage 98 migrations
already do this with `migration_id`, and the same shape extends to the families
below. The domain key names how the family refers to itself; `artifact_id`
names how governance refers to it.

| Family | Domain key | Value |
| --- | --- | --- |
| Stage 05 incident | `incident_id` | equal to `artifact_id` |
| Stage 05 postmortem | `incident_id` | equal to `artifact_id` |
| Stage 90 audits member | `audit_id` | equal to `artifact_id` |
| Stage 90 research member | `research_id` | equal to `artifact_id` |
| Stage 90 data member | `data_id` | equal to `artifact_id` |
| Stage 98 migration | `migration_id` | equal to `artifact_id` |

Two keys that carry the same role are consolidated rather than multiplied.
`type` already names the document's profile, so no separate `profile` key is
introduced; a family without domain addressing presents `artifact_id` alone.
The recency key is `updated`, and no `last-updated` spelling is admitted. A key
that no document presents is retired from the schema rather than kept
available, because an admitted but unused key is a form that will drift.

### Title boundary

`artifact_id` owns the document's identity, so `title` never repeats it. A
title that carries its own identifier duplicates a value with one owner and
drifts the moment that owner changes. Titles state what the document is.

### Template authoring form

A Stage 99 template presents the frontmatter its stage must author, using
placeholders rather than real values: `title`, `type`, `status`, `owner`,
`updated`, the family's `artifact_id`, and its domain key when the family has
one. Templates express form, never a validator rule.

### Filenames

A leaf document whose identity carries a number begins its filename with that
number. Two authoring forms are preserved: a Stage 03 Task keeps its
`tsk-####-` prefix, and a Stage 90 pack member uses the `m####-` prefix that
matches its member sequence. A document with no artifact identity keeps its
name, because that name is itself the contract its machine consumers load.

## Core Design

Identity is declared once per profile and enforced twice: the registry profile
owns the per-type pattern, and the frontmatter schema owns the union that any
governed document may present. Templates express the same form for authors.
No validator restates a pattern in prose or in a second constant.

Tombstone identity moves from a content digest to a parent-derived name. The
archive recovery owner keeps deriving the identity rather than reading it, so
the archive still proves it matches the pinned legacy tree; only the derivation
rule changes. Because legacy payloads carry no identity of their own, the
derivation reads the recorded `original_type` and the number in
`original_path`.

## Data Modeling & Storage Strategy

No storage changes. Identity remains a frontmatter scalar, and the corpus
remains plain Markdown in Git. Renames are Git renames so history stays
reachable through ordinary tooling.

## Interfaces & Data Structures

| Interface | Change |
| --- | --- |
| `registry.json` profile `artifactIdPattern` | Replace the Stage 03 Plan/Task and Stage 05 incident/postmortem patterns; add Stage 90 pack member patterns; replace the tombstone pattern |
| `frontmatter.schema.json` identity union | Replace the corresponding alternatives |
| Stage 99 templates | Present the target identity for every stage that has one |
| `archive_recovery.py` tombstone identity | Derive `tomb-<TYPE>-####` from the recorded original type and path |

## Edge Cases & Error Handling

A legacy tombstone payload carries no identity, so the derivation must not read
one. Two archived versions of the same original document would derive the same
identity; the migration must detect that collision and fail rather than emit a
duplicate. A Stage 90 pack member sequence must be stable across a rename, so
the member number is assigned once and never renumbered to close a gap. A
prose reference to an old identity that survives the migration is a defect,
not acceptable residue, except inside a sealed Stage 98 payload.

## Failure Modes & Fallback / Human Escalation

A partially applied identity change leaves two conventions live and is a
`FAIL`, not a staged state. If the tombstone derivation cannot produce a unique
identity for the current archive, the archive work package stops and escalates
rather than inventing a disambiguator. If a machine-loaded path would change,
the change is out of scope and escalates.

## Verification Commands

```bash
python3 -m unittest tests.test_document_strict_cutover
python3 -m unittest tests.test_archive_recovery tests.test_archive_validation
python3 scripts/validate-document-contract-registry.py --root . --mode strict
python3 scripts/validate-markdown-profiles.py --root . --mode strict
python3 scripts/validate-links-and-owners.py --root . --mode strict
python3 scripts/validate-document-lifecycle.py --root . --mode strict
python3 -m unittest discover --start-directory tests --top-level-directory tests --pattern 'test_*.py'
bash scripts/validate-repo-quality-gates.sh .
```

## Success Criteria & Verification Plan

| ID | Criterion |
| --- | --- |
| VAL-AIF-001 | Every governed profile declares exactly one identity pattern, and the frontmatter union admits exactly those forms. |
| VAL-AIF-002 | Every Stage 03 Plan and Task presents the target identity, and no document presents a retired form. |
| VAL-AIF-003 | Stage 05 identities match the target patterns, including the incident and postmortem forms, with no current document invalidated. |
| VAL-AIF-004 | Every Stage 90 pack member presents a member identity, and member numbers are unique inside their pack. |
| VAL-AIF-005 | Every Stage 98 tombstone presents a parent-derived identity, the recovery owner derives that identity, and no derivation collides. |
| VAL-AIF-006 | Every numbered leaf filename begins with its number, preserving the Task and Stage 90 member prefixes. |
| VAL-AIF-007 | No Stage 00 governance path, Stage 99 template path, or machine-loaded configuration path changes. |
| VAL-AIF-008 | Stage 99 templates present the target identity form and domain key for every stage that has one, as placeholders, with a consistent frontmatter guide. |
| VAL-AIF-011 | Every family with domain addressing presents its domain key equal to `artifact_id`, and no frontmatter key without a presenting document remains available. |
| VAL-AIF-012 | No `title` contains its document's artifact identifier, in the corpus or in a template. |
| VAL-AIF-009 | Prose cross-references outside sealed Stage 98 payloads name the target identities. |
| VAL-AIF-010 | The complete ordered validation sequence passes over the final bytes, and renames are recognized as Git renames. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| N/A — approved identity contract | VAL-AIF-001 | Single-owner pattern audit across registry and schema |
| N/A — approved identity contract | VAL-AIF-002 | Stage 03 Plan and Task corpus sweep with retired-form absence |
| N/A — approved identity contract | VAL-AIF-003 | Stage 05 pattern declaration and corpus validity check |
| N/A — approved identity contract | VAL-AIF-004 | Stage 90 member identity and per-pack uniqueness check |
| N/A — approved identity contract | VAL-AIF-005 | Tombstone derivation, collision, and archive recovery suites |
| N/A — approved filename constraint | VAL-AIF-006 | Numbered leaf filename sweep with preserved authoring prefixes |
| N/A — approved filename constraint | VAL-AIF-007 | Machine-loaded path stability assertion |
| N/A — approved identity contract | VAL-AIF-008 | Per-stage template authoring-form review |
| N/A — legacy and deprecated retirement | VAL-AIF-009 | Retired-form reference sweep outside sealed payloads |
| N/A — drift and completion boundary | VAL-AIF-010 | Ordered completion sequence and Git rename recognition |
| N/A — approved identity contract | VAL-AIF-011 | Domain-key parity sweep and unused frontmatter key retirement |
| N/A — approved identity contract | VAL-AIF-012 | Title identifier sweep across corpus and templates |

### Related Documents

- [Plan](./plan.md)
- [SPEC-0067-TSK-0001](./tasks/tsk-0001-aif-000.md)
- [Current Spec Index](../../../../03.specs/README.md#current-spec-index)
- [ADR-0024 — terminal artifact identity and archive layout](../../../../02.architecture/decisions/0024-terminal-artifact-identity-and-archive-layout.md)
- [Document Authoring Policy](../../../../00.agent-governance/policies/document-authoring.md)
- [Quality Policy](../../../../00.agent-governance/policies/quality.md)
