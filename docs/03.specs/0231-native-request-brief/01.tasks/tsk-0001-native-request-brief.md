---
title: "Native Request Brief Task"
version: "0.1.0"
type: "sdlc/task"
status: "in-progress"
owner: "platform"
updated: "2026-11-24"
artifact_id: "SPEC-0231-TSK-0001"
parent_ids: ["SPEC-0231-PLAN-0001"]
---

# Task: Native Request Brief

## 문서 개요

### 목적과 독자

This Task records the P08 execution and evidence for the [Plan](../plan.md)
and [Spec](../spec.md). The operator and reviewers use it to separate the
program behavior, the installed clients' observed behavior and criterion
acceptance.

### 책임과 적용 범위

WORK-001 serves AC-0001 through AC-0003. This Task owns P08 work state,
results and criterion decisions.

## 내용 계약

### 입력과 전제

The operator entered `prompts/P08-NATIVE-BRIEF.md` from package
`workspace_governance_remediation_1_2_0_20261123` (`package_version: 1.2.0`)
on 2026-11-24, authorizing bounded implementation, verification and
commit, push, pull request and merge. Intake found branch `main` at
`210587c2c089c941d127f086018c70814017a678` with a clean worktree. P00–P07,
R01 and R02 are not re-executed; SPEC-0229 (P07) keeps its own open runtime
blocker and this Task does not depend on it.

### 본문과 규칙

#### Scope

##### Objective and Parent

WORK-001 executes the [Plan work unit](../plan.md#work-units) for the three
[Spec criteria](../spec.md#criteria).

##### Inputs and Authority

The current user P08 message is the scoped request reference; EVD-001
records the execution receipt. The Spec and Plan stay `draft`; the receipt
grants no formal approval or criterion acceptance.

- **Allowed Paths**: the [Plan WORK-001](../plan.md#work-units) write scope.
- **Forbidden Paths**: other repositories, the user's provider configuration, SPEC-0229 runtime work and P09–P17.
- **Approval Required**: none beyond the current P08 request for ordinary Git delivery; trusting the new Codex hook entry is the user's own action.
- **Static Validation**: tooling suite, agent-governance and staged QA.
- **Live Validation**: one representative native observation per provider in the installed client.
- **Secret / Vault Handling**: no secret is read or printed; receipts keep a prompt digest only.
- **Rollback Plan**: revert the implementation commit.
- **Evidence Location**: this Task's Results.

#### Execution Log

##### Work Performed

`scripts/request_brief.py` adds intake, record and admit. Both providers
register a `UserPromptSubmit` adapter that runs intake, and the shared write
guard calls admit for every change it detects (structured paths, patches and
detected shell targets). The governance validator pins the intake adapter
command for both providers. Provider notes and the scripts README describe
the entry and its limits. The existing Codex pre-tool entry is unchanged, so
its stored trust stays valid.

##### Blockers and Decisions

The brief reaches the user twice: the model shows it in its reply, and the
guard sends the recorded brief through the user-only `systemMessage` on the
first admitted change. A receipt alone is not taken as display; the native
observation decides that. A receipt binds the repository through its Git
common directory, so linked worktrees of the same repository share it.
Branch and policy are checked until the first change only, because the
admitted work may itself switch branch or edit policy.

Residual observed in EVD-007: admission happens in the guard, so when a later
pre-tool hook of another plugin refuses the same call, the brief has already
been shown once and that call made no change. The brief stays recorded and
later changes pass; the display is not repeated.

##### Lifecycle Traceability

| Item | Upstream criterion | Result | Evidence |
| --- | --- | --- | --- |
| WORK-001 | [AC-0001](../spec.md#criteria), [AC-0002](../spec.md#criteria), [AC-0003](../spec.md#criteria) | PASS | Program regressions pass (EVD-004, EVD-005); Claude refused and normal cases observed (EVD-006, EVD-007); Codex unobserved (EVD-008); hosted EVD-009, EVD-011; accepted by the user |

#### Verification Evidence

##### Results

| Evidence ID | Criteria | Work Unit | Method | Input | Tool and Config | Command | Exit | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [AC-0001](../spec.md#criteria), [AC-0002](../spec.md#criteria), [AC-0003](../spec.md#criteria) | WORK-001 | observation | {"actor":"user","approval_ref":"Current human P08-NATIVE-BRIEF.md request of 2026-11-24 in this conversation for package workspace_governance_remediation_1_2_0_20261123, bounded implementation, verification and commit/push/PR/merge","scope":["SPEC-0231","SPEC-0231-PLAN-0001","SPEC-0231-TSK-0001"],"reviewed_spec_sha256":"bed0d526a3dcc3eb313f809c63a1622717813b7fd4822fc62565ee36c8a361df","reviewed_plan_sha256":"e7df23fc06ff924016bd45cea7966c9a63b93216095077ae883fcc7a0a99b929","request_revision":"cbeacda0aa0f9a0009b5bfeec0c6fe282c153b92151178522829f20520b93209","validity":"confirmed","revocation":"none"} | Current trusted human request; request revision is the validator-defined digest of this Task's scope and work items; exact draft parent hashes | Scoped execution approval | none | PASS | Records the current P08 execution scope only; no formal Spec or Plan approval, criterion acceptance or native result follows | true | none |
| EVD-002 | [AC-0001](../spec.md#criteria), [AC-0002](../spec.md#criteria) | WORK-001 | automated | Five `RequestBriefAdmissionTest` cases against the guard before admission was wired | Pinned validation venv, `unittest` | `python -m unittest tests.test_k8s_pre_edit_hook` | 1 | FAIL | Failing-first: four cases failed (missing, not shown, first display, other turn) and the read-only case passed | false | none |
| EVD-003 | [AC-0001](../spec.md#criteria) | WORK-001 | automated | New `UserPromptSubmit` registrations for both providers checked by the HEAD `210587c2` validator | `scripts/validate-agent-governance.py` at HEAD | `python3 scripts/validate-agent-governance.py --root .` | 1 | FAIL | Failing-first: HEAD rejected the unknown hook event with `AGENT-NATIVE-HOOK` | false | none |
| EVD-004 | [AC-0001](../spec.md#criteria), [AC-0002](../spec.md#criteria) | WORK-001 | automated | Module, guard and registration regressions on the working tree | Pinned validation venv, `unittest` | `python -m unittest tests.test_k8s_pre_edit_hook tests.test_request_brief tests.test_agent_governance` | 0 | PASS | 151 tests OK; four older guard tests were rewritten to the current contract (a change needs an admitted receipt) and the surrogate-session case passes after the receipt name hashes with `surrogatepass` | true | none |
| EVD-005 | [AC-0001](../spec.md#criteria), [AC-0002](../spec.md#criteria) | WORK-001 | automated | Tooling suite and agent registry on the working tree | Pinned validation venv | `python scripts/run-contract-tests.py --root . --suite tooling`; `python scripts/validate-agent-governance.py --root .`; `ruff check scripts tests` | 0 | PASS | tooling modules=9 tests=189; agent registry PASS providers=2 roles=17; ruff clean | true | none |
| EVD-006 | [AC-0002](../spec.md#criteria), [AC-0003](../spec.md#criteria) | WORK-001 | observation | This Claude Code session before any intake (hook registered after the session's first prompt); 2026-11-23T16:58Z | Claude Code 2.1.330, tracked project settings | Structured `Edit` of `scripts/request_brief.py` | 2 | PASS | Refused case observed: the client ran the guard and refused with `BRIEF-MISSING: no request was received for this session`; the receipt directory held only its lock | true | none |
| EVD-007 | [AC-0001](../spec.md#criteria), [AC-0003](../spec.md#criteria) | WORK-001 | observation | Next user prompt in the same session; receipt request `032de488005e3d39`, generation 1, received 2026-11-23T22:13:36Z, recorded 22:13:53Z, admitted 22:14:00Z | Claude Code (installed 2.1.331 at observation), tracked project settings | `UserPromptSubmit` intake; `python3 scripts/request_brief.py record --request 032de488005e3d39`; first structured `Edit` | 0 | PASS | Normal case observed: the model received the intake context, showed the brief in its reply, recorded it (`BRIEF-RECORDED`), and the first edit was admitted with the brief in the hook output, which the guard sends as `systemMessage` and `additionalContext`; later edits passed without a second display. The user's sight of the `systemMessage` is not yet confirmed | true | none |
| EVD-008 | [AC-0003](../spec.md#criteria) | WORK-001 | observation | One `codex exec` probe asking for an `apply_patch` write of `p08-probe.txt`; 2026-11-23T22:16Z; the new `user_prompt_submit` entry is not yet trusted in `/hooks` | Codex CLI 0.171.0, `workspace-write` sandbox | `codex exec --sandbox workspace-write "<probe>"` | 1 | DEFER | Unobserved: the account usage limit stopped the turn before any tool call (limit resets 2026-11-27). Only the trusted ponytail plugin's prompt hook ran; no Codex receipt and no probe file were created | true | none |
| EVD-009 | [AC-0001](../spec.md#criteria), [AC-0002](../spec.md#criteria) | WORK-001 | automated | PR #348 head `9eb842ef077148d3a685bb6fe7668e5c4187ca24` | GitHub Actions CI run 45279867140 and its `style-pr` job; GitGuardian | `gh pr checks 348` | 0 | PASS | ci-summary, style-pr, GitGuardian, label and greeting passed; merge state CLEAN | true | none |
| EVD-010 | [AC-0002](../spec.md#criteria), [AC-0003](../spec.md#criteria) | WORK-001 | observation | Same Claude session; a background task-completion notification arrived with no user message, 2026-11-23T22:4xZ | Claude Code (installed 2.1.331), tracked project settings | `UserPromptSubmit` intake on the notification turn | 0 | PASS | The client fired `UserPromptSubmit` for the notification, so intake started generation 2 (`c7c15fcfaea52160`) and the earlier brief became stale; the model showed and recorded a new brief before the next change | true | none |
| EVD-011 | [AC-0001](../spec.md#criteria), [AC-0002](../spec.md#criteria) | WORK-001 | observation | Pull request #348, head `fa40581f`, merged as `256d2b22` | GitHub Actions CI run 45280848291; GitGuardian | Hosted pull request checks | 0 | PASS | ci-summary, style-pr, label and GitGuardian passed on the final head; merged without bypass | true | none |
| EVD-012 | [AC-0001](../spec.md#criteria), [AC-0003](../spec.md#criteria) | WORK-001 | observation | Session transcript entries for the first admitted change of generations 1 and 2 (2026-11-23T22:14:00Z, 22:30:07Z) | Claude Code (installed 2.1.331) session transcript | Read of the transcript `attachment` entries | 0 | PASS | Each first admitted change produced a `hook_system_message` entry carrying the brief, separate from the model's `hook_additional_context`; the user did not recall seeing it, so the on-screen sight stays unconfirmed and a re-check was offered on generation 3 | true | none |
| EVD-013 | [AC-0002](../spec.md#criteria), [AC-0003](../spec.md#criteria) | WORK-001 | observation | Generation 3 (`49d94733dc6f2d4a`) recorded on `main`, then a new branch created before the first change; 2026-11-23T22:5xZ | Claude Code (installed 2.1.331), tracked project settings | Structured `Edit` of this Task on the new branch | 2 | PASS | Refused case observed: the guard refused with `BRIEF-STALE` because the branch changed since the request. A branch must be created before the brief is recorded | true | none |
| EVD-014 | [AC-0001](../spec.md#criteria), [AC-0003](../spec.md#criteria) | WORK-001 | observation | Same generation 3 after switching back to the request's branch `main` | Claude Code (installed 2.1.331), tracked project settings | Same structured `Edit` of this Task on `main` | 0 | PASS | The edit was admitted with the brief in the hook output; the uncommitted change then moved to the work branch | true | none |

##### Resolution Links

EVD-002 and EVD-003 were planned failing-first results, not required
failures; EVD-004 and EVD-005 show the passing state. EVD-007 is the normal
case following the refusal in EVD-006. EVD-008 is open: the Codex normal and refused cases need the user's
`/hooks` trust of the new entry and an available Codex quota. EVD-010 is a
residual: Claude Code also fires `UserPromptSubmit` for a background-task
notification, so such a turn starts a new generation and asks for a fresh
brief although the user sent nothing.

#### Acceptance Decision

##### Criterion Decisions

| Criterion | Intent | Acceptance | Evidence | Decision | Accepted By | Current Owner | Reassigned To |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [AC-0001](../spec.md#criteria) | accept | accepted | EVD-004, EVD-005, EVD-007, EVD-011, EVD-012, EVD-014 | User message of 2026-11-24 in this session accepting the SPEC-0231 criteria | user | platform | none |
| [AC-0002](../spec.md#criteria) | accept | accepted | EVD-004, EVD-005, EVD-006, EVD-010, EVD-011, EVD-013 | User message of 2026-11-24 in this session accepting the SPEC-0231 criteria | user | platform | none |
| [AC-0003](../spec.md#criteria) | undecided | pending | none | none | none | platform | none |

##### Remaining Conditions

Staged QA passed in the commit hooks and hosted checks passed (EVD-009,
EVD-011). On 2026-11-24 the user accepted the three criteria, AC-0003 with
Codex recorded as unobserved. AC-0001 and AC-0002 are recorded as accepted.
AC-0003 stays pending because a criterion cannot be accepted while its
required evidence EVD-008 is open. A later PASS of the same Codex probe,
after the user trusts the new `user_prompt_submit` entry in `/hooks` and the
Codex quota returns (2026-11-27), resolves it; the user's AC-0003 decision
is then recorded and the Task completes. The user's on-screen sight of the
`systemMessage` stays unconfirmed (EVD-012).

#### Handoff

##### Promotion Receipt

The Plan promotes no durable contract. Both provider notes carry the intake
entry directly; their native claims follow the observations recorded here.

##### Next Owner

Delivery and criterion acceptance are complete. The platform owner runs the
Codex probe of EVD-008 once it can run and records the resolving row. The next package input is
`prompts/P09-MEMORY.md`; this Task does not run it.

## 적용과 확인

### 적용 방법

Use this Task for P08 evidence and leave criteria pending until the operator
records decisions.

### 확인 기준

Program behavior is repository-static evidence; only the recorded native
observations show what an installed client delivered and displayed.

## 관계와 출처

### 관련 문서

| Relation | Target |
| --- | --- |
| requires | [SPEC-0231 Plan](../plan.md) |
| verifies | [SPEC-0231](../spec.md) |

### 외부 근거

The package D08 design is a dated input; no external standard is adopted.
