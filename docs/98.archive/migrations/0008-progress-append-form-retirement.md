---
title: "MIG-0008: Progress Append Form Retirement"
type: "content/archive-migration"
status: "draft"
owner: "platform"
updated: "2026-08-30"
artifact_id: "MIG-0008"
migration_id: "MIG-0008"
---

# MIG-0008: Progress Append Form Retirement

## Overview

This record designs the retirement of
`docs/99.templates/templates/governance/progress.template.md`, the append
fragment for the agent progress ledger, under Spec 0054 WP-012. It is open and
not executed: the retirement is blocked, and the blocking clause is named below.

The ledger it appended to was retired by
[MIG-0007](0007-agent-progress-ledger-retirement.md). The form describes how to
add an entry to a file that no longer exists and cannot be recreated: the memory
README now states that no progress ledger lives under `memory/`. Two registry
profiles depend on it. `governance/progress-ledger` matched exactly the retired
ledger path and now routes nothing. `governance/progress-entry` matched exactly
this form and carried the sole `appendContract` in the registry, whose
`parentProfileId` was `governance/progress-ledger`.

### Why the retirement is blocked

The form is a `moved` target of the sealed `MIG-0004`, listed in that record's
Stage 99 action targets. `validate_mig0004_historical_targets` already proves
those moves against a pinned commit rather than the current tree, which is the
recovery evidence. `_validate_mig0004_rows_and_targets` additionally requires
every Stage 99 target to be present in the current staged inventory, so
deleting the form raises `RECOVERY-MIGRATION-TARGET: current staged target set
differs`. `MIG-0004` is sealed and cannot be edited to lift that requirement.

This is the same shape MIG-0007 resolved for the ledger: a Git-side proof plus a
redundant current-tree presence requirement. Releasing it is a change to a
completed-migration proof whose row census and target sets are pinned
constants, so it is a separate classification under the Spec 0063 discard-list
rule and not a side effect of this Task. The form and both profiles stay in
place until that classification is approved.

Sealing this record requires that release. Until then it carries the row
unsealed, so it composes no target and changes no redirect.

## Migration Ledger

<!-- archive-migration-ledger:v1 format=json -->

```json
[
  {
    "legacy_path": "docs/99.templates/templates/governance/progress.template.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "deleted",
    "replacement": null,
    "source_commit": "959bd64d9ba278cf8ae9eb2b9f39cff73d28b636",
    "source_blob": "41eb12709d2a75ba137df87143774985d2401247",
    "content_sha256": "b8261f60bf201d7bf8be0f7d8a7978dc02c070f6ea695bccb40e85b99ed7f5bb",
    "reason": "Retire the append fragment for the progress ledger MIG-0007 retired; its only destination is gone and the memory README forbids recreating one, so the form has no document it can produce."
  }
]
```

## Recovery

The form is still tracked, so recovery is not yet needed. When the row seals,
recover its bytes with `git show
959bd64d9ba278cf8ae9eb2b9f39cff73d28b636:docs/99.templates/templates/governance/progress.template.md`
and verify both `source_blob` and `content_sha256` against the row above. The
row's action is `deleted`, so it composes no replacement target and resolves
through the Archive index.

### Historical consumers

This record admits no historical consumer. No current document renders a link
to the form; the Stage 03 records that name it do so as prose inside terminal
Plan and Spec bodies, which is not a rendered link and needs no redirect.

<!-- archive-historical-consumers:v1 format=json -->

```json
[]
```
