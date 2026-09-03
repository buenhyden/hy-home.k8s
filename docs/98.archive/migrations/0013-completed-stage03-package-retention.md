---
title: "Completed Stage 03 Package Retention"
version: "1.0.0"
type: "archive/migration"
layer: "archive"
status: "sealed"
owner: "platform"
updated: "2026-09-04"
artifact_id: "MIG-0013"
---

# MIG-0013: Completed Stage 03 Package Retention

## Overview

This reviewed ledger records the completed Stage 03 packages that leave the
active stage and are retained under `docs/98.archive/completed/`. A package is
eligible only when every document it holds is `done`, so the row retires a
terminal document rather than unfinished work.

Every row is `replaced` rather than `moved`. A retained copy is the same
document with its relative link prefixes re-based to the retention tree, so it
is not byte-identical to the source and cannot be declared as a move. The
retention invariant is target identity, not byte identity: each link in the
retained copy resolves to the document the source link named. The exact source
bytes stay recoverable from Git at the pinned `source_commit` and `source_blob`
this ledger records.

The retention tree mirrors the origin path exactly, so a row may only name
`docs/98.archive/<class>/<the document's own stage path>`. A relocation that
does not mirror its source is not a retention move.

## Migration Ledger

<!-- archive-migration-ledger:v1 format=json -->

```json
[
  {
    "legacy_path": "docs/03.specs/0067-artifact-identity-and-filename-normalization/plan.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0067-artifact-identity-and-filename-normalization/plan.md",
    "source_commit": "56557bcd524af55d0a50a144940402ee61d6e2ae",
    "source_blob": "033de827aa1458633abf216699c494d39d0092b5",
    "content_sha256": "04b5a492167bcd467d279f5f30cc54e78d9170b50b4ac2779b03ca3236a62cf7",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0067-artifact-identity-and-filename-normalization/spec.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0067-artifact-identity-and-filename-normalization/spec.md",
    "source_commit": "56557bcd524af55d0a50a144940402ee61d6e2ae",
    "source_blob": "413d1637ab8d1bd47340ca1371d734a778acee92",
    "content_sha256": "1912919aa7a8eb33a2212ec76a877fe339075355f13b4ba034d3e9c5ce7d0a59",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0067-artifact-identity-and-filename-normalization/tasks/tsk-0001-aif-000.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0067-artifact-identity-and-filename-normalization/tasks/tsk-0001-aif-000.md",
    "source_commit": "56557bcd524af55d0a50a144940402ee61d6e2ae",
    "source_blob": "3b4f7613991a1eacdaa2fdcd966dd16900d81e44",
    "content_sha256": "19f1b1b5c1d1ae275bb3f32469333fe69ebddcc10add38f021fc0d25395629e2",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  }
]
```

## Recovery

For every row, recover the source bytes with `git show
<source_commit>:<legacy_path>` and verify both `source_blob` and
`content_sha256`. Each row resolves through `replacement` to the retained copy,
which carries the same content with re-based link prefixes.

### Historical consumers

Every citation of a retained package was repointed at its retention path in the
same change, so no consumer needs a pinned historical declaration here and this
block admits no path.

<!-- archive-historical-consumers:v1 format=json -->

```json
[]
```
