# 04.execution/tasks

> 구현 작업 단위, 검증 증적, 완료 상태를 추적하는 Task stage다.

> [!NOTE]
> All AI agent interactions with this stage must comply with the [Agent Governance Hub](../../00.agent-governance/README.md).

## Overview

이 경로는 Plan과 Spec에서 파생된 구현, 검증, 평가 작업 단위의 canonical stage다.
Task 문서는 단순 TODO가 아니라 작업 ID, 상태, 검증 기준, 실행 명령, evidence를 함께 보존하는 실행 추적 위치다.
`../plans/`가 순서와 위험 관리를 소유하고, 이 경로는 실제 작업 상태와 완료 증거를 소유한다.

### Collection Readers

이 README의 주요 독자:

- Platform Engineers
- Operators
- QA/Verification Reviewers
- AI Agents

## Scope

### In Scope

- 구현, 테스트, 평가, 문서, 운영 작업 단위
- Parent Spec/Plan 링크와 phase/Task ID 추적
- 검증 기준, 실행 명령, 로그 또는 evidence 위치
- 소유자, 상태, 완료 여부, handoff 메모
- Agent 작업의 prompt, tool, memory, guardrail, eval, observability task

### Out of Scope

- 전체 시스템 설계 설명
- 운영 정책 정의
- 장애 대응 절차
- 근본 원인 분석
- future implementation narrative without executable task evidence

이 내용은 각각 `../../03.specs/`, `../../05.operations/policies/`, `../../05.operations/runbooks/`, `../../05.operations/incidents/`로 분리한다.

## Item Index

```text
04.execution/tasks/
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
├── 2026-06-02-phase-1-governance-alignment-audit.md
├── 2026-06-02-phase-2-governance-alignment.md
├── 2026-06-02-phase-3-protected-surface-hardening.md
├── 2026-06-02-phase-4-eso-vault-runtime-diagnosis.md
├── 2026-06-02-stage-00-codex-harness-coverage-reconciliation.md
├── 2026-06-04-harness-four-element-alignment.md
├── 2026-06-05-harness-connective-layer-risk-closure.md
├── 2026-06-05-harness-governance-v2-overlay.md
├── 2026-06-05-language-boundary-alignment.md
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
└── README.md
```

## Add and Find

1. 작업의 Parent Spec 또는 Parent Plan을 먼저 확인한다.
2. 새 Task 문서는 `../../99.templates/templates/sdlc/execution/task.template.md`에서 시작하고, canonical target pattern은 `docs/04.execution/tasks/YYYY-MM-DD-<feature-or-stream>.md`다.
3. 각 작업은 Task ID, Type, Parent Spec/Plan, Validation/Evidence, Owner, Status를 가진다.
4. 권장 Type은 `impl`, `test`, `eval`, `doc`, `ops`다. Agent-specific 작업은 `prompt`, `tool`, `memory`, `guardrail`, `eval`, `observability`를 사용할 수 있다.
5. 핵심 동작은 테스트 우선(TDD)을 기본값으로 하고, 문서-only 작업도 검증 evidence를 남긴다.
6. 기능 수준의 보조 `tasks.md`가 `../../03.specs/<feature-id>/`에 있더라도, 팀 실행·스프린트·검증 집계의 정본은 이 경로다.
7. 현재 구현과 상충하거나 superseded-only인 old Task는 `../../98.archive/README.md`에만 인덱싱하고, 활성 Task에서 Tombstone에 직접 연결하지 않는다.

### Relative Link Rules

이 README의 링크 기준 위치는 `docs/04.execution/tasks/`다.

- 같은 폴더의 Task 문서는 `./`로 시작하는 상대 경로를 사용한다.
- sibling Plan stage는 `../plans/`로 연결한다.
- upstream docs stage는 `../../03.specs/`, `../../02.architecture/`, `../../01.requirements/`처럼 `docs/` 기준으로 올라간다.
- Task 안의 Plan/Spec 링크는 `docs/04.execution/tasks/`의 최종 Task 파일 위치 기준으로 다시 계산한다.

### 문서 인덱스

| 문서                                                                                                                                 | 설명                                                                                                                                                                                                                                                                    | 상태 | 최종 수정  |
| ------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---- | ---------- |
| [`./2026-05-09-scripts-inventory-remediation.md`](./2026-05-09-scripts-inventory-remediation.md)                                     | `scripts/` 인벤토리 조사와 README 실행 계약 보정 Task                                                                                                                                                                                                                   | Done | 2026-05-21 |
| [`./2026-05-09-github-qa-ci-remediation.md`](./2026-05-09-github-qa-ci-remediation.md)                                               | `.github` QA, CI, 브랜치 정책, PR intake 계약 보정 Task                                                                                                                                                                                                                 | Done | 2026-05-09 |
| [`./2026-05-10-agent-first-harness-llm-wiki-hooks.md`](./2026-05-10-agent-first-harness-llm-wiki-hooks.md)                           | Agent-first harness, LLM Wiki, hook 계약 보정 Task                                                                                                                                                                                                                      | Done | 2026-05-10 |
| [`./2026-05-17-template-crosslink-fix.md`](./2026-05-17-template-crosslink-fix.md)                                                   | Template target-relative link display labels, generated document path text, and validation evidence alignment Task                                                                                                                                                      | Done | 2026-05-21 |
| [`./2026-05-18-argo-rollouts-progressive-delivery.md`](./2026-05-18-argo-rollouts-progressive-delivery.md)                           | Argo Rollouts current-contract backfill Task                                                                                                                                                                                                                            | Done | 2026-05-22 |
| [`./2026-05-18-argo-notifications-slack.md`](./2026-05-18-argo-notifications-slack.md)                                               | ArgoCD Notifications Slack current-contract backfill Task                                                                                                                                                                                                               | Done | 2026-05-22 |
| [`./2026-05-22-docs-governance-full-ab-hardening.md`](./2026-05-22-docs-governance-full-ab-hardening.md)                             | README, lifecycle docs, agent/runtime governance, hook 경계, repo-static gate 정합화 Task                                                                                                                                                                               | Done | 2026-05-22 |
| [`./2026-05-22-workspace-purpose-alignment.md`](./2026-05-22-workspace-purpose-alignment.md)                                         | 워크스페이스 목적 전체 기준 재감사, 버전 freshness, hook command boundary 보강 Task                                                                                                                                                                                     | Done | 2026-05-22 |
| [`./2026-05-24-p3-gitops-secret-runtime-remediation.md`](./2026-05-24-p3-gitops-secret-runtime-remediation.md)                       | 승인된 P3 ArgoCD/Vault/ESO/secret runtime remediation Task. Repo desired-state 보완은 완료됐고 live runtime 검증은 별도 follow-up이다.                                                                                                                                  | Done | 2026-05-24 |
| [`./2026-05-28-workspace-skill-expansion.md`](./2026-05-28-workspace-skill-expansion.md)                                             | repo-local skill expansion과 harness catalog routing 보강 Task                                                                                                                                                                                                          | Done | 2026-05-28 |
| [`./2026-05-30-antigravity-governance.md`](./2026-05-30-antigravity-governance.md)                                                   | Gemini/Antigravity 하네스와 공통 Stage 00 거버넌스 정합화 Task                                                                                                                                                                                                          | Done | 2026-06-02 |
| [`./2026-05-31-codex-governance-harness-alignment.md`](./2026-05-31-codex-governance-harness-alignment.md)                           | Codex/GPT 하네스, Model Policy, Template Contract drift 정합화 Task                                                                                                                                                                                                     | Done | 2026-05-31 |
| [`./2026-06-01-claude-agent-surface-restoration.md`](./2026-06-01-claude-agent-surface-restoration.md)                               | `.claude/agents`를 실제 Claude 전용 agent 파일 디렉터리로 복원하고 검증 게이트를 강화한 작업 추적                                                                                                                                                                       | Done | 2026-06-01 |
| [`./2026-06-01-stage-00-canonical-adapter-redesign.md`](./2026-06-01-stage-00-canonical-adapter-redesign.md)                         | Stage 00 canonical adapter 모델로 governance, provider adapter, template, hook, model policy, QA/CI 정합화를 완료 추적한 Task                                                                                                                                           | Done | 2026-06-01 |
| [`./2026-06-02-current-implementation-docs-alignment.md`](./2026-06-02-current-implementation-docs-alignment.md)                     | 현재 구현 기준 01-04 문서 정렬, central archive Tombstone 전환, QA/CI gate 보강 증적                                                                                                                                                                                    | Done | 2026-06-02 |
| [`./2026-06-02-docs-01-05-current-implementation-alignment.md`](./2026-06-02-docs-01-05-current-implementation-alignment.md)         | 현재 repo-backed 구현 기준 01-05 active 문서, 05.operations archive mirror, stale currentness gate를 정리한 Task                                                                                                                                                        | Done | 2026-06-02 |
| [`./2026-06-02-phase-1-governance-alignment-audit.md`](./2026-06-02-phase-1-governance-alignment-audit.md)                           | Phase 1 governance, provider adapter, docs lifecycle, QA/CI/CD, GitOps 정합성 재감사와 gap ledger                                                                                                                                                                       | Done | 2026-06-02 |
| [`./2026-06-02-phase-2-governance-alignment.md`](./2026-06-02-phase-2-governance-alignment.md)                                       | Phase 1 감사 결과를 Phase 2 Plan/Task 추적성으로 고정하는 작업 단위와 검증 증거                                                                                                                                                                                         | Done | 2026-06-02 |
| [`./2026-06-02-phase-3-protected-surface-hardening.md`](./2026-06-02-phase-3-protected-surface-hardening.md)                         | 승인된 보호 표면 범위에서 `.agents/**` shared asset trigger, hook runtime, template guidance, live validation evidence를 보강한 Task                                                                                                                                    | Done | 2026-06-02 |
| [`./2026-06-02-phase-4-eso-vault-runtime-diagnosis.md`](./2026-06-02-phase-4-eso-vault-runtime-diagnosis.md)                         | ESO/Vault live readiness 실패를 Vault sealed 상태로 분류하고 runbook/operator-bound 복구 경계를 보강한 Task                                                                                                                                                             | Done | 2026-06-02 |
| [`./2026-06-02-stage-00-codex-harness-coverage-reconciliation.md`](./2026-06-02-stage-00-codex-harness-coverage-reconciliation.md)   | Phase 1 follow-up plan의 축소 범위와 Stage 00/Codex harness 누락 항목을 기존 완료 증적에 연결한 보정 Task                                                                                                                                                               | Done | 2026-06-02 |
| [`./2026-06-04-harness-four-element-alignment.md`](./2026-06-04-harness-four-element-alignment.md)                                   | 하네스 네 요소와 Codex/Claude 보강, 문서 언어/템플릿/드리프트 GC 검증 evidence를 추적한 Task                                                                                                                                                                            | Done | 2026-06-04 |
| [`./2026-06-05-harness-connective-layer-risk-closure.md`](./2026-06-05-harness-connective-layer-risk-closure.md)                     | 하네스 연결 레이어의 Remaining Risk와 Follow-up Tasks를 repo-static evidence 및 승인 경계 기준으로 닫은 Task                                                                                                                                                            | Done | 2026-06-05 |
| [`./2026-06-05-harness-governance-v2-overlay.md`](./2026-06-05-harness-governance-v2-overlay.md)                                     | DAILY/LIBRARY 분류, workflow skill phase 기준, Hookify local advisory, deterministic eval, progress 단일화 검증 evidence를 추적한 Task                                                                                                                                  | Done | 2026-06-05 |
| [`./2026-06-05-language-boundary-alignment.md`](./2026-06-05-language-boundary-alignment.md)                                         | AI Agent 문서와 사람용 문서의 언어 경계를 조사하고 Stage 03/04 영어-first 정책과 operations 역할을 보강한 Task                                                                                                                                                          | Done | 2026-06-05 |
| [`./2026-07-02-workspace-harness-implementation-audit-pack.md`](./2026-07-02-workspace-harness-implementation-audit-pack.md)         | `docs/90.references/audits/` 구현 현황 감사 팩의 작성, benchmark-to-evidence 비교, automation opportunity, repo-static 검증 evidence를 추적                                                                                                                             | Done | 2026-07-03 |
| [`./2026-07-02-workspace-harness-research-pack.md`](./2026-07-02-workspace-harness-research-pack.md)                                 | `docs/90.references/research/` 통합 연구 팩의 작성, 소스 검증, market scan, implementation checklist, repo-static 검증 evidence 추적                                                                                                                                    | Done | 2026-07-02 |
| [`./2026-07-03-template-contract-governance-migration.md`](./2026-07-03-template-contract-governance-migration.md)                   | template contract/governance migration의 support baseline, template path migration, frontmatter cleanup, authored docs 적용, final validation evidence를 추적                                                                                                           | Done | 2026-07-03 |
| [`./2026-07-03-template-governance-audit-enhancement.md`](./2026-07-03-template-governance-audit-enhancement.md)                     | template governance 후속 audit findings, support contract drift 정리, validator hardening, final validation evidence를 추적                                                                                                                                             | Done | 2026-07-03 |
| [`./2026-07-03-workspace-document-governance-hardening.md`](./2026-07-03-workspace-document-governance-hardening.md)                 | workspace document governance hardening의 audit, core contract, provider entrypoint, workspace application, validation evidence를 추적                                                                                                                                  | Done | 2026-07-04 |
| [`./2026-07-04-active-control-surface-governance-hardening.md`](./2026-07-04-active-control-surface-governance-hardening.md)         | Active control surface governance hardening evidence for GitHub, CI/CD, QA, GitOps, infrastructure, policy, scripts, tests, Traefik, and sample-app snapshot boundaries.                                                                                                | Done | 2026-07-04 |
| [`./2026-07-04-agent-governance-contract-normalization.md`](./2026-07-04-agent-governance-contract-normalization.md)                 | agent governance contract normalization evidence와 baseline drift inventory를 추적                                                                                                                                                                                      | Done | 2026-07-04 |
| [`./2026-07-04-workspace-document-contract-normalization.md`](./2026-07-04-workspace-document-contract-normalization.md)             | active 문서와 historical evidence의 frontmatter, section, template, reference, CI/QA, validator 정규화 작업과 검증 evidence를 추적                                                                                                                                      | Done | 2026-07-04 |
| [`./2026-07-04-workspace-engineering-research-pack.md`](./2026-07-04-workspace-engineering-research-pack.md)                         | Workspace engineering research pack evidence for dated Stage 90 research references, existing reference moves, external-source refresh, Kubernetes/infrastructure/security, automation/pipeline/workflow/QA, AI agents roster and gap analysis, and validation closure. | Done | 2026-07-06 |
| [`./2026-07-05-template-path-numbering-contract.md`](./2026-07-05-template-path-numbering-contract.md)                               | Template path numbering contract execution evidence for PRD numeric renames, Stage 03 numbered feature-folder routing, template/support/governance/validator updates, and validation closure.                                                                           | Done | 2026-07-05 |
| [`./2026-07-05-workspace-contract-governance-normalization.md`](./2026-07-05-workspace-contract-governance-normalization.md)         | `_workspace` staging, frontmatter/template drift, CI/CD와 QA control-surface baseline inventory를 추적하는 workspace contract governance normalization Task                                                                                                             | Done | 2026-07-06 |
| [`./2026-07-05-workspace-engineering-implementation-audit-pack.md`](./2026-07-05-workspace-engineering-implementation-audit-pack.md) | Workspace engineering implementation audit pack evidence for dated Stage 90 audit folderization, part-based implementation reports, automation opportunities, and validation closure.                                                                                   | Done | 2026-07-05 |
| [`./2026-07-06-sdlc-lifecycle-contract.md`](./2026-07-06-sdlc-lifecycle-contract.md)                                                 | SDLC lifecycle, numbering, archive metadata, active-surface, `_workspace`, and deterministic validation contract implementation evidence.                                                                                                                               | Done | 2026-07-06 |
| [`./2026-07-06-control-cloud-doc-normalization.md`](./2026-07-06-control-cloud-doc-normalization.md)                                 | Control surface and cloud example documentation normalization evidence for frontmatter-free control surfaces, example-local SDLC snapshot routes, AWS/Azure docs, and repository-static validation.                                                                     | Done | 2026-07-06 |
| [`./2026-07-06-stage03-04-repo-static-gap-closure.md`](./2026-07-06-stage03-04-repo-static-gap-closure.md)                           | Stage 03/04 repo-static gap closure evidence for WER lifecycle drift, operator-approved follow-up routing, and validation closure.                                                                                                                                      | Done | 2026-07-06 |
| [`./2026-07-06-observability-and-network-review-agents.md`](./2026-07-06-observability-and-network-review-agents.md)                 | Task evidence for adding `observability-reviewer` and `network-reviewer` worker agents across three provider adapters and the harness catalog.                                                                                                                          | Done | 2026-07-06 |
| [`./2026-07-07-workspace-engineering-research-pack-refresh.md`](./2026-07-07-workspace-engineering-research-pack-refresh.md)         | Task evidence for workspace engineering research pack refresh.                                                                                                                                                                                                          | Done | 2026-07-07 |
| [`./2026-07-10-current-research-pack-fact-first-hardening.md`](./2026-07-10-current-research-pack-fact-first-hardening.md)           | Current research pack fact-first audit, source refresh, related-document integration, and validation evidence.                                                                                                                                                           | Done | 2026-07-10 |
| [`./2026-07-11-governance-owner-and-roster-currentness.md`](./2026-07-11-governance-owner-and-roster-currentness.md)               | Governance owner, lifecycle, audit IA, Plan evidence, and ten-role/30-adapter roster currentness implementation evidence.                                                                                                                                                | Done   | 2026-07-11 |
| [`./2026-07-11-workspace-engineering-research-audit-integration.md`](./2026-07-11-workspace-engineering-research-audit-integration.md) | Compact completion evidence for the thirteen-task workspace engineering research and implementation-audit integration, publication commits, reviews, and repository-static boundaries.                                                                                | Done | 2026-07-11 |
| [`./2026-07-12-document-contract-registry.md`](./2026-07-12-document-contract-registry.md) | Document contract registry schema, classifier, approved corpus, compatibility gate, and validation evidence. | Done | 2026-07-12 |
| [`./2026-07-12-template-contract-consolidation.md`](./2026-07-12-template-contract-consolidation.md) | Stage 99 support/form consolidation, canonical template normalization, legacy Task form removal, and compatibility evidence. | Done   | 2026-07-12 |
| [`./2026-07-12-readme-workspace-profiles.md`](./2026-07-12-readme-workspace-profiles.md) | Completed RWP-001 through RWP-006 evidence for 72 path-derived README profiles, five cloud handoffs, and the `_workspace` boundary. | Done | 2026-07-12 |
| [`./2026-07-12-semantic-document-validation.md`](./2026-07-12-semantic-document-validation.md) | SMDV-001 through SMDV-004 execution evidence for registry-driven document and cross-document validation. | Done | 2026-07-12 |

## Related Documents

- [Execution README](../README.md)
- [Docs README](../../README.md)
- [03.specs](../../03.specs/README.md)
- [04.execution/plans](../plans/README.md)
- [05.operations/incidents](../../05.operations/incidents/README.md)
- [Task Template](../../99.templates/templates/sdlc/execution/task.template.md)
- [Archive Index](../../98.archive/README.md)
