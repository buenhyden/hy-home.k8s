---
title: 'Reference: Provider Implementation Status'
type: content/reference
status: active
owner: platform
updated: 2026-08-08
---

# Reference: Provider Implementation Status

## Overview

This reference compares the official Claude Code and Codex surfaces against the
tracked adapters in this worktree. It deliberately distinguishes three evidence
depths: a checked product capability, a repository-static declaration, and an
authenticated/runtime observation. A row does not become a runtime fact because
configuration with a familiar filename exists.

## Reference Type

Official-provider source review and repository-static status matrix, observed on
2026-08-08.

## Authority Boundary

Anthropic and OpenAI own their products' instructions, settings, hooks,
subagents, MCP, model, sandbox, approval, and memory semantics. Stage 00 owns
this repository's policy, task gates, and evidence vocabulary. Credentials,
account entitlements, actual configuration parse/discovery, hook trust/delivery,
model availability, and live execution are outside this research scope and are
`DEFER` unless separately observed.

## Scope

This owner covers REQ-WERPC-004 (Claude) and REQ-WERPC-005 (Codex), including
instruction discovery, configuration, hooks, subagents, MCP, sandbox/approval,
memory, model, and runtime boundaries. Common control-plane findings route to
[workspace governance](workspace-governance-and-common-agent-environment.md).

## Definitions / Facts

### Evidence vocabulary

| Status | Meaning in this reference |
| --- | --- |
| `Verified` | A dated official source supports the bounded product claim, or the named tracked file directly supports a static implementation claim. |
| `Partial` | The source/file supports only part of the requested behavior; the missing dimension is named. |
| `Unverified` | A local claim needs inspection or no adequate source exists. |
| `DEFER` | The claim requires unauthorized/unavailable authenticated, provider-runtime, hosted, remote, credential-bearing, or live evidence. |

“Verified” never crosses an evidence boundary: a verified official feature is
not proof that the local adapter is used; a verified tracked adapter is not
proof that a provider discovered or enforced it.

### Claude baseline

Anthropic's official memory documentation says Claude Code reads `CLAUDE.md`
files and states explicitly that it does not read `AGENTS.md` directly; a
`CLAUDE.md` import is the documented bridge. It distinguishes user-authored
instructions from auto memory and says both are context rather than enforced
configuration; it identifies a `PreToolUse` hook as the hard-blocking mechanism.
The same official docs describe hierarchical/nested instruction loading,
`.claude/rules/` path-scoped instructions, and project-local configuration.
[SRC-WERPC-004](source-coverage-and-migration-ledger.md#source-register) is the
source of these bounded claims.

The repository's root `CLAUDE.md` imports `AGENTS.md`, then imports the
bootstrap, Claude provider note, `.claude/CLAUDE.md`, and `RTK.md`. This is a
**static configuration fact** consistent with the documented bridge; whether a
given Claude Code session loaded it is `DEFER`.

### Codex baseline

The locally supplied official Codex manual says Codex constructs an instruction
chain from global and project `AGENTS.md`/`AGENTS.override.md`, root-to-current
directory, with closer instructions later in context. It documents project
`.codex/config.toml`, custom project agents under `.codex/agents/`, hooks from
active configuration layers, MCP configuration, and separate sandbox/approval
controls. These facts are bounded to the official product documentation and are
registered as SRC-WERPC-009–013.

The worktree has `AGENTS.md`, `.codex/CODEX.md`, twelve `.codex/agents/*.toml`,
and `.codex/hooks.json`. Their presence is `Verified` repository-static
configuration. The currently supplied execution environment proves neither
native project discovery nor that these exact hooks ran; that remains `DEFER`.

### Provider surface matrix

| Surface | Claude Code: official / checked product claim | Codex: official / checked product claim | This workspace declaration | Claim status and limitation |
| --- | --- | --- | --- | --- |
| Instruction discovery | `CLAUDE.md`/`.claude/CLAUDE.md`, hierarchy and rules; `AGENTS.md` needs import/symlink bridge. | Global/project `AGENTS.md` chain; closer project guidance comes later. | Root `CLAUDE.md` imports `AGENTS.md`; root `AGENTS.md` routes Codex. | Product claims `Verified`; actual discovery for either client `DEFER`. |
| Configuration | `settings.json` has layered settings/permission configuration. | `config.toml` layers set durable session preferences and feature/config values. | `.claude/settings.json` is tracked. No project `.codex/config.toml` is tracked; `.codex/CODEX.md` is a local baseline, not a Codex config file. | Claude static settings `Verified`; Codex project-config absence `Verified`; effective parse/precedence for either client `DEFER`. |
| Hooks | Official hooks run at named lifecycle/tool events and can enforce actions; settings/hook delivery must be trusted/active at runtime. | Official hooks are discovered from hook/config layers, require trust for non-managed command hooks, and run at documented events. | Both folders point at shared lifecycle scripts; Codex file is not a Claude permission equivalent. | Static wiring `Verified`; trust, delivery, exit semantics, and effect `DEFER`. |
| Subagents | Custom subagents are configured in the Claude Code native surface with scoped instructions/tools. | Built-in/custom agents; project TOML agents and inherited sandbox/approval behavior are documented. | Twelve Claude Markdown and twelve Codex TOML role adapters, parity checked statically. | Adapters `Verified`; native loading/spawn/runtime tool set `DEFER`. |
| MCP | Claude Code can configure MCP servers and uses scopes/configuration; remote auth is separate. | MCP is configured through Codex configuration/CLI and adds external tool context. | Provider notes name an intended baseline; no tracked Codex project configuration, credential-bearing source, or connection observation was inspected. | Product capability `Verified`; local Codex configuration/connection/auth/tool execution `DEFER`. |
| Sandbox / approval | Permission modes, allow/deny rules, managed settings, and tool prompts are documented. | `sandbox_mode` and `approval_policy` are distinct controls; `workspace-write` and `on-request` are documented lower-risk defaults. | Claude allow/deny list; Codex provider note requires sandbox/escalation boundaries. | Claude static policy `Verified`; Codex runtime mode in an actual client `DEFER`. |
| Memory | `CLAUDE.md` plus auto memory; auto memory is context, not enforcement. | Official manual documents memories and project instructions; workspace must not turn provider-local memory into authority. | Four-class memory contract and shared progress ledger; provider memory is auxiliary. | Local contract `Verified`; actual provider memory discovery/retention `DEFER`. |
| Model | CLI/settings support session model selection; availability/authentication are environment dependent. | Model and reasoning values are configurable; product model availability/selection is account/client dependent. | Shared model policy and role-fitness contract explicitly leave runtime mappings `DEFER`. | Surface `Verified`; resolved value and fitness evidence `DEFER`. |
| Runtime/auth | Claude Code documents authentication routes and runtime requirements. | Codex documents auth/config/sessions and client/cloud distinctions. | No token, account, or local runtime state was read. | `DEFER`; no inference from tracked files. |

### Static configuration, native discovery, and runtime evidence

The required separation is operational, not semantic hair-splitting:

| Evidence layer | What it can establish | What it cannot establish | Current WERPC-002 result |
| --- | --- | --- | --- |
| Static configuration | A tracked file, adapter, hook declaration, command boundary, or local contract exists at the reviewed commit. | That a provider parsed, trusted, loaded, executed, or enforced it. | `Verified` for named `.claude/**`, `.codex/**`, Stage 00, and provider-neutral contracts. |
| Native discovery | A specified client/version loaded the declared project instruction/configuration/agent surface. | Authentication success, tool permission grant, model resolution, effect of every hook, or live deployment. | `DEFER`; no authorized client instrumentation was collected. |
| Authenticated/runtime | The account/client actually authenticated, resolved a model, connected an MCP, and produced scoped runtime evidence. | Broader account entitlement, another provider, or production/live environment health. | `DEFER`; credentials and external-state inspection were excluded. |

### Comparison gaps and target rules

| Gap | Why it matters | Target rule |
| --- | --- | --- |
| Treating `AGENTS.md` as native Claude discovery. | Claude documents `CLAUDE.md` as the reader and `AGENTS.md` as an import bridge. | Keep the root `CLAUDE.md` import and call it static bridge evidence; use `/context` or equivalent observed runtime evidence before asserting discovery. |
| Treating `.codex/hooks.json` as a permission gate. | Codex hooks and sandbox/approval are separate official surfaces. | Keep authorization in sandbox/approval controls and Stage 00 boundaries; hooks may provide context/validation only unless an observed, documented enforcement result says otherwise. |
| Calling adapter parity provider parity. | A parallel file inventory says nothing about discovery, schema compatibility, or tool availability. | Validate common semantics statically; report separate per-provider discovery/runtime columns. |
| Hard-coding model names as availability. | Models and reasoning levels are provider/client/account dependent. | Keep role policy as target/candidate configuration; require an authenticated observed resolution before `Verified`. |
| Assuming a project Codex configuration exists. | The official `config.toml` surface does not establish a file in this repository. | Record the absence as a workspace gap; do not call `.codex/CODEX.md` configuration. |
| Elevating provider auto memory to repository authority. | Auto memory is contextual and can be stale or private. | Preserve repository-wins resume and promote only reviewed redacted learning to `progress.md` or domain owners. |
| Enabling broadly to compensate for unknown behavior. | Wider tools, network, and permissions expand impact without evidence. | Start least privilege, keep writable roots bounded, request explicit escalation, and use read-only research by default. |

### Workspace Application

The portable control plane should be expressed once in Stage 00: task acceptance,
document routing, authority, evidence vocabulary, recovery, durable memory, and
GitOps security. Provider adapters then translate only these edge capabilities:

1. **Instructions**: Claude consumes the `CLAUDE.md` bridge; Codex consumes
   `AGENTS.md`; neither makes the shared policy a native hard gate by itself.
2. **Enforcement**: use the provider's native permission/sandbox surface where
   present plus repository validators. A hook is not presumed equivalent across
   providers.
3. **Delegation**: give subagents bounded paths and acceptance evidence; avoid
   parallel writes to the same surface. A spawned agent inherits no authority
   that the parent was not granted.
4. **External context**: register each MCP's owner, scope, auth requirement,
   data classification, and approval boundary before enabling it. Do not store
   credentials in the repository or report an installed declaration as a live
   connection.
5. **Memory and models**: retain policy and shared progress in versioned owners;
   label provider-local retention, auth, model resolution, and runtime behavior
   `DEFER` until an approved observation proves the exact claim.

## Sources

- **Anthropic primary sources**: [memory](https://code.claude.com/docs/en/memory),
  [settings](https://code.claude.com/docs/en/settings),
  [hooks](https://code.claude.com/docs/en/hooks),
  [subagents](https://code.claude.com/docs/en/sub-agents), and
  [MCP](https://code.claude.com/docs/en/mcp), each checked 2026-08-08. Their
  ledger rows are SRC-WERPC-004–008.
- **OpenAI primary sources**: the official manual cache was consulted first,
  with the linked official AGENTS, configuration, subagents, hooks, and MCP
  pages recorded as SRC-WERPC-009–013.
- **Workspace evidence**: `CLAUDE.md`, `.claude/CLAUDE.md`,
  `.claude/settings.json`, `AGENTS.md`, `.codex/CODEX.md`, `.codex/hooks.json`,
  `.codex/agents/`, Stage 00 provider notes and contracts, observed 2026-08-08.

## Review and Freshness

Refresh after an official provider release or documentation revision changing
instruction discovery, configuration precedence, hook trust/events, agent
schema, MCP authorization, sandbox/approval, memory, or model behavior; refresh
immediately when local adapters change. The source register keeps the checked
date and scope. Runtime assertions require a separate approved, non-secret
observation and must identify client/version, evidence class, date, and exact
surface.

## Related Documents

- [Harness and loop engineering](harness-and-loop-engineering.md)
- [Workspace governance and common environment](workspace-governance-and-common-agent-environment.md)
- [Source ledger](source-coverage-and-migration-ledger.md)
- [Claude provider notes](../../../00.agent-governance/providers/claude.md)
- [Codex provider notes](../../../00.agent-governance/providers/codex.md)
