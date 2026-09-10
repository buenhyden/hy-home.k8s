---
name: "k8s-security-audit"
description: "Use when auditing Kubernetes RBAC, NetworkPolicy gaps, Secret handling, container security context, image supply chain, CIS benchmark posture, or related cluster security hardening. Real-time intrusion detection and WAF configuration are outside this skill's scope."
disable-model-invocation: true
---

Read `.agents/governance/approval-and-safety.md` and the selected role before
using this procedure. Skill invocation does not authorize additional actions.

# k8s Security Audit — Cluster Security Assessment Workflow

Structured audit pipeline covering RBAC → NetworkPolicy → Secrets → Container security → Supply chain.

## Audit Dimensions

### 1. RBAC Analysis

**Detection Targets:**

| Risk Pattern                                   | Severity | Example                                       |
| ---------------------------------------------- | -------- | --------------------------------------------- |
| `ClusterRole` with `*` verbs                   | Critical | `verbs: ["*"]` on `secrets` resource          |
| `ClusterRoleBinding` to service accounts       | High     | SA with cluster-wide list/get on secrets      |
| `automountServiceAccountToken: true` (default) | Medium   | Pods that do not need API access              |
| Overly broad namespace-scoped roles            | Medium   | `Role` with `get/list/watch` on all resources |
| `system:masters` group membership              | Critical | Any non-bootstrap entity in this group        |

**RBAC Audit Checklist:**

```yaml
# Least-privilege check: list bindings per SA
# Flag: any SA with secrets read access it does not need
# Flag: any RoleBinding/ClusterRoleBinding using wildcard verbs
# Flag: default SA with non-empty automount
```

**Output format:**

```markdown
| Resource | Binding               | Subject    | Overpermission | Severity |
| -------- | --------------------- | ---------- | -------------- | -------- |
| secrets  | cluster-admin-binding | sa/default | list/get/watch | CRITICAL |
```

### 2. NetworkPolicy Gap Analysis

**Default-deny baseline check:**

```yaml
# Expected in every namespace:
kind: NetworkPolicy
spec:
  podSelector: {} # selects all pods
  policyTypes: [Ingress, Egress]
  # No ingress/egress rules = deny all
```

**Detection Targets:**

| Risk Pattern                         | Severity |
| ------------------------------------ | -------- |
| Namespace with no NetworkPolicy      | High     |
| Pods reachable from `0.0.0.0/0`      | Critical |
| Unrestricted egress to internet      | High     |
| DNS-only egress not enforced         | Medium   |
| Cross-namespace unrestricted ingress | High     |

**Verification approach:**

- List all namespaces
- For each namespace: check if `NetworkPolicy` resources exist
- For each pod: verify ingress/egress rules cover it
- Flag namespaces where `podSelector: {}` deny-all is absent

### 3. Secret Handling

**Stop-condition patterns (immediate block):**

- Plaintext secrets in manifest annotations or labels
- Secrets embedded in `ConfigMap` data values
- `KUBECONFIG` or credentials mounted via `hostPath`
- Secret values visible in container args or env vars (non-SecretKeyRef)

**Accepted patterns:**

```yaml
# Correct: reference, not value
env:
  - name: DB_PASSWORD
    valueFrom:
      secretKeyRef:
        name: db-credentials
        key: password
```

**Rejected patterns:**

```yaml
# Wrong: plaintext in env
env:
  - name: DB_PASSWORD
    value: 'mysecretpassword'

# Wrong: secret embedded in ConfigMap
# Wrong: base64 in annotation (base64 is NOT encryption)
```

**Secret age and rotation:**

- Flag Secrets older than 90 days without rotation evidence
- Flag Secrets with `immutable: false` that contain credentials

### 4. Container Security Context

**Required security context for production workloads:**

```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 1000 # non-zero UID
  readOnlyRootFilesystem: true
  allowPrivilegeEscalation: false
  capabilities:
    drop: ['ALL']
    add: [] # add only if strictly required
```

**Detection Targets:**

| Risk Pattern                                 | Severity |
| -------------------------------------------- | -------- |
| `runAsUser: 0` (root)                        | Critical |
| `privileged: true`                           | Critical |
| `allowPrivilegeEscalation: true`             | High     |
| `hostPID: true` or `hostNetwork: true`       | Critical |
| `hostPath` volume mounts                     | High     |
| Missing `readOnlyRootFilesystem`             | Medium   |
| `capabilities.add: ["NET_ADMIN"]` or similar | High     |

### 5. Image Supply Chain

**Verification targets:**

- Images must use digest pinning or immutable tags
- Images from unapproved registries are flagged
- No `latest` tag in production workloads

```yaml
# Correct: digest pinned
image: my-registry.io/app:v1.2.3@sha256:abc123...

# Rejected: floating tag
image: my-registry.io/app:latest
```

**Registry allowlist check:**

- Flag any image not from approved registries
- Flag images without vulnerability scan evidence in CI annotations

## Severity Classification

This table owns what a level obliges. It does not map manifest patterns onto
levels: `vulnerability-patterns` owns that mapping together with the conditions
that escalate a pattern, and its assignment governs where the two could be read
against each other. The right column illustrates a tier rather than classifying
anything.

| Severity     | Response Required            | Illustrative finding                                                              |
| ------------ | ---------------------------- | --------------------------------------------------------------------------------- |
| **CRITICAL** | Immediate stop — block merge | Plaintext secrets, container runtime socket mounted, cluster-admin to workload SA |
| **HIGH**     | Fix before next release      | Missing NetworkPolicy, root or privileged containers, unrestricted egress         |
| **MEDIUM**   | Fix within sprint            | Missing readOnlyRootFilesystem, default SA token automount                        |
| **LOW**      | Track in backlog             | Image tag conventions, label hygiene                                              |

## Audit Report Format

```markdown
# Security Audit Report

**Scope**: [namespace/cluster/path]
**Date**: YYYY-MM-DD
**Auditor**: security-auditor agent
**Audit Type**: [RBAC / Network / Secrets / Full]

## Executive Summary

- **Overall Posture**: PASS / CONDITIONAL / BLOCK
- **Critical findings**: N
- **High findings**: N

## Findings

### CRITICAL

| ID  | Resource | Issue | Evidence | Remediation |
| --- | -------- | ----- | -------- | ----------- |

### HIGH

...

### MEDIUM

...

## Remediation Priority

1. [Item] — by [date]
2. ...

## Closing State

| Level    | State recorded                                                          |
| -------- | ------------------------------------------------------------------------ |
| CRITICAL | Resolved, or unresolved and routed by name to whoever decides acceptance |
| HIGH     | Remediation owner and target release, or explicitly unassigned           |
```

State where each finding stands rather than ticking it off. Accepting an
unresolved CRITICAL finding weakens security semantics, which
[approval and safety](../../governance/approval-and-safety.md) places outside
what an audit may decide for itself, and [the SDLC flow](../../governance/sdlc.md)
never infers approval from a checkbox. A report that carries the acceptance
box also carries the invitation to tick it.

## Failure Handling

- Plaintext secret exposure → **immediate stop condition**; do not proceed until resolved.
- RBAC findings and network isolation gaps → route remediation to the
  implementation owner, or record them for the supervising owner when the
  selected role has no implementation handoff.
- Escalate ambiguous security decisions to the supervising owner.

## Related Skills

- `vulnerability-patterns` — Kubernetes manifest vulnerability pattern catalog (YAML/Helm)
