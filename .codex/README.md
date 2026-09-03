# .codex

## Overview

`.codex/` is the projection surface the Codex runtime reads. The shared
meaning of roles and skills belongs to [`.agents/`](../.agents/README.md);
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
- The shared skill view (`skills` symlink)

#### Out of Scope

- Shared role and skill definitions, owned by `.agents/registry.json`
- Execution policy, approval boundaries, and quality lanes, owned by `docs/00.agent-governance/policies/`
- Evidence of native discovery, permission enforcement, authentication, model resolution, or execution

## Structure

| Path | Responsibility |
| --- | --- |
| `CODEX.md` | Thin local baseline stating loading order and provider metadata |
| `agents/*.toml` | Native projections of the 12 roles, carrying `name`, `description`, `model`, `model_reasoning_effort`, and `developer_instructions` |
| `skills` | Symlink to `../.agents/skills`. Skill bodies are not edited here |

Each `developer_instructions` block covers runtime bootstrap, role, when to
use, inputs, outputs, guardrails, capability and evidence, handoff, and
postflight in that order. Wording may differ from the Claude projection, but
the meaning is the one the registry owns.

## Configuration Boundary

- The root `AGENTS.md` is the Codex gateway and does not import the Claude
  gateway.
- Declarations here may narrow the common approval boundary but never widen it.
- Model and reasoning-effort values follow the capability tiers in
  [model selection](../docs/00.agent-governance/policies/model-selection.md);
  these files do not redefine what a tier means.
- Policy text is referenced, not copied into this directory.

## Validation

| Validator | Checks |
| --- | --- |
| `agent-harness-contract` | Registry and this projection carry the same meaning |
| `agent-provider-evidence` | What a provider surface is allowed to claim |
| `agent-governance-ci` | Governance surfaces agree with the CI contract |
| `agent-legacy-cutover` | No retired role or path reference remains |

Run: `bash scripts/validate-repo-quality-gates.sh .`

Tracked files under this directory stay English-only; `repository-quality`
enforces that.

## Operations

- Changing a role means updating `.agents/registry.json`,
  `.agents/agents/<role>.md`, `.claude/agents/<role>.md`, and
  `.codex/agents/<role>.toml` in one change. Updating one side alone fails
  provider parity validation.
- Edit skill bodies under `.agents/skills/`.
- Do not write new policy sentences into `developer_instructions`; reference
  the canonical document instead.

## Related Documents

- [Codex Provider Notes](../docs/00.agent-governance/providers/codex.md)
- [Codex Local Baseline](CODEX.md)
- [Agent Registry](../.agents/README.md)
- [Model Selection Policy](../docs/00.agent-governance/policies/model-selection.md)
- [Work Lifecycle](../docs/00.agent-governance/skills/work-lifecycle.md)
