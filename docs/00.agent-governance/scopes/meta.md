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
| `docs/00.agent-governance/hooks/**` | meta  | Shared runtime hook contracts                   |
| `.agents/skills/**`           | meta  | Repo-backed shared skill source of truth        |
| `.claude/skills/**`           | meta  | Claude symlink view of shared skills            |
| `.codex/**`                   | meta  | Codex mirrors and hook wiring                   |

Meta scope owns `.claude/agents/**` roster and mirror contract shape through
`harness-catalog.md` and `subagent-protocol.md`; imported scope files own the
domain behavior for each worker.

Meta scope does **not** own `docs/01.requirements/`, `docs/02.architecture/`, `docs/03.specs/`, `docs/04.execution/`, `docs/05.operations/`, `docs/90.references/`, `docs/98.archive/`, or `docs/99.templates/` (authored SSoT).

## Subagent Bridge

No dedicated worker subagent for meta scope. Governance steward operates
directly, while `supervisor` imports `meta` only for routing and escalation
control.

Subagent dispatch: use Task tool only; never inline role definitions in prompts.

## Definition of Done

- Governance tree matches expected structure.
- Rule references are valid and non-duplicative.
- Governance documents remain English-only.
