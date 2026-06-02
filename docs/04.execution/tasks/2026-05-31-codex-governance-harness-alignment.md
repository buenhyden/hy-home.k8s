---
title: 'Task: Codex Governance Harness Alignment'
type: task
status: done
owner: platform
updated: 2026-05-31
---

# Task: Codex Governance Harness Alignment

---

## Overview (KR)

이 문서는 Codex/GPT 하네스, Stage 00 Model Policy, Template Contract drift 정합화 작업의 구현·검증 증적을 기록한다.
작업은 승인된 Phase 3 범위 안에서만 수행하며, live cluster mutation이나 secret value 접근은 포함하지 않는다.

## Inputs

- **Parent Plan**: [../plans/2026-05-31-codex-governance-harness-alignment.md](../plans/2026-05-31-codex-governance-harness-alignment.md)

## Working Rules

- 승인된 Plan의 `PLN-001`부터 `PLN-010` 범위만 구현한다.
- Governance와 provider/harness 문서는 English로 유지한다.
- Human-facing README와 Task/Plan 개요는 Korean을 유지한다.
- Kubernetes manifests, ArgoCD live sync, Vault writes, secret value inspection은 수행하지 않는다.
- 문서-only 변경도 validation evidence를 남긴다.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Phase 3 Task record and Task README index 작성 | doc | N/A | PLN-001 | Task file and `docs/04.execution/tasks/README.md` updated | platform | Done |
| T-002 | Stage 00 Model Policy and harness catalog 정합화 | doc | N/A | PLN-002 | Targeted model checks and repo quality gate | platform | Done |
| T-003 | Codex agent TOML model reasoning effort 명시 | guardrail | N/A | PLN-003 | `rg -n "model_reasoning_effort" .codex/agents` | platform | Done |
| T-004 | `AGENTS.md` Codex/GPT shim 역할과 provider docs 정리 | doc | N/A | PLN-004 | Link check and repo quality gate | platform | Done |
| T-005 | Shared hook script path references 정규화 | doc | N/A | PLN-005 | No stale provider-local runtime-script claims remain in active Codex/Gemini docs | platform | Done |
| T-006 | Policy template routing을 `policy.template.md`로 정규화 | doc | N/A | PLN-006 | No active `operation.template.md` routing references remain | platform | Done |
| T-007 | Operations policy frontmatter `type: policy` 정규화 | doc | N/A | PLN-007 | `rg -n "^type: operation$" docs/05.operations/policies` has no output | platform | Done |
| T-008 | Recurring drift를 repo quality gate로 보강 | test | N/A | PLN-008 | `bash scripts/validate-repo-quality-gates.sh .` | platform | Done |
| T-009 | README indexes and memory ledger 갱신 | memory | N/A | PLN-009 | README indexes current; progress entry appended | platform | Done |
| T-010 | 최종 검증 실행과 결과 기록 | test | N/A | PLN-010 | Verification Summary commands pass or limitations recorded | platform | Done |

## Suggested Types

- `doc`
- `test`
- `guardrail`
- `memory`

## Agent-specific Types (If Applicable)

- `tool`
- `guardrail`
- `memory`

## Phase View (Optional)

### Phase 3

- [x] T-001 Phase 3 Task record and Task README index 작성
- [x] T-002 Stage 00 Model Policy and harness catalog 정합화
- [x] T-003 Codex agent TOML model reasoning effort 명시
- [x] T-004 `AGENTS.md` Codex/GPT shim 역할과 provider docs 정리
- [x] T-005 Shared hook script path references 정규화
- [x] T-006 Policy template routing을 `policy.template.md`로 정규화
- [x] T-007 Operations policy frontmatter `type: policy` 정규화
- [x] T-008 Recurring drift를 repo quality gate로 보강
- [x] T-009 README indexes and memory ledger 갱신
- [x] T-010 최종 검증 실행과 결과 기록

## Verification Summary

- **Test Commands**:
  - `bash scripts/validate-repo-quality-gates.sh .` — PASS
  - `bash scripts/generate-llm-wiki-index.sh --check` — PASS
  - `bash -n docs/00.agent-governance/hooks/k8s-pre-edit.sh scripts/validate-repo-quality-gates.sh` — PASS
  - `git diff --check` — PASS
- **Eval Commands**:
  - `bash scripts/validate-repo-quality-gates.sh .`
  - `bash scripts/generate-llm-wiki-index.sh --check`
  - `rg -n "GPT-5.4-mini|gpt-5.4-mini" docs/00.agent-governance .codex AGENTS.md -g '!docs/00.agent-governance/memory/**'`
  - `rg -n "model_reasoning_effort" .codex/agents`
  - `rg -n "^type: operation$" docs/05.operations/policies`
  - `rg -n "operation\\.template\\.md" .agents docs/00.agent-governance .codex`
  - `bash -n docs/00.agent-governance/hooks/k8s-pre-edit.sh scripts/validate-repo-quality-gates.sh`
  - `git diff --check`
- **Logs / Evidence Location**: This task document and `docs/00.agent-governance/memory/progress.md`.

## Related Documents

- **Plan**: [../plans/2026-05-31-codex-governance-harness-alignment.md](../plans/2026-05-31-codex-governance-harness-alignment.md)
- **Model Policy**: [../../00.agent-governance/model-policy.md](../../00.agent-governance/model-policy.md)
- **Harness Catalog**: [../../00.agent-governance/harness-catalog.md](../../00.agent-governance/harness-catalog.md)
- **Codex Runtime Baseline**: [../../../.codex/CODEX.md](../../../.codex/CODEX.md)
