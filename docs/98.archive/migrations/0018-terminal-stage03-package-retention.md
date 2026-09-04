---
title: "Terminal Stage 03 Package Retention"
version: "1.0.0"
type: "archive/migration"
layer: "archive"
status: "sealed"
owner: "platform"
updated: "2026-09-04"
artifact_id: "MIG-0018"
---

# MIG-0018: Terminal Stage 03 Package Retention

## Overview

This reviewed ledger retains Spec 0058, whose work ended with eight `done`
documents and two `cancelled` tasks. The package is therefore terminal as a
whole while no single rule of the earlier retention batch reached it: those
ledgers admitted `done` only.

[ADR-0032](../../02.architecture/decisions/0032-completed-and-terminal-document-retention.md)
now states that the retention unit is the package. A task abandoned while its
package ran to completion travels with the package it belongs to, because
splitting it out as a record would break the links the plan and tasks make to
each other and would assert an ending the package did not have. A document that
ends alone, with no finished package around it, still gets a record.

Every row is `replaced` rather than `moved`, on the same reasoning as
[MIG-0013](./0013-completed-stage03-package-retention.md): a retained copy is
the same document with its relative link prefixes re-based to the retention
tree, so it is not byte-identical to its source. The retention invariant is
target identity, and the exact source bytes stay recoverable from Git at the
`source_commit` and `source_blob` each row pins.

## Migration Ledger

<!-- archive-migration-ledger:v1 format=json -->

```json
[
  {
    "legacy_path": "docs/03.specs/0058-workspace-research-consistency-and-partial-refresh/plan.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0058-workspace-research-consistency-and-partial-refresh/plan.md",
    "source_commit": "9554d37e696baa155872aadf14ded8a158ea7d5c",
    "source_blob": "5f11953309a75b342b34b317028db53b243447da",
    "content_sha256": "fc1ba98bd3ac2a4e76d6ccf1a19073e08f09df9ed6928a587f49617b03113469",
    "reason": "The package ran to an end, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0058-workspace-research-consistency-and-partial-refresh/spec.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0058-workspace-research-consistency-and-partial-refresh/spec.md",
    "source_commit": "9554d37e696baa155872aadf14ded8a158ea7d5c",
    "source_blob": "d6b095deb2128f94db6099ef9e808898a21b0ee9",
    "content_sha256": "0e21d44751acca7968bdc82803647973218743173d4794293d6ede204c8d6c07",
    "reason": "The package ran to an end, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0058-workspace-research-consistency-and-partial-refresh/tasks/tsk-0001-wrcp-000.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0058-workspace-research-consistency-and-partial-refresh/tasks/tsk-0001-wrcp-000.md",
    "source_commit": "9554d37e696baa155872aadf14ded8a158ea7d5c",
    "source_blob": "e2343b5c4573b11b2fefdfc5fca33facc4d131d4",
    "content_sha256": "8c5db9e91b202573bc957b881650956a4364985fcd7bcbb414d0c1a956b43519",
    "reason": "The package ran to an end, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0058-workspace-research-consistency-and-partial-refresh/tasks/tsk-0002-wrcp-001.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0058-workspace-research-consistency-and-partial-refresh/tasks/tsk-0002-wrcp-001.md",
    "source_commit": "9554d37e696baa155872aadf14ded8a158ea7d5c",
    "source_blob": "c2bb02421c6843545c0c0a1e76ae508e6f763743",
    "content_sha256": "0ed9cb299f5e18817975db84db235ad78a6b97d7e61f45f84b49c3cd913dbdff",
    "reason": "The package ran to an end, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0058-workspace-research-consistency-and-partial-refresh/tasks/tsk-0003-wrcp-002.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0058-workspace-research-consistency-and-partial-refresh/tasks/tsk-0003-wrcp-002.md",
    "source_commit": "9554d37e696baa155872aadf14ded8a158ea7d5c",
    "source_blob": "f8fa007492f91551299f788489f0b915fb8630ee",
    "content_sha256": "bc167576abd92cb720769c43cd94483f229e2e170e8c0d26e0137dcde3391d4b",
    "reason": "The package ran to an end, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0058-workspace-research-consistency-and-partial-refresh/tasks/tsk-0004-wrcp-003.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0058-workspace-research-consistency-and-partial-refresh/tasks/tsk-0004-wrcp-003.md",
    "source_commit": "9554d37e696baa155872aadf14ded8a158ea7d5c",
    "source_blob": "fbcbab582484dc064ed02ad6cee5bf96df812dcc",
    "content_sha256": "0061e828bfb8701556773213100b58145a56e4514a54b3206dabbd0a92c6ace7",
    "reason": "The package ran to an end, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0058-workspace-research-consistency-and-partial-refresh/tasks/tsk-0005-wrcp-004.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0058-workspace-research-consistency-and-partial-refresh/tasks/tsk-0005-wrcp-004.md",
    "source_commit": "9554d37e696baa155872aadf14ded8a158ea7d5c",
    "source_blob": "beac8e246fa5018d9e898af79fe79da6a81e6e20",
    "content_sha256": "448b434107a8f68e0f9b954132663fdae14775b19368e3e5165cefab668f19ab",
    "reason": "The package ran to an end, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0058-workspace-research-consistency-and-partial-refresh/tasks/tsk-0006-wrcp-005.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0058-workspace-research-consistency-and-partial-refresh/tasks/tsk-0006-wrcp-005.md",
    "source_commit": "9554d37e696baa155872aadf14ded8a158ea7d5c",
    "source_blob": "a3eed0003be5ec83354160cac40e77ba81fdde58",
    "content_sha256": "875160eba2dc117805797ae33a570795225e03d064b349f9b0b5c367eac6bfcc",
    "reason": "The package ran to an end, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0058-workspace-research-consistency-and-partial-refresh/tasks/tsk-0007-wrcp-006.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0058-workspace-research-consistency-and-partial-refresh/tasks/tsk-0007-wrcp-006.md",
    "source_commit": "9554d37e696baa155872aadf14ded8a158ea7d5c",
    "source_blob": "55608b2c225e61113d7e0c849b95d765dd1d23f0",
    "content_sha256": "59c7500a320dcd4cc7abd74e3c30ab6a64a5c843f16ade4d2d56823e64d6fc58",
    "reason": "The package ran to an end, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0058-workspace-research-consistency-and-partial-refresh/tasks/tsk-0008-wrcp-007.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0058-workspace-research-consistency-and-partial-refresh/tasks/tsk-0008-wrcp-007.md",
    "source_commit": "9554d37e696baa155872aadf14ded8a158ea7d5c",
    "source_blob": "bd030a5c6bf4ebfac13e211506fe4ed797af9114",
    "content_sha256": "000c99961d6049f3ef743b5dd3784a69c5d616b58c9d33d22f32a6b62d3bd9a3",
    "reason": "The package ran to an end, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  }
]
```

## Recovery

For every row, recover the source bytes with `git show
<source_commit>:<legacy_path>` and verify both `source_blob` and
`content_sha256`. Each row resolves through `replacement` to the retained copy,
which carries the same content with re-based link prefixes.

### Historical consumers

Every citation of the retained package was repointed at its retention path in
the same change, so no consumer needs a pinned historical declaration here and
this block admits no path.

<!-- archive-historical-consumers:v1 format=json -->

```json
[]
```
