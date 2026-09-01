---
title: 'Reference: Provider Implementation Status'
version: "1.0"
type: content/reference
layer: "90.references"
status: active
owner: platform
updated: 2026-08-31
artifact_id: "RES-0001-m0003"
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
[workspace governance](m0001-workspace-governance-and-common-agent-environment.md).

## Definitions / Facts

### Evidence vocabulary

| Status       | Meaning in this reference                                                                                                              |
| ------------ | -------------------------------------------------------------------------------------------------------------------------------------- |
| `Verified`   | A dated official source supports the bounded product claim, or the named tracked file directly supports a static implementation claim. |
| `Partial`    | The source/file supports only part of the requested behavior; the missing dimension is named.                                          |
| `Unverified` | A local claim needs inspection or no adequate source exists.                                                                           |
| `DEFER`      | The claim requires unauthorized/unavailable authenticated, provider-runtime, hosted, remote, credential-bearing, or live evidence.     |

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
[SRC-WERPC-004](m0012-source-coverage.md#source-register) is the
source of these bounded claims.

The repository's root `CLAUDE.md` imports the bootstrap, the Claude provider
note, `.claude/CLAUDE.md`, and `RTK.md`. It deliberately does **not** import
`AGENTS.md`: [Claude provider notes](../../../00.agent-governance/providers/claude.md)
forbid that import because `AGENTS.md` is the GPT/Codex provider shim, so shared
governance reaches Claude through the bootstrap import rather than through an
`AGENTS.md` bridge. This is a **static configuration fact** and is the local
choice among the options the product documents; whether a given Claude Code
session loaded it is `DEFER`. Checked 2026-08-10.

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

| Surface               | Claude Code: official / checked product claim                                                                                        | Codex: official / checked product claim                                                                                            | This workspace declaration                                                                                                                            | Claim status and limitation                                                                                                       |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| Instruction discovery | `CLAUDE.md`/`.claude/CLAUDE.md`, hierarchy and rules; `AGENTS.md` needs import/symlink bridge.                                       | Global/project `AGENTS.md` chain; closer project guidance comes later.                                                             | Root `CLAUDE.md` imports bootstrap/provider note, never `AGENTS.md`; root `AGENTS.md` routes Codex.                                                   | Product claims `Verified`; actual discovery for either client `DEFER`.                                                            |
| Configuration         | `settings.json` has layered settings/permission configuration.                                                                       | `config.toml` layers set durable session preferences and feature/config values.                                                    | `.claude/settings.json` is tracked. No project `.codex/config.toml` is tracked; `.codex/CODEX.md` is a local baseline, not a Codex config file.       | Claude static settings `Verified`; Codex project-config absence `Verified`; effective parse/precedence for either client `DEFER`. |
| Hooks                 | Official hooks run at named lifecycle/tool events and can enforce actions; settings/hook delivery must be trusted/active at runtime. | Official hooks are discovered from hook/config layers, require trust for non-managed command hooks, and run at documented events.  | Both folders point at shared lifecycle scripts; Codex file is not a Claude permission equivalent.                                                     | Static wiring `Verified`; trust, delivery, exit semantics, and effect `DEFER`.                                                    |
| Subagents             | Custom subagents are configured in the Claude Code native surface with scoped instructions/tools.                                    | Built-in/custom agents; project TOML agents and inherited sandbox/approval behavior are documented.                                | Twelve Claude Markdown and twelve Codex TOML role adapters, parity checked statically.                                                                | Adapters `Verified`; native loading/spawn/runtime tool set `DEFER`.                                                               |
| MCP                   | Claude Code can configure MCP servers and uses scopes/configuration; remote auth is separate.                                        | MCP is configured through Codex configuration/CLI and adds external tool context.                                                  | Provider notes name an intended baseline; no tracked Codex project configuration, credential-bearing source, or connection observation was inspected. | Product capability `Verified`; local Codex configuration/connection/auth/tool execution `DEFER`.                                  |
| Sandbox / approval    | Permission modes, allow/deny rules, managed settings, and tool prompts are documented.                                               | `sandbox_mode` and `approval_policy` are distinct controls; `workspace-write` and `on-request` are documented lower-risk defaults. | Claude allow/deny list; Codex provider note requires sandbox/escalation boundaries.                                                                   | Claude static policy `Verified`; Codex runtime mode in an actual client `DEFER`.                                                  |
| Memory                | `CLAUDE.md` plus auto memory; auto memory is context, not enforcement.                                                               | Official manual documents memories and project instructions; workspace must not turn provider-local memory into authority.         | Four-class memory contract and shared progress ledger; provider memory is auxiliary.                                                                  | Local contract `Verified`; actual provider memory discovery/retention `DEFER`.                                                    |
| Model                 | CLI/settings support session model selection; availability/authentication are environment dependent.                                 | Model and reasoning values are configurable; product model availability/selection is account/client dependent.                     | Shared model policy and role-fitness contract explicitly leave runtime mappings `DEFER`.                                                              | Surface `Verified`; resolved value and fitness evidence `DEFER`.                                                                  |
| Runtime/auth          | Claude Code documents authentication routes and runtime requirements.                                                                | Codex documents auth/config/sessions and client/cloud distinctions.                                                                | No token, account, or local runtime state was read.                                                                                                   | `DEFER`; no inference from tracked files.                                                                                         |

### Static configuration, native discovery, and runtime evidence

The required separation is operational, not semantic hair-splitting:

| Evidence layer        | What it can establish                                                                                                | What it cannot establish                                                                                   | Current WERPC-002 result                                                                  |
| --------------------- | -------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| Static configuration  | A tracked file, adapter, hook declaration, command boundary, or local contract exists at the reviewed commit.        | That a provider parsed, trusted, loaded, executed, or enforced it.                                         | `Verified` for named `.claude/**`, `.codex/**`, Stage 00, and provider-neutral contracts. |
| Native discovery      | A specified client/version loaded the declared project instruction/configuration/agent surface.                      | Authentication success, tool permission grant, model resolution, effect of every hook, or live deployment. | `DEFER`; no authorized client instrumentation was collected.                              |
| Authenticated/runtime | The account/client actually authenticated, resolved a model, connected an MCP, and produced scoped runtime evidence. | Broader account entitlement, another provider, or production/live environment health.                      | `DEFER`; credentials and external-state inspection were excluded.                         |

### Comparison gaps and target rules

| Gap                                                     | Why it matters                                                                                      | Target rule                                                                                                                                                                                                                                                                    |
| ------------------------------------------------------- | --------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Treating `AGENTS.md` as native Claude discovery.        | Claude documents `CLAUDE.md` as the reader and `AGENTS.md` as an import bridge.                     | Record that shared governance reaches Claude through the bootstrap import, not through an `AGENTS.md` bridge, and treat the documented bridge as a product option this repository declines; use `/context` or equivalent observed runtime evidence before asserting discovery. |
| Treating `.codex/hooks.json` as a permission gate.      | Codex hooks and sandbox/approval are separate official surfaces.                                    | Keep authorization in sandbox/approval controls and Stage 00 boundaries; hooks may provide context/validation only unless an observed, documented enforcement result says otherwise.                                                                                           |
| Calling adapter parity provider parity.                 | A parallel file inventory says nothing about discovery, schema compatibility, or tool availability. | Validate common semantics statically; report separate per-provider discovery/runtime columns.                                                                                                                                                                                  |
| Hard-coding model names as availability.                | Models and reasoning levels are provider/client/account dependent.                                  | Keep role policy as target/candidate configuration; require an authenticated observed resolution before `Verified`.                                                                                                                                                            |
| Assuming a project Codex configuration exists.          | The official `config.toml` surface does not establish a file in this repository.                    | Record the absence as a workspace gap; do not call `.codex/CODEX.md` configuration.                                                                                                                                                                                            |
| Elevating provider auto memory to repository authority. | Auto memory is contextual and can be stale or private.                                              | Preserve repository-wins resume and promote only reviewed redacted learning to `progress.md` or domain owners.                                                                                                                                                                 |
| Enabling broadly to compensate for unknown behavior.    | Wider tools, network, and permissions expand impact without evidence.                               | Start least privilege, keep writable roots bounded, request explicit escalation, and use read-only research by default.                                                                                                                                                        |

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

### 2026-08-17 full-corpus refresh

This increment is the fifth refresh cycle over this pack, executed under
Spec 058. Unlike the three preceding cycles it re-observed every owner row in
the pack rather than the twelve `Partial` rows, and it assigns each retained
`Partial` or `DEFER` row a blocking class recorded in the
[scope application index](m0013-scope-application-index.md). All observations are
dated **2026-08-17**. No live cluster, hosted CI run, provider runtime,
authenticated execution, or secret value was observed.

#### REQ-WERPC-004 re-observation

**External result:** `changed` (`SRC-WERPC-083`). Claude Code advanced from the
`2.1.220` read-only observation of 2026-07-28 recorded in
`providers/claude.md` to `2.1.233`, dated 2026-08-14. The hooks page now
documents roughly twenty-eight lifecycle events against the six wired locally,
including `Setup`, `SessionEnd`, `UserPromptExpansion`, `StopFailure`,
`PostToolUseFailure`, `PostToolBatch`, `PermissionRequest`, `SubagentStart`,
`TaskCreated`, `InstructionsLoaded`, `ConfigChange`, `PostCompact`, and
`Elicitation`. The `PreToolUse` hard-block mechanism, exit code 2 or
`permissionDecision: deny`, is unchanged.

**Workspace result:** `confirmed`. `.claude/settings.json:78-161` wires exactly
`SessionStart`, `PreToolUse`, `PostToolUse`, `Stop`, `SubagentStop`, and
`PreCompact`. All six remain valid current event names under the current matcher
and command schema, and the twelve `.claude/agents/*.md` files use only core
documented fields. No drift from current syntax was found.

**Status effect:** `no-change` (`CLM-WERPC-011-04`). The row keeps `Verified` on
bounded product surfaces and static adapter, with local discovery and runtime
`DEFER`. A version advance changes the observation, not the evidence class: an
installed version string still does not prove discovery, authentication,
entitlement, hook delivery, or delegated execution.

**Blocking class:** `repo-static` for the adopted-scope question, reachable.
Reopens if workspace hooks or settings must adopt a newly documented event or
subagent field, or if native discovery evidence is separately authorized.

#### REQ-WERPC-005 re-observation

**External result:** `unchanged` (`SRC-WERPC-079`). `AGENTS.md` discovery order,
the 32 KiB `project_doc_max_bytes` default, the TOML subagent required fields
`name`, `description`, and `developer_instructions`, and the example model
identifiers all match the 2026-08-14 baseline exactly. The dedicated Codex hooks
page reconfirms that non-managed command hooks require explicit review and trust
before running, which is not a settings-style permission gate.

**Workspace result:** `confirmed`. `.codex/hooks.json:3-86` wires the same six
events as the Claude tree through shared scripts, and `.codex/CODEX.md:46-47`
still describes those hooks as context and validation wiring rather than a
permission-equivalent gate.

**Status effect:** `no-change` (`CLM-WERPC-011-05`). **Blocking class:**
`repo-static`, reachable. Reopens on a Codex change to discovery order, the TOML
agent schema, or hook trust semantics.

#### Out-of-scope provider observations

Changelog entries `2.1.232` and `2.1.233` record that `subagent_type: "fork"` is
on by default, nested subagent spawn depth rose to three, a `DirectoryAdded`
hook was added, `SessionStart` reports `source: "fork"`, GitLab token families
gained secret redaction, and an opt-in Bash-tool memory cgroup control was
added. None of these bear on the two owner rows above and none is adopted here.

### 2026-08-20 full-corpus reverification

This increment consumes the reviewed provider/common report and its empty
source/claim allocation slice. It separates published product contracts,
tracked configuration, native discovery, and authenticated execution; no
provider client, account, credential, connected MCP, or live tool was inspected.

#### REQ-WERPC-004 Claude implementation status

- **External/workspace result:** `changed` / `confirmed`, using the existing
  `SRC-WERPC-004..008` and `SRC-WERPC-083` source boundaries and workspace
  selector
  `docs/90.references/research/0001-workspace-engineering/m0003-provider-implementation-status.md#claude-baseline`.
- **As-Is:** current Anthropic pages continue to document `CLAUDE.md` context
  and memory, layered settings and permissions, lifecycle hooks, custom
  subagents with tool/MCP/model/context controls, and MCP configuration. The
  changelog observed on 2026-08-20 advances through `2.1.237`. At the baseline
  commit the worktree contains `.claude/settings.json`, twelve tracked Claude
  agent adapters, and six configured hook event keys.
- **Gap / Target:** no authorized evidence establishes the installed Claude
  version, trusted settings, native agent discovery, hook delivery,
  authentication, entitlement, granted permissions, memory behavior, resolved
  model, MCP connectivity, or delegated execution. Retain the verified static
  inventory and require a separately authorized, versioned, non-secret runtime
  observation before making an operational claim.
- **Evidence depth / rejected inference:** current official public
  documentation plus repository-static selectors. A published release or a
  syntactically present adapter cannot prove installation, discovery, trust,
  authentication, permission enforcement, or execution.
- **Disposition / retained boundary:** `Verified` for the bounded product
  surfaces and static configuration; provider-native and authenticated/runtime
  behavior remains `DEFER` under blocking class `repo-static`.
- **Owner / safe follow-up / trigger:** Stage 00 Claude provider governance.
  Maintain the static inventory; reopen on a material settings, permission,
  hook, subagent, MCP, memory, model/context, changelog, or `.claude/` change,
  and run a runtime canary only after separate authorization.

#### REQ-WERPC-005 Codex implementation status

- **External/workspace result:** `unchanged` / `confirmed`, using existing
  `SRC-WERPC-009..013` and `SRC-WERPC-068` boundaries and workspace selector
  `docs/90.references/research/0001-workspace-engineering/m0003-provider-implementation-status.md#codex-baseline`.
- **As-Is:** current OpenAI pages continue to document the AGENTS instruction
  chain, layered configuration, custom subagents, sandbox and approval
  controls, hooks, memories, and model selection. The baseline worktree
  contains `AGENTS.md`, `.codex/CODEX.md`, `.codex/hooks.json`, and twelve
  `.codex/agents/` TOML adapters, but no tracked `.codex/config.toml`. The
  registered MCP URL was attempted during this cycle but the retrieval path
  failed, so no new current MCP-specific claim is adopted.
- **Gap / Target:** static files do not establish project-layer parsing or
  trust, native agent discovery, hook execution, sandbox/approval enforcement,
  authentication, entitlement, memory behavior, resolved models, MCP
  connection, or tool execution. Preserve configuration and runtime as separate
  evidence layers and treat the missing project config as a workspace gap, not
  a runtime failure.
- **Evidence depth / rejected inference:** current official public contracts
  for the reachable surfaces plus repository-static selectors; the MCP
  re-fetch limitation is explicit. Documented features and tracked adapters do
  not prove local discovery, effective controls, connectivity, or execution.
- **Disposition / retained boundary:** `Verified` for the bounded reachable
  product contracts and static inventory; provider-native and
  authenticated/runtime behavior remains `DEFER` under blocking class
  `repo-static`.
- **Owner / safe follow-up / trigger:** Stage 00 Codex provider governance.
  Reinspect the tracked project layer and registered official pages on a
  material AGENTS, config, subagent, sandbox/approval, hook, memory, model, MCP,
  or `.codex/` change; use a versioned non-secret runtime canary only after
  explicit authorization.

### 2026-08-23 provider-contract and authority-convergence increment

This gap-only increment records current official provider contracts without
promoting any repository declaration to runtime evidence. It also applies the
terminal Spec 0054 authority interpretation additively: Claude and Codex are the
current provider projections, while the provider-neutral repository core owns
shared scope, permission, evidence, validation, and memory rules. Older
four-surface inventory statements remain dated static observations; they do not
make Gemini or Antigravity a current terminal provider. No adapter or document
topology migration is performed by this research increment.

#### Codex documented capability delta

- The official [configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference)
  and [subagent guide](https://learn.chatgpt.com/docs/agent-configuration/subagents)
  now describe `features.multi_agent` as stable and enabled by default. This
  corrects an experimental-only product characterization; it does not prove
  that this workspace discovered a project agent, spawned a child, or resolved
  its model and tools.
- The official [hooks reference](https://learn.chatgpt.com/docs/hooks) documents
  lifecycle hooks, including stop, subagent-stop, and compaction boundaries.
  Hooks remain distinct from sandbox and approval authority. A tracked hook
  declaration therefore proves neither trust, delivery, ordering, nor effect.
- The official [AGENTS.md guide](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
  documents the global-to-project discovery chain and nearer-directory
  precedence. The subagent guide also documents inheritance of the parent
  sandbox and approval policy; an action that requires approval the child
  cannot obtain fails instead of silently widening authority.

#### Claude documented capability delta

The official [hooks guide](https://code.claude.com/docs/en/hooks-guide)
distinguishes deterministic command hooks, suitable for repeatable production
controls, from experimental agent hooks whose model-mediated behavior is not a
deterministic gate. The official
[subagent guide](https://code.claude.com/docs/en/subagents) documents separate
subagent context and configurable isolation. These contracts support bounded
delegation, but do not prove that this workspace loaded an adapter, delivered a
hook, created an isolated worktree, or enforced a permission.

#### Evidence disposition

- **Verified:** the bounded official capability statements above and the
  terminal authority rule that shared semantics belong to the provider-neutral
  core with Claude/Codex projections.
- **Partial:** repository-static adapters and hook declarations can be checked,
  but equivalence across the two provider runtimes is not established.
- **DEFER:** native discovery, hook delivery and effect, child execution and
  isolation, approval outcomes, authentication, entitlement, MCP connection,
  memory behavior, and resolved model remain provider-runtime observations.
  They require a separately authorized, versioned, non-secret canary.

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

- [Harness and loop engineering](m0002-harness-and-loop-engineering.md)
- [Workspace governance and common environment](m0001-workspace-governance-and-common-agent-environment.md)
- [Source ledger](m0012-source-coverage.md)
- [Claude provider notes](../../../00.agent-governance/providers/claude.md)
- [Codex provider notes](../../../00.agent-governance/providers/codex.md)
