---
title: "K8s GitOps Platform Operations Policy"
version: "1.0"
type: sdlc/policy
layer: "05.operations"
status: active
owner: platform
updated: 2026-09-01
artifact_id: "POL-0001"
---

# K8s GitOps Platform Operations Policy

## Overview

이 문서는 WSL2 기반 로컬 k3d GitOps 플랫폼의 운영 통제를 정의한다.
여기서 multi-node 또는 HA는 production 고가용성 보장이 아니라
`infrastructure/k3d/k3d-cluster.yaml`의 `servers: 1`, `agents: 3` 로컬
검증 baseline을 뜻한다.

## Policy Scope

- k3d cluster와 ArgoCD pull 기반 GitOps 운영
- ESO와 외부 Vault의 시크릿 경계
- 외부 PostgreSQL·Valkey·Vault 서비스 인터페이스
- ingress-nginx, 외부 Traefik, AppProject, NetworkPolicy 통제
- repository 정적 검증과 승인된 runtime 검증의 증적 경계

## Applies To

- **Systems**: `infrastructure/`, `gitops/`, `.github/workflows/`
- **Roles**: Platform Owner, Security Reviewer, GitOps/Docs automation agents
- **Environment**: WSL2 local cluster와 GitHub Actions

## Controls

### Responsibilities

| Role | Responsibility | Escalation owner |
| --- | --- | --- |
| Platform Owner | GitOps desired state, external endpoint, runtime baseline을 승인한다. | Workspace Owner |
| Security Reviewer | Vault, RBAC, NetworkPolicy, 예외의 최소권한을 검토한다. | Workspace Owner |
| Change author | 정적 검증과 필요한 승인·runtime 증적을 handoff한다. | Platform Owner |

### Control Register

| Control | Accountable role | Enforcement surface | Evidence |
| --- | --- | --- | --- |
| PLAT-001 topology | Platform Owner | `infrastructure/k3d/k3d-cluster.yaml` | `servers: 1`, `agents: 3`; inotify preflight `>= 512` |
| PLAT-002 external desired state | Platform Owner | `gitops/platform/external-services/*.yaml` | reviewed Service/EndpointSlice definitions |
| PLAT-003 secret boundary | Security Reviewer | Vault, ESO, secret scanners | no plaintext secret; approved Vault/ESO health evidence |
| PLAT-004 ingress and TLS | Platform Owner | ingress-nginx, Traefik, ArgoCD ingress | host, TLS secret, route target agreement |
| PLAT-005 least privilege | Security Reviewer | AppProject, RBAC, NetworkPolicy | wildcard absence and destination/egress review |
| PLAT-006 validation | Change author | local validators and GitHub Actions | static PASS plus separately approved runtime evidence when required |

### Required

- External-service Service와 EndpointSlice desired state는
  `gitops/platform/external-services/*.yaml`을 single source of truth로 삼는다.
- 포트 계약은 Vault `8200`, Valkey `6379`, PostgreSQL write `15432`,
  PostgreSQL read `15433`을 유지한다.
- Vault는 시크릿의 단일 소스이며 문서, manifest, Git history에 평문 토큰,
  비밀번호, API key를 저장하지 않는다.
- 호스트 접근은 `https://vault.127.0.0.1.nip.io`, cluster 내부 ESO 접근은
  `vault-external.platform.svc`를 사용한다.
- Vault Kubernetes auth는 현재 API endpoint와 reviewer JWT/CA 경계를
  소유 Runbook의 검증 대상으로 유지한다.
- ArgoCD host는 `argocd.127.0.0.1.nip.io`, TLS secret은
  `argocd-local-tls`이며, 외부 Traefik `websecure/443`은 ingress-nginx
  LoadBalancer endpoint로 라우팅한다.
- AppProject source/destination과 RBAC는 최소 allow-list, NetworkPolicy는
  필요한 DNS·HTTPS·external-service egress만 허용한다.
- CD는 ArgoCD pull/reconciliation이 소유한다. GitHub Actions와 로컬 gate는
  정적 검증 증적이며 배포 완료 증적을 대신하지 않는다.

### Allowed

- 검토된 Git desired state 변경과 ArgoCD reconciliation
- read-only 진단과 소유 Runbook에 따른 복구
- 명시적 human approval과 증적을 갖춘 bootstrap/break-glass 작업

### Disallowed

- 평문 시크릿 커밋, 승인 없는 권한 확장, wildcard AppProject 허용
- 로컬 파일 또는 정적 PASS만으로 runtime 배포·복구 완료 선언
- k3d agent 동시 재시작 또는 production HA로의 과장된 증적 표현
- Git desired state 없이 EndpointSlice를 상시 수동 관리

## Exceptions

EndpointSlice patch, AppProject live 반영, 외부 Vault 변경은 즉시 복구가
필요하고 Platform Owner가 범위·기간·위험·rollback을 승인한 bootstrap 또는
break-glass 상황에서만 허용한다. 실행 후 실제 상태를 Git desired state와
맞추고 승인·검증 증적을 남긴다. 예외는 만료 시 기본 통제로 복귀한다.

## Verification

| Control Area | Required Evidence | Runbook Owner |
| --- | --- | --- |
| Bootstrap and GitOps root | source path, revision, AppProject가 current Git 계약과 일치 | [RUN-0001](../runbooks/0001-argocd-platform-bootstrap-runbook.md) |
| External endpoints | Service/EndpointSlice 이름, IP, 포트가 reviewed desired state와 일치 | [RUN-0001](../runbooks/0001-argocd-platform-bootstrap-runbook.md) |
| Vault and ESO recovery | auth, network, ExternalSecret 상태와 plaintext 부재 | [RUN-0002](../runbooks/0002-argocd-eso-vault-recovery-runbook.md) |
| Static controls | affected validators와 hosted CI 결과; runtime claim과 분리 | [GDE-0010](../guides/0010-ci-cd-qa-reference-guide.md) |

## Review Cadence

월 1회 또는 topology, external endpoint, Vault auth, ingress/TLS, AppProject,
NetworkPolicy, CI workflow 계약이 바뀔 때 즉시 검토한다. 고정된 job 수나
문서 수가 아니라 현재 source와 semantic contract를 검토한다.

## Traceability

- [AD-0007 Current Local GitOps Platform](../../02.architecture/descriptions/0007-current-local-gitops-platform.md)
- [Spec 0008 Current Local GitOps Platform](../../03.specs/0008-current-local-gitops-platform/spec.md)
- [Platform Bootstrap Runbook](../runbooks/0001-argocd-platform-bootstrap-runbook.md)
- [ArgoCD/ESO/Vault Recovery Runbook](../runbooks/0002-argocd-eso-vault-recovery-runbook.md)

### Lifecycle Traceability

| Promoted owner | Control owner | Enforcement surface |
| --- | --- | --- |
| [Spec 0008](../../03.specs/0008-current-local-gitops-platform/spec.md) | Platform Owner; Security Reviewer for secrets and exceptions | k3d topology, GitOps desired state, Vault/ESO, ingress, AppProject, NetworkPolicy, static and approved runtime evidence |
