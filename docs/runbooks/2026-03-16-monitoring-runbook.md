---
title: 'Runbook: Monitoring'
status: 'Active'
date: '2026-03-16'
owner: 'buenhyden'
tags:
  - runbook
  - operation
layer: "ops"
---

# Runbook: Monitoring

- **Status**: Active
- **Owner**: buenhyden
- **Last Reviewed**: 2026-03-16
- **layer:** ops

**Overview (KR):** 서비스 상태를 지속적으로 모니터링하고 알람 발생 시 비정상 징후를 추적하기 위한 운영 절차입니다.

## 1. Document Purpose

Procedure for monitoring service health and responding to alert signals.

## 2. Prerequisites

- Access Requirements: Monitoring dashboards and alerting tools
- Tools: Metrics dashboard, logs viewer, tracing (if enabled)

## 3. Dashboards & Alerts (Required Links)

- [ ] **Primary Dashboard**: `[Link to grafana/datadog]`
- [ ] **SLOs / SLIs**: `[Link to SLO definitions]`
- [ ] **Alert Routing**: `[Where does this alert page? PagerDuty/Slack]`

## 4. Execution Steps

1. Check primary dashboard (latency, traffic, errors, saturation).

   ```bash
   # Open service dashboard and inspect last 30-60 minutes.
   ```

2. Correlate alerts with logs and traces.

   ```bash
   # Filter by correlation or trace id where available.
   ```

3. Classify incident severity and engage response flow.

   ```bash
   # Use SEV criteria from incident policy.
   ```

## 5. Validation

- Alert cause identified and documented.
- Mitigation action validated by metric recovery.

## 6. Rollback / Reversal Procedure

- If recovery fails, follow deployment rollback runbook.

## 7. Escalation Contacts

- Primary Contact: On-call rotation
- Secondary Contact: Platform/SRE team

## Canonical References

- [docs/plans/2026-03-16-infra-plan.md](../plans/2026-03-16-infra-plan.md)
- [docs/specs/2026-03-16-infra-spec.md](../specs/2026-03-16-infra-spec.md)
