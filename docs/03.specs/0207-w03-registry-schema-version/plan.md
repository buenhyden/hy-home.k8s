---
title: "W03 Registry Schema Version Mapping Plan"
version: "1.0.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-14"
artifact_id: "SPEC-0207-PLAN-0001"
parent_ids: ["SPEC-0207"]
---

# W03 Registry Schema Version Mapping Implementation Plan

## Global Constraints

This work order follows the [Spec](spec.md) and inherits all of its boundaries. It adds three constraints: only the `schema_version` value, its schema property, its readers and the named texts change, so no profile, form, template, section or lifecycle domain changes; the diagnostics of the four strict document validators over the tree are equal before and after; and no later package is edited here: each later registry change applies its own bump at its implementation commit (W03-D66).

## Overview

Replace the integer registry `schema_version` by an explicit, meaning-preserving SemVer string, choose the current value `11.0.0` (generation 10 is `10.0.0`), route every reader through one function that checks the MAJOR number, state the four-level bump rule in the policy text and an amending ADR, and leave every later registry change a defined starting value. [Task 0001](tasks/tsk-0001-w03-registry-schema-version.md) owns execution and evidence.

## Context

A read of `main` at `81096a83` found the integer `10` in `docs/99.templates/registry.json` and a const of `10` in `docs/99.templates/contracts/document-profile.schema.json`. Three runtime pins read it: `scripts/document_contracts.py` (the `Registry` field set from `raw["schema_version"]`, and the strict check that refuses a value other than 10), `scripts/validate-document-lifecycle.py` (`registry_at`, which loads a history registry only when its value is 10 and otherwise falls back to the current registry) and `scripts/provider_write_guard.py` (`load_document_routes`, which fails closed with `schema_version must be 10`). `scripts/document_authority.py` holds only the key name. Three tests pin the integer (`tests/test_common_form_tree.py`, `tests/test_k8s_pre_edit_hook.py` with a synthetic 10 and a 9, and the `registry_at` mock of `tests/test_document_lifecycle_cumulative_history.py`). Five other files carry their own integer (the agent role registry 2, the two provider binding files 1, the validation registry 4, and the workspace memory database 1) and are out of scope. The history is in the Spec: ten generations from 2026-07-12 to 2026-10-05, the first eight under the key `schemaVersion` in a file that moved. ADR-0059 Decision 1 records that optional keys were added without a bump. SPEC-0205 plans the integer 11 and an amending ADR; it is revised to use this package's form and its MAJOR step.

## Goals & In-Scope

- Registry value, schema property, the reader function, the loader, the strict check, `registry_at` and the write guard, with the tests that pin them and the new test module.
- The glossary row, the version paragraph of `document-authoring.md` and one amending ADR, ADR-0061 (W03-D69).
- The evidence row and ledger closure in the SPEC-0161 Task, and the handoff for the other integer versions.

## Non-Goals & Out-of-Scope

- Any profile, form, template or lifecycle content; the removal of `sections` and the generation raise (SPEC-0205); the integer versions of other files; Contract Versions, Document Revisions, artifact identities and package edition labels; tags and releases.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-REGVER-001](spec.md#success-criteria--verification-plan) | `registry_schema_version`, the registry value and schema property, the loader, the strict check, `REGISTRY_MAJOR` and `READABLE_REGISTRY_MAJORS`, `registry_at`, the write guard constant and the tests that pin them, with the new test module registered. | Approved Spec and Plan; W03-D65 recorded by SPEC-0193; SPEC-0191 landed. This package lands right after SPEC-0191 and before SPEC-0192 and every later package (W03-D66). | [Task 0001](tasks/tsk-0001-w03-registry-schema-version.md) | Failing tests first, then passing; the strict registry validator; `grep` of every reader before and after. |
| WORK-002 | [VAL-REGVER-002](spec.md#success-criteria--verification-plan) | The glossary row, the version paragraph, the amending ADR, the SPEC-0161 Task evidence row and ledger closure, the end condition of the transitional branch, regression and exact-index QA. | WORK-001. | [Task 0001](tasks/tsk-0001-w03-registry-schema-version.md) | Strict validators, suites, quality gate, markdownlint, ruff, staged QA and hooks. |

## Verification Plan

- Record W03-D66 in the Task as the settled answers; the Spec has no open question.
- Replay the cumulative-history rules over the whole replay window (the review counted 256 commits, all with integer-10 blobs, 237 different from the current registry) before and after, and require equal diagnostics; a history blob with the integer 10 must yield its own profiles. A difference stops the work for the user.
- Record the four strict document validators and the `grep -rn "schema_version"` list before any change and after each work unit; every reader in the list is either changed, shown to read the value through the new function, or named in the Task as out of scope.
- Re-read `git log -G'"schema_version"'` and the predecessor file on the day of implementation and compare the table of the Spec with it; record any difference in the Task before the mapping is written.
- Show each test failing first, then passing, including the history reader with the integer 10 and the guard with a string.
- Check that `git diff --stat` touches the registry in the `schema_version` line only, and that the schema diff touches the one property.
- Before each commit, rebase on `main` and renumber the rows this package appends to the SPEC-0161 Task. Commit order: the package commit; then `.secrets.baseline` changes alone; then the implementation with the Task evidence. Run the staged lifecycle check before each commit and `graphify update .` after the code change.
- Record the risk class (`medium`: the registry, its schema, the write guard hook pin, the history reader and tests; no permission, trigger or workflow) and the core-diff checklist.

## Risks & Mitigations

Risks use the risk-report scale (likelihood Likely, Possible or Unlikely; impact Severe, Moderate or Minor), rated from the read of `81096a83`.

- **The write guard rejects a valid registry and blocks all document writes.** Possible, Severe: HIGH, mitigate. Owner: W05 code. The guard fails closed on any registry it cannot read, so a pin that disagrees with the registry stops every governed edit. Mitigation: a consistency test compares the guard's MAJOR number with the registry and the schema, and the guard tests cover the string, the integer and another MAJOR number. Review cue: the guard test results. Signal that raises it: the hook reports `HOOK-DOC-REGISTRY` on the repository registry. Rollback: revert the implementation commit, which restores the integer in all readers together.
- **The history reader drops the replay window.** Possible, Severe: HIGH, mitigate. Owner: W05 code. `registry_at` is the one consumer that sees integers after this package, and a fallback to the current registry would change the classification of 237 of 256 replay commits (REQ:113, REQ:778). Mitigation: `READABLE_REGISTRY_MAJORS` lists `10` and `11`, the integer 10 maps to `10.0.0` and is read with its own typed reading, a test shows an integer-10 blob yielding its own profiles, and the replay before and after is compared. Review cue: that test and the replay result. Signal that raises it: any change in cumulative-history diagnostics over the tree. Rollback: revert the implementation commit.
- **The current-version choice is contested.** Possible, Minor: LOW, monitor. Owner: W03 author. W03-D66 decides it: the integer-to-string change is MAJOR, so the value is `11.0.0`. Review cue: the recorded decision. Signal that raises it: a package that lands before this one. Rollback: change the value and the schema constant together.
- **SPEC-0205 and its amending ADR conflict with this package.** Likely, Minor: MEDIUM, monitor. Owner: W03 author. SPEC-0205 and W03-D63 planned the integer 11; its drafter revises it to the string form and its own MAJOR step after this package. Review cue: the SPEC-0205 Spec text at the landing. Signal that raises it: an integer in a SPEC-0205 diff. Rollback: revise SPEC-0205 before its approval.
- **The mapping table survives as an old history table.** Unlikely, Minor: LOW, monitor. Owner: W03 author. REQ:890 treats it as temporary input; it lives in the Spec and leaves with the package, and the policy text carries one sentence. Review cue: the policy text diff. Signal that raises it: a table of generations in a current document. Rollback: remove the table.
- **Another file with an integer version is read as in scope.** Unlikely, Minor: LOW, monitor. Owner: W03 author. W03-D66 names them, hands them to W01, W05 and the SPEC-0191 owner, and the Task records the handoff. Review cue: the Task handoff row. Signal that raises it: a diff outside the Spec's scope. Rollback: revert that part.

## Completion Criteria

Both criteria need PASS evidence, no unresolved required failure and the operator's acceptance.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| Registry Schema Version form, mapping rule and four-level bump rule | [Document authoring policy](../../../.agents/governance/document-authoring.md) | Version paragraph; `registry_schema_version` in `scripts/document_contracts.py` |
