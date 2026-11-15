---
title: "W03 Onboarding Policy Rule IDs"
version: "2.0.0"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-11-15"
artifact_id: "SPEC-0204"
---

# W03 Onboarding Policy Rule IDs Technical Specification (Spec)

## Overview

### Intent

This approved change contract is Policy package 4b of handoff W03-H29 of the W03 stage of the external v14.7 execution package, recorded in the [SPEC-0161 Task](../0161-w00-v14-7-delta-intake/tasks/tsk-0001-w00-v14-7-delta-intake.md). SPEC-0194 built the rule ID contract of W03-D42 to W03-D44 and W03-D53 with an adoption gate: a `state` per policy in the `policy_rule_ids` registry section and the `POLICY-RULE-ADOPTION` rule keep the checks green while a policy is `pending`, and the package that adopts the last policy retires that gate. SPEC-0199, SPEC-0201 and SPEC-0202 adopt fourteen policies. On 2026-11-14 the user decided (W03-D62, recorded by the SPEC-0202 package commit) that POL-0007, the app GitOps onboarding policy at `docs/05.operations/policies/0007-app-gitops-onboarding-policy.md`, gets this package of its own, that it takes 45 rule IDs under a table that is binding at approval, and that this package carries the gate retirement. A read of `main` at `4bcda456` found that the policy, Korean-first, holds under `Requirements` an opening paragraph, 4 empty chapter headings, 4 H4 groups without a list or table, 5 mixed groups, 19 top-level list items and 19 table rows, with no nested item and no control register. Under W03-D62 the opening paragraph only introduces the chapters and takes no ID, each of the five mixed groups takes a group token, the two list items labelled `Required evidence` are evidence and take none, and every other item and row is one rule: `ONBOARD-R001` to `ONBOARD-R045`. This package gives the policy those definition tokens, the Rules table that its normative rules require (Rule ID, Condition, Level and Evidence, with the `Status` extension) and the state `adopted`, with no existing prose reworded; then its final source commit removes `state`, `POLICY-RULE-ADOPTION` and their tests, so that no adoption state stands between a policy and the contract. It does not make the table unconditional: under W03-D65, which the user decided on 2026-11-14 from the W03 task of the external package, `tasks/TASK-hy-home-k8s-W03.md` (REQ, by line), the Rules table is conditional content whose condition is that the policy states normative rules (REQ:310, REQ:742), its common columns are Rule ID, Condition, Level and Evidence (REQ:486), `Status` is a registered conditional extension (REQ:37, REQ:143), and the minimum of one row applies under that condition. The package records no new decision. It depends on SPEC-0194 being implemented in the base and merges after SPEC-0202. The [Task](tasks/tsk-0001-w03-onboarding-policy-rule-ids.md) records execution and the binding unit table, and the [Plan](plan.md) orders the work.

### Owning Requirements

[AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) owns the governance view; no component changes and no ADR body changes. The registry stays the single machine owner of the codes, and the profile check stays the one reader of a policy body.

## Scope

### In Scope

- In scope (writer W03, with W05 for validator code): the policy named above (definition tokens, one Rules table, and the frontmatter `version` and `updated`); `docs/99.templates/registry.json` (the `state` of the `ONBOARD` record, then the removal of `state` from all fifteen records); `docs/99.templates/contracts/document-profile.schema.json` (the `state` property); `scripts/document_contracts.py` (the loaded record); `scripts/validate-markdown-profiles.py` (the removal of `POLICY-RULE-ADOPTION`); `tests/test_policy_rule_ids.py` where it tests the gate or pins record states, and `tests/test_document_generator.py` only if its recorded authoring set changes; every sentence that names the state or the gate in `.agents/governance/document-authoring.md`, `docs/99.templates/README.md` and the two Policy templates; in the SPEC-0161 Task the refreshed state cell of W03-H29, an evidence row and the frontmatter `version` and `updated`, with the matching W03-H29 entry of the work residue ledger; this package, `docs/03.specs/README.md` and reviewed `.secrets.baseline` entries.

### Non-goals

- Not in this package: the fourteen policies adopted earlier; the no-reuse check across history and the permanence of a registered code (package 5); the coverage floor and every other rule, the grammar and the definition positions of SPEC-0194 as SPEC-0202 leaves them; the `Lifecycle Traceability` table and the body contract of the profile; any `Purpose`, `Scope`, `Enforcement`, `Exceptions` or `Ownership` text; any existing heading text or anchor; the runbook, the sample app and the manifests the policy names; the shared Policy form; the glossary; `_workspace/` (read-only input) and `docs/98.archive/`.
- No rule changes its wording, meaning, owner or enforcement in this package. No push, PR or merge without the user's approval. Open question: none; W03-D62 settles the choices.

## Behavior Contract

### Normal Behavior

Contracts:

- **Adoption (W03-D53).** One commit changes the policy and sets the `ONBOARD` record to `adopted`. After it, the six document rules of SPEC-0194 (`POLICY-RULE-CODE`, `POLICY-RULE-ADOPTION`, `POLICY-RULE-TABLE`, `POLICY-RULE-ID`, `POLICY-RULE-INLINE`, `POLICY-RULE-COVERAGE`) pass on the policy, and all fifteen records are `adopted`.
- **Rule units (W03-D43, W03-D58, W03-D62).** A top-level list item and a table row are each one rule led by its definition token. An H4 group without a list item or table row is one rule, identified by a token paragraph directly under its heading. Each of the five mixed groups takes a group token, because a paragraph of its own states a rule beyond its items or rows. The opening paragraph only introduces the chapters: it takes no ID and no heading is added over it. A list item labelled `Required evidence` is the evidence of its group's rule and takes no token; its group token covers it. The four chapter headings hold no content of their own, so none of them is an H4 rule group as SPEC-0194 reads the term, a group identified by a token paragraph over the rule text it holds (W03-D43); they take no ID by that reading, not by an exception. No group is split.
- **Numbering (W03-D42, W03-D62).** The policy takes exactly 45 IDs, `ONBOARD-R001` to `ONBOARD-R045`, issued in document order without a gap, a group token before the members of its group, as the Task's table lists them. Every row of this package has Status `active`.
- **Binding table (W03-D62).** The Task's table gives, for each H4 group, the units read at the base and the IDs they take. It is the binding reading, not a preliminary one. The implementation issues exactly those IDs to those units. If the policy at the implementation base no longer matches a row, the author stops and asks the user before any ID is issued.
- **Rules table (W03-D43, W03-D44, W03-D65).** The policy states normative rules, so the condition of the Rules table holds for it. It holds one Rules table directly under the `Requirements` heading, before the opening paragraph, with the four common columns, the registered `Status` extension and one row per ID in ascending order. The column names, the IDs and the Level and Status values are the same ASCII text as in every other policy (W03-D42).
- **Level (W03-D58, W03-D62).** The strongest obligation in the unit governs, read by meaning. `required` is the default and covers an obligation, a prohibition and every item of the group that lists what is forbidden. `권장` reads `recommended` and `선택` reads `optional`, when that is the unit's sole obligation. No wording is changed to fit a Level.
- **Condition (W03-D58, W03-D62).** Condition restates when the rule applies, from the rule's own applicability clause. When the rule states none it reads `Always`, the same ASCII value in every policy; other Condition and Evidence text follows the document's language (W03-D53).
- **Evidence (W03-D62).** Evidence cites, in this order, the first that exists for the rule: a control ID of the policy's own control register, which this policy does not have; the runbook or guide that the policy's `Enforcement` section names, by artifact ID; an existing repository check, looked up in `scripts/validation/registry.json`, `scripts/run-contract-tests.py` or the tree; otherwise the review that judges the rule. No cell names an artifact or check that does not exist, no cell copies the text of a `Required evidence` line or of the runbook, and no cell adds an obligation the rule does not state. Cells are short phrases, not sentences.
- **Review before the flip (W03-D58, W03-D62).** The map of each of the 45 IDs to its unit with its final Level, Condition and Evidence is listed in the Task for the user's review before the commit that sets the record to `adopted`. The same list names the opening paragraph as a no-ID reading, because it is worded as an imperative summary of the chapters.
- **Prose unchanged (W03-D43).** Three insertions are allowed and no other byte changes: the Rules table, as its lines and the one blank line after it; an item or row token, as the code span and the one space after it; and a group token, as its own line and the one blank line after it. After exactly those bytes are removed, the policy's body equals its body at the base byte for byte. Lines are not re-wrapped and no table is re-aligned.
- **Anchors.** No existing heading text changes and no heading is added. At `4bcda456` no Markdown fragment link targets this policy and no tracked file other than Markdown names a fragment of it; such files name its path only. Both kinds are searched again at implementation, and every consumer found keeps resolving.
- **Gate retirement (W03-D53, W03-D62, W03-D65).** After the fifteenth record is `adopted`, the final source commit of the package removes the `state` field from the fifteen records, the schema and the loader, and removes `POLICY-RULE-ADOPTION` and the tests of the gate. W03-D53 and W03-D62 also raised `minimum_rows` to 1 in the Policy TemplateDefinitions; W03-D65 replaces that step. The Rules table is conditional content (REQ:310, REQ:742), so the `minimum_rows` of the definitions stays 0 and the minimum of one row, which `rules_table` records with the condition, applies when the policy states normative rules. From then the rules apply with no adoption state between: a policy that states normative rules, or carries a Rules table, fails `POLICY-RULE-CODE` without a record and holds its table with at least one row, and a new one registers its code and carries its table in its first commit; a policy that states no normative rule needs neither. The ongoing protection moves to the rules that no longer read a state before the gate leaves, as the work lifecycle requires for a one-use check: new tests show a record with a `state` key refused, a policy that states normative rules with a record and no Rules table refused and a header-only Rules table refused, each failing first, and a policy that states no normative rule accepted without a table or a record. The past results of the gate stay in the Tasks of the earlier packages and in Git history.
- **Version.** The policy takes one minor version step from its version at the base and the commit date.
- **Handoff row.** The implementation refreshes the state cell of W03-H29 and its ledger entry: fifteen policies adopted, the gate retired, package 5 left. No recorded decision row is edited.

Data modeling and storage strategy:

One registry `state` value changes and the field then leaves all fifteen records; no `minimum_rows` value changes. One policy of 13,952 bytes at `4bcda456` gains 45 definition tokens and 45 table rows.

Interfaces and data structures:

- `docs/99.templates/registry.json` and `document-profile.schema.json`: `policy_rule_ids.codes` without `state`; the `Rules` table definition and `rules_table` unchanged.
- `scripts/document_contracts.py` and `scripts/validate-markdown-profiles.py`: the record without a state and five document rules without the gate.
- Tests: the three refusals and the one acceptance named under Gate retirement; all fifteen policies pass the profile check.
- The policy: the Rules table and the definition tokens.

### Failure and Edge Cases

Edge cases and error handling:

- The policy uses H4 for chapters and sections alike and separates chapters with horizontal rules; neither changes.
- Its four tables are padded to aligned columns; a token lengthens the first cell of each row and no padding is changed, so the alignment of those rows is lost and nothing else moves.
- The items of three groups begin with a bold label and two items of the forbidden list with a code span; the token precedes them and is the first content of the item.
- The profile's language check judges plain paragraphs only, so a token paragraph and a table cell draw no language finding in this Korean-first policy.
- `scripts/validation/repository/quality.py` scans the policy for commands, and one forbidden item names a command; if a token changes one of its findings, the author stops and asks the user, and no rule or test is relaxed.
- The retirement removes a registry key; if a reader of a comparison-base registry refuses the change, the author stops and asks the user.
- SPEC-0194 is not implemented at `4bcda456`, so every name of a rule, field and test here comes from its approved text and is re-read in the base before work starts.

Failure modes and fallback or human escalation:

If the policy cannot pass the six rules without rewording prose, if a cell would need an artifact or check that does not exist, if a unit's Level, Condition or Evidence cannot be read without adding meaning, or if the units at the base no longer match the binding table, the author stops, leaves the record `pending` and asks the user. The gate is not retired while any record is `pending`. If any document outside the scope gains a diagnostic, an adopted policy fails without the gate, or a suite fails, the change is wrong and is fixed before commit. If SPEC-0194 is not implemented in the base or SPEC-0202 has not merged, the author waits.

## Acceptance Criteria

### Criteria

| Criterion ID | Expected Result |
| --- | --- |
| VAL-ONBRULE-001 | The policy carries the 45 definition tokens `ONBOARD-R001` to `ONBOARD-R045` on the units the binding table names and one Rules table of 45 rows, its record is `adopted`, and the six document rules pass on it after failing on the unchanged body; all fifteen records are `adopted`. |
| VAL-ONBRULE-002 | The body with exactly the defined insertions removed equals the base body; every anchor resolves and the heading slugs are unchanged; the Task lists the map of each ID to its unit with its Level, Condition and Evidence, reviewed before the record flipped; every named artifact and check exists; the policy took one minor version step. |
| VAL-ONBRULE-003 | The gate is retired in the final source commit: no record, schema or loader carries `state`, `POLICY-RULE-ADOPTION` and its tests are gone, the minimum of one row applies to every policy that states normative rules while `minimum_rows` stays 0 in both definitions, the three refusal tests fail first and then pass, a policy that states no normative rule passes without a table, and all fifteen policies pass without the gate. |
| VAL-ONBRULE-004 | The W03-H29 state and the ledger entry are recorded; validator diagnostics outside the scope are unchanged; the suites, exact-index QA and the commit hooks pass. |

### Evidence Requirements

- Before and after, record the four strict document validators; diagnostics after must equal those before.
- Show the profile check refusing the policy with its record `adopted` and its body unchanged, then passing after the tokens and table.
- Remove exactly the inserted bytes the contract defines from the new body and compare the result with the base body; record both hashes.
- Verify the anchors for both kinds of consumer: the strict link validator, with the fragment check of SPEC-0193, and a search of every tracked file for a fragment of this policy; compare its heading slugs before and after.
- Check every Evidence cell that names an artifact, a validator, a suite or a path against the tree, `scripts/validation/registry.json` or `scripts/run-contract-tests.py`.
- For the retirement, show the three refusal tests failing first and then passing, the policy without normative rules accepted, and all fifteen policies passing the profile check without the gate.
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
| [REQ-0003-FR-0013](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ONBRULE-001 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Strict Markdown profile check on the adopted policy; registry check. |
| [REQ-0003-FR-0032](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ONBRULE-002 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Byte comparison of the stripped body; link check; reviewed unit map. |
| [REQ-0003-FR-0028](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ONBRULE-003 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Direct refusal tests for the retired gate; profile check over the fifteen policies. |
| [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ONBRULE-004 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Strict validators over the tree; suites; exact-index QA. |
