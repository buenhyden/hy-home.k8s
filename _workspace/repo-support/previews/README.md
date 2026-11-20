---
title: "workspace-repo-support-previews"
version: "1.0.0"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-11-20"
---
# _workspace/repo-support/previews

## 문서 개요

### 목적과 독자

이 README는 _workspace/repo-support/previews에 임시 지원 산출물을 두는 작업자에게 저장·정리 경계를 안내한다. 목적은 [Overview](#overview)에 기록한다.

### 책임과 적용 범위

platform은 _workspace/repo-support/previews의 staging 경계를 유지한다. 허용·금지 항목은 [Scope](#scope), 추적되는 하위 경로는 [Structure](#structure)에 기록한다.

## 내용 계약

### 입력과 전제

입력과 전제는 아래 역할별 본문의 해당 절에 기록한다.

### 본문과 규칙


> 렌더링한 manifest와 문서 미리보기를 두는 ignore된 staging 영역이다.

#### Overview

`kustomize build`·`helm template`으로 렌더링한 manifest, 변경 전후 diff, 문서 렌더링 결과처럼 반영 전에 눈으로 확인할 산출물을 둔다.

이 README만 추적한다. 나머지 하위 항목은 ignore되며 Git에 force-add하지 않는다.

#### Scope

##### Permitted Artifacts

- `kustomize build <overlay>` / `helm template` 출력
- 변경 전후 렌더링 결과의 diff
- Mermaid·C4 다이어그램 렌더링 미리보기

모든 산출물은 비밀이 없어야 하고, 지워도 안전해야 한다.

##### Forbidden Local State

- credential, 토큰, kubeconfig, 인증서, 개인 키
- 마스킹하지 않은 Secret 값이나 그 값이 들어 있는 manifest·로그
- shell history, provider cache, 개인 로컬 설정
- 다른 사람이 볼 수 없는 개인 진단 정보

#### Structure

직접 하위 디렉터리는 없다. 이 README 외의 파일은 모두 ignore된 scratch이다.

#### Usage

##### Promotion and Cleanup

미리보기는 cluster에 적용하지 않는다. `kubectl apply`, `argocd app sync`, Helm upgrade는 별도 승인 범위다. 확인한 결과는 Task Evidence에 렌더링 명령과 입력 commit을 함께 기록한다.

옮길 곳이 없는 산출물은 작업을 닫기 전에 삭제한다.

##### Tracking Rules

- 추적 대상은 `_workspace/repo-support/previews/README.md` 하나다.
- `scripts/validate-workspace-boundary.py`가 Git metadata만으로 이 경계를 검사한다.
  README가 추적되는지, 같은 위치의 `probe.log`가 ignore되는지 확인하며,
  ignore된 하위 항목은 열거나 읽지 않는다.

#### Related Documents

- [상위 staging 경계](../README.md)
- [Approval Boundaries](../../../docs/00.workspace/04.quality/approval-and-safety.md)
- [Workspace-staging 문서 양식 탐색](../../../docs/99.templates/README.md)

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
