---
title: "Claude Provider Notes"
version: "1.0.0"
type: "governance/provider"
status: "active"
owner: "platform"
updated: "2026-08-28"
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

Load the gateway, [work lifecycle](../.agents/workflows/work-lifecycle.md), relevant
responsibility, and current Task. Claude Markdown role projections carry
native model and least-privilege tool metadata; the neutral registry owns
their shared responsibility and permission meaning.

## Current Contract

Each `.claude/skills/<id>` is a relative link to
`../../.agents/skills/<id>`. `disable-model-invocation: true` requires explicit
invocation. The common procedure retains the selected role and user scope.

- Use `.claude/agents/*.md` projections selected by the neutral registry for
  authorized delegation through the available runtime mechanism.
- Read shared skills through `.claude/skills`, a view of the neutral owner.
  File presence alone does not prove native discovery or use.
- Tracked settings register only `.claude/hooks/k8s-pre-edit.sh` for pre-action
  safety. It enforces a boundary only when the intended runtime loads it.
  Run QA explicitly; edit, Stop, and compaction events do not run whole QA.
- Keep managed, project, and user instruction precedence intact. Use imports
  for shared context rather than copying policy into provider files.
- Treat auto-memory and ignored local warning files as auxiliary context, not
  shared policy or a substitute for repository validators.
- Do not add native metadata fields from assumptions about another client
  version. Verify the intended runtime contract when configuration changes.

Model labels use exact provider IDs to preserve the existing selection:
Sonnet 4.6 is `claude-sonnet-4-6`, Opus 4.8 is `claude-opus-4-8`,
and Sonnet 5 is `claude-sonnet-5`. These are configuration intent; actual
availability and resolution remain separate runtime evidence. The native
`Task` tool remains a documented alias for `Agent`.
See [subagent fields](https://code.claude.com/docs/en/sub-agents),
[model IDs](https://support.claude.com/en/articles/11940350-claude-code-model-configuration),
and [settings](https://code.claude.com/docs/en/settings).

## Validation and Refresh

Validate registry/projection semantics, tool metadata, settings, and hook
configuration after relevant changes. Separately evidence native discovery,
permission enforcement, hooks, model resolution, and authenticated operation.
Repository-static or hosted CI results cannot establish runtime success.

## Related Documents

- [Claude Baseline](CLAUDE.md)
- [Agent Registry](../.agents/roles/registry.json)
- [Model Selection](../.agents/governance/model-selection.md)
- [Quality Policy](../.agents/governance/quality.md)
