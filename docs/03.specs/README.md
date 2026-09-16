---
title: "03.specs"
version: "0.5.15"
type: "common/readme-stage-index"
status: "active"
owner: "platform"
updated: "2026-09-16"
layer: "specs"
---
# 03.specs

> Requirement Package와 Architecture를 구현 가능한 기술 계약과 검증 기준으로 구체화하는 Spec stage다.

> [!NOTE]
> All AI agent interactions with this stage must comply with the [Agent Governance Hub](../../.agents/README.md).

## Overview

이 경로는 Requirement Package, AD, ADR을 구현 가능한 기술 계약으로
구체화하는 Spec stage다. 서비스 동작, API 계약, 변경 한정 설계와 검증
기준은 이곳에서 하위 구현과 추적 가능해야 한다.

Spec은 실행 기준을 소유하는 문서다.
활성 Spec은 현재 repo-backed 구현과 일치해야 한다. 끝난 package는 ADR-0038에 따라
`98.archive/completed/`에 package 단위로 보존되고, Retention Catalog가 원래 경로를 한 번 명명하며,
원본 바이트는 Git history가 복구한다.

### Stage Readers

이 README의 주요 독자:

- Platform Engineers
- Application Developers
- Documentation Writers
- AI Agents

## Stage Contract

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

## Document Index

A package proves its own navigation: `spec.md` owns the change contract,
`plan.md` owns implementation order and risk, and `tasks/` is the Task
inventory. The compact tree below lists the governed body families; `tasks/`
denotes package-local `TSK-*` records rather than one package-wide ledger. Spec 0054's transitional execution ledger is a
finite WP-004C input and is intentionally not presented as a current family.

A package leaves the current tree only when it is proven obsolete, completed,
duplicated, or conflicting, and then only after lifecycle normalization,
mutable consumer cutover, and Git recovery. The retained set is therefore
whatever fails all four proofs; it is derived from lifecycle state and
unfinished scope, not declared as a fixed list. The tree and table below are a
point-in-time inventory, not a permanent roster or count invariant.

Spec 0054 owns integrated acceptance; completed Spec 0066 owned delegated
execution of WP-010 and WP-011, and WP-013 owns the current-corpus cutover.
The 2026-09-14 lifecycle reconciliation is recorded by
[SPEC-0078](./0078-document-currency-reconciliation/spec.md).

```text
03.specs/
├── 0006-workspace-harness-gap-analysis/
│   └── spec.md
├── 0008-current-local-gitops-platform/
│   └── spec.md
├── 0047-current-surface-and-stash-reconciliation/
│   ├── spec.md
│   ├── plan.md
│   └── tasks/
├── 0048-github-routing-and-ci-evidence/
│   ├── spec.md
│   ├── plan.md
│   └── tasks/
├── 0049-platform-validation-and-security-evidence/
│   ├── spec.md
│   ├── plan.md
│   └── tasks/
├── 0050-example-iac-and-validator-qa/
│   ├── spec.md
│   ├── plan.md
│   └── tasks/
├── 0051-repository-assurance-integration-and-closure/
│   ├── spec.md
│   ├── plan.md
│   └── tasks/
├── 0054-sdlc-document-and-agent-governance-consolidation/
│   ├── spec.md
│   ├── plan.md
│   └── tasks/
├── 0062-workspace-research-full-corpus-reverification/
│   ├── spec.md
│   ├── plan.md
│   └── tasks/
├── 0068-agent-projection-rendering-and-gate-reduction/
│   └── spec.md
├── 0070-retired-provider-residue-disposition/
│   └── spec.md
├── 0071-document-taxonomy-and-form-identity-normalization/
│   ├── spec.md
│   ├── plan.md
│   └── tasks/
├── 0072-agent-governance-and-quality-gate-consolidation/
│   ├── spec.md
│   ├── plan.md
│   └── tasks/
├── 0077-dead-contract-and-duplicate-execution-retirement/
│   ├── plan.md
│   ├── spec.md
│   └── tasks/
├── 0078-document-currency-reconciliation/
│   ├── plan.md
│   ├── spec.md
│   └── tasks/
├── 0083-finished-package-retention/
│   ├── plan.md
│   ├── spec.md
│   └── tasks/
├── 0084-stage03-backlog-closeout/
│   ├── plan.md
│   ├── spec.md
│   └── tasks/
└── README.md
```

The 2026-09-05 Stage 03 dispositions and scope-specific evidence are recorded
in [SPEC-0054-TSK-0013](./0054-sdlc-document-and-agent-governance-consolidation/tasks/tsk-0013-transition-only-taxonomy-terminal-cutover.md#stage-03-current-package-convergence-2026-09-05).

## Authoring Workflow

1. 관련 Requirement Package, AD, ADR 링크를 확인하고 Spec의 입력으로 고정한다.
2. 새 Spec은 `../99.templates/templates/specs/spec.template.md`에서 시작하고, canonical target pattern은 `docs/03.specs/<####-slug>/spec.md`다.
3. 변경 한정 설계와 실행 계약은 `spec.md`, 구현 순서·위험·검증·rollback은 `plan.md`, 실행 증거는 package-local Task record가 소유한다. 실행 가능한 API 계약은 해당 Spec Package가 소유한다.
4. 장기 구조는 Stage 02 Architecture Description으로, 중요한 장기 결정은 ADR로 승격한다. 폐기된 Stage 04 경로는 새 문서에서 사용하지 않는다.
5. 종단 처분은 Stage 98 disposition이 기록한다. 끝난 package는 consumer-zero 뒤 `98.archive/completed/`에 보존하고, 대체되거나 후속 없이 철회된 단독 문서는 `superseded/` 또는 `retired/`에 본문 그대로 보존한다. 경로 이동은 본문 없는 `migrations/`가 현재 owner를 명명한다([ADR-0039](../02.architecture/decisions/0039-unit-archive-retention-and-citation-table.md)). 원본 바이트는 Git history가 복구한다.

### Relative Link Rules

이 README의 링크 기준 위치는 `docs/03.specs/`다.

- 상위 문서는 `../`로 시작하는 상대 경로를 사용한다.
- 같은 stage의 spec은 `./<####-numbering>-<feature-id>/spec.md`로 연결한다.
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

### Current Spec Index

| 문서                                                                                                                             | 설명                                                                          | 상태   | 현재성                                                                                                                                                                                                                                                                            | 최종 수정  |
| -------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | ------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| [`./0006-workspace-harness-gap-analysis/spec.md`](./0006-workspace-harness-gap-analysis/spec.md)                                   | Workspace harness Gap analysis와 제한 구현 계약                               | Active | 2026-09-05 재관찰: historical harness-gap baseline과 미완료 runtime/operator 경계 때문에 active를 유지한다. Plan/Task 부재는 완료 증거가 아니며, 실행이나 완료 입증 후 별도 disposition이 필요하다. 새 Plan/Task나 runtime 증거는 만들지 않았다. | 2026-09-14 |
| [`./0008-current-local-gitops-platform/spec.md`](./0008-current-local-gitops-platform/spec.md)                                     | 현재 local GitOps platform baseline Spec                                      | Active | Headlamp, ingress-nginx, ArgoCD App-of-Apps, ESO/Vault, external services, Kiali/Istio, Rollouts, Notifications, monitoring, adminer 구현 증적을 소유한다.                                                                                                                        | 2026-09-14 |
| [`./0047-current-surface-and-stash-reconciliation/spec.md`](./0047-current-surface-and-stash-reconciliation/spec.md) | Current target inventory, canonical ownership, audit delta, protected boundary, and stash semantic reconciliation specification | Active | Spec 0052의 semantic closure 후 ADR-0031/0033와 package-local v9 경로로 Spec/Plan을 재개했다. 활성화 Task만 done이고 구현 Tasks는 queued다. stash metadata는 존재하며 tracked-hunk reconciliation은 미완료다. | 2026-09-14 |
| [`./0048-github-routing-and-ci-evidence/spec.md`](./0048-github-routing-and-ci-evidence/spec.md) | GitHub surface routing, label/CODEOWNERS parity, CI lane ownership, and read-only remote evidence specification | Draft | Spec/Plan draft, Tasks queued를 유지한다. Spec 0047의 검증된 package closure 뒤 package-local draft → active 경로로 재개한다. 제안된 GitHub projection contract/validator 구현은 미완료이며 ADR-0021은 superseded 이력이다. | 2026-09-14 |
| [`./0049-platform-validation-and-security-evidence/spec.md`](./0049-platform-validation-and-security-evidence/spec.md) | Layered Kubernetes/GitOps render, schema, policy, Traefik semantics, secret, and security evidence specification | Draft | Spec/Plan draft, Tasks queued를 유지한다. Spec 0048의 검증된 package closure 뒤 package-local draft → active 경로로 재개한다. Kustomize roots는 존재하지만 제안된 platform/Traefik validator 작업은 미완료다. | 2026-09-14 |
| [`./0050-example-iac-and-validator-qa/spec.md`](./0050-example-iac-and-validator-qa/spec.md) | AWS Terraform, Azure Bicep, example routing, and validator regression QA specification | Draft | Spec/Plan draft, Tasks queued를 유지한다. Spec 0049의 검증된 package closure 뒤 package-local draft → active 경로로 재개한다. 현재 validation registry에 Terraform/Bicep validator가 없어 example IaC 작업은 미완료다. | 2026-09-14 |
| [`./0051-repository-assurance-integration-and-closure/spec.md`](./0051-repository-assurance-integration-and-closure/spec.md) | Cross-tranche integration, lifecycle closure, local main merge, stash retirement, and cleanup specification | Draft | Spec/Plan draft, Tasks queued를 유지한다. Spec 0050의 검증된 package closure 뒤 package-local draft → active 경로로 재개한다. 선행 구현·통합·stash retirement는 완료되지 않았으며 새 merge/cleanup 권한은 없다. | 2026-09-14 |
| [`./0054-sdlc-document-and-agent-governance-consolidation/spec.md`](./0054-sdlc-document-and-agent-governance-consolidation/spec.md) | SDLC document and AI-agent governance consolidation specification | Active | 승인된 B 범위(Stage 90 포함)의 통합 수용 소유자로서 문서·agent governance·operations·reference·archive·template 수렴을 관리하고, WP-010/WP-011 실행은 리뷰된 활성화 경계 이후 Spec 0066에 위임한다. | 2026-09-07 |
| [`./0062-workspace-research-full-corpus-reverification/spec.md`](./0062-workspace-research-full-corpus-reverification/spec.md) | Full-corpus external-source and workspace reverification design over the existing WER research pack | Active | 2026-09-05 재관찰: 7 done/3 blocked Tasks를 유지하고, 작업 완료를 기록한 TSK-0011은 2026-09-14에 queued에서 in-progress로 옮겼다. 승인된 2026-08-29 administrative-closeout addendum이 미래의 기존 Path B replay를 대체한다. current index/link/census 정합성, fresh canonical local validation과 independent review 이후 별도 종료하며, 과거 미충족 증거는 PASS로 바꾸지 않는다. | 2026-09-07 |
| [`./0068-agent-projection-rendering-and-gate-reduction/spec.md`](./0068-agent-projection-rendering-and-gate-reduction/spec.md) | Prior renderer proposal | Superseded | SPEC-0072가 `.agents/` 공통 원본과 명시적 네이티브 참조로 대체한다. 이전 제안은 구현 증거가 아니다. | 2026-09-05 |
| [`./0070-retired-provider-residue-disposition/spec.md`](./0070-retired-provider-residue-disposition/spec.md) | Prior residue disposition proposal | Superseded | SPEC-0072가 항목별 현행·역사 구분과 처분을 소유한다. Task 4의 sealed-ledger와 Git recovery 증거는 역사 기록으로 보존하며, 과거 문서의 일괄 불변 예외는 현재 권위가 아니다. | 2026-09-06 |
| [`./0071-document-taxonomy-and-form-identity-normalization/spec.md`](./0071-document-taxonomy-and-form-identity-normalization/spec.md) | Family/kind profile identity, stage-free layer, semantic version, and Stage 99 form naming | Done | 문서 profile 식별자의 `<family>/<kind>` 통일, stage 접두어 없는 `layer`, 3요소 semver, Stage 99 form 이동(MIG-0010), strict 실행에서 평가되는 `frontmatter.schema.json`이 이미 구현되어 있다. 2026-09-14에 draft에서 active로 옮겼고, 검증 13개가 모두 증거를 갖춘 상태에서 2026-09-16에 SPEC-0084 회차로 done 종료했다. | 2026-09-14 |
| [`./0072-agent-governance-and-quality-gate-consolidation/spec.md`](./0072-agent-governance-and-quality-gate-consolidation/spec.md) | Common agent governance and shared local/CI QA | Active | 공통 역할·스킬 이관, provider 연결, QA 실행 및 CI 정합성을 구현한다. 현재 실행 증거는 패키지 Task가 소유한다. | 2026-09-09 |
| [`./0077-dead-contract-and-duplicate-execution-retirement/spec.md`](./0077-dead-contract-and-duplicate-execution-retirement/spec.md) | Retirement of unreachable validation code, absent-subject assertions, and same-snapshot duplicate gate execution | Active | 기준선 `qa.py full`이 22/22 PASS인 상태에서 green이 드러내지 못하는 결함을 처분한다. 도달 불가능한 cross-document 서브트리와 수집되지 않는 test class, 대상이 사라진 cutover pin, `unit-tests` 안에서 같은 snapshot에 재실행되는 등록 gate, 코퍼스가 실천하지 않는 skill 의무를 제거하고 archive cutover 워크플로에 소유 skill을 부여한다. Gate 의미, 문서 route, profile, 링크 경계 동작은 바뀌지 않는다. | 2026-09-14 |
| [`./0078-document-currency-reconciliation/spec.md`](./0078-document-currency-reconciliation/spec.md) | Reconciliation of stale and implementation-conflicting document statements and Stage 03 lifecycle state | Draft | `docs/` 전반에서 현재 구현과 다른 명령·경로·리소스 이름·버전·결정 서술을 근거와 함께 바로잡고, 구현되었거나 후속 작업으로 대체된 Stage 03 package를 다음 단일 lifecycle edge로 옮긴다. 미완료 작업은 구현하지 않고 처분과 차단 사유만 기록한다. | 2026-09-14 |
| [`./0083-finished-package-retention/spec.md`](./0083-finished-package-retention/spec.md) | Retention of the finished Stage 03 packages | Done | 완료된 package 열 개를 `completed/`에 단위 그대로 보존하고 소비자를 먼저 옮기며, 구현 전에 대체된 제안 두 개는 계약 충돌로 보존이 막힌 사실과 잔류하는 열여섯 개의 잔류 사유를 기록하고, 보존이 어긋나게 만든 소비자를 수리한다. | 2026-09-16 |
| [`./0084-stage03-backlog-closeout/spec.md`](./0084-stage03-backlog-closeout/spec.md) | Stage 03 잔류 package의 종결 처분 | Active | 잔류한 Stage 03 package를 기록된 증거에 따라 종결 상태로 옮기거나 날짜 박힌 잔류 사유를 남기고, 그 처분을 막던 registry 공백 두 곳(`sdlc/spec`의 `superseded_by` optional 키, `spec-plan`의 draft에서 withdrawn 간선)을 메우며, 중복된 frontmatter reader를 한 소유자로 수렴시키고, 종결된 단위를 보존한 뒤 그 이동이 어긋나게 만든 소비자를 수리한다. | 2026-09-16 |

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
