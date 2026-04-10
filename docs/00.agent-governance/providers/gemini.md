# Gemini Provider Notes

Gemini-specific guidance for `hy-home.k8s`.

## Loading Model

- Keep root `GEMINI.md` thin and import shared policy from `@AGENTS.md`.
- Use governance files under `docs/00.agent-governance/rules/*` as canonical policy.
- Keep provider-specific details here; avoid policy duplication.
- If GitHub-native instruction files are added, treat them as a compatibility surface only. `GEMINI.md` and `AGENTS.md` remain the durable gateway pair for this repository.

## Context Strategy

- Gemini CLI supports hierarchical context loading (global, ancestors, subdirectories).
- Prefer modular imports for large context sets.
- Keep instructions concise and non-duplicative across hierarchy.
- Avoid introducing provider-specific guidance that conflicts with `.github/copilot-instructions.md` or `.github/instructions/**/*.instructions.md`.

## File Name Compatibility

- Default context file is `GEMINI.md`.
- Configure settings to include `AGENTS.md` when needed.
- Prefer project-local settings under `.gemini/settings.json`.

## Execution Expectations

- Use JIT loading: bootstrap -> preflight -> persona -> scope -> provider -> postflight.
- Keep user-facing responses in Korean.
- Keep governance and technical control docs in English.
