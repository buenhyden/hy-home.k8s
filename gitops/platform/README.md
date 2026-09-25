---
title: "platform"
version: "0.1.0"
type: "common/readme-implementation"
status: "active"
owner: "platform"
updated: "2026-09-25"
---
# platform

> App-of-Apps가 배포하는 공통 플랫폼 리소스의 Kustomize 진입점을 관리한다.

## Overview

이 경로의 각 하위 디렉터리는 `apps/root`의 `platform-*` Application 하나가
가리키는 공통 플랫폼 구성 단위다. 앱 워크로드는 `../workloads/`가 소유한다.

## Structure

아래 표가 이 폴더의 직접 하위 디렉터리를 안내한다.

### Platform Coverage Matrix

이 표는 공통 플랫폼 디렉터리와 운영 책임을 연결한다. `repository-quality`
게이트는 이 표가 이 폴더의 실제 하위 디렉터리와 순서까지 동기화되어 있는지
검증한다.

| Area                         | Purpose and owner                                                                               | Lifecycle and config                                                                                                   | Dependencies, routes, secrets                                                                                                  | Validation and operations                                                                                                                                                             |
| ---------------------------- | ----------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `argocd` | ArgoCD runtime config and external Valkey integration owned by platform maintainers.            | Kustomize config for metrics, notifications, and external Valkey secret wiring.                                        | Depends on Vault-backed ExternalSecret and external Valkey endpoint; routes are handled by the ArgoCD ingress behind the k8s router.        | Validate static contracts and secret handling; live sync requires ArgoCD runtime checks.                                                                                              |
| `cert-manager` | Local certificate issuer config owned by platform maintainers.                                  | Kustomize config for mkcert ClusterIssuer.                                                                             | Depends on cert-manager controller and local CA material; do not commit private keys.                                          | Validate manifests statically; live readiness requires cert-manager checks.                                                                                                           |
| `eso` | External Secrets Operator platform config owned by platform maintainers.                        | Kustomize config for Vault ClusterSecretStore and app ExternalSecret examples.                                         | Depends on external Vault, exact `vault` audience, and approved Vault policy; secret values stay outside Git.                  | Validate with `python3 scripts/validate-vault-eso-contracts.py --root .` plus static secret checks; live readiness requires ESO/Vault checks.                                         |
| `external-services` | In-cluster Service/EndpointSlice contracts for external services owned by platform maintainers. | Kustomize config for Vault, PostgreSQL, Valkey, Prometheus, Loki, Tempo, Alloy, and Grafana endpoints.                 | Depends on external runtimes and stable local network addresses; Vault HTTP is annotated local-only and is not production TLS. | Validate with `python3 scripts/validate-vault-eso-contracts.py --root .` plus static contracts; live reachability requires `infrastructure/verify/verify-external-services.sh`.        |
| `headlamp` | Headlamp ingress config owned by platform maintainers.                                          | Kustomize config for Headlamp ingress.                                                                                 | Depends on Headlamp controller and local ingress/TLS route.                                                                    | Validate manifests statically; live route requires ingress/TLS checks.                                                                                                                |
| `ingress-routes` | k8s router apex redirects owned by platform maintainers (ADR-0043).                             | Kustomize config for `hy-k8s.home.arpa/<name>` 301 redirects to `<name>.hy-k8s.home.arpa`.                             | Depends on ingress-nginx, the `mkcert-ca-issuer` ClusterIssuer, and the k8s router on `192.168.0.14`.                          | Validate with `validate-infrastructure-contracts.sh`; live redirect requires `CHECK_K8S_ROUTER=true`.                                                                                 |
| `kiali` | Kiali ingress config owned by platform maintainers.                                             | Kustomize config for Kiali ingress.                                                                                    | Depends on Kiali, Istio, and observability endpoints.                                                                          | Validate manifests and Kiali egress policy; live route requires ingress/TLS checks.                                                                                                   |
| `monitoring` | Monitoring integration config owned by platform maintainers.                                    | Kustomize config for kube-state-metrics, Alloy log collection, and metrics NodePorts.                                  | Depends on monitoring namespace and external observability services.                                                           | Validate manifests statically; live behavior requires monitoring and external service checks.                                                                                         |
| `namespaces` | Namespace desired state owned by platform maintainers.                                          | Kustomize config for platform, apps, ingress, ESO, cert-manager, Istio, Headlamp, Rollouts, and monitoring namespaces. | Dependencies are cluster-scoped namespace resources; no secrets.                                                               | Validate Kustomize completeness and manifest syntax.                                                                                                                                  |
| `network-policies` | Network egress policy owned by platform/security maintainers.                                   | Kustomize config for apps, monitoring, Kiali, ESO-to-Vault, and ArgoCD-to-Valkey egress.                               | Depends on namespace labels, external service addresses, Vault, Valkey, and observability endpoints.                           | Validate Kustomize completeness and manifests; live behavior requires `verify-network-policies.sh`.                                                                                   |

## Configuration Boundary

각 디렉터리는 desired state만 선언한다. secret 값, 외부 서비스 런타임, live
cluster 변경은 이 폴더의 범위가 아니며 [gitops](../README.md)의 경계를 따른다.

## Validation

각 행의 Validation and operations 열이 해당 디렉터리의 정적 검증 명령을
명시한다. 저장소 전체 검증은 `python3 scripts/qa.py staged`로 실행한다.

## Operations

변경은 reviewed pull request로 반영하고 ArgoCD가 동기화한다. 운영 절차는
`docs/05.operations/`가 소유한다.

## Related Documents

- [gitops](../README.md)
- [workloads](../workloads/README.md)
