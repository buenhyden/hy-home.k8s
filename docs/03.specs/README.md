---
title: "03.specs"
version: "0.5.41"
type: "common/readme-stage-index"
status: "active"
owner: "platform"
updated: "2026-09-25"
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
Spec은 목표 계약을 담으므로 아직 구현되지 않은 동작을 포함할 수 있다. 관측된 구현과의 의도된 차이는
구현 대기이며, `completed`(현재 철자 `done`)는 수용 조건과 검사한 구현이 일치할 때만 인정한다. 끝난 package는
처분이 승인될 때까지 이 stage에서 기다리고, 승인되면 ADR-0040에 따라 `98.archive/completed/`에 package
단위로 원본 Git object 그대로 보존되며, Retention Catalog가 원래 경로를 한 번 명명하고 원본은 Git history가 복구한다.

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

Spec 0054 owned integrated acceptance; it is `done` and retained in
`98.archive/completed/` by [SPEC-0087](./0087-stage03-terminal-package-retention/spec.md); completed Spec 0066 owned delegated execution of WP-010 and
WP-011, and Spec 0054 WP-013 owned the current-corpus cutover.
The 2026-09-14 lifecycle reconciliation is recorded by
[SPEC-0078](../98.archive/completed/03.specs/0078-document-currency-reconciliation/spec.md).

```text
03.specs/
├── 0008-current-local-gitops-platform/
│   └── spec.md
├── 0049-platform-validation-and-security-evidence/
│   ├── spec.md
│   ├── plan.md
│   └── tasks/
├── 0072-agent-governance-and-quality-gate-consolidation/
│   ├── spec.md
│   ├── plan.md
│   └── tasks/
├── 0085-archive-reappraisal-and-document-standards/
│   ├── spec.md
│   ├── plan.md
│   └── tasks/
├── 0086-provider-native-runtime-observation/
│   ├── spec.md
│   ├── plan.md
│   └── tasks/
├── 0087-stage03-terminal-package-retention/
│   ├── spec.md
│   ├── plan.md
│   └── tasks/
├── 0088-operations-corpus-convergence/
│   ├── spec.md
│   ├── plan.md
│   └── tasks/
├── 0089-deferred-conflict-resolution/
│   ├── spec.md
│   ├── plan.md
│   └── tasks/
└── README.md
```

The 2026-09-05 Stage 03 dispositions and scope-specific evidence are recorded
in [SPEC-0054-TSK-0013](../98.archive/completed/03.specs/0054-sdlc-document-and-agent-governance-consolidation/tasks/tsk-0013-transition-only-taxonomy-terminal-cutover.md#stage-03-current-package-convergence-2026-09-05).

## Authoring Workflow

1. 관련 Requirement Package, AD, ADR 링크를 확인하고 Spec의 입력으로 고정한다.
2. 새 Spec은 `../99.templates/templates/specs/spec.template.md`에서 시작하고, canonical target pattern은 `docs/03.specs/<####-slug>/spec.md`다.
3. 변경 한정 설계와 실행 계약은 `spec.md`, 구현 순서·위험·검증·rollback은 `plan.md`, 실행 증거는 package-local Task record가 소유한다. 실행 가능한 API 계약은 해당 Spec Package가 소유한다.
4. 장기 구조는 Stage 02 Architecture Description으로, 중요한 장기 결정은 ADR로 승격한다. 폐기된 Stage 04 경로는 새 문서에서 사용하지 않는다.
5. 종단 처분은 Stage 98 disposition이 기록한다. 끝난 package는 consumer-zero 뒤 `98.archive/completed/`에 보존하고, 대체되거나 후속 없이 철회된 단독 문서는 `superseded/` 또는 `retired/`에 본문 그대로 보존한다. 경로 이동은 본문 없는 `migrations/`가 현재 owner를 명명한다([ADR-0040](../02.architecture/decisions/0040-archive-reappraisal-and-verifiable-sources.md)). 원본 바이트는 Git history가 복구한다.

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
| [`./0008-current-local-gitops-platform/spec.md`](./0008-current-local-gitops-platform/spec.md)                                     | 현재 local GitOps platform baseline Spec                                      | Active | Headlamp, ingress-nginx, ArgoCD App-of-Apps, ESO/Vault, external services, Kiali/Istio, Rollouts, Notifications, monitoring, adminer 구현 증적을 소유한다.                                                                                                                        | 2026-09-14 |
| [`./0049-platform-validation-and-security-evidence/spec.md`](./0049-platform-validation-and-security-evidence/spec.md) | Layered Kubernetes/GitOps render, schema, policy, Traefik semantics, secret, and security evidence specification | Withdrawn | 2026-09-25에 SPEC-0089로 철회했다. retired Spec 0048과 Traefik lane에 의존하고 없는 contract 위치를 가정해 현재 authority와 상충한다. 미구현 범위는 REQ-0004의 owner 없는 gap으로 남긴다. `retired/` 이동은 철회 commit이 default branch에 들어간 뒤 수행한다. | 2026-09-25 |
| [`./0072-agent-governance-and-quality-gate-consolidation/spec.md`](./0072-agent-governance-and-quality-gate-consolidation/spec.md) | Common agent governance and shared local/CI QA | Done | 공통 역할·스킬 이관, provider 연결, QA 실행 및 CI 정합성의 정적 수용을 완료했다. 2026-09-24에 request owner 승인("0072: Split the native half out and close")으로 native runtime 관측(WORK-009)을 SPEC-0086으로 이관하고 done으로 닫았다. native 결과는 통과로 주장하지 않는다. | 2026-09-24 |
| [`./0085-archive-reappraisal-and-document-standards/spec.md`](./0085-archive-reappraisal-and-document-standards/spec.md) | Archive reappraisal and document standards | Done | ADR-0040 cutover를 완료했다. default branch envelope 검증까지 구현했고 hosted `qa`가 `a264ebad`에서 통과해 2026-09-24에 done으로 닫았다. lifecycle·결과 어휘(WP-005·006)는 각자의 승인을 기다린다. | 2026-09-24 |
| [`./0086-provider-native-runtime-observation/spec.md`](./0086-provider-native-runtime-observation/spec.md) | Provider native runtime observation | Draft | 2026-09-24에 SPEC-0072에서 분리했다. Claude·Codex의 native discovery, invocation·model access, sandbox enforcement, hook event delivery 관측을 소유한다. operator가 승인한 native session만 증거가 되며, repository-static 결과로 닫을 수 없다. Task는 queued다. | 2026-09-24 |
| [`./0087-stage03-terminal-package-retention/spec.md`](./0087-stage03-terminal-package-retention/spec.md) | Stage 03 terminal package retention | Done | 2026-09-24 request owner 승인으로 withdrawn package 네 개(0047·0048·0050·0051)를 `retired/`로, done package 세 개(0054·0062·0084)를 `completed/`로 보존하고 done으로 닫았다. | 2026-09-24 |
| [`./0088-operations-corpus-convergence/spec.md`](./0088-operations-corpus-convergence/spec.md) | Operations corpus convergence | Done | 2026-09-25 request owner 요청으로 Stage 05 역할 중복·구현 drift, 검증 script의 dead·중복 logic을 local commit으로 정리했다. Stage 98 Operations 봉인 기록은 보존 근거와 제거 조건을 기록했고, hosted CI와 live 검증은 DEFER다. | 2026-09-25 |
| [`./0089-deferred-conflict-resolution/spec.md`](./0089-deferred-conflict-resolution/spec.md) | Deferred conflict resolution | Done | SPEC-0088의 deferred conflict 네 건을 해소하고 SPEC-0049를 철회했다. `retired/` 이동은 push 승인 뒤 request owner가 수행한다. | 2026-09-25 |

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
