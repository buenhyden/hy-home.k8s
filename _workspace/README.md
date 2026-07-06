# _workspace

> Repository-local support staging area for temporary, non-secret analysis scratch.

## Overview

`_workspace/` is a repository-local support staging boundary for temporary
analysis scratch. It exists so agents and maintainers can place short-lived,
non-secret evidence while auditing, dry-running migrations, or inventorying
routes without turning scratch into durable documentation.

Scratch artifacts remain ignored by default; only this README is tracked.

## Audience

This README is for:

- AI Agents
- Platform Maintainers
- Documentation Writers
- Reviewers

## Scope

### In Scope

- Temporary audit scratch.
- Redacted, non-secret dry-run logs and summaries.
- Generated route inventories.
- Migration ledgers.
- Non-secret scan summaries.

### Out of Scope

- Credentials.
- Tokens.
- Auth files.
- Shell history.
- Kubeconfigs.
- SSH keys.
- Browser profiles.
- Provider caches.
- Personal diagnostics that may contain local private state.
- Secret-bearing local logs.

## Structure

```text
_workspace/
├── README.md          # Tracked contract for this staging boundary
└── <ignored scratch>  # Temporary non-secret analysis files
```

## How to Work in This Area

1. Use `_workspace/` only for temporary, non-secret repo-support staging.
2. Do not place credentials, tokens, auth files, shell history, kubeconfigs,
   SSH keys, browser profiles, provider caches, personal diagnostics, or
   secret-bearing local logs here.
3. Keep scratch artifacts ignored by default. Do not force-add scratch files.
4. Promote durable findings to Stage 04 task evidence, Stage 90 audits, Stage
   00 governance, Stage 99 support contracts, or delete them before closure.

## Link Basis

Links in this README resolve from `_workspace/`.

- Use `../docs/04.execution/` for execution plans, task records, and command
  evidence.
- Use `../docs/90.references/` for durable audits or reference material.
- Use `../docs/00.agent-governance/` for governance changes.
- Use `../docs/99.templates/support/` for support contract changes.

## Related Documents

- [Documentation Protocol](../docs/00.agent-governance/rules/documentation-protocol.md)
- [Approval Boundaries](../docs/00.agent-governance/rules/approval-boundaries.md)
- [Subagent Protocol](../docs/00.agent-governance/subagent-protocol.md)
- [Documentation Contract](../docs/99.templates/support/documentation-contract.md)
