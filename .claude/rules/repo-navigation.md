# Repo Navigation Rules

Confirmed inspection commands for this repository:

```bash
git status --short
find .agent/rules -maxdepth 2 -type f | sort
find .agent/workflows -maxdepth 2 -type f | sort
find templates -maxdepth 2 -type f | sort
rg --files docs
```

- Use `.agent/rules/` for policy and standards.
- Use `.agent/workflows/` for repeatable delivery and troubleshooting patterns.
- Use `templates/` as the canonical template source.
- Use nearest scoped files under `docs/` before falling back to root guidance.
