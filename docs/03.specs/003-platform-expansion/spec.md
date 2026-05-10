# Platform Expansion Technical Specification

## Overview (KR)

이 문서는 플랫폼 확장(IP 수정, cert-manager, Kubernetes Dashboard, Istio, Kiali)의 기술 설계와 구현 계약을 정의한다. 기존 플랫폼 계약을 보전하면서 신규 컴포넌트와 수정 사항을 명시한다.

> **현재 실행계약 메모 (2026-05-09)**: 이 Spec은 2026-03-29 플랫폼 확장 설계 기록이다. 현재 repo-backed 실행계약은 [ADR-0010](../../02.architecture/decisions/0010-headlamp-replaces-dashboard.md)과 현재 `gitops/**` 매니페스트/정적 검증 스크립트가 우선한다. Kubernetes Dashboard는 Headlamp로 대체되었고, 외부 서비스 EndpointSlice/CIDR 계약은 `172.18.x` 기준이다.

## Strategic Boundaries & Non-goals

- **Owns**: IP 계약 수정, cert-manager TLS 자동화, Dashboard/Istio/Kiali GitOps 설치, Traefik router 계약, 검증 스크립트 갱신
- **Does Not Own**: 외부 서비스 런타임, 외부 Traefik 라우팅 파일 실제 구현, Istio IngressGateway

## Related Inputs

- **PRD**: [`../../01.requirements/2026-03-29-platform-expansion-dashboard-mesh.md`](../../01.requirements/2026-03-29-platform-expansion-dashboard-mesh.md)
- **ARD**: [`../../02.architecture/requirements/0003-platform-expansion-mesh-dashboard.md`](../../02.architecture/requirements/0003-platform-expansion-mesh-dashboard.md)
- **ADR-0006**: [`../../02.architecture/decisions/0006-cert-manager-mkcert-ca-issuer.md`](../../02.architecture/decisions/0006-cert-manager-mkcert-ca-issuer.md)
- **ADR-0007**: [`../../02.architecture/decisions/0007-kubernetes-dashboard-v3.md`](../../02.architecture/decisions/0007-kubernetes-dashboard-v3.md)
- **ADR-0008**: [`../../02.architecture/decisions/0008-istio-install-and-ingress-coexist.md`](../../02.architecture/decisions/0008-istio-install-and-ingress-coexist.md)
- **ADR-0009**: [`../../02.architecture/decisions/0009-kiali-external-observability.md`](../../02.architecture/decisions/0009-kiali-external-observability.md)

---

## Contracts

- **Config Contract**: GitOps manifests under `gitops/platform/**` and root ArgoCD Applications under `gitops/apps/root/**`.
- **Data / Interface Contract**: external service EndpointSlices, cert-manager TLS resources, ingress hostnames, and observability endpoint URLs.
- **Governance Contract**: changes are reviewed through GitOps paths; direct cluster mutation appears only as human-approved bootstrap or break-glass context.

## Core Design

- Phase-based platform expansion keeps each component independently reviewable while sharing the same root app reconciliation model.
- cert-manager owns local TLS issuance for platform UI endpoints.
- Dashboard-era UI contracts are retained as historical design evidence and superseded by the current Headlamp ADR and live manifests.
- Istio and Kiali are optional platform expansion components and do not replace the ingress-nginx local access contract.

## Data Modeling & Storage Strategy

- This spec does not introduce application data models or storage migrations.
- Platform state is modeled as Kubernetes desired state, Helm values, EndpointSlices, and NetworkPolicies.
- External observability and secret systems remain outside the k3d cluster; only their interface contracts are represented here.

## Interfaces & Data Structures

### Core Interfaces

- ArgoCD Application manifests under `gitops/apps/root/`
- component Kustomizations and Helm values under `gitops/platform/`
- Traefik dynamic config snippets maintained outside this GitOps repo
- static verification scripts under `infrastructure/tests/`

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

```text
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
# human-approved bootstrap only
kubectl -n cert-manager create secret tls mkcert-root-ca \
  --cert="$ROOT_CA_FILE" \
  --key="$ROOT_CA_KEY_FILE" \
  --dry-run=client -o yaml | kubectl apply -f -
```

> `ROOT_CA_KEY_FILE`은 mkcert rootCA 개인키 경로 (`secrets/certs/rootCA-key.pem`).

### File-level Contract (신규 파일)

```text
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

```text
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

```text
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
| Helm chart     | `kiali-server` @ `https://kiali.org/helm-charts` |
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

```text
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
  - https://kiali.org/helm-charts

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

## Edge Cases & Error Handling

- The historical Dashboard sections are superseded by Headlamp and must not be used as current deployment instructions.
- External service IP contracts may differ between historical design notes and current repo-backed manifests; current GitOps manifests and static tests take precedence.
- cert-manager, mesh, and observability components may be partially installed during bootstrap; verification should check each component independently before treating the platform as ready.

## Failure Modes & Fallback / Human Escalation

| Failure                             | Fallback                                                           | Human Escalation                                                    |
| ----------------------------------- | ------------------------------------------------------------------ | ------------------------------------------------------------------- |
| cert-manager ClusterIssuer NotReady | rootCA Secret 상태와 controller log 확인                           | Secret reinjection은 human-approved bootstrap 절차로만 수행         |
| Dashboard 접근 불가                 | 현재 Headlamp ADR과 live manifests 우선 확인                       | Dashboard 복구가 아니라 Headlamp 경로 검증으로 전환                 |
| Istiod CrashLoop                    | 자원 예산 확인 후 requests 조정 PR 작성                            | runtime patch 대신 GitOps 변경 PR로 처리                            |
| Kiali observability 연결 실패       | egress NetworkPolicy cidr 확인, Prometheus 172.19.0.20 가용성 확인 | 외부 observability endpoint 변경 시 reference snapshot 함께 갱신    |
| IP 변경 후 연결 실패                | EndpointSlice 갱신 여부 및 verify-contracts 재실행                 | static contract가 틀렸다면 spec, operation, script를 같은 PR로 보정 |

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

## Success Criteria & Verification Plan

- **VAL-SPC-001**: `verify-contracts-static.sh` PASS (IP 수정 반영).
- **VAL-SPC-002**: cert-manager `ClusterIssuer` `mkcert-ca-issuer` Ready=True.
- **VAL-SPC-003**: `k8s-dashboard.127.0.0.1.nip.io` HTTPS 200 (mkcert CA 신뢰).
- **VAL-SPC-004**: `istiod` Deployment Available=True.
- **VAL-SPC-005**: `kiali.127.0.0.1.nip.io` HTTPS 200 (mkcert CA 신뢰).
- **VAL-SPC-006**: Kiali UI에서 Prometheus 연결 상태 정상.
- **VAL-SPC-007**: CI 전체 게이트 PASS.

## Related Documents

- **Plan**: [`../../04.execution/plans/2026-03-29-platform-expansion.md`](../../04.execution/plans/2026-03-29-platform-expansion.md)
- **Tasks**: [`../../04.execution/tasks/2026-03-29-platform-expansion.md`](../../04.execution/tasks/2026-03-29-platform-expansion.md)
- **Guide**: [`../../05.operations/guides/0003-platform-expansion-bootstrap-guide.md`](../../05.operations/guides/0003-platform-expansion-bootstrap-guide.md)
- **Runbook**: [`../../05.operations/runbooks/0003-platform-expansion-bootstrap-runbook.md`](../../05.operations/runbooks/0003-platform-expansion-bootstrap-runbook.md)
