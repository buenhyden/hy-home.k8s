---
title: "Document Authoring Policy"
version: "1.1.0"
type: "governance/rule"
status: "active"
owner: "platform"
updated: "2026-09-04"
---

# Document Authoring Policy

## Overview

Select the document owner by purpose, author from its canonical template, and
close the change with traceable evidence.

## Authority Boundary

[Stage 99 README](../../docs/99.templates/README.md) is the human authoring guide.
Its [registry](../../docs/99.templates/registry.json) alone owns exact paths,
profiles, IDs, sections, metadata, lifecycle, and relationships. This policy
owns agent procedure, not a second machine contract.

## Governance Context

Use [SDLC flow](sdlc.md) to distinguish durable requirements, current
architecture, change-specific behavior, and operating knowledge. Stage numbers
express ownership, not a one-way waterfall. Root `DESIGN.md` owns UI and
design-system rules only.

## Current Contract

1. Identify the owning stage and normalize the final repository-relative path.
2. Resolve exactly one registry profile and read its canonical template before
   creating or restructuring a document. No match or multiple matches is a
   stop condition.
3. Use the profile-owned initial status, metadata, sections, and relationships.
   Do not assume every profile starts at "draft". Router READMEs participate in
   the governed envelope with an "active" routing constant, but have neither
   artifact identity nor lifecycle binding.
4. Take the frontmatter key set and its order from the selected profile, and
   each key's value grammar from the
   [frontmatter schema](../../docs/99.templates/contracts/frontmatter.schema.json).
   Every string, date, version, and identity scalar uses double quotes. A
   "title" never repeats the document's "artifact_id": identity is already a
   key, and a title that restates it carries no information.
5. Treat a key the profile omits as a key the document has no business
   declaring. `layer` names the numbered stage a document lives in, so common governance
   sits above that numbering and a Stage 99 form is not the document it
   produces; neither declares one. A profile that declares no `artifact_id`
   describes something the repository does not give a stable identity.
6. Replace prompts with concrete content, use complete stable IDs for
   traceability, and calculate links from the final target path.
7. Keep a Requirement Package solution-independent. Put executable interface
   contracts and change-scoped Technical Approach and Acceptance Contract in
   the owning Spec package; put order, risks, verification, and rollback in its
   Plan and execution evidence in its Task records.
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
    reciprocal lifecycle relationships, and minimal Git-backed recovery
    mappings rather than rewriting history or leaving redirects.
14. Run the checks selected by the affected paths and record evidence in the
    owning Task using [quality policy](quality.md).

All governed Markdown starts with the ordered common prefix "title", "version",
"type", "status", "owner", and "updated"; later keys appear only when the
selected profile declares them. A new document starts at version "0.1.0" and
the first stable approval raises it to "1.0.0". Patch means a correction
without changed meaning, minor means compatible meaning or section growth, and
major means an incompatible role or contract change. Status and version are
independent.

Markdown templates use the double-braced UPPER_SNAKE_CASE value grammar,
native templates use double-underscore UPPER_SNAKE_CASE markers, and author
guidance uses the registered HTML comment form. Authored documents contain none
of those markers. Template history belongs to Registry contract version and
Git, not to the created document's "version".
Governance and agent execution sections remain English. Human-facing root,
folder, requirement, operations, and reference explanation may use Korean;
source, authority, and machine-contract sections remain English-first. Never
hand-edit generated current output or create an off-taxonomy authored tree.

## Validation and Refresh

Run strict registry, Markdown-profile, link/owner, and lifecycle checks when
their contracts are affected. A deletion or consolidation requires replacement
coverage, consumer disposition, and applicable Archive recovery evidence in
the same logical change.

## Related Documents

- [Document Lifecycle](document-lifecycle.md)
- [Stage 99 Author Guide](../../docs/99.templates/README.md)
- [Work Lifecycle](../workflows/work-lifecycle.md)
- [Archive Index](../../docs/98.archive/README.md)
