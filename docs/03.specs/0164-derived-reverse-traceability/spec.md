---
title: "Derived Reverse Traceability"
version: "1.0.0"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-11-12"
layer: "specs"
artifact_id: "SPEC-0164"
---

# Derived Reverse Traceability Technical Specification (Spec)

## Overview

This approved change contract implements requirement DOC-09 of the external v14.7 execution package, which the user adopted on 2026-11-12 over the earlier SPEC-0156 rejection ([SPEC-0161](../0161-w00-v14-7-delta-intake/spec.md) Task, EVD-018). Each traceability relation is written once, by the document that cites its parent; the reverse view is derived from those forward links, and no document has to hand-write a back-link. Today the registry marks eleven authored profiles and their templates with `reciprocal_evidence`, and `scripts/validate-links-and-owners.py` raises `BODY-LINK-RECIPROCAL` when a cited document does not link back. [REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md) IF-0001 asks for reciprocal links. The [Plan](plan.md) orders the work; [Task 0001](tasks/tsk-0001-derived-reverse-traceability.md) records evidence and acceptance.

## Strategic Boundaries & Non-goals

- In scope, by writer:
  - W03: remove `reciprocal_evidence` from every `body_contract` in `docs/99.templates/registry.json`, and from both the `required` list and the `properties` of `body_contract` in `docs/99.templates/contracts/document-profile.schema.json`.
  - W05: remove the field, its `REGISTRY_BODY_RECIPROCAL` check and the `BODY-LINK-RECIPROCAL` branch with its `_links_back_to` helper from `scripts/document_contracts.py` and `scripts/validate-links-and-owners.py`; delete `test_current_backlink_is_still_required` in `tests/test_documentation_link_boundary.py` and the `reciprocal-without-link` case in `tests/test_document_terminal_contract.py`; add a schema negative case for a leftover key; add `scripts/document-backlinks.py` with `tests/test_document_backlinks.py` in the `tooling` suite; update `scripts/README.md`.
  - W01: REQ-0003 IF-0001, its Traceability row, the acceptance-criterion 02 Traceability row ("links are reciprocal" becomes "each link is written once by the citing document; the reverse view is derived"), the rejected-clause sentence and the three hand-written SPEC-0161 to SPEC-0163 back-link sentences; `.agents/governance/sdlc.md` row "Architecture boundary or durable choice" ("reciprocal links" becomes "forward links"); `.agents/skills/requirements-to-design/SKILL.md` step 5; AD-0006 rows for IF-0001 and criterion 02; the seven Stage 05 explicit-exclusion cells that say no upstream document "carries a reciprocal link" (policies 0003, 0004, 0005, 0007 and runbook 0004), reworded to say no eligible upstream document links to the document.
  - This package, the Stage 03 README and reviewed `.secrets.baseline` digests.
- Kept: supersession reciprocity (`supersedes` with `superseded_by`) is a lifecycle state relation, implemented by `SUPERSESSION_RECIPROCAL` in `scripts/document_authority.py`, `_reciprocal_links` in `scripts/document_lifecycle.py` and the lifecycle validator, and described by ADR-0056 Decision 5 and AD-0006. The policy sentences about it (`document-authoring.md` rule 13, `document-lifecycle.md` Validation and Refresh, `sdlc.md` rule 5) stay, as do accepted ADR texts that record past supersession.
- Deferred: parent-side link columns of the current forms (Requirement `Downstream owner`, Architecture Description `ADR / Spec`, ADR `Affected Spec`, Plan `Task`, incident and postmortem `Follow-up Task`) remain forward links that are checked for resolution and allowed profile but are no longer required to be reciprocal. The common-forms work of SPEC-0161 handoff W03 (COMMON-DOC-FORM-1) replaces them with derived downstream links.
- Not affected: DOC-09's rule that link presence alone does not pass self-containedness. No current check passes self-containedness on a link, and this change removes no self-containedness check.
- The backlinks tool is navigation tooling, not a gate, so `scripts/validation/registry.json` is unchanged.
- No push, PR or merge without separate approval.
- Open question: none.

## Contracts

- No validator requires a cited document to link back to the citing document; a forward link that resolves to an allowed profile is sufficient.
- No current owner tells an author to hand-write a back-link: `git grep -n -i -E 'reciprocal link|reciprocal/current|links back|back-?link|reciprocal evidence|reciprocal-link'` over `.agents`, `docs/AGENTS.md`, `docs/*/AGENTS.md`, Stage 01, 02 and 05 current documents and `docs/99.templates` returns only supersession uses or historical ADR text, each listed in the Task.
- `scripts/document-backlinks.py --root <repo> <path>` lists `git ls-files '*.md'` in sorted order and prints each document, other than the target itself, with a rendered local or anchor link that resolves to `<path>`; it exits 0. A target that is absent or outside the root exits 2 with a message.
- Forward links keep their checks: broken links, disallowed target profiles and stage boundaries still fail.
- The registry schema rejects a profile that still carries `reciprocal_evidence`.

## Core Design

[AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) owns the governance view; two of its traceability rows change wording and no structure changes. The tool loads `scripts/validate-links-and-owners.py` by path, as `scripts/validate-document-lifecycle.py` and the link tests do, and uses its public `rendered_local_links`, so forward and reverse readings cannot drift. It reads through the bounded helpers of `scripts/validation/repository/bounded_io.py` (`scripts/AGENTS.md` rule 4). Per rule 3, the removed rule leaves no compatibility branch.

## Data Modeling & Storage Strategy

No stored reverse index; the tool computes it on demand from the tree.

## Interfaces & Data Structures

`body_contract` loses the `reciprocal_evidence` key; the schema's `additionalProperties: false` on that object makes a leftover key fail. New CLI `scripts/document-backlinks.py --root PATH TARGET`.

## Edge Cases & Error Handling

- Links inside fenced code and HTML comments do not count, as in the forward check.
- An anchor link to the target (`target.md#section`) counts; a document's own `#anchor` links never list the target as its own back-link.
- A target outside the repository root, or absent, exits 2.

## Failure Modes & Fallback / Human Escalation

If removing the rule exposes a broken forward link elsewhere, it is fixed in the citing document, not by restoring the rule.

## Verification Commands

- `python3 scripts/run-contract-tests.py --root . --suite tooling` and `--suite document`, with the backlinks tests shown failing before the tool exists.
- `python3 scripts/document-backlinks.py --root . docs/01.requirements/0003-workspace-agent-governance-platform.md` lists the open Specs that cite REQ-0003.
- The repository search from the Contracts section.
- The strict document validators, the staged lifecycle check and the commit hooks on the exact index.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-REVERSE-001 | No validator, registry entry, schema key or current owner requires a hand-written back-link; the repository search lists only supersession or historical uses; the three REQ-0003 back-link sentences are gone; the strict document checks pass. |
| VAL-REVERSE-002 | The backlinks tool derives the citing documents of a target, with tests for forward and anchor links, fenced and commented links, absent and outside targets that fail before and pass after it exists. |
| VAL-REVERSE-003 | Forward link checks still fail a broken link and a disallowed profile, the schema rejects a leftover `reciprocal_evidence` key, and the `document` and `tooling` suites and commit hooks pass. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-IF-0001](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-REVERSE-001 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Repository search and strict document checks. |
| [REQ-0003-FR-0028](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-REVERSE-002 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Direct tests in the `tooling` suite. |
| [REQ-0003-FR-0028](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-REVERSE-003 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Negative cases in the `document` suite; commit hooks. |
