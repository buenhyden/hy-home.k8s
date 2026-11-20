---
title: "00.workspace/02.architecture/01.descriptions"
version: "1.0.0"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-11-20"
---

# 00.workspace/02.architecture/01.descriptions

## 문서 개요

### 목적과 독자

이 README는 docs/00.workspace/02.architecture/01.descriptions에서 현재 소유 문서를 찾는 작성자와 검토자를 안내한다. 이 컬렉션의 목적은 [Purpose](#purpose)에 기록한다.

### 책임과 적용 범위

platform은 docs/00.workspace/02.architecture/01.descriptions의 탐색 경로를 유지한다. 소유 파일은 [Paths](#paths), 진입 방법은 [Usage](#usage)에 연결하며 개별 문서의 계약은 해당 정본이 소유한다.

## 내용 계약

### 입력과 전제

입력과 전제는 아래 역할별 본문의 해당 절에 기록한다.

### 본문과 규칙

#### Responsibility

##### Purpose

> 작업 시스템 Architecture Description collection이다.

AD-0006은 문서·역할·QA Registry, 도구, CI, 제공자 어댑터의 경계와 흐름, 상태와 신뢰 경계를 설명한다.

###### Inputs and Outputs

<a id="in-scope"></a>

**In Scope**

- 작업 시스템 AD

<a id="out-of-scope"></a>

**Out of Scope**

- 제품 AD(AD-0004, AD-0005, AD-0007)

##### Excluded Responsibilities

제품 AD는 `docs/02.architecture/01.descriptions/`가 소유한다.

#### Current Contents

##### Paths

| Path | Purpose |
| --- | --- |
| [`./0006-workspace-agent-governance-platform.md`](./0006-workspace-agent-governance-platform.md) | 작업 시스템(문서·에이전트·QA·전달) 구조와 신뢰 경계 |

##### Owners

이 collection은 분류 표를 따로 두지 않는다.

#### Usage

##### Entry Points

1. 새 AD는 `docs/99.templates/02.templates/02.architecture/description.template.md`에서 시작한다.

###### Upstream and Downstream

- [Workspace architecture](../README.md)
- [Workspace decisions](../02.decisions/README.md)

###### Policy and Templates

- [Description form](../../../99.templates/02.templates/02.architecture/description.template.md)

##### Checks

AD 번호는 제품 AD와 하나의 순서를 공유한다.

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
