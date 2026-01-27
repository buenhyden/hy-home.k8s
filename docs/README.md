# Project Documentation

Welcome to the detailed documentation for `hy-home.k8s`. This directory contains technical guides, project standards, and deep-dives into the platform infrastructure.

---

## 📂 Documentation Structure

### 📖 [Guides](./guides/README.md)

Step-by-step instructions for common operational tasks.

- [Adding Applications](./guides/adding-applications.md): Workflow for deploying new services.
- [Cluster Bootstrap](./guides/cluster-bootstrap.md): How to setup the cluster from scratch.
- [Secret Management](./guides/secret-management.md): Secure handling of sensitive data.
- [Development Workflow](./guides/development-workflow.md): Contributing and testing.
- [Disaster Recovery](./guides/disaster-recovery.md): Restoring the cluster.

### 🔄 [Lifecycle](./lifecycle/README.md)

Management of the platform from bootstrap to upgrades.

- [Bootstrap Process](./lifecycle/bootstrap-process.md): Zero-to-Hero installation.
- [Maintenance](./lifecycle/maintenance.md): Upgrades and key rotation.

### 📱 [Applications](./applications/README.md)

Documentation for the business logic layer.

- [Standards](./applications/standards.md): Best practices for apps.
- [Examples](./applications/examples.md): Templates and reference apps.

### ⚖️ [Standards](./standards/README.md)

Rules and conventions that govern the project.

- [Naming Conventions](./standards/naming-conventions.md): Unified naming for resources and files.
- [GitOps Standard](./standards/gitops-standard.md): Workflow for Git-based delivery.

### 🏗️ [Infrastructure](./infrastructure/README.md)

Detailed technical documentation on platform components.

- [Service Mesh](./infrastructure/service-mesh.md): Istio, mTLS, and Networking.
- [Observability Stack](./infrastructure/observability-stack.md): Monitoring with the LGTM stack.
- [Security & Governance](./infrastructure/security-governance.md): Policies and identity.
- [External Services](./infrastructure/external-services.md): Connectivity to databases.

### 📝 [ADR (Architectural Decision Records)](./adr/README.md)

Documentation of significant architectural decisions.

---

## 🏛️ Architecture Overview

For a high-level overview of the system design and technology stack, please refer to the root [ARCHITECTURE.md](../ARCHITECTURE.md).

## 🤝 Contribution

If you would like to contribute to the documentation, please see [CONTRIBUTING.md](../CONTRIBUTING.md).
