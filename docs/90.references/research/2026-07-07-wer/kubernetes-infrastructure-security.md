---
title: 'Reference: Kubernetes Infrastructure Security Research'
type: content/reference
status: draft
owner: platform
updated: 2026-07-10
---

# Reference: Kubernetes Infrastructure Security Research

## Overview

This reference compares the repository's current Kubernetes, GitOps,
infrastructure, secret-management, policy-as-code, network, and software
supply-chain surfaces with primary upstream guidance. It consolidates the
still-valid analysis from the Historical research pack after rechecking every
local claim against the tracked repository on 2026-07-10.

The result is an implementation audit, not an implementation change. It does
not prove that Kubernetes, Argo CD, External Secrets Operator (ESO), Vault, a
network plugin, GitHub Actions, or any external service is live or correctly
enforcing the tracked desired state.

## Purpose

- Map external Kubernetes and GitOps expectations to exact local desired-state
  and validation surfaces.
- Preserve implemented strengths as well as evidence-backed gaps.
- Separate desired state, repo-static results, optional-tool fallbacks,
  operator-run live checks, and enforcement that remains unverified.
- Route each recommendation to one canonical follow-up owner without changing
  an active manifest, script, policy, workflow, or runtime.

## Reference Type

- Type: durable-concept / external-standard-snapshot / dated-implementation-audit
- Source checked: 2026-07-10 for all external and repository sources listed
  below.
- Refresh trigger: Kubernetes, Argo CD, ESO, Vault, OPA, Conftest, NIST,
  SLSA, OpenSSF Scorecard, AppProject, Kustomize, NetworkPolicy, secret,
  bootstrap, infrastructure-test, policy-gate, image, GitHub Actions, or
  supply-chain evidence changes.

## Authority Boundary

- **Authoritative for**:
  - the repo-static observations and source comparison checked on 2026-07-10;
  - the distinction between local desired state, static validation, optional
    fallback, operator-run live checks, and unverified enforcement; and
  - non-mutating recommendations and their follow-up routes.
- **Not authoritative for**:
  - active Kubernetes, GitOps, Argo CD, ESO, Vault, NetworkPolicy, RBAC,
    AppProject, image, policy, CI, or release-gate behavior;
  - live cluster, controller, CNI, Vault, endpoint, secret, ingress/TLS,
    workflow, branch-protection, or artifact readiness;
  - secret values, credentials, bootstrap, sync, rollback, deployment,
    break-glass recovery, policy exceptions, or runtime mutation; or
  - a SLSA level, security certification, or compliance attestation.

Canonical active owners remain the tracked files under `gitops/`,
`infrastructure/`, `policy/`, `scripts/`, `.github/`, and Stage 05 Operations.

## Scope

In scope are Kubernetes Secrets, RBAC, NetworkPolicy, Kustomize, OpenGitOps,
Argo CD Applications/AppProjects/ApplicationSet, ESO with Vault Kubernetes
authentication, Vault policy, OPA/Conftest, repo-static and live test lanes,
image controls, GitHub Actions dependency controls, NIST SP 800-204D, SLSA
v1.2, and OpenSSF Scorecard. Active files and all live or secret-bearing
operations are out of scope.

## Definitions / Facts

### External Security Expectations

- **Kubernetes Secrets**: the official page states that Secrets are stored
  unencrypted in etcd by default and recommends encryption at rest,
  least-privilege RBAC, container-specific access, and consideration of an
  external secret store. A repository ban on plaintext manifests addresses
  only one part of that model.
- **RBAC**: Kubernetes warns that wildcard resources or verbs can silently
  grant future permissions. Exact resources and verbs are the least-privilege
  benchmark. Argo CD AppProject allow-lists are a separate GitOps boundary,
  not a substitute for Kubernetes RBAC.
- **NetworkPolicy**: ingress and egress isolation are independent, and actual
  enforcement depends on a conformant network plugin. An accepted manifest or
  API object does not itself prove packet filtering.
- **Kustomize**: `kubectl kustomize` renders composed resources for review.
  Parsing `kustomization.yaml` and checking sibling references are useful but
  narrower than rendering every root and validating the rendered objects.
- **GitOps and Argo CD**: OpenGitOps defines declarative, versioned and
  immutable, automatically pulled, continuously reconciled desired state.
  Argo CD supports declarative Applications and AppProjects. Its documentation
  warns that a project allowed to deploy into the Argo CD namespace is
  admin-equivalent and requires tightly restricted RBAC and source-repository
  write access.
- **ESO and Vault**: the ESO Vault provider supports Kubernetes auth through a
  `serviceAccountRef`; a cluster-scoped store must name the ServiceAccount
  namespace. The checked rolling `latest` page also states that Vault 1.21+
  roles require an audience. Vault Kubernetes auth validates service-account
  JWTs through TokenReview, and its client-as-reviewer pattern requires
  `system:auth-delegator`.
- **Policy-as-code**: Conftest tests structured configuration with Rego before
  deployment. OPA admission control is a distinct runtime surface that
  evaluates create, update, and delete requests. Passing Conftest or a local
  fallback does not prove admission enforcement.
- **Supply chain**: NIST SP 800-204D covers software supply-chain controls in
  cloud-native DevSecOps CI/CD. SLSA v1.2 separates source/build tracks and
  provenance/verification concepts. OpenSSF Scorecard includes machine-
  checkable controls such as pinned dependencies, token permissions, signed
  releases, and security tooling. These are benchmarks, not proof that this
  repository meets a level or score.

### Current Desired-State Topology

The checked GitOps hierarchy corrects an earlier Current-pack ambiguity:

- `gitops/clusters/local/root-application.yaml` defines `root-platform`, which
  points to `gitops/apps/root` in the `platform` AppProject and declares
  automated prune and self-heal intent.
- `gitops/apps/root/kustomization.yaml` lists 18 platform `Application`
  manifests. It does not own workload generation.
- `gitops/clusters/local/applicationset-apps.yaml` defines `apps-generator`,
  discovers `gitops/workloads/*`, uses the `apps` AppProject, targets only the
  `apps` namespace, and declares automated prune and self-heal intent.
- `gitops/clusters/local/kustomization.yaml` includes the root Application,
  both AppProjects, and the workload ApplicationSet.
- Kustomize files compose the tracked platform/workload desired state; local
  structure checks parse them and require sibling manifests to be referenced.

This is repository desired-state evidence only. No controller pull,
Application generation, sync, health, self-heal, prune, or convergence was
observed in this task.

### AppProject and Authorization Boundaries

- The `apps` AppProject permits one repository and one destination namespace,
  has an empty cluster-resource allow-list, and names exactly eight
  namespaced kinds: Service, Ingress, ExternalSecret, Rollout,
  AnalysisTemplate, PeerAuthentication, VirtualService, and DestinationRule.
  Its local project role grants only `applications get` for `apps/*`.
- The `platform` AppProject enumerates its source repositories, destination
  namespaces, nine cluster-resource kinds, and namespaced kinds rather than
  using wildcard groups or kinds. Its local project role grants only
  `applications get` for `platform/*`.
- The platform destination list includes `argocd`. Per the Argo CD warning,
  this is an intentional high-trust boundary. The tracked allow-lists and
  read-only project role are strengths, but this task did not inspect live
  Argo CD RBAC, remote repository write access, or branch protection.
- ESO's ServiceAccount is bound to `system:auth-delegator`, matching the
  TokenReview requirement. The manifest proves the desired binding, not a live
  authorization decision.

### Secrets and Vault Boundary

The tracked desired-state path is Vault -> ESO `ClusterSecretStore` ->
`ExternalSecret` -> generated Kubernetes Secret. Current strengths are:

- the secret scanner rejects configured plaintext-sensitive key/value patterns
  and `stringData` on its scanned, non-exempt YAML surfaces;
- the Rego policy and built-in fallback categorically reject parsed
  `apiVersion: v1`, `kind: Secret` manifests across the policy gate's YAML
  target set;
- `vault-backend` names the Kubernetes auth mount, `eso-read-platform` role,
  `external-secrets` ServiceAccount, and its namespace;
- `infrastructure/vault/policies/eso-read.hcl` lists only the data and metadata
  paths for three logical platform secrets, with `read` and `list` capability
  and no broad `platform/*` data path; and
- `verify-secrets.sh` is designed to require a Ready store and ExternalSecret
  plus the expected role and ServiceAccount metadata when an approved live
  environment exists.

The boundaries are equally important:

- the repository does not prove etcd encryption-at-rest, namespace Secret
  access, container exposure, live Vault policy attachment, token TTL,
  rotation, seal state, or successful ESO reconciliation;
- the checked `ClusterSecretStore` uses HTTP to reach the in-cluster Vault
  service, so transport confidentiality is not established by the manifest;
- `bootstrap-local.sh` defaults the external Vault HTTPS client to skip
  certificate verification; and
- the bootstrap passes the Vault token in a curl header argument and the
  fetched Valkey password through `kubectl --from-literal`, creating a process-
  argument exposure risk even though values are not written to Git.

The current store does not declare `audiences`. Because the checked ESO page
ties audience requirements to Vault version and no live/version check ran,
compatibility is **Unverified**, not asserted broken.

### NetworkPolicy Boundary

Six egress policies are included by
`gitops/platform/network-policies/kustomization.yaml`. They cover the `apps`,
`platform`, `argocd`, `external-secrets`, `istio-system`, and `monitoring`
use cases with explicit DNS, external-service, API-server, observability, or
pod-CIDR rules. Notable least-privilege strengths include `/32` external
service destinations for PostgreSQL, Vault, Valkey, Prometheus, Grafana,
Tempo, and Loki. The Argo CD policy deliberately permits external HTTPS on
port 443 outside the cluster CIDRs for Git and chart access.

Every local policy is egress-focused. No ingress-isolation conclusion follows
from these files. Static tests check selected object names, CIDRs, and ports;
the live `verify-network-policies.sh` checks object presence and selected
fields, not packet-level allow/deny behavior. CNI conformance and actual
traffic enforcement therefore remain unverified.

### Platform Security Control Matrix

| Control domain | External expectation | Local implementation | Static evidence | Live evidence status | Verdict |
| --- | --- | --- | --- | --- | --- |
| GitOps desired state | Declarative, versioned, automatically pulled, continuously reconciled state. | Root Application owns platform Applications; separate ApplicationSet owns `gitops/workloads/*`; both declare prune/self-heal. | GitOps YAML, Kustomize inventory, structure validator, and static contracts pass. | Pull, generation, reconciliation, sync, health, prune, and self-heal were not checked. | Implemented desired state; runtime Unverified. |
| AppProject boundary | Explicit sources, destinations, roles, and resource permissions; protect admin-equivalent `argocd` destination. | `apps` denies cluster kinds and allows eight exact namespaced kinds; `platform` enumerates wider platform permissions and includes `argocd`. | YAML and wildcard/allow-list static checks pass. | Live Argo CD RBAC, repository write access, and project enforcement were not checked. | Strong repo-static least privilege; high-trust platform boundary Unverified. |
| Kubernetes RBAC | Exact resources/verbs; avoid wildcard growth. | ESO ServiceAccount has the TokenReview `system:auth-delegator` binding; project roles are read-only. | YAML parse, policy, and static contract evidence. | TokenReview and Kubernetes authorization behavior were not checked. | Partial, purpose-specific implementation. |
| Secret storage | Encrypt at rest, minimize RBAC/container access, and consider external stores. | Plaintext manifest ban plus ESO/Vault desired state and bootstrap-only generated Secrets. | Secret scanner and policy gate pass on tracked scanned surfaces. | Etcd encryption, Secret RBAC, container access, sync, and rotation were not checked. | Partial; repo leak prevention is not full Secret security. |
| Vault least privilege | Deny by default; exact paths and capabilities. | Three logical secrets have exact KV-v2 data/metadata paths with read/list only. | HCL and static regex contract pass; no broad data wildcard found. | Policy upload, role mapping, token capabilities, TTL, and audit behavior were not checked. | Implemented sample; live attachment Unverified. |
| ESO/Vault auth | Namespaced ServiceAccount, TokenReview delegation, version-compatible audience. | Store names ServiceAccount/namespace; auth-delegator binding exists; audience absent. | YAML and exact-field static checks pass. | Store readiness, TokenReview, Vault version, audience compatibility, and sync were not checked. | Partial; version-sensitive compatibility Unverified. |
| Secret transport/bootstrap | Verify TLS and keep credentials out of observable command arguments. | External bootstrap uses HTTPS but skips verification by default; in-cluster store uses HTTP; commands expand token/password into argv. | Direct script/manifest inspection. | Network trust, certificate validation, and process visibility were not checked. | Implementation gap. |
| Network isolation | Explicit ingress/egress policy with a conformant CNI and behavioral evidence. | Six egress policies define namespace/use-case allow-lists. | Kustomize, YAML, selected CIDR/port contracts, and kube-linter pass. | CNI enforcement and packet behavior were not checked; live script is structural. | Desired-state strength; enforcement Unverified. |
| Kustomize/schema | Render composition and validate produced resources. | Every tracked Kustomize sibling manifest is referenced and YAML-parseable. | Structure and YAML validators pass. | Full root rendering, API schema, dry-run/admission, and controller acceptance were not checked. | Needs strengthening. |
| Policy-as-code | Test config before deploy; separately enforce admission at runtime when required. | Rego plus built-in Python fallback deny plaintext Secret, namespace auto-create, wildcard AppProject, and `:latest`. | Built-in fallback passes; Conftest is optional. | No admission controller or live admission decision was checked. | Repo-static implementation only. |
| Image controls | Avoid mutable tags and establish artifact integrity/provenance. | Policy denies explicit `:latest`; kube-linter runs locally/pre-commit where installed but config excludes its latest-tag check. | Policy fallback and current local kube-linter pass. | Registry digest, vulnerability, signature, SBOM, provenance, and admission were not checked. | Partial tag hygiene only. |
| Workflow dependency integrity | Pin immutable dependencies and minimize token scope. | Workflows declare scoped permissions and Dependabot updates GitHub Actions weekly; action `uses:` references are tags and Zizmor disables `unpinned-uses`. | Workflow/config inspection and actionlint/Zizmor lanes. | Remote workflow, token, ruleset, and dependency provenance were not checked. | Needs strengthening. |

### Static and Live Evidence Boundary

| Evidence lane | What was checked or exists | What a PASS establishes | What remains outside the claim |
| --- | --- | --- | --- |
| Desired state | AppProjects, root Application, ApplicationSet, Kustomize trees, NetworkPolicies, ESO/Vault manifests, Vault HCL, workflow/config files. | The tracked declaration contains the described intent. | API acceptance, controller behavior, policy enforcement, traffic behavior, secret state, or remote settings. |
| Repo-static deterministic | `validate-repo-quality-gates.sh`, `validate-gitops-structure.sh`, YAML parsing, secret scan, policy gate, static infrastructure contracts, and diff hygiene. | The checked files satisfy the validators' explicit parse, inventory, regex, and policy rules at this revision. | Full Kustomize output, CRD/OpenAPI schema, server dry-run, admission, reconciliation, packet behavior, TLS trust, or secret correctness. |
| Optional tooling | Local kube-linter was available and passed. Conftest was not installed, so the built-in Python policy fallback ran and passed. | Kube-linter's configured checks passed; the fallback's four policy categories passed. | A Conftest pass, excluded kube-linter checks, CI tool availability, or runtime admission enforcement. |
| CI static | `manifest-static` declares five scripts, but installs only PyYAML; a separate pre-commit job can install matching hooks. | When remotely executed, the declared jobs can produce static evidence according to their installed tool set. | No remote run was inspected; the script lane may skip kube-linter and uses fallback when Conftest is absent. |
| Operator-run live | `run-all.sh` calls cluster, GitOps, secrets, external-services, NetworkPolicy, and ingress/TLS scripts. | A separately approved run can establish the scripts' assertions for one environment and time. | These commands were not run here; a prior or future PASS is not permanent readiness. |
| Unverified enforcement | Argo CD convergence, Kubernetes authorization, CNI filtering, OPA admission, Vault policy/role, ESO sync, TLS trust, remote Actions/rulesets, and artifact integrity. | Nothing in this task promotes these surfaces to ready. | Operator/runtime or remote evidence remains required under its canonical policy/runbook. |

Two live-script limitations require explicit reading:

- `verify-gitops.sh` accepts any nonempty Argo CD health string for nine named
  Applications and does not assert `Healthy` or `Synced`.
- `verify-ingress-tls.sh` uses `curl -k`, makes the external Traefik 443 check
  opt-in, and treats Headlamp/Kiali TLS-secret mismatches as warnings. These
  checks can pass without certificate-chain verification or all TLS surfaces
  meeting the documented expectation.

### Supply-Chain Security Analysis

Repository strengths include read-scoped default workflow permissions,
job-specific write permissions, `persist-credentials: false` on checkout in
CI/changelog jobs, weekly Dependabot updates for GitHub Actions, Gitleaks,
detect-secrets, actionlint, Zizmor, and explicit non-`latest` image policy.

The checked tracked workflows do not provide active CodeQL, dependency-review,
SBOM generation, build provenance/attestation, artifact or image signature
verification, signed-release verification, or OpenSSF Scorecard lanes.
GitHub Actions dependencies are referenced by version tags rather than commit
SHAs, and `.github/zizmor.yml` intentionally disables `unpinned-uses`.

NIST SP 800-204D, SLSA v1.2, and OpenSSF Scorecard therefore serve only as a
gap-analysis framework. No SLSA level is claimed or denied: this repository's
current static manifest/document pipeline, changelog artifact, builder trust,
provenance distribution, and verification evidence are insufficient for a
level assessment.

### Security Gap Register

Only the approved classifications `Fact defect`, `Implementation gap`,
`Needs strengthening`, and `Unverified` are used. Severity is part of each
finding; every row has one canonical active-file follow-up route. Implementing
any recommendation requires a separately approved Spec/Plan/Task.

| Finding | Evidence | Risk | Recommendation | Canonical follow-up route |
| --- | --- | --- | --- | --- |
| SEC-001 — Implementation gap (High): specialist CI path coverage | `repo_quality` does not include `infrastructure/bootstrap-local.sh` or Vault HCL; `manifests` includes infrastructure YAML/tests and `policy/**`, but not the bootstrap script or Vault HCL. | A standalone bootstrap or Vault-policy change can receive general pre-commit checks without the specialist repo-quality/manifest-static contract lanes. | Add path-to-gate regression tests, then extend filters only in a separately approved CI change. | [CI workflow](../../../../.github/workflows/ci.yml) |
| SEC-002 — Needs strengthening (Medium): local hook policy depth | Pre-commit runs shell/secret/workflow/manifest tools, but does not directly invoke the custom GitOps structure, policy-gate, or static infrastructure contract bundle. | Local feedback can be green before the specialized repository checks run. | Evaluate a fast, changed-surface wrapper or documented required local bundle with measured latency. | [Pre-commit config](../../../../.pre-commit-config.yaml) |
| SEC-003 — Implementation gap (Medium): optional policy/linter tools in `manifest-static` | The job installs PyYAML only. `validate-k8s-manifests.sh` skips kube-linter when absent; `validate-policy-gates.sh` always runs its built-in fallback and runs Conftest only when installed. | Remote manifest evidence can be weaker than a local/pre-commit run while all scripts still exit successfully. | Install and version explicit tools or make the accepted fallback evidence contract visible in the job summary. | [CI workflow](../../../../.github/workflows/ci.yml) |
| SEC-004 — Needs strengthening (High): Argo CD live-state assertion | `verify-gitops.sh` requires only nonempty health for named apps and does not assert sync status. | `Degraded`, `Progressing`, or out-of-sync state can satisfy the current presence-oriented check. | Add explicit expected health/sync assertions with documented transitional-state handling. | [GitOps live test](../../../../infrastructure/tests/verify-gitops.sh) |
| SEC-005 — Needs strengthening (High): TLS live evidence | `verify-ingress-tls.sh` uses `curl -k`, skips Traefik 443 by default, and warns for Headlamp/Kiali TLS mismatch. | The aggregate live suite can pass without certificate-chain trust or full endpoint coverage. | Define strict and diagnostic modes, verify the intended CA chain, and make required endpoint failures blocking. | [Ingress/TLS live test](../../../../infrastructure/tests/verify-ingress-tls.sh) |
| SEC-006 — Implementation gap (High): Vault bootstrap TLS default | `VAULT_SKIP_VERIFY` defaults to `true`; `vault_curl` then invokes `curl -k`. | A network attacker or misrouted endpoint can evade certificate verification during secret-bearing bootstrap. | Default to verification with an explicit CA bundle and keep any skip as approved, time-bounded break-glass behavior. | [Bootstrap script](../../../../infrastructure/bootstrap-local.sh) |
| SEC-007 — Implementation gap (High): ESO-to-Vault transport | `vault-backend` declares `http://vault-external.platform.svc.cluster.local:8200`. | NetworkPolicy constrains routes but does not provide transport confidentiality or endpoint authentication. | Evaluate Vault TLS with a trusted CA and update the store only after a versioned compatibility test. | [Vault store manifest](../../../../gitops/platform/eso/vault-secret-store.yaml) |
| SEC-008 — Implementation gap (High): secret-bearing process arguments | Bootstrap expands `X-Vault-Token` into curl arguments and the fetched password into `kubectl --from-literal`. | Same-host process inspection or diagnostic capture can expose credentials outside Git. | Use protected files/stdin or another mechanism whose secret value is not present in process argv, then test cleanup and redaction. | [Bootstrap script](../../../../infrastructure/bootstrap-local.sh) |
| SEC-009 — Unverified (High): Vault audience compatibility | The store has no `audiences`; the rolling ESO page says Vault 1.21+ roles require one. Vault/ESO versions and live auth were not checked. | A future or current version combination may warn or fail authentication, but the repository alone cannot establish impact. | Record the deployed version contract and canary an explicit audience before any manifest change. | [Vault store manifest](../../../../gitops/platform/eso/vault-secret-store.yaml) |
| SEC-010 — Unverified (High): NetworkPolicy enforcement | Six egress policies exist, but the live script checks objects/selected fields rather than allow/deny traffic and no CNI test ran. | Desired restrictions may not match effective traffic behavior. | Add approved negative and positive connectivity probes tied to the actual CNI and preserve redacted evidence. | [NetworkPolicy live test](../../../../infrastructure/tests/verify-network-policies.sh) |
| SEC-011 — Needs strengthening (Medium): regex-heavy static contracts | `verify-contracts-static.sh` primarily uses `grep -P`/`grep -Pz`; structure checks parse YAML but do not render every Kustomize root or validate API schemas. | Text presence can pass while object nesting, composition, schema, or admission semantics are wrong. | Layer full Kustomize render and version-matched schema/server-dry-run evidence without removing fast contract checks. | [Static contract test](../../../../infrastructure/tests/verify-contracts-static.sh) |
| SEC-012 — Implementation gap (High): immutable Actions dependencies | All checked `uses:` references are version tags; Zizmor's `unpinned-uses` rule is disabled. | A moved or compromised tag can change executed CI code without a repository diff. | Evaluate full commit-SHA pinning plus automated update metadata and rollback. | [Zizmor config](../../../../.github/zizmor.yml) |
| SEC-013 — Implementation gap (High): supply-chain evidence lanes | No active tracked workflow provides CodeQL, dependency review, SBOM, provenance/attestation, signature verification, or Scorecard. | Source, dependency, artifact, and release integrity have no end-to-end machine-verifiable evidence chain. | Prioritize threat-modelled lanes, define artifact ownership and verification consumers, and assess SLSA only after evidence exists. | [CI workflow](../../../../.github/workflows/ci.yml) |
| SEC-014 — Unverified (High): admin-equivalent Argo CD project boundary | `platform` can deploy to `argocd`; local role is read-only, but live RBAC and remote repository write controls were not inspected. | Compromise of an authorized source or principal could control Argo CD itself. | Require operator evidence for least-privilege Argo CD RBAC and protected source writes at each access-model change. | [Platform AppProject](../../../../gitops/clusters/local/appproject-platform.yaml) |

## Sources

### Repository Sources

- [GitOps README](../../../../gitops/README.md)
- [Infrastructure README](../../../../infrastructure/README.md)
- [Apps AppProject](../../../../gitops/clusters/local/appproject-apps.yaml)
- [Platform AppProject](../../../../gitops/clusters/local/appproject-platform.yaml)
- [Root Application](../../../../gitops/clusters/local/root-application.yaml)
- [Workload ApplicationSet](../../../../gitops/clusters/local/applicationset-apps.yaml)
- [Platform root Kustomize](../../../../gitops/apps/root/kustomization.yaml)
- [NetworkPolicy Kustomize](../../../../gitops/platform/network-policies/kustomization.yaml)
- [Vault store](../../../../gitops/platform/eso/vault-secret-store.yaml)
- [Vault TokenReview binding](../../../../gitops/platform/eso/vault-token-reviewer-binding.yaml)
- [Vault policy sample](../../../../infrastructure/vault/policies/eso-read.hcl)
- [Bootstrap script](../../../../infrastructure/bootstrap-local.sh)
- [Static infrastructure contracts](../../../../infrastructure/tests/verify-contracts-static.sh)
- [Live test aggregate](../../../../infrastructure/tests/run-all.sh)
- [Conftest policy](../../../../policy/conftest/kubernetes.rego)
- [Policy validator](../../../../scripts/validate-policy-gates.sh)
- [Kubernetes manifest validator](../../../../scripts/validate-k8s-manifests.sh)
- [Secret validator](../../../../scripts/check-secret-handling.sh)
- [CI workflow](../../../../.github/workflows/ci.yml)
- [Pre-commit config](../../../../.pre-commit-config.yaml)
- [Kubernetes/GitOps Operations Policy](../../../05.operations/policies/0001-k8s-gitops-operations-policy.md)
- [Platform bootstrap runbook](../../../05.operations/runbooks/0001-argocd-platform-bootstrap-runbook.md)
- [ESO/Vault recovery runbook](../../../05.operations/runbooks/0002-argocd-eso-vault-recovery-runbook.md)

### Primary External Sources

All 15 URLs below were opened and checked read-only on 2026-07-10.

| Source | Claim use | URL |
| --- | --- | --- |
| Kubernetes Secrets | Storage, encryption, RBAC, container access, external-store expectations | <https://kubernetes.io/docs/concepts/configuration/secret/> |
| Kubernetes NetworkPolicy | Independent ingress/egress isolation and CNI enforcement boundary | <https://kubernetes.io/docs/concepts/services-networking/network-policies/> |
| Kubernetes RBAC | Wildcard risk and exact least privilege | <https://kubernetes.io/docs/reference/access-authn-authz/rbac/> |
| Kubernetes Kustomize | Declarative composition and render inspection | <https://kubernetes.io/docs/tasks/manage-kubernetes-objects/kustomization/> |
| OpenGitOps | Four GitOps principles | <https://opengitops.dev/> |
| Argo CD declarative setup | Application/AppProject surfaces, source/destination/role boundary, admin-equivalent namespace warning | <https://argo-cd.readthedocs.io/en/stable/operator-manual/declarative-setup/> |
| Argo CD best practices | Config/source separation and immutable remote-base reference | <https://argo-cd.readthedocs.io/en/stable/user-guide/best_practices/> |
| ESO Vault provider | Kubernetes auth, namespaced ServiceAccount reference, audience caveat | <https://external-secrets.io/latest/provider/hashicorp-vault/> |
| Vault policies | Deny-by-default path/capability model | <https://developer.hashicorp.com/vault/docs/concepts/policies> |
| Vault Kubernetes auth | TokenReview and auth-delegator requirements | <https://developer.hashicorp.com/vault/docs/auth/kubernetes> |
| OPA for Kubernetes | Admission-time enforcement boundary | <https://www.openpolicyagent.org/docs/kubernetes> |
| Conftest | Structured-configuration testing with Rego | <https://www.conftest.dev/> |
| NIST SP 800-204D | Cloud-native CI/CD supply-chain strategies | <https://csrc.nist.gov/pubs/sp/800/204/d/final> |
| SLSA v1.2 | Source/build tracks, levels, provenance, and verification concepts | <https://slsa.dev/spec/v1.2/> |
| OpenSSF Scorecard | Machine-checkable dependency, token, signing, and security-tool checks | <https://scorecard.dev/> |

Source-currentness caveats: both Argo CD URLs use the rolling `stable` route,
so the content may move after the check date. The ESO URL uses rolling
`latest` and displayed version/currentness ambiguity while the checked body
contained the Vault 1.20/1.21 audience note. This reference records the exact
URL and observation date rather than inventing a fixed ESO release. Refresh
those sources when local controller or Vault versions change.

## Review and Freshness

- Last reviewed: 2026-07-10
- Review cadence: on any refresh trigger above or before a security-affecting
  Spec uses these findings.
- Review method: re-open every external URL; diff current repository owners;
  run repo-static gates; record optional-tool availability; keep live/remote
  evidence separate.
- Current limitation: no live Kubernetes, Argo CD, Vault, ESO, CNI, endpoint,
  ingress/TLS, secret-value, credential, remote GitHub, workflow, ruleset,
  artifact, publish, push, merge, or third-party check ran.

## Related Documents

- **Current pack README**: [README.md](README.md)
- **References README**: [../../README.md](../../README.md)
- **Historical security reference**:
  [2026-07-04 Kubernetes Infrastructure Security](../2026-07-04-wer/kubernetes-infrastructure-security.md)
- **Workspace baseline**:
  [workspace-governance-baseline.md](workspace-governance-baseline.md)
- **SDLC/CI/QA reference**:
  [spec-sdlc-ci-qa-formatting.md](spec-sdlc-ci-qa-formatting.md)
- **Automation/QA topology**:
  [automation-pipeline-workflow-qa.md](automation-pipeline-workflow-qa.md)
- **Active Operations Policy**:
  [0001-k8s-gitops-operations-policy.md](../../../05.operations/policies/0001-k8s-gitops-operations-policy.md)
- **Active bootstrap runbook**:
  [0001-argocd-platform-bootstrap-runbook.md](../../../05.operations/runbooks/0001-argocd-platform-bootstrap-runbook.md)
