---
title: "Document Lifecycle Policy"
version: "1.1.0"
type: "governance/rule"
status: "active"
owner: "platform"
updated: "2026-09-04"
---

# Document Lifecycle Policy

## Overview

This policy governs document promotion, blocking, supersession, retirement,
withdrawal, sealing, and historical recovery across the repository.

## Authority Boundary

The [Stage 99 registry](../../docs/99.templates/registry.json) is the sole machine
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
- A terminal document is retained rather than deleted. It leaves the active
  stage for the Stage 98 directory whose role matches why it ended, and the
  move is proved by a sealed migration row that pins the origin path, commit,
  and blob. Which states are terminal stays with the registry; this policy adds
  only the obligation that reaching one moves the document.
- Frozen legacy Archive payloads retain their original generation, bytes, and
  historical links. Current validators classify them as historical evidence
  and do not rewrite them to the current envelope.

## Validation and Refresh

Lifecycle validators use bounded regular-file reads, strict UTF-8, explicit
subprocess timeouts, and stage-zero Git bytes. Illegal edges, incomplete
reciprocal links, oversize or undecodable authority input, and material staged
drift are failures. Review this policy whenever the registry lifecycle catalog
changes.

## Related Documents

- [Software Development Lifecycle](sdlc.md)
- [Governance Hub](../README.md)
- [Document Profile Registry](../../docs/99.templates/registry.json)
- [Document Authoring Policy](document-authoring.md)
- [Archive Stage](../../docs/98.archive/README.md)
