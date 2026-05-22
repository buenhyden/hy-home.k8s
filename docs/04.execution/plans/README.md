# 04.execution/plans

> 실행 순서, 리스크, 롤아웃, 검증 게이트를 정의하는 Plan stage다.

> [!NOTE]
> All AI agent interactions with this stage must comply with the [Agent Governance Hub](../../00.agent-governance/README.md).

## Overview

이 경로는 승인된 요구와 기술 계약을 실행 순서, 위험 관리, 검증 게이트로 전환하는 Plan stage다.
Plan은 구현을 시작하기 전 작업 흐름, 롤아웃/롤백, 완료 기준을 합의하는 문서다.
Task evidence는 `../tasks/`가 소유하고, Plan은 그 evidence가 어떤 순서와 기준으로 만들어져야 하는지 정의한다.

## Audience

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

## Structure

```text
04.execution/plans/
├── 2026-03-27-wsl-k3d-argocd-platform.md
├── 2026-03-28-wsl2-k3d-argocd-ha-platform.md
├── 2026-03-29-platform-expansion.md
├── 2026-05-09-github-qa-ci-remediation.md
├── 2026-05-09-k3d-agent-first-remediation.md
├── 2026-05-09-scripts-inventory-remediation.md
├── 2026-05-10-agent-first-harness-llm-wiki-hooks.md
├── 2026-05-17-template-crosslink-fix.md
├── 2026-05-18-argo-rollouts-progressive-delivery.md
├── 2026-05-18-argo-notifications-slack.md
├── 2026-05-22-docs-governance-full-ab-hardening.md
└── README.md
```

## How to Work in This Area

1. 관련 PRD/ARD/ADR/Spec을 먼저 읽고 계획의 입력을 고정한다.
2. 새 Plan은 `../../99.templates/plan.template.md`에서 시작하고, canonical target pattern은 `docs/04.execution/plans/YYYY-MM-DD-<feature>.md`다.
3. Plan은 언제, 누가, 어떤 순서로, 어떤 제약과 위험을 관리하며 작업을 진행하는지 정의한다.
4. Plan 변경 시 관련 `../tasks/`의 Parent Plan/Phase 링크와 Task ID를 확인한다.
5. 완료된 계획은 완료 기준, 검증 결과, 후속 문서 링크를 남기되 상세 evidence 정본은 Task 문서에 둔다.
6. live rollout, direct cluster mutation, secret write, external service action은 human approval gate와 rollback trigger를 명시한다.

## Link Basis

이 README의 링크 기준 위치는 `docs/04.execution/plans/`다.

- 같은 폴더의 Plan 문서는 `./`로 시작하는 상대 경로를 사용한다.
- sibling Task stage는 `../tasks/`로 연결한다.
- upstream docs stage는 `../../01.requirements/`, `../../02.architecture/`, `../../03.specs/`처럼 `docs/` 기준으로 올라간다.
- Plan 안의 Task 링크는 `docs/04.execution/plans/`의 최종 Plan 파일 위치 기준으로 다시 계산한다.

## 문서 인덱스

| 문서                                                                                       | 설명                                                                            | 상태  | 최종 수정  |
| ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------- | ----- | ---------- |
| [`./2026-03-27-wsl-k3d-argocd-platform.md`](./2026-03-27-wsl-k3d-argocd-platform.md)         | WSL2 GitOps 플랫폼 단계별 실행 계획                                             | Draft | 2026-05-21 |
| [`./2026-03-28-wsl2-k3d-argocd-ha-platform.md`](./2026-03-28-wsl2-k3d-argocd-ha-platform.md) | TLS/최소권한 유지 + 변경영역 기반 CI 정적 게이트 + 롤백 규칙을 포함한 실행 계획 | Draft | 2026-05-18 |
| [`./2026-03-29-platform-expansion.md`](./2026-03-29-platform-expansion.md)                   | 2026-03-29 IP 수정 + cert-manager/Dashboard/Istio/Kiali 확장 계획, 현재 실행계약은 Headlamp/172.18.x 기준 | Done  | 2026-05-21 |
| [`./2026-05-09-k3d-agent-first-remediation.md`](./2026-05-09-k3d-agent-first-remediation.md) | k3d 운영 문서, Agent-first 실행 계약, 구조적 템플릿 coverage, lifecycle hook hardening 보정 계획 | Done  | 2026-05-22 |
| [`./2026-05-09-scripts-inventory-remediation.md`](./2026-05-09-scripts-inventory-remediation.md) | `scripts/` 인벤토리 조사와 README 실행 계약 보정 계획 | Done  | 2026-05-21 |
| [`./2026-05-09-github-qa-ci-remediation.md`](./2026-05-09-github-qa-ci-remediation.md) | `.github` QA, CI, 브랜치 정책, PR intake 계약 보정 계획 | Done  | 2026-05-09 |
| [`./2026-05-10-agent-first-harness-llm-wiki-hooks.md`](./2026-05-10-agent-first-harness-llm-wiki-hooks.md) | Agent-first harness, LLM Wiki, hook wiring 보정 계획 | Done  | 2026-05-10 |
| [`./2026-05-17-template-crosslink-fix.md`](./2026-05-17-template-crosslink-fix.md) | 문서 템플릿 target-relative 링크와 생성 문서 표시 경로 정합화 완료 이력. Historical exception으로 별도 Task record 없이 plan 내부 evidence와 migration note가 증적을 소유한다. | Done  | 2026-05-21 |
| [`./2026-05-18-argo-rollouts-progressive-delivery.md`](./2026-05-18-argo-rollouts-progressive-delivery.md) | Argo Rollouts current-contract backfill 실행 계획 | Done | 2026-05-21 |
| [`./2026-05-18-argo-notifications-slack.md`](./2026-05-18-argo-notifications-slack.md) | ArgoCD Notifications Slack current-contract backfill 실행 계획 | Done | 2026-05-21 |
| [`./2026-05-22-docs-governance-full-ab-hardening.md`](./2026-05-22-docs-governance-full-ab-hardening.md) | README, lifecycle docs, agent/runtime governance, hook 경계, repo-static gate 정합화 계획 | Done | 2026-05-22 |

## Related Documents

- [Execution README](../README.md)
- [Docs README](../../README.md)
- [03.specs](../../03.specs/README.md)
- [04.execution/tasks](../tasks/README.md)
- [05.operations/policies](../../05.operations/policies/README.md)
- [Plan Template](../../99.templates/plan.template.md)
