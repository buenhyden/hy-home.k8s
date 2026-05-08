---
title: 'k3d Workspace and Agent-first Remediation Implementation Plan'
type: plan
status: done
owner: 'platform'
updated: 2026-05-09
---

<!-- Target: docs/05.plans/YYYY-MM-DD-<feature>.md -->

# k3d Workspace and Agent-first Remediation Implementation Plan

> Use this template for `docs/05.plans/YYYY-MM-DD-<feature>.md`.
>
> Rules:
>
> - Every active plan must include explicit verification criteria.
> - Plan explains execution order, risk control, and rollout strategy.

---

# k3d Workspace and Agent-first Remediation Plan

## Overview (KR)

이 문서는 `hy-home.k8s`의 k3d 운영 문서와 Agent-first 실행 계약을 보정하기 위한 실행 계획서다.
작업 분해, 검증, 롤아웃, 위험 관리, 완료 기준을 정의한다.

## Context

현재 저장소는 k3d/k3s, ArgoCD App-of-Apps, ESO/Vault, 외부 PostgreSQL/Valkey/Observability 계약, Headlamp, Istio/Kiali, Rollouts, CI/pre-commit, `.claude`/`.codex` 하네스를 갖추고 있다.

문서 taxonomy도 `docs/01.prd`부터 `docs/10.incidents`, `docs/90.references`, `docs/99.templates`까지 정리되어 있어 k3d 운영과 Agent-first 협업에 적절하다. 남은 문제는 구조 부족이 아니라 일부 가이드/운영/런북 문서에서 직접 `kubectl apply`/`kubectl patch` 절차가 기본 경로처럼 보이는 점과, 하네스 readiness를 한눈에 확인하기 어렵다는 점이다.

2026-05-09 추가 audit 결과, `AGENTS.md`, root `CLAUDE.md`, `GEMINI.md`, `.claude/CLAUDE.md`, local agents/skills, `.codex` mirrors, `docs/00.agent-governance/**`는 thin gateway, JIT governance, GitOps-first, mirror validation 구조를 이미 갖추고 있다. 따라서 추가 보정은 새 runtime surface 생성이 아니라 current catalog clarity와 regression gate 강화로 제한한다.

## Goals & In-Scope

- **Goals**:
  - GitOps-first 원칙과 직접 cluster mutation 절차의 충돌을 줄인다.
  - Agent 실행 경로에서 직접 cluster mutation이 기본값이 아님을 명확히 한다.
  - 역사적 Dashboard/`172.19.x` 문맥과 현재 Headlamp/`172.18.x` 실행 계약을 분리한다.
  - 하네스와 Agent-first Engineering 구현 상태를 readiness matrix로 정리한다.
- **In Scope**:
  - `docs/05.plans`, `docs/06.tasks` 보정 작업 추적 문서 추가
  - `docs/07.guides`, `docs/08.operations`, `docs/09.runbooks`의 안전 경계 문구 보정
  - `docs/00.agent-governance/harness-catalog.md` 및 Agent-first 규칙 보강
  - 각 stage README 인덱스 갱신

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - docs taxonomy 축소 또는 stage 폴더 삭제
  - 새 Kubernetes manifest 추가 또는 기존 manifest 계약 변경
  - live cluster 검증 또는 직접 cluster mutation 수행
  - GitHub-native instruction 계층 추가
- **Out of Scope**:
  - 외부 Vault/PostgreSQL/Valkey/Observability 런타임 변경
  - `.claude`/`.codex` 에이전트 roster 변경
  - PRD/ARD/ADR/Spec 신규 작성

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | 보정 작업 plan/task 문서 추가 및 README 인덱스 갱신 | `docs/05.plans/`, `docs/06.tasks/` | REQ-DOC-001 | repo quality gate PASS |
| PLN-002 | 직접 cluster mutation 절차를 human-approved bootstrap/break-glass 경로로 격리 | `docs/07.guides/`, `docs/08.operations/`, `docs/09.runbooks/` | REQ-OPS-001 | `kubectl apply/patch` 문맥 검토 |
| PLN-003 | Dashboard/`172.19.x` 역사적 문맥과 현재 Headlamp/`172.18.x` 계약 분리 강화 | `docs/01-09` 관련 문서 중 보정 대상 | REQ-DOC-002 | stale contract gate PASS |
| PLN-004 | 하네스 readiness matrix와 Agent-first execution boundary 보강 | `docs/00.agent-governance/` | REQ-AI-001 | harness catalog mirror gate PASS |
| PLN-005 | 최소 정적 검증 묶음 실행 | `scripts/`, `infrastructure/tests/` | REQ-VAL-001 | 모든 repo-backed command PASS 또는 제한 명시 |
| PLN-006 | gateway/runtime audit 결과를 반영해 hook boundary와 historical memory current-source 문맥 보강 | `docs/00.agent-governance/` | REQ-AI-002 | repo quality gate PASS |
| PLN-007 | root shim thinness, governance/runtime English-only, hook-boundary clarity를 repo quality gate로 고정 | `scripts/validate-repo-quality-gates.sh` | REQ-VAL-002 | regression checks PASS |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Structural | repo governance quality gate | `bash scripts/validate-repo-quality-gates.sh .` | PASS |
| VAL-PLN-002 | Static | k3d/GitOps static contracts | `bash infrastructure/tests/verify-contracts-static.sh` | PASS |
| VAL-PLN-003 | Static | GitOps structure | `bash scripts/validate-gitops-structure.sh` | PASS |
| VAL-PLN-004 | Static | YAML syntax and optional kube-linter | `bash scripts/validate-k8s-manifests.sh .` | PASS or tool limitation stated |
| VAL-PLN-005 | Security | plaintext secret scan | `bash scripts/check-secret-handling.sh .` | PASS |
| VAL-PLN-006 | Static | shell syntax | `find infrastructure scripts .claude/hooks -type f -name '*.sh' -exec bash -n {} +` | no syntax errors |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Direct mutation guidance remains ambiguous | High | Mark direct `kubectl apply/patch` paths as human-approved bootstrap/break-glass only |
| Historical docs are mistaken for current runtime contract | Medium | Keep historical content but add current-contract notes pointing to Headlamp and `172.18.x` manifests |
| Documentation remediation expands into manifest changes | Medium | Keep Kubernetes manifests explicitly out of scope |
| New documents drift from templates | Medium | Start from `plan.template.md` and `task.template.md`; update stage README indexes |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: repo-backed validators must pass before handoff.
- **Sandbox / Canary Rollout**: not applicable; no live rollout or manifest change is planned.
- **Human Approval Gate**: direct cluster mutation, live cluster verification beyond read-only checks, and external runtime changes require explicit human approval.
- **Rollback Trigger**: revert only this documentation/governance change set if validation fails or safety language conflicts with existing governance.
- **Prompt / Model Promotion Criteria**: not applicable; no model or prompt roster change is planned.

## Completion Criteria

- [x] Scoped documentation and governance remediation completed
- [x] Stage README indexes updated
- [x] GitOps-first direct mutation boundaries clarified
- [x] Harness readiness matrix added
- [x] Gateway/runtime audit results reflected without adding new runtime surfaces
- [x] Regression gates cover gateway thinness, language boundaries, historical memory, and hook-boundary clarity
- [x] Required verification passed or limitations documented

## Related Documents

- **Governance**: [`../00.agent-governance/harness-catalog.md`](../00.agent-governance/harness-catalog.md)
- **Agent-first Rules**: [`../00.agent-governance/rules/agentic.md`](../00.agent-governance/rules/agentic.md)
- **Document Routing**: [`../00.agent-governance/rules/document-stage-routing.md`](../00.agent-governance/rules/document-stage-routing.md)
- **Task**: [`../06.tasks/2026-05-09-k3d-agent-first-remediation.md`](../06.tasks/2026-05-09-k3d-agent-first-remediation.md)
