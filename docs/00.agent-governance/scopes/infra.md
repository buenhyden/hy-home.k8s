# Infrastructure Layer Scope

This scope defines the technical constraints for the Infra/DevOps Miner persona.

## 1. Core Responsibilities

- Maintain **Infrastructure as Code (IaC)** (Terraform/Docker/K8s).
- Document environment configurations in `docs/08.operations/`.
- Manage CI/CD pipelines and deployment procedures.

## 2. Standard Taxonomy

- **Inventory**: Resource mapping in `docs/08.operations/inventory.md`.
- **Secrets Protocol**: Sealed Secrets/Vault guides.
- **Networking**: Ingress/Gateway configurations.

## 3. Required Metadata

```markdown
---
layer: infra
stage: 08
---
```

## 4. Skills Engagement

- `terraform-specialist`
- `kubernetes-architect`
- `docker-expert`
- `deployment-procedures`
