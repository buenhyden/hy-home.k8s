---
title: "Contained Provider Workers Task"
version: "0.1.0"
type: "sdlc/task"
status: "in-progress"
owner: "platform"
updated: "2026-11-24"
artifact_id: "SPEC-0235-TSK-0001"
parent_ids: ["SPEC-0235-PLAN-0001"]
---

# Task: Contained Provider Workers

## 문서 개요

### 목적과 독자

This Task records the P12 execution and evidence for the [Plan](../plan.md)
and [Spec](../spec.md). The operator and reviewers use it to separate module
behavior, local containment, live provider runs and criterion acceptance.

### 책임과 적용 범위

WORK-001 serves AC-0001 through AC-0004. This Task owns P12 work state,
results and criterion decisions.

## 내용 계약

### 입력과 전제

The operator entered `prompts/P12-PARALLEL.md` from package
`workspace_governance_remediation_1_2_0_20261123` (`package_version: 1.2.0`)
on 2026-11-24, authorizing bounded implementation, verification and
commit, push, pull request and merge. Intake found branch `main` at
`f6520ba06888062e354ef323c3eb97de9f8bc837` with a clean worktree. Earlier
packages are not re-executed.

### 본문과 규칙

#### Scope

##### Objective and Parent

WORK-001 executes the [Plan work unit](../plan.md#work-units) for the four
[Spec criteria](../spec.md#criteria).

##### Inputs and Authority

The current user P12 message is the scoped request reference; EVD-001
records the execution receipt. The Spec and Plan stay `draft`; the receipt
grants no formal approval or criterion acceptance.

- **Allowed Paths**: the [Plan WORK-001](../plan.md#work-units) write scope, this workspace's ignored runtime directory and transient user scopes named `hyk8s-par-*`.
- **Forbidden Paths**: other repositories, the user's provider configuration, and P13–P17.
- **Approval Required**: none beyond the current P12 request for ordinary Git delivery and bounded live worker runs on the existing accounts.
- **Static Validation**: dispatcher and brief regressions, Ruff and staged QA.
- **Live Validation**: one run of two Claude workers; one Codex worker after its quota returns.
- **Secret / Vault Handling**: no secret is read or printed; workers start from an empty environment and the prompts name no secret.
- **Rollback Plan**: revert the commits; stop any `hyk8s-par-*` scope and run `sweep`.
- **Evidence Location**: this Task's Results.

#### Execution Log

##### Work Performed

`scripts/work_parallel.py` accepts provider units (`claude`, `codex`) with a
bounded prompt, a model name and, for Claude, a budget. It builds the
installed CLI's own argv, writes the prompt to stdin, keeps stdout apart for
the parsed result, and records each unit's scope, session, cost, turns and
usage. A provider unit starts only after `request_brief.current` confirms
that the named request's brief is recorded, belongs to this workspace and
has an unchanged policy. Each provider worker runs as
`systemd-run --user --scope` with memory, swap, CPU, task and run-time caps
around `bwrap`, which binds the host read-only, a private `/tmp`, the CLI
binary and the writable clone, and clears the environment except `PATH`,
`HOME`, `LANG`, `TMPDIR` and the dispatcher's own variables. After the
security review of the first commit, bwrap also runs the worker in its own
PID, IPC and UTS namespaces and session, puts a tmpfs over `/run` with only
the resolver mounted back, and masks every other listening path socket from
`/proc/net/unix` with `/dev/null`. Stop, timeout,
cancel and `sweep` stop the whole scope, and its absence gates the lease
release. The clone's size is checked at collection. Command workers are
unchanged. The scope kept the spawned process ID and group, so the existing
launch receipt still matches.

Two contained Claude workers then updated the dispatcher's two documentation
consumers in run `269a0d83`; the integration owner reviewed and applied
`candidate.patch` unchanged.

##### Blockers and Decisions

The installed Claude CLI has no turn limit; `--max-budget-usd` and the unit
timeout bound a run. The live dispatch was first refused twice, as designed:
one execution-brief action covered both paths (`PARALLEL_BRIEF: mutation path
is outside current scope`), and after `scripts/request_brief.py` changed, the
original request `d87d248b56cc0ea6` was stale (`BRIEF-STALE: the policy
changed since the request`). A new request generation `86f07a4651b683f5`
was opened by a background-task notification, its brief shown and recorded,
and the dispatch ran under it. Codex is blocked by the account's usage limit
until 2026-11-27 12:53, so AC-0004 is unobserved. W10-H03 stays open because
command workers still run uncontained and disk has no hard quota; W10-H02
stays open for the Codex worker. Host reads, including the ignored workspace
stores, and the network stay open to provider workers. The automated security
review of commit `bec01440` found that a read-only mount does not stop a
socket connection: the user systemd bus, the Docker socket (this user is in
the `docker` group) and the dispatcher's own process were reachable, so a
worker could have started code outside the boundary. That was fixed before
merge (EVD-006 to EVD-008). Abstract sockets, a path socket created after
dispatch and local TCP services stay reachable while the network is shared.

##### Lifecycle Traceability

| Item | Upstream criterion | Result | Evidence |
| --- | --- | --- | --- |
| WORK-001 | [AC-0001](../spec.md#criteria), [AC-0002](../spec.md#criteria), [AC-0003](../spec.md#criteria), [AC-0004](../spec.md#criteria) | DEFER | Regressions pass (EVD-003, EVD-007); live Claude runs integrated (EVD-005) and repeated under the hardened boundary (EVD-008); live refusals (EVD-004); Codex run blocked by quota |

#### Verification Evidence

##### Results

| Evidence ID | Criteria | Work Unit | Method | Input | Tool and Config | Command | Exit | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [AC-0001](../spec.md#criteria), [AC-0002](../spec.md#criteria), [AC-0003](../spec.md#criteria), [AC-0004](../spec.md#criteria) | WORK-001 | observation | {"actor":"user","approval_ref":"Current human P12-PARALLEL.md request of 2026-11-24 in this conversation for package workspace_governance_remediation_1_2_0_20261123, bounded implementation, verification, live worker runs and commit/push/PR/merge","scope":["SPEC-0235","SPEC-0235-PLAN-0001","SPEC-0235-TSK-0001"],"reviewed_spec_sha256":"56d4d552650f6245a026574e0115b77f7fd97615d3234f1c71b2e2b8d3de505a","reviewed_plan_sha256":"2aab1b8dd40cfc65676edcdae39b1aff470e967bccf7b09fcfc955288f9b1ed5","request_revision":"3c10c2f3378690deaad22d5f8957388725e4e06942b6f9045bbdee119014b159","validity":"confirmed","revocation":"none"} | Current trusted human request; request revision is the validator-defined digest of this Task's scope and work items; exact draft parent hashes | Scoped execution approval | none | PASS | Records the current P12 execution scope only; no formal Spec or Plan approval or criterion acceptance follows | true | none |
| EVD-002 | [AC-0001](../spec.md#criteria), [AC-0002](../spec.md#criteria) | WORK-001 | automated | New brief case and new provider and containment cases before the code change | Pinned validation venv, `unittest` | `python -m unittest tests.test_request_brief`; `python -m unittest tests.test_work_parallel` | 1 | FAIL | Failing-first: brief 1 error (`current` missing); parallel module import error (`sandbox_available` missing) | false | none |
| EVD-003 | [AC-0001](../spec.md#criteria), [AC-0002](../spec.md#criteria) | WORK-001 | automated | Working tree after the change, on this host with user systemd and bwrap 0.9.0 | Pinned validation venv, `unittest`; Ruff | `python -m unittest tests.test_work_parallel tests.test_request_brief`; `ruff check` and `ruff format --check` on the four changed modules | 0 | PASS | 56 tests OK, including the stand-in CLI for both providers: write outside the clone refused, inherited secret variable absent, `setsid` child reclaimed after finish and after a 3-second timeout; Ruff clean. An earlier run of this state failed once on the inherited `HYK8S_FAKE_SECRET` and was fixed by passing only the dispatcher's own variables | true | none |
| EVD-004 | [AC-0001](../spec.md#criteria) | WORK-001 | observation | Live dispatches `d50ab042` and an earlier attempt, 2026-11-24T04:34Z | `scripts/work_parallel.py run --request d87d248b56cc0ea6` | Live dispatch before any worker | 1 | PASS | Both units refused before spawn: first `PARALLEL_BRIEF: mutation path is outside current scope` from the execution-brief preflight, then `PARALLEL_BRIEF: BRIEF-STALE: the policy changed since the request` after `scripts/request_brief.py` changed; no scope, clone or cost | true | none |
| EVD-005 | [AC-0002](../spec.md#criteria), [AC-0003](../spec.md#criteria) | WORK-001 | observation | Run `269a0d83`, 2026-11-24T04:35:34Z to 04:36:23Z, base `f6520ba0`, request `86f07a4651b683f5`; two units owning `scripts/README.md` and `.agents/workflows/delegated-development.md` | `claude` 2.1.331, model `sonnet`, budget 1.0 USD each, 1536 MiB, timeout 900 s; scope and bwrap boundary | `scripts/work_parallel.py run --request 86f07a4651b683f5` | 0 | PASS | `completed`; router active 0.505–13.299 s, session `b8290545-0d89-4b87-aebd-aee01b81fc95`, 3 turns, 0.0802 USD; workflow active 1.035–13.945 s, session `49fee84c-a8f8-4d51-b1ab-7f941e0e3860`, 3 turns, 0.0355 USD; overlap 12.26 s; each changed only its owned file; integration check `validate-links-and-owners.py` PASS; no `hyk8s-par-*` scope left; `candidate.patch` SHA-256 `99e731a1e2d6fd3a02d87df5008081ead854f334bd102be7de22f0a5bc71169d` reviewed and applied unchanged | true | none |
| EVD-006 | [AC-0002](../spec.md#criteria) | WORK-001 | automated | Automated security review of commit `bec01440`; new assertions in the containment cases | Pinned validation venv, `unittest` | `python -m unittest tests.test_work_parallel.ProviderPlanTest tests.test_work_parallel.ContainmentTest` | 1 | FAIL | Inside the boundary `/run/user/<uid>/bus`, `/run/docker.sock` and the dispatcher's process were visible for both providers, and the socket mask helper was missing (2 failures, 1 error); EVD-003 and EVD-005 therefore did not show that writes stay in the clone | true | none |
| EVD-007 | [AC-0002](../spec.md#criteria) | WORK-001 | automated | Working tree after `--unshare-pid`, `--unshare-ipc`, `--unshare-uts`, `--unshare-cgroup-try`, `--new-session`, a tmpfs over `/run` and the listening-socket masks | Pinned validation venv, `unittest`; Ruff | `python -m unittest tests.test_work_parallel.ProviderPlanTest tests.test_work_parallel.ContainmentTest` | 0 | PASS | Focused 7 tests OK, and the full `tests.test_work_parallel tests.test_request_brief` run 57 tests OK: bus, Docker socket and dispatcher process invisible to both stand-in providers, socket table parsed and masked, earlier containment and reclaim cases unchanged; Ruff clean | true | EVD-006 |
| EVD-008 | [AC-0002](../spec.md#criteria), [AC-0003](../spec.md#criteria) | WORK-001 | observation | Run `8c308111`, 2026-11-24T04:59:13Z to 05:00:04Z, the same plan and base `f6520ba0`, request `27e33e6c9554390d`, execution brief re-based on `bec01440` after the first attempt `7764a67b` was refused `PARALLEL_BRIEF: workspace or Git baseline changed` | `claude` 2.1.331, model `sonnet`, budget 1.0 USD each; hardened boundary | `scripts/work_parallel.py run --request 27e33e6c9554390d` | 0 | PASS | `completed`; router active 0.453–13.369 s, session `a68a5d6d-996a-4c88-b75b-8c28ab79604c`, 0.0739 USD; workflow active 1.027–15.232 s, session `5335be0d-4ad6-4082-a184-c393d98896c6`, 0.0344 USD; overlap 12.34 s; each changed only its owned file; integration check PASS; no scope left. Its patch was not applied: the run-1 text was already applied, and the integration owner added the namespace and socket clause to both consumers by hand | true | none |
| EVD-009 | [AC-0001](../spec.md#criteria), [AC-0002](../spec.md#criteria), [AC-0003](../spec.md#criteria) | WORK-001 | observation | Pull request #360, head `959de61c` | GitHub Actions CI run 45331212068; GitGuardian | Hosted pull request checks | 0 | PASS | ci-summary, style-pr (8 min 57 s, including `work-parallel-regressions` and `tooling-tests`), label and GitGuardian passed; the bounded output does not show whether the containment cases ran or skipped on the hosted runner, so EVD-007 stays the containment evidence | true | none |

##### Resolution Links

EVD-002 was a planned failing-first result, not a required failure; EVD-003
shows the passing state. EVD-007 resolves the required failure EVD-006.

#### Acceptance Decision

##### Criterion Decisions

| Criterion | Intent | Acceptance | Evidence | Decision | Accepted By | Current Owner | Reassigned To |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [AC-0001](../spec.md#criteria) | accept | accepted | EVD-003, EVD-004, EVD-009 | User answer of 2026-11-24 in this session (P16) accepting the SPEC-0235 criteria | user | platform | none |
| [AC-0002](../spec.md#criteria) | accept | accepted | EVD-003, EVD-005, EVD-006, EVD-007, EVD-008, EVD-009 | User answer of 2026-11-24 in this session (P16) accepting the SPEC-0235 criteria | user | platform | none |
| [AC-0003](../spec.md#criteria) | accept | accepted | EVD-005, EVD-008, EVD-009 | User answer of 2026-11-24 in this session (P16) accepting the SPEC-0235 criteria | user | platform | none |
| [AC-0004](../spec.md#criteria) | accept | pending | none | Awaiting a Codex run after 2026-11-27 12:53 | none | platform | none |

##### Remaining Conditions

The user accepted AC-0001 to AC-0003 on 2026-11-24 (P16). AC-0004 needs one Codex worker through the same dispatcher after the usage
limit resets on 2026-11-27 12:53 (W10-H02). Hosted checks passed (EVD-009);
the containment cases skip on a host without a user systemd manager or
bwrap. W10-H03 stays open for command workers and a hard disk
quota.

#### Handoff

##### Promotion Receipt

P12-PROVIDER-WORKERS: the
[delegated development workflow](../../../../.agents/workflows/delegated-development.md)
step 5 states provider units, brief freshness and the boundary.

##### Next Owner

The platform owner runs the Codex worker after the quota resets and records
hosted results; the operator decides the criteria. The next package input
is `prompts/P13-OBSERVABILITY.md`; this Task does not run it.

## 적용과 확인

### 적용 방법

Use this Task for P12 evidence and leave criteria pending until the operator
records decisions.

### 확인 기준

Regressions are local and repository-static evidence; EVD-004 and EVD-005
show live dispatches.

## 관계와 출처

### 관련 문서

| Relation | Target |
| --- | --- |
| requires | [SPEC-0235 Plan](../plan.md) |
| verifies | [SPEC-0235](../spec.md) |

### 외부 근거

Design D12 is a dated input; no external standard is adopted.
