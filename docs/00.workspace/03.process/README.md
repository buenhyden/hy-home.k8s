---
title: "00.workspace/03.process"
version: "1.0.0"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-11-20"
---

# 00.workspace/03.process

## 문서 개요

### 목적과 독자

이 README는 docs/00.workspace/03.process에서 현재 소유 문서를 찾는 작성자와 검토자를 안내한다. 이 컬렉션의 목적은 [Purpose](#purpose)에 기록한다.

### 책임과 적용 범위

platform은 docs/00.workspace/03.process의 탐색 경로를 유지한다. 소유 파일은 [Paths](#paths), 진입 방법은 [Usage](#usage)에 연결하며 개별 문서의 계약은 해당 정본이 소유한다.

## 내용 계약

### 입력과 전제

입력과 전제는 아래 역할별 본문의 해당 절에 기록한다.

### 본문과 규칙

#### Responsibility

##### Purpose

> 개발·문서·전달의 의미와 순서를 소유하는 공통 절차 collection이다.

###### Inputs and Outputs

<a id="in-scope"></a>

**In Scope**

- SDLC, 문서 작성, 문서 수명주기, Git 공통 기준
- 저장소 전달 절차(main 릴리스 준비)

<a id="out-of-scope"></a>

**Out of Scope**

- 에이전트 전달 명령(`.agents/governance/git.md`)
- 제품 운영 Runbook

##### Excluded Responsibilities

에이전트의 실행 차이와 제품 운영 절차는 이 collection이 소유하지 않는다.

#### Current Contents

##### Paths

| Path | Purpose |
| --- | --- |
| [sdlc.md](./sdlc.md) | SDLC 단계, 변경 종류, 책임 계층(SDLC-R036) |
| [document-authoring.md](./document-authoring.md) | 문서 작성과 stage 라우팅 |
| [document-lifecycle.md](./document-lifecycle.md) | 문서 상태, 처분, 이동(DOCLIFE-R023) |
| [git.md](./git.md) | 커밋·브랜치·릴리스·Git 시점 공통 기준 |
| [`./0012-main-release-preparation-runbook.md`](./0012-main-release-preparation-runbook.md) | main CHANGELOG 준비와 SemVer Release 게시 절차 |

##### Owners

규칙 ID는 문서마다 한 owner를 가진다. GIT-R011~R013은 `.agents/governance/git.md`가 소유한다.

#### Usage

##### Entry Points

1. 규칙 변경은 해당 정책의 규칙 ID를 유지하고 Registry `policy_rule_ids` 기록과 함께 바꾼다.

###### Upstream and Downstream

- [Workspace README](../README.md)
- [Quality](../04.quality/README.md)

###### Policy and Templates

- [Rule form](../../99.templates/02.templates/93.common/rule.template.md)

##### Checks

정책 변경은 governance 문서 변경으로 선택되는 검사를 따른다.

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
