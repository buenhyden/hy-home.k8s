# 99.templates

> [!NOTE]
> All AI agent interactions with this stage must comply with the [Agent Governance Hub](../00.agent-governance/README.md).

## Overview

이 경로는 repo-authored 문서와 README가 시작해야 하는 canonical template stage다.
새 문서 형식을 임의로 만들기 전에 여기의 템플릿과 상위 문서 라우팅 규칙을 먼저 확인한다.

## Audience

이 README의 주요 독자:

- Documentation Writers
- Platform Engineers
- Repository Maintainers
- AI Agents

## Scope

### In Scope

- 문서 stage별 Markdown 템플릿
- API/OpenAPI, GraphQL, proto 계약 템플릿
- README와 governance memory 항목 템플릿

### Out of Scope

- 실제 PRD/ARD/ADR/Spec/Plan/Task 문서
- 운영 기록이나 사고 기록
- 특정 기능의 구현 계약

## Structure

```text
99.templates/
├── adr.template.md
├── agent-design.template.md
├── api-spec.template.md
├── ard.template.md
├── data-model.template.md
├── guide.template.md
├── incident.template.md
├── memory.template.md
├── openapi.template.yaml
├── operation.template.md
├── plan.template.md
├── postmortem.template.md
├── prd.template.md
├── readme.template.md
├── reference.template.md
├── runbook.template.md
├── schema.template.graphql
├── service.template.proto
├── spec.template.md
├── task.template.md
├── tests.template.md
└── README.md
```

## How to Work in This Area

1. 새 문서를 만들 때 현재 stage에 맞는 템플릿을 먼저 선택한다.
2. 템플릿의 placeholder와 안내 주석은 authored 문서에서 제거한다.
3. 템플릿을 추가하거나 제거하면 이 README의 목록과 매핑을 함께 갱신한다.
4. README 변경 시 `readme.template.md`의 base structure와 품질 게이트가 일치하는지 확인한다.

## Related References

- [Docs README](../README.md)
- [Agent Governance Hub](../00.agent-governance/README.md)
- [Documentation Protocol](../00.agent-governance/rules/documentation-protocol.md)
- [Stage Authoring Matrix](../00.agent-governance/rules/stage-authoring-matrix.md)

## 목적

이 폴더는 문서 템플릿을 저장한다. 새 문서는 이 폴더의 템플릿을 복사해 시작한다.

## 포함할 내용

- 문서 stage별 Markdown 템플릿
- API/OpenAPI, GraphQL, proto 같은 계약 템플릿
- README와 governance memory 항목 템플릿

## 포함하지 말아야 할 내용

- 실제 PRD/ARD/ADR/Spec/Plan/Task 문서
- 운영 기록이나 사고 기록
- 특정 기능의 구현 계약

## 템플릿 목록

- `agent-design.template.md`
- `data-model.template.md`
- `tests.template.md`
- `openapi.template.yaml`
- `service.template.proto`
- `schema.template.graphql`
- `prd.template.md`
- `ard.template.md`
- `adr.template.md`
- `spec.template.md`
- `api-spec.template.md`
- `plan.template.md`
- `task.template.md`
- `guide.template.md`
- `operation.template.md`
- `runbook.template.md`
- `incident.template.md`
- `postmortem.template.md`
- `reference.template.md`
- `readme.template.md`
- `memory.template.md`

## 사용 원칙

1. 템플릿의 Target 경로를 실제 저장 위치와 맞춘다.
2. Placeholder는 모두 제거한다.
3. 상대 경로만 사용한다.
4. PRD/ARD/ADR/Spec/Plan/Task의 추적성을 유지한다.
5. Agent 기능은 Role, Tool, Guardrail, Eval, Fallback을 빠뜨리지 않는다.

## 템플릿-폴더 매핑

| Folder | Template |
| --- | --- |
| `01.prd/` | `prd.template.md` |
| `02.ard/` | `ard.template.md` |
| `03.adr/` | `adr.template.md` |
| `04.specs/` | `spec.template.md` |
| `04.specs/<feature-id>/api-spec.md` | `api-spec.template.md` |
| `05.plans/` | `plan.template.md` |
| `06.tasks/` | `task.template.md` |
| `07.guides/` | `guide.template.md` |
| `08.operations/` | `operation.template.md` |
| `09.runbooks/` | `runbook.template.md` |
| `10.incidents/` | `incident.template.md` |
| `10.incidents/postmortems/` | `postmortem.template.md` |
| `90.references/` | `reference.template.md` |
| `00.agent-governance/memory/` | `memory.template.md` |

## API Spec 템플릿 위치

API 계약 문서는 별도 유형이 아니라 `04.specs/` 아래에서 사용하는 하위 템플릿이다.

- 올바른 위치: `docs/04.specs/<feature-id>/api-spec.md`
- 잘못된 패턴: `docs/api/...`

## README 템플릿

각 폴더 README도 반복적으로 재사용되는 문서 유형이므로 별도 README 템플릿을 함께 제공한다.

## Spec 하위 보조 문서 템플릿

`04.specs/<feature-id>/` 아래에서 반복적으로 사용하는 보조 설계 문서와 계약 파일용 템플릿을 함께 제공한다.

## 관련 폴더

- `00.agent-governance/`: 템플릿 사용 규칙과 문서 라우팅 정책
- `01.prd/` ~ `10.incidents/`: 템플릿을 적용하는 authored stage
- `90.references/`: reference 템플릿 적용 대상

## 예시

- 새 PRD는 `prd.template.md`에서 시작한다.
- 새 런북은 `runbook.template.md`에서 시작한다.
- 사고 후 회고는 `postmortem.template.md`를 사용해 `10.incidents/postmortems/`에 작성한다.
