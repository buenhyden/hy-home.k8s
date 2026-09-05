---
title: ".codex"
version: "0.1.0"
type: "common/readme-implementation"
status: "active"
owner: "platform"
updated: "2026-09-04"
---
# .codex

## Overview

`.codex/` is the projection surface the Codex runtime reads. The shared
meaning of roles and skills belongs to [Stage 00](../docs/00.agent-governance/README.md);
this directory expresses that meaning in the Codex TOML agent format and in a
thin local baseline.

These tracked files are repository configuration. They do not prove that Codex
discovered them, that a permission was enforced, or which model and reasoning
effort ran. Each of those needs separate runtime evidence.

### Audience

- Platform maintainers
- Governance owners
- Operators running the Codex runtime

### Scope

#### In Scope

- The Codex local baseline (`CODEX.md`)
- Per-role native projections (`agents/*.toml`)
- Explicit Stage 00 procedure reads from root AGENTS and role instructions

#### Out of Scope

- Shared role and skill definitions, owned by `docs/00.agent-governance/roles/registry.json`
- Execution policy, approval boundaries, and quality lanes, owned by `docs/00.agent-governance/policies/`
- Evidence of native discovery, permission enforcement, authentication, model resolution, or execution

## Structure

| Path | Responsibility |
| --- | --- |
| `CODEX.md` | Thin local baseline stating loading order and provider metadata |
| `agents/*.toml` | Native projections of the 12 roles, carrying `name`, `description`, `model`, `model_reasoning_effort`, and `developer_instructions` |

Each `developer_instructions` block directly references the canonical role,
registry, lifecycle, and required skill procedures. These are explicit reads;
no repository Codex skill registration or projection generator is provided.

## Configuration Boundary

- The root `AGENTS.md` is the Codex gateway and does not import the Claude
  gateway.
- Declarations here may narrow the common approval boundary but never widen it.
- Model and reasoning-effort values follow the capability tiers in
  [model selection](../docs/00.agent-governance/policies/model-selection.md);
  these files do not redefine what a tier means.
- Policy text is referenced, not copied into this directory.

## Validation

Run `python3 scripts/validate-agent-governance.py --root .` for the registry,
native metadata, direct role/procedure reads, permissions, and retired consumers.
Run `python3 scripts/qa.py full` for complete repository-static validation.

Tracked files under this directory stay English-only; `repository-quality`
enforces that.

## Operations

- Changing a role means updating `docs/00.agent-governance/roles/registry.json`,
  `docs/00.agent-governance/roles/<role>.md`, `.claude/agents/<role>.md`, and
  `.codex/agents/<role>.toml` in one change. Updating one side alone fails
  provider parity validation.
- Edit skill bodies under `docs/00.agent-governance/skills/`.
- Do not write new policy sentences into `developer_instructions`; reference
  the canonical document instead.

## Related Documents

- [Codex Provider Notes](../docs/00.agent-governance/providers/codex.md)
- [Codex Local Baseline](CODEX.md)
- [Agent Registry](../docs/00.agent-governance/roles/registry.json)
- [Model Selection Policy](../docs/00.agent-governance/policies/model-selection.md)
- [Work Lifecycle](../docs/00.agent-governance/skills/work-lifecycle.md)
