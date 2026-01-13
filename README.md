# hy-home.k8s - GitOps Infrastructure Platform

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Kubernetes](https://img.shields.io/badge/kubernetes-%23326ce5.svg?style=flat&logo=kubernetes&logoColor=white)
![ArgoCD](https://img.shields.io/badge/argocd-%23eb5b3e.svg?style=flat&logo=argo&logoColor=white)

**GitOps-based Kubernetes infrastructure** using ArgoCD for declarative deployment of applications and platform services on Kind (Kubernetes in Docker).

## 🚀 Quick Start (15 Minutes)

```bash
# 1. Clone repository
git clone https://github.com/buenhyden/hy-home.k8s.git && cd hy-home.k8s

# 2. Create cluster
cd bootstrap && chmod +x *.sh && ./cluster-setup.sh

# 3. Install ArgoCD
./argocd-install.sh

# 4. Deploy everything
./root-apps.sh
```

**Done!** Access ArgoCD at `https://localhost:8080` (port-forward required).

📖 **Full Guide**: [docs/guides/getting-started.md](docs/guides/getting-started.md)

## 📋 Contents

- [Features](#features)
- [Architecture](#architecture)
- [Directory Structure](#directory-structure)
- [Key Components](#key-components)
- [🤖 AI & Automation](#-ai--automation)
- [Prerequisites](#prerequisites)
- [Documentation](#documentation)

## Features

### GitOps Workflow

- **Declarative**: All configuration in Git, deployed via ArgoCD
- **Automated Sync**: Changes auto-deploy within 3 minutes
- **Self-Healing**: Cluster state auto-corrects to match Git
- **Auditable**: Full deployment history in Git

### Progressive Delivery

- **Canary Deployments**: Argo Rollouts with traffic shifting (20% → 50% → 100%)
- **Istio Integration**: Precise traffic control via VirtualService
- **Zero Downtime**: Rolling updates with PodDisruptionBudgets

### Platform Services

- **Service Mesh**: Istio v1.24.0 (mTLS, traffic management)
- **Observability**: Prometheus, Loki, Tempo, Grafana, Alloy
- **Security**: Kyverno policies, Cert-Manager, Sealed Secrets
- **Workflow**: Apache Airflow for orchestration
- **Load Balancing**: MetalLB for local development

### Hybrid Networking

- **Kind Cluster**: 172.18.0.0/16
- **External Services**: PostgreSQL (Patroni), Redis Cluster via Headless Services
- **Docker Network**: 172.19.0.0/16 for external dependencies

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  Git Repository (Source of Truth)                          │
│  github.com/buenhyden/hy-home.k8s                          │
└──────────────────┬──────────────────────────────────────────┘
                   │ GitOps Sync
         ┌─────────▼──────────┐
         │  ArgoCD Controller │
         └─┬────────────────┬─┘
           │                │
     ┌─────▼──────┐  ┌──────▼───────┐
     │ Apps Root  │  │ Infra Root   │
     │ Application│  │ Application  │
     └─┬──────────┘  └──┬───────────┘
       │                │
       │                ├─► Controllers (Istio, MetalLB)
       │                ├─► Observability (Prometheus, Loki, Tempo)
       │                ├─► Security (Kyverno, Cert-Manager)
       │                ├─► External Services (DB connectors)
       │                └─► Workflow (Airflow)
       │
       └─► Your Applications (Backend, Frontend)
```

**Detailed Architecture**: [docs/architecture/overview.md](docs/architecture/overview.md)

## Directory Structure

```
hy-home.k8s/
├── apps/                   # Application workloads
│   ├── _templates/        # Templates for new apps (✅ Use these)
│   │   ├── backend/
│   │   └── frontend/
│   └── _examples/         # Legacy reference examples
├── bootstrap/             # Cluster setup scripts (⭐ Start here)
│   ├── cluster-setup.sh
│   ├── argocd-install.sh
│   └── root-apps.sh
├── clusters/              # Cluster configurations
│   └── docker-desktop/
│       ├── apps.yaml              # Apps root application
│       ├── infrastructure.yaml    # Infrastructure root app
│       └── infrastructure/        # Infra app definitions
├── infrastructure/        # Platform infrastructure
│   ├── controllers/       # Istio, MetalLB
│   ├── observability/     # Prometheus, Loki, Tempo, Grafana
│   ├── security/          # Kyverno, Cert-Manager, Sealed Secrets
│   ├── external-services/ # DB connectors (PostgreSQL, Redis)
│   └── workflow/          # Airflow
└── docs/                  # Documentation
    ├── guides/           # Getting started, troubleshooting
    ├── reference/        # Technical references
    └── architecture/     # System design
```

**Complete Reference**: [docs/reference/directory-structure.md](docs/reference/directory-structure.md)

## Key Components

### GitOps & Progressive Delivery

- **ArgoCD** - GitOps continuous deployment
- **Argo Rollouts** - Canary deployments, blue/green
- **Argo Image Updater** - Automatic image updates

### Service Mesh

- **Istio v1.24.0** - Traffic management, mTLS, observability
- **MetalLB** - LoadBalancer for bare metal/local

### Observability Stack

- **Prometheus Stack v66.7.1** - Metrics, alerting (Grafana, Alertmanager)
- **Loki v6.18.0** - Log aggregation
- **Tempo v1.12.0** - Distributed tracing
- **Alloy v0.9.0** - Unified telemetry collector
- **Grafana** - Visualization dashboards

### Security

- **Kyverno v3.2.0** - Policy engine (block `:latest`, enforce non-root)
- **Cert-Manager v1.16.0** - Certificate management
- **Sealed Secrets** - Encrypted secrets for Git

### Workflow

- **Apache Airflow v1.15.0** - Workflow orchestration

### External Services (Docker Network)

- **PostgreSQL** - Patroni HA cluster (172.19.0.56)
- **Redis Cluster** - 6-node cluster (172.19.0.60-65)
- **Kafka** - Message streaming
- **OpenSearch** - Search and analytics

**Full List**: [docs/reference/infrastructure-tools.md](docs/reference/infrastructure-tools.md)

## 🤖 AI & Automation

This project is built with an "AI-First" mindset, leveraging multiple agents for development, documentation, and maintenance.

- **Agents**: See [AGENTS.md](AGENTS.md) for available agents and their roles.
- **Workflows**: Standard operational procedures are defined in `.agent/workflows/` and can be executed by agents.
- **Context**: Agents use `task.md` and `implementation_plan.md` to maintain context across sessions.

## Prerequisites

- **Docker Desktop** (Windows/Mac) or Docker Engine (Linux)
- **kubectl** - Kubernetes CLI
- **Kind** - Kubernetes in Docker
- **Git** - Version control

**Install Guide**: [docs/guides/getting-started.md#prerequisites](docs/guides/getting-started.md#prerequisites)

## Documentation

### 📘 Essential Guides

| Guide | Description |
|-------|-------------|
| [Getting Started](docs/guides/getting-started.md)     | Complete 15-minute setup walkthrough |
| [Adding Applications](docs/guides/adding-applications.md) | Deploy your first app with GitOps    |
| [Troubleshooting](docs/guides/troubleshooting.md)     | Common issues and solutions          |
| [Credentials](docs/guides/credentials.md)         | Managing secrets and credentials    |

### 📚 Reference Documentation

| Doc | Description |
|-----|-------------|
| [Architecture Overview](docs/architecture/overview.md)    | System design, components, workflows    |
| [Directory Structure](docs/reference/directory-structure.md) | Complete folder layout explained     |
| [Infrastructure Tools](docs/reference/infrastructure-tools.md) | Component versions and configurations |

### 📖 Full Documentation

**Index**: [docs/README.md](docs/README.md)

## Common Tasks

### Deploy a New Application

```bash
# 1. Copy template
cp -r apps/_templates/backend apps/my-api

# 2. Edit manifests (replace APP_NAME, image, etc.)
vim apps/my-api/base/rollout.yaml

# 3. Commit and push
git add apps/my-api
git commit -m "feat: add my-api"
git push

# ArgoCD will auto-sync within 3 minutes
```

**Detailed Guide**: [docs/guides/adding-applications.md](docs/guides/adding-applications.md)

### Access Services

```bash
# ArgoCD UI
kubectl port-forward svc/argocd-server -n argocd 8080:443
# https://localhost:8080

# Grafana
kubectl port-forward -n observability svc/kube-prometheus-stack-grafana 3000:80
# http://localhost:3000

# Prometheus
kubectl port-forward -n observability svc/kube-prometheus-stack-prometheus 9090:9090
# http://localhost:9090
```

### Monitor Deployments

```bash
# All applications
kubectl get applications -n argocd

# Specific rollout
kubectl argo rollouts get rollout <app-name> -w

# Pod status
kubectl get pods -A
```

## Technology Stack

- **Container Orchestration**: Kubernetes via Kind
- **GitOps**: ArgoCD, Argo Rollouts, Argo Image Updater
- **Service Mesh**: Istio v1.24.0
- **Observability**: Prometheus Stack v66.7.1, Loki v6.18.0, Tempo v1.12.0, Grafana, Alloy v0.9.0
- **Security**: Kyverno v3.2.0, Cert-Manager v1.16.0, Sealed Secrets
- **Networking**: MetalLB
- **Workflow**: Apache Airflow v1.15.0
- **External Services**: PostgreSQL (Patroni), Redis Cluster, Kafka, OpenSearch

## Project Structure

This repository follows GitOps best practices:

- **apps/** - Application definitions (use templates for new apps)
- **bootstrap/** - One-time cluster setup scripts
- **clusters/** - Cluster-specific configurations and ArgoCD apps
- **infrastructure/** - Platform components (Istio, Prometheus, etc.)
- **docs/** - Comprehensive documentation

## Support

- **Issues**: [GitHub Issues](https://github.com/buenhyden/hy-home.k8s/issues)
- **Documentation**: [docs/](docs/)
- **Getting Help**: See [Troubleshooting Guide](docs/guides/troubleshooting.md)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Next Steps**: Start with [docs/guides/getting-started.md](docs/guides/getting-started.md) for complete setup instructions.
