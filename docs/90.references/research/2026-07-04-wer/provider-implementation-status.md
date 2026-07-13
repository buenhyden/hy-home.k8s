---
title: 'Reference: Provider Harness Implementation Status Research'
type: content/reference
status: draft
owner: platform
updated: 2026-07-04
---

# Reference: Provider Harness Implementation Status Research

## Overview

이 문서는 Claude Code, Codex/OpenAI, Gemini/Google의 harness capability를
official/provider documentation and repo-backed evidence 기준으로 비교한다.
The goal is to help future agents distinguish upstream provider capability from
this repository's current adapter implementation.

This is durable reference material. It summarizes current facts checked on
2026-07-04 and routes follow-up work to canonical owners; it does not redefine
active governance, provider permissions, CI behavior, or live-runtime procedure.

### Purpose

- Provide a dated, source-attributed comparison of provider harness surfaces.
- Distinguish native provider capabilities from this repo's adapter/mirror
  implementation status.
- Preserve the repo's current Claude, Codex, and Gemini differences so future
  work does not assume identical enforcement across providers.
- Name follow-up routes for gaps without turning this reference into policy.

## Reference Type

- Type: durable-concept / external-standard-snapshot
- Source checked: 2026-07-04
- Refresh trigger: Claude Code, Codex, Gemini CLI, Gemini Code Assist
  landscape changes, Google ADK, MCP, provider adapter, or local harness
  catalog changes.

## Authority Boundary

- **Authoritative for**:
  - Source-attributed provider capability snapshot checked on 2026-07-04.
  - Repo-backed summary of current provider adapter implementation status.
  - Checklist-level follow-up routing to canonical repository owners.
- **Not authoritative for**:
  - Active governance policy, provider runtime permission semantics, hook
    enforcement, CI semantics, subagent dispatch procedure, or live operations.
  - Live k3d, ArgoCD, Vault, ESO, Kubernetes, cloud, deployment, or secret
    readiness.
  - New MCP server additions, provider configuration changes, permission
    changes, adapter rewrites, or runtime roster changes.
  - Market-scan conclusions. No market-scan source is used as authority here;
    any future market-scan addition must be labeled non-authoritative.

## Scope

- Covers official/provider capability surfaces for Claude Code, Codex/OpenAI,
  Gemini CLI, Google ADK, and repo-backed adapter status in `hy-home.k8s`.
  Gemini Code Assist remains a freshness trigger, but WER-004 did not recheck
  Code Assist pages.
- Covers settings/instructions, subagents/delegation, hooks/automation,
  skills/extensions, MCP/tooling, sandbox/permissions/approvals, eval or
  feedback-loop support, and local implementation status.
- Excludes changes to Stage 00 governance, provider adapters, hooks, scripts,
  CI workflows, manifests, secrets, or third-party resources.
- Excludes market scan except to state that it is non-authoritative and not
  used for the implementation-status conclusions in this document.

## Definitions / Facts

### Provider capability matrix

| Capability | Claude Code upstream capability | Codex/OpenAI upstream capability | Gemini/Google upstream capability | Current repo implementation status |
| --- | --- | --- | --- | --- |
| Instruction/settings | Native hierarchical Claude settings and context files, including managed, user, project, and local scopes; project settings are designed for team-shared permissions, hooks, and MCP configuration. | Codex reads `~/.codex/config.toml` and trusted project `.codex/config.toml`; project layers can include config, hooks, and rules, and `AGENTS.md` is part of the Codex rules surface. | Gemini CLI repository material documents `GEMINI.md` context files, configuration documentation, built-in tools, MCP support, and non-interactive use. The WER-004 checked source set does not prove every detailed local settings behavior. | Stage 00 uses thin gateway files plus provider baselines: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.codex/CODEX.md`, and `.agents/GEMINI.md`. |
| Subagents/delegation | Native subagents use Markdown/YAML frontmatter in `.claude/agents/` or user/managed/plugin scopes, with tool, model, permission mode, MCP, hook, and memory options. | Native Codex subagent workflows can spawn specialized agents and project-scoped custom TOML agents under `.codex/agents/`; subagents inherit the active sandbox policy. | Google ADK supports multi-agent systems and delegation as an application framework. Gemini CLI repository material exposes automation, custom context, and GitHub-workflow integration, but this check did not verify a Gemini CLI-native equivalent to Claude's subagent permission model or Gemini Code Assist parity. | The repo keeps provider-aligned agents in `.claude/agents/*.md`, `.agents/agents/*.md`, and `.codex/agents/*.toml`; mirror parity is a repo-static validation concern, not proof of identical native enforcement. |
| Hooks/automation | Native hooks can run deterministic shell commands at lifecycle events; exit-code and JSON behavior can block selected actions, permission requests, prompts, Stop, SubagentStop, and compaction events depending on event type. | Native Codex hooks are enabled by default, load from `hooks.json` or config tables, require trust review for non-managed command hooks, and run lifecycle scripts. Codex rules can govern commands outside the sandbox, but the checked docs mark rules experimental. | Gemini CLI repository material documents automation and non-interactive scripts. This repo's `.agents/hooks.json` provides behavioral hook wiring where the runtime honors it; this check did not verify Claude-style native blocking-hook parity in Gemini CLI. | Claude has the strongest repo-backed native permission-gate story through `.claude/settings.json` as summarized by the harness catalog. Codex `.codex/hooks.json` and Gemini `.agents/hooks.json` are context/validation wiring and must not be treated as identical permission gates. |
| Skills/extensions | Claude skills live in enterprise, personal, project, or plugin locations, with `SKILL.md` as the required entrypoint. | Codex skills are available in CLI, IDE extension, and app, use progressive disclosure, and are scanned from `.agents/skills` in repo scopes plus user/admin/system locations. | Gemini CLI supports tools, custom context, MCP integrations, and extensions at the repository/docs level; Google ADK provides a broader framework with tools, graph workflows, multi-agent workflows, integrations, and skills for agents. | Shared skills, workflows, and output styles are owned by `.agents/`; `.claude/**` and `.codex/**` expose provider-native or symlinked views where supported. |
| MCP/tooling | Claude MCP supports local, project, user, plugin, and managed scopes; project-scoped servers are stored in `.mcp.json`; subagents can scope MCP servers to themselves. | Codex supports MCP in CLI and IDE extension, configured in `config.toml` at user or trusted project scope; it supports STDIO and streamable HTTP servers with authentication options. | Gemini CLI repository material lists MCP support for custom integrations; Google ADK exposes MCP/custom tool integration as part of a broader tool ecosystem. | Repo-backed tracked Codex surfaces are `.codex/CODEX.md`, `.codex/hooks.json`, `.codex/agents/*.toml`, `.agents/**`, and governance docs. ECC instructions and baseline concepts reference project-local `.codex/config.toml` as a possible trusted Codex layer, but no tracked `.codex/config.toml` exists in this checkout. New or changed MCP servers require least-privilege review and human approval for mutation-capable external actions. |
| Sandbox/permissions/approvals | Claude settings include permissions, sandbox filesystem/network settings, hook restrictions, and managed policy layers; subagents can use `permissionMode` but inherit parent context constraints. | Codex exposes sandbox modes (`read-only`, `workspace-write`, `danger-full-access`), approval policies (`untrusted`, `on-request`, `never`), network controls, destination policy, rules, and approval reviewers. | The checked Gemini/ADK source set supports tool and workflow construction, but does not prove Claude-style hook blocking or Codex-style sandbox/approval parity for the repo's Gemini mirror. | Repo governance keeps GitOps-first and no-secret boundaries provider-neutral. Enforcement differs: Claude can natively gate more through settings/hooks; Codex uses sandbox/approval/rules plus context/validation hooks; Gemini follows mirrored behavioral contracts in `.agents/**`. |
| Eval/feedback loop support | Claude hooks can run command, prompt, and experimental agent-based checks; Stop/SubagentStop hooks can prevent completion when configured to block. | Codex docs and navigation expose eval/improvement-loop materials; local CLI docs provide hooks, subagents, sandbox/approvals, and MCP surfaces that can support feedback loops. | Google ADK and Gemini Enterprise Agent Platform explicitly support evaluation, trajectories, metrics, simulations, online monitors, and multi-agent architectures. | Repo-static feedback loops are scripts, hooks, CI, task evidence, and progress memory. Static validation does not imply live cluster readiness. |
| Local repo implementation status | Implemented as thin Claude gateway/baseline, `.claude/agents/*.md`, `.claude/settings.json`, shared hook scripts, and `.claude/**` skill/workflow/output-style views. | Implemented as `AGENTS.md`, `.codex/CODEX.md`, `.codex/agents/*.toml`, `.codex/hooks.json`, and symlinked `.codex/{skills,workflows,output-styles}` to `.agents/`. | Implemented as `GEMINI.md`, `.agents/GEMINI.md`, `.agents/agents/*.md`, `.agents/hooks.json`, and `.agents/{skills,workflows,output-styles}` as shared SSoT. | The harness catalog records all three provider surfaces as repo/static `Ready` where applicable, while explicitly warning that readiness is not proof of identical runtime behavior or live environment health. |

### Claude implementation status

Claude Code has the broadest native provider surface among the three checked
providers for this repository's existing harness pattern:

- **Settings and instructions**: official Claude settings use managed, user,
  project, and local scopes. Project scope is intended for team-shared settings
  such as permissions, hooks, and MCP servers. Settings precedence gives
  managed policy the highest authority, then command-line, local, project, and
  user layers.
- **Subagents**: official Claude subagents are Markdown files with YAML
  frontmatter. Project subagents can live under `.claude/agents/`; custom
  agents can configure tool access, model, MCP servers, permission mode, hooks,
  and memory where supported by the current schema.
- **Hooks and automation**: official Claude hooks execute deterministic
  commands or model/prompt/agent hooks at lifecycle events. For selected events,
  exit code 2 or structured hook output can block a tool call, permission,
  prompt, stop, subagent stop, or compaction event. Async hooks are explicitly
  unable to block because execution has already continued.
- **Skills/extensions**: official Claude skills use `SKILL.md` under enterprise,
  personal, project, or plugin locations. Skills can include supporting
  templates, examples, references, and scripts.
- **MCP/tooling**: official Claude MCP supports local, project, user, plugin,
  and managed/enterprise surfaces. Project-scoped MCP config is stored in
  `.mcp.json`; subagents can scope MCP servers to themselves.
- **Repo-specific implementation distinction**: this repo's canonical sources
  treat Claude as the only provider with native permission plus event wiring
  through `.claude/settings.json`. That distinction is repo-backed in
  [harness-catalog.md](../../../00.agent-governance/harness-catalog.md),
  [common-governance.md](../../../00.agent-governance/common-governance.md), and
  [providers/claude.md](../../../00.agent-governance/providers/claude.md). This
  reference does not assert that every Claude hook currently blocks every class
  of action; blocking depends on event type and configured hook behavior.

### Codex/OpenAI implementation status

Codex/OpenAI has native CLI/app/IDE configuration, sandbox, approvals, hooks,
rules, MCP, skills, and subagent surfaces, but this repo's Codex adapter should
not be described as a Claude permission-gate clone.

- **Config and project docs**: official Codex config uses
  `~/.codex/config.toml` plus trusted project `.codex/config.toml` layers.
  Project layers can be skipped when a project is untrusted. Codex docs also
  expose `AGENTS.md`, rules, hooks, MCP, skills, and subagents as Codex
  configuration topics.
- **Sandboxing and approvals**: official Codex sandbox modes include
  `read-only`, `workspace-write`, and `danger-full-access`. Approval policies
  include `untrusted`, `on-request`, and `never`; default local work generally
  uses `workspace-write` with `on-request`. Network access in
  `workspace-write` is off unless enabled with
  `sandbox_workspace_write.network_access = true`, and optional network policy
  can constrain allowed destinations when network is enabled.
- **Hooks and rules**: official Codex hooks run lifecycle scripts from
  `hooks.json` or inline config tables and require trust review for
  non-managed command hooks. Rules can control which commands Codex may run
  outside the sandbox, but official docs mark rules as experimental.
- **Subagents and skills**: official Codex subagent workflows are enabled by
  default in current releases, spawn only when explicitly asked, and can use
  project custom agents under `.codex/agents/`. Codex skills use progressive
  disclosure, load `SKILL.md` only when selected, and can be discovered from
  `.agents/skills` repository scopes.
- **MCP/tooling**: official Codex MCP supports CLI and IDE extension use,
  configured in `config.toml` at user or trusted project scope. MCP servers can
  be STDIO or streamable HTTP, with auth support described by the Codex MCP
  docs.
- **Repo-specific implementation distinction**: this repo uses
  [AGENTS.md](../../../../AGENTS.md), [.codex/CODEX.md](../../../../.codex/CODEX.md),
  [.codex/hooks.json](../../../../.codex/hooks.json), and
  `.codex/agents/*.toml` as Codex runtime surfaces. The repo sources repeatedly
  state that `.codex/hooks.json` is context/validation wiring, not a
  Claude-style permission gate. Codex must still run explicit validation
  commands before handoff.

### Gemini/Google implementation status

Gemini/Google needs separate readings: Gemini CLI is the terminal provider
surface closest to this repository's mirror, Google ADK is a broader
framework/platform for building, evaluating, and deploying agents, and Gemini
Code Assist remains a freshness trigger even though WER-004 did not recheck
Code Assist agent-mode pages.

- **Gemini CLI context and tooling**: the Gemini CLI repository describes an
  open-source terminal AI agent with built-in tools for Google Search grounding,
  file operations, shell commands, web fetching, MCP support, extensions,
  non-interactive scripting, checkpointing, and custom `GEMINI.md` context
  files. The WER-004 required source set did not require proving every detailed
  settings or sandbox option.
- **Gemini CLI MCP/tooling**: the repository and docs tree establish MCP and
  extension support as upstream Gemini CLI capabilities. Least privilege still
  matters locally, but this reference does not infer active MCP servers or
  Gemini-native permission gates from upstream support.
- **Google ADK and eval platform**: Google ADK is an open-source framework for
  building, debugging, deploying, and evaluating AI agents. Google Cloud docs
  describe multi-agent systems, tools, built-in and partner evaluation tooling,
  trajectory testing, and deployment through Runtime, Cloud Run, or GKE. The
  ADK site also presents graph workflows, multi-agent workflows, agent runtime,
  observability, evaluation, safety/security, custom tools, MCP tools, and
  skills for agents.
- **Gemini Code Assist boundary**: Gemini Code Assist is included in the
  refresh trigger because it can affect the provider landscape, but the
  WER-004 source group supplied for this refresh did not include Code Assist
  agent-mode pages. This document therefore makes no fresh claim that Code
  Assist behavior equals Gemini CLI, Claude Code, Codex, or this repo's
  `.agents/**` adapter.
- **Repo-specific implementation distinction**: this repo uses
  [GEMINI.md](../../../../GEMINI.md), [.agents/GEMINI.md](../../../../.agents/GEMINI.md),
  [.agents/hooks.json](../../../../.agents/hooks.json), and `.agents/**` as the
  Gemini/Antigravity shared surface. The repo says Gemini operates under
  equivalent behavioral contracts, while also stating that `.agents/hooks.json`
  is not a Claude-style permission gate. Do not overclaim native permission
  parity based on `.agents` mirrors.

### Common environment and rule system

This repo builds shared provider behavior through the Stage 00 canonical
adapter model rather than by copying the same policy into every provider file.

- **Canonical core**: `docs/00.agent-governance/rules/**`,
  [harness-catalog.md](../../../00.agent-governance/harness-catalog.md),
  [common-governance.md](../../../00.agent-governance/common-governance.md), and
  [subagent-protocol.md](../../../00.agent-governance/subagent-protocol.md) own
  durable governance concepts, runtime roster, mirror rules, subagent
  boundaries, model-tier routing, and evidence lanes.
- **Provider adapters**: root gateway files and provider baselines route each
  runtime into the shared model. `AGENTS.md` and `.codex/CODEX.md` are the
  Codex path; `CLAUDE.md` and `.claude/**` are the Claude path; `GEMINI.md` and
  `.agents/**` are the Gemini path.
- **Shared asset SSoT**: `.agents/{skills,workflows,output-styles}/` is the
  shared source of truth. Provider views expose those assets through native or
  symlinked adapter surfaces.
- **Templates and scripts**: docs-stage routing is owned by
  `docs/99.templates/**` and Stage 00 documentation rules. Hook scripts live
  under `docs/00.agent-governance/hooks/*.sh`; validation gates live in
  `scripts/*.sh` and CI.
- **Validation gates**: repo-static validation is the default handoff evidence.
  `scripts/validate-repo-quality-gates.sh .` checks documentation structure,
  template routing, mirror contracts, hook-boundary clarity, sensitive-data
  boundaries, and other repository-wide governance conditions.

### Upstream capability versus repo implementation status

- Claude upstream supports native settings, hooks, subagents, skills, and MCP;
  this repo implements Claude through the thin gateway, `.claude/settings.json`,
  `.claude/agents/*.md`, shared hook scripts, and Stage 00 governance.
- Codex upstream supports CLI/app/IDE configuration, sandboxing, approvals,
  MCP, hooks, rules, skills, and subagents; this repo implements Codex through
  `AGENTS.md`, `.codex/CODEX.md`, `.codex/hooks.json`,
  `.codex/agents/*.toml`, shared `.agents/**` assets, and explicit validation.
- Gemini/Google upstream includes Gemini CLI terminal-agent capabilities and
  ADK application-framework capabilities; this repo implements the Gemini path
  through `GEMINI.md`, `.agents/GEMINI.md`, `.agents/agents/*.md`,
  `.agents/hooks.json`, shared `.agents/**` assets, and repo-static parity
  checks.
- Provider upstream features are not automatically active in this repository.
  A feature is local implementation only when an allowed repo surface, adapter,
  rule, script, template, task record, or managed runtime configuration owns it
  and its evidence lane is explicit.

### Non-authoritative market scan

The following scan is non-authoritative. It is derived from the official or
primary provider/source set checked on 2026-07-04 plus repo-backed evidence,
and it must not override canonical provider docs, MCP specifications, or Stage
00 governance.

- The three provider families use similar nouns but different mechanics:
  Claude emphasizes native settings/hook decision control, Codex emphasizes
  sandbox/approval/rule plus hook/subagent/skill configuration, and Gemini is
  split between Gemini CLI terminal-agent capabilities and ADK framework
  capabilities.
- A common agent environment now needs persistent instruction files, scoped
  tool/MCP access, reusable skills or commands, a reviewable permission model,
  subagent or multi-agent routing, and deterministic evidence capture.
- MCP is the shared integration layer across Claude, Codex, and Gemini, but it
  raises shared risks around tool metadata trust, user consent, SSRF, local
  server compromise, token audience separation, and scope minimization.
- Provider parity should be measured by local evidence lanes rather than
  vocabulary. In this repo, parity means each provider can route through the
  same Stage 00 contracts, shared `.agents/**` assets, and validation gates
  while preserving its native enforcement limitations.
- The implementation gap to watch is not missing terminology; it is accidental
  overclaiming that an upstream product/framework feature is active in this
  checkout without a tracked adapter, managed config, script, task record, or
  validation result.

### Shared MCP/tooling considerations

Official/provider sources support MCP and external tools across all three
families, but the safe local rule remains conservative:

- **Trust**: MCP server instructions, tool descriptions, schemas, and transport
  configuration can affect model behavior. Treat new or changed MCP servers as
  trust-boundary changes unless they are already repo-approved and scoped.
- **Least privilege**: start from read-only discovery where possible. Use
  include/exclude tool filters, per-tool approvals, sandbox constraints, scoped
  domains, and credential minimization when a provider supports them.
- **Source verification**: official/provider docs and repo-backed config
  outrank market scan. If market material is later added, label it
  non-authoritative and do not let it override official docs or canonical repo
  owners.
- **Approval boundaries**: networked tools are read-only by default for
  research. Posting, publishing, pushing, merging, opening paid jobs, changing
  third-party resources, or modifying credentials requires explicit human
  approval.
- **Credential handling**: store references to environment variables or managed
  credentials, not secret values. Never record Vault KV values, API tokens, or
  private runtime database contents in this reference.

### Current gaps and uncertainty

- Gemini CLI native hook/permission parity with Claude Code was not verified
  from the required official sources. Repo docs explicitly frame Gemini hooks
  as behavioral wiring, not a Claude permission-gate equivalent.
- Gemini Code Assist agent-mode parity was not rechecked because the WER-004
  required source group did not include Code Assist agent-mode pages; it remains
  a freshness trigger, not an asserted local implementation source.
- Codex rules are present in official docs but marked experimental; repo-local
  `.codex/hooks.json` remains context/validation wiring and does not replace
  explicit validation or human approval boundaries.
- Codex MCP configuration is an upstream/project-layer capability, but this
  checkout does not track `.codex/config.toml`; do not infer enabled Codex MCP
  servers from ECC baseline text alone.
- Claude Code has native settings/hooks/subagents/skills/MCP surfaces, but
  exact blocking behavior still depends on current hook event semantics,
  permission mode, managed policy, and project/user configuration.
- Google ADK capabilities are framework/platform capabilities, not evidence
  that the local `.agents` Gemini mirror implements those features.
- The repo's `Ready` status in the harness catalog means repo/static surface
  readiness. It is not proof of live cluster readiness, provider runtime
  availability, CI success in the current session, or identical enforcement
  across Claude, Codex, and Gemini.
- This document does not install, configure, test, or mutate external provider
  tools. It records a dated source snapshot only.

### Workspace Implementation Routing Checklist

This checklist is a descriptive routing map for future changes. It does not
define provider runtime policy or grant permission to mutate external systems.

- Runtime roster, model tier, adapter readiness, and provider-surface changes
  are owned by
  [harness-catalog.md](../../../00.agent-governance/harness-catalog.md) and the
  relevant provider baseline.
- Subagent dispatch, file ownership, tool scope, and mirror-contract changes
  are owned by
  [subagent-protocol.md](../../../00.agent-governance/subagent-protocol.md) and
  provider agent files in the same logical unit.
- Shared rule, approval-boundary, and no-live-mutation changes are owned by
  `docs/00.agent-governance/rules/**`; this reference only points to that
  owner.
- Shared skills, workflows, and output-style changes are owned by `.agents/**`,
  with `.claude/**` and `.codex/**` adapter views aligned by the relevant
  provider owners.
- Hook script or provider hook wiring changes are owned by
  `docs/00.agent-governance/hooks/*.sh`, `.claude/settings.json`,
  `.codex/hooks.json`, `.agents/hooks.json`, and their validation evidence.
- Template and documentation-routing changes are owned by
  [docs/99.templates/README.md](../../../99.templates/README.md),
  [reference.template.md](../../../99.templates/templates/common/reference.template.md),
  and Stage 00 documentation routing rules.
- MCP additions or mutations require an explicit task/plan and human approval
  when the change can mutate external resources, credentials, or third-party
  state; the active approval boundary is owned by Stage 00 rules.
- Validation evidence is recorded in
  [the research pack task](../../../04.execution/tasks/2026-07-04-workspace-engineering-research-pack.md);
  `docs/00.agent-governance/memory/progress.md` is used only when the current
  task write scope includes it.

## Sources

Official/provider sources checked on 2026-07-04:

OpenAI/Codex:

- Codex documentation home: <https://developers.openai.com/codex/>
- Codex CLI: <https://developers.openai.com/codex/cli/>
- Codex config reference: <https://developers.openai.com/codex/config-reference/>
- Codex agent approvals and security: <https://developers.openai.com/codex/agent-approvals-security/>
- Codex sandboxing: <https://developers.openai.com/codex/concepts/sandboxing/>
- Codex MCP: <https://developers.openai.com/codex/mcp/>
- Codex subagents: <https://developers.openai.com/codex/subagents/>
- Codex hooks: <https://developers.openai.com/codex/hooks/>
- Codex skills: <https://developers.openai.com/codex/skills/>
- Codex rules: <https://developers.openai.com/codex/rules/>
- OpenAI harness engineering article: <https://openai.com/index/harness-engineering/>
- OpenAI Codex agent-loop article: <https://openai.com/index/unrolling-the-codex-agent-loop/>

Anthropic Claude Code:

- Claude Code settings: <https://code.claude.com/docs/en/settings>
- Claude Code hooks: <https://code.claude.com/docs/en/hooks>
- Claude Code subagents: <https://code.claude.com/docs/en/sub-agents>
- Claude Code skills: <https://code.claude.com/docs/en/skills>
- Claude Code MCP: <https://code.claude.com/docs/en/mcp>

Google/Gemini/ADK:

- Gemini CLI repository: <https://github.com/google-gemini/gemini-cli>
- Gemini CLI docs tree: <https://github.com/google-gemini/gemini-cli/tree/main/docs>
- Google Cloud ADK page: <https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/adk>
- ADK site: <https://adk.dev/>

MCP:

- Model Context Protocol Specification, version 2025-06-18: <https://modelcontextprotocol.io/specification/2025-06-18>
- Model Context Protocol Security Best Practices: <https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices>

Repo sources checked on 2026-07-04:

- [Local Harness Catalog](../../../00.agent-governance/harness-catalog.md)
- [Common Governance & Mappings](../../../00.agent-governance/common-governance.md)
- [Subagent Protocol](../../../00.agent-governance/subagent-protocol.md)
- [Claude Provider Notes](../../../00.agent-governance/providers/claude.md)
- [Codex Provider Notes](../../../00.agent-governance/providers/codex.md)
- [Gemini Provider Notes](../../../00.agent-governance/providers/gemini.md)
- [Codex Runtime Baseline](../../../../.codex/CODEX.md)
- [Gemini Runtime Baseline](../../../../.agents/GEMINI.md)
- [Codex Hooks](../../../../.codex/hooks.json)
- [Gemini/Agents Hooks](../../../../.agents/hooks.json)
- [Reference Template](../../../99.templates/templates/common/reference.template.md)
- [Research README](../README.md)
- [Workspace Engineering Research Pack Task](../../../04.execution/tasks/2026-07-04-workspace-engineering-research-pack.md)

Market scan:

- None used as authority for this document. Future market-scan additions must
  be labeled non-authoritative.

## Review and Freshness

- Review cadence: on source change
- Last reviewed: 2026-07-04
- Next review trigger: Claude Code, Codex, Gemini CLI, Gemini Code Assist
  landscape changes, Google ADK, MCP, provider adapter, provider changelog,
  local harness catalog, subagent protocol, hook wiring, or shared
  `.agents/**` changes.

## Related Documents

- **Parent research README**: [README.md](../README.md)
- **Workspace baseline**: [Workspace Governance Baseline Research](workspace-governance-baseline.md)
- **Harness/loop reference**: [Harness and Loop Engineering Research](harness-and-loop-engineering.md)
- **Spec**: [Workspace Engineering Research Pack Spec](../../../03.specs/017-workspace-engineering-research-pack/spec.md)
- **Plan**: [Workspace Engineering Research Pack Plan](../../../04.execution/plans/2026-07-04-workspace-engineering-research-pack.md)
- **Task**: [Workspace Engineering Research Pack Task](../../../04.execution/tasks/2026-07-04-workspace-engineering-research-pack.md)
- **Harness catalog**: [Local Harness Catalog](../../../00.agent-governance/harness-catalog.md)
- **Common governance**: [Common Governance & Mappings](../../../00.agent-governance/common-governance.md)
- **Subagent protocol**: [Subagent Protocol](../../../00.agent-governance/subagent-protocol.md)
- **Reference maintenance runbook**: [Reference Maintenance Runbook](../../../05.operations/runbooks/0011-reference-maintenance-runbook.md)
