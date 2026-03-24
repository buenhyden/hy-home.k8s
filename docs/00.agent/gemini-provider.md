# Gemini Provider Notes

## Scope

This file contains Gemini CLI-specific guidance for the `hy-home.k8s` project.

## Context File Hierarchy

Gemini CLI loads context files in this order (lowest to highest precedence):

| File                       | Scope                 | Notes                                                                     |
| -------------------------- | --------------------- | ------------------------------------------------------------------------- |
| `~/.gemini/GEMINI.md`      | Global — all projects | User-wide preferences; personal defaults                                  |
| `./GEMINI.md` (repo root)  | Project — shared      | Checked into git; applies to all team members                             |
| `<subdirectory>/GEMINI.md` | Directory             | JIT-loaded when a tool accesses a file in that directory or its ancestors |

## Gemini CLI Guidance

layer: 'architecture'

- Keep the root `GEMINI.md` thin and delegate to this provider file.
- Use hierarchical context discovery: root file for universal rules, subdirectory files for local task context.
- **Skill Autonomy**: Gemini MUST utilize any available skill (e.g., `writing-plans`, `executing-plans`, `doc-coauthoring`) without persona-based restrictions.
- **MCP Servers**: Configured in `.gemini/settings.json`.

## Korean Mandate

- **USER interaction**: Summaries and high-level explanations MUST be in Korean.
- **Internal Docs**: All instructions and technical documentation in `docs/00.agent/` MUST be in English.

## References

- Gemini CLI context files (GEMINI.md): <https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/gemini-md.md>
- Gemini CLI settings: <https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/settings.md>
- Gemini CLI MCP integration: <https://github.com/google-gemini/gemini-cli/blob/main/docs/tools/mcp-server.md>
