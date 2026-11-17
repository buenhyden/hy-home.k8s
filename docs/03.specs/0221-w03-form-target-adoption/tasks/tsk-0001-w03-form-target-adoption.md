---
title: "W03 Form Target Adoption"
version: "0.7.0"
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

The first `document` suite run on the WORK-001 tree failed 8 cases in four tests. Three fixtures still placed the Spec table under References or matched a Criteria section by a following H2, and the version comparison tests assumed a 1.x common contract. Each fixture now uses the new position or a version relative to the current one; no assertion was removed. WORK-001 is commit `6ec18e41`.

WORK-002 moved the requirement and architecture forms, their two templates, the four Requirements and the four Architecture Descriptions by the Spec map, with every non-heading line kept (80, 85, 801 and 216 lines in the Requirements; 89, 91, 416 and 308 in the descriptions). REQ-0003 keeps its Archived Lineage byte for byte as the last local H3 under Traceability. Each description's new Trade-offs section restates facts from its own Quality and Risks, Decision Links and Overview text, quoted in the Results row. Eight links inside AD-0004, AD-0005 and AD-0007 pointed at a removed anchor; each now names and links its receiving section (Normal Flow, Scenarios, or Context and Boundaries). The Requirements take a PATCH version and the descriptions a MINOR version, because the descriptions gain a section. WORK-002 is commit `c97af061`.

WORK-003 moved the guide, runbook, policy, incident and postmortem forms, their six templates, the guide, the ten runbooks, the five operations policies and the ten governance rules by the Spec map, with every non-heading line kept. The guide's reader list moves from Outcome to the new Audience H3 without new text. Each policy's new Limits section restates the non-guarantees of its own Enforcement and rule text: the five Stage 05 policies in Korean, the governance rules in English. Read-only drafting agents proposed the Limits and Excluded Responsibilities texts, and the agent reviewed them before use. The incident resolution check now reads Resolution > Verified State by section id. Three links that pointed at the removed `#authority` and `#rollback` anchors now name Owner and Recovery or Forward Repair. The meaning-map pointer test no longer counts historical pointers, because each migration replaces its role's map; it now checks that every map naming a recovery proof points to it in the one form. The policies take a MINOR version for the new Limits section, and the guide and runbooks a PATCH version. The first staged run of the `document` suite then failed four cases in two modules whose literals still named `### Recovery Verification` and the guide's `## Verification`; they now name the new headings, and the generator test also asserts that its insertion point exists. WORK-003 is commit `9404749c`; its first commit attempt ran a `git status` beside the hook, which changed the index and failed the hook's snapshot identity check, and the retry without a concurrent Git command passed.

WORK-004 moved the skill form, its two templates, the 17 native skills and the two workflows by the Spec map, with every non-heading line kept. The former Inputs H3 stays as an H4 under When to Use, and the former Completion and Handoff text becomes Outputs > Handoff. Each skill's new Limits section restates the non-guarantees of its own Steps, Failure Handling or Outputs text; a read-only drafting agent proposed the texts, and the agent reviewed them before use. The local Authority Boundary H3 now sits under Trigger, and the Steps table under `skill.procedure.1`. Each skill and workflow takes a MINOR version for the new section. WORK-004 is commit `eafc7cc0`.

WORK-005 moved the root, stage and service README forms, their five templates and the 43 READMEs by the Spec map, with every non-heading line kept. The root README's reader list moves to the new Audience H3, and its role paragraphs and Boundaries to Outcome. Each stage README's new Excluded Responsibilities section restates the out-of-scope and owner text of its own Purpose and Inputs and Outputs; read-only drafting agents proposed 21 of the 22 texts, and the agent wrote the Stage 99 template catalog's text from its own Out of Scope list. The `readme_navigation` sections now name Current Paths, Paths and Purpose. Three adjustments kept the checks intact. First, the gitops README's Secret Management Responsibility Matrix stays an H4 next to Security Boundary, because the README matrix reader deliberately refuses an H5. Second, 23 prose sentences that named a renamed heading (Supported Environment, Local Workflow, Service Role) now name Usage > Prerequisites, Selected Start or Purpose. Third, the document authoring policy's link to Stage 99 `#create-and-review` now points to `#entry-points`. The root and stage READMEs take a MINOR version for the new sections, and the service READMEs a PATCH version.

### Blockers and Decisions

The user approved the Spec and Plan (EVD-002), with acceptance on green checks. No question is open.

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-FORM-001](../spec.md#criteria), [VAL-FORM-003](../spec.md#criteria) | Spec and plan forms and the retained form | platform | completed | PASS | EVD-003, EVD-004, EVD-005 |
| WORK-002 | [VAL-FORM-001](../spec.md#criteria), [VAL-FORM-002](../spec.md#criteria) | Requirement and architecture forms and documents | platform | completed | PASS | EVD-006, EVD-007, EVD-008 |
| WORK-003 | [VAL-FORM-001](../spec.md#criteria), [VAL-FORM-002](../spec.md#criteria) | Operations and policy forms and documents | platform | completed | PASS | EVD-009, EVD-010, EVD-011 |
| WORK-004 | [VAL-FORM-001](../spec.md#criteria), [VAL-FORM-002](../spec.md#criteria) | Skill form and documents | platform | completed | PASS | EVD-012, EVD-013, EVD-014 |
| WORK-005 | [VAL-FORM-001](../spec.md#criteria), [VAL-FORM-002](../spec.md#criteria) | README forms and documents | platform | in-progress | NOT_RUN | EVD-001 |
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
| EVD-006 | [VAL-FORM-001](../spec.md#criteria) | WORK-002 | Failing first | `python3 -m unittest tests.test_common_form_tree.RequirementFormTests tests.test_common_form_tree.ArchitectureFormTests tests.test_common_form_tree.RepositoryRegistryTests` with the changed tests over an export of `f2e3aeb0`; pinned venv, 2026-11-17 | PASS | Observed the defect: 28 tests, 36 failures against the old requirement and architecture forms. | yes | none |
| EVD-007 | [VAL-FORM-002](../spec.md#criteria) | WORK-002 | Focused tests and strict validators after the change | `python3 -m unittest tests.test_common_form_tree tests.test_documentation_link_boundary`; the strict registry, markdown profile, link and lifecycle validators over the whole tree; pinned venv, 2026-11-17 | PASS | Every listed check passed after the fixture repairs. The Trade-offs texts: AD-0004 shared controller and pinned requests and limits; AD-0005 shared-channel subscriptions and the OpenBao, ESO and Secret token path; AD-0006 once-per-input selection and separate evidence classes; AD-0007 the ADR-0042 single-host budget and the static-versus-live boundary. | yes | none |
| EVD-008 | [VAL-FORM-002](../spec.md#criteria) | WORK-002 | Strict document validators and staged QA | `python3 scripts/qa.py staged` on the WORK-002 index and the commit hooks of `c97af061`; pinned venv, 2026-11-17 | PASS | 12 selected gates passed on the exact index, and the hooks passed at the commit. | yes | none |
| EVD-009 | [VAL-FORM-001](../spec.md#criteria) | WORK-003 | Failing first | The runbook, incident, postmortem, operations policy and guide registry test classes of `tests.test_common_form_tree`, with the changed tests over an export of `c97af061`; pinned venv, 2026-11-17 | PASS | Observed the defect: 62 tests, 45 failures against the old forms. | yes | none |
| EVD-010 | [VAL-FORM-002](../spec.md#criteria) | WORK-003 | Focused tests and strict validators after the change | `python3 -m unittest tests.test_common_form_tree tests.test_document_terminal_contract tests.test_operations_section_contract tests.test_operations_lineage_contract tests.test_policy_rule_ids`; the strict registry, markdown profile, link, lifecycle, agent governance and knowledge surface validators; pinned venv, 2026-11-17 | PASS | 515 tests OK with 3 skips; every listed validator passed. A quality-engineer agent moved 57 fixtures to the new trees without removing an assertion. | yes | none |
| EVD-011 | [VAL-FORM-002](../spec.md#criteria) | WORK-003 | Strict document validators and staged QA | `python3 scripts/qa.py staged` on the WORK-003 index and the commit hooks of `9404749c`; pinned venv, 2026-11-17 | PASS | 14 selected gates, the `document` suite among them, passed on the exact index, and the hooks passed at the commit. | yes | none |
| EVD-012 | [VAL-FORM-001](../spec.md#criteria) | WORK-004 | Failing first | `python3 -m unittest tests.test_common_form_tree tests.test_native_skill_envelope tests.test_common_agents_document_routes` with the changed tests over an export of `9404749c`; pinned venv, 2026-11-17 | PASS | Observed the defect: 424 tests, 29 failures against the old skill form. | yes | none |
| EVD-013 | [VAL-FORM-002](../spec.md#criteria) | WORK-004 | Focused tests and strict validators after the change | The same three modules; the strict registry, markdown profile, link and lifecycle validators, and the agent governance and knowledge surface validators; pinned venv, 2026-11-17 | PASS | 424 tests OK with 3 skips; registry strict PASS over 297 paths; every listed validator passed. | yes | none |
| EVD-014 | [VAL-FORM-002](../spec.md#criteria) | WORK-004 | Strict document validators and staged QA | `python3 scripts/qa.py staged` on the WORK-004 index and the commit hooks of `eafc7cc0`; pinned venv, 2026-11-17 | PASS | 14 selected gates, the `document` suite among them, passed on the exact index, and the hooks passed at the commit. | yes | none |
| EVD-015 | [VAL-FORM-001](../spec.md#criteria) | WORK-005 | Failing first | `python3 -m unittest tests.test_common_form_tree tests.test_readme_navigation` with the changed tests over an export of `eafc7cc0`; pinned venv, 2026-11-17 | PASS | Observed the defect: 452 tests, 34 failures against the old README forms. | yes | none |
| EVD-016 | [VAL-FORM-002](../spec.md#criteria) | WORK-005 | Focused tests and strict validators after the change | The same two modules with `tests.test_semver_versions`, `tests.test_validate_knowledge_surface`, `tests.test_document_lifecycle_cumulative_history`, `tests.test_operations_lineage_contract`, `tests.test_prompt_input`, `tests.test_repository_quality_rules`, `tests.test_native_skill_envelope` and `tests.test_common_agents_document_routes`; the strict registry, markdown profile, link and lifecycle validators; pinned venv, 2026-11-17 | PASS | 615 tests OK with 3 skips; registry strict PASS over 297 paths; every listed validator passed after the matrix, prose and anchor repairs. | yes | none |

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
