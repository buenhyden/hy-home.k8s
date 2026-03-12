# Repo Navigation

This manual gives concrete discovery guidance for this repository. It exists so model-specific files can stay short.

## Key Locations

- Rules: [.agent/rules/](../.agent/rules/)
- Workflows: [.agent/workflows/](../.agent/workflows/)
- Documentation: [docs/](../docs/)
- Templates: [templates/](../templates/)
- Root agent docs: [AGENTS.md](../AGENTS.md), [GEMINI.md](../GEMINI.md), [CLAUDE.md](../CLAUDE.md)

## Safe Inspection Commands

Use these commands when you need repo truth without assuming structure:

```bash
find .agent/rules -maxdepth 2 -type f | sort
find .agent/workflows -maxdepth 2 -type f | sort
find templates -maxdepth 2 -type f | sort
rg --files docs
```

## Discovery Notes

- Inspect `docs/` before repeating inherited template language in generated documentation.
- Use `templates/` as the source of template truth; do not assume nested template folders still exist.
- Treat `.agent/skills/` as optional. If runtime exposes skills, use that source first. Only inspect `.agent/skills/` when it exists locally.
- Do not document root build or test commands unless they are confirmed from repo manifests; no root package manifest was found during inspection.

## When to Use Workflows

- Use `.agent/workflows/` when the request maps to an existing delivery or troubleshooting pattern.
- Use `.agent/rules/` when you need policy, constraints, or standards language.
- Use project manuals and guides when local process overrides matter more than generic workflow defaults.
