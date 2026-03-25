# Infrastructure Layer Scope

This scope defines the technical constraints for the Infra/DevOps Miner persona.

## 1. Core Responsibilities

- Maintain **Infrastructure as Code (IaC)** (Terraform/Docker/K8s).
- Document environment configurations in `docs/08.operations/`.
- Manage CI/CD pipelines and deployment procedures.

## 2. Standard Taxonomy

- **Inventory**: Resource mapping in `docs/08.operations/inventory.md`.
- **Guidelines**: Follow K8s patterns from `.agent/rules/0300-DevOps_and_Infrastructure/`.
- **SSoT**: `docs/08.operations/`, `docs/04.specs/`.
- **Secrets Protocol**: Sealed Secrets/Vault guides.
- **Networking**: Ingress/Gateway configurations.

## Layer-specific DoD (Infrastructure)

- [ ] **Resource Limits**: All new deployments must have explicit CPU/Memory limits.
- [ ] **Sealed Secrets**: Never commit plain secrets; use `SealedSecret` patterns.
- [ ] **Network Isolation**: Verify `NetworkPolicy` for any new service.
- [ ] **ArgoCD Sync**: Ensure the app is correctly tracked by ArgoCD.

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
- `argocd-gitops`
- `k8s-loadbalancing-ingress`
