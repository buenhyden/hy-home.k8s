# AGENTS.md

Agent instructions for `gitops/`. The README is for human readers; these
rules are for AI agents. The repository root gateway (`AGENTS.md` or
`CLAUDE.md`) and `.agents/governance/` still apply.

## Purpose

The Git desired state that Argo CD reconciles for the local k3d platform: cluster bootstrap, AppProjects and ApplicationSets (`clusters/local`), root Applications (`apps/root`), shared platform components (`platform/*`) and workload patterns (`workloads/*`). `platform/external-services` is the source of truth for external service endpoints.

## Responsibilities and Projections

| Work in `gitops/` | Role (`.agents/roles/`) | Skills (`.agents/skills/<id>/SKILL.md`) | Claude | Codex |
| --- | --- | --- | --- | --- |
| Change manifests | [k8s-implementer](../.agents/roles/k8s-implementer.md) | `gitops-workflow`, `deployment-strategies`, `k8s-validate`, `external-service-contract-audit` | `.claude/agents/k8s-implementer.md` | `.codex/agents/k8s-implementer.toml` |
| Review sync, ownership and drift | [gitops-reviewer](../.agents/roles/gitops-reviewer.md) | `gitops-workflow`, `k8s-validate`, `external-service-contract-audit` | `.claude/agents/gitops-reviewer.md` | `.codex/agents/gitops-reviewer.toml` |
| Review ingress, DNS and NetworkPolicy | [network-reviewer](../.agents/roles/network-reviewer.md) | `risk-report` | `.claude/agents/network-reviewer.md` | `.codex/agents/network-reviewer.toml` |
| Review metrics, logs and alerts | [observability-reviewer](../.agents/roles/observability-reviewer.md) | `risk-report` | `.claude/agents/observability-reviewer.md` | `.codex/agents/observability-reviewer.toml` |
| Review RBAC, secrets and isolation | [security-auditor](../.agents/roles/security-auditor.md) | `k8s-security-audit`, `vulnerability-patterns` | `.claude/agents/security-auditor.md` | `.codex/agents/security-auditor.toml` |

Claude reads each skill through `.claude/skills/<id>`. Native loading and
permission limits are in [`.claude/provider.md`](../.claude/provider.md) and
[`.codex/provider.md`](../.codex/provider.md); approval boundaries are in
[approval and safety](../.agents/governance/approval-and-safety.md).

## Rules

1. Change the platform only through this tree, a reviewed pull request and Argo CD reconciliation. Never run `kubectl apply`, `delete`, `patch` or `argocd app sync` against the live cluster; those are bootstrap-only or break-glass and need explicit approval.
2. Never commit a secret value. Reference secrets through ExternalSecret and the Vault/OpenBao store; Vault and ESO own the values.
3. Keep AppProject boundaries, sync waves and namespace ownership consistent with AD-0007 and the accepted ADRs.
4. Change external endpoints only in `platform/external-services/` and keep them consistent with REQ-0004.
5. Static checks are repository evidence; live sync and health need a separate read-only observation.

## Checks

Run the selected checks with `python3 scripts/qa.py staged`, or these
directly:

- `bash scripts/validate-gitops-structure.sh`
- `bash scripts/validate-k8s-manifests.sh .`
- `bash scripts/validate-policy-gates.sh .`
- `python3 scripts/validate-gitops-change-set.py --root . --base-ref HEAD`
- `python3 scripts/validate-vault-eso-contracts.py --root .`
