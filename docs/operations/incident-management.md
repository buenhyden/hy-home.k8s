---
layer: "ops"
---
# Incident Management Standard

## 1. Definition of SEV

- **SEV-1**: Production baseline down. Permanent resource loss.
- **SEV-2**: Flow degraded. GitOps reconciliation failing.
- **SEV-3**: Minor/Non-impactful bugs.

## 2. Lifecycle

1. **Identification**: Alert triggers (RED metrics).
2. **Mitigation**: Execute relevant service-specific runbook in `docs/runbooks/`.
3. **Communication**: Update stakeholders (Human).
4. **Resolution**: Root cause identified and hotfix applied.
5. **Postmortem**: Mandatory for SEV-1/2 within 24 hours.
