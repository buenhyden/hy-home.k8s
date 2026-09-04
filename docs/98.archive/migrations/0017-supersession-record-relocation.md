---
title: "Supersession Record Relocation"
version: "1.0.0"
type: "archive/migration"
layer: "archive"
status: "sealed"
owner: "platform"
updated: "2026-09-04"
artifact_id: "MIG-0017"
---

# MIG-0017: Supersession Record Relocation

## Overview

This reviewed ledger relocates the seventeen sealed records that
[MIG-0001](./0001-sdlc-taxonomy-convergence.md) placed under
`tombstones/`. Every one of them carries `archive_reason: superseded` and names
a replacement, which is what `superseded/` describes, so the directory named for
documents that end with no successor held only documents a successor replaced.

MIG-0001 derives each record's stable path structurally, and that derivation was
correct when it was sealed: `tombstones/` was then the only record directory.
[ADR-0032](../../02.architecture/decisions/0032-completed-and-terminal-document-retention.md)
gives Stage 98 four directories whose roles come from what a terminal state
means, and under that taxonomy these records belong one directory over. This
ledger does not amend MIG-0001, which remains a true record of where each
document went at the time; it records the later move on top of it.

Every row is `moved` rather than `replaced`. A record's ArchiveEnvelope carries
its origin, commit, and blob but never its own archive path, so relocating one
changes no byte. Each row therefore asserts byte identity, and `content_sha256`
is the digest of the record file itself at the pinned `source_commit` and
`source_blob`.

`artifact_id` is null on every row. A record identity such as `tomb-PRD-0001`
does not match the ledger's artifact pattern, and the identity is unchanged by
the move in any case: the record keeps the envelope it was sealed with.

## Migration Ledger

<!-- archive-migration-ledger:v1 format=json -->

```json
[
  {
    "legacy_path": "docs/98.archive/tombstones/01.requirements/0001-wsl-k3d-argocd-platform.md",
    "stable_path": "docs/98.archive/superseded/01.requirements/0001-wsl-k3d-argocd-platform.md",
    "artifact_id": null,
    "action": "moved",
    "replacement": null,
    "source_commit": "8e072d354c020e3e131ba00c6a5de60db84d8aac",
    "source_blob": "800d0b6a5a45a163e5239d23badcebf0bbfea270",
    "content_sha256": "4e43cbd06e48500c9f3bbead256b45356957219bc971a402d2b2c6a772a5f876",
    "reason": "The record documents a supersession: its envelope carries `archive_reason: superseded` and names a replacement, which is what `superseded/` holds. The sealed bytes are unchanged, so the row is a move."
  },
  {
    "legacy_path": "docs/98.archive/tombstones/01.requirements/0002-wsl2-k3d-argocd-ha-platform.md",
    "stable_path": "docs/98.archive/superseded/01.requirements/0002-wsl2-k3d-argocd-ha-platform.md",
    "artifact_id": null,
    "action": "moved",
    "replacement": null,
    "source_commit": "8e072d354c020e3e131ba00c6a5de60db84d8aac",
    "source_blob": "a583e57c1212e34316da594ff4961f1f58dc4f85",
    "content_sha256": "637e9e67f449a2ea18c62559ca222aa5656d424b01b70904ac8d5ee1ce49ba09",
    "reason": "The record documents a supersession: its envelope carries `archive_reason: superseded` and names a replacement, which is what `superseded/` holds. The sealed bytes are unchanged, so the row is a move."
  },
  {
    "legacy_path": "docs/98.archive/tombstones/01.requirements/0003-platform-expansion-dashboard-mesh.md",
    "stable_path": "docs/98.archive/superseded/01.requirements/0003-platform-expansion-dashboard-mesh.md",
    "artifact_id": null,
    "action": "moved",
    "replacement": null,
    "source_commit": "8e072d354c020e3e131ba00c6a5de60db84d8aac",
    "source_blob": "68499a877ddef06da415bbd4798a896dc1eba869",
    "content_sha256": "73a0dbc69cc91b5a05e3beb09003c6826ad8974ea87fb1bf4b473ccc9f5dc4f6",
    "reason": "The record documents a supersession: its envelope carries `archive_reason: superseded` and names a replacement, which is what `superseded/` holds. The sealed bytes are unchanged, so the row is a move."
  },
  {
    "legacy_path": "docs/98.archive/tombstones/02.architecture/0001-k3d-topology-and-network.md",
    "stable_path": "docs/98.archive/superseded/02.architecture/0001-k3d-topology-and-network.md",
    "artifact_id": null,
    "action": "moved",
    "replacement": null,
    "source_commit": "8e072d354c020e3e131ba00c6a5de60db84d8aac",
    "source_blob": "7ae2acec7f013d445e74619ead3504a7aceb4619",
    "content_sha256": "336a44351a6472674c55f01d23261d262c4452c8e93ca1a082e65db047064743",
    "reason": "The record documents a supersession: its envelope carries `archive_reason: superseded` and names a replacement, which is what `superseded/` holds. The sealed bytes are unchanged, so the row is a move."
  },
  {
    "legacy_path": "docs/98.archive/tombstones/02.architecture/0001-wsl-k3d-argocd-platform.md",
    "stable_path": "docs/98.archive/superseded/02.architecture/0001-wsl-k3d-argocd-platform.md",
    "artifact_id": null,
    "action": "moved",
    "replacement": null,
    "source_commit": "8e072d354c020e3e131ba00c6a5de60db84d8aac",
    "source_blob": "9eee51dde818388ae0c86244c034068e2c8b9496",
    "content_sha256": "b13f253197369d21a019d18d8ac441b3186f29eed08c4f89d627e2ef07037f75",
    "reason": "The record documents a supersession: its envelope carries `archive_reason: superseded` and names a replacement, which is what `superseded/` holds. The sealed bytes are unchanged, so the row is a move."
  },
  {
    "legacy_path": "docs/98.archive/tombstones/02.architecture/0002-wsl2-k3d-argocd-ha-platform.md",
    "stable_path": "docs/98.archive/superseded/02.architecture/0002-wsl2-k3d-argocd-ha-platform.md",
    "artifact_id": null,
    "action": "moved",
    "replacement": null,
    "source_commit": "8e072d354c020e3e131ba00c6a5de60db84d8aac",
    "source_blob": "04a8841ff005b5a59624024d3181833025324356",
    "content_sha256": "d04ec775fd8aa8b9c8604b76ba97017717965dc00d70c7f1568096cb7f75ef30",
    "reason": "The record documents a supersession: its envelope carries `archive_reason: superseded` and names a replacement, which is what `superseded/` holds. The sealed bytes are unchanged, so the row is a move."
  },
  {
    "legacy_path": "docs/98.archive/tombstones/02.architecture/0003-platform-expansion-mesh-dashboard.md",
    "stable_path": "docs/98.archive/superseded/02.architecture/0003-platform-expansion-mesh-dashboard.md",
    "artifact_id": null,
    "action": "moved",
    "replacement": null,
    "source_commit": "8e072d354c020e3e131ba00c6a5de60db84d8aac",
    "source_blob": "40430ab6b9ddcc6003ad5a085e28e8e65b4a8cbf",
    "content_sha256": "66a18fd86e264c6522654382a3e3b2a0b1435c5aece7ed98d7746a297dc18046",
    "reason": "The record documents a supersession: its envelope carries `archive_reason: superseded` and names a replacement, which is what `superseded/` holds. The sealed bytes are unchanged, so the row is a move."
  },
  {
    "legacy_path": "docs/98.archive/tombstones/02.architecture/0004-external-services-endpoints-and-valkey-backend.md",
    "stable_path": "docs/98.archive/superseded/02.architecture/0004-external-services-endpoints-and-valkey-backend.md",
    "artifact_id": null,
    "action": "moved",
    "replacement": null,
    "source_commit": "8e072d354c020e3e131ba00c6a5de60db84d8aac",
    "source_blob": "c6472070ef4476a2b56ae1f3e9322ef1dc993e2b",
    "content_sha256": "b0af3db33014aaccac22afb83b87cf749808ea497335f6fa409e13cf0b6b8ef9",
    "reason": "The record documents a supersession: its envelope carries `archive_reason: superseded` and names a replacement, which is what `superseded/` holds. The sealed bytes are unchanged, so the row is a move."
  },
  {
    "legacy_path": "docs/98.archive/tombstones/02.architecture/0005-wsl2-ha-baseline-and-external-endpoint-contract.md",
    "stable_path": "docs/98.archive/superseded/02.architecture/0005-wsl2-ha-baseline-and-external-endpoint-contract.md",
    "artifact_id": null,
    "action": "moved",
    "replacement": null,
    "source_commit": "8e072d354c020e3e131ba00c6a5de60db84d8aac",
    "source_blob": "a9cd256b212c7458d751cb7da6db8fa8eae886ad",
    "content_sha256": "a8ca737853057933403a27bb7f91e421cd7105711c75cb46bff6a609245040ef",
    "reason": "The record documents a supersession: its envelope carries `archive_reason: superseded` and names a replacement, which is what `superseded/` holds. The sealed bytes are unchanged, so the row is a move."
  },
  {
    "legacy_path": "docs/98.archive/tombstones/02.architecture/0007-kubernetes-dashboard-v3.md",
    "stable_path": "docs/98.archive/superseded/02.architecture/0007-kubernetes-dashboard-v3.md",
    "artifact_id": null,
    "action": "moved",
    "replacement": null,
    "source_commit": "8e072d354c020e3e131ba00c6a5de60db84d8aac",
    "source_blob": "1ab2227f415d2f2314bc1933135ffda10a8febd7",
    "content_sha256": "4ac8522cb93d4db90c21fc6d269540d7a17748ab1446087a43e6023e9698869c",
    "reason": "The record documents a supersession: its envelope carries `archive_reason: superseded` and names a replacement, which is what `superseded/` holds. The sealed bytes are unchanged, so the row is a move."
  },
  {
    "legacy_path": "docs/98.archive/tombstones/02.architecture/0010-headlamp-replaces-dashboard.md",
    "stable_path": "docs/98.archive/superseded/02.architecture/0010-headlamp-replaces-dashboard.md",
    "artifact_id": null,
    "action": "moved",
    "replacement": null,
    "source_commit": "8e072d354c020e3e131ba00c6a5de60db84d8aac",
    "source_blob": "b8a2681d53922ef194374a45d695c7cab8f68eb7",
    "content_sha256": "90a01ba9b580cf65fce2ddfcabeedef39d1ac29311888f2a83173021c4f41012",
    "reason": "The record documents a supersession: its envelope carries `archive_reason: superseded` and names a replacement, which is what `superseded/` holds. The sealed bytes are unchanged, so the row is a move."
  },
  {
    "legacy_path": "docs/98.archive/tombstones/03.specs/0001-wsl-k3d-argocd-platform.md",
    "stable_path": "docs/98.archive/superseded/03.specs/0001-wsl-k3d-argocd-platform.md",
    "artifact_id": null,
    "action": "moved",
    "replacement": null,
    "source_commit": "8e072d354c020e3e131ba00c6a5de60db84d8aac",
    "source_blob": "abf0c34b6e5a20c860a106eca6d0704fb4123f25",
    "content_sha256": "e843f8b98a664f43335af929a50739e173086fac3476cff62f317edac9e36a20",
    "reason": "The record documents a supersession: its envelope carries `archive_reason: superseded` and names a replacement, which is what `superseded/` holds. The sealed bytes are unchanged, so the row is a move."
  },
  {
    "legacy_path": "docs/98.archive/tombstones/03.specs/0002-wsl2-k3d-argocd-ha-platform.md",
    "stable_path": "docs/98.archive/superseded/03.specs/0002-wsl2-k3d-argocd-ha-platform.md",
    "artifact_id": null,
    "action": "moved",
    "replacement": null,
    "source_commit": "8e072d354c020e3e131ba00c6a5de60db84d8aac",
    "source_blob": "a75395e36e17fc3d2aaf6696f4a8e7581465bf55",
    "content_sha256": "07d944aca0f99c4ebd352366e8ed860f67ccfa58a52fefe68122bfe5064733a7",
    "reason": "The record documents a supersession: its envelope carries `archive_reason: superseded` and names a replacement, which is what `superseded/` holds. The sealed bytes are unchanged, so the row is a move."
  },
  {
    "legacy_path": "docs/98.archive/tombstones/03.specs/0003-platform-expansion.md",
    "stable_path": "docs/98.archive/superseded/03.specs/0003-platform-expansion.md",
    "artifact_id": null,
    "action": "moved",
    "replacement": null,
    "source_commit": "8e072d354c020e3e131ba00c6a5de60db84d8aac",
    "source_blob": "5451a77f8fd6a5ad03349e42c09fbcbaef310bd2",
    "content_sha256": "27123a0b202e09562aefcde10827b890997915fca9042ed72dd2ac8ac68d8671",
    "reason": "The record documents a supersession: its envelope carries `archive_reason: superseded` and names a replacement, which is what `superseded/` holds. The sealed bytes are unchanged, so the row is a move."
  },
  {
    "legacy_path": "docs/98.archive/tombstones/03.specs/0007-docs-governance-consistency.md",
    "stable_path": "docs/98.archive/superseded/03.specs/0007-docs-governance-consistency.md",
    "artifact_id": null,
    "action": "moved",
    "replacement": null,
    "source_commit": "8e072d354c020e3e131ba00c6a5de60db84d8aac",
    "source_blob": "d60ace148f754f551ca70ff32f0e525e7cc63d75",
    "content_sha256": "2b19853654b10e4221fb1cac83c921f96f0cb312e635321db597c0784d182e54",
    "reason": "The record documents a supersession: its envelope carries `archive_reason: superseded` and names a replacement, which is what `superseded/` holds. The sealed bytes are unchanged, so the row is a move."
  },
  {
    "legacy_path": "docs/98.archive/tombstones/05.operations/0004-headlamp-auth-oidc-guide.md",
    "stable_path": "docs/98.archive/superseded/05.operations/0004-headlamp-auth-oidc-guide.md",
    "artifact_id": null,
    "action": "moved",
    "replacement": null,
    "source_commit": "8e072d354c020e3e131ba00c6a5de60db84d8aac",
    "source_blob": "b69f2b7e1542178935ecbc7d3d8a62fc17da0ff6",
    "content_sha256": "e1123d3639f58e157c05f1372cb15e736551921b5ccbec279e7af207b3194f0c",
    "reason": "The record documents a supersession: its envelope carries `archive_reason: superseded` and names a replacement, which is what `superseded/` holds. The sealed bytes are unchanged, so the row is a move."
  },
  {
    "legacy_path": "docs/98.archive/tombstones/05.operations/0005-headlamp-keycloak-runbook.md",
    "stable_path": "docs/98.archive/superseded/05.operations/0005-headlamp-keycloak-runbook.md",
    "artifact_id": null,
    "action": "moved",
    "replacement": null,
    "source_commit": "8e072d354c020e3e131ba00c6a5de60db84d8aac",
    "source_blob": "cdc0121fb17a05bb0f7074e61dd0180f153f4add",
    "content_sha256": "a7f0d10c433a281b06b878de2a5897de732541d2fe8c4f9949a81480f5b45302",
    "reason": "The record documents a supersession: its envelope carries `archive_reason: superseded` and names a replacement, which is what `superseded/` holds. The sealed bytes are unchanged, so the row is a move."
  }
]
```

## Recovery

For every row, recover the record bytes with `git show
<source_commit>:<legacy_path>` and verify both `source_blob` and
`content_sha256`. The digest of the file now at `stable_path` equals the same
value, which is what makes each row a move rather than a replacement.

### Historical consumers

Current documents cite the Stage 98 index rather than an individual record, and
the index rows were repointed in the same change, so no consumer needs a pinned
historical declaration here and this block admits no path.

<!-- archive-historical-consumers:v1 format=json -->

```json
[]
```
