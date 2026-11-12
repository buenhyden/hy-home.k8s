---
title: "Pinned Hook Environment Plan"
version: "1.0.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-12"
layer: "specs"
artifact_id: "SPEC-0165-PLAN-0001"
parent_ids: ["SPEC-0165"]
---

# Pinned Hook Environment Implementation Plan

## Global Constraints

This approved work order follows the [approved Spec](spec.md) and inherits all of its boundaries. It adds one constraint: only the files the Spec names change.

## Overview

Make the hook dispatcher run the workspace hook inside the validation environment named by a Git option, and document the setup. [Task 0001](tasks/tsk-0001-pinned-hook-environment.md) owns execution and evidence.

## Context

SPEC-0161 to SPEC-0164 committed only with a session scratch environment first on `PATH`, because the workspace hook's checks run `python3` from `PATH` and the pre-commit interpreter recorded at install time is gone. SPEC-0161 handed the commit-time environment gap to W06; the user asked on 2026-11-12 to fix it now. This branch continues `claude/w00-v14-7-intake` after `8bdbc3fc`, which is open as PR #228. [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) is unchanged; no ADR changes.

## Goals & In-Scope

- Dispatcher option check and `PATH` selection, test-first.
- Git policy hook paragraph and `scripts/README.md` setup text.
- This machine's environment and option as Task evidence, then a real commit without the scratch environment.

## Non-Goals & Out-of-Scope

- Changes to `.pre-commit-config.yaml`, the lock, `scripts/qa.py` or hosted workflows.
- An installer script; the setup is the documented commands that the repair message also prints.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-HOOKENV-001](spec.md#success-criteria--verification-plan) | Dispatcher change, test-first. | Approved Spec and Plan. | [Task 0001](tasks/tsk-0001-pinned-hook-environment.md) | Dispatcher tests before and after; the `git-hook-chain-regressions` gate. |
| WORK-002 | [VAL-HOOKENV-002](spec.md#success-criteria--verification-plan) | Owner text; machine setup; real commit. | WORK-001. | [Task 0001](tasks/tsk-0001-pinned-hook-environment.md) | Exact-index QA and commit hooks without the scratch environment. |

## Verification Plan

- Show the new dispatcher cases failing before the change, then passing; the existing cases gain a synthetic environment in `setUp` and keep their assertions.
- Run the `git-hook-chain-regressions` gate, `bash -n` and the staged QA selection.
- Record the risk class (`high`: hook path) and the core-diff checklist. The changed hook behavior is the one protected path that changes: an unset or invalid option now blocks the workspace hook. No permission or trigger changes.
- Commit WORK-002 with the option set and the scratch environment removed from `PATH`.

## Risks & Mitigations

- **Every clone with `core.hooksPath` set fails its next commit until the option is set.** Mitigation: the `HOOK-ENV` message prints the setup commands, including `umask 022`; Git policy documents the global setting.
- **A writable or foreign environment could run another account's code.** Mitigation: a recursive owner and mode check over the whole environment and the interpreter target, and refusal inside any worktree; parent directories stay a recorded limit.
- **A stale environment passes.** Mitigation: Git policy says to rebuild it when the lock changes; a lock-hash marker is a possible later change.
- **Shell validators still use the closed system `PATH`.** Mitigation: the Spec states the pinned and unpinned sets; their library identity stays observed separately.
- **The global hook could change behavior.** Mitigation: the prefix is set on the workspace hook command only, and a test checks the global hook's `PATH`.

## Completion Criteria

Both criteria need PASS evidence, no unresolved required failure and the operator's acceptance.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| Commit hooks run with the validation environment named by `hyhome.validationVenv` | [Git policy](../../../.agents/governance/git.md) | Hook connection paragraph |
