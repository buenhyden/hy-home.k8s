---
title: "Manual Document Disposition Review"
version: "0.1.0"
type: "sdlc/architecture-decision"
status: "proposed"
owner: "platform"
updated: "2026-11-10"
layer: "architecture"
artifact_id: "ADR-0056"
---

# ADR-0056: Manual Document Disposition Review

## Overview

This proposed amendment adds manual review before disposing of a current
governed document. It replaces only the no-record/no-proof disposition clause
of [ADR-0053](./0053-unvalidated-archive.md) and the unconditional Git-recovery
interpretation of [ADR-0055](./0055-governance-decision-current-state-amendment.md)
Decision 1. Both decisions retain their original bodies and every other
accepted clause, including the unvalidated archive and its README lint exception.
The same change adds a bounded local lifecycle exception for recording a new
Spec/Plan pair as approved when its actual batch review and user approval are
already evidenced.

The request owner approved implementation of this policy-first plan on
2026-11-10. That request authorizes preparation of this candidate and its current
document consumers. The request owner subsequently authorized the limited
contract and validator change supporting that first-record approval exception.
Those requests do not record acceptance of this ADR or an individual
document's disposition. The original approval references, review, acceptance
and publication are recorded separately in
[SPEC-0152's Task](../../03.specs/0152-manual-document-disposition-policy/tasks/tsk-0001-manual-document-disposition-policy.md).

## Context

ADR-0053 removed the former archive catalog, migration records and recurring
archive validation. Its Decision permits deletion or an archive move without
a record or proof, relying on Git history for recovery. ADR-0055 Decision 1
carries that recovery boundary forward, and Decision 7 keeps the archive
README formatted and linted.

[REQ-0003-FR-0015 and REQ-0003-FR-0020](../../01.requirements/0003-workspace-agent-governance-platform.md)
require consumer succession and historical recovery. The existing document
lifecycle policy already assigns disposition to the owning work and lineage
to the current document. Neither a zero count of current consumers nor a
successful static check establishes that historical consumers are satisfied,
a preservation hold is resolved, or the exact original bytes are recoverable.

The approved first change concerns current documents and future dispositions.
It does not reassess earlier removals or restore the retired archive validation
system. The architecture can add a manual decision at the existing Task and
policy owners without introducing another registry or storage service.

A new Spec and Plan may have actual batch review and scoped user approval
before their first Git version. The default draft-only creation rule cannot
represent that already observed approval without an additional historical
version. [REQ-0003-FR-0012 and REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md)
require one machine owner and bounded lifecycle checks. The later scoped
authorization permits a contextual exception at those existing owners while
preserving the normal draft initial state and the separate meaning of Task
execution and criterion acceptance.

## Decision

1. **One policy owner.** The
   [document lifecycle policy](../../../.agents/governance/document-lifecycle.md)
   owns the manual pre-disposition requirements. Authoring guidance, operating
   procedures and stage navigation refer to that owner. Existing document-type
   disposition routes remain conditional on that review.
2. **Consumer and preservation review.** Before deleting a document or moving
   it into the archive, identify its current normative consumers, its
   historical, audit and recovery consumers, preservation needs, holds and
   the valid authority for the intended action. Transfer required current
   meaning to its current owner. Zero current consumers alone is insufficient.
3. **Git-only recovery evidence.** Before choosing Git-history-only
   disposition, identify the exact committed source as `commit:path`, verify
   that the source commit and blob are available through a reachable Git
   reference, restore that source into an authorized temporary location, and
   compare its bytes with the original being disposed of. Uncommitted source
   differences cannot be covered by an older Git object. A missing source,
   failed recovery or byte mismatch defers that disposition.
4. **Existing evidence owners.** Record consumer and hold findings,
   disposition authority, source identity and recovery results in the owning
   Task's existing Inputs, Approval and Safety Boundaries, and Evidence
   sections for every document type. For Stage 01-03 documents, record a
   completed disposition in the current semantic owner's existing Archived
   Lineage. Other types keep their profile's existing reciprocal lifecycle or
   disposition relationships; this amendment does not require them to add an
   Archived Lineage table. A routine disposition belongs to its existing
   work item and does not require a new Spec or a separate retention ledger.
   When a completed Stage 03 package includes its own evidence-owning Task,
   freeze the package's consumer, hold, authority and method decision in that
   Task before its final source commit. After that commit and before deleting
   any package file, record the actual reachable source and temporary byte
   comparison for each retired Spec, Plan and Task file in the surviving
   requirement owner's existing Archived Lineage, linked to the Task decision.
   Recording a file's final-byte proof inside itself would change the bytes
   being proved. This owner-location rule preserves every recovery condition.
5. **Local deferral.** Missing evidence, unknown or unresolved holds,
   unsatisfied consumers, or unavailable authority defer only the affected
   disposition. Preserve the source in place, name the missing condition and
   next owner, and continue independent authorized work. The continued
   presence of a non-current source during that deferral grants it no current
   authority.
6. **Manual control.** These requirements are a human/agent procedure and
   independent review obligation. Existing validators do not enforce them or
   authenticate authority. Stage 98 remains outside document-content
   validation; existing secret checks and the README's formatting and
   Markdown lint continue. No archive-content or historical-cutover gate is
   introduced.
7. **Evidence-bound first-record approval.** The local extension
   `Local candidate Spec/Plan first-recording as approved after actual batch review and approval`
   admits only a new, correctly related Spec and Plan recorded together as
   `approved` in the same package. The Registry's ordinary `spec-plan`
   initial states remain `draft`. The contextual lifecycle reader requires
   an owning Task approval receipt that identifies the user, the trusted
   approval reference, independent batch-review evidence, the pair's scope,
   the exact reviewed Spec and Plan byte hashes, and confirmed validity with
   no revocation. The receipt format belongs to the
   [Spec's contract](../../03.specs/0152-manual-document-disposition-policy/spec.md)
   and its existing lifecycle consumer; this ADR does not duplicate that
   schema. Missing, mismatched or unavailable context fails closed, including
   a standalone lifecycle comparison with no receipt context. A recorded
   receipt is checked for structure, relationships and byte identity; the
   validator does not authenticate an external user or approval source.

The first-record exception does not widen other initial states or transitions,
alter Task PASS/completion requirements, or authorize past execution
retroactively. Earlier authoring and QA observations retain their original
scope. Criterion acceptance, ADR acceptance and protected actions each keep
their existing authority and evidence boundaries. This is a local adapter
extension, not a new shared-contract edition or proof of another repository's
adoption.

The amendment takes effect through recorded review and acceptance of the
candidate. The Task separately records local implementation and validation;
neither is substituted for that acceptance. A later individual disposition
still requires its own applicable authority and evidence.

## Explicit Non-goals

- Deleting or moving any document as part of this policy change, or restoring
  and reassessing the historical deleted corpus.
- Rewriting accepted ADRs, completed Task evidence, published research, or
  historical numbering.
- Adding a retention catalog, frozen-body store, tombstone, migration ledger,
  automated archive-disposition or archive-content gate, historical-cutover
  gate, or CI job. The scoped Spec/Plan approval receipt and its lifecycle
  validation are the only added machine contract in this change.
- Applying development-document disposition rules to service data, backups,
  credentials or the shared memory store, or changing another repository.
- Treating this proposed ADR, a static PASS or the plan implementation request
  as permission for a particular destructive or external action.

## Consequences

- **Positive:** the current owner records why a document can leave the tree
  and demonstrates that Git can recover the intended original bytes.
- **Trade-off:** disposition still relies on scoped manual review. A bypass
  of those disposition prerequisites is not automatically rejected; its
  enforcement requires a separately designed follow-up. The separate
  first-record approval exception adds a bounded contextual reader and
  negative regressions without authenticating user authority.
- **Operational:** an unresolved hold or recovery failure retains the source
  until its next owner resolves the affected disposition. No live service or
  external publication changes are required by this amendment.

## Alternatives

- **Keep unconditional Git recovery:** rejected for the current plan because
  it provides no pre-disposition evidence for holds, historical consumers or
  recovery of the exact source.
- **Restore the full archive validation system:** deferred; the user selected
  policy and manual procedure first, and recurring archive sweeps would
  restore the cost deliberately removed by ADR-0053.
- **Supersede ADR-0053 and ADR-0055 as whole documents:** rejected; their
  remaining decisions still apply. The scoped-amendment pattern preserves
  those records and identifies the changed clauses without rewriting history.
- **Require a draft Git version even after actual batch approval:** rejected
  for the narrowly authorized case because it requires an intermediate
  version solely to represent an already observed decision.
- **Allow every new Spec or Plan to start approved:** rejected; ordinary
  creation remains draft-only, and missing pair, review, scope, byte or
  approval context cannot obtain the exception.

## Traceability

- **Requirements:** [REQ-0003-FR-0012, REQ-0003-FR-0015, REQ-0003-FR-0020 and REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md).
- **Architecture:** [AD-0006](../descriptions/0006-workspace-agent-governance-platform.md).
- **Change and acceptance:** [SPEC-0152](../../03.specs/0152-manual-document-disposition-policy/spec.md),
  criteria `VAL-DISP-001`, `VAL-DISP-002` and `VAL-DISP-003`.
- **Policy and procedure:** [document lifecycle](../../../.agents/governance/document-lifecycle.md)
  and [reference maintenance](../../05.operations/runbooks/0011-reference-maintenance-runbook.md).
- **First-record approval ownership:** the
  [Stage 99 local extension](../../99.templates/registry.json),
  [document lifecycle reader](../../../scripts/validate-document-lifecycle.py)
  and the owning Task's actual approval and independent-review receipts;
  criterion `VAL-DISP-003` covers their agreement and failure boundaries.

### Lifecycle Traceability

| Decision lineage | Replacement relation | Affected Spec |
| --- | --- | --- |
| [ADR-0053](./0053-unvalidated-archive.md) | Replaces only the permission to dispose of a document without a record or proof; preserves archive exclusion and the existing disposition routes | [SPEC-0152](../../03.specs/0152-manual-document-disposition-policy/spec.md) |
| [ADR-0055](./0055-governance-decision-current-state-amendment.md) | Qualifies Decision 1's Git-only recovery with manual pre-disposition review; preserves Decision 7's README lint exception and all other clauses | [SPEC-0152](../../03.specs/0152-manual-document-disposition-policy/spec.md) |
| [AD-0006](../descriptions/0006-workspace-agent-governance-platform.md) | Adds the bounded local first-record Spec/Plan approval exception at the existing policy, Registry and lifecycle reader owners | [SPEC-0152](../../03.specs/0152-manual-document-disposition-policy/spec.md) |
