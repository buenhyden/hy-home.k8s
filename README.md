# hy-home.k8s

AI-Optimized Home Lab Kubernetes Platform using GitOps.

This repository manages a Kubernetes cluster using the **GitOps** pattern. It is designed to be highly structured and strictly governed, making it ideal for both human developers and AI coding assistants.

---

## 🚀 Key Features

- **GitOps Continuous Delivery**: Fully automated deployments using [ArgoCD](https://argoproj.github.io/argo-cd/).
- **Service Mesh**: Robust networking, mTLS, and traffic management via [Istio](https://istio.io/).
- **Full Observability Stack**: Centralized logging, metrics, and tracing using Loki, Prometheus, and Tempo.
- **Security & Governance**: Policy enforcement with Kyverno and secret management with Sealed Secrets.
- **AI-Ready Structure**: Standardized layouts and machine-readable metadata for seamless AI collaboration.

---

## 🏗️ Project Structure

The repository follows a clear separation of concerns:

| Directory | Description |
| --- | --- |
| [`apps/`](file:///d:/hy-home.k8s/apps) | Application manifests and templates for developer services. |
| [`infrastructure/`](file:///d:/hy-home.k8s/infrastructure) | Core cluster components (Controllers, Security, Observability, etc.). |
| [`clusters/`](file:///d:/hy-home.k8s/clusters) | Cluster-specific configurations and ArgoCD application definitions. |
| [`bootstrap/`](file:///d:/hy-home.k8s/bootstrap) | Initial cluster setup and GitOps initialization scripts. |
| [`.agent/`](file:///d:/hy-home.k8s/.agent) | AI agent rules, workflows, and governance standards. |

---

## 📐 Architecture

This project adheres to a strict logical layering and directional dependency model. For details on design principles and the technology stack, see [ARCHITECTURE.md](file:///d:/hy-home.k8s/ARCHITECTURE.md).

### Logical Layers

1. **Agent Layer**: Rule-driven autonomous execution.
2. **Governance Layer**: Standardized skeletons and identifiers.
3. **Application Layer**: Business logic and domain entities.
4. **Infrastructure Layer**: Deployment & environment management.

---

## 🛠️ Development Workflow

To add a new application or service:

1. **Use Templates**: Navigate to [`apps/_templates`](file:///d:/hy-home.k8s/apps/_templates) and copy the appropriate template (backend/frontend).
2. **Configure Manifests**: Follow the instructions in [`apps/README.md`](file:///d:/hy-home.k8s/apps/README.md) to customize placeholders.
3. **Register Application**: Create an ArgoCD application manifest in [`clusters/docker-desktop/applications/`](file:///d:/hy-home.k8s/clusters/docker-desktop/applications/).
4. **Commit & Push**: Push your changes to trigger automatic deployment by ArgoCD.

---

## 🤝 Contributing

We welcome contributions! Please refer to [CONTRIBUTING.md](file:///d:/hy-home.k8s/CONTRIBUTING.md) for our development standards.

### Commit Message Standards

We follow a specific commit message format for better traceability. See [`.gitmessage.json`](file:///d:/hy-home.k8s/.gitmessage.json) for the full schema.

- Format: `<type>(<scope>): <subject>`
- Types: `feat`, `fix`, `refactor`, `docs`, `chore`, etc.

---

## 📄 License

This project is licensed under the [LICENSE](file:///d:/hy-home.k8s/LICENSE) file in the root directory.
