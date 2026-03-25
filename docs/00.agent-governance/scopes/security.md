# Security Layer Scope

This scope defines the security constraints for the Security Officer persona.

## 1. Core Responsibilities

- **Guidelines**: Follow OWASP patterns from `.agent/rules/2200-Security/`.
- **SSoT**: `docs/04.specs/`, `docs/10.incidents/`.

## Layer-specific DoD (Security)

- [ ] **Threat Model**: Update the threat model if new attack surfaces are introduced.
- [ ] **Secret Audit**: Verify no secrets are exposed in code or logs.
- [ ] **Sealed Secrets**: All Kubernetes secrets must be encrypted as `SealedSecret` artifacts.
- [ ] **Vulnerability Scan**: Run `vulnerability-scanner` on the changes.
- [ ] **Compliance**: Ensure alignment with project security policies (e.g., RBAC).
- Ensure compliance with OWASP Top 10.

## 2. Standard Taxonomy

- **Threat Model**: STRIDE analysis in `docs/04.specs/security.md`.
- **Audit Reports**: Security scan results.
- **Incidents**: Active security tracking.

## 3. Required Metadata

```markdown
---
layer: security
stage: [04|10]
---
```

## 4. Skills Engagement

- `security-audit`
- `threat-modeling-expert`
- `vulnerability-scanner`
- `k8s-sealed-secrets`
