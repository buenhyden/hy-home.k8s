---
title: "W03 Policy Rule ID Contract"
version: "1.0.0"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-11-14"
artifact_id: "SPEC-0194"
---

# W03 Policy Rule ID Contract Technical Specification (Spec)

## Overview

This approved change contract is Policy package 2 of handoff W03-H29 of the W03 stage of the external v14.7 execution package, recorded in the [SPEC-0161 Task](../0161-w00-v14-7-delta-intake/tasks/tsk-0001-w00-v14-7-delta-intake.md); SPEC-0187 (package 1) moved `.agents/governance/sdlc.md` to the Policy role. The COMMON-DOC-FORM-1 Policy form already says that `Requirements` holds, for each rule, a stable rule ID, a condition and a required, recommended or optional level (`안정 규칙 ID·조건·필수/권고/선택`), but no grammar, required table or check exists: the two Policy templates carry an optional `Rules` table (Rule, Condition, Evidence) that no policy uses, and none of the fifteen policies (ten on `governance/rule` after SPEC-0187, five on `operation/policy`) carries a rule ID. On 2026-11-13 the user decided the ID grammar `<CODE>-R<NNN>` (W03-D42), the rule unit, the inline ID and the required Rules table with a Level column (W03-D43) and the Status column for retired rules (W03-D44). On 2026-11-14 the user resolved a conflict with the W03 task of the external package, `tasks/TASK-hy-home-k8s-W03.md` (REQ below, by line), with the words `W03 프롬프트에 작성된대로` (as written in the W03 prompt). That resolution is W03-D65, recorded by the SPEC-0193 package commit: the Rules table is conditional content of the Policy role, its condition being that the policy states normative rules (REQ:310, REQ:742); its common columns are Rule ID, Condition, Level and Evidence (REQ:486); and `Status`, which no-reuse retirement needs (REQ:143), is a registered conditional extension with condition, owner, verification, review and removal criteria (REQ:37). This package builds that contract in the registry, its schema, the two templates, the validators and the tests, and registers one code per policy. It assigns no rule ID to any document: package 3 adopts the ten governance policies, package 4 the five operations policies, and package 5 adds the no-reuse check across history. A read of `main` at `de64c58d` found about 285 to 330 rule units in the fifteen policies, which is why adoption is split by document. The design choices this package adds (the adoption gate that keeps the checks green until a document adopts, the home of the code record, the definition position of an inline ID, the coverage floor, the Status values and the fifteen codes) are recorded as W03-D53 with this package's first commit, which copies the user's answers; the number is re-read at commit time. The package merges after SPEC-0187 to SPEC-0193. The [Task](tasks/tsk-0001-w03-policy-rule-id-contract.md) records execution and the [Plan](plan.md) orders the work.

## Strategic Boundaries & Non-goals

- In scope (writer W03, with W05 for validator code): `docs/99.templates/registry.json` (one new top-level section `policy_rule_ids`; one entry of `shared_contract.extensions` for the `Status` column; the `Rules` table, `validation` lists and `consumer_paths` of the `common/template-governance-rule` and `common/template-operation-policy` definitions); `docs/99.templates/contracts/document-profile.schema.json` (the section's shape); `scripts/document_authority.py` (the optional top-level key); `scripts/document_contracts.py` (the loader and the strict registry check); `scripts/validate-markdown-profiles.py` (the document rules); the templates `docs/99.templates/templates/governance/rule.template.md` and `docs/99.templates/templates/operations/policy.template.md` (the `Rules` table and its author prompt); a new `tests/test_policy_rule_ids.py` with its registration in the `document` suite of `scripts/run-contract-tests.py` and in `scripts/validation/registry.json`; `tests/test_common_form_tree.py` (the Policy table constants and headers, the shared column test and the top-level key pin) and any test that pins the list of shared extensions; `tests/test_document_generator.py` (its recorded authoring set, if a generated policy draws a new rule); the Policy sentences of `.agents/governance/document-authoring.md` and `docs/99.templates/README.md`; each edited document's frontmatter `version` and `updated`; in the SPEC-0161 Task the appended W03-D53 row, the refreshed state cell of W03-H29, an evidence row and the frontmatter `version` and `updated`, with the matching W03-H29 entry of the work residue ledger; this package, `docs/03.specs/README.md` and reviewed `.secrets.baseline` entries.
- Not in this package: any rule ID, Rules table or other body change in the fifteen policies, apart from the one Policy sentence of the document authoring policy (packages 3 and 4); the no-reuse check across history (package 5); any section of the shared Policy form, any other form, profile, lifecycle domain or frontmatter key; the `Control Register` tables and the control IDs; the glossary rows TERM-RULE and TERM-CONTROL; the document generator's code; `_workspace/` (read-only input) and `docs/98.archive/`.
- No policy changes its rules, owner or meaning in this package. No push, PR or merge without the user's approval. Open question: none; W03-D53 settles the design choices.

## Contracts

- **Grammar (W03-D42).** A rule ID is `<CODE>-R<NNN>`: the policy's code, the literal `-R` and three digits. A code matches `^[A-Z][A-Z0-9]{1,7}$`, belongs to exactly one policy and is never `PLAT` or `OBS`. Numbers are issued in ascending order from `001` without a gap and are never renumbered, moved to another policy or issued twice until a user-approved new baseline under the Q-07 contract (REQ:143). The IDs, the column names of the Rules table and the Level and Status values are the same ASCII text in English and Korean policies; the Condition and Evidence cells follow the document's language.
- **Code record (W03-D53).** The registry gains an optional top-level section `policy_rule_ids` holding `code_pattern`, `levels` (`required`, `recommended`, `optional`), `reserved_codes` (`PLAT`, `OBS`), `rules_table`, which records the condition of the Rules table, `the policy states normative rules`, and its minimum of one row under that condition (W03-D65), and `codes`, one record per policy with `path`, `code` and `state` (`pending` or `adopted`). The registry is the single machine owner (REQ-0003-FR-0012), and a registry record edits none of the fifteen documents, which a frontmatter key would. This package adds fifteen records, all `pending`, with the codes listed under Data Modeling. A code may change only while its record is `pending`.
- **Rules table (W03-D43, W03-D65).** The Rules table is conditional content of the Policy role (REQ:310, REQ:742), and its condition is `the policy states normative rules`. Its common content is four columns, `Rule ID`, `Condition`, `Level` and `Evidence`: REQ:486 gives a rule its stable ID, condition and level, and REQ:310 and REQ:742 name rule, condition and evidence. In both TemplateDefinitions the `Rules` table of `policy-rules-requirements` holds those four as required columns and `Status` as the one optional column after them, with row identity `Rule ID`; its `minimum_rows` stays 0, because a conditional table is not required of every document, and the minimum of one row is recorded with the condition in `rules_table`. A policy states normative rules when its `Requirements` section holds at least one rule unit: a top-level list item, a table row outside a control register, or an H4 group with content. A policy whose `Requirements` section holds only prose paragraphs therefore counts, for this check, as stating no rule, and the semantic review judges whether such prose states a rule. An adopted policy that does so holds exactly one Rules table under `Requirements`, with the four common columns, the `Status` column and at least one row (`POLICY-RULE-TABLE`). A policy that states no normative rule needs no table and no record; a Rules table that is present is checked in either case. Each `Rule ID` carries the document's code, and the rows ascend from `R001` without a gap or a duplicate (`POLICY-RULE-ID`). `Level` is one of the three registered values (`POLICY-RULE-TABLE`).
- **Status extension (W03-D44, W03-D65).** `Status` is not common content. It is a conditional extension of this repository, registered in `shared_contract.extensions` with the five criteria that REQ:37 requires. Condition: it applies to every Rules table of this repository, because a rule ID is never reused until a user-approved new baseline under the Q-07 contract and a retired rule keeps its row (REQ:143, W03-D42, W03-D44). Owner: the request owner that the other entries of that list name. Verification: `POLICY-RULE-TABLE` in the strict Markdown profile check and `tests/test_policy_rule_ids.py`. Review: when `shared_contract.version` changes and when the Rules table definition changes. Removal: when a shared edition of the Policy form defines rule retirement, when the user ends no-reuse retirement for rule IDs, or at a user-approved new baseline under the Q-07 contract. Its value is `active`, or `retired;` followed by a successor rule ID or `none`; a successor carries a registered code and, in the same document, names another row (`POLICY-RULE-TABLE`).
- **Definition token (W03-D43).** The inline ID is a code span holding one rule ID in a definition position: the first content of a list item, the first content of the first cell of a table row, or a paragraph of its own directly under an H4 heading, where it identifies the whole H4 group. Heading text never carries a token, so every anchor stays. A rule ID anywhere else is a reference and is not counted. Under `Requirements`, each `active` row has exactly one definition token, each definition token has an `active` row, and a `retired` row has none (`POLICY-RULE-INLINE`). Adding a token rewords no prose. `Authority` and `Enforcement` are not read, because their sentences are not rule units.
- **Coverage floor (W03-D43, W03-D53).** In an adopted policy every top-level list item and every table row under `Requirements` begins with a definition token or lies in an H4 group that carries one (`POLICY-RULE-COVERAGE`); the rows of the Rules table and of a control table are exempt. Which unit a rule takes, and whether a paragraph outside every unit is normative, stay judgments of the semantic review in packages 3 and 4. The check is a floor, and its PASS is not a review of meaning.
- **Controls (W03-D42).** A table whose first header cell is `Control` is a control register. Its rows keep their control IDs (`PLAT-001` to `PLAT-006` in POL-0001, `OBS-001` to `OBS-006` in POL-0005), need no rule ID and are not rule units: a control (TERM-CONTROL) is the mechanism that enforces a rule (TERM-RULE). No glossary row changes.
- **Retirement (W03-D44).** A rule that leaves a policy keeps its row with a `retired;` Status and loses its definition token. Because rows stay and numbers have no gap, a number cannot be issued twice inside a document, except by deleting the last row, which only history can show; that case and reuse across history go to package 5.
- **Adoption gate (W03-D53).** While a record is `pending`, its policy must carry no Rules table and no definition token (`POLICY-RULE-ADOPTION`), and no other rule above applies to it. Once the record is `adopted`, every rule applies. An authored policy that states normative rules, or that carries a Rules table, and has no record fails `POLICY-RULE-CODE` (W03-D65). Packages 3 and 4 set one record to `adopted` in the same commit that adds that document's IDs and table, so adoption is whole per document. The package that adopts the last policy removes `state`, `POLICY-RULE-ADOPTION` and their tests in its final source commit, so that the table's condition alone decides and the minimum of one row applies to every policy that states normative rules, never to every policy (W03-D65), as the work lifecycle requires for a one-use check; the W03-H29 row carries that duty.
- **Form and templates.** No section of the shared Policy form changes: its `policy-rules-requirements` content already states the requirement, and the form stays equal to COMMON-DOC-FORM-1 for the cross-repository comparison (W03-H09, W03-H22). The local binding lives in the two TemplateDefinitions and the new section. Each template shows the table with its four common columns, the `Status` extension and one sample row, and the author prompt that made the table optional is replaced by one that states the grammar, the condition under which the table is required and the registration of the code in the same change; the governance prompt is English and the operations prompt Korean.
- **Registry check.** `REGISTRY_POLICY_RULE_CODE` in the strict registry validator refuses a record whose path is not a tracked document of an authored profile of the `policy` role, a repeated path or code, a code outside `code_pattern` or inside `reserved_codes`, and a `levels` list other than the three values; the schema requires `rules_table` with a non-empty condition and a minimum of one.
- **Policy text.** The form paragraph of the document authoring policy and the Policy sentence of the Stage 99 README state the grammar, the conditional table with its condition, the `Status` extension, the definition token and the registered code, and name the registry as the owner of the exact values.
- **Decision and handoff rows.** The package commit appends W03-D53 to the SPEC-0161 Task with the user's exact words and refreshes the state cell of W03-H29 and its ledger entry; no recorded decision row is edited.

## Core Design

[AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) owns the governance view; no component changes and no ADR body changes. The registry stays the single machine owner of document form, and the profile check stays the one reader of a document body.

## Data Modeling & Storage Strategy

One registry section with fifteen records and the table's condition; one entry of `shared_contract.extensions`; two TemplateDefinition tables; no document data. The fifteen codes, each unique and outside the reserved list:

| Policy | Code |
| --- | --- |
| `.agents/governance/agent-execution.md` | `EXEC` |
| `.agents/governance/approval-and-safety.md` | `SAFE` |
| `.agents/governance/context-and-memory.md` | `CTX` |
| `.agents/governance/document-authoring.md` | `AUTHOR` |
| `.agents/governance/document-lifecycle.md` | `DOCLIFE` |
| `.agents/governance/formatting-and-linting.md` | `FMT` |
| `.agents/governance/git.md` | `GIT` |
| `.agents/governance/model-selection.md` | `MODEL` |
| `.agents/governance/quality.md` | `QUAL` |
| `.agents/governance/sdlc.md` | `SDLC` |
| `docs/05.operations/policies/0001-k8s-gitops-operations-policy.md` | `GITOPS` |
| `docs/05.operations/policies/0003-service-mesh-cert-manager-policy.md` | `MESH` |
| `docs/05.operations/policies/0004-rollouts-notifications-headlamp-policy.md` | `ROLLOUT` |
| `docs/05.operations/policies/0005-observability-platform-operations-policy.md` | `OBSERV` |
| `docs/05.operations/policies/0007-app-gitops-onboarding-policy.md` | `ONBOARD` |

## Interfaces & Data Structures

- `docs/99.templates/registry.json` and `document-profile.schema.json`: the `policy_rule_ids` section with `rules_table`, the `Status` entry of `shared_contract.extensions`, and the `Rules` table with four required columns and the optional `Status`; the shape of a table definition does not change.
- `scripts/document_authority.py`: `policy_rule_ids` among the optional top-level keys, absent in a comparison-base registry.
- `scripts/document_contracts.py`: the loaded section, copied to the authored profiles of the `policy` role as the loader copies a twin's tables, and `REGISTRY_POLICY_RULE_CODE`.
- `scripts/validate-markdown-profiles.py`: one function beside the table check that reads visible Markdown only and reports `POLICY-RULE-CODE`, `POLICY-RULE-ADOPTION`, `POLICY-RULE-TABLE`, `POLICY-RULE-ID`, `POLICY-RULE-INLINE` and `POLICY-RULE-COVERAGE`.
- `tests/test_policy_rule_ids.py`: for each rule a passing case and a refused case on synthetic policies, in English and in Korean; a `pending` policy with a table or a token refused; an adopted policy that states no normative rule passing without a table; a Rules table without the `Status` column refused; a control register row without a rule ID passing; a `PLAT-001` cell never read as a rule ID; a reference outside a definition position not counted; a token in a fence or comment not read; each registry refusal.

## Edge Cases & Error Handling

- The generator of SPEC-0192 checks that a generated document draws only recorded authoring rules. If a generated operations policy draws `POLICY-RULE-CODE`, that rule joins the recorded authoring set of `tests/test_document_generator.py`; the generator's code does not change.
- The shared column test of `tests/test_common_form_tree.py` unpacks three columns; it is generalized to any column count, and no assertion is weakened.
- A table headed by the former first key `Rule` is no longer the Rules table; none exists in the fifteen policies.
- A nested list item may carry a definition token; the coverage floor reads top-level items only.
- A renamed policy moves its record's `path` in the same change and keeps its code.
- A policy that states normative rules and is created before the gate is retired registers its code as `adopted` in the same change; `pending` is for the fifteen records of this package.

## Failure Modes & Fallback / Human Escalation

If any existing document gains a diagnostic, the change is wrong and is fixed before commit. If the unit inventory shows a policy whose `Requirements` the coverage floor cannot read without rewording prose, or a shared form section would need an edit, the author stops and asks the user and never relaxes a rule or a test. If SPEC-0187, SPEC-0191, SPEC-0192 or SPEC-0193 is absent from the base, the author waits and asks the user.

## Verification Commands

- Before and after, record the four strict document validators; diagnostics after must equal those before.
- `python3 scripts/run-contract-tests.py --root . --suite document`, `--suite document-lifecycle`, `--suite agent-governance`, `--suite validation-routing`; the new module and the changed Policy table tests fail first, then pass.
- `python3 scripts/validate-document-contract-registry.py --root .`; `python3 scripts/validate-affected-surfaces.py --root .`; `python3 scripts/validation/repository/quality.py --root .`; markdownlint over the edited Markdown; `ruff check scripts tests`; `python3 scripts/qa.py staged` and the commit hooks on the exact index; `graphify update .` after the code change.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-RULEID-001 | The registry carries `policy_rule_ids` with the grammar, the three levels, the reserved codes and fifteen `pending` records with unique codes; the schema, the authority guard, the loader and `REGISTRY_POLICY_RULE_CODE` match the contract; the registry records the table's condition and its minimum under that condition and registers the `Status` extension with its five criteria; both TemplateDefinitions and both templates carry the Rules table with four required columns and the optional `Status`; the tests fail first and then pass. |
| VAL-RULEID-002 | The six document rules match the contract, each with a passing and a refused case in English and Korean, including the adoption gate, the control register exemption and the reference and fence cases; the new module runs in the `document` suite that Stage 99 and validator changes select. |
| VAL-RULEID-003 | The policy texts are updated; W03-D53, the W03-H29 state and the ledger entry are recorded; the Task records the unit inventory of the fifteen policies; no policy body gained a rule ID or a table; validator diagnostics over the tree are unchanged; exact-index QA and the commit hooks pass. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0012](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-RULEID-001 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Registry check and schema tests; template parity. |
| [REQ-0003-FR-0028](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-RULEID-002 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Direct positive and negative tests for each rule. |
| [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-RULEID-003 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Strict validators over the tree; exact-index QA. |
