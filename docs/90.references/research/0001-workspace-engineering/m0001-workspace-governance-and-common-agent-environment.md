---
title: 'Reference: Workspace Governance and Common Agent Environment'
version: "1.0.0"
type: reference/research
layer: "references"
status: published
owner: platform
updated: 2026-08-31
artifact_id: "RES-0001-m0001"
---

# Reference: Workspace Governance and Common Agent Environment

## Overview

This reference maps the shared workspace environment that Claude and Codex
adapters are intended to serve. Its design conclusion is a provider-neutral
control plane: the repository owns task scope, governance, evidence, recovery,
and durable knowledge; each provider owns how it discovers instructions,
configures tools, asks for approval, executes hooks, authenticates, and resolves
models. The distinction preserves portability without inventing provider parity.

## Reference Type

Repository-static implementation analysis supported by dated primary provider
sources, observed on 2026-08-08.

## Authority Boundary

Stage 00 is authoritative for shared workspace policy and contracts. This
reference does not change those policies, create a runtime permission, or
establish authenticated provider behavior. The `.claude/**` and `.codex/**`
trees are reviewed configuration surfaces only. Provider discovery, hook trust
and delivery, model resolution, external-tool authentication, CI execution, and
live platform readiness stay `DEFER` without separately authorized evidence.

## Scope

This owner covers REQ-WERPC-003 (workspace application) and REQ-WERPC-006
(common system). It covers application at work-item, session, project, provider,
and CI scope; harness and provider details are linked rather than duplicated.

## Definitions / Facts

### Common-system baseline

The 2026-08-08 baseline used `harness-catalog.md` as the repository's
common-harness inventory. Current navigation starts at the
[Agent Governance Hub](../../../00.agent-governance/README.md), with machine
membership owned by the [Agent Registry](../../../../.agents/registry.json).
The dated inventory identified thin gateways,
runtime baselines, roles/adapters, shared assets, hooks, validation, memory,
and escalation. `AGENTS.md` and `CLAUDE.md` are thin gateways, while
`.codex/CODEX.md` and `.claude/CLAUDE.md` contain provider-local baselines.
These are `Verified` as tracked files on the reviewed commit; no native provider
discovery was tested in this research task.

### Workspace-application baseline

The JIT workflow encoded in bootstrap and both runtime baselines is:

`bootstrap → preflight → persona → scope → provider → progress → postflight`.

It is a repeatable intake route, not evidence that a client automatically read
every document. The route binds provider behavior to canonical workspace owners
before substantial work, rather than embedding mutable policy in an individual
task prompt or provider adapter.

### Common Provider-Neutral Control Plane

| Plane element                    | Canonical owner                                                                | Required behavior                                                                                                                      | Evidence depth today                                                      |
| -------------------------------- | ------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| Task contract                    | Stage 03 Spec and Stage 04 Plan/Task                                           | Name acceptance IDs, owned paths, authority, validation, rollback, and next owner.                                                     | `Verified` static document/registry contract.                             |
| Instruction routing              | `AGENTS.md`, `CLAUDE.md`, bootstrap, runtime baselines, scopes, provider notes | Enter via the appropriate gateway and load only the relevant JIT context.                                                              | `Verified` static routing; native discovery `DEFER`.                      |
| Authority and security           | `rules/agentic.md`, approval boundary, provider notes                          | Default to GitOps PR-ready repository work; no secrets, destructive Git, external writes, or live mutations without explicit approval. | `Verified` static rule; provider enforcement `DEFER`.                     |
| Templates and document ownership | Stage 99 template routing and document profiles                                | Choose a canonical document route before authoring, retain source/owner links.                                                         | `Verified` static contract.                                               |
| Evaluation                       | quality standards and validation-surface contract                              | Select affected validators and report independent `PASS`/`SKIP`/`FAIL`/`DEFER` lanes.                                                  | `Verified` static controls; hosted/live execution `DEFER`.                |
| Recovery                         | agent-loop/checkpoint contracts                                                | Repository-wins resume, bounded retries, redaction, no-progress escalation, compact handoff.                                           | `Verified` contract; actual ignored checkpoint/provider behavior `DEFER`. |
| Knowledge                        | memory README, `progress.md`, owning operational/SDLC records                  | Separate working, durable, domain, and provider-local auxiliary memory.                                                                | `Verified` static owner design; provider persistence `DEFER`.             |
| Provider adapters                | `.claude/agents/`, `.codex/agents/`, shared `.agents/` content                 | Preserve role, scope, guardrails, handoff, and postflight semantics while retaining native metadata.                                   | `Verified` static parity surface; runtime consumption `DEFER`.            |

This separation follows the product evidence without collapsing it: Claude
documents persistent `CLAUDE.md` context and contextual auto memory, while
Codex documents `AGENTS.md` instruction chains and project configuration. Each
fact supports a provider edge; neither changes the local canonical owner.
[SRC-WERPC-004](m0012-source-coverage.md#source-register) and
[SRC-WERPC-009](m0012-source-coverage.md#source-register) record
the source boundaries.

### Application Rules by Scope

| Scope     | Apply                                                                                                                                 | Do not infer                                                                         | Security / failure response                                                                                              |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------ |
| Work item | Bind a named request, acceptance criteria, owned paths, validation lane, evidence class, rollback, and handoff to one logical change. | A broad project policy is permission for unrelated files or external action.         | Stop/escalate when scope, authority, owner, or acceptance criterion is ambiguous.                                        |
| Session   | Rediscover tracked state; load scoped guidance; use the current task table and progress ledger; retain a compact redacted handoff.    | A prior conversation, auto memory, or ignored checkpoint overrules repository state. | Treat stale/conflicting memory as advisory; record limitation and re-plan from repository evidence.                      |
| Project   | Keep canonical policy, machine contracts, templates, validators, and durable progress under version control.                          | A repository file is automatically enforced by all clients.                          | Change the smallest canonical owner when a recurring defect demonstrates a control gap.                                  |
| Provider  | Map shared semantics to that provider's native instruction/config/hook/agent/MCP/sandbox/approval surface.                            | Equal adapter stems, filenames, or intent mean semantic/runtime equivalence.         | Record static config separately from discovery and authenticated execution; request provider-specific proof when needed. |
| CI        | Run selected static checks with bounded output and report exact path scope.                                                           | CI pass proves live cluster, provider runtime, remote action, or deployment health.  | Classify remote/live as `DEFER` unless it ran under approved authority and exact evidence is retained.                   |

### Workspace Gap and Target Matrix

| Area                        | Current evidence                                                                                                                                                                                                                                                                                         | Gap                                                                                                                      | Recommended target state                                                                                                          | Application rule                                                                                           |
| --------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| Gateway consistency         | Root gateways point into the same bootstrap/quality/template network.                                                                                                                                                                                                                                    | Each provider discovers gateway files differently.                                                                       | Preserve provider-specific bridge/adapters and validate links, not identical discovery claims.                                    | Verify discovery with a provider-native inspection only when the claim is necessary.                       |
| Instructions                | The two root gateways are parallel, not chained: `CLAUDE.md` imports the shared bootstrap, the Claude provider note, `.claude/CLAUDE.md`, and `RTK.md`; `AGENTS.md` imports the same bootstrap, the Codex provider note, `.codex/CODEX.md`, and `RTK.md`. Neither imports the other. Checked 2026-08-10. | Gateway thinness and the no-cross-import rule are prose policy in the provider notes; no validator enforces them.        | Keep gateways thin, canonical policy once, task/scope detail JIT.                                                                 | Move repeated multi-step method to an owned skill/template, not duplicated gateway prose.                  |
| Hooks                       | Common scripts are wired in both provider trees.                                                                                                                                                                                                                                                         | Static wiring does not show trust, supported event, ordering, or block outcome.                                          | Use native permission/sandbox for authorization; hooks supply bounded context/validation/review evidence.                         | Treat a missing runtime hook as a `DEFER` limitation and run explicit quality gates.                       |
| Subagents                   | A role roster is represented on Claude and Codex surfaces.                                                                                                                                                                                                                                               | Parallel writers can collide; provider agent schemas/tools differ.                                                       | Delegate only bounded independent work, assign owned paths, collect source/evidence summaries, retain one integration owner.      | Avoid concurrent edits to shared owners; child inherits task boundary, not extra authority.                |
| MCP/external context        | Provider notes/config mention a baseline set.                                                                                                                                                                                                                                                            | Connection, OAuth/key availability, tool scope, and data flow are not inspected.                                         | Maintain an owner/sensitivity/approval inventory per enabled server.                                                              | Use read-only lookup by default; require explicit approval before writes or credential-bearing activation. |
| Sandboxing and approvals    | Repository policy identifies least-privilege and escalation boundaries.                                                                                                                                                                                                                                  | Client setting and current environment may differ.                                                                       | Default to bounded writable roots and on-request approval; state exact runtime settings only when observed.                       | Do not emulate an approval decision by changing a repository document.                                     |
| Codex project configuration | `.codex/CODEX.md`, hooks, and agents are tracked.                                                                                                                                                                                                                                                        | No project `.codex/config.toml` is tracked, so a local Codex model/sandbox/approval/MCP configuration cannot be claimed. | Keep intended provider guidance in the provider note; add a project config only through a separately approved configuration task. | Treat absence as a gap, not as a failed or unobserved runtime setting.                                     |
| Memory                      | Four authority classes and a progress ledger are explicit.                                                                                                                                                                                                                                               | Provider memory may be stale, private, or unreviewed.                                                                    | Repository-wins recovery; only reviewed/redacted lessons promote to durable/domain owners.                                        | Never write secret/raw transcript/tool output into durable memory.                                         |
| Models/runtime              | Role policy and adapters declare intended values.                                                                                                                                                                                                                                                        | Availability, reasoning options, and authentication are client/account dependent.                                        | Maintain configured/candidate/observed distinctions and evaluate before promotion.                                                | `DEFER` any resolved-model claim without the specific authenticated observation.                           |

### Target-State Rollout

The target is incremental and control-first. It does not require an external
platform migration or a new provider surface.

1. **Task discipline** — require every non-trivial task to declare owned paths,
   acceptance evidence, authority boundary, stop condition, and rollback before
   editing. Apply the state machine from the harness reference.
2. **Provider-edge honesty** — retain a per-provider matrix with static,
   discovery, and runtime columns. When a capability changes, refresh only the
   authoritative source row and affected adapter claim.
3. **Failure learning** — normalize a failure, prohibit identical no-progress
   retries, then revise the smallest shared rule/validator/template after
   review. Do not turn model prose into evidence.
4. **Controlled external context** — document each MCP/data source's owner,
   least privilege, sensitivity, refresh, and approval behavior before using it
   in a task that can mutate external state.
5. **CI/static evidence** — preserve exact local/CI results and limitations;
   add a separate approved lane rather than calling static validation live
   readiness.

### Failure and Security Boundaries

The control plane treats the following as boundary crossings rather than normal
retry candidates: permission denial, credential/secret exposure, destructive
live mutation risk, schema corruption, and an explicit user stop. The first four
escalate; the last aborts. A retry needs a different authorized action plus a
measurable progress delta. This supports security in two ways: it prevents
permission expansion by repetition and avoids turning raw diagnostics or
provider-local data into an unbounded knowledge store.

For this GitOps repository, the default execution proof is a reviewable desired
state change and repository-static checks. `kubectl apply`, controller sync,
secret mutation, force push, credential reads, and external publication stay
outside the default path. The provider's own permission feature may add
technical enforcement, but no repository declaration substitutes for explicit
human approval of the protected action.

### 2026-08-17 full-corpus refresh

This increment is the fifth refresh cycle over this pack, executed under
Spec 058. Unlike the three preceding cycles it re-observed every owner row in
the pack rather than the twelve `Partial` rows, and it assigns each retained
`Partial` or `DEFER` row a blocking class recorded in the
[scope application index](m0013-scope-application-index.md). All observations are
dated **2026-08-17**. No live cluster, hosted CI run, provider runtime,
authenticated execution, or secret value was observed.

#### REQ-WERPC-003 re-observation

**External result:** `unchanged` (`SRC-WERPC-079`). The Claude Code memory page
still states that Claude Code reads `CLAUDE.md` and not `AGENTS.md`, and still
documents the `@AGENTS.md` import or symlink bridge as a recommended pattern
that this repository deliberately declines. The JIT sequence has no vendor
counterpart to contradict and remains a repository-owned pattern.

**Workspace result:** `confirmed`. `AGENTS.md:1-4` imports bootstrap, the Codex
provider note, `.codex/CODEX.md`, and `RTK.md`, symmetric to the `CLAUDE.md`
import set. Neither gateway imports the other, so the two-parallel-gateway
topology recorded by the 2026-08-10 correction still holds.

**Status effect:** `no-change` (`CLM-WERPC-011-03`). **Blocking class:**
`repo-static`, reachable. Reopens on a change to either gateway's import list.

#### REQ-WERPC-006 re-observation

**External result:** `changed` (`SRC-WERPC-079`, `SRC-WERPC-083`). Both pages
this row depends on grew materially since the 2026-08-14 `unchanged` verdict.
The Claude Code memory page now documents managed-policy `CLAUDE.md`,
`claudeMdExcludes`, an `/import` command, an `InstructionsLoaded` hook
cross-reference, a `modified` frontmatter timestamp, and expanded
`.claude/rules/` symlink and brace-expansion budget details. The subagents page
gained `disallowedTools`, `skills`, `mcpServers`, scoped `hooks`, a `memory`
scope, `background`, `effort`, `isolation`, `color`, `initialPrompt`, and a
`fable` model alias. The claim under test — that the `CLAUDE.md` and `AGENTS.md`
split exists and that tool, MCP, permission, hook, skill, isolation, and memory
frontmatter fields exist — is extended rather than contradicted.

**Workspace result:** `confirmed`. `harness-catalog.md:93-100` and
`contracts/harness-contract.json:5-6` still record `contractVersion` `1.0.0`,
cutoff `2026-07-10T10:00:00+09:00`, and `12 roles / 4 surfaces / 48 adapters`.
Direct enumeration returns twelve files in each of `.claude/agents/`,
`.codex/agents/`, `.agents/agents/`, and `.gemini/agents/`, totalling
forty-eight, an exact match. The `.claude/skills`, `.claude/workflows`, and
`.claude/output-styles` symlinks resolve to the `.agents/` single source of
truth.

**Status effect:** `no-change` (`CLM-WERPC-011-06`). The row keeps `Partial`:
static shared controls remain verified and provider parity plus effective
runtime remain `DEFER`. A documentation surface growing does not promote a
parity claim.

**Blocking class:** `repo-static`, reachable. Reopens if the harness contract's
counts diverge from actual adapter files, or if a newly documented subagent or
memory field must be adopted for a parity claim to hold.

#### Tooling caveat recorded for successors

The `Glob` tool does not traverse the `.claude/skills`, `.claude/workflows`, or
`.claude/output-styles` symlinks, while `Read` resolves them correctly. An agent
trusting `Glob` alone could wrongly conclude the shared assets are absent. This
is a tool artifact, not workspace drift.

### 2026-08-20 full-corpus reverification

This increment consumes the reviewed provider/common report and its empty
source/claim allocation slice. It adds no identifier and does not restate the
unchanged control-plane baseline. Public product documentation is evidence for
provider contracts only; tracked files are repository-static evidence only.

#### REQ-WERPC-003 workspace application

- **External/workspace result:** `unchanged` / `confirmed`, using the existing
  provider-source boundaries `SRC-WERPC-004` and `SRC-WERPC-009` and workspace
  selector
  `docs/90.references/research/0001-workspace-engineering/m0001-workspace-governance-and-common-agent-environment.md#workspace-application-baseline`.
- **As-Is:** at baseline commit `8d8c8e5634fe939f8daaf041fbf5dfb444ed4a9c`,
  `CLAUDE.md` and `AGENTS.md` remain parallel thin gateways. Each routes through
  bootstrap, its provider note and baseline, and `RTK.md`; neither imports the
  other. The repository-owned chain still binds task scope, environment and
  permission boundaries, tools, checkpoints, evaluation lanes, and evidence
  reporting before provider-specific execution.
- **Gap / Target:** no native Claude or Codex discovery, installation,
  authentication, entitlement, effective instruction chain, or execution was
  observed. Preserve the two gateways and the repository-owned JIT route;
  collect a versioned, non-secret provider-native observation only when an
  operational claim is authorized and necessary.
- **Evidence depth / rejected inference:** current public documentation plus
  repository-static selectors. Parallel gateways and documented instruction
  surfaces do not prove that either provider loaded or enforced this worktree.
- **Disposition / retained boundary:** `Verified` for the bounded product and
  tracked topology claims; provider-native and authenticated/runtime behavior
  remains `DEFER` under blocking class `repo-static`.
- **Owner / safe follow-up / trigger:** Stage 00 workspace and provider
  governance. Reinspect both gateway import lists without invoking a provider;
  reopen on a material Claude instruction-loading, Codex AGENTS-discovery, or
  root-gateway change.

#### REQ-WERPC-006 common system

- **External/workspace result:** `changed` / `confirmed`, within existing
  `SRC-WERPC-004`, `SRC-WERPC-007`, `SRC-WERPC-009`, `SRC-WERPC-011`, and
  `SRC-WERPC-068` boundaries and workspace selector
  `docs/90.references/research/0001-workspace-engineering/m0001-workspace-governance-and-common-agent-environment.md#common-system-baseline`.
- **As-Is:** the harness catalog and contract still project twelve roles onto
  four tracked provider surfaces, forty-eight adapters in total. The shared
  layer owns scope, permission, tool, checkpoint, evaluation, evidence, and
  durable-memory semantics; each adapter retains its provider-native
  instruction, subagent, hook, sandbox/approval, MCP, memory, and model edges.
- **Gap / Target:** current Claude documentation exposes a broader subagent
  field surface, while Codex documentation continues to distinguish AGENTS,
  custom agents, and optional local memory. Neither change proves discovery,
  parsing, authentication, permission enforcement, retention, or effective
  cross-provider parity. Preserve one repository control plane with distinct
  provider projections and require separately authorized per-provider runtime
  evidence for parity claims.
- **Evidence depth / rejected inference:** repository-static inventory plus
  current official public contracts. Equal counts, shared symlink views, and
  overlapping product features do not prove semantic or runtime equivalence.
- **Disposition / retained boundary:** `Partial`; the static common control
  plane is confirmed, while provider-native parity and authenticated execution
  remain `DEFER` under blocking class `repo-static`.
- **Owner / safe follow-up / trigger:** Stage 00 harness/provider governance.
  Reconcile static counts and contracts on a local change; reopen on a material
  provider contract, harness inventory, adapter-tree, or shared-asset-link
  change, and use a versioned non-secret runtime canary only with separate
  authorization.

## Sources

- **SRC-WERPC-004–008**: official Anthropic Claude Code documentation, checked
  2026-08-08, establishes product-specific surfaces only.
- **SRC-WERPC-009–013**: official OpenAI Codex documentation, checked
  2026-08-08. A non-repository manual cache was the first review surface; it is
  ephemeral, so the ledger's official URLs are the durable citation.
- **Workspace evidence**: `AGENTS.md`, `CLAUDE.md`, `.claude/**`, `.codex/**`,
  `docs/00.agent-governance/{rules,providers,contracts}/**`, and
  `harness-catalog.md`, inspected in the WERPC worktree on 2026-08-08.

## Review and Freshness

Recheck this reference if a gateway, provider adapter, Stage 00 control,
validation contract, MCP inventory, or official provider document changes.
Provider discovery/authentication/runtime rows must be re-observed per client
and date; they cannot inherit freshness from a static-config review. The source
ledger keeps the URLs, date, claim boundary, and refresh triggers. WERPC-002 did
not inspect secret values, private configuration, accounts, or live systems.

### 2026-08-11 Partial/DEFER incremental refresh

This bounded increment was executed and the cited live documentation was
checked on **2026-08-12**. The date in the heading identifies the approved
refresh package; it is not a claim that the checks ran on 2026-08-11. No
provider was authenticated or invoked, and no provider-local state or
effective permission was inspected.

#### REQ-WERPC-006 source and workspace reconciliation

| Evidence                                                                               | Official publication / revision                                     | Adopted scope                                                                                                                                                                               | Rejected inference, uncertainty, and refresh trigger                                                                                                                      |
| -------------------------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [OpenAI Codex AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md) | Current official page; no publication or last-modified date exposed | Codex builds a global-to-project instruction chain, checks one instruction file per directory, and gives nearer project guidance later precedence.                                          | Does not prove this session loaded the tracked gateway. Recheck when discovery order, fallback names, or size limits change.                                              |
| [OpenAI Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) | Current official page; no publication or last-modified date exposed | Project-scoped TOML agents, parent sandbox/approval inheritance, agent-file overrides, and explicit orchestration are current product surfaces.                                             | Does not prove local agent discovery, spawn, inherited tools, approvals, or execution. Recheck when schema, inheritance, or orchestration changes.                        |
| [OpenAI Codex memories](https://learn.chatgpt.com/docs/customization/memories)         | Current official page; no publication or last-modified date exposed | Local Codex memories are a separate generated recall store, are off by default, have per-chat use/generation controls, and are not the required-guidance owner.                             | Does not prove enablement, generation, retrieval, redaction, retention, or deletion in this environment. Recheck when memory storage, controls, or lifecycle changes.     |
| [Anthropic Claude Code memory](https://code.claude.com/docs/en/memory)                 | Current official page; no publication or last-modified date exposed | `CLAUDE.md` and auto memory are context rather than enforcement; auto memory is repository-scoped, machine-local, shared across worktrees, bounded at startup, and user-editable/deletable. | Does not prove that a Claude process loaded or changed memory. Recheck when loading, scope, compaction, deletion, or enforcement changes.                                 |
| [Anthropic Claude Code subagents](https://code.claude.com/docs/en/sub-agents)          | Current official page; no publication or last-modified date exposed | Current subagent definitions can scope tools, MCP servers, permission mode, hooks, skills, isolation, and memory, with parent/runtime rules affecting execution.                            | Does not prove discovery, effective permission order, delegation, or tool use for tracked adapters. Recheck when agent fields, permission inheritance, or memory changes. |

**As-Is:** `AGENTS.md`, the `.claude/`, `.codex/`, `.gemini/`, and
`.agents/` trees, and `docs/00.agent-governance/harness-catalog.md` still
project one repository-neutral control plane into provider-specific edges.
`contracts/harness-contract.json` records 12 roles, four repo-static surfaces,
48 current projections, and four non-transitive evidence classes. The current
Codex local-memory and Claude agent/memory contracts fit the existing
`provider-local-auxiliary` boundary; neither moves authority away from
checked-in owners.

**Gap and bounded target:** Native discovery, parsing, permission enforcement,
memory behavior, and cross-provider runtime parity remain unobserved. Preserve
the current static/provider-runtime separation. If a later claim needs runtime
parity, its owner must authorize a versioned, non-secret provider-native
inspection for the exact surface instead of extrapolating from tracked files.

**Final disposition:** `Partial`. Evidence depth is current official public
contract plus exact repository-static selectors. This check refreshes the
provider edge with observation-time evidence, but effective parity remains
`DEFER`. Owner: Stage 00 harness/provider governance. Refresh when one of the
cited provider contracts or named workspace selectors materially changes.

### 2026-08-14 consistency and Partial re-observation

This bounded increment re-observed the workspace and re-checked external
sources for `REQ-WERPC-006` only, checked on **2026-08-14**. It did not
invoke a provider, query the GitHub remote, or inspect a cluster.

#### REQ-WERPC-006 workspace and source consistency check

**Workspace delta:** `no-change`. `harness-catalog.md` and
`contracts/harness-contract.json` still describe exactly `12 roles / 4
surfaces / 48 adapters` at contract version `1.0.0`; `AGENTS.md`,
`CLAUDE.md`, `.claude/`, `.codex/`, `.gemini/`, and `.agents/` still project
the same provider-neutral control plane onto provider-specific edges
recorded in the 2026-08-11 section.

**External result:** all five sources were reachable and `unchanged` against
their 2026-08-12 adopted scope.

| Source                                                                                 | Result      | Note                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| -------------------------------------------------------------------------------------- | ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [OpenAI Codex AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md) | `unchanged` | Discovery order (global then project, override-then-base, `project_doc_fallback_filenames`), and the 32 KiB `project_doc_max_bytes` default still match. No publisher date.                                                                                                                                                                                                                                                                    |
| [OpenAI Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) | `unchanged` | Required `name`/`description`/`developer_instructions` fields, the agent-file-then-spawn-then-`[agents]`-default-then-parent precedence, and the `gpt-5.6`/`gpt-5.6-terra`/`gpt-5.6-luna`/`gpt-5.3-codex-spark` examples still match. No publisher date.                                                                                                                                                                                       |
| [OpenAI Codex memories](https://learn.chatgpt.com/docs/customization/memories)         | `unchanged` | Off-by-default, per-chat `/memories` controls, no retention/deletion guarantee, and the `AGENTS.md`-is-the-required-guidance-owner caution still match. No publisher date.                                                                                                                                                                                                                                                                     |
| [Anthropic Claude Code memory](https://code.claude.com/docs/en/memory)                 | `unchanged` | The `CLAUDE.md`/auto-memory distinction, on-by-default auto memory, machine-local repository scope shared across worktrees, and the 200-line/25KB `MEMORY.md` load limit still match. The current page also documents that auto-memory files are excluded from the session-transcript cleanup sweep and that subagents may hold a separate auto-memory directory; this extends, and does not contradict, the adopted scope. No publisher date. |
| [Anthropic Claude Code subagents](https://code.claude.com/docs/en/sub-agents)          | `unchanged` | Tool/MCP/permission/hook/skill/isolation/memory frontmatter fields, and the environment-override-then-per-invocation-then-frontmatter-then-main-conversation model precedence, still match. No publisher date.                                                                                                                                                                                                                                 |

**As-Is:** Unchanged from the 2026-08-11 section: one repository-neutral
control plane is still projected into Codex/Claude/Gemini/local-Antigravity
edges; `contracts/harness-contract.json` still records 12 roles, four
tracked surfaces, 48 adapters, and four non-transitive evidence classes.

**Gap and bounded target:** Unchanged. Native discovery, parsing, permission
enforcement, memory behavior, and cross-provider runtime parity remain
unobserved.

**Missing evidence:** authenticated, per-provider runtime discovery and
enforcement observation. **Owning authority:** Stage 00 harness/provider
governance. **Safe boundary:** a separately authorized, non-secret,
versioned provider-native inspection of the exact surface only; no live
cluster or credential access. **Refresh trigger:** a cited provider contract
or a named workspace selector materially changes.

**Final disposition:** `Partial`, unchanged from the 2026-08-12 baseline. No
promotion. New source registered: `SRC-WERPC-074`. New claim registered:
`CLM-WERPC-010-01`.

### 2026-08-23 Spec 0054 authority-convergence increment

This is an additive terminal correction, not a topology migration. Under the
approved Spec 0054 direction, the current provider set is Claude and Codex, and
the provider-neutral core owns shared authority, workflow, evidence,
validation, and durable-memory semantics. Provider gateways and adapters only
translate those semantics onto native surfaces. Earlier references to Gemini,
Antigravity, four surfaces, or forty-eight projections remain historical
repository-static observations for their stated dates; they are not current
terminal-provider declarations.

#### Common-environment gap reconciliation

| Boundary | Current external contract | Workspace rule | Evidence disposition |
| --- | --- | --- | --- |
| Codex orchestration | Official [configuration](https://learn.chatgpt.com/docs/config-file/config-reference) and [subagent](https://learn.chatgpt.com/docs/agent-configuration/subagents) pages describe multi-agent support as stable and on by default. | Keep role semantics and task authority in the provider-neutral core; a Codex agent file is a projection, not its owner. | Product capability `Verified`; project discovery, spawn, delivery, authentication, and model resolution `DEFER`. |
| Codex instructions and hooks | Official [AGENTS.md discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md) and [lifecycle hooks](https://learn.chatgpt.com/docs/hooks) are documented product surfaces. | Preserve the thin Codex gateway; keep sandbox/approval as authority and use hooks for bounded lifecycle evidence. | Product contracts `Verified`; effective chain, trust, hook ordering, delivery, and effect `DEFER`. |
| Child authority | Codex documents parent sandbox/approval inheritance and fail-closed behavior when a child cannot obtain required approval. | A child receives bounded paths and acceptance evidence but no authority expansion; the integration owner retains shared-file writes and final evidence. | Documented inheritance `Verified`; an actual approval outcome or child tool set `DEFER`. |
| Claude hooks and isolation | Official Claude [hooks](https://code.claude.com/docs/en/hooks-guide) distinguish deterministic command hooks from experimental agent hooks; [subagents](https://code.claude.com/docs/en/subagents) have separate context and configurable isolation. | Use deterministic command hooks only for repeatable controls, treat agent hooks as advisory/experimental, and require explicit non-overlapping ownership for isolated or parallel work. | Product contracts `Verified`; local discovery, hook delivery, isolation creation, permission effect, and execution `DEFER`. |

The authority correction does not authorize moving Stage 90 research, deleting
legacy projections, rewriting task topology, or cutting over validators. Those
changes remain with their Spec 0054 work packages. Until those owners land the
terminal topology, this research pack uses existing owner paths and records the
transition instead of creating a duplicate report or competing authority.

## Related Documents

- [Harness and loop engineering](m0002-harness-and-loop-engineering.md)
- [Provider implementation status](m0003-provider-implementation-status.md)
- [Source ledger](m0012-source-coverage.md)
- [Agent Governance Hub](../../../00.agent-governance/README.md)
- [Work Lifecycle](../../../00.agent-governance/skills/work-lifecycle.md)
