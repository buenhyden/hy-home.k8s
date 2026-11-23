---
title: "03.specs"
version: "1.0.0"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-11-20"
---

# 03.specs

## 문서 개요

### 목적과 독자

이 경로의 현행 Spec·Plan·Task를 찾는 사람과 작성자가 Stage 03의 변경 계약과 실행 증거를 구분하도록 안내한다.

### 책임과 적용 범위

Stage 03은 열린 변경 package의 문서와 잔여 포인터를 소유한다. 형식은 Stage 99, 지속 요구와 운영은 각각 해당 단계가 소유한다.

## 내용 계약

### 입력과 전제

문서 작성자는 현재 Requirement·Architecture·사용자 요청과 선택된 Stage 99 profile을 먼저 확인한다.

### 본문과 규칙

#### Responsibility

##### Purpose

> Requirement Package와 Architecture를 구현 가능한 기술 계약과 검증 기준으로 구체화하는 Spec stage다.

이 경로는 Requirement Package, AD, ADR을 구현 가능한 기술 계약으로
구체화하는 Spec stage다. 서비스 동작, API 계약, 변경 한정 설계와 검증
기준은 이곳에서 하위 구현과 추적 가능해야 한다.

Spec은 변경 계약과 수용 기준을, Plan은 그 계약을 실행할 순서·위험·예정
검증을 소유한다. 새 Spec·Plan의 `approved`는 검토된 계약의 현재 권한과
유효성을 뜻하며 구현 완료나 기준 수용의 표지가 아니다. Task의 실행 상태,
검사 사실과 기준별 단일 수용 판정이 실제 완료를 증명한다. `ready` Task는
실행 준비 상태이지 승인이나 실제 착수의 증거가 아니다. package는 변경이
열려 있는 동안만 이 stage에 있다.

###### Stage Readers

이 README의 주요 독자:

- Platform Engineers
- Application Developers
- Documentation Writers

###### Inputs and Outputs

<a id="in-scope"></a>

**In Scope**

- 기능/서비스 기술 설계와 인터페이스 계약
- 데이터 모델, API 계약, 비기능 요구, 검증 기준
- Agent 역할, 도구, 정책, 평가, 실패 모드 설계
- Requirement Package/AD/ADR과 Plan/Task/Runbook을 잇는 traceability

<a id="out-of-scope"></a>

**Out of Scope**

- 제품 우선순위와 사용자 가치 중심 설명
- 전사 운영 정책
- 실시간 장애 대응 절차
- work-unit 밖의 실행 추적 정본

위 내용은 각각 `01.requirements/`, `05.operations/policies/`,
`05.operations/runbooks/`, 그리고 각 Stage 03 work-unit의
`01.tasks/tsk-####-<slug>.md` records로 분리한다.

##### Excluded Responsibilities

이 stage는 제품 우선순위와 사용자 가치 중심 설명, 전사 운영 정책, 실시간 장애 대응 절차, work-unit 밖의 실행 추적 정본을 소유하지 않는다. 이는 각각 `01.requirements/`, `05.operations/policies/`, `05.operations/runbooks/`, 그리고 각 Stage 03 work-unit의 `01.tasks/tsk-####-<slug>.md` records로 분리한다. 새 Spec·Plan의 `approved`는 구현 완료나 기준 수용의 표지가 아니며, `ready` Task도 승인이나 실제 착수의 증거가 아니다.

#### Current Contents

##### Paths

각 package 폴더는 자신의 탐색을 스스로 소유한다. `spec.md`는 변경 계약을,
`plan.md`는 구현 순서와 위험을, `01.tasks/`는 package-local Task 기록을
소유한다. 이 README는 package 폴더까지만 안내하며, 각 package의 상태와
날짜는 그 package의 `spec.md` frontmatter가 소유한다.

아래 목록은 시점 목록이며 고정 roster나 개수 불변식이 아니다.

```text
03.specs/
├── 0223-work-residue-handoff/
├── 0224-workspace-path-cutover/
├── 0225-q07-history-bound-checks/
├── 0226-common-document-contract/
├── 0227-docs-sdlc-reconciliation/
├── 0228-independent-review-boundary/
├── 0229-selective-environment/
├── 0230-feedback-routing/
├── 0231-native-request-brief/
├── AGENTS.md
├── CLAUDE.md
├── README.md
└── work-residue-ledger.json
```

현재 package는 다음과 같다. 상태와 인수 여부는 각 문서가 소유한다.

| Path | Purpose |
| --- | --- |
| [SPEC-0223 Work Residue Handoff](./0223-work-residue-handoff/) | SPEC-0161, SPEC-0221, SPEC-0222의 열린 잔여를 넘겨받아 live residue 표를 두고, 세 package를 종료시키는 변경 package다. |
| [SPEC-0224 Workspace Path Cutover](./0224-workspace-path-cutover/) | W 계층 문서를 `docs/00.workspace/`로 옮기고 SAFE·GIT 규칙을 W/A로 나누며 `docs/` 분류 폴더를 번호화하는 변경 package다. |
| [SPEC-0225 Q07 History-Bound Check Conversion](./0225-q07-history-bound-checks/) | Q07-H01이 지목한 이력·번호 의존 검사를 바꾸거나 없애고, 전환 시점에 처리할 데이터를 잔여에 기록하는 변경 package다. |
| [SPEC-0226 Common Document Contract](./0226-common-document-contract/) | P04 공통 외피·유형별 내용·metadata·관계 의미를 Stage 99와 실제 생산자·검증기에 연결하는 변경 package다. |
| [SPEC-0227 Current Documentation and SDLC Reconciliation](./0227-docs-sdlc-reconciliation/) | P05 현행 문서 소유자·SDLC 권위·운영 잔여를 정합화하는 변경 package다. |
| [SPEC-0228 Independent Review and Read-Only Boundary](./0228-independent-review-boundary/) | P06 위험별 독립 검토, 결과 증거 재사용 및 실제 읽기 전용 실행 경계를 보완하는 변경 package다. |
| [SPEC-0229 Selective Validation Environment](./0229-selective-environment/) | P07 선택형 k3d 환경, 여러 실행의 합산 자원 제한과 생산 LAN 격리 경계를 다루는 변경 package다. |
| [SPEC-0230 Feedback Routing Repair](./0230-feedback-routing/) | R01 suite 등록과 일반 workspace guide 변경이 실제 소비자 검사만 선택하도록 검증 경로를 좁히는 변경 package다. |
| [SPEC-0231 Native Request Brief](./0231-native-request-brief/) | P08 provider 요청 접수를 현재 요청·workspace·정책에 결합하고, 사용자에게 보인 브리핑을 기록한 뒤에만 첫 변경을 허용하는 변경 package다. |
| [work-residue-ledger.json](./work-residue-ledger.json) | 열린 인계·충돌·채택·조사 잔여 항목을 포인터로만 담는 work residue ledger다. 실행 상태, 증거, 수용은 담지 않고 Task가 소유한다. 종결된 항목은 그 Task가 속한 package의 종료 commit까지 삭제한다. |
| [AGENTS.md](./AGENTS.md) | 이 stage에 적용되는 AI 에이전트 지시다. |
| [CLAUDE.md](./CLAUDE.md) | Claude가 그 지시를 불러오게 하는 한 줄 `@AGENTS.md` import다. |

완료된 package는 그 Requirement Package의 `Archived Lineage` 표가 요약한다.
최근 것은 SPEC-0162부터 SPEC-0220까지, SPEC-0154부터 SPEC-0160까지와 SPEC-0153, SPEC-0152다. 이들의 요약은
[REQ-0003의 Archived Lineage](../01.requirements/0003-workspace-agent-governance-platform.md#archived-lineage)에 있다.
SPEC-0141의 요약은 [REQ-0002](../01.requirements/0002-argo-notifications-slack.md#archived-lineage)에 있다.

##### Owners

분류: 해당 없음 — 이 stage README는 하위 유형을 따로 나누지 않는다.

#### Usage

##### Entry Points

1. 관련 Requirement Package, AD, ADR 링크를 확인하고 Spec의 입력으로 고정한다.
2. 새 Spec은 `../99.templates/02.templates/03.specs/spec.template.md`에서 시작하고, canonical target pattern은 `docs/03.specs/<####-slug>/spec.md`다.
3. 변경 한정 설계와 수용 기준은 `spec.md`, 실행 순서·위험·예정 검증·rollback은 `plan.md`, 실제 실행·검사 사실·기준별 수용 판정은 package-local Task record가 소유한다. 범위나 근거가 승인 계약을 바꾸면 영향을 받는 Spec·Plan을 재검토한다.
4. 장기 구조는 Stage 02 Architecture Description으로, 중요한 장기 결정은 ADR로 승격한다. 폐기된 Stage 04 경로는 새 문서에서 사용하지 않는다.

###### Relative Link Rules

이 README의 링크 기준 위치는 `docs/03.specs/`다.

- 상위 문서는 `../`로 시작하는 상대 경로를 사용한다.
- 같은 stage의 package는 `./<####-numbering>-<feature-id>/` 폴더로 연결한다.
- 실행 문서는 같은 work-unit의 `plan.md`와 `01.tasks/tsk-####-<slug>.md`, 운영 문서는 `../05.operations/`로 연결한다.

###### Spec Authoring Rules

1. 모든 활성 Spec은 관련 Requirement Package와 Architecture 입력을 링크하거나 부재를 명시한다.
2. Verification은 필수다.
3. Acceptance Contract와 테스트 의도는 Requirement Package에서 이어지고, 구현 검증은 Task record와 연결된다.
4. 실행 가능한 인터페이스 계약은 실제 구현 소유 경로에 두고 Spec에서 그 owner와 검증을 추적한다.
5. Agent 변경은 목표·동작·경계·실패 조건을 Spec에, 구현 순서와 rollback을 Plan에 기록한다.
6. Feature-local Task records가 해당 work-unit의 실행과 evidence를 소유한다. Validator의 독립 실행 테스트와 fixture는 top-level `tests/`와 `tests/fixtures/` 아래에 두고, production module은 이를 import하거나 runtime data로 읽지 않는다. `validation/tests/` 또는 Spec-package-local test control plane은 만들지 않는다.
7. Spec의 `Lifecycle Traceability` 표(Acceptance Criteria 아래)는 Requirement ID를 기준에 잇고, Plan의 `Work Breakdown` 표(Work Breakdown > Work Units 아래)는 각 work unit을 Task에 잇는다. Spec의 core `spec.checks` 표는 Verification Strategy 아래에, Plan의 core `plan.work_units` 표는 `Work Breakdown` 표 뒤에, core `plan.checks` 표는 Selected Checks 아래에 둔다(SPEC-0222).

###### Helper Templates

아래 템플릿은 `docs/03.specs/<####-slug>/` package의 Spec, Plan, Task에 사용한다.

- `../99.templates/02.templates/03.specs/spec.template.md`
- `../99.templates/02.templates/03.specs/plan.template.md`
- `../99.templates/02.templates/03.specs/task.template.md`

###### Upstream and Downstream

- [Docs README](../README.md)
- [01.requirements](../01.requirements/README.md)
- [02.architecture/descriptions](../02.architecture/01.descriptions/README.md)
- [02.architecture/decisions](../02.architecture/02.decisions/README.md)
- [05.operations/runbooks](../05.operations/03.runbooks/README.md)
- [Archive Index](../98.archive/README.md)

###### Policy and Templates

정책과 template: 해당 없음 — 이 stage README는 정책과 template 링크를 관련 문서로 따로 나열하지 않는다.

##### Checks

1. 끝난 package는 지속 계약을 현재 소유 문서로 승격하고 Requirement의 `Archived Lineage`에 요약한다. 대체되거나 철회된 단독 문서도 소유 문서에 요약한다. 삭제 전에는 [문서 수명주기 정책](../00.workspace/03.process/document-lifecycle.md)의 처분 조건을 확인하며, 원본은 확인된 Git 이력에서 복구한다([ADR-0053](../00.workspace/02.architecture/02.decisions/0053-unvalidated-archive.md)). 개별 단순 처분마다 새 Spec을 만들지 않는다.

## 적용과 확인

### 적용 방법

아래 package 색인에서 해당 Spec을 열고 Plan의 의존성을 확인한 뒤 Task의 실제 결과를 읽는다.

### 확인 기준

링크와 문서 profile 검사는 현재 트리를 확인한다. 인수와 live 동작은 각 Task의 실제 근거를 따른다.

## 관계와 출처

### 관련 문서

[요구사항](../01.requirements/README.md), [Architecture](../02.architecture/README.md), [Stage 99](../99.templates/README.md)가 이 색인의 입력과 형식 소유자다.

### 외부 근거

이 색인은 외부 규범을 직접 채택하지 않는다. 출처와 채택 판단은 연결된 Spec과 정식 소유 문서에서 확인한다.
