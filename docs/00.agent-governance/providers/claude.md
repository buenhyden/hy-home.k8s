# Claude Provider Notes

Claude-specific guidance for `hy-home.k8s`.

## Loading Model

- Keep root `CLAUDE.md` thin and import shared policy from `@AGENTS.md`.
- Use governance files under `docs/00.agent-governance/rules/*` as canonical policy.
- Keep provider-specific details here; do not duplicate global rules.

## Context Strategy

- Prefer concise CLAUDE context files (target under 200 lines per file).
- For larger projects, split rules into `.claude/rules/` files.
- Use path-scoped rules where applicable to reduce always-loaded context.
- Keep conflicting instructions out of CLAUDE hierarchy.

## Memory and Context

- Follow CLAUDE hierarchy: managed policy -> project -> user -> path-specific rules.
- Use imports for modular instructions when needed.
- Use auto memory for recurring lessons, but keep governance controls in docs.

## Execution Expectations

- Use JIT loading: bootstrap -> preflight -> persona -> scope -> provider -> postflight.
- Keep responses to users in Korean.
- Keep governance control docs in English.
