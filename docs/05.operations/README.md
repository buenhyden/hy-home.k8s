---
title: "05.operations"
version: "0.7.0"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-11-17"
---
# 05.operations

## Responsibility

### Purpose

> 안정 상태 운영 지식, 정책, 런북, 사고 기록을 분류하는 operations stage다.

`05.operations/`는 안정 상태 운영 지식, 운영 정책, 실행 런북, 사고 기록을 묶는 운영 허브다.
안내 문서는 `guides/`, 정책은 `policies/`, 절차는 `runbooks/`, 사고와 회고는 `incidents/`에 둔다.

#### Stage Readers

- GitOps Operators
- Platform Engineers
- Incident Responders

#### Inputs and Outputs

##### In Scope

- 사용자/개발자/운영자 대상 안정 상태 안내
- 운영 정책, 표준, 예외 처리 기준
- 순서가 중요한 반복 절차와 복구 런북
- Incident Record와 Postmortem

##### Out of Scope

- 요구사항 원문
- 아키텍처 결정 기록
- 기능 구현 상세 명세
- 임시 scratch 로그

##### Release Evidence Boundary

반복 가능한 발행 절차는 Runbook `RUN-0012`에 둔다.
개별 발행의 로컬 변경과 검증은 해당 Task와 Git에 기록하고, 발행 이력은
[CHANGELOG](../../CHANGELOG.md)에 남긴다. 태그, GitHub Release, hosted CI,
provider/runtime, 실제 운영 검증은 각각 관측한 결과를 링크한다.

### Excluded Responsibilities

이 stage는 요구사항 원문, 아키텍처 결정 기록, 기능 구현 상세 명세, 임시 scratch 로그를 소유하지 않는다. guides, policies, runbooks, incidents는 각자 맡는 일을 섞지 않으며, 개별 발행의 로컬 변경과 검증은 해당 Task와 Git에, 발행 이력은 `CHANGELOG`에 남는다.

## Current Contents

### Paths

```text
05.operations/
├── guides/
├── policies/
├── runbooks/
├── incidents/
├── AGENTS.md
├── CLAUDE.md
└── README.md
```

| Path | Purpose |
| --- | --- |
| [01.guides/](./01.guides/) | 안정 상태의 사용자·개발자·운영자 가이드 |
| [02.policies/](./02.policies/) | 공유 운영 정책과 표준 |
| [03.runbooks/](./03.runbooks/) | 실행 가능한 운영 절차 |
| [04.incidents/](./04.incidents/) | 사고 기록과 사후 분석 |
| [AGENTS.md](./AGENTS.md) | 이 stage에 적용되는 AI 에이전트 지시 |
| [CLAUDE.md](./CLAUDE.md) | Claude가 이 stage의 `AGENTS.md`를 불러오게 하는 한 줄 `@AGENTS.md` import |

#### Operations Folder Roles

`05.operations`는 운영 지식을 한곳에 모으되, 문서가 맡는 일을 섞지 않는다.

- `guides/`: 안정 상태에서 시스템을 이해하고 온보딩하거나 설정 흐름을 따라가기 위한 안내다.
- `policies/`: 허용/금지/예외 승인, 검증 증적, 운영 통제 기준을 정의한다.
- `runbooks/`: 정해진 순서로 실행하고, 검증하고, 실패 시 복구하는 절차다.
- `incidents/`: 실제 사고의 사실 기록과 postmortem을 보관한다.

### Owners

#### Operations Routing Matrix

| 필요 상황                                   | 사용할 위치                                                                  | 시작 템플릿                                                      |
| ------------------------------------------- | ---------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| 시스템을 이해하거나 온보딩 절차를 따라야 함 | [guides](./01.guides/README.md)                                                 | [guide.template.md](../99.templates/02.templates/05.operations/guide.template.md)           |
| 허용/금지/예외 승인 기준을 확인해야 함      | [policies](./02.policies/README.md)                                             | [policy.template.md](../99.templates/02.templates/05.operations/policy.template.md)         |
| 정해진 순서로 실행, 검증, 복구해야 함       | [runbooks](./03.runbooks/README.md)                                             | [runbook.template.md](../99.templates/02.templates/05.operations/runbook.template.md)       |
| 실제 사고 사실, 타임라인을 기록해야 함      | [incidents](./04.incidents/README.md)                                           | [incident.template.md](../99.templates/02.templates/05.operations/incident.template.md)     |
| 사고 후 원인과 재발 방지를 분석해야 함      | [incidents README](./04.incidents/README.md)에서 postmortem 경로 생성 조건 확인 | [postmortem.template.md](../99.templates/02.templates/05.operations/postmortem.template.md) |

#### Operations Mutation Boundary

운영 문서는 `kubectl apply/patch`, `argocd app sync`, `vault kv put`,
`vault policy write`, `helm upgrade/install`, `docker network connect`,
`kubectl config`, secret 값을 출력하는 `kubectl get secret -o yaml/json`처럼
live state나 외부 secret/runtime에 영향을 줄 수 있는 명령을 포함할 수 있다.
이런 예시는 반드시 가까운 문맥에서 실행 경계를 밝혀야 한다.

| 명령 계열 | 가까운 문맥에 둘 경계 |
| --- | --- |
| `kubectl apply/patch`, `docker network` 변경 | `human-approved`, `operator-approved`, `bootstrap-only`, `break-glass` |
| `argocd app sync` | `operator-triggered reconciliation`, `operator-approved`, `break-glass` |
| `helm upgrade/install` | `human-approved`, `operator-approved`, `break-glass` |
| `vault kv put`, `vault policy write` | `external secret operation`, `human-approved` |
| `kubectl config` 등 kubeconfig 변경 | `temporary kubeconfig` 또는 명시적 `--kubeconfig` |
| Secret 조회 | 값 비출력 `jsonpath` 등 실제 출력 선택자를 사용한다. raw YAML/JSON 출력은 실행 예시로 허용하지 않는다. |

이 절이 Stage 05 marker 규칙의 사람용 단일 설명이며, 하위 README는 이 절을
반복하지 않는다. 위험 명령을 설명·금지하는 산문 인용은 안전한 문서 작성이다.
`prohibited-example:` 또는 `do-not-run:`과 같은 줄의 backtick 인용은 실행
제안과 구분하며, runnable code block이나 shell comment에 표지를 붙이는 것으로
검사를 해제하지 않는다. `redacted`나 `metadata-only`라는 가까운 문구는
raw secret 출력 명령의 실제 출력을 바꾸지 않는다.
정확한 명령 패턴과 허용 marker 목록의 machine owner는
repository quality validator의 command boundary 규칙이며, 해당 변경에
선택된 문서 내용·repository quality gate가 authored docs와 examples를
스캔해 marker가 없으면 실패한다. live 변경 예외의 승인 조건은
[POL-0001](./02.policies/0001-k8s-gitops-operations-policy.md#exceptions)이
소유한다. 공통 승인 원본 확인과 저술/실행 권한은
[Approval and Safety](../00.workspace/04.quality/approval-and-safety.md)가 소유한다.
marker는 실행 권한을 부여하지 않는다.

## Usage

### Entry Points

1. 안정 상태 설명은 `guides/`, 준수해야 할 경계는 `policies/`, 실행 절차는 `runbooks/`, 사고 기록은 `incidents/`로 분리한다.
2. 사고가 없으면 `incidents/`는 README만 유지하고, 첫 사고 기록이 생길 때만 `incidents/<year>/inc-####-<slug>/` 폴더를 만든다. Incident와 Postmortem은 같은 폴더에서 각각 `incident.md`와 `postmortem.md`를 사용한다.
3. live cluster mutation 예시는 승인 조건, bootstrap-only 예외, break-glass 문맥 없이 추가하지 않는다.
4. 운영 문서가 현재 `infrastructure/bootstrap-local.sh`, `gitops/platform/external-services`, 정적 검증 계약과 충돌하지 않게 유지한다.

#### Relative Link Rules

이 README의 링크 기준 위치는 `docs/05.operations/`다.

- 하위 운영 폴더는 `./guides/`, `./policies/`, `./runbooks/`, `./incidents/`로 연결한다.
- upstream docs stage는 `../01.requirements/`, `../02.architecture/`, `../03.specs/`로 연결한다.
- 운영 목표 상태와 정적 검사의 원본은 [GitOps 선언](../../gitops/), [인프라 설정](../../infrastructure/), [검사 도구](../../scripts/)처럼 repository root 기준으로 연결한다. 실제 운영 검증 결과는 해당 Task나 운영 기록으로 연결한다.

#### Language Boundary

운영 문서는 사람이 읽고 실행하는 문서이므로 한국어를 기본으로 한다. 다만
tool/prompt contract, hook/validator contract 같은 기계 계약 섹션은 영어로 둔다. live
cluster, OpenBao, secret, ArgoCD 같은 고위험 명령의 실행 경계는 언어와
무관하게 위 Operations Mutation Boundary를 따른다.

#### Upstream and Downstream

- [Guides README](./01.guides/README.md)
- [Policies README](./02.policies/README.md)
- [Runbooks README](./03.runbooks/README.md)
- [Incidents README](./04.incidents/README.md)
- [Reference Maintenance Runbook](../00.workspace/06.maintenance/0011-reference-maintenance-runbook.md)

#### Policy and Templates

- [Document Stage Routing](../00.workspace/03.process/document-authoring.md)
- [Templates README](../99.templates/README.md)
- [Local Agent Registry](../../.agents/roles/registry.json)
- [Approval Boundaries](../00.workspace/04.quality/approval-and-safety.md)

### Checks

1. 현재 구현과 충돌하거나 소유 문서와 중복되는 운영 문서는 활성 소비자를 현재 Policy/Runbook으로 전환한 뒤 [Document Lifecycle Policy](../00.workspace/03.process/document-lifecycle.md)에 따라 처분한다. 대체 Guide·Policy·Runbook이 `supersedes`에 선행 문서의 ID를 기록한다. 수명주기 검사기는 그 관계에서 후속 문서를 찾아 현재 소유자를 확인한다.
