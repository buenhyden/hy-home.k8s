---
title: "ArgoCD Helm Install with App-of-Apps and ApplicationSet"
version: "1.0.0"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "platform"
updated: "2026-09-26"
layer: "architecture"
artifact_id: "ADR-0002"
---

# ADR-0002: ArgoCD Helm Install with App-of-Apps and ApplicationSet

## Overview

This ADR settles on a Helm-based ArgoCD install and adopts the App-of-Apps + ApplicationSet + AppProject scoping model.

## Context

Given the external Valkey backend settings, version upgrades, and declarative reproducibility, managing Helm values is better than raw manifests.

## Decision

- ArgoCD is installed and upgraded with its Helm chart.
- A root App-of-Apps application manages the child platform and app applications.
- The ApplicationSet Git generator automates app declarations.
- AppProjects are split into `platform` and `apps`, with least privilege applied to `sourceRepos/destinations/roles`.

## Explicit Non-goals

- Extending to multi-cluster management
- Extending the ArgoCD plugin ecosystem

## Consequences

- **Positive**:
  - Install, upgrade, and rollback are standardized
  - Permission separation along project boundaries becomes clear
- **Trade-offs**:
  - The Helm values schema must keep being tracked

## Alternatives

### Raw install.yaml + kustomize patch

- Good:
  - Directly tied to the official manifests
- Bad:
  - Patch complexity grows as external backends and settings are added

### Operator-centered ArgoCD install

- Good:
  - operator-managed lifecycle
- Bad:
  - More learning and operating complexity, excessive for the local scope

## Traceability

- **PRD**: [`../../01.requirements/0004-current-local-gitops-platform.md`](../../01.requirements/0004-current-local-gitops-platform.md)
- **ARD**: [`../descriptions/0007-current-local-gitops-platform.md`](../descriptions/0007-current-local-gitops-platform.md)
- **Spec**: [`../../03.specs/0008-current-local-gitops-platform/spec.md`](../../03.specs/0008-current-local-gitops-platform/spec.md)
- **Plan**: [`../../04.execution/plans/2026-06-02-current-implementation-docs-alignment.md`](../../98.archive/README.md#document-index)
- **Related ADR**: [`./0014-current-local-gitops-platform-contract.md`](./0014-current-local-gitops-platform-contract.md)
