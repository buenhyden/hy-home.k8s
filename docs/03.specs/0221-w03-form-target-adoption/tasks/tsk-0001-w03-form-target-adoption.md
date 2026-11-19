---
title: "W03 Form Target Adoption"
version: "0.10.1"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-19"
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
- **Forbidden Paths**: `_workspace/`, `docs/98.archive/`, `docs/03.specs/0161-w00-v14-7-delta-intake/spec.md`, `docs/03.specs/0161-w00-v14-7-delta-intake/plan.md`, every file under `gitops/` and `infrastructure/` except their Spec-scoped `README.md` files, `.github/workflows/`
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

WORK-005 moved the root, stage and service README forms, their five templates and the 43 READMEs by the Spec map, with every non-heading line kept. The root README's reader list moves to the new Audience H3, and its role paragraphs and Boundaries to Outcome. Each stage README's new Excluded Responsibilities section restates the out-of-scope and owner text of its own Purpose and Inputs and Outputs; read-only drafting agents proposed 21 of the 22 texts, and the agent wrote the Stage 99 template catalog's text from its own Out of Scope list. The `readme_navigation` sections now name Current Paths, Paths and Purpose. Three adjustments kept the checks intact. First, the gitops README's Secret Management Responsibility Matrix stays an H4 next to Security Boundary, because the README matrix reader deliberately refuses an H5. Second, 23 prose sentences that named a renamed heading (Supported Environment, Local Workflow, Service Role) now name Usage > Prerequisites, Selected Start or Purpose. Third, the document authoring policy's link to Stage 99 `#create-and-review` now points to `#entry-points`. The root and stage READMEs take a MINOR version for the new sections, and the service READMEs a PATCH version. WORK-005 is commit `7f5e5838`.

WORK-006 recorded the three out-of-scope differences of the Spec as the residue rows W03-H45 to W03-H47, owned by T99-CONFORMANCE, whose prompt compares the common core with the actual forms and classifies unmapped roles. Every new required section (Trade-offs, Limits, Audience, Excluded Responsibilities) holds text from its own document, so none is an empty or N/A section.

An independent read-only code-reviewer agent reviewed `2cc30e27..7f5e5838` and requested changes (EVD-018). The agent fixed each finding in this change:

- **F1, retained Plan rules.** The lifecycle Plan rules and the markdown table check read the Promotion and Constraints sections only by the form's titles, so the retained SPEC-0221 Plan failed PLAN-PROMOTION and PLAN-GLOBAL-CONSTRAINTS at completion and its Promotion table went unchecked. The retained form now carries `section_titles`, the H3 title a retained document keeps for a form section ID, which the schema allows only on a retained form. `CommonForm.section_heading` resolves a section's heading for one status and identity, and the lifecycle and table readers use it. Two RED tests fail first and pass after (EVD-019, EVD-020).
- **F2, stale prose.** 25 runbook, policy and governance sentences that named a removed heading (Actions, Recovery, Validation, Service Checks, Preconditions, Exception Conditions, Scope, Authority) now name the receiving heading, and each document takes a PATCH version.
- **F3, registry prose.** Six registry validation strings now name Resolution, Verified State, Actions, Facts, Escalation and the Plan promotion section ID.
- **F4, coverage.** A test shows the schema refusing `body_contract` and `section_titles` outside a retained form, and an identity test shows a retained title applies only to its bounded identity and status.

F5 (the meaning-map pointer count) is kept as recorded in WORK-003: each migration replaces its role's map, and the test now checks the form of every pointer. F6 is informational; the older-registry fallbacks it names predate this package and stay with W05-H09. The review fixes are commit `4cedd75f`.

At closing the agent found that the Forbidden Paths entry named all of `gitops/` and `infrastructure/`, while the approved Spec scope lists their five service READMEs, which WORK-005 changed. The entry meant the manifests and scripts there, so it now excludes those README files; no manifest or script under either path changed.

### Blockers and Decisions

The user approved the Spec and Plan (EVD-002), with acceptance on green checks. No question is open.

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-FORM-001](../spec.md#criteria), [VAL-FORM-003](../spec.md#criteria) | Spec and plan forms and the retained form | platform | completed | PASS | EVD-003, EVD-004, EVD-005 |
| WORK-002 | [VAL-FORM-001](../spec.md#criteria), [VAL-FORM-002](../spec.md#criteria) | Requirement and architecture forms and documents | platform | completed | PASS | EVD-006, EVD-007, EVD-008 |
| WORK-003 | [VAL-FORM-001](../spec.md#criteria), [VAL-FORM-002](../spec.md#criteria) | Operations and policy forms and documents | platform | completed | PASS | EVD-009, EVD-010, EVD-011 |
| WORK-004 | [VAL-FORM-001](../spec.md#criteria), [VAL-FORM-002](../spec.md#criteria) | Skill form and documents | platform | completed | PASS | EVD-012, EVD-013, EVD-014 |
| WORK-005 | [VAL-FORM-001](../spec.md#criteria), [VAL-FORM-002](../spec.md#criteria) | README forms and documents | platform | completed | PASS | EVD-015, EVD-016, EVD-017 |
| WORK-006 | [VAL-FORM-003](../spec.md#criteria) | Residue, independent review and the `document` suite | platform | completed | PASS | EVD-020, EVD-021, EVD-022 |

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
| EVD-017 | [VAL-FORM-002](../spec.md#criteria) | WORK-005 | Strict document validators and staged QA | `python3 scripts/qa.py staged` on the WORK-005 index and the commit hooks of `7f5e5838`; pinned venv, 2026-11-17 | PASS | 13 selected gates, the `document` suite among them, passed on the exact index, and the hooks passed at the commit. | yes | none |
| EVD-018 | [VAL-FORM-003](../spec.md#criteria) | WORK-006 | Independent review | A read-only code-reviewer agent over `git diff 2cc30e27..7f5e5838`, the Spec and Plan, the strict validators, a completion-mode lifecycle run and seven test modules, 2026-11-17; risk class `high` | FAIL | REQUEST CHANGES: F1 (HIGH) retained Plan fails PLAN-PROMOTION and PLAN-GLOBAL-CONSTRAINTS and its Promotion table is unchecked; F2 and F3 (MEDIUM) prose and registry strings name removed headings; F4 and F5 (LOW) coverage; F6 informational. Meaning preservation, the Spec map and the retained bound verified clean. | yes | none |
| EVD-019 | [VAL-FORM-003](../spec.md#criteria) | WORK-006 | Failing first | `tests.test_common_form_tree.RetainedSpecPlanTests` and `tests.test_task_execution_contract.AdoptedExecutionParentTests.test_a_retained_plan_reads_its_own_promotion_and_constraints` with the new tests over the code of `7f5e5838`; pinned venv, 2026-11-17 | PASS | Observed the defect: PLAN-PROMOTION and PLAN-GLOBAL-CONSTRAINTS raised for the retained Plan, and the table check could not take the document status. | yes | none |
| EVD-020 | [VAL-FORM-003](../spec.md#criteria) | WORK-006 | Focused tests and strict validators after the change | `python3 -m unittest tests.test_common_form_tree tests.test_task_execution_contract`; the strict registry, markdown profile, link and lifecycle validators; `validate-document-lifecycle.py --mode completion --include-path` the SPEC-0221 Spec; pinned venv, 2026-11-17 | PASS | 489 tests OK with 3 skips after the expected-extension update; every strict validator passed; the completion run no longer reports a PLAN rule, and only the acceptance rows still pending report. | yes | none |
| EVD-021 | [VAL-FORM-003](../spec.md#criteria) | WORK-006 | Independent review | The same read-only code-reviewer agent over the staged fix (`git diff --cached` on `7f5e5838`), with a completion-mode lifecycle run, the strict validators and 23 focused tests, 2026-11-17; risk class `high` | PASS | APPROVE: F1 to F3 fixed without widening the retained bound or adding an alias; F5 and F6 accepted. One optional LOW note stays open: no registry check requires a `section_titles` key to name an existing form section, and a wrong key is inert. | yes | EVD-018 |
| EVD-022 | [VAL-FORM-003](../spec.md#criteria) | WORK-006 | Strict document validators and staged QA | `python3 scripts/qa.py staged` on the index of `4cedd75f` (the final code and document tree) and its commit hooks; a separate `scripts/run-contract-tests.py --root . --suite document` run on the WORK-005 tree; pinned venv, 2026-11-17 | PASS | 13 selected gates passed, the `document` contract suite and the work residue ledger gate among them, and the hooks passed at the commit; the separate run passed 1148 tests in 31 modules. | yes | none |
| EVD-023 | [VAL-FORM-003](../spec.md#criteria) | WORK-006 | Residue closure by T99-CONFORMANCE | The SPEC-0222 export of `66fe7808` with the package comparator (sha256 `f6ee2636`) against the 4.0.0 design targets (sha256 `3ac2806e`); pinned venv, 2026-11-18 | PASS | W03-H45: `common_forms.core` binds the 4.0.0 targets, and every core-role form carries their sections, typed tables, metadata policy, relationships and lifecycle. W03-H46: the task form's section IDs are the core IDs `task.scope` to `task.handoff`. W03-H47: every form carries `core_role`. The ADR form maps to decision and AGENTS to agent-instructions, the reference report splits into research, audit and data-reference, and the other forms are classified `domain`. The export returned `DECLARED_CORE_MATCH` with 0 unmapped templates ([SPEC-0222 Task](../../0222-t99-common-core-conformance/tasks/tsk-0001-t99-common-core-conformance.md#results), EVD-039). | yes | none |
| EVD-024 | [VAL-FORM-001](../spec.md#criteria) | WORK-001 | Manual package-exit decision freeze | This package's `spec.md`, `plan.md` and Task; the consumers named below; the user's 2026-11-19 decision "Delete now, move residues (Recommended)" under SPEC-0223; Git-history-only method | PASS | The consumer, preservation, hold, authority and method decision is frozen below before this package's final source commit. Each file's committed `commit:path`, retained-ref reachability and byte comparison are recorded in REQ-0003 Archived Lineage before deletion. An unresolved condition defers the affected deletion. | false | none |

### Resolution Links

The Resolves column names the earlier row each PASS row closes: EVD-005 closes EVD-001 for WORK-001, and EVD-021 closes the review row EVD-018. EVD-003 records the observed failing-first run, and EVD-004 the passing run after the change.

### Residue Handoff

WORK-006 records the Spec's out-of-scope differences here and in `docs/03.specs/work-residue-ledger.json`. Each row names the package prompt that owns the next comparison.

| ID | Residue | State | Owner | Resume condition | Closure |
| --- | --- | --- | --- | --- | --- |
| W03-H45 | The 4.0.0 design targets' table columns and their typed tables, metadata policy, relationships and lifecycle members are not adopted; current tables and columns stay unchanged (Spec Non-goals) | terminal | T99-CONFORMANCE | When T99-CONFORMANCE compares the target core with a real registry export | EVD-023 |
| W03-H46 | The task role keeps its slug section IDs; its headings already match the target (Spec Non-goals) | terminal | T99-CONFORMANCE | When T99-CONFORMANCE compares the target core with a real registry export | EVD-023 |
| W03-H47 | The ADR, AGENTS, workspace README, reference report and pack, knowledge map, vocabulary, prompt, governance document and role, and evaluation forms keep their trees and slug section IDs, and the target roles decision, research, audit, data-reference and agent-instructions have no mapping (Spec Non-goals) | terminal | T99-CONFORMANCE | When T99-CONFORMANCE classifies each unmapped role as a mapped form or a native or domain module | EVD-023 |

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-FORM-001](../spec.md#criteria) | accepted | EVD-002, EVD-004, EVD-005, EVD-009, EVD-012, EVD-015 | Accepted under the user's 2026-11-17 answer `승인, 녹색이면 수용 (권장)` (EVD-002), whose conditions the listed PASS rows meet | platform |
| [VAL-FORM-002](../spec.md#criteria) | accepted | EVD-007, EVD-008, EVD-010, EVD-011, EVD-013, EVD-014, EVD-016, EVD-017 | Accepted under the user's 2026-11-17 answer `승인, 녹색이면 수용 (권장)` (EVD-002), whose conditions the listed PASS rows meet | platform |
| [VAL-FORM-003](../spec.md#criteria) | accepted | EVD-004, EVD-019, EVD-020, EVD-021, EVD-022 | Accepted under the user's 2026-11-17 answer `승인, 녹색이면 수용 (권장)` (EVD-002), whose conditions the listed PASS rows meet; the out-of-scope differences are residue W03-H45 to W03-H47 | platform |

### Remaining Conditions

No work unit remains. T99-CONFORMANCE closed the residue rows W03-H45 to W03-H47 (EVD-023), so no open residue row is sourced in this Task. Push, pull request and merge follow the user's request for this change.

Frozen package disposition decision:

- **Target and method**: After the final source commit, retire only this Stage 03 package (`spec.md`, `plan.md` and this Task) through Git-history-only recovery. No other document is selected.
- **Consumers and preservation**: Current consumers: the registry retained Spec and Plan form exceptions and the tests that read these files; the exit change updates each. SPEC-0223 holds the open residue that this package hosted, and REQ-0003 Archived Lineage keeps its summary.
- **Hold and authority**: The current repository documents and the user's request identify no hold on these files. The disposition authority is the user's 2026-11-19 decision "Delete now, move residues (Recommended)". If a hold or unmet consumer is identified before deletion, the affected deletion is deferred and its source kept. Remote retention is not inferred from local refs.
- **Proof handoff**: This Task freezes the decision before its final source commit. After that commit, each file's exact `commit:path`, blob availability, reachability from the retained local ref and a byte comparison with the source still in the tree are recorded in REQ-0003 Archived Lineage before any file is deleted.

## Handoff

### Promotion Receipt

FORM-TREES is reflected: the [document authoring policy](../../../../.agents/governance/document-authoring.md) delegates the exact form rules to the Stage 99 registry, and the registry `common_forms` holds the new trees of the twelve role forms and the retained form for the four approved identities (commits `6ec18e41` to `4cedd75f`).

### Next Owner

T99-CONFORMANCE closed W03-H45 to W03-H47 (EVD-023). The package exit, with its Archived Lineage and the removal of the three terminal ledger entries, is the next step for this package. The next package prompts, W04-LIFECYCLE and T99-CONFORMANCE, start only when the user enters their scope.
