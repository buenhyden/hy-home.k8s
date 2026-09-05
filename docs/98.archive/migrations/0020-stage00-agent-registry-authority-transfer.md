---
title: "Stage 00 Agent Registry Authority Transfer"
version: "1.0.0"
type: "archive/migration"
status: "sealed"
owner: "platform"
updated: "2026-09-05"
layer: "archive"
artifact_id: "MIG-0020"
---

# MIG-0020: Stage 00 Agent Registry Authority Transfer

## Overview

This finite ledger records the already accepted ADR-0034 transfer of the
provider-neutral registry and its schema from the retired `.agents/` root to
the Stage 00 roles owner. The source bytes remain recoverable from the sealed
Git commit; the current successors are semantic replacements, not byte-identical
moves. It neither changes ADR-0034 nor grants the retired root current authority.

## Migration Ledger

<!-- archive-migration-ledger:v1 format=json -->

```json
[
  {
    "legacy_path": ".agents/contracts/agent-registry.schema.json",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/00.agent-governance/roles/registry.schema.json",
    "source_commit": "0540a433100055c1fab8ac47eb619eecdc0d97f9",
    "source_blob": "0208f730029cb1bde484e5853386fa6ae6d035e3",
    "content_sha256": "5e908944ce58df14057c18f1beb02b527132a60336a7fe4f3b80ad8e7c84ac69",
    "reason": "Accepted ADR-0034 transfers the retired shared-root schema authority to the current Stage 00 roles owner."
  },
  {
    "legacy_path": ".agents/registry.json",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/00.agent-governance/roles/registry.json",
    "source_commit": "0540a433100055c1fab8ac47eb619eecdc0d97f9",
    "source_blob": "8eb375637d12eccdfd0a2fe073db102f5e687e71",
    "content_sha256": "412b9a685d935561e5383b45104c3af1fc6fda5528ad5609dfd4a649a96e3b07",
    "reason": "Accepted ADR-0034 transfers the retired shared-root registry authority to the current Stage 00 roles owner."
  }
]
```

## Recovery

The source commit is reachable Git history and each row binds its exact regular
source blob and SHA-256. The retired `.agents/` root has no current authority;
the Stage 00 successors are the only current registry and schema owners. The
proposed index and worktree must agree before this ledger is sealed.

<!-- archive-historical-consumers:v1 format=json -->

```json
[]
```
