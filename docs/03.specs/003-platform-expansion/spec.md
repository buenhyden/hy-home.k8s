---
title: 'Platform Expansion Technical Specification'
type: spec
status: active
owner: platform-team
updated: 2026-05-18
---

# Platform Expansion Specification

## Overview (KR)

이 문서는 cert-manager, Headlamp, Istio, Kiali, external service endpoint 계약의 현재 기술 명세다.
현재 실행계약은 `gitops/**` 매니페스트, 정적 검증 스크립트, ADR-0010을 기준으로 한다.

Dashboard와 `172.19.x` 값은 2026-03-29 설계 당시의 historical/superseded 기록으로만 보존한다.
현재 UI 계약은 Headlamp이며, 현재 external service/observability endpoint 계약은 `172.18.x` 기준이다.

## Strategic Boundaries & Non-goals

- **Owns**: cert-manager TLS 자동화, Headlamp UI 접근, Istio control plane, Kiali observability UI, external service/observability endpoint 정적 계약.
- **Does Not Own**: 외부 Docker observability 런타임, 외부 Traefik repository 적용, live cluster mutation, plaintext secret 생성.
- **Superseded Boundary**: Kubernetes Dashboard 배포 계약과 `172.19.x` endpoint 값은 현재 배포 지침이 아니다.

## Related Inputs

- **PRD**: [`../../01.requirements/2026-03-29-platform-expansion-dashboard-mesh.md`](../../01.requirements/2026-03-29-platform-expansion-dashboard-mesh.md)
- **ARD**: [`../../02.architecture/requirements/0003-platform-expansion-mesh-dashboard.md`](../../02.architecture/requirements/0003-platform-expansion-mesh-dashboard.md)
- **ADR-0006**: [`../../02.architecture/decisions/0006-cert-manager-mkcert-ca-issuer.md`](../../02.architecture/decisions/0006-cert-manager-mkcert-ca-issuer.md)
- **ADR-0007**: [`../../02.architecture/decisions/0007-kubernetes-dashboard-v3.md`](../../02.architecture/decisions/0007-kubernetes-dashboard-v3.md)
- **ADR-0008**: [`../../02.architecture/decisions/0008-istio-install-and-ingress-coexist.md`](../../02.architecture/decisions/0008-istio-install-and-ingress-coexist.md)
- **ADR-0009**: [`../../02.architecture/decisions/0009-kiali-external-observability.md`](../../02.architecture/decisions/0009-kiali-external-observability.md)
- **ADR-0010**: [`../../02.architecture/decisions/0010-headlamp-replaces-dashboard.md`](../../02.architecture/decisions/0010-headlamp-replaces-dashboard.md)

## Contracts

- **Config Contract**: Current platform expansion resources are declared by root ArgoCD Applications under `gitops/apps/root/**` and component manifests under `gitops/platform/**`.
- **Data / Interface Contract**: External services and observability endpoints use current `172.18.x` EndpointSlice and NetworkPolicy values.
- **Governance Contract**: Changes flow through GitOps review and static validation. Agents must not run direct cluster-mutating commands.

### Current Config Contract

| Area | Current source |
| --- | --- |
| cert-manager chart | `gitops/apps/root/platform-cert-manager-app.yaml` |
| cert-manager config | `gitops/apps/root/platform-cert-manager-config-app.yaml`, `gitops/platform/cert-manager/` |
| Headlamp chart | `gitops/apps/root/platform-headlamp-app.yaml` |
| Headlamp ingress config | `gitops/apps/root/platform-headlamp-config-app.yaml`, `gitops/platform/headlamp/` |
| Istio base | `gitops/apps/root/platform-istio-base-app.yaml` |
| Istiod | `gitops/apps/root/platform-istiod-app.yaml` |
| Kiali chart | `gitops/apps/root/platform-kiali-app.yaml` |
| Kiali ingress config | `gitops/apps/root/platform-kiali-config-app.yaml`, `gitops/platform/kiali/` |
| external services | `gitops/platform/external-services/` |
| egress policy | `gitops/platform/network-policies/` |
| static contract tests | `infrastructure/tests/verify-contracts-static.sh` |

### Current Interface Contract

| Interface | Current value | Source |
| --- | --- | --- |
| Vault external endpoint | `172.18.0.8:8200` | `gitops/platform/external-services/vault-external.yaml` |
| Valkey external endpoint | `172.18.0.9:6379` | `gitops/platform/external-services/valkey-external.yaml` |
| Prometheus external endpoint | `172.18.0.10:9090` | `gitops/platform/external-services/prometheus-external.yaml` |
| Tempo external endpoint | `172.18.0.12:3200` | `gitops/platform/external-services/tempo-external.yaml` |
| Grafana external endpoint | `172.18.0.14:3000` | `gitops/platform/external-services/grafana-external.yaml` |
| PostgreSQL external endpoint | `172.18.0.15:15432`, `172.18.0.15:15433` | `gitops/platform/external-services/postgres-external.yaml` |
| Headlamp host | `headlamp.127.0.0.1.nip.io` | `gitops/platform/headlamp/headlamp-ingress.yaml` |
| Kiali host | `kiali.127.0.0.1.nip.io/kiali` | `gitops/platform/kiali/kiali-ingress.yaml` |
| TLS issuer | `mkcert-ca-issuer` | `gitops/platform/cert-manager/cluster-issuer-mkcert.yaml` |

## Core Design

- cert-manager owns local TLS issuance through a single `mkcert-ca-issuer` ClusterIssuer.
- Headlamp is the current Kubernetes UI surface and replaces Kubernetes Dashboard for local platform inspection.
- Istio is installed without replacing ingress-nginx as the local ingress boundary.
- Kiali provides mesh observability and reads external Prometheus, Grafana, and Tempo through in-cluster service DNS plus `172.18.x` egress policy.
- External services remain represented as Kubernetes Service and EndpointSlice objects, while the actual runtimes remain outside this repo.

## Data Modeling & Storage Strategy

- This spec does not introduce application data models, persistent volumes, or migrations.
- Platform state is modeled as Kubernetes desired state: ArgoCD Applications, Helm values, Kustomizations, Services, EndpointSlices, Ingresses, and NetworkPolicies.
- External secret material remains outside Git. TLS secret names may appear in manifests, but secret values must not be committed.

## Interfaces & Data Structures

### Core Interfaces

```text
ArgoCD Application -> Helm chart or Git path -> Namespace-scoped platform component
External runtime -> EndpointSlice 172.18.x address -> Kubernetes Service DNS
Ingress host -> ingress-nginx -> service backend -> cert-manager TLS secret name
Kiali -> Service DNS / egress NetworkPolicy -> external observability runtime
```

### Component Interfaces

| Component | Interface |
| --- | --- |
| cert-manager | `ClusterIssuer/mkcert-ca-issuer` issues local TLS certificates. |
| Headlamp | `Ingress/headlamp` exposes `https://headlamp.127.0.0.1.nip.io/`. |
| Istio | `Deployment/istiod` provides mesh control plane without enabling Istio IngressGateway. |
| Kiali | `Ingress/kiali` exposes `/kiali` and reads Prometheus/Grafana/Tempo through configured URLs. |
| external services | EndpointSlices pin repo-backed `172.18.x` addresses for Vault, Valkey, PostgreSQL, and observability runtimes. |

## Historical/Superseded Contract Record

This section preserves historical design evidence only. It is not a deployment instruction.

- `172.19.x` endpoint values from the 2026-03-29 platform expansion design are superseded by current `172.18.x` GitOps manifests and static contract tests.
- Kubernetes Dashboard, `k8s-dashboard.127.0.0.1.nip.io`, `dashboard-tls`, `platform-dashboard-app.yaml`, and `kubernetes-dashboard` namespace references are superseded by Headlamp.
- ADR-0007 remains historical decision context; ADR-0010 is the current UI decision record.
- If a future task needs to restore Dashboard, it must create a new PRD/ARD/Spec/Plan/Task chain instead of reusing this superseded section as an implementation contract.

### Superseded Snapshot

| Historical item | Superseded by |
| --- | --- |
| `172.19.x` external endpoint notes | current `172.18.x` endpoint manifests and `verify-contracts-static.sh` |
| Kubernetes Dashboard UI | Headlamp via ADR-0010 and `gitops/platform/headlamp/` |
| `dashboard-tls` certificate | `headlamp-tls` for Headlamp and `kiali-tls` for Kiali |
| `platform-dashboard-app.yaml` | `platform-headlamp-app.yaml` and `platform-headlamp-config-app.yaml` |

## Edge Cases & Error Handling

- Historical documents may still mention Dashboard-era values. Current reviewers should check this spec's current contract tables before using historical values.
- Kiali can be partially available when external observability runtimes are down; static manifests may still be valid while live connectivity is degraded.
- cert-manager can reconcile the ClusterIssuer before all consuming Ingress certificates are Ready; verify issuer and endpoint-specific TLS separately.
- External service runtime IP changes require synchronized updates to EndpointSlice manifests, NetworkPolicies, operations docs, and static contract tests.

## Failure Modes & Fallback / Human Escalation

| Failure | Fallback | Human Escalation |
| --- | --- | --- |
| `mkcert-ca-issuer` NotReady | Inspect cert-manager namespace, issuer status, and Secret presence. | Secret reinjection is human-approved bootstrap only; do not commit key material. |
| Headlamp ingress unavailable | Verify `platform-headlamp` and `platform-headlamp-config` ArgoCD Applications plus `headlamp` Ingress/TLS. | External Traefik route updates happen outside this repo. |
| Istiod unavailable | Review Helm chart state and resource requests through GitOps manifests. | Runtime patching must be replaced by a GitOps PR. |
| Kiali cannot reach observability | Check service DNS, `172.18.x` EndpointSlices, and `allow-kiali-egress-to-observability`. | External observability endpoint changes require docs and static test updates. |
| Static contract mismatch | Treat the mismatch as a repo contract drift. | Patch manifests, docs, and tests together in one reviewable change. |

## Verification Commands

Static validation:

```bash
bash scripts/validate-gitops-structure.sh
bash scripts/validate-k8s-manifests.sh .
bash infrastructure/tests/verify-contracts-static.sh
```

Operator live evidence, when a cluster is intentionally available:

```bash
kubectl -n cert-manager get clusterissuer mkcert-ca-issuer -o jsonpath='{.status.conditions[0].type}'
kubectl -n headlamp get pods,ingress,svc
kubectl -n istio-system get deployment istiod
kubectl -n istio-system get deployment kiali
curl -ksS -o /dev/null -w '%{http_code}' https://headlamp.127.0.0.1.nip.io/
curl -ksS -o /dev/null -w '%{http_code}' https://kiali.127.0.0.1.nip.io/kiali
```

Agents may document these live checks as expected operator evidence, but must not mutate the cluster.

## Success Criteria & Verification Plan

- **VAL-SPC-003-001**: `bash scripts/validate-gitops-structure.sh` PASS.
- **VAL-SPC-003-002**: `bash scripts/validate-k8s-manifests.sh .` PASS.
- **VAL-SPC-003-003**: `bash infrastructure/tests/verify-contracts-static.sh` PASS.
- **VAL-SPC-003-004**: cert-manager `ClusterIssuer/mkcert-ca-issuer` reports Ready when live cluster validation is requested.
- **VAL-SPC-003-005**: Headlamp HTTPS route returns 200 when live route validation is requested.
- **VAL-SPC-003-006**: Istiod and Kiali deployments are Available when live cluster validation is requested.
- **VAL-SPC-003-007**: Kiali egress policy preserves current `172.18.0.10`, `172.18.0.14`, and `172.18.0.12` observability endpoints.

## Related Documents

- **Plan**: [`../../04.execution/plans/2026-03-29-platform-expansion.md`](../../04.execution/plans/2026-03-29-platform-expansion.md)
- **Tasks**: [`../../04.execution/tasks/2026-03-29-platform-expansion.md`](../../04.execution/tasks/2026-03-29-platform-expansion.md)
- **Guide**: [`../../05.operations/guides/0003-platform-expansion-bootstrap-guide.md`](../../05.operations/guides/0003-platform-expansion-bootstrap-guide.md)
- **Policy**: [`../../05.operations/policies/0003-service-mesh-cert-manager-policy.md`](../../05.operations/policies/0003-service-mesh-cert-manager-policy.md)
- **Current Operations Policy**: [`../../05.operations/policies/0004-rollouts-notifications-headlamp-policy.md`](../../05.operations/policies/0004-rollouts-notifications-headlamp-policy.md)
- **Runbook**: [`../../05.operations/runbooks/0003-platform-expansion-bootstrap-runbook.md`](../../05.operations/runbooks/0003-platform-expansion-bootstrap-runbook.md)
- **Current Operations Runbook**: [`../../05.operations/runbooks/0004-rollouts-notifications-headlamp-runbook.md`](../../05.operations/runbooks/0004-rollouts-notifications-headlamp-runbook.md)
