---
title: "W03 Frontmatter Key Contract"
version: "1.0.0"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0181"
---

# W03 Frontmatter Key Contract Technical Specification (Spec)

## Overview

This approved change contract closes handoffs W03-H07, W03-H14 and W03-H17 of the W03 stage of the external v14.7 execution package, and fixes two differences that the 2026-11-13 W00 to W03 conformance audit found. The W03 task asks for every real frontmatter key to be judged in one table with `document_type, key, purpose, type, requiredness, allowed_values, authoring_owner, derived_from, duplicate_source, consumer_paths, lifecycle, migration, positive_test, negative_test`, for a TemplateDefinition on every real template, and for the YAML and JSON Schema dialect to be recorded with the format and date split. W03-H07 decided that the registry owns one description per key and that the key set and grammar stay with each profile and `frontmatter.schema.json`. The audit also found that the seven WGOV-CORE extensions in `shared_contract` hold `unverified` for owner, verification, review and removal and a copy of their name as condition, which the requirement forbids for an extension (W03 line 18), and that `.agents/governance/document-authoring.md` still describes the Policy `Lifecycle Traceability` table as kept under Related Documents, which SPEC-0175 changed. The full TemplateDefinition record of W03-H15 needs heading content that the nine local roles get only from their forms (W03-D26) and that the six SDLC templates get in phase 3 (W03-H13), so this package hands W03-H15 to those packages instead of inventing that content. The user's direct 2026-11-13 answers W03-D25 to W03-D31 (the GOV-06 ledger, local forms, Policy role and rule IDs, CI-SCOPE staging, YAML 1.2.2, Q-07 renumbering only after all `docs/` work with current numbering kept until then, and keeping accurate pointer lines) and the follow-up handoff rows are recorded in the [SPEC-0161 Task](../0161-w00-v14-7-delta-intake/tasks/tsk-0001-w00-v14-7-delta-intake.md) with this package's first commit; W03-D22 to W03-D24 are already there. The [Task](tasks/tsk-0001-w03-frontmatter-key-contract.md), created in the same first commit, records execution and the [Plan](plan.md) orders the work.

## Strategic Boundaries & Non-goals

- In scope (writer W03, with W05 for validator code): `docs/99.templates/registry.json` (`frontmatter_keys`, `frontmatter_dialect`, the Codex template twin and its binding, and the WGOV-CORE extension `condition`, `owner`, `verification`, `review` and `removal`); `docs/99.templates/contracts/document-profile.schema.json` (the new sections); `scripts/document_authority.py` (admitting the two optional top-level keys); `scripts/document_contracts.py` (typed loading with defaults for a registry without the new sections, the registry checks and the key-table projection); `tests/test_common_form_tree.py`, `tests/test_shared_contract_binding.py`, `tests/test_document_terminal_contract.py` and a new key-contract test module registered in a suite; the forms paragraph and the frontmatter paragraph of `.agents/governance/document-authoring.md` and one sentence of `docs/99.templates/README.md`; in the SPEC-0161 Task the decision rows W03-D25 to W03-D31, the handoff rows for the follow-up packages, the conformance-audit rows, evidence rows and the frontmatter `version` and `updated` (appended rows only, carrying the user's recorded answers and the audits' findings with owner and resume condition, verified by the strict Task validators and the staged lifecycle check); each edited document's frontmatter `version` and `updated`; this package, the Stage 03 README and reviewed `.secrets.baseline` entries.
- Not in this package: the full TemplateDefinition record (W03-H15, handed to the local-forms package and phase 3); removing `layer` (W03-D22), the YAML 1.2.2 loaders (W03-D29), the generator (W03-D24), the local forms (W03-D26), the Policy work (W03-D27), the ledger (W03-D25) and the explained empty sections (W03-H18), each its own package; any document or template body; `shared_contract` `approved_by`, `approved_at`, `effective_from`, `scope`, `migration` and `rollback`, which stay `unverified` because no record states them (W03-D05; document authoring policy); phase 3.
- No push, PR or merge without the user's approval, which is standing for this work (2026-11-13). Open question: none.

## Contracts

- **Key descriptions.** The registry gains `frontmatter_keys`, one entry per key that any profile requires, allows, forbids or orders (22 today: `title`, `version`, `type`, `status`, `owner`, `updated`, `artifact_id`, `supersedes`, `superseded_by`, `layer`, `cancellation`, `description`, `parent_ids`, `name`, `resolved_at`, `metadata`, `disable-model-invocation`, `model`, `effort`, `tools`, `argument-hint`, `allowed-tools`). Each entry holds `key`, `purpose`, `data_type`, `condition` (when the key is required or allowed beyond the profile lists, for example `cancellation` on a cancelled Task, `resolved_at` on a resolved incident, `superseded_by` on a superseded document; empty otherwise), `authoring_owner` (`author`, `tool` or `derived`), `derived_from` (empty when authored), `duplicate_source` (the other place the same fact lives, or empty), `consumer_paths` (at least one existing file that reads the key: the profile check `scripts/validate-markdown-profiles.py` reads every governed key, and a native key names the repository file that checks it, such as `scripts/validate-agent-governance.py`), `lifecycle`, `migration`, and `positive_test` and `negative_test` (a test module path and test name). `title` names the H1 as its partly duplicate source (W03-D23); `layer` names the stage folder as its duplicate source, W03-D22 as its migration and `TEMPLATE_OMITTED_KEYS` in `scripts/validate-document-contract-registry.py` as a consumer that its removal package changes.
- **Key tests.** Where no test exercises a key today, the new test module adds one positive and one negative case through the profile or agent-governance check, so every entry names both tests. The registry check confirms that each named module and test exist and that the test's source contains the key; it does not claim more than that.
- **Per-type table.** The fourteen-column table of the W03 task is derived, not stored: for each profile, `requiredness` comes from the profile's frontmatter lists and the entry's `condition`, `allowed_values` from the profile constants and the schema grammar for the shared keys, from the provider binding for `model`, `effort` and `tools`, and as provider-owned free text for the other native keys, and the other columns from `frontmatter_keys`. One function in `scripts/document_contracts.py` returns it, and a test checks that it covers every profile and key.
- **Registry checks.** The registry check refuses a key used by a profile without an entry, an entry no profile uses, a duplicate entry, an empty or missing consumer path, and a test reference whose module, test name or key literal is missing. A comparison-base registry without the new sections still loads.
- **Dialect.** The registry gains `frontmatter_dialect`: current YAML 1.1 through PyYAML 6, listing each of the four loaders and its behavior (`scripts/validate-markdown-profiles.py` and `scripts/document_lifecycle.py`: `SafeLoader` with the timestamp resolver removed and duplicate keys refused; `scripts/validate-agent-governance.py`: duplicate keys refused, timestamps resolved; `scripts/validate-links-and-owners.py`: plain `safe_load`); target YAML 1.2.2 (W03-D29) with no check asserting it; JSON Schema Draft 2020-12 with `format` treated as an annotation without assertion; dates checked by `FM-DATE`.
- **Codex template (W03-H14).** A template-mode twin of `common/codex-agent-binding` for `docs/99.templates/templates/runtime/codex-agent.template.toml`, with frontmatter mode `absent` and placeholder policy `template-only`, joins the `provider-native` role with a TemplateDefinition and no tables, and `common/codex-agent-binding` gets the role.
- **WGOV-CORE extensions.** Each of the seven extensions gets a `condition` that states when the extension applies, the recorded contract owner `buenhyden` (`shared_contract.owner`) as `owner`, and `verification`, `review` and `removal` that name the check or review that confirms it, when it is reviewed and the event that ends it. The proposed texts are listed in the Task for the user's acceptance. The registry check refuses `unverified` in an extension's condition, owner, verification, review or removal, and the binding test changes from pinning `unverified` to pinning the new values.
- **Policy text.** The forms paragraph of `document-authoring.md` drops the stale Policy `Lifecycle Traceability` clause; its frontmatter paragraph says that `frontmatter_keys` owns key meaning and `frontmatter_dialect` the dialect; `docs/99.templates/README.md` gains one Korean sentence pointing to both.

## Core Design

[AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) owns the governance view; no component changes. The registry stays the single machine owner of document form, template definition and key meaning ([ADR-0033](../../02.architecture/decisions/0033-common-document-contract-v9.md) as amended by [ADR-0059](../../02.architecture/decisions/0059-registry-common-form-model.md)); no ADR body changes.

## Data Modeling & Storage Strategy

Registry data: 22 key entries, one dialect object, one template twin and two bindings, seven extensions. Code: the key-table projection, the authority admission and the registry checks.

## Interfaces & Data Structures

- `scripts/document_authority.py`: `OPTIONAL_TOP_LEVEL_KEYS` gains `frontmatter_keys` and `frontmatter_dialect`; `test_authority_admits_exactly_the_three_new_optional_keys` follows.
- `scripts/document_contracts.py`: the key-table projection; registry checks for `frontmatter_keys`, `frontmatter_dialect` and extension fields; defaults when the sections are absent.
- Tests: key coverage both ways, a missing and a stray entry, a missing consumer path and test reference, a test reference without the key literal, `unverified` in an extension field, the per-type table covering every profile, the Codex twin bound, a base registry without the sections loading, and a positive and a negative case for each key that had none.

## Edge Cases & Error Handling

- Native keys are owned by the provider format; their entries say so and name the repository file that checks them.
- A profile with frontmatter mode `absent` uses no key and adds no entry.

## Failure Modes & Fallback / Human Escalation

If a key's consumer cannot be found, the author stops and asks the user rather than leaving the entry empty. If any document gains a diagnostic, the change is wrong and is fixed before commit.

## Verification Commands

- Before and after, record the four strict document validators; diagnostics after must equal those before.
- `python3 scripts/run-contract-tests.py --root . --suite document`, `--suite document-lifecycle`, `--suite agent-governance`, `--suite validation-routing`.
- `python3 scripts/validation/repository/quality.py --root .`; markdownlint over the edited Markdown; `ruff check scripts tests`; `python3 scripts/qa.py staged` and the commit hooks on the exact index.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-KEYS-001 | `frontmatter_keys` covers every used key with every field and both tests, the per-type table is derived and tested, `frontmatter_dialect` records the four loaders and the target, the Codex twin has its definition, and the registry checks refuse the listed faults; tests fail first and then pass. |
| VAL-KEYS-002 | The seven WGOV-CORE extensions hold the accepted texts, the policy texts are updated, validator diagnostics over the tree are unchanged, and exact-index QA and the commit hooks pass. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0012](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-KEYS-001 | [ADR-0059](../../02.architecture/decisions/0059-registry-common-form-model.md) | Registry, projection and key tests. |
| [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-KEYS-002 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Strict validators over the tree; exact-index QA. |
