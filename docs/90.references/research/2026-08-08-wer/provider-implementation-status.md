---
title: 'Reference: Provider Implementation Status'
type: content/reference
status: active
owner: platform
updated: 2026-08-08
---

# Reference: Provider Implementation Status

## Overview

Baseline separation of provider product surfaces from tracked local adapters.

## Reference Type

Repository-static research baseline.

## Authority Boundary

Provider product documentation and authenticated runtimes own product behavior.
Tracked adapter files prove only repository-static configuration.

## Scope

It separates Claude and Codex from common workspace rules and leaves external
surface claims for WERPC-002.

## Definitions / Facts

### Claude baseline

The tracked `.claude/` surface is local configuration evidence. Native
discovery, authentication, and runtime use are Unverified.

### Codex baseline

`.codex/CODEX.md` and `.codex/agents/` are tracked local evidence. Native
discovery, permissions, model resolution, and runtime use are Unverified.

## Sources

No provider page was checked in WERPC-001. Predecessor URLs, if retained, are
dated evidence only and require WERPC-002 current recheck.

## Review and Freshness

Refresh on current official-source review or a material local adapter change;
never infer runtime status from static files.

## Related Documents

- [Common environment](workspace-governance-and-common-agent-environment.md)
- [Model routing](agent-model-routing-and-configuration.md)
- [Codex provider notes](../../../00.agent-governance/providers/codex.md)
