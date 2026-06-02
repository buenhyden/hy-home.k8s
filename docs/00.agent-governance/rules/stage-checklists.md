# Stage Checklists

Execution-focused checklist index by taxonomy path.

## `00.agent-governance`

- [ ] Routing files and checklists are current.
- [ ] JIT loading order is valid.
- [ ] English-only governance policy is preserved.

## `01.requirements`

- [ ] Problem, value, acceptance criteria, and scope are explicit.
- [ ] Links to downstream docs are prepared.

## `02.architecture/requirements`

- [ ] System boundaries and quality attributes are documented.
- [ ] Inputs from PRD are traceable.

## `02.architecture/decisions`

- [ ] Decision context, alternatives, and consequences are captured.
- [ ] Links to PRD/ARD/Spec are valid.

## `03.specs`

- [ ] Contracts, data models, and verification plan are defined.
- [ ] API/Agent design docs are included when needed.

## `04.execution/plans`

- [ ] Phases, risks, gates, and rollback strategy are documented.
- [ ] Plan links to source specs and tasks.
- [ ] Verification plan defines validation commands and pass criteria.

## `04.execution/tasks`

- [ ] Each task references parent plan/spec.
- [ ] Validation commands and evidence are attached.
- [ ] Verification summary separates local, CI-only, and skipped evidence lanes.

## `05.operations/guides`

- [ ] Audience, prerequisites, and reproducible steps are clear.
- [ ] Cross-links to specs, policies, and runbooks are present.

## `05.operations/policies`

- [ ] Policy controls and promotion criteria are explicit.
- [ ] Security and evidence-retention requirements are defined.

## `05.operations/runbooks`

- [ ] Step-by-step execution and recovery paths are operational.
- [ ] Validation and escalation paths are explicit.

## `05.operations/incidents`

- [ ] Timeline, impact, evidence, and mitigations are recorded.
- [ ] Related runbook links are attached.
- [ ] Postmortem RCA, preventive actions, and follow-up links are recorded under `docs/05.operations/incidents/postmortems/` when needed.

## `98.archive`

- [ ] Original docs subpath is mirrored under `docs/98.archive/`.
- [ ] Tombstone body contains metadata only and no old full body text.
- [ ] Current replacement and implementation evidence are linked.
- [ ] Active docs link archive content only through `docs/98.archive/README.md`.
