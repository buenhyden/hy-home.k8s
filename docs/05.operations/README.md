# 05.operations

> 안정 상태 운영 지식, 정책, 런북, 사고 기록을 분류하는 operations stage다.

> [!NOTE]
> All AI agent interactions with this stage must comply with the [Agent Governance Hub](../00.agent-governance/README.md).

## Overview

`05.operations/`는 안정 상태 운영 지식, 운영 정책, 실행 런북, 사고 기록을 묶는 운영 허브다.
안내 문서는 `guides/`, 정책은 `policies/`, 절차는 `runbooks/`, 사고와 회고는 `incidents/`에 둔다.

## Operations Routing Matrix

| 필요 상황 | 사용할 위치 | 시작 템플릿 |
| --- | --- | --- |
| 시스템을 이해하거나 온보딩 절차를 따라야 함 | [guides](./guides/README.md) | [guide.template.md](../99.templates/guide.template.md) |
| 허용/금지/예외 승인 기준을 확인해야 함 | [policies](./policies/README.md) | [operation.template.md](../99.templates/operation.template.md) |
| 정해진 순서로 실행, 검증, 복구해야 함 | [runbooks](./runbooks/README.md) | [runbook.template.md](../99.templates/runbook.template.md) |
| 실제 사고 사실, 타임라인을 기록해야 함 | [incidents](./incidents/README.md) | [incident.template.md](../99.templates/incident.template.md) |
| 사고 후 원인과 재발 방지를 분석해야 함 | [incidents README](./incidents/README.md)에서 postmortem 경로 생성 조건 확인 | [postmortem.template.md](../99.templates/postmortem.template.md) |

## Audience

- GitOps Operators
- Platform Engineers
- Incident Responders
- AI Agents

## Scope

### In Scope

- 사용자/개발자/운영자 대상 안정 상태 안내
- 운영 정책, 표준, 예외 처리 기준
- 순서가 중요한 반복 절차와 복구 런북
- Incident Record와 Postmortem

### Out of Scope

- 요구사항 원문
- 아키텍처 결정 기록
- 기능 구현 상세 명세
- 임시 scratch 로그

## Structure

```text
05.operations/
├── guides/      # Steady-state user/developer/operator guides
├── policies/    # Shared operational policies and standards
├── runbooks/    # Executable operational procedures
├── incidents/   # Incident records and postmortems
└── README.md
```

## How to Work in This Area

1. 안정 상태 설명은 `guides/`, 준수해야 할 경계는 `policies/`, 실행 절차는 `runbooks/`, 사고 기록은 `incidents/`로 분리한다.
2. 사고가 없으면 `incidents/`는 README만 유지하고, 첫 postmortem이 생길 때만 `incidents/postmortems/` 하위 문서를 추가한다.
3. live cluster mutation 예시는 승인 조건, bootstrap-only 예외, break-glass 문맥 없이 추가하지 않는다.
4. 운영 문서가 현재 `bootstrap-local.sh`, `gitops/platform/external-services`, 정적 검증 계약과 충돌하지 않게 유지한다.

## Link Basis

이 README의 링크 기준 위치는 `docs/05.operations/`다.

- 하위 운영 폴더는 `./guides/`, `./policies/`, `./runbooks/`, `./incidents/`로 연결한다.
- upstream docs stage는 `../01.requirements/`, `../02.architecture/`, `../03.specs/`, `../04.execution/`로 연결한다.
- root-level runtime evidence는 `../../gitops/`, `../../infrastructure/`, `../../scripts/`처럼 repository root 기준으로 올라간다.

## Related Documents

- [Guides README](./guides/README.md)
- [Policies README](./policies/README.md)
- [Runbooks README](./runbooks/README.md)
- [Incidents README](./incidents/README.md)
- [Reference Maintenance Runbook](./runbooks/0011-reference-maintenance-runbook.md)
- [Document Stage Routing](../00.agent-governance/rules/document-stage-routing.md)
- [Templates README](../99.templates/README.md)
