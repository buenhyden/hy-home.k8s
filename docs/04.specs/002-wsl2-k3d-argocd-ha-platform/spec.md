# WSL2 k3d/k3s ArgoCD HA Platform Specification

## Overview (KR)

이 문서는 WSL2 멀티노드 클러스터와 GitOps/Secret/외부 데이터 연동 구현 계약을 정의한다. 운영 핫픽스(수동 EndpointSlice)와 재발 방지 백로그를 분리해 명시한다.

## Strategic Boundaries & Non-goals

- **Owns**: 클러스터 토폴로지, GitOps 배포 구조, 외부 서비스 인터페이스, 검증 스크립트
- **Does Not Own**: 외부 서비스 컨테이너 런타임 배포/운영

## Related Inputs

- **PRD**: [`../../01.prd/2026-03-28-wsl2-k3d-argocd-ha-platform.md`](../../01.prd/2026-03-28-wsl2-k3d-argocd-ha-platform.md)
- **ARD**: [`../../02.ard/0002-wsl2-k3d-argocd-ha-platform.md`](../../02.ard/0002-wsl2-k3d-argocd-ha-platform.md)
- **Related ADRs**: [`../../03.adr/0005-wsl2-ha-baseline-and-external-endpoint-contract.md`](../../03.adr/0005-wsl2-ha-baseline-and-external-endpoint-contract.md)

## Contracts

- **Config Contract**:
  - `infrastructure/k3d/k3d-cluster.yaml`: `servers: 1`, `agents: 3`
  - network CIDR: `172.30.0.0/24`
- **Data / Interface Contract**:
  - `vault-external.platform.svc.cluster.local:8200`
  - `postgres-write-external:15432`
  - `postgres-read-external:15433`
  - `valkey-external:26379`
  - Vault paths: `secret/platform/argocd`, `secret/platform/postgres-app`
- **Access / TLS Contract**:
  - 공식 ArgoCD host: `argocd.127.0.0.1.nip.io`
  - ingress TLS secret: `argocd-local-tls` (`kubernetes.io/tls`)
  - `ingress-nginx-controller` service type: `LoadBalancer`
  - 외부 Traefik 계약: `443 -> k3d :8443`
  - 운영 fallback: `https://argocd.127.0.0.1.nip.io:8443`
- **GitOps Source Gate Contract**:
  - root app source path: `gitops/apps/root`
  - root app revision: `main`
  - 로컬 파일 수정만으로는 반영되지 않으며, 원격 `main` 동기화가 선행되어야 함
- **Governance Contract**:
  - README 인덱스 즉시 갱신
  - 상대 경로 링크 추적성 유지

## Phase 0 Analysis Output (Brainstorming)

### Existing Asset Findings

- `gitops/apps/root/*`: App-of-Apps 루트 경로/브랜치 계약(`gitops/apps/root`, `main`) 유지 중.
- `gitops/platform/external-services/*`: PostgreSQL/Valkey/Vault 외부 인터페이스 모델 존재.
- `infrastructure/bootstrap-local.sh`: ArgoCD 초기화 및 기본 검증 경로 존재.
- `secrets/certs/*`: `cert.pem`, `key.pem`, `rootCA.pem` 경로 확인됨.

### Current Operational Risks

- Valkey 연동이 `ExternalName` 모델일 경우 ipBlock 기반 네트워크 정책과 정합성 문제가 발생할 수 있음.
- Vault 복구가 수동 EndpointSlice에 의존하는 구간이 있어 재발 방지 백로그가 필요함.
- AppProject의 과도한 와일드카드 화이트리스트(`*/*`)는 권한 경계 약화를 유발함.

### Version Baseline Validation (2026-03-28)

| Component | Baseline in Repo | Release Observation | Decision |
| --- | --- | --- | --- |
| k3s | `v1.35.0+k3s1` | `v1.35.2+k3s1` stable, `v1.35.3-rc1+k3s1` pre-release | 운영 baseline 유지, 차기 업그레이드 후보로 `1.35.2` 등록 |
| k3d | `v5.8.3` | `v5.8.3` latest stable (`v5.9.0-rc.0` pre-release) | 유지 |
| Valkey | `9.0.1` | `9.0.1` 최신 GA로 확인(문서 수집 시점 기준) | 유지 |

참고 릴리스 페이지:

- `https://github.com/k3s-io/k3s/releases`
- `https://github.com/k3d-io/k3d/releases`
- `https://github.com/valkey-io/valkey/releases`

### TLS Certificate Validation Rule

- `cert.pem` SAN은 최소 `argocd.127.0.0.1.nip.io` 또는 `*.127.0.0.1.nip.io`를 포함해야 한다.
- SAN 미포함 시 `secrets/certs` 기준으로 인증서를 재발급하고 `argocd-local-tls`를 재주입해야 한다.

## Core Design

- **Component Boundary**:
  - Cluster: k3d/k3s
  - GitOps: ArgoCD + ApplicationSet
  - Secrets: ESO + Vault Kubernetes auth role `eso-read-platform`
  - External data: PostgreSQL EndpointSlice, Valkey EndpointSlice
- **Key Dependencies**:
  - `kubectl`, `k3d`, `helm`, `argocd`
- **Tech Stack**:
  - WSL2 Ubuntu + Docker Desktop

## Data Modeling & Storage Strategy

- Vault가 시크릿 원본 저장소.
- ESO가 K8s Secret 생성/회전을 담당.
- ArgoCD Valkey 연결 비밀번호는 Vault 경로를 단일 소스로 사용.

## Interfaces & Data Structures

### Core Interfaces

```yaml
externalContracts:
  vault:
    dns: vault-external.platform.svc.cluster.local
    port: 8200
  postgres:
    write:
      service: postgres-write-external
      port: 15432
    read:
      service: postgres-read-external
      port: 15433
  valkey:
    service: valkey-external
    endpointSlice: valkey-external-1
    address: 172.30.0.12
    port: 26379
```

## API Contract (If Applicable)

해당 범위는 외부 HTTP API가 아닌 Kubernetes 리소스 계약을 중심으로 한다.

## Tools & Tool Contract (If Applicable)

- **Tool List**: `kubectl`, `argocd`, `helm`, shell scripts
- **Permission Boundary**: 파괴적 변경 금지, 운영 변경은 승인 후 수행
- **Failure Handling**: Runbook 0002 절차로 단계적 복구

## Guardrails (If Applicable)

- **Input Guardrails**: 고정 포트/경로/서비스명 계약 변경 시 ADR 선행
- **Output Guardrails**: 평문 시크릿 금지
- **Blocked Conditions**: 인증 토큰/비밀번호 문서 저장 금지
- **Escalation Rule**: Vault auth/policy 변경은 운영 승인 필요
- **Policy Hardening**:
  - AppProject는 allow-list 리소스만 허용
  - Vault policy는 `argocd`, `postgres-app` 경로만 허용

## Edge Cases & Error Handling

- `connect: connection refused` on Vault external endpoint
- EndpointSlice 누락/오타로 인한 Service 라우팅 실패
- ExternalSecret `SecretSyncedError`로 인한 ArgoCD backend 비밀 누락

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: `ClusterSecretStore Ready=False`
- **Fallback**: `EndpointSlice platform/vault-external-1` 수동 적용 후 상태 재평가
- **Human Escalation**: endpoint contract 자체 변경 필요 시 플랫폼 오너 승인

## Verification

```bash
./infrastructure/tests/run-all.sh
./infrastructure/tests/verify-cluster.sh
./infrastructure/tests/verify-gitops.sh
./infrastructure/tests/verify-secrets.sh
./infrastructure/tests/verify-external-services.sh
./infrastructure/tests/verify-network-policies.sh
./infrastructure/tests/verify-ingress-tls.sh
```

## Success Criteria & Verification Plan

- **VAL-SPC-001**: 4개 노드 Ready
- **VAL-SPC-002**: `vault-backend Ready=True`
- **VAL-SPC-003**: `argocd-external-valkey Ready=True`
- **VAL-SPC-004**: 포트 계약(8200/15432/15433/26379) 유지
- **VAL-SPC-005**: ingress/TLS 계약(host/secret/service type/HTTPS 접속) 유지

## Related Documents

- **Plan**: [`../../05.plans/2026-03-28-wsl2-k3d-argocd-ha-platform.md`](../../05.plans/2026-03-28-wsl2-k3d-argocd-ha-platform.md)
- **Tasks**: [`../../06.tasks/2026-03-28-wsl2-k3d-argocd-ha-platform.md`](../../06.tasks/2026-03-28-wsl2-k3d-argocd-ha-platform.md)
- **Runbook**: [`../../09.runbooks/0002-argocd-eso-vault-recovery-runbook.md`](../../09.runbooks/0002-argocd-eso-vault-recovery-runbook.md)
