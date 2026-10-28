---
title: "03.specs"
version: "0.21.0"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-10-16"
layer: "specs"
---
# 03.specs

> Requirement Package와 Architecture를 구현 가능한 기술 계약과 검증 기준으로 구체화하는 Spec stage다.

> [!NOTE]
> 이 stage에서 이루어지는 모든 AI 에이전트 작업은 [Agent Governance Hub](../../.agents/README.md)를 따른다.

## Overview

이 경로는 Requirement Package, AD, ADR을 구현 가능한 기술 계약으로
구체화하는 Spec stage다. 서비스 동작, API 계약, 변경 한정 설계와 검증
기준은 이곳에서 하위 구현과 추적 가능해야 한다.

Spec은 변경 계약과 수용 기준을, Plan은 그 계약을 실행할 순서·위험·예정
검증을 소유한다. 새 Spec·Plan의 `approved`는 검토된 계약의 현재 권한과
유효성을 뜻하며 구현 완료나 기준 수용의 표지가 아니다. Task의 실행 상태,
검사 사실과 기준별 단일 수용 판정이 실제 완료를 증명한다. `ready` Task는
실행 준비 상태이지 승인이나 실제 착수의 증거가 아니다. 기존 완료
Spec·Plan·Task는 당시의 `completed` 상태와 근거를 보존하고, Stage 98의
동결된 `done` 기록도 원문 그대로 읽는다. 끝난 package는 처분이 승인될
때까지 이 stage에서 기다리고, 승인되면 ADR-0040에 따라
`98.archive/completed/`에 package 단위로 원본 Git object 그대로 보존된다.
Retention Catalog가 원래 경로를 한 번 명명하고 원본은 Git history가 복구한다.

### Stage Readers

이 README의 주요 독자:

- Platform Engineers
- Application Developers
- Documentation Writers
- AI Agents

## Scope

### In Scope

- 기능/서비스 기술 설계와 인터페이스 계약
- 데이터 모델, API 계약, 비기능 요구, 검증 기준
- Agent 역할, 도구, 정책, 평가, 실패 모드 설계
- Requirement Package/AD/ADR과 Plan/Task/Runbook을 잇는 traceability

### Out of Scope

- 제품 우선순위와 사용자 가치 중심 설명
- 전사 운영 정책
- 실시간 장애 대응 절차
- work-unit 밖의 실행 추적 정본

위 내용은 각각 `01.requirements/`, `05.operations/policies/`,
`05.operations/runbooks/`, 그리고 각 Stage 03 work-unit의
`tasks/tsk-####-<slug>.md` records로 분리한다.

## Structure

각 package 폴더는 자신의 탐색을 스스로 소유한다. `spec.md`는 변경 계약을,
`plan.md`는 구현 순서와 위험을, `tasks/`는 package-local Task 기록을
소유한다. 이 README는 package 폴더까지만 안내하며, 각 package의 상태와
날짜는 그 package의 `spec.md` frontmatter가 소유한다.

package는 폐기·완료·중복·상충이 증명되고 lifecycle 정규화, consumer 전환,
Git 복구가 끝난 뒤에만 현재 트리를 떠나 [Archive](../98.archive/README.md)에
보존된다. 아래 목록은 시점 목록이며 고정 roster나 개수 불변식이 아니다.

```text
03.specs/
├── README.md
├── 0105-authority-and-safe-authoring/
├── 0106-stage99-lifecycle-normalization/
├── 0107-local-qa-and-release/
├── 0108-task-status-and-provider-boundaries/
├── 0109-shared-workspace-memory/
├── 0110-provider-readme-and-qa-diagnostics/
├── 0111-historical-fixture-drift/
├── 0112-pinned-package-fixtures/
├── 0113-sdlc-sync-and-v9-gaps/
├── 0114-provider-permission-hardening/
├── 0115-r10-local-remediation/
├── 0116-independent-review-gate/
├── 0117-local-qa-rightsizing/
├── 0118-qa-phase-two/
├── 0119-ingress-controller-identity/
├── 0120-test-purpose-gates/
├── 0121-traefik-ingress-cutover/
├── 0122-archive-unit-disposition/
├── 0123-hosted-lock-check/
├── 0124-required-source-coverage/
├── 0125-survey-status-and-local-gaps/
├── 0126-architecture-views/
├── 0127-adr-lineage-and-branch-strategy/
├── 0128-change-kinds-and-authoring-prompts/
├── 0129-inventory-operations-and-qa-baseline/
├── 0130-archive-history-link-migration/
├── 0131-archive-evidence-owner-migration/
└── 0133-review-decisions-and-c4-prompt/
```

[Common Authority and Safe Authoring](./0105-authority-and-safe-authoring/)은 P01의 공통 권한과 안전한 저술 계약을 소유한다.
[Stage 99 Lifecycle Normalization](./0106-stage99-lifecycle-normalization/)은 P02의 문서 lifecycle과 실행 추적 계약을 소유한다.
[Local Quality and Release Lifecycle](./0107-local-qa-and-release/)은 로컬 QA와 릴리스 절차의 변경 계약을 소유한다.
[Task Status Derivation and Provider Boundaries](./0108-task-status-and-provider-boundaries/)는 다중 행 Task 요약 파생, provider README 언어, Claude 원격 명령 확인 경계를 소유한다.
[Shared Workspace Memory Store](./0109-shared-workspace-memory/)는 Claude와 Codex가 함께 쓰는 공유 기억 저장소와 native 기억 비활성화를 소유한다.
[Provider README Language and QA Tool Diagnostics](./0110-provider-readme-and-qa-diagnostics/)는 provider README 한국어화와 로컬 style 도구 누락 진단을 소유한다.
[Historical Fixture Drift in Lifecycle Tests](./0111-historical-fixture-drift/)는 역사 commit을 재생하는 lifecycle 테스트의 fixture 고정을 소유한다.
[Pinned Package Fixtures in Lifecycle Tests](./0112-pinned-package-fixtures/)는 완료 package 문서를 읽는 나머지 테스트의 Git 고정을 소유한다.
[SDLC Document Sync and Remaining v9 Gaps](./0113-sdlc-sync-and-v9-gaps/)는 SPEC-0108 이후 요구사항·아키텍처·Spec 문서 정합성과 남은 v9 지적 사항을 소유한다.
[Provider Native Permission and Hook Hardening](./0114-provider-permission-hardening/)은 Claude·Codex native 권한, Codex 설정·rules와 공유 write guard hook 보강을 소유한다.
[r10 Local Governance and Delivery Remediation](./0115-r10-local-remediation/)은 r10의 완료 증적과 현행 거버넌스·문서·검증·전달·GitOps 범위의 r13 후속 작업(SPEC-0115-TSK-0002)을 소유한다.
[Independent Review Merge Gate](./0116-independent-review-gate/)는 로컬 독립 리뷰를 리뷰 App의 필수 check로 게시해 PR이 고친 workflow의 check 위조를 막는 계약을 소유한다.
[Local QA Rightsizing](./0117-local-qa-rightsizing/)은 로컬 QA의 과잉·중복·상충·현행 불일치 검사 정리와 main에서 실패하던 테스트 복구를 소유한다.
[Local QA Phase Two](./0118-qa-phase-two/)는 workflow 검사 단일 소유, 좁힌 script·test surface와 lifecycle 모듈 gate를 소유한다.
[Ingress Controller Identity in Validators](./0119-ingress-controller-identity/)는 검증기의 ingress controller 식별자를 한 곳에 선언하고 중복 shell 검사를 정리하는 계약을 소유한다.
[Test Module Purpose Gates](./0120-test-purpose-gates/)는 모든 test 모듈을 하나의 목적 gate에 배정하는 공유 suite runner와 그 coverage guard를 소유한다.
[Traefik Ingress Cutover](./0121-traefik-ingress-cutover/)는 ingress-nginx를 Traefik으로 교체하는 병행 운영, 라이브 검증, 전환과 되돌리기 단위를 소유한다.
[Archive Unit Disposition](./0122-archive-unit-disposition/)는 소비자가 없는 Archive 보존 단위 7개를 `git-history-only`로 처분한 결정과 증거를 소유한다.
[Hosted CI Lock Check](./0123-hosted-lock-check/)는 `.github/requirements/`를 바꾸는 PR에서 검토된 base의 CI Python lock 검사를 hosted로 실행하는 변경을 소유한다.
[Required Source Coverage](./0124-required-source-coverage/)는 조사 명세가 지정한 필수 출처 10개의 직접 열람과 여섯 관점별 지원 수준 기록을 소유한다.
[Survey Status and Local Gaps](./0125-survey-status-and-local-gaps/)는 조사 명세 148개 요구의 현재 상태 기록과 운영자 결정이 필요 없는 로컬 공백 수정을 소유한다.
[Architecture Views](./0126-architecture-views/)는 AD-0007의 C4 맥락·컨테이너·배포 뷰와 arc42 절별 점검표를 소유한다.
[ADR Lineage and Branch Strategy](./0127-adr-lineage-and-branch-strategy/)는 현재 결정이 없는 supersession chain 거부, ADR 양식 prompt·번호 비재사용 규칙과 단일 `main` branch 전략 ADR을 소유한다.
[Change Kinds and Authoring Prompts](./0128-change-kinds-and-authoring-prompts/)는 변경 종류별 최소 기록·검사·승인 표, Spec·Plan·Task 작성 prompt와 링크만 있는 운영 절의 거부를 소유한다.
[Inventory, Operations and QA Baseline](./0129-inventory-operations-and-qa-baseline/)는 추적 파일 분류, 운영 문서 중복 조사와 두 수정, staged QA 시간 기준선 기록을 소유한다.
[Archive History Link Migration](./0130-archive-history-link-migration/)는 역사 링크만 소비자인 Archive 보존 단위 12개의 링크 이관과 `git-history-only` 처분을 소유한다.
[Archive Evidence Owner Migration](./0131-archive-evidence-owner-migration/)는 현재 문서만 소비자인 Archive 보존 단위 10개의 소비자·증적 소유 문장 이관과 `git-history-only` 처분을 소유한다.
[Review Decisions and C4 Prompt](./0133-review-decisions-and-c4-prompt/)는 m0012 `DERIVED_PROPOSAL` 칸과 외부 의존 조사 항목에 대한 운영자 결정 기록과 다이어그램 작성 prompt의 C4 점검 추가를 소유한다.
SPEC-0104 완료 증적과 완료된 local GitOps platform 구현 증적은
각 package의 원본을 보존하는
[Archive Retention Catalog](../98.archive/README.md#structure)에서 찾는다.

## Usage

1. 관련 Requirement Package, AD, ADR 링크를 확인하고 Spec의 입력으로 고정한다.
2. 새 Spec은 `../99.templates/templates/specs/spec.template.md`에서 시작하고, canonical target pattern은 `docs/03.specs/<####-slug>/spec.md`다.
3. 변경 한정 설계와 수용 기준은 `spec.md`, 실행 순서·위험·예정 검증·rollback은 `plan.md`, 실제 실행·검사 사실·기준별 수용 판정은 package-local Task record가 소유한다. 범위나 근거가 승인 계약을 바꾸면 영향을 받는 Spec·Plan을 재검토한다. 실행 가능한 API 계약은 해당 Spec Package가 소유한다.
4. 장기 구조는 Stage 02 Architecture Description으로, 중요한 장기 결정은 ADR로 승격한다. 폐기된 Stage 04 경로는 새 문서에서 사용하지 않는다.
5. 종단 처분은 Stage 98 disposition이 기록한다. 끝난 package는 consumer-zero 뒤 `98.archive/completed/`에 보존하고, 대체되거나 후속 없이 철회된 단독 문서는 `superseded/` 또는 `retired/`에 본문 그대로 보존한다. 경로 이동은 본문 없는 `migrations/`가 현재 owner를 명명한다([ADR-0040](../02.architecture/decisions/0040-archive-reappraisal-and-verifiable-sources.md)). 원본 바이트는 Git history가 복구한다.

### Relative Link Rules

이 README의 링크 기준 위치는 `docs/03.specs/`다.

- 상위 문서는 `../`로 시작하는 상대 경로를 사용한다.
- 같은 stage의 package는 `./<####-numbering>-<feature-id>/` 폴더로 연결한다.
- 실행 문서는 같은 work-unit의 `plan.md`와 `tasks/tsk-####-<slug>.md`, 운영 문서는 `../05.operations/`로 연결한다.
- feature-local helper 문서 링크는 `docs/03.specs/<####-numbering>-<feature-id>/` 안의 최종 파일 위치 기준으로 다시 계산한다.

### Spec Authoring Rules

1. 모든 활성 Spec은 관련 Requirement Package와 Architecture 입력을 링크하거나 부재를 명시한다.
2. Verification은 필수다.
3. Acceptance Contract와 테스트 의도는 Requirement Package에서 이어지고, 구현 검증은 Task record와 연결된다.
4. 실행 가능한 인터페이스 계약은 실제 구현 소유 경로에 두고 Spec에서 그 owner와 검증을 추적한다.
5. Agent 변경은 목표·동작·경계·실패 조건을 Spec에, 구현 순서와 rollback을 Plan에 기록한다.
6. Feature-local Task records가 해당 work-unit의 실행과 evidence를 소유한다. Validator의 독립 실행 테스트와 fixture는 top-level `tests/`와 `tests/fixtures/` 아래에 두고, production module은 이를 import하거나 runtime data로 읽지 않는다. `validation/tests/` 또는 Spec-package-local test control plane은 만들지 않는다.
7. `Related Inputs`는 upstream 요약이고, `Related Documents`는 Requirement Package/AD/ADR와 Plan/Task/Operations 링크를 함께 담는다.

### Helper Templates

아래 템플릿은 `docs/03.specs/<####-slug>/` 패키지와 해당 Spec이 소유하는 실행 가능 인터페이스 계약에 사용한다.

- `../99.templates/templates/specs/spec.template.md`
- `../99.templates/templates/specs/plan.template.md`
- `../99.templates/templates/specs/task.template.md`

## Related Documents

- [Docs README](../README.md)
- [01.requirements](../01.requirements/README.md)
- [02.architecture/descriptions](../02.architecture/descriptions/README.md)
- [02.architecture/decisions](../02.architecture/decisions/README.md)
- [05.operations/runbooks](../05.operations/runbooks/README.md)
- [Archive Index](../98.archive/README.md)
