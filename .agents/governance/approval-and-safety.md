---
title: "Approval and Safety Policy"
version: "1.7.0"
type: "governance/rule"
status: "active"
owner: "platform"
updated: "2026-11-17"
---

# Approval and Safety Policy

## Purpose and Scope

### Objective

Agents prepare desired-state changes and local evidence within the user's
scope. Protected actions require explicit human or operator authority.

### Applies To

Kubernetes, Argo CD, Vault, cloud, remote Git, and CI operations affect state
outside the reviewable repository. Keep those actions separate from writing
and validating their configuration.

- Operations Index (`docs/05.operations/README.md`)

#### Exclusions

This policy excludes no subject within its scope; if one is excluded, name it and its owner here.

## Rules

### Requirements

| Rule ID | Condition | Level | Evidence | Status |
| --- | --- | --- | --- | --- |
| SAFE-R001 | Always | required | Semantic review | active |
| SAFE-R002 | Always | required | Semantic review | active |
| SAFE-R003 | Always | required | `github-actions-security` | active |
| SAFE-R004 | Always | required | Semantic review | active |
| SAFE-R005 | Always | required | Semantic review | active |
| SAFE-R006 | Always | required | `secret-handling` | active |
| SAFE-R007 | Always | required | Semantic review | active |
| SAFE-R008 | Before a protected operation | required | Semantic review | active |
| SAFE-R009 | Before a protected operation | required | Semantic review | active |
| SAFE-R010 | Before a protected operation | required | Semantic review | active |
| SAFE-R011 | Immediately before execution and again on resume | required | Semantic review | active |
| SAFE-R012 | Always | required | Semantic review | active |
| SAFE-R013 | Always | required | Semantic review | active |
| SAFE-R014 | Always | required | `secret-handling` | active |
| SAFE-R015 | When reviewing an ExternalSecret | required | `vault-eso-contracts` | active |
| SAFE-R016 | Always | required | Semantic review | active |
| SAFE-R017 | Always | required | `scripts/provider_write_guard.py` | active |
| SAFE-R018 | Always | required | `agent-governance` | active |
| SAFE-R019 | Always | required | `agent-governance` | active |
| SAFE-R020 | When authority is missing | required | Semantic review | active |
| SAFE-R021 | Always | required | Semantic review | active |

| Surface                                        | Default                                         | Approval boundary                                                                        |
| ---------------------------------------------- | ----------------------------------------------- | ---------------------------------------------------------------------------------------- |
| `SAFE-R001` Repository docs, manifests, tests, and scripts | Scoped edits and deterministic local validation | Scope expansion or weakened security/gate failure semantics                              |
| `SAFE-R002` Bootstrap and recovery assets                  | Edit and review only                            | Running against a cluster or external service                                            |
| `SAFE-R003` CI configuration                               | Scoped static edits                             | Permission expansion, protected triggers, publishing, paid execution, or remote dispatch |
| `SAFE-R004` Git history and worktrees                      | Inspect; make requested logical commits         | Push, PR creation, merge, destructive cleanup, history rewrite, or worktree removal      |
| `SAFE-R005` Live cluster, Argo CD, Vault, and cloud        | No mutation                                     | Explicit operator action with target, command class, rollback, and evidence              |
| `SAFE-R006` Secrets and private runtime data               | Do not read or record values                    | Stop and use the approved secret/incident process; never expose values                   |

#### Authoring and execution

`SAFE-R007`

Scoped local authoring includes development and operating documents, redacted
examples, synthetic inputs and non-secret management metadata. A dangerous
command cited in that content is data, not a tool invocation or authorization.
Document its execution boundary; never inspect a real secret to produce an
example. A runnable raw secret-output command does not become safe because a
nearby sentence says `redacted` or `metadata-only`. An explicitly inert
prohibited example is different from a suggested operating step.

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

#### Operator approval route

`SAFE-R008`

There is no repository mechanism that authenticates an approving actor.
The request owner/operator verifies approval through the original trusted
interaction or native approval interface. Before a protected operation:

1. `SAFE-R009` Bind the approving actor and responsible executor, exact operation, subject
   or target, current request revision, reviewed revision/snapshot, and applicable
   validity conditions.
2. `SAFE-R010` Verify the original approval and current revocation state through that
   trusted interaction. Record its non-secret reference and the operator's
   verification result in the owning Task or incident; do not copy credentials
   or transcripts. A writer may record supplied facts but cannot invent an
   actor, approval, authentication result or revocation check.
3. `SAFE-R011` Compare the intended invocation against those bound inputs immediately
   before execution and again on resume. Missing/unavailable source, mismatch,
   expiry or revocation does not authorize the dependent action. Continue
   independent safe work and route the blocked action to the operator.

Before a protected operation, the owning Task or incident also records rollback
or backup and required evidence.

Document validators check structure, relationships and recovery objects only.
A Git object, lifecycle status, checkbox, historical quote, successful QA or
reviewer verdict is no approval. Historical approval is evidence of a past
decision, never a reusable standing grant. The operator route does not
delegate live/secret operations to a subagent.

#### Execution controls

- `SAFE-R012` Subagents never mutate live clusters. Approved bootstrap or break-glass
  actions remain operator-bound, not delegated background work.
- `SAFE-R013` `kubectl apply/patch/delete`, Helm installation or upgrade, forced Argo CD
  reconciliation, and external secret writes are not default agent actions.
- `SAFE-R014` Never read or record tokens, authentication files, private keys, plaintext
  Kubernetes secrets, shell history, raw transcripts, or environment dumps.
  Secret-bearing scratch needs human-directed handling; do not destroy local
  evidence under a generic cleanup request.
- `SAFE-R015` ExternalSecret reviews use only secret references, mount, and property names,
  never their values. Follow existing isolation and AppProject controls.
- `SAFE-R016` GitHub Actions is repository QA/CI, not live deployment CD.
- `SAFE-R017` Write-path guards observe structured file tools, patch envelopes, and the
  obvious write targets of a shell command. A patch envelope's file headers
  reach the same evaluation a structured write reaches. A shell target does
  not: it is reported and never blocked. A program that opens files itself,
  such as a Python or Node script, stays outside the observation entirely, and
  so do permission rules that match shell file commands. Treat
  instruction-level and rule-level controls as advisory for that class.
- `SAFE-R018` `read-only-evidence` names what the registry grants, not what an operating
  system enforces, and the two supported providers differ under that one name.
  On Codex the class binds an operating-system `read-only` sandbox, which is a
  real boundary. On Claude it withholds the structured write tools and, for a
  role whose skills require one, leaves a shell through which a write is
  prohibited by policy and observed advisorily rather than prevented. Every
  Claude role carries `Bash` (SPEC-0098 in `.claude/provider.md`), and
  `.claude/bindings.json` declares no narrower scope, so a read-only role
  confines its shell to read-only repository search by policy. This difference
  is documented and accepted; do not describe it as parity, and do not report
  the weaker side's policy prohibition as an enforced control.
- `SAFE-R019` A neutral permission class sets the maximum reach. A provider binding may
  choose a narrower native scope within that ceiling, and a native
  `role_overrides.scope` may narrow the provider binding for one role. The
  projection must match the resulting binding exactly. The validator rejects
  any binding or projection that exceeds the neutral class ceiling, so a
  per-role exception cannot become a second permission authority. Network
  reach is therefore its own read-only class rather than an exception on the
  ordinary one: the role that researches primary sources carries it, and no
  other read-only role gains it by default.
- `SAFE-R020` Missing authority stops the protected operation at its local draft, not
  independent approved authoring.
- `SAFE-R021` Safety denial is an authorization boundary. Cost, time and output limits,
  and the rule that a technical resource limit is no secret/live approval,
  business deadline, session timebox or validation reserve, belong to
  [quality](quality.md#validation-runner-envelope). Preserve failures and
  obtain necessary native permission for actual resources without bypassing a
  guard or misreporting an unexecuted check.

### Exceptions

This policy states no exception condition of its own; the operator approval route is stated under Requirements.

#### Approval and Review

Approval and review conditions are stated under Requirements.

## Enforcement

### Mechanisms

Run the affected safety, secret-handling, permission, and policy checks when a
protected surface changes. Report unexecuted external checks using the
[quality result vocabulary](quality.md#result-vocabulary). Never bypass a
failing required check or provider restriction.

### Limits

A Python or Node script that opens files itself stays outside shell-write observation, and so do permission rules that match shell file commands, so instruction-level and rule-level controls are advisory for that class. SAFE-R018 states that `read-only-evidence` names what the registry grants, not what an operating system enforces, and the two supported providers differ under that one name. External checks that were not executed are reported as such rather than counted as passed.

## Ownership

### Owner

This policy owns approval decisions. Native sandbox, tool, permission, and
approval controls may be stricter; static configuration never proves runtime
enforcement. Runbooks describe authorized procedures, not standing approval.

- [Agent Execution](agent-execution.md)
- [Git Policy](git.md)
- [Quality Policy](quality.md)

#### Responsibilities

Responsibilities are stated under Authority and Requirements.

### Review Triggers

This policy changes as a governed-document change under the work lifecycle and the document lifecycle policy, with no adoption step of its own; if it needs one, state it here.
