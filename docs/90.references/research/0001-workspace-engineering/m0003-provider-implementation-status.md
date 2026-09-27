---
title: "Reference: Provider Implementation Status"
version: "1.1.0"
type: "reference/research"
status: "published"
owner: "platform"
updated: "2026-09-27"
layer: "references"
artifact_id: "RES-0001-m0003"
---

# Reference: Provider Implementation Status

## Overview

This reference compares officially documented Claude Code CLI, IDE, web and Agent SDK with Codex CLI, IDE, cloud and SDK. The current matrix is external product research, not a status audit of tracked adapters. Native features, optional/custom integrations and unknown support are stated separately.

## Reference Type

Direct primary-source external research, observed on 2026-09-27, with conditional follow-up design and retained dated history.

## Authority Boundary

Vendor documentation establishes only its named product, version and surface. It does not establish local installation, account entitlement, discovery, trust, parsing, authorization, execution or effect. Every current workspace result is `not observed in this cycle`. This reference authorizes no provider/configuration change, credential or private-memory inspection, runtime probe, installation or external write. Product claims, source refresh results and document QA are separate evidence axes.

## Scope

Primary owner of U04 and U34, preserving REQ-WERPC-004 and REQ-WERPC-005. Includes instructions/import/precedence, system prompts, skills/plugins/subagents, lifecycle hooks, sandbox/approval/trust, MCP, compaction/resume/memory, models, noninteractive execution, PR review, inline edits, shortcuts, code actions and documentation hooks. Excludes installation, account inspection, local experiment and cross-product support inference.

## Definitions / Facts

### Provider surface comparison

All source cells below refer to [current source observations](m0012-source-coverage.md#current-source-observations), directly read on **2026-09-27**. `Verified` means bounded official support, never local execution. Unknown installed versions and account entitlements remain unknown. Every follow-up workspace result is `not observed in this cycle`.

| Feature / claim | Provider and product surface | Native / external configuration | Support status / version | Official setting or discovery | Permission / limitation | Evidence / read date | Commonizable area | Follow-up question |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Instructions — CLM-WERPC-017-17 | Claude Code local instruction loader | Native conditional fallback | Verified; documented v2.1.277 gate | `AGENTS.md` / `.claude/AGENTS.md` fallback; instruction-family mode | Ancestor Claude-family files suppress default fallback; mode is user/managed, not project/local | SRC-WERPC-004; 2026-09-27 | Shared procedure body | Q-WERPC-022 |
| Imports — CLM-WERPC-017-18 | Claude Code / Codex CLI | Claude native `@` import; Codex own loader/import route | Verified scoped contracts | Claude relative import ≤ four hops; Codex global → root/cwd chain, one file/directory, 32 KiB default | Outside-project Claude import approval; Codex links are not automatic `@` imports | SRC-WERPC-004, 009, 137; 2026-09-27 | Canonical references and provenance | Q-WERPC-022 |
| Built-in prompt — CLM-WERPC-017-19 | Claude CLI / Codex CLI | Native explicit override | Verified; unversioned docs | Claude `--system-prompt` replacement or `--append-system-prompt`; Codex `model_instructions_file` replacement | Repository prose is not built-in system prompt; Codex `instructions` reserved and experimental file key deprecated | SRC-WERPC-237, 049; 2026-09-27 | Goal/rules ownership | Q-WERPC-023 |
| Skills — CLM-WERPC-017-20 | Codex / Claude Code | Native packages; paths vary | Verified; current docs | Codex `.agents/skills/` at documented scopes; Claude `.claude/skills/`, nested/additional/plugin/account scopes | Metadata visibility is not invocation or permission; same names do not merge universally | SRC-WERPC-156, 157, 243; 2026-09-27 | Reviewed skill text and metadata | Q-WERPC-024 |
| Plugins — CLM-WERPC-017-21 | Claude Code plugins / Codex import | Native product packaging or conversion | Verified scope; no cross-product parity | Skills/agents/hooks/MCP packaged in provider namespaces | Plugin installation does not grant tool authority or hook trust | SRC-WERPC-158, 137; 2026-09-27 | Owned procedure body | Q-WERPC-024 |
| Subagents — CLM-WERPC-017-22 | Codex CLI | Native; explicit task authorization | Verified; enabled by documented default | TOML `name`, `description`, `developer_instructions`; delegate when user/AGENTS/skill asks | Parent permissions inherited; noninteractive child cannot obtain fresh approval | SRC-WERPC-011; 2026-09-27 | Role intent and bounded handoff | Q-WERPC-024 |
| Subagents — CLM-WERPC-017-23 | Claude Code | Native Markdown definitions | Verified; FORCE override v2.1.257 | Tools/permissions/MCP/skills/hooks/memory/background/effort/isolation fields | Parent denial is not granted away; worktree isolation is not complete sandbox | SRC-WERPC-007; 2026-09-27 | Responsibilities and acceptance | Q-WERPC-024 |
| Hook coverage — CLM-WERPC-017-24 | Codex local lifecycle hooks | Native command/MCP handlers | Verified; prompt/agent handlers parsed but skipped | Session/tool/permission/subagent/stop/interrupt/compaction events; shell and patch aliases | Hosted WebSearch has no events; `write_stdin` has no second Pre event; specialized tools may opt out | SRC-WERPC-012; 2026-09-27 | Event intent and evidence shape | Q-WERPC-025 |
| Hook trust/effect — CLM-WERPC-017-25 | Codex CLI | Native with explicit reviewed trust | Verified current docs | Trusted project plus exact non-managed definition hash and hook review | Edited definition needs retrust; Pre deny/legacy block/exit 2 blocks; unsupported responses can fail while tool continues; Post cannot undo | SRC-WERPC-012; 2026-09-27 | Negative-case design | Q-WERPC-026 |
| Hook failures — CLM-WERPC-017-26 | Claude CLI / Agent SDK callbacks | Native command/http/MCP/prompt/agent handlers | Verified; exit behavior v2.1.214, malformed JSON v2.1.248 | Event-specific exit/JSON response | PermissionRequest exit 2 ignored without deny JSON; Pre command/http/MCP timeout is nonblocking, SDK callback timeout blocks | SRC-WERPC-006; 2026-09-27 | Explicit failure/effect checks | Q-WERPC-026 |
| Approval and isolation — CLM-WERPC-017-27 | Claude local / Codex local | Native config plus host enforcement | Verified external contracts | Claude managed → CLI → local → project → user with exceptions; Codex trusted project layers and sandbox/approval | Trust, filesystem/network isolation, tool policy and prompting are separate controls | SRC-WERPC-005, 238, 242; 2026-09-27 | Least privilege and evidence lanes | Q-WERPC-023 |
| MCP — CLM-WERPC-017-28 | Claude Code / Codex | Native stdio/HTTP configuration; separate authentication | Verified; protocol revision 2026-07-28 | Product scopes/OAuth/tool policies and Resources | Claude SSE fallback deprecated at documented v2.1.265 gate; negotiated connection/access not established | SRC-WERPC-008, 013, 066, 087; 2026-09-27 | URI/provenance/access contract | Q-WERPC-027 |
| Resume/compaction — CLM-WERPC-017-29 | Claude CLI / Codex CLI and SDK | Native sessions and host recovery | Verified current docs | Claude JSONL resume/fork; Codex context/compaction defaults and SDK threads | Lossy summary and old history do not establish current files or rollback | SRC-WERPC-096, 049, 166; 2026-09-27 | Fresh Git/Task handoff | Q-WERPC-028 |
| Memory — CLM-WERPC-017-30 | Claude Code / Codex local | Native optional recall | Verified documented defaults | Provider-specific defaults and controls; [memory owner](m0011-agent-memory-tiers-and-management.md#memory-authority-and-lifecycle) | Recall, retention and correct application need separate evidence | SRC-WERPC-004, 068, 049; 2026-09-27 | Reviewed durable knowledge | Q-WERPC-028 |
| Model configuration — CLM-WERPC-017-31 | Codex product / Claude Code / APIs | Native, product-specific identifiers | Verified syntax; availability Partial | Product model catalog, role overrides, main/subagent environment layers | [Model owner](m0010-agent-model-routing-and-configuration.md#model-selection-and-escalation) bounds product/API differences | SRC-WERPC-136, 049, 236; 2026-09-27 | Risk/evaluation criteria | Q-WERPC-029 |
| Noninteractive — CLM-WERPC-017-32 | Claude CLI and Agent SDK | Native print mode / embedded binary | Verified; prompt suppression v2.1.259 | `-p`, text/JSON/stream JSON/schema, print-mode turn/budget controls | No prompts means denial, not permission; third-party SDK products need authorized API authentication | SRC-WERPC-237, 163; 2026-09-27 | Acceptance/output contract | Q-WERPC-030 |
| Noninteractive — CLM-WERPC-017-33 | Codex CLI and SDK | Native exec / SDK | Verified current docs | `codex exec`, JSON usage/schema/ephemeral/resume; Node 18+ TS or Python 3.10+ App Server | Read-only exec default; workspace writes explicit; full-auto deprecated; host credentials/budgets and required-MCP failure remain host concerns | SRC-WERPC-167, 166; 2026-09-27 | Redacted evidence and host budgets | Q-WERPC-030 |
| Inline edit — CLM-WERPC-017-34 | Claude VS Code / JetBrains | Native extension/plugin plus CLI | Verified; VS Code 1.94+, per-change context-menu review v2.1.275 | VS Code Alt/Option K selection, Cmd/Ctrl Esc focus, Cmd/Ctrl Shift Esc tab; JetBrains Cmd/Ctrl Esc and Cmd Option K / Alt Ctrl K refs | Bundled VS Code CLI differs from terminal CLI; JetBrains needs separate CLI/plugin; diagnostics tool is not automatic post-edit request | SRC-WERPC-159, 160; 2026-09-27 | Context-selection/review process | Q-WERPC-031 |
| IDE commands — CLM-WERPC-017-35 | Codex VS Code-compatible extension | Native extension; host bindings | Verified docs; installed immutable revision unknown | `chatgpt.addToThread`, `addFileToThread`, `newChat`, sidebar/menu/panel commands | Selection/file commands have no default binding; bindings editable; Xcode/JetBrains are distinct integrations | SRC-WERPC-164, 239, 240; 2026-09-27 | Explicit context and diff acceptance | Q-WERPC-031 |
| Shortcuts/code actions/doc hook — CLM-WERPC-017-36 | Claude CLI / editor / Git / CI | Product shortcuts; custom automation as needed | Verified shortcut surface; universal doc-on-save support Unverified | `~/.claude/keybindings.json` autoreloads CLI bindings; editor uses host bindings | Inline diff/context menu is not typing completion or an LSP quick fix; no universal native documentation-on-save feature established | SRC-WERPC-161, 159, 160, 240; 2026-09-27 | Event-specific outcome/evidence | Q-WERPC-031 |
| Web tasks — CLM-WERPC-017-37 | Claude Code web | Native remote product | Verified current docs | Isolated remote environment/network and session settings | Parallel sessions share usage; GitHub push/PR differs from GitLab/Bitbucket bundle route; SessionStart has time limits | SRC-WERPC-162; 2026-09-27 | Scoped task/diff review | Q-WERPC-032 |
| Cloud tasks — CLM-WERPC-017-38 | Codex cloud | Native repository environment | Verified; GitLab beta bounded | Per-repo dependencies/network/tools and isolated tasks | Cloud default model not locally selectable; API-key CLI/SDK/IDE excludes cloud/GitHub review/Slack | SRC-WERPC-165, 136, 169; 2026-09-27 | Environment and acceptance contract | Q-WERPC-032 |
| PR review — CLM-WERPC-017-39 | Codex CLI / IDE / app | Native review flow | Verified scoped product feature | `/review` base/uncommitted/commit/custom diff; `review_model` or product conversation settings | Prioritized findings do not prove tests, approval or merge; IDE needs Git; fixes use normal permissions. This research does not establish equivalent Claude native GitHub triggers | SRC-WERPC-168; 2026-09-27 | Independent criteria and evidence | Q-WERPC-032 |

### Hooks IDE and SDK boundaries

The earlier categorical “Claude does not read `AGENTS.md`” claim is **Contradicted as current product guidance** by the conditional v2.1.277 loader. Preserve the old dated history; do not infer that this worktree uses fallback, both-family mode or an import. Direct fallback lacks `InstructionsLoaded`, whereas imports/symlinks can emit it. Mode, ancestor exclusions and actual context must be considered together.

The model-precedence discrepancy recorded in older cycles now has a layer-specific explanation: Codex resolves explicit-spawn → agent default → parent, then an agent-file explicit model/effort overrides that result. A file setting only the model preserves resolved effort; an explicit new spawn model without effort uses the model default. The old finite reasoning enumeration no longer describes the current product catalog. Claude normal subagent precedence is invocation → definition → default environment → main conversation, with the documented FORCE environment override and exceptions. These are source reconciliation results, not installed-client observations; see [model routing](m0010-agent-model-routing-and-configuration.md#model-selection-and-escalation).

Four event systems must remain distinct. Git `pre-commit`/`pre-push`/`commit-msg` executes in a Git operation; provider lifecycle hooks receive that product's tool/session event; editor actions and on-save integration depend on the IDE/plugin; CI triggers run a hosted workflow. A provider hook does not automatically intercept all Git commands or save events. A command invoking Git or a documentation generator is custom integration until the exact native product contract establishes otherwise. [CI/CD and QA](m0008-ci-cd-github-actions-and-qa.md) owns Git/CI details.

Hooks require event-specific failure tests. Codex accepts Pre-tool deny, legacy block and exit 2, while `ask`, `approve`, `continue:false`, `stopReason` and `suppressOutput` are unsupported and can leave the tool continuing after hook failure. Claude exit 2 blocks most covered events even with invalid JSON at the documented gate; malformed JSON errors, exit 1 and missing commands are generally nonblocking, and PermissionRequest requires deny JSON rather than exit 2. Timeout behavior differs between command/http/MCP and SDK callbacks. Post-tool evaluation cannot reverse the completed operation. Neither the number of configured events nor a plugin installation establishes trust, delivery, coverage or fail-closed effect.

Choose local CLI when direct host integration is required; IDE when selection, diff review and shortcuts help the human; cloud/web when a reviewed isolated repository environment and remote workflow are appropriate; SDK when the host must own structured I/O, scheduling, budgets or evaluation. Prerequisites include compatible client/plugin/SDK revisions, non-secret authentication metadata, environment/network/tool boundaries, repository state and independent verification. More surfaces add portability and convenience but also settings drift, account limits and failures at product boundaries. No surface was exercised here.

### Provider verification questions

`CLM-WERPC-017-40` points to the [central follow-up question contracts](m0013-scope-application-index.md#follow-up-question-ledger). Candidate selectors are unobserved: `.claude/settings*.json`, `.claude/agents/`, `.claude/skills/`, `.codex/config.toml`, `.codex/hooks.json`, `.codex/agents/`, editor extension manifests, keybinding declarations and SDK call sites. Private configuration, credentials and conversations remain excluded.

- Q-WERPC-021: which exact CLI/IDE/web/cloud/SDK, version and non-secret account capability metadata does a claim concern?
- Q-WERPC-022: which instruction family, ancestor fallback, imports and events prove actual context inclusion, including direct AGENTS fallback without an event?
- Q-WERPC-023: which system-prompt/configuration layers and native sandbox/approval controls are effective, and what separates prose from enforcement?
- Q-WERPC-024: which skills/plugins/subagents are visible, parsed, invoked and permissioned under the exact product schema?
- Q-WERPC-025: which hook definition and reviewed hash/trust state covers each actual tool/event?
- Q-WERPC-026: do synthetic deny, malformed response, missing command and timeout cases block or continue as documented, and propagate failure to the caller?
- Q-WERPC-027: which MCP protocol, scope, authentication and read/write policy is negotiated without inspecting secrets?
- Q-WERPC-028: does resume/compaction/memory preserve acceptance/provenance and re-observe current files, rather than treating stored history as truth?
- Q-WERPC-029: which model/effort layer resolves and what fallback/account limits apply?
- Q-WERPC-030: which noninteractive/SDK output, budget and permission controls work for this exact host/product?
- Q-WERPC-031: which installed editor version implements inline edits, context menus, shortcut bindings, code actions and any documentation hook, and which parts can share a procedure rather than a schema?
- Q-WERPC-032: which cloud/web environment and PR-review trigger has authorized evidence, independent review and usage boundaries?

### Historical observations and corrections — 2026-08-08 to 2026-09-05

All following records preserve their original dates, identities, statuses, evidence boundaries and correction relationships. They are historical provenance, not current workspace results or load instructions. Current workspace result: `not observed in this cycle`.

#### Historical Overview

This reference compares the official Claude Code and Codex surfaces against the
tracked adapters in this worktree. It deliberately distinguishes three evidence
depths: a checked product capability, a repository-static declaration, and an
authenticated/runtime observation. A row does not become a runtime fact because
configuration with a familiar filename exists.

#### Historical Reference Type

Official-provider source review and repository-static status matrix, observed on
2026-08-08.

#### Historical Authority Boundary

Anthropic and OpenAI own their products' instructions, settings, hooks,
subagents, MCP, model, sandbox, approval, and memory semantics. Stage 00 owns
this repository's policy, task gates, and evidence vocabulary. Credentials,
account entitlements, actual configuration parse/discovery, hook trust/delivery,
model availability, and live execution are outside this research scope and are
`DEFER` unless separately observed.

#### Historical Scope

This owner covers REQ-WERPC-004 (Claude) and REQ-WERPC-005 (Codex), including
instruction discovery, configuration, hooks, subagents, MCP, sandbox/approval,
memory, model, and runtime boundaries. Common control-plane findings route to
[workspace governance](m0001-workspace-governance-and-common-agent-environment.md).

#### Historical Definitions / Facts

#### Evidence vocabulary

| Status       | Meaning in this reference                                                                                                              |
| ------------ | -------------------------------------------------------------------------------------------------------------------------------------- |
| `Verified`   | A dated official source supports the bounded product claim, or the named tracked file directly supports a static implementation claim. |
| `Partial`    | The source/file supports only part of the requested behavior; the missing dimension is named.                                          |
| `Unverified` | A local claim needs inspection or no adequate source exists.                                                                           |
| `DEFER`      | The claim requires unauthorized/unavailable authenticated, provider-runtime, hosted, remote, credential-bearing, or live evidence.     |

“Verified” never crosses an evidence boundary: a verified official feature is
not proof that the local adapter is used; a verified tracked adapter is not
proof that a provider discovered or enforced it.

#### Claude baseline

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
`AGENTS.md`: [Claude provider notes](../../../../.claude/provider.md)
forbid that import because `AGENTS.md` is the GPT/Codex provider shim, so shared
governance reaches Claude through the bootstrap import rather than through an
`AGENTS.md` bridge. This is a **static configuration fact** and is the local
choice among the options the product documents; whether a given Claude Code
session loaded it is `DEFER`. Checked 2026-08-10.

#### Codex baseline

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

#### Provider surface matrix

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

#### Static configuration, native discovery, and runtime evidence

The required separation is operational, not semantic hair-splitting:

| Evidence layer        | What it can establish                                                                                                | What it cannot establish                                                                                   | Current WERPC-002 result                                                                  |
| --------------------- | -------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| Static configuration  | A tracked file, adapter, hook declaration, command boundary, or local contract exists at the reviewed commit.        | That a provider parsed, trusted, loaded, executed, or enforced it.                                         | `Verified` for named `.claude/**`, `.codex/**`, Stage 00, and provider-neutral contracts. |
| Native discovery      | A specified client/version loaded the declared project instruction/configuration/agent surface.                      | Authentication success, tool permission grant, model resolution, effect of every hook, or live deployment. | `DEFER`; no authorized client instrumentation was collected.                              |
| Authenticated/runtime | The account/client actually authenticated, resolved a model, connected an MCP, and produced scoped runtime evidence. | Broader account entitlement, another provider, or production/live environment health.                      | `DEFER`; credentials and external-state inspection were excluded.                         |

#### Comparison gaps and target rules

| Gap                                                     | Why it matters                                                                                      | Target rule                                                                                                                                                                                                                                                                    |
| ------------------------------------------------------- | --------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Treating `AGENTS.md` as native Claude discovery.        | Claude documents `CLAUDE.md` as the reader and `AGENTS.md` as an import bridge.                     | Record that shared governance reaches Claude through the bootstrap import, not through an `AGENTS.md` bridge, and treat the documented bridge as a product option this repository declines; use `/context` or equivalent observed runtime evidence before asserting discovery. |
| Treating `.codex/hooks.json` as a permission gate.      | Codex hooks and sandbox/approval are separate official surfaces.                                    | Keep authorization in sandbox/approval controls and Stage 00 boundaries; hooks may provide context/validation only unless an observed, documented enforcement result says otherwise.                                                                                           |
| Calling adapter parity provider parity.                 | A parallel file inventory says nothing about discovery, schema compatibility, or tool availability. | Validate common semantics statically; report separate per-provider discovery/runtime columns.                                                                                                                                                                                  |
| Hard-coding model names as availability.                | Models and reasoning levels are provider/client/account dependent.                                  | Keep role policy as target/candidate configuration; require an authenticated observed resolution before `Verified`.                                                                                                                                                            |
| Assuming a project Codex configuration exists.          | The official `config.toml` surface does not establish a file in this repository.                    | Record the absence as a workspace gap; do not call `.codex/CODEX.md` configuration.                                                                                                                                                                                            |
| Elevating provider auto memory to repository authority. | Auto memory is contextual and can be stale or private.                                              | Preserve repository-wins resume and promote only reviewed redacted learning to `progress.md` or domain owners.                                                                                                                                                                 |
| Enabling broadly to compensate for unknown behavior.    | Wider tools, network, and permissions expand impact without evidence.                               | Start least privilege, keep writable roots bounded, request explicit escalation, and use read-only research by default.                                                                                                                                                        |

#### Workspace Application

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

#### 2026-08-17 full-corpus refresh

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

#### 2026-08-20 full-corpus reverification

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

#### 2026-08-23 provider-contract and authority-convergence increment

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

#### Historical Review and Freshness

Refresh after an official provider release or documentation revision changing
instruction discovery, configuration precedence, hook trust/events, agent
schema, MCP authorization, sandbox/approval, memory, or model behavior; refresh
immediately when local adapters change. The source register keeps the checked
date and scope. Runtime assertions require a separate approved, non-secret
observation and must identify client/version, evidence class, date, and exact
surface.

#### 2026-09-05 external-source reverification

This increment re-observed the two provider owners under the approved
2026-09-05 follow-on cycle. Workspace re-observation was excluded by direct user
decision. New sources are `SRC-WERPC-131` through `SRC-WERPC-136`; the cycle
claims are `CLM-WERPC-016-06` and `CLM-WERPC-016-07`.

#### REQ-WERPC-004 Claude surface re-observation

- **Sources and external result:** `changed` in three respects.

  First, the permission surface moved and grew. The access-management path
  previously cited for permission modes now renders authentication content, and
  the mode enumeration is documented at a separate path
  ([SRC-WERPC-131](m0012-source-coverage.md#2026-09-05-external-source-reverification)).
  That enumeration includes a classifier-reviewed automatic mode which the
  vendor documents as the starting mode for stated plan tiers from stated client
  versions. Any reading of the older citation for mode content is now
  misdirected.

  Second, the hook surface is materially wider than any list this corpus had
  enumerated, with five hook types, an unconditional blocking exit code, an
  administrative setting that suppresses non-managed hooks, and model-switch
  events added in a release dated after the previous increment
  ([SRC-WERPC-133](m0012-source-coverage.md#2026-09-05-external-source-reverification),
  [SRC-WERPC-134](m0012-source-coverage.md#2026-09-05-external-source-reverification)).
  The previously recorded distinction between deterministic command hooks and
  experimental agent hooks is confirmed unchanged.

  Third, settings precedence is documented as a five-level stack in which most
  keys merge across scopes while named keys are taken whole from the highest
  scope that sets them
  ([SRC-WERPC-132](m0012-source-coverage.md#2026-09-05-external-source-reverification)).
- **Workspace selector and result:** `not observed in this cycle`. The
  [Claude baseline](#claude-baseline) retains its earlier repository-static
  observation date; no tracked settings, hook, or projection file was re-read.
- **As-Is, gap, and target:** the row stays `Verified` for bounded product
  surfaces at public-documentation depth. The practical consequence is that a
  local assumption that a manual confirmation is the universal default is no
  longer supported by the vendor's own default table for every plan tier. That
  is a review trigger for the owning governance document, not a finding against
  this reference.
- **Evidence boundary:** blocking class and retained boundary remain
  `provider-runtime` / `DEFER`. Documented modes, events, and precedence do not
  prove this account's plan, the installed client version, the effective mode,
  hook delivery, or any permission decision in this worktree.
- **Owner, safe follow-up, and trigger:** owner is this reference and the Stage
  00 approval and safety policy. The safe follow-up is for the approval-boundary
  owner to re-read its own default-mode assumption against the current
  enumeration. Refresh when the mode enumeration, default-mode table, hook
  events, or settings precedence changes.

#### Requested provider sub-areas not admitted in this cycle

The 2026-09-05 request named several provider sub-areas explicitly. Four of
them were investigated but are recorded here as unmet evidence rather than as
findings, because collection reached only search-result depth and
`C-WRFR-003` does not accept a search summary as a substitute for reading a
source. No claim, source identifier, or status change is attached to any of
them.

| Requested sub-area | Evidence reached in this cycle | Disposition |
| --- | --- | --- |
| Global system-prompt and standing-context configuration for each provider | One provider's system-prompt append mechanism was read directly; the other provider's instruction-override key was named on a page that did not show its default or example in the returned excerpt. | `Partial` external evidence; not admitted. Needs a direct read of the second provider's advanced configuration page. |
| Git pre-commit hook integration for each provider | Both providers document integration patterns rather than a managed feature, but neither page was read in full. | `Unverified`; not admitted. The apparent absence of a first-class feature is itself the likely finding and needs a direct read to state. |
| Editor shortcuts and code actions | One provider's keybinding reference was read directly; the other provider's IDE page explicitly stated it did not contain shortcut-customisation detail, and the page that plausibly does was located but not read. | `Partial` external evidence; not admitted. |
| Token limits, context-window management, and cost or rate-limit controls | One provider's cost and limits page was read directly; the other provider's advanced configuration keys were named without numeric defaults in the returned excerpt. | `Partial` external evidence; not admitted. |

Each row is a bounded, named gap with a defined next step: read the exact
missing page directly in a later cycle. None of them blocks any claim recorded
above, and none may be cited as evidence until it is read.

#### REQ-WERPC-005 Codex surface re-observation

- **Sources and external result:** `changed` in one respect and `unchanged`
  otherwise. The instruction-discovery chain, its size limit, the configuration
  reference's accepted reasoning values and model example, the sandbox and
  approval vocabulary, and the memory default were all re-observed as
  `unchanged` on 2026-09-05. The hook reference was captured in detail for the
  first time, including a hash-anchored trust model that requires re-approval
  after any hook edit and fields documented as parsed but not yet implemented
  ([SRC-WERPC-135](m0012-source-coverage.md#2026-09-05-external-source-reverification)).
  The model page now lists eight identifiers and a six-value effort vocabulary
  that agrees with neither the configuration reference nor the earlier recorded
  subagent guidance
  ([SRC-WERPC-136](m0012-source-coverage.md#2026-09-05-external-source-reverification)).
- **Workspace selector and result:** `not observed in this cycle`. The
  [Codex baseline](#codex-baseline) retains its earlier repository-static
  observation date.
- **As-Is, gap, and target:** the row stays `Verified` for bounded product
  surfaces at public-documentation depth. The internal disagreement across the
  vendor's own pages is now three-way; the correct local response remains to
  treat no single page as authoritative and to resolve identifiers only at the
  adapter edge.
- **Evidence boundary:** blocking class and retained boundary remain
  `provider-runtime` / `DEFER`. A documented field is not a parsed field, and a
  documented model name is not an available model.
- **Owner, safe follow-up, and trigger:** owner is this reference and the Stage
  00 provider notes. A candidate contradiction was raised during collection
  about whether a legacy documentation host still redirects; it was supported
  only by search results, was not confirmed by a direct request, and is
  therefore recorded here as unverified rather than as a finding. Refresh when
  any cited page changes, or when a direct request settles the redirect question.

## Sources

The [current source observations](m0012-source-coverage.md#current-source-observations) own exact URLs/revisions and claim support for SRC-WERPC-004–009, 011–013, 049, 066, 068, 087, 096, 136, 137, 156–169 and 237–243 used above. Every current read is 2026-09-27. Version numbers above are documented feature gates, not detected local installations. MCP revision is 2026-07-28; unversioned pages and editor documentation expose no immutable installed revision or publication/modification date in this evidence.

### Historical source provenance

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

Recheck when instruction fallback/modes, skills/plugin discovery, subagent fields/precedence, hook event/trust/failure semantics, sandbox/approval, MCP transports, IDE commands, cloud environments, SDK revision or model/account policy changes. The four previously unmet provider subareas now have direct source support for system-prompt keys, bounded Git/provider/editor distinctions, IDE bindings and cost/context contracts; universal native documentation automation and equivalent review triggers remain explicitly unverified. Later local verification requires exact product/version and approved synthetic runtime evidence, not a tracked-file count.

## Related Documents

- [Harness and loop engineering](m0002-harness-and-loop-engineering.md)
- [Workspace governance and common environment](m0001-workspace-governance-and-common-agent-environment.md)
- [Source ledger](m0012-source-coverage.md)
- [Claude provider notes](../../../../.claude/provider.md)
- [Codex provider notes](../../../../.codex/provider.md)
