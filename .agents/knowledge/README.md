---
title: "Common Knowledge"
version: "0.4.0"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-10-13"
---
# Common Knowledge

## Overview

이 영역은 방향을 잡는 질문에 답한다. 어느 트리가 무엇을 소유하는지, 어떤
도메인에서 무엇을 먼저 열어야 하는지를 알려 준다. 여기에는 포인터와 범위가
정해진 관측 metadata만 있다. 정책, 설계, 절차, 현재 상태에 대한 서술은 모두 각
행이 가리키는 소유자에게 남는다.

## Scope

knowledge 문서는 소유자 경로, 읽는 사람이 먼저 여는 진입 경로, 그 행이 유효한
조건을 적는다. 가리키는 본문의 어떤 구간도 다시 옮겨 적지 않고, 사람이 직접
작성하며, 생성기가 쓰지 않는다. 퇴역한 생성 색인은 여기서 다시 만들지 않는다.
이 영역을 두 번째 권한 원본이 아닌 지도로 유지하는 것은 중복 금지 규칙과 그
validator다.

범위 밖: 승인 경계, 권한, 역할 명단, gate 명령, lifecycle 상태, 근거 등급. 이들은
기존 소유자에게 남으며, 그중 하나를 다시 서술하는 행은 편의가 아니라 결함이다.

## Structure

- [Project Map](project-map.md): 최상위 트리별 소유 범위와 각각의 진입 문서.
- [Domain Index](domains.md): 운영 도메인별 정규 소유자, 진입 경로, 행이 유효한
  조건.

## Usage

1. 문서를 추가하기 전에 [document authoring](../governance/document-authoring.md)을
   읽고 Stage 99 registry에서 knowledge profile을 고른다.
2. 읽는 사람이 이 행 없이는 소유자를 찾아 헤매야 할 때만 행을 추가한다. 소유자의
   자체 색인이 이미 말하는 내용을 반복하는 행은 추가하지 않는다.
3. 소유자 경로와 진입 경로는 트리에 실제로 있는 그대로 적는다. 소유자나 진입
   경로가 없는 행은 검증에 실패한다.
4. 포인터의 유효 조건은 관측 가능한 변화로 적는다. 선택적 관측 metadata는
   source hash와 만료일을 갖춰 context-and-memory 정책을 따르며, 원문 서술을
   복제하거나 변경을 승인하지 않는다.
5. 새 knowledge 포인터 문서를 받아들이면 위 Structure 절에서 링크하고, 소유자
   세부는 이 라우터에 복사하지 말고 그 문서에 둔다.

## Related Documents

- [Governance Hub](../README.md)
- [Context and Memory](../governance/context-and-memory.md)
- [knowledge-map skill](../skills/knowledge-map/SKILL.md)
- [Repository documentation](../../docs/README.md)
