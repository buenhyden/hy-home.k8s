---
title: ".agents"
version: "0.1.0"
type: "common/readme-implementation"
status: "active"
owner: "platform"
updated: "2026-09-04"
---
# .agents

## Overview

`.agents/` owns the provider-neutral agent assets. A role's responsibility,
permission class, skill set, and handoff targets are declared here once, and
`.claude/` and `.codex/` project that shared meaning into their own runtime
formats without redefining it.

Everything in this directory is repository-static configuration. It proves
neither native discovery, permission enforcement, model resolution,
authentication, nor execution.

### Audience

- Platform maintainers
- Governance owners
- AI agents

### Scope

#### In Scope

- The single machine owner of roles, skills, permission classes, and providers (`registry.json`)
- The structural contract that registry must satisfy (`contracts/agent-registry.schema.json`)
- Neutral role responsibilities (`agents/*.md`)
- Shared skill bodies (`skills/*/skill.md`)

#### Out of Scope

- Provider-native metadata such as model, tool allowlist, or hook declarations, owned by `.claude/` and `.codex/`
- Execution policy and approval boundaries, owned by `docs/00.agent-governance/policies/`
- Evidence of native execution, permission enforcement, or authentication

## Structure

| Path | Responsibility |
| --- | --- |
| `registry.json` | Neutral definition of 12 roles, 16 skills, 3 permission classes, and 2 providers |
| `contracts/agent-registry.schema.json` | Structural contract for `registry.json` |
| `agents/*.md` | Per-role responsibility, inputs and outputs, guardrails, and handoff targets |
| `skills/*/skill.md` | Provider-independent procedures. The `.claude/skills` and `.codex/skills` symlinks resolve here |

The permission classes are `read-only-evidence`, `scoped-authoring`, and
`orchestration`. The registry owns what each class means; a provider projection
may narrow a class but never widen it.

## Configuration Boundary

- `registry.json` is the canonical owner of roles and skills. Provider files
  reference that meaning rather than restating it.
- `.claude/skills` and `.codex/skills` are symlinks to `../.agents/skills`.
  Skill bodies are edited here and nowhere else.
- Role documents describe responsibility and do not repeat execution policy,
  which belongs to
  [`docs/00.agent-governance/policies/`](../docs/00.agent-governance/policies/agent-execution.md).

## Validation

| Validator | Checks |
| --- | --- |
| `agent-harness-contract` | Registry and provider projections carry the same meaning |
| `agent-governance-ci` | Governance surfaces agree with the CI contract |
| `agent-legacy-cutover` | No retired role or path reference remains |
| `agent-loop-lifecycle` | Delegation loop definitions are consistent |
| `document-contract-registry`, `markdown-profiles`, `links-and-owners`, `document-lifecycle` | Document profile, link, and lifecycle contracts |

Run: `bash scripts/validate-repo-quality-gates.sh .`

Every one of these is repository-static. Whether a runtime actually loaded
these files requires separate evidence.

## Operations

- Changing a role means updating `registry.json`, `agents/<role>.md`, and both
  provider projections (`.claude/agents/<role>.md`,
  `.codex/agents/<role>.toml`) in one change. Updating one side alone fails
  `agent-harness-contract`.
- Adding a skill means creating `skills/<name>/skill.md` and registering it in
  the registry skill list. The symlinks make per-provider copies unnecessary.
- A change that widens permission needs
  [approval and safety](../docs/00.agent-governance/policies/approval-and-safety.md)
  checked first.

## Related Documents

- [Agent Governance Hub](../docs/00.agent-governance/README.md)
- [Agent Execution Policy](../docs/00.agent-governance/policies/agent-execution.md)
- [Roles](../docs/00.agent-governance/roles/README.md)
- [Work Lifecycle](../docs/00.agent-governance/skills/work-lifecycle.md)
- [.claude](../.claude/README.md)
- [.codex](../.codex/README.md)
