---
title: "Agent Progress Ledger Retirement"
version: "1.0.0"
type: "archive/migration"
layer: "archive"
status: "sealed"
owner: "platform"
updated: "2026-08-30"
artifact_id: "MIG-0007"
---

# MIG-0007: Agent Progress Ledger Retirement

## Overview

This reviewed ledger records the retirement of
`docs/00.agent-governance/memory/progress.md`, the agent progress and memory
ledger, under Spec 0054 WP-012.

The ledger contradicted its own owner. `memory/README.md` forbids appending
new-work status there, while the ledger's header instructed the reader to use
the progress template for new entries and named
`docs/00.agent-governance/harness-catalog.md` as current runtime truth. That
file was removed. A record that instructs a reader to write into it, against
the policy that owns it, and cites a removed file as current, is not history
worth checking out.

Its size is the second reason. At 938488 bytes and 19086 lines it held 232 of
the 234 commit pins across `docs/00.agent-governance/`, `.agents/`, `.claude/`
and `.codex/`; the other three surfaces hold none. Each pin binds a past commit,
so the file grew a maintenance cost that rises as history advances while its
content describes work already finished.

No Tombstone accompanies this row. ADR-0030 admits a Tombstone only for a
deleted path that needs a durable replacement owner, and forbids one where a
Migration and Git recovery suffice. The ledger has no successor document: its
per-work evidence is owned by the Spec Tasks that produced it, and its bytes
remain reachable from Git. ADR-0030 also directs active documents to link the
Archive README or the relevant Migration rather than an individual Tombstone,
which is what this record provides.

## Migration Ledger

<!-- archive-migration-ledger:v1 format=json -->

```json
[
  {
    "legacy_path": "docs/00.agent-governance/memory/progress.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "deleted",
    "replacement": null,
    "source_commit": "90b5a74563db032bb00a4aaea270aafb2d8567ab",
    "source_blob": "e3e3e9730c1f4e7b9d506771c7e1b4cd1aa3e1e2",
    "content_sha256": "96d5045a2cecc6cc56eebe11a96efca382f5e5bb58114ba3919a545bb15ca259",
    "reason": "Retire a historical ledger that contradicted its owning README, cited a removed file as current runtime truth, and concentrated 232 of the four surfaces' 234 commit pins; its per-work evidence is owned by the Spec Tasks that produced it and its bytes remain recoverable from Git."
  }
]
```

## Recovery

Recover the retired bytes with `git show
90b5a74563db032bb00a4aaea270aafb2d8567ab:docs/00.agent-governance/memory/progress.md`
and verify both `source_blob` and `content_sha256` against the row above. The
row's action is `deleted`, so it composes no replacement target and resolves
through the Archive index.

### Historical consumers

Twelve current documents link the retired ledger. Eight already resolve through
MIG-0005, which registers them as its own consumers. The four below are the
remainder, and each is terminal: the registry classifies `done` as terminal for
`sdlc/spec` and `sdlc/plan`, so their bytes cannot be edited to drop the link.
Registration is what admits such a link; terminal status alone is not, because
registration records that a reviewer examined the citation at a named commit.
Each renders a link the ledger row retires, which is the reviewed disposition
this block requires.

The retired ledger itself is not registered here. MIG-0005 already registers it
as one of that record's consumers, and a second registration would be an
ambiguous consumer identity.

<!-- archive-historical-consumers:v1 format=json -->

```json
[
  {
    "source_commit": "2a74c122284604cef69e3a2ad344e8545bcbb314",
    "paths": [
      "docs/03.specs/0023-stage03-04-repo-static-gap-closure/plan.md",
      "docs/03.specs/0023-stage03-04-repo-static-gap-closure/spec.md",
      "docs/03.specs/0060-platform-currency-defect-closure/plan.md",
      "docs/03.specs/0061-workload-security-context-baseline/plan.md"
    ]
  }
]
```
