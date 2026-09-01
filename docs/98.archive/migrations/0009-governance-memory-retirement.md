---
title: "MIG-0009: Governance Memory Retirement"
type: "content/archive-migration"
status: "sealed"
owner: "platform"
updated: "2026-08-31"
artifact_id: "MIG-0009"
---

# MIG-0009: Governance Memory Retirement

## Overview

This reviewed ledger records the retirement of `docs/00.agent-governance/memory/`
under Spec 0065. Two rows retire the directory's only remaining file and the
form that no longer has a directory to fill:
`docs/00.agent-governance/memory/README.md` and
`docs/99.templates/templates/governance/memory.template.md`. The registry
profile `governance/memory`, whose path pattern matched only members the
directory never held, retires with them.

The directory is empty of memory documents. `MIG-0007` retired the progress
ledger it once held, and `MIG-0008` retired the append form that produced that
ledger's entries. What remained was a README explaining that the directory
holds nothing, and a template for documents no profile could admit once the
directory closed.

### The retained router clause is superseded

`TSK-0054-0003` recorded that "the retained memory router is not a deleted
Migration source", and scheduled its extracted context policy for `draft`
publication in WP-003A and `draft -> active` activation in WP-003B. That clause
was written before `MIG-0007`. It described a router that routed a reader to
the progress ledger. The ledger is gone, so the routing role is gone, and a
document whose stated purpose is to route to a retired path is not a retained
owner.

This record supersedes only that clause. WP-003B still owes the `draft ->
active` activation of
[context and memory policy](../../00.agent-governance/policies/context-and-memory.md),
which this record does not perform and does not claim. No ownership gap opens
in the meantime: that policy's own Authority Boundary names the owners that
govern until activation, and both
[agent execution](../../00.agent-governance/policies/agent-execution.md) and
[approval and safety](../../00.agent-governance/policies/approval-and-safety.md)
are active.

The one durable sentence the README carried, that current status, commands,
verification and handoff belong to the owning Spec Task and never to a memory
document, is already the second bullet of that policy's Current Contract. It is
not lost.

## Migration Ledger

<!-- archive-migration-ledger:v1 format=json -->

```json
[
  {
    "legacy_path": "docs/00.agent-governance/memory/README.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "deleted",
    "replacement": null,
    "source_commit": "a393ab066fdb31a5a2e20f323b230caf477bdef1",
    "source_blob": "78f93fe59ea2ea19baed11f1bc8ba03703978adb",
    "content_sha256": "d6577bb3cfc849fcdfdb956a9781ded21b95ee35e9aa11490827b4efca59bf1f",
    "reason": "Retire the collection index of a directory that holds no memory document; its routing role ended with the ledger MIG-0007 retired, and its durable rule is already carried by the context and memory policy."
  },
  {
    "legacy_path": "docs/99.templates/templates/governance/memory.template.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "deleted",
    "replacement": null,
    "source_commit": "959bd64d9ba278cf8ae9eb2b9f39cff73d28b636",
    "source_blob": "b7f80ea24323e6e4b956dea9531a64827d488e48",
    "content_sha256": "eaf93f9007ef3019b690d4f86431367c2dfc422c850bf4964f6425fa49848572",
    "reason": "Retire the form for a document class whose only directory closes with this record; the governance/memory profile that named it as its template retires in the same change."
  }
]
```

## Recovery

Recover the retired bytes with `git show <source_commit>:<legacy_path>` for
either row and verify both `source_blob` and `content_sha256` against that row.
Both actions are `deleted`, so neither composes a replacement target; both
resolve through the [Archive index](../README.md).

### Historical consumers

Nine current documents render a link to the retired README. Two are mutable
Stage 00 owners, the governance hub index and the context and memory policy;
their links were repointed rather than admitted, so neither is registered here.
Of the seven that cannot be edited, four already resolve through `MIG-0005`,
which registers them as its own consumers. A second registration would make the
consumer identity ambiguous, so the three below are the remainder.

Each is a Stage 90 historical observation body, whose recorded observations are
not rewritten to match a later tree. Registration is what admits such a link;
immutability alone is not, because registration records that a reviewer
examined the citation at a named commit.

<!-- archive-historical-consumers:v1 format=json -->

```json
[
  {
    "source_commit": "a393ab066fdb31a5a2e20f323b230caf477bdef1",
    "paths": [
      "docs/90.references/audits/2026-07-02-whia/harness-loop-implementation-audit.md",
      "docs/90.references/audits/2026-08-09-wgia/llm-wiki-memory-and-knowledge-management.md",
      "docs/90.references/research/2026-08-08-wer/agent-memory-tiers-and-management.md"
    ]
  }
]
```
