@AGENTS.md
@docs/00.agent-governance/providers/claude.md
@.claude/CLAUDE.md

# CLAUDE.md

- Runtime baseline: `.claude/CLAUDE.md`
- Canonical runtime roster: `docs/00.agent-governance/harness-catalog.md`
- Shared policy and constraints: `AGENTS.md` + `docs/00.agent-governance/**`

## graphify

This project has a graphify knowledge graph at graphify-out/.

Rules:
- Before answering architecture or codebase questions, read graphify-out/GRAPH_REPORT.md for god nodes and community structure
- If graphify-out/wiki/index.md exists, navigate it instead of reading raw files
- After modifying code files in this session, run `graphify update .` to keep the graph current (AST-only, no API cost)
