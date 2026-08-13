---
title: 'SDLC Document and AI Agent Governance Consolidation Technical Specification'
type: sdlc/spec
status: active
owner: platform
updated: 2026-08-13
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
- Consolidate the shared AI-agent control plane and provider-specific native
  adapters without claiming unobserved runtime behavior.
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
  not edited to make current validators pass.
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
├── 00.agent-governance/
├── 01.requirements/
├── 02.architecture/
│   ├── descriptions/
│   └── decisions/
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
├── 98.archive/
└── 99.templates/

scripts/
```

`00`, `90`, `98`, and `99` are a control plane, reference library, historical
evidence store, and template contract respectively. They are not sequential
SDLC approval stages.

### C-SDLC-002 — requirements and architecture ownership

`docs/01.requirements/` owns normative product, system/software, and interface
requirements. `docs/02.architecture/descriptions/` owns Architecture
Descriptions: stakeholder concerns, boundaries, viewpoints, models,
allocations, data flow, quality attributes, scenarios, and requirement
disposition. `docs/02.architecture/decisions/` owns decisions, alternatives,
rationale, consequences, and supersession.

`docs/02.architecture/requirements/` is not an active terminal owner. Any
remaining record is migrated to Stage 01, converted to an AD, or dispositioned
as historical evidence.

### C-SDLC-003 — work-unit-local Spec-driven execution

One work unit owns `spec.md`, `plan.md`, and `tasks.md` under the same
`docs/03.specs/####-<slug>/` directory. The Spec owns observable behavior and
acceptance criteria; the Plan owns technical approach, validation, and
recovery; Tasks own ordered execution and evidence. Cross-artifact validators
must reject identifier, state, criterion, and path drift.

`docs/04.execution/` is not restored as an active owner. Its numeric slot
remains unused so retired links are not silently reinterpreted.

### C-SDLC-004 — four-digit and date policy

Active SDLC filenames and directory identities use four digits. Typed prefixes
remain part of the profile route where defined, including `ad-`, `srs-`,
`ifc-`, and `inc-`. Ordinary active filenames do not contain dates. Dates stay
in frontmatter or typed event metadata.

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
negative fixture set. Stage 00 authoring guidance, Stage 99 support prose,
machine registry/schema, hooks, validators, fixtures, README indexes, and
aggregate quality gates must implement the same contract.

Legacy, deprecated, compatibility-only, conflicting, contradictory, or
duplicate owners are removed after their active consumers reach zero and their
Stage 98 disposition is valid.

### C-SDLC-008 — Stage 90 reference reconciliation

Every Stage 90 file receives exactly one disposition:

- `retain-current`: maintained reference with a named freshness owner;
- `regenerate`: generated projection with deterministic source and check mode;
- `merge`: content moves into one canonical current reference;
- `replace`: a current successor owns the material;
- `archive`: historical audit or research evidence moves through Stage 98;
- `delete`: content is redundant and recoverable from a recorded source
  commit, with no live consumer.

Current Stage 90 references use semantic, undated filenames. Observation dates
remain in frontmatter or source-check metadata. Dated audit, snapshot, and
research-pack directories may be retained only as explicitly typed evidence;
they are not active policy owners. Current links may be rewritten to canonical
owners. Historical source claims and audit evidence remain byte-preserved or
recoverable through their recorded source commit.

### C-SDLC-009 — Stage 98 migration evidence

Every moved, merged, replaced, or deleted current artifact has migration or
tombstone evidence with at least:

```yaml
legacy_path:
stable_path:
artifact_id:
action: moved | merged | replaced | deleted
replacement:
source_commit:
reason:
```

The validator enforces global artifact-ID uniqueness, typed four-digit stable
ID patterns, path/frontmatter identity equality, no unapproved date-based
active paths, disposition evidence for deletion or consolidation, and no
active direct links to individual Archive records.

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

## Data Modeling & Storage Strategy

The document registry remains the machine authority for active profiles. A
separate reviewed disposition ledger owns current-path migrations, Stage 90
classification, and script retirement. Frozen archive evidence remains in
Stage 98 and is never used as a mutable current-policy store.

Generated projections must name their canonical inputs, pin the transition
boundary when necessary, provide `--check` behavior, and leave protected output
unchanged in check mode. Validators read the candidate staged index for commit
claims and fail on index/worktree drift where a fixed-point proof is required.

## Interfaces & Data Structures

The canonical interfaces are:

- `document-profiles.json` plus its schema for active document contracts;
- Stage 00 contracts for agent roster, capability, evidence, and validation
  classes;
- a document migration/disposition ledger for current path changes;
- a Stage 90 disposition ledger for reference ownership and freshness;
- a script disposition ledger for executable ownership and retirement;
- Stage 98 migration and tombstone records for historical recovery;
- aggregate validation as the terminal repository-static decision surface.

Human-readable READMEs and catalogs are projections or routers. They do not
duplicate machine inventories or independently redefine lifecycle states.

## Edge Cases & Error Handling

- A current document matching two profiles is rejected as ambiguous.
- A three-digit active identity, malformed four-digit identity, uppercase
  Incident route, nested unexpected path, or path/frontmatter mismatch fails.
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
| VAL-SDLC-001 | Exact terminal active topology; no Stage 02 requirements or Stage 04 active owner; no unapproved Release family. |
| VAL-SDLC-002 | Every current numeric SDLC route uses four digits and every typed path matches its artifact ID. |
| VAL-SDLC-003 | Incident and Postmortem paths, templates, metadata, links, and negative fixtures use the exact lowercase co-located route. |
| VAL-SDLC-004 | Every work unit keeps Spec, Plan, and Tasks co-located with reciprocal criteria and state consistency. |
| VAL-SDLC-005 | Stage 00 has one canonical common contract per concern and thin, evidence-bounded provider adapters. |
| VAL-SDLC-006 | Every active authored profile has one template and one consistent prose/machine/validator contract. |
| VAL-SDLC-007 | Guide, Policy, Runbook, Incident, and Postmortem roles are disjoint; reviewed duplicate procedures have one owner. |
| VAL-SDLC-008 | Every Stage 90 file has exactly one disposition; current references have owners/freshness; historical evidence remains recoverable. |
| VAL-SDLC-009 | Every move, merge, replacement, and deletion has valid Stage 98 migration/tombstone evidence and no active direct Archive-record link. |
| VAL-SDLC-010 | The exact 50-script ledger is complete; consumer-safe transitions prove 49 and then 47 terminal assets. |
| VAL-SDLC-011 | Focused, affected, staged, aggregate, secret, all-files, and independent review gates pass at each required boundary. |
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
| N/A — VAL-SDLC-011 shares the direct approved requirement source above. | VAL-SDLC-011 | Focused, affected, staged, aggregate, and review gates. |
| N/A — VAL-SDLC-012 shares the direct approved requirement source above. | VAL-SDLC-012 | Commit-scope and staged-path audits. |

### External Basis

- [ISO/IEC/IEEE 12207](https://www.iso.org/cms/%20render/live/en/sites/isoorg/contents/data/standard/09/02/90219.html): lifecycle processes may be applied iteratively and recursively; a numbered folder tree is not a mandated waterfall.
- [ISO/IEC/IEEE 15289](https://www.iso.org/cms/%20render/live/en/sites/isoorg/contents/data/standard/07/49/74909.html): lifecycle information-item purpose and content, with organization-appropriate combination or separation.
- [ISO/IEC/IEEE 29148](https://www.iso.org/cms/%20render/live/en/sites/isoorg/contents/data/standard/07/20/72089.html): requirements engineering information items and content.
- [ISO/IEC/IEEE 42010](https://www.iso.org/standard/74393.html): Architecture Description structure and expression, distinct from system requirements.
- [GitHub Spec Kit](https://github.github.com/spec-kit/) and [Spec of Specs](https://github.com/github/spec-kit/blob/main/docs/concepts/spec-of-specs.md): Spec, Plan, Tasks, and implementation workflow with per-feature co-location.
- [OpenSpec](https://github.com/Fission-AI/OpenSpec/blob/main/docs/overview.md): change-unit artifacts, current truth, and archive feedback.
- [NIST AI RMF](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/) and [ISO/IEC 42001](https://www.iso.org/standard/42001): cross-cutting AI governance, traceability, monitoring, and continual improvement.
- [NIST SP 800-61r3](https://www.nist.gov/publications/incident-response-recommendations-and-considerations-cybersecurity-risk-management-csf), [Google SRE incident management](https://sre.google/resources/practices-and-processes/incident-management-guide/), and [postmortem culture](https://sre.google/workbook/postmortem-culture/): incident facts, roles, response, recovery, learning, and action ownership.
- [Diataxis](https://diataxis.fr/start-here/): separation of learning, how-to, reference, and explanation needs.
- [GitHub Releases](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository): release tags, notes, and assets as an external delivery owner.
- [OpenAI AGENTS.md guidance](https://developers.openai.com/codex/guides/agents-md), [Codex subagents](https://developers.openai.com/codex/subagents), [Anthropic settings](https://code.claude.com/docs/en/settings), and [Anthropic subagents](https://code.claude.com/docs/en/sub-agents): provider-native discovery and permission surfaces remain adapter-specific.
