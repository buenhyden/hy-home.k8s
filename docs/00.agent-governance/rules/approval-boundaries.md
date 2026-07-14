---
title: 'Harness Approval Boundaries'
type: governance/reference
status: active
owner: platform
updated: 2026-07-14
---

# Harness Approval Boundaries

## Overview

This is the single approval-boundary matrix for harness surfaces in
`hy-home.k8s`. It makes the default state, the condition that requires human or
operator approval, the required repo-static validation, where evidence is
recorded, and the rollback path explicit for each surface.

This document is canonical governance. It does not duplicate Stage 00 policy; it
consolidates the live-mutation and protected-surface boundaries that are
otherwise spread across `rules/bootstrap.md`, `rules/agentic.md`, and the
[Local Harness Catalog](../harness-catalog.md) into one decision table.

### Default Stance

- Agents operate on repo-backed desired state. Live cluster mutation is **not**
  part of the default execution path.
- Repo-static validation is the default completion evidence; it never proves
  live ArgoCD, Vault, ESO, or deployment readiness.
- Live cluster, Vault, cloud, GitHub publish/merge, and secret value work
  require explicit human/operator approval before any action begins.
- Provider hook/config surfaces are not interchangeable approval gates:
  `.claude/settings.json` owns Claude native permissions, while
  `.codex/hooks.json` provides Codex context/validation wiring and
  `.agents/hooks.json` provides local/Antigravity behavioral wiring where
  supported. The latter is not Gemini CLI native configuration;
  `.gemini/settings.json` is reserved and absent.

## Authority Boundary

### Approval Matrix

| Surface                                                      | Default State            | Approval Required When                                                      | Required Validation                                                                                                 | Evidence Location         | Rollback                           |
| ------------------------------------------------------------ | ------------------------ | --------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- | ------------------------- | ---------------------------------- |
| `gitops/**`                                                  | Editable (desired state) | Never live-synced by agents; ArgoCD sync/rollback is operator-bound         | `scripts/validate-gitops-structure.sh`, `scripts/validate-k8s-manifests.sh .`, `scripts/validate-policy-gates.sh .` | PR / manifest-static CI   | `git revert` desired state         |
| `infrastructure/**` (manifests)                              | Editable                 | Live apply or cluster bring-up needs operator approval                      | `scripts/validate-k8s-manifests.sh .`, `infrastructure/tests/verify-contracts-static.sh`                            | PR / runbook              | `git revert`                       |
| `infrastructure/bootstrap-local.sh`, `infrastructure/k3d/**` | Edit-only                | Running bootstrap against live k3d is operator-bound                        | static review                                                                                                       | runbook record            | re-run approved bootstrap/teardown |
| `infrastructure/vault/**`                                    | Edit-only (policy/path)  | Any live Vault operation or value read                                      | static review (no value read)                                                                                       | runbook (redacted)        | `git revert` policy file           |
| `scripts/**` (validators, hooks, gates)                      | Editable                 | Changing failure semantics of a Tier A gate                                 | `bash scripts/validate-harness.sh`                                                                                  | PR / `memory/progress.md` | `git revert`                       |
| `.github/workflows/**`                                       | Editable                 | Expanding permissions, `pull_request_target`, `write-all`, or branch policy | `scripts/validate-repo-quality-gates.sh .`                                                                          | PR                        | `git revert`                       |
| `docs/00.agent-governance/**`                                | Editable                 | None for docs; changes must not weaken boundaries                           | `scripts/validate-repo-quality-gates.sh .`                                                                          | PR / `memory/progress.md` | `git revert`                       |
| `docs/05.operations/**`                                      | Editable                 | None for docs; live procedure execution is operator-bound                   | `scripts/validate-repo-quality-gates.sh .`                                                                          | PR / runbook              | `git revert`                       |
| `docs/99.templates/**`                                       | Editable                 | None; keep template + README mapping aligned                                | `scripts/validate-repo-quality-gates.sh .`                                                                          | PR                        | `git revert`                       |
| `.env`                                                       | Edit keys only           | Never commit values; key parity with `.env.example`                         | `scripts/validate-repo-quality-gates.sh .`                                                                          | local only                | restore from `.env.example`        |
| `_workspace/**` scratch                                      | Ignored non-secret scratch | Potential secret-bearing artifact appears                                   | Do not inspect values; record only the path class and request human approval before cleanup that could destroy user-local evidence | Task evidence / handoff   | human-directed cleanup             |
| Vault token                                                  | Forbidden                | Never read or record                                                        | n/a                                                                                                                 | n/a                       | n/a                                |
| Secret values                                                | Forbidden                | Never read, commit, or record                                               | `scripts/check-secret-handling.sh .`                                                                                | redacted evidence only    | n/a                                |
| Live cluster                                                 | Read-only by default     | Any mutation needs explicit human/operator approval                         | none (live checks are operator-bound)                                                                               | runbook / incident        | operator-approved recovery         |
| Cloud resources                                              | Read-only by default     | Any cloud API mutation, paid job, publish, or provider refresh              | scoped plan/spec evidence and repo-static checks                                                                    | PR / runbook              | operator-approved recovery         |
| GitHub publish / merge / remote dispatch                     | Local draft only         | Any PR creation, merge, release, publish, workflow dispatch, or remote push | `git diff --check`, `scripts/validate-repo-quality-gates.sh .`, and human review                                    | PR / handoff              | revert / close remote action       |

### Mandatory Policies

- Live cluster mutation is forbidden by default.
- `kubectl apply` / `kubectl patch` / `kubectl delete` are allowed only on an
  approved bootstrap or emergency path with recorded scope and rollback.
- `helm install` / `helm upgrade` / `helm uninstall` are allowed only on an
  approved bootstrap or recovery path.
- Vault tokens and secret values must never be read or recorded.
- Secret value handling remains approval-bound even on emergency paths; agents
  must not display, commit, or record values.
- ExternalSecret changes record only `remoteRef.key`, `property`, mount, and the
  `SecretStore` / `ClusterSecretStore` reference — never values.
- GitHub Actions permission expansion is a protected surface.
- GitHub Actions is provider-agnostic QA/CI, not live deployment CD. Workflow
  changes must not add direct Kubernetes mutation, external Vault mutation,
  container publishing, or commit-push behavior without an explicit governance
  update and approval path.
- AppProject wildcard scopes and `CreateNamespace=true` are forbidden and gated
  by `scripts/validate-policy-gates.sh`.
- Live runtime evidence is separated from repo-static validation and is produced
  only through an approved operations runbook; skipped live checks are reported
  with their reason.

## Governance Context

The bootstrap and Agent-first rules establish GitOps-first execution; this file
is their decision matrix for protected surfaces. Provider-native permission
systems may add stricter controls, but they do not replace this shared approval
route or convert repo-static evidence into live readiness.

## Current Contract

- Repository edits and deterministic local validation are the default agent
  path within the user's stated scope.
- Live mutation, secret-value access, remote publication, merge, and paid or
  third-party state changes require explicit human or operator approval.
- Approved exceptions must record scope, target, rollback, evidence, and the
  responsible operator; absence of approval means stop at a local draft.
- The matrix above is the owner for surface-specific decisions. Runbooks own
  approved operational procedure, and provider settings own native enforcement.

## Validation and Refresh

Run `bash scripts/validate-repo-quality-gates.sh .` and
`bash scripts/validate-policy-gates.sh .` after changing a protected-surface
boundary. Review the matrix whenever a workflow gains permissions, a validator
changes failure semantics, or a new live, secret, cloud, or publication surface
is introduced. Any unverified live condition remains `DEFER` under
[`quality-standards.md`](quality-standards.md).

## Related Documents

- [Harness Implementation Map](../harness-implementation-map.md)
- [Local Harness Catalog](../harness-catalog.md)
- [Bootstrap Governance](bootstrap.md)
- [Canonical Task Approval and Safety Boundaries](../../99.templates/templates/sdlc/execution/task.template.md#approval-and-safety-boundaries)
