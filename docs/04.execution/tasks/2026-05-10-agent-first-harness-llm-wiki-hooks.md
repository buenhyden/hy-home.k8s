---
title: 'Task: Agent-first Harness, LLM Wiki, and Hook Contract Closure'
type: sdlc/task
status: done
owner: platform
updated: 2026-07-13
---

# Task: Agent-first Harness, LLM Wiki, and Hook Contract Closure

## Overview

This document tracks implementation and verification tasks for Harness
Engineering, Agent-first Engineering, the repo-local LLM Wiki, the hook
feedback loop, and memory ledger hardening. It records tasks derived from the
Plan in a traceable form.

## Inputs

- **Parent Spec**: not applicable; this closure does not introduce a new platform manifest or application contract.
- **Parent Plan**: [Agent-first Harness, LLM Wiki, and Hook Contract Closure Plan](../plans/2026-05-10-agent-first-harness-llm-wiki-hooks.md)

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Audit existing gateway, runtime, hook, memory, and LLM Wiki surfaces | doc | n/a | PLN-001 | Current files and dirty diff reviewed | Platform | Done |
| T-002 | Confirm generated LLM Wiki index freshness | test | n/a | PLN-002 | `bash scripts/generate-llm-wiki-index.sh --check` PASS | Platform | Done |
| T-003 | Confirm Claude/Codex runtime JSON parses | test | n/a | PLN-003 | `python3 -m json.tool` PASS for both runtime JSON files | Platform | Done |
| T-004 | Confirm hook and generator shell syntax | test | n/a | PLN-003 | `bash -n ...` PASS | Platform | Done |
| T-005 | Add explicit legacy path migration map | guardrail | n/a | PLN-004 | `document-stage-routing.md` and validator phrases updated | Platform | Done |
| T-006 | Add plan/task evidence and refresh stage indexes | doc | n/a | PLN-005 | `plans/README.md` and `tasks/README.md` include this work | Platform | Done |
| T-007 | Run repo quality gate after changes | test | n/a | PLN-001..PLN-005 | `bash scripts/validate-repo-quality-gates.sh .` PASS | Platform | Done |

### Phase View

### Phase 1

- [x] T-001 Audit existing implementation
- [x] T-002 Confirm LLM Wiki generated index
- [x] T-003 Confirm runtime JSON
- [x] T-004 Confirm hook and script syntax

### Phase 2

- [x] T-005 Add legacy path migration guard
- [x] T-006 Add plan/task evidence and indexes
- [x] T-007 Run repo quality gate

## Approval and Safety Boundaries

- **Allowed Paths**: `T-001 through T-007` is limited to these Agent-first Harness, LLM Wiki, and Hook Contract Closure owners and Task-Table surfaces:
  - `docs/04.execution/tasks/2026-05-10-agent-first-harness-llm-wiki-hooks.md`
  - `docs/04.execution/plans/2026-05-10-agent-first-harness-llm-wiki-hooks.md`
- **Forbidden Paths**: provider account settings, live agent sessions, credentials, model/runtime policy outside the parent Plan, and repository paths outside the Agent-first Harness, LLM Wiki, and Hook Contract Closure surfaces.
- **Approval Required**: Human approval is required before Agent-first Harness, LLM Wiki, and Hook Contract Closure provider configuration, model-policy promotion, remote agent action, credential access, protected-file expansion, push, merge, or publication.
- **Static Validation**: Preserve the Agent-first Harness, LLM Wiki, and Hook Contract Closure outcomes and limitations recorded in Verification Summary; use these recorded checks:
  - `bash scripts/generate-llm-wiki-index.sh --check`
  - `python3 -m json.tool .claude/settings.json`
  - `python3 -m json.tool .codex/hooks.json`
  - `bash -n docs/00.agent-governance/hooks/k8s-pre-edit.sh docs/00.agent-governance/hooks/post-validate.sh docs/00.agent-governance/hooks/session-start.sh scripts/validate-repo-quality-gates.sh scripts/generate-llm-wiki-index.sh`
- **Live Validation**: DEFER — Agent-first Harness, LLM Wiki, and Hook Contract Closure is closed by repository-static/documentation evidence; historical live commands, if any, are not authority for a new cluster, provider, external-service, or deployment claim.
- **Secret / Vault Handling**: Use only redacted repository contracts for Agent-first Harness, LLM Wiki, and Hook Contract Closure; do not read or print provider tokens, auth files, memory stores, private logs, kubeconfigs, secret values, or shell history.
- **Rollback Plan**: Revert the logical Agent-first Harness, LLM Wiki, and Hook Contract Closure change set for `T-001 through T-007` and restore its allowed implementation/evidence paths with this Task and parent Plan; documentation rollback does not authorize live mutation.
- **Evidence Location**: Durable Agent-first Harness, LLM Wiki, and Hook Contract Closure evidence remains in:
  - `docs/04.execution/tasks/2026-05-10-agent-first-harness-llm-wiki-hooks.md`
  - `docs/04.execution/plans/2026-05-10-agent-first-harness-llm-wiki-hooks.md`
  - `docs/00.agent-governance/memory/progress.md`

## Verification Summary

- **Test Commands**:
  - `bash scripts/generate-llm-wiki-index.sh --check`
  - `python3 -m json.tool .claude/settings.json`
  - `python3 -m json.tool .codex/hooks.json`
  - `bash -n docs/00.agent-governance/hooks/k8s-pre-edit.sh docs/00.agent-governance/hooks/post-validate.sh docs/00.agent-governance/hooks/session-start.sh scripts/validate-repo-quality-gates.sh scripts/generate-llm-wiki-index.sh`
  - `bash scripts/validate-repo-quality-gates.sh .`
- **Eval Commands**: not applicable; no prompt/model change is included.
- **Logs / Evidence Location**: this task document and `docs/00.agent-governance/memory/progress.md`. Evidence is repo/static and dated 2026-05-10; rerun the commands before using it for future handoff.

## Traceability

- **Plan**: [Agent-first Harness, LLM Wiki, and Hook Contract Closure Plan](../plans/2026-05-10-agent-first-harness-llm-wiki-hooks.md)
- **Governance**: [Harness Catalog](../../00.agent-governance/harness-catalog.md)
- **Governance**: [Document Stage Routing Rules](../../00.agent-governance/rules/document-stage-routing.md)
- **Reference**: [LLM WIKI Reference Index](../../90.references/llm-wiki/README.md)
