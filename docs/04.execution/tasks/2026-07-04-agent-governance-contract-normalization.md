---
title: 'Agent Governance Contract Normalization Task Record'
type: sdlc/task
status: draft
owner: platform
updated: 2026-07-04
---

# Task: Agent Governance Contract Normalization

## Overview

This document tracks implementation and verification work for the Agent
Governance Contract Normalization stream. It keeps the task units derived from
the parent Spec and Plan traceable, with compact evidence for each commit-sized
unit.

## Inputs

- **Parent Spec**:
  [../../03.specs/015-agent-governance-contract-normalization/spec.md](../../03.specs/015-agent-governance-contract-normalization/spec.md)
- **Parent Plan**:
  [../plans/2026-07-04-agent-governance-contract-normalization.md](../plans/2026-07-04-agent-governance-contract-normalization.md)

## Working Rules

- Keep provider parity provider-native: same role, scope imports, guardrails,
  handoff, and postflight expectations; not identical metadata keys.
- Keep root provider shims thin and route durable policy to Stage 00 owners.
- Treat `.github`, hooks, and validators as enforcement projections, not
  independent policy owners.
- Documentation-only work still needs validation evidence.
- Repo-static validation must not be reported as live runtime readiness unless
  a separate live check was approved and run.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| ------- | ----------- | ---- | --------------------- | ------------------- | --------------------- | ----- | ------ |
| T-001 | Create execution task record and capture baseline drift inventory | doc | Contracts, Evaluation | PLN-001 | Baseline inventory commands, `git diff --check`, repo quality gate | platform | Done |
| T-002 | Normalize Stage 00 canonical contract wording | doc | Contracts, Core Design | PLN-002 | Focused owner/drift scans and repo quality gate | platform | Todo |
| T-003 | Align provider adapter surfaces | doc | Data / Interface Contract, Governance Contract | PLN-003 | Provider metadata scans, JSON/TOML parse checks, repo quality gate | platform | Todo |
| T-004 | Align GitHub, QA, CI/CD, and protected-surface enforcement | doc | Guardrails, Evaluation | PLN-004 | Frontmatter scans, workflow parse checks, gate/harness validation | platform | Todo |
| T-005 | Complete final review, evidence closure, and branch-readiness handoff | doc | Evaluation, Memory & Context Strategy | PLN-005 | Full validation bundle and final review evidence | platform | Todo |

## Suggested Types

- `doc`
- `test`
- `eval`
- `guardrail`

## Phase View

### PLN-001

- [x] T-001 Create execution task record and capture baseline drift inventory.

### PLN-002

- [ ] T-002 Normalize Stage 00 canonical contract wording.

### PLN-003

- [ ] T-003 Align provider adapter surfaces.

### PLN-004

- [ ] T-004 Align GitHub, QA, CI/CD, and protected-surface enforcement.

### PLN-005

- [ ] T-005 Complete final review, evidence closure, and branch-readiness
  handoff.

## Baseline Drift Inventory

### Commands

- `rg --files AGENTS.md CLAUDE.md GEMINI.md .agents .claude .codex .github docs/00.agent-governance | sort`
- `rg -n "^---$|^name:|^description:|^model:|^tools:|^model_reasoning_effort|^description =|^developer_instructions =|^name =" .claude/agents .agents/agents .codex/agents`
- `rg -n "tools:|permission gate|hook wiring|provider-native|mirror|parity|Subagent|subagent|AGENTS.md|CLAUDE.md|GEMINI.md|QA|CI/CD|protected surface|frontmatter" docs/00.agent-governance AGENTS.md CLAUDE.md GEMINI.md .agents .claude .codex .github`

### Findings

- Target inventory returned 115 files across root provider shims, `.agents/`,
  `.claude/`, `.codex/`, `.github/`, and `docs/00.agent-governance/`.
- Provider metadata inventory confirmed eight Claude agent files with native
  `tools:` frontmatter, eight Gemini agent files with Gemini model frontmatter,
  and eight Codex TOML agent mirrors with `model` and
  `model_reasoning_effort`.
- Contract-drift candidate scan returned active surfaces for provider parity,
  hook behavior, QA/CI/CD expectations, protected-surface rules, and
  frontmatter boundaries.

### Classification

| Class | Representative Surfaces | Finding |
| ----- | ----------------------- | ------- |
| canonical owner | `docs/00.agent-governance/common-governance.md`, `subagent-protocol.md`, `harness-catalog.md`, `rules/*.md`, `providers/*.md` | Stage 00 already owns durable policy, parity, provider loading, hook boundary, QA, and protected-surface wording. |
| adapter summary | `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.claude/CLAUDE.md`, `.codex/CODEX.md`, `.agents/GEMINI.md`, provider agent files | Root shims and runtime baselines summarize Stage 00 and expose provider-native projections. |
| enforcement | `.github/ABOUT.md`, `.github/PULL_REQUEST_TEMPLATE.md`, `.github/workflows/ci.yml`, `.claude/settings.json`, `.codex/hooks.json`, `.agents/hooks.json`, `docs/00.agent-governance/hooks/*.sh` | GitHub controls, hook settings, hook JSON, and scripts enforce or surface QA/CI/CD and lifecycle checks. |
| historical evidence | `docs/00.agent-governance/memory/progress.md`, `.claude/hookify.*.local.md` | Progress entries and local Hookify advisory files preserve prior decisions and drift-remediation context. |

## Verification Summary

- **Test Commands**:
  - `git status --short --branch`
  - `git diff --check`
  - `bash scripts/validate-repo-quality-gates.sh .`
- **Eval Commands**:
  - Baseline inventory scans listed in `Baseline Drift Inventory`.
- **Logs / Evidence Location**:
  - This task record.
  - `../../00.agent-governance/memory/progress.md`

## Related Documents

- **Spec**:
  [../../03.specs/015-agent-governance-contract-normalization/spec.md](../../03.specs/015-agent-governance-contract-normalization/spec.md)
- **Plan**:
  [../plans/2026-07-04-agent-governance-contract-normalization.md](../plans/2026-07-04-agent-governance-contract-normalization.md)
- **Task Template**:
  [../../99.templates/templates/sdlc/execution/task.template.md](../../99.templates/templates/sdlc/execution/task.template.md)
