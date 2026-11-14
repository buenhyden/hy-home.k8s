---
title: "W03 Operations Policy Rule IDs"
version: "2.0.0"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-11-15"
artifact_id: "SPEC-0202"
---

# W03 Operations Policy Rule IDs Technical Specification (Spec)

## Overview

### Intent

This approved change contract is Policy package 4 of handoff W03-H29 of the W03 stage of the external v14.7 execution package, recorded in the [SPEC-0161 Task](../0161-w00-v14-7-delta-intake/tasks/tsk-0001-w00-v14-7-delta-intake.md). SPEC-0194 (package 2) built the rule ID contract of W03-D42 to W03-D44 and W03-D53: the grammar `<CODE>-R<NNN>`, the `policy_rule_ids` registry section with one code and one `state` per policy, the Rules table, the definition token, the coverage floor, the control register exemption and the six document rules. Under W03-D65, which the user decided on 2026-11-14 from the W03 task of the external package, `tasks/TASK-hy-home-k8s-W03.md` (REQ, by line), that table is conditional content whose condition is that the policy states normative rules (REQ:310, REQ:742), its common columns are Rule ID, Condition, Level and Evidence (REQ:486), and `Status` is a registered conditional extension (REQ:37, REQ:143). SPEC-0199 and SPEC-0201 (packages 3 and 3b) adopt the ten governance policies under the rules of W03-D58 and W03-D60. A read of `main` at `4bcda456` found that the five operations policies differ from them in ways those decisions did not settle, and on 2026-11-14 the user decided the seven open points (W03-D62): POL-0007 moves to its own following package, which adopts the last policy and carries the gate retirement; the W03-D58 rules and the SPEC-0199 contracts are reused unchanged; in POL-0003 and POL-0004, where the top-level items are the label lines `Required`, `Allowed` and `Disallowed` and 54 nested items state the rules, each nested item is one rule and the coverage floor of SPEC-0194 is amended to accept it; the Level is read by meaning and by those labels; Evidence comes first from the policy's own control register and `Enforcement` section; and `Always` is one ASCII value. This package therefore adopts four policies on the `operation/policy` profile, POL-0001, POL-0003, POL-0004 and POL-0005, with the codes `GITOPS`, `MESH`, `ROLLOUT` and `OBSERV`, and amends the coverage floor. Each policy gains a definition token on every rule unit under `Requirements`, the Rules table that its normative rules require (Rule ID, Condition, Level and Evidence, with the `Status` extension) and the state `adopted`, with no existing prose reworded: 18, 30, 27 and 7 rule IDs, 82 in all, which the table in the Task binds. The package commit records W03-D62 in the SPEC-0161 Task. The package depends on SPEC-0194 being implemented in the base and merges after SPEC-0201. The [Task](tasks/tsk-0001-w03-operations-policy-rule-ids.md) records execution and the binding unit table, and the [Plan](plan.md) orders the work.

### Owning Requirements

[AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) owns the governance view; no component changes and no ADR body changes. The registry stays the single machine owner of the codes and their states, and the profile check stays the one reader of a policy body.

## Scope

### In Scope

- In scope (writer W03, with W05 for validator code): the four policies under `docs/05.operations/policies/` named above (definition tokens, one Rules table, and the frontmatter `version` and `updated`); `docs/99.templates/registry.json` (the `state` of the four records, `pending` to `adopted`); `scripts/validate-markdown-profiles.py` (the coverage floor of `POLICY-RULE-COVERAGE`); `tests/test_policy_rule_ids.py` (the tests of the amended floor, and the record states where it pins them); the sentence that states the coverage floor in `.agents/governance/document-authoring.md`, `docs/99.templates/README.md` and the two Policy templates, where one exists; in the SPEC-0161 Task the appended W03-D62 row, the refreshed state cell of W03-H29, an evidence row and the frontmatter `version` and `updated`, with the matching W03-H29 entry of the work residue ledger; this package, `docs/03.specs/README.md` and reviewed `.secrets.baseline` entries.

### Non-goals

- Not in this package: POL-0007 and the retirement of the adoption gate, which is the removal of `state`, `POLICY-RULE-ADOPTION` and their tests, after which the table's condition alone decides (the following package, W03-D62, W03-D65); the ten governance policies; the no-reuse check across history and the permanence of a registered code (package 5); the control registers and the control IDs `PLAT-001` to `PLAT-006` and `OBS-001` to `OBS-006`; the `Lifecycle Traceability` table and the body contract of the profile; any `Purpose`, `Scope`, `Enforcement`, `Exceptions` or `Ownership` text; any existing heading text or anchor; any runbook, guide or manifest the policies name; any other rule, the grammar, the schema or the registry content of SPEC-0194; the shared Policy form; the glossary; `_workspace/` (read-only input) and `docs/98.archive/`.
- No rule changes its wording, meaning, owner or enforcement in this package. No push, PR or merge without the user's approval. Open question: none; W03-D62 settles the choices.

## Behavior Contract

### Normal Behavior

Contracts:

- **Coverage floor (W03-D62).** A top-level list item that begins with a definition token, or lies in an H4 group that carries one, is covered as before, whatever its nested items carry: an untokened nested item under a tokened parent stays part of the parent's rule (W03-D58). `POLICY-RULE-COVERAGE` now also accepts a top-level item that has no token of its own when it is a pure label and every one of its nested items begins with a definition token. A pure label is an item whose own text, trimmed and with the characters `*` and `_` removed, equals one of the three registered labels `Required`, `Allowed` or `Disallowed` followed by a single colon, with nothing else. The three labels are part of this contract, so a fourth label is a contract change. A top-level item without a token of its own, outside a group that carries one, stays refused in every other case: when one of its nested items carries no token, when its own text is more than a pure label even though every nested item is tokened, and when it holds no nested item. Nothing else of SPEC-0194 changes: the grammar, the definition positions, the control register exemption and the other five rules stay as approved. Six tests show it: an untokened label over a fully tokened nested list accepted, which fails before the amendment; a label over a partly tokened list refused; a label over an untokened list refused; an untokened parent whose text is a sentence ending in a colon refused although its nested items are tokened; an untokened parent with an inner colon, `**Required**: x:`, refused although its nested items are tokened; and a tokened parent over untokened nested items accepted, as before. The adopted governance policies still pass.
- **Adoption (W03-D53).** For each of the four policies, one commit changes the document and sets its record to `adopted`; several policies may share a commit. After it, the six document rules of SPEC-0194 (`POLICY-RULE-CODE`, `POLICY-RULE-ADOPTION`, `POLICY-RULE-TABLE`, `POLICY-RULE-ID`, `POLICY-RULE-INLINE`, `POLICY-RULE-COVERAGE`) pass on that policy. POL-0007 stays `pending`, so the gate stays.
- **Rule units (W03-D43, W03-D58, W03-D62).** A top-level list item is one rule led by its definition token, and an H4 group without a list item or table row is one rule, identified by a token paragraph directly under its heading. In POL-0003 and POL-0004 each nested item under a label item is one rule led by its token, and the label item carries none (W03-D62). These four policies hold no mixed group, no empty heading and no paragraph outside a group, so no group token beyond the two prose groups of POL-0005 and no new heading is added.
- **Controls (W03-D42, W03-D53).** The rows of the two control registers keep their control IDs, carry no rule ID and are not rule units. A control is the mechanism that enforces a rule (TERM-CONTROL) and never becomes a rule (TERM-RULE).
- **Numbering (W03-D42).** IDs are issued in document order from `R001` without a gap; the nested items of POL-0003 and POL-0004 are numbered in the order they stand. Every row of this package has Status `active`.
- **Binding table (W03-D62).** The Task's table gives, for each policy and each H4 group or label, the units read at the base and the IDs they take: 18 for `GITOPS`, 30 for `MESH`, 27 for `ROLLOUT` and 7 for `OBSERV`. It is the binding reading, not a preliminary one. The implementation issues exactly those IDs to those units. If a policy at the implementation base no longer matches a row, the author stops and asks the user before any ID is issued.
- **Rules table (W03-D43, W03-D44, W03-D65).** Each of the four policies states normative rules, so the condition of the Rules table holds for it. Each holds one Rules table directly under the `Requirements` heading, before any other content of the section, with the four common columns, the registered `Status` extension and one row per ID in ascending order. The column names, the IDs and the Level and Status values are the same ASCII text as in the governance policies (W03-D42).
- **Level (W03-D58, W03-D62).** The strongest obligation in the unit governs, read by meaning. A unit under a `Required` or `Disallowed` label or heading is `required`. A unit under `Allowed` is `optional`, unless it states a condition that must hold, which makes it `required`. Elsewhere `required` is the default; `권장` reads `recommended` and `선택` reads `optional`. No wording is changed to fit a Level.
- **Condition (W03-D58, W03-D62).** Condition restates when the rule applies, from the rule's own applicability clause. When the rule states none it reads `Always`, the same ASCII value in every policy; other Condition and Evidence text follows the document's language (W03-D53).
- **Evidence (W03-D62).** Evidence cites, in this order, the first that exists for the rule: the control ID of the policy's own control register that enforces it; the runbook or guide that the policy's `Enforcement` section names, by artifact ID; an existing repository check, looked up in `scripts/validation/registry.json`, `scripts/run-contract-tests.py` or the tree; otherwise the review that judges the rule. No cell names a control, artifact or check that does not exist, no cell copies the text of a control or a runbook, and no cell adds an obligation the rule does not state. Cells are short phrases, not sentences.
- **Review before the flip (W03-D58, W03-D62).** The map of each ID to its unit with its final Level, Condition and Evidence is listed in the Task for the user's review before the commit that sets that policy's record to `adopted`.
- **Prose unchanged (W03-D43).** Three insertions are allowed and no other byte changes: the Rules table, as its lines and the one blank line after it; an item token, at any list depth, as the code span and the one space after it; and a group token, as its own line and the one blank line after it. After exactly those bytes are removed, each policy's body equals its body at the base byte for byte. Lines are not re-wrapped.
- **Anchors.** No existing heading text changes and no heading is added. At `4bcda456` the consumers are six Markdown fragment links, all to the `exceptions` heading of POL-0001, from the Stage 05 README, the four other operations policies and one runbook; no link targets a heading under `Requirements`, and no tracked file other than Markdown names a fragment of these policies. Both kinds are searched again at implementation, and every consumer found keeps resolving.
- **Versions.** Each adopted policy takes one minor version step from its version at the base and the commit date.
- **Decision and handoff rows.** The package commit appends W03-D62 to the SPEC-0161 Task with the user's exact words. The implementation refreshes the state cell of W03-H29 and its ledger entry: fourteen policies adopted, POL-0007 and the gate retirement left to the following package, package 5 after it. No recorded decision row is edited.

Data modeling and storage strategy:

Four registry `state` values change. Four policies, 34,454 bytes together at `4bcda456`, gain 82 definition tokens and 82 table rows; nothing else is stored.

Interfaces and data structures:

- `scripts/validate-markdown-profiles.py`: `POLICY-RULE-COVERAGE` with the amended floor; no other rule changes.
- `tests/test_policy_rule_ids.py`: the six nested-list cases, in a Korean-first synthetic policy as well as an English one.
- `docs/99.templates/registry.json`: `policy_rule_ids.codes`, the `state` of four records.
- The four policies: the Rules table and the definition tokens.

### Failure and Edge Cases

Edge cases and error handling:

- The profile's language check judges plain paragraphs only, so a token paragraph and a table cell draw no language finding in a Korean-first policy.
- The control register is the first H4 group of POL-0001 and POL-0005; the Rules table precedes it and is told apart by its first header cell, `Rule ID`.
- One nested item of POL-0003 is a parenthetical note and one nested item of POL-0004 runs over three lines; each is one nested item and one rule.
- The three items of `CI Governance` in POL-0003 are top-level items without nested items and take their own tokens.
- `scripts/validation/repository/quality.py` scans the policies for commands; if a token changes one of its findings, the author stops and asks the user, and no rule or test is relaxed.
- SPEC-0194 is not implemented at `4bcda456`, so every name of a rule, field and test here comes from its approved text and is re-read in the base before work starts.

Failure modes and fallback or human escalation:

If a policy cannot pass the six rules without rewording prose, if a cell would need a control, artifact or check that does not exist, if a unit's Level, Condition or Evidence cannot be read without adding meaning, or if the units at the base no longer match the binding table, the author stops, leaves that policy `pending` and asks the user; the other policies may proceed. If the amended floor accepts a partly tokened list or an untokened parent that is not a pure label, refuses a tokened parent over untokened nested items, or gives an adopted governance policy a diagnostic, the change is wrong and is fixed before commit. If any document outside the scope gains a diagnostic, or a suite fails, the change is wrong and is fixed before commit. If SPEC-0194 is not implemented in the base or SPEC-0201 has not merged, the author waits.

## Acceptance Criteria

### Criteria

| Criterion ID | Expected Result |
| --- | --- |
| VAL-OPSRULE-001 | `POLICY-RULE-COVERAGE` accepts an untokened parent whose text is exactly `Required`, `Allowed` or `Disallowed` with one colon and whose every nested item carries a token, by a test that fails first and then passes; it still refuses such a label over a partly tokened or an untokened list, an untokened sentence ending in a colon and an untokened `**Required**: x:`, each over tokened nested items, and still accepts a tokened parent over untokened nested items; no other rule of SPEC-0194 changed and the ten governance policies pass. |
| VAL-OPSRULE-002 | Each of the four policies carries the definition tokens the binding table names, 82 in all, and one Rules table, its record is `adopted`, and the six document rules pass on it after failing on the unchanged body; no control row carries a rule ID; POL-0007 is unchanged and `pending`. |
| VAL-OPSRULE-003 | For each policy the body with exactly the defined insertions removed equals the base body; every anchor resolves and the heading slugs are unchanged; the Task lists the map of each ID to its unit with its Level, Condition and Evidence, reviewed before the record flipped; every named control, artifact and check exists; each policy took one minor version step. |
| VAL-OPSRULE-004 | W03-D62, the W03-H29 state and the ledger entry are recorded; validator diagnostics outside the scope are unchanged; the suites, exact-index QA and the commit hooks pass. |

### Evidence Requirements

- Before and after, record the four strict document validators; diagnostics after must equal those before.
- Show the six nested-list tests: the label acceptance failing before the floor is amended and passing after it, the four refusals and the tokened-parent acceptance holding before and after, and the ten governance policies passing the profile check after it.
- For each policy, show the profile check refusing it with its record `adopted` and its body unchanged, then passing after the tokens and table.
- For each policy, remove exactly the inserted bytes the contract defines from the new body and compare the result with the base body; record both hashes.
- Verify the anchors for both kinds of consumer: the strict link validator, with the fragment check of SPEC-0193, for the Markdown fragment links, and a search of every tracked file that is not Markdown for a fragment of these policies; compare the heading slugs of each policy before and after.
- Check every Evidence cell that names a control, an artifact, a validator, a suite or a path against the policy's control register, the tree, `scripts/validation/registry.json` or `scripts/run-contract-tests.py`.
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
| [REQ-0003-FR-0028](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-OPSRULE-001 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Direct positive and negative tests of the amended floor. |
| [REQ-0003-FR-0013](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-OPSRULE-002 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Strict Markdown profile check on each adopted policy; registry check. |
| [REQ-0003-FR-0032](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-OPSRULE-003 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Byte comparison of the stripped bodies; link check; reviewed unit map. |
| [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-OPSRULE-004 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Strict validators over the tree; suites; exact-index QA. |
