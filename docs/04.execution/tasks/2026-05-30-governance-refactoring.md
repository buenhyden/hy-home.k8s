---
title: 'Governance Refactoring Task'
type: task
status: superseded
owner: 'platform'
updated: 2026-06-01
---


# Governance Refactoring Task

---

## Overview (KR)

[2026-05-30-common-agent-governance-refactoring.md](../plans/2026-05-30-common-agent-governance-refactoring.md) 계획에 따른 실제 실행 추적.

## Inputs

- **Parent Spec**: N/A. Historical governance refactoring slice.
- **Parent Plan**: [../plans/2026-05-30-common-agent-governance-refactoring.md](../plans/2026-05-30-common-agent-governance-refactoring.md)

## Context

Stage 00 기반 거버넌스의 파편화를 방지하고, 템플릿 계약 준수를 위함.

2026-06-01 update: this task is superseded by
[2026-06-01-stage-00-canonical-adapter-redesign.md](./2026-06-01-stage-00-canonical-adapter-redesign.md).
The remaining work is tracked there with task-level validation evidence. This
document remains as historical context for the original 2026-05-30 slice.

## Objective

1. 템플릿 매핑 복구 (`policy.template.md` 신설)
2. ARD 파일명 일괄 변경 (`YYYY-MM-DD` -> `0001-`)
3. 모델 정책 갱신 (Legacy 분리 및 공식 모델 지정)
4. 플랫폼 하네스 중복 텍스트 제거

## Task Table

- `[ ]` TSK-001: `policy.template.md`를 `policy.template.md`로 이름 변경 및 템플릿 내부 내용 수정.
- `[ ]` TSK-002: `docs/99.templates/README.md`에서 매핑 갱신.
- `[ ]` TSK-003: `docs/02.architecture/requirements/` 내부의 파일들을 `0001-` 형식으로 리네임.
- `[ ]` TSK-004: ARD 리네임에 따른 기존 링크(`docs/01.requirements/` 등) 업데이트.
- `[ ]` TSK-005: `docs/00.agent-governance/model-policy.md` 내용 수정.
- `[ ]` TSK-006: `.agents/GEMINI.md`, `.claude/CLAUDE.md`, `.codex/CODEX.md` 텍스트 슬림화/어댑터화.

## Suggested Types

- `doc`
- `guardrail`
- `test`

## Working Rules

- Historical evidence is preserved here.
- Current execution continues in the superseding 2026-06-01 canonical adapter task.
- Do not use this task as the active implementation contract.

## Verification Summary

| TSK | Code / Output | Notes |
| --- | ------------- | ----- |
|     |               |       |

## Related Documents

- **Plan**: [../plans/2026-05-30-common-agent-governance-refactoring.md](../plans/2026-05-30-common-agent-governance-refactoring.md)
- **Superseding Task**: [./2026-06-01-stage-00-canonical-adapter-redesign.md](./2026-06-01-stage-00-canonical-adapter-redesign.md)
