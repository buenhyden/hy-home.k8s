# Platform Expansion Technical Specification

## Overview (KR)

이 문서는 플랫폼 확장(IP 수정, cert-manager, Kubernetes Dashboard, Istio, Kiali)의 기술 설계와 구현 계약을 정의한다. 기존 플랫폼 계약을 보전하면서 신규 컴포넌트와 수정 사항을 명시한다.

## Strategic Boundaries & Non-goals

- **Owns**: IP 계약 수정, cert-manager TLS 자동화, Dashboard/Istio/Kiali GitOps 설치, Traefik router 계약, 검증 스크립트 갱신
- **Does Not Own**: 외부 서비스 런타임, 외부 Traefik 라우팅 파일 실제 구현, Istio IngressGateway

## Related Inputs

- **PRD**: [`../../01.prd/2026-03-29-platform-expansion-dashboard-mesh.md`](../../01.prd/2026-03-29-platform-expansion-dashboard-mesh.md)
- **ARD**: [`../../02.ard/0003-platform-expansion-mesh-dashboard.md`](../../02.ard/0003-platform-expansion-mesh-dashboard.md)
- **ADR-0006**: [`../../03.adr/0006-cert-manager-mkcert-ca-issuer.md`](../../03.adr/0006-cert-manager-mkcert-ca-issuer.md)
- **ADR-0007**: [`../../03.adr/0007-kubernetes-dashboard-v3.md`](../../03.adr/0007-kubernetes-dashboard-v3.md)
- **ADR-0008**: [`../../03.adr/0008-istio-install-and-ingress-coexist.md`](../../03.adr/0008-istio-install-and-ingress-coexist.md)
- **ADR-0009**: [`../../03.adr/0009-kiali-external-observability.md`](../../03.adr/0009-kiali-external-observability.md)

---

## Phase 0: IP Subnet Correction

### Contracts (수정)

모든 외부 서비스 EndpointSlice 주소를 `172.30.0.x` → `172.19.0.x`로 수정한다.

| 서비스                  | K8s DNS                                              | IP            | Port    |
| ----------------------- | ---------------------------------------------------- | ------------- | ------- |
| vault-external          | `vault-external.platform.svc.cluster.local`          | `172.19.0.9`  | `8200`  |
| postgres-write-external | `postgres-write-external.platform.svc.cluster.local` | `172.19.0.11` | `15432` |
| postgres-read-external  | `postgres-read-external.platform.svc.cluster.local`  | `172.19.0.11` | `15433` |
| valkey-external         | `valkey-external.platform.svc.cluster.local`         | `172.19.0.12` | `6379`  |

### File-level Contract (수정 파일)

```
gitops/platform/external-services/vault-external.yaml          172.30.0.10 → 172.19.0.9
gitops/platform/external-services/postgres-external.yaml       172.30.0.11 → 172.19.0.11
gitops/platform/external-services/valkey-external.yaml         172.30.0.12 → 172.19.0.12
gitops/platform/network-policies/argocd-egress-*.yaml         cidr 172.30.0.12 → 172.19.0.12
gitops/platform/network-policies/egress-to-external-services.yaml  전체 cidr 수정
infrastructure/bootstrap-local.sh                              L15-19 기본값 수정
infrastructure/tests/verify-contracts-static.sh                172\.30\.0\. 패턴 → 172\.19\.0\.
```

---

## Phase 1: cert-manager

### Component Contract

| 항목               | 값                                            |
| ------------------ | --------------------------------------------- |
| Helm chart         | `cert-manager` @ `https://charts.jetstack.io` |
| Version            | `v1.17.x`                                     |
| Namespace          | `cert-manager`                                |
| CRD 설치           | `crds.enabled: true`                          |
| ClusterIssuer name | `mkcert-ca-issuer`                            |
| Issuer type        | CA (mkcert rootCA 참조)                       |
| rootCA Secret name | `mkcert-root-ca` (namespace: `cert-manager`)  |
| rootCA Secret key  | `tls.crt`, `tls.key`                          |

### Bootstrap 추가 단계

```bash
[NEW: 5.5/9] Inject mkcert rootCA into cert-manager namespace
kubectl -n cert-manager create secret tls mkcert-root-ca \
  --cert="$ROOT_CA_FILE" \
  --key="$ROOT_CA_KEY_FILE" \
  --dry-run=client -o yaml | kubectl apply -f -
```

> `ROOT_CA_KEY_FILE`은 mkcert rootCA 개인키 경로 (`secrets/certs/rootCA-key.pem`).

### File-level Contract (신규 파일)

```
gitops/platform/cert-manager/
  kustomization.yaml
  cluster-issuer-mkcert.yaml          # ClusterIssuer (mkcert-ca-issuer)
gitops/platform/namespaces/
  namespace-cert-manager.yaml         # namespace cert-manager
gitops/apps/root/
  platform-cert-manager-app.yaml      # ArgoCD Application
```

---

## Phase 2: Kubernetes Dashboard

### Component Contract

| 항목                    | 값                                                                |
| ----------------------- | ----------------------------------------------------------------- |
| Helm chart              | `kubernetes-dashboard` @ `https://kubernetes.github.io/dashboard` |
| Version                 | `v3.x`                                                            |
| Namespace               | `kubernetes-dashboard`                                            |
| Hostname                | `k8s-dashboard.127.0.0.1.nip.io`                                  |
| IngressClass            | `nginx`                                                           |
| TLS Secret              | `dashboard-tls` (cert-manager 발급)                               |
| cert-manager annotation | `cert-manager.io/cluster-issuer: mkcert-ca-issuer`                |
| RBAC                    | `dashboard-admin` SA + `cluster-admin` ClusterRoleBinding         |
| Auth                    | ServiceAccount Bearer Token                                       |
| Traefik router          | `dashboard-k3d` (외부 Traefik repo 관리)                          |

### Traefik Router Contract (외부 repo)

```yaml
# dashboard-k3d.yaml (외부 Traefik repo)
http:
  serversTransports:
    dashboard-k3d-transport:
      insecureSkipVerify: true
  services:
    dashboard-k3d:
      loadBalancer:
        passHostHeader: true
        serversTransport: dashboard-k3d-transport
        servers:
          - url: 'https://k3d-hyhome-serverlb:443'
  routers:
    dashboard-k3d:
      rule: 'Host(`k8s-dashboard.127.0.0.1.nip.io`)'
      entryPoints:
        - websecure
      service: dashboard-k3d
      tls: {}
```

### File-level Contract (신규 파일)

```
gitops/platform/dashboard/
  kustomization.yaml
  dashboard-ingress.yaml              # Ingress + cert-manager TLS
  dashboard-rbac.yaml                 # SA + ClusterRoleBinding
gitops/platform/namespaces/
  namespace-kubernetes-dashboard.yaml
gitops/apps/root/
  platform-dashboard-app.yaml
```

---

## Phase 3: Istio

### Component Contract

| 항목                            | 값                                                                                                |
| ------------------------------- | ------------------------------------------------------------------------------------------------- |
| istio-base chart                | `https://istio-release.storage.googleapis.com/charts`                                             |
| istiod chart                    | 동일                                                                                              |
| Version                         | `v1.25.x`                                                                                         |
| Namespace                       | `istio-system`                                                                                    |
| IngressGateway                  | `false` (비활성화)                                                                                |
| istiod pilot.resources.requests | `cpu: 100m, memory: 128Mi`                                                                        |
| Sidecar injection               | namespace opt-in (`istio-injection=enabled` label)                                                |
| Injection 제외 namespace        | `argocd`, `cert-manager`, `kubernetes-dashboard`, `ingress-nginx`, `external-secrets`, `platform` |

### File-level Contract (신규 파일)

```
gitops/platform/istio/
  kustomization.yaml
  istio-base-values.yaml
  istiod-values.yaml
gitops/platform/namespaces/
  namespace-istio-system.yaml
gitops/apps/root/
  platform-istio-base-app.yaml        # sync-wave: "1"
  platform-istiod-app.yaml            # sync-wave: "2"
```

---

## Phase 4: Kiali

### Component Contract

| 항목           | 값                                              |
| -------------- | ----------------------------------------------- |
| Helm chart     | `kiali-server` @ `https://kiali.io/helm-charts` |
| Version        | `v2.6.x`                                        |
| Namespace      | `istio-system`                                  |
| Prometheus URL | `http://172.19.0.20:9090`                       |
| Grafana URL    | `http://172.19.0.24:3000`                       |
| Tracing URL    | `http://172.19.0.22:3200`                       |
| Hostname       | `kiali.127.0.0.1.nip.io`                        |
| IngressClass   | `nginx`                                         |
| TLS Secret     | `kiali-tls` (cert-manager 발급)                 |
| Auth           | `anonymous` (로컬 전용)                         |
| Traefik router | `kiali-k3d` (외부 Traefik repo 관리)            |

### Traefik Router Contract (외부 repo)

```yaml
# kiali-k3d.yaml (외부 Traefik repo)
http:
  serversTransports:
    kiali-k3d-transport:
      insecureSkipVerify: true
  services:
    kiali-k3d:
      loadBalancer:
        passHostHeader: true
        serversTransport: kiali-k3d-transport
        servers:
          - url: 'https://k3d-hyhome-serverlb:443'
  routers:
    kiali-k3d:
      rule: 'Host(`kiali.127.0.0.1.nip.io`)'
      entryPoints:
        - websecure
      service: kiali-k3d
      tls: {}
```

### NetworkPolicy Egress (Kiali → Observability)

```yaml
egress:
  - to: [{ ipBlock: { cidr: 172.19.0.20/32 } }] # Prometheus
    ports: [{ protocol: TCP, port: 9090 }]
  - to: [{ ipBlock: { cidr: 172.19.0.24/32 } }] # Grafana
    ports: [{ protocol: TCP, port: 3000 }]
  - to: [{ ipBlock: { cidr: 172.19.0.22/32 } }] # Tempo
    ports: [{ protocol: TCP, port: 3200 }]
```

### File-level Contract (신규 파일)

```
gitops/platform/kiali/
  kustomization.yaml
  kiali-values.yaml                   # Prometheus/Grafana/Tempo URLs
  kiali-ingress.yaml                  # Ingress + cert-manager TLS
gitops/platform/network-policies/
  kiali-egress-to-observability.yaml
gitops/apps/root/
  platform-kiali-app.yaml             # sync-wave: "3"
```

---

## AppProject platform 갱신

```yaml
sourceRepos 추가:
  - https://charts.jetstack.io
  - https://kubernetes.github.io/dashboard
  - https://istio-release.storage.googleapis.com/charts
  - https://kiali.io/helm-charts

destinations 추가:
  - namespace: cert-manager
  - namespace: kubernetes-dashboard
  - namespace: istio-system

clusterResourceWhitelist 추가:
  - group: cert-manager.io, kind: Certificate
  - group: cert-manager.io, kind: ClusterIssuer
  - group: cert-manager.io, kind: Issuer
  - group: cert-manager.io, kind: CertificateRequest
  - group: networking.istio.io, kind: VirtualService
  - group: networking.istio.io, kind: DestinationRule
  - group: networking.istio.io, kind: Gateway
  - group: install.istio.io, kind: IstioOperator
```

---

## Access/TLS Contracts (전체 요약)

| Hostname                         | TLS Source                            | Traefik Router  | Status    |
| -------------------------------- | ------------------------------------- | --------------- | --------- |
| `argocd.127.0.0.1.nip.io`        | mkcert 수동 주입 (`argocd-local-tls`) | `argocd-k3d`    | 기존 유지 |
| `k8s-dashboard.127.0.0.1.nip.io` | cert-manager (`mkcert-ca-issuer`)     | `dashboard-k3d` | 신규      |
| `kiali.127.0.0.1.nip.io`         | cert-manager (`mkcert-ca-issuer`)     | `kiali-k3d`     | 신규      |

## Guardrails

- AppProject `apps`는 namespace wildcard 금지 유지.
- cert-manager ClusterIssuer는 `mkcert-ca-issuer` 단일 운영.
- Istio IngressGateway 비활성화 유지.
- rootCA Secret(`mkcert-root-ca`) 평문 커밋 금지.
- Kiali auth는 로컬 전용 anonymous — 프로덕션 배포 시 변경 필수.

## Failure Modes & Fallback

| Failure                             | Action                                                             |
| ----------------------------------- | ------------------------------------------------------------------ |
| cert-manager ClusterIssuer NotReady | rootCA Secret 재주입 → controller 재시작 확인                      |
| Dashboard 접근 불가                 | `dashboard-tls` Certificate 상태 확인 → cert-manager log           |
| Istiod CrashLoop                    | 자원 예산 초과 → requests 축소 또는 agent 노드 메모리 확인         |
| Kiali observability 연결 실패       | egress NetworkPolicy cidr 확인, Prometheus 172.19.0.20 가용성 확인 |
| IP 변경 후 연결 실패                | EndpointSlice 갱신 여부 및 verify-contracts 재실행                 |

## Verification

```bash
# Static
bash -n infrastructure/bootstrap-local.sh infrastructure/tests/*.sh
./infrastructure/tests/verify-contracts-static.sh

# Runtime
./infrastructure/tests/run-all.sh
CHECK_TRAEFIK_443=true ./infrastructure/tests/verify-ingress-tls.sh

# cert-manager
kubectl -n cert-manager get clusterissuer mkcert-ca-issuer -o jsonpath='{.status.conditions[0].type}'

# Dashboard
kubectl -n kubernetes-dashboard get certificate dashboard-tls

# Istio
kubectl -n istio-system get deployment istiod

# Kiali
kubectl -n istio-system get deployment kiali
```

## Success Criteria

- **VAL-SPC-001**: `verify-contracts-static.sh` PASS (IP 수정 반영).
- **VAL-SPC-002**: cert-manager `ClusterIssuer` `mkcert-ca-issuer` Ready=True.
- **VAL-SPC-003**: `k8s-dashboard.127.0.0.1.nip.io` HTTPS 200 (mkcert CA 신뢰).
- **VAL-SPC-004**: `istiod` Deployment Available=True.
- **VAL-SPC-005**: `kiali.127.0.0.1.nip.io` HTTPS 200 (mkcert CA 신뢰).
- **VAL-SPC-006**: Kiali UI에서 Prometheus 연결 상태 정상.
- **VAL-SPC-007**: CI 전체 게이트 PASS.

## Related Documents

- **Plan**: [`../../05.plans/2026-03-29-platform-expansion.md`](../../05.plans/2026-03-29-platform-expansion.md)
- **Tasks**: [`../../06.tasks/2026-03-29-platform-expansion.md`](../../06.tasks/2026-03-29-platform-expansion.md)
- **Guide**: [`../../07.guides/0003-platform-expansion-bootstrap-guide.md`](../../07.guides/0003-platform-expansion-bootstrap-guide.md)
- **Runbook**: [`../../09.runbooks/0003-platform-expansion-bootstrap-runbook.md`](../../09.runbooks/0003-platform-expansion-bootstrap-runbook.md)
