# Service Mesh & cert-manager Operations Policy

## Overview (KR)

이 문서는 cert-manager(TLS 자동화), Kubernetes Dashboard, Istio(서비스메시), Kiali(메시 관측) 운영 통제 기준을 정의한다.
플랫폼 확장 컴포넌트의 보안 정책, 갱신 제약, 허용/금지 작업을 명시한다.

## Policy Scope

- cert-manager + mkcert ClusterIssuer(`mkcert-ca-issuer`)
- Kubernetes Dashboard v3
- Istio(istiod) + sidecar 주입 정책
- Kiali + 외부 Observability 연동
- Traefik router 계약 (외부 repo)

## Applies To

- **Systems**: `gitops/platform/{cert-manager,dashboard,istio,kiali}/`, `infrastructure/bootstrap-local.sh`
- **Agents**: 문서/운영 자동화 에이전트
- **Environments**: WSL2 local cluster

## Controls

### TLS / cert-manager

- **Required**:
  - ClusterIssuer 단일 운영: `mkcert-ca-issuer` (CA type, mkcert rootCA 참조)
  - rootCA Secret 이름 고정: `mkcert-root-ca` (namespace: `cert-manager`, key: `tls.crt` / `tls.key`)
  - ArgoCD TLS는 `argocd-local-tls` Secret 수동 주입 유지 — cert-manager 이관 금지
  - `rootCA.pem`은 로컬 신뢰 저장소에 등록 후 HTTPS 접근
  - `secrets/certs/rootCA-key.pem` 파일을 평문 커밋 금지
- **Allowed**:
  - `kubectl -n cert-manager rollout restart deploy/cert-manager` 기반 컨트롤러 재시작
  - ClusterIssuer 상태 확인: `kubectl get clusterissuer mkcert-ca-issuer`
- **Disallowed**:
  - `mkcert-root-ca` Secret 평문 커밋
  - ClusterIssuer 다중 운영 (이름 오염 위험)

### Kubernetes Dashboard

- **Required**:
  - namespace: `kubernetes-dashboard`
  - hostname: `k8s-dashboard.127.0.0.1.nip.io`
  - 인증: ServiceAccount Bearer Token (`dashboard-admin`)
  - RBAC: `cluster-admin` ClusterRoleBinding — 로컬 전용으로 제한
  - TLS: cert-manager 발급 (`dashboard-tls` Certificate CR)
- **Allowed**:
  - 토큰 갱신: `kubectl -n kubernetes-dashboard create token dashboard-admin --duration=24h`
- **Disallowed**:
  - 프로덕션 환경에 `cluster-admin` 권한 유지 (최소권한 재검토 필수)
  - 익명(anonymous) 접근 활성화

### Istio / Service Mesh

- **Required**:
  - IngressGateway 비활성화 유지 (`gateways.enabled: false`)
  - sidecar 주입 opt-in: namespace `istio-injection=enabled` 레이블 명시적 부여
  - istiod 자원 예산: `cpu: 100m, memory: 128Mi` (requests)
  - sync-wave 순서 강제: `istio-base(wave:1)` → `istiod(wave:2)`
- **Allowed**:
  - Mesh 내 namespace에 `istio-injection=enabled` 레이블 추가
- **Disallowed**:
  - `argocd`, `cert-manager`, `kubernetes-dashboard`, `ingress-nginx`, `external-secrets`, `platform` namespace에 `istio-injection=enabled` 레이블 부여
  - IngressGateway 활성화
  - Ambient mesh 전환(로컬 플랫폼 스코프 외)

### Kiali / Observability

- **Required**:
  - auth: `anonymous` (로컬 전용)
  - Prometheus: `http://172.19.0.20:9090`
  - Grafana: `http://172.19.0.24:3000`
  - Tempo(Tracing): `http://172.19.0.22:3200`
  - egress NetworkPolicy: `172.19.0.20/32`, `172.19.0.22/32`, `172.19.0.24/32` cidr 허용
  - hostname: `kiali.127.0.0.1.nip.io`, TLS: cert-manager 발급 (`kiali-tls`)
- **Disallowed**:
  - 프로덕션에 anonymous auth 유지
  - Kiali egress를 `0.0.0.0/0` 등 광역 cidr로 확장

### Traefik Router 계약

- **Required**:
  - 외부 Traefik repo에서 `dashboard-k3d.yaml`, `kiali-k3d.yaml` 라우터 관리
  - `insecureSkipVerify: true`, `passHostHeader: true` 유지 (Traefik → k3d TLS 특성)
  - 라우터 규칙 hostname과 ArgoCD Application Ingress hostname 일치 유지
- **Disallowed**:
  - 본 repo에서 Traefik 라우팅 파일 직접 배포

## CI Governance

- `verify-contracts-static.sh` PASS가 모든 IP/endpoint 변경의 선행 조건이다.
- `bash -n` 정적 문법 검증 후 bootstrap-local.sh 변경을 반영한다.
- cert-manager/Dashboard/Istio/Kiali GitOps 리소스는 AppProject `platform` 스코프 내에서만 배포된다.

## Exceptions

- rootCA 재발급 시 `mkcert-root-ca` Secret 재주입 후 cert-manager controller 재시작 허용.
- Istio istiod CrashLoop 시 자원 requests 축소 허용 (단, 128Mi 미만으로 낮추지 않음).

## Related Documents

- **Spec**: [`../04.specs/003-platform-expansion/spec.md`](../04.specs/003-platform-expansion/spec.md)
- **Runbook**: [`../09.runbooks/0003-platform-expansion-bootstrap-runbook.md`](../09.runbooks/0003-platform-expansion-bootstrap-runbook.md)
- **Guide**: [`../07.guides/0003-platform-expansion-bootstrap-guide.md`](../07.guides/0003-platform-expansion-bootstrap-guide.md)
- **ADR-0006**: [`../03.adr/0006-cert-manager-mkcert-ca-issuer.md`](../03.adr/0006-cert-manager-mkcert-ca-issuer.md)
- **ADR-0007**: [`../03.adr/0007-kubernetes-dashboard-v3.md`](../03.adr/0007-kubernetes-dashboard-v3.md)
- **ADR-0008**: [`../03.adr/0008-istio-install-and-ingress-coexist.md`](../03.adr/0008-istio-install-and-ingress-coexist.md)
- **ADR-0009**: [`../03.adr/0009-kiali-external-observability.md`](../03.adr/0009-kiali-external-observability.md)
- **Previous Policy**: [`./0002-wsl2-k3d-gitops-ha-operations-policy.md`](./0002-wsl2-k3d-gitops-ha-operations-policy.md)
