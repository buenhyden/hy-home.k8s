---
title: "Task Artifact Cleanup Task"
version: "0.1.0"
type: "sdlc/task"
status: "in-progress"
owner: "platform"
updated: "2026-11-24"
artifact_id: "SPEC-0238-TSK-0001"
parent_ids: ["SPEC-0238-PLAN-0001"]
---

# Task: Task Artifact Cleanup

## 문서 개요

### 목적과 독자

This Task records the P15 execution and evidence for the [Plan](../plan.md)
and [Spec](../spec.md). The operator and reviewers use it to separate code
and rule changes, local deletions and criterion acceptance.

### 책임과 적용 범위

WORK-001 serves AC-0001 through AC-0003. This Task owns P15 work state,
results and criterion decisions.

## 내용 계약

### 입력과 전제

The operator entered `prompts/P15-CLEANUP.md` from package
`workspace_governance_remediation_1_2_0_20261123` (`package_version: 1.2.0`)
on 2026-11-24, authorizing bounded implementation, verification and
commit, push, pull request and merge. Intake found branch `main` at
`a4968ee5e81f15a47151672b6dbaf4081eac3ea3` with a clean worktree. The
operator approved deleting `_workspace/workspace_governance_remediation_1_1_0_20261120/`
in this session. Earlier packages are not re-executed.

### 본문과 규칙

#### Scope

##### Objective and Parent

WORK-001 executes the [Plan work unit](../plan.md#work-units) for the three
[Spec criteria](../spec.md#criteria).

##### Inputs and Authority

The current user P15 message is the scoped request reference; EVD-001
records the execution receipt. The Spec and Plan stay `draft`; the receipt
grants no formal approval or criterion acceptance.

- **Allowed Paths**: the [Plan WORK-001](../plan.md#work-units) write scope, this session's scratch area and the approved 1.1.0 package.
- **Forbidden Paths**: persistent stores, other workspaces' timers and material, `sessions/`, the 1.2.0 package, other repositories, the user's provider configuration, and P16–P17.
- **Approval Required**: the 1.1.0 package deletion, approved; recursive deletion is denied in this session's settings, so the operator runs it.
- **Static Validation**: analysis regressions and staged QA.
- **Live Validation**: listing of the scratch area, `_workspace/` and the user timers.
- **Secret / Vault Handling**: no secret is read or printed.
- **Rollback Plan**: revert the commit; deleted untracked material is not recoverable, as accepted.
- **Evidence Location**: this Task's Results.

#### Execution Log

##### Work Performed

The `install_timer` branch that retired the unnamed legacy unit is removed:
the legacy unit had been retired on this host in P10 and no clone still has
one, so it had no consumer. Its test is rewritten to the current contract:
only this clone's named timer and service are written and enabled, and any
other unit, even an unnamed one running this checkout, is left alone.
CTX-R023 drops its retirement sentence. QUAL-R025 now sorts temporary from
persistent material at the end of a task, limits deletion to what the task
made inside the checkout or its scratch area, excludes links, mounts and
host-wide pruning, requires an owner, resume point and deletion condition for
kept recovery material, and keeps an input package until its last reading
prompt is finished and its deletion approved. The work lifecycle's
Completion step 3 applies it. This session's scratch area, holding P07 VM
logs and journals, R01 trace helpers, QA logs and a Codex refusal log whose
facts are in their Tasks, was emptied with plain file removal.

##### Blockers and Decisions

No tracked file, check or command reads an input package: the only package
names in tracked files are recorded input references inside Task evidence,
so nothing had to move before P17. Kept as persistent: `.workspace-memory/`
stores including the set-aside `forecast.prerelease.sqlite3` trial store
(P17 resets baselines), `.workspace-test/parallel/locks`, the timers
`hy-home-k8s-session-analysis-83ced050` and another workspace's
`hy-home-session-analysis-40ae7a89c683`, the September `sessions/` exports,
which this work did not make, the six tracked `_workspace` READMEs and the
1.2.0 package for P16 and P17. The 1.1.0 package deletion needs recursive
removal, which this session's settings deny; it is handed to the operator as
`rm -rf _workspace/workspace_governance_remediation_1_1_0_20261120` and is
recorded when observed.

##### Lifecycle Traceability

| Item | Upstream criterion | Result | Evidence |
| --- | --- | --- | --- |
| WORK-001 | [AC-0001](../spec.md#criteria), [AC-0002](../spec.md#criteria), [AC-0003](../spec.md#criteria) | DEFER | Regressions pass (EVD-003); scratch emptied and persistent material kept (EVD-004); the 1.1.0 package deletion awaits the operator's command |

#### Verification Evidence

##### Results

| Evidence ID | Criteria | Work Unit | Method | Input | Tool and Config | Command | Exit | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [AC-0001](../spec.md#criteria), [AC-0002](../spec.md#criteria), [AC-0003](../spec.md#criteria) | WORK-001 | observation | {"actor":"user","approval_ref":"Current human P15-CLEANUP.md request of 2026-11-24 in this conversation for package workspace_governance_remediation_1_2_0_20261123, bounded implementation, verification and commit/push/PR/merge, with the user's answer approving deletion of the 1.1.0 package","scope":["SPEC-0238","SPEC-0238-PLAN-0001","SPEC-0238-TSK-0001"],"reviewed_spec_sha256":"31477abd3a1173df79c9035d06d7e70b34c386d35d8e776028a8688f3843d498","reviewed_plan_sha256":"5131460cb3b4db34dbe543804dcf7cf576b50840963ca2b8b79f78dbdfbd8b83","request_revision":"73747e20a6737c2b16e915a94adf144ab533eeeeb970782dc97b3624e2e7e13e","validity":"confirmed","revocation":"none"} | Current trusted human request; request revision is the validator-defined digest of this Task's scope and work items; exact draft parent hashes | Scoped execution approval | none | PASS | Records the current P15 execution scope only; no formal Spec or Plan approval or criterion acceptance follows | true | none |
| EVD-002 | [AC-0001](../spec.md#criteria) | WORK-001 | automated | The install test rewritten to the current contract, before the code change | Pinned validation venv, `unittest` | `python -m unittest tests.test_session_analysis` | 1 | FAIL | Failing-first: the new install test failed because the legacy branch still disabled and deleted the unnamed unit | false | none |
| EVD-003 | [AC-0001](../spec.md#criteria) | WORK-001 | automated | Working tree after the branch removal | Pinned validation venv, `unittest`; Ruff | `python -m unittest tests.test_session_analysis tests.test_work_observe`; `ruff check`; `ruff format --check` | 0 | PASS | analysis 31 and join 4 tests OK; no `legacy` reference remains in the module; Ruff clean | true | none |
| EVD-004 | [AC-0003](../spec.md#criteria) | WORK-001 | observation | Local host, 2026-11-24 | `systemctl --user list-unit-files`, `git grep`, `ls` | Unit listing; tracked search for package paths; scratch listing before and after plain `rm` and `rmdir` | 0 | PASS | No unnamed legacy unit exists; the two named timers remain; no tracked link, command or check reads a package; the scratch area went from 3.5 MiB to empty; `.workspace-memory/`, `.workspace-test/parallel/locks`, `sessions/` and the 1.2.0 package are unchanged | true | none |
| EVD-005 | [AC-0001](../spec.md#criteria), [AC-0002](../spec.md#criteria), [AC-0003](../spec.md#criteria) | WORK-001 | observation | Pull request #368, head `6428acd6`, the two P15 commits cherry-picked onto `main@071bca6b` after pull request #364 could not merge | GitHub Actions CI run 45374569897 | Hosted pull request checks | 0 | PASS | CI, Labeler and Greeting runs completed with success; the hosted checks cover the changed analysis module and its regressions and the quality and lifecycle rule texts | true | none |

##### Resolution Links

EVD-002 was a planned failing-first result, not a required failure; EVD-003
shows the passing state.

#### Acceptance Decision

##### Criterion Decisions

| Criterion | Intent | Acceptance | Evidence | Decision | Accepted By | Current Owner | Reassigned To |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [AC-0001](../spec.md#criteria) | accept | accepted | EVD-003, EVD-005 | User message of 2026-11-24 in this session accepting SPEC-0238 AC-0001 to AC-0003 | user | platform | none |
| [AC-0002](../spec.md#criteria) | accept | accepted | EVD-005 | User message of 2026-11-24 in this session accepting SPEC-0238 AC-0001 to AC-0003 | user | platform | none |
| [AC-0003](../spec.md#criteria) | accept | pending | EVD-004, EVD-005 | The user accepted it on 2026-11-24; it is recorded as accepted once the approved 1.1.0 package deletion is run and observed | none | platform | none |

##### Remaining Conditions

The user accepted AC-0001 to AC-0003 on 2026-11-24; AC-0001 and AC-0002 are
recorded as accepted. AC-0003 is recorded once the operator's command deletes
the 1.1.0 package and the deletion is observed here. Hosted checks passed on
pull request #368 (EVD-005), which replaced #364.

#### Handoff

##### Promotion Receipt

P15-CLEANUP-RULE: the
[work lifecycle](../../../../.agents/workflows/work-lifecycle.md) Completion
step 3 applies the QUAL-R025 sort.

##### Next Owner

The operator runs the package deletion; the platform owner records it and
the hosted results; the operator decides the criteria. The next package
input is `prompts/P16-ACCEPT.md`; this Task does not run it.

## 적용과 확인

### 적용 방법

Use this Task for P15 evidence and leave criteria pending until the operator
records decisions.

### 확인 기준

EVD-003 is repository-static evidence; EVD-004 shows the local host.

## 관계와 출처

### 관련 문서

| Relation | Target |
| --- | --- |
| requires | [SPEC-0238 Plan](../plan.md) |
| verifies | [SPEC-0238](../spec.md) |

### 외부 근거

Design D15 is a dated input; no external standard is adopted.
