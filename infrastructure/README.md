# infrastructure

> WSL2 + k3d + 외부 서비스 연동 기반 로컬 플랫폼 인프라 자산을 관리한다.

## Overview

이 디렉터리는 로컬 Kubernetes 플랫폼 부트스트랩에 필요한 인프라 설정을 담는다. WSL2/Docker Desktop/k3d 클러스터, 외부 서비스 연동 계약, ArgoCD 설치 값 파일, bootstrap 검증 스크립트, 정적 계약 테스트를 포함한다.

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
| `k3d/` | Local cluster configuration owned by platform maintainers. | Defines local k3d cluster shape and port exposure. | Depends on WSL2, Docker Desktop, k3d, and local network conventions. | Validate by static review and live `infrastructure/tests/verify-cluster.sh` when a cluster is available. |
| `tests/` | Static and live validation scripts owned by platform/ops maintainers. | Includes static contracts plus cluster, GitOps, external service, ingress/TLS, network policy, and secret verification. | Static tests require local files; live tests require a bootstrapped k3d/ArgoCD environment and external services. | Run `verify-contracts-static.sh` in CI-capable contexts; run `run-all.sh` only for intentional live validation. |
| `vault/` | Vault policy samples owned by platform/security maintainers. | Stores least-privilege policy material for ESO read access. | Depends on external Vault runtime and approved secret paths; never stores secret values. | Validate policy expectations through static contracts; live policy state requires external Vault verification. |
| `bootstrap-local.sh` | Local bootstrap entrypoint owned by platform maintainers. | Creates initial namespace, secret, MetalLB, and root GitOps application before ArgoCD owns desired state. | Depends on exported `VAULT_TOKEN`, kubectl context, k3d, Helm, Vault, and local certificates. | Validate shell syntax and bootstrap runbook alignment; execution is human-approved bootstrap work, not normal agent mutation. |
| `ipaddresspool.yaml` and `l2advertisement.yaml` | MetalLB bootstrap manifests owned by platform maintainers. | Bootstrap-time LoadBalancer address pool and L2 advertisement. | Depends on local network range and MetalLB controller. | Validate manifests statically; live behavior requires cluster networking checks. |

## How to Work in This Area

1. bootstrap 전 [Runbook](../docs/05.operations/runbooks/0001-argocd-platform-bootstrap-runbook.md)의 외부 의존성 점검을 확인한다.
2. `bootstrap-local.sh` 변경 시 bootstrap-only 예외 범위와 GitOps 소유권 전환 지점을 함께 점검한다.
3. Helm values, k3d config, static test 변경은 관련 Spec/Operations/Runbook 링크를 함께 갱신한다.
4. 변경 후 `bash infrastructure/tests/verify-contracts-static.sh`와 shell syntax check를 실행한다.

## Related References

- [PRD](../docs/01.requirements/2026-03-27-wsl-k3d-argocd-platform.md)
- [Spec](../docs/03.specs/001-wsl-k3d-argocd-platform/spec.md)
- [Runbook](../docs/05.operations/runbooks/0001-argocd-platform-bootstrap-runbook.md)
- [GitOps README](../gitops/README.md)
- [Tech Stack Version Inventory](../docs/90.references/versions/tech-stack-version-inventory.md)

## Validation Note

`infrastructure/tests/`에는 두 종류의 검증 스크립트가 있다.

- **정적 검증 (CI 실행 가능)**: `verify-contracts-static.sh` — live cluster 없이 실행되며 CI `manifest-static` 잡에서 자동으로 실행된다.
- **라이브 검증 (k3d 클러스터 필요)**: `verify-cluster.sh`, `verify-gitops.sh`, `verify-external-services.sh`, `verify-ingress-tls.sh`, `verify-network-policies.sh`, `verify-secrets.sh`, `run-all.sh` — 실행 전 k3d 클러스터가 부트스트랩되어 있어야 한다.

## Bootstrap Note

- 실행 전 `VAULT_TOKEN`을 반드시 export 해야 한다.
- `./bootstrap-local.sh`는 Vault KV(`secret/platform/argocd`)의 `valkey_password`를 유일한 소스로 사용한다.
- 외부 서비스(Vault/PostgreSQL/Valkey)는 별도 워크스페이스(repo)에서 관리한다.
- `./bootstrap-local.sh`의 `kubectl apply`는 ArgoCD 소유권이 생기기 전 초기 namespace, secret, MetalLB, root GitOps application 생성을 위한 bootstrap-only 예외다. 정상 운영 변경은 GitOps PR과 ArgoCD reconciliation으로 처리한다.
