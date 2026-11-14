---
title: "W03 Quality Policy Rule IDs"
version: "2.0.0"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-11-15"
artifact_id: "SPEC-0201"
---

# W03 Quality Policy Rule IDs Technical Specification (Spec)

## Overview

### Intent

This approved change contract is Policy package 3b of handoff W03-H29 of the W03 stage of the external v14.7 execution package, recorded in the [SPEC-0161 Task](../0161-w00-v14-7-delta-intake/tasks/tsk-0001-w00-v14-7-delta-intake.md). SPEC-0194 built the rule ID contract of W03-D42 to W03-D44 and W03-D53 (the grammar `<CODE>-R<NNN>`, the `policy_rule_ids` registry section, the Rules table, the definition token, the coverage floor and the six document rules), and SPEC-0199 applied it to nine governance policies. Under W03-D65, which the user decided on 2026-11-14 from the W03 task of the external package, `tasks/TASK-hy-home-k8s-W03.md` (REQ, by line), that table is conditional content whose condition is that the policy states normative rules (REQ:310, REQ:742), its common columns are Rule ID, Condition, Level and Evidence (REQ:486), and `Status` is a registered conditional extension (REQ:37, REQ:143). The user decided (W03-D58) that `.agents/governance/quality.md` gets its own package after SPEC-0199, with the same unit, Level, Condition and Evidence rules. This package applies them to that one policy: every rule unit under `Requirements` gains a definition token, the policy gains the Rules table that its normative rules require (Rule ID, Condition, Level and Evidence, with the `Status` extension), and its registry record, code `QUAL`, moves from `pending` to `adopted`, with no existing prose reworded. A read of `main` at `8daf643f` found, under `Requirements`, eleven H4 groups and nothing outside them: 33 top-level list items, 7 table rows, 5 groups without a list or table and 6 mixed groups. On 2026-11-14 the user decided (W03-D60) that all six mixed groups take a group token, which fixes 51 rule IDs, `QUAL-R001` to `QUAL-R051`; that one ID identifies a group and no group is split; and that Evidence cites only an existing validator ID, suite, script or the Task record, each looked up, and otherwise names the judging review. The table of those 51 IDs in the Task is the binding reading, not a preliminary one. Nine of the eleven H4 headings are the targets of the 34 Markdown fragment links that 25 other documents make into this policy, and the provider baselines name the policy among the files to read before acting. With this package all ten governance policies are adopted; the five operations policies stay `pending` for package 4. The package commit records W03-D60 in the SPEC-0161 Task. The package depends on SPEC-0194 being implemented in the base and merges after SPEC-0199. The [Task](tasks/tsk-0001-w03-quality-policy-rule-ids.md) records execution and the binding unit table, and the [Plan](plan.md) orders the work.

### Owning Requirements

[AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) owns the governance view; no component changes and no ADR body changes. The registry stays the single machine owner of the codes and their states, and the profile check stays the one reader of a policy body.

## Scope

### In Scope

- In scope (writer W03): `.agents/governance/quality.md` (definition tokens, one Rules table, and the frontmatter `version` and `updated`); `docs/99.templates/registry.json` (the `state` of the `QUAL` record, `pending` to `adopted`); `tests/test_policy_rule_ids.py` only where it pins the repository's record states; in the SPEC-0161 Task the appended W03-D60 row, the refreshed state cell of W03-H29, an evidence row and the frontmatter `version` and `updated`, with the matching W03-H29 entry of the work residue ledger; this package, `docs/03.specs/README.md` and reviewed `.secrets.baseline` entries.

### Non-goals

- Not in this package: the nine policies of SPEC-0199 and the five operations policies (package 4); the no-reuse check across history and the rule that a code changes only while `pending` (package 5); the retirement of the adoption gate, which belongs to the package that adopts the last policy; any validator, schema, template, form, profile or registry content other than the one `state` value; any `Purpose`, `Scope`, `Enforcement`, `Exceptions` or `Ownership` text of the policy; any existing heading text or anchor; any document that links the policy; the glossary.
- No rule changes its wording, meaning, owner or enforcement in this package. No push, PR or merge without the user's approval. Open question: none.

## Behavior Contract

### Normal Behavior

Contracts:

- **Adoption (W03-D53).** One commit changes the policy and sets the `QUAL` record to `adopted`. After it, the six document rules of SPEC-0194 (`POLICY-RULE-CODE`, `POLICY-RULE-ADOPTION`, `POLICY-RULE-TABLE`, `POLICY-RULE-ID`, `POLICY-RULE-INLINE`, `POLICY-RULE-COVERAGE`) pass on the policy.
- **Rule units (W03-D43, W03-D58, W03-D60).** Every top-level list item under `Requirements` is one rule and every table row is one rule, each led by its definition token. An H4 group that holds no list item and no table row is one rule, identified by a token paragraph directly under its heading. An H4 group that holds items or rows and also paragraphs of its own takes a group token only when those paragraphs state a rule beyond its items and rows; a sentence that only introduces them takes none. For this policy that reading is settled (W03-D60): each of the six mixed groups takes a group token. A paragraph that states a rule outside every H4 group and list item is placed under a new H4 heading and identified as a group; none exists at `8daf643f`, so no heading is added unless the base has changed. One ID identifies a group and no existing H4 group is split (W03-D60), because a new heading inside a group would shorten the section that an existing anchor names.
- **Numbering (W03-D42, W03-D60).** The policy takes exactly 51 IDs, `QUAL-R001` to `QUAL-R051`, issued in document order without a gap, a group token before the members of its group, as the Task's table lists them. Every row of this package has Status `active`.
- **Rules table (W03-D43, W03-D44, W03-D65).** The policy states normative rules, so the condition of the Rules table holds for it. It holds one Rules table directly under the `Requirements` heading, before the first H4 group, where the template places it, with the four common columns, the registered `Status` extension and one row per ID in ascending order.
- **Level (W03-D58).** The strongest obligation in the unit governs. `required` is the default and covers an imperative, a prohibition and the words must, never and only. `recommended` applies only when the unit's sole obligation is worded should or prefer, and `optional` only when the unit does nothing but grant a permission. A unit that joins a requirement with a permission is `required`. No wording is changed to fit a Level.
- **Condition and Evidence (W03-D58, W03-D60).** Condition restates when the rule applies, from the rule's own applicability clause, or reads `Always` when the rule states none. Evidence cites only a check that exists, each one looked up (W03-D60): a validator ID of `scripts/validation/registry.json`, a suite of `scripts/run-contract-tests.py`, a tracked script or hook, or the Task record that holds the result. Where no automated check exists it names the review that judges the rule. The policy's `Enforcement` section names one owner, the validation routing registry, so most cells are read from that registry. No cell names a check that does not exist, and no cell adds an obligation the rule does not state. Cells are short phrases, not sentences.
- **Prose unchanged (W03-D43).** Four insertions are allowed and no other byte changes: the Rules table, as its lines and the one blank line after it; an item or row token, as the code span and the one space after it; a group token, as its own line and the one blank line after it; and an added H4 heading, as its line and the one blank line after it. After exactly those bytes are removed, the policy's body equals its body at the base byte for byte. Lines are not re-wrapped.
- **Anchors.** No existing heading text changes, and an added H4 heading, if the base requires one, has a slug that no other heading of the document has, so no existing anchor moves or gains a numeric suffix. At `8daf643f` the consumers are 34 Markdown fragment links from 25 documents to nine slugs: `validation-lane-contract` (9), `validation-runner-envelope` (5), `agent-evaluation-evidence` (5), `semantic-review` (3), `ordinary-document-selection` (3), `handoff-evidence-contract` (3), `delivery-ownership` (3), `canonical-completion-sequence` (2) and `result-vocabulary` (1). No tracked file other than Markdown names a fragment of this policy; such files name its path only, in the `consumer_paths` of the registry, in validator path sets and in test fixtures. Both kinds are searched again at implementation, and every consumer found keeps resolving.
- **Binding table (W03-D60).** The Task holds, for each H4 group, the units read at the base, the links into it and the IDs it takes. That table is the binding reading, not a preliminary one: the implementation issues exactly those IDs to those units and records the map of each ID to its unit with its Level, Condition and Evidence. That map, with the final Level, Condition and Evidence of all 51 IDs, is listed in the Task for the user's review before the commit that sets the `QUAL` record to `adopted`, because W03-D58 requires each reading to be listed for review. If the policy at the implementation base no longer matches a row of the table, the author stops and asks the user before any ID is issued.
- **Version.** The policy takes one minor version step from its version at the base and the commit date, as the document authoring policy sets for section growth without a change of meaning.
- **Decision and handoff rows.** The package commit appends W03-D60 to the SPEC-0161 Task with the user's exact words. The implementation refreshes the state cell of W03-H29 and its ledger entry: all ten governance policies adopted, the five operations policies and the gate retirement left to package 4. No recorded decision row is edited.

Data modeling and storage strategy:

One registry `state` value changes. One policy gains 51 definition tokens and 51 table rows; nothing else is stored.

Interfaces and data structures:

- `docs/99.templates/registry.json`: `policy_rule_ids.codes`, the `state` of the `QUAL` record.
- `.agents/governance/quality.md`: the Rules table and the definition tokens.
- No script changes. `tests/test_policy_rule_ids.py` changes only if it pins the record states of the repository registry.

### Failure and Edge Cases

Edge cases and error handling:

- The items of `Result vocabulary` begin with a code span such as `PASS`, and those of `Validation lane contract` and `Canonical completion sequence` with a bold label; the token precedes them and is the first content of the item.
- The eight items of `Handoff evidence contract` are the clauses of one sentence that its opening line introduces; each item is one rule and keeps its punctuation.
- A group token and the item or row tokens of the same group coexist; the group token identifies the group's own paragraphs.
- A unit that defines a result value uses no modal word; the default `required` applies to it.
- Eleven IDs, the five groups without a list or table and the six group tokens, each cover several sentences; no group is split (W03-D60), and their Condition and Level follow the strongest obligation of the whole group.
- A validator or test that pins a sentence of the policy reads it after the token; if one fails because of a token, the author stops and asks the user, and no pin, rule or test is relaxed.
- The policy holds 22,266 bytes at `8daf643f` and agents read it before acting; one row for each rule adds an estimated 35 to 40 percent. That cost is accepted with this Spec: W03-D43 requires the table, a reader can cite a rule by its ID and find its condition, level and evidence in one row, the cells stay short phrases, and the measured byte delta is recorded in the Task at implementation.

Failure modes and fallback or human escalation:

If the policy cannot pass the six rules without rewording prose, if an Evidence cell would need a check that does not exist, if a unit's Level, Condition or Evidence cannot be read without adding meaning, or if the units at the base no longer match the binding table, the author stops, leaves the record `pending` and asks the user. If any other document gains a diagnostic, a link into the policy stops resolving, or a suite fails, the change is wrong and is fixed before commit. If SPEC-0194 is not implemented in the base or SPEC-0199 has not merged, the author waits.

## Acceptance Criteria

### Criteria

| Criterion ID | Expected Result |
| --- | --- |
| VAL-QUALRULE-001 | The policy carries the 51 definition tokens `QUAL-R001` to `QUAL-R051` on the units the binding table names and one Rules table of 51 rows, the `QUAL` record is `adopted`, and the six document rules pass on it after failing on the unchanged body; the five operations policies stay `pending` and unchanged. |
| VAL-QUALRULE-002 | The body with exactly the defined insertions removed equals the base body; every anchor resolves for both kinds of consumer, the 34 Markdown fragment links and any other file found to name a fragment, and the base heading slugs are unchanged; the Task records the map of each ID to its unit with its Level, Condition and Evidence, as the binding table lists them; every named check exists; the policy took one minor version step. |
| VAL-QUALRULE-003 | W03-D60, the W03-H29 state and the ledger entry are recorded; validator diagnostics outside the policy are unchanged; the suites, exact-index QA and the commit hooks pass. |

### Evidence Requirements

- Before and after, record the four strict document validators; diagnostics after must equal those before.
- Show the profile check refusing the policy with its record `adopted` and its body unchanged, then passing after the tokens and table.
- Remove exactly the inserted bytes the contract defines (the Rules table, the tokens and any added heading, each with its one following blank line or space) from the new body and compare the result with the base body; record both hashes.
- Verify the anchors for both kinds of consumer: the strict link validator, with the fragment check of SPEC-0193, for the Markdown fragment links; a search of every tracked file that is not Markdown for a fragment of this policy, and `python3 scripts/validate-agent-governance.py --root .`, for the others; compare the heading slugs of the policy before and after, so that the base slugs are unchanged and any added slug is new.
- Check every Evidence cell that names a validator, a suite or a path against `scripts/validation/registry.json`, `scripts/run-contract-tests.py` or the tree.
- `python3 scripts/run-contract-tests.py --root . --suite document`, `--suite document-lifecycle`, `--suite agent-governance`, `--suite validation-routing`, `--suite tooling`, `--suite qa-runner`.
- `python3 scripts/validate-document-contract-registry.py --root .`; `python3 scripts/validation/repository/quality.py --root .`; markdownlint over the edited Markdown; `python3 scripts/qa.py staged` and the commit hooks on the exact index.

## References

### Normative and Evidence

No separate reference list is kept; the requirement, architecture and decision owners this Spec relies on are linked in [Lifecycle Traceability](#lifecycle-traceability) below.

### Historical and Navigation

No separate reference list is kept; this Spec holds no historical or navigation links beyond the [Plan](plan.md) and the Task that its Overview names.

### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0013](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-QUALRULE-001 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Strict Markdown profile check on the adopted policy; registry check. |
| [REQ-0003-FR-0032](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-QUALRULE-002 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Byte comparison of the stripped body; link and agent governance checks; unit map against the binding table. |
| [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-QUALRULE-003 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Strict validators over the tree; suites; exact-index QA. |
