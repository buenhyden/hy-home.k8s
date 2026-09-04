---
title: 'Terminal Document Retention and Archive Stage Taxonomy'
version: "1.0.0"
type: sdlc/architecture-decision
layer: "architecture"
status: proposed
owner: platform
updated: 2026-09-04
artifact_id: "ADR-0032"
---

# ADR-0032: Terminal Document Retention and Archive Stage Taxonomy

## Overview

This decision retains terminal governed documents instead of deleting them,
keeps them out of the active stages, and gives Stage 98 four subdirectories
whose roles are derived from what a terminal state means rather than from a
label chosen for the folder. It makes scoped normative amendments to ADR-0030
and ADR-0031 and supersedes neither: both remain accepted and authoritative in
every other respect.

## Context

[ADR-0030](./0030-authority-first-sdlc-and-agent-governance-convergence.md)
established consumer-first deletion with Git-backed recovery, and
[ADR-0031](./0031-current-corpus-retention-and-validation-ownership.md) made
Git the default terminal-history owner. Under those decisions a finished
package is deleted once its consumers reach zero, and Stage 98 keeps only an
index, migration ledgers, and tombstones.

That model answers where the bytes live but not where a reader looks. Git
recovery requires already knowing that a document existed and which commit
holds it, which is exactly what a reader of finished work does not know.

Meanwhile the active stages describe finished work as if it were current. The
[Stage 99 registry](../../99.templates/registry.json) classifies every profile
state as `mutable`, `current`, or `terminal`, so this is measurable rather than
a matter of opinion: on 2026-09-04 the active stages held 415 documents in a
terminal state, 399 of them `done` Stage 03 documents.

Stage 98's own subdirectories had drifted from their names. All seventeen
records under `tombstones/` carried `archive_reason: "superseded"` and a
non-null replacement, so the directory named for documents that end held only
documents that were replaced. The stage index meanwhile declared a null
replacement for `completed-lineage` and `retired` records, a vocabulary no
record used.

## Decision

### Retention replaces deletion for terminal governed documents

A terminal governed document is retained. Deletion is no longer the disposition
for a document whose work is finished.

This amends ADR-0030's consumer-first deletion and ADR-0031's Git-first
terminal history for terminal documents only. Git remains the recovery owner
for the exact source bytes, and remains the sole owner for anything this
decision does not classify.

### The Stage 98 taxonomy is derived from what a terminal state means

The registry already owns which states are terminal. Three distinct meanings
sit inside that class, and each gets one directory:

| Directory | Role | Derivation | Retained form |
| --- | --- | --- | --- |
| `migrations/` | The sealed record of a path transition itself | `archive/migration` in state `sealed` | The ledger document |
| `completed/` | Work that ran to an end | A terminal state naming no replacement: `done`, and `cancelled` inside a package that finished | The document itself |
| `superseded/` | A document a named successor replaced | A terminal `superseded` state with a replacement | A record |
| `tombstones/` | A document that ended alone with no successor | `withdrawn`, `rejected`, `cancelled`, `retired`, or `invalidated`, with no replacement and no finished package around it | A record |

A directory keeps its role when it has no members. `tombstones/` holds nothing
once the seventeen supersession records move to the directory that describes
them, and that is a correct empty set rather than a disused folder.

### An accepted decision that a successor replaced stays in the decision log

A `superseded` architecture decision is not archived. ADR-0031 already requires
predecessor decision bodies to remain in the Stage 02 decision log, and a
reader looking for why a decision changed looks at the log, not the archive.
`superseded/` therefore holds records for superseded documents of other
families.

### Retention still waits for consumer zero

A terminal document is retained only once no current document names it. This is
ADR-0030's consumer-first rule unchanged: retention replaces what happens when a
document reaches consumer zero, not the condition for reaching it.

Two superseded requirement packages are the standing case. Six current Stage 02
documents name REQ-0005 or REQ-0006 as the requirement the decision serves.
Sealing either as a record would take that link away, because a current document
may not link a record directly, and repointing the citation at their successor
REQ-0008 would claim those decisions were made under a requirement that did not
yet exist. Both stay in Stage 01 until the documents tracing to them are
themselves terminal.

This is the same shape as the decision-log exception above, stated on the
consumer axis rather than the family axis: a document that current work still
reaches through its own traceability has not finished being current.

### Retention mirrors the origin path

A retained document occupies `docs/98.archive/completed/<its own stage path>`
and nowhere else. The mirror is what makes a retention move provable: a
relocation that does not mirror its source is not a retention move, whatever it
is labelled.

### The retention unit is the package

A Stage 03 package is one unit of work, so it is retained whole or not at all.
Its spec, plan, and tasks link to each other, and splitting the package across
two Stage 98 directories would break exactly the coupling retention exists to
keep readable.

This is why `completed/` admits `cancelled` beside `done`. A task abandoned
while its package ran to completion is part of that package's history, and a
tombstone record for it would assert an ending the package did not have. A
document that ends alone, with no finished package around it, still gets a
record. `superseded` stays out of `completed/` either way: it names a
replacement, which is what `superseded/` describes.

### A retained copy preserves target identity, not bytes

A relative link resolves against the directory that holds it, so relocating a
document changes what its links mean. A retained copy therefore carries the
same content with its relative link prefixes re-based, and each link resolves
to the document the source link named.

The retention invariant is that target identity, not byte identity. The exact
source bytes stay recoverable from Git through the `source_commit` and
`source_blob` the retiring migration row pins.

For the same reason a retention row is `replaced` rather than `moved`: a
`moved` row asserts byte identity, which a re-based copy cannot satisfy.

### A retained document is not a sealed archive record

A document under `completed/` carries no ArchiveEnvelope, keeps its own profile
and terminal state, and may link to current documents. Its provenance is the
migration row that retired its origin path. Validation treats it as the
document it is, and a current document may cite it directly at its retention
path. Records under `superseded/` and `tombstones/` remain sealed records and
are unaffected.

## Explicit Non-goals

- This decision does not retain untracked or generated output, secrets, or
  anything outside the governed document stages.
- It does not create a second authority. A retained document states no current
  requirement, decision, or contract, and citing one never makes it current.
- It does not change how migration ledgers or sealed records are validated.
- It does not name a retention class for any state the registry classifies as
  `mutable` or `current`. A document still in progress stays where it is,
  however old it looks.
- It routes only the stages whose retention is implemented. A terminal state in
  a family with no retention route yet stays in place until one is added.

## Consequences

Readers find finished work by browsing rather than by naming a commit, and the
active stages describe only current intent.

Every retention move needs a sealed migration row, so retiring a package costs
a reviewed ledger entry rather than a deletion. That is the intended cost: it
keeps the origin path's retirement provable.

Retained copies are not byte-identical to their sources, so a reader comparing
a retained document with its Git original will see link prefixes differ. The
migration row is what reconciles them.

Citations of a retained package are repointed to its retention path instead of
being rewritten or deleted, so the citing document keeps its meaning.

A package is retained only when every document in it is terminal, so one
unfinished task holds the whole package in the active stage. That is the
intended cost of keeping the package readable as a unit.

The seventeen existing supersession records move directory, which changes the
paths the stage index and the declared rehome table name.

## Alternatives

**Keep deleting and rely on Git.** Rejected: it answers where the bytes live
but not where a reader looks, which is the problem this decision addresses.

**Leave terminal work in the active stages.** Rejected: the active stage then
describes finished work as current, which is the other half of the problem.

**Name the retention classes independently of the registry.** Rejected, and
tried first: an earlier draft of this decision named a `stale` class, which
collides with `stale`, a `current` state in the `data` family. Deriving the
taxonomy from the registry's own terminal classification removes the collision
by construction.

**Seal each retained document as an archive record.** Rejected: an
ArchiveEnvelope replaces the document's own identity metadata, so the retained
artifact would no longer be the document that was retained.

## Traceability

### Lifecycle Traceability

| Decision lineage | Replacement relation | Affected Spec |
| --- | --- | --- |
| [ADR-0030](./0030-authority-first-sdlc-and-agent-governance-convergence.md) and [ADR-0031](./0031-current-corpus-retention-and-validation-ownership.md) | Scoped amendment of their deletion and Git-first terminal-history clauses for terminal documents; both remain accepted and are not superseded | [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |

### Implementation Traceability

| Decision element | Implementation owner | Evidence |
| --- | --- | --- |
| Retention routes and record routes | `docs/99.templates/registry.json` | Retained Stage 03 paths classify to their own profiles; record directories classify to `archive/tombstone` |
| Ledger-driven retention move | `scripts/validate-document-lifecycle.py` | A retention rehome is admitted only for a mirrored target whose source is terminal |
| A retained document is not a record | `scripts/archive_validation.py` | `completed/` excluded from record inventory and from current-to-archive coupling |
| First retirement ledger | MIG-0013 | Sealed rows pin each origin path's commit, blob, and digest |
