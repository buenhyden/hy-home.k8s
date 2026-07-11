---
title: 'Audit: SDLC, Document Lifecycle, and Frontmatter'
type: content/reference
status: draft
owner: platform
updated: 2026-07-11
---

# Audit: SDLC, Document Lifecycle, and Frontmatter

## Overview

이 문서는 Current research의 SDLC, 문서 수명주기, frontmatter 기준을 고정된
저장소 snapshot과 대조한 dated implementation audit다. PRD부터 README까지
14개 문서 계열, 번호·lineage·상태 전이, baseline five-key frontmatter와
consumer-bound 후보를 서로 다른 통제로 채점한다.

문서와 링크의 존재는 semantic requirement coverage와 구분한다. 특히
`PRD -> Spec -> Task -> validation` 경로가 연결되어 있어도 requirement ID와
검증 결과의 의미 대응이 없으면 semantic lineage로 인정하지 않는다.

## Purpose

- Audit roles, routes, templates, states, evidence, and necessity for all 14
  requested document families.
- Measure numbering exceptions, path-link lineage, semantic lineage, state
  mismatches, approval evidence, and reverse-transition handling.
- Assess every baseline frontmatter key/value class and proposed profile fields
  only against a named automation consumer.
- Compare Minimal, Consolidated, and Full redesign target states without changing
  active Stage 00/99 owners.

## Reference Type

- Type: dated-implementation-audit
- Audit observation SHA: `a85df194bbb8ebc61187b905afaef7f95215cc2f`
- Research cutoff: `2026-07-10 10:00 KST`
- Source checked: 2026-07-11
- Refresh trigger: lifecycle, route, template, frontmatter schema, validator,
  document inventory, requirement lineage, incident exercise, or Release decision
  changes.

## Authority Boundary

- **Authoritative for**:
  - The 31 report-local controls and repository evidence at the audit observation
    SHA.
  - This report's document-family, lineage, lifecycle, frontmatter, Release, and
    incident-readiness findings.
- **Not authoritative for**:
  - Active lifecycle policy, template routes, frontmatter schemas, validators,
    document states, release approval, incident procedure, or live operations.
  - Runtime, remote CI, deployment, release, or actual incident-readiness proof.

## Scope

- Includes canonical Stage 00/99 routing and lifecycle owners, Stage 01-05 authored
  documents, Stage 90 Reference/README surfaces, structural templates, repository
  quality-gate behavior, and fixed-tree path/status/link observations.
- Excludes active-owner edits, historical body rewrites, state promotion, release
  implementation, incident creation, tabletop execution, remote CI, and live
  cluster or provider checks.

## Definitions / Facts

### Evidence and Scoring Basis

Repository claims below are read from audit observation SHA
`a85df194bbb8ebc61187b905afaef7f95215cc2f` with `git show`, `git ls-tree`, and
`git grep`. The [pack audit method](README.md#audit-method) fixes the 12 columns,
maturity vocabulary, and formula: `sum(maturity) / (4 * applicable controls)`.
Maturity, verdict, and confidence remain independent. N/A controls state their
exclusion and stay outside the denominator. No static evidence receives maturity 4.

The observation tree contains 146 non-README Markdown documents in Stage 01-05,
30 non-README References in Stage 90, and 23 README indexes across those stages.
The 176 frontmatter-bearing documents all use `owner: platform`; their status
distribution is 9 `accepted`, 40 `active`, 84 `done`, and 43 `draft`. These counts
do not prove semantic lineage, approval, currentness, or runtime readiness.

### Document-Family Controls

| ID | Benchmark | Expected control | Repository evidence | Maturity | Verdict | Confidence | Gap | Recommendation | Priority | Follow-up owner | Acceptance evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DOC-001 | [Current SDLC research](../../research/2026-07-07-wer/spec-sdlc-ci-qa-formatting.md); Stage 99 SDLC governance | PRD owns product intent and numbered requirements, routes through the PRD template, follows `draft -> active -> done`, and hands requirements to downstream evidence. | Four PRDs use the canonical route/type and are `active`; all link a Spec and Plan, but their 44 file-qualified requirement instances (`PRD path + label`) have zero exact-label citations in Specs or Tasks. Only 12 unqualified literal labels are unique because labels are reused across PRDs. | 2 repository-static | Partial | Verified repo-static | Missing: semantic requirement handoff even though path links exist; unqualified labels also create collision risk. | Add a consumer-tested requirement coverage ledger in the owning Spec/Task chain; do not duplicate implementation detail in PRDs. | P1 near-term integrity | New Stage 03 Spec: sdlc-semantic-lineage-and-lifecycle-enforcement | Fixtures map all 44 current file-qualified requirement keys (`PRD path + label`) to one Spec acceptance/verification owner and one Task result or explicit scoped exclusion; orphan, duplicate-key, unqualified-collision, and unknown keys fail deterministically. |
| DOC-002 | Current SDLC research; [stage authoring matrix](../../../00.agent-governance/rules/stage-authoring-matrix.md) | ARD owns architecture boundaries and quality attributes, uses its route/template, follows `draft -> active -> accepted`, and links upstream/downstream owners. | Four ARDs use `docs/02.architecture/requirements/####-*.md`, `type: sdlc/ard`, and `status: active`; structural route, profile, and required headings are validator-covered. | 2 repository-static | Implemented | Verified repo-static | No missing repository-static role or route control; approval/currentness is not inferred from `active`. | Preserve the ARD role and explicit links without copying ADR or Spec detail. | N/A — no action | N/A — no action | N/A — no action |
| DOC-003 | Current SDLC research; Nygard/Cognitect ADR practice | ADR records one consequential decision, uses sequential four-digit routing and its template, preserves consequences/supersession, and reaches `accepted` or `archived`. | Nine ADRs use the canonical route/type and all are `accepted`; the validator enforces route, exact profile, and template headings. | 2 repository-static | Implemented | Verified repo-static | No missing repository-static role/route element; no claim is made that acceptance approval evidence is complete. | Preserve accepted decisions and use replacement links rather than deleting history. | N/A — no action | N/A — no action | N/A — no action |
| DOC-004 | Current SDLC research; GitHub Spec Kit comparison | Spec owns an implementation/verification contract, links upstream requirements and downstream execution, follows `draft -> active -> done`, and uses the feature route/template. | Twenty parent Specs use routed `spec.md` paths: 16 are `draft`, 4 `active`, and 0 `done`. All 16 draft Specs numbered 009-024 have same-slug done Plans and Tasks; exact PRD requirement citations are absent. | 2 repository-static | Partial | Verified repo-static | Corrective: downstream completion and upstream semantic coverage are not reflected in Spec lifecycle state or requirement mapping. | Reconcile Spec state from explicit completion evidence and add semantic coverage before future downstream closure. | P1 near-term integrity | New Stage 03 Spec: sdlc-semantic-lineage-and-lifecycle-enforcement | A fixed fixture set rejects a done Plan/Task when its parent Spec remains draft without an approved exception, and each completed Spec records requirement-to-validation coverage plus promotion evidence. |
| DOC-005 | Current SDLC research; Stage 99 Plan route | Plan owns execution order, gates, risk, rollback, and expected task evidence; it uses a dated route/template and ends `done` or `archived`. | All 41 Plans are `done`; structural routing, exact five-key profile, required headings, and Stage 04 README status/date parity are deterministic quality-gate checks. | 3 deterministic local+CI enforcement | Implemented | Verified repo-static | No missing Plan structure/index control; upstream semantic and state consistency are scored separately. | Preserve dated evidence and keep task results out of plan intent. | N/A — no action | N/A — no action | N/A — no action |
| DOC-006 | Current SDLC research; Stage 99 Task route | Task owns execution status, commands, results, limitations, review, and evidence; it uses a dated route/template and ends `done` or `archived`. | All 43 Tasks are `done`; route/profile/headings and Stage 04 index parity are enforced. Task tables and verification summaries exist, but cross-family semantic coverage is scored separately. | 3 deterministic local+CI enforcement | Implemented | Verified repo-static | No missing Task structure/index control in this row. | Preserve auditable results and limitations; link rather than copy parent contracts. | N/A — no action | N/A — no action | N/A — no action |
| DOC-007 | Current SDLC research; Stage 99 operations route | Guide owns stable explanatory how-to content, uses its numbered route/template, and remains distinct from executable Runbooks. | Eight Guides are `active`; route/type/headings and operations README status/date parity are deterministic checks. | 3 deterministic local+CI enforcement | Implemented | Verified repo-static | No missing role/route control; `active` is an allowed intermediate state and does not itself prove durable acceptance. | Preserve audience-focused guidance and link executable recovery to Runbooks. | N/A — no action | N/A — no action | N/A — no action |
| DOC-008 | Current SDLC research; Stage 99 operations route | Policy owns durable mandatory controls, exceptions, verification, and review cadence without duplicating Guide advice or ADR rationale. | Seven Policies are `active`; `type: sdlc/policy`, route/headings, and operations index parity are deterministic checks. | 3 deterministic local+CI enforcement | Implemented | Verified repo-static | No missing repository-static policy route or template control. | Preserve canonical control ownership and keep explanatory procedure linked. | N/A — no action | N/A — no action | N/A — no action |
| DOC-009 | Current SDLC research; Stage 99 operations route | Runbook owns ordered operational/recovery steps, verification, observability, and rollback and remains distinct from Guide and Incident chronology. | Nine Runbooks are `active`; route/type/headings and operations index parity are deterministic checks. | 3 deterministic local+CI enforcement | Implemented | Verified repo-static | No missing repository-static route/template control; execution effectiveness is not inferred. | Preserve executable steps and explicit static-versus-live evidence boundaries. | N/A — no action | N/A — no action | N/A — no action |
| DOC-010 | Current SDLC research; NIST SP 800-61 Rev. 3 | Incident owns real-event facts, impact, timeline, response state, and stabilization evidence at the canonical nested route; preparedness requires exercise or event evidence. | No authored Incident exists. The validator enforces the future `YYYY/INC-###-*` path, matching filename, template/profile, no placeholder directories, and explicit empty-state README language. | 2 repository-static | Partial | Conditional | Complementary: zero real incidents is neutral, but no tabletop/exercise evidence demonstrates that the route and response contract work. | Run a separately approved metadata-only/tabletop readiness exercise without fabricating a real Incident record. | P2 planned improvement | New Stage 04 Task: incident-response-tabletop-readiness | An approved exercise artifact records scenario, role handoffs, template/path dry run, evidence capture, failure findings, and remediation owners while the Incident index continues to distinguish exercises from real events. |
| DOC-011 | Current SDLC research; Google SRE postmortem practice | Postmortem owns stabilized-event RCA, contributing factors, prevention actions, and documentation feedback, colocated with its Incident. | No authored Postmortem exists. The route/template/profile are declared and the empty-state index is enforced, but no real or exercise record tests the learning loop. | 2 repository-static | Partial | Conditional | Complementary: no readiness evidence shows Incident facts can become owned learning actions without blame or chronology duplication. | Include the Postmortem handoff and action closure in the approved tabletop readiness exercise. | P2 planned improvement | New Stage 04 Task: incident-response-tabletop-readiness | The exercise produces a clearly labeled non-incident Postmortem dry run with evidence links, owned actions, documentation feedback, and closure criteria; no fake `INC-*` record is added. |
| DOC-012 | Current SDLC research; audit-pack SDLC design | Release is introduced only if an ADR establishes a home-lab need, owner, artifact/provenance, approval, rollback, and lifecycle route. | Stage 99 has no Release route or template, and the fixed tree contains no Release document family. No approved requirement or ADR establishes one. | N/A — excluded pending ADR-established Release need | Not in scope | Conditional | Excluded: adding a family without an approved consumer would create unnecessary lifecycle surface. | Keep Release absent unless a future ADR demonstrates need and chooses a route. | N/A — no action | N/A — no action | N/A — no action |
| DOC-013 | Current SDLC research; [reference template](../../../99.templates/templates/common/reference.template.md) | Reference owns slow-moving facts, source/freshness and authority boundaries, uses `content/reference`, and does not redefine active controls. | Thirty non-README Stage 90 References exist at the observation SHA; structural routing, exact profile, and required template headings are deterministic checks. | 3 deterministic local+CI enforcement | Implemented | Verified repo-static | No missing repository-static Reference route control; source freshness semantics are scored in frontmatter controls. | Preserve dated authority boundaries and link active owners. | N/A — no action | N/A — no action | N/A — no action |
| DOC-014 | Current SDLC research; README route contract | README is a frontmatter-free navigation/current-index surface and must not become a lifecycle document or duplicate governance. | Twenty-three README files occur across Stage 01-05 and Stage 90; quality gates ban frontmatter, require canonical README sections, and validate Stage 04/operations index membership plus status/date parity. | 3 deterministic local+CI enforcement | Implemented | Verified repo-static | No missing assessed README route/index control. | Keep READMEs as entrypoints and point lifecycle prose to canonical owners. | N/A — no action | N/A — no action | N/A — no action |

### Numbering, Lineage, and Transition Controls

The four PRDs contain 44 file-qualified requirement instances: 10, 11, 12, and
11 per file. Their stable audit keys are the pair `PRD path + label`; there are
only 12 unique unqualified literal labels because the same labels are reused
across PRDs, creating collision risk for any path-free join. Every PRD links a
Spec and Plan, and three link a Task directly. However, the linked Specs cite
none of those exact labels. Across all 20 parent Specs, 91 distinct `VAL-SPC-*`
labels exist; Tasks cite 32 distinct labels. The 32 is a repository-wide
reference count, not proof that 32 requirements close, because no
requirement-to-validation crosswalk owns that relationship.

| ID | Benchmark | Expected control | Repository evidence | Maturity | Verdict | Confidence | Gap | Recommendation | Priority | Follow-up owner | Acceptance evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LIN-001 | Stage 99 numbering/handoff contract | A new PRD and Spec use the same three-digit feature number; historical mismatches remain in place with explicit links and an exception reason. | The four PRD numbers are 001-004, while their linked Specs are 004, 005, 006, and 008: 4/4 numeric mismatches. Links preserve identity, but no deterministic numbering/exception validator or standard exception field exists. | 1 documented/routed | Partial | Verified repo-static | Corrective: historical links exist, but exception rationale and new-work mismatch prevention are prose-only. | Validate new PRD/Spec numbering and require a bounded exception record for historical or umbrella lineages instead of renumbering old files. | P2 planned improvement | New Stage 03 Spec: sdlc-numbering-and-lineage-exceptions | Positive fixtures accept a same-number lineage and a documented historical/umbrella exception; negative fixtures reject an unexplained new mismatch without changing existing identifiers. |
| LIN-002 | Stage 99 lifecycle handoff contract | Bidirectional path links connect PRD, architecture, Spec, Plan, Task, operations, and archive owners without broken or contradictory handoffs. | Four of four PRDs link a Spec and Plan, three link a Task. Three of the four linked Specs reciprocally name the PRD and downstream Plan/Task. `003` links Spec 006, but Spec 006 declares `PRD: N/A`; the related Plan/Task chain instead records a historical governance overlay. | 2 repository-static | Partial | Verified repo-static | Corrective: path links are mostly present, but one canonical PRD-to-Spec handoff contradicts the Spec body and link completeness is not semantic coverage. | Repair the 003/006 ownership statement and validate reciprocal owner links separately from requirement mapping. | P2 planned improvement | New Stage 04 Task: sdlc-link-and-state-reconciliation | A fixed link graph reports exactly one resolved owner for each of the four PRD lineages, resolves the 003/006 contradiction, and rejects a missing or contradictory reciprocal handoff. |
| LIN-003 | GitHub Spec Kit traceability principle; Current research lineage benchmark | Every PRD requirement has an explicit Spec disposition and verification owner, including scoped exclusions. | The four PRDs define 44 file-qualified requirement instances (`PRD path + label`) but only 12 unique unqualified literal labels, which are reused across PRDs. Exact-label search across all parent Specs and Tasks returns zero citations. | 0 absent | Gap | Verified repo-static | Missing: semantic PRD requirement-to-Spec coverage; filenames and generic Related Documents links cannot prove disposition, and path-free labels collide. | Introduce a body-owned coverage ledger keyed by fully qualified PRD path plus requirement label; do not put the full graph in frontmatter. | P1 near-term integrity | New Stage 03 Spec: sdlc-semantic-lineage-and-lifecycle-enforcement | The ledger accounts for 44/44 current file-qualified keys (`PRD path + label`) with implemented/deferred/not-applicable disposition, downstream Spec criterion, and verification owner; unknown, duplicate-key, unqualified-collision, and orphan keys fail. |
| LIN-004 | Current research candidate lineage | Spec verification criteria map to Task rows and recorded command/result evidence, including explicit skipped or unavailable lanes. | Parent Specs contain 91 distinct `VAL-SPC-*` labels; Tasks cite 32 distinct labels and many Tasks record commands/PASS results without label-level mapping. No deterministic coverage denominator joins Spec criteria to Task results. | 1 documented/routed | Partial | Verified repo-static | Missing: an auditable Spec-to-Task-to-result coverage relation; the citation count cannot distinguish covered, duplicated, or orphaned criteria. | Add criterion-level Task result mapping with PASS/FAIL/SKIP semantics and a deterministic orphan report. | P1 near-term integrity | New Stage 03 Spec: sdlc-semantic-lineage-and-lifecycle-enforcement | A generated fixed-tree report accounts for every applicable `VAL-SPC-*` ID exactly once or records an approved exclusion, links each to a Task result, and fails unknown or unowned criteria. |
| LIN-005 | Stage 99 lifecycle state contract | Upstream and downstream states are consistent, or a time-bounded approved exception explains why delivery evidence closes before its contract. | All 16 draft parent Specs numbered 009-024 have a same-slug `done` Plan and `done` Task. Overall, Specs are 16 draft/4 active/0 done while Plans are 41/41 done and Tasks 43/43 done. The validator accepts every global allowed status regardless of family or downstream state. | 1 documented/routed | Gap | Verified repo-static | Corrective: lifecycle state no longer communicates delivery position, and draft contracts can coexist indefinitely with completed execution. | Add family-specific state domains plus cross-stage consistency checks and reconcile existing exceptions through an approved Task. | P1 near-term integrity | New Stage 03 Spec: sdlc-semantic-lineage-and-lifecycle-enforcement | Family-state fixtures reject invalid terminal values and reject draft-Spec/done-Task pairs without owner, reason, expiry/review trigger, and promotion or archive disposition; the 16 current mismatches are explicitly resolved. |
| LIN-006 | Current research approval/reverse-transition benchmark | Promotion and any reverse transition record approver, reason, evidence, affected downstream owners, and next review; archived Tombstones never reactivate. | Stage 99 defines forward states and forbids Tombstone reactivation. Fixed-tree prose contains several “does not reopen” notes, but no shared approval/reverse-transition record or validator; Git history alone does not express intent or authorization. | 0 absent | Gap | Verified repo-static | Missing: approved reverse-transition semantics and evidence. Narrative non-reopen notes prevent some ambiguity but are not a reusable contract. | Define explicit promotion/reopen evidence and make rollback affect status only through a separately approved owner; preserve immutable archive behavior. | P1 near-term integrity | New Stage 03 Spec: sdlc-state-transition-evidence | Positive fixtures record from/to state, actor/approver, reason, evidence, affected lineage, and review trigger; negative fixtures reject unexplained reverse transitions and every archived-to-active transition. |

### Frontmatter and Consumer-Bound Profile Controls

The baseline contract is exactly `title`, `type`, `status`, `owner`, and
`updated` for non-README routed Markdown, with the documented Archive Tombstone
extension. At the observation SHA, all 176 sampled frontmatter-bearing documents
use `owner: platform`, none uses the `YYYY-MM-DD` placeholder for `updated`, and
none has an `updated` string lexically later than 2026-07-11. Those observations
do not erase validator gaps: the gate permits the template placeholder in authored
documents and checks date shape rather than calendar validity or future dates.

| ID | Benchmark | Expected control | Repository evidence | Maturity | Verdict | Confidence | Gap | Recommendation | Priority | Follow-up owner | Acceptance evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FM-001 | [Frontmatter schema](../../../99.templates/support/frontmatter-schema.md) | Every routed Markdown path has exactly one profile with exactly its required/allowed keys; README and native machine contracts remain frontmatter-free. | The validator maps structural paths to one template/profile, rejects uncovered/multiple routes and missing/extra keys, and bans README/native-contract frontmatter. | 3 deterministic local+CI enforcement | Implemented | Verified repo-static | No missing assessed key-set/profile-routing control. | Preserve exact profiles and explicit exceptions. | N/A — no action | N/A — no action | N/A — no action |
| FM-002 | Frontmatter schema baseline `title` | `title` is present, nonempty, human-readable, non-placeholder, and consistent enough with document identity for consumers. | The gate requires the `title` key but does not reject empty, template-placeholder, or identity-inconsistent values. The fixed sample passes current structural checks. | 2 repository-static | Partial | Verified repo-static | Corrective: key presence is enforced, but title value class is not. | Add bounded nonempty/placeholder checks; avoid enforcing exact H1 equality unless a consumer needs it. | P2 planned improvement | New Stage 04 Task: frontmatter-value-validation | Positive multilingual titles pass; empty and unchanged template-placeholder titles fail; any H1 comparison rule has a documented consumer and fixtures. |
| FM-003 | Frontmatter schema baseline `type` | `type` is the exact namespaced value for the route/profile. | The validator compares each routed path to its expected `sdlc/*`, `content/*`, or `governance/*` type and rejects unsupported or mismatched values. | 3 deterministic local+CI enforcement | Implemented | Verified repo-static | No missing assessed type-domain control. | Preserve route-owned namespaced values. | N/A — no action | N/A — no action | N/A — no action |
| FM-004 | Frontmatter schema baseline `status`; Stage 99 lifecycle owner | `status` belongs to the document family's allowed state path, and terminal/promotion semantics are family-specific. | The gate accepts the global set `draft`, `active`, `accepted`, `done`, `archived` for every normal profile; only Archive Tombstones are fixed to `archived`. Thus a PRD could statically pass with `accepted` or an ADR with `done`. | 2 repository-static | Partial | Verified repo-static | Corrective: valid vocabulary is enforced but family-specific value domains and transitions are not. | Enforce family-state domains and transition evidence through the lifecycle owner. | P1 near-term integrity | New Stage 03 Spec: sdlc-semantic-lineage-and-lifecycle-enforcement | Profile fixtures accept only each documented family path; PRD `accepted`, ADR `done`, Operations `done`, unexplained reverse transitions, and Tombstone reactivation fail. |
| FM-005 | Frontmatter schema baseline `owner` | Repository-authored documents use the canonical owner value, while detailed decision/approval responsibility stays in the body. | The gate requires `owner: platform`; all 176 sampled frontmatter documents use it. Decision/evidence roles remain template/body concerns. | 3 deterministic local+CI enforcement | Implemented | Verified repo-static | No missing baseline owner-domain control; expanding owner values without an authorization consumer would add ambiguity. | Keep the canonical value and body-owned responsibility split. | N/A — no action | N/A — no action | N/A — no action |
| FM-006 | Frontmatter schema baseline `updated` | `updated` is a real ISO calendar date, not in the future relative to the validation clock, and connects to profile-specific freshness where a consumer exists. | The gate checks only `YYYY-MM-DD` shape or literal placeholder. The observed sample has zero future strings and zero placeholders, but invalid calendar dates and future values are not rejected; only Stage 04/operations indexes compare the string. | 2 repository-static | Partial | Verified repo-static | Missing: semantic date validity and future-date rejection; review freshness has no common consumer. | Validate real non-future dates now; add `review_due` only with a defined freshness consumer and clock semantics. | P2 planned improvement | New Stage 04 Task: frontmatter-value-validation | Fixtures reject `2026-02-30`, future dates, and authored placeholders while accepting deterministic clock-bound valid dates; review alerts remain absent until separately specified. |
| FM-007 | Current research placeholder/value-class benchmark | Authored documents reject unresolved template placeholders and empty metadata values without mistaking illustrative template placeholders for authored data. | `validate_markdown_frontmatter_profile` explicitly permits `YYYY-MM-DD` for `updated` and `archived_on` outside the template-only loop; no general placeholder detector covers `title` or other strings. Current sampled documents contain no `updated` placeholder. | 1 documented/routed | Gap | Verified repo-static | Corrective: a clean snapshot can regress because the validator contract permits unresolved authored metadata. | Separate template placeholder allowances from authored-document value validation. | P1 near-term integrity | New Stage 04 Task: frontmatter-value-validation | Template files retain documented placeholders, while authored fixtures with placeholder title/date/archive values fail and current authored fixtures pass. |
| FM-008 | Current research consumer-bound common candidates | Common `id`, `created`, `review_due`, and `supersedes` fields are added only after a named consumer, uniqueness/domain rules, migration, and rollback are approved. | These keys are unsupported by current profiles, so the validator rejects them. No approved ID graph, review scheduler, or supersession consumer exists. | N/A — excluded until an approved consumer contract exists | Not in scope | Conditional | Excluded: universal expansion would duplicate path, Git history, body review notes, or archive lineage without a consumer. | Keep the fields out of baseline frontmatter; reconsider per profile through a separate Spec. | N/A — no action | N/A — no action | N/A — no action |
| FM-009 | Current research Reference candidate | Reference `source_checked` becomes metadata only if an index, freshness gate, or report generator consumes it; otherwise source checks stay in the Reference body. | The reference template owns `Source checked` under `## Reference Type`; `source_checked` is not an allowed frontmatter key and no metadata consumer exists. | N/A — excluded until a Reference freshness consumer is approved | Not in scope | Conditional | Excluded: adding the field now would duplicate body-owned freshness and create two truth surfaces. | Retain body ownership unless a future Spec consolidates the value and consumer atomically. | N/A — no action | N/A — no action | N/A — no action |
| FM-010 | Current research Incident candidates | `incident_id`, `severity`, and `incident_state` become Incident-only metadata when response/index automation defines domains, privacy, transitions, and exercise behavior. | No Incident records exist, current profiles reject these keys, and no incident automation consumer or domain contract exists. Path identity already carries `INC-###`; severity and response state currently belong to the template body. | N/A — excluded pending real or approved exercise consumer design | Not in scope | Conditional | Excluded: premature metadata would invent an untested response taxonomy and may duplicate path/body truth. | Use the tabletop Task to discover consumer needs; route any schema proposal through a later Spec. | N/A — no action | N/A — no action | N/A — no action |
| FM-011 | Frontmatter schema purpose and consumer-bound research rule | Metadata remains classification/lifecycle/freshness data; requirements, rationale, approval narrative, validation results, and operational facts stay in body-owned sections. | The exact-key validator rejects arbitrary frontmatter expansion, while templates provide body sections for requirements, decisions, evidence, approvals, sources, and incident facts. | 2 repository-static | Implemented | Verified repo-static | No missing baseline separation; proposed fields remain conditional because consumers are absent. | Preserve the boundary and require consumer, privacy, migration, and rollback evidence for every profile extension. | N/A — no action | N/A — no action | N/A — no action |

### Necessity and Retention Disposition

| Family | Current disposition | Necessity boundary |
| --- | --- | --- |
| PRD | Keep; consolidate duplicate intent; archive only with replacement | Needed for product intent and acceptance ownership. |
| ARD | Keep; consolidate duplicate domain views | Needed for reusable architecture requirements; single choices belong in ADR. |
| ADR | Keep accepted history; supersede rather than erase | Needed only for consequential choices. |
| Spec | Keep one current contract per feature; reconcile or archive obsolete duplicates | Needed where acceptance and verification can be executed. |
| Plan | Keep auditable rollout/decomposition; consolidate same stream | Decline trivial duplicates already fully owned by a Task. |
| Task | Keep execution/results evidence | Decline evidence-free status copies. |
| Guide | Keep reproducible explanatory guidance | Executable emergency procedure belongs in Runbook. |
| Policy | Keep enforceable durable controls | Non-normative advice belongs in Guide. |
| Runbook | Keep executable verified procedure | Narrative explanation and event chronology belong elsewhere. |
| Incident | Conditional keep for real incidents only | Zero records is neutral; never create placeholders or fake incidents. |
| Postmortem | Conditional keep when analysis/learning is warranted | Not every event requires a separate record; the Incident must remain factual owner. |
| Release | Decline until an ADR proves need | No current consumer or route justifies the family. |
| Reference | Keep factual, slow-moving, source-bounded knowledge | Consolidate duplicated Current summaries; never replace active controls. |
| README | Keep as frontmatter-free index | Consolidate governance prose into canonical owner links. |

### Score and Distribution Summary

| Category | Applicable controls | Maturity numerator | Denominator | Implementation | Maturity distribution (`0/1/2/3/4`, applicable only) | Verdict distribution (`Implemented/Partial/Gap/Not in scope`, all rows) | Confidence distribution (`Verified repo-static/Unverified live/Conditional`, all rows) | N/A exclusions |
| --- | ---: | ---: | ---: | ---: | --- | --- | --- | --- |
| Document families | 13 | 33 | 52 | 63.5% | `0/0/6/7/0` | `9/4/0/1` | `11/0/3` | DOC-012 Release |
| Numbering, lineage, transitions | 6 | 5 | 24 | 20.8% | `2/3/1/0/0` | `0/3/3/0` | `6/0/0` | None |
| Frontmatter/profile fields | 8 | 18 | 32 | 56.3% | `0/1/4/3/0` | `4/3/1/3` | `8/0/3` | FM-008 common candidates; FM-009 Reference; FM-010 Incident |
| **Overall** | **27** | **56** | **108** | **51.9%** | **`2/4/11/10/0`** | **`13/10/4/4`** | **`25/0/6`** | **Four rows** |

Arithmetic is `33 + 5 + 18 = 56` over
`4 * (13 + 6 + 8) = 108`. Four N/A rows are excluded from numerator and
denominator. The 14 actionable rows comprise eight P1 and six P2 findings; there
are no P0 or P3 findings. No maturity 4 is awarded because this fixed evidence set
contains no operational lifecycle, release, or incident exercise proof.

### Target-State Comparison

Decision scores use `1` (least favorable) through `5` (most favorable).
Benefit is weighted x3; affordability, migration feasibility, rollback safety,
blast-radius containment, and prerequisite readiness are x1. Maximum is 40.
These are decision-aid scores, not maturity scores.

| Target state | Benefit x3 | Affordability | Migration | Rollback | Blast containment | Prerequisite readiness | Weighted score | Decision |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Minimal | 2 | 5 | 5 | 5 | 5 | 5 | 31/40 | Repairs currentness, links, family status validation, and authored-placeholder rejection but leaves semantic lineage fragmented. |
| Consolidated | 5 | 3 | 4 | 4 | 4 | 4 | 34/40 | **Recommended**: centralizes lifecycle/exception rules, adds body-owned requirement/validation ledgers, and introduces profile fields only with consumers. |
| Full redesign | 4 | 1 | 1 | 2 | 1 | 1 | 18/40 | Defer: universal IDs and lineage-led metadata impose disproportionate migration and validator blast radius. |

Consolidated is the selected recommendation because the dominant 20.8% lineage
score cannot be repaired by link cleanup alone, while no consumer evidence supports
a universal metadata graph. Its migration should first add body-owned coverage and
exception fixtures, reconcile the 16 Spec-state mismatches, then enable checks after
the fixed inventory passes. Rollback is removal of the new opt-in checks while
preserving existing paths, links, and a generated exception ledger.

Full redesign would affect at least the 176 sampled frontmatter documents plus
templates, route owners, indexes, archive rules, and validators. Prerequisites are
an approved ADR/Spec, stable ID and relationship domains, consumer inventory,
collision census, dual-read validator, migration mapping, privacy boundary, and
rollback owner. Migration would backfill identifiers, dual-validate old/new forms,
switch consumers, and only then retire compatibility; rollback would retain old
paths and disable new required fields without losing the mapping ledger.

## Comparison Analysis

- Structural routing and exact five-key profiles are strong; semantic lineage and
  state evidence are the weakest category.
- 4/4 PRD-to-Spec numeric mismatches are historical, so cosmetic renumbering would
  destroy useful identity. Explicit exception records are safer.
- Path links do not resolve the 003/006 contradiction or account for 44/44
  file-qualified PRD requirement keys. A body-owned, path-plus-label coverage
  ledger is the smallest meaningful repair and avoids collisions among the 12
  reused unqualified literal labels.
- The 16 draft-Spec/done-Plan/done-Task pairs show a state contract that is
  documented but not applied consistently across stages.
- Incident/Postmortem absence is not a failure. Missing exercise evidence is the
  readiness uncertainty; Release remains unnecessary until an ADR establishes need.
- Current metadata correctly rejects arbitrary expansion. The immediate gaps are
  authored-placeholder, calendar/future-date, title value, and family-state checks,
  not universal IDs.

## Residual Risks

- Counts and link searches are repository-static and do not prove human approval,
  document comprehension, remote CI, release readiness, or incident response.
- The 32 Task citations to 91 Spec validation IDs are not coverage until a join rule
  defines applicability and duplicate/orphan behavior.
- Git history can show that a scalar changed but cannot by itself prove who approved
  a forward or reverse transition or why.
- A future consumer may justify profile-specific fields; this report intentionally
  does not pre-authorize them.

## Sources

- [Audit pack README and method](README.md)
- [Current SDLC, CI, QA, and Formatting Research](../../research/2026-07-07-wer/spec-sdlc-ci-qa-formatting.md)
- [Stage Authoring Matrix](../../../00.agent-governance/rules/stage-authoring-matrix.md)
- [Document Stage Routing](../../../00.agent-governance/rules/document-stage-routing.md)
- [SDLC Governance](../../../99.templates/support/sdlc-governance.md)
- [Template Routing](../../../99.templates/support/template-routing.md)
- [Frontmatter Schema](../../../99.templates/support/frontmatter-schema.md)
- [Reference Template](../../../99.templates/templates/common/reference.template.md)
- `scripts/validate-repo-quality-gates.sh` at the audit observation SHA

## Review and Freshness

- Review cadence: on source change
- Last reviewed: 2026-07-11
- Next review trigger: canonical lifecycle/route/frontmatter owner, validator,
  authored inventory, requirement/validation lineage, state reconciliation,
  incident exercise, Release ADR, or audit method change.
- Refresh method: retain the prior observation SHA, recount fixed-tree families and
  labels, rerun path/state/profile fixtures, recalculate all distributions and N/A
  exclusions, and keep live/approval evidence separate.

## Related Documents

- **Audit pack**: [2026-07-11 WEIA README](README.md)
- **Implementation plan**: [WEIA implementation plan](implementation-plan.md)
- **Current research pack**: [2026-07-07 WER README](../../research/2026-07-07-wer/README.md)
- **Parent audits index**: [Audits README](../README.md)
