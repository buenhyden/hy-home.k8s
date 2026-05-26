---
title: 'Workspace Harness Gap Analysis Technical Specification'
type: spec
status: active
owner: 'platform'
updated: 2026-05-26
---

# Workspace Harness Gap Analysis Technical Specification (Spec)

## Overview (KR)

이 문서는 `hy-home.k8s` 워크스페이스가 WSL2, WSL Linux native Docker, k3d,
ArgoCD GitOps, External Secrets, Vault, PostgreSQL, Valkey, SDD(Spec-Driven
Development), QA(Quality Assurance), CI/CD(Continuous Integration/Continuous
Delivery), AI Agent 협업 규칙을 일관되게 지탱하는지 감사하고 보강하는 기술 계약이다.

## Strategic Boundaries & Non-goals

This spec owns the repository-static improvement contract for the workspace
harness gap analysis. The original pass did not approve live cluster mutation,
direct ArgoCD sync, Vault writes, Kubernetes resource semantic changes, GitHub
branch protection changes, or plaintext secret handling.

On 2026-05-24 the human approved a separate P3 follow-up for ArgoCD, Vault,
External Secrets, secret, and runtime remediation. That approval allows
repository-backed desired-state changes and read-only runtime metadata checks
under the linked P3 plan. Direct live mutation, secret value inspection, Vault
KV writes, ArgoCD sync, and plaintext secret handling remain out of scope.

On 2026-05-25 the human approved a multi-area improvement overlay for the
workspace harness. That overlay allows low-risk README/status currentness fixes,
medium-risk validator and hook coverage improvements, and P3 precheck-only
records. Bulk deletion, live mutation, secret value inspection, CI ruleset
rewrites, and Kubernetes resource semantic changes remain out of scope for this
pass.

## Related Inputs

- **PRD**: N/A. This is a workspace governance and validation improvement.
- **ARD**: [../02.architecture/requirements/0001-wsl-k3d-argocd-platform.md](../../02.architecture/requirements/0001-wsl-k3d-argocd-platform.md)
- **Related ADRs**:
  [ADR-0002](../../02.architecture/decisions/0002-argocd-helm-and-gitops-model.md),
  [ADR-0003](../../02.architecture/decisions/0003-eso-vault-k8s-auth.md),
  [ADR-0004](../../02.architecture/decisions/0004-external-services-endpoints-and-valkey-backend.md)

## Contracts

- **Config Contract**: root gateway files remain thin; recurring workflow and
  task-to-skill routing are recorded in `docs/00.agent-governance/harness-catalog.md`.
- **Data / Interface Contract**: no new runtime API is introduced. New
  execution evidence lives in `docs/03.specs/`, `docs/04.execution/plans/`,
  `docs/04.execution/tasks/`, and `docs/00.agent-governance/memory/progress.md`.
- **Governance Contract**: all findings are classified as low, medium, or high
  risk. High-risk runtime, secret, ArgoCD, and CI/CD policy items are either
  deferred with explicit pre-checks or handled through a separate approved plan
  with its own verification and rollback record.

## Core Design

- **Component Boundary**: repository documentation, governance, validation
  scripts, and static GitOps checks only.
- **Key Dependencies**: existing subagent review results, repo templates,
  `scripts/validate-repo-quality-gates.sh`, `scripts/validate-gitops-structure.sh`,
  and static infrastructure tests.
- **Tech Stack**: Bash, Markdown, YAML, ArgoCD Application manifests, repo-local
  Claude/Codex harness files.

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**: Coverage Ledger, Integrated Gap Analysis,
  Implementation Plan, checklist gate, and Final Report are stored as Markdown
  tables in the linked plan and task documents.
- **Migration / Transition Plan**: no data migration is included. A temporary
  empty spec directory from the interrupted planning turn is reused by adding
  this `spec.md` file.

## Interfaces & Data Structures

### Core Interfaces

```text
Coverage Ledger -> Integrated Gap Analysis -> Implementation Plan -> Task evidence -> Verification summary
```

## API Contract (If Applicable)

Not applicable. This work does not expose an API.

## Agent Role & IO Contract (If Applicable)

- **Agent Role**: Codex implements the approved plan using previous subagent
  review outputs as investigation input.
- **Inputs**: six role-based review results, baseline static validation, repo
  governance documents, and the user-approved implementation plan.
- **Outputs**: updated spec/task/plan artifacts, scoped P1/P2 changes, deferred
  P3 follow-up records, and verification evidence.
- **Success Definition**: repository-static checks pass or limitations are
  recorded, and all high-risk items remain planned rather than silently omitted.

## Tools & Tool Contract (If Applicable)

- **Tool List**: `rg`, `find`, `bash`, `python3`, repo validation scripts.
- **Permission Boundary**: no live `kubectl`, ArgoCD, Vault, cloud, or secret
  value inspection is performed without explicit approval. Approved live checks
  are limited to metadata/status reads unless a follow-up explicitly authorizes
  mutation.
- **Failure Handling**: if repo-static validation fails, fix the scoped change
  or roll back the affected file set.

## Prompt / Policy Contract (If Applicable)

- **System / Instruction Contract**: `AGENTS.md` remains the thin gateway.
  Detailed workflow routing stays in governance docs.
- **Policy Constraints**: do not reduce scope, omit high-risk gaps, bypass
  safety gates, or implement high-risk runtime changes without a linked approval
  plan, verification method, and rollback path.
- **Versioning Rule**: this is a dated repository-static snapshot for
  2026-05-24 with a 2026-05-25 current-state overlay.

## Memory & Context Strategy (If Applicable)

- **Short-term Context**: previous subagent results and baseline command output.
- **Long-term Memory**: append a concise progress entry to
  `docs/00.agent-governance/memory/progress.md`.
- **Retrieval Boundary**: memory is supporting context; current repository files
  remain authoritative.

## Guardrails (If Applicable)

- **Input Guardrails**: compare prompt requests against repository governance
  before editing.
- **Output Guardrails**: all new authored documents must use the template
  contract and `Related Documents`.
- **Blocked Conditions**: direct live mutation, plaintext secret writes, or
  missing rollback path.
- **Escalation Rule**: high-risk runtime or policy decisions require human
  approval and a separate implementation plan.

## Evaluation (If Applicable)

- **Eval Types**: static repository validation and documentation conformance.
- **Metrics**: zero repo quality errors, generated LLM Wiki current, GitOps
  structure validation pass, manifest syntax pass, secret scan pass, static
  contract pass, shell syntax pass, diff whitespace pass.
- **Datasets / Fixtures**: existing repository files and manifests, plus a
  temporary `/tmp` negative fixture for quoted plaintext secret detection.
- **How to Run**: use the verification commands in the linked plan.

## Edge Cases & Error Handling

- **Empty root app set**: `scripts/validate-gitops-structure.sh` must fail when
  `gitops/apps/root` has no non-kustomization ArgoCD root app manifests.
- **Quoted plaintext secrets**: `scripts/check-secret-handling.sh` must flag
  quoted literal values for sensitive manifest keys while continuing to allow
  quoted placeholders such as `${TOKEN}`.
- **Local optional tools absent**: record skipped tools instead of treating them
  as passed.

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: high-risk GitOps or secret changes appear necessary.
- **Fallback**: defer the change and record pre-checks in the plan.
- **Human Escalation**: required for live k3d/ArgoCD/Vault mutation or runtime
  policy changes. The 2026-05-24 P3 follow-up approval covers repo-backed
  ArgoCD/Vault/ESO desired-state changes and read-only metadata checks only.

## Verification Commands

```bash
bash scripts/validate-repo-quality-gates.sh .
bash scripts/generate-llm-wiki-index.sh --check
bash scripts/validate-gitops-structure.sh
bash scripts/validate-k8s-manifests.sh .
bash scripts/check-secret-handling.sh .
bash infrastructure/tests/verify-contracts-static.sh
find infrastructure scripts .claude/hooks -type f -name '*.sh' -exec bash -n {} +
python3 -m json.tool .claude/settings.json
python3 -m json.tool .codex/hooks.json
git diff --check
```

## Success Criteria & Verification Plan

- **VAL-SPC-006-001**: Coverage Ledger, Integrated Gap Analysis, and
  Implementation Plan are recorded.
- **VAL-SPC-006-002**: P1/P2 scoped changes pass repo-static validation.
- **VAL-SPC-006-003**: P3 high-risk items are deferred with pre-checks and
  follow-up work.
- **VAL-SPC-006-004**: Required external `SKILL.md` paths are checked and
  missing paths, if any, are recorded as Gaps.
- **VAL-SPC-006-005**: Repeated broad workspace audit workflow is captured in a
  repo-local Skill or explicitly deferred with rationale.
- **VAL-SPC-006-006**: Hybrid refresh evidence preserves current role-based
  subagent results, path-level external skill checks, repo-static verification,
  and any new safe P1/P2 guardrail changes.
- **VAL-SPC-006-007**: Named additive review skills are recorded with applied,
  skipped, missing, or conflict status, and any design-only skill boundary is
  preserved in the linked plan/task.
- **VAL-SPC-006-008**: `superpowers:brainstorming` is applied as a design lens
  for initial-contract delta review, with alternatives, selected approach,
  skipped default design-doc gate rationale, implementation plan, and
  verification evidence preserved in canonical SDD artifacts.
- **VAL-SPC-006-009**: approved P3 ArgoCD/Vault/ESO secret/runtime remediation
  is implemented through repository desired-state changes, static contract
  validation, and read-only runtime metadata checks with unavailable-live-state
  results recorded instead of treated as passed.
- **VAL-SPC-006-010**: `gstack-plan-ceo-review` is applied as a HOLD SCOPE
  current-state review for first-input coverage drift, with exact named skill
  path evidence, P3 supersession status, implementation plan, and verification
  preserved in canonical SDD artifacts.
- **VAL-SPC-006-011**: `superpowers:executing-plans` is applied to the CEO
  review plan delta, with plan load/review/execution, required sub-skill path
  evidence, verification, and finish boundary preserved in canonical SDD
  artifacts.
- **VAL-SPC-006-012**: `skill-creator`, `skillify`, `skill-developer`, and
  `skill-improver` are applied as skill-quality lenses for the repo-local
  `workspace-harness-audit` Skill, with not-applicable boundaries and skipped
  automated reviewer limits recorded.
- **VAL-SPC-006-013**: repeated docs-stage conformance work found in current
  task evidence and Codex memory is implemented as the repo-local
  `docs-stage-conformance` Skill, registered in the harness catalog, and
  verified without creating unrelated browser-skill artifacts.
- **VAL-SPC-006-014**: 2026-05-25 multi-area overlay records P1 README/status
  currentness, P2 quoted plaintext secret scanning and hook manifest coverage
  clarification, P3 precheck-only boundaries, verification results, and
  cleanup/deletion deferrals in canonical SDD artifacts.
- **VAL-SPC-006-015**: 2026-05-25 P0 mandatory workstream revalidation records
  full target inventory, five fresh read-only subagent reviews, P0 coverage and
  gap decisions, T-049+ task linkage, safe P1/P2 implementation, P3 deferrals,
  verification results, and final report without creating a parallel docs tree.
- **VAL-SPC-006-016**: 2026-05-25 authored SSoT large-scale overlay preserves
  the external `P0-01` through `P0-22` identifiers in the existing 006 Plan and
  Task, maps each ID to repo-local evidence and implementation or deferral
  status, records six read-only subagent findings, and keeps live runtime,
  secret value, CI ruleset, Kubernetes semantic, and bulk deletion work
  deferred unless separately approved.
- **VAL-SPC-006-017**: 2026-05-25 deferred item repo-static improvement overlay
  resolves safe documentation and policy drift for EndpointSlice ownership,
  Traefik port wording, CI gate naming, OPA/Conftest feasibility, Vault
  endpoint role separation, script deletion prechecks, and `.agents` mirror
  status without changing runtime interfaces, secrets, CI workflow structure, or
  live cluster state.
- **VAL-SPC-006-018**: 2026-05-25 task-unit commit follow-up records published
  broad commit `870febd` as a forward-only historical exception, strengthens
  lifecycle hook guidance for dirty states that span multiple logical units, and
  preserves task-unit staging and `git diff --cached` review as the required
  path for future human-requested commits without rewriting public history.
- **VAL-SPC-006-019**: 2026-05-25 approval-bound completion audit records fresh
  read-only runtime and GitHub remote evidence, keeps unavailable live k3d state
  as a current-state limitation, and remediates the discovered CI version
  inventory drift for `actions/stale` without direct main-branch bypass.
- **VAL-SPC-006-020**: 2026-05-25 post-merge completion audit records PR #39
  merged into `main`, verifies the merge commit's CI and local static gates,
  and keeps live bootstrap/runtime proof deferred because approved prechecks
  show Vault, PostgreSQL, and Valkey are currently unreachable.
- **VAL-SPC-006-021**: 2026-05-25 live bootstrap runtime closure records the
  approved external-service startup, k3d bootstrap, Vault Kubernetes auth
  repair, EndpointSlice bootstrap boundary correction, MetalLB/Traefik
  validation fixes, and successful `infrastructure/tests/run-all.sh` evidence
  without printing secret values or rewriting public history.
- **VAL-SPC-006-022**: 2026-05-25 documentation/governance-first overlay
  records six fresh read-only subagent reviews, external `P0-01` through
  `P0-22` coverage, Integrated Gap Analysis, Implementation Plan, Checklist
  Gate, Final Report, safe P1 documentation/governance edits, duplicate skill
  deferrals, and the live kubeconfig TLS blocker without changing Kubernetes
  semantics, AppProject permissions, CI job structure, secret policy, live
  cluster state, or `.env` values.
- **VAL-SPC-006-023**: 2026-05-25 unreviewed-area follow-up rechecks
  `scripts/`, `gitops/`, `infrastructure/`, and `docs/05.operations/` against
  current files, strengthens weak evidence for script deletion/consolidation,
  GitOps hardening deferrals, infrastructure live-check TLS diagnostics, and
  operations index freshness, then verifies the resulting static and targeted
  checks without changing GitOps semantics, live state, secrets, CI job
  topology, or `.env` values.
- **VAL-SPC-006-024**: 2026-05-25 residual objective completion audit rechecks
  the remaining broad workspace axes: `traefik/`, `examples/`, `.env` key
  parity, QA/CI files, agent governance, repo-local Skills, bootstrap and WSL2
  boundaries, secret-management responsibility, external-service contracts, and
  documentation SSoT ownership. It records that no additional safe semantic
  implementation is introduced in this pass; current changes are limited to
  evidence in the existing 006 SDD chain and fresh verification records.
- **VAL-SPC-006-025**: 2026-05-25 operations index guardrail follow-up aligns
  `docs/05.operations/{guides,policies,runbooks}/README.md` index status/date
  rows with document frontmatter and extends `validate-repo-quality-gates.sh`
  to fail on future operations index/frontmatter drift.
- **VAL-SPC-006-026**: 2026-05-25 scripts inventory guardrail follow-up
  strengthens the `scripts/` deletion/consolidation review by validating that
  every tracked shell script is executable, uses the expected Bash shebang, has
  exactly one `scripts/README.md` inventory row, has an explicit decision, and
  cites Tier A or Tier B retention evidence when the decision is `Keep`.
- **VAL-SPC-006-027**: 2026-05-25 environment key contract guardrail
  follow-up strengthens `.env.example` and local `.env` role/key consistency by
  validating that `.env` remains ignored/untracked, `.env.example` has unique
  keys, and local `.env` key names match `.env.example` when `.env` exists,
  without printing or recording values.
- **VAL-SPC-006-028**: 2026-05-25 GitOps hierarchy guardrail follow-up
  strengthens root Application, platform App-of-Apps, and workload
  ApplicationSet separation by validating that `root-platform` owns
  `gitops/apps/root`, `apps-generator` owns `gitops/workloads/*`, required
  cluster overlay resources remain present, root app manifests use the
  `platform` project, and local root app source paths stay under
  `gitops/platform/` or `gitops/clusters/local` without changing Kubernetes
  resource semantics or AppProject permissions.
- **VAL-SPC-006-029**: 2026-05-25 infrastructure test inventory guardrail
  follow-up strengthens `infrastructure/` review by adding an
  `infrastructure/tests/*.sh` inventory to `infrastructure/README.md` and
  validating executable bits, Bash shebangs, exact inventory coverage, nonempty
  preconditions/result semantics/retention surfaces, and `run-all.sh` live-test
  call parity without executing live cluster mutations or repairing kubeconfig
  TLS state.
- **VAL-SPC-006-030**: 2026-05-25 Traefik route inventory guardrail follow-up
  strengthens `traefik/` review by adding a route inventory for each dynamic
  config and validating README coverage, router host rules, `websecure`
  entrypoints, TLS presence, service transport, backend URL
  `https://172.18.0.240:443`, and stale backend absence in both active Traefik
  configs and the sample app Traefik example without changing live gateway
  state.
- **VAL-SPC-006-031**: 2026-05-25 operations routing matrix guardrail
  follow-up strengthens `docs/05.operations/` normalization by making the
  stage-level routing table explicit and validating required operations buckets,
  routing row order, target links, and template links for guides, policies,
  runbooks, incident records, and postmortems without changing authored
  operations content semantics.
- **VAL-SPC-006-032**: 2026-05-26 GitOps coverage matrix guardrail follow-up
  strengthens `gitops/` review by validating that `gitops/README.md` Service
  Coverage Matrix and `gitops/workloads/README.md` Workload Coverage Matrix
  stay synchronized with actual `clusters/local`, `apps/root`, `platform/*`,
  and `workloads/*` directories and cite the expected validation commands
  without changing Kubernetes resource semantics, AppProject permissions,
  ApplicationSet behavior, or live cluster state.
- **VAL-SPC-006-033**: 2026-05-26 infrastructure coverage matrix guardrail
  follow-up strengthens `infrastructure/` review by validating that
  `infrastructure/README.md` Infrastructure Coverage Matrix stays synchronized
  with actual `argocd/`, `k3d/`, `tests/`, `vault/`, `bootstrap-local.sh`,
  `ipaddresspool.yaml`, and `l2advertisement.yaml` entrypoints and names
  ownership plus validation or operation evidence without changing bootstrap
  behavior, live cluster state, kubeconfig TLS trust, or Kubernetes resource
  semantics.
- **VAL-SPC-006-034**: 2026-05-26 operations incidents boundary guardrail
  follow-up strengthens `docs/05.operations/` normalization by validating the
  incident record and postmortem path/template/creation boundary in
  `docs/05.operations/incidents/README.md` and the current no-incident state
  without creating placeholder incident directories, authored incident records,
  or postmortems.
- **VAL-SPC-006-035**: 2026-05-26 scripts broad reference guardrail follow-up
  strengthens the `scripts/` deletion/consolidation review by validating that
  every tracked text reference matching `scripts/*.sh` points to an existing
  script while keeping broad references separate from Tier A/B retention
  evidence.
- **VAL-SPC-006-036**: 2026-05-26 examples role matrix guardrail follow-up
  strengthens `examples/` freshness by validating the `sample-app/`, `aws/`,
  and `azure/` role matrix, keeping `sample-app/` as a minimal onboarding
  template, and preserving `gitops/workloads/adminer/` as the fuller active
  workload reference without changing sample manifests or provider contracts.
- **VAL-SPC-006-037**: 2026-05-26 WSL2 runtime prerequisite guardrail
  follow-up strengthens WSL2 + WSL Linux native Docker readiness by validating
  a single infrastructure prerequisite matrix for Docker context, k3d/kubectl
  context, kubeconfig/TLS trust, local port/network contracts, and WSL
  networking constraints without switching contexts, repairing kubeconfig, or
  mutating live runtime state.
- **VAL-SPC-006-038**: 2026-05-26 external service contract matrix guardrail
  follow-up strengthens PostgreSQL/Valkey/Vault interface SSoT by validating
  host/service, port, database or Vault path, secret keys, TLS/CA ownership,
  rotation responsibility, namespace convention, and static/live verification
  pointers without changing EndpointSlices, secret policy, `.env` values, or
  external runtime state.
- **VAL-SPC-006-039**: 2026-05-26 secret management responsibility matrix
  guardrail follow-up strengthens ESO/Vault responsibility by validating the
  ClusterSecretStore, platform ExternalSecrets, ArgoCD target secrets, sample
  app ExternalSecret naming, owner boundaries, value-handling rule, and
  static/live verification pointers without reading secret values, changing
  Vault policy, or mutating live Kubernetes/Vault state.
- **VAL-SPC-006-040**: 2026-05-26 bootstrap boundary matrix guardrail
  follow-up strengthens repository/operator responsibility separation by
  validating k3d cluster creation, ArgoCD installation, root app application,
  Vault connection, and PostgreSQL/Valkey connection boundaries without
  creating clusters, installing ArgoCD, applying resources, reading secrets, or
  mutating live external services.
- **VAL-SPC-006-041**: 2026-05-26 GitHub workflow responsibility matrix
  guardrail follow-up strengthens QA/CI-CD SSoT by validating that
  `.github/ABOUT.md` lists every workflow, separates required QA gates from
  release-evidence and maintenance automation, and preserves no-deploy/no-live
  mutation boundaries without changing workflow job structure.
- **VAL-SPC-006-042**: 2026-05-26 app onboarding secret path contract
  guardrail follow-up strengthens `docs/05.operations`, `examples/sample-app`,
  and `gitops/README.md` consistency by validating that active onboarding docs
  distinguish the Vault CLI path `secret/apps/<appname>/config` from the ESO
  `remoteRef.key` value `apps/<appname>/config`, without changing AppProject
  permissions, Vault policy, secret values, or live Kubernetes state.
- **VAL-SPC-006-043**: 2026-05-26 Vault policy write boundary guardrail
  follow-up strengthens `docs/05.operations` command safety by validating that
  `vault policy write` examples carry an external-secret, human-approved,
  operator-approved, or break-glass marker, without applying Vault policy,
  reading secret values, or mutating live Vault/Kubernetes state.
- **VAL-SPC-006-044**: 2026-05-26 Docker network and RBAC create command
  boundary guardrail follow-up strengthens operations command safety by
  validating that `docker network connect` and `kubectl create
  clusterrolebinding` examples carry human-approved, bootstrap, break-glass,
  operator-approved, or dry-run context, without mutating Docker networks or
  Kubernetes RBAC state.
- **VAL-SPC-006-045**: 2026-05-26 script classification matrix guardrail
  follow-up strengthens `scripts/` deletion and consolidation review evidence
  by validating that every active script is classified with the task-contract
  terms `one-off`, `reusable`, `operations-critical`, `development-helper`, or
  `unknown`, and that current active scripts remain non-deletion and
  non-consolidation candidates without deleting, renaming, or merging scripts.
- **VAL-SPC-006-046**: 2026-05-26 approved temporary-kubeconfig live validation
  follow-up strengthens WSL2/k3d runtime evidence by recording that the default
  kubeconfig still fails TLS trust, while a k3d-generated temporary kubeconfig
  proves the read-only live aggregate `infrastructure/tests/run-all.sh` passes
  without modifying `~/.kube/config`, Kubernetes resources, Docker networks, or
  secret values.
- **VAL-SPC-006-047**: 2026-05-26 approved default kubeconfig TLS repair
  follow-up strengthens WSL2/k3d runtime support by backing up `~/.kube/config`,
  merging the k3d `hyhome` kubeconfig into the default kubeconfig, and proving
  that default `kubectl version --request-timeout=5s` and
  `infrastructure/tests/run-all.sh` pass without changing repository manifests,
  Kubernetes resources, Docker networks, Vault policy, secret values, or `.env`
  values.
- **VAL-SPC-006-048**: 2026-05-26 approved Traefik 443 runtime proof follow-up
  strengthens Traefik boundary evidence by running
  `CHECK_TRAEFIK_443=true bash infrastructure/tests/verify-ingress-tls.sh`,
  recording the failure when no external Traefik gateway container is running,
  and keeping external gateway startup or dynamic-config application outside
  this repository's GitOps desired-state ownership.
- **VAL-SPC-006-049**: 2026-05-26 targeted residual-area audit follow-up
  rechecks `scripts/`, `gitops/`, `infrastructure/`, and `docs/05.operations/`
  against the current worktree, confirms no deletion-ready scripts and no safe
  GitOps/Kubernetes semantic changes in this pass, and strengthens the
  operations high-risk command boundary SSoT without mutating live cluster,
  external runtime, secret, `.env`, or Kubernetes desired-state semantics.
- **VAL-SPC-006-050**: 2026-05-26 GitOps image and workload-kind policy scan
  guardrail follow-up strengthens the previously deferred image tag and
  workload-kind scan by validating active `gitops/workloads/*` container images,
  raw `gitops/platform/*` pod template images, and workload manifest kind
  membership in the `apps` AppProject `namespaceResourceWhitelist`, while
  keeping AppProject allow-list tightening, `CreateNamespace=true` ownership,
  CI failure-mode changes, OPA/Conftest, kube-linter enforcement, live cluster
  state, and Kubernetes desired-state semantics deferred.
- **VAL-SPC-006-051**: 2026-05-26 GitOps namespace ownership guardrail
  follow-up strengthens the previously deferred `CreateNamespace=true`
  ownership review by validating current root Application, apps ApplicationSet,
  and platform root Application namespace surfaces against
  `gitops/platform/namespaces` owner manifests, while keeping actual sync option
  removal, AppProject `Namespace` allow-list changes, live reconciliation,
  bootstrap ordering changes, and Kubernetes desired-state semantics deferred.
- **VAL-SPC-006-052**: 2026-05-26 kube-linter optional boundary guardrail
  follow-up strengthens manifest QA SSoT by validating `.kube-linter.yaml`
  exclusion order, inline rationale comments, and the `scripts/README.md`
  Kube-linter Exclusion Matrix, while keeping kube-linter installation,
  mandatory local enforcement, CI failure-mode changes, and broader policy
  bundle work deferred.
- **VAL-SPC-006-053**: 2026-05-26 Traefik serverlb boundary guardrail
  follow-up rechecks the read-only Traefik 443 proof after default kubeconfig
  repair, records that `CHECK_TRAEFIK_443=true` still fails while Docker only
  shows `k3d-hyhome-serverlb` on host `:443`, and validates that
  `traefik/README.md` distinguishes the k3d server load balancer from the
  external `hy-home.docker` Traefik gateway without starting containers,
  applying dynamic config, or changing GitOps desired state.
- **VAL-SPC-006-054**: 2026-05-26 destructive Git permission hardening
  follow-up closes the agent-governance deferred item by adding shared Claude
  deny rules for destructive or history-rewriting Git commands, documenting the
  human-approved recovery exception path in `git-workflow.md`, and validating
  the deny list through `scripts/validate-repo-quality-gates.sh` without
  running destructive Git commands or changing GitHub branch protection.
- **VAL-SPC-006-055**: 2026-05-26 AppProject allow-list rationale guardrail
  follow-up advances the GitOps allow-list tightening deferral by documenting
  `apps` AppProject cluster, active workload, and reserved onboarding allow-list
  surfaces, validating those rows against live repository manifests and
  `gitops/clusters/local/appproject-apps.yaml`, and keeping actual kind removal
  or platform chart-managed allow-list tightening deferred until app onboarding,
  chart render, and ArgoCD sync impact reviews are complete.

## Related Documents

- **Plan**: [../../04.execution/plans/2026-05-24-workspace-harness-gap-analysis.md](../../04.execution/plans/2026-05-24-workspace-harness-gap-analysis.md)
- **P3 Plan**: [../../04.execution/plans/2026-05-24-p3-gitops-secret-runtime-remediation.md](../../04.execution/plans/2026-05-24-p3-gitops-secret-runtime-remediation.md)
- **Tasks**: [../../04.execution/tasks/2026-05-24-workspace-harness-gap-analysis.md](../../04.execution/tasks/2026-05-24-workspace-harness-gap-analysis.md)
- **P3 Tasks**: [../../04.execution/tasks/2026-05-24-p3-gitops-secret-runtime-remediation.md](../../04.execution/tasks/2026-05-24-p3-gitops-secret-runtime-remediation.md)
- **Harness Catalog**: [../../00.agent-governance/harness-catalog.md](../../00.agent-governance/harness-catalog.md)
- **Subagent Protocol**: [../../00.agent-governance/subagent-protocol.md](../../00.agent-governance/subagent-protocol.md)
- **Docs Stage Conformance Skill**: [../../../.claude/skills/docs-stage-conformance/skill.md](../../../.claude/skills/docs-stage-conformance/skill.md)
- **Workspace Harness Audit Skill**: [../../../.claude/skills/workspace-harness-audit/skill.md](../../../.claude/skills/workspace-harness-audit/skill.md)
- **Scripts README**: [../../../scripts/README.md](../../../scripts/README.md)
