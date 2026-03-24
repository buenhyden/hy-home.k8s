---
layer: "ops"
---
# Runbook (RUNBOOK.md)

_Target Location: `docs/runbooks/<topic>.md`_
_Description: A step-by-step operational guide for resolving specific issues or managing recurring tasks. It prioritizes actionable steps over background theory._

## Overview (KR)
이 문서는 특정 장애 상황의 해결 방법이나 반복적인 운영 작업의 절차를 정의합니다. 증상별 진단 방법, 단계별 조치 사항, 그리고 에스컬레이션 경로를 포함합니다.

---

## 1. Runbook Metadata

- **Title**: [Issue or Task Name]
- **Status**: [Active | Deprecated]
- **On-Call Role**: [Primary / Secondary Contact]
- **layer**: [meta | infra | gitops | app | ops]

## 2. Severity & Impact Matrix (Senior)

| Severity | Description | SLA (Response) |
| :--- | :--- | :--- |
| **SEV-1** | Critical outage (e.g., Main API down) | 15 mins |
| **SEV-2** | Significant disruption (e.g., 50% increase in latency) | 1 hour |
| **SEV-3** | Minor issue / Non-blocking bug | 24 hours |

## 3. Diagnosis & Symptoms Check

| Symptom | Probable Cause | Diagnostic Command |
| :--- | :--- | :--- |
| **504 Gateway Timeout** | Backend pod crash / overload | `kubectl get pods -n <ns>` |
| **High Latency** | DB Lock / Resource exhaustion | `kubectl top pod <pod>` |
| **Auth Failures** | OIDC Provider / Secret expiry | `kubectl logs <auth-pod>` |

## 4. Remediation Procedure (Step-by-Step)

### Step 1: Initial Triage
- [ ] Check Grafana Dashboard: [Link]
- [ ] List recent deployments: `git log --oneline -n 5`

### Step 2: Resolution Action
- **Action A**: [e.g., Restart pods]
- **Action B**: [e.g., Scale up replica count]

## 5. Automation & Tooling
[List scripts or CLI tools that help automate this runbook.]
- **Cleanup Script**: `scripts/cleanup-tmp.sh`
- **Verification Tool**: `npm run test:prod`

## 6. Escalation Path
1. **Developer**: [Name/Slack Name]
2. **Platform/SRE**: `#ops-critical`
3. **Management**: [Name]

## 7. Evidence & Verification
- [ ] Log entry created in `docs/incidents/`?
- [ ] Post-remediation health check passed?
