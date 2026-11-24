---
title: "Selected Session Content Task"
version: "0.1.0"
type: "sdlc/task"
status: "in-progress"
owner: "platform"
updated: "2026-11-24"
artifact_id: "SPEC-0233-TSK-0001"
parent_ids: ["SPEC-0233-PLAN-0001"]
---

# Task: Selected Session Content

## 문서 개요

### 목적과 독자

This Task records the P10 execution and evidence for the [Plan](../plan.md)
and [Spec](../spec.md). The operator and reviewers use it to separate module
behavior, live store and timer observations and criterion acceptance.

### 책임과 적용 범위

WORK-001 serves AC-0001 through AC-0003. This Task owns P10 work state,
results and criterion decisions.

## 내용 계약

### 입력과 전제

The operator entered `prompts/P10-SESSIONS.md` from package
`workspace_governance_remediation_1_2_0_20261123` (`package_version: 1.2.0`)
on 2026-11-24, authorizing bounded implementation, verification and
commit, push, pull request and merge. Intake found branch `main` at
`30bd8dd5b3fc9220a3c57c0961607e6531cfd34e` with a clean worktree. Earlier
packages are not re-executed.

### 본문과 규칙

#### Scope

##### Objective and Parent

WORK-001 executes the [Plan work unit](../plan.md#work-units) for the three
[Spec criteria](../spec.md#criteria).

##### Inputs and Authority

The current user P10 message is the scoped request reference; EVD-001
records the execution receipt. The Spec and Plan stay `draft`; the receipt
grants no formal approval or criterion acceptance.

- **Allowed Paths**: the [Plan WORK-001](../plan.md#work-units) write scope and this workspace's user timer.
- **Forbidden Paths**: other repositories and their timers, the user's provider configuration, and P11–P17.
- **Approval Required**: none beyond the current P10 request for ordinary Git delivery and this workspace's timer.
- **Static Validation**: capture, analysis and memory regressions and staged QA.
- **Live Validation**: one live scan, a redaction residue check, the timer registration and one unit run.
- **Secret / Vault Handling**: no secret is read or printed; observations report counts only, never stored text.
- **Rollback Plan**: revert the implementation commit and reinstall the timer from the reverted checkout.
- **Evidence Location**: this Task's Results.

#### Execution Log

##### Work Performed

`scripts/session_capture.py` adds the `content` table and stores, in the
transaction of each new line, the visible prompt, visible response and tool
result after redaction, abridgement, a second redaction and a UTF-8 cap,
with call ID, failure class, turn, event time, expiry and editions. `expire`
drops expired content and 90-day-old session metadata while keeping cursors;
`contents` reads one session. `scripts/session_analysis.py` expires content
and unpromoted candidates on each run, adds the `repeated-permission-denial`
and `repeated-hook-rejection` rules (rules edition 2), and names the timer
with the workspace ID, retiring the legacy unit only when it is this
checkout's.

##### Blockers and Decisions

The existing offset-based event identity, the single cursor and record
transaction, idempotent redelivery and the `modified` flag already meet the
D10 cursor rules and are kept. The structural `repeated-tool-failure` rule
stays unchanged so the accepted candidate's rechecks keep their meaning.
Residue W08-H05 stays open: failures now carry call IDs and the permission,
hook and command classes, but a deliberate negative test is still not told
apart from a real failure.

##### Lifecycle Traceability

| Item | Upstream criterion | Result | Evidence |
| --- | --- | --- | --- |
| WORK-001 | [AC-0001](../spec.md#criteria), [AC-0002](../spec.md#criteria), [AC-0003](../spec.md#criteria) | PASS | Regressions pass (EVD-003); live scan, residue check, timer registration and unit run pass (EVD-004 to EVD-006); hosted checks passed (EVD-007) |

#### Verification Evidence

##### Results

| Evidence ID | Criteria | Work Unit | Method | Input | Tool and Config | Command | Exit | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [AC-0001](../spec.md#criteria), [AC-0002](../spec.md#criteria), [AC-0003](../spec.md#criteria) | WORK-001 | observation | {"actor":"user","approval_ref":"Current human P10-SESSIONS.md request of 2026-11-24 in this conversation for package workspace_governance_remediation_1_2_0_20261123, bounded implementation, verification and commit/push/PR/merge","scope":["SPEC-0233","SPEC-0233-PLAN-0001","SPEC-0233-TSK-0001"],"reviewed_spec_sha256":"5aa0367c0faf5da0f47d02ce4a2d244f1e9cdf8bfe82c14d4e51b7d2b6af9348","reviewed_plan_sha256":"330c306cc29c9b40773eed0997e9577d22d05b12f724c460c4ead37d20b1900f","request_revision":"679fc6d0cdc6c6abf7bdc164a84245e20f16ad0810ea93f411597e605e27077f","validity":"confirmed","revocation":"none"} | Current trusted human request; request revision is the validator-defined digest of this Task's scope and work items; exact draft parent hashes | Scoped execution approval | none | PASS | Records the current P10 execution scope only; no formal Spec or Plan approval or criterion acceptance follows | true | none |
| EVD-002 | [AC-0001](../spec.md#criteria), [AC-0002](../spec.md#criteria), [AC-0003](../spec.md#criteria) | WORK-001 | automated | New `SelectedContentTest` cases and four analysis cases before the code change | Pinned validation venv, `unittest` | `python -m unittest tests.test_session_capture.SelectedContentTest`; `python -m unittest tests.test_session_analysis` | 1 | FAIL | Failing-first: capture 7 errors, analysis 2 failures and 2 errors | false | none |
| EVD-003 | [AC-0001](../spec.md#criteria), [AC-0002](../spec.md#criteria), [AC-0003](../spec.md#criteria) | WORK-001 | automated | Working tree after the change; the two capture tests of the old no-text contract rewritten to Q-02 | Pinned validation venv, `unittest`; Ruff | `python -m unittest tests.test_session_capture tests.test_session_analysis tests.test_workspace_memory`; `ruff check scripts tests` | 0 | PASS | capture 28, analysis 31 and memory 38 tests OK; Ruff clean | true | none |
| EVD-004 | [AC-0001](../spec.md#criteria), [AC-0002](../spec.md#criteria), [AC-0003](../spec.md#criteria) | WORK-001 | observation | Live capture, 2026-11-24T02:50:10Z, after consistent SQLite backups of the capture (70 sessions, 146,397 records) and analysis stores, both integrity `ok` | Changed working-tree code | `scripts/session_capture.py scan`; counts by role, selection, failure class and gap | 0 | PASS | Integrity `ok`; 154,628 records. Content: 9 selected prompts (largest at the 16 KiB cap), 7 selected and 2 summarized responses, 36 selected failed tool results classed 20 `hook_rejected`, 5 `permission_denied` and 11 `command_failed`, 22 summarized results (each at most 4 KiB), and 135 response and 399 result `summary_cap` gaps from long turns | true | none |
| EVD-005 | [AC-0001](../spec.md#criteria) | WORK-001 | observation | The 76 stored live texts after EVD-004 | `session_capture._secret_left`, `SELECTED_LIMIT` | Read-only residue check | 0 | PASS | No secret or e-mail pattern remains, none exceeds its cap, and one value carries a redaction placeholder; no text was printed | true | none |
| EVD-006 | [AC-0003](../spec.md#criteria) | WORK-001 | observation | User systemd, 2026-11-24T02:50:44Z; the legacy `hy-home-k8s-session-analysis` timer had finished every daily run through 2026-11-24 03:00 KST (runs 14 to 19, including the 2026-11-21 recheck date) | systemd user manager; changed working-tree code | `scripts/session_analysis.py install-timer`; `systemctl --user start hy-home-k8s-session-analysis-83ced050.service` | 0 | PASS | `legacy_retired: true`; the timer `hy-home-k8s-session-analysis-83ced050` is listed for 03:00 and the other workspaces' timers are untouched. The unit run ended `Result=success`: run 20 completed under rules edition 2 for all six days at cost 0, added the `repeated-hook-rejection` and `repeated-permission-denial` harness candidates for 2026-11-23, and kept the accepted and the rejected candidates. Both backups were then deleted. The next scheduled firing is not yet observed | true | none |
| EVD-007 | [AC-0001](../spec.md#criteria), [AC-0002](../spec.md#criteria), [AC-0003](../spec.md#criteria) | WORK-001 | observation | Pull request #356, head `1225edc3` | GitHub Actions CI run 45316228108; GitGuardian | Hosted pull request checks | 0 | PASS | ci-summary, style-pr (6 min 33 s, including the affected capture, analysis and memory regression gates), label, greeting and GitGuardian passed | true | none |

##### Resolution Links

EVD-002 was a planned failing-first result, not a required failure; EVD-003
shows the passing state.

#### Acceptance Decision

##### Criterion Decisions

| Criterion | Intent | Acceptance | Evidence | Decision | Accepted By | Current Owner | Reassigned To |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [AC-0001](../spec.md#criteria) | undecided | pending | none | none | none | platform | none |
| [AC-0002](../spec.md#criteria) | undecided | pending | none | none | none | platform | none |
| [AC-0003](../spec.md#criteria) | undecided | pending | none | none | none | platform | none |

##### Remaining Conditions

Hosted checks passed (EVD-007); the operator's criterion decisions remain. The first
scheduled firing of the new timer (2026-11-25 03:00 KST) is not yet
observed; EVD-006 shows its registration and one unit run. Expiry boundaries
are shown by regressions, since no live content is old enough yet. W08-H05
stays open for deliberate negative tests.

#### Handoff

##### Promotion Receipt

P10-SESSION-RULES: the [context and memory policy](../../../../.agents/governance/context-and-memory.md)
states the changed rules in CTX-R006, R022 and R023.

##### Next Owner

The platform owner records hosted results and the next scheduled run; the
operator decides the criteria. The next package input is
`prompts/P11-FORECAST.md`; this Task does not run it.

## 적용과 확인

### 적용 방법

Use this Task for P10 evidence and leave criteria pending until the operator
records decisions.

### 확인 기준

Module behavior is repository-static evidence; EVD-004 to EVD-006 show the
local stores and the user timer.

## 관계와 출처

### 관련 문서

| Relation | Target |
| --- | --- |
| requires | [SPEC-0233 Plan](../plan.md) |
| verifies | [SPEC-0233](../spec.md) |

### 외부 근거

The package D10 design and retention policy are dated inputs; no external
standard is adopted.
