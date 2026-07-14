# 04.execution/plans

> 실행 순서, 리스크, 롤아웃, 검증 게이트를 정의하는 Plan stage다.

> [!NOTE]
> All AI agent interactions with this stage must comply with the [Agent Governance Hub](../../00.agent-governance/README.md).

## Overview

이 경로는 승인된 요구와 기술 계약을 실행 순서, 위험 관리, 검증 게이트로 전환하는 Plan stage다.
Plan은 구현을 시작하기 전 작업 흐름, 롤아웃/롤백, 완료 기준을 합의하는 문서다.
Task evidence는 `../tasks/`가 소유하고, Plan은 그 evidence가 어떤 순서와 기준으로 만들어져야 하는지 정의한다.
완료된 Plan에 남아 있는 미체크 박스는 승인된 과거 실행 지침을 보존하며 현재 작업 큐가 아니다.
연결된 `status: done` Task가 완료 상태와 evidence의 정본이다.

### Collection Readers

이 README의 주요 독자:

- Platform Engineers
- Operators
- Project Maintainers
- AI Agents

## Scope

### In Scope

- 목표, 범위, 단계, 마일스톤
- 위험과 완화 전략
- 검증 게이트, 완료 기준, 롤아웃/롤백 전략
- 하위 Task로 이어지는 실행 단위 참조
- Agent 작업의 offline eval, sandbox/canary, human approval, rollback, prompt/model promotion gate

### Out of Scope

- 요구사항 정본
- 상세 기술 설계 정본
- 실제 작업 증거와 상태 추적의 정본
- 반복 운영 절차와 장애 대응 runbook

이 내용은 각각 `../../01.requirements/`, `../../03.specs/`, `../tasks/`, `../../05.operations/`로 분리한다.

## Item Index

```text
04.execution/plans/
├── 2026-05-09-github-qa-ci-remediation.md
├── 2026-05-09-scripts-inventory-remediation.md
├── 2026-05-10-agent-first-harness-llm-wiki-hooks.md
├── 2026-05-17-template-crosslink-fix.md
├── 2026-05-18-argo-rollouts-progressive-delivery.md
├── 2026-05-18-argo-notifications-slack.md
├── 2026-05-22-docs-governance-full-ab-hardening.md
├── 2026-05-22-workspace-purpose-alignment.md
├── 2026-05-24-p3-gitops-secret-runtime-remediation.md
├── 2026-05-28-workspace-skill-expansion.md
├── 2026-05-30-antigravity-governance.md
├── 2026-05-31-codex-governance-harness-alignment.md
├── 2026-06-01-claude-agent-surface-restoration.md
├── 2026-06-01-stage-00-canonical-adapter-redesign.md
├── 2026-06-02-current-implementation-docs-alignment.md
├── 2026-06-02-docs-01-05-current-implementation-alignment.md
├── 2026-06-02-phase-1-decision-follow-up.md
├── 2026-06-02-phase-2-governance-alignment.md
├── 2026-06-02-phase-3-protected-surface-hardening.md
├── 2026-06-02-phase-4-eso-vault-runtime-diagnosis.md
├── 2026-06-02-stage-00-codex-harness-coverage-reconciliation.md
├── 2026-06-04-harness-four-element-alignment.md
├── 2026-06-05-harness-governance-v2-overlay.md
├── 2026-07-02-workspace-harness-implementation-audit-pack.md
├── 2026-07-02-workspace-harness-research-pack.md
├── 2026-07-03-template-contract-governance-migration.md
├── 2026-07-03-template-governance-audit-enhancement.md
├── 2026-07-03-workspace-document-governance-hardening.md
├── 2026-07-04-active-control-surface-governance-hardening.md
├── 2026-07-04-agent-governance-contract-normalization.md
├── 2026-07-04-workspace-document-contract-normalization.md
├── 2026-07-04-workspace-engineering-research-pack.md
├── 2026-07-05-template-path-numbering-contract.md
├── 2026-07-05-workspace-contract-governance-normalization.md
├── 2026-07-05-workspace-engineering-implementation-audit-pack.md
├── 2026-07-06-sdlc-lifecycle-contract.md
├── 2026-07-06-control-cloud-doc-normalization.md
├── 2026-07-06-stage03-04-repo-static-gap-closure.md
├── 2026-07-06-observability-and-network-review-agents.md
├── 2026-07-07-workspace-engineering-research-pack-refresh.md
├── 2026-07-10-current-research-pack-fact-first-hardening.md
├── 2026-07-11-governance-owner-and-roster-currentness.md
├── 2026-07-11-workspace-engineering-research-audit-integration.md
├── 2026-07-12-document-contract-registry.md
├── 2026-07-12-template-contract-consolidation.md
├── 2026-07-12-readme-workspace-profiles.md
├── 2026-07-12-semantic-document-validation.md
├── 2026-07-12-authored-document-migration.md
├── 2026-07-12-affected-surface-agent-qa.md
├── 2026-07-12-protected-surface-supply-chain-hardening.md
└── README.md
```

## Add and Find

1. 관련 PRD/ARD/ADR/Spec을 먼저 읽고 계획의 입력을 고정한다.
2. 새 Plan은 `../../99.templates/templates/sdlc/execution/plan.template.md`에서 시작하고, canonical target pattern은 `docs/04.execution/plans/YYYY-MM-DD-<feature>.md`다.
3. Plan은 언제, 누가, 어떤 순서로, 어떤 제약과 위험을 관리하며 작업을 진행하는지 정의한다.
4. Plan 변경 시 관련 `../tasks/`의 Parent Plan/Phase 링크와 Task ID를 확인한다.
5. 완료된 계획은 완료 기준, 검증 결과, 후속 문서 링크를 남기되 상세 evidence 정본은 Task 문서에 둔다.
6. live rollout, direct cluster mutation, secret write, external service action은 human approval gate와 rollback trigger를 명시한다.
7. 현재 구현과 상충하거나 superseded-only인 old Plan은 `../../98.archive/README.md`에만 인덱싱하고, 활성 Plan에서 Tombstone에 직접 연결하지 않는다.

### Relative Link Rules

이 README의 링크 기준 위치는 `docs/04.execution/plans/`다.

- 같은 폴더의 Plan 문서는 `./`로 시작하는 상대 경로를 사용한다.
- sibling Task stage는 `../tasks/`로 연결한다.
- upstream docs stage는 `../../01.requirements/`, `../../02.architecture/`, `../../03.specs/`처럼 `docs/` 기준으로 올라간다.
- Plan 안의 Task 링크는 `docs/04.execution/plans/`의 최종 Plan 파일 위치 기준으로 다시 계산한다.

### 문서 인덱스

| 문서                                                                                                                                 | 설명                                                                                                                                                                                                               | 상태 | 최종 수정  |
| ------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---- | ---------- |
| [`./2026-05-09-scripts-inventory-remediation.md`](./2026-05-09-scripts-inventory-remediation.md)                                     | `scripts/` 인벤토리 조사와 README 실행 계약 보정 계획                                                                                                                                                              | Done | 2026-05-21 |
| [`./2026-05-09-github-qa-ci-remediation.md`](./2026-05-09-github-qa-ci-remediation.md)                                               | `.github` QA, CI, 브랜치 정책, PR intake 계약 보정 계획                                                                                                                                                            | Done | 2026-05-09 |
| [`./2026-05-10-agent-first-harness-llm-wiki-hooks.md`](./2026-05-10-agent-first-harness-llm-wiki-hooks.md)                           | Agent-first harness, LLM Wiki, hook wiring 보정 계획                                                                                                                                                               | Done | 2026-05-10 |
| [`./2026-05-17-template-crosslink-fix.md`](./2026-05-17-template-crosslink-fix.md)                                                   | 문서 템플릿 target-relative 링크와 생성 문서 표시 경로 정합화 완료 이력. Plan과 Task record가 template link validation evidence를 소유한다.                                                                        | Done | 2026-05-21 |
| [`./2026-05-18-argo-rollouts-progressive-delivery.md`](./2026-05-18-argo-rollouts-progressive-delivery.md)                           | Argo Rollouts current-contract backfill 실행 계획                                                                                                                                                                  | Done | 2026-05-21 |
| [`./2026-05-18-argo-notifications-slack.md`](./2026-05-18-argo-notifications-slack.md)                                               | ArgoCD Notifications Slack current-contract backfill 실행 계획                                                                                                                                                     | Done | 2026-05-21 |
| [`./2026-05-22-docs-governance-full-ab-hardening.md`](./2026-05-22-docs-governance-full-ab-hardening.md)                             | README, lifecycle docs, agent/runtime governance, hook 경계, repo-static gate 정합화 계획                                                                                                                          | Done | 2026-05-22 |
| [`./2026-05-22-workspace-purpose-alignment.md`](./2026-05-22-workspace-purpose-alignment.md)                                         | 워크스페이스 목적 전체 기준 재감사, 버전 freshness, hook command boundary 보강 계획                                                                                                                                | Done | 2026-05-22 |
| [`./2026-05-24-p3-gitops-secret-runtime-remediation.md`](./2026-05-24-p3-gitops-secret-runtime-remediation.md)                       | 승인된 P3 ArgoCD/Vault/ESO/secret runtime remediation 실행 계획. Repo desired-state 보완은 완료됐고 live runtime 검증은 별도 follow-up이다.                                                                        | Done | 2026-06-04 |
| [`./2026-05-28-workspace-skill-expansion.md`](./2026-05-28-workspace-skill-expansion.md)                                             | repo-local skill expansion과 harness catalog routing 보강 계획                                                                                                                                                     | Done | 2026-05-28 |
| [`./2026-05-30-antigravity-governance.md`](./2026-05-30-antigravity-governance.md)                                                   | Gemini/Antigravity 하네스와 공통 Stage 00 거버넌스 정합화 계획                                                                                                                                                     | Done | 2026-06-02 |
| [`./2026-05-31-codex-governance-harness-alignment.md`](./2026-05-31-codex-governance-harness-alignment.md)                           | Codex/GPT 하네스, Model Policy, Template Contract drift 정합화 계획                                                                                                                                                | Done | 2026-05-31 |
| [`./2026-06-01-claude-agent-surface-restoration.md`](./2026-06-01-claude-agent-surface-restoration.md)                               | `.claude/agents`를 실제 Claude 전용 agent 파일 디렉터리로 복원하고 검증 게이트를 강화한 실행 계획                                                                                                                  | Done | 2026-06-01 |
| [`./2026-06-01-stage-00-canonical-adapter-redesign.md`](./2026-06-01-stage-00-canonical-adapter-redesign.md)                         | Stage 00 canonical adapter 모델로 공통 governance, provider adapter, template, hook, model policy, QA/CI gap을 변경 단위별로 정합화한 계획                                                                         | Done | 2026-06-01 |
| [`./2026-06-02-current-implementation-docs-alignment.md`](./2026-06-02-current-implementation-docs-alignment.md)                     | 현재 구현 기준으로 01-04 문서를 정렬하고 old 문서를 중앙 archive Tombstone으로 이동하는 실행 계획                                                                                                                  | Done | 2026-06-02 |
| [`./2026-06-02-docs-01-05-current-implementation-alignment.md`](./2026-06-02-docs-01-05-current-implementation-alignment.md)         | 현재 repo-backed 구현 기준으로 01-05 active 문서, 05.operations archive mirror, stale currentness gate를 정리한 실행 계획                                                                                          | Done | 2026-06-02 |
| [`./2026-06-02-phase-1-decision-follow-up.md`](./2026-06-02-phase-1-decision-follow-up.md)                                           | Phase 1 결정 항목을 후속 Phase 2 planning artifact로 고정하고 남은 QA skill/PATH/RTK gap boundary를 분리한 계획                                                                                                    | Done | 2026-06-02 |
| [`./2026-06-02-phase-2-governance-alignment.md`](./2026-06-02-phase-2-governance-alignment.md)                                       | Phase 1 governance alignment audit 결과를 Phase 2 Plan/Task 추적성으로 고정하고 live validation boundary를 분리한 계획                                                                                             | Done | 2026-06-02 |
| [`./2026-06-02-phase-3-protected-surface-hardening.md`](./2026-06-02-phase-3-protected-surface-hardening.md)                         | 승인된 policy/runtime/CI/template/live validation 범위에서 `.agents/**` shared asset trigger와 runtime readiness boundary를 보강한 계획                                                                            | Done | 2026-06-02 |
| [`./2026-06-02-phase-4-eso-vault-runtime-diagnosis.md`](./2026-06-02-phase-4-eso-vault-runtime-diagnosis.md)                         | Phase 3 live validation 실패를 Vault sealed runtime prerequisite로 분류하고 operator-bound 복구 경계를 고정한 계획                                                                                                 | Done | 2026-06-02 |
| [`./2026-06-02-stage-00-codex-harness-coverage-reconciliation.md`](./2026-06-02-stage-00-codex-harness-coverage-reconciliation.md)   | Phase 1 follow-up plan의 축소 범위를 보정하고 Stage 00/Codex harness 누락 항목을 기존 완료 증적에 연결한 계획                                                                                                      | Done | 2026-06-02 |
| [`./2026-06-04-harness-four-element-alignment.md`](./2026-06-04-harness-four-element-alignment.md)                                   | 하네스 네 요소를 공통 Stage 00, Codex, Claude runtime surface에 연결하고 문서 언어/템플릿/드리프트 GC 검증 게이트를 보강한 계획                                                                                    | Done | 2026-06-04 |
| [`./2026-06-05-harness-governance-v2-overlay.md`](./2026-06-05-harness-governance-v2-overlay.md)                                     | DAILY/LIBRARY 분류, workflow skill phase 기준, Hookify/eval/progress 단일화 계약을 기존 Stage 00 하네스 위에 덧붙인 계획                                                                                           | Done | 2026-06-05 |
| [`./2026-07-02-workspace-harness-implementation-audit-pack.md`](./2026-07-02-workspace-harness-implementation-audit-pack.md)         | `docs/90.references/audits/` 아래 workspace harness 구현 현황 감사 팩을 작성하고 research benchmark와 repo-backed evidence를 대조하는 실행 계획                                                                    | Done | 2026-07-03 |
| [`./2026-07-02-workspace-harness-research-pack.md`](./2026-07-02-workspace-harness-research-pack.md)                                 | `docs/90.references/research/` 통합 연구 팩 작성, 공식 외부 소스 우선 조사, market scan, implementation checklist, 검증 증적을 묶는 실행 계획                                                                      | Done | 2026-07-02 |
| [`./2026-07-03-template-contract-governance-migration.md`](./2026-07-03-template-contract-governance-migration.md)                   | `docs/99.templates/`를 template forms와 support contracts로 분리하고 validator, hook, governance, authored docs 적용을 추적하는 실행 계획                                                                          | Done | 2026-07-03 |
| [`./2026-07-03-template-governance-audit-enhancement.md`](./2026-07-03-template-governance-audit-enhancement.md)                     | `docs/99.templates/**` 후속 감사, support contract drift 정리, validator guardrail 보강, 최종 검증 증적을 묶는 실행 계획                                                                                           | Done | 2026-07-03 |
| [`./2026-07-03-workspace-document-governance-hardening.md`](./2026-07-03-workspace-document-governance-hardening.md)                 | workspace document type, provider entrypoint, README boundary, CI/QA governance hardening 실행 계획                                                                                                                | Done | 2026-07-04 |
| [`./2026-07-04-active-control-surface-governance-hardening.md`](./2026-07-04-active-control-surface-governance-hardening.md)         | `.github`, `scripts`, `gitops`, `infrastructure`, `policy`, `tests`, `traefik`, `examples/sample-app`의 active 운영 표면을 보강하고 AWS/Azure cloud examples를 dated snapshot으로 유지하는 실행 계획               | Done | 2026-07-04 |
| [`./2026-07-04-workspace-engineering-research-pack.md`](./2026-07-04-workspace-engineering-research-pack.md)                         | `docs/90.references/research/2026-07-04-wer/` 아래 dated research pack을 만들고 기존 4개 reference를 재배치하며 Kubernetes, infrastructure, security, automation, pipeline, workflow, QA 주제를 보강하는 실행 계획 | Done | 2026-07-04 |
| [`./2026-07-04-workspace-document-contract-normalization.md`](./2026-07-04-workspace-document-contract-normalization.md)             | active 문서와 historical evidence를 current frontmatter, section, template, CI/QA, validator 계약에 맞게 전면 정규화하는 실행 계획                                                                                 | Done | 2026-07-04 |
| [`./2026-07-04-agent-governance-contract-normalization.md`](./2026-07-04-agent-governance-contract-normalization.md)                 | Stage 00 governance와 Claude/Codex native role, repository-local baseline, local/Antigravity adapter, GitHub/QA/CI 표면을 정규화한 실행 계획 | Done | 2026-07-04 |
| [`./2026-07-05-workspace-engineering-implementation-audit-pack.md`](./2026-07-05-workspace-engineering-implementation-audit-pack.md) | `docs/90.references/audits/2026-07-05-wea/` 아래 part-based audit pack을 만들고 기존 audit 파일을 dated folder 구조로 정리하는 실행 계획                                                                           | Done | 2026-07-05 |
| [`./2026-07-05-template-path-numbering-contract.md`](./2026-07-05-template-path-numbering-contract.md)                               | Template path numbering contract implementation plan for PRD numeric renames, Stage 03 numbered feature-folder routing, template/support/governance/validator updates, and validation closure.                     | Done | 2026-07-05 |
| [`./2026-07-05-workspace-contract-governance-normalization.md`](./2026-07-05-workspace-contract-governance-normalization.md)         | Workspace contract governance normalization implementation plan for `_workspace` staging, frontmatter/template/section drift, CI/CD and QA control surfaces, validator coverage, and evidence closure.             | Done | 2026-07-06 |
| [`./2026-07-06-sdlc-lifecycle-contract.md`](./2026-07-06-sdlc-lifecycle-contract.md)                                                 | SDLC lifecycle contract implementation plan for status transitions, numeric lineage, handoff links, archive tombstone metadata, active-surface limits, `_workspace` staging, and validator gates.                  | Done | 2026-07-06 |
| [`./2026-07-06-control-cloud-doc-normalization.md`](./2026-07-06-control-cloud-doc-normalization.md)                                 | Historical implementation plan for frontmatter-free control surfaces and the cloud normalization tranche later superseded by Spec 030 Stage 90 consolidation and retired-path enforcement.                        | Done | 2026-07-14 |
| [`./2026-07-06-stage03-04-repo-static-gap-closure.md`](./2026-07-06-stage03-04-repo-static-gap-closure.md)                           | Stage 03/04 repo-static gap closure implementation plan for evidence-lane classification, WER lifecycle drift closure, operator-approved follow-up routing, and validation closure.                                | Done | 2026-07-06 |
| [`./2026-07-06-observability-and-network-review-agents.md`](./2026-07-06-observability-and-network-review-agents.md)                 | Implementation plan for adding `observability-reviewer` and `network-reviewer` worker agents across three tracked adapter surfaces and the harness catalog.                                                               | Done | 2026-07-06 |
| [`./2026-07-07-workspace-engineering-research-pack-refresh.md`](./2026-07-07-workspace-engineering-research-pack-refresh.md)         | Implementation plan for workspace engineering research pack refresh.                                                                                                                                               | Done | 2026-07-07 |
| [`./2026-07-10-current-research-pack-fact-first-hardening.md`](./2026-07-10-current-research-pack-fact-first-hardening.md)           | Fact-first in-place audit, external-source refresh, related-document integration, provider-model currentness analysis, and review plan for the Current workspace engineering research pack.                           | Done | 2026-07-10 |
| [`./2026-07-11-governance-owner-and-roster-currentness.md`](./2026-07-11-governance-owner-and-roster-currentness.md)               | Evidence-preserving audit IA, complete Spec/Plan lifecycle reconciliation, and RMD-004 ten-role/30-adapter roster currentness implementation plan.                                                                    | Done   | 2026-07-11 |
| [`./2026-07-11-workspace-engineering-research-audit-integration.md`](./2026-07-11-workspace-engineering-research-audit-integration.md) | Completed thirteen-task workspace engineering research and implementation-audit integration ledger relocated from the Current Stage 90 audit pack.                                                                  | Done | 2026-07-11 |
| [`./2026-07-12-document-contract-registry.md`](./2026-07-12-document-contract-registry.md) | Declarative document registry, schema, classifier, baseline inventory, and compatibility-gate implementation plan. | Done | 2026-07-12 |
| [`./2026-07-12-template-contract-consolidation.md`](./2026-07-12-template-contract-consolidation.md) | Stage 99 support/form consolidation, legacy template removal, and measured authored-document compatibility plan. | Done   | 2026-07-12 |
| [`./2026-07-12-readme-workspace-profiles.md`](./2026-07-12-readme-workspace-profiles.md) | Completed RWP-001 through RWP-006 plan for 72 path-derived README profiles, five cloud handoffs, and the `_workspace` boundary. | Done | 2026-07-12 |
| [`./2026-07-12-semantic-document-validation.md`](./2026-07-12-semantic-document-validation.md) | Registry-driven frontmatter, section, link, index, owner, migration-ledger, and reciprocal execution-lineage validation plan. | Done | 2026-07-12 |
| [`./2026-07-12-authored-document-migration.md`](./2026-07-12-authored-document-migration.md) | Full authored-document migration, durable research ledger, cloud SDLC consolidation, strict cutover, and reciprocal [Task](../tasks/2026-07-12-authored-document-migration.md) plan. | Done | 2026-07-13 |
| [`./2026-07-12-affected-surface-agent-qa.md`](./2026-07-12-affected-surface-agent-qa.md) | Completed ASQA-001 through ASQA-006 plan for canonical affected-surface selection, local/CI parity, cross-surface role semantics, and Stage 00 QA handoff with reciprocal [Spec](../../03.specs/031-affected-surface-agent-qa/spec.md) and [Task](../tasks/2026-07-12-affected-surface-agent-qa.md) lineage. | Done | 2026-07-14 |
| [`./2026-07-12-protected-surface-supply-chain-hardening.md`](./2026-07-12-protected-surface-supply-chain-hardening.md) | Completed PSH-001 through PSH-006 plan for immutable Action identity, least privilege, identity-only GitOps review, local-only Vault/ESO and secret-boundary hardening, and repository-static closure with reciprocal [Spec](../../03.specs/032-protected-surface-supply-chain-hardening/spec.md) and [Task](../tasks/2026-07-12-protected-surface-supply-chain-hardening.md) lineage. | Done | 2026-07-14 |

## Related Documents

- [Execution README](../README.md)
- [Docs README](../../README.md)
- [03.specs](../../03.specs/README.md)
- [04.execution/tasks](../tasks/README.md)
- [05.operations/policies](../../05.operations/policies/README.md)
- [Plan Template](../../99.templates/templates/sdlc/execution/plan.template.md)
- [Archive Index](../../98.archive/README.md)
