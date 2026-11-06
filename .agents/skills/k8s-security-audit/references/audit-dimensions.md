# Cluster Security Audit Dimensions

What to look for in each of the five dimensions — RBAC, NetworkPolicy,
secret handling, container security context, and image supply chain — with
the detection targets and checklists for each. Where `vulnerability-patterns`
lists a pattern, its level governs and the cell says so; any other row takes
the tier in `../SKILL.md`. Read the dimension the audit
is currently in; `../SKILL.md` owns the order, the severity meaning, and the
report.

## Audit Dimensions

### 1. RBAC Analysis

**Detection Targets:**

| Risk Pattern                                   | Severity                           | Example                                       |
| ---------------------------------------------- | ---------------------------------- | --------------------------------------------- |
| `ClusterRole` with `*` verbs                   | Level per `vulnerability-patterns` | `verbs: ["*"]` on `secrets` resource          |
| `ClusterRoleBinding` to service accounts       | Level per `vulnerability-patterns` | SA with cluster-wide list/get on secrets      |
| `automountServiceAccountToken: true` (default) | Medium                             | Pods that do not need API access              |
| Overly broad namespace-scoped roles            | Medium                             | `Role` with `get/list/watch` on all resources |
| `system:masters` group membership              | Critical                           | Any non-bootstrap entity in this group        |

**RBAC Audit Checklist:**

```yaml
# Least-privilege check: list bindings per SA
# Flag: any SA with secrets read access it does not need
# Flag: any RoleBinding/ClusterRoleBinding using wildcard verbs
# Flag: default SA with non-empty automount
```

**Output format:**

```markdown
| Resource | Binding               | Subject    | Overpermission | Level    |
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

| Risk Pattern                         | Severity                           |
| ------------------------------------ | ---------------------------------- |
| Namespace with no NetworkPolicy      | Level per `vulnerability-patterns` |
| Pods reachable from `0.0.0.0/0`      | Critical                           |
| Unrestricted egress to internet      | High                               |
| DNS-only egress not enforced         | Medium                             |
| Cross-namespace unrestricted ingress | High                               |

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
    value: "mysecretpassword"

# Wrong: secret embedded in ConfigMap
# Wrong: base64 in annotation (base64 is NOT encryption)
```

**Secret age and rotation:**

- Flag Secrets older than 90 days without rotation evidence
- Flag Secrets with `immutable: false` that contain credentials

### 4. Container Security Context

**Required security context for any workload Argo CD reconciles:**

```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 1000 # non-zero UID
  readOnlyRootFilesystem: true
  allowPrivilegeEscalation: false
  capabilities:
    drop: ["ALL"]
    add: [] # add only if strictly required
```

**Detection Targets:**

| Risk Pattern                                 | Severity                           |
| -------------------------------------------- | ---------------------------------- |
| `runAsUser: 0` (root)                        | Level per `vulnerability-patterns` |
| `privileged: true`                           | Level per `vulnerability-patterns` |
| `allowPrivilegeEscalation: true`             | High                               |
| `hostPID: true` or `hostNetwork: true`       | Level per `vulnerability-patterns` |
| `hostPath` volume mounts                     | Level per `vulnerability-patterns` |
| Missing `readOnlyRootFilesystem`             | `k8s-security-audit` tier (MEDIUM) |
| `capabilities.add: ["NET_ADMIN"]` or similar | High                               |

### 5. Image Supply Chain

**Verification targets:**

- Images use an explicit non-latest tag or a digest, the rule `gitops/README.md`
  sets for every workload Argo CD reconciles
- No `latest` or implicit-latest tag in any such workload

```yaml
# Correct: digest pinned
image: registry.example/app:v1.2.3@sha256:abc123...

# Rejected: floating tag
image: registry.example/app:latest
```

**Registry and scan evidence:**

- The repository defines no approved-registry list, so a registry is a reviewer
  judgment, not a finding by itself.
- Vulnerability-scan evidence in CI annotations is not currently enforced; record
  its absence as a gap, not as a violation.
