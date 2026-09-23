---
title: "Service Mesh & cert-manager Operations Policy"
version: "1.0.5"
type: "operation/policy"
status: "active"
owner: "platform"
updated: "2026-09-23"
layer: "operations"
artifact_id: "POL-0003"
---

# Service Mesh & cert-manager Operations Policy

## Overview

이 문서는 cert-manager(TLS 자동화), Istio(서비스메시), Kiali(메시 관측) 운영 통제 기준을 정의한다.
플랫폼 확장 컴포넌트의 보안 정책, 갱신 제약, 허용/금지 작업을 명시한다.
클러스터 UI(Headlamp) 통제는 [POL-0004](./0004-rollouts-notifications-headlamp-policy.md),
k8s router와 live 변경 예외의 공통 기준은 [POL-0001](./0001-k8s-gitops-operations-policy.md)이 소유한다.

## Policy Scope

- cert-manager + mkcert ClusterIssuer(`mkcert-ca-issuer`)
- Istio(istiod) + sidecar 주입 정책
- Kiali + 외부 Observability 연동

## Applies To

- **Systems**: `gitops/platform/{cert-manager,kiali}/`, `gitops/apps/root/platform-istio-base-app.yaml`, `gitops/apps/root/platform-istio-cni-app.yaml`, `gitops/apps/root/platform-istiod-app.yaml`, `infrastructure/bootstrap-local.sh`
- **Agents**: 문서/운영 자동화 에이전트
- **Environments**: Linux server local cluster

## Controls

### TLS / cert-manager

- **Required**:
  - ClusterIssuer 단일 운영: `mkcert-ca-issuer` (CA type, mkcert rootCA 참조)
  - rootCA Secret 이름 고정: `mkcert-root-ca` (namespace: `cert-manager`, key: `tls.crt` / `tls.key`)
  - ArgoCD TLS는 `argocd-local-tls` Secret 수동 주입 유지 — cert-manager 이관 금지
  - `rootCA.pem`은 로컬 신뢰 저장소에 등록 후 HTTPS 접근
  - `secrets/certs/rootCA-key.pem` 파일을 평문 커밋 금지
- **Allowed**:
  - cert-manager controller 재시작은 운영자 승인 후 [플랫폼 확장 런북](../runbooks/0003-platform-expansion-bootstrap-runbook.md)의 절차로 수행
  - ClusterIssuer 상태 확인은 [플랫폼 확장 런북](../runbooks/0003-platform-expansion-bootstrap-runbook.md)의 검증 절차로 수행
- **Disallowed**:
  - `mkcert-root-ca` Secret 평문 커밋
  - ClusterIssuer 다중 운영 (이름 오염 위험)

### Istio / Service Mesh

- **Required**:
  - IngressGateway를 선언하지 않는다 (istiod Application values에 gateway 없음, ADR-0008)
  - sidecar 주입 opt-in: namespace `istio-injection=enabled` 레이블 명시적 부여
  - istiod 자원 예산: `cpu: 100m, memory: 128Mi` (requests)
  - sync-wave 순서 강제: `istio-base`·`istio-cni`(wave:1) → `istiod`(wave:2, `pilot.cni.enabled: true`)
- **Allowed**:
  - Mesh 내 namespace에 `istio-injection=enabled` 레이블 추가
- **Disallowed**:
  - `argocd`, `cert-manager`, `headlamp`, `external-secrets`, `platform` namespace에 `istio-injection=enabled` 레이블 부여
  - (`apps`와 `ingress-nginx`는 mesh 대상이며 `istio-injection=enabled`를 유지한다.)
  - IngressGateway 활성화
  - Ambient mesh 전환(로컬 플랫폼 스코프 외)

### Kiali / Observability

- **Required**:
  - auth: `anonymous` (로컬 전용)
  - Prometheus: `http://prometheus-external.platform.svc.cluster.local:9090`
  - Grafana: `in_cluster_url` `http://grafana-external.platform.svc.cluster.local:3000`, 브라우저 링크 `url` `https://grafana.hy.home.arpa`
  - Tempo(Tracing): `in_cluster_url` `http://tempo-external.platform.svc.cluster.local:3200`
  - egress NetworkPolicy: host 주소 `192.168.0.13/32`의 `9090`, `3000`, `3200` 허용 (ADR-0046)
  - hostname: `kiali.hy-k8s.home.arpa`, TLS: cert-manager 발급 (`kiali-tls`)
- **Disallowed**:
  - 프로덕션에 anonymous auth 유지
  - Kiali egress를 `0.0.0.0/0` 등 광역 cidr로 확장

### CI Governance

- `scripts/validate-infrastructure-contracts.sh` PASS가 모든 IP/endpoint
  변경의 선행 조건이다. 이 검사의 선택과 실행은 QA 실행 레지스트리가 소유한다.
- shell syntax 정적 검증 후 bootstrap-local.sh 변경을 반영한다.
- cert-manager/Istio/Kiali GitOps 리소스는 AppProject `platform` 스코프 내에서만 배포된다.

## Exceptions

- rootCA 재발급 시 `mkcert-root-ca` Secret 재주입 후 cert-manager controller 재시작 허용.
- Istio istiod CrashLoop 시 자원 requests 축소 허용 (단, 128Mi 미만으로 낮추지 않음).

## Verification

- endpoint와 TLS 경계 계약 검증 증적을 남긴다.
- cert-manager/Istio/Kiali 변경 후 관련 GitOps manifest와 runbook의 계약 값이 일치하는지 확인한다.

## Review Cadence

- 플랫폼 컴포넌트 버전 변경 시마다 검토한다.
- cert-manager, Istio, Kiali 관련 ADR/Spec 변경 시 같은 PR에서 검토한다.

## Traceability

- **Spec**: [`../../03.specs/0008-current-local-gitops-platform/spec.md`](../../03.specs/0008-current-local-gitops-platform/spec.md)
- **Runbook**: [`../runbooks/0003-platform-expansion-bootstrap-runbook.md`](../runbooks/0003-platform-expansion-bootstrap-runbook.md)
- **ADR-0006**: [`../../02.architecture/decisions/0006-cert-manager-mkcert-ca-issuer.md`](../../02.architecture/decisions/0006-cert-manager-mkcert-ca-issuer.md)
- **ADR-0008**: [`../../02.architecture/decisions/0008-istio-install-and-ingress-coexist.md`](../../02.architecture/decisions/0008-istio-install-and-ingress-coexist.md)
- **ADR-0009**: [`../../02.architecture/decisions/0009-kiali-external-observability.md`](../../02.architecture/decisions/0009-kiali-external-observability.md)
- **ADR-0014**: [`../../02.architecture/decisions/0014-current-local-gitops-platform-contract.md`](../../02.architecture/decisions/0014-current-local-gitops-platform-contract.md)
- **Platform Policy**: [`./0001-k8s-gitops-operations-policy.md`](./0001-k8s-gitops-operations-policy.md)

### Lifecycle Traceability

| Promoted owner | Control owner | Enforcement surface |
| --- | --- | --- |
| N/A — cert-manager, Istio, and Kiali controls derive from accepted architecture and current operations evidence, but no eligible upstream document carries a reciprocal policy link | Platform Owner for component and namespace controls | ClusterIssuer and CA-secret contract, namespace injection rules, Istio sync waves, and Kiali egress limits |
