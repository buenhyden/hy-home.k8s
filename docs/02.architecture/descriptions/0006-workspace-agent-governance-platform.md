---
title: "Agent and Document Governance Architecture"
version: "1.8.3"
type: "sdlc/architecture-description"
status: "active"
owner: "platform"
updated: "2026-09-26"
layer: "architecture"
artifact_id: "AD-0006"
---

# Agent and Document Governance Architecture

## Overview

This Architecture describes the current owner boundaries of agent, document, validation, and execution evidence.
[ADR-0036](../decisions/0036-common-knowledge-and-prompt-surfaces.md) owns
the common governance design, [SPEC-0072](../../03.specs/0072-agent-governance-and-quality-gate-consolidation/spec.md) owns
the cutover and its acceptance conditions, and [Spec 0054](../../98.archive/completed/03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) owns
the wider unfinished document convergence.

### Convergence boundaries

This document owns ownership boundaries, flows, evidence classes, and quality attributes. Machine routes, schemas, state enums,
the role roster, validator argv, and task state are referenced at their canonical owners below and not copied.
[AD-0007](./0007-current-local-gitops-platform.md) owns the GitOps desired state and the platform interfaces.
External accounts, credentials, provider capabilities, and the live runtime are not implementation evidence for this document.
No separate governance registry, per-provider policy fork, Release family, or shared progress ledger is created.

### Convergence quality attributes

| Attribute | Boundary | Evidence |
| --- | --- | --- |
| Consistency | One machine/prose owner per responsibility, with thin projections | Registry/schema, profile, owner, and adapter parity |
| Verifiability | Repository-static, provider-runtime, hosted-CI, and remote/live kept apart | Direct observation per class; an unobserved class gets an owner and a retry trigger |
| Reliability | Bounded retry, a no-progress stop, and safe resume | The loop contract and positive/negative recovery fixtures |
| Security | Least privilege and approval boundaries; secrets, auth, and full transcripts excluded | Static guardrails and independent review; execution permission needs separate approval |
| Recoverability | Git recovery of ordinary changes kept apart from sealed evidence integrity | Consumer succession, sealed records' source commit/blob/digest, the Retention Envelope of retained bodies, and legal lifecycle edges |
| Maintainability | The actual consumer graph instead of a fixed census or duplicate wrappers | Targeted/affected/staged/all-files lanes and direct negative fixtures |

### Convergence authority context

### Authority planes

| Plane | Canonical owner | Consumers and limits |
| --- | --- | --- |
| Agent role/skill machine truth | [Common governance role registry](../../../.agents/roles/registry.json) and adjacent schema | Current Claude/Codex projections; native discovery and runtime enforcement are separate evidence |
| Human execution policy | [Common governance](../../../.agents/README.md) | Root/provider gateways, role responsibilities, approval, quality, and document authoring; copying the machine schema is forbidden |
| Document machine contract and forms | [Stage 99 Registry](../../99.templates/registry.json) and [forms](../../99.templates/README.md) | Profile, route, metadata, identity, lifecycle, and template consumers |
| Validation dispatch | [Validation Registry](../../../scripts/validation/registry.json) | Local/CI affected-path, lane, and argv; each validator keeps its own failure meaning |
| Execution | [Stage 03](../../03.specs/README.md) | Package-local Spec/Plan/Tasks; state, order, and validation evidence are not copied into a central roster |
| Operations and reference | [Stage 05](../../05.operations/README.md), [Stage 90](../../90.references/README.md) | Operating procedures kept apart from observed evidence; a Reference does not substitute for approval or current policy |
| Historical recovery | [Stage 98](../../98.archive/README.md) and reachable Git | Sealed records, completed packages, retained superseded bodies; not current execution authority or a reactivation path |

The number of roles and surfaces is derived from the common governance registry. The past local/Antigravity/Gemini proposals are not the current
supported roster. `.agents/roles/` owns the current machine truth of common roles and skills,
and `.agents/governance/` owns the execution policy. The current provider projection files are repository-static configuration,
not evidence of an observed authenticated discovery or run.

### Consumer and validation flow

1. A task sets its scope, role, skill, and approval boundaries in common governance and links to a package-local Plan/Task.
2. The current domain owner and the Registry select the change's profile, affected paths, and required lanes.
3. Each validator checks its independent contract and records its result, fallback, and limits under the matching evidence class.
4. The reviewer confirms consumer succession and negative fixtures and validates a stable staged snapshot.
5. The Task records commands, results, and unfinished owners. No external execution happens without separate approval and observation.

The aggregate is a router that calls the Registry's all-files runner, not a second owner of argv or policy.
The document Registry, Markdown/profile, link/owner, lifecycle, security, CI, and Archive checks have different failure meanings,
so they are not merged or weakened for the sake of orchestration.

### Convergence data architecture

### State, identity and evidence

The common governance registry owns role/skill identity, Stage 99 owns document identity/profile/state, and the
Validation Registry owns lanes and argv. A body change to an ordinary current document is judged by semantic/profile and link
validation, and an ordinary body is not fixed with a permanent SHA pin. The lifecycle validator judges
Registry-classified profiles, states, and allowed edges.

Risk, tool/data trust, oversight, stop, approval, trace, evaluation, and provenance link to
the current Registry and common governance responsibilities. The past `agentSystems`/`evidenceOwnerPolicies`
proposal is not claimed as an implemented parallel contract. A static declaration of high-risk execution or runtime
enforcement is not evidence of successful execution or policy enforcement.

### Terminal disposition and historical lineage

Before a disposition, source → current semantic owner → every current consumer → legal terminal route is proven.
ADR-0038 split the retention of no-longer-current documents into two kinds, ADR-0039 added the retention unit and exact retention, and [ADR-0040](../decisions/0040-archive-reappraisal-and-verifiable-sources.md), which superseded it, keeps that model and adds appraisal of retention units, whole removal of an approved unit (`git-history-only`), and envelope verification against the default branch. The appraisal is owned by the `Retention Assessment` table of the Archive index, not by the original text.
The retention classes `completed/`, `superseded/`, `retired/`, and `resolved/` keep the original Git objects of a spec package, an Incident bundle, or a single document, links included, under their original profile;
the route dispositions `tombstones/` and `migrations/` name only the route and the current owner, without a body. The ADR decision-log exception is retired.
Citability is judged by the registry's ordered citation table, and the catalog's Retention Envelope names the source Git object once
as `<commit>:<original path>`. The envelopes and source commit/blob/digest of the ADR-0032
generation are frozen historical evidence and are not edited. A terminal ADR's citations of its original documents stay
explicit historical links, and current documents do not consume a retained copy as execution authority.

REQ-0005/0006 → REQ-0008 is the original supersession history. REQ-0003 is the transitive
current semantic successor of this convergence and does not rewrite the original decision target.
The Migration seals the unique mapping of this many-to-one succession and does not extend into a practice of requiring a permanent pin for every ordinary document.

### Loop and checkpoint

The [bounded validation runner](../../../scripts/run-validation-lane.py) owns
the timeout, output, and child cleanup limits, and the Task owns the no-progress stop and handoff evidence.
A checkpoint is ignored transient recovery state and replaces neither policy, the Task, nor a credential store.
Compaction and resume keep only finished and unfinished work, validation results, and the next action, and exclude sensitive data and full transcripts.

### Convergence infrastructure and deployment

Tracked provider configuration and projections are secret-free repository configuration. The user's credential store is
neither read nor migrated. Native parsers and canaries are handled in the provider owner's independent evidence lane,
and no provider credential is added to hosted CI.

The implementation validation owners are [document contracts](../../../scripts/document_contracts.py),
[lifecycle](../../../scripts/document_lifecycle.py),
[Archive recovery](../../../scripts/archive_recovery.py),
[Archive validation](../../../scripts/archive_validation.py), and the lanes the Validation Registry points to.
Exact commands and tool versions are read from their execution owners and not copied into this Architecture.

### Unfinished ownership

Spec 0054 closed as `done` through WP-013/TSK-0013 and is kept in
[98.archive/completed](../../98.archive/completed/03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md).
No unfinished common governance item remains in this document. The current owner of platform implementation and validation
is the active Spec that [AD-0007](./0007-current-local-gitops-platform.md) points to;
this document provides the common routing, approval, and QA boundaries.
This document describes the responsibility boundaries of common governance, the Claude/Codex adapters, common QA, and
GitOps operations. [ADR-0036](../decisions/0036-common-knowledge-and-prompt-surfaces.md) owns
the design, and [SPEC-0072](../../03.specs/0072-agent-governance-and-quality-gate-consolidation/spec.md) owns
the cutover and its acceptance conditions. The existence of a file does not prove the installed runtime's discovery or
permission enforcement, nor hosted CI success. Actual validation state is confirmed in the relevant Task.

## Boundaries & Non-goals

- Common governance owns the meaning of common policy, roles, and skills, and role metadata.
- Stage 99 owns document profiles and forms and defines neither role permissions nor execution success.
- The execution registry and scripts own check selection, execution limits, and failure handling.
- The repository does not own provider accounts, authentication, model access, or global installs.
- GitOps desired state, Kubernetes policy, and external service interfaces stay in their existing domains.

## Quality Attributes

| Attribute | Architecture requirement | Evidence |
| --- | --- | --- |
| Consistency | Common meaning and machine field each have one owner | Role/schema/reference checks and profile routing |
| Security | Native permissions do not exceed registered scope; external mutation needs approval | Independent permission/path rejection tests and native evidence when authorized |
| Reliability | Commands have finite time/output limits and descendant cleanup | Bounded-runner timeout, overflow, cancellation, and pipe regressions |
| Recoverability | Work evidence preserves inputs, failures, ownership, and next action | Task/Git trace; isolated archive recovery checks |
| Reproducibility | Local full and CI share logical gates and configuration | Profile parity, single execution, interpreter and dependency checks |
| Legibility | Gateways point to common owners without copied policy bodies | Native syntax parse and canonical-reference tests |

## System Overview & Context

| Component | Canonical owner | Responsibility |
| --- | --- | --- |
| Entry | Root `AGENTS.md` and `CLAUDE.md` | Explicitly select common policy and relevant procedures |
| Policy | `.agents/governance/` | Approval, security, Git, document and quality meaning |
| Role metadata | `.agents/roles/registry.json` and adjacent schema | Stable IDs, permissions, handoffs, skill and adapter references |
| Role bodies and procedures | `.agents/roles/` and `.agents/skills/` | Neutral responsibilities and reusable work steps |
| Provider contract | `.claude/provider.md` and `.codex/provider.md` | Supported native syntax, loading route, and evidence limits |
| Native adapters | `.claude/` and `.codex/` | Native metadata and explicit common references |
| QA execution | `scripts/qa.py`, validation registry and bounded runner | Profile selection, one execution per gate/input, fail-closed results |
| Change evidence | Stage 03 Task and Git | Actual commands, scope, failures, limitations and handoff |

Claude exposes common `SKILL.md` packages through one relative link per skill.
Codex discovers the packages under `.agents/skills/`; both providers require
explicit invocation. Root instructions also require reading the selected role
and its common procedures. No provider generator or compatibility skill copy
is needed. A native hook is registered only for an actual supported event;
routine tool completion does not invoke whole-repository QA. ADR-0036 owns the
current authority location and carries forward the QA and CD boundary its
superseded predecessors ADR-0034 and ADR-0035 decided.

## Data Architecture

Role metadata references canonical role bodies and skill IDs; it does not copy
policy prose. Provider files retain native format and model bindings. Static
metadata validation cannot prove account availability or authenticated execution.

QA profiles contain gate IDs. The execution registry alone owns commands and
selection configuration; the runner owns bounded process handling. Quick checks
working-tree changes, full checks the final working tree, and staged validation
checks the real index in an isolated snapshot. CI checks its immutable checkout.
Snapshot preparation preserves Git history for recovery while keeping the user's
index and working files unchanged.

Historical facts remain in Git or isolated retained records. Active policy,
provider loading, and command selection do not consume a retired proposal as
current authority. Test fixtures are bounded synthetic inputs, never production
configuration or runtime admission evidence.

## Infrastructure & Deployment

GitHub Actions validates repository bytes through the common QA entrypoint.
`ci-summary` retains its externally observed check name and propagates failure,
cancellation, missing results, and unexpected skips. Static QA uses pinned tools
and minimal permissions; it does not need provider credentials or a cluster.

Argo CD reconciles `gitops/` desired state within the existing operating boundary.
`infrastructure/` supplies bootstrap support and `examples/` contains
examples. `policy/` is Kubernetes
Conftest/Rego policy, separate from common agent policy. External Vault,
PostgreSQL, and Valkey remain interface contracts, not services operated by QA.

A local commit does not authorize push, PR creation, workflow dispatch, release,
cluster mutation, or external service changes. Hosted, native provider, and live
verification require their own actual evidence and applicable authorization.

## Traceability

### Lifecycle Traceability

| Upstream requirement | Quality attribute or boundary | ADR / Spec |
| --- | --- | --- |
| [REQ-0003-FR-0001](../../01.requirements/0003-workspace-agent-governance-platform.md) | Agent Registry, common governance prose, and Stage 99 document-contract authority planes | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../98.archive/completed/03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-FR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | Thin provider projections with native syntax isolated from shared policy | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../98.archive/completed/03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-FR-0003](../../01.requirements/0003-workspace-agent-governance-platform.md) | Skill-source provenance and unavailable-capability boundary | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../98.archive/completed/03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-FR-0004](../../01.requirements/0003-workspace-agent-governance-platform.md) | Package-local scope and approval handoff into domain owners | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../98.archive/completed/03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-FR-0005](../../01.requirements/0003-workspace-agent-governance-platform.md) | Task-owned durable evidence and ignored transient checkpoint separation | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../98.archive/completed/03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-FR-0006](../../01.requirements/0003-workspace-agent-governance-platform.md) | Repository form owner separated from external reference formats | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../98.archive/completed/03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-FR-0007](../../01.requirements/0003-workspace-agent-governance-platform.md) | Common governance approval gates around secret, external, and live execution | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../98.archive/completed/03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-FR-0008](../../01.requirements/0003-workspace-agent-governance-platform.md) | Registry-derived provider projection admission | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../98.archive/completed/03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-FR-0009](../../01.requirements/0003-workspace-agent-governance-platform.md) | Static provider metadata versus authenticated runtime evidence | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../98.archive/completed/03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-FR-0010](../../01.requirements/0003-workspace-agent-governance-platform.md) | Agent Registry ownership of permission, stop and handoff semantics | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../98.archive/completed/03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-FR-0011](../../01.requirements/0003-workspace-agent-governance-platform.md) | Loop contract as bounded retry, no-progress and resume owner | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../98.archive/completed/03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-FR-0012](../../01.requirements/0003-workspace-agent-governance-platform.md) | Stage 99 machine contract versus common governance authoring policy | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../98.archive/completed/03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-FR-0013](../../01.requirements/0003-workspace-agent-governance-platform.md) | One form route per document profile with schema/template parity | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../98.archive/completed/03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-FR-0014](../../01.requirements/0003-workspace-agent-governance-platform.md) | Stage-specific purpose boundaries and no parallel Release family | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../98.archive/completed/03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-FR-0015](../../01.requirements/0003-workspace-agent-governance-platform.md) | Consumer transfer before source disposition with Git recovery evidence | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../98.archive/completed/03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-FR-0016](../../01.requirements/0003-workspace-agent-governance-platform.md) | Validation Registry dispatch and independent validator failure meanings | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../98.archive/completed/03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-FR-0017](../../01.requirements/0003-workspace-agent-governance-platform.md) | Independent CI evidence lanes and remote-observation boundary | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../98.archive/completed/03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-FR-0018](../../01.requirements/0003-workspace-agent-governance-platform.md) | Exact-diff review and rollback-ready logical delivery units | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../98.archive/completed/03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-FR-0019](../../01.requirements/0003-workspace-agent-governance-platform.md) | Package-local sequencing with unchanged historical program lineage | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../98.archive/completed/03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-FR-0020](../../01.requirements/0003-workspace-agent-governance-platform.md) | ADR-0040 unit retention, reappraisal, and ordered citation table | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../98.archive/completed/03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-FR-0021](../../01.requirements/0003-workspace-agent-governance-platform.md) | Reference provenance separated from current execution authority | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../98.archive/completed/03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-FR-0022](../../01.requirements/0003-workspace-agent-governance-platform.md) | Ignored checkpoint state versus Task-owned durable execution evidence | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../98.archive/completed/03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-FR-0023](../../01.requirements/0003-workspace-agent-governance-platform.md) | Profile-owned stable identity and source-preserving migration mapping | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../98.archive/completed/03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-FR-0024](../../01.requirements/0003-workspace-agent-governance-platform.md) | Consumer-zero removal of compatibility surfaces after semantic transfer | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../98.archive/completed/03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-FR-0025](../../01.requirements/0003-workspace-agent-governance-platform.md) | Current Agent Registry and common governance risk, trust, and approval owners | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../98.archive/completed/03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-FR-0026](../../01.requirements/0003-workspace-agent-governance-platform.md) | Separate repository-static, provider-runtime, hosted-CI and live evidence | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../98.archive/completed/03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md) | Lifecycle edges separated from ordinary body edits and sealed integrity | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../98.archive/completed/03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-FR-0028](../../01.requirements/0003-workspace-agent-governance-platform.md) | Direct negative fixtures with explicit tool-failure and fallback diagnostics | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../98.archive/completed/03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-NFR-0001](../../01.requirements/0003-workspace-agent-governance-platform.md) | Registry-derived admission rather than a frozen role/provider census | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../98.archive/completed/03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-NFR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | Stable target-path snapshots across focused and aggregate validation lanes | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../98.archive/completed/03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-NFR-0003](../../01.requirements/0003-workspace-agent-governance-platform.md) | Primary-source traceability with repository conventions labeled separately | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../98.archive/completed/03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-NFR-0004](../../01.requirements/0003-workspace-agent-governance-platform.md) | Explicit baseline-failure and environment-limit reporting | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../98.archive/completed/03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-IF-0001](../../01.requirements/0003-workspace-agent-governance-platform.md) | Atomic owner/consumer migration and reciprocal-link validation | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../98.archive/completed/03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-IF-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | External catalog provenance without policy or permission authority | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../98.archive/completed/03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |

### Architecture responsibility transfer

| Original description | Retained current responsibility | Consumer transfer |
| --- | --- | --- |
| AD-0008 | This AD: document machine owner, form parity, purpose-specific README, affected routing, CI/security and review boundaries | REQ-0003 member-ID map; terminal ADRs retain original decision citations |
| AD-0009 | This AD: lifecycle/profile evidence, legal recovery, package-local lineage, Reference/scratch and non-promotable evidence | REQ-0003 member-ID map; original follow-up and supersession chronology unchanged |
| AD-0011 | This AD: authority planes, stable identity, current taxonomy, validator ownership, consumer-zero and lifecycle/body separation | REQ-0003 and Spec 0054; original Spec 0052 history preserved |
| AD-0010, shared assurance boundary | This AD: validation routing, CI/QA, approval and direct negative tests; AD-0007 retains platform-specific design | REQ-0003/0004 explicit member transfer and Specs 0047..0051 |

The replacement record and this responsibility table express semantic succession, not a new claim that historical
ADRs originally served this AD. Superseded ADR bodies keep their reciprocal supersession and are retained under `98.archive/superseded/`.
The existing requirement IDs retain their identity. ADR-0036 and SPEC-0072
own the current governance and QA implementation; predecessor decisions remain
historical evidence rather than parallel operating instructions.

| Upstream requirement | Quality attribute or boundary | ADR / Spec |
| --- | --- | --- |
| [REQ-0003-FR-0001](../../01.requirements/0003-workspace-agent-governance-platform.md) | Common governance durable policy and owner graph | [ADR 0036](../decisions/0036-common-knowledge-and-prompt-surfaces.md) |
| [REQ-0003-FR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | Thin gateways and provider projections | [ADR 0036](../decisions/0036-common-knowledge-and-prompt-surfaces.md) |
| [REQ-0003-FR-0003](../../01.requirements/0003-workspace-agent-governance-platform.md) | Skill provenance and gap evidence | [ADR 0036](../decisions/0036-common-knowledge-and-prompt-surfaces.md) |
| [REQ-0003-FR-0004](../../01.requirements/0003-workspace-agent-governance-platform.md) | Strategy axes and scope owners | [ADR 0036](../decisions/0036-common-knowledge-and-prompt-surfaces.md) |
| [REQ-0003-FR-0005](../../01.requirements/0003-workspace-agent-governance-platform.md) | Execution/checkpoint/handoff evidence | [ADR 0036](../decisions/0036-common-knowledge-and-prompt-surfaces.md) |
| [REQ-0003-FR-0006](../../01.requirements/0003-workspace-agent-governance-platform.md) | Form/profile and routing contract | [ADR 0036](../decisions/0036-common-knowledge-and-prompt-surfaces.md) |
| [REQ-0003-FR-0007](../../01.requirements/0003-workspace-agent-governance-platform.md) | GitOps, secret, privilege, and approval boundary | [ADR 0036](../decisions/0036-common-knowledge-and-prompt-surfaces.md) |
| [REQ-0003-FR-0008](../../01.requirements/0003-workspace-agent-governance-platform.md) | Registry-derived admitted-provider projection | [ADR 0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md) |
| [REQ-0003-FR-0009](../../01.requirements/0003-workspace-agent-governance-platform.md) | Provider schema/model/effort/MCP and canary | [ADR 0036](../decisions/0036-common-knowledge-and-prompt-surfaces.md) |
| [REQ-0003-FR-0010](../../01.requirements/0003-workspace-agent-governance-platform.md) | Machine harness contract/schema | [ADR 0036](../decisions/0036-common-knowledge-and-prompt-surfaces.md) |
| [REQ-0003-FR-0011](../../01.requirements/0003-workspace-agent-governance-platform.md) | Bounded loop/checkpoint/compaction | [ADR 0036](../decisions/0036-common-knowledge-and-prompt-surfaces.md) |
| [REQ-0003-NFR-0001](../../01.requirements/0003-workspace-agent-governance-platform.md) | Registry-derived parity and eval/admission | [ADR 0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md) |
| [REQ-0003-NFR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | CI/QA/all-files evidence | [ADR 0036](../decisions/0036-common-knowledge-and-prompt-surfaces.md) |
| [REQ-0003-IF-0001](../../01.requirements/0003-workspace-agent-governance-platform.md) | Legacy cutover/current-owner integrity | [ADR 0036](../decisions/0036-common-knowledge-and-prompt-surfaces.md) |
| [REQ-0003-IF-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | Evidence-only external role admission | [ADR 0036](../decisions/0036-common-knowledge-and-prompt-surfaces.md) |
| N/A — [Acceptance criterion 01](../../01.requirements/0003-workspace-agent-governance-platform.md) remains package-owned | Owner graph consistency | [ADR 0036](../decisions/0036-common-knowledge-and-prompt-surfaces.md) |
| N/A — [Acceptance criterion 02](../../01.requirements/0003-workspace-agent-governance-platform.md) remains package-owned | Reciprocal lifecycle chain | [ADR 0036](../decisions/0036-common-knowledge-and-prompt-surfaces.md) |
| N/A — [Acceptance criterion 03](../../01.requirements/0003-workspace-agent-governance-platform.md) remains package-owned | Gateway/evidence-class separation | [ADR 0036](../decisions/0036-common-knowledge-and-prompt-surfaces.md) |
| N/A — [Acceptance criterion 04](../../01.requirements/0003-workspace-agent-governance-platform.md) remains package-owned | Repository static gate | [ADR 0036](../decisions/0036-common-knowledge-and-prompt-surfaces.md) |
| N/A — [Acceptance criterion 05](../../01.requirements/0003-workspace-agent-governance-platform.md) remains package-owned | Template form authority | [ADR 0036](../decisions/0036-common-knowledge-and-prompt-surfaces.md) |
| N/A — [Acceptance criterion 06](../../01.requirements/0003-workspace-agent-governance-platform.md) remains package-owned | Registry-derived role/provider parity | [ADR 0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md) |
| N/A — [Acceptance criterion 07](../../01.requirements/0003-workspace-agent-governance-platform.md) remains package-owned | Admitted-provider independent canary classification and readiness evidence | [ADR 0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md) |
| N/A — [Acceptance criterion 08](../../01.requirements/0003-workspace-agent-governance-platform.md) remains package-owned | Contract/schema/provider parity | [ADR 0036](../decisions/0036-common-knowledge-and-prompt-surfaces.md) |
| N/A — [Acceptance criterion 09](../../01.requirements/0003-workspace-agent-governance-platform.md) remains package-owned | Recovery fixture and safe resume | [ADR 0036](../decisions/0036-common-knowledge-and-prompt-surfaces.md) |
| N/A — [Acceptance criterion 10](../../01.requirements/0003-workspace-agent-governance-platform.md) remains package-owned | Eval/model-fitness evidence | [ADR 0036](../decisions/0036-common-knowledge-and-prompt-surfaces.md) |
| N/A — [Acceptance criterion 11](../../01.requirements/0003-workspace-agent-governance-platform.md) remains package-owned | CI and all-files gate | [ADR 0036](../decisions/0036-common-knowledge-and-prompt-surfaces.md) |
| N/A — [Acceptance criterion 12](../../01.requirements/0003-workspace-agent-governance-platform.md) remains package-owned | Zero stale legacy/orphan reference | [ADR 0036](../decisions/0036-common-knowledge-and-prompt-surfaces.md) |

- **Requirement Package**: [REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md)
- **Current decision**: [ADR-0036](../decisions/0036-common-knowledge-and-prompt-surfaces.md)
- **Current implementation**: [SPEC-0072](../../03.specs/0072-agent-governance-and-quality-gate-consolidation/spec.md)
- **Wider SDLC program**: [SPEC-0054](../../98.archive/completed/03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md)
- **Historical decisions**: ADR-0019, [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), ADR-0034, ADR-0035

The prior architecture narrative is recoverable from this same path at commit
`bb73116b7b09c4f257fc81baa12cfa8359495fc0`. Its retired providers, fixed retry
counts, synthetic runtime records, and separate agent CI topology are not
current contracts.
