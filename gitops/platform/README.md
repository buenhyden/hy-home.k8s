---
title: "platform"
version: "1.0.0"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-11-20"
---
# platform

## 문서 개요

### 목적과 독자

이 README는 gitops/platform의 사용·연결·검사 위치를 찾는 운영자와 기여자를 안내한다. 현재 역할은 [Service](#service)와 [Usage](#usage)에 기록한다.

### 책임과 적용 범위

platform은 gitops/platform의 진입 경로를 유지한다. 이 경로의 파일과 경계는 [Purpose](#purpose), 사용 조건은 [Usage](#usage), 검사는 [Checks](#checks)가 설명한다.

## 내용 계약

### 입력과 전제

입력과 전제는 아래 역할별 본문의 해당 절에 기록한다.

### 본문과 규칙


> App-of-Apps가 배포하는 공통 플랫폼 리소스의 Kustomize 진입점을 관리한다.

#### Service

##### Purpose

이 경로의 각 하위 디렉터리는 `apps/root`의 `platform-*` Application 하나가
가리키는 공통 플랫폼 구성 단위다. 앱 워크로드는 `../workloads/`가 소유한다.

아래 표가 이 폴더의 직접 하위 디렉터리를 안내한다.

- [gitops](../README.md)
- [workloads](../workloads/README.md)

###### Platform Coverage Matrix

이 표는 공통 플랫폼 디렉터리와 운영 책임을 연결한다. `repository-quality`
게이트는 이 표가 이 폴더의 실제 하위 디렉터리와 순서까지 동기화되어 있는지
검증한다.

| Area                         | Purpose and owner                                                                               | Lifecycle and config                                                                                                   | Dependencies, routes, secrets                                                                                                  | Validation and operations                                                                                                                                                             |
| ---------------------------- | ----------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `argocd` | ArgoCD runtime config and external Valkey integration owned by platform maintainers.            | Kustomize config for metrics, notifications, and external Valkey secret wiring.                                        | Depends on Vault-backed ExternalSecret and external Valkey endpoint; routes are handled by the ArgoCD ingress behind the k8s router.        | Validate static contracts and secret handling; live sync requires ArgoCD runtime checks.                                                                                              |
| `cert-manager` | Local certificate issuer config owned by platform maintainers.                                  | Kustomize config for mkcert ClusterIssuer.                                                                             | Depends on cert-manager controller and local CA material; do not commit private keys.                                          | Validate manifests statically; live readiness requires cert-manager checks.                                                                                                           |
| `eso` | External Secrets Operator platform config owned by platform maintainers.                        | Kustomize config for Vault ClusterSecretStore and app ExternalSecret examples.                                         | Depends on external Vault, exact `vault` audience, and approved Vault policy; secret values stay outside Git.                  | Validate with `python3 scripts/validate-vault-eso-contracts.py --root .` plus static secret checks; live readiness requires ESO/Vault checks.                                         |
| `external-services` | In-cluster Service/EndpointSlice contracts for external services owned by platform maintainers. | Kustomize config for PostgreSQL, Valkey, Loki, Tempo, and Alloy endpoints. | Depends on external runtimes and stable local network addresses; OpenBao, Prometheus, and Grafana use external HTTPS names instead. | Validate static contracts; live reachability requires `infrastructure/verify/verify-external-services.sh`. |
| `headlamp` | Headlamp ingress config owned by platform maintainers.                                          | Kustomize config for Headlamp ingress.                                                                                 | Depends on Headlamp controller and local ingress/TLS route.                                                                    | Validate manifests statically; live route requires ingress/TLS checks.                                                                                                                |
| `ingress-routes` | k8s router apex redirects owned by platform maintainers (ADR-0043).                             | Kustomize config for `hy-k8s.home.arpa/<name>` 301 redirects to `<name>.hy-k8s.home.arpa`.                             | Depends on Traefik, the `mkcert-ca-issuer` ClusterIssuer, and the k8s router on `192.168.0.14`.                          | Validate with `validate-infrastructure-contracts.sh`; live redirect requires `CHECK_K8S_ROUTER=true`.                                                                                 |
| `kiali` | Kiali ingress config owned by platform maintainers.                                             | Kustomize config for Kiali ingress.                                                                                    | Depends on Kiali, Istio, and observability endpoints.                                                                          | Validate manifests and Kiali egress policy; live route requires ingress/TLS checks.                                                                                                   |
| `monitoring` | Monitoring integration config owned by platform maintainers. | Kustomize config for kube-state-metrics, Alloy collection, and Prometheus API auth. | Depends on monitoring namespace and external observability services; metrics NodePorts are retired. | Validate manifests statically; live behavior requires monitoring and external service checks. |
| `namespaces` | Namespace desired state owned by platform maintainers.                                          | Kustomize config for platform, apps, ingress, ESO, cert-manager, Istio, Headlamp, Rollouts, and monitoring namespaces. | Dependencies are cluster-scoped namespace resources; no secrets.                                                               | Validate Kustomize completeness and manifest syntax.                                                                                                                                  |
| `network-policies` | Network egress policy owned by platform/security maintainers.                                   | Kustomize config for apps, monitoring, Kiali, ESO-to-Vault, and ArgoCD-to-Valkey egress.                               | Depends on namespace labels, external service addresses, Vault, Valkey, and observability endpoints.                           | Validate Kustomize completeness and manifests; live behavior requires `verify-network-policies.sh`.                                                                                   |

##### Interfaces

이 README는 별도의 외부 입출력 계약을 정의하지 않으며, 각 디렉터리의 의존성과 경로는 Platform Coverage Matrix의 열이 적는다.

###### Security Boundary

secret 값과 credential을 다루지 않는 경계는 아래 Usage > Prerequisites에 적혀 있다.

#### Usage

##### Prerequisites

각 디렉터리는 desired state만 선언한다. secret 값, 외부 서비스 런타임, live
cluster 변경은 이 폴더의 범위가 아니며 [gitops](../README.md)의 경계를 따른다.

##### Selected Start

변경은 reviewed pull request로 반영하고 ArgoCD가 동기화한다. 운영 절차는
`docs/05.operations/`가 소유한다.

#### Checks

##### Readiness

각 행의 Validation and operations 열이 해당 디렉터리의 정적 검증 명령을
명시한다. 저장소 전체 검증은 `python3 scripts/qa.py staged`로 실행한다.

##### Failure Handling

이 README는 별도의 관측·복구 절차를 두지 않으며, 각 디렉터리의 live 확인은 Platform Coverage Matrix의 Validation and operations 열이 적는다.

###### Runbook Links

이 README는 별도의 runbook 링크를 두지 않으며, 운영 절차의 소유처는 Selected Start에 `docs/05.operations/`로 적혀 있다.

## 적용과 확인

### 적용 방법

아래 역할별 본문에 기록된 사용 조건과 절차를 적용한다.

### 확인 기준

아래 역할별 본문의 검증·확인 조건과 그 한계에 따른다.

## 관계와 출처

### 관련 문서

관련 문서와 정본 링크는 아래 역할별 본문에서 확인한다.

### 외부 근거

외부 근거가 사용된 경우 아래 역할별 본문의 출처와 적용 범위에서 확인한다.
