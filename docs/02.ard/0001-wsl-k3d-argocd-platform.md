# WSL k3d/k3s ArgoCD Platform Architecture Reference Document (ARD)

## Overview (KR)

이 문서는 WSL2 환경에서 동작하는 k3d(k3s) 기반 Kubernetes 플랫폼의 참조 아키텍처를 정의한다. GitOps, 시크릿 관리, 외부 데이터 서비스 연결, 운영 통제 기준을 아키텍처 관점에서 명시한다.

## Summary

이 아키텍처는 로컬 개발 환경에서도 선언형 배포, 최소권한, 복구 가능성을 확보하기 위해 설계된 단일 리포 기반 GitOps 플랫폼이다.

## Boundaries & Non-goals

- **Owns**:
  - WSL2 기반 로컬 플랫폼 참조 구조
  - ArgoCD GitOps 경계/프로젝트 스코프
  - ESO + Vault 기반 시크릿 동기화 모델
  - 외부 서비스(K8s 래핑/외부 URL 포함) 연결 모델
- **Consumes**:
  - Docker Desktop networking
  - Helm/Kustomize 생태계
- **Does Not Own**:
  - 애플리케이션 도메인 기능 설계
  - 프로덕션 인프라 운영 자동화 전체
- **Non-goals**:
  - 멀티 클러스터 페더레이션
  - 완전한 DR 자동화

## Quality Attributes

- **Performance**: 로컬 개발 기준 빠른 재기동/동기화(수분 단위).
- **Security**: RBAC 최소권한, Vault 정책 기반 secret retrieval, NetworkPolicy egress 제한.
- **Reliability**: 선언형 복구, self-heal, 명시적 rollback runbook.
- **Scalability**: App-of-Apps + ApplicationSet으로 앱 수평 확장.
- **Observability**: ArgoCD health/sync 상태, 핵심 컴포넌트 로그/이벤트 추적.
- **Operability**: 문서 01~09 추적성과 표준 절차 제공.

## System Overview & Context

- Host: Windows + WSL2 Ubuntu
- Runtime: Docker Desktop backend
- Cluster: k3d(k3s) `1 server + 3 agents`
- GitOps Control Plane: ArgoCD(Helm install)
- Secret Plane: ESO + Vault Kubernetes Auth
- Data Plane: external PostgreSQL, managed Valkey

## Data Architecture

- **Key Entities / Flows**:
  - Git desired state -> ArgoCD reconciliation -> K8s live state
  - Vault secret path -> ESO -> Kubernetes Secret
  - Workload -> Service/EndpointSlice -> external PostgreSQL
  - ArgoCD/Workload -> ExternalName Service -> managed Valkey
- **Storage Strategy**:
  - 플랫폼 상태는 Git 선언으로 버전 관리
  - 런타임 비밀은 Vault에 저장, Git 비저장
- **Data Boundaries**:
  - ArgoCD project 경계 내에서 repo/namespace 허용 목록 제한

## Infrastructure & Deployment

- **Runtime / Platform**: WSL2, Docker Desktop, k3d, k3s
- **Deployment Model**: ArgoCD App-of-Apps + ApplicationSet Git generator
- **Operational Evidence**: runbook 기반 검증 체크리스트, task 증적 링크

## AI Agent Architecture Requirements (If Applicable)

- **Model/Provider Strategy**: 문서 우선 설계, 실행 전 검증 중심.
- **Tooling Boundary**: non-destructive 기본, 위험 변경 시 승인.
- **Memory & Context Strategy**: 01~09 문서를 SSoT로 상호 추적.
- **Guardrail Boundary**: 보안 정책 완화/권한 확장 자동 금지.
- **Latency / Cost Budget**: 로컬 개발 워크플로 기준 최적화.

## Related Documents

- **PRD**: [`../01.prd/2026-03-27-wsl-k3d-argocd-platform.md`](../01.prd/2026-03-27-wsl-k3d-argocd-platform.md)
- **Spec**: [`../04.specs/001-wsl-k3d-argocd-platform/spec.md`](../04.specs/001-wsl-k3d-argocd-platform/spec.md)
- **Plan**: [`../05.plans/2026-03-27-wsl-k3d-argocd-platform.md`](../05.plans/2026-03-27-wsl-k3d-argocd-platform.md)
- **ADR**: [`../03.adr/0001-k3d-topology-and-network.md`](../03.adr/0001-k3d-topology-and-network.md), [`../03.adr/0002-argocd-helm-and-gitops-model.md`](../03.adr/0002-argocd-helm-and-gitops-model.md), [`../03.adr/0003-eso-vault-k8s-auth.md`](../03.adr/0003-eso-vault-k8s-auth.md), [`../03.adr/0004-external-services-endpoints-and-valkey-backend.md`](../03.adr/0004-external-services-endpoints-and-valkey-backend.md)
