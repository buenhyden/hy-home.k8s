---
name: "archive-cutover"
description: "Use when a governed document or whole Spec package leaves its active stage for a Stage 98 disposition, when retention fails current lifecycle, link, or Archive integrity checks, or when a citation of a retained document needs repointing."
metadata:
  title: "Archive Cutover"
  version: "1.1.1"
  type: "governance/skill"
  status: "active"
  owner: "platform"
  updated: "2026-10-09"
disable-model-invocation: true
---

Read `.agents/governance/approval-and-safety.md` and the selected role before
using this procedure. Skill invocation does not authorize additional actions.

# archive-cutover

Move a document that is no longer current into the Stage 98 disposition that
matches what happened to it, so the move stays provable without a second
recovery ledger. The move is cheap to make and expensive to make wrong: once a
body or route record is in Stage 98 it does not change, and the Retention
Catalog row is the only machine evidence of where it came from.

## When NOT to Use

- Choosing the profile or template for a new current document; use `docs-stage-routing`.
- Repairing drift inside a document that stays current; use `docs-stage-conformance`.
- Recovering or rewriting frozen history; that needs its own approval.
- Moving a current document between active stages; identity lineage tracks a
  move that keeps its `artifact_id`, family, and state without a Stage 98 record.

## Workflow Steps

1. Confirm what happened to the unit and pick one disposition under the
   [current lifecycle policy](../../governance/document-lifecycle.md).
   The Stage 99 registry's
   `retention_classes` binds each class to the anchor states it admits, and
   `archive_citation` decides what may be cited. Verify the actual disposition
   approval and promoted durable meaning, then record the decision and current
   owner in the owning Task.
2. Check the preconditions. A spec package or an Incident bundle leaves as one
   unit, never member by member. Check the class and member states in the
   immutable comparison-base source. Normally its anchor must be admitted by
   the class and every other lifecycle member must be terminal or explicitly
   admitted by the unit rule. For the `spec-package` `completed/` route alone,
   the source Spec and Plan may both be `approved` when the same source package
   passes completion closure: assigned Tasks are completed, each required
   criterion has one accepted verdict, required adverse evidence is resolved,
   and lasting meaning has a named current owner. `approved` status alone does
   not qualify. No current document may still cite the source as authority:
   repoint each current citation to the successor or the current route first,
   because retention waits for consumer zero.
3. For a retention class, move the whole unit to the class directory at its
   own stage path with `git mv`, keeping its profile, identity, and source
   state. Change no path, file mode, or byte, links included; a retained body's
   links are read at its original path in the envelope commit.
4. For a route disposition, author the body-less record from the
   registry-selected `archive/route-tombstone` or `archive/scope-migration`
   form.
5. Add one Retention Catalog row to the Stage 98 index that names the retained
   unit, a package or bundle directory or one document, and
   `<commit>:<original path>`, where the commit is the comparison base. Add no
   blob, digest, branch SHA, or redirect.
6. Validate the exact index with the selected local staged QA profile. The
   lifecycle check covers the envelope object, anchor and member states,
   applicable source-package completion, and entry-for-entry equality; the
   links-and-owners check covers citation decisions. The current Archive
   integrity check covers catalog routes and
   retained-content invariants over its declared input. The historical
   cutover completion proof remains in its original evidence owner and is
   not recreated by a new placement check.

## Boundaries

A retained body, a route record, a frozen record, and a frozen ledger do not
change afterwards. A mistake found later needs its own decision. Git remains the
recovery owner for exact source bytes. A Retention Assessment Hold blocks any
later whole-unit removal under its separately approved disposition; cutover
eligibility does not authorize that removal.

## Outputs

The retained body or route record, its catalog row, repointed citations and
indexes, and the staged QA result for that exact index.
