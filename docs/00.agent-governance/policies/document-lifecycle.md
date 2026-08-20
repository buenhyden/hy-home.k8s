---
title: 'Document Lifecycle Policy'
type: governance/reference
status: active
owner: platform
updated: 2026-08-20
---

# Document Lifecycle Policy

## Overview

This policy governs document promotion, blocking, supersession, retirement,
withdrawal, sealing, and historical recovery across the repository.

## Authority Boundary

The [Stage 99 registry](../../99.templates/registry.json) is the sole machine
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
- Router READMEs have neither an artifact ID nor a lifecycle state.
- Templates identify their registry profile and do not own a destination path.
- Material Stage 99 index/worktree drift fails staged validation; the staged
  registry is the commit claim.

## Validation and Refresh

Lifecycle validators use bounded regular-file reads, strict UTF-8, explicit
subprocess timeouts, and stage-zero Git bytes. Illegal edges, incomplete
reciprocal links, oversize or undecodable authority input, and material staged
drift are failures. Review this policy whenever the registry lifecycle catalog
changes.

## Related Documents

- [Software Development Lifecycle](../sdlc.md)
- [Governance Hub](../README.md)
- [Document Profile Registry](../../99.templates/registry.json)
- [Document Authoring Policy](../rules/document-authoring.md)
