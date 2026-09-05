---
title: "SDLC Document and AI Agent Governance Consolidation Technical Specification"
version: "1.2.0"
type: "sdlc/spec"
status: "active"
owner: "platform"
updated: "2026-09-04"
layer: "specs"
artifact_id: "SPEC-0054"
---

# SDLC Document and AI Agent Governance Consolidation Technical Specification (Spec)

## Overview

This specification defines the approved B-scope consolidation of the
repository's SDLC documents, Spec-driven development workflow, AI-agent
governance, templates, validators, scripts, operations material, Stage 90
references, and the Stage 98 retention and history surface.

The target is a small set of canonical document owners with deterministic
four-digit identities, work-unit-local Spec/Plan/Task artifacts, one shared
agent-governance control plane with Codex and Claude adapters, and validators
that implement machine contracts without restating them. The design is based
on official ISO, NIST, GitHub Spec Kit, OpenSpec, Diataxis, Google SRE, Git,
OpenAI, Anthropic, and repository evidence reviewed through 2026-08-20.

This specification succeeds, reconciles, or retires conflicting current
instructions. It does not silently rewrite completed evidence. Current rules
that conflict with this specification receive a package-local disposition and
consumer/recovery proof before their active owners are removed. Reachable Git
history is the default exact-byte recovery source. Retained documents under
Stage 98 may be cited as historical trace, but neither they nor sealed Archive
records become current semantic authority or a routine deletion prerequisite.

Direct human approval on 2026-08-13 authorizes B-scope consolidation including
Stage 90. This integrated program inherits the incomplete WORK-109 candidate
from [Spec 0052](../0052-document-taxonomy-consolidation/spec.md), but accepts
only the portions that satisfy this specification after staged-index review.
The original direct-approval lineage was recorded by
[ADR-0022](../../02.architecture/decisions/0022-direct-approval-standalone-execution-lineage.md),
which remains predecessor context but no longer owns a global standalone
execution projection under
[accepted ADR-0031](../../02.architecture/decisions/0031-current-corpus-retention-and-validation-ownership.md).
The four-digit current-path and Incident identity decision is
[ADR-0025](../../02.architecture/decisions/0025-four-digit-document-path-identity.md),
which transfers the active WORK-109 implementation from Spec 0052 to this
specification's WORK-054-002 package.

Direct human approval on 2026-08-13 authorizes this Spec-owned execution
relation. No separate PRD or Architecture Description is required for this
package-local lifecycle. ADR-0025 owns the topology decision; accepted
ADR-0031 owns the current-corpus and validation-routing model; and
[accepted ADR-0032](../../02.architecture/decisions/0032-completed-and-terminal-document-retention.md)
owns the retention model that replaces deletion as the disposition for
completed, stale, and deprecated documents in WP-013 and WP-009.
[accepted ADR-0033](../../02.architecture/decisions/0033-common-document-contract-v9.md)
owns the scoped common-envelope, public Registry v9, template grammar, and
generation-aware Archive validation amendment implemented by the current
WP-013 change slice.

The retained current semantic owners are
[REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md) and
[AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md).
Their explicit requirement-member and architecture-responsibility transfer mappings
own the durable obligations inherited from REQ-0005/0006/0008 and AD-0008/0009/0011;
this reciprocal trace does not rewrite the original directly approved execution lineage.

Until WP-013 removes the parent-only compatibility roster, the current registry
still requires these two historical compatibility statements:

Direct human approval on 2026-08-13 authorizes this standalone execution relation.
No separate PRD or Architecture Description is required or part of this standalone lifecycle.

They preserve the current gate input only; they do not create a second program
owner or override the package-local delegation designed by ADR-0031.

Direct human approval on 2026-08-14 refines that topology into package-oriented
requirements, prefix-free architecture paths, a bounded Stage 90 library,
an explicitly classified Stage 98 retention/history surface, and a single Stage 99 registry. This
revision supersedes the earlier PRD/SRS/Interface Requirement form split,
`ad-`/`adr-` route prefixes, support-prose control plane, and snapshot-count or
line-digest Archive design. It retains the approved four-digit identity,
Incident route, work-unit co-location, immutable source recovery, and logical
commit boundaries.

Direct human approvals through 2026-08-20 establish
[ADR-0030](../../02.architecture/decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md)
as the terminal authority for this program. The approved migration strategy is
**authority-first incremental convergence**: establish each terminal machine
owner before moving its corpus, remove related duplication in the same work
package, and close repository-wide ownership in WP-010 and the final fixed
point in WP-014. The new decision supersedes conflicting terminal-shape,
provider-cardinality, archive-census, and script-census clauses of earlier
decisions while preserving their transition-safety and recoverability goals.

The reciprocal execution artifacts are [Plan 0054](plan.md) and
[Tasks 0054](plan.md).
Spec 0054 remains the integrated acceptance owner. Active
[Spec 0066](../../98.archive/completed/03.specs/0066-validation-tooling-ownership/spec.md) is the delegated
execution package for WP-010 and WP-011; it is not a standalone program.
SPEC-0054-TSK-0011 is the current parent acceptance record.

## Strategic Boundaries & Non-goals

### Authorized scope

- Reconcile the active document taxonomy and every current consumer.
- Normalize active SDLC numeric identities to four digits.
- Keep dates in frontmatter or evidence metadata rather than ordinary active
  filenames.
- Adopt the exact Incident route
  `docs/05.operations/incidents/<year>/inc-####-<slug>/`.
- Consolidate templates, registries, validators, fixtures, navigation, and
  cross-links with the document taxonomy.
- Keep root `DESIGN.md` as the canonical UI and design-system guide rather
  than treating it as an SDLC work-unit design artifact.
- Consolidate the shared AI-agent control plane and provider-specific native
  adapters without claiming unobserved runtime behavior.
- Reduce validator, aggregate-gate, fixture, and mutable-SHA complexity while
  preserving every permanent semantic rule and recovery guarantee.
- Review every tracked file in `scripts/`, migrate consumers, and remove only
  assets whose replacement and recovery evidence are complete.
- Review Stage 90 current references, generated indexes, research packs,
  snapshots, and audits by semantic owner. Keep the point-in-time disposition
  in the executing Task and reviewed diff rather than a permanent census.
- Use reachable Git history as the exact-byte recovery owner. Do not create a
  sealed Archive record or redirect as a current-document dependency or
  routine condition for retiring an owner. Retain terminal governed documents
  only through the accepted ADR-0032 package-retention route.
- Commit each independently testable logical unit separately.

### Protected boundaries

- Git history is not rewritten.
- Existing sealed Stage 98 records are not edited or compacted to make current
  validators pass. A record may be removed after reachable Git recovery is
  confirmed; mutable branch or remote-ancestry parity is not current policy.
- Stage 90 audit and source-provenance evidence is not cosmetically rewritten.
  It is retained, merged, or removed through a reviewed disposition, with
  reachable Git history as the default recovery owner.
- External publication, deployment, push, merge, release creation, live
  provider execution, and credential-bearing actions are outside this scope.
- `docs/05.operations/releases/` is not a supported family. Deployment
  execution belongs to a Spec Task or Runbook; published release identity and
  notes belong to Git tags and GitHub Releases.

## Contracts

### C-SDLC-001 — canonical document topology

The terminal active topology is:

```text
docs/
├── 00.agent-governance/
│   ├── README.md
│   ├── sdlc.md
│   ├── policies/
│   ├── roles/
│   ├── providers/
│   │   ├── claude.md
│   │   └── codex.md
│   └── skills/
├── 01.requirements/
│   ├── README.md
│   └── ####-<slug>.md
├── 02.architecture/
│   ├── README.md
│   ├── descriptions/####-<slug>.md
│   └── decisions/####-<slug>.md
├── 03.specs/
│   └── ####-<slug>/
│       ├── README.md
│       ├── spec.md
│       ├── plan.md
│       └── tasks/tsk-####-<slug>.md
├── 05.operations/
│   ├── README.md
│   ├── guides/####-<slug>.md
│   ├── incidents/<year>/inc-####-<slug>/
│   │   ├── incident.md
│   │   └── postmortem.md
│   ├── policies/####-<slug>.md
│   └── runbooks/####-<slug>.md
├── 90.references/
│   ├── README.md
│   ├── research/####-<slug>/
│   ├── audits/####-<slug>/
│   └── data/####-<slug>/
├── 98.archive/
│   ├── README.md
│   ├── migrations/####-<slug>.md
│   └── tombstones/<original-stage>/####-<slug>.md
└── 99.templates/
    ├── README.md
    ├── registry.json
    ├── contracts/
    │   ├── frontmatter.schema.json
    │   └── document-profile.schema.json
    └── templates/
        ├── governance/
        ├── requirements/
        ├── architecture/
        ├── specs/
        ├── operations/
        ├── references/
        └── common/

docs/00.agent-governance/
├── roles/registry.json
├── roles/registry.schema.json
├── roles/<role-id>.md
└── skills/<skill-id>/SKILL.md

.claude/
├── CLAUDE.md
├── agents/
└── <native-config>

.codex/
├── CODEX.md
├── agents/
└── <native-config>

scripts/
├── README.md
├── docs/
├── setup/
├── qa/
├── validation/
│   ├── documents/
│   ├── agents/
│   ├── archive/
│   └── repository/
└── lib/

tests/
├── <independent validator tests>
└── fixtures/
    └── <test-only case data>
```

`00` is the human AI-agent governance plane, `90` is the non-authoritative
reference library, `98` is the isolated historical archive, and `99` is the
document-template and contract plane. They are not sequential SDLC approval
stages.

The terminal tree contains no `.gemini/` directory and no root `GEMINI.md`.
The repository-owned `.agents/` tree is removed under
[SPEC-0072](../0072-agent-governance-and-quality-gate-consolidation/spec.md).
Codex and Claude are the only supported provider adapters.

### C-SDLC-002 — requirements and architecture ownership

`docs/01.requirements/####-<slug>.md` is one Requirement Package with
stable `REQ-####` identity. It combines the problem and goal, users and
stakeholders, functional and non-functional requirements, constraints,
external interface requirements, acceptance criteria, and links to related
Architecture and Spec artifacts. Stage 01 owns long-lived,
solution-independent requirements; it does not repeat one requirement across
separate PRD, SRS, and Interface Requirement documents.

Package members use the package identity as their global namespace:

```text
REQ-####-FR-####   functional requirement
REQ-####-NFR-####  non-functional requirement
REQ-####-IF-####   external interface requirement
```

The leading `REQ-####` must equal the containing Package `artifact_id`.
`FR`, `NFR`, and `IF` sequences are independent, four-digit, append-only
number spaces within that Package. A member ID is unique repository-wide and
is never reused for a different statement. Moving or splitting a requirement
into another Package creates a new member ID and an explicit migration or
supersession relation to the former ID; it does not silently retain the old
namespace. Cross-document links use the complete member ID. An `IF` member
states the solution-independent interface need; the executable OpenAPI,
GraphQL, or Protobuf contract remains owned by its implementing Spec Package.

`docs/02.architecture/descriptions/####-<slug>.md` owns current system
structure, boundaries, components, data flow, and deployment views under a
stable `AD-####` frontmatter identity.
`docs/02.architecture/decisions/####-<slug>.md` owns important choice context,
alternatives, decision, consequences, and supersession under stable
`ADR-####` identity. The parent directory determines the route type, so
`ad-` and `adr-` filename prefixes are not used. A superseded ADR stays in the
decision log and links reciprocally to its successor; it is not deleted or
moved to Archive.

Every retained Requirement Package and Architecture Description is reconciled
against the current repository implementation, including manifests,
configuration, executable code, validation entrypoints, and supported
operational interfaces. Stage 01 states the solution-independent goals,
functional behavior, quality attributes, constraints, and external-interface
needs that the implemented system currently satisfies. Stage 02 describes the
actual current structure, boundaries, components, data/control/deployment
flows, and important design choices. A future-only change belongs to an active
Spec until implemented; it must not be presented as current architecture.

The parity is bidirectional: durable implemented behavior has an appropriate
Stage 01 requirement owner and, where structural explanation is needed, a
Stage 02 owner; retained Stage 01/02 claims must have implementation evidence
or an explicit non-implementation status allowed by their lifecycle. Raw
inventories and transient snapshots are not copied into requirements or
architecture. They remain direct repository evidence or bounded Stage 90
supporting material linked from the canonical current owner.

The retired Stage 02 requirements route is not an active terminal owner. Any
remaining record is merged into a Requirement Package, converted to an
Architecture Description, or dispositioned as historical evidence.

The reviewed convergence target keeps and rewrites Requirement Packages
`0001` through `0004`; Packages `0005` through `0008` are removed after their
unique requirements and mutable consumers move to those owners. Architecture
Descriptions `0004` through `0007` remain current and are updated;
Descriptions `0008` through `0011` are retired after their unique structural
content and consumers move. These sets are reviewed semantic targets, not
fixed-count gate inputs.

All ADRs remain in the Stage 02 decision log. Their status and reciprocal
supersession links are reconciled, including accepted ADR-0031 and its five
superseded predecessors; an obsolete decision is superseded rather than
deleted as corpus cleanup.

### C-SDLC-003 — work-unit-local Spec-driven execution

One work unit owns a thin router `README.md`, `spec.md`, `plan.md`, and one or
more task records under `tasks/` in the same
`docs/03.specs/####-<slug>/` directory. The router has no `artifact_id`,
lifecycle, or duplicated contract body. The Spec owns change goals, observable
behavior, Technical Approach, Acceptance Contract, interfaces, and failure
conditions. The Plan owns implementation order, test strategy, risk,
rollback, and recovery. Each Task owns one independently reviewable execution
unit and its evidence.

A Task path is `tasks/tsk-####-<slug>.md`; its stable identity is
`TSK-<SPEC-NUMBER>-<TASK-SEQUENCE>`, for example `SPEC-0054-TSK-0001`.
The directory sequence and final Task sequence must agree. Task numbers are
append-only within a Spec Package and are never reused. Cross-artifact
validators reject identifier, lifecycle, criterion, path, dependency, or
evidence drift.

Stage 03 does not own `design.md`, `tests.md`, `agent-design.md`,
`data-model.md`, or a monolithic `tasks.md` as permanent artifact families.
Change-local design moves to `spec.md`; ordering, test strategy, and rollback
move to `plan.md`; execution evidence moves to Task records. A long-lived
structural description or important choice is promoted to Stage 02 before the
old file is removed. Under accepted ADR-0031, validator tests and fixtures
remain independent under the top-level `tests/` tree and production validators
never import or read them.

Executable interface contracts such as OpenAPI, GraphQL, and Protobuf belong
to the Spec Package that implements and validates them. Stage 01 records the
solution-independent external interface requirement and links to that
executable contract without duplicating it.

Concurrency is package-local: each Spec Package has at most one
`in-progress` Task. A parent integration Spec and an explicitly delegated
execution Spec may therefore progress concurrently while preserving one
acceptance owner and one execution owner for each criterion. Spec 0054 owns
integration acceptance through SPEC-0054-TSK-0011; Spec 0066 owns delegated
execution of WP-010 and WP-011 after activation.

Execution-component links remain package-local. Spec 0066 Plan and Task link
reciprocally to each other and their own Spec; they do not link a parent Plan
or Task merely to inherit its registry ownership. Spec 0054 and Spec 0066 link
reciprocally at Spec level, and accepted ADR-0031 authorizes that delegation.
The link gate added by SPEC-0054-TSK-0010 admits exactly that closed delegated
relation and rejects missing reciprocity, a proposed decision, multiple parent
owners, foreign execution-component links, or a duplicate Spec 0066
standalone row.

The current-corpus convergence target retains packages `0004`, `0005`,
`0008`, `0054`, and `0066`. Other packages are migration input, not a
permanent roster: they leave the current tree only after lifecycle
normalization, mutable-consumer cutover, and Git recovery are proven. The
observed candidate count is never a validation invariant.

The retired Stage 04 execution route is not restored as an active owner. Its
numeric slot remains unused so retired links are not silently reinterpreted.

### C-SDLC-004 — four-digit and date policy

Active SDLC filenames and directory identities use four digits. Parent
directories determine Requirement Package, Architecture Description, ADR,
and Research types; their paths do not repeat type prefixes.
Stable frontmatter IDs retain their typed forms, including `REQ-`, `AD-`,
`ADR-`, `RES-`, and `AUD-`. The Incident route retains its required `inc-`
prefix. Ordinary active filenames do not contain dates. Dates stay in
frontmatter or typed event metadata. The preserved externally researched pack
keeps its approved date-bearing path while Spec 0062 consumes it; this stable
evidence path is a bounded exception, not a naming rule for new packages.

The closed Incident exception is:

```text
docs/05.operations/incidents/<year>/inc-####-<slug>/incident.md
docs/05.operations/incidents/<year>/inc-####-<slug>/postmortem.md
```

The year is an event partition and part of `INC-<YYYY>-<DDDD>` and
`POSTMORTEM-<YYYY>-<DDDD>`, not a general authorization for dated filenames.

### C-SDLC-005 — operations family boundaries

- Guide: learning, onboarding, explanation, or low-risk goal-oriented use.
- Policy: normative control, responsibility, approval, exception, and required
  evidence.
- Runbook: trigger-driven operator procedure with permission, stop condition,
  verification, recovery, rollback, and escalation.
- Incident: contemporaneous facts, impact, timeline, roles, and redacted
  evidence.
- Postmortem: blameless causes, contributing factors, learning, and owned
  preventive actions.

Overlapping Guide and Runbook pairs are merged or rewritten so one canonical
owner remains for each procedure. Release publication remains owned by Git
tags/GitHub Releases. Any current local Release profile, template, route,
fixture, validator rule, or document is deleted after consumer migration and
recoverability proof; this program does not preserve a dormant Release family.

The reviewed Stage 05 convergence keeps and rewrites Guide `0010`; Guides
`0001`, `0002`, `0003`, `0006`, `0007`, `0008`, and `0009` merge into their
semantic owners and are then removed. Policies `0001`, `0003`, `0004`,
`0005`, and `0007` remain current; Policy `0002` merges into `0001` and Policy
`0006` merges into `0005`. The nine existing Runbooks remain procedure owners
and are rewritten to remove duplicated policy, unsafe live actions, and
secret-bearing examples. These reviewed sets guide the cutover but are not
cardinality invariants. Incident and Postmortem profiles are strengthened for
role, timeline, evidence, cause, action-owner, due-state, and closure semantics.

### C-SDLC-006 — integrated AI-agent governance

`docs/00.agent-governance/` is the human governance control plane:

- `sdlc.md` owns the Requirements → Architecture → Spec → Implementation →
  Operations flow;
- `policies/` owns approval, security, quality, data, Git, and SDLC norms;
- `roles/` owns responsibilities, boundaries, and handoff semantics;
- `providers/` owns only Codex and Claude capability differences;
- `skills/` owns skill approval, authoring, and lifecycle policy.

The former `rules/`, `scopes/`, `contracts/`, `hooks/`, and `memory/` trees are
not terminal owners. Their unique durable content moves to the owners above,
to the responsible Spec Task or Stage 90 Data record, or to executable
`scripts/` owners before duplicate and transition content is removed.

`docs/00.agent-governance/roles/registry.json`, validated by its adjacent
`registry.schema.json`, is the sole machine owner for role IDs, permission
classes, handoff edges, and skill references. Canonical role bodies and skill
procedures live in Stage 00 `roles/` and `skills/`. `.claude/` and `.codex/` contain only provider-native thin
adapters and configuration. Stage 99 does not own agent contracts.

Gemini and Antigravity are removed from current governance: `.gemini/`, root
`GEMINI.md`, Gemini provider notes, contracts, validators, canaries, hooks,
fixtures, adapter projections, and Gemini/Antigravity-specific executable meaning must reach zero current
consumers before deletion. Historical
claims are recovered through reachable Git history; current governance does
not depend on an Archive record.

The permanent agent validation surface contains three responsibilities:
agent-registry/schema integrity, provider projection/config integrity, and
semantic/permission integrity. The aggregate gate invokes these validators but
does not reproduce their rules. Repository-static presence, provider
discovery, authenticated execution, hosted CI, and live evidence remain
separate evidence classes.

Tracked provider configuration and evidence are secret-free. Validators and
agents do not collect or mutate user/private authentication configuration,
credential paths, tokens, or raw transcripts. Hosted CI contains no provider
credential; an authenticated canary is explicit local/manual work and records
only redacted, secret-free results. Checkpoint or handoff state contains only
bounded task and validation summaries. CI permissions follow least privilege
and third-party actions retain supply-chain identity pins where byte or commit
identity is the security contract.

### C-SDLC-007 — template and validator single contract

Every active authored profile has one canonical registry definition for its
route, identity, frontmatter, lifecycle, and relationship rules, plus a
directly copyable template when authoring requires one. Semantic tests cover
the contract without making a fixture, schema, profile, or template count a
policy invariant. `docs/99.templates/registry.json` is the only machine
authority for path, profile, required sections, lifecycle, and ID rules.
`contracts/frontmatter.schema.json` and
`contracts/document-profile.schema.json` validate frontmatter and the registry
itself. `templates/` contains directly copyable forms grouped under
`governance/`, `requirements/`, `architecture/`, `specs/`, `operations/`,
`references/`, and `common/`.

Stage 99 `README.md` is the single human router. Former `support/*.md` rules
are merged into that README or the registry and then removed.
`templates/changes/` becomes `templates/specs/`. The removed
`design.template.md`, `tests.template.md`, and separate PRD/SRS/Interface
Requirement templates converge into the Spec/Plan/Tasks and Requirement
Package templates. Templates reference a registry profile ID rather than
hardcoding their destination paths or restating validator behavior.

The v9 registry exposes only `$schema`, `$id`, `schema_version`, `profiles`, and
`lifecycle_domains`. It does not retain current-instance rosters or parallel
program/reference control planes: the former v8 `programLineage.programs`,
`referenceCurrentPacks`, and `standaloneExecutions` fields are removed. The
`data-model` profile/template, full-body Archive profile/template, and stale
progress or memory forms are removed with their consumers. Retained historical
records receive only the bounded safety and readability checks defined by
C-SDLC-009; they do not require an active authoring profile or template.

The registry owns these profile-specific lifecycle domains and transitions:

| Profile family | Lifecycle |
| --- | --- |
| Requirement Package / Architecture Description | `draft → active → superseded \| retired`; `draft → withdrawn` |
| ADR | `proposed → accepted \| rejected`; `accepted → superseded` |
| Spec / Plan | `draft → active → done \| superseded \| withdrawn` |
| Task | `queued → in-progress`; `in-progress → done \| cancelled`; `in-progress ↔ blocked` |
| Governance / Guide / Policy / Runbook | `draft → active → superseded \| retired` |
| Incident | `open → mitigated → resolved → closed` |
| Postmortem | `draft → published → superseded` |
| Migration | `draft → accepted → sealed`; `draft → sealed` |
| Tombstone | `archived` only; created finished and byte-immutable |
| Audit | `draft → completed → invalidated` |
| Research | `draft → published → superseded \| retired` |
| Data | `draft → active → stale → superseded \| retired` |
| Template / Profile | none of its own; a form inherits its source profile's domain |

The three reference roles have three shapes, not one. An audit finding is
completed at a point in time and later invalidated by a re-observation; a
research report is published and then superseded by a refresh or retired; a
dataset is active until it goes stale. A form is the one row with no graph:
`mode: template` is skipped by the state machine, and the `status` a form
carries is the entry value of the document it produces, so a graph there would
assert movement that cannot happen.

No new Task transition is required for delegated ownership transfer. The
activation transaction uses existing edges: SPEC-0054-TSK-0010 moves from
`in-progress` to `done`, SPEC-0054-TSK-0011 moves from `queued` to
`in-progress` as the parent acceptance owner, and SPEC-0066-TSK-0001 moves from
`queued` to `in-progress` as the execution owner. The existing Spec 0054
compatibility row moves with the parent owner from SPEC-0054-TSK-0010 to
SPEC-0054-TSK-0011; no Spec 0066 row is added. After SPEC-0054-TSK-0011 records
acceptance while remaining `in-progress`, Spec 0066 closes. A later parent
handoff atomically moves SPEC-0054-TSK-0011 to `done` and the compatibility row to
queued SPEC-0054-TSK-0013; only then can SPEC-0054-TSK-0013 activate. The activation does
not modify the Stage 99 Task lifecycle domain, schema, or its current code
projection, and WP-013 removes the temporary row and its consumers.

The registry maps each profile status to the internal `mutable`, `current`, or
`terminal` validation class; documents do not duplicate that class in
frontmatter. Router READMEs have no `artifact_id` or lifecycle. State changes
use the profile's legal transitions and, where replacement is meaningful,
reciprocal `supersedes` and `superseded_by` links. Stable IDs are never reused
after deletion or retirement.

For cumulative CI/ref comparisons, a newly introduced document's required
initial state and subsequent legal transitions may be proved from bounded
actual intermediate Git history within the supplied comparison range. This
preserves draft-first creation; it does not waive initial-state requirements,
alter the comparison base, or admit unproved transitions. Missing or ambiguous
history fails closed. Do not add a fixed SHA list, path exception, or separate
gate for this proof.

The active stable ID families are `REQ-####` and package-scoped requirement member
IDs, `AD-####`, `ADR-####`, `SPEC-####`, `PLAN-####`,
`TSK-<SPEC-NUMBER>-####`, `GDE-####`, `POL-####`, `RUN-####`,
`INC-<YYYY>-####`, `POSTMORTEM-<YYYY>-####`, `RES-####`, `AUD-####`,
and `DATA-####`. Retained Stage 98 records may keep their historical
`MIG-####` or `TMB-####` identifiers without becoming active authored
profiles. Validators enforce path-number,
parent-package, frontmatter-ID, and internal-ID equality. Cross-document
traceability uses complete IDs rather than ambiguous short forms such as
`FR-0001`.

Legacy, deprecated, compatibility-only, conflicting, contradictory, or
duplicate owners are removed after their active consumers reach zero and Git
recovery is proven. This program does not add an Archive record as part of a
current-owner deletion.

### C-SDLC-008 — Stage 90 reference reconciliation

Stage 90 is the semantic owner for workspace Audit, external Research, Data,
and other non-authoritative reference material. These category names are
supported document roles, not a requirement to retain obsolete bodies or keep
empty directories. The terminal current corpus contains only the Stage router,
the research collection router, and the latest externally researched pack
because no reviewed current Audit or Data body survives this cutover:

```text
docs/90.references/
├── README.md
└── research/
    ├── README.md
    └── <preserved-current-pack>/
```

The preserved pack owns dated external evidence, source coverage, and bounded
research synthesis only. It does not own current governance, repository
inventory, validation routing, operational procedure, or a permanent corpus
census. Its existing path remains stable while active Spec 0062 consumes it;
future observation dates belong in source metadata rather than a parallel pack.

The cutover classifies current material by semantic destination in the
executing Task and reviewed diff. Existing Audit snapshots and Data
control-plane copies are removed after live consumers route to canonical
Stage 00-05 owners or direct repository sources. A future Audit or Data
document may be admitted only when it has distinct reference purpose,
provenance, freshness, and a non-authoritative boundary. The existing
`cloud-examples`, `learning`, and `llm-wiki` bodies are removed after their
consumers are cut over: they have no distinct current reference owner,
`learning` is not operational procedure, and `llm-wiki` is a generated
parallel control plane. This point-in-time classification is not persisted as
a Stage 90 disposition ledger or exact corpus gate.

The large reference-information-architecture SHA, finite-state, current-pack,
and census contract is retired with its exclusive fixtures and gates. Current
reference validation checks package identity, semantic ownership, lifecycle,
freshness, consumers, bounded reads, and deterministic generation only where a
maintained generated projection remains. Observation dates stay in frontmatter
or source metadata, not filenames.

### C-SDLC-009 — Stage 98 retention and historical records

Git history is the default exact-byte recovery source. Stage 98 is a
non-current retention and history stage with four distinct roles:

```text
docs/98.archive/
├── README.md
├── completed/<original-stage>/<original-path>
├── migrations/####-<slug>.md
├── superseded/<original-stage>/####-<slug>.md
└── tombstones/<original-stage>/####-<slug>.md
```

The accepted ADR-0032 contract governs the distinction. `completed/` retains a
terminal governed document or whole Stage 03 package after current consumers
reach zero. The retained document keeps its original profile and identity, may
be cited directly for historical trace, and never becomes current requirement,
architecture, decision, or execution authority. Its sealed migration row owns
origin-path and Git provenance.

`migrations/`, `superseded/`, and `tombstones/` hold sealed records. A current
document may not use those records as semantic authority or recovery gates for
active work. Existing sealed records are never edited or compacted in place;
their internal historical links do not create current authority. Superseded
ADRs remain in the Stage 02 decision log.

Validation is role-specific. Retained documents keep their registered profile,
terminal lifecycle, mirrored origin path, link-target identity, and migration
provenance. Sealed records receive repository-containment, safe bounded-read,
strict-decoding, metadata, and declared immutable-byte checks. No role enforces
a full Archive census, current-document or branch SHA parity, remote ancestry,
unrelated current-file parity, or exact record counts. Secret-bearing history
follows incident, rotation, and approved history-removal procedure rather than
ordinary Stage 98 retention.

### C-SDLC-010 — scripts ownership and module boundaries

Accepted ADR-0031 makes this section the current scripts-ownership target.
ADR-0030 remains accepted and records the two-clause scoped amendment for the
top-level test location and responsibility/risk-based module boundaries.

The existing Stage 00 validation-surface contract moves atomically to
`scripts/validation/registry.json` with its schema. This registry owns only
the current routing graph: responsibility, lane selection, executable
entrypoints, and supported consumers. Point-in-time file disposition belongs
to the executing Task and reviewed diff rather than a permanent per-file
ledger. Historical census values, including earlier `50 → 49 → 47`
projections, are review evidence rather than terminal policy.

Production code converges under `docs/`, `setup/`, `qa/`,
`validation/{documents,agents,archive,repository}`, and `lib/`. Validator tests
and fixtures remain under top-level `tests/` and `tests/fixtures/`; production
modules never import or read them. Modules split when responsibility,
duplication, or change risk warrants it; line counts are review signals, not a
policy ceiling.

Compatibility entrypoints are temporary thin wrappers only. Production
validators do not embed a `--self-test` suite; independent tests exercise their
importable contracts. The aggregate gate is a thin orchestrator. All readers
use bounded input, strict UTF-8, explicit subprocess timeouts, and staged-index
semantics for commit claims, and fail on material index/worktree drift.
Filename similarity or line-count reduction alone is not sufficient evidence
for merging validators.

### C-SDLC-011 — design-document ownership

`docs/03.specs/####-<slug>/` has no permanent `design.md` or `tests.md`.
The Spec owns goals, observable behavior, Technical Approach, Acceptance
Contract, interfaces, failure conditions, and change-local design detail. The
Plan owns implementation order, risks, test strategy, validation, rollback,
and recovery. Task records own execution and evidence. A long-lived structural
view is promoted to an Architecture Description, and a long-lived important
choice is promoted to an ADR before a legacy design file is removed.

Root `DESIGN.md` is not part of that SDLC artifact sequence. It is the
canonical human-readable owner for UI and design-system color, typography,
component, and interaction rules. Validators and indexes must not reinterpret
it as a work-unit technical design.

### C-SDLC-012 — control-plane simplicity and evidence boundary

Each permanent rule has one canonical machine owner and one canonical
validator implementation. The aggregate gate composes validators; it does not
reimplement their rules in shell or prose. A CLI wrapper and importable library
remain separate only when they provide genuinely different supported
interfaces.

Fixtures remain finite and behavior-oriented. Tests keep only the examples
needed to prove semantic rule families and generate bounded mutations for
combinatorial cases instead of storing an exhaustive matrix or mandatory case
count. Point-in-time fixture, gate, and SHA dispositions live in the executing
Task and reviewed diff. A completed transition gate, fixture, ledger, or helper
is removed after its permanent semantics move, consumers reach zero, and Git
recovery is proven.

Mutable current-state SHA pins are not policy. Branch HEADs, current documents,
validators, templates, registries, aggregate line numbers, and corpus counts
are validated through schema, semantic projection, path/ID equality,
lifecycle, cross-link, and consumer-zero contracts. A digest remains only when
byte identity is itself the contract: external supply-chain material, a sealed
evidence payload, or a Git-reachable Archive recovery object. Digest retention
must name that purpose and its recovery or refresh boundary.

This simplification is applied incrementally without renumbering work
packages. Every remaining work package removes the duplication it touches;
WP-010 closes the whole-script ownership and consumer graph, and WP-014 proves
the terminal fixed point.

## Core Design

### Technical Approach

The implementation is a sequence of independently reviewable cutovers rather
than one broad rewrite. Requirement Package, prefix-free Architecture, and
route-sensitive Stage 99 changes are atomic. An existing governance candidate
that depends on the superseded registry or expanded Archive model is not
accepted until that foundation exists. A deletion, move, merge, or replacement
is atomic with semantic-owner cutover, consumer-zero, and Git recovery proof.
Stage 98 cleanup remains a later isolated historical operation.

WP-001 and WP-002 remain completed historical evidence, but any terminal
assumption they made that conflicts with ADR-0030 or accepted ADR-0031 is
superseded. The following list describes
integration dependencies, not a global scheduling lock:

1. **WP-004** completed the Stage 99 document-authority, Requirement Package,
   prefix-free Architecture, Stage 03 package, and lifecycle activation. Its
   accepted Task and reachable Git evidence are historical inputs, not work
   to regenerate.
2. **WP-003** originally converged the provider surface after WP-004.
   SPEC-0072 now owns the remaining Stage 00 source migration, `.agents/`
   removal, and shared QA transition; prior Task evidence remains historical.
3. **WP-007** reviews Stage 90 semantic destinations and retires the permanent
   RIA/census control plane under the user-approved research preservation
   boundary.
4. **WP-008** performs the Audit/Data ownership cutover while preserving the
   latest external-research pack.
5. **WP-005** reviews Stage 05 semantic owners and records the point-in-time
   cutover decisions in its Task and diff.
6. **WP-006** performs the Stage 05 owner cutover and strengthens operational
   contracts.
7. **WP-010** and **WP-011** form the delegated Spec 0066 branch. After the
   reviewed activation checkpoint they run while SPEC-0054-TSK-0011 remains the
   sole parent acceptance Task, and remain sequential within Spec 0066. No
   unrelated Spec 0054 Task runs during this delegated acceptance window.
8. **WP-012** removes duplicate progress, closure, snapshot, and generated
    current-state owners.
9. **WP-013** starts only after Spec 0054 accepts the completed Spec 0066
    result, performs the remaining Stage 01/02/03/99 current-corpus cutover,
    removes current-authority dependencies on sealed Stage 98 records, and
    validates completed-document retention before retiring residual taxonomy
    transition assets without concurrent delegated mutation.
10. **WP-009** runs after WP-013 has made sealed-record authority consumers
    zero. It minimizes obsolete sealed records without removing accepted
    completed-document retention or editing sealed records in place.
11. **WP-014** joins the delegated result with the parent integration path,
    proves the all-files ownership, lifecycle, recovery, security, test, and
    branch fixed point, and performs final independent reviews.

Every cutover starts with a focused failing test that proves the old conflict
or missing invariant. Implementation is minimal until that test passes. Broad
gates run only after the focused contract is green and the logical index and
worktree are synchronized.

The rule flow is unidirectional:

```text
approved Spec/ADR
  -> machine contract/schema
  -> canonical validator
  -> bounded fixture and mutation tests
  -> aggregate orchestration
```

Human-readable projections may explain this flow but do not become parallel
rule owners.

## Data Modeling & Storage Strategy

`docs/99.templates/registry.json` remains the machine authority for active
document profiles and normalized top-level lifecycle domains.
`docs/00.agent-governance/roles/registry.json` is the separate machine authority for agent roles,
permissions, handoffs, and skill references. Current-path, Stage 90, and script
dispositions live in the executing Task and reviewed diff; they do not form a
third permanent registry. Sealed Archive evidence remains immutable and is
never used as a mutable current-policy store.

Generated projections must name their canonical inputs, pin the transition
boundary when necessary, provide `--check` behavior, and leave protected output
unchanged in check mode. Validators read the candidate staged index for commit
claims and fail on index/worktree drift where a fixed-point proof is required.

## Interfaces & Data Structures

The canonical interfaces are:

- `docs/99.templates/registry.json` plus the two Stage 99 contract schemas for
  active document contracts;
- `docs/00.agent-governance/roles/registry.json` plus its schema for the provider-neutral agent
  registry;
- Stage 00 policy and role documents as human governance, with point-in-time
  provider/model evidence owned by Stage 90 Data and execution evidence owned
  by Spec Tasks or Git;
- package-local Task/diff evidence for current path and Stage 90 cutovers;
- `scripts/validation/registry.json` and its schema for validation routing,
  lane selection, executable entrypoints, and supported consumers;
- the Stage 98 router, retained completed documents, and sealed records as
  non-current historical material, outside the current authority graph;
- aggregate validation as the terminal repository-static decision surface.

Every remaining work package must report any canonical-owner consolidation,
duplicate aggregate logic removed, transition fixture retired, and mutable SHA
pin eliminated or explicitly retained under C-SDLC-012.

Human-readable READMEs and catalogs are projections or routers. They do not
duplicate machine inventories or independently redefine lifecycle states.

## Edge Cases & Error Handling

- A current document matching two profiles is rejected as ambiguous.
- Separate PRD, SRS, or Interface Requirement documents that repeat one
  Requirement Package fail the duplicate-owner audit.
- A Requirement Package member whose `REQ-####` namespace differs from its
  containing Package, whose family is not `FR`, `NFR`, or `IF`, or whose
  four-digit member number is reused fails identity validation.
- A three-digit active identity, malformed four-digit identity, uppercase
  Incident route, nested unexpected path, or path/frontmatter mismatch fails.
- An `ad-`, `adr-`, `res-`, or `aud-` path prefix fails even when the stable
  frontmatter ID is valid.
- A deleted path with a current consumer or without reachable Git recovery
  fails; adding an Archive dependency does not satisfy either condition.
- A current reference that claims policy authority fails Stage 90
  classification.
- A maintained generated reference whose canonical input or output drifts
  fails closed and does not rewrite output in check mode.
- A provider adapter claiming runtime support without provider-runtime evidence
  fails evidence classification.
- A Gemini/Antigravity current consumer, `.gemini/` surface, root `GEMINI.md`,
  or provider-specific meaning in `.agents/` fails the provider-retirement
  gate.
- An agent adapter cardinality or role count hard-coded outside the agent
  registry fails the machine-owner audit.
- A script retirement with a remaining CI, hook, documentation, fixture, or
  test consumer fails.
- A Guide and Runbook that both claim the same executable procedure fail the
  operations ownership audit.
- A permanent rule implemented in more than one validator or inline aggregate
  block fails the ownership audit.
- A current-state digest without an immutable-byte, supply-chain, or recovery
  purpose fails the evidence-boundary audit.
- A retired transition fixture or helper with no current consumer and no
  terminal semantic responsibility fails the residue audit.
- Any Stage 00/01/02/03/05/90 use of a sealed Stage 98 record as current
  semantic authority fails. A citation to a retained `completed/` document is
  valid only as historical trace and never substitutes for a current owner.

## Failure Modes & Fallback / Human Escalation

Each logical unit preserves a recoverable Git boundary. If a transition gate
fails, no later deletion or archive move occurs. The unit is corrected in its
own branch state or reverted by its logical commit; protected historical
evidence is not edited as a shortcut.

Any newly discovered document family, release-record requirement, provider
runtime claim, destructive history operation, remote mutation, credential use,
or expansion beyond the approved B scope stops for human approval.

## Verification Commands

The detailed implementation plan binds exact, currently resolvable commands to
each logical task and updates them atomically when an executable moves. The
terminal gate set includes independent test discovery, focused validators, the
thin aggregate, security checks, and both staged and all-files fixed points.
Production validators must not execute embedded self-tests. The current command
shape is:

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/validate-document-contract-registry.py --mode strict
python3 scripts/validate-markdown-profiles.py --root . --mode strict
python3 scripts/validate-links-and-owners.py --root . --mode strict
python3 scripts/validate-document-lifecycle.py --root . --mode staged
python3 scripts/validate-affected-surfaces.py --root .
TMPDIR=/tmp bash scripts/validate-repo-quality-gates.sh .
TMPDIR=/tmp pre-commit run
TMPDIR=/tmp pre-commit run --all-files
git diff --check
git diff --cached --check
```

Compatibility wrappers may temporarily forward to these owners during a
consumer migration, but WP-014 evidence uses the terminal entrypoints.

Passing repository-static checks does not prove provider-runtime discovery,
hosted CI, deployment, incident response, or live platform correctness.

## Success Criteria & Verification Plan

### Acceptance Contract

| Criterion | Required evidence |
| --- | --- |
| VAL-SDLC-001 | Exact terminal active topology; Requirement Packages replace repeated PRD/SRS/Interface forms; every retained Requirement Package and Architecture Description is bidirectionally reconciled with current implementation evidence; no implemented durable behavior lacks an appropriate Stage 01/02 owner, no current architecture claim describes absent implementation, and no Stage 02 requirements, Stage 04 owner, local Release family, `.gemini/`, root `GEMINI.md`, or Gemini/Antigravity current governance remains. |
| VAL-SDLC-002 | Every current numeric SDLC route uses four digits; parent folders determine prefix-free document types while typed frontmatter IDs match their paths, and every Requirement member uses a unique package-scoped `REQ-####-(FR|NFR|IF)-####` identity. |
| VAL-SDLC-003 | Incident and Postmortem paths, templates, metadata, links, and negative fixtures use the exact lowercase co-located route. |
| VAL-SDLC-004 | Every work unit has a thin README router, Spec, Plan, and append-only `TSK-<SPEC>-####` records with reciprocal criteria and profile-valid state consistency; no separate design/tests artifact remains. |
| VAL-SDLC-005 | Stage 00 human governance, `.agents` machine registry, and Codex/Claude thin projections have disjoint owners; the three permanent agent gates pass with no hard-coded roster/adaptor cardinality, tracked secret, private-auth mutation, hosted provider credential, unredacted canary result, or over-privileged CI claim. |
| VAL-SDLC-006 | Stage 99 has one registry containing profile definitions and normalized top-level lifecycle domains, one human router, and only the schemas/templates required by active authored profiles; no current-instance program, reference-pack, or standalone-execution roster remains. |
| VAL-SDLC-007 | Guide, Policy, Runbook, Incident, and Postmortem roles are disjoint; reviewed duplicate procedures have one owner. |
| VAL-SDLC-008 | Stage 90 preserves the latest externally researched pack and its routers; Audit/Data bodies and their RIA current-pack/SHA/FSM machine are absent after consumer cutover, with no permanent disposition census or exact corpus gate. Ongoing pack maintenance follows the [Reference Maintenance Runbook](../../05.operations/runbooks/0011-reference-maintenance-runbook.md). |
| VAL-SDLC-009 | Stages 00/01/02/03/05/90 have no current-authority dependency on sealed `migrations/`, `superseded/`, or `tombstones/` records; `completed/` retains terminal documents and whole Stage 03 packages with mirrored paths, terminal profiles, migration provenance, and historical-only citation semantics; Stage 98 has no full-corpus census, current-SHA parity, remote-ancestry, or exact-count gate. |
| VAL-SDLC-010 | After ADR-0031 acceptance, the validation routing and consumer graph has one owner; production modules obey responsibility boundaries, independent tests/fixtures remain under top-level `tests/`, aggregate duplication and embedded self-tests are absent, and no terminal entrypoint, file, case, or line-count invariant remains. |
| VAL-SDLC-011 | Focused, affected, staged, aggregate, secret, all-files, and independent review gates pass at each required boundary; permanent rules have one machine owner and validator, with zero aggregate duplication, unjustified current-state SHA pins, or consumer-free transition fixtures at the terminal fixed point. |
| VAL-SDLC-012 | Each independently testable logical unit is committed separately with no unrelated user changes included. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| N/A — the direct human-approved B-scope consolidation has no separate PRD. | VAL-SDLC-001 | Exact topology plus repository-to-Requirement/Architecture bidirectional parity audit. |
| N/A — VAL-SDLC-002 shares the direct approved requirement source above. | VAL-SDLC-002 | Registry path, identity, date, and malformed-route negatives. |
| N/A — VAL-SDLC-003 shares the direct approved requirement source above. | VAL-SDLC-003 | Incident and operations route, template, and metadata audits. |
| N/A — VAL-SDLC-004 shares the direct approved requirement source above. | VAL-SDLC-004 | Lifecycle and reciprocal cross-artifact contract tests. |
| N/A — VAL-SDLC-005 shares the direct approved requirement source above. | VAL-SDLC-005 | Agent contract, adapter, and evidence-class parity. |
| N/A — VAL-SDLC-006 shares the direct approved requirement source above. | VAL-SDLC-006 | Template, registry, Markdown, link, and lifecycle parity. |
| N/A — VAL-SDLC-007 shares the direct approved requirement source above. | VAL-SDLC-007 | Operations purpose and duplicate-owner audits. |
| N/A — VAL-SDLC-008 shares the direct approved requirement source above. | VAL-SDLC-008 | Complete Stage 90 disposition and freshness audit. |
| N/A — VAL-SDLC-009 shares the direct approved requirement source above. | VAL-SDLC-009 | Inbound-Archive-link zero plus isolated Archive safety and readability checks. |
| N/A — VAL-SDLC-010 shares the direct approved requirement source above. | VAL-SDLC-010 | Script ownership, consumer-zero, module-boundary, and no-fixed-census gates. |
| N/A — VAL-SDLC-011 shares the direct approved requirement source above. | VAL-SDLC-011 | Focused, affected, staged, aggregate, review, canonical-owner, duplicate-gate, fixture-residue, and digest-purpose audits. |
| N/A — VAL-SDLC-012 shares the direct approved requirement source above. | VAL-SDLC-012 | Commit-scope and staged-path audits. |

### External Basis

- [ISO/IEC/IEEE 12207](https://www.iso.org/cms/%20render/live/en/sites/isoorg/contents/data/standard/09/02/90219.html): lifecycle processes may be applied iteratively and recursively; a numbered folder tree is not a mandated waterfall.
- [ISO/IEC/IEEE 15289](https://www.iso.org/cms/%20render/live/en/sites/isoorg/contents/data/standard/07/49/74909.html): lifecycle information-item purpose and content, with organization-appropriate combination or separation.
- [ISO/IEC/IEEE 29148](https://www.iso.org/cms/%20render/live/en/sites/isoorg/contents/data/standard/07/20/72089.html): requirements engineering information items and content.
- [ISO/IEC/IEEE 42010](https://www.iso.org/standard/74393.html): Architecture Description structure and expression, distinct from system requirements.
- [GitHub Spec Kit](https://github.github.com/spec-kit/), [Handling Complex Features](https://github.github.com/spec-kit/concepts/complex-features.html), and [Spec of Specs](https://github.github.com/spec-kit/concepts/spec-of-specs.html): Spec, Plan, Tasks, and implementation workflow with focused per-feature slices and bounded subagent context.
- [OpenSpec](https://github.com/Fission-AI/OpenSpec/blob/main/docs/overview.md): change-unit artifacts, current truth, archive feedback, and the explicit principle that artifacts are enablers rather than accumulated gates.
- [NIST AI RMF](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/) and [ISO/IEC 42001](https://www.iso.org/standard/42001): cross-cutting AI governance, traceability, monitoring, and continual improvement.
- [NIST SP 800-61r3](https://www.nist.gov/publications/incident-response-recommendations-and-considerations-cybersecurity-risk-management-csf), [Google SRE incident management](https://sre.google/resources/practices-and-processes/incident-management-guide/), and [postmortem culture](https://sre.google/workbook/postmortem-culture/): incident facts, roles, response, recovery, learning, and action ownership.
- [Diataxis](https://diataxis.fr/start-here/): separation of learning, how-to, reference, and explanation needs.
- [GitHub Releases](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository): release tags, notes, and assets as an external delivery owner.
- [OpenAI AGENTS.md guidance](https://developers.openai.com/codex/guides/agents-md), [Codex subagents](https://developers.openai.com/codex/subagents), [Anthropic settings](https://code.claude.com/docs/en/settings), and [Anthropic subagents](https://code.claude.com/docs/en/sub-agents): provider-native discovery and permission surfaces remain adapter-specific.

These sources support separation of information-item purposes, decision
history, co-located change execution, operational learning, provider-native
adapters, and bounded automated controls. They do not mandate this repository's
exact directory names, four-digit widths, lifecycle labels, stable-ID grammar,
or work-package order; those are explicit local governance decisions approved
in ADR-0030 and this specification.
