# Contributing to hy-home.k8s

Thank you for your interest in contributing to the `hy-home.k8s` project! We welcome contributions from everyone.

## Getting Started

Before you begin, please read our **[Development Workflow](docs/guides/development-workflow.md)**. This guide covers:

- Setting up your local Kind cluster.
- Installing necessary tools (`kubectl`, `argocd`, etc.).
- The "Zero-to-Hero" bootstrap process.

## How to Contribute

1. **Fork and Clone**: Fork the repository and clone it locally.
2. **Create a Branch**: Create a feature branch (e.g., `feat/new-app` or `fix/typo`).
3. **Make Changes**:
    - Follow the **[Application Standards](docs/applications/standards.md)** for new apps.
    - Adhere to the **[Naming Conventions](docs/standards/naming-conventions.md)**.
    - Test your manifests against your local cluster.
4. **Commit**: Use the [Conventional Commits](https://www.conventionalcommits.org/) format.
5. **Push and PR**: Push your branch and open a Pull Request.

## Coding Standards

- **YAML First**: All configuration should be declarative YAML.
- **Kustomize**: We use Kustomize for resource management. Avoid raw edits to `manifest.yaml` if a `kustomization.yaml` exists.
- **Secrets**: **NEVER** commit plain text secrets. Use Sealed Secrets. See **[Secret Management](docs/guides/secret-management.md)**.

## Local Git Hooks

We use **[pre-commit](https://pre-commit.com/)** to ensure code quality and consistency.

### Setup

1. Install `pre-commit` (requires Python/pip):

   ```bash
   pip install pre-commit
   ```

2. Install the git hooks:

   ```bash
   pre-commit install
   ```

Now, linting and formatting checks will run automatically on every commit.

### Manual Run

To run checks on all files manually:

```bash
pre-commit run --all-files
```

## Documentation

Documentation is a first-class citizen. If you add a feature, you must add documentation in `docs/`.

- **Guides**: For how-to procedures.
- **ADR**: For architectural decisions.

We look forward to your contributions!
