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

## Workflow Steps

1. Confirm what happened to the document and pick one disposition. ADR-0038
   (`docs/02.architecture/decisions/0038-six-disposition-archive-stage.md`)
   owns the six dispositions, what each must name, and which may be cited; the
   Stage 99 registry's `retention_classes` binds each retention class to the
   source states it admits. Record the disposition approval in the owning Task.
2. Check the preconditions. Every document in a package must be terminal, or
   the whole package stays. No current document may still cite the source as
   authority: repoint each current citation to the successor or the current
   route first, because retention waits for consumer zero.
3. For a retention class, move the body to the class directory at its own
   stage path, keeping its profile, identity, and terminal state. Re-base only
   relative link prefixes, with `rebase_relative_links` in
   `scripts/archive_dispositions.py`, so every link keeps its target.
4. For a route disposition, author the body-less record from the
   registry-selected `archive/route-tombstone` or `archive/scope-migration`
   form.
5. Add one Retention Catalog row to the Stage 98 index that names the record
   and `<commit>:<original path>`, where the commit is the comparison base. Add
   no blob, digest, branch SHA, or redirect.
6. Validate the exact index with the staged QA profile. The lifecycle gate
   proves the envelope object, the source state, and link-rebase equivalence;
   the links-and-owners gate proves the citation boundary; the archive cutover
   gate proves catalog parity.

## Boundaries

A retained body, a route record, a frozen record, and a frozen ledger do not
change afterwards. A mistake found later needs its own decision. Git remains the
recovery owner for exact source bytes.

## Outputs

The retained body or route record, its catalog row, repointed citations and
indexes, and the staged QA result for that exact index.
