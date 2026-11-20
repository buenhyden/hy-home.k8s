---
title: "Work Lifecycle"
version: "3.0.0"
type: "governance/skill"
status: "active"
owner: "platform"
updated: "2026-11-20"
---

# Work Lifecycle

## 문서 개요

### 목적과 독자

작업자는 아래에 적힌 조건과 범위에서 업무 생명주기 절차를 사용한다.

### 책임과 적용 범위

이 절차의 적용 조건과 권한은 [사용 시점](#when-to-use)과 [권한 경계](#authority-boundary)에 따른다.

## 내용 계약

### 입력과 전제

단계를 수행하기 전에 현재 요청과 명시된 입력을 읽는다.

### 본문과 규칙

#### Trigger

##### When to Use

Use one intake-to-handoff procedure for substantial repository work rather than
separate bootstrap, preflight, and postflight rule copies.

Related policy and responsibility documents: [SDLC Flow](../../docs/00.workspace/03.process/sdlc.md),
[Document Authoring](../../docs/00.workspace/03.process/document-authoring.md),
[Context and Memory](../governance/context-and-memory.md) and
[Roles](../roles/README.md).

###### Inputs

Start at the current provider gateway, then load the minimum relevant policy,
role responsibility, provider note, and owning Spec/Plan/Task. Re-observe Git
state on resume; historical progress and provider-local memory are auxiliary.

##### When Not to Use

This procedure names no repository work it must not be used for; if such a case is found, state it here.

##### Authority Boundary

This procedure applies [agent execution](../governance/agent-execution.md),
[approval and safety](../../docs/00.workspace/04.quality/approval-and-safety.md), and
[quality](../../docs/00.workspace/04.quality/quality.md). It does not grant new scope or override the
active Task, registry permissions, or provider controls.

#### Procedure

##### Steps

The procedure parts are Intake, Resume, Implementation and Completion.

###### Intake

1. State the outcome, acceptance IDs, in/out scope, material assumptions, and
   protected actions. Resolve contradictions before editing.
2. Inspect branch/worktree, status, relevant diffs, and canonical owners. Use
   `.agents/knowledge/` to find which tree and which entry document own the
   affected area, then read that owner; the map routes and never decides.
   Preserve unrelated changes and identify the exact write boundary.
3. Select the responsibility from [roles](../roles/README.md), resolve any
   delegated role and skills from the agent registry, and load the provider
   note only for native behavior.
4. Resolve the Stage 99 profile and template before authored document changes.
   Record the current scoped request in the existing Task Inputs and Authority. Keep the Spec acceptance contract, Plan work mapping
   and actual Task execution/evidence separate; progress is kept as [context and memory](../governance/context-and-memory.md#objective) states.
   Identify the request reference and revision, applicable authority, target,
   scope and conditions. Draft authoring, review and focused document checks
   use the writing scope. Before dependent implementation, operation or
   completion, confirm a current authority separate from the draft and apply
   [the lifecycle policy](../../docs/00.workspace/03.process/document-lifecycle.md#rules).
5. Resolve selected required-check tools, environment, actual resource/output
   needs, technical command limits and necessary native execution approval through
   [quality preflight](../../docs/00.workspace/04.quality/quality.md#validation-runner-envelope).
   Define focused checks, expected lanes, rollback, unavailable tools and next
   owner before implementation; protected authority remains separate.
   Quality preflight creates no business deadline, session timebox or
   final-validation reserve approval.

###### Resume

Apply the [context policy resume decision](../governance/context-and-memory.md#resume-decision)
before dependent writes. Put worktree identity and relevant file hashes under
Results, and current approval/revocation and writer ownership under
Inputs and Authority. Carry command limits, partial output and known
budget state with the lane results and limitations of the Next Owner section
(the [handoff fields](../../docs/00.workspace/04.quality/quality.md#handoff-evidence-contract)). On conflict, retain completed work and name the
next owner; refresh the affected evidence before resuming.

###### Implementation

Make the smallest testable change. Demonstrate a focused failing case for a
changed executable behavior, then its passing result; use selected profile,
relationship, link and state checks for narrative documents. Keep active Task
evidence current. Before retiring a one-use check, transfer its ongoing
protection, remove its caller and registration, then its dedicated helper,
fixture and test when consumer-zero and Git recovery are established. Preserve
the past result in its existing Task or Git history. Use
[delegated development](delegated-development.md) for authorized subagents.

For an ordinary authored document or README router edit, select common diff,
applicable style and commit-message checks plus document content only, as
[quality](../../docs/00.workspace/04.quality/quality.md#ordinary-document-selection) defines. Do
not add a one-use test just to mirror prose. Treat changes to governance,
provider or native contracts, Stage 99 forms, schema or registry, and
implementation as their own contract or behavior changes with necessary
focused regressions. Document writer commands remain explicit, never an
automatic QA side effect.

Bound the attempt. Stop and report instead of continuing when the same check
fails twice with no new information, when two consecutive changes produce no
observable progress, when a repair would require widening the approved scope,
or when the obstacle is an unmet authority, an unavailable environment, or an
external limit. Classify the stop as a repository defect, a missing protected
approval, an unavailable tool or environment, a resource limit, or an authority
conflict, and name the next owner. Stop the dependent action and continue
independent approved safe work. Never weaken a contract, a gate, or a test to
end the loop.

###### Completion

1. Check acceptance, links, owner boundaries, language, and README navigation
   through the [semantic review contract](../../docs/00.workspace/04.quality/quality.md#semantic-review):
   a recorded risk class, applicable automated checks, a core-diff checklist
   and the owner's explicit acceptance. Apply the independent-review requirement
   to high-risk changes.
2. Follow the delivery route and ordered sequence in
   [quality policy](../../docs/00.workspace/04.quality/quality.md#delivery-ownership). Record local
   selected QA and pre-commit lint/format over their actual snapshots. PR branch
   metadata and the selected hosted `style-pr` leaves have distinct SHA/run
   evidence. Push and merge do not replay an identical leaf.
3. Review final diff scope and remove task-owned scratch/debug residue.
4. Record the canonical handoff fields in the active Task; include failures,
   skipped optional tools, unavailable runtime checks, review disposition,
   rollback, residual risk, and next owner. Write residue as a `Residue Handoff`
   row in that Task and an entry in the work residue ledger in the same change;
   a terminal entry leaves the ledger before its package exit.
5. Follow [Git policy](../../docs/00.workspace/03.process/git.md) for requested logical commits and
   branch finish. Do not infer push, merge, or cleanup approval.

Hooks are supplemental evidence or enforcement only when their intended
runtime actually loads them. Advisory compaction output is not completion
evidence, and the progress-ledger rule belongs to [context and memory](../governance/context-and-memory.md#objective).

##### Failure Handling

The stop rule is stated under Implementation in Steps ("Bound the attempt").

#### Outputs

##### Artifacts

This procedure defines no output format of its own beyond the results its Steps describe; if it needs one, define it here.

##### Handoff

Completion and handoff are stated under Completion in Steps.

#### Verification

##### Checks

Run the selected static checks and preserve exact results. Review this
procedure when intake, delegation, completion, or handoff routing changes;
keep shared lane meanings in quality policy.

##### Limits

The selected static checks do not establish provider-native or live behavior, and advisory compaction output is not completion evidence. Hooks are evidence or enforcement only when their intended runtime loads them, and quality preflight creates no business deadline, session timebox or final-validation reserve approval.

## 적용과 확인

### 적용 방법

각 단계와 실패 처리 규칙을 명시된 조건에 따라 적용한다.

### 확인 기준

지정된 검사를 실행하고 실제 근거 수준을 보고한다.

## 관계와 출처

### 관련 문서

본문의 관련 문서가 정책과 책임 소유자를 연결한다.

### 외부 근거

인용된 저장소 소유 문서가 이 절차를 정한다. 외부 자료는 참고 근거다.
