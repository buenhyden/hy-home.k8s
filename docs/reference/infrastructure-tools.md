# Infrastructure Tools & Services

This document lists the infrastructure components, their versions, and configurations used in the `hy-home.k8s` project.

## Controllers

| Component | Version | Helm Repo | Description | Path |
|-----------|---------|-----------|-------------|------|
| **Istio** | `1.24.0` | `https://istio-release.storage.googleapis.com/charts` | Service Mesh (Base, Istiod, Gateway) | `infrastructure/controllers/istio-*` |
| **MetalLB** | - | - | Bare metal load balancer implementation for Kubernetes | `infrastructure/controllers/metallb` |

## Observability

| Component | Version | Helm Repo | Description | Path |
|-----------|---------|-----------|-------------|------|
| **Kube-Prometheus-Stack** | `66.7.1` | `https://prometheus-community.github.io/helm-charts` | Prometheus, Alertmanager, Grafana | `infrastructure/observability/kube-prometheus-stack` |
| **Loki** | `6.18.0` | `https://grafana.github.io/helm-charts` | Log aggregation system | `infrastructure/observability/loki` |
| **Tempo** | `1.12.0` | `https://grafana.github.io/helm-charts` | Distributed tracing backend | `infrastructure/observability/tempo` |
| **Alloy** | `0.9.0` | `https://grafana.github.io/helm-charts` | OpenTelemetry Collector & Prometheus Agent | `infrastructure/observability/alloy` |

## Security

| Component | Version | Helm Repo | Description | Path |
|-----------|---------|-----------|-------------|------|
| **Kyverno** | `3.2.0` | `https://kyverno.github.io/kyverno/` | Kubernetes Native Policy Management | `infrastructure/security/kyverno` |
| **Cert-Manager** | `v1.16.0` | `https://charts.jetstack.io` | Cloud native certificate management | `infrastructure/security/cert-manager` |
| **Sealed Secrets** | - | - | Encrypted Secrets for Kubernetes | `infrastructure/security/sealed-secrets` |

## Workflow

| Component | Version | Helm Repo | Description | Path |
|-----------|---------|-----------|-------------|------|
| **Apache Airflow** | `1.15.0` | `https://airflow.apache.org` | Workflow orchestration platform | `infrastructure/workflow/airflow` |

## External Services

| Component | Connection Method | Path |
|-----------|------------------|------|
| **PostgreSQL** | Headless Service -> Docker IP (`172.19.0.56`) | `infrastructure/external-services/postgres` |
| **Redis Cluster** | Headless Service -> Docker IPs (`172.19.0.60-65`) | `infrastructure/external-services/redis` |
| **Kafka** | ServiceEntry | `infrastructure/external-services/kafka` |
| **OpenSearch** | ServiceEntry | `infrastructure/external-services/opensearch` |

## Clusters

| Cluster Name | Path | Description |
|--------------|------|-------------|
| **docker-desktop** | `clusters/docker-desktop` | Local development cluster using Kind |

---
**Note**: Versions are based on `kustomization.yaml` files in the respective directories.
