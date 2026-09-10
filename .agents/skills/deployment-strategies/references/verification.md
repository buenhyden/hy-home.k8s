# Probe, Rollback, and Delivery Measurement Reference

How a chosen strategy proves it is working: the three probe types and their
configuration, the conditions that abort or reverse a rollout, and the DORA
measures that describe delivery over time. Read this while designing the
verification half of a change; `../SKILL.md` owns when to reach for it.

## Health Check Design

### Three Probe Types

| Probe         | Validates               | Endpoint   | Period          |
| ------------- | ----------------------- | ---------- | --------------- |
| **Liveness**  | Process still alive     | `/healthz` | 10 s            |
| **Readiness** | Ready to serve traffic  | `/readyz`  | 5 s             |
| **Startup**   | Initialization complete | `/healthz` | 1 s (max 300 s) |

### Kubernetes Probe Configuration

```yaml
livenessProbe:
  httpGet:
    path: /healthz
    port: 8080
  initialDelaySeconds: 15
  periodSeconds: 10
  failureThreshold: 3

readinessProbe:
  httpGet:
    path: /readyz
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 5
  failureThreshold: 3

startupProbe:
  httpGet:
    path: /healthz
    port: 8080
  failureThreshold: 30
  periodSeconds: 10
```

### Health Endpoint Response Structure

```json
{
  "status": "healthy",
  "version": "2.1.0",
  "checks": {
    "database": { "status": "healthy", "latency_ms": 2 },
    "cache": { "status": "healthy", "latency_ms": 1 },
    "external": { "status": "degraded", "latency_ms": 500 }
  }
}
```

Readiness endpoint must return non-2xx when any required dependency is unhealthy — this is what prevents traffic routing to broken pods.

---

## Rollback Procedures

### Automatic Rollback Triggers

| Metric            | Threshold | Window            |
| ----------------- | --------- | ----------------- |
| HTTP 5xx rate     | > 5%      | 2 min consecutive |
| Latency p99       | > 3 s     | 5 min consecutive |
| Pod restart count | > 3       | Within 10 min     |
| Memory / CPU      | > 90%     | 5 min consecutive |

### GitOps Rollback Decision Tree

```
Trigger detected
    ├── ArgoCD Rollout (Canary/Blue-Green)
    │       → Revert or abort through the repository-backed rollback plan
    │       → Let ArgoCD reconcile from the merged Git state
    │
    └── Standard Deployment (Rolling)
            → Revert image tag commit in Git → PR/merge → ArgoCD reconciliation
```

After rollback:

1. Draft an alert for an authorized operator; send via Slack/PagerDuty only with explicit authorization.
2. Conduct RCA (see `rca-methodology` skill).
3. Fix root cause, re-deploy via normal GitOps path.

---

## DORA Metrics

### Four Key Metrics

| Metric                   | Description                        | Elite                    | High         | Medium       | Low       |
| ------------------------ | ---------------------------------- | ------------------------ | ------------ | ------------ | --------- |
| **Deployment Frequency** | How often to production            | On-demand (multiple/day) | Daily–weekly | Monthly      | < Monthly |
| **Lead Time**            | Commit → production                | < 1 h                    | 1 day–1 week | 1–4 weeks    | > 1 month |
| **Change Failure Rate**  | % of deployments causing incidents | < 5%                     | 6–15%        | 16–30%       | > 30%     |
| **Recovery Time (MTTR)** | Detection → resolution             | < 1 h                    | < 1 day      | 1 day–1 week | > 1 week  |

### Measurement Formulas

```
Deployment Frequency  = production deploy count / time period
Lead Time             = production_deploy_time − first_commit_time
Change Failure Rate   = rollback_deploys / total_deploys × 100
Recovery Time (MTTR)  = incident_resolution_time − incident_detection_time
```

---
