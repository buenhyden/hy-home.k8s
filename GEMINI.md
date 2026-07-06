@docs/00.agent-governance/rules/bootstrap.md
@docs/00.agent-governance/providers/gemini.md
@.agents/GEMINI.md
@RTK.md

# GEMINI.md

Thin Gemini provider shim for `hy-home.k8s`.

- Central gateway: `docs/00.agent-governance/rules/bootstrap.md`
- Gemini provider notes: `docs/00.agent-governance/providers/gemini.md`
- Local runtime baseline: `.agents/GEMINI.md`
- Runtime roster: `docs/00.agent-governance/harness-catalog.md`
- Cross-agent shell command SSOT: `RTK.md`
- Workspace Assets: Gemini sessions must respect the Stage 00 canonical adapter model: shared `skills/`, `workflows/`, and `output-styles` come from `.agents/`; Gemini/Antigravity agent references and hook wiring live under `.agents/`.
- Verification: Gemini sessions must run explicit QA, CI/static validation, and template-routing checks from Stage 00 and `docs/99.templates/support` before handoff.
