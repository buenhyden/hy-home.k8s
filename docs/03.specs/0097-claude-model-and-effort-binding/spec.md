---
title: "Claude Model and Effort Binding Technical Specification"
version: "0.1.0"
type: "sdlc/spec"
status: "active"
owner: "platform"
updated: "2026-09-27"
layer: "specs"
artifact_id: "SPEC-0097"
---

# Claude Model and Effort Binding Technical Specification (Spec)

## Overview

The request owner asked on 2026-09-27 for Claude's handling of the
`.claude/agents` roles, agents, models, and reasoning effort to be checked and
fixed. They allowed the latest models and asked for Fable 5.1 to be kept to a
minimum: only roles that need thinking and planning get it, and practical roles
get a lower model. The check found three gaps.

- **Effort**: the [subagent documentation](https://code.claude.com/docs/en/sub-agents)
  supports an `effort` field (`low`, `medium`, `high`, `xhigh`, `max`). The
  registry bound effort only for Codex, and the validator rejected any other
  Claude frontmatter key, so no Claude role could declare its effort.
- **Model**: the tier aliases `opus` and `sonnet` already resolve to the latest
  generation, but no role could depart from its tier's Claude model.
- **Tools**: on native Linux and macOS builds from 2.1.117, the client removed
  `Grep` and `Glob` and moved search into Bash. The projections still declare
  both, and the client drops them silently
  ([anthropics/claude-code#80526](https://github.com/anthropics/claude-code/issues/80526)).

This Spec owns the Claude effort binding, the Claude model departure, and the
record of the tool gap.

## Strategic Boundaries & Non-goals

In scope: the Claude `capability_reasoning` entry, the `claude` keys of
`native_reasoning_override` and `native_model_override`, their schema and
validator rules, the `model` and `effort` values of each `.claude/agents/*.md`
projection, the model-selection policy sentence on bindings, the Claude
provider note, and this package.

Out of scope: Codex bindings; tier membership; permission classes and tool
scopes, including any change to `Grep`, `Glob`, or `Bash` grants; user-level
Claude settings.

## Contracts

- A capability tier binds the Claude effort for every role that carries it, as
  it already does for Codex. A role whose effort or model genuinely differs
  declares the `claude` key of the matching override.
- The validator resolves each Claude projection's `model` and `effort` from the
  registry and rejects drift.
- `fable` is bound only to roles whose responsibility is planning,
  orchestration, or structural design.

## Core Design

| Scope | Roles | Model | Effort |
| --- | --- | --- | --- |
| `top` override | supervisor, architect | `fable` (Fable 5.1) | `xhigh` |
| `top` tier | governance-steward | `opus` (Opus 5.5) | `xhigh` |
| `top` tier, effort override | incident-responder, security-auditor | `opus` | `high` |
| `worker` tier | ten roles | `sonnet` (Sonnet 5) | `high` |
| `worker` tier, effort override | doc-writer, wiki-curator | `sonnet` | `medium` |

The effort values mirror the Codex bindings, so a role asks for the same
reasoning depth on both providers. Aliases stay in the projections, so each
tier follows the newest generation without a pin. Fable goes only to the two
planning roles, the same scope as `gpt-6-astra` on Codex under SPEC-0096.

## Data Modeling & Storage Strategy

The registry holds the bindings and overrides, and each projection restates the
resolved values. The schema adds `claudeReasoningEffort`, a required Claude
`capability_reasoning`, and `claude` keys on both override objects.

## Interfaces & Data Structures

- `_bound_reasoning(registry, role, provider="codex")` resolves either provider.
- The Claude projection check admits `effort` and requires it to equal the
  resolved binding.

## Edge Cases & Error Handling

A running session keeps the agent definitions it loaded at start, so a changed
projection takes effect only in a new session. A missing or drifted `effort`
fails `AGENT-NATIVE-METADATA`.

## Failure Modes & Fallback / Human Escalation

The tool gap is recorded, not fixed. Roles without `Bash`
(docs-researcher, incident-responder, observability-reviewer, supervisor) have
no search tool on native builds. Granting `Bash` widens a permission class, so
it needs the request owner's decision and a governance-steward change.

## Verification Commands

```bash
python3 scripts/validate-agent-governance.py --root .
python3 -m unittest tests.test_validate_agent_registry
python3 scripts/qa.py staged
```

## Success Criteria & Verification Plan

| ID | Criterion | Evidence |
| --- | --- | --- |
| VAL-CMB-001 | Every Claude projection's `model` and `effort` resolve from the registry, and drift is rejected | Unit tests and governance validator |
| VAL-CMB-002 | `fable` is bound only to supervisor and architect | Registry and projections |
| VAL-CMB-003 | Spawned roles in a new session apply the bound model and effort | Transcript records in the Task |
| VAL-CMB-004 | The `Grep` and `Glob` gap is recorded with an owner | Task and provider note |

## Traceability

The [Implementation Plan](plan.md) owns order and risk. The
[Task](tasks/tsk-0001-bind-claude-model-and-effort.md) owns the evidence.

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0003-FR-0025](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-CMB-001 | Unit tests and validator |
| [REQ-0003-FR-0025](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-CMB-002 | Registry and projections |
| [REQ-0003-FR-0025](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-CMB-003 | Transcript records |
| [REQ-0003-FR-0025](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-CMB-004 | Task and provider note |
