---
title: 'Reference: Harness and Loop Engineering Research'
type: content/reference
status: draft
owner: platform
updated: 2026-07-10
---

# Reference: Harness and Loop Engineering Research

## Overview

이 문서는 AI 에이전트가 소프트웨어 엔지니어링 작업을 수행할 때 필요한
하네스 엔지니어링과 bounded control loop를 설명한다. 외부의 공식
OpenAI/Codex, Anthropic Claude Code, Gemini CLI, Model Context Protocol(MCP)
자료를 현재 리포지토리 증적과 비교하여, 무엇이 실제로 선언·검증되었고
무엇이 아직 런타임에서 확인되지 않았는지를 구분한다.

This is descriptive Stage 90 reference material. It does not create a retry
policy, change provider permissions, enable MCP servers, or authorize live or
remote actions.

## Purpose

- Define a provider-neutral four-element harness and bounded
  Observe/Plan/Act/Verify/Learn control loop.
- Reconcile the Current and Historical research with canonical Stage 00,
  provider baseline, hook, validation, memory, and Stage 99 ownership.
- Separate declared wiring, validator evidence, provider-native behavior, and
  live/remote readiness.
- Identify evaluation, recovery, termination, compaction, approval, and
  knowledge-update requirements without implementing them from this reference.
- Route provider-specific implementation detail to
  [Provider Implementation Status](provider-implementation-status.md), which is
  owned by WERH-005.

## Reference Type

- Type: durable-concept / external-standard-snapshot
- Source checked: 2026-07-10
- Refresh trigger: official provider harness or agent-loop behavior changes,
  MCP revision/security guidance changes, Stage 00 harness ownership changes,
  provider-native runtime evidence, or validation-loop changes.

## Authority Boundary

- **Authoritative for**:
  - Source-attributed definitions and dated comparison findings checked on
    2026-07-10.
  - A provider-neutral interpretation of harness, loop, evaluation, recovery,
    termination, compaction, approval, and knowledge-update concerns.
  - Follow-up routing to the canonical repository owners.
- **Not authoritative for**:
  - Active governance, retry counts, provider permissions, provider runtime
    configuration, hook failure semantics, subagent dispatch, CI behavior,
    templates, task procedure, or operations runbooks.
  - Claims that Codex or Gemini consumes the tracked hook JSON at runtime.
  - Enabled MCP servers or live Claude, Codex, Gemini, k3d, Argo CD, Vault,
    ESO, Kubernetes, GitHub, deployment, credential, or secret readiness.
  - Provider-specific capability or model status; WERH-005 and
    [Provider Implementation Status](provider-implementation-status.md) own
    that analysis.

## Scope

- Covers the four-element harness, provider-neutral control loop, retry and
  escalation design, evaluation and recovery, termination, compaction,
  approval, knowledge updates, MCP version/security implications, and routed
  implementation gaps.
- Uses repository files and deterministic static output for local facts and
  official first-party sources for external facts.
- Excludes edits to Historical research, Stage 00 policy, shared scripts,
  hooks, provider adapters, runtime configuration, Stage 99 templates, CI,
  manifests, infrastructure, live environments, credentials, and remote state.

## Definitions / Facts

### Harness Ownership Boundary

**Repo fact.** The local harness is a `canonical core + provider adapter +
validation evidence` system. The four linked elements are instruction/settings,
architecture constraints, feedback loops, and knowledge stores. Their current
owners are distributed; `.agents/` is not the owner of governance, memory, or
templates.

| Contract area | Canonical owner | Local adapter or consumer | Evidence boundary |
| --- | --- | --- | --- |
| Governance, approval, execution, and checklist policy | `docs/00.agent-governance/rules/**`, `harness-catalog.md`, `subagent-protocol.md`, and `model-policy.md` | Root gateways and provider notes/baselines point into Stage 00 | Tracked text and repo-quality checks prove repository contracts, not that every host loaded or obeyed them. |
| Shared skills, workflows, and output styles | `.agents/{skills,workflows,output-styles}/` | `.claude/**` and `.codex/**` symlink views | The repository quality gate checks shared-asset structure and mirrors. |
| Gemini baseline and local Gemini adapters | `.agents/GEMINI.md`, `.agents/agents/**`, `.agents/rules/**`, and `.agents/hooks.json` | Gemini/Antigravity-facing local surfaces | File presence is adapter evidence; Gemini-native discovery or policy enforcement is not established by this checkout. |
| Provider-native/local adapters | `.claude/**`, `.codex/**`, and `.agents/**` within each documented boundary | Provider hosts | Similar names do not imply identical permissions, hook semantics, or runtime consumption. |
| Shared hook implementation | `docs/00.agent-governance/hooks/*.sh` | `.claude/settings.json`, `.codex/hooks.json`, and `.agents/hooks.json` declare event wiring | Script and payload simulation evidence does not prove every provider host invokes the wiring. |
| Durable work evidence and memory | `docs/04.execution/tasks/**` and `docs/00.agent-governance/memory/progress.md` | Provider handoffs link or append when their approved scope includes those files | Stage 04 owns task evidence; Stage 00 owns memory. Neither belongs to `.agents/`. |
| Document route and template contract | `docs/99.templates/support/template-routing.md` and `docs/99.templates/templates/**` | Routing skills, authored-doc hooks, and doc-writer adapters consume the contract | Stage 99 remains canonical; `.agents/` only owns the shared skill that may route to it. |
| Dated research synthesis | `docs/90.references/research/2026-07-07-wer/**` | Agents and maintainers use it as lookup context | This reference describes controls and recommendations; it does not enforce them. |

The evidence lanes must remain separate:

| Evidence lane | What this review establishes | What it does not establish |
| --- | --- | --- |
| Declared wiring | Tracked JSON points SessionStart, PreToolUse, PostToolUse, Stop, SubagentStop, and PreCompact events to shared scripts. | A provider host parsed, registered, or invoked those events. |
| Validator evidence | `validate-repo-quality-gates.sh` parses hook JSON, checks required event/script phrases, and simulates hook payloads, including blocking Stop/SubagentStop output and advisory PreCompact output. | End-to-end provider UI behavior, managed/user configuration precedence, or permission enforcement. |
| Runtime/native behavior | Official provider docs describe native subagent, hook, sandbox, approval, or policy-engine surfaces. Claude has tracked native settings/permissions in this repo. | That Codex/Gemini hook JSON is a native permission gate or that untracked provider settings exist. |
| Live/remote readiness | No live or remote check ran for this documentation task. | Claude/Codex/Gemini sessions, MCP connections, cluster health, CI/rulesets, Vault/ESO, deployment, credentials, secrets, or third-party readiness. |

**Fact defect corrected.** Earlier Current wording concentrated role definitions,
the four-element model, progress memory, and shared templates in `.agents/`.
Current canonical evidence limits `.agents/` ownership to shared skills,
workflows, output styles, the Gemini baseline, and its local adapters. Stage 00
owns governance and memory; Stage 99 owns templates; Stage 04 owns task
evidence.

**External fact.** OpenAI's harness account treats repository knowledge as the
system of record, uses a small entry-point map and progressive disclosure, and
mechanically checks architecture and documentation. It also treats repeated
failure as a signal to improve tools, guardrails, documentation, feedback, or
recovery rather than merely retrying the same action.

**Interpretation.** The local four-element model is compatible with that
benchmark, but compatibility is not runtime parity. A provider-neutral contract
needs a stable owner for intent, constraints, feedback, and knowledge while
each provider retains its native enforcement semantics.

### Provider-Neutral Control Loop Matrix

The matrix below is a **recommendation**, not active policy. It expresses the
minimum information a future canonical loop contract should carry. A task must
set its own retry budget and approval boundary; this reference does not invent
a repository-wide number.

| Phase | Inputs | Allowed action | Feedback evidence | Termination condition | Knowledge update |
| --- | --- | --- | --- | --- | --- |
| Observe | User intent, approved Spec/Plan/Task, repo state, canonical owners, current diffs, tool output, external sources, and known limitations | Read and classify facts, unknowns, authority, risk, and evidence lanes; do not mutate live or external state | Evidence inventory with `Repo fact`, `External fact`, `Interpretation`, and `Recommendation` labels | Required owners and success evidence are known; otherwise stop for clarification or record `Unverified` | Add task-local observations and source provenance, not durable policy |
| Plan | Observed facts, scope, acceptance criteria, approval boundary, failure classes, retry budget, and rollback/recovery route | Select the smallest authorized action, verifier, budget, escalation threshold, and handoff shape | Reviewable plan or task criteria tied to commands and expected results | Plan is testable and within authority; unresolved scope or required approval returns control to the human | Record decisions in the owning Spec/Plan/Task only |
| Act | Approved plan, current state, least-privilege tools, remaining retry budget, and human approval state | Make only scoped changes; one recovery attempt consumes budget only after the failure is diagnosed and the input, hypothesis, or implementation changes | Tool result, changed-path inventory, diff, audit log, and approval record where applicable | Planned action completes, an unexpected boundary is reached, approval is required, or safe action is impossible | Preserve material decisions and deviations in task evidence |
| Verify | Acceptance criteria, exact diff, deterministic checks, graders/review, and evidence-lane rules | Run the same defined verifier; classify failure as deterministic, transient, authority/approval, environment, or subjective-review failure | Command exit/output, test/static results, review findings, trace or transcript reference, and explicit skipped lanes | All required evidence passes; otherwise enter recovery while budget remains or escalate/terminate | Record pass/fail/skip honestly; static PASS never becomes live readiness |
| Learn/Handoff | Final evidence, remaining risks, failure history, changed files, approvals, and unresolved unknowns | Summarize outcome, route durable learning to the smallest canonical owner, and return control to the human or next task | Task verification summary, commit/diff identity, review state, limitations, and next owner | Success is evidenced, or incomplete work has an explicit blocker, owner, and safe continuation point | Update Stage 04 evidence and, only when in approved scope, Stage 00 progress memory or another canonical owner |
| Cross-phase: retry budget and failure escalation | Attempt count, repeated failure signature, elapsed/resource budget, and risk class | Retry only after diagnosis changes the next attempt; do not repeat identical tool calls or broaden authority | Attempt log with cause, changed hypothesis, and repeated-failure detection | Budget exhausted, the same blocking condition repeats, risk increases, or new authority is needed: stop and escalate | Store the failure class and next safe action in the task handoff |
| Cross-phase: compaction | Context pressure, active plan, changed paths, verification state, approvals, and remaining budget | Create a compact checkpoint before continuing; never treat compaction as verification or permission | Checkpoint records goal, decisions, files, commands/results, risks, and next step | Continue only when critical state is recoverable; otherwise hand off or ask the human | Preserve durable facts in canonical task/memory owners, not only a generated summary |
| Cross-phase: human approval | Planned mutation, affected system/data/people, privilege, rollback, and evidence requirement | Pause before approval-bound live, remote, credential, secret-value, publish, merge, push, paid, or protected-control action | Explicit approval scope or explicit denial/absence of approval | Approved action returns to Act; denial, timeout, or inability to surface approval terminates the branch safely | Record only approval scope and redacted evidence; never secret values |

**External fact.** OpenAI describes a turn as repeated inference and tool calls
until the model emits an assistant message, which is a loop termination state.
It also documents automatic compaction after a context threshold. Claude Code
and Gemini CLI document isolated subagent contexts, scoped tools, and explicit
turn limits; Codex documents thread/depth/runtime controls and inherited
sandbox/approval behavior. These are provider benchmarks, not proof of this
workspace's local provider configuration. WERH-005 owns the surface-by-surface
comparison.

**Repo fact.** The local `lifecycle-guard.sh` can emit structured block output
for objective Stop/SubagentStop validation failures and emits advisory output
for PreCompact. It does not maintain an attempt counter, set a retry budget,
grade agent behavior, or write a compaction checkpoint. Its block output is
validated by payload simulation. Whether a provider host consumes that output
at runtime remains provider-specific evidence.

### Evaluation and Recovery Loop

A reliable loop evaluates both the outcome and the path used to reach it.
Provider-neutral evaluation should combine:

1. **Capability criteria**: the Task states the intended behavior, input and
   authority boundaries, affected paths, required evidence, and termination
   conditions before work starts.
2. **Deterministic regression evidence**: rerunnable tests, linters, parsers,
   static validators, diff checks, and artifact checks protect known contracts.
3. **Traceability**: tool results, changed paths, attempt count, failure class,
   grader/reviewer findings, approval state, and skipped evidence lanes remain
   attributable to one task attempt.
4. **Calibrated judgment**: a human or model reviewer may grade subjective
   qualities, but the task must identify the rubric and cannot relabel that
   judgment as deterministic PASS.
5. **Evidence separation**: repo-static, CI/toolchain, provider-runtime, and
   live/remote results remain independent.

The recommended recovery state machine is:

```text
Verify failure
  -> preserve failing evidence
  -> classify cause and authority
  -> change hypothesis/input/implementation
  -> consume one declared retry unit
  -> rerun the same verifier
  -> PASS: Learn/Handoff
  -> budget/authority/risk boundary: Escalate or terminate safely
```

Recovery is not an identical retry. A new attempt is justified only when the
failure evidence changes the next hypothesis, input, implementation, tool, or
environment. The smallest owning surface should be repaired. Repeated harness
drift routes to a rule, skill, hook, validator, template, index, or memory owner;
product or infrastructure defects route to their implementation owners.

Provider-neutral termination modes are:

- **Success**: all required evidence passes and the handoff names limitations.
- **Needs human approval**: safe progress stops before the approval-bound
  action; no permission is inferred.
- **Blocked/unverified**: required evidence or authority is unavailable and a
  canonical follow-up owner is named.
- **Budget exhausted or repeated failure**: stop recovery, preserve attempts,
  and escalate without broadening scope.
- **Cancelled/interrupted**: leave the checkout and external state safe, then
  record the incomplete boundary.
- **Compacted continuation**: continue only from a checkpoint that preserves
  the active goal, decisions, evidence, approvals, and next verifier.

Current repository evaluation is repo-static by default: the harness catalog
defines capability criteria in Task records and regression evidence through
explicit commands/validators. There is no provider-neutral trial dataset,
attempt schema, numeric retry budget, behavioral grader, or automatically
verified compaction handoff. Those absences are recommendations for later
canonical work, not defects repaired by this reference.

### MCP Version and Security Boundary

**External fact.** The official MCP versioning page identifies `2025-11-25` as
the Current protocol revision, ready for use. It labels past complete revisions
Final. Therefore the plan's required `2025-06-18` source is retained as a
historical Final revision; it is not the latest stable/current specification.
The `2025-11-25` changelog records the changes since `2025-06-18`, including
experimental durable Tasks and updated security guidance.

The following threat names and mitigation summaries use only the official MCP
Security Best Practices taxonomy checked on 2026-07-10:

| Official threat category | Official mitigation direction | Workspace implication |
| --- | --- | --- |
| Confused Deputy Problem | MCP proxies must enforce per-client consent before third-party authorization, exact redirect-URI checks, and secure one-time state handling | Do not treat upstream authorization or a cached consent as workspace approval for a different client/action. |
| Token Passthrough | MCP servers must not accept tokens that were not explicitly issued for that server | Never infer credential reuse or downstream authority from tool availability. |
| Server-Side Request Forgery (SSRF) | Server-side clients must consider SSRF; production OAuth URLs should use HTTPS, private/link-local targets and unsafe redirects should be restricted, and egress controls should be considered | Remote MCP discovery requires a separate network/egress review; no local config is enabled by this reference. |
| Session Hijacking | Authorized servers must verify inbound requests, must not use sessions as authentication, must use secure nondeterministic IDs, and should bind IDs to user identity | Session IDs are not approval or identity evidence; provider-runtime evidence must preserve user/action attribution. |
| Local MCP Server Compromise | One-click configuration must show the exact command and obtain explicit consent; sandboxing, restricted filesystem/network access, and constrained transports are recommended | Treat local server installation as code execution and route it through provider configuration, sandbox, and approval owners. |
| OAuth Authorization URL Validation | Clients must restrict URL schemes, reject dangerous schemes, avoid shell-based URL opening, and validate/sanitize URLs | Provider adapters must not pass authorization URLs through shell execution or weaken the host approval boundary. |
| stdio Transport Security in Proxy Scenarios | Proxy designs should prevent enabling client-side vulnerabilities, sandbox spawned processes, restrict filesystem access, log use, and require extra authorization for dangerous commands | Direct `stdio` is not labeled inherently vulnerable; proxy process spawning requires its own least-privilege review. |
| Scope Minimization | Start with minimal baseline scopes, elevate incrementally through precise challenges, accept reduced scopes, and log correlated elevation | Default to discovery/read scope and require targeted approval for privileged operations; avoid wildcard/full-access grants. |

**Repo fact.** No tracked `.mcp.json`, `.codex/config.toml`, or
`.gemini/settings.json` exists in this checkout, so enabled local MCP servers,
their scopes, credentials, transports, and runtime behavior are Unverified.
Provider-specific MCP configuration remains WERH-005 scope.

### Harness and Loop Gap Register

This register uses only the approved classification vocabulary. It records
recommendations and canonical follow-up routes; it does not mutate the owners.

| ID | Classification | Severity | Risk rationale | Recommendation | Canonical follow-up |
| --- | --- | --- | --- | --- | --- |
| HL-001 | Fact defect | High | Assigning governance, memory, the four-element contract, or Stage 99 templates to `.agents/` hides the real authority boundary and can send policy changes to the wrong surface. | Keep the corrected ownership boundary and check the rest of the Current pack for the stale broad `.agents/` claim. | WERH-009 cross-document integration in [the current Task record](../../../04.execution/tasks/2026-07-10-current-research-pack-fact-first-hardening.md). |
| HL-002 | Implementation gap | High | The canonical loop requires validation but defines no task-level attempt schema, retry budget, repeated-failure threshold, or failure-escalation contract; identical retries can consume context and hide non-convergence. | In a separate approved change, define a bounded retry/escalation contract that every applicable Task must instantiate without imposing an arbitrary count from this reference. | [Agentic Execution Rules](../../../00.agent-governance/rules/agentic.md). |
| HL-003 | Needs strengthening | Medium | Current capability/regression eval language is accurate, but there is no common record for trials, traces, graders/rubrics, failure classes, and attempt-to-attempt comparison, limiting behavioral regression analysis. | Add an optional provider-neutral eval/evidence block only after a Spec/Plan/Task defines the schema and validator impact. | [Harness Task Contract Template](../../../99.templates/templates/sdlc/specs/harness-task-contract.template.md). |
| HL-004 | Implementation gap | Medium | PreCompact reports dirty paths and suggested validation but does not require a recoverable checkpoint containing goal, decisions, evidence, approval state, remaining budget, and next verifier. | Define a compact handoff/checkpoint contract in later canonical governance; keep compaction advisory unless a provider-specific design proves safe blocking semantics. | [Agentic Execution Rules](../../../00.agent-governance/rules/agentic.md). |
| HL-005 | Unverified | High | Tracked Codex/Gemini hook JSON and payload simulations can be mistaken for native permission or runtime-consumption evidence, creating false provider parity. | Keep status at declared wiring plus validator evidence until provider-native canaries record actual discovery, event handling, permission behavior, and managed/user precedence. | WERH-005 in [Provider Implementation Status](provider-implementation-status.md). |
| HL-006 | Unverified | High | Repo-static PASS or opt-in probe wiring can be promoted incorrectly to live provider, MCP, cluster, CI, credential, or remote readiness. | Preserve separate evidence lanes and require an explicitly approved operator/runtime check before any live/remote readiness claim. | [Harness Implementation Map: Live Runtime Evidence](../../../00.agent-governance/harness-implementation-map.md#live-runtime-evidence). |
| HL-007 | Implementation gap | High | No tracked MCP configuration or inventory proves server trust, command visibility, transport, scope, token audience, or egress controls against the current official taxonomy. | Do not enable or describe MCP servers as ready; require a separate approved provider/security task to inventory each server against the eight official categories above. | WERH-005 in [Provider Implementation Status](provider-implementation-status.md). |

## Sources

Official external sources, Source checked 2026-07-10:

| Source lane | Claim use | Exact URL |
| --- | --- | --- |
| OpenAI harness engineering | Repo legibility, progressive disclosure, mechanical constraints, feedback, recovery, human judgment, and garbage collection | <https://openai.com/index/harness-engineering/> |
| OpenAI Codex agent loop | Tool-result iteration, assistant-message termination, context growth, and compaction | <https://openai.com/index/unrolling-the-codex-agent-loop/> |
| Codex subagents | Thread orchestration, context isolation, concurrency/depth/runtime settings, and inherited sandbox/approval boundaries | <https://developers.openai.com/codex/subagents/> |
| Claude Code subagents | Isolated contexts, tool/permission scopes, `maxTurns`, and handoff to the parent | <https://code.claude.com/docs/en/sub-agents> |
| Claude Code hooks | Native event, block, Stop/SubagentStop, and PreCompact semantics | <https://code.claude.com/docs/en/hooks> |
| Gemini CLI subagents | Native `.gemini/agents/` surface, isolated contexts/tools, recursion protection, turn/time bounds, and subagent policies | <https://geminicli.com/docs/core/subagents/> |
| Gemini CLI policy engine | Native allow/deny/ask-user decisions, priority/approval modes, MCP/subagent targeting, and current workspace-tier limitation | <https://geminicli.com/docs/reference/policy-engine/> |
| MCP 2025-06-18 specification | Required historical Final revision | <https://modelcontextprotocol.io/specification/2025-06-18> |
| MCP Security Best Practices | Official attack and mitigation taxonomy used in this reference | <https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices> |
| MCP 2025-11-25 specification | Current/latest protocol revision | <https://modelcontextprotocol.io/specification/2025-11-25> |
| MCP versioning | Current, Final, Draft revision vocabulary and current-version identification | <https://modelcontextprotocol.io/docs/learn/versioning> |
| MCP 2025-11-25 changelog | Changes since 2025-06-18 and security-guidance update | <https://modelcontextprotocol.io/specification/2025-11-25/changelog> |

Repo-backed sources, inspected 2026-07-10:

- [Local Harness Catalog](../../../00.agent-governance/harness-catalog.md)
- [Harness Implementation Map](../../../00.agent-governance/harness-implementation-map.md)
- [Subagent Protocol](../../../00.agent-governance/subagent-protocol.md)
- [Model Selection Policy](../../../00.agent-governance/model-policy.md)
- [Agentic Execution Rules](../../../00.agent-governance/rules/agentic.md)
- [Harness Approval Boundaries](../../../00.agent-governance/rules/approval-boundaries.md)
- [Codex Provider Notes](../../../00.agent-governance/providers/codex.md)
- [Claude Provider Notes](../../../00.agent-governance/providers/claude.md)
- [Gemini Provider Notes](../../../00.agent-governance/providers/gemini.md)
- [Shared Lifecycle Guard](../../../00.agent-governance/hooks/lifecycle-guard.sh)
- [Codex Runtime Baseline](../../../../.codex/CODEX.md)
- [Claude Runtime Baseline](../../../../.claude/CLAUDE.md)
- [Gemini Runtime Baseline](../../../../.agents/GEMINI.md)
- [Current Workspace Governance Baseline](workspace-governance-baseline.md)
- [Historical Harness and Loop Research](../2026-07-04-wer/harness-and-loop-engineering.md)
- [2026-07-05 Governance/Harness/Loop Audit](../../audits/2026-07-05-wea/governance-harness-loop-providers.md)
- [2026-07-02 Harness/Loop Implementation Audit](../../audits/2026-07-02-whia/harness-loop-implementation-audit.md)
- [2026-07-02 Provider Harness/Loop Audit](../../audits/2026-07-02-whia/provider-harness-loop-implementation-audit.md)
- [Reference Template](../../../99.templates/templates/common/reference.template.md)
- [Template Routing Contract](../../../99.templates/support/template-routing.md)

No market-scan source is used as authority.

## Review and Freshness

- Review cadence: on source or canonical-owner change
- Last reviewed: 2026-07-10
- Next review trigger: OpenAI harness/loop update, Claude/Codex/Gemini
  subagent or permission/hook change, MCP Current revision or security taxonomy
  change, tracked provider configuration, lifecycle/eval/retry contract change,
  or provider-native/live evidence becoming available.
- Cutoff limitation: sources reflect pages checked on 2026-07-10. Later page
  changes require a new source check and must not be back-projected into this
  snapshot.
- Evidence limitation: no provider-native canary, live cluster, MCP connection,
  credential, secret-value, GitHub remote/CI/ruleset, publish, push, merge, or
  third-party mutation check ran.

## Related Documents

- **Parent research README**: [README.md](../README.md)
- **References README**: [../../README.md](../../README.md)
- **Workspace baseline**: [Workspace Governance Baseline](workspace-governance-baseline.md)
- **Provider-specific owner**: [Provider Implementation Status](provider-implementation-status.md)
- **Spec**: [Workspace Engineering Research Pack Spec](../../../03.specs/017-workspace-engineering-research-pack/spec.md)
- **Current Plan**: [Current Research Pack Fact-First Hardening Plan](../../../04.execution/plans/2026-07-10-current-research-pack-fact-first-hardening.md)
- **Current Task**: [Current Research Pack Fact-First Hardening Task](../../../04.execution/tasks/2026-07-10-current-research-pack-fact-first-hardening.md)
- **Harness catalog**: [Local Harness Catalog](../../../00.agent-governance/harness-catalog.md)
- **Implementation map**: [Harness Implementation Map](../../../00.agent-governance/harness-implementation-map.md)
- **Reference maintenance runbook**: [Reference Maintenance Runbook](../../../05.operations/runbooks/0011-reference-maintenance-runbook.md)
