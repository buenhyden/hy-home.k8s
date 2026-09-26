---
title: "workspace"
version: "0.1.0"
type: "common/readme-workspace-staging"
status: "active"
owner: "platform"
updated: "2026-09-26"
---
# _workspace

> 비밀이 아닌 임시 분석 산출물을 두는 저장소 로컬 지원 staging 영역이다.

## Overview

`_workspace/`는 감사, migration dry-run, route inventory 작업 중에 생기는
수명이 짧고 비밀이 아닌 산출물을 두는 격리된 저장소 지원 staging 경계다.
오래 유지할 문서, runtime 진단, 인증 상태, 개인 로컬 데이터를 두는 곳이 아니다.

이 README만 추적한다. scratch 하위 항목은 ignore 상태로 남고 Git에 강제로
추가하면 안 된다.

## Permitted Artifacts

- 임시 감사 scratch
- 가리고 정리한, 비밀이 아닌 dry-run 요약
- 생성된 route inventory
- migration 원장
- 비밀이 아닌 scan 요약

모든 산출물은 저장소 지원 범위 안에 있어야 하고 지워도 안전해야 하며
credential이나 secret이 담긴 runtime 세부 정보를 포함하지 않아야 한다.

## Forbidden Local State

다음 항목은 `_workspace/`에 두지 않는다.

- credential, 토큰, 인증 파일, kubeconfig
- SSH 키, 인증서, 그 밖의 개인 키 material
- shell history, 브라우저 프로필, provider cache, 로컬 설정
- 비공개 상태를 드러낼 수 있는 개인 진단 정보나 로컬 로그
- secret이 담긴 scan 출력, dry-run 로그, 명령 transcript

진단 정보, 로컬 로그, 인증 material, 토큰, shell history는 저장소와 이 staging
경계 밖에 둔다.

## Promotion and Cleanup

오래 남길 결과는 정본 소유 경로로 옮긴다.

- 에이전트 거버넌스와 재사용 memory는 Stage 00
- 변경 범위의 Spec, Plan, Task, 검증 계약은 Stage 03
- 오래 유지할 감사와 참조 자료는 Stage 90
- registry, schema, template 계약은 Stage 99

옮길 곳이 없는 임시 산출물은 작업을 닫기 전에 삭제한다. 옮길 때는 대상 문서의
template, 리뷰, secret 처리 계약을 지켜야 한다. 가공하지 않은 scratch를
force-add로 옮기지 않는다.

## Tracking Rules

추적되는 형태는 다음과 같다.

```text
_workspace/
├── README.md          # Tracked contract for this staging boundary
└── <ignored scratch>  # Temporary non-secret repository-support files
```

이 계약은 Git metadata로만 검증한다.

- `git ls-files _workspace`는 `_workspace/README.md`를 반환해야 한다.
- `git check-ignore -q _workspace/probe.tmp`는 probe 파일을 만들지 않고
  성공해야 한다.

이 규칙을 확인하는 동안 ignore된 하위 항목을 나열하거나, 열거나, 읽거나,
해시하거나, 옮기거나, 삭제하지 않는다.

## Related Documents

- [Documentation Protocol](../.agents/governance/document-authoring.md)
- [Approval Boundaries](../.agents/governance/approval-and-safety.md)
- [Subagent Protocol](../.agents/workflows/delegated-development.md)
- Documentation Contract (`docs/99.templates/README.md`)
- Workspace-staging README form (`docs/99.templates/templates/common/readme-workspace-staging.template.md`)
