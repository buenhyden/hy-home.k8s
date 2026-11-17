---
title: "T99 Common Core Conformance"
version: "0.4.0"
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

### Blockers and Decisions

Spec and Plan approval is open. The 0.1.0 draft failed its review (EVD-003) and was revised to 0.2.0 by the prompt's requirements; the review of 0.2.0 returned APPROVE WITH CHANGES (EVD-004), and the confirming review of 0.3.0 returned seven small changes (EVD-005), which 0.4.0 applies. The user approves the exact 0.4.0 bytes.

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-CORE-001](../spec.md#criteria) | Registry core members, `core_role` and classifications | platform | draft | NOT_RUN | EVD-001 |
| WORK-002 | [VAL-CORE-001](../spec.md#criteria), [VAL-CORE-003](../spec.md#criteria), [VAL-CORE-004](../spec.md#criteria) | Task core members, tables and transition adapter | platform | draft | NOT_RUN | EVD-001 |
| WORK-003 | [VAL-CORE-001](../spec.md#criteria), [VAL-CORE-003](../spec.md#criteria) | Requirement, architecture, spec and plan tables | platform | draft | NOT_RUN | EVD-001 |
| WORK-004 | [VAL-CORE-001](../spec.md#criteria), [VAL-CORE-003](../spec.md#criteria) | Operations and policy tables | platform | draft | NOT_RUN | EVD-001 |
| WORK-005 | [VAL-CORE-001](../spec.md#criteria), [VAL-CORE-003](../spec.md#criteria) | README tables | platform | draft | NOT_RUN | EVD-001 |
| WORK-006 | [VAL-CORE-001](../spec.md#criteria), [VAL-CORE-003](../spec.md#criteria) | Decision form | platform | draft | NOT_RUN | EVD-001 |
| WORK-007 | [VAL-CORE-001](../spec.md#criteria), [VAL-CORE-003](../spec.md#criteria) | Agent-instructions form | platform | draft | NOT_RUN | EVD-001 |
| WORK-008 | [VAL-CORE-001](../spec.md#criteria), [VAL-CORE-003](../spec.md#criteria) | Research, audit and data-reference forms | platform | draft | NOT_RUN | EVD-001 |
| WORK-009 | [VAL-CORE-002](../spec.md#criteria), [VAL-CORE-004](../spec.md#criteria) | Final export, residue closure, review and suite | platform | draft | NOT_RUN | EVD-001 |

## Verification Evidence

### Results

| Evidence ID | Consumer | Work Unit | Command | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-CORE-001](../spec.md#criteria) | WORK-001 | Strict document validators and staged QA | Implementation snapshot of each work unit | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-CORE-001](../spec.md#criteria) | WORK-001 | Package comparison of a reviewed export | One-time export of `docs/99.templates/registry.json` and the 38 templates at `a6ae5d73` (SHA-256 `9305a9cc69e61fa5ba5efe28aa7af92ed6fa8fcce5ea5f388c239bda41b0c157`); `compare_template_contracts.py --workspace-root` the repository root; pinned venv, 2026-11-17 | PASS | Observed the difference: status `MISMATCH` (result `05185b3ef929be30e9825d6c889067d97b39c942b9d618c53e957a693a6cfe17`), 19 roles compared, 15 unmapped templates, the groups listed under Work Performed. The row records that the comparison ran; `MISMATCH` is the observed difference, not a pass of the form. The tool's result asserts no runtime or approval fact. | no | none |
| EVD-003 | [VAL-CORE-001](../spec.md#criteria) | WORK-001 | Independent review of the draft package | A read-only code-reviewer agent over the staged 0.1.0 Spec, Plan and Task, the prompt, D24, the core, the tool, ADR-0059, ADR-0062 and the registry, 2026-11-17; risk class `high` | FAIL | NOT READY. Four blockers: a separate core file contradicts ADR-0059; SPEC-0222's own Spec and Plan cannot adopt new tables after approval; ADR-0062 is accepted outside the retained range; and the export rules for local extensions are undefined. Also high findings: required core cells with no source, the Task header adapter scope, wrong counts (17 reports, `scripts/document-generator.py`), a transition pending list, and bundled criteria. The 0.2.0 draft addresses each. | yes | none |
| EVD-004 | [VAL-CORE-001](../spec.md#criteria) | WORK-001 | Independent review of the draft package | The same read-only code-reviewer agent over the staged 0.2.0 Spec, Plan and Task, 2026-11-17; risk class `high` | FAIL | APPROVE WITH CHANGES: 14 findings, among them the Stage 02 rule on accepted ADRs, the staged `core_role` rollout, the core identity and field map, predictable stop cases (policy and requirement tables), native binding, review gates, and tables with no core counterpart. 0.3.0 applies them. | yes | none |
| EVD-005 | [VAL-CORE-001](../spec.md#criteria) | WORK-001 | Independent review of the draft package | The same agent over the staged 0.3.0 package, 2026-11-17; risk class `high` | PASS | All 14 earlier findings applied; seven small edits remained (native binding inside `template_definition`, the `classification` member, two counts, these review rows, the work order wording, recorded status reading, Task acceptance values), and 0.4.0 applies them. The reviewer stated the package is ready to approve after these edits. | yes | EVD-003, EVD-004 |

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
