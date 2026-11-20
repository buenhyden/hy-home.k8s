---
title: "provider-native Template Definition"
version: "0.1.0"
type: "common/template-exception-provider-native-command"
status: "draft"
owner: "platform"
updated: "2026-11-20"
---

# provider-native Template Definition

## 문서 개요

### 목적과 독자

<!-- 작성 규칙: Give authors one native form for a Claude command projection: a provider-native file whose body has no headings. -->

### 책임과 적용 범위

<!-- 작성 규칙: The projection consumes the native values the provider bindings own and restates no shared policy. -->

## 내용 계약

### 입력과 전제

<!-- 작성 규칙: 이 문서를 작성할 때 필요한 실제 입력, 권한과 전제를 밝힌다. -->

### 본문과 규칙

<!-- 작성 규칙: 아래 역할별 절의 내용과 표를 해당 문서의 실제 사실로 채운다. -->

~~~~~~~native-payload
---
description: "One sentence naming the prompt contract this entry point assembles."
argument-hint: "__OPTIONAL_ARGUMENT_HINT__"
allowed-tools: "__BOUNDED_BUILDER_INVOCATION__"
---

Run `python3 scripts/prompt-input.py __CONTRACT_IDENTIFIER__` from the repository
root and use its output as the request. The builder reads only the inputs
`.agents/prompts/__CONTRACT_IDENTIFIER__.md` declares, makes no model call, and
writes nothing to the repository or to Git state. When it exits non-zero, report
its diagnostic instead of producing a draft.
~~~~~~~

## 적용과 확인

### 적용 방법

<!-- 작성 규칙: 실제 사용 방법과 적용 대상을 설명한다. -->

### 확인 기준

<!-- 작성 규칙: 이 문서 유형에 해당하는 확인 방법과 한계를 적는다. -->

## 관계와 출처

### 관련 문서

<!-- 작성 규칙: 현재 정본의 관계와 탐색 링크만 연결한다. 실제 의미 관계가 있으면 Relation에 requires/designs/implements/verifies/operates/defines/cites 중 하나를, Target에 현재 문서의 상대 Markdown 링크 하나를 적는다. 단순 탐색 링크는 표 밖에 둔다. -->

| Relation | Target |
| --- | --- |

### 외부 근거

<!-- 작성 규칙: 외부 근거가 있으면 출처와 채택 범위를 적고, 없으면 그 이유를 명시한다. -->
