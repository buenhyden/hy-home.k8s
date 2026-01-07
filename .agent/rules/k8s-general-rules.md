# Kubernetes General Rules for Agents

## Scope and Goals

- The agent must manage Kubernetes manifests and commands in a way that does not depend on hard-coded file system paths.
- All configuration should be portable across environments (dev, staging, prod) and clusters, using relative paths and logical environment markers instead of absolute host paths.
- The agent should keep all Kubernetes-related changes declarative, versionable, and auditable.

## Path-agnostic Manifest Handling

- Never assume a fixed path such as `/home/user/project/k8s` or `C:\repo\k8s`.
- When locating manifests, the agent must:
  - Search the repository tree for common Kubernetes folders (for example, `k8s/`, `manifests/`, `deploy/`, `helm/`, `charts/`, `overlays/`).
  - Ask the user which directory should be treated as the primary Kubernetes configuration if multiple candidates exist.
- When generating new manifests, prefer:
  - A `k8s/` or `manifests/` folder at the repository root, or
  - Existing conventions already used in the repository (for example, a `deploy/` or `infra/` folder).

## Declarative Configuration First

- Prefer applying declarative YAML manifests or Helm/Kustomize configurations over imperative `kubectl` commands.
- Ensure that any change performed via imperative commands is also reflected in manifests, Helm values, or Kustomize overlays.
- Use `kubectl apply`, Helm, or Kustomize with configuration files stored in the repository instead of one-off script-only changes.

## Namespaces and Environments

- Do not rely on the current `kubectl` context implicitly; always be explicit about:
  - Cluster or context name.
  - Target namespace.
- Recommend using separate namespaces or clusters for different environments (for example, `dev`, `staging`, `prod`) while keeping manifests shared via Helm values or Kustomize overlays.
- The agent must never modify production namespaces or contexts unless the user clearly indicates that production changes are intended.

## Resource Management

- Always define CPU and memory `requests` and `limits` for Pods and containers to avoid unpredictable scheduling and resource contention.
- Use appropriate `readinessProbe` and `livenessProbe` definitions to allow Kubernetes to self-heal applications.
- Prefer Horizontal Pod Autoscalers or other autoscaling mechanisms where appropriate for stateless services.

## RBAC and Security

- Follow the principle of least privilege when defining Roles, RoleBindings, ClusterRoles, and ClusterRoleBindings.
- Avoid wildcard permissions such as `*` in `apiGroups`, `resources`, or `verbs` unless strictly necessary.
- Use Kubernetes Secrets for credentials and sensitive data, and do not hard-code secrets into manifests.
- Encourage the use of admission controllers, policy engines (for example, OPA Gatekeeper, Kyverno), and NetworkPolicies to enforce security baselines.

## Multi-cluster and Multi-context Behavior

- The agent must treat the kubeconfig as the source of truth for cluster access and should not hard-code cluster API endpoints.
- When multiple contexts or clusters are configured, the agent must:
  - List available contexts.
  - Ask the user which context and namespace to operate on.
  - Explicitly set the context in commands or configuration rather than relying on implicit defaults.
- The agent must never modify or merge kubeconfig files in a way that loses existing configuration.

## Logging, Monitoring, and Observability

- Ensure that workloads include reasonable logging configuration (stdout/stderr) compatible with typical Kubernetes logging stacks.
- Recommend using standardized labels (for example, `app`, `component`, `environment`) to integrate with monitoring, tracing, and alerting systems.
- When altering resources that affect monitoring (for example, ServiceMonitors, PodMonitors), the agent must document the changes in the repository.

## Documentation Expectations

- For any Kubernetes-related change, the agent should:
  - Explain the purpose and impact of the change in commit messages or comments.
  - Provide minimal instructions on how to apply, rollback, and verify the change using `kubectl`, Helm, or Kustomize commands.
- If the repository contains a `docs/` or `infra/` directory, keep Kubernetes documentation alongside existing infrastructure docs.
