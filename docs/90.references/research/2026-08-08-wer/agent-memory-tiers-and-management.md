---
title: 'Reference: Agent Memory Tiers and Management'
type: content/reference
status: active
owner: platform
updated: 2026-08-08
---

# Reference: Agent Memory Tiers and Management

## Overview

Baseline routing for the workspace's memory classes and management lifecycle.

## Reference Type

Repository-static research baseline.

## Authority Boundary

The Stage 00 memory contract owns class definitions and canonical authority.
Provider-local stores are advisory and never override repository evidence.

## Scope

It separately tracks short-term, long-term, domain-scoped memory, and memory
management for WERPC-006.

## Definitions / Facts

### Short-term-memory baseline

`.agent-work/checkpoint.json` is documented ignored working context. Its
existence or runtime use is Unverified and it is not read by this task.

### Long-term-memory baseline

`docs/00.agent-governance/memory/progress.md` is the durable shared progress
ledger.

### Domain-scoped-memory baseline

Owning Specs, Runbooks, Incidents, and Postmortems are the documented
domain-scoped owners; current domain completeness is Unverified.

### Memory-management baseline

`docs/00.agent-governance/memory/README.md` documents refresh, retention,
promotion, conflict, and handoff rules. Runtime enforcement is Unverified.

## Sources

No current external memory source was reviewed in WERPC-001. Historical URLs
remain dated predecessor evidence requiring a current recheck.

## Review and Freshness

WERPC-006 owns source-backed memory research. Refresh after memory-contract or
lifecycle-validator changes.

## Related Documents

- [Pack coverage matrix](README.md#requirement-coverage-matrix)
- [Source ledger](source-coverage-and-migration-ledger.md)
- [Memory README](../../../00.agent-governance/memory/README.md)
