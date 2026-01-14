# Claude Developer Guide

Guidelines for interacting with Claude in the context of `hy-home.k8s`.

## Project Context

- **Name**: hy-home.k8s
- **Platform**: GitOps-based Kubernetes Infrastructure
- **Tools**: Kind, ArgoCD, Istio, Prometheus, Grafana, PostgreSQL, Redis

## Instructions for Claude

### GitOps & Manifests

- **GitOps First**: All changes must be suitable for ArgoCD synchronization.
- **Manifest Standards**:
  - Use standard K8s API versions.
  - Include `metadata.labels` for correct identifying and selecting.
  - **Secrets**: NEVER output base64 encoded secrets in chat unless asking for a sealed secret generation. Use `SealedSecret` resources.

### Architectural Rules

- **Infrastructure (`infrastructure/`)**: Base layer (storage, networking, observability).
- **Apps (`apps/`)**: Workloads on top of infrastructure.
- **Local Dev (`bootstrap/`)**: Solutions must work in Kind.

### Security

- **Policies**: Respect Kyverno policies (no root, resource limits required).
- **Networking**: Use Istio VirtualServices/Gateways for ingress.
