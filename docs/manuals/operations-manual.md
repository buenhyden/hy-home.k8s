---
layer: "ops"
---
# Operations Manual (OPERATIONS.md)

_Target Location: `docs/manuals/operations-manual.md`_
_Description: This document defines the project's operational baseline, providing a unified standard for environments, deployment strategies, QA/Security gates, and observability._

## Overview (KR)
이 문서는 프로젝트의 운영 통합 표준을 정의합니다. 환경 계층, 배포 및 릴리스 전략, 그리고 품질(QA) 및 보안(Security) 기준을 하나의 실행 가능한 가이드로 통합하여 관리합니다. 또한 서비스 가용성을 위한 SLO/SLI 표준을 포함합니다.

---

## 1. Environment Hierarchy & Promotion Rules

| Environment | Purpose | Promotion Gate / Automation |
| :--- | :--- | :--- |
| **Development** | Feature testing | Auto-deploy on Merge to `main`/`develop` |
| **Staging** | Pre-prod validation | Tag-based deploy, Manual Approval (TL/QA) |
| **Production** | Live traffic | Scheduled Release, CI/CD Gate, Canary Pass |

### Promotion Policy
- **Strict Immutability**: Production artifacts MUST be the exact same images/builds tested in Staging.
- **Roll-forward Only**: In case of failure, prioritize fixing forward unless immediate rollback is required.

## 2. Deployment & Release Strategy

### Deployment Patterns
- **Primary Type**: Rolling Update (K8s Default)
- **K3d Specifics**:
  - Load balancing via MetalLB and Ingress-Nginx.
  - Stable connectivity via `localhost` port forwarding.
- **Automated Health Checks**:
  - **Liveness/Readiness**: Mandatory for all service deployments.
  - **Startup Probe**: Recommended for heavy services (e.g., Qdrant, MinIO).

### Rollback Strategy
- **Trigger**: Error rate > 1% or p99 Latency > 2s for 3 consecutive minutes during deployment.
- **Procedure**: Automated rollback via ArgoCD sync policy or `helm rollback`.

## 3. QA & Security Baseline (Merged)

### Quality Gates
- **Testing Strategy**: Multi-layer strategy (Unit/Integration/E2E).
- **Unit/Integration**: Mandatory > 80% coverage.
- **E2E**: Critical paths (Login, Data Ingestion) must pass in Staging.
- **Static Analysis**: ESLint/Prettier & Typecheck failure blocks PR.

### Security Baseline
- **Secret Scan**: Pre-commit & CI scan for leaked credentials in `.env` or YAML.
- **Dependency Audit**: `npm audit` or `trivy` scan on every build.
- **AuthN/AuthZ**: All API endpoints secured by [Better Auth/Supabase].
- **Data Protection**: Sensitive environment variables MUST be managed via Sealed Secrets in GitOps.

## 4. Observability & Reliability (Senior)

### SLIs & SLOs
| Metric (SLI) | Target (SLO) | Error Budget Policy |
| :--- | :--- | :--- |
| **Availability** | 99.9% (3 nines) | Block new features if budget exhausted |
| **Latency (p95)** | < 300ms | Optimize DB/Cache if breached |
| **Error Rate** | < 0.1% | Investigate SEV-2 immediately |

### Monitoring Stack
- **Dashboard**: Grafana (Prometheus datasource).
- **Logs**: JSON structured logging with `trace_id`.
- **Tracing**: Distributed tracing (Tempo/Jaeger) for inter-service communication.

## 5. Continuity & Scalability
- **Backup Strategy**: Hourly volume snapshots for persistent volumes (MinIO/Qdrant).
- **Recovery Goals**: Target RTO < 1h, RPO < 5m.
- **Auto-scaling**: HPA based on CPU/Memory threshold (> 70%).

## 6. Incident & Runbooks
- **Standard Runbooks**: Located in [docs/runbooks/](../runbooks/)
- **Incident Logs**: Located in [docs/incidents/](../incidents/)
- **Postmortems**: Mandatory for any SEV-1/2 incident affecting production.

---

## 7. Infrastructure Context (WSL2/k3d)
- **Resource Limits**: `.wslconfig` must limit RAM/CPU to prevent host starvation.
- **Filesystem Performance**: Keep all project data in the Linux filesystem (/home/hy/...) for optimal I/O.
