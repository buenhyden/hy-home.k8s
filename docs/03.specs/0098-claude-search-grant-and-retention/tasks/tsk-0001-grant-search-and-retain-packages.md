---
title: "Grant Search and Retain Packages"
version: "0.2.0"
type: "sdlc/task"
status: "in-progress"
owner: "platform"
updated: "2026-09-27"
layer: "specs"
artifact_id: "SPEC-0098-TSK-0001"
---

# Task: Grant Search and Retain Packages

## Overview

Execute [SPEC-0098-PLAN-0001](../plan.md). On 2026-09-27 the request owner
asked for search to be allowed for the Claude roles without it, and for the
Stage 03 packages waiting for archive to be tidied up.

## Inputs

- [Owning Spec](../spec.md)
- [Owning Plan](../plan.md)
- [ADR-0040](../../../02.architecture/decisions/0040-archive-reappraisal-and-verifiable-sources.md)
- `.agents/roles/registry.json`, `.claude/provider.md`, and `.agents/governance/approval-and-safety.md`

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | VAL-CSR-001, VAL-CSR-002 | Grant `Bash` and restate the two guardrails | platform | Done | Four scopes and projections carry `Bash`; two guardrails restated | [Grant](#grant-2026-09-27) |
| WORK-002 | VAL-CSR-004 | Retain SPEC-0095, SPEC-0096, and SPEC-0097 | platform | Queued | Pending | Lifecycle and archive gates |
| WORK-003 | VAL-CSR-003 | Observe the scopes in a new session and close | platform | Done | All four roles received `Bash` | [Session](#session-2026-09-27) |

## Approval and Safety Boundaries

- **Allowed Paths**: `.agents/roles/registry.json`, the four Claude projections, `.agents/roles/incident-responder.md`, `.agents/roles/observability-reviewer.md`, `tests/test_agent_governance.py`, `.claude/provider.md`, the three packages as whole units, `docs/98.archive/README.md`, their current citations, and this package
- **Forbidden Paths**: Codex projections and bindings; the content of any retained body or frozen record; credentials and cluster state
- **Approval Required**: the request owner asked for both changes. Push and merge stay with the request owner.
- **Static Validation**: unit tests, the governance validator, `python3 scripts/qa.py staged`, the archive contract tests, and the archive cutover gate
- **Live Validation**: a new headless Claude session that spawns the changed roles
- **Secret / Vault Handling**: no credential is read or recorded
- **Rollback Plan**: revert the grant commit or the move commit; Git restores every original path and scope
- **Evidence Location**: this Task

## Verification Summary

### Survey (2026-09-27)

| Unit | Members | Class | Current consumers |
| --- | --- | --- | --- |
| SPEC-0095 | Spec, Plan, and one Task done | `completed` | REQ-0003, the Stage 03 index |
| SPEC-0096 | Spec, Plan, and one Task done | `completed` | REQ-0003, `.codex/provider.md`, the Stage 03 index |
| SPEC-0097 | Spec, Plan, and one Task done | `completed` | REQ-0003, `.claude/provider.md`, SPEC-0098, the Stage 03 index |

### Grant (2026-09-27)

- The Claude `read-only-research` and `orchestration` scopes gain `Bash`.
  incident-responder and observability-reviewer drop their
  `native_scope_override`, so they resolve the `read-only-evidence` default,
  which already carries `Bash`. Codex is unchanged.
- Both role bodies now confine the shell to read-only repository search and
  keep their prohibition on live state, stated as policy.
- `ReadOnlyShellScopeTests` replaces the two tests that pinned the no-shell
  roles with three: every resolved Claude scope carries `Bash`, every
  projection carries it, and the two roles state the search-only limit. Before
  the change they failed for exactly the four roles, 10 subtests in all. After
  it they pass.
- 155 agent-related unit tests ran, and one failed:
  `test_equal_size_same_inode_content_restore_fails_closed`. It also failed in
  two of three runs on the unchanged tree, so it is a pre-existing timing
  failure, not a result of this change.

### Session (2026-09-27)

A new headless session (`claude -p --model sonnet --allowedTools Agent`,
`claude 2.1.283`, session `715521c6-a978-4034-800c-d9dcc1d4f2d7`) spawned each
changed role and asked for its callable tools:

| Role | Declared `tools` | Reported tools |
| --- | --- | --- |
| docs-researcher | `Read, Grep, Glob, Bash, WebFetch, WebSearch` | `Read, Bash, WebFetch, WebSearch` |
| supervisor | `Read, Grep, Glob, Bash, Task` | `Read, Bash, Agent` |
| incident-responder | `Read, Grep, Glob, Bash` | `Read, Bash` |
| observability-reviewer | `Read, Grep, Glob, Bash` | `Read, Bash` |

Each role now has `Bash` and so can search. The client dropped `Grep` and
`Glob`, as recorded for native builds, and exposed `Task` under its current
name, `Agent`. These rows are the agents' own reports. The withheld write tools
match SPEC-0086, which observed them from the same kind of spawn.

## Traceability

- Stable Task: `SPEC-0098-TSK-0001`

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-001](../plan.md#work-breakdown) | Done | [Grant](#grant-2026-09-27) |
| [WORK-002](../plan.md#work-breakdown) | Queued | Pending |
| [WORK-003](../plan.md#work-breakdown) | Done | [Session](#session-2026-09-27) |
