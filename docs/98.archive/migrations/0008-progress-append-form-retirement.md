---
title: "MIG-0008: Progress Append Form Retirement"
type: "content/archive-migration"
status: "sealed"
owner: "platform"
updated: "2026-08-31"
artifact_id: "MIG-0008"
---

# MIG-0008: Progress Append Form Retirement

## Overview

This reviewed ledger records the retirement of
`docs/99.templates/templates/governance/progress.template.md`, the append
fragment for the agent progress ledger, under Spec 0054 WP-012 and Spec 0065.

The ledger it appended to was retired by
[MIG-0007](0007-agent-progress-ledger-retirement.md). The form describes how to
add an entry to a file that no longer exists and cannot be recreated: the memory
README now states that no progress ledger lives under `memory/`. Two registry
profiles depend on it. `governance/progress-ledger` matched exactly the retired
ledger path and now routes nothing. `governance/progress-entry` matched exactly
this form and carried the sole `appendContract` in the registry, whose
`parentProfileId` was `governance/progress-ledger`.

### What the retirement required first

The form is a `moved` target of the sealed `MIG-0004`, listed in that record's
Stage 99 action targets. `validate_mig0004_historical_targets` proves those
moves against a pinned commit rather than the current tree, which is the
recovery evidence. `_validate_mig0004_rows_and_targets` additionally required
every Stage 99 target to be present in the current staged inventory, so
deleting the form raised `RECOVERY-MIGRATION-TARGET: current staged target set
differs`. `MIG-0004` is sealed and could not be edited to lift that
requirement.

That was the same shape MIG-0007 resolved for the ledger: a Git-side proof plus
a redundant current-tree presence requirement that proves nothing about the
past and only forbids a later reviewed retirement. Spec 0065 VAL-TRR-003
released it for exactly the case a sealed row covers, leaving the row census,
the Stage 99 action-target map, and `validate_mig0004_historical_targets`
untouched. This record seals on that release.

The two registry profiles the form supported retire with it.
`governance/progress-entry` matched the form and carried the sole
`appendContract`; `governance/progress-ledger` matched the ledger MIG-0007
retired and named that profile as its parent. Neither routes a path.

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

Recover the retired bytes with `git show
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
