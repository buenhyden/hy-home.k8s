# Development Workflow

This guide outlines the process for setting up your local development environment and contributing to the `hy-home.k8s` project.

## Prerequisites

Before you begin, ensure you have the following tools installed:

- **Docker Desktop**: Required to run the local Kubernetes cluster.
- **Kind**: For creating local clusters.
- **Kubectl**: For interacting with the cluster.
- **WSL 2** (Windows users): Recommended environment for running scripts.

## 1. Setting Up the Local Environment

### Clone the Repository

```bash
git clone https://github.com/buenhyden/hy-home.k8s.git
cd hy-home.k8s
```

### Initialize the Cluster

We use a helper script to spin up a Kind cluster with the necessary configuration.

```bash
./bootstrap/cluster-setup.sh
```

This script will:

- Create a Kind cluster named `hy-home`.
- Configure `MetalLB` for local load balancing.
- Apply the `Ingress Nginx` controller.

### Install ArgoCD

Once the cluster is running, install the GitOps engine.

```bash
./bootstrap/argocd-install.sh
```

### Apply Root Applications

Finally, sync the state from the repository to the cluster.

```bash
./bootstrap/root-apps.sh
```

## 2. Making Changes

### Branching Strategy

- Main branch: `main` (Protected).
- Feature branches: `feat/description`, `fix/issue-id`.

### Testing Changes

Since this is a GitOps project, the "test" is often applying the manifest to your local cluster.

1. Create your manifest or change the configuration.
2. Manually apply it to verify syntax and immediate behavior (optional but recommended for fast feedback).

   ```bash
   kubectl apply -k ./path/to/kustomization
   ```

3. Commit your changes to push them through the GitOps pipeline (Autosync is usually enabled for the local environment).

## 3. Commit Standards

We follow **Conventional Commits** to streamline release notes and versioning.

- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that do not affect the meaning of the code (white-space, formatting, etc)
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `chore`: Changes to the build process or auxiliary tools and libraries such as documentation generation

Example:

```bash
git commit -m "feat(infra): add redis operator to external services"
```
