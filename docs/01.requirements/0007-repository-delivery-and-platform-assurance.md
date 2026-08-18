---
title: 'Repository Delivery and Platform Assurance Product Requirements'
type: sdlc/prd
status: active
owner: platform
updated: 2026-08-07
artifact_id: "PRD-0007"
---

# Repository Delivery and Platform Assurance Product Requirements

## Overview

This program turns the repository's current audit findings into a bounded,
evidence-driven assurance path for GitHub automation, Kubernetes and GitOps
desired state, infrastructure examples, policy, scripts, tests, secret
boundaries, and Traefik dynamic configuration. It complements rather than
replaces the current local platform baseline owned by PRD-0004, AD-0007,
ADR-0014, and Spec 008.

PRD-0007 remains active and governing. Its execution is paused as of 2026-08-07
for the duration of the PRD-0008 document taxonomy consolidation program, because
Specs 049 and 050 would author validators against a surface that program
consolidates. Spec 047 returns to draft and Specs 048-051 remain planned draft
successors. Execution resumes in the consolidated structure when Spec 052
reaches `done`.

The program starts from the clean local `main` baseline observed on
2026-08-02. It preserves the Current audit pack as observation evidence, uses
read-only GitHub metadata as a separate remote lane, and reconciles the one
saved stash by semantic hunk disposition instead of wholesale application.

## Vision

Platform maintainers and AI agents can change repository delivery and desired
state with one traceable route from affected path to owner, validator, CI job,
evidence depth, and rollback unit. A local static PASS remains honest about
what it proves, while unavailable hosted, provider, credential-bearing, and
live evidence stays explicit and owned.

## Problem Statement

The repository already has strong document, workflow, secret, GitOps, and
agent-governance controls, but the remaining assurance gaps are distributed
across prose, workflows, validators, examples, and dated audit observations.
GitHub label and ownership projections can drift from the machine path
registry; current local CI changes do not have hosted evidence; Kubernetes
syntax checks do not establish render or schema validity; Traefik references
lack a product-semantic gate; Terraform and Bicep examples lack native
validation; and shell validators need direct negative and fallback tests.

Leaving those gaps implicit encourages either overclaiming shallow evidence or
duplicating commands and ownership across CI lanes. Applying the saved stash
wholesale would also reintroduce stale agent-governance and generated-object
state that current `main` has already superseded.

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
5. The saved stash is retired only after every hunk has a durable disposition
   and every adopted result passes review and repository QA.

## Functional Requirements

| Requirement ID | Requirement | Priority | Verification intent |
| --- | --- | --- | --- |
| REQ-RDPA-001 | Inventory every in-scope tracked surface and classify it as change, evidence-backed no-change, or bounded DEFER without forcing cosmetic edits. | Must | A reviewed current-surface matrix covers `.github`, `examples`, `gitops`, `infrastructure`, `policy`, `scripts`, `secrets`, `tests`, and `traefik`. |
| REQ-RDPA-002 | Reconcile saved stash object `6370311e...` by hunk disposition and regenerate derived object identities from current HEAD. | Must | The Task records every disposition, no stale generated object ID is copied, and the matching stash is dropped only after verified local integration. |
| REQ-RDPA-003 | Keep one machine owner for affected-path routing and add a non-duplicative GitHub label/CODEOWNERS projection contract. | Must | Schema, parity validator, and negative fixtures reject missing, extra, ambiguous, or duplicated routing facts. |
| REQ-RDPA-004 | Preserve intentional CI evidence lanes, one aggregate verdict, immutable Action identity, least privilege, and explicit remote observation boundaries. | Must | Workflow topology and routing tests pass without manufacturing a hosted run for an unpushed SHA. |
| REQ-RDPA-005 | Record platform evidence depth as syntax, render, schema or policy, product semantic, and live observation rather than one undifferentiated PASS. | Must | All 13 Kustomize roots and every platform validator have an exact tool, result, fallback, lane, and depth record. |
| REQ-RDPA-006 | Validate Traefik references, Kubernetes GVK expectations, GitOps structure, policy, Vault/ESO contracts, secret handling, and explicit local-only transport exceptions. | Must | Positive and negative fixtures prove fail-closed reference, policy, secret, and exception behavior. |
| REQ-RDPA-007 | Add provider-native Terraform and Bicep static validation for executable examples without cloud credentials or deployment. | Must | Terraform format/init/validate and Bicep lint/build evidence is recorded with pinned tool identity and no apply/deploy command. |
| REQ-RDPA-008 | Add deterministic direct tests for malformed input, missing tools, fallback behavior, unsafe paths, and forbidden actions. | Must | Focused test suites fail on every named negative fixture and distinguish required-tool failure from diagnostic SKIP. |
| REQ-RDPA-009 | Preserve secret, ignored-state, remote-action, and live-system approval boundaries throughout implementation. | Must | Diff and review evidence show no ignored secret read, credential change, push, remote mutation, or live mutation. |
| REQ-RDPA-010 | Execute as ordered Specs with separate Plans, Tasks, logical commits, independent reviews, rollback units, and final local-only integration. | Must | Each tranche has reciprocal evidence and passes its gate before its successor begins. |
| REQ-RDPA-011 | Keep image and artifact assurance fail-closed without performing an unverified blanket digest migration. | Should | Current non-`latest` tag-or-digest checks pass and any digest, SBOM, or provenance follow-up names consumers, owner, and trigger. |
| REQ-RDPA-012 | Keep native README/frontmatter forms unchanged unless the selected profile or observed content proves a real contract defect. | Must | Strict registry, Markdown-profile, and link/owner validation passes with no template residue or arbitrary README section. |

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
- **ACC-RDPA-007**: The saved stash has a complete semantic disposition,
  current generated identities, and no remaining matching stash after verified
  local integration.
- **ACC-RDPA-008**: Full repository QA, independent requirements and
  quality/security reviews, local `main` fast-forward integration, and cleanup
  complete without push or remote/live mutation.
- **ACC-RDPA-009**: Remote GitHub metadata is dated and SHA-bound; current
  hosted CI, provider-runtime, credential-bearing, and live results remain
  `DEFER` unless actually observed within separate authority.

## Scope and Non-goals

- **In scope**: `.github/**`, `examples/**`, `gitops/**`,
  `infrastructure/**`, `policy/**`, `scripts/**`, tracked `secrets/**`,
  `tests/**`, `traefik/**`, their canonical documentation contracts, the
  minimum Stage 00 machine routing contracts they consume, and the Stage 01-04
  lineage required to govern the work.
- **Authorized consolidation**: Protected-surface, contract, governance,
  workflow, validator, fixture, and obsolete placeholder changes are allowed
  when evidence identifies a real conflict, duplicate, or gap.
- **Non-goals**: Redefining current local platform topology; replacing
  PRD-0004, AD-0007, ADR-0014, or Spec 008; rewriting completed Specs or dated
  audits; reading ignored/private state; changing credentials; pushing;
  changing branch protection or rulesets; dispatching remote workflows;
  applying manifests; deploying cloud resources; or mutating Kubernetes,
  Argo CD, Vault, ESO, DNS, or TLS state.

## Risks, Dependencies, and Assumptions

- The Current audit pack is descriptive evidence pinned to an older SHA, not a
  current policy owner; every finding must be re-observed before a change.
- Local `main` is ahead of the observed remote SHA, so a historical remote
  failure cannot establish the result of current local changes.
- The repository currently lacks local Terraform, Bicep, kubeconform, conftest,
  and Traefik CLIs. Required CI-equivalent validation therefore needs
  checksum-verified ephemeral tooling or must fail; developer-only diagnostics
  may report a bounded SKIP.
- Requiring one CODEOWNER approval while only one eligible collaborator exists
  can deadlock changes. Remote enforcement remains a policy follow-up until a
  second eligible reviewer exists.
- Kubernetes, Terraform, Bicep, GitHub Actions, Vault, ESO, and Traefik
  behavior is grounded in their official documentation; exact tool versions
  remain pinned in the existing technology inventory rather than floated as
  `latest`.
- Logical commits and semantic stash reconciliation make rollback possible,
  but the stash must remain present until the integrated result is independently
  reviewed and revalidated.

## Traceability

### Lifecycle Traceability

| Requirement ID | Acceptance criterion | Downstream owner |
| --- | --- | --- |
| REQ-RDPA-001 | ACC-RDPA-001 | [AD-0010](../02.architecture/descriptions/ad-0010-repository-delivery-evidence-architecture.md) and [Spec 047](../03.specs/0047-current-surface-and-stash-reconciliation/spec.md) own architecture and first-tranche disposition evidence. |
| REQ-RDPA-002 | ACC-RDPA-007 | N/A — Spec 047 shares the downstream owner linked in REQ-RDPA-001. |
| REQ-RDPA-003 | ACC-RDPA-002 | [Spec 048](../03.specs/0048-github-routing-and-ci-evidence/spec.md) owns GitHub projection and CI evidence. |
| REQ-RDPA-004 | ACC-RDPA-002 | N/A — Spec 048 shares the downstream owner stated in REQ-RDPA-003. |
| REQ-RDPA-005 | ACC-RDPA-003 | [Spec 049](../03.specs/0049-platform-validation-and-security-evidence/spec.md) owns layered platform evidence. |
| REQ-RDPA-006 | ACC-RDPA-004 | N/A — Spec 049 shares the downstream owner stated in REQ-RDPA-005. |
| REQ-RDPA-007 | ACC-RDPA-005 | [Spec 050](../03.specs/0050-example-iac-and-validator-qa/spec.md) owns provider-native example validation. |
| REQ-RDPA-008 | ACC-RDPA-006 | N/A — Specs 049 and 050 share the downstream owners linked in REQ-RDPA-005 and REQ-RDPA-007. |
| REQ-RDPA-009 | ACC-RDPA-009 | N/A — Specs 047 through 051 share this approval boundary through the linked tranche owners. |
| REQ-RDPA-010 | ACC-RDPA-008 | [Spec 051](../03.specs/0051-repository-assurance-integration-and-closure/spec.md) owns terminal integration and closure. |
| REQ-RDPA-011 | ACC-RDPA-004 | N/A — Spec 049 shares the downstream owner stated in REQ-RDPA-005. |
| REQ-RDPA-012 | ACC-RDPA-001 | N/A — Specs 047 and 051 share the downstream owners linked in REQ-RDPA-001 and REQ-RDPA-010. |
