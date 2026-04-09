@AGENTS.md
@docs/00.agent-governance/providers/claude.md

# CLAUDE.md

- Canonical policy: `docs/00.agent-governance/rules/*`
- Harness: `.claude/agents/` (6, @import, model:opus) + `.claude/skills/` (k8s-validate · gitops-workflow · risk-report)
- H100: github.com/revfactory/harness-100 — H100:26,20,28,25,21,88,92 adapted
- `settings.json` = team (git tracked) · `settings.local.json` = personal (.gitignored) · no duplication
- GitOps-First: no `kubectl apply`; always PR path · postflight required every task
