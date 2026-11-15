---
title: "W03 Closing Report"
version: "2.0.0"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-11-15"
artifact_id: "SPEC-0211"
---

# W03 Closing Report Technical Specification (Spec)

## Overview

### Intent

This approved change contract is the report half of the W03 closing phase of the external v14.7 execution package (task file line 16: "closing H19/H20/H21/H31"; `REQ:n` below is line n of `_workspace/workspace_execution_tasks_v14_7_revision_20261113_r1/tasks/TASK-hy-home-k8s-W03.md`, a read-only input). It closes handoff W03-H20 ("W03 closing report (W03 section 11)") in the [SPEC-0161 Task](../0161-w00-v14-7-delta-intake/tasks/tsk-0001-w00-v14-7-delta-intake.md) and carries the duties of decision W03-D72: it closes the remaining parts of W03-H10 (README and Policy) and W03-H34 and W03-H35 after reading the final tree, moves DOC-12 to after W11 and DOC-S99 to W05 as the requirement assigns, and records each correction with an EVD row. It lands last in W03, after SPEC-0194 to SPEC-0208, SPEC-0210 (W03-H43, the creation state of the `requirement` lifecycle), the Q-07 preparation package (SPEC-0212, W03-D75) and SPEC-0209 (the records half: W03-H19, W03-H21, W03-H31, the writer delegation and the `Disposition Input` table). The [Plan](plan.md) orders the work and the [Task](tasks/tsk-0001-w03-closing-report.md) records execution.

The legacy row W03-H20 states the gap: no stage-level report, decision table, key table, migration table or stage acceptance exists; the W03-H01 and W03-H06 rows are not closed; OPEN-Q03 and WP-10, 11, 12, 13, 17, 18, 47 and 52 have no current disposition; and the accepted-ADR exception (W03-D02) is not stated as an exit exception. Its expected closure is "a closing section or package that closes the handoff rows, disposes the carried rows and states the exceptions", owner W03, resume "last before DOC-12". The requirement fixes what the report holds (section 11, REQ:828 to REQ:838), what a conflict-package classification holds (REQ:906 to REQ:916) and where execution records live (REQ:78, REQ:922).

At drafting, `main` was `eb017bfe`. The work residue ledger held 76 entries, 28 of them owned by `W03` alone, with W03-H20, W03-H10, W03-H34, W03-H35, DOC-12 and DOC-S99 among them. These figures are observations only: every count in this Spec and in the report is read from the final tree at implementation, after SPEC-0194 to SPEC-0210 have merged, and the Task records the observed value beside any figure named here.

### Owning Requirements

[AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) owns the governance view; no component changes. The report reuses the SPEC-0161 Task as the one owner of stage-level records (REQ-0003-FR-0019) and the ledger cycle of ADR-0060 for closure. It adds no gate, validator, script, key or table definition outside the Task, and it adds no progress ledger: the report states a result and its owners and does not track work.

## Scope

### In Scope

- In scope (writer W03; records and ledger data only, no code, schema, registry, form, template or document body): in the SPEC-0161 Task, appended rows (evidence rows, the report tables listed in Contracts), the `Owner` and `Resume condition` cells of the live residue rows that Contracts section "D72 duties" reassigns (DOC-12, DOC-S99 and each multi-stage owner named there, per W03-D74), the `State` and `Closure` cells of the rows this package closes, and its frontmatter `version` and `updated`; in `docs/03.specs/work-residue-ledger.json`, the matching `owner` and `resume_condition` edits and the deletion of terminal entries in the closing commit; this package, the Stage 03 README entry and reviewed `.secrets.baseline` entries.

### Non-goals

- Not in this package: any code, schema, registry, template, form, profile or validator change (a defect that the final-tree read finds in the README or Policy heading-list consumers stops this package; see W03-D74 answer 3); a rewrite of any recorded Task row, evidence row, decision, handoff or cell, which REQ:684, `docs/03.specs/AGENTS.md` rule 4 and ADR-0060 Decision 1 forbid (corrections are appended), except the live-table cells the user authorized in W03-D74 (the live table is entry-authoritative, ADR-0060 Decision 2; only the live row's `Owner` and `Resume condition` change and the legacy rows stay untouched); the classification of obligations that other stages own; W04 to W11 work and any statement that starts or authorizes W04; the cross-repository adoption of COMMON-DOC-FORM-1 (W11); the Q-07 preparation (owned by the Q-07 preparation package, W03-D75) and Q-07 renumbering itself (REQ:141, REQ:918: this task's completion condition does not include Q07 execution); copies of the package reports into `docs/90.references/` or `docs/98.archive/` (REQ:125); tags, releases, hosted CI.
- No push, PR or merge without the user's approval. The report claims no acceptance: stage acceptance is the user's decision on the criteria of this package, recorded as a user answer with its date.
- Open question: none. This Spec stays `draft` until its approval receipt exists.

#### Decisions (W03-D74, W03-D75)

On 2026-11-14 the user decided the three questions this package raised; the decision rows W03-D74 and W03-D75 are recorded in the SPEC-0161 Task by an earlier commit (the next change to that Task, expected to be the SPEC-0195 package commit), not by this package's commit; this package appends no decision row. Open question: none.

1. **Reassigning a live residue row.** Answer "Edit Owner/Resume in place (Recommended)": DOC-12 (to after W11, owner Q07) and DOC-S99 (to W05) stay open under a new owner and resume condition, and `Owner` and `Resume condition` are edited in place in the live row and the ledger entry together, with a PASS EVD row recording each correction. The live table is entry-authoritative (ADR-0060 Decision 2); only the live row's `Owner` and `Resume condition` change, and the legacy rows stay untouched. Closing as terminal with a successor entry is refused: it would show DOC-12 as done and REQ:913 forbids hiding a live requirement. The same edit applies to the multi-stage owners named under D72 duties, one correction row each.
2. **Where the report lives.** Answer "SPEC-0161 Task tables (Recommended)": the report is appended tables under the SPEC-0161 Task (REQ:78, REQ:922; Stage 90 and 98 excluded by REQ:125).
3. **A defect found while closing W03-H10.** Answer "Stop, fix package first (Recommended)": if the final-tree read shows a README or Policy heading-list consumer still wrong, this package stops, W03-H10 and W03-H20 stay open under W03 (W03-H24 makes W03-H10 a precondition of W04), and a small fix package lands first; this package then resumes. Closing on a read that shows a defect is refused.

**W03-D75.** The user amended W03-D30 to the requirement (REQ:141, REQ:672, REQ:823): a separate W03 package, landing before this closing report, prepares the Q-07 transition (a survey of the ID, reference, allocator and consumer set, an isolated rehearsal in scratch, and the confirmation or completion of the limited non-reuse migration with SPEC-0180). No real number change happens before W11. This package therefore reports DOC-12 as: preparation done by that package ("the Q-07 preparation package (W03-D75)"); real transition owned by Q07 after W11. No GAP is hidden: this package does not land until the Q-07 preparation package (SPEC-0212) is merged; the DOC-12 row cites its merged result.

## Behavior Contract

### Normal Behavior

Contracts:

#### Report content

The report is appended to the SPEC-0161 Task (W03-D74 answer 2) as plain tables and one overview paragraph, under the evidence section as the Task form of SPEC-0203 leaves it; this package reads that shape at implementation and assumes no heading. A table never copies a decision, registry value or ledger cell as a second owner: it cites the owner by ID, `commit:path` (plain text, never a link, once a package Task has left the tree) or evidence row. Each required element and its source:

| Element | Content | Source |
| --- | --- | --- |
| Execution boundary | `WORKSPACE_ROOT`, `PACKAGE_ROOT` and its edition, selected scope, HEAD and index at the base, the existing changes protected, and the read denominator with the states DISCOVERED, READ, SEMANTICALLY_REVIEWED, PARTIAL, EXCLUDED and BLOCKED, each with its exclusion reasons | REQ:832, REQ:53 |
| W03 outcome per item | One row per item of the requirement: DOC-01 to DOC-12 (REQ:571 to REQ:672), SUP-11 (REQ:682), the SemVer change contract (REQ:846 to REQ:904) and the workflow items 1 to 8 (REQ:169 to REQ:176). Columns: source ID and line, meaning and condition, selected, actual files and consumers, action (KEEP, ADD, CHANGE, MERGE, REMOVE, DEFER), evidence scope and edition, acceptance state, open owner, exit condition (REQ:97), plus the observation class PASS, GAP, CONFLICT, BLOCKED, N/A or UNVERIFIED (REQ:67). The REQ:833 cells are supplied as follows: the external basis and test by evidence ID; the authority by the `Approval and Safety Boundaries` and `Criterion Acceptance` cells of the Task that did the work (cited by frozen `commit:path`); the recovery by that Task's rollback line or the Git revert named there. The REQ:37 columns "workspace adopted edition" and "migration and compatibility transition" point to the SPEC-0209 `Common Form Adoption Facts` rows (H19) and the registry `migration` record, which own them; the report states no adoption of its own. DOC-12 reads "preparation done by the Q-07 preparation package (W03-D75); current number space kept; real transition owned by Q07 after W11" | REQ:833, REQ:97, REQ:67, REQ:672 |
| Modification result | The changed files, their actual consumers, generated-artifact consistency (the generator check of SPEC-0192), the work retained as KEEP_VERIFIED, and the code and document diff, stated as pointers to the Git diffs of the W03 packages and to the `Writer Delegation` table of SPEC-0209, with no file list retyped | REQ:834, REQ:129 |
| Decision table | Every W03-D number with the package or evidence that applied it and the owner of any part still open, by ID only | W03-H20 row |
| Key, section and table migration table | The 14 minimal columns `profile, document_type, current_contract, target_contract, field_or_section, current_shape, target_shape, meaning_preserved, consumer_path, migration_action, negative_case, rollback, owner, approval_ref`, one row per profile and role form (the grain of REQ:759 is the profile; its field and section rows are carried by the registry `migration` record that the row points to, so no row is repeated per field), each cell a pointer to the registry `migration` record, the recovery proof in the REQ-0003 Archived Lineage, the regression test and the acceptance evidence, so the registry stays the one owner | REQ:759, REQ:228, REQ:170, W03-H20 row |
| Verification results | For the final candidate: command, tool edition, environment, exit, original result, `Resolves` and the reason of any run not made; normal, violation and regression coverage by area (the cases listed at REQ:189) citing the package tests | REQ:835, REQ:189 |
| Acceptance and unfinished work | Approval, acceptance, merge and operation, each with its own basis; every unfinished requirement with owner, next action and resume condition; and the whole of REQ:838: a report with an approved modification still pending is not complete; a closure in which every item is KEEP and no difference exists states the basis of that no-change result; a blocked, unread or NOT_SELECTED item (REQ:67) is never recorded complete or N/A without a real basis; whether closing this Task closes the whole package is a separate judgment, which the report answers as no (W04 to W11 remain); structure-check success is not product completion | REQ:836, REQ:838, REQ:67, REQ:69, REQ:129 |
| Carried obligation dispositions | OPEN-Q03 and WP-10, 11, 12, 13, 17, 18, 47 and 52, each KEEP, DELTA, BLOCKED or RETIRED_ALIAS against the current Task, later `Resolves` and acceptance. OPEN-Q03 closes only with the exact approved contract, the conditional extensions, consumer migration and drift, generation and validation evidence, else it stays `PARTIAL` with an owner (a local adoption fact is not joint adoption; W03-H09 and W03-H32 stay with W11) | REQ:793 to REQ:804, REQ:808 |
| Audit identifiers | The disposition of OPEN-01 to OPEN-14 (REMAINING-14, REQ:808) and of the seven follow-up observations of V13_4-REMAINING-7 (REQ:806; REQ:153), each judged on later evidence as its own observation: OPEN-03 remainders stay individual and are not passed to OPEN-01, and the real unfinished parts of OPEN-07 (full content review), OPEN-08 and OPEN-10 (live) and OPEN-13 (required checks) are not exempted as historical IDs; a row read only in a package list is not recorded as semantically reviewed | REQ:808, REQ:806, REQ:153 |
| Old-obligation classification | Every live W03 obligation as KEEP_VALID, REVISE, SUPERSEDE, CANCEL_OBSOLETE or REMOVE_AFTER_TRANSFER, citing the classification table of SPEC-0213 (W03-D77, W03-D81) and the status rows of the SPEC-0209 `Disposition Input` table, and classifying only what changed after them; a cancelled requirement is never recorded as PASS; the dispositions of W03-H01 and W03-H06 cite the SPEC-0209 H31 correction EVD row, and the report does not restate them; the completion test of REQ:916 is run and its result recorded (see Final check) | REQ:906 to REQ:916 |
| Exit exceptions | The accepted-ADR exception (W03-D02, with the bound W03-D52 as amended by W03-D69; the accepted and `layer`-carrying ADR counts read from the tree), the `unverified` WGOV-CORE approval facts (W03-D05, SPEC-0209), the local-versus-joint adoption limit, the conditional extensions that REQ:37 permits with condition, owner, verification, review and removal, and every other exception still in force | W03-H20 row, REQ:37 |
| W04 entry statement | See below | REQ:16, REQ:135, REQ:137, REQ:141 |

#### Report table shape

`scripts/validate-work-residue-ledger.py` treats a Task table under a heading that contains `Handoff` or `Conflicts`, or one whose first-column cell fully matches `W[0-9]{2}-H[0-9]{2}`, as a residue table, and refuses it as `RESIDUE-MARKDOWN-ONLY` unless it is the live table or registered historical. The appended report tables therefore use no heading that contains `Handoff` or `Conflicts`, and none leads with an H-ID column (a table that must list H IDs puts a descriptive column first and the H ID in a later column). The gate runs after each append, not only at the end.

#### D72 duties

Each is performed after reading the final tree (every consumer file named is read in full, not by search), and each correction is an appended PASS EVD row in the SPEC-0161 Task; no recorded cell is rewritten.

- **W03-H10, README and Policy parts.** The Plan part closes with SPEC-0200. Read `scripts/document_contracts.py` README navigation, the README form profile and the Policy twin rule in the final tree. If both consumers handle a role that has a form (and a Policy source profile with more than one tabled twin merges or is refused), close the row with a PASS row that names the file, line and test read. If not, W03-D74 answer 3 applies: stop, W03-H10 and W03-H20 stay open, a small fix package lands first.
- **W03-H34 and W03-H35.** Re-read the registry and schema set and the template set (the 2 partial files; the 18 partial and 19 listed-only templates of the original survey, recounted) and record the denominator with the states of REQ:53. A file read in full is READ; it is SEMANTICALLY_REVIEWED only where a recorded review exists. A residue that cannot be closed (a file not read, or a read that finds a gap) is handed to a named owner, not closed.
- **DOC-12.** Reassign to owner Q07, resume condition "after W11 and every applicable docs task, in the separate Q07 task" (REQ:141, REQ:672, REQ:918; W03-D75, which amends W03-D30; W03-D17); `artifact_id` and current numbering are unchanged (REQ:823). The Q-07 preparation package (W03-D75) must have merged first; the closing reads its result and cites it. A correction EVD row records that the legacy rows reading "W03 (last)" are superseded, not edited.
- **DOC-S99.** Reassign to owner W05, resume condition "when W05 moves the hard-coded headings of tests (OPEN-09)"; the tests and validators are W05's (REQ:160, REQ:896). The correction EVD row records the same supersession of the legacy "W03 (`docs/99.templates/`); W05 consumes".
- **Multi-stage owners.** Multi-stage entries are edited, not assumed done. Each of the following gets one correction EVD row with its own basis, and `W03` is dropped from the live-row and entry owner only where the W03 part is evidenced closed in the final tree: OPEN-07 (owner "W03, W05, W06, W07, W10 by file set"; the W03 part is the file-set read of W03-H34 and W03-H35, and REQ:153 does not exempt OPEN-07), OPEN-06 ("W01, W03 or W07"), GOV-04 ("W01 policy, W03 registry"), W03-H15 and W03-H29 (each "W03 with W05"; these normally close with SPEC-0196 and SPEC-0206, in which case the entry is already gone and only a read is recorded). An entry whose W03 part is not evidenced closed keeps `W03` and the final check shows it. Any other entry whose owner names `W03` beside another stage is handled the same way, found by the filter of the Final check.
- **R45-10 and DOC-11.** No named package closes them (W03-D70 ties DOC-11 to the closing of W03-H13 and W03-H15 and names no package that closes it; R45-10 is named by no decision; SPEC-0196 cites R45-10 only as rationale), so they are ADDED to the W03-D72 duties, whose user-confirmed list is the W03-H10 parts, W03-H34, W03-H35, DOC-12 and DOC-S99. The user confirms the addition in this package's approval question, and the answer is recorded in the Task Inputs, not by a new decision row. Once W03-H13 and W03-H15 are terminal, close each by a PASS read of the final tree (every real template has its TemplateDefinition) with its own PASS EVD row, as for W03-H10, W03-H34 and W03-H35. If either condition is not met, stop as W03-D74 answer 3 does: both rows stay open under W03 and a small package lands first.
- **Order.** The reassignments and the H10, H34 and H35 closure rows come first; the report is written from the resulting ledger; W03-H20 closes last, in the closing commit.

#### Final check

Run twice. **Before the closing commit** (after the implementation commit): list the open entries with `python3 scripts/work-residue-ledger.py --root . --state open` and filter the full output on the owner column with `\bW03\b` (the script's `--owner` option is an exact match and would miss multi-stage owners such as `W03 with W05`). The target before the closing commit is that only W03-H20 carries W03; any other must be shown handed to a later stage with the new owner recorded, never left owned by W03. Every open entry owned by a later stage is listed in the report with owner, resume condition and next action, built from the ledger at implementation, so no hand-typed count exists. **After the closing commit:** the same filter shows no entry that carries `W03` in its owner, `python3 scripts/validate-work-residue-ledger.py --root .` passes, and each terminal entry's closure names a PASS EVD row of the SPEC-0161 Task and has been deleted. The REQ:916 test is run as: every live obligation has exactly one current owner (the report table, derived from the ledger); no active link, check input or Task status reference targets a package Task that has left the tree (strict link and owner validator plus a search of the SPEC-0161 Task for non-frozen references); a requirement cancelled by the user is not recorded PASS; no real earlier failure disappears without equivalent later evidence.

#### W04 entry statement

The statement is written from REQ:16 (W04 is forbidden before this remainder closes), REQ:135 (a purpose with unfinished W03 does not skip to W04; running one task does not authorize the others) and REQ:137 (W11 is the completion gate; handing work to another stage does not complete the whole). It says: W04 may start for this workspace (hy-home.k8s; REQ:135 keeps the Project-Template purpose at W03) when every item of REQ:16 is accepted and merged or handed with a named owner (SPEC-0185 to SPEC-0189, the local forms, ledger, policy and generator packages, phase 3, and closing H19, H20, H21 and H31), no approved modification is pending (REQ:838), this package has exited with W03-H20 terminal, the final check shows no entry carrying `W03`, W03-H10 is closed (W03-H24), and the user selects W04; it lists the entries W04 inherits (those whose owner names W04, read from the ledger); it states that no W05 to W11 work is started and that entries assigned to them are pointers only, that Q-07 stays after W11, and that the statement starts nothing and approves nothing. W04 is the user's selection (REQ:135), not an automatic next step.

#### Ledger closure

W03-H20 closes with a PASS evidence row appended in the closing commit after the user's acceptance, naming this package's Task by its frozen `commit:path` as plain text; the live row's `State` and `Closure` cells change in place and the terminal entry is deleted in the same change, as SPEC-0209 does, so the gate sees no half state. W03-H10, W03-H34, W03-H35, R45-10 and DOC-11 close the same way once their PASS rows exist.

Data modeling and storage strategy:

Appended tables in one Task and edits to the `owner` and `resume_condition` of the reassigned ledger entries, plus deletion of terminal ones. No ledger key, status or approval value is copied into the report, and no registry value is copied as a second owner.

Interfaces and data structures:

None beyond the ledger entry shape (`id`, `kind`, `state`, `owner`, `resume_condition`, `source`, `closure`) and the `Residue Handoff` table columns (`ID`, `Residue`, `State`, `Owner`, `Resume condition`, `Closure`), unchanged.

### Failure and Edge Cases

Edge cases and error handling:

- A closure row that names a deleted package Task names its frozen `commit:path` as plain text and never as a link.
- If the SPEC-0161 Task has moved to the Task form of SPEC-0203, appended tables follow its sections and no recorded cell moves.
- A count that differs from a figure in this Spec is recorded as observed; the Spec figure is not edited.
- An entry whose owner names several stages keeps the later stages; only `W03` is removed, and only when its W03 part is closed.
- A decision of another package that is not yet on `main` (W03-D70 to W03-D73, recorded by the SPEC-0194 implementation commit) is read from the merged Task; W03-D74 and W03-D75 are fixed by the user and recorded in the SPEC-0161 Task by an earlier commit; this package appends no decision row.
- `unverified` approval facts stay `unverified`; the report claims no approval it has no record for.

Failure modes and fallback or human escalation:

If any part needs a recorded row rewritten, a ledger entry for an unverified fact, a code or registry change, a W03-H10 defect fix (W03-D74 answer 3: stop, fix package first), or a ledger gate failure that is not a defect of this package's own edits, the author stops and asks the user, except where W03-D74 already answers. After two failed attempts with no new information the author stops and reports a repository defect. If an entry owned by W03 cannot be closed or handed to a named later-stage owner, W03 stays open for it and the report says so; the closing never weakens the final check. Rollback is the revert of the SPEC-0161 Task commit and of the ledger edits; the appended Task lines and the ledger data return to their base.

## Acceptance Criteria

### Criteria

| Criterion ID | Expected Result |
| --- | --- |
| VAL-W03REPORT-001 | The report tables of Contracts exist in the SPEC-0161 Task with the elements and sources named, built from the final tree; every item of the requirement has an outcome row (12 DOC items, SUP-11, the SemVer contract and 8 workflow items, counted at implementation); OPEN-Q03 and the 8 WP rows have a disposition; the modification result and the audit-identifier dispositions are stated; the report tables are not read as residue tables by the gate; the old-obligation classification and the exit exceptions are stated; no recorded cell is rewritten. |
| VAL-W03REPORT-002 | The D72 duties are done: W03-H10 (README and Policy), W03-H34, W03-H35, R45-10 and DOC-11 are closed on PASS reads (R45-10 and DOC-11 only once W03-H13 and W03-H15 are terminal, and only as added to the W03-D72 duties by the user's confirmation recorded in the Task Inputs) or handed to a named owner; DOC-12 and DOC-S99 are reassigned in place with a correction EVD row each, and each multi-stage owner is edited with its own basis or keeps W03 visibly; the ledger and the live rows agree under the gate. |
| VAL-W03REPORT-003 | The Final check passes before and after the closing commit: no entry carries `W03` in its owner after it, each open entry has a later-stage owner shown in the report, the REQ:916 test result is recorded, the REQ:838 statements and the W04 entry statement are present, and exact-index QA and the commit hooks pass. |

### Evidence Requirements

- Before and after, record the four strict document validators (`scripts/validate-markdown-profiles.py`, `scripts/validate-links-and-owners.py`, `scripts/validate-document-lifecycle.py` and `scripts/validate-document-contract-registry.py`, each `--mode strict` where it takes the option); diagnostics after must equal those before.
- `python3 scripts/validate-work-residue-ledger.py --root .` before, after each appended report table (no table may be read as an unregistered residue table) and after each ledger edit; `python3 scripts/work-residue-ledger.py --root . --state open` for the Final check.
- `python3 scripts/run-contract-tests.py --root . --suite document` and `--suite document-lifecycle`.
- `git diff` of the SPEC-0161 Task shows added lines only, apart from the `State` and `Closure` cells of the closed rows, live-table `Owner` and `Resume condition` cells of the reassigned rows (W03-D74) and the frontmatter `version` and `updated`.
- `markdownlint` over the edited Markdown; `python3 scripts/qa.py staged` and the commit hooks on the exact index.

## References

### Normative and Evidence

No separate reference list is kept; the requirement, architecture and decision owners this Spec relies on are linked in [Lifecycle Traceability](#lifecycle-traceability) below.

### Historical and Navigation

No separate reference list is kept; this Spec holds no historical or navigation links beyond the [Plan](plan.md) and the Task that its Overview names.

### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0019](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-W03REPORT-001 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Append-only diff of the SPEC-0161 Task; the report tables read against the ledger and the final tree. |
| [REQ-0003-FR-0019](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-W03REPORT-002 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | The `work-residue-ledger` gate; the PASS reads and correction rows. |
| [REQ-0003-FR-0022](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-W03REPORT-003 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | The Final check listing; the strict validators over the tree; no progress ledger added. |
