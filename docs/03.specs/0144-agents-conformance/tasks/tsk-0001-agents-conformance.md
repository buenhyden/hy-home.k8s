---
title: "Agent Surface Conformance"
version: "0.3.1"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-06"
layer: "specs"
artifact_id: "SPEC-0144-TSK-0001"
parent_ids: ["SPEC-0144-PLAN-0001"]
---

# Task: Agent Surface Conformance

## Overview

Correct the `.agents/` files against their governance, forms and the current
workspace. It executes [SPEC-0144](../spec.md) through
[WORK-001–004](../plan.md#work-breakdown).

## Inputs

- Request (2026-11-06): check every `.agents/` file against its governance,
  form and the current workspace, and remove conflicts, contradictions and
  duplication.
- Operator choices (2026-11-06): the correctness-and-code scope; bind
  `ops-runbook` to `doc-writer`; remove only the unread schema field.
- Approval (2026-11-06): the operator approved SPEC-0144 and its Plan after
  review of the draft in `d541fb8a`, and asked for a pull request and merge;
  that choice also accepts the criteria once their evidence passes.
- Start: branch `docs/agents-conformance` from `main` at `75ba7b04`.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-AGC-004](../spec.md#success-criteria--verification-plan) | Code, registry and schema changes | platform | completed | PASS | EVD-005, EVD-006, EVD-007 |
| WORK-002 | [VAL-AGC-001](../spec.md#success-criteria--verification-plan) | Governance files | platform | completed | PASS | EVD-008, EVD-009, EVD-010, EVD-011 |
| WORK-003 | [VAL-AGC-002](../spec.md#success-criteria--verification-plan) | Roles and skills | platform | completed | PASS | EVD-012 |
| WORK-004 | [VAL-AGC-003](../spec.md#success-criteria--verification-plan) | README, knowledge, prompts, workflows, evaluations | platform | completed | PASS | EVD-013 |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-AGC-004](../spec.md#success-criteria--verification-plan) | WORK-001 | Regression tests and agent-governance validator | Pending | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-AGC-001](../spec.md#success-criteria--verification-plan) | WORK-002 | Strict document checks | Pending | NOT_RUN | Pending | yes | none |
| EVD-003 | [VAL-AGC-002](../spec.md#success-criteria--verification-plan) | WORK-003 | Strict document checks and agent-governance validator | Pending | NOT_RUN | Pending | yes | none |
| EVD-004 | [VAL-AGC-003](../spec.md#success-criteria--verification-plan) | WORK-004 | Strict document checks | Pending | NOT_RUN | Pending | yes | none |
| EVD-005 | [VAL-AGC-004](../spec.md#success-criteria--verification-plan) | WORK-001 | Regression tests and agent-governance validator | Working tree on `c8f2ddba` with the new tests and the old code | FAIL | Local run, 2026-11-05T23:48Z: `test_change_review_reports_whitespace_errors_instead_of_aborting` raises `PROMPT-INPUT-FAILED: Whitespace check: command exited 2`; `test_doc_update_owner_candidates_include_the_root_routers` misses `docs/README.md`; at 23:49Z `test_every_registered_skill_has_a_binding_role` reports `ops-runbook` unbound and `test_permission_class_carries_no_unread_approval_flag` fails with `AGENT-REGISTRY-SCHEMA` | no | none |
| EVD-006 | [VAL-AGC-004](../spec.md#success-criteria--verification-plan) | WORK-001 | Regression tests and agent-governance validator | Working tree on `c8f2ddba` with the change | PASS | Local run, 2026-11-05T23:49Z: `tests.test_prompt_input` and `tests.test_validate_agent_registry` 50 tests OK; `tests.test_agent_governance` 61 tests OK; `validate-agent-governance.py` PASS (roles=17, skills=17, projections=51) | yes | EVD-001 |
| EVD-007 | [VAL-AGC-004](../spec.md#success-criteria--verification-plan) | WORK-001 | Changed surfaces | Working tree on `c8f2ddba` | PASS | `prompt-input.py` accepts exit 2 only for `git diff --check` and its allowlist gains `docs/README.md` and `.agents/*.md`, with the `doc-update` contract row changed to match; `doc-writer` binds `ops-runbook` in the registry and both projections; `external_writes_require_approval` is gone from the schema and the four registry rows | no | none |
| EVD-008 | [VAL-AGC-001](../spec.md#success-criteria--verification-plan) | WORK-002 | Independent review of the prose change | Working tree on `48384246`, the whole 54-file `.agents/` diff of WORK-002 to WORK-004 | FAIL | code-reviewer report: three blocking defects (a `sdlc.md` table row split across lines; the `vulnerability-patterns` floating-tag cell escalating every tag to CRITICAL; a circular severity deferral with `audit-dimensions.md`) and advisory items (dropped `personal data`, provider-bypass, ambiguous-authority and joint-edition sentences; a Traefik canary claim; SEV attribution; link labels; Korean wording) | no | none |
| EVD-009 | [VAL-AGC-001](../spec.md#success-criteria--verification-plan) | WORK-002 | Independent re-review of the fixes | Staged index on `48384246` after the fixes | PASS | code-reviewer re-review: the three blocking defects are resolved, each `audit-dimensions.md` deferral has a `vulnerability-patterns` row, and the restored rules each appear once; no new blocking issue | no | none |
| EVD-010 | [VAL-AGC-001](../spec.md#success-criteria--verification-plan) | WORK-002 | Changed surfaces | Staged index on `48384246` | PASS | 54 `.agents/` files: 10 governance rules, the roles README and 8 role bodies, 16 skills and 6 skill references, and 13 README, knowledge, prompt, workflow and evaluation files; each changed document has a patch version bump | no | none |
| EVD-011 | [VAL-AGC-001](../spec.md#success-criteria--verification-plan) | WORK-002 | Strict document checks | Staged index on `48384246` | PASS | Local run, 2026-11-06T00:16Z: strict registry, Markdown-profile, link and lifecycle checks PASS; `run-contract-tests.py --suite document` 282 tests PASS; `qa.py staged` rc 0 with 10 gates PASS | yes | EVD-002 |
| EVD-012 | [VAL-AGC-002](../spec.md#success-criteria--verification-plan) | WORK-003 | Strict document checks and agent-governance validator | Staged index on `48384246` | PASS | Local run, 2026-11-06T00:16Z: strict document checks PASS; `validate-agent-governance.py` PASS (roles=17, skills=17, projections=51); `tests.test_agent_governance`, `tests.test_validate_agent_registry` and `tests.test_prompt_input` 111 tests OK; `validate-service-endpoints.py` PASS | yes | EVD-003 |
| EVD-013 | [VAL-AGC-003](../spec.md#success-criteria--verification-plan) | WORK-004 | Strict document checks | Staged index on `48384246` | PASS | Local run, 2026-11-06T00:16Z: strict document checks PASS; `validate-knowledge-surface.py` PASS (2 documents); `tests.test_prompt_input` 24 tests OK | yes | EVD-004 |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-AGC-001](../spec.md#success-criteria--verification-plan) | accepted | EVD-011 | Operator accepted on 2026-11-06 | platform |
| [VAL-AGC-002](../spec.md#success-criteria--verification-plan) | accepted | EVD-012 | Operator accepted on 2026-11-06 | platform |
| [VAL-AGC-003](../spec.md#success-criteria--verification-plan) | accepted | EVD-013 | Operator accepted on 2026-11-06 | platform |
| [VAL-AGC-004](../spec.md#success-criteria--verification-plan) | accepted | EVD-006 | Operator accepted on 2026-11-06 | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: `.agents/`, `.claude/agents/doc-writer.md`,
  `.codex/agents/doc-writer.toml`, `scripts/prompt-input.py`,
  `scripts/validate-agent-governance.py`, `tests/`, `docs/03.specs/`,
  `docs/01.requirements/0003-workspace-agent-governance-platform.md`
- **Forbidden Paths**: `docs/99.templates/` registry and schemas, provider
  settings and hooks, `secrets/`
- **Approval Required**: Spec and Plan approval by the operator; push and
  merge are separate.
- **Static Validation**: regression tests, agent-governance validator,
  document contract suite, strict document checks, `python3 scripts/qa.py staged`
- **Live Validation**: not applicable
- **Secret / Vault Handling**: none
- **Rollback Plan**: revert the implementing commits
- **Evidence Location**: this Task

## Verification Summary

- Code and registry: the four regressions failed first (EVD-005) and pass
  with the change (EVD-006).
- Prose: the first independent review found three blocking defects (EVD-008);
  the fixes passed a re-review (EVD-009), and the strict document checks,
  agent-governance validator, unit tests and `qa.py staged` pass (EVD-011 to
  EVD-013).
- Deferred by the Spec: per-role rewrites of the shared role-body sections,
  new README Item Index tables, the derived schema constants, retyping
  `sdlc.md`, CIS renumbering and the sibling revision pin in the external
  service contract.
- Live lane: not applicable. Rollback: revert the implementing commits.
