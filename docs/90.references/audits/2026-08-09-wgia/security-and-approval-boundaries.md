---
title: 'Audit: Security and Approval Boundaries'
type: content/reference
status: draft
owner: platform
updated: 2026-08-09
---

# Audit: Security and Approval Boundaries

## Overview

This report owns the audit of repository, supply-chain, workflow, agent,
secret, GitOps, infrastructure, permission, destructive-action, remote, and
live approval controls. WGIA-001 records current evidence families without
reading sensitive values; WGIA-008 owns the complete control matrix and review.

## Reference Type

Dated repository-static security and approval audit. It is not a permission
gate, secret store, live security assessment, or approval grant.

## Authority Boundary

Stage 00 approval and security rules, workflow controls, supply-chain locks,
GitOps desired state, policy/configuration files, and validators retain their
current roles. This report cannot authorize a protected action, inspect secret
values, mutate a cluster, or claim enforcement from tracked configuration.

## Scope

Included: static repository trust boundaries, workflows, dependencies, agents,
secret references, GitOps/infrastructure policy, destructive operations, and
hosted/provider/live approval separation. Excluded: credentials, secret values,
provider accounts, remote settings, active exploitation, cluster mutation,
cloud state, and conclusions before WGIA-008 review.

## Definitions / Facts

### Security

Current source families include the Stage 00 approval boundary, Git workflow,
provider notes, `.github/workflows/`, validation dependency locks,
`.gitleaks.toml`, `.secrets.baseline`, GitOps and infrastructure desired state,
policy and secret-reference surfaces, and static security validators. Their
presence is repository-static evidence only.

### Approval-boundary Inventory

| Boundary | Current evidence surface | Foundation rule |
| --- | --- | --- |
| Repository writes | sandbox/user scope plus Stage 00 approval rules | Preserve exact allowed paths and unrelated changes. |
| Workflow/supply chain | `.github/workflows/`; CI lock inputs/artifacts; workflow security validator | Do not infer hosted execution or remote settings. |
| Agent/provider | provider notes, adapters, harness and approval contracts | Tracked declarations do not prove runtime enforcement. |
| Secret handling | `.gitleaks.toml`; `.secrets.baseline`; secret-reference validators | Never read, print, copy, rotate, or write secret values. |
| GitOps/infrastructure | `gitops/`; `infrastructure/`; `policy/`; `secrets/`; `traefik/` | Desired state is not live enforcement. |
| Destructive/remote/live | Stage 00 approval boundary and Task safety section | Require explicit human authority and exact evidence. |

### Finding Convention

Every material finding uses all pack fields and closed audit verdict/depth
values. A blocker includes cause, release condition, and owner. A static control
may be `Partial`, `Gap`, or another reviewed verdict, but never proves hosted,
provider-runtime, credential-bearing, or live enforcement.

#### WGA-SEC-001 — Security source inventory established

- **Request IDs**: security coverage row in the pack index.
- **Scope**: pinned approval, workflow, supply-chain, agent, secret-reference, GitOps, infrastructure, policy, and validator inventory.
- **Expected state**: WGIA-008 can assess every trust boundary against an exact current owner without exposing sensitive data or inferring enforcement.
- **Observed state**: current evidence families are identified; control completeness and effectiveness review remain pending.
- **Evidence**: `docs/00.agent-governance/rules/approval-boundaries.md#approval-matrix`; `.github/workflows/ci.yml#jobs`; `.github/requirements/ci-validation.in`; `.github/requirements/ci-validation.txt`; `.gitleaks.toml#allowlists`; `.secrets.baseline#results`; `gitops/clusters/local/root-application.yaml#kind=Application`; `gitops/platform/eso/vault-secret-store.yaml#kind=ClusterSecretStore`; `infrastructure/k3d/k3d-cluster.yaml#kind=Simple`; `policy/conftest/kubernetes.rego#deny[msg]`; `scripts/validate-github-actions-security.py#main`; `scripts/check-secret-handling.sh#add_scan_root`; `scripts/validate-k8s-manifests.sh#YAML_TARGETS`; `scripts/validate-policy-gates.sh#usage`; `scripts/validate-vault-eso-contracts.py#main`.
- **Evidence depth**: `repository-static`.
- **Verdict**: `Partial`.
- **Impact**: the audit has a bounded source map, but no broad security or approval-effectiveness conclusion is admissible.
- **Disposition**: `Keep`.
- **Canonical owner**: current Stage 00, workflow, supply-chain, GitOps, infrastructure, policy, and security-validation surfaces.
- **Verification**: focused static security/approval validators and WGIA-008 independent security review.
- **Uncertainty**: remote settings, provider enforcement, permissions, credentials, secrets, cluster, cloud, and operator behavior are unobserved.
- **Blocker**: none; protected deeper evidence remains `DEFER` pending separate authority.

## Sources

Source roles are closed to `policy owner`, `machine owner`, `human index`,
`evidence producer`, and `historical snapshot`.

| Source ID | Source role | Evidence at the observation commit | Use |
| --- | --- | --- | --- |
| SRC-WGA-SEC-001 | policy owner | `docs/00.agent-governance/rules/approval-boundaries.md#approval-matrix`; `docs/00.agent-governance/rules/git-workflow.md#rules`; `docs/00.agent-governance/providers/codex.md#permission--hook-boundary` | Protected-action and provider boundaries. |
| SRC-WGA-SEC-002 | machine owner | `.github/workflows/ci.yml#jobs`; `.github/requirements/ci-validation.txt`; `docs/00.agent-governance/contracts/validation-surfaces.json#protectedLevels`; `docs/00.agent-governance/contracts/harness-contract.json#permissionClasses`; `gitops/clusters/local/root-application.yaml#kind=Application`; `gitops/platform/eso/vault-secret-store.yaml#kind=ClusterSecretStore`; `policy/conftest/kubernetes.rego#deny[msg]` | Tracked control intent. |
| SRC-WGA-SEC-003 | evidence producer | `scripts/validate-github-actions-security.py#main`; `scripts/validate-ci-python-contract.py#main`; `scripts/check-secret-handling.sh#add_scan_root`; `scripts/validate-k8s-manifests.sh#YAML_TARGETS`; `scripts/validate-policy-gates.sh#usage`; `scripts/validate-vault-eso-contracts.py#main` | Repository-static evidence. |
| SRC-WGA-SEC-004 | historical snapshot | `docs/90.references/audits/2026-07-11-weia/kubernetes-infrastructure-security.md#actionable-finding-register` | Source-commit-bounded comparison only. |

## Review and Freshness

- Review status: `Pending` for WGIA-008 independent security review.
- Review disposition: `DEFER`; no complete security finding set is approved.
- Evidence observed: 2026-08-09 at the exact observation commit.
- Current-truth owners: Stage 00 approval rules and current workflow,
  supply-chain, GitOps, infrastructure, policy, secret-reference, and validator
  surfaces.
- Refresh triggers: approval, permission, workflow, dependency, agent, secret,
  GitOps, infrastructure, policy, destructive-action, source, observation, or
  verdict change.
- Hosted, provider-runtime, remote, authenticated, credential-bearing, secret-
  value, and live evidence remains `DEFER`.

## Related Documents

- [Pack Index](README.md)
- [Spec 054](../../../03.specs/054-workspace-governance-audit-and-remediation/spec.md)
- [Approval Boundaries](../../../00.agent-governance/rules/approval-boundaries.md)
- [Quality Standards](../../../00.agent-governance/rules/quality-standards.md)
- [Implementation Task](../../../04.execution/tasks/2026-08-09-workspace-governance-audit-and-remediation.md)
