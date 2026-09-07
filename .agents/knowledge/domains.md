---
title: "Domain Index"
version: "0.1.0"
type: "governance/knowledge"
status: "draft"
owner: "platform"
updated: "2026-09-07"
---

# Domain Index

## Overview

A reader working in one operating domain asks which document is authoritative
for it and which file to open first. This index answers that per domain and
carries no content of its own.

## Authority Boundary

A row names an owner; it does not summarize one. Operating policies, runbooks
and architecture descriptions keep their scope, their evidence rules and their
approval boundaries. Where a row and its owner disagree, the owner is correct
and the row is stale.

## Pointer Index

| Domain | Owner path | Entry path | Stays valid while |
| --- | --- | --- | --- |
| Kubernetes and GitOps desired state | `gitops/` | `docs/05.operations/policies/0001-k8s-gitops-operations-policy.md` | ArgoCD reconciles this repository and desired state stays declarative |
| Platform architecture and topology | `docs/02.architecture/descriptions/` | `docs/02.architecture/descriptions/0007-current-local-gitops-platform.md` | The local k3d platform remains the described system |
| Networking, ingress and service mesh | `gitops/platform/` | `docs/05.operations/policies/0003-service-mesh-cert-manager-policy.md` | Ingress and mesh stay platform components under `gitops/platform/` |
| Vault and External Secrets | `gitops/platform/eso/` | `docs/05.operations/runbooks/0002-argocd-eso-vault-recovery-runbook.md` | External Secrets remains the mechanism that projects Vault material |
| Observability | `gitops/platform/monitoring/` | `docs/05.operations/policies/0005-observability-platform-operations-policy.md` | Metrics, dashboards and alerts stay platform-owned |
| Progressive delivery and notifications | `gitops/platform/` | `docs/05.operations/policies/0004-rollouts-notifications-headlamp-policy.md` | Argo Rollouts remains the progressive delivery mechanism |
| Application onboarding | `gitops/workloads/` | `docs/05.operations/policies/0007-app-gitops-onboarding-policy.md` | New workloads enter through the onboarding path rather than direct cluster change |
| Documents, profiles and templates | `docs/99.templates/` | `docs/99.templates/README.md` | One profile owns each physical document form |
| Validation routing and gates | `scripts/validation/` | `scripts/README.md` | Validator routing stays declarative and registry-owned |
| Agent responsibilities and permissions | `.agents/roles/` | `.agents/roles/README.md` | The registry stays the single source for roles and permission classes |

## Validation and Refresh

Every canonical owner and entry path above must exist; a missing path fails the
knowledge validator. A row is refreshed when its domain changes owner, and
retired when the domain stops existing. A new operating policy or runbook does
not by itself require a row; only a change of canonical owner does.

## Related Documents

- [Common Knowledge](README.md)
- [Project Map](project-map.md)
- [Operations policies](../../docs/05.operations/policies/README.md)
