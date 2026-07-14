---
title: 'Reference: Kubernetes Infrastructure Security Implementation Audit'
type: content/reference
status: draft
owner: platform
updated: 2026-07-05
---

# Reference: Kubernetes Infrastructure Security Implementation Audit

## Overview

This dated audit compares the Kubernetes, Infrastructure, GitOps, policy, and
security benchmark model to current repo-backed implementation evidence in
`hy-home.k8s` as checked on 2026-07-05.

This audit is descriptive reference material. It does not change active
Kubernetes policy, GitOps behavior, Argo CD sync behavior, validation script
semantics, operations runbooks, Vault policy, secret handling, network policy,
or live runtime procedure.

### Purpose

- Record whether the researched Kubernetes, Infrastructure, GitOps, and
  security model is implemented in current repository surfaces.
- Separate declarative desired-state evidence, repo-static validation,
  CI/toolchain evidence, and live-runtime readiness.
- Preserve owner-routed follow-up paths for future hardening without mutating
  manifests, scripts, policy bundles, credentials, or live resources.

## Reference Type

- Type: dated-implementation-audit / external-standard-snapshot
- Source checked: 2026-07-05
- Refresh trigger: Kubernetes, GitOps, Argo CD, Argo Rollouts, AppProject,
  namespace, Kustomize, External Secrets, Vault, RBAC, NetworkPolicy, Traefik,
  OPA/Conftest, kube-linter, image policy, supply-chain, security, or
  live-runtime evidence changes.

## Authority Boundary

- **Authoritative for**:
  - Kubernetes, Infrastructure, GitOps, and security implementation audit
    findings as checked on 2026-07-05.
  - Repo-backed evidence paths used for this dated comparison.
  - Candidate follow-up routes for future specs, plans, tasks, manifests,
    validators, policy bundles, workflows, or operations documents.
- **Not authoritative for**:
  - Active Kubernetes, Argo CD, Argo Rollouts, External Secrets, Vault,
    NetworkPolicy, RBAC, AppProject, image, policy-as-code, or CI enforcement
    semantics.
  - Live k3d, Argo CD, Vault, ESO, Kubernetes, cloud, deployment, endpoint,
    network, ingress, TLS, external gateway, or secret readiness.
  - Secret values, credential changes, Vault writes, cluster mutation, Argo CD
    sync/rollback, bootstrap procedure, break-glass recovery, or third-party
    mutation.

## Scope

- Covers Kubernetes desired-state surfaces, GitOps repository layout, Argo CD
  App-of-Apps/root boundaries, AppProject allow-lists, namespace ownership,
  Kustomize/declarative management, External Secrets Operator and Vault
  boundaries, no-plaintext-secret evidence, RBAC/service-account evidence,
  NetworkPolicy coverage and gaps, ingress/Traefik static routing evidence,
  OPA/Conftest policy-as-code, manifest validation, kube-linter path, static
  infrastructure contracts, supply-chain/image policy, live-runtime readiness
  boundaries, and security automation opportunities.
- Uses the 2026-07-04 research pack as benchmark context and current
  repository files as local implementation evidence.
- Excludes live runtime checks, GitHub remote checks, secret reads, credential
  changes, manifest edits, policy edits, script edits, workflow edits, tool
  installation, cluster mutation, publishing, push, merge, or third-party
  mutation.

## Definitions / Facts

### Benchmark Model

The benchmark model expects Kubernetes and Infrastructure work to be managed as
declarative desired state, versioned in Git, reviewed through scoped changes,
and reconciled by Argo CD only after the repository state is accepted. It also
expects security controls to be expressed through least-privilege AppProject
boundaries, explicit namespace ownership, no plaintext Kubernetes Secret
manifests, External Secrets/Vault separation, NetworkPolicy intent, policy
checks, manifest validation, and static-vs-live evidence separation.

For this repository, implementation status is repo-backed only when a tracked
manifest, README, policy file, script, test, CI workflow, operation policy, or
task record owns the behavior. Static validation can prove file consistency and
desired-state contracts, but it does not prove live Argo CD sync, cluster
health, Vault auth, ESO sync, network enforcement, endpoint reachability, or
secret value correctness.

### Implementation Matrix

| Area | Benchmark expectation | Current implementation | Status | Evidence | Gap or risk | Follow-up route |
| --- | --- | --- | --- | --- | --- | --- |
| Kubernetes desired-state surfaces | Kubernetes resources should be declared in versioned Git surfaces, not mutated directly by default. | `gitops/` owns cluster-local root resources, platform Applications, namespaces, network policies, ESO/Vault interfaces, external service contracts, and the adminer workload pattern. | Implemented | [gitops README](../../../../gitops/README.md), [root Application](../../../../gitops/clusters/local/root-application.yaml), [apps root kustomization](../../../../gitops/apps/root/kustomization.yaml), [workloads README](../../../../gitops/workloads/README.md) | Repo files do not prove live Kubernetes API state or Argo CD reconciliation health. | Route desired-state changes through Stage 03/04, GitOps manifests, GitOps README, and static validation evidence. |
| GitOps repository layout | GitOps state should separate root/bootstrap, platform, workload, and reference implementation concerns. | The layout separates `clusters/local`, `apps/root`, `platform/*`, `workloads/adminer`, and README matrices for service coverage, image/kind policy, AppProject rationale, namespace ownership, external services, and secret responsibilities. | Implemented | [gitops README](../../../../gitops/README.md), [clusters/local](../../../../gitops/clusters/local/), [apps/root](../../../../gitops/apps/root/), [platform](../../../../gitops/platform/), [adminer workload](../../../../gitops/workloads/adminer/) | Layout evidence is static; live controller source paths and health need approved runtime checks. | Keep layout changes in GitOps owners and run GitOps structure plus manifest validation. |
| Argo CD App-of-Apps/root app boundaries | A root app and App-of-Apps pattern should define what Argo CD reconciles without turning agents into live mutators. | `root-application.yaml` points to `gitops/apps/root`; root kustomization declares platform Applications and a cluster config Application; operations policy keeps steady-state changes in Git/PR flow. | Implemented | [root Application](../../../../gitops/clusters/local/root-application.yaml), [apps root kustomization](../../../../gitops/apps/root/kustomization.yaml), [platform-cluster-config app](../../../../gitops/apps/root/platform-cluster-config-app.yaml), [operations policy](../../../05.operations/policies/0001-k8s-gitops-operations-policy.md) | Static source/path checks do not prove the live root Application is Synced/Healthy. | Use repo-static validation for file changes and approved runbooks for live Argo CD evidence. |
| AppProject allow-list boundaries | AppProject source, destination, and kind allow-lists should express least privilege for apps and platform components. | `apps` AppProject has no cluster resources and a narrow namespace kind set; `platform` AppProject carries broader platform/chart boundaries documented in the GitOps README. | Implemented | [apps AppProject](../../../../gitops/clusters/local/appproject-apps.yaml), [platform AppProject](../../../../gitops/clusters/local/appproject-platform.yaml), [GitOps AppProject matrix](../../../../gitops/README.md), [static contracts](../../../../infrastructure/tests/verify-contracts-static.sh) | Static allow-list review does not prove live Argo CD authorization behavior after reconciliation. | Route allow-list changes through GitOps review, static contracts, and live sync evidence when approved. |
| namespace ownership | Steady-state namespace ownership should be explicit and avoid accidental `CreateNamespace=true` drift. | Namespace manifests live under `gitops/platform/namespaces`; static contracts and policy gates reject steady-state `CreateNamespace=true` in GitOps YAML. | Implemented | [namespace kustomization](../../../../gitops/platform/namespaces/kustomization.yaml), [GitOps namespace matrix](../../../../gitops/README.md), [policy validator](../../../../scripts/validate-policy-gates.sh), [static contracts](../../../../infrastructure/tests/verify-contracts-static.sh) | Live namespace existence and labels require runtime checks. | Add new namespace owners under `gitops/platform/namespaces` and validate with GitOps/static gates. |
| Kustomize/declarative management | Kustomize entries should make sibling resources explicit and parseable. | `validate-gitops-structure.sh` validates root/ApplicationSet hierarchy, Kustomize parseability, and sibling manifest resource completeness; the GitOps README keeps layout expectations current. | Implemented | [validate-gitops-structure.sh](../../../../scripts/validate-gitops-structure.sh), [scripts README](../../../../scripts/README.md), [gitops README](../../../../gitops/README.md) | Kustomize structure validation does not prove applied live objects. | Keep resource additions in kustomization files and rerun GitOps structure checks. |
| External Secrets Operator and Vault boundaries | Secret source data should stay outside Git, with ESO/Vault interfaces represented as desired state and live auth handled separately. | `vault-backend`, platform ExternalSecrets, Vault token reviewer binding, and least-privilege Vault policy samples are tracked; no secret values are stored in these files. | Partial | [vault SecretStore](../../../../gitops/platform/eso/vault-secret-store.yaml), [vault token reviewer binding](../../../../gitops/platform/eso/vault-token-reviewer-binding.yaml), [platform ESO kustomization](../../../../gitops/platform/eso/kustomization.yaml), [Vault policy sample](../../../../infrastructure/vault/policies/eso-read.hcl), [secret management matrix](../../../../gitops/README.md) | Repo-static evidence does not prove live Vault auth mount, policy application, ESO controller health, or target Secret sync. | Use Stage 05 policy/runbook owners and approved live checks for Vault/ESO readiness. |
| secret handling and no plaintext secret values | Plaintext Kubernetes Secret manifests and secret values should not be committed or documented. | `check-secret-handling.sh`, `validate-policy-gates.sh`, gitleaks/detect-secrets, operations policies, and GitOps matrices define static no-plaintext-secret evidence. | Implemented | [check-secret-handling.sh](../../../../scripts/check-secret-handling.sh), [validate-policy-gates.sh](../../../../scripts/validate-policy-gates.sh), [pre-commit config](../../../../.pre-commit-config.yaml), [operations policy](../../../05.operations/policies/0001-k8s-gitops-operations-policy.md), [app onboarding policy](../../../05.operations/policies/0007-app-gitops-onboarding-policy.md) | Static scans cannot prove external secret values are correct, rotated, or unavailable elsewhere. | Keep credential work in approved operations/security tasks and record only non-secret evidence. |
| RBAC and service account evidence | Kubernetes RBAC/service-account surfaces should be explicit and reviewed separately from AppProject allow-lists. | ESO token reviewer binding and chart-managed RBAC expectations are represented in GitOps/static contracts; AppProject allow-lists are separately documented as GitOps project boundaries. | Partial | [vault token reviewer binding](../../../../gitops/platform/eso/vault-token-reviewer-binding.yaml), [platform AppProject](../../../../gitops/clusters/local/appproject-platform.yaml), [static contracts](../../../../infrastructure/tests/verify-contracts-static.sh), [Kubernetes research](../../research/2026-07-04-wer/kubernetes-infrastructure-security.md) | Static files do not prove live RBAC authorization behavior or Helm-rendered resource effects after sync. | Add RBAC changes through GitOps review, static tests, and approved live authorization checks when needed. |
| NetworkPolicy coverage and gaps | NetworkPolicy intent should be tracked, with static coverage separated from live network enforcement. | Platform NetworkPolicy manifests cover apps egress, ESO-to-Vault, Argo CD-to-Valkey, Kiali, monitoring, and external service egress; live verification stays in infrastructure tests. | Partial | [network policies](../../../../gitops/platform/network-policies/), [gitops README](../../../../gitops/README.md), [infrastructure README](../../../../infrastructure/README.md), [verify-network-policies.sh](../../../../infrastructure/tests/verify-network-policies.sh) | NetworkPolicy manifests do not prove CNI enforcement or live traffic behavior. | Keep policy changes in `gitops/platform/network-policies` and use approved live network checks for runtime proof. |
| ingress/Traefik/static routing evidence | Ingress and external routing references should be explicit without claiming live gateway readiness. | GitOps owns ingress-nginx and platform UI ingress desired state; `traefik/` stores reference-only external dynamic config for the separate `hy-home.docker` gateway. | Partial | [ingress app](../../../../gitops/apps/root/platform-ingress-nginx-app.yaml), [traefik README](../../../../traefik/README.md), [infrastructure README](../../../../infrastructure/README.md), [verify-ingress-tls.sh](../../../../infrastructure/tests/verify-ingress-tls.sh) | Traefik config files are not Kubernetes desired state and do not prove external gateway runtime readiness. | Route live gateway evidence to approved operations work; keep repo-static route references in Traefik and GitOps owners. |
| policy-as-code with Conftest/OPA | Policy checks should be explicit about repo-static CI/toolchain scope versus live admission control. | `policy/conftest/kubernetes.rego` defines deny rules for plaintext Secrets, `CreateNamespace=true`, wildcard AppProjects, and `:latest` images; `validate-policy-gates.sh` runs Conftest when available plus a built-in fallback. | Implemented | [policy bundle](../../../../policy/conftest/kubernetes.rego), [policy validator](../../../../scripts/validate-policy-gates.sh), [scripts README](../../../../scripts/README.md), [CI workflow](../../../../.github/workflows/ci.yml) | This is not live OPA/Gatekeeper/Kyverno admission control. `policy/README.md` is not present in this checkout. | Route policy changes through `policy/conftest`, scripts, CI path filters, and task evidence. |
| manifest validation and kube-linter path | Manifest validation should include syntax and optional linter evidence with skip semantics explicit. | `validate-k8s-manifests.sh` validates YAML syntax for GitOps/infrastructure/examples/Traefik manifests and runs optional kube-linter when available; `.kube-linter.yaml` exclusions are documented in scripts README. | Implemented | [validate-k8s-manifests.sh](../../../../scripts/validate-k8s-manifests.sh), [.kube-linter.yaml](../../../../.kube-linter.yaml), [scripts README](../../../../scripts/README.md), [CI workflow](../../../../.github/workflows/ci.yml) | Optional kube-linter absence is not kube-linter coverage; it must be reported as a skip/fallback limitation. | Keep exclusion rationale, script behavior, and CI evidence in sync. |
| infrastructure static contract tests | Static infrastructure contracts should verify file-level platform assumptions without live cluster access. | `verify-contracts-static.sh` checks root app contracts, external service ports, ingress/TLS settings, Vault policy least privilege, AppProjects, namespace ownership, Rollouts, notifications, observability, NetworkPolicy, and sample ExternalSecret shape. | Implemented | [static contract test](../../../../infrastructure/tests/verify-contracts-static.sh), [infrastructure README](../../../../infrastructure/README.md), [tests README](../../../../tests/README.md), [CI workflow](../../../../.github/workflows/ci.yml) | Static contracts do not prove live bootstrap, Argo CD sync, endpoint reachability, TLS issuance, or secret sync. | Keep static/live tests separated and record live checks only under approved operations evidence. |
| supply-chain and image policy boundaries | Image and supply-chain controls should be explicit and not overclaim signatures, SBOMs, or provenance where absent. | Repo-quality and policy gates reject active `:latest` images; GitOps README documents active image policy and distinguishes future supply-chain topics. | Partial | [gitops image policy](../../../../gitops/README.md), [policy validator](../../../../scripts/validate-policy-gates.sh), [SDLC/CI/QA audit](sdlc-ci-qa-formatting-automation.md) | The repo does not currently prove image signatures, vulnerability status, SBOMs, SLSA provenance, or artifact attestation. | Route image signing, scanning, SBOM, provenance, or Scorecard gates to future CI/security specs and tasks. |
| live-runtime readiness boundary | The audit should keep live k3d, Argo CD, Vault, ESO, network, and secret readiness outside repo-static claims. | Infrastructure README and tests README separate static contracts from live scripts; operations policies route live evidence to runbooks and approved checks. | Implemented | [infrastructure README](../../../../infrastructure/README.md), [tests README](../../../../tests/README.md), [operations policy](../../../05.operations/policies/0001-k8s-gitops-operations-policy.md), [run-all.sh](../../../../infrastructure/tests/run-all.sh) | Live checks were not run for this audit and cannot be inferred from passing static validation. | Use approved live validation runbooks and record runtime evidence separately from Stage 90 references. |
| security automation opportunities | Repeated security and evidence checks should become deterministic where feasible. | Existing repo-static gates cover many security contracts; gaps remain around audit-matrix validation, optional-tool evidence summaries, live-readiness evidence routing, and supply-chain security gates. | Partial | [scripts README](../../../../scripts/README.md), [CI workflow](../../../../.github/workflows/ci.yml), [Kubernetes research](../../research/2026-07-04-wer/kubernetes-infrastructure-security.md) | New automation can change CI behavior, permissions, runtime expectations, or operator burden. | Propose new security automation through scoped specs/plans/tasks with explicit approval and rollback boundaries. |

### Comparison Analysis

- Kubernetes and Infrastructure implementation is strongest at the GitOps
  desired-state and repo-static validation layers.
- AppProject, namespace, image, secret, policy, and static contract boundaries
  are documented and validated, but they do not prove live Argo CD, Kubernetes,
  Vault, ESO, NetworkPolicy, ingress, TLS, endpoint, or secret readiness.
- Policy-as-code is implemented as repository/CI validation with Conftest or a
  built-in fallback. It is not implemented as live admission control.
- ESO/Vault and no-plaintext-secret boundaries are well represented in tracked
  files, but live Vault policy application, Kubernetes auth, ESO controller
  health, and target Secret sync remain operator-owned live evidence.
- NetworkPolicy and Traefik evidence are intentionally conservative:
  manifests/reference configs show desired intent, while runtime traffic and
  external gateway proof stay outside this audit.
- Supply-chain evidence currently covers explicit image tags and static policy
  checks, not signatures, SBOMs, provenance, or vulnerability gates.

### Automation Opportunities

- Add an audit-matrix validator for required Kubernetes/security rows,
  allowed status values, exact columns, and evidence links.
- Add a GitOps evidence summarizer that reports AppProject allow-lists,
  namespace owners, active workload kinds, image policy state, and kustomize
  completeness in one repo-static output.
- Add a policy evidence summary that records whether Conftest ran or the
  built-in fallback ran, so optional-tool coverage is not overclaimed.
- Add a secret-handling evidence summary that combines gitleaks,
  detect-secrets, static secret handling, and policy-gate outputs without
  printing secret values.
- Add a live-runtime evidence routing checklist that names the approved
  runbook, required operator context, and evidence lane before any live check.
- Add supply-chain hardening proposals for image scanning, SBOM, signature, or
  provenance only through future scoped CI/security tasks.

### Implementation Checklist

- [x] Used the local reference template section model.
- [x] Included the required frontmatter exactly.
- [x] Included the required reference sections.
- [x] Included Benchmark Model, Implementation Matrix, Comparison Analysis,
  Automation Opportunities, Implementation Checklist, and Residual Risks.
- [x] Used the exact implementation matrix columns:
  `Area | Benchmark expectation | Current implementation | Status | Evidence | Gap or risk | Follow-up route`.
- [x] Covered Kubernetes desired state, GitOps layout, Argo CD, AppProject,
  namespace ownership, Kustomize, ESO/Vault, secrets, RBAC, NetworkPolicy,
  Traefik, OPA/Conftest, kube-linter, static contracts, supply-chain/image
  boundaries, live-runtime readiness, and security automation.
- [x] Used only `Implemented`, `Partial`, `Gap`, and `Not in scope` as audit
  status values.
- [x] Used repo-backed evidence only for implementation status claims.
- [x] Kept repo-static and live-runtime evidence lanes separate.
- [ ] Future work: automate matrix row coverage, optional-tool evidence
  summaries, and live-readiness evidence routing if recurring audits need it.

### Residual Risks

- This audit is a 2026-07-05 repository snapshot and can become stale when
  GitOps manifests, infrastructure tests, policies, scripts, operations docs,
  Traefik references, or research benchmark files change.
- Repo-static validation does not prove live k3d, Argo CD, Vault, ESO,
  Kubernetes, cloud, endpoint, NetworkPolicy, ingress/TLS, deployment, secret,
  paid-job, provider-runtime, or external-service readiness.
- Optional local tools such as kube-linter and Conftest may vary by
  environment; task evidence should record actual command output and fallback
  behavior.
- Existing policy-as-code is not live admission control.
- Existing supply-chain checks do not prove image vulnerability status,
  signatures, SBOMs, SLSA provenance, or artifact attestation.
- External Traefik gateway readiness belongs to a separate runtime owner and is
  not proven by reference dynamic config files in this repository.

## Sources

- [Kubernetes Infrastructure Security Research](../../research/2026-07-04-wer/kubernetes-infrastructure-security.md)
- [GitOps README](../../../../gitops/README.md)
- [Infrastructure README](../../../../infrastructure/README.md)
- [Scripts README](../../../../scripts/README.md)
- [Tests README](../../../../tests/README.md)
- [Traefik README](../../../../traefik/README.md)
- [K8s GitOps Platform Operations Policy](../../../05.operations/policies/0001-k8s-gitops-operations-policy.md)
- [App GitOps Onboarding Policy](../../../05.operations/policies/0007-app-gitops-onboarding-policy.md)
- [Policy Bundle](../../../../policy/conftest/kubernetes.rego)
- [Policy Validator](../../../../scripts/validate-policy-gates.sh)
- [GitOps Structure Validator](../../../../scripts/validate-gitops-structure.sh)
- [Kubernetes Manifest Validator](../../../../scripts/validate-k8s-manifests.sh)
- [Secret Handling Validator](../../../../scripts/check-secret-handling.sh)
- [Infrastructure Static Contracts](../../../../infrastructure/tests/verify-contracts-static.sh)
- [Vault ESO Policy Sample](../../../../infrastructure/vault/policies/eso-read.hcl)
- [CI Workflow](../../../../.github/workflows/ci.yml)
- [SDLC CI QA Automation Audit](sdlc-ci-qa-formatting-automation.md)
- [Parent Plan](../../../04.execution/plans/2026-07-05-workspace-engineering-implementation-audit-pack.md)
- [Task Record](../../../04.execution/tasks/2026-07-05-workspace-engineering-implementation-audit-pack.md)

## Review and Freshness

- Review cadence: on source change
- Last reviewed: 2026-07-05
- Next review trigger: Kubernetes, Infrastructure, GitOps, Argo CD,
  AppProject, Kustomize, External Secrets, Vault, secret, RBAC, NetworkPolicy,
  Traefik, OPA, Conftest, kube-linter, supply-chain, security, repo-static,
  live-runtime, research benchmark, audit-index, or status-vocabulary change.
- Refresh this report when repo-static security evidence, desired-state
  manifests, live-runtime boundary language, or supply-chain/image policy
  language changes.

## Related Documents

- **Audit pack README**: [README.md](./README.md)
- **Audits README**: [Parent audits index](../README.md)
- **Parent Plan**: [Workspace Engineering Implementation Audit Pack Plan](../../../04.execution/plans/2026-07-05-workspace-engineering-implementation-audit-pack.md)
- **Task record**: [Workspace Engineering Implementation Audit Pack Task](../../../04.execution/tasks/2026-07-05-workspace-engineering-implementation-audit-pack.md)
- **Kubernetes/infrastructure/security research**: [Kubernetes Infrastructure Security Research](../../research/2026-07-04-wer/kubernetes-infrastructure-security.md)
- **GitOps README**: [GitOps README](../../../../gitops/README.md)
- **Infrastructure README**: [Infrastructure README](../../../../infrastructure/README.md)
- **Reference maintenance runbook**: [Reference Maintenance Runbook](../../../05.operations/runbooks/0011-reference-maintenance-runbook.md)
