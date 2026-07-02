# 05.operations

> 안정 상태 운영 지식, 정책, 런북, 사고 기록을 분류하는 operations stage다.

> [!NOTE]
> All AI agent interactions with this stage must comply with the [Agent Governance Hub](../00.agent-governance/README.md).

## Overview

`05.operations/`는 안정 상태 운영 지식, 운영 정책, 실행 런북, 사고 기록을 묶는 운영 허브다.
안내 문서는 `guides/`, 정책은 `policies/`, 절차는 `runbooks/`, 사고와 회고는 `incidents/`에 둔다.

## Operations Routing Matrix

| 필요 상황                                   | 사용할 위치                                                                  | 시작 템플릿                                                      |
| ------------------------------------------- | ---------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| 시스템을 이해하거나 온보딩 절차를 따라야 함 | [guides](./guides/README.md)                                                 | [guide.template.md](../99.templates/templates/sdlc/operations/guide.template.md)           |
| 허용/금지/예외 승인 기준을 확인해야 함      | [policies](./policies/README.md)                                             | [policy.template.md](../99.templates/templates/sdlc/operations/policy.template.md)         |
| 정해진 순서로 실행, 검증, 복구해야 함       | [runbooks](./runbooks/README.md)                                             | [runbook.template.md](../99.templates/templates/sdlc/operations/runbook.template.md)       |
| 실제 사고 사실, 타임라인을 기록해야 함      | [incidents](./incidents/README.md)                                           | [incident.template.md](../99.templates/templates/sdlc/operations/incident.template.md)     |
| 사고 후 원인과 재발 방지를 분석해야 함      | [incidents README](./incidents/README.md)에서 postmortem 경로 생성 조건 확인 | [postmortem.template.md](../99.templates/templates/sdlc/operations/postmortem.template.md) |

## Operations Folder Roles

`05.operations`는 운영 지식을 한곳에 모으되, 문서가 맡는 일을 섞지 않는다.

- `guides/`: 안정 상태에서 시스템을 이해하고 온보딩하거나 설정 흐름을 따라가기 위한 안내다.
- `policies/`: 허용/금지/예외 승인, 검증 증적, 운영 통제 기준을 정의한다.
- `runbooks/`: 정해진 순서로 실행하고, 검증하고, 실패 시 복구하는 절차다.
- `incidents/`: 실제 사고의 사실 기록과 postmortem을 보관한다.

## Language Boundary

운영 문서는 사람이 읽고 실행하는 문서이므로 한국어를 기본으로 한다. 다만
자동화가 직접 따라야 하는 `AI Agent Requirements`, `Agent Execution Notes`,
tool/prompt contract, hook/validator contract 같은 섹션은 영어로 둔다. live
cluster, Vault, secret, ArgoCD 같은 고위험 명령은 언어와 무관하게
human-approved, operator-approved, bootstrap-only, break-glass 같은 실행
경계를 가까운 문맥에 남긴다.

## Operations Mutation Boundary

운영 문서는 `kubectl apply/patch`, `argocd app sync`, `vault kv put`,
`vault policy write`, `helm upgrade/install`, `docker network connect`,
`kubectl config`처럼 live state나 외부 secret/runtime에 영향을 줄 수 있는
명령을 포함할 수 있다. 이런 예시는 반드시 가까운 문맥에서
`human-approved`, `operator-approved`, `bootstrap-only`, `break-glass`,
`external secret operation`, `temporary kubeconfig` 같은 실행 경계를 밝혀야
한다.

`bash scripts/validate-repo-quality-gates.sh .`는 authored docs와 examples의
high-risk command 예시를 스캔해 boundary marker가 없는 경우 실패한다. 이
검사는 실행 권한을 부여하지 않으며, AI Agent는 기본적으로 Git 파일 수정,
리뷰, ArgoCD reconciliation 계획, 증적 정리까지만 수행한다.

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
2. 사고가 없으면 `incidents/`는 README만 유지하고, 첫 사고 기록이 생길 때만 `incidents/YYYY/INC-###-<title>/` 폴더를 만들며 postmortem은 같은 폴더의 `postmortem.md`로 추가한다.
3. live cluster mutation 예시는 승인 조건, bootstrap-only 예외, break-glass 문맥 없이 추가하지 않는다.
4. 운영 문서가 현재 `bootstrap-local.sh`, `gitops/platform/external-services`, 정적 검증 계약과 충돌하지 않게 유지한다.
5. 현재 구현과 충돌하거나 missing GitOps desired state를 active 운영 계약처럼 설명하는 old guide/runbook은 `../98.archive/README.md`에만 인덱싱되는 Tombstone으로 이동한다.

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
- [Harness Implementation Map](../00.agent-governance/harness-implementation-map.md)
- [Approval Boundaries](../00.agent-governance/rules/approval-boundaries.md)
