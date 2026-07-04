---
title: 'Reference: Harness and Loop Engineering Research'
type: content/reference
status: draft
owner: platform
updated: 2026-07-04
---

# Reference: Harness and Loop Engineering Research

## Overview

This reference summarizes harness engineering and loop engineering patterns for
agentic software work, using official OpenAI/Codex, Anthropic/Claude Code,
Google/Gemini, MCP, and repo-backed sources checked on 2026-07-04. It maps
those patterns back to the local `hy-home.k8s` four-element harness model
without redefining active governance.

This is durable reference material. It should help future agents and
maintainers reason about instruction surfaces, constraints, feedback loops,
knowledge stores, evals, review loops, and tool boundaries before proposing
follow-up work in the canonical owner documents.

## Purpose

- Provide a source-attributed snapshot of current harness and loop engineering
  concepts.
- Connect external agent-loop guidance to this repository's existing
  four-element harness model.
- Preserve a non-authoritative market scan for emerging terminology and risks.
- Name workspace application requirements and follow-up routes without creating
  new policy in `docs/90.references/research/`.

## Reference Type

- Type: durable-concept / external-standard-snapshot
- Source checked: 2026-07-04
- Refresh trigger: provider agent-loop docs changes, MCP/security changes,
  harness catalog changes, validation-loop changes, or research pack structure
  changes.

## Authority Boundary

- **Authoritative for**:
  - Source-attributed definitions and dated reference findings checked on
    2026-07-04.
  - Mapping external harness, loop, eval, and MCP concepts to the local
    repository's current reference model.
  - Checklist-level follow-up routing to canonical repo owners.
- **Not authoritative for**:
  - Active governance policy, provider runtime permissions, CI semantics,
    task execution procedure, subagent dispatch policy, or live operations.
  - Live k3d, ArgoCD, Vault, ESO, Kubernetes, deployment, or secret readiness.
  - Provider implementation status for Claude, Codex/OpenAI, or Gemini/Google;
    that belongs to the provider implementation status reference.
  - Spec, SDLC, CI, QA, or formatting policy; that belongs to the dedicated
    SDLC/CI/QA/formatting reference and canonical repo owners.

## Scope

- Covers harness engineering elements, loop engineering elements, feedback and
  eval loops, review-loop implications, MCP/tool boundary implications,
  common environment/rule-system construction, non-authoritative market scan
  findings, workspace application requirements, and implementation checklist
  items.
- Excludes changes to Stage 00 governance, provider adapters, CI workflows,
  validation scripts, task workflow policy, live cluster procedure, and
  third-party resources.
- Excludes provider-by-provider implementation status and SDLC formatting
  analysis except where those topics are necessary context for harness and loop
  engineering.

## Definitions / Facts

### Harness engineering elements

Harness engineering is the design of the environment that lets a model act as a
software agent. OpenAI frames this as the work of making repositories, tools,
feedback, and knowledge legible enough that agents can reliably do useful work;
the engineer's leverage moves from writing every line to designing
environments, specifying intent, and building feedback loops.

For this repository, harness engineering maps directly to the four-element
model in [harness-catalog.md](../../../00.agent-governance/harness-catalog.md):

- **Instruction/settings**: gateway files, provider baselines, task prompts,
  templates, and scope docs that tell an agent how to act.
- **Architecture constraints**: sandboxing, approval boundaries, GitOps-first
  limits, template routing, subagent scope, least-privilege tools, and
  validation requirements that constrain unsafe or off-domain action.
- **Feedback loops**: repo-static validators, hooks, task evidence, review
  loops, CI checks, and explicit verification commands that turn edits into
  evidence.
- **Knowledge stores**: Stage docs, research references, generated indexes, and
  the progress ledger that make durable context discoverable across sessions.

OpenAI's harness engineering guidance emphasizes repo-local knowledge as the
system of record, progressive disclosure instead of one giant instruction file,
mechanical checks for architecture and documentation, and feedback-driven
garbage collection when drift appears. The 2026-07-04 official-source review
adds provider-specific implementation surfaces to the same pattern: Codex
documents `AGENTS.md`, rules, hooks, skills, subagents, sandboxing, approvals,
and MCP; Claude Code documents settings, hooks, subagents, skills, and MCP;
Gemini CLI documents `GEMINI.md`, tools, MCP, extensions, and terminal-agent
automation; Google ADK documents a broader multi-agent/evaluation framework.
Those points reinforce this workspace's thin-gateway, template-first,
validation-backed model.

### Loop engineering elements

Loop engineering is the design of the repeated control cycle that drives an
agent from intent to verified completion. A practical loop for this workspace is:

- **Observe**: read the task, repo state, relevant docs, external sources, tool
  results, and current validation failures.
- **Plan**: choose the smallest scoped route, define verification evidence, and
  identify authority boundaries.
- **Act**: edit or generate only the approved surfaces using repo-native
  patterns and least-privilege tools.
- **Verify**: run deterministic checks, inspect outputs, compare results to the
  original request, and record evidence.
- **Learn**: route durable lessons to the appropriate owner, such as task
  evidence, progress memory, reference docs, templates, hooks, validators, or
  governance rules.

OpenAI's Codex loop article describes the agent loop as orchestration among the
user, model, tools, environment state, and final assistant handoff. For software
agents, the main output can be changed files or executed tool actions rather
than only a chat response, so context-window management, tool-result handling,
and termination criteria become loop responsibilities.

The checked provider documentation adds concrete loop surfaces around that
concept: Codex documents CLI execution, sandboxing, approvals, hooks, rules,
skills, subagents, and MCP; Claude Code documents settings, hooks, subagents,
skills, and MCP; Gemini CLI and Google ADK document terminal-agent, context,
MCP, multi-agent, tool, workflow, deployment, and evaluation surfaces. Those
surfaces are inputs to local loop design, not proof that each provider enforces
the same runtime controls.

A useful local meta-loop is to collect task evidence, attach human or model
feedback, turn repeated feedback into deterministic checks or eval criteria,
and use the evidence to propose the next harness changes. In this repository,
that meta-loop should route actual changes to canonical owners rather than
embedding policy in this reference.

The cross-provider control cycle checked on 2026-07-04 is therefore not just
`prompt -> answer`. It is `instruction context -> constrained tool action ->
observable evidence -> review/repair -> durable memory or contract update`.
For this workspace, a loop is incomplete until the task record and validation
summary say what was checked and which evidence lane it belongs to.

### Feedback and eval loops

Feedback loops convert agent work into signals that can be checked, repeated,
and improved. Official and repo-backed sources converge on several facts:

- Agent evals need task definitions, attempts or trials, graders, transcripts or
  traces, outcome checks, and suites that measure specific behaviors.
- Coding-agent evals are strongest when deterministic tests, static analysis,
  outcome checks, and tool-call checks are combined with calibrated human or
  model review where subjective quality matters.
- Capability evals and regression evals serve different purposes: one finds the
  hill to climb; the other protects against backsliding.
- Repair loops should not simply retry. They should inspect the failure,
  compare against the task or spec, change the smallest relevant surface, and
  re-run the same evidence path.
- Static validation is evidence for repo correctness only. It must not be
  reported as live k3d, ArgoCD, Vault, ESO, Kubernetes, deployment, or secret
  readiness.

Local implications are already implemented as Stage 04 task evidence,
`scripts/validate-repo-quality-gates.sh .`, optional CI/toolchain lanes, and
separate live-runtime evidence boundaries in the harness catalog and
implementation map.

Provider-loop implication: Claude can express more native blocking behavior
through settings and hook decision control; Codex can combine sandbox modes,
approval policies, rules, hooks, skills, subagents, and MCP; Gemini CLI exposes
terminal-agent tooling, MCP, context, and automation, while Google ADK provides
multi-agent and evaluation primitives outside this repo's local CLI mirror.
Local documentation must keep those capabilities separate from this checkout's
implemented adapter wiring.

### Worktree/subagent/review-loop implications

OpenAI's harness engineering post highlights isolated worktrees, local app
instances, observability, validation, review, and feedback handling as practical
ways to make higher-autonomy agent work reliable. This repository should apply
that pattern conservatively through its existing contracts:

- **Task-by-task commits**: logical units should be committed separately, with
  the task record naming evidence for each unit.
- **Subagent reviews**: delegated work and review should follow
  [subagent-protocol.md](../../../00.agent-governance/subagent-protocol.md) and the
  local runtime roster. Subagents must remain scoped to their file ownership and
  tool boundary.
- **Review loops**: agent or human feedback should produce targeted edits,
  repeat validation, and record evidence rather than silently broadening scope.
- **Static validation evidence**: repo-static gates, diff checks, and task
  evidence are required before handoff. They do not prove live operations.
- **Provider parity limits**: upstream provider docs can identify available
  loop surfaces, but local parity still requires repo-backed adapter evidence
  and must preserve each provider's native permission and hook semantics.
- **Garbage collection**: repeated drift should update the smallest durable
  harness surface that would prevent recurrence, such as a rule, prompt/skill,
  hook, validator, template, README index, archive Tombstone, or memory entry.

### MCP and tool boundary implications

MCP is a protocol for connecting models and agent hosts to tools, resources,
prompts, and related capabilities. The 2025-06-18 MCP specification explicitly
places security and trust obligations on implementors because MCP can expose
arbitrary data access and code execution paths.

Workspace implications:

- **Least privilege**: tools, MCP scopes, local commands, and subagent toolsets
  should start with minimal read/discovery capability and elevate only for a
  specific approved action.
- **Consent and authorization**: users must understand and approve data access,
  tool invocation, and privileged actions. This aligns with the repository's
  external-action rule: networked tools are read-only by default unless the user
  explicitly approves mutation.
- **Tool poisoning risks**: tool descriptions, annotations, schemas, or other
  metadata can contain malicious or misleading instructions. MCP tool behavior
  descriptions should be treated as untrusted unless they come from a trusted
  server and are reviewable.
- **Local server risk**: local MCP servers can execute code with the client's
  privileges. Consent dialogs, exact command visibility, sandboxing, restricted
  filesystem/network access, and logging are relevant controls.
- **Token and scope risk**: broad scopes increase blast radius and hide intent.
  Scope minimization, precise elevation prompts, down-scoping tolerance, and
  audit logs are safer defaults.
- **Provider-local configuration risk**: provider MCP configuration belongs to
  the relevant trusted provider layer or managed configuration route. This
  reference does not infer active MCP servers from a provider's upstream
  support alone.

This reference does not authorize adding or changing MCP servers. New or
modified tools belong in the provider/runtime adapter, approval-boundary,
security, and task evidence routes named by the harness catalog and
implementation map.

### Non-authoritative market scan

The following findings are non-authoritative market scan material. They are
synthesized from official/primary source surfaces checked on 2026-07-04 and
repo-backed evidence. They may inform terminology and future investigation, but
they do not override official provider documentation, MCP specifications, or
repo-backed contracts.

- The provider landscape is converging on five repeated harness primitives:
  persistent instruction files, tool/MCP integrations, reusable skills or
  commands, subagents or multi-agent delegation, and lifecycle feedback through
  hooks, approvals, evals, or review loops.
- OpenAI/Codex is market-positioned around repo-local harness engineering,
  `AGENTS.md`, sandboxing, approvals, hooks, rules, skills, subagents, MCP,
  worktrees, and explicit agent-loop termination criteria.
- Anthropic/Claude Code is market-positioned around project/user/managed
  settings, native hook decision control, subagent context isolation, skills,
  MCP server scoping, and permission policy layers.
- Google/Gemini is split across Gemini CLI as a terminal-first coding agent
  with `GEMINI.md`, tools, MCP, automation, extensions, and ADK as a broader
  framework for multi-agent orchestration, evaluation, deployment, and
  enterprise-scale agent systems.
- MCP has become the common integration vocabulary across all three provider
  families, but the official MCP spec and security guidance emphasize consent,
  untrusted tool metadata, explicit authorization, token audience separation,
  and SSRF/local-server risks.
- The practical market gap for this repository is provider parity illusion:
  similar nouns such as hooks, skills, agents, or MCP do not mean identical
  enforcement. The local system should build a common contract, provider
  adapters, and repeatable evidence instead of asserting runtime equivalence.

### Workspace application requirements

For `hy-home.k8s`, source-backed harness and loop engineering should preserve
these requirements:

- Keep `docs/00.agent-governance/harness-catalog.md` as the canonical local
  harness model and runtime roster.
- Keep `docs/00.agent-governance/harness-implementation-map.md` as the
  navigation map from harness surface to source of truth, validation, and
  evidence location.
- Keep task evidence in Stage 04 and progress/memory routing in the canonical
  progress ledger when a task's write scope allows it.
- Keep reference material descriptive and dated; route behavior changes to
  Stage 00, Stage 03, Stage 04, Stage 05, scripts, templates, or provider
  adapters.
- Keep the common provider environment as `canonical core + provider adapter +
  validation evidence`: Stage 00 owns rules and harness contracts, root shims
  route providers into that core, `.agents/**` owns shared assets, and
  provider-native files express only the runtime-specific adapter syntax.
- Keep external tools read-only by default unless the user approves a specific
  external mutation, push, publish, merge, credential change, paid job, or
  third-party resource change.
- Keep market scan findings labeled non-authoritative.
- Keep repo-static, CI/toolchain, and live-runtime evidence lanes separate.
- Keep upstream provider capability claims separate from the repo's adapter
  implementation status, especially when a provider documents a broad agent
  framework but the local adapter only exposes a mirrored behavioral contract.

### Implementation checklist

- Update harness model or runtime roster changes in
  [harness-catalog.md](../../../00.agent-governance/harness-catalog.md).
- Update source-of-truth routing, validation owners, and evidence locations in
  [harness-implementation-map.md](../../../00.agent-governance/harness-implementation-map.md).
- Route subagent dispatch, scope, tool, and mirror changes through
  [subagent-protocol.md](../../../00.agent-governance/subagent-protocol.md) and
  the provider agent files.
- Route approval-boundary or external-action changes to
  `docs/00.agent-governance/rules/approval-boundaries.md`.
- Route template or reference-format changes to
  [Templates README](../../../99.templates/README.md),
  [reference.template.md](../../../99.templates/templates/common/reference.template.md), and the
  repository quality gate when applicable.
- Route validation-loop or repo-static evidence changes to `scripts/**`,
  `.github/workflows/ci.yml`, Stage 04 task evidence, and the CI/CD QA guide.
- Route new research-pack status and validation evidence to
  [Workspace Engineering Research Pack Task](../../../04.execution/tasks/2026-07-04-workspace-engineering-research-pack.md).
- Route durable progress/memory updates to
  `docs/00.agent-governance/memory/progress.md` when the active task write
  scope includes that file.
- Before handoff, run `git diff --check` and
  `bash scripts/validate-repo-quality-gates.sh .`, then record PASS/FAIL and
  limitations in the task record.

## Sources

Official and primary external sources, checked 2026-07-04:

OpenAI/Codex:

- [Codex documentation home](https://developers.openai.com/codex/)
- [Codex CLI](https://developers.openai.com/codex/cli/)
- [Codex configuration reference](https://developers.openai.com/codex/config-reference/)
- [Codex agent approvals and security](https://developers.openai.com/codex/agent-approvals-security/)
- [Codex sandboxing](https://developers.openai.com/codex/concepts/sandboxing/)
- [Codex MCP](https://developers.openai.com/codex/mcp/)
- [Codex subagents](https://developers.openai.com/codex/subagents/)
- [Codex hooks](https://developers.openai.com/codex/hooks/)
- [Codex skills](https://developers.openai.com/codex/skills/)
- [Codex rules](https://developers.openai.com/codex/rules/)
- [OpenAI: Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/)
- [OpenAI: Unrolling the Codex agent loop](https://openai.com/index/unrolling-the-codex-agent-loop/)

Anthropic Claude Code:

- [Claude Code settings](https://code.claude.com/docs/en/settings)
- [Claude Code hooks](https://code.claude.com/docs/en/hooks)
- [Claude Code subagents](https://code.claude.com/docs/en/sub-agents)
- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [Claude Code MCP](https://code.claude.com/docs/en/mcp)

Google/Gemini/ADK:

- [Gemini CLI repository](https://github.com/google-gemini/gemini-cli)
- [Gemini CLI docs tree](https://github.com/google-gemini/gemini-cli/tree/main/docs)
- [Google Cloud Agent Development Kit page](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/adk)
- [ADK site](https://adk.dev/)

MCP:

- [Model Context Protocol Specification, version 2025-06-18](https://modelcontextprotocol.io/specification/2025-06-18)
- [Model Context Protocol Security Best Practices](https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices)

Repo-backed sources:

- [Local Harness Catalog](../../../00.agent-governance/harness-catalog.md)
- [Harness Implementation Map](../../../00.agent-governance/harness-implementation-map.md)
- [Subagent Protocol](../../../00.agent-governance/subagent-protocol.md)
- [Workspace Governance Baseline Research](workspace-governance-baseline.md)
- [Workspace Engineering Research Pack Spec](../../../03.specs/017-workspace-engineering-research-pack/spec.md)
- [Workspace Engineering Research Pack Plan](../../../04.execution/plans/2026-07-04-workspace-engineering-research-pack.md)
- [Workspace Engineering Research Pack Task](../../../04.execution/tasks/2026-07-04-workspace-engineering-research-pack.md)

Market scan:

- None used as authority. The non-authoritative market scan above is a
  synthesis of the official/provider and repo-backed source set checked on
  2026-07-04.

## Review and Freshness

- Review cadence: on source change
- Last reviewed: 2026-07-04
- Next review trigger: provider agent-loop docs changes, MCP/security changes,
  harness catalog changes, validation-loop changes, research pack structure
  changes, or repeated drift in task/review/evidence loops.

## Related Documents

- **Parent research README**: [README.md](../README.md)
- **Parent references README**: [90.references README](../../README.md)
- **Workspace baseline**: [Workspace Governance Baseline Research](workspace-governance-baseline.md)
- **Spec**: [Workspace Engineering Research Pack Spec](../../../03.specs/017-workspace-engineering-research-pack/spec.md)
- **Plan**: [Workspace Engineering Research Pack Plan](../../../04.execution/plans/2026-07-04-workspace-engineering-research-pack.md)
- **Task**: [Workspace Engineering Research Pack Task](../../../04.execution/tasks/2026-07-04-workspace-engineering-research-pack.md)
- **Harness catalog**: [Local Harness Catalog](../../../00.agent-governance/harness-catalog.md)
- **Implementation map**: [Harness Implementation Map](../../../00.agent-governance/harness-implementation-map.md)
- **Subagent protocol**: [Subagent Protocol](../../../00.agent-governance/subagent-protocol.md)
- **Reference maintenance runbook**: [Reference Maintenance Runbook](../../../05.operations/runbooks/0011-reference-maintenance-runbook.md)
