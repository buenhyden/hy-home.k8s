---
title: "99.templates"
version: "0.1.0"
type: "common/readme-stage-index"
status: "active"
owner: "platform"
updated: "2026-09-04"
layer: "templates"
---
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

- **Common forms** ("common/"): governed README entrypoints share the ordered
  six-key envelope but receive no fake identity. "readme-repository" covers
  the repository entrypoint, "readme-stage-index" covers documentation and
  stage entrypoints, "readme-collection-index" covers package and collection
  entrypoints, and the implementation, workspace-staging, and
  runtime-governance forms cover their named runtime surfaces. Registry
  profiles own each router's exact path, fixed "type"/"status", optional
  "layer", and heading contract.
- **Governance forms** (`governance/`): Stage 00의 여섯 owner kind에 각각
  `contract`, `provider`, `role`, `rule`, `skill` form이 대응한다.
  `governance/*` profile은 `artifact_id`를 선언하지 않는다.
- **Core SDLC forms**: `requirements/requirement-package`,
  `architecture/description`, `architecture/decision`, `specs/spec`,
  `specs/plan`, `specs/task`가 단계별 책임과 handoff를 기록한다.
- **Spec forms** (`specs/`): `spec`, `plan`, `task` form이 요구 추적,
  실행 계획, 작업 증거를 소유한다. 별도 data-model 및 native contract
  capacity는 현재 consumer가 없어 Spec 본문과 실제 구현 소유자에게 수렴했다.
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

### Deliberately Empty Profiles

현재 record가 없는 것은 곧 사용하지 않는 capacity를 뜻하지 않는다.
`operation/incident`와 `operation/postmortem`은 사건 발생 전에도 운영 증거를
기록할 수 있도록 유지한다. `reference/audit`, `reference/data`,
`common/readme-audit-pack`, `common/readme-data-pack`은 현재 record가 0건이어도
Stage 90 collection contract가 요구하는 audit/data collection·pack 경로를
구조적으로 보장하므로 유지한다. 이는 이미 retired한 미사용 capacity와 구별한다.

## Document Index

```text
99.templates/
├── contracts/          # machine contracts and their schemas
│   ├── document-profile.schema.json
│   └── frontmatter.schema.json
├── templates/          # copyable forms only
│   ├── README.md       # form catalog
│   ├── common/ governance/ requirements/ architecture/
│   ├── specs/ (+ specs/contracts/)
│   └── operations/ references/ archive/ runtime/
├── registry.json
└── README.md
```

이 README는 stage router다. 어떤 form이 어디에 있고 새 form을 어떻게 등록하는지는
form catalog가 소유한다.

- [Document Profile Registry](./registry.json)
- [Form Catalog](./templates/README.md)

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

Template 선택은 Registry profile ID를 따른다. lifecycle, supersession,
retention, Archive 의무는 Stage 00 policy가 설명하고 정확한 machine 값은
Registry가 소유한다. Governed README도 공통 envelope를 사용하지만
"artifact_id"와 lifecycle binding은 없으며, "status: active"는 router
constant다. Template은 실제 destination path를 hardcode하지 않는다.

### Shared Frontmatter Grammar

모든 governed Markdown은 "title", "version", "type", "status", "owner",
"updated" 순서로 시작한다. 이후 "layer", "artifact_id", relationship,
supersession, provenance key는 선택된 profile의 order에만 따라 나타난다.
모든 string, date, version, ID scalar는 큰따옴표를 사용한다.

| Key | Presence | Grammar | Template value |
| --- | --- | --- | --- |
| "title" | 항상 | identity를 반복하지 않는 사람용 이름 | "&#123;&#123;TITLE&#125;&#125;" |
| "version" | 항상 | SemVer; 새 문서는 "0.1.0" | "0.1.0" |
| "type" | 항상 | Registry profile ID인 "family/kind" | profile literal |
| "status" | 항상 | profile lifecycle subset 또는 router constant | profile literal |
| "owner" | 항상 | 책임 소유자 | "&#123;&#123;OWNER&#125;&#125;" |
| "updated" | 항상 | ISO date | "&#123;&#123;YYYY_MM_DD&#125;&#125;" |
| "layer" | profile이 stage/router layer를 소유할 때 | 숫자 접두어 없는 stage slug | profile literal |
| "artifact_id" | stable identity profile만 | "artifact_id_pattern" | "&#123;&#123;ARTIFACT_ID&#125;&#125;" |

값의 scalar/array 문법은
[frontmatter schema](./contracts/frontmatter.schema.json)가, profile별
required, optional, forbidden, order, constant, lifecycle, identity pattern은
[Registry](./registry.json)가 소유한다. Markdown placeholder는
"&#123;&#123;UPPER_SNAKE_CASE&#125;&#125;", native placeholder는 `__UPPER_SNAKE_CASE__`,
author guidance는 "<!-- Author prompt: ... -->"만 사용한다.

Template은 만드는 문서의 envelope를 투영하므로 profile이 요구하는 "layer"와
"artifact_id" placeholder를 포함한다. Template 파일 자체의 revision과 destination
identity는 Registry contract version과 Git history가 소유한다. Stage 00
"governance/*"와 README router는 stable "artifact_id"를 갖지 않는다.
"archive/tombstone"은 sealed envelope provenance key를 추가로 가진다.

## Related Documents

- [Docs README](../README.md)
- [Agent Governance Hub](../00.agent-governance/README.md)
- [Document Authoring Policy](../00.agent-governance/policies/document-authoring.md)
