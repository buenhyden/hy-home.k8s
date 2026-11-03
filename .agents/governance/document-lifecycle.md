---
title: "Document Lifecycle Policy"
version: "2.4.0"
type: "governance/rule"
status: "active"
owner: "platform"
updated: "2026-11-03"
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
- 새로 작성하거나 현행 범위에 맞춰 고치는 Plan은 승인된 Spec의 제약을
  `Global Constraints`에서 연결하고 추가 실행 제약만 적으며, 단일 `Promotion`
  기록 경로를 둔다. 진행 중인 계획은 승격 예정 대상을 승인이나 완료 증거로 쓰지 않는다.
  Spec Package의 완료를 수용할 때에는 Plan의 `Promotion` 기록이 모든 지속 계약을
  현재 Stage 00·01·02·05 소유 문서의 상대 링크와 그 안의 구체적 위치에 연결해야
  한다. 지속 계약이 없으면 `none | none | No durable contract was introduced`
  한 행만 명시한다. Registry가 구현하는 형식은
  Stage 99 자체를 별도 현행 정책으로 지목하지 않고 해당 형식을 위임한 현행 규칙을
  지목한다. Task의 PASS나 부모의 `approved`만으로 이 승격을
  대신하지 않는다. 과거 Plan 원문은 새 기록을 위해 다시 쓰지 않는다.
- A Task carries actual work state: `draft` is proposed, `ready` means the
  approved inputs and execution prerequisites are assembled, `in-progress`
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
  `ready` is no new
  approval or live-action permission.
- For a newly recorded Task in this k8s regional adapter, the first Git
  version may carry an actual nonterminal `ready`, `in-progress` or `blocked`
  row when the current scoped user authorization and Task Inputs identify the
  owner, prerequisites and evidence of preparation, execution or obstacle.
  `ready` still requires approved inputs and assembled prerequisites;
  `blocked` names the cause, resume condition and next owner. A new terminal
  Task is refused. Do not invent a draft-only commit to simulate an unobserved
  transition. Later transitions, required evidence, criterion acceptance and
  protected-action approval remain unchanged. This is an explicit local
  `shared_contract.extensions` rule, not a new WGOV-CORE 3.0.0 edition
  or, by itself, proof of full regional adoption.
- `Local candidate Spec/Plan direct draft-to-approved transition after actual batch review and approval`
  admits the direct edge for this k8s regional
  adapter when a scoped user request, actual batch review and approval are
  recorded. New Spec and Plan creation remains draft-only; approval means the
  reviewed contract and plan are authorized, not execution completion, Task
  criterion acceptance. Do not create an intermediate
  Git state that was not observed solely to satisfy a transition reader.
  This local extension does not change WGOV-CORE 3.0.0 or, by itself, claim
  regional adoption; all later transitions retain their existing checks.
- Stage 01, 02 and 03 documents have no `superseded`, `retired` or
  `deprecated` state and no older form. A replaced or withdrawn document, or a
  completed Spec package, is summarized in the owning current document's
  `Archived Lineage` table and deleted in the same change; Git history recovers
  it. A successor names its predecessor in `supersedes` where the profile
  allows it and in Traceability. 후속 Task의 기록 허용만으로 실행 권한이 생기지
  않으며, 새 활성 작업의 `ready`·`in-progress` 전이와 실제 실행에는 그 작업을
  소유하는 현행 `approved` Spec·Plan이 필요하다. No status alone grants
  disposition, removal or new-execution authority.
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
- Meaningful supersession of an operations, governance, reference or evaluation
  document requires the old owner to link `superseded_by` to the successor and
  the successor to link `supersedes` back in the same change.
- A mutable or current owner cannot disappear without replacement coverage
  and consumer disposition.
- Navigation READMEs carry an "active" routing constant without artifact
  identity or lifecycle binding. Stable reference
  pack anchors named README retain their IDs and publication lifecycle.
- Templates project their source profile, start no lifecycle of their own, and
  do not own a destination path.
- Material Stage 99 index/worktree drift fails staged validation; the staged
  registry is the commit claim.
- A governed document that is no longer current leaves its stage. Stage 01,
  02 and 03 documents are deleted after their Archived Lineage summary; another
  stage may delete it or move it under a `docs/98.archive/` disposition
  directory. In every case Git history is its record, recovered with
  `git show <commit>:<path>`.
  Stage 99 forms leave through Git history only, and a stage or collection
  index is retained in place.
- `docs/98.archive/` is unvalidated history. It is outside the document
  inventory: no profile, lifecycle, link, catalog, retention, citation or
  migration check reads it, and its files carry no envelope, digest or ledger.
  A change under it reruns only secret scanning. The directory keeps its README and disposition structure.
- A current document links the current owner rather than an archived file.
  A link into `docs/98.archive/` is not checked, not even for existence.
- A document that moves between active stages keeps no migration record.

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
