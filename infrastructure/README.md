# infrastructure

> WSL2 + k3d + 외부 서비스 연동 기반 로컬 플랫폼 인프라 자산을 관리한다.

## Overview

이 디렉터리는 로컬 Kubernetes 플랫폼 부트스트랩에 필요한 인프라 설정을 담는다. WSL2/WSL-native Docker/k3d 클러스터, 외부 서비스 연동 계약, ArgoCD 설치 값 파일, bootstrap 검증 스크립트, 정적 계약 테스트를 포함한다.

이 경로는 로컬 k3d 플랫폼을 만들기 위한 실행 자산을 보관하지만, 정상 운영 변경은 `gitops/` 선언과 ArgoCD reconciliation을 통해 처리한다.

MetalLB bootstrap manifest는 별도 `metallb/` 디렉터리가 아니라 이 디렉터리 루트의 `ipaddresspool.yaml`, `l2advertisement.yaml` 두 파일로 관리한다.

## Audience

이 README의 주요 독자:

- Operators
- Platform Engineers
- Documentation Writers
- AI Agents

## Scope

### In Scope

- k3d 클러스터 설정과 bootstrap 스크립트
- ArgoCD Helm values와 초기 GitOps 연결 자산
- MetalLB/EndpointSlice 같은 로컬 외부 서비스 연결 manifest
- repo-backed 정적 검증 스크립트와 계약 테스트

### Out of Scope

- 외부 Vault/PostgreSQL/Valkey 런타임 자체 생성
- AWS/Azure 실제 cloud 리소스 프로비저닝
- 애플리케이션 워크로드 매니페스트
- 정상 운영 변경을 위한 live cluster mutation

## Structure

```text
infrastructure/
├── argocd/                  # ArgoCD Helm values
├── k3d/                     # k3d 클러스터 설정
├── tests/                   # 정적 계약 검증 스크립트 및 라이브 클러스터 검증 스크립트
├── vault/                   # Vault 정책 샘플
├── bootstrap-local.sh       # 로컬 플랫폼 bootstrap 진입점
├── ipaddresspool.yaml       # MetalLB 로컬 LoadBalancer 주소 풀
├── l2advertisement.yaml     # MetalLB L2 advertisement
└── README.md                # This file
```

## Infrastructure Coverage Matrix

| Area | Purpose and owner | Lifecycle and config | Dependencies, routes, secrets | Validation and operations |
| --- | --- | --- | --- | --- |
| `argocd/` | Local ArgoCD Helm values owned by platform maintainers. | Bootstrap-time values for ingress, TLS, and external Valkey integration. | Depends on k3d, ingress, mkcert CA, external Valkey, and Vault-backed secret flow. | Validate with `bash infrastructure/tests/verify-contracts-static.sh`; live state requires ArgoCD and ingress/TLS checks. |
| `k3d/` | Local cluster configuration owned by platform maintainers. | Defines local k3d cluster shape and port exposure. | Depends on WSL2, WSL-native Docker, k3d, and local network conventions. | Validate by static review and live `infrastructure/tests/verify-cluster.sh` when a cluster is available. |
| `tests/` | Static and live validation scripts owned by platform/ops maintainers. | Includes static contracts plus cluster, GitOps, external service, ingress/TLS, network policy, and secret verification. | Static tests require local files; live tests require a bootstrapped k3d/ArgoCD environment and external services. | Run `verify-contracts-static.sh` in CI-capable contexts; run `run-all.sh` only for intentional live validation. |
| `vault/` | Vault policy samples owned by platform/security maintainers. | Stores least-privilege policy material for ESO read access. | Depends on external Vault runtime and approved secret paths; never stores secret values. | Validate policy expectations through static contracts; live policy state requires external Vault verification. |
| `bootstrap-local.sh` | Local bootstrap entrypoint owned by platform maintainers. | Creates initial namespace, secret, MetalLB, and root GitOps application before ArgoCD owns desired state. | Depends on exported `VAULT_TOKEN`, kubectl context, k3d, Helm, Vault, and local certificates. | Validate shell syntax and bootstrap runbook alignment; execution is human-approved bootstrap work, not normal agent mutation. |
| `ipaddresspool.yaml` and `l2advertisement.yaml` | MetalLB bootstrap manifests owned by platform maintainers. | Bootstrap-time LoadBalancer address pool and L2 advertisement. | Depends on local network range and MetalLB controller. | Validate manifests statically; live behavior requires cluster networking checks. |

## Infrastructure Test Inventory

이 표는 `infrastructure/tests/*.sh`의 현재 유지 계약이다. 정적 검증은 CI에서
실행할 수 있고, 라이브 검증은 의도적으로 부트스트랩된 k3d/ArgoCD 환경에서만
실행한다.

| Test script | Type | Preconditions | Result semantics | Retention / command surface |
| --- | --- | --- | --- | --- |
| `verify-contracts-static.sh` | Static | Local repository files only; no live cluster or secret value access. | PASS means declared GitOps, Vault policy, AppProject, external service, and sample contracts match the static repository contract. | Tier A: CI `manifest-static`, PR checklist, root README, and this README. |
| `verify-cluster.sh` | Live | Bootstrapped k3d context, trusted kubeconfig CA, kubectl, and MetalLB. | PASS means cluster node topology and MetalLB readiness match the local platform baseline. | Tier B: called by `run-all.sh`; documented in bootstrap runbook and this README. |
| `verify-gitops.sh` | Live | Reachable ArgoCD namespace and synchronized root/platform applications. | PASS means the live root Application source contract and required platform Application presence checks pass. | Tier B: called by `run-all.sh`; documented in bootstrap runbook and this README. |
| `verify-secrets.sh` | Live | External Secrets Operator, Vault auth, and ArgoCD external Valkey secret flow are bootstrapped. | PASS means `vault-backend` and `argocd-external-valkey` live readiness contracts pass. | Tier B: called by `run-all.sh`; documented in bootstrap runbook and this README. |
| `verify-external-services.sh` | Live | Platform namespace services and EndpointSlices exist for external PostgreSQL, Vault, Valkey, and observability contracts. | PASS means live service ports and EndpointSlice addresses match the declared local contracts. | Tier B: called by `run-all.sh`; documented in bootstrap runbook and this README. |
| `verify-network-policies.sh` | Live | NetworkPolicy resources are reconciled in platform, argocd, external-secrets, and istio-system namespaces. | PASS means required live egress NetworkPolicy contracts match the expected CIDR and port checks. | Tier B: called by `run-all.sh`; documented in bootstrap runbook and this README. |
| `verify-ingress-tls.sh` | Live | ingress-nginx LoadBalancer, ArgoCD ingress/TLS secret, curl, rg, and optional Traefik check inputs are available. | PASS means live ingress/TLS and fallback endpoint checks return the expected contracts. | Tier B: called by `run-all.sh`; documented in bootstrap runbook and this README. |
| `run-all.sh` | Live aggregate | All live-test preconditions above are satisfied. | PASS means every live verification script in this inventory completed successfully. | Tier B: canonical live validation entrypoint in this README and SDD verification records. |

## How to Work in This Area

1. bootstrap 전 [Runbook](../docs/05.operations/runbooks/0001-argocd-platform-bootstrap-runbook.md)의 외부 의존성 점검을 확인한다.
2. `bootstrap-local.sh` 변경 시 bootstrap-only 예외 범위와 GitOps 소유권 전환 지점을 함께 점검한다.
3. Helm values, k3d config, static test 변경은 관련 Spec/Operations/Runbook 링크를 함께 갱신한다.
4. 변경 후 `bash infrastructure/tests/verify-contracts-static.sh`와 shell syntax check를 실행한다.
5. `infrastructure/tests/*.sh`를 추가, 삭제, 리네임, 통합할 때는 이 README의
   Infrastructure Test Inventory와 `run-all.sh` 호출 목록을 함께 갱신한다.

## Link Basis

이 README의 링크 기준 위치는 `infrastructure/`다.

- 같은 폴더의 파일과 하위 경로는 현재 README 위치 기준 상대 링크로 연결한다.
- 상위 저장소 문서나 다른 stage 문서는 필요한 만큼 `../`로 올라가서 연결한다.
- 다른 README의 상대 링크를 그대로 복사하지 말고, 이 파일 위치 기준으로 다시 계산한다.

## Related Documents

- [PRD](../docs/01.requirements/2026-03-27-wsl-k3d-argocd-platform.md)
- [Spec](../docs/03.specs/001-wsl-k3d-argocd-platform/spec.md)
- [Runbook](../docs/05.operations/runbooks/0001-argocd-platform-bootstrap-runbook.md)
- [GitOps README](../gitops/README.md)
- [Tech Stack Version Inventory](../docs/90.references/versions/tech-stack-version-inventory.md)

## Validation Note

`infrastructure/tests/`에는 두 종류의 검증 스크립트가 있다.

- **정적 검증 (CI 실행 가능)**: `verify-contracts-static.sh` — live cluster 없이 실행되며 CI `manifest-static` 잡에서 자동으로 실행된다.
- **라이브 검증 (k3d 클러스터 필요)**: `verify-cluster.sh`, `verify-gitops.sh`, `verify-external-services.sh`, `verify-ingress-tls.sh`, `verify-network-policies.sh`, `verify-secrets.sh`, `run-all.sh` — 실행 전 k3d 클러스터가 부트스트랩되어 있어야 한다.

`run-all.sh`가 첫 단계에서 `kubectl cannot reach cluster`로 실패하면
클러스터가 없거나 kubeconfig/context/TLS trust가 맞지 않는 상태다. 특히
`x509: certificate signed by unknown authority`는 kubeconfig CA trust repair가
필요한 runtime blocker이며, 문서/정적 검증 pass에서 자동으로 고치지 않는다.

## Bootstrap Note

- 실행 전 `VAULT_TOKEN`을 반드시 export 해야 한다.
- `./bootstrap-local.sh`는 Vault KV(`secret/platform/argocd`)의 `valkey_password`를 유일한 소스로 사용한다.
- 외부 서비스(Vault/PostgreSQL/Valkey)는 별도 워크스페이스(repo)에서 관리한다.
- `./bootstrap-local.sh`의 `kubectl apply`는 ArgoCD 소유권이 생기기 전 초기 namespace, secret, MetalLB, root GitOps application 생성을 위한 bootstrap-only 예외다. 정상 운영 변경은 GitOps PR과 ArgoCD reconciliation으로 처리한다.
