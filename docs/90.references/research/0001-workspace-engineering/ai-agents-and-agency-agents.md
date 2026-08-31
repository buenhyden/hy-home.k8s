---
title: 'Reference: AI Agents and Agency-Agents'
type: content/reference
status: active
owner: platform
updated: 2026-08-31
---

# Reference: AI Agents and Agency-Agents

## Overview

This reference compares a governed AI-agent system with the pinned upstream
`msitarzewski/agency-agents` prompt catalog. It treats roles, instructions,
tools, isolation, evaluation, and review as a system; a persona file alone is
not an admitted agent. All external observations were checked on 2026-08-08.

## Reference Type

Repository-static and pinned-upstream comparison research.

## Authority Boundary

The [Agent Registry](../../../../.agents/registry.json) owns current local role
and permission membership; provider notes own native behavior. External catalogs are
comparison evidence, not automatic admission authority. Tracked adapters prove
declared configuration only; discovery, authentication, tool enforcement,
delegation, and effectiveness remain `DEFER` without matching runtime evidence.

## Scope

It covers the agent-system control plane, the Agency Agents pin and comparison,
and an adopt/adapt/reject decision rule. Model selection and memory controls
are primary-owned by the sibling references.

## Definitions / Facts

### AI-agent-systems baseline

The 2026-08-08 observation described a repository-static 12-role,
four-provider-surface roster in `harness-catalog.md` and
`contracts/harness-contract.json`. Current membership is routed through the
[Agent Registry](../../../../.agents/registry.json), not that dated roster.
Roles define bounded ownership; their
providers declare task instructions and configuration. The system requires a
work-item owner, scoped inputs, least-privilege tool/sandbox selection,
independent review for material risk, validation evidence, a rollback path, and
a durable handoff. It is `Implemented` as a static contract and `DEFER` for
native provider discovery, execution, permissions, and measured effectiveness.

OpenAI documents subagent workflows and task-specific instructions/model
configuration; Anthropic documents model/tool frontmatter, allow/deny controls,
MCP scoping, and optional worktree isolation. These are product capabilities,
not proof that either provider enforces this workspace's files.

### Agency-agents baseline

The comparison is fixed to
[`ebe9c99acb5c96f9468de368d8bead775387d1a7`](https://github.com/msitarzewski/agency-agents/tree/ebe9c99acb5c96f9468de368d8bead775387d1a7),
observed as the `main` tip on 2026-08-08. The pinned tree contains an MIT
license, Markdown personas with YAML frontmatter, a conversion script that
emits Codex TOML (`name`, `description`, `developer_instructions`), and an
installer that copies generated files. The scripts and installer were inspected
only; they were not executed.

| Upstream assertion or asset | Supported observation                                       | Not established                                                                       |
| --------------------------- | ----------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| Persona catalog             | Markdown role prompts and category layout exist at the pin. | Task fitness, quality, safety, or provider-native discovery.                          |
| Conversion/install scripts  | Script source transforms/copies files.                      | Safe overwrite behavior, successful conversion, installation, or runtime consumption. |
| MIT license                 | License text exists at the pin.                             | License counsel, attribution plan, or approval to copy content.                       |
| README marketing            | It is upstream author prose.                                | Production readiness, automatic update behavior, or a workspace admission decision.   |

### Adopt, adapt, or reject rule

| Decision       | Required condition                                                                                                                                    | Current result                                                                         |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| Adopt          | The exact role closes a documented workspace gap; license, security, roster-admission, provider-adapter, evaluation, and reviewer gates approve it.   | No candidate is adopted.                                                               |
| Adapt          | Only bounded role language is useful; repository rules, tool/sandbox limits, evidence lanes, and local canonical owners replace external assumptions. | Existing local roles remain the canonical adapted roster.                              |
| Reject / defer | The proposal duplicates an existing role, assumes unapproved tools/authority, lacks a benchmark, or requires runtime proof not collected.             | Bulk import, installer execution, and unreviewed prompt copying are rejected/deferred. |

### Agent-system admission and operating rules

1. Classify the work by reversibility, sensitivity, external effect, context,
   and verification burden before assigning a role.
2. Give one worker a bounded file/responsibility owner; use parallel workers
   only for independent, read-safe work. A supervisor reconciles overlap.
3. Bind the smallest tool and sandbox permission set that can perform the
   task. Credentials, live control planes, external writes, and destructive
   actions require their separate approval boundary.
4. Require a reviewer independent of the author for security, GitOps,
   destructive, policy, or high-impact changes. Record disposition, residual
   risk, rollback, and next owner.
5. Promote reusable conclusions only after source, validation, and review
   evidence are captured by a canonical repository owner.

### Confidence, promotion, and rollback

An agent output is a proposal until its cited source, repository observation,
and required validation/review lane agree. Promotion means updating the
canonical owner, not storing a prompt in a provider-local catalog. A failed
evaluation, security concern, incorrect routing, or stale external pin rolls
back by withholding admission or reverting the isolated approved change; it
does not authorize external cleanup or provider configuration changes.

### 2026-08-17 full-corpus refresh

This increment is the fifth refresh cycle over this pack, executed under
Spec 058. Unlike the three preceding cycles it re-observed every owner row in
the pack rather than the twelve `Partial` rows, and it assigns each retained
`Partial` or `DEFER` row a blocking class recorded in the
[scope application index](scope-application-index.md). All observations are
dated **2026-08-17**. No live cluster, hosted CI run, provider runtime,
authenticated execution, or secret value was observed.

#### REQ-WERPC-026 re-observation

**External result:** `unchanged` (`SRC-WERPC-078`). Codex project-agent required
fields and the override and inheritance chain are unchanged. Claude Code
subagent frontmatter still supports the fields this report lists; the current
page additionally documents `maxTurns` and an expanded `permissionMode` enum.
That is non-contradicting new detail, not a claim reversal.

**Workspace result:** `confirmed`. `harness-catalog.md:93-100` still records the
machine contract as exactly `12 roles / 4 surfaces / 48 adapters` and still
names `.gemini/agents/**` as repository-static only.

**Status effect:** `no-change` (`CLM-WERPC-011-26`). The row keeps `Partial`.

**Blocking class:** `provider-runtime`, structurally unreachable. Discovery,
permission enforcement, delegated execution, and role-design effectiveness
cannot be observed from the repository. Reopens if a provider agent contract
contradicts rather than extends prior scope, or if the harness contract counts
change.

#### REQ-WERPC-027 re-observation

**External result:** `unchanged` (`SRC-WERPC-078`). The pinned upstream commit
`ebe9c99acb5c96f9468de368d8bead775387d1a7` is still `HEAD` of `main`. Zero
commits landed since the previous check, so the pin remains byte-identical and
neither ahead nor behind.

**Workspace result:** `confirmed`. `.agents/agents/` still holds exactly the
twelve role files the pinned-commit comparison is scoped against.

**Status effect:** `no-change` (`CLM-WERPC-011-27`). **Blocking class:** `none`
— this row is unblocked and stays `Verified` on reproducible catalog, license,
and script comparison, with adoption, conversion, provider discovery, and
quality remaining out of its scope. Reopens when upstream `main` moves past the
pinned commit or the local role count changes.

## Sources

- [OpenAI Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents), checked 2026-08-08, re-checked 2026-08-10 (`SRC-WERPC-045`).
- [Anthropic Claude Code subagents](https://code.claude.com/docs/en/sub-agents), checked 2026-08-08, re-checked 2026-08-10 (`SRC-WERPC-046`).
- [Agency Agents pinned tree](https://github.com/msitarzewski/agency-agents/tree/ebe9c99acb5c96f9468de368d8bead775387d1a7), [MIT license](https://github.com/msitarzewski/agency-agents/blob/ebe9c99acb5c96f9468de368d8bead775387d1a7/LICENSE), and inspected converter/installer sources, checked 2026-08-08, re-checked 2026-08-10 (`SRC-WERPC-047`–`048`).
- The [source ledger](source-coverage.md#source-register) records claim limits and refresh triggers.

## Review and Freshness

Refresh after a roster, adapter, evaluation, tool/sandbox boundary, Agency
Agents pin/license, or upstream conversion/install-script change. Re-resolve
the full commit before any reuse. Do not infer provider runtime behavior or
prompt quality from static files or this dated comparison.

External sources were re-checked on 2026-08-10 and no cited claim changed. The
Agency Agents result is the strongest evidence in this pack: the repository's
default branch head is byte-identical to the pinned commit
`ebe9c99acb5c96f9468de368d8bead775387d1a7`, the comparison reports zero commits
ahead or behind, and the last push is dated 2026-08-06, before the original
check. No agent, structure, converter, installer, or license change has landed,
and the MIT license at the pin is unchanged. The two provider subagent pages
publish no last-modified date, so their unchanged result is content identity
rather than a publisher signal and is a weaker class of evidence than the pinned
commit comparison.

### 2026-08-11 Partial/DEFER incremental refresh

This bounded increment was executed and checked on **2026-08-12**; the heading
retains the approved package date and does not backdate the source review. It
does not refresh the pinned Agency Agents comparison because REQ-WERPC-026
admits only the current official provider-agent delta and the pinned catalog is
not needed to answer it.

#### REQ-WERPC-026 agent-contract delta

| Current official contract                                                                                                                       | Adopted scope                                                                                                                                                                                                                                                                                                           | Rejected inference and uncertainty                                                                                                                                                           | Refresh trigger                                                                                               |
| ----------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| [OpenAI Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents), current page with no publisher date, checked 2026-08-12 | Project files under `.codex/agents/` require `name`, `description`, and `developer_instructions`; custom agents may override model/reasoning and sandbox settings, while omitted settings inherit according to the documented chain. Explicit requests or applicable project/skill instructions can trigger delegation. | A documented load path or inheritance rule does not prove this worktree's files were discovered, a child was spawned, an approval was granted, or a tool ran.                                | OpenAI changes project-agent discovery, schema, inheritance, orchestration, sandbox, or approvals.            |
| [Anthropic Claude Code subagents](https://code.claude.com/docs/en/sub-agents), current page with no publisher date, checked 2026-08-12          | Project Markdown agents can scope tools, disallowed tools, MCP servers, permission modes, hooks, skills, isolation, and persistent memory; main-session and subagent contexts have distinct loading rules.                                                                                                              | Optional product fields are not mandatory local fields. The page does not prove tracked adapter discovery, effective deny/allow order, delegation, isolation, memory use, or result quality. | Anthropic changes agent discovery, fields, parent precedence, tool/permission behavior, isolation, or memory. |

**As-Is:** `contracts/harness-contract.json` remains the semantic owner for 12
roles and 48 current projections across `.agents/agents/`,
`.claude/agents/`, `.codex/agents/`, and `.gemini/agents/`.
`contracts/agent-evaluations.json` has 12 repository-static evaluation suites;
its evaluation and admission dispositions remain `DEFER`. Sampled adapters
retain the same bounded responsibilities, guardrails, handoff, and postflight
semantics while using surface-specific metadata.

**Gap and bounded target:** Current provider schemas expose more optional
capability and inheritance controls than the common roster contract needs.
That is not evidence that the local adapters are incomplete or effective.
Keep role semantics provider-neutral and add a provider-specific field only
through a separately approved roster/adapter change tied to a concrete gap.
Native discovery, delegation, tool execution, effective permission, model
resolution, and effectiveness require separate provider-runtime evidence.

**Final disposition:** `Partial`. Evidence depth is official public agent
contract plus exact repo-static roster, contract, evaluation, and adapter
selectors. Owner: Stage 00 harness and roster-admission contracts. Refresh when
a cited provider agent contract or the local roster/adapter contract changes.

### 2026-08-14 consistency and Partial re-observation

This bounded increment re-observed the workspace and re-checked external
sources for `REQ-WERPC-026` only, checked on **2026-08-14**. It continues not
to re-verify the pinned Agency Agents comparison: on 2026-08-11 that was
because the pinned catalog was not needed to answer the official-provider-delta
question; on 2026-08-14 it is additionally because this package has no
explicit human approval for a GitHub remote query, so
`github.com/msitarzewski/agency-agents` was not fetched. No provider was
invoked and no cluster was inspected.

#### REQ-WERPC-026 workspace and source consistency check

**Workspace delta:** `no-change`. `contracts/harness-contract.json` still
records exactly 12 roles and 48 current projections across `.agents/agents/`,
`.claude/agents/`, `.codex/agents/`, and `.gemini/agents/`, at contract
version `1.0.0`.

**External result:** both sources were reachable and `unchanged` against
their 2026-08-12 adopted scope.

| Source                                                                                 | Result      | Note                                                                                                                                                                                                                                                                                                     |
| -------------------------------------------------------------------------------------- | ----------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [OpenAI Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) | `unchanged` | Project-file required fields, agent-file-first override, and the inheritance chain for omitted settings still match. No publisher date.                                                                                                                                                                  |
| [Anthropic Claude Code subagents](https://code.claude.com/docs/en/sub-agents)          | `unchanged` | Project Markdown agent frontmatter (`tools`, `disallowedTools`, `model`, `permissionMode`, `mcpServers`, `hooks`, `skills`, `memory`, `isolation`, plus newer `background`/`effort`/`color`/`initialPrompt` fields) and the distinct main-session/subagent loading rules still match. No publisher date. |

**As-Is:** Unchanged. `contracts/harness-contract.json` remains the semantic
owner for 12 roles and 48 current projections; `contracts/agent-evaluations.json`
still has 12 repository-static evaluation suites with `DEFER` admission
dispositions.

**Gap and bounded target:** Unchanged. Current provider schemas still expose
more optional capability/inheritance controls than the common roster contract
needs; that is not evidence of local incompleteness. Native discovery,
delegation, tool execution, effective permission, model resolution, and
effectiveness require separate provider-runtime evidence.

**Missing evidence:** authenticated delegation/execution trace per tracked
adapter. **Owning authority:** Stage 00 harness and roster-admission
contracts. **Safe boundary:** a separately approved, non-secret
provider-runtime observation of the exact adapter; no bulk import, installer
execution, or unreviewed prompt copying. **Refresh trigger:** a cited
provider agent contract, the local roster/adapter contract, or the Agency
Agents pin changes.

**Final disposition:** `Partial`, unchanged from the 2026-08-12 baseline. No
promotion. New source registered: `SRC-WERPC-074`. New claim registered:
`CLM-WERPC-010-02`.

### 2026-08-20 full-corpus reverification

This increment re-observed the two agent-system rows at workspace baseline
`8d8c8e5634fe939f8daaf041fbf5dfb444ed4a9c`. The allocation slice assigns no
new source or claim ID. General provider-agent capability and the pinned
Agency Agents comparison remain separate from local adoption authority.

#### REQ-WERPC-026 governed agent-system re-observation

- **Sources and external result:** `unchanged`; `SRC-WERPC-045` and
  `SRC-WERPC-046` were re-observed on 2026-08-20. The official Codex and
  Claude subagent pages still document custom-agent configuration, model/tool
  controls, permissions, and scoped delegation without proving local use.
- **Workspace selector and result:** `confirmed` at
  `ai-agents-and-agency-agents.md#ai-agent-systems-baseline`. The baseline
  still records a twelve-role, four-provider-surface roster with bounded
  ownership, review, validation, rollback, and handoff contracts.
- **As-Is, gap, and target:** the local agent system remains `Partial` at
  public-documentation depth because provider discovery, effective
  permissions, delegated execution, isolation, and role effectiveness are
  unobserved. Keep common role semantics provider-neutral and provider schema
  at the adapter edge.
- **Evidence boundary:** blocking class and retained boundary are
  `provider-runtime` / `DEFER`. Static adapter parity or provider fields do not
  prove discovery, permissions, model resolution, tool use, or task quality.
- **Owner, safe follow-up, and trigger:** owner is this reference and the Stage
  00 harness/roster-admission contracts. After approval, use a read-only,
  non-secret canary for one exact agent adapter with no external writes.
  Refresh when a cited provider agent schema, inheritance, tool, permission,
  isolation, model, or local roster contract changes.

#### REQ-WERPC-027 Agency Agents comparison re-observation

- **Sources and external result:** `unchanged`; `SRC-WERPC-047` and
  `SRC-WERPC-048` were re-observed on 2026-08-20 against pinned commit
  `ebe9c99acb5c96f9468de368d8bead775387d1a7`. The pinned tree, MIT license,
  and scripts remain reachable; no release superseded the fixed comparison.
- **Workspace selector and result:** `confirmed` at
  `ai-agents-and-agency-agents.md#agency-agents-baseline`. The canonical local
  roster remains the adapted surface; the upstream catalog remains comparison
  evidence only.
- **As-Is, gap, and target:** the fixed-pin source comparison remains
  `Verified` at public-documentation depth. It does not establish current
  default-branch permanence, prompt quality, conversion or install success,
  provider support, security, or admission. Continue to require explicit
  license, security, roster, adapter, evaluation, and reviewer gates before
  reuse.
- **Evidence boundary:** blocking class is `none`, but no local-adoption or
  runtime claim is made. Catalog availability and script presence do not
  authorize prompt copying or script execution.
- **Owner, safe follow-up, and trigger:** owner is this reference. If reuse is
  proposed, separately review license, security, overwrite safety, and role
  admission before executing a converter or installer. Refresh when the pin,
  license, inspected scripts, or adoption policy changes.

## Related Documents

- [Model routing](agent-model-routing-and-configuration.md)
- [Memory tiers](agent-memory-tiers-and-management.md)
- [Source ledger](source-coverage.md)
- [Agent Registry](../../../../.agents/registry.json)
