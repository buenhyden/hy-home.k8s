@docs/00.agent-governance/rules/bootstrap.md
@docs/00.agent-governance/providers/claude.md
@.claude/CLAUDE.md
@RTK.md

# CLAUDE.md

Thin Claude provider shim for `hy-home.k8s`.

- Central gateway: `docs/00.agent-governance/rules/bootstrap.md`
- Claude provider notes: `docs/00.agent-governance/providers/claude.md`
- Local runtime baseline: `.claude/CLAUDE.md`
- Runtime roster: `docs/00.agent-governance/harness-catalog.md`
- Cross-agent shell command SSOT: `RTK.md`
- Workspace Assets: Claude sessions must respect the Stage 00 canonical adapter model: shared `skills/`, `workflows/`, and `output-styles` come from `.agents/`; Claude-native agents, settings, and hooks live under `.claude/`.
- Verification: Claude sessions must run explicit QA, CI/static validation, and template-routing checks from Stage 00 and `docs/99.templates/support` before handoff.
