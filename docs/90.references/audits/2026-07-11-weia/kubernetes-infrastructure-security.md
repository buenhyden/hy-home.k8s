---
title: 'Audit: Kubernetes Infrastructure and Security'
type: content/reference
status: draft
owner: platform
updated: 2026-07-11
---

# Audit: Kubernetes Infrastructure and Security

## Overview

이 보고서는 Current Kubernetes·infrastructure·security 연구 기준을 고정된
repository snapshot의 GitOps desired state, 정적 검증, 운영 절차와 대조한
dated implementation audit다. 26개 통제를 desired-state 기반 12개와
`SEC-001`~`SEC-014` 재조정 14개로 나누어 평가한다. 두 집합은 같은 결함을
중복 점수화하지 않는다. 원하는 상태와 검증 스크립트가 존재한다는 사실은
live Kubernetes, Argo CD, Vault, ESO, NetworkPolicy 또는 TLS enforcement를
증명하지 않는다.

## Purpose

- GitOps 소유권, Kustomize 구성, Application/AppProject/ApplicationSet 경계와
  environment·rollback 계약을 평가한다.
- RBAC, Vault/ESO, secret transport, NetworkPolicy, policy-as-code, image와
  admin-equivalent 경계를 정적 증거와 live 증거로 분리한다.
- Current 연구의 `SEC-001`~`SEC-014`를 현재 audit method로 재평가하고 하나의
  후속 SDLC 소유자와 측정 가능한 acceptance evidence로 연결한다.
- Task 12가 통합 우선순위를 만들 수 있도록 점수, 분포, 의존 관계를 제공한다.

## Reference Type

- Type: dated-implementation-audit
- Audit observation SHA: `a85df194bbb8ebc61187b905afaef7f95215cc2f`
- Observation date: `2026-07-11`
- Research cutoff: `2026-07-10 10:00 KST`
- Refresh trigger: GitOps topology, AppProject/RBAC, bootstrap, Vault/ESO,
  NetworkPolicy, policy, image, validator, live-test, or platform supply-chain
  evidence change.

## Authority Boundary

- **Authoritative for**:
  - The 26 report-local controls and repository evidence at the audit observation
    SHA.
  - The score arithmetic, maturity/verdict/confidence distributions, and
    `SEC-001`~`SEC-014` reconciliation in this dated report.
  - Non-mutating recommendations and follow-up routes for Task 12.
- **Not authoritative for**:
  - Active manifests, scripts, CI, policy, operations, credentials, secrets, or
    cluster configuration.
  - Kubernetes API acceptance, Argo CD reconciliation, Vault/ESO runtime,
    NetworkPolicy packet enforcement, TLS trust, registry identity, remote
    workflow behavior, or deployment readiness.
  - Permission to bootstrap, sync, rollback, rotate, patch, push, merge, or
    perform any other active or live change.

Canonical active owners remain `gitops/`, `infrastructure/`, `policy/`,
`scripts/`, `.github/`, and Stage 05 Operations. Repository claims below are
read from the audit observation SHA, not the evolving branch `HEAD`.

## Scope

In scope are the local desired-state hierarchy, Kustomize ownership,
Application/AppProject/ApplicationSet declarations, environment and recovery
contracts, ESO/Vault identity and secret flow, RBAC, transport, NetworkPolicy,
policy-as-code, manifest/image controls, and security-relevant supply-chain
impact. Live operations, secret values, credentials, controller state, packet
probes, remote GitHub settings/runs, and active remediation are excluded.

### Evidence Boundary

| Evidence lane | Evidence read at the observation SHA | What it can establish | What remains excluded |
| --- | --- | --- | --- |
| Desired state | `gitops/**`, Vault HCL, Kustomize, AppProjects, Applications, ApplicationSet, ESO, and NetworkPolicy manifests | Versioned intent, declared ownership, and exact configured fields | API/CRD acceptance, generation, reconciliation, authorization, delivery, or packet behavior |
| Deterministic repo-static | GitOps structure, YAML parse, secret scan, policy fallback, static contracts, repo-quality and declared CI selection | The explicit parser, inventory, pattern, and policy assertions for the fixed tree | Full render/schema/admission, runtime health, TLS trust, secret correctness, or live authorization |
| Optional tooling | Kube-linter and Conftest paths with named SKIP/fallback behavior | Only the tool actually executed and its configured rules | Optional-tool execution when absent, excluded rules, or runtime admission |
| Operator/live | `infrastructure/tests/**` and Stage 05 procedures | Only a separately approved, executed, time-bound observation | No live command ran for this audit; no readiness is inferred |
| Remote/supply chain | [Task 9 delivery and supply-chain owner](ci-qa-automation-pipeline-workflow.md#supply-chain-automation-controls) | Its fixed-tree workflow and relevance decisions | Remote runs, rulesets, dependency resolution, artifact trust, or release integrity |

## Definitions / Facts

### Fixed Snapshot Topology

At the observation SHA, `gitops/**` contains 79 YAML files and 12
`kustomization.yaml` files. The tracked Argo CD topology contains 19
`Application` objects, one `ApplicationSet`, and two `AppProject` objects.
The root Kustomization includes the root Application, two projects, and the
workload generator; the platform root Kustomization lists 18 platform
Applications. There are six tracked egress-focused `NetworkPolicy` objects.
These are repository file/object counts, not live resource counts.

The desired secret path is Vault -> `ClusterSecretStore/vault-backend` ->
`ExternalSecret` -> generated Kubernetes Secret. The checked GitOps and
infrastructure YAML surfaces contain no tracked `kind: Secret` object. This
does not establish etcd encryption, generated Secret access, delivery,
rotation, or runtime correctness.

## GitOps and Platform Foundation Controls

These controls score implemented desired-state foundations that are not the
corrective finding owned by a `SEC-*` row. Runtime shortcomings such as
health/sync depth, TLS trust, network behavior, and admin-equivalent access are
scored only in the corresponding SEC row.

| ID | Benchmark | Expected control | Repository evidence | Maturity | Verdict | Confidence | Gap | Recommendation | Priority | Follow-up owner | Acceptance evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PLAT-001 | [Current platform/security research](../../research/2026-07-07-wer/kubernetes-infrastructure-security.md); OpenGitOps | One declarative root owns platform desired state through an explicit project, source, destination, and versioned path. | `root-application.yaml` names `root-platform`, project `platform`, path `gitops/apps/root`, revision `main`, and the cluster-local destination; the structure gate asserts the hierarchy. | 3 deterministic local+CI enforcement | Implemented | Verified repo-static | No missing repository-static root-owner element; pull/reconcile behavior is excluded here and assessed by SEC-004. | Preserve one root owner and its deterministic hierarchy fixtures. | N/A — no action | N/A — no action | N/A — no action |
| PLAT-002 | Current research; Argo CD ApplicationSet | Workload discovery has one bounded generator, project, source family, and namespace rather than sharing platform ownership. | `apps-generator` discovers only `gitops/workloads/*`, renders into project `apps` and namespace `apps`; the structure gate asserts those exact fields. | 3 deterministic local+CI enforcement | Implemented | Verified repo-static | No missing static discovery boundary; generated Applications and controller discovery remain live-excluded. | Preserve the platform/workload owner split and exact generator fixture. | N/A — no action | N/A — no action | N/A — no action |
| PLAT-003 | Kubernetes Kustomize; Current research | Every Kustomize root parses, every sibling manifest is referenced, and ownership can be rendered for review. | The structure gate parses all 12 tracked Kustomizations and rejects unreferenced sibling YAML; manifest validation parses the broader YAML target set. | 3 deterministic local+CI enforcement | Implemented | Verified repo-static | No missing parse/completeness control; full root render/schema depth is owned by SEC-011. | Keep parse and sibling-completeness checks as the fast foundation. | N/A — no action | N/A — no action | N/A — no action |
| PLAT-004 | Kubernetes RBAC/AppProject least privilege; Current research | Workloads use a narrow source, destination, namespaced-kind list, no cluster kinds, and read-only project role. | `apps` permits one repository, only namespace `apps`, eight exact namespaced kinds, no cluster kinds, and `applications get` for `apps/*`; wildcard and unused-kind checks are deterministic. | 3 deterministic local+CI enforcement | Implemented | Verified repo-static | No missing tracked workload project restriction; live Argo CD authorization is excluded. | Preserve exact allow-lists and negative fixtures when onboarding a new workload kind. | N/A — no action | N/A — no action | N/A — no action |
| PLAT-005 | Argo CD AppProject; Current research | Platform permissions enumerate required sources, destinations, cluster kinds, and namespaced kinds without wildcard expansion. | `platform` enumerates nine sources, 11 destination namespaces, nine cluster kinds, and 18 namespaced kinds; policy rejects wildcard group/kind and the local role is read-only. | 3 deterministic local+CI enforcement | Implemented | Verified repo-static | Static enumeration is present; the `argocd` admin-equivalent destination and remote principals are assessed only by SEC-014. | Preserve enumeration and require separate security review for every source, destination, or kind expansion. | N/A — no action | N/A — no action | N/A — no action |
| PLAT-006 | OpenGitOps continuous reconciliation; Argo CD declarative sync | Root and generated workloads declare automated prune/self-heal intent without claiming execution. | Both the root Application and ApplicationSet template set `automated.prune: true` and `selfHeal: true`; the observation contains no controller result. | 2 repository-static | Implemented | Verified repo-static | No missing declaration; health, sync, drift, prune, and self-heal execution are deliberately outside this desired-state row. | Keep configured intent distinct from SEC-004 runtime assertions. | N/A — no action | N/A — no action | N/A — no action |
| PLAT-007 | Current GitOps policy and environment boundary | The local environment, namespace ownership, destination limits, external-runtime boundary, and no-auto-create rule are explicit and statically enforced. | Stage 05 policy limits scope to local WSL2, `gitops/README.md` assigns owners, AppProjects enumerate namespaces, and policy/static checks reject `CreateNamespace=true`. | 3 deterministic local+CI enforcement | Implemented | Verified repo-static | No missing current local boundary; this audit does not infer a dev/stage/prod promotion system. | Preserve the single-local-environment contract until a separate environment design is approved. | N/A — no action | N/A — no action | N/A — no action |
| PLAT-008 | Stage 05 recovery runbooks; GitOps rollback | Recovery paths capture pre-state, retain Git as desired-state owner, define break-glass limits, rollback, and post-recovery verification. | The platform bootstrap and Argo CD/ESO/Vault recovery runbooks document history/rollback, snapshots, operator-bound sync, break-glass EndpointSlice handling, and static/live rechecks; no rehearsal evidence exists at this SHA. | 1 documented/routed | Partial | Unverified live | Complementary: procedures exist but no time-bound rollback/recovery exercise proves sequencing, secret redaction, or restored reconciliation. | Rehearse one approved non-secret recovery scenario, capture timestamps and redacted results, then close any procedure mismatch through the active runbook owner. | P2 planned improvement | New Stage 04 Task: platform-recovery-rehearsal | A Task records pre-state, selected failure, operator approvals, rollback command/result, Argo CD/ESO recovery criteria, redaction check, elapsed time, and post-recovery static/live evidence for one revision. |
| PLAT-009 | Audit method; Current static/live boundary | Each parser, optional tool, CI declaration, and live script has a named claim boundary so a static PASS cannot become readiness. | Script output distinguishes optional SKIP/fallback, `scripts/README.md` defines exit semantics, Stage 05 owns operator checks, and this audit records no live execution. | 2 repository-static | Implemented | Verified repo-static | No missing evidence classification in the audited owners; individual assertion weaknesses are scored in SEC-003 through SEC-005 and SEC-010. | Continue recording exact command/tool and excluded lanes with every future evidence claim. | N/A — no action | N/A — no action | N/A — no action |
| PLAT-010 | Kubernetes Secrets guidance; Current secret benchmark | Tracked desired state avoids plaintext Secret objects and routes secret material through one purpose-specific external-store identity without inspecting values. | The policy fallback rejects `apiVersion: v1`, `kind: Secret`; the scanner rejects sensitive literals/`stringData`; ESO references `vault-backend`; its ServiceAccount has the `system:auth-delegator` TokenReview binding; no tracked Secret object appears on checked GitOps/infrastructure YAML surfaces. | 3 deterministic local+CI enforcement | Implemented | Verified repo-static | Repository leak prevention and purpose-specific desired identity are implemented; storage, live RBAC, transport, argv, delivery, and rotation remain separate SEC concerns. | Preserve value-free static evidence, external-store ownership, and the narrow TokenReview identity. | N/A — no action | N/A — no action | N/A — no action |
| PLAT-011 | Vault least privilege; Current research | ESO policy grants only named KV-v2 paths and necessary capabilities, with broad platform data wildcard rejected. | `eso-read.hcl` names data/metadata paths for three logical platform secrets with `read`/`list`; static contracts require them and reject `secret/data/platform/*`. | 2 repository-static | Implemented | Verified repo-static | The HCL is narrow, but SEC-001 shows that Vault HCL changes do not select the specialist CI lanes, so deterministic local+CI maturity is not awarded; upload, role attachment, token TTL/capability, audit, and rotation remain unverified live. | Preserve exact paths/capabilities; SEC-001 owns CI selection remediation and operator evidence remains separate. | N/A — no action | N/A — no action | N/A — no action |
| PLAT-012 | Kubernetes image hygiene; Current policy benchmark | Tracked container images reject explicit `:latest` in deterministic policy while stronger identity remains separately assessed. | Rego and the always-run Python fallback reject container/init-container `:latest`; observed explicit image references use non-`latest` tags. | 3 deterministic local+CI enforcement | Implemented | Verified repo-static | Mutable tag/digest/signature/provenance concerns are not hidden; their security architecture impact remains in SEC-013. | Preserve the non-`latest` baseline without presenting it as immutable image identity. | N/A — no action | N/A — no action | N/A — no action |

## SEC Finding Reconciliation Controls

The Current research classification is retained unless a row explicitly says
otherwise. No active owner changed between the research derivation and audit
observation SHA, so no finding is closed or superseded. Maturity scores the
expected control, not the amount of prose or desired state surrounding a gap.

| ID | Benchmark | Expected control | Repository evidence | Maturity | Verdict | Confidence | Gap | Recommendation | Priority | Follow-up owner | Acceptance evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SEC-001 | Current finding: specialist CI path coverage | Every bootstrap, Vault policy, GitOps, infrastructure, and policy change selects its security-relevant static owners, with positive and negative filter fixtures. | At the observation SHA, `repo_quality` omits `infrastructure/bootstrap-local.sh` and Vault HCL; `manifests` covers infrastructure YAML/tests and `policy/**` but omits the bootstrap script and Vault HCL. General pre-commit selection remains. | 1 documented/routed | Partial | Verified repo-static | Implementation gap (High), not superseded: standalone changes can miss the specialist repo-quality/manifest-static evidence lanes. | Define the canonical path-to-validator matrix and add filter fixtures before extending the workflow. | P1 near-term integrity | New Stage 03 Spec: platform-security-validation-evidence-contract | Fixtures prove bootstrap and Vault HCL changes select the approved security/static jobs; unrelated docs do not; CI summary names the executed or skipped owner without weakening general pre-commit. |
| SEC-002 | Current finding: local hook policy depth | Security-relevant edits receive bounded local GitOps structure, policy, and static-contract feedback or an explicit DEFER-to-CI result. | Pre-commit and shared hooks run shell, secret, workflow, and manifest tools but do not directly invoke the custom GitOps structure, policy-gate, or static infrastructure contract bundle. | 1 documented/routed | Partial | Verified repo-static | Needs strengthening (Medium), not superseded: local feedback can be green before specialized repository gates run. | Add a measured changed-surface wrapper or one documented DEFER contract; keep full completion commands authoritative. | P2 planned improvement | New Stage 03 Spec: platform-security-validation-evidence-contract | A latency-budgeted matrix maps every affected platform path to RUN or DEFER, negative fixtures detect omissions, and output distinguishes local PASS from CI-deferred evidence. |
| SEC-003 | Current finding: optional policy/linter tools in `manifest-static` | CI states and enforces the accepted manifest-lint and policy tool set, versions, fallbacks, and evidence labels. | The job installs PyYAML only; manifest validation may SKIP kube-linter and policy always runs the deterministic fallback while Conftest is optional. A separate pre-commit job can install its own hook tools. | 1 documented/routed | Partial | Verified repo-static | Implementation gap (Medium), not superseded: a successful script lane can supply narrower evidence than a tool-complete local run without a prominent contract summary. | Pin the required tools or explicitly approve and surface the fallback contract per job; never label fallback as Conftest/kube-linter evidence. | P1 near-term integrity | New Stage 03 Spec: platform-security-validation-evidence-contract | CI fixtures demonstrate required-tool execution or named fallback/SKIP, versions appear in logs, summaries identify the evidence provider, and no optional-tool absence is reported as that tool's PASS. |
| SEC-004 | Current finding: Argo CD live-state assertion | An approved live check requires intended Applications to be present, `Healthy`, and `Synced`, with bounded transitional states and timeout diagnostics. | `verify-gitops.sh` reads health for nine named Applications but accepts any nonempty value and never asserts sync status. No script was run in this audit. | 1 documented/routed | Partial | Unverified live | Needs strengthening (High), not superseded: `Degraded`, `Progressing`, or out-of-sync state can satisfy the presence-oriented check. | Specify strict and diagnostic modes, expected states, timeouts, and redacted failure evidence before changing the operator test. | P1 near-term integrity | New Stage 03 Spec: platform-live-assurance-modes | Fixtures cover missing, Healthy/Synced, Degraded, Progressing, Unknown, OutOfSync, and timeout cases; an approved canary records strict failure and recovery without mutating desired state ad hoc. |
| SEC-005 | Current finding: TLS live evidence | Required endpoints verify the intended CA chain, hostname, certificate validity, and response; diagnostic bypasses cannot satisfy strict readiness. | `verify-ingress-tls.sh` uses `curl -k`, makes Traefik 443 opt-in, and warns rather than fails for Headlamp/Kiali TLS-secret mismatches. No TLS probe ran here. | 1 documented/routed | Partial | Unverified live | Needs strengthening (High), not superseded: the aggregate suite can pass without chain validation or required endpoint coverage. | Define trust roots and strict/diagnostic modes; require all approved endpoints in strict mode while preserving bounded troubleshooting. | P1 near-term integrity | New Stage 03 Spec: platform-live-assurance-modes | Negative fixtures reject untrusted CA, hostname mismatch, expiry, missing endpoint, and TLS-secret mismatch; an approved strict canary verifies the intended chain for every required endpoint. |
| SEC-006 | Current finding: Vault bootstrap TLS default | Secret-bearing bootstrap verifies Vault TLS by default using an explicit trust root; bypass requires approved, expiring break-glass evidence. | `infrastructure/bootstrap-local.sh` sets `VAULT_SKIP_VERIFY` to `true` by default and `vault_curl` uses `curl -k` on that path. | 0 absent | Gap | Verified repo-static | Implementation gap (High), not superseded: the default removes endpoint authentication during secret-bearing bootstrap. | Do not use the insecure default for the next secret-bearing bootstrap absent approved break-glass; design CA input, secure default, failure mode, and rollback before editing. | P0 immediate safety | New Stage 03 Spec: vault-eso-transport-and-secret-exposure-hardening | Default bootstrap rejects an untrusted/mismatched certificate and succeeds with the approved CA; bypass requires owner, reason, expiry, audit record, and automatic return to verification. |
| SEC-007 | Current finding: ESO-to-Vault transport | ESO authenticates and encrypts its Vault connection with a versioned server identity and trusted CA. | `vault-backend` declares `http://vault-external.platform.svc.cluster.local:8200`; egress NetworkPolicy constrains routes but provides neither confidentiality nor endpoint authentication. | 0 absent | Gap | Verified repo-static | Implementation gap (High), not superseded: in-cluster secret transport has no manifest-declared TLS protection. | Design Vault service identity, CA distribution, ESO provider fields, version compatibility, canary order, and rollback before changing the store. | P1 near-term integrity | New Stage 03 Spec: vault-eso-transport-and-secret-exposure-hardening | A version-pinned canary proves ESO Ready and secret reconciliation over verified TLS, rejects an untrusted endpoint, records CA rotation, and restores the prior revision through GitOps rollback. |
| SEC-008 | Current finding: secret-bearing process arguments | Bootstrap keeps Vault tokens and fetched secret values out of process argv, logs, diagnostics, temporary world-readable files, and retained artifacts. | The bootstrap expands `X-Vault-Token` in curl arguments and the fetched Valkey password in `kubectl --from-literal`; values are not tracked in Git but can be visible to same-host process inspection/capture. | 0 absent | Gap | Verified repo-static | Implementation gap (High), not superseded: current secret handling exposes values at the process boundary. | Do not run the affected secret-bearing path until an approved operator accepts the risk; design protected stdin/file-descriptor flow, cleanup, and redaction tests. | P0 immediate safety | New Stage 03 Spec: vault-eso-transport-and-secret-exposure-hardening | An instrumented test captures argv, environment, stdout/stderr, temp paths, and cleanup and finds zero secret values; failure and interrupt cases remove protected material and retain only redacted metadata. |
| SEC-009 | Current finding: Vault audience compatibility | The deployed Vault/ESO/Kubernetes auth version contract defines the required service-account token audience and proves auth remains valid through one bounded secret-rotation/reconciliation event. | `vault-backend` has no `audiences`; the cutoff ESO guidance makes the requirement Vault-version-sensitive, while deployed versions, live auth, delivery, and rotation were not observed. | 1 documented/routed | Partial | Unverified live | Unverified (High), not superseded: repository evidence cannot establish compatibility, reconciliation, rotation, or failure for the deployed version combination. | Inventory deployed versions read-only, select an explicit audience from vendor contracts, then canary auth and one redacted rotation before manifest change. | P2 planned improvement | New Stage 03 Spec: vault-eso-transport-and-secret-exposure-hardening | The Spec pins Vault/ESO/Kubernetes versions and expected audience; a non-secret canary records accepted/rejected audiences, store/auth result, one value-free rotation/reconciliation timestamp, upgrade trigger, and rollback. |
| SEC-010 | Current finding: NetworkPolicy enforcement | The actual CNI enforces intended ingress/egress behavior with positive and negative probes for each protected flow. | Six egress policies and selected CIDR/port static checks exist; `verify-network-policies.sh` inspects object presence/fields but sends no traffic and no CNI behavior was observed. | 1 documented/routed | Partial | Unverified live | Unverified (High), not superseded: desired restrictions may diverge from effective connectivity, and no ingress-isolation claim follows. | Define the CNI/version contract and approved ephemeral positive/negative probes with cleanup and redacted evidence. | P1 near-term integrity | New Stage 03 Spec: network-policy-behavioral-assurance | For every policy owner, approved probes prove intended DNS/API/external flows succeed and forbidden destinations/ports fail; evidence records CNI/version, namespaces, cleanup, and timestamp. |
| SEC-011 | Current finding: regex-heavy static contracts | Fast sentinels are complemented by parsed/rendered negative fixtures and version-matched schema or approved server-dry-run evidence. | `verify-contracts-static.sh` is primarily `grep -P`/`grep -Pz`; structure checks parse YAML and sibling references but do not render every root or validate produced objects against APIs/CRDs. | 2 repository-static | Partial | Verified repo-static | Needs strengthening (Medium), not superseded: text can satisfy a check while nesting, composition, schema, or admission semantics are invalid. | Keep fast sentinels, then add full Kustomize render and schema layers in dependency order with explicit offline/live boundaries. | P2 planned improvement | New Stage 03 Spec: platform-security-validation-evidence-contract | Negative fixtures for wrong nesting, omitted render output, unknown field, unavailable CRD schema, and admission rejection fail the correct layer; every root renders and tool/version evidence is explicit. |
| SEC-012 | [Task 9 supply-chain owner](ci-qa-automation-pipeline-workflow.md#supply-chain-automation-controls); Current immutable-Action finding | Third-party Actions execute immutable reviewed commits with update metadata, least privilege, and rollback. | Task 9 owns the fixed-tree Action identity and workflow facts; this row consumes that evidence without restating counts. Security impact is that mutable dependency identity can change CI-executed code without a repository change. | 1 documented/routed | Gap | Verified repo-static | Implementation gap (High), not superseded: update automation does not provide immutable execution identity. | Use Task 9's coordinated pinning route; security review supplies source trust, permission, rollback, and compromise-response acceptance. | P1 near-term integrity | New Stage 03 Spec: github-actions-immutable-dependency-identity | Task 9 acceptance evidence is met, and security review additionally records upstream owner/repository trust, least permissions, reviewed SHA provenance, rollback SHA, and one moved-tag negative fixture. |
| SEC-013 | [Task 9 supply-chain owner](ci-qa-automation-pipeline-workflow.md#supply-chain-automation-controls); NIST SP 800-204D/SLSA | Platform image and any future build/release artifact receive only threat-modelled identity, vulnerability, SBOM, provenance, signature, and verification controls with named consumers. | Task 9 owns current workflow/artifact relevance and N/A decisions; this row does not duplicate them. The platform still consumes mutable image tags, while no approved artifact-verification architecture or consumer evidence exists. | 1 documented/routed | Partial | Conditional | Implementation gap (High), not superseded but narrowed: broad enterprise lanes are not automatically applicable; the unresolved security issue is deciding and enforcing assurance for actual GitOps image/artifact consumers. | Threat-model image/chart/Action inputs, name verifier decisions, and adopt only controls with an artifact owner and response consumer. | P2 planned improvement | New Stage 02 ARD: platform-supply-chain-assurance-scope | The ARD inventories actual dependency/artifact classes, threat and trust boundaries, owner/verifier/retention/response consumers, explicit adopt/defer decisions, and measurable triggers that reopen every deferred lane. |
| SEC-014 | Current finding; Argo CD AppProject security warning | Any project able to deploy into `argocd` has tightly restricted live Argo CD RBAC, protected source writes, review, audit, and revocation evidence. | `platform` can deploy to `argocd`; its tracked project role is read-only and resource/source lists are explicit, but live Argo CD RBAC and remote source-write protection were not inspected. | 2 repository-static | Partial | Unverified live | Unverified (High), not superseded: the tracked boundary is narrow but compromise of an authorized principal/source could control Argo CD itself. | Define the admin-equivalent principal/source matrix and require separately approved read-only evidence at every access-model change. | P1 near-term integrity | New Stage 03 Spec: argocd-admin-boundary-assurance | A redacted inventory maps every principal and source write path to least privilege, review/ruleset, audit, expiry/revocation, break-glass, and quarterly read-only verification; an unauthorized fixture is denied. |

## Score and Distribution Summary

| Category | Applicable controls | Maturity numerator | Denominator | Implementation | Maturity distribution (`0/1/2/3/4`) | Verdict distribution (`Implemented/Partial/Gap/Not in scope`) | Confidence distribution (`Verified repo-static/Unverified live/Conditional`) | N/A exclusions |
| --- | ---: | ---: | ---: | ---: | --- | --- | --- | --- |
| GitOps and platform foundations | 12 | 31 | 48 | 64.6% | `0/1/3/8/0` | `11/1/0/0` | `11/1/0` | None |
| SEC finding reconciliation | 14 | 13 | 56 | 23.2% | `3/9/2/0/0` | `0/10/4/0` | `8/5/1` | None |
| **Overall** | **26** | **44** | **104** | **42.3%** | **`3/10/5/8/0`** | **`11/11/4/0`** | **`19/6/1`** | **None** |

Arithmetic is `31 + 13 = 44` over `4 * (12 + 14) = 104`. All 26
controls are applicable; there are no N/A exclusions. No maturity 4 is awarded
because this audit ran no approved Kubernetes, Argo CD, Vault, ESO, TLS,
NetworkPolicy, recovery, registry, or remote workflow observation.

The 15 actionable controls comprise two P0, eight P1, five P2, and zero P3
findings. Every non-actionable implemented row uses the exact
`N/A — no action` value for priority, follow-up owner, and acceptance evidence.

### SEC Supersession Result

| Result | Count | IDs | Reason |
| --- | ---: | --- | --- |
| Retained | 14 | `SEC-001`~`SEC-014` | The audit observation SHA preserves every owning path and material condition used by the refreshed Current research. |
| Superseded | 0 | None | No active implementation or stronger approved evidence replaced a finding. |
| Closed | 0 | None | No acceptance evidence required by these controls exists at the observation SHA. |

`SEC-013` is retained but interpreted with Task 9's relevance decisions: the
absence of every enterprise supply-chain lane is not fourteen independent
failures. The actionable question is assurance for the image, chart, Action,
or future artifact consumers the repository actually owns.

### Actionable Finding Register

| Priority | Controls | Dependency-aware disposition |
| --- | --- | --- |
| P0 immediate safety | SEC-006, SEC-008 | Contain use of the affected secret-bearing bootstrap path first; design verified TLS and argv-free secret transfer together so one fix does not preserve the other exposure. |
| P1 near-term integrity | SEC-001, SEC-003, SEC-004, SEC-005, SEC-007, SEC-010, SEC-012, SEC-014 | Establish path/evidence selection and immutable CI identity, then land strict read-only assertions before transport or authorization changes; runtime promotion waits for approved canaries. |
| P2 planned improvement | PLAT-008, SEC-002, SEC-009, SEC-011, SEC-013 | Use the validation contract and version inventory to scope render/schema, audience, recovery, and supply-chain decisions without turning optional tools or absent artifact consumers into false readiness gates. |
| P3 optional/telemetry-gated | None | No evidence supports an optional platform redesign or additional security product in this snapshot. |

## Comparison Analysis

- Desired-state structure is the strongest area: root/platform/workload
  ownership, Kustomize completeness, exact AppProject lists, namespace
  ownership, plaintext-Secret rejection, and tag hygiene have deterministic
  local/CI enforcement.
- Runtime assurance is intentionally weak in the score. Automated prune and
  self-heal are declarations; the current live scripts do not prove strict
  sync/health, CA trust, NetworkPolicy behavior, or rollback recovery.
- Secret-plane findings have the shortest risk path. The repository visibly
  defaults bootstrap TLS verification off, configures ESO-to-Vault HTTP, and
  expands secret values into argv. These are implementation facts even though
  no live secret or process was inspected.
- AppProject enumeration is a meaningful least-privilege strength, but the
  `platform` project's `argocd` destination remains admin-equivalent. Static
  project roles cannot substitute for live Argo CD RBAC and protected source
  writes.
- Consolidated improvement is preferred: one platform-security validation
  contract, one Vault/ESO transport and exposure contract, strict diagnostic
  modes, behavioral network checks, immutable CI dependencies, and one
  admin-boundary evidence model. A full environment/platform replacement is
  not justified by this repository snapshot.

## Residual Risks

- The fixed-tree counts and validations do not prove controllers accepted or
  reconciled the manifests, nor that installed CRD/API versions match them.
- No secret value, credential, Vault policy attachment, token lifetime,
  rotation, seal state, audit device, or generated Secret access was inspected.
- NetworkPolicy objects and `/32` destinations do not prove the active CNI
  filters traffic; all six tracked policies are egress-focused.
- Static allow-lists do not prove live Kubernetes or Argo CD authorization,
  remote repository protection, or revocation behavior.
- Task 9 supply-chain relevance decisions can change when a first-party build,
  release, image promotion, signature verifier, or public dependency consumer
  is introduced; this report must then be refreshed rather than retroactively
  promoted.

## Sources

### Repository and Audit Sources

- [Audit pack method](README.md)
- [Implementation plan](../../../04.execution/plans/2026-07-11-workspace-engineering-research-audit-integration.md)
- [Current Kubernetes, Infrastructure, and Security Research](../../research/2026-07-07-wer/kubernetes-infrastructure-security.md)
- [Task 9 CI, QA, and Supply-Chain Audit](ci-qa-automation-pipeline-workflow.md)
- [GitOps README](../../../../gitops/README.md)
- [Infrastructure README](../../../../infrastructure/README.md)
- [Root Application](../../../../gitops/clusters/local/root-application.yaml)
- [Workload ApplicationSet](../../../../gitops/clusters/local/applicationset-apps.yaml)
- [Apps AppProject](../../../../gitops/clusters/local/appproject-apps.yaml)
- [Platform AppProject](../../../../gitops/clusters/local/appproject-platform.yaml)
- [Vault store](../../../../gitops/platform/eso/vault-secret-store.yaml)
- [ESO TokenReview binding](../../../../gitops/platform/eso/vault-token-reviewer-binding.yaml)
- [Vault policy](../../../../infrastructure/vault/policies/eso-read.hcl)
- [NetworkPolicy Kustomization](../../../../gitops/platform/network-policies/kustomization.yaml)
- [Kubernetes policy bundle](../../../../policy/conftest/kubernetes.rego)
- [GitOps structure validator](../../../../scripts/validate-gitops-structure.sh)
- [Manifest validator](../../../../scripts/validate-k8s-manifests.sh)
- [Policy validator](../../../../scripts/validate-policy-gates.sh)
- [Secret scanner](../../../../scripts/check-secret-handling.sh)
- [Static infrastructure contracts](../../../../infrastructure/tests/verify-contracts-static.sh)
- [GitOps live test](../../../../infrastructure/tests/verify-gitops.sh)
- [Secret live test](../../../../infrastructure/tests/verify-secrets.sh)
- [NetworkPolicy live test](../../../../infrastructure/tests/verify-network-policies.sh)
- [Ingress/TLS live test](../../../../infrastructure/tests/verify-ingress-tls.sh)
- [Kubernetes GitOps operations policy](../../../05.operations/policies/0001-k8s-gitops-operations-policy.md)
- [Argo CD/ESO/Vault recovery runbook](../../../05.operations/runbooks/0002-argocd-eso-vault-recovery-runbook.md)

Repository links identify active owner paths; every implementation claim was
read from those paths at the audit observation SHA.

### External Benchmarks

- [Kubernetes Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)
- [Kubernetes RBAC](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
- [Kubernetes NetworkPolicy](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
- [Kubernetes Kustomize](https://kubernetes.io/docs/tasks/manage-kubernetes-objects/kustomization/)
- [OpenGitOps Principles](https://opengitops.dev/)
- [Argo CD AppProjects](https://argo-cd.readthedocs.io/en/stable/user-guide/projects/)
- [External Secrets Operator Vault Provider](https://external-secrets.io/latest/provider/hashicorp-vault/)
- [Vault Kubernetes Authentication](https://developer.hashicorp.com/vault/docs/auth/kubernetes)
- [OPA for Kubernetes](https://www.openpolicyagent.org/docs/kubernetes)
- [NIST SP 800-204D](https://csrc.nist.gov/pubs/sp/800/204/d/final)
- [SLSA v1.2](https://slsa.dev/spec/v1.2/)

## Review and Freshness

- Review cadence: on source change
- Last reviewed: 2026-07-11
- Next review trigger: any source listed in the Reference Type changes, a SEC
  acceptance artifact lands, or approved live/remote evidence becomes
  available.
- Refresh method: retain the prior observation SHA, open a new dated audit or
  advance the snapshot explicitly, recount the GitOps topology, rerun each
  repo-static lane, reassess all 26 rows and N/A relevance, and collect
  live/remote evidence only with separate approval.

## Related Documents

- **Audit pack**: [2026-07-11 WEIA README](README.md)
- **Implementation plan**: [WEIA implementation plan](../../../04.execution/plans/2026-07-11-workspace-engineering-research-audit-integration.md)
- **Current research pack**: [2026-07-07 WER README](../../research/2026-07-07-wer/README.md)
- **Parent audits index**: [Audits README](../README.md)
- **Integrated remediation owner**: `remediation-roadmap.md`
