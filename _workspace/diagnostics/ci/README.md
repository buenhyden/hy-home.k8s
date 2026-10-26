---
title: "workspace-diagnostics-ci"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-10-27"
---
# _workspace/diagnostics/ci

> GitHub Actions job을 로컬에서 재현한 출력을 두는 ignore된 staging 영역이다.

## Overview

`.github/workflows/ci.yml`의 job을 로컬에서 재현할 때 나오는 출력을 둔다. 예: 같은 lock(`.github/requirements/ci-validation.txt`)으로 설치한 환경에서 다시 돌린 step 출력, `gh run view --log`로 받은 실패 step 발췌.

이 README만 추적한다. 나머지 하위 항목은 ignore되며 Git에 force-add하지 않는다.

## Scope

### Permitted Artifacts

- 재현한 job·step의 stdout/stderr 발췌
- `gh run view --log-failed` 출력의 비밀 없는 발췌
- lock 설치 결과(`pip check`, 도구 버전) 기록

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

원인과 수정 근거는 해당 Task Evidence에 run ID, commit SHA, 실패 step 이름과 함께 기록한다. hosted run 결과를 로컬 재현 결과로 대체하지 않는다.

옮길 곳이 없는 산출물은 작업을 닫기 전에 삭제한다.

### Tracking Rules

- 추적 대상은 `_workspace/diagnostics/ci/README.md` 하나다.
- `scripts/validate-workspace-boundary.py`가 Git metadata만으로 이 경계를 검사한다.
  README가 추적되는지, 같은 위치의 `probe.log`가 ignore되는지 확인하며,
  ignore된 하위 항목은 열거나 읽지 않는다.

## Related Documents

- [상위 staging 경계](../README.md)
- [Approval Boundaries](../../../.agents/governance/approval-and-safety.md)
- [Workspace-staging 문서 양식 탐색](../../../docs/99.templates/README.md)
