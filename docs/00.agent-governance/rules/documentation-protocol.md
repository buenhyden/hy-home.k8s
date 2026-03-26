# Documentation Protocol (March 2026)

This protocol defines how governance references authored docs and how language boundaries are applied.

## Core Requirements

- Governance policy belongs in `docs/00.agent-governance/`.
- Product and delivery truth remains in `docs/01~99`.
- Governance files must reference authored docs and must not duplicate stage content.

## Language Boundary Rules

- `docs/00.agent-governance/*`: English only.
- Human-facing README files: Korean (`README.md`, `docs/README.md`, and stage READMEs).
- Agent execution control documents under governance must be written in English.

## Traceability Rules

- Every governance change should keep clear links to stage folders (`01` to `11`, `90`, `99`).
- Persona and scope instructions must state which stage folders are authoritative.
- Stage expectations must map to [stage-authoring-matrix.md](stage-authoring-matrix.md).

## Template Link Policy

- Example links inside templates must resolve relative to the template location.
- Optional or project-specific files that may not exist (for example, `ARCHITECTURE.md`) should be shown as code literals, not Markdown links.
- Placeholder paths should be expressed as placeholders (`{path}`) or fenced snippets to avoid false-positive broken-link checks.

## Checklist Policy

- Run `preflight-checklist.md` before editing.
- Run `postflight-checklist.md` before finalization.
