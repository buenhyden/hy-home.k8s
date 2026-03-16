---
layer: "meta"
---
# Operations Index

This document is the central index for operational readiness. It provides policy-level guidance and points to executable runbooks managed by the **DevOps Agent**.

> [!IMPORTANT]
> All operational procedures, deployment scripts, and incident guides are located in the flattened plural directories: `docs/runbooks/` and `docs/operations/`.

## 1. Runbook Catalog

All procedures MUST use `templates/runbook-template.md`.

| Runbook           | Status | Location                                 | Purpose                              |
|-------------------|--------|------------------------------------------|--------------------------------------|
| Deployment        | Active | `docs/runbooks/deployment-runbook.md`    | Staging/Production release steps     |
| Incident Response | Active | `docs/runbooks/incident-response-runbook.md` | SEV-1/SEV-2 incident mitigation      |
| Monitoring        | Active | `docs/runbooks/monitoring-runbook.md`    | Threshold checks and alerting config |
| Local k3d (WSL2)  | Active | `docs/runbooks/local-k3d-wsl2.md`        | Local cluster setup and troubleshooting |
| GitOps Bootstrap  | Active | `docs/runbooks/local-gitops-argocd.md`   | Deterministic ArgoCD repo key setup  |

## 2. Operational Strategies

Strategies are managed as durable planning assets:

- **[Deployment Strategy](docs/operations/deployment-strategy.md)**: Environment hierarchy and automation policies.
- **[Observability Standard](docs/operations/observability-standard.md)**: OTel, logging, and error budget standards.

## 3. Incident Management

Critical failure tracking is managed in `docs/operations/`:

- **Active Incidents**: `docs/operations/incidents/`
- **Postmortems**: `docs/operations/postmortems/`

## 4. Operational Rules

### Pre-Deployment Gates

1. **Spec Existence**: Approved spec in `docs/specs/` is required.
2. **AI Approval**: AI Reviewer must approve the PR logic.
3. **Traceability**: PR must link to a specific Implementation Plan.
4. **Rollback Ready**: Rollback steps MUST be documented in the deployment runbook.

### Incident Priorities

- **SEV-1 (Critical)**: Production offline. Immediate action via `runbooks/incident-response-runbook.md`.
- **SEV-2 (Major)**: Critical flow degraded. Log in `docs/operations/incidents/`.
- **SEV-3 (Minor)**: Non-critical bugs.

## 5. Security & Compliance

- CI/CD enforces SAST and secret scanning via `.github/workflows/`.
- All operational docs MUST include `layer: "meta" | "infra" | "gitops" | "ops"`.
