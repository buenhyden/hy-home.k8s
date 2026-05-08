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
- Do not embed long RTK, graphify, catalog, or role-separation blocks in root shims.
- Use JIT loading via `bootstrap -> preflight -> persona -> scope -> provider -> postflight`.
- Keep the instruction hierarchy inside repository gateway files plus runtime governance assets only:
  - root shims: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`
  - runtime bridge: `.claude/**` and `.codex/**`
  - policy SSoT: `docs/00.agent-governance/**`
- Do not introduce GitHub-native instruction files such as `.github/copilot-instructions.md` or `.github/instructions/**/*.instructions.md` in this repository.
- RTK guidance belongs in `RTK.md`, not in root shim bodies.

## Documentation Boundary Policy

- Treat `docs/01-10`, `docs/90.references`, and `docs/99.templates` as authored source of truth by default.
- Changes to `docs/01-10`, `docs/90.references`, and `docs/99.templates` must be explicitly requested by a human.
- Route governance evolution to `docs/00.agent-governance/*`.
- Do not introduce parallel authored trees such as `docs/superpowers/**`; route outputs into the official stage folders.

## Quality Policy

- Always keep checklist and matrix references valid:
  - `rules/preflight-checklist.md`
  - `rules/postflight-checklist.md`
  - `rules/stage-authoring-matrix.md`
  - `rules/stage-checklists.md`
- Keep scope and provider docs action-oriented and non-duplicative.

## Workspace Alignment

Infrastructure assumptions must match current workspace assets:

- WSL2+k3d home-lab platform
- ArgoCD repo-backed GitOps workflow
- `infrastructure/`
- `gitops/`
- `scripts/`
- `tests/`
- `.claude/`
- `.codex/`

`.codex/agents/*.toml` files are Codex mirrors of `.claude/agents/*.md` and must keep the same role, scope imports, guardrails, and postflight requirements.
