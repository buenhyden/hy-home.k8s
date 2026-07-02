---
title: 'Task: Harness Governance V2 Overlay'
type: sdlc/task
status: done
owner: platform
updated: 2026-06-05
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

## Working Rules

- Keep `docs/00.agent-governance` as the common AI Agent governance SSOT.
- Keep `.claude/**` and `.codex/**` as provider adapters derived from Stage 00.
- Do not create a `skill-library` router, new runtime agents, tracked Hookify
  rules, provider-local skill trees, or `.claude/evals`.
- Record repo-changing progress only in
  `docs/00.agent-governance/memory/progress.md`.
- Treat eval PASS as explicit command evidence or recorded human/operator
  approval only.
- Do not probe or mutate live k3d, ArgoCD, Vault, ESO, Kubernetes resources,
  secret values, CI topology, or model policy.

## Named Skill Application Boundary

| Named Skill | Path Evidence | Application in This Task |
| ----------- | ------------- | ------------------------ |
| `imp-using-superpowers` | `/home/hy/.agents/skills/imp-using-superpowers/SKILL.md` exists | Applied as the process reminder to load named skills before acting. The current Codex app uses local skill files rather than a dedicated Skill tool. |
| `skill-creator` | `/home/hy/.codex/skills/.system/skill-creator/SKILL.md` exists | Applied to update the existing `workspace-harness-audit` skill concisely instead of creating a new skill. |
| `imp-agent-md-refactor` | `/home/hy/.agents/skills/imp-agent-md-refactor/SKILL.md` exists | Applied as the progressive-disclosure lens for thin provider adapters and Stage 00 SSOT. |
| `imp-claude-md-improver` | `/home/hy/.agents/skills/imp-claude-md-improver/SKILL.md` exists | Applied as a targeted Claude runtime-baseline improvement lens; no broad interactive quality-report flow was needed because the task supplied an implementation plan. |
| `Hook Development` | `/home/hy/.agents/skills/hook-development/SKILL.md` exists | Applied to keep shared enforcement in tracked settings, hooks, hook JSON, scripts, and validators. |
| `imp-doc-coauthoring` | `/home/hy/.agents/skills/imp-doc-coauthoring/SKILL.md` exists | Applied as document-structure guidance for Plan/Task evidence; the request was already scoped, so no extra co-authoring interview was needed. |
| `imp-harness` | `/home/hy/.agents/skills/imp-harness/SKILL.md` exists | Applied as the primary harness architecture lens while preserving existing Stage 00 surfaces. |
| `testing-handbook-skills:harness-writing` | `/home/hy/.codex/trailofbits-skills/plugins/testing-handbook-skills/skills/harness-writing/SKILL.md` exists | Applied as a determinism and reproducibility lens, not as a fuzz-target implementation request. |
| `agent-sort` | `/home/hy/.codex/skills/agent-sort/SKILL.md` exists | Applied to classify ECC surfaces into evidence-backed DAILY and LIBRARY buckets. |
| `workflow-skill-design:designing-workflow-skills` | `/home/hy/.codex/trailofbits-skills/plugins/workflow-skill-design/skills/designing-workflow-skills/SKILL.md` exists | Applied to add numbered phases, Entry Criteria, Exit Criteria, and Verification Criteria to `workspace-harness-audit`. |
| `Writing Hookify Rules` | `/home/hy/.agents/skills/writing-hookify-rules/SKILL.md` exists | Applied to record `.claude/hookify.*.local.md` as ignored local advisory, not tracked shared enforcement. |
| `enhance-prompt` | `/home/hy/.agents/skills/enhance-prompt/SKILL.md` exists | Recorded as a near-miss no-op because this task is not a UI/Stitch prompt improvement task. |
| `eval-harness` | `/home/hy/.codex/skills/eval-harness/SKILL.md` exists | Applied to express completion as deterministic repo-static capability and regression eval evidence. |

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

## Suggested Types

- `doc`
- `test`
- `eval`
- `guardrail`
- `prompt`
- `memory`

## Agent-specific Types (If Applicable)

- `prompt`
- `tool`
- `memory`
- `guardrail`
- `eval`
- `observability`

## Phase View (Optional)

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

## Related Documents

- **Spec**: [../../03.specs/006-workspace-harness-gap-analysis/spec.md](../../03.specs/006-workspace-harness-gap-analysis/spec.md)
- **Plan**: [../plans/2026-06-05-harness-governance-v2-overlay.md](../plans/2026-06-05-harness-governance-v2-overlay.md)
- **Harness Catalog**: [../../00.agent-governance/harness-catalog.md](../../00.agent-governance/harness-catalog.md)
- **Progress Ledger**: [../../00.agent-governance/memory/progress.md](../../00.agent-governance/memory/progress.md)
