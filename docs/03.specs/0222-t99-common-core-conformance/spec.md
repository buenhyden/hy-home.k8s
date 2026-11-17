---
title: "T99 Common Core Conformance"
version: "1.0.0"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-11-17"
artifact_id: "SPEC-0222"
---

# T99 Common Core Conformance Technical Specification (Spec)

## Overview

### Goal

The 4.2.0 T99-CONFORMANCE prompt asks each workspace to resolve the differences between the common document core and its actual forms and readers. The core is the package's template design targets, definition model 4.0.0 (`workspace-document-role-design`). A reviewed one-time export of this repository's Stage 99 registry and templates at `a6ae5d73` returned `MISMATCH` from the package comparison tool, as recorded in the [Task](tasks/tsk-0001-t99-common-core-conformance.md). [SPEC-0221](../0221-w03-form-target-adoption/spec.md) already moved the heading trees of twelve roles. The remaining differences are:

- **Tables.** The core tables of 17 roles differ from the registry tables in columns, order, types or presence. The agent-instructions and skill roles have no core table.
- **Typed core.** The registry does not carry the core's purpose, non-goals, section rules, column types, metadata, language, status, relationship, lifecycle and rule members.
- **Unadopted roles.** The task section IDs keep their slug form, and the decision, agent-instructions, research, audit and data-reference roles have no core tree.
- **Unmapped templates.** 15 templates have no core role.

The user answered every design question on 2026-11-17 the same way: implement as the prompt's requirements state. This Spec takes each design choice from the prompt and its design D24, which says:

- The design owner holds the common meaning, and the existing `docs/99.templates/` registry, schema and generator hold the local machine implementation.
- A change to a table header or a judgment meaning is never passed off as a local binding.
- Each form is a core role, an approved domain role or a verified native format.

The [Plan](plan.md) orders the work.

#### Owning Requirements

[REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md) FR-0012 and FR-0013 own the single registry owner of form and the template-validator agreement. Accepted [ADR-0059](../../02.architecture/decisions/0059-registry-common-form-model.md) gives the registry common form model, and this Spec stays inside it. The core lives in the existing `common_forms` key, so no new top-level key and no second form file is added. [ADR-0062](../../02.architecture/decisions/0062-accepted-decision-retained-form.md) bounds the retained form to ADR-0001 to ADR-0061; every later ADR takes the form tree in every status.

### Consumers

- **Authors:** use the templates and `scripts/document-generator.py`.
- **Validators:**
  - the registry check;
  - the markdown profile, link and lifecycle validators;
  - the policy rule ID check;
  - the README navigation check;
  - the work residue ledger gate.
- **Comparison:** the package comparison tool, which reads a one-time export.

## Scope

### In Scope

- **The core in the registry.** The registry carries the core in the existing `common_forms` key:
  - **Identity.** `common_forms` gains a `core` member with `contract_id` (`workspace-document-role-design`), `contract_version` (`4.0.0`) and the SHA-256 of the package core file. `stage`, `approval_ref`, `source` and `content_digest` stay as recorded; the adoption is recorded in the Task, because ADR-0059 never infers an approval. Each role's `status` (`DESIGN_PROPOSAL_NOT_ADOPTED`) is copied verbatim and is not a claim of adoption.
  - **`core_role`.** Each form gains `core_role`, which is one of the 19 core role IDs, `domain` or `native`. A native template has no form, so its already admitted `template_definition` carries `core_role: native` and its classification; no profile key is added.
  - **Core members.** A form whose `core_role` is a core role gains the core's members with the core's exact values: purpose, non-goals, section rules, table IDs, column keys, labels, value types, meanings and requiredness, metadata policy, language, status, relationships, lifecycle and rules.
  - **Shared fields.** An existing registry field with the same meaning takes the core value and type, by a field map recorded in WORK-001 before any code changes. Examples: section `title` and `title_en`, `children` and `subsections`.
  - **Local bindings.** A field the core does not have stays a local binding: paths, owner values, body language, native envelope, validation IDs and required-content prompts.
  - **Code.** The registry schema, the typed loader and the authority guard move with them.
  - **Rollout.** A form receives `core_role` and its core members in the work unit that moves its tree and tables. The drift check covers every form that carries `core_role`. A form without it keeps its existing form checks until WORK-009, which enables the refusal of a form without `core_role`.
- **The registry split for core roles.** The reference report form becomes three forms: research, audit and data-reference. The `adr` and `agents` forms bind `decision` and `agent-instructions`.
- **The 15 unmapped templates.** Each is classified once:
  - **domain:** evaluation task, score and results; knowledge map; vocabulary; prompt; governance document and role; workspace README; the three reference pack READMEs. Their ten forms take `core_role: domain`.
  - **native:** the two Claude runtime templates and the Codex agent TOML. Their `template_definition` takes `core_role: native`.
  - Beside `core_role: domain` or `native`, each entry carries a `classification` member with `owner`, `reason`, `review_trigger` and `authority_ref`. For these entries the `authority_ref` is `SPEC-0222 approval (receipt in the SPEC-0222 Task)`, because the user's approval of this Spec approves the twelve domain roles.
- **The core tables of each role.** Each takes its exact labels, order and types in the registry tables and template tables. Every current document of the role follows the table rules under Behavior Contract.
- **The decision, agent-instructions, research, audit and data-reference trees and section IDs**, with their templates and current documents:
  - ADR-0062 (accepted, outside the retained range) and ADR-0063 (the only proposed ADR);
  - 16 AGENTS.md files;
  - 17 reference reports: 2 audits and 15 research reports. No data-reference document exists; its template is the evidence.
  - The 36 accepted ADRs ADR-0002 to ADR-0061 keep their bounded retained form.
- **Task section IDs.** They move to the core IDs (`task.scope` and the rest), with every reader.
- **SPEC-0222's own Spec and Plan.** WORK-003 changes the Spec and Plan tables and runs after every other unit except WORK-009. In the same unit, this package's Spec and Plan move to the new tables. They go through `in-review` and a renewed user approval in a separate commit, with the exact bytes recorded in a new Task row, because an approved contract does not change its bytes.
- **The registered local extensions.** Each local H3 and local table keeps its condition, owner, verification, review and removal, and gains an `authority_ref`. It never replaces a core section or table, and never adds a column to a core table.
  - **`authority_ref` values:** `ADR-0059` for entries registered before this Spec, and `SPEC-0222` for entries this Spec adds.
  - **Export mapping:** the export reads an entry's `condition`, `verification` and `review` as the tool's `reason`, `validation` and `review_trigger`, with `changes_core: false`.
- **The prose and owner rules that change:**
  - Stage 03 `AGENTS.md` rule 4 on the Task header adapter;
  - Stage 02 `AGENTS.md` rule 3, which gains: a heading or table move that keeps every sentence and fact of an accepted ADR outside ADR-0001 to ADR-0061 is not an in-place edit of the decision. ADR-0062 then takes a PATCH version;
  - the lifecycle status reader and its policy text, which read work-item status from the core `task.work_items` table in new Tasks;
  - the validators, generator and tests;
  - the governance and Stage 99 prose that names a changed table, section or role.

### Out of Scope

- **Records that keep their current bytes:**
  - the approved Spec and Plan identities of SPEC-0161 and SPEC-0221, on their retained form;
  - the 36 retained ADRs;
  - every recorded Task row.
- **History and paths:** `docs/98.archive/` and Git history; renumbering and path moves, which stay with DOC-PATH-PLAN and Q07-CUTOVER.
- **Other repositories:** execution in the other three repositories, and any cross-repository adoption claim.
- **Re-runs and gates:** no completed prompt or Task of earlier packages is re-run. No global QA lane, per-commit full template read or fixed template count is added.
- **Protected actions:** any push, merge, secret read, cluster access or remote setting change without the user's separate request.

## Behavior Contract

### Inputs and Outputs

**Heading moves.** For ADR-0062, ADR-0063, the 16 AGENTS.md files and the 17 reference reports, each sentence moves by the SPEC-0221 rule:

- **keep or rename:** the heading keeps or changes its title in place;
- **H4:** a former heading with no core home stays, with its title, as an H4 under the core H3 that holds its sentences;
- **new:** a new core section holds only facts the same document states, or an author prompt in a template.

**Tables.** A core table carries exactly the core's columns, in order, with the core's labels and types. A current table moves in one of five ways:

- **rename:** a column is relabeled with the same meaning;
- **move:** a cell moves to the core column of the same meaning;
- **derive:** a cell value is taken from a fact the same document states;
- **local table:** values with no core column (for example policy `Level` and `Status`) move to a registered local table keyed by the core row ID and placed after the core table;
- **local table of its own:** a current table with no core counterpart stays a registered local table with its own row identity and columns. Examples are the Spec `Criteria`, the Plan `Work Breakdown` and `Promotion`, and the `Lifecycle Traceability` tables. It never changes a core table.

These table maps follow from the documents and are fixed here:

- **Policy rules.**
  - `Requirement` takes the rule bullet text keyed by the rule ID, which leaves the bullet list, so each rule's meaning has one place.
  - `Enforcement` takes the former `Evidence` cell, and `Evidence` takes `none` unless the document states another check.
  - `Level` and `Status` move to the local table keyed by Rule ID.
- **Requirements.**
  - `Priority` values take the core's lower case (`Must` becomes `must`), as a listed rename.
  - A quality row without measure facts stays a row of `requirement.requirements`. `requirement.quality` is defined and not rendered.
- **Task work items.** In a new Task the core `task.work_items` table holds each work item's `Status`, and the local `Lifecycle Traceability` table keeps only the columns with no core home, so status has one owner. Under the recorded header, the adapter reads the `Status` of the recorded `Lifecycle Traceability` table as the work-item status.
- **Task acceptance.** In new rows, `Intent` is `undecided` and `Accepted By` and `Reassigned To` are `none` until the operator's recorded decision; an agent never writes an acceptance or an acceptor.

A core table whose `required_when` holds for the document must be present. A conditional core table is defined in the registry and the template with its condition, and a document renders it only where the condition holds. A required core cell with no source fact is not filled: the work stops for that role and asks the user. Nothing is invented.

**Task records.** A recorded Task table keeps its header and rows. A transition adapter in the Task reader reads a table under either the recorded header or the core header, never a mixture:

- under the recorded header, `yes` and `no` read as `true` and `false`;
- columns the recorded header lacks read as not recorded;
- the adapter writes nothing.

New Tasks use the core header. A Task that already holds a recorded table, including this one, keeps that header until its package leaves the tree. Its new rows put method, tool and exit facts in the Command and Result cells. The adapter is removed once the SPEC-0161, SPEC-0221 and SPEC-0222 packages have exited.

**Export.** The export is a reviewed one-time script, not committed, that parses the actual template Markdown. A registered extension heading or table is removed from the observed lists only when its registry entry names that exact heading or table, and the export then lists it under `extensions`. A classified domain or native template leaves the unmapped list and stays in `source_files`. Any other difference is a difference. `DECLARED_CORE_MATCH` covers form and template definitions only: not current documents, retained identities, runtime or approval. The Task lists the retained identities and recorded Task headers as declared deviations.

### Failure Behavior

- **Refused by the registry check:**
  - from WORK-009 on, a form without `core_role`;
  - a core-role form whose sections or tables lack a core member, or whose core member has a wrong type;
  - from WORK-009 on, a template whose form or native profile has no `core_role`;
  - an extension without `authority_ref`;
  - a column appended to a core table.
- **Refused by the document validators:**
  - a core table with a missing, reordered or relabeled column;
  - a cell of the wrong type;
  - a heading or table placed only inside a fence, quote or HTML block;
  - a mixed recorded and core Task header.
- **Stop condition:** if a table move cannot keep a recorded value's meaning without inventing a fact, the work stops and asks the user.

## Acceptance Criteria

### Criteria

| Criterion ID | Expected Result |
| --- | --- |
| VAL-CORE-001 | The registry carries `core_role` on every form and the core members on every core-role form, and its check refuses each drift kind under Failure Behavior. Focused negative tests cover each kind, including a table whose labels match but whose type differs. |
| VAL-CORE-002 | A fresh export of the registry and every template returns `DECLARED_CORE_MATCH` from the package tool with source hashes rechecked. Negative exports return non-match: a changed source hash, a missing role, `inventory_complete` false, an unclassified template, and an extension without its registry entry. |
| VAL-CORE-003 | Every template and current document of each changed role passes the strict document validators under the new forms and tables. Each moved sentence and cell is found again after normalization, with renames and dropped headings listed. One current document per applicable role is checked through the write, parse and validate round trip. |
| VAL-CORE-004 | Recorded Task rows of SPEC-0161, SPEC-0221 and SPEC-0222 and the retained identities are byte-unchanged, and the adapter reads them. The `document` suite and `python3 scripts/qa.py staged` pass. `scripts/validation/registry.json` gains no lane, and no test or script contains a template count. The residue rows W03-H45 to W03-H47 close in the SPEC-0221 Task (State and Closure cells only), and any new residue is recorded. |

### Verification Strategy

- The strict registry, markdown profile, link and owner, and lifecycle validators. The work residue ledger gate. The `document` suite once on the final tree. `python3 scripts/qa.py staged` through the commit hooks on each exact index.
- Focused RED and GREEN tests for each changed check. The source hash of each export script and export, and the comparison results, are recorded in the Task.
- Risk class `high` (registry model, validators and table contracts): an independent read-only review after WORK-001, after WORK-002 and before acceptance.

#### Normative and Evidence

- [REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md), [ADR-0059](../../02.architecture/decisions/0059-registry-common-form-model.md) and [ADR-0062](../../02.architecture/decisions/0062-accepted-decision-retained-form.md).
- The package targets, prompt, design D24 and comparison tool are evidence only; their SHA-256 values are in the Task.

#### Historical and Navigation

- [SPEC-0221](../0221-w03-form-target-adoption/spec.md) adopted the twelve heading trees and recorded W03-H45 to W03-H47.

### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0012](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-CORE-001 | [ADR-0059](../../02.architecture/decisions/0059-registry-common-form-model.md) | Registry check and focused negative tests |
| [REQ-0003-FR-0013](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-CORE-002 | [ADR-0059](../../02.architecture/decisions/0059-registry-common-form-model.md) | Package tool on a fresh export and negative exports |
| [REQ-0003-FR-0013](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-CORE-003 | [ADR-0062](../../02.architecture/decisions/0062-accepted-decision-retained-form.md) | Strict document validators, normalized move check and round trip |
| [REQ-0003-FR-0018](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-CORE-004 | [ADR-0059](../../02.architecture/decisions/0059-registry-common-form-model.md) | Byte comparison, document suite, staged QA and independent review |
| [REQ-0003-FR-0019](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-CORE-004 | [ADR-0059](../../02.architecture/decisions/0059-registry-common-form-model.md) | Residue closure and ledger gate |
