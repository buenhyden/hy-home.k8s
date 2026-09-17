---
title: "Document Lifecycle Policy"
version: "1.7.0"
type: "governance/rule"
status: "active"
owner: "platform"
updated: "2026-09-17"
---

# Document Lifecycle Policy

## Overview

This policy governs document promotion, blocking, supersession, retirement,
withdrawal, sealing, and historical recovery across the repository.

## Authority Boundary

The Stage 99 registry (`docs/99.templates/registry.json`) is the sole machine
owner for lifecycle states, directed transitions, and the internal `mutable`,
`current`, and `terminal` validation classes. Documents carry only their
profile status. This policy explains evidence obligations and does not repeat
the machine transition table.

## Governance Context

Stable identities are append-only and never reused. Mutable and current
documents may change only within their selected profile contract. Immutable
Stage 98 and Stage 90 evidence is not rewritten to satisfy a later profile.
Transition-only legacy routes remain a finite fail-closed projection until
their owning migration work package moves them.

## Current Contract

- A proposed status change must be one directed edge declared by the selected
  profile family.
- Meaningful supersession requires the old owner to link `superseded_by` to the
  successor and the successor to link `supersedes` back in the same change.
- A mutable or current owner cannot disappear without replacement coverage,
  consumer disposition, and applicable Git-backed recovery evidence.
- Router READMEs carry an "active" routing constant but have neither an
  artifact ID nor a lifecycle binding.
- Templates project their source profile, start no lifecycle of their own, and
  do not own a destination path.
- Material Stage 99 index/worktree drift fails staged validation; the staged
  registry is the commit claim.
- A governed document that is no longer current is retained rather than
  deleted. A document in Stages 01, 02, 03, 05, or 90 leaves for the Stage 98
  disposition that matches what happened to it, and a superseded architecture
  decision follows the same rule. Stage 99 follows its retention modes: a
  retired form leaves through `git-history-only` with no Stage 98 record, and a
  stage or collection index is retained in place. Which states are terminal stays with the
  registry; this policy adds only the obligation that reaching one moves the
  document, and that each disposition needs its own authorization.
- Stage 98 has six dispositions of two kinds. A retention class holds a whole
  once-current body under the profile that governed it: `completed/` names what
  it promoted, `superseded/` names the document that replaced it, `retired/`
  names why a rule or scope was withdrawn with no successor, and `resolved/`
  holds a closed Incident bundle with its published Postmortem and names the
  closure evidence and current corrective-work owner. A route disposition holds
  no body: `tombstones/` names a retired route, its successor or absence, and
  the reason, and `migrations/` names a moved scope and its current owner as
  `MIG-####`. A disposition's directory is created by the change that first
  uses it.
- Citability is decided by the registry's ordered `archive_citation` table,
  and every citation check consumes that one decision. An active-stage document
  may cite the index, `completed/`, and, as historical evidence, `resolved/`.
  It cites the successor instead of a `superseded/` body, and the current route
  instead of a `retired/` body, a tombstone, or a migration. Before any class
  admission, no source outside Stage 98 links a unit judged `withdrawn` or
  `invalidated` or no longer `retained`. An
  `operation/incident` or `operation/postmortem` may also cite a body in any
  retention class as historical evidence. No document outside Stage 98 links a
  route record or a frozen sealed record; it names a frozen record by
  identifier through the index.
- Retention follows the profile: frozen bodies remain immutable, while a
  Git-history-only disposition retains recoverable provenance without a
  compatibility copy. No Stage 98 record carries a second recovery ledger: no
  redirect, path ledger, self-designed body digest, branch SHA, or recovery
  commit. The Stage 98 catalog's Retention Envelope names the source Git object
  once as `<commit>:<original path>`, and normal Git history recovers it.
- ADR-0038 recorded this model and superseded ADR-0032. ADR-0039 supersedes
  ADR-0038, keeps its six dispositions, and retains units exactly. A spec
  package is one unit with its anchor `spec.md`, an Incident bundle is one unit
  with its anchor `incident.md` and a published Postmortem, and any other
  document is its own unit. The anchor's state admits the class, and every
  other member is terminal in its own family. The retained path equals the
  source Git object entry for entry, links included, and its catalog row names
  a blob or a tree. The sixteen bodies ADR-0038 retained with rebased links
  keep that generation and cannot grow in number.
- ADR-0040 supersedes ADR-0039 and keeps its units and exact retention. A
  retained unit is frozen against unapproved change, not kept forever: its
  bytes are never edited, renamed, recreated, or partly deleted, and the one
  admitted change is an approved removal of the whole unit, after which its
  availability is `git-history-only`, its catalog row stays, and its envelope
  still verifies. Removal is not purification and needs its own approval.
- A unit's current evidential value is judged in the Archive index's
  Retention Assessment table, never in the frozen body. A unit without a row
  is `unreviewed` and `retained`; every other judgment names a current Task,
  Spec, or decision that records it, a `superseded` judgment names the current
  owner, and a Hold blocks removal. A row never leaves and a removed unit never
  returns. `invalidated` judges old evidence and does not rewrite the old
  state. The registry owns the values and conditions, and `purged` stays
  reserved until a security-approved purification contract exists.
- An envelope commit is reachable from the registry-named default branch, so a
  unit's source is integrated before the change that retains it.
- The Stage 99 registry declares the units, binds each retention mode to the
  profiles that may use it, routes a retained body under its original profile,
  and binds each retention class to the anchor states it admits. Frozen records
  and ledgers route by exact path, so no new sealed record or path ledger can be
  created. The lifecycle gate admits a retained unit through its catalog row,
  and full validation re-verifies every row against the object it names.
- A document that moves between active stages in one change, keeping its
  `artifact_id`, family, and state, is tracked by identity lineage and needs no
  Stage 98 record. A scope migration is recorded only when a consumer outside
  the repository reads the moved paths.
- Frozen Stage 98 content keeps its generation. Sealed records with their
  ArchiveEnvelope and digests, migration ledgers with pinned rows, and retained
  packages keep their bytes and historical links; validators classify them as
  historical evidence and never rewrite them to the current form.

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
