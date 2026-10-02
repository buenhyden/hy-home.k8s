---
title: "Agent Contract and Resource Ownership"
version: "1.0.0"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "platform"
updated: "2026-09-29"
layer: "architecture"
artifact_id: "ADR-0047"
---

# ADR-0047: Agent Contract and Resource Ownership

## Overview

Record a user-approved, scoped amendment to the ownership choices in
[ADR-0036](0036-common-knowledge-and-prompt-surfaces.md): skill packages own
resources dedicated to their procedure, common knowledge may own reviewed
domain facts, and one common evaluation package owns its cases, responses and
exclusive runner. Current execution authority remains in common governance and
native adapters, independent of individual development records.

The request owner approved this decision, SPEC-0102 and the execution Plan on
2026-09-29. Commit `8e811506` records the initial `proposed` creation state;
this reviewed change records `accepted` and version `1.0.0`. Implementation
follows the approved Plan, without external or live authority.
[SPEC-0102](../../98.archive/completed/03.specs/0102-agent-contracts-and-skill-ownership/spec.md)
owns the approved behavior, migration boundaries and acceptance criteria.

The amendment concerns ADR-0036's skill-resource boundary, pointer-only
knowledge restriction and evaluation location. It adds the current-authority
boundary for individual stage records. ADR-0036 remains accepted for its
unchanged common governance, roles, workflows, prompts, provider adapters,
retired progress ledger and evidence boundaries. This is not whole-document
supersession; its body and metadata remain unchanged.

## Context

The current registry, role boundaries, common workflows, provider projections
and validation lanes already separate declaration from execution evidence.
Replacing those working owners would enlarge the migration without resolving
the specific gaps. Existing skill bundles already support scripts, references
and assets. The remaining restrictions concern registered skill-owned gates,
dedicated output templates and nested asset reachability. The constraints that
need revision are narrower:

- A gate's selection authority and its implementation's domain ownership have
  been coupled. This prevents some procedure-specific validators and assets
  from living with the skill that defines and consumes them.
- Pointer-only knowledge can route a reader, but cannot own the reviewed,
  scoped domain facts required for cross-provider work. Historical records and
  provider observations then remain prerequisites for understanding current
  instructions.
- Replacing a link to an individual development record with its plain path
  leaves the same authority dependency. Navigation and active-task evidence
  need different contracts from permanent execution instructions.
- Agent evaluation cases, responses and their exclusive runner form one
  behavior-evaluation concern. Their current separation across root trees
  makes that concern harder to identify without adding independent consumers.

These are ownership changes, not evidence that native discovery, model access,
hook delivery or live operations work. Existing results keep their observed
scope and date.

## Decision

1. **Preserve the common execution structure.** Common governance remains the
   owner of shared policy; the neutral registry owns role, permission, skill
   and projection membership. Role bodies keep responsibility boundaries,
   skills keep reusable procedures, and common workflows keep lifecycle and
   delegation. Providers express their native differences. Implementation and
   independent review remain separate, and no new role is required merely to
   match a new skill or folder.
2. **Separate gate selection from resource ownership.** The shared validation
   registry remains the sole owner of gate admission, argv, lane and profile
   selection. A skill may own its dedicated validator, references and assets
   inside its package, including code reached by an approved global gate. A CI
   call or regression test is an execution consumer, not by itself a second
   domain owner. Genuinely shared helpers and independent contracts stay with
   their shared owners. Every moved resource has one implementation owner;
   narrow safety checks replace blanket bans without relaxing containment,
   bounded input, secret handling or failure semantics.
3. **Keep current authority independent of individual stage records.**
   Permanent files outside `docs/` navigate the documentation tree through
   README entry points. They do not directly link individual stage documents
   or depend on the same documents through plain paths, IDs, footnotes or
   other syntax. Current rules belong to governance or the responsible native
   adapter; reviewed domain facts belong to their current knowledge or
   implementation owner. Individual requirements, decisions and work records
   remain available for authorized investigation and internal documentation
   traceability. An active task is resolved for that execution, rather than
   hard-coded into permanent provider instructions. Necessary machine reads
   of a registry, schema or authoring template require an exact consumer,
   purpose and scope; there is no blanket exception for individual documents.
4. **Admit bounded domain knowledge without a second state ledger.** The
   existing knowledge surface retains owner-navigation indexes and may own
   reviewed facts that have no other current owner. Each fact records `owner`,
   `scope`, `source`, `observed_at`, `valid_for`, `invalidated_by`,
   `review_status` and `sensitivity`. Governance owns approval and permission;
   implementation owns mutable configuration; the active Task owns progress,
   approval evidence and validation results. Knowledge does not copy those
   authorities or maintain a second inventory of their values. Provider recall
   is an untrusted candidate until reviewed against its source. Correction,
   expiry and deletion invalidate derived summaries; receiving work rechecks
   repository identity, source state and authorization before acting. Temporary
   provider summaries remain disposable and cannot grant approval.
5. **Give homogeneous evaluations one package owner.**
   `.agents/evaluations/` owns the agent-behavior case and response corpus and
   its exclusive runner. Shared gate selection and reusable bounded-input
   helpers remain under their existing shared owners. Independent regression
   tests remain under top-level `tests/`. Ordinary infrastructure and tooling
   tests do not move into this package. The migration preserves stable case
   identity and each existing positive and negative verdict, updates every
   runner and data consumer, and removes the old exclusive paths only after
   consumer verification. Synthetic evaluation remains repository-static
   evidence; it cannot certify actual provider behavior.

These clauses describe the approved target. Existing implementation and
validation contracts remain unchanged pending their authorized migration;
recording approval establishes no implemented behavior or runtime enforcement.

## Explicit Non-goals

This decision does not change operating permissions, model entitlement,
provider trust, sandbox controls, credentials, or approval for external writes.
It does not authorize cluster, Vault, cloud, Argo CD, publishing, paid calls or
remote dispatch. It creates no central progress ledger, provider session store,
new document taxonomy or parallel gate registry. It does not reopen completed
packages, rewrite accepted decision history, or make implementation approval
implicit in design approval.

## Consequences

A procedure and its dedicated resources become reviewable together while
common QA still controls which checks execute. The evaluation package becomes
one discoverable owner. Current knowledge can support a handoff without forcing
permanent instructions to depend on historical documents.

The cost is a coordinated consumer migration and more precise ownership
checks. The repository gives up the simplicity of blanket folder prohibitions
and pointer-only knowledge. Fact freshness and deletion now require explicit
validation and review; merely relocating files would leave the requirement
unmet. Existing provider differences and unavailable runtime evidence remain
visible rather than being concealed by a common folder layout.

## Alternatives

- **Keep the current ownership restrictions.** This minimizes the diff and
  retains simple presence checks, but continues to reject approved skill-owned
  gates and dedicated output templates. It also leaves the domain-fact and
  current-authority requirements unmet. Rejected for this change.
- **Replace the harness and collapse domain responsibilities.** A wholesale
  redesign could impose one new layout, but would discard working consumers
  and independently reviewable boundaries. Its larger migration has no
  demonstrated functional benefit. Rejected.
- **Move all scripts, tests and documentation below the agent tree.** This
  creates visual uniformity but obscures shared tooling and infrastructure
  owners and duplicates current authority. Rejected.
- **Retain root evaluation data and its separate exclusive runner.** This
  avoids path migration, but gives up cohesion for a single homogeneous
  concern. The decision instead accepts a bounded move with verdict parity
  and complete consumer cutover as acceptance conditions.

## Traceability

The decision implements the ownership and projection intent of
[REQ-0003-FR-0001, REQ-0003-FR-0002 and REQ-0003-FR-0010](../../01.requirements/0003-workspace-agent-governance-platform.md),
the document and evidence boundaries of
[REQ-0003-FR-0014, REQ-0003-FR-0019, REQ-0003-FR-0021 and REQ-0003-FR-0022](../../01.requirements/0003-workspace-agent-governance-platform.md),
and the single routing owner and migration obligations of
[REQ-0003-FR-0015, REQ-0003-FR-0016, REQ-0003-FR-0024 and REQ-0003-IF-0001](../../01.requirements/0003-workspace-agent-governance-platform.md).
[REQ-0003-FR-0007, REQ-0003-FR-0026 and REQ-0003-FR-0028](../../01.requirements/0003-workspace-agent-governance-platform.md)
retain approval, evidence-depth and negative-test boundaries.

[AD-0006](../descriptions/0006-workspace-agent-governance-platform.md) describes
the current platform. Implementing the approved amendment requires updating
that view and the current ownership contracts together. SPEC-0102 supplies
change-specific behavior; its later approved Plan and Tasks will own execution
order and evidence. The pending persisted acceptance transition and approved
decision claim no completed migration or implemented acceptance criterion.

### Lifecycle Traceability

| Decision lineage | Replacement relation | Affected Spec |
| --- | --- | --- |
| [ADR-0036](0036-common-knowledge-and-prompt-surfaces.md) | User-approved scoped amendment for skill resources, knowledge facts and evaluation ownership, adding current-authority boundaries; ADR-0036 remains accepted for unchanged clauses, with no whole-document supersession | [SPEC-0102](../../98.archive/completed/03.specs/0102-agent-contracts-and-skill-ownership/spec.md) |
