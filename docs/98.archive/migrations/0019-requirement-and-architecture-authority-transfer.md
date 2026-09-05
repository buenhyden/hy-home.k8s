---
title: "Requirement and Architecture Authority Transfer"
version: "1.0.0"
type: "archive/migration"
status: "sealed"
owner: "platform"
updated: "2026-09-05"
layer: "archive"
artifact_id: "MIG-0019"
---

# MIG-0019: Requirement and Architecture Authority Transfer

## Overview

This finite mapping records the reviewed semantic transfer from REQ-0005..0008
and AD-0008..0011 into retained current owners. Source-identical records use
ADR-0032's superseded stage mirror; the sources either already are superseded
or take their Registry-declared active-to-superseded edge in this same change.
It does not retain a Stage 03 package, close WP-013, or alter any ADR lifecycle.

The original REQ-0005/0006 to REQ-0008 lineage is preserved in their exact source
payloads. The record envelopes and this ledger name REQ-0003 as the transitive
current semantic successor, not as the requirement those decisions originally
served. REQ-0007 and AD-0010 also transfer shared governance to REQ-0003/AD-0006;
their primary platform successors are REQ-0004/AD-0007. Explicit member and
architecture responsibility mappings live in those retained owners.

## Migration Ledger

<!-- archive-migration-ledger:v1 format=json -->

```json
[
  {
    "legacy_path": "docs/01.requirements/0005-workspace-document-assurance-modernization.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/01.requirements/0003-workspace-agent-governance-platform.md",
    "source_commit": "89dc12df213849e3e591c3f52bde2b1d288f033b",
    "source_blob": "5f47c5104c0195d9237c9353260b272c008a48ed",
    "content_sha256": "f719388aaa5eab9d4cdd4e26402e0a33f1463e6cb889f56537866ffae307ff9f",
    "reason": "Reviewed current semantic authority transfer; the exact original source and decision lineage remain in the paired superseded record."
  },
  {
    "legacy_path": "docs/01.requirements/0006-workspace-document-lifecycle-and-evidence-consolidation.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/01.requirements/0003-workspace-agent-governance-platform.md",
    "source_commit": "89dc12df213849e3e591c3f52bde2b1d288f033b",
    "source_blob": "03dfeaf1e9771348e09071a92ae290234a165f2d",
    "content_sha256": "5a5658b59d93e91ab12bbdd687ec9128a32cf7fcf71630d7371ba114fc7f15e2",
    "reason": "Reviewed current semantic authority transfer; the exact original source and decision lineage remain in the paired superseded record."
  },
  {
    "legacy_path": "docs/01.requirements/0007-repository-delivery-and-platform-assurance.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/01.requirements/0004-current-local-gitops-platform.md",
    "source_commit": "89dc12df213849e3e591c3f52bde2b1d288f033b",
    "source_blob": "eeee654e76e8fdc67dc5425e2f7514ce19f0784f",
    "content_sha256": "0ae1a7c664784230e4dbfb220cc06819df7580a80f7041d72f78ac37238cd185",
    "reason": "Reviewed current semantic authority transfer; the exact original source and decision lineage remain in the paired superseded record."
  },
  {
    "legacy_path": "docs/01.requirements/0008-workspace-document-taxonomy-consolidation.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/01.requirements/0003-workspace-agent-governance-platform.md",
    "source_commit": "89dc12df213849e3e591c3f52bde2b1d288f033b",
    "source_blob": "39873ca978afad84d1cb10129c66b6c1f3424098",
    "content_sha256": "28ae25c1608db13f51c586c3b568d4d3c97356e9fce34125e685463da9ee77f7",
    "reason": "Reviewed current semantic authority transfer; the exact original source and decision lineage remain in the paired superseded record."
  },
  {
    "legacy_path": "docs/02.architecture/descriptions/0008-workspace-document-assurance-operating-model.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/02.architecture/descriptions/0006-workspace-agent-governance-platform.md",
    "source_commit": "89dc12df213849e3e591c3f52bde2b1d288f033b",
    "source_blob": "09b6966e4915afd7c6e90c131ab095707ef6f97b",
    "content_sha256": "2c694a9adfa3192917505ec3fb8b3fdd9944545a1851bf6508c74c0d17049f3a",
    "reason": "Reviewed current semantic authority transfer; the exact original source and decision lineage remain in the paired superseded record."
  },
  {
    "legacy_path": "docs/02.architecture/descriptions/0009-document-lifecycle-evidence-operating-model.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/02.architecture/descriptions/0006-workspace-agent-governance-platform.md",
    "source_commit": "89dc12df213849e3e591c3f52bde2b1d288f033b",
    "source_blob": "02f09b51676305bae082cf8c685b462c85adf6fc",
    "content_sha256": "240aee6adaa9915d03070ebbecfe8c392947243623e335eeb4894401cae757a0",
    "reason": "Reviewed current semantic authority transfer; the exact original source and decision lineage remain in the paired superseded record."
  },
  {
    "legacy_path": "docs/02.architecture/descriptions/0010-repository-delivery-evidence-architecture.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/02.architecture/descriptions/0007-current-local-gitops-platform.md",
    "source_commit": "89dc12df213849e3e591c3f52bde2b1d288f033b",
    "source_blob": "dd1d54ca4112c915753cee313aeec4f92a745cd2",
    "content_sha256": "2ca26c452cbc75bd5f7d1c5bdfee4cfe6f8f1c10d3555e8a7e5d3edea77a6b70",
    "reason": "Reviewed current semantic authority transfer; the exact original source and decision lineage remain in the paired superseded record."
  },
  {
    "legacy_path": "docs/02.architecture/descriptions/0011-document-taxonomy-consolidation-architecture.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/02.architecture/descriptions/0006-workspace-agent-governance-platform.md",
    "source_commit": "89dc12df213849e3e591c3f52bde2b1d288f033b",
    "source_blob": "9c03158b129e5b1f4e885af94d3129f87eb84052",
    "content_sha256": "a73c32d18bec1102b8103adc73e637cda073ef7b262d724a6115e3d8e93821ac",
    "reason": "Reviewed current semantic authority transfer; the exact original source and decision lineage remain in the paired superseded record."
  }
]
```

## Recovery

The source commit remains reachable from the named local branch
`codex/document-contract-v9`. Each row records the source's regular Git blob
identity and SHA-256. The paired record retains those exact source bytes;
the current successor is a semantic replacement, not a byte-identical move.
Verify this ledger with `python3 scripts/archive_recovery.py --root . --record
docs/98.archive/migrations/0019-requirement-and-architecture-authority-transfer.md --verify`.
The proposed index and worktree must agree before sealing and handoff.

All current-tree consumers are updated in the same change. Terminal ADRs and
Spec 0052 cite original records only as explicit history; no current authority
is granted to a record. No unchanged consumer receives a waiver.

<!-- archive-historical-consumers:v1 format=json -->

```json
[]
```
