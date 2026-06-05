---
title: 'Task: Codex Governance Harness Alignment'
type: task
status: done
owner: platform
updated: 2026-05-31
---

# Task: Codex Governance Harness Alignment

---

## Overview

This document records implementation and verification evidence for aligning
the Codex/GPT harness, Stage 00 Model Policy, and Template Contract drift. The
work is limited to the approved Phase 3 scope and does not include live cluster
mutation or secret-value access.

## Inputs

- **Parent Plan**: [../plans/2026-05-31-codex-governance-harness-alignment.md](../plans/2026-05-31-codex-governance-harness-alignment.md)

## Working Rules

- Implement only the approved Plan scope from `PLN-001` through `PLN-010`.
- Keep governance and provider/harness documents in English.
- Keep human-facing README files in Korean; Stage 04 Plan and Task records are now English-first under the language policy.
- Do not perform Kubernetes manifest changes, ArgoCD live sync, Vault writes, or secret-value inspection.
- Documentation-only changes still need validation evidence.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Write the Phase 3 Task record and Task README index | doc | N/A | PLN-001 | Task file and `docs/04.execution/tasks/README.md` updated | platform | Done |
| T-002 | Align the Stage 00 Model Policy and harness catalog | doc | N/A | PLN-002 | Targeted model checks and repo quality gate | platform | Done |
| T-003 | Declare Codex agent TOML model reasoning effort | guardrail | N/A | PLN-003 | `rg -n "model_reasoning_effort" .codex/agents` | platform | Done |
| T-004 | Clarify the `AGENTS.md` Codex/GPT shim role and provider docs | doc | N/A | PLN-004 | Link check and repo quality gate | platform | Done |
| T-005 | Normalize shared hook script path references | doc | N/A | PLN-005 | No stale provider-local runtime-script claims remain in active Codex/Gemini docs | platform | Done |
| T-006 | Normalize policy template routing to `policy.template.md` | doc | N/A | PLN-006 | No active `operation.template.md` routing references remain | platform | Done |
| T-007 | Normalize operations policy frontmatter to `type: policy` | doc | N/A | PLN-007 | `rg -n "^type: operation$" docs/05.operations/policies` has no output | platform | Done |
| T-008 | Harden repo quality gates against recurring drift | test | N/A | PLN-008 | `bash scripts/validate-repo-quality-gates.sh .` | platform | Done |
| T-009 | Update README indexes and the memory ledger | memory | N/A | PLN-009 | README indexes current; progress entry appended | platform | Done |
| T-010 | Run final verification and record results | test | N/A | PLN-010 | Verification Summary commands pass or limitations recorded | platform | Done |

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

- [x] T-001 Write the Phase 3 Task record and Task README index.
- [x] T-002 Align the Stage 00 Model Policy and harness catalog.
- [x] T-003 Declare Codex agent TOML model reasoning effort.
- [x] T-004 Clarify the `AGENTS.md` Codex/GPT shim role and provider docs.
- [x] T-005 Normalize shared hook script path references.
- [x] T-006 Normalize policy template routing to `policy.template.md`.
- [x] T-007 Normalize operations policy frontmatter to `type: policy`.
- [x] T-008 Harden repo quality gates against recurring drift.
- [x] T-009 Update README indexes and the memory ledger.
- [x] T-010 Run final verification and record results.

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
