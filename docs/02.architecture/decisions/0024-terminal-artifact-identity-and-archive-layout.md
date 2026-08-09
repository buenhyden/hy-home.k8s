---
title: 'ADR-0024: Terminal Artifact Identity and Archive Layout'
type: sdlc/adr
status: active
owner: platform
updated: 2026-08-10
---

# ADR-0024: Terminal Artifact Identity and Archive Layout

## Overview

This active record is the human-approved terminal successor design produced by
the pre-WORK-104 package `WDTC-AMEND-001`. It establishes Architecture
Description (AD), a closed global artifact identity grammar, stable terminal
Stage 98 records, and the exact `scripts/` closure from 50 to 47 tracked
assets. It records a decision but does not perform any physical migration.

Accepted
[ADR-0023](./0023-work-unit-document-taxonomy-and-governance-authority.md)
remains the transition decision and the PRD-008 program-decision registry
projection. ADR-0024 is the current terminal design, but its partial
supersessions and terminal authority take effect only through WORK-105's
atomic acceptance and registry projection. WORK-104 remains the existing
82-move task and is not completed by `WDTC-AMEND-001`.

## Context

The reviewed transition manifest is pinned to source commit
`713dff1fc3de58a2d1682970a7f24faa39c14263` and remains exact at 132 sources,
82 `move-current` entries, and 50 `archive-unique` entries. The frozen Stage 04
PRD-008 Plan and Task remain byte-identical. WORK-103 left 93 historical
ArchiveEnvelope records under Stage 98, while `scripts/` contains 50 tracked
assets: 40 Python, eight shell, one JSON, and one README.

Accepted
[ADR-0018](./0018-full-body-archive-record-and-retention.md) requires a
full-body immutable payload and provenance but also fixes an archive record at
the mirrored original path and prohibits a parallel Tombstone. Accepted
ADR-0023 preserves Stage 98 dates and existing paths for the transition.
Active
[ARD-0011](../requirements/0011-document-taxonomy-consolidation-architecture.md)
also treats ARD and the mirror archive invariant as current. Those path/form
constraints conflict with the approved terminal topology, although their
payload, provenance, recovery, and transition-safety purposes remain valid.

[ISO/IEC/IEEE 42010:2022](https://www.iso.org/standard/74393.html) specifies
the structure and expression of an Architecture Description and distinguishes
architecture from the AD, but does not prescribe recording format or media.
[ISO/IEC/IEEE 29148:2018](https://www.iso.org/standard/72089.html) covers
requirements-engineering processes and requirements information items without
mandating this repository's folders or PRD/SRS/Interface Requirement split.
[ISO/IEC/IEEE 15289:2019](https://www.iso.org/standard/74909.html) covers the
purpose and content of lifecycle information items and permits an
organization-appropriate presentation and repository model. Every local path,
filename, ID, pairing, ledger, and script-disposition rule below is a
human-approved repository decision, not a standards-conformance claim.

## Decision

Terminal active requirement forms are PRD, optional SRS, and optional
Interface Requirement. Terminal active architecture forms are Architecture
Description (AD) and ADR. AD uses `sdlc/ad` at
`docs/02.architecture/descriptions/ad-<id>-<slug>.md`. ARD-0011 becomes
AD-0011 without renumbering. ARD and RFC have no terminal active profile,
template, route, relationship, or navigation; immutable historical payload
text may retain those terms.

The global current-artifact namespace excludes navigational README files,
templates, fixtures, historical observation profiles, and embedded immutable
archive payloads. Each included outer record has exactly one globally unique
`artifact_id`. A lowercase path token maps to the uppercase canonical ID, and
the path-derived value must equal frontmatter exactly:

| Terminal record | Path extraction | Required outer identity |
| --- | --- | --- |
| PRD | One `docs/01.requirements/<ddd>-<slug>.md` record per three-digit `ddd` | `artifact_id=PRD-<DDD>` |
| SRS | One `srs-<ddd>-<slug>.md` record per three-digit `ddd` | `artifact_id=SRS-<DDD>` |
| Interface Requirement | `ifc-<ddd>-<slug-token>.md`, where the lowercase slug token is part of identity | `artifact_id=IFC-<DDD>-<SLUG-TOKEN>`; the token is uppercased, preserving hyphens, so multiple interfaces under one number remain unique |
| AD | `ad-<dddd>-<slug>.md` | `artifact_id=AD-<DDDD>` |
| ADR | `docs/02.architecture/decisions/<dddd>-<slug>.md` | `artifact_id=ADR-<DDDD>` |
| Spec | `docs/03.specs/<ddd>-<slug>/spec.md` | `artifact_id=SPEC-<DDD>` |
| Plan | `docs/03.specs/<ddd>-<slug>/plan.md` | `artifact_id=PLAN-<DDD>` |
| Task | `docs/03.specs/<ddd>-<slug>/tasks.md` | `artifact_id=TASK-<DDD>` |

`<ddd>` and `<dddd>` are zero-padded decimal tokens. `<slug-token>` is one or
more lowercase alphanumeric segments separated by single hyphens; its
canonical ID token is the same sequence uppercased. PRD and SRS permit one
outer record per numeric ID. AD, ADR, Spec, Plan, and Task likewise permit one
record per typed numeric ID; Interface Requirement alone uses its slug token
to preserve multiple unique interfaces for one numeric group.

Terminal Stage 98 uses this stable layout:

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

The Stage 98 path/frontmatter grammar is closed:

| Terminal record | Path/frontmatter equality |
| --- | --- |
| Change aggregate | Directory `changes/chg-<dddd>-<slug>/` has `change_id=CHG-<DDDD>`; `change_id` is grouping metadata, not an `artifact_id`. |
| Change Plan leaf | `changes/chg-<dddd>-<slug>/plan.md` has outer `artifact_id=PLAN-CHG-<DDDD>`. |
| Change Task leaf | `changes/chg-<dddd>-<slug>/task.md` has outer `artifact_id=TASK-CHG-<DDDD>`. |
| Migration control record | `migrations/mig-<dddd>-<slug>.md` has outer `artifact_id=MIG-<DDDD>` and `migration_id=MIG-<DDDD>`. |
| Tombstone | `tombstones/<stage>/tmb-<type>-<stable-token>.md` has outer `artifact_id=TMB-<TYPE>-<STABLE-TOKEN>`; lowercase path type/token map to uppercase frontmatter. |

Tombstone `<stage>/<TYPE>` pairs are limited to
`01.requirements/{PRD,SRS,IFC}`,
`02.architecture/{AD,ADR}`,
`03.specs/{SPEC,PLAN,TASK}`, and
`05.operations/{GUIDE,INCIDENT,POLICY,RUNBOOK,POSTMORTEM}`. A historical ARD
payload maps to terminal type `AD`; its embedded `original_artifact_id` may
remain `ARD-####`. The `<stable-token>` is the lowercase, hyphen-preserving
remainder after the terminal type prefix and maps byte-for-byte after uppercase
normalization to `<STABLE-TOKEN>`. Embedded `original_artifact_id` is
provenance only and is excluded from the outer/global current-ID namespace.

The 93 current historical records undergo a 93-to-93 cutover, and every row's
`action` is `moved`. The 76 execution records become 41 change directories:
35 Plan/Task pairs, two Plan-only directories, and four Task-only directories.
The other 17 records become individual tombstones distributed exactly three
requirements, eight architecture, four specs, and two operations. Migration
documents are control records outside the 93-record count.

Every ledger row retains the seven named user fields `legacy_path`,
`stable_path`, `artifact_id`, `action`, `replacement`, `source_commit`, and
`reason`; those fields are required, not an exclusive field set. It also
requires `schema_version`, `migration_id`, `legacy_archive_commit`,
`legacy_envelope_blob`, `source_blob`, `content_sha256`, and `record_kind`.
`source_commit` and `source_blob` identify the original archived source;
`legacy_archive_commit` and `legacy_envelope_blob` independently identify the
old ArchiveEnvelope commit/object before the outer wrapper or path changes.

Actions are closed to `moved`, `merged`, `replaced`, and `deleted`. `moved`
maps one legacy record to one unique terminal record with `replacement=null`.
A future `merged` or `replaced` action retains a unique tombstone
`stable_path` for that source and requires a non-null replacement artifact ID.
A future `deleted` action also retains a unique tombstone `stable_path` but
requires `replacement=null`. No action may share or collapse two rows onto one
`stable_path`; every source always retains one independently addressable
terminal evidence record.

The cutover preserves original payload bytes, `source_commit`, `source_blob`,
and `content_sha256`. Recovery must succeed from both the terminal record and
the independently retained old envelope Git object/path.

The direct-link validator corpus is mutable/current, registry-selected
Markdown outside Stage 98. Historical observation profiles and embedded
immutable archive payloads are excluded. The Stage 98 collection README and a
migration ledger/control record may reference individual stable records for
index and provenance. Every other current document may link only to
`docs/98.archive/README.md`, never an individual Stage 98 record.

The successor schedule in Spec 052 is closed at WORK-104 through WORK-115.
WORK-104 performs the 82 moves and rebases the destination Plan/Task; WORK-105
creates the AD route and Stage 99 core forms, atomically converts active
ARD-0011 to AD-0011 with its archive-invariant replacement, accepts ADR-0024,
and changes the registry projection. Stage 98 rehome in WORK-107 is forbidden
before that WORK-105 acceptance. The destination Plan/Task rebaseline
explicitly supersedes their old WORK-105 through WORK-110 meanings.

The exact terminal script deletion set is `scripts/validate-harness.sh`,
`scripts/document-taxonomy-migration.json`, and
`scripts/migrate-document-work-units.py`. WORK-112 first migrates orchestration
consumers, reconciles the full 50-row disposition ledger and
`scripts/README.md`, and deletes only `validate-harness.sh`, leaving 49
tracked assets. WORK-114 deletes the transition JSON/tool and its external
test after terminal cutover, leaving exactly 47 tracked `scripts/` assets: 39
Python, seven shell, and one README. The other 47 assets remain because each
owns distinct rules, arguments, diagnostics, negative fixtures, evidence, or
manual recovery.

At WORK-105 acceptance this decision partially supersedes only ADR-0018's
mirror-original-path requirement and Tombstone prohibition, plus ADR-0023's
Stage 98 date/mirror-path immutability. ADR-0018's full-body payload,
provenance, retention, and recovery invariants and ADR-0023's transition
safety and all unrelated decisions remain preserved. Active ARD-0011 is a
conflicting transition predecessor: it MUST be converted to AD-0011 and its
mirror-path archive invariant MUST be replaced atomically before ADR-0024 can
be accepted. Until then ADR-0018 and ADR-0023 remain accepted predecessors,
ARD-0011 remains active, and ADR-0023 remains the registry projection.

## Explicit Non-goals

- Completing the frozen Task's WORK-104 82-move tranche in `WDTC-AMEND-001`.
- Moving or editing a Stage 98 record before WORK-105 acceptance and the later
  schema-versioned ledger, validators, recovery proof, and bounded cutover.
- Changing the current registry, profile, template, relationship, navigation,
  migration manifest, or script inventory in `WDTC-AMEND-001`.
- Accepting this successor or replacing ADR-0023 in PRD-008 registry lineage
  before WORK-105's atomic lifecycle transition.
- Rewriting a historical payload, digest, source commit, source blob, embedded
  original artifact ID, or observation to match current terminology.
- Treating ISO standards as the source of this repository's physical tree,
  naming, stable-ID, pairing, ledger, or script-count decisions.
- Deleting or merging a script based only on a similar name or implementation
  language.

## Consequences

Architecture and requirement authors gain a smaller terminal form vocabulary,
and AD naming follows the Architecture Description concept without claiming a
standards-mandated Markdown representation. Preserving the number in
ARD-0011-to-AD-0011 keeps lineage stable but makes the WORK-105 conversion and
archive-invariant replacement a hard acceptance gate.

Stage 98 becomes navigable by stable change and migration identities rather
than mirror dates. That costs a complete 93-row ledger, unique terminal
evidence for every source, closed action semantics, global identity
validation, old-envelope Git-object retention, and two-path recovery proof.

The script inventory has an auditable numerical closure. The three deletions
occur only at their named consumer/cutover gates, so the terminal count cannot
be achieved by weakening semantically distinct validators.

Until WORK-105 atomically accepts this record and updates the program-decision
projection, ADR-0023 remains authoritative for transition registry lineage.
Until the later terminal work units implement the new routes and archive
schema, validators continue to enforce transition-state paths and profiles.

## Alternatives

- **Retain ARD as the terminal active architecture description form**:
  rejected because the approved vocabulary distinguishes Architecture
  Description (AD) from ADR while preserving the existing numeric identity.
- **Keep dated mirror paths permanently in Stage 98**: rejected because dates
  do not provide stable artifact identity or a typed change/migration ledger.
- **Reuse one terminal path for merged sources**: rejected because it destroys
  independently addressable source evidence and makes reverse recovery
  ambiguous.
- **Rename Stage 98 records without an old-object ledger**: rejected because a
  path-only rewrite weakens provenance and recovery evidence.
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
| [ADR-0018](./0018-full-body-archive-record-and-retention.md) | At WORK-105 acceptance, partially supersedes mirror-original-path and Tombstone prohibition only; preserves full-body payload, provenance, retention, and recovery | [Spec 052](../../03.specs/052-document-taxonomy-consolidation/spec.md) |
| [ADR-0023](./0023-work-unit-document-taxonomy-and-governance-authority.md) | At WORK-105 acceptance, partially supersedes terminal Stage 98 date/mirror-path immutability only; preserves transition safety and unrelated decisions | [Spec 052](../../03.specs/052-document-taxonomy-consolidation/spec.md) |
