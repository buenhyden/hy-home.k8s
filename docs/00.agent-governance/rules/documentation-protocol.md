# Documentation Protocol (March 2026)

This protocol defines how governance references authored docs and how language boundaries are applied.

## Core Requirements

- Governance policy belongs in `docs/00.agent-governance/`.
- Product and delivery truth remains in `docs/01.requirements`, `docs/02.architecture`, `docs/03.specs`, `docs/04.execution`, `docs/05.operations`, `docs/90.references`, and `docs/99.templates`.
- Governance files must reference authored docs and must not duplicate stage content.

## Document Output Routing

- Generated documents must use the canonical stage tree only.
- Use [document-stage-routing.md](./document-stage-routing.md) for path selection and skill-specific rerouting rules.
- Do not create parallel authored trees such as `docs/superpowers/**`.
- Do not place API contract docs under `docs/api/**`; keep them under `docs/03.specs/<feature-id>/`.

## Template Enforcement Policy

- All authored documents under `docs/01.requirements/`, `docs/02.architecture/`, `docs/03.specs/`, `docs/04.execution/`, `docs/05.operations/`, and `docs/90.references/` must start from the matching template listed in `docs/99.templates/README.md`.
- README files must use `docs/99.templates/readme.template.md`.
- PRD, ARD, ADR, Spec, Plan, Task, Guide, Operations Policy, Runbook, Incident, Postmortem, and Reference documents must use their stage-specific templates from `docs/99.templates/`.
- `docs/03.specs/<feature-id>/api-spec.md`, `agent-design.md`, `data-model.md`, and `tests.md` must use their matching helper templates.
- New authored documents must keep `status: draft` until a human promotes the lifecycle state.
- Authored documents must keep the required template headings and must include `## Related Documents`.
- Agents must report the template path used and the validation evidence before handoff.
- Generated exceptions, such as `docs/90.references/llm-wiki/wiki-index.md`, must keep their generator contract and must not be edited by hand.
- Claude and Codex Write/Edit/MultiEdit hooks must surface Template-First guidance before authored stage doc edits and run post-edit documentation template enforcement.

## Language Boundary Rules

- `docs/00.agent-governance/*`: English only.
- Human-facing README files: Korean (`README.md`, `docs/README.md`, and stage READMEs).
- Agent execution control documents under governance must be written in English.

## Traceability Rules

- Every governance change should keep clear links to the canonical docs taxonomy (`01.requirements`, `02.architecture`, `03.specs`, `04.execution`, `05.operations`, `90.references`, `99.templates`).
- Postmortems belong under `docs/05.operations/incidents/postmortems/`, not a separate top-level docs stage.
- Persona and scope instructions must state which stage folders are authoritative.
- Stage expectations must map to [stage-authoring-matrix.md](stage-authoring-matrix.md).
- Repo-changing agent work must append progress and reusable memory to `docs/00.agent-governance/memory/progress.md` using `docs/99.templates/progress.template.md`.
- Standalone files under `docs/00.agent-governance/memory/` must use `docs/99.templates/memory.template.md` and must be accompanied by a related `progress.md` entry in the same change.

## Template Link Policy

- Actual Markdown links inside templates must resolve relative to the template file location.
- Placeholder, optional, or target-relative examples must be written as code literals or fenced snippets and calculated from the final authored document location.
- Optional or project-specific files that may not exist (for example, `ARCHITECTURE.md`) should be shown as code literals, not Markdown links.
- Placeholder paths should be expressed as placeholders (`{path}`) or fenced snippets to avoid false-positive broken-link checks.

## Checklist Policy

- Run `preflight-checklist.md` before editing.
- Run `postflight-checklist.md` before finalization.

## Docs 3 Rules (HALT)

**R1 — Template-First:** Read `docs/99.templates/README.md`, then read the matching template in `docs/99.templates/` before creating any document. Fill all required fields and required template headings; set `status: draft`. k8s-specific triggers: new namespace → ARD required; RBAC change → ADR required; production change → OPER policy first.

**R2 — README Sync:** Any folder-level change (add, move, remove files) requires the folder's `README.md` to be updated in the same PR. Work is **BLOCKED** until the README reflects the change.

**R3 — Related Documents:** Every authored document must include a `## Related Documents` section with upstream links. A document without this section is **INCOMPLETE**.

**R4 — Memory Ledger Coupling:** Repo-changing work updates `memory/progress.md`. Standalone memory files use `memory.template.md` and link back to their related progress entry.

**HALT conditions:** Missing template read → HALT. README not updated → HALT. Related Documents section absent → HALT. Memory entry without progress ledger update → HALT.
