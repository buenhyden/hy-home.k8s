---
title: 'Postmortem Standard'
status: 'Approved'
owner: 'buenhyden'
tags: ['standard', 'operation']
layer: 'ops'
lastReviewed: '2026-03-19'
---

# Postmortem Standard

- **Status**: Active
- **Owner**: buenhyden
- **Last Reviewed**: 2026-03-19
- **layer:** ops

**Overview (KR):** 장애 사후 분석을 위한 표준 절차와 템플릿 사용법을 정의합니다.

## 1. Purpose

To learn from failures without blame and prevent recurrence.

## 2. Requirement

Mandatory for all SEV-1 and SEV-2 incidents.

## 3. Template Usage

All postmortems MUST use `templates/postmortem-template.md` and be stored in `docs/operations/postmortems/`.

## 4. Review Process

1. Drafted by the **DevOps Agent** or incident responder.
2. Reviewed by the **Architect Agent** for systemic improvements.

## Related Documents

- [Incident Management](./2026-03-19-incident-management.md)
- [Deployment Runbook](../runbooks/2026-02-27-deployment-runbook.md)
