---
title: "W03 Form Target Adoption"
version: "0.3.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-17"
artifact_id: "SPEC-0221-TSK-0001"
parent_ids: ["SPEC-0221-PLAN-0001"]
---

# Task: W03 Form Target Adoption

## Scope

### Objective and Parent

This Task executes WORK-001 to WORK-006 of the [Plan](../plan.md) for [SPEC-0221](../spec.md) criteria VAL-FORM-001 to VAL-FORM-003. Completion evidence is the strict validators, the `document` suite, staged QA and the independent review.

### Inputs and Authority

- **Request:** on 2026-11-17 (Asia/Seoul) the user applied the 4.2.0 W03-FORMS prompt to this workspace with the standing limits, and asked the agent to continue until completion and fix errors at their cause. The package is `_workspace/workspace_governance_4_2_0_20261116/`.
- **Decision:** the agent found that twelve role forms differ from the package's template design targets 4.0.0 (`dependencies/template-design-targets.json`, SHA-256 `3ac2806ec2db8b9f7cd320faa1b5bfe36675624555e63269783be8cdc2039a0e`). The completed W03-FORMS work checked the 3.0.1 targets (`3e829e5e141d7d5ad9d7379de90de7fd34b2cbda4544292f91bb7bd3bd14fea2`). The agent asked how to handle the difference, and the user chose the option `후보 전면 채택` (adopt the candidate in full): adopt the candidate for the twelve roles together with their documents, registry, schema, validators and tests. The choice approves no Spec or Plan bytes and no criterion.
- **Base:** `main` at `7b91d3da`; branch `claude/w03-form-adoption`.
- **Design summary:**
  - Reference designs: D01, D02, D03 and D24 of package 4.2.0.
  - Choice: target H2 and H3 titles and section IDs; former H3 kept as H4 when merged; retained form for four approved identities.
  - Alternatives not taken: keeping the current trees with a mapping table, and adopting only some roles.
  - Failure: the registry form check refuses an old tree.
  - Acceptance: VAL-FORM-001 to VAL-FORM-003.

- **Allowed Paths**: `docs/99.templates/`, the current documents of the twelve roles named in the Spec, `scripts/`, `tests/`, `.agents/governance/`, `docs/*/AGENTS.md`, `docs/03.specs/0221-w03-form-target-adoption/`, `docs/03.specs/README.md`, `docs/03.specs/work-residue-ledger.json`, `docs/01.requirements/0003-workspace-agent-governance-platform.md` (moved headings and Archived Lineage only), `.secrets.baseline` (reviewed line moves only)
- **Forbidden Paths**: `_workspace/`, `docs/98.archive/`, `docs/03.specs/0161-w00-v14-7-delta-intake/spec.md`, `docs/03.specs/0161-w00-v14-7-delta-intake/plan.md`, `gitops/`, `infrastructure/`, `.github/workflows/`
- **Approval Required**: Spec and Plan approval; criterion acceptance; push, pull request and merge
- **Static Validation**: strict document validators, ledger gate, focused tests, `scripts/run-contract-tests.py --suite document`, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface in scope
- **Secret / Vault Handling**: no secret read or printed
- **Rollback Plan**: delete the branch `claude/w03-form-adoption`; `main` is unchanged
- **Evidence Location**: this Task

## Execution Log

### Work Performed

On 2026-11-17 the agent compared the targets with the registry `common_forms` and with the actual H2 and H3 trees of the current documents of each role, then drafted this package.

WORK-001 changed the spec and plan forms, their two templates, the synthetic SPEC-0140 completion fixture and the readers of their section IDs. Three implementation choices sit inside the approved Spec:

- **One MAJOR for the common contract.** The registry check binds every COMMON-DOC-FORM-1 TemplateDefinition to the version of `common_forms`. So the common contract moves from 1.0.0 to 2.0.0 once, and all 20 of its TemplateDefinitions move with it. WORK-002 to WORK-005 stay inside 2.0.0.
- **Retained body-contract location.** The retained form gains an optional `body_contract` (section and table heading), which the schema allows only on a retained form. `DocumentProfile.body_contract_location` reads it, so the four retained identities keep their Lifecycle Traceability or Work Breakdown table where they were approved. The markdown profile, link and lifecycle readers use that one method.
- **Spec references.** The two References H3 of the Spec template move as two H4 (Normative and Evidence, Historical and Navigation) under Verification Strategy. The Plan's `Global Constraints` H4 moves to Constraints, after that section's text, and the lifecycle reader takes it from `plan.intent.2`.

The first `document` suite run on the WORK-001 tree failed 8 cases in four tests. Three fixtures still placed the Spec table under References or matched a Criteria section by a following H2, and the version comparison tests assumed a 1.x common contract. Each fixture now uses the new position or a version relative to the current one; no assertion was removed.

### Blockers and Decisions

The user approved the Spec and Plan (EVD-002), with acceptance on green checks. No question is open.

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-FORM-001](../spec.md#criteria), [VAL-FORM-003](../spec.md#criteria) | Spec and plan forms and the retained form | platform | in-progress | NOT_RUN | EVD-001 |
| WORK-002 | [VAL-FORM-001](../spec.md#criteria), [VAL-FORM-002](../spec.md#criteria) | Requirement and architecture forms and documents | platform | in-progress | NOT_RUN | EVD-001 |
| WORK-003 | [VAL-FORM-001](../spec.md#criteria), [VAL-FORM-002](../spec.md#criteria) | Operations and policy forms and documents | platform | ready | NOT_RUN | EVD-001 |
| WORK-004 | [VAL-FORM-001](../spec.md#criteria), [VAL-FORM-002](../spec.md#criteria) | Skill form and documents | platform | ready | NOT_RUN | EVD-001 |
| WORK-005 | [VAL-FORM-001](../spec.md#criteria), [VAL-FORM-002](../spec.md#criteria) | README forms and documents | platform | ready | NOT_RUN | EVD-001 |
| WORK-006 | [VAL-FORM-003](../spec.md#criteria) | Residue, independent review and the `document` suite | platform | ready | NOT_RUN | EVD-001 |

## Verification Evidence

### Results

| Evidence ID | Consumer | Work Unit | Command | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-FORM-001](../spec.md#criteria) | WORK-001 | Strict document validators and staged QA | Implementation snapshot of each work unit | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-FORM-001](../spec.md#criteria) | WORK-001 | Spec/Plan approval | Direct current-session user answer `승인, 녹색이면 수용 (권장)` (approve, accept when green) to the SPEC-0221 approval question naming spec.md `c19ed378` and plan.md `722984da` of in-review commit `1c81056a`, 2026-11-17; risk class `high` | PASS | Approves the reviewed Spec and Plan content of `1c81056a`; the approved files differ from it only in `status` and `version`. The same answer accepts VAL-FORM-001 to VAL-FORM-003 on the condition that the strict validators, the `document` suite, staged QA and the independent review pass; later rows check that condition. | yes | none |
| EVD-003 | [VAL-FORM-001](../spec.md#criteria) | WORK-001 | Failing first | `python3 -m unittest tests.test_common_form_tree.SpecPlanFormTests tests.test_common_form_tree.RetainedSpecPlanTests tests.test_task_execution_contract` with the changed tests over an export of `2cc30e27` (registry and code before the change); pinned `hyhome-validation` venv, 2026-11-17 | PASS | Observed the defect: 82 tests, 28 failures and 1 error. The old registry has neither the new trees nor the retained forms. | yes | none |
| EVD-004 | [VAL-FORM-001](../spec.md#criteria), [VAL-FORM-003](../spec.md#criteria) | WORK-001 | Focused tests and registry check after the change | `python3 -m unittest tests.test_common_form_tree tests.test_task_execution_contract tests.test_document_lifecycle_cumulative_history`; `python3 scripts/validate-document-contract-registry.py --root . --mode strict`; pinned venv, 2026-11-17 | PASS | 535 tests, OK with 3 skips; registry strict PASS over 297 paths. The four retained identities pass their approved tree and keep their table location. A fifth identity in the old tree, or a retained identity in another status, is refused. | yes | none |
| EVD-005 | [VAL-FORM-001](../spec.md#criteria) | WORK-001 | Strict document validators and staged QA | `python3 scripts/qa.py staged` on the WORK-001 index; pinned venv, 2026-11-17 | PASS | Every selected gate passed on the exact index before the commit; the commit hooks repeat it. | yes | EVD-001 |

### Resolution Links

The Resolves column names the earlier row each PASS row closes: EVD-005 closes EVD-001 for WORK-001. EVD-003 records the observed failing-first run, and EVD-004 the passing run after the change.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-FORM-001](../spec.md#criteria) | pending | none | Run WORK-001 to WORK-005 and their checks | platform |
| [VAL-FORM-002](../spec.md#criteria) | pending | none | Run WORK-002 to WORK-005 and their checks | platform |
| [VAL-FORM-003](../spec.md#criteria) | pending | none | Run WORK-001 and WORK-006 | platform |

### Remaining Conditions

WORK-002 to WORK-006, the independent review and the user's acceptance remain.

## Handoff

### Promotion Receipt

The Plan's FORM-TREES row is not yet reflected.

### Next Owner

The agent runs WORK-002 to WORK-005, then WORK-006.
