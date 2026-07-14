---
title: 'Task: Claude Agent Surface Restoration'
type: sdlc/task
status: done
owner: platform
updated: 2026-07-13
---

# Task: Claude Agent Surface Restoration

## Overview

This document tracks the work units and validation evidence for restoring
`.claude/agents` as the real Claude-specific agent file directory. Phase 3
restoration and validation hardening were completed after Phase 2 planning.

## Inputs

- **Parent Plan**: [../plans/2026-06-01-claude-agent-surface-restoration.md](../plans/2026-06-01-claude-agent-surface-restoration.md)
- **Runtime Baseline**: [../../../.claude/CLAUDE.md](../../../.claude/CLAUDE.md)
- **Harness Catalog**: [../../00.agent-governance/harness-catalog.md](../../00.agent-governance/harness-catalog.md)
- **Subagent Protocol**: [../../00.agent-governance/subagent-protocol.md](../../00.agent-governance/subagent-protocol.md)

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Record current `.claude/agents` symlink drift and intended final state | doc | N/A | PLN-001 | `ls -l .claude/agents .agents/agents .codex/agents` | platform | Done |
| T-002 | Replace `.claude/agents` symlink with real Claude files | impl | N/A | PLN-002 | `test -d .claude/agents && test ! -L .claude/agents` | platform | Done |
| T-003 | Add Claude model/tool frontmatter to all Claude agent files | impl | N/A | PLN-003 | validator parser plus `rg -n "model: Gemini\|Gemini 3\\." .claude/agents` | platform | Done |
| T-004 | Preserve mirror parity across Claude/Gemini/Codex agents | test | N/A | PLN-004 | `bash scripts/validate-repo-quality-gates.sh .` | platform | Done |
| T-005 | Harden validator for symlink and Claude frontmatter drift | test | N/A | PLN-005 | validator fails on symlink/frontmatter drift and passes after remediation | platform | Done |
| T-006 | Update governance/readiness text only where current evidence requires it | doc | N/A | PLN-006 | Current governance text already matched the restored provider-specific agent layout | platform | Done |
| T-007 | Record Phase 3 execution evidence and limitations | doc | N/A | PLN-007 | task verification summary includes commands, skipped checks, and no-live-action statement | platform | Done |

### Phase View

### Phase 2

- [x] T-001 Record current `.claude/agents` symlink drift and intended final state.
- [x] T-005 Prepare validator hardening requirement for Phase 3.
- [x] T-007 Record Phase 2 planning evidence and limitations.

### Phase 3

- [x] T-002 Replace `.claude/agents` symlink with real Claude files.
- [x] T-003 Add Claude model/tool frontmatter to all Claude agent files.
- [x] T-004 Preserve mirror parity across Claude/Gemini/Codex agents.
- [x] T-006 Update governance/readiness text only where current evidence requires it.

## Approval and Safety Boundaries

- **Allowed Paths**: `T-001 through T-007` is limited to these Claude Agent Surface Restoration owners and Task-Table surfaces:
  - `docs/04.execution/tasks/2026-06-01-claude-agent-surface-restoration.md`
  - `docs/04.execution/plans/2026-06-01-claude-agent-surface-restoration.md`
  - `.claude/CLAUDE.md`
  - `docs/00.agent-governance/harness-catalog.md`
  - `docs/00.agent-governance/subagent-protocol.md`
  - `.claude/agents`
- **Forbidden Paths**: provider account settings, live agent sessions, credentials, model/runtime policy outside the parent Plan, and repository paths outside the Claude Agent Surface Restoration surfaces.
- **Approval Required**: Human approval is required before Claude Agent Surface Restoration provider configuration, model-policy promotion, remote agent action, credential access, protected-file expansion, push, merge, or publication.
- **Static Validation**: Preserve the Claude Agent Surface Restoration outcomes and limitations recorded in Verification Summary; use these recorded checks:
  - `find .claude/agents -maxdepth 1 -type f -name '*.md' | sort`
  - `rg -n "model: Gemini|Gemini 3\\." .claude/agents`
  - `bash scripts/validate-repo-quality-gates.sh .`
- **Live Validation**: DEFER — Claude Agent Surface Restoration is closed by repository-static/documentation evidence; historical live commands, if any, are not authority for a new cluster, provider, external-service, or deployment claim.
- **Secret / Vault Handling**: Use only redacted repository contracts for Claude Agent Surface Restoration; do not read or print provider tokens, auth files, memory stores, private logs, kubeconfigs, secret values, or shell history.
- **Rollback Plan**: Revert the logical Claude Agent Surface Restoration change set for `T-001 through T-007` and restore its allowed implementation/evidence paths with this Task and parent Plan; documentation rollback does not authorize live mutation.
- **Evidence Location**: Durable Claude Agent Surface Restoration evidence remains in:
  - `docs/04.execution/tasks/2026-06-01-claude-agent-surface-restoration.md`
  - `docs/04.execution/plans/2026-06-01-claude-agent-surface-restoration.md`
  - `.claude/CLAUDE.md`
  - `docs/00.agent-governance/harness-catalog.md`
  - `docs/00.agent-governance/subagent-protocol.md`

## Verification Summary

- **Test Commands**:
  - `test -d .claude/agents && test ! -L .claude/agents` — PASS
  - `find .claude/agents -maxdepth 1 -type f -name '*.md' | sort` — eight Claude agent files listed
  - `rg -n "model: Gemini|Gemini 3\\." .claude/agents` — no matches
  - `bash scripts/validate-repo-quality-gates.sh .` — PASS
  - Negative smoke in `/tmp` copy with `.claude/agents` reverted to a symlink — validator failed with `.claude/agents must be a real Claude-specific directory, not a symlink`
  - Negative smoke in `/tmp` copy with `code-reviewer` tools reduced — validator failed with `.claude/agents/code-reviewer.md tools must be 'Read, Grep, Glob, Bash'`
- **Eval Commands**:
  - `scripts/validate-repo-quality-gates.sh` now checks `.claude/agents` is not a symlink and validates Claude `model` / `tools` frontmatter.
- **Logs / Evidence Location**:
  - `.claude/agents/*.md`
  - `scripts/validate-repo-quality-gates.sh`
  - `docs/00.agent-governance/memory/progress.md`

## Traceability

- **Plan**: [../plans/2026-06-01-claude-agent-surface-restoration.md](../plans/2026-06-01-claude-agent-surface-restoration.md)
- **Runtime Baseline**: [../../../.claude/CLAUDE.md](../../../.claude/CLAUDE.md)
- **Harness Catalog**: [../../00.agent-governance/harness-catalog.md](../../00.agent-governance/harness-catalog.md)
- **Subagent Protocol**: [../../00.agent-governance/subagent-protocol.md](../../00.agent-governance/subagent-protocol.md)
