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
├── progress.template.md
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
5. 템플릿의 Target 경로와 실제 저장 위치를 맞추고, 상대 경로만 사용한다.
6. PRD/ARD/ADR/Spec/Plan/Task의 추적성을 유지한다.
7. Agent 기능 문서는 Role, Tool, Guardrail, Eval, Fallback을 빠뜨리지 않는다.
8. 템플릿의 placeholder 또는 code-literal cross-link는 최종 authored Target 위치 기준으로 계산한다.
   실제 Markdown 링크는 이 템플릿 파일 위치에서도 깨지지 않아야 한다.
9. README 템플릿은 frontmatter를 요구하지 않는다. PRD/ARD/ADR/Spec/Plan/Task, Spec helper Markdown 템플릿(`api-spec`, `agent-design`, `data-model`, `tests`), 운영·참조 템플릿은 `title`, `type`, `status`, `owner`, `updated` metadata를 유지한다.
10. 템플릿 구조를 바꾸면 이미 생성된 문서에 안전하게 반영할 수 있는 heading, placeholder, Related Documents만 갱신하고 문서 고유 의도는 대량 재작성하지 않는다.

## Link Basis

이 README의 링크 기준 위치는 `docs/99.templates/`다.

- 템플릿 안의 실제 Markdown 링크는 `docs/99.templates/` 기준으로도 resolve되어야 한다.
- 최종 authored 문서 예시 경로는 해당 Target 위치 기준의 code literal로 작성한다.
- 아직 존재하지 않는 optional 문서, placeholder 경로, target-relative 예시는 Markdown 링크가 아니라 backtick code literal로 남긴다.
- 생성 문서에 템플릿 안내 주석, placeholder, `Target:` 주석, `Use this template` 문구를 남기지 않는다.

## Template-Folder Mapping

| Target Pattern | Template | Responsibility |
| --- | --- | --- |
| `README.md`, `docs/**/README.md`, `.claude/README.md`, `.codex/README.md` | `readme.template.md` | Entry point, scope, structure, workflow, link basis |
| `docs/01.requirements/YYYY-MM-DD-<feature-or-system>.md` | `prd.template.md` | Product requirements, users, scope, success / acceptance criteria |
| `docs/02.architecture/requirements/####-<system-or-domain>.md` | `ard.template.md` | Architecture requirements, quality attributes, reference model |
| `docs/02.architecture/decisions/####-<short-title>.md` | `adr.template.md` | One architecture decision, context, consequences, alternatives |
| `docs/03.specs/<feature-id>/spec.md` | `spec.template.md` | Implementation contract, interfaces, verification |
| `docs/03.specs/<feature-id>/api-spec.md` | `api-spec.template.md` | Feature-local API contract |
| `docs/03.specs/<feature-id>/agent-design.md` | `agent-design.template.md` | Feature-local AI agent behavior, orchestration, safety, and eval design |
| `docs/03.specs/<feature-id>/data-model.md` | `data-model.template.md` | Feature-local logical and physical data model |
| `docs/03.specs/<feature-id>/tests.md` | `tests.template.md` | Feature-local test and evaluation strategy |
| `docs/03.specs/<feature-id>/contracts/openapi.yaml` | `openapi.template.yaml` | Feature-local OpenAPI contract |
| `docs/03.specs/<feature-id>/contracts/schema.graphql` | `schema.template.graphql` | Feature-local GraphQL schema contract |
| `docs/03.specs/<feature-id>/contracts/service.proto` | `service.template.proto` | Feature-local gRPC/protobuf contract |
| `docs/03.specs/<feature-id>/README.md` | `readme.template.md` | Optional feature-local index when a spec folder grows beyond `spec.md` |
| `docs/04.execution/plans/YYYY-MM-DD-<feature>.md` | `plan.template.md` | Execution order, risk control, rollout, verification |
| `docs/04.execution/tasks/YYYY-MM-DD-<feature-or-stream>.md` | `task.template.md` | Implementation and validation task evidence |
| `docs/05.operations/guides/####-<topic>.md` | `guide.template.md` | Stable-state user, developer, or operator guidance |
| `docs/05.operations/policies/####-<policy-or-standard>.md` | `operation.template.md` | Operational policy, controls, boundaries |
| `docs/05.operations/runbooks/####-<topic>.md` | `runbook.template.md` | Executable operational procedure and recovery path |
| `docs/05.operations/incidents/YYYY/YYYY-MM-DD-<incident>.md` | `incident.template.md` | Incident fact record and timeline |
| `docs/05.operations/incidents/postmortems/YYYY/YYYY-MM-DD-<incident>.md` | `postmortem.template.md` | Incident analysis and prevention follow-up |
| `docs/90.references/<category>/<topic>.md` | `reference.template.md` | Reference material, glossary, appendix, inventory |
| `docs/00.agent-governance/memory/<topic>.md` | `memory.template.md` | Stable memory entry |
| `docs/00.agent-governance/memory/progress.md` | `progress.template.md` | Repo-changing work progress entry |

## Contract Template Placement

API 계약 문서는 별도 top-level docs 유형이 아니라 `03.specs/` 아래에서 사용하는 하위 템플릿이다.

- 올바른 위치: `docs/03.specs/<feature-id>/api-spec.md`
- 잘못된 패턴: `docs/api/...`

OpenAPI, GraphQL, proto 같은 계약 파일은 관련 `docs/03.specs/<feature-id>/` 문맥에서 추적성을 유지한다.

## Reference and Memory Rules

`reference.template.md`는 `90.references/` 문서의 역할과 freshness를 강제한다.

- 모든 reference 문서는 `Reference Type`을 명시한다.
- 모든 reference 문서는 `Authority Boundary`에서 소유하는 사실과 소유하지 않는 실행계약을 분리한다.
- 외부 기준이나 버전 snapshot은 `Review and Freshness`에 검토일과 갱신 trigger를 남긴다.
- repo-changing agent work의 진행 상황은 `progress.template.md` 구조로 `00.agent-governance/memory/progress.md`에 작성한다.
- `00.agent-governance/memory/`에 standalone memory 파일을 만들거나 갱신할 때는 `memory.template.md`를 사용한다.
- standalone memory 파일 변경은 같은 변경 단위에서 `progress.md` entry를 함께 남긴다.

## README and Spec Helper Templates

각 폴더 README도 반복적으로 재사용되는 문서 유형이므로 별도 README 템플릿을 함께 제공한다.
`03.specs/<feature-id>/` 아래에서 반복적으로 사용하는 보조 설계 문서와 계약 파일용 템플릿을 함께 제공한다.

- `readme.template.md`는 repository root, `docs/README.md`, stage README, nested README에서 재사용되는 multi-target 템플릿이다. 단일 `Target:` 주석을 강제하지 않고, 최종 README 위치에서 상대 링크를 다시 계산한다.
- `docs/03.specs/<feature-id>/README.md`는 필수가 아니다. 기본 인덱스는 `docs/03.specs/README.md`가 소유하며, feature-local README는 API/agent/data/test 보조 문서가 늘어날 때만 만든다.
- `openapi.template.yaml`, `schema.template.graphql`, `service.template.proto`는 형식상 YAML/GraphQL/proto 파일이므로 frontmatter 없이 owner comments와 parent API spec 링크로 추적성을 유지한다.
- `memory.template.md`는 `docs/00.agent-governance/memory/<topic>.md` target family를 사용한다. 관련 progress 링크는 최종 memory 파일 위치 기준으로 계산한다.
- `progress.template.md`는 `docs/00.agent-governance/memory/progress.md`에 append되는 entry 템플릿이다. entry 안의 링크는 `docs/00.agent-governance/memory/` 기준으로 계산한다.

## Related Documents

- [Docs README](../README.md)
- [Agent Governance Hub](../00.agent-governance/README.md)
- [Documentation Protocol](../00.agent-governance/rules/documentation-protocol.md)
- [Stage Authoring Matrix](../00.agent-governance/rules/stage-authoring-matrix.md)
