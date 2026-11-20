---
title: "00.workspace/04.quality"
version: "1.0.0"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-11-20"
---

# 00.workspace/04.quality

## 문서 개요

### 목적과 독자

이 README는 docs/00.workspace/04.quality에서 현재 소유 문서를 찾는 작성자와 검토자를 안내한다. 이 컬렉션의 목적은 [Purpose](#purpose)에 기록한다.

### 책임과 적용 범위

platform은 docs/00.workspace/04.quality의 탐색 경로를 유지한다. 소유 파일은 [Paths](#paths), 진입 방법은 [Usage](#usage)에 연결하며 개별 문서의 계약은 해당 정본이 소유한다.

## 내용 계약

### 입력과 전제

입력과 전제는 아래 역할별 본문의 해당 절에 기록한다.

### 본문과 규칙

#### Responsibility

##### Purpose

> 품질·형식·수용·검토와 보호 행위·승인 기준 collection이다.

###### Inputs and Outputs

<a id="in-scope"></a>

**In Scope**

- 품질과 완료 기준, 검토 등급과 재검토 조건
- 형식·lint 기준
- 보호 행위와 승인 의미(W 범위 SAFE 규칙)
- CI/CD QA 안내(GDE-0010)

<a id="out-of-scope"></a>

**Out of Scope**

- 에이전트의 실행 직전 확인·위임·권한 집행(`.agents/governance/approval-and-safety.md`)

##### Excluded Responsibilities

검사 구현은 `scripts/`와 `.github/workflows/`, 에이전트 실행 차이는 `.agents/governance/`가 소유한다.

#### Current Contents

##### Paths

| Path | Purpose |
| --- | --- |
| [quality.md](./quality.md) | 품질·검증·완료·인계 기준 |
| [formatting-and-linting.md](./formatting-and-linting.md) | 형식·lint 기준 |
| [approval-and-safety.md](./approval-and-safety.md) | 보호 행위와 승인(SAFE W 규칙) |
| [`./0010-ci-cd-qa-reference-guide.md`](./0010-ci-cd-qa-reference-guide.md) | 로컬·호스팅 QA 경계와 증적 해석 안내 |

##### Owners

SAFE-R011, R012, R017~R019는 `.agents/governance/approval-and-safety.md`가 소유한다.

#### Usage

##### Entry Points

1. 검사 의무는 quality 정책과 `scripts/validation/registry.json`이 소유하며 GDE-0010은 그 안내만 한다.

###### Upstream and Downstream

- [Workspace README](../README.md)
- [Process](../03.process/README.md)

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
