# Kubernetes Multi-environment Rules for Agents

## Environment Strategy

- Treat each environment (for example, dev, staging, prod) as a first-class concept, represented by either:
  - Separate namespaces within a cluster, or
  - Separate clusters per environment, depending on the organization’s strategy.
- Keep application manifests as shared as possible between environments, using overlays or values to represent differences.

## Configuration Differences

- Use Helm values files or Kustomize overlays to manage environment-specific configuration such as:
  - Replica counts and resource sizes.
  - External service endpoints.
  - Feature flags and logging levels.
- Avoid copying and diverging entire directories of manifests per environment; prefer parameterization and overlays.

## “Build Once, Deploy Many” Principle

- Container images should be built once and reused across environments; only configuration should vary at deploy time.
- The agent should not bake environment-specific configuration into the image; use environment-specific manifests instead.

## Safety Rules

- For production environments, enforce stricter rules:
  - No direct edits via `kubectl edit`; use configuration files and pull requests.
  - Require explicit user confirmation or CI/CD-based promotion before applying changes.
- Clearly label resources with environment identifiers (for example, `environment: dev`) for observability and policy enforcement.
