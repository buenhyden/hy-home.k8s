---
title: "03.specs"
version: "0.1.0"
type: "common/readme-stage-index"
status: "active"
owner: "platform"
updated: "2026-09-05"
layer: "specs"
---
# 03.specs

> Requirement Package와 Architecture를 구현 가능한 기술 계약과 검증 기준으로 구체화하는 Spec stage다.

> [!NOTE]
> All AI agent interactions with this stage must comply with the [Agent Governance Hub](../00.agent-governance/README.md).

## Overview

이 경로는 Requirement Package, AD, ADR을 구현 가능한 기술 계약으로
구체화하는 Spec stage다. 서비스 동작, API 계약, 변경 한정 설계와 검증
기준은 이곳에서 하위 구현과 추적 가능해야 한다.

Spec은 실행 기준을 소유하는 문서다.
활성 Spec은 현재 repo-backed 구현과 일치해야 한다. superseded 또는 삭제된 경로의 전체 본문은
Git history에서 복구하고, Stage 98에는 registry가 요구하는 Migration 또는 최소 Tombstone lookup만
남긴다.

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

An earlier revision of this paragraph named `0004`, `0005`, `0008`, `0054`, and
`0066` as the retained set. That list has since drifted from the derivation: it
names `0066` after it reached `done`, and it omits every package still holding
unfinished scope. Read it as the reviewed removal candidate of its date rather
than as the rule. Spec 0054 owns integrated acceptance; completed Spec 0066
owned delegated execution of WP-010 and WP-011 through its package-local Plan
and Task, and WP-013 owns the current-corpus cutover that resolves the rest.

```text
03.specs/
├── 0004-argo-rollouts-progressive-delivery/
│   ├── spec.md
│   ├── plan.md
│   └── tasks/
├── 0005-argo-notifications-slack/
│   ├── spec.md
│   ├── plan.md
│   └── tasks/
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
├── 0052-document-taxonomy-consolidation/
│   ├── spec.md
│   ├── plan.md
│   └── tasks/
├── 0054-sdlc-document-and-agent-governance-consolidation/
│   ├── spec.md
│   └── plan.md
├── 0062-workspace-research-full-corpus-reverification/
│   ├── spec.md
│   ├── plan.md
│   └── tasks/
├── 0068-agent-projection-rendering-and-gate-reduction/
│   ├── spec.md
│   └── tasks/
├── 0070-retired-provider-residue-disposition/
│   ├── spec.md
│   └── tasks/
├── 0071-document-taxonomy-and-form-identity-normalization/
│   ├── spec.md
│   ├── plan.md
│   └── tasks/
└── README.md
```

The 2026-09-05 Stage 03 dispositions and scope-specific evidence are recorded
in [SPEC-0054-TSK-0013](./0054-sdlc-document-and-agent-governance-consolidation/tasks/tsk-0013-transition-only-taxonomy-terminal-cutover.md#stage-03-current-package-convergence-2026-09-05).
Spec 0052 remains here as a dependency-ordered intermediate state: terminal
status alone does not establish consumer-zero or authorize retention before
the later current-consumer and Archive-link units.

## Authoring Workflow

1. 관련 Requirement Package, AD, ADR 링크를 확인하고 Spec의 입력으로 고정한다.
2. 새 Spec은 `../99.templates/templates/specs/spec.template.md`에서 시작하고, canonical target pattern은 `docs/03.specs/<####-slug>/spec.md`다.
3. 변경 한정 설계와 실행 계약은 `spec.md`, 구현 순서·위험·검증·rollback은 `plan.md`, 실행 증거는 package-local Task record가 소유한다. 실행 가능한 API 계약은 해당 Spec Package가 소유한다.
4. 장기 구조는 Stage 02 Architecture Description으로, 중요한 장기 결정은 ADR로 승격한다. 폐기된 Stage 04 경로는 새 문서에서 사용하지 않는다.
5. 삭제된 경로의 이전 본문은 Git history가 보존한다. 실제 immutable lookup이 Git만으로 해소되지 않을 때만 Stage 98 Migration을 사용하고, Tombstone은 Git과 Migration 모두로 해결되지 않을 때만 최소 형태로 둔다.

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
4. API가 있다면 실행 가능한 OpenAPI/GraphQL/Proto 계약을 해당 Spec Package에 함께 둔다.
5. Agent 변경은 목표·동작·경계·실패 조건을 Spec에, 구현 순서와 rollback을 Plan에 기록한다.
6. Feature-local Task records가 해당 work-unit의 실행과 evidence를 소유한다. Validator의 독립 실행 테스트와 fixture는 top-level `tests/`와 `tests/fixtures/` 아래에 두고, production module은 이를 import하거나 runtime data로 읽지 않는다. `validation/tests/` 또는 Spec-package-local test control plane은 만들지 않는다.
7. `Related Inputs`는 upstream 요약이고, `Related Documents`는 Requirement Package/AD/ADR와 Plan/Task/Operations 링크를 함께 담는다.

### Current Spec Index

| 문서                                                                                                                             | 설명                                                                          | 상태   | 현재성                                                                                                                                                                                                                                                                            | 최종 수정  |
| -------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | ------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| [`./0004-argo-rollouts-progressive-delivery/spec.md`](./0004-argo-rollouts-progressive-delivery/spec.md)                           | Argo Rollouts 점진적 배포 current-contract backfill 명세                      | Active | `platform-rollouts` Application, dashboard, metrics, AppProject 권한, 앱 canary AnalysisTemplate 경계를 현재 계약으로 정리한다. 구현 evidence는 Spec의 Implementation Status를 따른다.                                                                                            | 2026-06-04 |
| [`./0005-argo-notifications-slack/spec.md`](./0005-argo-notifications-slack/spec.md)                                               | ArgoCD Notifications Slack current-contract backfill 명세                     | Active | ArgoCD Notifications, Vault/ESO credential boundary, template/trigger 계약을 현재 기준으로 정리한다. 구현 evidence는 Spec의 Implementation Status를 따른다.                                                                                                                       | 2026-05-22 |
| [`./0006-workspace-harness-gap-analysis/spec.md`](./0006-workspace-harness-gap-analysis/spec.md)                                   | Workspace harness Gap analysis와 제한 구현 계약                               | Active | 2026-09-05 재관찰: historical harness-gap baseline과 미완료 runtime/operator 경계 때문에 active를 유지한다. Plan/Task 부재는 완료 증거가 아니며, 실행이나 완료 입증 후 별도 disposition이 필요하다. 새 Plan/Task나 runtime 증거는 만들지 않았다. | 2026-07-13 |
| [`./0008-current-local-gitops-platform/spec.md`](./0008-current-local-gitops-platform/spec.md)                                     | 현재 local GitOps platform baseline Spec                                      | Active | Headlamp, ingress-nginx, ArgoCD App-of-Apps, ESO/Vault, external services, Kiali/Istio, Rollouts, Notifications, monitoring, adminer 구현 증적을 소유한다.                                                                                                                        | 2026-06-02 |
| [`./0047-current-surface-and-stash-reconciliation/spec.md`](./0047-current-surface-and-stash-reconciliation/spec.md) | Current target inventory, canonical ownership, audit delta, protected boundary, and stash semantic reconciliation specification | Active | Spec 0052의 semantic closure 후 ADR-0031/0033와 package-local v9 경로로 Spec/Plan을 재개했다. 활성화 Task만 done이고 구현 Tasks는 queued다. stash metadata는 존재하며 tracked-hunk reconciliation은 미완료다. | 2026-09-05 |
| [`./0048-github-routing-and-ci-evidence/spec.md`](./0048-github-routing-and-ci-evidence/spec.md) | GitHub surface routing, label/CODEOWNERS parity, CI lane ownership, and read-only remote evidence specification | Draft | Spec/Plan draft, Tasks queued를 유지한다. Spec 0047의 검증된 package closure 뒤 package-local draft → active 경로로 재개한다. 제안된 GitHub projection contract/validator 구현은 미완료이며 ADR-0021은 superseded 이력이다. | 2026-09-05 |
| [`./0049-platform-validation-and-security-evidence/spec.md`](./0049-platform-validation-and-security-evidence/spec.md) | Layered Kubernetes/GitOps render, schema, policy, Traefik semantics, secret, and security evidence specification | Draft | Spec/Plan draft, Tasks queued를 유지한다. Spec 0048의 검증된 package closure 뒤 package-local draft → active 경로로 재개한다. Kustomize roots는 존재하지만 제안된 platform/Traefik validator 작업은 미완료다. | 2026-09-05 |
| [`./0050-example-iac-and-validator-qa/spec.md`](./0050-example-iac-and-validator-qa/spec.md) | AWS Terraform, Azure Bicep, example routing, and validator regression QA specification | Draft | Spec/Plan draft, Tasks queued를 유지한다. Spec 0049의 검증된 package closure 뒤 package-local draft → active 경로로 재개한다. 현재 validation registry에 Terraform/Bicep validator가 없어 example IaC 작업은 미완료다. | 2026-09-05 |
| [`./0051-repository-assurance-integration-and-closure/spec.md`](./0051-repository-assurance-integration-and-closure/spec.md) | Cross-tranche integration, lifecycle closure, local main merge, stash retirement, and cleanup specification | Draft | Spec/Plan draft, Tasks queued를 유지한다. Spec 0050의 검증된 package closure 뒤 package-local draft → active 경로로 재개한다. 선행 구현·통합·stash retirement는 완료되지 않았으며 새 merge/cleanup 권한은 없다. | 2026-09-05 |
| [`./0052-document-taxonomy-consolidation/spec.md`](./0052-document-taxonomy-consolidation/spec.md) | Stage 03 work-unit migration, governance authority, agent controls, disposition, and validator reconciliation specification | Done | 17개 done Tasks의 완료/Spec 0054 이관 증거와 VAL-WDTC-015/016 semantic 검증에 따라 Spec/Plan을 종료했다. 과거 census는 ADR-0031에 따라 이력으로 보존한다. ADR-0032 terminal 전제는 충족하지만 WP-013의 current consumer 이관·consumer-zero/link proof·migration 전까지 이 경로에 유지한다. | 2026-09-05 |
| [`./0054-sdlc-document-and-agent-governance-consolidation/spec.md`](./0054-sdlc-document-and-agent-governance-consolidation/spec.md) | SDLC document and AI-agent governance consolidation specification | Active | 승인된 B 범위(Stage 90 포함)의 통합 수용 소유자로서 문서·agent governance·operations·reference·archive·template 수렴을 관리하고, WP-010/WP-011 실행은 리뷰된 활성화 경계 이후 Spec 0066에 위임한다. | 2026-08-31 |
| [`./0062-workspace-research-full-corpus-reverification/spec.md`](./0062-workspace-research-full-corpus-reverification/spec.md) | Full-corpus external-source and workspace reverification design over the existing WER research pack | Active | 2026-09-05 재관찰: 7 done/3 blocked Tasks를 그대로 유지한다. 승인된 2026-08-29 administrative-closeout addendum이 미래의 기존 Path B replay를 대체한다. current index/link/census 정합성, fresh canonical local validation과 independent review 이후 별도 종료하며, 과거 미충족 증거는 PASS로 바꾸지 않는다. | 2026-08-29 |
| [`./0068-agent-projection-rendering-and-gate-reduction/spec.md`](./0068-agent-projection-rendering-and-gate-reduction/spec.md) | Registry-rendered agent projections and agent-surface gate reduction | Draft | Claude/Codex 역할 투영을 `.agents/registry.json`에서 렌더하는 산출물로 바꾸고, 티어→모델 바인딩을 티어를 이미 소유한 레지스트리로 옮긴다. 손으로 유지되던 중복이 사라지면서 질문 자체가 없어지는 validator와 fixture를 폐기한다. ADR-0030의 thin-projection·Stage 90 evidence·three-responsibility 조항에 대한 적합성 수복이다. | 2026-09-02 |
| [`./0070-retired-provider-residue-disposition/spec.md`](./0070-retired-provider-residue-disposition/spec.md) | Disposition of Gemini/Antigravity residue left by ADR-0030 | Draft | ADR-0030이 제거한 프로바이더의 잔재 667건 중, 살아있는 경로 패턴·훅 분기·라벨 glob·테스트 환경변수 4곳과 현행 상태로 제거된 프로바이더를 후보로 제시하는 AD-0006·REQ-0003 2건만 정리한다. 닫힌 기록, superseded ADR, Stage 98 봉인 원장, Stage 90 관측, 부재 증명 테스트, 자격증명 denylist는 보존한다. | 2026-09-02 |
| [`./0071-document-taxonomy-and-form-identity-normalization/spec.md`](./0071-document-taxonomy-and-form-identity-normalization/spec.md) | Family/kind profile identity, stage-free layer, semantic version, and Stage 99 form naming | Draft | 문서 profile 식별자를 `<family>/<kind>`로 통일하고, `layer`에서 stage 정렬 접두어를 제거하며, `version`을 기계 계약이 이미 쓰는 3요소 semver로 맞춘다. Stage 99 form 12개는 자신이 만드는 문서 이름으로 옮기고 governance form 하나를 여섯 kind로 나눈다. 소비자가 없던 `frontmatter.schema.json`을 strict 실행마다 평가되는 계약으로 만든다. Stage 98 봉인 계약은 세대별로 분기하고 form 이동은 MIG-0010으로 봉인한다. | 2026-09-02 |

### Helper Templates

아래 템플릿은 `docs/03.specs/<####-slug>/` 패키지와 해당 Spec이 소유하는 실행 가능 인터페이스 계약에 사용한다.

- `../99.templates/templates/specs/spec.template.md`
- `../99.templates/templates/specs/plan.template.md`
- `../99.templates/templates/specs/task.template.md`
- `../99.templates/templates/specs/contracts/openapi.template.yaml`
- `../99.templates/templates/specs/contracts/service.template.proto`
- `../99.templates/templates/specs/contracts/schema.template.graphql`

## Related Documents

- [Docs README](../README.md)
- [01.requirements](../01.requirements/README.md)
- [02.architecture/descriptions](../02.architecture/descriptions/README.md)
- [02.architecture/decisions](../02.architecture/decisions/README.md)
- [05.operations/runbooks](../05.operations/runbooks/README.md)
- [Archive Index](../98.archive/README.md)
