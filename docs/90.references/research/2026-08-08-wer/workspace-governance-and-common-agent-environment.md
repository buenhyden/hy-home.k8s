---
title: 'Reference: Workspace Governance and Common Agent Environment'
type: content/reference
status: active
owner: platform
updated: 2026-08-08
---

# Reference: Workspace Governance and Common Agent Environment

## Overview

Baseline routing for the repository's shared agent environment and application
of its documented governance.

## Reference Type

Repository-static research baseline.

## Authority Boundary

Current governance remains owned by Stage 00 rules and provider notes; this
reference does not alter runtime permissions or active policy.

## Scope

It covers shared instructions, templates, scripts, and workspace application;
provider-specific product findings belong in provider status.

## Definitions / Facts

### Common-system baseline

`docs/00.agent-governance/harness-catalog.md` is the workspace catalog owner.
The effectiveness of any configured provider integration is Unverified.

### Workspace-application baseline

`AGENTS.md` is the repository gateway and `RTK.md` is its shell-command guide.
Whether every provider consumes either file is Unverified.

## Sources

No current external source was reviewed in WERPC-001. `SRC-WERPC-001` through
`SRC-WERPC-003` in the ledger are dated predecessor evidence and require a
current recheck before supporting a material external claim.

## Review and Freshness

Refresh when WERPC-002 records primary sources or when a canonical Stage 00
owner changes. Current truth remains with the linked workspace owners.

## Related Documents

- [Pack coverage matrix](README.md#requirement-coverage-matrix)
- [Provider implementation status](provider-implementation-status.md)
- [Governance bootstrap](../../../00.agent-governance/rules/bootstrap.md)
