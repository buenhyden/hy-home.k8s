---
layer: "ops"
---
# Operations Manual (OPERATION.md)

_Target Location: `OPERATION.md` (Project Root)_
_Description: This document defines the project's operational baseline, including environments, deployment strategies, quality/security gates, and observability, as per the `0301-operations-blueprint-standard.md` rule._

## Overview (KR)
이 문서는 프로젝트의 운영 표준을 정의합니다. 환경 계층, 배포 전략, QA 및 보안 기준, 그리고 서비스 가용성을 보장하기 위한 Observability 표준을 포함합니다.

---

## 1. Environment Hierarchy & Promotion Rules

| Environment | Purpose | Promotion Gate / Automation |
| :--- | :--- | :--- |
| **Development** | Feature testing | Auto-deploy on PR/Merge to `develop` |
| **Staging** | Pre-prod validation | Tag-based deploy, Manual Approval (TL/QA) |
| **Production** | Live traffic | Scheduled Release, CI/CD Gate, Canary Pass |

### Promotion Policy
- **Strict Immutability**: Production artifacts MUST be the exact same images/builds tested in Staging.
- **Roll-forward Only**: In case of failure, prioritize fixing forward unless immediate rollback is required.

## 2. Deployment & Release Strategy

### Deployment Patterns
- **Primary Type**: [e.g., Rolling Update / Blue-Green / Canary]
- **Canary Strategy**: [e.g., 5% traffic for 10 min -> Analyze Error Rate -> 100%]
- **Automated Health Checks**:
  - **Liveness/Readiness**: Defined in K8s manifests.
  - **Startup Probe**: Required for heavy services.

### Rollback Strategy
- **Trigger**: [e.g., Error rate > 1% or p99 Latency > 2s for 3m during deploy]
- **Procedure**: Automated via [CI Tool] or manual `helm rollback`.

## 3. QA & Security Baseline (Merged)

### Quality Gates
- **Unit/Integration**: Mandatory > 80% coverage.
- **E2E**: Critical paths (Login, Checkout) must pass in Staging.
- **Static Analysis**: Linter & Typecheck failure blocks PR.

### Security Baseline
- **Secret Scan**: Pre-commit & CI scan for leaked credentials.
- **SAST/DAST**: Weekly vulnerability scanning.
- **Dependency Audit**: `npm audit` or `trivy` scan on every build.
- **AuthN/AuthZ**: All endpoints must be secured by [Auth Provider].

## 4. Observability & Reliability (Senior)

### SLIs & SLOs
| Metric (SLI) | Target (SLO) | Error Budget Policy |
| :--- | :--- | :--- |
| **Availability** | 99.9% (3 nines) | Block new features if budget exhausted |
| **Latency (p95)** | < 300ms | Optimize DB/Cache if breached |
| **Error Rate** | < 0.1% | Investigate SEV-2 immediately |

### Monitoring Stack
- **Dashboard**: [Link to Grafana/Datadog]
- **Logs**: JSON structured logging with `trace_id`.
- **Tracing**: Distributed tracing (OpenTelemetry) for cross-service calls.

## 5. Continuity & Scalability

- **RTO / RPO**: Target RTO < 1h, RPO < 5m (Database).
- **Backup Strategy**: [e.g., WAL-G for Postgres, Hourly S3 Snapshots]
- **Auto-scaling**: HPA based on [CPU/Memory/Reqs] threshold (> 70%).

## 6. Incident & Runbooks
- **Standard Runbooks**: Located in `docs/runbooks/`
- **Incident Logs**: Located in `docs/incidents/`
- **Postmortems**: Mandatory for SEV-1/2 incidents.
