---
title: "Approval and Safety Policy"
version: "2.0.0"
type: "governance/rule"
status: "active"
owner: "platform"
updated: "2026-11-20"
---

# Approval and Safety Policy

## 문서 개요

### 목적과 독자

Workers and reviewers use Approval and Safety Policy for the rules in its stated scope.

### 책임과 적용 범위

The policy's coverage is defined in [Purpose and Scope](#purpose-and-scope) and [Applies To](#applies-to).

## 내용 계약

### 입력과 전제

Read the current request, owner and rule conditions before applying this policy.

### 본문과 규칙

#### Purpose and Scope

##### Objective

Agents prepare desired-state changes and local evidence within the user's
scope. Protected actions require explicit human or operator authority.

##### Applies To

Kubernetes, Argo CD, Vault, cloud, remote Git, and CI operations affect state
outside the reviewable repository. Keep those actions separate from writing
and validating their configuration.

This workspace policy owns what a protected action is, what an approval binds
and how the operator verifies it, for people and agents alike (W, SDLC-R036).
How an agent compares its call with a bound approval, delegates and is
confined by tool permissions (SAFE-R011, SAFE-R012 and SAFE-R017 to
SAFE-R019) is owned once by the
[agent safety execution policy](../../../.agents/governance/approval-and-safety.md).

- Operations Index (`docs/05.operations/README.md`)

###### Exclusions

This policy excludes no subject within its scope; if one is excluded, name it and its owner here.

#### Rules

##### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| SAFE-R001 | Always | Repository docs, manifests, tests, and scripts | Semantic review | none |
| SAFE-R002 | Always | Bootstrap and recovery assets | Semantic review | none |
| SAFE-R003 | Always | CI configuration | `github-actions-security` | none |
| SAFE-R004 | Always | Git history and worktrees | Semantic review | none |
| SAFE-R005 | Always | Live cluster, Argo CD, Vault, and cloud | Semantic review | none |
| SAFE-R006 | Always | Secrets and private runtime data | `secret-handling` | none |
| SAFE-R007 | Always | Scoped local authoring includes development and operating documents, redacted examples, synthetic inputs and non-secret management metadata. A dangerous command cited in that content is data, not a tool invocation or authorization. Document its execution boundary; never inspect a real secret to produce an example. A runnable raw secret-output command does not become safe because a nearby sentence says `redacted` or `metadata-only`. An explicitly inert prohibited example is different from a suggested operating step. | Semantic review | none |
| SAFE-R008 | Before a protected operation | There is no repository mechanism that authenticates an approving actor. The request owner/operator verifies approval through the original trusted interaction or native approval interface. Before a protected operation: | Semantic review | none |
| SAFE-R009 | Before a protected operation | Bind the approving actor and responsible executor, exact operation, subject or target, current request revision, reviewed revision/snapshot, and applicable validity conditions. | Semantic review | none |
| SAFE-R010 | Before a protected operation | Verify the original approval and current revocation state through that trusted interaction. Record its non-secret reference and the operator's verification result in the owning Task or incident; do not copy credentials or transcripts. A writer may record supplied facts but cannot invent an actor, approval, authentication result or revocation check. | Semantic review | none |
| SAFE-R013 | Always | `kubectl apply/patch/delete`, Helm installation or upgrade, forced Argo CD reconciliation, and external secret writes are not default agent actions; each runs only as an operator-approved action under SAFE-R005 and SAFE-R008. | Semantic review | none |
| SAFE-R014 | Always | Never read or record tokens, authentication files, private keys, plaintext Kubernetes secrets, shell history, raw transcripts, or environment dumps. The one exception is the session capture route of CTX-R022 in the context and memory policy, which reads this workspace's own transcripts to record pointers and structure and never their text. Secret-bearing scratch needs human-directed handling; do not destroy local evidence under a generic cleanup request. | `secret-handling` | none |
| SAFE-R015 | When reviewing an ExternalSecret | ExternalSecret reviews use only secret references, mount, and property names, never their values. Follow existing isolation and AppProject controls. | `vault-eso-contracts` | none |
| SAFE-R016 | Always | GitHub Actions is repository QA/CI, not live deployment CD. | Semantic review | none |
| SAFE-R020 | When authority is missing | Missing authority stops the protected operation at its local draft, not independent approved authoring. | Semantic review | none |
| SAFE-R021 | Always | Safety denial is an authorization boundary. Cost, time and output limits, and the rule that a technical resource limit is no secret/live approval, business deadline, session timebox or validation reserve, belong to [quality](quality.md#validation-runner-envelope). Preserve failures and obtain necessary native permission for actual resources without bypassing a guard or misreporting an unexecuted check. | Semantic review | none |

| Rule ID | Level | Status |
| --- | --- | --- |
| SAFE-R001 | required | active |
| SAFE-R002 | required | active |
| SAFE-R003 | required | active |
| SAFE-R004 | required | active |
| SAFE-R005 | required | active |
| SAFE-R006 | required | active |
| SAFE-R007 | required | active |
| SAFE-R008 | required | active |
| SAFE-R009 | required | active |
| SAFE-R010 | required | active |
| SAFE-R013 | required | active |
| SAFE-R014 | required | active |
| SAFE-R015 | required | active |
| SAFE-R016 | required | active |
| SAFE-R020 | required | active |
| SAFE-R021 | required | active |

| Rule ID | Default | Approval boundary |
| ---------------------------------------------- | ----------------------------------------------- | ---------------------------------------------------------------------------------------- |
| SAFE-R001 | Scoped edits and deterministic local validation | Scope expansion or weakened security/gate failure semantics |
| SAFE-R002 | Edit and review only | Running against a cluster or external service |
| SAFE-R003 | Scoped static edits | Permission expansion, protected triggers, publishing, paid execution, or remote dispatch |
| SAFE-R004 | Inspect; make requested logical commits | Push, PR creation, merge, destructive cleanup, history rewrite, or worktree removal |
| SAFE-R005 | No mutation | Explicit operator action with target, command class, rollback, and evidence |
| SAFE-R006 | Do not read or record values | Stop and use the approved secret/incident process; never expose values |

###### Authoring and execution

`SAFE-R007`

Repairing this policy and its consumers under an explicit scoped request is
ordinary authoring, including removal of a contradictory local rule. Keep the
latest authorized intent and revise the affected contract together. This
does not let a role expand its own permissions or bypass a provider deny,
sandbox, trust requirement or tool approval. An actual native restriction
requires its supported operator path; changing the command or wrapper to evade
it is forbidden.

Read-only reviewers report findings. Route a repair to an approved writer with
the relevant Task and paths; review does not grant writes or authorization.
Reuse valid approval for the same scope, subject and reviewed revision rather
than asking the human to repeat a completed routine review.

###### Operator approval route

`SAFE-R008`

Before a protected operation, the owning Task or incident also records rollback
or backup and required evidence.

Document validators check structure, relationships and recovery objects only.
A Git object, lifecycle status, checkbox, historical quote, successful QA or
reviewer verdict is no approval. Historical approval is evidence of a past
decision, never a reusable standing grant. The operator route does not
delegate live/secret operations to a subagent.

###### Execution controls

- `SAFE-R013`
- `SAFE-R014`
- `SAFE-R015`
- `SAFE-R016`
- `SAFE-R020`
- `SAFE-R021`

##### Exceptions

This policy states no exception condition of its own; the operator approval route is stated under Requirements.

###### Approval and Review

Approval and review conditions are stated under Requirements.

#### Enforcement

##### Mechanisms

Run the affected safety, secret-handling, permission, and policy checks when a
protected surface changes. Report unexecuted external checks using the
[quality result vocabulary](quality.md#result-vocabulary). Never bypass a
failing required check or provider restriction.

##### Limits

A Python or Node script that opens files itself stays outside shell-write observation, and so do permission rules that match shell file commands, so instruction-level and rule-level controls are advisory for that class. SAFE-R018 states that `read-only-evidence` names what the registry grants, not what an operating system enforces, and the two supported providers differ under that one name. External checks that were not executed are reported as such rather than counted as passed.

#### Ownership

##### Owner

This policy owns approval decisions. Native sandbox, tool, permission, and
approval controls may be stricter; static configuration never proves runtime
enforcement. Runbooks describe authorized procedures, not standing approval.

- [Agent Execution](../../../.agents/governance/agent-execution.md)
- [Git Policy](../03.process/git.md)
- [Quality Policy](quality.md)

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
