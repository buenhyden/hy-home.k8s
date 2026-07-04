# Harness Approval Boundaries

This is the single approval-boundary matrix for harness surfaces in
`hy-home.k8s`. It makes the default state, the condition that requires human or
operator approval, the required repo-static validation, where evidence is
recorded, and the rollback path explicit for each surface.

This document is canonical governance. It does not duplicate Stage 00 policy; it
consolidates the live-mutation and protected-surface boundaries that are
otherwise spread across `rules/bootstrap.md`, `rules/agentic.md`, and the
[Local Harness Catalog](../harness-catalog.md) into one decision table.

## Default Stance

- Agents operate on repo-backed desired state. Live cluster mutation is **not**
  part of the default execution path.
- Repo-static validation is the default completion evidence; it never proves
  live ArgoCD, Vault, ESO, or deployment readiness.
- Provider hook/config surfaces are not interchangeable approval gates:
  `.claude/settings.json` owns Claude native permissions, while
  `.agents/hooks.json` and `.codex/hooks.json` provide context/validation
  wiring where supported.

## Approval Matrix

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
| Vault token                                                  | Forbidden                | Never read or record                                                        | n/a                                                                                                                 | n/a                       | n/a                                |
| Secret values                                                | Forbidden                | Never read, commit, or record                                               | `scripts/check-secret-handling.sh .`                                                                                | redacted evidence only    | n/a                                |
| Live cluster                                                 | Read-only by default     | Any mutation needs explicit human/operator approval                         | none (live checks are operator-bound)                                                                               | runbook / incident        | operator-approved recovery         |

## Mandatory Policies

- Live cluster mutation is forbidden by default.
- `kubectl apply` / `kubectl patch` / `kubectl delete` are allowed only on an
  approved bootstrap or emergency path with recorded scope and rollback.
- `helm install` / `helm upgrade` / `helm uninstall` are allowed only on an
  approved bootstrap or recovery path.
- Vault tokens and secret values must never be read or recorded.
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

## Related Documents

- [Harness Implementation Map](../harness-implementation-map.md)
- [Local Harness Catalog](../harness-catalog.md)
- [Bootstrap Governance](bootstrap.md)
- [Harness Task Contract Template](../../99.templates/templates/sdlc/specs/harness-task-contract.template.md)
