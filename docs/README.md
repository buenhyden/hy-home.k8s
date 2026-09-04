---
title: "docs: 프로젝트 문서 허브"
version: "0.1.0"
type: "common/readme-stage-index"
status: "active"
owner: "platform"
updated: "2026-09-04"
---
# docs: 프로젝트 문서 허브

## Overview

요구사항, 구조적 결정, 변경 계약, 실행 증거와 운영 지식을 연결하는
`hy-home.k8s` 문서 진입점이다. 각 문서는 한 가지 목적의 정본을 가지며
README는 탐색을 돕고 별도의 정책·상태 목록을 만들지 않는다.

## Stage Contract

- Stage 00: AI Agent 거버넌스, 정책, 규칙, 역할, skill, Codex/Claude 차이와
  실행 절차.
- Stage 01: 구현 독립적인 Requirement Package.
- Stage 02: 현재 구조를 설명하는 Architecture Description과 중요한 선택을
  기록하는 ADR.
- Stage 03: 변경별 Spec, Plan, 개별 Task와 실행 가능한 interface 계약.
- Stage 05: Guide, Operations Policy, Runbook, Incident와 Postmortem.
- Stage 90: 워크스페이스 Audit, 외부 Research, Data와 기타 참고 자료. 다른
  stage의 규칙이나 실행 권한을 덮어쓰지 않는다.
- Stage 98: SDLC·운영·reference에서 퇴역한 자료를 독립적으로 정리하는
  historical archive. 활성 stage의 문서가 이 stage의 문서·파일을 인용하거나
  cross-link하지 않는다.
- Stage 99: docs에서 사용하는 문서 profile, 경로, ID, lifecycle, schema와
  복사 가능한 template.

Stage 04는 사용하지 않는다. 모든 변경이 모든 stage의 새 문서를 요구하지는
않지만, 필요한 요구·결정·수용 기준·실행 증거는 서로 추적 가능해야 한다.

## Document Index

| 영역 | 정본과 탐색 |
| --- | --- |
| [00.agent-governance](00.agent-governance/README.md) | 정책·책임·공급자·절차와 SDLC 흐름 |
| [01.requirements](01.requirements/README.md) | 하나의 Package에 기능·비기능·interface 요구와 acceptance 통합 |
| [02.architecture](02.architecture/README.md) | descriptions와 decisions |
| [03.specs](03.specs/README.md) | 패키지 README, spec.md, plan.md, tasks/tsk-####-slug.md |
| [05.operations](05.operations/README.md) | 운영 설명·통제·절차·사고 기록 |
| [90.references](90.references/README.md) | 출처와 시점이 명확한 Audit·Research·Data 참고 근거 |
| [98.archive](98.archive/README.md) | 활성 문서와 분리된 historical archive |
| [99.templates](99.templates/README.md) | 유일한 문서 registry와 복사 가능한 template |

`.agents/registry.json`은 문서 registry와 별개로 역할 ID, 권한, handoff,
skill과 provider projection을 소유한다. 루트 `DESIGN.md`는 UI와
design-system 전용 정본이다.

## Authoring Workflow

1. [SDLC 흐름](00.agent-governance/sdlc.md)으로 목적과 소유 stage를 정한다.
2. [Stage 99 안내](99.templates/README.md)와 registry에서 최종 경로의
   profile을 하나로 선택하고 해당 template을 읽는다.
3. profile이 정한 초기 상태·ID·section·relationship을 사용한다. 모든
   문서를 draft로 시작하거나 동일한 heading을 강요하지 않는다.
4. Requirement Package는 장기적 요구를, AD/ADR은 구조와 결정을, Spec은
   변경의 Technical Approach·Acceptance Contract·실패 조건을 소유한다.
   구현 순서·위험·검증·rollback은 Plan, 작업 결과는 개별 Task에 둔다.
5. 경로 또는 내용 변경 시 해당 README와 현재 cross-link를 함께 점검한다.
   ID는 재사용하지 않고 다른 문서에서는 전체 ID로 추적한다.
6. superseded ADR은 decision log에 남긴다. 완료·봉인된 본문을 새 형식에
   맞추려고 다시 쓰지 않는다. 폐기 문서의 본문은 Git history에서 복구하며,
   활성 Stage 00/01/02/03/05/90 문서에는 Archive 문서·파일의 인용이나
   cross-link, 본문 복제본 또는 redirect를 만들지 않는다.
7. [문서 작성 정책](00.agent-governance/policies/document-authoring.md)과
   [품질·증거 정책](00.agent-governance/policies/quality.md)에 따라 검증하고
   현재 Task에 결과·제한·다음 담당자를 기록한다.

정적 검증은 live cluster 변경 승인이나 실제 provider 실행 증거가 아니다.

### 문서 역할과 언어 계약

사람이 읽는 안내와 요약은 한국어를 우선하고, AI Agent가 실행 기준으로 삼는
정책·프롬프트·도구·검증 계약은 영어를 우선한다. 한 문서가 두 독자를 함께
상대하면 사람용 맥락은 한국어로, `AI Agent Requirements` 같은 에이전트용
요구사항 섹션은 영어로 작성한다.

실행 계약에 가까운 문서는 영어를 기본값으로 둔다. Stage 00, `spec.md`,
`plan.md`, 개별 Task는 계획·검증·handoff 증적이므로 영어로 작성한다. README와
운영 안내처럼 사람이 먼저 읽는 문서는 한국어로 두되, 그 안에 들어가는 AI Agent
실행 지시나 도구 계약은 영어로 분리한다.

## Related Documents

- [Root README](../README.md)
- [Governance Hub](00.agent-governance/README.md)
- [Document Lifecycle](00.agent-governance/policies/document-lifecycle.md)
- [Templates](99.templates/README.md)
- [Archive](98.archive/README.md)
- [Scripts](../scripts/README.md)
