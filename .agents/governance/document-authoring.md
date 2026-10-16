---
title: "Document Authoring Policy"
version: "3.3.0"
type: "governance/rule"
status: "active"
owner: "platform"
updated: "2026-10-16"
---

# Document Authoring Policy

## Overview

Select the document owner by purpose, author from its canonical template, and
close the change with traceable evidence.

## Authority Boundary

Stage 99 README (`docs/99.templates/README.md`) is the human authoring guide.
Its registry (`docs/99.templates/registry.json`) alone owns exact paths,
profiles, IDs, sections, metadata, lifecycle, and relationships. This policy
owns agent procedure, not a second machine contract.

## Governance Context

Use [SDLC flow](sdlc.md) to distinguish durable requirements, current
architecture, change-specific behavior, and operating knowledge. Stage numbers
express ownership, not a one-way waterfall.

## Current Contract

1. Identify the owning stage and normalize the final repository-relative path.
2. Resolve exactly one registry profile and read its canonical template before
   creating or restructuring a document. No match or multiple matches is a
   stop condition.
3. Use the profile-owned initial status, metadata, sections, and relationships.
   Do not assume every profile starts at "draft". Router READMEs participate in
   the governed envelope with an "active" routing constant, but have neither
   artifact identity nor lifecycle binding. Stable reference pack anchors keep
   their reference identity and publication lifecycle even when named README.md.
4. Take the frontmatter key set and its order from the selected profile, and
   each key's value grammar from the
   frontmatter schema (`docs/99.templates/contracts/frontmatter.schema.json`).
   Every string, date, version, and identity scalar uses double quotes. A
   "title" never repeats the document's "artifact_id": identity is already a
   key, and a title that restates it carries no information.
5. Treat a key the profile omits as a key the document has no business
   declaring. `layer` names the numbered stage a document lives in, so common governance
   sits above that numbering and a Stage 99 form is not the document it
   produces; neither declares one. A profile that declares no `artifact_id`
   describes something the repository does not give a stable identity. Preserve
   an existing optional governance identity; do not mint one for normalization.
6. Replace prompts with concrete content, use complete stable IDs for
   traceability, and calculate links from the final target path. A file outside
   `docs/` links to current owners and stage or collection README navigation,
   never directly to an individual numbered-stage document, including historical
   records. Renaming a link to a plain path or artifact ID does not remove a
   current authority dependency: promote the needed rule to its current owner.
   The boundary normalizes relative/absolute references, Markdown references,
   HTML/wiki links, repository blob/raw URLs, encoding, case and separators.
   Machine reads are admitted only by the exact consumer, target and access-kind
   tuples in the link validator; they do not authorize rendered links. Route
   grammars stay in the Stage 99 registry. Links inside `docs/` retain their
   historical and current relationship contracts.
   The registry's ordered `archive_citation` table decides every link into
   `docs/98.archive/`. A document links no further than the index and the
   retention classes whose own body still leads a reader to current authority:
   `completed/`, through its promotion declaration, and `resolved/`, as
   historical evidence, through its corrective-work owner. It cites the
   successor instead of a `superseded/` body and the current route instead of a
   `retired/` body, a tombstone, or a migration. It never links a unit the
   Archive index's Retention Assessment judges `withdrawn` or `invalidated` or
   no longer `retained`; it names that unit by identifier through the index. A frozen record it must still
   name is named by identifier and reached through the index. An
   `operation/incident` record or its `operation/postmortem` may also cite a
   body in any retention class as historical evidence, but never a route record
   or a frozen sealed record, because neither holds an evidence body.
7. Keep a Requirement Package solution-independent. Put executable interface
   contracts and change-scoped Technical Approach and Acceptance Contract in
   the owning Spec package; put order, risks, verification, and rollback in its
   Plan and execution evidence in its Task records. A fresh Spec and Plan
   describe authorized, current intent when approved; Task execution and
   criterion acceptance remain separate from that approval. Keep one Task
   Table with criterion links, row state, result and evidence. Its frontmatter status is
   the sole document status marker. For one row, author its state only in
   frontmatter and use literal `frontmatter` in the row. For multiple rows,
   author only row states; generate the required header summary with the
   explicit Task status writer, never a second human-maintained state. The
   read-only checker verifies that summary against Registry-bound rows.
   Record each criterion's sole authored `pending`, `accepted`, `rejected`, or
   `not-required` disposition in the Task's Criterion Acceptance table, with
   evidence, disposition rationale and current owner. Neither the execution
   row nor a factual check row repeats that verdict. A row's PASS alone is not
   completion: required work needs a completed execution state, concrete PASS
   evidence and an accepted criterion verdict, with no unresolved required
   adverse result. Keep failed or deferred observations in Task Evidence; a
   later PASS resolves an earlier required result only when it names that
   evidence ID and matches the check, work unit and criterion.
   `not-required` is reserved for a cancelled Task whose same-package Spec is
   also cancelled with actual criterion-specific scope and authorization proof.
   Both cancellation dispositions name the exact criterion, and the Task's
   authorization reference points to that Spec decision.
   A successor-only handoff, active/completed/superseded Task, or QA
   `NOT_APPLICABLE` result does not waive a criterion.
   Keep ordered work, dependencies, Task links and verification intent in the
   Plan, without copied execution status. Attach factual checks in Task
   Evidence with exact inputs, results, locations, whether each check is
   required, and any earlier evidence it resolves; these facts do not replace
   execution rows, the sole criterion verdict or authorization.
   An observed `FAIL` needs concrete Check, Input and Location just as `PASS`
   does. Unrun `NOT_RUN` or unavailable `DEFER` may retain `Pending` in a
   location until real evidence exists, with the reason and next owner stated.
8. Promote durable cross-change decisions to an Architecture Decision and
   current system views to an Architecture Description. Do not create parallel
   design, test, release, or progress authority. This repository uses external
   release evidence: Task and Git own local work, while tags, hosted CI, and
   provider/live results remain external evidence.
9. Review the owning README after content or path changes and update stale
   navigation in the same logical change.
10. Do not add a router to a Spec package. `spec.md` owns the change contract,
    `plan.md` owns order and risk, and `tasks/` is the Task inventory; a
    package-level index only restates them and drifts from `tasks/`.
11. Keep a Stage 90 collection complete at all three of its levels. The
    registry routes each level and names its form; the reason they are distinct
    is that a collection outlives any one pack, a pack owns its own observation
    boundary and refresh trigger, and a member carries one dated observation or
    finding with its source. A
    collection with a missing level pushes one of those three jobs onto a
    document that does not own it.
12. Treat a sealed retirement as retiring a document, not a location. A
    reviewed, tracked document may later occupy a retired path; never restore
    the retired bytes there.
13. Preserve accepted decisions and completed evidence. Use successors,
    reciprocal lifecycle relationships, and the one Git object a Stage 98
    Retention Envelope names rather than rewriting history, leaving redirects,
    or keeping a second recovery ledger.
14. Run the checks selected by the affected paths and record evidence in the
    owning Task using [quality policy](quality.md).

Architecture Description은 요구와 연결된 품질 시나리오의 자극·환경·응답·측정값,
구조 선택과 ADR, 책임과 관계를 읽을 수 있는 context/container 관점을 설명한다.
Stage 90의 Audit는 기준·검사 범위·관측·심각도와 근거가 있는 발견·교정 owner·검증
상태를, Research는 질문·방법·출처별 주장·한계·권고를, Data는 범위와 출처·생성
방법·필드 의미와 단위·실제 사실·노후화 경계를 각각 소유한다. Registry는 지역
heading과 형식을, 양식은 작성 출발점을 제공하며 사실·판정·현재 권한은 각 문서의
실제 근거와 소유자가 결정한다.

Governed Markdown uses the ordered common prefix "title", "version",
"type", "status", "owner", and "updated"; later keys appear only when the
selected profile declares them. A new document starts at version "0.1.0" and
the first stable approval raises it to "1.0.0". Patch means a correction
without changed meaning, minor means compatible meaning or section growth, and
major means an incompatible role or contract change. Status and version are
independent. Native Skill packages keep name and description at the top and
place that six-key document envelope inside metadata. Preserve native
invocation, tool and model controls; metadata does not grant execution authority.

Markdown templates use the double-braced UPPER_SNAKE_CASE value grammar,
native templates use double-underscore UPPER_SNAKE_CASE markers, and author
guidance uses the registered HTML comment form. The shared value markers are
TITLE, OWNER, UPDATED, ARTIFACT_ID and PARENT_ID; parent_ids names exactly one
direct structural owner rather than a duplicate spec_id. Authored documents contain none
of those markers. Template history belongs to Registry contract version and
Git, not to the created document's "version".
Registry의 `document_language`가 문서별 언어를 소유한다. Navigation,
reference-pack, operations profile은 한국어가 기본이다. `.agents/`의 governed
Markdown에는 새 설명을 한국어로 쓰며 기존 영어 본문도 유효하다. 기계 key와 필수
heading은 등록된 문법을 유지한다. `.agents/`의 비 Markdown 파일과 `.claude/`,
`.codex/`의 non-README 파일은 영어 전용이다. README는 navigation profile을
따른다. 그 밖의 현재 문서, 특히 Stage 01~03의 non-README 저술은 영어를
유지하고 agent requirement section도 영어다. Template의 author prompt는
등록된 언어를 따르며, 생성된 현행 산출물을 손으로 고치거나 taxonomy 밖의
저술 트리를 만들지 않는다.

## Validation and Refresh

Stage 99 Registry의 선택적 `shared_contract`는 승인된 공동 판본과 이 지역
adapter를 식별한다. 고정된 원본 revision과 digest는 검토한 bytes를 가리키며,
`approval_ref`는 별도 공동 결정을 기록한다. Registry의 stage 값은 지역
선언이지 그 자체로 수용 증거가 아니다. 실제 지역 채택에는 소유 Task의 통합
검사·독립 검토·기준 판정이 필요하고, 공동 채택에는 각 저장소의 적용 근거가
필요하다. 이 adapter의 상태·언어·native 확장은 명시적으로 유지한다. 새 공동
판본에는 실제 소유자 결정과 채택 근거가 필요하며, 별도 지역 WGOV core를
만들지 않는다.

For Guide, Policy and Runbook, use the selected role's ordered sections and
place its existing Lifecycle Traceability table under Related Documents.
Classifications, prerequisites, controls, observations and recovery stay native
submodules in their relevant roles. Fill sections with concrete content; a
heading, comment, placeholder or empty fence is no operating instruction.
An inapplicable item states why and who owns the remaining boundary. A format
check cannot authenticate a current operator, live service or approval.

Run strict registry, Markdown-profile, link/owner, and lifecycle checks when
their contracts are affected. A deletion or consolidation requires replacement
coverage, consumer disposition, and applicable Archive recovery evidence in
the same logical change.

## Related Documents

- [Document Lifecycle](document-lifecycle.md)
- Stage 99 Author Guide (`docs/99.templates/README.md`)
- [Work Lifecycle](../workflows/work-lifecycle.md)
- Archive Index (`docs/98.archive/README.md`)
