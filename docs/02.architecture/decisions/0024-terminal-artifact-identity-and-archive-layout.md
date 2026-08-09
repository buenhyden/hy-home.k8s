---
title: 'ADR-0024: Terminal Artifact Identity and Archive Layout'
type: sdlc/adr
status: active
owner: platform
updated: 2026-08-10
---

# ADR-0024: Terminal Artifact Identity and Archive Layout

## Overview

This active decision records the human-approved successor to the bounded
artifact-form, archive-path, and script-disposition portions of accepted
[ADR-0023](./0023-work-unit-document-taxonomy-and-governance-authority.md).
It establishes Architecture Description (AD), global artifact identity, a
stable terminal Stage 98 layout, and the exact `scripts/` closure from 50 to 47
tracked assets.

WORK-104 records the decision only. ADR-0023 remains the accepted historical
predecessor and the PRD-008 program-decision registry projection. WORK-105 owns
the atomic lifecycle acceptance and projection change after the reviewed 82
moves. No move, Stage 98 transformation, registry/profile/template change, or
script deletion occurs in this decision-recording work unit.

## Context

The reviewed transition manifest is pinned to source commit
`713dff1fc3de58a2d1682970a7f24faa39c14263` and remains exact at 132 sources,
82 `move-current` entries, and 50 `archive-unique` entries. The frozen Stage 04
PRD-008 Plan and Task remain byte-identical. WORK-103 left 93 historical
ArchiveEnvelope records under Stage 98, while `scripts/` currently contains 50
tracked assets: 40 Python, eight shell, one JSON, and one README.

The transition design still treats ARD as an active architecture form and
dated mirror paths as a Stage 98 exception. It also protects every current
Stage 98 path from change. Those constraints preserve transition safety, but
they do not supply stable terminal identity or a compact archive topology. A
reviewed terminal cutover can change only the outer wrapper and path while
retaining original payload and provenance evidence.

[ISO/IEC/IEEE 42010:2022](https://www.iso.org/standard/74393.html) specifies
the structure and expression of an Architecture Description and distinguishes
architecture from the AD, but does not prescribe recording format or media.
[ISO/IEC/IEEE 29148:2018](https://www.iso.org/standard/72089.html) covers
requirements-engineering processes and requirements information items without
mandating this repository's folders or PRD/SRS/Interface Requirement split.
[ISO/IEC/IEEE 15289:2019](https://www.iso.org/standard/74909.html) covers the
purpose and content of lifecycle information items and supports an
organization-appropriate presentation and repository model. Every local path,
filename, ID, pairing, ledger, and script-disposition rule below is therefore
a human-approved repository decision, not a standards-conformance claim.

## Decision

- Terminal active requirement forms are PRD, optional SRS, and optional
  Interface Requirement. Terminal active architecture forms are Architecture
  Description (AD) and ADR.
- The AD profile/type is `sdlc/ad`, and its terminal route is
  `docs/02.architecture/descriptions/ad-<id>-<slug>.md`. Numeric identity is
  preserved: ARD-0011 becomes AD-0011 in a later work unit and does not receive
  a new number.
- ARD and RFC have no terminal active profile, template, route, relationship,
  or navigation. Immutable historical payload text may retain both terms.
- Every governed terminal artifact carries exactly one globally unique,
  type-valid `artifact_id`. Existing identifiers are preserved. A path-bound
  stable ID must equal its frontmatter identity; the owning terminal profiles
  define the closed typed patterns.
- Terminal Stage 98 uses this stable layout:

  ```text
  docs/98.archive/
  ├── README.md
  ├── changes/
  │   └── chg-0001-<slug>/
  │       ├── plan.md
  │       └── task.md
  ├── tombstones/
  │   ├── 01.requirements/
  │   ├── 02.architecture/
  │   ├── 03.specs/
  │   └── 05.operations/
  └── migrations/
      └── mig-0001-<slug>.md
  ```

- Change and migration paths use four-digit stable IDs (`chg-0001` and
  `mig-0001`). Terminal Stage 98 paths contain no date or year component.
- The 93 historical records survive through one schema-versioned,
  ledger-backed bijection. The 76 execution records become 41 change
  directories: 35 Plan/Task pairs, two Plan-only directories, and four
  Task-only directories. The other 17 records become tombstones distributed
  exactly 3 requirements, 8 architecture, 4 specs, and 2 operations.
  Migration documents are control records and are counted separately from the
  93 historical records.
- The cutover preserves original payload bytes, `source_commit`, `source_blob`,
  and content digest. Before changing an outer wrapper or path, it records the
  old ArchiveEnvelope Git blob. Recovery must succeed from both the terminal
  record and the old Git object/path.
- Each migration ledger row contains exactly `legacy_path`, `stable_path`,
  `artifact_id`, `action`, `replacement`, `source_commit`, and `reason`.
  `action` is closed to `moved`, `merged`, `replaced`, or `deleted`;
  provenance fields may be additive.
- Terminal validators enforce global `artifact_id` uniqueness, typed stable-ID
  patterns, path/frontmatter ID equality, no Stage 98 date/year path,
  migration or tombstone evidence for merged/deleted artifacts, and zero
  active direct links to any individual Stage 98 record. Active navigation may
  use only `docs/98.archive/README.md`.
- The exact terminal script deletion set is
  `scripts/validate-harness.sh`,
  `scripts/document-taxonomy-migration.json`, and
  `scripts/migrate-document-work-units.py`. WORK-112 first migrates the
  wrapper's orchestration consumers, reconciles the full 50-row disposition
  ledger and `scripts/README.md`, and deletes only `validate-harness.sh`,
  leaving 49 tracked assets. WORK-114 deletes the transition JSON/tool and its
  external test after terminal cutover, leaving exactly 47 tracked
  `scripts/` assets: 39 Python, seven shell, and one README.
- The other 47 script assets remain because each owns distinct rules,
  arguments, diagnostics, negative fixtures, evidence, or manual recovery.
  Consolidation occurs at the orchestration/caller layer; similar filenames do
  not establish duplicate semantics.

This decision explicitly supersedes only ADR-0023's terminal Stage 98
mirror-path/date exception and its no-existing-archive-path-change constraint.
The transition constraints remain in force until the reviewed ledger cutover.
ADR-0023's payload/provenance invariants and all other decisions remain
accepted history.

## Explicit Non-goals

- Applying the manifest, moving the 82 current artifacts, or modifying the
  frozen Stage 04 Plan/Task in WORK-104.
- Moving or editing a Stage 98 record before the schema-versioned ledger,
  validators, recovery proof, and bounded cutover are reviewed together.
- Changing the current registry, profile, template, relationship, navigation,
  migration manifest, or script inventory in WORK-104.
- Accepting this successor or replacing ADR-0023 in PRD-008 registry lineage
  before WORK-105's atomic lifecycle transition.
- Rewriting a historical payload, digest, source commit, source blob, or
  observation to match current terminology.
- Treating ISO standards as the source of this repository's physical tree,
  naming, stable-ID, pairing, ledger, or script-count decisions.
- Deleting or merging a script based only on a similar name or implementation
  language.

## Consequences

Architecture and requirement authors gain a smaller terminal form vocabulary,
and AD naming follows the Architecture Description concept without claiming a
standards-mandated Markdown representation. Preserving the number in
ARD-0011-to-AD-0011 keeps lineage stable but requires later atomic profile,
template, navigation, relationship, and path migration.

Stage 98 becomes navigable by stable change and migration identities rather
than mirror dates. This permits a reviewed wrapper/path transformation at the
cost of a complete 93-row ledger, closed action semantics, global identity
validation, old-envelope Git-object retention, and two-path recovery proof.

The script inventory has an auditable numerical closure. The three deletions
occur only at their named consumer/cutover gates, so the terminal count cannot
be achieved by weakening semantically distinct validators.

Until WORK-105 accepts this record and updates the program-decision projection,
ADR-0023 remains authoritative for current registry lineage. Until the later
terminal work units implement the new routes and archive schema, repository
validators continue to enforce transition-state paths and profiles.

## Alternatives

- **Retain ARD as the terminal active architecture description form**: rejected
  because the approved vocabulary distinguishes Architecture Description (AD)
  from ADR while preserving the existing numeric identity.
- **Keep dated mirror paths permanently in Stage 98**: rejected because dates
  do not provide stable artifact identity or a typed change/migration ledger.
- **Rename Stage 98 records without an old-object ledger**: rejected because a
  path-only rewrite would weaken provenance, bijection, and recovery evidence.
- **Allocate new AD numbers during ARD conversion**: rejected because it would
  break existing lineage for a form-name migration.
- **Reduce scripts by combining similar filenames**: rejected because names do
  not prove equal contracts, arguments, diagnostics, fixtures, or recovery
  behavior.
- **Claim the local form/tree as ISO conformance**: rejected because the cited
  standards bound information-item concerns but do not prescribe this local
  repository design.

## Traceability

### Lifecycle Traceability

| Decision lineage | Replacement relation | Affected Spec |
| --- | --- | --- |
| [ADR-0023](./0023-work-unit-document-taxonomy-and-governance-authority.md) | Supersedes only the terminal Stage 98 mirror-path/date exception and no-existing-archive-path-change constraint; WORK-105 owns atomic acceptance and registry projection | [Spec 052](../../03.specs/052-document-taxonomy-consolidation/spec.md) |
