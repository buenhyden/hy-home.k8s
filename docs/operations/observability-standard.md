---
layer: "ops"
---
# Observability Baseline

## 1. Metrics

Essential RED metrics MUST be collected utilizing OTel collectors, adhering to `.agent/rules/2610-observability-strategy.md`.

## 2. Logging

All logs MUST use structured JSON format with correlation IDs per `.agent/rules/2620-logging-std.md`.

## 3. Tracing

Critical inter-service pipelines MUST propagate HTTP `trace_id` headers per `.agent/rules/2610-observability-strategy.md`.

## 4. Alerts

Alerts trigger based on SLO Error Budget burns affecting users, adhering to `.agent/rules/2630-alerting-std.md`.

## 5. Continuity & Disaster Recovery

- **Data Backups**: All stateful data stores MUST have automated, encrypted daily backups at a minimum, verified monthly, adhering to `.agent/rules/0342-backup-restore.md`.
- **Recovery Time Objective (RTO)**: Target < 4 hours for Tier-1 services.
- **Recovery Point Objective (RPO)**: Target < 1 hour of potential data loss via WAL (Write-Ahead Logging) or continuous replication.
