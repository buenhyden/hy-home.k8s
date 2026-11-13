---
title: "W03 Work Residue Ledger Plan"
version: "1.0.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-13"
artifact_id: "SPEC-0191-PLAN-0001"
parent_ids: ["SPEC-0191"]
---

# W03 Work Residue Ledger Implementation Plan

## Global Constraints

This approved work order follows the [approved Spec](spec.md) and inherits all of its boundaries. It adds four constraints: no recorded Task row, EVD row, decision or handoff is rewritten, and the SPEC-0161 Task changes by appended lines and its frontmatter `version` and `updated` only; no view is committed; the gate reads the files under its root only, with no Git history and no network; and the diagnostics of the four strict document validators over the tree are equal before and after. No existing gate or test is weakened.

## Overview

Record W03-D47, then build the ledger schema, the `work_residue` registry block, the drift and closure gate, the on-demand view and their tests; register the gate and its routes; seed the ledger and the `Residue Handoff` table of the SPEC-0161 Task from current truth and register the legacy tables as historical; update the REQ-0003 check cells, AD-0006 and the policy sentences; and close W03-H30 and the `LEDGER` conflict through the ledger cycle. [Task 0001](tasks/tsk-0001-w03-work-residue-ledger.md) owns execution and evidence.

## Context

A read of `main` at `8231f782` found:

- `docs/03.specs/` holds one package, SPEC-0161; SPEC-0185 was merged by pull request #250, closed and left the tree, and Git history recovers it; every current handoff table is in the SPEC-0161 Task (version 0.1.24, last evidence row EVD-046, last decision W03-D40), whose status is `completed` and which already carries sections appended after completion (EVD-023, EVD-025);
- that Task has 33 handoff rows (W02-H01 in `Stage Follow-up Handoffs`, W03-H01 to W03-H32 inside the `W03 Decisions` table), 6 `Conflicts` rows, 52 `Requirement Changes` rows with 26 recorded `OPEN`, 20 `Document Form Handoff` rows, 20 `Stage QA Handoff` rows, 8 `Read Denominator` rows and 14 `OPEN Dispositions` with 12 corrections; W03-H31 records that several of these states are stale;
- the handoff rows have no state cell, most keep owner and resume condition in one cell, and `W03 Decisions` mixes rows of four and five cells under a four-column header, which the exact-column readers reject;
- the `sdlc/task` profile registers the Task Table, Task Evidence and Criterion Acceptance tables and no handoff table; `common_forms` has twelve forms and none for the Task, the profile fixes H2 names only, and every appended H3 of the SPEC-0161 Task sits under `Task Evidence` after the evidence table; the Stage 03 README is a `common/readme-stage-index` whose `Current Items` index `readme_navigation` marks complete, and the Stage 03 folder holds no non-Markdown file today; a `Resolves` cell admits EVD IDs only and closes earlier `FAIL`, `DEFER` or `NOT_RUN` rows only (`scripts/document_contracts.py`);
- the readers to reuse are `_exact_heading_section`, `_first_visible_table` and `task_base_evidence_rows` of `scripts/validate-links-and-owners.py`, `schema_errors` of `scripts/json_schema_validation.py` and the bounded helpers that `scripts/document-backlinks.py` uses;
- `scripts/validation/registry.json` (schema version 4) has 33 validators and 43 surfaces, matches by exact value or anchored regex with no precedence, and `scripts/validate-affected-surfaces.py` requires `uncovered=0 ambiguous=0`: `docs/03.specs/**` belongs to `authored-documents`, new scripts fall into the `scripts` regex, `docs/99.templates/contracts/*.json` to `stage99-machine-contracts`, and a new `tests/test_*.py` has no route until one is added;
- `scripts/run-contract-tests.py` runs named suites, each test module in exactly one; `document_backlinks` is in `tooling` and the Task row tests are in `document`;
- the Stage 99 registry is closed at top level (`additionalProperties: false`), so a new block needs its property in `document-profile.schema.json`; `readme_navigation` already holds path lists; `shared_contract` has six `unverified` approval facts and `common_forms` holds `contract_id`, `version` and `forms`;
- `scripts/validation/repository/quality.py` refuses a tracked `progress.md`, and the document routes of `tests/test_common_agents_document_routes.py` classify Markdown only, so a JSON file under `.agents/` has no document route today;
- ADR-0060 is `accepted` (version 1.0.1) and REQ-0003 is at version 3.4.1 with the amended FR-0019 and FR-0022; their check cells still say that package 2 builds and checks the ledger, AD-0006 (version 2.5.0) calls the ledger a separate repository file without naming it, and the `LEDGER` conflict row and the W03-H30 row keep their recorded text.

## Goals & In-Scope

- Contract and code: the schema, the `work_residue` block and its registry-schema property, the gate, the view, the tests, the suite row, the validator entry, two surfaces and the route carve-outs.
- Data: the ledger seeded from current truth; the appended `Residue Handoff` table, the historical-table registrations and the EVD rows in the SPEC-0161 Task.
- Text: the REQ-0003 check cells, the AD-0006 sentence, the work lifecycle and Stage 03 `AGENTS.md` sentences, the Task template prompt and the README entries.

## Non-Goals & Out-of-Scope

- Stage 90 entries; hold, disposition and retention entries; rewriting recorded rows; the W03-H31 corrections; the phase-3 Task form; a committed view; accepted ADRs; registry pointers below the two keys.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-RESIDUE-001](spec.md#success-criteria--verification-plan) | Schema, registry block, gate, view, tests, suite row, validator entry, surfaces and carve-outs; the seed that the gate needs to pass (entries, the appended table and the historical registrations). | Approved Spec and Plan; W03-D47 recorded with the package commit. | [Task 0001](tasks/tsk-0001-w03-work-residue-ledger.md) | Failing tests first, then passing; the gate over the tree; the affected-surface check. |
| WORK-002 | [VAL-RESIDUE-002](spec.md#success-criteria--verification-plan) | The seed record per kind and table; the check cells, AD-0006 and policy sentences; regression and exact-index QA; the closure of W03-H30 and `LEDGER` through the ledger cycle. | WORK-001. | [Task 0001](tasks/tsk-0001-w03-work-residue-ledger.md) | Strict validators, suites, quality gate, markdownlint, ruff, staged QA and hooks; the append-only diff of the SPEC-0161 Task. |

## Verification Plan

- Record the four strict document validators before any change.
- Read current truth row by row before seeding: for each legacy row, record whether it is open and the evidence (a merged package, a later decision or an EVD row) when it is not. A row whose state cannot be shown is seeded open and named in the Task as unverified.
- Show each refusal test failing before the gate exists and passing after; no test runs the gate over the repository.
- Run the gate over the tree after the seed, then the view, and confirm with `git status --short` that the view wrote nothing; the gate run also shows that no seeded owner or resume condition trips the copied-value scan, and the README navigation check shows the Stage 03 index complete with the ledger listed.
- Confirm that the diff of the SPEC-0161 Task has added lines only, apart from its frontmatter `version` and `updated`.
- Commit order: (1) the package commit with this Task, the Korean Stage 03 README entry and the decision row W03-D47; (2) `.secrets.baseline` changes alone, including any line moved by the registry edit; (3) the implementation in one commit, because the gate refuses the tree without the seed and the seed is unchecked without the gate: schema, registry block, gate, view, tests, registration, the seeded ledger, the appended table and the historical registrations, with the text changes and the Task evidence; (4) after the user's acceptance, the closing EVD row that makes W03-H30 and `LEDGER` terminal; their entries are deleted no later than the exit commit. Run the staged lifecycle check before each commit and `graphify update .` after the code change.
- Merge order: SPEC-0190 (schemas and glossary; the exclusion list of `scripts/validation/registry.json` gains `semver_grammar.py`), SPEC-0186 to SPEC-0189 and SPEC-0192 touch `scripts/validation/registry.json`, `scripts/run-contract-tests.py`, `document-profile.schema.json` and the SPEC-0161 Task. This package rebases on `main` before each commit, re-reads the route exclusions and suite rows it edits, and renumbers appended rows on collision; W03-D46 is SPEC-0190's deviation decision, W03-D47 this package's and W03-D48 SPEC-0192's.
- Record the risk class (`medium`: a registry, schema, template, validator, test and policy-text change; no permission, secret-handling, hook or workflow) and the core-diff checklist.

## Risks & Mitigations

Risks use the risk-report scale (likelihood Likely, Possible or Unlikely; impact Severe, Moderate or Minor), rated from the tree read above.

- **The seed misjudges current truth.** Likely, Moderate: HIGH; it blocks the seed commit. Owner: W03 author. W03-H31 records stale states in the same tables. Each seeded and unseeded row is recorded with its evidence, and an unprovable row is seeded open. Review cue: the seed EVD row. Signal that raises it: an entry for closed work, or an open row with no entry. Rollback: revert the implementation commit.
- **Residue written as prose stays undetected.** Likely, Minor: MEDIUM, monitor. Owner: W03 author. The SPEC-0161 Verification Summary names next owners in a sentence today, and the recognizer reads tables only. The work lifecycle sentence sends residue to the live table. Review cue: the core-diff checklist of each package. Signal that raises it: a next owner named only in prose.
- **The ledger is read as a progress ledger or a second owner of execution state.** Possible, Moderate: MEDIUM, monitor. Owner: W03 author. The schema closes every object and has no key for status, result or evidence, and the status-value test reads the Task domain from the registry. Review cue: any schema change. Signal that raises it: a new entry key. Rollback: revert the key.
- **A route change leaves a path uncovered or ambiguous.** Possible, Moderate: MEDIUM, mitigate. Owner: W05 code. Two existing regex routes gain exclusions. Review cue: `python3 scripts/validate-affected-surfaces.py --root .`. Signal that raises it: a count other than `uncovered=0 ambiguous=0`. Rollback: revert the registry edit.
- **The new gate blocks unrelated document commits when the ledger drifts.** Possible, Moderate: MEDIUM, mitigate. Owner: W05 code. The gate runs on every Stage 01 to 90 document change. Each diagnostic names the entry and the field, and the repair is one row or one entry. Review cue: the first packages after this one. Signal that raises it: a refusal on a document that holds no residue. Rollback: correct the row or entry; never remove the gate from the surface.
- **Concurrent packages edit the ledger, the registries and the SPEC-0161 Task.** Possible, Moderate: MEDIUM, mitigate. Owner: W03 author. Entries are sorted, appended numbers are re-read at commit time and the later package rebases. Review cue: the diff against current HEAD before each commit. Signal that raises it: a duplicate ID. Rollback: renumber before commit.
- **The copied-value check refuses honest text.** Possible, Minor: LOW, monitor. Owner: W05 code. Only contract identifiers, digests, revisions and approval references are matched, not versions or owner names. Review cue: the first adoption entries. Signal that raises it: a refusal with no copied value.
- **Not scored:** how often residue will have no Task owner (W03-D47 allows such survey entries). No evidence in the tree shows the rate; the first such entry is the review cue.

## Completion Criteria

Both criteria need PASS evidence, no unresolved required failure and the operator's acceptance. W03-D47 is recorded with the package commit and is not part of either criterion.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| Work residue ledger shape, residue row form and refusals | `docs/99.templates/registry.json` `work_residue` and `docs/99.templates/contracts/work-residue-ledger.schema.json`; [REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md) FR-0019 and FR-0022 | The registry block, the schema and the two check cells; the gate in `scripts/validation/registry.json` |
| Where residue is written and when it leaves | [Work lifecycle](../../../.agents/workflows/work-lifecycle.md); Stage 03 `AGENTS.md` | Completion step 4; Allowed Surface and rule 7 |
