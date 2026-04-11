@AGENTS.md
@docs/00.agent-governance/providers/claude.md

# CLAUDE.md

- Canonical policy: `docs/00.agent-governance/rules/*`
- Harness catalog: `docs/00.agent-governance/harness-catalog.md`
- Agents: `.claude/agents/` (sonnet) + `supervisor.md` (opus)
- Skills: `.claude/skills/` (`k8s-validate` · `gitops-workflow` · `risk-report`)
- `settings.json` = team (git tracked) · `settings.local.json` = personal (.gitignored) · no duplication
- GitOps-First: no `kubectl apply`; always PR path · postflight required every task
