---
title: "Cutover Readiness Task"
version: "0.1.0"
type: "sdlc/task"
status: "in-progress"
owner: "platform"
updated: "2026-11-24"
artifact_id: "SPEC-0239-TSK-0001"
parent_ids: ["SPEC-0239-PLAN-0001"]
---

# Task: Cutover Readiness

## 문서 개요

### 목적과 독자

This Task records the P16 readiness inventory, its evidence and the
criterion decisions for the [Plan](../plan.md) and [Spec](../spec.md). The
operator uses it to see what still blocks P17.

### 책임과 적용 범위

WORK-001 serves AC-0001 through AC-0004. This Task owns P16 work state,
results and criterion decisions.

## 내용 계약

### 입력과 전제

The operator entered `prompts/P16-ACCEPT.md` from package
`workspace_governance_remediation_1_2_0_20261123` (`package_version: 1.2.0`)
on 2026-11-24, authorizing bounded work, verification and commit, push,
pull request and merge. Intake found `main` at
`a4968ee5e81f15a47151672b6dbaf4081eac3ea3`. On 2026-11-24 the operator
accepted the pending criteria of SPEC-0227, SPEC-0228, SPEC-0232, SPEC-0234,
SPEC-0236 and SPEC-0237 and AC-0001 to AC-0003 of SPEC-0235, chose to retire
the P07 VM route, and chose to keep the rest of W10-H03 future-conditional.
The request arrived while P15's branch was checked out; the work was moved to
`main` and ran under request `eb6fb66a23c29089`, whose brief was shown and
recorded.

### 본문과 규칙

#### Scope

##### Objective and Parent

WORK-001 executes the [Plan work unit](../plan.md#work-units) for the four
[Spec criteria](../spec.md#criteria).

##### Inputs and Authority

The current user P16 message and its three answers are the scoped request
reference; EVD-001 records the execution receipt. The Spec and Plan stay
`draft`; the receipt grants no formal approval or criterion acceptance.

- **Allowed Paths**: the [Plan WORK-001](../plan.md#work-units) write scope.
- **Forbidden Paths**: P15's open branch, other repositories, the user's provider configuration, remote history, and P17.
- **Approval Required**: none beyond the P16 request and answers for ordinary Git delivery.
- **Static Validation**: staged QA and, for the rule, Task-evidence regressions.
- **Live Validation**: none new; the Claude half of AGENT-04 is read from this session's own hook and import records.
- **Secret / Vault Handling**: no secret is read or printed.
- **Rollback Plan**: revert the commits.
- **Evidence Location**: this Task's Results.

#### Execution Log

##### Work Performed

Readiness inventory through P16, in this workspace's resume order. Each item
gives design, code, regression, live and user acceptance, then its state.

- SPEC-0229 (P07 resume and exit): design, host-route code and regressions
  done; live host route PASS and VM route failures; AC-0001 accepted,
  AC-0002 to AC-0006 pending. State: blocked until the VM route is retired
  (AC-0004 of this Task) and the operator decides AC-0002 to AC-0006.
- R01 (SPEC-0230) and R02 (SPEC-0226, exited): complete and accepted.
- P05 (SPEC-0227) and P06 (SPEC-0228): complete; accepted on 2026-11-24 with
  a current re-verification of their promotion owners. W07-H05, the excluded
  Desktop review route, stays maintained as excluded.
- P08 (SPEC-0231): AC-0001 and AC-0002 accepted; AC-0003 blocked on the Codex
  observation (EVD-008), which needs the operator's `/hooks` trust and the
  Codex quota after 2026-11-27 12:53.
- P09 (SPEC-0232), P11 (SPEC-0234), P13 (SPEC-0236), P14 (SPEC-0237):
  complete and accepted on 2026-11-24. Named follow-ups: the two-provider
  live memory write and W10-H01 wait for Codex; W06-H02 waits for a manifest
  or CI lock change.
- P10 (SPEC-0233): complete and accepted; the first scheduled firing of the
  per-workspace timer on 2026-11-25 03:00 KST is an accepted follow-up.
- P12 (SPEC-0235): AC-0001 to AC-0003 accepted on 2026-11-24; AC-0004, a
  Codex worker run (W10-H02), is blocked until the Codex quota returns.
  W10-H03 is narrowed to future-conditional command-worker containment and a
  hard disk cap (SPEC-0223 EVD-047).
- P15 (SPEC-0238): pull request #364 is open; the 1.1.0 package deletion
  waits for the operator's command, then its record, merge and decisions.
  State: blocked.
- Residues: AGENT-04's Claude half is observed (EVD-005) and its Codex half
  blocked; W08-H03 is blocked on Codex; W08-H01, W08-H02, W08-H04 and W08-H05
  (its call IDs and failure classes landed in P10; deliberate negative tests
  stay unattributed) are future-conditional; DOC-12, DOC-H01, Q07-H01 and
  T99-H03 are P17-owned.
- Not applicable here: the Template `main`/`dev` roles and the Blog public
  boundary belong to other workspaces.

P17 preparation, reviewed without running P17: one worktree; 24 remote
branches (`main` and 23 merged `claude/*` work branches) and 10 tags (9
`main-<sha>` and `v0.1.0`); 16 Spec packages to exit or carry, counting
SPEC-0238 and this one;
the set-aside `forecast.prerelease.sqlite3` store and the current forecast
store to set aside for an N=0 baseline; the 1.2.0 package to remove last.
Verdict: `cutover_ready: false`.

##### Blockers and Decisions

Blocking P17: the SPEC-0229 retirement and decisions; the Codex native
observations (SPEC-0231 AC-0003, SPEC-0235 AC-0004, W10-H01, W10-H02,
W08-H03 and AGENT-04's Codex half), external until 2026-11-27 12:53 and the
operator's `/hooks` trust; and P15's completion. No unchanged check was
rerun as a whole; SPEC-0227 received a current approval receipt because its
Spec had changed after its receipt.

##### Lifecycle Traceability

| Item | Upstream criterion | Result | Evidence |
| --- | --- | --- | --- |
| WORK-001 | [AC-0001](../spec.md#criteria), [AC-0002](../spec.md#criteria), [AC-0003](../spec.md#criteria), [AC-0004](../spec.md#criteria) | DEFER | Inventory (EVD-002); acceptances recorded (EVD-003); W10-H03 narrowed (EVD-004); AGENT-04 Claude half (EVD-005); the retired-route rule follows in a second pull request |

#### Verification Evidence

##### Results

| Evidence ID | Criteria | Work Unit | Method | Input | Tool and Config | Command | Exit | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [AC-0001](../spec.md#criteria), [AC-0002](../spec.md#criteria), [AC-0003](../spec.md#criteria), [AC-0004](../spec.md#criteria) | WORK-001 | observation | {"actor":"user","approval_ref":"Current human P16-ACCEPT.md request of 2026-11-24 in this conversation for package workspace_governance_remediation_1_2_0_20261123 with the user's three P16 answers; bounded work, verification and commit/push/PR/merge","scope":["SPEC-0239","SPEC-0239-PLAN-0001","SPEC-0239-TSK-0001"],"reviewed_spec_sha256":"baba37ba6f3ce1c44bd4f032dabfe627ad9f7832001f3c8b188f193b157743de","reviewed_plan_sha256":"5bbaac38752a0911b3ea8427455445c9d217a533f9941d4dbabba7948b6cebc2","request_revision":"bd911ed73e0f34c3850bd178c93a327c6773e1e4e330f0174a4e8b6283dbab9b","validity":"confirmed","revocation":"none"} | Current trusted human request; request revision is the validator-defined digest of this Task's scope and work items; exact draft parent hashes | Scoped execution approval | none | PASS | Records the current P16 execution scope only; no formal Spec or Plan approval or criterion acceptance follows | true | none |
| EVD-002 | [AC-0001](../spec.md#criteria), [AC-0003](../spec.md#criteria) | WORK-001 | observation | `main@a4968ee5`: every Task under `docs/03.specs/`, the work residue ledger, `git worktree list` and the remote refs | Python standard library; Git | Read each Task's status and Criterion Decisions; list open ledger entries; `git ls-remote --heads origin`; `git ls-remote --tags origin` | 0 | PASS | 14 packages on `main`, with SPEC-0238 on its open pull request; SPEC-0230 and SPEC-0233 completed and accepted; 15 open ledger entries before this change; one worktree; 24 heads and 10 tags. The inventory and the three blockers are stated under Work Performed | true | none |
| EVD-003 | [AC-0002](../spec.md#criteria) | WORK-001 | automated | The accepted decision rows in SPEC-0227, SPEC-0228, SPEC-0232, SPEC-0234, SPEC-0235, SPEC-0236 and SPEC-0237; SPEC-0227 EVD-013 and EVD-014; SPEC-0228 EVD-021 | Pinned validation venv | `scripts/validate-document-lifecycle.py --mode staged`; `scripts/validate-markdown-profiles.py --root . --mode strict` over the changed Tasks | 0 | PASS | No violations: every accepted criterion cites a relevant required PASS, the six fully accepted Tasks are `completed` with valid promotion receipts, and SPEC-0235 stays `in-progress` for AC-0004 | true | none |
| EVD-004 | [AC-0003](../spec.md#criteria) | WORK-001 | automated | SPEC-0223 EVD-047 and the narrowed W10-H03 row and entry | Pinned validation venv | `scripts/validate-work-residue-ledger.py --root .` | 0 | PASS | 30 entries; W10-H03 stays open with the resume condition "When an untrusted command worker is dispatched, or a hard disk cap is required" | true | none |
| EVD-005 | [AC-0003](../spec.md#criteria) | WORK-001 | observation | This Claude Code session on 2026-11-24 | Claude Code CLI with the tracked hooks | Read of the session's own records after `/compact` and after file reads in folders with a `CLAUDE.md` | 0 | PASS | After `/compact`, both `PreCompact` command hooks completed and the `SessionStart` `compact` hook delivered its instruction to re-read folder `AGENTS.md` files. Reading files in `docs/`, `docs/03.specs/`, `docs/02.architecture/`, `docs/00.workspace/`, `docs/99.templates/`, `scripts/` and `tests/` loaded each folder `CLAUDE.md` and its imported `AGENTS.md`. This is the Claude half of AGENT-04; Codex delivery is unobserved, so AGENT-04 stays open | true | none |
| EVD-006 | [AC-0001](../spec.md#criteria), [AC-0002](../spec.md#criteria), [AC-0003](../spec.md#criteria) | WORK-001 | observation | Pull request #365, head `ee95b677` | GitHub Actions CI run 45361808473 | Hosted pull request checks | 0 | PASS | CI, Labeler and Greeting runs completed with success on the head | true | none |

##### Resolution Links

None.

#### Acceptance Decision

##### Criterion Decisions

| Criterion | Intent | Acceptance | Evidence | Decision | Accepted By | Current Owner | Reassigned To |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [AC-0001](../spec.md#criteria) | accept | pending | EVD-002, EVD-006 | Awaiting the operator's decision | none | platform | none |
| [AC-0002](../spec.md#criteria) | accept | pending | EVD-003, EVD-006 | Awaiting the operator's decision | none | platform | none |
| [AC-0003](../spec.md#criteria) | accept | pending | EVD-002, EVD-004, EVD-005, EVD-006 | Awaiting the operator's decision | none | platform | none |
| [AC-0004](../spec.md#criteria) | accept | pending | none | Awaiting the retired-route rule in the second pull request | none | platform | none |

##### Remaining Conditions

The retired-route rule and its SPEC-0229 use follow in a second pull
request; the operator then decides SPEC-0229 AC-0002 to AC-0006. Hosted
checks of the first pull request passed (EVD-006). `cutover_ready` stays false while the
three blockers remain.

#### Handoff

##### Promotion Receipt

P16-RETIRED-ROUTE: the [document lifecycle policy](../../../00.workspace/03.process/document-lifecycle.md)
states the retired-route rule once the second pull request lands.

##### Next Owner

The platform owner lands the retired-route rule and records hosted results;
the operator decides the open criteria, runs the P15 package deletion and
trusts the Codex hook. The next package input is `prompts/P17-FINAL-CUTOVER.md`,
which starts only after `cutover_ready` is true; this Task does not run it.

## 적용과 확인

### 적용 방법

Use this Task as the P16 readiness record and leave criteria pending until
the operator records decisions.

### 확인 기준

EVD-003 and EVD-004 are repository-static evidence; EVD-002 and EVD-005 are
observations of the checkout and this session.

## 관계와 출처

### 관련 문서

| Relation | Target |
| --- | --- |
| requires | [SPEC-0239 Plan](../plan.md) |
| verifies | [SPEC-0239](../spec.md) |

### 외부 근거

Design D16 is a dated input; no external standard is adopted.
