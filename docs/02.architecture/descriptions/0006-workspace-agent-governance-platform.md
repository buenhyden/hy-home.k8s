---
title: "Agent and Document Governance Architecture"
version: "2.0.0"
type: "sdlc/architecture-description"
status: "active"
owner: "platform"
updated: "2026-10-07"
layer: "architecture"
artifact_id: "AD-0006"
---

# Agent and Document Governance Architecture

## Overview

This Architecture describes the current owner boundaries of agent, document, validation, and execution evidence.
[ADR-0036](../decisions/0036-common-knowledge-and-prompt-surfaces.md) owns
the common governance design, [SPEC-0072](../../98.archive/completed/03.specs/0072-agent-governance-and-quality-gate-consolidation/spec.md) owns
the cutover and its acceptance conditions, and [Spec 0054](../../98.archive/completed/03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) owns
the completed convergence record; its remaining Stage 03 dispositions transferred to SPEC-0083 and SPEC-0084.

The selected local delivery design is recorded in
[ADR-0048](../decisions/0048-local-qa-and-semver-release-ownership.md) and
[SPEC-0107](../../03.specs/0107-local-qa-and-release/spec.md). Their change replaces
recurring hosted QA and per-main-push tagging with local validation and explicit
SemVer releases. This view describes that target ownership; the Spec's Task
records which implementation and validation have actually completed. Earlier
cutover evidence does not establish completion of this change.

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
| Maintainability | The actual consumer graph instead of a fixed census or duplicate wrappers | The v4 source routes targeted/affected/staged selection, purpose-specific gates and direct negative fixtures; acceptance of the aggregate all-files retirement stays with the owning Task |

### Convergence authority context

### Authority planes

| Plane | Canonical owner | Consumers and limits |
| --- | --- | --- |
| Agent role/skill machine truth | [Common governance role registry](../../../.agents/roles/registry.json) and adjacent schema | Current Claude/Codex projections; native discovery and runtime enforcement are separate evidence |
| Human execution policy | [Common governance](../../../.agents/README.md) | Root/provider gateways, role responsibilities, approval, quality, and document authoring; copying the machine schema is forbidden |
| Document machine contract and forms | [Stage 99 Registry](../../99.templates/registry.json) and [forms](../../99.templates/README.md) | Profile, route, metadata, identity, lifecycle, and template consumers |
| Validation dispatch | [Validation Registry](../../../scripts/validation/registry.json) | Local affected-path, lane, and argv; each validator keeps its own failure meaning |
| Execution | [Stage 03](../../03.specs/README.md) | Package-local Spec/Plan/Tasks; state, order, and validation evidence are not copied into a central roster |
| Skill evaluation evidence | [Evaluation router](../../../.agents/evaluations/README.md) | Same-task noSkill/withSkill observations and their scoring; evidence form belongs to Stage 99, Skill membership and runtime contracts remain with their existing owners |
| Operations and reference | [Stage 05](../../05.operations/README.md), [Stage 90](../../90.references/README.md) | Operating procedures kept apart from observed evidence; a Reference does not substitute for approval or current policy |
| Historical recovery | [Stage 98](../../98.archive/README.md) and reachable Git | Sealed records, completed packages, retained superseded bodies; not current execution authority or a reactivation path |

The number of roles and surfaces is derived from the common governance registry. The past local/Antigravity/Gemini proposals are not the current
supported roster. `.agents/roles/` owns the current machine truth of common roles and skills,
and `.agents/governance/` owns the execution policy. The current provider projection files are repository-static configuration,
not evidence of an observed authenticated discovery or run.

### Consumer and validation flow

1. A task sets its scope, role, skill, and approval boundaries in common governance and links to a package-local Plan/Task.
2. The current domain owner and the Registry select the change's profile, affected paths, and required local lanes; tools, budget and execution authority are resolved before implementation.
3. Each validator checks its independent contract and records its result, fallback, and limits under the matching evidence class.
4. The reviewer confirms consumer succession and negative fixtures and validates a stable staged snapshot.
5. The Task records commands, results, and unfinished owners. No external execution happens without separate approval and observation.

The aggregate selects the Registry's applicable local checks rather than owning
another copy of argv or policy. Ordinary document content selects profile,
relationship, link and state checks. Implementation regressions follow changes
to their responsible implementation or declared inputs. A global QA-contract
change or explicit bounded audit selects named affected purpose and unit checks;
the long full/ci sweep and blanket unit discovery are retired from completion.
Distinct document, platform, security and
Archive rules retain their failure meanings when their orchestration is shared.

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
The local QA and release ownership transition belongs to
[SPEC-0107](../../03.specs/0107-local-qa-and-release/spec.md); its Task owns actual
results and remaining work. The current owner of platform implementation and validation
is the active Spec that [AD-0007](./0007-current-local-gitops-platform.md) points to;
this document provides the common routing, approval, and QA boundaries.
This document describes the responsibility boundaries of common governance, the Claude/Codex adapters, common QA, and
GitOps operations. [ADR-0036](../decisions/0036-common-knowledge-and-prompt-surfaces.md) owns
the common governance design, and [SPEC-0072](../../98.archive/completed/03.specs/0072-agent-governance-and-quality-gate-consolidation/spec.md) preserves
the original cutover and its acceptance conditions. ADR-0048 records the local
delivery change. The existence of a file does not prove the installed runtime's discovery or
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
| Reproducibility | A local result names its input bytes, configuration, tool, scope, mode, trust and relevant history | Exact-index isolation, dependency identity and refusal of reuse after a relevant input changes |
| Proportional cost | Each selected leaf runs once for identical inputs; ordinary document edits do not invoke implementation regression discovery | Registry selection and actual invocation evidence in the owning Task |
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
| Release production | `scripts/release.py`, `.cz.toml`, `cliff.toml` and main `CHANGELOG.md` | Local preparation and one SemVer tag/Release producer; publication remains an authorized external operation |
| Change evidence | Stage 03 Task and Git | Actual commands, scope, failures, limitations and handoff |
| Skill comparison evidence | `.agents/evaluations/` | Actual task, paired raw outputs, scoped score and one aggregate results owner; no recurring grader or runtime authority |

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
working-tree changes and staged validation checks the real index in an isolated
snapshot. Named purpose gates and focused units check only their declared
scope. The retired local full/ci sweep is not a completion profile or proof of
hosted execution.
Snapshot preparation preserves Git history for recovery while keeping the user's
index and working files unchanged.

Evidence reuse requires identical declared bytes, configuration, tool identity,
scope, mode, trust and relevant base/history. An index, working tree and merged
tree are not interchangeable merely because their path lists match. A changed
input invalidates its dependent result. Within a run, parsing and Git reads may
be shared without merging independent failure meanings or persisting a second
source of document state.

Recurring Archive validation owns safe paths, retained-body integrity and
recoverable source objects. A past cutover's fixed census and completion proof
remain historical evidence. Retirement transfers any unique ongoing protection
before removing its caller, registration and dedicated helper, fixture or test.
Frozen bodies and original observed results are preserved.

Historical facts remain in Git or isolated retained records. Active policy,
provider loading, and command selection do not consume a retired proposal as
current authority. Test fixtures are bounded synthetic inputs, never production
configuration or runtime admission evidence.

### Skill comparison records

The [evaluation router](../../../.agents/evaluations/README.md) leads to
representative harness evidence. Each evaluation's `task.md` owns the workload,
comparison conditions and criteria; `baseline.md` and `with-skill.md` retain
the actual noSkill and withSkill outputs. `score.md` owns the evidence
granularity, trial count, result signals, grader and criterion IDs, reasons for
partial scores and human-calibration state. The root `results.md` owns the
representative scores, status, reviewer and date without a second README score
table. Actual evaluation cycles alone update those records; an aggregate entry
requires the corresponding task, complete output pair and score.

Stage 99 owns the bounded task, score, results and opaque-output profiles and
canonical forms. The local templates router links to those forms rather than
copying them. Existing document checks cover authored evidence structure;
they neither rescore an evaluation nor certify its accuracy. Raw outputs retain
their observed bytes instead of acquiring frontmatter, formatter edits or
executable instructions through document normalization. Secret and safe-path
controls still apply, and new cycles use distinct evidence so that earlier
observations are not overwritten.

The common Skill index owns active membership, while common governance owns
evaluation authority and stop conditions. Imported Skill descriptions or
synthetic responses establish neither local Skill admission nor native
selection, actual command execution or permission enforcement. Missing paired
outputs stay unobserved; retired historical grading criteria are not silently
reapplied to a changed contract. Retiring a fixed recurring grader leaves this
evidence capacity available without adding a new QA gate.

## Infrastructure & Deployment

### Local delivery stages

| Stage | Execution owner and boundary |
| --- | --- |
| Editing | Focused behavior regressions and affected content checks selected from the current local registry |
| Logical commit | Exact-index staged validation and the actual Commitizen message check; an active hook's identical leaf is not repeated manually |
| Feature push | Git transport preserves commit evidence and adds no repeated QA requirement |
| PR and main integration | Review local evidence and check inputs changed by integration; refresh only invalidated results |
| After merge | Verify delivered identity and state; a merge resolution that changes validated inputs selects the affected checks |
| Global QA-contract change or bounded audit | Resolve tools, time, output and native execution approval for affected purpose gates and named behavior, Archive and security units; do not run a blanket sweep |
| Release | Validate release inputs and publish through one producer; tag or Release publication does not repeat QA |

GitHub Actions retains `ci-summary`, which validates branch metadata, and a
separate PR-only selected style job. `ci-summary` reports the branch-policy
verdict itself. Missing metadata, an invalid
PR base or source branch, or an unexpected event/ref fails that job;
PR branch policy is not applicable on main. Historical hosted full QA
`NOT_RUN` records remain evidence, not a current check. A successful metadata
or style job does not certify local purpose QA. This design gives up an
independent hosted full/unit QA execution and its per-push attestation.
Actual remote protections, settings and execution remain separately observed.

### Release and work-tracking boundaries

One local release producer prepares the committed main release history in
`CHANGELOG.md` through a release-preparation PR, then binds a SemVer tag and
GitHub Release to an exact reviewed main commit. Development pushes do not
generate release notes or publish versions. Required assets are attached to a
draft before publication; repository configuration cannot prove GitHub's
immutable-release setting. Existing `main-<full SHA>` tags remain historical
refs and are neither moved nor republished.

Version compatibility covers supported CLI commands and options, machine JSON
schemas, governed document profiles and frontmatter, GitOps desired state and
external-service interfaces. For released 1.0-or-later contracts, incompatible
changes raise major, compatible additions raise minor and compatible fixes
raise patch. The operator selects the initial 0.y version and compatibility
promise from the reviewed release scope. A release version certifies neither
deployment nor provider or live runtime acceptance.

Issues own requests and priorities, Specs own contracts, Tasks own execution
and evidence, and Projects display work. Links and one-way metadata connect
them without copying complete Spec/Task bodies or overwriting their state in
both directions. Project activation is remote state, not a consequence of this
architecture description.

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
| [REQ-0003-FR-0016](../../01.requirements/0003-workspace-agent-governance-platform.md) | Local Registry dispatch, proportional selection and independent failure meanings | [ADR-0048](../decisions/0048-local-qa-and-semver-release-ownership.md), [SPEC-0107](../../03.specs/0107-local-qa-and-release/spec.md) |
| [REQ-0003-FR-0017](../../01.requirements/0003-workspace-agent-governance-platform.md) | Local QA and hosted delivery metadata with separate evidence | [ADR-0048](../decisions/0048-local-qa-and-semver-release-ownership.md), [SPEC-0107](../../03.specs/0107-local-qa-and-release/spec.md) |
| [REQ-0003-FR-0018](../../01.requirements/0003-workspace-agent-governance-platform.md) | Exact-index logical delivery and no repeated identical leaf at later stages | [ADR-0048](../decisions/0048-local-qa-and-semver-release-ownership.md), [SPEC-0107](../../03.specs/0107-local-qa-and-release/spec.md) |
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
| [REQ-0003-FR-0031](../../01.requirements/0003-workspace-agent-governance-platform.md) | Paired Skill observations and one aggregate owner, with Stage 99 form and separate runtime authority | [ADR-0048](../decisions/0048-local-qa-and-semver-release-ownership.md), [SPEC-0107](../../03.specs/0107-local-qa-and-release/spec.md) |
| [REQ-0003-NFR-0001](../../01.requirements/0003-workspace-agent-governance-platform.md) | Registry-derived admission rather than a frozen role/provider census | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../98.archive/completed/03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-NFR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | Exact-input local validation, budget preflight and bounded reuse | [ADR-0048](../decisions/0048-local-qa-and-semver-release-ownership.md), [SPEC-0107](../../03.specs/0107-local-qa-and-release/spec.md) |
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
The existing requirement IDs retain their identity. ADR-0036 retains the common
governance design and SPEC-0072 its implementation history. ADR-0048 and SPEC-0107
own the selected local QA and release transition; predecessor decisions remain
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
| [REQ-0003-NFR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | Proportionate local QA and exact-input evidence | [ADR-0048](../decisions/0048-local-qa-and-semver-release-ownership.md) |
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
| N/A — [Acceptance criterion 11](../../01.requirements/0003-workspace-agent-governance-platform.md) remains package-owned | Selected local validation with separate remote observations | [ADR-0048](../decisions/0048-local-qa-and-semver-release-ownership.md) |
| N/A — [Acceptance criterion 12](../../01.requirements/0003-workspace-agent-governance-platform.md) remains package-owned | Zero stale legacy/orphan reference | [ADR 0036](../decisions/0036-common-knowledge-and-prompt-surfaces.md) |

- **Requirement Package**: [REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md)
- **Current decision**: [ADR-0036](../decisions/0036-common-knowledge-and-prompt-surfaces.md)
- **Local QA and release decision**: [ADR-0048](../decisions/0048-local-qa-and-semver-release-ownership.md)
- **Local QA and release implementation**: [SPEC-0107](../../03.specs/0107-local-qa-and-release/spec.md)
- **Original governance implementation**: [SPEC-0072](../../98.archive/completed/03.specs/0072-agent-governance-and-quality-gate-consolidation/spec.md)
- **Wider SDLC program**: [SPEC-0054](../../98.archive/completed/03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md)
- **Historical decisions**: ADR-0019, [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), ADR-0034, ADR-0035

The prior architecture narrative is recoverable from this same path at commit
`bb73116b7b09c4f257fc81baa12cfa8359495fc0`. Its retired providers, fixed retry
counts, synthetic runtime records, and separate agent CI topology are not
current contracts.
