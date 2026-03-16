---
title: 'Incident Management Standard'
status: 'Approved'
owner: 'buenhyden'
tags: ['standard', 'operation']
layer: 'ops'
---

# Incident Management Standard

- **Status**: Approved
- **Owner**: buenhyden
- **layer:** ops

**Overview (KR):** 인프라 및 서비스 장애의 심각도를 정의하고, 발생부터 복구까지의 전체 장애 대응 라이프사이클을 관리하는 표준 가이드입니다.

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

- [docs/runbooks/incident-response-runbook.md](../runbooks/incident-response-runbook.md)
- [docs/operations/postmortem-standard.md](./postmortem-standard.md)
