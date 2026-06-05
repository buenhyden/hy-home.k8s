---
title: 'Current Local GitOps Platform Product Requirements'
type: prd
status: active
owner: platform
updated: 2026-06-02
---

# Current Local GitOps Platform Product Requirements

## Overview

이 문서는 현재 repo-backed 구현을 기준으로 로컬 GitOps 플랫폼 요구사항을 정의한다.
old 요구사항 문서는 `98.archive` Tombstone으로 격리하고, 이 문서가 현재 플랫폼 범위의 PRD 입력을 소유한다.

## Vision

WSL2 + WSL-native Docker 기반 로컬 Kubernetes 플랫폼을 GitOps-first 방식으로 재현 가능하게 운영한다.
플랫폼 사용자는 현재 Git desired state와 정적 검증 증거만으로 구현 범위, 운영 경계, 외부 서비스 계약을 판단할 수 있어야 한다.

## Problem Statement

초기 문서에는 오래된 endpoint와 제거된 UI 구성 요소가 남아 있어 현재 구현과 문서 판단 기준이 갈라졌다.
현재 플랫폼 요구사항은 active 문서에서 current contract만 설명하고, old 실행계약은 archive index로만 추적해야 한다.

## Personas

- **Platform Engineer**: 로컬 k3d 플랫폼 구성과 GitOps desired state를 변경하고 검증해야 한다.
- **GitOps Operator**: ArgoCD App-of-Apps, platform Application, workload ApplicationSet 상태를 기준으로 운영 경계를 판단해야 한다.
- **AI Agent**: 현재 구현과 상충되는 historical 문서를 current input으로 사용하지 않아야 한다.

## Key Use Cases

- **STORY-01**: 사용자는 `gitops/`와 `infrastructure/tests/verify-contracts-static.sh`를 통해 현재 플랫폼 계약을 확인한다.
- **STORY-02**: 운영자는 Headlamp, Kiali, Rollouts, ArgoCD UI를 local ingress/TLS 경로로 접근한다.
- **STORY-03**: 애플리케이션 작성자는 `gitops/workloads/adminer`와 `examples/sample-app` 패턴을 기준으로 앱을 온보딩한다.
- **STORY-04**: AI Agent는 old 문서 본문 대신 current baseline 문서와 archive index를 사용한다.

## Functional Requirements

- **REQ-PRD-FUN-01**: 로컬 클러스터 desired state는 `gitops/clusters/local`, `gitops/apps/root`, `gitops/platform`, `gitops/workloads`가 소유한다.
- **REQ-PRD-FUN-02**: ArgoCD는 App-of-Apps와 ApplicationSet 구조로 platform component와 workload를 분리해야 한다.
- **REQ-PRD-FUN-03**: 외부 Vault, PostgreSQL, Valkey, observability service는 Kubernetes `Service`와 `EndpointSlice` 계약으로 연결해야 한다.
- **REQ-PRD-FUN-04**: Cluster UI는 Headlamp를 기준으로 하며 active docs는 제거된 old UI runtime을 current input으로 다루지 않는다.
- **REQ-PRD-FUN-05**: cert-manager, ingress-nginx, Istio, Kiali, Argo Rollouts, Argo Notifications, monitoring, ESO/Vault 연동은 현재 platform scope에 포함한다.
- **REQ-PRD-FUN-06**: secret value, Vault token, private key는 Git, 문서, 로그에 남기지 않는다.
- **REQ-PRD-FUN-07**: archive로 이동한 old 문서는 active 문서와 Index Only로만 연결한다.

## Success / Acceptance Criteria

- **REQ-PRD-MET-01**: `bash infrastructure/tests/verify-contracts-static.sh`가 현재 GitOps contract를 통과한다.
- **REQ-PRD-MET-02**: `bash scripts/validate-gitops-structure.sh`가 root Application, platform Application, workload ApplicationSet 경계를 통과한다.
- **REQ-PRD-MET-03**: `bash scripts/validate-k8s-manifests.sh .`가 tracked Kubernetes YAML syntax를 통과한다.
- **REQ-PRD-MET-04**: `bash scripts/validate-repo-quality-gates.sh .`가 active docs와 archive Tombstone policy를 통과한다.

## Scope and Non-goals

- **In Scope**:
  - WSL2 + WSL-native Docker + k3d local platform.
  - ArgoCD App-of-Apps GitOps model.
  - Platform components under `gitops/platform`.
  - `adminer` reference workload and app onboarding examples.
  - Active-doc/archive cleanup policy.
- **Out of Scope**:
  - External Vault/PostgreSQL/Valkey runtime creation.
  - Cloud provider resource provisioning.
  - Live cluster mutation without explicit human approval.
- **Non-goals**:
  - Preserving old conflicting document bodies in active docs.
  - Treating archive Tombstones as implementation guidance.

## Risks, Dependencies, and Assumptions

- External services must already exist outside this repository.
- Live cluster validation requires a trusted kubeconfig and bootstrapped k3d environment.
- Static validation proves repo-backed desired state, not live reconciliation.
- Active docs must be updated when GitOps desired state changes.

## AI Agent Requirements (If Applicable)

- **Allowed Actions**:
  - Read active baseline docs, GitOps manifests, infrastructure scripts, and archive index.
  - Update active docs and Tombstones when implementation scope changes.
- **Disallowed Actions**:
  - Use archived Tombstone targets as current implementation input.
  - Reintroduce old conflicting runtime contracts into active docs.
  - Read or expose secrets.
- **Human-in-the-loop Requirement**:
  - Required for live cluster mutation, Vault writes, secret rotation, or external service changes.
- **Evaluation Expectation**:
  - Run repo quality and relevant static GitOps checks before handoff.

## Related Documents

- **ARD**: [../02.architecture/requirements/0007-current-local-gitops-platform.md](../02.architecture/requirements/0007-current-local-gitops-platform.md)
- **Spec**: [../03.specs/008-current-local-gitops-platform/spec.md](../03.specs/008-current-local-gitops-platform/spec.md)
- **Plan**: [../04.execution/plans/2026-06-02-current-implementation-docs-alignment.md](../04.execution/plans/2026-06-02-current-implementation-docs-alignment.md)
- **ADR**: [../02.architecture/decisions/0014-current-local-gitops-platform-contract.md](../02.architecture/decisions/0014-current-local-gitops-platform-contract.md)
- **Archive Index**: [../98.archive/README.md](../98.archive/README.md)
