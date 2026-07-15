# 03.specs

> PRD/ARD/ADR을 구현 가능한 기술 계약과 검증 기준으로 구체화하는 Spec stage다.

> [!NOTE]
> All AI agent interactions with this stage must comply with the [Agent Governance Hub](../00.agent-governance/README.md).

## Overview

이 경로는 PRD, ARD, ADR을 구현 가능한 기술 계약으로 구체화하는 Spec stage다.
서비스, API, 데이터 모델, Agent 설계, 검증 기준은 이곳에서 하위 구현과 추적 가능해야 한다.

Spec은 실행 기준을 소유하는 문서다.
활성 Spec은 현재 repo-backed 구현과 일치해야 하며, 구현과 상충하는 old Spec은 중앙 archive Tombstone으로 이동한다.

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
- PRD/ARD/ADR과 Plan/Task/Runbook을 잇는 traceability

### Out of Scope

- 제품 우선순위와 사용자 가치 중심 설명
- 전사 운영 정책
- 실시간 장애 대응 절차
- 실행 추적의 정본 작업 목록

위 내용은 각각 `01.requirements/`, `05.operations/policies/`, `05.operations/runbooks/`, `04.execution/tasks/`로 분리한다.

## Document Index

```text
03.specs/
├── 004-argo-rollouts-progressive-delivery/
│   └── spec.md
├── 005-argo-notifications-slack/
│   └── spec.md
├── 006-workspace-harness-gap-analysis/
│   └── spec.md
├── 008-current-local-gitops-platform/
│   └── spec.md
├── 009-workspace-harness-research-pack/
│   └── spec.md
├── 010-workspace-harness-implementation-audit-pack/
│   └── spec.md
├── 011-template-contract-governance-migration/
│   └── spec.md
├── 012-template-governance-audit-enhancement/
│   └── spec.md
├── 013-workspace-document-governance-hardening/
│   └── spec.md
├── 014-workspace-document-contract-normalization/
│   └── spec.md
├── 015-agent-governance-contract-normalization/
│   └── spec.md
├── 016-active-control-surface-governance-hardening/
│   └── spec.md
├── 017-workspace-engineering-research-pack/
│   └── spec.md
├── 018-workspace-engineering-implementation-audit-pack/
│   └── spec.md
├── 019-template-path-numbering-contract/
│   └── spec.md
├── 020-workspace-contract-governance-normalization/
│   └── spec.md
├── 021-sdlc-lifecycle-contract/
│   └── spec.md
├── 022-control-cloud-doc-normalization/
│   └── spec.md
├── 023-stage03-04-repo-static-gap-closure/
│   └── spec.md
├── 024-observability-and-network-review-agents/
│   ├── spec.md
│   └── agent-design.md
├── 025-governance-owner-and-roster-currentness/
│   └── spec.md
├── 026-document-contract-registry/
│   └── spec.md
├── 027-template-contract-consolidation/
│   └── spec.md
├── 028-readme-workspace-profiles/
│   └── spec.md
├── 029-semantic-document-validation/
│   └── spec.md
├── 030-authored-document-migration/
│   └── spec.md
├── 031-affected-surface-agent-qa/
│   └── spec.md
├── 032-protected-surface-supply-chain-hardening/
│   └── spec.md
├── 033-template-lifecycle-contract-normalization/
│   └── spec.md
├── 034-authority-and-lineage-foundation/
│   └── spec.md
├── 035-document-schema-and-lifecycle-contract/
│   └── spec.md
├── 036-archive-record-and-workspace-boundary/
│   └── spec.md
├── 037-active-corpus-and-execution-retention/
│   └── spec.md
├── 038-reference-information-architecture/
│   └── spec.md
├── 039-github-ci-qa-evidence/
│   └── spec.md
├── 040-contract-cutover-and-program-closure/
│   └── spec.md
└── README.md
```

## Authoring Workflow

1. 관련 PRD, ARD, ADR 링크를 확인하고 Spec의 입력으로 고정한다.
2. 새 Spec은 `../99.templates/templates/sdlc/specs/spec.template.md`에서 시작하고, canonical target pattern은 `docs/03.specs/<###-Numbering>-<feature-id>/spec.md`다.
3. API/데이터/Agent/Test 보조 문서는 같은 feature 하위 폴더에 두고 상위 `spec.md`와 연결한다.
4. 구현 및 검증 추적은 `04.execution/tasks/`로 연결한다.
5. 현재 구현과 상충하는 historical/superseded 값은 활성 Spec에 보존하지 않고 `../98.archive/README.md`의 Tombstone 인덱스로 분리한다.

### Relative Link Rules

이 README의 링크 기준 위치는 `docs/03.specs/`다.

- 상위 문서는 `../`로 시작하는 상대 경로를 사용한다.
- 같은 stage의 spec은 `./<###-Numbering>-<feature-id>/spec.md`로 연결한다.
- 실행 문서는 `../04.execution/`, 운영 문서는 `../05.operations/`로 연결한다.
- feature-local helper 문서 링크는 `docs/03.specs/<###-Numbering>-<feature-id>/` 안의 최종 파일 위치 기준으로 다시 계산한다.

### Spec Authoring Rules

1. 모든 활성 Spec은 관련 PRD와 ARD를 링크하거나 부재를 명시한다.
2. Verification은 필수다.
3. Acceptance Criteria와 테스트는 PRD에서 이어지고, 구현 검증은 Task와 연결된다.
4. API가 있다면 API Spec 또는 계약 파일을 함께 둔다.
5. Agent 설계가 있다면 Role, Tool, Policy, Memory, Guardrail, Evaluation, Fallback을 명시한다.
6. feature-local `tasks.md` 또는 `tests.md`는 설계 보조 문서이며, 실행 추적 정본은 `../04.execution/tasks/`다.
7. `Related Inputs`는 upstream 요약이고, `Related Documents`는 PRD/ARD/ADR와 Plan/Task/Operations 링크를 함께 담는다.

### Current Spec Index

| 문서                                                                                                                             | 설명                                                                          | 상태   | 현재성                                                                                                                                                                                                                                                                            | 최종 수정  |
| -------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | ------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| [`./004-argo-rollouts-progressive-delivery/spec.md`](./004-argo-rollouts-progressive-delivery/spec.md)                           | Argo Rollouts 점진적 배포 current-contract backfill 명세                      | Active | `platform-rollouts` Application, dashboard, metrics, AppProject 권한, 앱 canary AnalysisTemplate 경계를 현재 계약으로 정리한다. 구현 evidence는 Spec의 Implementation Status를 따른다.                                                                                            | 2026-06-04 |
| [`./005-argo-notifications-slack/spec.md`](./005-argo-notifications-slack/spec.md)                                               | ArgoCD Notifications Slack current-contract backfill 명세                     | Active | ArgoCD Notifications, Vault/ESO credential boundary, template/trigger 계약을 현재 기준으로 정리한다. 구현 evidence는 Spec의 Implementation Status를 따른다.                                                                                                                       | 2026-05-22 |
| [`./006-workspace-harness-gap-analysis/spec.md`](./006-workspace-harness-gap-analysis/spec.md)                                   | Workspace harness Gap analysis와 제한 구현 계약                               | Active | WSL2, WSL Linux native Docker, k3d, ArgoCD GitOps, SDD lifecycle, QA, CI/CD, Agent governance의 repo-static 개선 범위를 정의한다. P3 repo desired-state 보완은 별도 실행 증적에 반영됐고, live runtime 검증·secret value 확인·CI ruleset/pinning 정책은 deferred item으로 남긴다. | 2026-07-11 |
| [`./008-current-local-gitops-platform/spec.md`](./008-current-local-gitops-platform/spec.md)                                     | 현재 local GitOps platform baseline Spec                                      | Active | Headlamp, ingress-nginx, ArgoCD App-of-Apps, ESO/Vault, external services, Kiali/Istio, Rollouts, Notifications, monitoring, adminer 구현 증적을 소유한다.                                                                                                                        | 2026-06-02 |
| [`./009-workspace-harness-research-pack/spec.md`](./009-workspace-harness-research-pack/spec.md)                                 | Workspace harness/loop engineering research pack 명세                         | Done   | `docs/90.references/research/` 아래 통합 연구 팩의 구조, 공식 외부 소스 우선순위, market scan 경계, implementation checklist 포함 방식, 검증 기준을 정의한다.                                                                                                                     | 2026-07-11 |
| [`./010-workspace-harness-implementation-audit-pack/spec.md`](./010-workspace-harness-implementation-audit-pack/spec.md)         | Workspace harness/loop implementation audit pack 명세                         | Done   | `docs/90.references/research/` 기준 모델과 repo-backed evidence를 대조해 `docs/90.references/audits/` 아래 4개 구현 현황 감사 보고서와 README를 작성하는 계약을 정의한다.                                                                                                         | 2026-07-11 |
| [`./011-template-contract-governance-migration/spec.md`](./011-template-contract-governance-migration/spec.md)                   | Template contract와 governance migration 명세                                 | Done   | `docs/99.templates/`를 template forms와 support contracts로 분리하고, frontmatter schema, validator, hook, governance, authored docs 적용을 4단계 migration으로 정의한다.                                                                                                         | 2026-07-11 |
| [`./012-template-governance-audit-enhancement/spec.md`](./012-template-governance-audit-enhancement/spec.md)                     | Template governance follow-up audit와 선택 보강 명세                          | Done   | 이미 완료된 template contract migration 위에서 `docs/99.templates/**`, support contracts, Stage 00 routing, validator, authored docs 사용 상태를 audit-first로 검증하고 안정적인 보강 범위를 정의한다.                                                                            | 2026-07-11 |
| [`./013-workspace-document-governance-hardening/spec.md`](./013-workspace-document-governance-hardening/spec.md)                 | Workspace document type, provider entrypoint, CI/QA governance hardening 명세 | Done   | template/frontmatter contracts, provider shims, README scope, workspace-wide authored docs, and repo-static validation을 staged governance hardening 흐름으로 정렬한다.                                                                                                           | 2026-07-11 |
| [`./014-workspace-document-contract-normalization/spec.md`](./014-workspace-document-contract-normalization/spec.md)             | Workspace document contract normalization 명세                                | Done   | active 문서와 historical evidence까지 frontmatter, section, template 계약에 맞게 전면 정규화하고, 과거 증거는 current contract와 분리된 섹션으로 보존하는 후속 패스를 정의한다.                                                                                                   | 2026-07-11 |
| [`./015-agent-governance-contract-normalization/spec.md`](./015-agent-governance-contract-normalization/spec.md)                 | Agent governance contract normalization 명세                                  | Done   | Stage 00, Claude/Codex native role files, repository-local baselines, local/Antigravity `.agents/**`, exact wiring surfaces, absent/`DEFER` Gemini CLI native boundary, QA/CI 정규화 범위를 정의한다. | 2026-07-14 |
| [`./016-active-control-surface-governance-hardening/spec.md`](./016-active-control-surface-governance-hardening/spec.md)         | Active control surface governance hardening 명세                              | Done   | `.github`, `scripts`, `gitops`, `infrastructure`, `policy`, `tests`, `traefik`, `examples/sample-app`의 active 운영 표면을 보강하고 AWS/Azure cloud examples는 dated snapshot으로 유지하는 계약을 정의한다.                                                                       | 2026-07-11 |
| [`./017-workspace-engineering-research-pack/spec.md`](./017-workspace-engineering-research-pack/spec.md)                         | Workspace engineering research pack specification                             | Done   | `docs/90.references/research/2026-07-04-wer/` 아래 dated research pack을 만들고 기존 4개 research reference를 재배치하며 Kubernetes, infrastructure, security, automation, pipeline, workflow, QA 주제를 보강하는 계약을 정의한다.                                                | 2026-07-11 |
| [`./018-workspace-engineering-implementation-audit-pack/spec.md`](./018-workspace-engineering-implementation-audit-pack/spec.md) | Workspace engineering implementation audit pack specification                 | Done   | `docs/90.references/audits/2026-07-05-wea/` 아래 part-based audit pack을 만들고 기존 root audit 파일을 dated folder 구조로 정리하는 계약을 정의한다.                                                                                                                              | 2026-07-11 |
| [`./019-template-path-numbering-contract/spec.md`](./019-template-path-numbering-contract/spec.md)                               | Template path numbering contract specification                                | Done   | `docs/01.requirements/` PRD numeric filename contract와 `docs/03.specs/` numbered feature-folder contract를 template/support/governance/validator surfaces에 맞춰 정규화하는 설계를 정의한다.                                                                                     | 2026-07-11 |
| [`./020-workspace-contract-governance-normalization/spec.md`](./020-workspace-contract-governance-normalization/spec.md)         | Workspace contract governance normalization specification                     | Done   | `_workspace` repo-support staging 계약과 repo-wide frontmatter, section, template, governance, CI/CD, QA, validation drift 감사 및 표적 정규화 설계를 정의한다.                                                                                                                   | 2026-07-11 |
| [`./021-sdlc-lifecycle-contract/spec.md`](./021-sdlc-lifecycle-contract/spec.md)                                                 | SDLC lifecycle contract specification                                         | Done   | `01.requirements -> 02.architecture -> 03.specs -> 04.execution` 흐름의 상태 전이, 번호, handoff, archive metadata, active-surface 제한, `_workspace` staging 경계를 하나의 검증 가능한 계약으로 정의한다.                                                                        | 2026-07-11 |
| [`./022-control-cloud-doc-normalization/spec.md`](./022-control-cloud-doc-normalization/spec.md)                                 | Control surface and cloud example documentation normalization specification   | Done   | control surface와 당시 AWS/Azure example-local route 정규화를 완료한 historical tranche를 기록하며, 현재 cloud 문서 steady state는 Spec 030의 Stage 90 snapshot 통합과 retired-path 금지를 따른다.                                                                           | 2026-07-14 |
| [`./023-stage03-04-repo-static-gap-closure/spec.md`](./023-stage03-04-repo-static-gap-closure/spec.md)                           | Stage 03/04 repo-static gap closure specification                             | Done   | Stage 03/04 문서의 repo-static 미구현/증적 gap을 닫고 live/runtime, secret, remote-required 항목은 operator-approved follow-up으로 분리하는 계약을 정의한다.                                                                                                                      | 2026-07-11 |
| [`./024-observability-and-network-review-agents/spec.md`](./024-observability-and-network-review-agents/spec.md)                 | Observability and network review agents specification                         | Done   | 두 worker role을 Claude-native, Codex-native, local/Antigravity tracked adapter surface와 harness catalog에 추가한 repo-static 설계를 정의하며 Gemini CLI native 지원은 주장하지 않는다. | 2026-07-14 |
| [`./025-governance-owner-and-roster-currentness/spec.md`](./025-governance-owner-and-roster-currentness/spec.md)                 | Governance owner and roster currentness specification                         | Done   | 전체 Spec/Plan 생명주기와 감사 IA를 증거 기반으로 정합화하고, RMD-004의 10-role/30-tracked-role-adapter roster 및 canonical-owner currentness 계약과 검증 경계를 정의한다.                                                                                                                     | 2026-07-14 |
| [`./026-document-contract-registry/spec.md`](./026-document-contract-registry/spec.md)                                         | Document contract registry specification                                      | Done   | Registry schema v4와 `DocumentProfileContract.v3`가 62개 문서 profile의 route, metadata, lifecycle, section, README, local/native 예외와 retired cloud-tree 금지를 machine-readable 단일 정본으로 정의한다.                                                                                                    | 2026-07-14 |
| [`./027-template-contract-consolidation/spec.md`](./027-template-contract-consolidation/spec.md)                               | Template contract consolidation specification                                 | Done   | Stage 99 support와 form을 registry에 정렬하고 중복 섹션, 작성 지침, Legacy Task form을 통합·삭제한다.                                                                                                                                | 2026-07-12 |
| [`./028-readme-workspace-profiles/spec.md`](./028-readme-workspace-profiles/spec.md)                                           | README and workspace profile specification                                    | Done   | 67개 baseline과 5개 cloud handoff를 합친 72개 README를 6개 경로 프로필로 이행하고 `_workspace`의 non-secret repo-support staging 경계를 보존했다.                                                                  | 2026-07-12 |
| [`./029-semantic-document-validation/spec.md`](./029-semantic-document-validation/spec.md)                                     | Semantic document validation specification                                    | Done | Frontmatter, Markdown structure, link, index, duplicate owner, template residue와 reciprocal execution lineage를 fixture 기반으로 검증한다.                                                                                          | 2026-07-12 |
| [`./030-authored-document-migration/spec.md`](./030-authored-document-migration/spec.md)                                       | Authored document migration specification                                     | Done | reciprocal [Plan](../04.execution/plans/2026-07-12-authored-document-migration.md)과 [Task](../04.execution/tasks/2026-07-12-authored-document-migration.md)에 따라 전 문서 모집단을 wave별로 이행하고 AWS/Azure SDLC prose를 Stage 90 provider snapshot으로 통합한다.                    | 2026-07-13 |
| [`./031-affected-surface-agent-qa/spec.md`](./031-affected-surface-agent-qa/spec.md)                                           | Affected surface and Agent QA specification                                   | Done | reciprocal [Plan](../04.execution/plans/2026-07-12-affected-surface-agent-qa.md)과 [Task](../04.execution/tasks/2026-07-12-affected-surface-agent-qa.md)에 따라 affected/staged/all-files/message/manual/CI/remote-live lane, local/Claude/Codex adapter-surface 역할 semantics, handoff evidence를 정렬하고 ASQA-001부터 ASQA-006까지 완료했다. | 2026-07-14 |
| [`./032-protected-surface-supply-chain-hardening/spec.md`](./032-protected-surface-supply-chain-hardening/spec.md)             | Protected surface and supply-chain hardening specification                    | Done | reciprocal [Plan](../04.execution/plans/2026-07-12-protected-surface-supply-chain-hardening.md)과 [Task](../04.execution/tasks/2026-07-12-protected-surface-supply-chain-hardening.md)에 따라 PSH-001부터 PSH-006까지 완료하고, GitHub Actions identity, workflow permissions, GitOps identity-only review, Vault/ESO 및 secret 경계의 repository-static 증거와 remote/live `DEFER`를 분리했다. | 2026-07-14 |
| [`./033-template-lifecycle-contract-normalization/spec.md`](./033-template-lifecycle-contract-normalization/spec.md)           | Template lifecycle contract normalization specification                       | Done | Stage 99 form/support/registry 분리, 현재 문서 body contract migration, production cutover와 독립 whole-branch closure review를 완료한 명세다. | 2026-07-15 |
| [`./034-authority-and-lineage-foundation/spec.md`](./034-authority-and-lineage-foundation/spec.md) | Authority and lineage foundation specification | Active | Spec 033 follow-up 관계, 새 program lineage, Current audit overlay, Stage 00/99 권위 경계를 정규화한다. | 2026-07-15 |
| [`./035-document-schema-and-lifecycle-contract/spec.md`](./035-document-schema-and-lifecycle-contract/spec.md) | Document schema and lifecycle contract specification | Active | 유형별 폐쇄형 metadata, 상태 전이, 증거, template parity 계약을 정의한다. | 2026-07-15 |
| [`./036-archive-record-and-workspace-boundary/spec.md`](./036-archive-record-and-workspace-boundary/spec.md) | Archive record and workspace boundary specification | Active | 31개 Tombstone을 full-body archive로 복원하고 _workspace 경계를 검증한다. | 2026-07-15 |
| [`./037-active-corpus-and-execution-retention/spec.md`](./037-active-corpus-and-execution-retention/spec.md) | Active corpus and execution retention specification | Active | 종료 lineage의 eligible Plan/Task를 archive하고 active-stage 누적을 제한한다. | 2026-07-15 |
| [`./038-reference-information-architecture/spec.md`](./038-reference-information-architecture/spec.md) | Reference information architecture specification | Active | Stage 90 Current/Historical/generated/source freshness와 중복 소유권을 정리한다. | 2026-07-15 |
| [`./039-github-ci-qa-evidence/spec.md`](./039-github-ci-qa-evidence/spec.md) | GitHub CI and QA evidence specification | Active | affected/all-files QA, aggregate verdict, artifact retention, FIFO portability 경계를 정리한다. | 2026-07-15 |
| [`./040-contract-cutover-and-program-closure/spec.md`](./040-contract-cutover-and-program-closure/spec.md) | Contract cutover and program closure specification | Active | compatibility 제거, strict corpus cutover, 전체 검증과 독립 closure review를 소유한다. | 2026-07-15 |

### Helper Templates

아래 템플릿은 `docs/03.specs/<###-Numbering>-<feature-id>/` 아래에서 `spec.md`를 보조하는 계약 문서에만 사용한다.

- `../99.templates/templates/sdlc/specs/spec.template.md`
- `../99.templates/templates/sdlc/specs/api-spec.template.md`
- `../99.templates/templates/sdlc/specs/agent-design.template.md`
- `../99.templates/templates/sdlc/specs/data-model.template.md`
- `../99.templates/templates/sdlc/specs/tests.template.md`
- `../99.templates/templates/sdlc/specs/openapi.template.yaml`
- `../99.templates/templates/sdlc/specs/service.template.proto`
- `../99.templates/templates/sdlc/specs/schema.template.graphql`

## Related Documents

- [Docs README](../README.md)
- [01.requirements](../01.requirements/README.md)
- [02.architecture/requirements](../02.architecture/requirements/README.md)
- [02.architecture/decisions](../02.architecture/decisions/README.md)
- [04.execution/plans](../04.execution/plans/README.md)
- [04.execution/tasks](../04.execution/tasks/README.md)
- [05.operations/runbooks](../05.operations/runbooks/README.md)
- [Archive Index](../98.archive/README.md)
