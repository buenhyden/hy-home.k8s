---
title: "00.workspace/02.architecture"
version: "1.0.0"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-11-20"
---

# 00.workspace/02.architecture

## 문서 개요

### 목적과 독자

이 README는 docs/00.workspace/02.architecture에서 현재 소유 문서를 찾는 작성자와 검토자를 안내한다. 이 컬렉션의 목적은 [Purpose](#purpose)에 기록한다.

### 책임과 적용 범위

platform은 docs/00.workspace/02.architecture의 탐색 경로를 유지한다. 소유 파일은 [Paths](#paths), 진입 방법은 [Usage](#usage)에 연결하며 개별 문서의 계약은 해당 정본이 소유한다.

## 내용 계약

### 입력과 전제

입력과 전제는 아래 역할별 본문의 해당 절에 기록한다.

### 본문과 규칙

#### Responsibility

##### Purpose

> 작업 시스템(문서·에이전트·QA·전달 체계) 자체의 구조와 결정을 보존하는 architecture 영역이다.

이 영역은 저장소에서 일하는 방식을 하나의 시스템으로 보고 그 구조(AD)와 지속 결정(ADR)을 둔다. 문서 Registry, 역할 Registry, QA Registry, 검사기, CI, Git·릴리스, 에이전트 거버넌스가 대상이다. 로컬 k8s GitOps 플랫폼이라는 제품의 구조와 결정은 [제품 architecture](../../02.architecture/README.md)가 소유한다.

###### Inputs and Outputs

<a id="in-scope"></a>

**In Scope**

- 작업 시스템의 문맥·구성·흐름·상태·신뢰·환경 관점(AD-0006)
- 문서 계약, 에이전트 거버넌스, QA·CI, Git·릴리스, 처분에 관한 ADR

<a id="out-of-scope"></a>

**Out of Scope**

- 클러스터·GitOps·네트워크·보안·관측 같은 제품 구조와 결정
- 실행 절차와 작업 증거

##### Excluded Responsibilities

제품 구조와 결정은 `docs/02.architecture/`, 구현 계약은 `docs/03.specs/`, 운영 절차는 `docs/05.operations/`가 소유한다.

#### Current Contents

##### Paths

| Path | Purpose |
| --- | --- |
| [01.descriptions/](./01.descriptions/) | 작업 시스템 Architecture Description |
| [02.decisions/](./02.decisions/) | 작업 시스템 ADR |

##### Owners

| 질문 | 위치 |
| --- | --- |
| 이 결정이 제품 동작을 바꾸는가 | 제품이면 `docs/02.architecture/02.decisions/` |
| 일하는 방식(문서·검사·전달·에이전트)을 바꾸는가 | 작업 시스템이면 [02.decisions/](./02.decisions/) |

#### Usage

##### Entry Points

1. 결정이 어느 시스템을 바꾸는지로 위치를 고른다. 두 영역을 모두 바꾸면 결정의 주된 대상에 두고 다른 쪽 AD에서 링크한다.
2. AD/ADR 형식과 상태는 제품 영역과 같은 profile(`sdlc/architecture-description`, `sdlc/architecture-decision`)을 쓴다.

###### Upstream and Downstream

- [Workspace README](../README.md)
- [Product architecture](../../02.architecture/README.md)

###### Policy and Templates

- [Architecture forms](../../99.templates/02.templates/02.architecture/)

##### Checks

ADR 번호는 두 영역이 하나의 순서를 공유하며 재사용하지 않는다. 처분은 문서 수명주기 정책을 따른다.

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
