---
title: 'Reference: Scope Application Index'
version: "1.0.0"
type: reference/research
layer: "references"
status: draft
owner: platform
updated: 2026-09-04
artifact_id: "RES-0001-m0013"
---

# Reference: Scope Application Index

## Overview

This index keeps the Workspace Engineering Research pack routable after the
repository replaced its ten legacy file-ownership scopes with seven current
responsibility documents and the neutral agent registry. The dated scope
projection remains historical evidence. The current projection routes the same
thirty-six research requests to responsibility lenses without turning those
lenses into file permissions.

This update contributes no new external finding, source identifier, claim
identifier, or requirement-status change. The retained external observation
boundary remains 2026-08-28; the current repository observation is `main` at
`24fe45af3771ad7e42fd0c871b375a6d5ecfec00` on 2026-09-04.

## Reference Type

Routing index over existing research, dated workspace observations, and current
responsibility owners. It is not a policy, permission grant, runtime result,
deployment control, or backlog.

## Authority Boundary

The current [responsibility router](../../../00.agent-governance/roles/README.md)
defines the available review and work lenses. The
[agent registry](../../../../.agents/registry.json) owns concrete role,
permission, skill, provider-projection, and handoff membership. Stage owners
retain substantive decisions, and the pack
[Requirement Coverage Matrix](README.md#requirement-coverage-matrix) remains the
status owner.

The former `docs/00.agent-governance/scopes/` tree was removed during the
Spec 0054 governance convergence. Its 2026-08-14 and 2026-08-17 projections
below are observation-dated evidence only. They cannot be used as current file
ownership or write authority.

This index cannot create a responsibility, assign a file, authorize a live or
hosted action, or promote a finding. A request appearing under a responsibility
means that lens is relevant to review or handoff; exact authority still resolves
through the active Task and agent registry.

## Scope

The index covers `REQ-WERPC-001` through `REQ-WERPC-036`, the seven current
responsibilities, the retained blocking classes, and repository-static deltas
between the 2026-08-28 external revalidation and current `main`.

It excludes a new external-source cycle, provider-runtime execution, hosted
workflow execution for this branch, live-cluster inspection, credential or
secret access, stakeholder validation, and any mutation outside this research
index and its owning Task evidence.

## Definitions / Facts

### Current responsibility routing at 2026-09-04

Responsibility rows intentionally overlap. They identify the review lens and
handoff destination; they do not replace the exact permission and ownership
records in `.agents/registry.json`.

| Current responsibility | Related requests | Current routing surface | Retained evidence boundary |
| --- | --- | --- | --- |
| [Architecture](../../../00.agent-governance/roles/architecture.md) | `REQ-WERPC-007`, `010`-`013`, `034`-`036` | Requirements, Architecture Descriptions, ADRs, Specs, Plans, and Tasks | Structural consistency is repository-static; generated behavior, decision effectiveness, and stakeholder acceptance remain `DEFER`. |
| [Documentation](../../../00.agent-governance/roles/documentation.md) | `REQ-WERPC-014`, `016`, `018`, `020`, `021`, `034`-`036` | Authored forms, navigation, reference routing, and release communication | Documentation owns form and navigation quality, not every stage's substantive claim. No separate Release family is activated. |
| [Infrastructure](../../../00.agent-governance/roles/infrastructure.md) | `REQ-WERPC-008`, `009` | `gitops/`, `infrastructure/`, policy manifests, and reconciliation structure | Desired-state text does not prove effective RBAC, admission, reconciliation, health, or recovery; those remain `live-cluster` / `DEFER`. |
| [Supervision](../../../00.agent-governance/roles/supervision.md) | `REQ-WERPC-001`-`006`, `026`-`032` | Stage 00 policy, the agent registry, and Claude/Codex projections | Supervision coordinates bounded work but does not gain authoring permission. Provider discovery, execution, parity, model resolution, and provider memory remain `provider-runtime` / `DEFER`. |
| [Operations](../../../00.agent-governance/roles/operations.md) | `REQ-WERPC-014`-`019` | Guides, policies, runbooks, incidents, postmortems, and recovery knowledge | Static procedure quality does not prove rehearsal, operator authority, or safe live execution. |
| [Quality](../../../00.agent-governance/roles/quality.md) | `REQ-WERPC-022`-`024`, `033` | Validation routing, tests, fixtures, workflow lane content, and evidence semantics | Repository checks establish bounded verification. Hosted enforcement and intended-use validation remain `hosted-ci` or `human-judgement` / `DEFER`. |
| [Security](../../../00.agent-governance/roles/security.md) | `REQ-WERPC-008`, `009`, `025`, and security-impacting parts of `026`-`028` | Secret references, access control, isolation, unsafe execution, and third-party adoption review | Review is read-only unless a separate implementation owner is authorized. It grants no secret access, live investigation, or repair. |

Backend, frontend, and product remain general duties routed through the owning
Requirement, Spec, and implementation Task rather than standalone responsibility
documents. This is deliberate current topology, not an unowned-role defect.

### 2026-09-04 current-main workspace delta gate

The gate compared the retained 2026-08-28 external observation with current
`main`. It reviewed repository history and current owner paths only; it did not
re-observe external product or standards sources. Consequently it allocates no
`SRC-WERPC-*` or `CLM-WERPC-*` identifier and changes no coverage-matrix status.

| Delta area | Material current-main observation | Requests affected | Research effect |
| --- | --- | --- | --- |
| Governance and provider topology | The ten scope documents are gone. Seven responsibility documents plus `.agents/registry.json` now route work; Claude and Codex remain the provider projections. | `REQ-WERPC-003`-`006`, `026`-`032` | Current routing changed; provider-runtime limits and existing statuses remain unchanged. |
| SDLC, document identity, and lifecycle | Legacy Stage 03 package routers were retired, authored identity and frontmatter were normalized, reference families gained separate lifecycles, and terminal packages now route through the Stage 98 retention taxonomy. | `REQ-WERPC-007`, `010`-`021`, `034`-`036` | Workspace owners and paths changed; external document-family findings and effectiveness limits remain unchanged. |
| Knowledge and memory authority | The progress ledger and governance memory directory were retired. Durable authority routes through canonical Specs, operating documents, Git history, and the active context-and-memory policy. | `REQ-WERPC-021`, `029`-`032` | Historical memory-path evidence is no longer current authority; provider retention, deletion, retrieval, and secure erasure remain `DEFER`. |
| Validation and GitHub surface | Validation routing moved to `scripts/validation/registry.json`, semantic rules were consolidated to one production owner, Python gained an explicitly scoped Ruff lane, and the GitHub routing document is `.github/repository-surface.md`. | `REQ-WERPC-022`-`024`, `033` | Static implementation paths changed. Verification/validation and hosted-CI distinctions remain unchanged. |
| Archive and navigation | Stage 98 now separates `migrations/`, `completed/`, `superseded/`, and `tombstones/`; top-level trees have routed README coverage. | `REQ-WERPC-003`, `007`, `010`-`021`, `024`, `031` | Recovery and navigation facts changed without changing research statuses or source-backed claims. |
| Kubernetes and security desired state | This bounded re-projection identified no material post-2026-08-28 GitOps, cluster, Vault, network-policy, or workload-security finding. | `REQ-WERPC-008`, `009`, `025` | Existing `Partial` and `live-cluster` / `DEFER` boundaries remain. |
| Hosted evidence | The observed `main` workflow run at this baseline failed required jobs, including `ci-summary`. No branch-specific hosted run existed at the pre-commit observation boundary. | `REQ-WERPC-022`, `023` | A failed baseline is not branch evidence and cannot be converted into `PASS`; hosted validation remains separately required. |

The A-mode result is therefore **material workspace-routing change with zero
external-status promotion**. The canonical pack stays in place; no duplicate
research directory, transitional checker, provider adapter, workflow, manifest,
or one-time tracked artifact is added.

### Historical 2026-08-14 scope-to-requirement projection

The previous ten-scope map was derived from the then-current
`docs/00.agent-governance/scopes/` file-ownership tables. It identified five
paths not listed by those tables: `.github/**`, `.agents/agents/**`, `traefik/`,
`.pre-commit-config.yaml`, and root `policy/`.

That projection is preserved as a dated finding, not a current ownership claim.
The scope tree no longer exists, `.github/**` was subsequently assigned and
then responsibility routing replaced scope routing. Current authority must not
be inferred from the historical unowned-path list.

### 2026-08-17 full-corpus re-projection and blocking-class closure

The 2026-08-17 cycle assigned every retained `Partial` and `DEFER` row one
blocking class and one reopen condition. Of thirty-six request owners, twelve
were unblocked, ten were reachable through repository-static work, and fourteen
were structurally unreachable from repository-static evidence.

| Blocking class | Requests | Reachable by repository-static work | Reopen condition |
| --- | --- | --- | --- |
| `none` | `REQ-WERPC-007`, `011`-`013`, `015`-`017`, `019`, `027`, `029`-`031` | n/a | n/a |
| `repo-static` | `REQ-WERPC-003`-`006`, `010`, `021`, `024`, `034`-`036` | yes | A material current-owner or repository-contract delta. |
| `provider-runtime` | `REQ-WERPC-001`, `002`, `026`, `028`, `032` | no | Authorized provider-runtime evidence or a contradicting provider contract. |
| `hosted-ci` | `REQ-WERPC-022`, `023` | no | Authorized hosted-run evidence at the current revision. |
| `live-cluster` | `REQ-WERPC-008`, `009`, `025` | no | Operator-authorized live observation. |
| `human-judgement` | `REQ-WERPC-014`, `018`, `020`, `033` | no | A named approval, reviewer record, reader test, or stakeholder-validation activity. |

Closure is an evidence-reachability statement, not a correctness or safety
claim. The 2026-09-04 repository delta satisfies the reopen condition only for
the affected `repo-static` rows. It does not reopen provider, hosted, live, or
human-judgement rows.

### Retained cycle register

| Observation date | Cycle result retained by this index |
| --- | --- |
| 2026-08-11/12 | The twelve `Partial` rows were re-tested and remained `Partial`; hosted metadata narrowed but did not close the hosted boundary. |
| 2026-08-14 | Spec, Plan, and Task were added as `REQ-WERPC-034`-`036`; the ten-scope projection was re-observed. |
| 2026-08-20 | Full-corpus repository and public-source deltas changed selected owner facts without lowering evidence boundaries. |
| 2026-08-23 | The source ledger extended through `SRC-WERPC-115` and `CLM-WERPC-014-11`; no status changed. |
| 2026-08-28 | The closed full-scope revalidation extended the ledger through `SRC-WERPC-122` and `CLM-WERPC-015-11`. |
| 2026-09-04 | Current-main routing and lifecycle changes were re-projected without a new external-source cycle. |

### 2026-08-28 closed full-scope revalidation

The full-scope cycle re-observed all thirty-six request owners using official or
primary external sources and named repository-static selectors. It retained
fourteen Markdown files, thirty-six owners, 122 source identifiers, and 163
claim identifiers. No requirement status or evidence class was promoted.

Material currentness deltas were limited to added C4/arc42/ADR coverage, a newer
`agency-agents` main branch, newer upstream kube-state-metrics and Argo CD
releases, and recovered NASA traceability-source availability. The terminal
blocking classes and reopen conditions above remained unchanged.

The 2026-09-04 workspace delta does not supersede that external observation.
It updates only current repository routing and preserves the source and claim
ledger exactly as recorded in
[m0012](m0012-source-coverage.md#2026-08-28-source-delta-increment).

## Sources

- Current repository observation, 2026-09-04:
  [`main` at `24fe45af3771ad7e42fd0c871b375a6d5ecfec00`](https://github.com/buenhyden/hy-home.k8s/commit/24fe45af3771ad7e42fd0c871b375a6d5ecfec00).
- Current responsibility topology:
  [roles router](../../../00.agent-governance/roles/README.md) and
  [agent registry](../../../../.agents/registry.json).
- Current document and lifecycle routing:
  [Stage 99 registry](../../../99.templates/registry.json) and
  [Stage 98 archive taxonomy](../../../98.archive/README.md).
- Current evidence and validation routing:
  [quality policy](../../../00.agent-governance/policies/quality.md),
  [validation registry](../../../../scripts/validation/registry.json), and
  [pre-commit configuration](../../../../.pre-commit-config.yaml).
- Current memory authority:
  [context and memory policy](../../../00.agent-governance/policies/context-and-memory.md).
- Current GitHub routing:
  [repository surface](../../../../.github/repository-surface.md).
- Hosted baseline observation:
  [workflow run 33837691808](https://github.com/buenhyden/hy-home.k8s/actions/runs/33837691808).
- Retained external-source and claim evidence:
  [pack coverage matrix](README.md#requirement-coverage-matrix) and
  [source coverage ledger](m0012-source-coverage.md).

These are repository-static or repository-hosted observations. This update
introduces no external source and adds no row to the source register.

## Review and Freshness

The external research observation remains dated 2026-08-28. The responsibility,
path, lifecycle, archive, validation, and hosted-baseline observations are dated
2026-09-04 and bound to the exact `main` commit stated above.

Refresh this index when the role router, agent registry, Stage 98 taxonomy,
Stage 99 profile registry, validation registry, coverage-matrix status, or
blocking-class reopen evidence changes. Do not refresh an external claim from a
repository-only diff; route an actual source delta through `m0012`.

The historical ten-scope projection must remain labelled historical. Recreating
its file-ownership conclusions from the current role documents would conflate a
review responsibility with write permission.

## Related Documents

- [Pack README and coverage matrix](README.md)
- [Source and claim ledger](m0012-source-coverage.md)
- [Workspace governance](m0001-workspace-governance-and-common-agent-environment.md)
- [Harness and loop](m0002-harness-and-loop-engineering.md)
- [Provider status](m0003-provider-implementation-status.md)
- [SDLC contracts](m0004-spec-driven-sdlc-and-document-contracts.md)
- [Documentation architecture](m0005-documentation-architecture-and-diataxis.md)
- [LLM-WIKI routing](m0006-llm-wiki-and-knowledge-routing.md)
- [Platform security](m0007-kubernetes-infrastructure-and-security.md)
- [CI/CD and QA](m0008-ci-cd-github-actions-and-qa.md)
- [AI agents](m0009-ai-agents-and-agency-agents.md)
- [Model routing](m0010-agent-model-routing-and-configuration.md)
- [Memory](m0011-agent-memory-tiers-and-management.md)
- [Responsibility router](../../../00.agent-governance/roles/README.md)
