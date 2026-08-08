---
title: 'Reference: Harness and Loop Engineering'
type: content/reference
status: active
owner: platform
updated: 2026-08-08
---

# Reference: Harness and Loop Engineering

## Overview

Baseline routing for harness elements and the agent execution loop.

## Reference Type

Repository-static research baseline.

## Authority Boundary

Stage 00 contracts own harness and loop controls; this reference does not prove
runtime operation, evaluation quality, or provider execution.

## Scope

It covers the documented harness and loop boundaries, recovery and verification
routes, and workspace application controls.

## Definitions / Facts

### Harness baseline

`.codex/CODEX.md` describes the local four-element harness contract. Actual
harness delivery by provider runtimes is Unverified.

### Loop baseline

`docs/00.agent-governance/rules/agentic.md` is the documented execution-loop
owner. Runtime recovery behavior is Unverified.

## Sources

No WERPC-001 external research was performed. Dated predecessor material is
registered as recheck-required evidence in the source ledger.

## Review and Freshness

WERPC-002 must add source-backed findings and distinguish repository-static
controls from observed runtime behavior.

## Related Documents

- [Workspace governance baseline](workspace-governance-and-common-agent-environment.md)
- [Source ledger](source-coverage-and-migration-ledger.md)
- [Agentic execution rules](../../../00.agent-governance/rules/agentic.md)
