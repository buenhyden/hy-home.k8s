---
title: "Change Review Prompt Contract"
version: "1.1.0"
type: "governance/prompt"
status: "draft"
owner: "platform"
updated: "2026-11-20"
---

# Change Review Prompt Contract

## 문서 개요

### 목적과 독자

이 prompt 계약은 Change Review Prompt Contract 요청을 구성하는 작성자와 그 결과를 검토하는 역할에게 입력·출력 경계를 제공한다. 요청 목적은 [Overview](#overview)에 기록한다.

### 책임과 적용 범위

platform은 이 prompt 계약을 유지한다. 허용 권한은 [Authority Boundary](#authority-boundary), 필수 입력은 [Inputs](#inputs)에 기록하며 실행 권한을 추가하지 않는다.

## 내용 계약

### 입력과 전제

입력과 전제는 아래 역할별 본문의 해당 절에 기록한다.

### 본문과 규칙

#### Overview

Identifier `change-review`. Assemble a review request for the actual candidate
before commit or handoff. The local builder collects unstaged and staged diffs;
the requesting author supplies the base-to-candidate diff when reviewing a
commit or PR candidate. The review lens follows the current requirement and
affected consumers, rather than the author's expected conclusion.

#### Authority Boundary

A review lens is not write access. This contract selects what a reviewer reads;
the agent registry keeps permission classes and the approval policy keeps
protected actions. The contract names no reviewer role and grants none.

#### Inputs

| Input | Command | Why it is needed |
| --- | --- | --- |
| Local difference | `git diff` | The subject of the review |
| Staged difference | `git diff --cached` | Separates what is already staged from what is not |
| Changed path set | `git status --porcelain` | Establishes the owner boundaries the change touches |
| Whitespace check | `git diff --check` | A defect class a reviewer should not have to find by eye |
| Staged paths | `git diff --cached --name-only` | The exact path set that the staged checks ran on |

The subject inputs are `Local difference` and `Staged difference`. When both
are empty the contract refuses, because there is no difference to review.

The requesting author also supplies, once, the review packet that Git cannot,
so the reviewer does not reconstruct it ([QUAL-R055](../../docs/00.workspace/04.quality/quality.md#requirements)):

- the current user request, applicable Spec and design, acceptance IDs, and
  the concrete behavior expected of affected consumers;
- the actual candidate and base: branch, commit when one exists, changed paths
  and the full local or base-to-candidate diff being reviewed;
- the risk class, impact and authority reason (QUAL-R016), affected permissions
  and approved cost limits;
- for a change to a governance, role, skill or provider file, its Kubernetes
  impact: the GitOps or infrastructure consumers whose behavior it changes, or
  `none`. Such a change may select only document checks (for example
  `.agents/governance/`), so the reviewer checks this statement against
  `gitops/` and `infrastructure/`;
- check results already observed on the candidate, with their snapshot, and
  known failures, unsupported conditions and unobserved scope; the reviewer
  does not rerun a check to repeat a PASS;
- for a re-review, the reviewed commit, the earlier findings and the
  `scripts/review_delta.py` result (QUAL-R054);
- the review surface and actual source-write boundary evidence when required.

Start a fresh review context with these inputs, without the implementer's
proposed verdict or self-evaluation. The reviewer tests reachable failure
conditions, affected consumers, complexity and rule conflicts. A medium-risk
review uses a focused non-implementer; a high-risk review also needs the
verified read-only boundary and relevant domain expertise of QUAL-R015. Do not
send the same unchanged candidate to two paid providers by default.

#### Output

An ordered finding list, one finding per root cause. Each finding names the
file and line, states the defect in one sentence, gives the concrete condition
under which it goes wrong, and carries its grade under
[QUAL-R053](../../docs/00.workspace/04.quality/quality.md#requirements). A finding without a failure
condition is a preference and is reported as `NOTE`. State the exact reviewed
candidate and scope, the review surface, enforcement status (`enforced`,
`failed`, `unobserved`, `unsupported`), observed source-write result
(`denied`, `allowed`, `unobserved`), and any excluded runtime or consumer scope.
A review verdict is neither an execution grant nor user acceptance.

#### Validation

Findings are checked against the candidate and affected consumers before they
are acted on. A finding on an unchanged consumer names the changed cause and
the reachable failure it introduces. A finding unsupported by either the
diff or its affected consumer is discarded rather than reported. Recheck only
the semantic delta and its affected findings after repair; factual evidence
alone does not cause a new whole review under QUAL-R054.

#### Refusal Conditions

The builder enforces only the empty-subject refusal; the requesting agent
enforces the remaining conditions below.

- Both builder differences are empty, so that local builder has nothing to
  review. An untracked-only path set does not establish a reviewable diff;
  supply the actual content or a commit candidate for review.
- The request asks for a verdict on live cluster, hosted, or provider-runtime
  behavior, which a local difference cannot establish.
- The request asks to review content the approval boundary excludes from
  reading, such as credentials or environment dumps.

#### Related Documents

- [Common Prompt Contracts](README.md)
- [Agent Responsibilities](../roles/README.md)
- [Quality and Evidence Policy](../../docs/00.workspace/04.quality/quality.md)

## 적용과 확인

### 적용 방법

아래 역할별 본문에 기록된 사용 조건과 절차를 적용한다.

### 확인 기준

아래 역할별 본문의 검증·확인 조건과 그 한계에 따른다.

## 관계와 출처

### 관련 문서

관련 문서와 정본 링크는 아래 역할별 본문에서 확인한다.

### 외부 근거

외부 근거가 사용된 경우 아래 역할별 본문의 출처와 적용 범위에서 확인한다.
