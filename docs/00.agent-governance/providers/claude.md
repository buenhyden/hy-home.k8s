# Claude Provider Notes

Claude-specific guidance for `hy-home.k8s`.

## Loading Model

- Keep root `CLAUDE.md` thin and import shared policy from `@AGENTS.md`.
- Root `CLAUDE.md` must load the existing hierarchy; it must not copy RTK, graphify, catalog, or governance policy blocks inline.
- Use `.claude/CLAUDE.md` as the local runtime baseline for agent roster and model hierarchy.
- Use governance files under `docs/00.agent-governance/rules/*` as canonical policy.
- Use `@RTK.md` for shell-command guidance when Claude needs that context.
- Keep provider-specific details here; do not duplicate global rules.
- Keep Claude-specific runtime wiring under `.claude/**`; do not create a parallel `.github/**` instruction layer for this repository.

## Context Strategy

- Prefer concise CLAUDE context files (target under 200 lines per file).
- For larger projects, split rules into `.claude/rules/` files.
- Use path-scoped rules where applicable to reduce always-loaded context.
- Keep conflicting instructions out of CLAUDE hierarchy.
- Avoid introducing provider-specific guidance outside the existing `AGENTS.md` + `.claude/**` + `docs/00.agent-governance/**` hierarchy.

## Memory and Context

- Follow CLAUDE hierarchy: managed policy -> project -> user -> path-specific rules.
- Use imports for modular instructions when needed.
- Use auto memory for recurring lessons, but keep governance controls in docs.

## Execution Expectations

- Use JIT loading: bootstrap -> preflight -> persona -> scope -> provider -> postflight.
- Keep responses to users in Korean.
- Keep governance control docs in English.
- Use `docs/00.agent-governance/harness-catalog.md` as the canonical runtime roster.
