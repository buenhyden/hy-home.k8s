---
title: 'Agent-first Harness, LLM Wiki, and Hook Contract Closure Plan'
type: plan
status: done
owner: 'platform'
updated: 2026-05-10
---

# Agent-first Harness, LLM Wiki, and Hook Contract Closure Plan

## Overview (KR)

이 문서는 `hy-home.k8s`의 Harness Engineering, Agent-first Engineering, repo-local LLM Wiki, hook/feedback loop, memory ledger 보강을 재검증하고 닫기 위한 실행 계획서다.
작업 분해, 검증, 위험 관리, 완료 기준을 정의한다.

## Context

현재 저장소는 이미 thin gateway, `.claude` runtime baseline, `.codex` mirrors, local agents/skills, matrix-first harness catalog, generated LLM Wiki index, and scoped hook validation을 갖추고 있다.

이번 작업의 핵심은 새 runtime surface를 더 늘리는 것이 아니라, “이미 완료된 구현을 신뢰할 수 있는지”를 재검증하고 남은 gap, excess, duplication을 최소 보강으로 닫는 것이다.

문서 taxonomy도 기존 13-folder model에서 `01.requirements`, `02.architecture`, `03.specs`, `04.execution`, `05.operations`, `90.references`, `99.templates` 중심의 축소 모델로 hard-migrated 상태다. 남은 보강은 legacy path mapping을 governance rule과 repo quality gate가 함께 설명하고 검증하도록 만드는 것이다.

## Goals & In-Scope

- **Goals**:
  - Harness Engineering과 Agent-first Engineering readiness를 현재 repo evidence로 재확인한다.
  - Guardrails/Rules, Hooks/Feedback Loop, Memory, LLM Wiki curation surface가 실제 agent runtime에서 찾을 수 있게 한다.
  - Legacy docs path가 다시 생기거나 문서 라우팅이 옛 모델로 회귀하지 않도록 한다.
  - Plan/Task/README 인덱스에 2026-05-10 보강 증거를 남긴다.
- **In Scope**:
  - `docs/00.agent-governance/rules/document-stage-routing.md`
  - `.claude/CLAUDE.md`
  - Root `README.md`
  - `docs/04.execution/plans/README.md`
  - `docs/04.execution/tasks/README.md`
  - `scripts/validate-repo-quality-gates.sh`
  - Current hook, LLM Wiki, memory, and harness catalog validation

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - 새 Kubernetes manifest, cluster mutation, or live ArgoCD reconciliation
  - 새 provider-native instruction layer
  - 새 agent/skill 추가 beyond the existing `wiki-curator`
  - Vector store, retrieval service, static wiki site, or cache runtime for LLM Wiki
- **Out of Scope**:
  - Cloud example version changes
  - External Vault/PostgreSQL/Valkey runtime changes
  - Rewriting unrelated authored SSoT documents

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | Reconfirm harness and Agent-first readiness from current repo evidence | `docs/00.agent-governance/harness-catalog.md`, `.claude/**`, `.codex/**` | REQ-AI-001 | repo quality gate PASS |
| PLN-002 | Keep LLM Wiki as generated Markdown owner map with a real `wiki-curator` role | `.claude/agents/wiki-curator.md`, `.codex/agents/wiki-curator.toml`, `docs/90.references/llm-wiki/**`, `scripts/generate-llm-wiki-index.sh` | REQ-AI-002 | generated index check PASS |
| PLN-003 | Wire hook feedback loops through Claude implementations and Codex event wiring | `.claude/hooks/*.sh`, `.claude/settings.json`, `.codex/hooks.json` | REQ-AI-003 | JSON, shell, payload simulation PASS |
| PLN-004 | Record reduced docs taxonomy and legacy path mapping | `document-stage-routing.md`, `docs/README.md`, validator | REQ-DOC-001 | old folder and mapping guard PASS |
| PLN-005 | Add plan/task evidence and update README indexes | `docs/04.execution/plans/`, `docs/04.execution/tasks/` | REQ-DOC-002 | template heading checks PASS |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Static | Generated LLM Wiki freshness | `bash scripts/generate-llm-wiki-index.sh --check` | PASS |
| VAL-PLN-002 | Static | Runtime JSON parse | `python3 -m json.tool .claude/settings.json` and `python3 -m json.tool .codex/hooks.json` | PASS |
| VAL-PLN-003 | Static | Hook and script syntax | `bash -n .claude/hooks/k8s-pre-edit.sh .claude/hooks/post-validate.sh .claude/hooks/session-start.sh scripts/validate-repo-quality-gates.sh scripts/generate-llm-wiki-index.sh` | no syntax errors |
| VAL-PLN-004 | Structural | Repo quality gate | `bash scripts/validate-repo-quality-gates.sh .` | PASS |
| VAL-PLN-005 | Static | Legacy docs path scan | `rg -n "docs/(01\\.prd\|02\\.ard\|03\\.adr\|04\\.specs\|05\\.plans\|06\\.tasks\|07\\.guides\|08\\.operations\|09\\.runbooks\|10\\.incidents)" docs .claude .codex AGENTS.md CLAUDE.md GEMINI.md README.md` | only validator sentinel or migration-map context |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Overbuilding new runtime surfaces when matrices already show `Ready` | Medium | Use the matrix-first rule and close gaps in existing files only |
| Treating LLM Wiki as a policy source | High | Keep `wiki-index.md` generated and route policy/procedure to canonical owners |
| Codex hooks being mistaken for Claude-equivalent permission gates | Medium | Document Codex hooks as context/validation wiring only |
| Legacy docs folders reappearing | Medium | Keep explicit migration map and validator checks |
| Validation evidence aging | Medium | Record commands as a dated snapshot and require rerun before future handoff |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: repo quality gate and generated index freshness check must pass.
- **Sandbox / Canary Rollout**: not applicable; no cluster rollout is included.
- **Human Approval Gate**: required for any direct cluster mutation or new runtime surface beyond this plan.
- **Rollback Trigger**: revert only this docs/runtime-governance change set if validation fails.
- **Prompt / Model Promotion Criteria**: not applicable; no model change is planned.

## Completion Criteria

- [x] Existing harness and Agent-first surfaces reviewed against current repo evidence
- [x] LLM Wiki remains generated, Markdown-only, and tied to `wiki-curator`
- [x] Hook feedback loop validates JSON, shell, manifest, secret, and repo-quality paths
- [x] Legacy docs path mapping is explicit and validator-backed
- [x] Plan/task evidence and README indexes updated
- [x] Required validation passed

## Related Documents

- **Governance**: [Harness Catalog](../../00.agent-governance/harness-catalog.md)
- **Governance**: [Agentic Execution Rules](../../00.agent-governance/rules/agentic.md)
- **Governance**: [Document Stage Routing Rules](../../00.agent-governance/rules/document-stage-routing.md)
- **Reference**: [LLM WIKI Reference Index](../../90.references/llm-wiki/README.md)
- **Task**: [Task: Agent-first Harness, LLM Wiki, and Hook Contract Closure](../tasks/2026-05-10-agent-first-harness-llm-wiki-hooks.md)
