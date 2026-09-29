# External service consumer contracts

Owner: platform. Scope: repository-static review, observed 2026-09-29.
Invalidate this reference when the cited consumer changes its endpoint,
authentication reference, protocol or retry policy. The owning manifest wins.

| Protocol | Current consumer / owner | Review contract |
| --- | --- | --- |
| OpenBao HTTP(S) | `gitops/platform/eso/vault-secret-store.yaml` | Preserve provider URL, auth method and reference names. ESO owns reconciliation and retry; no token value belongs in an audit. |
| Prometheus HTTP(S) | `gitops/workloads/adminer/analysis-template.yaml`, `gitops/platform/kiali/kiali-prometheus-auth-externalsecret.yaml` | Verify query endpoint and authentication reference at the caller; analysis/consumer configuration owns retry and timeout. |
| Grafana HTTP(S) | `gitops/apps/root/platform-kiali-app.yaml`, `gitops/platform/kiali/kiali-grafana-auth-externalsecret.yaml` | Keep the consumer URL and auth reference aligned; do not infer credentials or availability from ExternalSecret syntax. |
| PostgreSQL TCP | `gitops/platform/external-services/postgres-external.yaml`, `gitops/workloads/adminer/rollout.yaml` | Distinguish read and write endpoints and ports; the client owns connection timeout and retries. |
| Valkey TCP | `gitops/platform/external-services/valkey-external.yaml`, `gitops/platform/argocd/argocd-external-valkey-secret.yaml` | The Service exposes 6379 and routes to backend 26379. Inspect the actual Argo CD consumer and auth reference before altering either. |
| Alloy OTLP | `gitops/platform/external-services/alloy-external.yaml` | gRPC 4317 and HTTP 4318 are distinct named ports. Aggregate all matching slices; exporter configuration owns TLS and retry. |

The dedicated checker compares selectorless Services against all matching
EndpointSlices using namespace, service-name label, port name, protocol and
numeric targetPort. It permits repeated identical endpoints and multiple slices.
Selector-managed Services use Kubernetes discovery and are excluded from this
specific static join. Addresses must match the declared family and must not be
loopback, unspecified, multicast or link-local. This does not prove routing.

Sources reviewed 2026-09-29: [Kubernetes Service](https://kubernetes.io/docs/concepts/services-networking/service/)
and [EndpointSlices](https://kubernetes.io/docs/concepts/services-networking/endpoint-slices/).
The procedure and checker are original repository work; sources are referenced,
not copied or distributed as a third-party skill. Service definitions and
consumer manifests above remain the current contract owners.
