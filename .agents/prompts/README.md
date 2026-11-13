---
title: "Common Prompt Contracts"
version: "0.4.1"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-11-13"
---

# Common Prompt Contracts

## Stage Responsibility

### Purpose and Readers

반복되는 작성 요청은 세션마다 다시 입력하는 산문으로 agent에 전달되므로 그
입력과 거절 조건을 검증할 수 없다. 이 영역은 그런 요청마다 계약을 둔다. 무엇이
필요한지, 그 입력을 어떻게 만드는지, 답이 어떤 형태인지, 언제 답을 만들지
않는지를 정한다.

### Inputs and Outputs

계약 식별자는 파일 이름(stem)이다. 각 계약은 필수 입력과 그것을 만드는 정확한
명령(`scripts/prompt-input.py`의 닫힌 `ALLOWED_COMMANDS` 목록에 있는 것), 출력 형태, 만들어진 초안에 적용하는 검증, 거절 조건을 적는다.
권한이나 승인 경계는 적지 않으며, 그것은 agent registry와 승인 정책이 계속
소유한다.

소비자는 [`scripts/prompt-input.py`](../../scripts/prompt-input.py)다. 이
script는 선언된 입력을 모아 요청을 표준 출력으로 쓴다. model 호출이나 네트워크
접근을 하지 않고, 저장소나 Git 상태에 아무것도 쓰지 않는다. 만들어진 초안은
사용자가 받아들이거나 고치거나 버리는 일시적 출력이다.

## Contents

### Current Items

#### Item Index

| Path | Purpose |
| --- | --- |
| [handoff](handoff.md) | quality 정책이 이미 소유한 필드로 작업 인계를 조립한다. |
| [change-review](change-review.md) | 로컬 차이에 대한 검토 요청을 조립한다. |
| [commit-message](commit-message.md) | staged 차이만으로 커밋 메시지 초안 요청을 조립한다. |
| [doc-update](doc-update.md) | 변경의 정규 소유자를 찾아 그 문서에 대한 수정안 요청을 만든다. |

### Classification

이 README는 분류 표를 따로 두지 않는다. 분류 표를 두게 되면 여기에 둔다.

## Workflow

### Create and Review

#### Add and Find

1. 계약을 추가하기 전에 [document authoring](../governance/document-authoring.md)을
   읽고 Stage 99 registry에서 prompt profile을 고른다.
2. 식별자가 기존 skill 식별자나 command 진입점과 겹치지 않는지 확인한다.
3. 입력 명령은 `scripts/prompt-input.py`의 닫힌 `ALLOWED_COMMANDS` 목록에 있는
   것만 선언한다. 목록에 없는 명령을 선언한 계약은 거부되며, 명령을 목록에
   더하는 것은 검토를 거치는 script 변경이다.
4. 거절 조건을 명시한다. builder는 주제 입력이 비어 있는 경우만 거부하고 나머지
   조건은 요청하는 agent가 지킨다. 거절 조건이 없는 계약은 입력이 비어 있을 때 아무것도
   설명하지 않는 초안을 만든다.
5. 새 계약은 위 Item Index 표에 모두 색인하고, 같은 식별자로
   `.claude/commands/<id>.md` 진입점을 하나 둔다([Claude adapter](../../.claude/README.md)).
   진입점은 자체 계약을 갖지 않는다.

### Transition and Exit

이 README는 상태, 승격, 종료 규칙을 따로 두지 않는다. 그런 규칙을 두게 되면 여기에 적는다.

## Related Documents

### Upstream and Downstream

- [Common Agent Governance](../README.md)
- [Scripts](../../scripts/README.md)

### Policy and Templates

- [Quality and Evidence Policy](../governance/quality.md)
- [Approval and Safety](../governance/approval-and-safety.md)
