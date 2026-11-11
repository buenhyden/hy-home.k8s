---
title: "Shared Edition Consistency"
version: "1.0.0"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-11-11"
layer: "specs"
artifact_id: "SPEC-0157"
---

# Shared Edition Consistency Technical Specification (Spec)

## Overview

This approved change contract completes stage W01 of the externally supplied v14.2 execution package, which stays git-ignored evidence and never repository authority. Completed SPEC-0156 recorded W01's rejected clauses, but a later re-audit against the full W01 prompt ran its violation tests on a disposable copy of the repository. Projection drift and an adopted shared contract without approval or with a draft edition were refused. A rule document naming a different WGOV-CORE edition from the one the Stage 99 registry adopts was not refused by any document validator. W01's acceptance condition requires that a consumer on another edition is never shown as adopted. This change adds that check to the existing registry validator. W00 is closed by completed SPEC-0158. The [Plan](plan.md) orders the work; [Task 0001](tasks/tsk-0001-shared-edition-consistency.md) records the re-audit, execution and acceptance.

## Strategic Boundaries & Non-goals

- Scope is one pure function in `scripts/document_contracts.py`, its call in `scripts/validate-document-contract-registry.py`, its regression tests in `tests/test_shared_contract_binding.py`, one sentence in `.agents/governance/document-lifecycle.md` stating the rule with that file's patch `version` bump (2.5.0 to 2.5.1) and `updated` date, and this package with its Stage 03 README entry and REQ-0003 back-link.
- The check reads only current rule surfaces: tracked Markdown under `.agents/`, `docs/99.templates/`, `.claude/` and `.codex/`. Spec packages, the archive, dated references and `CHANGELOG.md` are history and are never checked or rewritten.
- No change to the registry schema, the shared contract binding, its stages or approval fields, provider settings or hosted workflows, and no governance policy change beyond that one sentence, which states the rule the validator enforces and adds no other obligation. The current documents already name the adopted edition and need no other edit.
- No new ledger, gate, lane or cross-repository check; Project-Template stays outside this workspace's boundary.
- Open question: none.

## Contracts

- When the registry has a `shared_contract`, every edition mention of its `contract_id` on a current rule surface must equal its `version`. Recognized forms are `WGOV-CORE 3.0.0` and `WGOV-CORE / 3.0.0`, with or without code formatting, including pre-release suffixes.
- A mismatch fails the validator with rule `REGISTRY_SHARED_EDITION_MISMATCH`, naming the path, line, expected edition and found edition; it is never a warning or a skip.
- Without a `shared_contract`, the check does nothing. A mention of the contract without an edition is not a mismatch.
- Existing diagnostics, exit codes and the PASS summary stay unchanged for a consistent tree.

## Core Design

[AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) owns the governance system view; this change conforms and changes no architecture. A pure function in `scripts/document_contracts.py` takes the registry's contract ID and version and a mapping of path to text, and returns mismatch diagnostics. The validator's `main()` calls it after loading the registry, with the rule-surface files listed by the existing `enumerate_tracked_regular_paths` and read by the existing bounded `read_repository_text`. This keeps the comparison testable without Git and the validator's command line unchanged. The lifecycle policy names the rule beside its existing statement that the shared WGOV-CORE edition stays intact, so the policy and the validator agree.

## Data Modeling & Storage Strategy

No stored data changes. The registry's `shared_contract.contract_id` and `version` are read only.

## Interfaces & Data Structures

The validator's command line, modes and output format are unchanged; one new rule ID can appear in its existing `FAIL <rule> <path>: expected …; actual …` form.

## Edge Cases & Error Handling

- Several mentions in one file are each reported. A file that cannot be read within the existing bounds fails closed, as other reads in this validator do.
- A mention inside a Spec package or `CHANGELOG.md` with an older edition passes, because those paths are history.
- Text such as `WGOV-CORE claim` without an edition number is ignored.

## Failure Modes & Fallback / Human Escalation

If the check reports a mismatch on the current tree, the document or the registry must be corrected to the approved edition; the check is not weakened. If a legitimate current mention of an older edition is ever needed, that is a scope change returned to Spec review.

## Verification Commands

- Focused tests: `python3 -m unittest tests.test_shared_contract_binding`, first failing on the new cases before the implementation, then passing.
- The registry validator on the current tree passes; on a disposable copy where the Stage 99 README names WGOV-CORE 3.1.0, it fails with the new rule.
- Strict document validators, the staged lifecycle check and the active commit hooks on the exact index.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-EDITION-001 | Focused tests fail before and pass after the change: a rule-surface mismatch is refused in both recognized forms, history paths and edition-less mentions are ignored, and an absent shared contract disables the check. |
| VAL-EDITION-002 | The registry validator passes on the current tree and fails with `REGISTRY_SHARED_EDITION_MISMATCH` on a disposable copy with a wrong edition in a rule document; the earlier projection and approval refusals still fail. |
| VAL-EDITION-003 | An independent review finds no blocking issue, the strict document checks and commit hooks pass, and the W01 re-audit evidence is recorded in the Task. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0028](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-EDITION-001 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Focused RED/GREEN deterministic negative tests of the edition check. |
| [REQ-0003-FR-0001](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-EDITION-002 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | The owner graph links without contradiction: the registry and rule documents name one edition; direct negative case on a disposable copy. |
| [REQ-0003-NFR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-EDITION-003 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Targeted named tests and staged checks; independent review, strict document checks and commit hooks. |
