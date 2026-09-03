---
title: 'Authority-First SDLC and Agent Governance Convergence'
version: "1.0.0"
type: sdlc/architecture-decision
layer: "architecture"
status: accepted
owner: platform
updated: 2026-09-01
artifact_id: "ADR-0030"
supersedes: ["ADR-0013", "ADR-0015", "ADR-0018", "ADR-0019", "ADR-0023", "ADR-0024", "ADR-0025"]
---

# ADR-0030: Authority-First SDLC and Agent Governance Convergence

## Overview

This accepted decision establishes the terminal ownership model for SDLC
documents, Spec-driven execution, operations, references, Archive evidence,
templates, scripts, and AI-agent governance. It selects **authority-first
incremental convergence**: establish one canonical authority for a concern,
migrate its consumers, remove touched duplication in the same work package,
and then delete obsolete owners with bounded recovery evidence.

The decision keeps the approved four-digit identity and lowercase Incident
grammar, work-unit co-location, transition fail-closed behavior, and explicit
Git recovery. It replaces conflicting document-family, Archive-census,
provider-cardinality, script-census, and mutable-SHA designs in its accepted
predecessors. [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md)
is the implementation authority.

## Context

The repository has repeatedly encoded the same policy in prose, registries,
templates, validators, aggregate shell blocks, fixtures, current-document
digests, and historical snapshots. Those controls made earlier migrations
auditable, but many transition contracts became permanent current owners.
This produced conflicting terminal shapes, large mutation matrices, exact
corpus counts, and branch-relative SHA pins that require validator changes for
ordinary current-document edits.

The active corpus also retains separate PRD, SRS, and Interface forms for a
small workspace; prefixed architecture and reference paths; one monolithic
`tasks.md`; optional Stage 03 design/test families; provider-specific agent
policy copies; a four-surface agent harness including Gemini and Antigravity;
and an Archive that mirrors full historical bodies. These surfaces overlap in
purpose and disagree with the final user-approved ownership boundaries.

[ISO/IEC/IEEE 29148](https://www.iso.org/standard/72089.html),
[ISO/IEC/IEEE 42010](https://www.iso.org/standard/74393.html), and
[ISO/IEC/IEEE 15289](https://www.iso.org/standard/74909.html) distinguish
requirements, architecture descriptions, decisions, and lifecycle information
items while allowing organization-appropriate packaging. GitHub Spec Kit
co-locates Spec, Plan, and Tasks; OpenSpec treats change artifacts as enabling
workflow rather than permanent gate accumulation. AWS ADR guidance keeps
accepted and superseded decisions in a linked decision log. Google SRE
separates incident response facts from blameless postmortem learning. Git
history provides recoverable prior content while reachable objects exist.
OpenAI and Anthropic document different native project instruction and
subagent surfaces.

Those sources support the separation of responsibilities below. They do not
mandate the exact local paths, IDs, status labels, or work-package order; those
are repository governance decisions.

## Decision

### Authority-first convergence

For each concern, implementation proceeds in this order:

1. approve the human design and identify its canonical machine owner;
2. add the terminal schema, semantic contract, and a focused failing test;
3. migrate current content and all consumers atomically;
4. remove duplicate prose, gate logic, fixtures, and mutable digest pins
   touched by the work package;
5. prove consumer-zero and Git recovery before deleting the old owner;
6. close the complete ownership graph in WP-010 and the repository fixed point
   in WP-014.

WP-001 and WP-002 remain completed historical evidence, but their conflicting
terminal assumptions do not constrain this decision. WP-004 establishes the
document foundation before blocked WP-003 resumes agent-governance cutover.

### Terminal document topology and ownership

- Stage 00 contains human governance only: `sdlc.md`, `policies/`, `roles/`,
  `providers/{claude,codex}.md`, and skill governance under `skills/`.
- Stage 01 contains one flat `####-<slug>.md` Requirement Package per durable,
  solution-independent requirement set. It replaces separate PRD, SRS, and
  human Interface Requirement documents.
- Stage 02 contains prefix-free `descriptions/####-<slug>.md` and
  `decisions/####-<slug>.md`. Stable frontmatter IDs remain `AD-####` and
  `ADR-####`. The retired `02.architecture/requirements/` route has no active
  owner and is not restored.
- Stage 03 packages contain a thin `README.md`, `spec.md`, `plan.md`, and
  append-only `tasks/tsk-####-<slug>.md` records. There is no permanent
  `design.md`, `tests.md`, `agent-design.md`, `data-model.md`, or monolithic
  `tasks.md` family.
- Stage 05 contains Guide, Policy, Runbook, Incident, and Postmortem families.
  There is no local Release family; deployments use Spec Tasks or Runbooks and
  publication uses Git tags and GitHub Releases.
- Stage 90 contains only Research, Audit, and Data packages, with learning
  material routed to a Stage 05 Guide or Research. References cannot override
  active policy.
- Stage 98 is a minimal Git-backed lookup layer containing only README,
  Migration, and necessary Tombstone records.
- Stage 99 is the sole document-contract machine authority through
  `registry.json` and its two schemas; its templates are copyable projections,
  not parallel rule owners.

The root `DESIGN.md` remains the UI/design-system authority and is not a Stage
03 technical-design artifact.

### Stable identity and lifecycle

Numeric authored document identities use exactly four digits. Type is inferred
from the parent route, while stable frontmatter retains typed IDs. Requirement
members use complete package-scoped IDs:

```text
REQ-0001-FR-0001
REQ-0001-NFR-0001
REQ-0001-IF-0001
```

Task identity is `TSK-<SPEC-NUMBER>-<TASK-SEQUENCE>`, such as
`SPEC-0054-TSK-0001`. IDs are never reused. Cross-document traceability uses full
IDs. Path numbers, parent package numbers, frontmatter IDs, and internal
member IDs must agree.

Lifecycle is profile-specific. Requirement/AD, ADR, Spec/Plan, Task,
governance/operations, Incident/Postmortem, Research/Audit/Data,
Migration/Tombstone, and Template/Profile each use the transition domain in
Spec 0054. The document registry maps statuses to internal mutable/current/
terminal validation classes; documents do not repeat that class. Router
READMEs have no artifact identity or lifecycle. Replacement uses reciprocal
`supersedes` and `superseded_by` relations where the profile permits it.

Dates remain in frontmatter or evidence metadata. The only path partition
exception is `incidents/<year>/inc-####-<slug>/` with fixed `incident.md` and
`postmortem.md` siblings.

### Spec-driven content boundary

The Spec owns goals, observable behavior, Technical Approach, Acceptance
Contract, interfaces, and failure conditions. The Plan owns implementation
order, test strategy, risk, rollback, and recovery. Task records own execution
and evidence. Executable OpenAPI, GraphQL, and Protobuf contracts belong to the
implementing Spec Package; Stage 01 contains only solution-independent
interface requirements.

Long-lived structure moves from a removed Stage 03 design document to an
Architecture Description. A long-lived important choice moves to an ADR.
Tests remain with their responsible production module.

### AI-agent governance boundary

Stage 00 owns human policy and responsibilities. `.agents/registry.json`,
validated by `.agents/contracts/agent-registry.schema.json`, is the sole
machine owner for role IDs, permission classes, handoff edges, and skill
references. `.agents/agents/` and `.agents/skills/` are provider-neutral
executable surfaces. Stage 00 `skills/` owns skill lifecycle policy, not skill
bodies.

`.claude/` and `.codex/` are the only supported provider-native projections.
They contain thin metadata and configuration required by their runtimes and do
not duplicate common policy. `.gemini/`, root `GEMINI.md`, Gemini provider
contracts and validation, Gemini adapters and canaries, and Antigravity/Gemini
meaning under `.agents/` are removed after consumer-zero proof. Unsupported
hook graphs are not kept as compatibility policy.

Permanent static validation has three responsibilities: agent registry/schema,
provider projection/config, and semantic/permission integrity. No validator
hard-codes role or adapter cardinality. Point-in-time model/provider evidence
belongs to Stage 90 Data; execution progress and closure evidence belongs to a
Spec Task or Git history. Repository-static presence never proves runtime
discovery, authentication, hosted execution, or live effectiveness.

Tracked provider configuration is secret-free. Agent tooling does not collect
or mutate user/private authentication configuration, credential paths, tokens,
or raw transcripts. Hosted CI contains no provider credentials and uses least
privilege. Authenticated canaries are explicit local/manual work and persist
only redacted, secret-free results. Checkpoint and handoff state contains only
bounded task and validation summaries. Third-party CI actions retain full
commit identity where that supply-chain identity is the security contract.

### Scripts, fixtures, gates, and byte identity

Scripts converge under responsibility directories `docs/`, `setup/`, `qa/`,
`validation/{documents,agents,archive,repository}`, and `lib/`. Validator tests
and fixtures are co-located under `validation/tests/`; application and
infrastructure tests may remain top-level. Modules normally contain 200–400
lines and require a reviewed exception above 800 lines.

Compatibility entrypoints are temporary thin wrappers. Production validators
do not embed `--self-test`; the aggregate invokes canonical validators without
reimplementing their semantics. Fixtures contain one representative positive
per profile or contract and one independent negative per semantic family,
with bounded generated mutations for combinatorial coverage.

Historical script counts are evidence, not terminal invariants. The terminal
inventory follows the closed owner/consumer graph. All file and subprocess
input is bounded, strict UTF-8 is enforced, timeouts are explicit, and staged
commit claims read the index and reject material worktree drift.

SHA pins remain only for external supply-chain identity, sealed evidence
payloads, or Git-reachable Archive recovery objects. Current HEADs, ordinary
documents, validators, registries, templates, line numbers, and corpus counts
use semantic validation rather than byte pins.

### Archive and migration boundary

Git history is the default full-content archive. A Migration records a bounded
large path or authority mapping. A Tombstone records only a deleted stable path
that needs durable replacement, reason, and recovery lookup. Routine moves and
merges do not create redundant full-body copies or one Tombstone per source
when a Migration and Git recovery are sufficient.

Deletion requires more than a textual commit field. The recovery identity is a
full Git object ID that resolves to a commit reachable from a named durable
current or protected ref; `legacy_path` must resolve to a regular blob at that
commit. Validators use bounded object reads, strict UTF-8 for claimed text, and
an exact digest when sealed-byte identity is declared. Missing, unreachable,
wrong-type, wrong-path, oversized, undecodable, or digest-drifting recovery
evidence fails closed. Secret-bearing history is excluded from ordinary
preservation and follows incident handling, credential rotation, and approved
secret-removal procedure.

Superseded ADRs remain in Stage 02 and link reciprocally to successors. Active
documents link to the Archive README or a relevant Migration, not individual
Tombstones. Protected historical bytes are not rewritten to satisfy current
rules, and transition deletion remains atomic with consumer-zero and recovery
proof.

## Explicit Non-goals

- Rewriting Git history or deleting evidence whose recovery is unproven.
- Claiming ISO, NIST, SRE, OpenAI, or Anthropic conformance from local path
  choices or repository-static checks.
- Adding a local Release document family.
- Retaining Gemini or Antigravity as dormant supported providers.
- Treating exact script, role, adapter, Archive, fixture, or document counts as
  permanent policy.
- Replacing root `DESIGN.md` or changing live infrastructure, credentials,
  provider accounts, hosted settings, or external services.

## Consequences

### Positive

- Each permanent concern has one human owner, one machine owner where needed,
  and one validator implementation.
- Requirement, architecture, change, operations, reference, and historical
  evidence purposes are explicit and smaller.
- Codex and Claude consume the same provider-neutral role system without
  common-policy copies.
- Ordinary current-document edits no longer require mutable SHA or corpus-count
  rebaselines.
- Git history and minimal recovery records replace tracked full-body snapshot
  duplication.

### Costs and trade-offs

- Authority-first convergence temporarily preserves compatibility wrappers and
  reviewed transition aliases until all consumers move.
- Stage 01, Stage 03, agent, operations, reference, Archive, template, and
  script changes require multiple independently green commits rather than one
  mechanical rename.
- Removing Gemini/Antigravity reduces current provider breadth deliberately.
- A strict 800-line exception boundary requires decomposing several existing
  validators before transition helpers can be retired.

### Operational implications

- WP-004 must reconcile AD-0011 and the prior PRD-0008 program-decision
  projection so ADR-0030 is not a second current terminal owner.
- WP-007/WP-008 must explicitly disposition the pre-existing staged RIA change
  from the main checkout instead of discarding or silently importing it.
- Each deletion is recoverable by its own logical commit and applicable
  Migration/Tombstone evidence.
- Push, merge, release publication, and worktree cleanup remain explicit human
  handoff actions.

## Alternatives

### Preserve the current taxonomy and add more transition exceptions

Rejected because it keeps duplicated PRD/SRS/Interface, provider, Archive,
fixture, and validator owners and makes every ordinary change re-authorize old
transitions.

### Perform one repository-wide mechanical rewrite

Rejected because partial states would be unreviewable, recovery evidence would
lag deletions, and the existing staged RIA candidate could be lost or mixed
without a disposition decision.

### Keep four provider surfaces but mark Gemini/Antigravity dormant

Rejected because tracked adapters, contracts, fixtures, and gates remain
current maintenance obligations even when runtime support is absent.

### Preserve full-body Archive records and exact corpus counts

Rejected because Git already stores the prior bodies, count pins are mutable
current state, and the extra copies do not improve recovery once a reachable
commit and bounded mapping are proven.

### Merge Spec, Plan, and Tasks into one file

Rejected because behavior, implementation strategy, and execution evidence
have different lifecycle and review responsibilities even when co-located.

## Traceability

Accepted [ADR-0031](./0031-current-corpus-retention-and-validation-ownership.md)
amends exactly two validation-layout clauses in this decision: independent
validator tests and fixtures remain under top-level `tests/` and
`tests/fixtures/` rather than `validation/tests/`, and module review follows
semantic responsibility and risk rather than a mandatory exception above 800
lines. This is a scoped amendment, not lifecycle supersession; every other
ADR-0030 clause and its `accepted` status remain authoritative.

The current registry does not yet admit the terminal `superseded` lifecycle and
reciprocal frontmatter fields. This design-authority commit records the direct
successor relations here and in the decision index without mutating closed
predecessor evidence. WP-004 activates document-lifecycle representation and
its document predecessors atomically; WP-003 does the same for ADR-0019 after
the Stage 99 foundation is active.

### Lifecycle Traceability

| Decision lineage | Replacement relation | Affected Spec |
| --- | --- | --- |
| [ADR-0013](0013-stage-00-canonical-adapter-model.md) | This decision replaces its provider-specific shared surfaces and custom-hook model while preserving its historical decision body and stable identity. | [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [ADR-0015](./0015-declarative-document-contract-registry.md) | Partially supersedes its fixed metadata baseline and old profile inventory; preserves the declarative document registry as sole document machine authority. | [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [ADR-0018](./0018-full-body-archive-record-and-retention.md) | Supersedes mandatory full-body, one-record-per-source, and no-Tombstone clauses; preserves explicit recovery and non-authoritative history. | [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [ADR-0019](./0019-provider-native-agent-harness-and-loop-model.md) | Supersedes four-provider, Gemini/Antigravity, fixed 12/48, and harness-machine-owner clauses; preserves provider-native deltas, evidence classes, bounded execution, and least privilege. | [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [ADR-0023](./0023-work-unit-document-taxonomy-and-governance-authority.md) | Partially supersedes `tasks.md`, old agent-contract, and ArchiveEnvelope clauses; preserves Stage 03 co-location, retired Stage 04, stable Stage 05, no Release, and consumer-first migration. | [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [ADR-0024](./0024-terminal-artifact-identity-and-archive-layout.md) | Supersedes its terminal form split, prefixed AD path, mandatory child forms, exact Archive/census/SHA design, and fixed script inventory; preserves AD/ADR meaning, stable identity integrity, native interface contracts, consumer-zero, provenance, and recovery intent. | [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [ADR-0025](./0025-four-digit-document-path-identity.md) | Partially supersedes only its old family table; preserves four-digit identity, lowercase Incident package, atomic migration, and immutable historical paths. | [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [ADR-0031](./0031-current-corpus-retention-and-validation-ownership.md) | Scoped amendment only: top-level independent tests/fixtures and responsibility/risk-based module review replace the two validation-layout clauses named above; ADR-0030 remains accepted. | [Spec 0066](../../98.archive/completed/03.specs/0066-validation-tooling-ownership/spec.md) |
