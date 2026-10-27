---
title: "workspace-diagnostics"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-10-27"
---
# _workspace/diagnostics

> 저장소 QA·CI 진단 출력을 두는 ignore된 staging 영역이다.

## Overview

로컬에서 재현한 CI 실패와 validator 진단처럼, 원인을 좁히는 동안만 필요한 출력을 모은다. 하위 경로는 출처에 따라 나뉜다.

이 README만 추적한다. 나머지 하위 항목은 ignore되며 Git에 force-add하지 않는다.

## Scope

### Permitted Artifacts

- `ci/`·`validation/` 하위에 두는 진단 출력

모든 산출물은 비밀이 없어야 하고, 지워도 안전해야 한다.

### Forbidden Local State

- credential, 토큰, kubeconfig, 인증서, 개인 키
- 마스킹하지 않은 Secret 값이나 그 값이 들어 있는 manifest·로그
- shell history, provider cache, 개인 로컬 설정
- 다른 사람이 볼 수 없는 개인 진단 정보

## Structure

| Path | Purpose |
| --- | --- |
| `ci/` | GitHub Actions job을 로컬에서 재현한 출력 |
| `validation/` | `scripts/qa.py`와 개별 validator의 진단 출력 |

두 경로에 자동으로 쓰는 producer는 없다. 작업자가 필요한 출력을 직접 리디렉션해 둔다.
`scripts/qa.py`는 자체 임시 디렉터리를 쓰고 이 경로에 쓰지 않는다.

## Usage

### Promotion and Cleanup

진단에서 확정한 원인과 증거는 해당 Task의 Evidence 표로 옮긴다. 원본 로그는 옮기지 않는다.

옮길 곳이 없는 산출물은 작업을 닫기 전에 삭제한다.

### Tracking Rules

- 추적 대상은 `_workspace/diagnostics/README.md` 하나다.
- `scripts/validate-workspace-boundary.py`가 Git metadata만으로 이 경계를 검사한다.
  README가 추적되는지, 같은 위치의 `probe.log`가 ignore되는지 확인하며,
  ignore된 하위 항목은 열거나 읽지 않는다.

## Related Documents

- [상위 staging 경계](../README.md)
- [Approval Boundaries](../../.agents/governance/approval-and-safety.md)
- [Workspace-staging 문서 양식 탐색](../../docs/99.templates/README.md)
