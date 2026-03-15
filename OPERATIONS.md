---
layer: "meta"
---
# Operations Index

This document is the central index for operational readiness in repositories created from this template. It provides policy-level guidance and points to executable runbooks managed by the **DevOps Agent**.

> **IMPORTANT:** Detailed operational procedures, deployment scripts, and incident guides are located in the `docs/runbooks/` and `docs/operations/` directories.

## 1. Runbook Catalog

All operational procedures must use `templates/runbook-template.md`. Below is the index of standard runbooks included in the `docs/runbooks/` directory.

| Runbook           | Status | Location                                 | Purpose                              |
|-------------------|--------|------------------------------------------|--------------------------------------|
| Deployment        | Active | `docs/runbooks/deployment-runbook.md`    | Staging/Production release steps     |
| Incident Response | Active | `docs/runbooks/incident-response-runbook.md` | SEV-1/SEV-2 incident mitigation      |
| Monitoring        | Active | `docs/runbooks/monitoring-runbook.md`    | Threshold checks and alerting config |
| Local k3d (WSL2)  | Active | `docs/runbooks/local-k3d-wsl2.md`        | Local cluster setup and troubleshooting |
| GitOps Bootstrap  | Active | `docs/runbooks/local-gitops-argocd.md`   | Deterministic ArgoCD repo key setup  |
| Sealed Secrets    | Active | `docs/runbooks/sealed-secrets-local.md`  | Secret encryption and sealing workflow|

> **Note:** If a specific operational procedure (e.g. database migration, failover) is missing from this index, the DevOps Agent should proactively create a new runbook based on `templates/runbook-template.md` and link it here.

## 2. Operational Strategies

Detailed strategies for deployment and observability are managed as independent operational assets:

- **[Deployment Strategy](docs/operations/deployment-strategy.md)**: Environment hierarchy and Blue-Green automation policies.
- **[Observability Baseline](docs/operations/observability-standard.md)**: OTel metrics, JSON logging, and error budget alerting standards.

## 3. Continuity & Disaster Recovery

Disaster recovery policies and RTO/RPO targets are defined in the **[Observability Baseline](docs/operations/observability-standard.md)**.

## 5. Operational Rules

### Pre-Deployment Checks

Code must not be deployed unless:

1. Specs in `docs/specs/` exist and are implemented.
2. Reviewer Agent approves the PR.
3. Tests across all tiers pass (unit tests colocated, E2E in global `tests/`) via `.github/workflows/`.
4. A rollback procedure is documented in the corresponding deployment runbook.

### Incident Priorities

- **SEV-1 (Critical)**: Production offline. Immediate action via `runbooks/incident-response-runbook.md` and `.agent/rules/0380-incident-response.md`.
- **SEV-2 (Major)**: Critical flow degraded. Reference `docs/operations/incidents/` for active tracking.
- **SEV-3 (Minor)**: Non-critical bugs.

## 6. Security Baseline

- CI/CD must run `.github/workflows/` container and SAST security scans.
- See `.github/SECURITY.md` for vulnerability policies.

---

> **Note to AI Agents (DevOps Role):** Do not write operation steps directly in this index. For any operational change, modify or create a specific runbook inside `docs/runbooks/` using the approved template.
