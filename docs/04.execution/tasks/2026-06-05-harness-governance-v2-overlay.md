---
title: 'Task: Harness Governance V2 Overlay'
type: sdlc/task
status: done
owner: platform
updated: 2026-07-13
---

# Task: Harness Governance V2 Overlay

## Overview

This document records evidence for adding DAILY/LIBRARY classification,
workflow skill phase criteria, Hookify local advisory boundaries,
deterministic eval completion contracts, and canonical `progress.md`
single-source rules on top of the Stage 00 four-element harness contract.

## Inputs

- **Parent Spec**: [../../03.specs/006-workspace-harness-gap-analysis/spec.md](../../03.specs/006-workspace-harness-gap-analysis/spec.md)
- **Parent Plan**: [../plans/2026-06-05-harness-governance-v2-overlay.md](../plans/2026-06-05-harness-governance-v2-overlay.md)

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| ------- | ----------- | ---- | --------------------- | ------------------- | --------------------- | ----- | ------ |
| V2-T-001 | Add ECC DAILY/LIBRARY and Agent Eval Completion Contract | guardrail | Harness governance | V2-PLN-001 | `docs/00.agent-governance/harness-catalog.md` | platform | Done |
| V2-T-002 | Refactor workspace harness audit into phase workflow | prompt | Harness skill quality | V2-PLN-002 | `.agents/skills/workspace-harness-audit/skill.md` | platform | Done |
| V2-T-003 | Add Claude/Codex adapter pointers for progress, eval, and hook boundary | guardrail | Provider adapters | V2-PLN-003 | `.claude/CLAUDE.md`, `.codex/CODEX.md` | platform | Done |
| V2-T-004 | Add common progress singleton and eval completion rules | doc | Stage 00 rules | V2-PLN-004 | `agentic.md`, `documentation-protocol.md` | platform | Done |
| V2-T-005 | Extend repo quality gate for overlay regression checks | test | Repository validators | V2-PLN-005 | `scripts/validate-repo-quality-gates.sh` | platform | Done |
| V2-T-006 | Update Plan/Task indexes and canonical progress ledger | memory | Documentation evidence | V2-PLN-006 | README rows and `memory/progress.md` entry | platform | Done |
| V2-T-007 | Run deterministic verification | eval | Verification | Verification Plan | Verification Summary | platform | Done |

### Phase View

### Phase 1 - Workspace Review

- [x] V2-T-001 Map existing Stage 00, Claude, Codex, hook, eval, and memory
  surfaces against the overlay request.

### Phase 2 - Implementation Planning

- [x] V2-T-002 Select the existing catalog, runtime baselines, skill,
  governance rules, validator, Plan/Task, README index, and progress ledger as
  the smallest durable surfaces.

### Phase 3 - Implementation

- [x] V2-T-003 Add governance and provider adapter overlay pointers.
- [x] V2-T-004 Add workflow-skill phase criteria and named-skill boundaries.
- [x] V2-T-005 Add deterministic regression checks.
- [x] V2-T-006 Record documentation and memory evidence.
- [x] V2-T-007 Run verification and record results.

## Approval and Safety Boundaries

- **Allowed Paths**: `V2-T-001 through V2-T-007` is limited to these Harness Governance V2 Overlay owners and Task-Table surfaces:
  - `docs/04.execution/tasks/2026-06-05-harness-governance-v2-overlay.md`
  - `docs/03.specs/006-workspace-harness-gap-analysis/spec.md`
  - `docs/04.execution/plans/2026-06-05-harness-governance-v2-overlay.md`
  - `docs/00.agent-governance/harness-catalog.md`
  - `.agents/skills/workspace-harness-audit/skill.md`
  - `.claude/CLAUDE.md`
  - `.codex/CODEX.md`
- **Forbidden Paths**: provider account settings, live agent sessions, credentials, model/runtime policy outside the parent Plan, and repository paths outside the Harness Governance V2 Overlay surfaces.
- **Approval Required**: Human approval is required before Harness Governance V2 Overlay provider configuration, model-policy promotion, remote agent action, credential access, protected-file expansion, push, merge, or publication.
- **Static Validation**: Preserve the Harness Governance V2 Overlay outcomes and limitations recorded in Verification Summary; use these recorded checks:
  - `bash scripts/validate-repo-quality-gates.sh .`
  - `git diff --check`
  - `bash -n scripts/validate-repo-quality-gates.sh`
  - `python3 -m json.tool .claude/settings.json`
- **Live Validation**: DEFER — Harness Governance V2 Overlay is closed by repository-static/documentation evidence; historical live commands, if any, are not authority for a new cluster, provider, external-service, or deployment claim.
- **Secret / Vault Handling**: Use only redacted repository contracts for Harness Governance V2 Overlay; do not read or print provider tokens, auth files, memory stores, private logs, kubeconfigs, secret values, or shell history.
- **Rollback Plan**: Revert the logical Harness Governance V2 Overlay change set for `V2-T-001 through V2-T-007` and restore its allowed implementation/evidence paths with this Task and parent Plan; documentation rollback does not authorize live mutation.
- **Evidence Location**: Durable Harness Governance V2 Overlay evidence remains in:
  - `docs/04.execution/tasks/2026-06-05-harness-governance-v2-overlay.md`
  - `docs/03.specs/006-workspace-harness-gap-analysis/spec.md`
  - `docs/04.execution/plans/2026-06-05-harness-governance-v2-overlay.md`
  - `docs/00.agent-governance/memory/progress.md`
  - `.agents/**`

## Verification Summary

- **Test Commands**:
  - `bash scripts/validate-repo-quality-gates.sh .` — PASS.
  - `git diff --check` — PASS.
  - `bash -n scripts/validate-repo-quality-gates.sh` — PASS.
  - `python3 -m json.tool .claude/settings.json` — PASS.
  - `python3 -m json.tool .codex/hooks.json` — PASS.
  - `python3 -m json.tool .agents/hooks.json` — PASS.
  - `find infrastructure scripts docs/00.agent-governance/hooks -type f -name '*.sh' -exec bash -n {} +` — PASS.
  - `bash scripts/generate-llm-wiki-index.sh --check` — PASS.
  - `git check-ignore -v .claude/hookify.postflight-reminder.local.md` — PASS,
    `.gitignore:66:.claude/*.local.md`.
- **Eval Commands**:
  - `rg --files | rg '(^|/)progress\.md$'` — PASS, returned only
    `docs/00.agent-governance/memory/progress.md`.
  - `/home/hy/.local/bin/pre-commit run --files <changed files>` — PASS after
    approved outside-sandbox execution. The first sandbox run failed because
    EOF fixer could not open `.agents/**` and `.codex/**` files.
- **Logs / Evidence Location**:
  - This task, paired Plan, canonical progress ledger, and final command output.

## Traceability

- **Spec**: [../../03.specs/006-workspace-harness-gap-analysis/spec.md](../../03.specs/006-workspace-harness-gap-analysis/spec.md)
- **Plan**: [../plans/2026-06-05-harness-governance-v2-overlay.md](../plans/2026-06-05-harness-governance-v2-overlay.md)
- **Harness Catalog**: [../../00.agent-governance/harness-catalog.md](../../00.agent-governance/harness-catalog.md)
- **Progress Ledger**: [../../00.agent-governance/memory/progress.md](../../00.agent-governance/memory/progress.md)
