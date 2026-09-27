---
title: "Reference: Agent Model Routing and Configuration"
version: "1.2.0"
type: "reference/research"
status: "published"
owner: "platform"
updated: "2026-09-27"
layer: "references"
artifact_id: "RES-0001-m0010"
---

# Reference: Agent Model Routing and Configuration

## Overview

This reference compares task-sensitive model selection, configuration resolution, cost and rate controls. Vendor workload labels and published prices provide hypotheses and estimates; promotion needs measured task quality, latency, total cost and independent review. No model, role or adapter is changed.

## Reference Type

External primary-source research directly read on 2026-09-27, with conditional investigation design and preserved historical evidence.

## Authority Boundary

Official documentation establishes only bounded external product facts. This reference defines no local permission, model promotion, memory retention rule or provider configuration change. Current workspace availability, parsing, entitlement, effective settings, execution, cost, retrieval and correct application are `not observed in this cycle`. Candidate selectors are unobserved. Private settings, account records, memory stores, credentials and conversations are excluded. External claim judgment is separate from source refresh result and repository-static document QA.

## Scope

Primary owner of U29 and U35 and existing REQ-WERPC-028. Covers model family/ID, reasoning, context/output/tool limits, fallback/escalation, API versus subscription usage, caching/compaction, budgets, concurrency and bounded retry. Excludes account catalogs, actual invoices, effective local model selection, fitness experiments and permanent price/model policy.

## Definitions / Facts

### Model selection and escalation

`CLM-WERPC-017-131` treats selection as a task-risk hypothesis. Mechanical edits and bounded formatting may fit a smaller/lower-effort model; investigation and implementation need evidence coverage and tool fitness; architecture, root-cause/security review and uncertain sources may justify stronger reasoning plus independent review. Final verification relies on the right test/evidence contract, not the reviewer model's name. Larger models and effort can increase latency/spend without proportional task benefit. Compare the same representative suite, quality/safety thresholds, failed attempts, review effort and total latency/cost before adoption. Vendor family labels are not repository-quality measurements.

`CLM-WERPC-017-132` and `CLM-WERPC-017-133` record API catalog facts, directly read **2026-09-27**:

| API model ID / version boundary | Context / maximum output | Reasoning / input-output / tool boundary | Evidence limit |
| --- | --- | --- | --- |
| `gpt-6-sol`, `gpt-6-luna` | 1,050,000 / 128,000 tokens | Text/image input, text output; no audio/video. `none`, `low`, default `medium`, `high`, `xhigh`, `max`. Responses lists built-in tools/function/MCP and product-specific tools; Chat Completions function calling is restricted to effort `none`. | No immutable dated snapshot ID was exposed in the read snapshot; alias/revision is mutable. No listed fine-tuning support established. |
| `gpt-6-astra` | 1,050,000 / 128,000 | Text/image input, text output; `low` through `max`, with `none` unsupported; catalog-specific Responses tools. | API catalog does not prove Codex account availability, native product feature parity or actual accepted settings. |
| `claude-fable-5-1` | 1,000,000 / 128,000 | Always adaptive thinking; high default effort. | API ID is not a Claude Code role alias or entitlement proof. |
| `claude-opus-5-5` | 1,000,000 / 128,000 | Always adaptive thinking; medium default effort. | Account/product/provider route may differ. |
| `claude-sonnet-5` | 1,000,000 / 128,000 | Adaptive thinking; high default effort. | Verify exact supported effort/tools for the intended endpoint. |
| `claude-haiku-4-5`; dated `claude-haiku-4-5-20251001` | 200,000 / 64,000 | Fixed extended thinking, no effort control. | Dated API ID and mutable alias are distinct identities. |

These bounded documented values are `Verified` from SRC-WERPC-229–231 and SRC-WERPC-128 in [current source observations](m0012-source-coverage.md#current-source-observations). Immutable pinning where absent, effective entitlement and measured fitness remain `Partial`/unknown. Output ceilings are limits, not typical response sizes, and maximum context is not a requirement to fill it.

`CLM-WERPC-017-134` resolves three historical ambiguities. The current Codex configuration reference describes `model_reasoning_effort` as a string against the catalog; the old finite five-value enumeration is **Contradicted as current guidance**. The product catalog includes `low`, `medium`, `high`, `xhigh`, `max`, `ultra`, with no Luna `ultra`; `ultra` is product orchestration, not an API effort. Codex base resolution is explicit spawn → `[agents]` default → parent, followed by an agent-file explicit model/effort override. File-only model preserves resolved effort; explicit new spawn model without effort uses the model default. Thus “spawn beats default” and “file beats spawn” concern different layers and the prior apparent precedence conflict is resolved; no local parser check occurred. Sources: SRC-WERPC-049, 136 and 011.

`CLM-WERPC-017-135` bounds Claude resolution and fallback. Main conversation selection is `/model` → `--model` → `ANTHROPIC_MODEL` → settings → default-model environment, subject to managed available-model constraints. Normal subagent resolution is invocation → definition → default `CLAUDE_CODE_SUBAGENT_MODEL` → main; the documented FORCE override introduced at v2.1.257 has exceptions. Fallback tries up to three deduplicated alternatives for the current turn and eligible availability/nonretryable server errors; it excludes auth, billing, rate, size, transport and policy-denial errors. Compaction does not fall back to smaller-context models; subagent fallback has a v2.1.247 gate. Exact parsing, fallback and resolution require authorized client evidence. Source: SRC-WERPC-236.

### Cost context and rate control

`CLM-WERPC-017-136` and `CLM-WERPC-017-137` record **standard API list prices in USD per million tokens**, read 2026-09-27. They are not subscription plan fees, included allowance, account quotes or actual bills.

| API model | Uncached input | Cache write | Cache read | Output | Conditions |
| --- | --- | --- | --- | --- | --- |
| GPT-6 Sol | 2.00 | 2.50 | 0.20 | 10.00 | Current standard list pricing. |
| GPT-6 Luna | 0.10 | 0.125 | 0.01 | 0.50 | Current standard list pricing. |
| GPT-6 Astra | 10.00 | 12.50 | 1.00 | 50.00 | Current standard list pricing. |
| Claude Fable 5.1 | 10.00 | 1.25× input for 5-minute cache; 2× for 1-hour | 0.25 | 50.00 | Cache multipliers apply to write, not every cached request. |
| Claude Opus 5.5 | 4.00 | Same stated write multipliers | 0.20 | 20.00 | Cache read is not a universal 0.1× rule. |
| Claude Sonnet 5 | 2.00 | Same stated write multipliers | 0.20 | 10.00 | Current standard list pricing. |
| Claude Haiku 4.5 | 1.00 | Same stated write multipliers | 0.10 | 5.00 | Current standard list pricing. |

OpenAI input above 272K tokens changes whole-request input/cache pricing to 2× and output to 1.5×. The read catalog also documents Fast 2×, Batch/Flex half price and regional premiums; do not assume tier modifiers combine. Anthropic documents 50% Batch pricing, applicable regional 1.1× and additional partner/tool fees. Its newer-tokenizer approximately 30% token increase is a vendor content-dependent observation, not a universal cost-normalization constant. Sources: SRC-WERPC-229–231 and SRC-WERPC-233. Choose caching only when repeated prefixes and invalidation justify write/storage cost; cache hits and bill savings require usage evidence. Smaller relevant context lowers spend and stale-content risk, while compaction can lose details required for acceptance.

`CLM-WERPC-017-138` separates Codex product credits from dollars and API tokens. API-key billing applies to local CLI/SDK/IDE, excluding cloud, GitHub review and Slack. Subscription local/cloud usage shares an allowance that varies by model/task and may have weekly limits; Enterprise/Edu flexible credits are not fixed request counts. Documented standard credits per million input/cache/output tokens are Astra 250/25/1250, Sol 50/5/250 and Luna 2.5/0.25/12.5, with no cache-write charge on that product surface. Credits are neither USD nor included account allowance. The product catalog dates GPT-5.5 retirement from ChatGPT Work/Codex at 2026-10-14 and GPT-5.4's ChatGPT-sign-in retirement at 2026-08-31; these exclusions do not establish API retirement. Sources: SRC-WERPC-169 and 136. Account-specific remaining limits and availability were not queried.

`CLM-WERPC-017-139` proposes an estimate over uncached input, cache write/read and output at the exact product/tier/region rates, plus tools and all children/retries/review. Reserve capacity for compaction, fallback and verification; measure sanitized usage against the applicable billing contract; set warning and stop thresholds at a durable host owner. Context/output, RPM, input/output-token-per-minute, spend and concurrency caps are distinct. A per-run CLI budget is not a project-wide durable budget: Claude print-only `--max-budget-usd` counts current-run children and documented spawn/background stops, but excludes previous resumed-session costs. Sources: SRC-WERPC-235 and 237.

Ordinary rate-limit recovery should honor retry timing and use bounded exponential backoff/jitter; failed OpenAI requests consume allowance. Anthropic acceleration limits call for gradual ramp-up. Hard spend-limit 429 with `enforced_spend_limit_reached` lacks retry-after and needs account/budget recovery; user caps can return 400. Never retry authentication/policy denial by switching model or widen privileges to regain throughput. Limit simultaneous agents to the lower applicable rate/budget bound and terminate when recovery cannot make new authorized progress. Sources: SRC-WERPC-232 and 234; [harness/loop failure controls](m0002-harness-and-loop-engineering.md#loop-design-and-failure-controls) own the host-recovery comparison.

### Model and budget questions

`CLM-WERPC-017-140` links to the [central question evidence contracts](m0013-scope-application-index.md#follow-up-question-ledger). All workspace results are `not observed in this cycle`; candidates include `.codex/config.toml`, `.codex/agents/`, `.claude/agents/`, SDK model/run options, budget/concurrency declarations and redacted usage summaries. Private account dashboards, invoices and environment values are excluded here.

- Q-WERPC-161: what exact alias or snapshot, product/client/account/region, effort, tools and context/output limits does each task require, and which retirement trigger mandates recheck?
- Q-WERPC-162: what same-suite quality, safety, latency and total cost justify routing and risk-proportional independent review?
- Q-WERPC-163: which file/spawn/default/environment/managed layer actually resolves the model and effort without silent fallback?
- Q-WERPC-164: which failures allow fallback, how are smaller context and policy denials excluded, and do fallback attempts preserve budget and stop history?
- Q-WERPC-165: are API dollars, subscription credits, cache/tier/tool charges and spend/rate/concurrency limits measured separately against the correct contract?
- Q-WERPC-166: do sibling agents, retries, compaction and review share durable counters, warnings, stop thresholds and a recoverable checkpoint?

### Historical observations and corrections — 2026-08-08 to 2026-09-05

The following preserves original observation dates, identities, statuses, evidence limits and correction relationships. Retired owners and product assumptions are dated provenance, not current instructions or workspace findings. Current workspace result: `not observed in this cycle`.

#### Historical Overview

This reference defines evidence-bound routing from task characteristics to a
role, tier, provider configuration, tool/sandbox boundary, and reviewer. It
does not select a new model or change an adapter.

#### Historical Reference Type

Repository-static research baseline.

#### Historical Authority Boundary

Model policy and the model-fitness contract own the local tier and promotion
contract; provider documentation owns provider configuration vocabulary.
Tracked adapters prove a configured incumbent only. Authentication, model
availability, parsing, resolution, performance, cost, latency, and access are
`DEFER` without matching evidence.

#### Historical Scope

It covers task-characteristic routing, model/reasoning configuration,
evaluation, fallback, and promotion. It does not reassign roles, consume an
account catalog, or alter provider configuration.

#### Historical Definitions / Facts

#### Model-routing baseline

> [!NOTE]
> The rows below are observations at the dates their cycles record, not the
> current owner graph. `docs/00.agent-governance/` and its `memory/`, `rules/`,
> `contracts/` and `harness-catalog.md` were retired, `.agents/agents/` and
> `.gemini/` are not part of the current two-provider surface, and common
> authority now lives under `.agents/` with progress owned by the Stage 03 Task.

The workspace policy assigns `top` to planning/supervision and `worker` to
bounded implementation, validation, and focused edits. A worker may escalate a
high-risk governance, security, or cluster-affecting review without changing
its role class. Exact provider tuples, candidates, incumbent values, reasoning
support, evaluation readiness, and promotion state lived in
`contracts/agent-model-fitness.json` at the recorded observation; that contract
was retired with the former governance root, and the capability tier to model
binding is now declared per provider in `.agents/roles/registry.json`. All
observed runtime/promotion/canary tuples remain `DEFER`.

| Task characteristics                                                      | Role / tier                             | Tool and sandbox expectation                                                   | Review / promotion rule                                                         |
| ------------------------------------------------------------------------- | --------------------------------------- | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------- |
| Bounded documentation, inventory, formatting, or deterministic validation | Named worker                            | Read-only or minimal workspace-write surface; no credentials/live tools.       | Normal reviewer when the change is material; validation evidence is required.   |
| Cross-file architecture, conflicting sources, or multi-agent coordination | Supervisor / `top`                      | Narrow delegation and explicit ownership; preserve a shared evidence ledger.   | Independent review before canonical decision or broad edit.                     |
| Security, GitOps, incident, destructive, or external-affecting work       | Specialist with risk-appropriate tier   | Least privilege; human approval controls live/secret/remote/destructive tools. | Independent specialist review and explicit rollback/handoff; no self-promotion. |
| Unknown model fitness or provider feature                                 | Existing safe incumbent or no execution | Do not broaden tools or change configuration to compensate.                    | `DEFER`; collect approved parsing and same-suite evaluation evidence first.     |

#### Configuration baseline

Codex's current configuration reference documents `agents.<name>` settings and
`model_reasoning_effort` values `minimal`, `low`, `medium`, `high`, and
`xhigh`; support for `xhigh` is model-dependent. Claude documents task-specific
subagent model/tool configuration. These current product facts do not prove
this worktree's effective provider configuration. Local adapters and the
model-fitness contract remain the repository-static incumbent projection.

#### Routing, evaluation, and fallback rules

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

#### Evidence and confidence boundaries

`Implemented` applies to the static tier/contract and declared adapter
projection. `Partial` may describe a locally recorded candidate or evaluation
readiness. Provider-runtime model resolution, actual reasoning support,
token/cost/latency measurements, account availability, and canary outcomes are
`DEFER`. Product-specific surfaces (Codex CLI, OpenAI API/SDK, and Claude Code)
are separate: evidence for one does not transfer to another.

#### 2026-08-10 freshness re-check

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

#### 2026-08-17 full-corpus refresh

This increment is the fifth refresh cycle over this pack, executed under
Spec 058. Unlike the three preceding cycles it re-observed every owner row in
the pack rather than the twelve `Partial` rows, and it assigns each retained
`Partial` or `DEFER` row a blocking class recorded in the
[scope application index](m0013-scope-application-index.md). All observations are
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

#### Historical Review and Freshness

Refresh when a provider changes configuration/model/reasoning semantics or when
a role, model-policy tuple, adapter, evaluation corpus, threshold, candidate,
or promotion decision changes. Recheck official sources and obtain separately
authorized runtime evidence before promoting a configuration.

External sources were re-checked on 2026-08-10; no cited claim changed inside
that window. The re-check recorded that the two Codex pages disagree on model
identifiers, reasoning-effort values, and precedence order, so no single page is
sufficient on its own. None of the four sources publishes a last-modified date,
so an unchanged result is content identity rather than a publisher signal.

#### 2026-08-11 Partial/DEFER incremental refresh

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

#### 2026-08-14 consistency and Partial re-observation

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

#### 2026-08-20 full-corpus reverification

The allocation slice assigns no new source or claim ID for this row.

#### REQ-WERPC-028 model-routing re-observation

- **Sources and external result:** `unchanged`; `SRC-WERPC-049`,
  `SRC-WERPC-045`, and `SRC-WERPC-046` were re-observed on 2026-08-20. The
  official provider pages still describe configuration, subagent model, and
  reasoning surfaces without proving parser acceptance, entitlement, or
  effective resolution.
- **Workspace selector and result:** `confirmed` at baseline commit
  `8d8c8e5634fe939f8daaf041fbf5dfb444ed4a9c` and
  `m0010-agent-model-routing-and-configuration.md#model-routing-baseline`. Local
  policy still maps task/role to provider, configured model tier, reasoning
  effort, and bounded tool surface; the model-fitness contract remains the
  evidence owner for each provider-role tuple.
- **As-Is, gap, and target:** configured incumbent mappings remain `Partial`
  at public-documentation depth. Exact parsing, account-level model and effort
  resolution, task/tool fitness, same-suite quality and safety, cost, latency,
  canary, rollback, and promotion evidence are absent. Preserve each
  incumbent until those evidence classes and independent adjudication exist.
- **Evidence boundary:** blocking class and retained boundary are
  `provider-runtime` / `DEFER`. A documented model name or reasoning level is
  not a stable local target and does not prove that the provider accepted or
  applied the tuple; no runtime promotion is made.
- **Owner, safe follow-up, and trigger:** owner is this reference and the Stage
  00 model policy/model-fitness contract. After platform-owner approval, use
  one non-secret parse/resolution canary for an exact provider-role tuple
  without changing adapters. Refresh when cited configuration, model,
  reasoning, precedence, tool mapping, or a local fitness selector changes.

#### 2026-08-23 Codex routing guidance gap increment

This gap-only increment records current documentation without changing any
model, role, adapter, effort value, evaluation binding, or terminal document
topology. It applies only to the Spec 0054 Claude/Codex provider boundary.

- **Precedence is a product contract, not runtime evidence.** The current
  [Codex subagent
  guide](https://learn.chatgpt.com/docs/agent-configuration/subagents)
  documents agent-file model or reasoning overrides ahead of an explicit spawn
  value, then `[agents]` defaults and the parent setting
  (`SRC-WERPC-011`/`SRC-WERPC-045`). The [configuration
  reference](https://learn.chatgpt.com/docs/config-file/config-reference)
  remains a second required surface for accepted keys and values
  (`SRC-WERPC-010`/`SRC-WERPC-049`). Neither page proves parsing, entitlement,
  effective resolution, or absence of silent fallback in this workspace.
- **Model names are recommendations only.** The current [Codex subagent
  guide](https://learn.chatgpt.com/docs/agent-configuration/subagents) and
  official model guidance assign
  `gpt-5.6` to the most demanding work, `gpt-5.6-terra` to read-heavy analysis,
  and `gpt-5.6-luna` to narrow high-volume work. These names and workload
  descriptions are dated documentation facts, not admitted local routing
  tuples or fitness results; see the [latest-model
  guide](https://developers.openai.com/api/docs/guides/latest-model).
- **Promotion remains closed.** Exact account availability, parser support,
  price, latency, task/tool fitness, quality, safety, fallback behavior,
  canary outcome, and promotion evidence all remain `DEFER`. Do not edit
  configuration from this documentation alone. A future candidate must use
  the same evaluation suite, independent adjudication, an exact resolution
  check, rollback evidence, and platform-owner approval.

**Disposition:** `REQ-WERPC-028` remains `Partial` at public-documentation plus
repository-static depth. The dated guidance refines a candidate hypothesis; it
does not change the model-fitness contract or any configured incumbent.

#### 2026-09-05 external-source reverification

This increment re-observed the model-routing owner under the approved
2026-09-05 follow-on cycle. Workspace re-observation was excluded by direct user
decision. New sources are `SRC-WERPC-128`, `SRC-WERPC-129`, `SRC-WERPC-130`, and
`SRC-WERPC-136`; the cycle claims are `CLM-WERPC-016-04` and `CLM-WERPC-016-05`.

#### REQ-WERPC-028 model-routing re-observation

- **Sources and external result:** `changed` in two independent ways.

  First, the documented subagent model-resolution order changed. The order
  recorded here on 2026-08-14 placed the environment override first; the
  reference observed on 2026-09-05 places the per-invocation value first, then
  the agent-file value, then the environment override, then the parent
  conversation, and attributes the reordering to a named client release
  ([SRC-WERPC-130](m0012-source-coverage.md#2026-09-05-external-source-reverification),
  [SRC-WERPC-134](m0012-source-coverage.md#2026-09-05-external-source-reverification)).
  This supersedes the 2026-08-14 ordering statement as of 2026-09-05; the
  earlier statement remains truthful for its own date.

  Second, the model-identifier disagreement widened. It was previously recorded
  as three generations across two pages of one product. On 2026-09-05 a third
  page states a further generation and a further reasoning-effort vocabulary
  ([SRC-WERPC-129](m0012-source-coverage.md#2026-09-05-external-source-reverification),
  [SRC-WERPC-136](m0012-source-coverage.md#2026-09-05-external-source-reverification)),
  and the other provider's catalogue was captured for the first time
  ([SRC-WERPC-128](m0012-source-coverage.md#2026-09-05-external-source-reverification)).
  No single page is authoritative for a routing target.

  The recorded methodology caveat reproduced during this cycle. A first
  single-pass read of the subagent guidance paraphrased the precedence order
  incorrectly; a second read demanding verbatim text matched the wording already
  on record. Any future check of that page must obtain verbatim text before an
  apparent precedence change is treated as real.
- **Workspace selector and result:** `not observed in this cycle`. The
  [model-routing baseline](#model-routing-baseline) and the local model policy
  retain their earlier repository-static observation dates.
- **As-Is, gap, and target:** the row stays `Partial` at public-documentation
  depth. No promotion, and no candidate is adopted. The practical effect is that
  the specific candidate names recorded on 2026-08-23 are now one generation
  behind the vendors' own general catalogues, while the local disposition that
  model names are recommendations rather than routing authority is strengthened.
- **Evidence boundary:** blocking class and retained boundary remain
  `provider-runtime` / `DEFER`. Public model documentation does not prove parser
  resolution, entitlement, availability, cost, latency, safety, or fitness.
- **Owner, safe follow-up, and trigger:** owner is this reference and the Stage
  00 model policy. The safe follow-up is to keep tier semantics provider-neutral
  and to resolve concrete identifiers only at the adapter edge, under a separate
  authorisation that admits entitlement evidence. Refresh when any cited page
  changes, or when the three pages converge.

## Sources

See [m0012 current source observations](m0012-source-coverage.md#current-source-observations) for SRC-WERPC-011, 049, 128, 136, 169 and 229–237. API model/pricing/rate, Claude costs/configuration/CLI and Codex product catalog/pricing pages were directly read on 2026-09-27. No publisher modification date was exposed in the read snapshots. Mutable aliases, feature gates, rollout dates and retirement dates are different metadata; list prices never prove effective account cost or access.

### Historical source provenance

- [OpenAI Codex configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference), checked 2026-08-08, re-checked 2026-08-10 (`SRC-WERPC-049`).
- [OpenAI Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) and [OpenAI Agents SDK sessions](https://openai.github.io/openai-agents-python/sessions/), checked 2026-08-08, re-checked 2026-08-10 (`SRC-WERPC-045`, `SRC-WERPC-050`).
- [Anthropic Claude Code subagents](https://code.claude.com/docs/en/sub-agents), checked 2026-08-08, re-checked 2026-08-10 (`SRC-WERPC-046`).
- [Model Selection Policy](../../../../.agents/governance/model-selection.md) is the current model-policy owner; `contracts/agent-model-fitness.json` remains part of the dated local observation.

## Review and Freshness

Refresh before material routing/budget decisions and on alias/snapshot, effort/tool/endpoint, context/output, configuration precedence, model retirement, price/region/tier, caching, rate/spend or entitlement changes. Preserve dated price observations rather than presenting them as permanent policy. The next owner needs an authorized exact-model parse and same-suite evaluation, independent adjudication and rollback before any local promotion; actual billing remains separate evidence.

## Related Documents

- [Provider implementation status](m0003-provider-implementation-status.md)
- [AI agents](m0009-ai-agents-and-agency-agents.md)
- [Model Selection Policy](../../../../.agents/governance/model-selection.md)
