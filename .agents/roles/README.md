---
title: "Agent Responsibilities"
version: "1.0.0"
type: "common/readme-collection-index"
status: "active"
owner: "platform"
updated: "2026-09-07"
---
# Agent Responsibilities

## Overview

Select the responsibility needed for the task, then resolve the concrete role
and provider projection from the [agent registry](registry.json).
This router is not a duplicate roster or permission inventory.

## Scope

Responsibility explains the domain boundary; registry permission and explicit
task ownership determine permitted actions. A review lens is not write access.

The seven boundaries below are sections of this router rather than separate
documents. A concrete role body keeps its own guardrails, inputs, outputs and
handoffs; this page keeps only the domain boundary each role reads for context.

### Architecture

Keep system structure and important decisions consistent with durable
requirements and change-specific contracts. Architecture Descriptions and ADRs
own structural views and durable choices; a Spec owns change-specific behavior.
This boundary owns neither infrastructure manifests nor common governance
policy.

- Trace structural changes to complete Requirement Package IDs and affected
  Specs.
- Use a successor ADR for a changed accepted decision; retain superseded ADRs in
  the decision log.
- Hand implementation, operational, and security consequences to their
  responsible owners. Do not claim ownership of all documentation.

This boundary is carried by [architect](architect.md).

### Documentation

Keep authored documents and navigation useful, traceable, and correctly routed.
This boundary covers shared authoring and navigation concerns and assigned
document edits, not authority over every stage's content. Stage owners retain
substantive decisions and Stage 99 owns exact forms. Git history is the
full-content archive; Stage 98 is a minimal recovery index.

- Apply the selected profile and template and the document language boundary.
- Keep current links and README navigation aligned with moves and deletions.
- Hand domain claims to their owner and research gaps to evidence collection; do
  not manufacture source support.
- Preserve completed or sealed evidence; use approved migration recovery instead
  of rewriting history.

### Infrastructure

Keep Kubernetes and GitOps desired state reproducible, isolated, and aligned
with approved system contracts. Scoped implementation may cover assigned
infrastructure or GitOps manifests and their automation; review roles remain
read-only. This boundary grants no live mutation and owns neither upstream
requirements nor governance. Local cluster assets sit under `infrastructure/`
and reconciliation begins at `gitops/clusters/local/root-application.yaml`.

- Preserve secure secret-reference handling and network isolation.
- Validate affected manifest syntax, policy, and reconciliation structure using
  repository checks.
- Record operational effects and rollback in the owning Plan or Task and hand
  runbook changes to operations.
- Keep cluster bring-up and reconciliation operator-bound under explicit
  approval.

### Operations

Preserve safe operating procedures, recoverability, incident evidence, and
escalation. This boundary owns assigned operating policies, runbooks, and
incident knowledge. It grants no change to GitOps desired state or live
services; those need the relevant owner and approval. Guides explain use,
policies define operating controls, runbooks provide ordered procedures, and
incident records preserve facts and learning. Do not create a separate
release-record family.

- Trace proposed operational actions to policy, a Spec, or incident context.
- State prerequisites, impact, verification, rollback or recovery, and the
  responsible operator.
- Separate authorized observations from suggested checks and unexecuted actions.
- Turn durable corrective actions into owned requirements, decisions, Specs, or
  operating updates.

### Quality

Map acceptance to reproducible checks and report failures, limitations, and
regression risk. Registry permissions and the delegated scope bound QA writes:
QA may author assigned tests, fixtures, Python validators, or validation-lane
content, and gains no product, manifest, security-signoff, shell-validator, or
policy ownership. CI triggers, permissions, concurrency, and non-lane jobs
remain governance-owned.

- Derive positive and independent negative cases from semantic rule families.
- Prefer bounded mutation tests over copied exhaustive fixture matrices.
- Keep expected and observed results traceable to acceptance IDs, and preserve
  independent implementation review.
- Hand documentation, security, and unowned implementation changes to their
  owners; use quality policy for lane and result meanings.

### Security

Review secret exposure, access control, isolation, and unsafe execution against
the approved contract. Security review is read-only when the selected registry
role is read-only. A finding authorizes no repair, live investigation, secret
access, or broader file ownership. Use repository policy, manifest references,
Specs, and approved redacted incident evidence; do not inspect credentials or
secret values to establish a finding.

- Trace security-impacting findings to evidence and a specific failure or risk.
- Review privilege escalation, network isolation, untrusted input, command
  boundaries, and data retention.
- Hand fixes to the authorized implementation owner and record unresolved risk
  or required operator action.
- Connect recurring incident lessons to durable controls without rewriting
  historical facts.

### Supervision

Coordinate authorized work and reconcile ownership, dependencies, review, and
evidence. The supervisor's registry permission class is orchestration, not
authoring; governance maintenance requires an explicitly scoped authoring owner
and routing grants a worker no new tools or write paths. Common governance owns
human policy, the neutral registry owns the roster and handoffs, and provider
projections own native configuration.

- Decompose work into bounded tasks with explicit file responsibility and
  dependencies.
- Select existing registry roles and skills; do not expand the roster for
  speculative gaps.
- Preserve independent review and route disagreements or approval needs to the
  human.
- Reconcile each returned result with acceptance and current repository evidence
  before final handoff.

## Item Index

Canonical role bodies:

- [supervisor](supervisor.md)
- [architect](architect.md)
- [governance-steward](governance-steward.md)
- [ci-workflow-engineer](ci-workflow-engineer.md)
- [code-reviewer](code-reviewer.md)
- [doc-writer](doc-writer.md)
- [gitops-reviewer](gitops-reviewer.md)
- [incident-responder](incident-responder.md)
- [k8s-implementer](k8s-implementer.md)
- [network-reviewer](network-reviewer.md)
- [observability-reviewer](observability-reviewer.md)
- [security-auditor](security-auditor.md)
- [wiki-curator](wiki-curator.md)
- [docs-researcher](docs-researcher.md)
- [quality-engineer](quality-engineer.md)

## Add and Find

Load only the relevant responsibility owners. Product intent belongs in the
Requirement Package; backend and API behavior belong in the Spec and its
implementation task. These general duties do not need unused standalone agent
scopes in this infrastructure workspace.

Add a role or skill only for an approved concrete gap, through the neutral
registry and reviewed projections. Declare ownership transitions when a task
crosses domains; escalate unclear or conflicting boundaries.

Record evidence and handoff through [quality policy](../governance/quality.md).
Reassess the responsibility when the active Task changes scope; exact role,
permission, skill, and handoff membership stays in the agent registry.

## Related Documents

- [Governance Hub](../README.md)
- [SDLC Flow](../governance/sdlc.md)
- [Delegated Development](../workflows/delegated-development.md)
- [Approval and Safety](../governance/approval-and-safety.md)
- [Document Authoring](../governance/document-authoring.md)
- Architecture Index (`docs/02.architecture/README.md`)
- Operations Index (`docs/05.operations/README.md`)
