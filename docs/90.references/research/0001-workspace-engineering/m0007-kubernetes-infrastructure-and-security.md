---
title: "Reference: Kubernetes, Infrastructure, and Security"
version: "1.1.0"
type: "reference/research"
status: "published"
owner: "platform"
updated: "2026-09-27"
layer: "references"
artifact_id: "RES-0001-m0007"
---

# Reference: Kubernetes, Infrastructure, and Security

## Overview

This reference synthesizes current external Kubernetes, infrastructure and security knowledge for platform, delivery, security and operations decisions. It covers U08/U09/U26 and preserves earlier local observations as dated history. It does not assess this workspace's current deployment or authorize implementation.

## Reference Type

Primary-source external research and conditional follow-up investigation design; historical repository/hosted evidence is separately dated below. The settled profile is reference/research under the Stage 99 research template.

## Authority Boundary

This reference supplies decision inputs, not policy, deployment authority or a current implementation verdict. Canonical implementation, governance and operational owners retain their responsibilities. Rendering, local document QA and configuration declarations establish neither hosted execution nor provider/runtime, authorization, reconciliation, security enforcement, intended-use fitness or restore success. Every workspace result is **not observed in this cycle**.

## Scope

Includes API/controller and declarative delivery, support/skew/API/CRD lifecycle, network/DNS/Gateway/TLS, storage and recovery, resources/scheduling/probes/SLO/cost, Linux/provisioning/IaC/environment separation, RBAC/admission/secrets, artifact trust, vulnerability response and rollback. Single-host development/home-lab and multi-host operational trade-offs are distinguished without deciding which is deployed here. No local implementation audit, live cluster/cloud/Vault/Argo access, credential reading, configuration change or recovery execution is included.

## Definitions / Facts

### Current external research

This synthesis was researched against directly read primary sources on **2026-09-27 (Asia/Seoul)**. The claim register distinguishes external support from source refresh outcomes; every workspace result is **not observed in this cycle**. Implementation choices below are conditional analysis, not decisions or detected local deficiencies.

#### API reconciliation and declarative delivery

`CLM-WERPC-017-81` (`SRC-WERPC-170, SRC-WERPC-171, SRC-WERPC-172`): Kubernetes controllers watch desired and current state and reconcile differences, including reporting external state. An API write is not an atomic transaction across controllers, networking and applications. Workload controllers manage Pods; namespaces scope namespaced objects but not Nodes, PVs or StorageClasses, and labels acquire meaning through selectors rather than intrinsic security semantics. Choose workload, namespace and label conventions around ownership and selection; namespace separation alone is not tenant isolation. Verification needs rendered selectors, controller ownership and status transitions; a completed API request alone is insufficient.

`CLM-WERPC-017-82` (`SRC-WERPC-175, SRC-WERPC-176, SRC-WERPC-250`): Kustomize composes bases, overlays, patches and generated configuration; Helm packages templates and release inputs. Choose plain YAML for small stable sets, Kustomize for reviewed environment differences, and Helm where upstream chart lifecycle is useful. Complexity grows when multiple tools own the same field. Resolve tool versions and inputs, render deterministically, then check schemas and policy. Rendering cannot establish API admission or controller effect. The generic Helm page identifies 4.3.0 but explicitly warns its text is not updated for Helm 4: its CRD installation/upgrade limitations are adopted only as **Helm 3** guidance.

`CLM-WERPC-017-99` (`SRC-WERPC-027, SRC-WERPC-063`): OpenGitOps v1.0.0 defines declarative desired state with versioned immutable history, automatic pulling and continuous reconciliation (`SRC-WERPC-264`). Argo CD documents explicit prune/self-heal settings and source-integrity failure preventing sync. Automated-sync rollback is unavailable while automation is enabled; a controlled Git reversal is one recovery option, whose effect still needs observation. Bootstrap installs the management plane and trust inputs; ongoing desired-state reconciliation has a different owner and recovery path. Pinning a Git revision improves reproducibility but adds promotion work; branch tracking eases updates but requires precise revision records. Test deletion/prune effects, source-policy failures, fetched revision, sync and application health independently. Do not infer chart/OCI authentication from Git verification.

#### Version API and CRD lifecycle

`CLM-WERPC-017-83` (`SRC-WERPC-143`): The release page lists 1.37.0 released 2026-08-26, and maintained lines 1.37, 1.36 and 1.35. It also lists 1.34.11 with EOL 2026-10-27; the apparent wording/table difference remains unresolved rather than silently reclassified. Version-skew policy permits HA API servers one minor apart; kubelets and proxies must not be newer than the API server and generally may be three minors older (older than 1.25: two); controllers may be one older, and kubectl one either side. Distribution rules may be stricter. Upgrade one minor at a time with the documented sequence, capacity, drain and recovery prerequisites; patch currency is not compatibility evidence.

`CLM-WERPC-017-84` (`SRC-WERPC-173, SRC-WERPC-174`): Kubernetes GA, beta and alpha API deprecation guarantees differ; vendor CRDs do not inherit those guarantees. CRD served versions, selected storage version and recorded storedVersions are separate. Preserve conversion support and migrate stored objects before removing an old storage version. Compare API discovery, release/deprecation notes, rendered resources and CRD conversion/storage contracts before upgrade. A successful render cannot detect every removed live API or failed conversion; deleting a CRD risks deleting its instances. Helm 3's non-templated CRD installation does not provide automatic upgrade, rollback or deletion.

#### Network DNS Gateway and TLS

`CLM-WERPC-017-85` (`SRC-WERPC-023`): NetworkPolicy needs an enforcing network implementation. Ingress and egress isolation are independent and allowed policies are additive; selected traffic can require both source egress and destination ingress permission. Default-deny plus explicit DNS/service exceptions improves bounded isolation but requires complete dependency mapping. Existing-connection behavior on a policy change is implementation dependent. Verify CNI capability, exact selectors and separately controlled allowed/denied new flows; do not substitute YAML review for packet evidence.

`CLM-WERPC-017-86` (`SRC-WERPC-177, SRC-WERPC-178, SRC-WERPC-179, SRC-WERPC-180`): Service DNS search is namespace-sensitive; cross-namespace access needs an appropriate name. Ingress is frozen but not planned for removal and requires a controller. Gateway API separates GatewayClass, Gateway and Route responsibilities and requires compatible CRDs/controller/conformance. Choose Ingress for sufficient stable routing or Gateway for required role separation and richer routing, accounting for migration cost. Downstream TLS termination/passthrough and upstream BackendTLSPolicy are distinct trust legs. The TLS guide's TLSRoute v1.5.0 stable statement is a documented feature boundary, not a local installed version. Verify DNS, routes, certificate identity/expiry/renewal and backend TLS separately; avoid assuming controller-independent feature support.

#### Storage backup and recovery

`CLM-WERPC-017-87` (`SRC-WERPC-181`): A PV represents backing storage; a namespaced PVC requests it. Dynamic provisioning depends on StorageClass/CSI/topology and reclaim behavior. Delete commonly removes backing storage; Retain requires manual disposition. ReadWriteOnce is a node constraint, not a guarantee of one Pod. Choose storage on durability, placement, access and recovery requirements; local storage lowers operational cost but constrains rescheduling. Check reclaim rules, CSI capabilities, binding, attach/mount and deletion finalizers before destructive changes.

`CLM-WERPC-017-88` (`SRC-WERPC-182, SRC-WERPC-183`): K3s recovery differs for SQLite, external databases and embedded etcd, and restore requires the protected server-token material to decrypt datastore content. Velero **v1.17 is an example version**, not a latest-version assertion: it backs up API objects and supported volume snapshots, requires restore API versions to exist, and describes a default 30-day TTL whose expiry deletes backups/snapshots. Neither control-plane snapshots nor volume snapshots guarantee application-consistent or external-database recovery. Choose backup scope, off-host copies, retention and encryption from loss scenarios and agreed RPO/RTO; verify a representative isolated restore, data correctness and service recovery without recording tokens.

#### Resources scheduling availability and SLO

`CLM-WERPC-017-89` (`SRC-WERPC-223`): Requests drive scheduling; CPU limits throttle and memory limits can lead to reactive OOM termination. Disk-backed ephemeral storage and memory-backed emptyDir have different accounting. Choose requests from measurements plus headroom; under-requesting increases contention and over-requesting strands capacity/cost. Test workload peaks, CPU throttling, OOM/eviction and storage pressure; manifest values are not utilization measurements.

`CLM-WERPC-017-90` (`SRC-WERPC-226, SRC-WERPC-227`): Topology spread can be hard DoNotSchedule or soft ScheduleAnyway; affinity can be required or preferred. Hard placement protects separation but may leave Pods pending. IgnoredDuringExecution does not evict on later label change; security-relevant node labels require the documented Node authorizer/NodeRestriction boundary. Observe eligible topology domains and scheduling outcomes. Multiple containers or logical nodes on one host do not create physical failure independence.

`CLM-WERPC-017-91` (`SRC-WERPC-224`): Liveness can restart a container, readiness controls traffic eligibility and startup probes protect slow initialization. A bad liveness threshold can amplify overload into cascading restarts. Choose checks around a failure action, avoid treating a temporarily unavailable dependency as a reason to restart everything, and measure startup/load/failure transitions. Probe declaration alone is not availability proof.

`CLM-WERPC-017-92` (`SRC-WERPC-225, SRC-WERPC-245`): PDBs constrain voluntary eviction but cannot prevent involuntary loss or enforce application-controller rolling-update availability. K3s embedded-etcd HA needs at least three servers with an odd quorum and suitable disk performance. A one-host home lab may accept outage and simple restore; multi-host operation needs genuine failure domains, redundant capacity and maintenance tests. A PDB cannot make a singleton highly available and may block drain.

`CLM-WERPC-017-93` (`SRC-WERPC-228`): Choose a few user-relevant SLIs such as availability, latency, durability or correctness, then agree SLOs and error budgets appropriate to the service. Observability combines user outcomes with controller, node and application signals; metric collection alone is not an SLO. Capacity and cost analysis should include requests versus use, peaks, spare failure capacity, storage/backup growth and operational effort. No numerical home-lab SLO is prescribed here. Verify indicators against actual user paths and use breach/burn and capacity evidence to justify changes.

#### Host provisioning state and environment separation

`CLM-WERPC-017-94` (`SRC-WERPC-244, SRC-WERPC-245, SRC-WERPC-246`): K3s prerequisites include Linux/cgroups, unique node identities, suitable storage I/O and CNI-dependent connectivity; minimum host resources exclude workload demand. Do not expose VXLAN UDP 8472 publicly or translate troubleshooting advice into blanket firewall removal. Kubernetes Linux-security guidance warns that secret/memory-backed data can reach swap under older or unsupported configurations; kernel/backport support matters. The context-dependent, nonexhaustive Kubernetes security checklist (`SRC-WERPC-265`) describes syscall/security profiles, image scanning/patching and protected audit logs; a profile declaration does not prove an active kernel control. Provisioning should bind host/cluster versions, ports, storage, recovery assets and upgrade ownership. Disposable development clusters trade fidelity for cheap reset; replicas on one Linux host share its failure boundary. Verify host and network prerequisites separately from cluster creation and workload behavior.

`CLM-WERPC-017-95` (`SRC-WERPC-247, SRC-WERPC-248, SRC-WERPC-249`): Terraform 1.16.x documentation makes locking backend dependent, lock acquisition failure a stop condition and force-unlock appropriate only for one's own lock. Sensitive redaction does not remove values from state; local state can be plaintext, and ephemeral/write-only facilities have version/provider conditions. CLI workspaces isolate state but are inappropriate for boundaries requiring separate credentials or access control. Choose separate state/backends/credentials where trust separation matters; one tool is not mandatory. Inspect sanitized backend/lock/access contracts, environment-to-state identity and concurrent-operation behavior, never raw state containing secrets.

#### Identity policy secrets and supply chain

`CLM-WERPC-017-96` (`SRC-WERPC-031, SRC-WERPC-108`): Prefer bounded ServiceAccounts and least-privilege authorization with short-lived, audience-bound TokenRequest credentials where needed. Secret list/watch permits object data, and nodes/proxy GET can reach privileged kubelet operations while bypassing API audit/admission. A metadata-only exporter does not narrow that authorization. Choose explicit resource/namespace scope and disable unneeded automatic token mounts after compatibility review; verify effective permissions and consumer need, not just role text.

`CLM-WERPC-017-97` (`SRC-WERPC-025, SRC-WERPC-250`): Pod Security Admission separates enforce/audit/warn; enforcement checks Pods while audit/warn also inspect workload templates, and exemptions skip checks. Native CEL ValidatingAdmissionPolicy needs a binding and explicit actions/failure behavior. Choose baseline/restricted PSA for standard posture, native CEL for compatible custom rules or a separately evaluated webhook policy engine. Audit/warn eases adoption but does not deny; fail-open policies ease outages but weaken enforcement. Test exemptions, invalid cases, failure paths and rollback with the exact API version. CI policy-as-code is a separate pre-merge boundary.

`CLM-WERPC-017-98` (`SRC-WERPC-024, SRC-WERPC-029`): Kubernetes Secrets are unencrypted in etcd by default; Pod-creation permission can expose namespace Secrets through mounts. Secret volume updates are eventual and subPath mounts do not automatically update. ESO Vault guidance documents audience warnings for Vault 1.20 and an audience requirement at 1.21+, plus namespace requirements for ClusterSecretStore ServiceAccount references. Choose backend/transport/at-rest access and rotation/reload contracts together. Observe redacted identity/conditions and consumer reload; never collect Secret values, tokens or private keys.

`CLM-WERPC-017-100` (`SRC-WERPC-064, SRC-WERPC-065, SRC-WERPC-015, SRC-WERPC-251, SRC-WERPC-252`): Image digests fix bytes; tags may move. Helm **v3.22.0** provenance binds chart checksum/signature to a trusted key and fails verification before rendering. Cosign keyless verification needs expected identity/issuer and digest claims; attestation verification is separate. SLSA v1.2 verification checks signed provenance, subject digest, trusted builder and expected parameters; presence establishes neither a level nor artifact safety. SPDX/CycloneDX describe SBOM inventory/dependencies and related completeness/vulnerability context, not vulnerability absence. Choose artifact/registry retention, SBOM format, signature/provenance production and receiver policy to match release risk; reassess affected dependencies, replace or revoke unsafe artifacts and retain audit/rollback evidence. Immutable artifacts can remain vulnerable. Public NIST SSDF v1.1 metadata supplies practice vocabulary, not certification; inaccessible CISA SBOM pages supply no verified minimum-element claim.

### Follow-up workspace questions

The complete evidence contracts are indexed in [the follow-up question ledger](m0013-scope-application-index.md#follow-up-question-ledger). Each row below uses its corresponding current claim/source mapping; all results are **not observed in this cycle**. The central ledger owns scopes, candidate selectors, approval/risk boundaries, evidence contracts, next roles and triggers; this table supplies topic-specific questions without duplicating that contract. No credential or Secret value may be collected.

| Question / U / requirement / claim | Topic question and distinguishing evidence |
| --- | --- |
| Q-WERPC-096 / U08 / REQ-WERPC-008 / CLM-WERPC-017-81 | Map controller ownership and selected objects; resolve ambiguous ownership and dangling selectors. Observe reconciliation status separately from the static graph. |
| Q-WERPC-097 / U08 / REQ-WERPC-008 / CLM-WERPC-017-82 | Capture render versions/inputs/output identities; check intended resources, field ownership and CRD installation order. Admission requires its own approved test. |
| Q-WERPC-098 / U08 / REQ-WERPC-008 / CLM-WERPC-017-83 | Build current/proposed vendor-specific skew/support matrix and sequential upgrade/drain/rollback prerequisites; newest release alone cannot pass compatibility. |
| Q-WERPC-099 / U08 / REQ-WERPC-008 / CLM-WERPC-017-84 | Inventory removed/deprecated APIs and conversion/storage migration; removal acceptance requires successful migration and rollback compatibility, not render success. |
| Q-WERPC-100 / U08 / REQ-WERPC-008 / CLM-WERPC-017-85 | Produce static allow/deny matrix including DNS; separately approve positive/negative new and established TCP/UDP flow tests against exact CNI. |
| Q-WERPC-101 / U08 / REQ-WERPC-008 / CLM-WERPC-017-86 | Map DNS, downstream termination and upstream trust/renewal owner; approved probes must meet hostname/chain/route/denial/renewal expectations without private keys. |
| Q-WERPC-102 / U09 / REQ-WERPC-009 / CLM-WERPC-017-87 | Resolve storage ownership, deletion/retention, placement and snapshot compatibility; any destructive/node-failure test needs operator approval and recoverable fixtures. |
| Q-WERPC-103 / U09 / REQ-WERPC-009 / CLM-WERPC-017-88 | Record backup IDs/version/TTL/off-host scope and key-availability procedure; approved isolated restore must prove agreed data correctness, RPO/RTO and service recovery without token values. |
| Q-WERPC-104 / U08 / REQ-WERPC-008 / CLM-WERPC-017-89 | Compare requests/limits with sanitized peak/throttle/OOM/eviction measurements and headroom; capacity acceptance must cover workload and failure load. |
| Q-WERPC-105 / U08 / REQ-WERPC-008 / CLM-WERPC-017-90 | Map eligible physical failure domains; test intended hard/soft scheduling and pending behavior, separately approving scheduler/runtime evidence. |
| Q-WERPC-106 / U08 / REQ-WERPC-008 / CLM-WERPC-017-91 | Define failure actions and timing; approved slow-start/load/dependency-loss tests must show readiness and restart behavior without cascading failure. |
| Q-WERPC-107 / U08 / REQ-WERPC-008 / CLM-WERPC-017-92 | Distinguish voluntary maintenance from host loss; demonstrate spare capacity, quorum and expected drain/rollout behavior under approved scenarios. |
| Q-WERPC-108 / U08 / REQ-WERPC-008 / CLM-WERPC-017-93 | Select user paths, objectives, error budget and capacity/cost model; acceptance needs measured user outcomes and justified targets rather than metric presence. |
| Q-WERPC-109 / U09 / REQ-WERPC-009 / CLM-WERPC-017-94 | Check distro/Linux/cgroups/swap support, private CNI exposure, disk capacity and physical failure independence; approved host/runtime evidence stays separate from declarations. |
| Q-WERPC-110 / U09 / REQ-WERPC-009 / CLM-WERPC-017-95 | Map each environment to credentials and state owner; check locking/conflict handling and access/encryption contract without raw state. Pass requires the intended trust separation, not workspace names. |
| Q-WERPC-111 / U26 / REQ-WERPC-025 / CLM-WERPC-017-96 | Map resource/verb/namespace need, Secret-read and nodes/proxy access; approved effective authorization and exporter-consumer evidence must justify each permission. |
| Q-WERPC-112 / U26 / REQ-WERPC-025 / CLM-WERPC-017-97 | Check modes/exemptions/version/failure policy; separately approved negative admission and dependency-failure cases must prove denials and usable rollback. |
| Q-WERPC-113 / U26 / REQ-WERPC-025 / CLM-WERPC-017-98 | Observe only sanitized role/condition/reference metadata; approved tests must establish audience alignment, encrypted transport/storage and timely consumer reload without payloads. |
| Q-WERPC-114 / U08 / REQ-WERPC-008 / CLM-WERPC-017-99 | Trace source policy, revision, render, sync and health; approved bad-source/prune/Git-reversal scenarios must meet explicit recovery criteria. |
| Q-WERPC-115 / U26 / REQ-WERPC-025 / CLM-WERPC-017-100 | Bind accepted artifact to signer/builder/parameters and vulnerability decisions; approved invalid-identity/digest tests fail closed. Track patch/rebuild/promotion and compatible rollback audit evidence. |

## Sources

Current claim mappings are `CLM-WERPC-017-81` through `CLM-WERPC-017-100` in [current source observations](m0012-source-coverage.md#current-source-observations). These link directly read primary sources, dates, section selectors, version/revision limits and source refresh results. The current definition of factual `Verified` applies only within those external scopes; conditional choices and future criteria are research analysis.

Key primary anchors include [Kubernetes controller concepts](https://kubernetes.io/docs/concepts/architecture/controller/), [version skew policy](https://kubernetes.io/releases/version-skew-policy/), [NetworkPolicy semantics](https://kubernetes.io/docs/concepts/services-networking/network-policies/), [K3s datastore backup/restore](https://docs.k3s.io/datastore/backup-restore), [Terraform state locking](https://developer.hashicorp.com/terraform/language/state/locking), [Argo automated sync](https://argo-cd.readthedocs.io/en/stable/user-guide/auto_sync/), and [SLSA v1.2 verification](https://slsa.dev/spec/v1.2/verifying-artifacts).

Currency/access limits: mutable `stable`/`latest` and publisher footer abbreviations are not reproducible full immutable page pins. Helm 4 equivalence is unverified; Helm 3 CRD/provenance scope is explicit. Velero v1.17 and Terraform's 1.16.x documentation are qualified examples/surfaces, not installed-version observations. The release-page 1.34 wording/table ambiguity is retained. SPDX landing and CycloneDX overview do not establish full standard compliance or a latest patch release; the CycloneDX 1.7 mediaType example is not release verification. NIST SSDF public metadata was read, not the complete standard. CISA SBOM and OWASP vulnerability-management pages were inaccessible to the research tool; this is `unreachable`, not a proven HTTP 404 or an implementation gap. Their unverified contents support no claim.

## Review and Freshness

Recheck primary contracts before a decision when the cited release, support window, API, controller, driver, backend, event, permission, trust policy, test method, stakeholder expectation or recovery objective changes. Source freshness is distinct from historical local truth. Detailed current evidence and question contracts remain with their respective ledger owners.

### Evidence insufficiency correction dated 2026-09-27

The retained 2026-08-18 paragraph associated with `CLM-WERPC-012-02` inferred that default collectors had been running without required RBAC and called it a live pre-existing defect. Static image/argument/RBAC declarations do not establish running collectors, effective authorization, requests or failures. **That live-effect inference is unsupported and is withdrawn as a current conclusion**; the original dated wording remains below for correction provenance. `CLM-WERPC-017-96` supplies the current authorization boundary, and Q-WERPC-111 specifies the next evidence. Neither this correction nor later dated pin notes establish present workspace state.

### Dated history retained from 2026-08-08 through 2026-09-14

The material below preserves earlier observation dates, claim/source identifiers, corrections and section anchors. Its words such as current, confirmed, Verified, As-Is and defect refer to those dated cycles, not this cycle. Historical commands and retired selectors are provenance, not instructions to load or execute them. Superseding dated notes and the explicit correction above must be read with the earlier passages. No historical status is promoted by the new external access date.

#### Historical overview

This reference records a 2026-08-08 repository-static baseline, plus a bounded
2026-08-10 gap-only refresh, for the local k3d platform, its Argo CD GitOps
desired state, and related security controls.
It is a decision input for platform, security, delivery, and operations owners;
it is not a change authorization, live-cluster assessment, or certification.

#### Historical reference type

Current-primary-source research combined with repository-static platform and
security evidence. The source register is [the pack ledger](m0012-source-coverage.md#source-register).

#### Historical authority boundary

`gitops/` remains the Kubernetes desired-state authority, `infrastructure/`
owns bootstrap and static/live test boundaries, and Stage 05 owners retain
operational authority. A manifest, local policy, or static validator does not
prove an Argo CD sync, Kubernetes admission/CNI enforcement, effective RBAC,
Vault/ESO readiness, secret rotation, CI execution, or an external gateway.
Those remote/live/credential-bearing observations remain `DEFER` unless a
separately approved read-only check collects them without secret values.

#### Historical scope

Included: Kubernetes desired state, GitOps reconciliation, infrastructure
boundaries, network/RBAC/secret/admission controls, rollout and rollback
implications, supply-chain controls, and a workspace-specific gap analysis.

Excluded: direct cluster, Docker, Argo CD, Vault, ESO, CNI, registry, cloud, or
gateway access; kubeconfig and credential inspection; secret-value access; and
any implementation or policy decision. Baseline external pages were checked on
2026-08-08; only the admitted kube-state-metrics, Adminer, and immutable
delivery sources were checked on 2026-08-10. Product version and configuration
applicability remain bounded in the ledger.

#### Historical definitions / facts

#### Evidence-depth model

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

#### Layered platform model and trust boundaries

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
live rollback capability. [SRC-WERPC-027](m0012-source-coverage.md#source-register)
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

#### Kubernetes baseline

Kubernetes NetworkPolicy is meaningful only when the selected networking
implementation enforces it; isolation behavior follows the policies selecting a
Pod. [SRC-WERPC-023](m0012-source-coverage.md#source-register)
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

#### Infrastructure baseline

`infrastructure/README.md` separates `verify-contracts-static.sh` from
cluster-dependent checks such as `verify-cluster.sh`, `verify-gitops.sh`,
`verify-network-policies.sh`, `verify-secrets.sh`, and `run-all.sh`. The static
boundary is therefore `Verified`; the existence, TLS trust, k3d state, Docker
state, endpoint reachability, and results of the live scripts are `DEFER`.

The root Application and platform Application declarations provide a versioned
desired-state topology, but track a branch (`main`) rather than an immutable
commit. This is an observation for change-control and recovery design, not a
finding that the selected revision was fetched or reconciled.

#### Security baseline

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
they complement rather than replace repository linting. [SRC-WERPC-025](m0012-source-coverage.md#source-register),
[SRC-WERPC-026](m0012-source-coverage.md#source-register), and
[SRC-WERPC-028](m0012-source-coverage.md#source-register) define
the source boundary.

Kubernetes documents Secrets as base64-encoded and unencrypted in etcd by
default. No cluster encryption configuration, effective Secret RBAC, or
generated Secret metadata/value was inspected here. [SRC-WERPC-024](m0012-source-coverage.md#source-register)
is a platform benchmark, not evidence of the local setting.

#### 2026-08-10 gap-only Kubernetes/Security refresh

This refresh admits only three question-level deltas left under-sourced by the
baseline. The proposed targets are decision inputs, not manifest changes. The
Namespace ingress/default-deny candidate was rejected as a duplicate: the
existing [Kubernetes baseline](#kubernetes-baseline) and
[SRC-WERPC-023](m0012-source-coverage.md#source-register) already
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
[SRC-WERPC-060](m0012-source-coverage.md#source-register) and
[SRC-WERPC-061](m0012-source-coverage.md#source-register) bound
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
that the standard ClusterRole is necessary. [CLM-WERPC-008-01](m0012-source-coverage.md#werg-003-gap-only-claim-register)
and [CLM-WERPC-008-02](m0012-source-coverage.md#werg-003-gap-only-claim-register)
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
[SRC-WERPC-062](m0012-source-coverage.md#source-register),
[CLM-WERPC-008-03](m0012-source-coverage.md#werg-003-gap-only-claim-register),
and [CLM-WERPC-008-04](m0012-source-coverage.md#werg-003-gap-only-claim-register)
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
[SRC-WERPC-063](m0012-source-coverage.md#source-register) and
[SRC-WERPC-064](m0012-source-coverage.md#source-register) are the
direct product sources.

Currency note (2026-09-14): the bootstrap observation above no longer holds.
`infrastructure/bootstrap-local.sh` now installs Argo CD with an exact chart
version (`10.4.0`) and MetalLB `0.16.1`, and the live network-policy check this
report cites under `infrastructure/tests/` now lives at
`infrastructure/verify/verify-network-policies.sh`. The dated finding is kept as
observed; a targeted refresh of this report owns any new conclusion.

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
result was observed. [SRC-WERPC-065](m0012-source-coverage.md#source-register),
[CLM-WERPC-008-05](m0012-source-coverage.md#werg-003-gap-only-claim-register),
and [CLM-WERPC-008-06](m0012-source-coverage.md#werg-003-gap-only-claim-register)
preserve these non-equivalences.

| Delta                    | Exact repository selector                                                                                                                                                                     | As-Is                                                                                                                  | Gap / decision input                                                                               | Target acceptance evidence                                                                                                                                                                                              |
| ------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Secret collector/RBAC    | `gitops/platform/monitoring/kube-state-metrics.yaml`: `ClusterRole/kube-state-metrics rules[apiGroups=[""]]` containing `resources: secrets`, `verbs: [list, watch]`; container has no `args` | Cluster-wide Secret object read stream is declared for the v2.14.0 collector.                                          | Whether any `kube_secret_*` metric consumer justifies it is unobserved.                            | Consumer inventory, approved minimum resource/namespace scope, static manifest validation, then separately authorized effective-RBAC and scrape evidence without values.                                                |
| Adminer token/hardening  | `gitops/workloads/adminer/rollout.yaml`: `Rollout/adminer spec.template.spec` lacks `serviceAccountName`, `automountServiceAccountToken`, and pod/container `securityContext`                 | Kubernetes defaults and workload fields leave token and hardening intent implicit.                                     | API need and image compatibility are unknown; linter exemptions do not establish safety.           | Approved ServiceAccount/RBAC decision, token-disabled manifest, image compatibility test, restricted-field static checks, and separately authorized admission/runtime evidence.                                         |
| Git/chart/image identity | `gitops/clusters/local/root-application.yaml`, `gitops/clusters/local/applicationset-apps.yaml`, `gitops/apps/root/`, `infrastructure/bootstrap-local.sh`, Adminer/KSM/Alloy image fields     | Git sources track `main`; chart applications mix exact versions with an unpinned bootstrap chart; images are tag-only. | Identity, authenticity, build provenance, and policy enforcement are separate unproven properties. | Environment-specific immutable-ref policy, full Git SHA where required, pinned bootstrap chart, image `tag@digest`, and independently configured/verified provenance or signatures against explicit trust expectations. |

#### Threat, control, and evidence matrix

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

#### Policy, reconciliation, rollout, and rollback design implications

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
provenance, attestation, or signature verification was observed. [SRC-WERPC-032](m0012-source-coverage.md#source-register)
and [SRC-WERPC-034](m0012-source-coverage.md#source-register)
must not be converted into implementation claims.

#### Workspace As-Is, gap, and target matrix

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

#### Required deferred-validation backlog

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

#### 2026-08-17 full-corpus refresh

This increment is the fifth refresh cycle over this pack, executed under
Spec 058. Unlike the three preceding cycles it re-observed every owner row in
the pack rather than the twelve `Partial` rows, and it assigns each retained
`Partial` or `DEFER` row a blocking class recorded in the
[scope application index](m0013-scope-application-index.md). All observations are
dated **2026-08-17**. No live cluster, hosted CI run, provider runtime,
authenticated execution, or secret value was observed.

#### Two recorded refresh triggers fired

`REQ-WERPC-008` and `REQ-WERPC-025` carried refresh triggers written into this
report's own source rows, and both fired on 2026-08-17. This is a contract signal
rather than a judgement call.

| Trigger source  | Recorded condition                              | Observed on 2026-08-17                                  |
| --------------- | ----------------------------------------------- | ------------------------------------------------------- |
| SRC-WERPC-060   | kube-state-metrics version changes              | pinned `v2.14.0`; upstream latest `v2.19.1` (2026-06-10) |
| SRC-WERPC-063   | Argo CD source-integrity facility changes       | shipped GA in `3.5.0` (2026-08-04) and `3.5.1` (2026-08-12) |

#### REQ-WERPC-008 re-observation

**External result:** `changed` (`SRC-WERPC-081`, `SRC-WERPC-084`,
`SRC-WERPC-085`). kube-state-metrics has released five minor versions past the
pinned `v2.14.0`. The upstream `v2.19.1` standard `ClusterRole` still grants
`secrets` `list` and `watch`, so this report's security claim is unchanged. Argo
CD's `sourceIntegrity` facility, described here as newer and labeled version 3.5,
is now shipped in stable releases rather than forward-looking. Gatekeeper's
current documentation tracks `v3.23.x`, one minor ahead of the pinned `v3.22.x`
reference, with the concept unchanged.

**Workspace result:** `confirmed`.
`gitops/platform/monitoring/kube-state-metrics.yaml:21-24,35` still grants
`secrets` `list` and `watch`; the Deployment container at `:112-137` still
declares no `args` and still pins `v2.14.0` at `:114`.
`infrastructure/bootstrap-local.sh:246-248` still installs Argo CD with no
`--version`. Ten `gitops/apps/root/*.yaml` files plus
`gitops/clusters/local/root-application.yaml:10` and
`applicationset-apps.yaml:20` still track `targetRevision: main`.

**New repository-static finding.** A repository-wide search for `kube_secret_`
returns zero matches in any tracked Grafana dashboard, Prometheus rule, or alert
configuration; only this pack's own documents mention the string
(`CLM-WERPC-011-39`). That closes the in-repository half of the consumer-need
sub-claim. It cannot close the claim outright, because
`gitops/platform/monitoring/kube-state-metrics.yaml:3` states the real consumer
is an external Docker-hosted Prometheus outside this repository's tracked paths,
whose query set stays `DEFER`.

**Status effect:** `no-change` (`CLM-WERPC-011-08`). `REQ-WERPC-008` keeps
`Partial`. Two fired triggers and one partially closed sub-claim are a recorded
delta, not a promotion: effective RBAC, admission enforcement, controller
reconciliation, and immutable delivery identity remain unobservable from the
repository.

**Blocking class:** `live-cluster`, structurally unreachable, with a
`repo-static` remainder for the consumer-need sub-claim and a `human-judgement`
remainder for the immutable-identity design decision. Reopens for the two fired
triggers by admitting a targeted version and facility refresh; the remaining
sub-claims reopen only with operator-authorized live evidence or an approved
design decision.

#### REQ-WERPC-009 re-observation

**External result:** `unchanged`, and this row has no pinned primary source
registered in the ledger, so there is nothing to re-check as changed or
unchanged. It has always rested on repository-static evidence.

**Workspace result:** `confirmed`. `infrastructure/README.md:106-110` still
separates the static contract verifier from the five documented live verifiers.
`infrastructure/k3d/k3d-cluster.yaml:5,12,15` still pins
`rancher/k3s:v1.35.0-k3s1` with host ports `80:80` and `443:443`.

**Status effect:** `no-change` (`CLM-WERPC-011-09`).

**Blocking class:** `live-cluster`, structurally unreachable. The static and live
boundary itself is confirmed, but effective cluster, gateway, registry, and cloud
state require an operator-authorized live check. Reopens when an operator
authorizes a live observation or a named selector changes.

**Version drift with no ledger home.** `infrastructure/k3d/k3d-cluster.yaml:5`
pins `rancher/k3s:v1.35.0-k3s1` while upstream has shipped `v1.35.5`, `v1.35.6`,
and a `v1.36.X` line. Because `REQ-WERPC-009` has no registered external source
row, this drift has no source-row home in this pack; it reinforces the
2026-08-12 note recorded earlier in this report. If this row ever acquires a
dedicated source row, this delta should be its first admitted trigger.

#### REQ-WERPC-025 re-observation

**External result:** `changed` (`SRC-WERPC-085`), sharing the Argo CD
`sourceIntegrity` GA change with `REQ-WERPC-008`, which bears directly on this
row's Git, chart, and image identity gap. All other pinned security sources
re-verified `unchanged`: the Kubernetes Secrets page still states etcd storage is
unencrypted by default, Pod Security Admission is unchanged, RBAC good practices
still warn that Secret `list` and `watch` reveal contents, the Vault Kubernetes
auth documentation still describes TokenReview with an `audience` role field, and
Cosign keyless verification is unchanged.

**Workspace result:** `confirmed`.
`gitops/platform/eso/vault-secret-store.yaml:18-24` still declares Kubernetes
auth with a `serviceAccountRef` and an `audiences` block.
`gitops/workloads/adminer/rollout.yaml:19-49` still declares no
`serviceAccountName`, no `automountServiceAccountToken`, and no pod or container
`securityContext`. No Pod Security Admission labels, admission policies, or
Gatekeeper constraints exist under `gitops/`, `policy/`, or `infrastructure/`.

**Status effect:** `no-change` (`CLM-WERPC-011-25`). `REQ-WERPC-025` keeps
`Partial`.

**Blocking class:** `live-cluster`, structurally unreachable, with
`human-judgement` remainders for the admission-architecture and trust-policy
design decisions and a `provider-runtime` remainder for external Vault role,
version, and audience alignment. None is closable by repository-static work.

#### 2026-08-18 correction to the 2026-08-17 kube-state-metrics statement

The 2026-08-17 external result above originally stated that upstream added a
`serviceaccounts` resource that was absent at `v2.14.0`. **That statement was
wrong and is withdrawn** (`CLM-WERPC-012-01`). Both tags' shipped
`examples/standard/cluster-role.yaml` were retrieved and diffed directly on
2026-08-18 (`SRC-WERPC-090`): the `v2.14.0` and `v2.19.1` files are byte-identical
except the `app.kubernetes.io/version` label. `serviceaccounts` was already
present at `v2.14.0`, and upstream has not changed its shipped ClusterRole rules
anywhere in this range.

The correction changes what the finding is. The divergence is not upstream adding
a resource; it is that this repository's hand-curated `ClusterRole` at
`gitops/platform/monitoring/kube-state-metrics.yaml:14-71` has always been a
trimmed subset of the upstream standard role. Relative to upstream at either tag
it omits `serviceaccounts`, `authentication.k8s.io/tokenreviews`,
`authorization.k8s.io/subjectaccessreviews`,
`certificates.k8s.io/certificatesigningrequests`,
`discovery.k8s.io/endpointslices`, `coordination.k8s.io/leases`, the four
`rbac.authorization.k8s.io` resources, and `networking.k8s.io/ingressclasses`.

Two of those omissions matter now rather than after any upgrade
(`CLM-WERPC-012-02`). `certificates.k8s.io/certificatesigningrequests` and
`coordination.k8s.io/leases` are documented **default** resources, collected
without any `--resources` flag, and were default at `v2.14.0` as well. The
deployment passes no `args:`, so those two collectors have been running without
the permissions they require for as long as the current pin has been in place.
This is a live pre-existing defect, not an upgrade consequence.

Exactly one RBAC requirement is introduced by upgrading (`CLM-WERPC-012-03`).
Version `v2.18.0` replaced `endpoints` with `endpointslices` in the default
resource set. Because no `args:` are declared, the new image default takes effect
silently and no Deployment-spec diff would reveal it, so
`discovery.k8s.io/endpointslices` `list`/`watch` must be granted or `--resources`
must be set explicitly to retain `endpoints`. A repository-wide search for
`kube_endpoints_` returns zero matches outside this pack, so no tracked
dashboard, rule, or alert consumes the metrics that would stop being emitted; the
external Docker-hosted Prometheus named at
`gitops/platform/monitoring/kube-state-metrics.yaml:3` remains outside tracked
paths and its query set stays `DEFER`.

Currency note (2026-09-14): `gitops/platform/monitoring/kube-state-metrics.yaml`
now pins `v2.19.1`, so the `v2.14.0` pin described in this and the preceding
dated observations is historical. The compatibility gap stated below closed
with that change; the Secret `list`/`watch` grant is a separate finding.

A further currency observation, recorded without action (`CLM-WERPC-012-04`): the
pinned `v2.14.0` ships client-go `v1.31` while
`infrastructure/k3d/k3d-cluster.yaml:5` declares k3s `v1.35.0-k3s1`. Upstream
documents `v2.19.x` as the line supporting client-go `v1.35`. The current pin is
therefore already outside the documented compatibility matrix by four minor
versions; upstream states neither that it works nor that it breaks, and actual
behavior against this cluster remains `live-cluster` blocked.

#### Historical sources

The dated baseline primary-source rows are `SRC-WERPC-023` through
`SRC-WERPC-034`, and the admitted gap-only rows are `SRC-WERPC-060` through
`SRC-WERPC-065`, in
the [source register](m0012-source-coverage.md#source-register).
The first range was checked 2026-08-08; the second was checked 2026-08-10 and
covers only kube-state-metrics Secret RBAC/metrics, Adminer token and hardening,
and immutable Git/chart/image and verifiable-artifact distinctions. Product and
version limitations and refresh triggers are part of each row. Predecessor
documents remain dated provenance until WERPC-008; their current findings were
reconciled here without rewriting historical claims.

#### Historical review and freshness

Refresh this reference when Kubernetes/k3s, Argo CD, ESO, Vault, CNI,
admission/policy, GitOps root/AppProject, secret transport, image/release, or
external-gateway design changes. Also refresh the admitted rows when the
kube-state-metrics version/collector arguments/metric consumers/RBAC scope,
Adminer image/ServiceAccount/security context, Argo version or source-integrity
configuration, Git revision policy, Helm chart/provenance handling, image
digest, signature/attestation tooling, or trust policy changes. Recheck the
current primary sources before a policy decision. The required deferred
observations must remain distinct even if a local static validator passes.

#### 2026-08-11 Partial/DEFER incremental refresh

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

#### 2026-08-14 consistency and Partial re-observation

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

#### 2026-08-20 full-corpus reverification

This increment consumes the reviewed platform/security report at workspace
baseline `8d8c8e5634fe939f8daaf041fbf5dfb444ed4a9c` and its exact allocation
slice. Kubernetes desired state, infrastructure execution contracts, and
security controls remain separate evidence layers. No cluster, container
runtime, registry, Argo CD, Helm, Vault, ESO, gateway, or cloud command was
run; no Secret value, credential, token, trust store, artifact, signature,
attestation, or recovery output was inspected.

#### REQ-WERPC-008 Kubernetes desired state

- **Sources and result:** `unchanged` / `drifted`, using existing
  `SRC-WERPC-060`, `SRC-WERPC-061`, and `SRC-WERPC-090`, plus selector
  `m0007-kubernetes-infrastructure-and-security.md#kubernetes-baseline`.
  `CLM-WERPC-013-04` records the current repository-static correction. The
  v2.19.1 upstream role retains the Secret authorization boundary documented
  at v2.14.0; metadata-oriented exported metrics do not narrow the underlying
  Kubernetes API permission.
- **As-Is:** `gitops/platform/monitoring/kube-state-metrics.yaml:21-34`
  declares `secrets` with `list` and `watch`, while `:70-89` declares the
  current default collector permissions and `:124-160` binds the dedicated
  ServiceAccount to image `v2.19.1` with hardened pod/container fields. The
  six exact manifests under `gitops/platform/network-policies/` still declare
  Egress-only policy intent. `gitops/platform/namespaces/namespace-monitoring.yaml:7-10`
  declares Restricted Pod Security labels. These selectors describe desired
  state, not observed authorization, admission, CNI, scrape, or workload state.
- **Gap / Target:** the owner previously described the v2.14.0 pin and must
  reflect v2.19.1 without presenting the upgrade as runtime evidence. Preserve
  the declared Secret-read risk, explicit collector/RBAC review, and the
  NetworkPolicy/Pod Security intent; require separately authorized effective
  RBAC, API admission, CNI flow, Argo reconciliation, and scrape-consumer
  observations before asserting enforcement or necessity.
- **Evidence / rejected inference:** official public documentation plus exact
  repository selectors, evidence depth `repository-static`. A ClusterRole,
  namespace label, hardened workload, or Egress policy proves no actual Secret
  read, metric exposure, admission decision, selected traffic isolation, or
  reconciled pod. The external Prometheus query set remains outside tracked
  paths.
- **Disposition / retained boundary:** `Partial`, blocking class
  `live-cluster`. Effective authorization, Secret-safe scrape evidence,
  admission/CNI behavior, and controller reconciliation remain `DEFER`.
- **Owner / safe follow-up / trigger:** Kubernetes/observability owners with
  platform and security review. A separately authorized read-only observation
  may inspect effective RBAC, admission, CNI, and non-secret metric metadata;
  reopen on a kube-state-metrics version, collector/RBAC, NetworkPolicy,
  namespace-admission, cited source, or owner-selector change.

#### REQ-WERPC-009 Infrastructure and GitOps execution boundary

- **Sources and result:** `changed` / `drifted`, using new
  `SRC-WERPC-091` with existing `SRC-WERPC-027`, `SRC-WERPC-032`, and
  `SRC-WERPC-064`, plus selector
  `m0007-kubernetes-infrastructure-and-security.md#infrastructure-baseline`.
  `SRC-WERPC-091` is only official K3s v1.35 release-family context;
  `CLM-WERPC-013-05` records the static infrastructure delta.
- **As-Is:** `infrastructure/k3d/k3d-cluster.yaml:5,8-17` declares
  `rancher/k3s:v1.35.0-k3s1`, the API host port, and HTTP/HTTPS load-balancer
  mappings. `infrastructure/bootstrap-local.sh:246-253` now pins the Argo CD
  Helm chart to `10.4.0`. `gitops/clusters/local/root-application.yaml:10`,
  `gitops/clusters/local/applicationset-apps.yaml:20`, and Git-sourced owners
  under `gitops/apps/root/` continue to select moving branch `main`.
  `infrastructure/README.md#infrastructure-test-inventory` keeps the static
  contract verifier distinct from the cluster-dependent verification suite.
- **Gap / Target:** a pinned chart version is not Helm provenance, a moving Git
  branch is not immutable revision identity, and a tagged image is not an
  observed registry digest. Keep bootstrap inputs and static/live test
  contracts current, then require an approved design for immutable revision,
  chart provenance, image identity, trust policy, and Git-revert-first recovery
  before any enforcement claim.
- **Evidence / rejected inference:** official public release, GitOps, Helm,
  image, SLSA, and SSDF material plus repository-static selectors. The K3s
  release family does not prove patch suitability, image pull, cluster
  creation, gateway reachability, Argo fetch/render/sync, registry content, or
  recovery. A version pin, digest, signature, attestation, and SLSA provenance
  are distinct identities or statements and are never equivalent by presence.
- **Disposition / retained boundary:** `Partial`, blocking class
  `live-cluster`. Cluster, gateway, controller, rendered-resource, registry,
  hosted, cloud, and recovery results remain `DEFER`.
- **Owner / safe follow-up / trigger:** Infrastructure and GitOps owners, with
  delivery/security and platform-operations review. A later operator-approved
  observation may collect exact revision, render, sync/health, registry
  identity, and recovery evidence without credential or Secret payloads;
  reopen on a K3s, Argo CD, Helm, SLSA, SSDF, k3d, bootstrap, chart, image,
  targetRevision, or recovery-contract change.

#### REQ-WERPC-025 Security controls and recovery evidence

- **Sources and result:** `unchanged` / `drifted`, using existing
  `SRC-WERPC-025`, `SRC-WERPC-026`, `SRC-WERPC-028`, `SRC-WERPC-062`, and
  `SRC-WERPC-065`, plus selector
  `m0007-kubernetes-infrastructure-and-security.md#security-baseline`.
  `CLM-WERPC-013-06` records the current Adminer hardening observation.
- **As-Is:** `gitops/workloads/adminer/rollout.yaml:19-50` now declares
  non-root UID/GID, `RuntimeDefault` seccomp, disabled privilege escalation,
  and dropped capabilities, while still omitting `serviceAccountName` and
  `automountServiceAccountToken` and intentionally deferring a read-only root
  filesystem. `gitops/platform/namespaces/namespace-apps.yaml:6-8` declares
  Baseline audit/warn, not enforcement. `gitops/platform/eso/vault-secret-store.yaml:12-25`
  declares the local-only Vault endpoint, KV v2, Kubernetes auth role,
  ServiceAccount identity, and `vault` audience; the matching
  `gitops/platform/eso/vault-token-reviewer-binding.yaml:1-14` declares the
  TokenReview binding. `policy/conftest/kubernetes.rego:1-67` remains a static
  pre-merge policy, not API admission.
- **Gap / Target:** the workload fields align with Kubernetes hardening
  guidance but do not establish image compatibility, effective
  ServiceAccount/RBAC, token use, admission, or runtime posture. Vault/ESO
  declarations do not establish role alignment, backend health,
  ExternalSecret reconciliation, Secret encryption/rotation, or consumer
  reload. The bounded tree contains no accepted artifact digest, Helm
  provenance, Cosign verification, attestation, SLSA provenance, or Argo source
  integrity result. Preserve these as separate controls with explicit trust
  roots, identity expectations, fail-closed policy, rollback, and evidence
  owners.
- **Evidence / rejected inference:** official Kubernetes, Gatekeeper,
  ESO/Vault, Sigstore, SLSA, GitHub, and NIST material plus repository-static
  selectors, evidence depth `repository-static`. Hardened YAML, an audit/warn
  label, TokenReview binding, Vault role name, static Rego, signature, or
  attestation proves no admission decision, effective access, backend state,
  artifact trust, conformance, or recovery capability.
- **Disposition / retained boundary:** `Partial`, blocking class
  `live-cluster`. Admission, effective identity/RBAC, Vault/ESO conditions,
  Secret storage/rotation, registry artifact, trust-policy acceptance, and
  recovery effectiveness remain `DEFER`.
- **Owner / safe follow-up / trigger:** Security owner with Kubernetes,
  delivery, Vault, and recovery owners. A separately authorized secret-safe
  observation may collect admission decisions, effective identities,
  readiness metadata, artifact-verifier results, and a controlled recovery
  exercise; it must never collect Secret values or credential material. Reopen
  on a Kubernetes, ESO, Vault, Gatekeeper, Argo CD, Sigstore, SLSA, GitHub,
  NIST, Adminer, identity/admission, trust-policy, artifact-flow, or recovery
  change.

#### 2026-08-23 reconciliation and workload-identity increment

The current [Argo CD automated-sync contract](https://argo-cd.readthedocs.io/en/stable/user-guide/auto_sync/)
preserves an important trigger boundary: a live-cluster change alone does not
cause another automated synchronization for an already synchronized Git
revision unless automated self-heal is enabled. The tracked Applications'
`selfHeal: true` fields are repository-static desired state only. They do not
prove the controller observed drift, retried, pruned, reconciled, or restored
health; revision identity, sync/health status, and recovery behavior remain
`DEFER` pending separately authorized live evidence.

Kubernetes' current [ServiceAccount guidance](https://kubernetes.io/docs/concepts/security/service-accounts/)
continues to favor dedicated identities, least-privilege authorization, and
short-lived projected tokens obtained through TokenRequest over long-lived
credentials. Its [declarative-management guidance](https://kubernetes.io/docs/tasks/manage-kubernetes-objects/declarative-config/)
describes managing object configuration from files, but applying desired state
does not prove effective RBAC, token audience or lifetime, admission, rollout,
or workload behavior. The existing ServiceAccount, token-automount, and RBAC
gaps therefore keep their `Partial`/`DEFER` disposition; this increment does
not authorize a manifest or live-cluster change.

The immutable-reference, signature, and attestation boundary is also
unchanged. A Git revision, chart version, image digest, signature, provenance
statement, verifier policy, and admission result remain distinct evidence
classes; no registry object, trust decision, reconciliation, or runtime result
was inspected.

#### 2026-09-05 external-source reverification

This increment re-observed the Kubernetes, infrastructure, and security owners
under the approved 2026-09-05 follow-on cycle. Workspace re-observation was
excluded by direct user decision, so no declared image tag, chart version,
manifest field, or policy label was re-read and no live system was contacted.
New sources are `SRC-WERPC-143` through `SRC-WERPC-146`; the cycle claims are
`CLM-WERPC-016-13` and `CLM-WERPC-016-14`.

#### REQ-WERPC-008 Kubernetes re-observation

- **Sources and external result:** `changed` for currency, `unchanged` for
  semantics. The network-policy, secret, pod-security admission and standards,
  admission-controller, role-based access, secret-handling, and service-account
  documentation were all re-observed as `unchanged`; the default-deny selection
  model, the unencrypted-at-rest default, the three policy levels and three
  modes, and the warning that list and watch access effectively reveal secret
  contents all hold. Currency moved: a new upstream minor released on
  2026-08-26, three days after this reference's most recent increment, so the
  supported set has shifted and the previously pinned line is now the oldest
  supported minor with the nearest end-of-life date
  ([SRC-WERPC-143](m0012-source-coverage.md#2026-09-05-external-source-reverification)).
  The log-collection agent's upstream release is now several minor versions
  beyond the pin this reference records, quantifying a gap that was previously
  stated only as a pin
  ([SRC-WERPC-146](m0012-source-coverage.md#2026-09-05-external-source-reverification)).
  The metrics collector and reconciliation controller releases already registered
  on 2026-08-28 were re-observed as `unchanged` and remain current.
- **Workspace selector and result:** `not observed in this cycle`. The
  [Kubernetes baseline](#kubernetes-baseline) retains its earlier
  repository-static observation date.
- **As-Is, gap, and target:** the row stays `Partial`. No promotion. Version
  currency is a review trigger only; this cycle performs no compatibility
  assessment and recommends no upgrade.
- **Evidence boundary:** blocking class and retained boundary remain
  `live-cluster` / `DEFER`. Upstream release pages prove that a version exists,
  never that it is deployed, compatible, reconciled, or running here.
- **Owner, safe follow-up, and trigger:** owner is this reference and the Stage
  05 platform owners. The safe follow-up is a workspace-observation cycle that
  re-reads the declared pins before any upgrade proposal. Refresh on any further
  upstream release or support-window change.

#### REQ-WERPC-009 infrastructure re-observation

- **Sources and external result:** `changed` for currency, `unchanged` for
  semantics. Automated-sync, self-heal, bootstrap, tracking-strategy, and
  source-integrity documentation were re-observed as `unchanged` in substance,
  and the field names for the source-integrity policy were captured for the
  first time. The node distribution has shipped further patches on the pinned
  line and a newer line, and a further line is at release-candidate stage, so
  the drift recorded on 2026-08-17 has widened
  ([SRC-WERPC-144](m0012-source-coverage.md#2026-09-05-external-source-reverification)).
  The secret-management operator's current release and its version-gated Vault
  audience requirement were captured for the first time
  ([SRC-WERPC-145](m0012-source-coverage.md#2026-09-05-external-source-reverification)).
- **Workspace selector and result:** `not observed in this cycle`. The
  [infrastructure baseline](#infrastructure-baseline) retains its earlier
  repository-static observation date.
- **As-Is, gap, and target:** the row stays `Partial`. No promotion. The
  operator release figure is new evidence with no earlier pinned figure to
  compare against, so it establishes a baseline rather than a drift.
- **Evidence boundary:** blocking class and retained boundary remain
  `live-cluster` / `DEFER`. Declared reconciliation intent is not observed sync,
  health, recovery, or rollback.
- **Owner, safe follow-up, and trigger:** owner is this reference and the Stage
  05 platform owners. Refresh on any further release, or on a change to the
  provider authentication fields.

#### REQ-WERPC-025 security re-observation

- **Sources and external result:** `unchanged`. The secret-authorisation and
  least-privilege guidance, the service-account token model, the workload
  hardening checklist, the provenance mechanism, the supply-chain specification
  at its current approved version, the signature and attestation verification
  surface, and the secure-development, cybersecurity-framework, and control
  catalogue publications were all re-observed as `unchanged`, with one patch
  release noted in the control catalogue family. Two link-rot candidates raised
  during collection were rejected: the retained bootstrap and attestation
  citations already use their current paths.
- **Workspace selector and result:** `not observed in this cycle`. The
  [security baseline](#security-baseline) retains its earlier repository-static
  observation date.
- **As-Is, gap, and target:** the row stays `Partial`. No promotion, and no
  named gap closes. The external control basis is stable, so the retained gaps
  remain local-evidence gaps rather than external-uncertainty gaps.
- **Evidence boundary:** blocking class and retained boundary remain
  `live-cluster` / `DEFER`, with `secret-value` operations prohibited outright.
  No secret was read, no cluster was contacted, and no policy enforcement was
  observed.
- **Owner, safe follow-up, and trigger:** owner is this reference and the Stage
  05 security owners. Refresh when any cited control publication is revised, or
  when a separately authorised evidence class admits live verification.

## Related Documents

- [CI/CD and QA](m0008-ci-cd-github-actions-and-qa.md)
- [Source coverage and migration ledger](m0012-source-coverage.md)
- [GitOps overview](../../../../gitops/README.md)
- [Infrastructure overview](../../../../infrastructure/README.md)
- [ArgoCD ESO Vault recovery runbook](../../../05.operations/runbooks/0002-argocd-eso-vault-recovery-runbook.md)
- [Operations policies](../../../05.operations/policies/README.md)
