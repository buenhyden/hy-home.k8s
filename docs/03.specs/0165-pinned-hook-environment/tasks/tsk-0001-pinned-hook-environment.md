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
| WORK-001 | [VAL-HOOKENV-001](../spec.md#success-criteria--verification-plan) | Dispatcher change, test-first. | platform | ready | NOT_RUN | Spec and Plan approved (EVD-002, EVD-003); implementation next. |
| WORK-002 | [VAL-HOOKENV-002](../spec.md#success-criteria--verification-plan) | Owner text; machine setup; real commit. | platform | ready | NOT_RUN | Waits for WORK-001. |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-HOOKENV-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Pre-approval review rounds | Read-only code-reviewer that wrote none of the package; round 1 over spec.md `8542f31c…`, plan.md `33db9ff7…`; round 2 over `afd5e94a…`, `957c8b0c…`; round 3 over `1e32ceed…`, `2049388e…`; 2026-11-12 | PASS | Round 1 REJECT: one BLOCK (the trust boundary claimed more than it checked: no refusal inside the checkout, no owner check, only two paths mode-checked) and seven FIXes (unset should fail; pinned set overstated; check `python3` and `pre-commit`; empty value and scopes; PATH scope mechanism; testable cases; approval receipt). Round 2 APPROVE with four FIXes (umask 002, recursive check, worktree boundary, synthetic test environment). Round 3 APPROVE with three NOTEs, two applied to the Spec. | no | none |
| EVD-002 | [VAL-HOOKENV-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"5de6677c79086ec6b7e7226a79ee479996942ef15dfe853647524334f1ad0813","plan_sha256":"2049388e967f41e66cf73225a336817e157d841872f27d0d418858ef256b739f"} | PASS | Same reviewer, round 4, 2026-11-12: both hashes matched; only the two NOTE edits changed since round 3; verdict APPROVE, no BLOCK or FIX. One NOTE left as implementation detail: the repair message wording for the `umask 002` `__pycache__` case. The reviewer is independent of the author; this row records a review, not a second approval. | yes | none |
| EVD-003 | [VAL-HOOKENV-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve these bytes to the SPEC-0165 question naming spec.md 5de6677c and plan.md 2049388e dated 2026-11-12 Asia/Seoul","review_ref":"EVD-002","scope":["SPEC-0165","SPEC-0165-PLAN-0001"],"reviewed_spec_sha256":"5de6677c79086ec6b7e7226a79ee479996942ef15dfe853647524334f1ad0813","reviewed_plan_sha256":"2049388e967f41e66cf73225a336817e157d841872f27d0d418858ef256b739f","validity":"confirmed","revocation":"none"} | PASS | No message UUID was supplied or invented. This receipt accepts no criterion and authorizes no push, PR or merge. | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-HOOKENV-001](../spec.md#success-criteria--verification-plan) | pending | none | Dispatcher tests before and after | platform |
| [VAL-HOOKENV-002](../spec.md#success-criteria--verification-plan) | pending | none | Owner text and a real commit without the scratch environment | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: the files the Spec names, this package, `docs/03.specs/README.md`, `.secrets.baseline` (this Task's reviewed digests only)
- **Forbidden Paths**: `.pre-commit-config.yaml`, `.github/**`, `scripts/qa.py`; `core.hooksPath` and the generated `.git/hooks` files stay as they are
- **Approval Required**: Spec and Plan bytes; criterion acceptance; any push, PR or merge
- **Static Validation**: `git-hook-chain-regressions`, `bash -n`, strict document validators, staged lifecycle check, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface
- **Secret / Vault Handling**: no secret read or printed
- **Rollback Plan**: revert the implementation commit; after the revert the option is no longer read and can be unset
- **Evidence Location**: this Task

## Verification Summary

The Spec and Plan are approved (EVD-002, EVD-003); implementation has not started. Risk class `high` (hook path).
