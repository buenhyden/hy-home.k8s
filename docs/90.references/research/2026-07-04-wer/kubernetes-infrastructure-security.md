---
title: 'Reference: Kubernetes Infrastructure Security Research'
type: content/reference
status: draft
owner: platform
updated: 2026-07-05
---

# Reference: Kubernetes Infrastructure Security Research

## Overview

This document is a dated Stage 90 reference for Kubernetes, infrastructure,
GitOps, secrets/security, policy-as-code, CI/CD/QA evidence lanes, and
implementation routing in `hy-home.k8s`.

It compares official Kubernetes, Argo, External Secrets Operator, Vault, OPA,
Conftest, NIST, and OpenSSF source material with the repository's current
GitOps and infrastructure evidence. It is descriptive reference material only.
It does not define active policy, live runbook steps, release gates, deployment
approval, Argo CD sync procedure, Vault procedure, or secret handling procedure.

### Purpose

- Preserve a 2026-07-05 source snapshot for Kubernetes and infrastructure
  security concepts used by this repository.
- Compare external best-practice concepts with current repo-backed desired
  state, static validators, and live-runtime evidence boundaries.
- Keep repo-static, CI/toolchain, and live-runtime evidence lanes separate for
  future specs, plans, tasks, audits, and operations docs.
- Provide an implementation checklist and routing map without turning this
  reference into active policy.

## Reference Type

- Type: durable-concept / external-standard-snapshot / dated-implementation-audit
- Source checked: 2026-07-05 for Kubernetes Secrets, Kubernetes
  NetworkPolicies, Kubernetes RBAC, Kubernetes Kustomize/declarative
  management, OpenGitOps, Argo CD docs, Argo CD declarative setup, Argo CD best
  practices, Argo Rollouts, External Secrets Operator, ESO Vault provider, OPA
  Kubernetes admission, Conftest, HashiCorp Vault policies, Vault Kubernetes
  auth, NIST SP 800-204D, and OpenSSF Scorecard.
- Refresh trigger: Kubernetes, Argo CD, Argo Rollouts, External Secrets
  Operator, Vault, OPA, Conftest, NIST, OpenSSF, GitOps manifests,
  infrastructure contracts, NetworkPolicy, RBAC, AppProject, namespace,
  image-policy, secret, policy-gate, CI/toolchain, or live-runtime evidence
  changes.

## Authority Boundary

- **Authoritative for**:
  - Source-attributed reference findings checked on 2026-07-05.
  - Lookup-level mapping between official Kubernetes/infrastructure/security
    concepts and current repo-backed evidence.
  - Evidence-lane separation for repo-static, CI/toolchain, and live-runtime
    claims in this research pack.
  - Checklist-level routing to canonical owners.
- **Not authoritative for**:
  - Active Kubernetes, GitOps, Argo CD, Argo Rollouts, External Secrets
    Operator, Vault, NetworkPolicy, RBAC, AppProject, image, or policy
    enforcement semantics.
  - Live k3d, Argo CD, Vault, ESO, cloud, deployment, network, or secret
    readiness.
  - Secret values, credential changes, Vault writes, cluster mutation, Argo CD
    sync/rollback, bootstrap procedure, or break-glass recovery.
  - CI workflow changes, policy bundle changes, validation-script behavior, or
    tool installation.
  - Market scan conclusions. Market/context scan notes here are
    non-authoritative and cannot override official sources or repo-backed
    canonical owners.

## Scope

- Covers Kubernetes API security concepts, GitOps desired-state management,
  Argo CD, Argo Rollouts, External Secrets Operator, Vault integration,
  NetworkPolicy, RBAC, Kustomize, OPA, Conftest, NIST SP 800-204D, OpenSSF
  Scorecard, repo implementation comparison, static-vs-live evidence lanes,
  CI/CD/QA links, and owner-routed follow-up checklist items.
- Excludes active changes to `gitops/`, `infrastructure/`, `policy/`,
  `scripts/`, `.github/`, operations policies, runbooks, secrets, credentials,
  or live Kubernetes resources.
- Excludes any live runtime validation. Repo-static and CI/toolchain evidence
  do not prove live-runtime readiness.

## Definitions / Facts

### Kubernetes control surfaces

Kubernetes exposes declarative API resources for workloads, networking,
authorization, and configuration. This repository treats those resources as
desired state managed through Git and Argo CD, not as objects for default
agent-side live mutation.

Relevant official concepts:

- **Kubernetes Secret**: a Kubernetes API object intended for sensitive data.
  The official docs also warn that base64 encoding is not encryption and that
  Secrets require deliberate protection. In this repo, plaintext Kubernetes
  `Secret` manifests are not an allowed desired-state pattern.
- **NetworkPolicy**: a Kubernetes resource for controlling pod ingress and
  egress traffic. In this repo, the current NetworkPolicy evidence is mostly
  egress-focused and lives under `gitops/platform/network-policies/`.
- **RBAC**: Kubernetes role-based access control is the API authorization model
  for Roles, ClusterRoles, RoleBindings, and ClusterRoleBindings. This repo
  also uses Argo CD AppProject allow-lists as a GitOps project boundary; that
  is not the same thing as Kubernetes RBAC, but both belong in least-privilege
  review.
- **Kustomize**: Kubernetes declarative management tooling for composing and
  customizing resource manifests. This repo uses `kustomization.yaml` files as
  desired-state entrypoints for GitOps platform and workload resources.

Local evidence:

- `gitops/README.md` defines the GitOps desired-state model, AppProject
  allow-list rationale, namespace ownership, image policy, external service
  contracts, ESO/Vault boundaries, and NetworkPolicy responsibilities.
- `infrastructure/README.md` separates bootstrap assets, static contracts, and
  live verification scripts.
- `scripts/README.md` separates deterministic repo-static validators from
  optional tools and live tests.

### GitOps and Argo CD

OpenGitOps frames GitOps around declarative desired state, versioned and
immutable storage, automated application, and continuous reconciliation. Argo
CD is the current controller family used by this repository to reconcile
declared Git state into the local Kubernetes platform.

Local implementation mapping:

| Concept | Official/source concept | Current repo evidence | Boundary |
| --- | --- | --- | --- |
| GitOps desired state | Git is the source for declared desired state and reconciliation. | `gitops/clusters/local`, `gitops/apps/root`, `gitops/platform`, and `gitops/workloads`. | Desired-state evidence is repo-static until Argo CD live reconciliation is checked. |
| Argo CD declarative setup | Argo CD can be configured declaratively through Kubernetes manifests and app definitions. | Root Application, AppProjects, ApplicationSet, and platform Application manifests under `gitops/`. | This reference does not authorize sync, rollback, or live app mutation. |
| App-of-Apps | Argo CD can manage a tree of Applications. | `gitops/apps/root` owns platform Application declarations. | Structure checks prove file consistency, not live sync health. |
| Argo Rollouts | Progressive delivery controller with Rollout and analysis concepts. | `gitops/apps/root/platform-rollouts-app.yaml` and `gitops/workloads/adminer` Rollout/AnalysisTemplate pattern. | Live rollout health belongs to live-runtime checks and onboarding runbooks. |

### Desired-state surfaces

The repository currently splits desired-state surfaces as follows:

| Surface | Role | Static evidence | Live-runtime evidence boundary |
| --- | --- | --- | --- |
| `gitops/clusters/local` | Argo CD root Application, AppProjects, and workload ApplicationSet. | `validate-gitops-structure.sh`, `verify-contracts-static.sh`, repo-quality gate. | Argo CD Application sync/health and live namespace/project state require approved runtime checks. |
| `gitops/apps/root` | Platform Application declarations and App-of-Apps entrypoint. | GitOps structure and manifest syntax checks. | Live Argo CD reconciliation is not inferred from file checks. |
| `gitops/platform/*` | Platform components, namespaces, ESO, network policies, external service contracts, and config. | Kustomize completeness, manifest syntax, secret handling, policy gates, static contracts. | Runtime readiness requires k3d, Argo CD, ESO, Vault, endpoint, ingress/TLS, and network-policy live tests. |
| `gitops/workloads/adminer` | Reference workload pattern using Argo Rollouts, services, ingress, Istio, and analysis. | Image policy, AppProject kind policy, manifest syntax, secret scan, GitOps structure. | Rollout health, ingress reachability, and pod readiness require live checks. |
| `infrastructure/*` | Bootstrap assets, k3d config, Argo CD values, MetalLB manifests, Vault policy sample, and test scripts. | Static contract script and repo-quality inventory checks. | Bootstrap execution and live test scripts are operator-approved runtime work. |

### AppProject allow-list and RBAC comparison

Kubernetes RBAC and Argo CD AppProject allow-lists address different layers.
RBAC governs Kubernetes API authorization. AppProject allow-lists constrain
which repositories, destinations, and resource kinds Argo CD applications may
use.

Current repo comparison:

| Boundary | Current desired state | Security meaning | Evidence lane |
| --- | --- | --- | --- |
| `apps` AppProject cluster resources | `clusterResourceWhitelist: []`. | App workloads do not own cluster-scoped resources. | repo-static via `gitops/README.md`, AppProject YAML, `verify-contracts-static.sh`, and policy gates. |
| `apps` namespace resources | Active workload kinds plus policy-optional `ExternalSecret`. | Workloads are constrained to the current Rollout/Ingress/Istio/Service pattern and optional ESO secret bridge. | repo-static; live authorization and sync impact require runtime evidence. |
| `platform` AppProject resources | Broader allow-list for platform and chart-managed components. | Platform components require cluster and namespace resources that apps do not own. | repo-static plus manual chart-kind review when allow-lists change. |
| Kubernetes RBAC resources | ESO token reviewer binding and chart-managed RBAC appear in platform surfaces. | RBAC review must consider Kubernetes API least privilege separately from AppProject kind allow-lists. | repo-static for manifests; live authorization behavior requires runtime checks. |

### Namespace ownership

The repo's current namespace ownership model removes steady-state
`CreateNamespace=true` usage and keeps namespaces in explicit desired-state
manifests or bootstrap boundaries.

| Namespace category | Current owner | Evidence | Boundary |
| --- | --- | --- | --- |
| `argocd` | Bootstrap/Argo CD installation boundary. | `gitops/README.md` namespace ownership matrix and `verify-contracts-static.sh`. | Bootstrap execution is not normal agent mutation. |
| `apps` | `gitops/platform/namespaces/namespace-apps.yaml`. | GitOps README, ApplicationSet destination, static contracts. | New app namespaces need owner manifests and policy review. |
| Platform namespaces | `gitops/platform/namespaces/*.yaml`. | GitOps README and Kustomize completeness checks. | Live namespace existence requires cluster validation. |

### Image policy

The current repo-static image policy is intentionally narrower than a full
runtime admission policy. It checks active GitOps images for explicit non-latest
tags or digests and keeps placeholder images only in onboarding examples.

| Surface | Current repo evidence | Not proved by this evidence |
| --- | --- | --- |
| `gitops/workloads/*` | Active workload images must not use `:latest`; current adminer image is pinned. | Image signature, vulnerability status, runtime pull success, or provenance. |
| `gitops/platform/*` | Raw platform pod templates are checked for explicit non-latest tags or digests. | Helm chart sub-image provenance or live deployed image digest. |
| `examples/sample-app/*` | Placeholder images are allowed only as template placeholders. | Production readiness or deployability without replacement. |

Supply-chain follow-up for image signing, vulnerability scanning, SBOMs,
SLSA provenance, or OpenSSF Scorecard gating belongs to a future
CI/toolchain/security task, not this reference.

### Secrets and ESO/Vault boundaries

Kubernetes Secrets, External Secrets Operator, and Vault represent three
different layers:

| Layer | Official concept | Current repo implementation | Boundary |
| --- | --- | --- | --- |
| Kubernetes Secret | In-cluster object for sensitive data. | Plaintext `Secret` manifests are disallowed by policy gates and static scans; target Secrets are expected to be produced by ESO or bootstrap-only approved flows. | This reference does not authorize reading or printing secret values. |
| External Secrets Operator | Controller that syncs external provider data into Kubernetes Secret resources. | `ClusterSecretStore vault-backend` plus platform/app `ExternalSecret` examples. | Repo-static manifests do not prove ESO controller health or successful sync. |
| Vault provider | ESO Vault provider maps ExternalSecret remote refs to Vault paths using provider auth. | Vault Kubernetes auth is represented by `vault-backend` and least-privilege policy samples. | External Vault runtime, auth mount configuration, token reviewer state, and secret rotation are operator-owned live work. |
| Vault policies | Vault policy documents define path capabilities. | `infrastructure/vault/policies/eso-read.hcl` limits ESO reads to approved platform paths and avoids broad wildcard access. | Static policy sample does not prove live Vault policy application. |

Current repo-static checks:

- `scripts/check-secret-handling.sh .` scans GitOps, infrastructure, and
  examples manifests for plaintext secret patterns while allowing
  ExternalSecret-like resources.
- `scripts/validate-policy-gates.sh .` denies plaintext Kubernetes `Secret`
  manifests through Conftest or built-in fallback.
- `infrastructure/tests/verify-contracts-static.sh` checks Vault path and
  external-service naming contracts without reading secret values.

### NetworkPolicy

Kubernetes NetworkPolicy controls traffic for selected pods when supported by
the cluster networking implementation. The current repository records
NetworkPolicy desired state under `gitops/platform/network-policies/` and
keeps live network behavior in `infrastructure/tests/verify-network-policies.sh`.

Current comparison:

| NetworkPolicy surface | Current intent | Static evidence | Live-runtime evidence |
| --- | --- | --- | --- |
| `apps-egress.yaml` | Apps egress to PostgreSQL, DNS, and Istio control plane. | Kustomize completeness, manifest syntax, static contract checks. | Live policy reconciliation and traffic behavior require cluster checks. |
| `external-secrets-egress-to-vault.yaml` | ESO egress to Vault, DNS, and Kubernetes API. | Static contract checks for Vault CIDR/port, DNS, and API server allowance. | Live ESO-to-Vault behavior requires approved ESO/Vault checks. |
| `argocd-egress-to-external-valkey.yaml` | Argo CD egress to external Valkey plus required support routes. | Manifest syntax and policy gate coverage. | Live Valkey connectivity and Argo CD behavior require runtime checks. |
| `monitoring`, `kiali`, and external-services policies | Observability and platform egress boundaries. | Static contract and manifest checks. | Live behavior requires network-policy verification. |

### Policy-as-code

OPA policy and Conftest are used here as repo-static validation concepts. The
active local policy bundle is `policy/conftest/kubernetes.rego`, and
`scripts/validate-policy-gates.sh .` runs Conftest when available or a built-in
Python fallback when Conftest is not installed.

Current local policy categories:

- Deny plaintext Kubernetes `Secret` manifests.
- Deny `CreateNamespace=true` on Argo CD Application and ApplicationSet
  resources.
- Deny wildcard AppProject cluster or namespace resource allow-list entries.
- Deny container and initContainer images ending in `:latest`.

This is repo-static evidence. It is not equivalent to live OPA admission
control, Kubernetes ValidatingAdmissionPolicy, Kyverno, Gatekeeper, or another
cluster admission controller unless a future implementation explicitly adds
that runtime surface and records live evidence.

### Static, CI/toolchain, and live evidence lanes

This repository should keep evidence in three separate lanes:

| Lane | Examples in this repo | PASS means | PASS does not mean |
| --- | --- | --- | --- |
| repo-static | `git diff --check`, `validate-repo-quality-gates.sh`, `validate-gitops-structure.sh`, `validate-k8s-manifests.sh`, `check-secret-handling.sh`, `validate-policy-gates.sh`, `verify-contracts-static.sh`. | Files, docs, manifests, policy bundle, and static contracts satisfy checked repository rules. | Live Kubernetes, Argo CD, Vault, ESO, external service, network, rollout, or secret readiness. |
| CI/toolchain | GitHub Actions lanes and optional local tools such as kube-linter, Conftest, pre-commit, and future security scanners. | The configured toolchain ran or explicitly skipped optional checks according to its contract. | Runtime deployment health, live reconciliation, or secret value correctness. |
| live-runtime | `infrastructure/tests/run-all.sh` and its live children, approved Argo CD/Vault/ESO/k3d checks, and runbook evidence. | The checked runtime environment matched live expectations at the time of the approved check. | Permanent readiness, unrelated environments, or permission to mutate live state. |

### Infrastructure static/live test boundary

`infrastructure/tests/verify-contracts-static.sh` is intentionally static. It
checks files for GitOps source contracts, external service ports, Argo CD
ingress/TLS settings, Vault policy least privilege, AppProject allow-lists,
namespace ownership, Argo Rollouts setup, notification secret wiring,
observability endpoints, ClusterIssuer references, NetworkPolicy CIDRs and
ports, and sample ExternalSecret shape.

The live tests are separate:

- `verify-cluster.sh`
- `verify-gitops.sh`
- `verify-secrets.sh`
- `verify-external-services.sh`
- `verify-network-policies.sh`
- `verify-ingress-tls.sh`
- `run-all.sh`

Those live scripts require a bootstrapped k3d/Argo CD environment, trusted
kubeconfig, external services, and approved runtime context. This reference
does not run them and does not treat static validation as live-runtime proof.

### CI/CD and QA links

Current Kubernetes/infrastructure QA links are descriptive:

| QA topic | Current local owner | Evidence notes |
| --- | --- | --- |
| Repo-wide quality gate | `scripts/validate-repo-quality-gates.sh .` | Covers docs, scripts inventory, GitOps matrices, infrastructure matrices, workflow contracts, generated indexes, and static currentness checks. |
| GitOps structure | `scripts/validate-gitops-structure.sh` | Checks root Application, ApplicationSet, App-of-Apps hierarchy, Kustomize parseability, and resource completeness. |
| Kubernetes manifest syntax | `scripts/validate-k8s-manifests.sh .` | Runs YAML syntax and optional kube-linter when installed. Optional-tool skip is not full kube-linter coverage. |
| Secret handling | `scripts/check-secret-handling.sh .` | Scans manifest roots for plaintext secret patterns and redacts findings. |
| Policy gates | `scripts/validate-policy-gates.sh .` | Runs Conftest or built-in fallback against Kubernetes/GitOps policy categories. |
| Infrastructure static contracts | `infrastructure/tests/verify-contracts-static.sh` | Validates declared contracts only; no live cluster or secret value access. |
| Broader CI/security context | `spec-sdlc-ci-qa-formatting.md` | Describes CI/toolchain, supply-chain, and artifact evidence lanes. |

### NIST and OpenSSF security context

NIST SP 800-204D is relevant because it treats cloud-native DevSecOps CI/CD
pipelines as software supply-chain surfaces. In this repository, that maps to
manifest review, GitOps desired-state validation, policy-as-code checks,
secrets boundaries, and future supply-chain controls such as provenance or
artifact attestations.

OpenSSF Scorecard is useful as a context signal for open source supply-chain
security checks. It is not an active gate in this repository. Any Scorecard
adoption would be a future CI/toolchain proposal with task evidence, not a
policy established by this reference.

### Non-authoritative market/context scan

The non-authoritative market scan for this topic is a landscape map, not a
tool recommendation:

| Area | Common landscape category | Current repo stance |
| --- | --- | --- |
| GitOps controllers | Argo CD, Flux, and related reconciliation tools. | Argo CD is the current local implementation; this reference does not compare or replace it. |
| Progressive delivery | Argo Rollouts, service mesh traffic shifting, and analysis-based rollout gates. | Argo Rollouts is present as a platform component and adminer pattern. |
| External secrets | ESO, CSI drivers, Vault integrations, and cloud secret managers. | ESO plus Vault is the current local desired-state pattern. |
| Policy-as-code | OPA/Conftest, admission controllers, linter policies, and CI rules. | Conftest-style repo-static checks are present; live admission is not claimed. |
| Supply-chain posture | Scorecard, SLSA, dependency scanning, image scanning, SBOM, and signatures. | Some concepts are documented; active enforcement remains future-routed unless present in CI/tooling. |

Market/context scan material is non-authoritative. Official docs, repo-backed
desired state, and canonical operations/governance owners outrank it.

### Repo implementation comparison

| Implementation area | Desired target pattern from sources | Current repo implementation | Evidence lane | Follow-up route |
| --- | --- | --- | --- | --- |
| Desired-state surfaces | Declarative Kubernetes/GitOps state, versioned in Git and reconciled by a controller. | `gitops/` owns Argo CD Applications, AppProjects, ApplicationSet, platform components, namespaces, network policies, and workload pattern. | repo-static until live Argo CD evidence exists. | Stage 03/04 for behavior changes; `gitops/README.md` and GitOps manifests for desired-state changes. |
| AppProject allow-list | Least-privilege project boundaries and explicit allowed sources/destinations/kinds. | `apps` AppProject is tightly scoped; `platform` AppProject is broader for platform/chart resources. | repo-static. | GitOps manifests, app onboarding policy, and static contract tests. |
| Namespace ownership | Explicit namespace lifecycle and no accidental namespace creation by applications. | Steady-state `CreateNamespace=true` is banned; namespaces are owned by bootstrap or `gitops/platform/namespaces`. | repo-static; live namespace existence is live-runtime. | GitOps namespace manifests and bootstrap/runbook owners. |
| Image policy | Avoid ambiguous mutable tags and route image supply-chain checks to CI/tooling. | Active GitOps images must not use `:latest`; sample placeholders are allowed only in examples. | repo-static. | Policy bundle, repo-quality gate, future CI/security tasks. |
| ESO/Vault boundaries | External secret source remains outside Git; cluster target Secrets are generated by controller or approved bootstrap. | `vault-backend`, platform ExternalSecrets, sample app ExternalSecret, and Vault policy sample are present. | repo-static; live ESO/Vault readiness requires runtime checks. | Stage 05 policy/runbook, `gitops/platform/eso`, `infrastructure/vault`, and live-test evidence. |
| NetworkPolicy | Explicit allowed traffic where the cluster network plugin enforces it. | Platform egress policies cover apps, monitoring, ESO-to-Vault, Argo CD-to-Valkey, Kiali, and external services. | repo-static; live traffic behavior is live-runtime. | `gitops/platform/network-policies`, operations policy, and live verification scripts. |
| Infrastructure tests | Static contracts and live tests should not be conflated. | `verify-contracts-static.sh` is static; `run-all.sh` aggregates live tests. | separate repo-static and live-runtime lanes. | `infrastructure/README.md`, tests inventory, and Stage 04 evidence. |
| Policy-as-code | Policy checks can run in CI or admission; scope must be explicit. | OPA/Conftest-style policies run repo-static with fallback. | repo-static / CI-toolchain only. | `policy/conftest`, `scripts/validate-policy-gates.sh`, and future admission-control specs if adopted. |

### Implementation checklist and routing map

- **Stage 00 governance**: Route approval-boundary, live mutation, provider
  runtime, secret-value, and evidence-lane rule changes to
  `docs/00.agent-governance/**`.
- **Stage 03 specs**: Route behavior-changing Kubernetes/GitOps/security
  requirements to the owning spec before changing active implementation
  surfaces.
- **Stage 04 execution**: Record WER-006 evidence, validation output,
  limitations, and no-mutation statements in
  `docs/04.execution/tasks/2026-07-04-workspace-engineering-research-pack.md`.
- **Stage 05 operations**: Route active GitOps policy, bootstrap, recovery,
  live validation, Vault, ESO, NetworkPolicy, Argo CD, and Rollouts procedure
  changes to policies/runbooks.
- **`gitops/`**: Route desired-state changes for AppProjects, Applications,
  namespaces, platform resources, workloads, ExternalSecrets, NetworkPolicies,
  and images to GitOps manifests plus README matrices.
- **`infrastructure/`**: Route bootstrap assets, static contract checks, Vault
  policy samples, k3d config, Argo CD values, and live test inventory changes
  to infrastructure owners.
- **`policy/` and `scripts/`**: Route OPA/Conftest policy categories,
  fallback semantics, manifest validation, secret scanning, and repo-quality
  changes to the owning policy bundle and scripts.
- **CI/toolchain**: Route optional tool promotion, image scanning, Scorecard,
  SLSA provenance/attestation, SBOM, or admission-control work to a scoped
  CI/security task.
- **`docs/90.references`**: Keep this document descriptive, source-checked,
  and freshness-bounded. Do not encode active policy or live runbook procedure
  here.

## Sources

Repo-backed sources:

- [GitOps README](../../../../gitops/README.md)
- [Infrastructure README](../../../../infrastructure/README.md)
- [Conftest Kubernetes Policy](../../../../policy/conftest/kubernetes.rego)
- [Scripts README](../../../../scripts/README.md)
- [K8s GitOps Platform Operations Policy](../../../05.operations/policies/0001-k8s-gitops-operations-policy.md)
- [ArgoCD Platform Bootstrap Runbook](../../../05.operations/runbooks/0001-argocd-platform-bootstrap-runbook.md)
- [Infrastructure Static Contract Test](../../../../infrastructure/tests/verify-contracts-static.sh)
- [Policy Gate Validator](../../../../scripts/validate-policy-gates.sh)
- [GitOps Structure Validator](../../../../scripts/validate-gitops-structure.sh)
- [Kubernetes Manifest Validator](../../../../scripts/validate-k8s-manifests.sh)
- [Secret Handling Validator](../../../../scripts/check-secret-handling.sh)
- [Spec SDLC CI QA Formatting Reference](spec-sdlc-ci-qa-formatting.md)

Official and primary external sources checked on 2026-07-05:

- [Kubernetes Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)
- [Kubernetes NetworkPolicies](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
- [Kubernetes RBAC](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
- [Kubernetes Kustomize / declarative management](https://kubernetes.io/docs/tasks/manage-kubernetes-objects/kustomization/)
- [OpenGitOps](https://opengitops.dev/)
- [Argo CD docs](https://argo-cd.readthedocs.io/en/stable/)
- [Argo CD declarative setup](https://argo-cd.readthedocs.io/en/stable/operator-manual/declarative-setup/)
- [Argo CD best practices](https://argo-cd.readthedocs.io/en/stable/user-guide/best_practices/)
- [Argo Rollouts](https://argo-rollouts.readthedocs.io/en/stable/)
- [External Secrets Operator](https://external-secrets.io/latest/)
- [ESO Vault provider](https://external-secrets.io/latest/provider/hashicorp-vault/)
- [OPA Kubernetes admission](https://www.openpolicyagent.org/docs/kubernetes)
- [Conftest](https://www.conftest.dev/)
- [HashiCorp Vault policies](https://developer.hashicorp.com/vault/docs/concepts/policies)
- [Vault Kubernetes auth](https://developer.hashicorp.com/vault/docs/auth/kubernetes)
- [NIST SP 800-204D](https://csrc.nist.gov/pubs/sp/800/204/d/final)
- [OpenSSF Scorecard](https://scorecard.dev/)

## Review and Freshness

- Review cadence: on source change
- Last reviewed: 2026-07-05
- Next review trigger: Kubernetes, Argo CD, Argo Rollouts, External Secrets
  Operator, Vault, OPA, Conftest, NIST, OpenSSF, GitOps manifest,
  infrastructure contract, policy bundle, NetworkPolicy, RBAC, Kustomize,
  AppProject, namespace ownership, image policy, ESO/Vault, CI/toolchain,
  repo-static, or live-runtime evidence changes.

## Related Documents

- **Pack README**: [Workspace Engineering Research Pack](README.md)
- **Parent research README**: [Research README](../README.md)
- **Parent references README**: [90.references README](../../README.md)
- **Spec**: [Workspace Engineering Research Pack Spec](../../../03.specs/017-workspace-engineering-research-pack/spec.md)
- **Plan**: [Workspace Engineering Research Pack Plan](../../../04.execution/plans/2026-07-04-workspace-engineering-research-pack.md)
- **Task**: [Workspace Engineering Research Pack Task](../../../04.execution/tasks/2026-07-04-workspace-engineering-research-pack.md)
- **Reference template**: [Reference Template](../../../99.templates/templates/common/reference.template.md)
- **Operations policy**: [K8s GitOps Platform Operations Policy](../../../05.operations/policies/0001-k8s-gitops-operations-policy.md)
- **Bootstrap runbook**: [ArgoCD Platform Bootstrap Runbook](../../../05.operations/runbooks/0001-argocd-platform-bootstrap-runbook.md)
