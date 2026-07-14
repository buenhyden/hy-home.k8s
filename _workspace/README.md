# _workspace

> Repository-local support staging for temporary, non-secret analysis artifacts.

## Overview

`_workspace/` is an isolated repository-support staging boundary for
short-lived, non-secret artifacts produced while auditing, dry-running a
migration, or inventorying routes. It is not a home for durable documentation,
runtime diagnostics, authentication state, or personal local data.

Only this README is tracked. Scratch children remain ignored and must not be
forced into Git.

## Permitted Artifacts

- Temporary audit scratch.
- Redacted, non-secret dry-run summaries.
- Generated route inventories.
- Migration ledgers.
- Non-secret scan summaries.

Every artifact must be bounded to repository support, safe to delete, and free
of credentials or secret-bearing runtime detail.

## Forbidden Local State

Do not place any of the following in `_workspace/`:

- Credentials, tokens, auth files, or kubeconfigs.
- SSH keys, certificates, or other private key material.
- Shell history, browser profiles, provider caches, or local settings.
- Personal diagnostics or local logs that may expose private state.
- Secret-bearing scan output, dry-run logs, or command transcripts.

Diagnostics, local logs, auth material, tokens, and shell history belong
outside the repository and outside this staging boundary.

## Promotion and Cleanup

Promote a durable outcome to its canonical owner:

- Stage 00 for agent governance and reusable memory.
- Stage 04 for execution plans, tasks, and validation evidence.
- Stage 90 for durable audits and reference material.
- Stage 99 for template and support contracts.

Delete temporary artifacts before task closure when they have no durable
destination. Promotion must preserve the destination document's template,
review, and secret-handling contract; do not promote raw scratch by force-adding
it.

## Tracking Rules

The tracked shape is:

```text
_workspace/
├── README.md          # Tracked contract for this staging boundary
└── <ignored scratch>  # Temporary non-secret repository-support files
```

The contract is verified only through Git metadata:

- `git ls-files _workspace` must return `_workspace/README.md`.
- `git check-ignore -q _workspace/probe.tmp` must succeed without creating the
  probe.

Do not list, open, read, hash, move, or delete ignored children while checking
this rule.

## Related Documents

- [Documentation Protocol](../docs/00.agent-governance/rules/documentation-protocol.md)
- [Approval Boundaries](../docs/00.agent-governance/rules/approval-boundaries.md)
- [Subagent Protocol](../docs/00.agent-governance/subagent-protocol.md)
- [Documentation Contract](../docs/99.templates/support/documentation-contract.md)
- [Workspace-staging README form](../docs/99.templates/templates/common/readme-workspace-staging.template.md)
