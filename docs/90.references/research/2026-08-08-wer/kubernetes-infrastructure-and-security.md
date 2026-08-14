---
title: 'Reference: Kubernetes, Infrastructure, and Security'
type: content/reference
status: active
owner: platform
updated: 2026-08-10
---

# Reference: Kubernetes, Infrastructure, and Security

## Overview

This reference records a 2026-08-08 repository-static baseline, plus a bounded
2026-08-10 gap-only refresh, for the local k3d platform, its Argo CD GitOps
desired state, and related security controls.
It is a decision input for platform, security, delivery, and operations owners;
it is not a change authorization, live-cluster assessment, or certification.

## Reference Type

Current-primary-source research combined with repository-static platform and
security evidence. The source register is [the pack ledger](source-coverage-and-migration-ledger.md#source-register).

## Authority Boundary

`gitops/` remains the Kubernetes desired-state authority, `infrastructure/`
owns bootstrap and static/live test boundaries, and Stage 05 owners retain
operational authority. A manifest, local policy, or static validator does not
prove an Argo CD sync, Kubernetes admission/CNI enforcement, effective RBAC,
Vault/ESO readiness, secret rotation, CI execution, or an external gateway.
Those remote/live/credential-bearing observations remain `DEFER` unless a
separately approved read-only check collects them without secret values.

## Scope

Included: Kubernetes desired state, GitOps reconciliation, infrastructure
boundaries, network/RBAC/secret/admission controls, rollout and rollback
implications, supply-chain controls, and a workspace-specific gap analysis.

Excluded: direct cluster, Docker, Argo CD, Vault, ESO, CNI, registry, cloud, or
gateway access; kubeconfig and credential inspection; secret-value access; and
any implementation or policy decision. Baseline external pages were checked on
2026-08-08; only the admitted kube-state-metrics, Adminer, and immutable
delivery sources were checked on 2026-08-10. Product version and configuration
applicability remain bounded in the ledger.

## Definitions / Facts

### Evidence-depth model

| Evidence level                     | What this review can establish                                                     | What it cannot establish                                                       | Current result                               |
| ---------------------------------- | ---------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ | -------------------------------------------- |
| Repository desired state           | Tracked YAML, scripts, policies, and documentation contain the stated declaration. | Rendering success, controller use, access authorization, or live effect.       | Verified where paths are cited.              |
| Static/render validation           | A named local validator accepts a stated repository input.                         | Hosted CI execution, admission, controller reconciliation, or workload health. | Verified only when the named command is run. |
| Hosted CI                          | A remote workflow ran a revision and reported a result.                            | Deployment, cluster health, registry state, or production safety.              | DEFER.                                       |
| Remote GitOps                      | Argo CD fetched, rendered, synchronized, and reported revision/health.             | API admission, CNI behavior, application availability, or secret correctness.  | DEFER.                                       |
| Live Kubernetes and secret backend | API-server/CNI/RBAC/controller/Vault/ESO conditions and controlled outcomes.       | Broader security conformance or future availability.                           | DEFER.                                       |
| External gateway and cloud         | Gateway configuration, TLS, endpoint, cloud IAM, and provider health.              | GitOps desired-state correctness by itself.                                    | DEFER.                                       |

The statuses deliberately describe evidence depth, not control quality. A
`Verified` repository declaration cannot promote a deeper row to `Verified`.

### Layered platform model and trust boundaries

The intended reconciliation path is:

`reviewed Git revision` -> `Argo CD root Application and AppProject` ->
`Application/ApplicationSet render of GitOps paths` -> `Kubernetes API
authentication, authorization, and admission` -> `controllers and CNI` ->
`live resources, Pods, endpoints, and conditions`.

`gitops/clusters/local/root-application.yaml` declares the root Application
against `main` with automated prune and self-heal. The apps ApplicationSet also
declares `main`, an `apps` destination, and automated prune/self-heal.
`appproject-apps.yaml` declares an empty `clusterResourceWhitelist: []`, so no
cluster-scoped resource is permitted, while the platform
project enumerates allowed sources, destinations, and resource kinds. This is
repository evidence of intended source and scope boundaries, not proof of
repository authorization, a rendered Application, or effective Argo/Kubernetes
RBAC.

Argo CD documents that automated sync acts on a Git-versus-live difference;
`prune` and `selfHeal` are explicit settings, and an Application with automated
sync enabled cannot use Argo CD rollback. The operational implication here is
an evidence-backed, Git-revert-first recovery path rather than an inferred
live rollback capability. [SRC-WERPC-027](source-coverage-and-migration-ledger.md#source-register)
also treats App-of-Apps source write access as an administrative trust boundary.

The intended secret path is:

`external Vault KV path and role/policy` -> `Kubernetes TokenReview-based
Vault auth` -> `ESO ClusterSecretStore` -> `ExternalSecret reconciliation` ->
`Kubernetes Secret metadata/value` -> `Argo CD or workload consumer`.

`gitops/platform/eso/vault-secret-store.yaml` declares Vault Kubernetes auth
for the `external-secrets` ServiceAccount with audience `vault`; the matching
TokenReview binding and a six-path `eso-read` Vault policy are tracked. The
Store also marks its HTTP service endpoint as a local-only exception. The
repository contains no secret values in this review. Vault auth, TokenReview,
role/audience alignment, transport, Store/ExternalSecret conditions, generated
Secret values, rotation, and consumer reload therefore remain `DEFER`.

`traefik/` is a reference-only copy for an external `hy-home.docker` gateway,
not an Argo-managed Kubernetes deployment path. Its local endpoint and TLS
claims must not be used as evidence that a gateway is running or that an
external service is healthy.

### Kubernetes baseline

Kubernetes NetworkPolicy is meaningful only when the selected networking
implementation enforces it; isolation behavior follows the policies selecting a
Pod. [SRC-WERPC-023](source-coverage-and-migration-ledger.md#source-register)
is the upstream basis for that boundary. The repository has six egress-focused
policies under `gitops/platform/network-policies/`, covering apps, platform
external services, ESO-to-Vault, Argo CD-to-Valkey, monitoring, and Kiali.
Checked 2026-08-10, all six declare `policyTypes: [Egress]` only, and the
tracked paths `gitops/`, `infrastructure/`, and `policy/` contain no
Ingress-type and no default-deny NetworkPolicy. That is a repository-static
absence observation about tracked manifests; it does not describe cluster
state.
`infrastructure/tests/verify-network-policies.sh` is explicitly a live test.
Thus manifest intent is `Verified`; CNI capability and selected allow/deny
flows are `DEFER`.

The checked tree has explicit ESO TokenReview and monitoring RBAC resources,
plus AppProject allow-lists. It does not establish a complete least-privilege
inventory, effective aggregated permissions, or periodic review. Kubernetes
RBAC and admission behavior are runtime API-server concerns, not properties of
the YAML alone.

The two inspected monitoring workloads (`alloy-k8s-logs` and
`kube-state-metrics`) declare non-root execution, no privilege escalation,
dropped capabilities, read-only root filesystems, resource settings, and probe
configuration. They are examples, not a tree-wide workload-hardening policy or
runtime evidence.

### Infrastructure baseline

`infrastructure/README.md` separates `verify-contracts-static.sh` from
cluster-dependent checks such as `verify-cluster.sh`, `verify-gitops.sh`,
`verify-network-policies.sh`, `verify-secrets.sh`, and `run-all.sh`. The static
boundary is therefore `Verified`; the existence, TLS trust, k3d state, Docker
state, endpoint reachability, and results of the live scripts are `DEFER`.

The root Application and platform Application declarations provide a versioned
desired-state topology, but track a branch (`main`) rather than an immutable
commit. This is an observation for change-control and recovery design, not a
finding that the selected revision was fetched or reconciled.

### Security baseline

`policy/conftest/kubernetes.rego` denies plaintext `Secret` manifests,
`CreateNamespace=true`, AppProject wildcard groups/kinds, and `:latest` image
tags. `scripts/check-secret-handling.sh` and the static manifest validators are
pre-merge controls when invoked; they are not Kubernetes admission controls.
The checked paths contain no tracked Pod Security Admission labels,
ValidatingAdmissionPolicy/MutatingAdmissionPolicy resources, Gatekeeper
installation, ConstraintTemplate, or Constraint. This is a bounded tracked-path
absence observation, not a claim about an uninspected cluster configuration.

Kubernetes documents Pod Security Admission as namespace-scoped enforcement,
audit, and warning of Pod Security Standards. API admission can validate or
mutate API writes. Gatekeeper, separately, is an OPA-backed validating/mutating
webhook with audit capability. These are runtime or API-boundary mechanisms;
they complement rather than replace repository linting. [SRC-WERPC-025](source-coverage-and-migration-ledger.md#source-register),
[SRC-WERPC-026](source-coverage-and-migration-ledger.md#source-register), and
[SRC-WERPC-028](source-coverage-and-migration-ledger.md#source-register) define
the source boundary.

Kubernetes documents Secrets as base64-encoded and unencrypted in etcd by
default. No cluster encryption configuration, effective Secret RBAC, or
generated Secret metadata/value was inspected here. [SRC-WERPC-024](source-coverage-and-migration-ledger.md#source-register)
is a platform benchmark, not evidence of the local setting.

### 2026-08-10 gap-only Kubernetes/Security refresh

This refresh admits only three question-level deltas left under-sourced by the
baseline. The proposed targets are decision inputs, not manifest changes. The
Namespace ingress/default-deny candidate was rejected as a duplicate: the
existing [Kubernetes baseline](#kubernetes-baseline) and
[SRC-WERPC-023](source-coverage-and-migration-ledger.md#source-register) already
own the CNI dependency, selected-policy semantics, static directory evidence,
and live-flow `DEFER` boundary.

#### kube-state-metrics Secret collection boundary

The v2.14.0 upstream deployment example grants cluster-wide `list` and `watch`
for Secrets, and its documented Secret collector emits `kube_secret_*` object
metadata/status families without Secret values. The same product supports an
explicit resource allow-list and namespace restriction. Kubernetes
authorization remains the stronger boundary: an API client authorized to
`get`, `list`, or `watch` Secrets can receive the Secret objects, and Secret
`list` output includes their data. Metadata-only exported metrics therefore do
not make the underlying API permission metadata-only.
[SRC-WERPC-060](source-coverage-and-migration-ledger.md#source-register) and
[SRC-WERPC-061](source-coverage-and-migration-ledger.md#source-register) bound
this distinction.

The checked `ClusterRole/kube-state-metrics` includes `secrets` with
`verbs: [list, watch]`; `Deployment/kube-state-metrics` uses the dedicated
ServiceAccount, image `registry.k8s.io/kube-state-metrics/kube-state-metrics:v2.14.0`,
and no container arguments. This is static evidence for the broad declared
collector/RBAC shape, not effective authorization, actual metric exposure, or
a consumer requirement. Before changing it, inventory consumers of
`kube_secret_*`. If none exist, the least-privilege target is an explicit
resource allow-list that excludes Secrets plus removal of the Secret RBAC
rule. If only selected namespaces need the collector, evaluate upstream
namespace restriction with namespaced Roles/RoleBindings rather than infer
that the standard ClusterRole is necessary. [CLM-WERPC-008-01](source-coverage-and-migration-ledger.md#werg-003-gap-only-claim-register)
and [CLM-WERPC-008-02](source-coverage-and-migration-ledger.md#werg-003-gap-only-claim-register)
record the evidence and decision gate.

#### Adminer workload and service-account boundary

`Rollout/adminer` declares neither `serviceAccountName` nor
`automountServiceAccountToken`, so Kubernetes' documented defaults assign the
namespace's `default` ServiceAccount and make API credentials available unless
automounting is disabled. The Rollout also has no pod or container
`securityContext`; `.kube-linter.yaml` explicitly excludes the non-root and
read-only-root-filesystem checks. These are exact tracked-field observations,
not evidence that Adminer calls the Kubernetes API, runs as root, violates an
active Pod Security policy, or can run unchanged under every hardening field.

The target is a dedicated ServiceAccount with no workload-specific
RoleBinding or ClusterRoleBinding in tracked manifests and pod-level
`automountServiceAccountToken: false`, plus a compatibility-tested Restricted
Pod Security posture: non-root UID/GID, `seccompProfile.type: RuntimeDefault`,
no privilege escalation or privileged mode, all capabilities dropped, and a
read-only root filesystem only if the image's writable paths support it. If a
future API need is demonstrated, grant only the required RBAC and use a bounded
projected token instead of re-enabling the default automatic credential mount.
Image UID,
writable paths, readiness, canary behavior, API need, admission, and runtime
remain `DEFER`; effective authorization also remains `DEFER` because group
bindings, discovery access, and external authorization were not observed.
[SRC-WERPC-062](source-coverage-and-migration-ledger.md#source-register),
[CLM-WERPC-008-03](source-coverage-and-migration-ledger.md#werg-003-gap-only-claim-register),
and [CLM-WERPC-008-04](source-coverage-and-migration-ledger.md#werg-003-gap-only-claim-register)
own this boundary.

#### Immutable identity and verifiable supply-chain evidence

The repository uses `main` for `Application/root-platform`, for both Git
revision fields in `ApplicationSet/apps-generator`, and for the ten Git-sourced
Applications under `gitops/apps/root/` (checked 2026-08-10). Those values follow a
moving branch tip; an exact Git commit SHA is the immutable Git content
identity. Several Helm Applications use exact chart versions, but
`infrastructure/bootstrap-local.sh` installs `argo/argo-cd` after a repository
index update without `--version`. Exact chart selection is not Helm provenance:
a `.prov` file plus a trusted PGP key verifies the packaged chart checksum and
origin. Argo CD renders Helm with `helm template`; its Git signature verification
does not verify Helm chart or OCI signatures. The current Argo CD stable
documentation labels the newer `sourceIntegrity` facility as version 3.5, so
the repository's unpinned bootstrap leaves compatibility `DEFER`.
[SRC-WERPC-063](source-coverage-and-migration-ledger.md#source-register) and
[SRC-WERPC-064](source-coverage-and-migration-ledger.md#source-register) are the
direct product sources.

Tracked Adminer, kube-state-metrics, and Alloy image references use tags with
no digest. A Kubernetes `@sha256:` digest fixes image bytes; it does not prove
who signed or built them. A signature binds an asserted signer identity to an
artifact digest. An attestation is a signed statement about an artifact, and
SLSA provenance is a specific statement about how, where, and from which source
an artifact was produced. Each still requires a trusted root, identity/builder
expectations, artifact-digest match, and fail-closed verification policy;
GitHub explicitly does not present an attestation as a security guarantee by
itself. No Git signature enforcement, Helm `.prov`, image digest, Cosign
signature, attestation, SLSA provenance, verification policy, or admission
result was observed. [SRC-WERPC-065](source-coverage-and-migration-ledger.md#source-register),
[CLM-WERPC-008-05](source-coverage-and-migration-ledger.md#werg-003-gap-only-claim-register),
and [CLM-WERPC-008-06](source-coverage-and-migration-ledger.md#werg-003-gap-only-claim-register)
preserve these non-equivalences.

| Delta                    | Exact repository selector                                                                                                                                                                     | As-Is                                                                                                                  | Gap / decision input                                                                               | Target acceptance evidence                                                                                                                                                                                              |
| ------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Secret collector/RBAC    | `gitops/platform/monitoring/kube-state-metrics.yaml`: `ClusterRole/kube-state-metrics rules[apiGroups=[""]]` containing `resources: secrets`, `verbs: [list, watch]`; container has no `args` | Cluster-wide Secret object read stream is declared for the v2.14.0 collector.                                          | Whether any `kube_secret_*` metric consumer justifies it is unobserved.                            | Consumer inventory, approved minimum resource/namespace scope, static manifest validation, then separately authorized effective-RBAC and scrape evidence without values.                                                |
| Adminer token/hardening  | `gitops/workloads/adminer/rollout.yaml`: `Rollout/adminer spec.template.spec` lacks `serviceAccountName`, `automountServiceAccountToken`, and pod/container `securityContext`                 | Kubernetes defaults and workload fields leave token and hardening intent implicit.                                     | API need and image compatibility are unknown; linter exemptions do not establish safety.           | Approved ServiceAccount/RBAC decision, token-disabled manifest, image compatibility test, restricted-field static checks, and separately authorized admission/runtime evidence.                                         |
| Git/chart/image identity | `gitops/clusters/local/root-application.yaml`, `gitops/clusters/local/applicationset-apps.yaml`, `gitops/apps/root/`, `infrastructure/bootstrap-local.sh`, Adminer/KSM/Alloy image fields     | Git sources track `main`; chart applications mix exact versions with an unpinned bootstrap chart; images are tag-only. | Identity, authenticity, build provenance, and policy enforcement are separate unproven properties. | Environment-specific immutable-ref policy, full Git SHA where required, pinned bootstrap chart, image `tag@digest`, and independently configured/verified provenance or signatures against explicit trust expectations. |

### Threat, control, and evidence matrix

| Scope / threat                                        | Existing preventive or detective control                                                   | Local evidence                                                                                                      | Missing deeper evidence / status                                                                                                                | Next owner                                   |
| ----------------------------------------------------- | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------- |
| Unauthorized desired-state expansion                  | AppProject source/destination/resource allow-lists; Git-reviewed root/AppSet declarations. | Root Application, AppProjects, ApplicationSet, GitOps structure validator.                                          | Repository access policy, Argo project enforcement, rendered apps, sync/health: DEFER.                                                          | Platform + security.                         |
| Unauthorized API write or unsafe Pod                  | Conftest checks; selected workload security contexts.                                      | `policy/conftest/kubernetes.rego`; two monitoring manifests.                                                        | PSA labels/config, native admission policies/Gatekeeper, API-server enablement, rejection/audit outcomes: DEFER.                                | Security architect + platform.               |
| Lateral/egress access                                 | Six egress NetworkPolicies.                                                                | `gitops/platform/network-policies/`; live verifier exists.                                                          | CNI support, namespace default-deny posture, effective rules, permitted/denied traffic tests: DEFER.                                            | Platform + security.                         |
| Excess privilege                                      | Selected ClusterRoleBindings and AppProject scope restrictions.                            | ESO TokenReview binding, monitoring RBAC, Conftest wildcard-AppProject rule.                                        | Service-account/RBAC inventory, wildcard verbs/resources review, effective/aggregated roles: DEFER.                                             | Platform + security.                         |
| Secret-object exposure through metrics collector      | kube-state-metrics has a dedicated ServiceAccount and explicit ClusterRole.                | Its ClusterRole grants cluster-wide Secret `list/watch`; the v2.14.0 container has no resource/namespace arguments. | Metric consumer need, effective authorization, actual exported metrics, and Secret-object access outcome: DEFER.                                | Monitoring + platform/security.              |
| Default workload API token or weak container boundary | Resource limits/probes exist for Adminer; general static policies exist.                   | Adminer lacks explicit ServiceAccount/token and security-context fields; related kube-linter checks are excluded.   | API need, image UID/write compatibility, admission and runtime posture: DEFER.                                                                  | Workload + platform/security.                |
| Secret disclosure or stale secret                     | No plaintext Secret policy; Vault/ESO shape and local-only HTTP annotation.                | Store, TokenReview binding, Vault policy, secret-handling validator.                                                | etcd encryption, Vault seal/TLS/auth/role policy, ESO readiness, Secret readers/rotation/reload: DEFER.                                         | External-Vault operator + platform/security. |
| Image tampering / mutable supply chain                | `:latest` prohibition and CI/static workflows.                                             | Rego rule; moving Git refs, tag-only images, exact/floating Helm identities, and bootstrap script.                  | Immutable Git/image/chart identities, trusted signature/provenance expectations, verification/admission, and registry artifact evidence: DEFER. | Delivery + security.                         |
| Destructive or failed deployment                      | Argo automated sync, prune/self-heal declaration and recovery runbooks.                    | Root/ApplicationSet YAML; Argo/Vault recovery runbooks.                                                             | Sync history, health, retry, prune effect, recovery exercise, Git revert evidence: DEFER.                                                       | Platform operations.                         |
| Gateway or cloud boundary drift                       | Reference-only Traefik documentation and explicit static/live split.                       | `traefik/README.md`; infrastructure inventory.                                                                      | External gateway config/load, TLS, endpoint, cloud IAM/provider health: DEFER.                                                                  | External gateway operator + platform.        |

### Policy, reconciliation, rollout, and rollback design implications

Static Conftest, shell, Python, YAML, and optional kube-linter checks prevent
some repository regressions before merge. PSA, native admission policies,
Gatekeeper, and CNI policy enforcement apply only if configured at the API or
network boundary. Static and runtime controls should be layered: neither proves
the other, and neither replaces observability or a tested recovery procedure.

The practical follow-up is to choose an admission architecture only after a
version-compatible, human-approved design decision: namespace PSA labels for a
baseline/restricted posture, then native CEL policies or Gatekeeper for custom
rules as appropriate. Start with audit/warn, exemptions, negative fixtures,
and a rollback path; do not describe this target as implemented.

Argo auto-sync with self-heal makes direct live drift non-durable. With prune
enabled, deletion-sensitive changes require review and recovery planning. A
canonical Git-revert-first runbook should make impact review, reconciliation,
and observed sync/health evidence explicit; any break-glass exception remains
operator-approved. This is an analysis of documented semantics and repository
intent, not a completed recovery test.

The current non-`latest` rule is tag hygiene, not immutable digest pinning or
artifact authenticity. SLSA v1.2 and NIST SSDF are useful benchmarks for a
future supply-chain mapping, but no SLSA level, SSDF conformance, SBOM,
provenance, attestation, or signature verification was observed. [SRC-WERPC-032](source-coverage-and-migration-ledger.md#source-register)
and [SRC-WERPC-034](source-coverage-and-migration-ledger.md#source-register)
must not be converted into implementation claims.

### Workspace As-Is, gap, and target matrix

| Priority | As-Is / bounded gap                                                                                                                                      | Target acceptance evidence                                                                                                                 | Owner and scope boundary                                    |
| -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------- |
| High     | NetworkPolicy manifests do not prove CNI enforcement or a default-deny posture.                                                                          | Approved read-only CNI/version observation and controlled allowed/denied-flow evidence; a documented default-deny decision and exceptions. | Platform + security; live check required.                   |
| High     | No tracked PSA/admission/Gatekeeper artifacts were found; static Rego cannot reject an out-of-band API write.                                            | ADR-backed admission choice, audit-first rollout, exemptions, negative fixtures, rollback procedure, and approved live admission evidence. | Security architect + platform; no implementation implied.   |
| High     | Vault/ESO shape does not prove encryption at rest, Secret RBAC, authentication health, rotation, or consumer reload. Local HTTP is expressly local-only. | Accepted local threat model; approved audit of readers/encryption; TLS/CA outside local scope; readiness/rotation evidence without values. | Vault operator + platform/security; secret values excluded. |
| Medium   | AppProject allow-lists do not replace Kubernetes least-privilege RBAC.                                                                                   | Service-account/RBAC inventory, justified scope, rendered-resource review, and focused wildcard/privilege validation.                      | Platform + security.                                        |
| Medium   | Non-`latest` does not make images immutable or authenticated.                                                                                            | Digest pinning, SBOM/provenance production, attestation/signature verification after a compatible design decision.                         | Delivery + security.                                        |
| Medium   | Auto-sync/prune/self-heal affects recovery; direct Argo rollback is not an ordinary path with auto-sync enabled.                                         | Git-revert-first runbook, destructive-prune review, observed sync/health, and approved emergency exception.                                | Platform operations; live exercise required.                |
| Medium   | Hardened contexts appear on selected workloads only.                                                                                                     | Compatible baseline template/policy, resource and privilege controls, audit/warn before enforcement.                                       | Workload/platform + security.                               |
| Low      | External Traefik reference copies can drift from the actual gateway.                                                                                     | Retain reference-only label and add an approved external-gateway evidence procedure, or retire stale copies.                               | External gateway operator + platform.                       |

### Required deferred-validation backlog

- Read-only API-server/version/admission configuration, namespace PSA labels,
  effective Roles/ClusterRoles/bindings, and Secret encryption configuration
  under operator authority.
- Read-only Argo CD Application/ApplicationSet revision, sync, health, and
  operation history plus repository/controller reachability.
- CNI identity/capability and controlled NetworkPolicy allow/deny evidence.
- ESO Store/ExternalSecret conditions and Vault auth metadata without token or
  secret-value output.
- Hosted CI run, branch-protection, registry digest, SBOM/provenance/signature,
  and verification evidence.
- kube-state-metrics Secret-metric consumer need, effective RBAC, and actual
  scrape surface without reading Secret values.
- Adminer image UID/writable-path compatibility, Kubernetes API need, effective
  ServiceAccount permissions, and Pod Security admission/runtime outcome.
- An approved Git-revert/prune/auto-sync-aware recovery exercise.

## Sources

The dated baseline primary-source rows are `SRC-WERPC-023` through
`SRC-WERPC-034`, and the admitted gap-only rows are `SRC-WERPC-060` through
`SRC-WERPC-065`, in
the [source register](source-coverage-and-migration-ledger.md#source-register).
The first range was checked 2026-08-08; the second was checked 2026-08-10 and
covers only kube-state-metrics Secret RBAC/metrics, Adminer token and hardening,
and immutable Git/chart/image and verifiable-artifact distinctions. Product and
version limitations and refresh triggers are part of each row. Predecessor
documents remain dated provenance until WERPC-008; their current findings were
reconciled here without rewriting historical claims.

## Review and Freshness

Refresh this reference when Kubernetes/k3s, Argo CD, ESO, Vault, CNI,
admission/policy, GitOps root/AppProject, secret transport, image/release, or
external-gateway design changes. Also refresh the admitted rows when the
kube-state-metrics version/collector arguments/metric consumers/RBAC scope,
Adminer image/ServiceAccount/security context, Argo version or source-integrity
configuration, Git revision policy, Helm chart/provenance handling, image
digest, signature/attestation tooling, or trust policy changes. Recheck the
current primary sources before a policy decision. The required deferred
observations must remain distinct even if a local static validator passes.

### 2026-08-11 Partial/DEFER incremental refresh

This bounded increment was executed and checked on **2026-08-12**. The heading
preserves the approved package date. Public-source refresh was limited to
admitted rows REQ-WERPC-008 and REQ-WERPC-025; REQ-WERPC-009 used repository-
static evidence only. The project-advertised `.agents/skills/deep-research/`
`SKILL.md` was absent, so the Plan's official-primary-source-only workflow was
used directly. No Secret value, cluster API, registry or artifact, cloud,
gateway, hosted CI, credential, provider runtime, trust store, or recovery
execution was accessed.

#### Admitted current-source outcomes

| Official primary source                                                                                                                                                                                       | Publication / revision and adopted scope                                                                                                                                                                                                | Rejected inference, uncertainty, and refresh trigger                                                                                                                                                                                                                                           |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Kubernetes RBAC good practices](https://kubernetes.io/docs/concepts/security/rbac-good-practices/)                                                                                                           | Last modified 2026-05-20, revision `87470db12b`; checked 2026-08-12. Adopted the newly explicit warning that `get` on `nodes/proxy` is not read-only because it reaches privileged kubelet APIs and can bypass API audit and admission. | It does not prove the local Alloy grant is exercised or unnecessary. Recheck when the RBAC page, Alloy version/configuration, or local ClusterRole changes.                                                                                                                                    |
| [Grafana Alloy `loki.source.kubernetes` at v1.13.1](https://github.com/grafana/alloy/blob/v1.13.1/docs/sources/reference/components/loki/loki.source.kubernetes.md)                                           | Exact upstream tag matching the local image; checked 2026-08-12. The component tails Pod container logs through the Kubernetes API, not node logs, and defaults to the running Pod's ServiceAccount when no client block is supplied.   | Component behavior does not by itself enumerate every permission required by the complete local Alloy graph. Removal of `nodes/proxy` needs version-compatible RBAC mapping and separately authorized runtime verification.                                                                    |
| [Kubernetes admission controllers](https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/)                                                                                            | Last modified 2026-03-16, revision `65a8302b72`; checked 2026-08-12. It preserves admission as write-request enforcement and documents the new `ServiceAccountNodeAudienceRestriction` feature.                                         | Current docs are v1.36 while the repository declares k3s v1.35.0. The feature gate and live admission chain were not observed, and this feature cannot establish the external Vault role's audience binding. Recheck on the declared k3s version, feature-gate, or admission-policy selectors. |
| [Argo CD source integrity](https://argo-cd.readthedocs.io/en/latest/user-guide/source-integrity/) and [Git GnuPG verification](https://argo-cd.readthedocs.io/en/latest/user-guide/source-integrity-git-gpg/) | Current undated pages checked 2026-08-12. Project-level `spec.sourceIntegrity` can block sync when configured criteria fail; the GnuPG page identifies the Argo CD 3.5 declaration and legacy-`signatureKeys` compatibility boundary.   | The local controller version is not pinned or observed, and no local `sourceIntegrity` or `signatureKeys` selector exists. Capability is not configured enforcement. Recheck when Argo CD version/bootstrap, AppProject integrity, repository trust, or revision selectors change.             |
| [Helm documentation](https://helm.sh/docs/) and [Helm v3 provenance](https://helm.sh/docs/v3/topics/provenance/)                                                                                              | Current docs identify Helm 4.2.3; the retained exact v3 page identifies version 3.21.1. Both were checked 2026-08-12. The v3 contract binds a chart archive checksum and signer through a `.prov` file and trusted PGP key.             | Local bootstrap does not pin the Helm chart version or record provenance verification, and the local Helm client version is unobserved. The v3 procedure is not assumed compatible with every Helm 4 path. Recheck on bootstrap version/provenance or Helm major-version changes.              |
| [External Secrets Operator Vault provider](https://external-secrets.io/latest/provider/hashicorp-vault/)                                                                                                      | Current undated page checked 2026-08-12. It now gives an exact version boundary: Vault 1.20 warns for roles without an audience and Vault 1.21+ requires an audience.                                                                   | The manifest's requested `vault` audience does not prove the external Vault role, server version, token review, or authentication outcome. Recheck when ESO/Vault versions, Store authentication, ServiceAccount, or external role contract changes.                                           |
| [Gatekeeper](https://open-policy-agent.github.io/gatekeeper/website/docs/)                                                                                                                                    | Current undated documentation checked 2026-08-12. It retains validating/mutating admission and audit as distinct effects.                                                                                                               | No local Gatekeeper constraint selector exists, and neither deployment nor effective admission/audit was observed. Recheck when the admission design or policy selectors change.                                                                                                               |
| [Sigstore Cosign verification](https://docs.sigstore.dev/cosign/verifying/verify/)                                                                                                                            | Current undated page checked 2026-08-12. Keyless verification binds certificate identity and issuer; normal image verification checks the signed digest claim, while attestation uses a separate verification command.                  | A signature is not an attestation or provenance. `--check-claims=false` is rejected as the target because it skips payload-claim verification. No local signature, trust root, registry object, or enforcement was observed. Recheck when image identity or trust-policy selectors change.     |
| [SLSA v1.2 artifact verification](https://slsa.dev/spec/v1.2/verifying-artifacts)                                                                                                                             | Approved specification v1.2, checked 2026-08-12. Adopted the distinct verification steps for trusted builder identity, signed provenance envelope, expected build parameters, and consumer policy.                                      | Provenance presence alone does not prove verification or policy acceptance. No artifact, attestation, builder identity, or verifier result was accessed. Recheck on SLSA revision or local provenance policy/tooling changes.                                                                  |
| [NIST SP 800-218 SSDF v1.1](https://csrc.nist.gov/pubs/sp/800/218/final)                                                                                                                                      | Published February 2022; checked 2026-08-12. Retained only as secure-development practice vocabulary.                                                                                                                                   | It does not certify repository conformance or prove a deployed control. Recheck on a new NIST revision or an approved local SSDF mapping.                                                                                                                                                      |

The Kubernetes Secret guidance, Pod Security Admission guidance, Argo CD
tracking/auto-sync contract, and already registered baseline sources remain
supporting evidence without a material source-scope change. New external
research for NetworkPolicy, kube-state-metrics, and Adminer was explicitly
rejected as duplicate: the six Egress-only NetworkPolicy declarations, Secret
RBAC/metric distinction, and Adminer ServiceAccount/token/security-context
gaps remain answered by the existing report and static selectors.

#### Exact static reconciliation

The declared desired state remains k3s `v1.35.0-k3s1`. The Alloy manifest pins
`grafana/alloy:v1.13.1`, uses `loki.source.kubernetes` and
`loki.source.kubernetes_events`, mounts a dedicated ServiceAccount token, and
grants `get,list,watch` over a combined resource rule that includes
`nodes/proxy`, plus `get` on `pods/log`. The current Kubernetes clarification
therefore makes the combined grant a concrete least-privilege review item, but
static configuration cannot show controller need or effective authorization.

Twelve GitOps files still declare `targetRevision: main`; the root Application
and ApplicationSet paths retain automated reconciliation. Bootstrap still
installs the Argo CD chart without a chart version. Static searches found no
GitOps `sourceIntegrity` or `signatureKeys`, no image `@sha256` references under
the admitted GitOps/infrastructure/policy selectors, and no repository-static
Cosign, attestation, or provenance enforcement. Git revision identity, chart
package identity, image digest identity, signature verification, attestation
verification, provenance verification, admission, and runtime reconciliation
remain separate controls.

The Vault ClusterSecretStore still requests the `vault` audience for the named
ServiceAccount, and the TokenReview binding still references
`system:auth-delegator`. Those declarations do not establish the external
Vault role's `bound_audiences`, server version, or authentication result.
Static searches still find no Gatekeeper constraints, Kubernetes admission-
policy objects, or Pod Security Admission namespace labels in the admitted
selectors. `.kube-linter.yaml`, Conftest policies, and repository validators
are static gates, not admission or runtime evidence.

REQ-WERPC-009 remains static-only: the k3d image, declared ports, GitOps desired
state, external Traefik reference, and explicit static/live validator split are
visible. Effective cluster, gateway, registry, cloud, hosted-CI, and recovery
state remain `DEFER`; no static declaration is promoted to a runtime result.

#### Final request dispositions

| Request / final disposition | As-Is                                                                                                                                                    | Gap                                                                                                                                                            | Bounded target                                                                                                                                                                                                                                                              | Evidence depth                                                                                                                                            | Owner                                                                             | Refresh trigger                                                                                                                             |
| --------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| REQ-WERPC-008 — `Partial`   | Exact Alloy v1.13.1 and GitOps/bootstrap selectors are repo-static `Verified`; the current Kubernetes source makes `nodes/proxy` privilege explicit.     | Component need, effective RBAC, Argo/Helm compatibility, controller reconciliation, and immutable-source enforcement are `DEFER`.                              | Map each configured controller component to minimum permissions; remove `nodes/proxy` unless an exact-version need is demonstrated; separately test effective authorization and log continuity. Pin and verify Git/chart/image identities with version-compatible controls. | Current official primary sources plus exact repository-static selectors; no live or artifact evidence.                                                    | Kubernetes/observability baseline with platform delivery and security owners.     | A cited upstream contract, Alloy/Argo/Helm version, RBAC, Git revision, bootstrap, image, or policy selector changes.                       |
| REQ-WERPC-009 — `Partial`   | Repository-static k3d, GitOps, validator, and external-gateway declarations remain observable.                                                           | Effective cluster, gateway, registry, cloud, hosted CI, and provider state are `DEFER`.                                                                        | Preserve the static/runtime boundary; collect only separately authorized, read-only live evidence with rollback and secret-safe output controls.                                                                                                                            | Repository-static declarations and already registered sources only.                                                                                       | Infrastructure baseline and the operator for each external system.                | An operator authorizes a separate live observation or a named infrastructure selector changes.                                              |
| REQ-WERPC-025 — `Partial`   | ESO audience and TokenReview intent, static policy checks, and current identity/signature/attestation/provenance contracts are source/static `Verified`. | External Vault role/version, effective admission, trust roots, signatures, attestations, provenance, artifacts, recovery, and runtime enforcement are `DEFER`. | Design version-compatible, fail-closed admission and artifact verification with explicit identity/issuer/builder expectations; verify the external Vault audience contract and perform an approved recovery exercise separately.                                            | Current official primary sources plus exact policy/GitOps/infrastructure/runbook selectors; no Secret, live, trust-store, artifact, or recovery evidence. | Security baseline with Kubernetes platform, delivery, Vault, and recovery owners. | A cited security source, admission or identity selector, Vault/ESO version/role, trust policy, artifact flow, or recovery contract changes. |

No row is promoted to `Verified` because the admitted source delta and static
reconciliation do not close their runtime and compatibility questions. No
`Contradicted` row was found. PDRR-006 owns final shared-ledger integration and
contiguous source/claim IDs; this increment creates proposals only.

### 2026-08-14 consistency and Partial re-observation

This bounded increment re-observed the workspace and re-checked external
sources for `REQ-WERPC-008`, `REQ-WERPC-009`, and `REQ-WERPC-025`, checked on
**2026-08-14**. It did not run `kubectl`, `k3d`, `helm`, `argocd`, or `vault`,
and it did not query the GitHub remote for this repository. The objective
workspace check was `git diff --stat a5d2dfbb HEAD -- gitops/ policy/
infrastructure/ traefik/`, where `a5d2dfbb` is the 2026-08-12 baseline merge
commit; the command returned zero changed files, so every selector cited
below was spot-verified rather than assumed unchanged.

#### REQ-WERPC-008 Kubernetes workspace and source consistency check

**Workspace delta:** `no-change`. The six tracked policies under
`gitops/platform/network-policies/` still declare `policyTypes: [Egress]`
only; `ClusterRole/kube-state-metrics` in
`gitops/platform/monitoring/kube-state-metrics.yaml` still includes
`secrets` with `verbs: [list, watch]` and the Deployment still has no
`args`; `Rollout/adminer` in `gitops/workloads/adminer/rollout.yaml` still
declares neither `serviceAccountName`, `automountServiceAccountToken`, nor a
pod/container `securityContext`; twelve GitOps files still declare
`targetRevision: main`; and `infrastructure/bootstrap-local.sh` still runs
`helm upgrade --install argocd argo/argo-cd` with no `--version`. These are
the same selectors the [Kubernetes baseline](#kubernetes-baseline), the
[2026-08-10 refresh](#2026-08-10-gap-only-kubernetesecurity-refresh), and
the [2026-08-11 refresh](#2026-08-11-partialdefer-incremental-refresh)
already cite.

**External result:** all fourteen distinct URLs across the registered rows
`SRC-WERPC-023`–`028`, `SRC-WERPC-031`–`032`, `SRC-WERPC-034`, `SRC-WERPC-060`,
and `SRC-WERPC-062`–`065` that bound this row were reachable, with one
inconclusive sub-claim; see the [shared source-outcome
table](#re-checked-external-sources-shared-by-req-werpc-008-and-req-werpc-025)
below.

**As-Is:** Unchanged from the 2026-08-11 section: manifest intent for the
six Egress-only NetworkPolicies, the kube-state-metrics Secret RBAC/metric
distinction, the Adminer ServiceAccount/hardening gap, and the Git/chart/
image identity gaps remain repo-static `Verified`; CNI capability, effective
RBAC, controller need, and immutable-source enforcement remain `DEFER`.

**Gap and bounded target:** Unchanged. Component need, effective RBAC,
reconciliation, and supply-chain verification are not established by static
manifests alone.

**Missing evidence:** effective RBAC, admission behavior, reconciliation
state, and Secret-backend/runtime authorization for the cited grants and
gaps. **Owning authority:** Kubernetes/observability baseline with platform
delivery and security owners; the kube-state-metrics Secret-read grant and
the absent default-deny ingress posture are already tracked as the two
highest-value open items in `docs/00.agent-governance/memory/progress.md`'s
2026-08-10 entry and are not re-derived here as new findings. **Safe
boundary:** a separately authorized, non-secret, read-only effective-RBAC or
admission observation against the exact cited selector; no cluster or
credential access. **Refresh trigger:** a cited Kubernetes, Argo CD,
Gatekeeper, Helm, Sigstore, or SLSA source, or a named `gitops/`, `policy/`,
or `infrastructure/` selector, materially changes.

**Final disposition:** `Partial`, unchanged from the 2026-08-12 baseline. No
promotion. New claim registered: `CLM-WERPC-010-05`.

#### REQ-WERPC-009 Infrastructure workspace consistency check

**Workspace delta:** `no-change`. `infrastructure/README.md` still
separates `verify-contracts-static.sh` from the cluster-dependent
`verify-cluster.sh`, `verify-gitops.sh`, `verify-network-policies.sh`,
`verify-secrets.sh`, and `run-all.sh`; `infrastructure/k3d/k3d-cluster.yaml`
still pins `image: rancher/k3s:v1.35.0-k3s1` with host ports `80:80` and
`443:443`; and `gitops/clusters/local/root-application.yaml` and
`gitops/apps/root/` still track `targetRevision: main`. These match the
[Infrastructure baseline](#infrastructure-baseline) and the 2026-08-11
section's static-only reconciliation.

**External result:** not applicable this cycle. Consistent with the
2026-08-11 precedent, `REQ-WERPC-009` has no dedicated row in the source
register and continues to rely on repository-static evidence only; no
external URL was re-fetched for it. The Kubernetes/Argo CD sources checked
for `REQ-WERPC-008` provide shared background context but are not this row's
own evidence.

**As-Is:** Unchanged. Repository-static k3d, GitOps, validator, and
external-gateway declarations remain observable.

**Gap and bounded target:** Unchanged. Effective cluster, gateway, registry,
cloud, hosted-CI, and provider state remain `DEFER`; preserve the static/
runtime boundary rather than collect live evidence in this increment.

**Missing evidence:** effective cluster, gateway, registry, cloud, hosted
CI, and provider state. **Owning authority:** Infrastructure baseline and
the operator for each external system. **Safe boundary:** an
operator-authorized, read-only live observation with rollback and
secret-safe output controls; no live command was run this cycle. **Refresh
trigger:** an operator authorizes a separate live observation, or a named
`infrastructure/` or `traefik/` selector materially changes.

**Final disposition:** `Partial`, unchanged from the 2026-08-12 baseline. No
promotion. New claim registered: `CLM-WERPC-010-06`.

#### REQ-WERPC-025 Security workspace and source consistency check

**Workspace delta:** `no-change`. `policy/conftest/kubernetes.rego` still
denies plaintext `Secret` manifests, `CreateNamespace=true`, AppProject
wildcard groups/kinds, and `:latest` image tags; the checked paths still
contain no tracked Pod Security Admission labels,
ValidatingAdmissionPolicy/MutatingAdmissionPolicy resources, Gatekeeper
installation, ConstraintTemplate, or Constraint; and
`gitops/platform/eso/vault-secret-store.yaml` still requests the `vault`
audience with the `system:auth-delegator` TokenReview binding. These match
the [Security baseline](#security-baseline) and the 2026-08-11 section's
static reconciliation.

**External result:** all URLs across the registered rows `SRC-WERPC-024`–
`026`, `SRC-WERPC-028`–`034`, `SRC-WERPC-061`, and `SRC-WERPC-065` that bound
this row were reachable, with one inconclusive sub-claim; see the [shared
source-outcome
table](#re-checked-external-sources-shared-by-req-werpc-008-and-req-werpc-025)
below.

**As-Is:** Unchanged. ESO audience and TokenReview intent, static policy
checks, and current identity/signature/attestation/provenance contracts
remain source/static `Verified`.

**Gap and bounded target:** Unchanged. External Vault role/version,
effective admission, trust roots, signatures, attestations, provenance,
artifacts, recovery, and runtime enforcement remain `DEFER`.

**Missing evidence:** external Vault role/version, effective admission,
trust roots, signatures, attestations, provenance, artifacts, recovery, and
runtime enforcement. **Owning authority:** Security baseline with
Kubernetes platform, delivery, Vault, and recovery owners. **Safe
boundary:** a separately authorized, non-secret inspection of the exact
cited identity/admission/trust selector; no Secret value, trust-store,
artifact, or recovery access. **Refresh trigger:** a cited security source,
admission or identity selector, Vault/ESO version/role, trust policy,
artifact flow, or recovery contract changes.

**Final disposition:** `Partial`, unchanged from the 2026-08-12 baseline. No
promotion. New claim registered: `CLM-WERPC-010-07`.

#### Re-checked external sources (shared by REQ-WERPC-008 and REQ-WERPC-025)

A representative URL from each of the eighteen registered rows
`SRC-WERPC-023`–`034` and `SRC-WERPC-060`–`065` was re-fetched on
**2026-08-14**. Every previously adopted claim held except one, which was
inconclusive rather than contradicted.

| Source (registered row)                                                                                                                                 | Result         | Note                                                                                                                                                                                                                                                                                                                                                           |
| ------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [NetworkPolicy concepts](https://kubernetes.io/docs/concepts/services-networking/network-policies/) (`SRC-WERPC-023`)                                   | `unchanged`    | Still states policies require a supporting network implementation and that isolation follows which policies select a Pod; no visible last-modified date.                                                                                                                                                                                                       |
| [Secrets concepts](https://kubernetes.io/docs/concepts/configuration/secret/) (`SRC-WERPC-024`)                                                         | `unchanged`    | Still states Secret data is stored unencrypted in etcd by default.                                                                                                                                                                                                                                                                                             |
| [Pod Security Admission](https://kubernetes.io/docs/concepts/security/pod-security-admission/) (`SRC-WERPC-025`)                                        | `unchanged`    | Still describes namespace-scoped enforce/audit/warn against Pod Security Standards; page shows a last-modified date of March 7, 2024.                                                                                                                                                                                                                          |
| [Kubernetes policy mechanisms](https://kubernetes.io/docs/concepts/policy/) (`SRC-WERPC-026`, `034`)                                                    | `unchanged`    | Still lists API objects, admission controllers, ValidatingAdmissionPolicy, dynamic admission webhooks, and OPA Gatekeeper as an implementation example; page shows a last-modified date of December 24, 2023.                                                                                                                                                  |
| [Admission controllers reference](https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/) (`SRC-WERPC-026`)                     | `inconclusive` | Still states admission enforces create/delete/modify/connect, not reads. The fetched content was truncated twice before reaching either the `ServiceAccountNodeAudienceRestriction` entry or the page footer, so the 2026-08-12 claim that this feature is newly documented could not be independently reconfirmed this cycle. Not contradicted — unconfirmed. |
| [Argo CD automated sync](https://argo-cd.readthedocs.io/en/stable/user-guide/auto_sync/) (`SRC-WERPC-027`)                                              | `unchanged`    | Still describes automated sync, prune, self-heal, and retry policy; no explicit version shown.                                                                                                                                                                                                                                                                 |
| [Argo CD cluster bootstrapping](https://argo-cd.readthedocs.io/en/stable/operator-manual/cluster-bootstrapping/) (`SRC-WERPC-027`)                      | `unchanged`    | Still documents ApplicationSet cluster-generator and app-of-apps as the two bootstrapping approaches.                                                                                                                                                                                                                                                          |
| [Gatekeeper introduction v3.22.x](https://open-policy-agent.github.io/gatekeeper/website/docs/v3.22.x/) (`SRC-WERPC-028`, `034`)                        | `unchanged`    | Still describes Gatekeeper as a validating and mutating OPA-backed webhook with audit capability.                                                                                                                                                                                                                                                              |
| [RBAC good practices](https://kubernetes.io/docs/concepts/security/rbac-good-practices/) (`SRC-WERPC-031`)                                              | `unchanged`    | Still warns `get` on `nodes/proxy` is not read-only, and that `list`/`watch` on Secrets reveals contents the same as `get`.                                                                                                                                                                                                                                    |
| [SLSA v1.2 specification](https://slsa.dev/spec/v1.2/) (`SRC-WERPC-032`)                                                                                | `unchanged`    | Still the current Approved specification version; no newer released version referenced.                                                                                                                                                                                                                                                                        |
| [NIST SP 800-218 SSDF v1.1](https://csrc.nist.gov/pubs/sp/800/218/final) (`SRC-WERPC-033`)                                                              | `unchanged`    | Still Final, published February 2022; page now surfaces a related `SP 800-218A` part reference not previously noted, which extends rather than contradicts the adopted scope.                                                                                                                                                                                  |
| [kube-state-metrics v2.14.0 README and standard ClusterRole](https://github.com/kubernetes/kube-state-metrics/blob/v2.14.0/README.md) (`SRC-WERPC-060`) | `unchanged`    | Content pinned to the immutable `v2.14.0` git tag; the standard `ClusterRole` example still grants `secrets` `list`/`watch`.                                                                                                                                                                                                                                   |
| [Authorization request verbs](https://kubernetes.io/docs/reference/access-authn-authz/authorization/index.html) (`SRC-WERPC-061`)                       | `unchanged`    | Still documents `get`/`list`/`watch` as distinct verbs that are equivalent in data access, including the `list` on `secrets` caution.                                                                                                                                                                                                                          |
| [Application security checklist](https://kubernetes.io/docs/concepts/security/application-security-checklist/) (`SRC-WERPC-062`)                        | `unchanged`    | Still recommends `automountServiceAccountToken: false` unless needed, dedicated ServiceAccounts over `default`, and deployment into a namespace enforcing an appropriate Pod Security Standard.                                                                                                                                                                |
| [Argo CD source integrity](https://argo-cd.readthedocs.io/en/stable/user-guide/source-integrity/) (`SRC-WERPC-063`)                                     | `unchanged`    | Still describes project-level `sourceIntegrity` blocking sync on failed criteria; no version number stated on this page. The `tracking_strategies`, `source-integrity-git-gpg`, and `helm` pages under this row were not individually re-fetched this cycle.                                                                                                   |
| [Helm v3 provenance](https://helm.sh/docs/v3/topics/provenance/) (`SRC-WERPC-064`)                                                                      | `unchanged`    | Still describes the `.prov` file, SHA256 checksum, and OpenPGP signature contract, plus `helm install --verify`. The Kubernetes image-names page under this row was not individually re-fetched this cycle.                                                                                                                                                    |
| [Sigstore Cosign verification](https://docs.sigstore.dev/cosign/verifying/verify/) (`SRC-WERPC-065`)                                                    | `unchanged`    | Still describes keyless verification binding certificate identity and issuer, and that `--check-claims=false` skips payload-claim verification only.                                                                                                                                                                                                           |
| [GitHub artifact attestations](https://docs.github.com/en/actions/concepts/security/artifact-attestations) (`SRC-WERPC-065`)                            | `unchanged`    | Still states attestations are not by themselves a security guarantee; the SLSA-provenance and cosign-attestation-verify pages under this row were not individually re-fetched this cycle.                                                                                                                                                                      |

No `kubectl`, `k3d`, `helm`, `argocd`, or `vault` command was run, and no
GitHub API or `gh` query was made; only public documentation pages were
fetched. No row is promoted to `Verified`; no row is `Contradicted`. New
source registered: `SRC-WERPC-075`. New claims registered:
`CLM-WERPC-010-05` through `CLM-WERPC-010-07`.

## Related Documents

- [CI/CD and QA](ci-cd-github-actions-and-qa.md)
- [Source coverage and migration ledger](source-coverage-and-migration-ledger.md)
- [GitOps overview](../../../../gitops/README.md)
- [Infrastructure overview](../../../../infrastructure/README.md)
- [ArgoCD ESO Vault recovery runbook](../../../05.operations/runbooks/0002-argocd-eso-vault-recovery-runbook.md)
- [Operations policies](../../../05.operations/policies/README.md)
