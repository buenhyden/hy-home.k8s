# Gemini Provider Notes

Gemini-specific guidance for `hy-home.k8s`.

## Loading Model

- Keep root `GEMINI.md` thin and import shared policy from `@AGENTS.md`.
- Root `GEMINI.md` must load the existing hierarchy; it must not copy RTK, graphify, catalog, or governance policy blocks inline.
- Use `.claude/CLAUDE.md` as the runtime baseline when agent roster or model hierarchy is needed.
- Use governance files under `docs/00.agent-governance/rules/*` as canonical policy.
- Keep provider-specific details here; avoid policy duplication.
- Keep Gemini-specific runtime wiring under the existing gateway hierarchy; do not create a parallel `.github/**` instruction layer for this repository.

## Context Strategy

- Gemini CLI supports hierarchical context loading (global, ancestors, subdirectories).
- Prefer modular imports for large context sets.
- Keep instructions concise and non-duplicative across hierarchy.
- Avoid introducing provider-specific guidance outside the existing `AGENTS.md` + `.claude/**` + `docs/00.agent-governance/**` hierarchy.

## File Name Compatibility

- Default context file is `GEMINI.md`.
- Configure settings to include `AGENTS.md` when needed.
- Prefer project-local settings under `.gemini/settings.json`.

## Execution Expectations

- Use JIT loading: bootstrap -> preflight -> persona -> scope -> provider -> progress -> postflight.
- Keep user-facing responses in Korean.
- Keep governance and technical control docs in English.
- Use `docs/00.agent-governance/harness-catalog.md` as the canonical runtime roster.
