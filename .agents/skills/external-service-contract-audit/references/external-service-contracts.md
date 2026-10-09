# External service consumer contracts

Owner: platform. Scope: repository-static review, observed 2026-10-09.
Invalidate this reference when the cited consumer changes its endpoint,
authentication reference, protocol or retry policy, or the external Docker
publication changes. The owning manifest or Compose file wins.

| Protocol | Current consumer / owner | Review contract |
| --- | --- | --- |
| OpenBao HTTP(S) | `gitops/platform/eso/vault-secret-store.yaml` | Preserve provider URL, auth method and reference names. ESO owns reconciliation and retry; no token value belongs in an audit. |
| Prometheus HTTP(S) | `gitops/workloads/adminer/analysis-template.yaml`, `gitops/platform/kiali/kiali-prometheus-auth-externalsecret.yaml` | Verify query endpoint and authentication reference at the caller; analysis/consumer configuration owns retry and timeout. |
| Grafana HTTP(S) | `gitops/apps/root/platform-kiali-app.yaml`, `gitops/platform/kiali/kiali-grafana-auth-externalsecret.yaml` | Keep the consumer URL and auth reference aligned; do not infer credentials or availability from ExternalSecret syntax. |
| PostgreSQL TCP | `hy-home.docker/infra/04-data/mng-db/docker-compose.yml` (`mng-pg`) and `hy-home.docker/infra/04-data/dev-db/docker-compose.yml` (`dev-pg`) | Optional management and development Docker publications are respectively `127.0.0.1:25432→5432` and `127.0.0.1:25433→5432`. Neither loopback address supplies a Kubernetes-reachable endpoint. Adminer has no PostgreSQL default server; a future Kubernetes consumer needs an explicitly reviewed reachable binding, Service/EndpointSlice, authentication and network policy. |
| Valkey TCP | `gitops/platform/external-services/valkey-external.yaml`, `gitops/platform/argocd/argocd-external-valkey-secret.yaml`; Docker owner: `hy-home.docker/infra/04-data/mng-db/docker-compose.yml` | Required management `mng-valkey` publishes `192.168.0.13:26379→6379`. The Kubernetes Service exposes 6379 and routes to backend 26379 for Argo CD; inspect its auth reference before altering either. Development `dev-valkey` stays on Docker `dev_data_net:6379` without a host publication. |
| Alloy OTLP | `gitops/platform/external-services/alloy-external.yaml` | gRPC 4317 and HTTP 4318 are distinct named ports. Aggregate all matching slices; exporter configuration owns TLS and retry. |

The dedicated checker compares selectorless Services against all matching
EndpointSlices using namespace, service-name label, port name, protocol and
numeric targetPort. It permits repeated identical endpoints and multiple slices.
Selector-managed Services use Kubernetes discovery and are excluded from this
specific static join. Addresses must match the declared family and must not be
loopback, unspecified, multicast or link-local. This does not prove routing.
The separate `postgres-ha`/`pg-router` write/read ports 15432/15433 and the
Valkey cluster lab are not current Kubernetes data-service contracts.

Docker port declarations were checked against clean `hy-home.docker` revision
`77a80bc1478c3dfb46cfe8b8de97aa971817c494`, in the management and
development Compose files named above. Recheck that source when its revision
or runtime publication changes; this static reference does not establish
database login, authentication or live reachability.

Sources reviewed 2026-09-29: [Kubernetes Service](https://kubernetes.io/docs/concepts/services-networking/service/)
and [EndpointSlices](https://kubernetes.io/docs/concepts/services-networking/endpoint-slices/).
The procedure and checker are original repository work; sources are referenced,
not copied or distributed as a third-party skill. Service definitions and
consumer manifests above remain the current contract owners.
