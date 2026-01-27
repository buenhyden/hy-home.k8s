# Project Lifecycle

This directory documents the lifecycle management of the `hy-home.k8s` platform, from initial creation to ongoing maintenance and upgrades.

## Topics

### 1. [Bootstrap Process](./bootstrap-process.md)

A detailed breakdown of how the cluster is initialized from zero to full GitOps state. Explains the scripts found in the `bootstrap/` directory.

### 2. [Maintenance & Upgrades](./maintenance.md)

Procedures for:

- Upgrading Kubernetes (Kind image versions).
- Upgrading ArgoCD.
- Rotating Security Keys.
- Periodic cleanup tasks.
