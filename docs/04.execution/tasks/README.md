# 04.execution/tasks

> 구현 작업 단위, 검증 증적, 완료 상태를 추적하는 Task stage다.

> [!NOTE]
> All AI agent interactions with this stage must comply with the [Agent Governance Hub](../../00.agent-governance/README.md).

## Overview

이 경로는 Plan과 Spec에서 파생된 구현, 검증, 평가 작업 단위의 canonical stage다.
Task 문서는 단순 TODO가 아니라 작업 ID, 상태, 검증 기준, 실행 명령, evidence를 함께 보존하는 실행 추적 위치다.
`../plans/`가 순서와 위험 관리를 소유하고, 이 경로는 실제 작업 상태와 완료 증거를 소유한다.

## Audience

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

## Structure

```text
04.execution/tasks/
├── 2026-03-27-wsl-k3d-argocd-platform.md
├── 2026-03-28-wsl2-k3d-argocd-ha-platform.md
├── 2026-03-29-platform-expansion.md
├── 2026-05-09-github-qa-ci-remediation.md
├── 2026-05-09-k3d-agent-first-remediation.md
├── 2026-05-09-scripts-inventory-remediation.md
├── 2026-05-10-agent-first-harness-llm-wiki-hooks.md
├── 2026-05-18-argo-rollouts-progressive-delivery.md
├── 2026-05-18-argo-notifications-slack.md
├── 2026-05-22-docs-governance-full-ab-hardening.md
├── 2026-05-22-workspace-purpose-alignment.md
├── 2026-05-22-spec-execution-implementation-audit.md
├── 2026-05-24-p3-gitops-secret-runtime-remediation.md
├── 2026-05-28-docs-governance-consistency.md
├── 2026-05-28-workspace-skill-expansion.md
├── 2026-05-30-antigravity-governance.md
├── 2026-05-30-governance-refactoring.md
├── 2026-05-31-codex-governance-harness-alignment.md
├── 2026-06-01-claude-agent-surface-restoration.md
├── 2026-06-01-stage-00-canonical-adapter-redesign.md
├── 2026-06-02-stage-00-codex-harness-coverage-reconciliation.md
└── README.md
```

## How to Work in This Area

1. 작업의 Parent Spec 또는 Parent Plan을 먼저 확인한다.
2. 새 Task 문서는 `../../99.templates/task.template.md`에서 시작하고, canonical target pattern은 `docs/04.execution/tasks/YYYY-MM-DD-<feature-or-stream>.md`다.
3. 각 작업은 Task ID, Type, Parent Spec/Plan, Validation/Evidence, Owner, Status를 가진다.
4. 권장 Type은 `impl`, `test`, `eval`, `doc`, `ops`다. Agent-specific 작업은 `prompt`, `tool`, `memory`, `guardrail`, `eval`, `observability`를 사용할 수 있다.
5. 핵심 동작은 테스트 우선(TDD)을 기본값으로 하고, 문서-only 작업도 검증 evidence를 남긴다.
6. 기능 수준의 보조 `tasks.md`가 `../../03.specs/<feature-id>/`에 있더라도, 팀 실행·스프린트·검증 집계의 정본은 이 경로다.

## Link Basis

이 README의 링크 기준 위치는 `docs/04.execution/tasks/`다.

- 같은 폴더의 Task 문서는 `./`로 시작하는 상대 경로를 사용한다.
- sibling Plan stage는 `../plans/`로 연결한다.
- upstream docs stage는 `../../03.specs/`, `../../02.architecture/`, `../../01.requirements/`처럼 `docs/` 기준으로 올라간다.
- Task 안의 Plan/Spec 링크는 `docs/04.execution/tasks/`의 최종 Task 파일 위치 기준으로 다시 계산한다.

## 문서 인덱스

| 문서                                                                                                           | 설명                                                                                                                                   | 상태 | 최종 수정  |
| -------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | ---- | ---------- |
| [`./2026-03-27-wsl-k3d-argocd-platform.md`](./2026-03-27-wsl-k3d-argocd-platform.md)                           | 초기 GitOps 플랫폼 Task의 historical closure와 repo-static/live evidence boundary                                                      | Done | 2026-05-22 |
| [`./2026-03-28-wsl2-k3d-argocd-ha-platform.md`](./2026-03-28-wsl2-k3d-argocd-ha-platform.md)                   | RED/GREEN/REFACTOR 기반 TLS/Ingress + CI static contract/workflow-security 작업 Task                                                   | Done | 2026-05-22 |
| [`./2026-03-29-platform-expansion.md`](./2026-03-29-platform-expansion.md)                                     | 2026-03-29 IP 수정 + cert-manager/Dashboard/Istio/Kiali 확장 Task, 현재 실행계약은 Headlamp/172.18.x 기준                              | Done | 2026-05-18 |
| [`./2026-05-09-k3d-agent-first-remediation.md`](./2026-05-09-k3d-agent-first-remediation.md)                   | k3d 운영 문서, Agent-first 실행 계약, 구조적 템플릿 coverage, lifecycle hook hardening 보정 Task                                       | Done | 2026-05-22 |
| [`./2026-05-09-scripts-inventory-remediation.md`](./2026-05-09-scripts-inventory-remediation.md)               | `scripts/` 인벤토리 조사와 README 실행 계약 보정 Task                                                                                  | Done | 2026-05-21 |
| [`./2026-05-09-github-qa-ci-remediation.md`](./2026-05-09-github-qa-ci-remediation.md)                         | `.github` QA, CI, 브랜치 정책, PR intake 계약 보정 Task                                                                                | Done | 2026-05-09 |
| [`./2026-05-10-agent-first-harness-llm-wiki-hooks.md`](./2026-05-10-agent-first-harness-llm-wiki-hooks.md)     | Agent-first harness, LLM Wiki, hook 계약 보정 Task                                                                                     | Done | 2026-05-10 |
| [`./2026-05-18-argo-rollouts-progressive-delivery.md`](./2026-05-18-argo-rollouts-progressive-delivery.md)     | Argo Rollouts current-contract backfill Task                                                                                           | Done | 2026-05-22 |
| [`./2026-05-18-argo-notifications-slack.md`](./2026-05-18-argo-notifications-slack.md)                         | ArgoCD Notifications Slack current-contract backfill Task                                                                              | Done | 2026-05-22 |
| [`./2026-05-22-docs-governance-full-ab-hardening.md`](./2026-05-22-docs-governance-full-ab-hardening.md)       | README, lifecycle docs, agent/runtime governance, hook 경계, repo-static gate 정합화 Task                                              | Done | 2026-05-22 |
| [`./2026-05-22-workspace-purpose-alignment.md`](./2026-05-22-workspace-purpose-alignment.md)                   | 워크스페이스 목적 전체 기준 재감사, 버전 freshness, hook command boundary 보강 Task                                                    | Done | 2026-05-22 |
| [`./2026-05-22-spec-execution-implementation-audit.md`](./2026-05-22-spec-execution-implementation-audit.md)   | `docs/03.specs`와 `docs/04.execution` 구현 evidence 재감사 및 Spec status 보정 Task                                                    | Done | 2026-05-22 |
| [`./2026-05-24-p3-gitops-secret-runtime-remediation.md`](./2026-05-24-p3-gitops-secret-runtime-remediation.md) | 승인된 P3 ArgoCD/Vault/ESO/secret runtime remediation Task. Repo desired-state 보완은 완료됐고 live runtime 검증은 별도 follow-up이다. | Done | 2026-05-25 |
| [`./2026-05-28-docs-governance-consistency.md`](./2026-05-28-docs-governance-consistency.md)                   | 문서 거버넌스 일관성 정비 Task — templates, policies, runbooks, guides, plans/tasks 준수율 향상 및 레거시 파일 제거                    | Done | 2026-05-29 |
| [`./2026-05-28-workspace-skill-expansion.md`](./2026-05-28-workspace-skill-expansion.md)                       | repo-local skill expansion과 harness catalog routing 보강 Task                                                                        | Done | 2026-05-28 |
| [`./2026-05-30-antigravity-governance.md`](./2026-05-30-antigravity-governance.md)                             | Gemini/Antigravity 하네스와 공통 Stage 00 거버넌스 정합화 Task                                                                        | Active | 2026-05-30 |
| [`./2026-05-30-governance-refactoring.md`](./2026-05-30-governance-refactoring.md)                             | 공통 AI Agent governance, template contract, model policy refactoring Task. 2026-06-01 canonical adapter Task로 superseded             | Superseded | 2026-06-01 |
| [`./2026-05-31-codex-governance-harness-alignment.md`](./2026-05-31-codex-governance-harness-alignment.md)     | Codex/GPT 하네스, Model Policy, Template Contract drift 정합화 Task                                                                   | Done | 2026-05-31 |
| [`./2026-06-01-claude-agent-surface-restoration.md`](./2026-06-01-claude-agent-surface-restoration.md)         | `.claude/agents`를 실제 Claude 전용 agent 파일 디렉터리로 복원하고 검증 게이트를 강화한 작업 추적                                    | Done | 2026-06-01 |
| [`./2026-06-01-stage-00-canonical-adapter-redesign.md`](./2026-06-01-stage-00-canonical-adapter-redesign.md)   | Stage 00 canonical adapter 모델로 governance, provider adapter, template, hook, model policy, QA/CI 정합화를 완료 추적한 Task        | Done | 2026-06-01 |
| [`./2026-06-02-stage-00-codex-harness-coverage-reconciliation.md`](./2026-06-02-stage-00-codex-harness-coverage-reconciliation.md) | Phase 1 follow-up plan의 축소 범위와 Stage 00/Codex harness 누락 항목을 기존 완료 증적에 연결한 보정 Task | Done | 2026-06-02 |

## Related Documents

- [Execution README](../README.md)
- [Docs README](../../README.md)
- [03.specs](../../03.specs/README.md)
- [04.execution/plans](../plans/README.md)
- [05.operations/incidents](../../05.operations/incidents/README.md)
- [Task Template](../../99.templates/task.template.md)
