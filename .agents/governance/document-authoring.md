---
title: "Document Authoring Policy"
version: "3.0.0"
type: "governance/rule"
status: "active"
owner: "platform"
updated: "2026-10-08"
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
    boundary and refresh trigger, and a member carries one dated finding. A
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
The registry's `document_language` contract owns each document's language:
Navigation, reference-pack and operations profiles are Korean-first, files under `.agents/`,
`.claude/`, and `.codex/` are English only, every other current document is
English-first, agent requirement sections stay English, and a template writes
its author prompts in its output's language. Never hand-edit generated current
output or create an off-taxonomy authored tree.

## Validation and Refresh

The Stage 99 Registry's optional `shared_contract` identifies the one common
review candidate and the local adapter. A candidate digest identifies reviewed
bytes, not approval. Missing source revision or approval reference stays null;
final common approval and actual local/joint adoption need their own evidence.
The locally reviewed state, language and native extensions remain explicit in
this adapter; a future common edition needs its actual owner decision and
adoption evidence. Do not establish another local WGOV core.

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
