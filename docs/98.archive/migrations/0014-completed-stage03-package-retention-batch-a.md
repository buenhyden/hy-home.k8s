---
title: "Completed Stage 03 Package Retention Batch A"
version: "1.0.0"
type: "archive/migration"
layer: "archive"
status: "sealed"
owner: "platform"
updated: "2026-09-04"
artifact_id: "MIG-0014"
---

# MIG-0014: Completed Stage 03 Package Retention Batch A

## Overview

This reviewed ledger retires 19 completed Stage 03 packages under
ADR-0032, covering 145 documents. The forty-nine packages retired in
this change are split across three ledgers because a migration document is
capped at 128 KiB and one ledger cannot hold every row. MIG-0013 sealed the
first package separately, and a sealed ledger takes no further rows.

A package is eligible only when every document it holds is `done`, so each row
retires terminal work rather than unfinished scope. This ledger covers:

- `0009-workspace-harness-research-pack`
- `0010-workspace-harness-implementation-audit-pack`
- `0011-template-contract-governance-migration`
- `0012-template-governance-audit-enhancement`
- `0013-workspace-document-governance-hardening`
- `0014-workspace-document-contract-normalization`
- `0015-agent-governance-contract-normalization`
- `0016-active-control-surface-governance-hardening`
- `0017-workspace-engineering-research-pack`
- `0018-workspace-engineering-implementation-audit-pack`
- `0019-template-path-numbering-contract`
- `0020-workspace-contract-governance-normalization`
- `0021-sdlc-lifecycle-contract`
- `0022-control-cloud-doc-normalization`
- `0023-stage03-04-repo-static-gap-closure`
- `0024-observability-and-network-review-agents`
- `0025-governance-owner-and-roster-currentness`
- `0026-document-contract-registry`
- `0027-template-contract-consolidation`

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
    "legacy_path": "docs/03.specs/0009-workspace-harness-research-pack/plan.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0009-workspace-harness-research-pack/plan.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "d0e6a5ddd4c2dea9a0703e6de8a3b5a1fe264799",
    "content_sha256": "071b32d4f64ffc8d4e1f8ba89ac8e0de7f25852fd939045e95be22cce8b2a668",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0009-workspace-harness-research-pack/spec.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0009-workspace-harness-research-pack/spec.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "8855c0344dcc4708a39e1d8d794bd89612b2baed",
    "content_sha256": "f5294e7e27940d5a2fc0543d0d44df2052a2dfbb744d3504c33318014402df77",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0009-workspace-harness-research-pack/tasks/tsk-0001-t-001.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0009-workspace-harness-research-pack/tasks/tsk-0001-t-001.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "186bdc37335191e08a36cc76bf541c0ce708fc06",
    "content_sha256": "8b9078407e94a575fbaa3afaf0a8b200eadb23d2fcd1236b54273c8884e831c8",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0009-workspace-harness-research-pack/tasks/tsk-0002-t-002.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0009-workspace-harness-research-pack/tasks/tsk-0002-t-002.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "c36edf0b811dec24bf1c867799ce3918fd6dd133",
    "content_sha256": "e041b5764848169007f2282ef3620bb1c7f08ca769ce41865df3bb1730320693",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0009-workspace-harness-research-pack/tasks/tsk-0003-t-003.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0009-workspace-harness-research-pack/tasks/tsk-0003-t-003.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "c9e6a5a32511f00ba44f85b0371791daa67267f9",
    "content_sha256": "31d6921169a1587123846c852c1ecb6fad62e4c14bec610fb75dc2f8025a2ec6",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0009-workspace-harness-research-pack/tasks/tsk-0004-t-004.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0009-workspace-harness-research-pack/tasks/tsk-0004-t-004.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "a63b10e8fecd715297cc9d94575ba6fe30cabdb2",
    "content_sha256": "0290c9e366b6d6e3589801518e8e35e6ccadb44bb9ba9b65113b8ecb2a222712",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0009-workspace-harness-research-pack/tasks/tsk-0005-t-005.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0009-workspace-harness-research-pack/tasks/tsk-0005-t-005.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "de75a552db2f4ee0695a192f50f3af3932adee9d",
    "content_sha256": "f0a8337fdd468b6693467b22985c50caaa26ee24d2f71e8c76ab0131278e9ee5",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0009-workspace-harness-research-pack/tasks/tsk-0006-t-006.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0009-workspace-harness-research-pack/tasks/tsk-0006-t-006.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "fe517fe7e7764fd4cef081d0017a5b813677d75d",
    "content_sha256": "f73caabe0b5f298777b910f8dcde87aafff94011e558fd83e2cea1152bbc903b",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0010-workspace-harness-implementation-audit-pack/plan.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0010-workspace-harness-implementation-audit-pack/plan.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "81d08c3101ba4cdbcb9095f532d1704f1b8c6690",
    "content_sha256": "97c2c85ef490107bd895bb0094f22fcdaa9860d6a1989be50d52bfebe623201c",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0010-workspace-harness-implementation-audit-pack/spec.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0010-workspace-harness-implementation-audit-pack/spec.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "7055e0c1a13dfa093cdac2a9e6b66319bee04d2e",
    "content_sha256": "695df963d8a76eec8a53506706e8493ceeab1cf86241c3c22f63e49570f107af",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0010-workspace-harness-implementation-audit-pack/tasks/tsk-0001-t-001.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0010-workspace-harness-implementation-audit-pack/tasks/tsk-0001-t-001.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "3d43eb90a699792793a5e9c1f5db4b6e57cd3a17",
    "content_sha256": "f1dc5a6d8bba55bdc9405d45fab54ba4086c28330ddd8e2bde2f637e287befa1",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0010-workspace-harness-implementation-audit-pack/tasks/tsk-0002-t-002.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0010-workspace-harness-implementation-audit-pack/tasks/tsk-0002-t-002.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "b8dcf807897702c3610f85505dbc3d98ce002611",
    "content_sha256": "7eedca600d1eb8ab04252a72091ad22db98c88d714568e008353d89f924ca67a",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0010-workspace-harness-implementation-audit-pack/tasks/tsk-0003-t-003.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0010-workspace-harness-implementation-audit-pack/tasks/tsk-0003-t-003.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "1a39fe22789342a15db5f2b208047ccc10033cb7",
    "content_sha256": "c426a606bbde175784399fbbe00db19a3419265a1fd3d50df234e370745d8ef5",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0010-workspace-harness-implementation-audit-pack/tasks/tsk-0004-t-004.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0010-workspace-harness-implementation-audit-pack/tasks/tsk-0004-t-004.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "c646f7e618bab80b16002ef0c5329be1e87e38ca",
    "content_sha256": "8a4a9e47110d04cb187cb6cc1e74e53bd4cfe33cacbd411962e961b64e8a9eb3",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0010-workspace-harness-implementation-audit-pack/tasks/tsk-0005-t-005.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0010-workspace-harness-implementation-audit-pack/tasks/tsk-0005-t-005.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "fad6595ca1325a75915340c5ae4e1c09e40184dd",
    "content_sha256": "c25dddb6e72455c6243e64e3e27d4737a92a9654cfa6e9f97bff8113e8e3bfa2",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0010-workspace-harness-implementation-audit-pack/tasks/tsk-0006-t-006.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0010-workspace-harness-implementation-audit-pack/tasks/tsk-0006-t-006.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "9bb780fcb9cf0ebf65b3f128d8877b50714ba4c5",
    "content_sha256": "337bfafa8886d42dba7f576574b4e63e72421faf4046f022571e2c66c505ba4d",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0011-template-contract-governance-migration/plan.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0011-template-contract-governance-migration/plan.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "d8834eb8e4f2d686450a4bd06572944fa9f2a30c",
    "content_sha256": "e7e3549a0c084d3bcf367b6768d206f8746c3e31203371eab634a1fedcc4b15b",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0011-template-contract-governance-migration/spec.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0011-template-contract-governance-migration/spec.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "63a8eff58fe3caae184d6b88f9bcccde87830ccd",
    "content_sha256": "b8a8e8df5925c225d3ccb55dc7a25705501cd7727ba96babf6c84e489382333d",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0011-template-contract-governance-migration/tasks/tsk-0001-t-001.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0011-template-contract-governance-migration/tasks/tsk-0001-t-001.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "15adf38c2a1b1909e6b2c62b085b2fef4d77aa41",
    "content_sha256": "c06904f8de0fdda846db150f842462fecb57c0c2be4ec9a86661e6a206fbe1b1",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0011-template-contract-governance-migration/tasks/tsk-0002-t-002.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0011-template-contract-governance-migration/tasks/tsk-0002-t-002.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "897907dd21efa757dcddd51a8d758fd24d5c696e",
    "content_sha256": "1eac944a05976633b7417cd39c2304c98d5c9f1009e70ed8e5a7cc18c954e00a",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0011-template-contract-governance-migration/tasks/tsk-0003-t-003.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0011-template-contract-governance-migration/tasks/tsk-0003-t-003.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "1a2dd41a003686ae1d27c7f483f3cf293ddd8ad1",
    "content_sha256": "95c29e751b5a58b6215d49737a64e3460eb495c3b41adbab539b3842d4a11c8d",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0011-template-contract-governance-migration/tasks/tsk-0004-t-004.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0011-template-contract-governance-migration/tasks/tsk-0004-t-004.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "ba386bdfc776ea844817aa6471298e81127f2efe",
    "content_sha256": "bcb5b54c7a0c8430e5bd9cdb7c620b3d2edcd0133d6f9ae498c1993897e166b8",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0011-template-contract-governance-migration/tasks/tsk-0005-t-005.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0011-template-contract-governance-migration/tasks/tsk-0005-t-005.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "0783b90506fb7f99ead96967cd11b03b519bb493",
    "content_sha256": "0da5a1b9dfd4f39bea314217994bff8a69f604e2faf16f121f1a2ec56112f513",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0011-template-contract-governance-migration/tasks/tsk-0006-t-006.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0011-template-contract-governance-migration/tasks/tsk-0006-t-006.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "e821ce04f52a70a822e3239d79457365462a6e33",
    "content_sha256": "918aee50835aa345aff4f23e27261634dded4b378e789fd333b733092b519ce5",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0011-template-contract-governance-migration/tasks/tsk-0007-t-007.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0011-template-contract-governance-migration/tasks/tsk-0007-t-007.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "968af9baa8051e74069d9191158e36194c983e07",
    "content_sha256": "2adbf18549bdf9778be9e350e723df502e5afe31aaa33ba71e05aa15862584bb",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0012-template-governance-audit-enhancement/plan.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0012-template-governance-audit-enhancement/plan.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "a7ddb797bdf0be203b101fb1aac5bd477bda6399",
    "content_sha256": "78670aaa626dfdb4f7334d8a4cb30641f12e71f89de7c38c9fcb0a042366eb2b",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0012-template-governance-audit-enhancement/spec.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0012-template-governance-audit-enhancement/spec.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "9168c9f8f81a532a7b6e760ebb8167907140de9b",
    "content_sha256": "0fb697c4a35252c1c99b6449888c9f752385c750bf7dab09e9518ef60e40e9e9",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0012-template-governance-audit-enhancement/tasks/tsk-0001-t-001.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0012-template-governance-audit-enhancement/tasks/tsk-0001-t-001.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "19ca431125a903fbc15a510fb63e1a70298634ae",
    "content_sha256": "987e24edf3f477d38932a47f8dbd9010be4cbf6c8c732abadba5cdc9a8973bdd",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0012-template-governance-audit-enhancement/tasks/tsk-0002-t-002.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0012-template-governance-audit-enhancement/tasks/tsk-0002-t-002.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "2834b09cb3ed10b951e3fa20d015a8332d774e54",
    "content_sha256": "2f3b4f15bec38c0bfc71bfaa3fa25081b9e23d7abb6daf108d4873b7036f482c",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0012-template-governance-audit-enhancement/tasks/tsk-0003-t-003.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0012-template-governance-audit-enhancement/tasks/tsk-0003-t-003.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "e1454dd56a38f95e0021999620144e023905aedc",
    "content_sha256": "62a720630f41867b415e6d204b71477f846aeb2a512b0f2c1505782d7d36cb65",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0012-template-governance-audit-enhancement/tasks/tsk-0004-t-004.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0012-template-governance-audit-enhancement/tasks/tsk-0004-t-004.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "88873f7819938797326fcbe5ef13b2e3991cbaf1",
    "content_sha256": "c9ca3ead6ae122fa69ffd3fb40f4c27837444bbaa913a53617fad04c53358935",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0012-template-governance-audit-enhancement/tasks/tsk-0005-t-005.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0012-template-governance-audit-enhancement/tasks/tsk-0005-t-005.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "e0443906d8b816c2c0accf600f7142d6742eabff",
    "content_sha256": "96f49926be4bbf1603fe3f961797a41ffe271d1a29877bf2ae4b7d46279f0ad5",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0012-template-governance-audit-enhancement/tasks/tsk-0006-t-006.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0012-template-governance-audit-enhancement/tasks/tsk-0006-t-006.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "1d24a223b4295ba95f2b25f16ec773aeda31eebf",
    "content_sha256": "e696fe6d7a8b0a379a1cfe9d7758acd7512bedada0ead5ca68ee441df18747e8",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0013-workspace-document-governance-hardening/plan.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0013-workspace-document-governance-hardening/plan.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "77ae69761fd6178d01548b4772c28cef7a5ce088",
    "content_sha256": "c57713defd1dbc4eee0519a9a5604591093c17be24566242e52e0ac000c525cc",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0013-workspace-document-governance-hardening/spec.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0013-workspace-document-governance-hardening/spec.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "6eb2563aa690902d2271fe3f6d71d68bf99f3850",
    "content_sha256": "09cca8b8fe1dbc0223f4a31b1e1a0c8a3c52da2b8ade369343b0247ec120f9fb",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0013-workspace-document-governance-hardening/tasks/tsk-0001-t-001.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0013-workspace-document-governance-hardening/tasks/tsk-0001-t-001.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "0aa34f6f187bc440a99a0b7ca045cca9961bbcc4",
    "content_sha256": "6780819ac5c344c19ef575f6be63ca604d080a8ea622e5a1798751a5fd7d9e94",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0013-workspace-document-governance-hardening/tasks/tsk-0002-t-002.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0013-workspace-document-governance-hardening/tasks/tsk-0002-t-002.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "fdf725018caf6123fdba88af29d6eed7afdfbd9c",
    "content_sha256": "40929ff2c88ad1f106463e52c6f1eb230025046d1892228396554f202f627ef8",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0013-workspace-document-governance-hardening/tasks/tsk-0003-t-003.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0013-workspace-document-governance-hardening/tasks/tsk-0003-t-003.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "9c7f382671c4f64330584fce48852134b3838e34",
    "content_sha256": "e830e07c3a243dc55c974c957e4d0c3fd6d6ae94683efd3b50392aeafa28d121",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0013-workspace-document-governance-hardening/tasks/tsk-0004-t-004.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0013-workspace-document-governance-hardening/tasks/tsk-0004-t-004.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "f6ad67ba6c11725c8bc74a7013f68a8cdb92072e",
    "content_sha256": "faad85ac398bf58d88736d6fd254e90668704e1d67467f77b962e0fa98c4051b",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0013-workspace-document-governance-hardening/tasks/tsk-0005-t-005.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0013-workspace-document-governance-hardening/tasks/tsk-0005-t-005.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "55e4cbab4b135121d968608870e40391bf4dcd6a",
    "content_sha256": "5eee1af894ff7ad7a287a6fc3c87b955af139961b651a1a14bfdbc7c0c7319d4",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0014-workspace-document-contract-normalization/plan.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0014-workspace-document-contract-normalization/plan.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "d1b5a4ce44c57af25a42589f76fb0eafc63ec33c",
    "content_sha256": "7cfb8165735aa3246cfc137486a27982d5c2a70040d4ede8d5fe522d8d46b31e",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0014-workspace-document-contract-normalization/spec.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0014-workspace-document-contract-normalization/spec.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "8d0003e5e0762bfd8274eb8951316dfc54be5769",
    "content_sha256": "4742e0baf4b4a5b5bbf91a096919ba49fee91d8413a9a6a618006072f50d8399",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0014-workspace-document-contract-normalization/tasks/tsk-0001-t-001.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0014-workspace-document-contract-normalization/tasks/tsk-0001-t-001.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "2039475977766847bed998da540e0bb5ce6a938c",
    "content_sha256": "65a621b843825e9eba049e17436616f42f5b42158f619b4ac96c11cb1ba65a22",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0014-workspace-document-contract-normalization/tasks/tsk-0002-t-002.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0014-workspace-document-contract-normalization/tasks/tsk-0002-t-002.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "f0780396d8a9a371bf5be280fbe6a09584810bd9",
    "content_sha256": "7fad6e83c8b4202e56adb61d3b92016d6aab55e44cb74dc41213739da73fb749",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0014-workspace-document-contract-normalization/tasks/tsk-0003-t-003.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0014-workspace-document-contract-normalization/tasks/tsk-0003-t-003.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "e41fd18f7bf2a9e864d70d453ce8b5c6a5f64398",
    "content_sha256": "8bccf77870280a5faf1956899775af13c3756ce60d6f111ff97159c464ae9f2f",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0014-workspace-document-contract-normalization/tasks/tsk-0004-t-004.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0014-workspace-document-contract-normalization/tasks/tsk-0004-t-004.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "f090aecc5b3067c99ad90dda7451c7bb5c85f139",
    "content_sha256": "b7f079615d7e7c966ac05d4b092cf4b853d248111d0df5788c9e754ea902f27d",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0014-workspace-document-contract-normalization/tasks/tsk-0005-t-005.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0014-workspace-document-contract-normalization/tasks/tsk-0005-t-005.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "084b7e6bda8611055526d3c860bf91e5502835f8",
    "content_sha256": "4ba9d82ac757d9e0496d1dc11c35a6ba493b563e5e1744cd823c093d5104025c",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0014-workspace-document-contract-normalization/tasks/tsk-0006-t-006.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0014-workspace-document-contract-normalization/tasks/tsk-0006-t-006.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "ffc09530f720737af860f9db09ee8cc4c37f93b6",
    "content_sha256": "c2bce6d9fff70893eeee30dc813ad3c06aac50d289b4c99f5a60a74267eb05f4",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0015-agent-governance-contract-normalization/plan.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0015-agent-governance-contract-normalization/plan.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "c0274b6b3cead517fb4f999d0b345bbb5d1f7ff8",
    "content_sha256": "eaa6e269360fbc121218f8a367b96674fde822e51bc48e2a2a6289d4c1ba07fd",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0015-agent-governance-contract-normalization/spec.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0015-agent-governance-contract-normalization/spec.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "c68d7589da9c3ec301589b43da3b1abaed76c991",
    "content_sha256": "49a45a5d12813ca89d16ee4eedcd71448a074f82fce86b467c140ed71c7be68a",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0015-agent-governance-contract-normalization/tasks/tsk-0001-t-001.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0015-agent-governance-contract-normalization/tasks/tsk-0001-t-001.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "24ae1ac02a51d7b1f1ec3596ca4de82983894bc7",
    "content_sha256": "5c759ccaeb55a9db8eea763b8eede9f91809398becb2e2fabd35c486b5850975",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0015-agent-governance-contract-normalization/tasks/tsk-0002-t-002.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0015-agent-governance-contract-normalization/tasks/tsk-0002-t-002.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "b5aeb22e95afcc1577fb53beb7dc399835556549",
    "content_sha256": "7a692e74f765cddaafe14c9c3955c4cf3ed614ad86a8fb028ea614d6f2c03ded",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0015-agent-governance-contract-normalization/tasks/tsk-0003-t-003.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0015-agent-governance-contract-normalization/tasks/tsk-0003-t-003.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "fb0da2efdeb2b1d8bb631a275b5154c6da22f5b0",
    "content_sha256": "4852c798c4a4aaf0dd390e8caa67aec2629393c77ce65c7d201c3c6987d9da89",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0015-agent-governance-contract-normalization/tasks/tsk-0004-t-004.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0015-agent-governance-contract-normalization/tasks/tsk-0004-t-004.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "c513e9af8a6154f38a836cec0ce9867a3eda642d",
    "content_sha256": "51c4091521498813fa7eb11d2d089f7cef1f5e46404c1de1a91a4ac73abd0ff5",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0015-agent-governance-contract-normalization/tasks/tsk-0005-t-005.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0015-agent-governance-contract-normalization/tasks/tsk-0005-t-005.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "eed3d5e939fd8e78af4c6e61aa7aacce150e193c",
    "content_sha256": "92a55026b8b56669bc2e9797883462fe894d9c67159a91c5bec6d852a4cb9ed7",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0016-active-control-surface-governance-hardening/plan.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0016-active-control-surface-governance-hardening/plan.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "34eab5c4aeef43d861af9cb36f19c4850cceff76",
    "content_sha256": "23d4e0626731cb7bdc547c1fd0df80d1280bb0c483d0e973126a5a4bb4d1797d",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0016-active-control-surface-governance-hardening/spec.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0016-active-control-surface-governance-hardening/spec.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "18d04f852839877afa1fd1b3f17ae37b4f3901ae",
    "content_sha256": "8b58618e98c4524e1db5ea1243bc69bedd32ea202dfac87c23f6a68764723bb6",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0016-active-control-surface-governance-hardening/tasks/tsk-0001-acs-001.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0016-active-control-surface-governance-hardening/tasks/tsk-0001-acs-001.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "569821340f397b56dab56708545c07cfe09267d6",
    "content_sha256": "513c959f3921574dd75746d144b34c369ca8cea01dd532b34154b8ad9ae48f23",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0016-active-control-surface-governance-hardening/tasks/tsk-0002-acs-002.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0016-active-control-surface-governance-hardening/tasks/tsk-0002-acs-002.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "991962089da8014c4796aa020e5ec828e17e250f",
    "content_sha256": "47d7a04827c3774243bab02ba976bac9d5a2ff3a378cd2b4fc987f621063c964",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0016-active-control-surface-governance-hardening/tasks/tsk-0003-acs-003.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0016-active-control-surface-governance-hardening/tasks/tsk-0003-acs-003.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "e8ccf226397b56eca2a4d8ee5a64620969a27758",
    "content_sha256": "76a737385b5625a4a856bc4240dee9b165b8416be54b36d27eb5fa4a7d88a621",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0016-active-control-surface-governance-hardening/tasks/tsk-0004-acs-004.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0016-active-control-surface-governance-hardening/tasks/tsk-0004-acs-004.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "97e86447bf1a84443d2a3071527d2c7a274f860e",
    "content_sha256": "79744a78bc40b3d268da5df2d9b4e49dd6a65a3cd8e65fbb7918d99ebca3e819",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0016-active-control-surface-governance-hardening/tasks/tsk-0005-acs-005.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0016-active-control-surface-governance-hardening/tasks/tsk-0005-acs-005.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "f72d5bde2d05113ef7b4f802203d8a3fb5ed91b2",
    "content_sha256": "4242503b30522ea997bf4e8324ab06808c99ed0ae1b63f16253ad48ae369dedd",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0017-workspace-engineering-research-pack/plan.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0017-workspace-engineering-research-pack/plan.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "71ff6247346c73a79ad4cde69e438067d5b52950",
    "content_sha256": "4e9f4a056c27183a5301a4a740e339b140acba2eefd8dc31757c78760f612295",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0017-workspace-engineering-research-pack/spec.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0017-workspace-engineering-research-pack/spec.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "12c6cd68d44645c85441f533aa3e18adb954e475",
    "content_sha256": "6600b6131dc7f0b91da5e90872ebdcd0b0c6c43c3896024957a7c2165a82cfd1",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0017-workspace-engineering-research-pack/tasks/tsk-0001-wer-001.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0017-workspace-engineering-research-pack/tasks/tsk-0001-wer-001.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "ebab5c84e4a4bf25bdce36e5d78a7a3f371bc746",
    "content_sha256": "112375e583a9c65920aa22452f1025d94e3fee24062cc5f9cf56ab2c460d04a4",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0017-workspace-engineering-research-pack/tasks/tsk-0002-wer-002.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0017-workspace-engineering-research-pack/tasks/tsk-0002-wer-002.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "a08bb7747462994bfdd82c8ffcda55d2a081f3b2",
    "content_sha256": "0f37395fc6ec7a19f36983fe3281d4e00c7a805931c83874d4b1cd0444629716",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0017-workspace-engineering-research-pack/tasks/tsk-0003-wer-003.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0017-workspace-engineering-research-pack/tasks/tsk-0003-wer-003.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "79e36efc82375c9f930c200fcca2546f081ed6c8",
    "content_sha256": "590a148e0949ca2fa06f6c83cccff26846122f648ee66a0a73d5eb65a3260669",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0017-workspace-engineering-research-pack/tasks/tsk-0004-wer-004.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0017-workspace-engineering-research-pack/tasks/tsk-0004-wer-004.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "fe3fc7be686f010c32207864748c3cdd385da118",
    "content_sha256": "487b305942cda270b9a60a125971840427e81c569504bcd69fecadfc05fec68c",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0017-workspace-engineering-research-pack/tasks/tsk-0005-wer-005.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0017-workspace-engineering-research-pack/tasks/tsk-0005-wer-005.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "ac6bec119bf7f8533b72367d1e637907de8ac57e",
    "content_sha256": "c5c82bcfcbb10402460c785d833d504b1572a944047eb1b5089c3e61d98f5a60",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0017-workspace-engineering-research-pack/tasks/tsk-0006-wer-006.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0017-workspace-engineering-research-pack/tasks/tsk-0006-wer-006.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "29ab1995a54a23f274aa7be9d144204ae59a633b",
    "content_sha256": "3c3dcb5a17e042ba6bdddd1a5510af74c5f8ab06459ebb02de196e7ab1118742",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0017-workspace-engineering-research-pack/tasks/tsk-0007-wer-007.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0017-workspace-engineering-research-pack/tasks/tsk-0007-wer-007.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "feb212ae3fa8972943adffa2b7e118937dd42877",
    "content_sha256": "adb032d00f2d58d81675f374b58251b0961705be651e92a95e1a55ba4995437f",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0017-workspace-engineering-research-pack/tasks/tsk-0008-wer-008.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0017-workspace-engineering-research-pack/tasks/tsk-0008-wer-008.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "281b2b8c2eb0acbe0904e7aef9ef34b9b5943d10",
    "content_sha256": "5e8625e361c4cd0b592f58383a24dbb3e8142b85c4259582cf7758af81b4863a",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0018-workspace-engineering-implementation-audit-pack/plan.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0018-workspace-engineering-implementation-audit-pack/plan.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "b10d90b8a81eadbf976f1f302cb44f1d2ef41274",
    "content_sha256": "0721a1132d40bb24084e6ddda535894ffc79d322b91d1c4b5844bd5477d7ccbf",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0018-workspace-engineering-implementation-audit-pack/spec.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0018-workspace-engineering-implementation-audit-pack/spec.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "1dff7b4de18e9f452f22d9725ad8b2a9f5995411",
    "content_sha256": "df7d70224dc3871642c0b4b85b4ef1acc1682921f80c05345aa70203c9d8cfa4",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0018-workspace-engineering-implementation-audit-pack/tasks/tsk-0001-wea-001.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0018-workspace-engineering-implementation-audit-pack/tasks/tsk-0001-wea-001.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "6fd40912b3464a3eb22f3ad32fc07250d9ead46a",
    "content_sha256": "5ff7cc296f2e5caa11d4176ea78ef98f8f72352a3eb4c40f961b0c626f0b0022",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0018-workspace-engineering-implementation-audit-pack/tasks/tsk-0002-wea-002.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0018-workspace-engineering-implementation-audit-pack/tasks/tsk-0002-wea-002.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "3d204588e0302e0e45983ca66c71d05aeb136a60",
    "content_sha256": "16cdcc4c48d4bf1ef67a3e24bd2d11c50b0755a39fbb73586d44a969cf5ee081",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0018-workspace-engineering-implementation-audit-pack/tasks/tsk-0003-wea-003.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0018-workspace-engineering-implementation-audit-pack/tasks/tsk-0003-wea-003.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "b5706ff43d508236f680b292b05b431d05903875",
    "content_sha256": "730313cdc3881295d4eb75424feecb6420d8a78d502cb7c76c45bfba354a70ba",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0018-workspace-engineering-implementation-audit-pack/tasks/tsk-0004-wea-004.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0018-workspace-engineering-implementation-audit-pack/tasks/tsk-0004-wea-004.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "6f58252aac48361a264b4861539dca94b2b69973",
    "content_sha256": "f04cd49cd93c79395aee7219a0a43593566f6eca761d094e7511f403ae4cb5ad",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0018-workspace-engineering-implementation-audit-pack/tasks/tsk-0005-wea-005.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0018-workspace-engineering-implementation-audit-pack/tasks/tsk-0005-wea-005.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "d2995241389c79b69ab5584d0a9d4c755e6f45c9",
    "content_sha256": "523f6e2bf45af433d034d885750f04c5c50499d01f1dcbca667f0afda6078f7a",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0018-workspace-engineering-implementation-audit-pack/tasks/tsk-0006-wea-006.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0018-workspace-engineering-implementation-audit-pack/tasks/tsk-0006-wea-006.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "3b93a28e9253546b8dca0ad9f16321918feb69f9",
    "content_sha256": "9cd3a11957e4530914a1d2845a3ac8dc8d288fd1c5622bb44fc6e745c2a36450",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0018-workspace-engineering-implementation-audit-pack/tasks/tsk-0007-wea-007.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0018-workspace-engineering-implementation-audit-pack/tasks/tsk-0007-wea-007.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "3850501a281a86a7e1a1a33e69e79c22445d80f6",
    "content_sha256": "e1f72a0150a532e4a4c73c00289b81d2569674b11bb1d4cda8fd240385eaac21",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0019-template-path-numbering-contract/plan.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0019-template-path-numbering-contract/plan.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "cadb6752680c37ea73b15d7b91105e32fd175857",
    "content_sha256": "5c7202d2f54d9fb54263f9dc6dece58a694cf9353c7b3902c7b685d57b50af2a",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0019-template-path-numbering-contract/spec.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0019-template-path-numbering-contract/spec.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "dec5c2f1c969575e467cb4322b702d8b66eda930",
    "content_sha256": "09b4c9a136f799a6a79936a358719432f973fd52b959bfc53b93d83a4e75b098",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0019-template-path-numbering-contract/tasks/tsk-0001-tpn-001.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0019-template-path-numbering-contract/tasks/tsk-0001-tpn-001.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "eba266fe448920c3c607903c08bc85a852071d7b",
    "content_sha256": "c740cf4263df817836d87a9f33f613ed5b8d378ce07022c33982f3beb35478db",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0019-template-path-numbering-contract/tasks/tsk-0002-tpn-002.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0019-template-path-numbering-contract/tasks/tsk-0002-tpn-002.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "48bd7b0d75a5495372fe8a68ee8d0ad836505568",
    "content_sha256": "e624eee22cffe69baf0c861c33a63bc66b6b302cdcad22792ea9029b3d1ac036",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0019-template-path-numbering-contract/tasks/tsk-0003-tpn-003.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0019-template-path-numbering-contract/tasks/tsk-0003-tpn-003.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "07523a83f07a695a1bc96faa5102f91e81826511",
    "content_sha256": "5d187dc4d78306cbda6a4042eef6d2f82a795260b61d4a796b1ab6553c736011",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0019-template-path-numbering-contract/tasks/tsk-0004-tpn-004.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0019-template-path-numbering-contract/tasks/tsk-0004-tpn-004.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "c4385442e3749188d2dfc09effed062ee4d80148",
    "content_sha256": "d5ce8637a6dac311e2a7312a6d9b6133a7d4f1d65271cf0d44ea530ba82695c9",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0019-template-path-numbering-contract/tasks/tsk-0005-tpn-005.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0019-template-path-numbering-contract/tasks/tsk-0005-tpn-005.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "5bfae964ebdc1e6a36eb3c00fb8f77c72cd22148",
    "content_sha256": "c93988998695851334fd9029396a14302806c7ad7cbee046a26a33d96d996210",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0020-workspace-contract-governance-normalization/plan.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0020-workspace-contract-governance-normalization/plan.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "546e0a69ac7229e9bd9bb4fc435c761fabad8764",
    "content_sha256": "f5d3f6361510e7ef3cc6f2b5b493ba2e8973dc57a5f83d470eca3a22b9583cc1",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0020-workspace-contract-governance-normalization/spec.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0020-workspace-contract-governance-normalization/spec.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "51becf18d36a2ae9d24fb45ff72574bccb0093fa",
    "content_sha256": "0e90518650de5a609356e3bf99d5b9d7e6c46595ffd93e7fd768202e78d630a2",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0020-workspace-contract-governance-normalization/tasks/tsk-0001-wcgn-001.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0020-workspace-contract-governance-normalization/tasks/tsk-0001-wcgn-001.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "9045ef5a3350dee800554be0d5e19690d7056888",
    "content_sha256": "4dd5e3a0e5fced8cceeb5cf758fc380ed1cae73a1389e5866c8667524c5d4846",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0020-workspace-contract-governance-normalization/tasks/tsk-0002-wcgn-002.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0020-workspace-contract-governance-normalization/tasks/tsk-0002-wcgn-002.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "ad3144d4f42219c7ec426c2290917fb90e604648",
    "content_sha256": "2334e414b81515e969e4ea0ffb1e873c47ac072bd0b764936d81d076e81fc684",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0020-workspace-contract-governance-normalization/tasks/tsk-0003-wcgn-003.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0020-workspace-contract-governance-normalization/tasks/tsk-0003-wcgn-003.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "8e505bdc21495cc6b0ca92c5347c4a9ec5c412a2",
    "content_sha256": "22d390bfd6c366df64a7deca64e2df1922c36b4976f77bc9ca1d8fbd96d84de3",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0020-workspace-contract-governance-normalization/tasks/tsk-0004-wcgn-004.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0020-workspace-contract-governance-normalization/tasks/tsk-0004-wcgn-004.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "92e45b44583ced1e66f759121a1123687f09390c",
    "content_sha256": "876c10a4f4d0bc2a43d25fe5d101b575b588591f609386807e85542e91dc3bad",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0020-workspace-contract-governance-normalization/tasks/tsk-0005-wcgn-005.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0020-workspace-contract-governance-normalization/tasks/tsk-0005-wcgn-005.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "5aa4592c0036e508f4936c2be508a1575785e45b",
    "content_sha256": "6f7ff044192b5f014dc3354f2c1801e02464de43bb86cf1f6298cee2dc21daa5",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0021-sdlc-lifecycle-contract/plan.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0021-sdlc-lifecycle-contract/plan.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "690baea515f4fdfde568a3d26d8e2a6047ad9fe7",
    "content_sha256": "3837b0de2ac87dd5151114d22371e553bc7ef316f2fd59d7d2fba73fffa08714",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0021-sdlc-lifecycle-contract/spec.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0021-sdlc-lifecycle-contract/spec.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "2833d967de3e0472729bf14cd9ca06b09ced6f18",
    "content_sha256": "02ab105d354ae97312a40d5e4f41dfbc66c1ac04ef79f086a0e38cf3e574e13d",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0021-sdlc-lifecycle-contract/tasks/tsk-0001-t-001.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0021-sdlc-lifecycle-contract/tasks/tsk-0001-t-001.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "724467674ad3677da02ab536f760340b00884eaf",
    "content_sha256": "7e2284b084f0aea74901719c79bc0abce692896183225bd0b52772f8a5c0ad44",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0021-sdlc-lifecycle-contract/tasks/tsk-0002-t-002.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0021-sdlc-lifecycle-contract/tasks/tsk-0002-t-002.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "2347fb21aee4581303beb3b1b7bbd8b75f715618",
    "content_sha256": "378644964aca5ff457f7662e6279d2cc638b9b99e5294ebf6ed3ad2d654826fa",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0021-sdlc-lifecycle-contract/tasks/tsk-0003-t-003.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0021-sdlc-lifecycle-contract/tasks/tsk-0003-t-003.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "e977457a77ab5489eeeb6c3c2be39c852eadb948",
    "content_sha256": "90e36c892cc5704d4fb24e190126250fd257cc5895719c1361c7ff7ae1a8a553",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0021-sdlc-lifecycle-contract/tasks/tsk-0004-t-004.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0021-sdlc-lifecycle-contract/tasks/tsk-0004-t-004.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "88711bef7d9941d163b801e4a4626461190f1710",
    "content_sha256": "66cf8b64b438e5a326f24122927d314e039079c147ad519487258a60bdebd35e",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0022-control-cloud-doc-normalization/plan.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0022-control-cloud-doc-normalization/plan.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "7c0633d17992380baed11f1e94a5f13d9dad5202",
    "content_sha256": "9807a6d28b05ac723c2fef66a86576b3fe74f8303a94013a46acfde14df00b62",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0022-control-cloud-doc-normalization/spec.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0022-control-cloud-doc-normalization/spec.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "a00c6c2a902449bda8fe8b53ab0df7a94a06a962",
    "content_sha256": "80a1a9d20a55d8b2f1ce297cdf5394f12bb9dda557645e0e7ebd7b808f082565",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0022-control-cloud-doc-normalization/tasks/tsk-0001-ccdn-001.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0022-control-cloud-doc-normalization/tasks/tsk-0001-ccdn-001.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "435025eccfe99fd961652bfb811f651ce5c8393c",
    "content_sha256": "432e662db3c9ee0a53778f72136515080165413608a435f777d63e1a3afa0585",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0022-control-cloud-doc-normalization/tasks/tsk-0002-ccdn-002.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0022-control-cloud-doc-normalization/tasks/tsk-0002-ccdn-002.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "656e4e54ce2b663e9c407804d89d17cec0cd471a",
    "content_sha256": "83baf5164a425e6498b275b83a3ae7401ecb82778a6599e8c45ed9caabc0cc1a",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0022-control-cloud-doc-normalization/tasks/tsk-0003-ccdn-003.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0022-control-cloud-doc-normalization/tasks/tsk-0003-ccdn-003.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "949fb2fb7e6a4ac395b94ac9a98c2980208424e4",
    "content_sha256": "5dbf8a5116288eaebfa15ebf0723bea9bb130c8928131e8421e6f7235915c94b",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0022-control-cloud-doc-normalization/tasks/tsk-0004-ccdn-004.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0022-control-cloud-doc-normalization/tasks/tsk-0004-ccdn-004.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "356e7c4f1bce413f636991a3859dc29987a6dfaf",
    "content_sha256": "e277a15e3453f5f282d2f554bdea0b388ec2ac05eefcc10facfb1b63c36b8aff",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0022-control-cloud-doc-normalization/tasks/tsk-0005-ccdn-005.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0022-control-cloud-doc-normalization/tasks/tsk-0005-ccdn-005.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "964859e69363e4c8726570f465717cc97257bc4c",
    "content_sha256": "4db5939b4767a3e31ba170f3bb021a350daf908a7dd668abf2cb083b0518f771",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0022-control-cloud-doc-normalization/tasks/tsk-0006-ccdn-006.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0022-control-cloud-doc-normalization/tasks/tsk-0006-ccdn-006.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "9378f8fd8e8adcebfa60836eb47fd918593112b6",
    "content_sha256": "ea4e8d3dbe1a431a0e41ee706574ed9a061d96479b2419131e1bd1cfb0719ae7",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0023-stage03-04-repo-static-gap-closure/plan.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0023-stage03-04-repo-static-gap-closure/plan.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "79368b69f407535b69bb24167a28e2586384943d",
    "content_sha256": "69be1f394217b18f757e0334dc1f560117c54349c399ef6c57160c16fe584928",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0023-stage03-04-repo-static-gap-closure/spec.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0023-stage03-04-repo-static-gap-closure/spec.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "63b361ba7d6eedb95726c36a358d98412ed06e63",
    "content_sha256": "ff594ee1b9fd17fd208137680b849ac31f1b58d3c1ce2ddcf51b8996afeb11d8",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0023-stage03-04-repo-static-gap-closure/tasks/tsk-0001-s34-001.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0023-stage03-04-repo-static-gap-closure/tasks/tsk-0001-s34-001.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "1d058f997ddf070078ef5f8c2791c9b674fc5c1a",
    "content_sha256": "159db2bc3bd7d749aa4d1183bb34e91cbd90e178daad4ae90f81abf528321c36",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0023-stage03-04-repo-static-gap-closure/tasks/tsk-0002-s34-002.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0023-stage03-04-repo-static-gap-closure/tasks/tsk-0002-s34-002.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "337f1b97cc373315b00dc735e495fa4430b2f620",
    "content_sha256": "5cad10cb0409f4c512496fa0bd6b3d9430aee67c81dbd53e052d5aa08c7b5760",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0023-stage03-04-repo-static-gap-closure/tasks/tsk-0003-s34-003.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0023-stage03-04-repo-static-gap-closure/tasks/tsk-0003-s34-003.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "d743a035a5c7abfb130d14b56d99b5f3358d7447",
    "content_sha256": "7c8f131230bb2378ce4032bde1e7961525aa2daba6ade1ff33d9cfcf344ca961",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0023-stage03-04-repo-static-gap-closure/tasks/tsk-0004-s34-004.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0023-stage03-04-repo-static-gap-closure/tasks/tsk-0004-s34-004.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "764d9f906ca3c05e16d94e9d6f8f80eda7079815",
    "content_sha256": "9bab19a1551327df1a7de5c9b36f7f36122312799ddaa42d1e2fd6ef185c4c1e",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0023-stage03-04-repo-static-gap-closure/tasks/tsk-0005-s34-005.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0023-stage03-04-repo-static-gap-closure/tasks/tsk-0005-s34-005.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "9f8fb1abf2c3c6631fe3333b13666d1ea15480df",
    "content_sha256": "400ef843e084e57a4df772226985d47be851eae0f07cbe16ca8592a0bbef2e9d",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0024-observability-and-network-review-agents/plan.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0024-observability-and-network-review-agents/plan.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "214a839b84ba2f105532b3b5cd12efb9c1e583e9",
    "content_sha256": "89dbfed74a636f79fe4fe4bd57bbd7d0c0ea785c98fdb67a80cf5e79e401f176",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0024-observability-and-network-review-agents/spec.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0024-observability-and-network-review-agents/spec.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "d4cdc0a6564bdb3f1ff82c1ccbd126bb86a8a017",
    "content_sha256": "7ee888caffe621b2fff269fdeaa3fc9348a4070defd5c751eea14b86edff7e17",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0024-observability-and-network-review-agents/tasks/tsk-0001-ona-001.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0024-observability-and-network-review-agents/tasks/tsk-0001-ona-001.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "7cdf8844b8143e827f69e670ab070f0473b69a50",
    "content_sha256": "3d201aac2baa9fc9f6ee4a456fab6afe27df4af065b12fc0f0e9f3b0907de3b5",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0024-observability-and-network-review-agents/tasks/tsk-0002-ona-002.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0024-observability-and-network-review-agents/tasks/tsk-0002-ona-002.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "82c43906b733ba6cc691dc142bb25c899364bf70",
    "content_sha256": "e7b13cc6611cb460f90beb6b064f2ce50ae0a1d5e15a4efc9d7fe25d02d3737b",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0024-observability-and-network-review-agents/tasks/tsk-0003-ona-003.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0024-observability-and-network-review-agents/tasks/tsk-0003-ona-003.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "b6d34f776a6271b8d871809a4469e440c5d48e9a",
    "content_sha256": "301406d2e97620acbf26d242e33e0c19285dd5533a53e80236448cd1e77ec441",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0024-observability-and-network-review-agents/tasks/tsk-0004-ona-004.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0024-observability-and-network-review-agents/tasks/tsk-0004-ona-004.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "2691d3de4981f6d188e0b2654bc4c329d86c27b9",
    "content_sha256": "a3729b48c84bce51abedf8d723b459aed82bffc8bf7141aaab4a3d0742fa8a95",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0025-governance-owner-and-roster-currentness/plan.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0025-governance-owner-and-roster-currentness/plan.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "bbe089ee97e197c80ac38bf5d8008d0ff433095b",
    "content_sha256": "94f4bba290e19638d64eb7e424241f6992de2f8be95b1758e7106b38aa72d2ff",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0025-governance-owner-and-roster-currentness/spec.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0025-governance-owner-and-roster-currentness/spec.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "460351e689135a45582065e49aa87282bcdfa54e",
    "content_sha256": "e8296064f32201d8ae8ecaba3c39a0995d9ef1e0ab14953c0df4005356b66cce",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0025-governance-owner-and-roster-currentness/tasks/tsk-0001-rcr-001.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0025-governance-owner-and-roster-currentness/tasks/tsk-0001-rcr-001.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "7a780b6d863859e76a84c8917e4f6dc1f70a5153",
    "content_sha256": "dc1ff432cb2cb09552b4314b528bdab7b35ed0cb973788aa938545bb439407f3",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0025-governance-owner-and-roster-currentness/tasks/tsk-0002-rcr-002.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0025-governance-owner-and-roster-currentness/tasks/tsk-0002-rcr-002.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "b4d5846b2606d256d9fd4139192ab3e80b013978",
    "content_sha256": "72df6931ec0ce42a77b1635174976e7e17828a3c76e19fd5581dd5bcb5416ccb",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0025-governance-owner-and-roster-currentness/tasks/tsk-0003-rcr-003.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0025-governance-owner-and-roster-currentness/tasks/tsk-0003-rcr-003.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "5abbfbbbe1e1f2d2e73d886daaf99bfa2fd721c2",
    "content_sha256": "8625332111b6293b59f5593fb956ac344b0f7526d82152708e446a017973c355",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0025-governance-owner-and-roster-currentness/tasks/tsk-0004-rcr-004.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0025-governance-owner-and-roster-currentness/tasks/tsk-0004-rcr-004.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "1b69ae5294c762fc2d0178e93aa5eb58bd28bf4f",
    "content_sha256": "d6d7190ef921701d9516dc2d4d6a21ea8934c301c2df0f3380639c8af9918b60",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0025-governance-owner-and-roster-currentness/tasks/tsk-0005-rcr-005.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0025-governance-owner-and-roster-currentness/tasks/tsk-0005-rcr-005.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "a620b8a44645e8ec7116cd2714782b66c4b3959b",
    "content_sha256": "4ac00c9c928e98dd4bff06ea92e5e8fe57ef9d15d2cded1553fff6ca9f189862",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0025-governance-owner-and-roster-currentness/tasks/tsk-0006-rcr-006.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0025-governance-owner-and-roster-currentness/tasks/tsk-0006-rcr-006.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "c98d1022d2c0015ab6f20ced14954885b7c6b838",
    "content_sha256": "693ead969b930444ca308f84905e9a8cbf1746ce4320782d882a294fcc87ebc7",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0026-document-contract-registry/plan.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0026-document-contract-registry/plan.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "e5652b6fe7c82c0d7f65168bcc47a924169c9789",
    "content_sha256": "55ad23ecf9d4cf88c6f20015a8f3e195201a645ef9faa241dc0993b8d255fb10",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0026-document-contract-registry/spec.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0026-document-contract-registry/spec.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "9180477bdc132887e9670902a3507a68a1c6cb93",
    "content_sha256": "2a41e5c60b4b40f63bf544c71131294bca681087a13476a615d51b0e7e8e7c2e",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0026-document-contract-registry/tasks/tsk-0001-dcr-001.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0026-document-contract-registry/tasks/tsk-0001-dcr-001.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "4b2156591f682535395d2c01de56bed022b595e5",
    "content_sha256": "83df504d19ea98c71909e61e76af3e7a3bd89702d5be10140816831810dbe0ca",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0026-document-contract-registry/tasks/tsk-0002-dcr-002.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0026-document-contract-registry/tasks/tsk-0002-dcr-002.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "4bc9459a6ed1ecb38b951036b1982840392337bf",
    "content_sha256": "a7c2e6cd45d47d3c457283ccff85ac68d30ed2267f95c638c9605f9fa7ec7feb",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0026-document-contract-registry/tasks/tsk-0003-dcr-003.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0026-document-contract-registry/tasks/tsk-0003-dcr-003.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "7778f30e82e74033428f1c3986e59ab7d6552731",
    "content_sha256": "ac617b7d8a37b95bed7c6cc0e14896501d8a0fd1cd5bd608526028755a7fcd12",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0026-document-contract-registry/tasks/tsk-0004-dcr-004.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0026-document-contract-registry/tasks/tsk-0004-dcr-004.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "7f76e1a646c5d7a066d2fd180cf3426fcf01d4ed",
    "content_sha256": "51948e0ecb86af205875f8a4f09f62c318ecfaabba8725ee0d1576bd303b4e14",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0026-document-contract-registry/tasks/tsk-0005-dcr-005.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0026-document-contract-registry/tasks/tsk-0005-dcr-005.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "dfd65f1fed92a63e9b4721e1f379f172ef28c094",
    "content_sha256": "2f517d8d2b1975342a8cce7ff6cd75307f907cbeab0a98303b7701b5b8d65ca9",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0027-template-contract-consolidation/plan.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0027-template-contract-consolidation/plan.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "1ef19777ccc212db6d1c949942a116724443ad95",
    "content_sha256": "ee66de12fda25c9565ba42f32b23fac1c164e2caf0de9b54e8d5c93244b84aa4",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0027-template-contract-consolidation/spec.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0027-template-contract-consolidation/spec.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "a923c3441f2295ae2dc82f60125f7157c1170658",
    "content_sha256": "03d2349b9d1671276192b8d6dcdb57853ca36cb34cd65b096f5fc3e87b15c3fd",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0027-template-contract-consolidation/tasks/tsk-0001-tcc-001.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0027-template-contract-consolidation/tasks/tsk-0001-tcc-001.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "434073df4ff4fc56f8d36ab3b6bb0a58372a68b7",
    "content_sha256": "83836ccade047d5127bd877d24adeb4b991e889a9b85a8e80f50d3e6d12d7366",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0027-template-contract-consolidation/tasks/tsk-0002-tcc-002.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0027-template-contract-consolidation/tasks/tsk-0002-tcc-002.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "12a8813378145a6efe1c6b1fbe57e38aafb6fe75",
    "content_sha256": "3c0413b595e9646d5791fce6535dd3016a16d0965fe06e2232ff82dae8195c43",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0027-template-contract-consolidation/tasks/tsk-0003-tcc-003.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0027-template-contract-consolidation/tasks/tsk-0003-tcc-003.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "4f08c893c4ee6582b00117c325181b3c0436f19d",
    "content_sha256": "7dbe657fc7dfbea7b63e300e8867013aa0df5efade68d928f5252e96fe3e0c2f",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0027-template-contract-consolidation/tasks/tsk-0004-tcc-004.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0027-template-contract-consolidation/tasks/tsk-0004-tcc-004.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "d34985bb8365c27ac4931cdb72a269e9f4399b75",
    "content_sha256": "4340bbe45cbd30890c298eccd94987ff3e64cb7897a62ab6d273ddc760f40423",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0027-template-contract-consolidation/tasks/tsk-0005-tcc-005.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0027-template-contract-consolidation/tasks/tsk-0005-tcc-005.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "3fc6f8f007f823eb3d0170672d97436531bc41fc",
    "content_sha256": "b20b525bad614e6f002f306e5fc0550cc504257fc26dc79e173245e36c64d71d",
    "reason": "The package is complete, so its Stage 03 path retires and the retained copy carries the same document with its relative link prefixes re-based to the retention tree."
  },
  {
    "legacy_path": "docs/03.specs/0027-template-contract-consolidation/tasks/tsk-0006-tcc-006.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "replaced",
    "replacement": "docs/98.archive/completed/03.specs/0027-template-contract-consolidation/tasks/tsk-0006-tcc-006.md",
    "source_commit": "ae09213d07229b59d1ccff1102dbf6f020e54d2f",
    "source_blob": "4f147e3e81d1113656c928f43101b4d3c3e1787a",
    "content_sha256": "8ae9bdce7a29c1994ed3d7074c599df6ed825b74cf2dd9dbc350043a37a6aa6a",
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
