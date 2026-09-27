---
title: "Bind Claude Model and Effort"
version: "0.1.0"
type: "sdlc/task"
status: "queued"
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
| WORK-002 | VAL-CMB-001, VAL-CMB-002 | Add the Claude effort binding and overrides, and sync the projections | platform | Queued | Pending | Unit tests and validator |
| WORK-003 | VAL-CMB-003 | Observe the applied model and effort in new sessions | platform | Queued | Pending | Transcript records |

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

## Traceability

- Stable Task: `SPEC-0097-TSK-0001`

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-001](../plan.md#work-breakdown) | Done | Research above |
| [WORK-002](../plan.md#work-breakdown) | Queued | Pending |
| [WORK-003](../plan.md#work-breakdown) | Queued | Pending |
