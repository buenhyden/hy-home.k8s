# Project Documentation

Welcome to the `hy-home.k8s` GitOps documentation.

## Quick Links

- **New to this project?** Start with [Getting Started](guides/getting-started.md)
- **Looking for specific info?** Check [Reference Documentation](reference/)
- **Understanding the system?** See [Architecture Overview](architecture/overview.md)

## Structure

### [Guides](guides/)

Step-by-step instructions and how-to articles.

- [Getting Started](guides/getting-started.md): Complete setup guide (15 minutes)
- [Credentials & Secrets](guides/credentials.md): Managing secrets and credentials
- [Troubleshooting](guides/troubleshooting.md): Common issues and solutions

### [Reference](reference/)

Technical reference documentation.

- [Directory Structure](reference/directory-structure.md): Complete folder layout
- [Infrastructure Tools](reference/infrastructure-tools.md): Tool versions and configurations
- [Application Templates](reference/application-templates.md): Available Helm starters

### [Architecture](architecture/)

System design and architecture documentation.

- [Overview](architecture/overview.md): High-level system architecture

### [Templates](templates/)

Templates for creating new documentation.

- [Service README Template](templates/service-readme.md): Standard service documentation format

## Contributing

When adding new documentation:

1. Choose the appropriate directory (guides/reference/architecture)
2. Use templates from the `templates/` directory
3. Add links to this index
4. Keep it concise and actionable

## External Resources

- [ArgoCD Documentation](https://argo-cd.readthedocs.io/)
- [Kustomize Documentation](https://kustomize.io/)
- [Istio Documentation](https://istio.io/latest/docs/)
