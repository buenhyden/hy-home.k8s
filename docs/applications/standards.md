# Application Standards

To ensure reliability, observability, and manageability, all applications deployed to `hy-home.k8s` must adhere to the following standards.

## 1. Labeling Strategy

All resources must have the standard Kubernetes labels.

- `app.kubernetes.io/name`: The name of the application (e.g., `postgresql`).
- `app.kubernetes.io/instance`: The unique name of the release (often same as name).
- `app.kubernetes.io/version`: The version of the application.
- `app.kubernetes.io/part-of`: The larger system usually `hy-home`.
- `app.kubernetes.io/managed-by`: Usually `kustomize` or `argocd`.

## 2. Health Checks (Probes)

Every Pod **must** define Liveness and Readiness probes.

### Liveness Probe

- **Goal**: Detect if the app is deadlocked or broken.
- **Action**: Kills and restarts the container.
- **Config**:

  ```yaml
  livenessProbe:
    httpGet:
      path: /healthz
      port: 8080
    initialDelaySeconds: 5
    periodSeconds: 10
  ```

### Readiness Probe

- **Goal**: Detect if the app is ready to serve traffic.
- **Action**: Adds/Removes IP from Service Endpoints.
- **Config**:

  ```yaml
  readinessProbe:
    httpGet:
      path: /ready
      port: 8080
  ```

## 3. Resource Management

Containers generally should have **Requests** set to ensure scheduling guarantees, but **Limits** may be omitted or set high to allow bursting in a home-lab environment (unless strict isolation is needed).

```yaml
resources:
  requests:
    cpu: "100m"
    memory: "128Mi"
  limits:
    memory: "512Mi"
```

## 4. Configuration

- **ConfigMaps**: For non-sensitive configuration.
- **SealedSecrets**: For all sensitive data (API keys, passwords). **Never commit plain Kubernetes Secrets.**
