---
title: "Agent Surface Deferred Conformance"
version: "0.3.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-06"
layer: "specs"
artifact_id: "SPEC-0145-TSK-0001"
parent_ids: ["SPEC-0145-PLAN-0001"]
---

# Task: Agent Surface Deferred Conformance

## Overview

Handle the six items SPEC-0144 deferred. It executes [SPEC-0145](../spec.md)
through [WORK-001–004](../plan.md#work-breakdown).

## Inputs

- Request (2026-11-06): handle the deferred items and finish.
- Approval (2026-11-06): the operator's instruction to handle the deferred
  items and finish approves SPEC-0145 and its Plan, drafted in `87e32afd`, and the
  delivery through a pull request and merge; it also accepts the criteria once
  their evidence passes.
- Start: branch `docs/agents-deferred` from `main` at `18b76c17`.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-DEF-003](../spec.md#success-criteria--verification-plan) | Derived projection fields | platform | in-progress | PASS | EVD-005, EVD-006 |
| WORK-002 | [VAL-DEF-001](../spec.md#success-criteria--verification-plan) | Role-body shared sections | platform | in-progress | PASS | EVD-007, EVD-008 |
| WORK-003 | [VAL-DEF-002](../spec.md#success-criteria--verification-plan) | Collection-index README subsections | platform | in-progress | PASS | EVD-009 |
| WORK-004 | [VAL-DEF-004](../spec.md#success-criteria--verification-plan) | `sdlc.md` invariant, CIS numbers, sibling pin | platform | in-progress | PASS | EVD-010 |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-DEF-003](../spec.md#success-criteria--verification-plan) | WORK-001 | Regression test and agent-governance validator | Pending | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-DEF-001](../spec.md#success-criteria--verification-plan) | WORK-002 | Strict document checks and agent-governance tests | Pending | NOT_RUN | Pending | yes | none |
| EVD-003 | [VAL-DEF-002](../spec.md#success-criteria--verification-plan) | WORK-003 | Strict document checks | Pending | NOT_RUN | Pending | yes | none |
| EVD-004 | [VAL-DEF-004](../spec.md#success-criteria--verification-plan) | WORK-004 | Source comparison and strict document checks | Pending | NOT_RUN | Pending | yes | none |
| EVD-005 | [VAL-DEF-003](../spec.md#success-criteria--verification-plan) | WORK-001 | Regression test and agent-governance validator | Working tree on `40b97e1e` with the new test and the old registry | FAIL | Local run, 2026-11-06T00:44Z: `test_role_projections_are_derived_not_declared` fails because every role still carries `projections` and `supported_providers` | no | none |
| EVD-006 | [VAL-DEF-003](../spec.md#success-criteria--verification-plan) | WORK-001 | Regression test and agent-governance validator | Working tree on `40b97e1e` with the change | PASS | Local run, 2026-11-06T00:54Z: `tests.test_validate_agent_registry`, `tests.test_agent_governance` and `tests.test_prompt_input` 111 tests OK; `validate-agent-governance.py` PASS with projections=51; `role_projections` derives each path and the stale-or-extra projection comparison is unchanged; the role-level provider checks it replaced were unreachable | yes | EVD-001 |
| EVD-007 | [VAL-DEF-001](../spec.md#success-criteria--verification-plan) | WORK-002 | Independent review of the prose change | Staged index on `40b97e1e`, the whole SPEC-0145 diff | PASS | code-reviewer report: handoff targets match `handoff_to` for all 17 roles and every command, link and anchor exists; one blocking stale CIS cell (`vulnerability-patterns/SKILL.md` 5.2.6) and advisory items (missing `--root .`, undefined lane names, the skill-local checker in quality-engineer's scope, agent-evaluator evidence wording and README link, the dropped registry-ownership sentence, the `sdlc.md` "exactly one" wording) were fixed before this commit | no | none |
| EVD-008 | [VAL-DEF-001](../spec.md#success-criteria--verification-plan) | WORK-002 | Strict document checks and agent-governance tests | Staged index on `9a02b489` | PASS | Local run, 2026-11-06T01:07Z: strict registry, Markdown-profile, link and lifecycle checks PASS; `validate-agent-governance.py` PASS; agent-governance, registry and prompt-input unit tests 111 OK; document suite 282 tests PASS | yes | EVD-002 |
| EVD-009 | [VAL-DEF-002](../spec.md#success-criteria--verification-plan) | WORK-003 | Strict document checks | Staged index on `9a02b489` | PASS | Local run, 2026-11-06T01:07Z: `roles/`, `knowledge/` and `prompts/` READMEs carry `Item Index` (17 roles plus `registry.json` and `registry.schema.json`; 2 maps; 4 prompts) and `Add and Find`; strict checks and `validate-knowledge-surface.py` PASS | yes | EVD-003 |
| EVD-010 | [VAL-DEF-004](../spec.md#success-criteria--verification-plan) | WORK-004 | Source comparison and strict document checks | Staged index on `9a02b489`; kube-bench `cfg/cis-1.9/policies.yaml`; `hy-home.docker` at `63d5b78a` | PASS | 2026-11-06: CIS v1.9 numbers 5.2.7 root, 5.2.2 privileged, 5.2.3–5.2.5 host namespaces, 5.2.12 HostPath, 5.1.3 wildcard, 5.1.5–5.1.6 default service account; the ClusterRole-scope pattern has no matching control and lost its number; the sibling checkout is clean at `63d5b78a` and publishes `127.0.0.1:25432`, `127.0.0.1:25433` and `192.168.0.13:26379` as recorded; `sdlc.md` states the change-kind invariant; strict checks and `validate-service-endpoints.py` PASS | yes | EVD-004 |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-DEF-001](../spec.md#success-criteria--verification-plan) | pending | none | Run EVD-002 | platform |
| [VAL-DEF-002](../spec.md#success-criteria--verification-plan) | pending | none | Run EVD-003 | platform |
| [VAL-DEF-003](../spec.md#success-criteria--verification-plan) | pending | none | Run EVD-001 | platform |
| [VAL-DEF-004](../spec.md#success-criteria--verification-plan) | pending | none | Run EVD-004 | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: `.agents/`, `scripts/validate-agent-governance.py`,
  `tests/test_agent_governance.py`, `tests/test_validate_agent_registry.py`,
  `docs/03.specs/`, `docs/01.requirements/0003-workspace-agent-governance-platform.md`
- **Forbidden Paths**: `docs/99.templates/` registry and schemas, provider
  settings, hooks and projections, `secrets/`, the sibling repository
- **Approval Required**: Spec and Plan approval by the operator; push and
  merge are separate.
- **Static Validation**: regression test, agent-governance validator and
  tests, strict document checks, `python3 scripts/qa.py staged`
- **Live Validation**: not applicable
- **Secret / Vault Handling**: none
- **Rollback Plan**: revert the implementing commits
- **Evidence Location**: this Task

## Verification Summary

- Registry: the derivation regression failed first (EVD-005) and passes with
  the change (EVD-006).
- Prose: an independent review found one blocking stale CIS cell and
  advisory items, all fixed (EVD-007); strict checks, agent-governance tests,
  the knowledge-surface and endpoint checks pass (EVD-008 to EVD-010).
- Sources: CIS v1.9 through kube-bench and the clean sibling checkout.
- Live lane: not applicable. Rollback: revert the implementing commits.
