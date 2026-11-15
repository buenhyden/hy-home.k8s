---
title: "W03 Requirement Creation State Plan"
version: "2.0.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-15"
artifact_id: "SPEC-0210-PLAN-0001"
parent_ids: ["SPEC-0210"]
---

# W03 Requirement Creation State Implementation Plan

## Overview

### Goal and Boundary

Show the gap with failing tests, declare `initial_states: ["draft"]` for the `requirement` domain, amend the registry check so that it accepts and requires that declaration, raise the Registry Schema Version at the MAJOR level, make `sdlc/requirement` a round-trip sample of the generator, correct any policy sentence that states the gap, and record this package's evidence rows and, at acceptance, the closure of W03-H43 and the REQ-0003 lineage row in the SPEC-0161 Task and REQ-0003. [Task 0001](tasks/tsk-0001-w03-requirement-creation-state.md) owns execution and evidence.

Goals and in-scope:

- The failing-first tests, the one registry entry, the two clauses of the registry check, the MAJOR raise with its reason, the generator sample and any policy sentence.
- This package's evidence rows, the W03-H43 closure with its ledger step in the SPEC-0161 Task, and the REQ-0003 completed-spec lineage row at closure. No decision row: W03-D71 to W03-D73 are already recorded.

Non-goals and out-of-scope:

- A domain's states or transitions, the other families, templates, profiles, forms, the lifecycle reader, the generator code, existing Requirement documents, numbering, the ledger design and hosted CI.

#### Global Constraints

This draft work order follows the [Spec](spec.md) and inherits all of its boundaries. It adds three constraints: no `states`, `transitions` or `profile_ids` of any lifecycle domain changes and `scripts/document_lifecycle.py` and `scripts/document-generator.py` stay as they are; the registry check is tightened in the two clauses the Spec names and in no other; and the diagnostics of the four strict document validators over the tree are equal before and after.

### Assumptions

Read at `main` `eb017bfe` (after pull request #262, SPEC-0208), with the registry `schema_version` at `12.0.0` on that base; the phase-3 registry packages SPEC-0194 to SPEC-0206 are expected to have landed before this package, so the registry is at `13.0.0` or later at implementation and every fact below is re-read on that base.

- The `requirement` domain of `docs/99.templates/registry.json` lists states `draft` (mutable), `in-review` (mutable) and `approved` (current), and transitions `draft` to `in-review`, `in-review` to `draft` and `in-review` to `approved`. Only the `spec-plan` and `task` domains declare `initial_states`; every other domain derives its creation state from the states without an inbound edge, and each has one except `requirement`, whose `draft` has the inbound rework edge.
- `creation_states(domain)` (`scripts/document_lifecycle.py` line 218) returns `domain.initial_states` when declared and otherwise the states without an inbound edge. `_create_diagnostics` and the generator both call it. `tests/test_document_artifact_identity.py` line 294 asserts that the `requirement` domain yields `()`, and `tests/test_document_generator.py` asserts the refusal at line 527 and adds `sdlc/requirement` to the sample set by hand at line 305.
- The strict registry check (`scripts/document_contracts.py` lines 1975 to 2030) refuses an `initial_states` entry with an inbound edge unless it is the local Task first-recording set, and requires `["draft"]` of `spec-plan` and the Task set of `task`. A `requirement` declaration of `["draft"]` is therefore refused today: the repair needs this check edited, which is why the level is MAJOR (Spec, Contracts).
- The profile schema already allows `initial_states` (a nonempty array of unique strings) on any domain. The requirement template carries `status: "draft"` and the shared markers only, so the profile is generable by form; `REQUIREMENT-PACKAGE-IDENTITY` is already in `IDENTITY_RULES` of the round-trip test, but `REQUIREMENT-PACKAGE-MEMBER-ID` (`scripts/validate-markdown-profiles.py` lines 795 to 808) is not in `AUTHORING_RULES`, and the template sample member `REQ-0001-FR-0001` does not match the prefix `REQ-9001-` of the sample path, so WORK-002 adds that rule to `AUTHORING_RULES` as an authoring finding and the failing-first run records the actual rule set.
- No current policy text states the gap: `.agents/governance/document-lifecycle.md` holds no creation-state sentence for a Requirement, and `document-authoring.md` line 51, `docs/99.templates/README.md` line 206 and `scripts/README.md` line 65 name the generator and no Requirement exception.
- W03-H43 is a live `Residue Handoff` row of the SPEC-0161 Task, recorded by EVD-058, with a ledger entry whose resume condition is "When the registry admits a creation state for the `requirement` lifecycle domain". The user decided this package on 2026-11-14 (W03-D71 intake; the design choices are W03-D73, recorded by the SPEC-0194 implementation commit).

Migration is none: no document changes. Rollback is the revert of the implementation commit.

## Dependencies

### Prerequisites

The prerequisites of each work unit are in the Dependencies column of the [Work Breakdown](#work-breakdown) table.

### Dependency Order

The order of the work units follows the Dependencies column of the [Work Breakdown](#work-breakdown) table.

## Implementation Strategy

### Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-REQCREATE-001](spec.md#criteria) | The survey; the failing-first creation-state, registry check and `LIFECYCLE-CREATE` tests; the registry entry; the two clauses of the registry check. | Approved Spec and Plan; main after SPEC-0206 and the decisions of W03-D73. | [Task 0001](tasks/tsk-0001-w03-requirement-creation-state.md) | Failing tests first, then passing; strict validators equal before and after. |
| WORK-002 | [VAL-REQCREATE-002](spec.md#criteria) | The Requirement sample, the `REQUIREMENT-PACKAGE-MEMBER-ID` authoring finding and the completeness assertion of the generator tests; the MAJOR raise; the policy survey; the SPEC-0161 Task rows and, at acceptance, the ledger cycle; regression and exact-index QA. | WORK-001. | [Task 0001](tasks/tsk-0001-w03-requirement-creation-state.md) | Strict validators, suites, routing check, ruff, staged QA and hooks; the ledger gate. |

### Change and Rollback

The rollback, where a risk states one, is under [Risks and Mitigations](#risks-and-mitigations).

## Verification Plan

### Verification Matrix

- Record the four strict document validators before any change, and re-read on the implementation base the registry value, the `requirement` entry, the lines named in Context and the Requirement template status.
- Survey the domains: compute `creation_states` for every domain of the registry and record that `requirement` is the only one that yields none. Grep the three policy files and the stage 01 README for a sentence that states the gap, and record the result.
- Show each new behavior failing first on the implementation base and then passing, and list the regression cases that already pass: the repository registry raising no `REGISTRY_LIFECYCLE_DOMAIN` once the entry exists; `["draft"]` on another family still refused (built from a synthetic added inbound edge); `in-review` to `draft` still accepted; `in-review` and `approved` still refused at creation.
- Show that `["draft"]` on another family with an inbound edge to `draft` is still refused, so the exemption stays narrow.
- Read the Registry Schema Version at the base, raise its MAJOR number once, record the base value, the level MAJOR and the reason of the Spec in the Task, and show the MAJOR constants and the schema version value updated together and the version tests of SPEC-0207 passing without an edit.
- Run the generator once for a Requirement into a temporary copy of the tree and record the printed line; generate nothing into the repository.
- Ledger cycle at acceptance: record the evidence row, make the live W03-H43 row terminal with it as Closure, make its ledger entry terminal and then delete it, and run `python3 scripts/validate-work-residue-ledger.py --root .` before and after each step.
- Architecture compliance: the work stays within AD-0006 and adds no gate, script or reader.
- Record the risk class (`medium`: a registry entry, a registry-check clause and a version raise; no permission, secret-handling, hook or workflow) and the core-diff checklist.

Completion criteria:

Both criteria need PASS evidence, no unresolved required failure and the operator's acceptance. The Spec leaves `draft` with its approval receipt; the decisions are recorded as W03-D73.

### Stage Placement

- Commit order: the package commit appends no decision row (W03-D71 to W03-D73 are recorded by the SPEC-0194 implementation commit) and only this package's evidence row(s); then `.secrets.baseline` changes alone; then the implementation with the Task evidence. Run the staged lifecycle check before each commit and `graphify update .` after the code change. Merge after SPEC-0206 and before SPEC-0209 (W03-D73), rebasing on `main` before each commit.

## Risks

### Risks and Mitigations

Risks use the risk-report scale (likelihood Likely, Possible or Unlikely; impact Severe, Moderate or Minor).

- **The registry check exemption admits a wrong declaration on another family.** Unlikely, Moderate: LOW, mitigate. Owner: W05 code. The exemption names the `requirement` family and `["draft"]` only, and a test refuses the same declaration elsewhere. Review cue: the negative cases. Rollback: revert the clause.
- **A MAJOR raise leaves a reader on the earlier number.** Possible, Moderate: MEDIUM, mitigate. Owner: W05 code. The constants and the schema value are edited together and the version tests of SPEC-0207 read them; the history reader lists the earlier MAJOR. Review cue: the first run of the document and lifecycle suites. Signal that raises it: a refused registry at a replayed commit.
- **A sibling package edits the same registry lines or constants first.** Likely, Minor: MEDIUM, monitor. Owner: W03 author. SPEC-0205 and SPEC-0207 touch the version and constants, and SPEC-0195 may move the Requirement form; this package rebases and re-reads them. Review cue: the rebase diff of the registry and the constants. Signal that raises it: a conflict or a changed sample path.
- **A new Requirement is created before this package lands.** Possible, Minor: LOW, monitor. Owner: W03 author. The creation rule and the generator both refuse it until then, so none can be created; no mitigation is needed. Rollback: none needed.
- **The level is read as too high.** Possible, Minor: LOW, monitor. Owner: W03 author. W03-D73 settled MAJOR with the user, and the Task records the reason; a lower level holds only if the earlier validator accepts the value, which the failing-first test of the earlier clause shows it does not.
- **Not scored.** Whether a Requirement already exists in Git history whose creation commit the cumulative replay would now judge differently rests on no evidence yet; WORK-001 runs the replay and records any first failing commit.

### Escalation

Escalation follows [Failure and Edge Cases](spec.md#failure-and-edge-cases) of the Spec.

## Promotion Map

### Durable Meaning

The durable contracts are the first column of the table under Owner and Receipt.

### Owner and Receipt

| Promotion ID | Target Owner | Acceptance | Evidence |
| --- | --- | --- | --- |
| The `requirement` domain declares its creation state, and the registry check requires it | [Document authoring policy](../../../.agents/governance/document-authoring.md) | The generator sentence of the policy names no Requirement exception, the `requirement` domain declares `["draft"]` and the registry check requires it, with PASS evidence for VAL-REQCREATE-001 and VAL-REQCREATE-002 | The generator sentence of the policy, which names no Requirement exception; the `requirement` entry of `lifecycle_domains` in `docs/99.templates/registry.json` and the lifecycle domain rule |
