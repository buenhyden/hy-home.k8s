# Repo Navigation

Human-readable repo map that matches the runtime navigation rules.

## Key Locations

- Root contract: [AGENTS.md](../AGENTS.md)
- Claude runtime entrypoint: [CLAUDE.md](CLAUDE.md)
- Gemini runtime entrypoint: [GEMINI.md](GEMINI.md)
- Runtime rules: [rules/](rules/)
- Repo docs: [docs/](../docs/)
- Templates: [templates/](../templates/)
- Rules: [../.agent/rules/](../.agent/rules/)
- Workflows: [../.agent/workflows/](../.agent/workflows/)

## Confirmed Safe Commands

```bash
git status --short
find .agent/rules -maxdepth 2 -type f | sort
find .agent/workflows -maxdepth 2 -type f | sort
find templates -maxdepth 2 -type f | sort
rg --files docs
```

## Notes

- Inspect `docs/agentic/` before expanding root tool files.
- Inspect nearest scoped files under `docs/` before applying generic guidance.
- Do not document root build or test commands unless a real root manifest appears.
