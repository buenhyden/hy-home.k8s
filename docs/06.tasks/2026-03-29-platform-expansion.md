# Task: Platform Expansion Execution

## Overview (KR)

이 문서는 플랫폼 확장(IP 수정, cert-manager, Dashboard, Istio, Kiali) 구현 작업을 추적한다.
TDD(RED/GREEN/REFACTOR) 중심으로 정적 계약 검증이 먼저 정의되고, 구현이 이를 통과하는 방식으로 진행한다.

## Inputs

- **Parent Spec**: [`../04.specs/003-platform-expansion/spec.md`](../04.specs/003-platform-expansion/spec.md)
- **Parent Plan**: [`../05.plans/2026-03-29-platform-expansion.md`](../05.plans/2026-03-29-platform-expansion.md)

## Working Rules

- RED: 실패 조건(정적 검증, 계약 불일치)을 먼저 정의한다.
- GREEN: 최소 변경으로 통과한다.
- REFACTOR: 검증 메시지/계약 문구를 표준화한다.

## Task Table

| Task ID | Description                                              | Type | Parent Spec / Section   | Parent Plan / Phase | Validation / Evidence                            | Status |
| ------- | -------------------------------------------------------- | ---- | ----------------------- | ------------------- | ------------------------------------------------ | ------ |
| T-001   | EndpointSlice IP 수정 (`172.30.0.x` → `172.19.0.x`)      | impl | Phase 0 / Contracts     | PLN-001             | `verify-contracts-static.sh` PASS                | Todo   |
| T-002   | NetworkPolicy cidr 수정 (`172.19.0.x`)                   | impl | Phase 0 / NetworkPolicy | PLN-002             | `verify-network-policies.sh` PASS                | Todo   |
| T-003   | `bootstrap-local.sh` 기본값 수정                         | impl | Phase 0 / bootstrap     | PLN-003             | `bash -n` 오류 없음                              | Todo   |
| T-004   | `verify-contracts-static.sh` IP 패턴 갱신                | test | Phase 0 / Verification  | PLN-004             | standalone PASS                                  | Todo   |
| T-005   | cert-manager namespace YAML 생성                         | impl | Phase 1 / namespace     | PLN-006             | `kubectl get ns cert-manager`                    | Todo   |
| T-006   | cert-manager ArgoCD Application 생성                     | impl | Phase 1 / App           | PLN-005             | ArgoCD sync 성공                                 | Todo   |
| T-007   | ClusterIssuer(mkcert-ca-issuer) YAML 생성                | impl | Phase 1 / ClusterIssuer | PLN-005             | ClusterIssuer Ready=True                         | Todo   |
| T-008   | `bootstrap-local.sh` rootCA Secret 주입 단계 추가        | impl | Phase 1 / bootstrap     | PLN-007             | Secret 존재 확인                                 | Todo   |
| T-009   | `gitops/platform/namespaces/kustomization.yaml` 갱신     | impl | 전체                    | PLN-015             | ArgoCD namespace sync                            | Todo   |
| T-010   | kubernetes-dashboard namespace YAML 생성                 | impl | Phase 2 / namespace     | PLN-009             | `kubectl get ns kubernetes-dashboard`            | Todo   |
| T-011   | Dashboard ArgoCD Application 생성                        | impl | Phase 2 / App           | PLN-008             | ArgoCD sync 성공                                 | Todo   |
| T-012   | Dashboard Ingress + cert-manager TLS YAML 생성           | impl | Phase 2 / Ingress       | PLN-008             | `k8s-dashboard.127.0.0.1.nip.io` HTTPS 접근      | Todo   |
| T-013   | Dashboard RBAC (SA + ClusterRoleBinding) YAML 생성       | impl | Phase 2 / RBAC          | PLN-008             | `kubectl get clusterrolebinding dashboard-admin` | Todo   |
| T-014   | istio-system namespace YAML 생성                         | impl | Phase 3 / namespace     | PLN-011             | `kubectl get ns istio-system`                    | Todo   |
| T-015   | istio-base ArgoCD Application 생성                       | impl | Phase 3 / istio-base    | PLN-010             | CRD 설치 확인                                    | Todo   |
| T-016   | istiod ArgoCD Application 생성                           | impl | Phase 3 / istiod        | PLN-010             | istiod Deployment Available                      | Todo   |
| T-017   | istiod Helm values (WSL resource limits)                 | impl | Phase 3 / istiod        | PLN-010             | pilot requests 확인                              | Todo   |
| T-018   | Kiali ArgoCD Application 생성                            | impl | Phase 4 / App           | PLN-012             | ArgoCD sync 성공                                 | Todo   |
| T-019   | Kiali Helm values (external observability URLs)          | impl | Phase 4 / Kiali         | PLN-012             | Kiali Prometheus 연결 정상                       | Todo   |
| T-020   | Kiali Ingress + cert-manager TLS YAML 생성               | impl | Phase 4 / Ingress       | PLN-012             | `kiali.127.0.0.1.nip.io` HTTPS 접근              | Todo   |
| T-021   | Kiali egress NetworkPolicy YAML 생성                     | impl | Phase 4 / NetworkPolicy | PLN-013             | egress cidr 확인                                 | Todo   |
| T-022   | AppProject platform 갱신 (sourceRepos/destinations/CRDs) | impl | Spec / AppProject       | PLN-014             | ArgoCD sync 오류 없음                            | Todo   |
| T-023   | `gitops/apps/root/kustomization.yaml` 신규 앱 추가       | impl | Spec / App-of-Apps      | PLN-015             | App-of-Apps root sync                            | Todo   |
| T-024   | `verify-contracts-static.sh` 신규 서비스 계약 검증 추가  | test | Spec / Verification     | PLN-004             | standalone PASS                                  | Todo   |
| T-025   | 문서 체인 ADR-0001/0004/0005 IP 갱신                     | doc  | 추적성                  | PLN-017             | 링크/IP 정합성 확인                              | Done   |
| T-026   | README 인덱스 동기화 (01~09)                             | doc  | 거버넌스                | PLN-018             | 인덱스 반영                                      | Todo   |

## TDD Scenarios

### TC-01 IP Contract

- RED: `verify-contracts-static.sh`가 `172.30.0.x` 패턴으로 실패
- GREEN: EndpointSlice + NetworkPolicy + verify-contracts 동시 수정으로 PASS
- REFACTOR: bootstrap 기본값과 verify-contracts 패턴 일치 확인

### TC-02 cert-manager ClusterIssuer

- RED: rootCA Secret 없이 ClusterIssuer Ready=False
- GREEN: bootstrap rootCA 주입 후 Ready=True
- REFACTOR: bootstrap `require_file` 추가로 rootCA 경로 누락 조기 탐지

### TC-03 Dashboard TLS

- RED: cert-manager ClusterIssuer 없이 Certificate pending
- GREEN: ClusterIssuer 준비 후 Certificate Ready=True → `k8s-dashboard.127.0.0.1.nip.io` HTTPS 접근
- REFACTOR: Ingress annotation 표준화

### TC-04 Istio 설치 순서

- RED: istio-base CRD 없이 istiod 설치 시 오류
- GREEN: sync-wave `istio-base(wave:1) → istiod(wave:2)` 강제
- REFACTOR: `platform-istio-base-app.yaml` syncPolicy retry 설정

### TC-05 Kiali Observability

- RED: egress NetworkPolicy 없이 Prometheus 연결 실패
- GREEN: egress cidr `172.19.0.20/32, 172.19.0.22/32, 172.19.0.24/32` 추가
- REFACTOR: NetworkPolicy selector를 Kiali Pod label 기준으로 범위 제한

## Verification Summary

- **Static**:
  - `bash -n infrastructure/bootstrap-local.sh infrastructure/tests/*.sh`
  - `./infrastructure/tests/verify-contracts-static.sh`
- **Runtime**:
  - `./infrastructure/tests/run-all.sh`
  - `CHECK_TRAEFIK_443=true ./infrastructure/tests/verify-ingress-tls.sh`
  - `kubectl -n cert-manager get clusterissuer mkcert-ca-issuer`
  - `kubectl -n kubernetes-dashboard get certificate dashboard-tls`
  - `kubectl -n istio-system get deploy istiod kiali`

## Evidence Location

- Scripts: `infrastructure/tests/*`
- GitOps: `gitops/platform/{cert-manager,dashboard,istio,kiali}/`
- Apps: `gitops/apps/root/`
- Spec: `../04.specs/003-platform-expansion/spec.md`
