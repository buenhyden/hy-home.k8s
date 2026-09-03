---
title: "Completed Stage 03 Package Retention Batch C"
version: "1.0.0"
type: "archive/migration"
layer: "archive"
status: "sealed"
owner: "platform"
updated: "2026-09-04"
artifact_id: "MIG-0016"
---

# MIG-0016: Completed Stage 03 Package Retention Batch C

## Overview

This reviewed ledger retires 9 completed Stage 03 packages under
ADR-0032, covering 57 documents. The forty-nine packages retired in
this change are split across three ledgers because a migration document is
capped at 128 KiB and one ledger cannot hold every row. MIG-0013 sealed the
first package separately, and a sealed ledger takes no further rows.

A package is eligible only when every document it holds is `done`, so each row
retires terminal work rather than unfinished scope. This ledger covers:

- `0056-workspace-engineering-gap-only-refresh`
- `0057-workspace-engineering-partial-defer-incremental-refresh`
- `0059-workspace-research-full-corpus-refresh`
- `0060-platform-currency-defect-closure`
- `0061-workload-security-context-baseline`
- `0063-governance-invariant-consolidation`
- `0064-agent-governance-surface-consolidation`
- `0065-transition-residue-retirement`
- `0066-validation-tooling-ownership`

Every row is `replaced` rather than `moved`. A retained copy is the same
document with its relative link prefixes re-based to the retention tree, so it
is not byte-identical to its source and cannot be declared as a move. The
retention invariant is target identity: each link in the retained copy resolves
to the document the source link named. The exact source bytes stay recoverable
from Git at the `source_commit` and `source_blob` each row pins.

Citations from outside the retired set were repointed at the retention path in
the same change, so no consumer lost the document it was naming.

## Migration Ledger

<!-- archive-migration-ledger:v1 format=json -->

```json
[
  {
    "legacy_path": "docs/03.specs/0056-workspace-engineering-gap-only-refresh/plan.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0056-workspace-engineering-gap-only-refresh/plan.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "3a41e74c87690b3d42b84f744f4b76348647c2ec",
    "content_sha256": "1b8829ac260147d0fe06880d023173eb1d8bea3fb95aa7df0046548d5d6a35d4",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0056-workspace-engineering-gap-only-refresh/spec.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0056-workspace-engineering-gap-only-refresh/spec.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "271c188a09520e9ca160ca6a33068eb9f07ee4b8",
    "content_sha256": "870476f1ec4e3dafd7080ee1833703783241fcf3182696c6663369448fe054f7",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0056-workspace-engineering-gap-only-refresh/tasks/tsk-0001-werg-000.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0056-workspace-engineering-gap-only-refresh/tasks/tsk-0001-werg-000.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "e06f8abfb2ec0e132a23a3685f5266ded288b651",
    "content_sha256": "32c8d9252dacdd973a95bd2ad22c612790b75b574cb27da78cc89dc4f5193f00",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0056-workspace-engineering-gap-only-refresh/tasks/tsk-0002-werg-001.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0056-workspace-engineering-gap-only-refresh/tasks/tsk-0002-werg-001.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "a4c47a8d869e35dcbbe48e0ac6b38e50b0e02da3",
    "content_sha256": "d04a735551e95d05cd9e0c5ee579168ce4be79586b659248f3372e5dcc6687da",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0056-workspace-engineering-gap-only-refresh/tasks/tsk-0003-werg-002.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0056-workspace-engineering-gap-only-refresh/tasks/tsk-0003-werg-002.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "552584106fc99d7786c1a407afc7dd25ea1835cb",
    "content_sha256": "f27faf4dbb1c0d18d7e4742873f1b70a313ad0d0a5dae5925cb8897a3846ac5c",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0056-workspace-engineering-gap-only-refresh/tasks/tsk-0004-werg-003.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0056-workspace-engineering-gap-only-refresh/tasks/tsk-0004-werg-003.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "a3d6f033ed7c2d280a5d55d187dc2198aadd510c",
    "content_sha256": "4de59652c18c4d06bf51d5a215d211b959c2f8988b15ced4feebe696b6cd644b",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0056-workspace-engineering-gap-only-refresh/tasks/tsk-0005-werg-004.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0056-workspace-engineering-gap-only-refresh/tasks/tsk-0005-werg-004.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "559b5a150f1ad9291b09e586c4d6b78f267b803f",
    "content_sha256": "b6e76c4b0d36da03715511bc0f9c0646ee241f0f3a4213cab94b8bcc115ad4e3",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0056-workspace-engineering-gap-only-refresh/tasks/tsk-0006-werg-005.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0056-workspace-engineering-gap-only-refresh/tasks/tsk-0006-werg-005.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "1a31873c9252ae8571a7d2dbf34551de9635812b",
    "content_sha256": "6f811cc5891bbb6ea665ed4c0ff34c8253dc6f34937c9fc7443b98eae5031836",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0057-workspace-engineering-partial-defer-incremental-refresh/plan.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0057-workspace-engineering-partial-defer-incremental-refresh/plan.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "9deb09a1851b75eafcdae7794c3d12fc982f2ebd",
    "content_sha256": "ac0a492a1a59afe467c7c776cfe5593bd3411e4dc2be2b47a41612c277f9082e",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0057-workspace-engineering-partial-defer-incremental-refresh/spec.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0057-workspace-engineering-partial-defer-incremental-refresh/spec.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "959105f28fef0f7b5b50d08c33af282214f13c3c",
    "content_sha256": "a044f7ab0cd91892fe16e97d1194f073d0311040988c172a19e2c6872569cc0e",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0057-workspace-engineering-partial-defer-incremental-refresh/tasks/tsk-0001-pdrr-000.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0057-workspace-engineering-partial-defer-incremental-refresh/tasks/tsk-0001-pdrr-000.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "722682c3a048e093b8b6353741a7b1355b0f9fab",
    "content_sha256": "d3020fd9d68dc598fbd3de993f34a4a8ddc49fe0a29d27aa18c8c6364e373acf",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0057-workspace-engineering-partial-defer-incremental-refresh/tasks/tsk-0002-pdrr-001.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0057-workspace-engineering-partial-defer-incremental-refresh/tasks/tsk-0002-pdrr-001.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "a20fc7da0dfb9664b9098e5e005767092602e085",
    "content_sha256": "228a3b2f8a599dfab09e89b9ff4e869134567206f37573f0e5bbf131e0afe3e6",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0057-workspace-engineering-partial-defer-incremental-refresh/tasks/tsk-0003-pdrr-002.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0057-workspace-engineering-partial-defer-incremental-refresh/tasks/tsk-0003-pdrr-002.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "93ae9eeb996639428ebfaf55244c753ffd91a575",
    "content_sha256": "40d2a6f7063c2d4d536dbb5abbe89a9f3129f171bdb8ece7f3fac03b48ee3ef7",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0057-workspace-engineering-partial-defer-incremental-refresh/tasks/tsk-0004-pdrr-003.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0057-workspace-engineering-partial-defer-incremental-refresh/tasks/tsk-0004-pdrr-003.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "66d6d7694e151fbdb2141bfec0d47e077cbe2e27",
    "content_sha256": "ea7e711c0d36dec5e390dfe12a237f9d44b15806011594adfcbc00e69c5e366e",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0057-workspace-engineering-partial-defer-incremental-refresh/tasks/tsk-0005-pdrr-004.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0057-workspace-engineering-partial-defer-incremental-refresh/tasks/tsk-0005-pdrr-004.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "eed26ce52839bea9cd64b087141ce5c44af0175f",
    "content_sha256": "1fa27570d7c070f39a4fb1c5420b97d359a222181f0d922a24a9d56694e54080",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0057-workspace-engineering-partial-defer-incremental-refresh/tasks/tsk-0006-pdrr-005.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0057-workspace-engineering-partial-defer-incremental-refresh/tasks/tsk-0006-pdrr-005.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "a4cdb18a0358db05fc7f06e7dadf059b022b2d95",
    "content_sha256": "ea95f6e8cd3d824d8cd83cda1bfd6bd28c8fa054e5a20f38505f7dd01f372d4a",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0057-workspace-engineering-partial-defer-incremental-refresh/tasks/tsk-0007-pdrr-006.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0057-workspace-engineering-partial-defer-incremental-refresh/tasks/tsk-0007-pdrr-006.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "494ef38391faeb66d259440f9120cb45bce61aa0",
    "content_sha256": "757382810d73cb99d032bc06506bca0d1a4c2156c159c4a095fd2cf5c48787ac",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0057-workspace-engineering-partial-defer-incremental-refresh/tasks/tsk-0008-pdrr-007.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0057-workspace-engineering-partial-defer-incremental-refresh/tasks/tsk-0008-pdrr-007.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "89533884a18d612f70b5e715e51cd27a8dbb9dc2",
    "content_sha256": "ffd9954bd48e9fbc5d3cd25d77561d1aa327127243b816cd71981993ea6a9956",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0059-workspace-research-full-corpus-refresh/plan.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0059-workspace-research-full-corpus-refresh/plan.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "a529ee2c1e3d71fadbc6cc71abd6fae59b00d290",
    "content_sha256": "5d3913e3c039197687a4c38dc174f9a0f6351ef9301cc2a46fb2cc2fe2b169f9",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0059-workspace-research-full-corpus-refresh/spec.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0059-workspace-research-full-corpus-refresh/spec.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "d5b14cdaaed65d4e432f1e211fd4114ed971368d",
    "content_sha256": "d85e3c1603b8fc2f995a38f04d53cbd05468b784ff87681696fedd470257c20b",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0059-workspace-research-full-corpus-refresh/tasks/tsk-0001-wrfc-000.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0059-workspace-research-full-corpus-refresh/tasks/tsk-0001-wrfc-000.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "c4a01bb36547a5b210699bc266626fcdf343f430",
    "content_sha256": "fad3e4a670d4cdb8fff271544602002d1b71b1c0bf6cf69934eb64362931a9af",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0059-workspace-research-full-corpus-refresh/tasks/tsk-0002-wrfc-001.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0059-workspace-research-full-corpus-refresh/tasks/tsk-0002-wrfc-001.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "8bc7cccc8e8e8a9e885e7b87c50774cba0b16a05",
    "content_sha256": "62bdcafc02c7284ecc6313934c167424be2b101bf662a57023265d3b0a1ce419",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0059-workspace-research-full-corpus-refresh/tasks/tsk-0003-wrfc-002.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0059-workspace-research-full-corpus-refresh/tasks/tsk-0003-wrfc-002.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "dd712031ba26d2bab7fd82fb7e1ba57d68d38eb1",
    "content_sha256": "eabff9ac42a555756f7733a5e5b25f68e89df293a4370aa6d50c19b6dd29cd0c",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0059-workspace-research-full-corpus-refresh/tasks/tsk-0004-wrfc-003.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0059-workspace-research-full-corpus-refresh/tasks/tsk-0004-wrfc-003.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "0bfe2a2ec9f5b8da27eef70f5702be1823711f5f",
    "content_sha256": "7ef360325d1f7429981e299612c564303ed0ba30bc5610d8b0e0cca736acc74e",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0059-workspace-research-full-corpus-refresh/tasks/tsk-0005-wrfc-004.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0059-workspace-research-full-corpus-refresh/tasks/tsk-0005-wrfc-004.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "df97be1059f8b50e232721b8ba64cb05cc38561b",
    "content_sha256": "9724c65859d051614ec2cf1541e6dacaa0a6b35bbd5be42e15abacfa60c25cfd",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0059-workspace-research-full-corpus-refresh/tasks/tsk-0006-wrfc-005.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0059-workspace-research-full-corpus-refresh/tasks/tsk-0006-wrfc-005.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "1d17fce8624f00b967489f2af2172460c26c4748",
    "content_sha256": "f59c9d4d0f74e0b5ccc28c39735f43b4f1144fbe5cf8b11ec05f2a7954fc40c9",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0059-workspace-research-full-corpus-refresh/tasks/tsk-0007-wrfc-006.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0059-workspace-research-full-corpus-refresh/tasks/tsk-0007-wrfc-006.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "8613671e289fd299d1073c1cd974e45624d9ef03",
    "content_sha256": "127b476a896a76742c184852bc8d5b324c07ac0dc34bcbb0bd9e988df3acc412",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0059-workspace-research-full-corpus-refresh/tasks/tsk-0008-wrfc-007.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0059-workspace-research-full-corpus-refresh/tasks/tsk-0008-wrfc-007.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "5c203631edb846bb298d08592e07b13ac6767c17",
    "content_sha256": "388fdaad585d4004a2eee5a1214218aac0ffbb2cfd3d8bd6c80b748be4f02940",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0059-workspace-research-full-corpus-refresh/tasks/tsk-0009-wrfc-008.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0059-workspace-research-full-corpus-refresh/tasks/tsk-0009-wrfc-008.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "c3faa1d8cd74d493b8b4ad5f025c83e7464ba453",
    "content_sha256": "f7c254e9245ce0839739ff925f1d0758ccc058eb39b37002e741b567ebdffd4e",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0059-workspace-research-full-corpus-refresh/tasks/tsk-0010-wrfc-009.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0059-workspace-research-full-corpus-refresh/tasks/tsk-0010-wrfc-009.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "be2ad987fc9e817d0589e197f42de7175fc9d985",
    "content_sha256": "bbcc81690cf544ff99f9fa659cf7a40ee085e533913d04e62c0c5aeb5f8ca9af",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0059-workspace-research-full-corpus-refresh/tasks/tsk-0011-wrfc-010.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0059-workspace-research-full-corpus-refresh/tasks/tsk-0011-wrfc-010.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "4822359876cd05c58ac8a6c9644eed61b1528276",
    "content_sha256": "bc5a39f78e33803cff928c72c3875a3fd94a4418e99d510cd12c444e97c811a3",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0059-workspace-research-full-corpus-refresh/tasks/tsk-0012-wrfc-011.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0059-workspace-research-full-corpus-refresh/tasks/tsk-0012-wrfc-011.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "ddaaefc909896906645eb80605060364281b69a5",
    "content_sha256": "027b5a6bd470f386947d9ab6fcfd4e304f2b68c8ac0dbabcfee77d21fbe89671",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0059-workspace-research-full-corpus-refresh/tasks/tsk-0013-wrfc-012.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0059-workspace-research-full-corpus-refresh/tasks/tsk-0013-wrfc-012.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "af375cbca1b9d3520a7181f5ef2678ac762d501c",
    "content_sha256": "c7a3fe2d737bcc8f90164a65fee1e6ae86091337d68bab2aebfe406e4a072f40",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0060-platform-currency-defect-closure/plan.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0060-platform-currency-defect-closure/plan.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "717e3d3fad9422dc9133578b416f572b16c8c969",
    "content_sha256": "287096f965a58fe058ccc2f69d9e63d4f090cda2f0b1da86680ed2448e779e34",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0060-platform-currency-defect-closure/spec.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0060-platform-currency-defect-closure/spec.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "40420e9031f71f3ca782a85c811df2882d5568fb",
    "content_sha256": "d29241802ee164840244739802692afbd4a5ec5c84ae7d5278769141b713be6b",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0060-platform-currency-defect-closure/tasks/tsk-0001-pcdc-001.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0060-platform-currency-defect-closure/tasks/tsk-0001-pcdc-001.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "03b08833f36d3feceacd97c04ef974ea12ab31de",
    "content_sha256": "608618ddce405ca6b187d3f330a2f1552135eeeda4fb20d1edf323fd5c72a2e3",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0060-platform-currency-defect-closure/tasks/tsk-0002-pcdc-002.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0060-platform-currency-defect-closure/tasks/tsk-0002-pcdc-002.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "0ebd48608263074acb2b0f85951250591eb6e66a",
    "content_sha256": "4a2dd54b1517b0087d7cf6ad765a95dcf12cedf7d073565091024b04b3a9e39e",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0060-platform-currency-defect-closure/tasks/tsk-0003-pcdc-003.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0060-platform-currency-defect-closure/tasks/tsk-0003-pcdc-003.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "423796afd121ed88cd1eb02cc8c8a2354fc97b11",
    "content_sha256": "a3dada0fcc2cd9f319c71af4a43c8921bd9e191ea9ce323b23a61682344793e9",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0060-platform-currency-defect-closure/tasks/tsk-0004-pcdc-004.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0060-platform-currency-defect-closure/tasks/tsk-0004-pcdc-004.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "a847060d123bcd1045e6ed8f7d80effd226b6495",
    "content_sha256": "cdb39cb3fbe68b6cbcf28a80030f372a977e8d0db86b916168f91007ca47a283",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0061-workload-security-context-baseline/plan.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0061-workload-security-context-baseline/plan.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "199d8df9d3497fec92ee1ef6dd022b20b46f1da1",
    "content_sha256": "facb508893f539b7d63f77538b213674cfc2d9e60ae48f5abc1fe23f2dd5821d",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0061-workload-security-context-baseline/spec.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0061-workload-security-context-baseline/spec.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "7bfd310df86bd4802431921415a2ee3b1e2f9022",
    "content_sha256": "8022c62ab4ff799bddd1cb4c5383dcd5f94a85a91e6363c5699de64bbb738966",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0061-workload-security-context-baseline/tasks/tsk-0001-wscb-001.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0061-workload-security-context-baseline/tasks/tsk-0001-wscb-001.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "306c1a48d37b5469b89f3f530eb980241dc5450d",
    "content_sha256": "e229843f259518b6eee20d93596501d57bd3e5a4cd3b8b4c95c8e27dbaca27d2",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0061-workload-security-context-baseline/tasks/tsk-0002-wscb-002.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0061-workload-security-context-baseline/tasks/tsk-0002-wscb-002.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "76cdb01f9a5be7cacdef2b9afbcce450dc62822a",
    "content_sha256": "9b98b27acccf33a2c016c0d582312e6563fe8e7bea06c9f044360cb8906ffe91",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0061-workload-security-context-baseline/tasks/tsk-0003-wscb-003.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0061-workload-security-context-baseline/tasks/tsk-0003-wscb-003.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "55ed7c9d3f5d5f5e811e68f5ce835499cabcc008",
    "content_sha256": "b2b8295f2868ab402d742a3d4df5a54590194e07fcfcb941433229584425a367",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0061-workload-security-context-baseline/tasks/tsk-0004-wscb-004.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0061-workload-security-context-baseline/tasks/tsk-0004-wscb-004.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "1d1a7a782df5dcb6307f83bdc61d883e6a385d90",
    "content_sha256": "68c5b15221b959b2c1dc309e3c6dab6c7faa1e8583936d5f64d62e0893132ffa",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0063-governance-invariant-consolidation/plan.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0063-governance-invariant-consolidation/plan.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "6a8ca97ed2e9a9ee3f752ebf3c7ea7fb165ce184",
    "content_sha256": "12483a4a3ad5f6b2b5964e8702f053803cbde2dbaca136382a6c8485a796978e",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0063-governance-invariant-consolidation/spec.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0063-governance-invariant-consolidation/spec.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "f7ef8d755867c667db0b79a866d130d7625430eb",
    "content_sha256": "4b5e2a3bfdbd533959a3594cacf10d18f3cab1204e1e0eb3b641a82484165d3b",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0063-governance-invariant-consolidation/tasks/tsk-0001-gic-000.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0063-governance-invariant-consolidation/tasks/tsk-0001-gic-000.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "e27b9bfc60073d66ecc7bcaa1e76837a82822fc9",
    "content_sha256": "dc92f8b4e98eafa7b19c34435f3fc50ac39b0f01b9ab5d0bc67624e5cdced90a",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0064-agent-governance-surface-consolidation/plan.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0064-agent-governance-surface-consolidation/plan.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "8048cad7a1723564b5bceebbb9acdc9d1886875c",
    "content_sha256": "ba2679ad2b22246fafea523b41a440f8bf24be2a794624b17fe5647c1a97630f",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0064-agent-governance-surface-consolidation/spec.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0064-agent-governance-surface-consolidation/spec.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "75ffa5075cd01b3c1bc6b420dae3f966a48bd471",
    "content_sha256": "6b1ac21c4917f465197c1c827bc5f1514e7f66374019a2dbae298bbfd36c8370",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0064-agent-governance-surface-consolidation/tasks/tsk-0001-ags-000.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0064-agent-governance-surface-consolidation/tasks/tsk-0001-ags-000.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "29d485ef26c1dc512b7b6fc117adf4965042cb75",
    "content_sha256": "0927eca5eab26b183f005fc6c456af0a11f6c7f6108f585d6d88204d7995737a",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0065-transition-residue-retirement/plan.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0065-transition-residue-retirement/plan.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "374da6c59f7f0d21adfa50f950ca3879a8096b7d",
    "content_sha256": "35644236ecd482969183dda495bdcfe636586b353f6ea339a1a34bd5dbbed70c",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0065-transition-residue-retirement/spec.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0065-transition-residue-retirement/spec.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "cb5e0952b078621862bfebf3868a07ff737d9034",
    "content_sha256": "aee56ca1422543fb2598bf03f1c159ac7c23ead014c3703795ee107570ce68f6",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0065-transition-residue-retirement/tasks/tsk-0001-trr-000.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0065-transition-residue-retirement/tasks/tsk-0001-trr-000.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "79035a386ca05b688c5b56e36a04ce330cdcafa6",
    "content_sha256": "86d629c41455057759aa66a05c0e9afe75d336b6a470af5e0116996a08543d52",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0066-validation-tooling-ownership/plan.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0066-validation-tooling-ownership/plan.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "d9bcac570030ac76e1ec8c5658ceac3a22c9381a",
    "content_sha256": "153084db20cdc95675b86c551cf9eb972c5d36f328fd3011d9ef59951c8ee895",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0066-validation-tooling-ownership/spec.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0066-validation-tooling-ownership/spec.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "5eaade166efef0c3231e744887ddf9dcb0411807",
    "content_sha256": "36947bc62d9da7961acc6a04e142a7f6e7d893637aa31c2de8621f717ad8edc1",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0066-validation-tooling-ownership/tasks/tsk-0001-vto-000.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0066-validation-tooling-ownership/tasks/tsk-0001-vto-000.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "6ae834af81821fef463c26bdad86cd4fb2781292",
    "content_sha256": "06ddb279b1af9c5c8d258bd26be0efb3b6be9b7914a0852f50ff6442439b520f",
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
