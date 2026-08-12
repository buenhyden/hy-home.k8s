---
title: "Archive Record: WSL k3d/k3s ArgoCD Platform Technical Specification"
type: "content/archive"
status: "archived"
owner: "platform"
updated: "2026-06-02"
original_type: "spec"
original_path: "docs/03.specs/001-wsl-k3d-argocd-platform/spec.md"
archived_on: "2026-06-02"
archive_reason: "superseded"
replacement: "docs/03.specs/008-current-local-gitops-platform/spec.md"
source_commit: "5e0221525450dbdacb585e6c98ade3f060ddc827"
source_blob: "814a42d68c3fe7f78cd6bf274ef08dfe662bb159"
content_sha256: "eb482d1d5ebb3815746815f3dc868ff1669d79b9a1effca53fd7347f55447298"
---
<!-- archive-envelope:v1 payload=rest-of-file encoding=git-blob-bytes -->
---
title: 'WSL k3d/k3s ArgoCD Platform Technical Specification'
type: spec
status: historical
owner: platform
updated: 2026-05-22
---

# WSL k3d/k3s ArgoCD Platform Specification

## Overview (KR)

이 문서는 WSL2 기반 k3d(k3s) 플랫폼에서 ArgoCD GitOps, ESO+Vault, 외부 PostgreSQL/Valkey 연동을 구현하기 위한 기술 명세를 정의한다.

> **현재 실행계약 메모 (2026-05-22)**: 이 Spec은 초기 플랫폼 설계 기록이다. 현재 기본 컨테이너 런타임 전제는 WSL-native Docker이며, 역사적 Docker Desktop 표현은 당시 실행 기준으로만 해석한다. 현재 repo-backed 외부 서비스 실행계약은 `gitops/platform/external-services/`, `gitops/platform/network-policies/`, `infrastructure/tests/verify-contracts-static.sh`의 `172.18.x` EndpointSlice/CIDR 값이 우선한다.

## Implementation Status

이 초기 baseline Spec의 구현 범위는 현재 repo-backed 계약으로 흡수되었다. 구현 여부 판단은 이 문서의 과거 값이 아니라 아래 current-contract evidence를 우선한다.

| Area | Current implementation evidence | Verification boundary |
| --- | --- | --- |
| k3d 1+3 topology | `infrastructure/k3d/k3d-cluster.yaml` | Static review plus `infrastructure/tests/verify-cluster.sh` for live clusters |
| ArgoCD App-of-Apps | `gitops/clusters/local/root-application.yaml`, `gitops/apps/root/kustomization.yaml` | `bash scripts/validate-gitops-structure.sh` |
| ingress/TLS | `infrastructure/argocd/values-local.yaml`, `gitops/apps/root/platform-ingress-nginx-app.yaml` | `bash infrastructure/tests/verify-contracts-static.sh`; live TLS evidence via `verify-ingress-tls.sh` |
| ESO/Vault/external data services | `gitops/platform/eso/`, `gitops/platform/external-services/`, `gitops/platform/network-policies/` | static contracts and live `verify-secrets.sh` / `verify-external-services.sh` |
| docs lifecycle | `docs/04.execution/plans/2026-03-27-wsl-k3d-argocd-platform.md`, `docs/04.execution/tasks/2026-03-27-wsl-k3d-argocd-platform.md` | Historical closure record; current work uses later active specs and tasks |

## Strategic Boundaries & Non-goals

- Owns: 클러스터 토폴로지, GitOps 경계, 외부 서비스 인터페이스, 보안 기본 통제.
- Non-goals: 애플리케이션 비즈니스 로직, 클라우드 프로덕션 인프라 자동화.

## Related Inputs

- **PRD**: [`../../01.requirements/2026-03-27-wsl-k3d-argocd-platform.md`](../../01.requirements/2026-03-27-wsl-k3d-argocd-platform.md)
- **ARD**: [`../../02.architecture/requirements/0001-wsl-k3d-argocd-platform.md`](../../02.architecture/requirements/0001-wsl-k3d-argocd-platform.md)
- **Related ADRs**: [`../../02.architecture/decisions/0001-k3d-topology-and-network.md`](../../02.architecture/decisions/0001-k3d-topology-and-network.md), [`../../02.architecture/decisions/0002-argocd-helm-and-gitops-model.md`](../../02.architecture/decisions/0002-argocd-helm-and-gitops-model.md), [`../../02.architecture/decisions/0003-eso-vault-k8s-auth.md`](../../02.architecture/decisions/0003-eso-vault-k8s-auth.md), [`../../02.architecture/decisions/0004-external-services-endpoints-and-valkey-backend.md`](../../02.architecture/decisions/0004-external-services-endpoints-and-valkey-backend.md)

## Contracts

- **Config Contract**:
  - k3d: `servers=1`, `agents=3`, server arg `--disable=traefik`
  - External integration network(CIDR): `172.30.0.0/24`
  - Fixed IP: PostgreSQL `.11`
  - Vault/Valkey: 외부 관리형 엔드포인트 사용
- **Data / Interface Contract**:
  - K8s Service names: `postgres-write-external`, `postgres-read-external`, `valkey-external`
  - PostgreSQL은 HAProxy write/read 포트를 각각 EndpointSlice로 외부 고정 IP에 매핑
  - Valkey는 ExternalName Service(`host.k3d.internal`)로 외부 관리형 인스턴스에 매핑
- **Governance Contract**:
  - 현재 docs taxonomy 추적성 유지
  - README 인덱스 동기화 필수
  - 외부 서비스 런타임은 별도 워크스페이스(repo)에서 관리

## External Runtime Integration (Required)

외부 서비스는 이 저장소에서 기동하지 않는다. 이 저장소는 Kubernetes 매핑/연동 계약만 관리한다.

| 서비스 | 외부 런타임(별도 repo) | 필수 접속값 | 이 저장소 연동 방식 | 기본 확인 |
| --- | --- | --- | --- | --- |
| Vault | `vault`, `vault-agent` on `infra_net` | `https://vault.127.0.0.1.nip.io` | ESO + Vault Kubernetes auth | `curl -ksS -o /dev/null -w '%{http_code}\n' https://vault.127.0.0.1.nip.io/v1/sys/health` |
| PostgreSQL | HAProxy-backed external DB runtime | `172.30.0.11:15432`(write), `172.30.0.11:15433`(read) | `Service + EndpointSlice` (`postgres-write-external`, `postgres-read-external`) | `kubectl -n platform get svc,endpointslice \| rg 'postgres-(write\|read)-external'` |
| Valkey | `mng-valkey` on `infra_net` | `host.k3d.internal:26379` (`mng-valkey:6379` published) | `ExternalName Service` (`valkey-external -> host.k3d.internal`) | `kubectl -n platform get svc valkey-external -o yaml` |

- 민감정보(예: Valkey 비밀번호)는 Vault KV `secret/platform/argocd`의 `valkey_password`를 단일 소스로 사용한다.
- 서비스용 PostgreSQL 접근 정보(`app_db`, `app_user`, 비밀번호)는 평문 커밋 없이 Vault 경로에서 관리한다.
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
  postgresWrite: "172.30.0.11:15432"
  postgresRead: "172.30.0.11:15433"
  valkey: "host.k3d.internal:26379"
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

- current docs taxonomy를 단일 추적 체인으로 유지

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

## Verification Commands

```bash
k3d cluster list
kubectl get nodes
curl -ksS -o /dev/null -w '%{http_code}\n' https://vault.127.0.0.1.nip.io/v1/sys/health
kubectl -n platform get svc,endpointslice | rg 'postgres-(write|read)-external'
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

- **PRD**: [`../../01.requirements/2026-03-27-wsl-k3d-argocd-platform.md`](../../01.requirements/2026-03-27-wsl-k3d-argocd-platform.md)
- **ARD**: [`../../02.architecture/requirements/0001-wsl-k3d-argocd-platform.md`](../../02.architecture/requirements/0001-wsl-k3d-argocd-platform.md)
- **Related ADRs**: [`../../02.architecture/decisions/0001-k3d-topology-and-network.md`](../../02.architecture/decisions/0001-k3d-topology-and-network.md), [`../../02.architecture/decisions/0002-argocd-helm-and-gitops-model.md`](../../02.architecture/decisions/0002-argocd-helm-and-gitops-model.md), [`../../02.architecture/decisions/0003-eso-vault-k8s-auth.md`](../../02.architecture/decisions/0003-eso-vault-k8s-auth.md), [`../../02.architecture/decisions/0004-external-services-endpoints-and-valkey-backend.md`](../../02.architecture/decisions/0004-external-services-endpoints-and-valkey-backend.md)
- **Plan**: [`../../04.execution/plans/2026-03-27-wsl-k3d-argocd-platform.md`](../../04.execution/plans/2026-03-27-wsl-k3d-argocd-platform.md)
- **Tasks**: [`../../04.execution/tasks/2026-03-27-wsl-k3d-argocd-platform.md`](../../04.execution/tasks/2026-03-27-wsl-k3d-argocd-platform.md)
- **Runbook**: [`../../05.operations/runbooks/0001-argocd-platform-bootstrap-runbook.md`](../../05.operations/runbooks/0001-argocd-platform-bootstrap-runbook.md)
