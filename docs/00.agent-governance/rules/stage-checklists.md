---
title: 'Stage Checklists'
type: governance/reference
status: active
owner: platform
updated: 2026-07-14
---

# Stage Checklists

## Overview

Execution-focused checklist index by taxonomy path.

## Authority Boundary

These checklists summarize execution readiness and completion by stage. They do
not define template structure, lifecycle transitions, or approval rights;
Stage 99 support contracts and the protected-surface approval matrix own those
decisions. A checklist item cannot override an owning stage document.

## Governance Context

Agents use this index after persona and stage selection to translate the
authoring matrix into review questions. The active Plan and Task hold concrete
acceptance evidence, while this file remains a reusable cross-stage checklist.

## Current Contract

### `00.agent-governance`

- [ ] Routing files and checklists are current.
- [ ] JIT loading order is valid.
- [ ] English-only governance policy is preserved.

### `01.requirements`

- [ ] Problem, value, acceptance criteria, and scope are explicit.
- [ ] Links to downstream docs are prepared.

### `02.architecture/requirements`

- [ ] System boundaries and quality attributes are documented.
- [ ] Inputs from PRD are traceable.

### `02.architecture/decisions`

- [ ] Decision context, alternatives, and consequences are captured.
- [ ] Links to PRD/ARD/Spec are valid.

### `03.specs`

- [ ] Contracts, data models, and verification plan are defined.
- [ ] API/Agent design docs are included when needed.

### `04.execution/plans`

- [ ] Phases, risks, gates, and rollback strategy are documented.
- [ ] Plan links to source specs and tasks.
- [ ] Verification plan defines validation commands and pass criteria.

### `04.execution/tasks`

- [ ] Each task references parent plan/spec.
- [ ] Validation commands and evidence are attached.
- [ ] Verification summary separates local, CI-only, and skipped evidence lanes.

### `05.operations/guides`

- [ ] Audience, prerequisites, and reproducible steps are clear.
- [ ] Cross-links to specs, policies, and runbooks are present.

### `05.operations/policies`

- [ ] Policy controls and promotion criteria are explicit.
- [ ] Security and evidence-retention requirements are defined.

### `05.operations/runbooks`

- [ ] Step-by-step execution and recovery paths are operational.
- [ ] Validation and escalation paths are explicit.

### `05.operations/incidents`

- [ ] Timeline, impact, evidence, and mitigations are recorded.
- [ ] Related runbook links are attached.
- [ ] Postmortem RCA, preventive actions, and follow-up links are recorded as `docs/05.operations/incidents/YYYY/INC-###-<title>/postmortem.md` when needed.

### `98.archive`

- [ ] Original docs subpath is mirrored under `docs/98.archive/`.
- [ ] Tombstone body contains metadata only and no old full body text.
- [ ] Current replacement and implementation evidence are linked.
- [ ] Active docs link archive content only through `docs/98.archive/README.md`.

## Validation and Refresh

Run `python3 scripts/validate-markdown-profiles.py --root . --mode strict`,
`python3 scripts/validate-links-and-owners.py --root . --mode strict`, and
`bash scripts/validate-repo-quality-gates.sh .` after checklist changes. Review
the affected checklist whenever the stage matrix, a template completion
contract, or evidence vocabulary changes.

## Related Documents

- [Stage Authoring Matrix](stage-authoring-matrix.md)
- [Preflight Checklist](preflight-checklist.md)
- [Postflight Checklist](postflight-checklist.md)
- [Agent Quality Standards](quality-standards.md)
