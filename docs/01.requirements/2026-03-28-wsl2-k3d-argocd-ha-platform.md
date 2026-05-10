# WSL2 k3d/k3s ArgoCD HA Platform Product Requirements

## Overview (KR)

이 문서는 Windows WSL2 환경에서 `k3s + k3d` 멀티노드(`1 Master + 3 Workers`) 플랫폼을 구축하고, ArgoCD GitOps/ESO+Vault/외부 PostgreSQL/외부 Valkey를 안정적으로 통합하기 위한 제품 요구사항을 정의한다.

> **현재 실행계약 메모 (2026-05-09)**: 이 PRD는 2026-03-28 HA 플랫폼 요구사항 기록이다. 현재 repo-backed 외부 서비스 실행계약은 `gitops/platform/external-services/`, `gitops/platform/network-policies/`, `infrastructure/tests/verify-contracts-static.sh`의 `172.18.x` EndpointSlice/CIDR 값이 우선한다.

## Vision

WSL2 개발 환경에서도 운영 수준의 재현성, 보안성, 복구 가능성을 갖춘 GitOps 플랫폼을 표준화한다.

## Problem Statement

로컬 플랫폼 운영에서 외부 서비스 연결 계약, 시크릿 동기화, ArgoCD 상태 복구 절차가 분산되어 재현성과 운영 안정성이 낮다. 또한 CI가 단일 품질 게이트에 집중되어 계약 회귀를 조기에 차단하지 못한다.

## Personas

- **Platform Engineer**: WSL2에서 클러스터를 빠르게 재구축하고 네트워크/리소스를 안정적으로 운영해야 한다.
- **DevOps Engineer**: GitOps 배포 파이프라인을 일관되게 유지하고 장애 시 즉시 복구해야 한다.
- **Security Engineer**: 최소권한(RBAC/Vault policy)과 시크릿 관리 통제를 강제해야 한다.

## Key Use Cases

- **STORY-01**: WSL2에서 `k3d` 멀티노드 클러스터(`1+3`)를 재현 가능하게 기동한다.
- **STORY-02**: ArgoCD App-of-Apps + ApplicationSet으로 플랫폼 컴포넌트를 자동 동기화한다.
- **STORY-03**: ESO가 Vault에서 시크릿을 동기화해 ArgoCD/워크로드가 소비한다.
- **STORY-04**: 외부 PostgreSQL/Valkey/Vault를 Kubernetes Service/EndpointSlice 계약으로 소비한다.
- **STORY-05**: CI에서 변경영역 기반 정적 게이트로 계약 회귀를 클러스터 없이 탐지한다.

## Functional Requirements

- **REQ-PRD-FUN-01**: 클러스터 토폴로지는 `Master 1 + Worker 3`을 만족해야 한다.
- **REQ-PRD-FUN-02**: 외부 서비스 네트워크 대역은 `172.19.0.0/16`(Docker `infra_net` 실제 서브넷)을 사용해야 한다.
- **REQ-PRD-FUN-03**: 다음 공용 인터페이스 계약을 유지해야 한다.
  - `vault-external.platform.svc.cluster.local:8200`
  - `postgres-write-external:15432`
  - `postgres-read-external:15433`
  - `valkey-external:6379` (K8s-side 포트; Docker host publish `26379:6379`는 호스트 접근 전용)
- **REQ-PRD-FUN-03A**: `valkey-external`은 `Service + EndpointSlice(172.19.0.12:6379)` 모델을 사용해야 한다.
- **REQ-PRD-FUN-03B**: ArgoCD HTTPS 공식 엔트리포인트는 `argocd.127.0.0.1.nip.io`로 고정해야 한다.
- **REQ-PRD-FUN-03C**: 호스트 80/443은 외부 Docker Traefik이 소유하며, 443 트래픽은 k3d `:8443`으로 프록시되어야 한다.
- **REQ-PRD-FUN-04**: Vault 경로는 `secret/platform/argocd`, `secret/platform/postgres-app`를 표준으로 사용해야 한다.
- **REQ-PRD-FUN-05**: 보안 통제는 RBAC 최소권한 + Vault policy(`eso-read-platform`)를 적용해야 한다.
- **REQ-PRD-FUN-06**: 현재 docs taxonomy 문서는 상호 상대 링크로 추적성을 유지해야 한다.
- **REQ-PRD-FUN-07**: `argocd-local-tls` Secret은 `secrets/certs/cert.pem,key.pem`를 `bootstrap-local.sh`에서 주입해야 한다.
- **REQ-PRD-FUN-08**: `argocd` namespace egress는 Valkey(6379) + DNS(53/TCP,UDP) + HTTPS(443/TCP)를 허용해야 한다.
- **REQ-PRD-FUN-09**: CI는 정적 검증 중심으로 운영하고 CD는 ArgoCD pull reconciliation 모델을 유지해야 한다.
- **REQ-PRD-FUN-10**: CI 필수 게이트는 `pre-commit`, `manifest-static`, `workflow-security`, `shell-static`를 포함해야 한다.

## Success Criteria

- **REQ-PRD-MET-01**: `vault-backend`(ClusterSecretStore) `Ready=True`.
- **REQ-PRD-MET-02**: `argocd-external-valkey`(ExternalSecret) `Ready=True`.
- **REQ-PRD-MET-03**: `platform-eso-config`, `platform-argocd-config` 앱 `Degraded` 해소.
- **REQ-PRD-MET-04**: 계약 포트(8200/15432/15433/6379) 회귀 0건.
- **REQ-PRD-MET-05**: Vault-ESO 장애 복구 목표시간(MTTR) 15분 이내.
- **REQ-PRD-MET-06**: 보안 검증(AppProject allow-list, Vault 최소권한 정책) 통과율 100%.
- **REQ-PRD-MET-07**: ArgoCD TLS/Ingress 검증(`verify-ingress-tls.sh`) 회귀 0건.
- **REQ-PRD-MET-08**: CI 정적 계약 검증(`verify-contracts-static.sh`) 회귀 0건.

## Scope and Non-goals

- **In Scope**:
  - WSL2 최적화 멀티노드 토폴로지 설계
  - ArgoCD/ESO/Vault/외부 DB/외부 Valkey 통합 설계
  - 변경영역 기반 정적 CI 게이트 구현
  - 검증 스크립트 포함 운영 문서화
- **Out of Scope**:
  - 클라우드 관리형 Kubernetes(EKS/AKS/GKE) 운영
  - 애플리케이션 비즈니스 기능 구현
- **Non-goals**:
  - 외부 서비스 런타임(컨테이너) 자체를 본 저장소에서 기동
  - GitHub Actions push 기반 직접 배포

## Risks, Dependencies, and Assumptions

- WSL2 + Docker Desktop 자원 제한으로 인한 성능 저하 가능성.
- AppProject allow-list 축소 시 신규 리소스 도입 때 화이트리스트 업데이트 필요.
- 인증서 SAN이 공식 호스트(`argocd.127.0.0.1.nip.io`)를 포함하지 않으면 HTTPS 접속이 실패하므로 재발급 절차가 필요.
- CI 정적 게이트 false-positive/false-negative는 정책 예외 승인/룰 개선 루프로 관리한다.

## AI Agent Requirements (If Applicable)

- **Allowed Actions**: 문서 갱신, 비파괴 검증, 상태 수집.
- **Disallowed Actions**: 승인 없는 파괴적 명령(`reset --hard`, 데이터 삭제).
- **Human-in-the-loop Requirement**: 정책 완화/권한 확장/운영 endpoint 변경 시 승인 필수.
- **Evaluation Expectation**: 검증 스크립트 기반 PASS/FAIL 증적 제시.

## Related Documents

- **ARD**: [`../02.architecture/requirements/0002-wsl2-k3d-argocd-ha-platform.md`](../02.architecture/requirements/0002-wsl2-k3d-argocd-ha-platform.md)
- **Spec**: [`../03.specs/002-wsl2-k3d-argocd-ha-platform/spec.md`](../03.specs/002-wsl2-k3d-argocd-ha-platform/spec.md)
- **Plan**: [`../04.execution/plans/2026-03-28-wsl2-k3d-argocd-ha-platform.md`](../04.execution/plans/2026-03-28-wsl2-k3d-argocd-ha-platform.md)
- **ADR**: [`../02.architecture/decisions/0005-wsl2-ha-baseline-and-external-endpoint-contract.md`](../02.architecture/decisions/0005-wsl2-ha-baseline-and-external-endpoint-contract.md)
