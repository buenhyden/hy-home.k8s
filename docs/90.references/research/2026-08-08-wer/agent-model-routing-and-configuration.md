---
title: 'Reference: Agent Model Routing and Configuration'
type: content/reference
status: active
owner: platform
updated: 2026-08-08
---

# Reference: Agent Model Routing and Configuration

## Overview

This reference defines evidence-bound routing from task characteristics to a
role, tier, provider configuration, tool/sandbox boundary, and reviewer. It
does not select a new model or change an adapter.

## Reference Type

Repository-static research baseline.

## Authority Boundary

Model policy and the model-fitness contract own the local tier and promotion
contract; provider documentation owns provider configuration vocabulary.
Tracked adapters prove a configured incumbent only. Authentication, model
availability, parsing, resolution, performance, cost, latency, and access are
`DEFER` without matching evidence.

## Scope

It covers task-characteristic routing, model/reasoning configuration,
evaluation, fallback, and promotion. It does not reassign roles, consume an
account catalog, or alter provider configuration.

## Definitions / Facts

### Model-routing baseline

The workspace policy assigns `top` to planning/supervision and `worker` to
bounded implementation, validation, and focused edits. A worker may escalate a
high-risk governance, security, or cluster-affecting review without changing
its role class. Exact provider tuples, candidates, incumbent values, reasoning
support, evaluation readiness, and promotion state live in
`contracts/agent-model-fitness.json`; all observed runtime/promotion/canary
tuples remain `DEFER`.

| Task characteristics | Role / tier | Tool and sandbox expectation | Review / promotion rule |
| --- | --- | --- | --- |
| Bounded documentation, inventory, formatting, or deterministic validation | Named worker | Read-only or minimal workspace-write surface; no credentials/live tools. | Normal reviewer when the change is material; validation evidence is required. |
| Cross-file architecture, conflicting sources, or multi-agent coordination | Supervisor / `top` | Narrow delegation and explicit ownership; preserve a shared evidence ledger. | Independent review before canonical decision or broad edit. |
| Security, GitOps, incident, destructive, or external-affecting work | Specialist with risk-appropriate tier | Least privilege; human approval controls live/secret/remote/destructive tools. | Independent specialist review and explicit rollback/handoff; no self-promotion. |
| Unknown model fitness or provider feature | Existing safe incumbent or no execution | Do not broaden tools or change configuration to compensate. | `DEFER`; collect approved parsing and same-suite evaluation evidence first. |

### Configuration baseline

Codex's current configuration reference documents `agents.<name>` settings and
`model_reasoning_effort` values `minimal`, `low`, `medium`, `high`, and
`xhigh`; support for `xhigh` is model-dependent. Claude documents task-specific
subagent model/tool configuration. These current product facts do not prove
this worktree's effective provider configuration. Local adapters and the
model-fitness contract remain the repository-static incumbent projection.

### Routing, evaluation, and fallback rules

1. Select risk, reversibility, sensitivity, required context, and independent
   review before selecting a provider/model name.
2. Select the local role and `top`/`worker` tier, then the smallest permitted
   provider configuration that the contract records.
3. Treat reasoning effort as configured intent, never as universal quality or
   a measured cost/latency property.
4. A configuration change needs platform-owner authorization, official source
   recheck, successful parsing/resolution without silent fallback, same-suite
   evaluation against the incumbent, threshold/adjudication evidence, a
   canary where relevant, and a rollback record.
5. If an evaluation is unavailable or fails, preserve the approved incumbent,
   narrow the task or add review; do not infer a better model from its name.

### Evidence and confidence boundaries

`Implemented` applies to the static tier/contract and declared adapter
projection. `Partial` may describe a locally recorded candidate or evaluation
readiness. Provider-runtime model resolution, actual reasoning support,
token/cost/latency measurements, account availability, and canary outcomes are
`DEFER`. Product-specific surfaces (Codex CLI, OpenAI API/SDK, and Claude Code)
are separate: evidence for one does not transfer to another.

## Sources

- [OpenAI Codex configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference), checked 2026-08-08 (`SRC-WERPC-049`).
- [OpenAI Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) and [OpenAI Agents SDK sessions](https://openai.github.io/openai-agents-python/sessions/), checked 2026-08-08 (`SRC-WERPC-045`, `SRC-WERPC-050`).
- [Anthropic Claude Code subagents](https://code.claude.com/docs/en/sub-agents), checked 2026-08-08 (`SRC-WERPC-046`).
- [Model policy](../../../00.agent-governance/model-policy.md) and `contracts/agent-model-fitness.json` are the local static owners.

## Review and Freshness

Refresh when a provider changes configuration/model/reasoning semantics or when
a role, model-policy tuple, adapter, evaluation corpus, threshold, candidate,
or promotion decision changes. Recheck official sources and obtain separately
authorized runtime evidence before promoting a configuration.

## Related Documents

- [Provider implementation status](provider-implementation-status.md)
- [AI agents](ai-agents-and-agency-agents.md)
- [Model policy](../../../00.agent-governance/model-policy.md)
