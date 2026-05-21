---
title: 'Platform Expansion Implementation Plan'
type: plan
status: complete
owner: platform-team
updated: 2026-05-21
---

# Platform Expansion Implementation Plan

## Overview (KR)

이 문서는 IP 서브넷 수정, cert-manager, Kubernetes Dashboard, Istio, Kiali 도입을 위한 단계별 실행 계획이다.
기존 플랫폼 계약과 부트스트랩 흐름을 보전하면서 신규 컴포넌트를 순서대로 통합한다.

> **현재 실행계약 메모 (2026-05-09)**: 이 Plan은 2026-03-29 플랫폼 확장 실행 기록이다. 현재 repo-backed 실행계약은 [ADR-0010](../../02.architecture/decisions/0010-headlamp-replaces-dashboard.md)과 현재 `gitops/**` 매니페스트/정적 검증 스크립트가 우선한다. Kubernetes Dashboard는 Headlamp로 대체되었고, 외부 서비스 EndpointSlice/CIDR 계약은 `172.18.x` 기준이다.

## Context

이 계획은 2026-03-29 기준 플랫폼 확장 작업의 실행 순서와 완료 증적을 기록한다. Dashboard 관련 항목은 역사적 실행 기록이며, 현재 UI 실행계약은 Headlamp ADR과 live GitOps manifests를 우선한다.

## Goals & In-Scope

- **Goals**:
  - 외부 서비스 IP를 `172.19.0.x`(infra_net 실제 서브넷)로 수정.
  - cert-manager + mkcert CA ClusterIssuer로 TLS 자동화.
  - Kubernetes Dashboard v3 GitOps 설치 및 HTTPS 노출.
  - Istio v1.25.x(istiod) GitOps 설치.
  - Kiali v2.6.x GitOps 설치 및 외부 Observability 연동.
  - 현재 문서 taxonomy 기반 문서 체인 + README 동기화.
- **In Scope**:
  - `gitops/`, `infrastructure/`, `docs/` 변경
  - Traefik router config 명세 (외부 repo 적용은 별도)
  - `verify-contracts-static.sh` 패턴 갱신

## Non-Goals & Out-of-Scope

- 외부 서비스 런타임 배포
- Istio IngressGateway 활성화
- ArgoCD TLS cert-manager 이관
- GitHub Actions push deploy
- 외부 Traefik repo 직접 수정

## Work Breakdown

| Task    | Description                                              | Files / Docs Affected                                                                  | Target REQ    | Validation Criteria            |
| ------- | -------------------------------------------------------- | -------------------------------------------------------------------------------------- | ------------- | ------------------------------ |
| PLN-001 | EndpointSlice IP 수정 (`172.30.0.x` → `172.19.0.x`)      | `gitops/platform/external-services/*.yaml`                                             | REQ-FUN-01    | `verify-contracts-static.sh`   |
| PLN-002 | NetworkPolicy cidr 수정                                  | `gitops/platform/network-policies/*.yaml`                                              | REQ-FUN-02    | `verify-network-policies.sh`   |
| PLN-003 | bootstrap-local.sh 기본값 수정                           | `infrastructure/bootstrap-local.sh`                                                    | REQ-FUN-03    | `bash -n` + 수동 확인          |
| PLN-004 | verify-contracts-static.sh 패턴 갱신                     | `infrastructure/tests/verify-contracts-static.sh`                                      | REQ-FUN-12    | standalone PASS                |
| PLN-005 | cert-manager GitOps 리소스 작성                          | `gitops/platform/cert-manager/`, `gitops/apps/root/platform-cert-manager-app.yaml`     | REQ-FUN-04    | ClusterIssuer Ready=True       |
| PLN-006 | namespace-cert-manager 추가                              | `gitops/platform/namespaces/namespace-cert-manager.yaml`                               | REQ-FUN-04    | namespace 생성 확인            |
| PLN-007 | bootstrap rootCA Secret 주입 단계 추가                   | `infrastructure/bootstrap-local.sh`                                                    | REQ-FUN-06    | Secret 존재 확인               |
| PLN-008 | Dashboard GitOps 리소스 작성                             | `gitops/platform/dashboard/`, `gitops/apps/root/platform-dashboard-app.yaml`           | REQ-FUN-07/08 | Dashboard Deployment Available |
| PLN-009 | namespace-kubernetes-dashboard 추가                      | `gitops/platform/namespaces/namespace-kubernetes-dashboard.yaml`                       | REQ-FUN-07    | namespace 생성 확인            |
| PLN-010 | Istio GitOps 리소스 작성 (istio-base + istiod)           | `gitops/platform/istio/`, `gitops/apps/root/platform-istio-*.yaml`                     | REQ-FUN-09    | istiod Available               |
| PLN-011 | namespace-istio-system 추가                              | `gitops/platform/namespaces/namespace-istio-system.yaml`                               | REQ-FUN-09    | namespace 생성 확인            |
| PLN-012 | Kiali GitOps 리소스 작성                                 | `gitops/platform/kiali/`, `gitops/apps/root/platform-kiali-app.yaml`                   | REQ-FUN-10    | Kiali Deployment Available     |
| PLN-013 | Kiali egress NetworkPolicy 추가                          | `gitops/platform/network-policies/kiali-egress-to-observability.yaml`                  | REQ-FUN-10    | Prometheus 연결 확인           |
| PLN-014 | AppProject platform 갱신 (sourceRepos/destinations/CRDs) | `gitops/clusters/local/appproject-platform.yaml`                                       | REQ-FUN-09/10 | ArgoCD sync 성공               |
| PLN-015 | kustomization.yaml 갱신 (namespaces, apps/root)          | `gitops/platform/namespaces/kustomization.yaml`, `gitops/apps/root/kustomization.yaml` | 전체          | ArgoCD App-of-Apps sync        |
| PLN-016 | Traefik router config 명세 생성 (외부 repo용)            | `docs/03.specs/003-platform-expansion/spec.md` 참조                                    | REQ-FUN-11    | 별도 repo 적용 후 HTTPS 접근   |
| PLN-017 | 문서 체인 갱신 (ADR-0001/0004/0005 IP 수정)              | `docs/02.architecture/decisions/0001,0004,0005-*.md`                                                      | 추적성        | 링크 정합성 확인               |
| PLN-018 | README 인덱스 동기화 (current taxonomy)                  | `README.md`, `docs/README.md`, stage `README.md`                                        | 거버넌스      | 인덱스 반영 확인               |

## Verification Plan

| ID          | Level   | Description                | Command / How to Run                                                       | Pass Criteria |
| ----------- | ------- | -------------------------- | -------------------------------------------------------------------------- | ------------- |
| VAL-PLN-001 | Static  | IP 패턴 계약               | `./infrastructure/tests/verify-contracts-static.sh`                        | PASS          |
| VAL-PLN-002 | Static  | Shell 문법                 | `bash -n infrastructure/bootstrap-local.sh`                                | 오류 없음     |
| VAL-PLN-003 | Runtime | cert-manager ClusterIssuer | `kubectl get clusterissuer mkcert-ca-issuer`                               | Ready=True    |
| VAL-PLN-004 | Runtime | Dashboard HTTPS            | `curl -sko /dev/null -w '%{http_code}' https://dashboard.127.0.0.1.nip.io` | 200 또는 401  |
| VAL-PLN-005 | Runtime | istiod 가용성              | `kubectl -n istio-system get deploy istiod`                                | AVAILABLE≥1   |
| VAL-PLN-006 | Runtime | Kiali HTTPS                | `curl -sko /dev/null -w '%{http_code}' https://kiali.127.0.0.1.nip.io`     | 200           |
| VAL-PLN-007 | Runtime | 외부 서비스 연결           | `./infrastructure/tests/verify-external-services.sh`                       | PASS          |
| VAL-PLN-008 | Runtime | 전체 검증                  | `./infrastructure/tests/run-all.sh`                                        | PASS          |

## Risks & Mitigations

| Risk                                  | Impact | Mitigation                                         |
| ------------------------------------- | ------ | -------------------------------------------------- |
| IP 수정 후 verify-contracts 패턴 누락 | High   | PLN-004와 PLN-001을 동시 실행                      |
| Istio CRD 설치 순서 오류              | High   | istio-base → istiod sync-wave 순서 강제            |
| rootCA Key 파일 경로 불일치           | Medium | bootstrap에서 `require_file` 검증 추가             |
| Kiali Prometheus 연결 실패            | Medium | egress NetworkPolicy cidr 및 infra_net 가용성 확인 |
| Dashboard cluster-admin 권한 과다     | Low    | 로컬 전용 명시, 프로덕션 배포 금지 문서화          |

## Completion Criteria

- [x] PLN-001~004 완료 (IP 수정 + 정적 검증 패턴)
- [x] PLN-005~007 완료 (cert-manager + ClusterIssuer)
- [x] PLN-008~009 완료 (Dashboard)
- [x] PLN-010~011 완료 (Istio)
- [x] PLN-012~013 완료 (Kiali)
- [x] PLN-014~015 완료 (AppProject + kustomization)
- [x] VAL-PLN-001~002 정적 검증 PASS (`verify-contracts-static.sh`)
- [x] PLN-017~018 완료 (문서 + README 동기화)
- [x] Phase 4D 완료 (관측성 외부 서비스 T-027~T-031)

## Related Documents

- **PRD**: [`../../01.requirements/2026-03-29-platform-expansion-dashboard-mesh.md`](../../01.requirements/2026-03-29-platform-expansion-dashboard-mesh.md)
- **ARD**: [`../../02.architecture/requirements/0003-platform-expansion-mesh-dashboard.md`](../../02.architecture/requirements/0003-platform-expansion-mesh-dashboard.md)
- **Spec**: [`../../03.specs/003-platform-expansion/spec.md`](../../03.specs/003-platform-expansion/spec.md)
- **ADR**: [`../../02.architecture/decisions/0006-cert-manager-mkcert-ca-issuer.md`](../../02.architecture/decisions/0006-cert-manager-mkcert-ca-issuer.md)
- **ADR**: [`../../02.architecture/decisions/0007-kubernetes-dashboard-v3.md`](../../02.architecture/decisions/0007-kubernetes-dashboard-v3.md) — historical/superseded Dashboard decision
- **ADR**: [`../../02.architecture/decisions/0008-istio-install-and-ingress-coexist.md`](../../02.architecture/decisions/0008-istio-install-and-ingress-coexist.md)
- **ADR**: [`../../02.architecture/decisions/0009-kiali-external-observability.md`](../../02.architecture/decisions/0009-kiali-external-observability.md)
- **ADR**: [`../../02.architecture/decisions/0010-headlamp-replaces-dashboard.md`](../../02.architecture/decisions/0010-headlamp-replaces-dashboard.md) — current UI decision
- **Tasks**: [`../tasks/2026-03-29-platform-expansion.md`](../tasks/2026-03-29-platform-expansion.md)
