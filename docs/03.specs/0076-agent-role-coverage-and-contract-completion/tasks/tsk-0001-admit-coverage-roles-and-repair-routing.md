---
title: "Admit Coverage Roles and Repair Routing"
version: "0.1.0"
type: "sdlc/task"
status: "queued"
owner: "platform"
updated: "2026-09-10"
layer: "specs"
artifact_id: "SPEC-0076-TSK-0001"
---

# Task: Admit Coverage Roles and Repair Routing

## Overview

This Task owns execution for [SPEC-0076](../spec.md) through the ordered work
packages in [the plan](../plan.md). It records per-package results, the evidence
lane each result belongs to, the approval boundaries observed, and the limits
that remain unobserved.

It is queued. No package has run, and every row below says so rather than
anticipating an outcome. A row moves to a result only when the command that
produced it has been executed and its output read.

## Inputs

- [SPEC-0076](../spec.md) for the change contract and the criteria.
- [Implementation Plan](../plan.md) for ordered packages, entry gates, and exit
  evidence.
- [Work lifecycle](../../../../.agents/workflows/work-lifecycle.md) for intake,
  bounded implementation, and completion.
- [Approval and safety](../../../../.agents/governance/approval-and-safety.md)
  for protected actions.
- [Quality policy](../../../../.agents/governance/quality.md) for lane
  meanings, the completion sequence, and the handoff fields.
- [Agent registry](../../../../.agents/roles/registry.json) for current role
  membership, permission classes, and projection paths.
- [Responsibility router](../../../../.agents/roles/README.md) for the seven
  declared boundaries.
- Baseline observation: branch `main`, HEAD `1e86f86d`, registry holding twelve
  roles, seven declared boundaries of which the role bodies read six.
- Upstream observation: `msitarzewski/agency-agents` head
  `6d29a9b08785a0e49ffc9818bbdd381164c2df5f`, dated 2026-09-09, MIT licensed,
  observed 2026-09-10 and recorded by
  [RES-0001-m0009](../../../90.references/research/0001-workspace-engineering/m0009-ai-agents-and-agency-agents.md).

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| [WORK-001](../plan.md#work-breakdown) | VAL-ARCC-001 | Admit `architect` with its body, projections, router row and evaluation case | platform | Queued | Not run | None recorded |
| [WORK-002](../plan.md#work-breakdown) | VAL-ARCC-010 | State the `architect` and `doc-writer` boundary from both sides | platform | Queued | Not run | None recorded |
| [WORK-003](../plan.md#work-breakdown) | VAL-ARCC-002 | Admit `governance-steward` with its body, projections, router row and evaluation case | platform | Queued | Not run | None recorded |
| [WORK-004](../plan.md#work-breakdown) | VAL-ARCC-003 | Admit `ci-workflow-engineer` with its body, projections, router row and negative evaluation case | platform | Queued | Not run | None recorded |
| [WORK-005](../plan.md#work-breakdown) | VAL-ARCC-003 | Admit `repo-tooling-engineer` with its body, projections, router row and negative evaluation case | platform | Queued | Not run | None recorded |
| [WORK-006](../plan.md#work-breakdown) | VAL-ARCC-011 | Admit `agent-evaluator`, record the runner carve-out reciprocally, and close the steward edge | platform | Queued | Not run | None recorded |
| [WORK-007](../plan.md#work-breakdown) | VAL-ARCC-007 | Reconcile the router index, run full QA and record lane-separated evidence | platform | Queued | Not run | None recorded |

## Approval and Safety Boundaries

- Authoring is bounded to `.agents/roles/`, `.claude/agents/`,
  `.codex/agents/`, `evals/` and this Stage 03 package. No other tree is
  written by this Task.
- No permission class, provider block or permission scope is changed, and no
  projection is authored independently of the registry that derives it.
- No lane membership in `scripts/validation/registry.json` is changed.
- Push, merge, release and any hosted or live execution are outside this Task
  and are not assumed by any package.
- No secret value, credential or personal identifier enters an evaluation case
  or a recorded response.
- A self-directed change to the `governance-steward` definition, once that role
  exists, is an operator decision and is not taken here.

## Verification Summary

Planned repository-static commands, none yet executed:
`python3 scripts/json_schema_validation.py`,
`python3 scripts/validate-agent-governance.py`,
`python3 scripts/validate-markdown-profiles.py`,
`python3 scripts/validate-links-and-owners.py`,
`python3 scripts/validate-knowledge-surface.py`,
`python3 scripts/run-agent-evaluations.py --root .`,
`python3 scripts/qa.py staged` per logical commit, and
`python3 scripts/qa.py full` before handoff.

Each admitting package demonstrates the governance validator failing on the
missing projections before writing them, then passing after, so the change is
evidenced by a focused failing case and its passing result rather than by a
single green run.

Lanes that this Task does not execute and will not claim: provider discovery of
the admitted roles, native permission enforcement, model resolution,
authenticated operation, and hosted continuous-integration results. A
repository-static PASS is evidence of declared configuration only. An
evaluation cycle whose responses are all `synthetic` is evidence of harness
wiring and criterion behaviour, never of agent quality.

## Traceability

This Task executes [SPEC-0076](../spec.md) through
[the plan](../plan.md). Requirement lineage runs to
[REQ-0003](../../../01.requirements/0003-workspace-agent-governance-platform.md)
and the structural view in
[AD-0006](../../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md).
External catalogue provenance is owned by
[RES-0001-m0009](../../../90.references/research/0001-workspace-engineering/m0009-ai-agents-and-agency-agents.md)
and is not restated here.

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-001](../plan.md#work-breakdown) | Not run | None recorded |
| [WORK-002](../plan.md#work-breakdown) | Not run | None recorded |
| [WORK-003](../plan.md#work-breakdown) | Not run | None recorded |
| [WORK-004](../plan.md#work-breakdown) | Not run | None recorded |
| [WORK-005](../plan.md#work-breakdown) | Not run | None recorded |
| [WORK-006](../plan.md#work-breakdown) | Not run | None recorded |
| [WORK-007](../plan.md#work-breakdown) | Not run | None recorded |
