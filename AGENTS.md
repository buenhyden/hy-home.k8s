@docs/00.agent-governance/rules/bootstrap.md
@docs/00.agent-governance/providers/codex.md
@.codex/CODEX.md
@RTK.md

# AGENTS.md

Thin GPT/Codex provider shim for `hy-home.k8s`.

- Codex/GPT bootstrap gateway: `docs/00.agent-governance/rules/bootstrap.md`
- Codex provider notes: `docs/00.agent-governance/providers/codex.md`
- Local runtime baseline: `.codex/CODEX.md`
- Runtime roster: `docs/00.agent-governance/harness-catalog.md`
- Cross-agent shell command SSOT: `RTK.md`
- Workspace Memory: `docs/00.agent-governance/memory/`
- Workspace Assets: Codex sessions must respect the Stage 00 canonical adapter model: shared `skills/`, `workflows/`, and `output-styles/` come from `.agents/`; provider adapters expose native agent files, rule pointers, and event/validation wiring via `hooks.json` or shared scripts.
- Verification: Codex sessions must run explicit QA, CI/CD validation, and template-routing checks from Stage 00 and `docs/99.templates/support` before handoff.
