# Cluster Security Audit Dimensions

What to look for in each of the five dimensions — RBAC, NetworkPolicy,
secret handling, container security context, and image supply chain — with
the detection targets and checklists for each. Read the dimension the audit
is currently in; `../SKILL.md` owns the order, the severity meaning, and the
report.

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
