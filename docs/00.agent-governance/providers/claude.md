# Claude Provider Notes

Claude-specific guidance for `hy-home.k8s`.

## Loading Model

- Keep root `CLAUDE.md` thin and import shared policy from `@AGENTS.md`.
- Use governance files under `docs/00.agent-governance/rules/*` as canonical policy.
- Keep provider-specific details here; do not duplicate global rules.

## Memory and Context

- Follow CLAUDE.md hierarchy: managed policy -> project -> user -> subdirectory JIT.
- Prefer modular imports for large policy sets.
- Remove conflicting or stale rules before adding new ones.

## Execution Expectations

- Use JIT loading: bootstrap -> persona -> scope -> provider.
- Keep responses to users in Korean.
- Keep governance/spec text in English where policy requires it.
