# AI Agent Governance Hub

> Central governance entry point for AI agents operating in `hy-home.k8s`.

## Overview

This directory is the policy SSoT for local agent execution in `hy-home.k8s`.
It also routes the human SDLC flow and lifecycle policy without duplicating
the Stage 99 machine registry.
It keeps gateway files thin by hosting durable rules, execution checklists,
scope routing, provider notes, reusable memory, shared hook scripts, model
policy, and the canonical runtime catalog used by Claude-native
`.claude/agents/*.md`, Codex-native `.codex/agents/*.toml`, repository-local
runtime baselines and shared/local `.agents/**` assets. Gemini CLI native
`.gemini/**` adoption remains a separate `DEFER` boundary.

### Stage Readers

This README is primarily for:

- Repository maintainers
- Agent authors
- Runtime operators
- AI agents loading governance context

## Stage Contract

### In Scope

- Governance rules and execution checklists
- Scope-specific policy for agent work
- Provider-specific notes for supported engines
- Canonical runtime roster and subagent protocol
- Reusable operational memory entries
- Documentation language, template routing, and drift garbage-collection policy
- Human SDLC flow and document-lifecycle policy

### Out of Scope

- Product, architecture, feature-local execution, operations, reference, archive, and template SSoT under `docs/01.requirements`, `docs/02.architecture`, `docs/03.specs`, `docs/05.operations`, `docs/90.references`, `docs/98.archive`, and `docs/99.templates`
- Runtime bridge content under `.claude/**`
- Human-facing project onboarding outside this governance area

### Current Adapter Surface Matrix

| Surface | Ownership and current meaning |
| --- | --- |
| `.claude/agents/*.md` | Claude native role definitions; `.claude/CLAUDE.md` is the repository-local Claude baseline. |
| `.codex/agents/*.toml` | Codex native role definitions; `.codex/CODEX.md` is the repository-local Codex baseline. |
| `.agents/agents/*.md` | Local/Antigravity role adapters, not Gemini CLI native roles. |
| `.agents/{skills,workflows,output-styles}/` | Shared SSoT exposed through the tracked Claude/Codex symlink views. |
| `.codex/hooks.json`, `.agents/hooks.json` | Context/validation wiring; the latter is local/Antigravity wiring. |
| `.gemini/agents/**`, `.gemini/settings.json` | Gemini CLI native project surfaces tracked as repo-static evidence; runtime discovery, event delivery, auth, and model resolution remain `DEFER` or `ABSENT`. |

## Document Index

The document-profile registry owns this exhaustive path set. Each lifecycle
cell mirrors the target document's frontmatter and is validated for exact path,
status, uniqueness, and order.

### Current Governance Authority Index

| Document | Lifecycle |
| --- | --- |
| [`harness-catalog.md`](harness-catalog.md) | `active` |
| [`model-policy.md`](model-policy.md) | `active` |
| [`document-lifecycle.md`](policies/document-lifecycle.md) | `active` |
| [`claude.md`](providers/claude.md) | `active` |
| [`codex.md`](providers/codex.md) | `active` |
| [`gemini.md`](providers/gemini.md) | `active` |
| [`agentic.md`](rules/agentic.md) | `active` |
| [`approval-boundaries.md`](rules/approval-boundaries.md) | `active` |
| [`bootstrap.md`](rules/bootstrap.md) | `active` |
| [`document-authoring.md`](rules/document-authoring.md) | `active` |
| [`git-workflow.md`](rules/git-workflow.md) | `active` |
| [`persona.md`](rules/persona.md) | `active` |
| [`postflight-checklist.md`](rules/postflight-checklist.md) | `active` |
| [`preflight-checklist.md`](rules/preflight-checklist.md) | `active` |
| [`quality-standards.md`](rules/quality-standards.md) | `active` |
| [`standards.md`](rules/standards.md) | `active` |
| [`architecture.md`](scopes/architecture.md) | `active` |
| [`backend.md`](scopes/backend.md) | `active` |
| [`docs.md`](scopes/docs.md) | `active` |
| [`frontend.md`](scopes/frontend.md) | `active` |
| [`infra.md`](scopes/infra.md) | `active` |
| [`meta.md`](scopes/meta.md) | `active` |
| [`ops.md`](scopes/ops.md) | `active` |
| [`product.md`](scopes/product.md) | `active` |
| [`qa.md`](scopes/qa.md) | `active` |
| [`security.md`](scopes/security.md) | `active` |
| [`sdlc.md`](sdlc.md) | `active` |
| [`subagent-protocol.md`](subagent-protocol.md) | `active` |

### Directory Map

Key folders in this area:

- `rules/`: global policy, document authoring, and execution checklists
- `scopes/`: layer-specific execution rules
- `providers/`: provider-specific notes
- `hooks/`: shared lifecycle/edit hook scripts invoked by provider wiring
- `memory/`: agent progress ledger and reusable operational lessons
- `policies/`: lifecycle and SDLC norms that apply across document families

```text
docs/00.agent-governance/
├── rules/              # Global policy, document authoring, and checklists
├── scopes/             # Layer-specific execution rules
├── providers/          # Provider-specific notes for Claude, Gemini, and gateways
├── hooks/              # Shared lifecycle/edit hook scripts reused by providers
├── memory/             # Reusable lessons and operational findings
├── policies/           # Human lifecycle and SDLC norms
├── sdlc.md             # Requirements-to-operations flow
├── harness-catalog.md  # Canonical runtime roster for local agents and skills
├── model-policy.md     # Cross-provider model tier and effort policy
├── subagent-protocol.md
└── README.md           # This file
```

## Authoring Workflow

1. Start from repository gateway files: `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md`.
2. Follow the JIT loading order in `rules/bootstrap.md` and `rules/preflight-checklist.md`.
3. Use `docs/99.templates/` when creating or restructuring governance documents.
4. Use `rules/document-authoring.md` for stage selection, language,
   Template-First execution, lifecycle checks, and validation handoff.
5. Treat repeated agent failures as harness feedback: update the smallest
   relevant rule, prompt/skill, hook, validator, template, README index, or
   memory entry.
6. Update `harness-catalog.md` and this README in the same change set when the runtime roster changes.

### Relative Link Rules

Links in this README are relative to `docs/00.agent-governance/`.

- Governance rules use `rules/<file>.md`.
- Scope and provider notes use `scopes/<file>.md` and `providers/<file>.md`.
- Repository-root runtime files use `../../<path>`.
- Template links use `../99.templates/templates/**/<template>`.

### Governance Entry Points

- [Model Policy](model-policy.md)
- [Preflight Checklist](rules/preflight-checklist.md)
- [Postflight Checklist](rules/postflight-checklist.md)
- [Document Authoring Policy](rules/document-authoring.md)
- [SDLC Flow](sdlc.md)
- [Document Lifecycle Policy](policies/document-lifecycle.md)
- [Local Harness Catalog](harness-catalog.md)
- [Subagent Protocol](subagent-protocol.md)
- [Codex Provider Notes](providers/codex.md)

## Related Documents

- [AGENTS.md](../../AGENTS.md)
- [Runtime Baseline](../../.claude/CLAUDE.md)
- [Codex Runtime Baseline](../../.codex/CODEX.md)
- [Claude Provider Notes](providers/claude.md)
- [Codex Provider Notes](providers/codex.md)
- [Gemini Provider Notes](providers/gemini.md)

### Examples

- Add a new execution rule under `rules/`.
- Add a provider note under `providers/`.
- Add work progress and reusable memory under `memory/progress.md` using `docs/99.templates/templates/governance/progress.template.md`.
