---
name: "archive-cutover"
description: "Use when a governed document or whole Spec package that is no longer current leaves its active stage for a Stage 98 disposition, when a disposition fails the lifecycle, link, or archive cutover gates, or when a citation of a retained document needs repointing."
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

1. Confirm what happened to the unit and pick one disposition. ADR-0039
   (`docs/02.architecture/decisions/0039-unit-archive-retention-and-citation-table.md`)
   owns the retention units, exact retention, and the citation table on top of
   the six dispositions ADR-0038 named. The Stage 99 registry's
   `retention_classes` binds each class to the anchor states it admits, and
   `archive_citation` decides what may be cited. Record the disposition
   approval in the owning Task.
2. Check the preconditions. A spec package or an Incident bundle leaves as one
   unit, never member by member. Its anchor's state must admit the class and
   every other member must be terminal in its own family, or the whole unit
   stays. No current document may still cite the source as authority: repoint
   each current citation to the successor or the current route first, because
   retention waits for consumer zero.
3. For a retention class, move the whole unit to the class directory at its
   own stage path with `git mv`, keeping its profile, identity, and terminal
   state. Change no path, file mode, or byte, links included; a retained body's
   links are read at its original path in the envelope commit.
4. For a route disposition, author the body-less record from the
   registry-selected `archive/route-tombstone` or `archive/scope-migration`
   form.
5. Add one Retention Catalog row to the Stage 98 index that names the retained
   unit, a package or bundle directory or one document, and
   `<commit>:<original path>`, where the commit is the comparison base. Add no
   blob, digest, branch SHA, or redirect.
6. Validate the exact index with the staged QA profile. The lifecycle gate
   proves the envelope object, the anchor and member states, and entry-for-entry
   equality; the links-and-owners gate proves the citation decision; the archive
   cutover gate proves catalog parity and re-verifies every catalog row.

## Boundaries

A retained body, a route record, a frozen record, and a frozen ledger do not
change afterwards. A mistake found later needs its own decision. Git remains the
recovery owner for exact source bytes.

## Outputs

The retained body or route record, its catalog row, repointed citations and
indexes, and the staged QA result for that exact index.
