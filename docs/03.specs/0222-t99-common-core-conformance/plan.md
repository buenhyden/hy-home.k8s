---
title: "T99 Common Core Conformance"
version: "1.1.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-18"
artifact_id: "SPEC-0222-PLAN-0001"
parent_ids: ["SPEC-0222"]
---

# T99 Common Core Conformance Implementation Plan

## Overview

### Outcome

This Plan executes [SPEC-0222](spec.md). When it is complete:

- every common form carries `core_role`, and every core-role form carries the core members;
- each changed role's templates and current documents carry the core trees and tables;
- the 15 unmapped templates are classified;
- a fresh export returns `DECLARED_CORE_MATCH`.

### Constraints

The current forms are the ones SPEC-0221 put in place. This Plan touches:

- the registry `common_forms` data, its schema, typed loader and authority guard;
- the document lifecycle and authoring policies, the Stage 99 README, Stage 03 `AGENTS.md` rule 4 and Stage 02 `AGENTS.md` rule 3;
- REQ-0003's tables (WORK-003) and the architecture descriptions' tables (WORK-003).

It stays inside ADR-0059's registry model and ADR-0062's retained range, and adds no ADR.

#### Global Constraints

Every work unit inherits the [Spec](spec.md#out-of-scope) constraints. Also:

- Each work unit is one commit, and the commit passes `python3 scripts/qa.py staged` on its exact index. A form, its core members and every document and test that reads it move together.
- **No compatibility code.** No alias, fallback or dual reading of an old section ID, title or column stays in code, per `scripts/AGENTS.md` rule 3. The one exception is the Task transition adapter that the Spec names.
- **No transition gate.** There is no pending list. A form receives `core_role` and its core members in the unit that moves its tree and tables, and the drift check covers every form that carries `core_role`. A form without it keeps its existing form checks, and WORK-009 enables the refusal of a form without `core_role`.
- **No count gate.** The core check reads registry JSON only. It adds no QA lane and hard-codes no template count.

#### Risks and Mitigations

- **A recorded value lost in a table move.** Before each move, a one-time scratch script lists every cell and sentence. After the move, it finds each one again with a normalized match, and records the rename and dropped-heading allowances in the Task.
- **A required core cell with no source fact.** The work stops for that role and asks the user; nothing is filled in to pass.
- **Large commits.** WORK-005 and WORK-008 are split by form, as listed.

#### Escalation

The work stops and asks the user in five cases:

- a table move cannot keep a recorded value's meaning;
- a required core cell has no source fact;
- a validator would have to be weakened to pass;
- SPEC-0222's own Spec and Plan need renewed approval in WORK-003;
- an independent review rates a finding high or above; the next unit waits for its disposition.

It resumes after the user's answer.

## Dependencies

### Prerequisites

- Spec and Plan approval by the user, with the exact bytes recorded in the Task.
- The `hyhome-validation` environment for the validators, the `document` suite and staged QA.
- The package comparison tool and core files, read in place for each export. Their hashes are recorded in the Task.

### Shared Resources

All work units write `docs/99.templates/registry.json`, its schema and `tests/test_common_form_tree.py`. They run in sequence, one commit each.

## Work Breakdown

### Work Units

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-CORE-001](spec.md#criteria) | The field map from registry fields to core members, recorded in the Task before code. Then: the registry schema, loader and guard for the `common_forms` `core` identity, `core_role`, the core members and extension `authority_ref`; `authority_ref` on every existing extension; and the ten domain forms and the `template_definition` of the three native profiles. | Approval | [Task](tasks/tsk-0001-t99-common-core-conformance.md) | RED and GREEN focused tests; strict registry check; staged QA; independent review |
| WORK-002 | [VAL-CORE-001](spec.md#criteria), [VAL-CORE-003](spec.md#criteria), [VAL-CORE-004](spec.md#criteria) | Task `core_role`, core members, section IDs and three core tables; the transition adapter; the lifecycle status reader on `task.work_items`; Stage 03 `AGENTS.md` rule 4; the Task template and readers. | WORK-001 review disposition | [Task](tasks/tsk-0001-t99-common-core-conformance.md) | Same, plus recorded rows byte-unchanged |
| WORK-004 | [VAL-CORE-001](spec.md#criteria), [VAL-CORE-003](spec.md#criteria) | Guide, runbook, policy, incident and postmortem `core_role`, core members and tables, the policy table map and local Level and Status table, the policy rule ID binding, and their templates and documents. | WORK-002 | [Task](tasks/tsk-0001-t99-common-core-conformance.md) | Same, plus normalized move check |
| WORK-005 | [VAL-CORE-001](spec.md#criteria), [VAL-CORE-003](spec.md#criteria) | Root, stage and service README and skill `core_role`, core members and tables, README navigation, and their templates and documents; one commit per README form. | WORK-002 | [Task](tasks/tsk-0001-t99-common-core-conformance.md) | Same |
| WORK-006 | [VAL-CORE-001](spec.md#criteria), [VAL-CORE-003](spec.md#criteria) | Decision `core_role`, core tree, members and table on the `adr` form, its template, ADR-0062 (PATCH) and ADR-0063, and Stage 02 `AGENTS.md` rule 3. | WORK-002 | [Task](tasks/tsk-0001-t99-common-core-conformance.md) | Same |
| WORK-007 | [VAL-CORE-001](spec.md#criteria), [VAL-CORE-003](spec.md#criteria) | Agent-instructions `core_role`, core tree and members on the `agents` form, its template and the 16 AGENTS.md files. | WORK-002 | [Task](tasks/tsk-0001-t99-common-core-conformance.md) | Same |
| WORK-008 | [VAL-CORE-001](spec.md#criteria), [VAL-CORE-003](spec.md#criteria) | Research, audit and data-reference forms split from the reference report form, with `core_role`, core members, templates and the 17 reports; one commit per form. | WORK-002 | [Task](tasks/tsk-0001-t99-common-core-conformance.md) | Same |
| WORK-003 | [VAL-CORE-001](spec.md#criteria), [VAL-CORE-003](spec.md#criteria) | Requirement, architecture, spec and plan `core_role`, core members and tables, templates and current documents. This package's Spec and Plan move through `in-review` and a renewed user approval; the unit is two commits, the move and the approval. | WORK-004 to WORK-008 | [Task](tasks/tsk-0001-t99-common-core-conformance.md) | Same, plus renewed approval receipt |
| WORK-009 | [VAL-CORE-002](spec.md#criteria), [VAL-CORE-004](spec.md#criteria) | The refusal of a form without `core_role`; a fresh export and negative exports; the declared deviations; residue closure of W03-H45 to W03-H47; the final independent review and the `document` suite. | WORK-003 | [Task](tasks/tsk-0001-t99-common-core-conformance.md) | `DECLARED_CORE_MATCH`; review record; suite result |

| Work Unit | Outcome | Depends On | Owner | Write Scope | Acceptance | Checks |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | The field map recorded in the Task; the registry schema, loader and guard for the `common_forms` `core` identity, `core_role`, the core members and extension `authority_ref`; `authority_ref` on every existing extension; the ten domain forms and the `template_definition` of the three native profiles classified. | none | platform | `docs/99.templates/`, `scripts/`, `tests/`, `docs/03.specs/0222-t99-common-core-conformance/` | [VAL-CORE-001](spec.md#criteria) | CHK-PLAN-FOCUSED, CHK-PLAN-REGRESSION, CHK-PLAN-NORMAL, CHK-PLAN-ARCH, CHK-PLAN-STAGED, CHK-PLAN-REVIEW |
| WORK-002 | The Task form bound to the core: `core_role`, core members, section IDs and three core tables; the transition adapter; the lifecycle status reader on `task.work_items`; Stage 03 `AGENTS.md` rule 4; the Task template and readers. | WORK-001 | platform | `docs/99.templates/`, `scripts/`, `tests/`, `.agents/governance/`, `docs/03.specs/AGENTS.md`, `docs/03.specs/0222-t99-common-core-conformance/` | [VAL-CORE-001](spec.md#criteria), [VAL-CORE-003](spec.md#criteria), [VAL-CORE-004](spec.md#criteria) | CHK-PLAN-FOCUSED, CHK-PLAN-REGRESSION, CHK-PLAN-NORMAL, CHK-PLAN-ARCH, CHK-PLAN-STAGED, CHK-PLAN-BYTES |
| WORK-004 | The guide, runbook, policy, incident and postmortem forms bound to the core with their tables, the policy table map and local Level and Status table, the policy rule ID binding, and their templates and documents. | WORK-002 | platform | `docs/99.templates/`, `scripts/`, `tests/`, `.agents/governance/`, `docs/05.operations/`, `docs/03.specs/0222-t99-common-core-conformance/` | [VAL-CORE-001](spec.md#criteria), [VAL-CORE-003](spec.md#criteria) | CHK-PLAN-FOCUSED, CHK-PLAN-REGRESSION, CHK-PLAN-NORMAL, CHK-PLAN-ARCH, CHK-PLAN-STAGED, CHK-PLAN-MOVE |
| WORK-005 | The root, stage and service README and skill forms bound to the core with their tables, README navigation, and their templates and documents. | WORK-002 | platform | `docs/99.templates/`, `scripts/`, `tests/`, `README.md`, `docs/03.specs/README.md`, `.agents/evaluations/harnesses/README.md`, `.agents/evaluations/templates/README.md`, `docs/05.operations/incidents/README.md`, `docs/90.references/audits/README.md`, `docs/90.references/data/README.md`, `gitops/README.md`, `infrastructure/README.md`, `docs/03.specs/0222-t99-common-core-conformance/` | [VAL-CORE-001](spec.md#criteria), [VAL-CORE-003](spec.md#criteria) | CHK-PLAN-FOCUSED, CHK-PLAN-REGRESSION, CHK-PLAN-NORMAL, CHK-PLAN-ARCH, CHK-PLAN-STAGED, CHK-PLAN-MOVE |
| WORK-006 | The `adr` form bound to the core decision tree, members and table, with its template, ADR-0062 (PATCH), ADR-0063 and Stage 02 `AGENTS.md` rule 3. | WORK-002 | platform | `docs/99.templates/`, `scripts/`, `tests/`, `docs/02.architecture/decisions/0062-accepted-decision-retained-form.md`, `docs/02.architecture/decisions/0063-affected-pr-gitops-validation.md`, `docs/02.architecture/AGENTS.md`, `docs/03.specs/0222-t99-common-core-conformance/` | [VAL-CORE-001](spec.md#criteria), [VAL-CORE-003](spec.md#criteria) | CHK-PLAN-FOCUSED, CHK-PLAN-REGRESSION, CHK-PLAN-NORMAL, CHK-PLAN-ARCH, CHK-PLAN-STAGED, CHK-PLAN-MOVE, CHK-PLAN-BYTES |
| WORK-007 | The `agents` form bound to the core agent-instructions tree and members, with its template and the 16 AGENTS.md files. | WORK-002 | platform | `docs/99.templates/`, `scripts/`, `tests/`, `**/AGENTS.md`, `docs/03.specs/0222-t99-common-core-conformance/` | [VAL-CORE-001](spec.md#criteria), [VAL-CORE-003](spec.md#criteria) | CHK-PLAN-FOCUSED, CHK-PLAN-REGRESSION, CHK-PLAN-NORMAL, CHK-PLAN-ARCH, CHK-PLAN-STAGED, CHK-PLAN-MOVE |
| WORK-008 | The research, audit and data-reference forms split from the reference report form, with `core_role`, core members, templates and the 17 reports. | WORK-002 | platform | `docs/99.templates/`, `scripts/`, `tests/`, `docs/90.references/`, `docs/03.specs/0222-t99-common-core-conformance/` | [VAL-CORE-001](spec.md#criteria), [VAL-CORE-003](spec.md#criteria) | CHK-PLAN-FOCUSED, CHK-PLAN-REGRESSION, CHK-PLAN-NORMAL, CHK-PLAN-ARCH, CHK-PLAN-STAGED, CHK-PLAN-MOVE, CHK-PLAN-BYTES |
| WORK-003 | The requirement, architecture, spec and plan forms bound to the core with their tables, templates and current documents; this package's Spec and Plan on the new tables, through `in-review` and a renewed user approval. | WORK-004, WORK-005, WORK-006, WORK-007, WORK-008 | platform | `docs/99.templates/`, `scripts/`, `tests/`, `docs/01.requirements/`, `docs/02.architecture/descriptions/`, `docs/03.specs/0222-t99-common-core-conformance/` | [VAL-CORE-001](spec.md#criteria), [VAL-CORE-003](spec.md#criteria) | CHK-PLAN-FOCUSED, CHK-PLAN-REGRESSION, CHK-PLAN-NORMAL, CHK-PLAN-ARCH, CHK-PLAN-STAGED, CHK-PLAN-MOVE, CHK-PLAN-BYTES, CHK-PLAN-APPROVAL |
| WORK-009 | The refusal of a form without `core_role`; a fresh export and negative exports; the declared deviations; residue closure of W03-H45 to W03-H47; the final independent review and the `document` suite. | WORK-003 | platform | `docs/99.templates/`, `scripts/`, `tests/`, `docs/03.specs/0221-w03-form-target-adoption/tasks/`, `docs/03.specs/work-residue-ledger.json`, `docs/03.specs/0222-t99-common-core-conformance/` | [VAL-CORE-002](spec.md#criteria), [VAL-CORE-004](spec.md#criteria) | CHK-PLAN-FOCUSED, CHK-PLAN-NORMAL, CHK-PLAN-STAGED, CHK-PLAN-EXPORT, CHK-PLAN-SUITE, CHK-PLAN-REVIEW |

#### Change and Rollback

Each work unit changes its forms' core members and registry entries, then the templates, documents, code, tests and prose. To undo a work unit, revert its commit; the adapter and extension changes revert with their unit. Revert later units first, because each unit leaves a consistent tree.

### Dependency Edges

- **Order:** WORK-001, WORK-002, WORK-004 to WORK-008, then WORK-003, then WORK-009.
- **WORK-001:** adds the schema fields and the field map that every later unit fills.
- **WORK-002:** starts after the disposition of the WORK-001 review.
- **WORK-004 to WORK-008:** depend only on WORK-001, so by the user's decision recorded in the Task they are prepared in parallel with WORK-002, each in its own worktree. Each is integrated after WORK-002 in the order above, one commit per unit.
- **WORK-003:** runs last before WORK-009. It changes the Spec and Plan tables that this package's own approved Spec and Plan use, so no unit runs on a basis that is back in review.
- **WORK-009:** runs after all the others.

## Verification Plan

### Selected Checks

- **Normal case:** every document of the role passes the strict registry, markdown profile, link and lifecycle validators under its new form and tables.
- **Violation cases:** each refusal under the Spec's Failure Behavior, and the negative exports of VAL-CORE-002.
- **Regression:** the focused modules that name the role's sections or tables. The `document` suite runs once in WORK-009.
- **Architecture compliance:** every change stays within ADR-0059's registry model and ADR-0062's retained range. A change outside them returns the Spec to in-review.

| Check ID | Guarantee | Input | Trust Boundary | Required When | Evidence |
| --- | --- | --- | --- | --- | --- |
| CHK-PLAN-NORMAL | Every document of the role passes the strict registry, markdown profile, link and lifecycle validators under its new form and tables. | The registry, templates and current documents of the changed roles | Repository-static; no live surface is in scope. | Every work unit | Validator results in the Task |
| CHK-PLAN-FOCUSED | Each changed check fails first and passes after the change, and each refusal under the Spec's Failure Behavior and each negative export of VAL-CORE-002 is shown. | The focused tests of each changed check | Covers only the changed check. | Every work unit | RED and GREEN results in the Task |
| CHK-PLAN-REGRESSION | The focused modules that name the role's sections or tables pass. | Those modules | The `document` suite runs once in WORK-009, not per unit. | Every work unit that changes a role | Module results in the Task |
| CHK-PLAN-ARCH | Every change stays within ADR-0059's registry model and ADR-0062's retained range. | The unit's change, ADR-0059 and ADR-0062 | A change outside them returns the Spec to in-review. | Every work unit | Compliance note in the Task |
| CHK-PLAN-STAGED | `qa.py staged` passes through the hooks on the exact index of the unit's commit. | The exact index of each commit | Push and merge do not repeat an identical leaf. | Each commit | Staged QA result in the Task |
| CHK-PLAN-MOVE | Every cell and sentence listed before a move is found again after it with a normalized match. | A one-time scratch list of every cell and sentence of the moved documents | The scratch script is one-time; the rename and dropped-heading allowances are recorded in the Task. | A unit that moves a heading, table or cell of a current document | Move check result and allowances in the Task |
| CHK-PLAN-BYTES | Recorded Task rows and the retained identities stay byte-unchanged, and the adapter reads the recorded rows. | The recorded Tasks and retained documents | Only bytes are compared; meaning is the other checks'. | A unit that changes a form or reader that a recorded Task or retained identity uses | Byte comparison in the Task |
| CHK-PLAN-APPROVAL | This package's Spec and Plan return to approved only with the user's renewed approval of their exact bytes. | The moved Spec and Plan and the user's answer | An agent never writes an approval; the user's answer is the authority. | WORK-003 | Renewed approval receipt in a new Task row |
| CHK-PLAN-EXPORT | A fresh export returns `DECLARED_CORE_MATCH`, and the negative exports return non-match. | A reviewed one-time export and the package comparison tool | Covers form and template definitions only. | WORK-009 | Export and result hashes in the Task |
| CHK-PLAN-SUITE | The `document` suite passes. | The final tree | Runs once, on the final tree. | WORK-009 | Suite result in the Task |
| CHK-PLAN-REVIEW | An independent review of the change; a finding rated high or above blocks the next unit until its disposition. | WORK-001's change; in WORK-009, every integrated unit, split across parallel reviewers by area | Read-only. | After WORK-001, and once in WORK-009 for WORK-002 and every later unit | Review record in the Task |
| CHK-PLAN-HOSTED | The hosted `ci-summary` and `style-pr` checks pass on the pull request. | The pull request | Runs once; push and merge do not repeat an identical leaf. | The pull request | Hosted run results |

### Evidence Plan

Each work unit's commit runs `qa.py staged` through the hooks on its exact index. The independent review of WORK-001 runs after WORK-001. By the user's decision recorded in the Task, the reviews of WORK-002 and every later unit move into one final independent review in WORK-009, after all units are integrated, split across parallel reviewers by area; every unit still passes the strict validators and staged QA before its commit. A finding rated high or above blocks the next unit until its disposition. The `document` suite and the final export run once on the final tree in WORK-009. The pull request runs the hosted `ci-summary` and `style-pr` checks once. Push and merge do not repeat an identical leaf.

## Promotion Map

### Durable Owners

| Promotion ID | Target Owner | Acceptance | Evidence |
| --- | --- | --- | --- |
| CORE-BINDING | [Document Authoring](../../../.agents/governance/document-authoring.md) | The authoring policy delegates the exact form and table rules to the Stage 99 registry, and the registry carries `core_role` and the core members on every common form. | Stage 99 `common_forms` |

### Consumer Updates

The `core_role` bindings and the core members stay in the registry after the work. The Task transition adapter stays while any tracked Task uses a recorded header, and is removed when none does.
