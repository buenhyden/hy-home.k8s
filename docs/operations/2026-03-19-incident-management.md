---
title: 'Incident Management Standard'
status: 'Approved'
owner: 'buenhyden'
tags: ['standard', 'operation']
layer: 'ops'
---

# Incident Management

- **Status**: Active
- **Owner**: buenhyden
- **Last Reviewed**: 2026-03-19
- **layer:** ops

## 1. Definition of SEV

- **SEV-1**: Production baseline down. Permanent resource loss.
- **SEV-2**: Flow degraded. GitOps reconciliation failing.
- **SEV-3**: Minor/Non-impactful bugs.

## 2. Lifecycle

1. **Identification**: Alert triggers (RED metrics).
2. **Mitigation**: Execute relevant service-specific runbook in `docs/runbooks/`.
3. **Communication**: Update stakeholders (Human).
4. **Resolution**: Root cause identified and hotfix applied.

## Related Documents

- [Incident Response Runbook](../runbooks/2026-03-19-incident-response-runbook.md)
- [Postmortem Standard](./2026-03-19-postmortem-standard.md)
