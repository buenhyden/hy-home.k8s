---
title: "W03 Retired Identity Reservation"
version: "1.0.0"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0180"
---

# W03 Retired Identity Reservation Technical Specification (Spec)

## Overview

This approved change contract closes handoff W03-H03 (from W02-H01) of the W03 stage of the external v14.7 execution package. The [document lifecycle policy](../../../.agents/governance/document-lifecycle.md) says stable identities are append-only and never reused, but `LIFECYCLE-IDENTITY-REUSE` reserves only identities present in the comparison base. An identity whose document left the tree through Git history and is named in an `Archived Lineage` row can be minted again: the SPEC-0161 Task observed this with a synthetic probe (EVD-024). W03-H03 decided where retired identities are reserved, the first column of each owner's `Archived Lineage` table, and asked for a refusal test for a retired SPEC identity; its writer is W05 and its resume condition is "now". The user asked on 2026-11-13 to do now any item that was due before. The package commit also records in the SPEC-0161 Task the user's decisions W03-D22 to W03-D24 and the tracking rows of the 2026-11-13 W03 gap audit, so later packages can cite them. The [Task](tasks/tsk-0001-w03-retired-identity-reservation.md) records execution and the [Plan](plan.md) orders the work.

## Strategic Boundaries & Non-goals

- In scope (writer W05 validator code under W03-H03): `scripts/document_lifecycle.py` (`artifact_identity_reuse_diagnostics`, `LifecycleEvidenceContext`, `compare_lifecycle` and a public lineage-identity helper), `scripts/validate-document-lifecycle.py` (`_evidence_context`, the two direct callers in the cumulative-history path and its snapshot cache), `tests/test_document_artifact_identity.py`, `tests/test_document_lifecycle_cumulative_history.py` and any test that pins the reuse diagnostic; one sentence in `.agents/governance/document-lifecycle.md` naming the lineage as the reservation source, with its frontmatter `version` and `updated`; in the SPEC-0161 Task the decision rows W03-D22 to W03-D24, the audit tracking rows, evidence rows and the frontmatter `version` and `updated` (appended rows only: they carry the user's recorded 2026-11-13 answers and the audit findings with owner and resume condition, add no requirement, and are verified by the strict Task validators and the staged lifecycle check); this package, the Stage 03 README and reviewed `.secrets.baseline` entries.
- Not in this package: any `Archived Lineage` row or other document text; a registry key for retired identities; identities that need no lineage row (research, audit, runbook, policy, guide and incident identities under ADR-0056), which stay reserved only while present; the snapshot and completion modes, which have no base to define a new identity; W03-H04 and the generator, whose decision W03-D24 this package only records; phase 3.
- No push, PR or merge without the user's approval, which is standing for this work (2026-11-13). Open question: none.

## Contracts

- **Reservation source.** A retired identity is any identity token in the first cell of a data row of an `Archived Lineage` table (an H2 or H3 section found as the package-exit check finds it today, `_archived_lineage_text`) in any document of the base or proposed snapshot; today six documents carry one (four requirements and two architecture descriptions). Header and separator rows and a first cell without a token are skipped; cells are split on unescaped `|`. A token is the longest match, bounded by no letter, digit or `-` on its left and no letter or digit on its right, of the identity grammar of `frontmatter.schema.json` `terminalArtifactId` (for example `SPEC-0165`, `SPEC-0165-TSK-0001`, `RES-0002-m0001`, `inc-0001-0001-PM`) or of a historical prefix outside it (`OPS-####`, `MIG-####`); the first cell may hold one bare token (`SPEC-0165`), a token with a note (`REQ-0001 (superseded)`) or a title with the token in parentheses (`… (AD-0003)`), and every token in it is read.
- **Refusal.** A proposed document whose `artifact_id` is new at its path (its base document at the same path is absent or has another identity) fails `LIFECYCLE-IDENTITY-REUSE` when that `artifact_id` equals a retired identity or begins with a retired identity followed by `-` (for example `SPEC-0165-PLAN-0001`). The observed text names the retired identity and the lineage that reserves it. The existing base-reservation rule is unchanged.
- **Unchanged documents pass.** A document whose base at the same path holds the same identity is not judged, as today. The current `REQ-0001`, `REQ-0002` and `REQ-0003` reuse earlier identities that `REQ-0004`'s lineage names as superseded; they predate this check and keep passing because they are not new at their paths.
- **Package exit.** The closure change that adds a lineage row and deletes the package creates no new identity, so it is not refused.
- **Every caller.** `compare_lifecycle` holds no text, so `LifecycleEvidenceContext` gains a defaulted field `retired_identities` that `_evidence_context` fills from both snapshots' text maps (iterating the maps it receives), and `compare_lifecycle` passes it on; the staged, ci and explicit-ref comparisons and the cumulative-history calls that use the cache's evidence context pick it up. The two direct cumulative-history calls derive the set from the cache's snapshot texts, and the cache memoizes the set per commit. `artifact_identity_reuse_diagnostics` takes the set as a keyword-only argument with an empty default, so existing callers and tests stay valid. The snapshot and completion modes run no reuse check and stay as they are.
- **Policy text.** The lifecycle policy says that retired identities are reserved by the first column of the owners' `Archived Lineage` and are checked by `LIFECYCLE-IDENTITY-REUSE`.

## Core Design

[AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) owns the governance view; no component changes and no ADR changes. [ADR-0056](../../02.architecture/decisions/0056-manual-document-disposition-review.md) keeps disposition review manual; this check adds only identity reservation.

## Data Modeling & Storage Strategy

No stored data changes. The reserved set is derived from current lineage text at check time.

## Interfaces & Data Structures

- `artifact_identity_reuse_diagnostics` gains the keyword-only retired set; `LifecycleEvidenceContext` gains `retired_identities`; one public helper next to `_archived_lineage_text` derives the set from a text map and is imported by `scripts/validate-document-lifecycle.py`.
- `tests/test_document_artifact_identity.py`: a new document reusing a retired `SPEC` identity named only in lineage fails; a child `SPEC-####-PLAN-0001` of a retired identity fails; a title-with-parentheses cell and a `(superseded)` cell reserve their token; a member identity (`RES-####-m####`) and an incident identity are read whole; an unchanged or edited document at its path whose identity a lineage names passes; a package-exit-shaped change passes; the base-reservation control still fails; one Git-fixture test through the staged or explicit-ref comparison and one cumulative-history test through a direct call show the refusal end to end.

## Edge Cases & Error Handling

- A token in a lineage row that is not in the first cell (for example inside a summary column) is not read.
- A lineage section without a table reserves nothing; the package-exit check keeps owning lineage shape.
- `_archived_lineage_text` is a plain heading search, so a fenced `Archived Lineage` sample in a template would reserve its tokens; no template holds one today.
- A reservation lasts as long as its lineage row: the union of base and proposed snapshots covers a row deleted in the same change, not a later deletion, which stays a manual review matter under ADR-0056.

## Failure Modes & Fallback / Human Escalation

If the check refuses a current document, the change is wrong and is fixed before commit; no document is edited to pass. If a caller cannot supply text without widening this scope, the author stops and asks the user.

## Verification Commands

- Before and after, record the output of the four strict document validators; diagnostics after must equal those before.
- `python3 scripts/run-contract-tests.py --root . --suite document-lifecycle`, `--suite document`, `--suite validation-routing`.
- `ruff check scripts tests`; `python3 scripts/qa.py staged` and the commit hooks on the exact index.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-RETIRED-001 | A new document reusing a retired identity or a child of one fails `LIFECYCLE-IDENTITY-REUSE` in every mode that reads lineage; the failing case is shown before the change and passes after; existing documents and package exits pass. |
| VAL-RETIRED-002 | The policy sentence is updated; validator diagnostics over the tree are unchanged; exact-index QA and the commit hooks pass. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0023](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-RETIRED-001 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Identity refusal tests; lifecycle suite. |
| [REQ-0003-FR-0023](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-RETIRED-002 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Strict validators over the tree; exact-index QA. |
