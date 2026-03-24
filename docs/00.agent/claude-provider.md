# Claude Provider Notes

## Scope

This file contains Claude Code-specific guidance and memory hierarchy for the `hy-home.k8s` project.

## Memory Hierarchy

Claude Code loads `CLAUDE.md` files in this order (lowest to highest precedence):

| File                       | Scope                 | Notes                                                    |
| -------------------------- | --------------------- | -------------------------------------------------------- |
| `~/.claude/CLAUDE.md`      | Global — all projects | User-wide preferences; personal defaults                 |
| `./CLAUDE.md` (repo root)  | Project — shared      | Checked into git; applies to all team members            |
| `./.claude.local.md`       | Project — personal    | Gitignored; use for local overrides not shared with team |
| `<subdirectory>/CLAUDE.md` | Directory             | Loaded automatically when working within that directory  |

## Claude Code Instructions

layer: 'architecture'

- Keep the root `CLAUDE.md` thin and delegate to this provider file.
- Prefer parent-to-child memory hierarchy: root file for universal rules, subdirectory files for local detail.
- Use `.claude.local.md` for personal preferences (API keys, editor settings).
- **Skill Autonomy**: Claude MUST utilize any available skill (e.g., `writing-plans`, `executing-plans`, `doc-coauthoring`) without persona-based restrictions.
- **Progressive Disclosure**: Use `@` references if needed, but prefer JIT loading of scopes via `agent-instructions.md`.

## Korean Mandate

- **USER interaction**: Summaries and high-level explanations MUST be in Korean.
- **Internal Docs**: All instructions and technical documentation in `docs/00.agent/` MUST be in English.
