# Preflight Checklist (March 2026)

Run this checklist before making substantial edits.

## 1. Task Intake

- [ ] Goal and success criteria are explicit.
- [ ] In-scope and out-of-scope boundaries are identified.
- [ ] High-risk assumptions are listed.
- [ ] Workspace purpose and active repo contracts are identified.

## 2. Governance Routing

- [ ] `rules/bootstrap.md` reviewed.
- [ ] Persona selected via `rules/persona.md`.
- [ ] Matching scope loaded from `scopes/`.
- [ ] Provider notes loaded from `providers/` when relevant.
- [ ] `memory/progress.md` reviewed for current progress, handoff, and reusable memory context.

## 3. Stage and Source Mapping

- [ ] Stage ownership confirmed using `stage-authoring-matrix.md`.
- [ ] Authoritative input documents identified.
- [ ] Required output documents identified.

## 4. Safety and Boundaries

- [ ] Language boundary confirmed (governance English, user-facing Korean).
- [ ] Planned edits avoid unintended scope expansion.
- [ ] Path references to be changed are real workspace paths.
- [ ] Existing staged and unstaged changes reviewed; unrelated user changes will be preserved.
- [ ] Repo-backed vs live-cluster boundary is stated; no direct cluster mutation is planned.

## 5. Execution Readiness

- [ ] Validation commands/checks are defined before editing.
- [ ] Evidence requirements for completion are defined.
- [ ] Unavailable local tools and expected validation limitations are identified.
- [ ] A `memory/progress.md` update is planned for repo-changing work.
