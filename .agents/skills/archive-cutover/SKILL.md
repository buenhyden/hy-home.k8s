---
name: "archive-cutover"
description: "Use when a finished governed document or whole Spec package leaves its active stage for docs/98.archive: retaining completed work, relocating a sealed record, or sealing the migration ledger that proves the move. Also use when a retention move fails the lifecycle, link, or archive cutover gates, or when a citation of a retained document needs repointing."
disable-model-invocation: true
---

Read `.agents/governance/approval-and-safety.md` and the selected role before
using this procedure. Skill invocation does not authorize additional actions.

# archive-cutover

Move a terminal document out of its active stage so that the retirement of its
origin path stays provable. The move is cheap to make and expensive to make
wrong: Stage 98 is byte-immutable once sealed, and the migration ledger is the
only machine evidence of where a document went.

## When NOT to Use

- Choosing the profile or template for a new current document; use `docs-stage-routing`.
- Repairing drift inside a document that stays current; use `docs-stage-conformance`.
- Recovering or rewriting sealed history; that needs its own approval.

## Workflow Steps

1. Confirm the move is a retention, not a deletion or a rewrite.
   ADR-0032 (`docs/02.architecture/decisions/0032-completed-and-terminal-document-retention.md`)
   owns which terminal state maps to which Stage 98 directory and what form is
   retained; read it rather than inferring a class from a directory name.
2. Check the preconditions it sets. Every document in a package must be
   terminal, or the whole package stays. No current document may still name
   the source: retention waits for consumer zero, and a citation that current
   traceability still needs keeps the source in its stage.
3. Allocate the next unused `MIG-` identity through the Stage 99 registry and
   author the ledger from the registry-selected `archive/migration` template.
   Record one row per source at the exact source commit, blob, and digest. Use
   `moved` only when the bytes are identical; a retained copy whose link
   prefixes were re-based is `replaced`.
4. Make the move itself so the target mirrors the origin path, re-basing only
   relative link prefixes so every link keeps its target identity.
5. Repoint each remaining citation of a retained package at its retention path
   and update the stage indexes the move touches. A current document reaches
   a record through the archive index, never directly.
6. Seal the ledger only over the reviewed finite mapping, then prove it: run
   `scripts/archive_recovery.py` against the record as its template's Recovery
   section describes, and validate the exact index with the staged QA profile.
   The lifecycle, links-and-owners, and archive-cutover gates are the ones a
   wrong row fails.

## Boundaries

A sealed ledger and a sealed record do not change afterwards. A mistake found
later is corrected by a new migration, never by editing either. Git remains the
recovery owner for exact source bytes.

## Outputs

A sealed migration ledger, the mirrored retained documents or records it
proves, repointed citations and indexes, and the staged QA result for that
exact index.
