---
title: "Local GitOps Platform and Delivery Assurance Requirements"
version: "1.0.4"
type: "sdlc/requirement"
status: "active"
owner: "platform"
updated: "2026-09-26"
layer: "requirements"
artifact_id: "REQ-0004"
---

# Local GitOps Platform and Delivery Assurance Requirements

## Overview

This document owns the user value, operating boundaries, and delivery assurance requirements of the local GitOps platform.
[AD-0007](../02.architecture/descriptions/0007-current-local-gitops-platform.md) owns the concrete topology and implementation choices,
and [REQ-0003](./0003-workspace-agent-governance-platform.md) owns the common governance, validation, and approval requirements.

## Vision

Users must be able to reproduce the local platform and change it safely from the repository's desired state and from evidence whose depth is kept distinct.

## Problem Statement

Confusing the current desired state, historical documents, and actual runtime state can present a removed feature or an unverified
security level as supported. The existence of static configuration must be kept apart from reconciliation or external service availability.

## Personas

- Platform engineer: manages the platform ownership boundaries and external service interfaces.
- Operator: operates through the current UIs, GitOps state, and bounded observed evidence.
- Application author: follows the validation and onboarding boundaries of workloads and cloud examples.

## Key Use Cases

- A changer finds each surface's semantic owner and the static validation it needs.
- An operator confirms the platform/workload boundary and external service dependencies.
- A reviewer judges failure, fallback, DEFER, and live-unobserved states separately.
- An executor resumes an unfinished assurance package within its prerequisite validation and approval scope.

## Functional Requirements

- **REQ-0004-FR-0001**: The local platform's desired state must be declared reproducibly in the repository, with its ownership boundaries kept distinct.
- **REQ-0004-FR-0002**: The reconciliation, ownership, and permission boundaries of platform components and user workloads must be separated.
- **REQ-0004-FR-0003**: Connections to external secret, data, and observability services must be expressed as explicit service interfaces and kept distinct from creating the external runtime.
- **REQ-0004-FR-0004**: Operators must be able to reach the currently supported cluster UIs, and a removed UI must not be presented as the current implementation.
- **REQ-0004-FR-0005**: Each tracked surface in a change's scope must be classified as changed, unchanged with a reason, or DEFER with an owner and a retry condition.
- **REQ-0004-FR-0006**: Resumed, recovered, and uncommitted changes must be adopted or excluded according to their semantic owner, and a temporary branch, stash, or generated identity must not be fixed as current authority.
- **REQ-0004-FR-0007**: GitHub's label and code ownership projections must match the single affected-path owner, and missing, duplicate, or ambiguous routing must be validated.
- **REQ-0004-FR-0008**: Platform validation results must distinguish the depth (syntax, render, schema/policy, product semantic, and live observation) and the tool, fallback, lane, and result.
- **REQ-0004-FR-0009**: An executable cloud example must carry guidance beside the example and provider-native static validation, and must be verifiable without credentials or apply/deploy.
- **REQ-0004-FR-0010**: Ingress references, resource kinds, GitOps structure, policy, secret sync, and explicit local-only transport exceptions must be checked fail-closed.
- **REQ-0004-FR-0011**: Platform assurance work must proceed in ordered per-package review, validation, and rollback units and must prove the final local-only integration.
- **REQ-0004-FR-0012**: Exact infrastructure, workflow, dependency, and example versions must be confirmed from the executable source or a reviewed lock, and a Reference mirror must not be required as an execution precondition.
- **REQ-0004-FR-0013**: The revision policy of the repository's own continuously reconciled source must be kept distinct from that of external release sources, and revisited when multiple operators or environments, or history rewriting, are introduced.
- **REQ-0004-FR-0014**: The Pod security enforcement level must be proportional to the workload evidence the repository owns and validates statically. Chart, injection, and runtime uncertainty is separated as audit/warn, and CNI desired state is not promoted to live evidence.
- **REQ-0004-NFR-0001**: The local platform must provide the current integration scope of certificates, ingress, service mesh, observability UIs, progressive delivery, notifications, monitoring, and external secret integration.
- **REQ-0004-NFR-0002**: Secret values, tokens, and private keys must not be recorded in Git, documents, or logs.
- **REQ-0004-NFR-0003**: Image and artifact assurance must stay fail-closed without an unvalidated blanket digest conversion, and follow-on provenance obligations must be stated with a consumer, owner, and trigger.
- **REQ-0004-IF-0001**: Historical records must be kept apart from current execution authority. An explicit historical citation of a completed package is allowed, but a sealed record is not used as current implementation guidance.

## Success / Acceptance Criteria

The current desired-state structure, Kubernetes syntax, and product static contract must pass their validators.
Delivery assurance must leave a classification, validation depth, result, and limits for every in-scope surface,
and does not substitute a static PASS for unobserved remote or runtime state. The per-member verdicts in the trace below link to the AD and its Spec.

- **Acceptance criterion 01**: Validate the current platform product static contract.
- **Acceptance criterion 02**: Validate the GitOps ownership and reconciliation boundaries of root, platform, and workload.
- **Acceptance criterion 03**: Validate the syntax of tracked Kubernetes manifests.
- **Acceptance criterion 04**: Validate the authority separation between current documents and the historical Archive, and the related repository gates.

## Scope and Non-goals

In scope: the current local platform, the platform/workload separation, external service connections, onboarding examples, and local-only assurance.
Out of scope: creating the external runtime, cloud provisioning, unapproved cluster changes, and an unvalidated blanket digest conversion.

## Risks, Dependencies, and Assumptions

External services and actual cluster availability need separate preparation and observation. Updating this document is not live validation or deployment.
Reading secrets, pushing, cloud work, and live mutation each need separate approval.

### Unfinished delivery assurance

Spec 0049 depended on the retired Spec 0048 and the Traefik lane and was withdrawn on 2026-09-25 ([SPEC-0089](../03.specs/0089-deferred-conflict-resolution/spec.md)); it is kept in `98.archive/retired/` and not cited ([SPEC-0090](../03.specs/0090-spec0049-retirement/spec.md)). Its unimplemented scope (render, schema, policy, secret, shell fixture, image, and tool evidence lanes) remains an ownerless gap of REQ-0004-FR-0008 and FR-0010; the next owner is the request owner who plans a new package under current authority.
Specs 0047, 0048, 0050, and 0051 were withdrawn without successors and kept in `98.archive/retired/`
([SPEC-0087](../03.specs/0087-stage03-terminal-package-retention/spec.md)); their scope currently has no implementation owner.
The original REQ-0007 program history is kept; its current platform meaning passes to this document and its common routing, approval, and QA meaning to REQ-0003.
This succession does not declare any tranche, or Spec 0054 WP-013, complete.
[SPEC-0088](../03.specs/0088-operations-corpus-convergence/spec.md) owns aligning operations documents with current implementation facts
and validating the boundary that secret values are never printed.
[SPEC-0089](../03.specs/0089-deferred-conflict-resolution/spec.md) owns confirming the cluster UI chart objects
that RUN-0004 points to.

## Traceability

### Lifecycle Traceability

| Requirement ID | Acceptance criterion | Downstream owner |
| --- | --- | --- |
| REQ-0004-FR-0001 | The local platform's desired state must be declared reproducibly in the repository, with its ownership boundaries kept distinct. Whether it is met is judged by the owner's static validation and separate observed evidence. | [AD-0007](../02.architecture/descriptions/0007-current-local-gitops-platform.md) |
| REQ-0004-FR-0002 | The reconciliation, ownership, and permission boundaries of platform components and user workloads must be separated. Whether it is met is judged by the owner's static validation and separate observed evidence. | [AD-0007](../02.architecture/descriptions/0007-current-local-gitops-platform.md) |
| REQ-0004-FR-0003 | Connections to external secret, data, and observability services must be expressed as explicit service interfaces and kept distinct from creating the external runtime. Whether it is met is judged by the owner's static validation and separate observed evidence. | [AD-0007](../02.architecture/descriptions/0007-current-local-gitops-platform.md) |
| REQ-0004-FR-0004 | Operators must be able to reach the currently supported cluster UIs, and a removed UI must not be presented as the current implementation. Whether it is met is judged by the owner's static validation and separate observed evidence. | [AD-0007](../02.architecture/descriptions/0007-current-local-gitops-platform.md) |
| REQ-0004-FR-0005 | Each tracked surface in a change's scope must be classified as changed, unchanged with a reason, or DEFER with an owner and a retry condition. Whether it is met is judged by the owner's static validation and separate observed evidence. | [AD-0007](../02.architecture/descriptions/0007-current-local-gitops-platform.md) |
| REQ-0004-FR-0006 | Resumed, recovered, and uncommitted changes must be adopted or excluded according to their semantic owner, and a temporary branch, stash, or generated identity must not be fixed as current authority. Whether it is met is judged by the owner's static validation and separate observed evidence. | [AD-0007](../02.architecture/descriptions/0007-current-local-gitops-platform.md) |
| REQ-0004-FR-0007 | GitHub's label and code ownership projections must match the single affected-path owner, and missing, duplicate, or ambiguous routing must be validated. Whether it is met is judged by the owner's static validation and separate observed evidence. | [AD-0007](../02.architecture/descriptions/0007-current-local-gitops-platform.md) |
| REQ-0004-FR-0008 | Platform validation results must distinguish the depth (syntax, render, schema/policy, product semantic, and live observation) and the tool, fallback, lane, and result. Whether it is met is judged by the owner's static validation and separate observed evidence. | [AD-0007](../02.architecture/descriptions/0007-current-local-gitops-platform.md) |
| REQ-0004-FR-0009 | An executable cloud example must carry guidance beside the example and provider-native static validation, and must be verifiable without credentials or apply/deploy. Whether it is met is judged by the owner's static validation and separate observed evidence. | [AD-0007](../02.architecture/descriptions/0007-current-local-gitops-platform.md) |
| REQ-0004-FR-0010 | Ingress references, resource kinds, GitOps structure, policy, secret sync, and explicit local-only transport exceptions must be checked fail-closed. Whether it is met is judged by the owner's static validation and separate observed evidence. | [AD-0007](../02.architecture/descriptions/0007-current-local-gitops-platform.md) |
| REQ-0004-FR-0011 | Platform assurance work must proceed in ordered per-package review, validation, and rollback units and must prove the final local-only integration. Whether it is met is judged by the owner's static validation and separate observed evidence. | [AD-0007](../02.architecture/descriptions/0007-current-local-gitops-platform.md) |
| REQ-0004-FR-0012 | Exact infrastructure, workflow, dependency, and example versions must be confirmed from the executable source or a reviewed lock, and a Reference mirror must not be required as an execution precondition. Whether it is met is judged by the owner's static validation and separate observed evidence. | [AD-0007](../02.architecture/descriptions/0007-current-local-gitops-platform.md) |
| REQ-0004-FR-0013 | The revision policy of the repository's own continuously reconciled source must be kept distinct from that of external release sources, and revisited when multiple operators or environments, or history rewriting, are introduced. Whether it is met is judged by the owner's static validation and separate observed evidence. | [AD-0007](../02.architecture/descriptions/0007-current-local-gitops-platform.md) |
| REQ-0004-FR-0014 | The Pod security enforcement level must be proportional to the workload evidence the repository owns and validates statically. Chart, injection, and runtime uncertainty is separated as audit/warn, and CNI desired state is not promoted to live evidence. Whether it is met is judged by the owner's static validation and separate observed evidence. | [AD-0007](../02.architecture/descriptions/0007-current-local-gitops-platform.md) |
| REQ-0004-NFR-0001 | The local platform must provide the current integration scope of certificates, ingress, service mesh, observability UIs, progressive delivery, notifications, monitoring, and external secret integration. Whether it is met is judged by the owner's static validation and separate observed evidence. | [AD-0007](../02.architecture/descriptions/0007-current-local-gitops-platform.md) |
| REQ-0004-NFR-0002 | Secret values, tokens, and private keys must not be recorded in Git, documents, or logs. Whether it is met is judged by the owner's static validation and separate observed evidence. | [AD-0007](../02.architecture/descriptions/0007-current-local-gitops-platform.md) |
| REQ-0004-NFR-0003 | Image and artifact assurance must stay fail-closed without an unvalidated blanket digest conversion, and follow-on provenance obligations must be stated with a consumer, owner, and trigger. Whether it is met is judged by the owner's static validation and separate observed evidence. | [AD-0007](../02.architecture/descriptions/0007-current-local-gitops-platform.md) |
| REQ-0004-IF-0001 | Historical records must be kept apart from current execution authority. An explicit historical citation of a completed package is allowed, but a sealed record is not used as current implementation guidance. Whether it is met is judged by the owner's static validation and separate observed evidence. | [AD-0007](../02.architecture/descriptions/0007-current-local-gitops-platform.md) |

### Reviewed member-ID transfer

The table below records the succession of current meaning. Earlier member IDs are historical identifiers of the original decisions and program and are not reassigned.

| Original member ID | Current semantic owner |
| --- | --- |
| REQ-0007-FR-0001 | REQ-0004-FR-0005 |
| REQ-0007-FR-0002 | REQ-0004-FR-0006 |
| REQ-0007-FR-0003 | REQ-0004-FR-0007 / REQ-0003-FR-0016 |
| REQ-0007-FR-0004 | REQ-0003-FR-0017 |
| REQ-0007-FR-0005 | REQ-0004-FR-0008 |
| REQ-0007-FR-0006 | REQ-0004-FR-0010 |
| REQ-0007-FR-0007 | REQ-0004-FR-0009 |
| REQ-0007-FR-0008 | REQ-0003-FR-0028 |
| REQ-0007-FR-0009 | REQ-0003-FR-0007 |
| REQ-0007-FR-0010 | REQ-0004-FR-0011 / REQ-0003-FR-0018 / REQ-0003-FR-0019 |
| REQ-0007-FR-0011 | REQ-0004-FR-0012 |
| REQ-0007-FR-0012 | REQ-0004-FR-0013 |
| REQ-0007-FR-0013 | REQ-0004-FR-0014 |
| REQ-0007-NFR-0001 | REQ-0004-NFR-0003 |
| REQ-0007-NFR-0002 | REQ-0003-FR-0014 |

REQ-0004-FR-0009 also inherits REQ-0005-FR-0006's requirement that examples sit beside their executable sources.

- Current architecture: [AD-0007](../02.architecture/descriptions/0007-current-local-gitops-platform.md).
- Platform implementation: [Spec 0008](../03.specs/0008-current-local-gitops-platform/spec.md).
- Shared architecture: [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md).
- Current self-source and namespace decisions remain in the [decision log](../02.architecture/decisions/README.md).
