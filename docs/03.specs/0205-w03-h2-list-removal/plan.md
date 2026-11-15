---
title: "W03 H2-List Model Removal Plan"
version: "2.0.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-15"
artifact_id: "SPEC-0205-PLAN-0001"
parent_ids: ["SPEC-0205"]
---

# W03 H2-List Model Removal Implementation Plan

## Overview

### Goal and Boundary

Show that the form tree and the retained ADR form protect every document the list checks protected, move the four readers of the heading contract and the accessor function of the old-shape Plan branch onto one accessor, record the replay of earlier commits, then remove the `sections` key from every profile and from the current schema, raise the Registry Schema Version by one MAJOR step in the registry, the schema, `REGISTRY_MAJOR`, `READABLE_REGISTRY_MAJORS` and the guard's `DOC_REGISTRY_MAJOR`, keep for `registry_at` a history reading that builds the lists of earlier registries, add the rule for profiles without a form, retire the helpers, fixtures and tests that lose their last consumer, and update the policy texts. [Task 0001](tasks/tsk-0001-w03-h2-list-removal.md) owns execution and evidence.

Goals and in-scope:

- Protection first: the transfer table, the accessor, the four readers and the old-shape Plan branch as a fifth consumer, the renamed field, the recorded replays of earlier commits, and regression tests that stay.
- Removal and version: the registry key, the schema property, the guard entry, `_form_headings`, the two registry rules, the three README identifiers, `REGISTRY_FORM_REQUIRED`, the MAJOR step in the registry, the schema `const`, `REGISTRY_MAJOR`, `READABLE_REGISTRY_MAJORS` and the guard's `DOC_REGISTRY_MAJOR`, and the history reading of earlier registries.
- Texts and records: the two policy texts; the W03-D63 row, the handoff closures and the ledger entries; the bump level and its reason in the Task.
- Cleanup: helpers, fixtures and tests without a consumer.

Non-goals and out-of-scope:

- The SemVer form of the version, its mapping function, its reader rule and its bump rule, which are SPEC-0207's; any ADR; forms, sections, extensions and governed document bodies; the retained ADR form and its checks; a form for `provider-native` or a profile without a role; the old-shape reader branches of SPEC-0200 and SPEC-0203; hook registration, permissions and provider adapters; the W03 closing report; Q-07.

#### Global Constraints

This work order, a draft until its review and approval receipts exist, follows the [Spec](spec.md) and inherits all of its boundaries. It adds five constraints: every heading rule that reaches a current document stays active in every commit of this package, so each reader takes its H2 from the form before the lists and the derived lists go; the Registry Schema Version rises by exactly one MAJOR step under the bump rule of SPEC-0207, with MINOR and PATCH at 0, and the registry, the schema `const`, `REGISTRY_MAJOR`, `READABLE_REGISTRY_MAJORS` and the guard's `DOC_REGISTRY_MAJOR` change in one commit, with no commit that holds a write guard for two MAJOR numbers; the history reading of earlier registries and the old-shape reader branches serve the replay of earlier commits only, which line 778 of the W03 prompt keeps until the transition, so every generation in `READABLE_REGISTRY_MAJORS` stays readable, and no current input is read in an old shape; a check is retired only in the order transfer, then caller and registration, then helper, fixture and test; and the diagnostics of the four strict document validators over the tree are equal before and after. The design choices follow W03-D63, W03-D65 and W03-D66 as the Spec states them.

### Assumptions

A read of `main` at `81096a83` found 85 profiles and 21 forms. Each profile carries `sections` with `required`, `optional` and `forbidden`; 12 are non-empty (the profile and template twin of the six SDLC roles) and 73 are empty. `scripts/document_authority.py` requires the key in `PROFILE_KEYS`, and the schema requires it in the profile definition. `_profile_from_mapping` in `scripts/document_contracts.py` builds a heading contract from the lists, or from the form through `_form_headings` when the role has one, so list readers keep working on form profiles. Those readers are the lifecycle evidence reader of `scripts/validate-links-and-owners.py`, `scripts/validation/repository/form_contracts.py`, `scripts/validation/repository/quality.py`, `scripts/validate-document-contract-registry.py`, the Plan guard of `scripts/validate-document-lifecycle.py` that SPEC-0200 re-points, and the list branch of the body check in `scripts/validate-markdown-profiles.py`, which a form profile reaches only through a retained form. Three identifiers of that branch, `README_H2_REQUIRED`, `README_H2_DUPLICATE` and `README_H2_UNSUPPORTED`, are named by no test and no text. At that commit `schema_version` is the integer 10, pinned by the schema constant, by the strict check of `scripts/document_contracts.py`, by `registry_at`, which reads a commit's registry by its own reading only for that value and returns the current registry for any other, and by `scripts/provider_write_guard.py`, which fails closed with `HOOK-DOC-REGISTRY` for any other. SPEC-0207 changes all of that before this package, right after SPEC-0191 (W03-D66): the value becomes a SemVer string at `11.0.0`, `registry_schema_version` is the one function that reads it and maps an integer of history to `N.0.0`, `REGISTRY_MAJOR` and `READABLE_REGISTRY_MAJORS` in `scripts/document_authority.py` hold the MAJOR the readers implement and the MAJOR numbers the history reader reads, the guard holds its standard-library copy `DOC_REGISTRY_MAJOR`, the loader and the guard refuse any other MAJOR, `registry_at` reads every generation in `READABLE_REGISTRY_MAJORS` with that commit's own typed reading, the tests that pin the version read the constants, an amending ADR replaces the sentence of ADR-0059 Decision 1 that fixed the value at 10, and each later registry change applies the bump rule of lines 877 to 882 of the W03 prompt, under which a removed required key is MAJOR. Line 778 keeps the cumulative-history replay until the transition. Rule 3 of `scripts/AGENTS.md` keeps no compatibility branch for an older format, generation or pinned historical commit; the Spec states why a replay-only reader is not such a branch. 15 profiles have no form: six `provider-native` and nine without a role, all native, non-target or a `provider-native` template, and none carries a list. Six test modules build a profile list or read the heading contract; no fixture file and no template holds a list.

## Dependencies

### Prerequisites

The prerequisites of each work unit are in the Dependencies column of the [Work Breakdown](#work-breakdown) table.

### Dependency Order

The order of the work units follows the Dependencies column of the [Work Breakdown](#work-breakdown) table.

## Implementation Strategy

### Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-LISTREMOVAL-002](spec.md#criteria) | Transfer first: the table that maps each list rule to the tree rule or retained form that covers the same documents; the accessor; the four readers and the accessor function of the old-shape Plan branch on it; the renamed field; the recorded replays of a commit of the retired MAJOR and of a commit that holds the integer; the tests that show each reader and each role still refused. | Approved Spec and Plan; SPEC-0191, SPEC-0207 and SPEC-0192 to SPEC-0204 merged in that order, then this package; rebase on `main` and renumber appended rows before each commit. | [Task 0001](tasks/tsk-0001-w03-h2-list-removal.md) | The mutation run per role; the reader tests failing first, then passing; the replay records; the cumulative-history suite. |
| WORK-002 | [VAL-LISTREMOVAL-001](spec.md#criteria) | Callers and registration: the `sections` key of every profile, the schema property, the guard entry, `_form_headings`, the two registry rules, the three README identifiers, `REGISTRY_FORM_REQUIRED`; the MAJOR step of `schema_version` in the registry, the schema `const`, `REGISTRY_MAJOR`, `READABLE_REGISTRY_MAJORS` and the guard's `DOC_REGISTRY_MAJOR`, with the history reading of earlier registries in `registry_at`. | WORK-001; SPEC-0207 merged. | [Task 0001](tasks/tsk-0001-w03-h2-list-removal.md) | Failing tests first, then passing; the strict registry validator; the derived tests of SPEC-0207, unedited; the mutation run and the replays again. |
| WORK-003 | [VAL-LISTREMOVAL-002](spec.md#criteria) | Helpers, fixtures and tests that lost their last consumer, each after a recorded search; the two policy texts; the SPEC-0161 Task rows and ledger entries; regression and exact-index QA. | WORK-002. | [Task 0001](tasks/tsk-0001-w03-h2-list-removal.md) | The consumer search; suites, quality gate, markdownlint, ruff, staged QA and hooks. |

### Change and Rollback

The rollback, where a risk states one, is under [Risks and Mitigations](#risks-and-mitigations).

## Verification Plan

### Verification Matrix

- Run the mutation baseline: in a temporary copy remove one required H2 from one document of each role that has a form and from one accepted ADR, and record the rule that refuses each.
- Keep the heading rules active, in this order. First add the accessor and move the four readers, and the accessor function of the old-shape Plan branch, onto it while the derived lists still exist, with one test for each reader that fails a document or template lacking a required H2 of its form. Then rename the field that holds a registry's own lists, so a reader left behind fails loudly, and run the suites. Only then remove `_form_headings` and the registry key.
- Record the bump as evidence: the level MAJOR, its reason under line 877 of the W03 prompt, and the value before and after with MINOR and PATCH at 0.
- Show the refusals of the current input: a registry of the new MAJOR that carries `sections` is refused by the schema and by the strict check, and a registry of the retired MAJOR at the current path is refused.
- Record the retirement order in the Task: for each removed rule, function, fixture and test, the protection it had, where that protection is now, and the search that shows no consumer is left. A test that still protects a reachable rule is rewritten onto a retained form or a registry of the retired MAJOR and its assertions are compared before and after.
- Record for each of the 85 profiles that it meets `REGISTRY_FORM_REQUIRED` and by which clause, and show one document of each profile without a form keeping its fence and frontmatter diagnostics.
- Record the risk class as `high`, because the write guard is the pre-action hook program, and complete the core-diff checklist for it: no permission, trigger or hook registration changes, and the one protected behaviour that changes is the MAJOR the guard accepts. List each removed check under the removed-or-weakened item.

Completion criteria:

Both criteria need PASS evidence, no unresolved required failure and the operator's acceptance. On the final tree one document of each role with a form and one accepted ADR must be shown refused when a required H2 is removed, the replays of a commit of the retired MAJOR, of a commit that holds the integer and of a commit with an old-shape Plan and Task must equal their baselines, and the write guard must accept the new MAJOR and refuse the retired one.

### Stage Placement

- Record the four strict document validators, the count of profiles and of non-empty lists, the list of readers, the version on `main` and every place that pins its MAJOR before any change. Stop if a list is non-empty or SPEC-0207 has not merged.
- Record the replay baseline: the result of the cumulative-history check over a range that holds earlier commits, a test that replays one commit of the retired MAJOR, on a commit whose registry still lists H2 for a role where the range holds one, a test that replays one commit that still holds the integer, and a test that replays one commit of an earlier MAJOR with an old-shape Plan and an old-shape Task, in which an invalid promotion table fails `PLAN-PROMOTION`, missing shared constraints fail `PLAN-GLOBAL-CONSTRAINTS`, and an edited evidence row, a removed work row and an executable Task without an approved parent fail their `TASK-` rules.
- Raise the MAJOR in one working-tree step that leaves the write guard usable. The guard judges every structured write against the registry in the tree, so the order is: let the guard accept the retired and the new MAJOR in the working tree only; set the registry, the schema `const` and `REGISTRY_MAJOR` to the new MAJOR, append it to `READABLE_REGISTRY_MAJORS` and keep the history reading for the earlier numbers; set `DOC_REGISTRY_MAJOR` to the new MAJOR alone; and commit once. The Task records the three steps and that no commit holds the guard for two. The derived tests of SPEC-0207 then pass unedited: the guard accepts the new MAJOR and refuses the retired one, and its copy equals `REGISTRY_MAJOR`. Record the output of `git diff --cached -- scripts/provider_write_guard.py` as proof that the staged guard changes `DOC_REGISTRY_MAJOR` alone and holds one MAJOR, and route a `security-auditor` read of that diff before merge.
- Show the history side again after the change: the three replays give the recorded results, the old-shape one with every named rule still firing, `registry_at` reads every version through `registry_schema_version`, an earlier registry with the history reading and one of the new MAJOR with the current reading, the commit that changes the version passes the staged check with its base of the retired MAJOR, and the cumulative-history suite is unchanged.
- Before each commit, rebase on `main`, count again and renumber the rows this package appends to the SPEC-0161 Task. Commit order: the package commit with the W03-D63 row; then `.secrets.baseline` changes alone; then the implementation with the Task evidence. Run the staged lifecycle check before each commit and `graphify update .` after the code change.

## Risks

### Risks and Mitigations

Risks use the risk-report scale (likelihood Likely, Possible or Unlikely; impact Severe, Moderate or Minor), rated from the pre-approval read.

- **A heading reader keeps reading a list that is now empty.** Without a control this is Likely, Moderate: HIGH, because four readers take their H2 from the derived lists today and an empty list passes every document, and it would block the implementation commit. This Plan closes it: the first Global Constraint keeps every heading rule active in every commit; the readers move onto the accessor before the derived lists go; the field is renamed so a reader left behind fails instead of passing; one regression test for each reader stays in the suite; and the mutation run must refuse one document of each role by the same rule before and after. With those controls the residual is Unlikely, Moderate: LOW, monitor. Owner: W05 code. Review cue: the mutation run and the reader tests. Signal that raises it: a document with a removed required H2 that passes. Rollback: revert the implementation commit.
- **The write guard and the registry disagree on the MAJOR.** Without a control this is Likely, Moderate: HIGH, because the guard accepts only the MAJOR in `DOC_REGISTRY_MAJOR` and fails closed, so a registry at the new MAJOR with the old guard, or the reverse, refuses every structured write in that tree, and it would block the implementation commit. This Plan closes it: the second Global Constraint moves the registry, the schema `const`, `REGISTRY_MAJOR`, `READABLE_REGISTRY_MAJORS` and `DOC_REGISTRY_MAJOR` in one commit; the working-tree order keeps the guard usable while the registry changes; the committed guard accepts the new MAJOR only; the derived tests of SPEC-0207, unedited, show the guard accepting it and refusing the retired one and `DOC_REGISTRY_MAJOR` equal to `REGISTRY_MAJOR`; and the change is reviewed as risk class `high`. With those controls the residual is Unlikely, Moderate: LOW, monitor. Owner: W05 code. Review cue: the recorded three steps and the derived tests. Signal that raises it: a `HOOK-DOC-REGISTRY` refusal on a tree whose registry and guard are both committed. Rollback: revert the implementation commit, which restores both.
- **The replay of an earlier commit changes its result.** Without a control this is Likely, Moderate: HIGH, because the current typed reading builds no heading list once the key is gone, so an earlier commit read with it would be judged without the lists its registry carried, and it would block the implementation commit. This Plan closes it: the history reading of earlier registries is kept in the same commit and no number leaves `READABLE_REGISTRY_MAJORS`; the replay of such a commit, of a commit that holds the integer and of a commit with an old-shape Plan and Task is recorded before the change and compared after it; the old-shape Plan branch reads its list through the accessor; and the cumulative-history suite runs unchanged. With those controls the residual is Unlikely, Moderate: LOW, monitor. Owner: W05 code. Review cue: the replay records. Signal that raises it: a diagnostic on a past commit that the baseline did not have. Rollback: revert the implementation commit.
- **SPEC-0207 merges differently from its draft.** Possible, Minor: LOW, monitor. Owner: the author of SPEC-0207. This package waits for it and follows what merged: its function, its constants and its reader rule. Review cue: the readers recorded in the Task after the rebase. Signal that raises it: a place that pins the version and that neither package names. Rollback: none; the author stops and asks the user.
- **A branch cut before this package meets the new MAJOR.** Likely, Minor: MEDIUM, monitor. Owner: each branch's author. Its registry and guard are both at the retired MAJOR until it rebases and both at the new one afterwards; a half-resolved rebase can leave them apart. Review cue: the first rebase after this package merges. Signal that raises it: `HOOK-DOC-REGISTRY` during a rebase. Rollback: finish or abort the rebase.
- **A test is weakened while it is rewritten or removed.** Possible, Moderate: MEDIUM, monitor. Owner: W05 code. Six modules build lists, and the version tests of SPEC-0207 read the constants and are not edited; a test is removed only when the rule it protected has no caller, and a rewritten test keeps its assertions. Review cue: the retirement record and the test diff. Signal that raises it: fewer assertions on a rule that is still reachable. Rollback: restore the test.
- **The retained ADR lists lose their checks.** Unlikely, Moderate: LOW, monitor. Owner: W05 code. The list branch stays for a retained form and a test removes a retained H2 from an accepted ADR. Review cue: that test and the mutation run. Signal that raises it: an accepted ADR in the range that passes without a retained H2. Rollback: revert the implementation commit.
- **An earlier package changes the registry, the readers or the MAJOR first.** Likely, Minor: MEDIUM, monitor. Owner: W03 author. SPEC-0207 and every package from SPEC-0191 to SPEC-0204 merge before this one, five of them bind an SDLC form, and any of them may raise the version. Review cue: the counts and the version recorded after the rebase. Signal that raises it: a non-empty list at the start, a MAJOR other than the one recorded, or a merge conflict. Rollback: rebase the package.

### Escalation

Escalation follows [Failure and Edge Cases](spec.md#failure-and-edge-cases) of the Spec.

## Promotion Map

### Durable Meaning

The durable contracts are the first column of the table under Owner and Receipt.

### Owner and Receipt

| Promotion ID | Target Owner | Acceptance | Evidence |
| --- | --- | --- | --- |
| A profile's headings come from its role's form; no profile carries H2 lists; which profiles may have no form | [Document authoring policy](../../../.agents/governance/document-authoring.md) | The document authoring policy states that a profile's headings come from its role's form, that no profile carries H2 lists and which profiles may have no form, and the schema, `REGISTRY_FORM_REQUIRED` and the strict registry rule enforce it, with PASS evidence for VAL-LISTREMOVAL-002 | Forms paragraph; the profile definition in `docs/99.templates/contracts/document-profile.schema.json`, `REGISTRY_FORM_REQUIRED` and the strict registry rule |
