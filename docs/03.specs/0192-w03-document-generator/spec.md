---
title: "W03 Document Generator"
version: "1.0.0"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-11-14"
artifact_id: "SPEC-0192"
---

# W03 Document Generator Technical Specification (Spec)

## Overview

This approved change contract closes handoff W03-H27 of the W03 stage of the external v14.7 execution package. The W03 task names the consumer chain Registry, Schema, Template, Generator, Parser, Validator, Tests and CI and asks for a real generate, parse and validate round trip. The repository has every link except the generator: no script fills the template markers and forms are copied by hand. On 2026-11-13 the user decided to build a document generator that creates a new document from the registry and its template and fills the frontmatter placeholders, after the `layer` removal (W03-D24, which resolves W03-H04). SPEC-0184 removed `layer` and is merged, so the templates have their settled frontmatter. On the same day the user settled the ten design choices of this package by adopting the recommended answer to each (W03-D48, recorded in the SPEC-0161 Task with this package's commit). This package adds one command, `scripts/document-generator.py`, which reads the Stage 99 registry and the selected profile's template, writes one new document with the shared value markers filled, and refuses every request that the registry or the identity rules do not admit. Its tests generate a document for every profile the generator serves, load the result with the one frontmatter loader and validate it with the strict profile check. The [Task](tasks/tsk-0001-w03-document-generator.md) records execution and the [Plan](plan.md) orders the work.

## Strategic Boundaries & Non-goals

- In scope (writer W03, with W05 for the validation consumers): the new `scripts/document-generator.py` and `tests/test_document_generator.py`; `scripts/run-contract-tests.py` (the test module joins one suite) and `scripts/validation/registry.json` (the generator and its test get exact routes on the surface that selects that suite, and the generator joins the exclusion list of the generic `scripts` surface route, as `frontmatter_yaml.py` does, because a path that two surfaces match is refused as `SURFACE-PATH-AMBIGUOUS`); `scripts/document_lifecycle.py` (the creation-state derivation moves into one public function, with no behavior change) with its tests; `scripts/validate-markdown-profiles.py` (`expected_artifact_id` gains the reference pack anchors) with its test; `docs/99.templates/registry.json` (the `version` entry of `frontmatter_keys`, its lifecycle sentence only); the sentences that name the generator in `.agents/governance/document-authoring.md`, `docs/99.templates/README.md` (Create and Review, step 2) and `scripts/README.md` (one row); each edited document's frontmatter `version` and `updated`; in the SPEC-0161 Task the appended W03-D48 row, the evidence rows, the row that closes W03-H27 and one new handoff row, recorded with this package's commit, for the repair of the missing `sdlc/requirement` creation state, and, once SPEC-0191 has merged, the matching entries of `docs/03.specs/work-residue-ledger.json`; this package, the Stage 03 README and reviewed `.secrets.baseline` entries.
- Not in this package: Q-07 renumbering and any number allocation or number search (W03-D30); the design, schema, script and checks of the work residue ledger (W03-H30); any change to a template, a profile, a lifecycle domain or the frontmatter schema, including the repair of the `requirement` domain, which the new handoff row carries to its own package; any existing document's content; provider-native projections, which stay checked consumers; README index rows, `Archived Lineage` rows and sibling files of a generated document; any rule that makes the generator mandatory.
- No push, PR or merge without the user's approval. Open question: none.

## Contracts

- **Command.** `python3 scripts/document-generator.py --root <repository> --profile <profile id> --title <title> --owner <owner> <target path>` creates exactly one file and prints one line that names its path, profile, identity, parent and status. It exits 0 after a write and 2 after a refusal. A refusal prints one line with its reason ID, writes no file and creates no directory.
- **Sources.** The generator reads the registry through `document_contracts.load_registry` and the template that the selected profile names in `template_source`. It restates no route, key list, status, identity or parent rule: the route comes from `classify_path`, the identity from `expected_artifact_id`, the parent from `direct_parent`, the creation states and the reserved identities from `document_lifecycle`, and the frontmatter rules from the profile check.
- **Generable profiles (W03-D48).** A profile is generable when its mode is not `template`, it names a Markdown template, and the five shared value markers are the only placeholders in that template's frontmatter. A template without frontmatter qualifies, which keeps the legal frontmatter-omitted case (`common/folder-agents-guide`) in the round trip. Every other profile is refused: template-mode profiles, profiles without a template, the native skill package, whose `name` and `description` placeholders and package obligations belong to agent governance, and the Claude and Codex runtime forms, which use the native double-underscore grammar and take their values from the provider bindings.
- **Fill.** The TITLE and OWNER markers take the inputs, UPDATED takes the current date in Asia/Seoul (the clock the profile check uses), ARTIFACT_ID takes the path-derived identity and PARENT_ID the path-derived direct parent identity. Each marker is replaced wherever it occurs in the template, because an authored document contains none of them. Every other byte of the template is kept: the author guidance comments, the starter H1, the sample table rows, the profile-specific markers, and the template's own `version` and `status` values (W03-D48).
- **Identity (W03-D48).** The generator allocates no number: the caller writes it in the target path and the path fixes the identity. A request is refused when a required identity cannot be derived, when a current document at another path owns it, or when it equals or extends an identity reserved in an `Archived Lineage`, the predicate of `LIFECYCLE-IDENTITY-REUSE`. Nothing is renumbered and no retired number is reopened (W03-D30). So that the three reference pack anchors derive an identity, `expected_artifact_id` returns the category prefix and the pack folder number for them, which also gives those anchors the path correspondence check they lack today.
- **Parent (W03-D48).** A Plan or a Task is refused when the direct parent file that `direct_parent` names is absent, so no generated document starts as an orphan.
- **Status (W03-D48).** There is no status input. The document keeps the template's status value, and the request is refused when that value is not a creation state of the profile's lifecycle domain or when the domain yields no creation state. A router README keeps its `active` constant.
- **Refusals.** An unknown or non-generable profile (`GENERATOR-PROFILE`); a target path that is absolute, leaves the root, or that the registry routes to another profile or to none (`GENERATOR-ROUTE`); an existing target of any kind, with no overwrite option (`GENERATOR-OCCUPIED`); the identity, parent and status cases above (`GENERATOR-IDENTITY`, `GENERATOR-PARENT`, `GENERATOR-STATUS`); an empty title or owner, or one that holds a double quote, a backslash, a line break, a control character or a double-braced marker (`GENERATOR-INPUT`); and a produced text that fails the output check (`GENERATOR-OUTPUT`).
- **Output check.** Before writing, the generator loads the produced frontmatter with `frontmatter_yaml.load_frontmatter`, requires that no shared marker remains, and runs the profile check's frontmatter and identity rules on the produced text; any finding is a refusal. The file is created exclusively, so an existing or concurrently created file is never overwritten.
- **Fresh document.** On a generated document the strict profile check reports no `FM-` rule and no identity rule, and the lifecycle creation rule admits its status. What remains is authoring: author prompts, the starter H1, empty sections and sample rows stay refused until the author replaces them. A generated file is a starting point, never a finished document.
- **Chain (W03-D48).** The round-trip test module belongs to the `document` suite and the generator and its test are routed with the document readers, so a change to the registry, a template, the loader, the profile check or the generator reruns the round trip in the affected and staged lanes. The generator is carved out of the generic `scripts` route so that exactly one surface owns it; without the carve-out its path is `SURFACE-PATH-AMBIGUOUS`. The lifecycle reader keeps its own surface, which already selects the `document` and `document-lifecycle` suites. Hosted CI keeps its metadata and style role (REQ-0003-FR-0017).
- **Policy text (W03-D48).** The document authoring policy and the Stage 99 README name the generator as the way to start a document from its form. Copying a form by hand stays valid and the validators stay the gate.
- **Residue records.** The W03-H27 closure and the new repair handoff take the form that is current when this package merges. If SPEC-0191 has merged, each is a live `Residue Handoff` row in the SPEC-0161 Task with its entry in `docs/03.specs/work-residue-ledger.json`, written in the same change by the ledger's own rules. If it has not, each is an appended handoff row and SPEC-0191's seed takes both from current truth.
- **Key table (W03-D48).** The registry `version` entry says a document starts at `1.0.0`; the authoring policy, the Stage 99 README and every template that carries a version say `0.1.0`, raised to `1.0.0` at the first stable approval. The entry's sentence is corrected to match, and the generator keeps the template's `0.1.0`.

## Core Design

[AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) owns the governance view. Its plane "Document machine contract and forms" lists the template consumers of the Stage 99 Registry, and the generator is one more consumer: it owns no contract and no state. The same description keeps native adapter projections as checked consumers with no provider generator, which is why the runtime forms are refused. No AD or ADR text changes. The flow is fixed: resolve the profile, check the route, derive the identity and the parent, check identity use and reservation, check the creation state, fill the markers, check the output, create the file. W03-D22 holds without a special case, because the decision template carries no `layer` and a generated ADR therefore carries none. W03-D23 holds: `title` is filled from the input and the H1 stays the author's.

## Data Modeling & Storage Strategy

The generator stores nothing: no state file, cache, ledger, index or committed view. Its only output is the one new document. A simulation at `8231f782` over the 87 profiles found 39 template-mode profiles, 9 without a template and 39 with one; of those 39, 35 are generable under the rule above and 4 are refused. These counts are observations and no part of the contract: later packages change the forms, and the tests compute both sets from the registry.

## Interfaces & Data Structures

- `scripts/document-generator.py`: `main(argv)` and one function that returns the produced text or raises a refusal carrying its reason ID. The function takes the date as a parameter so that tests fix it; the command line has no date option.
- Reused without change: `load_registry`, `classify_path`, `direct_parent` and `read_repository_text` of `document_contracts`; `load_frontmatter`; `validate_document_text` and `current_artifact_identities` of the profile check, whose hyphenated file `scripts/validate-markdown-profiles.py` the generator loads through `importlib`, as `scripts/document-backlinks.py` loads the link validator; `lineage_retired_identities` and `artifact_identity_reuse_diagnostics` of `document_lifecycle`.
- Changed: `expected_artifact_id`, for the pack anchors only (W03-D48).
- Changed: `scripts/document_lifecycle.py`. The creation states are derived inline in the private `_create_diagnostics`, from a domain's `initial_states` and transitions, and only for snapshot documents. That derivation moves into one public function that `_create_diagnostics` and the generator both call. It is a refactor of a protected reader: no diagnostic changes, the existing lifecycle tests pass unchanged, and one direct test covers the function.
- Round-trip tests in `tests/test_document_generator.py`: one sample target path per generable profile, with a completeness assertion that the sample set equals the generable set computed from the registry; for each sample the loaded title, owner, updated date, type, status, identity and parent equal the expected values, the output equals the template with only the shared markers replaced, the profile check reports no `FM-` or identity rule, and every remaining rule belongs to the recorded authoring set.
- Negative tests in the same module: one per refusal reason, each asserting the reason ID, exit code 2 and an unchanged tree; a template with a duplicate key, an injected impossible date, a template whose status is no creation state, a profile that requires a key its template lacks and a template that carries a key its profile does not list are each refused.

## Edge Cases & Error Handling

- A package folder that does not exist is created with the file; after a refusal no folder is left behind.
- A Spec, Plan and Task are generated in that order, because the parent must exist (W03-D48).
- An identity that exists only in the Git comparison base, because its document is deleted in the working tree, is not seen by the generator, which reads the current tree; the staged lifecycle check still refuses it with `LIFECYCLE-IDENTITY-REUSE`.
- At `8231f782` the `requirement` lifecycle domain yields no creation state, because `in-review` to `draft` gives `draft` an inbound edge, and the lifecycle creation rule refuses every new Requirement. The generator refuses that profile by its status rule (W03-D48), the new handoff row carries the repair of the domain, and the generator serves the profile without a code change once the registry admits a creation state.
- A Task with several rows drops its frontmatter `status` line by the authoring policy; that edit is the author's and follows generation.
- Without `ruamel.yaml` the loader import fails with its install command; the generator fails and never falls back to another parser.

## Failure Modes & Fallback / Human Escalation

If a generated document draws an `FM-` or identity finding, the generator, the template or the registry is wrong: the author stops and fixes the owner and never relaxes the output check or a test. If the work needs a change to a template, a profile, a lifecycle domain, the schema, or a validator or reader beyond `expected_artifact_id` and the creation-state extraction, or if any existing document gains a diagnostic, the author stops and asks the user.

## Verification Commands

- Before and after, record the four strict document validators over the tree; diagnostics after must equal those before.
- `python3 scripts/run-contract-tests.py --root . --suite document`, `--suite document-lifecycle` and `--suite validation-routing`.
- `python3 scripts/validate-affected-surfaces.py --root .`.
- One manual run of the command into a temporary copy of the tree for a Spec, a Plan and a Task, with the printed lines recorded in the Task.
- `python3 scripts/validation/repository/quality.py --root .`; markdownlint over the edited Markdown; `ruff check scripts tests`; `python3 scripts/qa.py staged` and the commit hooks on the exact index.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-GEN-001 | The command creates one document from the registry profile and its template with the five shared markers filled and every other byte kept; for every generable profile the round-trip tests generate, load and validate with no `FM-` rule, no identity rule and an admitted creation status; every other profile is refused; the module runs in the `document` suite that Stage 99 changes select. |
| VAL-GEN-002 | Identity and parent come from the target path through the existing rules; a used identity, a reserved identity or its extension, an underivable identity, an absent parent and an occupied path are each refused with nothing written; the pack anchors derive their identity in the profile check; no number is allocated or renumbered and no existing document changes. |
| VAL-GEN-003 | Each refusal reason has a direct negative test that fails first and then passes, including a duplicate key, an impossible date, a status outside the creation states and a template that disagrees with its profile; the policy texts and the key table sentence are updated; validator diagnostics over the tree are unchanged and the lifecycle suites pass unchanged after the creation-state extraction; exact-index QA and the commit hooks pass. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0013](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-GEN-001 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Round-trip tests per generable profile; suite selection. |
| [REQ-0003-FR-0023](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-GEN-002 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Identity, parent and occupied-path tests; tree comparison before and after. |
| [REQ-0003-FR-0028](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-GEN-003 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Direct negative tests; strict validators over the tree; exact-index QA. |
