---
title: 'Agent Governance Contract Normalization Task Record'
type: sdlc/task
status: done
owner: platform
updated: 2026-07-14
---

# Task: Agent Governance Contract Normalization

## Overview

This document tracks implementation and verification work for the Agent
Governance Contract Normalization stream. It keeps the task units derived from
the parent Spec and Plan traceable, with compact evidence for each commit-sized
unit.

**2026-07-14 terminology correction:** T-001 through T-005 remain done, and
their commands, eight-role point-in-time counts, validation results, and commit
facts are preserved. Current classification treats `.claude/agents/*.md` and
`.codex/agents/*.toml` as native role files; `.agents/**` as shared/local
Antigravity assets; `.claude/CLAUDE.md` and `.codex/CODEX.md` as
repository-local baselines; `.codex/hooks.json` and `.agents/hooks.json` as
context/validation wiring; and Gemini CLI `.gemini/**` as absent/`DEFER`.

## Inputs

- **Parent Spec**:
  [../../03.specs/015-agent-governance-contract-normalization/spec.md](../../03.specs/015-agent-governance-contract-normalization/spec.md)
- **Parent Plan**:
  [../plans/2026-07-04-agent-governance-contract-normalization.md](../plans/2026-07-04-agent-governance-contract-normalization.md)

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| ------- | ----------- | ---- | --------------------- | ------------------- | --------------------- | ----- | ------ |
| T-001 | Create execution task record and capture baseline drift inventory | doc | Contracts, Evaluation | PLN-001 | Baseline inventory commands, `git diff --check`, repo quality gate | platform | Done |
| T-002 | Normalize Stage 00 canonical contract wording | doc | Contracts, Core Design | PLN-002 | Official source basis checked 2026-07-04, focused owner/drift scans, JSON/TOML parse checks, repo quality gate | platform | Done |
| T-003 | Align provider adapter surfaces | doc | Data / Interface Contract, Governance Contract | PLN-003 | Root shim/runtime baseline checks, provider metadata scans, JSON/TOML parse checks, repo quality gate | platform | Done |
| T-004 | Align GitHub, QA, CI/CD, and protected-surface enforcement | doc | Guardrails, Evaluation | PLN-004 | Frontmatter scans, workflow parse checks, validator status, repo quality gate | platform | Done |
| T-005 | Complete final review, evidence closure, and branch-readiness handoff | doc | Evaluation, Memory & Context Strategy | PLN-005 | Full validation bundle and final review evidence | platform | Done |

### Phase View

### PLN-001

- [x] T-001 Create execution task record and capture baseline drift inventory.

### PLN-002

- [x] T-002 Normalize Stage 00 canonical contract wording.

### PLN-003

- [x] T-003 Align provider adapter surfaces.

### PLN-004

- [x] T-004 Align GitHub, QA, CI/CD, and protected-surface enforcement.

### PLN-005

- [x] T-005 Complete final review, evidence closure, and branch-readiness
  handoff.

### Baseline Drift Inventory

### Commands

- `rg --files AGENTS.md CLAUDE.md GEMINI.md .agents .claude .codex .github docs/00.agent-governance | sort`
- `rg -n "^---$|^name:|^description:|^model:|^tools:|^model_reasoning_effort|^description =|^developer_instructions =|^name =" .claude/agents .agents/agents .codex/agents`
- `rg -n "tools:|permission gate|hook wiring|provider-native|mirror|parity|Subagent|subagent|AGENTS.md|CLAUDE.md|GEMINI.md|QA|CI/CD|protected surface|frontmatter" docs/00.agent-governance AGENTS.md CLAUDE.md GEMINI.md .agents .claude .codex .github`

### Findings

- Target inventory returned 115 files across root provider shims, `.agents/`,
  `.claude/`, `.codex/`, `.github/`, and `docs/00.agent-governance/`.
- The historical metadata inventory confirmed eight Claude agent files with
  native `tools:` frontmatter, eight local/Antigravity Markdown adapters with
  Gemini-named model declarations, and eight Codex TOML role files with `model` and
  `model_reasoning_effort`.
- Contract-drift candidate scan returned active surfaces for provider parity,
  hook behavior, QA/CI/CD expectations, protected-surface rules, and
  frontmatter boundaries.

### Classification

| Class | Representative Surfaces | Finding |
| ----- | ----------------------- | ------- |
| canonical owner | `docs/00.agent-governance/common-governance.md`, `subagent-protocol.md`, `harness-catalog.md`, `rules/*.md`, `providers/*.md` | Stage 00 already owns durable policy, parity, provider loading, hook boundary, QA, and protected-surface wording. |
| adapter summary | `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.claude/CLAUDE.md`, `.codex/CODEX.md`, `.agents/GEMINI.md`, tracked role files | Root shims, repository-local baselines, native Claude/Codex roles, and local/Antigravity projections summarize Stage 00 without implying Gemini CLI native support. |
| enforcement | `.github/ABOUT.md`, `.github/PULL_REQUEST_TEMPLATE.md`, `.github/workflows/ci.yml`, `.claude/settings.json`, `.codex/hooks.json`, `.agents/hooks.json`, `docs/00.agent-governance/hooks/*.sh` | GitHub controls and scripts enforce QA/CI/CD; `.codex/hooks.json` and `.agents/hooks.json` provide context/validation wiring rather than Claude-equivalent permission gates. |
| historical evidence | `docs/00.agent-governance/memory/progress.md`, `.claude/hookify.*.local.md` | Progress entries and local Hookify advisory files preserve prior decisions and drift-remediation context. |

## Approval and Safety Boundaries

- **Allowed Paths**: `T-001 through T-005` is limited to these Agent Governance Contract Normalization owners and Task-Table surfaces:
  - `docs/04.execution/tasks/2026-07-04-agent-governance-contract-normalization.md`
  - `docs/03.specs/015-agent-governance-contract-normalization/spec.md`
  - `docs/04.execution/plans/2026-07-04-agent-governance-contract-normalization.md`
  - `docs/00.agent-governance`
  - `docs/00.agent-governance/common-governance.md`
  - `.claude/CLAUDE.md`
  - `.codex/CODEX.md`
- **Forbidden Paths**: provider account settings, live agent sessions, credentials, model/runtime policy outside the parent Plan, and repository paths outside the Agent Governance Contract Normalization surfaces.
- **Approval Required**: Human approval is required before Agent Governance Contract Normalization provider configuration, model-policy promotion, remote agent action, credential access, protected-file expansion, push, merge, or publication.
- **Static Validation**: Preserve the Agent Governance Contract Normalization outcomes and limitations recorded in Verification Summary; use these recorded checks:
  - `git status --short --branch`
  - `git diff --check`
  - `bash scripts/validate-repo-quality-gates.sh .`
  - `python3 - <<'PY' ... tomllib.loads(path.read_text()) ... PY`
- **Live Validation**: DEFER — Agent Governance Contract Normalization is closed by repository-static/documentation evidence; historical live commands, if any, are not authority for a new cluster, provider, external-service, or deployment claim.
- **Secret / Vault Handling**: Use only redacted repository contracts for Agent Governance Contract Normalization; do not read or print provider tokens, auth files, memory stores, private logs, kubeconfigs, secret values, or shell history.
- **Rollback Plan**: Revert the logical Agent Governance Contract Normalization change set for `T-001 through T-005` and restore its allowed implementation/evidence paths with this Task and parent Plan; documentation rollback does not authorize live mutation.
- **Evidence Location**: Durable Agent Governance Contract Normalization evidence remains in:
  - `docs/04.execution/tasks/2026-07-04-agent-governance-contract-normalization.md`
  - `docs/03.specs/015-agent-governance-contract-normalization/spec.md`
  - `docs/04.execution/plans/2026-07-04-agent-governance-contract-normalization.md`
  - `docs/00.agent-governance/memory/progress.md`
  - `docs/00.agent-governance/common-governance.md`

## Verification Summary

- **Test Commands**:
  - `git status --short --branch`
  - `git diff --check` — PASS.
  - `bash scripts/validate-repo-quality-gates.sh .` — PASS, including
    `[PASS] repository quality gates passed`.
- **Eval Commands**:
  - Baseline inventory scans listed in `Baseline Drift Inventory`.
- **Logs / Evidence Location**:
  - This task record.
  - `../../00.agent-governance/memory/progress.md`

### T-002 Evidence

### Official Source Basis

Checked on 2026-07-04:

- Codex custom instructions with `AGENTS.md`: <https://developers.openai.com/codex/guides/agents-md>
- Codex subagents: <https://developers.openai.com/codex/subagents>
- Codex CLI/config/approval modes: <https://developers.openai.com/codex/cli>
- Claude Code settings: <https://code.claude.com/docs/en/settings>
- Claude Code hooks: <https://code.claude.com/docs/en/hooks>
- Claude Code subagents: <https://code.claude.com/docs/en/sub-agents>
- Gemini CLI commands and hierarchical memory: <https://github.com/google-gemini/gemini-cli/blob/main/docs/reference/commands.md>
- GitHub Actions: <https://docs.github.com/en/actions>

### Files Changed

- `docs/00.agent-governance/common-governance.md`
- `docs/00.agent-governance/subagent-protocol.md`
- `docs/00.agent-governance/harness-catalog.md`
- `docs/00.agent-governance/harness-implementation-map.md`
- `docs/00.agent-governance/rules/bootstrap.md`
- `docs/00.agent-governance/rules/agentic.md`
- `docs/00.agent-governance/rules/standards.md`
- `docs/00.agent-governance/rules/quality-standards.md`
- `docs/00.agent-governance/rules/approval-boundaries.md`
- `docs/00.agent-governance/scopes/*.md`
- `docs/00.agent-governance/providers/claude.md`
- `docs/00.agent-governance/providers/codex.md`
- `docs/00.agent-governance/providers/gemini.md`
- `docs/04.execution/tasks/2026-07-04-agent-governance-contract-normalization.md`
- `docs/00.agent-governance/memory/progress.md`

### Validation Commands

- `git diff --check` — PASS.
- `jq empty .agents/hooks.json .claude/settings.json .codex/hooks.json` —
  PASS.
- `python3 - <<'PY' ... tomllib.loads(path.read_text()) ... PY` — PASS for
  all `.codex/agents/*.toml`.
- `bash scripts/validate-repo-quality-gates.sh .` — PASS, including
  `[PASS] repository quality gates passed`.

### Local Review Follow-up

- Local T-002 review found active `docs/00.agent-governance/scopes/*.md`
  bridge text that still said `Task tool only`; scope bridge wording was
  aligned to the then-current delegated-agent contract. The 2026-07-14 current
  contract distinguishes native Claude/Codex dispatch from local/Antigravity
  workflow compatibility and `DEFER` Gemini CLI native delegation.

### Next

- T-003 is tracked below.

### T-003 Evidence

### Files Changed

- `AGENTS.md`
- `CLAUDE.md`
- `GEMINI.md`
- `.claude/CLAUDE.md`
- `.agents/GEMINI.md`
- `docs/04.execution/tasks/2026-07-04-agent-governance-contract-normalization.md`
- `docs/00.agent-governance/memory/progress.md`

### Adapter Parity Findings

- Root shims remain thin: `AGENTS.md` has 17 lines, `CLAUDE.md` has 16 lines,
  and `GEMINI.md` has 16 lines.
- Agent stem parity scan returned `claude_only= []`, `gemini_only= []`, and
  `codex_only= []`.
- Historical metadata scan confirmed Claude `model:` plus `tools:`, a
  local/Antigravity `model:` declaration, and Codex `model =` plus
  `model_reasoning_effort`; it did not establish Gemini CLI native discovery.
- Hook JSON files parsed successfully; no Claude-style permission keys were
  added to Codex or local/Antigravity context/validation wiring.

### Validation Commands

- `git diff --check` — PASS.
- `jq empty .agents/hooks.json .claude/settings.json .codex/hooks.json` —
  PASS.
- `python3 - <<'PY' ... tomllib.loads(path.read_text()) ... PY` — PASS for
  all `.codex/agents/*.toml`.
- `bash scripts/validate-repo-quality-gates.sh .` — PASS, including
  `[PASS] repository quality gates passed`.

### Next

- T-004 is tracked below.

### T-004 Evidence

### Files Changed

- `.github/SECURITY.md`
- `docs/00.agent-governance/rules/quality-standards.md`
- `docs/00.agent-governance/rules/approval-boundaries.md`
- `docs/04.execution/tasks/2026-07-04-agent-governance-contract-normalization.md`
- `docs/00.agent-governance/memory/progress.md`

### Findings

- `.github/ABOUT.md`, `.github/PULL_REQUEST_TEMPLATE.md`, and
  `.github/SECURITY.md` remain frontmatter-free GitHub-native Markdown.
- `.github/workflows/*.yml` parsed successfully with PyYAML.
- `.github/SECURITY.md` now routes secret-handling and protected-surface
  boundaries to the canonical approval-boundaries rule.
- `quality-standards.md` and `approval-boundaries.md` explicitly separate
  provider-agnostic QA/CI from live deployment CD and live runtime readiness.
- Validator logic unchanged; existing repository quality gate coverage used.

### Validation Commands

- GitHub Markdown frontmatter-free check — PASS.
- GitHub workflow YAML parse — PASS with `workflow-yaml-ok`.
- `git diff --check` — PASS.
- `jq empty .agents/hooks.json .claude/settings.json .codex/hooks.json` —
  PASS.
- `bash scripts/validate-repo-quality-gates.sh .` — PASS, including
  `[PASS] repository quality gates passed`.

### Next

- T-005 is tracked below.

### T-005 Evidence

### Final Validation Bundle

- `git diff --check` - PASS.
- `jq empty .agents/hooks.json .claude/settings.json .codex/hooks.json` -
  PASS.
- `bash -n scripts/validate-repo-quality-gates.sh` - PASS.
- `bash scripts/validate-repo-quality-gates.sh .` - PASS, including
  `[PASS] repository quality gates passed`.
- `bash scripts/validate-harness.sh` - PASS, including
  `PASS harness repo-static validation`.

### Focused Final Scan

- Focused scan command:
  `rg -n "docs/superpowers|deprecated owner value|permission gate equivalent|Task tool only|must contain.*tools" AGENTS.md CLAUDE.md GEMINI.md .agents .claude .codex .github docs/00.agent-governance docs/04.execution/plans/2026-07-04-agent-governance-contract-normalization.md docs/04.execution/tasks/2026-07-04-agent-governance-contract-normalization.md`.
- Matches were classified as allowed active guardrail text, negated
  `permission gate equivalent` wording, or historical/plan/task evidence.
- Active policy no longer claims that `.codex/hooks.json` or local
  `.agents/hooks.json` is a Claude permission gate equivalent or that every
  tracked adapter must use Claude-style `tools:` frontmatter.

### Review Result

- Local final review completed because the reviewer subagent hit the current
  account usage limit during T-002 review.
- No blocking correctness, scope, safety, validation, or contract issue remains.
- Repo-static validation remains distinct from live k3d, ArgoCD, Vault, ESO, or
  deployment readiness.

## Traceability

- **Spec**:
  [../../03.specs/015-agent-governance-contract-normalization/spec.md](../../03.specs/015-agent-governance-contract-normalization/spec.md)
- **Plan**:
  [../plans/2026-07-04-agent-governance-contract-normalization.md](../plans/2026-07-04-agent-governance-contract-normalization.md)
- **Task Template**:
  [../../99.templates/templates/sdlc/execution/task.template.md](../../99.templates/templates/sdlc/execution/task.template.md)
