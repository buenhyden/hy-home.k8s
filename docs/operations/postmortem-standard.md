# Postmortem Standard

- **Status**: Approved
- **layer:** ops

**Overview (KR):** 장애 복구 후 재발 방지와 지식 공유를 위해 작성하는 포스트모텀(사후 분석 리포트)의 작성 기준 및 결과 검토 프로세스를 정의합니다.

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

- [docs/operations/incident-management.md](./incident-management.md)
- [docs/runbooks/deployment-runbook.md](../runbooks/deployment-runbook.md)
