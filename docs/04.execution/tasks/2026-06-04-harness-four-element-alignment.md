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

## Approval and Safety Boundaries

- Keep Stage 00 as the common AI Agent governance source of truth.
- Keep `.claude/**` and `.codex/**` as provider adapters based on Stage 00.
- Preserve `.agents/{skills,workflows,output-styles}` as the shared content
  SSoT and provider symlink target.
- Keep human-facing README and overview prose Korean, but keep explicit
  AI-agent-facing requirement sections in English.
- Treat recurring code, document, and structure drift as harness feedback that
  should update a durable rule, skill, hook, validator, template, README index,
  archive Tombstone, or memory entry.
- Do not mutate live k3d, ArgoCD, Vault, ESO, Kubernetes resources, CI
  topology, model policy, or secret-bearing state.
- Record validation evidence before handoff.

### Named Skill Application Boundary

| Named Skill | Path Evidence | Application in This Task |
| ----------- | ------------- | ------------------------ |
| `using-superpowers` | `/home/hy/.codex/plugins/cache/claude-plugins-official/superpowers/5.1.0/skills/using-superpowers/SKILL.md` exists | Applied as the process lens for explicit skill routing and named-skill evidence. The current Codex tool surface did not expose a dedicated Skill invocation tool. |
| `skill-creator` | `/home/hy/.codex/skills/.system/skill-creator/SKILL.md` provided in prompt | Applied to keep `workspace-harness-audit` concise and update an existing skill instead of creating an unnecessary new one. |
| `imp-agent-md-refactor` | `/home/hy/.agents/skills/imp-agent-md-refactor/SKILL.md` provided in prompt | Applied as the progressive-disclosure lens: root gateways stayed thin and detailed behavior moved to catalog/provider baselines. |
| `claude-md-improver` | `/home/hy/.codex/plugins/cache/claude-plugins-official/claude-md-management/1.0.0/skills/claude-md-improver/SKILL.md` exists; `/home/hy/.agents/skills/claude-md-improver/SKILL.md` absent | Applied as a targeted CLAUDE runtime-baseline improvement lens. Full interactive quality-report approval flow was skipped because the user explicitly requested implementation in this turn. |
| `Hook Development` | `/home/hy/.agents/skills/hook-development/SKILL.md` provided in prompt | Applied to keep shared hook scripts and provider wiring as the enforcement/feedback surface instead of adding provider-local hook drift. |
| `imp-doc-coauthoring` | `/home/hy/.agents/skills/imp-doc-coauthoring/SKILL.md` provided in prompt | Applied as a document-structure lens for Plan/Task evidence. The interactive co-authoring workflow was not used because the request supplied scope and asked for implementation. |
| `imp-harness` | `/home/hy/.agents/skills/imp-harness/SKILL.md` provided in prompt | Applied as the primary harness architecture workflow. Existing harness assets were updated in place rather than creating a new agent team or duplicate skill tree. |
| `testing-handbook-skills:harness-writing` | `/home/hy/.codex/trailofbits-skills/plugins/testing-handbook-skills/skills/harness-writing/SKILL.md` exists | Treated as a near-miss technique lens: no fuzz target was needed, but its determinism, input boundary, and feedback-quality principles informed the AI harness validation framing. |

### Current Audit Ledger

| Harness Element | Current Common Surface | Claude Surface | Codex Surface | Result |
| --------------- | ---------------------- | -------------- | ------------- | ------ |
| Instruction and settings documents | `AGENTS.md`, root `CLAUDE.md`, `docs/00.agent-governance/rules/bootstrap.md`, `harness-catalog.md` | `.claude/CLAUDE.md`, `.claude/settings.json`, `.claude/agents/*.md` | `.codex/CODEX.md`, `.codex/hooks.json`, `.codex/agents/*.toml` | Present; relationship made explicit in this task |
| Architecture constraints | `rules/agentic.md`, `subagent-protocol.md`, `model-policy.md`, templates, GitOps-first rules | Native allow/deny policy in `.claude/settings.json` plus shared hooks | Codex sandbox/approval boundary plus `.codex/hooks.json` context/validation wiring | Present; provider difference documented |
| Feedback loops | `scripts/validate-*.sh`, `scripts/check-secret-handling.sh`, `infrastructure/tests/*.sh`, `.github/workflows/ci.yml`, lifecycle hooks | SessionStart, PreToolUse, PostToolUse, Stop, SubagentStop, PreCompact hooks | Same shared hook scripts through Codex event wiring plus explicit validation commands | Present; regression checks strengthened |
| Knowledge stores | `docs/00.agent-governance/memory/progress.md`, `docs/90.references/llm-wiki/wiki-index.md`, Stage 01-05 docs, `graphify-out/GRAPH_REPORT.md` when present | Runtime baseline points to memory, catalog, and generated wiki rules | Runtime baseline points to memory, catalog, generated wiki rules, and RTK limitations | Present; next-session loop documented |
| Documentation language and template routing | `documentation-protocol.md`, `stage-authoring-matrix.md`, `document-stage-routing.md`, `docs/99.templates/README.md`, `docs/README.md` | `.claude/CLAUDE.md` points to common Stage 00; Claude hooks warn and validate authored docs | `.codex/CODEX.md` points to common Stage 00; Codex hooks reuse shared doc validation wiring | Present; explicit AI-agent-facing sections are English and template routing owners are recorded |
| Drift garbage collection | `rules/agentic.md`, `documentation-protocol.md`, `scripts/validate-repo-quality-gates.sh`, `docs/98.archive`, `memory/progress.md` | Claude runtime routes repeated errors to shared harness surfaces | Codex runtime routes repeated errors to shared harness surfaces | Present; recurring drift is treated as a harness feedback loop |

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

### Suggested Types

- `doc`
- `test`
- `eval`
- `guardrail`
- `prompt`
- `memory`

### Agent-specific Types

- `prompt`
- `tool`
- `memory`
- `guardrail`
- `eval`
- `observability`

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
