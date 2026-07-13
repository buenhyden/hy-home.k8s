---
title: 'Task: Harness Four-Element Alignment'
type: sdlc/task
status: done
owner: platform
updated: 2026-07-13
---

# Task: Harness Four-Element Alignment

## Overview

This document tracks the current workspace implementation state of the four
harness elements through the Codex and Claude provider surfaces. It records
evidence for hardening the shared catalog, runtime baseline, audit skills, and
validation gates.

## Inputs

- **Parent Spec**: [../../03.specs/006-workspace-harness-gap-analysis/spec.md](../../03.specs/006-workspace-harness-gap-analysis/spec.md)
- **Parent Plan**: [../plans/2026-06-04-harness-four-element-alignment.md](../plans/2026-06-04-harness-four-element-alignment.md)

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| ------- | ----------- | ---- | --------------------- | ------------------- | --------------------- | ----- | ------ |
| H4-T-001 | Audit current governance/runtime/hook/memory surfaces | eval | Harness audit | PLN-001 | Current Audit Ledger | platform | Done |
| H4-T-002 | Add four-element control model to common catalog | doc | REQ-H4-002 | PLN-002 | `harness-catalog.md` update | platform | Done |
| H4-T-003 | Add provider four-element runtime contracts | guardrail | REQ-H4-003 | PLN-003 | `.claude/CLAUDE.md`, `.codex/CODEX.md` updates | platform | Done |
| H4-T-004 | Update workspace harness audit skill | prompt | REQ-H4-004 | PLN-004 | `.agents/skills/workspace-harness-audit/skill.md` update | platform | Done |
| H4-T-005 | Add repository quality regression checks | test | REQ-H4-005 | PLN-005 | `scripts/validate-repo-quality-gates.sh` update | platform | Done |
| H4-T-006 | Add docs language/template and drift GC contracts | guardrail | REQ-H4-006 | PLN-006 | `documentation-protocol.md`, `stage-authoring-matrix.md`, `agentic.md`, `docs/README.md` updates | platform | Done |
| H4-T-007 | Normalize AI-agent requirement prose | doc | REQ-H4-006 | PLN-006 | Existing PRD `AI Agent Requirements` sections use English | platform | Done |
| H4-T-008 | Update indexes and progress memory | memory | REQ-H4-007 | PLN-007 | README index rows and progress ledger entry | platform | Done |
| H4-T-009 | Run static validation | eval | Verification | PLN-007 | Verification Summary | platform | Done |

### Phase View

### Phase 1 - Workspace Analysis and Review

- [x] H4-T-001 Audit current governance/runtime/hook/memory surfaces.

### Phase 2 - Implementation Planning

- [x] H4-T-002 Add four-element control model to common catalog.
- [x] H4-T-003 Add provider four-element runtime contracts.

### Phase 3 - Implementation

- [x] H4-T-004 Update workspace harness audit skill.
- [x] H4-T-005 Add repository quality regression checks.
- [x] H4-T-006 Add docs language/template and drift GC contracts.
- [x] H4-T-007 Normalize AI-agent requirement prose.
- [x] H4-T-008 Update indexes and progress memory.
- [x] H4-T-009 Run static validation.

## Approval and Safety Boundaries

- **Allowed Paths**: `H4-T-001 through H4-T-009` is limited to these Harness Four-Element Alignment owners and Task-Table surfaces:
  - `docs/04.execution/tasks/2026-06-04-harness-four-element-alignment.md`
  - `docs/03.specs/006-workspace-harness-gap-analysis/spec.md`
  - `docs/04.execution/plans/2026-06-04-harness-four-element-alignment.md`
  - `.claude/CLAUDE.md`
  - `.codex/CODEX.md`
  - `.agents/skills/workspace-harness-audit/skill.md`
  - `scripts/validate-repo-quality-gates.sh`
- **Forbidden Paths**: provider account settings, live agent sessions, credentials, model/runtime policy outside the parent Plan, and repository paths outside the Harness Four-Element Alignment surfaces.
- **Approval Required**: Human approval is required before Harness Four-Element Alignment provider configuration, model-policy promotion, remote agent action, credential access, protected-file expansion, push, merge, or publication.
- **Static Validation**: Preserve the Harness Four-Element Alignment outcomes and limitations recorded in Verification Summary; use these recorded checks:
  - `git diff --check`
  - `python3 -m json.tool .claude/settings.json`
  - `python3 -m json.tool .codex/hooks.json`
  - `python3 -m json.tool .agents/hooks.json`
- **Live Validation**: DEFER — Harness Four-Element Alignment is closed by repository-static/documentation evidence; historical live commands, if any, are not authority for a new cluster, provider, external-service, or deployment claim.
- **Secret / Vault Handling**: Use only redacted repository contracts for Harness Four-Element Alignment; do not read or print provider tokens, auth files, memory stores, private logs, kubeconfigs, secret values, or shell history.
- **Rollback Plan**: Revert the logical Harness Four-Element Alignment change set for `H4-T-001 through H4-T-009` and restore its allowed implementation/evidence paths with this Task and parent Plan; documentation rollback does not authorize live mutation.
- **Evidence Location**: Durable Harness Four-Element Alignment evidence remains in:
  - `docs/04.execution/tasks/2026-06-04-harness-four-element-alignment.md`
  - `docs/03.specs/006-workspace-harness-gap-analysis/spec.md`
  - `docs/04.execution/plans/2026-06-04-harness-four-element-alignment.md`
  - `.agents/**`
  - `.codex/**`

## Verification Summary

- **Test Commands**:
  - `git diff --check` — PASS.
  - `python3 -m json.tool .claude/settings.json` — PASS.
  - `python3 -m json.tool .codex/hooks.json` — PASS.
  - `python3 -m json.tool .agents/hooks.json` — PASS.
  - `bash -n scripts/validate-repo-quality-gates.sh` — PASS.
  - `find infrastructure scripts docs/00.agent-governance/hooks -type f -name '*.sh' -exec bash -n {} +` — PASS.
  - `bash scripts/generate-llm-wiki-index.sh --check` — PASS.
  - `bash scripts/validate-repo-quality-gates.sh .` — PASS after adding four-element, language-boundary, and drift-GC regression checks.
  - `bash scripts/validate-gitops-structure.sh` — PASS.
  - `bash scripts/validate-k8s-manifests.sh .` — PASS with optional `kube-linter` skip because it is not installed locally.
  - `bash scripts/check-secret-handling.sh .` — PASS.
  - `bash scripts/validate-policy-gates.sh .` — PASS with built-in fallback because optional `conftest` is not installed locally.
  - `bash infrastructure/tests/verify-contracts-static.sh` — PASS.
  - `/home/hy/.local/bin/pre-commit run --files <changed files>` — PASS after
    approved outside-sandbox execution.
- **Eval Commands**:
  - `zsh -lc 'command -v pre-commit'` — PASS,
    `/home/hy/.local/bin/pre-commit`.
  - `/home/hy/.local/bin/pre-commit run --all-files` — FAILED in sandbox:
    EOF fixer could not open some `.agents/**` / `.codex/**` files and
    `detect-secrets` reported existing `graphify-out/**` generated-output false
    positives. Changed-file pre-commit passed after approved outside-sandbox
    execution.
  - `zsh -lc 'command -v rtk'` — PASS, `/home/hy/.local/bin/rtk`.
  - `/home/hy/.local/bin/rtk --version` — PASS, `rtk 0.34.3`.
  - `/home/hy/.local/bin/rtk gain` — failed to initialize its tracking
    database; commands were run directly without inspecting private RTK state.
- **Logs / Evidence Location**:
  - This task document.
  - [Progress Ledger](../../00.agent-governance/memory/progress.md)

## Traceability

- **Spec**: [../../03.specs/006-workspace-harness-gap-analysis/spec.md](../../03.specs/006-workspace-harness-gap-analysis/spec.md)
- **Plan**: [../plans/2026-06-04-harness-four-element-alignment.md](../plans/2026-06-04-harness-four-element-alignment.md)
- **Harness Catalog**: [../../00.agent-governance/harness-catalog.md](../../00.agent-governance/harness-catalog.md)
- **Claude Runtime Baseline**: [../../../.claude/CLAUDE.md](../../../.claude/CLAUDE.md)
- **Codex Runtime Baseline**: [../../../.codex/CODEX.md](../../../.codex/CODEX.md)
- **Repository Quality Gate**: [../../../scripts/validate-repo-quality-gates.sh](../../../scripts/validate-repo-quality-gates.sh)
