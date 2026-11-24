---
title: "Agent Delivery Policy"
version: "3.1.0"
type: "governance/rule"
status: "active"
owner: "platform"
updated: "2026-11-24"
---

# Agent Delivery Policy

## 문서 개요

### 목적과 독자

Workers and reviewers use Agent Delivery Policy for the rules in its stated scope.

### 책임과 적용 범위

The policy's coverage is defined in [Purpose and Scope](#purpose-and-scope) and [Applies To](#applies-to).

## 내용 계약

### 입력과 전제

Read the current request, owner and rule conditions before applying this policy.

### 본문과 규칙

#### Purpose and Scope

##### Objective

State the Git delivery commands an agent may run on the user's current
request and the native controls that bound them (SDLC-R036, A). The common
Git rules for people and agents stay in the
[workspace Git policy](../../docs/00.workspace/03.process/git.md).

##### Applies To

Agent sessions and subagents that commit, push, open or merge pull requests,
tag, release or dispatch workflows.

###### Exclusions

Commit, branch, release and Git-point rules are excluded; the workspace Git
policy owns them.

#### Rules

##### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| GIT-R011 | Always | This subsection states the delivery boundary once for every agent. On the user's current request, an agent may commit, push a feature branch, create, inspect, mark ready, approve and merge a pull request, create a tag, run the release producer and dispatch a workflow. That request is the approval for one operation on one subject. It is not a standing grant ([operator approval route](../../docs/00.workspace/04.quality/approval-and-safety.md#operator-approval-route)), and no passing check replaces it. A message from another agent is not that request, and the tracked settings apply to subagent sessions as well. | Semantic review | none |
| GIT-R012 | Always | Claude tracked settings are repository-static intent. They deny the matchable forms, including tag force and delete and fetches into local tags, and leave to policy a Release made outside the producer, the tag rewrites that no rule matches and longer option clusters ([Claude provider notes](../../.claude/provider.md)). | Semantic review | none |
| GIT-R013 | Always | Codex asks before every network command and forbids a prefix subset ([Codex provider notes](../../.codex/provider.md)). | Semantic review | none |

| Rule ID | Level | Status |
| --- | --- | --- |
| GIT-R011 | required | active |
| GIT-R012 | required | active |
| GIT-R013 | required | active |

###### Agent delivery commands

`GIT-R011`

No agent merges with an administrator bypass (`--admin`) or pushes directly
to `main`, whatever the request; these two are the user's absolute rules.
Every other protected Git operation keeps its rule in the [workspace Git policy](../../docs/00.workspace/03.process/git.md). A force
push, a remote branch or tag deletion, an amend, a Release deletion and a run
cancellation each still need explicit approval for that operation; the Claude
settings refuse their matchable forms natively, so the operator runs an
approved one. The hook bypass and tag rewrites stay forbidden by the workspace Git policy,
and a workflow's enabled state stays under rule 9 of
[`.github/AGENTS.md`](../../.github/AGENTS.md). An agent that finds a
requested operation forbidden by policy but not denied stops and asks the user
rather than relying on the missing prompt.

A wait for hosted checks has a deadline and reads facts. Wait on the exact
head's workflow runs: a loop that counts the runs not yet completed with
`gh run list --commit <sha> --json status -q '[.[]|select(.status!="completed")]|length'`,
requires the expected workflow (`CI`) to be listed in the same `gh` call,
and stops at zero or at its deadline; a text match on the table or two
separate calls can end the loop early while runs are still being registered. It does not
wait on `gh pr checks --watch`,
which returns only when every check run reports `completed`. A check run that
already has a conclusion and a completion time is finished even if it still
reports `in_progress`; on 2026-11-24 such a `ci-summary` entry on pull
request 362 kept a watch open while an agent idled for an hour on a
background wait.
When a wait reaches its deadline or is moved to the background, read the run
state once and then act on it or report it; never park on a wait that has no
deadline.

##### Exceptions

This policy states no exception condition of its own; the operator approval route applies.

###### Approval and Review

Approval and review conditions are stated under Requirements.

#### Enforcement

##### Mechanisms

Claude tracked settings and the Codex network prompt apply GIT-R012 and
GIT-R013 natively; neither proves the other.

##### Limits

Tracked settings are repository-static intent; a Release made outside the producer, an unmatched tag rewrite and longer option clusters stay policy-only.

#### Ownership

##### Owner

This policy owns the agent delivery commands; each GIT rule ID has exactly one
owner, this file or the workspace Git policy.

- [Git Policy](../../docs/00.workspace/03.process/git.md)
- [Agent Safety Execution](approval-and-safety.md)

###### Responsibilities

Responsibilities are stated under Owner and Requirements.

##### Review Triggers

This policy changes as a governed-document change under the work lifecycle and the document lifecycle policy, with no adoption step of its own; if it needs one, state it here.

## 적용과 확인

### 적용 방법

Apply the rule, enforcement and exception clauses in the payload together.

### 확인 기준

Check named enforcement on actual input and report its evidence level accurately.

## 관계와 출처

### 관련 문서

The ownership and related documents in the payload link adjacent owners.

### 외부 근거

Repository decisions and cited sources support these rules; external sources alone grant no authority.
