---
title: "W03 Governance Policy Rule IDs"
version: "1.0.0"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-11-14"
artifact_id: "SPEC-0199"
---

# W03 Governance Policy Rule IDs Technical Specification (Spec)

## Overview

This approved change contract is Policy package 3 of handoff W03-H29 of the W03 stage of the external v14.7 execution package, recorded in the [SPEC-0161 Task](../0161-w00-v14-7-delta-intake/tasks/tsk-0001-w00-v14-7-delta-intake.md). SPEC-0194 (package 2) built the rule ID contract of W03-D42 to W03-D44 and W03-D53: the grammar `<CODE>-R<NNN>`, the `policy_rule_ids` registry section with one code and one `state` per policy, the Rules table, the definition token, the coverage floor and the six document rules. It assigned no ID. Under W03-D65, which the user decided on 2026-11-14 from the W03 task of the external package, `tasks/TASK-hy-home-k8s-W03.md` (REQ, by line), that table is conditional content whose condition is that the policy states normative rules (REQ:310, REQ:742), its common columns are Rule ID, Condition, Level and Evidence (REQ:486), and `Status` is a registered conditional extension (REQ:37, REQ:143). This package applies that contract to the governance policies under `.agents/governance/`, all on the `governance/rule` profile since SPEC-0187: each adopted policy gains a definition token on every rule unit under `Requirements`, the Rules table that its normative rules require (Rule ID, Condition, Level and Evidence, with the `Status` extension), and the state `adopted` in its registry record, with no existing prose reworded. A read of `main` at `8daf643f` found 196 to 215 rule units in the ten policies, 45 to 51 of them in `quality.md`, which also receives 34 of the 42 Markdown fragment links found from other documents into these policies. This package therefore adopts nine policies (151 to 164 units) and leaves `quality.md` to its own package, which follows directly. The choices this package adds (that split, the unit rule for H4 groups and for paragraphs outside every unit, the Level rule and the Condition and Evidence rule) are recorded as W03-D58 with this package's first commit, which copies the user's answers; the number is re-read at commit time. The package depends on SPEC-0194 being implemented and merged, and merges after SPEC-0198. The [Task](tasks/tsk-0001-w03-governance-policy-rule-ids.md) records execution and the reviewed unit inventory, and the [Plan](plan.md) orders the work.

## Strategic Boundaries & Non-goals

- In scope (writer W03): the nine policies `.agents/governance/agent-execution.md`, `approval-and-safety.md`, `context-and-memory.md`, `document-authoring.md`, `document-lifecycle.md`, `formatting-and-linting.md`, `git.md`, `model-selection.md` and `sdlc.md` (definition tokens, one Rules table, an H4 heading over each paragraph that states a rule outside every unit, and the frontmatter `version` and `updated`); `docs/99.templates/registry.json` (the `state` of the nine records, `pending` to `adopted`); `tests/test_policy_rule_ids.py` only where it pins the repository's record states; in the SPEC-0161 Task the appended W03-D58 row, the refreshed state cell of W03-H29, an evidence row and the frontmatter `version` and `updated`, with the matching W03-H29 entry of the work residue ledger; this package, `docs/03.specs/README.md` and reviewed `.secrets.baseline` entries.
- Not in this package: `.agents/governance/quality.md` (its own package, next); the five operations policies (package 4); the no-reuse check across history and the rule that a code changes only while `pending` (package 5); the retirement of the adoption gate, which belongs to the package that adopts the last policy; any validator, schema, template, form, profile or registry content other than the nine `state` values; any `Purpose`, `Scope`, `Enforcement`, `Exceptions` or `Ownership` text; any existing heading text or anchor; the glossary.
- No rule changes its wording, meaning, owner or enforcement in this package. No push, PR or merge without the user's approval. Open question: none; W03-D58 settles the choices.

## Contracts

- **Adoption (W03-D53).** For each of the nine policies, one commit changes the document and sets its record to `adopted`; several policies may share a commit. After it, the six document rules of SPEC-0194 (`POLICY-RULE-CODE`, `POLICY-RULE-ADOPTION`, `POLICY-RULE-TABLE`, `POLICY-RULE-ID`, `POLICY-RULE-INLINE`, `POLICY-RULE-COVERAGE`) pass on that policy. The codes are those SPEC-0194 registered: `EXEC`, `SAFE`, `CTX`, `AUTHOR`, `DOCLIFE`, `FMT`, `GIT`, `MODEL` and `SDLC`; `QUAL` stays `pending`.
- **Rule units (W03-D43, W03-D58).** Every top-level list item under `Requirements` is one rule and every table row is one rule, each led by its definition token. An H4 group that holds no list item and no table row is one rule, identified by a token paragraph directly under its heading. An H4 group that holds items or rows and also paragraphs of its own takes a group token only when those paragraphs state a rule beyond its items and rows; a sentence that only introduces them takes none. A paragraph that states a rule outside every H4 group and list item is placed under a new H4 heading, alone or with the adjacent paragraphs of the same subject, and identified as a group; the heading is new text and the paragraph is not reworded. A nested list item belongs to its parent's rule.
- **Numbering (W03-D42).** IDs are issued in document order from `R001` without a gap, a group token before the members of its group. Every row of this package has Status `active`.
- **Rules table (W03-D43, W03-D44, W03-D65).** Each of the nine policies states normative rules, so the condition of the Rules table holds for it. Each holds one Rules table directly under the `Requirements` heading, before the first rule, where the template places it, with the four common columns, the registered `Status` extension and one row per ID in ascending order.
- **Level (W03-D58).** The strongest obligation in the unit governs. `required` is the default and covers an imperative, a prohibition and the words must, never and only. `recommended` applies only when the unit's sole obligation is worded should or prefer. `optional` applies only when the unit does nothing but grant a permission worded may or can. A unit that joins a requirement with a permission is `required`. The policies are not written with reserved keywords, so the Level is a reading of each unit, listed for review, and no wording is changed to fit a Level.
- **Condition and Evidence (W03-D58).** Condition restates when the rule applies, from the rule's own applicability clause, or reads `Always` when the rule states none. Evidence names the check, validator, suite or record that the policy's `Enforcement` section or the validation registry already names for that rule; where no automated check exists it names the review that judges the rule. No cell names a check that does not exist, and no cell adds an obligation the rule does not state.
- **Prose unchanged (W03-D43).** Four insertions are allowed and no other byte changes: the Rules table, as its lines and the one blank line after it; an item or row token, as the code span and the one space after it; a group token, as its own line and the one blank line after it; and an added H4 heading, as its line and the one blank line after it. After exactly those bytes are removed, each policy's body equals its body at the base byte for byte. Lines are not re-wrapped.
- **Anchors.** No existing heading text changes, and every added H4 heading has a slug that no other heading of its document has, so no existing anchor moves or gains a numeric suffix. Both kinds of consumer keep resolving: the Markdown fragment links (at `8daf643f`, 42 from other documents, 34 of them into `quality.md`, and 2 inside the policies themselves) and the 17 `capability_tier_ref` JSON references of `.agents/roles/registry.json` to `model-selection.md#top` and `model-selection.md#worker`, which `scripts/validate-agent-governance.py` resolves against one-word heading lines; four more such strings sit in Python test fixtures, one of them naming a missing heading on purpose.
- **Reviewed inventory.** The Task holds, for each policy, the units read at the base (top-level items, table rows, H4 groups without a list or table, H4 groups with both, paragraphs outside every unit) and the range of IDs they yield. Before the Spec is approved the review confirms it; at implementation the Task records the final map of each ID to its unit, its Level and the judgment made for each mixed group and each paragraph outside a unit.
- **Versions.** Each adopted policy takes one minor version step and the commit date, as the document authoring policy sets for section growth without a change of meaning.
- **Decision and handoff rows.** The package commit appends W03-D58 to the SPEC-0161 Task with the user's exact words and refreshes the state cell of W03-H29 and its ledger entry; no recorded decision row is edited.

## Core Design

[AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) owns the governance view; no component changes and no ADR body changes. The registry stays the single machine owner of the codes and their states, and the profile check stays the one reader of a policy body.

## Data Modeling & Storage Strategy

Nine registry `state` values change. Nine policies gain between 151 and 164 definition tokens and as many table rows; nothing else is stored.

## Interfaces & Data Structures

- `docs/99.templates/registry.json`: `policy_rule_ids.codes`, the `state` of nine records.
- The nine policies: the Rules table, the definition tokens and the added H4 headings.
- No script changes. `tests/test_policy_rule_ids.py` changes only if it pins the record states of the repository registry.

## Edge Cases & Error Handling

- `document-authoring.md` holds nine paragraphs after its numbered list and `sdlc.md` one after its own, outside every H4 group; each is judged, and those that state a rule get an H4 heading. The headings add anchors and change none.
- `document-authoring.md` carries the Policy sentence that SPEC-0194 added; it is read as it stands at the base.
- A validator or test that pins a sentence of a policy reads it after the token; if one fails because of a token, the author stops and asks the user, and no pin, rule or test is relaxed.
- `agent-execution.md` and `approval-and-safety.md` are read at the start of every agent session, and each policy grows by one table row per rule; cells stay short.
- A unit whose Level, Condition or Evidence cannot be read from the policy without adding meaning is listed in the Task and goes to the user before its policy is adopted.

## Failure Modes & Fallback / Human Escalation

If a policy cannot pass the six rules without rewording prose, if an Evidence cell would need a check that does not exist to be invented, or if the unit map departs from the reviewed inventory beyond its stated range, the author stops, leaves that policy `pending` and asks the user; the other policies may proceed. If any document outside the scope gains a diagnostic, or a suite fails, the change is wrong and is fixed before commit. If SPEC-0194 is not implemented in the base, the author waits.

## Verification Commands

- Before and after, record the four strict document validators; diagnostics after must equal those before.
- For each policy, show the profile check refusing it with its record `adopted` and its body unchanged, then passing after the tokens and table.
- For each policy, remove exactly the inserted bytes the contract defines (the Rules table, the tokens and the added headings, each with its one following blank line or space) from the new body and compare the result with the base body; record both hashes.
- Verify the anchors for both kinds of consumer: the strict link validator, with the fragment check of SPEC-0193, for the Markdown fragment links, and `python3 scripts/validate-agent-governance.py --root .` for the `capability_tier_ref` JSON references; compare the heading slugs of each policy before and after, so that the base slugs are unchanged and each added slug is new in its document.
- `python3 scripts/run-contract-tests.py --root . --suite document`, `--suite document-lifecycle`, `--suite agent-governance`, `--suite validation-routing`, `--suite tooling`.
- `python3 scripts/validate-document-contract-registry.py --root .`; `python3 scripts/validation/repository/quality.py --root .`; markdownlint over the edited Markdown; `python3 scripts/qa.py staged` and the commit hooks on the exact index.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-GOVRULE-001 | Each of the nine policies carries its definition tokens and one Rules table, its record is `adopted`, and the six document rules pass on it after failing on the unchanged body; `quality.md` and the five operations policies stay `pending` and unchanged. |
| VAL-GOVRULE-002 | For each policy the body with exactly the defined insertions removed equals the base body; every anchor resolves for both kinds of consumer, the Markdown fragment links and the `capability_tier_ref` JSON references, and each added heading slug is unique in its document; the Task records the final map of each ID to its unit with its Level, Condition and Evidence reading, within the reviewed inventory; each policy took one minor version step. |
| VAL-GOVRULE-003 | W03-D58, the W03-H29 state and the ledger entry are recorded; validator diagnostics outside the nine policies are unchanged; the suites, exact-index QA and the commit hooks pass. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0013](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-GOVRULE-001 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Strict Markdown profile check on each adopted policy; registry check. |
| [REQ-0003-FR-0032](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-GOVRULE-002 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Byte comparison of the stripped bodies; link and agent governance checks; reviewed unit map. |
| [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-GOVRULE-003 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Strict validators over the tree; suites; exact-index QA. |
