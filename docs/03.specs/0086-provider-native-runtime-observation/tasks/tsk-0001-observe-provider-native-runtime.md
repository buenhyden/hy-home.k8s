---
title: "Observe Provider Native Runtime"
version: "0.2.0"
type: "sdlc/task"
status: "in-progress"
owner: "platform"
updated: "2026-09-27"
layer: "specs"
artifact_id: "SPEC-0086-TSK-0001"
---

# Task: Observe Provider Native Runtime

## Overview

Own the operator-authorized native-runtime observation for Claude and Codex
that [SPEC-0072-TSK-0001](../../0072-agent-governance-and-quality-gate-consolidation/tasks/tsk-0001-consolidate-governance-and-quality-gates.md)
transferred here on 2026-09-24 rather than claiming as passed. This record is
append-only evidence of what an operator-authorized session actually observed;
it never promotes a repository-static or hosted-CI result to runtime evidence.

## Inputs

- [Owning Spec](../spec.md)
- [Owning Plan](../plan.md)
- [SPEC-0072-TSK-0001](../../0072-agent-governance-and-quality-gate-consolidation/tasks/tsk-0001-consolidate-governance-and-quality-gates.md), which recorded `WORK-009` and transferred it here
- `.claude/provider.md` and `.codex/provider.md`

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | VAL-PNRO-001, VAL-PNRO-003, VAL-PNRO-005, VAL-PNRO-007 | Obtain an operator-authorized Claude session and observe discovery, invocation/model access, sandbox enforcement, and event delivery | operator | Done | All four observed; one tool-surface finding | [Claude session](#claude-session-2026-09-27) |
| WORK-002 | VAL-PNRO-002, VAL-PNRO-004, VAL-PNRO-006, VAL-PNRO-008 | Obtain an operator-authorized Codex session and observe the same four properties | operator | Done | 002 and 006 observed; 004 not observable; 008 `DEFER` by operator choice | [Codex session](#codex-session-2026-09-27) |

## Approval and Safety Boundaries

- **Allowed Paths**: this Task, the owning Spec and Plan, and this package's index rows
- **Forbidden Paths**: live credentials, secret values, private configuration, session logs beyond the recorded client identity and result
- **Approval Required**: any native Provider session; the operator alone authorizes it. No agent may authorize, simulate, or infer it.
- **Static Validation**: none satisfies this Task's criteria; see the owning Spec's Verification Commands
- **Live Validation**: the operator-authorized native session itself, recorded per provider
- **Secret / Vault Handling**: no credential, token, or private configuration is read, printed, or recorded
- **Rollback Plan**: no mutation occurs; a recorded observation is append-only evidence and needs no rollback
- **Evidence Location**: this Task

## Verification Summary

No repository-static command exists for this Task's acceptance criteria. Each
row closes only on a dated, attributed operator-authorized session record.

**Authorization (2026-09-27).** The request owner asked in a Claude Code session
to complete or dispose of every blocked, deferred, or unstarted Stage 03 item.
For Codex they chose "run read-only, defer the hook" (chooser: request owner),
which declines a hook-trust bypass. No trust state, global setting, or
permission was changed.

### Claude session (2026-09-27)

Client `claude 2.1.283`, main model `claude-opus-5-5[1m]`, working tree
`docs/spec-0086-close-and-retention` at `fbcafca1`.

| Criterion | Action | Observed result |
| --- | --- | --- |
| VAL-PNRO-001 discovery | Compared the session's agent-type list with `.claude/agents/*.md` and the model-visible skill list with `.claude/skills/` | All 17 role projections were discovered as agent types with their declared tool lists. None of the 17 project skills is model-visible. Each has `disable-model-invocation: true`, so this is the documented behavior. Explicit `/` invocation was not exercised. |
| VAL-PNRO-003 invocation and model | Invoked the `code-reviewer` projection (`model: "sonnet"`) and asked it to report its model | Resolved to `claude-sonnet-5` ("Sonnet 5"). |
| VAL-PNRO-005 permission boundary | The same `code-reviewer` invocation (`read-only-evidence`) reported its callable tools | `Read`, `Bash`, and the hand-back tool. `Write`, `Edit`, and `MultiEdit` were withheld, so the structured-write boundary was enforced. **Finding:** the projection declares `Grep` and `Glob`, which this client does not expose (the main session has none either). Owner: `governance-steward`, to reconcile `permission_scopes` with the tools the client offers. |
| VAL-PNRO-007 hook delivery | Issued a structured `Write` to `docs/00.agent-governance/pnro-probe.md` | The hook `.claude/hooks/k8s-pre-edit.sh` received the payload, read `tool_input.file_path`, and blocked the call with `[FAIL] HOOK-PATH-RETIRED: common authority is owned by .agents/`. The file does not exist. |

### Codex session (2026-09-27)

Client `codex-cli 0.155.1`, logged in with ChatGPT. Command:
`codex exec --sandbox read-only --json -C <worktree> "<probe prompt>"`, thread
`01a0dfda-bdd0-7ec2-a387-0bc8ac2372c9`. The prompt asked for the model
identifier, the available skill names, the spawnable roles (and one
`code-reviewer` spawn), and one `touch .pnro-probe && echo WROTE`.

| Criterion | Observed result |
| --- | --- |
| VAL-PNRO-002 discovery | The session emitted `Skill descriptions were shortened to fit the skills context budget`. It listed 143 skill names, and none of the 17 project skills was among them, which matches `allow_implicit_invocation: false`. The spawnable roles were `docs_researcher`, `explorer`, `reviewer`, `default`, and `worker`. **Finding:** none of the `.codex/agents/*.toml` projections was discovered, including `code-reviewer`. Owner: the operator for project-layer trust, then `governance-steward` if the projections still stay undiscovered. |
| VAL-PNRO-004 invocation and model | Not observable. The agent reported only "GPT-6 family", with no exact identifier, and no role projection could be spawned, so the declared `gpt-5.3-codex-spark` binding was not resolved. |
| VAL-PNRO-006 sandbox enforcement | The write was denied fail-closed. The command exited `1` with `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`, and `.pnro-probe` does not exist. The sandbox refused to start the command, so this shows fail-closed setup, not a path-level write denial. |
| VAL-PNRO-008 hook delivery | `DEFER`. The request owner declined the hook-trust bypass. Next owner: the operator, for a reviewed project hook trust state; see `.codex/provider.md`. |

No credential, session log, or private configuration was read or retained.

## Traceability

- Stable Task: `SPEC-0086-TSK-0001`
- Predecessor: `SPEC-0072-TSK-0001` `WORK-009`, transferred here on 2026-09-24

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-001](../plan.md#work-breakdown) | Done | [Claude session](#claude-session-2026-09-27) |
| [WORK-002](../plan.md#work-breakdown) | Done, 004 not observable and 008 `DEFER` | [Codex session](#codex-session-2026-09-27) |
