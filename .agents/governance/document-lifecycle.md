---
title: "Document Lifecycle Policy"
version: "2.0.0"
type: "governance/rule"
status: "active"
owner: "platform"
updated: "2026-10-08"
---

# Document Lifecycle Policy

## Overview

This policy governs document promotion, blocking, supersession, retirement,
withdrawal, sealing, and historical recovery across the repository.

## Authority Boundary

The Stage 99 registry (`docs/99.templates/registry.json`) is the sole machine
owner for lifecycle states, directed transitions, and the internal `mutable`,
`current`, and `terminal` validation classes. Documents carry only their
profile status. This policy explains evidence obligations and does not repeat
the machine transition table.

## Governance Context

Stable identities are append-only and never reused. Mutable and current
documents may change only within their selected profile contract. Immutable
Stage 98 and Stage 90 evidence is not rewritten to satisfy a later profile.
Transition-only legacy routes remain a finite fail-closed projection until
their owning migration work package moves them.

## Current Contract

- A proposed status change must be one directed edge declared by the selected
  profile family. For a new Spec or Plan, `draft` states unreviewed intent,
  `in-review` is the review interval, and `approved` establishes the current
  authorized contract. Changed scope or contradicting evidence sends the
  affected contract back to `in-review`; approval is renewed against the
  revised target before dependent execution. `cancelled` and `superseded`
  require a reason, actual authority and disposition of remaining criteria.
  Approval never asserts implementation completion, criterion acceptance,
  integration or archive eligibility.
- A Task carries actual work state: `draft` is proposed, `ready` means the
  approved inputs and execution prerequisites are assembled, `in-progress`
  records started execution, and `blocked` names the obstacle and next owner.
  Resume requires evidence that the obstacle was resolved. `completed`
  requires completed work, applicable required checks, accepted criteria and
  durable owner handoff. `cancelled` or `superseded` keeps its observed results
  and assigns each remaining required criterion to a verified successor in
  the current Plan. A criterion becomes `not-required` only for a cancelled
  Task under a same-package cancelled Spec with actual criterion-specific
  scope and authorization proof. Both dispositions name the criterion, and
  the Task authorization references the Spec decision; a successor alone is
  no waiver. Active, completed and superseded Tasks cannot use that verdict.
  QA `NOT_APPLICABLE` describes a check without a target, not a criterion
  waiver.
  `ready` is no new
  approval or live-action permission.
- Historical `done` remains valid in its frozen body or earlier Git generation.
  The 2026-09-28 generation used `completed` for Spec, Plan and Task closure;
  current completed parents and Tasks retain their actual status, bytes,
  approval and evidence instead of being backfilled as `approved`. Narrow
  compatibility for a completed Task checks its original path, identity,
  revision and bytes; copying an old form into a new Task does not qualify.
  A completed parent may receive an authorized follow-up Task without
  reopening the original record. No status alone grants disposition, removal
  or new-execution authority.
- Document approval, Task execution, criterion acceptance, QA result,
  publication, integration and archival disposition are separate claims. A
  Requirement's `approved`, an ADR's `accepted`, an operating document's
  `active`, an Incident's `resolved`, and a Postmortem's `published` retain
  their different role meanings; none is Task `completed`. A
  current Task keeps execution in one Task Table and one frontmatter status
  marker. For one row, the marker is the human source; for multiple rows, the
  row states are the human source and an explicit writer generates the marker.
  The Registry owns state/result values and summary binding; the lifecycle
  checker reads the Git index for completion handoff. Each assigned criterion
  has one authored verdict in Criterion Acceptance, and each factual Task
  Evidence row records its required status and any earlier observation it
  resolves. A required `FAIL`, `DEFER` or `NOT_RUN` remains visible until a
  later matching PASS explicitly resolves its evidence ID. Unrelated PASS
  cannot satisfy the criterion.
- Nonrequired cancellation does not waive required work. A cancelled document
  records reason, authorization_ref and criteria_disposition. The reference
  leads to original approval evidence and does not authenticate it: verify the
  actual actor, target, action, time and revocation through the trusted approval
  route. Preserve all observed results, including failures, when cancelling.
  A resolved Incident records its actual zoned resolved_at and body evidence;
  a placeholder or date alone cannot establish resolution.
- Meaningful supersession requires the old owner to link `superseded_by` to the
  successor and the successor to link `supersedes` back in the same change.
- A mutable or current owner cannot disappear without replacement coverage,
  consumer disposition, and applicable Git-backed recovery evidence.
- Navigation READMEs and the current Archive catalog carry an "active" routing
  constant without artifact identity or lifecycle binding. Stable reference
  pack anchors named README retain their IDs and publication lifecycle.
- Templates project their source profile, start no lifecycle of their own, and
  do not own a destination path.
- Material Stage 99 index/worktree drift fails staged validation; the staged
  registry is the commit claim.
- A governed document that is no longer current is retained rather than
  deleted. A document in Stages 01, 02, 03, 05, or 90 leaves for the Stage 98
  disposition that matches what happened to it, and a superseded architecture
  decision follows the same rule. Stage 99 follows its retention modes: a
  retired form leaves through `git-history-only` with no Stage 98 record, and a
  stage or collection index is retained in place. The Registry selects status
  and package-specific retention eligibility. Eligibility does not execute a
  disposition: actual approval, promoted durable meaning, and consumer-zero
  review are separate. An eligible unit waits intact in its source stage until
  that decision; status or package closure alone authorizes neither its move
  nor new execution.
- Stage 98 has six dispositions of two kinds. A retention class holds a whole
  once-current body under the profile that governed it: `completed/` names what
  it promoted, `superseded/` names the document that replaced it, `retired/`
  names why a rule or scope was withdrawn with no successor, and `resolved/`
  holds a closed Incident bundle with its published Postmortem and names the
  closure evidence and current corrective-work owner. A route disposition holds
  no body: `tombstones/` names a retired route, its successor or absence, and
  the reason, and `migrations/` names a moved scope and its current owner as
  `MIG-####`. Current tombstone and scope-migration routes share the
  archive/route draft-to-sealed meaning while their existing profiles and paths
  select the route-specific fields. A disposition's directory is created by the change that first
  uses it.
- Citability is decided by the registry's ordered `archive_citation` table,
  and every citation check consumes that one decision. An active-stage document
  may cite the index, `completed/`, and, as historical evidence, `resolved/`.
  It cites the successor instead of a `superseded/` body, and the current route
  instead of a `retired/` body, a tombstone, or a migration. Before any class
  admission, no source outside Stage 98 links a unit judged `withdrawn` or
  `invalidated` or no longer `retained`. An
  `operation/incident` or `operation/postmortem` may also cite a body in any
  retention class as historical evidence. No document outside Stage 98 links a
  route record or a frozen sealed record; it names a frozen record by
  identifier through the index.
- Retention follows the profile: frozen bodies remain immutable, while a
  Git-history-only disposition retains recoverable provenance without a
  compatibility copy. No Stage 98 record carries a second recovery ledger: no
  redirect, path ledger, self-designed body digest, branch SHA, or recovery
  commit. The Stage 98 catalog's Retention Envelope names the source Git object
  once as `<commit>:<original path>`, and normal Git history recovers it.
- ADR-0038 recorded this model and superseded ADR-0032. ADR-0039 supersedes
  ADR-0038, keeps its six dispositions, and retains units exactly. A spec
  package is one unit with its anchor `spec.md`, an Incident bundle is one unit
  with its anchor `incident.md` and a published Postmortem, and any other
  document is its own unit. In that generation, the anchor's terminal state
  admitted the class and every other member was terminal in its own family.
  The retained path equals the
  source Git object entry for entry, links included, and its catalog row names
  a blob or a tree. The sixteen bodies ADR-0038 retained with rebased links
  keep that generation and cannot grow in number.
- For the current `spec-package` `completed/` route only, the Registry also
  admits `approved` Spec and Plan authority members when the immutable
  comparison-base tree contains both at that state and the same source package
  passes closure: assigned Tasks completed, each required criterion has one
  accepted authored verdict, required adverse evidence is explicitly resolved,
  and the lasting meaning has a named current owner. `approved` alone does
  not qualify. This is a scoped package rule, not general admission of active
  documents or a change to the completed-only class for other units. Review
  actual promotion, consumer disposition and approval of the whole retention
  action separately. The envelope still requires exact source bytes, paths and
  modes, and no Archive body is rewritten to meet a later contract.
- ADR-0040 supersedes ADR-0039 and keeps its units and exact retention. A
  retained unit is frozen against unapproved change, not kept forever: its
  bytes are never edited, renamed, recreated, or partly deleted, and the one
  admitted change is an approved removal of the whole unit, after which its
  availability is `git-history-only`, its catalog row stays, and its envelope
  still verifies. Removal is not purification and needs its own approval.
- A unit's current evidential value is judged in the Archive index's
  Retention Assessment table, never in the frozen body. A unit without a row
  is `unreviewed` and `retained`; every other judgment names a current Task,
  Spec, or decision that records it, a `superseded` judgment names the current
  owner, and a Hold blocks removal. A row never leaves and a removed unit never
  returns. `invalidated` judges old evidence and does not rewrite the old
  state. The registry owns the values and conditions, and `purged` stays
  reserved until a security-approved purification contract exists.
- An envelope commit is reachable from the registry-named default branch, so a
  unit's source is integrated before the change that retains it.
- The Stage 99 registry declares the units, binds each retention mode to the
  profiles that may use it, routes a retained body under its original profile,
  and binds each retention class to admitted anchor states plus the narrow
  Spec-package authority-member closure. Frozen records
  and ledgers route by exact path, so no new sealed record or path ledger can be
  created. The lifecycle gate admits a retained unit through its catalog row,
  and the current Archive integrity gate re-verifies every row against the
  object it names when that contract is selected.
- A document that moves between active stages in one change, keeping its
  `artifact_id`, family, and state, is tracked by identity lineage and needs no
  Stage 98 record. A scope migration is recorded only when a consumer outside
  the repository reads the moved paths.
- Frozen Stage 98 content keeps its generation. Sealed records with their
  ArchiveEnvelope and digests, migration ledgers with pinned rows, and retained
  packages keep their bytes and historical links; validators classify them as
  historical evidence and never rewrite them to the current form.

## Validation and Refresh

Lifecycle validators use bounded regular-file reads, strict UTF-8, explicit
subprocess timeouts, and stage-zero Git bytes. Illegal edges, incomplete
reciprocal links, oversize or undecodable authority input, and material staged
drift are failures. Review this policy whenever the registry lifecycle catalog
changes.

## Related Documents

- [Software Development Lifecycle](sdlc.md)
- [Governance Hub](../README.md)
- Document Profile Registry (`docs/99.templates/registry.json`)
- [Document Authoring Policy](document-authoring.md)
- Archive Stage (`docs/98.archive/README.md`)
