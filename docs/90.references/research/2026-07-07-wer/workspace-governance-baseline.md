---
title: 'Reference: Workspace Governance Baseline Research'
type: content/reference
status: draft
owner: platform
updated: 2026-07-10
---

# Reference: Workspace Governance Baseline Research

## Overview

이 문서는 `hy-home.k8s` 워크스페이스의 거버넌스 baseline을 현재
repository evidence와 공식 OpenGitOps 원칙에 대조해 설명한다. 워크스페이스는
WSL2 + k3d 로컬 Kubernetes 홈랩, ArgoCD GitOps desired state, Stage 00~99
문서 체계, 그리고 사람과 AI가 공유하는 Spec-Driven Development(SDD) 협업
계약을 한 저장소에서 관리한다.

이 문서는 설명용 Stage 90 reference다. 활성 정책, CI semantics, provider
runtime behavior, release 승인, live-cluster 절차를 정의하거나 변경하지 않는다.

## Purpose

- 워크스페이스 목적과 GitOps-first operating contract를 current repo fact로
  요약한다.
- governance area별 canonical owner, local evidence, authority boundary를
  연결한다.
- instruction, preventive control, feedback evidence, knowledge store의 관계를
  하나의 enforcement map으로 보존한다.
- 현재 확인되는 governance gap을 severity와 canonical follow-up route가 있는
  비변경 recommendation으로 기록한다.

## Reference Type

- Type: durable-concept / source-ledger
- Source checked: 2026-07-10
- Refresh trigger: workspace purpose, Stage routing/lifecycle contract, agent roster,
  provider adapter, approval boundary, CI workflow, validation script, audit index,
  release evidence, or Graphify snapshot changes.

## Authority Boundary

- **Authoritative for**:
  - Repo-backed governance baseline and owner/evidence mapping checked on
    2026-07-10.
  - Dated comparison between local evidence and the official OpenGitOps
    benchmark.
  - Evidence-backed follow-up recommendations for later scoped work.
- **Not authoritative for**:
  - Active Stage 00/05 policy, Stage 99 template/routing contracts, CI workflow
    semantics, provider-native permissions, or release procedure.
  - Live k3d, Kubernetes, ArgoCD, Vault, ESO, credential, secret, provider-runtime,
    remote GitHub, or deployment readiness.
  - Proof that an external benchmark capability is implemented locally.

## Scope

- Covers workspace purpose, GitOps-first flow, persona/owner routing, provider
  adapters, Stage taxonomy, approval boundaries, CI/static validation, evidence
  stores, templates, scripts, integration guidance, and governance follow-up.
- Excludes active control changes, live/remote checks, secret-value inspection,
  provider-runtime inspection, Historical-pack edits, and implementation of the
  recommendations below.

## Definitions / Facts

### Workspace Purpose and Operating Contract

- **Repo fact — purpose**: [Root README](../../../../README.md) defines this
  repository as the document SSoT, GitOps manifest set, and bootstrap asset set
  for a WSL2 + WSL-native Docker + k3d local platform. External Vault,
  PostgreSQL, Valkey, and cloud runtimes remain outside the repository-owned
  runtime boundary.
- **Repo fact — execution contract**:
  [Bootstrap Governance](../../../00.agent-governance/rules/bootstrap.md) and
  [Agentic Execution Rules](../../../00.agent-governance/rules/agentic.md)
  require repo-first planning, explicit validation, and the default desired-state
  flow `repository change -> review -> ArgoCD reconciliation`. Direct live
  mutation is not the normal agent path.
- **Repo fact — reconciliation evidence**:
  [`root-application.yaml`](../../../../gitops/clusters/local/root-application.yaml)
  points ArgoCD at `gitops/apps/root`, while
  [`applicationset-apps.yaml`](../../../../gitops/clusters/local/applicationset-apps.yaml)
  discovers `gitops/workloads/*`; both declare automated pruning and self-healing.
  This proves declarative configuration exists, not that a live controller
  reconciled it in this review.
- **Repo fact — people and agents**: persona-to-layer routing is owned by
  [Persona Protocol](../../../00.agent-governance/rules/persona.md) and the
  matching scopes. A 2026-07-10 file inventory found the same ten agent stems in
  each of `.claude/agents/*.md`, `.agents/agents/*.md`, and
  `.codex/agents/*.toml`. This proves file-stem parity only, not provider-native
  registration or runtime behavior.
- **Repo fact — CI inventory**: `.github/workflows/` contains exactly five YAML
  workflows. [`ci.yml`](../../../../.github/workflows/ci.yml) declares six jobs:
  `branch-policy`, `changes`, `pre-commit`, `repo-quality-static`,
  `manifest-static`, and `ci-summary`. Local inspection did not verify remote
  GitHub Actions runs or branch-protection/ruleset state.

### External Benchmark

**External fact**: OpenGitOps v1.0.0 defines four GitOps principles for desired
state: Declarative, Versioned and Immutable, Pulled Automatically, and
Continuously Reconciled. Sources were checked on 2026-07-10 at the
[OpenGitOps official site](https://opengitops.dev/) and the
[OpenGitOps official principles document](https://github.com/open-gitops/documents/blob/main/PRINCIPLES.md).

| OpenGitOps benchmark context | Repo fact | Interpretation |
| --- | --- | --- |
| Declarative | Kubernetes/Argo CD desired state is stored under `gitops/**`; the root Application and workload ApplicationSet name repository paths explicitly. | Aligned for the tracked desired-state surface. The benchmark is context; the manifests are the local proof. |
| Versioned and Immutable | Desired state is Git-tracked, and local history is available. This review did not inspect remote branch protection, signed commits, retention, or history-rewrite controls. | Versioning is evidenced; immutable-history enforcement is **Unverified** on the remote surface. |
| Pulled Automatically | Argo CD Application/ApplicationSet manifests point to the Git repository and `main`. | Pull configuration is present repo-statically; a live pull was not observed. |
| Continuously Reconciled | The same manifests configure `automated.prune: true` and `selfHeal: true`. | Reconciliation intent is present; controller health, sync status, and actual convergence were not checked. |

**Recommendation boundary**: OpenGitOps does not establish any local
implementation verdict by itself. Future live-convergence evidence must come from
an operator-approved runbook, while remote immutability evidence requires a
separate approved GitHub settings/ruleset review.

### Owner and Authority Matrix

| Area | Canonical owner | Local implementation evidence | Authority boundary | Current verdict |
| --- | --- | --- | --- | --- |
| Workspace purpose and intake | [Root README](../../../../README.md), [Bootstrap Governance](../../../00.agent-governance/rules/bootstrap.md) | Repository scope, JIT loading order, repo-evidence sources, GitOps-first rule | This reference summarizes; it does not change workspace scope or intake policy. | Sufficient (repo-static) |
| Persona and layer ownership | [Persona Protocol](../../../00.agent-governance/rules/persona.md), [Documentation Scope](../../../00.agent-governance/scopes/docs.md) | Technical Writer owns Stage 90 references; other persona scopes own their active stages | Stage 90 cannot grant another persona's implementation or operational authority. | Sufficient |
| SDLC stage and template routing | [Stage Authoring Matrix](../../../00.agent-governance/rules/stage-authoring-matrix.md), [SDLC Governance](../../../99.templates/support/sdlc-governance.md), [Template Routing Contract](../../../99.templates/support/template-routing.md) | Numeric Stage 01/03 routes, date-based Stage 04 routes, one template per authored path | Active lifecycle/route changes belong to Stage 00/99 owners and validators, not this reference. | Needs strengthening; duplicate summaries remain |
| Agent roster and provider adapters | [Local Harness Catalog](../../../00.agent-governance/harness-catalog.md), [Harness Implementation Map](../../../00.agent-governance/harness-implementation-map.md), provider notes | Ten matching agent stems across three adapter directories; shared assets under `.agents/**` with provider views | File parity is not native registration, permission enforcement, or live provider behavior. | Sufficient for inventory; runtime Unverified |
| Approval and mutation boundary | [Harness Approval Boundaries](../../../00.agent-governance/rules/approval-boundaries.md) | Protected-surface matrix; live cluster, Vault/secret, cloud, GitHub publish/merge/dispatch boundaries | Only explicit human/operator approval can broaden the default read-only/live-mutation boundary. | Sufficient |
| GitOps desired state | `gitops/**`, [Kubernetes GitOps operations policy](../../../05.operations/policies/0001-k8s-gitops-operations-policy.md) | Root Argo CD Application, workload ApplicationSet, Kustomize resources, automated prune/self-heal declarations | Repo evidence proves desired-state configuration, never live reconciliation or readiness. | Sufficient repo-static; live Unverified |
| CI and validation lanes | [`ci.yml`](../../../../.github/workflows/ci.yml), [Scripts README](../../../../scripts/README.md), [CI/CD & QA guide](../../../05.operations/guides/0010-ci-cd-qa-reference-guide.md) | Five workflow files, six CI jobs, repo-quality and manifest-static command bundles | Local PASS cannot prove remote CI, optional-tool, or live-runtime PASS. | Sufficient repo-static; remote CI Unverified |
| Execution evidence and durable memory | Stage 04 task records, [Progress Ledger](../../../00.agent-governance/memory/progress.md) | Task IDs, command evidence, limitations, handoff, reusable lessons | Task records prove recorded checks only; the harness catalog and active owners retain current truth. | Sufficient, with lifecycle asymmetry |
| Research and audit currentness | [Research index](../README.md), [Audit index](../../audits/README.md), reference maintenance runbook | Dated Current/Historical research packs and dated audit snapshots | Stage 90 remains descriptive and must not label stale snapshots as active policy. | Needs strengthening; audit Current labels drift |
| Release evidence | [GitHub automation hub](../../../../.github/ABOUT.md), [`generate-changelog.yml`](../../../../.github/workflows/generate-changelog.yml) | Version-tag workflow creates a review artifact and does not publish or mutate repository history | Artifact generation is not release approval, promotion policy, provenance, or deployment. | Partial; no dedicated release document contract |

### Enforcement and Evidence Map

| Contract | Instruction | Preventive control | Feedback evidence | Knowledge store |
| --- | --- | --- | --- | --- |
| GitOps-first desired-state changes | Bootstrap and agentic rules require repository change, review, and reconciliation; direct mutation is exceptional. | Approval-boundary matrix plus provider-specific sandbox/permission controls; there is no claim of one identical provider gate. | GitOps structure, manifest, secret, and policy validators; Stage 04 task evidence | GitOps policy/runbooks, harness implementation map, progress ledger |
| Authored document routing | Read template routing and the matching template before editing; keep Stage 90 descriptive. | Pre-edit documentation hooks where wired and deterministic structural/template checks in the repo-quality gate | `git diff --check`, Markdown checks, `validate-repo-quality-gates.sh` | Stage 00 routing, Stage 99 support contracts/templates, Stage README indexes |
| Provider adapter parity | Keep role, scope import, guardrail, handoff, and postflight aligned while preserving native metadata. | Repository parity/inventory checks; Claude settings remain the native permission gate, while Codex/Gemini hook JSON is context/validation wiring | Harness/repo-quality validation and task-scoped adapter review | Harness catalog, provider notes, model policy |
| Protected external/live action | Default external research is read-only; mutation, publish, push, merge, dispatch, paid jobs, secrets, and live changes require approval. | Runtime sandbox/approval plus the canonical approval matrix; secret values remain forbidden | Redacted secret scan, policy gates, explicit skipped-live limitations | Approval boundaries, operations runbooks/incidents, Stage 04 evidence |
| CI/static quality lanes | Run local deterministic checks and keep repo-static, CI/toolchain, and live evidence separate. | CI path filters, read-only workflow permission, required workflow jobs, local script failure semantics | Five workflow definitions, six job results when remote CI runs, local script output | CI/CD QA guide, scripts inventory, task verification summaries |
| SDD lifecycle and handoff | Route requirement, architecture, spec, plan, task, operations, and reference artifacts to their owning stages. | Route/frontmatter/index gates enforce deterministic shape; semantic lineage remains manual/link-based | Resolved-link checks, status/index checks, reviewer evidence | Stage documents, task records, progress ledger, archive tombstones |

### Governance Gap Register

The rows below are **recommendations**, not active changes. Severity is included
inside `Risk`, and each row names the canonical route for a later scoped task.

| Finding | Evidence | Risk | Recommendation | Canonical follow-up route |
| --- | --- | --- | --- | --- |
| Lifecycle draft/done asymmetry | A 2026-07-10 scan found 16 of 20 active `docs/03.specs/*/spec.md` files at `status: draft` and no Spec at `done`; for example, `021-sdlc-lifecycle-contract/spec.md` is draft while its Stage 04 plan and task are done. | **Medium** — completed execution can appear to depend on an unpromoted implementation contract, weakening lifecycle/currentness signals. | Define an explicit human promotion/closure review and deterministic evidence rule; do not auto-promote existing specs from this research pass. | New Stage 03 lifecycle-governance spec, then Stage 00 `documentation-protocol.md`/`stage-authoring-matrix.md`, Stage 03/04 indexes, templates, and repo-quality validation. |
| Release document contract is absent | The Stage 99 route map has no release template. `.github/workflows/generate-changelog.yml` creates a changelog artifact, while `.github/ABOUT.md` states it does not publish, push, or deploy. | **Medium** — approval, promotion, retention, provenance, and rollback evidence can remain implicit even though a release-evidence artifact exists. | Decide whether a dedicated release record is needed and define its owner/route before adding a template or workflow gate. | New Stage 03 release-contract spec; if approved, Stage 05 policy/runbook plus Stage 99 route/template and `.github` release-evidence owner. |
| Lifecycle and route summaries are duplicated | `sdlc-governance.md` says it owns lifecycle state, numeric lineage, handoff, and duplicate rules, but substantially similar summaries also appear in `stage-authoring-matrix.md` and `document-stage-routing.md`; `template-routing.md` already points to the canonical owner. | **Medium** — parallel normative summaries can diverge and make ownership ambiguous. | Keep one normative lifecycle body and convert secondary surfaces to concise role-specific pointers after a scoped cross-owner review. | Stage 00/99 governance-normalization spec and task covering `sdlc-governance.md`, stage routing/matrix, template routing, README indexes, and validator sentinels. |
| Lifecycle lineage is link-only at the semantic layer | Templates and Stage READMEs require related-document links, and the quality gate checks deterministic routes/headings/links. The lifecycle implementation plan records that semantic duplicate lineage cannot be inferred safely; no stable lineage ID is enforced across PRD/ARD/ADR/Spec/Plan/Task. | **Medium** — links may resolve while representing incomplete or mismatched feature lineage, leaving reviewers to reconstruct traceability manually. | Evaluate a stable lineage identifier or a narrowly deterministic cross-stage validator before changing frontmatter or templates. | New Stage 03 traceability spec, followed by Stage 99 frontmatter/template support, Stage README contracts, and `scripts/validate-repo-quality-gates.sh`. |
| Audit currentness labels drift | `docs/90.references/audits/README.md` labels several 2026-07-02/04 reports and the 2026-07-05 pack as `Current`; the 2026-07-05 audit pack still benchmarks the now-Historical `2026-07-04-wer` research pack, while `2026-07-07-wer` is the Current research pack. | **Medium** — readers can mistake multiple dated snapshots for one current implementation verdict and miss newer source evidence. | Establish one explicit current-audit pointer and label older packs as dated or resolved snapshots; refresh audits only against current canonical evidence. | Stage 90 audit index and reference-maintenance runbook through a Stage 03/04 audit-currentness task. |
| Graphify snapshot is stale | `graphify-out/GRAPH_REPORT.md` is dated 2026-06-04 and says it was built from commit `e8a99671`; before this edit, `git rev-list --count e8a99671..HEAD` returned 199. | **Low** — optional graph navigation may omit newer governance and agent surfaces, but canonical repo files still control decisions. | Regenerate the tracked Graphify artifacts when the optional tool is intentionally available, review the diff, and record the source commit; never use the stale graph as current proof. | Graphify generated-artifact maintenance task with `graphify-out/**` review and Stage 04 evidence; no active-policy change. |

## Sources

### Repository Sources

- [Root README](../../../../README.md)
- [Bootstrap Governance](../../../00.agent-governance/rules/bootstrap.md)
- [Agentic Execution Rules](../../../00.agent-governance/rules/agentic.md)
- [Harness Approval Boundaries](../../../00.agent-governance/rules/approval-boundaries.md)
- [Persona Protocol](../../../00.agent-governance/rules/persona.md)
- [Documentation Scope](../../../00.agent-governance/scopes/docs.md)
- [Local Harness Catalog](../../../00.agent-governance/harness-catalog.md)
- [Harness Implementation Map](../../../00.agent-governance/harness-implementation-map.md)
- [Stage Authoring Matrix](../../../00.agent-governance/rules/stage-authoring-matrix.md)
- [SDLC Governance](../../../99.templates/support/sdlc-governance.md)
- [Template Routing Contract](../../../99.templates/support/template-routing.md)
- [Reference Template](../../../99.templates/templates/common/reference.template.md)
- [CI/CD & QA Reference Guide](../../../05.operations/guides/0010-ci-cd-qa-reference-guide.md)
- [Scripts README](../../../../scripts/README.md)
- [GitHub CI Workflow](../../../../.github/workflows/ci.yml)
- [Argo CD root Application](../../../../gitops/clusters/local/root-application.yaml)
- [Workload ApplicationSet](../../../../gitops/clusters/local/applicationset-apps.yaml)
- [Audit index](../../audits/README.md)
- [Graphify report](../../../../graphify-out/GRAPH_REPORT.md)
- [Historical governance baseline](../2026-07-04-wer/workspace-governance-baseline.md)

### External Sources

- [OpenGitOps official site](https://opengitops.dev/) — Source checked:
  2026-07-10; v1.0.0 principles and benchmark context.
- [OpenGitOps official principles document](https://github.com/open-gitops/documents/blob/main/PRINCIPLES.md) —
  Source checked: 2026-07-10; primary upstream text for the four principles.

## Review and Freshness

- Review cadence: on source change
- Last reviewed: 2026-07-10
- Next review trigger: canonical governance, lifecycle/route ownership, agent
  inventory, provider adapters, approval boundary, GitOps root/ApplicationSet,
  CI workflow/job inventory, validation scripts, audit Current pointer, release
  evidence, or Graphify source commit changes.

## Related Documents

- **Current pack README**: [README.md](./README.md)
- **Parent research README**: [../README.md](../README.md)
- **Parent references README**: [../../README.md](../../README.md)
- **Spec**: [Workspace Engineering Research Pack Spec](../../../03.specs/017-workspace-engineering-research-pack/spec.md)
- **Plan**: [Current Research Pack Fact-First Hardening Plan](../../../04.execution/plans/2026-07-10-current-research-pack-fact-first-hardening.md)
- **Task**: [Current Research Pack Fact-First Hardening Task](../../../04.execution/tasks/2026-07-10-current-research-pack-fact-first-hardening.md)
- **Reference maintenance runbook**: [Reference Maintenance Runbook](../../../05.operations/runbooks/0011-reference-maintenance-runbook.md)
