---
title: "Reference: Harness and Loop Engineering"
version: "1.2.0"
type: "reference/research"
status: "published"
owner: "platform"
updated: "2026-09-27"
layer: "references"
artifact_id: "RES-0001-m0002"
---

# Reference: Harness and Loop Engineering

## Overview

This reference distinguishes an agent harness from the loops it hosts. It synthesizes directly read vendor engineering cases and product/SDK contracts into bounded design choices for context, tools, state, evaluation, budgets and recovery. It does not establish an implemented local harness.

## Reference Type

Primary-source external research and conditional investigation design, directly observed on 2026-09-27. Dated prior repository observations are retained below as history.

## Authority Boundary

Official sources establish only the identified external product or method. This reference grants no local permission, policy change, installation, model promotion or operational approval. Every current workspace implementation, discovery, authentication, enforcement, runtime, billing and live result is `not observed in this cycle`. Candidate paths are investigation selectors, not observed files. External finding judgments and source refresh results remain separate from document QA and future workspace observations.

## Scope

Primary owner of U01 and U02 and existing REQ-WERPC-001 and REQ-WERPC-002. Covers harness components, observe/plan/act/verify transitions, independent evaluation, stopping, checkpoints, retries/backoff, idempotency, concurrency and escalation. Product-native loops, SDK orchestration and external runners are separate implementation choices. Excludes local runner inspection, provider execution, background scheduling and live mutation.

## Definitions / Facts

### Harness components and lifecycle

`CLM-WERPC-017-09` uses **harness** as the host environment around an agent: context construction, tools/skills, execution isolation, permissions/sandbox, planning and state, evaluation, observability, recovery and handoff. OpenAI's harness case describes isolated worktrees, browser/log/metric visibility and mechanical feedback; Anthropic distinguishes predefined workflows from agents that dynamically choose actions. Neither case is a certified universal architecture. Prefer the simplest workflow that meets the task; use autonomous choice only when the needed flexibility justifies greater cost and harder verification. Sources: SRC-WERPC-155 and SRC-WERPC-123, including its separate effective-agents URL observation.

| Component | Purpose and implementation choice | Prerequisite, failure and check |
| --- | --- | --- |
| Context and tools | A small owner map plus task evidence; explicit skills and bounded tool capabilities. | Verify discovery separately from presence; filter untrusted source instructions and prevent sensitive-data promotion. |
| Isolation and authority | Local process/worktree, SDK environment or cloud task boundary with native sandbox and approvals. | A worktree prevents some file collisions, not network or credential access. Negative permission evidence requires approved runtime observation. |
| Plan and state | Goal, acceptance, invariants, remaining work and checkpoint; host controls transitions. | Stale state can claim completion early; compare resumed state with fresh files and canonical evidence. |
| Evaluation | Deterministic acceptance plus independent reviewer/evaluator for material risk. | Model self-confidence or an agent's final response is insufficient; reproduce pass and deliberate negative cases. |
| Observation and recovery | Sanitized actions, outcomes, resource use, progress and next owner. | Missing telemetry, lossy summaries or unsafe retries hide failures; retain bounded provenance and explicit stop reasons. |

`CLM-WERPC-017-10` defines **loop engineering** here as designing repeated observe → plan → act → verify transitions against a goal and invariants, with independent review, stop conditions and recoverable handoff. This is a working definition, not a single accredited standard. Anthropic's long-running harness case shows that compaction alone does not maintain progress: initialization, feature tests and incremental verified work provide durable state. Its loop article distinguishes turn-based agent completion, goal-based evaluation plus a turn bound, time-based repetition and proactive/cloud routines; those are product-specific examples. Deterministic criteria, small pilots and fresh review support bounded autonomy. Sources: SRC-WERPC-123 and SRC-WERPC-124.

`CLM-WERPC-017-11` compares where orchestration lives:

| Choice | Directly read contract | Trade-off and excluded inference |
| --- | --- | --- |
| Native product loop | Codex `/goal` stores a chat goal with edit/pause/resume/clear controls and a 4,000-character bound; Claude documents local time loops and cloud `/schedule` routines at stated preview boundaries. | Less runner code, but product/account/version semantics apply. Goal length is not a dollar budget or portable state machine. |
| OpenAI Agents SDK | `Runner` continues tool calls/handoffs and stops at final output; `max_turns` counts model calls and raises `MaxTurnsExceeded`; `None` removes that bound. | Explicit orchestration and evaluation hooks cost engineering effort. It is distinct from the Codex SDK. |
| Claude Agent SDK | Hosts the Claude Code binary's agent loop, tools, context, permissions and sessions. | It is distinct from the Anthropic API Client SDK; embedding it does not grant subscription use or third-party execution permission. |
| Codex SDK | TypeScript threads require Node 18+; Python App Server JSON-RPC uses Python 3.10+ and a pinned CLI. | Session/CLI compatibility and host permissions remain prerequisites; no universal budget or account entitlement follows. |
| External runner | Host implements state, budgets, scheduling and durable evidence across products. | More control and portability, with duplicate-execution, checkpoint and maintenance risk. Add only for an evidenced native/SDK limitation. |

Sources: SRC-WERPC-163, 166, 239 and 241. Product support is `Verified` in the bounded documentation; comparative fit is a conditional proposal, not measured performance.

### Loop design and failure controls

`CLM-WERPC-017-12` recommends explicit iteration, elapsed-time, input/output-token, dollar, tool-call, concurrency and retry bounds at the owning host. Apply aggregate budgets across children and keep counters across provider/model fallback. A larger model or new thread must not reset failure history. Claude's print-mode `--max-turns` has no default cap and `--max-budget-usd` counts subagents; documented background/spawn behavior has a v2.1.217 gate and resumed prior spend is not counted. Codex context/automatic-compaction values use model defaults when unset, while agent concurrency limits are not a dollar cap. Sources: SRC-WERPC-237 and SRC-WERPC-049. Effective budget closure and billing are unobserved.

`CLM-WERPC-017-13` separates failure classes before retry:

| Failure class | Safe response design | Verification and limit |
| --- | --- | --- |
| Approval or policy denial | Stop at the authority boundary and name the responsible owner. | More retries or changing provider cannot manufacture authority. |
| Missing environment/tool | Identify the missing prerequisite; use a scoped alternative only if already authorized. | Repeated identical execution gives no new evidence; do not label unavailable execution a pass. |
| Provider rate/acceleration limit | Bound exponential backoff with jitter, honor documented retry timing, reduce/ramp concurrency. | Failed OpenAI requests still consume allowance. Anthropic distinguishes RPM/input/output-token limits and acceleration limits. |
| Provider spend/account cap | Stop and hand off account/budget decisions. | Anthropic hard spend 429 has no retry-after and `enforced_spend_limit_reached`; user caps can return 400. Generic retry is inappropriate. |
| Repository defect | Reproduce the failing acceptance case; make the smallest authorized repair and recheck. | Repair outside owned paths needs the owning role/scope; provider fallback is not a code fix. |

Sources: SRC-WERPC-232, 234 and 236. Claude's documented model fallback excludes authentication, billing, rate, size, transport and policy denial failures; fallback is not a general recovery mechanism.

`CLM-WERPC-017-14` treats checkpoint/resume and idempotency as different contracts. SDK sessions store/retrieve conversation items, but backend and serialized compaction recovery can fail. Claude's JSONL resume/fork retains history while current files may differ; compaction is lossy, and file checkpoint rewind is not Git or external-database undo. Conditional runner controls are atomic bounded checkpoints, unique external operation keys, observation before retry, one writer per owned path and explicit collision handling. A retry of a non-idempotent external operation needs verified prior outcome or operator reconciliation. Sources: SRC-WERPC-050 and SRC-WERPC-096.

`CLM-WERPC-017-15` separates autonomy from gates. Native filesystem/network sandbox, tool approval, hook trust and deterministic acceptance protect different boundaries. Post-tool hooks cannot undo an action; documented hook coverage and timeout/error behavior must be tested for the exact event. OpenAI's engineering case describes an experimental merge approach; it is not approval to copy permissive merging into infrastructure work. Sources: SRC-WERPC-012, 006, 242 and 155.

`CLM-WERPC-017-16` proposes measurable progress deltas and a host-owned no-progress stop rather than repeated confidence statements. Independent validation should distinguish repository-static, hosted CI, provider-runtime and live effects; retain sanitized command/source/version, outcome, timing/usage, remaining work and next owner. Do not retain credentials, raw transcripts or unlimited diagnostics. Stop when acceptance is met, budget expires, the same failure recurs without new information, required authority/environment is missing or the user stops. These are research design options; exact local counts remain with the canonical procedure and were not inspected as an implementation audit.

### Harness and loop questions

Full scope, selectors, approval and acceptance live in the [follow-up question ledger](m0013-scope-application-index.md#follow-up-question-ledger); every current result is `not observed in this cycle`.

- Q-WERPC-011: which native product, SDK or runner owns goals, transitions, budgets and resume? Candidates: runner configuration, SDK call sites, task contracts and scheduled-job declarations.
- Q-WERPC-012: which acceptance criteria and independent negative/reviewer evidence close the loop, rather than the agent's final text?
- Q-WERPC-013: how are permission, missing environment, 429/spend and repository failures distinguished, bounded and handed off? Examine retry configuration and sanitized result records.
- Q-WERPC-014: how do concurrent child work, shared file ownership and aggregate time/token/spend limits interact? Test a synthetic collision and exhausted shared budget only in an approved disposable environment.
- Q-WERPC-015: what measurable delta separates progress from repeated failure, and what checkpoint/stop evidence persists?
- Q-WERPC-016: can resume detect changed Git/task state and unknown non-idempotent outcomes without claiming checkpoint replay or rewind undoes external effects?

- Q-WERPC-017: which harness components and source-specific loop terminology apply, and which owner separates native features from custom state/control?
- Q-WERPC-018: what exact approval, sandbox, hook and independent acceptance evidence limits autonomy without copying experimental permissive merge policy?

### Historical observations and corrections — 2026-08-08 to 2026-09-05

The following records preserve their original observation dates, evidence boundaries, status and correction relationships. They are historical provenance, not current workspace findings or instructions. Retired paths and old counts remain statements about their recorded cycles. Current workspace result: `not observed in this cycle`.

#### Historical Overview

This reference describes an agent harness as the bounded operating environment
that makes an otherwise probabilistic agent accountable: it supplies context and
tools, limits authority, evaluates observable results, and preserves only
reviewable recovery evidence. It is a dated design and implementation-status
analysis, not a claim that a provider runtime has executed the controls.

#### Historical Reference Type

Source-backed design analysis plus repository-static implementation evidence,
observed on 2026-08-08.

#### Historical Authority Boundary

The canonical workspace controls remain the Stage 00 rules, contracts, and
validators. Provider documentation establishes a product surface only; an
authenticated execution, hook delivery, permission decision, model resolution,
or live GitOps operation needs its own runtime evidence. The only permitted
default outcome here is repository change plus static verification; no live
cluster or third-party mutation is authorized by this reference.

#### Historical Scope

This owner covers REQ-WERPC-001 (harness) and REQ-WERPC-002 (loop): definitions,
components, transitions, evaluation, recovery, observability, and the resulting
workspace target state. Provider-specific discovery and configuration belong in
[provider status](m0003-provider-implementation-status.md).

#### Historical Definitions / Facts

#### Harness baseline

A harness is the control plane around an agent task, rather than the model or a
single prompt. Its minimum components and the evidence required to call each
component present are:

> [!NOTE]
> The rows below are observations at the dates their cycles record, not the
> current owner graph. `docs/00.agent-governance/` and its `memory/`, `rules/`,
> `contracts/` and `harness-catalog.md` were retired, `.agents/agents/` and
> `.gemini/` are not part of the current two-provider surface, and common
> authority now lives under `.agents/` with progress owned by the Stage 03 Task.

| Component     | Responsibility                                                                                                                      | Workspace owner at the recorded observation                                                                                                                   | Status boundary                                                                                                 |
| ------------- | ----------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| Context       | Load task, scope, canonical owners, and local instructions in an ordered, bounded form.                                             | `AGENTS.md`, `CLAUDE.md`, `.codex/CODEX.md`, bootstrap, scope, provider note, and `memory/progress.md` state the JIT order.                                   | Verified as tracked text; native loading is `DEFER`.                                                            |
| Tools         | Provide only task-relevant file, shell, validation, and approved read-only research capabilities.                                   | `RTK.md`, validation-surface contract, provider adapters, and tool instructions.                                                                              | Partial: static routing exists; actual installed-tool/provider availability is runtime-specific.                |
| Guardrails    | Bound filesystem, approval, destructive action, secret, GitOps, and delegation authority before action.                             | `rules/agentic.md`, approval boundary, `.claude/settings.json`, plus Codex's documented sandbox/approval surface. No project `.codex/config.toml` is tracked. | Partial: workspace policy and Claude static settings exist; Codex project configuration/enforcement is `DEFER`. |
| Evaluation    | Turn acceptance criteria into deterministic checks and separate static, CI, and live evidence.                                      | `rules/quality-standards.md`, `contracts/validation-surfaces.json`, repository quality gate.                                                                  | Verified as static contract; a passing static lane is not a live result.                                        |
| Recovery      | Normalize failures, prohibit no-progress repetition, retain redacted checkpoint/handoff material, and stop at authority boundaries. | `contracts/agent-loop-lifecycle.json` and checkpoint schema.                                                                                                  | Verified as tracked executable-contract surface; actual provider checkpoint use is `DEFER`.                     |
| Observability | Produce redacted, attributable evidence of action, result, limitation, and handoff.                                                 | Task records, `memory/progress.md`, lifecycle contracts, validators.                                                                                          | Partial: schema and durable ledger exist; telemetry completeness is not measured.                               |

This aligns with OpenAI's official Codex guidance that durable instructions,
configuration, subagents, and MCP define a repeatable workflow, and
with its instruction-discovery and hook documentation; those sources do not
claim that this particular repository's configuration was consumed in a given
session. See [SRC-WERPC-009](m0012-source-coverage.md#source-register)
through [SRC-WERPC-013](m0012-source-coverage.md#source-register).

#### Loop baseline

At this observation, the workspace machine owner was
[`agent-loop-lifecycle.json` at its retained Git revision](https://github.com/buenhyden/hy-home.k8s/blob/193e5b8859db5731128a2236545f2f75bee37be4/docs/00.agent-governance/contracts/agent-loop-lifecycle.json).
Current procedure is owned by [work lifecycle](../../../../.agents/workflows/work-lifecycle.md).
The historical contract was more precise than a generic “observe-plan-act” slogan: it defined terminal
states, admissible transitions, failure normalization, retry budgets, and
redaction. The intended human-readable loop is:

1. **Observe / ready** — rediscover repository state, task scope, authority,
   and acceptance criteria. Repository evidence wins any checkpoint or memory
   conflict.
2. **Plan / start** — choose one authorized, bounded action with a named
   expected evidence delta.
3. **Act / running** — perform the action without crossing the sandbox,
   approval, secrets, or live-mutation boundary.
4. **Verify / validating** — run the selected deterministic evidence lane;
   classify its output rather than treating narrative confidence as evidence.
5. **Learn / hand off** — preserve compact, reviewed lessons in the appropriate
   durable/domain owner only after outcome and sensitivity review.

The external Codex documentation supports the general orchestration surfaces
(instructions, configuration, hooks, subagents, and approval/sandbox); the
state names, retry numbers, and evidence rules below are workspace controls,
not provider features. [SRC-WERPC-010](m0012-source-coverage.md#source-register)
and [SRC-WERPC-012](m0012-source-coverage.md#source-register)
are therefore supporting context, not authority for the local policy.

#### State machine and termination

| State              | Entry event                                                               | Authorized next outcome                                                                                                                                          | Terminal condition / evidence                                  |
| ------------------ | ------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| `ready`            | Task inputs and repository observation are complete.                      | `start` → `running`.                                                                                                                                             | No; incomplete scope or authority remains a preflight blocker. |
| `running`          | One authorized action begins.                                             | `submit-for-validation` → `validating`.                                                                                                                          | No; action output alone is not success.                        |
| `validating`       | A deterministic check or bounded observation completes.                   | pass → `completed`; recoverable failure → `retry-assessment`; blocked dependency → `blocked`; escalation-required → `escalated`; explicit user stop → `aborted`. | No.                                                            |
| `retry-assessment` | A normalized recoverable failure exists.                                  | approved different action → `running`; denied/budget-exhausted → `escalated`.                                                                                    | No.                                                            |
| `completed`        | Every named acceptance condition passed.                                  | none.                                                                                                                                                            | Yes; only terminal success state.                              |
| `blocked`          | A required dependency or authority is unavailable.                        | none.                                                                                                                                                            | Yes; record exact blocker and owner.                           |
| `escalated`        | Automatic recovery is unsafe, non-retryable, no-progress, or over budget. | none.                                                                                                                                                            | Yes; an owned human/supervisor decision is needed.             |
| `aborted`          | User explicitly stops the work.                                           | none.                                                                                                                                                            | Yes; do not make further automatic action.                     |

The transition table is an implementation fact from the local contract. It
does not prove that all provider runs emit every event. A runtime event record
must be redacted and include the task/role/provider identity, transition,
attempt and recovery counters, signature digest, progress delta, result class,
validation reference, stop reason, handoff owner, and redaction result.

#### Retry, stop, and escalation rules

The loop does not retry an error merely because it is inconvenient. The current
contract permits at most two automatic retries for the same normalized failure
signature and three recovery actions per task (using the lower applicable
limit). A retry must take a **different** action and produce deterministic
progress. The evaluation order is non-retryable class, second identical
no-progress result, per-signature budget, task budget, then different-action
requirement.

| Condition                                                                                                       | Decision                            | Reason / required handoff content                                                                    |
| --------------------------------------------------------------------------------------------------------------- | ----------------------------------- | ---------------------------------------------------------------------------------------------------- |
| Validation passes all named criteria.                                                                           | Stop `completed`.                   | Record scope, commands, result lane, limitations, rollback, reviewer, and next owner.                |
| Same normalized result recurs without an allowed progress delta.                                                | Escalate on the second observation. | Repeating commands, more tokens, wording changes, and unverified fallbacks do not count as progress. |
| Permission denial, credential boundary, secret detection, destructive live-mutation risk, or schema corruption. | Escalate immediately.               | These are non-retryable; preserve the sanitized class, never credential/raw diagnostic content.      |
| Missing authority or dependency.                                                                                | Stop `blocked`.                     | Name the dependency/authority and the decision required; do not silently broaden access.             |
| User stop.                                                                                                      | Stop `aborted`.                     | Do not continue automatically.                                                                       |
| Recoverable failure within budgets with a distinct safe action.                                                 | Retry.                              | Record normalized signature, budget consumption, expected measurable delta, and next validation.     |

Provider, model, tool, or handoff fallback does not reset counters. That prevents
“retry by relabeling” and makes escalation auditable. It is a local policy;
it is not inferred from either provider's product documentation.

#### Evaluation and observability

Evaluation is a hierarchy, not one green command. The workspace names the
`targeted`, `affected`, `staged`, `tests`, `all-files`, `formatter-review`,
`rerun`, and `diff-checks` phases in that order. Each uses `PASS`, `SKIP`,
`FAIL`, or `DEFER`; `DEFER` is a visible missing-evidence class rather than a
success. CI, provider-runtime, remote, and live-cluster evidence are separate
lanes. The minimum task record therefore contains:

- the scope, acceptance IDs, changed paths, command and tool/version;
- the selected lane and its result, including skipped-tool reason;
- sanitized failure signature and measurable progress delta when retrying;
- reviewer/disposition, rollback procedure, residual risk, limitation, and
  next owner; and
- no secret values, raw prompts/transcripts, credentials, environment dumps,
  provider response bodies, or unbounded command output.

This produces observability useful for corrective action without treating task
prose, token count, or static adapter presence as an operating measurement.

#### Workspace Application and Gap Matrix

| Concern         | Current repository evidence                                                            | Gap / risk                                                                   | Target state and application rule                                                                                                                               |
| --------------- | -------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Intake context  | JIT bootstrap and `AGENTS.md`/`CLAUDE.md` gateways point to canonical owners.          | Provider discovery is not observed.                                          | At **session** start, record the gateway and scope read; use a native runtime inspection only as separately dated runtime evidence.                             |
| Authority       | GitOps-first and destructive-action boundaries are explicit.                           | Static policy cannot physically prevent every tool outside a given provider. | At **task** scope, reject live mutation, credentials, and external writes unless explicit human approval names target, rollback, and verification.              |
| Validation      | Selected static lanes and full quality gate are defined.                               | No current metric ties a class of defects to control effectiveness.          | At **project/CI** scope, preserve lane distinctions and add a deterministic negative test when a recurring defect exposes a missing control.                    |
| Recovery        | State, retry budget, no-progress rule, checkpoint redaction, and handoff schema exist. | Ignored checkpoint/provider memory execution is unobserved.                  | At **session** scope, rediscover the repository; checkpoint is advisory and cannot override current tracked state.                                              |
| Provider parity | Claude/Codex adapters and shared roster are statically validated.                      | Parity can be mistaken for native behavior.                                  | At **provider** scope, state separately: static configuration, native discovery, authenticated/runtime evidence.                                                |
| Learning        | Durable progress ledger and domain owners are designated.                              | Auto/provider memory may retain inaccurate or sensitive detail.              | At **project** scope, promote only reviewed, redacted, durable lessons; current policy stays in Stage 00 and current implementation truth stays with its owner. |

#### Recommended Target State

The target is a provider-neutral control plane with provider-specific adapters
at the edge. It does not require identical files or promises that two clients
implement hooks the same way. It requires the following invariants:

| Scope     | Required control                                                                                     | Failure/security boundary                                                           |
| --------- | ---------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| Work item | Acceptance IDs, owned paths, authority, validation and rollback are explicit before edits.           | Out-of-scope path, unclear owner, or missing approval stops work.                   |
| Session   | Fresh repository observation, scoped instructions, bounded tools, and compact redacted handoff.      | Provider/local memory is advisory; repository wins conflicts.                       |
| Project   | Canonical rules, contracts, templates, validators, and durable ledger are versioned.                 | A static file proves configuration only, not discovery or enforcement.              |
| Provider  | Map instruction/config/hook/agent/MCP/sandbox/approval semantics to the provider's official surface. | Never transpose a Claude setting into Codex evidence, or vice versa.                |
| CI        | Run repository-static checks over the declared path set and retain reviewed results.                 | CI/static PASS is not hosted execution, provider runtime, or live deployment proof. |

Apply these in stages: (1) bind every non-trivial task to the state machine and
evidence lanes; (2) require an explicit normalized failure/progress record
before any retry; (3) ensure every provider adapter says what it can prove and
what remains `DEFER`; and (4) periodically inspect recurring failures to change
the smallest authoritative rule, validator, or template. Do not promote a
marketing feature statement or inference into implementation truth.

#### 2026-08-17 full-corpus refresh

This increment is the fifth refresh cycle over this pack, executed under
Spec 058. Unlike the three preceding cycles it re-observed every owner row in
the pack rather than the twelve `Partial` rows, and it assigns each retained
`Partial` or `DEFER` row a blocking class recorded in the
[scope application index](m0013-scope-application-index.md). All observations are
dated **2026-08-17**. No live cluster, hosted CI run, provider runtime,
authenticated execution, or secret value was observed.

#### REQ-WERPC-001 and REQ-WERPC-002 re-observation

**External result:** `unchanged` for both rows (`SRC-WERPC-078`). The Codex
configuration reference, subagents, and `AGENTS.md` pages still describe the
same instruction-discovery, config, hook, subagent, and sandbox surfaces this
report cites as harness-component evidence. Discovery mechanics are unchanged:
global override, then a project walk from the Git root, then concatenation with
closer files winning, under a 32 KiB `project_doc_max_bytes` default. No
provider page documents a state machine, retry budget, or termination
vocabulary, which continues to support this report's claim that the loop's state
names and retry counts are workspace policy rather than provider features.

**Workspace result:** `confirmed` for both rows. `.codex/CODEX.md:102-105` still
states that the presence of `.codex/agents/*.toml` or `.codex/hooks.json` is
repository-static evidence only and does not prove native discovery or role
consumption. `docs/00.agent-governance/rules/agentic.md:21-29` still carries the
Direct Mutation Boundary and its no-live-mutation-without-approval rule.

**Status effect:** `no-change` for both (`CLM-WERPC-011-01`,
`CLM-WERPC-011-02`). Both rows keep `Verified` on static harness and loop
contract, with provider-runtime delivery `DEFER`.

**Blocking class:** `provider-runtime` for both, structurally unreachable by
repository-static work. Reopens when a provider publishes documented retry or
termination semantics, when `contracts/agent-loop-lifecycle.json` changes, or
when authorized provider-runtime evidence is collected.

#### Historical Review and Freshness

Refresh this reference when a loop-contract version, validation-lane contract,
or official provider behavior materially changes. Recheck each external source
on a provider release affecting instructions, hooks, subagents, sandbox or
approval behavior; retain the old checked date rather than silently moving it.
No native discovery, hook delivery, credential-bearing action, hosted CI, or
live-cluster observation was collected for WERPC-002.

External sources were re-checked on 2026-08-10 and no cited claim changed. The
config reference still carries the retry, interrupt, approval, hook-event, and
telemetry keys this report relies on. Two bounded observations are recorded
without changing a claim. First, `developers.openai.com/codex` now answers with
a permanent redirect to `learn.chatgpt.com/docs`; the redirect was observed today
and cannot be attributed to the two-day window, since the pack already cited the
`learn.chatgpt.com` host on 2026-08-08. Second, the `openai/codex` default branch
carries unreleased commits dated 2026-08-08 to 2026-08-10 touching approval,
config, and hook surfaces, with no corresponding change to the published README
or to any documented key. Unreleased source movement is not a documented
behavior change and is not adopted here.

#### 2026-08-20 full-corpus reverification

This increment re-observed both owner rows at workspace baseline
`8d8c8e5634fe939f8daaf041fbf5dfb444ed4a9c`. External and workspace
results remain independent. The allocation slice assigns no new source or
claim ID, so this section cites the existing source identities and does not
change the shared ledger.

#### REQ-WERPC-001 harness re-observation

- **Sources and external result:** `unchanged`; `SRC-WERPC-009` through
  `SRC-WERPC-013` were re-observed on 2026-08-20. Current official Codex
  pages still describe instruction, configuration, sandbox, model, subagent,
  hook, and MCP surfaces. They do not establish this workspace runtime.
- **Workspace selector and result:** `confirmed` at
  `m0002-harness-and-loop-engineering.md#harness-baseline`. The repository-static
  control plane still owns context, role and task instructions, bounded tools
  and permissions, orchestration and isolation boundaries, evaluation,
  checkpoint/recovery contracts, observability, and handoff evidence.
- **As-Is, gap, and target:** the static harness remains `Verified`; native
  instruction discovery, permission enforcement, hook delivery, MCP
  connection, model resolution, execution, and runtime cost/latency telemetry
  are not observed. Keep provider product surfaces separate from local
  controls and admit runtime or cost evidence only through a separately
  authorized observation.
- **Evidence boundary:** depth is `repository-static`; blocking class and
  retained execution boundary are `provider-runtime` / `DEFER`. Tracked files
  and public documentation do not prove that a provider loaded or enforced
  any control in this session.
- **Owner, safe follow-up, and trigger:** owner is this reference and the
  linked Stage 00 harness contracts. After approval, use one read-only,
  redacted canary for one named provider control; do not invoke credential or
  live-GitOps paths. Refresh when a cited instruction, configuration, sandbox,
  model, subagent, hook, MCP, or local harness contract materially changes.

#### REQ-WERPC-002 loop re-observation

- **Sources and external result:** `unchanged`; `SRC-WERPC-010` and
  `SRC-WERPC-012` were re-observed on 2026-08-20. They remain supporting
  context for orchestration surfaces; loop states and retry budgets remain
  local policy.
- **Workspace selector and result:** `confirmed` at
  `m0002-harness-and-loop-engineering.md#loop-baseline`. The local contract still
  defines ready/running/validating/retry-assessment and terminal states,
  bounded retry and recovery budgets, second-identical-result no-progress
  escalation, redaction, validation, and owned handoff.
- **As-Is, gap, and target:** the repository-static loop remains `Verified`.
  Provider event emission, actual checkpoint use, executed recovery, and
  deterministic replay are not observed. Retain the local lifecycle as the
  authority and require a redacted event record before asserting provider
  execution or replay behavior.
- **Evidence boundary:** depth is `repository-static`; blocking class and
  retained execution boundary are `provider-runtime` / `DEFER`. Public hook
  or configuration semantics do not prove that a provider followed this
  state machine or that a retry made measurable progress.
- **Owner, safe follow-up, and trigger:** owner is this reference and
  `agent-loop-lifecycle.json`. After approval, run one non-secret canary for
  an exact provider/version and retain only redacted transition, stop,
  recovery, and handoff metadata. Refresh when a cited Codex orchestration
  surface or the local lifecycle/checkpoint contract changes.

#### 2026-08-23 provider-control gap increment

This gap-only increment follows the Spec 0054 terminal provider boundary:
Claude and Codex are the provider adapters under comparison, while the shared
repository contract remains provider-neutral. It changes no adapter, hook,
model configuration, owner, validator, or document topology.

#### Codex orchestration and hook delta

- **Documented fact:** the current [Codex configuration
  reference](https://learn.chatgpt.com/docs/config-file/config-reference) and
  [subagent guide](https://learn.chatgpt.com/docs/agent-configuration/subagents)
  describe multi-agent operation as stable and enabled by default. This
  supersedes an experimental-only product-surface description, but it does not
  prove native agent discovery or delegation in this worktree
  (`SRC-WERPC-010`–`011`).
- **Documented fact:** the current [Codex hooks
  guide](https://learn.chatgpt.com/docs/hooks) includes lifecycle events such
  as `Stop`, `SubagentStop`, `PreCompact`, and `PostCompact`
  (`SRC-WERPC-012`). Their existence supplies interception and observation
  points; it does not make hook coverage complete or a hook equivalent to the
  workspace approval, sandbox, validation, or termination contracts.
- **Loop rule:** the subagent permission contract is fail-closed. If a child
  needs approval and cannot obtain it, the operation returns failure to the
  parent. The local loop must classify that evidence as `FAIL`, `blocked`, or
  `escalated` according to the owning contract; it must never infer `PASS` from
  absent approval or absent hook output.

#### Claude hook delta

The current [Claude Code hooks
guide](https://code.claude.com/docs/en/hooks-guide) distinguishes deterministic
command hooks, suitable for production guardrails, from prompt- or agent-based
hooks whose agent-hook surface is experimental (`SRC-WERPC-006`). A command
hook can enforce its documented exit-code contract, but tracked configuration
still does not prove trust, delivery, execution, or complete coverage. Agent
hooks therefore remain advisory until separately validated and cannot replace
the same approval and deterministic validation owners.

**Disposition:** the public capability description changed, while local
runtime evidence did not. Harness and loop contracts remain `Verified` at
repository-static depth; provider discovery, hook delivery, approval handling,
delegation, compaction-event delivery, and enforcement completeness remain
`provider-runtime` / `DEFER`. Recheck on a provider lifecycle, permission, or
multi-agent contract change, and admit promotion only from a separately
authorized, non-secret runtime observation.

#### 2026-09-05 external-source reverification

This increment re-observed the external evidence layer for the two harness and
loop owners under the approved 2026-09-05 follow-on cycle. Workspace
re-observation was excluded from this cycle by direct user decision, so the
workspace selectors below retain their earlier observation dates and no local
status is promoted or demoted. New sources are `SRC-WERPC-123` and
`SRC-WERPC-124`; the cycle claim is `CLM-WERPC-016-01`.

#### REQ-WERPC-001 harness re-observation

- **Sources and external result:** `changed` by coverage. Two official vendor
  engineering publications now define an agent harness directly and distinguish
  orchestrated workflows from self-directing agents. They were observed on
  2026-09-05 and registered as
  [SRC-WERPC-123](m0012-source-coverage.md#2026-09-05-external-source-reverification).
  Until this cycle the harness baseline above cited only provider configuration
  pages, which describe surfaces rather than the harness concept.
- **Workspace selector and result:** `not observed in this cycle`. The
  [harness baseline](#harness-baseline) component table retains its earlier
  repository-static observation date; no local file was re-read here.
- **As-Is, gap, and target:** the row stays `Verified` at public-documentation
  depth. The gap is narrower than before, because the local six-component model
  can now be compared against an external definition instead of being derived
  only from configuration surfaces. Whether the local model agrees with,
  extends, or diverges from that definition is not assessed here and is the
  next safe step.
- **Evidence boundary:** blocking class and retained boundary remain
  `provider-runtime` / `DEFER`. A vendor definition establishes vocabulary, not
  that this repository's harness is loaded, dispatched, or effective.
- **Owner, safe follow-up, and trigger:** owner is this reference and the Stage
  00 harness contracts. The safe follow-up is a bounded reading comparison
  between the external definition and the component table, with no contract
  edit. Refresh when a further vendor harness publication appears or the local
  harness contract changes.

#### REQ-WERPC-002 loop re-observation

- **Sources and external result:** `changed` by coverage. An official vendor
  publication dated 2026-06-30 now names four loop types, turn-based,
  goal-based, time-based, and proactive, and recommends deterministic
  verifiable stop conditions over subjective ones. It was observed on
  2026-09-05 and registered as
  [SRC-WERPC-124](m0012-source-coverage.md#2026-09-05-external-source-reverification).
- **Workspace selector and result:** `not observed in this cycle`. The
  [loop baseline](#loop-baseline) and the state and termination table retain
  their earlier repository-static observation dates.
- **As-Is, gap, and target:** the row stays `Verified` at public-documentation
  depth. The external taxonomy classifies loops by what ends them, while the
  local contract enumerates terminal states and transitions; the two are
  compatible framings at different levels and neither supersedes the other. The
  external preference for deterministic stop conditions agrees with the local
  rule that a deterministic evidence lane, not narrative confidence, closes a
  loop.
- **Evidence boundary:** blocking class and retained boundary remain
  `provider-runtime` / `DEFER`. The transition table is a local implementation
  fact; no provider is proven to emit any event.
- **Owner, safe follow-up, and trigger:** owner is this reference and the local
  loop lifecycle contract. The safe follow-up is to record, without changing the
  contract, which local terminal states correspond to which external loop type.
  Refresh when a further vendor loop publication appears or the local lifecycle
  contract changes.

## Sources

See [current source observations](m0012-source-coverage.md#current-source-observations) for SRC-WERPC-006, 012, 049, 050, 096, 123, 124, 155, 163, 166, 232, 234, 236, 237, 239, 241 and 242 and their per-URL claims/limits. All were directly read on 2026-09-27. Engineering publication dates: OpenAI harness 2026-02-11, Anthropic long-running harness 2025-11-26, effective-agents article 2024-12-19 and loops article 2026-06-30. Access dates are not release or modification dates; unversioned SDK pages do not prove an installed package revision.

### Historical source provenance

- **SRC-WERPC-009–013** — official OpenAI Codex materials, checked 2026-08-08,
  re-checked 2026-08-10.
  A locally supplied manual cache outside the repository was the first
  consultation surface; it is ephemeral and not reproducible, so the durable
  citation is the official URL. The ledger records each direct URL, adopted
  claim boundary, and refresh trigger.
- **Workspace evidence** — `.codex/CODEX.md`, `rules/agentic.md`,
  `rules/quality-standards.md`, and `contracts/agent-loop-lifecycle.json`,
  observed in this worktree on 2026-08-08. These support repository-static
  implementation claims only.

## Review and Freshness

Refresh when loop or SDK termination, background schedule, checkpoint/session semantics, hook failure behavior, retry/rate/spend contract or cost/concurrency controls change. Future evaluation uses one exact product/version and sanitized synthetic inputs under separately authorized runtime scope. No external operation, installed runner, checkpoint contents, hosted task or live environment was observed here.

## Related Documents

- [Workspace governance and common environment](m0001-workspace-governance-and-common-agent-environment.md)
- [Provider implementation status](m0003-provider-implementation-status.md)
- [Source ledger](m0012-source-coverage.md)
- [Agent Execution Policy](../../../../.agents/governance/agent-execution.md)
