---
title: "T99 Common Core Conformance"
version: "0.12.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-17"
artifact_id: "SPEC-0222-TSK-0001"
parent_ids: ["SPEC-0222-PLAN-0001"]
---

# Task: T99 Common Core Conformance

## Scope

### Objective and Parent

This Task executes WORK-001 to WORK-009 of the [Plan](../plan.md) for [SPEC-0222](../spec.md) criteria VAL-CORE-001 to VAL-CORE-004. Completion evidence is a fresh export that returns `DECLARED_CORE_MATCH`, the strict validators, the `document` suite, staged QA and the independent review.

### Inputs and Authority

- **Request:** on 2026-11-17 (Asia/Seoul) the user applied the 4.2.0 T99-CONFORMANCE prompt to this workspace with the standing limits and asked the agent to continue. The package is `_workspace/workspace_governance_4_2_0_20261116/`.
- **Decision:** the agent reported the comparison mismatch below and asked how far to apply it. The user answered `요구사항에 작성된 내용에 맞게 진행한다.` (proceed as the requirements state). The T99 requirement applies only the differences, to the schema, registry, generator, validator, current documents and links together. The answer approves no Spec or Plan bytes and no criterion.
- **Design answers:** after the draft review (EVD-003), the agent asked four design questions: where the core lives, ADR-0062, local headings and tables, and columns with no core home. The user answered each with `프롬프트의 요구사항에 작성된 내용에 따라 구현하고 진행한다.` (implement as the prompt's requirements state). The Spec takes each choice from the prompt and D24. The user's earlier `승인한다.` (I approve) applied to the 0.1.0 draft, which the review found not ready, so it is not recorded as approval of these bytes.
- **Inputs (SHA-256):**
  - `dependencies/template-design-targets.json` `3ac2806ec2db8b9f7cd320faa1b5bfe36675624555e63269783be8cdc2039a0e`;
  - `dependencies/template-design-targets.schema.json` `a07b2f24bc9980bab04895128e4ddf3339a2d719485a6f48f49e7ba26e227ad2`;
  - `prompts/T99-CONFORMANCE.md` `7baaaa3d98cd44b4be0e0528eb1ed7fc3b9f796a4994f33d5f20768b83082be7`;
  - `tools/compare_template_contracts.py` `42f2c0df3bd9d5cbdfaa06a05e0ddcfb57db847f9034b8687c86c76c38aae97d`.
- **Base:** `main` at `a6ae5d73`; branch `claude/t99-conformance`.
- **Design summary:**
  - Reference designs: D01, D02, D03, D24, D25, D26, D27 and D28 of package 4.2.0.
  - Choice: the core members carried in the registry `common_forms` with a `core_role` on every form, core tables with recorded moves, local tables for values without a core column, a transition adapter for recorded Task rows, and a domain or native classification of unmapped templates.
  - Alternatives not taken:
    - a separate core file, which ADR-0059 rejected as a second form owner;
    - recording the differences only, which leaves the requirement unmet;
    - copying one repository's tables as the core;
    - treating a changed header as a local binding.
  - Interface: the registry `common_forms` members read by the registry check and a one-time export.
  - Failure: the check refuses tree, table and inventory drift.
  - Acceptance: VAL-CORE-001 to VAL-CORE-004.

- **Allowed Paths**: `docs/99.templates/`, `scripts/`, `tests/`, `.agents/governance/`, `.agents/skills/` and `.agents/workflows/` (moved table references only), every tracked `AGENTS.md` and `README.md` in the Spec's scope, `docs/01.requirements/`, `docs/02.architecture/descriptions/`, `docs/02.architecture/decisions/0062-accepted-decision-retained-form.md` and `0063-affected-pr-gitops-validation.md` (heading and table moves only), `docs/05.operations/`, `docs/90.references/`, `docs/03.specs/0222-t99-common-core-conformance/`, `docs/03.specs/0221-w03-form-target-adoption/tasks/` (residue State and Closure cells only), `docs/03.specs/AGENTS.md` (rule 4), `docs/02.architecture/AGENTS.md` (rule 3), `docs/03.specs/README.md`, `docs/03.specs/work-residue-ledger.json`, `.secrets.baseline` (reviewed line moves only)
- **Forbidden Paths**: `_workspace/`, `docs/98.archive/`, the approved Spec and Plan files of SPEC-0161 and SPEC-0221, ADR-0001 to ADR-0061, every recorded Task row, every manifest and script under `gitops/` and `infrastructure/`, `.github/workflows/`
- **Approval Required**: Spec and Plan approval; criterion acceptance; push, pull request and merge
- **Static Validation**: strict document validators, ledger gate, focused tests, the package comparison tool on a fresh export, `scripts/run-contract-tests.py --suite document`, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface in scope
- **Secret / Vault Handling**: no secret read or printed; the export holds only Stage 99 form structure and hashes
- **Rollback Plan**: delete the branch `claude/t99-conformance`; `main` is unchanged
- **Evidence Location**: this Task

## Execution Log

### Work Performed

On 2026-11-17 the agent ran these steps:

1. Listed the 38 templates and 37 template profiles of Stage 99.
2. Wrote a reviewed one-time export of the registry and the templates at `a6ae5d73`. The export holds:
   - the observed H2, H3 and table headers of each mapped template;
   - the SHA-256 of each source file;
   - the 15 unmapped templates.
3. Ran the package comparison tool with `--workspace-root`, so the tool rechecked the source hashes.
4. Drafted this package from the result.

The result was `MISMATCH` (export `9305a9cc69e61fa5ba5efe28aa7af92ed6fa8fcce5ea5f388c239bda41b0c157`, result `05185b3ef929be30e9825d6c889067d97b39c942b9d618c53e957a693a6cfe17`). The differences fall into these groups:

- **Every core role:**
  - its `contract` members, because no local core copy exists;
  - its table headers.
- **Extra local H3 extensions** in the observed H3 lists of the twelve SPEC-0221 roles. These are registered local extensions. A correct export lists one under `extensions` rather than as a difference only when its registry entry names that exact heading.
- **Task:** the slug section IDs.
- **Decision, agent-instructions, research, audit and data-reference:** their H2 and H3 trees.
- **Unmapped templates:** 15 of them.

#### WORK-001 Field Map

Recorded before any code changes, as the Spec requires. A registry member that has the core's meaning carries the core's value: the drift check requires equality, and the one-time export reads it under the core name. Local bindings keep their registry names and are never exported as core.

| Core member | Registry member | Rule |
| --- | --- | --- |
| identity `contract_id`, `contract_version` | `common_forms.core.contract_id`, `.contract_version`, `.sha256` | New; `stage`, `approval_ref`, `source` and `content_digest` stay as recorded |
| role | form `core_role` (or native `template_definition.core_role`) | New; one of 19 core roles, `domain` or `native`; `domain` and `native` carry `classification` (`owner`, `reason`, `review_trigger`, `authority_ref`) |
| `purpose`, `non_goals`, `metadata_policy`, `language`, `status`, `relationships`, `lifecycle`, `rules` | form `core.<member>` | New; verbatim core values |
| section `section_id`, `level`, `parent_id`, `order` | section `section_id`, `level`, `parent_id`, `order` | Existing; equal values |
| section `title_en` | section `title` | Existing; equal value |
| section `required_when` | section `condition` and `core.required_when` | Existing `condition` takes the core value; `core.required_when` holds it verbatim and the check requires them equal |
| section `title_ko`, `content_rule`, `prohibited_content` (string), `empty_policy` (H2 sentence) | section `core.title_ko`, `.content_rule`, `.prohibited_content`, `.empty_policy` | New; verbatim. The registry `content`, `required_content`, `prohibited_content` list, `empty_policy` code, `validation_ids` and `link_only` stay local authoring bindings |
| `subsections` | section `children` | Existing; equal structure |
| `tables` | form `core.tables` | New; verbatim core tables |
| table `table_id`, `section_id`, `required_when`, `empty_policy` | template table `table_id`, `section`, `required_when`, `empty_policy` | `table_id`, `required_when` and `empty_policy` are new; `section` takes the core H2 ID |
| column `label`, `key`, `value_type`, `meaning`, `required`, `allowed_values` | template column `key`, `id`, `data_type`, `meaning`, `required`, `allowed_values` | `key` carries the label as the header text; `id` is new and holds the core key; `data_type` takes the core value type; `meaning`, `required` and `allowed_values` take core values |
| extension `reason`, `validation`, `review_trigger`, `authority_ref` | extension `condition`, `verification`, `review`, `authority_ref` | `authority_ref` is new: `ADR-0059` for entries before this Spec, `SPEC-0222` for new ones |

WORK-001 implemented the field map's registry side:

- **Schema.** `document-profile.schema.json` gains the `common_forms.core` identity, `core_role`, `classification`, the role and section core members, the core table fields and the required extension `authority_ref`.
- **Registry data.**
  - The `common_forms.core` identity (SHA-256 of the package core).
  - `authority_ref: ADR-0059` on all 61 existing extensions.
  - `core_role: domain` with a classification on the ten domain forms, and `core_role: native` in the `template_definition` of the three provider-native templates.
- **Loader.** `CommonForm` and `CommonFormsRecord` read the new members, and `FormExtension` reads `authority_ref`.
- **Check.** `_core_role_diagnostics` refuses two things:
  - a core-role form section without its core members (`REGISTRY_CORE_SECTION`);
  - a template table that is missing, or differs from the core in section, condition, empty policy, labels, keys, types, meanings, requiredness, order or column count (`REGISTRY_CORE_TABLE`), and a core table ID outside a core-role form.

The identity hash key is `sha256`, not `source_sha256` as first written in the field map. The first staged run failed `detect-secrets` on that line, and the repository's identity-key exclusion admits only the `sha256` key. No form carries a core role yet; each later unit adds its own. The Stage 99 README describes the binding.

The independent WORK-001 review (EVD-009) returned two HIGH findings, which blocked WORK-002, and the agent fixed each finding:

- **Enums.** Core columns carry `allowed_values`, which the schema could not hold and the check did not compare. Both the core column and the template column now carry it, and the check compares it.
- **Repeated table IDs.** A repeated `table_id` in a template or in a form core could hide a drifted copy. Both are now refused.
- **Medium and low findings, also fixed:**
  - the core identity is required once a form binds a core role (`REGISTRY_CORE_IDENTITY`);
  - `core_role` in a TemplateDefinition is admitted only for a form-less provider-native template (`REGISTRY_CORE_ROLE`);
  - a section's `condition` must equal its core `required_when`, which `section.core` now holds;
  - an H3 core may not carry the H2-only members;
  - the new tests sit above the module's `__main__` guard;
  - new negative tests cover a dropped column, an enum difference, a repeated ID, an extra core table ID, the identity and the section members.
- **Record.** The TemplateDefinition record and its schema stay unchanged on purpose. The one-time export reads the registry directly, and no record consumer needs the classification.

WORK-002 bound the `task` form to the core:

- **Form.** `core_role: task`, the core members, the section IDs `task.scope` to `task.handoff.2`, and the section core members. The Task template carries the three core tables exactly. A local Lifecycle Traceability table keeps `Item | Upstream criterion | Result | Evidence`.
- **Transition adapter.** One adapter block in `scripts/document_contracts.py` (`read_task_tables`, `task_header_form`, `task_recorded_row`) reads a Task under the recorded header or the core header, never a mixture (`TASK-HEADER-MIXED`), and writes nothing.
  - Under the recorded header, it renames `ID` to `Item` and `Work Unit`, `Consumer` to `Criteria` and `Current owner` to `Current Owner`, and reads `Required` `yes`/`no` as `true`/`false`. The recorded ID is also read as the Work Unit, because recorded evidence cites the work-item ID there.
  - Core cells are checked against the registry's allowed values (`TASK-CORE-CELL`).
  - Work-item status in a core Task comes from `task.work_items`.
  - New core rows without a recorded decision keep `Intent` `undecided` and the acceptor cells `none` (`TASK-ACCEPTANCE-DECISION`).
- **Registry.** `task-evidence-local-columns` and the `local_columns` extension kind are removed, because their removal condition is met. The evidence result states take the core enum, and a required `ERROR` or `CANCELLED` check stays open until a later PASS resolves it, as `FAIL` does.
- **Prose.** Stage 03 `AGENTS.md` rule 4, AUTHOR-R007, DOCLIFE-R009 and the Stage 99 README state the adapter rule.
- **Recorded Tasks.** The three recorded Tasks are byte-unchanged and pass under the adapter.
- **Baseline.** The `.secrets.baseline` registry line moved in its own commit first (`d5603cc9`).
- **Suite speed.** The staged `document` suite timed out three times at its 900-second gate limit. A timed run of the suite alone showed the cause: it needed 941 seconds of CPU on this tree and 966 seconds on `d5603cc9`, before WORK-002. So the suite had outgrown its limit on this machine, and WORK-002 was not a regression. The user chose to fix the root cause rather than raise the limit. A profile of the slowest module showed `schema_errors` re-checking the same schema against its meta-schema on each of 1,444 calls. `scripts/json_schema_validation.py` now caches the checked validator by the schema's canonical JSON. A changed schema is checked again, and a schema that fails the check is never cached. The suite now takes 455 seconds of CPU.

On 2026-11-17 the user also approved (`승인`) moving the independent review of WORK-002 and later units into one final review after all units are integrated. That review runs in WORK-009, split across parallel reviewers by area, and every unit still passes the strict validators and staged QA before its commit. The Plan's Evidence Plan text is brought up to date in the WORK-003 renewed approval.

On 2026-11-17 the user asked to run the remaining work units in parallel where possible (`남아 있는 WORK중에서 동시에 진행이 가능한 work은 동시에 진행한다.`). WORK-004 to WORK-008 depend only on WORK-001, so they were prepared at the same time as WORK-002, each in its own worktree. Each is integrated in the Plan's order, one commit per unit, after the WORK-002 review disposition. WORK-003 and WORK-009 stay sequential.

The prepared units reported stop cases, and the user answered four questions on 2026-11-17:

- **Required core cells with no source fact.** The answer was to render a header-only core table plus residue if that matches the prompt. It does: the core empty policy defines the columns and writes rows when facts occur, D24 forbids invented values, and D25 links each gap to an owner. So the core table is rendered header-only, existing prose and tables stay as registered local tables, and the missing facts become residue owned by W04-CONTENT.
- **The 13 published Stage 90 reports.** The answer was to replace them with new members.
- **Policy rules that are not bullets.** The answer was that the Requirement cell takes the rule's lead sentence, if that matches the prompt. It does, because the rule ID stays the single meaning owner. The supporting text stays under the rule's H4.
- **Agent judgments.** All four are accepted:
  - the root `AGENTS.md` heading cap of 20, re-derived for the new form;
  - the RUN-0012 header rename;
  - the runbook `Triggers` table replaced by the core Steps table;
  - the ADR-0063 Trade-off split.

### Blockers and Decisions

The user approved the Spec and Plan (EVD-006); criterion acceptance stays with the user. Before that, the 0.1.0 draft failed its review (EVD-003) and was revised to 0.2.0 by the prompt's requirements; the review of 0.2.0 returned APPROVE WITH CHANGES (EVD-004), and the confirming review of 0.3.0 returned seven small changes (EVD-005), which 0.4.0 applies. The user approves the exact 0.4.0 bytes.

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-CORE-001](../spec.md#criteria) | Registry core members, `core_role` and classifications | platform | completed | PASS | EVD-007, EVD-008, EVD-010, EVD-011, EVD-012, EVD-013 |
| WORK-002 | [VAL-CORE-001](../spec.md#criteria), [VAL-CORE-003](../spec.md#criteria), [VAL-CORE-004](../spec.md#criteria) | Task core members, tables and transition adapter | platform | completed | PASS | EVD-014, EVD-015, EVD-016, EVD-017 |
| WORK-003 | [VAL-CORE-001](../spec.md#criteria), [VAL-CORE-003](../spec.md#criteria) | Requirement, architecture, spec and plan tables | platform | ready | NOT_RUN | EVD-001 |
| WORK-004 | [VAL-CORE-001](../spec.md#criteria), [VAL-CORE-003](../spec.md#criteria) | Operations and policy tables | platform | in-progress | NOT_RUN | EVD-001 |
| WORK-005 | [VAL-CORE-001](../spec.md#criteria), [VAL-CORE-003](../spec.md#criteria) | README tables | platform | ready | NOT_RUN | EVD-001 |
| WORK-006 | [VAL-CORE-001](../spec.md#criteria), [VAL-CORE-003](../spec.md#criteria) | Decision form | platform | ready | NOT_RUN | EVD-001 |
| WORK-007 | [VAL-CORE-001](../spec.md#criteria), [VAL-CORE-003](../spec.md#criteria) | Agent-instructions form | platform | ready | NOT_RUN | EVD-001 |
| WORK-008 | [VAL-CORE-001](../spec.md#criteria), [VAL-CORE-003](../spec.md#criteria) | Research, audit and data-reference forms | platform | ready | NOT_RUN | EVD-001 |
| WORK-009 | [VAL-CORE-002](../spec.md#criteria), [VAL-CORE-004](../spec.md#criteria) | Final export, residue closure, review and suite | platform | ready | NOT_RUN | EVD-001 |

## Verification Evidence

### Results

| Evidence ID | Consumer | Work Unit | Command | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-CORE-001](../spec.md#criteria) | WORK-001 | Strict document validators and staged QA | Implementation snapshot of each work unit | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-CORE-001](../spec.md#criteria) | WORK-001 | Package comparison of a reviewed export | One-time export of `docs/99.templates/registry.json` and the 38 templates at `a6ae5d73` (SHA-256 `9305a9cc69e61fa5ba5efe28aa7af92ed6fa8fcce5ea5f388c239bda41b0c157`); `compare_template_contracts.py --workspace-root` the repository root; pinned venv, 2026-11-17 | PASS | Observed the difference: status `MISMATCH` (result `05185b3ef929be30e9825d6c889067d97b39c942b9d618c53e957a693a6cfe17`), 19 roles compared, 15 unmapped templates, the groups listed under Work Performed. The row records that the comparison ran; `MISMATCH` is the observed difference, not a pass of the form. The tool's result asserts no runtime or approval fact. | no | none |
| EVD-003 | [VAL-CORE-001](../spec.md#criteria) | WORK-001 | Independent review of the draft package | A read-only code-reviewer agent over the staged 0.1.0 Spec, Plan and Task, the prompt, D24, the core, the tool, ADR-0059, ADR-0062 and the registry, 2026-11-17; risk class `high` | FAIL | NOT READY. Four blockers: a separate core file contradicts ADR-0059; SPEC-0222's own Spec and Plan cannot adopt new tables after approval; ADR-0062 is accepted outside the retained range; and the export rules for local extensions are undefined. Also high findings: required core cells with no source, the Task header adapter scope, wrong counts (17 reports, `scripts/document-generator.py`), a transition pending list, and bundled criteria. The 0.2.0 draft addresses each. | yes | none |
| EVD-004 | [VAL-CORE-001](../spec.md#criteria) | WORK-001 | Independent review of the draft package | The same read-only code-reviewer agent over the staged 0.2.0 Spec, Plan and Task, 2026-11-17; risk class `high` | FAIL | APPROVE WITH CHANGES: 14 findings, among them the Stage 02 rule on accepted ADRs, the staged `core_role` rollout, the core identity and field map, predictable stop cases (policy and requirement tables), native binding, review gates, and tables with no core counterpart. 0.3.0 applies them. | yes | none |
| EVD-005 | [VAL-CORE-001](../spec.md#criteria) | WORK-001 | Independent review of the draft package | The same agent over the staged 0.3.0 package, 2026-11-17; risk class `high` | PASS | All 14 earlier findings applied; seven small edits remained (native binding inside `template_definition`, the `classification` member, two counts, these review rows, the work order wording, recorded status reading, Task acceptance values), and 0.4.0 applies them. The reviewer stated the package is ready to approve after these edits. | yes | EVD-003, EVD-004 |
| EVD-006 | [VAL-CORE-001](../spec.md#criteria) | WORK-001 | Spec/Plan approval | Direct current-session user answer `요구사항에 작성된 대로 진행하고 구현한다.` (proceed and implement as the requirements state) to the SPEC-0222 approval question naming spec.md `8bff1cd0` and plan.md `4db258c2` of draft commit `f5022431`, 2026-11-17; risk class `high` | PASS | Approves the reviewed Spec and Plan content of `f5022431` for implementation; the approved files differ from it only in `status` and `version`. The answer does not accept a criterion: VAL-CORE-001 to VAL-CORE-004 stay pending until the user's acceptance. | yes | none |
| EVD-007 | [VAL-CORE-001](../spec.md#criteria) | WORK-001 | Failing first | `python3 -m unittest tests.test_common_form_tree.CoreRoleBindingTests` with the new tests over an export of `294156dc`; pinned venv, 2026-11-17 | PASS | Observed the defect: 6 tests, 9 failures and 2 errors; the registry carried no core identity, classification or `authority_ref`, and no drift check existed. | yes | none |
| EVD-008 | [VAL-CORE-001](../spec.md#criteria) | WORK-001 | Focused tests and strict validators after the change | The 32 test modules that read the registry, its schema or TemplateDefinitions; the strict registry, markdown profile, link and lifecycle validators; agent governance and ledger gates; pinned venv, 2026-11-17 | PASS | `tests.test_common_form_tree` 423 tests OK with 3 skips after 25 extension fixtures gained `authority_ref`; the other 31 modules passed in the first run; every validator passed. | yes | none |
| EVD-009 | [VAL-CORE-001](../spec.md#criteria) | WORK-001 | Independent review | A read-only code-reviewer agent over `git show fa35445c`, the Spec, Plan, field map, ADR-0059, the core and the comparison tool, with in-memory registry probes, 2026-11-17; risk class `high` | FAIL | APPROVE WITH FINDINGS. Two HIGH findings blocked WORK-002: `allowed_values` could not be stored or compared, and a repeated `table_id` hid a drifted copy. Medium: the identity was optional, native `core_role` was unbound, the record was silent, and section `required_when` was unchecked. Low: test placement and coverage gaps. No assertion was weakened; the rename and scope were correct. | yes | none |
| EVD-010 | [VAL-CORE-001](../spec.md#criteria) | WORK-001 | Failing first | `python3 -m unittest tests.test_common_form_tree.CoreRoleBindingTests` with the extended tests over an export of `fa35445c`; pinned venv, 2026-11-17 | PASS | Observed the defects: 11 tests, 19 failures. | yes | none |
| EVD-011 | [VAL-CORE-001](../spec.md#criteria) | WORK-001 | Focused tests and strict validators after the change | `python3 -m unittest tests.test_common_form_tree`; the strict registry, markdown profile, link and lifecycle validators; pinned venv, 2026-11-17 | PASS | 428 tests OK with 3 skips, including 11 `CoreRoleBindingTests`; every listed validator passed. | yes | none |
| EVD-012 | [VAL-CORE-001](../spec.md#criteria) | WORK-001 | Independent review | The same read-only code-reviewer agent over `git show db0eb818`, rerunning its earlier in-memory probes, 2026-11-17; risk class `high` | PASS | APPROVE: H1, H2, M1, M2 and M4 closed (each probe now refused or accepted as expected); M3 accepted as decided. Remaining notes are low: a core-role form without a template is unchecked, and a same-named local table without `table_id` is accepted, which is not a bypass because the core table is still required by ID. | yes | EVD-009 |
| EVD-013 | [VAL-CORE-001](../spec.md#criteria) | WORK-001 | Strict document validators and staged QA | `python3 scripts/qa.py staged` on the indexes of `fa35445c` and `db0eb818`, and their commit hooks; pinned venv, 2026-11-17 | PASS | 12 selected gates, the `document` suite among them, passed on each exact index. The first hook run of `db0eb818` timed out in the `document` suite (`rc=-9`, load average about 7) and committed nothing; the unchanged retry passed. | yes | EVD-001 |
| EVD-014 | [VAL-CORE-001](../spec.md#criteria) | WORK-002 | Failing first | The changed tests of `tests.test_task_execution_contract`, `test_task_acceptance_contract`, `test_task_acceptance_boundaries`, `test_common_form_tree` and `test_document_lifecycle_cumulative_history` over an export of `b6e99e9d`; pinned venv, 2026-11-17 | PASS | Observed the defect: three modules failed to import the adapter (1 error each), `test_common_form_tree` 428 tests with 9 failures, `test_document_lifecycle_cumulative_history` 50 tests with 8 failures and 1 error. | yes | none |
| EVD-015 | [VAL-CORE-003](../spec.md#criteria) | WORK-002 | Focused tests and strict validators after the change | 15 modules that read Task tables, the registry or the lifecycle: form tree, task execution, acceptance contract and boundaries, cumulative history, summary derivation, residue ledger, registry schema version, frontmatter keys, generator, package exit, artifact identity, relationship contract, link boundary and shared contract binding; the four strict validators; pinned venv, 2026-11-17 | PASS | 878 tests OK with 3 skips, including 11 `TaskCoreHeaderTests`; the registry, markdown profile, link and lifecycle validators passed; the three recorded Tasks are byte-unchanged. | yes | none |
| EVD-016 | [VAL-CORE-004](../spec.md#criteria) | WORK-002 | Suite runtime | `scripts/run-contract-tests.py --root . --suite document` timed alone with `time`, on this tree before the fix, on an export of `d5603cc9`, and after the schema check cache, with `tests.test_json_schema_validation` and `tests.test_common_form_tree`; pinned venv, 12 CPUs, load average 7 to 20, 2026-11-17 | PASS | Before: 941 s CPU (1,174 tests) and 966 s CPU on `d5603cc9` (1,163 tests), both above the 900-second gate limit. After: 455 s CPU, 1,176 tests OK. `test_common_form_tree` 256 s to 96 s. Two cache tests prove one check per distinct schema and no caching of an invalid schema. | yes | none |
| EVD-017 | [VAL-CORE-003](../spec.md#criteria) | WORK-002 | Strict document validators and staged QA | `python3 scripts/qa.py staged` on the index of `3909ae40` and its commit hooks; pinned venv, 2026-11-17 | PASS | 17 selected gates passed, the `document` suite among them, after three earlier runs timed out in that suite and committed nothing (EVD-016 records the cause and fix). The independent review of WORK-002 moves to the final WORK-009 review by the user's decision. | yes | none |

### Resolution Links

EVD-005 resolves EVD-003 and EVD-004 for the reviewed draft.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-CORE-001](../spec.md#criteria) | pending | none | Run WORK-001 to WORK-008 and their checks | platform |
| [VAL-CORE-002](../spec.md#criteria) | pending | none | Run WORK-009 | platform |
| [VAL-CORE-003](../spec.md#criteria) | pending | none | Run WORK-002 to WORK-008 and their checks | platform |
| [VAL-CORE-004](../spec.md#criteria) | pending | none | Run WORK-002 and WORK-009 | platform |

### Remaining Conditions

Spec and Plan approval, WORK-001 to WORK-009, the independent review and the user's acceptance remain.

## Handoff

### Promotion Receipt

The Plan's CORE-BINDING row is not yet reflected.

### Next Owner

The user decides on the Spec and Plan. After approval, the agent runs the work units in the Plan's dependency order.
