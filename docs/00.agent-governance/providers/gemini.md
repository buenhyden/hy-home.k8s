# Gemini Provider Notes

Gemini-specific guidance for `hy-home.k8s`.

## Loading Model

- Keep root `GEMINI.md` thin and import shared policy from `@AGENTS.md`.
- Use governance files under `docs/00.agent-governance/rules/*` as canonical policy.
- Keep provider-specific details here; avoid policy duplication.

## Context Strategy

- Gemini supports hierarchical context files and JIT local loading.
- If needed, set `contextFileName` to `AGENTS.md` in Gemini CLI settings for compatibility.
- Prefer modular `@file` references for large context sets.

## Execution Expectations

- Use JIT loading: bootstrap -> persona -> scope -> provider.
- Keep user-facing responses in Korean.
- Keep governance and technical control docs in English.
