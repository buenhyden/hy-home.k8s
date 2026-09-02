---
title: 'Codex Provider Notes'
version: "1.0.0"
type: governance/provider
status: active
owner: platform
updated: 2026-08-28
---

# Codex Provider Notes

## Overview

Describe Codex-native loading and configuration without duplicating shared
execution policy or the agent roster.

## Authority Boundary

`AGENTS.md` is the thin Codex gateway; `.codex/CODEX.md` is the local
baseline. Native sandbox, approval, and configuration surfaces govern the
running client. The neutral registry owns shared role and permission meaning.

## Governance Context

Load the gateway, [work lifecycle](../skills/work-lifecycle.md), relevant
responsibility, and current Task. Codex TOML role projections carry native
model and reasoning metadata; configured values alone do not prove provider
resolution or tool enforcement.

## Current Contract

- Use `.codex/agents/*.toml` projections selected by the neutral registry when
  authorized delegation and the current runtime mechanism are available.
- Read shared skills through `.codex/skills`, a view of the neutral owner.
  File presence is not evidence of native skill discovery.
- Use native sandbox and approval controls; do not treat a custom hook file as
  a permission or completion gate.
- Unsupported custom hook graphs are not a Codex execution surface. Run
  explicit repository validation; do not infer event delivery from a file.
- Keep provider-local memory advisory and re-observe repository/task state on
  resume. Shared context and safety rules live in policies, not this note.
- Follow `RTK.md` for shell tooling. Record an unavailable tool or runtime
  instead of inspecting private configuration to manufacture readiness.

## Validation and Refresh

Validate registry/projection semantics and native configuration after relevant
changes. Check the intended installed client's documented configuration when a
native capability changes. Separately evidence discovery, authenticated
execution, model resolution, sandbox/approval behavior, and event delivery;
repository-static PASS establishes none of them.

## Related Documents

- [Codex Baseline](../../../.codex/CODEX.md)
- [Agent Registry](../../../.agents/registry.json)
- [Model Selection](../policies/model-selection.md)
- [Quality Policy](../policies/quality.md)
