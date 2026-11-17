---
title: "Document Lifecycle Policy"
version: "3.1.2"
type: "governance/rule"
status: "active"
owner: "platform"
updated: "2026-11-17"
---

# Document Lifecycle Policy

## Purpose and Scope

### Objective

This policy governs document promotion, blocking, supersession, retirement,
withdrawal, and historical recovery across the repository.

### Applies To

Stable identities are append-only and never reused. Retired identities are
reserved by the first column of the owners' `Archived Lineage` and checked by
`LIFECYCLE-IDENTITY-REUSE`. Mutable and current
documents may change only within their selected profile contract. Stage 90
evidence is not rewritten to satisfy a later profile.

- [Common Agent Governance](../README.md)
- Archive Stage (`docs/98.archive/README.md`)

#### Exclusions

This policy excludes no subject within its scope; if one is excluded, name it and its owner here.

## Rules

### Requirements

| Rule ID | Condition | Level | Evidence | Status |
| --- | --- | --- | --- | --- |
| DOCLIFE-R001 | Always | required | `document-lifecycle` | active |
| DOCLIFE-R002 | When a Plan is newly authored or revised for current scope | required | `markdown-profiles` | active |
| DOCLIFE-R003 | Always | required | `document-lifecycle` | active |
| DOCLIFE-R004 | For a newly recorded Task | required | `document-lifecycle` | active |
| DOCLIFE-R005 | When a scoped user request, actual batch review and approval are recorded | required | `document-lifecycle` | active |
| DOCLIFE-R006 | When a scoped request, actual batch review and user approval occurred before the first commit | required | `document-lifecycle` | active |
| DOCLIFE-R007 | Always | required | `document-contract-registry` | active |
| DOCLIFE-R008 | Always | required | `document-lifecycle` | active |
| DOCLIFE-R009 | Always | required | `document-lifecycle` | active |
| DOCLIFE-R010 | When a document is cancelled | required | `document-lifecycle` | active |
| DOCLIFE-R011 | On supersession of an operations, governance, reference or evaluation document | required | `document-lifecycle` | active |
| DOCLIFE-R012 | Always | required | Semantic review | active |
| DOCLIFE-R013 | Always | required | Semantic review | active |
| DOCLIFE-R014 | Before a current document is deleted or moved into `docs/98.archive/` | required | Semantic review | active |
| DOCLIFE-R015 | When Git-history-only disposition is chosen | required | Semantic review | active |
| DOCLIFE-R016 | Always | required | `markdown-profiles` | active |
| DOCLIFE-R017 | Always | required | `document-contract-registry` | active |
| DOCLIFE-R018 | Always | required | `document-lifecycle` | active |
| DOCLIFE-R019 | Always | required | `document-lifecycle` | active |
| DOCLIFE-R020 | Always | required | `.markdownlint-cli2.yaml` | active |
| DOCLIFE-R021 | Always | required | Semantic review | active |
| DOCLIFE-R022 | When a policy document leaves its profile path | required | `document-lifecycle` | active |

- `DOCLIFE-R001` A proposed status change must be one directed edge declared by the selected
  profile family. For a new Spec or Plan, `draft` states unreviewed intent,
  `in-review` is the review interval, and `approved` establishes the current
  authorized contract. Changed scope or contradicting evidence sends the
  affected contract back to `in-review`; approval is renewed against the
  revised target before dependent execution. `cancelled` requires a reason,
  actual authority and disposition of remaining criteria.
  Approval never asserts implementation completion, criterion acceptance,
  or integration. Current Spec and Plan use `draft`, `in-review`, `approved`
  and `cancelled`. Task owns `in-progress`, `blocked` and `completed` work.
  A historical comparison reads the states of its original Registry edition.
- `DOCLIFE-R002` A newly authored Plan, or one revised for current scope, links the approved
  Spec's constraints in `Global Constraints`, an H4 of Overview > Constraints
  placed after that section's text, adds only execution constraints specific to the
  Plan, and keeps one promotion table under Promotion Map > Durable Owners. A
  Plan for in-progress Task work does not treat an intended promotion target as approval or
  completion evidence.
  When a Spec package is accepted as complete, the Plan's promotion table
  (Promotion ID, Target Owner, Acceptance, Evidence)
  links every durable contract to its current owner under `.agents/` governance
  or Stage 01, 02 or 05, states the condition under which the promotion counts
  as done, and names the concrete location in that owner. If
  there is no durable contract, use exactly one row:
  `none | none | none | No durable contract was introduced`. For a form implemented
  by the Registry, name the current rule that delegates the form to Stage 99,
  rather than Stage 99 itself as a separate policy owner. Neither a Task PASS
  nor the parent Spec's `approved` state substitutes for promotion. Do not
  rewrite a historical Plan to add a new record.
- `DOCLIFE-R003` A Task carries actual work state: `draft` is proposed, `ready` means the
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
- `DOCLIFE-R004` For a newly recorded Task in this k8s regional adapter, the first Git
  version may carry an actual nonterminal `ready`, `in-progress` or `blocked`
  row when the current scoped user authorization and the Task's Inputs and Authority identify the
  owner, prerequisites and evidence of preparation, execution or obstacle.
  A new terminal Task is refused. Do not invent a draft-only commit to simulate an unobserved
  transition. Later transitions, required evidence, criterion acceptance and
  protected-action approval remain unchanged. This is an explicit local
  `shared_contract.extensions` rule, not a new WGOV-CORE 3.0.0 edition
  or, by itself, proof of full regional adoption.
- `DOCLIFE-R005` The `shared_contract.extensions` entry `Local candidate Spec/Plan direct
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
- `DOCLIFE-R006` The `shared_contract.extensions` entry `Local candidate Spec/Plan
  first-recording as approved after actual batch review and approval` admits a
  narrow first Git record at `approved` when a scoped request, actual batch
  review and user approval occurred before the first commit. The same-package
  Spec and Plan must be recorded together with their typed parent identities
  and Task link. The Task's Results table holds a separate `Independent semantic
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
- `DOCLIFE-R007` Current rule documents under `.agents/`, `docs/99.templates/`, `.claude/`
  and `.codex/` name only the `shared_contract.version` the Stage 99 registry
  adopts; the registry validator refuses another edition as
  `REGISTRY_SHARED_EDITION_MISMATCH`. Spec packages, the archive and
  `CHANGELOG.md` are history and may name older editions.
- `DOCLIFE-R008` Stage 01, 02 and 03 documents have no `superseded`, `retired` or
  `deprecated` state and no older form. A replaced or withdrawn document, or a
  completed Spec package, is summarized in the owning current document's
  `Archived Lineage` table and deleted in the same change; Git history recovers
  it. A successor names its predecessor in `supersedes` where the profile
  allows it and in Traceability. A `rejected` ADR is not current: once the
  manual disposition review below is satisfied, the change that records the
  rejection summarizes it in the owning document's `Archived Lineage` and
  deletes it; otherwise that disposition is deferred. Permission to record a
  successor Task does
  not itself grant execution authority. Draft creation, revision, review and
  focused document checks may proceed within the writing scope. Drafts and QA
  results grant no implementation, operating or completion authority.
  Starting or resuming active work requires a current approved basis or a
  separately verified user authorization for that execution request. Record
  the original reference, actor, target, scope, request revision, reviewed inputs
  and current validity using [Approval and Safety](approval-and-safety.md).
  Keep draft states intact when separately authorized work uses them as inputs.
  No status alone grants disposition, removal or new-execution authority.

  For a changed executable Task, unchanged approved Spec and Plan bytes may
  carry the existing basis. Changed reviewed inputs, draft parents or a draft
  Requirement cited as a normative execution basis need the separately verified
  authorization. A writing check recorded as PASS does not activate a Task.
  In the existing Results table, `Scoped execution approval` records one JSON
  input with `actor`, `approval_ref`, `scope` (Spec, Plan, Task IDs in that order),
  `reviewed_spec_sha256`, `reviewed_plan_sha256`, `request_revision`, `validity`
  and `revocation`. The revision is the SHA-256 of UTF-8 Python JSON with
  `ensure_ascii=False` and default separators, containing the exact text under
  the Task's Scope heading, ordered work rows projected to `ID`,
  `Upstream criterion`, `Work item` and `Owner`, and sorted pairs of draft
  normative Requirement paths for those criteria and their text SHA-256 values.
  The latest receipt must match the current inputs and attest `user`, `confirmed`,
  `none` and PASS for the receipt check. Append a new record on withdrawal or
  reauthorization in chronological order. Recording a withdrawal without
  changing work state or scope does not resume that work. The checker verifies
  the receipt structure and input binding.
  The operator verifies the original approval and current revocation before
  executing or resuming. A receipt never supplies criterion acceptance.
- `DOCLIFE-R009` An SDLC stage identifies the artifact's responsibility and placement.
  Frontmatter status expresses the lifecycle of that artifact. Document approval,
  Task execution, criterion acceptance, QA result,
  publication, integration and archival disposition are separate claims. A
  Requirement's `approved`, an ADR's `accepted`, an operating document's
  `active`, an Incident's `resolved`, and a Postmortem's `published` retain
  their different role meanings; none is Task `completed`. A
  current Task keeps each work item's state in the core Work Items table and
  its result and evidence in the Lifecycle Traceability table (both under
  Execution Log, joined by Item; a Task recorded under the earlier header keeps
  the state in its Lifecycle Traceability row) and one frontmatter status
  marker. For one item, the marker is the human source; for multiple items, the
  row states are the human source, frontmatter `status` is omitted and the
  validators derive the summary from the rows. A multi-row Task that already
  carries `status` must equal the row-derived value, and earlier records are
  not rewritten. A table that cannot be read in the current column form
  yields no derived summary and fails as a missing status.
  The Registry owns state/result values and summary binding; the lifecycle
  checker reads the Git index for completion handoff. Each assigned criterion
  has one authored verdict in Criterion Decisions, and each factual Task
  evidence row records its required status and any earlier observation it
  resolves. A required `FAIL`, `DEFER` or `NOT_RUN` remains visible until a
  later matching PASS explicitly resolves its evidence ID. Unrelated PASS
  cannot satisfy the criterion.
- `DOCLIFE-R010` Nonrequired cancellation does not waive required work. A cancelled document
  records reason, authorization_ref and criteria_disposition. The reference
  leads to original approval evidence and does not authenticate it: verify the
  actual actor, target, action, time and revocation through the trusted approval
  route. Preserve all observed results, including failures, when cancelling.
  A resolved Incident records its actual zoned resolved_at and body evidence;
  a placeholder or date alone cannot establish resolution.
- `DOCLIFE-R011` A replacement Guide, Policy or Runbook names its predecessor
  artifact ID in `supersedes`. While a superseded document stays in the tree,
  the lifecycle checker derives its successors by ID and requires a path to
  an active successor of the same profile. A path rename keeps the ID relation.
  A disposition that removes a predecessor keeps its historical identifier.
  Governance, reference and evaluation domains retain their reciprocal evidence
  requirements in their applicable Registry edition.
- `DOCLIFE-R012` A mutable or current owner cannot disappear without replacement coverage
  and consumer disposition.
- `DOCLIFE-R013` These disposition rules govern repository development documents only.
  Service and operations data, backups, credentials, Vault records and the
  shared memory store keep their own owners and are never removed under them.
  Rules 14–19 govern ordinary disposition. An explicitly approved final
  transition has its own scope and checks. After candidate validation and
  acceptance, the final transition keeps no recovery copy for its approved
  removal targets. That requirement does not authorize a final transition or
  change recovery protection for other work.
- `DOCLIFE-R014` Before a current document is deleted or moved into `docs/98.archive/`,
  manually assess its current normative, historical, audit and recovery
  consumers; preservation value and access need; holds; and actual disposition
  authority. Record the target, basis, approval scope, disposition method and
  unresolved conditions in the existing Task's Inputs and Authority and Results. Transfer current meaning to its canonical
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
- `DOCLIFE-R015` Choose Git-history-only disposition only after proving that the exact
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
- `DOCLIFE-R016` Navigation READMEs carry an "active" routing constant without artifact
  identity or lifecycle binding. Stable reference
  pack anchors named README retain their IDs and publication lifecycle.
- `DOCLIFE-R017` Templates project their source profile, start no lifecycle of their own, and
  do not own a destination path.
- `DOCLIFE-R018` Material Stage 99 index/worktree drift fails staged validation; the staged
  registry is the commit claim.
- `DOCLIFE-R019` A governed document that is no longer current leaves its stage. A stage
  other than 01, 02 or 03 may delete it or move it under a `docs/98.archive/`
  disposition directory. In ordinary disposition Git history is its record, recovered with
  `git show <commit>:<path>`.
  Stage 99 forms leave through Git history only, and a stage or collection
  index is retained in place.
- `DOCLIFE-R020` `docs/98.archive/` is unvalidated history. It is outside the document
  inventory: no profile, lifecycle, link, catalog, retention, citation or
  migration check reads it, and its files carry no envelope, digest or ledger.
  A change to an Archive body reruns only secret scanning; its README keeps the
  existing formatting and Markdown-lint selection. The directory keeps its
  README and disposition structure.
  A current document links the current owner rather than an archived file; a
  link into it is not checked, not even for existence.
- `DOCLIFE-R021` A document that moves between active stages keeps no migration record.
- `DOCLIFE-R022` A policy document that leaves its profile path moves its registered code to
  `reserved_codes` in the same change, and only then may its rule IDs leave their Rules tables.
  The reserved list never shrinks until a user-approved new baseline under the Q-07 contract,
  so the code and its IDs are never issued again.

### Exceptions

Exception and escalation conditions are stated under Requirements.

#### Approval and Review

Approval and review conditions are stated under Requirements.

## Enforcement

### Mechanisms

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

### Limits

The lifecycle validators do not decide recovery proof, holds, consumers or authority, which stay manual. A placeholder or date alone cannot establish resolution, and the manual disposition review of a document's normative, historical, audit and recovery value is not performed by a validator.

## Ownership

### Owner

The Stage 99 registry (`docs/99.templates/registry.json`) is the sole machine
owner for lifecycle states, directed transitions, and the internal `mutable`,
`current`, and `terminal` validation classes. Documents carry only their
profile status. This policy explains evidence obligations and does not repeat
the machine transition table.

- [Software Development Lifecycle](sdlc.md)
- Document Profile Registry (`docs/99.templates/registry.json`)
- [Document Authoring Policy](document-authoring.md)

#### Responsibilities

Responsibilities are stated under Owner and Requirements.

### Review Triggers

Change and adoption conditions are stated under Enforcement.
