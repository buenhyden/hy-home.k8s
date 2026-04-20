# Documentation Protocol (March 2026)

This protocol defines how governance references authored docs and how language boundaries are applied.

## Core Requirements

- Governance policy belongs in `docs/00.agent-governance/`.
- Product and delivery truth remains in `docs/01~99`.
- Governance files must reference authored docs and must not duplicate stage content.

## Document Output Routing

- Generated documents must use the canonical stage tree only.
- Use [document-stage-routing.md](./document-stage-routing.md) for path selection and skill-specific rerouting rules.
- Do not create parallel authored trees such as `docs/superpowers/**`.
- Do not place API contract docs under `docs/api/**`; keep them under `docs/04.specs/<feature-id>/`.

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

## Docs 3 Rules (HALT)

**R1 — Template-First:** Read the matching template in `docs/99.templates/` before creating any document. Fill all required fields; set `status: draft`. k8s-specific triggers: new namespace → ARD required; RBAC change → ADR required; production change → OPER policy first.

**R2 — README Sync:** Any folder-level change (add, move, remove files) requires the folder's `README.md` to be updated in the same PR. Work is **BLOCKED** until the README reflects the change.

**R3 — Related Documents:** Every authored document must include a `## Related Documents` section with upstream links. A document without this section is **INCOMPLETE**.

**HALT conditions:** Missing template read → HALT. README not updated → HALT. Related Documents section absent → HALT.
