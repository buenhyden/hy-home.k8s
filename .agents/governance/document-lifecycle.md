---
title: "Document Lifecycle Policy"
version: "1.4.0"
type: "governance/rule"
status: "active"
owner: "platform"
updated: "2026-09-15"
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
  deleted. It leaves Stages 01, 02, 03, 05, 90, and 99 for the Stage 98
  disposition that matches what happened to it, and a superseded architecture
  decision follows the same rule. Which states are terminal stays with the
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
- Citability follows from what a family names. An active-stage document may
  cite `completed/` and, as historical evidence, `resolved/`. It cites the
  successor instead of a `superseded/` body, and the current route instead of a
  `retired/` body, a tombstone, or a migration.
- Retention follows the profile: frozen bodies remain immutable, while a
  Git-history-only disposition retains recoverable provenance without a
  compatibility copy. No Stage 98 record carries a second recovery ledger: no
  redirect, path ledger, self-designed body digest, branch SHA, or recovery
  commit. The Stage 98 catalog's Retention Envelope names the source Git object
  once as `<commit>:<original path>`, and normal Git history recovers it.
- ADR-0038 records this model and supersedes ADR-0032. The Stage 99 registry
  routes a retained body under its original profile and binds each retention
  class to the terminal states it admits. Frozen records and ledgers route by
  exact path, so no new sealed record or path ledger can be created. The
  lifecycle gate admits a retained body through its catalog row and a move
  through a body-less scope migration the catalog names.
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
