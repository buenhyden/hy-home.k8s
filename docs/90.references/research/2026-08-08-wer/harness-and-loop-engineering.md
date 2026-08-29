---
title: 'Reference: Harness and Loop Engineering'
type: content/reference
status: active
owner: platform
updated: 2026-08-10
---

# Reference: Harness and Loop Engineering

## Overview

This reference describes an agent harness as the bounded operating environment
that makes an otherwise probabilistic agent accountable: it supplies context and
tools, limits authority, evaluates observable results, and preserves only
reviewable recovery evidence. It is a dated design and implementation-status
analysis, not a claim that a provider runtime has executed the controls.

## Reference Type

Source-backed design analysis plus repository-static implementation evidence,
observed on 2026-08-08.

## Authority Boundary

The canonical workspace controls remain the Stage 00 rules, contracts, and
validators. Provider documentation establishes a product surface only; an
authenticated execution, hook delivery, permission decision, model resolution,
or live GitOps operation needs its own runtime evidence. The only permitted
default outcome here is repository change plus static verification; no live
cluster or third-party mutation is authorized by this reference.

## Scope

This owner covers REQ-WERPC-001 (harness) and REQ-WERPC-002 (loop): definitions,
components, transitions, evaluation, recovery, observability, and the resulting
workspace target state. Provider-specific discovery and configuration belong in
[provider status](provider-implementation-status.md).

## Definitions / Facts

### Harness baseline

A harness is the control plane around an agent task, rather than the model or a
single prompt. Its minimum components and the evidence required to call each
component present are:

| Component     | Responsibility                                                                                                                      | Workspace owner / present static evidence                                                                                                                     | Status boundary                                                                                                 |
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
session. See [SRC-WERPC-009](source-coverage-and-migration-ledger.md#source-register)
through [SRC-WERPC-013](source-coverage-and-migration-ledger.md#source-register).

### Loop baseline

The workspace machine owner is
[`agent-loop-lifecycle.json`](../../../00.agent-governance/contracts/agent-loop-lifecycle.json).
It is more precise than a generic “observe-plan-act” slogan: it defines terminal
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
not provider features. [SRC-WERPC-010](source-coverage-and-migration-ledger.md#source-register)
and [SRC-WERPC-012](source-coverage-and-migration-ledger.md#source-register)
are therefore supporting context, not authority for the local policy.

### State machine and termination

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

### Retry, stop, and escalation rules

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

### Evaluation and observability

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

### Workspace Application and Gap Matrix

| Concern         | Current repository evidence                                                            | Gap / risk                                                                   | Target state and application rule                                                                                                                               |
| --------------- | -------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Intake context  | JIT bootstrap and `AGENTS.md`/`CLAUDE.md` gateways point to canonical owners.          | Provider discovery is not observed.                                          | At **session** start, record the gateway and scope read; use a native runtime inspection only as separately dated runtime evidence.                             |
| Authority       | GitOps-first and destructive-action boundaries are explicit.                           | Static policy cannot physically prevent every tool outside a given provider. | At **task** scope, reject live mutation, credentials, and external writes unless explicit human approval names target, rollback, and verification.              |
| Validation      | Selected static lanes and full quality gate are defined.                               | No current metric ties a class of defects to control effectiveness.          | At **project/CI** scope, preserve lane distinctions and add a deterministic negative test when a recurring defect exposes a missing control.                    |
| Recovery        | State, retry budget, no-progress rule, checkpoint redaction, and handoff schema exist. | Ignored checkpoint/provider memory execution is unobserved.                  | At **session** scope, rediscover the repository; checkpoint is advisory and cannot override current tracked state.                                              |
| Provider parity | Claude/Codex adapters and shared roster are statically validated.                      | Parity can be mistaken for native behavior.                                  | At **provider** scope, state separately: static configuration, native discovery, authenticated/runtime evidence.                                                |
| Learning        | Durable progress ledger and domain owners are designated.                              | Auto/provider memory may retain inaccurate or sensitive detail.              | At **project** scope, promote only reviewed, redacted, durable lessons; current policy stays in Stage 00 and current implementation truth stays with its owner. |

### Recommended Target State

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

### 2026-08-17 full-corpus refresh

This increment is the fifth refresh cycle over this pack, executed under
Spec 058. Unlike the three preceding cycles it re-observed every owner row in
the pack rather than the twelve `Partial` rows, and it assigns each retained
`Partial` or `DEFER` row a blocking class recorded in the
[scope application index](scope-application-index.md). All observations are
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

## Sources

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

## Related Documents

- [Workspace governance and common environment](workspace-governance-and-common-agent-environment.md)
- [Provider implementation status](provider-implementation-status.md)
- [Source ledger](source-coverage-and-migration-ledger.md)
- [Agent Execution Policy](../../../00.agent-governance/policies/agent-execution.md)
