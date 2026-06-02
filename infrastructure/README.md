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

이 표는 `infrastructure/`의 현재 bootstrap/runtime-support entrypoint와
운영 책임을 연결한다. `validate-repo-quality-gates.sh`는 이 표가 실제
`argocd/`, `k3d/`, `tests/`, `vault/`, `bootstrap-local.sh`,
`ipaddresspool.yaml`, `l2advertisement.yaml` 표면과 동기화되어 있는지
검증한다.

| Area | Purpose and owner | Lifecycle and config | Dependencies, routes, secrets | Validation and operations |
| --- | --- | --- | --- | --- |
| `argocd/` | Local ArgoCD Helm values owned by platform maintainers. | Bootstrap-time values for ingress, TLS, and external Valkey integration. | Depends on k3d, ingress, mkcert CA, external Valkey, and Vault-backed secret flow. | Validate with `bash infrastructure/tests/verify-contracts-static.sh`; live state requires ArgoCD and ingress/TLS checks. |
| `k3d/` | Local cluster configuration owned by platform maintainers. | Defines local k3d cluster shape and port exposure. | Depends on WSL2, WSL-native Docker, k3d, and local network conventions. | Validate by static review and live `infrastructure/tests/verify-cluster.sh` when a cluster is available. |
| `tests/` | Static and live validation scripts owned by platform/ops maintainers. | Includes static contracts plus cluster, GitOps, external service, ingress/TLS, network policy, and secret verification. | Static tests require local files; live tests require a bootstrapped k3d/ArgoCD environment and external services. | Run `verify-contracts-static.sh` in CI-capable contexts; run `run-all.sh` only for intentional live validation. |
| `vault/` | Vault policy samples owned by platform/security maintainers. | Stores least-privilege policy material for ESO read access. | Depends on external Vault runtime and approved secret paths; never stores secret values. | Validate policy expectations through static contracts; live policy state requires external Vault verification. |
| `bootstrap-local.sh` | Local bootstrap entrypoint owned by platform maintainers. | Creates initial namespace, secret, MetalLB, and root GitOps application before ArgoCD owns desired state. | Depends on exported `VAULT_TOKEN`, kubectl context, k3d, Helm, Vault, and local certificates. | Validate shell syntax and bootstrap runbook alignment; execution is human-approved bootstrap work, not normal agent mutation. |
| `ipaddresspool.yaml` and `l2advertisement.yaml` | MetalLB bootstrap manifests owned by platform maintainers. | Bootstrap-time LoadBalancer address pool and L2 advertisement. | Depends on local network range and MetalLB controller. | Validate manifests statically; live behavior requires cluster networking checks. |

## WSL2 Runtime Prerequisite Matrix

이 표는 WSL2 + WSL Linux native Docker + k3d live validation을 시작하기 전
확인해야 하는 runtime 전제를 모은다. 정적 검증은 이 표의 SSoT와 failure
boundary를 확인하지만, kubeconfig repair나 live cluster mutation을 자동으로
수행하지 않는다.

| Prerequisite | Repository SSoT | Owner / responsibility | Validation / evidence | Failure boundary |
| --- | --- | --- | --- | --- |
| `WSL2 shell and Docker context` | WSL2 Ubuntu shell with WSL-native Docker; Docker context must be checked from inside WSL. | Operator owns local Docker daemon/context and external runtime startup. | Run `docker context show` and confirm Docker commands work from WSL before bootstrap. | Wrong Docker context or Docker Desktop-only context blocks bootstrap; this repository records the blocker and does not switch contexts automatically. |
| `kubectl and k3d context` | Local cluster name and kubectl context are `k3d-hyhome`; cluster shape lives in `k3d/k3d-cluster.yaml`. | Operator owns cluster creation/reuse through `bootstrap-local.sh` and k3d. | Run `k3d cluster list` and `kubectl config current-context`; live proof uses `infrastructure/tests/verify-cluster.sh`. | Missing cluster or wrong context blocks live validation; static gates remain valid. |
| `kubeconfig and TLS trust` | Default kubeconfig is `~/.kube/config` unless `KUBECONFIG` is intentionally set for a temporary check. | Operator owns kubeconfig CA trust and context repair. | `kubectl version --request-timeout=5s` must reach the API server; `x509: certificate signed by unknown authority` is a TLS trust blocker. | TLS trust repair is an operator action, not an automatic doc/static-gate side effect. |
| `Port and network contracts` | Current local contracts are ingress-nginx LoadBalancer `172.18.0.240:443`, Valkey `172.18.0.9:6379`, and PostgreSQL HAProxy `172.18.0.15:15432/15433`. | External service workspace owns service containers and addresses; this repository owns Kubernetes interface contracts. | Static proof comes from `verify-contracts-static.sh`; live proof uses `run-all.sh` after bootstrap. | Port conflicts or stale addresses block runtime checks and require external-service or bootstrap follow-up. |
| `WSL networking constraints` | Local UI routes use `127.0.0.1.nip.io` hostnames and Traefik dynamic configs target the k3d ingress-nginx backend. | Operator owns Windows/WSL networking, host reachability, and optional external Traefik gateway. | Validate dynamic config statically; live Traefik 443 checks are explicit runtime validation. | Windows portproxy, firewall, or external gateway state is outside repo-static ownership. |

## Bootstrap Boundary Matrix

이 표는 bootstrap-only 예외와 정상 GitOps 운영 경계를 분리한다. 정적 검증은
이 경계가 문서화되어 있는지 확인하지만, k3d 생성, ArgoCD 설치, root app
적용, Vault auth refresh, 외부 DB/Valkey runtime 관리를 자동 수행하지 않는다.

| Boundary | Repository responsibility | Operator / external responsibility | Allowed command surface | Verification / evidence | Failure boundary |
| --- | --- | --- | --- | --- | --- |
| `k3d cluster creation` | Owns `k3d/k3d-cluster.yaml`, bootstrap prechecks, and documented `k3d-hyhome` context contract. | Operator owns WSL2 shell, WSL-native Docker context, port availability, and the human-approved bootstrap run. | `./bootstrap-local.sh` may call `k3d cluster create` during bootstrap-only execution. | Static README guardrails plus `k3d cluster list`, `kubectl config current-context`, and live `infrastructure/tests/verify-cluster.sh`. | Repo-static checks do not create, delete, or repair clusters; wrong Docker/kubectl context remains operator-owned. |
| `ArgoCD installation` | Owns `argocd/values-local.yaml`, bootstrap script install flow, and ArgoCD ingress/TLS configuration contract. | Operator owns Helm/kubectl execution, certificate inputs, and approved bootstrap timing. | `./bootstrap-local.sh` may run `helm upgrade --install` for ArgoCD before GitOps ownership is established. | `bash infrastructure/tests/verify-contracts-static.sh`; live `infrastructure/tests/verify-gitops.sh` after bootstrap. | Agents do not directly install or upgrade ArgoCD outside approved bootstrap/break-glass evidence. |
| `root app application` | Owns `gitops/clusters/local/root-application.yaml`, `gitops/apps/root`, and App-of-Apps source path/branch contracts. | Operator owns the first root app apply and any approved recovery action before ArgoCD reconciliation is healthy. | `./bootstrap-local.sh` may run `kubectl apply` for the root GitOps Application as a bootstrap-only exception. | `bash scripts/validate-gitops-structure.sh`; live `infrastructure/tests/verify-gitops.sh` after bootstrap. | Steady-state app changes stay in Git PRs and ArgoCD reconciliation; direct apply is not normal operation. |
| `Vault connection contract` | Owns `gitops/platform/external-services/vault-external.yaml`, `gitops/platform/eso/vault-secret-store.yaml`, Vault policy sample, and no-secret static checks. | External Vault operator owns Vault runtime, unseal, token handling, auth mount configuration, policy application, and secret rotation. | Bootstrap may perform metadata/no-value Vault readiness checks and approved auth setup; secret values are not printed or committed. | `bash infrastructure/tests/verify-contracts-static.sh`; `bash scripts/check-secret-handling.sh .`; live `infrastructure/tests/verify-secrets.sh`. | Repo-static checks do not read secret values, write Vault policy, refresh Vault auth, or repair live Vault state. |
| `PostgreSQL and Valkey connection contract` | Owns Kubernetes Service/EndpointSlice contracts, ExternalSecret target naming, and static port/address checks for PostgreSQL and Valkey. | External service workspace owns PostgreSQL/Valkey runtime, container/network state, credentials, TLS/CA material if enabled, and rotation evidence. | Bootstrap may run TCP reachability prechecks and create the initial ArgoCD Valkey Secret from approved Vault source. | `bash infrastructure/tests/verify-contracts-static.sh`; live `infrastructure/tests/verify-external-services.sh` and `infrastructure/tests/verify-secrets.sh`. | Repo-static checks do not start external services, change `.env` values, rotate credentials, or prove live reachability. |

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

- [PRD](../docs/01.requirements/2026-06-02-current-local-gitops-platform.md)
- [Spec](../docs/03.specs/008-current-local-gitops-platform/spec.md)
- [Runbook](../docs/05.operations/runbooks/0001-argocd-platform-bootstrap-runbook.md)
- [GitOps README](../gitops/README.md)
- [Tech Stack Version Inventory](../docs/90.references/versions/tech-stack-version-inventory.md)

## Validation Note

`infrastructure/tests/`에는 두 종류의 검증 스크립트가 있다.

- **정적 검증 (CI 실행 가능)**: `verify-contracts-static.sh` — live cluster 없이 실행되며 CI `manifest-static` 잡에서 자동으로 실행된다.
- **라이브 검증 (k3d 클러스터 필요)**: `verify-cluster.sh`, `verify-gitops.sh`, `verify-external-services.sh`, `verify-ingress-tls.sh`, `verify-network-policies.sh`, `verify-secrets.sh`, `run-all.sh` — 실행 전 k3d 클러스터가 부트스트랩되어 있어야 한다.

기본 `run-all.sh`는 ingress-nginx LoadBalancer fallback 경로를 검증한다.
외부 Traefik 443 증명은 `CHECK_TRAEFIK_443=true`를 명시한 별도 live check이며,
Docker에 외부 Traefik gateway 컨테이너가 없으면 `hy-home.docker` runtime 또는
dynamic config 반영 증거가 부족한 상태로 기록한다.

`run-all.sh`가 첫 단계에서 `kubectl cannot reach cluster`로 실패하면
클러스터가 없거나 kubeconfig/context/TLS trust가 맞지 않는 상태다. 특히
`x509: certificate signed by unknown authority`는 kubeconfig CA trust repair가
필요한 runtime blocker이며, 문서/정적 검증 pass에서 자동으로 고치지 않는다.

기본 kubeconfig가 TLS trust 문제로 막히는지, 클러스터 자체가 실패하는지
분리해야 할 때는 k3d가 출력한 임시 kubeconfig를 `/tmp`에 두고
`KUBECONFIG=/tmp/<file> bash infrastructure/tests/run-all.sh`로 read-only live
검증을 실행한다. 이 방식은 `~/.kube/config`를 수정하지 않으며, 통과하더라도
기본 kubeconfig repair가 완료됐다는 뜻은 아니다.

승인된 기본 kubeconfig repair에서는 먼저 `~/.kube/config`를 백업한 뒤
`k3d kubeconfig merge hyhome --kubeconfig-merge-default --kubeconfig-switch-context`를
실행한다. repair 후 `kubectl version --request-timeout=5s`와
`bash infrastructure/tests/run-all.sh`가 기본 kubeconfig로 통과해야 하며,
rollback은 백업 파일을 `~/.kube/config`로 되돌리는 방식이다.

## Bootstrap Note

- 실행 전 `VAULT_TOKEN`을 반드시 export 해야 한다.
- `./bootstrap-local.sh`는 Vault KV(`secret/platform/argocd`)의 `valkey_password`를 유일한 소스로 사용한다.
- 외부 서비스(Vault/PostgreSQL/Valkey)는 별도 워크스페이스(repo)에서 관리한다.
- `./bootstrap-local.sh`의 `kubectl apply`는 ArgoCD 소유권이 생기기 전 초기 namespace, secret, MetalLB, root GitOps application 생성을 위한 bootstrap-only 예외다. 정상 운영 변경은 GitOps PR과 ArgoCD reconciliation으로 처리한다.
