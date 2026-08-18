---
title: 'Audit: Security and Approval Boundaries'
type: content/reference
status: draft
owner: platform
updated: 2026-08-09
---

# Audit: Security and Approval Boundaries

## Overview

This report audits repository, workflow, supply-chain, agent, secret, GitOps,
infrastructure, permission, destructive-action, remote, and live trust
boundaries at observation commit
`50628b84165479b03efc0a25be075a49c91a9aef`. The reviewed security owners and
desired-state surfaces are identical at the current starting HEAD
`e4ed34d56f7b90a12771232c7bfe54d5c4d6f94e`.

## Reference Type

Dated repository-static security and approval audit. It is not a permission
gate, secret store, vulnerability scan result, cluster assessment, provider
policy, approval grant, or remediation authority.

## Authority Boundary

Stage 00 owns approvals; provider settings own only their native tracked
configuration; workflows and locks own CI intent; GitOps owns desired state;
policy and validators own their exact static checks. This report inspected only
tracked structure and metadata. It did not inspect or print secret values,
authenticate, contact a provider or remote, read a cluster, invoke Vault/ESO,
dispatch a workflow, mutate infrastructure, or promote static evidence to
hosted/provider-runtime/live enforcement.

## Scope

Included: approval/exception routing, Git and workflow permissions, Action and
Python dependency integrity, agent permissions, secret-reference and scanning
controls, GitOps/AppProject/RBAC, NetworkPolicy, container security context,
image/chart/Git target identity, policy-as-code, local infrastructure, and
remote/live separation. Excluded: secret values, credentials, remote branch
rules, hosted workflow results, provider consumption, effective permissions,
cluster admission/RBAC/network behavior, image registry evidence, Vault/ESO
delivery, cloud state, and operator rehearsal.

## Definitions / Facts

### Security

The current contract is local-home-lab desired state. Accepted local exceptions
must remain visibly local and must not be reused as production-like evidence.
The static manifest/security probe found:

| Dimension | Exact repository-static result | Claim boundary |
| --- | --- | --- |
| Namespaces / policies | Nine tracked Namespace objects; six NetworkPolicies in `apps`, `argocd`, `external-secrets`, `istio-system`, `monitoring`, and `platform`; all six are Egress-only; zero Ingress or default-deny policies; four tracked namespaces have no policy. | Desired state only; no CNI or packet observation. |
| RBAC | Five raw RBAC objects and zero wildcard rules; KSM is nevertheless bound cluster-wide with `list,watch` on `secrets`. | Absence of wildcards is not least-privilege proof. |
| Raw pod templates | Three: Alloy and KSM Deployments have non-root/read-only/no-escalation/drop-all controls; Adminer Rollout lacks these controls and service-account-token opt-out. | Helm-rendered workloads and live admission are not included. |
| Raw images | Three pod images, all non-`latest`, zero digest-pinned; local k3d also uses a mutable version tag. | Tag hygiene is not provenance, signature, SBOM, or immutable identity. |
| Secret objects | Zero tracked raw `kind: Secret` objects in GitOps/infrastructure; three ExternalSecret objects and one ClusterSecretStore route references only. | Generated Secret contents, storage, delivery, rotation, and access are live evidence. |
| Immediate-stop patterns | Zero wildcard RBAC rules, explicit root/privileged/escalation/host escapes, or `:latest` images in the reviewed raw desired state. | This does not negate the narrower permission, RBAC, isolation, admission, or identity gaps below. |

The actual static tools also expose important result distinctions:

- GitHub Actions security, CI Python lock, Vault/ESO, GitOps structure/change
  set, secret-handling, manifests, policy fallback, and static infrastructure
  checks pass.
- KubeLinter runs and reports no lint errors, but `.kube-linter.yaml` explicitly
  excludes non-root, read-only-root-filesystem, latest-tag, CPU, memory, and
  anti-affinity checks. The pass cannot imply those controls.
- Conftest is not installed; `validate-policy-gates.sh` reports `SKIP` for
  optional Conftest and then passes its built-in fallback. The fallback checks
  raw Secret, wildcard AppProject scope, CreateNamespace, and `:latest`, not
  pod-hardening or live admission.
- The bounded secret handler passes 100 selected files. In contrast, redacted
  actual Gitleaks scans return RED: four no-git worktree candidates and eleven
  Git-history candidates. Metadata-only triage identifies two current tracked
  false-positive-shaped records and two ignored bytecode hits; historical
  candidates remain unclassified. No match or secret value was inspected.

### Approval-boundary Inventory

| Boundary | Owner | Threat | Enforcement point | Evidence artifact | Bypass / exception route | Failure mode | Approval authority | Depth / result |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Repository writes and destructive Git | Stage 00 approval matrix and Git workflow | Unscoped overwrite, history loss, unauthorized merge/push | Sandbox/task ownership, deny patterns, staged review, human finish choice | `docs/00.agent-governance/rules/approval-boundaries.md#approval-matrix`; `docs/00.agent-governance/rules/git-workflow.md#rules` | Exact human recovery approval with scope, target, rollback, evidence | Broad command or provider allow bypasses human decision | User/human owner | `repository-static`; broadly `Aligned`, provider exception in `WGA-SEC-002` |
| Workflow permissions | Workflow owner and Actions security validator | Token write, untrusted trigger, unpinned Action, direct deployment | Trigger/permission/concurrency/action-SHA validator and read-only workflow permissions | `.github/workflows/ci.yml#permissions`; `scripts/validate-github-actions-security.py#main` | Protected workflow expansion requires governance update and approval | Hosted token or branch controls differ from tracked YAML | Repository owner | `repository-static`; `Aligned`, hosted `DEFER` |
| Validation supply chain | CI lock owner and CI Python contract | Dependency substitution or downloaded-tool tampering | Hashed requirements, full Action SHA, Gitleaks archive SHA-256 | `.github/requirements/ci-validation.txt`; `.github/workflows/ci.yml#jobs.repo-quality-static`; `scripts/validate-ci-python-contract.py#main` | Version change through reviewed lock regeneration | Hosted fetch/install or package provenance differs | Repository owner | `repository-static`; `Aligned`, hosted `DEFER` |
| Agent/provider permission | Stage 00 shared policy plus provider setting owner | Secret read, unapproved Git remote action, cluster information disclosure | Provider allow/deny config and shared approval stop conditions | `.claude/settings.json#permissions.allow`; `.claude/settings.json#permissions.deny`; `scripts/validate-agent-provider-config.py#validate_claude_permissions`; `docs/00.agent-governance/rules/approval-boundaries.md#mandatory-policies` | Unlisted commands retain the human decision path; tracked deny rules explicitly stop secret-read and remote-mutation shapes | Native loading or matcher behavior differs from tracked intent | User/operator | `repository-static`; `Aligned`; runtime `DEFER` |
| Secret detection | Gitleaks/detect-secrets config, bounded scanner, workflow/pre-commit owners | Committed credential or noisy gate that masks a real leak | Pre-commit Gitleaks/detect-secrets plus bounded structural scanner | `.gitleaks.toml#rules[id=generic-api-key]`; `.pre-commit-config.yaml#repos[id=gitleaks]`; `scripts/check-secret-handling.sh#add_scan_root` | Exact reviewed false-positive allowlist only; real finding requires stop/rotation | Full worktree/history scan is RED while bounded scan passes | Security owner; credential owner if real | `repository-static`; `Partial` |
| Vault/ESO secret references | GitOps/security, external Vault operator | Plaintext secret, wrong store/identity, unsafe bootstrap value path | ExternalSecret/ClusterSecretStore/RBAC/HCL contracts, HTTPS bootstrap, stdin/header/file flow | `gitops/platform/eso/vault-secret-store.yaml#kind=ClusterSecretStore`; `infrastructure/bootstrap-local.sh#vault_curl`; `scripts/validate-vault-eso-contracts.py#main` | Annotated local-only HTTP store; bootstrap-only mutation; production reuse prohibited | Exception reused outside local or live policy/identity diverges | Platform/security for Git; Vault/operator for live | `repository-static`; `Aligned` to declared local contract; live `DEFER` |
| GitOps and AppProject | GitOps desired-state owner and approval matrix | Direct mutation, wildcard deployment authority, namespace creation bypass | Argo applications/projects, policy gate, immutable identity diff | `gitops/clusters/local/appproject-apps.yaml#kind=AppProject`; `scripts/validate-gitops-structure.sh#ROOT_APP`; `scripts/validate-gitops-change-set.py#main` | Approved bootstrap/break-glass with rollback/reconciliation | Argo live RBAC/reconciliation differs or source `main` changes | Operator for sync/live; repository owner for desired state | `repository-static`; `Aligned` structure; live `DEFER` |
| Kubernetes RBAC | Platform/security and workload manifest owner | Cluster-wide Secret metadata access beyond metrics need | Raw ClusterRole/Binding and manifest/static checks | `gitops/platform/monitoring/kube-state-metrics.yaml#kind=ClusterRole,metadata.name=kube-state-metrics`; `scripts/validate-k8s-manifests.sh#YAML_TARGETS` | No focused exception/justification or least-privilege negative gate found | KSM SA lists/watches Secrets cluster-wide | Platform/security reviewer | `repository-static`; `Partial` |
| Network isolation | Security-owned policy manifests and GitOps app | Lateral ingress or unrestricted namespace traffic | Six selected egress NetworkPolicies and static contract checks | `gitops/platform/network-policies/kustomization.yaml#resources`; `infrastructure/tests/verify-contracts-static.sh#require_pattern` | Local-home-lab design may accept scoped absence only after explicit decision | Four tracked namespaces uncovered; no Ingress/default-deny; CNI may not enforce | Platform/security for desired state; operator for live probes | `repository-static`; `Gap`; live `DEFER` |
| Container and admission | Workload/platform owners, KubeLinter/policy config | Root/writeable/escalating workload or unenforced baseline | Raw pod securityContext, KubeLinter, policy fallback, PR review | `.kube-linter.yaml#checks.exclude`; `gitops/workloads/adminer/rollout.yaml#spec.template.spec`; `policy/conftest/kubernetes.rego#deny[msg]` | Explicit home-lab exclusions; no production-like promotion route exists | Rollout remains unhardened and no PSA/admission policy blocks recurrence | Workload owner plus platform/security | `repository-static`; `Gap`; live admission `DEFER` |
| Image/chart/Git identity | GitOps/application and workflow supply-chain owners | Mutable upstream content, compromised registry/chart/source | Non-latest tag checks and version fields | `gitops/clusters/local/root-application.yaml#spec.source.targetRevision`; `gitops/workloads/adminer/rollout.yaml#spec.template.spec.containers[name=adminer].image`; `gitops/README.md#workload-image-and-kind-policy-matrix` | Local tag/version use is explicit; no signature/provenance exception authority exists | Same tag/main/chart version resolves to different bytes | Platform/security architecture owner | `repository-static`; `Partial`; registry/hosted `DEFER` |
| Remote/live | Human/operator and runbook owners | Unapproved publish, workflow dispatch, cluster/Vault mutation, false readiness | Stage 00 stop condition and operations runbooks | `docs/00.agent-governance/rules/approval-boundaries.md#approval-matrix`; `gitops/README.md#configuration-boundary` | Explicit human/operator approval with target, rollback, redacted evidence | Static result promoted to runtime/live claim | User/operator | `repository-static` boundary `Aligned`; deeper evidence `DEFER` |

### Blockers

| ID | Cause | Impact | Affected request IDs | Release condition | Owner | Evidence depth | Classification |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BLK-WGA-SEC-001 | Hosted branch/ruleset, provider loading/effective permissions, remote publication, cluster admission/RBAC/CNI, GitOps reconciliation, Vault/ESO, registry identity, and live operator behavior were not authorized or observed. | Static controls cannot establish effective enforcement, readiness, confidentiality, or network behavior. | `REQ-WGA-024` | Separately approved redacted hosted/provider/live evidence is collected by the current owner without secret values or mutation outside scope. | Repository/provider/operator owners by lane. | `provider-runtime` and `live` | `DEFER` evidence limitation, not a blocker to the static audit. |
| BLK-WGA-SEC-002 | Redacted Gitleaks finds eleven historical candidates; the audit intentionally did not inspect match/secret payloads. | A clean-history assertion is unavailable; broad allowlisting could conceal a real credential. | `REQ-WGA-024` | Security/credential owners triage candidate metadata through an approved non-disclosing process, rotate/revoke any real credential, and add only exact false-positive rules. | Security owner and any affected credential owner. | `repository-static` | Blocks clean-history promotion, not completion of the bounded report. |

### Finding Convention

Every material finding uses the closed pack fields plus explicit threat,
enforcement, exception, failure, and approval mappings. A static PASS applies
only to the rule actually executed. A blocker is either a complete object above
or explicit `none`.

#### WGA-SEC-001 — Shared approval, workflow, and GitOps structure align within the static lane

- **Request IDs**: `REQ-WGA-024`.
- **Scope**: repository writes, destructive Git, workflows, validation dependencies, GitOps structure, AppProject wildcard/namespace policy, and static infrastructure.
- **Expected state**: one human-owned approval route separates local desired-state edits from protected publish, destructive, remote, provider, and live actions, with deterministic static checks.
- **Observed state**: Stage 00 and Git rules agree; Actions/CI/GitOps/policy/manifests/static-infrastructure checks pass; workflows use read-oriented permissions, full Action SHAs, and hashed Python/tool inputs; no current security-owner drift exists.
- **Threat**: unauthorized destructive/remote action, workflow token expansion, dependency substitution, or direct live mutation.
- **Enforcement point**: approval matrix, Git rules, workflow permissions/triggers, AppProject/policy gates, immutable change-set evidence.
- **Evidence**: `docs/00.agent-governance/rules/approval-boundaries.md#approval-matrix`; `docs/00.agent-governance/rules/git-workflow.md#rules`; `.github/workflows/ci.yml#permissions`; `.github/requirements/ci-validation.txt`; `scripts/validate-github-actions-security.py#main`; `scripts/validate-ci-python-contract.py#main`; `gitops/clusters/local/appproject-apps.yaml#kind=AppProject`; `scripts/validate-gitops-structure.sh#ROOT_APP`; `scripts/validate-gitops-change-set.py#main`.
- **Bypass / exception**: only recorded human recovery/bootstrap/break-glass authority; provider-specific overbreadth is excluded to `WGA-SEC-002`.
- **Failure mode**: tracked configuration drifts, a protected action bypasses approval, or hosted/live state differs.
- **Approval authority**: user/operator for destructive, publish, remote, and live action; repository owner for desired-state review.
- **Evidence depth**: `repository-static`.
- **Verdict**: `Aligned`.
- **Impact**: current static routing and broad control structure are deterministic without claiming deeper enforcement.
- **Disposition**: `Keep`.
- **Canonical owner**: Stage 00 approval/Git rules, workflows/locks, GitOps/AppProject, and their validators by concern.
- **Verification**: focused Actions, CI lock, GitOps, policy, manifest, infrastructure, profile, link, and diff checks.
- **Uncertainty**: hosted settings, provider consumption, remote Git, cluster/GitOps, and operator action.
- **Blocker**: none for this bounded static structure; `BLK-WGA-SEC-001` limits deeper evidence.

#### WGA-SEC-002 — Claude tracked permissions align with shared approval stops

- **Request IDs**: `REQ-WGA-024`.
- **Scope**: Claude native Bash allow/deny patterns for file reads, Git, kubectl, secrets, and remote action.
- **Expected state**: provider-native permissions are no broader than shared secret-value, remote publication, and live-cluster approval boundaries, or require the same explicit human gate.
- **Observed state**: the observation configuration allowed broad `cat`, `grep`, `git`, and kubectl read families and omitted ordinary push/merge and secret-read stops. WGIA-011 replaces those allows with exact repository-static validator commands and fixed metadata-only Git commands. Root-taking validators receive literal `.`, the LLM-WIKI producer is allowlisted only in `--check` mode, and no allow contains wildcard syntax. The focused provider validator owns the exact complete 62-entry deny tuple, including environment/Vault/Kubernetes secret reads, remote/destructive Git, GitHub mutation, kubectl/Argo/Vault writes, recursive removal, and k3d deletion; the aggregate retains only unrelated hook wiring. Runtime loading remains unobserved.
- **Threat**: provider runtime treats a broad allow as authority to read secret-bearing files/resources or perform ordinary Git remote actions.
- **Enforcement point**: `.claude/settings.json` permission matcher and Stage 00 human approval stop.
- **Evidence**: `.claude/settings.json#permissions.allow`; `.claude/settings.json#permissions.deny`; `scripts/validate-agent-provider-config.py#validate_claude_permissions`; `tests/test_validate_agent_provider_config.py#ProviderConfigContractTests.test_each_broad_claude_allow_rule_fails_closed`; `tests/test_validate_agent_provider_config.py#ProviderConfigContractTests.test_each_required_claude_deny_rule_fails_closed_when_missing`; `docs/00.agent-governance/rules/approval-boundaries.md#mandatory-policies`; `docs/00.agent-governance/rules/git-workflow.md#rules`; `docs/00.agent-governance/providers/claude.md#native-boundary`.
- **Bypass / exception**: no tracked exception weakens the shared matrix; operations outside the closed allow set are not pre-authorized by tracked configuration, and explicit denies retain the repository-static stop. Native prompting behavior remains `DEFER`.
- **Failure mode**: tracked settings broaden an allowed command family, remove a required stop, or native runtime behavior differs from the repository-static contract.
- **Approval authority**: user/operator; provider config cannot self-authorize.
- **Evidence depth**: `repository-static`.
- **Verdict**: `Aligned`.
- **Impact**: tracked Claude permission intent no longer subsumes secret reads, ordinary remote mutation, or broad live reads; actual provider enforcement remains `DEFER`.
- **Disposition**: `Correct`; WGIA-009 admitted and WGIA-011 implemented the bounded tracked-adapter correction.
- **Canonical owner**: Stage 00 approval rules for shared authority; `.claude/settings.json` for Claude-native enforcement syntax.
- **Verification**: the focused unit module covers the production set, every forbidden broad allow, wildcard mutation, alternate-root mutation, and removal of each of the 62 required denies; provider-config self-test/production, harness contract/semantics/currentness, and later separately authorized runtime evidence remain distinct.
- **Uncertainty**: matcher precedence, native loading, interactive approval prompts, and actual execution.
- **Blocker**: `BLK-WGA-SEC-001` blocks runtime-effect claims, not the static conflict.

#### WGA-SEC-003 — Secret scanning is bounded but full-worktree/history evidence is noisy and incomplete

- **Request IDs**: `REQ-WGA-024`.
- **Scope**: bounded secret scanner, Gitleaks/detect-secrets configuration, current worktree, ignored bytecode, and Git-history scan.
- **Expected state**: current tracked and history scans either pass or produce an exact non-disclosing triage/rotation route; false positives are narrowly allowlisted without suppressing real secrets.
- **Observed state**: bounded scanner passes 100 files. Redacted actual Gitleaks no-git scan returns four: two current tracked false-positive-shaped metadata/prose rows and two ignored bytecode hits. Redacted Git scan returns eleven untriaged historical candidates. No value or match payload was inspected.
- **Threat**: real credential exposure is obscured by false-positive noise, or a broad allowlist weakens future detection.
- **Enforcement point**: Gitleaks/detect-secrets pre-commit/CI configuration and bounded structural scanner.
- **Evidence**: `.gitleaks.toml#rules[id=generic-api-key].allowlists`; `.pre-commit-config.yaml#repos[id=gitleaks]`; `.pre-commit-config.yaml#repos[id=detect-secrets]`; `scripts/check-secret-handling.sh#add_scan_root`; `docs/03.specs/024-observability-and-network-review-agents/spec.md#strategic-boundaries--non-goals`; `docs/90.references/data/active-corpus-migration-results.json#batches[].pairKey`; `docs/04.execution/tasks/2026-08-09-workspace-governance-audit-and-remediation.md#wgia-008-focused-evidence`.
- **Bypass / exception**: only path-and-line-specific reviewed false-positive allowances; ignored `__pycache__` is non-authoritative transient output.
- **Failure mode**: current/all-history scan remains RED, a real secret is untriaged, or an overbroad suppression makes the gate green.
- **Approval authority**: security owner for classifier changes; credential owner for rotation/revocation if a candidate is real.
- **Evidence depth**: `repository-static`.
- **Verdict**: `Gap`.
- **Impact**: selected source families are structurally clean, but the repository cannot claim a clean current corpus/history from the actual Gitleaks CLI.
- **Disposition**: `Correct` provisionally; never normalize by exposing candidate values.
- **Canonical owner**: `.gitleaks.toml`, pre-commit/CI secret gates, and security-owned triage route.
- **Verification**: redacted current tracked/history scans, exact negative fixtures, ignored-artifact exclusion, and security review of each remaining metadata record.
- **Uncertainty**: historical candidate classification and whether any credential requires rotation.
- **Blocker**: `BLK-WGA-SEC-002`.

#### WGA-SEC-004 — Kube-state-metrics has unjustified cluster-wide Secret metadata access

- **Request IDs**: `REQ-WGA-024`.
- **Scope**: KSM ClusterRole, ClusterRoleBinding, ServiceAccount token, and current least-privilege validation.
- **Expected state**: a metrics service account receives only resources required for its selected collectors; Secret list/watch requires explicit necessity and a negative regression gate.
- **Observed state**: KSM is bound to a ClusterRole with cluster-wide `list,watch` on `secrets` and automounts its service-account token. No focused current owner, justification, or validator asserts this access is necessary. The generic wildcard probe still passes because the rule is exact, not wildcard.
- **Threat**: KSM compromise enumerates Secret metadata cluster-wide or expands exposure beyond metrics need.
- **Enforcement point**: KSM ClusterRole/Binding and a missing resource-specific least-privilege gate.
- **Evidence**: `gitops/platform/monitoring/kube-state-metrics.yaml#kind=ClusterRole,metadata.name=kube-state-metrics`; `gitops/platform/monitoring/kube-state-metrics.yaml#kind=ClusterRoleBinding,metadata.name=kube-state-metrics`; `gitops/platform/monitoring/kube-state-metrics.yaml#spec.template.spec.automountServiceAccountToken`; `scripts/validate-k8s-manifests.sh#YAML_TARGETS`; `infrastructure/tests/verify-contracts-static.sh#require_pattern`.
- **Bypass / exception**: none found; upstream defaults alone are not a repository approval.
- **Failure mode**: exact but unnecessary Secret access passes syntax/policy checks and reaches the cluster through GitOps.
- **Approval authority**: platform/security reviewer after collector/compatibility evidence.
- **Evidence depth**: `repository-static`.
- **Verdict**: `Partial`.
- **Impact**: current raw RBAC is not least privilege despite zero wildcard rules.
- **Disposition**: `Correct` provisionally after collector/version dependency review.
- **Canonical owner**: KSM desired-state manifest; security scope owns the least-privilege review.
- **Verification**: negative fixture forbids Secret access unless a named collector contract requires it; manifest/GitOps/policy checks and later live metrics canary.
- **Uncertainty**: enabled KSM collectors, compatibility requirements, and live authorization/effect.
- **Blocker**: none for the static finding; live compatibility belongs to `BLK-WGA-SEC-001`.

#### WGA-SEC-005 — Network isolation covers selected egress only

- **Request IDs**: `REQ-WGA-024`.
- **Scope**: tracked namespaces, NetworkPolicy objects, selectors, policy types, default-deny baseline, and CNI evidence boundary.
- **Expected state**: local-home-lab namespace isolation has an explicit accept/defer/design decision; any claimed protected namespace has selected ingress/egress/default-deny coverage and later positive/negative CNI verification.
- **Observed state**: six policies are Egress-only and none is default-deny; zero Ingress policies exist. Four of nine tracked namespaces—`argo-rollouts`, `cert-manager`, `headlamp`, `ingress-nginx`—have no policy. Current docs accurately call the owner egress policy, not comprehensive isolation.
- **Threat**: lateral ingress, unrestricted namespace paths, or false confidence from manifest presence.
- **Enforcement point**: security-owned NetworkPolicy manifests, GitOps app, static coverage contract, and later CNI enforcement.
- **Evidence**: `gitops/platform/network-policies/kustomization.yaml#resources`; `gitops/platform/namespaces/kustomization.yaml#resources`; `gitops/README.md#service-coverage-matrix`; `infrastructure/tests/verify-contracts-static.sh#require_pattern`; `infrastructure/tests/verify-network-policies.sh#platform_np`.
- **Bypass / exception**: a reviewed local-home-lab exception may retain selective egress, but it must state namespaces/flows and cannot be promoted to production-like isolation.
- **Failure mode**: uncovered ingress/namespace remains reachable or live CNI ignores desired rules.
- **Approval authority**: platform/security for baseline design; operator for live probes.
- **Evidence depth**: `repository-static`.
- **Verdict**: `Gap`.
- **Impact**: selected egress is constrained, but namespace isolation/default deny is incomplete.
- **Disposition**: `Integrate` provisionally into an explicit local baseline and live verification route.
- **Canonical owner**: `gitops/platform/network-policies/**`, namespace owner map, and network-policy operations verification.
- **Verification**: exact namespace/policy matrix fixtures, default-deny/exception tests, manifest/GitOps gates, and separately approved positive/negative CNI probes.
- **Uncertainty**: intended local trust model, chart-created workloads, CNI/version, and effective packet behavior.
- **Blocker**: `BLK-WGA-SEC-001` blocks live enforcement claims only.

#### WGA-SEC-006 — Pod hardening and admission are only partially enforced

- **Request IDs**: `REQ-WGA-024`.
- **Scope**: three raw pod templates, KubeLinter exclusions, Adminer Rollout, monitoring security contexts, PSA/admission/policy-as-code coverage.
- **Expected state**: local exceptions are explicit and bounded; production-like promotion requires non-root, no escalation, read-only rootfs, dropped capabilities, service-account-token minimization, and an admission/enforcement decision.
- **Observed state**: Alloy and KSM raw Deployments implement the hardening set. Adminer Rollout omits pod/container hardening and token opt-out. KubeLinter excludes non-root/read-only/latest checks; no tracked PSA namespace labels, Gatekeeper/ConstraintTemplate, ValidatingAdmissionPolicy, or equivalent pod-hardening admission owner was found. Policy fallback does not test these controls.
- **Threat**: compromised workload gains writable/root-capable execution or API token access; PR-only lint does not prevent live drift.
- **Enforcement point**: pod templates, KubeLinter config, policy bundle/fallback, namespace labels/admission controller.
- **Evidence**: `gitops/platform/monitoring/alloy-k8s-logs.yaml#spec.template.spec.securityContext`; `gitops/platform/monitoring/kube-state-metrics.yaml#spec.template.spec.securityContext`; `gitops/workloads/adminer/rollout.yaml#spec.template.spec`; `.kube-linter.yaml#checks.exclude`; `policy/conftest/kubernetes.rego#deny[msg]`; `scripts/validate-policy-gates.sh#usage`.
- **Bypass / exception**: explicit home-lab exclusions exist, but no promotion/expiry/owner record bounds them to particular workloads.
- **Failure mode**: an unhardened Rollout passes current manifest/linter/policy checks or live admission accepts weaker workloads.
- **Approval authority**: workload owner plus platform/security for exceptions and admission design.
- **Evidence depth**: `repository-static`.
- **Verdict**: `Gap`.
- **Impact**: two raw deployments are hardened, but workload-class enforcement and production-like admission are absent.
- **Disposition**: `Integrate` provisionally with the local-versus-production baseline decision.
- **Canonical owner**: workload manifests, `.kube-linter.yaml`, policy bundle/fallback, and namespace/admission owner if adopted.
- **Verification**: Rollout-aware negative fixtures, exact exception inventory, optional Conftest parity, manifest/linter gates, and later authorized admission canary.
- **Uncertainty**: Adminer image requirements, Helm-rendered pod posture, cluster PSA/admission config, and live enforcement.
- **Blocker**: `BLK-WGA-SEC-001` blocks admission/live claims only.

#### WGA-SEC-007 — Non-latest controls do not establish immutable supply-chain identity

- **Request IDs**: `REQ-WGA-024`.
- **Scope**: Git target revisions, raw container/k3d images, Helm chart versions, Action/tool/dependency pins, SBOM/provenance/signature consumers.
- **Expected state**: each consumed artifact class has an explicit threat decision and, where required, immutable identity/verification plus a response owner; local deferral remains explicit.
- **Observed state**: Actions, downloaded Gitleaks, and Python requirements are strongly pinned/hashed. GitOps uses `targetRevision: main`; three raw pod images and k3d use tag-only identities; Helm Applications use versions without tracked artifact digest/signature; no SBOM/provenance/signature verifier/response consumer is current.
- **Threat**: mutable tag/branch/chart resolution or registry compromise changes deployed bytes without a reviewed desired-state identity change.
- **Enforcement point**: Application source revision, image fields, chart fields, registry/policy verification, and CI evidence consumer.
- **Evidence**: `.github/workflows/ci.yml#jobs.repo-quality-static`; `.github/requirements/ci-validation.txt`; `gitops/clusters/local/root-application.yaml#spec.source.targetRevision`; `gitops/clusters/local/applicationset-apps.yaml#spec.template.spec.source.targetRevision`; `gitops/workloads/adminer/rollout.yaml#spec.template.spec.containers[name=adminer].image`; `infrastructure/k3d/k3d-cluster.yaml#image`; `gitops/apps/root/platform-external-secrets-operator-app.yaml#spec.source.targetRevision`; `gitops/README.md#workload-image-and-kind-policy-matrix`.
- **Bypass / exception**: current local-home-lab policy accepts explicit non-latest tag/version and accurately defers stronger identity; no production-like exception route is defined.
- **Failure mode**: a tag/main/chart version resolves to different bytes while all current static gates remain green.
- **Approval authority**: platform/security architecture owner and artifact consumer owner.
- **Evidence depth**: `repository-static`.
- **Verdict**: `Partial`.
- **Impact**: CI tooling integrity is strong, but deployable artifact identity and response evidence are incomplete.
- **Disposition**: `Integrate` provisionally through threat-modelled scope, not blanket tooling adoption.
- **Canonical owner**: GitOps Application/image/chart desired state and validation supply-chain owners by artifact class.
- **Verification**: artifact inventory, adopt/defer decisions, immutable-reference negative fixtures where adopted, verifier output consumer, rollback and registry/hosted evidence.
- **Uncertainty**: registry/chart signatures, SBOM/provenance availability, remote branch protection, actual pulled digests, and response process.
- **Blocker**: `BLK-WGA-SEC-001` limits hosted/registry/live proof.

#### WGA-SEC-008 — Secret references and local Vault/ESO boundaries align statically

- **Request IDs**: `REQ-WGA-024`.
- **Scope**: tracked Secret kinds, ExternalSecret/ClusterSecretStore, Vault policy/auth identity/audience, bootstrap TLS/token/value flow, local-only transport exception.
- **Expected state**: no values in desired state, purpose-specific references/identity, verified external bootstrap TLS, non-argv secret flow, and explicit local exception boundaries.
- **Observed state**: zero raw Secret kinds; bounded scanner passes; Vault/ESO contract passes 10 self-test cases and production; bootstrap requires HTTPS/CA and pipes token/value data without command-line literals; the in-cluster store is annotated local-only HTTP and documentation rejects production TLS inference.
- **Threat**: plaintext value, broad Vault policy, argv/log leakage, identity mismatch, or local HTTP exception reused outside local.
- **Enforcement point**: scanner, store/ExternalSecret/RBAC/HCL contracts, bootstrap functions, and local annotation/documentation.
- **Evidence**: `gitops/platform/eso/vault-secret-store.yaml#kind=ClusterSecretStore`; `gitops/platform/eso/postgres-app-secret.yaml#kind=ExternalSecret`; `gitops/platform/eso/vault-token-reviewer-binding.yaml#kind=ClusterRoleBinding`; `infrastructure/vault/policies/eso-read.hcl#path`; `infrastructure/bootstrap-local.sh#vault_curl`; `infrastructure/bootstrap-local.sh#cleanup_sensitive`; `scripts/validate-vault-eso-contracts.py#main`; `scripts/check-secret-handling.sh#add_scan_root`; `gitops/README.md#secret-management-responsibility-matrix`.
- **Bypass / exception**: annotated local-only HTTP inside the home-lab service path and approved bootstrap-only mutation; neither is production-like or live proof.
- **Failure mode**: tracked reference/value drift, insecure external bootstrap, local exception reuse, or live Vault/ESO mismatch.
- **Approval authority**: platform/security for desired state; Vault/operator for auth, policy attachment, values, and live rotation.
- **Evidence depth**: `repository-static`.
- **Verdict**: `Aligned`.
- **Impact**: the declared local secret-reference contract is exact and value-free without concealing the transport/live limits.
- **Disposition**: `Keep`.
- **Canonical owner**: GitOps ESO manifests, Vault HCL, bootstrap, GitOps responsibility matrix, and validators by concern.
- **Verification**: bounded scanner, Vault/ESO self-test/production, manifest/policy/static-infrastructure gates; separately approved live rotation/reconciliation if needed.
- **Uncertainty**: generated Secret contents/storage/access, live Vault policy/auth, transport packet behavior, rotation, and delivery.
- **Blocker**: `BLK-WGA-SEC-001` blocks live promotion only; `BLK-WGA-SEC-002` separately blocks a clean-history claim.

#### WGA-SEC-009 — Hosted, provider, remote, and live enforcement remain deferred

- **Request IDs**: `REQ-WGA-024`.
- **Scope**: hosted workflow/ruleset, native provider permission loading, Git remote action, cluster admission/RBAC/CNI, Argo reconciliation, Vault/ESO, registry, cloud, and operator behavior.
- **Expected state**: no deeper-lane claim or action occurs without explicit authority, redaction, target, rollback, and owner.
- **Observed state**: this audit used tracked files and local static tools only; every deeper surface remains unobserved.
- **Threat**: false assurance or unauthorized action caused by treating static configuration as enforcement.
- **Enforcement point**: Stage 00 approval stop and future lane-specific runbook/evidence record.
- **Evidence**: `docs/00.agent-governance/rules/approval-boundaries.md#default-stance`; `docs/00.agent-governance/rules/approval-boundaries.md#approval-matrix`; `gitops/README.md#validation`; `infrastructure/tests/verify-network-policies.sh#platform_np`; `infrastructure/tests/verify-secrets.sh#store_ready`.
- **Bypass / exception**: none during WGIA-008; later human/operator approval must remain action-specific.
- **Failure mode**: static PASS is reported as hosted/provider/live PASS or an action begins without approval.
- **Approval authority**: user/operator and lane owner.
- **Evidence depth**: `repository-static`.
- **Verdict**: `DEFER`.
- **Impact**: current findings are bounded and cannot establish effective runtime security.
- **Disposition**: `Keep` the boundary and route only accepted future verification.
- **Canonical owner**: Stage 00 approval matrix and lane-specific provider/workflow/runbook owners.
- **Verification**: separately authorized, redacted, non-mutating evidence first; mutation only through approved runbook.
- **Uncertainty**: all effective hosted/provider/remote/live controls and outcomes.
- **Blocker**: `BLK-WGA-SEC-001`.

## Sources

Source roles are closed to `policy owner`, `machine owner`, `human index`,
`evidence producer`, and `historical snapshot`.

| Source ID | Source role | Evidence at the observation commit | Use |
| --- | --- | --- | --- |
| SRC-WGA-SEC-001 | policy owner | `docs/00.agent-governance/rules/approval-boundaries.md#approval-matrix`; `docs/00.agent-governance/rules/git-workflow.md#rules`; `docs/00.agent-governance/scopes/security.md#file-ownership` | Shared approvals, Git, and security ownership. |
| SRC-WGA-SEC-002 | machine owner | `.claude/settings.json#permissions`; `.github/workflows/ci.yml#jobs`; `.kube-linter.yaml#checks.exclude`; `.gitleaks.toml#rules`; `policy/conftest/kubernetes.rego#deny[msg]`; `gitops/platform/monitoring/kube-state-metrics.yaml#kind=ClusterRole,metadata.name=kube-state-metrics`; `gitops/platform/network-policies/kustomization.yaml#resources` | Tracked permission and security-control intent. |
| SRC-WGA-SEC-003 | evidence producer | `scripts/validate-github-actions-security.py#main`; `scripts/validate-ci-python-contract.py#main`; `scripts/check-secret-handling.sh#add_scan_root`; `scripts/validate-policy-gates.sh#usage`; `scripts/validate-k8s-manifests.sh#YAML_TARGETS`; `scripts/validate-gitops-structure.sh#ROOT_APP`; `scripts/validate-gitops-change-set.py#main`; `scripts/validate-vault-eso-contracts.py#main`; `infrastructure/tests/verify-contracts-static.sh#require_pattern` | Deterministic local results and exact limitations. |
| SRC-WGA-SEC-004 | human index | `gitops/README.md#service-coverage-matrix`; `gitops/README.md#workload-image-and-kind-policy-matrix`; `gitops/README.md#secret-management-responsibility-matrix`; `gitops/README.md#current-hardening-deferrals` | Current local-home-lab boundaries; machine owners win. |
| SRC-WGA-SEC-005 | historical snapshot | `docs/90.references/audits/2026-07-11-weia/kubernetes-infrastructure-security.md#actionable-finding-register` | Historical comparison only; current/observation owners and probes override stale facts. |

## Review and Freshness

- Review status: `Approved`; fresh specification/content and security
  fix-round reviews found no Critical/Important issue against VAL-WGA-009.
- Review disposition: the bounded WGIA-008 report and WGIA-011 remediation are
  `Approved`; fresh specification/content, Python/quality, and security reviews
  are `Approved`, and the exact staged complete repository quality gate passes.
  Of six WGIA-008 roadmap inputs, the admitted
  Claude row is implemented and the other five remain `DEFER`.
- Focused document evidence: the WGIA-008 observation probe passed nine
  findings, 14 conceptual fields each, six candidate routes, and 42 unique
  observation-commit evidence paths with zero missing. WGIA-011 reclassifies
  only `WGA-SEC-002` from `Conflict` to repository-static `Aligned`; strict
  registry reports 502 paths, Markdown profiles report zero
  violations, strict links are valid, and diff/Stage 98 checks pass. The first
  strict-validator invocation used unsupported `--strict` syntax and exited 2
  at argument parsing; corrected `--mode strict` invocations pass.
- Evidence observed: 2026-08-09 at exact observation commit
  `50628b84165479b03efc0a25be075a49c91a9aef`, compared with starting HEAD
  `e4ed34d56f7b90a12771232c7bfe54d5c4d6f94e`.
- Current-truth owners: Stage 00 approval/Git/provider rules, workflow/locks,
  GitOps/infrastructure/policy/secret references, and exact validators.
- Refresh triggers: permission, approval, secret scan/triage, RBAC, namespace,
  NetworkPolicy, workload context, admission, image/chart/Git identity,
  exception, provider/hosted/live evidence, observation commit, or verdict.
- Hosted, provider-runtime, authenticated, credential-bearing, secret-value,
  remote, registry, cluster, GitOps, Vault/ESO, cloud, and live evidence remains
  `DEFER`.
- No disposition-ledger row is warranted: no Legacy, Deprecated, one-shot, or
  deletion candidate was proven.

## Related Documents

- [Pack Index](README.md)
- [Spec 054](../../../03.specs/0055-workspace-governance-audit-and-remediation/spec.md)
- [Implementation Plan](../../../03.specs/0055-workspace-governance-audit-and-remediation/plan.md)
- [Implementation Task](../../../03.specs/0055-workspace-governance-audit-and-remediation/tasks.md)
- [Approval Boundaries](../../../00.agent-governance/rules/approval-boundaries.md)
- [GitOps README](../../../../gitops/README.md)
