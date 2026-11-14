---
title: "W03 Document Generator Plan"
version: "1.0.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-14"
artifact_id: "SPEC-0192-PLAN-0001"
parent_ids: ["SPEC-0192"]
---

# W03 Document Generator Implementation Plan

## Global Constraints

This approved work order follows the [approved Spec](spec.md) and inherits all of its boundaries. It adds three constraints: the generator restates no registry, identity or lifecycle rule and calls the existing owner of each, and the one extraction that makes a rule callable changes no diagnostic; no existing document, template, profile or lifecycle domain changes; and the diagnostics of the four strict document validators over the tree are equal before and after.

## Overview

Build `scripts/document-generator.py` with its round-trip and negative tests, give the reference pack anchors a path-derived identity, move the creation-state derivation of the lifecycle reader into a public function, register the test module and route the two new files, correct the registry `version` sentence, name the generator in the policy texts, and record W03-D48, the W03-H27 closure and the new repair handoff row in the SPEC-0161 Task. [Task 0001](tasks/tsk-0001-w03-document-generator.md) owns execution and evidence.

## Context

A read of the tree at `8231f782`, main after SPEC-0185, and a simulation over a copy of that tree outside the repository, run with the pinned validation interpreter and `ruamel.yaml` 0.19.1, found the following. The registry, the templates, `scripts/` and `tests/` are unchanged since `c54eed50`, main after SPEC-0184. The SPEC-0161 Task's chain table records the Generator link as absent. The registry has 87 profiles: 39 template-mode, 9 without a template and 39 with one (28 authored, 6 router, 5 native). Filling the five shared markers into each generable template and running the strict profile check gave no `FM-` and no identity finding for 32 of the 35 generable profiles. The three reference pack anchors kept the ARTIFACT_ID marker and drew `FM-VALUE-PATTERN`, because `expected_artifact_id` derives nothing for them and no check binds their identity to the pack folder number; the three anchors in the tree match their folders. The findings that remained on a fresh document were `BODY-AUTHOR-PROMPT`, `BODY-H1-PLACEHOLDER`, `BODY-HEADING-EMPTY`, `BODY-SECTION-EMPTY` and, for a Requirement, `REQUIREMENT-PACKAGE-MEMBER-ID`. Only the spec-plan and task lifecycle domains declare `initial_states`; the others derive them, and the `requirement` domain derives none, so `_create_diagnostics` returned `LIFECYCLE-CREATE` for a new Requirement at `draft`; the registry check refuses an `initial_states` entry that has an inbound edge, so the repair is a lifecycle contract change of its own. `Archived Lineage` reserves 152 identities, 143 of them Spec identities from SPEC-0001 through SPEC-0185; SPEC-0192 is unused and unreserved. The registry `version` entry says a document starts at `1.0.0`, where the authoring policy, the Stage 99 README and every template that carries a version say `0.1.0`. `scripts/document-backlinks.py` is the precedent for a tool that is no gate; its test sits in the `tooling` suite, which the Stage 99 surfaces do not select, where they do select the `document` suite. The simulation called validator functions directly; no staged QA run is part of it. On 2026-11-13 the user adopted the recommended answer to each of the ten design choices (W03-D48). Cross-package note: this package needs no unmerged package's behavior but shares edit points with the packages around it. SPEC-0190 is merging and adds `scripts/semver_grammar.py` to the exclusion list of the generic `scripts` surface route in `scripts/validation/registry.json`, the list this package extends for the generator. SPEC-0186 to SPEC-0189 also edit the SPEC-0161 Task and the registry. SPEC-0191 adds the work residue ledger, a live `Residue Handoff` table in the SPEC-0161 Task and `docs/03.specs/work-residue-ledger.json`. Merge order: this package rebases on main after SPEC-0190 and after whichever of SPEC-0186 to SPEC-0189 and SPEC-0191 have merged by then, and re-reads those edit points on that base. If SPEC-0191 lands first, the W03-H27 closure and the repair handoff are each a live `Residue Handoff` row with a ledger entry in the same change; if this package lands first, they are appended handoff rows and SPEC-0191's seed includes them. This plan touches the Stage 99 consumer plane of AD-0006 and no ADR; migration is none, because the generator is additive, and rollback is a revert of the implementation commit.

## Goals & In-Scope

- The command, its refusals and its output check; the round-trip and negative tests.
- The pack anchor identity in `expected_artifact_id` with its failing-first test.
- The creation-state extraction in `scripts/document_lifecycle.py` with its direct test.
- Suite membership, exact surface routes and the carve-out from the generic `scripts` route; the `scripts/README.md` row; the policy sentences; the registry `version` sentence.
- The W03-D48 row, evidence rows, W03-H27 closure and the repair handoff row for the `sdlc/requirement` creation state in the SPEC-0161 Task, in the form current at merge, with ledger entries once SPEC-0191 has merged.

## Non-Goals & Out-of-Scope

- Renumbering, number allocation, the design, schema, script and checks of the work residue ledger, the Requirement lifecycle domain, templates, profiles, the schema, provider-native projections, README index rows and existing documents.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-GEN-001](spec.md#success-criteria--verification-plan) | The command, the fill, the output check, the creation-state extraction, the round-trip tests, suite membership, surface routes and the `scripts` route carve-out. | Approved Spec and Plan; main at or after `8231f782`, rebased as Context states. | [Task 0001](tasks/tsk-0001-w03-document-generator.md) | Failing tests first, then passing; the generable set equals the sample set. |
| WORK-002 | [VAL-GEN-002](spec.md#success-criteria--verification-plan) | Identity, parent, occupied-path and status refusals; the pack anchor identity in the profile check. | WORK-001. | [Task 0001](tasks/tsk-0001-w03-document-generator.md) | Negative tests with an unchanged tree; pack anchors in the tree draw no new finding. |
| WORK-003 | [VAL-GEN-003](spec.md#success-criteria--verification-plan) | Remaining negative tests; policy texts and the key table sentence; SPEC-0161 Task rows and, once the ledger exists, its entries; regression and exact-index QA. | WORK-002. | [Task 0001](tasks/tsk-0001-w03-document-generator.md) | Strict validators, suites, quality gate, markdownlint, ruff, staged QA and hooks. |

## Verification Plan

- Record the four strict document validators over the tree before any change, and re-observe the profile, template and reserved-identity counts of Context on the implementation base, because a package that lands first can change the forms.
- Show each round-trip and negative test failing first and then passing. Record in the Task the generable and refused profile sets and the authoring rule set observed on fresh output.
- Show the pack anchor test failing first, then passing, and the three anchors in the tree unchanged and without a new finding.
- Show the direct test of the creation-state function failing first and then passing, and the `document` and `document-lifecycle` suites passing with no changed lifecycle diagnostic.
- Confirm with `python3 scripts/validate-affected-surfaces.py --root .` that the generator and its test each match exactly one surface, with no `SURFACE-PATH-AMBIGUOUS` and no `SURFACE-PATH-UNMATCHED`.
- Run the command once into a temporary copy of the tree for a Spec, a Plan and a Task and record the printed lines; generate nothing into the repository.
- Architecture compliance: confirm in the core-diff checklist that the generator imports its rules from the existing owners, writes no provider-native file and stores no state, as AD-0006 requires of a Stage 99 consumer; a departure returns the Spec to in-review.
- Commit order: the package commit; then `.secrets.baseline` changes alone; then the implementation with the Task evidence. Run the staged lifecycle check before each commit and `graphify update .` after the code change.
- Record the risk class (`medium`: one new tool that writes a file only on an explicit call, one validator function, one behavior-preserving extraction in the protected lifecycle reader, one registry sentence, one suite and its routes; no permission, trigger, hook or workflow) and the core-diff checklist.

## Risks & Mitigations

Risks use the risk-report scale (likelihood Likely, Possible or Unlikely; impact Severe, Moderate or Minor), rated from the Context evidence.

- **A new Requirement cannot be created.** Likely, Minor: MEDIUM, monitor. Owner: W03. The simulation observed the empty creation set; the generator refuses the profile by rule (W03-D48) and the new handoff row carries the repair to its own package. Review cue: the handoff row. Signal that raises it: a Requirement must be created before that package lands. Rollback: none needed.
- **The command runs under an interpreter without the YAML library.** Likely, Minor: MEDIUM, monitor. Owner: W05. The bare system `python3` has no `ruamel.yaml`, while the pinned validation interpreter has 0.19.1; the loader fails closed with its install command and the generator adds no fallback. Review cue: the first run of the command. Signal that raises it: an import error. Rollback: none needed.
- **The generator drifts from the registry or a template.** Possible, Minor: LOW, monitor. Owner: W05 code. The output check runs the profile check on every write, and Stage 99 changes select the suite that carries the round trip. Review cue: the `document` suite. Signal that raises it: a `GENERATOR-OUTPUT` refusal. Rollback: revert the implementation commit.
- **The pack anchor identity flags an existing pack.** Unlikely, Moderate: LOW, monitor. Owner: W05 code. The three anchors in the tree match their folder numbers. Review cue: the before and after validator comparison. Signal that raises it: a new identity finding on a pack README. Rollback: revert the function change.
- **The extraction changes a lifecycle diagnostic.** Unlikely, Moderate: LOW, monitor. Owner: W05 code. `tests/test_document_lifecycle_cumulative_history.py` and `tests/test_task_acceptance_contract.py` exercise `LIFECYCLE-CREATE` and must pass unchanged. Review cue: the `document` and `document-lifecycle` suites. Signal that raises it: any changed lifecycle diagnostic. Rollback: revert the extraction.
- **A sibling package edits the same lines first.** Likely, Minor: MEDIUM, monitor. Owner: W03 author. The sibling drafts show SPEC-0190 editing the same `scripts` route and SPEC-0186 to SPEC-0189 and SPEC-0191 editing the SPEC-0161 Task and the registry; this package rebases and re-reads those edit points. Review cue: the rebase diff of `scripts/validation/registry.json` and the SPEC-0161 Task. Signal that raises it: a conflict or `SURFACE-PATH-AMBIGUOUS`. Rollback: none needed.
- **A write lands on or outside the intended path.** Unlikely, Moderate: LOW, monitor. Owner: W05 code. The target is checked against the root and the registry route and is created exclusively. Review cue: the negative tests. Signal that raises it: a changed tree after a refusal. Rollback: delete the created file.
- **An identity deleted from the working tree is reused.** Possible, Minor: LOW, monitor. Owner: W03 author. The generator reads the current tree only; the staged lifecycle check compares with the Git base and refuses the reuse. Review cue: the staged lifecycle check. Signal that raises it: `LIFECYCLE-IDENTITY-REUSE` on a generated document. Rollback: delete the generated file.
- **An author treats generated output as finished.** Possible, Minor: LOW, monitor. Owner: W03 author. The strict profile check refuses author prompts, the starter H1 and empty sections. Review cue: the profile check on the new file. Signal that raises it: none beyond that check. Rollback: none needed.
- **Not scored.** Whether a test pins the registry `version` sentence, and whether a package that lands first changes that entry or the shared markers, rests on no evidence yet; WORK-001 reads them on the implementation base before editing.

## Completion Criteria

All three criteria need PASS evidence, no unresolved required failure and the operator's acceptance.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| A new document starts from the generator or a hand copy of its form; the generator fills the shared markers and refuses unadmitted requests | [Document authoring policy](../../../.agents/governance/document-authoring.md) | Requirements, rule 2; the command row in `scripts/README.md` |
