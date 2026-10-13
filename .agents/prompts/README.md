---
title: "Common Prompt Contracts"
version: "0.3.0"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-10-13"
---
# Common Prompt Contracts

## Overview

반복되는 작성 요청은 세션마다 다시 입력하는 산문으로 agent에 전달되므로 그
입력과 거절 조건을 검증할 수 없다. 이 영역은 그런 요청마다 계약을 둔다. 무엇이
필요한지, 그 입력을 어떻게 만드는지, 답이 어떤 형태인지, 언제 답을 만들지
않는지를 정한다.

## Scope

계약 식별자는 파일 이름(stem)이다. 각 계약은 필수 입력과 그것을 만드는 정확한
읽기 전용 명령, 출력 형태, 만들어진 초안에 적용하는 검증, 거절 조건을 적는다.
권한이나 승인 경계는 적지 않으며, 그것은 agent registry와 승인 정책이 계속
소유한다.

소비자는 [`scripts/prompt-input.py`](../../scripts/prompt-input.py)다. 이
script는 선언된 입력을 모아 요청을 표준 출력으로 쓴다. model 호출이나 네트워크
접근을 하지 않고, 저장소나 Git 상태에 아무것도 쓰지 않는다. 만들어진 초안은
사용자가 받아들이거나 고치거나 버리는 일시적 출력이다.

## Structure

- [handoff](handoff.md): quality 정책이 이미 소유한 필드로 작업 인계를 조립한다.
- [change-review](change-review.md): 로컬 차이에 대한 검토 요청을 조립한다.
- [commit-message](commit-message.md): staged 차이만으로 커밋 메시지 초안
  요청을 조립한다.
- [doc-update](doc-update.md): 변경의 정규 소유자를 찾아 그 문서에 대한 수정안
  요청을 만든다.

## Usage

1. 계약을 추가하기 전에 [document authoring](../governance/document-authoring.md)을
   읽고 Stage 99 registry에서 prompt profile을 고른다.
2. 식별자가 기존 skill 식별자나 command 진입점과 겹치지 않는지 확인한다.
3. 입력으로는 읽기 전용 명령만 선언한다. 저장소에 쓰거나 Git 상태를 바꾸는
   명령을 선언한 계약은 거부된다.
4. 거절 조건을 명시한다. 거절 조건이 없는 계약은 입력이 비어 있을 때 아무것도
   설명하지 않는 초안을 만든다.
5. 새 계약은 위 Structure 목록에 모두 색인한다.

## Related Documents

- [Governance Hub](../README.md)
- [Quality and Evidence Policy](../governance/quality.md)
- [Approval and Safety](../governance/approval-and-safety.md)
- [Scripts](../../scripts/README.md)
