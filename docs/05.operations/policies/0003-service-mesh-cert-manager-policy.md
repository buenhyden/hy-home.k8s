---
title: "Service Mesh & cert-manager Operations Policy"
version: "1.5.1"
type: "operation/policy"
status: "active"
owner: "platform"
updated: "2026-11-17"
artifact_id: "POL-0003"
---

# Service Mesh & cert-manager Operations Policy

## Purpose and Scope

### Objective

이 문서는 cert-manager(TLS 자동화), Istio(서비스메시), Kiali(메시 관측) 운영 통제 기준을 정의한다.
플랫폼 확장 컴포넌트의 보안 정책, 갱신 제약, 허용/금지 작업을 명시한다.
클러스터 UI(Headlamp) 통제는 [POL-0004](./0004-rollouts-notifications-headlamp-policy.md),
k8s router와 live 변경 예외의 공통 기준은 [POL-0001](./0001-k8s-gitops-operations-policy.md)이 소유한다.

### Applies To

- cert-manager + mkcert ClusterIssuer(`mkcert-ca-issuer`)
- Istio(istiod) + sidecar 주입 정책
- Kiali + 외부 Observability 연동

- **Systems**: `gitops/platform/{cert-manager,kiali}/`, `gitops/apps/root/platform-istio-base-app.yaml`, `gitops/apps/root/platform-istio-cni-app.yaml`, `gitops/apps/root/platform-istiod-app.yaml`, `infrastructure/bootstrap-local.sh`
- **Agents**: 문서/운영 자동화 에이전트
- **Environments**: Linux server local cluster

#### Exclusions

이 정책은 범위에서 제외한다고 따로 표시한 항목을 Applies To에 두지 않으며, 금지 작업은 위 Requirements의 Disallowed 항목에 적혀 있다.

## Rules

### Requirements

| Rule ID | Condition | Level | Evidence | Status |
| --- | --- | --- | --- | --- |
| MESH-R001 | Always | required | RUN-0003 | active |
| MESH-R002 | Always | required | RUN-0003 | active |
| MESH-R003 | Always | required | `infrastructure-contracts` | active |
| MESH-R004 | HTTPS 접근 전 | required | RUN-0003 | active |
| MESH-R005 | Always | required | `secret-handling` | active |
| MESH-R006 | 운영자 승인 후 | required | RUN-0003 | active |
| MESH-R007 | Always | optional | RUN-0003 | active |
| MESH-R008 | Always | required | `policy-gates` | active |
| MESH-R009 | Always | required | Semantic review | active |
| MESH-R010 | Always | required | Semantic review | active |
| MESH-R011 | Always | required | Semantic review | active |
| MESH-R012 | Always | required | RUN-0003 | active |
| MESH-R013 | Always | required | RUN-0003 | active |
| MESH-R014 | Mesh 내 namespace일 때 | optional | Semantic review | active |
| MESH-R015 | Always | required | Semantic review | active |
| MESH-R016 | Always | required | Semantic review | active |
| MESH-R017 | Always | required | Semantic review | active |
| MESH-R018 | Always | required | Semantic review | active |
| MESH-R019 | Always | required | Semantic review | active |
| MESH-R020 | Always | required | RUN-0003 | active |
| MESH-R021 | Always | required | RUN-0003 | active |
| MESH-R022 | Always | required | `infrastructure-contracts` | active |
| MESH-R023 | Always | required | RUN-0003 | active |
| MESH-R024 | Always | required | `infrastructure-contracts` | active |
| MESH-R025 | Always | required | RUN-0003 | active |
| MESH-R026 | Always | required | Semantic review | active |
| MESH-R027 | Always | required | Semantic review | active |
| MESH-R028 | 모든 IP/endpoint 변경 시 | required | `infrastructure-contracts` | active |
| MESH-R029 | bootstrap-local.sh 변경 시 | required | `selected-style` | active |
| MESH-R030 | Always | required | `infrastructure-contracts` | active |

#### TLS / cert-manager

- **Required**:
  - `MESH-R001` ClusterIssuer 단일 운영: `mkcert-ca-issuer` (CA type, mkcert rootCA 참조)
  - `MESH-R002` rootCA Secret 이름 고정: `mkcert-root-ca` (namespace: `cert-manager`, key: `tls.crt` / `tls.key`)
  - `MESH-R003` ArgoCD TLS는 `argocd-local-tls` Secret 수동 주입 유지 — cert-manager 이관 금지
  - `MESH-R004` `rootCA.pem`은 로컬 신뢰 저장소에 등록 후 HTTPS 접근
  - `MESH-R005` `secrets/certs/rootCA-key.pem` 파일을 평문 커밋 금지
- **Allowed**:
  - `MESH-R006` cert-manager controller 재시작은 운영자 승인 후 [플랫폼 확장 런북](../runbooks/0003-platform-expansion-bootstrap-runbook.md)의 절차로 수행
  - `MESH-R007` ClusterIssuer 상태 확인은 [플랫폼 확장 런북](../runbooks/0003-platform-expansion-bootstrap-runbook.md)의 검증 절차로 수행
- **Disallowed**:
  - `MESH-R008` `mkcert-root-ca` Secret 평문 커밋
  - `MESH-R009` ClusterIssuer 다중 운영 (이름 오염 위험)

#### Istio / Service Mesh

- **Required**:
  - `MESH-R010` IngressGateway를 선언하지 않는다 (istiod Application values에 gateway 없음, ADR-0008)
  - `MESH-R011` sidecar 주입 opt-in: namespace `istio-injection=enabled` 레이블 명시적 부여
  - `MESH-R012` istiod 자원 예산: `cpu: 100m, memory: 128Mi` (requests)
  - `MESH-R013` sync-wave 순서 강제: `istio-base`·`istio-cni`(wave:1) → `istiod`(wave:2, `pilot.cni.enabled: true`)
- **Allowed**:
  - `MESH-R014` Mesh 내 namespace에 `istio-injection=enabled` 레이블 추가
- **Disallowed**:
  - `MESH-R015` `argocd`, `cert-manager`, `headlamp`, `external-secrets`, `platform` namespace에 `istio-injection=enabled` 레이블 부여
  - `MESH-R016` mesh 대상인 [`apps`](../../../gitops/platform/namespaces/namespace-apps.yaml)와 [`traefik`](../../../gitops/platform/namespaces/namespace-traefik.yaml)의 `istio-injection=enabled` 레이블 제거
  - `MESH-R017` IngressGateway 활성화
  - `MESH-R018` Ambient mesh 전환(로컬 플랫폼 스코프 외)

#### Kiali / Observability

- **Required**:
  - `MESH-R019` auth: `anonymous` (로컬 전용)
  - `MESH-R020` Prometheus: `https://prometheus.hy.home.arpa`, Basic Auth `secret:kiali-prometheus-auth:*`
  - `MESH-R021` Grafana: `in_cluster_url`과 브라우저 링크 `url` 모두 `https://grafana.hy.home.arpa`, bearer `secret:kiali-grafana-auth:token`(Viewer service account)
  - `MESH-R022` gateway CA: `istio-system/kiali-cabundle` (bootstrap 생성)
  - `MESH-R023` Tempo(Tracing): `in_cluster_url` `http://tempo-external.platform.svc.cluster.local:3200`
  - `MESH-R024` egress NetworkPolicy: host 주소 `192.168.0.13/32`의 `443`, `3200` 허용 (ADR-0046)
  - `MESH-R025` hostname: `kiali.hy-k8s.home.arpa`, TLS: cert-manager 발급 (`kiali-tls`)
- **Disallowed**:
  - `MESH-R026` 프로덕션에 anonymous auth 유지
  - `MESH-R027` Kiali egress를 `0.0.0.0/0` 등 광역 cidr로 확장

#### CI Governance

- `MESH-R028` `scripts/validate-infrastructure-contracts.sh` PASS가 모든 IP/endpoint
  변경의 선행 조건이다. 이 검사의 선택과 실행은 QA 실행 레지스트리가 소유한다.
- `MESH-R029` shell syntax 정적 검증 후 bootstrap-local.sh 변경을 반영한다.
- `MESH-R030` cert-manager/Istio/Kiali GitOps 리소스는 AppProject `platform` 스코프 내에서만 배포된다.

### Exceptions

- rootCA 재발급 시 `mkcert-root-ca` Secret 재주입 후 cert-manager controller 재시작 허용.
- Istio istiod CrashLoop가 관측되어 requests 변경이 필요한 경우 Platform Owner가
  현재 `gitops/apps/root/platform-istiod-app.yaml`의 requests(`100m`, `128Mi`)와
  limits(`500m`, `512Mi`), 실패 증상, 변경안과 rollback을 검토한다. 변경안의
  memory request는 128Mi 아래로 낮추지 않는다. Platform Owner 승인과
  [POL-0001의 live 예외](./0001-k8s-gitops-operations-policy.md#exceptions)가
  필요한 실행은 운영자에게 넘기고 실제 조정 결과를 별도 증거로 기록한다.

#### Approval and Review

예외 승인은 위 Exceptions의 Platform Owner 검토와 POL-0001의 live 예외 승인을 따른다.

## Enforcement

### Mechanisms

- endpoint와 TLS 경계 계약 검증 증적을 남긴다.
- cert-manager/Istio/Kiali 변경 후 관련 GitOps manifest와 runbook의 계약 값이 일치하는지 확인한다.

- 플랫폼 컴포넌트 버전 변경 시마다 검토한다.
- cert-manager, Istio, Kiali 관련 ADR 변경 시 같은 변경에서 검토한다.
- CA·TLS와 외부 Kiali 연결의 제품 측정 기준은
  [REQ-0004의 Secret TLS 복구](../../01.requirements/0004-current-local-gitops-platform.md#quality-scenario-secret-tls-recovery)와
  [외부 인터페이스](../../01.requirements/0004-current-local-gitops-platform.md#quality-scenario-external-interface)에
  둔다. 이 정책의 현재 설정 확인은 복구 시간이나 실제 연결 성공을 증명하지 않는다.

- **Runbook**: [`../runbooks/0003-platform-expansion-bootstrap-runbook.md`](../runbooks/0003-platform-expansion-bootstrap-runbook.md)

### Limits

이 정책의 현재 구성 검사는 CA, TLS, 외부 Kiali 경로의 복구 시간이나 실제 연결 성공을 증명하지 않는다. 그 경로들의 측정 기준은 REQ-0004의 Secret TLS 복구와 외부 인터페이스 시나리오가 소유한다.

## Ownership

### Owner

- **Architecture**: [AD-0007](../../02.architecture/descriptions/0007-current-local-gitops-platform.md)
- **ADR-0006**: [`../../02.architecture/decisions/0006-cert-manager-mkcert-ca-issuer.md`](../../02.architecture/decisions/0006-cert-manager-mkcert-ca-issuer.md)
- **ADR-0008**: [`../../02.architecture/decisions/0008-istio-install-and-ingress-coexist.md`](../../02.architecture/decisions/0008-istio-install-and-ingress-coexist.md)
- **ADR-0009**: [`../../02.architecture/decisions/0009-kiali-external-observability.md`](../../02.architecture/decisions/0009-kiali-external-observability.md)
- **ADR-0014**: [`../../02.architecture/decisions/0014-current-local-gitops-platform-contract.md`](../../02.architecture/decisions/0014-current-local-gitops-platform-contract.md)
- **Platform Policy**: [`./0001-k8s-gitops-operations-policy.md`](./0001-k8s-gitops-operations-policy.md)

#### Responsibilities

책임 주체는 아래 Lifecycle Traceability 표의 Control owner 열에 적혀 있다.

### Review Triggers

변경 검토 시점은 위 Enforcement의 컴포넌트 버전 변경 및 ADR 변경 항목을 따른다.

### Lifecycle Traceability

- **Current control review**: SPEC-0106 (left the tree; Git history recovers it)의 과거 review는 이 정책을 istiod source와 비교했다. 원래 promotion 승인이나 live 도입 증적이 아니다.

| Promoted owner | Control owner | Enforcement surface |
| --- | --- | --- |
| N/A — cert-manager, Istio, and Kiali controls derive from accepted architecture and current operations evidence, but no eligible upstream document is available to link as the promoting owner | Platform Owner for component and namespace controls | ClusterIssuer and CA-secret contract, namespace injection rules, Istio sync waves, and Kiali egress limits |
