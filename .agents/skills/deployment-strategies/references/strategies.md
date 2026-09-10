# Kubernetes and Argo CD Deployment Strategy Catalog

Five strategies with their manifest shape, trade-offs, and the conditions
that suit each one, plus the comparison table that separates them. Read this
when choosing; `../SKILL.md` owns the procedure that turns a choice into a
reviewable change.

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
# Operator-only example; requires explicit Git mutation authorization.
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

**Automatic canary-abort conditions** — tighter than the release-wide
triggers under Rollback Procedures, because a canary aborts on a small early
signal from a small share of traffic:

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
