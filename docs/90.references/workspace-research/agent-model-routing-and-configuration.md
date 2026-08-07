---
title: 'Agent Model Routing and Configuration Reference'
type: content/reference
status: active
owner: platform
updated: 2026-08-07
---

# Agent Model Routing and Configuration Reference

## Overview

This reference records how model selection and reasoning-effort settings are
matched to task characteristics, from provider primary sources checked on
2026-08-07, and how this repository's 12 roles across 4 adapter surfaces are
currently configured. It records the mechanical rule that produces the
repository's 21 `PASS` and 27 `DEFER` mapping readiness split, and it records
four conflicts between current provider documentation and the repository's
fixed-cutoff contract.

The repository operates a fixed observation cutoff of `2026-07-10T10:00:00+09:00`
for cutoff-sensitive capability claims. Everything fetched on 2026-08-07 is
post-cutoff, current-only evidence. Under the repository's own rules such
evidence cannot establish fixed-cutoff mapping readiness and cannot move the
approved cutoff. This reference therefore reports conflicts rather than
resolving them.

This is descriptive Stage 90 reference material. It does not change a model
value, a reasoning setting, a tier, a contract, or a validator.

### Purpose

- Record source-backed model and effort guidance mapped to task characteristics.
- Record the complete role, provider, model, and decision-state inventory
  observed on 2026-08-07.
- Explain the derivation rule that produces the current readiness split.
- Route each conflict and gap to its owning path and name the evidence class
  that would close it.

## Reference Type

- Type: durable-concept / external-standard-snapshot
- Source checked: `2026-08-07`
- Refresh trigger: an authorized cutoff refresh; a change to
  `docs/00.agent-governance/model-policy.md`,
  `docs/00.agent-governance/contracts/agent-model-fitness.json`, or any adapter
  under `.claude/agents/`, `.codex/agents/`, `.agents/agents/`, or
  `.gemini/agents/`; or the first observed same-suite evaluation result.

## Authority Boundary

- **Authoritative for**:
  - Dated provider findings checked 2026-08-07, including exact parameter names,
    enumerated values, and the pages' own limits.
  - The repository role, provider, model, reasoning, and decision-state
    inventory observed 2026-08-07.
  - The derivation rule and the resulting counts.
  - The conflict list between current provider documentation and the
    fixed-cutoff contract.
- **Not authoritative for**:
  - Any model value, tier, reasoning setting, threshold, or promotion decision.
    Those belong to `docs/00.agent-governance/model-policy.md` and
    `docs/00.agent-governance/contracts/agent-model-fitness.json`.
  - Moving the `2026-07-10` cutoff. That requires an authorized refresh.
  - Any claim that a configured model string resolves at runtime. Model
    resolution is `DEFER` on every surface.
  - Live cluster, provider runtime, hosted CI, authentication, entitlement, or
    remote evidence.

## Scope

### In Scope

- Anthropic, OpenAI, and Google model-selection and reasoning-effort
  documentation as external rules.
- Published routing and cascading literature as cost-lever context.
- The repository's tier vocabulary, role roster, adapter surfaces, fitness
  contract, and validator enforcement.
- Task-characteristic mapping, conflicts, and gap routing.

### Out of Scope

- Changing any adapter, contract, tier, or validator.
- Executing an evaluation, canary, or authenticated provider call.
- Adding or retiring a role, which would change the fixed 12/4/48 inventory.
- Asserting that any model name exists beyond what a fetched page states.

## Definitions / Facts

### Provider Effort and Model Controls

**Anthropic effort** (<https://platform.claude.com/docs/en/build-with-claude/effort>,
checked 2026-08-07). Levels and their stated typical use cases are `max` for
"Tasks requiring the deepest possible reasoning and most thorough analysis";
`xhigh` for "Long-running agentic and coding tasks (over 30 minutes) with token
budgets in the millions"; `high` for "Complex reasoning, difficult coding
problems, agentic tasks", described as the default and "Equivalent to not
setting the parameter"; `medium` for "Agentic tasks that require a balance of
speed, cost, and performance"; and `low` for "Simpler tasks that need the best
speed and lowest costs, such as subagents". The page states the mechanism
plainly: effort "affects all tokens in the response" and "is a behavioral
signal, not a strict token budget". It also records a caching interaction:
"Changing the effort value between requests invalidates prompt caching, so vary
effort across workloads rather than within a conversation that relies on cache
hits." Its own guidance is to "Evaluate performance on your specific use cases
before deploying."

**Claude Code subagents** (<https://code.claude.com/docs/en/sub-agents>, checked
2026-08-07). Subagent frontmatter accepts `model` and also `effort`, documented
as "Effort level when this subagent is active. Overrides the session effort
level. Default: inherits from session. Options: `low`, `medium`, `high`,
`xhigh`, `max`; available levels depend on the model." Extended thinking is
inherited from the main conversation and "There is no per-subagent thinking
setting." The page names cost control as a reason to route to cheaper models.

**Claude Code model configuration**
(<https://code.claude.com/docs/en/model-config>, checked 2026-08-07). The
`model` setting accepts an alias or a full model name. Aliases include
`default`, `best`, `fable`, `sonnet`, `opus`, `haiku`, `sonnet[1m]`,
`opus[1m]`, and `opusplan`, and alias resolution differs by provider surface.
The page recommends pinning with a full model name such as `claude-opus-5`.
Subagent frontmatter `model` participates in a documented precedence chain
alongside the Agent tool `model` parameter and `CLAUDE_CODE_SUBAGENT_MODEL`.

**Anthropic migration guidance**
(<https://platform.claude.com/docs/en/about-claude/models/migration-guide>,
checked 2026-08-07). The strongest external support for a promotion gate:
"Re-evaluate your `effort` setting: run a fresh effort sweep on your own evals
rather than carrying over a setting tuned for an earlier model", and
"Re-baseline cost and latency on your own workloads."

**OpenAI reasoning**
(<https://developers.openai.com/api/docs/guides/reasoning>, checked
2026-08-07). The parameter is `reasoning.effort` with values `none`, `minimal`,
`low`, `medium`, `high`, `xhigh`, `max`. Stated mappings include `none` for
"Latency-critical tasks that do not benefit from any reasoning", `medium` as
"Default configuration for most workloads", `high` for "Hard reasoning, complex
debugging, deep planning", and `xhigh` for "Deep research, asynchronous
workflows".

**OpenAI Codex configuration**
(<https://learn.chatgpt.com/docs/config-file/config-reference> and
`/docs/agent-configuration/subagents.md`, checked 2026-08-07).
`model_reasoning_effort` is typed `minimal | low | medium | high | xhigh`
("Responses API only; `xhigh` is model-dependent"). Subagent files are TOML
under `.codex/agents/`, and precedence is explicit spawn value, then agent file
setting, then `[agents]` default, then parent session value.

**Google Gemini thinking** (<https://ai.google.dev/gemini-api/docs/thinking>,
checked 2026-08-07). The parameter is `thinking_level` with `minimal`, `low`,
`medium`, `high`, support varying by model. Task mapping: "minimal or low
thinking for fact retrieval or classification"; default thinking for comparing
concepts; "maximum thinking for advanced coding, math, or multi-step planning".

A cross-surface fact matters for this repository: the API enum, the Codex CLI
enum, and the Gemini enum differ from one another. That independently
corroborates `model-policy.md`'s statement that its `medium`, `high`, and
`xhigh` vocabulary is repository routing intent and "not a universal provider
enum".

**Routing literature.** FrugalGPT (<https://arxiv.org/abs/2305.05176>, checked
2026-08-07) describes "1) prompt adaptation, 2) LLM approximation, and 3) LLM
cascade". RouteLLM (<https://arxiv.org/abs/2406.18665>, checked 2026-08-07)
learns to route between stronger and weaker models and reports "cost reductions
exceeding 2x without quality loss", with routers that transfer when the
underlying models change. Neither paper evaluates agentic coding or GitOps
workloads, so neither validates this repository's roles.

### Task Characteristic Mapping

The recommendations below are derived from the sources above. They are not
repository policy; `model-policy.md` remains the owner.

| Task characteristic                                  | Tier                              | Effort or thinking                                          | External basis                                                                                       | Matching repository roles                                                                              |
| ---------------------------------------------------- | --------------------------------- | ----------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| Multi-agent orchestration and delegation planning    | strongest available               | `xhigh`                                                     | Anthropic `xhigh` long-horizon agentic; OpenAI `high` deep planning                                  | `supervisor`                                                                                           |
| Architecture or unfamiliar-domain diagnosis          | top                               | default `high`, escalate only on a diagnosed capability gap | Anthropic effort defaults                                                                            | `supervisor`, `incident-responder`                                                                     |
| Security review with irreversible blast radius       | top                               | `high` or above                                             | Repository priority order quality, safety, cost, latency                                             | `security-auditor`                                                                                     |
| Incident timeline reconstruction under time pressure | top capability, latency sensitive | `high`, not `max`                                           | Anthropic per-model effort tables                                                                    | `incident-responder`                                                                                   |
| Bounded high-risk manifest or config review          | worker with escalation            | `high`                                                      | OpenAI `high` hard reasoning                                                                         | `gitops-reviewer`, `network-reviewer`, `observability-reviewer`, `k8s-implementer`, `quality-engineer` |
| Primary-source research with repeated tool calling   | worker capability, high effort    | `high` to `xhigh`                                           | Anthropic exploratory guidance; OpenAI `xhigh` deep research                                         | `docs-researcher`                                                                                      |
| Standard code, YAML, and Helm review                 | worker                            | `medium`                                                    | OpenAI `medium` default for most workloads                                                           | `code-reviewer`                                                                                        |
| Bounded documentation drafting and routing           | worker                            | `medium`                                                    | Anthropic `medium` balanced                                                                          | `doc-writer`, `wiki-curator`                                                                           |
| High-volume discovery, search, classification        | cheapest capable                  | `low`, `minimal`, or `none`                                 | Anthropic `low` "such as subagents"; OpenAI `none` fast retrieval; Gemini minimal for classification | No dedicated role exists                                                                               |

Four cross-cutting rules follow from the sources. Diagnose before changing:
prefer the model's default effort and treat effort as a workload-level rather
than task-level preference. Effort is a behavioral signal, not a token budget.
Hold effort constant inside a cache-dependent conversation. And effort enums are
surface-specific, so a repository-level vocabulary must be declared as intent.

### Repository Inventory Observed 2026-08-07

`docs/00.agent-governance/contracts/harness-contract.json` version `1.0.0`
declares 12 roles, 4 surfaces, and 48 adapter projections, with a source
observation cutoff of `2026-07-10T10:00:00+09:00` and four evidence classes
whose cross-class inference is disallowed.

`docs/00.agent-governance/contracts/agent-model-fitness.json` version `1.1.0`
declares `evidenceClass: repository-static`, a priority order of quality,
safety, cost, latency, thresholds of `qualityMinimum 0.9`, `safetyMinimum 1`,
`costMaximumUsd 1`, `latencyMaximumMs 120000`, a validator pass meaning of
`mapping-readiness-only`, and an unobserved-metric policy of
`remain-DEFER-never-synthesize`.

Claude adapters observed in `.claude/agents/`:

| Role                     | Model        | Tools                                 |
| ------------------------ | ------------ | ------------------------------------- |
| `supervisor`             | `opus 4.8`   | Read, Grep, Glob, Task                |
| `code-reviewer`          | `sonnet 4.6` | Read, Grep, Glob, Bash                |
| `doc-writer`             | `sonnet 4.6` | Read, Write, Edit, Grep, Glob, Bash   |
| `gitops-reviewer`        | `sonnet 4.6` | Read, Grep, Glob, Bash                |
| `incident-responder`     | `sonnet 4.6` | Read, Grep, Glob, Bash                |
| `k8s-implementer`        | `sonnet 4.6` | Read, Write, Edit, Grep, Glob, Bash   |
| `network-reviewer`       | `sonnet 4.6` | Read, Grep, Glob, Bash                |
| `observability-reviewer` | `sonnet 4.6` | Read, Grep, Glob, Bash                |
| `security-auditor`       | `sonnet 4.6` | Read, Grep, Glob, Bash                |
| `wiki-curator`           | `sonnet 4.6` | Read, Write, Edit, Grep, Glob, Bash   |
| `docs-researcher`        | `Sonnet 5`   | Read, Grep, Glob, WebFetch, WebSearch |
| `quality-engineer`       | `Sonnet 5`   | Read, Write, Edit, Grep, Glob, Bash   |

No Claude adapter declares an `effort` field.

Codex adapters in `.codex/agents/` carry both `model` and
`model_reasoning_effort`: `supervisor` is `gpt-5.5` at `xhigh`;
`docs-researcher` and `quality-engineer` are `gpt-5.6-terra` at `high`;
`doc-writer` and `wiki-curator` are `gpt-5.3-codex` at `medium`; the remaining
seven are `gpt-5.3-codex` at `high`.

Local and Antigravity adapters in `.agents/agents/` carry `name`,
`description`, and `model` only, with no `tools` key: `Gemini 3.1 Pro` for
`supervisor` and `docs-researcher`, `Gemini 3.5 Flash` for the other ten.

Gemini project adapters in `.gemini/agents/` carry neither `model` nor `tools`,
which matches the provider note's statement that the frontmatter intentionally
omits both.

### The Derivation Rule and the 21/27 Split

`scripts/validate-agent-model-fitness.py` assigns a role class mechanically:
`planning-supervisor` when `riskTier` is `high`, otherwise `worker-subagent`.
Each role then inherits its provider's candidate and readiness for that class.

The provider table is: `local` is `PASS` on both classes with
`cutoffConfidence: repository-only`; `claude` is `PASS` on
`planning-supervisor` because the `opus 4.8` candidate is cutoff-backed and
`DEFER` on `worker-subagent` because the `sonnet 4.6` candidate is a
current-only source; `codex` and `gemini` are `DEFER` on both.

Nine of twelve roles carry `riskTier: high`; the three `standard` roles are
`code-reviewer`, `doc-writer`, and `wiki-curator`. That yields 12 `PASS` for
`local`, 9 `PASS` and 3 `DEFER` for `claude`, and 12 `DEFER` each for `codex`
and `gemini` — exactly the recorded 21 `PASS` and 27 `DEFER`.

For all 48 tuples the observed value, fitness, promotion, canary, and runtime
decisions are `DEFER`; baseline and candidate metric digests, threshold results,
and evaluation dispositions are `DEFER`; adjudicator readiness is `PASS`; silent
fallback is disallowed; and rollback state is `armed-not-executed`.

The validator additionally enforces adapter-to-contract equality, so an adapter
model or effort that drifts from the contract fails `AREA-FIT-INCUMBENT-DRIFT`,
and it blocks preclaiming with dedicated codes for runtime, fitness, promotion,
canary, baseline, candidate, and threshold values.

### Conflicts and Gap Routing

| ID      | Finding                                                                                                                                                                                                                                                                                                                                                                          | Owning path                                                                                                       | Evidence class needed                                                        |
| ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| MOD-G1  | Configured Claude model strings (`opus 4.8`, `sonnet 4.6`, `Sonnet 5`) match neither a documented alias nor a documented full model ID form. No fetched page states they are invalid, so this is an unresolved resolution risk, not a proven defect                                                                                                                              | `.claude/agents/*.md`, `docs/00.agent-governance/contracts/agent-model-fitness.json`                              | provider-runtime                                                             |
| MOD-G2  | The contract records Claude reasoning as `not-configurable-on-native-surface` for all 12 Claude tuples, but the current subagent documentation documents an `effort` frontmatter field with five levels. This is the highest-value conflict                                                                                                                                      | `agent-model-fitness.json`, `scripts/validate-agent-model-fitness.py`, `docs/00.agent-governance/model-policy.md` | repo-static to record the source; provider-runtime to prove it is honored    |
| MOD-G3  | Current Anthropic documentation lists `opus 4.8` and `sonnet 4.6` under legacy models. Acting on this requires an authorized cutoff refresh; the migration guide independently requires a fresh effort sweep on local evals before switching                                                                                                                                     | `docs/00.agent-governance/contracts/provider-runtime-evidence.json`                                               | repo-static cutoff refresh, then provider-runtime plus same-suite evaluation |
| MOD-G4  | `gpt-5.3-codex` is not corroborated by any fetched page; `gpt-5.6-terra` is. This explains why all 12 Codex mappings are already `DEFER`                                                                                                                                                                                                                                         | `.codex/agents/*.toml`                                                                                            | provider-runtime                                                             |
| MOD-G5  | Current Gemini CLI subagent documentation defines a per-agent `model` field defaulting to `inherit`, while the contract labels Gemini model values `not-configurable-on-native-surface`. The design intent to omit the field is not falsified; the factual label about the surface is contradicted. The publisher authority of the fetched host was not verifiable from the page | `docs/00.agent-governance/providers/gemini.md`                                                                    | repo-static wording reconciliation; provider-runtime is currently `ABSENT`   |
| MOD-G6  | Codex `code-reviewer` is `riskTier: standard` yet configured at `high`, while the other two standard roles are `medium`. The rule is a hard-coded role set, not a risk-tier derivation, and the asymmetry is unstated                                                                                                                                                            | `scripts/validate-agent-model-fitness.py`, `.codex/agents/code-reviewer.toml`                                     | repo-static rationale                                                        |
| MOD-G7  | No cheapest-capable tier exists. Every role is `top` or `worker`, while all three providers recommend a low-effort tier for search, classification, and retrieval. Adding a role would change the asserted 12/4/48 inventory, so this is a governance decision                                                                                                                   | `docs/00.agent-governance/model-policy.md`, `harness-contract.json`                                               | repo-static governance decision through roster admission                     |
| MOD-G8  | No observed evaluation exists for any tuple. Suites, corpora digests, fixtures, graders, and adjudicators are already bound per role; the missing input is execution, not design                                                                                                                                                                                                 | `docs/00.agent-governance/contracts/agent-evaluations.json`                                                       | provider-runtime plus a recorded same-suite baseline                         |
| MOD-G9  | Canary evidence is synthetic only, with mutation disabled and cross-lane promotion blocked                                                                                                                                                                                                                                                                                       | `scripts/validate-agent-provider-canaries.py`                                                                     | provider-runtime; remote-live under explicit human approval                  |
| MOD-G10 | The effort-to-prompt-caching interaction and the workload-level rather than task-level guidance are recorded nowhere in the repository                                                                                                                                                                                                                                           | `docs/00.agent-governance/model-policy.md`                                                                        | repo-static                                                                  |
| MOD-G11 | The 12 `local` `PASS` results rest on repository labels with empty source IDs and `cutoffConfidence: repository-only`. The `PASS` means the label matches itself and is the weakest of the 21                                                                                                                                                                                    | `agent-model-fitness.json`                                                                                        | provider-runtime for the local runtime                                       |

## Sources

- <https://platform.claude.com/docs/en/about-claude/models/overview> checked
  2026-08-07 (HTTP 302 from `docs.claude.com`). Adopted: the current and legacy
  model listings and the effort-default note. Rejected: any claim about which
  model this repository's account resolves.
- <https://platform.claude.com/docs/en/build-with-claude/effort> checked
  2026-08-07. Adopted: the five levels, their stated use cases, the
  behavioral-signal framing, and the caching interaction.
- <https://platform.claude.com/docs/en/about-claude/models/migration-guide>
  checked 2026-08-07. Adopted: the fresh-effort-sweep and re-baseline
  requirements.
- <https://code.claude.com/docs/en/sub-agents> checked 2026-08-07. Adopted: the
  frontmatter field set including `effort`, and the thinking-inheritance rule.
  Rejected: any claim about which literal `model:` strings are accepted.
- <https://code.claude.com/docs/en/model-config> checked 2026-08-07. Adopted:
  the alias set, provider-specific resolution, and the pinning recommendation.
- <https://code.claude.com/docs/en/costs> checked 2026-08-07. Adopted: the
  model-choice and delegation cost guidance.
- <https://developers.openai.com/api/docs/guides/reasoning> checked 2026-08-07
  (HTTP 301 from `platform.openai.com`). Adopted: the `reasoning.effort` enum
  and per-level guidance. Rejected: the existence of any model ID not listed.
- <https://learn.chatgpt.com/docs/config-file/config-reference> and
  <https://learn.chatgpt.com/docs/agent-configuration/subagents.md> checked
  2026-08-07 (HTTP 308 from `developers.openai.com/codex/`). Adopted:
  `model_reasoning_effort` typing and the four-level precedence order.
- <https://ai.google.dev/gemini-api/docs/thinking> checked 2026-08-07. Adopted:
  `thinking_level` values and task mapping. Rejected: any implication for
  Gemini CLI resolution.
- <https://geminicli.com/docs/core/subagents/> checked 2026-08-07. Adopted: the
  documented per-agent field set. Flagged: the publisher's official status was
  not verifiable from the page, so treat it as secondary.
- <https://arxiv.org/abs/2305.05176> and <https://arxiv.org/abs/2406.18665>
  checked 2026-08-07. Adopted: cascade and learned-routing as published cost
  levers. Rejected: applicability to agentic coding or to this roster.
- Repository evidence read 2026-08-07:
  `docs/00.agent-governance/model-policy.md`,
  `docs/00.agent-governance/contracts/harness-contract.json`,
  `docs/00.agent-governance/contracts/agent-model-fitness.json`,
  `docs/00.agent-governance/contracts/provider-runtime-evidence.json`,
  `docs/00.agent-governance/harness-catalog.md`, the four adapter directories,
  and the fitness, admission, and canary validators in `scripts/`.

## Review and Freshness

- Review on an authorized cutoff refresh, an adapter or contract change, or the
  first observed same-suite evaluation.
- Provider model documentation changes frequently. Every finding here is
  observation-time evidence for 2026-08-07 and must be re-observed before any
  dated claim is promoted.
- The `2026-07-10` cutoff is not moved by this reference. Post-cutoff findings
  are recorded as conflicts, not as resolutions.
- Model resolution, authentication, entitlement, observed fitness, threshold,
  promotion, canary, and runtime remain `DEFER` for all 48 tuples.

## Related Documents

- [Research Pack Index](README.md)
- [Provider Implementation Status](../research/2026-07-07-wer/provider-implementation-status.md)
- [Harness and Loop Engineering](../research/2026-07-07-wer/harness-and-loop-engineering.md)
- [AI Agents Roster and Gap Analysis](../research/2026-07-07-wer/ai-agents-roster-and-gap-analysis.md)
- [Model Policy](../../00.agent-governance/model-policy.md)
