---
title: "workspace-repo-support-analysis"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-10-27"
---
# _workspace/repo-support/analysis

> 감사·인벤토리·dry-run 분석 자료를 두는 ignore된 staging 영역이다.

## Overview

Archive 처분 단위 dry-run, route·소비자 인벤토리, 요구사항 대조표처럼 결정에 앞서 만드는 분석 자료를 둔다.

이 README만 추적한다. 나머지 하위 항목은 ignore되며 Git에 force-add하지 않는다.

## Scope

### Permitted Artifacts

- 처분·이전 대상 인벤토리(CSV/JSON)
- `git grep`·`graphify` 결과를 정리한 소비자 목록
- 외부 실행 명세와 그 대조 자료의 로컬 사본

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

확정한 판정은 소유 Task의 Evidence와 결정 표에 기록한다. 분석 파일 자체를 승인이나 수용의 근거로 삼지 않는다.

옮길 곳이 없는 산출물은 작업을 닫기 전에 삭제한다.

### Tracking Rules

- 추적 대상은 `_workspace/repo-support/analysis/README.md` 하나다.
- `scripts/validate-workspace-boundary.py`가 Git metadata만으로 이 경계를 검사한다.
  README가 추적되는지, 같은 위치의 `probe.log`가 ignore되는지 확인하며,
  ignore된 하위 항목은 열거나 읽지 않는다.

## Related Documents

- [상위 staging 경계](../README.md)
- [Approval Boundaries](../../../.agents/governance/approval-and-safety.md)
- [Workspace-staging 문서 양식 탐색](../../../docs/99.templates/README.md)
