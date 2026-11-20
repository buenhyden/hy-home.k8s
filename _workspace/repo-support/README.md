---
title: "workspace-repo-support"
version: "1.0.0"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-11-20"
---
# _workspace/repo-support

## 문서 개요

### 목적과 독자

이 README는 _workspace/repo-support에 임시 지원 산출물을 두는 작업자에게 저장·정리 경계를 안내한다. 목적은 [Overview](#overview)에 기록한다.

### 책임과 적용 범위

platform은 _workspace/repo-support의 staging 경계를 유지한다. 허용·금지 항목은 [Scope](#scope), 추적되는 하위 경로는 [Structure](#structure)에 기록한다.

## 내용 계약

### 입력과 전제

입력과 전제는 아래 역할별 본문의 해당 절에 기록한다.

### 본문과 규칙


> 감사·분석·미리보기 같은 저장소 지원 작업의 산출물을 두는 ignore된 staging 영역이다.

#### Overview

코드나 문서를 바꾸기 전에 만드는 분석 자료와, 바꾼 결과를 확인하는 미리보기를 둔다.

이 README만 추적한다. 나머지 하위 항목은 ignore되며 Git에 force-add하지 않는다.

#### Scope

##### Permitted Artifacts

- `analysis/`·`previews/` 하위에 두는 지원 산출물

모든 산출물은 비밀이 없어야 하고, 지워도 안전해야 한다.

##### Forbidden Local State

- credential, 토큰, kubeconfig, 인증서, 개인 키
- 마스킹하지 않은 Secret 값이나 그 값이 들어 있는 manifest·로그
- shell history, provider cache, 개인 로컬 설정
- 다른 사람이 볼 수 없는 개인 진단 정보

#### Structure

| Path | Purpose |
| --- | --- |
| `analysis/` | 감사, 인벤토리, dry-run 분석 자료 |
| `previews/` | 렌더링한 manifest와 문서 미리보기 |

#### Usage

##### Promotion and Cleanup

분석에서 나온 결정은 해당 Spec·Plan·Task로, 오래 둘 참고 자료는 Stage 90으로 옮긴다.

옮길 곳이 없는 산출물은 작업을 닫기 전에 삭제한다.

##### Tracking Rules

- 추적 대상은 `_workspace/repo-support/README.md` 하나다.
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
