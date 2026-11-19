---
title: "Agent Delivery Policy"
version: "2.11.0"
type: "governance/rule"
status: "active"
owner: "platform"
updated: "2026-11-19"
---

# Agent Delivery Policy

## Purpose and Scope

### Objective

State the Git delivery commands an agent may run on the user's current
request and the native controls that bound them (SDLC-R036, A). The common
Git rules for people and agents stay in the
[workspace Git policy](../../docs/00.workspace/03.process/git.md).

### Applies To

Agent sessions and subagents that commit, push, open or merge pull requests,
tag, release or dispatch workflows.

#### Exclusions

Commit, branch, release and Git-point rules are excluded; the workspace Git
policy owns them.

## Rules

### Requirements

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

#### Agent delivery commands

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

### Exceptions

This policy states no exception condition of its own; the operator approval route applies.

#### Approval and Review

Approval and review conditions are stated under Requirements.

## Enforcement

### Mechanisms

Claude tracked settings and the Codex network prompt apply GIT-R012 and
GIT-R013 natively; neither proves the other.

### Limits

Tracked settings are repository-static intent; a Release made outside the producer, an unmatched tag rewrite and longer option clusters stay policy-only.

## Ownership

### Owner

This policy owns the agent delivery commands; each GIT rule ID has exactly one
owner, this file or the workspace Git policy.

- [Git Policy](../../docs/00.workspace/03.process/git.md)
- [Agent Safety Execution](approval-and-safety.md)

#### Responsibilities

Responsibilities are stated under Owner and Requirements.

### Review Triggers

This policy changes as a governed-document change under the work lifecycle and the document lifecycle policy, with no adoption step of its own; if it needs one, state it here.
