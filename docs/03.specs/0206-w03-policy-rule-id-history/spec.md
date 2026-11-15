---
title: "W03 Policy Rule ID History"
version: "2.0.0"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-11-15"
artifact_id: "SPEC-0206"
---

# W03 Policy Rule ID History Technical Specification (Spec)

## Overview

### Intent

This approved change contract is Policy package 5, the last package of handoff W03-H29 of the W03 stage of the external v14.7 execution package, recorded in the [SPEC-0161 Task](../0161-w00-v14-7-delta-intake/tasks/tsk-0001-w00-v14-7-delta-intake.md). The user decided that a rule ID `<CODE>-R<NNN>` is issued once, never renumbered and never reused, with a retired row kept in the Rules table (W03-D42, W03-D44), and that reuse is refused inside a document first and across history in a later package. Under W03-D65, which the user decided on 2026-11-14 from the W03 task of the external package (REQ, by line), the Rules table is conditional content of the Policy role whose condition is that the policy states normative rules (REQ:310, REQ:742), and the `Status` of a row is a registered conditional extension that no-reuse retirement needs (REQ:37, REQ:143). SPEC-0194 built the in-document part: rows ascend from `R001` without a gap or a duplicate. It left to this package the one case a single document cannot show, the deletion of the last row followed by a new rule under the same number, and reuse across history in general. Its review also left one note that the user deferred here: SPEC-0194 says that a code may change only while its record is `pending`, and nothing enforces it. SPEC-0199, SPEC-0201, SPEC-0202 and SPEC-0204 then adopt the fifteen policies, and SPEC-0204 retires the adoption gate and removes `state`, so that no record is `pending` any more and the deferred note reads: a registered code never changes. This package adds the history rules that hold both: a rule ID never leaves the Rules tables, a retired rule ID is never issued again, and a registered code never changes and is never given to another policy. These rules hold until a user-approved new baseline under the Q-07 contract, because the W03 task (line 143) keeps no-reuse and reservation in force until the transition; this package does not implement that transition. A read of `main` at `81096a83` found that the document lifecycle check already keeps identities across Git in this way: it compares a base snapshot with the proposal, keeps every Task work ID across the two (`TASK-ITEM-DELETE`), refuses a reused artifact identity (`LIFECYCLE-IDENTITY-REUSE`), and holds a reader of the registry a commit carried (`registry_at`). Five design choices were not settled by the earlier decisions. They were resolved from the W03 task of the external package, `tasks/TASK-hy-home-k8s-W03.md`, under the user's standing instruction of 2026-11-14, `선택이 필요할 경우, 요구사항을 따른다` (when a choice is needed, follow the requirements), and are recorded as W03-D64 with this package's first commit: history is read step by step in the existing lifecycle check; one audit at landing covers what came before; a retired rule never becomes active again; the code of a policy that leaves the tree moves to `reserved_codes`, which never shrinks; and the code rule reads one section of the base registry as plain JSON. The package depends on SPEC-0194 being implemented in the base and merges after SPEC-0204. With it W03-H29 closes. The [Task](tasks/tsk-0001-w03-policy-rule-id-history.md) records execution and the [Plan](plan.md) orders the work.

### Owning Requirements

[AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) owns the governance view; no component changes and no ADR body changes. The lifecycle check stays the owner of what must hold between two Git snapshots, the profile check stays the one reader of a policy body, and the registry stays the single machine owner of the codes.

## Scope

### In Scope

- In scope (writer W03, with W05 for validator code): `scripts/document_lifecycle.py` (the three history rules and the base rows in the evidence context); `scripts/validate-document-lifecycle.py` (the collection of the base Rules tables and of the base `policy_rule_ids` section); `scripts/validate-markdown-profiles.py` only to expose the Rules table reader of SPEC-0194 to the lifecycle check, so that one reader serves both; a new `tests/test_policy_rule_history.py` with its registration in the `document-lifecycle` suite of `scripts/run-contract-tests.py` and in `scripts/validation/registry.json`; the description of `reserved_codes` in `docs/99.templates/contracts/document-profile.schema.json`, which says that the list never shrinks until a user-approved new baseline under the Q-07 contract; in `docs/99.templates/registry.json` the `verification` text of the `Status` entry of `shared_contract.extensions`, which gains the reissue rule; the sentences that state the permanence of rule IDs and codes in `.agents/governance/document-authoring.md` and `docs/99.templates/README.md`, and the disposition rule of `.agents/governance/document-lifecycle.md` for a policy that leaves the tree, each new rule with the next rule ID of its policy and one Rules table row, and each edited policy's frontmatter `version` and `updated`; in the SPEC-0161 Task the appended W03-D64 row, the closure row and the refreshed state cell of W03-H29, an evidence row and the frontmatter `version` and `updated`, with the closed W03-H29 entry of the work residue ledger; this package, `docs/03.specs/README.md` and reviewed `.secrets.baseline` entries.

### Non-goals

- Not in this package: any rule ID, Rules table row or code of the fifteen policies beyond the rows the new policy sentences need; the grammar, the six document rules, the coverage floor and the registry records of SPEC-0194 as SPEC-0202 and SPEC-0204 leave them; whether an `active` rule still means what it meant, which stays a judgment of the semantic review; the artifact identity and Task work ID rules of the lifecycle check; the other lifecycle rules and base modes; a walk of old commits at every run, a recorded high-water mark and a committed audit script, which W03-D64 excludes; hosted CI, which runs no document check; the Q-07 number transition of the external package, which this package neither starts nor prepares; `_workspace/` (read-only input) and `docs/98.archive/`.
- No existing rule ID, code or rule text of a policy changes in this package; the policy sentences it adds are new rules. No push, PR or merge without the user's approval. Open question: none; W03-D64 settles the choices.

## Behavior Contract

### Normal Behavior

Contracts:

- **Rule ID permanence (W03-D42, W03-D44).** Every rule ID that a Rules table holds at the comparison base is held by a Rules table of the proposal; a missing ID is refused (`POLICY-RULE-DELETE`). Because SPEC-0194 requires each table to ascend from `R001` without a gap and to carry its document's code, an ID that cannot leave cannot be issued twice: the deletion of the last row is refused at the commit that makes it. The rule holds until a user-approved new baseline under the Q-07 contract. A renamed policy passes, because the comparison follows the IDs and not the path. The one exception is a policy that leaves the tree, below.
- **No reissue (W03-D44, W03-D64, W03-D65).** A row whose Status is `retired` at the base keeps a `retired` Status in the proposal (`POLICY-RULE-REISSUE`). `Status` is the registered conditional extension of the Rules table (REQ:37), and this rule joins the verification that its registry entry records. A retired rule never becomes `active` again until a user-approved new baseline under the Q-07 contract: a restored rule takes a new ID, and the retired row may name it as its successor, so its successor part may be corrected. The W03 task (line 143) keeps the ban on reusing past numbers in force. A row may go from `active` to `retired` at any time, as SPEC-0194 allows.
- **Code permanence (W03-D42; the note deferred from SPEC-0194).** SPEC-0194 lets a code change only while its record is `pending`, and SPEC-0204 leaves no `pending` record, so a registered code never changes until a user-approved new baseline under the Q-07 contract. Every code of the base registry is, in the proposal, the code of a record or a reserved code, and no reserved code of the base leaves the list (`POLICY-CODE-CHANGE`). A record's path may change with a rename; its code may not.
- **Reading the base registry (W03-D64).** The code rule reads only the `policy_rule_ids` section of the base registry blob, as plain JSON; a base without the section has no code rule. This keeps W03-D54, which forbids something else: parsing a historical registry as the typed registry in order to classify the base, where a key the current schema retired could fail base loading. A plain JSON read of one section builds no typed registry and classifies no document. It is needed because the W03 task (line 143) requires the reservation to be enforced, and without the base list nothing would show a reserved code removed.
- **A policy that leaves the tree (W03-D64).** When a policy document leaves its profile path, its code moves to `reserved_codes` in the same change. Only then may its rule IDs leave the tables: `POLICY-RULE-DELETE` passes a missing ID whose code the proposal reserves and no record carries. The reserved list never shrinks until a user-approved new baseline under the Q-07 contract, and SPEC-0194 already refuses a reserved code for a new policy, so the code and its IDs are never issued again. The W03 task (line 226) requires the reserved history and the stable IDs to be preserved.
- **Where the rules run (W03-D64).** History is read step by step in the existing document lifecycle check: each run compares the base snapshot with the proposal, as the Task row rules do, in every mode that has a comparison base, `staged` (the index against `HEAD`), `ci` (a ref against its merge base) and `explicit-ref`. A history that passed every step holds the invariant, and no run walks old commits. The W03 task (line 778) forbids a standing gate over historical bodies that contradicts the new contract, and rule 4 of `scripts/AGENTS.md` bounds every subprocess, file read and output, which the existing helpers of the check already do. The rules read the Rules table with the reader of the profile check, so no second reader of a policy body exists. A proposal whose Rules table is missing or malformed fails the permanence rule for every ID of the base table, as the Task row rule does for a hidden table.
- **Landing audit (W03-D64).** A rule ID retired before this package lands is a row with a `retired` Status at the base and is protected from the first compared commit. For what no check saw, one audit runs at landing: for each of the fifteen policies, every commit from its adoption to the base is read once, and the audit shows that no ID left a table, no retired ID became active again and no code changed. Its method, the commits it read and its result are recorded in the Task. A finding stops the package and goes to the user. The audit is not kept as a gate and its script is not committed, because rule 3 of `scripts/AGENTS.md` keeps no check of a finished one-time transition. The W03 task keeps no-reuse and reservation in force until the transition (line 143) and keeps recorded acceptance and current failures (lines 149 and 173), which the Task record serves.
- **Limits.** The rules are inductive and local: a commit made without the check, or a rewritten history, is not seen by a later step, and hosted CI runs no document check. They do not judge whether an `active` ID still names the same rule; that stays with the semantic review. A PASS of these rules is not a review of meaning.
- **Policy text.** The document authoring policy and the Stage 99 README state that a rule ID and a code are permanent until a user-approved new baseline under the Q-07 contract, and the document lifecycle policy states that a departing policy's code is reserved for the same span. These are adopted policies: a sentence that forms a new rule unit takes the next rule ID of its policy and one Rules table row, as the contract of SPEC-0194 requires.
- **Decision and handoff rows.** The package commit appends W03-D64 to the SPEC-0161 Task, with the standing instruction quoted, the five resolutions and the lines of the W03 task they rest on. The implementation appends the closure row of W03-H29, refreshes its state cell and closes its ledger entry: packages 1 to 5 are complete. No recorded decision row is edited.

Data modeling and storage strategy:

Nothing new is stored: the Rules tables and the registry's code records and reserved list are the record, and each comparison reads them at two snapshots. The landing audit stores nothing but its Task evidence.

Interfaces and data structures:

- `scripts/document_lifecycle.py`: `POLICY-RULE-DELETE`, `POLICY-RULE-REISSUE` and `POLICY-CODE-CHANGE` beside the Task row rules; the evidence context carries the base rule rows and the base codes.
- `scripts/validate-document-lifecycle.py`: the base Rules tables of the policy documents, and the `policy_rule_ids` section of the base registry blob read as plain JSON.
- `tests/test_policy_rule_history.py`: for each rule a passing and a refused case over real Git snapshots, as the lifecycle tests build them: the last row deleted and refused; the last row deleted and a new rule issued under its number, refused; a retired row made active, refused; a row retired, a new row appended and a policy renamed, each passing; a code changed and a reserved code removed, each refused; a policy that leaves the tree with its code reserved, passing, and without, refused; a base without the section or without a table, passing.

### Failure and Edge Cases

Edge cases and error handling:

- A base from before a policy adopted holds no Rules table, and a base from before SPEC-0194 holds no `policy_rule_ids` section; neither yields a rule.
- A base registry whose other sections carry keys the current schema retired still serves the code rule, because only the one section is read.
- A new policy has no base and is free to issue from `R001`.
- A policy whose rules have all retired keeps its Rules table, because its IDs cannot leave; the table's condition (W03-D65) decides whether a table must exist, never whether one may go.
- A rule that moves to another policy keeps its old row as `retired` with the new ID as successor; the old ID stays in its table.
- The `snapshot` mode has no comparison base and runs none of the three rules.
- A merge compared in `ci` mode is judged against its merge base, so an ID deleted on one side and kept on the other is refused when the result lacks it.
- SPEC-0194, SPEC-0202 and SPEC-0204 are not implemented at `81096a83`, so every name of a rule, field and test of theirs here comes from their Spec texts and is re-read in the base before work starts.

Failure modes and fallback or human escalation:

If the landing audit finds an ID that left a table, a retired ID that became active or a changed code, the author stops and asks the user; no table is repaired without a decision. If a rule refuses a change that the contract allows, such as a rename, a retirement or an appended row, the rule is wrong and is fixed before commit; no rule or test is relaxed to pass a document. If the one section of the base registry cannot be read as plain JSON, or any existing lifecycle test fails, the author stops and asks the user. If SPEC-0194 is not implemented in the base or SPEC-0204 has not merged, the author waits.

## Acceptance Criteria

### Criteria

| Criterion ID | Expected Result |
| --- | --- |
| VAL-RULEHIST-001 | A rule ID of the base that is missing from the proposal is refused, including the deletion of the last row with or without a new rule under its number, and a retired row that becomes active is refused; a retirement, an appended row and a rename pass; the tests fail first and then pass over real Git snapshots. |
| VAL-RULEHIST-002 | A changed code and a removed reserved code are refused; a policy that leaves the tree passes with its code reserved and is refused without; the base registry is read as one plain JSON section and a base without it yields no rule; the tests fail first and then pass, and the existing lifecycle suites pass unchanged. |
| VAL-RULEHIST-003 | The landing audit is recorded for the fifteen policies with no finding and no audit script is committed; the policy texts state the permanence with their new rule IDs; W03-D64, the closure of W03-H29 and its ledger entry are recorded; validator diagnostics outside the scope are unchanged; exact-index QA and the commit hooks pass. |

### Evidence Requirements

- Before and after, record the four strict document validators; diagnostics after must equal those before.
- Show the new tests failing first, then passing, and the existing lifecycle suites passing unchanged.
- Run the landing audit and record the commits read and the result for each of the fifteen policies; confirm that no audit script is in the index.
- Show `python3 scripts/validate-document-lifecycle.py --root . --mode staged` passing on the package's own commits, which add rules to adopted policies.
- `python3 scripts/run-contract-tests.py --root . --suite document`, `--suite document-lifecycle`, `--suite agent-governance`, `--suite validation-routing`, `--suite tooling`.
- `python3 scripts/validate-document-contract-registry.py --root .`; `python3 scripts/validate-affected-surfaces.py --root .`; `python3 scripts/validation/repository/quality.py --root .`; markdownlint over the edited Markdown; `ruff check scripts tests`; `python3 scripts/qa.py staged` and the commit hooks on the exact index; `graphify update .` after the code change.

## References

### Normative and Evidence

No separate reference list is kept; the requirement, architecture and decision owners this Spec relies on are linked in [Lifecycle Traceability](#lifecycle-traceability) below.

### Historical and Navigation

No separate reference list is kept; this Spec holds no historical or navigation links beyond the [Plan](plan.md) and the Task that its Overview names.

### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-RULEHIST-001 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Lifecycle comparison tests over Git snapshots. |
| [REQ-0003-FR-0028](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-RULEHIST-002 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Direct refusal tests for the code and reserved list rules. |
| [REQ-0003-FR-0032](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-RULEHIST-003 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Landing audit; strict validators over the tree; exact-index QA. |
