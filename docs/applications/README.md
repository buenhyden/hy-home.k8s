# Application Layer

This directory contains documentation related to the applications deployed on the `hy-home.k8s` platform. The Application Layer is where business logic and services reside, distinct from the underlying infrastructure.

## Documentation

### 1. [Application Standards](./standards.md)

Rules and best practices for creating production-ready manifests, including labeling, resource quotas, and health checks.

### 2. [Examples & Templates](./examples.md)

A guide to the existing example applications and how to utilize the `_templates` directory to scaffold new services quickly.

## Structure

All applications are located in the `apps/` directory at the project root.

- `apps/_templates/`: Reusable Kustomize bases.
- `apps/_examples/`: Reference implementations.
- `apps/<tenant>/<app-name>`: Actual application deployments.
