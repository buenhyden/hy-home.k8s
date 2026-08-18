---
title: "MIG-0003: Agent Governance Control Plane Consolidation"
type: "content/archive-migration"
status: "accepted"
owner: "platform"
updated: "2026-08-14"
artifact_id: "MIG-0003"
migration_id: "MIG-0003"
---

# MIG-0003: Agent Governance Control Plane Consolidation

## Overview

This reviewed ledger binds the WORK-054-003 Stage 00 agent-governance cutover
to the exact source commit. It records three legacy active reference owners
merged into the canonical Stage 00 control plane.

## Migration Ledger

<!-- archive-migration-ledger:v1 format=json -->

```json
[
  {
    "legacy_path": "docs/00.agent-governance/common-governance.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/00.agent-governance/harness-catalog.md",
    "source_commit": "128beada377f18bc9f942c8ebb3e27e1f2fdcfae",
    "source_blob": "de7e7edfe177ff349cd3824aebd82418adff95d7",
    "content_sha256": "c5da620d5f6c1aa26f2e0d99769872b90c6d2ec2fdb3c03813be27992f43e4ba",
    "reason": "Merge duplicate common agent-governance concepts and adapter ownership tables into the canonical harness catalog, model policy, rules, and provider notes."
  },
  {
    "legacy_path": "docs/00.agent-governance/harness-implementation-map.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/00.agent-governance/harness-catalog.md",
    "source_commit": "128beada377f18bc9f942c8ebb3e27e1f2fdcfae",
    "source_blob": "7e7a6d64a05be91658cc6657cd640491153a615a",
    "content_sha256": "3ea2f89c3ba17fbf0bac64533cbb5a378a85c062a020881a3844cfa190c9c218",
    "reason": "Merge duplicate harness implementation navigation into the canonical harness catalog, validation-surface contract, quality standards, approval boundaries, and operations links."
  },
  {
    "legacy_path": "docs/00.agent-governance/providers/agents-md.md",
    "stable_path": null,
    "artifact_id": null,
    "action": "merged",
    "replacement": "docs/00.agent-governance/providers/codex.md",
    "source_commit": "128beada377f18bc9f942c8ebb3e27e1f2fdcfae",
    "source_blob": "06d9a7a5453ac8b6e28268850467e3e96de06dc9",
    "content_sha256": "5ea07c187ea54061f5ecc770a58a99edf40dfd73372ba8fc9e1d4ab14bf85bae",
    "reason": "Merge the AGENTS.md gateway note into the Codex provider note and root gateway shim so provider-specific guidance has one active owner."
  }
]
```

## Recovery

For every row, recover the legacy bytes with `git show
<source_commit>:<legacy_path>` and verify both `source_blob` and
`content_sha256`. Merged rows resolve through `replacement`; their legacy bytes
remain recoverable from Git history.
