# Reference: Common Governance & Mappings

> Use this document to understand the common governance structure across all AI agents operating in `hy-home.k8s`.

---

## Overview

This document defines the common governance concepts, cross-platform mappings, Memory/QA/CI/CD policies, and support matrix for AI agents (Gemini, Claude, Codex) operating in `hy-home.k8s`. Shared skills, workflows, and output-style content use `.agents/` as their Single Source of Truth (SSoT), while provider-native agent files remain aligned mirrors.

## Purpose

To provide a unified understanding of agent concepts and their implementation across different agent runtimes.

## Reference Type

- Type: durable-concept
- Source checked: 2026-05-30
- Refresh trigger: On new platform addition or hook restructuring.

## Authority Boundary

- **Authoritative for**:
  - Agent terminology
  - Platform mapping rules
  - High-level QA, Memory, and CI/CD policies
- **Not authoritative for**:
  - Technical implementation of specific skills or hooks (see `docs/00.agent-governance/hooks/`)

## Scope

- Common agent concepts
- Directory mappings for `.agents/`, `.claude/`, and `.codex/`
- Policy requirements for operations

## Definitions / Facts

- **Agent**: An entity assigned a specific persona (e.g., `k8s-implementer`) to perform tasks.
- **Skill**: A bundled capability, script, or knowledge set invoked by an agent to execute tasks.
- **Rule**: Guidelines and constraints the agent must strictly follow (e.g., coding standards).
- **Hook**: Trigger scripts (Session Start, Pre-edit, Post-validate) for context injection and validation.
- **Subagent**: A specialized agent invoked by a supervisor to delegate domain-specific sub-tasks.
- **Output Style**: Formatting, tone, and markdown conventions for generating files.
- **Workflow**: Procedural pipelines defining multi-step tasks or agent interactions.
- **Memory**: Persistent storage (`docs/00.agent-governance/memory/`) for lessons learned and context.
- **QA / CI/CD**: Automated pipelines enforcing code quality, templates, and Kubernetes manifest validity.

## Platform Mapping

| Concept | Gemini (Antigravity) | Claude | Codex |
| --- | --- | --- | --- |
| **Shared Content SSoT** | `.agents/` (Primary) | `.claude/{skills,workflows,output-styles}` symlinks | `.codex/{skills,workflows,output-styles}` symlinks |
| **Agent Definition** | `.agents/agents/*.md` | `.claude/agents/*.md` | `.codex/agents/*.toml` |
| **Skills** | `.agents/skills/` | `.claude/skills/` | `.codex/skills/` |
| **Rules** | `.agents/rules/` | `.claude/rules/` | `.codex/rules/` |
| **Hooks Config** | `.agents/hooks.json` | `.claude/settings.json` | `.codex/hooks.json` |
| **Hooks Scripts** | `docs/00.agent-governance/hooks/*.sh` | `docs/00.agent-governance/hooks/*.sh` | `docs/00.agent-governance/hooks/*.sh` |
| **Workflows** | `.agents/workflows/` | `.claude/workflows/` | `.codex/workflows/` |
| **Output Styles** | `.agents/output-styles/` | `.claude/output-styles/` | `.codex/output-styles/` |

## Policies

- **Memory Policy**: Agents must log lessons learned and persistent context in `docs/00.agent-governance/memory/` and review them before initiating work.
- **GitOps-First QA**: Agents cannot modify the production cluster directly (`no-kubectl-mutation`). All changes must go through PR and CI/CD validation.
- **Hook Enforcement**:
  - **Pre-flight/edit**: Enforce templates and structural rules.
  - **Post-flight/validate**: Run `scripts/validate-repo-quality-gates.sh` to ensure compliance.

## Support Matrix

| Feature | Gemini (Antigravity) | Claude | Codex | Status |
| --- | --- | --- | --- | --- |
| **Rules / Skills / Workflows** | ✅ Supported | ✅ Supported | ✅ Supported | Supported via `.agents/` shared content plus provider shims |
| **Centralized Hooks (Pre/Post)** | ⚠️ Wiring/behavioral (`hooks.json`) | ✅ Native (`settings.json`) | ⚠️ Wiring/behavioral (`hooks.json`) | Supported via `docs/00.agent-governance/hooks/`; only Claude has a native permission gate |
| **Subagent Protocol** | ⚠️ Partial (Prompt-reliant) | ✅ Fully Supported | ⚠️ Partial | Pending |
| **Cross-Platform Memory DB** | ❌ Unsupported | ❌ Unsupported | ❌ Unsupported | Unsupported (Fallback to Markdown) |
| **Output Style Enforcement** | ⚠️ Tone/behavioral | ✅ Native output-style files | ⚠️ Tone/behavioral | Shared style content exists; native enforcement differs by provider |

## Sources

- Original prompt requirements and workspace analysis.

## Review and Freshness

- Review cadence: on dependency bump or agent framework update
- Last reviewed: 2026-05-30
- Next review trigger: Antigravity Subagent upgrade

## Related Documents

- **AGENTS.md**: `../../AGENTS.md`
- **Subagent Protocol**: `subagent-protocol.md`
