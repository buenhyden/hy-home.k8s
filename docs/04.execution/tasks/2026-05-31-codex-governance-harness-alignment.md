---
title: 'Task: Codex Governance Harness Alignment'
type: sdlc/task
status: done
owner: platform
updated: 2026-07-13
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

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Write the Phase 3 Task record and Task README index | doc | N/A | PLN-001 | Task file and `docs/04.execution/tasks/README.md` updated | platform | Done |
| T-002 | Align the Stage 00 Model Policy and harness catalog | doc | N/A | PLN-002 | Targeted model checks and repo quality gate | platform | Done |
| T-003 | Declare Codex agent TOML model reasoning effort | guardrail | N/A | PLN-003 | `rg -n "model_reasoning_effort" .codex/agents` | platform | Done |
| T-004 | Clarify the `AGENTS.md` Codex/GPT shim role and provider docs | doc | N/A | PLN-004 | Link check and repo quality gate | platform | Done |
| T-005 | Normalize shared hook script path references | doc | N/A | PLN-005 | No stale provider-local runtime-script claims remain in active Codex/Gemini docs | platform | Done |
| T-006 | Normalize policy template routing to `policy.template.md` | doc | N/A | PLN-006 | No active `deprecated operations-template route` routing references remain | platform | Done |
| T-007 | Normalize operations policy frontmatter to `type: sdlc/policy` | doc | N/A | PLN-007 | `rg -n "^type: operation$" docs/05.operations/policies` has no output | platform | Done |
| T-008 | Harden repo quality gates against recurring drift | test | N/A | PLN-008 | `bash scripts/validate-repo-quality-gates.sh .` | platform | Done |
| T-009 | Update README indexes and the memory ledger | memory | N/A | PLN-009 | README indexes current; progress entry appended | platform | Done |
| T-010 | Run final verification and record results | test | N/A | PLN-010 | Verification Summary commands pass or limitations recorded | platform | Done |

### Phase View

### Phase 3

- [x] T-001 Write the Phase 3 Task record and Task README index.
- [x] T-002 Align the Stage 00 Model Policy and harness catalog.
- [x] T-003 Declare Codex agent TOML model reasoning effort.
- [x] T-004 Clarify the `AGENTS.md` Codex/GPT shim role and provider docs.
- [x] T-005 Normalize shared hook script path references.
- [x] T-006 Normalize policy template routing to `policy.template.md`.
- [x] T-007 Normalize operations policy frontmatter to `type: sdlc/policy`.
- [x] T-008 Harden repo quality gates against recurring drift.
- [x] T-009 Update README indexes and the memory ledger.
- [x] T-010 Run final verification and record results.

## Approval and Safety Boundaries

- **Allowed Paths**: `T-001 through T-010` is limited to these Codex Governance Harness Alignment owners and Task-Table surfaces:
  - `docs/04.execution/tasks/2026-05-31-codex-governance-harness-alignment.md`
  - `docs/04.execution/plans/2026-05-31-codex-governance-harness-alignment.md`
  - `docs/04.execution/tasks/README.md`
- **Forbidden Paths**: provider account settings, live agent sessions, credentials, model/runtime policy outside the parent Plan, and repository paths outside the Codex Governance Harness Alignment surfaces.
- **Approval Required**: Human approval is required before Codex Governance Harness Alignment provider configuration, model-policy promotion, remote agent action, credential access, protected-file expansion, push, merge, or publication.
- **Static Validation**: Preserve the Codex Governance Harness Alignment outcomes and limitations recorded in Verification Summary; use these recorded checks:
  - `bash scripts/validate-repo-quality-gates.sh .`
  - `bash scripts/generate-llm-wiki-index.sh --check`
  - `bash -n docs/00.agent-governance/hooks/k8s-pre-edit.sh scripts/validate-repo-quality-gates.sh`
  - `git diff --check`
- **Live Validation**: DEFER — Codex Governance Harness Alignment is closed by repository-static/documentation evidence; historical live commands, if any, are not authority for a new cluster, provider, external-service, or deployment claim.
- **Secret / Vault Handling**: Use only redacted repository contracts for Codex Governance Harness Alignment; do not read or print provider tokens, auth files, memory stores, private logs, kubeconfigs, secret values, or shell history.
- **Rollback Plan**: Revert the logical Codex Governance Harness Alignment change set for `T-001 through T-010` and restore its allowed implementation/evidence paths with this Task and parent Plan; documentation rollback does not authorize live mutation.
- **Evidence Location**: Durable Codex Governance Harness Alignment evidence remains in:
  - `docs/04.execution/tasks/2026-05-31-codex-governance-harness-alignment.md`
  - `docs/04.execution/plans/2026-05-31-codex-governance-harness-alignment.md`
  - `docs/00.agent-governance/memory/progress.md`

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

## Traceability

- **Plan**: [../plans/2026-05-31-codex-governance-harness-alignment.md](../plans/2026-05-31-codex-governance-harness-alignment.md)
- **Model Policy**: [../../00.agent-governance/model-policy.md](../../00.agent-governance/model-policy.md)
- **Harness Catalog**: [../../00.agent-governance/harness-catalog.md](../../00.agent-governance/harness-catalog.md)
- **Codex Runtime Baseline**: [../../../.codex/CODEX.md](../../../.codex/CODEX.md)
