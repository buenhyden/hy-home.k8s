# hy-home.k8s

AI-Optimized Home Lab Kubernetes Platform using GitOps.

This repository manages a Kubernetes cluster using the **GitOps** pattern. It is designed to be highly structured, strictly governed, and optimized for both human developers and AI coding assistants.

---

## 🚀 Key Features

- **GitOps Continuous Delivery**: Fully automated deployments using [ArgoCD](https://argoproj.github.io/argo-cd/).
- **Service Mesh**: Robust networking, mTLS, and traffic management via [Istio](https://istio.io/).
- **Observability Stack**: Unified logging, metrics, and tracing using **LGTM** (Loki, Grafana, Tempo, Mimir/Prometheus).
- **Security & Governance**: Policy enforcement with [Kyverno](https://kyverno.io/), secret management with [Sealed Secrets](https://github.com/bitnami-labs/sealed-secrets), and certificate automation with [Cert-manager](https://cert-manager.io/).
- **AI-Ready Structure**: Standardized layouts and machine-readable metadata via `.agent/` for seamless AI collaboration.

---

## 🏗️ Project Structure

The repository follows a strict separation of concerns to maximize modularity and clarity:

| Directory | Description |
| :--- | :--- |
| [`.agent/`](file:///d:/hy-home.k8s/.agent) | AI agent rules, skills, workflows, and governance standards. |
| [`apps/`](file:///d:/hy-home.k8s/apps) | Application manifests and templates for developer services. |
| [`bootstrap/`](file:///d:/hy-home.k8s/bootstrap) | Initial cluster setup scripts and GitOps initialization. |
| [`clusters/`](file:///d:/hy-home.k8s/clusters) | Cluster-specific configurations and ArgoCD application definitions. |
| [`infrastructure/`](file:///d:/hy-home.k8s/infrastructure) | Core cluster components (Controllers, Security, Observability, etc.). |
| [`docs/`](file:///d:/hy-home.k8s/docs) | Project documentation, ADRs, and technical deep-dives. |

---

## 📐 Architecture

This project adheres to a strict logical layering and directional dependency model. For deep technical details on design principles, data flow, and networking, see [ARCHITECTURE.md](file:///d:/hy-home.k8s/ARCHITECTURE.md).

### Logical Layers

1. **Agent Layer**: Rule-driven autonomous execution via specialized AI personas.
2. **Governance Layer**: Standardized skeletons, identifiers, and ADRs.
3. **Application Layer**: Business logic and domain entities (GitOps-managed).
4. **Infrastructure Layer**: Deployment & environment management (Core Controllers).

---

## 🛠️ Getting Started

### 1. Prerequisites

- A running Kubernetes cluster (e.g., Docker Desktop K8s, Kind, or K3s).
- `kubectl`, `helm`, and `kustomize` installed locally.
- [ArgoCD CLI](https://argoproj.github.io/argo-cd/getting_started/#2-download-argocd-cli) (optional but recommended).

### 2. Cluster Bootstrap

Navigate to [`bootstrap/`](file:///d:/hy-home.k8s/bootstrap) and run the setup scripts:

```bash
# Install ArgoCD and base components
./bootstrap/cluster-setup.sh

# Deploy root applications
./bootstrap/root-apps.sh
```

### 3. Adding an Application

1. **Use Templates**: Navigate to [`apps/_templates`](file:///d:/hy-home.k8s/apps/_templates) and copy a template.
2. **Configure**: Update placeholders in the copied manifests.
3. **Register**: Create an ArgoCD `Application` in [`clusters/docker-desktop/applications/`](file:///d:/hy-home.k8s/clusters/docker-desktop/applications/).
4. **Deploy**: Commit and push to trigger GitOps sync.

For more details, see the [Adding Applications Guide](file:///d:/hy-home.k8s/docs/guides/adding-applications.md).

---

## 📚 Detailed Documentation

Explore our in-depth guides and standards in the [`docs/`](file:///d:/hy-home.k8s/docs) folder:

- **Operational Guides**: [Cluster Bootstrap](file:///d:/hy-home.k8s/docs/guides/cluster-bootstrap.md), [Secret Management](file:///d:/hy-home.k8s/docs/guides/secret-management.md).
- **Standards**: [Naming Conventions](file:///d:/hy-home.k8s/docs/standards/naming-conventions.md), [GitOps Workflow](file:///d:/hy-home.k8s/docs/standards/gitops-standard.md).
- **Infrastructure**: [Service Mesh](file:///d:/hy-home.k8s/docs/infrastructure/service-mesh.md).

---

## 🤝 AI & Human Collaboration

This project is built to be "Agentic-First". We utilize specialized AI personas documented in [AGENTS.md](file:///d:/hy-home.k8s/AGENTS.md).

### Commit Message Standards

We follow a strict format for better traceability and automated changelogs. See [`.gitmessage.json`](file:///d:/hy-home.k8s/.gitmessage.json).

- Format: `<type>(<scope>): <subject>`
- Types: `feat`, `fix`, `refactor`, `docs`, `chore`, `test`.

---

## 📄 License

This project is licensed under the [LICENSE](file:///d:/hy-home.k8s/LICENSE) found in the root directory.
