# AI Agent Standards (March 2026)

Global standards for all agents in this repository.

## Language Policy

- `docs/00.agent-governance/*`: English only.
- User-facing responses: Korean only.
- Human-facing top-level docs (`README.md`, `docs/README.md`, stage READMEs): Korean.

## Token and Context Policy

- Keep root shims (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`) minimal.
- Recommended max length for each root shim: 40 lines.
- Avoid duplicated policy text across gateway files.
- Use JIT loading via `bootstrap -> preflight -> persona -> scope -> provider -> postflight`.
- Treat GitHub-native instruction files (`.github/copilot-instructions.md`, `.github/instructions/**/*.instructions.md`) as adapters, not policy SSoT.
- When multiple instruction layers coexist, keep them non-conflicting and narrowly scoped.
- If path-scoped instruction files are introduced later, they must refine behavior for matching paths only and still resolve back to `AGENTS.md` plus `docs/00.agent-governance/*`.

## Documentation Boundary Policy

- Treat `docs/01~99` as authored source of truth by default.
- Changes to `docs/01~99` must be explicitly requested by a human.
- Route governance evolution to `docs/00.agent-governance/*`.

## Quality Policy

- Always keep checklist and matrix references valid:
  - `rules/preflight-checklist.md`
  - `rules/postflight-checklist.md`
  - `rules/stage-authoring-matrix.md`
  - `rules/stage-checklists.md`
- Keep scope and provider docs action-oriented and non-duplicative.

## Workspace Alignment

Infrastructure assumptions must match current workspace assets:

- `infrastructure/`
- `gitops/`
- `scripts/`
- `tests/`
- `.agent/workflows/`
