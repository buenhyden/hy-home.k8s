---
title: "Resolve Deferred Conflicts"
version: "0.2.0"
type: "sdlc/task"
status: "done"
owner: "platform"
updated: "2026-09-25"
layer: "specs"
artifact_id: "SPEC-0089-TSK-0001"
---

# Task: Resolve Deferred Conflicts

## Overview

Execute [SPEC-0089-PLAN-0001](../plan.md). The request owner asked on
2026-09-25 for the SPEC-0088 deferrals to be resolved and for conflicting open
packages to be withdrawn, cleaned up, or corrected. Push, merge, Stage 98
moves, and live actions are not authorized.

## Inputs

- [Owning Spec](../spec.md)
- [Owning Plan](../plan.md)
- [SPEC-0088 Task](../../0088-operations-corpus-convergence/tasks/tsk-0001-converge-operations-corpus.md)

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | VAL-DCR-004, VAL-DCR-005 | Survey the deferrals and open packages | platform | Done | Survey below | This Task |
| WORK-002 | VAL-DCR-001, VAL-DCR-002 | Covered gates and English-first scope | platform | Done | `coveredBy` and `SURFACE-COVERED-BY` added test-first; English-first checks current plans and Tasks | Focused tests and staged QA |
| WORK-003 | VAL-DCR-003 | Correct ADR-0031 and AD-0006 | platform | Done | Spec 0054 closure and the role registry path stated | Link gate and staged QA |
| WORK-004 | VAL-DCR-005 | Withdraw SPEC-0049 and update its consumers | platform | Done | Spec and Plan withdrawn; seven Tasks opened for cancellation; REQ-0003, REQ-0004, AD-0007 and three indexes updated | Lifecycle and link gates |
| WORK-005 | VAL-DCR-005, VAL-DCR-006 | Cancel SPEC-0049 Tasks, record evidence, and close | platform | Done | Seven Tasks cancelled; package closed | Full QA below |

## Approval and Safety Boundaries

- **Allowed Paths**: `scripts/validate-affected-surfaces.py`, `scripts/validation/`, `scripts/README.md`, the tests they own, `docs/01.requirements/`, `docs/02.architecture/`, `docs/03.specs/`
- **Forbidden Paths**: `gitops/`, `infrastructure/`, `.github/`, `docs/98.archive/`, and the Stage 99 registry
- **Approval Required**: push, pull request, merge, the retirement move of SPEC-0049, and any live action
- **Static Validation**: focused tests, document gates, staged QA per commit, and full QA on the final tree
- **Live Validation**: DEFER; the Headlamp render is a local chart render, not a cluster read
- **Secret / Vault Handling**: no secret value is read
- **Rollback Plan**: revert each local commit
- **Evidence Location**: this Task

## Verification Summary

### Survey (2026-09-25, `main` at `a008aa67`)

| Item | Finding | Disposition |
| --- | --- | --- |
| Archive gate double run | `unit-tests` discovers the six modules that `archive-contract-tests` runs, and `full` and the `all-files` and `ci` lanes selected both. The coverage invariant required every gate in `full` | Resolve: `coveredBy` declaration and its invariant |
| English-first scope | The rule checked only `spec.md`; its plan and Task globs named the retired Stage 04 tree. The Korean SPEC-0008 plan and Task are `done` | Resolve: check current plans and Tasks, skip terminal states by registry class |
| ADR-0031, AD-0006 | ADR-0031 calls Spec 0054 active and names `.agents/registry.json`; AD-0006 calls TSK-0013 unfinished. Spec 0054 and TSK-0013 are `done` in `completed/`, and the registry is `.agents/roles/registry.json` | Resolve: factual correction |
| RUN-0004 Headlamp objects | `helm template` of the pinned chart `headlamp` `0.41.0` with the repository values renders ClusterRoleBinding `headlamp-admin` to `cluster-admin` and ServiceAccount `headlamp` | Confirmed; no change |
| SPEC-0008 | Spec active as the current platform contract; Plan and Task `done`. No statement contradicts the tree or SPEC-0088 | Keep |
| SPEC-0086 | Draft, operator-only native observation; consistent with its closed predecessor SPEC-0072 and the provider notes | Keep |
| SPEC-0049 | Draft with seven queued Tasks. It waits on Spec 0048, which was withdrawn and retired; plans a Traefik validator whose subject ADR-0043 retired; names a `.agents/contracts/` location the layout does not have; and treats `conftest` as optional though `policy-gates` requires it. Its own 2026-09-24 note says it cannot activate without a new plan | Withdraw; record the unowned gap at REQ-0004 |

The request owner's 2026-09-24 choice to keep SPEC-0049 for a re-plan is
superseded by the 2026-09-25 instruction to withdraw conflicting packages. The
open scope it named (VAL-PVSE-001 to 003 and 005 to 008: render, schema,
policy, secret, shell-fixture, image, and tool-evidence lanes) has no
validator and stays a requirement gap under REQ-0004-FR-0008 and
REQ-0004-FR-0010, for a new package to plan from current authority.

### Results

| Commit | Scope |
| --- | --- |
| `b5f16aaf` | Propose this package and record the survey |
| `6d197774` | `coveredBy` and `SURFACE-COVERED-BY`; English-first scope by registry state |
| `f1304d01` | ADR-0031 and AD-0006 corrections |
| `12247313` | SPEC-0049 Spec and Plan withdrawn; consumers updated |
| Closing commit | SPEC-0049 Tasks cancelled; this package closed |

- **Staged QA**: passed for each commit over its exact index.
- **Full QA** on `12247313`: every gate passed except three that fail for
  environment reasons. `archive-cutover` and two `unit-tests` cases need
  Gitleaks, which this host lacks. `pre-commit` is not on the runner's trusted
  `PATH`. `test_escaped_descendant_is_failed_without_post_reap_group_signal`
  and `test_file_reader_rejects_changes_during_read` also fail on this host;
  the second fails identically on the pre-work baseline `8076d374~1`.
  `test_equal_size_same_inode_content_restore_fails_closed` failed once and
  passed three isolated reruns, so it is recorded as flaky, not as a
  regression.
- **Hosted `ci-summary`**: DEFER; not observed, and local results do not
  establish it.
- **Live validation**: DEFER; no cluster read or mutation.
- **Deferral**: the move of SPEC-0049 into `98.archive/retired/` needs its
  withdrawal commit on the default branch. Next owner: the request owner, after
  push authorization.
- **Remote note**: the request owner pushed `origin/main` to `4b1d69f6` and
  then to `12247313`, and approved the prior work on 2026-09-25. This session
  pushed nothing.
  With `12247313` on the default branch, the precondition for the SPEC-0049
  retirement move appears met, but the move stays out of this round's scope.
- **Rollback**: revert the local commits in reverse order.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-001](../plan.md#work-breakdown) | Survey recorded | This Task |
| [WORK-002](../plan.md#work-breakdown) | Covered gates and English-first scope resolved | Results above |
| [WORK-003](../plan.md#work-breakdown) | Architecture corrected | Results above |
| [WORK-004](../plan.md#work-breakdown) | SPEC-0049 withdrawn | Results above |
| [WORK-005](../plan.md#work-breakdown) | Tasks cancelled; package closed | Results above |
