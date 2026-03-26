# AI Agent Standards (March 2026)

Global standards for all agents in this repository.

## Language Policy

- `docs/00.agent-governance/*`: English only.
- User-facing responses: Korean only.
- Human-facing top-level docs (`README.md`, `docs/README.md`): Korean.

## Token and Context Policy

- Keep root shims (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`) minimal.
- Avoid duplicated policy text across files.
- Use JIT loading via bootstrap -> persona -> scope -> provider.

## Documentation Boundary Policy

- Treat `docs/01~99` as authored source of truth.
- Do not alter authored content in `docs/01~99` unless explicitly requested by a human.
- Route governance evolution to `docs/00.agent-governance/*`.

## Workspace Alignment

- Infrastructure assumptions must match current workspace assets:
  - `infrastructure/`
  - `gitops/`
  - `scripts/`
  - `tests/`
