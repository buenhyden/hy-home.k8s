# Claude Developer Guide

Guidelines for interacting with Claude in the context of `hy-home.k8s`.

## Project Context

- **Name**: hy-home.k8s
- **Platform**: GitOps-based Kubernetes Infrastructure
- **Core Tools**: Kind, ArgoCD, Istio, Prometheus, Grafana, PostgreSQL, Redis

## Instructions for Claude

- **GitOps Focus**: When proposing changes, ensure they align with the GitOps model (ArgoCD based synchronization).
- **Manifest Standards**: Recommend and follow the standard Kubernetes manifest structure used in the project.
- **Local Dev**: Prioritize solutions that work with the local Kind environment defined in `bootstrap/`.
- **Infrastructure First**: Changes to applications (`apps/`) must consider the underlying infrastructure requirements in `infrastructure/`.
- **Security Check**: Flag any potential security issues, especially related to secrets management (Sealed Secrets).
