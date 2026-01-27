# Infrastructure Documentation

This directory contains deep-dives into the core platform services that power the `hy-home.k8s` cluster.

## Platform Pillars

### 1. [Service Mesh (Istio)](./service-mesh.md)

Detailed configuration of the Istio control plane, ingress gateway, and mTLS enforcement.

### 2. [Observability Stack (LGTM)](./observability-stack.md)

Architecture of the logging, metrics, and tracing pipeline based on Grafana Alloy and the LGTM stack.

### 3. [Security & Governance](./security-governance.md)

How Kyverno, Cert-manager, and Sealed Secrets work together to secure the cluster.

### 4. [External Services](./external-services.md)

Guidelines for connecting the cluster to databases and services running on the host network.

- [Read the Deep Dive & Troubleshooting Guide](./external-services-deepdive.md)

### 5. [Network Controllers](./controllers.md)

Documentation for Ingress Nginx, MetalLB, and Istio Ingress Gateway.

### 6. [Storage Architecture](./storage.md)

How persistent volumes and storage classes are managed in the cluster.

---

## Management

All infrastructure components are managed via the **Infrastructure Root Application** in ArgoCD.
Source: [`clusters/docker-desktop/infrastructure/`](../../clusters/docker-desktop/infrastructure/)
