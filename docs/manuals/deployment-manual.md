---
layer: "infra"
---
# Deployment Manual (DEPLOYMENT.md)

_Target Location: `docs/manuals/deployment-manual.md`_
_Description: Defines the project's environment hierarchy and deployment workflows using GitOps principles and ArgoCD._

## Overview (KR)
이 문서는 프로젝트의 환경 구성과 배포 워크플로우를 정의합니다. GitOps 원칙에 기반한 ArgoCD 활용 방식과 불변 인프라(Immutable Infrastructure) 배포 정책을 다룹니다.

---

## 1. Environment Hierarchy

- **Development (Dev)**: 
  - **Purpose**: Feature validation and integration testing.
  - **Trigger**: Automatic deployment on PR merge to `main`.
- **Staging**: 
  - **Purpose**: Pre-production parity testing (Performance, QA).
  - **Trigger**: Tag-based deployment (`v*.*.*-rc.*`) via ArgoCD.
- **Production**: 
  - **Purpose**: Live user traffic.
  - **Trigger**: Manual promotion or high-confidence CI/CD release.

## 2. Infrastructure as Code (IaC)

- **Policy**: Manual "ClickOps" in production is strictly **FORBIDDEN**.
- **Tools**:
  - **Cluster Management**: K3d/K3s (WSL2 host).
  - **GitOps**: ArgoCD for declarative state reconciliation.
  - **Secrets**: Sealed Secrets for Git-safe credential management.

## 3. Deployment Workflow (GitOps)

1. **Commit**: Standardized commit following conventional commit standards.
2. **Build**: GitHub Actions builds OCI-compliant image and pushes to registry.
3. **Update**: Update manifest/helm values in the `gitops` repository (or folder).
4. **Sync**: ArgoCD detects the diff and synchronizes the cluster state.

## 4. Rollback Procedure
- **ArgoCD**: Use the "Rollback" feature in the ArgoCD UI for immediate reversion.
- **Git**: Revert the commit in the GitOps repository to ensure the declarative state matches the desire.
