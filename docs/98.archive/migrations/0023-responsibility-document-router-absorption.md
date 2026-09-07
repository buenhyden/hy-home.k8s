---
title: "Responsibility Document Router Absorption"
version: "1.0.0"
type: "archive/migration"
status: "draft"
owner: "platform"
updated: "2026-09-07"
layer: "archive"
artifact_id: "MIG-0023"
---

# MIG-0023: Responsibility Document Router Absorption

## Overview

This finite ledger records the seven responsibility documents under
`.agents/roles/` that stopped being separate files when their content was
absorbed into the responsibility router. Every source document is `active` at
commit `2696c77183760969fbdd5440cbf349a595c13784`.

The seven carried no registry entry. Each held a domain boundary statement and
three or four contract bullets that no concrete role body duplicated, plus a
Validation and Refresh paragraph and a Related Documents list identical across
all seven. The router now carries the boundary and the bullets as a section per
domain with a stable anchor; the per-file boilerplate is what the change drops.

Every row uses `replaced` rather than `deleted`. The content did not leave the
repository — it moved into a document that already indexed these seven — so the
successor endpoint is the router, not the Archive index.

This ledger exists because [MIG-0021](0021-common-agent-authority-routing.md)
names each of these paths as the replacement target for a retired Stage 00
document. Without a successor row here, those fourteen composed routes would
terminate at a path the tree no longer has.

## Migration Ledger

<!-- archive-migration-ledger:v1 format=json -->

```json
[
  {
    "legacy_path": ".agents/roles/architecture.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/roles/README.md",
    "source_commit": "2696c77183760969fbdd5440cbf349a595c13784",
    "source_blob": "fd740d0bf83e1e593fdb7d790b4ecaaa39e10e6e",
    "content_sha256": "9eac3fc94c357e295e8029d2aae06c5143a4e2796bb54d6d05af4bf8eef92e07",
    "reason": "The responsibility document is absorbed into the responsibility router as a section with a stable anchor. Its domain boundary and contract bullets are carried; only the per-file boilerplate is dropped."
  },
  {
    "legacy_path": ".agents/roles/documentation.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/roles/README.md",
    "source_commit": "2696c77183760969fbdd5440cbf349a595c13784",
    "source_blob": "0a150a611636fb853d08de70413f1869ec7c6fd2",
    "content_sha256": "c520d50ce05397934182f5493fb42634dcd40e2db90e73ef6270069071aaa137",
    "reason": "The responsibility document is absorbed into the responsibility router as a section with a stable anchor. Its domain boundary and contract bullets are carried; only the per-file boilerplate is dropped."
  },
  {
    "legacy_path": ".agents/roles/infrastructure.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/roles/README.md",
    "source_commit": "2696c77183760969fbdd5440cbf349a595c13784",
    "source_blob": "1fda6912dc24d6e58b6f0a3141e6d85dabb13027",
    "content_sha256": "098952ffb140c4279183db6fff6b7a43a72fbaefb82e61312fe1facc0451b815",
    "reason": "The responsibility document is absorbed into the responsibility router as a section with a stable anchor. Its domain boundary and contract bullets are carried; only the per-file boilerplate is dropped."
  },
  {
    "legacy_path": ".agents/roles/operations.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/roles/README.md",
    "source_commit": "2696c77183760969fbdd5440cbf349a595c13784",
    "source_blob": "b0fb113976ce05e9a8d6eb340db527f3e2e0c87a",
    "content_sha256": "2c3bc68e8f3367e4f580a18f70c68e517dc10527a9cf096ad1485542c40c5b59",
    "reason": "The responsibility document is absorbed into the responsibility router as a section with a stable anchor. Its domain boundary and contract bullets are carried; only the per-file boilerplate is dropped."
  },
  {
    "legacy_path": ".agents/roles/quality.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/roles/README.md",
    "source_commit": "2696c77183760969fbdd5440cbf349a595c13784",
    "source_blob": "9f4d246d6f7b65e8fa08787a5955cdad3132e44b",
    "content_sha256": "49a421de1c5896f5a54bbd836d5ca7f5457d400f439f952aa70bae6dd21e895e",
    "reason": "The responsibility document is absorbed into the responsibility router as a section with a stable anchor. Its domain boundary and contract bullets are carried; only the per-file boilerplate is dropped."
  },
  {
    "legacy_path": ".agents/roles/security.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/roles/README.md",
    "source_commit": "2696c77183760969fbdd5440cbf349a595c13784",
    "source_blob": "7c59b45b62afb4d3d34de0ffa3bc59038253cbad",
    "content_sha256": "3d88695c3c419f00a76fe393d4ecb17a9c6df402f5eb72bd3696c189dfb48830",
    "reason": "The responsibility document is absorbed into the responsibility router as a section with a stable anchor. Its domain boundary and contract bullets are carried; only the per-file boilerplate is dropped."
  },
  {
    "legacy_path": ".agents/roles/supervision.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": ".agents/roles/README.md",
    "source_commit": "2696c77183760969fbdd5440cbf349a595c13784",
    "source_blob": "b7454a3ae2b3a393d7676ded08682fbdba8f89fa",
    "content_sha256": "8895f8ff6be40855fd9b7d4812b637f82b46820cc1dbdee8d5cde52ee93e51b5",
    "reason": "The responsibility document is absorbed into the responsibility router as a section with a stable anchor. Its domain boundary and contract bullets are carried; only the per-file boilerplate is dropped."
  }
]
```

## Recovery

Local `main` retains source commit `2696c77183760969fbdd5440cbf349a595c13784`. For each row, resolve the
`legacy_path` at that commit and verify its regular Git mode `100644`,
`source_blob`, and `content_sha256` before reading or restoring the source. The
`replacement` is the responsibility router; the absorbed content is found at the
section anchor named by the source document's own domain.

Verify the declared recovery through the public entrypoint:

```bash
python3 -B scripts/archive_recovery.py --root . \
  --record docs/98.archive/migrations/0023-responsibility-document-router-absorption.md \
  --verify
```

### Historical consumers

Twelve concrete role bodies read one of these seven for broader responsibility
context; each now reads the router section anchor instead. The Stage 90 scope
application index maps seven governance scopes to these paths; each row now
names the same anchors. No consumer keeps an unchanged-source reference, and no
rendered link resolves to a removed path.

`validate-agent-governance.py` treated every Markdown file under
`.agents/roles/` as a role projection and carried a hard-coded exception list
for the eight that were not. With the seven gone, that list is one name.
