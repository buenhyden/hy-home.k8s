---
title: "workspace-repo-support-previews"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-10-27"
---
# _workspace/repo-support/previews

> 렌더링한 manifest와 문서 미리보기를 두는 ignore된 staging 영역이다.

## Overview

`kustomize build`·`helm template`으로 렌더링한 manifest, 변경 전후 diff, 문서 렌더링 결과처럼 반영 전에 눈으로 확인할 산출물을 둔다.

이 README만 추적한다. 나머지 하위 항목은 ignore되며 Git에 force-add하지 않는다.

## Scope

### Permitted Artifacts

- `kustomize build <overlay>` / `helm template` 출력
- 변경 전후 렌더링 결과의 diff
- Mermaid·C4 다이어그램 렌더링 미리보기

모든 산출물은 비밀이 없어야 하고, 지워도 안전해야 한다.

### Forbidden Local State

- credential, 토큰, kubeconfig, 인증서, 개인 키
- 마스킹하지 않은 Secret 값이나 그 값이 들어 있는 manifest·로그
- shell history, provider cache, 개인 로컬 설정
- 다른 사람이 볼 수 없는 개인 진단 정보

## Structure

직접 하위 디렉터리는 없다. 이 README 외의 파일은 모두 ignore된 scratch이다.

## Usage

### Promotion and Cleanup

미리보기는 cluster에 적용하지 않는다. `kubectl apply`, `argocd app sync`, Helm upgrade는 별도 승인 범위다. 확인한 결과는 Task Evidence에 렌더링 명령과 입력 commit을 함께 기록한다.

옮길 곳이 없는 산출물은 작업을 닫기 전에 삭제한다.

### Tracking Rules

- 추적 대상은 `_workspace/repo-support/previews/README.md` 하나다.
- `scripts/validate-workspace-boundary.py`가 Git metadata만으로 이 경계를 검사한다.
  README가 추적되는지, 같은 위치의 `probe.log`가 ignore되는지 확인하며,
  ignore된 하위 항목은 열거나 읽지 않는다.

## Related Documents

- [상위 staging 경계](../README.md)
- [Approval Boundaries](../../../.agents/governance/approval-and-safety.md)
- [Workspace-staging 문서 양식 탐색](../../../docs/99.templates/README.md)
