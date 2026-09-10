---
title: "Admit Coverage Roles and Repair Routing"
version: "0.1.0"
type: "sdlc/task"
status: "done"
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

It is done. WP-001 through WP-007 have run;
each row below carries the command result actually read, and a row that has
not run says so rather than anticipating an outcome.

One package deviated from its own procedure. In WP-001 the architect body was
committed before the staged gate result was read, and the gate then reported
`LIFECYCLE-CREATE ... expected="create in zero-indegree lifecycle state
('draft',)" observed="absent -> active"`. The `governance/role` lifecycle
domain declares no edge from `active` back to `draft`, and Git policy prefers
a forward corrective commit over amending, so the body stays `active` and the
skipped creation state is recorded here rather than repaired. The four
remaining bodies were created as `draft` and transitioned in WP-007.

Two defects in this package's own plan were found while executing it and are
recorded rather than silently corrected. The plan predicted
`AGENT-REGISTRY-PROJECTION` for a registry entry whose projections are absent
while the validator reports `AGENT-NATIVE-METADATA`; and no package step
filled the six supervisor edges the registry already omitted, although the
specification named that repair. A third was found in WP-007: a role body can
state a routing edge in its Role section that the registry does not carry, and
three admitted roles did. All three are corrected in the tree and in the
contract documents.

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
| [WORK-001](../plan.md#work-breakdown) | VAL-ARCC-001 | Admit `architect` with its body, projections, router row and evaluation case | platform | Done | `architect` admitted at tier `#top` with skills `requirements-to-design` and `docs-stage-routing`; both projections derived from the registry; router Architecture section and Item Index updated; positive evaluation case added | Commit `114973cc`; governance validator FAIL `AGENT-NATIVE-METADATA` before the projections and PASS after at roles=13; evaluation gate PASS. Deviation: committed before the staged gate was read, see Overview |
| [WORK-002](../plan.md#work-breakdown) | VAL-ARCC-010 | State the `architect` and `doc-writer` boundary from both sides | platform | Done | `doc-writer` now excludes Stage 02 structure and states the wiki-curator navigation edge from its side, matching the reciprocal sentence the architect body carries | Commit `66305bcb`; link and owner validation PASS; staged QA 7 gates PASS |
| [WORK-003](../plan.md#work-breakdown) | VAL-ARCC-002 | Admit `governance-steward` with its body, projections, router row and evaluation case | platform | Done | `governance-steward` admitted at tier `#top`; a change to its own entry, body or projections is an operator stop condition; measurement routed to `agent-evaluator` | Commit `52ce0a1e`; governance validator FAIL then PASS at roles=14, handoffs=44, projections=42; evaluation gate PASS; staged QA 8 gates PASS |
| [WORK-004](../plan.md#work-breakdown) | VAL-ARCC-003 | Admit `ci-workflow-engineer` with its body, projections, router row and negative evaluation case | platform | Done | `ci-workflow-engineer` admitted at tier `#worker` owning `.github/`; permission widening, `pull_request_target` and mutable action references are stop conditions | Commit `f7abf332`; governance validator FAIL then PASS at roles=15; negative case observed `boundary` exactly as declared; staged QA 8 gates PASS |
| [WORK-005](../plan.md#work-breakdown) | VAL-ARCC-003 | Admit `repo-tooling-engineer` with its body, projections, router row and negative evaluation case | platform | Done | `repo-tooling-engineer` admitted at tier `#worker`; the split from the quality engineer is decided by membership in `scripts/validation/registry.json` rather than by filename | Commit `e0a9374a`; governance validator FAIL then PASS at roles=16; negative case observed `groundedness` exactly as declared; staged QA 8 gates PASS |
| [WORK-006](../plan.md#work-breakdown) | VAL-ARCC-011 | Admit `agent-evaluator`, record the runner carve-out reciprocally, and close the steward edge | platform | Done | `agent-evaluator` admitted at tier `#worker` owning `evals/`, the runner and its regression test; the steward edge closed in both directions; the runner carve-out stated in `repo-tooling-engineer` | Commit `25954579`; governance validator FAIL then PASS at roles=17, handoffs=57, projections=51; negative case observed `success-claim` exactly as declared; staged QA 8 gates PASS |
| [WORK-007](../plan.md#work-breakdown) | VAL-ARCC-007 | Reconcile the router index, run full QA and record lane-separated evidence | platform | Done | Seven declared boundaries each read by at least one body (architecture 1, documentation 3, infrastructure 3, operations 2, quality 5, security 1, supervision 2). `supervisor.handoff_to` completed to sixteen peers, which the admitting packages had left at ten. Four admitted bodies stated a routing edge the registry did not carry, so `doc-writer` gained `architect`, `ci-workflow-engineer` gained `repo-tooling-engineer`, and `repo-tooling-engineer` gained `agent-evaluator` and `ci-workflow-engineer`; handoffs went from 63 to 67. Four bodies transitioned `draft` to `active` | Boundary anchor count and empty unreachable-peer list observed; the body-to-registry edge comparison reports nothing for all seventeen roles after the four additions and reported nothing for the original twelve before them, which is what establishes the convention; six static validators plus the evaluation gate PASS; provenance cycle present once and no upstream persona frontmatter key in the tree; `python3 scripts/qa.py full` PASS with 22/22 gates on the final tree |

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

Executed repository-static commands. Each admitting package ran
`python3 scripts/validate-agent-governance.py` before its projections existed
and read `ERR AGENT-NATIVE-METADATA agent registry validation failed` with
exit code 1, then ran the same command after and read PASS. The registry grew
from twelve roles to seventeen with handoffs 40, 44, 48, 52 and 57 at the
respective passes and sixty-three after the supervisor roster was completed.
`python3 scripts/run-agent-evaluations.py --root .` reports fourteen cases,
all `synthetic`, eight of them negative, and each added negative case observed
exactly the criterion it declared: `boundary`, `groundedness` and
`success-claim`.

The commands the plan names:
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

One provider-runtime observation was made and is recorded in its own lane
rather than folded into the static results. After the `ci-workflow-engineer`
and `governance-steward` entries were committed, the running Claude session
listed both as available agent types without being restarted. That is direct
evidence of native discovery of those two projections in that client at that
moment. It is not evidence of permission enforcement, model resolution,
delegation or authenticated operation, and it says nothing about the Codex
projections, which were not observed at run time.

Lanes that this Task does not execute and will not claim: native permission
enforcement, model resolution, authenticated operation, hosted
continuous-integration results, and discovery of any projection other than the
two named above. A repository-static PASS is evidence of declared
configuration only. An evaluation cycle whose responses are all `synthetic` is
evidence of harness wiring and criterion behaviour, never of agent quality.

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
| [WORK-001](../plan.md#work-breakdown) | Done | Commit `114973cc`; governance validator FAIL `AGENT-NATIVE-METADATA` before the projections and PASS after at roles=13; evaluation gate PASS. Deviation: committed before the staged gate was read, see Overview |
| [WORK-002](../plan.md#work-breakdown) | Done | Commit `66305bcb`; link and owner validation PASS; staged QA 7 gates PASS |
| [WORK-003](../plan.md#work-breakdown) | Done | Commit `52ce0a1e`; governance validator FAIL then PASS at roles=14, handoffs=44, projections=42; evaluation gate PASS; staged QA 8 gates PASS |
| [WORK-004](../plan.md#work-breakdown) | Done | Commit `f7abf332`; governance validator FAIL then PASS at roles=15; negative case observed `boundary` exactly as declared; staged QA 8 gates PASS |
| [WORK-005](../plan.md#work-breakdown) | Done | Commit `e0a9374a`; governance validator FAIL then PASS at roles=16; negative case observed `groundedness` exactly as declared; staged QA 8 gates PASS |
| [WORK-006](../plan.md#work-breakdown) | Done | Commit `25954579`; governance validator FAIL then PASS at roles=17, handoffs=57, projections=51; negative case observed `success-claim` exactly as declared; staged QA 8 gates PASS |
| [WORK-007](../plan.md#work-breakdown) | Done | Boundary anchor count and empty unreachable-peer list observed; the body-to-registry edge comparison reports nothing for all seventeen roles after the four additions and reported nothing for the original twelve before them, which is what establishes the convention; six static validators plus the evaluation gate PASS; provenance cycle present once and no upstream persona frontmatter key in the tree; `python3 scripts/qa.py full` PASS with 22/22 gates on the final tree |
