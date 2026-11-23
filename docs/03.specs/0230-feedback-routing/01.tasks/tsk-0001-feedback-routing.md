---
title: "Feedback Routing Repair Task"
version: "0.1.0"
type: "sdlc/task"
status: "in-progress"
owner: "platform"
updated: "2026-11-23"
artifact_id: "SPEC-0230-TSK-0001"
parent_ids: ["SPEC-0230-PLAN-0001"]
---

# Task: Feedback Routing Repair

## 문서 개요

### 목적과 독자

This Task records the R01 execution and evidence for the [Plan](../plan.md)
and [Spec](../spec.md). The operator and reviewers use it to separate
routing behavior, measured cost and detection from criterion acceptance.

### 책임과 적용 범위

WORK-001 serves AC-0001 through AC-0003. This Task owns R01 work state,
results and criterion decisions.

## 내용 계약

### 입력과 전제

The operator entered `prompts/R01-FEEDBACK.md` from package
`workspace_governance_remediation_1_2_0_20261123` (`package_version: 1.2.0`)
on 2026-11-23, authorizing bounded implementation, verification and
commit, push, pull request and merge. Intake found branch `main` at
`0c2b98e47a91e67c7b655289a8ba99e293d7290f` with a clean worktree. P01, P02
and the eleven earlier streams are not re-executed. SPEC-0229 (P07) keeps its
own open runtime blocker; R01 does not depend on it.

### 본문과 규칙

#### Scope

##### Objective and Parent

WORK-001 executes the [Plan work unit](../plan.md#work-units) for the three
[Spec criteria](../spec.md#criteria).

##### Inputs and Authority

The current user R01 message is the scoped request reference; EVD-001
records the execution receipt. The Spec and Plan stay `draft`; the receipt
grants no formal approval or criterion acceptance.

- **Allowed Paths**: the [Plan WORK-001](../plan.md#work-units) write scope.
- **Forbidden Paths**: other repositories, validator implementations, SPEC-0229 runtime work and P08–P17.
- **Approval Required**: none beyond the current R01 request for ordinary Git delivery; no protected action is planned.
- **Static Validation**: validation-routing suite, mutation checks and staged QA.
- **Live Validation**: not applicable; routing is repository-static.
- **Secret / Vault Handling**: no secret is read or printed.
- **Rollback Plan**: revert the implementation commit.
- **Evidence Location**: this Task's Results.

#### Execution Log

##### Work Performed

The suite module lists moved from `scripts/run-contract-tests.py` into one
file per suite under `scripts/validation/contract-suites/`, which the runner
reads with a bounded, validated loader. Each suite file has its own registry
surface selecting that suite and `validation-routing-tests`. The engine
surface keeps every suite and now includes `test-cluster-regressions`, which
it had omitted since P07. A `governance-guides` surface routes numbered
workspace guides away from `document-contract-tests`, except those the
document suite reads by name. The four documents that named the old
registration location now name the suite files.

##### Blockers and Decisions

The consumer set was decided from measurement, not literal references. One
traced document-suite run (EVD-002) showed that 25 governance documents are
read by specific tests and six test groups read the whole governance corpus.
The whole-corpus groups check link fragments, language, profiles, ADR
diagnostics and context loading, which `links-and-owners`,
`markdown-profiles` and `document-contract-registry` already run for a
changed document. Policy owners, the workspace architecture and every
`.agents` document keep the full regression as a conservative boundary. None
is open.

##### Lifecycle Traceability

| Item | Upstream criterion | Result | Evidence |
| --- | --- | --- | --- |
| WORK-001 | [AC-0001](../spec.md#criteria), [AC-0002](../spec.md#criteria), [AC-0003](../spec.md#criteria) | PASS | Routing regressions, mutation detection and before and after cost are recorded; hosted results and operator criterion decisions remain |

#### Verification Evidence

##### Results

| Evidence ID | Criteria | Work Unit | Method | Input | Tool and Config | Command | Exit | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [AC-0001](../spec.md#criteria), [AC-0002](../spec.md#criteria), [AC-0003](../spec.md#criteria) | WORK-001 | observation | {"actor":"user","approval_ref":"Current human R01-FEEDBACK.md request of 2026-11-23 in this conversation for package workspace_governance_remediation_1_2_0_20261123, bounded implementation, verification and commit/push/PR/merge","scope":["SPEC-0230","SPEC-0230-PLAN-0001","SPEC-0230-TSK-0001"],"reviewed_spec_sha256":"5b49e0108cfbaca1246f056a05b89ce97a1b6ee2e4b0c051bec5381427e2daa5","reviewed_plan_sha256":"97ceb8eb4955f20368c1575e82c05d5dbf1fcf0fcdbf5c60f6ea2782d1c86a20","request_revision":"0804563a80682464046714fbd3d588fe157b0fa250bd878f19a1bd24f38964f1","validity":"confirmed","revocation":"none"} | Current trusted human request; request revision is the validator-defined digest of this Task's scope and work items; exact draft parent hashes | Scoped execution approval | none | PASS | Records the current R01 execution scope only; no formal Spec or Plan approval, criterion acceptance or hosted result follows | true | none |
| EVD-002 | [AC-0002](../spec.md#criteria) | WORK-001 | observation | Document suite at the intake revision, 33 modules | Pinned `/home/hyunyoun/.venvs/hyhome-validation/bin/python`; one-off stdlib audit hook recording repository opens per test (deleted after use) | Traced `document` suite run | 0 | PASS | 1229/1229 tests passed. All 47 governance-surface files were opened; 25 by tests that open at most 15 of them, and the rest only by six whole-corpus groups (fragment, language, profile, ADR and context-load tests). This decides the consumer boundary in AC-0002; it is not a timing sample | true | none |
| EVD-003 | [AC-0001](../spec.md#criteria), [AC-0002](../spec.md#criteria) | WORK-001 | automated | Working tree of `claude/r01-feedback-routing` before commit | Pinned validation Python | New routing tests first, then `python3 scripts/run-contract-tests.py --root . --suite validation-routing` | 0 | PASS | Before the registry change the general-guide test failed on `document-contract-tests`, and the new engine test failed because the engine route omitted `test-cluster-regressions`. After it the suite passed 177/177: each suite file selects only its suite and `validation-routing-tests`, the engine selects every suite, general guides skip `document-contract-tests`, consumers keep it, the named-input drift guard holds and malformed suite files are rejected | true | none |
| EVD-004 | [AC-0003](../spec.md#criteria) | WORK-001 | automated | Selection on `main@0c2b98e4` registry versus the working-tree registry for the same paths; PR341 leaf times from run 45105112715 | `select_paths` of `scripts/validate-affected-surfaces.py`, lane `affected` | In-process selection comparison | 0 | PASS | PR341 file set with registration as data: 23 validators, about 673 s, to 15, about 94 s. One general guide: 8, about 446 s, to 7, about 49 s. One suite registration: 13, about 595 s, to 4, about 13 s. Engine change: 13 to 14 validators (adds the omitted `test-cluster` suite). Estimates use one hosted sample, not p95 | true | none |
| EVD-005 | [AC-0003](../spec.md#criteria) | WORK-001 | automated | Same host, current tree | Pinned validation Python | `python3 scripts/run-contract-tests.py --root . --suite document`; `qa.py quick` with one blank line added to `0013-selective-execution-environment.md` in a temporary worktree of `main` | 0 | PASS | The document suite alone took 544.3 s locally. `qa.py quick` on that guide change took 618.2 s with the `main` registry (8 gates including `document-contract-tests`) and 131.9 s with the new registry copied in, which also selected the registry's own routing checks because the registry itself differed there. The temporary worktree was restored and removed | true | none |
| EVD-006 | [AC-0001](../spec.md#criteria), [AC-0002](../spec.md#criteria) | WORK-001 | automated | Reverted mutations of `scripts/validation/contract-suites/test-cluster.json` and `docs/00.workspace/05.environment/0013-selective-execution-environment.md` | Pinned validation Python; validators the new routes select | `run-contract-tests.py` validation-routing and test-cluster suites; `validate-links-and-owners.py` and `validate-markdown-profiles.py` with `--change-scope` | 0 | PASS | An unknown module fails the test-cluster suite load, which the suite file selects; a module registered twice fails validation-routing. A broken link fails `links-and-owners` (`LINK-BROKEN`); a renamed required heading fails `markdown-profiles` (`BODY-COMMON-ENVELOPE`) and `links-and-owners`. Both files were restored byte for byte | true | none |
| EVD-007 | [AC-0003](../spec.md#criteria) | WORK-001 | automated | Temporary worktree at commit `c2cd6b3d` with one blank line added to `0013-selective-execution-environment.md` | Pinned validation Python, same host as EVD-005 | `python3 scripts/qa.py quick` | 0 | PASS | 7 gates selected without `document-contract-tests`, all PASS, in 87.9 s, against 618.2 s for the same guide change on the `main` registry in EVD-005. Single local sample. The worktree file was restored and the worktree removed | true | none |

##### Resolution Links

No earlier failure is open; the failing-first results in EVD-003 were test
runs before the change and are not separate evidence rows.

#### Acceptance Decision

##### Criterion Decisions

| Criterion | Intent | Acceptance | Evidence | Decision | Accepted By | Current Owner | Reassigned To |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [AC-0001](../spec.md#criteria) | undecided | pending | none | none | none | platform | none |
| [AC-0002](../spec.md#criteria) | undecided | pending | none | none | none | platform | none |
| [AC-0003](../spec.md#criteria) | undecided | pending | none | none | none | platform | none |

##### Remaining Conditions

Staged QA passed in the commit hook of `c2cd6b3d` and the guide-only timing
is EVD-007. Hosted pull request checks and the operator's three criterion
decisions remain.

#### Handoff

##### Promotion Receipt

The Plan promotes no durable contract.

##### Next Owner

The repository owner completes delivery; the operator decides the three
criteria. Hosted timing on later pull requests is a separate observation. The
next package input is `prompts/R02-CONTRACT.md`; this Task does not run it.

## 적용과 확인

### 적용 방법

Use this Task for R01 evidence and leave criteria pending until the operator
records decisions.

### 확인 기준

Routing and mutation results are repository-static; timing values are single
local or hosted samples.

## 관계와 출처

### 관련 문서

| Relation | Target |
| --- | --- |
| requires | [SPEC-0230 Plan](../plan.md) |
| verifies | [SPEC-0230](../spec.md) |

### 외부 근거

The package D18 design and PR341 timing are dated inputs; no external
standard is adopted.
