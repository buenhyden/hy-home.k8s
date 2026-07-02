---
title: 'Reference: Harness and Loop Engineering Research'
type: reference
status: draft
owner: platform
updated: 2026-07-02
---

# Reference: Harness and Loop Engineering Research

## Overview

This reference summarizes harness engineering and loop engineering patterns for
agentic software work, using official OpenAI, Anthropic, MCP, and repo-backed
sources checked on 2026-07-02. It maps those patterns back to the local
`hy-home.k8s` four-element harness model without redefining active governance.

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
- Source checked: 2026-07-02
- Refresh trigger: provider agent-loop changes, MCP spec/security changes,
  harness catalog changes, validation-loop changes, or research pack structure
  changes.

## Authority Boundary

- **Authoritative for**:
  - Source-attributed definitions and dated reference findings checked on
    2026-07-02.
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
  non-authoritative market scan findings, workspace application requirements,
  and implementation checklist items.
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
model in [harness-catalog.md](../../00.agent-governance/harness-catalog.md):

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
garbage collection when drift appears. Those points reinforce this workspace's
thin-gateway, template-first, validation-backed model.

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

OpenAI's agent improvement loop example adds a meta-loop: collect traces, attach
human/model feedback, turn feedback into evals, and use the evidence to propose
the next harness changes. In this repository, that meta-loop should route actual
changes to canonical owners rather than embedding policy in this reference.

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

### Worktree/subagent/review-loop implications

OpenAI's harness engineering post highlights isolated worktrees, local app
instances, observability, validation, review, and feedback handling as practical
ways to make higher-autonomy agent work reliable. This repository should apply
that pattern conservatively through its existing contracts:

- **Task-by-task commits**: logical units should be committed separately, with
  the task record naming evidence for each unit.
- **Subagent reviews**: delegated work and review should follow
  [subagent-protocol.md](../../00.agent-governance/subagent-protocol.md) and the
  local runtime roster. Subagents must remain scoped to their file ownership and
  tool boundary.
- **Review loops**: agent or human feedback should produce targeted edits,
  repeat validation, and record evidence rather than silently broadening scope.
- **Static validation evidence**: repo-static gates, diff checks, and task
  evidence are required before handoff. They do not prove live operations.
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

This reference does not authorize adding or changing MCP servers. New or
modified tools belong in the provider/runtime adapter, approval-boundary,
security, and task evidence routes named by the harness catalog and
implementation map.

### Non-authoritative market scan

The following findings are non-authoritative market scan material. They may
inform terminology and future investigation, but they do not override official
provider documentation, MCP specifications, or repo-backed contracts.

- Agent-loop terminology in June/July 2026 increasingly separates a single
  agent harness from the higher-level loop that schedules work, assigns agents,
  verifies outputs, writes memory, and chooses the next task.
- Vendor and practitioner material clusters around worktrees, skills,
  connectors or MCP, subagents, durable memory, traces, evals, observability,
  and explicit stop/verify criteria.
- LangChain's harness article reports a common failure pattern: agents build,
  reread their own work, and stop before running meaningful tests. Their
  proposed repair pattern is plan, build, verify, fix, with middleware forcing a
  pre-completion verification pass.
- MLflow market material frames production agents as distributed systems work:
  architecture, runtime governance, observability, security, tracing, evals, and
  drift monitoring matter more than prompt quality alone.
- MCP security researchers outside the official spec ecosystem highlight tool
  poisoning, shadowing, and rug-pull risks where natural-language tool metadata
  or later server updates steer an agent toward exfiltration or unauthorized
  action. Treat these as threat-intel signals, not canonical protocol text.

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
- Keep external tools read-only by default unless the user approves a specific
  external mutation, push, publish, merge, credential change, paid job, or
  third-party resource change.
- Keep market scan findings labeled non-authoritative.
- Keep repo-static, CI/toolchain, and live-runtime evidence lanes separate.

### Implementation checklist

- Update harness model or runtime roster changes in
  [harness-catalog.md](../../00.agent-governance/harness-catalog.md).
- Update source-of-truth routing, validation owners, and evidence locations in
  [harness-implementation-map.md](../../00.agent-governance/harness-implementation-map.md).
- Route subagent dispatch, scope, tool, and mirror changes through
  [subagent-protocol.md](../../00.agent-governance/subagent-protocol.md) and
  the provider agent files.
- Route approval-boundary or external-action changes to
  `docs/00.agent-governance/rules/approval-boundaries.md`.
- Route template or reference-format changes to
  [Templates README](../../99.templates/README.md),
  [reference.template.md](../../99.templates/reference.template.md), and the
  repository quality gate when applicable.
- Route validation-loop or repo-static evidence changes to `scripts/**`,
  `.github/workflows/ci.yml`, Stage 04 task evidence, and the CI/CD QA guide.
- Route new research-pack status and validation evidence to
  [Workspace Harness Research Pack Task](../../04.execution/tasks/2026-07-02-workspace-harness-research-pack.md).
- Route durable progress/memory updates to
  `docs/00.agent-governance/memory/progress.md` when the active task write
  scope includes that file.
- Before handoff, run `git diff --check` and
  `bash scripts/validate-repo-quality-gates.sh .`, then record PASS/FAIL and
  limitations in the task record.

## Sources

Official and primary external sources, checked 2026-07-02:

- [OpenAI: Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/)
- [OpenAI: Unrolling the Codex agent loop](https://openai.com/index/unrolling-the-codex-agent-loop/)
- [OpenAI Cookbook: Build an Agent Improvement Loop with Traces, Evals, and Codex](https://developers.openai.com/cookbook/examples/agents_sdk/agent_improvement_loop)
- [Anthropic: Building Effective AI Agents](https://www.anthropic.com/research/building-effective-agents)
- [Anthropic: Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
- [Model Context Protocol Specification, version 2025-06-18](https://modelcontextprotocol.io/specification/2025-06-18)
- [Model Context Protocol Security Best Practices](https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices)

Repo-backed sources:

- [Local Harness Catalog](../../00.agent-governance/harness-catalog.md)
- [Harness Implementation Map](../../00.agent-governance/harness-implementation-map.md)
- [Subagent Protocol](../../00.agent-governance/subagent-protocol.md)
- [Workspace Governance Baseline Research](./workspace-governance-baseline.md)
- [Workspace Harness Research Pack Spec](../../03.specs/009-workspace-harness-research-pack/spec.md)
- [Workspace Harness Research Pack Plan](../../04.execution/plans/2026-07-02-workspace-harness-research-pack.md)
- [Workspace Harness Research Pack Task](../../04.execution/tasks/2026-07-02-workspace-harness-research-pack.md)

Non-authoritative market scan sources, checked 2026-07-02:

- [Addy Osmani: Loop Engineering](https://addyosmani.com/blog/loop-engineering/)
- [LangChain: Improving Deep Agents with harness engineering](https://www.langchain.com/blog/improving-deep-agents-with-harness-engineering)
- [MLflow: Building Production-Ready AI Agents in 2026](https://mlflow.org/articles/building-production-ready-ai-agents-in-2026/)
- [Invariant Labs: MCP Security Notification: Tool Poisoning Attacks](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks)

## Review and Freshness

- Review cadence: on source change
- Last reviewed: 2026-07-02
- Next review trigger: provider agent-loop changes, MCP spec/security changes,
  harness catalog changes, validation-loop changes, research pack structure
  changes, or repeated drift in task/review/evidence loops.

## Related Documents

- **Parent research README**: [README.md](./README.md)
- **Parent references README**: [90.references README](../README.md)
- **Workspace baseline**: [Workspace Governance Baseline Research](./workspace-governance-baseline.md)
- **Spec**: [Workspace Harness Research Pack Spec](../../03.specs/009-workspace-harness-research-pack/spec.md)
- **Plan**: [Workspace Harness Research Pack Plan](../../04.execution/plans/2026-07-02-workspace-harness-research-pack.md)
- **Task**: [Workspace Harness Research Pack Task](../../04.execution/tasks/2026-07-02-workspace-harness-research-pack.md)
- **Harness catalog**: [Local Harness Catalog](../../00.agent-governance/harness-catalog.md)
- **Implementation map**: [Harness Implementation Map](../../00.agent-governance/harness-implementation-map.md)
- **Subagent protocol**: [Subagent Protocol](../../00.agent-governance/subagent-protocol.md)
- **Reference maintenance runbook**: [Reference Maintenance Runbook](../../05.operations/runbooks/0011-reference-maintenance-runbook.md)
