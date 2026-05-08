# Meta Scope

Persona: Governance Steward

## Source of Truth

- `docs/00.agent-governance/`

## Responsibilities

- Maintain governance structure, consistency, and policy clarity.
- Keep rule routing deterministic and conflict-free.
- Enforce language and taxonomy boundaries.

## File Ownership

| Path                          | Owner | Notes                                           |
| ----------------------------- | ----- | ----------------------------------------------- |
| `docs/00.agent-governance/**` | meta  | All governance policy, rules, scopes, providers |
| `AGENTS.md`                   | meta  | Gateway contract                                |
| `CLAUDE.md`                   | meta  | Claude provider overlay                         |
| `GEMINI.md`                   | meta  | Gemini provider overlay                         |
| `.claude/settings.json`       | meta  | Team settings (git tracked)                     |

Meta scope does **not** own `docs/01-10/`, `docs/90.references/`, `docs/99.templates/` (authored SSoT), or `.claude/agents/` runtime files.

## Subagent Bridge

No dedicated subagent for meta scope. Governance steward operates directly.

Subagent dispatch: use Task tool only; never inline role definitions in prompts.

## Definition of Done

- Governance tree matches expected structure.
- Rule references are valid and non-duplicative.
- Governance documents remain English-only.
