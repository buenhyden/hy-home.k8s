# 99.templates

> repo-authored 문서와 README가 시작해야 하는 canonical template stage다.

> [!NOTE]
> All AI agent interactions with this stage must comply with the [Agent Governance Hub](../00.agent-governance/README.md).

## Overview

이 경로는 직접 복사 가능한 form과 사람을 위한 authoring guidance를 함께 제공한다. 정확한 경로, profile, frontmatter, 상태, heading, lifecycle,
relationship, template 연결은
[Document Profile Registry](./registry.json)가 단독으로 소유한다.
README는 해당 machine contract를 복제하지 않고 사람이 올바른 소유자를 찾도록
안내한다.

## Stage Contract

### Responsibility Boundary

| Surface | Role | Canonical owner |
| --- | --- | --- |
| Machine contract | 경로를 정확히 하나의 profile과 form으로 분류하고 lifecycle edge를 검증한다. | [Document Profile Registry](./registry.json)와 [`contracts/`](./contracts/)의 두 schema |
| Human guidance | profile을 고르고 안전하게 작성·검증·복구하는 방법을 설명하며 machine authority가 아니다. | 이 README |
| Forms | 작성자가 복사한 뒤 topic-specific 사실과 증거로 채우는 최소 구조를 제공한다. | [`templates/`](#form-family-inventory) |
| Authored documents | 요구, 결정, 명세, 실행, 운영, 참조, 보존 증거를 소유한다. | `docs/01.requirements`부터 `docs/05.operations`, `docs/90.references`, `docs/98.archive` |

이 stage는 실제 PRD, AD, ADR, Spec, Plan, Task, 운영 기록이나 기능별 구현
계약을 소유하지 않는다. Form에는 재사용 가능한 구조만 두고, 공통 규칙은 이 README
또는 Stage 00 governance로 돌려보낸다.

### Form Family Inventory

Form directory 이름은 stage를, 파일 이름은 그 form이 만드는 문서 kind를 말한다.
Profile ID는 같은 사실을 `<family>/<kind>`로 표현한다.

- **Common forms** (`common/`): 저장소의 다섯 entrypoint 종류가 공유하는 README
  form. `readme-repository`는 repository entrypoint(`README.md`),
  `readme-stage-index`는 documentation entrypoint(`docs/README.md`)와 각 stage
  entrypoint, `readme-collection-index`는 stage 안의 package·collection
  entrypoint, `readme-implementation`과 `readme-workspace-staging`은
  runtime-governance entrypoint 중 구현 표면과 workspace staging,
  `readme-runtime-governance`는 provider 런타임이 직접 읽는 제어 표면
  (`.github/README.md`)을 담당한다. 모두 frontmatter가 없고 heading contract만
  가진다.
- **Governance forms** (`governance/`): Stage 00의 여섯 owner kind에 각각
  `contract`, `control`, `provider`, `role`, `rule`, `skill` form이 대응한다.
  `governance/*` profile은 `artifact_id`를 선언하지 않는다.
- **Core SDLC forms**: `requirements/requirement-package`,
  `architecture/description`, `architecture/decision`, `specs/spec`,
  `specs/plan`, `specs/task`가 단계별 책임과 handoff를 기록한다.
- **Spec contract forms** (`specs/contracts/`): `data-model` Markdown form과
  OpenAPI, GraphQL, protobuf native form. Native form 3종의 authored
  destination은 `docs/03.specs/####-<slug>/contracts/`이고, data model은
  package 루트의 `data-model.md`다. Form 쪽에서는 Spec이 소유하는 계약을 한
  디렉터리로 모은다.
- **Operations forms** (`operations/`): `guide`, `policy`, `runbook`,
  `incident`, `postmortem`의 서로 다른 운영 증거 책임을 유지한다.
- **Reference forms** (`references/`): Stage 90 collection 세 곳은 모두 같은 3단
  구조를 갖는다. collection router `{audits,data,research}/README.md`는
  `common/readme-collection-index` form을, pack router
  `####-<slug>/README.md`는 `audit-pack`·`data-pack`·`research-pack` form을,
  pack member `####-<slug>/m####-<slug>.md`는 같은 family의
  `audit-reference`·`data-reference`·`research-reference` form을 사용한다.
- **Archive forms** (`archive/`): `migration` control과 `tombstone` record.
- **Runtime forms** (`runtime/`): provider가 직접 읽는 binding만 담는다.
  Claude는 `claude-agent.template.md`, Codex는 `codex-agent.template.toml`이며
  두 form은 provider 소유 key(`name`/`description`/`model`/
  `model_reasoning_effort`/`tools`)만 가지고 guided 문서 key는 갖지 않는다.
  provider-neutral `.agents/`는 binding이 아니므로 form을 갖지 않는다.

현재 physical form의 전체 목록과 각각의 소유 profile은 README나 support prose가
아니라 registry와 repository quality gate에서 계산한다.

## Document Index

```text
99.templates/
├── contracts/          # machine contracts and their schemas
│   ├── document-profile.schema.json
│   └── frontmatter.schema.json
├── templates/          # copyable forms only
│   ├── common/ governance/ requirements/ architecture/
│   ├── specs/ (+ specs/contracts/)
│   └── operations/ references/ archive/ runtime/
├── registry.json
└── README.md
```

- [Document Profile Registry](./registry.json)
- [Template Forms](./templates/)

## Authoring Workflow

1. **Classify**: repository-relative target path를 registry로 분류하고 정확히 하나의
   profile이 선택되는지 확인한다.
2. **Copy**: 선택된 profile의 canonical form을 복사한다. 이웃 파일명이나 README
   목록으로 form을 추측하지 않는다.
   Stage 90 pack은 반드시 `audits|data|research/####-<slug>/` 아래에서
   category와 일치하는 pack form을 선택한다.
3. **Author**: 모든 prompt와 placeholder를 제거하고, 각 section을 문서의 topic에
   맞는 조사 결과, 결정, 링크, 검증 증거로 채운다. 상대 링크는 최종 target
   위치에서 다시 계산한다.
4. **Validate**: registry, Markdown profile, link/owner 검증과 repository quality
   gate를 실행하고 repo-static 결과와 remote/live 결과를 구분해 기록한다.

Template 선택은 registry profile ID를 따른다. lifecycle·supersession·retention·archive는
profile schema와 Stage 00 authoring policy를 따른다.
README는 frontmatter-free이며 선택된 README profile의 heading contract만 따른다.
Template은 frontmatter의 `type` 값으로 registry profile ID를 소비하며 실제
작성 destination path를 hardcode하지 않는다.

### Shared Frontmatter Grammar

`type`과 `status`는 profile이 고정한 값이고, 나머지 공통 key는 form에서
placeholder로 제공된다.

| Key | 필수 | Grammar | Template placeholder |
| --- | --- | --- | --- |
| `title` | 항상 | 문서 이름. `artifact_id`를 반복하지 않는다. | `'{...}'` |
| `version` | 항상 | `<major>.<minor>.<patch>` | `"#.#.#"` |
| `type` | 항상 | `<family>/<kind>` = registry profile ID | 고정값 |
| `status` | 항상 | profile의 `statusDomain` 중 initial state | 고정값 |
| `owner` | 항상 | 책임 소유자 | `'{owner}'` |
| `updated` | 항상 | ISO date | `YYYY-MM-DD` |
| `layer` | 번호가 붙은 stage 문서만 | 숫자 접두어가 없는 stage slug (`specs`, `operations`, …) | 없음 |
| `artifact_id` | 식별자를 가진 profile만 | profile의 `artifactIdPattern` | `"AD-####"` 형태 |

값 문법은 [`contracts/frontmatter.schema.json`](./contracts/frontmatter.schema.json)이,
profile별 required·allowed·order는 [`registry.json`](./registry.json)이 소유한다.

Form은 자신이 만드는 문서가 아니므로 그 문서의 식별자도, 그 문서가 살게 될
layer도 갖지 않는다. Stage 00 governance 문서 역시 번호가 붙은 stage에 속하지
않으므로 `layer`를 선언하지 않으며, `governance/*`는 `artifact_id`도 갖지 않는다.
`archive/tombstone`은 sealed envelope 전용 key를 추가로 갖는다.

## Related Documents

- [Docs README](../README.md)
- [Agent Governance Hub](../00.agent-governance/README.md)
- [Document Authoring Policy](../00.agent-governance/policies/document-authoring.md)
