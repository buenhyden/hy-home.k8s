---
title: "99.templates"
version: "0.19.0"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-11-12"
layer: "templates"
---
# 99.templates

> repo-authored 문서와 README가 시작해야 하는 canonical template stage다.

## Overview

이 경로는 직접 복사 가능한 form과 사람을 위한 authoring guidance를 함께 제공한다. 정확한 경로, profile, frontmatter, 상태, heading, lifecycle,
relationship, template 연결은
[Document Profile Registry](./registry.json)가 단독으로 소유한다.
README는 해당 machine contract를 복제하지 않고 사람이 올바른 소유자를 찾도록
안내한다.

Registry의 `shared_contract`는 buenhyden이 정확한 원본에 대해 승인한
`WGOV-CORE / 3.0.0`과 이 저장소의 지역 adapter를 식별한다. 공동
정본의 입구는 Project-Template의 기존 `.agents/governance/standards.md`다.
그 소스 묶음은 Project-Template 원본의 Stage 00·99, QA·Git·harness·모델·환경
정책, handoff prompt와 Skill을 포함한 67개 저장소 상대 경로다. 이 저장소에는
Stage 00이 없으며 그 지역 소유자는 `.agents/`다. digest는 중복 없는 경로를 UTF-8
순서로 정렬하고 각 경로 bytes·NUL·해당 Git blob 원문 bytes를 SHA-256에
차례로 넣어 계산한다. blob 뒤에는 별도 NUL을 넣지 않는다.

공동 승인 `approval_ref`는 Registry `shared_contract`가 소유하며, 이전 검증 근거는
Git history에서 복구한다.

현행 지역 언어 확장에서는 `.agents/governance/` 정책을 영어로 작성한다.
그 밖의 `.agents/` governed Markdown에는 새 설명을 한국어로 작성하며 기존
영어 본문도 유효하다. Registry가 요구하는
heading과 native key, 명령·인용·원시 증거는 원문을 유지한다. `.agents/`의
JSON·YAML 등 비 Markdown 파일과 `.codex/`·`.claude/`의 native 문서는
영어 전용이다. README는 해당 navigation profile을 따른다.
`docs/01.requirements`~`docs/03.specs`의 non-README 본문은 계속 영어다.
공통 Governance form의 기계 field·heading과 영어 author prompt는 유지하고,
복사해 작성한 `.agents/` 본문의 새 설명에 위 지역 규칙을 적용한다. 이 언어
확장과 아래의 Task 최초 기록·Spec/Plan 직접 전이·조건부 최초 승인 확장은 각각 하나만으로 승인된
WGOV-CORE 3.0.0의 새 판본이나 전체 지역 채택을 뜻하지 않는다.

## Scope

### Responsibility Boundary

| Surface | Role | Canonical owner |
| --- | --- | --- |
| Machine contract | 경로를 정확히 하나의 profile과 form으로 분류하고 lifecycle edge를 검증한다. | [Document Profile Registry](./registry.json)와 [`contracts/`](./contracts/)의 두 schema |
| Human guidance | profile을 고르고 안전하게 작성·검증·복구하는 방법을 설명하며 machine authority가 아니다. | 이 README |
| Forms | 작성자가 복사한 뒤 topic-specific 사실과 증거로 채우는 최소 구조를 제공한다. | [`templates/`](#physical-form-inventory) |
| Authored documents | 요구, 결정, 명세, 실행, 운영, 참조를 소유한다. | `docs/01.requirements`부터 `docs/05.operations`, `docs/90.references` |

이 stage는 실제 PRD, AD, ADR, Spec, Plan, Task, 운영 기록이나 기능별 구현
계약을 소유하지 않는다. Form에는 재사용 가능한 구조만 두고, 공통 규칙은 이 README
또는 `.agents/governance`의 공통 정책으로 돌려보낸다.

### Physical Form Inventory

Form directory는 사람이 form을 찾도록 physical responsibility surface별로 묶는다.
파일 이름은 form이 만드는 문서 kind를 나타내지만, directory 이름은 Registry
profile family를 정의하지 않는다. 예를 들어 `templates/specs/plan.template.md`는
그 경로를 유지하면서 `sdlc/plan` profile의 form으로 연결된다. 정확한 profile ID와
form 경로의 대응은 Registry만 소유한다.

- **Common forms** (`common/`): governed navigation README는 순서가 고정된
  여섯 key 봉투와 `type: "common/readme"`, `status: "active"`, 별도 artifact
  identity 없는 `Overview`/`Scope`/`Structure`/`Usage`/`Related Documents` core를
  공유한다. 저장소·stage·collection·implementation·workspace form과 선택 module은
  경로별 Registry profile이 고른다. stage·collection index form은 `updated` 뒤에
  `layer`를 더한다. README는 사람 독자만을 대상으로 한다. 폴더의 agent 지시는 그
  폴더의 `AGENTS.md`에 두며, 이는 frontmatter와 form이 없는 native
  `common/folder-agents-guide` 파일이다. 루트 `AGENTS.md`와 `CLAUDE.md`는
  `common/root-provider-shim` gateway로 유지한다.
- **Governance forms** (`governance/`): 공통 SDLC 계약, provider note, 역할,
  정책, 워크플로, 지식 지도, 프롬프트 계약에 `contract`, `provider`, `role`,
  `rule`, `skill`, `knowledge`, `prompt` form이 대응한다. 공통 소유자는
  `.agents`에, provider note는 `.claude/provider.md`와
  `.codex/provider.md`에 둔다. `governance/skill`은 두 flat workflow의
  생명주기 있는 문서 타입이며 native skill package와 구별한다.
  `governance/knowledge`는 `.agents/knowledge/`의 포인터 문서를,
  `governance/vocabulary`는 그 안의 `glossary.md` 용어 정의 문서 하나를,
  `governance/prompt`는 `.agents/prompts/`의 요청 계약을 소유하며 두 surface의
  README는 공통 router profile로 해석한다.
  `governance/*`는 기존 path/role identity를 유지한다. 기존 optional
  `artifact_id`가 있으면 보존하며 표준화만을 위해 새 ID를 만들지 않는다.
- **Evaluation evidence forms** (`evaluations/`): `task`, `score`, `results`
  form은 `.agents/evaluations/`의 선언, 한 쌍의 실제 관측에 대한 점수,
  집계 문서에 각각 대응한다. 각 harness directory는 하나의 paired trial이며
  재평가는 새 cycle ID와 directory를 사용한다. `baseline.md`와
  `with-skill.md`는 frontmatter나 Markdown wrapper를 요구하지 않는 원시
  출력이다. Registry는 경로와 작성 형식을 검사하며 점수의 진실성이나
  provider 실행을 인증하지 않는다. 원시 출력은 format hook과 lint의
  정확한 출력 경로에서만 제외하고 비밀·크기·파일 안전 검사는 유지한다.
- **Core SDLC forms**: physical `requirements/`, `architecture/`, `specs/`
  grouping은 `sdlc/requirement`, `sdlc/architecture-description`,
  `sdlc/architecture-decision`, `sdlc/spec`, `sdlc/plan`, `sdlc/task` profile의
  form을 담아 단계별 책임과 handoff를 기록한다.
- **Spec forms** (`specs/`): `spec`, `plan`, `task` form이 요구 추적,
  실행 계획, 작업 증거를 소유한다. 별도 data-model 및 native contract
  capacity는 현재 consumer가 없어 Spec 본문과 실제 구현 소유자에게 수렴했다.
- **Operations forms** (`operations/`): `guide`, `policy`, `runbook`,
  `incident`, `postmortem`의 서로 다른 운영 증거 책임을 유지한다.
  Guide는 Registry form을 쓰며 분류·독자·목표는 `Purpose`,
  `Lifecycle Traceability` 관계 표는 `Verification` 아래에 둔다.
  Policy의 적용 대상·통제·검토, Runbook의 트리거·절차·검증·복구는
  해당 역할의 core에 배치한다. Policy와 Runbook의 기존
  `Lifecycle Traceability` 관계 표는 각 역할 package 전까지
  `Related Documents` 아래에서 같은 source·열·상호 참조 의미를 유지한다.
  기계가 읽는 정확한 heading과 순서·내용 경계는 Registry가 소유한다. 빈 heading이나
  placeholder만 채운 항목은 실질 내용이 아니며, 형식 PASS는 live 증거가 아니다.
- **Reference forms** (`references/`): Stage 90 collection 세 곳은 모두 같은 3단
  구조를 갖는다. collection router `{audits,data,research}/README.md`는
  `common/readme` type으로, pack anchor
  `####-<slug>/README.md`는 `reference/audit-pack`·`reference/data-pack`·`reference/research-pack` form을,
  pack member `####-<slug>/m####-<slug>.md`는 같은 family의
  `reference/audit`·`reference/data`·`reference/research` form을 사용한다.
- **Runtime forms** (`runtime/`): provider가 직접 읽는 binding만 담는다.
  Claude는 `claude-agent.template.md`와 `claude-command.template.md`, Codex는
  `codex-agent.template.toml`이며 이 form들은 provider 소유
  key만 가지고 guided 문서 key는 갖지 않는다. Claude agent는
  `name`/`description`/`model`/`effort`/`tools`, Codex agent는
  `name`/`description`/`model`/`model_reasoning_effort`/`sandbox_mode`/`developer_instructions`,
  command는 `description`/`argument-hint`/`allowed-tools`다. `.claude/commands/*.md`는
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
| [AGENTS.md](./AGENTS.md) | 이 stage에 적용되는 AI 에이전트 지시 |
| [CLAUDE.md](./CLAUDE.md) | Claude가 이 stage의 `AGENTS.md`를 불러오게 하는 한 줄 `@AGENTS.md` import |

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

Template 선택은 Registry profile ID를 따른다. lifecycle, supersession
의무는 `.agents/governance`가 설명하고 정확한 machine 값은
Registry가 소유한다. Governed README도 공통 envelope를 사용하지만
"artifact_id"와 lifecycle binding은 없으며, "status: active"는 router
constant다. Template은 실제 destination path를 hardcode하지 않는다.
Spec은 변경 계약과 수용 기준을, Plan은 실행 순서와 위험·예정 검증을
소유한다. 새 Spec·Plan의 `approved`는 현재 계약의 승인·유효성을 뜻하며
구현 완료를 뜻하지 않는다. Task의 단일 Task Table은 실행 상태·결과와
증거 포인터를 기록하고, Criterion Acceptance 표가 기준별 수용 판정의
유일한 작성 원본이다. Task Evidence는 검사 사실을 보존한다. 기존 완료
Spec·Plan·Task는 당시의 `completed`와 승인·검사 근거를 소급 변경하지 않는다.
새로 작성하거나 현행 내용을 바꾸는 Plan은 승인된 Spec의 제약을
`Global Constraints`에서 연결하고 Plan에만 필요한 추가 실행 제약을 적으며,
지속 계약의 실제 현행 소유자와 위치를 `Promotion`에 기록한다. 완료 판정에서는
이 표가 유일한 승격 기록이며, 승격 대상이 없으면
`none | none | No durable contract was introduced` 한 행만 명시한다.
Registry의 두 절은 과거 profile 호환을 위해 optional로 등록하고, 현행 Plan의
작성·완료 의무는 lifecycle reader가 선택한 입력에 대해 검사한다. Stage 99
형식 구현은 해당 형식을 위임하는 현행 정책 소유자를 가리킨다.

Plan, Task Table, Criterion Acceptance, Task Evidence 표의 열 이름과 순서, 수용
값 집합은 Registry의 `body_contract`가 소유하며 이 README는 복제하지 않는다.
`not-required`는 취소된 Task와 같은 package의 취소된 Spec에서 해당 기준의
실제 범위 변경과 승인 근거를 확인한 때만 쓴다. 두 취소 처분 모두 정확한
기준 ID를 명시하고 Task의 승인 참조는 해당 Spec 결정을 가리킨다. 후속
Task만 정하거나 활성·
완료·대체 Task로 끝내는 경우 기준 면제로 바꾸지 않는다. QA의
`NOT_APPLICABLE`는 검사 대상 판정으로 이 수용 값과 다르다.
`Required`는 `yes` 또는 `no`, `Resolves`는 `none` 또는 앞선 증거 ID를
쉼표와 공백으로 연결한다. `no`는 원래 검증 계획에서 비필수인 검사와
그 사유에만 쓰며 필수 실패를 사후 재분류하지 않는다. 필수
`FAIL`·`DEFER`·`NOT_RUN`은 같은 검사·작업
항목·기준의 뒤따르는 `PASS`가 이전 증거 ID를 명시해야 해소된다. 다른
PASS로 미해소 필수 결과를 숨기지 않는다. 완료 인계는 필수 기준의 Plan
배정, 실제 Task 완료, 구체적 PASS 증거, 단일 `accepted` 판정과 지속
의미의 현재 owner를 함께 확인한다. QA 결과, 기준 수용, 원본 승인,
통합과 보관은 서로의 대체값이 아니다. 취소·대체는 남은 필수 기준의
후속 Task의 Plan 배정을 명시하고, 관측 결과를 보존한다.
관측된 `FAIL`은 `PASS`처럼 구체적인 Check·Input·Location을 적는다.
`NOT_RUN`·`DEFER`에는 아직 실제 결과 위치가 없으면 `Pending`을 쓸 수
있지만 사유와 다음 owner를 남긴다.
resolved Incident에는 시간대를 포함한 실제 resolved_at과 해결 증거가 필요하다.

### Task Status Authoring

Task 행 상태와 frontmatter `status`의 작성법은
[Document Authoring Policy](../../.agents/governance/document-authoring.md)와
[Document Lifecycle Policy](../../.agents/governance/document-lifecycle.md)가,
Task 최초 기록이 허용하는 상태와 Spec·Plan의 direct approval·first-record
approval 예외는 Document Lifecycle Policy가 정본이다. 이 README는 그 규칙을
다시 적지 않는다. 지역 확장의 정확한 이름은 Registry
`shared_contract.extensions`에 있다.

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
| "layer" | profile이 stage/router layer를 소유할 때 | 숫자 접두어 없는 stage slug | profile literal; stage-index·collection-index README form은 "&#123;&#123;LAYER&#125;&#125;" |
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
Stage 98(`docs/98.archive/`)에는 profile과 form이 없다. 그 경로는 문서
inventory 밖이며 검증하지 않는다.

## Related Documents

- [Docs README](../README.md)
- [Agent Governance Hub](../../.agents/README.md)
- [Document Authoring Policy](../../.agents/governance/document-authoring.md)
