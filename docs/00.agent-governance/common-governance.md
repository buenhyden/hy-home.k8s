---
title: 'Reference: Common Governance & Mappings'
type: governance/reference
status: active
owner: platform
updated: 2026-07-29
---

# Reference: Common Governance & Mappings

## Overview

> Use this document to understand the common governance structure across all AI agents operating in `hy-home.k8s`.

This document defines the common governance concepts, cross-platform mappings,
Memory, QA, and CI/static validation policies, and support matrix for AI agents (Gemini, Claude,
Codex) operating in `hy-home.k8s`. Shared skills, workflows, and output-style
content use `.agents/` as their provider-neutral Single Source of Truth (SSoT).
The `.agents/agents/*.md` files are local/Antigravity role adapters, while
`.claude/agents/*.md`, `.codex/agents/*.toml`, and `.gemini/agents/*.md` are
provider-native role adapter surfaces. Static role parity across all four
surfaces is repository evidence only, not evidence of four-runtime discovery
or enforcement.

### Purpose

To provide a unified understanding of agent concepts and their implementation across different agent runtimes.

### Reference Type

- Type: durable-concept
- Source checked: 2026-07-28
- Refresh trigger: On new platform addition or hook restructuring.

## Authority Boundary

- **Authoritative for**:
  - Agent terminology
  - Platform mapping rules
  - High-level QA, Memory, and CI/static validation policies
- **Not authoritative for**:
  - Technical implementation of specific skills or hooks (see `docs/00.agent-governance/hooks/`)
  - Concrete model IDs and reasoning-effort values (see `harness-catalog.md` and `model-policy.md`)
  - Stage-to-template mapping details (see `docs/99.templates/support/template-routing.md` and `rules/document-stage-routing.md`)

### Scope

- Common agent concepts
- Directory mappings for `.agents/`, `.claude/`, `.codex/`, and `.gemini/`
- Policy requirements for operations

## Governance Context

### Definitions / Facts

- **Agent**: An entity assigned a specific persona (e.g., `k8s-implementer`) to perform tasks.
- **Skill**: A bundled capability, script, or knowledge set invoked by an agent to execute tasks.
- **Rule**: Guidelines and constraints the agent must strictly follow (e.g., coding standards).
- **Hook**: Trigger scripts (Session Start, Pre-edit, Post-validate) for context injection and validation.
- **Subagent**: A specialized agent invoked by a supervisor to delegate domain-specific sub-tasks.
- **Output Style**: Formatting, tone, and markdown conventions for generating files.
- **Workflow**: Procedural pipelines defining multi-step tasks or agent interactions.
- **Memory**: Persistent storage (`docs/00.agent-governance/memory/`) for lessons learned and context.
- **QA / CI**: Automated pipelines enforcing code quality, templates, and Kubernetes manifest validity.

### Platform Mapping

| Concept | Local/Antigravity | Claude | Codex | Gemini CLI |
| --- | --- | --- | --- | --- |
| **Shared Content SSoT** | `.agents/` (primary) | `.claude/{skills,workflows,output-styles}` symlinks | `.codex/{skills,workflows,output-styles}` symlinks | Stage 00 pointers only; no native shared-content mirror |
| **Agent Definition** | `.agents/agents/*.md` | `.claude/agents/*.md` | `.codex/agents/*.toml` | `.gemini/agents/*.md` |
| **Skills** | `.agents/skills/` | `.claude/skills/` | `.codex/skills/` | Native consumption not established |
| **Rules** | `.agents/rules/` plus Stage 00 rules | Stage 00 `rules/**` plus provider imports | Stage 00 `rules/**` plus `.codex/rules/` placeholder/adapter surface | Root `GEMINI.md` plus provider pointers; native policy loading unproved |
| **Hooks Config** | `.agents/hooks.json` (behavioral wiring) | `.claude/settings.json` | `.codex/hooks.json` | `.gemini/settings.json` (minimal agent-settings surface only) |
| **Hooks Scripts** | `docs/00.agent-governance/hooks/*.sh` | `docs/00.agent-governance/hooks/*.sh` | `docs/00.agent-governance/hooks/*.sh` | Event delivery not configured or proved |
| **Workflows** | `.agents/workflows/` | `.claude/workflows/` | `.codex/workflows/` | Native consumption not established |
| **Output Styles** | `.agents/output-styles/` | `.claude/output-styles/` | `.codex/output-styles/` | Native consumption not established |

## Current Contract

### Canonical Adapter Ownership

| Layer | Canonical Owner | Provider Adapter Rule |
| --- | --- | --- |
| Governance rules, checklists, documentation routing | `docs/00.agent-governance/rules/**` | Provider files import or point here instead of copying durable policy. |
| Model/tier vocabulary | `harness-catalog.md` and `model-policy.md` | Provider agent files declare concrete models from the catalog and do not create separate tier names. |
| Shared skills, workflows, and output-style content | `.agents/{skills,workflows,output-styles}/` | `.claude/**` and `.codex/**` expose symlinked views where supported. |
| Role adapter surfaces | `.agents/agents/*.md` (local/Antigravity), `.claude/agents/*.md` (Claude native), `.codex/agents/*.toml` (Codex native), `.gemini/agents/*.md` (Gemini native syntax) | Agent roles stay statically aligned, while metadata, model, tool, and permission syntax remains surface-specific. |
| Hook scripts | `docs/00.agent-governance/hooks/*.sh` | `.claude/settings.json` wires Claude native settings/hooks; `.codex/hooks.json` is Codex context/validation wiring; `.agents/hooks.json` is local/Antigravity behavioral wiring and is not Gemini CLI native configuration. |
| Execution evidence | `docs/04.execution/tasks/**` and `docs/00.agent-governance/memory/progress.md` | Provider handoff text links to evidence rather than embedding separate ledgers. |

### Gemini CLI Native Boundary

Gemini CLI native-syntax project agents and minimal project settings are
tracked at `.gemini/agents/**` and `.gemini/settings.json`. The settings file
contains only its schema pointer and an empty `agents.overrides` object; exact
candidate models remain in the agent frontmatter and model-fitness contract.
These files prove repository-static schema and roster parity only. Gemini CLI
installation, native discovery, event delivery, policy loading,
authentication, model resolution, and execution remain `ABSENT` or `DEFER`;
`.agents/**` and tracked `.gemini/**` files must not be promoted into evidence
for those runtime behaviors.

### Policies

- **Memory Policy**: Agents must log lessons learned and persistent context in `docs/00.agent-governance/memory/` and review them before initiating work.
- **GitOps-First QA**: Agents cannot modify the production cluster directly (`no-kubectl-mutation`). All changes must go through PR and CI/static validation.
- **Hook and Validation Wiring**:
  - **Pre-flight/edit**: Surface templates and structural rules where the provider runtime supports event wiring.
  - **Post-flight/validate**: Run `scripts/validate-repo-quality-gates.sh` to ensure compliance.
  - Claude has the native permission gate; Codex hook JSON is context/validation wiring, and `.agents/hooks.json` is local/Antigravity behavioral wiring rather than Gemini CLI native configuration.

### Support Matrix

| Feature | Local/Antigravity | Claude | Codex | Gemini CLI | Status |
| --- | --- | --- | --- | --- | --- |
| **Rules / Skills / Workflows** | ✅ Shared content | ✅ Symlink/import view | ✅ Symlink/import view | ⚠️ Stage 00 pointers only | Repository structure exists; provider-native consumption remains evidence-specific |
| **Centralized Hooks (Pre/Post)** | ⚠️ Behavioral wiring | ✅ Native permission + event wiring | ⚠️ Context/validation wiring | ❌ Not configured | Shared scripts live in `docs/00.agent-governance/hooks/`; only Claude has a native permission gate |
| **Subagent Protocol** | ⚠️ Local adapter | ✅ Native agent frontmatter | ⚠️ TOML adapter/config | ⚠️ Native-syntax repo surface | Four-surface static parity is validated; runtime discovery and enforcement require provider evidence |
| **Shared Repository Memory** | ✅ Markdown contract | ✅ Markdown contract | ✅ Markdown contract | ✅ Markdown contract | Repository memory is authoritative; provider-local recall is auxiliary only |
| **Output Style Enforcement** | ⚠️ Behavioral | ✅ Native output-style files | ⚠️ Behavioral | ❌ Not established | Shared style content exists; native enforcement differs by provider |

## Validation and Refresh

### Sources

- Official capability basis reconciled through the fixed 2026-07-10 cutoff and
  checked again on 2026-07-28: Codex `AGENTS.md`,
  subagents, CLI/config/approval modes; Claude settings, hooks, subagents;
  Gemini CLI commands and hierarchical memory; GitHub Actions.
- External agent-roster market scan checked on 2026-07-06:
  <https://github.com/msitarzewski/agency-agents>.
- Workspace analysis and current provider adapter files.

### Review and Freshness

- Review cadence: on dependency bump or agent framework update
- Last reviewed: 2026-07-29
- Next review trigger: provider agent-schema, model-catalog, or runtime-evidence change

## Related Documents

- **AGENTS.md**: `../../AGENTS.md`
- **Subagent Protocol**: `subagent-protocol.md`
