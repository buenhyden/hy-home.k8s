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

Every package owns a thin `README.md` router. The compact tree below lists the
governed body families; `tasks/` denotes package-local `TSK-*` records rather
than one package-wide ledger. Spec 0054's transitional execution ledger is a
finite WP-004C input and is intentionally not presented as a current family.

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
├── 0009-workspace-harness-research-pack/
│   ├── spec.md
│   ├── plan.md
│   └── tasks/
├── 0010-workspace-harness-implementation-audit-pack/
│   ├── spec.md
│   ├── plan.md
│   └── tasks/
├── 0011-template-contract-governance-migration/
│   ├── spec.md
│   ├── plan.md
│   └── tasks/
├── 0012-template-governance-audit-enhancement/
│   ├── spec.md
│   ├── plan.md
│   └── tasks/
├── 0013-workspace-document-governance-hardening/
│   ├── spec.md
│   ├── plan.md
│   └── tasks/
├── 0014-workspace-document-contract-normalization/
│   ├── spec.md
│   ├── plan.md
│   └── tasks/
├── 0015-agent-governance-contract-normalization/
│   ├── spec.md
│   ├── plan.md
│   └── tasks/
├── 0016-active-control-surface-governance-hardening/
│   ├── spec.md
│   ├── plan.md
│   └── tasks/
├── 0017-workspace-engineering-research-pack/
│   ├── spec.md
│   ├── plan.md
│   └── tasks/
├── 0018-workspace-engineering-implementation-audit-pack/
│   ├── spec.md
│   ├── plan.md
│   └── tasks/
├── 0019-template-path-numbering-contract/
│   ├── spec.md
│   ├── plan.md
│   └── tasks/
├── 0020-workspace-contract-governance-normalization/
│   ├── spec.md
│   ├── plan.md
│   └── tasks/
├── 0021-sdlc-lifecycle-contract/
│   ├── spec.md
│   ├── plan.md
│   └── tasks/
├── 0022-control-cloud-doc-normalization/
│   ├── spec.md
│   ├── plan.md
│   └── tasks/
├── 0023-stage03-04-repo-static-gap-closure/
│   ├── spec.md
│   ├── plan.md
│   └── tasks/
├── 0024-observability-and-network-review-agents/
│   ├── spec.md
│   ├── plan.md
│   └── tasks/
├── 0025-governance-owner-and-roster-currentness/
│   ├── spec.md
│   ├── plan.md
│   └── tasks/
├── 0026-document-contract-registry/
│   ├── spec.md
│   ├── plan.md
│   └── tasks/
├── 0027-template-contract-consolidation/
│   ├── spec.md
│   ├── plan.md
│   └── tasks/
├── 0028-readme-workspace-profiles/
│   ├── spec.md
│   ├── plan.md
│   └── tasks/
├── 0029-semantic-document-validation/
│   ├── spec.md
│   ├── plan.md
│   └── tasks/
├── 0030-authored-document-migration/
│   ├── spec.md
│   ├── plan.md
│   └── tasks/
├── 0031-affected-surface-agent-qa/
│   └── spec.md
├── 0032-protected-surface-supply-chain-hardening/
│   └── spec.md
├── 0033-template-lifecycle-contract-normalization/
│   └── spec.md
├── 0034-authority-and-lineage-foundation/
│   └── spec.md
├── 0035-document-schema-and-lifecycle-contract/
│   └── spec.md
├── 0036-archive-record-and-workspace-boundary/
│   └── spec.md
├── 0037-active-corpus-and-execution-retention/
│   ├── spec.md
│   ├── plan.md
│   └── tasks/
├── 0038-reference-information-architecture/
│   ├── spec.md
│   ├── plan.md
│   └── tasks/
├── 0039-github-ci-qa-evidence/
│   ├── spec.md
│   ├── plan.md
│   └── tasks/
├── 0040-contract-cutover-and-program-closure/
│   ├── spec.md
│   ├── plan.md
│   └── tasks/
├── 0041-stage-00-agent-governance-contract/
│   ├── spec.md
│   ├── plan.md
│   └── tasks/
├── 0042-provider-native-runtime-and-model-evidence/
│   ├── spec.md
│   ├── plan.md
│   └── tasks/
├── 0043-agent-harness-loop-lifecycle/
│   ├── spec.md
│   ├── plan.md
│   └── tasks/
├── 0044-agent-roster-evaluation-and-admission/
│   ├── spec.md
│   ├── plan.md
│   └── tasks/
├── 0045-agent-governance-ci-qa-cutover/
│   ├── spec.md
│   ├── plan.md
│   └── tasks/
├── 0046-agent-governance-program-closure/
│   ├── spec.md
│   ├── plan.md
│   └── tasks/
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
├── 0053-workspace-engineering-research-pack-consolidation/
│   ├── spec.md
│   ├── plan.md
│   └── tasks/
├── 0054-sdlc-document-and-agent-governance-consolidation/
│   ├── spec.md
│   └── plan.md
├── 0055-workspace-governance-audit-and-remediation/
│   ├── spec.md
│   ├── plan.md
│   └── tasks/
├── 0056-workspace-engineering-gap-only-refresh/
│   ├── spec.md
│   ├── plan.md
│   └── tasks/
├── 0057-workspace-engineering-partial-defer-incremental-refresh/
│   ├── spec.md
│   ├── plan.md
│   └── tasks/
├── 0058-workspace-research-consistency-and-partial-refresh/
│   ├── spec.md
│   ├── plan.md
│   └── tasks/
├── 0059-workspace-research-full-corpus-refresh/
│   ├── spec.md
│   ├── plan.md
│   └── tasks/
├── 0060-platform-currency-defect-closure/
│   ├── spec.md
│   ├── plan.md
│   └── tasks/
├── 0061-workload-security-context-baseline/
│   ├── spec.md
│   ├── plan.md
│   └── tasks/
├── 0062-workspace-research-full-corpus-reverification/
│   ├── spec.md
│   ├── plan.md
│   └── tasks/
├── 0063-governance-invariant-consolidation/
│   ├── spec.md
│   ├── plan.md
│   └── tasks/
├── 0064-agent-governance-surface-consolidation/
│   ├── spec.md
│   ├── plan.md
│   └── tasks/
└── README.md
```

## Authoring Workflow

1. 관련 Requirement Package, AD, ADR 링크를 확인하고 Spec의 입력으로 고정한다.
2. 새 Spec은 `../99.templates/templates/sdlc/specs/spec.template.md`에서 시작하고, canonical target pattern은 `docs/03.specs/<####-numbering>-<feature-id>/spec.md`다.
3. 변경 한정 설계와 실행 계약은 `spec.md`, 구현 순서·위험·검증·rollback은 `plan.md`, 실행 증거는 package-local Task record가 소유한다. 실행 가능한 API 계약은 해당 Spec Package가 소유한다.
4. 장기 구조는 Stage 02 Architecture Description으로, 중요한 장기 결정은 ADR로 승격한다. 폐기된 Stage 04 경로는 새 문서에서 사용하지 않는다.
5. 삭제된 경로의 이전 본문은 Git history가 보존하며, 필요한 lookup/recovery만 Stage 98 Migration 또는 Tombstone이 기록한다.

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
6. Feature-local Task records가 해당 work-unit의 실행과 evidence를 소유하며 executable tests는 production module과 함께 둔다.
7. `Related Inputs`는 upstream 요약이고, `Related Documents`는 Requirement Package/AD/ADR와 Plan/Task/Operations 링크를 함께 담는다.

### Current Spec Index

| 문서                                                                                                                             | 설명                                                                          | 상태   | 현재성                                                                                                                                                                                                                                                                            | 최종 수정  |
| -------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | ------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| [`./0004-argo-rollouts-progressive-delivery/spec.md`](./0004-argo-rollouts-progressive-delivery/spec.md)                           | Argo Rollouts 점진적 배포 current-contract backfill 명세                      | Active | `platform-rollouts` Application, dashboard, metrics, AppProject 권한, 앱 canary AnalysisTemplate 경계를 현재 계약으로 정리한다. 구현 evidence는 Spec의 Implementation Status를 따른다.                                                                                            | 2026-06-04 |
| [`./0005-argo-notifications-slack/spec.md`](./0005-argo-notifications-slack/spec.md)                                               | ArgoCD Notifications Slack current-contract backfill 명세                     | Active | ArgoCD Notifications, Vault/ESO credential boundary, template/trigger 계약을 현재 기준으로 정리한다. 구현 evidence는 Spec의 Implementation Status를 따른다.                                                                                                                       | 2026-05-22 |
| [`./0006-workspace-harness-gap-analysis/spec.md`](./0006-workspace-harness-gap-analysis/spec.md)                                   | Workspace harness Gap analysis와 제한 구현 계약                               | Active | WSL2, WSL Linux native Docker, k3d, ArgoCD GitOps, SDD lifecycle, QA, CI/CD, Agent governance의 repo-static 개선 범위를 정의한다. P3 repo desired-state 보완은 별도 실행 증적에 반영됐고, live runtime 검증·secret value 확인·CI ruleset/pinning 정책은 deferred item으로 남긴다. | 2026-07-11 |
| [`./0008-current-local-gitops-platform/spec.md`](./0008-current-local-gitops-platform/spec.md)                                     | 현재 local GitOps platform baseline Spec                                      | Active | Headlamp, ingress-nginx, ArgoCD App-of-Apps, ESO/Vault, external services, Kiali/Istio, Rollouts, Notifications, monitoring, adminer 구현 증적을 소유한다.                                                                                                                        | 2026-06-02 |
| [`./0009-workspace-harness-research-pack/spec.md`](./0009-workspace-harness-research-pack/spec.md)                                 | Workspace harness/loop engineering research pack 명세                         | Done   | `docs/90.references/research/` 아래 통합 연구 팩의 구조, 공식 외부 소스 우선순위, market scan 경계, implementation checklist 포함 방식, 검증 기준을 정의한다.                                                                                                                     | 2026-07-11 |
| [`./0010-workspace-harness-implementation-audit-pack/spec.md`](./0010-workspace-harness-implementation-audit-pack/spec.md)         | Workspace harness/loop implementation audit pack 명세                         | Done   | `docs/90.references/research/` 기준 모델과 repo-backed evidence를 대조해 `docs/90.references/audits/` 아래 4개 구현 현황 감사 보고서와 README를 작성하는 계약을 정의한다.                                                                                                         | 2026-07-11 |
| [`./0011-template-contract-governance-migration/spec.md`](./0011-template-contract-governance-migration/spec.md)                   | Template contract와 governance migration 명세                                 | Done   | `docs/99.templates/`를 template forms와 support contracts로 분리하고, frontmatter schema, validator, hook, governance, authored docs 적용을 4단계 migration으로 정의한다.                                                                                                         | 2026-07-11 |
| [`./0012-template-governance-audit-enhancement/spec.md`](./0012-template-governance-audit-enhancement/spec.md)                     | Template governance follow-up audit와 선택 보강 명세                          | Done   | 이미 완료된 template contract migration 위에서 `docs/99.templates/**`, support contracts, Stage 00 routing, validator, authored docs 사용 상태를 audit-first로 검증하고 안정적인 보강 범위를 정의한다.                                                                            | 2026-07-11 |
| [`./0013-workspace-document-governance-hardening/spec.md`](./0013-workspace-document-governance-hardening/spec.md)                 | Workspace document type, provider entrypoint, CI/QA governance hardening 명세 | Done   | template/frontmatter contracts, provider shims, README scope, workspace-wide authored docs, and repo-static validation을 staged governance hardening 흐름으로 정렬한다.                                                                                                           | 2026-07-11 |
| [`./0014-workspace-document-contract-normalization/spec.md`](./0014-workspace-document-contract-normalization/spec.md)             | Workspace document contract normalization 명세                                | Done   | active 문서와 historical evidence까지 frontmatter, section, template 계약에 맞게 전면 정규화하고, 과거 증거는 current contract와 분리된 섹션으로 보존하는 후속 패스를 정의한다.                                                                                                   | 2026-07-11 |
| [`./0015-agent-governance-contract-normalization/spec.md`](./0015-agent-governance-contract-normalization/spec.md)                 | Agent governance contract normalization 명세                                  | Done   | Stage 00, Claude/Codex native role files, repository-local baselines, local/Antigravity `.agents/**`, exact wiring surfaces, absent/`DEFER` Gemini CLI native boundary, QA/CI 정규화 범위를 정의한다. | 2026-07-14 |
| [`./0016-active-control-surface-governance-hardening/spec.md`](./0016-active-control-surface-governance-hardening/spec.md)         | Active control surface governance hardening 명세                              | Done   | `.github`, `scripts`, `gitops`, `infrastructure`, `policy`, `tests`, `traefik`, `examples/sample-app`의 active 운영 표면을 보강하고 AWS/Azure cloud examples는 dated snapshot으로 유지하는 계약을 정의한다.                                                                       | 2026-07-11 |
| [`./0017-workspace-engineering-research-pack/spec.md`](./0017-workspace-engineering-research-pack/spec.md)                         | Workspace engineering research pack specification                             | Done   | `docs/90.references/research/2026-07-04-wer/` 아래 dated research pack을 만들고 기존 4개 research reference를 재배치하며 Kubernetes, infrastructure, security, automation, pipeline, workflow, QA 주제를 보강하는 계약을 정의한다.                                                | 2026-07-11 |
| [`./0018-workspace-engineering-implementation-audit-pack/spec.md`](./0018-workspace-engineering-implementation-audit-pack/spec.md) | Workspace engineering implementation audit pack specification                 | Done   | `docs/90.references/audits/2026-07-05-wea/` 아래 part-based audit pack을 만들고 기존 root audit 파일을 dated folder 구조로 정리하는 계약을 정의한다.                                                                                                                              | 2026-07-11 |
| [`./0019-template-path-numbering-contract/spec.md`](./0019-template-path-numbering-contract/spec.md)                               | Template path numbering contract specification                                | Done   | `docs/01.requirements/` PRD numeric filename contract와 `docs/03.specs/` numbered feature-folder contract를 template/support/governance/validator surfaces에 맞춰 정규화하는 설계를 정의한다.                                                                                     | 2026-07-11 |
| [`./0020-workspace-contract-governance-normalization/spec.md`](./0020-workspace-contract-governance-normalization/spec.md)         | Workspace contract governance normalization specification                     | Done   | `_workspace` repo-support staging 계약과 repo-wide frontmatter, section, template, governance, CI/CD, QA, validation drift 감사 및 표적 정규화 설계를 정의한다.                                                                                                                   | 2026-07-11 |
| [`./0021-sdlc-lifecycle-contract/spec.md`](./0021-sdlc-lifecycle-contract/spec.md)                                                 | SDLC lifecycle contract specification                                         | Done   | `01.requirements -> 02.architecture -> 03.specs -> 04.execution` 흐름의 상태 전이, 번호, handoff, archive metadata, active-surface 제한, `_workspace` staging 경계를 하나의 검증 가능한 계약으로 정의한다.                                                                        | 2026-07-11 |
| [`./0022-control-cloud-doc-normalization/spec.md`](./0022-control-cloud-doc-normalization/spec.md)                                 | Control surface and cloud example documentation normalization specification   | Done   | control surface와 당시 AWS/Azure example-local route 정규화를 완료한 historical tranche를 기록하며, 현재 cloud 문서 steady state는 Spec 030의 Stage 90 snapshot 통합과 retired-path 금지를 따른다.                                                                           | 2026-07-14 |
| [`./0023-stage03-04-repo-static-gap-closure/spec.md`](./0023-stage03-04-repo-static-gap-closure/spec.md)                           | Stage 03/04 repo-static gap closure specification                             | Done   | Stage 03/04 문서의 repo-static 미구현/증적 gap을 닫고 live/runtime, secret, remote-required 항목은 operator-approved follow-up으로 분리하는 계약을 정의한다.                                                                                                                      | 2026-07-11 |
| [`./0024-observability-and-network-review-agents/spec.md`](./0024-observability-and-network-review-agents/spec.md)                 | Observability and network review agents specification                         | Done   | 두 worker role을 Claude-native, Codex-native, local/Antigravity tracked adapter surface와 harness catalog에 추가한 repo-static 설계를 정의하며 Gemini CLI native 지원은 주장하지 않는다. | 2026-07-14 |
| [`./0025-governance-owner-and-roster-currentness/spec.md`](./0025-governance-owner-and-roster-currentness/spec.md)                 | Governance owner and roster currentness specification                         | Done   | 전체 Spec/Plan 생명주기와 감사 IA를 증거 기반으로 정합화하고, RMD-004의 10-role/30-tracked-role-adapter roster 및 canonical-owner currentness 계약과 검증 경계를 정의한다.                                                                                                                     | 2026-07-14 |
| [`./0026-document-contract-registry/spec.md`](./0026-document-contract-registry/spec.md)                                         | Document contract registry specification                                      | Done   | Registry schema v4와 `DocumentProfileContract.v3`가 62개 문서 profile의 route, metadata, lifecycle, section, README, local/native 예외와 retired cloud-tree 금지를 machine-readable 단일 정본으로 정의한다.                                                                                                    | 2026-07-14 |
| [`./0027-template-contract-consolidation/spec.md`](./0027-template-contract-consolidation/spec.md)                               | Template contract consolidation specification                                 | Done   | Stage 99 support와 form을 registry에 정렬하고 중복 섹션, 작성 지침, Legacy Task form을 통합·삭제한다.                                                                                                                                | 2026-07-12 |
| [`./0028-readme-workspace-profiles/spec.md`](./0028-readme-workspace-profiles/spec.md)                                           | README and workspace profile specification                                    | Done   | 67개 baseline과 5개 cloud handoff를 합친 72개 README를 6개 경로 프로필로 이행하고 `_workspace`의 non-secret repo-support staging 경계를 보존했다.                                                                  | 2026-07-12 |
| [`./0029-semantic-document-validation/spec.md`](./0029-semantic-document-validation/spec.md)                                     | Semantic document validation specification                                    | Done | Frontmatter, Markdown structure, link, index, duplicate owner, template residue와 reciprocal execution lineage를 fixture 기반으로 검증한다.                                                                                          | 2026-07-12 |
| [`./0030-authored-document-migration/spec.md`](./0030-authored-document-migration/spec.md)                                       | Authored document migration specification                                     | Done | reciprocal [Plan](0030-authored-document-migration/plan.md)과 [Task](0030-authored-document-migration/README.md)에 따라 전 문서 모집단을 wave별로 이행하고 AWS/Azure SDLC prose를 Stage 90 provider snapshot으로 통합한다.                    | 2026-07-13 |
| [`./0031-affected-surface-agent-qa/spec.md`](./0031-affected-surface-agent-qa/spec.md)                                           | Affected surface and Agent QA specification                                   | Done | 이 Spec은 affected/staged/all-files/message/manual/CI/remote-live lane, local/Claude/Codex adapter-surface 역할 semantics, handoff evidence의 현재 closure authority를 유지한다. 완료된 Plan/Task 실행 이력의 전체 본문은 Git history에 있고, 필요한 migration/tombstone lookup만 [Stage 98 Index](../98.archive/README.md#document-index)에서 찾는다. | 2026-07-14 |
| [`./0032-protected-surface-supply-chain-hardening/spec.md`](./0032-protected-surface-supply-chain-hardening/spec.md)             | Protected surface and supply-chain hardening specification                    | Done | 이 Spec은 GitHub Actions identity, workflow permissions, GitOps identity-only review, Vault/ESO 및 secret 경계의 repository-static closure authority를 유지한다. 완료된 Plan/Task 실행 이력의 전체 본문은 Git history에 있고, 필요한 migration/tombstone lookup만 [Stage 98 Index](../98.archive/README.md#document-index)에서 찾는다. | 2026-07-14 |
| [`./0033-template-lifecycle-contract-normalization/spec.md`](./0033-template-lifecycle-contract-normalization/spec.md)           | Template lifecycle contract normalization specification                       | Done | Stage 99 form/support/registry 분리, 현재 문서 body contract migration, production cutover와 독립 whole-branch closure review를 완료한 명세다. | 2026-07-15 |
| [`./0034-authority-and-lineage-foundation/spec.md`](./0034-authority-and-lineage-foundation/spec.md) | Authority and lineage foundation specification | Done | Spec 033 follow-up 관계, 새 program lineage, Current audit overlay, Stage 00/99 권위 경계를 정규화하고 repository-static 폐쇄 증거를 기록했다. | 2026-07-15 |
| [`./0035-document-schema-and-lifecycle-contract/spec.md`](./0035-document-schema-and-lifecycle-contract/spec.md) | Document schema and lifecycle contract specification | Done | 유형별 폐쇄형 metadata, 상태 전이, 증거, template/source role, native-surface 계약과 결정적 검증을 완료했다. | 2026-07-17 |
| [`./0036-archive-record-and-workspace-boundary/spec.md`](./0036-archive-record-and-workspace-boundary/spec.md) | Archive record and workspace boundary specification | Done | ARWB-001부터 ARWB-005까지 31개 full-body Archive Record, 202개 historical link, archive 권위, `_workspace` metadata-only 경계를 구현·폐쇄했다. 기존 envelope/payload는 Git object byte 단위로 불변이며, 현재 replacement 진화는 registry-selected current target을 가리키는 archive index만 소유한다. 독립 whole-tranche 검토를 통과한 [completed execution history](../98.archive/README.md#document-index)는 closure commit `855fa78` 및 postflight corrections `cdac53c`, `a12aedf`까지 기록한다. | 2026-07-19 |
| [`./0037-active-corpus-and-execution-retention/spec.md`](./0037-active-corpus-and-execution-retention/spec.md) | Active corpus and execution retention specification | Done | ACER-001~005의 reviewed repository-static 결과와 ACER-006 terminal closure를 기록한다. 현재 Stage 04는 49 Plan/51 Task, 52 lineage의 48/1/3 cardinality, 100 `DEFER`/0 `retain`, accepted ADR 13개와 done Spec 29개 guard, findings 0이다. closure content commit `cfabc506`과 clean-tree postflight PASS를 관측했으며 evidence-update commit 자체는 unidentified·unclaimed이다. | 2026-07-19 |
| [`./0038-reference-information-architecture/spec.md`](./0038-reference-information-architecture/spec.md) | Reference information architecture specification | Done | Reciprocal [Plan](0038-reference-information-architecture/plan.md)과 [Task](0038-reference-information-architecture/README.md)는 RIA-000~006의 reviewed contract/FSM, stage-zero authority, source·generator·duplicate-owner 증거를 기록한다. RIA-007 C1 exact-seven commit `8c0dcea558212e11ac93a0fe626cddb31315859b`은 final `REQUIREMENTS COMPLIANT`/`QUALITY APPROVED`와 activation-to-C1 explicit-ref lifecycle 및 repository-static clean-tree postflight PASS를 관측했다. 현재 C2는 six lifecycle paths, 446-row ledger, contract, exact-value `.secrets.baseline` adjudication의 exact-nine staged proposal일 뿐이며 C2 SHA/postcommit, C3, settlement, terminal explicit-ref, CI-hosted/provider/remote/live 결과를 주장하지 않는다. | 2026-07-26 |
| [`./0039-github-ci-qa-evidence/spec.md`](./0039-github-ci-qa-evidence/spec.md) | GitHub CI and QA evidence specification | Done | GCQE-001~005의 reviewed repository-static 구현과 GCQE-006 closure를 기록한다. Exact eight-path commit `e1d1e910840337327a557ab4b84e86f8fced11d6`, activation `2ddfe4b7697e998b41d3125be94cdc4cee295388`부터의 raw-OID explicit-ref lifecycle, clean-tree repository-static postflight는 PASS였다. Spec 040은 Active다. Hosted run `29982910320`은 과거 exact-SHA FAIL이고 current hosted/provider/live는 `DEFER`이며, 이 evidence-update commit 자체는 주장하지 않는다. | 2026-07-27 |
| [`./0040-contract-cutover-and-program-closure/spec.md`](./0040-contract-cutover-and-program-closure/spec.md) | Contract cutover and program closure specification | Done | 2026-07-28 exact 14-path terminal closure commit `c5adc27b13893d7cbd1266c9225372cfb7df79e9`은 CCPC-000~004 repository-static 완료와 final frontier `0/0·6/3·3`을 기록한다. Lifecycle `668`, staged/strict/residue/aggregate/all-files/formatter/diff gates는 PASS이고 reviewed digest `e146fb13fb3a62db014e6317992a4f519b79ba330253c4c5fe89834dc67e1888`은 terminal requirements/quality/security approval을 받았다. Parent `35d8552ba423e3e2d92294ddeb81674392b8f333`부터 closure까지 explicit-ref와 clean-tree aggregate는 PASS이며 evidence-update commit 자체와 hosted/provider/remote/live는 주장하지 않는다. | 2026-07-28 |
| [`./0041-stage-00-agent-governance-contract/spec.md`](./0041-stage-00-agent-governance-contract/spec.md) | Stage 00 agent governance contract specification | Done | Execution 당시 accepted ADR-0013이 지배한 첫 tranche로 provider-neutral harness machine contract, 당시 current 10/30과 target-only 12/48 분리, 네 memory class 경계, consumer migration, routing, QA/review를 완료했다. Present-tense program decision은 accepted ADR-0019이며 provider/runtime/live 결과는 `DEFER`다. | 2026-08-01 |
| [`./0042-provider-native-runtime-and-model-evidence/spec.md`](./0042-provider-native-runtime-and-model-evidence/spec.md) | Provider native runtime and model evidence specification | Done | 구현 commit `9c4dcc7b7572bfe8f436d81ee87ede872707cc73`에서 exact 10-source cutoff ledger, provider 4개, candidate-only model 8개, MCP 7개, redacted canary 12개와 focused/aggregate 검증을 완료했다. 요구사항은 `COMPLIANT`, 품질·보안은 `APPROVED`이며 provider discovery/authenticated run/model promotion/hosted/remote/live는 관찰된 `DEFER` 또는 `ABSENT` 상태를 유지한다. | 2026-07-29 |
| [`./0043-agent-harness-loop-lifecycle/spec.md`](./0043-agent-harness-loop-lifecycle/spec.md) | Agent harness loop lifecycle specification | Done | bounded retry/recovery와 non-retryable stop, repository-wins checkpoint/resume, 네 memory class의 promotion/refresh/expiry/archive-GC/conflict/compaction/handoff, routing/provider projection을 구현했다. 구현·보강 commits `8a995014`, `95a6ee03`, `f0190643`, `9d8a2a36`과 focused `59/82/39`, lifecycle `668`, aggregate/all-files, 독립 요구사항·품질·보안 승인을 기록하며 provider/runtime/live와 실제 ignored checkpoint 실행은 주장하지 않는다. | 2026-08-01 |
| [`./0044-agent-roster-evaluation-and-admission/spec.md`](./0044-agent-roster-evaluation-and-admission/spec.md) | Agent roster evaluation and admission specification | Done | 구현 `258955b3`, AREA-004 postflight `a15d5e10`, AREA-005 semantic reconciliation `7891368e`로 exact 12-role/4-provider-surface/48-tuple repository-static readiness와 gate enforcement를 닫았다. Mapping은 `PASS` 21 / `DEFER` 27이고 configured incumbent는 유지된다. AREA-003 evaluation readiness는 완료됐지만 observed evaluation/final admission/model fitness/threshold/promotion/canary/runtime/provider auth/hosted CI/remote/live는 해당 범위에서 계속 `DEFER`다. 다음 handoff는 Spec 045다. | 2026-07-30 |
| [`./0045-agent-governance-ci-qa-cutover/spec.md`](./0045-agent-governance-ci-qa-cutover/spec.md) | Agent governance CI and QA cutover specification | Done | AGQC-000~006 repository-static CI/QA cutover를 terminal HEAD `ed892285`까지 완료했다. Baseline `a886e061`에서 Python `741`, aggregate, all-files, formatter review 및 diff가 PASS했고 test-only delta는 관련 `49`, nested-subreaper probe, file pre-commit 및 세 독립 검토를 통과했다(모두 `0/0/0`). 고정 cutoff는 `2026-07-10T10:00:00+09:00`이며 hosted CI, branch protection, provider runtime/auth/model discovery, actual eval/admission/promotion, remote/live 및 provider resume/handoff canary는 Spec 046 범위로 `DEFER`한다. | 2026-08-01 |
| [`./0046-agent-governance-program-closure/spec.md`](./0046-agent-governance-program-closure/spec.md) | Agent governance program closure specification | Done | Execution 당시 active REQ-0003/AD-0006 및 accepted ADR-0019 lineage를 closure contract `1.2.0`으로 통합한 historical tranche다. ADR-0019의 provider/cardinality 방향은 현재 ADR-0030에 superseded되었고, provider/hosted/actual/remote/live `DEFER`/`ABSENT` 증거만 역사적 의미로 유지한다. | 2026-08-01 |
| [`./0047-current-surface-and-stash-reconciliation/spec.md`](./0047-current-surface-and-stash-reconciliation/spec.md) | Current target inventory, canonical ownership, audit delta, protected boundary, and stash semantic reconciliation specification | Draft | PRD-0007 program의 첫 tranche로서 전수 disposition과 stash hunk 분류를 소유하며 GitHub, platform, IaC 구현은 후속 Specs 048–050에 인계한다. 2026-08-07부터 PRD-0008 document taxonomy consolidation 기간 동안 suspend되어 draft로 되돌아갔고, Spec 052가 `done`에 도달하면 통합된 구조에서 재개한다. | 2026-08-07 |
| [`./0048-github-routing-and-ci-evidence/spec.md`](./0048-github-routing-and-ci-evidence/spec.md) | GitHub surface routing, label/CODEOWNERS parity, CI lane ownership, and read-only remote evidence specification | Draft | validation-surface ID를 참조하는 단일 projection contract와 native GitHub 정합성을 소유하며 branch protection 및 hosted rerun은 별도 권한으로 남긴다. | 2026-08-02 |
| [`./0049-platform-validation-and-security-evidence/spec.md`](./0049-platform-validation-and-security-evidence/spec.md) | Layered Kubernetes/GitOps render, schema, policy, Traefik semantics, secret, and security evidence specification | Draft | 13개 Kustomize root와 명시적 evidence depth를 소유하며 live cluster/Vault/ESO/TLS 및 remote Helm 결과는 분리된 DEFER로 유지한다. | 2026-08-02 |
| [`./0050-example-iac-and-validator-qa/spec.md`](./0050-example-iac-and-validator-qa/spec.md) | AWS Terraform, Azure Bicep, example routing, and validator regression QA specification | Draft | Provider-native non-deploy validation과 exact tool/fallback evidence를 소유하며 cloud login, plan/apply, deploy, what-if 및 live readiness는 범위 밖이다. | 2026-08-02 |
| [`./0051-repository-assurance-integration-and-closure/spec.md`](./0051-repository-assurance-integration-and-closure/spec.md) | Cross-tranche integration, lifecycle closure, local main merge, stash retirement, and cleanup specification | Draft | 두 machine contract와 최종 target matrix를 통합하고 전체 QA/review 후 local-only fast-forward 및 cleanup을 수행하며 hosted/provider/remote/live 증거는 분리한다. | 2026-08-02 |
| [`./0052-document-taxonomy-consolidation/spec.md`](./0052-document-taxonomy-consolidation/spec.md) | Stage 03 work-unit migration, governance authority, agent controls, disposition, and validator reconciliation specification | Active | 2026-08-09 승인 설계에 따라 Stage 03에 Spec/Plan/Task를 통합하고 Stage 04 execution을 폐지하되 Stage 05를 유지한다. Release 제외, stable filename/date 예외, fail-closed transition, Archive/observation 무결성, harness-contract 확장, script/validator 의미 보존 및 기준선 실패 해결을 소유한다. | 2026-08-09 |
| [`./0053-workspace-engineering-research-pack-consolidation/spec.md`](./0053-workspace-engineering-research-pack-consolidation/spec.md) | Workspace engineering research pack consolidation and replacement specification | Done | 2026-08-08 승인에 따라 신규 13-file `2026-08-08-wer` 통합 팩, 25개 predecessor disposition, mutable consumer 전환, 세 predecessor 팩 삭제, whole-branch 검토와 repository-static 게이트를 완료했다. Stage 98은 불변이고 provider/runtime/hosted/remote/live 증거는 주장하지 않는다. | 2026-08-09 |
| [`./0054-sdlc-document-and-agent-governance-consolidation/spec.md`](./0054-sdlc-document-and-agent-governance-consolidation/spec.md) | SDLC document and AI-agent governance consolidation specification | Active | 승인된 B 범위(Stage 90 포함)에 따라 4자리 문서 identity, co-located Spec/Plan/Task, 통합 agent governance, Stage 05/90/98 disposition, template/validator/script convergence를 실행한다. | 2026-08-13 |
| [`./0055-workspace-governance-audit-and-remediation/spec.md`](./0055-workspace-governance-audit-and-remediation/spec.md)                           | Workspace governance audit, canonical-owner remediation, current-pointer cutover, and evidence-gated cleanup specification                    | Done   | 승인된 30개 요청 범위를 신규 10-file Current 감사 팩으로 조사하고 canonical owner 보정, sole-Current 전환, 증거 기반 no-deletion 결과, terminal QA와 review를 완료했다. 기존 감사 팩은 source-commit 고정 역사 증거로 보존하며 hosted/provider/remote/live 결과는 `DEFER`한다.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | 2026-08-09 |
| [`./0056-workspace-engineering-gap-only-refresh/spec.md`](./0056-workspace-engineering-gap-only-refresh/spec.md)                                   | Existing 2026-08-08 WER gap-only external-source refresh specification                                                                        | Done   | 기존 팩에서 조사되지 않았거나 외부 근거가 불충분한 `Partial` 질문만 2026-08-10 공식 1차 출처와 현재 workspace evidence로 보강했다. 새 팩·중복 보고서·provider/runtime/hosted/remote/live 증거는 범위 밖이다.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | 2026-08-10 |
| [`./0057-workspace-engineering-partial-defer-incremental-refresh/spec.md`](./0057-workspace-engineering-partial-defer-incremental-refresh/spec.md) | Existing WER pack Partial/DEFER closed-ledger incremental refresh design                                                                      | Done   | 2026-08-12 직접 승인된 standalone execution은 12개 base `Partial` 행과 조건부 qualified `DEFER` 증거만 폐쇄형 원장으로 재검토한다. 공식 공개 1차 출처, 현재 repository-static 증거, 허용된 GitHub Actions/설정 읽기 전용 메타데이터만 사용하며 새 연구 팩·중복 보고서·원격 변경·secret value·provider/runtime/cluster/live 증거는 금지한다.                                                                                                                                                                                                                                                                                                                                                                                                                                               | 2026-08-12 |
| [`./0058-workspace-research-consistency-and-partial-refresh/spec.md`](./0058-workspace-research-consistency-and-partial-refresh/spec.md)           | Combined constraint-consistency and Partial re-observation cycle over the existing WER pack                                                   | Done   | 2026-08-14 직접 요청된 23개 주제를 기존 `REQ-WERPC` 오너 36개 행으로 폐쇄 매핑하고, 승인된 2건의 일회성 산출물 정리, 12개 `Partial` 행의 workspace 재관측과 외부 출처 재확인, 10개 scope 재투영, 최종 cross-link 정합화를 하나의 사이클로 수행한다. 새 연구 팩·중복 보고서·요구사항 ID 신설은 금지하며 cluster/hosted/provider-runtime 증거는 `DEFER`로 유지한다.                                                                                                                                                                                                                                                                                                                                                                                                                         | 2026-08-14 |
| [`./0059-workspace-research-full-corpus-refresh/spec.md`](./0059-workspace-research-full-corpus-refresh/spec.md)                                   | Full-corpus external and workspace re-observation with terminal blocking-class closure over the existing WER pack                             | Done   | 2026-08-17 직접 승인된 다섯 번째 리프레시 사이클로, 12행 `Partial` 표본을 반복하는 대신 36개 owner row 전수를 외부·워크스페이스 두 증거 클래스로 재관측하고, 잔존 `Partial`/`DEFER` 행마다 차단 evidence class를 확정해 정적 재검증 루프를 종료시킨다. 새 연구 팩·중복 보고서·요구사항 ID 신설은 금지한다.                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | 2026-08-17 |
| [`./0060-platform-currency-defect-closure/spec.md`](./0060-platform-currency-defect-closure/spec.md)                                               | Bounded closure of live platform version-currency defects plus the source-integrity non-adoption decision                                     | Done | 2026-08-18 직접 승인된 제한 범위 보정 사이클로, 발화된 refresh trigger 평가에서 드러난 두 개의 현재 결함(kube-state-metrics 기본 수집기 RBAC 결손, bootstrap 단계 Helm chart 핀 부재)을 닫고 Argo CD source-integrity 미채택을 ADR 0023으로 확정한다. 네 건의 버전 업그레이드는 target·전제조건·차단 클래스와 함께 다음 사이클로 이연한다.                                                                                                                                                                                                                                                                                                                                                                                                                                       | 2026-08-18 |
| [`./0061-workload-security-context-baseline/spec.md`](./0061-workload-security-context-baseline/spec.md) | Bounded closure of the workload security context asymmetry and of the sample template that propagates it | Done | 2026-08-18 직접 승인된 제한 범위 사이클로, house 하드닝 패턴에서 유일하게 빠져 있던 `adminer` Rollout에 이미지 UID·파일시스템과 무관하게 성립하는 컨트롤만 적용하고, 신규 워크로드가 복사해 가는 `examples/sample-app` 템플릿에는 완전한 기준선을 심는다. `runAsNonRoot`/`runAsUser` 커플링과 `readOnlyRootFilesystem`은 전제조건과 함께 이연한다. | 2026-08-18 |
| [`./0062-workspace-research-full-corpus-reverification/spec.md`](./0062-workspace-research-full-corpus-reverification/spec.md) | Full-corpus external-source and workspace reverification design over the existing WER research pack | Active | 2026-08-20 직접 승인된 standalone 실행 관계로, 기존 36개 `REQ-WERPC` owner를 외부·workspace 증거로 전수 재검증하고 결과를 기존 14-file 연구 팩에 증분 통합한다. | 2026-08-20 |
| [`./0063-governance-invariant-consolidation/spec.md`](./0063-governance-invariant-consolidation/spec.md) | Retirement of completed-migration validation machinery and unification of the declared contract with the executed gate | Done | 2026-08-29 직접 승인된 standalone 실행 관계로, 완료된 이관에 묶인 검증기와 핀을 은퇴시키고 ADR-0030의 Stage 98 경계를 집행하며 계약을 실행 목록의 단일 소유자로 만든다. | 2026-08-30 |
| [`./0064-agent-governance-surface-consolidation/spec.md`](./0064-agent-governance-surface-consolidation/spec.md) | Correction of the agent-governance surfaces so each states only what is currently true, with one owner per fact | Active | 2026-08-30 직접 승인된 standalone 실행 관계로, `docs/00.agent-governance/`·`.agents/`·`.claude/`·`.codex/` 98개 파일을 6개 축으로 감사해 자기모순 상태의 progress 원장을 Stage 98 최소 Tombstone으로 은퇴시키고, 소유되지 않은 경로를 지시하는 skill과 참조 없는 스캐폴드를 제거한다. 기각된 후보 8건도 근거와 함께 기록한다. | 2026-08-30 |

### Helper Templates

아래 템플릿은 `docs/03.specs/<###-Numbering>-<feature-id>/` 아래에서 `spec.md`를 보조하는 계약 문서에만 사용한다.

- `../99.templates/templates/sdlc/specs/spec.template.md`
- `../99.templates/templates/sdlc/specs/interface.template.md`
- `../99.templates/templates/sdlc/specs/agent-design.template.md`
- `../99.templates/templates/sdlc/specs/data-model.template.md`
- `../99.templates/templates/sdlc/specs/tests.template.md`
- `../99.templates/templates/sdlc/specs/openapi.template.yaml`
- `../99.templates/templates/sdlc/specs/service.template.proto`
- `../99.templates/templates/sdlc/specs/schema.template.graphql`

## Related Documents

- [Docs README](../README.md)
- [01.requirements](../01.requirements/README.md)
- [02.architecture/descriptions](../02.architecture/descriptions/README.md)
- [02.architecture/decisions](../02.architecture/decisions/README.md)
- [05.operations/runbooks](../05.operations/runbooks/README.md)
- [Archive Index](../98.archive/README.md)
