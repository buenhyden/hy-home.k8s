# 99.templates

> repo-authored 문서와 README가 시작해야 하는 canonical template stage다.

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
- 중앙 archive Tombstone 템플릿
- API/OpenAPI, GraphQL, proto 계약 템플릿
- 보호 표면 변경을 위한 canonical Task 승인·안전 계약
- README와 governance memory 항목 템플릿

### Out of Scope

- 실제 PRD/ARD/ADR/Spec/Plan/Task 문서
- 운영 기록이나 사고 기록
- 특정 기능의 구현 계약

## Structure

```text
99.templates/
├── support/
│   ├── README.md
│   ├── common-documentation-governance.md
│   ├── documentation-contract.md
│   ├── frontmatter-schema.md
│   ├── legacy-cleanup-rules.md
│   ├── sdlc-governance.md
│   └── template-routing.md
├── templates/
│   ├── README.md
│   ├── common/
│   │   ├── archive-tombstone.template.md
│   │   ├── governance-reference.template.md
│   │   ├── memory.template.md
│   │   ├── progress.template.md
│   │   ├── readme-collection-index.template.md
│   │   ├── readme-implementation.template.md
│   │   ├── readme-repository.template.md
│   │   ├── readme-snapshot-pack.template.md
│   │   ├── readme-stage-index.template.md
│   │   ├── readme-workspace-staging.template.md
│   │   ├── readme.template.md
│   │   ├── reference.template.md
│   │   └── template-support.template.md
│   └── sdlc/
│       ├── architecture/
│       │   ├── adr.template.md
│       │   └── ard.template.md
│       ├── execution/
│       │   ├── plan.template.md
│       │   └── task.template.md
│       ├── operations/
│       │   ├── guide.template.md
│       │   ├── incident.template.md
│       │   ├── policy.template.md
│       │   ├── postmortem.template.md
│       │   └── runbook.template.md
│       ├── requirements/
│       │   └── prd.template.md
│       └── specs/
│           ├── agent-design.template.md
│           ├── api-spec.template.md
│           ├── data-model.template.md
│           ├── openapi.template.yaml
│           ├── schema.template.graphql
│           ├── service.template.proto
│           ├── spec.template.md
│           └── tests.template.md
└── README.md
```

## How to Work in This Area

1. 새 문서를 만들 때 현재 stage에 맞는 템플릿을 먼저 선택한다.
2. 템플릿 contract, frontmatter, governance, routing을 바꾸기 전에는
   [`support/`](./support/README.md)의 관련 support 문서를 먼저 확인한다.
3. 템플릿의 placeholder와 안내 주석은 authored 문서에서 제거한다.
4. 템플릿을 추가하거나 제거하면 이 README의 목록과 매핑을 함께 갱신한다.
5. README 변경 시 `readme.template.md`의 base structure와 품질 게이트가 일치하는지 확인한다.
6. 템플릿의 Target 경로와 실제 저장 위치를 맞추고, 상대 경로만 사용한다.
7. stage README는 target file pattern을 장황하게 복제하지 말고 `support/template-routing.md`와 이 README의 Template-Folder Mapping으로 연결한다.
8. PRD/ARD/ADR/Spec/Plan/Task의 추적성을 유지한다.
9. Agent 기능 문서는 Role, Tool, Guardrail, Eval, Fallback을 빠뜨리지 않는다.
10. 템플릿의 placeholder 또는 code-literal cross-link는 최종 authored Target 위치 기준으로 계산한다.
   실제 Markdown 링크는 이 템플릿 파일 위치에서도 깨지지 않아야 한다.
11. README 템플릿은 frontmatter를 요구하지 않는다. PRD/ARD/ADR/Spec/Plan/Task, Spec helper Markdown 템플릿(`api-spec`, `agent-design`, `data-model`, `tests`), 운영·참조 템플릿은 `title`, `type`, `status`, `owner`, `updated` metadata를 유지한다.
    새 authored 문서의 기본 `status`는 `draft`, 기본 `owner`는 `platform`이다. Status promotion은 owning Plan/Task evidence 또는 human review 후에만 수행한다.
    `.github/ABOUT.md`, `.github/PULL_REQUEST_TEMPLATE.md`, `.github/SECURITY.md`는 GitHub-native control Markdown이므로 frontmatter-free 예외로 유지한다.
12. 템플릿 구조를 바꾸면 이미 생성된 문서에 안전하게 반영할 수 있는 heading, placeholder, `Link Basis`, `Related Documents`만 갱신하고 문서 고유 의도는 대량 재작성하지 않는다.
13. `Related Documents` 예시는 upstream PRD/ARD/ADR/Spec/Plan과 downstream Task/Operation/Runbook/Incident를 추적할 수 있어야 한다.
14. `docs/01.requirements`, `docs/02.architecture`, `docs/03.specs`, `docs/04.execution`, `docs/05.operations`, `docs/90.references`, `docs/98.archive` 아래의 비-README Markdown은 정확히 하나의 Template-Folder Mapping 행에 매핑되어야 한다.
15. `examples/aws/docs/**`와 `examples/azure/docs/**`의 비-README Markdown은 example-local SDLC snapshot route로 분류하고, 문서 역할에 맞는 SDLC frontmatter와 섹션 기대값을 적용한다.
16. 실행 전제가 바뀌면 active README/guide/runbook은 새 current contract로 갱신하고, 현재 구현과 상충하는 old PRD/ARD/ADR/Spec/Plan/Task는 `docs/98.archive` Tombstone으로 이동한다.

## Language Policy

- `spec.template.md`로 만드는 `docs/03.specs/**/spec.md` 문서는 영어로 작성한다.
- `plan.template.md`로 만드는 `docs/04.execution/plans/*.md` 문서는 영어로 작성한다.
- `task.template.md`로 만드는 `docs/04.execution/tasks/*.md` 문서는 영어로 작성한다.
- `guide`, `policy`, `runbook`, `incident`, `postmortem` 문서는 운영자가 읽는 본문은 한국어를 기본으로 하되, AI Agent 실행 지시나 tool/prompt contract는 영어로 분리한다.
- `reference.template.md`로 만드는 `docs/90.references/**/*.md` 문서는 사람용 overview와 설명에는 한국어를 사용할 수 있지만, `Reference Type`, `Authority Boundary`, `Sources`, `Review and Freshness`, version support boundary, generated-index contract는 영어를 우선한다.

## Template Improvement Plan

템플릿을 수정할 때는 먼저 `support/template-routing.md`, 이 README의 mapping, link rules를 갱신 대상으로 확정한다.

- target pattern, placeholder naming, target-relative examples를 mapping과 일치시킨다.
- 실제 Markdown 링크는 `docs/99.templates/` 기준으로 resolve되게 유지하고, 아직 존재하지 않는 target-relative 예시는 code literal로 둔다.
- core template 변경 후에는 기존 생성 문서에 안전하게 반영 가능한 heading, `Related Documents`, archive routing note만 갱신한다.
- runtime premise 변경은 current replacement 문서, README index, archive Tombstone, 검증 게이트 순서로 반영하고 old 문서를 활성 실행계약처럼 보존하지 않는다.
- 운영 정책은 controls/evidence를 소유하고, 실행 명령 순서와 복구 절차는 guide/runbook template로 라우팅한다.
- stage-specific lifecycle 보강은 required headings, status/currentness notes, verification, handoff/limitations, rollout/rollback/follow-up, troubleshooting signatures처럼 기존 문서에 안전하게 추가 가능한 섹션을 우선한다.

## Support Contract Index

`support/`는 템플릿 양식 자체가 아니라 템플릿 체계의 contract,
governance, routing, frontmatter schema, legacy cleanup rule을 소유한다.

| Support Document | Responsibility |
| --- | --- |
| [Documentation Contract](./support/documentation-contract.md) | Template forms, support contracts, Stage 00 governance, authored docs의 소유 경계를 분리한다. |
| [SDLC Governance](./support/sdlc-governance.md) | PRD부터 postmortem까지 SDLC template family의 역할과 검증 경계를 정의한다. |
| [Common Documentation Governance](./support/common-documentation-governance.md) | README, Reference, Archive, Memory, Progress template family의 역할을 정의한다. |
| [Frontmatter Schema](./support/frontmatter-schema.md) | 현재 canonical frontmatter profile model을 정의한다. |
| [Template Routing](./support/template-routing.md) | 현재 `templates/**` route와 folder family를 정의한다. |
| [Legacy Cleanup Rules](./support/legacy-cleanup-rules.md) | active legacy template, key, value, section, route cleanup 대상을 정의한다. |

## Link Basis

이 README의 링크 기준 위치는 `docs/99.templates/`다.

- 템플릿 안의 실제 Markdown 링크는 `docs/99.templates/` 기준으로도 resolve되어야 한다.
- 최종 authored 문서 예시 경로는 해당 Target 위치 기준의 code literal로 작성한다.
- 아직 존재하지 않는 optional 문서, placeholder 경로, target-relative 예시는 Markdown 링크가 아니라 backtick code literal로 남긴다.
- 생성 문서에 템플릿 안내 주석, placeholder, target-path 주석, template-use 문구를 남기지 않는다.
- Spec 문서의 `Related Inputs`는 upstream 입력 요약이고, 필수
  `Related Documents` 섹션은 upstream/downstream 추적 링크를 함께 유지한다.
- 모든 README는 `Link Basis`와 `Related Documents`를 사용한다. Deprecated related-document headings는 새 README나 정리된 README에 남기지 않는다.

## Template-Folder Mapping

| Target Pattern                                                           | Template Path                                                              | Responsibility                                                          |
| ------------------------------------------------------------------------ | -------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| Registry `readme/repository` routes                                     | `templates/common/readme-repository.template.md`                           | Repository purpose, map, setup, validation, and owner links             |
| Registry `readme/stage-index` routes                                    | `templates/common/readme-stage-index.template.md`                          | Stage contract, contained-document index, and authoring handoff          |
| Registry `readme/collection-index` routes                               | `templates/common/readme-collection-index.template.md`                     | Collection scope, item inventory, and add/find workflow                  |
| Registry `readme/implementation` routes                                 | `templates/common/readme-implementation.template.md`                       | Component structure, configuration, validation, and operations          |
| Registry `readme/snapshot-pack` routes                                  | `templates/common/readme-snapshot-pack.template.md`                        | Snapshot boundary, report index, refresh, succession, and evidence      |
| Registry `readme/workspace-staging` routes                              | `templates/common/readme-workspace-staging.template.md`                    | Temporary non-secret staging, promotion, cleanup, and tracking          |
| Detached compatibility form; no authored route; removal owner RWP-006   | `templates/common/readme.template.md`                                      | Bounded transition state only                                           |
| `docs/01.requirements/<###-Numbering>-<feature-or-system>.md`                 | `templates/sdlc/requirements/prd.template.md`                              | Product requirements, users, scope, success / acceptance criteria       |
| `docs/02.architecture/requirements/####-<system-or-domain>.md`           | `templates/sdlc/architecture/ard.template.md`                              | Architecture requirements, quality attributes, reference model          |
| `docs/02.architecture/decisions/####-<short-title>.md`                   | `templates/sdlc/architecture/adr.template.md`                              | One architecture decision, context, consequences, alternatives          |
| `docs/03.specs/<###-Numbering>-<feature-id>/spec.md`                                     | `templates/sdlc/specs/spec.template.md`                                    | Parent implementation contract, interfaces, verification                |
| `docs/03.specs/<###-Numbering>-<feature-id>/api-spec.md`                                 | `templates/sdlc/specs/api-spec.template.md`                                | Feature-local API contract                                              |
| `docs/03.specs/<###-Numbering>-<feature-id>/agent-design.md`                             | `templates/sdlc/specs/agent-design.template.md`                            | Feature-local AI agent behavior, orchestration, safety, and eval design |
| `docs/03.specs/<###-Numbering>-<feature-id>/data-model.md`                               | `templates/sdlc/specs/data-model.template.md`                              | Feature-local logical and physical data model                           |
| `docs/03.specs/<###-Numbering>-<feature-id>/tests.md`                                    | `templates/sdlc/specs/tests.template.md`                                   | Feature-local test and evaluation strategy                              |
| `docs/03.specs/<###-Numbering>-<feature-id>/contracts/openapi.yaml`                      | `templates/sdlc/specs/openapi.template.yaml`                               | Feature-local OpenAPI contract                                          |
| `docs/03.specs/<###-Numbering>-<feature-id>/contracts/schema.graphql`                    | `templates/sdlc/specs/schema.template.graphql`                             | Feature-local GraphQL schema contract                                   |
| `docs/03.specs/<###-Numbering>-<feature-id>/contracts/service.proto`                     | `templates/sdlc/specs/service.template.proto`                              | Feature-local gRPC/protobuf contract                                    |
| `docs/04.execution/plans/YYYY-MM-DD-<feature>.md`                        | `templates/sdlc/execution/plan.template.md`                                | Execution order, risk control, rollout, verification                    |
| `docs/04.execution/tasks/YYYY-MM-DD-<feature-or-stream>.md`              | `templates/sdlc/execution/task.template.md`                                | Implementation and validation task evidence                             |
| `docs/05.operations/guides/####-<topic>.md`                              | `templates/sdlc/operations/guide.template.md`                              | Stable-state user, developer, or operator guidance                      |
| `docs/05.operations/policies/####-<policy-or-standard>.md`               | `templates/sdlc/operations/policy.template.md`                             | Operational policy, controls, boundaries                                |
| `docs/05.operations/runbooks/####-<topic>.md`                            | `templates/sdlc/operations/runbook.template.md`                            | Executable operational procedure and recovery path                      |
| `docs/05.operations/incidents/YYYY/INC-###-<title>/INC-###-<title>.md`   | `templates/sdlc/operations/incident.template.md`                           | Incident fact record and timeline                                       |
| `docs/05.operations/incidents/YYYY/INC-###-<title>/postmortem.md`        | `templates/sdlc/operations/postmortem.template.md`                         | Incident analysis and prevention follow-up                              |
| `docs/90.references/<category>/<topic>.md`                               | `templates/common/reference.template.md`                                   | Reference material, glossary, appendix, inventory                       |
| `docs/98.archive/**/*.md`                                                | `templates/common/archive-tombstone.template.md`                           | Tombstone metadata for old docs moved out of active stages              |
| `docs/00.agent-governance/memory/<topic>.md`                             | `templates/common/memory.template.md`                                      | Stable memory entry                                                     |
| `docs/00.agent-governance/memory/progress.md`                            | `templates/common/progress.template.md`                                    | Repo-changing work progress entry                                       |

The memory `<topic>` placeholder excludes `progress`; `progress.md` is an
exact reserved route owned by the progress template.

## Contract Template Placement

API 계약 문서는 별도 top-level docs 유형이 아니라 `03.specs/` 아래에서 사용하는 하위 템플릿이다.

- 올바른 위치: `docs/03.specs/<###-Numbering>-<feature-id>/api-spec.md`
- 잘못된 패턴: `docs/api/...`

OpenAPI, GraphQL, proto 같은 계약 파일은 관련 `docs/03.specs/<###-Numbering>-<feature-id>/` 문맥에서 추적성을 유지한다.

## Structural Template Coverage

구조적 템플릿 누락은 문서가 canonical stage 아래에 있으나 어떤 템플릿 매핑에도 포함되지 않는 상태를 뜻한다.
비-README authored Markdown은 아래 조건을 모두 만족해야 한다.

- `docs/99.templates/support/template-routing.md`와 이 README의 Template-Folder Mapping에 target pattern과 template이 있어야 한다.
- `scripts/validate-repo-quality-gates.sh`의 structural template mapping에 같은 target pattern과 template이 있어야 한다.
- 한 문서는 정확히 하나의 mapping, 즉 exactly one mapping에만 매칭되어야 한다.
- 매핑된 템플릿 파일은 `docs/99.templates/`에 존재해야 한다.
- 문서는 매핑된 템플릿의 required template headings와 `## Related Documents` 계약을 유지해야 한다.

## Reference and Memory Rules

`reference.template.md`는 `90.references/` 문서의 역할과 freshness를 강제한다.

- 모든 reference 문서는 `Reference Type`을 명시한다.
- Reference Type은 `version-contract-inventory`, `external-standard-snapshot`,
  `durable-concept`, `data-catalog`, `source-ledger`, `learning-roadmap`,
  `glossary`, `faq`, `dated-implementation-audit` 중 하나 또는 호환되는
  조합으로 작성한다.
- 모든 reference 문서는 `Authority Boundary`에서 소유하는 사실과 소유하지 않는 실행계약을 분리한다.
- 외부 기준이나 버전 snapshot은 `Review and Freshness`에 검토일과 갱신 trigger를 남긴다.
- repo-changing agent work의 진행 상황은 `progress.template.md` 구조로 `00.agent-governance/memory/progress.md`에 작성한다.
- `00.agent-governance/memory/`에 standalone memory 파일을 만들거나 갱신할 때는 `memory.template.md`를 사용한다.
- standalone memory 파일 변경은 같은 변경 단위에서 `progress.md` entry를 함께 남긴다.

## Archive Tombstone Rules

`archive-tombstone.template.md`는 `98.archive/` 문서의 metadata-only 본문을 강제한다.

- archive 경로는 원래 `docs/` 하위 경로를 `docs/98.archive/<original-docs-subpath>`로 mirror한다.
- Tombstone 본문은 원문을 보존하지 않고 original path, archived date, reason, replacement, implementation evidence, archive index link만 남긴다.
- 활성 문서는 Tombstone에 직접 연결하지 않고 [`../98.archive/README.md`](../98.archive/README.md)를 통해서만 archive를 노출한다.

## README and Spec Helper Templates

각 폴더 README도 반복적으로 재사용되는 문서 유형이므로 별도 README 템플릿을 함께 제공한다.
`03.specs/<###-Numbering>-<feature-id>/` 아래에서 반복적으로 사용하는 보조 설계 문서와 계약 파일용 템플릿을 함께 제공한다.

- `readme.template.md`는 repository root, `docs/README.md`, stage README, nested README에서 재사용되는 multi-target 템플릿이다. 단일 `Target:` 주석을 강제하지 않고, 최종 README 위치에서 상대 링크를 다시 계산한다.
- 모든 README는 `Overview`, `Audience`, `Scope`, `Structure`, `How to Work in This Area`, `Link Basis`, `Related Documents`를 유지한다.
- `docs/03.specs/<###-Numbering>-<feature-id>/README.md`는 필수가 아니다. 기본 인덱스는 `docs/03.specs/README.md`가 소유하며, feature-local README는 API/agent/data/test 보조 문서가 늘어날 때만 만든다.
- `openapi.template.yaml`, `schema.template.graphql`, `service.template.proto`는 형식상 YAML/GraphQL/proto 파일이므로 frontmatter 없이 owner comments와 parent API spec 링크로 추적성을 유지한다.
- `memory.template.md`는 `docs/00.agent-governance/memory/<topic>.md` target family를 사용한다. 관련 progress 링크는 최종 memory 파일 위치 기준으로 계산한다.
- `progress.template.md`는 `docs/00.agent-governance/memory/progress.md`에 append되는 entry 템플릿이다. entry 안의 링크는 `docs/00.agent-governance/memory/` 기준으로 계산한다.
- Required template headings는 template 파일의 literal `##` heading에서
  계산하며, placeholder가 있거나 optional/if-applicable로 표시된 heading은
  필수 heading에서 제외한다.

## Related Documents

- [Docs README](../README.md)
- [Agent Governance Hub](../00.agent-governance/README.md)
- [Documentation Protocol](../00.agent-governance/rules/documentation-protocol.md)
- [Stage Authoring Matrix](../00.agent-governance/rules/stage-authoring-matrix.md)
- [Template Support Contracts](./support/README.md)
