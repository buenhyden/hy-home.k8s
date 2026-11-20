---
title: "verify"
version: "1.0.0"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-11-20"
---
# verify

## 문서 개요

### 목적과 독자

이 README는 infrastructure/verify의 사용·연결·검사 위치를 찾는 운영자와 기여자를 안내한다. 현재 역할은 [Service](#service)와 [Usage](#usage)에 기록한다.

### 책임과 적용 범위

platform은 infrastructure/verify의 진입 경로를 유지한다. 이 경로의 파일과 경계는 [Purpose](#purpose), 사용 조건은 [Usage](#usage), 검사는 [Checks](#checks)가 설명한다.

## 내용 계약

### 입력과 전제

입력과 전제는 아래 역할별 본문의 해당 절에 기록한다.

### 본문과 규칙


> 부트스트랩된 로컬 클러스터를 대상으로 하는 라이브 검증 스크립트를 관리한다.

#### Service

##### Purpose

이 폴더의 스크립트는 모두 라이브 검증이며 저장소 정적 검사를 대신하지 않는다.
실행 전제와 결과 의미는 아래 표가 소유한다.

아래 표가 이 폴더의 스크립트를 안내한다.

- [infrastructure](../README.md)

##### Interfaces

이 README는 별도의 외부 입출력 계약을 정의하지 않으며, 각 스크립트의 실행 전제와 결과 의미는 Infrastructure Test Inventory가 소유한다.

###### Security Boundary

secret 값을 출력하지 않는 경계는 아래 Usage > Prerequisites에 적혀 있다.

#### Usage

##### Prerequisites

스크립트는 kubeconfig와 클러스터 상태를 읽기만 하며 secret 값을 출력하지 않는다.
클러스터 변경은 [infrastructure](../README.md)의 bootstrap 절차가 소유한다.

##### Selected Start

전체 라이브 검증은 `run-all.sh`로 실행한다. 복구 절차는
`docs/05.operations/03.runbooks/`가 소유한다.

#### Checks

##### Readiness

`bash -n`과 shellcheck 정적 검사는 `python3 scripts/qa.py staged`가 선택한다.
라이브 실행은 승인된 운영 절차에서만 한다.

###### Infrastructure Test Inventory

이 표는 이 폴더의 `*.sh`의 현재 유지 계약이며 전부 라이브 검증이다.
부트스트랩된 k3d/ArgoCD 환경에서만 실행한다. 저장소 정적 계약 검사는
`scripts/validate-infrastructure-contracts.sh`가 소유하며 QA 실행
레지스트리가 그 선택과 실행을 결정한다.

| Test script | Type | Preconditions | Result semantics | Retention / command surface |
| --- | --- | --- | --- | --- |
| `verify-cluster.sh` | Live | Bootstrapped k3d context, trusted kubeconfig CA, kubectl, and MetalLB. | PASS means at least four nodes report Ready and MetalLB matches the local platform baseline. | Tier B: called by `run-all.sh`; documented in bootstrap runbook and this README. |
| `verify-gitops.sh` | Live | Reachable ArgoCD namespace and reconciled root/platform applications. | PASS means the live root Application source path/revision matches and the applications explicitly named in the script are Healthy and Synced; other root children are outside this check. | Tier B: called by `run-all.sh`; documented in bootstrap runbook and this README. |
| `verify-secrets.sh` | Live | External Secrets Operator, OpenBao HTTPS/Kubernetes auth, and ArgoCD external Valkey secret flow are bootstrapped. | PASS means `vault-backend` and `argocd-external-valkey` live readiness contracts pass. | Tier B: called by `run-all.sh`; documented in bootstrap runbook and this README. |
| `verify-external-services.sh` | Live | Python 3 is available; platform namespace Services and EndpointSlices exist for external Valkey and observability contracts. | PASS means non-headless selectorless ClusterIP Service ports and every same-service EndpointSlice port/address match the four declared local contracts; connectivity and authentication are outside this check. | Tier B: called by `run-all.sh`; documented in bootstrap runbook and this README. |
| `verify-network-policies.sh` | Live | NetworkPolicy resources are reconciled in platform, argocd, external-secrets, and istio-system namespaces. | PASS means required live egress NetworkPolicy contracts match the expected CIDR and port checks. | Tier B: called by `run-all.sh`; documented in bootstrap runbook and this README. |
| `verify-ingress-tls.sh` | Live | Traefik LoadBalancer (Service `traefik/traefik`), ArgoCD ingress/TLS, the mkcert root CA file used by the verifier, curl, rg, and optional k8s router inputs are available. | PASS means ArgoCD ingress/TLS and fallback endpoint pass CA-verified HTTPS; router checks run only when enabled, and Headlamp/Kiali TLS type mismatches report warnings. | Tier B: called by `run-all.sh`; documented in bootstrap runbook and this README. |
| `run-all.sh` | Live aggregate | All live-test preconditions above are satisfied. | PASS means every live verification script in this inventory completed successfully. | Tier B: canonical live validation entrypoint in this README and SDD verification records. |

##### Failure Handling

이 README는 별도의 관측·복구 절차를 두지 않으며, 복구 절차는 Selected Start에 적힌 `docs/05.operations/03.runbooks/`가 소유한다.

###### Runbook Links

이 README는 별도의 runbook 링크를 두지 않으며, 복구 절차의 소유처는 Selected Start에 `docs/05.operations/03.runbooks/`로 적혀 있다.

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
