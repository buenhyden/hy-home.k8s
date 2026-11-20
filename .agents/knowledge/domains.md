---
title: "Domain Index"
version: "1.0.0"
type: "governance/knowledge"
status: "draft"
owner: "platform"
updated: "2026-11-20"
---

# Domain Index

## 문서 개요

### 목적과 독자

이 지식 문서는 Domain Index에서 현재 소유 경로를 찾는 작업자와 검토자의 탐색을 돕는다. 개요는 [Overview](#overview)에 기록한다.

### 책임과 적용 범위

platform은 이 지식 지도를 유지한다. 권한 경계는 [Authority Boundary](#authority-boundary), 실제 포인터는 [Pointer Index](#pointer-index)에 기록한다.

## 내용 계약

### 입력과 전제

입력과 전제는 아래 역할별 본문의 해당 절에 기록한다.

### 본문과 규칙

#### Overview

A reader working in one operating domain asks which document is authoritative
for it and which file to open first. This index answers that per domain and
carries no content of its own.

#### Authority Boundary

A row names an owner; it does not summarize one. Operating policies, runbooks
and architecture descriptions keep their scope, their evidence rules and their
approval boundaries. Where a row and its owner disagree, the owner is correct
and the row is stale.

#### Pointer Index

| Domain | Owner path | Entry path | Stays valid while |
| --- | --- | --- | --- |
| Kubernetes and GitOps desired state | `gitops/` | `docs/05.operations/02.policies/README.md` | ArgoCD reconciles this repository and desired state stays declarative |
| Platform architecture and topology | `docs/02.architecture/01.descriptions/` | `docs/02.architecture/01.descriptions/README.md` | The local k3d platform remains the described system |
| Networking, ingress and service mesh | `gitops/platform/` | `docs/05.operations/02.policies/README.md` | Ingress and mesh stay platform components under `gitops/platform/` |
| Vault and External Secrets | `gitops/platform/eso/` | `docs/05.operations/03.runbooks/README.md` | External Secrets remains the mechanism that projects Vault material |
| Observability | `gitops/platform/monitoring/` | `docs/05.operations/02.policies/README.md` | Metrics, dashboards and alerts stay platform-owned |
| Progressive delivery and notifications | `gitops/platform/` | `docs/05.operations/02.policies/README.md` | Argo Rollouts remains the progressive delivery mechanism |
| Application onboarding | `gitops/workloads/` | `docs/05.operations/02.policies/README.md` | New workloads enter through the onboarding path rather than direct cluster change |
| Documents, profiles and templates | `docs/99.templates/` | `docs/99.templates/README.md` | One profile owns each physical document form |
| Validation routing and gates | `scripts/validation/` | `scripts/README.md` | Validator routing stays declarative and registry-owned |
| Local validation environment | `docs/00.workspace/05.environment/` | `docs/00.workspace/05.environment/README.md` | The hashed validation lock and external-checkout tool environment remain the preparation inputs |
| Agent responsibilities and permissions | `.agents/roles/` | `.agents/roles/README.md` | The registry stays the single source for roles and permission classes |

#### Validation and Refresh

The external-service audit uses this bounded provenance observation. Re-read
the source for its values; owner review is required before promotion or reuse
after invalidation.

```knowledge-fact
{
  "owner": "platform",
  "scope": "external Valkey frontend and backend port observation",
  "source": {
      "sha256": "99b67cdd1f884979a771a1b7ca80174f3ff0dab97551014ffe7e06104f4a80e6",
      "path": "gitops/platform/external-services/valkey-external.yaml"
  },
  "observed_at": "2026-09-29",
  "valid_for": "2026-12-28",
  "invalidated_by": [
    "source",
    "scope",
    "approval",
    "validity"
  ],
  "review_status": "advisory",
  "sensitivity": "public"
}
```

Every canonical owner and entry path above must exist; a missing path fails the
knowledge validator. A row is refreshed when its domain changes owner, and
retired when the domain stops existing. A new operating policy or runbook does
not by itself require a row; only a change of canonical owner does.

#### Related Documents

- [Common Knowledge](README.md)
- [Project Map](project-map.md)
- Operations policies (`docs/05.operations/02.policies/README.md`)

## 적용과 확인

### 적용 방법

아래 역할별 본문에 기록된 사용 조건과 절차를 적용한다.

### 확인 기준

아래 역할별 본문의 검증·확인 조건과 그 한계에 따른다.

## 관계와 출처

### 관련 문서

관련 문서와 정본 링크는 아래 역할별 본문에서 확인한다.

### 외부 근거

외부 근거가 사용된 경우 아래 역할별 본문의 출처와 적용 범위에서 확인한다.
