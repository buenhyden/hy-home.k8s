# Kubernetes Security Rules for Agents

## Workload Isolation

- Prefer running untrusted or experimental workloads in dedicated namespaces with restricted permissions.
- Do not schedule sensitive workloads on the same nodes as untrusted or publicly exposed workloads when PodSecurity or node isolation mechanisms are available.

## Pod and Container Security

- Avoid running containers as `root` unless there is a clear, documented justification.
- Use securityContext settings such as `runAsNonRoot`, `readOnlyRootFilesystem`, and dropping unnecessary Linux capabilities.
- Avoid hostPath mounts for sensitive host directories unless absolutely necessary, and document such usage clearly.

## Network and Access Controls

- Encourage the use of NetworkPolicies to restrict pod-to-pod and pod-to-external traffic, defaulting to deny-all and adding only required allowances.
- Do not expose Services via LoadBalancer or NodePort types unless the user explicitly intends external access.
- When Ingress resources are created or modified, ensure TLS and host restrictions are correctly configured.

## Secrets and Configuration

- Store secrets in Kubernetes Secrets or external secret managers and never inline them in plain text manifests or code.
- Use ConfigMaps and environment variables for non-sensitive configuration, and avoid baking configuration directly into container images when environment-specific values are required.
- Recommend encryption at rest for Secrets where the cluster supports it.

## RBAC Best Practices

- Assign permissions at the namespace level whenever possible and use RoleBindings instead of ClusterRoleBindings when scope is limited.
- Minimize the number of service accounts with elevated permissions and avoid distributing privileged tokens broadly.
- Regularly review RBAC policies and remove unused roles, bindings, and service accounts.

## Auditability and Change Control

- The agent must ensure that any high-impact or security-relevant change is traceable via:
  - Version-controlled manifests.
  - Clear commit messages.
  - Optional change logs.
- For production clusters, the agent should recommend routing changes through a CI/CD pipeline rather than direct `kubectl` access.
