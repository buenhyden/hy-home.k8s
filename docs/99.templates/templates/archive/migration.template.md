---
title: "{{TITLE}}"
version: "0.1.0"
type: "archive/migration"
status: "draft"
owner: "{{OWNER}}"
updated: "{{YYYY_MM_DD}}"
layer: "archive"
artifact_id: "{{ARTIFACT_ID}}"
---

# {{ARTIFACT_ID}}: {{MIGRATION_TITLE}}

## Overview

<!-- Author prompt: state the reviewed scope and source identity. The registry owns draft-to-sealed lifecycle; seal only the reviewed finite mapping, never a branch-current census. -->

## Migration Ledger

<!-- Author prompt: replace the example with ordered, unique nine-field recovery rows. Use moved only for identical bytes, merged/replaced for changed responsibility, and deleted with null replacement for Archive lookup without a live successor. -->

<!-- archive-migration-ledger:v1 format=json -->

```json
[
  {
    "legacy_path": ".agents/governance/<retired-owner>.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": ".agents/governance/<current-owner>.md",
    "source_commit": "{{GIT_OID}}",
    "source_blob": "3333333333333333333333333333333333333333",
    "content_sha256": "4444444444444444444444444444444444444444444444444444444444444444",
    "reason": "Reviewed authority consolidation"
  }
]
```

## Recovery

<!-- Author prompt: identify the durable named ref retaining source commits and the public archive_recovery.py --record ... --verify command. State source-mode, source/blob/digest, target, and index/worktree proof. Do not copy whole original bodies or treat derived symlinks as regular recovery payloads. -->

<!-- Author prompt: list only approved finite unchanged historical consumers, grouped by immutable source commit. Use an empty array when none. Every admitted consumer must match its complete source bytes and synchronized index; its rendered retired references need validated dispositions. A lifecycle status, directory or matching token is not an exception. -->

<!-- Author prompt: add optional typed historical-reference evidence only when an approved literal path or historical symlink view needs it. Its closed data shape is owned by the Archive migration parser; ordinary consumer records need no such block. -->

<!-- archive-historical-consumers:v1 format=json -->

```json
[]
```
