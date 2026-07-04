# Claude Provider Notes

Claude-specific guidance for `hy-home.k8s`.

## Official Source Basis

Checked on 2026-07-04:

- Claude Code settings: <https://code.claude.com/docs/en/settings>
- Claude Code hooks: <https://code.claude.com/docs/en/hooks>
- Claude Code subagents: <https://code.claude.com/docs/en/sub-agents>

## Loading Model

- Keep root `CLAUDE.md` thin; it imports `@docs/00.agent-governance/rules/bootstrap.md` (shared governance), `@docs/00.agent-governance/providers/claude.md`, `@.claude/CLAUDE.md`, and `@RTK.md`. It must not import `@AGENTS.md`, which is the GPT/Codex provider shim.
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
- Avoid introducing provider-specific guidance outside the existing `CLAUDE.md` + `.claude/**` + `docs/00.agent-governance/**` hierarchy.

## Memory and Context

- Follow CLAUDE hierarchy: managed policy -> project -> user -> path-specific rules.
- Use imports for modular instructions when needed.
- Use auto memory for recurring lessons, but keep governance controls in docs.

## Native Boundary

- `.claude/settings.json` owns Claude native permissions and hook wiring.
- `.claude/agents/*.md` owns Claude subagent metadata, including `name`,
  `description`, `model`, and least-privilege `tools:`.
- Claude hooks may block objective repo-state failures when wired through
  settings; they do not prove live runtime readiness.
- Claude native tools and permissions must not weaken the repository's
  GitOps-first, no-live-mutation, and secret-handling boundaries.

## Execution Expectations

- Use JIT loading: bootstrap -> preflight -> persona -> scope -> provider -> progress -> postflight.
- Keep responses to users in Korean.
- Keep governance control docs in English.
- Use `docs/00.agent-governance/harness-catalog.md` as the canonical runtime roster.
- Use `docs/00.agent-governance/hooks/lifecycle-guard.sh` as the shared lifecycle hook contract wired by `.claude/settings.json`: Stop/SubagentStop may block objective repo-state failures; PreCompact is advisory and must not replace validation evidence.
- Keep `.claude/*.local.md`, including Hookify rules, as ignored local warning files only. Shared Claude enforcement stays in `.claude/settings.json`, `docs/00.agent-governance/hooks/*.sh`, and repository validators.
