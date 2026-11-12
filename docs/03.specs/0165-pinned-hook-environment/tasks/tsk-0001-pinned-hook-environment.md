---
title: "Pinned Hook Environment"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-12"
layer: "specs"
artifact_id: "SPEC-0165-TSK-0001"
parent_ids: ["SPEC-0165-PLAN-0001"]
---

# Task: Pinned Hook Environment

## Overview

This Task records the commit-hook environment change for [SPEC-0165](../spec.md) under its [Plan](../plan.md).

## Inputs

- **Request:** on 2026-11-12 (Asia/Seoul) the user asked for a way to make the commit-hook environment the same everywhere, and then chose the option the assistant had labelled "root fix (repository change, recommended)", answering in Korean. That answer approved no Spec bytes. The user then answered "Approve these bytes" to the SPEC-0165 question (EVD-003); that answer accepts no criterion and authorizes no push, PR or merge.
- **Base:** branch `claude/w00-v14-7-intake` after `8bdbc3fc`, open as PR #228.
- **Observed problem:** `.git/hooks/pre-commit` records `INSTALL_PYTHON=/tmp/hyhome-r10-validation/bin/python`, which is absent; `python3` on `PATH` has jsonschema 4.10.3 while the lock pins 4.26.0.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-HOOKENV-001](../spec.md#success-criteria--verification-plan) | Dispatcher change, test-first. | platform | completed | PASS | EVD-004 and EVD-007 pass; the user accepted the criterion on 2026-11-12. |
| WORK-002 | [VAL-HOOKENV-002](../spec.md#success-criteria--verification-plan) | Owner text; machine setup; real commit. | platform | completed | PASS | EVD-006 resolves EVD-005; the user accepted the criterion on 2026-11-12. |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-HOOKENV-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Pre-approval review rounds | Read-only code-reviewer that wrote none of the package; round 1 over spec.md `8542f31c…`, plan.md `33db9ff7…`; round 2 over `afd5e94a…`, `957c8b0c…`; round 3 over `1e32ceed…`, `2049388e…`; 2026-11-12 | PASS | Round 1 REJECT: one BLOCK (the trust boundary claimed more than it checked: no refusal inside the checkout, no owner check, only two paths mode-checked) and seven FIXes (unset should fail; pinned set overstated; check `python3` and `pre-commit`; empty value and scopes; PATH scope mechanism; testable cases; approval receipt). Round 2 APPROVE with four FIXes (umask 002, recursive check, worktree boundary, synthetic test environment). Round 3 APPROVE with three NOTEs, two applied to the Spec. | no | none |
| EVD-002 | [VAL-HOOKENV-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"5de6677c79086ec6b7e7226a79ee479996942ef15dfe853647524334f1ad0813","plan_sha256":"2049388e967f41e66cf73225a336817e157d841872f27d0d418858ef256b739f"} | PASS | Same reviewer, round 4, 2026-11-12: both hashes matched; only the two NOTE edits changed since round 3; verdict APPROVE, no BLOCK or FIX. One NOTE left as implementation detail: the repair message wording for the `umask 002` `__pycache__` case. The reviewer is independent of the author; this row records a review, not a second approval. | yes | none |
| EVD-003 | [VAL-HOOKENV-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve these bytes to the SPEC-0165 question naming spec.md 5de6677c and plan.md 2049388e dated 2026-11-12 Asia/Seoul","review_ref":"EVD-002","scope":["SPEC-0165","SPEC-0165-PLAN-0001"],"reviewed_spec_sha256":"5de6677c79086ec6b7e7226a79ee479996942ef15dfe853647524334f1ad0813","reviewed_plan_sha256":"2049388e967f41e66cf73225a336817e157d841872f27d0d418858ef256b739f","validity":"confirmed","revocation":"none"} | PASS | No message UUID was supplied or invented. This receipt accepts no criterion and authorizes no push, PR or merge. | yes | none |
| EVD-004 | [VAL-HOOKENV-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Dispatcher regression tests | `python3 tests/test_chained_git_hooks.py` after `b4504f13`, before and after the dispatcher change; `shellcheck`, `bash -n`, `ruff check` and `ruff format`; 2026-11-12 | PASS | RED with the old dispatcher: 16 tests, 20 failing subtests, every one a new case (unset, empty, relative, missing, inside the checkout, inside another worktree, no `python3`, no `pre-commit`, group- or other-writable directory, `bin`, `pre-commit` or `site-packages` file, a `umask 002` build, foreign owner through a `find` shim, `HOOK-CONFIG` through a `git` shim, the global and workspace `PATH` for `pre-commit` and `commit-msg`, sibling prefix, symbolic link and `~` expansion); the 9 existing tests passed with the synthetic environment in `setUp`. GREEN: 16 OK. A first test fix cleared the hook log that the worktree setup commit wrote. `shellcheck` clean after six info findings were fixed in code; no rule was disabled. | yes | none |
| EVD-005 | [VAL-HOOKENV-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Exact-index QA and commit hooks without the scratch environment | First commit attempt of the implementation from a shell whose `PATH` has no scratch environment (`python3` = `/usr/bin/python3`, jsonschema 4.10.3), option set to `~/.venvs/hyhome-validation` built under `umask 022` from the lock; 2026-11-12 | FAIL | The hook ran every Python gate with `/home/hyunyoun/.venvs/hyhome-validation/bin/python3`; 11 of 12 gates passed and `selected-style` failed on `shellcheck` (SC2016, SC2015, SC2094 in the dispatcher). No commit was made. | yes | none |
| EVD-006 | [VAL-HOOKENV-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Exact-index QA and commit hooks without the scratch environment | Commit `beae88a1` (tree `522121e9d4ef957f652a0815efe7c6dc011af791`) from the same shell after the `shellcheck` fixes; then the dispatcher run in a scratch repository whose workspace `pre-commit` prints `command -v python3` and the jsonschema version, with the option unset (`GIT_CONFIG_GLOBAL=/dev/null`) and set; 2026-11-12 | PASS | Staged QA Snapshot, Commitizen and the commit-message exception hooks passed. Probe: unset gives `HOOK-ENV` and the setup commands with a literal `$HOME`; set gives `/home/hyunyoun/.venvs/hyhome-validation/bin/python3` and jsonschema 4.26.0. `git.md` 2.5.0 and `scripts/README.md` 0.12.0 state the option, setup, boundary and the pinned and unpinned sets. | yes | EVD-005 |
| EVD-007 | [VAL-HOOKENV-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Core-diff checklist | Diff `b4504f13..beae88a1` (4 files, 310 insertions, 12 deletions); risk class `high` (hook path); 2026-11-12 | PASS | Acceptance matches VAL-HOOKENV-001 (EVD-004) and VAL-HOOKENV-002 (EVD-006). Only the Spec's files changed; `.pre-commit-config.yaml`, the lock, `scripts/qa.py`, workflows and the validation registry are unchanged. Changed protected path: an unset or invalid option now blocks the workspace hook (`HOOK-ENV`, exit 2) before any hook runs; the global hook keeps the caller's `PATH`; order, first non-zero status, pre-push payload, missing, non-executable, recursion and duplicate handling are unchanged and still tested. No permission or trigger changed; no check removed or weakened. No secret. Recovery: revert `beae88a1`. Findings: NOTE, every clone with `core.hooksPath` set must set the option before its next commit; the message prints the commands. NOTE, the Spec's limits stand (no lock comparison, parent directories, base interpreter libraries). No BLOCK or FIX open. | yes | none |
| EVD-008 | [VAL-HOOKENV-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Manual package-exit decision freeze | This package's `spec.md`, `plan.md` and Task; the consumers named below; the user's 2026-11-12 exit authority; Git-history-only method | PASS | The consumer, preservation, hold, authority and method decision is frozen below before this package's final source commit. Each file's committed `commit:path`, retained-ref reachability, temporary restoration and byte comparison are recorded in REQ-0003 Archived Lineage before deletion. An unresolved condition defers the affected deletion. | no | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-HOOKENV-001](../spec.md#success-criteria--verification-plan) | accepted | EVD-004, EVD-007 | Accepted by the user on 2026-11-12 (direct answer "Accept both" to the SPEC-0165 acceptance question) | platform |
| [VAL-HOOKENV-002](../spec.md#success-criteria--verification-plan) | accepted | EVD-006 | Accepted by the user on 2026-11-12 (direct answer "Accept both" to the SPEC-0165 acceptance question) | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: the files the Spec names, this package, `docs/03.specs/README.md`, `.secrets.baseline` (this Task's reviewed digests only)
- **Forbidden Paths**: `.pre-commit-config.yaml`, `.github/**`, `scripts/qa.py`; `core.hooksPath` and the generated `.git/hooks` files stay as they are
- **Approval Required**: Spec and Plan bytes; criterion acceptance; any push, PR or merge
- **Static Validation**: `git-hook-chain-regressions`, `bash -n`, strict document validators, staged lifecycle check, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface
- **Secret / Vault Handling**: no secret read or printed
- **Rollback Plan**: revert the implementation commit; after the revert the option is no longer read and can be unset
- **Evidence Location**: this Task

### Frozen Package Disposition Decision

- **Target and method**: After the final source commit, retire only this Stage 03 package (`spec.md`, `plan.md` and this Task) through Git-history-only recovery. No other document is selected.
- **Consumers and preservation**: The durable contract is promoted to Git policy 2.5.0 (Promotion row); the dispatcher, its tests and `scripts/README.md` carry the rest. Current consumers: the Stage 03 README entry, this Task's `.secrets.baseline` entries and the dispatcher's header comment, which now names Git policy instead of this package. SPEC-0161's mentions are historical text and stay.
- **Hold and authority**: The current repository documents and the user's request identify no hold on these files. The user's explicit 2026-11-12 answer "Exit SPEC-0165 now" is the disposition authority. If a hold or unmet consumer is identified before deletion, the affected deletion is deferred and its source kept. Remote retention is not inferred from local refs.
- **Proof handoff**: This Task freezes the decision before its final source commit. After that commit, each file's exact `commit:path`, blob availability, reachability from the retained local ref and a temporary byte comparison with the source still in the tree are recorded in REQ-0003 Archived Lineage before any file is deleted. This Task cannot contain that proof without changing its own bytes.

## Verification Summary

The Spec and Plan are approved (EVD-002, EVD-003). WORK-001 passes (EVD-004, checklist EVD-007); WORK-002 passes on commit `beae88a1` made without the scratch environment (EVD-006 resolves EVD-005). The durable contract is promoted to Git policy 2.5.0. The user accepted both criteria on 2026-11-12. Risk class `high` (hook path).
