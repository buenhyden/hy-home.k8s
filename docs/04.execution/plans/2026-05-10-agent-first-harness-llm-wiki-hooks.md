---
title: 'Agent-first Harness, LLM Wiki, and Hook Contract Closure Plan'
type: sdlc/plan
status: done
owner: platform
updated: 2026-05-10
---

# Agent-first Harness, LLM Wiki, and Hook Contract Closure Plan

## Overview

This document is the implementation plan for revalidating and closing the
Harness Engineering, Agent-first Engineering, repo-local LLM Wiki,
hook/feedback loop, and memory ledger hardening for `hy-home.k8s`. It defines
work breakdown, verification, risk management, and completion criteria.

## Context

The current repository already has thin gateways, a `.claude` runtime baseline,
`.codex` mirrors, local agents/skills, a matrix-first harness catalog, a
generated LLM Wiki index, and scoped hook validation.

The point of this work is not to add more runtime surface. It revalidates
whether the already-completed implementation can be trusted and closes the
remaining gaps, excess, and duplication with minimal hardening.

The documentation taxonomy has also been hard-migrated from the prior
13-folder model to the reduced model centered on `01.requirements`,
`02.architecture`, `03.specs`, `04.execution`, `05.operations`,
`90.references`, and `99.templates`. The remaining hardening ensures legacy
path mapping is both explained by governance rules and validated by the repo
quality gate.

## Goals & In-Scope

- **Goals**:
  - Reconfirm Harness Engineering and Agent-first Engineering readiness using current repo evidence.
  - Make Guardrails/Rules, Hooks/Feedback Loop, Memory, and LLM Wiki curation surfaces discoverable from the actual agent runtime.
  - Prevent legacy docs paths from returning and prevent documentation routing from regressing to the old model.
  - Record 2026-05-10 hardening evidence in the Plan, Task, and README indexes.
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
  - New Kubernetes manifests, cluster mutation, or live ArgoCD reconciliation
  - New provider-native instruction layers
  - New agents or skills beyond the existing `wiki-curator`
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
| PLN-003 | Wire hook feedback loops through shared hook scripts and provider event wiring | `docs/00.agent-governance/hooks/*.sh`, `.agents/hooks.json`, `.claude/settings.json`, `.codex/hooks.json` | REQ-AI-003 | JSON, shell, payload simulation PASS |
| PLN-004 | Record reduced docs taxonomy and legacy path mapping | `document-stage-routing.md`, `docs/README.md`, validator | REQ-DOC-001 | old folder and mapping guard PASS |
| PLN-005 | Add plan/task evidence and update README indexes | `docs/04.execution/plans/`, `docs/04.execution/tasks/` | REQ-DOC-002 | template heading checks PASS |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Static | Generated LLM Wiki freshness | `bash scripts/generate-llm-wiki-index.sh --check` | PASS |
| VAL-PLN-002 | Static | Runtime JSON parse | `python3 -m json.tool .claude/settings.json` and `python3 -m json.tool .codex/hooks.json` | PASS |
| VAL-PLN-003 | Static | Hook and script syntax | `bash -n docs/00.agent-governance/hooks/k8s-pre-edit.sh docs/00.agent-governance/hooks/post-validate.sh docs/00.agent-governance/hooks/session-start.sh scripts/validate-repo-quality-gates.sh scripts/generate-llm-wiki-index.sh` | no syntax errors |
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
