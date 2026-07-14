---
title: 'Reference: Common Governance & Mappings'
type: governance/reference
status: active
owner: platform
updated: 2026-07-14
---

# Reference: Common Governance & Mappings

## Overview

> Use this document to understand the common governance structure across all AI agents operating in `hy-home.k8s`.

This document defines the common governance concepts, cross-platform mappings,
Memory, QA, and CI/static validation policies, and support matrix for AI agents (Gemini, Claude,
Codex) operating in `hy-home.k8s`. Shared skills, workflows, and output-style
content use `.agents/` as their provider-neutral Single Source of Truth (SSoT),
while `.agents/agents/*.md`, `.claude/agents/*.md`, and
`.codex/agents/*.toml` are provider-native role adapters.

### Purpose

To provide a unified understanding of agent concepts and their implementation across different agent runtimes.

### Reference Type

- Type: durable-concept
- Source checked: 2026-07-06
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
- Directory mappings for `.agents/`, `.claude/`, and `.codex/`
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

| Concept | Gemini (Antigravity) | Claude | Codex |
| --- | --- | --- | --- |
| **Shared Content SSoT** | `.agents/` (Primary) | `.claude/{skills,workflows,output-styles}` symlinks | `.codex/{skills,workflows,output-styles}` symlinks |
| **Agent Definition** | `.agents/agents/*.md` | `.claude/agents/*.md` | `.codex/agents/*.toml` |
| **Skills** | `.agents/skills/` | `.claude/skills/` | `.codex/skills/` |
| **Rules** | `.agents/rules/` plus Stage 00 rules | Stage 00 `rules/**` plus provider imports | Stage 00 `rules/**` plus `.codex/rules/` placeholder/adapter surface |
| **Hooks Config** | `.agents/hooks.json` | `.claude/settings.json` | `.codex/hooks.json` |
| **Hooks Scripts** | `docs/00.agent-governance/hooks/*.sh` | `docs/00.agent-governance/hooks/*.sh` | `docs/00.agent-governance/hooks/*.sh` |
| **Workflows** | `.agents/workflows/` | `.claude/workflows/` | `.codex/workflows/` |
| **Output Styles** | `.agents/output-styles/` | `.claude/output-styles/` | `.codex/output-styles/` |

## Current Contract

### Canonical Adapter Ownership

| Layer | Canonical Owner | Provider Adapter Rule |
| --- | --- | --- |
| Governance rules, checklists, documentation routing | `docs/00.agent-governance/rules/**` | Provider files import or point here instead of copying durable policy. |
| Model/tier vocabulary | `harness-catalog.md` and `model-policy.md` | Provider agent files declare concrete models from the catalog and do not create separate tier names. |
| Shared skills, workflows, and output-style content | `.agents/{skills,workflows,output-styles}/` | `.claude/**` and `.codex/**` expose symlinked views where supported. |
| Provider-native role adapters | `.agents/agents/*.md`, `.claude/agents/*.md`, `.codex/agents/*.toml` | Agent roles stay aligned, while metadata, model, tool, and permission syntax remains provider-specific. |
| Hook scripts | `docs/00.agent-governance/hooks/*.sh` | `.claude/settings.json` wires Claude native settings/hooks; `.agents/hooks.json` and `.codex/hooks.json` are context/validation wiring, not native permission gates equivalent to Claude settings. |
| Execution evidence | `docs/04.execution/tasks/**` and `docs/00.agent-governance/memory/progress.md` | Provider handoff text links to evidence rather than embedding separate ledgers. |

### Policies

- **Memory Policy**: Agents must log lessons learned and persistent context in `docs/00.agent-governance/memory/` and review them before initiating work.
- **GitOps-First QA**: Agents cannot modify the production cluster directly (`no-kubectl-mutation`). All changes must go through PR and CI/static validation.
- **Hook and Validation Wiring**:
  - **Pre-flight/edit**: Surface templates and structural rules where the provider runtime supports event wiring.
  - **Post-flight/validate**: Run `scripts/validate-repo-quality-gates.sh` to ensure compliance.
  - Claude has the native permission gate; Gemini and Codex hook JSON files are context/validation wiring.

### Support Matrix

| Feature | Gemini (Antigravity) | Claude | Codex | Status |
| --- | --- | --- | --- | --- |
| **Rules / Skills / Workflows** | ✅ Supported | ✅ Supported | ✅ Supported | Supported via `.agents/` shared content plus provider shims |
| **Centralized Hooks (Pre/Post)** | ⚠️ Wired/behavioral (`hooks.json`) | ✅ Native permission + event wiring (`settings.json`) | ⚠️ Wired/behavioral (`hooks.json`) | Shared scripts live in `docs/00.agent-governance/hooks/`; only Claude has a native permission gate |
| **Subagent Protocol** | ⚠️ Adapter/behavioral | ✅ Native tools frontmatter | ⚠️ TOML adapter/config-based | Ready when provider-native role adapters pass repository validation; native tool enforcement differs by provider |
| **Cross-Platform Memory DB** | ❌ Unsupported | ❌ Unsupported | ❌ Unsupported | Unsupported (Fallback to Markdown) |
| **Output Style Enforcement** | ⚠️ Tone/behavioral | ✅ Native output-style files | ⚠️ Tone/behavioral | Shared style content exists; native enforcement differs by provider |

## Validation and Refresh

### Sources

- Official capability basis checked on 2026-07-06: Codex `AGENTS.md`,
  subagents, CLI/config/approval modes; Claude settings, hooks, subagents;
  Gemini CLI commands and hierarchical memory; GitHub Actions.
- External agent-roster market scan checked on 2026-07-06:
  <https://github.com/msitarzewski/agency-agents>.
- Workspace analysis and current provider adapter files.

### Review and Freshness

- Review cadence: on dependency bump or agent framework update
- Last reviewed: 2026-07-06
- Next review trigger: Antigravity Subagent upgrade

## Related Documents

- **AGENTS.md**: `../../AGENTS.md`
- **Subagent Protocol**: `subagent-protocol.md`
