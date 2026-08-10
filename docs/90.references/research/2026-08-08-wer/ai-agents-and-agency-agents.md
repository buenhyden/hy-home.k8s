---
title: 'Reference: AI Agents and Agency-Agents'
type: content/reference
status: active
owner: platform
updated: 2026-08-10
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

The harness catalog, roster-admission contract, provider adapters, and
evaluation contracts own local role and admission truth. External catalogs are
comparison evidence, not automatic admission authority. Tracked adapters prove
declared configuration only; discovery, authentication, tool enforcement,
delegation, and effectiveness remain `DEFER` without matching runtime evidence.

## Scope

It covers the agent-system control plane, the Agency Agents pin and comparison,
and an adopt/adapt/reject decision rule. Model selection and memory controls
are primary-owned by the sibling references.

## Definitions / Facts

### AI-agent-systems baseline

The workspace has a repository-static 12-role, four-provider-surface roster
described by the [harness catalog](../../../00.agent-governance/harness-catalog.md)
and `contracts/harness-contract.json`. Roles define bounded ownership; their
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

| Upstream assertion or asset | Supported observation | Not established |
| --- | --- | --- |
| Persona catalog | Markdown role prompts and category layout exist at the pin. | Task fitness, quality, safety, or provider-native discovery. |
| Conversion/install scripts | Script source transforms/copies files. | Safe overwrite behavior, successful conversion, installation, or runtime consumption. |
| MIT license | License text exists at the pin. | License counsel, attribution plan, or approval to copy content. |
| README marketing | It is upstream author prose. | Production readiness, automatic update behavior, or a workspace admission decision. |

### Adopt, adapt, or reject rule

| Decision | Required condition | Current result |
| --- | --- | --- |
| Adopt | The exact role closes a documented workspace gap; license, security, roster-admission, provider-adapter, evaluation, and reviewer gates approve it. | No candidate is adopted. |
| Adapt | Only bounded role language is useful; repository rules, tool/sandbox limits, evidence lanes, and local canonical owners replace external assumptions. | Existing local roles remain the canonical adapted roster. |
| Reject / defer | The proposal duplicates an existing role, assumes unapproved tools/authority, lacks a benchmark, or requires runtime proof not collected. | Bulk import, installer execution, and unreviewed prompt copying are rejected/deferred. |

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

## Sources

- [OpenAI Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents), checked 2026-08-08, re-checked 2026-08-10 (`SRC-WERPC-045`).
- [Anthropic Claude Code subagents](https://code.claude.com/docs/en/sub-agents), checked 2026-08-08, re-checked 2026-08-10 (`SRC-WERPC-046`).
- [Agency Agents pinned tree](https://github.com/msitarzewski/agency-agents/tree/ebe9c99acb5c96f9468de368d8bead775387d1a7), [MIT license](https://github.com/msitarzewski/agency-agents/blob/ebe9c99acb5c96f9468de368d8bead775387d1a7/LICENSE), and inspected converter/installer sources, checked 2026-08-08, re-checked 2026-08-10 (`SRC-WERPC-047`–`048`).
- The [source ledger](source-coverage-and-migration-ledger.md#source-register) records claim limits and refresh triggers.

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

## Related Documents

- [Model routing](agent-model-routing-and-configuration.md)
- [Memory tiers](agent-memory-tiers-and-management.md)
- [Source ledger](source-coverage-and-migration-ledger.md)
- [Harness catalog](../../../00.agent-governance/harness-catalog.md)
