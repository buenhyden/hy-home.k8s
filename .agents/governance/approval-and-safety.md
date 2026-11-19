---
title: "Agent Safety Execution Policy"
version: "1.9.0"
type: "governance/rule"
status: "active"
owner: "platform"
updated: "2026-11-19"
---

# Agent Safety Execution Policy

## Purpose and Scope

### Objective

State only how an agent applies the workspace
[approval and safety policy](../../docs/00.workspace/04.quality/approval-and-safety.md):
it compares its intended call with a bound approval, never delegates live
mutation, and reads tool permissions as advisory or enforced (SDLC-R036, A).
What a protected action is and what an approval binds stay in that policy.

### Applies To

Agent sessions, subagents, provider bindings and write-path guards.

#### Exclusions

The meaning of protected actions and the operator approval route are excluded;
the workspace approval and safety policy owns them.

## Rules

### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| SAFE-R011 | Immediately before execution and again on resume | Compare the intended invocation against those bound inputs immediately before execution and again on resume. Missing/unavailable source, mismatch, expiry or revocation does not authorize the dependent action. Continue independent safe work and route the blocked action to the operator. | Semantic review | none |
| SAFE-R012 | Always | Subagents never mutate live clusters. Approved bootstrap or break-glass actions remain operator-bound, not delegated background work. | Semantic review | none |
| SAFE-R017 | Always | Write-path guards observe structured file tools, patch envelopes, and the obvious write targets of a shell command. A patch envelope's file headers reach the same evaluation a structured write reaches. A shell target does not: it is reported and never blocked. A program that opens files itself, such as a Python or Node script, stays outside the observation entirely, and so do permission rules that match shell file commands. Treat instruction-level and rule-level controls as advisory for that class. | `scripts/provider_write_guard.py` | none |
| SAFE-R018 | Always | `read-only-evidence` names what the registry grants, not what an operating system enforces, and the two supported providers differ under that one name. On Codex the class binds an operating-system `read-only` sandbox, which is a real boundary. On Claude it withholds the structured write tools and, for a role whose skills require one, leaves a shell through which a write is prohibited by policy and observed advisorily rather than prevented. Every Claude role carries `Bash` (SPEC-0098 in `.claude/provider.md`), and `.claude/bindings.json` declares no narrower scope, so a read-only role confines its shell to read-only repository search by policy. This difference is documented and accepted; do not describe it as parity, and do not report the weaker side's policy prohibition as an enforced control. | `agent-governance` | none |
| SAFE-R019 | Always | A neutral permission class sets the maximum reach. A provider binding may choose a narrower native scope within that ceiling, and a native `role_overrides.scope` may narrow the provider binding for one role. The projection must match the resulting binding exactly. The validator rejects any binding or projection that exceeds the neutral class ceiling, so a per-role exception cannot become a second permission authority. Network reach is therefore its own read-only class rather than an exception on the ordinary one: the role that researches primary sources carries it, and no other read-only role gains it by default. | `agent-governance` | none |

| Rule ID | Level | Status |
| --- | --- | --- |
| SAFE-R011 | required | active |
| SAFE-R012 | required | active |
| SAFE-R017 | required | active |
| SAFE-R018 | required | active |
| SAFE-R019 | required | active |

#### Execution controls

- `SAFE-R011`
- `SAFE-R012`
- `SAFE-R017`
- `SAFE-R018`
- `SAFE-R019`

### Exceptions

This policy states no exception condition of its own; the workspace operator approval route applies.

#### Approval and Review

Approval and review conditions are stated under Requirements.

## Enforcement

### Mechanisms

The agent-governance check enforces the permission ceiling of SAFE-R019, and
`scripts/provider_write_guard.py` observes write paths under SAFE-R017.

### Limits

A Python or Node script that opens files itself stays outside shell-write observation, and so do permission rules that match shell file commands, so instruction-level and rule-level controls are advisory for that class. SAFE-R018 states that `read-only-evidence` names what the registry grants, not what an operating system enforces.

## Ownership

### Owner

This policy owns the agent execution differences of the SAFE rule set; each
SAFE rule ID has exactly one owner, this file or the workspace policy.

- [Approval and Safety](../../docs/00.workspace/04.quality/approval-and-safety.md)
- [Agent Execution](agent-execution.md)

#### Responsibilities

Responsibilities are stated under Owner and Requirements.

### Review Triggers

This policy changes as a governed-document change under the work lifecycle and the document lifecycle policy, with no adoption step of its own; if it needs one, state it here.
