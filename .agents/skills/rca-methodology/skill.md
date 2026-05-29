---
name: rca-methodology
description: "Use when performing root cause analysis with 5 Whys, Fishbone diagrams, Fault Tree Analysis, change analysis, incident cause analysis, or cognitive-bias checks. Timeline reconstruction and remediation planning are outside this skill's scope."
---

# RCA Methodology — Root Cause Analysis Technique Reference

Structured analysis techniques for systematically tracing cluster incident root causes.

## 1. 5 Whys Technique

### Procedure

```
Problem: Payment service namespace unreachable for 30 minutes.

Why 1: Why was the namespace unreachable?
→ The Pod readiness probe was failing continuously.

Why 2: Why was the readiness probe failing?
→ The application could not connect to the database.

Why 3: Why could it not connect to the database?
→ The Secret containing the DB credentials was rotated but not updated in the manifest.

Why 4: Why was the Secret not updated?
→ The rotation runbook did not include a step to update the k8s Secret resource.

Why 5: Why was there no such step in the runbook?
→ Secret rotation was previously handled manually without a documented procedure.

Root Cause: Missing runbook step for propagating credential rotation to cluster Secrets
```

### 5 Whys Pitfalls

| Pitfall                   | Description                        | Prevention                                   |
| ------------------------- | ---------------------------------- | -------------------------------------------- |
| Stopping too early        | Concluding at step 2–3             | Ask: "Would fixing this prevent recurrence?" |
| Leading to blame          | Ending with "who made the mistake" | Focus on system and process causes           |
| Single path only          | Missing compound causes            | Review branches at each step                 |
| Speculation-based answers | Hypotheses without evidence        | Verify with logs, events, or metrics         |

## 2. Fishbone Diagram (Ishikawa)

```
               +- People --------- Operator unaware of rotation procedure
               |                   Code review skipped for Secret update
               |
               +- Process -------- Rotation runbook incomplete
               |                   No pre-deploy Secret validation step
               |
Namespace  <---+- Technology ----- Readiness probe too aggressive
Unreachable    |                   No Secret sync mechanism in place
               |
               +- Environment ---- Staging Secret not rotated (diverged)
               |                   Namespace network policy blocking DNS
               |
               +- Monitoring ----- No alert for Secret age or staleness
                                   DB connection errors not surfaced to dashboard
```

### 6M Categories Applied to Kubernetes Incidents

| Traditional 6M | Kubernetes Application  | Investigation Items                                      |
| -------------- | ----------------------- | -------------------------------------------------------- |
| Man            | People/Team             | Runbook training, on-call handoff, review skips          |
| Method         | Process                 | Deployment procedures, change management, approval gates |
| Machine        | Infrastructure/Platform | Cluster version, node pressure, control-plane health     |
| Material       | Manifests/Config        | Secret contents, ConfigMap values, image tags            |
| Measurement    | Observability           | Alerts, metrics, log coverage, tracing gaps              |
| Environment    | Cluster Environment     | Namespace isolation, network policy, resource quotas     |

## 3. Fault Tree Analysis (FTA)

```
                    Namespace Unreachable (Top Event)
                          |
                    +-----OR-----+
                    |            |
              Pod Failure    Network Failure
                |                |
          +-----OR-----+  +------AND------+
          |             |  |               |
    Crash Loop   OOM Kill  NetworkPolicy  DNS Failure
          |
    +-----AND-----+
    |              |
Bad Config    Probe Failure
```

**Probability Estimation:**

```
OR gate:  P(A OR B)  = 1 - (1-P(A)) × (1-P(B))
AND gate: P(A AND B) = P(A) × P(B)

Example: P(bad config)=0.2, P(probe failure)=0.3
  P(crash loop) = 0.2 × 0.3 = 0.06 (6%)
```

## 4. Change Analysis

Investigate all changes in the window before the incident.

```markdown
| Change Time | Change Content                        | Author     | Scope      | Correlation   |
| ----------- | ------------------------------------- | ---------- | ---------- | ------------- |
| T-2h        | Payment API image bumped to v2.3      | Dev        | payment ns | HIGH          |
| T-1h        | ArgoCD sync triggered by drift        | ArgoCD     | payment ns | HIGH          |
| T-30m       | Network policy applied to database ns | Ops        | db ns      | MEDIUM        |
| T-10m       | Alert fired: DB connection errors     | Monitoring | —          | LOW (symptom) |
```

**Correlation criteria:**

1. **Temporal proximity** — Change time vs. incident onset time
2. **Scope match** — Change blast radius vs. incident impact scope
3. **Rollback effect** — Does reverting the change resolve the incident?

## 5. Cognitive Bias Prevention Checklist

| Bias                              | Description                                             | Prevention                                                  |
| --------------------------------- | ------------------------------------------------------- | ----------------------------------------------------------- |
| **Confirmation bias**             | Collecting only evidence that fits the first hypothesis | Actively search for counterexamples                         |
| **Hindsight bias**                | "Obviously this was the cause"                          | Judge based only on information available at detection time |
| **Availability bias**             | Equating with a recently seen similar incident          | Enforce evidence-based analysis each time                   |
| **Fundamental attribution error** | Attributing to human error                              | Prioritize system and process causes                        |
| **Anchoring**                     | Fixating on the initial incident report                 | Analyze independently from multiple angles                  |

## RCA Technique Selection Guide

| Situation                             | Recommended Technique             | Reason                               |
| ------------------------------------- | --------------------------------- | ------------------------------------ |
| Simple incident, fast analysis needed | 5 Whys                            | Lightweight; can be done immediately |
| Suspected compound causes             | Fishbone                          | Multi-dimensional cause exploration  |
| Safety-related or severe incidents    | FTA                               | Quantitative and systematic          |
| Post-deployment incidents             | Change Analysis                   | Rapidly narrows candidate causes     |
| All cases                             | 5 Whys + Change Analysis combined | Fast yet structured                  |

## Output Format

Save scratch RCA output to `_workspace/02_root_cause.md` during analysis, then
move durable incident or postmortem findings into `docs/05.operations/incidents/` or
`docs/05.operations/incidents/postmortems/` when a record is required. Use this structure:

```markdown
# Root Cause Analysis

## Primary Root Cause

[One-sentence statement of the confirmed root cause]

## Contributing Factors

| Factor   | Category                         | Evidence                     |
| -------- | -------------------------------- | ---------------------------- |
| [Factor] | [Process/Tech/People/Monitoring] | [Log/event/metric reference] |

## 5 Whys Chain

Why 1: [Question] → [Answer]
Why 2: [Question] → [Answer]
Why 3: [Question] → [Answer]
Why 4: [Question] → [Answer]
Why 5: [Question] → [Answer]
Root Cause: [Conclusion]

## Bias Checks Performed

- [ ] Counterexamples searched
- [ ] Evidence-based (not verbal assumption)
- [ ] System/process focus confirmed (no blame language)
```
