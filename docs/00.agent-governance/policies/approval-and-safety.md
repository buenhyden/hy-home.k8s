---
title: 'Approval and Safety Policy'
version: "1.0.0"
type: governance/rule
status: active
owner: platform
updated: 2026-08-28
---

# Approval and Safety Policy

## Overview

Agents prepare desired-state changes and local evidence within the user's
scope. Protected actions require explicit human or operator authority.

## Authority Boundary

This policy owns approval decisions. Native sandbox, tool, permission, and
approval controls may be stricter; static configuration never proves runtime
enforcement. Runbooks describe authorized procedures, not standing approval.

## Governance Context

Kubernetes, Argo CD, Vault, cloud, remote Git, and CI operations affect state
outside the reviewable repository. Keep those actions separate from writing
and validating their configuration.

## Current Contract

| Surface | Default | Approval boundary |
| --- | --- | --- |
| Repository docs, manifests, tests, and scripts | Scoped edits and deterministic local validation | Scope expansion or weakened security/gate failure semantics |
| Bootstrap and recovery assets | Edit and review only | Running against a cluster or external service |
| CI configuration | Scoped static edits | Permission expansion, protected triggers, publishing, paid execution, or remote dispatch |
| Git history and worktrees | Inspect; make requested logical commits | Push, PR creation, merge, destructive cleanup, history rewrite, or worktree removal |
| Live cluster, Argo CD, Vault, and cloud | No mutation | Explicit operator action with target, command class, rollback, and evidence |
| Secrets and private runtime data | Do not read or record values | Stop and use the approved secret/incident process; never expose values |

- Subagents never mutate live clusters. Approved bootstrap or break-glass
  actions remain operator-bound, not delegated background work.
- `kubectl apply/patch/delete`, Helm installation or upgrade, forced Argo CD
  reconciliation, and external secret writes are not default agent actions.
- Never read or record tokens, authentication files, private keys, plaintext
  Kubernetes secrets, shell history, raw transcripts, or environment dumps.
  Secret-bearing scratch needs human-directed handling; do not destroy local
  evidence under a generic cleanup request.
- ExternalSecret reviews use only secret references, mount, and property names,
  never their values. Follow existing isolation and AppProject controls.
- GitHub Actions is repository QA/CI, not live deployment CD. Do not infer
  runtime readiness from a successful static or hosted check.
- Before an exception, record scope, target, responsible operator, rollback or
  backup, and required evidence in the owning Task or incident. Missing
  authority means stop at the local draft.

## Validation and Refresh

Run the affected safety, secret-handling, permission, and policy checks when a
protected surface changes. Report unexecuted external checks using the
[quality result vocabulary](quality.md#result-vocabulary). Never bypass a
failing required check or provider restriction.

## Related Documents

- [Agent Execution](agent-execution.md)
- [Git Policy](git.md)
- [Quality Policy](quality.md)
- [Operations Index](../../05.operations/README.md)
