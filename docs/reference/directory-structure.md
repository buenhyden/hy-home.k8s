# Directory Structure

This document provides a comprehensive map of the `hy-home.k8s` repository.

## Root Directory

| Path | Description |
|------|-------------|
| `apps/` | User-facing applications and templates. |
| `bootstrap/` | Scripts for initializing the local Kind cluster. |
| `clusters/` | Environment-specific Kustomize overlays (e.g., `docker-desktop`). |
| `docs/` | Project documentation. |
| `infrastructure/` | Core platform services (Helm charts, controllers). |
| `.agent/` | AI agent configuration and workflows. |

## Apps (`apps/`)

| Path | Description |
|------|-------------|
| `_templates/` | Helm chart starter templates for new services. |
| `_examples/` | Reference implementations of backend/frontend services. |
| `backend/` | Backend microservices manifests. |
| `frontend/` | Frontend application manifests. |

## Infrastructure (`infrastructure/`)

| Path | Description |
|------|-------------|
| `controllers/` | Ingress controllers, Gateways, and Operators (Istio, MetalLB). |
| `observability/` | Monitoring and Logging stack (Prometheus, Loki, Tempo, Alloy). |
| `security/` | Security tools (Kyverno, Cert-Manager, Sealed Secrets). |
| `workflow/` | Data orchestration tools (Airflow). |
| `external-services/` | Connectors for services running in Docker (Postgres, Redis). |

## Documentation (`docs/`)

| Path | Description |
|------|-------------|
| `architecture/` | High-level system design and decision records. |
| `guides/` | How-to guides for common tasks (setup, troubleshooting). |
| `reference/` | Detailed technical references (this file, tools list). |
| `templates/` | Templates for writing new documentation. |
