---
layer: "ops"
---
# Incident Management Manual

_Target Location: `docs/manuals/incident-management-manual.md`_
_Description: Defines the procedures for responding to, managing, and resolving production incidents._

## Overview (KR)
이 문서는 장애 발생 시 대응, 관리 및 해결을 위한 절차를 정의합니다. 장애 등급(Severity) 정의, 대응 역할 및 커뮤니케이션 프로토콜을 포함합니다.

---

## 1. Severity Levels & SLAs

| Severity | Description | Response SLA | Resolution Target |
| :--- | :--- | :--- | :--- |
| **SEV-1 (Critical)** | Core functionality down for all users | < 15 min | < 2 hours |
| **SEV-2 (High)** | Major feature degraded or partial outage | < 30 min | < 8 hours |
| **SEV-3 (Medium)** | Minor bug or localized performance issue | < 4 hours | < 3 days |

## 2. Incident Response Roles

- **Incident Commander (IC)**: Leads the response, coordinates team, and makes final decisions.
- **Communications Lead**: Updates stakeholders and updates status pages.
- **Ops/Dev Lead**: Executes technical fixes, investigates logs/metrics.

## 3. Triage & Diagnosis (Senior)

### Symptoms vs. Causes Matrix

| Symptom | Potential Root Cause | First Action |
| :--- | :--- | :--- |
| **5xx Errors (All)** | Ingress controller down or DB connection failure | Check Ingress-Nginx logs & DB pods |
| **High Latency** | Resource exhaustion (CPU/Mem) or N+1 query | Check HPA/Top pods & APM traces |
| **Data Inconsistency** | Message queue lag or race condition | Check RabbitMQ/Kafka lag metrics |

## 4. Communication Protocol
- **Internal**: Dedicated incident Slack channel.
- **External**: Status updates every 30 minutes for SEV-1.

## 5. Postmortem & Learning
- **Mandatory**: For SEV-1 and SEV-2.
- **Format**: Use the [Postmortem Template](../../templates/postmortem-template.md).
- **Goal**: Blameless analysis to prevent recurrence.
