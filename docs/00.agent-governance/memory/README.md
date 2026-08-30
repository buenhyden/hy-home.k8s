# Historical Context Transition

## Overview

This directory retains earlier progress context while Spec 0054 completes its
approved progress-owner retirement. It is not a current policy or task-status
authority.

## Scope

Read historical entries only when relevant to the task and recheck their claims
against current repository owners. Do not rewrite the historical body to
conceal stale paths, and do not append new-work status here.

The ledger's own header contradicts this README: it instructs the reader to
author new entries from the progress template and names a removed
`harness-catalog.md` as current runtime truth. That header is historical text
under a byte freeze, not an instruction. `MIG-0005` is sealed and its
historical-consumers block pins the ledger's exact bytes as of its recorded
source commit, so the body cannot be edited, truncated, or deleted while that
migration stands. This README is the authority for what may be written here;
the header is not.

## Item Index

- `progress.md`: retained historical work context, byte-frozen by the sealed
  `MIG-0005` consumer proof. Spec 0064 measured that freeze and recorded that
  the approved retirement cannot complete while it stands; recovery remains
  Git-backed.

## Add and Find

Record current status, commands, verification, and handoff in the owning
Spec Task. Route durable lessons to the responsible policy, skill, operating
document, or reference owner under
[context and memory policy](../policies/context-and-memory.md).
Use the [Archive index](../../98.archive/README.md) for retired routes.

## Related Documents

- [Governance Hub](../README.md)
- [Context and Memory](../policies/context-and-memory.md)
- [Work Lifecycle](../skills/work-lifecycle.md)
