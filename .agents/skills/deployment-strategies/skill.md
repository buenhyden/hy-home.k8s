---
name: deployment-strategies
description: "Use when comparing or designing Kubernetes and ArgoCD deployment strategies, including Blue-Green, Canary, Rolling update, rollback, zero-downtime deployment, progressive delivery, probes, and DORA metrics. Monitoring tool setup and actual CI pipeline configuration are outside this skill's scope."
---

# Deployment Strategies — Kubernetes & ArgoCD Deployment Strategy Catalog

Reference patterns for selecting and implementing deployment strategies in Kubernetes clusters managed via ArgoCD.

## Strategy Comparison

| Strategy       | Downtime | Risk     | Infra Cost | Rollback Speed | Best For                               |
| -------------- | -------- | -------- | ---------- | -------------- | -------------------------------------- |
| **Rolling**    | None     | Medium   | Low        | Medium         | General workloads                      |
| **Blue-Green** | None     | Low      | 2×         | Instant        | Mission-critical services              |
| **Canary**     | None     | Very Low | Slight     | Instant        | High-traffic / high-risk releases      |
| **Recreate**   | Yes      | High     | None       | Slow           | Dev/staging only                       |
| **A/B Test**   | None     | Low      | Slight     | Instant        | Feature experiments                    |
| **Shadow**     | None     | None     | 2×         | N/A            | Performance / compatibility validation |

---

## 1. Rolling Update

```
Pool: [v1] [v1] [v1] [v1]
→    [v2] [v1] [v1] [v1]
→    [v2] [v2] [v1] [v1]
→    [v2] [v2] [v2] [v1]
→    [v2] [v2] [v2] [v2]  ✓
```

**Kubernetes manifest:**

```yaml
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1 # or 25%
      maxSurge: 1 # or 25%
```

- **Pros**: No extra infrastructure; gradual rollout limits blast radius.
- **Cons**: v1 and v2 pods coexist — APIs must be backward-compatible during the transition window.

**GitOps rollback:**

```bash
# Revert the image tag or rollout manifest commit.
git revert <commit-sha>

# Open or update a PR, wait for review/merge, then let ArgoCD reconcile from Git.
```

Direct cluster mutation commands are outside the normal path and require explicit human emergency approval.

---

## 2. Blue-Green Deployment

```
Blue  (active):  [v1][v1][v1]  ← 100% traffic
Green (staging): [v2][v2][v2]  ← 0% traffic

After switch:
Blue:  [v1][v1][v1]  ← 0% (standby for rollback)
Green: [v2][v2][v2]  ← 100% traffic
```

**ArgoCD Rollouts CRD (preferred for GitOps):**

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: my-app
spec:
  strategy:
    blueGreen:
      activeService: my-app-active
      previewService: my-app-preview
      autoPromotionEnabled: false # require manual promotion gate
      scaleDownDelaySeconds: 300 # keep Blue alive 5 min post-switch
```

**Promotion procedure:**

1. ArgoCD deploys new version to preview (Green) replicas.
2. Run smoke tests against `previewService`.
3. Promote through the approved repository-backed release gate, or an explicitly approved Argo Rollouts manual gate.
4. Monitor for 5 minutes; keep Blue scaled until confirmed stable.
5. `scaleDownDelaySeconds` elapses → Blue automatically removed.

**Rollback:** use the repository-backed rollback plan. Direct Argo Rollouts abort actions require explicit human emergency approval.

---

## 3. Canary Deployment

```
Stage 1: [v1 × 95%] [v2 × 5%]
Stage 2: [v1 × 80%] [v2 × 20%]
Stage 3: [v1 × 50%] [v2 × 50%]
Stage 4: [v2 × 100%]           ✓
```

**ArgoCD Rollouts CRD:**

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
spec:
  strategy:
    canary:
      steps:
        - setWeight: 5
        - pause: { duration: 10m }
        - analysis:
            templates:
              - templateName: success-rate
        - setWeight: 20
        - pause: { duration: 30m }
        - setWeight: 50
        - pause: { duration: 1h }
        - setWeight: 100
      canaryService: my-app-canary
      stableService: my-app-stable
```

**Per-stage validation criteria:**

| Stage | Traffic | Wait   | Validation              |
| ----- | ------- | ------ | ----------------------- |
| 1     | 5%      | 10 min | Error rate, p99 latency |
| 2     | 20%     | 30 min | + business metrics      |
| 3     | 50%     | 1–2 h  | All metrics             |
| 4     | 100%    | —      | Complete                |

**Automatic rollback conditions:**

- HTTP 5xx rate > 1% (2× baseline)
- p99 latency > 2 s (50% above baseline)
- Business metric anomaly (conversion rate, revenue, etc.)

---

## 4. A/B Testing

- Traffic split by user segment (header, cookie, user-id hash).
- Integrate with feature flag systems (LaunchDarkly, Flagsmith, etc.).
- Promote only after reaching statistical significance.
- Kubernetes implementation: Istio `VirtualService` weighted routes, or Nginx Ingress canary annotations.

---

## 5. Shadow (Traffic Mirroring)

- Production requests are mirrored to the new version; responses are discarded.
- Zero user impact — used solely for performance, error rate, and compatibility validation.
- Kubernetes: Istio `VirtualService` mirror + mirrorPercentage.

---

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

1. Alert via Slack/PagerDuty.
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

## GitOps Branch Strategy Mapping

| Branch Strategy | Deploy Flow                                | Best For                          |
| --------------- | ------------------------------------------ | --------------------------------- |
| **Trunk-Based** | `main` → staging → production              | Small teams, frequent releases    |
| **GitHub Flow** | `feature` → PR → `main` → production       | Medium teams, mature GitOps       |
| **GitFlow**     | `feature` → `develop` → `release` → `main` | Large teams, fixed release cycles |

### ArgoCD App-of-Apps Environment Rules

```
feature/*  → PR preview environment (ephemeral ArgoCD app, auto-deleted on PR close)
main       → auto-sync → staging (full test suite gate)
main + tag → manual promotion gate → production
hotfix/*   → emergency path → production (simplified approval, mandatory post-incident review)
```
