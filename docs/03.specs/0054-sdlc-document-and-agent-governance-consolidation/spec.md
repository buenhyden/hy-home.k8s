---
title: 'SDLC Document and AI Agent Governance Consolidation Technical Specification'
type: sdlc/spec
status: active
owner: platform
updated: 2026-08-14
artifact_id: "SPEC-0054"
---

# SDLC Document and AI Agent Governance Consolidation Technical Specification (Spec)

## Overview

This specification defines the approved B-scope consolidation of the
repository's SDLC documents, Spec-driven development workflow, AI-agent
governance, templates, validators, scripts, operations material, Stage 90
references, and Stage 98 disposition evidence.

The target is a small set of canonical document owners with deterministic
four-digit identities, work-unit-local Spec/Plan/Task artifacts, one shared
agent-governance control plane with provider-native adapters, and validators
that implement the same rules as the prose and templates. The design is based
on official ISO, NIST, GitHub Spec Kit, OpenSpec, Diataxis, Google SRE, GitHub
Releases, OpenAI, Anthropic, and repository evidence reviewed on 2026-08-13.

This specification succeeds, reconciles, or retires conflicting current
instructions. It does not silently rewrite completed evidence. Current rules
that conflict with this specification are migrated, tombstoned, or archived
with an explicit disposition before their active owners are removed.

Direct human approval on 2026-08-13 authorizes B-scope consolidation including
Stage 90. This standalone program inherits the incomplete WORK-109 candidate
from [Spec 0052](../0052-document-taxonomy-consolidation/spec.md), but accepts
only the portions that satisfy this specification after staged-index review.
The direct-approval lineage follows
[ADR-0022](../../02.architecture/decisions/0022-direct-approval-standalone-execution-lineage.md).
The four-digit current-path and Incident identity decision is
[ADR-0025](../../02.architecture/decisions/0025-four-digit-document-path-identity.md),
which transfers the active WORK-109 implementation from Spec 0052 to this
specification's WORK-054-002 package.

Direct human approval on 2026-08-13 authorizes this standalone execution relation.
No separate PRD or Architecture Description is required or part of this standalone lifecycle.
ADR-0022 owns its approval lineage and ADR-0025 owns the topology decision.

Direct human approval on 2026-08-14 refines that topology into package-oriented
requirements, prefix-free architecture paths, a three-family Stage 90 library,
a minimal Git-backed Stage 98 index, and a single Stage 99 registry. This
revision supersedes the earlier PRD/SRS/Interface Requirement form split,
`ad-`/`adr-` route prefixes, support-prose control plane, and snapshot-count or
line-digest Archive design. It retains the approved four-digit identity,
Incident route, work-unit co-location, immutable source recovery, and logical
commit boundaries.

The reciprocal execution artifacts are [Plan 0054](plan.md) and
[Tasks 0054](tasks.md).

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
  snapshots, and audits through a complete disposition ledger.
- Record moved, merged, replaced, or deleted material in Stage 98 migration or
  tombstone evidence.
- Commit each independently testable logical unit separately.

### Protected boundaries

- Git history is not rewritten.
- Existing Stage 98 archive envelopes, source blobs, and immutable records are
  not edited to make current validators pass. They may be removed only by the
  later approved Archive-compaction package after consumer-zero and Git
  recovery are independently proven.
- Stage 90 audit and source-provenance evidence is not cosmetically rewritten.
  It is retained in place or moved through reviewed Stage 98 evidence.
- External publication, deployment, push, merge, release creation, live
  provider execution, and credential-bearing actions are outside this scope.
- `docs/05.operations/releases/` is not created without an approved owner,
  lifecycle, template, consumer, and independent evidence need.

## Contracts

### C-SDLC-001 — canonical document topology

The terminal active topology is:

```text
docs/
├── 00.agent-governance/*
├── 01.requirements/
│   ├── README.md
│   └── ####-<slug>/README.md
├── 02.architecture/
│   ├── README.md
│   ├── descriptions/####-<slug>.md
│   └── decisions/####-<slug>.md
├── 03.specs/
│   └── ####-<slug>/
│       ├── spec.md
│       ├── plan.md
│       └── tasks.md
├── 05.operations/
│   ├── guides/
│   ├── incidents/<year>/inc-####-<slug>/
│   ├── policies/
│   └── runbooks/
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
        ├── archive/
        └── common/

scripts/
```

`00`, `90`, `98`, and `99` are a control plane, reference library, historical
evidence store, and template contract respectively. They are not sequential
SDLC approval stages.

### C-SDLC-002 — requirements and architecture ownership

`docs/01.requirements/####-<slug>/README.md` is one Requirement Package with
stable `REQ-####` identity. It combines the problem and goal, users and
stakeholders, functional and non-functional requirements, constraints,
external interface requirements, acceptance criteria, and links to related
Architecture and Spec artifacts. Stage 01 owns long-lived,
solution-independent requirements; it does not repeat one requirement across
separate PRD, SRS, and Interface Requirement documents.

`docs/02.architecture/descriptions/####-<slug>.md` owns current system
structure, boundaries, components, data flow, and deployment views under a
stable `AD-####` frontmatter identity.
`docs/02.architecture/decisions/####-<slug>.md` owns important choice context,
alternatives, decision, consequences, and supersession under stable
`ADR-####` identity. The parent directory determines the route type, so
`ad-` and `adr-` filename prefixes are not used. A superseded ADR stays in the
decision log and links reciprocally to its successor; it is not deleted or
moved to Archive.

`docs/02.architecture/requirements/` is not an active terminal owner. Any
remaining record is merged into a Requirement Package, converted to an
Architecture Description, or dispositioned as historical evidence.

### C-SDLC-003 — work-unit-local Spec-driven execution

One work unit owns `spec.md`, `plan.md`, and `tasks.md` under the same
`docs/03.specs/####-<slug>/` directory. The Spec owns observable behavior and
acceptance criteria; the Plan owns technical approach, validation, and
recovery; Tasks own ordered execution and evidence. Cross-artifact validators
must reject identifier, state, criterion, and path drift.

Executable interface contracts such as OpenAPI, GraphQL, and Protobuf belong
to the Spec Package that implements and validates them. Stage 01 records the
solution-independent external interface requirement and links to that
executable contract without duplicating it.

`docs/04.execution/` is not restored as an active owner. Its numeric slot
remains unused so retired links are not silently reinterpreted.

### C-SDLC-004 — four-digit and date policy

Active SDLC filenames and directory identities use four digits. Parent
directories determine Requirement Package, Architecture Description, ADR,
Research, Audit, and Data types; their paths do not repeat type prefixes.
Stable frontmatter IDs retain their typed forms, including `REQ-`, `AD-`,
`ADR-`, `RES-`, and `AUD-`. The Incident route retains its required `inc-`
prefix. Ordinary active filenames do not contain dates. Dates stay in
frontmatter or typed event metadata.

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
tags/GitHub Releases unless a future approved local release-record contract is
introduced.

### C-SDLC-006 — integrated AI-agent governance

`docs/00.agent-governance/` is the shared control plane. Common policy has one
owner under `rules/`; domain constraints live under `scopes/`; machine-readable
roster, evidence, routing, and lifecycle shapes live under `contracts/`;
provider capability deltas live under `providers/`; shared implementations
live under `hooks/`; durable repository memory lives under `memory/`.

Repository root and provider-native files are thin gateways or adapters. They
carry only the native metadata and instructions required by that provider.
Repository-static presence, provider discovery, authenticated execution,
hosted CI, and live evidence remain separate evidence classes.

### C-SDLC-007 — template and validator single contract

Every authored profile has exactly one canonical template, route, deterministic
identity rule, frontmatter contract, lifecycle, relationship contract, and
negative fixture set. `docs/99.templates/registry.json` is the only machine
authority for path, profile, required sections, lifecycle, and ID rules.
`contracts/frontmatter.schema.json` and
`contracts/document-profile.schema.json` validate frontmatter and the registry
itself. `templates/` contains directly copyable forms grouped under
`governance/`, `requirements/`, `architecture/`, `specs/`, `operations/`,
`references/`, `archive/`, and `common/`.

Stage 99 `README.md` is the single human router. Former `support/*.md` rules
are merged into that README or the registry and then removed.
`templates/changes/` becomes `templates/specs/`. The removed
`design.template.md`, `tests.template.md`, and separate PRD/SRS/Interface
Requirement templates converge into the Spec/Plan/Tasks and Requirement
Package templates. Templates reference a registry profile ID rather than
hardcoding their destination paths or restating validator behavior.

Legacy, deprecated, compatibility-only, conflicting, contradictory, or
duplicate owners are removed after their active consumers reach zero and their
Stage 98 disposition is valid.

### C-SDLC-008 — Stage 90 reference reconciliation

The terminal Stage 90 topology contains only:

```text
docs/90.references/
├── README.md
├── research/####-<slug>/
├── audits/####-<slug>/
└── data/####-<slug>/
```

Each package has a `README.md` owner and only the bounded supporting source or
data files that it indexes. Research owns external evidence and investigation;
Audit owns point-in-time gap or conformance assessment; Data owns repository
inventory and structured reference data. `RES-####` and `AUD-####` remain
frontmatter identities, but `res-` and `aud-` are not repeated in paths.

Every existing Stage 90 file receives exactly one disposition:

- `retain-current`: maintained reference with a named freshness owner;
- `regenerate`: generated projection with deterministic source and check mode;
- `merge`: content moves into one canonical current reference;
- `replace`: a current successor owns the material;
- `archive`: historical audit or research evidence moves through Stage 98;
- `delete`: content is redundant and recoverable from a recorded source
  commit, with no live consumer.

Current `learning/` content becomes a Stage 05 Guide when it teaches repository
operation, or Research when it records external evidence. Deprecated redirect
documents are removed after consumer migration. A Stage 90 link to a retired
path is not preserved as if it were current; the historical claim is converted
to a Git source commit or Stage 98 evidence when needed. Stage 90 never
overrides rules owned by Stage 00, 01, 02, 03, or 05.

Observation dates remain in frontmatter or source-check metadata. Historical
source claims and audit evidence remain recoverable through their recorded Git
source or an approved Archive record; byte-for-byte copies are not created by
default.

### C-SDLC-009 — Stage 98 migration evidence

Git history is the default full-content archive. Stage 98 is a minimal lookup
and recovery index:

```text
docs/98.archive/
├── README.md
├── migrations/####-<slug>.md
└── tombstones/<original-stage>/####-<slug>.md
```

A Migration records a large path or authority cutover. A Tombstone records a
deleted stable path, replacement, reason, and recovery commit. Every moved,
merged, replaced, or deleted current artifact has only the minimum applicable
evidence, including:

```yaml
legacy_path:
stable_path:
artifact_id:
action: moved | merged | replaced | deleted
replacement:
recovery_commit:
reason:
```

The validator enforces global artifact-ID uniqueness, typed four-digit stable
ID patterns, path/frontmatter identity equality, no unapproved date-based
active paths, disposition evidence for deletion or consolidation, and no
active direct links to individual Archive records.

Completed Spec/Plan/Task bodies are not copied into Archive without a specific
audit or legal retention requirement. Active documents link to the Archive
README or an applicable Migration, not to individual Tombstones. Superseded
ADRs remain in Stage 02. Line-number SHA ledgers, full Archive snapshot counts,
and other restatable Git inventories are removed. The existing Archive corpus
is reviewed path by path and reduced to minimal Migration or Tombstone evidence
only when Git recovery and consumer-zero are proven; otherwise the record is
retained with an explicit reason.

### C-SDLC-010 — scripts disposition and terminal inventory

All 50 current `scripts/` assets receive a reviewed machine-readable
disposition containing owner, purpose, consumer, arguments, diagnostics,
fixtures, evidence, recovery, and retirement gate.

The first consolidation migrates consumers from the compatibility-only
`validate-harness.sh` wrapper and removes it, yielding 49 tracked assets. After
terminal taxonomy consumers are transferred to permanent contracts, the
one-time `document-taxonomy-migration.json` and
`migrate-document-work-units.py` are removed, yielding 47 tracked assets.
Filename similarity alone is not sufficient evidence for merging validators.

### C-SDLC-011 — design-document ownership

`docs/03.specs/####-<slug>/` does not require a separate `design.md` by
default. The Spec owns observable behavior, acceptance criteria, and
change-local design detail; the Plan owns the implementation approach,
validation, and recovery; Tasks own ordered execution and evidence. A
long-lived structural view is promoted to an Architecture Description, and a
long-lived important choice is promoted to an ADR before the work-unit-local
`design.md` is removed.

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

Fixtures remain finite: one representative positive per profile or contract
and one independent negative per semantic rule family. Tests generate bounded
mutations for combinatorial cases instead of storing an exhaustive matrix in
large static fixture files. A completed transition gate, fixture, ledger, or
helper is removed after its permanent invariants, current consumers, and Stage
98 recovery evidence have moved to their terminal owners.

Mutable current-state SHA pins are not policy. Branch HEADs, current validator
blobs, and ordinary current document blobs are validated through schema,
semantic projection, path/ID equality, lifecycle, cross-link, and
consumer-zero contracts. A digest remains only when byte identity is itself the
contract: immutable Stage 98 recovery sources, external supply-chain material,
or a sealed evidence payload. Digest retention must name that purpose and its
recovery or refresh boundary.

This simplification is applied incrementally without renumbering work
packages. Every remaining work package removes the duplication it touches;
WP-010 closes the whole-script ownership and consumer graph, and WP-014 proves
the terminal fixed point.

## Core Design

The implementation is a sequence of independently reviewable cutovers rather
than one broad rewrite. Route-sensitive Stage 00 and Stage 99 changes are
atomic with the four-digit topology cutover. A deletion, move, merge, or
replacement is atomic with its Stage 98 migration or tombstone evidence; a
later global archive package verifies parity but does not retroactively repair
an evidence gap.

The closed execution order is: approved design; topology and route-sensitive
contracts; integrated agent governance; remaining templates; Stage 05
responsibility ledger; Stage 05 cutover; Stage 90 disposition ledger; Stage 90
cutover; global Stage 98 parity; exact fifty-script ledger; wrapper retirement
to forty-nine; append-only progress and generated-current cleanup; transition
asset retirement to forty-seven with terminal route state; and final
fixed-point review and branch completion.

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
profiles. A
separate reviewed disposition ledger owns current-path migrations, Stage 90
classification, and script retirement. Frozen archive evidence remains in
Stage 98 and is never used as a mutable current-policy store.

Generated projections must name their canonical inputs, pin the transition
boundary when necessary, provide `--check` behavior, and leave protected output
unchanged in check mode. Validators read the candidate staged index for commit
claims and fail on index/worktree drift where a fixed-point proof is required.

## Interfaces & Data Structures

The canonical interfaces are:

- `docs/99.templates/registry.json` plus the two Stage 99 contract schemas for
  active document contracts;
- Stage 00 contracts for agent roster, capability, evidence, and validation
  classes;
- a document migration/disposition ledger for current path changes;
- a Stage 90 disposition ledger for reference ownership and freshness;
- a script disposition ledger for executable ownership and retirement;
- Stage 98 migration and tombstone records for historical recovery;
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
- A three-digit active identity, malformed four-digit identity, uppercase
  Incident route, nested unexpected path, or path/frontmatter mismatch fails.
- An `ad-`, `adr-`, `res-`, or `aud-` path prefix fails even when the stable
  frontmatter ID is valid.
- A deleted path without migration/tombstone proof fails.
- A current reference that claims policy authority fails Stage 90
  classification.
- A generated reference whose canonical input or output pin drifts fails
  closed and does not rewrite output in check mode.
- A provider adapter claiming runtime support without provider-runtime evidence
  fails evidence classification.
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
- An active document linking directly to an individual Archive record fails;
  collection indexes or migration ledgers are used instead.

## Failure Modes & Fallback / Human Escalation

Each logical unit preserves a recoverable Git boundary. If a transition gate
fails, no later deletion or archive move occurs. The unit is corrected in its
own branch state or reverted by its logical commit; protected historical
evidence is not edited as a shortcut.

Any newly discovered document family, release-record requirement, provider
runtime claim, destructive history operation, remote mutation, credential use,
or expansion beyond the approved B scope stops for human approval.

## Verification Commands

The detailed implementation plan will bind exact commands to each logical
task. The terminal gate set must include:

```bash
python3 scripts/validate-document-contract-registry.py --self-test
python3 scripts/validate-document-contract-registry.py --mode strict --route-state terminal
python3 scripts/validate-markdown-profiles.py --root . --self-test
python3 scripts/validate-markdown-profiles.py --root . --mode strict
python3 scripts/validate-links-and-owners.py --root . --self-test
python3 scripts/validate-links-and-owners.py --root . --mode strict
python3 scripts/validate-document-lifecycle.py --root . --self-test
python3 scripts/validate-document-lifecycle.py --root . --mode staged
TMPDIR=/tmp bash scripts/validate-repo-quality-gates.sh .
TMPDIR=/tmp pre-commit run
TMPDIR=/tmp pre-commit run --all-files
git diff --check
git diff --cached --check
```

Passing repository-static checks does not prove provider-runtime discovery,
hosted CI, deployment, incident response, or live platform correctness.

## Success Criteria & Verification Plan

| Criterion | Required evidence |
| --- | --- |
| VAL-SDLC-001 | Exact terminal active topology; Requirement Packages replace repeated PRD/SRS/Interface forms; no Stage 02 requirements, Stage 04 owner, or unapproved Release family. |
| VAL-SDLC-002 | Every current numeric SDLC route uses four digits; parent folders determine prefix-free document types while typed frontmatter IDs match their paths. |
| VAL-SDLC-003 | Incident and Postmortem paths, templates, metadata, links, and negative fixtures use the exact lowercase co-located route. |
| VAL-SDLC-004 | Every work unit keeps Spec, Plan, and Tasks co-located with reciprocal criteria and state consistency. |
| VAL-SDLC-005 | Stage 00 has one canonical common contract per concern and thin, evidence-bounded provider adapters. |
| VAL-SDLC-006 | Stage 99 has one registry, two contract schemas, one human README, and one directly copyable template per active authored profile. |
| VAL-SDLC-007 | Guide, Policy, Runbook, Incident, and Postmortem roles are disjoint; reviewed duplicate procedures have one owner. |
| VAL-SDLC-008 | Every Stage 90 file resolves to Research, Audit, Data, Stage 05 Guide, Git history, Stage 98 evidence, or deletion exactly once; reference material cannot own active policy. |
| VAL-SDLC-009 | Stage 98 contains only the minimal README, Migration, and Tombstone topology needed for mapping and Git recovery, with no active direct Tombstone link or redundant snapshot/count ledger. |
| VAL-SDLC-010 | The exact 50-script ledger is complete; consumer-safe transitions prove 49 and then 47 terminal assets. |
| VAL-SDLC-011 | Focused, affected, staged, aggregate, secret, all-files, and independent review gates pass at each required boundary; permanent rules have one machine owner and validator, with zero aggregate duplication, unjustified current-state SHA pins, or consumer-free transition fixtures at the terminal fixed point. |
| VAL-SDLC-012 | Each independently testable logical unit is committed separately with no unrelated user changes included. |

## Traceability

### Lifecycle Traceability

| PRD requirement | Spec criterion | Verification method |
| --- | --- | --- |
| N/A — the direct human-approved B-scope consolidation has no separate PRD. | VAL-SDLC-001 | Exact topology and scope audit. |
| N/A — VAL-SDLC-002 shares the direct approved requirement source above. | VAL-SDLC-002 | Registry path, identity, date, and malformed-route negatives. |
| N/A — VAL-SDLC-003 shares the direct approved requirement source above. | VAL-SDLC-003 | Incident and operations route, template, and metadata audits. |
| N/A — VAL-SDLC-004 shares the direct approved requirement source above. | VAL-SDLC-004 | Lifecycle and reciprocal cross-artifact contract tests. |
| N/A — VAL-SDLC-005 shares the direct approved requirement source above. | VAL-SDLC-005 | Agent contract, adapter, and evidence-class parity. |
| N/A — VAL-SDLC-006 shares the direct approved requirement source above. | VAL-SDLC-006 | Template, registry, Markdown, link, and lifecycle parity. |
| N/A — VAL-SDLC-007 shares the direct approved requirement source above. | VAL-SDLC-007 | Operations purpose and duplicate-owner audits. |
| N/A — VAL-SDLC-008 shares the direct approved requirement source above. | VAL-SDLC-008 | Complete Stage 90 disposition and freshness audit. |
| N/A — VAL-SDLC-009 shares the direct approved requirement source above. | VAL-SDLC-009 | Migration, tombstone, recovery, and direct-Archive-link gates. |
| N/A — VAL-SDLC-010 shares the direct approved requirement source above. | VAL-SDLC-010 | Script disposition, consumer-zero, and exact-census gates. |
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
