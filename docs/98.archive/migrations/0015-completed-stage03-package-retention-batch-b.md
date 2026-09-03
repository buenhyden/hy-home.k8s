---
title: "Completed Stage 03 Package Retention Batch B"
version: "1.0.0"
type: "archive/migration"
layer: "archive"
status: "sealed"
owner: "platform"
updated: "2026-09-04"
artifact_id: "MIG-0015"
---

# MIG-0015: Completed Stage 03 Package Retention Batch B

## Overview

This reviewed ledger retires 21 completed Stage 03 packages under
ADR-0032, covering 142 documents. The forty-nine packages retired in
this change are split across three ledgers because a migration document is
capped at 128 KiB and one ledger cannot hold every row. MIG-0013 sealed the
first package separately, and a sealed ledger takes no further rows.

A package is eligible only when every document it holds is `done`, so each row
retires terminal work rather than unfinished scope. This ledger covers:

- `0028-readme-workspace-profiles`
- `0029-semantic-document-validation`
- `0030-authored-document-migration`
- `0031-affected-surface-agent-qa`
- `0032-protected-surface-supply-chain-hardening`
- `0033-template-lifecycle-contract-normalization`
- `0034-authority-and-lineage-foundation`
- `0035-document-schema-and-lifecycle-contract`
- `0036-archive-record-and-workspace-boundary`
- `0037-active-corpus-and-execution-retention`
- `0038-reference-information-architecture`
- `0039-github-ci-qa-evidence`
- `0040-contract-cutover-and-program-closure`
- `0041-stage-00-agent-governance-contract`
- `0042-provider-native-runtime-and-model-evidence`
- `0043-agent-harness-loop-lifecycle`
- `0044-agent-roster-evaluation-and-admission`
- `0045-agent-governance-ci-qa-cutover`
- `0046-agent-governance-program-closure`
- `0053-workspace-engineering-research-pack-consolidation`
- `0055-workspace-governance-audit-and-remediation`

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
    "legacy_path": "docs/03.specs/0028-readme-workspace-profiles/plan.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0028-readme-workspace-profiles/plan.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "a9645f3012f40de26ed445be513923ddcba685ae",
    "content_sha256": "0c5f3130444f283f4133db1364de928044bead51df98cb955658aac6469d1138",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0028-readme-workspace-profiles/spec.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0028-readme-workspace-profiles/spec.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "5574ced717c66db8a88e7c157c02bae4915d8731",
    "content_sha256": "b54bae8e231ed3d92612eb1944689550a343a7ade651049417b8b9e015872dd0",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0028-readme-workspace-profiles/tasks/tsk-0001-rwp-001.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0028-readme-workspace-profiles/tasks/tsk-0001-rwp-001.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "af313c1fb418a21b84f6da53ab826797f9d10cf8",
    "content_sha256": "79925168f16fd16f1d2312b88438c44b81b2774f441dac19fa88d3c1628cb393",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0028-readme-workspace-profiles/tasks/tsk-0002-rwp-002.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0028-readme-workspace-profiles/tasks/tsk-0002-rwp-002.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "371839175e29e1865a4693ea08472683e2fa35a5",
    "content_sha256": "0e4735df9a7426e8abaa5fc1ce8ce646297617a2cd1f03ae152757f63302b2af",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0028-readme-workspace-profiles/tasks/tsk-0003-rwp-003.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0028-readme-workspace-profiles/tasks/tsk-0003-rwp-003.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "79fedb6287073cfe0295f7c7bc081c19a9493523",
    "content_sha256": "9dc36ac120302a055f814bb760ae0d40f57ec5cb5c57b1c067997b2e1a3bfef0",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0028-readme-workspace-profiles/tasks/tsk-0004-rwp-004.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0028-readme-workspace-profiles/tasks/tsk-0004-rwp-004.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "4ba010149838983826c07d0016e312db35dbf841",
    "content_sha256": "20f0de18edc42b54612959930766d43fccf85c5bd09e9f6af6aca80299968f4d",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0028-readme-workspace-profiles/tasks/tsk-0005-rwp-005.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0028-readme-workspace-profiles/tasks/tsk-0005-rwp-005.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "478173d18ebc8c321af2f205dbbbd7a00871f7e3",
    "content_sha256": "af529f25fd2055794ea0ae223f7f8732cf3ebf3fa154ac7ed9841951ac1c0d12",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0028-readme-workspace-profiles/tasks/tsk-0006-rwp-006.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0028-readme-workspace-profiles/tasks/tsk-0006-rwp-006.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "b7db54910021dd290512d7421c795bd71b4acbfd",
    "content_sha256": "783877df020d459ad129313322844d9fda70dc659dc9997ab0424c57fa0ec08a",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0029-semantic-document-validation/plan.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0029-semantic-document-validation/plan.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "460edaff345191d881df8198512b04af6a2831b9",
    "content_sha256": "234f8e0d940708919bcfa6e19d7365fd88f41fadf3eaafb90eddf14b7603a59c",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0029-semantic-document-validation/spec.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0029-semantic-document-validation/spec.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "0702ae78f23308e4efaa23a4ae46c1ed098388be",
    "content_sha256": "d07b4b874049fa1e8c3dfc1f312117be91369a1817964f0a2aa201f59e08e7a8",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0029-semantic-document-validation/tasks/tsk-0001-smdv-001.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0029-semantic-document-validation/tasks/tsk-0001-smdv-001.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "beb45f23adeed0304080d9caed62a69b5f7fdeea",
    "content_sha256": "c3520f4d595df3eb0861568806ed89a55b8c11f8dd46d77acbb0ada907d3302c",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0029-semantic-document-validation/tasks/tsk-0002-smdv-002.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0029-semantic-document-validation/tasks/tsk-0002-smdv-002.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "20f719b13ffce77a794c9784cc3213f4e94c05cb",
    "content_sha256": "1a6bc0b0b10621af9c279a7c8605cf6d1b96fa258a71d4276787ab950ac2b475",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0029-semantic-document-validation/tasks/tsk-0003-smdv-003.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0029-semantic-document-validation/tasks/tsk-0003-smdv-003.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "6f427021e6d89b286a23b97ecd52181fd09eae1c",
    "content_sha256": "e04cf9c552099d4894a26ed3f5ba0a5965277d36f603d96529b2ad5734ecaa16",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0029-semantic-document-validation/tasks/tsk-0004-smdv-004.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0029-semantic-document-validation/tasks/tsk-0004-smdv-004.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "f403ad0ada6af7f0e7be6fdf9451090e47f3b49b",
    "content_sha256": "98738c9e607de479b3584d97b38c320da451b0289e92db0b00f3c5865628cc8d",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0030-authored-document-migration/plan.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0030-authored-document-migration/plan.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "8c0db3f46fdd9e1320978925d3a94f0aa493cfc2",
    "content_sha256": "c6f49af52189f30ae9fb1e3fcd2301e16cf636266800de52b329390eeb693b39",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0030-authored-document-migration/spec.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0030-authored-document-migration/spec.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "edd7057a401b74a71aec14b26b30ff3eda399b01",
    "content_sha256": "44efa1f119a4d00ba17a30b28baa210292a77155d1fae36e70d7324763d498a8",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0030-authored-document-migration/tasks/tsk-0001-adm-001.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0030-authored-document-migration/tasks/tsk-0001-adm-001.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "4944f5aa001fee4cc3f7f2927419582485862791",
    "content_sha256": "9ac21f26f0d0054e2c903258e1c69cbdcfcdb8708d896849a968f95862ef0a2e",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0030-authored-document-migration/tasks/tsk-0002-adm-002.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0030-authored-document-migration/tasks/tsk-0002-adm-002.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "28384778487c82c98c93de2fc21d8e13d5c09a99",
    "content_sha256": "c7601bb6bc326b2395f265d33e6a1a11b0053f41ac919f922600bfbebce86483",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0030-authored-document-migration/tasks/tsk-0003-adm-003.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0030-authored-document-migration/tasks/tsk-0003-adm-003.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "25ff4d763e4eead0585d41464a230558c54630ef",
    "content_sha256": "71d01806119e85965913ca5fe09d24410ddeb212ceea947075aa0028768ae433",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0030-authored-document-migration/tasks/tsk-0004-adm-004.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0030-authored-document-migration/tasks/tsk-0004-adm-004.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "97897c9952c6428fc49f060f00693d1ebfdf0f77",
    "content_sha256": "15917cc5d5a03dda33298562bbc32c42a21b80cc8cdb51998abb83118d1657e4",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0030-authored-document-migration/tasks/tsk-0005-adm-005.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0030-authored-document-migration/tasks/tsk-0005-adm-005.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "cf05c93751b1aa9246fe4dd7ed605835d1d39ddf",
    "content_sha256": "fa53b803480c425636ae1e09cba323df9dd67689ca24bb9846544ceaa15b7314",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0030-authored-document-migration/tasks/tsk-0006-adm-006.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0030-authored-document-migration/tasks/tsk-0006-adm-006.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "417874d0b65b9ad44e6ccef93e9b58e2e384aa74",
    "content_sha256": "a09d1ddd5471bcc28b79c87ec5bf355996b0b1025e1d4a1e09109107f8246b38",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0030-authored-document-migration/tasks/tsk-0007-adm-006c.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0030-authored-document-migration/tasks/tsk-0007-adm-006c.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "99acc8cfca032f8e607b4ddadb1771c309d6138f",
    "content_sha256": "35a0b2e1f20a0d238243706d7135107a376e7c477d2e15c6e20dc6c2f9e28344",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0030-authored-document-migration/tasks/tsk-0008-adm-007.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0030-authored-document-migration/tasks/tsk-0008-adm-007.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "4bd522eb747b58f4eb105fee75430c73ac5de1e6",
    "content_sha256": "2bb1f6315c7d505bd46455303004d77c236ae279d97261926746cb5e26658470",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0031-affected-surface-agent-qa/spec.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0031-affected-surface-agent-qa/spec.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "c8f952e2bd8172431cd2b199517cc9202c7abbac",
    "content_sha256": "ab2dd514ad4614d19e8ea8d33aed0ce1873af977e7418ebf96446d7b5261f332",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0032-protected-surface-supply-chain-hardening/spec.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0032-protected-surface-supply-chain-hardening/spec.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "1e19b1386b0391fe4b675cdef2bf008fe9f574c6",
    "content_sha256": "b63f862c35bee1865b30ffb20db6539ee475adee6a8e043320342c8edb0863f1",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0033-template-lifecycle-contract-normalization/spec.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0033-template-lifecycle-contract-normalization/spec.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "385d9cc7a7cc91576332b1ecdf15b29b588e8692",
    "content_sha256": "dd72639f51d4e15905886f4d4dfd81fccbde6b511d36a2f19281ff15fc6d211a",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0034-authority-and-lineage-foundation/spec.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0034-authority-and-lineage-foundation/spec.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "171d22e8519599e2d18dd85c3605a866069ed575",
    "content_sha256": "b0b3e2ecd6d05b2b4e3ce5b875fac640ef22aa376fbdafaa0783445b1cc27809",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0035-document-schema-and-lifecycle-contract/spec.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0035-document-schema-and-lifecycle-contract/spec.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "5407f1b5f508363a978756aa22c7f844369e814c",
    "content_sha256": "39b5ec25f0654b54fcce732079aebe8905340daa012a68793cb1fcbfd4f29864",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0036-archive-record-and-workspace-boundary/spec.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0036-archive-record-and-workspace-boundary/spec.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "8352339e123728de94c100f839bcfed39ce5a68d",
    "content_sha256": "89721eb0f15c50746fcec54a4c02da842c510e4626ba6b308f66e2aa4fb96fa9",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0037-active-corpus-and-execution-retention/plan.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0037-active-corpus-and-execution-retention/plan.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "f3174216eff8bb7429c868d6722cc687e7631332",
    "content_sha256": "39fc047fb0bad911dd6919a2bec28179a74fa769da94d5ba1017705ef6e7f918",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0037-active-corpus-and-execution-retention/spec.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0037-active-corpus-and-execution-retention/spec.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "d1db9a2e552aaaa4b1f9e2e8becd109ee853b4bf",
    "content_sha256": "f25fb058de6c58844218ccdaf9ca15f5d0b41dfeb3e025d6496af445553b0b3b",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0037-active-corpus-and-execution-retention/tasks/tsk-0001-acer-001.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0037-active-corpus-and-execution-retention/tasks/tsk-0001-acer-001.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "48bc65c5f26ced24833e85415a5bd6a4e56d14e2",
    "content_sha256": "199afbe42bcb3621d013cad61b659e27d7a112324182e18a97c03da3ad1d05ca",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0037-active-corpus-and-execution-retention/tasks/tsk-0002-acer-002.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0037-active-corpus-and-execution-retention/tasks/tsk-0002-acer-002.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "739520a8b10d87f47a443a0611b86e912ac43ee6",
    "content_sha256": "d2c77be892c908da7d1700cd78b799196b3df2ee26356fa8f3dbeff572dd37e9",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0037-active-corpus-and-execution-retention/tasks/tsk-0003-acer-003.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0037-active-corpus-and-execution-retention/tasks/tsk-0003-acer-003.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "2d6b0d876d15d527972d49c115ebdeda630c08a2",
    "content_sha256": "3813b2829c97edc76ca5fd4d7fbddaa863842951a0557e4be0f87422161f3b7a",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0037-active-corpus-and-execution-retention/tasks/tsk-0004-acer-004.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0037-active-corpus-and-execution-retention/tasks/tsk-0004-acer-004.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "42d1a1fefe3c983be41e27340f4366c82a9ce996",
    "content_sha256": "7705a325b3049b0542f7cb859dd1e3a0b5fb0958516878d1addf3474b9694082",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0037-active-corpus-and-execution-retention/tasks/tsk-0005-acer-005.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0037-active-corpus-and-execution-retention/tasks/tsk-0005-acer-005.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "6c4c4135590e1198b47b602466fa8615f17b4603",
    "content_sha256": "016f18885014e1c1d1e7756792ccc51f44a36daa20812eee04f034f86fd70094",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0037-active-corpus-and-execution-retention/tasks/tsk-0006-acer-006.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0037-active-corpus-and-execution-retention/tasks/tsk-0006-acer-006.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "e176bed6618f65e309be8d2073df1b741b218fff",
    "content_sha256": "a61322883a65ded743428fa3dab21974fad628f2d96634c333120009ba914e81",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0038-reference-information-architecture/plan.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0038-reference-information-architecture/plan.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "41be580453a8f6f071a9a795fe7de90d5ff289dd",
    "content_sha256": "b264e9f96c774e5ec68f170ff4b8d7177b284b32dfd589684647b861b7a56ed2",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0038-reference-information-architecture/spec.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0038-reference-information-architecture/spec.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "42e40cd0b12e807895000f5de9b20d20fe150376",
    "content_sha256": "cc1b298fe5e5975172c367478cdc5c24cd0cd4dd13cddf1eb479ea166b1a554a",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0038-reference-information-architecture/tasks/tsk-0001-ria-000.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0038-reference-information-architecture/tasks/tsk-0001-ria-000.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "dbedf421a27d43e7f4d3223f23d229ef9af5aa31",
    "content_sha256": "b1fa217d47022870b59e1d1d4b2d176548f8285fc161847ab415e9cb0bef049d",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0038-reference-information-architecture/tasks/tsk-0002-ria-001.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0038-reference-information-architecture/tasks/tsk-0002-ria-001.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "f9be1789dae6bcecdfc8f8b1f35fe7a6f3c6b8a1",
    "content_sha256": "7ca53a8f6ae8d83058fcb62f1280be5b3aa551ca3ba9eb213d6b3df1a375278e",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0038-reference-information-architecture/tasks/tsk-0003-ria-002.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0038-reference-information-architecture/tasks/tsk-0003-ria-002.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "fc7167ccad68643b384f02e4001ba0fa652f04ca",
    "content_sha256": "d37eb0ab115ce3623f68f5518f206d22f1000b7a07757f340c3c801d975250ca",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0038-reference-information-architecture/tasks/tsk-0004-ria-003.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0038-reference-information-architecture/tasks/tsk-0004-ria-003.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "292775311342e9a60b8a7dcea2f6b0a54aaaaf1b",
    "content_sha256": "5b682e91a05fb3c2fc46b941c62b01c8c773141d333beaf6659707719b69e50b",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0038-reference-information-architecture/tasks/tsk-0005-ria-004.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0038-reference-information-architecture/tasks/tsk-0005-ria-004.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "488d6bb576c396050414fd79e1a7d662359058d7",
    "content_sha256": "7d6c7f26af81f9e162c3b4cfb54ccd38edd0e8c669d05cd52e9fc02fbf893f6c",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0038-reference-information-architecture/tasks/tsk-0006-ria-005.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0038-reference-information-architecture/tasks/tsk-0006-ria-005.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "84ca5ee467ca7f59208316847b77c81700f48154",
    "content_sha256": "010c976ac8e9f349010a45f1dbefeccf488fa35fb1f419cd992c4e36183626c6",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0038-reference-information-architecture/tasks/tsk-0007-ria-006.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0038-reference-information-architecture/tasks/tsk-0007-ria-006.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "edef2d1f67ed029633e982bd0699ba33eaaeaa8d",
    "content_sha256": "7079f43d72c9c623174734d7529435b5c88573347468c6b6cebf3dffe8c11569",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0038-reference-information-architecture/tasks/tsk-0008-ria-007.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0038-reference-information-architecture/tasks/tsk-0008-ria-007.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "b14ff9594e34aed67be5488503e6b2519e5629ce",
    "content_sha256": "004b23df45ba245e8d6b657564ca0a5bb32669d6eee0da3cd9263e5b7b1e1a1c",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0039-github-ci-qa-evidence/plan.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0039-github-ci-qa-evidence/plan.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "6c1d5e23512f787ace0222a316cf6d12be4b53ad",
    "content_sha256": "f74dee28e735a0f6a17a32256c7881dd636bf27a5a9251b823bbd35be60b8aa2",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0039-github-ci-qa-evidence/spec.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0039-github-ci-qa-evidence/spec.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "893c32c5eb4c8f2ad559546d688f834cc7fb2ff0",
    "content_sha256": "25b25c63e1f6a3a46e46e958bcfd9153adc9234d1baabc0fd671110e0a2e74a1",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0039-github-ci-qa-evidence/tasks/tsk-0001-gcqe-000.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0039-github-ci-qa-evidence/tasks/tsk-0001-gcqe-000.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "2df988438706c920b1ceba31f49a613c36e4945c",
    "content_sha256": "8fb18ed4bb3abfab4078d4bd091e4210ac3c917a88e9795611292a44e2168c21",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0039-github-ci-qa-evidence/tasks/tsk-0002-gcqe-001.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0039-github-ci-qa-evidence/tasks/tsk-0002-gcqe-001.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "59c3000f94ddf05160e4f9ce21016f5aecc5cb32",
    "content_sha256": "d1b40b2c369aa72820735734cce0884b911daaa42838ec78852752e59e4e265b",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0039-github-ci-qa-evidence/tasks/tsk-0003-gcqe-002.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0039-github-ci-qa-evidence/tasks/tsk-0003-gcqe-002.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "b0087420c3fd2cc0b80c1b7b3244de8240e377a8",
    "content_sha256": "fa69eaa98807edafbdcd285bcb5581eff218f0084ad58aefe5dc5d5dfe750fd5",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0039-github-ci-qa-evidence/tasks/tsk-0004-gcqe-003.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0039-github-ci-qa-evidence/tasks/tsk-0004-gcqe-003.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "bc41250b7334d66abf775d9255cdc53a28642a79",
    "content_sha256": "3b6f8c205be68a009df2a1d85d2eff8d655a10a9c75ef27487c039bd85fdba8f",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0039-github-ci-qa-evidence/tasks/tsk-0005-gcqe-004.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0039-github-ci-qa-evidence/tasks/tsk-0005-gcqe-004.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "483000715dcba22b7a28257bb7795c676fe92b98",
    "content_sha256": "81fa46abf6ca42a9a3790dc99cc8b524b352e3cad55a576f1c34dda9429c3130",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0039-github-ci-qa-evidence/tasks/tsk-0006-gcqe-005.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0039-github-ci-qa-evidence/tasks/tsk-0006-gcqe-005.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "0979b1f1a0f991fc24488b9b3da69be59802ee42",
    "content_sha256": "c01858c481914ed68cfa8293f3a161a469ff1ed065e92ba9aa16cd348109dc3c",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0039-github-ci-qa-evidence/tasks/tsk-0007-gcqe-006.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0039-github-ci-qa-evidence/tasks/tsk-0007-gcqe-006.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "9afff8e9d5d4c9c9cff06b6d6d58a9f39bbf7ddf",
    "content_sha256": "bbd3e8f30756a38b38583d19f90db1b3c6cb1ab4a33fdb37f56b96ae9c2abd88",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0040-contract-cutover-and-program-closure/plan.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0040-contract-cutover-and-program-closure/plan.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "2dc46e11d7dc296d2714bb3add4b4dd86ddee52f",
    "content_sha256": "fb3d4b5a80c09099f0c12a2cf95c1084c9136a7eb9b0ba32b3bb5e4cd63addf4",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0040-contract-cutover-and-program-closure/spec.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0040-contract-cutover-and-program-closure/spec.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "597a5413b7c34cc5a5881e028f58f41183d9c34b",
    "content_sha256": "d675381720089aad672114a0e6cdd4e04e975192f7fbe9de9442b00842fbbe29",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0040-contract-cutover-and-program-closure/tasks/tsk-0001-ccpc-000.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0040-contract-cutover-and-program-closure/tasks/tsk-0001-ccpc-000.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "a29b2a01c442c926021b7d38838c3ecf74160de1",
    "content_sha256": "5766477387c06aaa5e55ae443d56b2a1182b02f6271dcf494783428aa173e56d",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0040-contract-cutover-and-program-closure/tasks/tsk-0002-ccpc-001.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0040-contract-cutover-and-program-closure/tasks/tsk-0002-ccpc-001.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "965fa4ed7bb90869a168951fa13e3be370dfec25",
    "content_sha256": "d568518fef469651891bb17cd60587ad8830909f75aac206297accd8f3db694a",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0040-contract-cutover-and-program-closure/tasks/tsk-0003-ccpc-002.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0040-contract-cutover-and-program-closure/tasks/tsk-0003-ccpc-002.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "9b17d31b32bc29edea9c0da632ca052799091e2d",
    "content_sha256": "6982fd09130b9e00635312f6debf2ec22bc484c35032ca71246cb8211dc84b3e",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0040-contract-cutover-and-program-closure/tasks/tsk-0004-ccpc-003.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0040-contract-cutover-and-program-closure/tasks/tsk-0004-ccpc-003.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "3248b128897e411bbfcfc3cbf56fe10de0151d78",
    "content_sha256": "0e6851194e5d842fa7ec8de5632bb2765eb0e64485e5c4df19adc817d16d54e0",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0040-contract-cutover-and-program-closure/tasks/tsk-0005-ccpc-004.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0040-contract-cutover-and-program-closure/tasks/tsk-0005-ccpc-004.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "3f89eb284351790ba52f7e04bb1d1991a6c67b61",
    "content_sha256": "b0f993a6403fd95b2e98b979f406196369fd91064c7d2423dc2966e0fc67512e",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0041-stage-00-agent-governance-contract/plan.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0041-stage-00-agent-governance-contract/plan.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "18ebc158d503989183243f69749f14a200c408bd",
    "content_sha256": "7188bd75d8bcfee7c270be25cd8eb955437d3ee5aa02554f45a3d13dca37e499",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0041-stage-00-agent-governance-contract/spec.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0041-stage-00-agent-governance-contract/spec.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "6cfeec14f8e2e7771f4224b671442edb3410cc69",
    "content_sha256": "25334c25204c40839f78e9972380fead2026d04b1d3af78b452cce678317e4ad",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0041-stage-00-agent-governance-contract/tasks/tsk-0001-sagc-000.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0041-stage-00-agent-governance-contract/tasks/tsk-0001-sagc-000.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "6b80d379f15daba3817748152d1fd37d049ae12c",
    "content_sha256": "d8c366199b84e2213b7063b427ab707733d0186a0d6b19cf1ef4e6f5552c9dc8",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0041-stage-00-agent-governance-contract/tasks/tsk-0002-sagc-001.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0041-stage-00-agent-governance-contract/tasks/tsk-0002-sagc-001.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "5bcc1d3ee583b7ba660ad90dc8537fe2b426c319",
    "content_sha256": "ce2e75bcb268a0a896b6bc83704f0612d0e523b908694d854c0280c61e6fc707",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0041-stage-00-agent-governance-contract/tasks/tsk-0003-sagc-002.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0041-stage-00-agent-governance-contract/tasks/tsk-0003-sagc-002.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "1e8dcd8b58e67aa1da4a95c052c475a07c78f908",
    "content_sha256": "de97906fb3519dea51c5a34f86bacb7e83d1311d910192d4c88d655eb330f419",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0041-stage-00-agent-governance-contract/tasks/tsk-0004-sagc-003.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0041-stage-00-agent-governance-contract/tasks/tsk-0004-sagc-003.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "68d2b24f2c0dec6adeebe8b71c0bb6dbe5da35af",
    "content_sha256": "673737a41c2e9ce05de3422e10f7b5c76a739c9af1ffdf3fbe661854efe54129",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0041-stage-00-agent-governance-contract/tasks/tsk-0005-sagc-004.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0041-stage-00-agent-governance-contract/tasks/tsk-0005-sagc-004.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "cf67a76fcf5e07791601c26bcab210448da5e40e",
    "content_sha256": "8c166c2657c58e6e9717cfe4dadec6c13a9da0dfa06a136e2ce0bd78532be6be",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0041-stage-00-agent-governance-contract/tasks/tsk-0006-sagc-005.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0041-stage-00-agent-governance-contract/tasks/tsk-0006-sagc-005.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "66ce9776a4e4126fe7f4eb6d0b732c53bde850c1",
    "content_sha256": "c9d897d82c7a9067b96f1465b49af5261ce86530fcd04571a62d7484a661ebf9",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0042-provider-native-runtime-and-model-evidence/plan.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0042-provider-native-runtime-and-model-evidence/plan.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "bffa13350be801986e124517354ecab5dfb4b927",
    "content_sha256": "6e867bbaa93302ab9492c2e013be9adce59de211375bacf750509b7f5c4b5580",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0042-provider-native-runtime-and-model-evidence/spec.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0042-provider-native-runtime-and-model-evidence/spec.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "d841eaefa45f804dde25cc2cb75a5d3367a10e80",
    "content_sha256": "0789fd060d190dfec479f946e18a601fa1407b4ea25b1ddea12c208668230267",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0042-provider-native-runtime-and-model-evidence/tasks/tsk-0001-pnme-000.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0042-provider-native-runtime-and-model-evidence/tasks/tsk-0001-pnme-000.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "ce5cc34e314eec4e8c8fa12910954e5cc99f01b0",
    "content_sha256": "6c00271b26990464f2052a6e9ed135fa27970f78f8a5a80defdccf77eb7deae5",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0042-provider-native-runtime-and-model-evidence/tasks/tsk-0002-pnme-001.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0042-provider-native-runtime-and-model-evidence/tasks/tsk-0002-pnme-001.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "e28dc8604c299986fb9f43b234a1b787fbd7a1fe",
    "content_sha256": "378f06dc0f2a8e9421b493010c458ef7d69fc6a21434cb6fcf70a6e6b906fba6",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0042-provider-native-runtime-and-model-evidence/tasks/tsk-0003-pnme-002.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0042-provider-native-runtime-and-model-evidence/tasks/tsk-0003-pnme-002.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "9ad71f4f23d4f64ea69c0ec7f185ebfb0bc4f1a4",
    "content_sha256": "0fa42540f160bdee9e5a3f9ce28a6725d4e40dc8d55801d9c19e6c61010452c6",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0042-provider-native-runtime-and-model-evidence/tasks/tsk-0004-pnme-003.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0042-provider-native-runtime-and-model-evidence/tasks/tsk-0004-pnme-003.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "1cbcddb1e2cf2601c231ebb73cd4ab0570f80d29",
    "content_sha256": "6494a2f9e3a8c9b4335edcad4f38223a103ebdbb8dc58013348a5d2e148c9063",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0042-provider-native-runtime-and-model-evidence/tasks/tsk-0005-pnme-004.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0042-provider-native-runtime-and-model-evidence/tasks/tsk-0005-pnme-004.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "fe928da4530e82c4a6eee0937f5063c80da78d6e",
    "content_sha256": "16d9007502fcd640a38df3d729658e99679961d84f71baf2b4af87da70077491",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0042-provider-native-runtime-and-model-evidence/tasks/tsk-0006-pnme-005.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0042-provider-native-runtime-and-model-evidence/tasks/tsk-0006-pnme-005.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "98e0861d15616c9c9a2cbddad91b35dcfe2e198c",
    "content_sha256": "1f56c2bc8bb8b1284d7f531d32860400f58a9a04645f8f128ba1bcd7cfed9b3a",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0043-agent-harness-loop-lifecycle/plan.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0043-agent-harness-loop-lifecycle/plan.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "ceed1bc6b6920466da65d1d0514aa10c1f51f6de",
    "content_sha256": "f10e6a848384ab55b288d2cd9e269639bcc1d63478d7ea4ef307f92402a77055",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0043-agent-harness-loop-lifecycle/spec.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0043-agent-harness-loop-lifecycle/spec.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "2f1f77e211b542afe1e8b156e63229aa96827c62",
    "content_sha256": "386693111f241257ba056fc01f6c58423c10820a43cfa1fc7194cb890959e0e9",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0043-agent-harness-loop-lifecycle/tasks/tsk-0001-ahll-000.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0043-agent-harness-loop-lifecycle/tasks/tsk-0001-ahll-000.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "03e30411532ae47f54a0bd723e041d13d870d93d",
    "content_sha256": "7c297c5ba7243305718e0ccd30b82c3c4c750fc3ed90e6974ab6b8d8e086acfb",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0043-agent-harness-loop-lifecycle/tasks/tsk-0002-ahll-001.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0043-agent-harness-loop-lifecycle/tasks/tsk-0002-ahll-001.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "869b65a363cbb9d4f79bf4f21714034a5773c2da",
    "content_sha256": "f4908712c3788d4e0f2292f6899d4766baa15b9aa53a954fb7efce3d8ea1e395",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0043-agent-harness-loop-lifecycle/tasks/tsk-0003-ahll-002.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0043-agent-harness-loop-lifecycle/tasks/tsk-0003-ahll-002.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "f1c98dc19fc1f15e94473a5f314f7ec3942dd920",
    "content_sha256": "efc4601b0b5c19a993ec2ac412aa345cc6d01a87ade7a6f0d17ae06d2880f423",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0043-agent-harness-loop-lifecycle/tasks/tsk-0004-ahll-003.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0043-agent-harness-loop-lifecycle/tasks/tsk-0004-ahll-003.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "51d7e23777bb0743707bae2564182ca571eae2c5",
    "content_sha256": "46d14fe950b162d3eab18e9ef4f44883f1e64011c91f1bcf9264614a8c3844d7",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0043-agent-harness-loop-lifecycle/tasks/tsk-0005-ahll-004.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0043-agent-harness-loop-lifecycle/tasks/tsk-0005-ahll-004.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "9293756c2c8d5462ad4a513bfc7bc990db4e5069",
    "content_sha256": "05fddae30d97b1ea0645592530206533daf5ca5a52e08f0e79a6aa97a107d9e1",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0044-agent-roster-evaluation-and-admission/plan.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0044-agent-roster-evaluation-and-admission/plan.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "c2ee71136912109d1dd2fda0470e5c53ed768be4",
    "content_sha256": "cd15fd50df2eca4db1837fbbc1edf82bcd8384a39a0cd06e4b36320737987a74",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0044-agent-roster-evaluation-and-admission/spec.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0044-agent-roster-evaluation-and-admission/spec.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "06c27fa583280e23b1ed0ea31660a8314900689e",
    "content_sha256": "5d9ee6575166d033a7158bc9464b1384a319a262bece05c0abea86b127b56f6f",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0044-agent-roster-evaluation-and-admission/tasks/tsk-0001-area-000.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0044-agent-roster-evaluation-and-admission/tasks/tsk-0001-area-000.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "dab83b1e3008dab17cc18296b3cdea14d216ffe5",
    "content_sha256": "f5e4c2d67db29166bd38ad46fd674e066b509c33d3f6a5bf718685630b3c6fda",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0044-agent-roster-evaluation-and-admission/tasks/tsk-0002-area-001.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0044-agent-roster-evaluation-and-admission/tasks/tsk-0002-area-001.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "6888d2658a7a7a0f75210761ddcfa64017a0d766",
    "content_sha256": "9b8cb5ef1a78328b3278a463f53fc4ccec8a6e3cb4eac2eabc81a9122635de53",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0044-agent-roster-evaluation-and-admission/tasks/tsk-0003-area-002.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0044-agent-roster-evaluation-and-admission/tasks/tsk-0003-area-002.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "5f8e929234952103294f8ea6bc377fb8d2485a0a",
    "content_sha256": "c2c3a4d830d23baf11feb440ca940fad2c46982b0ac85da1edea83f16d5e294d",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0044-agent-roster-evaluation-and-admission/tasks/tsk-0004-area-003.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0044-agent-roster-evaluation-and-admission/tasks/tsk-0004-area-003.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "022871c586076c604de3f7b8b685a5003b53568a",
    "content_sha256": "d7b26008dc3b6ef4eb4fe9e46da9e4bdeb8f1cee37df63dce2893ce0e989b6a8",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0044-agent-roster-evaluation-and-admission/tasks/tsk-0005-area-004.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0044-agent-roster-evaluation-and-admission/tasks/tsk-0005-area-004.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "b94d6a589b94a9672acc4af3a40fb4a3c1d0f3c1",
    "content_sha256": "6798e3aef53a2b6d241c8d330d63fed99777550ff00745a90e4d9c3f80c42412",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0044-agent-roster-evaluation-and-admission/tasks/tsk-0006-area-005.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0044-agent-roster-evaluation-and-admission/tasks/tsk-0006-area-005.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "8ddccfbdf6dba2413dc6c4650034a04da06bb0b4",
    "content_sha256": "c237cf4ce37d51e412b58dca58fe22c902344b2ad39670bdd5f9b0a29501f27d",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0045-agent-governance-ci-qa-cutover/plan.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0045-agent-governance-ci-qa-cutover/plan.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "a6da21eba75ec92420ccc3bb0f21d2864da164f7",
    "content_sha256": "4f38656bad0ce37763ee1d52a44f40f9993f9630276065e65c3840bafb83645b",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0045-agent-governance-ci-qa-cutover/spec.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0045-agent-governance-ci-qa-cutover/spec.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "5e5bdc83f32ca50b9cab1ca838bfd7690ffb5bc3",
    "content_sha256": "27a09c2abdd6c1e5d75f4ea87f40703cddca0c64b57422481d6484f3dd20b506",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0045-agent-governance-ci-qa-cutover/tasks/tsk-0001-agqc-000.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0045-agent-governance-ci-qa-cutover/tasks/tsk-0001-agqc-000.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "8499910de3c9e5afc3d779bae62dd71f1544cd34",
    "content_sha256": "87d7dec190a6fecd3c2189d90ad474a81c45fcd8d808aaf94233823e70e63677",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0045-agent-governance-ci-qa-cutover/tasks/tsk-0002-agqc-001.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0045-agent-governance-ci-qa-cutover/tasks/tsk-0002-agqc-001.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "eb4d1610b1c969d82664db74feb528498c5958cd",
    "content_sha256": "90c3a566b8784bf5906f1310e400b21d49f74e21a896ecd0b2ea7b9aa6659919",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0045-agent-governance-ci-qa-cutover/tasks/tsk-0003-agqc-002.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0045-agent-governance-ci-qa-cutover/tasks/tsk-0003-agqc-002.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "6806613d6454236df33e68ee02b15d9db3588d68",
    "content_sha256": "abcb67f0489eb1b845a8265f8fa78b7453cfc70e777b5cd329582a89676b3290",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0045-agent-governance-ci-qa-cutover/tasks/tsk-0004-agqc-003.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0045-agent-governance-ci-qa-cutover/tasks/tsk-0004-agqc-003.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "ca0fa70864ead151240c0937bda9713b1070ab8e",
    "content_sha256": "ffac96b7bff8b2f92d9cdaea51fa7008287d3cd8ce07d2ff07152cc3bf3695bb",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0045-agent-governance-ci-qa-cutover/tasks/tsk-0005-agqc-004.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0045-agent-governance-ci-qa-cutover/tasks/tsk-0005-agqc-004.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "7a7dad7ee49310e9ffb4d99db31799f065013b68",
    "content_sha256": "3bd3e392ba2331b17b436f9f9fb6b9d3e9a8fe25ff81fdfced671e06827b456f",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0045-agent-governance-ci-qa-cutover/tasks/tsk-0006-agqc-005.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0045-agent-governance-ci-qa-cutover/tasks/tsk-0006-agqc-005.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "eb411de7dbca736554adf50e929b3549a8e9d8c5",
    "content_sha256": "bbe2d940d06527ffc9425e1489beb0db8d77ad0a3ba7cc6cc3d6d68d2c7da672",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0045-agent-governance-ci-qa-cutover/tasks/tsk-0007-agqc-006.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0045-agent-governance-ci-qa-cutover/tasks/tsk-0007-agqc-006.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "103f58564145b422b53b1dc26a8677a0561a1ff8",
    "content_sha256": "98bb5ddbbeccefb950273fb2ea689593a49a76f8b426eaa0d88bbc75606f5055",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0046-agent-governance-program-closure/plan.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0046-agent-governance-program-closure/plan.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "14cf6f5695093cc006dddd6210d2e792331f33b9",
    "content_sha256": "77b0c72c4f0797235b8dc6f69b6f0f2b9635da7a9ee19da0d532f634f37895ad",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0046-agent-governance-program-closure/spec.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0046-agent-governance-program-closure/spec.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "a1fcfeb0ded65bbd65785e4b39e33068f180e5f3",
    "content_sha256": "50d0a78262a2236a725d61c0136085d13a071aed5966894225507c8b6d16cf68",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0046-agent-governance-program-closure/tasks/tsk-0001-agpc-000.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0046-agent-governance-program-closure/tasks/tsk-0001-agpc-000.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "2f6dc356a5fab0716b341f6b9dfd87a9b486c3d9",
    "content_sha256": "a56328554f6cac88e50bff8daeae5c74c97ee00452b8151014282108fcba12fb",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0046-agent-governance-program-closure/tasks/tsk-0002-agpc-001.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0046-agent-governance-program-closure/tasks/tsk-0002-agpc-001.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "ba81cbe9d4b8a097319caf82aaae8fb385adc322",
    "content_sha256": "b5d1f28c11b1ff9d0584bfd052f38f3a9bddc87752787ff07935de5f4a23088e",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0046-agent-governance-program-closure/tasks/tsk-0003-agpc-002.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0046-agent-governance-program-closure/tasks/tsk-0003-agpc-002.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "49cb6de9dc3ddeb0533da785f6d94fda17f4590a",
    "content_sha256": "0bd69bd3dd208ba29e2c39b50fe388f3cd8ebf4fcc65d689445dbf392c1f9016",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0046-agent-governance-program-closure/tasks/tsk-0004-agpc-003.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0046-agent-governance-program-closure/tasks/tsk-0004-agpc-003.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "7d2ded8785cd222850723c262662f60df0e7cda3",
    "content_sha256": "b330e450a898cca73dd923cf8bdbfe25048b62610ba9d6f61f465f54f0b44f03",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0046-agent-governance-program-closure/tasks/tsk-0005-agpc-004.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0046-agent-governance-program-closure/tasks/tsk-0005-agpc-004.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "47821d264262b3d9685ef694c5cb81d215e7fc22",
    "content_sha256": "db5a9e8d1174dfba384837b5f8e10e5cfbf2342678a77a7d5cbab59e43605353",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0046-agent-governance-program-closure/tasks/tsk-0006-agpc-005.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0046-agent-governance-program-closure/tasks/tsk-0006-agpc-005.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "f5c498c2eeb2a8675defc39c03dfd58c9b84ca81",
    "content_sha256": "fd35e77140d0254ffbb020f6b28e2d8373ddefa9c0967fd83e77cb692ad3067d",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0053-workspace-engineering-research-pack-consolidation/plan.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0053-workspace-engineering-research-pack-consolidation/plan.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "2f1ae3d55371f379b939622b780905d215cde4c1",
    "content_sha256": "ab5cd67bfc07d035781819b94ea91cd9d040dc0383ec6688276b52edf8d6210b",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0053-workspace-engineering-research-pack-consolidation/spec.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0053-workspace-engineering-research-pack-consolidation/spec.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "f530ae7e1d85bd6d9ce1c12680c05a21b922a416",
    "content_sha256": "7ebe3bbb4d34441763eb275b9c14bd3661fbc52481fea24a89680b4bfa3dba24",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0053-workspace-engineering-research-pack-consolidation/tasks/tsk-0001-werpc-000.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0053-workspace-engineering-research-pack-consolidation/tasks/tsk-0001-werpc-000.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "5fa63ba6b3bc7724edfe87b099dc71fc00ffa704",
    "content_sha256": "624fad7fe8b565974ecdc67ad59b5c340ff4cb7def1f8a63b2c341a4c877b8e3",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0053-workspace-engineering-research-pack-consolidation/tasks/tsk-0002-werpc-000a.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0053-workspace-engineering-research-pack-consolidation/tasks/tsk-0002-werpc-000a.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "41e1a95aef00a018bfd1cd66ae73f0e31b79bdb9",
    "content_sha256": "ebf5a0d2c164f134ee797d3e84ad85be0468d7e775fcdf22f211f1dd723995e1",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0053-workspace-engineering-research-pack-consolidation/tasks/tsk-0003-werpc-001.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0053-workspace-engineering-research-pack-consolidation/tasks/tsk-0003-werpc-001.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "47b23566a0ba45ff3074880c7b3e2a952b9f239d",
    "content_sha256": "685950c346ebcaea03c23375777bde2719444ec369be2d46da44b3c36d7e28d9",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0053-workspace-engineering-research-pack-consolidation/tasks/tsk-0004-werpc-002.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0053-workspace-engineering-research-pack-consolidation/tasks/tsk-0004-werpc-002.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "22fc287faa9afa005bfce0aab1370af4cf3929e2",
    "content_sha256": "36ecd8fa3ac3f0716989ce60398f23c5ed0a2d1baec346bf1a7b6644970bd780",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0053-workspace-engineering-research-pack-consolidation/tasks/tsk-0005-werpc-003.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0053-workspace-engineering-research-pack-consolidation/tasks/tsk-0005-werpc-003.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "7a47a9690bf625a0f50c889943d4eaff508dc0cb",
    "content_sha256": "81a480703c0a3ab2eca5068561f4a2b6a32c06cef05e1f0b15f62ac09df7905c",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0053-workspace-engineering-research-pack-consolidation/tasks/tsk-0006-werpc-004.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0053-workspace-engineering-research-pack-consolidation/tasks/tsk-0006-werpc-004.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "3df984fd7eeb2519dca91134171cde7463010c74",
    "content_sha256": "2bd850af3d050400a76060309dc7281b3b3b51cf312856fe791a338f583ef2ab",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0053-workspace-engineering-research-pack-consolidation/tasks/tsk-0007-werpc-005.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0053-workspace-engineering-research-pack-consolidation/tasks/tsk-0007-werpc-005.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "76e984ea86ce8f5869f69ba4a3718a83621a0cbb",
    "content_sha256": "7c2ac22876dbee72e145734812bf9bb0241f4ada731bc724a7098f429332bc9d",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0053-workspace-engineering-research-pack-consolidation/tasks/tsk-0008-werpc-006.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0053-workspace-engineering-research-pack-consolidation/tasks/tsk-0008-werpc-006.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "19caeeda017ef4fc20c94381db2a230a48a4af12",
    "content_sha256": "9bdfc32b6dd8839359f332a96992659298449b3085cbd0ed890a9d408799f751",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0053-workspace-engineering-research-pack-consolidation/tasks/tsk-0009-werpc-007.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0053-workspace-engineering-research-pack-consolidation/tasks/tsk-0009-werpc-007.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "49c24e67f244e51c95fa4506fd6f266d26d3118b",
    "content_sha256": "8bcd32913fd42c1c0987e4554d02f0c734e68aa9e939773d4b2171a8aa7a9bad",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0053-workspace-engineering-research-pack-consolidation/tasks/tsk-0010-werpc-008.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0053-workspace-engineering-research-pack-consolidation/tasks/tsk-0010-werpc-008.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "34e718920183938beb4b4a691fdd1b8f8118fa9d",
    "content_sha256": "c0242e868d257824af82795532452b5e90d26ec35efe510b1c80c0a1a5b1d111",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0053-workspace-engineering-research-pack-consolidation/tasks/tsk-0011-werpc-009.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0053-workspace-engineering-research-pack-consolidation/tasks/tsk-0011-werpc-009.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "95d21af0360aeb322ac51a76b5cd04b7d63428f7",
    "content_sha256": "ac406165ca68e4345da0af9773a367933cad58420316b8ff1a35bb5058300a86",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0055-workspace-governance-audit-and-remediation/plan.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0055-workspace-governance-audit-and-remediation/plan.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "2151ab37d562d5b988d2267e712b134b7e142725",
    "content_sha256": "e3635a5e15788151ab2e4b4a2b75e60926199c0fba0116e3bbc4834d8a719d21",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0055-workspace-governance-audit-and-remediation/spec.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0055-workspace-governance-audit-and-remediation/spec.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "dc4d489596b90090b7b2953f77eb22d68dbf54ba",
    "content_sha256": "bf7c91db88b00bfbdcc840bb8fc6e5068b4f2bfdf6fd5872f0c7d691636dcf22",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0055-workspace-governance-audit-and-remediation/tasks/tsk-0001-wgia-000.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0055-workspace-governance-audit-and-remediation/tasks/tsk-0001-wgia-000.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "7573818e318c582d49805200dc7bb169f61e2e31",
    "content_sha256": "5e384d48ec22f2fc89775574652800fd3c87bace2caa444e149d86463ec44f36",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0055-workspace-governance-audit-and-remediation/tasks/tsk-0002-wgia-001.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0055-workspace-governance-audit-and-remediation/tasks/tsk-0002-wgia-001.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "3ae0df3eb99232af5a1b5724f566c2fff9d7afc9",
    "content_sha256": "736096eab96b413780cf8fe179cb52c088629b5ee115b59bac5b6e96564cd421",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0055-workspace-governance-audit-and-remediation/tasks/tsk-0003-wgia-002.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0055-workspace-governance-audit-and-remediation/tasks/tsk-0003-wgia-002.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "59cf8ca47926ebb8a2ac12bb98989e9f7256c5f8",
    "content_sha256": "90151cb81475c2375848eb25d182b0a25b8d220fccdda8ba17a5885354ddc382",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0055-workspace-governance-audit-and-remediation/tasks/tsk-0004-wgia-003.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0055-workspace-governance-audit-and-remediation/tasks/tsk-0004-wgia-003.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "a5e72cb4e6e74930094ce6731ae498171fcc1770",
    "content_sha256": "20ba848ef830a3e7e0fddd5ab74527309ec89a7e658505d43c99577cc71e033c",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0055-workspace-governance-audit-and-remediation/tasks/tsk-0005-wgia-004.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0055-workspace-governance-audit-and-remediation/tasks/tsk-0005-wgia-004.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "970f34f47f29d7483203308f491f8a7ada027853",
    "content_sha256": "63994cd34ac4d2ba8846bb08b6d999a0221fe62b4d1f1652a91c14810dceb335",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0055-workspace-governance-audit-and-remediation/tasks/tsk-0006-wgia-005.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0055-workspace-governance-audit-and-remediation/tasks/tsk-0006-wgia-005.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "65784c959c627ed5c6b45ac4b55a078db9dff53f",
    "content_sha256": "4e66f9a6cf20b79abcec09f87fdf3e0a346b579ae728e97190e7c0b43e3a4d65",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0055-workspace-governance-audit-and-remediation/tasks/tsk-0007-wgia-006.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0055-workspace-governance-audit-and-remediation/tasks/tsk-0007-wgia-006.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "21db86efcb05ff5c0d795da9fe58d6b833d44911",
    "content_sha256": "c24ba4ce46b726098487067b94e90c7d64013d9533285601a27eeb90dd8b2526",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0055-workspace-governance-audit-and-remediation/tasks/tsk-0008-wgia-007.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0055-workspace-governance-audit-and-remediation/tasks/tsk-0008-wgia-007.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "649e095865ad7223ef78a940a61f6c3501de3b32",
    "content_sha256": "da0a66d3d74fadf618ece376f61b130d54549da6f4eb1cf47c7f54b454d52524",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0055-workspace-governance-audit-and-remediation/tasks/tsk-0009-wgia-008.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0055-workspace-governance-audit-and-remediation/tasks/tsk-0009-wgia-008.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "b0088715cd9fbb49a4ffbdb54aea729d2cd7f913",
    "content_sha256": "a40be996b3d933663ad8bbded88184fb4e7892697f4b0225b2c3c71167453029",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0055-workspace-governance-audit-and-remediation/tasks/tsk-0010-wgia-009.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0055-workspace-governance-audit-and-remediation/tasks/tsk-0010-wgia-009.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "8d068dcf0bc19feeae5700df6201dc7ebe7e53da",
    "content_sha256": "1583491b88d5b668356ef4d2aa8a33e586efa3724db51e7a8c2b785ea90b3cc2",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0055-workspace-governance-audit-and-remediation/tasks/tsk-0011-wgia-010.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0055-workspace-governance-audit-and-remediation/tasks/tsk-0011-wgia-010.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "3b76fb920cf867c39da43a00eb614a75a1a2d32a",
    "content_sha256": "6613550df8a993ea229ad4264358ea07e31d0d4bde05ebe2f52111b322f6e7f4",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0055-workspace-governance-audit-and-remediation/tasks/tsk-0012-wgia-011.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0055-workspace-governance-audit-and-remediation/tasks/tsk-0012-wgia-011.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "09a2c6e67b505b46a142cd0583865cc32392675d",
    "content_sha256": "ec77733d92988768def91640ba1908e68b0eb2a2dd4870c84072b9d4593f848b",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0055-workspace-governance-audit-and-remediation/tasks/tsk-0013-wgia-012.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0055-workspace-governance-audit-and-remediation/tasks/tsk-0013-wgia-012.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "48f32c2305ab86507ae4514114b8750a3ed4fc81",
    "content_sha256": "5ae6d51b895dce4dc9c314298810505149b0eaf5289e20d93b47eee53b0f8220",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0055-workspace-governance-audit-and-remediation/tasks/tsk-0014-wgia-013.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0055-workspace-governance-audit-and-remediation/tasks/tsk-0014-wgia-013.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "5128ca1808a53d97e35466bdefbf19bf4b08de9b",
    "content_sha256": "263103c25e4891766677ef950e39b609bdb35c38cfc0bbef8014f498c1ee5a2d",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0055-workspace-governance-audit-and-remediation/tasks/tsk-0015-wgia-014.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0055-workspace-governance-audit-and-remediation/tasks/tsk-0015-wgia-014.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "245c38cf0799f3bfee5deb933908d2e9a5b368c5",
    "content_sha256": "3ba3bce0f0428e0299770e446cf7b61233d05a5114e71a467191d50697680cb4",
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
