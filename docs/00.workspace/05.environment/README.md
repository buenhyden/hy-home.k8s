---
title: "00.workspace/05.environment"
version: "1.0.0"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-11-20"
---

# 00.workspace/05.environment

## 문서 개요

### 목적과 독자

이 README는 docs/00.workspace/05.environment에서 현재 소유 문서를 찾는 작성자와 검토자를 안내한다. 이 컬렉션의 목적은 [Purpose](#purpose)에 기록한다.

### 책임과 적용 범위

platform은 docs/00.workspace/05.environment의 탐색 경로를 유지한다. 소유 파일은 [Paths](#paths), 진입 방법은 [Usage](#usage)에 연결하며 개별 문서의 계약은 해당 정본이 소유한다.

## 내용 계약

### 입력과 전제

입력과 전제는 아래 역할별 본문의 해당 절에 기록한다.

### 본문과 규칙

#### Responsibility

##### Purpose

이 collection은 로컬 작업과 검증에 필요한 재현 가능한 환경 준비를 안내한다.
검증 의무와 결과 판정은 [Quality Policy](../04.quality/quality.md)가 소유한다.

###### Inputs and Outputs

검토된 [Python 의존성 lock](../../../.github/requirements/ci-validation.txt)과
현재 checkout을 입력으로 삼아, checkout 밖의 계정 소유 검증 환경을 준비하는
가이드를 제공한다. 환경 준비 결과는 실제 선택된 interpreter와 도구 identity로
확인한다.

##### Excluded Responsibilities

Git hook 연결·실패 조건은 [Git Policy](../03.process/git.md), QA 명령과
구현은 [scripts README](../../../scripts/README.md), native provider의
권한·sandbox 설정은 `.claude/`와 `.codex/`가 소유한다. 이 collection은
비밀 값, live cluster 접근, 전역 설정의 현재 값을 기록하지 않는다.

#### Current Contents

##### Paths

| Path | Purpose |
| --- | --- |
| [0011-local-validation-environment.md](./0011-local-validation-environment.md) | 로컬 검증 venv의 준비·identity 확인·lock 갱신 안내 |
| [0012-independent-review-environment.md](./0012-independent-review-environment.md) | Codex·Claude 독립 검토의 실제 읽기 전용 경로 준비·권한 확인 안내 |

##### Owners

현재 하위 문서는 로컬 검증과 독립 검토 환경 가이드다. lock은 `.github/requirements/`에,
실행 계약은 `scripts/`에 남으며 이 README는 두 원본의 내용을 복제하지 않는다.

#### Usage

##### Entry Points

로컬 검증 환경을 새로 만들거나 lock이 바뀌었으면
[GDE-0011](./0011-local-validation-environment.md)에서 시작한다. 새 guide는
[Stage 99 Guide form](../../99.templates/02.templates/05.operations/guide.template.md)을
따라 이 collection에 번호가 붙은 파일로 추가한다.

독립 검토의 실제 권한 경로는 [GDE-0012](./0012-independent-review-environment.md)에서
준비하고 확인한다.

###### Upstream and Downstream

- [Workspace README](../README.md)
- [Quality collection](../04.quality/README.md)
- [Git process collection](../03.process/README.md)

###### Policy and Templates

- [Document Authoring Policy](../03.process/document-authoring.md)
- [Guide form](../../99.templates/02.templates/05.operations/guide.template.md)

##### Checks

문서 형식·링크·상태는 [Document Authoring Policy](../03.process/document-authoring.md)와
[Document Lifecycle Policy](../03.process/document-lifecycle.md)의 선택된 검사를 따른다.
환경이 실제로 설치되거나 hook이 실행되었는지는 문서 검사만으로 증명하지 않는다.

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
