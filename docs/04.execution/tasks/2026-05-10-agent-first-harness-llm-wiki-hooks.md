---
title: 'Task: Agent-first Harness, LLM Wiki, and Hook Contract Closure'
type: task
status: done
owner: 'platform'
updated: 2026-05-10
---

# Task: Agent-first Harness, LLM Wiki, and Hook Contract Closure

## Overview (KR)

이 문서는 Harness Engineering, Agent-first Engineering, repo-local LLM Wiki, hook feedback loop, memory ledger 보강 작업의 구현·검증 작업 목록이다.
Plan에서 파생된 작업을 추적 가능하게 기록한다.

## Inputs

- **Parent Spec**: not applicable; this closure does not introduce a new platform manifest or application contract.
- **Parent Plan**: [Agent-first Harness, LLM Wiki, and Hook Contract Closure Plan](../plans/2026-05-10-agent-first-harness-llm-wiki-hooks.md)

## Working Rules

- Keep root gateways thin and route durable policy to `docs/00.agent-governance/**`.
- Keep governance/runtime files English-only.
- Keep human-facing README files Korean.
- Do not create a new runtime surface unless the matrix records a concrete gap or a human explicitly requests it.
- Treat validation evidence as a dated repo/static snapshot, not live cluster proof.

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

## Suggested Types

- `impl`
- `test`
- `eval`
- `doc`
- `ops`

## Agent-specific Types (If Applicable)

- `prompt`
- `tool`
- `memory`
- `guardrail`
- `eval`
- `observability`

## Phase View (Optional)

### Phase 1

- [x] T-001 Audit existing implementation
- [x] T-002 Confirm LLM Wiki generated index
- [x] T-003 Confirm runtime JSON
- [x] T-004 Confirm hook and script syntax

### Phase 2

- [x] T-005 Add legacy path migration guard
- [x] T-006 Add plan/task evidence and indexes
- [x] T-007 Run repo quality gate

## Verification Summary

- **Test Commands**:
  - `bash scripts/generate-llm-wiki-index.sh --check`
  - `python3 -m json.tool .claude/settings.json`
  - `python3 -m json.tool .codex/hooks.json`
  - `bash -n docs/00.agent-governance/hooks/k8s-pre-edit.sh docs/00.agent-governance/hooks/post-validate.sh docs/00.agent-governance/hooks/session-start.sh scripts/validate-repo-quality-gates.sh scripts/generate-llm-wiki-index.sh`
  - `bash scripts/validate-repo-quality-gates.sh .`
- **Eval Commands**: not applicable; no prompt/model change is included.
- **Logs / Evidence Location**: this task document and `docs/00.agent-governance/memory/progress.md`. Evidence is repo/static and dated 2026-05-10; rerun the commands before using it for future handoff.

## Related Documents

- **Plan**: [Agent-first Harness, LLM Wiki, and Hook Contract Closure Plan](../plans/2026-05-10-agent-first-harness-llm-wiki-hooks.md)
- **Governance**: [Harness Catalog](../../00.agent-governance/harness-catalog.md)
- **Governance**: [Document Stage Routing Rules](../../00.agent-governance/rules/document-stage-routing.md)
- **Reference**: [LLM WIKI Reference Index](../../90.references/llm-wiki/README.md)
