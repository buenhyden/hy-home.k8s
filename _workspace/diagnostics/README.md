---
title: "workspace-diagnostics"
version: "1.0.0"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-11-20"
---
# _workspace/diagnostics

## 문서 개요

### 목적과 독자

이 README는 _workspace/diagnostics에 임시 지원 산출물을 두는 작업자에게 저장·정리 경계를 안내한다. 목적은 [Overview](#overview)에 기록한다.

### 책임과 적용 범위

platform은 _workspace/diagnostics의 staging 경계를 유지한다. 허용·금지 항목은 [Scope](#scope), 추적되는 하위 경로는 [Structure](#structure)에 기록한다.

## 내용 계약

### 입력과 전제

입력과 전제는 아래 역할별 본문의 해당 절에 기록한다.

### 본문과 규칙


> 저장소 QA·CI 진단 출력을 두는 ignore된 staging 영역이다.

#### Overview

로컬에서 재현한 CI 실패와 validator 진단처럼, 원인을 좁히는 동안만 필요한 출력을 모은다. 하위 경로는 출처에 따라 나뉜다.

이 README만 추적한다. 나머지 하위 항목은 ignore되며 Git에 force-add하지 않는다.

#### Scope

##### Permitted Artifacts

- `ci/`·`validation/` 하위에 두는 진단 출력

모든 산출물은 비밀이 없어야 하고, 지워도 안전해야 한다.

##### Forbidden Local State

- credential, 토큰, kubeconfig, 인증서, 개인 키
- 마스킹하지 않은 Secret 값이나 그 값이 들어 있는 manifest·로그
- shell history, provider cache, 개인 로컬 설정
- 다른 사람이 볼 수 없는 개인 진단 정보

#### Structure

| Path | Purpose |
| --- | --- |
| `ci/` | GitHub Actions job을 로컬에서 재현한 출력 |
| `validation/` | `scripts/qa.py`와 개별 validator의 진단 출력 |

두 경로에 자동으로 쓰는 producer는 없다. 작업자가 필요한 출력을 직접 리디렉션해 둔다.
`scripts/qa.py`는 자체 임시 디렉터리를 쓰고 이 경로에 쓰지 않는다.

#### Usage

##### Promotion and Cleanup

진단에서 확정한 원인과 증거는 해당 Task의 Evidence 표로 옮긴다. 원본 로그는 옮기지 않는다.

옮길 곳이 없는 산출물은 작업을 닫기 전에 삭제한다.

##### Tracking Rules

- 추적 대상은 `_workspace/diagnostics/README.md` 하나다.
- `scripts/validate-workspace-boundary.py`가 Git metadata만으로 이 경계를 검사한다.
  README가 추적되는지, 같은 위치의 `probe.log`가 ignore되는지 확인하며,
  ignore된 하위 항목은 열거나 읽지 않는다.

#### Related Documents

- [상위 staging 경계](../README.md)
- [Approval Boundaries](../../docs/00.workspace/04.quality/approval-and-safety.md)
- [Workspace-staging 문서 양식 탐색](../../docs/99.templates/README.md)

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
