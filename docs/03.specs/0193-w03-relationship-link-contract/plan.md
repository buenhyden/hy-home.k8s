---
title: "W03 Relationship and Link Contract Plan"
version: "1.1.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-14"
artifact_id: "SPEC-0193-PLAN-0001"
parent_ids: ["SPEC-0193"]
---

# W03 Relationship and Link Contract Implementation Plan

## Global Constraints

This approved work order follows the [approved Spec](spec.md) and inherits all of its boundaries. It adds three constraints: no relation changes its meaning, owner or check, and no form, template, body contract or heading changes; the only document edits outside the two policy texts are fragment repairs; and the diagnostics of the four strict document validators over the tree are equal before and after apart from those repairs. The design choices follow W03-D51 as the Spec states them.

## Overview

Record the eight document relations (one for each DOC-09 concept, the verification evidence and the two further kinds), the seven relation kinds and the four link types in one registry section with the checks and tests that already enforce them, check that record from the strict registry validator, add the fragment check to the link validator with its repairs, update the two policy texts, and close W03-H08 and W03-H16. [Task 0001](tasks/tsk-0001-w03-relationship-link-contract.md) owns execution and evidence.

## Context

A read of `main` at `de64c58d` (after SPEC-0186, which has left the tree; the registry holds 18 forms) found the relations spread over four carriers and no contract that names them together. `direct_parent` in `scripts/document_contracts.py` derives a Plan's and a Task's parent from the package path, and `PARENT-IDENTITY` (profile and link validators) and `TASK-PARENT-APPROVAL` (lifecycle validator) check it. The `Lifecycle Traceability` body contracts of the six SDLC profiles carry requirement basis and design constraints as link columns checked against allowed profiles, except the Spec `Architecture` column, whose links no rule checks. `PLAN-PROMOTION` reads the Plan `Promotion` table. `LIFECYCLE-EVIDENCE` enforces reciprocal supersession for the lifecycle domains that have a `superseded` state and refuses a chain without a current document. `scripts/document-backlinks.py` derives the reverse view on demand (SPEC-0164). The link validator resolves a link's path and skips its fragment, and markdownlint `MD051` is disabled; an approximate count found about 960 fragment links outside the archive, three broken (`examples/sample-app/README.md` and `gitops/workloads/README.md` to `../README.md#verification`, and one same-file link in the published research member m0007), and 125 into Stage 01 to 03 documents. SPEC-0181 is the model for a registry section whose entries name consumers, rules and tests (`frontmatter_keys`, `REGISTRY_KEY_CONSUMER`, `REGISTRY_KEY_TEST`). Phase 3 continues after this package with the Requirement, Architecture, ADR, Spec and Plan, and Task form packages and the removal of the H2-list model, in the order W03-D49 fixes.

## Goals & In-Scope

- Registry, schema and guard: the `relationship_contract` section, its schema and the optional top-level key.
- Code and tests: the loader, four strict registry rules, the supersession cycle observation, `LINK-FRAGMENT`, a new test module and fragment cases, with suite and surface registration.
- Documents: fragment repairs, the document authoring policy sentences, the Stage 99 README list, and the decision, closure and evidence rows of the SPEC-0161 Task with the matching work residue ledger entries once that ledger exists.

## Non-Goals & Out-of-Scope

- Forms, templates, headings, body contracts, frontmatter keys and lifecycle domains; reciprocal fields; the Plan `Promotion Map` reader (W03-H10); the six SDLC TemplateDefinitions (W03-H13); a Spec `Architecture` link check; an automated `commit:path` reachability check; cross-repository equivalence; Q-07.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-RELATION-001](spec.md#success-criteria--verification-plan) | The registry section with its 19 entries (seven kinds, eight relations, four link types), the schema, the authority guard key, the loader, the four strict registry rules (including `REGISTRY_RELATION_CYCLE`) and their tests with suite and surface registration. | Approved Spec and Plan; SPEC-0191 and SPEC-0207 merged first, in that order, then SPEC-0187, SPEC-0188, SPEC-0189 and SPEC-0192, then this package; rebase on `main` and renumber appended rows before each commit. | [Task 0001](tasks/tsk-0001-w03-relationship-link-contract.md) | Failing tests first, then passing; the strict registry validator. |
| WORK-002 | [VAL-RELATION-002](spec.md#success-criteria--verification-plan) | `LINK-FRAGMENT` with its tests, the supersession cycle observation of `LIFECYCLE-EVIDENCE` (one successor graph over `supersedes` and `superseded_by`, every document of the proposed tree) with its tests, the fragment repairs, the two policy texts, the SPEC-0161 Task rows (W03-D49 to W03-D52 and W03-D65) and ledger entries, regression and exact-index QA. | WORK-001. | [Task 0001](tasks/tsk-0001-w03-relationship-link-contract.md) | Fragment tests failing first, then passing; strict validators, suites, quality gate, markdownlint, ruff, staged QA and hooks. |

## Verification Plan

- Record the four strict document validators before any change, and again after each work unit.
- Before writing an entry, read the rule it cites in the named script and the test it names, and record in the Task one line per entry: the rule, what it enforces and the gap, if any. An entry never cites a rule for a relation that rule does not enforce.
- Show each registry rule, the supersession cycle observation and each fragment case failing first, then passing. Before enabling the cycle observation, list the documents it would report over the tree (the pre-approval read of `81096a83` found six documents with `supersedes`, none with `superseded_by`); a non-empty list stops the work for the user. Before any repair, record the exact list of fragments the implemented check reports over the tree, and compare it with the three found before approval.
- Confirm that no profile, form, template, body contract or lifecycle domain changed (`git diff --stat` over `docs/99.templates/templates/` is empty and the registry diff touches the new section only), and that each repaired document changed only in its link destinations, `version` and `updated`.
- Before each commit, rebase on `main` and renumber the rows this package appends to the SPEC-0161 Task. Commit order: the package commit with the W03-D49 to W03-D52 and W03-D65 rows; then `.secrets.baseline` changes alone; then the implementation with the Task evidence. Run the staged lifecycle check before each commit and `graphify update .` after the code change.
- Record the risk class (`medium`: the registry, its schema and guard, two validators and tests; no permission, trigger, hook or workflow) and the core-diff checklist.

## Risks & Mitigations

Risks use the risk-report scale (likelihood Likely, Possible or Unlikely; impact Severe, Moderate or Minor), rated from the pre-approval read.

- **An entry cites a rule that does not enforce its relation.** Possible, Minor: LOW, monitor. Owner: W03 author. The pre-approval read already withdrew two such citations; each entry is written after reading its rule, and the registry rule checks only that the identifier exists. Review cue: the per-entry line in the Task. Signal that raises it: a cited rule whose test does not exercise the relation. Rollback: correct the entry.
- **The fragment slug rule differs from the renderer.** Possible, Moderate: MEDIUM, monitor. Owner: W05 code. Slugs come from the validator's own heading scan, and tests cover punctuation, repeated headings, explicit anchors and Korean headings. Review cue: the before and after list over the tree. Signal that raises it: a reported fragment that resolves in the rendered page, or a link that fails there while the check passes. Rollback: revert the implementation commit.
- **A broken fragment sits in a document that may not be edited.** Unlikely, Moderate: LOW, monitor. Owner: W03 author. The pre-approval read found none in a finished package or a terminal document, and a published member may change its link destinations. Review cue: the exact list recorded before repair. Signal that raises it: a reported path under a freeze gate. Rollback: none; the author stops and asks the user.
- **The cycle observation reports a case the tree holds.** Unlikely, Moderate: LOW, monitor. Owner: W05 code. The pre-approval read of `81096a83` found six documents with `supersedes` and none with `superseded_by`, so no case is expected. Review cue: the list recorded before the observation is enabled. Signal that raises it: any reported document. Rollback: none; the author stops and asks the user.
- **A relation entry for authority or change impact overstates a check.** Possible, Minor: LOW, monitor. Owner: W03 author. Both entries record a gap (no existence check of a `policy_refs` path or of a definition's `consumer_paths`) and cite only rules that read their carrier. Review cue: the per-entry line in the Task. Signal that raises it: a cited rule that does not read the carrier. Rollback: correct the entry.
- **The new check blocks the later form packages.** Likely, Minor: MEDIUM, monitor. Owner: each form package's author. This is the intended effect: 125 fragment links target Stage 01 to 03 documents and a renamed heading must repoint them in the same change. The Spec and Plan form package (package 5 of W03-D49) repoints the 57 links to the Spec criteria anchor, the ones in frozen records under the W03-D50 exemption. Review cue: each form package's link list. Signal that raises it: a rename that cannot repoint a link in a frozen record outside that exemption. Rollback: none needed.
- **Earlier packages edit the registry and the SPEC-0161 Task first.** Likely, Minor: MEDIUM, monitor. Owner: W03 author. SPEC-0187 is open on its branch and SPEC-0188, SPEC-0189, SPEC-0191 and SPEC-0192 are approved and pending, and all edit these files; SPEC-0191 also adds an optional top-level registry key (`work_residue`) with its schema property, so it and this package both edit the `OPTIONAL_TOP_LEVEL_KEYS` set of `scripts/document_authority.py`, the registry loader, the tests that pin the top-level key set and `scripts/validation/registry.json`. SPEC-0207 lands right after SPEC-0191 and changes `schema_version` to a SemVer string, so this package also applies its expected MAJOR bump (a new top-level key) to the registry, the schema `const`, `REGISTRY_MAJOR`, `READABLE_REGISTRY_MAJORS` and the write guard constant at its implementation commit and records the level and the reason in the Task. This package merges after them in the order SPEC-0191, SPEC-0207, then SPEC-0187, SPEC-0188, SPEC-0189 and SPEC-0192, and is rebased on `main` with its appended rows renumbered before each commit. Review cue: the base commit recorded in the Task. Signal that raises it: a merge conflict in any of these files, or an appended row number already taken on `main`. Rollback: rebase the package.

## Completion Criteria

Both criteria need PASS evidence, no unresolved required failure and the operator's acceptance.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| Relation, relation-kind and link-type meaning with the fragment rule and the cycle rule | [Document authoring policy](../../../.agents/governance/document-authoring.md) | Link and relationship rule; `relationship_contract` in `docs/99.templates/registry.json` |
