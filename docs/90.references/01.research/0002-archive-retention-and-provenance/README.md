---
title: "Archive Retention and Provenance Research Pack"
version: "1.0.0"
type: "reference/research-pack"
status: "in-review"
owner: "platform"
updated: "2026-11-20"
artifact_id: "RES-0002"
---

# Archive Retention and Provenance Research Pack

## 문서 개요

### 목적과 독자

이 연구 묶음은 Archive Retention and Provenance Research Pack의 조사 보고서를 찾고 출처 경계를 확인하는 조사자와 검토자를 위한 색인이다. 질문은 [Overview](#overview)에 기록한다.

### 책임과 적용 범위

platform은 이 묶음의 현재 범위를 유지한다. 포함 대상과 해석 한계는 [Scope](#scope), 보고서의 관계는 [Pack Contract](#pack-contract)에 기록한다.

## 내용 계약

### 입력과 전제

입력과 전제는 아래 역할별 본문의 해당 절에 기록한다.

### 본문과 규칙

#### Overview

이 pack은 ADR-0039와 ADR-0040이 다룬 Stage 98 보존·인용 문제의 외부 증거를
기록한다. 두 ADR은 tree를 떠났으며 Git history로 복구한다. 현재 Stage 98 결정은
[ADR-0053](../../../00.workspace/02.architecture/02.decisions/0053-unvalidated-archive.md)이 소유하며,
Stage 98은 검증 대상이 아니고 Git history가 유일한 복구 경로다.
Git이 객체에 이름을 붙이고 보관하는 방식, 대체된 결정과 incident 기록을 보관하는
방식, 공개 URL 이동을 알리는 방식, schema annotation이 검증과 어떻게 다른지가
여기에 해당한다. 날짜가 붙은 서술 증거이며 정책이 아니다.

#### Scope

이 pack은 아래 연구 계약과 보고서 색인에 명시한 주제와 출처를 포함한다.
실행 승인, 현재 정책, hosted·provider·live 결과는 증거 범위에서 제외한다.

#### Pack Contract

- **관찰 날짜**: 2026-09-15.
- **출처 종류**: Git, HTTP, JSON Schema, CommonMark, GitHub의 1차 문서, ADR
  원문 글, Google SRE postmortem 장, Diátaxis framework 사이트.
- **방법**: 각 출처는 관찰 날짜에 가져왔고 인용문을 확보한 주장만 기록한다.
  가져올 수 없었던 출처는 주장 없이 `unreachable`로 기록한다.
- **권한**: 현재 권한은 [common governance](../../../../.agents/README.md), Stage 99
  registry, 승인된 아키텍처 결정에 있다. 여기의 발견은 결정을 뒷받침하거나 그
  범위를 정할 뿐, 결정을 대신하지 않는다.

#### Structure

직접 멤버와 그 연구 책임은 아래 보고서 색인에서 찾는다. 각 멤버의 날짜와
판정은 멤버 본문이 소유하며 이 anchor는 별도 실행 상태를 기록하지 않는다.

#### Pack Index

| Reference | Role |
| --- | --- |
| [Git provenance and superseded record citation](m0001-git-provenance-and-superseded-record-citation.md) | 객체 이름, 도달 가능성, 대체된 기록의 관행, URL 이동, schema annotation, link 파싱 |

#### Usage

먼저 연구 계약과 증거 경계를 확인한 뒤 보고서 색인에서 필요한 멤버를 읽는다.
갱신은 아래 승계 절차를 따르며 연구 근거를 현재 실행 승인으로 사용하지 않는다.

#### Refresh and Succession

출처가 인용한 절을 바꾸거나, 그 주장에 기대는 결정이 개정되면 주장을 갱신한다.
새 발견은 이전 발견 옆에 날짜를 붙여 추가하며 기존 주장은 다시 쓰지 않는다.

#### Evidence Boundary

이 발견은 외부 문서다. 저장소 동작, hosted CI 결과, provider runtime, live
cluster 상태를 입증하지 않으며 여기서 인용했다고 해서 그 표준을 채택하거나
인증한 것도 아니다.

#### Related Documents

- [Research collection](../README.md)
- [ADR-0053](../../../00.workspace/02.architecture/02.decisions/0053-unvalidated-archive.md)
- ADR-0039, ADR-0040과 Spec 0082는 tree를 떠났으며 Git history가 복구한다. 예:
  `git show 69445fca:docs/02.architecture/decisions/0039-unit-archive-retention-and-citation-table.md`,
  `git show dcbbf84a^:docs/02.architecture/02.decisions/0040-archive-reappraisal-and-verifiable-sources.md`

## 적용과 확인

### 적용 방법

아래 역할별 본문에 기록된 사용 조건과 절차를 적용한다.

### 확인 기준

아래 역할별 본문의 검증·확인 조건과 그 한계에 따른다.

## 관계와 출처

### 관련 문서

관련 문서와 정본 링크는 아래 역할별 본문에서 확인한다.

### 외부 근거

외부 근거가 사용된 경우 아래 역할별 본문의 출처와 적용 범위에서 확인한다.
