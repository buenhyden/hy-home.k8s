# WSL2 k3d/k3s ArgoCD HA Platform Architecture Reference Document (ARD)

## Overview (KR)

이 문서는 WSL2 기반 k3d/k3s 멀티노드 플랫폼의 참조 아키텍처를 정의한다. GitOps, Secret, 외부 데이터 서비스 통합 경계를 표준 계약으로 명시한다.

## Summary

플랫폼은 다음 4개 평면으로 구성한다.

- **Cluster Plane**: k3d/k3s `1 master + 3 workers`
- **GitOps Plane**: ArgoCD App-of-Apps + ApplicationSet
- **Secret Plane**: ESO + Vault(Kubernetes auth)
- **External Data Plane**: PostgreSQL(write/read), Valkey, Vault endpoint
- **Access Plane**: External Docker Traefik(443) -> k3d ingress(8443) -> ArgoCD ingress

## Boundaries & Non-goals

- **Owns**:
  - 플랫폼 선언형 리소스(`gitops/`, `infrastructure/`)
  - 외부 서비스의 Kubernetes 인터페이스 계약(Service/EndpointSlice)
- **Consumes**:
  - 외부 런타임(Vault/PostgreSQL/Valkey)
  - WSL2 + Docker Desktop 실행 환경
- **Does Not Own**:
  - 외부 서비스 컨테이너 라이프사이클 자체
  - 비즈니스 워크로드 애플리케이션 로직
- **Non-goals**:
  - 멀티클러스터 페더레이션
  - 퍼블릭 클라우드 운영 자동화 전체

## Quality Attributes

- **Performance**: WSL2 리소스 예산 내에서 제어면 안정 유지
- **Security**: RBAC 최소권한 + Vault policy 기반 시크릿 접근
- **Reliability**: 상태 드리프트 self-heal + 명시적 recovery runbook
- **Scalability**: Git generator 기반 ApplicationSet으로 앱 확장
- **Observability**: ArgoCD/ESO/Store Ready 상태와 이벤트 로그 수집
- **Operability**: 스크립트 기반 사전검증 + 문서 추적성(01~09)

## System Overview & Context

- Host: Windows + WSL2(Ubuntu)
- Container Runtime: Docker Desktop (WSL integration)
- K8s: k3s `v1.35.0+k3s1`, k3d `v5.8.3`
- GitOps: ArgoCD
- Secret: External Secrets Operator + HashiCorp Vault
- Data: External PostgreSQL + External Valkey
- External Bridge CIDR: `172.30.0.0/24`

## Data Architecture

- **Key Entities / Flows**:
  - Git desired state -> ArgoCD reconciliation -> cluster live state
  - Vault KV -> ESO -> Kubernetes Secret
  - Workload/ArgoCD -> Service/EndpointSlice -> external DB/Cache
- **Storage Strategy**:
  - 시크릿 원본은 Vault 단일 소스
  - Git에는 평문 비밀값 저장 금지
- **Data Boundaries**:
  - `platform`, `argocd`, `external-secrets` namespace 분리
  - namespace별 egress 제어 정책 분리:
    - `platform`: Vault/PostgreSQL/Valkey 허용
    - `argocd`: Valkey 허용
    - `external-secrets`: Vault 허용
  - ArgoCD 접근 경계:
    - 공식 FQDN: `argocd.127.0.0.1.nip.io`
    - ingress TLS secret: `argocd-local-tls` (`argocd` namespace)

## Infrastructure & Deployment

- **Runtime / Platform**: k3d cluster config(`servers:1`, `agents:3`)
- **Deployment Model**: root app(`gitops/apps/root`) 기반 GitOps 동기화
- **Operational Evidence**: `infrastructure/tests/*.sh` + runbook 명령 증적
- **Network Isolation**:
  - 외부 브리지 대역 `172.30.0.0/24`로 고정
  - 서비스 인터페이스는 `Service + EndpointSlice` 표준 래핑
- **Ingress Ownership Boundary**:
  - 호스트 `80/443`은 외부 Docker Traefik 소유
  - 본 저장소는 계약만 정의: `443 -> k3d :8443`
  - 실제 Traefik 라우팅 파일은 외부 인프라 저장소에서 관리

## AI Agent Architecture Requirements (If Applicable)

- **Model/Provider Strategy**: 문서 우선 + 증적 중심 운영
- **Tooling Boundary**: non-destructive 기본, 승인 기반 확장
- **Memory & Context Strategy**: PRD-ARD-ADR-Spec-Plan-Task-Guide-Oper-Runbook 체인 유지
- **Guardrail Boundary**: 시크릿/토큰 평문 기록 금지
- **Latency / Cost Budget**: 로컬 개발 목적(WSL 자원 한도 내)

## Related Documents

- **PRD**: [`../01.prd/2026-03-28-wsl2-k3d-argocd-ha-platform.md`](../01.prd/2026-03-28-wsl2-k3d-argocd-ha-platform.md)
- **Spec**: [`../04.specs/002-wsl2-k3d-argocd-ha-platform/spec.md`](../04.specs/002-wsl2-k3d-argocd-ha-platform/spec.md)
- **Plan**: [`../05.plans/2026-03-28-wsl2-k3d-argocd-ha-platform.md`](../05.plans/2026-03-28-wsl2-k3d-argocd-ha-platform.md)
- **ADR**: [`../03.adr/0005-wsl2-ha-baseline-and-external-endpoint-contract.md`](../03.adr/0005-wsl2-ha-baseline-and-external-endpoint-contract.md)
