---
title: "Agent and Document Governance Architecture Description (AD)"
version: "2.4.0"
type: "sdlc/architecture-description"
status: "active"
owner: "platform"
updated: "2026-11-10"
layer: "architecture"
artifact_id: "AD-0006"
---

# Agent and Document Governance Architecture Description (AD)

## Overview

This Architecture describes the current owner boundaries of agent, document, validation, and execution evidence.
[ADR-0036](../decisions/0036-common-knowledge-and-prompt-surfaces.md) owns the common governance design. The earlier
Spec packages are deleted; the Archived Lineage table below summarizes them and Git history recovers them.

The selected local delivery design is recorded in
[ADR-0048](../decisions/0048-local-qa-and-semver-release-ownership.md);
SPEC-0107 left the tree (Git history recovers it). That change replaces
recurring hosted QA and per-main-push tagging with local validation and explicit
SemVer releases. The implementation is `scripts/qa.py` and `scripts/release.py`; earlier
cutover evidence does not establish completion of other changes.

This document owns ownership boundaries, flows, evidence classes, and quality attributes. Machine routes, schemas, state enums,
the role roster, validator argv, and task state are referenced at their canonical owners below and not copied.
[AD-0007](./0007-current-local-gitops-platform.md) owns the GitOps desired state and the platform interfaces.
The existence of a file does not prove the installed runtime's discovery or permission enforcement, nor hosted CI success;
actual validation state is confirmed in the relevant Task.

## Boundaries & Non-goals

- Common governance owns the meaning of common policy, roles, and skills, and role metadata.
- Stage 99 owns document profiles and forms and defines neither role permissions nor execution success.
- The execution registry and scripts own check selection, execution limits, and failure handling.
- The repository does not own provider accounts, authentication, model access, or global installs. External accounts,
  credentials, provider capabilities, and the live runtime are not implementation evidence for this document.
- GitOps desired state, Kubernetes policy, and external service interfaces stay in their existing domains.
- No separate governance registry, per-provider policy fork, Release family, or shared progress ledger is created.
- SPEC-0152 (left the tree; Git history recovers it) completed the manual
  disposition policy and bounded first-record Spec/Plan approval change. The
  [REQ-0003 Archived Lineage](../../01.requirements/0003-workspace-agent-governance-platform.md#archived-lineage)
  retains its Task acceptance and exact recovery route; current authority is
  the lifecycle policy and accepted ADR-0056, not a deleted package.

## Quality Attributes

| Quality attribute | Stimulus | Environment | Response | Measure |
| --- | --- | --- | --- | --- |
| Consistency (REQ-0003-FR-0001, REQ-0003-FR-0010) | A role, skill, profile or gateway states a responsibility | Repository tree with thin provider projections | One machine owner and one prose owner per responsibility; projections stay thin | Registry/schema, profile, owner and adapter parity checks PASS |
| Verifiability (REQ-0003-FR-0026) | A result is reported as evidence | Static, provider-runtime, hosted-CI and remote/live classes | The classes stay apart; an unobserved class gets an owner and a retry trigger | Direct observation recorded per class in the Task |
| Reliability (REQ-0003-FR-0011, REQ-0003-FR-0028) | A command hangs, overflows or leaves descendants | Bounded validation runner | Finite time and output limits, descendant cleanup, bounded retry, a no-progress stop and safe resume | Bounded-runner timeout, overflow, cancellation, pipe and recovery regressions PASS |
| Security (REQ-0003-FR-0007) | A native permission widens, or an external mutation is requested | Provider projections and approval boundaries | Native permissions stay within registered scope; secrets, auth and full transcripts are excluded; external mutation needs separate approval | Independent permission/path rejection tests and independent review |
| Recoverability (REQ-0003-FR-0015, REQ-0003-FR-0020) | A current document is proposed for deletion or an archive move | Git history and the owning Task | The accepted manual-review decision requires consumer, preservation, hold and authority review; Git-only disposition also requires exact-source recovery and byte comparison; unmet conditions defer that disposition | Task records each manual result and current owner; static lifecycle checks do not enforce these prerequisites or prove acceptance |
| Reproducibility (REQ-0003-FR-0016, REQ-0003-NFR-0002) | A local result is reused | Exact-index isolation | A result names its input bytes, configuration, tool, scope, mode, trust and relevant history, and is refused after a relevant input changes | Dependency identity and reuse-refusal fixtures |
| Proportional cost (REQ-0003-FR-0016, REQ-0003-NFR-0002) | An ordinary document edit or an identical later stage | Local registry selection | Each selected leaf runs once per identical input; implementation regression discovery is not invoked for ordinary edits | Registry selection and actual invocation evidence in the owning Task |
| Maintainability (REQ-0003-FR-0024, REQ-0003-NFR-0001) | A wrapper, script or census outlives its consumer | The actual consumer graph | Targeted/affected/staged selection and purpose-specific gates replace fixed censuses and duplicate wrappers | Direct negative fixtures; aggregate all-files retirement stays with the owning Task |
| Legibility (REQ-0003-FR-0002) | A gateway or provider note is added | Root and provider gateways | Gateways point to common owners without copied policy bodies | Native syntax parse and canonical-reference tests PASS |

## System Overview & Context

| Component | Canonical owner | Responsibility |
| --- | --- | --- |
| Entry | Root `AGENTS.md` and `CLAUDE.md` | Explicitly select common policy and relevant procedures |
| Policy | `.agents/governance/` | Approval, security, Git, document and quality meaning |
| Role metadata | `.agents/roles/registry.json` and adjacent schema | Stable IDs, neutral permission classes, handoffs, skills and provider binding paths |
| Role bodies and procedures | `.agents/roles/` and `.agents/skills/` | Neutral responsibilities and reusable work steps |
| Provider contract | `.claude/provider.md` and `.codex/provider.md` | Supported native syntax, loading route, and evidence limits |
| Native adapters | `.claude/bindings.json`, `.codex/bindings.json` and their projections | Provider-specific values and explicit common references; projections are checked consumers, not generators |
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
current authority location and carries forward the QA and CD boundary
its deleted predecessors decided (see Archived Lineage).

### Authority planes

| Plane | Canonical owner | Consumers and limits |
| --- | --- | --- |
| Agent role/skill machine truth | [Common governance role registry](../../../.agents/roles/registry.json) and adjacent schema | Neutral IDs, classes, handoffs, skills and provider binding paths; no concrete native value authored here |
| Provider-native binding | [Claude bindings](../../../.claude/bindings.json) and [Codex bindings](../../../.codex/bindings.json) | One concrete model/effort/scope/skill table per provider; checked role projections consume it under independent neutral permission ceilings, while discovery and runtime enforcement remain separate evidence |
| Human execution policy | [Common governance](../../../.agents/README.md) | Root/provider gateways, role responsibilities, approval, quality, and document authoring; copying the machine schema is forbidden |
| Document machine contract and forms | [Stage 99 Registry](../../99.templates/registry.json) and [forms](../../99.templates/README.md) | Profile, route, metadata, identity, lifecycle, and template consumers |
| Validation dispatch | [Validation Registry](../../../scripts/validation/registry.json) | Local affected-path, lane, and argv; each validator keeps its own failure meaning |
| Execution | [Stage 03](../../03.specs/README.md) | Package-local Spec/Plan/Tasks; state, order, and validation evidence are not copied into a central roster |
| Skill evaluation evidence | [Evaluation router](../../../.agents/evaluations/README.md) | Same-task noSkill/withSkill observations and their scoring; evidence form belongs to Stage 99, Skill membership and runtime contracts remain with their existing owners |
| Operations and reference | [Stage 05](../../05.operations/README.md), [Stage 90](../../90.references/README.md) | Operating procedures kept apart from observed evidence; a Reference does not substitute for approval or current policy |
| Historical recovery | Reachable Git, the owning Task and profile-specific lineage owners | The [accepted manual-review decision](../decisions/0056-manual-document-disposition-review.md) keeps evidence in every owning Task, Archived Lineage for Stage 01-03, and existing profile relationships for other types; [Stage 98](../../98.archive/README.md) remains unvalidated history under ADR-0053 and is not current authority or a reactivation path |

The number of roles and surfaces is derived from the common governance registry. The past local/Antigravity/Gemini proposals are not the current
supported roster. `.agents/roles/` owns the current machine truth of common roles and skills,
and `.agents/governance/` owns the execution policy. The current provider projection files are repository-static configuration,
not evidence of an observed authenticated discovery or run.

### Consumer and validation flow

1. A task sets its scope, role, skill, and approval boundaries in common governance and links to a package-local Plan/Task.
2. The current domain owner and registries select the change's profile, affected paths, and required local lanes; actual tools, resources and execution authority are resolved before implementation without a business/session deadline gate.
3. Each validator checks its independent contract and records its result, fallback, and limits under the matching evidence class.
4. The reviewer confirms consumer succession and negative fixtures and validates a stable staged snapshot.
5. The Task records commands, results, and unfinished owners. No external execution happens without separate approval and observation.

The aggregate selects the Registry's applicable local checks rather than owning
another copy of argv or policy. Ordinary document content selects profile,
relationship, link and state checks. Implementation regressions follow changes
to their responsible implementation or declared inputs. A global QA-contract
change or explicit bounded audit selects named affected purpose and unit checks;
the long full/ci sweep and blanket unit discovery are retired from completion.
Distinct document, platform and
security rules retain their failure meanings when their orchestration is shared.

## Data Architecture

Role metadata references canonical role bodies, skill IDs and provider binding
paths; it does not copy native values or policy prose. Each provider binding
table owns its native model, effort, skill and scope mapping; checked role
projections retain the supported client format. Independent neutral class
ceilings reject a coordinated table/projection permission widening. Static
metadata validation cannot prove account availability, native permission
enforcement or authenticated execution.

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


Retirement of a past cutover's fixed census and completion proof transfers any unique ongoing protection
before removing its caller, registration and dedicated helper, fixture or test. Historical facts remain in Git history
alone. Active policy, provider loading, and command selection do not consume a retired proposal as
current authority. Test fixtures are bounded synthetic inputs, never production
configuration or runtime admission evidence.

### State, identity and evidence

The common governance registry owns role/skill identity, Stage 99 owns document identity/profile/state, and the
Validation Registry owns lanes and argv. A body change to an ordinary current document is judged by semantic/profile and link
validation, and an ordinary body is not fixed with a permanent SHA pin. The lifecycle validator judges
Registry-classified profiles, states, and allowed edges.

The local first-record approval extension in the
[Stage 99 Registry](../../99.templates/registry.json), described by
[ADR-0056](../decisions/0056-manual-document-disposition-review.md), retains
`draft` as the ordinary initial state of a Spec or Plan. Only a new Spec/Plan
pair in the same package can be admitted as `approved` through contextual
validation of the owning Task's actual batch-review and user-approval receipt.
The existing lifecycle reader verifies the pair's identity and relationships,
reviewed byte hashes, approval and review references, scope, and recorded
validity/revocation checks. The receipt's exact format stays with
the current [document lifecycle policy](../../../.agents/governance/document-lifecycle.md),
Stage 99 Registry and lifecycle reader. SPEC-0152 (left the tree; Git history
recovers it) records the original implementation. A standalone comparison without that context, or an
incomplete or mismatched receipt, remains a creation failure.

This machine check validates recorded structure and candidate bytes; the
trusted approval route owns verification of the actual user and authorization.
The exception neither turns past authoring into retroactive execution
authority nor changes Task PASS/completion, criterion acceptance, ADR
acceptance, protected operations or the shared-contract edition.

Risk, tool/data trust, oversight, stop, approval, trace, evaluation, and provenance link to
the current Registry and common governance responsibilities. The past `agentSystems`/`evidenceOwnerPolicies`
proposal is not claimed as an implemented parallel contract. A static declaration of high-risk execution or runtime
enforcement is not evidence of successful execution or policy enforcement.

### Terminal disposition and historical lineage

Before a disposition, source → current semantic owner → every current consumer
is proven. [ADR-0056](../decisions/0056-manual-document-disposition-review.md)
records the accepted manual-review amendment completed by SPEC-0152. Its canonical
procedure belongs to [document lifecycle](../../../.agents/governance/document-lifecycle.md):
review current and historical consumers, preservation needs, holds and valid
disposition authority; Git-history-only removal also needs a reachable exact
source and temporary recovery with byte comparison. The Task owns those
findings and any disposition deferral. Until an unmet condition is resolved,
the source remains in place without regaining current authority. Candidate
implementation, acceptance and a later actual disposition remain distinct.

Once its applicable conditions are met, a non-current document follows its
existing type-specific route. Stage 01-03 documents have no superseded,
retired or withdrawn state: their current semantic owner summarizes a
completed disposition in Archived Lineage and Git history recovers the source.
Other document types retain their profile's existing reciprocal lifecycle or
disposition relationships without adding an Archived Lineage table. The owning
Task records manual-review evidence for every type.
A wholly replaced ADR's successor keeps the predecessor ID in `supersedes`
and Traceability. A scoped amendment instead identifies the replaced clauses
while retaining the other accepted decisions, as ADR-0055 does.
[ADR-0053](../decisions/0053-unvalidated-archive.md) keeps Stage 98 outside
document-content validation, and ADR-0055 retains the README lint exception.
The accepted manual-review decision adds no recovery ledger, catalog or automatic
archive-disposition/content check and does not reopen historical removals.
The first-record approval exception above changes only the separate
Spec/Plan creation-evidence contract.

REQ-0005/0006 → REQ-0008 is the original supersession history (those requirements left the tree; Git history recovers them). REQ-0003 is the transitive
current semantic successor of this convergence and does not rewrite the original decision target.

### Loop and checkpoint

The [bounded validation runner](../../../scripts/run-validation-lane.py) owns
the timeout, output, and child cleanup limits, and the Task owns the no-progress stop and handoff evidence.
A checkpoint is ignored transient recovery state and replaces neither policy, the Task, nor a credential store.
Compaction and resume keep only finished and unfinished work, validation results, and the next action, and exclude sensitive data and full transcripts.
Reusable decision context may live in the shared workspace memory store
(`scripts/workspace_memory.py`, Git-ignored `.workspace-memory/`). Both
providers read and write it, and their native memory is disabled in project
configuration. It is never Task status, evidence, approval or acceptance, and
it is not the retired shared progress ledger. The shared store belongs to the
representative worktree; source references are checked against the caller
worktree without following symlinks. Request-bound retries, a capacity bound
on every store connection, and verified atomic backup replacement protect
context integrity. The store grants no authority to the stored context.

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

Tracked provider configuration and projections are secret-free repository configuration. The user's credential store is
neither read nor migrated. Native parsers and canaries are handled in the provider owner's independent evidence lane,
and no provider credential is added to hosted CI.

Provider permission and hook hardening is recorded in the provider notes;
native configuration parsing and operator-relayed hook delivery are separate
observations. The recorded host `bwrap` startup failure does not establish operating-system
sandbox isolation; a command subsequently approved outside that sandbox
supplies no workspace-isolation evidence. Native syntax and loading remain
with the [provider notes](../../../.codex/provider.md), while current r10
findings and follow-up verification belong to the provider owner's evidence.

The implementation validation owners are [document contracts](../../../scripts/document_contracts.py),
[lifecycle](../../../scripts/document_lifecycle.py), and the lanes the Validation Registry points to.
Exact commands and tool versions are read from their execution owners and not copied into this Architecture.

### Local delivery stages

| Stage | Execution owner and boundary |
| --- | --- |
| Editing | Focused behavior regressions and affected content checks selected from the current local registry |
| Logical commit | Exact-index staged validation and the actual Commitizen message check; an active hook's identical leaf is not repeated manually |
| Feature push | Git transport preserves commit evidence and adds no repeated QA requirement |
| PR and main integration | Review local evidence and check inputs changed by integration; refresh only invalidated results |
| After merge | Verify delivered identity and state; a merge resolution that changes validated inputs selects the affected checks |
| Global QA-contract change or bounded audit | Resolve tools, time, output and native execution approval for affected purpose gates and named behavior and security units; do not run a blanket sweep |
| Release | Validate release inputs and publish through one producer; tag or Release publication does not repeat QA |

GitHub Actions retains `ci-summary`, which validates branch and PR commit
metadata, and a separate PR-only selected style job. `ci-summary` reports the
branch-policy verdict itself. Its canonical Python producer is projected as
matching inline workflow logic: it reads candidate commit objects as data,
uses trusted-base message grammar, checks the actual merge identity and parents,
and validates the complete base-to-head commit range. The workflow separately
checks its PR branch-prefix policy. Missing metadata, an
invalid PR base or source branch, a failed commit identity/range check, or an
unexpected event/ref fails that job; PR branch policy is not applicable on
main. The workflow and its inline projection remain PR-editable, so independent
protected workflow control requires separate remote evidence. Historical hosted
full QA `NOT_RUN` records remain evidence, not a current check. A successful
metadata or style job does not certify local purpose QA. This design gives up an
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
Conftest/Rego policy, separate from common agent policy. External OpenBao
([ADR-0041](../decisions/0041-openbao-secret-backend.md)), PostgreSQL, and Valkey remain interface contracts, not services operated by QA.

A local commit does not authorize push, PR creation, workflow dispatch, release,
cluster mutation, or external service changes. Hosted, native provider, and live
verification require their own actual evidence and applicable authorization.

## Traceability

### Lifecycle Traceability

| Upstream requirement | Quality attribute or boundary | ADR / Spec |
| --- | --- | --- |
| [REQ-0003-FR-0001](../../01.requirements/0003-workspace-agent-governance-platform.md) | Agent Registry, common governance prose, and Stage 99 document-contract authority planes | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [ADR-0036](../decisions/0036-common-knowledge-and-prompt-surfaces.md), [ADR-0047](../decisions/0047-agent-contract-and-resource-ownership.md), [ADR-0048](../decisions/0048-local-qa-and-semver-release-ownership.md) |
| [REQ-0003-FR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | Thin provider projections with native syntax isolated from shared policy | [ADR-0036](../decisions/0036-common-knowledge-and-prompt-surfaces.md), [ADR-0047](../decisions/0047-agent-contract-and-resource-ownership.md) |
| [REQ-0003-FR-0003](../../01.requirements/0003-workspace-agent-governance-platform.md) | Skill-source provenance and unavailable-capability boundary | [ADR-0036](../decisions/0036-common-knowledge-and-prompt-surfaces.md) |
| [REQ-0003-FR-0004](../../01.requirements/0003-workspace-agent-governance-platform.md) | Package-local scope and approval handoff into domain owners | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [ADR-0052](../decisions/0052-single-main-trunk-branch-strategy.md) |
| [REQ-0003-FR-0005](../../01.requirements/0003-workspace-agent-governance-platform.md) | Task-owned durable evidence and ignored transient checkpoint separation | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [ADR-0048](../decisions/0048-local-qa-and-semver-release-ownership.md) |
| [REQ-0003-FR-0006](../../01.requirements/0003-workspace-agent-governance-platform.md) | Repository form owner separated from external reference formats | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [ADR-0033](../decisions/0033-common-document-contract-v9.md) |
| [REQ-0003-FR-0007](../../01.requirements/0003-workspace-agent-governance-platform.md) | Common governance approval gates around secret, external, and live execution | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [ADR-0047](../decisions/0047-agent-contract-and-resource-ownership.md) |
| [REQ-0003-FR-0008](../../01.requirements/0003-workspace-agent-governance-platform.md) | Registry-derived provider projection admission | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md) |
| [REQ-0003-FR-0009](../../01.requirements/0003-workspace-agent-governance-platform.md) | Static provider metadata versus authenticated runtime evidence | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md) |
| [REQ-0003-FR-0010](../../01.requirements/0003-workspace-agent-governance-platform.md) | Agent Registry ownership of permission, stop and handoff semantics | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [ADR-0031](../decisions/0031-current-corpus-retention-and-validation-ownership.md), [ADR-0047](../decisions/0047-agent-contract-and-resource-ownership.md) |
| [REQ-0003-FR-0011](../../01.requirements/0003-workspace-agent-governance-platform.md) | Loop contract as bounded retry, no-progress and resume owner | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md) |
| [REQ-0003-FR-0012](../../01.requirements/0003-workspace-agent-governance-platform.md) | Stage 99 machine contract versus common governance authoring policy, including the bounded local first-record approval extension | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [ADR-0031](../decisions/0031-current-corpus-retention-and-validation-ownership.md), [ADR-0033](../decisions/0033-common-document-contract-v9.md), [ADR-0056](../decisions/0056-manual-document-disposition-review.md), SPEC-0152 (left the tree; Git history recovers it) |
| [REQ-0003-FR-0013](../../01.requirements/0003-workspace-agent-governance-platform.md) | One form route per document profile with schema/template parity | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [ADR-0033](../decisions/0033-common-document-contract-v9.md) |
| [REQ-0003-FR-0014](../../01.requirements/0003-workspace-agent-governance-platform.md) | Stage-specific purpose boundaries and no parallel Release family | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [ADR-0033](../decisions/0033-common-document-contract-v9.md), [ADR-0047](../decisions/0047-agent-contract-and-resource-ownership.md) |
| [REQ-0003-FR-0015](../../01.requirements/0003-workspace-agent-governance-platform.md) | Consumer succession and accepted manual pre-disposition review; completed package evidence is in REQ-0003 Archived Lineage | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [ADR-0031](../decisions/0031-current-corpus-retention-and-validation-ownership.md), [ADR-0047](../decisions/0047-agent-contract-and-resource-ownership.md), [ADR-0056](../decisions/0056-manual-document-disposition-review.md), SPEC-0152 (left the tree; Git history recovers it) |
| [REQ-0003-FR-0016](../../01.requirements/0003-workspace-agent-governance-platform.md) | Local Registry dispatch, proportional selection and independent failure meanings | [ADR-0031](../decisions/0031-current-corpus-retention-and-validation-ownership.md), [ADR-0047](../decisions/0047-agent-contract-and-resource-ownership.md), [ADR-0048](../decisions/0048-local-qa-and-semver-release-ownership.md) |
| [REQ-0003-FR-0017](../../01.requirements/0003-workspace-agent-governance-platform.md) | Local QA and hosted delivery metadata with separate evidence | [ADR-0048](../decisions/0048-local-qa-and-semver-release-ownership.md) |
| [REQ-0003-FR-0018](../../01.requirements/0003-workspace-agent-governance-platform.md) | Exact-index logical delivery and no repeated identical leaf at later stages | [ADR-0048](../decisions/0048-local-qa-and-semver-release-ownership.md), [ADR-0052](../decisions/0052-single-main-trunk-branch-strategy.md) |
| [REQ-0003-FR-0019](../../01.requirements/0003-workspace-agent-governance-platform.md) | Package-local sequencing with unchanged historical program lineage | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [ADR-0047](../decisions/0047-agent-contract-and-resource-ownership.md) |
| [REQ-0003-FR-0020](../../01.requirements/0003-workspace-agent-governance-platform.md) | Unvalidated archive with accepted manual hold, authority and exact-source recovery checks before disposition | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [ADR-0031](../decisions/0031-current-corpus-retention-and-validation-ownership.md), [ADR-0053](../decisions/0053-unvalidated-archive.md), [ADR-0056](../decisions/0056-manual-document-disposition-review.md), SPEC-0152 (left the tree; Git history recovers it) |
| [REQ-0003-FR-0021](../../01.requirements/0003-workspace-agent-governance-platform.md) | Reference provenance separated from current execution authority | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [ADR-0047](../decisions/0047-agent-contract-and-resource-ownership.md) |
| [REQ-0003-FR-0022](../../01.requirements/0003-workspace-agent-governance-platform.md) | Ignored checkpoint state and the shared memory store versus Task-owned durable execution evidence | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [ADR-0047](../decisions/0047-agent-contract-and-resource-ownership.md) |
| [REQ-0003-FR-0023](../../01.requirements/0003-workspace-agent-governance-platform.md) | Profile-owned stable identity and source-preserving migration mapping | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [ADR-0033](../decisions/0033-common-document-contract-v9.md) |
| [REQ-0003-FR-0024](../../01.requirements/0003-workspace-agent-governance-platform.md) | Consumer-zero removal of compatibility surfaces after semantic transfer | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [ADR-0031](../decisions/0031-current-corpus-retention-and-validation-ownership.md), [ADR-0047](../decisions/0047-agent-contract-and-resource-ownership.md), [ADR-0048](../decisions/0048-local-qa-and-semver-release-ownership.md) |
| [REQ-0003-FR-0025](../../01.requirements/0003-workspace-agent-governance-platform.md) | Current Agent Registry and common governance risk, trust, and approval owners | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md) |
| [REQ-0003-FR-0026](../../01.requirements/0003-workspace-agent-governance-platform.md) | Separate repository-static, provider-runtime, hosted-CI and live evidence | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [ADR-0047](../decisions/0047-agent-contract-and-resource-ownership.md), [ADR-0048](../decisions/0048-local-qa-and-semver-release-ownership.md) |
| [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md) | Lifecycle edges separated from ordinary body edits; first-record approval fails closed without same-package reviewed-byte receipt context | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [ADR-0048](../decisions/0048-local-qa-and-semver-release-ownership.md), [ADR-0056](../decisions/0056-manual-document-disposition-review.md), SPEC-0152 (left the tree; Git history recovers it) |
| [REQ-0003-FR-0028](../../01.requirements/0003-workspace-agent-governance-platform.md) | Direct negative fixtures with explicit tool-failure and fallback diagnostics | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [ADR-0047](../decisions/0047-agent-contract-and-resource-ownership.md) |
| [REQ-0003-FR-0029](../../01.requirements/0003-workspace-agent-governance-platform.md) | One SemVer tag and GitHub Release producer prepared from a reviewed main release-preparation PR | [ADR-0048](../decisions/0048-local-qa-and-semver-release-ownership.md) |
| [REQ-0003-FR-0030](../../01.requirements/0003-workspace-agent-governance-platform.md) | Retirement of CI/QA scripts, tests and `.github/` surfaces only after consumer and coverage transfer (SPEC-0140 left the tree; Git history recovers it) | [ADR-0048](../decisions/0048-local-qa-and-semver-release-ownership.md) |
| [REQ-0003-FR-0031](../../01.requirements/0003-workspace-agent-governance-platform.md) | Paired Skill observations and one aggregate owner, with Stage 99 form and separate runtime authority | [ADR-0048](../decisions/0048-local-qa-and-semver-release-ownership.md) |
| [REQ-0003-NFR-0001](../../01.requirements/0003-workspace-agent-governance-platform.md) | Registry-derived admission rather than a frozen role/provider census | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md) |
| [REQ-0003-NFR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | Exact-input local validation, budget preflight and bounded reuse | [ADR-0048](../decisions/0048-local-qa-and-semver-release-ownership.md) |
| [REQ-0003-NFR-0003](../../01.requirements/0003-workspace-agent-governance-platform.md) | Primary-source traceability with repository conventions labeled separately | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md) |
| [REQ-0003-NFR-0004](../../01.requirements/0003-workspace-agent-governance-platform.md) | Explicit baseline-failure and environment-limit reporting | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md) |
| [REQ-0003-IF-0001](../../01.requirements/0003-workspace-agent-governance-platform.md) | Atomic owner/consumer migration and reciprocal-link validation | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [ADR-0047](../decisions/0047-agent-contract-and-resource-ownership.md), [ADR-0048](../decisions/0048-local-qa-and-semver-release-ownership.md) |
| [REQ-0003-IF-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | External catalog provenance without policy or permission authority | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md) |
| N/A — [Acceptance criterion 01](../../01.requirements/0003-workspace-agent-governance-platform.md) remains package-owned | Owner graph consistency | [ADR-0036](../decisions/0036-common-knowledge-and-prompt-surfaces.md) |
| N/A — [Acceptance criterion 02](../../01.requirements/0003-workspace-agent-governance-platform.md) remains package-owned | Reciprocal lifecycle chain | [ADR-0036](../decisions/0036-common-knowledge-and-prompt-surfaces.md) |
| N/A — [Acceptance criterion 03](../../01.requirements/0003-workspace-agent-governance-platform.md) remains package-owned | Gateway/evidence-class separation | [ADR-0036](../decisions/0036-common-knowledge-and-prompt-surfaces.md) |
| N/A — [Acceptance criterion 04](../../01.requirements/0003-workspace-agent-governance-platform.md) remains package-owned | Repository static gate | [ADR-0036](../decisions/0036-common-knowledge-and-prompt-surfaces.md) |
| N/A — [Acceptance criterion 05](../../01.requirements/0003-workspace-agent-governance-platform.md) remains package-owned | Template form authority | [ADR-0036](../decisions/0036-common-knowledge-and-prompt-surfaces.md) |
| N/A — [Acceptance criterion 06](../../01.requirements/0003-workspace-agent-governance-platform.md) remains package-owned | Registry-derived role/provider parity | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md) |
| N/A — [Acceptance criterion 07](../../01.requirements/0003-workspace-agent-governance-platform.md) remains package-owned | Admitted-provider independent canary classification and readiness evidence | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md) |
| N/A — [Acceptance criterion 08](../../01.requirements/0003-workspace-agent-governance-platform.md) remains package-owned | Contract/schema/provider parity | [ADR-0036](../decisions/0036-common-knowledge-and-prompt-surfaces.md) |
| N/A — [Acceptance criterion 09](../../01.requirements/0003-workspace-agent-governance-platform.md) remains package-owned | Recovery fixture and safe resume | [ADR-0036](../decisions/0036-common-knowledge-and-prompt-surfaces.md) |
| N/A — [Acceptance criterion 10](../../01.requirements/0003-workspace-agent-governance-platform.md) remains package-owned | Eval/model-fitness evidence | [ADR-0036](../decisions/0036-common-knowledge-and-prompt-surfaces.md) |
| N/A — [Acceptance criterion 11](../../01.requirements/0003-workspace-agent-governance-platform.md) remains package-owned | Selected local validation with separate remote observations | [ADR-0048](../decisions/0048-local-qa-and-semver-release-ownership.md) |
| N/A — [Acceptance criterion 12](../../01.requirements/0003-workspace-agent-governance-platform.md) remains package-owned | Zero stale legacy/orphan reference | [ADR-0036](../decisions/0036-common-knowledge-and-prompt-surfaces.md) |
| N/A — [Acceptance criterion 13](../../01.requirements/0003-workspace-agent-governance-platform.md) remains package-owned | Main release-preparation PR with one SemVer tag/Release producer | [ADR-0048](../decisions/0048-local-qa-and-semver-release-ownership.md) |
| N/A — [Acceptance criterion 14](../../01.requirements/0003-workspace-agent-governance-platform.md) remains package-owned | No proven one-off or duplicate script, test or `.github/` execution after consumer succession | [ADR-0048](../decisions/0048-local-qa-and-semver-release-ownership.md) |

### Architecture responsibility transfer

| Original description | Retained current responsibility | Consumer transfer |
| --- | --- | --- |
| AD-0008 | This AD: document machine owner, form parity, purpose-specific README, affected routing, CI/security and review boundaries | REQ-0003 member-ID map; terminal ADRs retain original decision citations |
| AD-0009 | This AD: lifecycle/profile evidence, legal recovery, package-local lineage, Reference/scratch and non-promotable evidence | REQ-0003 member-ID map; original follow-up and supersession chronology unchanged |
| AD-0011 | This AD: authority planes, stable identity, current taxonomy, validator ownership, consumer-zero and lifecycle/body separation | REQ-0003; earlier Spec history is in Archived Lineage |
| AD-0010, shared assurance boundary | This AD: validation routing, CI/QA, approval and direct negative tests; AD-0007 retains platform-specific design | REQ-0003/0004 explicit member transfer |

The replacement record and this responsibility table express semantic succession, not a new claim that historical
ADRs originally served this AD. Superseded ADR bodies are summarized in Archived Lineage and deleted; Git history recovers them.
The existing requirement IDs retain their identity. ADR-0048 owns the selected local QA and release transition; predecessor decisions remain
historical evidence rather than parallel operating instructions.

- **Requirement Package**: [REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md)
- **Current decision**: [ADR-0036](../decisions/0036-common-knowledge-and-prompt-surfaces.md)
- **Local QA and release decision**: [ADR-0048](../decisions/0048-local-qa-and-semver-release-ownership.md)
- **Current-state amendment**: [ADR-0055](../decisions/0055-governance-decision-current-state-amendment.md) replaces the governance ADR clauses that no longer match the repository
- **Accepted manual disposition amendment**: [ADR-0056](../decisions/0056-manual-document-disposition-review.md) qualifies the no-proof disposition and unconditional Git-recovery clauses and records the bounded local first-record approval exception; the user's acceptance and completed implementation are separately recorded in REQ-0003 Archived Lineage
- **Local QA and release implementation**: `scripts/qa.py` and `scripts/release.py`
- **Completed change**: SPEC-0152 (left the tree; Git history recovers it) produced the manual policy and bounded approval reader. Its accepted Task and exact three-file recovery route are summarized in [REQ-0003 Archived Lineage](../../01.requirements/0003-workspace-agent-governance-platform.md#archived-lineage). Earlier Spec packages also remain recoverable through their lineage owners.
- **Historical decisions**: [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md); earlier ADRs are in Archived Lineage

The prior architecture narrative is recoverable from this same path at commit
`bb73116b7b09c4f257fc81baa12cfa8359495fc0`. Its retired providers, fixed retry
counts, synthetic runtime records, and separate agent CI topology are not
current contracts.

### Archived Lineage

These documents were deleted from `docs/98.archive/` or the decision log under SPEC-0140 and are recovered with `git show 69445fca:<path>`.
The ADR-0013 to ADR-0025 and ADR-0035 rows were already deleted from `docs/98.archive/superseded/` at that commit
(`fe3bd418`); recover them with `git show 9a509be9:<path>`.

| Source | Kind | Summary | Original path |
| --- | --- | --- | --- |
| ADR-0013 | superseded decision | Stage 00 Canonical Adapter Model: kept AI Agent governance in one Stage 00 common root and separated provider-native adapters, local adapters and symlink views. Provider-specific shared surfaces and the custom-hook model were replaced by ADR-0030. | `docs/98.archive/superseded/02.architecture/decisions/0013-stage-00-canonical-adapter-model.md` |
| ADR-0015 | superseded decision | Declarative Document Contract Registry: made one machine-readable registry the owner of document routes, metadata profiles, lifecycle states, section profiles and README profiles. ADR-0030 replaced its fixed metadata baseline and profile inventory and kept the registry as sole machine authority. | `docs/98.archive/superseded/02.architecture/decisions/0015-declarative-document-contract-registry.md` |
| ADR-0016 | superseded decision | Program-to-Tranche Document Lineage: defined numeric and semantic lineage for one program PRD implemented through several dependent Specs. ADR-0031 superseded its instance-roster and validation-routing authority. | `docs/98.archive/superseded/02.architecture/decisions/0016-program-to-tranche-document-lineage.md` |
| ADR-0017 | superseded decision | Program Follow-up Lineage Semantics: kept ADR-0016's seven modernization tranches while modeling a completed Spec as a follow-up within the same program. ADR-0031 superseded its instance-roster and validation-routing authority. | `docs/98.archive/superseded/02.architecture/decisions/0017-program-follow-up-lineage-semantics.md` |
| ADR-0018 | superseded decision | Full-body Archive Record and Retention: replaced metadata-only archive Tombstones with one immutable, non-current, full-body record at each mirrored original path. ADR-0030 superseded the full-body and no-Tombstone clauses; ADR-0053 later withdrew archive validation. | `docs/98.archive/superseded/02.architecture/decisions/0018-full-body-archive-record-and-retention.md` |
| ADR-0019 | superseded decision | Provider-Native Agent Harness and Loop Model: projected Stage 00 governance onto local/Antigravity, Claude, Codex and Gemini surfaces with one machine harness contract, per-role model and effort, a bounded execution loop and strict runtime evidence. ADR-0030 replaced the provider roster and harness ownership. | `docs/98.archive/superseded/02.architecture/decisions/0019-provider-native-agent-harness-and-loop-model.md` |
| ADR-0020 | superseded decision | Document Lifecycle Program Closure Evidence: recorded the closure-evidence architecture for the PRD-006 and ARD-0009 document lifecycle program. ADR-0031 superseded its instance-roster and validation-routing authority. | `docs/98.archive/superseded/02.architecture/decisions/0020-document-lifecycle-program-closure-evidence.md` |
| ADR-0021 | superseded decision | Canonical Surface Routing and Evidence-Depth Architecture: selected reference-based projections of GitHub routing and platform evidence depth on top of the existing validation-surface contract. ADR-0031 superseded its instance-roster and validation-routing authority. | `docs/98.archive/superseded/02.architecture/decisions/0021-canonical-surface-routing-and-evidence-depth.md` |
| ADR-0022 | superseded decision | Direct-Approval Standalone Execution Lineage: added one optional standalone-execution relation (a directly approved Spec, Plan and Task) to document profile registry schema v8. ADR-0031 superseded its instance-roster and validation-routing authority. | `docs/98.archive/superseded/02.architecture/decisions/0022-direct-approval-standalone-execution-lineage.md` |
| ADR-0023 | superseded decision | Work-Unit Document Taxonomy and Governance Authority: set the work-unit-centered document topology with a stable Stage 05 operations path and one authority plane for document and AI-agent governance. ADR-0030 replaced its `tasks.md`, agent-contract and ArchiveEnvelope clauses. | `docs/98.archive/superseded/02.architecture/decisions/0023-work-unit-document-taxonomy-and-governance-authority.md` |
| ADR-0024 | superseded decision | Terminal Artifact Identity and Archive Layout: established the Architecture Description, a closed global artifact identity grammar, stable terminal Stage 98 records and a script closure from 50 to 47 assets. ADR-0030 replaced its terminal form split, archive and census design. | `docs/98.archive/superseded/02.architecture/decisions/0024-terminal-artifact-identity-and-archive-layout.md` |
| ADR-0025 | superseded decision | Four-Digit Document Path Identity: standardized every numeric identity token in authored `docs/` routes on four zero-padded digits and fixed the lowercase Incident package grammar. ADR-0030 replaced only its old family table. | `docs/98.archive/superseded/02.architecture/decisions/0025-four-digit-document-path-identity.md` |
| ADR-0035 | superseded decision | Common Agents Authority and Native Skill Routing: moved the common authority to `.agents/`, retired the former documentation governance root and refused optional memory, rule, prompt, evaluation and script directories. Superseded by ADR-0036, which adopted a knowledge and a prompt surface. | `docs/98.archive/superseded/02.architecture/decisions/0035-common-agents-authority-and-native-skill-routing.md` |
| ADR-0032 | superseded decision | Terminal Document Retention and Archive Stage Taxonomy: retained completed and terminal governed documents instead of deleting them and gave Stage 98 four subdirectories. Superseded by ADR-0038 (six dispositions); Stage 98 validation was later withdrawn by ADR-0053. | `docs/98.archive/superseded/02.architecture/decisions/0032-completed-and-terminal-document-retention.md` |
| ADR-0039 | superseded decision | Unit Archive Retention and Citation Table: kept ADR-0038's six dispositions, retained whole units byte for byte with one catalog row each, decided every citation through one ordered registry table, and tracked moves between active stages by identity. Superseded by ADR-0040 on 2026-09-17; removed from the decision log under SPEC-0140. | `docs/02.architecture/decisions/0039-unit-archive-retention-and-citation-table.md` |
| ADR-0040 | superseded decision | Archive Reappraisal and Verifiable Sources: froze retained units against unapproved change, judged their evidential value in a Retention Assessment table, and verified envelopes against the default branch. Superseded by ADR-0053, which stopped validating the archive; removed from the decision log under SPEC-0140. | `docs/02.architecture/decisions/0040-archive-reappraisal-and-verifiable-sources.md` |
| AD-0008 | superseded architecture | Workspace Document Assurance Operating Model: one owner per fact across human governance, machine-readable profiles, template forms, validators, provider adapters and CI selectors, with copies treated as non-authoritative views. Replaced by AD-0006. | `docs/98.archive/superseded/02.architecture/descriptions/0008-workspace-document-assurance-operating-model.md` |
| AD-0009 | superseded architecture | Document Lifecycle and Evidence Operating Model: extended the assurance platform with lifecycle and evidence handling (Specs 034 to 040, ADR-0020); hosted, provider, remote and live readiness stayed deferred. Replaced by AD-0006. | `docs/98.archive/superseded/02.architecture/descriptions/0009-document-lifecycle-evidence-operating-model.md` |
| AD-0011 | superseded architecture | Document Taxonomy Consolidation Architecture: one repository-local control plane for SDLC documents, profiles, agent governance and validation, organizing change evidence around a Stage 03 work unit and retiring the separate Stage 04 tree (implements REQ-0008). Replaced by AD-0006. | `docs/98.archive/superseded/02.architecture/descriptions/0011-document-taxonomy-consolidation-architecture.md` |
| MIG-0001 | migration ledger | Rehomed 93 Stage 98 records to stable paths during the SDLC taxonomy convergence (93-to-93, no content change). Current structure is owned by the SDLC flow and AD-0006. | `docs/98.archive/migrations/0001-sdlc-taxonomy-convergence.md` |
| MIG-0002 | migration ledger | Bound the WP-002 cutover: 141 document moves from three-digit to four-digit numbering, three Stage 04 index replacements and ten Stage 00/99 owner merges. Current owners are the SDLC flow and Stage 00/99. | `docs/98.archive/migrations/0002-sdlc-document-and-governance-consolidation.md` |
| MIG-0003 | migration ledger | Merged three legacy reference owners into the canonical Stage 00 agent-governance control plane (WORK-054-003). Current owner is Stage 00 under AD-0006. | `docs/98.archive/migrations/0003-agent-governance-control-plane-consolidation.md` |
| MIG-0004 | migration ledger | Sealed the WP-004B cutover of Requirement Package, prefix-free Architecture Description and Spec-package Task authority, plus the WP-004C Stage 99 authority/form cutover (33 deleted or moved objects). Current owners are Stage 01, Stage 02, Stage 03 and Stage 99. | `docs/98.archive/migrations/0004-document-authority-convergence.md` |
| MIG-0005 | migration ledger | Recorded the reviewed authority removals of Spec 0054 WP-003A for Codex and Claude governance; changed prose and projections were merged, not identical moves. Current owner is the agent registry and provider notes. | `docs/98.archive/migrations/0005-codex-claude-agent-governance-convergence.md` |
| MIG-0006 | migration ledger | Retired three Stage 99 templates (`content/audit`, `content/research`, `content/data`) whose profiles required a `YYYY-<letter>` directory and so never routed a real Stage 90 document; the 43 existing documents were unaffected. Current owner is Stage 99. | `docs/98.archive/migrations/0006-unroutable-reference-profile-retirement.md` |
| MIG-0007 | migration ledger | Retired `docs/00.agent-governance/memory/progress.md` (Spec 0054 WP-012) because it contradicted its own README; progress evidence lives in the Task. Current owner is the work lifecycle. | `docs/98.archive/migrations/0007-agent-progress-ledger-retirement.md` |
| MIG-0008 | migration ledger | Retired the `progress.template.md` append form (Spec 0054 WP-012, Spec 0065) after MIG-0007 retired the ledger it appended to. Current owner is the work lifecycle. | `docs/98.archive/migrations/0008-progress-append-form-retirement.md` |
| MIG-0009 | migration ledger | Retired the `docs/00.agent-governance/memory/` directory, its README, the memory template and the `governance/memory` profile (Spec 0065). Current owner is the shared workspace memory store in context and memory policy. | `docs/98.archive/migrations/0009-governance-memory-retirement.md` |
| MIG-0010 | migration ledger | Recorded twelve Stage 99 forms renamed or moved when the contract changed to `family/kind` profile identities; nine were replaced with new frontmatter identity. Current owner is Stage 99. | `docs/98.archive/migrations/0010-stage99-form-naming-and-profile-identity-convergence.md` |
| MIG-0011 | migration ledger | Retired 63 Stage 03 package routers because `spec.md`, `plan.md` and `tasks/` already prove their own navigation. Current owner is the Spec package. | `docs/98.archive/migrations/0011-stage03-package-router-retirement.md` |
| MIG-0012 | migration ledger | Renamed three Stage 90 reference forms to the family they serve, dropping the redundant `-reference` suffix. Current owner is Stage 99. | `docs/98.archive/migrations/0012-reference-form-family-naming.md` |
| MIG-0013 | migration ledger | Moved the first completed Stage 03 package into `docs/98.archive/completed/`; the copy re-based its relative links. Superseded by the removal of archive validation (ADR-0053). | `docs/98.archive/migrations/0013-completed-stage03-package-retention.md` |
| MIG-0014 | migration ledger | Retained 19 completed Stage 03 packages (145 documents) under ADR-0032, batch A of three. Superseded by ADR-0053. | `docs/98.archive/migrations/0014-completed-stage03-package-retention-batch-a.md` |
| MIG-0015 | migration ledger | Retained 21 completed Stage 03 packages (142 documents) under ADR-0032, batch B of three. Superseded by ADR-0053. | `docs/98.archive/migrations/0015-completed-stage03-package-retention-batch-b.md` |
| MIG-0016 | migration ledger | Retained 9 completed Stage 03 packages (57 documents) under ADR-0032, batch C of three. Superseded by ADR-0053. | `docs/98.archive/migrations/0016-completed-stage03-package-retention-batch-c.md` |
| MIG-0017 | migration ledger | Relocated the seventeen sealed supersession records MIG-0001 had placed under `tombstones/` into `superseded/`, which matches their `superseded` reason. Superseded by ADR-0053. | `docs/98.archive/migrations/0017-supersession-record-relocation.md` |
| MIG-0018 | migration ledger | Retained Spec 0058 (eight done documents, two cancelled tasks) as a terminal package, applying the ADR-0032 rule that the retention unit is the package. Superseded by ADR-0053. | `docs/98.archive/migrations/0018-terminal-stage03-package-retention.md` |
| MIG-0019 | migration ledger | Recorded the semantic transfer of REQ-0005..0008 and AD-0008..0011 into retained current owners, mirroring source-identical records into the superseded stage. Current owners are REQ-0003/REQ-0004 and AD-0006/AD-0007. | `docs/98.archive/migrations/0019-requirement-and-architecture-authority-transfer.md` |
| MIG-0020 | migration ledger | Recorded the ADR-0034 transfer of the provider-neutral registry and schema from the retired `.agents/` root to the Stage 00 roles owner (semantic replacement). Current owner is the agent registry under `.agents/roles/`. | `docs/98.archive/migrations/0020-stage00-agent-registry-authority-transfer.md` |
| MIG-0021 | migration ledger | Applied ADR-0035 to the former Stage 00 authority sources and closed intermediate endpoints left by earlier transitions; deleted unused forms have no successor. Current owner is common governance under `.agents/governance/`. | `docs/98.archive/migrations/0021-common-agent-authority-routing.md` |
| MIG-0022 | migration ledger | Retained the completed Spec 0052 package (Spec, Plan and seventeen Tasks) at mirrored `completed/` paths under ADR-0032. Superseded by ADR-0053. | `docs/98.archive/migrations/0022-document-taxonomy-package-retention.md` |
| MIG-0023 | migration ledger | Absorbed seven responsibility documents under `.agents/roles/` into the responsibility router, each reduced to a boundary statement and a few contract bullets. Current owner is `.agents/roles/README.md`. | `docs/98.archive/migrations/0023-responsibility-document-router-absorption.md` |
