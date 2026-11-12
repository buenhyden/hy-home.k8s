---
title: "Document Lifecycle Policy"
version: "2.7.0"
type: "governance/rule"
status: "active"
owner: "platform"
updated: "2026-11-12"
---

# Document Lifecycle Policy

## Overview

This policy governs document promotion, blocking, supersession, retirement,
withdrawal, and historical recovery across the repository.

## Authority Boundary

The Stage 99 registry (`docs/99.templates/registry.json`) is the sole machine
owner for lifecycle states, directed transitions, and the internal `mutable`,
`current`, and `terminal` validation classes. Documents carry only their
profile status. This policy explains evidence obligations and does not repeat
the machine transition table.

## Governance Context

Stable identities are append-only and never reused. Mutable and current
documents may change only within their selected profile contract. Stage 90
evidence is not rewritten to satisfy a later profile.

## Current Contract

- A proposed status change must be one directed edge declared by the selected
  profile family. For a new Spec or Plan, `draft` states unreviewed intent,
  `in-review` is the review interval, and `approved` establishes the current
  authorized contract. Changed scope or contradicting evidence sends the
  affected contract back to `in-review`; approval is renewed against the
  revised target before dependent execution. `cancelled` requires a reason,
  actual authority and disposition of remaining criteria.
  Approval never asserts implementation completion, criterion acceptance,
  or integration.
- A newly authored Plan, or one revised for current scope, links the approved
  Spec's constraints in `Global Constraints`, adds only execution constraints
  specific to the Plan, and keeps one `Promotion` record. An in-progress Plan
  does not treat an intended promotion target as approval or completion evidence.
  When a Spec package is accepted as complete, the Plan's `Promotion` record
  links every durable contract to its current owner under `.agents/` governance
  or Stage 01, 02 or 05, and names the concrete location in that owner. If
  there is no durable contract, use exactly one row:
  `none | none | No durable contract was introduced`. For a form implemented
  by the Registry, name the current rule that delegates the form to Stage 99,
  rather than Stage 99 itself as a separate policy owner. Neither a Task PASS
  nor the parent Spec's `approved` state substitutes for promotion. Do not
  rewrite a historical Plan to add a new record.
- A Task carries actual work state: `draft` is proposed, `ready` means the
  approved inputs and execution prerequisites are assembled (it is no new
  approval or live-action permission), `in-progress`
  records started execution, and `blocked` names the obstacle and next owner.
  Resume requires evidence that the obstacle was resolved. `completed`
  requires completed work, applicable required checks, accepted criteria and
  durable owner handoff. `cancelled` keeps its observed results
  and assigns each remaining required criterion to a verified successor in
  the current Plan. A criterion becomes `not-required` only for a cancelled
  Task under a same-package cancelled Spec with actual criterion-specific
  scope and authorization proof. Both dispositions name the criterion, and
  the Task authorization references the Spec decision; a successor alone is
  no waiver. Active and completed Tasks cannot use that verdict.
  QA `NOT_APPLICABLE` describes a check without a target, not a criterion
  waiver.
- For a newly recorded Task in this k8s regional adapter, the first Git
  version may carry an actual nonterminal `ready`, `in-progress` or `blocked`
  row when the current scoped user authorization and Task Inputs identify the
  owner, prerequisites and evidence of preparation, execution or obstacle.
  A new terminal Task is refused. Do not invent a draft-only commit to simulate an unobserved
  transition. Later transitions, required evidence, criterion acceptance and
  protected-action approval remain unchanged. This is an explicit local
  `shared_contract.extensions` rule, not a new WGOV-CORE 3.0.0 edition
  or, by itself, proof of full regional adoption.
- The `shared_contract.extensions` entry `Local candidate Spec/Plan direct
  draft-to-approved transition after actual batch review and approval`
  admits the direct edge for this k8s regional
  adapter when a scoped user request, actual batch review and approval are
  recorded. Ordinary new Spec and Plan creation remains draft-only, subject
  only to the separately defined first-record approval exception below;
  approval means the
  reviewed contract and plan are authorized, not execution completion, Task
  criterion acceptance. Do not create an intermediate
  Git state that was not observed solely to satisfy a transition reader.
  This local extension does not change WGOV-CORE 3.0.0 or, by itself, claim
  regional adoption; all later transitions retain their existing checks.
- The `shared_contract.extensions` entry `Local candidate Spec/Plan
  first-recording as approved after actual batch review and approval` admits a
  narrow first Git record at `approved` when a scoped request, actual batch
  review and user approval occurred before the first commit. The same-package
  Spec and Plan must be recorded together with their typed parent identities
  and Task link. The Task Evidence holds a separate `Independent semantic
  review` PASS row, which records the exact-byte checklist review by the
  approving owner or an optional separate reviewer, and a `Spec/Plan first-record approval` PASS receipt. Both
  rows identify SHA-256 hashes of the exact reviewed approved Spec and Plan
  bytes. The receipt names the user, trusted approval reference, review row,
  both document IDs, confirmed validity and no known revocation.
  Each row's `Input` is one JSON object: the review row has exactly
  `spec_sha256` and `plan_sha256`; the receipt has exactly `actor` (`user`),
  `approval_ref`, `review_ref`, `scope` (the Spec and Plan IDs),
  `reviewed_spec_sha256`, `reviewed_plan_sha256`, `validity` (`confirmed`)
  and `revocation` (`none`). A human
  confirms the approval source and scope; the local validator checks only
  receipt form, relationships and byte identity. This exception does not turn
  authoring permission or earlier QA into retroactive execution approval,
  Task criterion acceptance, ADR acceptance, protected-action authority or
  integration evidence. Do not fabricate a draft commit or remove observed
  Task evidence to satisfy the normal route. The shared WGOV-CORE edition and
  ordinary later transitions remain intact.
- Current rule documents under `.agents/`, `docs/99.templates/`, `.claude/`
  and `.codex/` name only the `shared_contract.version` the Stage 99 registry
  adopts; the registry validator refuses another edition as
  `REGISTRY_SHARED_EDITION_MISMATCH`. Spec packages, the archive and
  `CHANGELOG.md` are history and may name older editions.
- Stage 01, 02 and 03 documents have no `superseded`, `retired` or
  `deprecated` state and no older form. A replaced or withdrawn document, or a
  completed Spec package, is summarized in the owning current document's
  `Archived Lineage` table and deleted in the same change; Git history recovers
  it. A successor names its predecessor in `supersedes` where the profile
  allows it and in Traceability. A `rejected` ADR is not current: once the
  manual disposition review below is satisfied, the change that records the
  rejection summarizes it in the owning document's `Archived Lineage` and
  deletes it; otherwise that disposition is deferred. Permission to record a
  successor Task does
  not itself grant execution authority. Moving new active work to `ready` or
  `in-progress`, or executing it, requires its current owning `approved` Spec
  and Plan. No status alone grants
  disposition, removal or new-execution authority.
- Document approval, Task execution, criterion acceptance, QA result,
  publication, integration and archival disposition are separate claims. A
  Requirement's `approved`, an ADR's `accepted`, an operating document's
  `active`, an Incident's `resolved`, and a Postmortem's `published` retain
  their different role meanings; none is Task `completed`. A
  current Task keeps execution in one Task Table and one frontmatter status
  marker. For one row, the marker is the human source; for multiple rows, the
  row states are the human source, frontmatter `status` is omitted and the
  validators derive the summary from the rows. A multi-row Task that already
  carries `status` must equal the row-derived value, and earlier records are
  not rewritten. A table that cannot be read in the current column form
  yields no derived summary and fails as a missing status.
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
- Meaningful supersession of an operations, governance, reference or evaluation
  document requires the old owner to link `superseded_by` to the successor and
  the successor to link `supersedes` back in the same change.
- A mutable or current owner cannot disappear without replacement coverage
  and consumer disposition.
- These disposition rules govern repository development documents only.
  Service and operations data, backups, credentials, Vault records and the
  shared memory store keep their own owners and are never removed under them.
- Before a current document is deleted or moved into `docs/98.archive/`,
  manually assess its current normative, historical, audit and recovery
  consumers; preservation value and access need; holds; and actual disposition
  authority. Record the target, basis, approval scope, disposition method and
  unresolved conditions in the existing Task's Inputs, Approval and Safety
  Boundaries, and Task Evidence. Transfer current meaning to its canonical
  owner first. For Stage 01–03 documents, retain source identity and recovery
  route in the current owner's existing `Archived Lineage`; other document
  types use their existing relationships or disposition record. Do not impose
  a new table or field on every profile, or a separate Spec or permanent catalog
  for each simple disposition. When a completed Stage 03 package includes its
  own evidence-owning Task, freeze the package's consumer, hold, authority and
  method decision in that Task before its final source commit. The completed
  Spec, Plan and Task cannot each contain proof of restoring their own final
  committed bytes without changing those bytes. Before deleting any package
  file, record the actual reachable `commit:path` and temporary byte-comparison
  result for each retired file in the surviving current owner's existing
  `Archived Lineage`, linked to the frozen Task decision. This changes only the
  location of the completed package's postcommit proof; every recovery and
  authority condition still applies to every file in the retiring unit.
  After the final source commit, the frozen decision and evidence text is
  not reformatted, translated or normalized; a correction goes to a current
  document.
- Choose Git-history-only disposition only after proving that the exact
  `commit:path` containing the bytes of the current source is reachable from
  the intended retained history and that a temporary restoration matches the
  current source byte for byte. An older Git object that loses uncommitted
  changes is not recovery evidence. An object reachable only through the
  reflog, absent from a shallow clone, or lost by squash, rebase or branch
  cleanup is not retained history, and its disposition is deferred. Git LFS,
  submodules and filters are not used here; if one is introduced, recovery
  covers its payload, not the pointer or gitlink. First identify the reason
  and consumer
  when original-body preservation is required. If a hold, authority, consumer
  transfer or applicable recovery evidence remains unresolved, defer that
  disposition without changing or deleting the source. Do not retrospectively
  rewrite completed records or rerun past dispositions under this procedure.
- Navigation READMEs carry an "active" routing constant without artifact
  identity or lifecycle binding. Stable reference
  pack anchors named README retain their IDs and publication lifecycle.
- Templates project their source profile, start no lifecycle of their own, and
  do not own a destination path.
- Material Stage 99 index/worktree drift fails staged validation; the staged
  registry is the commit claim.
- A governed document that is no longer current leaves its stage. A stage
  other than 01, 02 or 03 may delete it or move it under a `docs/98.archive/`
  disposition directory. In every case Git history is its record, recovered with
  `git show <commit>:<path>`.
  Stage 99 forms leave through Git history only, and a stage or collection
  index is retained in place.
- `docs/98.archive/` is unvalidated history. It is outside the document
  inventory: no profile, lifecycle, link, catalog, retention, citation or
  migration check reads it, and its files carry no envelope, digest or ledger.
  A change to an Archive body reruns only secret scanning; its README keeps the
  existing formatting and Markdown-lint selection. The directory keeps its
  README and disposition structure.
  A current document links the current owner rather than an archived file; a
  link into it is not checked, not even for existence.
- A document that moves between active stages keeps no migration record.

## Validation and Refresh

Lifecycle validators use bounded regular-file reads, strict UTF-8, explicit
subprocess timeouts, and stage-zero Git bytes. Illegal edges, incomplete
reciprocal links, oversize or undecodable authority input, and material staged
drift are failures. In `staged` mode `LIFECYCLE-PACKAGE-EXIT` refuses a Stage
03 package exit in the wrong shape among the package's Markdown files: an
unfinished package, part of a package, a package that no Requirement changed
in the same commit names in Archived Lineage, or a Spec or Plan edit in a
package whose Tasks are all terminal (ADR-0057).
Recovery proof, holds, consumers and authority stay manual. Review this policy
whenever the registry lifecycle catalog changes.

## Related Documents

- [Software Development Lifecycle](sdlc.md)
- [Common Agent Governance](../README.md)
- Document Profile Registry (`docs/99.templates/registry.json`)
- [Document Authoring Policy](document-authoring.md)
- Archive Stage (`docs/98.archive/README.md`)
