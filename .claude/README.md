---
title: ".claude"
version: "0.1.0"
type: "common/readme-implementation"
status: "active"
owner: "platform"
updated: "2026-09-04"
---
# .claude

## Overview

`.claude/` is the projection surface the Claude runtime reads. The shared
meaning of roles and skills belongs to [Stage 00](../docs/00.agent-governance/README.md);
this directory adds only the Claude-native metadata on top of it, such as
model, tool allowlist, permission declarations, and hook registration.

These tracked files are repository configuration. They do not prove that
Claude discovered them, that a permission was enforced, that a hook was
delivered, or which model resolved. Each of those needs separate runtime
evidence.

### Audience

- Platform maintainers
- Governance owners
- Operators running the Claude runtime

### Scope

#### In Scope

- The Claude local baseline (`CLAUDE.md`)
- Per-role native projections with least-privilege tool metadata (`agents/*.md`)
- Native permission and event declarations (`settings.json`)
- The shared skill view (`skills` symlink)

#### Out of Scope

- Shared role and skill definitions, owned by `docs/00.agent-governance/roles/registry.json`
- Execution policy, approval boundaries, and quality lanes, owned by `docs/00.agent-governance/policies/`
- Evidence of native discovery, permission enforcement, authentication, model resolution, or execution

## Structure

| Path | Responsibility |
| --- | --- |
| `CLAUDE.md` | Thin local baseline stating loading order and provider metadata |
| `agents/*.md` | Native projections of the 12 roles. Frontmatter allows `name` and `description`, plus optional `model` and `tools` |
| `settings.json` | `permissions` and the pre-action `hooks` declarations |
| `skills` | Symlink to `../docs/00.agent-governance/skills`. Skill bodies are not edited here |

## Configuration Boundary

- Declarations here may narrow the common approval boundary but never widen
  it. Widening requires
  [approval and safety](../docs/00.agent-governance/policies/approval-and-safety.md)
  to change first.
- Managed, project, and user instruction precedence stays intact. Shared
  context is imported rather than copied.
- `settings.local.json` and `*.local.md` are gitignored auxiliary context.
  They replace neither shared policy nor repository validators.
- Native metadata fields are not added from assumptions about another client
  version. Verify the intended runtime contract when configuration changes.

## Validation

Run `python3 scripts/validate-agent-governance.py --root .` for the registry,
native metadata, direct role/procedure reads, permissions, and retired consumers.
Run `python3 scripts/qa.py full` for complete repository-static validation.

Tracked files under this directory stay English-only; `repository-quality`
enforces that.

## Operations

- Changing a role means updating `docs/00.agent-governance/roles/registry.json`,
  `docs/00.agent-governance/roles/<role>.md`, `.claude/agents/<role>.md`, and
  `.codex/agents/<role>.toml` in one change.
- After adding or editing a hook, confirm separately that the intended runtime
  loads and dispatches it. A tracked declaration alone proves nothing about
  hook behavior.
- Edit skill bodies under `docs/00.agent-governance/skills/`.

## Related Documents

- [Claude Provider Notes](../docs/00.agent-governance/providers/claude.md)
- [Claude Local Baseline](CLAUDE.md)
- [Agent Registry](../docs/00.agent-governance/roles/registry.json)
- [Model Selection Policy](../docs/00.agent-governance/policies/model-selection.md)
- [Quality Policy](../docs/00.agent-governance/policies/quality.md)
