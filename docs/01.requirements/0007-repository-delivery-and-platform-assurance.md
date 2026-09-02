---
title: 'Repository Delivery and Platform Assurance Requirement Package'
version: "1.0.0"
type: sdlc/requirement
layer: "requirements"
status: active
owner: platform
updated: 2026-09-01
artifact_id: "REQ-0007"
---

# Repository Delivery and Platform Assurance Requirement Package

## Overview

This package defines a bounded, evidence-driven assurance path for GitHub
automation, Kubernetes and GitOps
desired state, infrastructure examples, policy, scripts, tests, secret
boundaries, and Traefik dynamic configuration. It complements rather than
replaces the current local platform baseline owned by REQ-0004, AD-0007,
ADR-0014, and Spec 008.

Current execution follows the active Spec index and the Spec 0054/0066
consolidation boundary. The latest Stage 90 research is supporting evidence,
not a current implementation or version owner. Repository files, the staged
diff, manifests, configuration, and reviewed locks determine current truth.

## Vision

Platform maintainers and AI agents can change repository delivery and desired
state with one traceable route from affected path to owner, validator, CI job,
evidence depth, and rollback unit. A local static PASS remains honest about
what it proves, while unavailable hosted, provider, credential-bearing, and
live evidence stays explicit and owned.

## Problem Statement

Repository delivery assurance spans documents, workflows, validators, examples,
and deployment sources. Those surfaces must keep one owner for routing and
version facts, preserve evidence depth, and avoid promoting reference snapshots
into a parallel control plane. Local evidence still does not imply hosted CI,
provider runtime, or live-cluster evidence.

Leaving those gaps implicit encourages either overclaiming shallow evidence or
duplicating commands and ownership across CI lanes. Uncommitted or recovered
changes require semantic review against current owners rather than wholesale
application or branch-SHA parity.

## Personas

| Persona | Goal | Constraint or authority boundary |
| --- | --- | --- |
| Platform maintainer | Review one coherent repository-delivery verdict before local integration. | May approve protected repository changes, but remote or live mutation remains separate. |
| Infrastructure engineer | Receive deterministic render, schema, policy, and product-semantic feedback. | Cannot treat local static validation as cluster readiness. |
| Quality engineer | Maintain fixtures that reject drift, missing tools, and false PASS results. | Owns tests and delegated Python validators, not infrastructure policy. |
| Security reviewer | Verify least privilege, secret handling, supply-chain identity, and explicit local-only exceptions. | Does not inspect ignored credentials, tokens, kubeconfigs, or secret-bearing logs. |
| AI agent | Select the correct validator and record lane-specific evidence before a logical commit. | Must follow repository authority, approval, and subagent handoff contracts. |

## Key Use Cases

1. A contributor changes a governed path and can resolve the canonical owner,
   affected validators, CI projection, and required evidence without reading
   duplicated workflow path lists.
2. A GitOps or Traefik change receives syntax, render, schema or allowlisted
   CRD, policy, and product-reference results at their actual evidence depth.
3. An AWS Terraform or Azure Bicep example receives provider-native static
   validation without planning, applying, authenticating, or deploying.
4. A reviewer can distinguish repository-static, hosted CI, and remote/live
   observations and see why any `SKIP` or `DEFER` remains open.
5. A resumed or recovered worktree change is accepted only after every adopted
   hunk matches a current owner and passes repository QA.

## Functional Requirements

| Requirement ID | Requirement | Priority | Verification intent |
| --- | --- | --- | --- |
| REQ-0007-FR-0001 | Inventory every in-scope tracked surface and classify it as change, evidence-backed no-change, or bounded DEFER without forcing cosmetic edits. | Must | A reviewed current-surface matrix covers `.github`, `examples`, `gitops`, `infrastructure`, `policy`, `scripts`, `secrets`, `tests`, and `traefik`. |
| REQ-0007-FR-0002 | Reconcile resumed, recovered, or uncommitted changes by semantic owner without branch-HEAD, stash-object, or generated-object identity pins. | Must | The Task records adopted and rejected scope, and no stale generated identity becomes a current authority. |
| REQ-0007-FR-0003 | Keep one machine owner for affected-path routing and add a non-duplicative GitHub label/CODEOWNERS projection contract. | Must | Schema, parity validator, and negative fixtures reject missing, extra, ambiguous, or duplicated routing facts. |
| REQ-0007-FR-0004 | Preserve intentional CI evidence lanes, one aggregate verdict, immutable Action identity, least privilege, and explicit remote observation boundaries. | Must | Workflow topology and routing tests pass without manufacturing a hosted run for an unpushed SHA. |
| REQ-0007-FR-0005 | Record platform evidence depth as syntax, render, schema or policy, product semantic, and live observation rather than one undifferentiated PASS. | Must | All 13 Kustomize roots and every platform validator have an exact tool, result, fallback, lane, and depth record. |
| REQ-0007-FR-0006 | Validate Traefik references, Kubernetes GVK expectations, GitOps structure, policy, Vault/ESO contracts, secret handling, and explicit local-only transport exceptions. | Must | Positive and negative fixtures prove fail-closed reference, policy, secret, and exception behavior. |
| REQ-0007-FR-0007 | Validate executable Terraform and Bicep examples with provider-native static checks without cloud credentials or deployment. | Must | Terraform format/init/validate and Bicep lint/build evidence is recorded with pinned tool identity and no apply/deploy command. |
| REQ-0007-FR-0008 | Add deterministic direct tests for malformed input, missing tools, fallback behavior, unsafe paths, and forbidden actions. | Must | Focused test suites fail on every named negative fixture and distinguish required-tool failure from diagnostic SKIP. |
| REQ-0007-FR-0009 | Preserve secret, ignored-state, remote-action, and live-system approval boundaries throughout implementation. | Must | Diff and review evidence show no ignored secret read, credential change, push, remote mutation, or live mutation. |
| REQ-0007-FR-0010 | Execute as ordered Specs with separate Plans, Tasks, logical commits, independent reviews, rollback units, and final local-only integration. | Must | Each tranche has reciprocal evidence and passes its gate before its successor begins. |
| REQ-0007-FR-0011 | Keep exact infrastructure, workflow, dependency, and cloud-example version constraints with their executable source or reviewed lock; do not require a Stage 90 mirror as an execution input. | Must | Validators read manifests, scripts, workflow configuration, dependency locks, Terraform, and Bicep directly, and reference-only documents are not required for execution. |
| REQ-0007-FR-0012 | Retain `targetRevision: main` only for repository-self-referencing Argo CD sources under the current single-operator continuous-reconciliation model; keep external chart revisions exact and reconsider the branch policy when multi-operator, multi-environment, or history-rewrite workflows are introduced. | Must | Root and platform Application manifests show semantic self-source versus external-source treatment, and ADR-0029 records the reconsideration trigger. |
| REQ-0007-FR-0013 | Keep Pod Security Admission labels aligned with repository-authored and statically verified workloads: use `enforce` only where the repository owns enough workload evidence, retain `audit`/`warn` for chart, injection, or runtime uncertainty, and treat Istio CNI as desired state rather than live proof. | Must | Namespace manifests, the Istio CNI Application, and related ADRs agree without claiming admission or cluster state. |
| REQ-0007-NFR-0001 | Keep image and artifact assurance fail-closed without performing an unverified blanket digest migration. | Should | Current non-`latest` tag-or-digest checks pass and any digest, SBOM, or provenance follow-up names consumers, owner, and trigger. |
| REQ-0007-NFR-0002 | Keep native README/frontmatter forms unchanged unless the selected profile or observed content proves a real contract defect. | Must | Strict registry, Markdown-profile, and link/owner validation passes with no template residue or arbitrary README section. |

## Success / Acceptance Criteria

- **ACC-RDPA-001**: Every in-scope tracked path has one disposition and one
  canonical owner, with zero duplicate current-purpose documents or controls.
- **ACC-RDPA-002**: GitHub routing parity validates against the existing
  affected-surface owner, while local workflows retain one `ci-summary`
  verdict and no proven duplicate job.
- **ACC-RDPA-003**: Thirteen Kustomize roots render with an approved,
  repository-pinned tool identity; built-in resources receive schema evidence
  and allowlisted external CRDs retain explicit schema limitations.
- **ACC-RDPA-004**: Traefik reference, Vault/ESO, policy, secret, GitOps, and
  image contracts pass focused positive and negative tests.
- **ACC-RDPA-005**: Terraform and Bicep examples pass their provider-native
  non-deploy validation lanes in the required CI-equivalent environment.
- **ACC-RDPA-006**: Required repository and CI gates never translate missing
  tooling or failed fallback behavior into PASS.
- **ACC-RDPA-007**: Resumed or recovered changes have a reviewed semantic
  disposition, no generated-current identity pin, and no orphaned worktree
  state after verified local integration.
- **ACC-RDPA-008**: Full repository QA, independent requirements and
  quality/security reviews, local `main` fast-forward integration, and cleanup
  complete without push or remote/live mutation.
- **ACC-RDPA-009**: Remote GitHub metadata records its observation date and
  relevant immutable source identity; current
  hosted CI, provider-runtime, credential-bearing, and live results remain
  `DEFER` unless actually observed within separate authority.
- **ACC-RDPA-010**: Removing a reference inventory does not change the direct
  version constraints or make any required CI, bootstrap, Terraform, Bicep, or
  manifest validation unavailable.
- **ACC-RDPA-011**: Repository-self-referencing Argo CD sources and external
  chart sources retain their distinct revision policies and explicit
  reconsideration triggers.
- **ACC-RDPA-012**: PSA namespace labels and Istio CNI desired state are
  documented without promoting repository-static evidence into a live-cluster
  claim.

## Scope and Non-goals

- **In scope**: `.github/**`, `examples/**`, `gitops/**`,
  `infrastructure/**`, `policy/**`, `scripts/**`, tracked `secrets/**`,
  `tests/**`, `traefik/**`, their canonical documentation contracts, the
  minimum Stage 00 machine routing contracts they consume, and the Stage 01-03
  lineage required to govern the work.
- **Authorized consolidation**: Protected-surface, contract, governance,
  workflow, validator, fixture, and obsolete placeholder changes are allowed
  when evidence identifies a real conflict, duplicate, or gap.
- **Non-goals**: Redefining current local platform topology; replacing
  REQ-0004, AD-0007, ADR-0014, or Spec 008; reading ignored/private state;
  changing credentials; pushing;
  changing branch protection or rulesets; dispatching remote workflows;
  applying manifests; deploying cloud resources; or mutating Kubernetes,
  Argo CD, Vault, ESO, DNS, or TLS state.

## Risks, Dependencies, and Assumptions

- Stage 90 research is descriptive evidence, not a current policy, version, or
  implementation owner; every local claim must be re-observed against current
  repository sources.
- Historical remote results cannot establish the result of current local
  changes, regardless of branch ancestry.
- The repository currently lacks local Terraform, Bicep, kubeconform, conftest,
  and Traefik CLIs. Required CI-equivalent validation therefore needs
  checksum-verified ephemeral tooling or must fail; developer-only diagnostics
  may report a bounded SKIP.
- Requiring one CODEOWNER approval while only one eligible collaborator exists
  can deadlock changes. Remote enforcement remains a policy follow-up until a
  second eligible reviewer exists.
- Kubernetes, Terraform, Bicep, GitHub Actions, Vault, ESO, and Traefik
  behavior is grounded in their official documentation; exact tool versions
  remain with executable configuration or reviewed dependency locks rather
  than a Stage 90 inventory.
- Logical commits and semantic worktree review make rollback possible without
  preserving a stash or branch SHA as a permanent policy input.

## Traceability

### Lifecycle Traceability

| Requirement ID | Acceptance criterion | Downstream owner |
| --- | --- | --- |
| REQ-0007-FR-0001 | ACC-RDPA-001 | [AD-0010](../02.architecture/descriptions/0010-repository-delivery-evidence-architecture.md) and [Spec 047](../03.specs/0047-current-surface-and-stash-reconciliation/spec.md) own architecture and first-tranche disposition evidence. |
| REQ-0007-FR-0002 | ACC-RDPA-007 | N/A — Spec 047 shares the downstream owner linked in REQ-0007-FR-0001. |
| REQ-0007-FR-0003 | ACC-RDPA-002 | [Spec 048](../03.specs/0048-github-routing-and-ci-evidence/spec.md) owns GitHub projection and CI evidence. |
| REQ-0007-FR-0004 | ACC-RDPA-002 | N/A — Spec 048 shares the downstream owner stated in REQ-0007-FR-0003. |
| REQ-0007-FR-0005 | ACC-RDPA-003 | [Spec 049](../03.specs/0049-platform-validation-and-security-evidence/spec.md) owns layered platform evidence. |
| REQ-0007-FR-0006 | ACC-RDPA-004 | N/A — Spec 049 shares the downstream owner stated in REQ-0007-FR-0005. |
| REQ-0007-FR-0007 | ACC-RDPA-005 | [Spec 050](../03.specs/0050-example-iac-and-validator-qa/spec.md) owns provider-native example validation. |
| REQ-0007-FR-0008 | ACC-RDPA-006 | N/A — Specs 049 and 050 share the downstream owners linked in REQ-0007-FR-0005 and REQ-0007-FR-0007. |
| REQ-0007-FR-0009 | ACC-RDPA-009 | N/A — Specs 047 through 051 share this approval boundary through the linked tranche owners. |
| REQ-0007-FR-0010 | ACC-RDPA-008 | [Spec 051](../03.specs/0051-repository-assurance-integration-and-closure/spec.md) owns terminal integration and closure. |
| REQ-0007-FR-0011 | ACC-RDPA-010 | [AD-0010](../02.architecture/descriptions/0010-repository-delivery-evidence-architecture.md) owns direct executable-source evidence. |
| REQ-0007-FR-0012 | ACC-RDPA-011 | [AD-0010](../02.architecture/descriptions/0010-repository-delivery-evidence-architecture.md) owns the current delivery-evidence architecture and routes the `ADR-0029` decision. |
| REQ-0007-FR-0013 | ACC-RDPA-012 | [AD-0010](../02.architecture/descriptions/0010-repository-delivery-evidence-architecture.md) owns the namespace evidence architecture and routes the `ADR-0028` decision. |
| REQ-0007-NFR-0001 | ACC-RDPA-004 | N/A — Spec 049 shares the downstream owner stated in REQ-0007-FR-0005. |
| REQ-0007-NFR-0002 | ACC-RDPA-001 | N/A — Specs 047 and 051 share the downstream owners linked in REQ-0007-FR-0001 and REQ-0007-FR-0010. |
