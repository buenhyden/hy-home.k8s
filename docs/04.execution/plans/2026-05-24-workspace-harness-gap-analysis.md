---
title: 'Workspace Harness Gap Analysis Implementation Plan'
type: plan
status: done
owner: 'platform'
updated: 2026-05-26
---

# Workspace Harness Gap Analysis Implementation Plan

## Overview (KR)

이 문서는 `hy-home.k8s`가 WSL2, WSL Linux native Docker, k3d, ArgoCD GitOps,
External Secrets, Vault, PostgreSQL, Valkey, SDD, QA, CI/CD, AI Agent 협업
규칙을 일관되게 지탱하는지 감사하고 보강하는 실행 계획이다.

## Context

이 작업은 이전 6개 role-based subagent 리뷰와 baseline static verification을
이어받는다. `grill-with-docs` 검토 결과에 따라 `AGENTS.md`는 thin gateway로
유지하고, recurring workflow와 task-to-skill routing은 기존 runtime SSoT인
`docs/00.agent-governance/harness-catalog.md`에 통합한다.

## Current-State Navigation (2026-05-26)

| Current record | Use for | Evidence anchor | Status |
| --- | --- | --- | --- |
| GitOps Image and Kind Policy Scan Guardrail Overlay | Current repo-static guardrail for active workload image tag policy, raw platform pod template image tags, and workload kind membership in the apps AppProject whitelist | VAL-SPC-006-050; T-237 through T-242 | Current |
| Targeted Residual-Area Audit Overlay | Current continuation audit for `scripts/`, `gitops/`, `infrastructure/`, and `docs/05.operations`, including operations high-risk command boundary SSoT | VAL-SPC-006-049; T-231 through T-236 | Current |
| Traefik 443 Runtime Proof Overlay | Current approved runtime follow-up proving ingress-nginx fallback passes but external Traefik 443 is not reachable because no external gateway runtime is present | VAL-SPC-006-048; T-227 through T-230 | Current |
| Default Kubeconfig TLS Repair Overlay | Current approved runtime follow-up proving default kubeconfig TLS trust repair and default `run-all.sh` live validation pass | VAL-SPC-006-047; T-222 through T-226 | Current |
| Temporary Kubeconfig Live Validation Overlay | Current approved runtime follow-up proving read-only live validation passes with a k3d-generated temporary kubeconfig while default kubeconfig TLS trust remains unrepaired | VAL-SPC-006-046; T-217 through T-221 | Current |
| Script Classification Matrix Guardrail Overlay | Current guardrail follow-up for task-contract script classifications and deletion/consolidation candidate evidence in `scripts/README.md` | VAL-SPC-006-045; T-212 through T-216 | Current |
| Docker Network and RBAC Create Boundary Guardrail Overlay | Current guardrail follow-up for Docker network mutation and RBAC create command safety markers in operations docs | VAL-SPC-006-044; T-207 through T-211 | Current |
| Vault Policy Write Boundary Guardrail Overlay | Current guardrail follow-up for `vault policy write` command safety markers in operations docs | VAL-SPC-006-043; T-202 through T-206 | Current |
| App Onboarding Secret Path Contract Guardrail Overlay | Current guardrail follow-up for Vault CLI path versus ESO `remoteRef.key` consistency across operations, sample app, and GitOps docs | VAL-SPC-006-042; T-197 through T-201 | Current |
| GitHub Workflow Responsibility Matrix Guardrail Overlay | Current guardrail follow-up for QA gate, release-evidence, and maintenance workflow responsibility boundaries | VAL-SPC-006-041; T-192 through T-196 | Current |
| Bootstrap Boundary Matrix Guardrail Overlay | Current guardrail follow-up for k3d creation, ArgoCD install, root app apply, Vault connection, and PostgreSQL/Valkey connection responsibility boundaries | VAL-SPC-006-040; T-187 through T-191 | Current |
| Secret Management Responsibility Matrix Guardrail Overlay | Current guardrail follow-up for ESO, ClusterSecretStore, Vault auth, ExternalSecret naming, secret value handling, and verification responsibility SSoT | VAL-SPC-006-039; T-182 through T-186 | Current |
| External Service Contract Matrix Guardrail Overlay | Current guardrail follow-up for PostgreSQL/Valkey/Vault host, port, secret key, TLS/CA, rotation, namespace, and verification contract SSoT | VAL-SPC-006-038; T-177 through T-181 | Current |
| WSL2 Runtime Prerequisite Guardrail Overlay | Current guardrail follow-up for WSL2, WSL-native Docker, k3d, kubectl, kubeconfig/TLS, port, and WSL networking prerequisite SSoT | VAL-SPC-006-037; T-172 through T-176 | Current |
| Examples Role Matrix Guardrail Overlay | Current guardrail follow-up for `examples/` onboarding/reference-only role boundaries and sample-app/adminer separation | VAL-SPC-006-036; T-167 through T-171 | Current |
| Scripts Broad Reference Guardrail Overlay | Current guardrail follow-up for tracked `scripts/*.sh` reference safety during deletion or rename prechecks | VAL-SPC-006-035; T-162 through T-166 | Current |
| Operations Incidents Boundary Guardrail Overlay | Current guardrail follow-up for `docs/05.operations/incidents/README.md` incident/postmortem routing and no-incident state | VAL-SPC-006-034; T-157 through T-161 | Current |
| Infrastructure Coverage Matrix Guardrail Overlay | Current guardrail follow-up for `infrastructure/README.md` coverage matrix drift | VAL-SPC-006-033; T-152 through T-156 | Current |
| GitOps Coverage Matrix Guardrail Overlay | Current guardrail follow-up for `gitops/README.md` and `gitops/workloads/README.md` coverage matrix drift | VAL-SPC-006-032; T-147 through T-151 | Current |
| Operations Routing Matrix Guardrail Overlay | Current guardrail follow-up for `docs/05.operations/` stage bucket and template routing | VAL-SPC-006-031; T-142 through T-146 | Current |
| Traefik Route Inventory Guardrail Overlay | Current guardrail follow-up for `traefik/*.yaml` route inventory and backend drift checks | VAL-SPC-006-030; T-137 through T-141 | Current |
| Infrastructure Test Inventory Guardrail Overlay | Current guardrail follow-up for `infrastructure/tests/*.sh` inventory and `run-all.sh` live-test parity | VAL-SPC-006-029; T-132 through T-136 | Current |
| GitOps Hierarchy Guardrail Overlay | Current guardrail follow-up for root app, platform app, and workload ApplicationSet hierarchy | VAL-SPC-006-028; T-127 through T-131 | Current |
| Environment Key Contract Guardrail Overlay | Current guardrail follow-up for `.env.example` and local `.env` key-only consistency | VAL-SPC-006-027; T-122 through T-126 | Current |
| Scripts Inventory Guardrail Overlay | Current guardrail follow-up for `scripts/` deletion/consolidation inventory evidence | VAL-SPC-006-026; T-117 through T-121 | Current |
| Operations Index Guardrail Overlay | Current guardrail follow-up for `docs/05.operations` README index/frontmatter sync | VAL-SPC-006-025; T-112 through T-116 | Current |
| Residual Objective Completion Audit Overlay | Current final continuation audit for remaining broad objective axes beyond the four named follow-up paths | VAL-SPC-006-024; T-107 through T-111 | Current |
| Unreviewed-Area Follow-up Overlay | Current follow-up audit for weak or unreviewed evidence in `scripts/`, `gitops/`, `infrastructure/`, and `docs/05.operations` | VAL-SPC-006-023; T-101 through T-106 | Current |
| Documentation/Governance-First Workspace Improvement Overlay | Current approved limited implementation for P0-01 through P0-22, fresh six-review overlay, P1 docs/governance edits, verification, checklist, and final report | VAL-SPC-006-022; T-091 through T-100 | Current |
| Live Bootstrap Runtime Closure Overlay | Historical approved runtime closure with live bootstrap and full runtime validation evidence | VAL-SPC-006-021; T-084 through T-090 | Historical evidence |
| Post-Merge Completion Audit Overlay | Historical PR #39 merged-main and static/liveness blocker snapshot | VAL-SPC-006-020; T-081 through T-083 | Historical evidence |
| Earlier overlays in this file | Prior audit, skill, P0, deferred item, and task-unit evidence | VAL-SPC-006-001 through VAL-SPC-006-019 | Historical evidence |

Use the newest dated overlay for current state. Preserve older overlays as
evidence snapshots unless a later overlay explicitly supersedes them.

## GitOps Image and Kind Policy Scan Guardrail Overlay

This overlay follows the active-goal review for a previously deferred GitOps
hardening item. It keeps the change repo-static and documentation/governance:
no Kubernetes manifests, AppProject permissions, ApplicationSet behavior,
namespace ownership, live cluster state, CI job structure, secret policy, or
`.env` values are changed.

### Gap Delta

| Area | Gap | Evidence path | Impact | Risk | Action type | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| GitOps image tag policy scan | Active workload and raw platform pod-template images were documented by manifests but not protected by a reusable repo-quality guardrail against `latest` or untagged images | `gitops/workloads/adminer/rollout.yaml`; `gitops/platform/monitoring/`; `gitops/README.md` | A future active workload or platform pod template could introduce a mutable image tag while existing YAML syntax checks still pass | Medium | improvement | P1 |
| Workload kind policy scan | The `apps` AppProject whitelist existed, but active workload manifest kinds were not checked against `namespaceResourceWhitelist` by the broad quality gate | `gitops/clusters/local/appproject-apps.yaml`; `gitops/workloads/adminer/` | App onboarding could add a kind outside the intended apps project boundary without an early repo-static failure | Medium | improvement | P1 |
| Example placeholder boundary | `examples/sample-app` intentionally contains image placeholders, but that exception needed to stay separate from active ApplicationSet desired state | `examples/sample-app/rollout.yaml`; `gitops/README.md` | A template placeholder could be mistaken for an allowed active workload image pattern | Low | supplementation | P1 |

### Implementation Plan Delta

| Priority | Action type | Target | Change | Linked task | Verification | Rollback |
| --- | --- | --- | --- | --- | --- | --- |
| P1 | documentation | `gitops/README.md` | Add Workload Image and Kind Policy Matrix for active workloads, raw platform pod templates, and sample-app placeholder boundaries | T-238 | repo quality and README review | Revert matrix and deferral wording |
| P1 | guardrail | `scripts/validate-repo-quality-gates.sh` | Validate active workload images, raw platform pod-template images, workload kind membership in `apps` AppProject `namespaceResourceWhitelist`, and README evidence rows | T-239 | repo quality gate and shell syntax | Revert validator block |
| P1 | documentation | `scripts/README.md` | Align command contract wording with the new GitOps image/workload-kind policy matrix guardrail | T-240 | scripts README review | Revert wording |
| P1 | evidence | 006 Spec/Plan/Task/progress | Record VAL-SPC-006-050, implementation decisions, verification, and remaining semantic deferrals | T-241, T-242 | SDD chain check | Revert overlay entries |

### Verification Result

| Command or method | Result | Notes |
| --- | --- | --- |
| current manifest and AppProject inspection | PASS | Active workload image is `adminer:4.8.1`; active workload kinds are covered by the apps AppProject whitelist |
| repo-static verification | PASS | `validate-repo-quality-gates.sh`, GitOps structure, manifest syntax, secret scan, static contracts, shell syntax, JSON parse, workflow YAML parse, env key-name comparison, wiki check, and diff check passed |
| remaining deferrals | recorded | AppProject allow-list tightening, `CreateNamespace=true` ownership, CI failure-mode changes, OPA/Conftest, kube-linter enforcement, and live runtime mutation remain outside this pass |

## Targeted Residual-Area Audit Overlay

This overlay follows the continuation request to check whether any requested
area remains unreviewed and proceed where safe. It changes only documentation
and SDD evidence. It does not change Kubernetes manifests, ArgoCD semantics,
AppProject permissions, Docker networks, external services, secret policy,
`.env` values, live cluster state, or CI job structure.

### Coverage Ledger Delta

| Area | Current status | Evidence path | Gap decision | Next action |
| --- | --- | --- | --- | --- |
| `scripts/` deletion/consolidation | complete repo-static | `scripts/README.md`; `scripts/validate-repo-quality-gates.sh`; executable bits | No deletion-ready or consolidation-ready script; keep all five scripts | Keep deletion/rename precheck guardrails |
| `gitops/` implemented infrastructure | partial | `gitops/README.md`; `scripts/validate-gitops-structure.sh`; `infrastructure/tests/verify-contracts-static.sh` | Static hierarchy/contracts pass; semantic hardening remains deferred | Keep AppProject, namespace ownership, image/workload-kind policy changes in P3 follow-up |
| `infrastructure/` implemented infrastructure | partial | `infrastructure/README.md`; `infrastructure/tests/run-all.sh`; `CHECK_TRAEFIK_443=true` check | Default live aggregate passes; external Traefik 443 runtime proof remains outside this repo | Keep external gateway proof in `hy-home.docker` operations boundary |
| `docs/05.operations/` structure | complete repo-static | `docs/05.operations/README.md`; operations subfolder READMEs; repo quality gate | Bucket routing, indexes, frontmatter, incident boundary, and high-risk command boundary are guarded | Keep new operation docs on the same routing/mutation-boundary contract |

### Gap Delta

| Area | Gap | Evidence path | Impact | Risk | Action type | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| Operations mutation-boundary SSoT | The reusable gate already scans high-risk command examples, but the operations stage entrypoint did not name that gate-level command-boundary contract explicitly | `docs/05.operations/README.md`; `scripts/validate-repo-quality-gates.sh` | Operators and agents could miss that live mutation examples need nearby approved-context markers | Low | supplementation | P1 |
| Script command contract wording | `scripts/README.md` described several specific boundary checks but under-reported the broader operations high-risk command boundary covered by the gate | `scripts/README.md`; `scripts/validate-repo-quality-gates.sh` | Script inventory and command-contract SSoT could lag validator behavior | Low | supplementation | P1 |
| External Traefik proof boundary | GitOps and infrastructure entrypoints did not both point readers from k3d ingress fallback success to the external gateway runtime proof gap | `gitops/README.md`; `infrastructure/README.md`; `traefik/README.md` | Readers could confuse GitOps/live fallback success with external gateway readiness | Medium | supplementation | P1 |

### Implementation Plan Delta

| Priority | Action type | Target | Change | Linked task | Verification | Rollback |
| --- | --- | --- | --- | --- | --- | --- |
| P1 | documentation | `docs/05.operations/README.md` | Add operations mutation-boundary SSoT for high-risk command examples and repo-quality enforcement | T-232 | repo quality gate | Revert README section |
| P1 | documentation | `scripts/README.md` | Align `validate-repo-quality-gates.sh` contract wording with operations high-risk command boundary scans | T-233 | repo quality gate and diff check | Revert README wording |
| P1 | documentation | `gitops/README.md`; `infrastructure/README.md` | Record external Traefik 443 proof as outside GitOps desired state and external to default live aggregate fallback proof | T-234 | GitOps/static/live checks | Revert README wording |
| P1 | evidence | 006 Spec/Plan/Task/progress | Record VAL-SPC-006-049, residual audit status, verification, and remaining deferrals | T-235, T-236 | SDD chain check | Revert overlay entries |

### Verification Result

| Command or method | Result | Notes |
| --- | --- | --- |
| current worktree inventory and targeted search | PASS | No untracked unreviewed target files found in the four named areas; high-risk operations commands are covered by repo-quality boundary rules |
| `bash scripts/validate-repo-quality-gates.sh .` | PASS | Repository quality gates passed after operations/script/GitOps/infrastructure README updates |
| `bash scripts/generate-llm-wiki-index.sh --check` | PASS | Generated LLM Wiki index remained current |
| `bash scripts/validate-gitops-structure.sh` | PASS | Root Application, ApplicationSet, hierarchy, and Kustomize completeness checks passed |
| `bash infrastructure/tests/verify-contracts-static.sh` | PASS | Static GitOps, Vault, external service, AppProject, and workload contracts passed |
| `bash scripts/validate-k8s-manifests.sh .` | PASS | YAML syntax passed; optional kube-linter skipped because it is not installed |
| `bash scripts/check-secret-handling.sh .` | PASS | Plaintext secret scan passed |
| `find infrastructure scripts .claude/hooks -type f -name '*.sh' -exec bash -n {} +` | PASS | Shell syntax passed |
| JSON/workflow/env metadata checks | PASS | `.claude/settings.json`, `.codex/hooks.json`, workflow YAML parse, and `.env.example`/`.env` key-name comparison passed |
| `bash infrastructure/tests/run-all.sh` | PASS | Default live aggregate passed with Traefik 443 enforcement skipped |
| `CHECK_TRAEFIK_443=true bash infrastructure/tests/verify-ingress-tls.sh` | EXPECTED FAIL | External Traefik endpoint is not reachable; Docker inventory shows no separate external Traefik gateway container |

## Traefik 443 Runtime Proof Overlay

This overlay follows explicit approval for approval-gated items. It keeps the
check read-only: no external Traefik gateway is started, no dynamic config is
copied into `hy-home.docker`, no Kubernetes resource is mutated, and no Docker
network is changed.

### Gap Delta

| Area | Gap | Evidence path | Impact | Risk | Action type | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| External Traefik runtime proof | Default live ingress/TLS validation passes through ingress-nginx fallback, but `CHECK_TRAEFIK_443=true` fails because the external Traefik gateway endpoint is not reachable | `infrastructure/tests/verify-ingress-tls.sh`; `docker ps`; `traefik/README.md` | Operators could mistake a k3d GitOps success for full external gateway readiness | Medium | supplementation | P2 |

### Implementation Plan Delta

| Priority | Action type | Target | Change | Linked task | Verification | Rollback |
| --- | --- | --- | --- | --- | --- | --- |
| P2 | live read-only validation | `infrastructure/tests/verify-ingress-tls.sh`; Docker runtime | Run `CHECK_TRAEFIK_443=true` and inspect Docker inventory for external gateway presence | T-227, T-228 | command output and exit status | N/A; read-only |
| P1 | documentation | `traefik/README.md` | Clarify that Traefik 443 failure with no external gateway container is a `hy-home.docker` runtime/dynamic-config proof gap, not a k3d GitOps desired-state failure | T-229 | repo quality and manifest checks | Revert README note |
| P1 | evidence | 006 Spec/Plan/Task/progress | Record VAL-SPC-006-048 and verification | T-229, T-230 | repo quality and diff check | Revert overlay entries |

### Verification Result

| Command or method | Result | Notes |
| --- | --- | --- |
| `CHECK_TRAEFIK_443=true bash infrastructure/tests/verify-ingress-tls.sh` | FAIL | `Traefik 443 endpoint is not reachable (argocd.127.0.0.1.nip.io:443)` |
| `docker ps --format '{{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}'` | PASS | No external Traefik gateway container was present in the current Docker inventory |
| `bash infrastructure/tests/run-all.sh` | PASS | k3d ingress/TLS fallback path passed with Traefik 443 enforcement skipped |

## Default Kubeconfig TLS Repair Overlay

This overlay follows explicit approval for approval-gated items. It changes
only local kubeconfig state: no repository manifest, Kubernetes resource,
Docker network, Vault policy, secret value, or `.env` value is changed.

### Gap Delta

| Area | Gap | Evidence path | Impact | Risk | Action type | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| Default kubeconfig TLS trust | Live platform health was proven through a temporary k3d kubeconfig, but default `~/.kube/config` still failed TLS verification | `kubectl version --request-timeout=5s`; `infrastructure/tests/run-all.sh`; `~/.kube/config` metadata | Routine local validation would still fail unless the operator remembered to set `KUBECONFIG` | Medium | improvement | P1 |

### Implementation Plan Delta

| Priority | Action type | Target | Change | Linked task | Verification | Rollback |
| --- | --- | --- | --- | --- | --- | --- |
| P1 | local runtime repair | `~/.kube/config` | Back up default kubeconfig and merge k3d `hyhome` kubeconfig into the default kubeconfig | T-222, T-223 | `kubectl version`; `run-all.sh` | Restore `~/.kube/config.codex-backup-20260526T-k3d-hyhome-tls-repair` to `~/.kube/config` |
| P1 | documentation | `infrastructure/README.md` | Document approved repair command, verification, and rollback boundary | T-225 | repo quality and static checks | Revert README note |
| P1 | evidence | 006 Spec/Plan/Task/progress | Record VAL-SPC-006-047 and verification | T-225, T-226 | repo quality and diff check | Revert overlay entries |

### Verification Result

| Command or method | Result | Notes |
| --- | --- | --- |
| default kubeconfig backup | PASS | Backup exists at `~/.kube/config.codex-backup-20260526T-k3d-hyhome-tls-repair` |
| `k3d kubeconfig merge hyhome --kubeconfig-merge-default --kubeconfig-switch-context` | PASS | Default kubeconfig updated by k3d |
| `kubectl config current-context` | PASS | Current context is `k3d-hyhome` |
| `kubectl version --request-timeout=5s` | PASS | API server reached with default kubeconfig; kubectl reported client/server minor version skew warning |
| `bash infrastructure/tests/run-all.sh` | PASS | Cluster topology, MetalLB, GitOps, ESO/Vault, external services, network policy, and ingress/TLS checks passed; Traefik 443 enforcement stayed skipped by default |

## Temporary Kubeconfig Live Validation Overlay

This overlay follows explicit approval to proceed on approval-gated items. It
keeps the runtime action read-only: no Kubernetes resource, Docker network,
Vault policy, secret value, `.env` value, or `~/.kube/config` file is changed.

### Gap Delta

| Area | Gap | Evidence path | Impact | Risk | Action type | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| Live runtime proof | Default kubeconfig still fails TLS trust even though Docker, k3d, and external-service containers are running | `kubectl version --request-timeout=5s`; `docker ps`; `k3d cluster list` | Static pass could still be mistaken for live readiness unless the kubeconfig failure mode is separated from cluster health | Medium | supplementation | P1 |
| Kubeconfig diagnostic boundary | Existing docs said a temporary `KUBECONFIG` can be intentional, but did not record the approved temporary-kubeconfig live validation path and result | `infrastructure/README.md`; `infrastructure/tests/run-all.sh` | Operators could repair `~/.kube/config` unnecessarily before proving the live platform state | Low | improvement | P1 |

### Implementation Plan Delta

| Priority | Action type | Target | Change | Linked task | Verification | Rollback |
| --- | --- | --- | --- | --- | --- | --- |
| P1 | live read-only validation | Docker, k3d, kubectl, `infrastructure/tests/run-all.sh` | Confirm default kubeconfig blocker, generate k3d temporary kubeconfig under `/tmp`, and run the aggregate live validation with `KUBECONFIG` set | T-217 through T-219 | command output and exit status | Remove temporary `/tmp` kubeconfig if desired; no repo rollback needed |
| P1 | documentation | `infrastructure/README.md` | Document temporary-kubeconfig diagnostic boundary without claiming default kubeconfig repair | T-220 | repo quality and static checks | Revert README note |
| P1 | evidence | 006 Spec/Plan/Task/progress | Record VAL-SPC-006-046 and verification | T-220, T-221 | repo quality and diff check | Revert overlay entries |

### Verification Result

| Command or method | Result | Notes |
| --- | --- | --- |
| `docker context show` | PASS | Docker context is `default` |
| `docker ps --format '{{.Names}}\t{{.Status}}\t{{.Ports}}'` | PASS | PostgreSQL, Vault, Valkey, and k3d containers were running |
| `k3d cluster list` | PASS | `hyhome` showed `1/1` server, `3/3` agents, load balancer enabled |
| `kubectl config current-context` | PASS | Current context is `k3d-hyhome` |
| `kubectl version --request-timeout=5s` | BLOCKED | Default kubeconfig still fails TLS trust with `x509: certificate signed by unknown authority` |
| `k3d kubeconfig get hyhome > /tmp/hy-home-k8s-k3d-hyhome.kubeconfig` | PASS | Temporary kubeconfig generated under `/tmp`; `~/.kube/config` not modified |
| `KUBECONFIG=/tmp/hy-home-k8s-k3d-hyhome.kubeconfig kubectl version --request-timeout=5s` | PASS | API server reached; kubectl reported client/server minor version skew warning |
| `KUBECONFIG=/tmp/hy-home-k8s-k3d-hyhome.kubeconfig bash infrastructure/tests/run-all.sh` | PASS | Cluster topology, MetalLB, GitOps, ESO/Vault, external services, network policy, and ingress/TLS checks passed; Traefik 443 enforcement stayed skipped by default |
| temporary kubeconfig cleanup | PASS | `/tmp/hy-home-k8s-k3d-hyhome.kubeconfig` removed after validation |

## Script Classification Matrix Guardrail Overlay

This overlay follows the continuation audit for `scripts/` deletion and
consolidation evidence. It keeps the change documentation/governance and
repo-static: no script is deleted, renamed, consolidated, or removed from a
command surface.

### Gap Delta

| Area | Gap | Evidence path | Impact | Risk | Action type | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| Script classification SSoT | The 006 plan recorded `operations-critical/reusable` and `development-helper/reusable` classifications, but `scripts/README.md` and the reusable repo-quality gate did not require the task-contract classification terms per active script | `scripts/README.md`; `scripts/validate-repo-quality-gates.sh`; 006 plan scripts reviewer ledger | Future deletion/consolidation reviews could keep Tier evidence while losing the explicit `one-off`, `reusable`, `operations-critical`, `development-helper`, `unknown` classification vocabulary requested by the task contract | Low | improvement | P1 |

### Implementation Plan Delta

| Priority | Action type | Target | Change | Linked task | Verification | Rollback |
| --- | --- | --- | --- | --- | --- | --- |
| P1 | documentation | `scripts/README.md` | Add a Script Classification Matrix covering all active scripts, current deletion candidate state, current consolidation candidate state, and evidence | T-213 | targeted matrix check and repo quality | Revert classification matrix and command-contract wording |
| P1 | guardrail | `scripts/validate-repo-quality-gates.sh` | Validate the Script Classification Matrix header, row coverage, allowed classification terms, expected current classifications, and no deletion/consolidation candidates | T-212, T-214 | shell syntax and repo quality | Revert validator block |
| P1 | evidence | 006 Spec/Plan/Task/progress | Record VAL-SPC-006-045 and verification | T-215, T-216 | repo quality and diff check | Revert overlay entries |

### Verification Result

| Command or method | Result | Notes |
| --- | --- | --- |
| `bash -n scripts/validate-repo-quality-gates.sh` | PASS | Validator shell syntax after matrix guardrail edit |
| `bash scripts/validate-repo-quality-gates.sh .` | PASS | New Script Classification Matrix guardrail |
| targeted script classification matrix check | PASS | Active script rows use expected task-contract classifications |
| `bash scripts/generate-llm-wiki-index.sh --check` | PASS | Generated reference index remained current |
| `bash scripts/validate-gitops-structure.sh` | PASS | GitOps hierarchy still validates after documentation/guardrail change |
| `bash scripts/validate-k8s-manifests.sh .` | PASS | YAML syntax passed; optional kube-linter remained unavailable |
| `bash scripts/check-secret-handling.sh .` | PASS | No plaintext secret patterns found |
| `bash infrastructure/tests/verify-contracts-static.sh` | PASS | Static infrastructure/GitOps contracts passed |
| `git diff --check` | PASS | Whitespace check after verification record update |

## Docker Network and RBAC Create Boundary Guardrail Overlay

This overlay follows the continuation audit for `docs/05.operations` command
safety. It keeps the change documentation/governance and repo-static: no Docker
network is changed, no Kubernetes RBAC object is created, and no live cluster
state is mutated.

### Gap Delta

| Area | Gap | Evidence path | Impact | Risk | Action type | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| Docker network mutation boundary | The reusable command boundary gate did not validate `docker network connect`, while WSL2/Vault recovery docs include that command for k3d network attachment | `scripts/validate-repo-quality-gates.sh`; `docs/05.operations/guides/0002-wsl2-k3d-argocd-ha-setup-guide.md`; `docs/05.operations/runbooks/0002-argocd-eso-vault-recovery-runbook.md` | Agents or operators could treat Docker network mutation as a routine doc command rather than approval-bound bootstrap/break-glass work | Medium | improvement | P1 |
| RBAC create boundary | The reusable command boundary gate covered `kubectl apply/patch` but not `kubectl create clusterrolebinding`, while Headlamp docs include RBAC creation examples | `docs/05.operations/guides/0004-headlamp-auth-oidc-guide.md`; `docs/05.operations/runbooks/0005-headlamp-keycloak-runbook.md` | RBAC escalation examples could lose explicit approval context while still passing repo quality | Medium | improvement | P1 |

### Implementation Plan Delta

| Priority | Action type | Target | Change | Linked task | Verification | Rollback |
| --- | --- | --- | --- | --- | --- | --- |
| P1 | documentation | WSL2 HA guide | Mark Docker network connection as human-approved bootstrap/break-glass work | T-208 | targeted command-boundary check | Revert guide comment/date/index |
| P1 | guardrail | `scripts/validate-repo-quality-gates.sh`; `scripts/README.md` | Validate `docker network connect/disconnect/create/rm` and `kubectl create clusterrolebinding` examples carry approval/bootstrap/break-glass/dry-run context | T-207, T-209 | repo quality and shell syntax | Revert validator and README wording |
| P1 | evidence | 006 Spec/Plan/Task/progress | Record VAL-SPC-006-044 and verification | T-210, T-211 | repo quality and wiki check | Revert overlay entries |

### Verification Result

| Command or method | Result | Notes |
| --- | --- | --- |
| `bash scripts/validate-repo-quality-gates.sh .` | PASS | New Docker network/RBAC create boundary guardrail passed |
| `bash -n scripts/validate-repo-quality-gates.sh` | PASS | Validator shell syntax after guardrail edit |
| targeted Docker network/RBAC create boundary check | PASS | Docker network and RBAC create examples carry approved context |
| operations frontmatter/index sync check | PASS | Touched WSL2 HA guide frontmatter and Stage 05 guide index use `2026-05-26` |
| `bash scripts/generate-llm-wiki-index.sh --check` | PASS | Generated reference index unchanged |
| `git diff --check` | PASS | No whitespace errors after verification record update |

## Vault Policy Write Boundary Guardrail Overlay

This overlay follows the continuation audit for `docs/05.operations` command
safety. It keeps the change documentation/governance and repo-static: no Vault
policy is applied, no secret value is read, and no live Vault or Kubernetes
state is changed.

### Gap Delta

| Area | Gap | Evidence path | Impact | Risk | Action type | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| Vault policy write command boundary | The reusable command boundary gate covered `vault kv put` but did not cover `vault policy write`, while active app onboarding guide/runbook include policy application examples | `scripts/validate-repo-quality-gates.sh`; `docs/05.operations/guides/0008-github-app-gitops-onboarding-guide.md`; `docs/05.operations/runbooks/0010-github-app-gitops-onboarding-runbook.md` | Agents or operators could treat Vault policy writes as ordinary copy/paste commands instead of approval-bound external secret operations | Medium | improvement | P1 |
| Operations command safety SSoT | Active onboarding docs had Vault policy application commands with weaker inline boundary markers than neighboring secret-write commands | operations guide/runbook | Secret-management responsibility could drift from the documented approval model | Medium | supplementation | P1 |

### Implementation Plan Delta

| Priority | Action type | Target | Change | Linked task | Verification | Rollback |
| --- | --- | --- | --- | --- | --- | --- |
| P1 | documentation | active onboarding guide/runbook | Add `external secret operation; human-approved policy change only` markers before `vault policy write` examples | T-203 | targeted boundary check | Revert comment lines |
| P1 | guardrail | `scripts/validate-repo-quality-gates.sh`; `scripts/README.md` | Validate `vault policy write` examples carry external-secret/human-approved/operator-approved/break-glass markers | T-202, T-204 | repo quality and shell syntax | Revert validator and README wording |
| P1 | evidence | 006 Spec/Plan/Task/progress | Record VAL-SPC-006-043 and verification | T-205, T-206 | repo quality and wiki check | Revert overlay entries |

### Verification Result

| Command or method | Result | Notes |
| --- | --- | --- |
| `bash scripts/validate-repo-quality-gates.sh .` | PASS | New Vault policy write boundary guardrail passed |
| `bash -n scripts/validate-repo-quality-gates.sh` | PASS | Validator shell syntax after guardrail edit |
| targeted Vault policy write boundary check | PASS | Active `vault policy write` examples carry human-approved external secret operation markers |
| operations frontmatter/index sync check | PASS | Touched guide/runbook frontmatter and Stage 05 indexes use `2026-05-26` |
| `bash scripts/generate-llm-wiki-index.sh --check` | PASS | Generated reference index unchanged |
| `git diff --check` | PASS | No whitespace errors after verification record update |

## App Onboarding Secret Path Contract Guardrail Overlay

This overlay follows the continuation audit for `docs/05.operations`,
`examples/sample-app`, and GitOps secret responsibility docs. It keeps the
change documentation/governance and repo-static: no AppProject permission,
Vault policy, secret value, ExternalSecret manifest semantics, or live
Kubernetes state is changed.

### Gap Delta

| Area | Gap | Evidence path | Impact | Risk | Action type | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| App onboarding secret path SSoT | Active onboarding docs and the sample ExternalSecret distinguish Vault CLI path from ESO `remoteRef.key`, but the reusable quality gate did not validate that distinction across operations, examples, and GitOps README summaries | `docs/05.operations/guides/0008-github-app-gitops-onboarding-guide.md`; `docs/05.operations/policies/0007-app-gitops-onboarding-policy.md`; `docs/05.operations/runbooks/0010-github-app-gitops-onboarding-runbook.md`; `examples/sample-app/external-secret.yaml`; `gitops/README.md` | Future edits could reintroduce the old mount-prefix confusion and make copied onboarding examples fail at runtime | Medium | improvement | P1 |
| GitOps sample secret wording | `gitops/README.md` described the sample app as reading Vault path `apps/<appname>/config`, which was accurate as an ESO remoteRef but ambiguous next to Vault CLI path `secret/apps/<appname>/config` | `gitops/README.md`; sample ExternalSecret | Operators could confuse Vault storage path with ESO remoteRef key | Low | supplementation | P1 |

### Implementation Plan Delta

| Priority | Action type | Target | Change | Linked task | Verification | Rollback |
| --- | --- | --- | --- | --- | --- | --- |
| P1 | documentation | `gitops/README.md` | Clarify that sample app ESO uses remoteRef key `apps/<appname>/config` while Vault CLI writes to `secret/apps/<appname>/config` | T-198 | repo quality and targeted phrase check | Revert README row wording |
| P1 | guardrail | `scripts/validate-repo-quality-gates.sh`; `scripts/README.md` | Validate active guide, policy, runbook, sample ExternalSecret, and GitOps README path-language consistency | T-197, T-199 | repo quality, shell syntax, targeted app secret path check | Revert validator and README wording |
| P1 | evidence | 006 Spec/Plan/Task/progress | Record VAL-SPC-006-042 and verification | T-200, T-201 | repo quality and wiki check | Revert overlay entries |

### Verification Result

| Command or method | Result | Notes |
| --- | --- | --- |
| `bash scripts/validate-repo-quality-gates.sh .` | PASS | New app onboarding secret path contract guardrail passed |
| `bash -n scripts/validate-repo-quality-gates.sh` | PASS | Validator shell syntax after guardrail edit |
| targeted app secret path contract check | PASS | Active guide/policy/runbook/sample/GitOps README distinguish Vault CLI path and ESO remoteRef key |
| `bash scripts/generate-llm-wiki-index.sh --check` | PASS | Generated reference index unchanged |
| `git diff --check` | PASS | No whitespace errors after verification record update |

## Goals & In-Scope

- **Goals**:
  - 전체 대상 범위를 `complete`, `partial`, `unknown`으로 기록한다.
  - 모든 Gap, 삭제 후보, 통합 후보, deferred item, unknown item을 분리한다.
  - 안전한 P1/P2만 구현하고 P3는 pre-check와 follow-up으로 남긴다.
- **In Scope**:
  - spec/task/plan evidence, README indexes, progress memory.
  - scope bridge correction, subagent scratch boundary, task-to-skill routing.
  - GitOps root app manifest non-empty validation.
  - script command-contract clarification.

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Kubernetes resource semantic changes.
  - ArgoCD App-of-Apps ownership changes.
  - Vault policy writes or secret value inspection.
  - CI/CD pipeline structure changes.
  - AI Agent instruction priority changes.
- **Out of Scope**:
  - live k3d, ArgoCD, Vault, PostgreSQL, Valkey, ESO, or Traefik runtime checks.
  - bulk deletion or ignored local file cleanup.

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | Record spec/task/plan evidence and indexes | `docs/03.specs`, `docs/04.execution`, `memory/progress.md` | REQ-SDD-TRACE | Repo quality gate PASS |
| PLN-002 | Correct subagent scope bridge drift | `docs/00.agent-governance/scopes/*.md` | REQ-AGENT-ROUTE | Scope imports match bridge rows |
| PLN-003 | Clarify scratch workspace and skill-routing boundaries | `subagent-protocol.md`, `harness-catalog.md` | REQ-HARNESS | Governance docs stay English and gateway remains thin |
| PLN-004 | Harden GitOps root app validation | `scripts/validate-gitops-structure.sh`, `scripts/README.md` | REQ-GITOPS-STATIC | GitOps structure check PASS |
| PLN-005 | Preserve high-risk Gap follow-up | This plan and linked task | REQ-RISK | P3 items have pre-checks and follow-up |
| PLN-006 | Run verification and final checklist | scripts, docs, runtime JSON | REQ-VALIDATION | Commands pass or limitations recorded |
| PLN-007 | Audit unreflected input tasks and close safe follow-up gaps | this plan, linked task, `harness-catalog.md`, `.claude/skills/workspace-harness-audit/skill.md` | REQ-INPUT-REFLECTION | Skill path check PASS and repo quality gate PASS |
| PLN-008 | Apply `office-hours` reflection to initial-contract coverage | this plan, linked task, `workspace-harness-audit` skill, progress ledger | REQ-INPUT-REFLECTION | Office-hours boundary recorded and repo quality gate PASS |
| PLN-009 | Apply `superpowers:brainstorming` design-lens review to remaining initial-contract coverage | this plan, linked task, `workspace-harness-audit` skill, progress ledger | REQ-INPUT-REFLECTION | Brainstorming alternatives, selected design, and verification recorded |
| PLN-010 | Apply `gstack-plan-ceo-review` to current Hybrid coverage drift | this plan, linked task, Spec 006, `workspace-harness-audit` skill, progress ledger | REQ-INPUT-REFLECTION | CEO review findings, current-state overlay, and verification recorded |
| PLN-011 | Execute the CEO review plan through `superpowers:executing-plans` | this plan, linked task, Spec 006, `workspace-harness-audit` skill, progress ledger | REQ-INPUT-REFLECTION | executing-plans review, task execution, verification, and finish boundary recorded |
| PLN-012 | Improve the repo-local audit Skill with skill creation/improvement lenses | this plan, linked task, Spec 006, `workspace-harness-audit` skill, progress ledger | REQ-SKILL-QUALITY | skill creation/improvement review, boundaries, and validation recorded |
| PLN-013 | Create a repo-local Skill from repeated docs-stage conformance work | `.claude/skills/docs-stage-conformance/skill.md`, `harness-catalog.md`, this plan, linked task, Spec 006, progress ledger | REQ-SKILL-CREATION | new Skill exists, routing is registered, and verification passes |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Structural | Repository quality and docs governance | `bash scripts/validate-repo-quality-gates.sh .` | PASS |
| VAL-PLN-002 | Generated docs | LLM Wiki generated index freshness | `bash scripts/generate-llm-wiki-index.sh --check` | PASS |
| VAL-PLN-003 | GitOps | Root apps and kustomization structure | `bash scripts/validate-gitops-structure.sh` | PASS |
| VAL-PLN-004 | Manifests | YAML syntax and optional kube-linter | `bash scripts/validate-k8s-manifests.sh .` | PASS or optional-tool skip recorded |
| VAL-PLN-005 | Secrets | Plaintext secret pattern scan | `bash scripts/check-secret-handling.sh .` | PASS |
| VAL-PLN-006 | Infra | Static infrastructure contracts | `bash infrastructure/tests/verify-contracts-static.sh` | PASS |
| VAL-PLN-007 | Shell | Shell syntax check | `find infrastructure scripts .claude/hooks -type f -name '*.sh' -exec bash -n {} +` | PASS |
| VAL-PLN-008 | Runtime JSON | Claude and Codex JSON parse | `python3 -m json.tool .claude/settings.json`; `python3 -m json.tool .codex/hooks.json` | PASS |
| VAL-PLN-009 | Env | Key-name-only env comparison | compare `.env.example` and `.env` keys without values | no differences |
| VAL-PLN-010 | Git hygiene | Whitespace sanity | `git diff --check` | PASS |
| VAL-PLN-011 | Named skill evidence | Office-hours/input-contract reflection and heading hygiene | `rg -n "^# " docs/04.execution/plans/2026-05-24-workspace-harness-gap-analysis.md` plus repo quality gate | only document title remains as H1; office-hours section present |
| VAL-PLN-012 | Brainstorming evidence | Brainstorming design-lens section and canonical SDD routing | targeted `rg` check for Brainstorming section names plus repo quality gate | section and selected design present |
| VAL-PLN-013 | CEO review evidence | `gstack-plan-ceo-review` current-state overlay and initial-contract coverage ledger | targeted `rg` check for CEO review sections plus repo quality gate | sections, findings, and overlay present |
| VAL-PLN-014 | Executing-plans evidence | `superpowers:executing-plans` execution record and finish boundary | targeted `rg` check for executing-plans sections plus repo quality gate | plan load/review/execute/verify/finish evidence present |
| VAL-PLN-015 | Skill quality evidence | skill-creator, skillify, skill-developer, and skill-improver application boundary | targeted `rg` check, line count check, repo quality gate | skill quality section and `When NOT to Use` present |
| VAL-PLN-016 | Skill creation evidence | `docs-stage-conformance` Skill, harness catalog route, and skill creation boundary | line count, targeted `rg`, repo quality gate, wiki check, `git diff --check` | new Skill and routing evidence present |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Full-scope audit becomes broad runtime change | High | Limit implementation to P1/P2 and defer P3 |
| Skill routing duplicates gateway policy | Medium | Keep `AGENTS.md` thin and record routing in `harness-catalog.md` |
| Static checks are mistaken for live health | Medium | Label live checks as unknown/deferred |
| Optional tools are unavailable locally | Medium | Record skipped reason and CI follow-up |
| Empty root app set passes validation | Medium | Add explicit non-kustomization root app manifest assertion |
| Named design-only review skill conflicts with implementation request | Low | Use the skill as a review lens, record the boundary, and keep implementation governed by the direct task contract |
| Named brainstorming skill defaults to off-taxonomy design docs | Low | Preserve the design review in existing SDD spec/task/plan artifacts unless the human explicitly requests a separate design document |
| `gstack-plan-ceo-review` preamble writes outside the workspace | Medium | Use the review workflow as a repo-static lens and record that external-write preamble/telemetry steps were not run |
| Earlier Hybrid P3 rows become stale after approved follow-up work | Medium | Add a current-state overlay that links resolved P3 items to the P3 plan instead of rewriting historical evidence |
| `superpowers:executing-plans` expects a development branch flow | Medium | Record that this repo task continued the existing human-approved task-unit commit flow on `main`; no separate worktree was created |
| `skillify` is scrape-specific and not applicable to this docs Skill | Low | Record it as reviewed but not applicable instead of forcing a browser-skill workflow |
| `skill-improver` expects `plugin-dev:skill-reviewer` | Medium | Apply its critical/major issue checklist manually and record that automated reviewer was unavailable in this repo harness |
| New docs conformance Skill overlaps existing docs-stage-routing | Low | Keep `docs-stage-routing` for new artifact placement and `docs-stage-conformance` for in-place cleanup and validation drift |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: repo-static validation listed above.
- **Sandbox / Canary Rollout**: not applicable.
- **Human Approval Gate**: required for live cluster, Vault, ArgoCD, or GitHub
  ruleset changes.
- **Rollback Trigger**: revert this documentation/governance/script change set
  if repo quality or GitOps structure checks cannot pass.
- **Prompt / Model Promotion Criteria**: not applicable.

## Completion Criteria

- [x] Baseline instructions checked.
- [x] Full target inventory recorded.
- [x] Six subagent results collected.
- [x] Coverage Ledger created.
- [x] Integrated Gap Analysis created.
- [x] Deletion, consolidation, deferral, and unknown items recorded.
- [x] spec/task/plan artifacts created.
- [x] Implementation Plan created.
- [x] P1/P2 changes implemented.
- [x] Verification run and limitations recorded.
- [x] Checklist gate completed.
- [x] Final Report created.
- [x] Input reflection follow-up completed.
- [x] CEO review follow-up completed.
- [x] Executing-plans follow-up completed.
- [x] Skill quality follow-up completed.
- [x] Skill creation follow-up completed.

## Coverage Ledger

| Area | Target path | Investigation status | Representative files read | Gap count | Deletion/consolidation/deferral candidate count | Unknown items | Next action |
| --- | --- | --- | --- | ---: | ---: | --- | --- |
| Documentation | `docs/00.agent-governance/` | complete | `documentation-protocol.md`, `stage-authoring-matrix.md`, `harness-catalog.md` | 2 | 3 | live runtime parity | Update scope bridges and harness catalog |
| Documentation | `docs/01.requirements/` | complete | README, PRD files via lifecycle reviewer | 0 | 0 | external freshness | Keep current |
| Documentation | `docs/02.architecture/` | complete | README, ADR/ARD index, superseded Dashboard ADR | 0 | 1 | strict legacy policy | Keep historical records |
| Documentation | `docs/03.specs/` | complete | README, specs 001-005, this spec | 1 | 0 | live implementation parity | Add this spec and index |
| Documentation | `docs/04.execution/` | complete | plan/task READMEs and current audit docs | 1 | 1 | strict plan/task exception policy | Add plan/task evidence |
| Documentation | `docs/05.operations/` | complete | guide/runbook/policy indexes and superseded onboarding docs | 1 | 3 | live operations state | Defer live checks |
| Documentation | `docs/90.references/` | complete | LLM Wiki README/index, version inventory | 1 | 0 | external latest freshness | Keep generated index checked |
| Documentation | `docs/99.templates/` | complete | README, spec/task/plan/readme templates | 0 | 1 | none | Keep templates unchanged |
| Scripts | `scripts/` | complete | README and five shell scripts | 2 | 1 | secret scan tolerance | Harden GitOps validation and clarify hook env |
| GitOps | `gitops/` | partial | root apps, platform network policies, ESO, argocd notifications | 5 | 3 | live ArgoCD health | Defer semantic/runtime changes |
| Infrastructure | `infrastructure/` | partial | README, bootstrap, static tests, Vault policy | 3 | 2 | live Vault/external reachability | Defer policy/runtime changes |
| Traefik | `traefik/` | complete | README and dynamic configs | 0 | 0 | live route health | Keep helper boundary |
| Examples | `examples/` | partial | sample app, AWS/Azure README/manifests | 2 | 1 | cloud version freshness | Defer sample secret contract alignment |
| Environment | `.env.example`, `.env` | complete | key-name-only comparison | 0 | 0 | value correctness | Keep values uninspected |
| QA | `tests/`, `infrastructure/tests/` | partial | tests README, static/live test scripts | 2 | 2 | live test state | Keep live tests manual |
| CI/CD | `.github/`, `.pre-commit-config.yaml` | partial | CI workflow, pre-commit, zizmor config | 2 | 2 | remote CI/rulesets | Defer SHA/ruleset decisions |
| Agent governance | `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.claude/`, `.codex/`, `.agents/` | partial | gateways, runtime baseline, agents, hooks, local mirrors | 5 | 5 | local permission precedence | Implement P1/P2 governance fixes |
| Agent governance | `.agent/` | unknown | path missing | 1 | 0 | whether path is intentionally absent | Record as missing path, no file creation |

## Integrated Gap Analysis

## Summary

- Overall status: repository-static baseline is healthy, with targeted harness,
  validation, and documentation-routing gaps.
- Largest Gap: GitOps semantic/runtime readiness around ESO egress, Vault policy,
  AppProject permissions, and bootstrap ownership.
- Immediately implementable: scope bridge drift, scratch boundary,
  task-to-skill routing, root app non-empty validation, hook env documentation.
- Needs deferral: Kubernetes resource semantics, ArgoCD ownership, Vault policy,
  GitHub Actions SHA pinning, live cluster validation.
- Unknown areas: live k3d/ArgoCD/Vault state, optional local toolchain, GitHub
  branch protection/rulesets, `.env` value freshness.

## Gaps by Area

| Area | Gap | Evidence path | Impact | Risk | Action type | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| Agent governance | Docs scope bridge omits `wiki-curator` | `docs/00.agent-governance/scopes/docs.md`; `.claude/agents/wiki-curator.md` | Misleading subagent routing | Low | improvement | P1 |
| Agent governance | Infra scope bridge omits `gitops-reviewer` | `docs/00.agent-governance/scopes/infra.md`; `.claude/agents/gitops-reviewer.md` | Misleading ownership review | Low | improvement | P1 |
| Agent governance | Scratch `_workspace/` convention is skill-local only | `.claude/skills/incident-postmortem/skill.md`; `subagent-protocol.md` | Future ad-hoc runtime folders | Low | supplementation | P1 |
| Agent governance | Prompt-level skill routing is not consolidated | user task contract; `harness-catalog.md` | Repeated task-to-skill rules can drift | Medium | supplementation | P2 |
| Agent governance | Reference-pattern skills are described as uniform workflow contracts | `harness-catalog.md` Skills table | Skill expectations are ambiguous | Medium | supplementation | P2 |
| Agent governance | Required external `SKILL.md` paths were listed but exact path-check evidence was not preserved | user task contract; `harness-catalog.md` | Missing-path Gap requirement lacked durable proof | Low | supplementation | P1 |
| Agent governance | Repeated broad workspace audit workflow was cataloged but not captured as a repo-local Skill | `harness-catalog.md`; previous plan | Future broad audits can omit path checks or raw ledger preservation | Medium | addition | P2 |
| Documentation | Initial Final Report contract included `Skill and Harness Updates`, but the report used the shorter later format | user task contract; this Final Report | Reporting format drift for harness work | Low | supplementation | P1 |
| Agent governance | Raw subagent ledgers are summarized but not durably archived in original role output format | this plan `Subagent Summary` | Replayability weaker than prompt contract | Medium | deferral | P3 |
| Scripts | GitOps root app validator does not fail on zero non-kustomization root app manifests | `scripts/validate-gitops-structure.sh` | Empty App-of-Apps root could partially pass | Medium | improvement | P2 |
| Scripts | Hook simulation skip env is internal but undocumented | `.claude/hooks/post-validate.sh`; `scripts/validate-repo-quality-gates.sh` | Maintainers may misuse bypass | Low | supplementation | P2 |
| GitOps | ESO egress policy may omit DNS/API egress | `gitops/platform/network-policies/external-secrets-egress-to-vault.yaml` | ESO reconciliation risk | High | deferral | P3 |
| GitOps | Vault policy omits `platform/notifications` path | `infrastructure/vault/policies/eso-read.hcl`; `argocd-notifications-secret.yaml` | Slack ExternalSecret sync risk | High | deferral | P3 |
| GitOps | AppProject may not permit documented app `ExternalSecret` | `gitops/clusters/local/appproject-apps.yaml`; `examples/sample-app/external-secret.yaml` | App onboarding drift | Medium | deferral | P3 |
| GitOps | `gitops/clusters/local` bootstrap CR ownership is not fully reconciled by root app | `root-application.yaml`; `bootstrap-local.sh` | AppProject/ApplicationSet drift risk | High | deferral | P3 |
| CI/CD | GitHub Actions use tag pinning with `unpinned-uses` disabled | `.github/zizmor.yml`; `.github/workflows/ci.yml` | Supply-chain policy risk | Medium | deferral | P3 |
| Agent governance | `.claude/settings.local.json` broad local allows need precedence review | `.claude/settings.local.json`; `.claude/settings.json` | Local safety ambiguity | Medium | deferral | P3 |
| Agent governance | ignored graphify rules/workflows are outside repo skill SSoT | `.agents/rules/graphify.md`; `.agents/workflows/graphify.md` | Local-only drift | Medium | deferral | P3 |
| QA | Optional local tooling unavailable | `.pre-commit-config.yaml`; local command checks | Local parity gap | Medium | deferral | P3 |
| Environment | `.env` values not inspected | `.env`, `.env.example` | Secret freshness unknown | Medium | deferral | P3 |

## Conflicts/Duplicates

| Target | Description | Impact | Recommended action |
| --- | --- | --- | --- |
| `AGENTS.md` vs requested recurring rules | User asked to consolidate recurring workflow/skill-routing; repo says gateway stays thin | Root gateway could become duplicative | Keep `AGENTS.md` thin and extend `harness-catalog.md` |
| `.claude/settings.local.json` vs shared deny boundary | Local allows may be broader than shared policy | Unknown local permission behavior | Defer until precedence is verified |
| `.agents/rules` and `.agents/workflows` | Ignored local graphify surfaces are outside tracked skill SSoT | Local-only drift | Keep ignored or clean locally after owner decision |
| Plan/task pairing | One historical plan lacks separate task record | Strict automation ambiguity | Keep documented exception unless policy changes |

## Deletion Candidates

| Target | Type | Candidate reason | Reference check | Impact | Recommended action |
| --- | --- | --- | --- | --- | --- |
| `.agents/rules/graphify.md` | deletion candidate | Ignored local rule can trigger generated churn | Local ignored only; no tracked references | Local context | Defer owner decision |
| `gitops/clusters/local/appproject-apps.yaml` `Namespace` whitelist | deletion candidate | Namespace ownership appears platform-owned | Requires `CreateNamespace=true` check | AppProject least privilege | Defer |
| Legacy/superseded docs | deletion candidate | Some documents are historical | References remain and replacement pointers exist | Architecture/ops history | Do not delete |

## Consolidation Candidates

| Target | Consolidation reason | Target location | Required pre-check |
| --- | --- | --- | --- |
| task-to-skill routing | Repeated prompt routing should not live in root gateway | `docs/00.agent-governance/harness-catalog.md` | Confirm gateway remains thin |
| `_workspace/` scratch convention | Incident skill has repeated scratch workflow | `docs/00.agent-governance/subagent-protocol.md` | Confirm no durable docs go to scratch |
| `gitops/clusters/local` bootstrap CR ownership | Bootstrap resources are repo-backed but not fully root-managed | Future GitOps bootstrap owner model | Decide ArgoCD ownership pattern |
| `examples/sample-app/external-secret.yaml` Vault key format | Sample path may not match ClusterSecretStore path | Examples and app onboarding docs | Validate intended ESO key semantics |

## Deferred Items

| Target | Deferral reason | Required pre-check | Follow-up work |
| --- | --- | --- | --- |
| ESO NetworkPolicy DNS/API egress | Kubernetes network policy semantic change | Confirm ESO required egress and cluster DNS/API targets | Add manifest change and live ESO validation |
| Vault policy `platform/notifications` | Secret access policy change | Confirm Vault path, runtime policy, and rollback | Add least-privilege HCL and static coverage |
| App `ExternalSecret` permission | AppProject permission change | Confirm intended app onboarding secret model | Update AppProject and examples together |
| Bootstrap CR ownership | ArgoCD ownership model change | Decide bootstrap vs managed-app pattern | Create separate architecture/operations plan |
| GitHub Actions SHA pinning | CI/CD supply-chain policy decision | Confirm accepted risk vs SHA pinning | Update workflows, inventory, and zizmor config |
| `.claude/settings.local.json` | Ignored local runtime file | Verify Claude local/project precedence | Tighten or document local-only scope |
| Live validation | Requires live cluster and secret-safe checks | Human approval and target context | Run read-only live test scripts |

## Unknown

| Item | Reason unknown | Follow-up check |
| --- | --- | --- |
| `.agent/` | Path missing in this checkout | Confirm whether absence is intentional |
| Live k3d/ArgoCD/Vault/ESO health | No live commands approved | Run approved read-only checks |
| Optional local toolchain | Some tools may not be installed | Run `pre-commit run --all-files` in CI/tooling environment |
| GitHub branch protection/rulesets | Not stored in worktree | Inspect GitHub repository settings |
| `.env` value freshness | Values intentionally not read or printed | Human-only secret review |

## Implementation Plan

## P1 Low risk / Immediate implementation

| Action type | Target | Change | Required skill | Linked task | Verification | Rollback |
| --- | --- | --- | --- | --- | --- | --- |
| improvement | `docs/00.agent-governance/scopes/docs.md` | Add `wiki-curator` to Subagent Bridge | `grill-with-docs`; `agent-md-refactor`; `claude-md-improver` | T-004 | repo quality gate | Revert line |
| improvement | `docs/00.agent-governance/scopes/infra.md` | Add `gitops-reviewer` to Subagent Bridge | `grill-with-docs`; `agent-md-refactor`; `claude-md-improver` | T-004 | repo quality gate | Revert line |
| supplementation | `docs/00.agent-governance/subagent-protocol.md` | Clarify `_workspace/` scratch boundary | `grill-with-docs`; `subagent-driven-development`; `agent-md-refactor` | T-005 | repo quality gate | Revert paragraph |
| addition | spec/task/plan docs | Create traceability docs and indexes | `grill-with-docs`; `documentation-writer`; `doc-coauthoring`; `gstack-document-release`; `humanizer` | T-001 | repo quality gate and link checks | Remove added docs/index entries |
| supplementation | this plan and linked task | Record input reflection audit and exact external skill path check result | `grill-with-docs`; `workspace-harness-audit` | T-010, T-011 | repo quality gate | Revert follow-up sections |
| supplementation | Final Report section layout | Add explicit `Skill and Harness Updates` section | `documentation-writer`; `humanizer`; `workspace-harness-audit` | T-010 | repo quality gate | Revert report section edit |
| supplementation | Implementation Plan skill column | Add row-level `Required skill` evidence for P1/P2/P3 work | `grill-with-docs`; `workspace-harness-audit` | T-013 | repo quality gate | Revert table-column edit |

## P2 Medium risk / Limited implementation

| Action type | Target | Change | Required skill | Linked task | Verification | Rollback |
| --- | --- | --- | --- | --- | --- | --- |
| improvement | `scripts/validate-gitops-structure.sh` | Fail when root app manifest count is zero | `bash-scripting`; `senior-devops`; `kubernetes-specialist`; repo-local `k8s-validate` | T-006 | `bash scripts/validate-gitops-structure.sh`; shell syntax | Revert script hunk |
| supplementation | `scripts/README.md` | Document hook simulation bypass as internal | `bash-scripting`; `documentation-writer`; `humanizer` | T-006 | repo quality gate | Revert README paragraph |
| supplementation | `harness-catalog.md` | Add external requested skill routing and skill type boundary | `grill-with-docs`; `agent-md-refactor`; `claude-md-improver` | T-005 | repo quality gate | Revert sections |
| addition | `.claude/skills/workspace-harness-audit/skill.md` and `harness-catalog.md` | Capture repeated workspace-wide audit workflow as repo-local Skill | `writing-skills`; `skill-creator`; `write-a-skill`; `skill-improver` | T-012 | repo quality gate | Remove skill and catalog row |

## P3 High risk / Deferred

| Action type | Target | Deferral reason | Pre-check | Required skill | Follow-up work |
| --- | --- | --- | --- | --- | --- |
| deferral | ESO NetworkPolicy | Kubernetes semantic behavior | Confirm DNS/API egress and live ESO needs | `senior-devops`; `kubernetes-specialist`; `kubernetes-architect`; repo-local `k8s-security-audit` | Separate GitOps manifest task |
| deferral | Vault policy | Secret access policy | Confirm Vault runtime path and rollback | `senior-devops`; `architect-review`; repo-local `k8s-security-audit` | Add HCL plus static test |
| deferral | AppProject app `ExternalSecret` | Permission model change | Confirm onboarding contract | `senior-devops`; `kubernetes-specialist`; repo-local `gitops-workflow` | Update AppProject/examples/docs |
| deferral | Bootstrap CR ownership | ArgoCD ownership design | Decide managed owner model | `senior-architect`; `architecture`; `kubernetes-architect`; repo-local `gitops-workflow` | Architecture and runbook update |
| deferral | GitHub Actions SHA pinning | CI policy decision | Review supply-chain risk | `senior-devops`; `devops-engineer`; `devops-troubleshooter` | Update workflows and inventory |
| deferral | Local Claude settings | Ignored local runtime behavior | Verify precedence | `claude-md-improver`; `agent-md-refactor`; `hook-development` | Tighten local file if needed |
| deferral | Live checks | Requires approved runtime context | Human approval | `senior-devops`; `testing-qa`; `kubernetes-deployment` | Run live read-only tests |
| deferral | Historical raw subagent ledgers | Original raw role outputs are not authoritative current-state files | Future subagent runs must persist raw Summary/Ledger tables into plan/task evidence | `subagent-driven-development`; `workspace-harness-audit` | Enforce through `workspace-harness-audit` skill |

## Input Reflection Follow-up

## Unreflected or Weakly Reflected Input Tasks

| Input task | Existing reflection | Gap judgment | Implementation |
| --- | --- | --- | --- |
| Verify exact required external `SKILL.md` paths and record missing paths as Gaps | Paths were listed in `harness-catalog.md`, but no durable path-check result was recorded | weak reflection | Added path-check result to this plan/task; all listed paths were present in the current WSL environment |
| Create or improve reusable Skills for repeated workflows where appropriate | Repeated routing was consolidated into `harness-catalog.md` only | partial reflection | Added `.claude/skills/workspace-harness-audit/skill.md` and cataloged it |
| Include `Skill and Harness Updates` in the Final Report | Final Report used the shorter later contract | weak reflection | Added the explicit section and kept the rest of the report intact |
| Preserve subagent Summary and Ledger output format | Plan preserves summaries and integrated ledgers, not raw role output tables | partial reflection | Current raw outputs are not reconstructed; future runs must preserve raw role tables through the new Skill workflow |
| Record chosen skill group before each implementation task | Skill routing existed, but implementation plan rows did not carry `Required skill` evidence | weak reflection | Added `Required skill` columns to P1/P2/P3 implementation rows |

## Required External Skill Path Check

| Area | Result | Missing paths |
| --- | --- | --- |
| Workspace investigation and analysis | PASS | none |
| Documentation writing | PASS | none |
| Documentation co-authoring and release | PASS | none |
| Repeated workflow and instruction skills | PASS | none |
| Subagent creation and subagent-driven work | PASS | none |
| Hook work | PASS | none |
| Native instruction files and runtime governance | PASS | none |
| Scripts | PASS | none |
| Kubernetes and infrastructure | PASS | none |
| QA | PASS | none |
| CI/CD | PASS | none |

## Office-Hours Reflection Follow-up

### Application Boundary

`/home/hy/gstack/.agents/skills/gstack-office-hours/SKILL.md` was applied as a
problem-framing and stress-test lens for this follow-up. Its design-doc-only
hard gate conflicts with the active human request to implement the safe plan, so
implementation remains governed by the direct task contract and this repository's
P1/P2/P3 safety rules. The office-hours preamble was not run because it writes
to `~/.gstack` outside the workspace; current repository evidence replaced that
step.

### Infra-Adapted Forcing Questions

| Office-hours question | Repository-specific answer | Result |
| --- | --- | --- |
| Q2 Status quo | The workspace already has Spec 006, linked task/plan, Hybrid Refresh evidence, and static verification, but named `office-hours` application was not durably recorded. | Add plan/task/progress evidence. |
| Q4 Narrowest wedge | The smallest safe implementation is documentation evidence plus skill guardrail updates; no runtime, GitOps, secret, or CI semantics need to change. | Implement P1 docs/skill updates only. |
| Other questions | Product-demand and customer-persona questions are not material for this internal infra governance refresh. | Record as N/A rather than expanding scope. |

### Initial Contract Delta Ledger

| Initial or follow-up requirement | Current reflection | Gap judgment | Action |
| --- | --- | --- | --- |
| Review all entered matters with `grill-with-docs` | `grill-with-docs` was used for previous reflection and Hybrid Refresh, but no office-hours delta table existed. | weak reflection | Add this contract delta ledger and task evidence. |
| Apply `office-hours` review to omissions in the Hybrid Refresh plan | No durable plan/task entry existed for `office-hours`. | gap | Record application boundary and forcing-question result. |
| Consider medium and high risk, not only low risk | P1/P2/P3 tables already preserve low, medium, and high-risk treatment. | complete | Keep high-risk P3 deferrals unchanged. |
| Preserve exact external `SKILL.md` path checks | Hybrid path-level ledger is present and all requested paths are marked present. | complete | No new path check required. |
| Preserve fresh six-role subagent outputs | Hybrid section preserves current read-only role tables. | complete | No subagent rerun required for this delta. |
| Handle template-change impact rules | No `docs/99.templates/` file changed in this implementation series. | N/A recorded | Keep explicit no-template-change note. |
| Apply deletion/consolidation/legacy safeguards | No deletion or consolidation was implemented; candidates remain deferred. | complete | Keep deferred items. |
| Create task-sized commits | Prior work used task-sized commits; this delta is isolated as its own verified commit unit. | complete | Keep this office-hours reflection as a separate commit. |

### Office-Hours Delta Gap Analysis

| Area | Gap | Evidence path | Impact | Risk | Action type | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| Skills/harness | Named `office-hours` review was applied in the conversation but not preserved in durable evidence. | this plan before this section; linked task before T-021 | Future refreshes could repeat the omission. | Low | supplementation | P1 |
| Documentation lifecycle | `Input Reflection Follow-up` remained a post-title H1. | this plan | Heading hierarchy drift weakens template conformance. | Low | consolidation | P1 |
| Skills/harness | `workspace-harness-audit` did not explicitly require named-skill application boundary evidence. | `.claude/skills/workspace-harness-audit/skill.md` | Future named-skill conflicts could stay implicit. | Low | improvement | P1 |

### Office-Hours Implementation Plan

| Action type | Target | Change | Required skill | Linked task | Verification | Rollback |
| --- | --- | --- | --- | --- | --- | --- |
| supplementation | linked plan/task/progress | Record office-hours application boundary, initial-contract delta, verification, and handoff. | `office-hours`; `grill-with-docs`; `workspace-harness-audit`; `documentation-writer` | T-021, T-022, T-023 | repo quality gate; heading check; `git diff --check` | Revert this section and task/progress entries. |
| consolidation | linked plan | Demote remaining post-title H1 to H2. | `workspace-harness-audit`; `documentation-writer` | T-022 | heading check | Revert heading line. |
| improvement | `.claude/skills/workspace-harness-audit/skill.md` | Require durable named-skill application boundary evidence. | `workspace-harness-audit`; `skill-improver`; `writing-skills` | T-022 | repo quality gate | Revert skill hunk. |

### Office-Hours Deferred Items

| Target | Deferral reason | Required pre-check | Follow-up work |
| --- | --- | --- | --- |
| `office-hours` preamble writing to `~/.gstack` | Writes outside workspace and is not required for repository-static evidence. | Human approval for external write location. | Run only if a future design-doc workflow needs gstack project files. |
| Live k3d/ArgoCD/Vault/ESO checks | High-risk/external runtime boundary remains unchanged. | Explicit read-only live-check approval. | Use the existing P3 live validation plan. |

### Office-Hours Verification Results

| Command or method | Result | Record location |
| --- | --- | --- |
| `bash scripts/validate-repo-quality-gates.sh .` | PASS | linked task Office-Hours summary |
| `bash scripts/generate-llm-wiki-index.sh --check` | PASS | linked task Office-Hours summary |
| `bash scripts/validate-gitops-structure.sh` | PASS | linked task Office-Hours summary |
| `bash scripts/validate-k8s-manifests.sh .` | PASS for YAML syntax; optional `kube-linter` skipped because it is not installed locally | linked task Office-Hours summary |
| `bash scripts/check-secret-handling.sh .` | PASS | linked task Office-Hours summary |
| `bash infrastructure/tests/verify-contracts-static.sh` | PASS | linked task Office-Hours summary |
| shell syntax check | PASS | linked task Office-Hours summary |
| runtime JSON parse | PASS for `.claude/settings.json` and `.codex/hooks.json` | linked task Office-Hours summary |
| `.env.example` and `.env` key comparison | PASS; key names matched without printing values | linked task Office-Hours summary |
| plan H1 heading check | PASS; only the document title remains as H1 | linked task Office-Hours summary |
| `git diff --check` | PASS | linked task Office-Hours summary |

## Superpowers Brainstorming Reflection Follow-up

### Application Boundary

`/home/hy/.codex/plugins/cache/claude-plugins-official/superpowers/5.1.0/skills/brainstorming/SKILL.md`
was applied as a design-lens review for the remaining initial-contract delta.
The skill's default hard gate requires a new design document under
`docs/superpowers/specs/` and user approval before implementation. That default
conflicts with this already-approved workspace improvement objective and the
repo's canonical SDD stage artifacts, so this review is preserved in the
existing Spec 006, linked plan, linked task, and progress ledger instead of
creating an off-taxonomy design document.

### Brainstorming Context Check

| Checklist item | Repository evidence | Result |
| --- | --- | --- |
| Explore project context | Current plan/task/spec, recent commits, and `workspace-harness-audit` skill were inspected. | complete |
| Visual companion | Not relevant; the task is textual governance/evidence review. | N/A |
| Clarifying questions | Answered from repository evidence: this is a delta review, not a new runtime feature; P3 remains deferred; canonical SDD artifacts are the storage target. | complete |
| Approaches | Alternatives are recorded below. | complete |
| Design | Selected design is recorded below. | complete |
| Separate design doc | Skipped because current repo contract requires updating existing spec/task/plan artifacts and avoiding file proliferation. | deferred by boundary |

### Brainstorming Alternatives

| Approach | Trade-off | Decision |
| --- | --- | --- |
| Strict Superpowers default: create `docs/superpowers/specs/...` and stop for user approval | Maximally follows the standalone skill, but duplicates canonical SDD artifacts and halts an already-approved implementation objective. | rejected for this task |
| No additional change after Office-Hours | Avoids churn, but leaves `superpowers:brainstorming` unproven in durable evidence. | rejected |
| Canonical SDD delta: record brainstorming alternatives, selected design, plan, verification, and progress in existing artifacts | Satisfies the named-skill review intent while preserving repo taxonomy and avoiding runtime changes. | selected |

### Brainstorming Selected Design

| Component | Design |
| --- | --- |
| Scope | Documentation and harness evidence only; no Kubernetes, ArgoCD, Vault, secret/env, CI/CD, or live runtime semantic changes. |
| Data flow | Initial task contract -> current Hybrid/Office-Hours evidence -> brainstorming alternatives -> selected canonical SDD delta -> verification summary. |
| Error handling | If repo validation fails, revert the P1 documentation hunk; if a future user requires strict Superpowers flow, create a separate design-doc task. |
| Testing | Run repo quality gate, LLM wiki index check, targeted brainstorming evidence search, plan H1 check, and `git diff --check`. |

### Brainstorming Delta Gap Analysis

| Area | Gap | Evidence path | Impact | Risk | Action type | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| Skills/harness | `superpowers:brainstorming` named-skill application was not yet preserved in durable evidence. | this plan before this section; linked task before T-024 | Future audits could not prove the requested brainstorming review occurred. | Low | supplementation | P1 |
| Documentation lifecycle | Standalone brainstorming default design-doc path conflicts with canonical SDD artifact update rule for this task. | brainstorming skill; `AGENTS.md`; this plan | File proliferation or approval deadlock risk. | Low | deferral | P1 |
| Skills/harness | `workspace-harness-audit` did not explicitly prefer canonical SDD artifacts over off-taxonomy design-doc locations for named review skills. | `.claude/skills/workspace-harness-audit/skill.md` | Future broad audits could duplicate evidence locations. | Low | improvement | P1 |

### Brainstorming Implementation Plan

| Action type | Target | Change | Required skill | Linked task | Verification | Rollback |
| --- | --- | --- | --- | --- | --- | --- |
| supplementation | linked plan/task/progress | Record brainstorming application boundary, alternatives, selected design, delta Gap analysis, verification, and handoff. | `superpowers:brainstorming`; `grill-with-docs`; `workspace-harness-audit`; `documentation-writer` | T-024, T-025, T-026 | repo quality gate; targeted evidence search; `git diff --check` | Revert this section and task/progress entries. |
| improvement | `.claude/skills/workspace-harness-audit/skill.md` | Prefer canonical SDD artifacts over off-taxonomy design-doc locations for named review skills unless explicitly requested. | `workspace-harness-audit`; `skill-improver`; `writing-skills` | T-025 | repo quality gate | Revert skill hunk. |

### Brainstorming Deferred Items

| Target | Deferral reason | Required pre-check | Follow-up work |
| --- | --- | --- | --- |
| `docs/superpowers/specs/...` design document | Would duplicate existing canonical Spec 006 and conflict with in-place SDD update rules for this approved implementation task. | Explicit human request for a separate Superpowers design-doc workflow. | Create a separate design-doc task only if requested. |
| User approval gate inside standalone brainstorming flow | Current human objective already directs implementation of this delta; stopping here would reduce the requested scope. | Future task that starts from an unapproved design idea. | Use the full Superpowers gate for new feature/design work. |
| Live k3d/ArgoCD/Vault/ESO checks | High-risk/external runtime boundary remains unchanged. | Explicit read-only live-check approval. | Use the existing P3 live validation plan. |

### Brainstorming Verification Results

| Command or method | Result | Record location |
| --- | --- | --- |
| `bash scripts/validate-repo-quality-gates.sh .` | PASS | linked task Brainstorming summary |
| `bash scripts/generate-llm-wiki-index.sh --check` | PASS | linked task Brainstorming summary |
| `bash scripts/validate-gitops-structure.sh` | PASS | linked task Brainstorming summary |
| `bash scripts/validate-k8s-manifests.sh .` | PASS for YAML syntax; optional `kube-linter` skipped because it is not installed locally | linked task Brainstorming summary |
| `bash scripts/check-secret-handling.sh .` | PASS | linked task Brainstorming summary |
| `bash infrastructure/tests/verify-contracts-static.sh` | PASS | linked task Brainstorming summary |
| shell syntax check | PASS | linked task Brainstorming summary |
| runtime JSON parse | PASS for `.claude/settings.json` and `.codex/hooks.json` | linked task Brainstorming summary |
| `.env.example` and `.env` key comparison | PASS; key names matched without printing values | linked task Brainstorming summary |
| targeted brainstorming evidence search | PASS | linked task Brainstorming summary |
| plan H1 heading check | PASS; only the document title remains as H1 | linked task Brainstorming summary |
| `git diff --check` | PASS | linked task Brainstorming summary |

## Hybrid Refresh - 2026-05-24

### Summary

- Overall status: committed workspace harness artifacts remain valid as the
  baseline, but the fresh review found additional low/medium-risk evidence and
  guardrail gaps that are safe to close without changing Kubernetes, ArgoCD,
  Vault, secret, or CI/CD semantics.
- Largest Gap: live/runtime truth is still unverified and remains out of scope
  without explicit approval; `SessionStart` previously made live read-only
  probes automatic, which conflicted with no-live audit tasks.
- Immediately implementable: status/metadata alignment, plan heading cleanup,
  path-level external skill evidence, `SessionStart` live-probe opt-in,
  scratch ignore coverage, meta runtime ownership wording, and scripts/examples
  evidence freshness.
- Needs deferral: ESO DNS/API egress, Vault `platform/notifications`, app
  `ExternalSecret` AppProject permission, bootstrap CR ownership, GitHub
  Actions SHA pinning, local Claude permission precedence, graphify local
  cleanup, and live k3d/ArgoCD/Vault/ESO validation.
- Unknown areas: live runtime health, `.env` value freshness, remote CI/ruleset
  state, optional toolchain coverage, `.agent/` absence intent, and ignored
  graphify ownership.

### Hybrid Coverage Ledger

| Area | Target path | Investigation status | Representative files read | Gap count | Deletion/consolidation/deferral candidate count | Unknown items | Next action |
| --- | --- | --- | --- | ---: | ---: | --- | --- |
| Documentation lifecycle | `docs/00.agent-governance/`, `docs/01.requirements/`, `docs/02.architecture/`, `docs/03.specs/`, `docs/04.execution/`, `docs/05.operations/`, `docs/90.references/`, `docs/99.templates/` | complete | spec/plan/task, stage READMEs, templates, progress ledger | 6 | 5 | live runtime, `.agent/`, optional toolchain | Align status/metadata/headings and preserve fresh outputs |
| Agent governance | `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.claude/`, `.codex/`, `.agents/`, `.agent/` | partial | gateway shims, runtime baseline, settings, hooks, scope files, harness catalog | 6 | 8 | permission precedence, no-live hook behavior, graphify intent | Implement opt-in live probes and ownership wording |
| Scripts | `scripts/` | complete | `scripts/README.md`, five shell scripts, CI/hook references | 3 | 5 | scanner fixtures, optional lint tools | Refresh inventory date and keep validator hardening |
| GitOps infrastructure | `gitops/`, `infrastructure/`, `traefik/`, `examples/` | partial | root apps, AppProjects, ESO/Vault manifests, examples READMEs, Traefik README | 8 | 8 | live ArgoCD/Vault/ESO, cloud latest | Defer semantic changes; refresh examples evidence wording |
| Environment/QA/CI | `.env.example`, `.env`, `.github/`, `.pre-commit-config.yaml`, `tests/`, `infrastructure/tests/` | partial | env key comparison, workflows, static tests, QA READMEs | 5 | 6 | `.env` values, remote CI/rulesets, optional tools | Keep static verification; defer live and policy checks |
| Skills/harness | `.claude/skills/`, `.agents/skills/`, hooks, subagent protocol, harness catalog | partial | `workspace-harness-audit`, skill catalog, hooks, `.gitignore` | 7 | 7 | local mirrors, raw historical ledgers, Codex provider note intent | Add path-level skill ledger and scratch guardrail |

### Hybrid Integrated Gap Analysis

| Area | Gap | Evidence path | Impact | Risk | Action type | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| Documentation lifecycle | Spec status was `draft` while stage README marked the spec `Active` | `docs/03.specs/006-workspace-harness-gap-analysis/spec.md`; `docs/03.specs/README.md` | Lifecycle promotion ambiguity | Medium | improvement | P1 |
| Documentation lifecycle | Plan had multiple H1 sections after the document title | `docs/04.execution/plans/2026-05-24-workspace-harness-gap-analysis.md` | Template/heading consistency drift | Low | consolidation | P1 |
| Documentation lifecycle | Harness catalog and subagent protocol metadata lagged current 2026-05-24 content | `docs/00.agent-governance/harness-catalog.md`; `docs/00.agent-governance/subagent-protocol.md` | Freshness evidence weaker | Low | improvement | P1 |
| Agent governance | `SessionStart` hook ran live read-only `k3d`/`kubectl get` probes automatically | `.claude/hooks/session-start.sh`; `.claude/settings.json`; `.codex/hooks.json` | No-live audit tasks can touch live state before approval | Medium | improvement | P2 |
| Agent governance | Meta scope did not explicitly own tracked hook/skill/Codex runtime contract surfaces | `docs/00.agent-governance/scopes/meta.md`; `harness-catalog.md` | Runtime ownership ambiguity | Low | supplementation | P1 |
| Skills/harness | External `SKILL.md` path evidence was area-level, not path-by-path | `harness-catalog.md`; linked task | Missing-path audit replayability weaker | Low | supplementation | P1 |
| Skills/harness | `_workspace/` scratch paths were allowed by skills/protocol but not ignored | `.claude/skills/incident-postmortem/skill.md`; `.gitignore`; `subagent-protocol.md` | Temporary scratch files could be staged | Medium | improvement | P2 |
| Skills/harness | Workflow/reference-pattern skill distinction lacked per-skill metadata | `harness-catalog.md` | Skill review expectations can drift | Low | supplementation | P1 |
| Scripts | `scripts/README.md` retained 2026-05-17 inventory wording after 2026-05-24 hardening | `scripts/README.md`; linked task | Evidence freshness weaker | Low | improvement | P1 |
| GitOps infrastructure | Examples snapshot wording mixed older dates with the current version inventory | `examples/README.md`; `examples/aws/docs/README.md`; `examples/azure/docs/README.md`; `docs/90.references/versions/tech-stack-version-inventory.md` | Cloud examples freshness evidence weaker | Low | supplementation | P1 |
| GitOps infrastructure | ESO DNS/API egress remains unresolved | `gitops/platform/network-policies/external-secrets-egress-to-vault.yaml` | ESO reconciliation risk | High | deferral | P3 |
| GitOps infrastructure | Vault policy lacks `platform/notifications` coverage | `infrastructure/vault/policies/eso-read.hcl`; `argocd-notifications-secret.yaml` | Notification secret sync risk | High | deferral | P3 |
| GitOps infrastructure | AppProject and sample app ExternalSecret contract remain inconsistent | `appproject-apps.yaml`; `examples/sample-app/external-secret.yaml` | App onboarding drift | Medium | deferral | P3 |
| CI/CD | GitHub Actions SHA pinning and skipped-job/ruleset behavior need policy review | `.github/workflows/ci.yml`; `.github/zizmor.yml` | Supply-chain and required-check ambiguity | Medium | deferral | P3 |

### Hybrid Implementation Plan

#### P1 Low risk / Immediate implementation

| Action type | Target | Change | Required skill | Linked task | Verification | Rollback |
| --- | --- | --- | --- | --- | --- | --- |
| improvement | `docs/03.specs/006-workspace-harness-gap-analysis/spec.md` | Set status to `active` and add hybrid refresh acceptance criterion | `grill-with-docs`; `documentation-writer`; `workspace-harness-audit` | T-016 | repo quality gate | Revert status/criterion |
| consolidation | linked plan | Demote post-title H1 sections and add Hybrid Refresh evidence | `grill-with-docs`; `documentation-writer`; `humanizer` | T-014, T-016 | repo quality gate | Revert heading/evidence section |
| supplementation | linked plan/task | Preserve fresh role review outputs and path-level external skill checks | `grill-with-docs`; `subagent-driven-development`; `workspace-harness-audit` | T-014, T-015 | repo quality gate | Revert Hybrid Refresh sections |
| supplementation | `docs/00.agent-governance/scopes/meta.md` | Clarify meta ownership of hooks, skills, Codex wiring, and supervisor exception | `claude-md-improver`; `agent-md-refactor`; `workspace-harness-audit` | T-017 | repo quality gate | Revert scope wording |
| improvement | `docs/00.agent-governance/harness-catalog.md`, `subagent-protocol.md` | Refresh metadata and add per-skill contract type | `claude-md-improver`; `agent-md-refactor`; `skill-improver` | T-017 | repo quality gate | Revert metadata/table changes |
| improvement | `scripts/README.md`, `examples/README.md`, cloud docs READMEs | Refresh evidence wording without changing examples or scripts | `documentation-writer`; `humanizer`; `grill-with-docs` | T-018 | repo quality gate | Revert wording |

#### P2 Medium risk / Limited implementation

| Action type | Target | Change | Required skill | Linked task | Verification | Rollback |
| --- | --- | --- | --- | --- | --- | --- |
| improvement | `.claude/hooks/session-start.sh` | Make live k3d/kubectl startup probes opt-in via `HY_HOME_K8S_ENABLE_SESSION_LIVE_PROBES=1` | `hook-development`; `writing-rules`; `agent-md-refactor` | T-019 | shell syntax; repo quality gate | Revert hook guard |
| improvement | `.gitignore` | Ignore `_workspace/` and `_workspace_prev/` scratch directories | `workspace-harness-audit`; `agent-md-refactor` | T-019 | repo quality gate; `git status` | Revert ignore lines |

#### P3 High risk / Deferred

| Action type | Target | Deferral reason | Required pre-check | Required skill | Follow-up work |
| --- | --- | --- | --- | --- | --- |
| deferral | ESO NetworkPolicy DNS/API egress | Kubernetes semantic change | Confirm DNS/API targets and live ESO behavior | `senior-devops`; `kubernetes-specialist`; `k8s-security-audit` | Separate manifest task |
| deferral | Vault `platform/notifications` policy | Secret access policy change | Confirm Vault path and rollback | `senior-devops`; `architect-review`; `k8s-security-audit` | Separate security/GitOps task |
| deferral | AppProject ExternalSecret permission and sample key format | App onboarding permission/secret model change | Decide intended app secret onboarding model | `gitops-workflow`; `kubernetes-specialist`; `architect-review` | Update AppProject/examples/docs together |
| deferral | `gitops/clusters/local` bootstrap CR ownership | ArgoCD ownership design change | Choose bootstrap-owned vs reconciled owner model | `senior-architect`; `kubernetes-architect`; `gitops-workflow` | Separate architecture/runbook plan |
| deferral | GitHub Actions SHA pinning and skipped-job policy | CI/CD policy change | Review supply-chain and branch ruleset requirements | `senior-devops`; `devops-engineer`; `devops-troubleshooter` | Separate CI governance task |
| deferral | `.claude/settings.local.json` broad allows | Ignored local runtime precedence unknown | Verify Claude settings precedence without destructive commands | `claude-md-improver`; `hook-development`; `agent-md-refactor` | Local hardening task |
| deferral | Live k3d/ArgoCD/Vault/ESO validation | Requires live runtime context | Explicit approval and read-only command scope | `senior-devops`; `testing-qa`; `kubernetes-deployment` | Run live validation scripts |

### Hybrid Path-Level External Skill Check

| Skill path | Result |
| --- | --- |
| `/home/hy/.agents/skills/grill-with-docs/SKILL.md` | present |
| `/home/hy/.agents/skills/brainstorming/SKILL.md` | present |
| `/home/hy/.agents/skills/gstack/plan-ceo-review/SKILL.md` | present |
| `/home/hy/.codex/skills/.system/skill-creator/SKILL.md` | present |
| `/home/hy/gstack/.agents/skills/gstack-skillify/SKILL.md` | present |
| `/home/hy/.agents/skills/skill-developer/SKILL.md` | present |
| `/home/hy/.codex/plugins/cache/claude-plugins-official/superpowers/5.1.0/skills/executing-plans/SKILL.md` | present |
| `/home/hy/.codex/plugins/cache/claude-plugins-official/superpowers/5.1.0/skills/finishing-a-development-branch/SKILL.md` | present |
| `/home/hy/.codex/plugins/cache/claude-plugins-official/superpowers/5.1.0/skills/using-git-worktrees/SKILL.md` | present |
| `/home/hy/.codex/plugins/cache/claude-plugins-official/superpowers/5.1.0/skills/writing-plans/SKILL.md` | present |
| `/home/hy/.agents/skills/documentation-writer/SKILL.md` | present |
| `/home/hy/.agents/skills/humanizer/SKILL.md` | present |
| `/home/hy/gstack/.agents/skills/gstack-document-release/SKILL.md` | present |
| `/home/hy/.agents/skills/technical-blog-writing/SKILL.md` | present |
| `/home/hy/.agents/skills/doc-coauthoring/SKILL.md` | present |
| `/home/hy/.codex/plugins/cache/claude-plugins-official/superpowers/5.1.0/skills/writing-skills/SKILL.md` | present |
| `/home/hy/.codex/trailofbits-skills/plugins/skill-improver/skills/skill-improver/SKILL.md` | present |
| `/home/hy/.agents/skills/skill-creator/SKILL.md` | present |
| `/home/hy/.agents/skills/write-a-skill/SKILL.md` | present |
| `/home/hy/.codex/plugins/cache/claude-plugins-official/superpowers/5.1.0/skills/subagent-driven-development/SKILL.md` | present |
| `/home/hy/.agents/skills/hook-development/SKILL.md` | present |
| `/home/hy/.codex/plugins/cache/claude-plugins-official/hookify/local/skills/writing-rules/SKILL.md` | present |
| `/home/hy/.codex/plugins/cache/claude-plugins-official/claude-md-management/1.0.0/skills/claude-md-improver/SKILL.md` | present |
| `/home/hy/.agents/skills/claude-md-improver/SKILL.md` | present |
| `/home/hy/.agents/skills/agent-md-refactor/SKILL.md` | present |
| `/home/hy/.agents/skills/bash-scripting/SKILL.md` | present |
| `/home/hy/.agents/skills/senior-devops/SKILL.md` | present |
| `/home/hy/.agents/skills/senior-architect/SKILL.md` | present |
| `/home/hy/.agents/skills/architect-review/SKILL.md` | present |
| `/home/hy/.agents/skills/architecture/SKILL.md` | present |
| `/home/hy/.agents/skills/kubernetes-specialist/SKILL.md` | present |
| `/home/hy/.agents/skills/kubernetes-architect/SKILL.md` | present |
| `/home/hy/.agents/skills/kubernetes-deployment/SKILL.md` | present |
| `/home/hy/.agents/skills/senior-qa/SKILL.md` | present |
| `/home/hy/.agents/skills/testing-qa/SKILL.md` | present |
| `/home/hy/.codex/trailofbits-skills/plugins/testing-handbook-skills/skills/coverage-analysis/SKILL.md` | present |
| `/home/hy/.agents/skills/devops-engineer/SKILL.md` | present |
| `/home/hy/.agents/skills/devops-troubleshooter/SKILL.md` | present |

### Hybrid Raw Subagent Output Preservation

> Historical note: the following Hybrid Refresh reviewer tables are preserved
> as point-in-time evidence from 2026-05-24. Later CEO, multi-area, and P0
> overlays supersede stale current-state claims without rewriting preserved raw
> reviewer evidence.

The six fresh role reviews were rerun in read-only mode and are preserved below
in the requested table shape. The original subagent messages used absolute
paths in several cells; this plan keeps the same evidence targets while using
repository-relative paths where that improves readability.

#### Documentation Lifecycle Reviewer Summary

| Key finding | Evidence path | Impact | Risk | Action type | Recommended action |
| --- | --- | --- | --- | --- | --- |
| SDD chain is connected, but Spec lifecycle state conflicted with the index: Spec `draft`, README `Active`, Plan/Task `done`. | `docs/03.specs/006-workspace-harness-gap-analysis/spec.md`; `docs/03.specs/README.md`; linked plan/task | Lifecycle promotion ambiguity | Medium | partial | Align spec status and index state. |
| Current Plan preserves required evidence, but used multiple H1 sections after the document title. | linked plan | Heading hierarchy weakened template consistency | Low | partial | Demote appended report sections while preserving content. |
| README freshness for current Spec/Plan/Task artifacts is good. | `docs/03.specs/README.md`; `docs/04.execution/plans/README.md`; `docs/04.execution/tasks/README.md` | Navigation intact | Low | complete | Keep current indexes. |
| Original raw role Summary/Ledger tables were not durably archived. | linked plan; `memory/progress.md` | Replayability weaker than prompt contract | Medium | partial | Preserve fresh role tables in this Hybrid Refresh; keep historical gap noted. |
| P3 runtime, secret-policy, GitOps ownership, CI, and live validation remain deferred or unknown. | linked plan; `memory/progress.md` | Static docs cannot prove live readiness | High | partial | Keep separate owner-approved follow-up work. |
| Harness governance content was newer than metadata dates. | `harness-catalog.md`; `subagent-protocol.md` | Freshness metadata under-reported content | Low | partial | Refresh metadata when editing. |
| External skill path evidence was area-level rather than path-by-path. | linked plan; `harness-catalog.md`; linked task | Replayability weaker | Low | partial | Store path-by-path results. |

#### Documentation Lifecycle Reviewer Ledger

| Target | Finding | Type | Evidence path | Reference check | Recommended action |
| --- | --- | --- | --- | --- | --- |
| `docs/03.specs/006-workspace-harness-gap-analysis/spec.md` | Template sections, related links, and verification plan are present; lifecycle state needed alignment. | partial | spec and `docs/03.specs/README.md` | Spec template and stage index checked | Align status and README state. |
| linked plan | Coverage, gap analysis, input reflection, verification, and final report are present; heading hierarchy was noncanonical. | partial | linked plan | Plan template headings checked | Normalize headings. |
| linked task | Task IDs T-001 through T-013, verification summary, skipped checks, and related links are recorded. | complete | linked task | Task template checked | Keep as baseline evidence. |
| `memory/progress.md` | Progress entries capture the gap-analysis pass and input-reflection follow-up. | complete | progress ledger | Progress coupling checked | Append for future repo-changing work. |
| `harness-catalog.md` | Workspace harness skill and task-to-skill routing are cataloged; metadata date was stale. | partial | harness catalog | Runtime roster SSoT checked | Refresh metadata. |
| `subagent-protocol.md` | Scratch workspace boundary is captured; metadata date was stale. | partial | subagent protocol | Protocol checked | Refresh metadata. |
| `.claude/skills/workspace-harness-audit/skill.md` | Broad audit Skill covers inventory, skill paths, raw ledger preservation, and P3 deferral. | complete | skill file | Baseline skill checked | Use for future broad refreshes. |
| Scoped README files | Current Spec/Plan/Task indexes satisfy scoped README contract. | complete | stage READMEs | Link/section scan checked | Keep current. |
| Legacy references | Legacy path references appear in routing policy, templates, historical context, or migration guidance. | complete | governance/templates/historical plans | Legacy scan checked | Retain documented migration references. |
| Current validation evidence | Baseline records PASS results; fresh validation must be rerun after edits. | partial | linked task/progress | Existing evidence checked | Rerun static gates. |

#### Documentation Lifecycle Reviewer Deletion/Consolidation/Deferral Candidates

| Target | Candidate type | Reason | Reference check | Impact scope | Recommended action |
| --- | --- | --- | --- | --- | --- |
| linked plan report sections | consolidation | Multiple post-template H1 sections fragmented one Plan document. | linked plan | Plan readability and template conformance | Demote headings. |
| historical raw subagent ledgers | deferral | Raw role output format was acknowledged missing from earlier durable evidence. | linked plan; progress | Audit replayability | Preserve fresh tables now; do not reconstruct older unavailable outputs. |
| legacy/superseded docs | retain | Historical records remain referenced and replacement context exists. | linked plan; spec README | Architecture and operations history | Do not delete. |
| P3 GitOps/Vault/CI/live items | deferral | Require semantic/runtime or owner-approved checks. | linked plan/progress | Runtime readiness | Track as separate tasks. |
| `.agents/rules/graphify.md`, `.agents/workflows/graphify.md` | deletion candidate | Ignored local surfaces are local-only drift. | linked plan | Local context only | Defer owner decision. |

#### Documentation Lifecycle Reviewer Unknown

| Item | Reason unknown | Follow-up check |
| --- | --- | --- |
| Live k3d/ArgoCD/Vault/ESO health | Live commands were not approved or run. | Run owner-approved read-only live validation. |
| `.env` value freshness | Values were intentionally not read or printed. | Human-only secret review. |
| GitHub branch protection/rulesets | Not represented in the worktree. | Inspect repository settings through approved GitHub path. |
| Optional local toolchain current state | Baseline recorded missing optional tools; refresh did not run all optional tool checks. | Recheck in CI or provisioned local shell. |
| `.agent/` absence | Missing path intent is not proven. | Owner decision or governance note. |
| Current external `SKILL.md` path existence | Docs reviewer did not recheck filesystem paths directly. | Use the path-level check in this Hybrid Refresh. |

#### Agent Governance Reviewer Summary

| Key finding | Evidence path | Impact | Risk | Action type | Recommended action |
| --- | --- | --- | --- | --- | --- |
| Gateway thinness and native instruction priority are mostly coherent. | `AGENTS.md`; `CLAUDE.md`; `GEMINI.md`; `.claude/CLAUDE.md` | Root files route instead of duplicating policy | Low | keep | Keep routing in `harness-catalog.md` and skills. |
| Local Claude settings remain the largest provider/runtime ambiguity. | `.claude/settings.local.json`; `.claude/settings.json` | Local allows may conflict with shared deny boundaries | Medium | defer | Verify precedence before local hardening. |
| SessionStart hook could run live read-only probes automatically. | `.claude/hooks/session-start.sh`; `.claude/settings.json`; `.codex/hooks.json` | No-live tasks could touch live state | Medium | supplement | Make probes opt-in or approval-gated. |
| Broad workspace audit workflow is correctly outside the gateway. | `.claude/skills/workspace-harness-audit/skill.md`; `harness-catalog.md` | Reduces prompt drift | Low | keep | Continue using the Skill. |
| Historical raw subagent ledgers remain weak evidence. | linked plan; progress | Replayability weaker | Medium | defer | Preserve current raw tables. |
| Runtime ownership is partly implicit for skills, hooks, and Codex files. | `scopes/meta.md`; `harness-catalog.md` | Role separation can be ambiguous | Low | supplement | Clarify meta/runtime ownership language. |

#### Agent Governance Reviewer Ledger

| Target | Finding | Type | Evidence path | Reference check | Recommended action |
| --- | --- | --- | --- | --- | --- |
| `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` | Thin gateway/provider shims. | complete | root shims | line-count and routing checked | Preserve. |
| `.claude/CLAUDE.md` | Runtime baseline clear; no-live interaction with SessionStart needed clarification. | partial | runtime baseline and hook | no-live opt-out absent | Add guard/documentation. |
| `CLAUDE.local.md` | Not present. | complete | workspace root | absence checked | No action. |
| `.agent/` | Path absent. | unknown | `.gitignore`; linked plan | intent unknown | Keep unknown; do not create. |
| `.agents/skills/**` | Existing local mirrors are non-canonical; new workspace skill mirror absence is acceptable. | complete | `.agents/skills/`; `.claude/skills/`; catalog | mirror policy checked | Keep ignored. |
| `.agents/rules`, `.agents/workflows` | Local graphify guidance can drift. | partial | ignored `.agents/` files | ignored/untracked | Defer owner decision. |
| `.claude/settings.json` | Shared settings block mutation families and wire hooks. | complete | settings JSON | mutation deny present | Keep. |
| `.claude/settings.local.json` | Broad local allows need precedence review. | partial | local settings | ignored/local-only | Verify precedence. |
| `.claude/hooks/session-start.sh` | Live read-only probes were automatic. | partial | hook script | read-only but live | Make opt-in. |
| `.claude/hooks/post-validate.sh`, lifecycle hooks | Static validation and lifecycle checks are scoped. | complete | hook scripts | shared validation surface | Preserve. |
| `.claude/agents/**`, `.codex/agents/**` | Eight Claude agents have matching Codex mirrors. | complete | agent folders | pair inventory complete | Preserve same-change mirror rule. |
| `.codex/hooks.json` | Reuses Claude hooks as context/validation wiring. | complete | Codex hooks | boundary documented | Preserve. |
| `harness-catalog.md` | Centralizes skill routing and readiness semantics. | complete | catalog | external skill paths present | Keep SSoT. |
| `workspace-harness-audit` skill | Captures repeated broad audit workflow. | complete | skill file | covers path checks and P1/P2/P3 | Use for next refresh. |
| `subagent-protocol.md` | Dispatch and scratch boundary explicit. | complete | protocol | role separation preserved | Preserve. |
| `meta.md` scope | Runtime file ownership wording was weak. | partial | meta scope | documentation-level gap | Clarify ownership. |

#### Agent Governance Reviewer Deletion/Consolidation/Deferral Candidates

| Target | Candidate type | Reason | Reference check | Impact scope | Recommended action |
| --- | --- | --- | --- | --- | --- |
| `.claude/settings.local.json` | deferral | Local broad allows may weaken shared boundaries depending on precedence. | local/shared settings | Local Claude runtime | Verify precedence, then narrow if needed. |
| `.claude/hooks/session-start.sh` | consolidation | Live probes belonged behind explicit no-live/opt-in behavior. | hook and settings | Claude/Codex startup | Add opt-in guard. |
| `.agents/rules/graphify.md` | deletion candidate | Ignored local rule can generate drift. | `.gitignore` | Local operator context | Defer owner decision. |
| `.agents/workflows/graphify.md` | deletion candidate | References external graphify skill outside repo SSoT. | `.gitignore` | Local operator context | Defer owner decision. |
| runtime file ownership | consolidation | Hook/skill/Codex ownership was not explicit in scope ownership. | meta scope/catalog | Governance role separation | Clarify. |
| historical raw subagent ledgers | deferral | Earlier raw tables not durable current-state files. | linked plan/skill | Replayability | Preserve future/current raw tables. |
| `.agent/` | deferral | Path absent and ignored, intent unknown. | `.gitignore` | Local runtime discovery | Keep absent unless requested. |

#### Agent Governance Reviewer Unknown

| Item | Reason unknown | Follow-up check |
| --- | --- | --- |
| Claude local/project permission precedence | Broad local settings were not live-tested. | Verify without destructive commands. |
| No-live task handling for SessionStart | Hook opt-out was not documented before this change. | Validate opt-in behavior. |
| `.agent/` absence | Missing path intent is unknown. | Ask owner before creating. |
| Live k3d/ArgoCD/Vault/ESO health | Live commands prohibited. | Run only after approval. |
| GitHub branch protection/rulesets | Not in worktree. | Inspect GitHub settings separately. |
| `.env` value freshness | Secret values intentionally not read. | Human-only review. |
| Graphify local surfaces owner intent | Ignored local files may be intentional or stale. | Ask owner. |

#### Scripts Reviewer Summary

| Key finding | Evidence path | Impact | Risk | Action type | Recommended action |
| --- | --- | --- | --- | --- | --- |
| Current `scripts/` inventory is five shell scripts; no one-off or unknown script found. | `scripts/README.md`; `scripts/` | Deletion scope stays narrow | Low | keep | Retain scripts. |
| Four scripts are operations-critical validators; LLM Wiki generator is reusable helper with `--check`. | `scripts/README.md`; CI; hooks | Avoids cleanup misclassification | Low | keep | Preserve contracts. |
| GitOps root app validator hardening is implemented. | `validate-gitops-structure.sh`; linked task | Empty root app set fails statically | Low | verify | Keep root app count assertion. |
| Hook simulation bypass is internal-only. | `scripts/README.md`; hooks; quality gate | Reduces misuse | Low | keep | Keep manual validation unbypassed. |
| Script command-reference validation is allowlist-scoped. | `scripts/README.md`; quality gate | New reference surfaces can drift | Medium | monitor | Update allowlist with new script surfaces. |
| `scripts/README.md` used a 2026-05-17 inventory snapshot after 2026-05-24 hardening. | `scripts/README.md`; linked plan | Evidence freshness weaker | Low | refresh evidence | Refresh wording. |
| Secret scanner tolerance lacks fixture coverage. | `check-secret-handling.sh`; `tests/README.md` | False positive/negative regressions can hide | Medium | test hardening | Add fixtures only in scanner task. |
| Optional local toolchain unavailable. | QA docs and task | Local validation limited | Medium | deferral | Treat optional tools as CI/provisioned evidence. |

#### Scripts Reviewer Ledger

| Target | Finding | Type | Evidence path | Reference check | Recommended action |
| --- | --- | --- | --- | --- | --- |
| `validate-repo-quality-gates.sh` | Central governance validator tied to CI, hooks, inventory, docs contracts, and simulations. | operations-critical/reusable | script | CI, hooks, README | Keep; split only preserving public command. |
| `validate-gitops-structure.sh` | Checks root app existence, kind, count, kustomization parsing, and completeness. | operations-critical/reusable | script | CI, PR template, GitOps README | Preserve zero-root-app semantics. |
| `validate-k8s-manifests.sh` | YAML parser with optional kube-linter. | operations-critical/reusable | script | CI, hooks, tests README | Report optional kube-linter skip. |
| `check-secret-handling.sh` | Plaintext-secret scanner redacts matched values. | operations-critical/reusable | script | CI, hooks, PR template | Add fixtures before broadening. |
| `generate-llm-wiki-index.sh` | Generated index helper; `--check` is quality-gate mode. | development-helper/reusable | script | quality gate, LLM Wiki docs | Keep; use `--check` for read-only checks. |
| `scripts/README.md` | Inventory, retention tiers, command contracts, tools, and bypass warning present. | reusable | README | root README, PR template, tests README | Refresh evidence date. |

#### Scripts Reviewer Deletion/Consolidation/Deferral Candidates

| Target | Candidate type | Reason | Reference check | Impact scope | Recommended action |
| --- | --- | --- | --- | --- | --- |
| `scripts/*.sh` | no deletion candidate | All five scripts have Tier A or B retention evidence. | README, CI, hooks | CI/hooks/manual validation | Do not delete. |
| `validate-repo-quality-gates.sh` | deferral | Large validator but high blast radius if split casually. | script and CI | Repo governance gate | Defer splitting. |
| `check-secret-handling.sh` | deferral | Regex behavior lacks fixtures. | scanner and tests README | Secret static gate | Add fixtures in dedicated task. |
| `validate-k8s-manifests.sh` | deferral | Optional kube-linter unavailable locally. | validator and tests README | Manifest validation | Confirm lint in CI/toolchain. |
| `scripts/README.md` | evidence refresh | Snapshot date predates 2026-05-24 hardening. | README and linked plan | Reviewer evidence | Refresh wording. |

#### Scripts Reviewer Unknown

| Item | Reason unknown | Follow-up check |
| --- | --- | --- |
| Live k3d/ArgoCD/Vault/ESO health | Live commands out of scope. | Separate approved read-only checks. |
| `.env` value freshness | Secret values not inspected. | Human-only review. |
| Secret scanner tolerance | No fixture suite run or created. | Add positive/negative fixtures before scanner changes. |
| Remote CI/ruleset state | Worktree cannot prove GitHub settings. | Inspect GitHub checks/settings if needed. |
| Optional toolchain coverage | Optional tools unavailable. | Run in CI/provisioned shell. |

#### GitOps Infrastructure Reviewer Summary

| Key finding | Evidence path | Impact | Risk | Action type | Recommended action |
| --- | --- | --- | --- | --- | --- |
| Static GitOps/manifests baseline is structurally healthy. | validators and static tests | Root App-of-Apps, Kustomize, YAML, contracts, secret scan pass | Low | keep | Keep static gates as merge prerequisites. |
| ESO egress policy is narrower than adjacent namespace policies. | `external-secrets-egress-to-vault.yaml`; adjacent policies | ESO may need DNS/API egress | High | deferred fix | Separate GitOps task with live ESO validation. |
| Vault policy lacks ArgoCD notifications path. | `eso-read.hcl`; notifications ExternalSecret | Slack token sync can fail | High | deferred fix | Add policy in separate security change. |
| Apps AppProject omits ExternalSecret while onboarding example includes it. | `appproject-apps.yaml`; sample app | Secret-backed app can be rejected | Medium | deferred fix | Decide onboarding model first. |
| Sample app Vault key format differs from active ClusterSecretStore usage. | sample ExternalSecret; platform ESO manifests | Copy-paste onboarding risk | Medium | consolidation | Align sample in separate app onboarding task. |
| Bootstrap CR ownership split remains. | bootstrap script and cluster manifests | Drift possible | High | design deferral | Decide owner model. |
| Cloud example freshness evidence is mixed. | examples READMEs; version inventory | Weak freshness evidence | Low | evidence refresh | Normalize wording to inventory. |
| Original raw subagent ledger preservation remained weak. | linked plan/progress/skill | Replayability weaker | Medium | future-process fix | Preserve fresh tables. |

#### GitOps Infrastructure Reviewer Ledger

| Target | Finding | Type | Evidence path | Reference check | Recommended action |
| --- | --- | --- | --- | --- | --- |
| `gitops/apps/root` | 17 non-kustomization ArgoCD Application manifests. | pass | root kustomization and validator | GitOps structure PASS | Keep assertion. |
| `gitops/clusters/local/root-application.yaml` | Root app targets `gitops/apps/root` on `main`. | pass | root application | Static contract PASS | Keep entrypoint. |
| `applicationset-apps.yaml` | Workload ApplicationSet uses project `apps`; ExternalSecret caveat remains. | pass with caveat | ApplicationSet/AppProject | Static PASS | Fix secret model separately. |
| `appproject-apps.yaml` | Allows workloads but omits `external-secrets.io/ExternalSecret`. | gap | AppProject and sample | P3 already recorded | Update after decision. |
| ESO egress policy | Allows only Vault IP/port. | gap | NetworkPolicy | Compared adjacent policies | Separate task. |
| Vault ESO policy | Omits `platform/notifications`. | gap | Vault HCL and ExternalSecret | Static contract partial | Separate task. |
| external service contracts | PostgreSQL, Vault, Valkey contracts present. | pass | platform external services | static contract PASS | Keep; live unknown. |
| k3d config | Matches version inventory and disables bundled Traefik/servicelb. | pass | k3d config/version inventory | YAML PASS | Keep. |
| `traefik/` | Reference-only helper boundary is clear and YAML valid. | pass | Traefik README/configs | YAML PASS | Keep separate from GitOps. |
| `examples/sample-app` | ExternalSecret excluded from sample kustomization by default. | pass with caveat | sample app | syntax/secret scan PASS | Keep disabled until model fixed. |
| `examples/aws`, `examples/azure` | Reference-only boundary documented; snapshot wording lagged inventory. | weak evidence | examples READMEs and version inventory | repo-static only | Refresh wording. |

#### GitOps Infrastructure Reviewer Deletion/Consolidation/Deferral Candidates

| Target | Candidate type | Reason | Reference check | Impact scope | Recommended action |
| --- | --- | --- | --- | --- | --- |
| AppProject `Namespace` whitelist | deletion candidate | Namespace appears platform-owned while ApplicationSet uses `CreateNamespace=true`. | platform namespace and ApplicationSet | AppProject least privilege | Defer. |
| `gitops/clusters/local` bootstrap resources | consolidation | AppProject/ApplicationSet/root app are bootstrap-applied. | bootstrap script and manifests | Bootstrap/ownership | Separate design task. |
| sample ExternalSecret | consolidation | RemoteRef key format includes mount prefix unlike active platform pattern. | sample and platform ESO | App onboarding | Separate app onboarding task. |
| Vault policy | deferral | Adding notifications changes secret access policy. | HCL and ExternalSecret | Vault/ESO/ArgoCD | Separate security change. |
| ESO egress policy | deferral | DNS/API egress is runtime semantic change. | NetworkPolicy | ESO reconciliation | Separate NetworkPolicy task. |
| examples snapshot wording | consolidation | Mixed date evidence. | examples and version inventory | Cloud references | Refresh wording. |
| `traefik/` | keep | Reference-only helper boundary explicit. | README and YAML | Local UI helper | Retain. |

#### GitOps Infrastructure Reviewer Unknown

| Item | Reason unknown | Follow-up check |
| --- | --- | --- |
| Live k3d, ArgoCD, ESO, Vault, PostgreSQL, Valkey, TLS, and NetworkPolicy behavior | Live commands out of scope. | Approved live validation only. |
| Vault secret value freshness | Values not inspected. | Secret-safe operator review. |
| Official cloud latest support state | External provider freshness not queried. | Refresh version inventory from official sources. |
| kube-linter findings | Optional tool unavailable. | Run in prepared environment. |
| GitHub rulesets and remote CI | Not in worktree. | Separate CI/governance review. |

#### Environment Quality Reviewer Summary

| Key finding | Evidence path | Impact | Risk | Action type | Recommended action |
| --- | --- | --- | --- | --- | --- |
| `.env.example` and local `.env` key names match; `.env` remains ignored/untracked. | env files and `.gitignore` | Template consistency intact without values | Low | keep | Keep key-name-only comparison. |
| Static quality gates passed in read-only refresh. | validators and static tests | Committed baseline structurally healthy | Low | keep | Continue static gate bundle. |
| Secret handling has static layers, but live Vault/ESO remains deferred. | pre-commit, gitleaks, secret scanner, plan | Runtime secret reconciliation not proven | High | defer | Separate approved live checks. |
| Local lint toolchain incomplete. | pre-commit, tests README, scripts README | Local review cannot reproduce all lint/security checks | Medium | improve | Install tools or rely on CI. |
| Workflows are structurally checked, but actions are tag-pinned with `unpinned-uses` disabled. | workflows, zizmor, quality gate | Supply-chain hardening remains policy decision | Medium | defer | Decide SHA pinning separately. |
| Path-filtered CI jobs can skip by design. | CI workflow | Skipped-check interpretation depends on branch protection | Medium | verify | Confirm rulesets. |
| Raw subagent ledgers were not reconstructed historically. | plan and skill | Replayability weaker | Medium | defer | Preserve fresh tables. |
| Live QA scripts exist but were not run. | infrastructure live tests | Runtime health unknown | High | defer | Run only after approval. |

#### Environment Quality Reviewer Ledger

| Target | Finding | Type | Evidence path | Reference check | Recommended action |
| --- | --- | --- | --- | --- | --- |
| `.env.example`, `.env` | Key names match; values not printed. | pass | env files | key-name-only comparison | Keep. |
| `.env` tracking | `.env` ignored and untracked; `.env.example` tracked. | pass | `.gitignore`; env template | git ls-files check | Keep local-only. |
| Secret scanners | Gitleaks, detect-secrets, and manifest scanner configured. | coverage | configs and scanner | secret scan PASS | Keep layered static scan. |
| manifest validation | YAML passes; kube-linter optional and skipped locally. | skipped check risk | validator and config | manifest check PASS with skip | Install or use CI evidence. |
| CI workflow | Required jobs and summary present. | pass | workflow and gate | quality gate PASS | Keep dependencies. |
| workflow syntax | YAML parser passes; actionlint unavailable locally. | partial | workflow/pre-commit | local actionlint missing | Verify in CI/toolchain. |
| action pinning | Tag pins accepted by current config. | deferred risk | zizmor/workflows/inventory | quality gate allows only disable | Decide SHA policy separately. |
| test model | Static infra validation, no app unit/typecheck stack. | context | tests/scripts READMEs | no app config found | Add tests when app code exists. |
| static contracts | Infra static contracts pass. | pass | static contract script | PASS | Keep. |
| live tests | Live scripts call runtime surfaces and were not run. | deferred | infrastructure live tests | not executed | Run with approval. |

#### Environment Quality Reviewer Deletion/Consolidation/Deferral Candidates

| Target | Candidate type | Reason | Reference check | Impact scope | Recommended action |
| --- | --- | --- | --- | --- | --- |
| GitHub Actions SHA pinning | deferral | SHA pinning stronger than current tag policy. | `.github/zizmor.yml` | CI supply chain | Separate task. |
| Local optional QA tools | deferral | Tooling not installed. | pre-commit config | Local QA parity | Install or use CI. |
| Live runtime checks | deferral | Live scripts require prohibited runtime commands. | live test scripts | Runtime QA | Approved read-only pass. |
| historical raw subagent ledgers | deferral | Earlier docs summarized role outputs only. | linked plan | Replayability | Preserve fresh tables. |
| `.env` value freshness | deferral | Secret-sensitive. | linked plan | Environment correctness | Human-only review. |
| CI skipped-job interpretation | improvement candidate | Path filters and rulesets interact outside worktree. | workflow and GitHub docs | CI governance | Verify rulesets. |

#### Environment Quality Reviewer Unknown

| Item | Reason unknown | Follow-up check |
| --- | --- | --- |
| `.env` value correctness | Values intentionally not inspected. | Human-only review. |
| Live k3d/ArgoCD/Vault/ESO health | Live commands out of scope. | Approved read-only validation. |
| Remote CI run status | Remote checks not queried. | Inspect GitHub checks. |
| Full local pre-commit result | `pre-commit` unavailable. | Run in prepared toolchain or CI. |
| Full workflow lint/security result | `actionlint` and `zizmor` unavailable locally. | Run CI/pre-commit jobs. |
| kube-linter semantic result | `kube-linter` unavailable. | Install or use CI. |
| Historical raw role tables | Earlier committed files lack authoritative raw tables. | Preserve tables during current/future audits. |

#### Skills & Harness Reviewer Summary

| Key finding | Evidence path | Impact | Risk | Action type | Recommended action |
| --- | --- | --- | --- | --- | --- |
| Agent and Codex mirror surfaces are structurally aligned; repo quality gate passed. | quality gate; `.claude/agents/`; `.codex/agents/` | No tracked mirror drift | Low | keep | Keep mirror checks. |
| External `SKILL.md` paths are recorded and present, but durable verification was grouped by area. | catalog, plan, task | Path replayability weaker | Low | evidence hardening | Add path-level ledger. |
| `workspace-harness-audit` captures broad audit workflow; historical raw ledgers remain deferred. | skill and plan | Future protected, original less replayable | Medium | deferral | Keep deferral and preserve fresh raw tables. |
| SessionStart hooks ran live probes automatically. | hook/settings/Codex hooks/spec | Live state could be touched before approval | Medium | hook boundary | Make probes opt-in. |
| Local Claude settings allow broad command families. | local settings and local Hookify rules | Shared deny boundary may be weakened if precedence wins | High | governance check | Verify and harden later. |
| `_workspace/` scratch paths are authorized but not ignored. | incident/RCA skills, protocol, `.gitignore` | Scratch files could be staged | Medium | guardrail | Add ignore/check coverage. |
| Meta scope says no dedicated subagent while supervisor imports meta. | meta scope; supervisor; catalog | Routing wording ambiguous | Low | documentation fix | Clarify supervisor exception. |
| Workflow/reference distinction is prose only. | catalog and skill files | Reviewers may apply wrong checklist expectations | Low | catalog refinement | Add per-skill type column. |
| Governance document dates were stale. | catalog, protocol, progress | Freshness signals weaker | Low | metadata fix | Refresh metadata. |

#### Skills & Harness Reviewer Ledger

| Target | Finding | Type | Evidence path | Reference check | Recommended action |
| --- | --- | --- | --- | --- | --- |
| `workspace-harness-audit` skill | Reusable broad audit workflow exists. | confirmed OK | skill and catalog | contract checked | Keep. |
| External requested skills | All checked paths present; committed evidence was area-level. | weak evidence | catalog/plan | path check | Store path-level results. |
| `.agents/skills/` | Local mirrors are ignored/non-canonical. | local-only | `.agents/skills/`; `.claude/skills/` | validator checks existing mirrors | No tracked action. |
| graphify local files | Ignored graphify workflow remains outside repo SSoT. | deferral | `.agents/`; `.claude/CLAUDE.md` | local-only | Defer owner decision. |
| SessionStart hook | Performs live `k3d`/`kubectl get` checks automatically. | confirmed gap | hook/settings/Codex hooks | live checks deferred in spec/plan | Gate behind opt-in. |
| local settings | Broad local allows include destructive/live families. | local risk | settings.local | Hookify warns only | Verify precedence. |
| scratch boundary | `_workspace/` and `_workspace_prev/` named but not ignored. | guardrail gap | skills/protocol/gitignore | absent now | Ignore or validate cleanup. |
| meta/supervisor bridge | Supervisor imports `meta` while meta says no dedicated subagent. | wording drift | supervisor and meta scope | other bridge rows ok | Clarify. |
| raw subagent ledgers | Original role output tables not durably archived. | deferred evidence gap | plan/skill | plan records limitation | Preserve current/future tables. |
| skill type distinction | Catalog lacked per-skill type metadata. | weak routing | catalog and skills | reference skills differ | Add type column. |

#### Skills & Harness Reviewer Deletion/Consolidation/Deferral Candidates

| Target | Candidate type | Reason | Reference check | Impact scope | Recommended action |
| --- | --- | --- | --- | --- | --- |
| `.claude/hooks/session-start.sh` live probes | consolidation | Live health checks were automatic hook behavior. | spec and hook | startup | Make opt-in. |
| `.claude/settings.local.json` | deferral | Broad local permissions may weaken command boundaries. | local/shared settings | local runtime | Verify precedence. |
| graphify local files | deletion/consolidation | Ignored workflow can drift. | `.agents/`; `.gitignore` | local exploration | Remove locally or promote only if mandatory. |
| `_workspace/`, `_workspace_prev/` | consolidation | Scratch paths described but not ignored. | skills and `.gitignore` | scratch output | Add ignore/check coverage. |
| historical raw subagent ledgers | deferral | Original tables not authoritative committed artifacts. | plan and skill | replayability | Keep limitation; preserve fresh/current tables. |
| `.agents/skills/workspace-harness-audit/skill.md` | deferral | Local mirror absent but `.agents/` is not SSoT. | mirrors and catalog | local convenience | Do not add unless operator needs it. |
| per-skill type metadata | consolidation | Workflow/reference distinction not machine-checkable per skill. | catalog and skills | skill routing | Add type column. |

#### Skills & Harness Reviewer Unknown

| Item | Reason unknown | Follow-up check |
| --- | --- | --- |
| Actual runtime effect of SessionStart live probes | Live commands not run. | Run only with explicit approval. |
| Settings precedence | Local/shared merge behavior not verified. | Non-destructive permission simulation or provider docs. |
| `.agents/skills/workspace-harness-audit` mirror absence | Operator intent unknown. | Ask local operator or document existing-only mirror policy. |
| Graphify local workflow intent | Optional local or mandatory unknown. | Owner decision. |
| Historical raw role table source | Not in committed artifacts. | Preserve directly in future/current audits. |
| Codex provider note location | `agents-md.md` may cover Codex, but no `codex.md`. | Confirm provider mapping before adding file. |

### Hybrid Verification Results

| Command or method | Result | Record location |
| --- | --- | --- |
| `bash scripts/validate-repo-quality-gates.sh .` | PASS | linked task Hybrid Refresh section |
| `bash scripts/generate-llm-wiki-index.sh --check` | PASS | linked task Hybrid Refresh section |
| `bash scripts/validate-gitops-structure.sh` | PASS; root app manifest count: 17 | linked task Hybrid Refresh section |
| `bash scripts/validate-k8s-manifests.sh .` | PASS for YAML syntax; optional `kube-linter` skipped because it is not installed locally | linked task Hybrid Refresh section |
| `bash scripts/check-secret-handling.sh .` | PASS | linked task Hybrid Refresh section |
| `bash infrastructure/tests/verify-contracts-static.sh` | PASS | linked task Hybrid Refresh section |
| shell syntax check | PASS | linked task Hybrid Refresh section |
| runtime JSON parse | PASS for `.claude/settings.json` and `.codex/hooks.json` | linked task Hybrid Refresh section |
| `.env.example` and `.env` key comparison | PASS after Bash rerun; key names matched without printing values | linked task Hybrid Refresh section |
| Path-level external `SKILL.md` check | PASS; all listed paths present | this plan; linked task |
| `git diff --check` | PASS | linked task Hybrid Refresh section |
| Live k3d/ArgoCD/Vault/ESO validation | skipped by task boundary | Deferred Items |

### Hybrid Checklist Gate

| Checklist item | Status | Evidence |
| --- | --- | --- |
| Is the goal clear in one sentence? | pass | Hybrid refresh plan and existing Spec 006 |
| Are related files, logs, issues, or reproduction steps provided or discovered? | pass | Six fresh role reviews, file inventory, path check, static verification plan |
| Are modification scope and forbidden scope separated? | pass | Hybrid P1/P2/P3 tables |
| Are existing patterns, compatibility, and dependency rules stated? | pass | GitOps-first, no-live default, gateway-thin, template-first, task-to-skill routing |
| Are test, lint, and type-check commands identified? | pass | Verification Plan and Hybrid Verification Results |
| Are completion criteria measurable? | pass | Spec VAL-SPC-006-006, task T-014 through T-020 |
| Are recurring instructions moved or planned for `AGENTS.md` or Skills? | pass | `workspace-harness-audit` skill and `harness-catalog.md` |

### Hybrid Final Report

| Section | Hybrid refresh result |
| --- | --- |
| Baseline Instruction Check | Rechecked gateway shims, governance docs, templates, `.claude/`, `.codex/`, `.agents/`, and missing `.agent/`; no gateway expansion was needed. |
| Coverage Ledger Summary | All target areas were inventoried; static documentation/scripts were mostly complete, while GitOps/runtime/CI/live areas remain partial or unknown where external state is required. |
| Subagent Summary | Six fresh read-only role reviews completed and are preserved above in role table shape. |
| Integrated Gap Analysis Summary | New safe gaps were documentation evidence, metadata, no-live hook boundary, scratch ignore coverage, and skill-path replayability; high-risk runtime/secret/CI policy items remain deferred. |
| spec/task/plan Updates | Existing Spec 006, linked plan, linked task, and progress ledger were updated in place. |
| Implementation Changes | Implemented only P1/P2 guardrail and evidence changes; no Kubernetes resource semantics, ArgoCD structure, Vault policy, secret/env policy, CI structure, or live checks were changed. |
| Deletion, Consolidation, and Deferred Items | No deletion performed; graphify local cleanup, AppProject/Vault/NetworkPolicy/bootstrap/CI/live items remain deferred with pre-checks. |
| Verification | Repo-static bundle passed; optional `kube-linter` and live validation remain explicitly skipped/deferred. |
| Checklist Gate | Passed with evidence recorded above. |
| Remaining Risks and Next Work | Live runtime state, `.env` values, GitHub rulesets, optional toolchain, `.claude/settings.local.json` precedence, and P3 GitOps/security decisions remain open. |

## Verification Results

| Command or method | Result | Record location |
| --- | --- | --- |
| `bash scripts/generate-llm-wiki-index.sh --check` | PASS | linked task |
| `bash scripts/validate-repo-quality-gates.sh .` | PASS | linked task |
| `bash scripts/validate-gitops-structure.sh` | PASS, root app manifest count: 17 | linked task |
| `bash scripts/validate-k8s-manifests.sh .` | PASS for YAML syntax; optional `kube-linter` skipped because it is not installed locally | linked task |
| `bash scripts/check-secret-handling.sh .` | PASS | linked task |
| `bash infrastructure/tests/verify-contracts-static.sh` | PASS | linked task |
| shell syntax check | PASS | linked task |
| runtime JSON parse | PASS for `.claude/settings.json` and `.codex/hooks.json` | linked task |
| `.env.example` and `.env` key comparison | PASS, key names match without printing values | linked task |
| required external `SKILL.md` path check | PASS, all listed paths present | linked task |
| `git diff --check` | PASS | linked task |

## Checklist Gate

| Checklist item | Status | Evidence |
| --- | --- | --- |
| Is the goal clear in one sentence? | pass | User task contract and this plan summary |
| Are related files, logs, issues, or reproduction steps provided or discovered? | pass | Six subagent reviews and repo-static checks |
| Are modification scope and forbidden scope separated? | pass | P1/P2/P3 sections |
| Are existing patterns, compatibility, and dependency rules stated? | pass | AGENTS thin gateway, GitOps-first, template-first rules |
| Are test, lint, and type-check commands identified? | pass | Verification Plan |
| Are completion criteria measurable? | pass | Completion Criteria and verification commands |
| Are recurring instructions moved or planned for `AGENTS.md` or Skills? | pass | Routing consolidated into `harness-catalog.md` |

## Final Report

### 1. Baseline Instruction Check

| Target | Checked | Key impact |
| --- | --- | --- |
| `AGENTS.md` | yes | Thin gateway remains primary contract |
| `CLAUDE.md` | yes | Claude shim remains thin |
| `.claude/CLAUDE.md` | yes | Runtime baseline and hook boundaries preserved |
| `CLAUDE.local.md` | yes | Not present |
| `GEMINI.md` | yes | Gemini shim remains thin |
| `docs/00.agent-governance/` | yes | Governance SSoT and matrix-first rules used |
| `docs/99.templates/` | yes | Spec/task/plan templates followed |
| `.agent/` | yes | Missing path recorded as unknown |
| `.agents/` | yes | Ignored local mirrors and graphify surfaces recorded |
| `.claude/` | yes | Agents, hooks, skills, settings reviewed |
| `.codex/` | yes | Agent mirrors and hook wiring reviewed |

### 2. Coverage Ledger Summary

| Area | Investigation status | Gap count | Candidate count | Unknown |
| --- | --- | ---: | ---: | --- |
| Documentation | complete | 4 | 6 | live parity, strict exception policy |
| Scripts | complete | 2 | 1 | secret scan depth |
| GitOps/infrastructure | partial | 8 | 6 | live cluster, Vault, external reachability |
| Environment/QA/CI | partial | 4 | 4 | optional tools, CI/rulesets, env values |
| Agent governance | partial | 6 | 5 | local precedence, `.agent/` absence |

### 3. Subagent Summary

| Role | Status | Key findings | Unknown |
| --- | --- | --- | --- |
| Documentation Lifecycle Reviewer | complete | Lifecycle and templates are healthy; one historical plan/task exception | live runtime parity |
| Agent Governance Reviewer | complete | Gateway/mirrors coherent; local settings and graphify local surfaces deferred | local permission precedence |
| Scripts Reviewer | complete | All scripts retained; root app count and hook env docs need hardening | env bypass audience |
| GitOps Infrastructure Reviewer | complete | Semantic GitOps gaps in ESO, Vault, AppProject, bootstrap ownership | live ArgoCD/Vault state |
| Environment Quality Reviewer | complete | Env keys match; CI/static gates clear; optional tools missing | remote CI/rulesets |
| Skills & Harness Reviewer | complete | Scope bridge drift and scratch convention need correction | live hook behavior |

### 4. Integrated Gap Analysis Summary

| Area | Key Gap | Risk | Action | Priority |
| --- | --- | --- | --- | --- |
| Agent governance | stale scope bridge rows | Low | update | P1 |
| Agent governance | task-to-skill routing not consolidated | Medium | add to catalog | P2 |
| Scripts | root app manifest count not asserted | Medium | harden validator | P2 |
| GitOps | ESO/Vault/AppProject semantic gaps | High | defer | P3 |
| CI/CD | tag pinning accepted risk | Medium | defer | P3 |

### 5. spec/task/plan Updates

| Document | Change | Linked work |
| --- | --- | --- |
| `docs/03.specs/006-workspace-harness-gap-analysis/spec.md` | New technical contract | T-001 |
| `docs/04.execution/plans/2026-05-24-workspace-harness-gap-analysis.md` | New plan with ledgers and report | T-002 |
| `docs/04.execution/tasks/2026-05-24-workspace-harness-gap-analysis.md` | New execution evidence | T-003 |
| stage README indexes | New entries | T-001 |
| `memory/progress.md` | Progress and evidence entry | T-009 |

### 6. Skill and Harness Updates

| Target | Action | Skill used | Reason |
| --- | --- | --- | --- |
| `.claude/skills/workspace-harness-audit/skill.md` | Added repo-local workflow Skill | `writing-skills`, `write-a-skill`, `skill-creator`, `skill-improver` guidance | Capture repeated broad workspace audit workflow and prevent future omission of skill path checks or raw ledger preservation |
| `docs/00.agent-governance/harness-catalog.md` | Added skill inventory row and retained external requested skill routing | `grill-with-docs`, `agent-md-refactor` routing principles | Keep `AGENTS.md` thin while centralizing harness routing |
| Required external `SKILL.md` paths | Verified exact paths | `grill-with-docs` plus task-specific skill routing | Satisfy missing-path Gap recording contract; no missing paths found |

### 7. Implementation Changes

| Target | Change | Reason | Linked task |
| --- | --- | --- | --- |
| `docs.md` scope | Add `wiki-curator` bridge | Match actual import | T-004 |
| `infra.md` scope | Add `gitops-reviewer` bridge | Match actual import | T-004 |
| `subagent-protocol.md` | Add scratch boundary | Prevent ad-hoc durable outputs | T-005 |
| `harness-catalog.md` | Add task-to-skill routing and skill type note | Consolidate recurring workflow routing | T-005 |
| `validate-gitops-structure.sh` | Add root app manifest count assertion | Close static validation gap | T-006 |
| `scripts/README.md` | Clarify hook env bypass | Prevent manual misuse | T-006 |
| `.claude/skills/workspace-harness-audit/skill.md` | Add reusable workspace audit workflow | Close repeated-workflow Skill gap | T-012 |
| this plan and linked task | Add input reflection follow-up and skill path check evidence | Close weakly reflected original input tasks | T-010, T-011 |

### 8. Deletion, Consolidation, and Deferred Items

| Target | Type | Reason | Reference check | Recommended action |
| --- | --- | --- | --- | --- |
| `.agents/rules/graphify.md` | deletion candidate | ignored local drift | local ignored only | defer owner decision |
| `gitops/clusters/local` ownership | consolidation | bootstrap CR drift | static review partial | defer design |
| ESO NetworkPolicy | deferred | runtime semantic change | manifest review | separate task |
| Vault policy | deferred | secret access policy | manifest/HCL review | separate task |
| SHA pinning | deferred | CI policy | workflow/zizmor review | separate task |
| historical raw subagent ledgers | deferred | original raw role output tables are not current-state files | current plan has integrated summaries | preserve raw Summary/Ledger tables in future runs through `workspace-harness-audit` |

### 9. Verification

| Command or method | Result | Record location |
| --- | --- | --- |
| Full verification bundle | PASS; optional `kube-linter` unavailable and live checks deferred | task verification summary |
| External required skill path check | PASS; no missing paths | input reflection follow-up |

### 10. Checklist Gate

| Checklist item | Status | Evidence |
| --- | --- | --- |
| Goal clear | pass | task contract |
| Related files discovered | pass | ledger |
| Scope separated | pass | P1/P2/P3 |
| Existing patterns stated | pass | governance links |
| Commands identified | pass | verification plan |
| Criteria measurable | pass | completion criteria |
| Recurring rules routed | pass | harness catalog |

### 11. Remaining Risks and Next Work

- Complete live runtime validation only with explicit approval.
- Implement P3 GitOps and security-policy changes as separate reviewed tasks.
- Verify optional toolchain and GitHub rulesets outside this local static pass.
- Do not reconstruct historical raw subagent output tables without authoritative
  source output; preserve them directly in future workspace harness audits.

## CEO Review Follow-up - 2026-05-24

### CEO Review Scope

`/home/hy/.agents/skills/gstack/plan-ceo-review/SKILL.md` was applied in
HOLD SCOPE mode. The goal was not to expand the platform, but to pressure-test
whether the first user task contract still had weak or missing evidence in the
Hybrid Refresh plan after the later P3 remediation commits.

The skill preamble, design-doc persistence, and telemetry steps were not run
because they write to `~/.gstack` outside the repository. The review was
preserved in canonical SDD artifacts instead.

### CEO System Audit

| Check | Result | Evidence |
| --- | --- | --- |
| Current branch | `main` | `git branch --show-current` |
| Base branch | `origin/main` | `git symbolic-ref refs/remotes/origin/HEAD` |
| Worktree before edits | clean | `git status --short` |
| Recent history | P3 remediation and follow-up evidence are the latest commits | `git log --oneline -30` |
| Stashes | none | `git stash list` |
| TODO/FIXME scan | only template/example TODO-like references found | `rg -l "TODO\|FIXME\|HACK\|XXX"` |
| Design doc | not used | canonical SDD plan/task/spec are the source of truth for this repository task |

### CEO Mode and Alternatives

| Approach | Summary | Effort | Risk | Pros | Cons | Reuses |
| --- | --- | --- | --- | --- | --- | --- |
| A. Minimal current-state overlay | Add only the missing skill-path evidence and a P3 supersession note. | S | Low | Small diff; fixes the stale claims | Does not improve future audit behavior much | Existing plan/task |
| B. Canonical CEO follow-up | Add CEO review findings, coverage matrix, P3 current-state overlay, task/spec/progress evidence, and skill guardrail. | M | Low | Fixes the current gap and prevents the same drift later | More documentation rows | Existing Spec 006, plan/task, `workspace-harness-audit` |
| C. New separate CEO plan | Create a standalone CEO review plan/task pair. | M | Medium | Isolates the review | File proliferation and weaker continuity | Existing templates |

**Recommendation**: choose Approach B. It closes the real gaps without creating
another parallel artifact tree.

### CEO Initial-Contract Coverage Ledger

| Initial input requirement | Current Hybrid evidence | CEO judgment | Action |
| --- | --- | --- | --- |
| Use `grill-with-docs` to review all entered matters | Plan/task record `grill-with-docs`, Office-Hours, and Brainstorming follow-ups | complete | Keep evidence |
| Consider low, medium, and high risk | P1/P2/P3 tables exist and P3 follow-up has separate plan/task | complete | Add current-state overlay |
| Check exact required `SKILL.md` paths | Hybrid path ledger exists, but it omitted the first prompt's `brainstorming` exact path | weak evidence | Add `/home/hy/.agents/skills/brainstorming/SKILL.md` |
| Record current named `gstack-plan-ceo-review` usage | No prior durable evidence for this named skill | gap | Add this CEO Review Follow-up |
| Keep `AGENTS.md` as thin gateway | Gateway remains thin; routing lives in governance docs | complete | No change |
| Preserve P3 items and follow-up work | Historical Hybrid rows still say selected P3 items are deferred even after approved P3 remediation | stale evidence | Add P3 current-state overlay |
| Run six role-based subagent reviews for Hybrid freshness | Fresh role tables are preserved in the plan | complete | No change |
| Preserve raw Summary/Ledger/Candidates/Unknown shape | Hybrid plan preserves fresh tables; historical raw tables remain unavailable | partial but explicit | Keep limitation |
| Run verification and checklist gates | Static gates recorded; live runtime remains unavailable | complete with limitation | Keep live limitation |
| Commit by task unit | Recent commits are task-sized: plan, implementation, evidence | complete | Record in progress entry |

### CEO Findings

| ID | Finding | Evidence path | Impact | Risk | Action type | Priority | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CEO-001 | First prompt's exact `brainstorming` skill path was not represented in the Hybrid path-level ledger | this plan `Hybrid Path-Level External Skill Check` | Missing-path replayability gap | Low | supplementation | P1 | Implemented in this plan |
| CEO-002 | Current `gstack-plan-ceo-review` application was not durably recorded | current user request; this plan | Named-skill evidence gap | Low | supplementation | P1 | Implemented in this plan/task/spec/progress |
| CEO-003 | Hybrid P3 deferred status became stale after approved P3 remediation | P3 plan/task; commits `c22a961`, `c184e57` | Readers may think resolved GitOps/Vault/ESO items are still only planned | Medium | supplementation | P1 | Add current-state overlay |
| CEO-004 | Hybrid verification summaries still record root app count 17 from the pre-P3 state | P3 validation shows root app count 18 | Current-state confusion | Medium | supplementation | P1 | Add current-state verification note |
| CEO-005 | `workspace-harness-audit` does not explicitly require stale-deferral overlays after follow-up work changes status | `.claude/skills/workspace-harness-audit/skill.md` | Future plans can drift after follow-up commits | Low | improvement | P1 | Update skill |

### CEO P3 Current-State Overlay

This overlay does not rewrite the historical Hybrid Refresh finding. It records
the current state after the approved P3 remediation work.

| Former Hybrid P3 item | Current state | Evidence | Remaining risk |
| --- | --- | --- | --- |
| ESO DNS/API egress | resolved in repo desired state | `gitops/platform/network-policies/external-secrets-egress-to-vault.yaml`; P3 plan/task; commit `c22a961` | Live ESO behavior still unverified because local cluster API was unavailable |
| Vault `platform/notifications` policy | resolved in repo desired state | `infrastructure/vault/policies/eso-read.hcl`; P3 plan/task; commit `c22a961` | Vault KV values and live ESO readiness not inspected |
| AppProject `ExternalSecret` permission and sample key format | resolved in repo desired state | `gitops/clusters/local/appproject-apps.yaml`; `examples/sample-app/external-secret.yaml`; commit `c22a961` | Live ArgoCD sync not verified |
| `gitops/clusters/local` bootstrap CR ownership | resolved in repo desired state | `gitops/apps/root/platform-cluster-config-app.yaml`; `gitops/clusters/local/kustomization.yaml`; commit `c22a961` | Existing clusters may require bootstrap handoff |
| GitHub Actions SHA pinning and ruleset policy | still deferred | `.github/zizmor.yml`; workflow review rows | Requires CI governance decision |
| `.claude/settings.local.json` precedence | still deferred | local settings review rows | Requires provider precedence simulation or owner decision |
| ignored graphify cleanup | still deferred | `.agents/rules/graphify.md`; `.agents/workflows/graphify.md` | Requires local owner decision |
| live k3d/ArgoCD/Vault/ESO validation | attempted and current-state failed | P3 task runtime check results | Start `k3d-hyhome`, then rerun read-only metadata checks |

### CEO Implementation Plan

| Action type | Target | Change | Required skill | Linked task | Verification | Rollback |
| --- | --- | --- | --- | --- | --- | --- |
| supplementation | this plan | Add CEO review coverage ledger, findings, and current-state overlay | `gstack-plan-ceo-review`; `workspace-harness-audit`; `documentation-writer` | T-027, T-028 | repo quality gate; targeted `rg` | Revert this section |
| supplementation | linked task | Add CEO review task rows and verification summary | `gstack-plan-ceo-review`; `documentation-writer` | T-027, T-030 | repo quality gate | Revert task additions |
| supplementation | Spec 006 | Add CEO review acceptance criterion | `gstack-plan-ceo-review`; `documentation-writer` | T-027 | repo quality gate | Revert criterion |
| improvement | `.claude/skills/workspace-harness-audit/skill.md` | Require current-state overlays when follow-up work changes prior deferred status | `gstack-plan-ceo-review`; `skill-improver`; `agent-md-refactor` | T-029 | repo quality gate | Revert skill wording |
| memory | `docs/00.agent-governance/memory/progress.md` | Record CEO review result and remaining risks | `gstack-plan-ceo-review`; `workspace-harness-audit` | T-029 | repo quality gate | Revert progress entry |

### CEO Deferred Items

| Target | Deferral reason | Required pre-check | Follow-up work |
| --- | --- | --- | --- |
| Live ArgoCD/Vault/ESO readiness proof | Local cluster API refused connection during approved P3 read-only checks | Start `k3d-hyhome`; wait for ArgoCD reconciliation | Rerun metadata-only checks from the P3 task |
| GitHub Actions SHA pinning and ruleset policy | Remote governance decision, not a repo-static fix | Inspect current branch protection/rulesets and CI requirements | Separate CI supply-chain task |
| `.claude/settings.local.json` precedence hardening | Local provider behavior can change runtime permissions | Non-destructive precedence simulation or provider documentation review | Separate local-runtime hardening task |
| graphify local cleanup | Ignored local files may be user-specific | Owner decision whether to delete locally or promote to governed docs | Separate local cleanup task |

### CEO Verification Results

| Command or method | Result | Record location |
| --- | --- | --- |
| `test -f /home/hy/.agents/skills/brainstorming/SKILL.md` | PASS | this section |
| `test -f /home/hy/.agents/skills/gstack/plan-ceo-review/SKILL.md` | PASS | this section |
| `git diff origin/main --stat` before edits | clean | system audit |
| `git stash list` | no stashes | system audit |
| current root app count after P3 | PASS; root app manifest count is 18 | `bash scripts/validate-gitops-structure.sh` |
| targeted CEO evidence search | PASS | linked task CEO summary |

## Executing-Plans Follow-up - 2026-05-24

### Executing-Plans Scope

`/home/hy/.codex/plugins/cache/claude-plugins-official/superpowers/5.1.0/skills/executing-plans/SKILL.md`
was applied to execute the CEO review coverage plan. The plan being executed is
the `CEO Review Follow-up - 2026-05-24` section above, not a new platform
feature plan.

### Executing-Plans Critical Review

| Review item | Result | Action |
| --- | --- | --- |
| Written plan exists | PASS; CEO Review Follow-up section exists | Execute that section's implementation plan |
| Concerns before execution | One concern: executing-plans expects branch/worktree finishing, while this repository had an existing task-unit commit flow on `main` | Record branch/finish boundary instead of pretending a feature branch exists |
| Blockers | none | Proceed |
| Subagent note | Subagents are useful for fresh reviews, but this was a current-state documentation execution delta | No new subagent run |

### Executing-Plans Task Execution

| Task | Plan reference | Status | Evidence |
| --- | --- | --- | --- |
| Load plan | CEO Review Follow-up | done | plan section inspected |
| Review critically | CEO Mode and Alternatives; CEO Findings | done | missing executing-plans evidence identified |
| Execute task evidence updates | linked task and Spec 006 | done | T-031 through T-034; VAL-SPC-006-011 |
| Execute reusable guardrail update | `workspace-harness-audit` | done | skill now requires named execution-skill boundary evidence |
| Run verification | Executing-Plans Verification Results | done | repo quality, wiki, GitOps, targeted search, diff check |
| Finish boundary | normal repo on `main`, no separate worktree | done | `git rev-parse --git-dir` equals `git rev-parse --git-common-dir` |

### Executing-Plans Implementation Plan

| Action type | Target | Change | Required skill | Linked task | Verification | Rollback |
| --- | --- | --- | --- | --- | --- | --- |
| supplementation | this plan | Add executing-plans review, execution, verification, and finish boundary | `superpowers:executing-plans`; `documentation-writer` | T-031, T-032 | repo quality gate; targeted `rg` | Revert this section |
| supplementation | linked task | Add executing-plans task rows and verification summary | `superpowers:executing-plans`; `documentation-writer` | T-031, T-034 | repo quality gate | Revert task additions |
| supplementation | Spec 006 | Add executing-plans acceptance criterion | `superpowers:executing-plans`; `documentation-writer` | T-031 | repo quality gate | Revert criterion |
| improvement | `.claude/skills/workspace-harness-audit/skill.md` | Require named execution-skill evidence when a prompt requests it | `superpowers:executing-plans`; `skill-improver`; `agent-md-refactor` | T-033 | repo quality gate | Revert skill wording |
| memory | `docs/00.agent-governance/memory/progress.md` | Record executing-plans completion and branch boundary | `superpowers:executing-plans`; `workspace-harness-audit` | T-033 | repo quality gate | Revert progress entry |

### Executing-Plans Verification Results

| Command or method | Result | Record location |
| --- | --- | --- |
| `test -f .../executing-plans/SKILL.md` | PASS | this section |
| `test -f .../finishing-a-development-branch/SKILL.md` | PASS | this section |
| `test -f .../using-git-worktrees/SKILL.md` | PASS | this section |
| `test -f .../writing-plans/SKILL.md` | PASS | this section |
| `git rev-parse --abbrev-ref HEAD` | `main` | finish boundary |
| `git rev-parse --git-dir` and `git rev-parse --git-common-dir` | both `.git`; normal repo, not a linked worktree | finish boundary |
| targeted executing-plans evidence search | PASS | linked task |

## Skill Quality Follow-up - 2026-05-24

### Skill Quality Scope

The named skill creation/improvement lenses were applied to the existing
repo-local workflow skill `.claude/skills/workspace-harness-audit/skill.md`.
This was an update to an existing skill, not a new skill creation pass.

### Skill Lens Application

| Skill | Application result | Evidence | Decision |
| --- | --- | --- | --- |
| `/home/hy/.codex/skills/.system/skill-creator/SKILL.md` | applied | frontmatter, concise body, progressive disclosure, line-count guidance | Keep one `skill.md` file because repo-local Claude skills use lowercase paths |
| `/home/hy/gstack/.agents/skills/gstack-skillify/SKILL.md` | reviewed, not applicable | scrape codification workflow is browser-specific | Do not create browser script/test/fixture artifacts |
| `/home/hy/.agents/skills/skill-developer/SKILL.md` | applied | 500-line rule, trigger clarity, `When NOT to Use` guidance | Add `When NOT to Use` section |
| `/home/hy/.codex/trailofbits-skills/plugins/skill-improver/skills/skill-improver/SKILL.md` | applied manually | critical/major checklist; automated `skill-reviewer` not in repo harness | Fix missing `When NOT to Use`; keep manual review evidence |

### Skill Quality Findings

| ID | Finding | Evidence path | Impact | Risk | Action type | Priority | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SKILL-Q-001 | `workspace-harness-audit` had `When to Use` but no `When NOT to Use` section | `.claude/skills/workspace-harness-audit/skill.md` | Trigger boundary less precise | Low | improvement | P1 | Added section |
| SKILL-Q-002 | Current prompt named exact skill-maker paths not all present in the path-level ledger | this plan | Replayability weaker | Low | supplementation | P1 | Added exact path rows |
| SKILL-Q-003 | `skillify` could be misapplied to non-scrape workflow work | `gstack-skillify` skill body | Would create irrelevant artifacts | Low | deferral | P3 | Recorded as not applicable |
| SKILL-Q-004 | Automated `skill-reviewer` loop was unavailable in the current repo harness | `skill-improver` prerequisites | Cannot prove plugin-dev review loop | Medium | deferral | P3 | Manual critical/major review used |

### Skill Quality Implementation Plan

| Action type | Target | Change | Required skill | Linked task | Verification | Rollback |
| --- | --- | --- | --- | --- | --- | --- |
| improvement | `.claude/skills/workspace-harness-audit/skill.md` | Add `When NOT to Use` boundaries | `skill-creator`; `skill-developer`; `skill-improver` | T-035, T-036 | line count; repo quality gate | Revert section |
| supplementation | this plan | Record skill lens application, findings, and exact paths | `skill-creator`; `skillify`; `skill-developer`; `skill-improver` | T-035, T-037 | targeted `rg`; repo quality gate | Revert this section |
| supplementation | linked task | Add skill quality task rows and verification summary | `skill-creator`; `skill-developer`; `skill-improver` | T-035, T-038 | repo quality gate | Revert task additions |
| supplementation | Spec 006 | Add skill quality acceptance criterion | `skill-creator`; `skill-developer`; `skill-improver` | T-035 | repo quality gate | Revert criterion |
| memory | `docs/00.agent-governance/memory/progress.md` | Record skill quality follow-up and unavailable automated review loop | `skill-creator`; `skill-improver` | T-037 | repo quality gate | Revert progress entry |

### Skill Quality Deferred Items

| Target | Deferral reason | Required pre-check | Follow-up work |
| --- | --- | --- | --- |
| `skillify` browser-skill artifacts | No successful browser scrape flow exists in this task | Identify a real repeated scrape workflow | Run `skillify` only for browser automation codification |
| automated `skill-reviewer` loop | `plugin-dev:skill-reviewer` is not part of this repo harness | Enable plugin-dev or expose the reviewer agent | Rerun `skill-improver` automated loop if available |
| `agents/openai.yaml` metadata | Repo-local `.claude/skills/*/skill.md` roster does not use Codex skill package layout | Decide whether to package this as a Codex skill | Generate metadata only if promoted outside `.claude/skills` |

### Skill Quality Verification Results

| Command or method | Result | Record location |
| --- | --- | --- |
| `wc -l .claude/skills/workspace-harness-audit/skill.md` | PASS; 92 lines, under 500 lines | linked task |
| `rg -n "When NOT to Use" .claude/skills/workspace-harness-audit/skill.md` | PASS | linked task |
| `python3 .../quick_validate.py .claude/skills/workspace-harness-audit` | EXPECTED FAIL; repo uses lowercase `skill.md`, validator expects `SKILL.md` | linked task |
| targeted skill quality evidence search | PASS | linked task |
| `bash scripts/validate-repo-quality-gates.sh .` | PASS | linked task |
| `bash scripts/generate-llm-wiki-index.sh --check` | PASS | linked task |
| `git diff --check` | PASS | linked task |

## Skill Creation Follow-up - 2026-05-24

### Repeated Workflow Review

| Source | Repeated workflow found | Evidence | Skill decision |
| --- | --- | --- | --- |
| Codex memory | Audit docs stages before editing, narrow to concrete defects, fix in place, validate with repo gates and wiki index | `/home/hy/.codex/memories/MEMORY.md`; `/home/hy/.codex/memories/skills/docs-stage-conformance/SKILL.md` | Create repo-local Skill so the workflow is available inside this checkout |
| Current task evidence | Workspace harness work repeatedly recorded docs template, README/index, heading, link, and progress-ledger validation boundaries | this plan; linked task; `memory/progress.md` | Split narrow docs conformance from broad `workspace-harness-audit` |
| Harness catalog | New local skills must be registered in the catalog in the same change set | `docs/00.agent-governance/harness-catalog.md` | Add Skill row and task-to-skill routing |
| `skillify` | Skill is browser scrape codification and writes gstack runtime state | `/home/hy/gstack/.agents/skills/gstack-skillify/SKILL.md` | Do not create browser artifacts; record not applicable |

### Created Skill Design

| Field | Decision |
| --- | --- |
| Skill path | `.claude/skills/docs-stage-conformance/skill.md` |
| Skill type | workflow |
| Trigger surface | authored docs cleanup, template conformance, README/index drift, duplicate-H1 cleanup, link drift, docs validation evidence |
| Explicit non-trigger | full workspace audit, new feature design/planning, live runtime validation, semantic rewrites |
| Source basis | current task evidence plus Codex memory repeated workflow |
| Packaging boundary | repo-local lowercase `skill.md`; no Codex package `SKILL.md` or `agents/openai.yaml` metadata |

### Skill Creation Implementation Plan

| Action type | Target | Change | Required skill | Linked task | Verification | Rollback |
| --- | --- | --- | --- | --- | --- | --- |
| addition | `.claude/skills/docs-stage-conformance/skill.md` | Add repo-local workflow Skill for repeated docs-stage conformance work | `skill-creator`; `skill-developer`; `skill-improver` | T-039, T-040 | line count; targeted `rg`; repo quality gate | Delete new Skill file |
| supplementation | `docs/00.agent-governance/harness-catalog.md` | Register the Skill and route docs writing tasks to routing vs conformance workflows | `skill-creator`; `agent-md-refactor` | T-041 | repo quality gate; targeted `rg` | Revert catalog rows |
| improvement | `.claude/skills/workspace-harness-audit/skill.md` | Point narrow docs conformance work to the new Skill | `skill-improver` | T-041 | targeted `rg`; repo quality gate | Revert wording |
| supplementation | Spec 006, linked task, this plan, progress ledger | Record repeated-workflow review, creation decision, verification, and boundaries | `skill-creator`; `skillify`; `skill-developer`; `skill-improver` | T-039, T-042 | repo quality gate; wiki check; `git diff --check` | Revert evidence sections |

### Skill Creation Deferred Items

| Target | Deferral reason | Required pre-check | Follow-up work |
| --- | --- | --- | --- |
| Browser-skill artifact from `skillify` | No successful `/scrape` flow exists in this task | Identify a repeated browser scrape workflow | Run `skillify` only for browser automation codification |
| Codex package metadata | Repo-local `.claude/skills/*/skill.md` roster uses lowercase Skill files without `agents/openai.yaml` | Decide to promote repo skill outside Claude runtime | Generate package metadata only after that promotion decision |
| Automated `plugin-dev:skill-reviewer` review | Reviewer agent is not exposed in the active harness | Enable plugin-dev reviewer surface | Rerun automated skill review; current pass uses manual critical/major checklist |

### Skill Creation Verification Results

| Command or method | Result | Record location |
| --- | --- | --- |
| `wc -l .claude/skills/docs-stage-conformance/skill.md` | PASS; 77 lines, under 500 lines | linked task |
| targeted Skill creation evidence search | PASS | linked task |
| `bash scripts/validate-repo-quality-gates.sh .` | PASS | linked task |
| `bash scripts/generate-llm-wiki-index.sh --check` | PASS | linked task |
| `git diff --check` | PASS | linked task |

## Multi-Area Workspace Improvement Overlay - 2026-05-25

### Overlay Scope

This overlay implements the human-approved multi-area design without creating a
parallel documentation tree. It updates the existing Spec 006, this plan, the
linked task, README indexes, script command contracts, and progress ledger.

| Priority | Scope | Decision |
| --- | --- | --- |
| P1 | README/status currentness and revalidation ledger | Implemented in place |
| P2 | Secret scanner and hook manifest coverage | Implemented with static verification |
| P3 | live runtime, secret values, CI rulesets, AppProject/Vault/K8s semantic changes | Precheck-only and deferred |

### Overlay Coverage Ledger

| Lane | Investigation status | Key result | Evidence path | Next action |
| --- | --- | --- | --- | --- |
| Documentation lifecycle | complete | Spec/Plan/Task README status drift corrected; legacy docs retained | `docs/03.specs/README.md`; `docs/04.execution/*/README.md` | Keep currentness rows tied to execution evidence |
| Scripts / QA | complete | `check-secret-handling.sh` now detects quoted literal sensitive values and redacts findings | `scripts/check-secret-handling.sh`; `/tmp` negative fixture | Keep fixture pattern in future validator changes |
| GitOps / Infrastructure | partial | Static gates remain passing; no semantic resource changes in this pass | `gitops/`; `infrastructure/` | Use separate approved plan for semantic changes |
| Environment | complete | `.env.example` and `.env` remain key-name-only checked; values uninspected | `.env.example`; `.env` | Human-only value review if required |
| CI/CD | partial | Workflow structure unchanged; policy drift remains deferred | `.github/`; `.pre-commit-config.yaml` | Separate CI governance task for rulesets/SHA pinning |
| Agent governance | partial | Gateway remains thin; hook coverage comments clarify recursive Bash `case` behavior | `.claude/hooks/*.sh` | Keep repeated routing in catalog/skills |
| Cleanup | partial | No deletion performed; legacy/local candidates remain reference-check deferred | `.agents/`; `.claude/*.local.md`; legacy docs | Owner decision before delete/consolidate |

### Overlay Gap Delta

| Area | Gap | Evidence path | Impact | Risk | Action type | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| Documentation | P3 plan/task README rows were stale after repo desired-state work completed | `docs/04.execution/plans/README.md`; `docs/04.execution/tasks/README.md` | Reader may treat completed repo changes as still active | Low | improvement | P1 |
| Documentation | Spec 006 README currentness row did not distinguish resolved repo desired-state work from still-deferred live/policy checks | `docs/03.specs/README.md` | Current-state ambiguity | Low | supplementation | P1 |
| Scripts / QA | Plaintext secret scanner missed quoted literal values for sensitive keys | `scripts/check-secret-handling.sh` | Quoted secret literals could pass static scan | Medium | improvement | P2 |
| Hooks | Manifest hook coverage could be misread as shallow because recursive behavior depends on Bash `case` semantics | `.claude/hooks/post-validate.sh`; `.claude/hooks/lifecycle-guard.sh` | Maintainer confusion and future drift | Low | supplementation | P2 |
| CI/CD | `workflow-security` naming/pinning/ruleset policy remains outside repo-static implementation | `.github/`; `.pre-commit-config.yaml` | Supply-chain policy ambiguity | Medium | deferral | P3 |
| Runtime | Live cluster and secret value checks remain unavailable by design | P3 task records; `.env` | Runtime health unknown | Medium | deferral | P3 |

### Overlay Implementation Plan

| Action type | Target | Change | Linked task | Verification | Rollback |
| --- | --- | --- | --- | --- | --- |
| improvement | README indexes | Mark P3 repo desired-state work Done and preserve live follow-up boundary | T-044 | repo quality gate; wiki check | Revert README rows |
| supplementation | Spec 006 and this plan | Add 2026-05-25 overlay scope, gap delta, and P3 precheck-only boundary | T-045 | repo quality gate | Revert overlay sections |
| improvement | `scripts/check-secret-handling.sh` | Replace grep-only patterns with YAML-aware line scanner that flags quoted literals and redacts values | T-046 | secret scan; negative fixture; shell syntax | Revert script change |
| supplementation | hook scripts | Document recursive manifest matching semantics without changing hook behavior | T-047 | shell syntax; repo quality gate | Revert comments |
| supplementation | progress ledger | Record multi-area overlay results and deferred P3 boundaries | T-048 | repo quality gate | Revert progress entry |

### Overlay Deletion, Consolidation, and Deferral Delta

| Target | Type | Reason | Reference check | Recommended action |
| --- | --- | --- | --- | --- |
| `.agents/skills/**` | consolidation candidate | Local skill surfaces may duplicate governed `.claude/skills` routing | References not exhaustively cleared | Defer owner-reviewed consolidation |
| `.claude/*.local.md` / local settings surfaces | deferral | Local provider precedence and permissions are user-specific | Shared docs cannot prove local precedence | Defer provider precedence review |
| Legacy/superseded docs | deletion candidate | Some historical records have current replacements | References remain and history is useful | Retain; do not bulk delete |
| CI `workflow-security` / SHA pinning policy | deferral | Requires governance decision and remote ruleset context | Worktree-only check is insufficient | Separate CI supply-chain task |
| AppProject/Vault/ESO/NetworkPolicy semantics | deferral | Kubernetes and secret-access semantic changes need a scoped plan | Static gates cannot prove live effect | Separate approved GitOps/runtime plan |

### Overlay Verification Results

| Command or method | Result | Record location |
| --- | --- | --- |
| `bash -n scripts/check-secret-handling.sh .claude/hooks/post-validate.sh .claude/hooks/lifecycle-guard.sh` | PASS | current overlay |
| `bash scripts/check-secret-handling.sh .` | PASS | current overlay |
| temporary `/tmp` quoted-sensitive-value negative fixture | PASS; quoted literal sensitive value failed with redacted finding and quoted placeholder stayed clean | current overlay |
| `.env.example` and `.env` key-name-only comparison | PASS; key names match without printing values | current overlay |
| full verification bundle | PASS after final rerun; optional `kube-linter` remains skipped by `validate-k8s-manifests.sh` because it is not installed locally | linked task overlay summary |

### Overlay Checklist Gate

| Checklist item | Status | Evidence |
| --- | --- | --- |
| Is the goal clear in one sentence? | pass | Human-approved multi-area design implemented as P1/P2 with P3 precheck-only |
| Are related files, logs, issues, or reproduction steps provided or discovered? | pass | Existing 006 SDD artifacts, README indexes, scripts, hooks, and validation commands inspected |
| Are modification scope and forbidden scope separated? | pass | Overlay Scope and Non-goals preserve no live mutation, no secret value inspection, no bulk deletion |
| Are existing patterns, compatibility, and dependency rules stated? | pass | Existing SDD artifacts updated in place; gateway remains thin |
| Are test, lint, and type-check commands identified? | pass | Overlay Verification Results and linked task summary |
| Are completion criteria measurable? | pass | VAL-SPC-006-014 and T-044 through T-048 |
| Are recurring instructions moved or planned for `AGENTS.md` or Skills? | pass | `AGENTS.md` remains thin; routing stays in catalog/skills |

## P0 Mandatory Workstream Revalidation - 2026-05-25

### P0 Mandatory Workstream Status

| P0 ID | Workstream | Inventory status | Gap status | Plan status | Implementation status | Verification status | Evidence path |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P0-1 | Environment, system, and rules for the workspace purpose | complete | gaps recorded | planned | P1/P2 docs and validator fixes implemented; high-risk runtime deferred | static verification run | this section; `AGENTS.md`; `.claude/CLAUDE.md`; `scripts/` |
| P0-2 | `docs/` lifecycle across stages 01/02/03/04/05/90 | complete | gaps recorded | planned | README currentness fixed for 006 Plan/Task; legacy docs retained | repo quality and wiki checks | `docs/03.specs/`; `docs/04.execution/`; `docs/90.references/` |
| P0-3 | `scripts/` cleanup/classification | complete | gaps recorded | planned | `validate-gitops-structure.sh` now rejects unexpected args; no deletion | shell syntax and GitOps validator checks | `scripts/README.md`; `scripts/validate-gitops-structure.sh` |
| P0-4 | `gitops/` infrastructure | complete | gaps recorded | planned | semantic changes deferred | GitOps structure and manifest checks | `gitops/` |
| P0-5 | `infrastructure/` reproducibility/contracts | complete | gaps recorded | planned | semantic changes deferred | static contract tests | `infrastructure/` |
| P0-6 | `traefik/` routing and local platform alignment | complete | gaps recorded | planned | semantic changes deferred | manifest and static review | `traefik/` |
| P0-7 | `examples/` operational/example separation | complete | gaps recorded | planned | cleanup candidates deferred | repo-static review | `examples/` |
| P0-8 | `.env.example` and `.env` role/key consistency | complete | gaps recorded | planned | no value inspection; reserved-key review deferred | key-name-only comparison | `.env.example`; `.env` |

### Fresh Subagent Review Results

| Role | Status | Key findings | Unknown |
| --- | --- | --- | --- |
| Documentation Lifecycle Reviewer | complete | 006 Spec/Plan/Task chain remains connected; Plan/Task README 006 rows under-reported the 2026-05-25 overlay; preserved Hybrid raw tables need historical framing | live runtime, secret freshness, full-repo link proof |
| Agent Governance Reviewer | complete | Gateway/provider shims stay thin; Codex provider resolution was implicit; broad governance priority changes should be deferred | local ignored provider files and remote permission state |
| Scripts Reviewer | complete | Scripts are reusable, not deletion-ready; GitOps validator README says no args but script accepted extras | current pass/fail until verification rerun |
| GitOps Infrastructure Reviewer | complete | Static desired-state structure is present; AppProject, Vault/ESO, Istio, Traefik, examples, and cloud semantics need separate prechecks | live ArgoCD, Vault, ESO, k3d, external service reachability |
| Environment Quality Reviewer | complete | `.env.example` and `.env` key names match; `APP_STAGE` appears reserved/unused; CI structure is coherent, optional supply-chain tools are not guaranteed | secret values, GitHub rulesets, optional tool availability |

### P0 Coverage Ledger

| Area | Target path | Investigation status | Representative files read | Gap count | Deletion/deferral candidate count | Unknown items | Next action |
| --- | --- | --- | --- | ---: | ---: | --- | --- |
| Documentation governance | `docs/00.agent-governance/` | complete | `README.md`; provider/rule files; `memory/progress.md` | 1 | 2 | local ignored files | Clarify Codex provider resolution; defer priority rewrites |
| Requirements | `docs/01.requirements/` | complete | `README.md`; stage inventory | 0 | 0 | none from static pass | Keep linked through Spec 006 and ARD references |
| Architecture | `docs/02.architecture/` | complete | `README.md`; ARD/ADR indexes | 0 | 1 | live runtime fitness | Keep current-contract notes separate from historical docs |
| Specs | `docs/03.specs/` | complete | `README.md`; `006-workspace-harness-gap-analysis/spec.md` | 1 | 0 | none | Add VAL-SPC-006-015 |
| Execution plans | `docs/04.execution/plans/` | complete | `README.md`; 006 plan | 3 | 5 | live/runtime verification | Update 006 row; record P0 overlay |
| Execution tasks | `docs/04.execution/tasks/` | complete | `README.md`; 006 task | 1 | 0 | none | Add T-049+ rows and verification evidence |
| Operations | `docs/05.operations/` | complete | `README.md`; runbook/policy indexes | 0 | 1 | live operator proof | Defer runtime proof |
| References/templates | `docs/90.references/`; `docs/99.templates/` | complete | README and template indexes | 0 | 1 | full link graph | No template change |
| Scripts | `scripts/` | complete | `README.md`; validator scripts | 3 | 1 | optional tool parity | Reject unexpected GitOps validator args; restore executable mode; defer scanner expansion |
| GitOps | `gitops/` | complete | root app and app manifests | 3 | 3 | live ArgoCD reconciliation | Keep semantic changes P3 |
| Infrastructure | `infrastructure/` | complete | tests and k3d contracts | 2 | 2 | live k3d/DB/Valkey | Keep semantic changes P3 |
| Traefik | `traefik/` | complete | README/manifests | 1 | 1 | external Traefik parity | Defer routing semantic changes |
| Examples | `examples/` | complete | README/examples manifests | 2 | 3 | example runtime freshness | Defer consolidation |
| Environment | `.env.example`; `.env` | complete | key-name-only comparison | 1 | 1 | values intentionally unknown | Keep values human-only |
| QA and CI/CD | `.github/`; `.pre-commit-config.yaml` | complete | workflow and pre-commit config | 2 | 3 | rulesets/SHA policy | Defer CI policy changes |
| Agent runtime | `AGENTS.md`; `CLAUDE.md`; `.claude/`; `.codex/`; `.agents/` | complete | gateway, provider, hook, catalog files | 2 | 4 | ignored local precedence | Clarify Codex provider resolution; defer consolidation |

### P0 Integrated Gap Analysis

#### Summary

- Overall status: repo-static P0 revalidation is complete; live runtime and
  policy-owner checks remain deferred.
- Largest Gap: static repository evidence cannot prove live k3d, ArgoCD, Vault,
  ESO, PostgreSQL, Valkey, Traefik, or NetworkPolicy behavior.
- Immediately implementable: README currentness drift, historical reviewer
  framing, Codex provider resolution, and GitOps validator argument contract.
- Needs deferral: Kubernetes semantics, ArgoCD App-of-Apps structure, CI
  policy/rulesets, secret values, bulk deletion, and ignored local files.
- Unknown areas: live services, secret value freshness, remote GitHub rulesets,
  optional security tool output, and user-local provider precedence.

#### Gaps by Area

| Area | Gap | Evidence path | Impact | Risk | Action type | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| Documentation | 006 Plan/Task README rows lagged the P0 overlay date and scope | `docs/04.execution/plans/README.md`; `docs/04.execution/tasks/README.md` | Readers may miss current evidence | Low | improvement | P1 |
| Documentation | Historical Hybrid reviewer tables could be read as current | this plan | Stale claims can conflict with later overlays | Low | supplementation | P1 |
| Specs/tasks | P0 revalidation lacked dedicated acceptance and T-049+ linkage | Spec 006; linked task | Traceability gap | Low | supplementation | P1 |
| Scripts | GitOps validator accepted unexpected arguments despite no-arg contract | `scripts/README.md`; `scripts/validate-gitops-structure.sh` | Accidental path argument is ignored | Medium | improvement | P2 |
| Scripts/QA | One infrastructure verification helper lacked executable mode | `infrastructure/tests/verify-ingress-tls.sh` | Direct script execution can fail even though `bash script.sh` works | Low | improvement | P2 |
| Scripts/security | Secret scanner alias/field expansion needs fixtures before change | `scripts/check-secret-handling.sh` | Possible false negatives | Medium | deferral | P3 |
| Governance | Codex provider resolution was implicit rather than explicit | `docs/00.agent-governance/providers/agents-md.md` | Provider ambiguity | Low | supplementation | P1 |
| GitOps/infra | AppProject, Vault/ESO, Istio, Traefik, and example semantics need owner review | `gitops/`; `infrastructure/`; `traefik/`; `examples/` | Live behavior risk | High | deferral | P3 |
| Environment | `APP_STAGE` appears reserved/unused in env key set | `.env.example`; `.env` | Potential confusion | Low | deferral | P3 |
| CI/CD | Optional supply-chain tooling and SHA/ruleset policy are not enforced by this pass | `.github/`; `.pre-commit-config.yaml` | Policy ambiguity | Medium | deferral | P3 |

#### Conflicts/Duplicates

| Target | Description | Impact | Recommended action |
| --- | --- | --- | --- |
| Hybrid reviewer evidence | Preserved 2026-05-24 tables contain claims superseded by later overlays | Reader confusion | Keep as historical evidence with explicit note |
| `status: complete` vs index `Done` | P3 plan/task and README use equivalent but different status vocabularies | Minor metadata drift | Defer vocabulary normalization to a docs metadata pass |
| `.agents/skills/**` vs `.claude/skills/**` | Multiple skill surfaces exist | Routing confusion if treated as equal | Keep `.claude/skills/**` as runtime source; defer consolidation |

#### Deletion Candidates

| Target | Type | Candidate reason | Reference check | Impact | Recommended action |
| --- | --- | --- | --- | --- | --- |
| Legacy/superseded docs | historical reference | Current contracts now live in later specs/plans | References remain | Deleting would remove audit history | Retain |
| `.agents/skills/**` | consolidation candidate | May duplicate governed `.claude/skills/**` routing | Not exhaustively clear | Could break local workflows | Defer owner-reviewed consolidation |
| Example cloud secret/Terraform material | cleanup candidate | Example-only and policy-sensitive | References remain in examples/docs | Could remove useful reference | Defer with scoped example policy task |

#### Deferred Items

| Target | Deferral reason | Required pre-check | Follow-up work |
| --- | --- | --- | --- |
| k3d/ArgoCD/Vault/ESO/PostgreSQL/Valkey live state | Live access and mutation are outside this pass | Human approval and read-only command list | Run live metadata proof and record unavailable services |
| AppProject/Vault/ESO/NetworkPolicy semantics | High-risk Kubernetes and secret-access changes | Dedicated GitOps/runtime plan and rollback | Implement repository desired-state changes only after approval |
| CI rulesets/SHA pinning/workflow-security policy | Remote and supply-chain governance decision needed | Inspect rulesets and ownership policy | Create CI supply-chain plan |
| `.env` values | Secret value inspection forbidden | Human-only value review | Compare values outside agent output if needed |
| Bulk deletion or consolidation | References not exhaustively cleared | Link/reference search and owner approval | Delete only individual proven-unused files |

#### Unknown

| Item | Reason unknown | Follow-up check |
| --- | --- | --- |
| Live cluster health | No live validation approved | Read-only k3d/kubectl/argocd status plan |
| Secret value freshness | Values intentionally not inspected | Human-owned value review |
| GitHub branch protection/rulesets | Remote policy not queried in this pass | `gh`/repository settings review with approval |
| Optional tools | Tool availability is environment-specific | Record command presence during verification |

### P0 Implementation Plan

#### P1 Low risk / Immediate implementation

| Action type | Target | Change | Linked task | Verification | Rollback |
| --- | --- | --- | --- | --- | --- |
| improvement | Plan/Task README indexes | Update 006 rows to 2026-05-25 P0 overlay scope | T-052 | repo quality gate; wiki check | Revert README rows |
| supplementation | Spec 006 and linked task/plan | Add VAL-SPC-006-015 and T-049+ P0 evidence | T-049, T-050, T-051, T-057 | repo quality gate; targeted evidence search | Revert overlay sections |
| supplementation | Historical Hybrid section | Add point-in-time evidence note | T-053 | repo quality gate | Revert note |
| supplementation | `providers/agents-md.md` | Clarify Codex provider resolution without adding a new file | T-055 | repo quality gate; targeted evidence search | Revert section |
| memory | `memory/progress.md` | Record P0 revalidation and deferred boundaries | T-057 | repo quality gate | Revert progress entry |

#### P2 Medium risk / Limited implementation

| Action type | Target | Change | Linked task | Verification | Rollback |
| --- | --- | --- | --- | --- | --- |
| improvement | `scripts/validate-gitops-structure.sh` | Reject unexpected arguments with usage and exit 2 | T-054 | shell syntax; positive and negative validator checks | Revert argument check |
| improvement | `infrastructure/tests/verify-ingress-tls.sh` | Restore executable mode for the verification helper | T-056 | script executability check; shell syntax | `chmod -x infrastructure/tests/verify-ingress-tls.sh` |

#### P3 High risk / Deferred

| Action type | Target | Deferral reason | Pre-check | Follow-up work |
| --- | --- | --- | --- | --- |
| deferral | live platform validation | Requires live services and approval | Read-only command list and owner approval | Validate k3d, ArgoCD, Vault, ESO, PostgreSQL, Valkey |
| deferral | Kubernetes/GitOps semantic changes | Could change live desired state | Dedicated plan, rollback, static diff review | Update AppProject/Vault/ESO/NetworkPolicy only after approval |
| deferral | CI policy/rulesets/SHA pinning | Remote policy and supply-chain decision | Ruleset inspection and CI ownership decision | Create CI policy hardening task |
| deferral | `.env` values and secret material | Secret value inspection prohibited | Human-only value review | Record key/value policy without exposing values |
| deletion candidate | legacy/local/example candidates | References not cleared and deletion would be nontrivial | Full reference check and owner approval | Delete or consolidate only one proven-safe item at a time |

### P0 Verification Results

| Command or method | Result | Record location |
| --- | --- | --- |
| `bash scripts/validate-repo-quality-gates.sh .` | PASS | this section; linked task |
| `bash scripts/generate-llm-wiki-index.sh --check` | PASS | this section; linked task |
| `bash scripts/validate-gitops-structure.sh` | PASS; root app manifest count 18 | this section; linked task |
| `bash scripts/validate-gitops-structure.sh unexpected` | PASS; expected exit 2 | this section; linked task |
| `bash scripts/validate-k8s-manifests.sh .` | PASS; YAML syntax for 103 files; script-local optional kube-linter path check skipped, separate kube-linter run passed | this section; linked task |
| `bash scripts/check-secret-handling.sh .` | PASS | this section; linked task |
| `bash infrastructure/tests/verify-contracts-static.sh` | PASS | this section; linked task |
| `find infrastructure scripts .claude/hooks -type f -name '*.sh' -exec bash -n {} +` | PASS | this section; linked task |
| Shell script executability check | PASS; 18 shell scripts executable after restoring `verify-ingress-tls.sh` | this section; linked task |
| JSON parse checks for `.claude/settings.json` and `.codex/hooks.json` | PASS | this section; linked task |
| `.env.example` vs `.env` key-name-only comparison | PASS; 18 key names match and no values printed | this section; linked task |
| CI workflow syntax/job dependency inspection | PASS; 5 workflows and 11 jobs inspected | this section; linked task |
| `git diff --check` | PASS | this section; linked task |
| Optional `actionlint` | PASS | this section; linked task |
| Optional `zizmor` | PASS; no findings, 16 suppressed | this section; linked task |
| Optional `kube-linter` | PASS; no lint errors found | this section; linked task |
| Optional `shellcheck` | PASS | this section; linked task |
| Optional `pre-commit run --all-files --hook-stage manual` | PARTIAL; configured hooks passed except `end-of-file-fixer`, which failed on read-only `.codex` mirror files; rerun with `SKIP=end-of-file-fixer` passed | this section; linked task |

### P0 Final Report

#### 1. Baseline Instruction Check

| Target | Checked | Key impact |
| --- | --- | --- |
| `AGENTS.md` | yes | Thin gateway, Korean user responses, GitOps-first, no plaintext secrets, no file proliferation |
| `CLAUDE.md`; `.claude/CLAUDE.md`; `GEMINI.md` | yes | Provider shims and runtime baseline checked; root shims do not replace shared governance |
| `CLAUDE.local.md` | yes | Missing; no local override applied |
| `docs/00.agent-governance/`; `.claude/`; `.codex/`; `.agents/` | yes | Runtime/policy docs inspected; Codex provider ambiguity clarified |
| `docs/99.templates/` | yes | No template changes made |

#### P0 Mandatory Workstream Status

| P0 ID | Workstream | Inventory | Gap | Plan | Implementation/Deferral | Verification | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P0-1 | Environment/system/rules | complete | recorded | planned | P1/P2 implemented; P3 deferred | PASS repo-static; live deferred | this section |
| P0-2 | Docs lifecycle | complete | recorded | planned | README/currentness fixed | PASS repo quality/wiki | docs stage READMEs |
| P0-3 | Scripts | complete | recorded | planned | no-arg validator guard and executable mode implemented | PASS syntax/executability/validator checks | `scripts/validate-gitops-structure.sh`; `infrastructure/tests/verify-ingress-tls.sh` |
| P0-4 | `gitops/` | complete | recorded | planned | semantic changes deferred | PASS static GitOps checks | `gitops/` |
| P0-5 | `infrastructure/` | complete | recorded | planned | semantic changes deferred | PASS static contracts | `infrastructure/` |
| P0-6 | `traefik/` | complete | recorded | planned | semantic changes deferred | PASS manifest/static checks | `traefik/` |
| P0-7 | `examples/` | complete | recorded | planned | cleanup deferred | PASS static review/gates | `examples/` |
| P0-8 | env files | complete | recorded | planned | key-only check; values deferred | PASS key-name-only comparison | `.env.example`; `.env` |

#### 2. Coverage Ledger Summary

| Area | Investigation status | Gap count | Deletion/deferral candidate count | Unknown |
| --- | --- | ---: | ---: | --- |
| Documentation lifecycle | complete | 3 | 5 | live runtime proof |
| Scripts/QA | complete | 3 | 2 | optional tool parity |
| GitOps/infrastructure/Traefik/examples | complete | 8 | 9 | live service behavior |
| Environment/CI/CD | complete | 3 | 4 | values and remote rulesets |
| Agent governance | complete | 2 | 4 | ignored local precedence |

#### 3. Subagent Summary

| Role | Status | Key findings | Unknown |
| --- | --- | --- | --- |
| Documentation Lifecycle Reviewer | complete | 006 chain connected; Plan/Task README drift; historical Hybrid rows need framing | live/runtime and full link proof |
| Agent Governance Reviewer | complete | Thin gateway intact; Codex provider path implicit | local ignored precedence |
| Scripts Reviewer | complete | No deletion-ready scripts; GitOps validator arg contract gap | final command rerun |
| GitOps Infrastructure Reviewer | complete | Static structure coherent; semantics require P3 plan | live ArgoCD/Vault/ESO |
| Environment Quality Reviewer | complete | Env key names match; optional tooling/policy deferred | secret values and rulesets |

#### 4. Integrated Gap Analysis Summary

| Area | Key Gap | Risk | Action | Priority |
| --- | --- | --- | --- | --- |
| Documentation | README/currentness and historical evidence framing | Low | improvement | P1 |
| Scripts | GitOps validator accepted unexpected args; one test helper lacked executable mode | Medium | improvement | P2 |
| Governance | Codex provider resolution implicit | Low | supplementation | P1 |
| GitOps/infra | Semantic/live behavior not proven by static checks | High | deferral | P3 |
| CI/env/secrets | Values/rulesets/pinning not inspected or changed | Medium | deferral | P3 |

#### 5. spec/task/plan Updates

| Document | Change | Linked work |
| --- | --- | --- |
| Spec 006 | Added VAL-SPC-006-015 | T-049+ |
| Linked Plan | Added P0 mandatory workstream revalidation overlay | T-049 through T-057 |
| Linked Task | Added P0 task rows, phase, evidence, and verification summary | T-049 through T-057 |
| Progress ledger | Added P0 revalidation memory entry | T-057 |

#### 6. Implementation Changes

| Target | Change | Reason | Linked task |
| --- | --- | --- | --- |
| Plan/Task README indexes | Updated 006 currentness rows to 2026-05-25 P0 overlay | Fresh drift finding | T-052 |
| `scripts/validate-gitops-structure.sh` | Added no-arg contract guard | README/script contract mismatch | T-054 |
| `infrastructure/tests/verify-ingress-tls.sh` | Restored executable bit | Script executability gate found one non-executable helper | T-056 |
| `providers/agents-md.md` | Clarified Codex provider resolution | Provider ambiguity | T-055 |
| linked plan/spec/task/progress | Recorded P0 status, gaps, implementation, deferrals, and verification | SDD traceability | T-049 through T-057 |

#### 7. Deletion Candidates and Deferred Items

| Target | Type | Reason | Reference check | Recommended action |
| --- | --- | --- | --- | --- |
| legacy docs | deletion candidate | superseded but historically useful | references remain | retain |
| `.agents/skills/**` | consolidation candidate | possible duplicate skill surface | not clear | defer owner-reviewed consolidation |
| AppProject/Vault/ESO/NetworkPolicy | deferral | high-risk desired-state semantics | static-only | separate approved plan |
| `.env` values | deferral | secret value inspection prohibited | key names only | human-only review |
| CI rulesets/SHA pinning | deferral | remote/policy context needed | local only | CI supply-chain task |

#### 8. Verification

| Command or method | Result | Record location |
| --- | --- | --- |
| Full requested verification bundle | PASS repo-static; live checks deferred | P0 Verification Results; linked task |
| Optional tooling availability | PASS except pre-commit `end-of-file-fixer` blocked by read-only `.codex`; alternate `SKIP=end-of-file-fixer` run passed | P0 Verification Results; linked task |

#### 9. Remaining Risks and Next Work

- Live platform behavior remains unknown until an approved read-only runtime
  validation pass runs.
- CI policy hardening and SHA pinning need a separate supply-chain decision.
- Deletion/consolidation candidates require reference checks and owner approval.

## Authored SSoT Large-Scale Improvement Overlay - 2026-05-25

### Intent and Boundary

This overlay implements the approved "large-scale improvement execution"
contract inside the existing 006 SDD chain. It does not create a parallel
Spec/Plan/Task tree. The human-facing `P0-01` through `P0-22` identifiers are
preserved as external traceability keys, while repo-local task IDs remain
`T-058` through `T-062`.

No Kubernetes, ArgoCD, Vault, CI ruleset, runtime, secret value, or live cluster
change is included. All changes are repo-static authored SSoT updates, evidence
normalization, and follow-up planning.

### P0-01 Through P0-22 Crosswalk

| External P0 ID | Requested workstream | Repo-local evidence | Current status | Gap / decision | Verification / follow-up |
| --- | --- | --- | --- | --- | --- |
| P0-01 | Workspace-purpose environment, system, and rules | `AGENTS.md`; `.claude/CLAUDE.md`; `docs/00.agent-governance/`; Spec 006 | partial | Rules exist; exact external P0 traceability was missing, now added here | repo quality gate; live/runtime rules remain deferred |
| P0-02 | `docs/` lifecycle environment, system, and rules | stage READMEs; `docs/99.templates/`; Spec/Plan/Task 006 | complete repo-static | Existing lifecycle is connected; overlay records current SSoT traceability | wiki index check; no new docs tree |
| P0-03 | `scripts/` deletion and consolidation review | `scripts/README.md`; validation scripts | complete repo-static | Scripts are reusable or operations-critical; no deletion-ready script found | shell syntax/executability; broad reference precheck remains required |
| P0-04 | One-off script removal when safe | `scripts/README.md`; this plan | deferred | No script met deletion criteria after reference and rollback constraints | deletion requires a dedicated task and reference-clearing evidence |
| P0-05 | Improve `gitops/` infrastructure | `gitops/`; GitOps validators; P3 remediation plan | partial | Static structure passes; EndpointSlice and semantic ownership remain P3 | GitOps/manifests checks; live ArgoCD proof deferred |
| P0-06 | Normalize `gitops/README.md` with template | `gitops/README.md`; `docs/99.templates/readme.template.md` | complete repo-static | README already participates in the template-shaped index contract | repo quality/wiki checks |
| P0-07 | Improve `infrastructure/` implementation | `infrastructure/`; `infrastructure/tests/verify-contracts-static.sh` | partial | Static contracts pass; live k3d/external-service proof remains separate | static contract test; live proof deferred |
| P0-08 | Normalize `infrastructure/README.md` with template | `infrastructure/README.md`; template | complete repo-static | README current enough for this overlay | repo quality/wiki checks |
| P0-09 | Improve `traefik/` implementation | `traefik/`; `traefik/README.md`; manifests | partial | Backend/fallback port wording drift needs a scoped docs fix | manifest validation; wording cleanup deferred |
| P0-10 | Normalize `traefik/README.md` with template | `traefik/README.md`; template | partial | Template shape is acceptable; route wording drift remains | repo quality/wiki checks; follow-up wording task |
| P0-11 | Normalize `docs/05.operations/` | `docs/05.operations/README.md`; runbooks/policies | partial | Structure is coherent; `workflow-security` wording and Vault endpoint role separation need updates | repo quality/wiki checks; scoped ops-doc follow-up |
| P0-12 | `.env.example` and `.env` role/key consistency | `.env.example`; `.env` key-name-only comparison | complete key-only | Key names match; values intentionally not inspected | key-name-only diff; value review remains human-owned |
| P0-13 | Relevant README freshness/template compliance | root/stage/area READMEs; 006 README rows | complete repo-static | Current overlay keeps freshness in the existing 006 chain | repo quality/wiki checks |
| P0-14 | Safe workspace-purpose implementation | Spec/Plan/Task 006; progress ledger | complete for P1/P2 docs | Implemented only low-risk authored SSoT updates | validation bundle; runtime/semantic work deferred |
| P0-15 | Implement docs lifecycle system for target folders | Spec 006; this plan; linked task | complete repo-static | Lifecycle traceability now includes external P0 IDs | repo quality/wiki checks |
| P0-16 | Workspace-specific AI Agent skill set | `.claude/skills/`; `harness-catalog.md`; `.agents/` | partial | Existing skills cover most roles; seven new duplicate skills rejected/deferred | skill existence/routing check; `.agents` consolidation deferred |
| P0-17 | Bootstrap boundaries | bootstrap docs; infrastructure contracts; GitOps root app docs | partial | Repo responsibility is documented; EndpointSlice/runtime handoff needs clarification | static checks; live boundary proof deferred |
| P0-18 | WSL2 and Docker prerequisites | ops/docs, scripts, contracts, `.env.example` | complete repo-static | WSL Linux native Docker prerequisites are documented; no runtime probe added | repo quality gate; live Docker/k3d check deferred |
| P0-19 | GitOps hierarchy | `gitops/root-app.yaml`; platform/shared app structure | complete repo-static | Root app/App-of-Apps/ApplicationSet split is static-checkable | GitOps validator and manifest validation |
| P0-20 | Secret-management responsibility | ESO/Vault manifests; `scripts/check-secret-handling.sh`; P3 plan | partial | Declarative model exists; live Vault auth and values remain outside scope | secret scan and manifests check; live proof deferred |
| P0-21 | External service contracts | `infrastructure/`; EndpointSlice/service manifests; `.env.example` | partial | PostgreSQL/Valkey contracts exist; EndpointSlice ownership ambiguity remains | static contract test; ownership clarification deferred |
| P0-22 | Documentation SSoT consistency | Spec/Plan/Task 006; progress ledger; READMEs | complete for this overlay | Exact P0 crosswalk and subagent-derived gaps are now recorded | full static validation bundle |

### Six Subagent Review Result Integration

| Role | Integrated finding | Decision | Follow-up |
| --- | --- | --- | --- |
| Documentation Lifecycle Reviewer | 006 chain is canonical, but external `P0-01` through `P0-22` IDs were absent | Add this crosswalk and VAL-SPC-006-016 | Keep older summaries historical |
| GitOps Infrastructure Reviewer | Static GitOps structure is coherent; EndpointSlice ownership and Traefik wording need owner review | Defer semantic desired-state changes | Use the P3 remediation chain or a new scoped follow-up |
| Scripts and Env Reviewer | Scripts are not deletion-ready; env key names match without value inspection | No deletion; record broad reference precheck requirement | Add deletion only through a reference-clearing task |
| QA CI/CD and Policy Reviewer | Static QA is strong; OPA/Conftest feasibility and `workflow-security` policy wording are undefined | Defer policy changes | Create a policy-gate feasibility task |
| Agent Governance Reviewer | Gateway remains thin; exact external P0 traceability and `.agents` mirror status need explicit handling | Add crosswalk; keep `.claude/skills/**` canonical | Defer `.agents` consolidation |
| Skills and Harness Reviewer | Existing skills cover most requested role agents; creating seven duplicate skills would add noise | Reject duplicate skill creation for this pass | Reassess only if a concrete repeated workflow is missing |

### Subagent-Derived Authored SSoT Gap Table

| Gap | Evidence path | Risk | Decision | Follow-up |
| --- | --- | --- | --- | --- |
| EndpointSlice ownership ambiguity for external services | `gitops/`; `infrastructure/`; P3 plan | Medium | Defer desired-state semantics | Clarify GitOps-owned vs break-glass ownership before changes |
| Traefik backend/fallback port wording drift | `traefik/README.md`; Traefik manifests | Low | Defer wording-only cleanup | Update wording in a scoped operations/docs pass |
| `workflow-security` policy wording drift from current CI jobs | `docs/05.operations/`; `.github/workflows/` | Medium | Defer CI policy wording | Align policy text with actual workflow structure |
| OPA/Conftest feasibility undefined | QA/CI docs and scripts | Medium | Defer policy-gate design | Evaluate Conftest only after policy ownership is named |
| Vault endpoint role separation note needed | `.env.example`; ops docs; infrastructure contracts | Medium | Defer ops-doc supplementation | Document host/browser vs Docker-network endpoint roles |
| Script deletion broad-reference precheck needed | `scripts/README.md`; this plan | Medium | Defer deletion | Require `rg` reference sweep, rollback, and task linkage |
| `.agents` mirror consolidation deferred | `.agents/`; `.claude/skills/`; harness catalog | Low | Keep `.claude/skills/**` canonical | Owner-reviewed consolidation only |

### Implementation Plan Delta

| Priority | Action type | Target | Change | Linked task | Verification | Rollback |
| --- | --- | --- | --- | --- | --- | --- |
| P1 | supplementation | Spec 006 | Add VAL-SPC-006-016 for exact external P0 traceability | T-058 | repo quality gate | Revert criterion |
| P1 | supplementation | 006 Plan | Add this P0-01 through P0-22 crosswalk and subagent gap integration | T-058, T-059 | repo quality gate; wiki check | Revert overlay section |
| P1 | supplementation | 006 Task | Add phase/task rows and current verification summary | T-060, T-062 | repo quality gate | Revert task rows/summary |
| P1 | supplementation | 006 Plan/Task links | Add reciprocal links to P3 GitOps Secret Runtime Remediation Plan/Task | T-061 | link/static checks | Revert link rows |
| P1 | memory | progress ledger | Record authored SSoT large-scale overlay and deferred boundaries | T-062 | repo quality gate | Revert progress entry |
| P3 | deferral | GitOps/runtime/CI/secrets/deletion | Do not implement high-risk or owner-dependent changes | T-059 | deferred-item tables | Separate approved follow-up |

### Verification Delta

The current task records the executable verification result. Live checks remain
deferred because this overlay is repo-static and does not have approval to query
or mutate k3d, Kubernetes, ArgoCD, Vault, PostgreSQL, Valkey, or CI rulesets.

### Checklist Gate Delta

| Checklist item | Status | Evidence |
| --- | --- | --- |
| Goal stated in one sentence | pass | Intent and Boundary section |
| Related files discovered | pass | P0 crosswalk and subagent integration tables |
| Scope and forbidden scope separated | pass | No runtime/secret/CI/Kubernetes semantic changes |
| Existing patterns preserved | pass | Existing 006 chain reused; no parallel SDD tree |
| Test/lint/check commands identified | pass | linked task Verification Summary |
| Completion criteria measurable | pass | VAL-SPC-006-016 and T-058 through T-062 |
| Recurring instructions handled through Skills/governance | pass | `.claude/skills/**` remains canonical |
| All P0 workstreams represented | pass | P0-01 through P0-22 crosswalk |
| Additional review items represented | pass | Crosswalk plus subagent-derived gap table |
| Workspace-specific skills designed/updated/deferred | pass | P0-16 and Skills/Harness row |

## Deferred Item Repo-Static Improvement Overlay - 2026-05-25

### Intent and Boundary

This overlay implements the approved repo-static follow-up for deferred items.
It keeps the existing 006 SDD chain canonical and treats the authored SSoT
large-scale overlay as the current base. It does not query live k3d, Kubernetes,
Docker, ArgoCD, Vault, PostgreSQL, Valkey, Traefik runtime, or GitHub remote
rulesets, and it does not inspect secret values.

### Deferred Item Improvement Table

| Deferred item | Repo-static change | Evidence path | Status after this overlay | Remaining non-static boundary |
| --- | --- | --- | --- | --- |
| EndpointSlice ownership ambiguity | Clarify that `gitops/platform/external-services/*.yaml` is the desired-state SSoT, while direct EndpointSlice patch/apply remains human-approved break-glass when ArgoCD resource exclusions or runtime drift prevent reconciliation | `gitops/README.md`; `docs/05.operations/policies/0002-wsl2-k3d-gitops-ha-operations-policy.md` | improved repo-static | live reconciliation proof and any direct cluster hotfix |
| Traefik backend/fallback port wording drift | Superseded by VAL-SPC-006-021 live evidence: external Traefik backend should target ingress-nginx `LoadBalancer` IP `172.18.0.240:443`; direct host fallback remains explicit-only | `traefik/README.md`; operations policy; live closure overlay | improved with live correction | external Traefik gateway runtime proof |
| `workflow-security` policy wording drift | Replace stale `workflow-security` job wording with current CI gate names: `branch-policy`, `pre-commit`, `repo-quality-static`, `manifest-static`, and `shell-static` | operations policy; `.github/workflows/ci.yml` | improved repo-static | GitHub branch protection/ruleset review |
| OPA/Conftest feasibility undefined | Record that no OPA/Conftest gate is introduced until policy owner, bundle location, install path, and failure semantics are defined | operations policy; this plan | improved repo-static | separate policy-gate design task |
| Vault endpoint role separation | Document host/browser `VAULT_ADDR`, in-cluster `vault-external` EndpointSlice, and Vault Kubernetes auth API endpoint roles separately | `.env.example`; operations policy | improved repo-static | live Vault/ESO readiness |
| Script deletion broad-reference precheck | Add explicit broad `rg` sweep, task linkage, rollback, and allowlist review before deleting or renaming scripts | `scripts/README.md` | improved repo-static | actual deletion remains separate owner-approved work |
| `.agents` mirror consolidation | Keep `.claude/skills/**` canonical and `.agents/**` ignored local mirror; no file movement or deletion | this plan; `.claude/CLAUDE.md`; repo quality gate | improved repo-static | owner-reviewed consolidation only |

### Implementation Plan Delta

| Priority | Action type | Target | Change | Linked task | Verification | Rollback |
| --- | --- | --- | --- | --- | --- | --- |
| P1 | supplementation | Spec 006 | Add VAL-SPC-006-017 for deferred item repo-static improvement | T-063 | repo quality gate | Revert criterion |
| P1 | supplementation | 006 Plan/Task | Add current-state overlay, T-063 through T-070, and verification evidence | T-063, T-070 | repo quality gate; wiki check | Revert overlay sections |
| P1 | improvement | GitOps and operations docs | Clarify EndpointSlice desired-state versus break-glass ownership | T-064 | repo quality gate; targeted `rg` | Revert wording |
| P1 | improvement | Traefik README and operations policy | Clarify external Traefik 443 route versus direct fallback 8443 route | T-065 | targeted stale wording check | Revert wording |
| P1 | improvement | Operations policy | Align CI gate names and record OPA/Conftest non-adoption boundary | T-066, T-067 | workflow YAML parse; targeted `rg` | Revert wording |
| P1 | improvement | `.env.example` and operations policy | Add Vault endpoint role separation comments without key changes | T-068 | env key-name-only comparison | Revert comments |
| P1 | improvement | `scripts/README.md` | Add deletion precheck and rollback contract | T-069 | repo quality gate; targeted `rg` | Revert section |
| P1 | memory | progress ledger | Record resolved repo-static deferrals and remaining non-static work | T-070 | repo quality gate | Revert progress entry |

### Verification Delta

| Check | Expected result | Notes |
| --- | --- | --- |
| Required repo-static validation bundle | PASS | Same command set as linked task Verification Summary |
| Stale `workflow-security` policy claim | no match in operations policy | CI workflow structure unchanged |
| Stale external Traefik `443 -> k3d 8443` claim | no match in updated docs | Direct fallback `8443` remains allowed as fallback wording |
| EndpointSlice ownership wording | present | GitOps desired-state and break-glass distinction recorded |
| Vault endpoint role wording | present | `.env.example` key set unchanged |
| `.agents` mirror state | ignored and untracked | no `.agents` movement or deletion |

## Task-Unit Commit Follow-up Overlay - 2026-05-25

### Intent and Boundary

This overlay implements the approved forward-only follow-up for task-unit
commit discipline. It records that `870febd` already reached `origin/main` as a
single broad commit that bundled authored SSoT overlay work, deferred item
repo-static work, and lifecycle hook changes. The repository will not rewrite
that public history. The corrective action is to record the exception, improve
future dirty-state guidance, and commit this follow-up as one logical unit.

No reset, rebase, amend, force-push, live runtime command, secret value review,
Kubernetes mutation, ArgoCD sync, or Vault write is included.

### Current State Decision

| Item | Current state | Decision | Follow-up rule |
| --- | --- | --- | --- |
| Published broad commit | `870febd` is on `main` and `origin/main` | Keep it as historical evidence | Do not rewrite published history for this cleanup |
| Task-unit commit policy | Governance and hooks require logical task-unit staging and `git diff --cached` review | Preserve and strengthen | Future broad dirty states must be split before commit |
| Corrective change | This overlay, hook wording, validator coverage, and progress entry are one work unit | Commit as one forward-only change | Use Conventional Commit with why/how body |

### Implementation Plan Delta

| Priority | Action type | Target | Change | Linked task | Verification | Rollback |
| --- | --- | --- | --- | --- | --- | --- |
| P1 | supplementation | Spec 006 | Add VAL-SPC-006-018 for task-unit commit follow-up | T-071 | repo quality gate | Revert criterion |
| P1 | supplementation | 006 Plan/Task | Add this overlay, T-071 through T-075, and verification summary | T-071, T-075 | repo quality gate; wiki check | Revert overlay sections |
| P1 | supplementation | progress ledger | Record `870febd` as a forward-only exception and capture future rule | T-072 | repo quality gate | Revert progress entry |
| P1 | guardrail | lifecycle hook and Git workflow rule | Strengthen dirty-state and published-history guidance | T-073 | hook self-test; shell syntax | Revert wording |
| P1 | test | repo quality gate | Require the stronger hook advisory in Stop and PreCompact simulations | T-074 | repo quality gate | Revert self-test phrase checks |
| P1 | commit | Git history | Create one forward-only corrective commit for this follow-up | T-075 | `git status --short --branch` | Revert commit with a normal revert if needed |

### Verification Delta

| Check | Expected result | Notes |
| --- | --- | --- |
| Repo quality gate | PASS | Covers hook self-test wording |
| LLM Wiki index | PASS | Ensures generated index freshness |
| Shell syntax | PASS | Covers `.claude/hooks/lifecycle-guard.sh` |
| JSON parse | PASS | Confirms hook config files remain valid |
| Lifecycle hook self-test | PASS | Stop and PreCompact mention task-unit discipline, multi-unit dirty states, and `git diff --cached` |
| Git status | clean and synced after push | No history rewrite |

## Approval-Bound Completion Audit Overlay - 2026-05-25

### Intent and Boundary

This overlay implements the approved follow-up review for items that were
previously blocked by approval or external state. It performs read-only live
runtime checks and GitHub remote inspection, then remediates the repo-backed CI
version inventory drift discovered from open PR evidence. It does not inspect
secret values, run Vault KV reads/writes, force ArgoCD sync, run `kubectl apply`
or `kubectl patch`, rewrite public history, or bypass `main` branch protection.

### Current-State Audit

| Area | Evidence | Current result | Decision |
| --- | --- | --- | --- |
| Docker/k3d | `docker context show`; `docker ps`; `k3d cluster list` | Docker context is `default`; no running containers; no k3d clusters listed | Live platform proof remains unavailable in current WSL state |
| Kubernetes API | `kubectl config current-context`; read-only `kubectl get` | context is `k3d-hyhome`; API `https://0.0.0.0:6550` refuses connection | Record current-state fail; do not treat as live success |
| ArgoCD/ESO metadata | read-only `kubectl get` only | same API refusal | Defer runtime metadata proof until cluster exists |
| GitHub branch protection | `gh api .../branches/main/protection` | `ci-summary` required; PR review settings present with zero required approvals; admin enforcement disabled; force-push/deletion disabled | Avoid direct main bypass; use branch/PR for follow-up |
| GitHub rulesets | `gh api .../rulesets` | no repository rulesets returned | Branch protection is the active remote policy evidence |
| Main CI | `gh run view` and check-runs for `d8b9c19` | latest main CI completed successfully | Main branch repo-static state is green |
| Dependabot PR #38 | `gh pr view`, failed repo-quality logs, and `gh pr close` | `actions/stale` drift to `v10.2.0` without version inventory update; closed as superseded by PR #39 | Keep replacement remediation in PR #39 |

### Implementation Plan Delta

| Priority | Action type | Target | Change | Linked task | Verification | Rollback |
| --- | --- | --- | --- | --- | --- | --- |
| P1 | supplementation | Spec 006 | Add VAL-SPC-006-019 for approval-bound completion audit | T-076 | repo quality gate | Revert criterion |
| P1 | supplementation | 006 Plan/Task | Add this audit overlay and T-076 through T-079 | T-076, T-079 | repo quality gate; wiki check | Revert overlay sections |
| P1 | CI/version inventory | `.github/workflows/stale.yml`; version inventory | Align `actions/stale` pin and SSoT inventory to `v10.2.0` | T-077 | repo quality gate; workflow parse | Revert both files together |
| P1 | memory | progress ledger | Record live unavailable state, GitHub remote policy, and PR replacement boundary | T-078 | repo quality gate | Revert progress entry |

### Verification Delta

| Check | Expected result | Notes |
| --- | --- | --- |
| Repo quality gate | PASS | Version inventory must match workflow pin |
| Workflow YAML parse | PASS | `.github/workflows/stale.yml` remains parseable |
| LLM Wiki index | PASS | Generated index freshness |
| Git diff whitespace | PASS | No whitespace errors |
| PR checks | PASS | PR #39 passed `ci-summary`, `pre-commit`, `repo-quality-static`, `branch-policy`, `changes`, `label`, and GitGuardian checks; manifest/shell jobs skipped by path-filter design |

## Post-Merge Completion Audit Overlay - 2026-05-25

### Intent and Boundary

This overlay records the current state after PR #39 was merged into `main`.
It proves the repo-static portion on the merged default branch, cleans up the
local merged feature branch, and performs no-secret-output bootstrap prechecks
for the remaining live-runtime proof. It does not print secret values, write
Vault data, force ArgoCD sync, or mutate Kubernetes because required external
runtime dependencies are unavailable.

### Current-State Audit

| Area | Evidence | Current result | Decision |
| --- | --- | --- | --- |
| PR #39 | `gh pr view 39` | merged at `2026-05-25T04:28:51Z` with merge commit `780fb7601e51ec534a11bca9a4b645d86bf6e470` | PR blocker resolved |
| Local `main` | `git pull --ff-only origin main`; `git status --short --branch` | local `main` fast-forwarded to `780fb76`; working tree clean | Use merged `main` as current SSoT |
| Main CI | `gh run list --branch main` | merge commit CI completed with `success` | Remote repo-static gate passed |
| Local static gates | repo quality, wiki index, GitOps, manifests, secret scan, contracts, shell syntax, JSON, workflow YAML, env key names, diff check | all passed on merged `main` | Repo-static portion complete |
| Live runtime | `docker context show`; `docker ps`; `k3d cluster list`; `kubectl get nodes --request-timeout=5s` | Docker context is `default`; no running containers; no k3d clusters; Kubernetes API `https://0.0.0.0:6550` refused connection | Live proof unavailable |
| Bootstrap prechecks | command presence, inotify, ports, certificate files, Vault health, PostgreSQL TCP, Valkey TCP | required commands, inotify, ports, and cert files are ready; Vault health is `000`; PostgreSQL write/read and Valkey are unreachable | Do not run bootstrap until external services are up |

### Implementation Plan Delta

| Priority | Action type | Target | Change | Linked task | Verification | Rollback |
| --- | --- | --- | --- | --- | --- | --- |
| P1 | supplementation | Spec 006 | Add VAL-SPC-006-020 for post-merge completion audit | T-081 | repo quality gate | Revert criterion |
| P1 | supplementation | 006 Plan/Task | Add this post-merge overlay and tasks | T-081, T-083 | repo quality gate; wiki check | Revert overlay sections |
| P1 | cleanup | local Git branch | Delete merged local branch `codex/approval-bound-completion-audit` | T-082 | `git branch --merged main` and `git status` | Recreate branch from `4f87a9e` if needed |
| P3 | deferral | live bootstrap/runtime proof | Keep bootstrap deferred until Vault, PostgreSQL, and Valkey are reachable | T-083 | no-secret-output prechecks | Start external services, then rerun bootstrap and live validation |

### Verification Delta

| Check | Result | Notes |
| --- | --- | --- |
| `bash scripts/validate-repo-quality-gates.sh .` | PASS | merged `main` |
| `bash scripts/generate-llm-wiki-index.sh --check` | PASS | generated index current |
| `bash scripts/validate-gitops-structure.sh` | PASS | root app and kustomization checks |
| `bash scripts/validate-k8s-manifests.sh .` | PASS | kube-linter optional skip; YAML syntax passed |
| `bash scripts/check-secret-handling.sh .` | PASS | no plaintext secret patterns |
| `bash infrastructure/tests/verify-contracts-static.sh` | PASS | static contracts passed |
| `find infrastructure scripts .claude/hooks -type f -name '*.sh' -exec bash -n {} +` | PASS | shell syntax |
| JSON parse | PASS | `.claude/settings.json`; `.codex/hooks.json` |
| workflow YAML parse | PASS | `.github/workflows/*.yml` |
| `.env.example` vs `.env` key-name-only compare | PASS | missing=0; extra=0 |
| `git diff --check` | PASS | no whitespace errors |
| live bootstrap precheck | BLOCKED | Vault, PostgreSQL, and Valkey unreachable |

## Live Bootstrap Runtime Closure Overlay - 2026-05-25

### Intent and Boundary

This overlay records the human-approved live bootstrap follow-up after PR #40
was merged. It continues to use the existing 006 SDD chain as the canonical
SSoT. It does not inspect or print secret values, rewrite public Git history,
force ArgoCD sync, or merge directly to `main`.

### Runtime Closure Decisions

| Area | Evidence | Decision | Follow-up |
| --- | --- | --- | --- |
| External dependencies | Vault, Valkey, PostgreSQL router, and k3d containers started locally; Vault health returned `200`; PostgreSQL write/read and Valkey TCP checks passed | Treat live bootstrap preconditions as satisfied for this approved run | Keep external service startup outside normal repo automation |
| MetalLB bootstrap | MetalLB chart `0.16.0` rendered only after explicitly disabling the `frr-k8s` ServiceMonitor value; cold image pulls exceeded the previous 120s wait | Add explicit Helm value and extend MetalLB timeout to 300s | Revisit if chart defaults change again |
| EndpointSlice boundary | ArgoCD excludes EndpointSlice resources, so only Services reconciled from `platform-external-services`; live Vault path failed until EndpointSlices were bootstrap-applied | Bootstrap applies all external-service `Service` and `EndpointSlice` resources before ESO/Vault validation | Keep Git desired state as SSoT and bootstrap as approved break-glass initializer |
| Vault Kubernetes auth | Vault reached Kubernetes API, but login returned `403` until the current `external-secrets` serviceAccount had TokenReview permission and reviewer JWT/CA were refreshed | Add GitOps ClusterRoleBinding to `system:auth-delegator` and refresh Vault auth config during approved live recovery | Vault token reviewer refresh remains a human-approved live operation |
| Traefik / TLS validation | Ingress `LoadBalancer` IP `172.18.0.240:443` with host/SNI resolve returned HTTP `200`; `127.0.0.1:443` is only valid when an external gateway is actually present | Make live TLS validation default to ingress-nginx LoadBalancer IP and keep external Traefik 443 as an optional check | External Traefik runtime proof remains separate from cluster bootstrap proof |

### Implementation Plan Delta

| Priority | Action type | Target | Change | Linked task | Verification | Rollback |
| --- | --- | --- | --- | --- | --- | --- |
| P1 | supplementation | Spec 006 | Add VAL-SPC-006-021 for approved live runtime closure | T-084 | repo quality gate | Revert criterion |
| P1 | supplementation | 006 Plan/Task | Add this overlay and T-084 through T-090 | T-084, T-090 | repo quality gate; wiki check | Revert overlay sections |
| P2 | bootstrap | `infrastructure/bootstrap-local.sh` | Set MetalLB `frr-k8s.prometheus.serviceMonitor.enabled=false`, use 300s timeout, and apply all external-service endpoints during bootstrap | T-085, T-086 | bootstrap run and shell syntax | Revert script edits |
| P2 | GitOps RBAC | `gitops/platform/eso/` | Add `external-secrets` TokenReview ClusterRoleBinding for Vault Kubernetes auth | T-087 | `kubectl auth can-i`; ESO/Vault live check | Remove binding manifest |
| P2 | validation | `infrastructure/tests/` | Support current MetalLB deployment name and validate TLS via ingress-nginx LoadBalancer IP | T-088 | `infrastructure/tests/run-all.sh` | Revert validation edits |
| P1 | Traefik docs/config | `traefik/`, `.env.example`, operations policy | Align external Traefik backend wording and config with ingress-nginx LoadBalancer IP | T-089 | targeted `rg`; YAML parse | Revert wording/config edits |
| P1 | verification | validation bundle | Run live and repo-static checks without printing secret values | T-090 | Verification Summary | Re-run after rollback |

### Verification Delta

| Check | Result | Notes |
| --- | --- | --- |
| `infrastructure/bootstrap-local.sh` | PASS | Reused `k3d-hyhome`; installed MetalLB/ArgoCD; applied external-service EndpointSlices |
| Vault Kubernetes auth login status | PASS | metadata-only check returned HTTP `200`; JWT and Vault token were not printed |
| `kubectl auth can-i create tokenreviews...` | PASS | `external-secrets` serviceAccount can create TokenReviews |
| `bash infrastructure/tests/verify-secrets.sh` | PASS | `vault-backend` and `argocd-external-valkey` Ready checks passed |
| `bash infrastructure/tests/run-all.sh` | PASS | cluster, MetalLB, GitOps, ESO/Vault, external service, network policy, and ingress/TLS checks passed |
| External Traefik 443 | DEFERRED | optional `CHECK_TRAEFIK_443=true` remains separate because no external gateway runtime proof was requested for this branch |

## Documentation/Governance-First Workspace Improvement Overlay - 2026-05-25

### Intent and Boundary

This overlay implements the approved documentation/governance-first plan for
the workspace improvement prompt. It records a fresh current-state review across
P0-01 through P0-22 and applies only low-risk documentation, governance, README,
example, and Skill metadata edits. It does not change Kubernetes semantics,
AppProject permissions, CI job structure, secret policy, live cluster state, or
`.env` values.

### Baseline Instruction Check

| Target | Checked | Key impact |
| --- | --- | --- |
| `AGENTS.md` | yes | Thin gateway, Korean user-facing responses, English governance/runtime docs, GitOps-first boundary |
| `CLAUDE.md` | yes | Root runtime shim delegates to `.claude/CLAUDE.md` |
| `.claude/CLAUDE.md` | yes | Runtime baseline, progress ledger, mirror parity, direct mutation boundary |
| `GEMINI.md` | yes | Root runtime shim delegates to governance providers |
| `docs/00.agent-governance/` | yes | Canonical JIT, scopes, provider notes, harness catalog, subagent protocol |
| `docs/99.templates/` | yes | README/template routing retained; no template structure changed |
| `.agent/`, `.agents/`, `.claude/`, `.codex/` | yes | `.claude` remains canonical; `.codex` mirrors updated; ignored `.agents` mirror cleanup deferred |

### Subagent Summary

| Role | Status | Key findings | Unknown |
| --- | --- | --- | --- |
| Documentation Lifecycle Reviewer | complete | 006 plan is canonical but needs current navigation; `examples/sample-app` was overstated as complete; cloud snapshot wording needed SSoT alignment | none |
| GitOps Infrastructure Reviewer | complete | App-of-Apps structure is intact; AppProject allow-list and `CreateNamespace=true` hardening remain semantic deferrals | live reconciliation proof outside this pass |
| Scripts and Env Reviewer | complete | Five active scripts remain keep; `.env.example` and `.env` key names match; `APP_STAGE` cleanup deferred | secret values intentionally unknown |
| QA CI/CD and Policy Reviewer | complete | Static checks pass; optional policy tools absent; kube-linter/OPA hardening deferred | CI runner optional-tool state |
| Agent Governance Reviewer | complete | JIT shorthand omitted `progress`; direct mutation and `doc-writer` ownership wording needed narrowing | none |
| Skills and Harness Reviewer | complete | Do not create duplicate candidate agents/skills; improve existing Skill descriptions; keep `.claude/skills/**` canonical | ignored `.agents/**` mirror cleanup deferred |

### Coverage Ledger

| Area | Target path | P0 ID | Investigation status | Representative files read | Gap count | Deletion/consolidation/deferral/skill candidate count | Unknown items | Next action |
| --- | --- | --- | --- | --- | ---: | ---: | --- | --- |
| Baseline governance | `AGENTS.md`, `.claude/CLAUDE.md`, `docs/00.agent-governance/` | P0-01, P0-16, P0-17, P0-22 | complete | `agentic.md`, `harness-catalog.md`, provider notes, agent mirrors | 3 | 10 | none | P1 wording updates and P3 deferrals recorded |
| Docs lifecycle | `docs/01.requirements` through `docs/99.templates` | P0-02, P0-11, P0-13, P0-15, P0-22 | complete | 006 spec/plan/task, operations guides/runbooks, README/template indexes | 4 | 3 | none | Current overlay and onboarding wording updated |
| Scripts and env | `scripts/`, `.env.example`, `.env` | P0-03, P0-04, P0-12, P0-18 | complete | `scripts/README.md`, validators, env key comparison | 2 | 2 | secret values | No deletion; `APP_STAGE` deferred |
| GitOps | `gitops/`, `gitops/README.md` | P0-05, P0-06, P0-17, P0-19, P0-20, P0-21 | complete | root app, AppProjects, platform apps, external-services, workloads/adminer | 5 | 6 | live ArgoCD sync | Semantic hardening deferred |
| Infrastructure | `infrastructure/`, `infrastructure/README.md` | P0-07, P0-08, P0-17, P0-18, P0-20, P0-21 | complete | bootstrap scripts, tests, contract checks | 2 | 2 | kubeconfig TLS root cause | Live TLS repair deferred |
| Traefik | `traefik/`, `traefik/README.md`, sample Traefik example | P0-09, P0-10 | complete | `traefik/*.yaml`, `examples/sample-app/traefik-k3d.yaml.example` | 1 | 1 | external gateway runtime proof | Sample backend aligned |
| Examples and contracts | `examples/`, cloud examples, external service docs | P0-13, P0-17, P0-18, P0-21, P0-22 | complete | `examples/README.md`, sample app README, version inventory | 3 | 2 | provider latest support | Wording normalized to version inventory snapshot |
| QA/CI/CD | `.github/`, `.pre-commit-config.yaml`, validators | P0-13, P0-14, P0-22 | complete | workflows, PR template, repo quality scripts | 3 | 5 | optional local tools | Optional-tool hardening deferred |

### Integrated Gap Analysis

#### Summary

- Overall status: partial, with repo-static documentation/governance improvements complete and live kubeconfig TLS repair deferred.
- P0 status: all P0-01 through P0-22 have current coverage, a gap decision, an implementation or deferral decision, verification coverage, and final-report status.
- Largest Gap: live `kubectl` access is blocked by kubeconfig TLS trust (`x509: certificate signed by unknown authority`), so `infrastructure/tests/run-all.sh` cannot prove current runtime health.
- Immediately implementable: JIT shorthand, direct mutation wording, `doc-writer` ownership wording, sample Traefik backend, onboarding/sample-app currentness, cloud snapshot wording, Skill descriptions, and 006 SDD evidence.
- Needs deferral: AppProject allow-list, `CreateNamespace=true`, kube-linter enforcement, OPA/Conftest, `.env` `APP_STAGE`, `.agents` mirror cleanup, kubeconfig TLS repair, destructive Git permission hardening, image tag/workload-kind policy scans.
- Unknown areas: secret values, live ArgoCD reconciliation state, external Traefik gateway runtime proof, provider latest support ranges.

#### P0 Workstream Gap Table

| P0 ID | Workstream | Gap | Evidence path | Impact | Risk | Action type | Priority |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P0-01 | Workspace purpose environment/system/rules | Runtime rules existed but JIT and mutation wording were inconsistent | `AGENTS.md`; `.claude/CLAUDE.md`; `agentic.md` | Agent execution ambiguity | Medium | improvement | P1 |
| P0-02 | `docs/` lifecycle rules | Current overlay needed explicit lifecycle traceability | this plan; linked spec/task | SDD traceability drift | Medium | supplementation | P1 |
| P0-03 | `scripts/` deletion/consolidation review | No deletion-safe one-off scripts found; keep classification needed to remain explicit | `scripts/README.md` | Accidental deletion risk | Low | deferral | P3 |
| P0-04 | Safe one-off script cleanup | Deletion criteria do not pass because scripts are referenced validators | `scripts/README.md`; CI docs | Broken validation path | Medium | deferral | P3 |
| P0-05 | GitOps infrastructure | AppProject and namespace ownership hardening are semantic changes | `gitops/` | ArgoCD behavior change risk | High | deferral | P3 |
| P0-06 | `gitops/README.md` normalization | No current P1 edit required after template review | `gitops/README.md`; template | Reader drift risk low | Low | supplementation | P1 |
| P0-07 | Infrastructure | Live validation blocked by kubeconfig TLS trust | `infrastructure/tests/run-all.sh` | Runtime proof unavailable | High | deferral | P3 |
| P0-08 | `infrastructure/README.md` normalization | No current P1 edit required after template review | `infrastructure/README.md`; template | Reader drift risk low | Low | supplementation | P1 |
| P0-09 | Traefik infrastructure | Sample Traefik config still pointed at old Docker DNS backend | `examples/sample-app/traefik-k3d.yaml.example` | Onboarding route mismatch | Medium | improvement | P1 |
| P0-10 | `traefik/README.md` normalization | Active README already documents LoadBalancer backend | `traefik/README.md` | None current | Low | supplementation | P1 |
| P0-11 | `docs/05.operations/` structure | Onboarding docs overstated sample-app as complete | operations onboarding guide/runbook | Misleading operator guidance | Medium | improvement | P1 |
| P0-12 | `.env.example` and `.env` key consistency | Key names match; `APP_STAGE` remains reserved/unused follow-up | env key-name-only compare | Contract cleanup deferred | Low | deferral | P3 |
| P0-13 | README freshness/template compliance | Root/examples cloud snapshot wording needed SSoT alignment | `README.md`; `examples/README.md` | Stale snapshot claim | Medium | improvement | P1 |
| P0-14 | Safe implementation | Only docs/governance P1 items are safe in this pass | approved plan | Scope control | Low | improvement | P1 |
| P0-15 | Docs lifecycle system | Existing 006 chain needed current pass update | 006 spec/plan/task/progress | Evidence fragmentation | Medium | supplementation | P1 |
| P0-16 | Workspace-specific AI Agent skills | Seven requested candidates duplicate existing harness surfaces; Skill descriptions not trigger-style | `.claude/skills/**`; `harness-catalog.md` | Skill routing drift | Medium | improvement | P1 |
| P0-17 | Bootstrap boundaries | Subagent/operator mutation boundary needed clearer wording | `AGENTS.md`; `.claude/CLAUDE.md`; `agentic.md` | Live mutation confusion | High | improvement | P1 |
| P0-18 | WSL2/Docker prerequisites | Docs SSoT exists; current live kubeconfig TLS trust blocks verification | `infrastructure/tests/run-all.sh`; kubeconfig metadata | Runtime proof unavailable | High | deferral | P3 |
| P0-19 | GitOps hierarchy | Hierarchy is clear; AppProject/ApplicationSet hardening deferred | `gitops/` | Potential future privilege sprawl | Medium | deferral | P3 |
| P0-20 | Secret responsibility | ESO/Vault model exists; policy changes and secret values out of scope | `gitops/platform/eso`; secret scan | Secret handling risk | High | deferral | P3 |
| P0-21 | External service contracts | Contracts exist; live TLS blocker prevents runtime proof | `gitops/platform/external-services`; infra tests | Runtime contract proof unavailable | Medium | deferral | P3 |
| P0-22 | Documentation SSoT consistency | Current-state overlay and sample/cloud wording needed synchronization | this plan; examples; README | Reader and agent drift | Medium | improvement | P1 |

#### Additional Review Criteria

| Review item | Current state | Gap | Evidence path | Required action |
| --- | --- | --- | --- | --- |
| Bootstrap boundary | GitOps-first and approved bootstrap/break-glass paths exist | Needed subagent/operator wording | `AGENTS.md`; `.claude/CLAUDE.md`; `agentic.md` | Implemented P1 wording; kubeconfig repair deferred |
| WSL2 + Docker prerequisites | Docker/k3d prerequisites documented; Docker/k3d containers observed running in baseline | `kubectl` TLS trust blocks live validation | infra tests; baseline live check | Record blocker; defer repair |
| GitOps hierarchy | Root app/platform/shared/workload split present | AppProject allow-list and namespace ownership hardening deferred | `gitops/` | P3 semantic follow-up |
| Secret-management responsibility | ESO/Vault and ClusterSecretStore model present | Policy tightening and secret value checks out of scope | `gitops/platform/eso`; secret scan | Defer sensitive changes |
| External service contracts | PostgreSQL/Valkey/Vault contracts documented and statically verified | Runtime proof blocked by kubeconfig TLS | `verify-contracts-static.sh`; live run-all blocker | Keep static proof; defer live repair |
| Documentation SSoT consistency | 006 SDD chain remains canonical | Sample/cloud/JIT wording drift found | 006 plan; README; examples | Implement P1 wording and overlay |

#### Deletion, Consolidation, Deferred, Skill, and Unknown Items

| Target | Type | Reason | Reference check | Recommended action |
| --- | --- | --- | --- | --- |
| `scripts/` | deletion candidate rejected | Current scripts are validators or operational helpers | README, CI, docs, scripts checked | Keep; require broad reference check before future deletion |
| `.agents/**` | deferred cleanup | Ignored mirror cleanup may affect local convenience state | `.claude/skills/**` canonical; `.agents` ignored | Defer until explicit mirror maintenance pass |
| Seven candidate agents/skills | rejected/deferred | Duplicate existing harness/agent surfaces without a concrete matrix gap | `harness-catalog.md`; `.claude/skills/**` | Do not create; improve existing Skill descriptions |
| AppProject allow-list | P3 deferred | Semantic ArgoCD permission change | `gitops/` | Plan separate GitOps hardening |
| `CreateNamespace=true` ownership | P3 deferred | Reconciliation behavior change | `gitops/` | Plan separate namespace ownership pass |
| kubeconfig TLS repair | P3 deferred | External live-state repair outside docs/governance scope | live `kubectl` TLS error | Repair in approved runtime pass |
| OPA/Conftest policy gate | P3 deferred | Needs policy owner and bundle design | QA/CI review | Create follow-up before enforcement |
| `.env` `APP_STAGE` | P3 deferred | Env policy cleanup could change local expectations | key-name-only compare | Handle in env contract pass |
| Secret values | unknown | Values intentionally not read or printed | policy and task boundary | Keep unknown |
| Provider latest support | unknown | No web refresh requested in this pass | version inventory | Use current inventory snapshot only |

#### Workspace-Specific Skill Set

| Skill | Status | Target path | Reason | Next action |
| --- | --- | --- | --- | --- |
| Compose Stack Agent | deferred/rejected as duplicate | existing harness/skills | Would duplicate repo-local governance without a concrete matrix gap | Reconsider only after matrix gap |
| Requirements-to-Design Agent | deferred/rejected as duplicate | existing docs routing skills | Existing SDD docs routing already covers traceability | Improve existing docs skills |
| Execution Plan Agent | deferred/rejected as duplicate | existing 006 chain and skills | Existing plan/task workflow is active | Keep using 006 chain |
| Task Breakdown Agent | deferred/rejected as duplicate | existing task artifacts | Task rows and supervisor routing cover breakdown | No new skill |
| Ops Runbook Agent | deferred/rejected as duplicate | existing docs/runbook skills | Would overlap doc-writer and operations docs | Use existing docs scope |
| Knowledge Map Agent | deferred/rejected as duplicate | `harness-catalog.md`, wiki-curator | Existing catalog/wiki-curator owns maps | Keep current surfaces |
| Policy Gate Agent | deferred/rejected as duplicate | validators/hooks | OPA/Conftest lacks owner and bundle | Defer policy design |
| Existing repo-local skills | updated | `.claude/skills/*/skill.md`; local `.agents/skills/*/skill.md` mirrors | Descriptions needed trigger-style `Use when...` wording; repo quality gate enforces mirror parity when local mirrors exist | Keep `.claude/skills/**` canonical; leave broader `.agents` cleanup deferred |

### Implementation Plan

#### P0 Mandatory Workstreams

| P0 ID | Action type | Target | Change | Linked task | Verification | Rollback |
| --- | --- | --- | --- | --- | --- | --- |
| P0-01 | improvement | Governance/runtime rules | JIT and mutation boundary wording plus repo-quality expected phrase | T-094 | targeted `rg`; repo quality | Revert wording/script phrase together |
| P0-02 | supplementation | 006 SDD chain | Add VAL-SPC-006-022 overlay | T-093 | repo quality/wiki check | Revert overlay |
| P0-03 | deferral | `scripts/` | Record no deletion-safe script | T-093 | script syntax/executability | N/A |
| P0-04 | deferral | `scripts/` | Defer deletion | T-093 | reference checks | N/A |
| P0-05 | deferral | `gitops/` | Keep semantic hardening deferred | T-093 | GitOps structure check | N/A |
| P0-06 | supplementation | `gitops/README.md` | Record reviewed state | T-093 | README compliance review | N/A |
| P0-07 | deferral | `infrastructure/` | Record kubeconfig TLS blocker | T-097 | live check blocked | N/A |
| P0-08 | supplementation | `infrastructure/README.md` | Record reviewed state | T-093 | README compliance review | N/A |
| P0-09 | improvement | Traefik sample | Align backend to `172.18.0.240:443` | T-095 | targeted stale backend check | Revert sample |
| P0-10 | supplementation | `traefik/README.md` | Record reviewed state | T-093 | README compliance review | N/A |
| P0-11 | improvement | operations onboarding | Mark sample minimal, adminer fuller reference | T-095 | targeted wording check | Revert wording |
| P0-12 | deferral | env files | Record key parity and `APP_STAGE` deferral | T-093 | key-name-only compare | N/A |
| P0-13 | improvement | root/examples README | Normalize cloud snapshot wording | T-095 | targeted snapshot check | Revert wording |
| P0-14 | improvement | safe implementation | Limit implementation to P1 docs/governance | T-094..T-096 | verification bundle | Revert scoped edits |
| P0-15 | supplementation | docs lifecycle | Link current pass to 006 spec/plan/task/progress | T-093, T-099 | repo quality | Revert overlay/progress |
| P0-16 | improvement | repo-local skills | Update descriptions, sync existing local mirrors, and do not create duplicate skills | T-096 | trigger-style and mirror parity checks | Revert descriptions |
| P0-17 | improvement | bootstrap boundary | Clarify subagent/operator mutation boundary | T-094 | targeted wording check | Revert wording |
| P0-18 | deferral | WSL2/Docker prereqs | Record current TLS blocker and prerequisites state | T-097 | live check blocked | N/A |
| P0-19 | deferral | GitOps hierarchy | Defer semantic hierarchy hardening | T-093 | GitOps structure check | N/A |
| P0-20 | deferral | secret responsibility | Keep sensitive policy changes deferred | T-093 | secret scan | N/A |
| P0-21 | deferral | external contracts | Keep static proof; live proof deferred | T-097 | contract static check | N/A |
| P0-22 | improvement | docs SSoT | Align overlay, examples, README, JIT, Skill descriptions | T-093..T-096 | repo quality/wiki check | Revert scoped edits |

#### P1 Low Risk / Immediate Implementation

| Action type | Target | Change | Linked task | Verification | Rollback |
| --- | --- | --- | --- | --- | --- |
| improvement | JIT shorthand | Add `progress` to provider, rule, agent, and Codex mirror shorthand | T-094 | no stale shorthand remains | Revert strings |
| improvement | repo quality gate | Align JIT expected phrase with canonical `progress` step | T-094 | repo quality gate | Revert script phrase |
| improvement | mutation boundary | Clarify subagents never mutate and approved bootstrap/break-glass is operator-bound | T-094 | targeted wording check | Revert wording |
| improvement | `doc-writer` | Narrow from broad authorship to routing/drafting/delegated updates | T-094 | mirror parity and targeted wording | Revert wording |
| improvement | sample Traefik | Use ingress-nginx LoadBalancer backend `172.18.0.240:443` | T-095 | stale backend check | Revert sample |
| improvement | onboarding docs | Reframe sample as minimal template and adminer as fuller active reference | T-095 | targeted wording check | Revert wording |
| improvement | README cloud wording | Point to current version inventory snapshot | T-095 | targeted snapshot check | Revert wording |
| improvement | Skill descriptions | Convert safe existing descriptions to `Use when...` wording and sync existing local ignored mirrors required by the quality gate | T-096 | description and mirror parity checks | Revert frontmatter |

#### P2 Medium Risk / Limited Implementation

| Action type | Target | Change | Linked task | Verification | Rollback |
| --- | --- | --- | --- | --- | --- |
| none | n/a | No P2 implementation selected in this pass | n/a | n/a | n/a |

#### P3 High Risk / Deferred

| Action type | Target | Deferral reason | Pre-check | Follow-up work |
| --- | --- | --- | --- | --- |
| deferral | AppProject allow-list | Permission semantics change | AppProject review | Separate GitOps hardening plan |
| deferral | `CreateNamespace=true` | Namespace ownership semantics change | ApplicationSet review | Separate namespace ownership plan |
| deferral | kube-linter enforcement | Tooling/CI hardening not scoped | optional-tool availability | Add CI/static policy plan |
| deferral | OPA/Conftest | No policy owner/bundle yet | policy ownership decision | Create Policy Gate design |
| deferral | `.env` `APP_STAGE` | Env contract cleanup may affect local flows | env role review | Env contract plan |
| deferral | `.agents` mirror cleanup | Ignored local mirror maintenance | mirror inventory | Explicit mirror cleanup task |
| deferral | kubeconfig TLS repair | Live runtime repair out of docs scope | no-secret live diagnostics | Approved runtime pass |
| deferral | destructive Git permission hardening | Runtime permission policy change | tool permission review | Agent governance hardening pass |

### Verification

| Command or method | Result | Record location |
| --- | --- | --- |
| `bash scripts/validate-repo-quality-gates.sh .` | PASS | T-098 |
| `bash scripts/generate-llm-wiki-index.sh --check` | PASS | T-098 |
| `bash scripts/validate-gitops-structure.sh` | PASS | T-098 |
| `bash scripts/validate-k8s-manifests.sh .` | PASS; optional kube-linter skipped locally | T-098 |
| `bash scripts/check-secret-handling.sh .` | PASS | T-098 |
| `bash infrastructure/tests/verify-contracts-static.sh` | PASS | T-098 |
| Shell syntax for `infrastructure`, `scripts`, `.claude/hooks` | PASS | T-098 |
| JSON parse for `.claude/settings.json` and `.codex/hooks.json` | PASS | T-098 |
| Workflow YAML parse for `.github/workflows/*.yml` | PASS | T-098 |
| `.env.example` vs `.env` key-name-only comparison | PASS baseline: missing=0, extra=0, 18 keys each | T-098 |
| Targeted stale backend check | PASS; no active `k3d-hyhome-serverlb:443` in sample | T-095 |
| JIT shorthand check | PASS; shorthand includes `progress` | T-094 |
| Skill description check | PASS; repo-local descriptions use trigger-style wording | T-096 |
| `bash infrastructure/tests/run-all.sh` | BLOCKED baseline: `kubectl` TLS `x509: certificate signed by unknown authority` | T-097 |

#### P0 Verification Coverage

| P0 ID | Verification coverage | Status |
| --- | --- | --- |
| P0-01 | targeted governance wording and repo quality | pass |
| P0-02 | 006 chain update and repo quality | pass |
| P0-03 | script syntax/executability and reference decision | pass |
| P0-04 | deletion deferral recorded | pass |
| P0-05 | GitOps structure static check | pass |
| P0-06 | README template review | pass |
| P0-07 | infra static check; live blocker recorded | partial |
| P0-08 | README template review | pass |
| P0-09 | stale backend targeted check | pass |
| P0-10 | Traefik README review | pass |
| P0-11 | operations wording targeted check | pass |
| P0-12 | env key-name-only compare | pass |
| P0-13 | README snapshot wording check | pass |
| P0-14 | full repo-static verification bundle | pass |
| P0-15 | 006 spec/plan/task/progress check | pass |
| P0-16 | Skill description/routing check | pass |
| P0-17 | bootstrap boundary wording check | pass |
| P0-18 | prerequisite docs and live TLS blocker record | partial |
| P0-19 | GitOps structure check and deferral record | pass |
| P0-20 | secret scan and deferral record | pass |
| P0-21 | static contract check and live blocker record | partial |
| P0-22 | repo quality, wiki, and targeted SSoT checks | pass |

### Checklist Gate

| Checklist item | Status | Evidence |
| --- | --- | --- |
| Is the goal clear in one sentence? | pass | Documentation/governance-first limited implementation for WSL2/k3d/ArgoCD GitOps and SDD collaboration support |
| Are related files, logs, issues, or reproduction steps provided or discovered? | pass | Baseline instructions, six subagent reviews, validators, live TLS blocker |
| Are modification scope and forbidden scope separated? | pass | Intent and Boundary plus P3 deferred table |
| Are existing patterns, compatibility, and dependency rules stated? | pass | 006 chain extension, `.claude` canonical skills, `.codex` mirrors |
| Are test, lint, and type-check commands identified? | pass | Verification table |
| Are completion criteria measurable? | pass | VAL-SPC-006-022 and T-091 through T-100 |
| Are recurring instructions moved or planned for `AGENTS.md`, `CLAUDE.md`, governance docs, or Skills? | pass | JIT/mutation/doc-writer wording and Skill descriptions updated |
| Are all P0 workstreams represented in Coverage Ledger, Gap Analysis, Implementation Plan, Verification, and Final Report? | pass | P0 tables in this overlay |
| Are additional review items represented? | pass | Additional Review Criteria table |
| Are workspace-specific AI Agent skills designed, updated, created, or deferred with reasons? | pass | Workspace-Specific Skill Set table |

### Final Report

#### 1. Baseline Instruction Check

| Target | Checked | Key impact |
| --- | --- | --- |
| Baseline governance and runtime docs | yes | Scope locked to docs/governance P1 edits and P3 deferrals |

#### 2. P0 Mandatory Workstream Status

| P0 ID | Workstream | Status | Evidence | Next action |
| --- | --- | --- | --- | --- |
| P0-01 | Environment/system/rules | complete | governance wording updates | Verify and keep P3 runtime changes deferred |
| P0-02 | `docs/` lifecycle | complete | VAL-SPC-006-022 | Keep 006 chain current |
| P0-03 | scripts review | complete | no deletion-safe scripts | Keep scripts |
| P0-04 | one-off cleanup | deferred | reference checks do not permit deletion | Separate cleanup only with proof |
| P0-05 | GitOps infra | partial | static structure pass, semantic hardening deferred | Separate GitOps plan |
| P0-06 | `gitops/README.md` | complete | reviewed | No P1 edit |
| P0-07 | infrastructure | partial | static proof, live TLS blocker | Repair kubeconfig later |
| P0-08 | `infrastructure/README.md` | complete | reviewed | No P1 edit |
| P0-09 | Traefik infra | complete | sample backend update | Verify targeted check |
| P0-10 | `traefik/README.md` | complete | reviewed | No P1 edit |
| P0-11 | operations docs | complete | onboarding wording update | Verify targeted check |
| P0-12 | env parity | complete | key names match | `APP_STAGE` deferred |
| P0-13 | README freshness | complete | root/examples README updates | Verify targeted check |
| P0-14 | safe implementation | complete | P1-only changes | Verify bundle |
| P0-15 | docs lifecycle system | complete | spec/plan/task/progress | Keep current |
| P0-16 | AI Agent skills | complete | descriptions updated; duplicates deferred | Revisit only with matrix gap |
| P0-17 | bootstrap boundaries | complete | mutation boundary wording | Keep operator-bound exceptions |
| P0-18 | WSL2/Docker prereqs | partial | prerequisite checks and TLS blocker | Runtime repair later |
| P0-19 | GitOps hierarchy | partial | structure pass; semantic hardening deferred | Separate plan |
| P0-20 | secret responsibility | partial | scan pass; policy changes deferred | Separate security plan |
| P0-21 | external contracts | partial | static contracts pass; live proof blocked | Runtime repair later |
| P0-22 | documentation SSoT | complete | overlay and wording updates | Verify bundle |

#### 3. Additional Review Criteria Status

| Review item | Status | Evidence | Next action |
| --- | --- | --- | --- |
| Bootstrap boundary | complete | governance wording | Keep live mutation operator-bound |
| WSL2 + Docker prerequisites | partial | live TLS blocker | Repair kubeconfig later |
| GitOps hierarchy | partial | static structure | Defer semantic hardening |
| Secret responsibility | partial | secret scan and deferral | Separate security plan |
| External service contracts | partial | static contracts | Live proof after TLS repair |
| Documentation SSoT consistency | complete | 006 overlay and wording updates | Keep current overlay first |

#### 4. Coverage Ledger Summary

| Area | Investigation status | Gap count | Candidate count | Unknown |
| --- | --- | ---: | ---: | --- |
| Governance/docs/scripts/gitops/infra/traefik/examples/QA/skills | complete | 23 | 31 | secret values, provider latest support, live ArgoCD/runtime proof |

#### 5. Subagent Summary

| Role | Status | Key findings | Unknown |
| --- | --- | --- | --- |
| Six role reviewers | complete | JIT/doc-writer/sample/cloud/skill description P1 edits; semantic/runtime changes deferred | live runtime and secret values |

#### 6. Integrated Gap Analysis Summary

| Area | Key Gap | Risk | Action | Priority |
| --- | --- | --- | --- | --- |
| Governance/docs/examples/skills | currentness and routing drift | Medium | implemented P1 | P1 |
| GitOps/infra/secrets/runtime | semantic/live-state hardening | High | deferred | P3 |

#### 7. spec/task/plan Updates

| Document | Change | Linked work |
| --- | --- | --- |
| Spec 006 | Added VAL-SPC-006-022 | P0 overlay |
| Plan 006 | Added current-state navigation and this overlay | T-091 through T-100 |
| Task 006 | Added T-091 through T-100 and Phase 20 | VAL-SPC-006-022 |
| Progress ledger | Add 2026-05-25 documentation/governance entry after verification | T-099 |

#### 8. Workspace-Specific AI Agent Skills

| Skill | Status | Path or target path | Reason | Next action |
| --- | --- | --- | --- | --- |
| Existing repo-local skills | updated | `.claude/skills/**/skill.md` | Trigger-style descriptions | Verify descriptions |
| Seven requested candidate agents/skills | deferred/rejected | existing harness surfaces | Duplicative without matrix gap | Revisit only with concrete gap |

#### 9. Implementation Changes

| Target | Change | Reason | Linked task |
| --- | --- | --- | --- |
| Governance/runtime docs and mirrors | JIT, mutation boundary, `doc-writer` wording, and matching quality-gate phrase | Agent boundary clarity | T-094 |
| Examples/onboarding/README | sample backend/currentness/cloud wording | Documentation SSoT | T-095 |
| `.claude/skills/**` and existing `.agents/skills/**` mirrors | Trigger-style descriptions with mirror parity | Skill routing clarity and quality-gate compatibility | T-096 |
| 006 SDD chain | Current overlay | Evidence continuity | T-093 |

#### 10. Deletion, Consolidation, and Deferred Items

| Target | Type | Reason | Reference check | Recommended action |
| --- | --- | --- | --- | --- |
| `scripts/` | deletion deferred | referenced validators | pass | keep |
| semantic GitOps/secret/CI/runtime changes | deferred | outside approved scope | recorded | separate plans |
| `.agents/**` | cleanup deferred | ignored local mirror | recorded | explicit maintenance pass |

#### 11. Verification

| Command or method | Result | Record location |
| --- | --- | --- |
| Static and targeted checks | PASS | T-098 |
| Live `run-all.sh` | BLOCKED by kubeconfig TLS trust | T-097 |

#### 12. Checklist Gate

| Checklist item | Status | Evidence |
| --- | --- | --- |
| All checklist items | pass or partial only where live runtime is blocked | Checklist Gate table |

#### 13. Remaining Risks and Next Work

- Repair kubeconfig TLS trust before rerunning `infrastructure/tests/run-all.sh`.
- Plan semantic GitOps hardening separately for AppProject allow-list and namespace ownership.
- Define an OPA/Conftest owner and bundle before enforcing policy gates.
- Keep secret values uninspected unless a human explicitly requests a sensitive runtime operation.
- Refresh cloud provider support separately before treating examples as deployable cloud guidance.

## Unreviewed-Area Follow-up Overlay - 2026-05-25

### Intent and Boundary

This overlay answers the follow-up request to check whether any requested areas
were not sufficiently reviewed. It narrows to the explicitly named focus areas:
`scripts/`, `gitops/`, `infrastructure/`, and `docs/05.operations/`. Changes are
P1 documentation or diagnostic clarity only. It does not change GitOps
semantics, AppProject permissions, CI job topology, secret policy, live cluster
state, or `.env` values.

### Brainstorming Design Lens

| Approach | Trade-off | Decision |
| --- | --- | --- |
| Re-run the whole workspace audit | Maximum coverage but high churn and duplicates the existing 006 chain | Rejected for this continuation |
| Only run validators | Fast but too weak to prove review coverage | Rejected as insufficient |
| Target weak evidence in the four named areas and update the 006 chain | Focused, evidence-driven, and keeps scope aligned with the active goal | Selected |

### Follow-up Gap Table

| Area | Weak or unreviewed evidence | Action | Risk | Verification |
| --- | --- | --- | --- | --- |
| `scripts/` | README still used the prior snapshot date and did not mention canonical JIT contract coverage after validator update | Updated script inventory wording and deletion/consolidation evidence date | Low | repo quality gate; broad reference sweep |
| `gitops/` | Semantic hardening deferrals were only in the large 006 overlay, not visible from the GitOps entrypoint | Added current hardening deferrals for AppProject allow-list, `CreateNamespace=true`, and image/workload policy scans | Low | GitOps structure and manifest checks |
| `infrastructure/` | Live `run-all.sh` blocker was recorded, but `verify-cluster.sh` hid the TLS trust cause behind a generic reachability message | Added TLS-specific diagnostic branch and README note | Low | shell syntax; live blocked output |
| `docs/05.operations/` | Modified onboarding guide/runbook content had stale `updated` metadata and README index dates | Updated frontmatter and guide/runbook README index rows | Low | repo quality gate and targeted index checks |

### Implementation Plan Delta

| Priority | Action type | Target | Change | Linked task | Verification | Rollback |
| --- | --- | --- | --- | --- | --- | --- |
| P1 | documentation | `scripts/README.md` | Refresh current inventory and deletion/consolidation evidence wording | T-102 | repo quality; reference sweep | Revert README wording |
| P1 | documentation | `gitops/README.md` | Surface semantic hardening deferrals at entrypoint | T-103 | GitOps structure and manifest checks | Revert README section |
| P1 | diagnostic | `infrastructure/tests/verify-cluster.sh`; `infrastructure/README.md` | Report kubeconfig TLS trust blocker explicitly | T-104 | shell syntax; live blocked run | Revert script/README wording |
| P1 | documentation | `docs/05.operations` onboarding docs/indexes | Align `updated` metadata and index dates with current edits | T-105 | repo quality; targeted index check | Revert metadata/index rows |
| P1 | evidence | 006 Spec/Plan/Task/progress | Record VAL-SPC-006-023 and T-101 through T-106 | T-101, T-106 | repo quality; wiki check | Revert overlay |

### Verification Result

| Command or method | Result | Notes |
| --- | --- | --- |
| `bash scripts/validate-repo-quality-gates.sh .` | PASS | Docs/governance and operations index checks |
| `bash scripts/generate-llm-wiki-index.sh --check` | PASS | Generated reference index unchanged |
| `bash scripts/validate-gitops-structure.sh` | PASS | GitOps structure unaffected |
| `bash scripts/validate-k8s-manifests.sh .` | PASS; optional `kube-linter` skipped locally | Manifest semantics unchanged |
| `bash scripts/check-secret-handling.sh .` | PASS | Secret policy unchanged |
| `bash infrastructure/tests/verify-contracts-static.sh` | PASS | Static contracts unchanged |
| `find infrastructure scripts .claude/hooks -type f -name '*.sh' -exec bash -n {} +` | PASS | Shell syntax after diagnostic edit |
| `bash infrastructure/tests/run-all.sh` | BLOCKED; reports kubeconfig TLS trust failure explicitly | Live state intentionally not repaired |
| targeted metadata/index checks | PASS | Operations guide/runbook dates match current edit |

## Residual Objective Completion Audit Overlay - 2026-05-25

### Intent and Boundary

This overlay answers the continuation check for requested objective areas that
were not part of the explicit four-path follow-up. It reviews the remaining
workspace-purpose axes using current files and validators, then records the
decision to avoid additional semantic implementation in this pass. It does not
change Kubernetes resources, AppProject permissions, CI job structure, secret
policy, live cluster state, or `.env` values.

### Residual Coverage Matrix

| Requirement axis | Current evidence | Status | Gap/decision | Verification |
| --- | --- | --- | --- | --- |
| Traefik local ingress | `traefik/README.md`; `traefik/*.yaml`; `examples/sample-app/traefik-k3d.yaml.example` | complete repo-static | Active sample and README use the ingress-nginx LoadBalancer backend; live route proof remains outside this docs/governance pass | targeted stale-backend check; manifest validation |
| Examples and cloud references | `examples/README.md`; `examples/sample-app/README.md`; version inventory snapshot links | complete repo-static | `sample-app` is a minimal onboarding template; `gitops/workloads/adminer` remains the fuller active reference; provider latest support is not refreshed here | targeted wording check; wiki check |
| Environment role/key parity | `.env.example`; `.env` key-name-only comparison | complete key-only | Keys match in the local checkout; values are intentionally uninspected and `APP_STAGE` cleanup stays deferred | key-name-only compare |
| QA/CI and policy gates | `.github/workflows/*.yml`; `.pre-commit-config.yaml`; `.github/zizmor.yml`; PR template | partial | Static workflow/config parsing is enough for this pass; actionlint/zizmor/kube-linter/OPA enforcement remains P3 policy work | YAML parse; repo quality; manifest validation |
| Agent governance | `AGENTS.md`; `.claude/CLAUDE.md`; `docs/00.agent-governance/**`; `.codex/agents/*.toml` | complete repo-static | Thin gateway and mirror contracts are represented; priority and destructive Git permission hardening remain deferred | repo quality gate |
| Repo-local Skills | `.claude/skills/**`; ignored `.agents/skills/**` mirrors | complete repo-static | Existing Skills cover the requested roles well enough; seven duplicate candidate skills remain rejected/deferred | trigger-style description check; repo quality gate |
| Bootstrap and WSL2/Docker prerequisites | `infrastructure/README.md`; `infrastructure/bootstrap-local.sh`; operations guides/runbooks | partial | Repo/static ownership is documented; live `run-all.sh` remains blocked by kubeconfig TLS trust repair | static contracts; blocked live check |
| Secret-management responsibility | `gitops/platform/eso`; `infrastructure/vault`; secret scanner | partial | ESO/Vault responsibility is declarative; live Vault auth and secret value checks remain outside this pass | secret scan; static contracts |
| External service contracts | `gitops/platform/external-services`; `infrastructure/tests/verify-contracts-static.sh`; `.env.example` | partial | PostgreSQL/Valkey contracts are static-checkable; live reachability remains blocked by the kubeconfig/runtime state | static contract test; blocked live check |
| Documentation SSoT ownership | 006 Spec/Plan/Task/progress; docs stage READMEs; generated LLM wiki index | complete repo-static | Current-state overlays are preserved in the existing 006 chain instead of creating a parallel task tree | repo quality; wiki check |

### Implementation Plan Delta

| Priority | Action type | Target | Change | Linked task | Verification | Rollback |
| --- | --- | --- | --- | --- | --- | --- |
| P1 | evidence | 006 Spec/Plan/Task/progress | Record residual objective completion audit and verification evidence | T-107 through T-111 | repo quality, wiki check, targeted residual checks | Revert this overlay, task rows, spec validation item, and progress entry |
| P3 | deferral | GitOps/CI/security/runtime semantics | Keep AppProject allow-list, `CreateNamespace=true`, image/workload policy scans, OPA/Conftest, `.env` policy cleanup, `.agents` mirror cleanup, destructive Git permission hardening, and kubeconfig TLS repair out of this pass | existing P3 rows | N/A for this pass | Separate approved follow-up |

### Verification Result

| Command or method | Result | Notes |
| --- | --- | --- |
| `bash scripts/validate-repo-quality-gates.sh .` | PASS | Repository governance and SDD chain after residual overlay |
| `bash scripts/generate-llm-wiki-index.sh --check` | PASS | Generated reference index unchanged |
| `bash scripts/validate-gitops-structure.sh` | PASS | Root app, Application manifests, and kustomization completeness |
| `bash scripts/validate-k8s-manifests.sh .` | PASS; optional `kube-linter` skipped locally | YAML syntax for 104 manifest files |
| `bash scripts/check-secret-handling.sh .` | PASS | No plaintext secret patterns found in scanned manifests |
| `bash infrastructure/tests/verify-contracts-static.sh` | PASS | Static external service, Vault, AppProject, and workload contracts |
| `find infrastructure scripts .claude/hooks -type f -name '*.sh' -exec bash -n {} +` | PASS | Shell syntax unchanged after this evidence-only overlay |
| workflow YAML parse for `.github/workflows/*.yml` | PASS; 5 files | Parser-only workflow syntax check |
| `.env.example` vs `.env` key-name-only comparison | PASS; missing=0, extra=0, 18 keys each | Values intentionally not printed or inspected |
| targeted residual content checks | PASS | Traefik backend, sample/adminer wording, version inventory, JIT/progress routing, `doc-writer`, and Skill descriptions |
| `git diff --check` | PASS | No whitespace errors |
| `bash infrastructure/tests/run-all.sh` | BLOCKED | `kubectl` cannot reach cluster: kubeconfig TLS trust failed (`x509: certificate signed by unknown authority`) |

## Operations Index Guardrail Overlay - 2026-05-25

### Intent and Boundary

This overlay follows the continuation audit's weak-proof check for
`docs/05.operations`. It keeps the implementation low risk: README index rows
and repository quality validation only. It does not change operations policy
content, Kubernetes semantics, bootstrap behavior, live cluster state, or secret
material.

### Gap Table

| Area | Gap | Evidence path | Impact | Risk | Action type | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| Operations guides index | Superseded guide frontmatter had `updated: 2026-05-22`, but README index showed `2026-05-21` | `docs/05.operations/guides/0005-new-app-gitops-onboarding-guide.md`; `docs/05.operations/guides/README.md` | Stage 05 freshness drift | Low | improvement | P1 |
| Operations policies index | Four policy frontmatter dates were newer than README index dates | `docs/05.operations/policies/*.md`; `docs/05.operations/policies/README.md` | Stage 05 freshness drift | Low | improvement | P1 |
| Operations runbooks index | Superseded runbook frontmatter had `updated: 2026-05-22`, but README index showed `2026-05-21` | `docs/05.operations/runbooks/0006-new-app-onboarding-runbook.md`; `docs/05.operations/runbooks/README.md` | Stage 05 freshness drift | Low | improvement | P1 |
| Quality gate coverage | Repo quality gate did not enforce operations subfolder index/frontmatter parity | `scripts/validate-repo-quality-gates.sh` | Drift could recur silently | Low | improvement | P1 |

### Implementation Plan Delta

| Priority | Action type | Target | Change | Linked task | Verification | Rollback |
| --- | --- | --- | --- | --- | --- | --- |
| P1 | documentation | `docs/05.operations/guides/README.md`; `docs/05.operations/policies/README.md`; `docs/05.operations/runbooks/README.md` | Align index `최종 수정` dates with document frontmatter | T-112, T-113 | operations index/frontmatter sync check | Revert README rows |
| P1 | guardrail | `scripts/validate-repo-quality-gates.sh`; `scripts/README.md` | Validate guides/policies/runbooks index coverage, stale links, status, and updated date parity | T-114 | repo quality gate | Revert validator and README wording |
| P1 | evidence | 006 Spec/Plan/Task/progress | Record VAL-SPC-006-025 and verification | T-115, T-116 | repo quality and wiki checks | Revert overlay entries |

### Verification Result

| Command or method | Result | Notes |
| --- | --- | --- |
| operations index/frontmatter sync targeted check | PASS | Guides, policies, and runbooks all match frontmatter status/date |
| `bash scripts/validate-repo-quality-gates.sh .` | PASS | New operations index guardrail passed |
| `bash scripts/generate-llm-wiki-index.sh --check` | PASS | Generated reference index unchanged |
| `bash -n scripts/validate-repo-quality-gates.sh` | PASS | Validator shell syntax after guardrail edit |
| `git diff --check` | PASS | No whitespace errors |

## Scripts Inventory Guardrail Overlay - 2026-05-25

### Intent and Boundary

This overlay follows the completion audit's weak-proof check for `scripts/`.
The implementation is limited to repository-static validation and inventory
wording. It does not delete, rename, consolidate, or change script behavior.

### Gap Table

| Area | Gap | Evidence path | Impact | Risk | Action type | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| Script inventory validation | Repo quality gate only checked that each script name appeared somewhere in `scripts/README.md` | `scripts/validate-repo-quality-gates.sh`; `scripts/README.md` | Deletion/consolidation review could drift while still passing validation | Low | improvement | P1 |
| Script entrypoint validation | Executable bit and Bash shebang were not part of the repo quality gate | `scripts/*.sh` | CI/manual command contracts could silently degrade | Low | improvement | P1 |

### Implementation Plan Delta

| Priority | Action type | Target | Change | Linked task | Verification | Rollback |
| --- | --- | --- | --- | --- | --- | --- |
| P1 | guardrail | `scripts/validate-repo-quality-gates.sh`; `scripts/README.md` | Validate script inventory rows, explicit decisions, Tier A/B retention for `Keep`, executable bit, and Bash shebang | T-117, T-118 | repo quality and targeted scripts inventory check | Revert validator and README wording |
| P1 | evidence | 006 Spec/Plan/Task/progress | Record VAL-SPC-006-026 and verification | T-119 through T-121 | repo quality, shell syntax, wiki check | Revert overlay entries |

### Verification Result

| Command or method | Result | Notes |
| --- | --- | --- |
| scripts inventory guardrail targeted check | PASS | Five scripts have exact inventory rows, `Keep` decisions, Tier A/B retention evidence, executable bit, and Bash shebang |
| `bash scripts/validate-repo-quality-gates.sh .` | PASS | New scripts inventory guardrail passed |
| `bash scripts/generate-llm-wiki-index.sh --check` | PASS | Generated reference index unchanged |
| `bash -n scripts/validate-repo-quality-gates.sh` | PASS | Validator shell syntax after scripts guardrail edit |
| `git diff --check` | PASS | No whitespace errors |

## Environment Key Contract Guardrail Overlay - 2026-05-25

### Intent and Boundary

This overlay follows the completion audit's weak-proof check for
`.env.example` and local `.env` consistency. It makes the existing key-name-only
comparison part of the repository quality gate while preserving the secret
boundary: values are not printed or recorded, `.env` stays ignored/untracked,
and CI-capable contexts without a local `.env` still validate `.env.example`.

### Gap Table

| Area | Gap | Evidence path | Impact | Risk | Action type | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| Environment key parity | Key-name-only comparison was recorded as ad hoc evidence, not enforced by a reusable repo gate | `.env.example`; `.env`; `scripts/validate-repo-quality-gates.sh` | Env role/key drift could recur silently | Low | improvement | P1 |
| Secret boundary | `.env` must remain ignored/untracked while allowing key-only validation | `.gitignore`; `.env.example`; `.env` | Secret value exposure or accidental tracking risk | Medium | improvement | P1 |

### Implementation Plan Delta

| Priority | Action type | Target | Change | Linked task | Verification | Rollback |
| --- | --- | --- | --- | --- | --- | --- |
| P1 | guardrail | `scripts/validate-repo-quality-gates.sh`; `scripts/README.md` | Validate `.env` ignore/tracking contract, unique `.env.example` keys, duplicate local `.env` keys, and key parity when `.env` exists | T-122, T-123 | repo quality and targeted env key-only check | Revert validator and README wording |
| P1 | evidence | 006 Spec/Plan/Task/progress | Record VAL-SPC-006-027 and verification | T-124 through T-126 | repo quality, shell syntax, wiki check | Revert overlay entries |

### Verification Result

| Command or method | Result | Notes |
| --- | --- | --- |
| env key-only guardrail targeted check | PASS; `.env.example` keys=18, `.env` keys=18 | Key names only; values not printed |
| `bash scripts/validate-repo-quality-gates.sh .` | PASS | New environment key contract guardrail passed |
| `bash scripts/generate-llm-wiki-index.sh --check` | PASS | Generated reference index unchanged |
| `bash -n scripts/validate-repo-quality-gates.sh` | PASS | Validator shell syntax after env guardrail edit |
| `git diff --check` | PASS | No whitespace errors |

## GitOps Hierarchy Guardrail Overlay - 2026-05-25

### Intent and Boundary

This overlay follows the residual objective audit for GitOps hierarchy
consistency. It keeps the change repo-static and guardrail-only: no Kubernetes
resource semantics, AppProject permissions, ArgoCD ownership model, live cluster
state, secret policy, CI job structure, or `.env` values are changed.

### Gap Table

| Area | Gap | Evidence path | Impact | Risk | Action type | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| GitOps hierarchy | `validate-gitops-structure.sh` checked kind and kustomization shape but did not assert root Application, ApplicationSet, platform app, and workload source ownership boundaries | `scripts/validate-gitops-structure.sh`; `gitops/clusters/local/`; `gitops/apps/root/` | App-of-Apps and ApplicationSet responsibility drift could recur silently | Medium | improvement | P1 |
| README command contract | `gitops/README.md` and `scripts/README.md` described hierarchy but did not identify the new executable boundary checks | `gitops/README.md`; `scripts/README.md` | Operators could miss which static gate protects the GitOps hierarchy | Low | supplementation | P1 |

### Implementation Plan Delta

| Priority | Action type | Target | Change | Linked task | Verification | Rollback |
| --- | --- | --- | --- | --- | --- | --- |
| P1 | guardrail | `scripts/validate-gitops-structure.sh`; `gitops/README.md`; `scripts/README.md` | Validate `root-platform -> gitops/apps/root`, `apps-generator -> gitops/workloads/*`, required `clusters/local` resources, root app `platform` project, and local source path prefixes for root app manifests | T-127 through T-129 | GitOps structure, manifest syntax, repo quality, shell syntax, wiki check | Revert validator and README wording |
| P1 | evidence | 006 Spec/Plan/Task/progress | Record VAL-SPC-006-028 and verification | T-130, T-131 | repo quality, GitOps structure, wiki check | Revert overlay entries |

### Verification Result

| Command or method | Result | Notes |
| --- | --- | --- |
| `bash scripts/validate-gitops-structure.sh` | PASS | Root Application, apps ApplicationSet, cluster resources, root app project, and local source path boundaries passed |
| `bash scripts/validate-k8s-manifests.sh .` | PASS | YAML syntax passed for 104 files; optional `kube-linter` skipped locally because it is not installed |
| `bash scripts/validate-repo-quality-gates.sh .` | PASS | Repository quality gates passed after GitOps guardrail edit |
| `bash scripts/generate-llm-wiki-index.sh --check` | PASS | Generated reference index unchanged |
| `bash -n scripts/validate-gitops-structure.sh` | PASS | Validator shell syntax after hierarchy guardrail edit |
| `git diff --check` | PASS | No whitespace errors |

## Infrastructure Test Inventory Guardrail Overlay - 2026-05-25

### Intent and Boundary

This overlay follows the continuation audit for `infrastructure/`. It keeps the
change repo-static and documentation/governance-only: no live cluster command,
Kubernetes resource semantics, AppProject permissions, secret policy, CI job
structure, external service state, or kubeconfig TLS trust is changed.

### Gap Table

| Area | Gap | Evidence path | Impact | Risk | Action type | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| Infrastructure test inventory | `infrastructure/README.md` described static/live test categories but did not list each `infrastructure/tests/*.sh` command with preconditions, result semantics, and retention surface | `infrastructure/README.md`; `infrastructure/tests/` | Test deletion, rename, or consolidation drift could recur without an explicit owner-facing inventory | Low | improvement | P1 |
| Live aggregate parity | `run-all.sh` called live tests, but the repo quality gate did not verify that the live-test inventory and aggregate call list stay in sync | `infrastructure/tests/run-all.sh`; `scripts/validate-repo-quality-gates.sh` | A live test could be added or removed without updating the aggregate entrypoint or README contract | Medium | improvement | P1 |

### Implementation Plan Delta

| Priority | Action type | Target | Change | Linked task | Verification | Rollback |
| --- | --- | --- | --- | --- | --- | --- |
| P1 | guardrail | `infrastructure/README.md`; `scripts/validate-repo-quality-gates.sh` | Add Infrastructure Test Inventory and validate executable bits, Bash shebangs, exact test rows, nonempty preconditions/result semantics/retention surfaces, and `run-all.sh` live-test call parity | T-132 through T-134 | repo quality, shell syntax, static contracts, wiki check | Revert README and validator edits |
| P1 | evidence | 006 Spec/Plan/Task/progress | Record VAL-SPC-006-029 and verification | T-135, T-136 | repo quality and wiki check | Revert overlay entries |

### Verification Result

| Command or method | Result | Notes |
| --- | --- | --- |
| `bash scripts/validate-repo-quality-gates.sh .` | PASS | New infrastructure test inventory and `run-all.sh` parity guardrail passed |
| `bash -n scripts/validate-repo-quality-gates.sh` | PASS | Validator shell syntax after guardrail edit |
| `find infrastructure scripts .claude/hooks -type f -name '*.sh' -exec bash -n {} +` | PASS | Shell syntax for infrastructure, scripts, and hooks |
| `bash infrastructure/tests/verify-contracts-static.sh` | PASS | Static infrastructure contracts still pass |
| `bash scripts/generate-llm-wiki-index.sh --check` | PASS | Generated reference index unchanged |
| `git diff --check` | PASS | No whitespace errors |

## Traefik Route Inventory Guardrail Overlay - 2026-05-25

### Intent and Boundary

This overlay follows the continuation audit for `traefik/`. It keeps the change
repo-static and reference-only: no external Traefik runtime, live gateway state,
Kubernetes resource semantics, AppProject permissions, secret policy, CI job
structure, or kubeconfig TLS trust is changed.

### Gap Table

| Area | Gap | Evidence path | Impact | Risk | Action type | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| Traefik route inventory | `traefik/README.md` described the backend contract but did not list each dynamic config with host/backend ownership | `traefik/README.md`; `traefik/*.yaml` | Route/backend drift could recur without a row-level owner-facing inventory | Low | improvement | P1 |
| Backend drift guardrail | Stale backend checks were recorded as targeted evidence but not enforced by the repo quality gate | `scripts/validate-repo-quality-gates.sh`; `examples/sample-app/traefik-k3d.yaml.example` | Sample or active dynamic configs could silently regress to the old Docker DNS backend | Medium | improvement | P1 |

### Implementation Plan Delta

| Priority | Action type | Target | Change | Linked task | Verification | Rollback |
| --- | --- | --- | --- | --- | --- | --- |
| P1 | guardrail | `traefik/README.md`; `scripts/validate-repo-quality-gates.sh` | Add Traefik Route Inventory and validate config coverage, router host, backend URL, `websecure`, TLS, service transport, and stale backend absence for active configs plus sample app example | T-137 through T-139 | repo quality, manifest validation, shell syntax, wiki check | Revert README and validator edits |
| P1 | evidence | 006 Spec/Plan/Task/progress | Record VAL-SPC-006-030 and verification | T-140, T-141 | repo quality and wiki check | Revert overlay entries |

### Verification Result

| Command or method | Result | Notes |
| --- | --- | --- |
| `bash scripts/validate-repo-quality-gates.sh .` | PASS | New Traefik route inventory and backend drift guardrail passed |
| `bash -n scripts/validate-repo-quality-gates.sh` | PASS | Validator shell syntax after guardrail edit |
| `bash scripts/validate-k8s-manifests.sh .` | PASS | YAML syntax passed for 104 files; optional `kube-linter` skipped locally because it is not installed |
| `bash scripts/generate-llm-wiki-index.sh --check` | PASS | Generated reference index unchanged |
| `git diff --check` | PASS | No whitespace errors |

## Operations Routing Matrix Guardrail Overlay - 2026-05-25

### Intent and Boundary

This overlay follows the continuation audit for `docs/05.operations/`. It keeps
the change structural and repo-static: no operations content semantics, live
cluster state, secret policy, GitOps manifests, CI job structure, or runtime
configuration are changed.

### Gap Table

| Area | Gap | Evidence path | Impact | Risk | Action type | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| Operations stage routing | The stage README routed guides, policies, runbooks, incidents, and postmortems, but the table had no explicit heading for targeted validation | `docs/05.operations/README.md` | Stage-level routing drift could recur outside the existing subfolder index guardrail | Low | supplementation | P1 |
| Operations bucket/template validation | Repo quality enforced subfolder index/frontmatter parity but did not validate exact operations buckets or template-routing links from the stage README | `scripts/validate-repo-quality-gates.sh`; `docs/05.operations/README.md` | New or missing operations buckets or wrong template links could weaken SDD stage routing | Medium | improvement | P1 |

### Implementation Plan Delta

| Priority | Action type | Target | Change | Linked task | Verification | Rollback |
| --- | --- | --- | --- | --- | --- | --- |
| P1 | guardrail | `docs/05.operations/README.md`; `scripts/validate-repo-quality-gates.sh` | Add `Operations Routing Matrix` heading and validate required buckets, routing row order, target links, and template links for guides, policies, runbooks, incidents, and postmortems | T-142 through T-144 | repo quality, wiki check, shell syntax | Revert README and validator edits |
| P1 | evidence | 006 Spec/Plan/Task/progress | Record VAL-SPC-006-031 and verification | T-145, T-146 | repo quality and wiki check | Revert overlay entries |

### Verification Result

| Command or method | Result | Notes |
| --- | --- | --- |
| `bash scripts/validate-repo-quality-gates.sh .` | PASS | New operations routing matrix and bucket/template guardrail passed |
| `bash -n scripts/validate-repo-quality-gates.sh` | PASS | Validator shell syntax after guardrail edit |
| `bash scripts/generate-llm-wiki-index.sh --check` | PASS | Generated reference index unchanged |
| `git diff --check` | PASS | No whitespace errors |

## GitOps Coverage Matrix Guardrail Overlay - 2026-05-26

### Intent and Boundary

This overlay follows the continuation audit for implemented infrastructure
under `gitops/`. It keeps the change documentation/governance and repo-static:
no Kubernetes resource semantics, AppProject permissions, ApplicationSet
behavior, ArgoCD sync state, live cluster state, secret policy, or CI job
structure are changed.

### Gap Table

| Area | Gap | Evidence path | Impact | Risk | Action type | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| GitOps coverage SSoT | `gitops/README.md` documented a Service Coverage Matrix, but the repo quality gate did not verify that rows match actual `clusters/local`, `apps/root`, `platform/*`, and `workloads/*` directories | `gitops/README.md`; `gitops/` | Platform component additions, removals, or renames could silently drift from the entrypoint README | Medium | improvement | P1 |
| Workload coverage SSoT | `gitops/workloads/README.md` documented workload coverage, but the repo quality gate did not verify row coverage or expected validation commands | `gitops/workloads/README.md`; `gitops/workloads/` | ApplicationSet-scanned workload onboarding could miss README and validation command updates | Medium | improvement | P1 |

### Implementation Plan Delta

| Priority | Action type | Target | Change | Linked task | Verification | Rollback |
| --- | --- | --- | --- | --- | --- | --- |
| P1 | guardrail | `gitops/README.md`; `gitops/workloads/README.md`; `scripts/validate-repo-quality-gates.sh` | Validate GitOps service/workload coverage matrix headers, exact row order, actual directory existence, ownership text, and expected validation command references | T-147 through T-149 | repo quality, GitOps structure, manifest checks, wiki check | Revert README and validator edits |
| P1 | evidence | 006 Spec/Plan/Task/progress | Record VAL-SPC-006-032 and verification | T-150, T-151 | repo quality and wiki check | Revert overlay entries |

### Verification Result

| Command or method | Result | Notes |
| --- | --- | --- |
| `bash scripts/validate-repo-quality-gates.sh .` | PASS | New GitOps service/workload coverage matrix guardrail passed |
| `bash -n scripts/validate-repo-quality-gates.sh` | PASS | Validator shell syntax after guardrail edit |
| `bash scripts/validate-gitops-structure.sh` | PASS | Root Application, apps ApplicationSet, root app manifest count, and Kustomize completeness checks passed |
| `bash scripts/validate-k8s-manifests.sh .` | PASS | YAML syntax passed for 104 files; optional `kube-linter` skipped locally because it is not installed |
| `bash scripts/check-secret-handling.sh .` | PASS | Plaintext secret scan passed |
| `bash infrastructure/tests/verify-contracts-static.sh` | PASS | Static infrastructure/GitOps contracts passed |
| `bash scripts/generate-llm-wiki-index.sh --check` | PASS | Generated reference index unchanged |
| `find infrastructure scripts .claude/hooks -type f -name '*.sh' -exec bash -n {} +` | PASS | Shell syntax for infrastructure, scripts, and hooks |
| `git diff --check` | PASS | No whitespace errors |

## Infrastructure Coverage Matrix Guardrail Overlay - 2026-05-26

### Intent and Boundary

This overlay follows the continuation audit for implemented infrastructure
under `infrastructure/`. It keeps the change documentation/governance and
repo-static: no bootstrap behavior, Kubernetes resource semantics, live cluster
state, kubeconfig TLS trust, secret policy, external service state, or CI job
structure are changed.

### Gap Table

| Area | Gap | Evidence path | Impact | Risk | Action type | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| Infrastructure coverage SSoT | `infrastructure/README.md` documented an Infrastructure Coverage Matrix, but the repo quality gate did not verify that rows match actual bootstrap/runtime-support entrypoints | `infrastructure/README.md`; `infrastructure/` | Infrastructure entrypoint additions, removals, or renames could silently drift from the README | Medium | improvement | P1 |
| Bootstrap/runtime-support boundary evidence | The coverage matrix named responsibilities, but the reusable gate did not require ownership and validation/operation evidence per row | `infrastructure/README.md`; `scripts/validate-repo-quality-gates.sh` | Bootstrap-only and live-runtime support boundaries could become less explicit over time | Medium | improvement | P1 |

### Implementation Plan Delta

| Priority | Action type | Target | Change | Linked task | Verification | Rollback |
| --- | --- | --- | --- | --- | --- | --- |
| P1 | guardrail | `infrastructure/README.md`; `scripts/validate-repo-quality-gates.sh`; `scripts/README.md` | Validate Infrastructure Coverage Matrix header, exact entrypoint order, file/directory existence, ownership text, and validation/operation evidence | T-152 through T-154 | repo quality, static contracts, shell syntax, wiki check | Revert README and validator edits |
| P1 | evidence | 006 Spec/Plan/Task/progress | Record VAL-SPC-006-033 and verification | T-155, T-156 | repo quality and wiki check | Revert overlay entries |

### Verification Result

| Command or method | Result | Notes |
| --- | --- | --- |
| `bash scripts/validate-repo-quality-gates.sh .` | PASS | New Infrastructure Coverage Matrix guardrail passed |
| `bash -n scripts/validate-repo-quality-gates.sh` | PASS | Validator shell syntax after guardrail edit |
| `bash scripts/validate-gitops-structure.sh` | PASS | Root Application, apps ApplicationSet, root app manifest count, and Kustomize completeness checks passed |
| `bash scripts/validate-k8s-manifests.sh .` | PASS | YAML syntax passed for 104 files; optional `kube-linter` skipped locally because it is not installed |
| `bash scripts/check-secret-handling.sh .` | PASS | Plaintext secret scan passed |
| `bash infrastructure/tests/verify-contracts-static.sh` | PASS | Static infrastructure/GitOps contracts passed |
| `bash scripts/generate-llm-wiki-index.sh --check` | PASS | Generated reference index unchanged |
| `find infrastructure scripts .claude/hooks -type f -name '*.sh' -exec bash -n {} +` | PASS | Shell syntax for infrastructure, scripts, and hooks |
| `git diff --check` | PASS | No whitespace errors |

## Operations Incidents Boundary Guardrail Overlay - 2026-05-26

### Intent and Boundary

This overlay follows the continuation audit for `docs/05.operations/`. It keeps
the change documentation/governance and repo-static: no incident record,
postmortem, placeholder incident directory, live cluster state, GitOps manifest,
secret policy, external service state, or CI job structure is created or
changed.

### Gap Table

| Area | Gap | Evidence path | Impact | Risk | Action type | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| Incident/postmortem routing | `docs/05.operations/incidents/README.md` described incident and postmortem paths, but the repo quality gate did not validate the path/template/creation boundary | `docs/05.operations/incidents/README.md`; `scripts/validate-repo-quality-gates.sh` | Future incident records or postmortems could be routed outside the intended stage shape | Medium | improvement | P1 |
| No-incident state | The current no-incident state was documented but not reusable-gate enforced | `docs/05.operations/incidents/README.md`; `docs/05.operations/incidents/` | Placeholder incident directories or stale README state could appear without review | Low | improvement | P1 |

### Implementation Plan Delta

| Priority | Action type | Target | Change | Linked task | Verification | Rollback |
| --- | --- | --- | --- | --- | --- | --- |
| P1 | guardrail | `docs/05.operations/incidents/README.md`; `scripts/validate-repo-quality-gates.sh`; `scripts/README.md` | Add and validate Incident Boundary Matrix rows for incident records and postmortems, template links, creation rules, and current no-incident state | T-157 through T-159 | repo quality, wiki check, shell syntax | Revert README and validator edits |
| P1 | evidence | 006 Spec/Plan/Task/progress | Record VAL-SPC-006-034 and verification | T-160, T-161 | repo quality and wiki check | Revert overlay entries |

### Verification Result

| Command or method | Result | Notes |
| --- | --- | --- |
| `bash scripts/validate-repo-quality-gates.sh .` | PASS | New operations incidents boundary guardrail passed |
| `bash -n scripts/validate-repo-quality-gates.sh` | PASS | Validator shell syntax after guardrail edit |
| `bash scripts/validate-gitops-structure.sh` | PASS | Root Application, apps ApplicationSet, root app manifest count, and Kustomize completeness checks passed |
| `bash scripts/validate-k8s-manifests.sh .` | PASS | YAML syntax passed for 104 files; optional `kube-linter` skipped locally because it is not installed |
| `bash scripts/check-secret-handling.sh .` | PASS | Plaintext secret scan passed |
| `bash infrastructure/tests/verify-contracts-static.sh` | PASS | Static infrastructure/GitOps contracts passed |
| `bash scripts/generate-llm-wiki-index.sh --check` | PASS | Generated reference index unchanged |
| `find infrastructure scripts .claude/hooks -type f -name '*.sh' -exec bash -n {} +` | PASS | Shell syntax for infrastructure, scripts, and hooks |
| `git diff --check` | PASS | No whitespace errors |

## WSL2 Runtime Prerequisite Guardrail Overlay

This overlay follows the continuation audit for WSL2 and Docker prerequisites.
It keeps the change documentation/governance and repo-static: no kubeconfig,
Docker context, k3d cluster, port binding, external service, or live runtime
state is changed in this pass.

### Gap Delta

| Area | Gap | Evidence path | Impact | Risk | Action type | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| WSL2 prerequisite SSoT | WSL2, WSL-native Docker, k3d, kubectl, kubeconfig/TLS, port, and WSL networking prerequisites were spread across bootstrap docs and runtime notes without one reusable matrix guarded by repo-quality validation | `infrastructure/README.md`; `docs/05.operations/guides/0001-wsl-k3d-argocd-bootstrap-guide.md`; `docs/05.operations/guides/0002-wsl2-k3d-argocd-ha-setup-guide.md`; `docs/05.operations/runbooks/0001-argocd-platform-bootstrap-runbook.md` | Operators could miss which checks are repo SSoT, which are live evidence, and which failures remain operator-owned | Medium | improvement | P1 |
| TLS and networking failure boundary | The kubeconfig `x509` blocker and Windows/WSL networking ownership were documented in prose, but not validated as part of the infrastructure prerequisite contract | `infrastructure/README.md`; `scripts/validate-repo-quality-gates.sh` | Static success could be mistaken for live readiness or automatic kubeconfig/network repair | Medium | supplementation | P1 |

### Implementation Plan Delta

| Priority | Action type | Target | Change | Linked task | Verification | Rollback |
| --- | --- | --- | --- | --- | --- | --- |
| P1 | guardrail | `infrastructure/README.md`; `scripts/validate-repo-quality-gates.sh`; `scripts/README.md` | Add and validate WSL2 Runtime Prerequisite Matrix rows for Docker context, k3d/kubectl context, kubeconfig/TLS trust, port/network contracts, and WSL networking constraints | T-172 through T-174 | repo quality, static contracts, shell syntax, wiki check | Revert README and validator edits |
| P1 | evidence | 006 Spec/Plan/Task/progress | Record VAL-SPC-006-037 and verification | T-175, T-176 | repo quality and wiki check | Revert overlay entries |

### Verification Result

| Command or method | Result | Notes |
| --- | --- | --- |
| `bash scripts/validate-repo-quality-gates.sh .` | PASS | New WSL2 Runtime Prerequisite Matrix guardrail passed |
| `bash -n scripts/validate-repo-quality-gates.sh` | PASS | Validator shell syntax after guardrail edit |
| `bash infrastructure/tests/verify-contracts-static.sh` | PASS | Static infrastructure/GitOps contracts passed |
| `bash scripts/generate-llm-wiki-index.sh --check` | PASS | Generated reference index unchanged |
| `bash scripts/validate-gitops-structure.sh` | PASS | Root Application, apps ApplicationSet, root app manifest count, and Kustomize completeness checks passed |
| `bash scripts/validate-k8s-manifests.sh .` | PASS | YAML syntax passed for 104 files; optional `kube-linter` skipped locally because it is not installed |
| `bash scripts/check-secret-handling.sh .` | PASS | Plaintext secret scan passed |
| `find infrastructure scripts .claude/hooks -type f -name '*.sh' -exec bash -n {} +` | PASS | Shell syntax for infrastructure, scripts, and hooks |
| JSON parse for `.claude/settings.json` and `.codex/hooks.json` | PASS | Agent runtime JSON parsed |
| workflow YAML parse for `.github/workflows/*.yml` | PASS | Parsed 5 workflow files |
| `.env.example` vs `.env` key-name-only comparison | PASS | 18 key names matched; values were not printed |
| `git diff --check` | PASS | No whitespace errors |

## Examples Role Matrix Guardrail Overlay

This overlay follows the continuation audit for `examples/`. It keeps the
change documentation/governance and repo-static: no sample manifest,
cloud-reference manifest, GitOps workload, provider contract, or live runtime
state is changed in this pass.

### Gap Delta

| Area | Gap | Evidence path | Impact | Risk | Action type | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| Examples role SSoT | `examples/README.md` described `sample-app/` as a minimal onboarding template and AWS/Azure as reference snapshots, but the reusable gate did not validate an explicit role matrix | `examples/README.md`; `scripts/validate-repo-quality-gates.sh` | Example directories could drift into active desired-state or provider-latest claims without repo-static failure | Medium | improvement | P1 |
| Sample app vs active reference | `examples/sample-app/README.md` named `gitops/workloads/adminer/` as the fuller active reference, but no gate checked that the sample file set stayed minimal and adminer retained the richer reference files | `examples/sample-app/README.md`; `gitops/workloads/adminer/`; `scripts/validate-repo-quality-gates.sh` | Onboarding examples could accidentally look like the active workload SSoT or lose the active comparison path | Medium | improvement | P1 |

### Implementation Plan Delta

| Priority | Action type | Target | Change | Linked task | Verification | Rollback |
| --- | --- | --- | --- | --- | --- | --- |
| P1 | guardrail | `examples/README.md`; `scripts/validate-repo-quality-gates.sh`; `scripts/README.md` | Add and validate Example Role Matrix rows for `sample-app/`, `aws/`, and `azure/`, including reference-only/provider-snapshot boundaries and expected validation commands | T-167 through T-169 | repo quality, manifest syntax, secret scan, wiki check | Revert README and validator edits |
| P1 | evidence | 006 Spec/Plan/Task/progress | Record VAL-SPC-006-036 and verification | T-170, T-171 | repo quality and wiki check | Revert overlay entries |

### Verification Result

| Command or method | Result | Notes |
| --- | --- | --- |
| `bash scripts/validate-repo-quality-gates.sh .` | PASS | New examples role matrix and sample-app/adminer boundary guardrail passed |
| `bash -n scripts/validate-repo-quality-gates.sh` | PASS | Validator shell syntax after guardrail edit |
| `bash scripts/validate-k8s-manifests.sh .` | PASS | YAML syntax passed for 104 files; optional `kube-linter` skipped locally because it is not installed |
| `bash scripts/check-secret-handling.sh .` | PASS | Plaintext secret scan passed |
| `bash scripts/generate-llm-wiki-index.sh --check` | PASS | Generated reference index unchanged |
| `bash scripts/validate-gitops-structure.sh` | PASS | Root Application, apps ApplicationSet, root app manifest count, and Kustomize completeness checks passed |
| `bash infrastructure/tests/verify-contracts-static.sh` | PASS | Static infrastructure/GitOps contracts passed |
| `find infrastructure scripts .claude/hooks -type f -name '*.sh' -exec bash -n {} +` | PASS | Shell syntax for infrastructure, scripts, and hooks |
| JSON parse for `.claude/settings.json` and `.codex/hooks.json` | PASS | Agent runtime JSON parsed |
| workflow YAML parse for `.github/workflows/*.yml` | PASS | Parsed 5 workflow files |
| `.env.example` vs `.env` key-name-only comparison | PASS | 18 key names matched; values were not printed |
| `git diff --check` | PASS | No whitespace errors |

## GitHub Workflow Responsibility Matrix Guardrail Overlay

This overlay follows the continuation audit for QA/CI-CD governance. It keeps
the change documentation/governance and repo-static: no workflow job structure,
branch policy, deploy command, publish command, or GitHub remote setting is
changed.

### Gap Delta

| Area | Gap | Evidence path | Impact | Risk | Action type | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| GitHub workflow responsibility SSoT | `.github/ABOUT.md` described workflow roles in prose, but did not have a guarded matrix tied to the actual `.github/workflows/*.yml` inventory | `.github/ABOUT.md`; `.github/workflows/` | New workflow files could appear without clear QA/release/maintenance ownership and boundary text | Medium | improvement | P1 |
| QA/CD boundary evidence | Repo quality parsed workflow YAML and CI jobs, but did not protect the human-facing no-deploy/no-live-mutation workflow role summary | `scripts/validate-repo-quality-gates.sh`; `.github/ABOUT.md` | Maintenance automation could be mistaken for QA gates or deploy CD if documentation drifts | Medium | supplementation | P1 |

### Implementation Plan Delta

| Priority | Action type | Target | Change | Linked task | Verification | Rollback |
| --- | --- | --- | --- | --- | --- | --- |
| P1 | guardrail | `.github/ABOUT.md`; `scripts/validate-repo-quality-gates.sh`; `scripts/README.md` | Add and validate Workflow Responsibility Matrix rows for `ci.yml`, `generate-changelog.yml`, `greetings.yml`, `labeler.yml`, and `stale.yml`, including role, trigger/scope, evidence, and no-deploy/no-live-mutation boundaries | T-192 through T-194 | repo quality, workflow YAML parse, shell syntax, wiki check | Revert ABOUT and validator edits |
| P1 | evidence | 006 Spec/Plan/Task/progress | Record VAL-SPC-006-041 and verification | T-195, T-196 | repo quality and wiki check | Revert overlay entries |

### Verification Result

| Command or method | Result | Notes |
| --- | --- | --- |
| `bash scripts/validate-repo-quality-gates.sh .` | PASS | New Workflow Responsibility Matrix guardrail passed |
| `bash -n scripts/validate-repo-quality-gates.sh` | PASS | Validator shell syntax after guardrail edit |
| workflow YAML parse for `.github/workflows/*.yml` | PASS | Parsed 5 workflow files |
| `bash scripts/generate-llm-wiki-index.sh --check` | PASS | Generated reference index unchanged |
| `git diff --check` | PASS | No whitespace errors |

## Bootstrap Boundary Matrix Guardrail Overlay

This overlay follows the continuation audit for P0-17 bootstrap boundaries. It
keeps the change documentation/governance and repo-static: no cluster is
created, no ArgoCD install is run, no root app is applied, no secret is read,
and no external runtime state is changed.

### Gap Delta

| Area | Gap | Evidence path | Impact | Risk | Action type | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| Bootstrap boundary SSoT | k3d creation, ArgoCD installation, root app application, Vault connection, and PostgreSQL/Valkey connection boundaries were documented in prose across bootstrap docs, but not consolidated in a guarded matrix | `infrastructure/README.md`; `infrastructure/bootstrap-local.sh`; `docs/05.operations/runbooks/0001-argocd-platform-bootstrap-runbook.md`; `gitops/README.md` | Operators and agents could confuse bootstrap-only exceptions with normal GitOps operation | Medium | improvement | P1 |
| Verification coverage | Static gates checked contracts and GitOps structure, but repo-quality did not protect the human-facing bootstrap/operator responsibility matrix | `scripts/validate-repo-quality-gates.sh`; `infrastructure/README.md` | Future docs could weaken bootstrap/live mutation boundaries while static manifests still pass | Medium | supplementation | P1 |

### Implementation Plan Delta

| Priority | Action type | Target | Change | Linked task | Verification | Rollback |
| --- | --- | --- | --- | --- | --- | --- |
| P1 | guardrail | `infrastructure/README.md`; `scripts/validate-repo-quality-gates.sh`; `scripts/README.md` | Add and validate Bootstrap Boundary Matrix rows for k3d cluster creation, ArgoCD installation, root app application, Vault connection, and PostgreSQL/Valkey connection responsibility boundaries | T-187 through T-189 | repo quality, static contracts, GitOps structure, manifest syntax, secret scan, shell syntax | Revert README and validator edits |
| P1 | evidence | 006 Spec/Plan/Task/progress | Record VAL-SPC-006-040 and verification | T-190, T-191 | repo quality and wiki check | Revert overlay entries |

### Verification Result

| Command or method | Result | Notes |
| --- | --- | --- |
| `bash scripts/validate-repo-quality-gates.sh .` | PASS | New Bootstrap Boundary Matrix guardrail passed |
| `bash -n scripts/validate-repo-quality-gates.sh` | PASS | Validator shell syntax after guardrail edit |
| `bash infrastructure/tests/verify-contracts-static.sh` | PASS | Static external service, Vault, AppProject, and workload contracts passed |
| `bash scripts/validate-gitops-structure.sh` | PASS | Root Application, apps ApplicationSet, root app manifest count, and Kustomize completeness checks passed |
| `bash scripts/validate-k8s-manifests.sh .` | PASS | YAML syntax passed for 104 files; optional `kube-linter` skipped locally because it is not installed |
| `bash scripts/check-secret-handling.sh .` | PASS | Plaintext secret scan passed |
| `bash scripts/generate-llm-wiki-index.sh --check` | PASS | Generated reference index unchanged |
| `git diff --check` | PASS | No whitespace errors |

## Secret Management Responsibility Matrix Guardrail Overlay

This overlay follows the continuation audit for P0-20 secret-management
responsibility. It keeps the change documentation/governance and repo-static:
no secret values are read, no Vault policy is changed, and no live
Kubernetes/Vault state is mutated.

### Gap Delta

| Area | Gap | Evidence path | Impact | Risk | Action type | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| Secret-management responsibility SSoT | ESO/Vault resources existed, but ClusterSecretStore, platform ExternalSecrets, ArgoCD target secrets, sample app ExternalSecret naming, owner boundaries, and value-handling rules were not consolidated in a guarded matrix | `gitops/platform/eso/`; `gitops/platform/argocd/`; `examples/sample-app/external-secret.yaml`; `gitops/README.md` | Operators could miss who owns Vault auth, target Secret naming, rotation, and app-secret enablement boundaries | Medium | improvement | P1 |
| Verification coverage | Static contracts and secret scans passed, but repo-quality did not protect the human-facing secret responsibility summary | `scripts/validate-repo-quality-gates.sh`; `scripts/check-secret-handling.sh`; `gitops/README.md` | Secret governance docs could drift while manifests still pass syntax and secret scans | Medium | supplementation | P1 |

### Implementation Plan Delta

| Priority | Action type | Target | Change | Linked task | Verification | Rollback |
| --- | --- | --- | --- | --- | --- | --- |
| P1 | guardrail | `gitops/README.md`; `scripts/validate-repo-quality-gates.sh`; `scripts/README.md` | Add and validate Secret Management Responsibility Matrix rows for `vault-backend`, platform PostgreSQL secret, ArgoCD Valkey secret, ArgoCD notifications secret, and optional sample app ExternalSecret | T-182 through T-184 | repo quality, static contracts, GitOps structure, manifest syntax, secret scan, shell syntax | Revert README and validator edits |
| P1 | evidence | 006 Spec/Plan/Task/progress | Record VAL-SPC-006-039 and verification | T-185, T-186 | repo quality and wiki check | Revert overlay entries |

### Verification Result

| Command or method | Result | Notes |
| --- | --- | --- |
| `bash scripts/validate-repo-quality-gates.sh .` | PASS | New Secret Management Responsibility Matrix guardrail passed |
| `bash -n scripts/validate-repo-quality-gates.sh` | PASS | Validator shell syntax after guardrail edit |
| `bash infrastructure/tests/verify-contracts-static.sh` | PASS | Static external service, Vault, AppProject, and workload contracts passed |
| `bash scripts/validate-gitops-structure.sh` | PASS | Root Application, apps ApplicationSet, root app manifest count, and Kustomize completeness checks passed |
| `bash scripts/validate-k8s-manifests.sh .` | PASS | YAML syntax passed for 104 files; optional `kube-linter` skipped locally because it is not installed |
| `bash scripts/check-secret-handling.sh .` | PASS | Plaintext secret scan passed |
| `bash scripts/generate-llm-wiki-index.sh --check` | PASS | Generated reference index unchanged |
| `git diff --check` | PASS | No whitespace errors |

## External Service Contract Matrix Guardrail Overlay

This overlay follows the continuation audit for P0-21 external service
contracts. It keeps the change documentation/governance and repo-static:
EndpointSlices, services, ExternalSecrets, Vault policy, `.env` values, and
external runtimes are not changed.

### Gap Delta

| Area | Gap | Evidence path | Impact | Risk | Action type | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| External service contract SSoT | PostgreSQL, Valkey, and Vault static contracts existed across manifests and tests, but host/service, port, database or Vault path, secret keys, TLS/CA ownership, rotation responsibility, namespace convention, and static/live verification were not consolidated in a guarded matrix | `gitops/platform/external-services/`; `gitops/platform/eso/`; `gitops/platform/argocd/argocd-external-valkey-secret.yaml`; `infrastructure/tests/verify-contracts-static.sh`; `gitops/README.md` | Operators could miss which contract attributes are owned here versus external-service or secret-management owners | Medium | improvement | P1 <!-- pragma: allowlist secret --> |
| Verification coverage | `verify-contracts-static.sh` checked concrete IP/port/secret contracts, but repo-quality did not protect the human-facing contract summary | `scripts/validate-repo-quality-gates.sh`; `gitops/README.md` | Future README drift could weaken documentation SSoT while static manifests still pass | Medium | supplementation | P1 |

### Implementation Plan Delta

| Priority | Action type | Target | Change | Linked task | Verification | Rollback |
| --- | --- | --- | --- | --- | --- | --- |
| P1 | guardrail | `gitops/README.md`; `scripts/validate-repo-quality-gates.sh`; `scripts/README.md` | Add and validate External Service Contract Matrix rows for Vault API, PostgreSQL write/read, and Valkey auth, covering host/service, port, database or Vault path, secret keys, TLS/CA responsibility, rotation owner, namespace convention, and verification command | T-177 through T-179 | repo quality, static contracts, GitOps structure, secret scan, shell syntax | Revert README and validator edits |
| P1 | evidence | 006 Spec/Plan/Task/progress | Record VAL-SPC-006-038 and verification | T-180, T-181 | repo quality and wiki check | Revert overlay entries |

### Verification Result

| Command or method | Result | Notes |
| --- | --- | --- |
| `bash scripts/validate-repo-quality-gates.sh .` | PASS | New External Service Contract Matrix guardrail passed |
| `bash -n scripts/validate-repo-quality-gates.sh` | PASS | Validator shell syntax after guardrail edit |
| `bash infrastructure/tests/verify-contracts-static.sh` | PASS | Static external service, Vault, AppProject, and workload contracts passed |
| `bash scripts/validate-gitops-structure.sh` | PASS | Root Application, apps ApplicationSet, root app manifest count, and Kustomize completeness checks passed |
| `bash scripts/validate-k8s-manifests.sh .` | PASS | YAML syntax passed for 104 files; optional `kube-linter` skipped locally because it is not installed |
| `bash scripts/check-secret-handling.sh .` | PASS | Plaintext secret scan passed |
| `bash scripts/generate-llm-wiki-index.sh --check` | PASS | Generated reference index unchanged |
| `git diff --check` | PASS | No whitespace errors after verification record update |

## Scripts Broad Reference Guardrail Overlay

This overlay follows the continuation audit for `scripts/`. It keeps the
change documentation/governance and repo-static: no script is deleted, renamed,
or consolidated in this pass.

### Gap Delta

| Area | Gap | Evidence path | Impact | Risk | Action type | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| Script deletion precheck | `scripts/README.md` required a broad reference sweep before script deletion or rename, but the reusable gate only checked the command-contract allowlist for dangling `scripts/*.sh` references | `scripts/README.md`; `scripts/validate-repo-quality-gates.sh` | Script deletion or rename could leave active references in historical, governance, operations, GitOps, infrastructure, or example text without a reusable failure | Medium | improvement | P1 |
| Retention evidence boundary | Broad references need to be checked for dangling links without turning every mention into Tier A/B retention evidence | `scripts/README.md` | Future cleanup could over-retain scripts because any reference is mistaken for preservation evidence | Low | supplementation | P1 |

### Implementation Plan Delta

| Priority | Action type | Target | Change | Linked task | Verification | Rollback |
| --- | --- | --- | --- | --- | --- | --- |
| P1 | guardrail | `scripts/validate-repo-quality-gates.sh`; `scripts/README.md` | Validate that every tracked text reference matching `scripts/*.sh` points to an existing script, while documenting that broad references are a deletion/rename safety net and not automatic Tier A/B retention evidence | T-162 through T-164 | repo quality, shell syntax, broad reference spot check | Revert validator and README wording |
| P1 | evidence | 006 Spec/Plan/Task/progress | Record VAL-SPC-006-035 and verification | T-165, T-166 | repo quality and wiki check | Revert overlay entries |

### Verification Result

| Command or method | Result | Notes |
| --- | --- | --- |
| `bash scripts/validate-repo-quality-gates.sh .` | PASS | New tracked script reference sweep guardrail passed |
| `bash -n scripts/validate-repo-quality-gates.sh` | PASS | Validator shell syntax after guardrail edit |
| tracked script reference spot check | PASS | 183 tracked `scripts/*.sh` references resolved to existing files |
| `bash scripts/generate-llm-wiki-index.sh --check` | PASS | Generated reference index unchanged |
| `bash scripts/validate-gitops-structure.sh` | PASS | Root Application, apps ApplicationSet, root app manifest count, and Kustomize completeness checks passed |
| `bash scripts/validate-k8s-manifests.sh .` | PASS | YAML syntax passed for 104 files; optional `kube-linter` skipped locally because it is not installed |
| `bash scripts/check-secret-handling.sh .` | PASS | Plaintext secret scan passed |
| `bash infrastructure/tests/verify-contracts-static.sh` | PASS | Static infrastructure/GitOps contracts passed |
| `find infrastructure scripts .claude/hooks -type f -name '*.sh' -exec bash -n {} +` | PASS | Shell syntax for infrastructure, scripts, and hooks |
| JSON parse for `.claude/settings.json` and `.codex/hooks.json` | PASS | Agent runtime JSON parsed |
| workflow YAML parse for `.github/workflows/*.yml` | PASS | Parsed 5 workflow files |
| `.env.example` vs `.env` key-name-only comparison | PASS | 18 key names matched; values were not printed |
| `git diff --check` | PASS | No whitespace errors |

## Related Documents

- **Spec**: [../../03.specs/006-workspace-harness-gap-analysis/spec.md](../../03.specs/006-workspace-harness-gap-analysis/spec.md)
- **Tasks**: [../tasks/2026-05-24-workspace-harness-gap-analysis.md](../tasks/2026-05-24-workspace-harness-gap-analysis.md)
- **P3 Plan**: [../plans/2026-05-24-p3-gitops-secret-runtime-remediation.md](../plans/2026-05-24-p3-gitops-secret-runtime-remediation.md)
- **P3 Task**: [../tasks/2026-05-24-p3-gitops-secret-runtime-remediation.md](../tasks/2026-05-24-p3-gitops-secret-runtime-remediation.md)
- **Harness Catalog**: [../../00.agent-governance/harness-catalog.md](../../00.agent-governance/harness-catalog.md)
- **Docs Stage Conformance Skill**: [../../../.claude/skills/docs-stage-conformance/skill.md](../../../.claude/skills/docs-stage-conformance/skill.md)
- **Workspace Harness Audit Skill**: [../../../.claude/skills/workspace-harness-audit/skill.md](../../../.claude/skills/workspace-harness-audit/skill.md)
- **Scripts README**: [../../../scripts/README.md](../../../scripts/README.md)
