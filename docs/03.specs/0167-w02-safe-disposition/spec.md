---
title: "W02 Safe Disposition"
version: "1.0.0"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-11-12"
layer: "specs"
artifact_id: "SPEC-0167"
---

# W02 Safe Disposition Technical Specification (Spec)

## Overview

This approved change contract carries out the W02 stage of the external v14.7 execution package: development documents stay active-only, and a completed or withdrawn unit leaves the tree only after its meaning, holds, authority and exact Git recovery are confirmed. A read-only survey at `b4925358` judged 18 requirement rows: 12 already fit, 5 need a text change in the disposition owners and 1 is handed to W05; the [Task](tasks/tsk-0001-w02-safe-disposition.md) records it. The existing exit route (freeze, then closure with recovery proof in the owner's `Archived Lineage`, checked by `LIFECYCLE-PACKAGE-EXIT`) and ADR-0056's manual review are reused unchanged. The [Plan](plan.md) orders the work.

## Strategic Boundaries & Non-goals

- In scope (writer W02): `.agents/governance/document-lifecycle.md`, `docs/01.requirements/README.md`, `docs/02.architecture/AGENTS.md`; this package, the Stage 03 README and reviewed `.secrets.baseline` digests.
- Kept, with evidence in the Task: the Git-history-only exit for Stage 01 to 03 and 99, the ADR-0056 manual consumer, hold, authority and byte-recovery review, the ADR-0057 event-scoped exit shape check, the unvalidated archive (ADR-0053), the self-removing Task rule, and the absence of any archive-body, retention-catalog or migration gate.
- Not reopened: a presence or age check for Stage 03 packages. ADR-0057 rejected a presence gate because ADR-0056 Decision 5 allows a deferred source to stay, and the user chose its event-scoped check over no check on 2026-11-11. That check catches a wrong exit shape, not a finished package left in place; the Stage 03 index and manual review cover that case.
- Handed over, not changed here: the ADR `rejected` state in the registry (W03, W04), the unreachable `done` and `archived` status branches in two scripts (W05).
- No disposition of any current document: no Stage 01 to 03 document carries a non-current status, and the only open packages are SPEC-0161 and this one.
- No retroactive change to accepted ADRs, completed Task evidence or Archived Lineage rows, including rows that name former `docs/98.archive/` paths.
- No push, PR or merge without separate approval. Open question: none.

## Contracts

- **Retained history (ARC-05, W02-A).** `document-lifecycle.md`: an object reachable only through the reflog, absent from a shallow clone, or lost by squash, rebase or branch cleanup is not retained history, and its disposition is deferred. LFS pointers, submodule gitlinks and filters are not used here; if one is introduced, recovery covers its payload, not the pointer.
- **Frozen text (ARC-03, QA-C04).** `document-lifecycle.md`: after a package's final source commit, its frozen decision and evidence text is not reformatted, translated or normalized; a correction goes to a current document.
- **Disposition scope (ARC-09).** `document-lifecycle.md`: these rules govern repository development documents only. Service and operations data, backups, credentials, Vault records and the shared memory store keep their own owners and are never removed under them.
- **Rejected ADR (ARC-02).** `document-lifecycle.md` and Stage 02 `AGENTS.md`: a `rejected` ADR is not current; once the manual disposition review is satisfied, record the rejection, summarize it in the owning document's `Archived Lineage` and delete it in the same change, otherwise defer. Stage 02 `AGENTS.md` describes `rejected` as the decision outcome that triggers this exit, not a state kept in the tree.
- **Index wording.** `docs/01.requirements/README.md` names the owning current document's `Archived Lineage`, not the Architecture Description's, matching `document-lifecycle.md` and Stage 01 `AGENTS.md`.

## Core Design

[AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) owns the governance view; no component changes. `document-lifecycle.md` stays the single disposition owner; the README and Stage 02 `AGENTS.md` route to it. Constraining decisions: [ADR-0053](../../02.architecture/decisions/0053-unvalidated-archive.md), [ADR-0056](../../02.architecture/decisions/0056-manual-document-disposition-review.md) and [ADR-0057](../../02.architecture/decisions/0057-package-exit-shape-check.md), all unchanged.

## Data Modeling & Storage Strategy

No new file, field, ledger or catalog.

## Interfaces & Data Structures

Handoffs, each recorded in the Task with owner and resume condition:

- W03 and W04 (resume: W03 starts): decide whether the ADR family keeps `rejected` as a stored state now that a rejected ADR leaves the tree in the same change.
- W05 (resume: W05 starts): trace `validate-links-and-owners.py` status branches for `done` and `archived` and `scripts/validation/current_executable_references.py` terminal statuses; remove them with their tests if no registry domain reaches them.

## Edge Cases & Error Handling

- A deferred disposition keeps its source unchanged; no status records the deferral.
- Archived Lineage rows naming former archive paths stay as history; recovery uses `git show <commit>:<path>`.

## Failure Modes & Fallback / Human Escalation

If a disposition condition is unmet, that disposition alone is deferred and the next owner is named in its Task; no override is offered.

## Verification Commands

- `python3 scripts/validate-document-contract-registry.py --root . --mode strict`, `validate-markdown-profiles.py`, `validate-links-and-owners.py` and `validate-document-lifecycle.py` in strict mode; `python3 scripts/run-contract-tests.py --root . --suite document`.
- Anchor search on a whitespace-collapsed copy (the policy is hard-wrapped), one hit each in `document-lifecycle.md`: `reachable only through the reflog`, `not reformatted, translated or normalized`, `repository development documents only`, `` a `rejected` ADR is not current ``.
- Phrase search, no hit after: `Architecture Description의 Archived Lineage` and `AD의 Archived Lineage` in `docs/01.requirements/README.md`.
- `python3 scripts/qa.py staged` and the commit hooks on the exact index.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-DISPOSE-001 | The four anchors are found once in `document-lifecycle.md`, and every KEEP row has file:line evidence in the Task. |
| VAL-DISPOSE-002 | The README phrase search finds no hit, Stage 02 `AGENTS.md` names the rejected-ADR exit, and the strict document checks pass. |
| VAL-DISPOSE-003 | The W03, W04 and W05 handoffs are recorded with owner, interface and resume condition; exact-index QA and the commit hooks pass. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0020](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-DISPOSE-001 | [ADR-0056](../../02.architecture/decisions/0056-manual-document-disposition-review.md) | Anchor search and owner review. |
| [REQ-0003-FR-0015](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-DISPOSE-002 | [ADR-0053](../../02.architecture/decisions/0053-unvalidated-archive.md) | Phrase search; strict document checks. |
| [REQ-0003-FR-0030](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-DISPOSE-003 | [ADR-0057](../../02.architecture/decisions/0057-package-exit-shape-check.md) | Handoff table; exact-index QA. |
