---
title: 'Workspace Purpose Alignment Audit Plan'
type: plan
status: done
owner: 'platform'
updated: 2026-05-22
---

# Workspace Purpose Alignment Audit Plan

## Overview (KR)

이 문서는 `hy-home.k8s`가 WSL2 native Docker, k3d, ArgoCD GitOps, External Secrets/Vault,
외부 PostgreSQL/Valkey 계약, SDD 문서 생명주기, AI Agent governance를 실제로 지탱하는지
전면 재감사하고 확인된 격차만 보강하기 위한 실행 계획서다.

## Context

이전 `docs governance Full A+B hardening` 작업으로 README 구조, lifecycle 문서 템플릿,
Agent runtime mirror, Hookify local boundary, repo quality gate는 이미 정리되어 있었다.
이번 작업은 그 결과를 다시 기준선으로 삼되, 범위를 문서와 Agent 규칙에 한정하지 않고
GitOps, 인프라 계약, CI, 검증 스크립트, 예제, 외부 버전 기준까지 전체 목적과 대조한다.

기준선 감사에서 repo quality, LLM Wiki freshness, GitOps structure, static infrastructure
contract 검증은 통과했다. 확인된 보강 대상은 외부 버전 인벤토리 freshness와 live command
deny 경계의 명시성이다.

## Goals & In-Scope

- **Goals**:
  - docs lifecycle, templates, README, Agent governance, hooks, CI, GitOps, infra contracts를 워크스페이스 목적 기준으로 재감사한다.
  - 확인된 drift만 작게 수정하고 기존 SSoT 구조를 유지한다.
  - 외부 버전 snapshot의 검토일과 공식 기준을 2026-05-22 기준으로 갱신한다.
  - Claude/Hookify command boundary가 direct cluster mutation과 direct reconciliation을 더 명확히 차단하도록 보강한다.
- **In Scope**:
  - `docs/01.requirements` through `docs/05.operations`
  - `docs/90.references/versions`
  - `docs/99.templates`
  - `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.claude/**`, `.codex/**`
  - root, docs, GitOps, infrastructure, scripts, tests, examples README layers
  - repository validation scripts and static CI contracts

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - live k3d bootstrap, ArgoCD sync, Vault write, PostgreSQL/Valkey runtime mutation
  - Kubernetes manifest desired-state contract 변경
  - cloud example version target 자동 업그레이드
  - historical PRD/ARD/Spec/Plan/Task 의미 재작성
- **Out of Scope**:
  - AWS/Azure 실제 계정 배포
  - plaintext Kubernetes secret authoring
  - new top-level documentation tree
  - new shared runtime surface without a concrete matrix gap

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | Capture full-purpose audit plan and execution evidence | `docs/04.execution/plans`, `docs/04.execution/tasks` | REQ-SDD-001 | Plan/Task follow templates and are indexed |
| PLN-002 | Re-audit docs lifecycle, templates, and README layer | `docs/01.requirements` through `docs/05.operations`, `docs/99.templates`, `**/README.md` | REQ-DOC-001 | Repo quality gate passes with no template drift |
| PLN-003 | Re-audit Agent governance and runtime boundaries | `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.claude/**`, `.codex/**`, `docs/00.agent-governance/**` | REQ-AI-001 | Gateway thinness, mirror, hook, and local-rule checks pass |
| PLN-004 | Refresh external version basis without changing desired-state pins | `docs/90.references/versions/tech-stack-version-inventory.md` | REQ-REF-001 | Official source date and snapshot notes reflect 2026-05-22 |
| PLN-005 | Harden shared and local advisory command boundaries | `.claude/settings.json`, `.claude/*.local.md` | REQ-HOOK-001 | JSON parse and quality gate pass; local rules remain ignored |
| PLN-006 | Record memory and validation handoff | `docs/00.agent-governance/memory/progress.md` | REQ-MEM-001 | Progress entry includes evidence and limitations |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Structural | Repository governance and docs quality gate | `bash scripts/validate-repo-quality-gates.sh .` | PASS |
| VAL-PLN-002 | Static | LLM Wiki generated index freshness | `bash scripts/generate-llm-wiki-index.sh --check` | PASS |
| VAL-PLN-003 | Static | GitOps structure | `bash scripts/validate-gitops-structure.sh` | PASS |
| VAL-PLN-004 | Static | Kubernetes manifests and optional kube-linter | `bash scripts/validate-k8s-manifests.sh .` | PASS, with optional-tool skip reported if applicable |
| VAL-PLN-005 | Static | Secret handling | `bash scripts/check-secret-handling.sh .` | PASS |
| VAL-PLN-006 | Static | Static infrastructure contracts | `bash infrastructure/tests/verify-contracts-static.sh` | PASS |
| VAL-PLN-007 | Static | Runtime hook JSON parse | `python3 -m json.tool .claude/settings.json` and `python3 -m json.tool .codex/hooks.json` | PASS |
| VAL-PLN-008 | Static | Shell syntax | `find infrastructure scripts .claude/hooks -type f -name '*.sh' -exec bash -n {} +` | PASS |
| VAL-PLN-009 | Static | Diff whitespace sanity | `git diff --check` | PASS |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Full audit becomes broad rewrite | High | Modify only evidence-backed drift and preserve current SSoT layout |
| External latest versions are mistaken for upgrade instructions | Medium | Refresh reference snapshot only; keep desired-state pins unchanged |
| Local Hookify rules are mistaken for shared enforcement | Medium | Keep `.claude/*.local.md` ignored and document shared enforcement in tracked settings/hooks/validators |
| Optional local tools are treated as passed when absent | Medium | Report absent tools as limitations and rely on repo-backed gates plus CI |
| Direct live mutation is normalized by examples | High | Keep direct commands behind human-approved bootstrap or break-glass boundaries |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: repo-static validation commands in this plan must pass.
- **Sandbox / Canary Rollout**: not applicable; no live runtime rollout is included.
- **Human Approval Gate**: required for any direct cluster mutation, ArgoCD forced sync, Vault write, cloud account change, or version pin upgrade outside this plan.
- **Rollback Trigger**: revert this documentation/governance change set if repo quality, static contracts, or JSON parse cannot be restored.
- **Prompt / Model Promotion Criteria**: not applicable; no model or prompt promotion is included.

## Completion Criteria

- [x] Docs lifecycle, templates, README layer, Agent governance, hooks, GitOps, infra contracts, CI, examples, and version references were audited against the workspace purpose.
- [x] External version inventory was refreshed without changing desired-state manifests or cloud example targets.
- [x] Claude direct-command deny boundary and local Hookify advisory wording were aligned.
- [x] Plan/Task evidence and progress memory were updated.
- [x] Verification commands passed or skipped optional tools were reported.

## Related Documents

- **Task**: [../tasks/2026-05-22-workspace-purpose-alignment.md](../tasks/2026-05-22-workspace-purpose-alignment.md)
- **Previous Plan**: [./2026-05-22-docs-governance-full-ab-hardening.md](./2026-05-22-docs-governance-full-ab-hardening.md)
- **Templates**: [../../99.templates/README.md](../../99.templates/README.md)
- **Harness Catalog**: [../../00.agent-governance/harness-catalog.md](../../00.agent-governance/harness-catalog.md)
- **Agentic Rules**: [../../00.agent-governance/rules/agentic.md](../../00.agent-governance/rules/agentic.md)
- **Version Inventory**: [../../90.references/versions/tech-stack-version-inventory.md](../../90.references/versions/tech-stack-version-inventory.md)
