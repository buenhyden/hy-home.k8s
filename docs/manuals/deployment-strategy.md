---
layer: "ops"
---
# Deployment Strategy

## 1. Environment Hierarchy

- **Development (Dev)**: Used for intra-team testing. Automatically deployed upon PR merge to `main`.
- **Staging**: Used for pre-production validation (QA, Load testing, User Acceptance). Matches production infrastructure parity exactly.
- **Production**: Live environment for end-users.

## 2. Deployment Strategy

- **Default Strategy**: Blue-Green Deployment (or Rolling Update for stateless worker tiers). Zero-downtime required.
- **Infrastructure Mutability**: Manual "ClickOps" in production is strictly **FORBIDDEN**. All changes must execute via Infrastructure-as-Code (Terraform/ArgoCD).
