---
title: "W03 Frontmatter Key Contract Plan"
version: "1.0.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0181-PLAN-0001"
parent_ids: ["SPEC-0181"]
---

# W03 Frontmatter Key Contract Implementation Plan

## Global Constraints

This approved work order follows the [approved Spec](spec.md) and inherits all of its boundaries. It adds two constraints: no document or template body changes other than the two policy texts, the SPEC-0161 Task rows named in the Spec and this package's README entry, and the diagnostics of the four strict document validators over the tree are equal before and after.

## Overview

Admit and add `frontmatter_keys` and `frontmatter_dialect` to the registry and schema; derive the per-type key table and test it; add the missing key tests; give the Codex agent template a twin and definition; replace the `unverified` WGOV-CORE extension fields with accepted texts; update the policy texts; record W03-D25 to W03-D31, the follow-up handoff rows and the conformance-audit rows. [Task 0001](tasks/tsk-0001-w03-frontmatter-key-contract.md) owns execution and evidence.

## Context

SPEC-0179 added TemplateDefinitions for the templates without a common role and SPEC-0180 reserves retired identities. A read of the tree found:

- 22 frontmatter keys across the registry profiles, 13 shared and 9 provider-native, with no stored meaning, author, derivation or consumer;
- a registry authority guard that admits only the current optional top-level keys;
- template definitions that store 10 of the package schema's fields; the rest needs the local forms (W03-D26) and phase 3 (W03-H13) for its heading content;
- keys without a key-specific test (`supersedes`, `superseded_by`'s negative case, `argument-hint`, `allowed-tools` and others the implementation lists);
- the Codex agent template named only by a native profile, with no template twin;
- seven WGOV-CORE extensions holding `unverified` owner, verification, review and removal and a copy of their name as condition, pinned by `tests/test_shared_contract_binding.py`; six `shared_contract` fields holding `unverified`, of which no record states any;
- four frontmatter loaders on PyYAML 6 with different duplicate-key and timestamp behavior, and a schema on Draft 2020-12, with no recorded dialect;
- a stale Policy sentence in the document authoring policy.

## Goals & In-Scope

- Registry and schema: `frontmatter_keys`, `frontmatter_dialect`, the Codex twin and bindings, the seven extensions.
- Code and tests: the authority admission, the key-table projection, the registry checks, the missing key tests and their updates.
- Policy: the two texts.
- Tracking: in the SPEC-0161 Task, with the package commit, W03-D25 to W03-D31, handoff rows for the follow-up packages (the `layer` removal, the YAML 1.2.2 loaders, the generator, the explained empty sections, the local forms with W03-H15, the Policy work and the ledger), the conformance-audit rows and evidence rows.

## Non-Goals & Out-of-Scope

- The full TemplateDefinition record (W03-H15), the `layer` removal, the YAML 1.2.2 loaders, the generator, the explained empty sections, the local forms, the Policy work, the ledger and phase 3.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-KEYS-001](spec.md#success-criteria--verification-plan) | Authority admission, key entries, dialect, key-table projection, Codex twin, registry checks and tests. | Approved Spec and Plan. | [Task 0001](tasks/tsk-0001-w03-frontmatter-key-contract.md) | Failing tests first, then passing; strict registry check; any moved baseline line in its own commit first. |
| WORK-002 | [VAL-KEYS-002](spec.md#success-criteria--verification-plan) | Extension texts; policy texts; regression and exact-index QA. | WORK-001. | [Task 0001](tasks/tsk-0001-w03-frontmatter-key-contract.md) | Strict validators, suites, quality gate, markdownlint, ruff, staged QA and hooks. |

## Verification Plan

- Record the four strict document validators before any change.
- Show each changed test failing before its change, then passing.
- Record in the Task, per key, the consumer and test references and the tests added; and the proposed extension texts, which the acceptance question shows the user.
- Commit order: the package commit with this Task, this package's entry in `docs/03.specs/README.md` and the SPEC-0161 rows; then `.secrets.baseline` changes alone; then the implementation with the Task evidence. Run the staged lifecycle check before each commit and `graphify update .` after the code change.
- Architecture compliance: AD-0006, ADR-0033 and ADR-0059 bodies unchanged.
- Record the risk class (`medium`: registry, schema, code and tests; no permission, trigger, hook or workflow) and the core-diff checklist.

## Risks & Mitigations

Risks use the risk-report scale (likelihood Likely, Possible or Unlikely; impact Severe, Moderate or Minor), rated from the pre-approval review's evidence.

- **The registry stops loading when the new sections are added.** Likely, Moderate: HIGH, mitigate; it blocks the implementation commit. Owner: W05 code. The review reproduced the authority refusal; the authority admission, the schema and the typed defaults change together, and a base registry without the sections is tested. Review cue: the registry tests. Signal that raises it: a `REGISTRY_TOP_LEVEL` diagnostic. Rollback: revert the implementation commit.
- **Pinned `unverified` tests fail.** Likely, Minor: MEDIUM, mitigate. Owner: W03 author. `tests/test_shared_contract_binding.py` is in scope and changes with the values. Review cue: the binding test. Signal that raises it: a failing pin. Rollback: revert the implementation commit.
- **Agent-written extension texts are taken as recorded facts.** Possible, Moderate: MEDIUM, mitigate. Owner: W03 author. The texts are proposals the user accepts in the criterion question; the approval facts and `scope`, `migration` and `rollback` stay `unverified`. Review cue: the acceptance question. Signal that raises it: a value without a source. Rollback: revert the implementation commit.
- **Key consumers and tests drift from the code.** Possible, Minor: LOW, monitor. Owner: W05 code. The registry check confirms each path, module, test name and key literal. Review cue: a registry diagnostic. Signal that raises it: a renamed test. Rollback: correct the entry.
- **The TOML twin breaks a Markdown-only check.** Unlikely, Minor: LOW, monitor. Owner: W05 code. The review simulated the twin with every strict validator passing and four expected test updates. Review cue: the profile tests. Signal that raises it: a template-mode check reading the TOML. Rollback: drop the twin and record the exclusion.

## Completion Criteria

Both criteria need PASS evidence, no unresolved required failure and the operator's acceptance.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| Frontmatter key meaning and dialect | [Document authoring policy](../../../.agents/governance/document-authoring.md) | Frontmatter paragraph; machine data in `docs/99.templates/registry.json` |
