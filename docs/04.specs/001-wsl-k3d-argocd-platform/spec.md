# WSL k3d/k3s ArgoCD Platform Specification

## Overview (KR)

이 문서는 WSL2 기반 k3d(k3s) 플랫폼에서 ArgoCD GitOps, ESO+Vault, 외부 PostgreSQL/Valkey 연동을 구현하기 위한 기술 명세를 정의한다.

## Strategic Boundaries & Non-goals

- Owns: 클러스터 토폴로지, GitOps 경계, 외부 서비스 인터페이스, 보안 기본 통제.
- Non-goals: 애플리케이션 비즈니스 로직, 클라우드 프로덕션 인프라 자동화.

## Related Inputs

- **PRD**: [`../../01.prd/2026-03-27-wsl-k3d-argocd-platform.md`](../../01.prd/2026-03-27-wsl-k3d-argocd-platform.md)
- **ARD**: [`../../02.ard/0001-wsl-k3d-argocd-platform.md`](../../02.ard/0001-wsl-k3d-argocd-platform.md)
- **Related ADRs**: [`../../03.adr/0001-k3d-topology-and-network.md`](../../03.adr/0001-k3d-topology-and-network.md), [`../../03.adr/0002-argocd-helm-and-gitops-model.md`](../../03.adr/0002-argocd-helm-and-gitops-model.md), [`../../03.adr/0003-eso-vault-k8s-auth.md`](../../03.adr/0003-eso-vault-k8s-auth.md), [`../../03.adr/0004-external-services-endpoints-and-valkey-backend.md`](../../03.adr/0004-external-services-endpoints-and-valkey-backend.md)

## Contracts

- **Config Contract**:
  - k3d: `servers=1`, `agents=3`, server arg `--disable=traefik`
  - External integration network(CIDR): `172.30.0.0/24`
  - Fixed IP: PostgreSQL `.11`
  - Vault/Valkey: 외부 관리형 엔드포인트 사용
- **Data / Interface Contract**:
  - K8s Service names: `postgres-external`, `valkey-external`
  - PostgreSQL은 EndpointSlice로 외부 고정 IP에 매핑
  - Valkey는 ExternalName Service(`host.k3d.internal`)로 외부 관리형 인스턴스에 매핑
- **Governance Contract**:
  - 01~09 문서 추적성 유지
  - README 인덱스 동기화 필수
  - 외부 서비스 런타임은 별도 워크스페이스(repo)에서 관리

## External Runtime Integration (Required)

외부 서비스는 이 저장소에서 기동하지 않는다. 이 저장소는 Kubernetes 매핑/연동 계약만 관리한다.

| 서비스 | 외부 런타임(별도 repo) | 필수 접속값 | 이 저장소 연동 방식 | 기본 확인 |
| --- | --- | --- | --- | --- |
| Vault | `vault`, `vault-agent` on `infra_net` | `https://vault.127.0.0.1.nip.io` | ESO + Vault Kubernetes auth | `curl -ksS -o /dev/null -w '%{http_code}\n' https://vault.127.0.0.1.nip.io/v1/sys/health` |
| PostgreSQL | external DB runtime | `172.30.0.11:5432` | `Service + EndpointSlice` (`postgres-external`) | `kubectl -n platform get svc,endpointslice postgres-external` |
| Valkey | `mng-valkey` on `infra_net` | `mng-valkey:6379` | `ExternalName Service` (`valkey-external -> host.k3d.internal`) | `kubectl -n platform get svc valkey-external -o yaml` |

- 민감정보(예: Valkey 비밀번호)는 Vault KV `secret/platform/argocd`의 `valkey_password`를 단일 소스로 사용한다.
- `bootstrap-local.sh`는 외부 런타임 기동을 수행하지 않으며, Vault/연동 리소스 검증과 ArgoCD 설치만 수행한다.

## Core Design

- **Component Boundary**:
  - infra layer: cluster/ingress/networkpolicy/argocd/eso
  - app layer: application workloads
- **Key Dependencies**:
  - k3s `v1.35.0+k3s1`, k3d `v5.8.3`, ArgoCD `v3.3.0`, Valkey `9.0.1`
- **Tech Stack**:
  - WSL2 Ubuntu, Docker Desktop, Helm, Kubernetes manifests

## Data Modeling & Storage Strategy

- Vault가 시크릿 원본 저장소
- ESO가 Kubernetes Secret로 동기화
- PostgreSQL/Valkey는 외부 데이터 서비스
- ArgoCD state backend는 external Valkey

## Interfaces & Data Structures

### Core Interfaces

```yaml
cluster:
  topology:
    servers: 1
    agents: 3
  k3sArgs:
    - "--disable=traefik"
externalServices:
  networkCIDR: "172.30.0.0/24"
  vault: "https://vault.127.0.0.1.nip.io"
  postgres: "172.30.0.11:5432"
  valkey: "mng-valkey:6379"
```

## API Contract (If Applicable)

본 기능은 별도 외부 API를 제공하지 않으며, Kubernetes CRD/리소스 계약을 사용한다.

## Agent Role & IO Contract (If Applicable)

- **Agent Role**: 문서/구성 생성 및 검증 자동화 보조
- **Inputs**: PRD/ARD/ADR/환경 제약
- **Outputs**: 명세/계획/작업/운영 문서 및 검증 증적
- **Success Definition**: 링크 무결성과 검증 시나리오 충족

## Tools & Tool Contract (If Applicable)

- **Tool List**: `kubectl`, `k3d`, `helm`, `argocd`, `docker`
- **Permission Boundary**: destructive 명령은 명시 승인 필요
- **Failure Handling**: 실패 시 runbook 경로로 에스컬레이션

## Prompt / Policy Contract (If Applicable)

- 정책 문서는 00.agent-governance 기준 준수
- 사람용 README는 한국어 유지

## Memory & Context Strategy (If Applicable)

- stage docs(01~09)를 단일 추적 체인으로 유지

## Guardrails (If Applicable)

- **Input Guardrails**: 버전/네트워크 값 검증
- **Output Guardrails**: 상대 링크/템플릿 필수 섹션 누락 금지
- **Blocked Conditions**: 평문 시크릿 커밋 금지
- **Escalation Rule**: 운영 보안 정책 완화 시 승인 필요

## Evaluation (If Applicable)

- **Eval Types**: 구조 검증, 연결성 검증, 정책 검증
- **Metrics**: 링크 오류 0, 핵심 체크 통과율 100%
- **Datasets / Fixtures**: 예시 manifest, external service mapping 표
- **How to Run**: task 문서의 검증 명령 참조

## Edge Cases & Error Handling

- PostgreSQL EndpointSlice IP 충돌 시 재할당 필요
- Vault auth role mismatch 시 ESO sync 실패
- ArgoCD external Valkey 연결 실패 시 ExternalName/네트워크 경로와 helm values/secret 재검증

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: ArgoCD Sync Degraded
- **Fallback**: manual sync + 이전 리비전 rollback
- **Human Escalation**: platform owner 승인 후 정책 조정

## Verification

```bash
k3d cluster list
kubectl get nodes
curl -ksS -o /dev/null -w '%{http_code}\n' https://vault.127.0.0.1.nip.io/v1/sys/health
kubectl -n platform get svc,endpointslice postgres-external
kubectl -n platform get svc valkey-external -o yaml
kubectl -n argocd get pods
kubectl -n external-secrets get externalsecret,secretstore,clustersecretstore
```

## Success Criteria & Verification Plan

- **VAL-SPC-001**: 4개 노드 Ready
- **VAL-SPC-002**: ArgoCD/ESO 핵심 컴포넌트 정상
- **VAL-SPC-003**: 외부 서비스(PostgreSQL EndpointSlice, Valkey ExternalName) 연결 확인
- **VAL-SPC-004**: Vault 기반 secret sync 성공

## Related Documents

- **Plan**: [`../../05.plans/2026-03-27-wsl-k3d-argocd-platform.md`](../../05.plans/2026-03-27-wsl-k3d-argocd-platform.md)
- **Tasks**: [`../../06.tasks/2026-03-27-wsl-k3d-argocd-platform.md`](../../06.tasks/2026-03-27-wsl-k3d-argocd-platform.md)
- **Runbook**: [`../../09.runbooks/0001-argocd-platform-bootstrap-runbook.md`](../../09.runbooks/0001-argocd-platform-bootstrap-runbook.md)
