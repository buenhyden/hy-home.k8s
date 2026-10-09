---
title: "99.templates"
version: "0.10.0"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-10-09"
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

Registry의 `shared_contract`는 buenhyden이 정확한 원본에 대해 승인한
`WGOV-CORE / 3.0.0`과 이 저장소의 지역 adapter 후보를 식별한다. 공동
정본의 입구는 Project-Template의 기존 `.agents/governance/standards.md`다.
그 소스 묶음은 Stage 00·99, QA·Git·harness·모델·환경 정책, handoff prompt와
Skill을 포함한 67개 저장소 상대 경로다. digest는 중복 없는 경로를 UTF-8
순서로 정렬하고 각 경로 bytes·NUL·해당 Git blob 원문 bytes를 SHA-256에
차례로 넣어 계산한다. blob 뒤에는 별도 NUL을 넣지 않는다.

검토용 `3.0.0-draft.8` 묶음의 실제 정상 commit은
`bc5b70556c57198768119f94c287f93c87964482`이고, 그 원본 blob digest는
Registry의 `sha256:aa2523943e35908ba24e4e415793f7aa8099de247aa3628ec1678cd6c91725ee`다.
별도 인증된 buenhyden 결정 `call_415633a444f34091860dcb4b8700431d/0`은
바로 이 commit·digest를 최종 `WGOV-CORE / 3.0.0`으로 승인했다. commit과
digest만으로 승인을 추론하지 않으며, 이 결정 참조가 판본 승인 근거다.
Project-Template native commit/정적 리뷰 통과는 그 원본 입력에 한정된다.

현재 Registry의 `stage: candidate`는 **이 k8s 지역 adapter의 채택이 아직
완료되지 않았다**는 뜻이다. Stage 99 계약에는 `candidate`와 `adopted`만
있으므로 공동 owner의 최종 승인과 지역 채택 상태를 혼동해 `adopted`로
승격하지 않는다. Project-Template의 P06 Git 소비자는 별도 commit
`10001e3c1f9b7aea3f2fda555e1a5dcf0a6dfbc3`에서 관측했다. 이전 k8s C07
Commitizen 문법 차이는 이번 지역 수정에서 원래 네 문장 재비교와 집중
회귀가 통과했다. 생성 메시지의 정확한 예외 형태, release parser와 PR
제목의 로컬 정적 경계도 확인했다. 수정된 21개 경로는 선택된 19개
검사를 모두 통과했고, 실제 commit 메시지의 고정 Commitizen·지역 형태
검사와 독립 소스 검토를 거쳐 `2a99a8bb25e4ffd521af89a3cf4e9dd7d66288bc`로
정상 commit된 뒤 동일 tree로 지역 `main`에 통합됐다. 이는 C07 지역
구현과 로컬 전달의 근거이며 공통 계약 전체의 지역 채택 판정은 아니다.
PR 제목의 GitHub Actions 실제 실행이나 PR SHA 결과는 관측하지 않았다.
다른 세 저장소와
네 저장소 공동 채택은 각자의 실제 adapter·
승인판본 적용 근거가 생긴 뒤 별도로 기록한다. Kubernetes의 Task 상태
요약·과거 완료 부모, 문서 언어와 native 문법은 명시된 지역 차이이며 별도
공동 정본을 뜻하지 않는다.

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
  Guide의 분류·독자·목표, Policy의 적용 대상·통제·검토,
  Runbook의 트리거·절차·검증·복구는 해당 역할의 core에 배치한다.
  기존 `Lifecycle Traceability` 관계 표는 세 역할의 `Related Documents`
  아래에서 같은 source·열·상호 참조 의미를 유지한다. 기계가 읽는 정확한
  heading과 순서·내용 경계는 Registry가 소유한다. 빈 heading이나
  placeholder만 채운 항목은 실질 내용이 아니며, 형식 PASS는 live 증거가 아니다.
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
Spec은 변경 계약과 수용 기준을, Plan은 실행 순서와 위험·예정 검증을
소유한다. 새 Spec·Plan의 `approved`는 현재 계약의 승인·유효성을 뜻하며
구현 완료를 뜻하지 않는다. Task의 단일 Task Table은 실행 상태·결과와
증거 포인터를 기록하고, Criterion Acceptance 표가 기준별 수용 판정의
유일한 작성 원본이다. Task Evidence는 검사 사실을 보존한다. 기존 완료
Spec·Plan·Task는 당시의 `completed`와 승인·검사 근거를 소급 변경하지 않는다.

Plan은 `Work Unit | Criteria | Work | Dependencies | Task | Verification`을,
Task Table은 `ID | Upstream criterion | Work item | Owner | Status | Result | Evidence`를,
Criterion Acceptance는 `Criterion | Acceptance | Evidence | Disposition | Current owner`를,
Task Evidence는 `Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves`를
사용한다. 수용 값은 `pending`·`accepted`·`rejected`·`not-required`다.
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
후속 Task의 Plan 배정을 명시한다. 기준 면제는 위의 Spec·Task 취소와
기준별 승인 근거가 있을 때만 기록하며, 관측 결과는 보존한다.
관측된 `FAIL`은 `PASS`처럼 구체적인 Check·Input·Location을 적는다.
`NOT_RUN`·`DEFER`에는 아직 실제 결과 위치가 없으면 `Pending`을 쓸 수
있지만 사유와 다음 owner를 남긴다.
resolved Incident에는 시간대를 포함한 실제 resolved_at과 해결 증거가 필요하다.

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

한 행 Task는 frontmatter만 사람이 작성하며, 다중 행 Task는 행 상태만 사람이
작성한다. 다중 행 frontmatter는 기존 소비자를 위한 생성 요약이므로 사람이
두 곳에 상태를 복사하지 않는다. `ready`는 실행 준비이지 별도 승인 단계가
아니다. `superseded`는 실제 후속 Task의 Plan 배정과 남은 기준의 귀속이 확인된 경우에만
사용하며, 상태만 바꿔 미완료 기준이나 실패를 지우지 않는다.

현재 일반 파일과 안전한 부모 경로만 받고, Registry 분류·strict 문서 계약·
현재 상태에서 파생 상태로의 lifecycle edge를 확인한다. 잘못된 내용이나
불법 전이는 오류 ID와 대상 경로, exit 2로 거부한다. 쓰기 전 원본이 바뀌거나
원자적 교체가 실패하면 해당 원본을 보존한다. Result, Criterion Acceptance,
Task Evidence와 실제 승인 사실은 관측에 따라 별도로 작성해야 한다. validator와 Git hook은
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

현재 Registry의 `spec-package`에만 적용되는 `completed_authority_members`는
`approved` Spec·Plan을 `completed/` 보존 후보로 볼 때 원본 비교 기준 Git tree의
두 권한 문서가 모두 `approved`이고, 같은 원본 package의 Task 완료·Plan 배정·
기준별 단일 `accepted`·필수 실패 해소·지속 의미 owner가 확인되도록 한다.
`approved` 표기만으로 보관하지 않으며 다른 보존 단위의 종단 상태를 완화하지
않는다. 지속 의미의 실제 승격, 현재 소비자 처분, 별도 보관 승인과 Retention
Envelope의 원본 path·mode·bytes 동일성도 필요하다. 검증기의 구조 PASS가
승인자나 운영 사실을 인증하지 않으며, 이 안내는 보관 이동을 실행하지 않는다.

## Related Documents

- [Docs README](../README.md)
- [Agent Governance Hub](../../.agents/README.md)
- [Document Authoring Policy](../../.agents/governance/document-authoring.md)
