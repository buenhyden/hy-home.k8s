---
title: 'WSL2 k3d/k3s ArgoCD HA Platform Architecture Reference Document'
type: ard
status: draft
owner: platform
updated: 2026-05-22
---

# WSL2 k3d/k3s ArgoCD HA Platform Architecture Reference Document (ARD)

## Overview (KR)

이 문서는 WSL2 기반 k3d/k3s 멀티노드 플랫폼의 참조 아키텍처를 정의한다. GitOps, Secret, 외부 데이터 서비스 통합 경계와 CI 정적 검증 계층을 표준 계약으로 명시한다.

> **현재 실행계약 메모 (2026-05-22)**: 이 ARD는 2026-03-28 HA 플랫폼 참조 아키텍처 기록이다. 현재 기본 컨테이너 런타임 전제는 WSL-native Docker이며, 역사적 Docker Desktop 표현은 당시 실행 기준으로만 해석한다. 현재 repo-backed 외부 서비스 실행계약은 `gitops/platform/external-services/`, `gitops/platform/network-policies/`, `infrastructure/tests/verify-contracts-static.sh`의 `172.18.x` EndpointSlice/CIDR 값이 우선한다.

## Summary

플랫폼은 다음 5개 평면으로 구성한다.

- **Cluster Plane**: k3d/k3s `1 master + 3 workers`
- **GitOps Plane**: ArgoCD App-of-Apps + ApplicationSet
- **Secret Plane**: ESO + Vault(Kubernetes auth)
- **External Data Plane**: PostgreSQL(write/read), Valkey, Vault endpoint
- **CI Control Plane**: GitHub Actions 변경영역 기반 정적 게이트
- **Access Plane**: External Docker Traefik(443) -> k3d ingress(8443) -> ArgoCD ingress

## Boundaries & Non-goals

- **Owns**:
  - 플랫폼 선언형 리소스(`gitops/`, `infrastructure/`)
  - 외부 서비스의 Kubernetes 인터페이스 계약(Service/EndpointSlice)
  - CI 정적 검증 워크플로우(`.github/workflows/ci.yml`)
- **Consumes**:
  - 외부 런타임(Vault/PostgreSQL/Valkey)
  - WSL2 + Docker Desktop 실행 환경
- **Does Not Own**:
  - 외부 서비스 컨테이너 라이프사이클 자체
  - 외부 Traefik 라우팅 파일 실제 구현
- **Non-goals**:
  - 멀티클러스터 페더레이션
  - GitHub Actions 기반 push deploy

## Quality Attributes

- **Performance**: WSL2 리소스 예산 내에서 제어면 안정 유지
- **Security**: RBAC/AppProject/Vault policy 최소권한 + workflow security gate
- **Reliability**: ArgoCD self-heal + 런북 기반 복구 + 정적 계약 회귀 탐지
- **Scalability**: Git generator 기반 ApplicationSet으로 앱 확장
- **Observability**: ArgoCD/ESO/Store Ready 상태와 이벤트 로그 수집
- **Operability**: 스크립트 기반 검증 + 현재 docs taxonomy 추적성

## System Overview & Context

- Host: Windows + WSL2(Ubuntu)
- Container Runtime: Docker Desktop (WSL integration)
- K8s baseline: k3s `v1.35.0+k3s1`, k3d `v5.8.3`
- GitOps: ArgoCD (`root-platform` -> `gitops/apps/root`, `main`)
- Secret: External Secrets Operator + HashiCorp Vault
- Data: External PostgreSQL + External Valkey
- External Bridge CIDR: `172.30.0.0/24`

## Data Architecture

- **Key Entities / Flows**:
  - Git desired state -> ArgoCD reconciliation -> cluster live state
  - Vault KV -> ESO -> Kubernetes Secret
  - ArgoCD/workloads -> Service/EndpointSlice -> external DB/Cache
- **Storage Strategy**:
  - 시크릿 원본은 Vault 단일 소스
  - Git에는 평문 비밀값 저장 금지
- **Data Boundaries**:
  - `platform`, `argocd`, `external-secrets` namespace 분리
  - namespace별 egress 정책 분리:
    - `platform`: Vault/PostgreSQL/Valkey 허용
    - `argocd`: Valkey + DNS + HTTPS 허용
    - `external-secrets`: Vault 허용

## Infrastructure & Deployment

- **Runtime / Platform**: `infrastructure/k3d/k3d-cluster.yaml` (`servers:1`, `agents:3`)
- **Deployment Model**: ArgoCD pull 기반 CD(자동 동기화/자가치유)
- **Ingress Ownership Boundary**:
  - 호스트 `80/443`은 외부 Docker Traefik 소유
  - 본 저장소는 계약만 정의: `443 -> k3d :8443`
- **TLS Contract**:
  - 공식 FQDN: `argocd.127.0.0.1.nip.io`
  - secret: `argocd-local-tls` (`argocd` namespace) # pragma: allowlist secret

## CI Architecture

- **Path Detection**: `dorny/paths-filter`로 변경영역 분류
- **Static Gates**:
  - `pre-commit`: 공통 품질
  - `manifest-static`: `verify-contracts-static.sh`
  - `workflow-security`: `actionlint` + `zizmor`
  - `shell-static`: `bash -n` + `shellcheck`
- **Aggregation**: `ci-summary`가 잡 결과를 집계하고 실패를 최종 반영
- **Principle**: CI는 정적 검증 중심, 런타임 검증은 로컬 `run-all.sh`로 분리

## Related Documents

- **PRD**: [`../../01.requirements/2026-03-28-wsl2-k3d-argocd-ha-platform.md`](../../01.requirements/2026-03-28-wsl2-k3d-argocd-ha-platform.md)
- **Spec**: [`../../03.specs/002-wsl2-k3d-argocd-ha-platform/spec.md`](../../03.specs/002-wsl2-k3d-argocd-ha-platform/spec.md)
- **Plan**: [`../../04.execution/plans/2026-03-28-wsl2-k3d-argocd-ha-platform.md`](../../04.execution/plans/2026-03-28-wsl2-k3d-argocd-ha-platform.md)
- **ADR**: [`../decisions/0005-wsl2-ha-baseline-and-external-endpoint-contract.md`](../decisions/0005-wsl2-ha-baseline-and-external-endpoint-contract.md)
