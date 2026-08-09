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

The read-only census at review base `833995d1` found exactly eight tracked
current `sdlc/ard` records: active ARD-0004 through ARD-0007, accepted
ARD-0008 and ARD-0009, and active ARD-0010 and ARD-0011. A terminal AD form
cannot be accepted by converting only ARD-0011; every active or accepted ARD
and every live consumer of the ARD form requires an exact disposition.

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
`docs/02.architecture/descriptions/ad-<id>-<slug>.md`. WORK-105 converts the
complete eight-record current ARD corpus one-to-one, preserves every numeric
identifier and filename slug, and preserves each record's active or accepted
lifecycle state:

| Current ID | Current status | Exact current path | Terminal ID and exact WORK-105 path |
| --- | --- | --- | --- |
| ARD-0004 | active | `docs/02.architecture/requirements/0004-argo-rollouts-progressive-delivery.md` | AD-0004 at `docs/02.architecture/descriptions/ad-0004-argo-rollouts-progressive-delivery.md` |
| ARD-0005 | active | `docs/02.architecture/requirements/0005-argo-notifications-slack.md` | AD-0005 at `docs/02.architecture/descriptions/ad-0005-argo-notifications-slack.md` |
| ARD-0006 | active | `docs/02.architecture/requirements/0006-workspace-agent-governance-platform.md` | AD-0006 at `docs/02.architecture/descriptions/ad-0006-workspace-agent-governance-platform.md` |
| ARD-0007 | active | `docs/02.architecture/requirements/0007-current-local-gitops-platform.md` | AD-0007 at `docs/02.architecture/descriptions/ad-0007-current-local-gitops-platform.md` |
| ARD-0008 | accepted | `docs/02.architecture/requirements/0008-workspace-document-assurance-operating-model.md` | AD-0008 at `docs/02.architecture/descriptions/ad-0008-workspace-document-assurance-operating-model.md` |
| ARD-0009 | accepted | `docs/02.architecture/requirements/0009-document-lifecycle-evidence-operating-model.md` | AD-0009 at `docs/02.architecture/descriptions/ad-0009-document-lifecycle-evidence-operating-model.md` |
| ARD-0010 | active | `docs/02.architecture/requirements/0010-repository-delivery-evidence-architecture.md` | AD-0010 at `docs/02.architecture/descriptions/ad-0010-repository-delivery-evidence-architecture.md` |
| ARD-0011 | active | `docs/02.architecture/requirements/0011-document-taxonomy-consolidation-architecture.md` | AD-0011 at `docs/02.architecture/descriptions/ad-0011-document-taxonomy-consolidation-architecture.md` |

These ARD/AD labels are lifecycle document identities; WORK-105 preserves the
four-digit identity and WORK-108 later backfills the mandatory `artifact_id`
field after the full conversion. WORK-105 MUST NOT leave a ninth implicit
mapping, renumber a record, change a slug, or change an active/accepted state.

The full conversion includes a complete tracked full-repository `git grep`
classifier for ARD profile, template, route, relationship, lifecycle,
registry, navigation, authoring, validation, test, fixture, skill, issue-form,
execution, operations, and generated-current consumers. Every match is either
`migrate-current` to AD terminology/routes or `retain-history` only when the
containing surface is immutable or explicitly historical. Terminal acceptance
requires both zero unconverted current ARDs and zero live or unclassified ARD
consumers. Literal matches may remain only in reviewed `retain-history`
surfaces. ARD and RFC then have no terminal active profile, template, route,
relationship, or navigation.

Within that full-corpus migration, the ARD-0011 authority conflict is a
separate atomic gate: AD-0011 must contain the replacement archive invariant,
ADR-0024 must be accepted, and the PRD-008 registry projection must change
from ADR-0023 to ADR-0024 in the same reviewed change. That authority gate
cannot pass early or substitute for the eight-record conversion and complete
consumer disposition.

The current transition registry also exposes the human-authored profile
`sdlc/api-spec` at `docs/03.specs/<ddd>-<slug>/api-spec.md` and its authored
`api-spec.template.md`. WORK-105 retires that profile, route, template, and
authored relationships as part of the atomic AD/Stage 99 forms cutover.
Terminal human-authored interface requirements live only as Stage 01
`sdlc/interface` records under the `IFC-<DDD>-<SLUG-TOKEN>` grammar below.
The current tracked corpus contains zero authored
`docs/03.specs/*/api-spec.md` records. That instance census is only the first
retirement condition; it is not consumer proof. WORK-105 must satisfy two
independent conditions before retirement:

1. the tracked authored instance census for
   `docs/03.specs/*/api-spec.md` is zero; and
2. a full-repository `git grep` classifier assigns every authored-profile
   reference a reviewed disposition, leaving zero live or unclassified
   authored API Spec consumers.

The consumer classifier covers, at minimum, profile/template and relationship
surfaces; the positive Markdown fixture; lifecycle transitions and
implementation; registry allowlists, mappings, and self-tests; the authoring
hook and template routing; current Stage 00 and Stage 03 navigation prose; and
validators, tests, documentation, and fixtures. Each match must migrate to the
Stage 01 Interface form or a native contract, convert from positive API Spec
coverage to a terminal retired-route negative fixture, or be classified
`retain-history` / `retain-native` when it is immutable history or native
evidence. A literal repository-wide match count is not required to reach zero;
the acceptance invariant is zero live or unclassified consumers after the
complete classifier.

Native OpenAPI, GraphQL, and Protobuf profiles and their native templates
remain machine-readable Interface evidence. They are not human-authored API
Spec records, do not enter the mandatory human `artifact_id` namespace, and
retain their separate native contract identity and validation rules.

Global uniqueness applies to every declared `artifact_id`. The mandatory
terminal outer profiles are PRD, SRS, Interface Requirement, AD, ADR, Spec,
Agent Design, Data Model, Tests, Plan, Task, Guide, Policy, Runbook, Incident,
Postmortem, and the Stage 98 Plan, Task, Tombstone, and Migration records. Each
such record MUST declare exactly one path-derived `artifact_id`.

The following profiles and surfaces are outside the mandatory namespace and
MUST NOT declare `artifact_id`: Stage 00 governance/reference, all Stage 90
content/reference/observation profiles, governance memory/progress, Stage 99
support, README/navigation, templates, fixtures, native/generated surfaces,
the current authored `sdlc/api-spec` / `api-spec.md` surface being retired,
the virtual Stage 98 change-directory aggregate, and embedded immutable
archive payloads. The authored `api-spec.template.md` is both a template and a
retired terminal surface. Embedded `original_artifact_id` is provenance, not
an outer `artifact_id`, and is excluded from global current-ID uniqueness.

Terminal active path extraction is deterministic and closed:

| Mandatory outer profile | Path extraction | Required `artifact_id` |
| --- | --- | --- |
| PRD | `docs/01.requirements/<ddd>-<slug>.md` | `PRD-<DDD>` |
| SRS | `docs/01.requirements/srs-<ddd>-<slug>.md` | `SRS-<DDD>` |
| Interface Requirement | `docs/01.requirements/ifc-<ddd>-<slug-token>.md`; the complete filename suffix after `ifc-<ddd>-` is identity-bearing | `IFC-<DDD>-<SLUG-TOKEN>` |
| AD | `docs/02.architecture/descriptions/ad-<dddd>-<slug>.md` | `AD-<DDDD>` |
| ADR | `docs/02.architecture/decisions/<dddd>-<slug>.md` | `ADR-<DDDD>` |
| Spec | `docs/03.specs/<ddd>-<slug>/spec.md` | `SPEC-<DDD>` |
| Agent Design | `docs/03.specs/<ddd>-<slug>/agent-design.md` | `AGENT-DESIGN-<DDD>` |
| Data Model | `docs/03.specs/<ddd>-<slug>/data-model.md` | `DATA-MODEL-<DDD>` |
| Tests | `docs/03.specs/<ddd>-<slug>/tests.md` | `TESTS-<DDD>` |
| Plan | `docs/03.specs/<ddd>-<slug>/plan.md` | `PLAN-<DDD>` |
| Task | `docs/03.specs/<ddd>-<slug>/tasks.md` | `TASK-<DDD>` |
| Guide | `docs/05.operations/guides/<dddd>-<slug>.md` | `GUIDE-<DDDD>` |
| Policy | `docs/05.operations/policies/<dddd>-<slug>.md` | `POLICY-<DDDD>` |
| Runbook | `docs/05.operations/runbooks/<dddd>-<slug>.md` | `RUNBOOK-<DDDD>` |
| Incident | `docs/05.operations/incidents/<yyyy>/INC-<nnn>-<slug>/INC-<nnn>-<slug>.md`; directory and filename incident numbers MUST agree | `INC-<YYYY>-<NNN>` |
| Postmortem | `docs/05.operations/incidents/<yyyy>/INC-<nnn>-<slug>/postmortem.md` | `POSTMORTEM-<YYYY>-<NNN>` |

`<ddd>`, `<dddd>`, `<yyyy>`, and `<nnn>` are zero-padded decimal tokens.
Interface `<SLUG-TOKEN>` matches
`[A-Z0-9]+(?:-[A-Z0-9]+)*`; its path form is the exact ASCII-lowercase token.
For every typed ID, ASCII-lowercasing the canonical ID and its path-derived
counterpart must yield the same hyphen-delimited token sequence. Validators
reject aliases, collisions, leading/trailing/double hyphens, non-canonical
case, or more than one path that derives the same ID.

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
| Change aggregate | Directory `changes/chg-<dddd>-<slug>/` yields the virtual/path-derived `change_id=CHG-<DDDD>`. A directory has no frontmatter and the change aggregate is not an artifact. |
| Change Plan leaf | `changes/chg-<dddd>-<slug>/plan.md` has `change_id=CHG-<DDDD>` and unique outer `artifact_id=PLAN-CHG-<DDDD>`. |
| Change Task leaf | `changes/chg-<dddd>-<slug>/task.md` has `change_id=CHG-<DDDD>` and unique outer `artifact_id=TASK-CHG-<DDDD>`. |
| Migration control record | `migrations/mig-<dddd>-<slug>.md` has outer `artifact_id=MIG-<DDDD>` and `migration_id=MIG-<DDDD>`. |
| Tombstone | `tombstones/<stage>/tmb-<type>-<stable-token>.md` has outer `artifact_id=TMB-<TYPE>-<STABLE-TOKEN>`; lowercase path type/token map to uppercase frontmatter. |

Every present change Plan/Task leaf MUST carry the virtual `change_id` derived
from its parent directory, and sibling leaves MUST carry the same value. The
leaf `artifact_id` remains globally unique; `change_id` is not admitted to the
artifact namespace.

Tombstone `<stage>/<TYPE>` pairs are limited to
`01.requirements/{PRD,SRS,IFC}`,
`02.architecture/{AD,ADR}`,
`03.specs/{SPEC,AGENT-DESIGN,DATA-MODEL,TESTS,PLAN,TASK}`, and
`05.operations/{GUIDE,POLICY,RUNBOOK,INCIDENT,POSTMORTEM}`. A historical ARD
payload maps to terminal type `AD`; its embedded `original_artifact_id` may
remain `ARD-####`.

The current 93-record cutover needs no `API-SPEC` tombstone type because its
reviewed corpus contains no authored API Spec record. If a historical
`api-spec.md` is discovered later, terminal entry fails until a reviewed
ledger disposition maps it to the Stage 01 Interface form or to an `IFC`
tombstone under the existing grammar; no new tombstone type is inferred.

When `original_artifact_id` exists, `<STABLE-TOKEN>` is the complete suffix
after that original ID's type prefix and separator; the lowercase path token
must be its exact canonical lowercase form. When it is null, the ID token is
`LEGACY-<HASH>`, where `<HASH>` is the full uppercase SHA-256 hex digest of the
UTF-8 bytes `canonical legacy_path`, one NUL byte, and the lowercase ASCII
`source_blob` Git OID. The path token is `legacy-<hash>` in lowercase.
`canonical legacy_path` is the exact repository-relative POSIX tracked path
with no leading slash, `.` or `..` segment, repeated separator, or alternate
spelling. Tombstone validation rejects token aliases, digest truncation,
collisions, and leading/trailing/double hyphens.

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
creates the AD route and Stage 99 core forms, atomically converts all eight
current ARD records under the closed mapping, closes every live ARD consumer,
and separately gates AD-0011's archive-invariant replacement with ADR-0024
acceptance and the registry projection change. It also retires authored
`sdlc/api-spec` / `api-spec.md` / `api-spec.template.md` with zero authored
instance proof, complete consumer disposition, and terminal negative fixtures,
and preserves the native
OpenAPI/GraphQL/Protobuf evidence contracts and classified immutable history.
Stage 98 rehome in WORK-107 is forbidden before that WORK-105 acceptance. The
WORK-108 `artifact_id` backfill is forbidden until the full WORK-105 AD
conversion and both ARD closure gates pass. The
destination Plan/Task rebaseline explicitly supersedes their old WORK-105
through WORK-110 meanings.

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
conflicting transition predecessor inside the eight-record ARD conversion: its
AD-0011 target, replacement archive invariant, ADR-0024 acceptance, and
registry projection change form the separate atomic authority gate. Until the
full eight-record and consumer closure plus that authority gate pass,
ADR-0018 and ADR-0023 remain accepted predecessors, the current ARD records
retain their reviewed states, and ADR-0023 remains the registry projection.

## Explicit Non-goals

- Completing the frozen Task's WORK-104 82-move tranche in `WDTC-AMEND-001`.
- Moving or editing a Stage 98 record before WORK-105 acceptance and the later
  schema-versioned ledger, validators, recovery proof, and bounded cutover.
- Changing the current registry, profile, template, relationship, navigation,
  migration manifest, or script inventory in `WDTC-AMEND-001`.
- Moving any of the eight current ARDs or rewriting one of their consumers in
  `WDTC-AMEND-001`; WORK-105 owns the physical full-corpus conversion.
- Retiring the current authored API Spec surface before WORK-105 performs its
  atomic forms cutover, zero-instance proof, complete consumer disposition,
  and terminal negative fixtures.
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
standards-mandated Markdown representation. Preserving ARD-0004 through
ARD-0011 as AD-0004 through AD-0011 keeps every lineage stable. It also makes
the complete eight-record/consumer closure and the separate AD-0011 authority
gate mandatory WORK-105 acceptance evidence.

Retiring the empty authored API Spec route removes a second human interface
form without deleting machine-readable API contracts. Authors use Stage 01
Interface Requirement; OpenAPI, GraphQL, and Protobuf retain separate native
identity validation and remain implementation evidence.

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
  break existing lineage for a form-name migration across the complete
  eight-record current corpus.
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
