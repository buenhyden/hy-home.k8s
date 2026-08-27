---
title: "MIG-{NNNN}: {Migration Title}"
type: "content/archive-migration"
status: "accepted"
owner: "platform"
updated: "YYYY-MM-DD"
migration_id: "MIG-0000"
---

# MIG-{NNNN}: {Migration Title}

## Overview

<!-- Author prompt: state the reviewed archive migration boundary and exact record census. -->

## Migration Ledger

<!-- Author prompt: replace the example with the exact reviewed 14-field legacy-to-stable ledger rows. -->

<!-- archive-migration-ledger:v1 format=json -->

```json
[
  {
    "schema_version": 1,
    "migration_id": "MIG-{NNNN}",
    "legacy_path": "docs/98.archive/<legacy-path>.md",
    "stable_path": "docs/98.archive/<stable-path>.md",
    "artifact_id": "<typed-stable-id>",
    "action": "moved",
    "replacement": null,
    "source_commit": "0000000000000000000000000000000000000000",
    "legacy_archive_commit": "1111111111111111111111111111111111111111",
    "legacy_envelope_blob": "2222222222222222222222222222222222222222",
    "source_blob": "3333333333333333333333333333333333333333",
    "content_sha256": "4444444444444444444444444444444444444444444444444444444444444444",
    "record_kind": "change-plan",
    "reason": "Reviewed stable Stage 98 rehome"
  }
]
```

## Recovery

<!-- Author prompt: identify the exact old-envelope and terminal-record recovery checks. -->
