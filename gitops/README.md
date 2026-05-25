# gitops

> ArgoCD App-of-Apps 기반으로 로컬 클러스터 desired state를 선언형 관리한다.

## Overview

이 디렉터리는 ArgoCD가 동기화할 GitOps 리소스를 포함한다. 프로젝트 경계(AppProject), ApplicationSet, 루트 애플리케이션, 플랫폼 리소스, 워크로드 리소스를 분리해 로컬 k3d 클러스터의 desired state를 추적한다.

정상 운영 변경은 feature branch에서 매니페스트를 수정하고 PR review 이후 ArgoCD reconciliation으로 반영한다. live cluster를 직접 변경하는 명령은 bootstrap-only 또는 break-glass 맥락이 명시된 경우에만 문서화한다.

현재 구현 범위는 `clusters/local`의 bootstrap/AppProject/ApplicationSet, `apps/root`의 플랫폼 Application 선언, `platform/*`의 공통 컴포넌트, `workloads/adminer`의 앱 패턴 참조 구현이다.

`platform/external-services`의 `Service`와 `EndpointSlice` 파일은 외부
Vault/PostgreSQL/Valkey/Observability 연결의 Git desired state SSoT다.
ArgoCD resource exclusion 또는 runtime drift 때문에 직접 EndpointSlice
patch/apply가 필요한 경우에도 이는 human-approved break-glass 예외이며,
실행 후 실제 endpoint 값을 Git과 운영 증적에 되돌려 맞춰야 한다.

## Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

## Scope

### In Scope

- ArgoCD AppProject, ApplicationSet, Application 리소스
- 플랫폼 공통 리소스와 워크로드 매니페스트
- 로컬 k3d 클러스터의 GitOps desired state
- 앱 온보딩을 위한 `gitops/workloads/` 구조

### Out of Scope

- k3d 클러스터 생성과 ArgoCD 설치 스크립트
- 외부 Vault/PostgreSQL/Valkey 런타임 자체 운영
- AWS/Azure 실제 cloud 리소스 프로비저닝
- live cluster mutation을 기본 운영 경로로 안내하는 문서

## Structure

```text
gitops/
├── clusters/local/          # root Application, AppProjects, apps ApplicationSet
├── apps/root/               # platform-* Application 선언과 App-of-Apps entry
├── platform/                # argocd, cert-manager, eso, ingress, istio, monitoring 등 공통 리소스
├── workloads/
│   └── adminer/             # Rollout/AnalysisTemplate/Ingress/Istio 패턴 참조 워크로드
└── README.md                # This file
```

## Service Coverage Matrix

| Area | Purpose and owner | Lifecycle and config | Dependencies, routes, secrets | Validation and operations |
| --- | --- | --- | --- | --- |
| `clusters/local` | Local ArgoCD bootstrap entrypoint owned by platform maintainers. | Contains root Application, AppProjects, and workload ApplicationSet. | Depends on ArgoCD and the repository URL/target revision contract; no application secrets live here. | Validate root Application/ApplicationSet hierarchy with `bash scripts/validate-gitops-structure.sh` and static contracts with `bash infrastructure/tests/verify-contracts-static.sh`. |
| `apps/root` | App-of-Apps root for platform components owned by platform maintainers. | Declares platform Application resources and Kustomize entrypoint. | Depends on `gitops/platform/*` paths, the self-managed `gitops/clusters/local` config app, and ArgoCD project permissions. | Validate platform-project and local-source boundaries with GitOps structure and manifest checks before PR merge. |
| `platform/argocd` | ArgoCD runtime config and external Valkey integration owned by platform maintainers. | Kustomize config for metrics, notifications, and external Valkey secret wiring. | Depends on Vault-backed ExternalSecret and external Valkey endpoint; routes are handled by ArgoCD ingress/Traefik docs. | Validate static contracts and secret handling; live sync requires ArgoCD runtime checks. |
| `platform/cert-manager` | Local certificate issuer config owned by platform maintainers. | Kustomize config for mkcert ClusterIssuer. | Depends on cert-manager controller and local CA material; do not commit private keys. | Validate manifests statically; live readiness requires cert-manager checks. |
| `platform/eso` | External Secrets Operator platform config owned by platform maintainers. | Kustomize config for Vault ClusterSecretStore and app ExternalSecret examples. | Depends on external Vault and approved Vault policy; secret values stay outside Git. | Validate static contracts and secret handling; live readiness requires ESO/Vault checks. |
| `platform/external-services` | In-cluster Service/EndpointSlice contracts for external services owned by platform maintainers. | Kustomize config for Vault, PostgreSQL, Valkey, Prometheus, Loki, Tempo, Alloy, and Grafana endpoints. | Depends on external runtimes and stable local network addresses; no live mutation in normal GitOps flow. | Validate static contracts; live reachability requires `infrastructure/tests/verify-external-services.sh`. |
| `platform/headlamp` | Headlamp ingress config owned by platform maintainers. | Kustomize config for Headlamp ingress. | Depends on Headlamp controller and local ingress/TLS route. | Validate manifests statically; live route requires ingress/TLS checks. |
| `platform/kiali` | Kiali ingress config owned by platform maintainers. | Kustomize config for Kiali ingress. | Depends on Kiali, Istio, and observability endpoints. | Validate manifests and Kiali egress policy; live route requires ingress/TLS checks. |
| `platform/monitoring` | Monitoring integration config owned by platform maintainers. | Kustomize config for kube-state-metrics, Alloy log collection, and metrics NodePorts. | Depends on monitoring namespace and external observability services. | Validate manifests statically; live behavior requires monitoring and external service checks. |
| `platform/namespaces` | Namespace desired state owned by platform maintainers. | Kustomize config for platform, apps, ingress, ESO, cert-manager, Istio, Headlamp, Rollouts, and monitoring namespaces. | Dependencies are cluster-scoped namespace resources; no secrets. | Validate Kustomize completeness and manifest syntax. |
| `platform/network-policies` | Network egress policy owned by platform/security maintainers. | Kustomize config for apps, monitoring, Kiali, ESO-to-Vault, and ArgoCD-to-Valkey egress. | Depends on namespace labels, external service addresses, Vault, Valkey, and observability endpoints. | Validate Kustomize completeness and manifests; live behavior requires `verify-network-policies.sh`. |
| `workloads/adminer` | Reference workload owned by platform maintainers and app operators. | Kustomize config for Rollout, services, ingress, Istio routing, PeerAuthentication, and analysis. | Depends on apps namespace, ingress, Rollouts, Istio, and PostgreSQL external service route assumptions. | Validate manifests statically; live rollout and route checks require cluster validation. |

## How to Work in This Area

1. 플랫폼 계약은 먼저 [Spec](../docs/03.specs/001-wsl-k3d-argocd-platform/spec.md)과 [Operations Policy](../docs/05.operations/policies/0001-k8s-gitops-operations-policy.md)에서 확인한다.
2. 새 앱은 [examples/sample-app](../examples/sample-app/README.md)을 복사해 `gitops/workloads/<appname>/`에서 시작한다.
3. 변경은 feature branch와 PR review를 거쳐 `main`에 병합하고, ArgoCD가 Git 상태를 reconcile하도록 둔다.
4. 매니페스트 변경 후 `bash scripts/validate-gitops-structure.sh`와 `bash scripts/validate-k8s-manifests.sh .`를 실행한다.
5. secret 값은 매니페스트에 직접 쓰지 않고 External Secrets/Vault 계약으로 연결한다.

## Current Hardening Deferrals

현재 GitOps 구조는 정적 검증을 통과하지만, 아래 항목은 Kubernetes/ArgoCD
semantics가 바뀌는 작업이라 별도 승인된 hardening pass에서 다룬다.

- `apps` AppProject allow-list 최소화: 현재 워크로드 패턴을 깨지 않는
  resource-kind 기준을 먼저 확정해야 한다.
- `CreateNamespace=true` ownership 정리: ApplicationSet과
  `platform/namespaces`의 namespace 소유권 경계를 먼저 검증해야 한다.
- image tag와 workload-kind 정책 스캔: 운영 정책과 CI failure mode를 먼저
  설계한 뒤 validator에 추가한다.

## Link Basis

이 README의 링크 기준 위치는 `gitops/`다.

- 같은 폴더의 파일과 하위 경로는 현재 README 위치 기준 상대 링크로 연결한다.
- 상위 저장소 문서나 다른 stage 문서는 필요한 만큼 `../`로 올라가서 연결한다.
- 다른 README의 상대 링크를 그대로 복사하지 말고, 이 파일 위치 기준으로 다시 계산한다.

## Related Documents

- [ADR-0002](../docs/02.architecture/decisions/0002-argocd-helm-and-gitops-model.md)
- [ADR-0004](../docs/02.architecture/decisions/0004-external-services-endpoints-and-valkey-backend.md)
- [Spec](../docs/03.specs/001-wsl-k3d-argocd-platform/spec.md)
- [Workloads README](./workloads/README.md)
- [Examples README](../examples/README.md)
