---
title: "Document Taxonomy Package Retention"
version: "1.0.0"
type: "archive/migration"
status: "sealed"
owner: "platform"
updated: "2026-09-06"
layer: "archive"
artifact_id: "MIG-0022"
---

# MIG-0022: Document Taxonomy Package Retention

## Overview

This finite ledger retains the completed Spec 0052 package: its Spec, Plan,
and seventeen Tasks. Every source document is `done` at commit
`4053793a41a9cedff1edeaa4a9d3b2a6a80e1272`. The package's completed work and
transfers to Spec 0054 remain historical evidence in the retained documents.

[ADR-0032](../../02.architecture/decisions/0032-completed-and-terminal-document-retention.md)
authorizes whole-package retention at the mirrored `completed/` paths. The
retained documents keep their profiles, identities, terminal states, and
content with rendered relative link prefixes re-based to preserve target
identity. They carry no ArchiveEnvelope. Each row uses `replaced`, because
link rebasing changes bytes while Git preserves the exact source.

## Migration Ledger

<!-- archive-migration-ledger:v1 format=json -->

```json
[
  {
    "legacy_path": "docs/03.specs/0052-document-taxonomy-consolidation/plan.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0052-document-taxonomy-consolidation/plan.md",
    "source_commit": "4053793a41a9cedff1edeaa4a9d3b2a6a80e1272",
    "source_blob": "9c2d44cf9a4eedebb7324475618d9ea57540d052",
    "content_sha256": "cd382b41b612fc735f40887c8caf47714408300f7fe1fb842826dc93018e6f71",
    "reason": "The completed package leaves Stage 03 and is retained whole with its relative link prefixes re-based while preserving the original document and link-target identities."
  },
  {
    "legacy_path": "docs/03.specs/0052-document-taxonomy-consolidation/spec.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0052-document-taxonomy-consolidation/spec.md",
    "source_commit": "4053793a41a9cedff1edeaa4a9d3b2a6a80e1272",
    "source_blob": "cc894677bdefc9de6ecd73ad9c0c0d4cdb75099f",
    "content_sha256": "99cb764cb28977234ffccd855208e7936b2d4b4f2ddd7dec6b7afa498f476d4d",
    "reason": "The completed package leaves Stage 03 and is retained whole with its relative link prefixes re-based while preserving the original document and link-target identities."
  },
  {
    "legacy_path": "docs/03.specs/0052-document-taxonomy-consolidation/tasks/tsk-0001-work-100.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0052-document-taxonomy-consolidation/tasks/tsk-0001-work-100.md",
    "source_commit": "4053793a41a9cedff1edeaa4a9d3b2a6a80e1272",
    "source_blob": "b490cf91dbd93efcf5e893f0f1e6b11d690e4b0f",
    "content_sha256": "8fa19c2b41a6bd57a2cabe9bbde9323b9db985f8c62c01d006b68f9c57ea2c38",
    "reason": "The completed package leaves Stage 03 and is retained whole with its relative link prefixes re-based while preserving the original document and link-target identities."
  },
  {
    "legacy_path": "docs/03.specs/0052-document-taxonomy-consolidation/tasks/tsk-0002-work-101.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0052-document-taxonomy-consolidation/tasks/tsk-0002-work-101.md",
    "source_commit": "4053793a41a9cedff1edeaa4a9d3b2a6a80e1272",
    "source_blob": "a3f6edd9a6822104c60405098f254e52b02aa898",
    "content_sha256": "6c4ccd1ef9df1d63fb9bd70a2e759a9db2105920b4255e660fe57750cdda11f2",
    "reason": "The completed package leaves Stage 03 and is retained whole with its relative link prefixes re-based while preserving the original document and link-target identities."
  },
  {
    "legacy_path": "docs/03.specs/0052-document-taxonomy-consolidation/tasks/tsk-0003-work-102.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0052-document-taxonomy-consolidation/tasks/tsk-0003-work-102.md",
    "source_commit": "4053793a41a9cedff1edeaa4a9d3b2a6a80e1272",
    "source_blob": "c93d326a59594f51c4f3d999789371cbbef83552",
    "content_sha256": "2899b74267c1adb73afc755239667f4915e9830d8648c14a81ec9e9f81f9191e",
    "reason": "The completed package leaves Stage 03 and is retained whole with its relative link prefixes re-based while preserving the original document and link-target identities."
  },
  {
    "legacy_path": "docs/03.specs/0052-document-taxonomy-consolidation/tasks/tsk-0004-work-103.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0052-document-taxonomy-consolidation/tasks/tsk-0004-work-103.md",
    "source_commit": "4053793a41a9cedff1edeaa4a9d3b2a6a80e1272",
    "source_blob": "ebf04d487a110dc237913696920e021902f7fb76",
    "content_sha256": "35b74f8a83376ebf2d26d71693675d878826b9dbc258769379d1e33aab06118c",
    "reason": "The completed package leaves Stage 03 and is retained whole with its relative link prefixes re-based while preserving the original document and link-target identities."
  },
  {
    "legacy_path": "docs/03.specs/0052-document-taxonomy-consolidation/tasks/tsk-0005-wdtc-amend-001.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0052-document-taxonomy-consolidation/tasks/tsk-0005-wdtc-amend-001.md",
    "source_commit": "4053793a41a9cedff1edeaa4a9d3b2a6a80e1272",
    "source_blob": "5766e935b31fda8a519fc677b96d135ef2e8861e",
    "content_sha256": "e77c25b469f90c907d0b47e1d89aaff402e1e03c3e55224901ed03a993fbce6d",
    "reason": "The completed package leaves Stage 03 and is retained whole with its relative link prefixes re-based while preserving the original document and link-target identities."
  },
  {
    "legacy_path": "docs/03.specs/0052-document-taxonomy-consolidation/tasks/tsk-0006-work-104.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0052-document-taxonomy-consolidation/tasks/tsk-0006-work-104.md",
    "source_commit": "4053793a41a9cedff1edeaa4a9d3b2a6a80e1272",
    "source_blob": "187645af36f3049e1cef69fdfd92fd91be6f09ff",
    "content_sha256": "fabd1f9f4d2f3625590f1608b59db213694114450262113d2829bc1e3f7ddd06",
    "reason": "The completed package leaves Stage 03 and is retained whole with its relative link prefixes re-based while preserving the original document and link-target identities."
  },
  {
    "legacy_path": "docs/03.specs/0052-document-taxonomy-consolidation/tasks/tsk-0007-work-105.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0052-document-taxonomy-consolidation/tasks/tsk-0007-work-105.md",
    "source_commit": "4053793a41a9cedff1edeaa4a9d3b2a6a80e1272",
    "source_blob": "87c7f1207e8e11191c72f54208794fb8e0828df2",
    "content_sha256": "24937c8ed409c7c96ed10d6f15e2d1d2a8cc77aab463017a0dad7017a667e58b",
    "reason": "The completed package leaves Stage 03 and is retained whole with its relative link prefixes re-based while preserving the original document and link-target identities."
  },
  {
    "legacy_path": "docs/03.specs/0052-document-taxonomy-consolidation/tasks/tsk-0008-work-106.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0052-document-taxonomy-consolidation/tasks/tsk-0008-work-106.md",
    "source_commit": "4053793a41a9cedff1edeaa4a9d3b2a6a80e1272",
    "source_blob": "951ed8de5679c33736b68d0f6750211affa2e367",
    "content_sha256": "239e038018360669f6f18eae89bee7969764d8d7b9aa9b63da74e6c67cdae92e",
    "reason": "The completed package leaves Stage 03 and is retained whole with its relative link prefixes re-based while preserving the original document and link-target identities."
  },
  {
    "legacy_path": "docs/03.specs/0052-document-taxonomy-consolidation/tasks/tsk-0009-work-107.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0052-document-taxonomy-consolidation/tasks/tsk-0009-work-107.md",
    "source_commit": "4053793a41a9cedff1edeaa4a9d3b2a6a80e1272",
    "source_blob": "69cc80265daa271846327169d8a0f7defc528cac",
    "content_sha256": "48c0a52c62f69a8e5cc8824140894f079b25d7b2df76a9166f9df465f541bfc9",
    "reason": "The completed package leaves Stage 03 and is retained whole with its relative link prefixes re-based while preserving the original document and link-target identities."
  },
  {
    "legacy_path": "docs/03.specs/0052-document-taxonomy-consolidation/tasks/tsk-0010-work-108.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0052-document-taxonomy-consolidation/tasks/tsk-0010-work-108.md",
    "source_commit": "4053793a41a9cedff1edeaa4a9d3b2a6a80e1272",
    "source_blob": "4bcd676605e45c6a02c0f1dca6ac65c31f1406ce",
    "content_sha256": "18e8b47985332cc1f01b64fef59fd854da0f0291232ccd3614b83eeb45c18bfc",
    "reason": "The completed package leaves Stage 03 and is retained whole with its relative link prefixes re-based while preserving the original document and link-target identities."
  },
  {
    "legacy_path": "docs/03.specs/0052-document-taxonomy-consolidation/tasks/tsk-0011-work-109.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0052-document-taxonomy-consolidation/tasks/tsk-0011-work-109.md",
    "source_commit": "4053793a41a9cedff1edeaa4a9d3b2a6a80e1272",
    "source_blob": "3757233323b6f98a4e07fcdccff46fcc9547aa52",
    "content_sha256": "9e24b258d07683478603ad53fcb179a5cfc55e26add522e27b3bb4ed3c851b74",
    "reason": "The completed package leaves Stage 03 and is retained whole with its relative link prefixes re-based while preserving the original document and link-target identities."
  },
  {
    "legacy_path": "docs/03.specs/0052-document-taxonomy-consolidation/tasks/tsk-0012-work-110.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0052-document-taxonomy-consolidation/tasks/tsk-0012-work-110.md",
    "source_commit": "4053793a41a9cedff1edeaa4a9d3b2a6a80e1272",
    "source_blob": "b5638323f4ed18da9bb8fb85cb1f826c5d46d68a",
    "content_sha256": "04e3bae1f2466d8790b8c24577cf5644331a753f849dedd8e285b1a81f23000c",
    "reason": "The completed package leaves Stage 03 and is retained whole with its relative link prefixes re-based while preserving the original document and link-target identities."
  },
  {
    "legacy_path": "docs/03.specs/0052-document-taxonomy-consolidation/tasks/tsk-0013-work-111.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0052-document-taxonomy-consolidation/tasks/tsk-0013-work-111.md",
    "source_commit": "4053793a41a9cedff1edeaa4a9d3b2a6a80e1272",
    "source_blob": "4fe0bd1ae0f7484a90f400aa7991abd75a3f11da",
    "content_sha256": "f4af84c859b72c70cc83e7f514bef1770b9a2d500bdf2330d753bf7c81e887fa",
    "reason": "The completed package leaves Stage 03 and is retained whole with its relative link prefixes re-based while preserving the original document and link-target identities."
  },
  {
    "legacy_path": "docs/03.specs/0052-document-taxonomy-consolidation/tasks/tsk-0014-work-112.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0052-document-taxonomy-consolidation/tasks/tsk-0014-work-112.md",
    "source_commit": "4053793a41a9cedff1edeaa4a9d3b2a6a80e1272",
    "source_blob": "d091ec55900667ab6b1cb5c89e8249019bc8728c",
    "content_sha256": "75b578a380344063b8b4030e25a057e5235028bbfb67678c064966ee3b2d720a",
    "reason": "The completed package leaves Stage 03 and is retained whole with its relative link prefixes re-based while preserving the original document and link-target identities."
  },
  {
    "legacy_path": "docs/03.specs/0052-document-taxonomy-consolidation/tasks/tsk-0015-work-113.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0052-document-taxonomy-consolidation/tasks/tsk-0015-work-113.md",
    "source_commit": "4053793a41a9cedff1edeaa4a9d3b2a6a80e1272",
    "source_blob": "fcdc609a8bd846393a62613d08dd8247bae3a745",
    "content_sha256": "5a84fb14524c1535d615e5004f64a332f47cf58159695756916646557f18df6e",
    "reason": "The completed package leaves Stage 03 and is retained whole with its relative link prefixes re-based while preserving the original document and link-target identities."
  },
  {
    "legacy_path": "docs/03.specs/0052-document-taxonomy-consolidation/tasks/tsk-0016-work-114.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0052-document-taxonomy-consolidation/tasks/tsk-0016-work-114.md",
    "source_commit": "4053793a41a9cedff1edeaa4a9d3b2a6a80e1272",
    "source_blob": "59aca605b41bf3f64b0e8e4036dc6bf3141c21ad",
    "content_sha256": "379ae0052680bafb1d8b01e0aea4dc66b5cab7fcf105c1c9ffbf8928e6341632",
    "reason": "The completed package leaves Stage 03 and is retained whole with its relative link prefixes re-based while preserving the original document and link-target identities."
  },
  {
    "legacy_path": "docs/03.specs/0052-document-taxonomy-consolidation/tasks/tsk-0017-work-115.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0052-document-taxonomy-consolidation/tasks/tsk-0017-work-115.md",
    "source_commit": "4053793a41a9cedff1edeaa4a9d3b2a6a80e1272",
    "source_blob": "cb78764ca0ebe8b25aaf632fda08d6d4b909c269",
    "content_sha256": "ccd9da5c4c2ba87ab3b77c544da386f62176b5dd936ed5d2cab59a8636c837c4",
    "reason": "The completed package leaves Stage 03 and is retained whole with its relative link prefixes re-based while preserving the original document and link-target identities."
  }
]
```

## Recovery

Local `main` retains source commit
`4053793a41a9cedff1edeaa4a9d3b2a6a80e1272`. For each row, resolve the
`legacy_path` at that commit and verify its regular Git mode `100644`,
`source_blob`, and `content_sha256` before reading or restoring the source.
Each exact Git blob passed the repository's private, fully redacted secret
classifier before the retained copy was written. The `replacement` is the
mirrored retained document, whose rendered links preserve source target
identity after composing this package's path transition.

Verify the declared recovery through the public entrypoint:

```bash
rtk proxy python3 -B scripts/archive_recovery.py --root . \
  --record docs/98.archive/migrations/0022-document-taxonomy-package-retention.md \
  --verify
```

Publication requires the same source removals, retained targets, incoming-link
updates, and this ledger in the exact logical index and working tree. The
existing staged lifecycle gate proves that publication; a working-tree check
alone does not establish index synchronization.

### Historical consumers

All rendered incoming references are repointed to the retained package, and
its Stage 03 index entry is removed in this change. The retained Specs 0053
and 0056 receive link-target corrections only; their original retention rows
and historical content are unchanged. No consumer needs an unchanged-source
exception, and this block admits none.

<!-- archive-historical-consumers:v1 format=json -->

```json
[]
```
