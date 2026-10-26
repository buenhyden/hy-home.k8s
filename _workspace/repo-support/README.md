---
title: "workspace-repo-support"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-10-27"
---
# _workspace/repo-support

> 감사·분석·미리보기 같은 저장소 지원 작업의 산출물을 두는 ignore된 staging 영역이다.

## Overview

코드나 문서를 바꾸기 전에 만드는 분석 자료와, 바꾼 결과를 확인하는 미리보기를 둔다.

이 README만 추적한다. 나머지 하위 항목은 ignore되며 Git에 force-add하지 않는다.

## Scope

### Permitted Artifacts

- `analysis/`·`previews/` 하위에 두는 지원 산출물

모든 산출물은 비밀이 없어야 하고, 지워도 안전해야 한다.

### Forbidden Local State

- credential, 토큰, kubeconfig, 인증서, 개인 키
- 마스킹하지 않은 Secret 값이나 그 값이 들어 있는 manifest·로그
- shell history, provider cache, 개인 로컬 설정
- 다른 사람이 볼 수 없는 개인 진단 정보

## Structure

| Path | Purpose |
| --- | --- |
| `analysis/` | 감사, 인벤토리, dry-run 분석 자료 |
| `previews/` | 렌더링한 manifest와 문서 미리보기 |

## Usage

### Promotion and Cleanup

분석에서 나온 결정은 해당 Spec·Plan·Task로, 오래 둘 참고 자료는 Stage 90으로 옮긴다.

옮길 곳이 없는 산출물은 작업을 닫기 전에 삭제한다.

### Tracking Rules

- 추적 대상은 `_workspace/repo-support/README.md` 하나다.
- `scripts/validate-workspace-boundary.py`가 Git metadata만으로 이 경계를 검사한다.
  README가 추적되는지, 같은 위치의 `probe.log`가 ignore되는지 확인하며,
  ignore된 하위 항목은 열거나 읽지 않는다.

## Related Documents

- [상위 staging 경계](../README.md)
- [Approval Boundaries](../../.agents/governance/approval-and-safety.md)
- [Workspace-staging 문서 양식 탐색](../../docs/99.templates/README.md)
