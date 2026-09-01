---
title: 'Claude Provider Notes'
version: "1.0"
type: governance/reference
layer: "00.agent-governance"
status: active
owner: platform
updated: 2026-08-28
---

# Claude Provider Notes

## Overview

Describe Claude-native loading, permissions, and hooks without duplicating
shared execution policy or the agent roster.

## Authority Boundary

Root `CLAUDE.md` is the thin Claude gateway and must not import the Codex
gateway. `.claude/CLAUDE.md` is the local baseline;
`.claude/settings.json` carries native permission and hook declarations.
These may restrict but never expand common approval boundaries.

## Governance Context

Load the gateway, [work lifecycle](../skills/work-lifecycle.md), relevant
responsibility, and current Task. Claude Markdown role projections carry
native model and least-privilege tool metadata; the neutral registry owns
their shared responsibility and permission meaning.

## Current Contract

- Use `.claude/agents/*.md` projections selected by the neutral registry for
  authorized delegation through the available runtime mechanism.
- Read shared skills through `.claude/skills`, a view of the neutral owner.
  File presence alone does not prove native discovery or use.
- Tracked settings reference shared lifecycle hooks. A hook can enforce a
  boundary only when the intended runtime actually loads and dispatches it;
  advisory compaction output is not completion evidence.
- Keep managed, project, and user instruction precedence intact. Use imports
  for shared context rather than copying policy into provider files.
- Treat auto-memory and ignored local warning files as auxiliary context, not
  shared policy or a substitute for repository validators.
- Do not add native metadata fields from assumptions about another client
  version. Verify the intended runtime contract when configuration changes.

## Validation and Refresh

Validate registry/projection semantics, tool metadata, settings, and hook
configuration after relevant changes. Separately evidence native discovery,
permission enforcement, hooks, model resolution, and authenticated operation.
Repository-static or hosted CI results cannot establish runtime success.

## Related Documents

- [Claude Baseline](../../../.claude/CLAUDE.md)
- [Agent Registry](../../../.agents/registry.json)
- [Model Selection](../policies/model-selection.md)
- [Quality Policy](../policies/quality.md)
