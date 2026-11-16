---
title: "W03 Form Target Adoption"
version: "0.1.0"
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

### Blockers and Decisions

Spec and Plan approval is open. The work starts after the user approves the exact bytes.

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-FORM-001](../spec.md#criteria), [VAL-FORM-003](../spec.md#criteria) | Spec and plan forms and the retained form | platform | draft | NOT_RUN | EVD-001 |
| WORK-002 | [VAL-FORM-001](../spec.md#criteria), [VAL-FORM-002](../spec.md#criteria) | Requirement and architecture forms and documents | platform | draft | NOT_RUN | EVD-001 |
| WORK-003 | [VAL-FORM-001](../spec.md#criteria), [VAL-FORM-002](../spec.md#criteria) | Operations and policy forms and documents | platform | draft | NOT_RUN | EVD-001 |
| WORK-004 | [VAL-FORM-001](../spec.md#criteria), [VAL-FORM-002](../spec.md#criteria) | Skill form and documents | platform | draft | NOT_RUN | EVD-001 |
| WORK-005 | [VAL-FORM-001](../spec.md#criteria), [VAL-FORM-002](../spec.md#criteria) | README forms and documents | platform | draft | NOT_RUN | EVD-001 |
| WORK-006 | [VAL-FORM-003](../spec.md#criteria) | Residue, independent review and the `document` suite | platform | draft | NOT_RUN | EVD-001 |

## Verification Evidence

### Results

| Evidence ID | Consumer | Work Unit | Command | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-FORM-001](../spec.md#criteria) | WORK-001 | Strict document validators and staged QA | Implementation snapshot of each work unit | NOT_RUN | Pending | yes | none |

### Resolution Links

No earlier failure is open.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-FORM-001](../spec.md#criteria) | pending | none | Run WORK-001 to WORK-005 and their checks | platform |
| [VAL-FORM-002](../spec.md#criteria) | pending | none | Run WORK-002 to WORK-005 and their checks | platform |
| [VAL-FORM-003](../spec.md#criteria) | pending | none | Run WORK-001 and WORK-006 | platform |

### Remaining Conditions

Spec and Plan approval, all six work units, the independent review and the user's acceptance remain.

## Handoff

### Promotion Receipt

The Plan's FORM-TREES row is not yet reflected.

### Next Owner

The user reviews and approves the Spec and Plan. The agent then runs WORK-001.
