---
title: "99.templates"
version: "1.0.0"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-11-20"
---
# 99.templates

## 문서 개요

### 목적과 독자

이 README는 문서 양식을 고르는 작성자와 profile·validator를 유지하는 담당자에게 Stage 99의 정본 경로와 소비 순서를 안내한다. 양식 단계의 목적은 [Purpose](#purpose)에 기록한다.

### 책임과 적용 범위

platform은 Stage 99 양식 안내를 유지한다. Registry, schema, form의 소유 경계는 [Paths](#paths)와 [Owners](#owners), 작성·검증 소비 경로는 [Usage](#usage)와 [Checks](#checks)에 연결한다.

## 내용 계약

### 입력과 전제

입력과 전제는 아래 역할별 본문의 해당 절에 기록한다.

### 본문과 규칙

#### Responsibility

##### Purpose

> repo-authored 문서와 README가 시작해야 하는 canonical template stage다.

이 경로는 직접 복사 가능한 form과 사람을 위한 authoring guidance를 함께 제공한다. 정확한 경로, profile, frontmatter, 상태, heading, lifecycle,
relationship, template 연결은
[Document Profile Registry](./registry.json)가 단독으로 소유한다.
README는 해당 machine contract를 복제하지 않고 사람이 올바른 소유자를 찾도록
안내한다.

Registry의 `shared_contract`는 `WGOV-CORE / 3.0.0` 후보와 이 저장소의
지역 adapter를 식별한다. Registry의 현재 `stage`는 `candidate`이며,
기존 `approval_ref`와 고정된 revision·digest는 당시 검토 대상을 추적하는
근거다. 이것만으로 현행 공동 판본의 최종 승인, 이 저장소의 지역 채택이나
다른 workspace의 적용을 주장하지 않는다. 공동
정본의 입구는 Project-Template의 기존 `.agents/governance/standards.md`다.
그 소스 묶음은 Project-Template 원본의 Stage 00·99, QA·Git·harness·모델·환경
정책, handoff prompt와 Skill을 포함한 67개 저장소 상대 경로다. 이 저장소에는
Stage 00이 없으며 그 지역 소유자는 `.agents/`다. digest는 중복 없는 경로를 UTF-8
순서로 정렬하고 각 경로 bytes·NUL·해당 Git blob 원문 bytes를 SHA-256에
차례로 넣어 계산한다. blob 뒤에는 별도 NUL을 넣지 않는다.

기존 `approval_ref`는 Registry `shared_contract`가 소유하며, 이전 검증 근거는
Git history에서 복구한다. 현행 후보의 최종 결정과 지역 적용 증거는 해당 Task에서
별도로 확인한다.

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

###### Inputs and Outputs

입력과 출력: 해당 없음 — 이 stage README는 입력과 출력의 범위를 따로 나열하지 않는다.

##### Excluded Responsibilities

이 stage는 실제 PRD, AD, ADR, Spec, Plan, Task, 운영 기록이나 기능별 구현 계약을 소유하지 않으며, Form에는 재사용 가능한 구조만 둔다. 공통 규칙은 이 README 또는 `.agents/governance`의 공통 정책으로 돌려보내고, 정확한 경로, profile, frontmatter, 상태, heading, lifecycle, relationship, template 연결은 Document Profile Registry가 단독으로 소유하므로 README는 이 machine contract를 복제하지 않는다.

#### Current Contents

##### Paths

| Path | Purpose |
| --- | --- |
| [01.contracts/](./01.contracts/) | 기계 계약과 그 schema |
| [02.templates/](./02.templates/) | 복사해서 쓰는 form catalog |
| [registry.json](./registry.json) | Document Profile Registry |
| [AGENTS.md](./AGENTS.md) | 이 stage에 적용되는 AI 에이전트 지시 |
| [CLAUDE.md](./CLAUDE.md) | Claude가 이 stage의 `AGENTS.md`를 불러오게 하는 한 줄 `@AGENTS.md` import |

이 README는 stage router다. 어떤 form이 어디에 있고 새 form을 어떻게 등록하는지는
[form catalog](./02.templates/README.md)가 소유한다.

##### Owners

###### Responsibility Boundary

| Surface | Role | Canonical owner |
| --- | --- | --- |
| Machine contract | 경로를 정확히 하나의 profile과 form으로 분류하고 lifecycle edge를 검증한다. | [Document Profile Registry](./registry.json)와 [`01.contracts/`](./01.contracts/)의 네 schema |
| Human guidance | profile을 고르고 안전하게 작성·검증·복구하는 방법을 설명하며 machine authority가 아니다. | 이 README |
| Forms | 작성자가 복사한 뒤 topic-specific 사실과 증거로 채우는 최소 구조를 제공한다. | [`templates/`](#physical-form-inventory) |
| Authored documents | 요구, 결정, 명세, 실행, 운영, 참조를 소유한다. | `docs/01.requirements`부터 `docs/05.operations`, `docs/90.references` |

이 stage는 실제 PRD, AD, ADR, Spec, Plan, Task, 운영 기록이나 기능별 구현
계약을 소유하지 않는다. Form에는 재사용 가능한 구조만 두고, 공통 규칙은 이 README
또는 `.agents/governance`의 공통 정책으로 돌려보낸다.

###### Physical Form Inventory

Form directory는 사람이 form을 찾도록 physical responsibility surface별로 묶는다.
파일 이름은 form이 만드는 문서 kind를 나타내지만, directory 이름은 Registry
profile family를 정의하지 않는다. 예를 들어 `templates/specs/plan.template.md`는
그 경로를 유지하면서 `sdlc/plan` profile의 form으로 연결된다. 정확한 profile ID와
form 경로의 대응은 Registry만 소유한다.

- **Common forms** (`common/`): governed navigation README는 순서가 고정된
  여섯 key 봉투와 `type: "common/readme"`, `status: "active"`, 별도 artifact
  identity 없는 형태를 공유한다. stage·collection README는 Stage README form을 쓰고,
  implementation(agent·provider README 네 곳 포함)·runtime-governance README는
  Service README form을 쓰며,
  `Overview`/`Scope`/`Structure`/`Usage`/`Related Documents` core는
  workspace README만 공유하며, workspace README는 W03-D09에 따른 Stage 99
  지역 역할의 자체 Workspace README form을 쓴다. 루트 README는 Registry form의 `Purpose`,
  `Repository Map`, `Getting Started`, `References`를 쓴다. 각 form과 선택
  module은 경로별 Registry profile이 고른다. README는 사람 독자만을 대상으로 한다. 폴더의 agent 지시는 그
  폴더의 `AGENTS.md`에 두며, 루트 `AGENTS.md`를 포함한 모든 `AGENTS.md`는
  frontmatter 없이 AGENTS form을 쓰는 native `common/folder-agents-guide`
  파일이다. 루트 `CLAUDE.md`는 `common/root-provider-shim` gateway로, 폴더의
  `CLAUDE.md`는 native import로 유지한다.
- **Governance forms** (`governance/`): 공통 SDLC 계약, provider note, 역할,
  정책, 워크플로, 지식 지도, 프롬프트 계약에 `contract`, `provider`, `role`,
  `rule`, `skill`, `knowledge`, `prompt` form이 대응한다. `rule`은 운영 `policy`와
  같은 Policy form을 쓴다. `skill`은 `.agents/workflows/`의 두 workflow와
  `.agents/skills/<id>/SKILL.md` native package가 같은 Skill form을 쓰며,
  skill reference file과 asset은 role 없이 native로 남는다. 공통 소유자는
  `.agents`에, provider note는 `.claude/provider.md`와
  `.codex/provider.md`에 둔다. `governance/skill`은 두 workflow의
  생명주기 있는 문서 타입이며 native skill package와 같은 Skill form을 쓰되
  문서 frontmatter와 native 봉투로 구별한다. workflow는 등록된 지역 H3
  `Authority Boundary`를 쓸 수 있다.
  `governance/knowledge`는 `.agents/knowledge/`의 포인터 문서를,
  `governance/vocabulary`는 `.agents/knowledge/glossary.md`의 공통 용어와
  `docs/00.workspace/01.project/glossary.md`의 로컬 용어를 같은 form으로 검증하며,
  두 문서는 서로 다른 TERM ID의 정의를 소유한다.
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
  W03-D20과 W03-D26에 따라 `knowledge-map`, `vocabulary`, `prompt`,
  `evaluation-task`, `evaluation-score`, `evaluation-results` 여섯 역할은
  각자의 Stage 99 지역 form을 쓴다. W03-D34에 따라
  `governance-role`(`.agents/roles/*.md`, Current Contract 아래 여덟 역할 절)과
  `governance-document`(provider 노트 두 개)도 각자의 지역 form을 쓴다.
  현행 작성 문서는 공통 외피의 네 H2와 여덟 H3를 물리적으로 사용하고,
  이전 역할별 제목과 표는 `본문과 규칙` 아래의 하위 절에 둔다.
  `provider-native`를 뺀 모든 Stage 99 지역 역할은 각자의 지역 form을 쓰며,
  SPEC-0222에 따라 Stage 90 보고서는 core 역할의 form을 쓴다. 연구 보고서는
  `research`(`Question and Scope`·`Sources`·`Analysis`·`Application and Limits`,
  core 표 `research.sources`), 감사 보고서는 `audit`(`Scope`·`Findings`·`Actions`,
  core 표 `audit.findings`), 자료 보고서는 `data-reference`(`Purpose`·`Provenance`·
  `Interpretation`, core 표 `data-reference.schema`) form이다. 게시된 RES-0001-m0001~
  m0012와 AUD-0001-m0001은 identity가 묶인 retained form으로 이전의 여덟 H2를
  유지하며, 그 처분은 Q07-CUTOVER가 맡는다. `provider-native`만 form 없는 Stage 99 지역
  역할이며 table을 기록하지 않는다. 모든 등록 템플릿에는 TemplateDefinition이
  있다. `template_definition_record`는 Registry의 정의와 profile, form,
  키·관계·생명주기·언어 계약에서 레코드를 유도하며, Registry 검증이 모든 레코드를
  `contracts/template-definition.schema.json`에
  맞춰 검사한다. `contract_id`는 공통 양식이면 `COMMON-DOC-FORM-1`, 지역
  양식이면 `STAGE99-LOCAL-FORM-1`이다. `contract_version`은 그 계약의
  ASCII 숫자 세 요소 판본을 별도 필드에 기록한다. 변경 수준은
  [작성 정책](../00.workspace/03.process/document-authoring.md#frontmatter-order-and-versions)의
  소비자 호환성 기준을 따른다.
  `provider-native`의 빈 heading은 조건·소유자·검증·검토·제거 기준을 갖는
  조건부 확장(`headings_extension`)으로 기록한다. profile의 역할별 payload는
  form에서 오며 어떤 profile도 H2 목록(`sections`)을 두지 않는다. schema와 엄격
  Registry 검사가 `sections` key를 거부하고, mode가 `authored`, `router`,
  `template`인 profile은 `provider-native` role을 뺀 모든 경우에 form을 가져야
  한다(`REGISTRY_FORM_REQUIRED`). `native`나 `non-target` profile은 form이 없어도
  되며, 그때 Markdown profile 검증은 fence·frontmatter·placeholder 검사만 적용하고
  heading 규칙은 적용하지 않는다. ADR-0001부터 ADR-0061까지의 accepted ADR은
  등록된 retained form의 H2 목록과 그 검사를 ADR-0062에 따라 유지한다.
  SPEC-0222에 따라 `common_forms.core`는 채택한 공통 core의 `contract_id`,
  `contract_version`, 원본 SHA-256을 기록한다. form의 `core_role`은 19개 core
  역할 중 하나이거나 `domain`이며, form이 없는 `provider-native` 템플릿은
  `template_definition`에 `core_role: native`를 둔다. `domain`과 `native`에는
  소유자·이유·검토 조건·권한 근거를 담은 `classification`이 있다. core 역할 form은
  core 구성원을 그대로 담고, 각 템플릿이 core 표의 ID·조건·열·타입을 정확히
  가지는지 엄격 Registry 검사가 확인한다(`REGISTRY_CORE_TABLE`,
  `REGISTRY_CORE_SECTION`). 모든 지역 확장과 `table_id`가 없는 템플릿 지역 표는
  `authority_ref`를 가진다(SPEC-0222 이전 등록은 `ADR-0059`, SPEC-0222가 추가한
  것은 `SPEC-0222`). Incident 템플릿의 `Field | Value` 메타데이터 표는 계약 표가
  아니므로 등록하지 않는다(SPEC-0171). 문서 검사는 `required_when`이 `always`인 core 표가 core H2
  안에 정확한 core 머리글로 있는지(`BODY-CORE-TABLE-MISSING`)와 각 core 셀이 열
  타입을 지키는지(`BODY-CORE-TABLE-CELL`: 필수 셀 공란, 허용값 밖의 값, 정수 열의
  비정수)를 확인한다. 템플릿은 머리글만 검사하고, retained identity와 Task 표는
  제외한다.
- **Core SDLC forms**: physical `requirements/`, `architecture/`, `specs/`
  grouping은 `sdlc/requirement`, `sdlc/architecture-description`,
  `sdlc/architecture-decision`, `sdlc/spec`, `sdlc/plan`, `sdlc/task` profile의
  form을 담아 단계별 책임과 handoff를 기록한다. `sdlc/requirement`는 이 중
  처음으로 `requirement` form(네 H2와 여덟 H3, Traceability 아래 지역 H3
  `Lifecycle Traceability`와 `Archived Lineage`)을 쓰며 H2 목록을 두지 않는다.
  추적 표에 이 패키지의 NFR ID를 기록하면 같은 ID의 요구 행을
  `Quality Requirements`에 둔다. 기능 요구사항 표에는 FR과 IF 행을 둔다.
  `sdlc/architecture-description`은 `architecture` form(다섯 H2와 열 개 H3,
  Decisions and Adoption 아래 같은 두 지역 H3)을 쓰고 H2 목록을 두지 않으며, 각 요구 member를 자신의
  `Upstream requirement` 열에서 인용한다. Requirement는 downstream 링크 열을
  두지 않고, 파생 역조회와 `REQUIREMENT-COVERAGE` 검사가 그 자리를 대신한다.
  `sdlc/architecture-decision`은 core `decision` 역할에 묶인 `adr` form(Context,
  Options, Decision, Consequences의 네 H2와 여덟 H3, Decision 아래 지역 H3
  `Lifecycle Traceability`)을 쓰고 H2 목록을 두지 않는다(SPEC-0222). 근거와 선행
  결정은 Authority and Effect 아래 H4 `Sources`와 `Supersession`에 두고, 대안
  표는 core `decision.options` 표(`Option`, `Benefit`, `Cost and Risk`,
  `Reason`)다. 출처 사실이 없는 core 셀이 있는 ADR-0062는 열만 둔 core 표 뒤에
  기존 `Alternatives` 표를 `authority_ref: SPEC-0222`인 독자 지역 표로 유지한다.
  `sdlc/spec`은 `spec` form(네 H2와 여덟 H3, Acceptance Criteria 아래 지역 H3
  `Lifecycle Traceability`)을, `sdlc/plan`은 `plan` form(다섯 H2와 열 개 H3)을
  쓰며 둘 다 H2 목록을 두지 않는다. 두 form은 4.0.0 설계 목표의 제목과 section
  ID(`spec.intent.1` 등)를 쓴다(SPEC-0221).
  Spec의 기준 표는 `Criterion ID`와
  `Expected Result` 열로 Acceptance Criteria 아래에 두고, `Architecture` 열은
  architecture description이나 ADR 링크 또는 설명된 제외를 검사받는다. Plan의
  `Work Breakdown` 표는 Work Breakdown > Work Units 아래에, 승격 표
  (`Promotion ID`, `Target Owner`, `Acceptance`, `Evidence`)는 Promotion Map의
  Durable Owners 아래에 둔다.
  SPEC-0222에 따라 이 네 form은 core `requirement`, `architecture`, `spec`,
  `plan` 역할에 묶인다. 기능·품질 요구사항 표는 core `requirement.requirements`
  표(`Requirement ID`, `Statement`, `Rationale`, `Acceptance`, `Priority`)의
  인스턴스이고 `Priority`는 `must`, `should`, `could` 중 하나다
  (`BODY-CORE-TABLE-CELL`). `Quality Requirements` H3는 항상 두며, core
  `requirement.quality` 표는 정의만 두고 렌더링하지 않는다. core
  `task.work_items` 표도 frontmatter `status`와 함께 둘 수 없으므로 Task
  템플릿은 한 항목 Task의 `status`를 두고 이 표를 작성자 안내로만 둔다. 외부 인터페이스를 밝힌
  architecture description은 Structure > Interfaces에 core
  `architecture.interface` 표를 둔다. Spec은 Verification Strategy 아래에 core
  `spec.checks` 표를, Plan은 Work Units의 `Work Breakdown` 표 뒤에 core
  `plan.work_units` 표를, Selected Checks 아래에 core `plan.checks` 표를 둔다.
  기존 `Criteria`, `Work Breakdown`, 승격 표, `Lifecycle Traceability`,
  `Constraints`, `Quality Scenarios` 표는 `authority_ref: ADR-0059`인 독자 지역
  표로 남는다.
  ADR-0001부터 ADR-0061까지의 accepted ADR은 승인된 일곱 H2를 등록된
  retained form으로 유지하며(W03-D02, W03-D52, W03-D69), 그 범위 뒤의 ADR은
  accepted를 포함한 모든 상태에서 공통 form을 쓴다.
- **Spec forms** (`specs/`): `spec`, `plan`, `task` form이 요구 추적,
  실행 계획, 작업 증거를 소유한다. 별도 data-model 및 native contract
  capacity는 현재 consumer가 없어 Spec 본문과 실제 구현 소유자에게 수렴했다.
- **Operations forms** (`operations/`): `guide`, `policy`, `runbook`,
  `incident`, `postmortem`의 서로 다른 운영 증거 책임을 유지한다.
  Guide, Runbook, Incident, Postmortem, Policy는 4.0.0 설계 목표의 제목과 section
  ID를 쓰는 Registry form을 쓴다(SPEC-0221). Guide의 독자·목표는 `Purpose`,
  `Lifecycle Traceability` 관계 표는 `Troubleshooting` 아래에 둔다. Runbook의
  트리거·절차·검증·상향은 form의 `Trigger and Scope`, `Preflight`, `Procedure`,
  `Verification`, `Escalation`에 배치하고, `Lifecycle Traceability` 관계 표는
  `Verification` 아래에 둔다. Incident의 `Lifecycle Traceability` 관계 표는
  `Resolution` 아래에, Postmortem의 표는 `Actions` 아래에 둔다. Policy의
  목적·범위·규칙·예외·집행·소유는 form의 `Purpose and Scope`, `Rules`,
  `Enforcement`, `Ownership`에 배치하고, Policy의
  `Lifecycle Traceability` 관계 표는 `Ownership` 아래에서 같은 source·열·상호 참조
  의미를 유지한다. Policy가 규범적 규칙을 진술하면 `Requirements` 아래에 core
  `Rules` 표(Rule ID·Condition·Requirement·Enforcement·Evidence)에 현재 규칙마다
  한 행을, 그 뒤 Rule ID로 묶인 지역 `Rule Levels` 표(Rule ID·Level, 선택 열
  Status)에 발급한 규칙 ID마다 한 행을 둔다(SPEC-0222). 규칙 ID는 정책의 등록
  code로 만든 `<CODE>-R<NNN>`이고, 규칙의 내용은 Rules 행에만 있으며 본문의 보충
  단락·목록은 ID를 코드 스팬 한 줄로 둔 H4 아래에 남는다. 열이 더 많은 규칙 표는
  Rule ID로 묶인 지역 표로 남는다. `Status`는 `retired;` 뒤에 후속
  ID나 `none`을 적어 폐기한 규칙의 행을 남기는 이 저장소의 조건부 확장이며,
  정확한 값과 code 기록은 Registry의 `policy_rule_ids`가 소유한다. 규칙 ID와 code는
  사용자가 승인한 Q-07 새 baseline까지 영구하다. ID는 삭제하거나 폐기 뒤 다시 `active`로
  되돌리지 않고, 등록된 code는 바꾸거나 다른 정책에 주지 않으며, 트리를 떠나는 정책의
  code는 줄어들지 않는 `reserved_codes`로 옮긴다.
  기계가 읽는 정확한 heading과 순서·내용 경계는 Registry가 소유한다. 빈 heading이나
  placeholder만 채운 항목은 실질 내용이 아니며, 형식 PASS는 live 증거가 아니다.
- **Reference forms** (`references/`): Stage 90 collection 세 곳은 모두 같은 3단
  구조를 갖는다. collection router `{audits,data,research}/README.md`는
  `common/readme` type으로, pack anchor
  `####-<slug>/README.md`는 `reference/audit-pack`·`reference/data-pack`·`reference/research-pack` form을,
  pack member `####-<slug>/m####-<slug>.md`는 같은 family의
  `reference/audit`·`reference/data`·`reference/research` form을 사용한다.
  세 pack README는 W03-D10에 따른 Stage 99 지역 역할의 자체 Reference Pack
  README form을 함께 쓰며, 종류별 계약 절은 `Pack Contract`, 멤버 색인 절은
  `Pack Index`로 부른다. Registry는 pack 유형별 필수 마감 절의 적용 대상을 원본
  profile로 지정하고 템플릿에도 같은 바인딩을 적용한다. 게시된 멤버의 retained
  form은 Registry에 등록된 보고서 ID에만 적용하며, 검사기는 문서 경로에서 그
  ID를 유도한다.
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
  profile로 분류하며 Skill form을 쓰고 `common/template-native-skill`
  template이 그 form을 보인다. top-level `name`/`description`, 공통 여섯 key를 담는
  `metadata`, boolean `disable-model-invocation: true`를 사용한다. 문서
  봉투는 metadata 내부에만 두며 실제 native invocation/tool/model
  controls를 형식 정규화를 위해 바꾸지 않는다. 각 package의
  `agents/openai.yaml`은 Codex의 `policy.allow_implicit_invocation: false`를
  소유한다. 이 native sidecar와 Claude skill adapter의 정확한 집합은
  [agent validator](../../scripts/validate-agent-governance.py)가 검증한다.

현재 physical form의 전체 목록과 각각의 소유 profile은 README나 support prose가
아니라 registry와 repository quality gate에서 계산한다.

###### Deliberately Empty Profiles

현재 record가 없는 것은 곧 사용하지 않는 capacity를 뜻하지 않는다.
`operation/incident`와 `operation/postmortem`은 사건 발생 전에도 운영 증거를
기록할 수 있도록 유지한다. `reference/audit`, `reference/data`,
`reference/audit-pack`, `reference/data-pack`은 각각 Stage 90의 감사와
데이터 자료를 지원한다. [Audit collection](../90.references/02.audits/README.md)은
현재 감사 pack을 안내한다. Data는 자료가 생길 때 사용할 pack과 member
profile을 유지한다.

#### Usage

##### Entry Points

1. **Classify**: repository-relative target path를 registry로 분류하고 정확히 하나의
   profile이 선택되는지 확인한다.
2. **Copy**: 선택된 profile의 canonical form을 복사한다.
   `python3 scripts/document-generator.py`가 정규 TemplateDefinition을 확인하고
   양식의 절과 표 열을 검사한 뒤 공통 marker 다섯 개를 채운다(번호는 호출자가
   target path에 쓴다). 적용되는 절에서 작성 문서에 데이터 행을 요구하는
   표는 복제 원본에 등록된 열을 갖춰야 한다. 생성 시점에는 빈 데이터 행 없이
   표 머리글만 둘 수 있다. form을 손으로 복사해도
   유효하며 validator가 gate다. 이웃 파일명이나 README 목록으로 form을
   추측하지 않는다.
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
소유한다. 현행 Spec·Plan 상태는 `draft`, `in-review`, `approved`, `cancelled`다.
`approved`는 현재 계약의 승인·유효성을 뜻한다. Task의 core Work Items 표(Work Performed의
첫 표)는 작업 항목별 상태를, Lifecycle Traceability 표(Execution Log 아래)는
Item별 결과와 증거 포인터를 기록하고, Criterion Decisions 표가 기준별 수용 판정의
유일한 작성 원본이다. Results 표는 검사 사실을 보존한다. 기존 완료
Spec·Plan·Task는 당시 Registry 판본으로 읽으며 상태와 승인·검사 근거를 보존한다.
새로 작성하거나 현행 내용을 바꾸는 Plan은 승인된 Spec의 제약을
`Global Constraints`에서 연결하고 Plan에만 필요한 추가 실행 제약을 적으며,
지속 계약의 실제 현행 소유자와 위치를 Promotion Map의 Durable Owners 표에
기록한다. `Global Constraints`는 Overview > Constraints의 본문 뒤에 오는 H4다. 완료
판정에서는 이 표가 유일한 승격 기록이며, 승격 대상이 없으면
`none | none | none | No durable contract was introduced` 한 행만 명시한다.
lifecycle reader는 두 위치를 form의 section id로 읽고, 현행 Plan의
작성·완료 의무는 선택한 입력에 대해 검사한다. Stage 99
형식 구현은 해당 형식을 위임하는 현행 정책 소유자를 가리킨다.

Plan, Task Work Items, Lifecycle Traceability, Criterion Decisions, Results 표의 열 이름과
순서, 수용 값 집합은 Registry의 `body_contract`와 core 표가 소유하며 이 README는
복제하지 않는다. 기록된 Task는 기록 당시 머리행 그대로 전환 어댑터가 core 이름으로
읽고, 한 Task 안에서 두 머리행을 섞지 않는다.
`not-required`는 취소된 Task와 같은 package의 취소된 Spec에서 해당 기준의
실제 범위 변경과 승인 근거를 확인한 때만 쓴다. 두 취소 처분 모두 정확한
기준 ID를 명시하고 Task의 승인 참조는 해당 Spec 결정을 가리킨다. 후속
Task만 정하거나 활성·
완료·대체 Task로 끝내는 경우 기준 면제로 바꾸지 않는다. QA의
`NOT_APPLICABLE`는 검사 대상 판정으로 이 수용 값과 다르다.
`Required`는 `true` 또는 `false`(기록된 Task의 `yes`·`no`는 같은 뜻으로 읽는다), `Resolves`는 `none` 또는 앞선 증거 ID를
쉼표와 공백으로 연결한다. `false`는 원래 검증 계획에서 비필수인 검사와
그 사유에만 쓰며 필수 실패를 사후 재분류하지 않는다. 필수
`FAIL`·`DEFER`·`NOT_RUN`은 같은 검사·작업
항목·기준의 뒤따르는 `PASS`가 이전 증거 ID를 명시해야 해소된다. 다른
PASS로 미해소 필수 결과를 숨기지 않는다. 완료 인계는 필수 기준의 Plan
배정, 실제 Task 완료, 구체적 PASS 증거, 단일 `accepted` 판정과 지속
의미의 현재 owner를 함께 확인한다. QA 결과, 기준 수용, 원본 승인,
통합과 보관은 서로의 대체값이 아니다. 취소·대체는 남은 필수 기준의
후속 Task의 Plan 배정을 명시하고, 관측 결과를 보존한다.
관측된 `FAIL`은 `PASS`처럼 구체적인 Command·Input·Location을 적는다.
`NOT_RUN`·`DEFER`에는 아직 실제 결과 위치가 없으면 `none`(기록된 Task는 `Pending`)을
쓸 수 있지만 사유와 다음 owner를 남긴다.
resolved Incident에는 시간대를 포함한 실제 resolved_at과 해결 증거가 필요하다.

###### Shared Frontmatter Grammar

모든 governed Markdown은 "title", "version", "type", "status", "owner",
"updated" 순서로 시작한다. 이후 "artifact_id", relationship,
supersession, provenance key는 선택된 profile의 order에만 따라 나타난다.
모든 string, date, version, ID scalar는 큰따옴표를 사용한다.

| Key | Presence | Grammar | Template value |
| --- | --- | --- | --- |
| "title" | 항상 | identity를 반복하지 않는 사람용 이름 | "&#123;&#123;TITLE&#125;&#125;" |
| "version" | 항상 | ASCII 숫자 세 요소(`X.Y.Z`), 선행 0·접두사·접미사 없이 표기 | "0.1.0" |
| "type" | 항상 | Registry profile ID인 "family/kind" | profile literal |
| "status" | 항상 | profile lifecycle subset 또는 router constant | profile literal |
| "owner" | 항상 | 책임 소유자 | "&#123;&#123;OWNER&#125;&#125;" |
| "updated" | 항상 | ISO date | "&#123;&#123;UPDATED&#125;&#125;" |
| "artifact_id" | stable identity profile만 | "artifact_id_pattern" | "&#123;&#123;ARTIFACT_ID&#125;&#125;" |

값의 scalar/array 문법은
[Stage 99 contracts](./01.contracts/)의 frontmatter schema가, profile별
required, optional, forbidden, order, constant, lifecycle, identity pattern은
[Registry](./registry.json)가 소유한다. 각 key의 의미·작성 주체·소비 경로·테스트는
Registry의 `frontmatter_keys`가, YAML과 JSON Schema dialect는 `frontmatter_dialect`가
소유한다. 각 문서 relation의 종류·방향·cardinality·소유자·소비 경로와 link 유형 네 가지의
의미는 Registry의 `relationship_contract`가 소유한다. Markdown placeholder는
"&#123;&#123;UPPER_SNAKE_CASE&#125;&#125;", native placeholder는 `__UPPER_SNAKE_CASE__`,
작성 안내는 `<!-- 작성 규칙: ... -->` 주석을 사용한다. 이 주석은 빈 form의
작성 단계에서만 사용하며 완료된 작성 문서에는 남기지 않는다. 공통 외피와
역할별 본문·표의 규칙은 [common document contract](./01.contracts/common-document-contract.json),
Registry의 profile·form·TemplateDefinition이 나누어 소유한다. `관련 문서`의
선택적인 `Relation | Target` 표는 실제 의미 관계에 한해 사용하며 relation은
`requires`, `designs`, `implements`, `verifies`, `operates`, `defines`, `cites` 중
하나이고 target은 단일 Markdown 링크다. 단순 탐색 링크는 표 밖에 둔다.

Template은 만드는 문서의 envelope를 투영하므로 profile이 요구하는
"artifact_id" placeholder를 포함한다. "layer"는 ADR-0001부터 ADR-0061까지의 accepted ADR에만 남으며 어떤
template도 선언하지 않는다. Template 파일 자체의 revision과 destination
identity는 Registry contract version과 Git history가 소유한다.
README router에는 stable "artifact_id"가 없으며 reference pack anchor는
기존 AUD/RES/DATA identity와 게시 생명주기를 유지한다. governance에는 기존
optional identity만 보존한다.
Stage 98(`docs/98.archive/`)에는 profile과 form이 없다. 그 경로는 문서
inventory 밖이며 검증하지 않는다.

###### Upstream and Downstream

- [Docs README](../README.md)

###### Policy and Templates

- [Agent Governance Hub](../../.agents/README.md)
- [Document Authoring Policy](../00.workspace/03.process/document-authoring.md)

##### Checks

###### Task Status Authoring

Task 행 상태와 frontmatter `status`의 작성법은
[Document Authoring Policy](../00.workspace/03.process/document-authoring.md)와
[Document Lifecycle Policy](../00.workspace/03.process/document-lifecycle.md)가,
Task 최초 기록이 허용하는 상태와 Spec·Plan의 direct approval·first-record
approval 예외는 Document Lifecycle Policy가 정본이다. 이 README는 그 규칙을
다시 적지 않는다. 지역 확장의 정확한 이름은 Registry
`shared_contract.extensions`에 있다.

## 적용과 확인

### 적용 방법

아래 역할별 본문에 기록된 사용 조건과 절차를 적용한다.

### 확인 기준

아래 역할별 본문의 검증·확인 조건과 그 한계에 따른다.

## 관계와 출처

### 관련 문서

관련 문서와 정본 링크는 아래 역할별 본문에서 확인한다.

### 외부 근거

외부 근거가 사용된 경우 아래 역할별 본문의 출처와 적용 범위에서 확인한다.
