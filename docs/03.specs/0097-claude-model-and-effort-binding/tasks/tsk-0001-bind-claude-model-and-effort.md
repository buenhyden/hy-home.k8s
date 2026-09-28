---
title: "Bind Claude Model and Effort"
version: "0.2.0"
type: "sdlc/task"
status: "completed"
owner: "platform"
updated: "2026-09-27"
layer: "specs"
artifact_id: "SPEC-0097-TSK-0001"
---

# Task: Bind Claude Model and Effort

## Overview

Execute [SPEC-0097-PLAN-0001](../plan.md). On 2026-09-27 the request owner
asked for Claude's handling of roles, agents, models, and reasoning effort to be
checked and fixed. They allowed the latest models and asked for Fable 5.1 to be
kept to the thinking and planning roles.

## Inputs

- [Owning Spec](../spec.md)
- [Owning Plan](../plan.md)
- `.agents/governance/model-selection.md`, `.agents/roles/registry.json`, and `.claude/provider.md`

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | VAL-CMB-004 | Research the subagent contract and the tool gap | platform | Done | See the research below | [Research](#research-2026-09-27) |
| WORK-002 | VAL-CMB-001, VAL-CMB-002 | Add the Claude effort binding and overrides, and sync the projections | platform | Done | 17 projections carry the resolved `model` and `effort`; only supervisor and architect bind `fable` | [Binding](#binding-2026-09-27) |
| WORK-003 | VAL-CMB-003 | Observe the applied model and effort in new sessions | platform | Done | Four roles applied their bound model and effort | [Spawn](#spawn-2026-09-27) |

## Approval and Safety Boundaries

- **Allowed Paths**: `.agents/roles/registry.json` and its schema, `scripts/validate-agent-governance.py`, `tests/test_validate_agent_registry.py`, `.agents/governance/model-selection.md`, `.claude/agents/*.md`, `.claude/provider.md`, and this package
- **Forbidden Paths**: tool scopes and permission classes; Codex bindings; user-level Claude settings
- **Approval Required**: the request owner asked for the change. Push and merge stay with the request owner.
- **Static Validation**: unit tests, the governance validator, and `python3 scripts/qa.py staged`
- **Live Validation**: new headless `claude -p --model sonnet` sessions that spawn roles
- **Secret / Vault Handling**: no credential is read or recorded
- **Rollback Plan**: revert the binding commit; the schema then requires no Claude effort
- **Evidence Location**: this Task

## Verification Summary

### Research (2026-09-27)

- **Client**: `claude 2.1.283`, native Linux build. The main session model is
  `claude-opus-5-5[1m]`.
- **Contract**: the [subagent documentation](https://code.claude.com/docs/en/sub-agents)
  lists `model` (`sonnet`, `opus`, `haiku`, `fable`, a full ID, or `inherit`)
  and `effort` (`low`, `medium`, `high`, `xhigh`, `max`) among the frontmatter
  fields.
- **Gap 1, effort**: the registry bound effort only for Codex, and the
  validator admitted only `name`, `description`, `model`, and `tools` in a Claude
  projection.
- **Gap 2, model**: the tier aliases resolve to the latest generation (`opus` to
  `claude-opus-5-5` and `sonnet` to `claude-sonnet-5`), but no role could
  depart from its tier's Claude model.
- **Gap 3, tools**: [anthropics/claude-code#80526](https://github.com/anthropics/claude-code/issues/80526)
  and [#91492](https://github.com/anthropics/claude-code/issues/91492), both
  open, record that native macOS and Linux builds from 2.1.117 removed `Grep`
  and `Glob`, moved search into Bash (`ugrep`, `bfs`), and drop the unknown
  names silently. Windows and npm installs keep both tools. This matches
  SPEC-0086, which saw a `code-reviewer` spawn get only `Read` and `Bash`. On
  native builds, docs-researcher, incident-responder, observability-reviewer,
  and supervisor therefore have no search tool. Owner: `governance-steward`,
  after a request-owner decision on granting `Bash`, which widens a permission
  class.

### Binding (2026-09-27)

- The registry gives Claude `capability_reasoning` `top: xhigh` and
  `worker: high`, which mirrors Codex. The four existing effort overrides gain
  a `claude` key with the same value: incident-responder and security-auditor
  get `high`, and doc-writer and wiki-curator get `medium`. Supervisor and
  architect declare `native_model_override.claude = fable`.
- The schema adds `claudeReasoningEffort`, requires Claude
  `capability_reasoning`, and admits `claude` keys on both override objects.
  `_bound_reasoning` takes a provider. The Claude projection check admits
  `effort` and requires it to equal the binding.
- Three new unit tests (`test_claude_declares_an_effort_for_every_tier`,
  `test_every_claude_projection_carries_its_bound_effort`, and
  `test_a_claude_effort_override_replaces_only_claude`) failed before the
  change and pass after it.
- Every model stays an alias (`fable`, `opus`, `sonnet`). No role binds
  `haiku`, because no role does work light enough for it.

### Spawn (2026-09-27)

A session already running kept its startup definitions: an `architect` spawned
from it answered `claude-opus-5-5[1m]`, which is the pre-change binding. Two new
headless sessions (`claude -p --model sonnet --allowedTools Agent`, session IDs
`178254e6-e002-4bf3-813c-6c83c1ed9353` and
`0dd6ced4-37ba-49ad-ba8b-dd13ba416c4e`) spawned roles from the changed
projections. Each row comes from the subagent transcript's own `message.model`
and `effort` fields, and its `.meta.json` names the `agentType`.

| Role | Bound model and effort | Applied model | Applied effort |
| --- | --- | --- | --- |
| architect | `fable`, `xhigh` | `claude-fable-5-1` | `xhigh` |
| governance-steward | `opus`, `xhigh` | `claude-opus-5-5` | `xhigh` |
| code-reviewer | `sonnet`, `high` | `claude-sonnet-5` | `high` |
| doc-writer | `sonnet`, `medium` | `claude-sonnet-5` | `medium` |

doc-writer applied `medium` while its parent session ran at `high`, which shows
that the role's own effort took effect rather than an inherited value. These
records prove only that the configuration applied. They say nothing about
quality or cost.

### Validation

`python3 scripts/qa.py staged` passed on each commit, and 154 agent-related
unit tests passed. Local `pre-commit run --all-files --hook-stage manual`
failed only in Gitleaks, and only on the ignored local files `.env` and
`secrets/certs/*.pem`. `ruff format` reformatted one test file, and that change
is committed.

## Traceability

- Stable Task: `SPEC-0097-TSK-0001`

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-001](../plan.md#work-breakdown) | Done | Research above |
| [WORK-002](../plan.md#work-breakdown) | Done | [Binding](#binding-2026-09-27) |
| [WORK-003](../plan.md#work-breakdown) | Done | [Spawn](#spawn-2026-09-27) |
