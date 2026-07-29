@docs/00.agent-governance/rules/bootstrap.md
@docs/00.agent-governance/providers/gemini.md
@.agents/GEMINI.md
@RTK.md

# GEMINI.md

Thin Gemini provider shim for `hy-home.k8s`.

- Runtime and role roster: `docs/00.agent-governance/harness-catalog.md`
- Validation lanes, results, and handoff evidence: `docs/00.agent-governance/rules/quality-standards.md`
- Completion checklist: `docs/00.agent-governance/rules/postflight-checklist.md`
- Template selection: `docs/99.templates/support/template-routing.md`

Tracked `.agents/**` adapters are local/Antigravity repo-static configuration,
not Gemini CLI native surfaces. Tracked `.gemini/agents/**` and
`.gemini/settings.json` provide Gemini CLI repo-static project-surface evidence
only; native discovery, event delivery, policy loading, authenticated execution,
and model resolution remain `DEFER` under the provider evidence contract.
