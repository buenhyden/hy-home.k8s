---
title: "00.workspace/05.environment"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-11-20"
---

# 00.workspace/05.environment

## Responsibility

### Purpose

이 collection은 로컬 작업과 검증에 필요한 재현 가능한 환경 준비를 안내한다.
검증 의무와 결과 판정은 [Quality Policy](../04.quality/quality.md)가 소유한다.

#### Inputs and Outputs

검토된 [Python 의존성 lock](../../../.github/requirements/ci-validation.txt)과
현재 checkout을 입력으로 삼아, checkout 밖의 계정 소유 검증 환경을 준비하는
가이드를 제공한다. 환경 준비 결과는 실제 선택된 interpreter와 도구 identity로
확인한다.

### Excluded Responsibilities

Git hook 연결·실패 조건은 [Git Policy](../03.process/git.md), QA 명령과
구현은 [scripts README](../../../scripts/README.md), native provider의
권한·sandbox 설정은 `.claude/`와 `.codex/`가 소유한다. 이 collection은
비밀 값, live cluster 접근, 전역 설정의 현재 값을 기록하지 않는다.

## Current Contents

### Paths

| Path | Purpose |
| --- | --- |
| [0011-local-validation-environment.md](./0011-local-validation-environment.md) | 로컬 검증 venv의 준비·identity 확인·lock 갱신 안내 |

### Owners

현재 하위 문서는 환경 준비 가이드 한 개다. lock은 `.github/requirements/`에,
실행 계약은 `scripts/`에 남으며 이 README는 두 원본의 내용을 복제하지 않는다.

## Usage

### Entry Points

로컬 검증 환경을 새로 만들거나 lock이 바뀌었으면
[GDE-0011](./0011-local-validation-environment.md)에서 시작한다. 새 guide는
[Stage 99 Guide form](../../99.templates/02.templates/05.operations/guide.template.md)을
따라 이 collection에 번호가 붙은 파일로 추가한다.

#### Upstream and Downstream

- [Workspace README](../README.md)
- [Quality collection](../04.quality/README.md)
- [Git process collection](../03.process/README.md)

#### Policy and Templates

- [Document Authoring Policy](../03.process/document-authoring.md)
- [Guide form](../../99.templates/02.templates/05.operations/guide.template.md)

### Checks

문서 형식·링크·상태는 [Document Authoring Policy](../03.process/document-authoring.md)와
[Document Lifecycle Policy](../03.process/document-lifecycle.md)의 선택된 검사를 따른다.
환경이 실제로 설치되거나 hook이 실행되었는지는 문서 검사만으로 증명하지 않는다.
