---
name: requirements-to-design
description: Use when connecting requirement documents to architecture or design documents, verifying docs/01→02 traceability, or ensuring PRD requirements map to ARD/ADR artifacts in hy-home.k8s.
---

# requirements-to-design

## Purpose

Maintain traceable links between product requirement documents (`docs/01.requirements/`) and
architecture artifacts (`docs/02.architecture/`) in this repository's SDD lifecycle.

## Trigger Phrases

- "trace requirements to design"
- "check requirements coverage"
- "link PRD to architecture"
- "verify 01→02 connection"
- "requirements traceability"
- "which ADR covers this requirement"

## When to Use

- Creating or updating an ARD and needing to confirm which PRD requirements it satisfies.
- Creating an ADR and needing to reference the driving requirement or ARD.
- Auditing whether all PRD requirements have a corresponding architecture artifact.
- Reviewing a new feature request to identify which existing architecture decisions apply.

## When NOT to Use

- Authoring the PRD or ADR content itself; use `docs-stage-routing` to select the template.
- Narrow template conformance or link drift cleanup; use `docs-stage-conformance`.
- Execution planning or task breakdown; use `execution-plan` or `task-breakdown`.

## Workflow Steps

1. Read the target PRD (`docs/01.requirements/`) to extract numbered requirements.
2. Scan `docs/02.architecture/requirements/` for ARDs that reference those requirements.
3. Scan `docs/02.architecture/decisions/` for ADRs that reference the PRD or ARD.
4. Build a coverage matrix: Requirement → ARD → ADR (with status: covered, partial, missing).
5. For each missing or partial coverage, record the gap with the requirement ID and the
   nearest existing artifact that partially addresses it.
6. Report the coverage matrix and gaps. Do not auto-create architecture artifacts;
   present the gap list and recommend which template to use.
7. Update `## Related Documents` in the PRD to list confirmed ARD/ADR links.

## Coverage Matrix Format

| Requirement | Covered By (ARD/ADR) | Status  | Gap / Note                                                 |
| ----------- | -------------------- | ------- | ---------------------------------------------------------- |
| REQ-001     | ARD-0001, ADR-0003   | covered | —                                                          |
| REQ-002     | —                    | missing | No ARD addresses scalability under WSL2 memory constraints |
