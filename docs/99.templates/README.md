---
title: "99.templates"
version: "0.7.0"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-10-05"
layer: "templates"
---
# 99.templates

> repo-authored 문서와 README가 시작해야 하는 canonical template stage다.

> [!NOTE]
> 이 stage에서 이루어지는 모든 AI 에이전트 작업은 [Agent Governance Hub](../../.agents/README.md)를 따른다.

## Overview

이 경로는 직접 복사 가능한 form과 사람을 위한 authoring guidance를 함께 제공한다. 정확한 경로, profile, frontmatter, 상태, heading, lifecycle,
relationship, template 연결은
[Document Profile Registry](./registry.json)가 단독으로 소유한다.
README는 해당 machine contract를 복제하지 않고 사람이 올바른 소유자를 찾도록
안내한다.

## Scope

### Responsibility Boundary

| Surface | Role | Canonical owner |
| --- | --- | --- |
| Machine contract | 경로를 정확히 하나의 profile과 form으로 분류하고 lifecycle edge를 검증한다. | [Document Profile Registry](./registry.json)와 [`contracts/`](./contracts/)의 두 schema |
| Human guidance | profile을 고르고 안전하게 작성·검증·복구하는 방법을 설명하며 machine authority가 아니다. | 이 README |
| Forms | 작성자가 복사한 뒤 topic-specific 사실과 증거로 채우는 최소 구조를 제공한다. | [`templates/`](#physical-form-inventory) |
| Authored documents | 요구, 결정, 명세, 실행, 운영, 참조, 보존 증거를 소유한다. | `docs/01.requirements`부터 `docs/05.operations`, `docs/90.references`, `docs/98.archive` |

이 stage는 실제 PRD, AD, ADR, Spec, Plan, Task, 운영 기록이나 기능별 구현
계약을 소유하지 않는다. Form에는 재사용 가능한 구조만 두고, 공통 규칙은 이 README
또는 `.agents/governance`의 공통 정책으로 돌려보낸다.

### Physical Form Inventory

Form directory는 사람이 form을 찾도록 physical responsibility surface별로 묶는다.
파일 이름은 form이 만드는 문서 kind를 나타내지만, directory 이름은 Registry
profile family를 정의하지 않는다. 예를 들어 `templates/specs/plan.template.md`는
그 경로를 유지하면서 `sdlc/plan` profile의 form으로 연결된다. 정확한 profile ID와
form 경로의 대응은 Registry만 소유한다.

- **Common forms** (`common/`): governed navigation READMEs share the ordered
  six-key envelope, `type: "common/readme"`, `status: "active"`, and the
  `Overview`/`Scope`/`Structure`/`Usage`/`Related Documents` core without a
  separate artifact identity. Path-specific registry profiles still choose the
  repository, stage, collection, implementation, and workspace forms and any
  optional module. The current Archive catalog has its own `archive/catalog`
  type and retains the catalog tables.
- **Governance forms** (`governance/`): 공통 SDLC 계약, provider note, 역할,
  정책, 워크플로, 지식 지도, 프롬프트 계약에 `contract`, `provider`, `role`,
  `rule`, `skill`, `knowledge`, `prompt` form이 대응한다. 공통 소유자는
  `.agents`에, provider note는 `.claude/provider.md`와
  `.codex/provider.md`에 둔다. `governance/skill`은 두 flat workflow의
  생명주기 있는 문서 타입이며 native skill package와 구별한다.
  `governance/knowledge`는 `.agents/knowledge/`의 포인터 문서를,
  `governance/prompt`는 `.agents/prompts/`의 요청 계약을 소유하며 두 surface의
  README는 공통 router profile로 해석한다.
  `governance/*`는 기존 path/role identity를 유지한다. 기존 optional
  `artifact_id`가 있으면 보존하며 표준화만을 위해 새 ID를 만들지 않는다.
- **Core SDLC forms**: physical `requirements/`, `architecture/`, `specs/`
  grouping은 `sdlc/requirement`, `sdlc/architecture-description`,
  `sdlc/architecture-decision`, `sdlc/spec`, `sdlc/plan`, `sdlc/task` profile의
  form을 담아 단계별 책임과 handoff를 기록한다.
- **Spec forms** (`specs/`): `spec`, `plan`, `task` form이 요구 추적,
  실행 계획, 작업 증거를 소유한다. 별도 data-model 및 native contract
  capacity는 현재 consumer가 없어 Spec 본문과 실제 구현 소유자에게 수렴했다.
- **Operations forms** (`operations/`): `guide`, `policy`, `runbook`,
  `incident`, `postmortem`의 서로 다른 운영 증거 책임을 유지한다.
- **Reference forms** (`references/`): Stage 90 collection 세 곳은 모두 같은 3단
  구조를 갖는다. collection router `{audits,data,research}/README.md`는
  `common/readme` type으로, pack anchor
  `####-<slug>/README.md`는 `reference/audit-pack`·`reference/data-pack`·`reference/research-pack` form을,
  pack member `####-<slug>/m####-<slug>.md`는 같은 family의
  `audit-reference`·`data-reference`·`research-reference` form을 사용한다.
- **Archive forms** (`archive/`): route disposition인 `route-tombstone`과
  `scope-migration`, 그리고 동결 generation의 `migration` 원장과 `tombstone` record.
  보존 단위에는 form이 없다. retention class는 원본 Git object를 그대로 옮긴다.
- **Runtime forms** (`runtime/`): provider가 직접 읽는 binding만 담는다.
  Claude는 `claude-agent.template.md`와 `claude-command.template.md`, Codex는
  `codex-agent.template.toml`이며 이 form들은 provider 소유
  key(`name`/`description`/`model`/`model_reasoning_effort`/`tools`,
  command는 `description`/`argument-hint`/`allowed-tools`)만 가지고 guided 문서
  key는 갖지 않는다. `.claude/commands/*.md`는
  `common/provider-native-command`로 분류하며 `.agents/prompts/`의 계약을
  호출하는 진입점일 뿐 계약 자체를 소유하지 않는다.
  `.agents/skills/<id>/SKILL.md`는 `common/native-skill-package` native
  profile로 분류하며 top-level `name`/`description`, 공통 여섯 key를 담는
  `metadata`, boolean `disable-model-invocation: true`를 사용한다. 문서
  봉투는 metadata 내부에만 두며 실제 native invocation/tool/model
  controls를 형식 정규화를 위해 바꾸지 않는다. 각 package의
  `agents/openai.yaml`은 Codex의 `policy.allow_implicit_invocation: false`를
  소유한다. 이 native sidecar와 Claude skill adapter의 정확한 집합은
  [agent validator](../../scripts/validate-agent-governance.py)가 검증한다.

현재 physical form의 전체 목록과 각각의 소유 profile은 README나 support prose가
아니라 registry와 repository quality gate에서 계산한다.

### Deliberately Empty Profiles

현재 record가 없는 것은 곧 사용하지 않는 capacity를 뜻하지 않는다.
`operation/incident`와 `operation/postmortem`은 사건 발생 전에도 운영 증거를
기록할 수 있도록 유지한다. `reference/audit`, `reference/data`,
`reference/audit-pack`, `reference/data-pack`은 현재 record가 0건이어도
Stage 90 collection contract가 요구하는 audit/data collection·pack 경로를
구조적으로 보장하므로 유지한다. 이는 이미 retired한 미사용 capacity와 구별한다.

## Structure

| Path | Purpose |
| --- | --- |
| [contracts/](./contracts/) | 기계 계약과 그 schema |
| [templates/](./templates/) | 복사해서 쓰는 form catalog |
| [registry.json](./registry.json) | Document Profile Registry |

이 README는 stage router다. 어떤 form이 어디에 있고 새 form을 어떻게 등록하는지는
[form catalog](./templates/README.md)가 소유한다.

## Usage

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
retention, Archive 의무는 `.agents/governance`가 설명하고 정확한 machine 값은
Registry가 소유한다. Governed README도 공통 envelope를 사용하지만
"artifact_id"와 lifecycle binding은 없으며, "status: active"는 router
constant다. Template은 실제 destination path를 hardcode하지 않는다.
Spec은 수용 기준을, Plan은 실행 순서를, Task의 단일 Task Table은 실행
상태·결과·증거를 기록한다. Task의 frontmatter `status`는 하나의 상태
표시이며, 여러 행의 상태와 일치하는지는 lifecycle validator가 Registry의
`task_execution` binding에 따라 읽기 전용으로 확인한다. 완료 인계는 필수
Spec 기준에서 Plan의 배정과 Task의 완료·PASS·accepted·구체적 증거까지
확인한다. Plan은 `Work Unit | Criteria | Work | Dependencies | Task | Verification`을,
Task는 `ID | Upstream criterion | Work item | Owner | Status | Result | Acceptance | Evidence`를,
Task Evidence는 `Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance`를
사용한다. Result, Acceptance, 실제 승인, 통합과 보관은 서로의 대체값이 아니다.
cancelled는 실제 이유·승인 원본 참조·필수 기준 처리 근거를 요구하고 관측 결과를
보존한다. resolved Incident에는 시간대를 포함한 실제 resolved_at과 해결 증거가 필요하다.

### Explicit Task Summary Authoring

다중 행 Task의 Status를 먼저 실제 관측에 맞게 작성한 뒤
[`sync-task-status.py`](../../scripts/sync-task-status.py)로 frontmatter 요약을
미리 확인할 수 있다. `TASK_PATH`에는 현재 저장소의 실제 `sdlc/task` 경로 하나를
설정한다.

```bash
python3 scripts/sync-task-status.py --root . --path "$TASK_PATH"
python3 scripts/sync-task-status.py --root . --path "$TASK_PATH" --write
```

첫 명령은 현재 값과 파생 값을 표시하는 읽기 전용 preview다. 두 번째 명령은
명시적으로 top-level `status` scalar만 동기화한다. 한 행 Task의 literal
`frontmatter` 표시는 그대로 두며 값이 이미 맞으면 파일을 다시 쓰지 않는다.
나머지 metadata, 본문, 행, 인용·주석·줄바꿈과 파일 mode는 보존한다.

현재 일반 파일과 안전한 부모 경로만 받고, Registry 분류·strict 문서 계약·
현재 상태에서 파생 상태로의 lifecycle edge를 확인한다. 잘못된 내용이나
불법 전이는 오류 ID와 대상 경로, exit 2로 거부한다. 쓰기 전 원본이 바뀌거나
원자적 교체가 실패하면 해당 원본을 보존한다. Result, Acceptance, Evidence와
실제 승인 사실은 관측에 따라 별도로 작성해야 한다. validator와 Git hook은
이 writer를 자동 호출하지 않는다.

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
| "updated" | 항상 | ISO date | "&#123;&#123;UPDATED&#125;&#125;" |
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
identity는 Registry contract version과 Git history가 소유한다.
README router에는 stable "artifact_id"가 없으며 reference pack anchor는
기존 AUD/RES/DATA identity와 게시 생명주기를 유지한다. governance에는 기존
optional identity만 보존한다.
"archive/tombstone"은 sealed envelope provenance key를 추가로 가진다.
현재 "archive/route"와 "archive/scope-migration" profile은 같은
"archive/route" type과 draft/sealed를 투영하며 본문 없이 각 route key만 가진다.
Registry의 "retention_classes"는 Stage 98 retention class마다 본문이 명명하는 대상과
허용하는 anchor 종단 상태를 묶는다. "retention_units"는 spec package와 Incident bundle을
보존 단위로, "retention_modes"는 profile마다 쓸 수 있는 보존 방식을, "archive_citation"은
Stage 98 인용을 판정하는 순서 있는 표를, "legacy_rebased_retained_paths"는 ADR-0038이
상대 링크를 재기준해 보존한 16개 본문을 선언한다.

## Related Documents

- [Docs README](../README.md)
- [Agent Governance Hub](../../.agents/README.md)
- [Document Authoring Policy](../../.agents/governance/document-authoring.md)
