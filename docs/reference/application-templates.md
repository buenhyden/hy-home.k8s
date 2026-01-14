# Application Templates

The `apps/_templates` directory contains Helm chart starters for creating new services in `hy-home.k8s`.

## Available Templates

### 1. Backend Service (`apps/_templates/backend`)

A standard backend microservice template including:

- **Deployment**: Configured for high availability (default 3 replicas).
- **Service**: ClusterIP for internal communication.
- **ServiceAccount**: Dedicated identity for IAM.
- **PrometheusMonitor**: Auto-configured metrics scraping.

### 2. Frontend Application (`apps/_templates/frontend`)

A frontend application template including:

- **Deployment**: Standard web server configuration.
- **Service**: Target for Ingress traffic.
- **Istio VirtualService**: Routing rules (canary ready).

## Usage

To create a new application using a template:

1. **Copy** the basic folder structure:

    ```bash
    cp -r apps/_templates/backend apps/my-new-service
    ```

2. **Update** `Chart.yaml` with the new service name.
3. **Configure** `values.yaml` with specific environment variables and resource limits.
4. **Add** to ArgoCD manifest in `apps/root-app/`.
