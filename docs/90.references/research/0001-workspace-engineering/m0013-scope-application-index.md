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
| SDLC, document identity, and lifecycle | Stage 03 package routers were retired, authored identity and frontmatter were normalized, reference families gained separate lifecycles, and terminal packages now route through the Stage 98 retention taxonomy. | `REQ-WERPC-007`, `010`-`021`, `034`-`036` | Workspace owners and paths changed; external document-family findings and effectiveness limits remain unchanged. |
| Knowledge and memory authority | The progress ledger and governance memory directory were retired. Durable authority routes through canonical Specs, operating documents, Git history, and the active context-and-memory policy. | `REQ-WERPC-021`, `029`-`032` | Historical memory-path evidence is no longer current authority; provider retention, deletion, retrieval, and secure erasure remain `DEFER`. |
| Validation and GitHub surface | Validation routing moved to `scripts/validation/registry.json`, semantic rules were consolidated to one production owner, Python gained an explicitly scoped Ruff lane, and the GitHub routing document is `.github/repository-surface.md`. | `REQ-WERPC-022`-`024`, `033` | Static implementation paths changed. Verification/validation and hosted-CI distinctions remain unchanged. |
| Archive and navigation | Stage 98 now separates `migrations/`, `completed/`, `superseded/`, and `tombstones/`; all top-level trees have routed README coverage. | `REQ-WERPC-003`, `007`, `010`-`021`, `024`, `031` | Recovery and navigation facts changed without changing research statuses or source-backed claims. |
| Kubernetes and security desired state | No reviewed post-2026-08-28 commit in this bounded delta introduced a material GitOps, cluster, Vault, network-policy, or workload-security finding. | `REQ-WERPC-008`, `009`, `025` | Existing `Partial` and `live-cluster` / `DEFER` boundaries remain. |
| Hosted evidence | The latest observed `main` workflow run at this baseline failed required jobs, including `ci-summary`. No branch-specific hosted run exists at the time of this record. | `REQ-WERPC-022`, `023` | A failed baseline is not branch evidence and cannot be converted into `PASS`; hosted validation remains separately required. |

The A-mode result is therefore **material workspace-routing change with zero
external-status promotion**. The canonical pack stays in place; no duplicate
research directory, transitional checker, provider adapter, workflow, manifest,
or one-time tracked artifact is added.

### Historical 2026-08-14 scope-to-requirement map

The following map is preserved as observation-dated evidence. It was derived by
matching each requirement's canonical owner against the file-ownership globs in
the ten scope documents that existed on 2026-08-14. The scope tree no longer
exists, so these rows are not current routing or write authority.

Scope labels link to the closest current responsibility owners only for
navigation. Those links do not make the 2026-08-14 membership, owner paths,
gaps, or dispositions current.

| Scope | Related REQ | Canonical owner paths | As-Is evidence | Recorded gap | DEFER boundary | Scope owner next action |
| --- | --- | --- | --- | --- | --- | --- |
| [architecture](../../../00.agent-governance/roles/architecture.md) | `REQ-WERPC-007`, `REQ-WERPC-012`, `REQ-WERPC-013`, `REQ-WERPC-031` | `docs/03.specs/`, `docs/02.architecture/requirements/`, `docs/02.architecture/decisions/` | [Spec-driven baseline](m0004-spec-driven-sdlc-and-document-contracts.md#spec-driven-development-baseline), [Document-family matrix](m0004-spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix), [Domain-memory baseline](m0011-agent-memory-tiers-and-management.md#domain-scoped-memory-baseline) | All four `Verified` | Generated-code outcomes, decision quality, and actual retrieval remain `DEFER` | None required. Static contracts are sourced; treat architecture effectiveness as an unmeasured property, not a passing one. |
| [backend](../../../00.agent-governance/roles/README.md) | `REQ-WERPC-007`, `REQ-WERPC-010`, `REQ-WERPC-011`, `REQ-WERPC-031` | `docs/03.specs/`, `docs/01.requirements/` | [Spec-driven baseline](m0004-spec-driven-sdlc-and-document-contracts.md#spec-driven-development-baseline), [Document-family matrix](m0004-spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix) | All four `Verified` | Conformance, effectiveness, and stakeholder validation remain `DEFER` | None required. Template conformance is not product validation. |
| [docs](../../../00.agent-governance/roles/documentation.md) | `REQ-WERPC-014`, `REQ-WERPC-016`, `REQ-WERPC-020`, `REQ-WERPC-021` | `docs/05.operations/guides/`, `docs/99.templates/`, historical observation: `docs/90.references/llm-wiki/` | [Document-family matrix](m0004-spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix), [Diátaxis baseline](m0005-documentation-architecture-and-diataxis.md#diátaxis-baseline), [historical LLM-WIKI baseline](m0006-llm-wiki-and-knowledge-routing.md#llm-wiki-baseline) | `REQ-WERPC-014` `Partial`, `REQ-WERPC-020` `Partial` | Tutorial classification and usability need a named reader and human review; no static validator infers them | Answered on 2026-08-11: approved Spec 052 `DOC-G2` and `DOC-G3` already decline both routes, and the framework's own instruction not to create empty structures was verified at upstream source. Do not propose these profiles. The open item was `DOC-G1` enum enforcement under the then-queued `WORK-013` package. |
| [frontend](../../../00.agent-governance/roles/README.md) | `REQ-WERPC-007`, `REQ-WERPC-010`, `REQ-WERPC-011`, `REQ-WERPC-031` | `docs/03.specs/`, `docs/01.requirements/` | [Spec-driven baseline](m0004-spec-driven-sdlc-and-document-contracts.md#spec-driven-development-baseline), [Document-family matrix](m0004-spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix) | All four `Verified` | Same as `backend`; the two scopes declared identical ownership globs | None required. The identical membership was a property of the scope registry, not a mapping error. |
| [infra](../../../00.agent-governance/roles/infrastructure.md) | `REQ-WERPC-008`, `REQ-WERPC-009`, `REQ-WERPC-017`, `REQ-WERPC-019`, `REQ-WERPC-024`, `REQ-WERPC-025` | `gitops/`, `infrastructure/`, `scripts/`, `docs/05.operations/policies/`, `docs/05.operations/runbooks/` | [Kubernetes baseline](m0007-kubernetes-infrastructure-and-security.md#kubernetes-baseline), [Infrastructure baseline](m0007-kubernetes-infrastructure-and-security.md#infrastructure-baseline), [Security baseline](m0007-kubernetes-infrastructure-and-security.md#security-baseline), [QA baseline](m0008-ci-cd-github-actions-and-qa.md#qa-baseline) | `REQ-WERPC-008`, `REQ-WERPC-009`, `REQ-WERPC-025` `Partial` | k3d, gateway, registry, hosted CI, effective RBAC, and live posture remain `DEFER` | The then-highest-value bounded item was the `kube-state-metrics` Secret read recorded in the retired progress ledger; its consumer inventory was complete. Human approval remained required before any manifest change. |
| [meta](../../../00.agent-governance/roles/supervision.md) | `REQ-WERPC-001`–`REQ-WERPC-006`, `REQ-WERPC-026`, `REQ-WERPC-028`–`REQ-WERPC-030`, `REQ-WERPC-032`, `REQ-WERPC-033` | `docs/00.agent-governance/`, `AGENTS.md`, `.claude/settings.json`, `.claude/skills/`, `.agents/skills/`, `.codex/` | [Harness baseline](m0002-harness-and-loop-engineering.md#harness-baseline), [Loop baseline](m0002-harness-and-loop-engineering.md#loop-baseline), [Claude baseline](m0003-provider-implementation-status.md#claude-baseline), [Codex baseline](m0003-provider-implementation-status.md#codex-baseline), [Common-system baseline](m0001-workspace-governance-and-common-agent-environment.md#common-system-baseline), [Model-routing baseline](m0010-agent-model-routing-and-configuration.md#model-routing-baseline), [Memory-management baseline](m0011-agent-memory-tiers-and-management.md#memory-management-baseline) | `REQ-WERPC-006`, `REQ-WERPC-026`, `REQ-WERPC-028`, `REQ-WERPC-032`, `REQ-WERPC-033` `Partial` | Provider parity, discovery, permission enforcement, model resolution, cost and latency, retention, and connected-resource behavior all require provider runtime execution, which is `DEFER` | This scope carried the largest `Partial` count. None was closable statically; provider runtime evidence was a separate authorized activity, not pending documentation work. |
| [ops](../../../00.agent-governance/roles/operations.md) | `REQ-WERPC-015`, `REQ-WERPC-017`, `REQ-WERPC-019` | `docs/05.operations/incidents/`, `docs/05.operations/policies/`, `docs/05.operations/runbooks/`, `infrastructure/tests/` | [Document-family matrix](m0004-spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix) | All three `Verified` | Runtime response, enforcement, rehearsal, and live command safety remain `DEFER` | None required. A structurally valid runbook is not a rehearsed or authorized one; record rehearsal as evidence when it happens. |
| [product](../../../00.agent-governance/roles/README.md) | `REQ-WERPC-010`, `REQ-WERPC-011` | `docs/01.requirements/`, historical observation: `docs/04.execution/plans/` | [Spec-driven baseline](m0004-spec-driven-sdlc-and-document-contracts.md#spec-driven-development-baseline), [Document-family matrix](m0004-spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix) | Both `Verified` | Stakeholder and product validation remain `DEFER` | None required. Requirements validation is a stakeholder activity, not a validator lane. |
| [qa](../../../00.agent-governance/roles/quality.md) | `REQ-WERPC-023`, `REQ-WERPC-024`, `REQ-WERPC-029`, `REQ-WERPC-033` | `scripts/validate-*.py`, `docs/00.agent-governance/contracts/`, `tests/` | [GitHub Actions baseline](m0008-ci-cd-github-actions-and-qa.md#github-actions-baseline), [QA baseline](m0008-ci-cd-github-actions-and-qa.md#qa-baseline), [Verification and Validation matrix](m0008-ci-cd-github-actions-and-qa.md#verification-and-validation-question-matrix) | `REQ-WERPC-023`, `REQ-WERPC-033` `Partial` | Hosted runs, rulesets, secrets, environments, OIDC, artifacts, and intended-use evidence remain `DEFER` | Keep static `PASS` labelled as bounded conformance evidence. A green lane is verification, never validation of intended use. |
| [security](../../../00.agent-governance/roles/security.md) | `REQ-WERPC-008`, `REQ-WERPC-015`, `REQ-WERPC-016`, `REQ-WERPC-025` | `gitops/platform/network-policies/`, `infrastructure/vault/`, `docs/05.operations/incidents/` | [Kubernetes baseline](m0007-kubernetes-infrastructure-and-security.md#kubernetes-baseline), [Security baseline](m0007-kubernetes-infrastructure-and-security.md#security-baseline), [Document-family matrix](m0004-spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix) | `REQ-WERPC-008`, `REQ-WERPC-025` `Partial` | Effective RBAC, real traffic flows, attestation, and live posture remain `DEFER` | The absent default-deny ingress posture recorded in the retired progress ledger was the highest-risk item in the pack. It required a complete allowed-flow inventory and a security-reviewed Spec, never an incremental edit. |

#### Historical unowned canonical paths

Five canonical owner paths named by the coverage matrix appeared in no scope's
file-ownership table. Searching all ten scope documents for `github`, `.agents`,
`traefik`, `pre-commit`, and a root `policy/` ownership row returned exactly one
match, `meta.md` for `.agents/skills/**`.

| Path | Requirements affected | Historical observation |
| --- | --- | --- |
| `.github/**` | `REQ-WERPC-018`, `REQ-WERPC-022`, `REQ-WERPC-023` | Release, CI/CD, and GitHub Actions named `.github/workflows/` as canonical owner. No scope listed `.github/**`, so workflow changes had no declared scope owner at that observation. |
| `.agents/agents/**` | `REQ-WERPC-027` | `meta` owned `.agents/skills/**` only. The agent definitions themselves were unlisted. |
| `traefik/` | `REQ-WERPC-009` | `infra` owned `infrastructure/**` and `gitops/**`. The top-level `traefik/` tree was unlisted. |
| `.pre-commit-config.yaml` | `REQ-WERPC-024` | Named as a QA canonical owner. `qa` owned `scripts/validate-*.py` and `contracts/**`, not this file. |
| `policy/` (repository root) | `REQ-WERPC-025` | Distinct from `docs/05.operations/policies/**`, which `infra` and `ops` owned. The root `policy/` tree was unlisted. |

This was a scope-registration observation only. It did not establish that any
path was unprotected in practice, because branch protection, CODEOWNERS,
approval boundaries, and hooks were separate controls. The later responsibility
and registry topology supersedes this scope-ownership question.

### Blocked-by-DEFER summary

All twelve `Partial` requirements shared one property: the missing evidence was
unobtainable from the repository alone. Grouping them by blocking evidence class
showed that no further repository-static research could raise any of them.

| Blocking evidence class | Requirements | Why static work cannot close it |
| --- | --- | --- |
| Live cluster, effective RBAC, or real traffic | `REQ-WERPC-008`, `REQ-WERPC-009`, `REQ-WERPC-025` | Manifest text states intent; only a live API server resolves effective permission and reachability. |
| Hosted CI run, rulesets, secrets, environments, OIDC | `REQ-WERPC-022`, `REQ-WERPC-023` | Workflow declarations are static; run outcomes, protection rules, and identity federation exist only on the hosted side. |
| Provider runtime, discovery, parity, or retention | `REQ-WERPC-006`, `REQ-WERPC-026`, `REQ-WERPC-028`, `REQ-WERPC-032` | Adapter configuration is observable; what a provider actually discovers, routes, enforces, and retains at run time is not. |
| Reader, usability, or stakeholder judgement | `REQ-WERPC-014`, `REQ-WERPC-020`, `REQ-WERPC-033` | Structural validity is machine-checkable; whether a reader can act safely, or a product meets intended use, is a human determination. |

The practical consequence for planning is that a `Partial` row is not an
outstanding documentation task. Treating it as one produces repeated research
passes that cannot change its status.

The 2026-08-11 Partial/DEFER incremental refresh, executed on 2026-08-12,
re-tested this grouping against current official sources and one approved
read-only GitHub metadata batch. All twelve rows remained `Partial`, so the
table above was unchanged. The hosted row narrowed but did not close: projected
Actions permissions, the default workflow token setting, the ruleset list,
`main` branch protection, environment totals, and artifact totals were observed
as dated metadata, while OIDC customization stayed `unavailable` and effective
per-run permissions, merge enforcement, bypass and fork behavior, deployment,
promotion, and rollback stayed `DEFER`. The observations and their exact
limitations are recorded in
[CI/CD, Actions, and QA](m0008-ci-cd-github-actions-and-qa.md#2026-08-11-partialdefer-incremental-refresh);
the other affected scopes route to the dated sections listed in the
[pack README](README.md#2026-08-11-partialdefer-refresh-reconciliation).

### 2026-08-14 re-projection re-observation

This bounded re-projection re-read every file under the then-current
`docs/00.agent-governance/scopes/` tree and re-matched each requirement's
canonical owner against that registry. `git diff --stat` against the 2026-08-12
baseline commit (`a5d2dfbb`) returned zero changed scope files, and the
registry's last actual content change (`138ce6ac`) predated that baseline by two
weeks. No row in the historical scope-to-requirement map changed.

The five-path unowned-canonical-path search was re-run against all ten scope
documents and returned the same single match, `meta.md` for
`.agents/skills/**`. No path was adopted during that cycle.

The map excluded `REQ-WERPC-034`, `035`, and `036`: Spec 057 amendment
`C-WRCP-010` admitted the Spec, Task, and Plan document families as three new
pack README coverage-matrix owner rows only. No historical scope row was added
for those IDs.

### 2026-08-17 full-corpus re-projection and blocking-class closure

This re-projection belongs to the 2026-08-17 full-corpus refresh cycle
(WRFC-008) executed under Spec 058. It contributes no new finding, source, or
status. It re-derived scope membership from the then-current registry and, for
the first time in this pack, recorded a terminal blocking class for every
retained `Partial` and `DEFER` row rather than only the twelve `Partial` rows.

#### Historical scope re-derivation result

Scope membership was re-derived from `docs/00.agent-governance/scopes/` rather
than carried forward from the previous projection. The registry contained
exactly ten scope documents. Re-searching all ten for `github`, `.agents`,
`traefik`, `pre-commit`, and a root `policy/` ownership row returned exactly one
match, `meta.md:27` for `.agents/skills/**`.

The five unowned canonical paths were therefore unchanged at that observation.
No scope acquired or released a path, and the map needed no structural revision.

One consequence was that `.github/**` remained unowned while
`REQ-WERPC-022` and `REQ-WERPC-023` were both closed as `hosted-ci` blocked.
Those rows could only be advanced by hosted evidence, and the surface that would
produce it had no declared scope owner. That historical gap was later addressed
before scope routing itself was retired.

#### Terminal blocking-class closure

Every retained `Partial` and `DEFER` row carries exactly one blocking class and
a reopen condition. Of the thirty-six owner rows, twelve are unblocked, ten are
reachable by repository-static work, and fourteen are structurally unreachable.

| Blocking class | Requirements | Reachable | Terminal for static work |
| --- | --- | --- | --- |
| `none` | `REQ-WERPC-007`, `011`, `012`, `013`, `015`, `016`, `017`, `019`, `027`, `029`, `030`, `031` | n/a | n/a |
| `repo-static` | `REQ-WERPC-003`, `004`, `005`, `006`, `010`, `021`, `024`, `034`, `035`, `036` | yes | no |
| `provider-runtime` | `REQ-WERPC-001`, `002`, `026`, `028`, `032` | no | yes |
| `hosted-ci` | `REQ-WERPC-022`, `023` | no | yes |
| `live-cluster` | `REQ-WERPC-008`, `009`, `025` | no | yes |
| `human-judgement` | `REQ-WERPC-014`, `018`, `020`, `033` | no | yes |

The fourteen terminal rows are closed against further repository-static
re-testing. A successor cycle cites this closure instead of re-observing them,
and reopens a row only when its named condition is met.

| Terminal class | What closure means | Named reopen condition |
| --- | --- | --- |
| `provider-runtime` | Manifest and adapter text states configuration; only an authenticated provider run resolves discovery and execution. | Authorized provider-runtime observation, or a provider contract that contradicts rather than extends. |
| `hosted-ci` | Workflow declarations state intent; only a hosted run resolves effective tokens, rulesets, environments, and OIDC. | Authorized hosted-run evidence at the current revision. |
| `live-cluster` | Manifests state intent; only a live API server resolves effective RBAC, admission, and reconciliation. | Operator-authorized live observation. |
| `human-judgement` | No file read supplies a stakeholder record, an approved enforcement decision, or a risk-proportionate review. | A named approval, reviewer record, or reader-validation activity. |

This closure distinguished the cycle from the three that preceded it. Specs
055, 056, and 057 had re-tested a twelve-row `Partial` sample and promoted
nothing because the sample ignored whether its blocking evidence was reachable.
Recording reachability once converted a repeating no-op into a decision.

#### What closure does not authorize

Closure is a statement about evidence reachability, not correctness or safety.
It does not promote status, lower an evidence bar, or permit a reopen condition
to be waived. It grants no current responsibility or write authority.

### 2026-08-20 full-corpus reverification

| Scope | Requests | Evidence depths | Outcome | Blocking classes | Canonical owners |
| --- | --- | --- | --- | --- | --- |
| repository governance | REQ-WERPC-003 | public-documentation | unchanged | repo-static | `docs/90.references/research/0001-workspace-engineering/m0001-workspace-governance-and-common-agent-environment.md` |
| harness and loop | REQ-WERPC-001, REQ-WERPC-002 | repository-static | unchanged | provider-runtime | `docs/90.references/research/0001-workspace-engineering/m0002-harness-and-loop-engineering.md` |
| provider and common environment | REQ-WERPC-004, REQ-WERPC-005, REQ-WERPC-006 | public-documentation, repository-static | changed | repo-static | `docs/90.references/research/0001-workspace-engineering/m0003-provider-implementation-status.md`, `docs/90.references/research/0001-workspace-engineering/m0001-workspace-governance-and-common-agent-environment.md` |
| agents, model, and memory | REQ-WERPC-026, REQ-WERPC-027, REQ-WERPC-028, REQ-WERPC-029, REQ-WERPC-030, REQ-WERPC-031, REQ-WERPC-032 | public-documentation, repository-static | unchanged | provider-runtime | `docs/90.references/research/0001-workspace-engineering/m0011-agent-memory-tiers-and-management.md`, `docs/90.references/research/0001-workspace-engineering/m0010-agent-model-routing-and-configuration.md`, `docs/90.references/research/0001-workspace-engineering/m0009-ai-agents-and-agency-agents.md` |
| SDLC and document contracts | REQ-WERPC-007, REQ-WERPC-010, REQ-WERPC-011, REQ-WERPC-012, REQ-WERPC-013, REQ-WERPC-014, REQ-WERPC-015, REQ-WERPC-016, REQ-WERPC-017, REQ-WERPC-018, REQ-WERPC-019, REQ-WERPC-034, REQ-WERPC-035, REQ-WERPC-036 | public-documentation, repository-static | changed | human-judgement, repo-static | `docs/90.references/research/0001-workspace-engineering/m0004-spec-driven-sdlc-and-document-contracts.md` |
| documentation and knowledge routing | REQ-WERPC-020, REQ-WERPC-021 | repository-static | unchanged | human-judgement, repo-static | `docs/90.references/research/0001-workspace-engineering/m0005-documentation-architecture-and-diataxis.md`, `docs/90.references/research/0001-workspace-engineering/m0006-llm-wiki-and-knowledge-routing.md` |
| Kubernetes and infrastructure | REQ-WERPC-008, REQ-WERPC-009 | repository-static | changed | live-cluster | `docs/90.references/research/0001-workspace-engineering/m0007-kubernetes-infrastructure-and-security.md` |
| security and approval | REQ-WERPC-025 | repository-static | changed | live-cluster | `docs/90.references/research/0001-workspace-engineering/m0007-kubernetes-infrastructure-and-security.md` |
| CI/CD and QA | REQ-WERPC-022, REQ-WERPC-023, REQ-WERPC-024 | repository-static | unchanged | hosted-ci, repo-static | `docs/90.references/research/0001-workspace-engineering/m0008-ci-cd-github-actions-and-qa.md` |
| verification and validation | REQ-WERPC-033 | repository-static | unchanged | human-judgement | `docs/90.references/research/0001-workspace-engineering/m0008-ci-cd-github-actions-and-qa.md` |

### 2026-08-23 Spec 0054-compatible gap projection

The closed incremental ledger extended through `SRC-WERPC-115` and
`CLM-WERPC-014-11`. It changed no requirement status or evidence-class
promotion. This projection routed the new claims without editing the then-frozen
pack README or the two frozen SDLC/documentation topical owners.

| Scope | Claim IDs | Materialized owner | Retained boundary |
| --- | --- | --- | --- |
| harness and loop | `CLM-WERPC-014-01` | [Harness and loop](m0002-harness-and-loop-engineering.md#2026-08-23-provider-control-gap-increment) | Product capability is documented; native discovery, hook delivery, approval outcome, execution, and enforcement completeness remain `provider-runtime` / `DEFER`. |
| provider and common environment | `CLM-WERPC-014-02`, `CLM-WERPC-014-03` | [Provider status](m0003-provider-implementation-status.md#2026-08-23-provider-contract-and-authority-convergence-increment), [common environment](m0001-workspace-governance-and-common-agent-environment.md#2026-08-23-spec-0054-authority-convergence-increment) | Claude/Codex are the terminal projections and shared rules remain provider-neutral; adapter loading, authentication, isolation, and parity remain `DEFER`. |
| SDLC and document contracts | `CLM-WERPC-014-04` | [Ledger addendum](m0012-source-coverage.md#2026-08-23-spec-0054-authority-convergence-addendum); terminal owner remains `m0004-spec-driven-sdlc-and-document-contracts.md` | ISO and spec-driven sources support but do not prescribe the local package. Owner-body materialization, Task sharding, registry/profile activation, and validator cutover remained `DEFER`. |
| documentation and release communication | `CLM-WERPC-014-05` | [Ledger addendum](m0012-source-coverage.md#2026-08-23-spec-0054-authority-convergence-addendum); terminal owner remains `m0005-documentation-architecture-and-diataxis.md` | Diátaxis and GitHub Releases do not define local families or authority. Reader validation, rollout evidence, Stage 90 relocation, and cross-link cutover remained `DEFER`. |
| Kubernetes, infrastructure, and security | `CLM-WERPC-014-06` | [Platform security](m0007-kubernetes-infrastructure-and-security.md#2026-08-23-reconciliation-and-workload-identity-increment) | Desired state, self-heal declarations, and identity guidance do not prove live reconciliation, effective RBAC, admission, or recovery. |
| CI/CD, GitHub Actions, QA, and V&V | `CLM-WERPC-014-07` | [CI/CD and QA](m0008-ci-cd-github-actions-and-qa.md#2026-08-23-conditional-oidc-and-supply-chain-increment) | Repository creation/rename/transfer history, OIDC opt-in/JWT/trust, hosted runs, attestation verification, and intended-use evidence remain `DEFER`. |
| model routing | `CLM-WERPC-014-08` | [Model routing](m0010-agent-model-routing-and-configuration.md#2026-08-23-codex-routing-guidance-gap-increment) | Model names are candidate guidance only; exact resolution, account availability, same-suite fitness, cost, latency, safety, rollback, and approval remain `DEFER`. |
| memory and LLM-WIKI | `CLM-WERPC-014-09`, `CLM-WERPC-014-11` | [Memory tiers](m0011-agent-memory-tiers-and-management.md#2026-08-23-provider-memory-gap-increment), [LLM-WIKI](m0006-llm-wiki-and-knowledge-routing.md#2026-08-20-full-corpus-reverification) | Provider memory is auxiliary and no external source defines the workspace taxonomy; retrieval effectiveness, retention/deletion, promotion, and secure erasure remain `DEFER`. |
| AI agents and agency-agents | `CLM-WERPC-014-10` | [AI agents](m0009-ai-agents-and-agency-agents.md#2026-08-20-full-corpus-reverification) | Upstream was unchanged after the retained baseline; direct import, provider parity, evaluation, model fitness, and admission remained unproven. |

The pack README remained byte-identical to its reviewed transition successor.
This was intentional transition compliance, not a missing source or claim. The
source ledger was the closed evidence owner for the increment, and this index
was its cross-scope router until Spec 0054 performed the Stage 90 cutover.

The ignored Spec 0062 task checker remained frozen to the earlier allocation
ending at `SRC-WERPC-091` and `CLM-WERPC-013-06`; when applied to the later
increment it failed closed with `ERROR INTEGRATION_LEDGER_LEGACY`. That result
was an expected legacy-allocation boundary, not a passing validation. This work
did not widen the ignored checker or revive the legacy `tasks.md` control plane.

### 2026-08-28 closed full-scope revalidation

The requested corpus was re-observed across all 36 requirement owners using
official or primary external sources and named repository-static selectors.
The source ledger extends through `SRC-WERPC-122` and `CLM-WERPC-015-11`. No
requirement status, evidence class, document route, provider adapter, workflow,
manifest, model, memory policy, or live/hosted state was promoted. The only
currentness deltas were new C4/arc42/ADR coverage, an advanced `agency-agents`
main branch, newer upstream kube-state-metrics and Argo CD releases, and
recovered NASA traceability-source availability.

| Scope | Requests re-observed | 2026-08-28 outcome | Claim routing | Closed boundary / reopen condition |
| --- | --- | --- | --- | --- |
| harness, loop, provider, and common environment | REQ-WERPC-001–006 | unchanged | `CLM-WERPC-015-07` | Repository adapters and public provider documents do not prove discovery, hook delivery, child execution, authentication, approval effect, isolation, or Claude/Codex parity; reopen with authorized `provider-runtime` evidence. |
| spec-driven SDLC and lifecycle documents | REQ-WERPC-007, REQ-WERPC-010–019, REQ-WERPC-034–036 | changed coverage, no status effect | `CLM-WERPC-015-01`, `CLM-WERPC-015-02`, `CLM-WERPC-015-08` in the [source delta](m0012-source-coverage.md#2026-08-28-source-delta-increment) | C4 and arc42 are tailorable AD practices and ADR templates are plural; none replaces terminal AD/ADR profiles or activates a Release family. Spec 0054 owner materialization and reader/stakeholder judgement remained `DEFER`. |
| documentation, Diátaxis, and LLM-WIKI | REQ-WERPC-020, REQ-WERPC-021 | unchanged | `CLM-WERPC-015-09` | Documentation modes remain distinct from lifecycle authority; retrieval quality, publication, promotion review, retention/deletion, and reader validation remain `DEFER`. |
| Kubernetes and infrastructure | REQ-WERPC-008, REQ-WERPC-009 | upstream freshness changed, no status effect | `CLM-WERPC-015-04`, `CLM-WERPC-015-05` | v2.20.0/v3.5.2 are review triggers only. Compatibility, effective RBAC, reconciliation, health, recovery, and running versions require approved review or `live-cluster` evidence. |
| security and approval | REQ-WERPC-025 | unchanged | `CLM-WERPC-015-10` | Static workload hardening, identity, admission, and supply-chain guidance do not prove effective RBAC, Vault/ESO health, policy enforcement, artifact trust, or recovery; reopen with `live-cluster` or approved trust evidence. |
| CI/CD, GitHub Actions, and QA | REQ-WERPC-022–024 | unchanged | `CLM-WERPC-015-10` | Tracked workflows still contained no deployment, `id-token: write`, attestation, cloud-login, or environment consumer; repository settings, effective permissions, OIDC/trust, hosted checks, deployment, and rollback remained `hosted-ci` / admin `DEFER`. |
| verification and validation | REQ-WERPC-033 | source availability recovered, no status effect | `CLM-WERPC-015-06` | Bidirectional traceability supports verification planning but does not supply a current trace graph, product conformance, representative users/operators, intended environment, or stakeholder acceptance. |
| AI agents and agency-agents | REQ-WERPC-026, REQ-WERPC-027 | upstream changed, no local effect | `CLM-WERPC-015-03`; it supersedes only the currentness premise of `CLM-WERPC-014-10` | The retained pin remains reproducible and new upstream roles remain inspiration-only; reopen after bounded translation, license/security review, evaluation, approval, and provider-runtime evidence. |
| model routing and memory tiers | REQ-WERPC-028–032 | unchanged | `CLM-WERPC-015-11` | Public model and provider-memory documentation does not prove parser resolution, entitlement, fitness, cost/latency/safety, retention/deletion, secure erasure, or repository authority; configured incumbents and repository-wins semantics remain. |

This is a closed incremental finding ledger, not a claim that every retained
`Partial` or `DEFER` has become reachable. The terminal blocking classes and
their named reopen conditions remain unchanged. No new research directory,
duplicate report, one-time artifact, transitional topology, or legacy checker
expansion was created.

## Sources

- Pre-convergence projection recovery: Git blob `de2fa4e62e10aa9cbfd47e2bbc4fae384390cd8f` at the exact 2026-09-04 baseline.
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
