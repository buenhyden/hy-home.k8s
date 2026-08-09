---
title: 'Document Taxonomy Consolidation Technical Specification'
type: sdlc/spec
status: active
owner: platform
updated: 2026-08-10
---

# Document Taxonomy Consolidation Technical Specification (Spec)

## Overview

This specification implements
[PRD-008](../../01.requirements/008-workspace-document-taxonomy-consolidation.md),
[ARD-0011](../../02.architecture/requirements/0011-document-taxonomy-consolidation-architecture.md),
and the human-approved direction recorded in accepted
[ADR-0023](../../02.architecture/decisions/0023-work-unit-document-taxonomy-and-governance-authority.md).
It replaces the earlier Spec 052 direction that would have renumbered
`05.operations` and deleted several validator families without current
consumer proof.

The pre-WORK-104 design package `WDTC-AMEND-001` created active
[ADR-0024](../../02.architecture/decisions/0024-terminal-artifact-identity-and-archive-layout.md),
which records the later human-approved successor for terminal requirement and
architecture forms, global artifact identity, stable Stage 98 layout, and the
exact `scripts/` disposition. ADR-0023 remains the accepted transition decision
and PRD-008 registry projection until WORK-105 atomically converts active
ARD-0011 to AD-0011 with its archive-invariant replacement, accepts ADR-0024,
and changes the projection after WORK-104's 82 reviewed moves.

WORK-105 also retires the current human-authored `sdlc/api-spec` profile,
Stage 03 `api-spec.md` route, and `api-spec.template.md`. Terminal authored
Interface Requirements live only at Stage 01 as `sdlc/interface`; native
OpenAPI, GraphQL, and Protobuf profiles/templates remain machine-readable
Interface evidence under their separate native identity contracts.

The terminal result co-locates each retained Spec/Plan/Task work unit in Stage
03, removes the Stage 04 execution tree, preserves Stage 05, excludes a Release
family, consolidates document and AI-agent governance authorities, reconciles
validators and scripts by behavior, disposes of legacy material with explicit
provenance, and closes the observed pre-change validation failures.

This is an implementation-ready repository-static contract. It does not claim
that a provider consumed an adapter, enforced a policy, executed an approved
action, ran hosted CI, or changed remote/live infrastructure.

## Strategic Boundaries & Non-goals

Authorized paths are `docs/**`, repository-local agent/provider instruction
projections, document and harness contracts, templates, scripts, tests,
fixtures, generated documentation outputs, indexes, and cross-links affected
by the migration. Git history may be read to establish provenance.

Existing `docs/98.archive/**` records remain read-only during
`WDTC-AMEND-001`, WORK-104, WORK-105, and WORK-106. WORK-107 cannot begin until
WORK-105 has atomically replaced the conflicting ARD-0011 archive invariant
and accepted ADR-0024. The later cutover transforms only the outer wrapper/path
through the activated schema-versioned ledger, validators, and recovery proof
while preserving payload bytes, digest, original `source_commit`,
`source_blob`, and the old ArchiveEnvelope commit/blob. Dated Stage 90
observation bodies retain their historical meaning; only contract-permitted
navigation or explicit annotations may change.

The implementation must not renumber Stage 05 or any lifecycle identifier,
create a Release family, create tutorial/explanation families, change platform
desired state, inspect secret values, authenticate providers, mutate hosted CI,
publish, push, merge, deploy, or operate live infrastructure.

## Contracts

### DTC-1 Work-unit topology

The terminal live route is `docs/03.specs/<NNN>-<slug>/`. `spec.md` is the work
unit owner. `plan.md` is optional but requires the Spec. `tasks.md` is optional
but requires both Spec and Plan. No live Spec, Plan, Task, or index remains
under `docs/04.execution/`.

### DTC-2 Stable identity and date exceptions

Mutable PRD, SRS, Interface Requirement, AD, ADR, Spec, Plan, Task, Guide,
Policy, and Runbook filenames use stable identifiers or slugs and carry
authoring dates in frontmatter. Dates remain in terminal paths only for dated
Stage 90 observation/snapshot identity and real Incident/Postmortem identity.
Terminal Stage 98 paths contain no date or year component. The registry owns
the exact path classes and exceptions after the terminal cutover.

### DTC-3 Stage and document-family boundary

`docs/05.operations/` remains the only live operations stage and contains
guides, incidents, policies, and runbooks. Stage 04 is unused after execution
retirement. No Release profile, template, folder, lifecycle, or validator is
introduced.

### DTC-4 Authority uniqueness

`document-profiles.json` and its schema are the sole machine owner of routes,
profile IDs, frontmatter keys and states, headings, canonical forms,
relationships, and exceptions. Stage 00 owns agent-facing authoring policy.
Stage 99 `document-contract.md` and `document-lifecycle.md` explain template
and lifecycle rationale. README files are navigation and inventory only.

### DTC-5 Lineage integrity

Existing identifiers are unchanged. Program and standalone lineage remains in
the closed registry relations and reciprocal lifecycle tables; no competing
frontmatter lineage keys are added. The unrelated ADR-0021 association was
corrected atomically when reviewed ADR-0023 was accepted. During transition
the registry and immutable self-test projection require `decision=0023`; the
current terminal design is ADR-0024. WORK-105 owns the atomic
ARD-0011-to-AD-0011/invariant replacement, authored API Spec retirement,
ADR-0024 acceptance, and projection change. No acceptance or registry change
occurs in `WDTC-AMEND-001` or WORK-104.

### DTC-6 Route transition

The registry and validators implement explicit `legacy`, `transition`, and
`terminal` route modes. Transition accepts only the enumerated mapping and
rejects duplicate active ownership. Terminal mode rejects every live Stage 04
execution path and every mutable consumer of that path.

### DTC-7 Disposition evidence

Each retired document, contract, script, test, fixture, or generated artifact
has exactly one reviewed disposition: `move-current`, `archive-unique`,
`retain-observation`, `merge-successor`, `delete-redundant`, or
`retain-contract`. Deletion requires a named successor or reproducibility,
zero live consumers, and no unique negative fixture or rule.

For the terminal Stage 98 cutover, every migration ledger row requires
`legacy_path`, `stable_path`, `artifact_id`, `action`, `replacement`,
`source_commit`, and `reason`, but those seven fields are not exclusive. It
also requires `schema_version`, `migration_id`, `legacy_archive_commit`,
`legacy_envelope_blob`, `source_blob`, `content_sha256`, and `record_kind`.
`source_commit` identifies the original source; `legacy_archive_commit`
identifies the distinct commit containing the old envelope. `action` is closed
to `moved`, `merged`, `replaced`, or `deleted`, with the unique-terminal-record
semantics in DTC-15.

### DTC-8 Agent-governance control

The existing harness contract and schema gain a closed `agentSystems` policy
and record-shape section covering purpose, intended/prohibited use,
accountable owner, lifecycle, contextual risk, treatment, residual risk,
review cadence, tool/data trust, oversight, stop conditions, approval/trace
evidence references, evaluation, and component provenance. Actual runtime
records remain at their approved Task, Runbook, Incident, or provider-evidence
owner. Provider adapters contain provider-native deltas only.

The current approval-boundary `Evidence Location` column is the human routing
input. The target harness selects one closed `evidenceOwnerPolicy` whose owner
type is `task`, `runbook-record`, `incident`, or `provider-runtime-record`.
The policy binds a canonical owner reference, allowed append principal class,
immutability rule, retention class, validator, and trust anchor. Missing or
self-asserted identity cannot close approval. The harness schema,
approval-boundary projection, provider evidence contract, and validators must
activate atomically; until then this control remains designed, not enforced.

### DTC-9 Approval and trust boundary

An action requiring approval records `approvalPolicyRef`, `actionClass`,
`approvalId`, `actionFingerprint`, `requesterPrincipal`,
`approverPrincipal`, normalized/redacted target metadata plus digest,
`argumentsDigest`, `authorityScope`, `issuedAt`, `expiresAt`, `decision`,
`approvalEvidenceRef`, and `resultEvidenceRef`. Untrusted prompts, retrieved
context, and tool output remain untrusted until a named control validates or
isolates them. General conversation approval cannot authorize a different
target, arguments, action class, or authority scope.

### DTC-10 Evidence non-promotion

Repository declaration, provider-runtime enforcement, hosted-CI observation,
and authorized remote/live observation are separate states. Each control
separates `designEnforcementDisposition` from
`observedEnforcementEvidenceRef`; the latter remains `DEFER` without matching
provider-runtime evidence. Static schema or adapter validation cannot satisfy
an enforcement or execution state.

### DTC-11 Validator semantic preservation

The aggregate quality gate remains. Selection/orchestration duplication is
consolidated through `validation-surfaces.json`. Registry, Markdown,
links/owners, archive, security, CI, and agent-semantic validators remain
separate where inputs, negative fixtures, failures, or evidence differ.
`validate-harness.sh` is removed only after its live consumers migrate.

### DTC-12 Green terminal baseline

The program closes the recorded registry self-test memory allocation failure,
detect-secrets false-positive/baseline drift, and Markdown heading failure
without disabling the corresponding checks. Every logical commit records
focused and aggregate results; terminal acceptance requires all-files PASS.

### DTC-13 Terminal document forms

Terminal active requirement forms are PRD, optional SRS, and optional
Interface Requirement. Terminal active architecture forms are Architecture
Description (AD) and ADR. AD uses profile/type `sdlc/ad` at
`docs/02.architecture/descriptions/ad-<id>-<slug>.md`. The later conversion
preserves numeric identity, so ARD-0011 becomes AD-0011. Because active
ARD-0011 still asserts the conflicting mirror archive invariant, WORK-105 MUST
replace that invariant and convert the record atomically before accepting
ADR-0024. ARD and RFC then have no terminal active profile, template, route,
relationship, or navigation; historical payload text may retain both terms.

Current `sdlc/api-spec`, its fixed `api-spec.md` Stage 03 route, and the
authored `api-spec.template.md` are transition surfaces, not a terminal form.
WORK-105 retires them only after two independent evidence conditions pass:

1. zero tracked authored `docs/03.specs/*/api-spec.md` instances; and
2. a complete full-repository `git grep` consumer classifier with zero live or
   unclassified authored-profile consumers.

The second condition inventories profile/template and relationships; the
positive Markdown fixture; lifecycle transitions and implementation; registry
allowlists, mappings, and self-tests; the authoring hook and template routing;
current Stage 00 and Stage 03 navigation prose; and validators, tests,
documentation, and fixtures. Each reference must migrate to Stage 01 Interface
or a native contract, convert from positive API Spec coverage to a terminal
retired-route negative fixture, or be classified `retain-history` /
`retain-native` for immutable history or native evidence. The gate does not
require literal grep zero across history; it requires zero live or unclassified
consumers after classification.

A human authors interface requirements only as Stage 01 `sdlc/interface` under
the IFC grammar. Native OpenAPI, GraphQL, and Protobuf profiles/templates
remain machine-readable Interface evidence; they are not authored API Spec and
retain their separate native identity/validation contracts.

### DTC-14 Global artifact identity

Global uniqueness applies to every declared `artifact_id`. Mandatory terminal
outer profiles are PRD, SRS, Interface Requirement, AD, ADR, Spec, Agent
Design, Data Model, Tests, Plan, Task, Guide, Policy, Runbook, Incident,
Postmortem, and Stage 98 Plan, Task, Tombstone, and Migration. Every record in
that set MUST declare exactly one path-derived `artifact_id`.

Stage 00 governance/reference, all Stage 90 content/reference/observation
profiles, governance memory/progress, Stage 99 support, README/navigation,
template, fixture, native/generated, the retiring authored `sdlc/api-spec` /
`api-spec.md` surface, the virtual Stage 98 change aggregate, and embedded
immutable archive payload surfaces MUST NOT declare `artifact_id`.
`api-spec.template.md` is both a template and a retired terminal surface.
Embedded `original_artifact_id` is provenance and does not participate in
outer global uniqueness. Native OpenAPI/GraphQL/Protobuf contract identity is
separate from mandatory human artifact identity.

| Mandatory outer profile | Closed path/frontmatter identity |
| --- | --- |
| PRD / SRS | `docs/01.requirements/<ddd>-<slug>.md` / `srs-<ddd>-<slug>.md` maps to `PRD-<DDD>` / `SRS-<DDD>`. |
| Interface Requirement | The complete suffix of `ifc-<ddd>-<slug-token>.md` maps to `IFC-<DDD>-<SLUG-TOKEN>`, permitting multiple interfaces under one number. |
| AD / ADR | Four-digit `ad-<dddd>` / decision `<dddd>` token maps to `AD-<DDDD>` / `ADR-<DDDD>`. |
| Stage 03 | Parent work-unit `<ddd>` plus `spec.md`, `agent-design.md`, `data-model.md`, `tests.md`, `plan.md`, or `tasks.md` maps to `SPEC-<DDD>`, `AGENT-DESIGN-<DDD>`, `DATA-MODEL-<DDD>`, `TESTS-<DDD>`, `PLAN-<DDD>`, or `TASK-<DDD>`. |
| Guide / Policy / Runbook | Stage 05 four-digit filename token maps to `GUIDE-<DDDD>`, `POLICY-<DDDD>`, or `RUNBOOK-<DDDD>`. |
| Incident / Postmortem | Year directory plus matching three-digit incident directory/file token maps to `INC-<YYYY>-<NNN>`; sibling `postmortem.md` maps to `POSTMORTEM-<YYYY>-<NNN>`. |

Interface `<SLUG-TOKEN>` matches
`[A-Z0-9]+(?:-[A-Z0-9]+)*` and the path uses its exact ASCII-lowercase form.
All canonical typed path tokens use single hyphens. The validator derives the
full ID from the path, ASCII-lowercases both comparison forms, and then requires
exact token equality. It rejects aliases, collisions, noncanonical case,
leading/trailing/double hyphens, or more than one path deriving the same ID.
Existing numeric identities remain unchanged.

### DTC-15 Stable terminal Stage 98

Terminal Stage 98 contains `README.md`, stable `changes/chg-####-<slug>/`
directories with `plan.md` and/or `task.md`, stage-typed tombstone collections,
and `migrations/mig-####-<slug>.md` control records. A change directory has no
frontmatter. Its path yields virtual `change_id=CHG-####`, which is grouping
metadata rather than an `artifact_id`. Every present Plan/Task leaf MUST carry
that same parent-derived `change_id`; sibling leaves MUST agree. Their unique
outer IDs are `PLAN-CHG-####` and `TASK-CHG-####`. A migration path has outer
`artifact_id=MIG-####` and equal `migration_id`.

A tombstone path
`tombstones/<stage>/tmb-<type>-<stable-token>.md` has outer
`artifact_id=TMB-<TYPE>-<STABLE-TOKEN>`, with lowercase path tokens mapped to
uppercase frontmatter. The closed stage/type map is
`01.requirements/{PRD,SRS,IFC}`,
`02.architecture/{AD,ADR}`,
`03.specs/{SPEC,AGENT-DESIGN,DATA-MODEL,TESTS,PLAN,TASK}`, and
`05.operations/{GUIDE,POLICY,RUNBOOK,INCIDENT,POSTMORTEM}`. Historical ARD
payload uses terminal outer type AD. Embedded `original_artifact_id` remains
provenance and is excluded from the outer/global current-ID namespace.

The reviewed 93-record corpus has no authored API Spec and therefore adds no
`API-SPEC` tombstone type. If a historical `api-spec.md` is later discovered,
terminal validation stops until a reviewed ledger disposition maps it to a
Stage 01 Interface record or to an `IFC` tombstone under the closed grammar.

If `original_artifact_id` exists, the tombstone `<STABLE-TOKEN>` is its full
suffix after the original type prefix and separator. If it is null, the token
is `LEGACY-<HASH>`, where `<HASH>` is the full uppercase SHA-256 hex digest of
the UTF-8 bytes `canonical legacy_path`, one NUL byte, and lowercase ASCII
`source_blob`; the path uses `legacy-<hash>`. The canonical legacy path is the
exact repository-relative POSIX tracked path with no leading slash, `.` or
`..` segment, repeated separator, or alias. Tombstone validators reject token
aliases, collisions, truncated hashes, and leading/trailing/double hyphens.

The current cutover is 93-to-93 and every row has `action=moved`: 76 execution
records become unique Plan/Task leaves in 41 change directories (35 pairs, two
Plan-only, four Task-only), while 17 other records become unique tombstones in
the exact requirements/architecture/specs/operations split `3/8/4/2`.
Migration documents are counted separately from those 93 records. A future
`moved` row is one-to-one with null replacement; a future `merged` or
`replaced` row retains a unique tombstone path and non-null replacement; a
future `deleted` row retains a unique tombstone path and null replacement. No
two ledger rows may share a stable path.

The cutover preserves payload bytes, original `source_commit`, `source_blob`,
`content_sha256`, `legacy_archive_commit`, and `legacy_envelope_blob`.
Recovery must work from the terminal record and the old Git object/path.

The direct-link validator corpus is mutable/current, registry-selected
Markdown outside Stage 98; historical observation profiles and embedded
immutable archive payloads are excluded. Stage 98's README and migration
ledger/control records may link to individual stable records for
index/provenance. Every other current document may link only to
`docs/98.archive/README.md`.

### DTC-16 Exact script closure

The current 50 tracked `scripts/` assets close to 47 through exactly three
deletions. WORK-112 migrates orchestration consumers, reconciles the full
50-row disposition ledger and `scripts/README.md`, then removes only
`validate-harness.sh`, leaving 49 assets. WORK-114 removes only
`document-taxonomy-migration.json` and `migrate-document-work-units.py` plus the
tool's external test after terminal cutover, leaving 39 Python, seven shell,
and one README asset. The other 47 assets retain distinct rule, argument,
diagnostic, negative-fixture, evidence, or manual-recovery responsibilities.

ISO/IEC/IEEE 42010:2022 defines Architecture Description
structure/expression but not recording media; ISO/IEC/IEEE 29148:2018 defines
requirements-engineering processes and information items but not the local
PRD/SRS/Interface Requirement split; ISO/IEC/IEEE 15289:2019 supports an
organization-selected information-item presentation/repository model. The
official-source links and precise claim boundaries are recorded in ADR-0024.
None of these standards mandates the local route, filename, ID, pairing,
ledger, or script disposition.

## Core Design

### Tranche dependency graph

```text
WDTC-AMEND-001 approved terminal design
  -> WORK-104 moves and destination Plan/Task rebaseline
  -> WORK-105 AD/invariant/API-Spec-retirement/ADR acceptance
  -> WORK-106 transition validators
  -> WORK-107 Stage 98 rehome
  -> WORK-108..114 bounded terminal tranches
  -> WORK-115 independent closure
```

Tests and fixtures precede each production contract change. Later tranches may
depend on earlier path moves, but archive creation, rule consolidation,
agent-governance extension, and script retirement remain separate logical
commits so each can be reviewed or reverted independently.

The successor schedule is closed; no unlisted work number may absorb these
contracts:

| Work | Closed scope |
| --- | --- |
| WORK-104 | Apply exactly the 82 current moves, rewrite the two transition edges, and rebaseline the destination Plan/Task to this table. |
| WORK-105 | Activate the AD route and Stage 99 core forms; atomically convert active ARD-0011 to AD-0011 with archive-invariant replacement; retire authored `sdlc/api-spec` / `api-spec.md` / `api-spec.template.md` only after independent zero-instance and complete full-grep consumer-disposition gates leave zero live/unclassified consumers; migrate Interface/native consumers, convert positive fixtures to retired-route negatives, retain classified history/native evidence, preserve OpenAPI/GraphQL/Protobuf contracts; accept ADR-0024; and change the PRD-008 registry projection. |
| WORK-106 | Implement global artifact-identity and migration-ledger transition validators and negative fixtures. |
| WORK-107 | Rehome all 93 Stage 98 records under the closed stable grammar; entry is forbidden before WORK-105 acceptance. |
| WORK-108 | Backfill global outer `artifact_id` values under the closed grammar and exclusions. |
| WORK-109 | Consolidate document authority and terminal routes. |
| WORK-110 | Consolidate agent-governance contracts and projections. |
| WORK-111 | Reconcile the complete 50-row script disposition ledger. |
| WORK-112 | Consolidate orchestration, migrate consumers, delete only `validate-harness.sh`, and prove 49 scripts. |
| WORK-113 | Rotate/clean progress and generated graph surfaces with recovery and consumer proof. |
| WORK-114 | Delete the migration JSON/tool/external test and transition projections after cutover, and prove 47 scripts. |
| WORK-115 | Perform independent terminal closure, reciprocal-lineage review, and PRD-007 resumption handoff. |

When WORK-104 moves the frozen Plan/Task to their Stage 03 destination, this
table explicitly supersedes the old destination WORK-105 through WORK-110
meanings. The source Stage 04 Plan/Task remain frozen in `WDTC-AMEND-001`; this
amendment does not claim their WORK-104 task complete. WORK-107 MUST NOT begin
before WORK-105's atomic acceptance.

### Work-unit inventory and mapping

The 2026-08-09 baseline contains 49 `spec.md` files, 65 authored Plans, and 67
authored Tasks. The earlier 39-triad/24-orphan/3-orphan-task classification is
a candidate inventory, not an execution truth; it is regenerated from current
HEAD before migration because Spec 053 completed after the earlier census.

The committed mapping enumerates every source, target, work-unit ID, slug,
current status, and disposition. Same-slug correspondence is evidence for
review, not an automatic move rule. A source cannot appear twice, a target
cannot appear twice, and an existing target blocks application.

### Document-governance consolidation

Stage 00's target `rules/document-authoring.md` absorbs the current stage
routing, authoring matrix, checklist, and documentation-protocol rules that
govern agent timing and execution. Stage 99's target
`support/document-contract.md` absorbs template selection, body, frontmatter,
and profile rationale; `support/document-lifecycle.md` absorbs lifecycle,
supersession, retention, archive, and legacy-disposition rationale.

The migration first builds a rule-to-owner ledger. A source document is
deleted only after every non-duplicate rule maps to one target section and all
consumers route to that target. Machine values are removed from prose when the
registry already owns them.

### AI-agent governance integration

The harness contract remains the provider-neutral owner. Its role roster is
not duplicated inside `agentSystems`; systems reference roles, permission
classes, evidence classes, evaluation suites, and provider surfaces by ID.
New schema definitions are closed and have positive and negative fixtures for
risk owner, prohibited use, untrusted data, tool coverage, oversight, stop,
approval binding, trace availability, evaluation adjudication, component
digest, and evidence-class non-promotion.

Existing `current` and `repository-static-evaluation-ready` values are renamed
or explicitly scoped so a reader cannot interpret them as provider enforced.
Consumer docs and adapters migrate in the same logical change as the schema.

### Validator and script disposition

The script audit starts from command consumers in pre-commit, workflows,
`validation-surfaces.json`, root/Stage 00 docs, tests, and active execution
records. Similar names do not establish duplication. For each candidate pair,
the audit compares rule owner, accepted arguments, input domain, exit behavior,
diagnostics, negative fixtures, lane, and downstream evidence.

`validate-repo-quality-gates.sh` is retained. Pre-commit and affected selection
use one declared orchestration path. WORK-112 removes only
`validate-harness.sh` after root README, PR template, tests, scripts index, and
current work-unit consumers migrate, reducing the inventory from 50 to 49.
WORK-114 removes only the transition manifest and migration tool after terminal
cutover, reducing it to exactly 47 (39 Python, seven shell, one README).
Active-corpus validators remain because their current rules and negative
fixtures are distinct. Historical lifecycle checks may be quarantined from the
hot path but are not deleted without the same proof. Similar filenames never
establish semantic duplication.

### One-time and generated cleanup

The progress ledger is rotated only after archived sections are recoverable
and linked. Stale tracked `graphify-out/**` content is treated as a generated
snapshot, verified for consumers and reproducibility, then removed or admitted
through an explicit governed snapshot route. Future scratch output is ignored.
Tracked `__pycache__` or equivalent one-time runtime residue is removed only by
exact path inventory; broad recursive deletion is forbidden.

## Data Modeling & Storage Strategy

### Migration mapping

```json
{
  "schemaVersion": 1,
  "mode": "transition",
  "entries": [
    {
      "source": "docs/04.execution/plans/<legacy-name>.md",
      "target": "docs/03.specs/<NNN>-<slug>/plan.md",
      "workUnit": "Spec-<NNN>",
      "disposition": "move-current",
      "sourceBlob": "<git-blob-sha>",
      "reviewed": true
    }
  ]
}
```

The production artifact may use the existing registry or a temporary ignored
review artifact as selected by the implementation plan. If tracked, it needs a
canonical profile and lifecycle; no unprofiled one-shot file is committed.

### Disposition ledger

The ledger records path, blob identity, classification, current consumer count,
unique rule/fixture count, successor or archive target, reviewer, and result.
Generated output additionally records generator, reproducibility command, and
whether the terminal output is tracked or ignored.

The terminal Stage 98 migration ledger is schema-versioned and separate from
that working disposition audit. Its required fields include:

```json
{
  "schema_version": 1,
  "migration_id": "MIG-0001",
  "legacy_path": "docs/98.archive/<legacy-path>",
  "stable_path": "docs/98.archive/<stable-path>",
  "artifact_id": "<typed-stable-id>",
  "action": "moved|merged|replaced|deleted",
  "replacement": "<artifact-id-or-null>",
  "source_commit": "<original-source-commit>",
  "legacy_archive_commit": "<old-envelope-commit>",
  "legacy_envelope_blob": "<old-envelope-git-blob>",
  "source_blob": "<original-source-git-blob>",
  "content_sha256": "<original-payload-sha256>",
  "record_kind": "change-plan|change-task|tombstone",
  "reason": "<reviewed-reason>"
}
```

The seven user-named fields remain required but are not the exclusive schema;
none of the 14 fields above may be renamed or omitted. `source_commit` and
`source_blob` identify the original archived source, while
`legacy_archive_commit` and `legacy_envelope_blob` identify the old envelope
before cutover. The current ledger is a 93-record historical bijection with all
actions `moved`; migration control documents are outside that count. Future
actions retain one unique terminal record per row as specified by DTC-15.

### Harness data

`agentSystems` references existing role, permission, evidence, evaluation, and
surface IDs rather than copying their values. The contract stores policy,
required record shapes, digests, redacted metadata, and immutable evidence
references; actual approval/trace/action records live append-only at the
approved Task, Runbook, Incident, or provider evidence owner. Approval argument
bodies, raw targets, and secret-bearing payloads are never stored. Trace policy
records `traceAvailability`, risk tier, and whether audit evidence is required.
A required but unavailable trace stops or stays `DEFER` unless an approved
operator Runbook records a bounded exception.

`evidenceOwnerPolicies` is a closed list keyed by the canonical
approval-boundary surface. Each entry names the owner type and canonical ID,
append principal class, Git or provider trust anchor, immutability rule,
retention class, and validator. Repository evidence is integrity-bound to a
reviewed Git blob and commit. Provider evidence resolves through
`provider-runtime-evidence.json`; a provider claim without its required
observed identity remains `DEFER`.

### Archive and memory

Terminal archive cutover preserves every original payload byte, source commit,
source blob, and content digest while recording the old ArchiveEnvelope Git
blob before an outer-wrapper/path transformation. The schema-versioned ledger
provides the reversible old-to-stable path mapping. Progress rotation uses the
approved terminal tombstone/change mechanism; the live ledger contains only
the approved current window after recovery validation passes.

## Interfaces & Data Structures

### Route validator interface

The document validators accept an explicit contract mode or derive it from one
closed registry state. They report the mode, selected profile, legacy target,
and ambiguity reason. They never choose a path by declaration order.

```text
validate-document-contract-registry --root . --mode strict --route-state legacy
validate-document-contract-registry --root . --mode strict --route-state transition
validate-document-contract-registry --root . --mode strict --route-state terminal
```

Exact command-line spelling is finalized by the implementation plan and tests;
the three-state behavior and fail-closed results are normative.

### Approval evidence interface

An approval record is created at its approved evidence owner before the action,
binds policy, action class, requester and approver principals, authority scope,
target and arguments digests, expires, and links the later result. Reject,
expiry, principal/scope/target/argument mismatch, missing immutable evidence,
or missing result produces a non-approved state; there is no fallback to a
broader task approval or self-asserted approver string. The owner policy
resolver also rejects an owner class inconsistent with the approval-boundary
surface, a writer outside `appendPrincipalClass`, or an unverifiable Git or
provider trust anchor.

### Validation selection interface

`validation-surfaces.json` remains the only machine owner of surface IDs,
tracked path selection, argv, lane, evidence class, and fallback. Wrappers call
that contract or the aggregate gate; they do not maintain a second validator
inventory.

## Edge Cases & Error Handling

| Condition | Deterministic behavior |
| --- | --- |
| Mapping source is missing, duplicated, or changed from its reviewed blob | Stop before writes and report the source entry. |
| Mapping target already exists or is named by another entry | Stop before writes and report both owners. |
| Transition produces both legacy and target active owners | Fail route validation; do not commit. |
| Plan lacks a sibling Spec, or Task lacks Spec/Plan | Fail work-unit validation with the missing sibling. |
| A date-prefixed mutable file has no registered identity exception | Fail profile validation and name the matched family. |
| An existing Stage 98 path changes outside the reviewed schema-versioned ledger or before recovery proof | Stop before writes and report the unowned transformation. |
| A Stage 98 payload, digest, `source_commit`, or `source_blob` changes during cutover | Stop; wrapper/path migration cannot alter historical payload or provenance. |
| A terminal `artifact_id` is duplicate, mistyped, aliased, noncanonical, or differs from its path ID | Fail terminal identity validation and report both owners. |
| A Stage 00/90/99, governance memory/progress, README/navigation, template, fixture, native/generated, or embedded immutable-payload surface declares `artifact_id` | Fail namespace selection and report the prohibited profile/path. |
| An authored `sdlc/api-spec`, `api-spec.md`, or authored API Spec template survives terminal mode, or a native contract is reclassified as authored API Spec | Fail terminal form validation; require WORK-105 retirement/negative-fixture evidence while preserving the native profile. |
| The authored API Spec instance census is zero but a consumer class is unscanned, live, or unclassified | Fail WORK-105 acceptance; instance zero cannot substitute for complete consumer disposition. |
| Immutable history or native evidence still matches the grep classifier after `retain-history` / `retain-native` disposition | Permit the classified reference; terminal acceptance requires zero live/unclassified consumers, not literal grep zero. |
| A historical `api-spec.md` appears without a reviewed Interface/`IFC` tombstone ledger disposition | Stop terminal entry; do not infer an `API-SPEC` tombstone type. |
| A Stage 98 change directory is treated as frontmatter-bearing or declares `artifact_id`, a leaf lacks the parent `change_id` or its typed outer ID, siblings disagree, or a tombstone stage/type pair is outside the closed map | Fail path/frontmatter validation before cutover. |
| A tombstone fallback token is truncated, does not match the full canonical-path/source-blob digest, or aliases another spelling | Fail tombstone identity validation and report the computed token and owner. |
| Two ledger rows share a stable path, or a future merged/replaced/deleted row lacks its unique tombstone evidence | Stop; every source retains one independently addressable terminal record. |
| A current non-Stage-98 document links directly to a stable record instead of the collection README | Fail the direct-link corpus check; only Stage 98 README/migration index-provenance links are excepted. |
| WORK-107 Stage 98 rehome starts before WORK-105 atomic acceptance | Stop before writes; transition archive invariants remain authoritative. |
| A Stage 90 observation body would be rewritten | Stop and require retain/annotation/merge disposition review. |
| A deleted script still has a consumer or unique negative fixture | Retain it and record `retain-contract`. |
| A static record claims provider enforcement or action execution | Fail evidence non-promotion validation. |
| Approval policy, principals, scope, target, argument digest, expiry, or result does not match | Reject the action evidence and require a new approval. |
| Approval evidence owner, append principal, retention, validator, or trust anchor does not match the surface policy | Reject the record; retain `DEFER` and require the canonical owner/controller. |
| Required high-risk trace collection is unavailable | Stop or retain `DEFER`; only a separately approved operator-Runbook exception may proceed. |
| Baseline gate fails for a new reason | Stop and isolate the regression from the recorded pre-change failures. |
| Baseline defect remains at terminal cutover | Do not mark the program done. |

## Failure Modes & Fallback / Human Escalation

Each logical commit must pass its focused tests, affected lane, registry and
document checks, archive diff boundary, `git diff --check`, and the aggregate
gate applicable to its scope. The final state additionally requires
`pre-commit run --all-files` PASS. Recorded baseline failures are not accepted
terminal exceptions.

If a tranche fails, retain its evidence, reverse only that uncommitted tranche
with a reviewed patch or revert its isolated commit, and re-run the last known
green state. Never use a broad destructive reset. Contract consolidation that
cannot preserve a rule or fixture is deferred as `retain-contract`, not forced
through for line-count reduction.

Human escalation is required for any unledgered edit to an existing archive
record, payload/provenance mutation, uncertain historical disposition, removal
of a unique rule or fixture, unapproved lifecycle identifier change, new
document family, evidence-class promotion, credential or secret access,
external write, remote action, or live mutation.

## Verification Commands

```bash
# Document profile, route, body, and link contracts.
python3 scripts/migrate-document-work-units.py --root . --manifest scripts/document-taxonomy-migration.json --check
python3 scripts/validate-document-contract-registry.py --root . --self-test
python3 scripts/validate-document-contract-registry.py --root . --mode strict
python3 scripts/validate-markdown-profiles.py --root . --mode strict
python3 scripts/validate-links-and-owners.py --root . --mode strict

# Archive integrity and agent-governance contracts.
python3 -m unittest tests/test_archive_validation.py
python3 scripts/archive_cutover.py --root .
python3 scripts/validate-agent-harness-contract.py --root .
python3 scripts/validate-agent-harness-semantics.py --root .

# Aggregate and all-files repository-static evidence.
git diff --check
bash scripts/validate-repo-quality-gates.sh .
pre-commit run --all-files
```

The recorded pre-change all-files run failed before design edits: the document
registry self-test could not allocate its configured temporary directory,
detect-secrets reported three existing findings and tried to rewrite its
baseline, and Markdown lint found an H1-to-H3 increment in the completed Spec
053 Plan. The hook-created baseline change was reverted and the isolated
worktree returned to clean. These results are baseline evidence only.

All commands above are repository-static. They do not prove provider runtime,
hosted CI, remote settings, secret safety, deployment, or live operation.

## Success Criteria & Verification Plan

| Criterion ID | Criterion | Evidence |
| --- | --- | --- |
| VAL-WDTC-001 | Every retained Spec/Plan/Task resolves in one Stage 03 work unit and no live Stage 04 execution path remains. | Reviewed mapping, terminal inventory, locality and route negative fixtures. |
| VAL-WDTC-002 | Stage 05 remains stable and no Release-family route or artifact exists. | Path inventory and focused registry/residue search. |
| VAL-WDTC-003 | Mutable authored filenames are date-free, terminal Stage 98 has no date/year path, and every remaining date-identity exception is registered. | Profile inventory, exception fixtures, and frontmatter preservation diff. |
| VAL-WDTC-004 | PRD-008 transition lineage and registry projection remain `decision=0023` until WORK-105 atomically accepts terminal/current ADR-0024; all active relations remain reciprocal without renumbering. | Registry projection, ADR-0018/ADR-0023/ARD-0011/ADR-0024 reciprocal links, and lifecycle traceability results. |
| VAL-WDTC-005 | Stage 00/99 prose and the document registry have disjoint human and machine authority. | Rule-to-owner ledger, duplicate-rule scan, profile/template validation. |
| VAL-WDTC-006 | Every removed path has a reviewed disposition; Stage 98 payload/provenance is immutable and any outer-wrapper/path migration is ledger-backed. | Disposition ledger, source blobs, archive validation, and old-object recovery proof. |
| VAL-WDTC-007 | Validator/script reduction removes no live consumer, rule, or unique negative fixture. | Consumer graph, semantic comparison, fixture mutation results, declared/executable parity. |
| VAL-WDTC-008 | Harness systems record risk, trust, oversight, approval, trace, evaluation, and provenance with non-promotable evidence. | Schema positive/negative fixtures and agent-governance semantic validation. |
| VAL-WDTC-009 | Progress and generated-output cleanup is recoverable and leaves no unowned tracked artifact. | Archive recovery, consumer/reproducibility checks, ignored-path and registry results. |
| VAL-WDTC-010 | The three pre-change validation failures and all migration regressions are closed. | Aggregate and all-files PASS with explicit secret-finding adjudication. |
| VAL-WDTC-011 | Specs 047–051 remain unexecuted during migration and have a valid consolidated resumption route. | Status, task evidence, and final path inventory. |
| VAL-WDTC-012 | No provider, hosted, remote, credential-bearing, or live result is claimed or performed. | Handoff evidence-class report and change inventory. |
| VAL-WDTC-013 | Terminal active forms are PRD, optional SRS, optional Stage 01 Interface Requirement, AD (`sdlc/ad`), and ADR; ARD/RFC and authored `sdlc/api-spec` have no terminal surface, ARD-0011 becomes AD-0011, and native API contracts remain separate Interface evidence. | Terminal registry/profile/template/route/navigation inventory, independent zero authored-instance proof, complete full-grep consumer disposition with zero live/unclassified results, retired-route negative fixtures, native/history retention classifications, and preserved-ID mapping. |
| VAL-WDTC-014 | Every mandatory terminal outer profile has exactly one globally unique, type-valid `artifact_id` equal to its deterministic path-derived value; every excluded profile, including authored `sdlc/api-spec`, prohibits the field; API Spec retirement independently proves zero instances and zero live/unclassified consumers after complete classification; native API contract identity stays separate; and virtual `CHG-####` remains `change_id` only. | Mandatory/prohibited namespace selection; full consumer-class coverage across profile/template/relationships, positive fixture, lifecycle, registry, authoring hook/routing, Stage 00/03 prose, validators/tests/docs/fixtures; migration/negative/retention dispositions; native-contract non-promotion; and global identity/path fixtures. |
| VAL-WDTC-015 | The current 93 records map 93-to-93 with action `moved`, unique stable paths, exact `35/2/4` execution grouping and `3/8/4/2` tombstones; future actions retain unique terminal evidence. | Schema-versioned 14-field ledger, action/replacement/stable-path negatives, payload/provenance digests, old-envelope proof, and dual recovery. |
| VAL-WDTC-016 | The exact tracked script closure is `50 -> 49 -> 47`, deleting only `validate-harness.sh` in WORK-112 and the transition JSON/tool in WORK-114. | Full 50-row disposition ledger, consumer/argument/diagnostic/fixture/evidence/recovery comparison, scripts README parity, and exact language-count census. |

## Traceability

- **Program requirement**:
  [PRD-008](../../01.requirements/008-workspace-document-taxonomy-consolidation.md)
- **Architecture**:
  [ARD-0011](../../02.architecture/requirements/0011-document-taxonomy-consolidation-architecture.md)
- **Accepted full-body archive predecessor**:
  [ADR-0018](../../02.architecture/decisions/0018-full-body-archive-record-and-retention.md)
- **Accepted decision and PRD-008 lineage authority**:
  [ADR-0023](../../02.architecture/decisions/0023-work-unit-document-taxonomy-and-governance-authority.md)
- **Terminal/current successor design pending WORK-105 atomic AD/invariant/acceptance/projection**:
  [ADR-0024](../../02.architecture/decisions/0024-terminal-artifact-identity-and-archive-layout.md)
- **Approved implementation Plan and Task, to move during transition**:
  [legacy Plan](../../04.execution/plans/2026-08-07-document-taxonomy-consolidation.md)
  and [legacy Task](../../04.execution/tasks/2026-08-07-document-taxonomy-consolidation.md)
- **External evidence boundary**:
  [Spec-driven SDLC and document contracts](../../90.references/research/2026-08-08-wer/spec-driven-sdlc-and-document-contracts.md)
  and [AI agents and Agency Agents](../../90.references/research/2026-08-08-wer/ai-agents-and-agency-agents.md)
- **Suspended program**:
  [PRD-007](../../01.requirements/007-repository-delivery-and-platform-assurance.md)

### Lifecycle Traceability

| PRD requirement | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-WDTC-001](../../01.requirements/008-workspace-document-taxonomy-consolidation.md#functional-requirements) | VAL-WDTC-001 | Mapping and terminal route/locality fixtures prove Stage 03 co-location and Stage 04 retirement. |
| N/A — REQ-WDTC-002 shares the PRD source above. | VAL-WDTC-003 | Filename/frontmatter inventory and exception fixtures prove stable identity. |
| N/A — REQ-WDTC-003 and REQ-WDTC-007 share the PRD source above. | VAL-WDTC-002 | Residue and registry checks prove Stage 05 stability and Release exclusion. |
| N/A — REQ-WDTC-004 shares the PRD source above. | VAL-WDTC-004 | Registry and reciprocal-link validation prove stable lineage. |
| N/A — REQ-WDTC-005 and REQ-WDTC-006 share the PRD source above. | VAL-WDTC-005 | Rule-owner and profile/template checks prove authority separation. |
| N/A — REQ-WDTC-008 through REQ-WDTC-010 share the PRD source above. | VAL-WDTC-006 | Disposition, source-blob, archive, and path results prove safe migration. |
| N/A — REQ-WDTC-011 and REQ-WDTC-012 share the PRD source above. | VAL-WDTC-007 | Consumer, rule, fixture, and parity evidence prove safe script reconciliation. |
| N/A — REQ-WDTC-013 and REQ-WDTC-014 share the PRD source above. | VAL-WDTC-008 | Harness schema and semantic fixtures prove governance and evidence boundaries. |
| N/A — REQ-WDTC-015 shares the PRD source above. | VAL-WDTC-009 | Recovery and reproducibility evidence prove bounded cleanup. |
| N/A — REQ-WDTC-016 shares the PRD source above. | VAL-WDTC-010 | Aggregate and all-files PASS prove baseline and regression closure. |
| N/A — REQ-WDTC-017 shares the PRD source above. | VAL-WDTC-011 | Status and path evidence prove suspension and resumption safety. |
| N/A — REQ-WDTC-018 shares the PRD source above. | VAL-WDTC-012 | Evidence-class handoff proves local-only scope. |
| N/A — REQ-WDTC-019 shares the PRD source above. | VAL-WDTC-013 | Terminal inventory, independent authored instance/consumer gates, complete classification, retired-route negatives, native/history retention, and preserved-ID mapping prove the approved document taxonomy. |
| N/A — REQ-WDTC-020 shares the PRD source above. | VAL-WDTC-014 | Mandatory/prohibited selection, complete API Spec consumer disposition, native-contract non-promotion, global uniqueness, canonical typed-ID, virtual change-ID, tombstone digest, and path/frontmatter fixtures prove artifact identity. |
| N/A — REQ-WDTC-021 shares the PRD source above. | VAL-WDTC-015 | Exact ledger census, immutable payload/provenance, old-object evidence, and recovery prove the 93-row Stage 98 bijection. |
| N/A — REQ-WDTC-022 shares the PRD source above. | VAL-WDTC-016 | Exact staged inventories and the 50-row semantic disposition ledger prove `50 -> 49 -> 47` closure. |
