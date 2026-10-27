---
title: "workspace-diagnostics-validation"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-10-27"
---
# _workspace/diagnostics/validation

> 저장소 validator 진단 출력을 두는 ignore된 staging 영역이다.

## Overview

`python3 scripts/qa.py quick|staged`와 `scripts/validate-*.py`를 실행해 나온 출력을, 실패 원인을 찾는 동안 보관한다.

이 README만 추적한다. 나머지 하위 항목은 ignore되며 Git에 force-add하지 않는다.

## Scope

### Permitted Artifacts

- `scripts/qa.py` lane 출력 (`> _workspace/diagnostics/validation/<lane>.log`)
- 단일 validator의 `--root .` 실행 출력
- 실패를 재현한 최소 입력의 비밀 없는 사본

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

통과·실패 판정은 Task Evidence에 명령, exit code, 입력 snapshot(working-tree 또는 index)과 함께 기록한다. 로그 파일 경로는 증거로 인용하지 않는다. ignore된 파일은 다른 checkout에서 열 수 없기 때문이다.

옮길 곳이 없는 산출물은 작업을 닫기 전에 삭제한다.

### Tracking Rules

- 추적 대상은 `_workspace/diagnostics/validation/README.md` 하나다.
- `scripts/validate-workspace-boundary.py`가 Git metadata만으로 이 경계를 검사한다.
  README가 추적되는지, 같은 위치의 `probe.log`가 ignore되는지 확인하며,
  ignore된 하위 항목은 열거나 읽지 않는다.

## Related Documents

- [상위 staging 경계](../README.md)
- [Approval Boundaries](../../../.agents/governance/approval-and-safety.md)
- [Workspace-staging 문서 양식 탐색](../../../docs/99.templates/README.md)
