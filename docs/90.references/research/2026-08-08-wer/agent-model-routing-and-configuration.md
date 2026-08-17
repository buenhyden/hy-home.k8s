---
title: 'Reference: Agent Model Routing and Configuration'
type: content/reference
status: active
owner: platform
updated: 2026-08-10
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

| Task characteristics                                                      | Role / tier                             | Tool and sandbox expectation                                                   | Review / promotion rule                                                         |
| ------------------------------------------------------------------------- | --------------------------------------- | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------- |
| Bounded documentation, inventory, formatting, or deterministic validation | Named worker                            | Read-only or minimal workspace-write surface; no credentials/live tools.       | Normal reviewer when the change is material; validation evidence is required.   |
| Cross-file architecture, conflicting sources, or multi-agent coordination | Supervisor / `top`                      | Narrow delegation and explicit ownership; preserve a shared evidence ledger.   | Independent review before canonical decision or broad edit.                     |
| Security, GitOps, incident, destructive, or external-affecting work       | Specialist with risk-appropriate tier   | Least privilege; human approval controls live/secret/remote/destructive tools. | Independent specialist review and explicit rollback/handoff; no self-promotion. |
| Unknown model fitness or provider feature                                 | Existing safe incumbent or no execution | Do not broaden tools or change configuration to compensate.                    | `DEFER`; collect approved parsing and same-suite evaluation evidence first.     |

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

### 2026-08-10 freshness re-check

All four external sources were re-read on 2026-08-10. No cited claim changed
inside the 2026-08-08 to 2026-08-10 window. The re-check did record three
disagreements that exist between the live official pages themselves, which
bounds how strongly any single page can be cited for model resolution.

| Observation                                   | Live evidence on 2026-08-10                                                                                                                                                                                                                                                          | Effect on this report                                                                                                                                                                                                                              |
| --------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Model identifiers disagree across Codex pages | The config reference uses `gpt-5.5` as its `model` example; the subagents page names `gpt-5.6`, `gpt-5.6-terra`, and `gpt-5.6-luna` in prose while its own TOML example sets `gpt-5.3-codex-spark`. Three generations appear across two pages of the same product.                   | Do not treat any documented model identifier as a stable routing target. A model-policy tuple must be validated against the provider at run time, which is `DEFER`.                                                                                |
| Reasoning-effort value sets disagree          | The config reference lists `minimal`, `low`, `medium`, `high`, `xhigh` for `model_reasoning_effort`; the subagents page lists `ultra`, `max`, `xhigh`, `high`, `medium`, `low`. `ultra` and `max` appear only on the second page; `minimal` only on the first.                       | A local effort value that validates against one page may be rejected by the runtime. Effort-value admission stays an unverified property.                                                                                                          |
| Model precedence order disagrees              | The config reference says of `agents.default_subagent_model` that "An explicit spawn model takes precedence." The subagents page states the agent file value takes precedence, and only otherwise resolves explicit spawn value, then the `[agents]` default, then the parent value. | The two statements order the agent-file and explicit-spawn sources differently. This report therefore records no single authoritative Codex precedence chain; the Claude Code chain, which one page states end to end, remains separately citable. |

One attribution limit is also recorded. The Agents SDK sessions page
(`SRC-WERPC-050`) documents session storage backends only; it states no
model-selection key, no model identifier, and no resolution or fallback rule.
It supports the session-context claims in this pack, not the model-routing
claims, and it should not be cited for the latter.

`REQ-WERPC-028` stays `Partial`. Parsing, resolution, fitness, cost and latency,
canary, and promotion still require provider runtime evidence that is `DEFER`,
and the disagreements above make that runtime check more necessary, not less.

### 2026-08-17 full-corpus refresh

This increment is the fifth refresh cycle over this pack, executed under
Spec 058. Unlike the three preceding cycles it re-observed every owner row in
the pack rather than the twelve `Partial` rows, and it assigns each retained
`Partial` or `DEFER` row a blocking class recorded in the
[scope application index](scope-application-index.md). All observations are
dated **2026-08-17**. No live cluster, hosted CI run, provider runtime,
authenticated execution, or secret value was observed.

#### REQ-WERPC-028 re-observation

**External result:** `unchanged` (`SRC-WERPC-078`). All three disagreements
recorded on 2026-08-10 and re-confirmed on 2026-08-12 and 2026-08-14 persist
verbatim. Model identifiers still differ between the configuration reference and
the subagents page. Reasoning-effort vocabulary still differs, with `ultra` and
`max` still absent from the configuration reference. Precedence order is still
stated in opposite directions by the two pages: the configuration reference says
an explicit spawn model takes precedence, while the subagents page says an agent
file's `model` or `model_reasoning_effort` takes precedence. Claude Code
subagent model resolution order is unchanged.

**Workspace result:** `confirmed`. `model-policy.md:20,58-62` still owns only
`top` and `worker` tiers and the `medium`, `high`, `xhigh` reasoning-intent
vocabulary. `harness-catalog.md:134-140` still records `12 roles / 4 providers /
48 tuples` with mapping readiness `PASS` for 21 and `DEFER` for 27, and
fitness, promotion, canary, and runtime `DEFER` for all 48.

**Status effect:** `no-change` (`CLM-WERPC-011-28`). The row keeps `Partial`.

**Blocking class:** `provider-runtime`, structurally unreachable. Parsing,
resolution, fitness, cost, latency, canary, and promotion evidence all require
an authenticated provider runtime. Reopens if the two Codex pages converge or
diverge further, or if the model-fitness contract version or tuple counts
change.

#### Recorded methodology caveat

A single-pass documentation fetch during this cycle returned a paraphrase that
inverted the documented precedence order; a targeted re-fetch requesting
verbatim text returned the correct order matching the prior finding. Precedence
and ordering claims must be confirmed against verbatim source text before
adoption.

#### Stale reference observed in a governance owner

`model-policy.md` still links `developers.openai.com/codex/subagents` and
`developers.openai.com/codex/guides/agents-md` in its Related Documents section,
although this pack recorded on 2026-08-10 that `developers.openai.com/codex`
permanently redirects to `learn.chatgpt.com/docs`. This is an uncorrected stale
reference in a Stage 00 owner rather than in this pack, and correcting a Stage 00
owner is outside this cycle's scope.

## Sources

- [OpenAI Codex configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference), checked 2026-08-08, re-checked 2026-08-10 (`SRC-WERPC-049`).
- [OpenAI Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) and [OpenAI Agents SDK sessions](https://openai.github.io/openai-agents-python/sessions/), checked 2026-08-08, re-checked 2026-08-10 (`SRC-WERPC-045`, `SRC-WERPC-050`).
- [Anthropic Claude Code subagents](https://code.claude.com/docs/en/sub-agents), checked 2026-08-08, re-checked 2026-08-10 (`SRC-WERPC-046`).
- [Model policy](../../../00.agent-governance/model-policy.md) and `contracts/agent-model-fitness.json` are the local static owners.

## Review and Freshness

Refresh when a provider changes configuration/model/reasoning semantics or when
a role, model-policy tuple, adapter, evaluation corpus, threshold, candidate,
or promotion decision changes. Recheck official sources and obtain separately
authorized runtime evidence before promoting a configuration.

External sources were re-checked on 2026-08-10; no cited claim changed inside
that window. The re-check recorded that the two Codex pages disagree on model
identifiers, reasoning-effort values, and precedence order, so no single page is
sufficient on its own. None of the four sources publishes a last-modified date,
so an unchanged result is content identity rather than a publisher signal.

### 2026-08-11 Partial/DEFER incremental refresh

This bounded increment was executed and checked on **2026-08-12**. The heading
preserves the approved package date; no model was invoked and no cost, latency,
fitness, canary, fallback, promotion, entitlement, or effective configuration
was observed.

#### REQ-WERPC-028 current configuration reconciliation

| Official source                                                                                     | Publication / revision and adopted scope                                                                                                                                                                                                                          | Rejected inference, uncertainty, and refresh trigger                                                                                                                                                                                                                 |
| --------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [OpenAI Codex configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference) | Current page with no publisher date, checked 2026-08-12. It documents `[agents]` defaults, per-role config layers, explicit-spawn precedence over those defaults, and `model_reasoning_effort` as `minimal`, `low`, `medium`, `high`, or model-dependent `xhigh`. | It does not prove an adapter parsed, a model exists for this account, or an effort value was applied. Recheck when agent/config/model/reasoning keys or precedence change.                                                                                           |
| [OpenAI Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)              | Current page with no publisher date, checked 2026-08-12. Agent-file model/effort overrides precede explicit spawn and `[agents]` defaults; the page also lists `low` through `ultra` effort guidance and current model recommendations.                           | `max` and `ultra` still do not appear in the configuration reference's accepted-value row. No single page establishes actual parser acceptance or account availability. Recheck when the two official surfaces converge or a runtime parse is separately authorized. |
| [Anthropic Claude Code subagents](https://code.claude.com/docs/en/sub-agents)                       | Current page with no publisher date, checked 2026-08-12. Model resolution is documented as environment override, per-invocation value, subagent frontmatter, then main conversation; aliases and full model IDs are allowed.                                      | Does not prove the tracked frontmatter parsed, its named model resolved, or its tools/permissions were effective. Recheck when aliases, precedence, effort, or agent schema changes.                                                                                 |

**As-Is:** `model-policy.md` still owns only `top`/`worker` and shared
`medium`/`high`/`xhigh` intent. `contracts/agent-model-fitness.json` version
1.1.0 still owns 48 provider-role tuples: mapping readiness is `PASS` for 21
and `DEFER` for 27, while fitness, promotion, canary, and runtime are `DEFER`
for all 48. The `.codex/agents/*.toml`, `.claude/agents/*.md`,
`.agents/agents/*.md`, and `.gemini/agents/*.md` values remain configured
projections, not observations.

**Gap and bounded target:** The current Codex pages still expose a wider effort
vocabulary on the subagents page than in the configuration reference, and all
provider identifiers remain account/client/version sensitive. Preserve each
configured incumbent. A future change must have platform-owner authorization,
successful exact parsing and resolution without silent fallback, same-suite
quality/safety evidence, independent adjudication, canary evidence, and a
rollback record before promotion.

**Final disposition:** `Partial`. Evidence depth is official configuration
syntax plus exact repo-static model policy, fitness contract, evaluation
bindings, and adapters. Owner: Stage 00 model policy and model-fitness
contract. Refresh when a cited provider configuration contract or a local
model/evaluation selector materially changes.

### 2026-08-14 consistency and Partial re-observation

This bounded increment re-observed the workspace and re-checked external
sources for `REQ-WERPC-028` only, checked on **2026-08-14**. No model was
invoked and no cost, latency, fitness, canary, fallback, promotion,
entitlement, or effective configuration was observed.

#### REQ-WERPC-028 workspace and source consistency check

**Workspace delta:** `no-change`. `model-policy.md` still owns only
`top`/`worker` and shared `medium`/`high`/`xhigh` intent.
`contracts/agent-model-fitness.json` remains version `1.1.0` with 48
provider-role tuples: mapping readiness is `PASS` for 21 and `DEFER` for 27,
and fitness/promotion/canary/runtime remain `DEFER` for all 48 — an exact
match to the 2026-08-12 baseline.

**External result:** all three sources were reachable and `unchanged`
against their 2026-08-12 adopted scope; the two Codex pages still disagree
with each other.

| Source                                                                                              | Result      | Note                                                                                                                                                                                                                                                                                            |
| --------------------------------------------------------------------------------------------------- | ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [OpenAI Codex configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference) | `unchanged` | `model_reasoning_effort` accepted values still list only `minimal, low, medium, high, xhigh`; the `model` example is still `gpt-5.5`; `agents.default_subagent_model` precedence still states an explicit spawn model takes precedence. No publisher date.                                      |
| [OpenAI Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)              | `unchanged` | Still lists `ultra, max, xhigh, high, medium, low` — `ultra`/`max` still absent from the configuration reference. Agent-file model/effort overrides still precede explicit spawn and `[agents]` defaults. No publisher date.                                                                    |
| [Anthropic Claude Code subagents](https://code.claude.com/docs/en/sub-agents)                       | `unchanged` | Model resolution is still: `CLAUDE_CODE_SUBAGENT_MODEL` environment override, then per-invocation `model` parameter, then subagent frontmatter, then the main conversation's model; aliases (`sonnet`, `opus`, `haiku`, `fable`) and full model IDs are still both accepted. No publisher date. |

**As-Is:** Unchanged. The three-generation Codex model-identifier
disagreement, the reasoning-effort vocabulary disagreement, and the
agent-file/explicit-spawn precedence disagreement recorded on 2026-08-10 and
2026-08-12 all still hold; no single Codex page is sufficient on its own.

**Gap and bounded target:** Unchanged. Preserve each configured incumbent. A
future change still needs platform-owner authorization, successful exact
parsing and resolution without silent fallback, same-suite quality/safety
evidence, independent adjudication, canary evidence, and a rollback record
before promotion.

**Missing evidence:** authenticated same-suite evaluation and account-level
model/effort resolution. **Owning authority:** Stage 00 model policy and
model-fitness contract. **Safe boundary:** a platform-owner-authorized,
non-secret parsing/resolution check against the exact configured tuple; no
broadened tool or configuration scope to compensate for unknown fitness.
**Refresh trigger:** a cited provider configuration contract or a local
model/evaluation selector materially changes.

**Final disposition:** `Partial`, unchanged from the 2026-08-12 baseline. No
promotion. New source registered: `SRC-WERPC-074`. New claim registered:
`CLM-WERPC-010-03`.

## Related Documents

- [Provider implementation status](provider-implementation-status.md)
- [AI agents](ai-agents-and-agency-agents.md)
- [Model policy](../../../00.agent-governance/model-policy.md)
