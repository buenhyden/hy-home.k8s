# 04.execution/tasks

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
└── README.md
```

## How to Work in This Area

1. 작업의 Parent Spec 또는 Parent Plan을 먼저 확인한다.
2. 새 Task 문서는 `../../99.templates/task.template.md`에서 시작한다.
3. 각 작업은 Task ID, Type, Parent Spec/Plan, Validation/Evidence, Owner, Status를 가진다.
4. 권장 Type은 `impl`, `test`, `eval`, `doc`, `ops`다. Agent-specific 작업은 `prompt`, `tool`, `memory`, `guardrail`, `eval`, `observability`를 사용할 수 있다.
5. 핵심 동작은 테스트 우선(TDD)을 기본값으로 하고, 문서-only 작업도 검증 evidence를 남긴다.
6. 기능 수준의 보조 `tasks.md`가 `../../03.specs/<feature-id>/`에 있더라도, 팀 실행·스프린트·검증 집계의 정본은 이 경로다.

## Link Basis

Stage README files: links start from the owning stage folder (`docs/04.execution/tasks/`).

- 같은 폴더의 Task 문서는 `./`로 시작하는 상대 경로를 사용한다.
- sibling Plan stage는 `../plans/`로 연결한다.
- upstream docs stage는 `../../03.specs/`, `../../02.architecture/`, `../../01.requirements/`처럼 `docs/` 기준으로 올라간다.

## 문서 인덱스

| 문서                                                                                       | 설명                                                                                 | 상태  | 최종 수정  |
| ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------ | ----- | ---------- |
| [`./2026-03-27-wsl-k3d-argocd-platform.md`](./2026-03-27-wsl-k3d-argocd-platform.md)         | TDD/검증 중심 실행 Task 목록과 증적 기준                                             | Draft | 2026-03-27 |
| [`./2026-03-28-wsl2-k3d-argocd-ha-platform.md`](./2026-03-28-wsl2-k3d-argocd-ha-platform.md) | RED/GREEN/REFACTOR 기반 TLS/Ingress + CI static contract/workflow-security 작업 Task | Draft | 2026-03-28 |
| [`./2026-03-29-platform-expansion.md`](./2026-03-29-platform-expansion.md)                   | 2026-03-29 IP 수정 + cert-manager/Dashboard/Istio/Kiali 확장 Task, 현재 실행계약은 Headlamp/172.18.x 기준 | Done  | 2026-05-09 |
| [`./2026-05-09-k3d-agent-first-remediation.md`](./2026-05-09-k3d-agent-first-remediation.md) | k3d 운영 문서와 Agent-first 실행 계약의 GitOps-first 충돌 보정 Task | Done  | 2026-05-09 |
| [`./2026-05-09-scripts-inventory-remediation.md`](./2026-05-09-scripts-inventory-remediation.md) | `scripts/` 인벤토리 조사와 README 실행 계약 보정 Task | Done  | 2026-05-09 |
| [`./2026-05-09-github-qa-ci-remediation.md`](./2026-05-09-github-qa-ci-remediation.md) | `.github` QA, CI, 브랜치 정책, PR intake 계약 보정 Task | Done  | 2026-05-09 |
| [`./2026-05-10-agent-first-harness-llm-wiki-hooks.md`](./2026-05-10-agent-first-harness-llm-wiki-hooks.md) | Agent-first harness, LLM Wiki, hook 계약 보정 Task | Done | 2026-05-10 |
| [`./2026-05-18-argo-rollouts-progressive-delivery.md`](./2026-05-18-argo-rollouts-progressive-delivery.md) | Argo Rollouts current-contract backfill Task | Done | 2026-05-18 |
| [`./2026-05-18-argo-notifications-slack.md`](./2026-05-18-argo-notifications-slack.md) | ArgoCD Notifications Slack current-contract backfill Task | Done | 2026-05-18 |

## Related Documents

- [Execution README](../README.md)
- [Docs README](../../README.md)
- [03.specs](../../03.specs/README.md)
- [04.execution/plans](../plans/README.md)
- [05.operations/incidents](../../05.operations/incidents/README.md)
- [Task Template](../../99.templates/task.template.md)
