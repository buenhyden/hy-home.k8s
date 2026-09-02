---
title: 'Reference: Scope Application Index'
version: "1.0"
type: content/research-reference
layer: "90.references"
status: draft
owner: platform
updated: 2026-08-31
artifact_id: "RES-0001-m0013"
---

# Reference: Scope Application Index

## Overview

This index re-projects the findings of this pack onto the ten canonical
governance scopes so that a scope owner can reach the requirements that bind
their paths without reading all twelve topical reports. The pack is organised by
research topic; this document is the same evidence organised by who owns the
affected surface. It contributes no new finding, source, or status.

## Reference Type

Routing index over existing dated research. It is not a research report, not a
scope contract, not a permission grant, and not a backlog.

## Authority Boundary

`docs/00.agent-governance/scopes/` remains the authoritative owner of scope
membership, file ownership, and write permission. This index cannot create a
scope, widen a scope, assign an owner, or promote a research finding into
policy. A requirement appearing in a scope row means the research touched a path
that the scope already owns; it does not mean the scope acquired new authority.

Where this document notes that a canonical path appears in no scope's
file-ownership table, that is a repository-static observation about the current
scope registry. It is not an instruction to add the path, and adopting or
deliberately declining any such path is a `meta` scope decision that requires
human approval.

No status in this index may differ from the pack README's
[Requirement Coverage Matrix](README.md). Where the two disagree, the README is
correct and this index is stale.

## Scope

Its base map covers `REQ-WERPC-001`–`REQ-WERPC-033` and the ten governance
scopes as they stood on 2026-08-14. The 2026-08-28 pack-level addendum also
routes `REQ-WERPC-034`–`REQ-WERPC-036` without claiming a current scope-topology
projection. Current scope ownership always comes from the scope registry, not
from this dated map.

It excludes any change to a requirement status, any new external source, and any
evidence that requires cluster, hosted CI, provider runtime, or stakeholder
access.

## Definitions / Facts

### Scope-to-requirement map

Scope membership below is derived by matching each requirement's canonical owner
against the file-ownership globs declared in that scope's own document. A
requirement can appear in more than one scope when its canonical owner spans
several ownership globs.

Scope labels below now link to current responsibility owners. The 2026-08-14
membership, owner-path observations, gaps, and dispositions remain unchanged;
the new links do not make current role routing evidence for those historical globs.

| Scope                                                               | Related REQ                                                                                                         | Canonical owner paths                                                                                                    | As-Is evidence                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | Recorded gap                                                                                  | DEFER boundary                                                                                                                                                                              | Scope owner next action                                                                                                                                                                                                                                                                                                                                     |
| ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [architecture](../../../00.agent-governance/roles/architecture.md) | `REQ-WERPC-007`, `REQ-WERPC-012`, `REQ-WERPC-013`, `REQ-WERPC-031`                                                  | `docs/03.specs/`, `docs/02.architecture/requirements/`, `docs/02.architecture/decisions/`                                | [Spec-driven baseline](m0004-spec-driven-sdlc-and-document-contracts.md#spec-driven-development-baseline), [Document-family matrix](m0004-spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix), [Domain-memory baseline](m0011-agent-memory-tiers-and-management.md#domain-scoped-memory-baseline)                                                                                                                                                                                                                                                                         | All four `Verified`                                                                           | Generated-code outcomes, decision quality, and actual retrieval remain `DEFER`                                                                                                              | None required. Static contracts are sourced; treat architecture effectiveness as an unmeasured property, not a passing one                                                                                                                                                                                                                                  |
| [backend](../../../00.agent-governance/roles/README.md)           | `REQ-WERPC-007`, `REQ-WERPC-010`, `REQ-WERPC-011`, `REQ-WERPC-031`                                                  | `docs/03.specs/`, `docs/01.requirements/`                                                                                | [Spec-driven baseline](m0004-spec-driven-sdlc-and-document-contracts.md#spec-driven-development-baseline), [Document-family matrix](m0004-spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix)                                                                                                                                                                                                                                                                                                                                                                       | All four `Verified`                                                                           | Conformance, effectiveness, and stakeholder validation remain `DEFER`                                                                                                                       | None required. Template conformance is not product validation                                                                                                                                                                                                                                                                                               |
| [docs](../../../00.agent-governance/roles/documentation.md)                 | `REQ-WERPC-014`, `REQ-WERPC-016`, `REQ-WERPC-020`, `REQ-WERPC-021`                                                  | `docs/05.operations/guides/`, `docs/99.templates/`, historical observation: `docs/90.references/llm-wiki/`                | [Document-family matrix](m0004-spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix), [Diátaxis baseline](m0005-documentation-architecture-and-diataxis.md#diátaxis-baseline), [historical LLM-WIKI baseline](m0006-llm-wiki-and-knowledge-routing.md#llm-wiki-baseline)                                                                                                                                                                                                                                                                                                    | `REQ-WERPC-014` `Partial`, `REQ-WERPC-020` `Partial`                                          | Tutorial classification and usability need a named reader and human review; no static validator infers them                                                                                 | Answered on 2026-08-11: approved Spec 052 `DOC-G2` and `DOC-G3` already decline both routes, and the framework's own instruction not to create empty structures was verified at upstream source. Do not propose these profiles. The open item is `DOC-G1` enum enforcement under the queued `WORK-013` package, owned by its Plan rather than by this scope |
| [frontend](../../../00.agent-governance/roles/README.md)         | `REQ-WERPC-007`, `REQ-WERPC-010`, `REQ-WERPC-011`, `REQ-WERPC-031`                                                  | `docs/03.specs/`, `docs/01.requirements/`                                                                                | [Spec-driven baseline](m0004-spec-driven-sdlc-and-document-contracts.md#spec-driven-development-baseline), [Document-family matrix](m0004-spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix)                                                                                                                                                                                                                                                                                                                                                                       | All four `Verified`                                                                           | Same as `backend`; the two scopes declare identical ownership globs                                                                                                                         | None required. The identical membership is a property of the scope registry, not a mapping error                                                                                                                                                                                                                                                            |
| [infra](../../../00.agent-governance/roles/infrastructure.md)               | `REQ-WERPC-008`, `REQ-WERPC-009`, `REQ-WERPC-017`, `REQ-WERPC-019`, `REQ-WERPC-024`, `REQ-WERPC-025`                | `gitops/`, `infrastructure/`, `scripts/`, `docs/05.operations/policies/`, `docs/05.operations/runbooks/`                 | [Kubernetes baseline](m0007-kubernetes-infrastructure-and-security.md#kubernetes-baseline), [Infrastructure baseline](m0007-kubernetes-infrastructure-and-security.md#infrastructure-baseline), [Security baseline](m0007-kubernetes-infrastructure-and-security.md#security-baseline), [QA baseline](m0008-ci-cd-github-actions-and-qa.md#qa-baseline)                                                                                                                                                                                                                                                 | `REQ-WERPC-008`, `REQ-WERPC-009`, `REQ-WERPC-025` `Partial`                                   | k3d, gateway, registry, hosted CI, effective RBAC, and live posture remain `DEFER`                                                                                                          | Highest-value bounded item is the `kube-state-metrics` Secret read recorded in `memory/progress.md`; its consumer inventory is already complete. Human approval required before any manifest change                                                                                                                                                         |
| [meta](../../../00.agent-governance/roles/supervision.md)                 | `REQ-WERPC-001`–`REQ-WERPC-006`, `REQ-WERPC-026`, `REQ-WERPC-028`–`REQ-WERPC-030`, `REQ-WERPC-032`, `REQ-WERPC-033` | `docs/00.agent-governance/`, `AGENTS.md`, `.claude/settings.json`, `.claude/skills/`, `.agents/skills/`, `.codex/`       | [Harness baseline](m0002-harness-and-loop-engineering.md#harness-baseline), [Loop baseline](m0002-harness-and-loop-engineering.md#loop-baseline), [Claude baseline](m0003-provider-implementation-status.md#claude-baseline), [Codex baseline](m0003-provider-implementation-status.md#codex-baseline), [Common-system baseline](m0001-workspace-governance-and-common-agent-environment.md#common-system-baseline), [Model-routing baseline](m0010-agent-model-routing-and-configuration.md#model-routing-baseline), [Memory-management baseline](m0011-agent-memory-tiers-and-management.md#memory-management-baseline) | `REQ-WERPC-006`, `REQ-WERPC-026`, `REQ-WERPC-028`, `REQ-WERPC-032`, `REQ-WERPC-033` `Partial` | Provider parity, discovery, permission enforcement, model resolution, cost and latency, retention, and connected-resource behavior all require provider runtime execution, which is `DEFER` | This scope carries the largest `Partial` count. None is closable statically; treat provider runtime evidence as a separate authorized activity, not as pending documentation work                                                                                                                                                                           |
| [ops](../../../00.agent-governance/roles/operations.md)                   | `REQ-WERPC-015`, `REQ-WERPC-017`, `REQ-WERPC-019`                                                                   | `docs/05.operations/incidents/`, `docs/05.operations/policies/`, `docs/05.operations/runbooks/`, `infrastructure/tests/` | [Document-family matrix](m0004-spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix)                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | All three `Verified`                                                                          | Runtime response, enforcement, rehearsal, and live command safety remain `DEFER`                                                                                                            | None required. A structurally valid runbook is not a rehearsed or authorized one; record rehearsal as evidence when it happens                                                                                                                                                                                                                              |
| [product](../../../00.agent-governance/roles/README.md)           | `REQ-WERPC-010`, `REQ-WERPC-011`                                                                                    | `docs/01.requirements/`, `docs/04.execution/plans/`                                                                      | [Spec-driven baseline](m0004-spec-driven-sdlc-and-document-contracts.md#spec-driven-development-baseline), [Document-family matrix](m0004-spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix)                                                                                                                                                                                                                                                                                                                                                                       | Both `Verified`                                                                               | Stakeholder and product validation remain `DEFER`                                                                                                                                           | None required. Requirements validation is a stakeholder activity, not a validator lane                                                                                                                                                                                                                                                                      |
| [qa](../../../00.agent-governance/roles/quality.md)                     | `REQ-WERPC-023`, `REQ-WERPC-024`, `REQ-WERPC-029`, `REQ-WERPC-033`                                                  | `scripts/validate-*.py`, `docs/00.agent-governance/contracts/`, `tests/`                                                 | [GitHub Actions baseline](m0008-ci-cd-github-actions-and-qa.md#github-actions-baseline), [QA baseline](m0008-ci-cd-github-actions-and-qa.md#qa-baseline), [Verification and Validation matrix](m0008-ci-cd-github-actions-and-qa.md#verification-and-validation-question-matrix)                                                                                                                                                                                                                                                                                                                  | `REQ-WERPC-023`, `REQ-WERPC-033` `Partial`                                                    | Hosted runs, rulesets, secrets, environments, OIDC, artifacts, and intended-use evidence remain `DEFER`                                                                                     | Keep static `PASS` labelled as bounded conformance evidence. A green lane is verification, never validation of intended use                                                                                                                                                                                                                                 |
| [security](../../../00.agent-governance/roles/security.md)         | `REQ-WERPC-008`, `REQ-WERPC-015`, `REQ-WERPC-016`, `REQ-WERPC-025`                                                  | `gitops/platform/network-policies/`, `infrastructure/vault/`, `docs/05.operations/incidents/`                            | [Kubernetes baseline](m0007-kubernetes-infrastructure-and-security.md#kubernetes-baseline), [Security baseline](m0007-kubernetes-infrastructure-and-security.md#security-baseline), [Document-family matrix](m0004-spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix)                                                                                                                                                                                                                                                                                                    | `REQ-WERPC-008`, `REQ-WERPC-025` `Partial`                                                    | Effective RBAC, real traffic flows, attestation, and live posture remain `DEFER`                                                                                                            | The absent default-deny ingress posture recorded in `memory/progress.md` is the highest-risk item in the pack. It requires a complete allowed-flow inventory and a security-reviewed Spec, never an incremental edit                                                                                                                                        |

### Unowned canonical paths

Five canonical owner paths named by the coverage matrix appear in no scope's
file-ownership table. Searching all ten scope documents for `github`, `.agents`,
`traefik`, `pre-commit`, and a root `policy/` ownership row returns exactly one
match, `meta.md` for `.agents/skills/**`.

| Path                        | Requirements affected                             | Observation                                                                                                                                                        |
| --------------------------- | ------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `.github/**`                | `REQ-WERPC-018`, `REQ-WERPC-022`, `REQ-WERPC-023` | Release, CI/CD, and GitHub Actions all name `.github/workflows/` as canonical owner. No scope lists `.github/**`, so workflow changes have no declared scope owner |
| `.agents/agents/**`         | `REQ-WERPC-027`                                   | `meta` owns `.agents/skills/**` only. The agent definitions themselves are unlisted                                                                                |
| `traefik/`                  | `REQ-WERPC-009`                                   | `infra` owns `infrastructure/**` and `gitops/**`. The top-level `traefik/` tree is unlisted                                                                        |
| `.pre-commit-config.yaml`   | `REQ-WERPC-024`                                   | Named as a QA canonical owner. `qa` owns `scripts/validate-*.py` and `contracts/**`, not this file                                                                 |
| `policy/` (repository root) | `REQ-WERPC-025`                                   | Distinct from `docs/05.operations/policies/**`, which `infra` and `ops` do own. The root `policy/` tree is unlisted                                                |

This is a scope-registration observation only. It does not establish that any of
these paths is unprotected in practice, because branch protection, CODEOWNERS,
approval boundaries, and hooks are separate controls that this index did not
examine. Whether each path should be adopted by an existing scope, split across
scopes, or deliberately left unowned is a `meta` decision requiring human
approval.

### Blocked-by-DEFER summary

All twelve `Partial` requirements share one property: the missing evidence is
unobtainable from the repository alone. Grouping them by blocking evidence class
shows that no further repository-static research can raise any of them.

| Blocking evidence class                              | Requirements                                                       | Why static work cannot close it                                                                                                      |
| ---------------------------------------------------- | ------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------ |
| Live cluster, effective RBAC, or real traffic        | `REQ-WERPC-008`, `REQ-WERPC-009`, `REQ-WERPC-025`                  | Manifest text states intent; only a live API server resolves effective permission and reachability                                   |
| Hosted CI run, rulesets, secrets, environments, OIDC | `REQ-WERPC-022`, `REQ-WERPC-023`                                   | Workflow declarations are static; run outcomes, protection rules, and identity federation exist only on the hosted side              |
| Provider runtime, discovery, parity, or retention    | `REQ-WERPC-006`, `REQ-WERPC-026`, `REQ-WERPC-028`, `REQ-WERPC-032` | Adapter configuration is observable; what a provider actually discovers, routes, enforces, and retains at run time is not            |
| Reader, usability, or stakeholder judgement          | `REQ-WERPC-014`, `REQ-WERPC-020`, `REQ-WERPC-033`                  | Structural validity is machine-checkable; whether a reader can act safely, or a product meets intended use, is a human determination |

The practical consequence for planning is that a `Partial` row is not an
outstanding documentation task. Treating it as one produces repeated research
passes that cannot change its status.

The 2026-08-11 Partial/DEFER incremental refresh, executed on 2026-08-12,
re-tested this grouping against current official sources and one approved
read-only GitHub metadata batch. All twelve rows remained `Partial`, so the
table above is unchanged. The hosted row narrowed but did not close: projected
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

This bounded re-projection re-read every file under
`docs/00.agent-governance/scopes/` and re-matched each requirement's canonical
owner against the current registry. `git diff --stat` against the 2026-08-12
baseline commit (`a5d2dfbb`) for `docs/00.agent-governance/scopes/` returned
zero changed files, and the directory's last actual content change
(`138ce6ac`) predates that baseline by two weeks (2026-07-29). No row in the
scope-to-requirement map above changed as a result; none needed to.

The five-path unowned-canonical-path search was re-run against all ten scope
documents and returned the same single match recorded above, `meta.md` for
`.agents/skills/**`. `.github/**`, `.agents/agents/**`, `traefik/`,
`.pre-commit-config.yaml`, and root `policy/` remain unowned by any scope's
file-ownership table. No path was adopted; adoption remains a `meta` decision
requiring human approval and was not performed here.

This document's declared Scope excludes `REQ-WERPC-034`, `035`, and `036`:
Spec 057 amendment `C-WRCP-010` admits the Spec, Task, and Plan document
families as three new pack README coverage-matrix owner rows only (see the
pack [README](README.md#2026-08-14-consistency-and-partial-re-observation-reconciliation)).
This index's mapping stays bounded to `REQ-WERPC-001`–`REQ-WERPC-033`; no
scope row was added for the three new IDs, and doing so was out of scope for
this re-projection.

### 2026-08-17 full-corpus re-projection and blocking-class closure

This re-projection belongs to the 2026-08-17 full-corpus refresh cycle
(WRFC-008) executed under Spec 058. It contributes no new finding, source, or
status. It re-derives scope membership from the registry and, for the first time
in this pack, records a terminal blocking class for every retained `Partial` and
`DEFER` row rather than only the twelve `Partial` rows.

#### Scope re-derivation result

Scope membership was re-derived from `docs/00.agent-governance/scopes/` rather
than carried forward from the previous projection. The registry still contains
exactly ten scope documents. Re-searching all ten for `github`, `.agents`,
`traefik`, `pre-commit`, and a root `policy/` ownership row returns exactly one
match, `meta.md:27` for `.agents/skills/**`.

The five unowned canonical paths recorded above are therefore **unchanged**. No
scope acquired or released a path this cycle, and the scope-to-requirement map
needs no structural revision.

One consequence is worth stating plainly. `.github/**` remains unowned while
`REQ-WERPC-022` and `REQ-WERPC-023` are both closed below as `hosted-ci`
blocked. Those two rows can only be advanced by hosted evidence, and the surface
that would produce it has no declared scope owner. Assigning that ownership
remains a `meta` decision requiring human approval and is not made here.

#### Terminal blocking-class closure

Every retained `Partial` and `DEFER` row now carries exactly one blocking class
and a reopen condition. Of the thirty-six owner rows, twelve are unblocked, ten
are reachable by repository-static work, and fourteen are structurally
unreachable.

| Blocking class     | Requirements                                                                                                       | Reachable | Terminal for static work |
| ------------------ | ------------------------------------------------------------------------------------------------------------------ | --------- | ------------------------ |
| `none`             | `REQ-WERPC-007`, `011`, `012`, `013`, `015`, `016`, `017`, `019`, `027`, `029`, `030`, `031`                        | n/a       | n/a                      |
| `repo-static`      | `REQ-WERPC-003`, `004`, `005`, `006`, `010`, `021`, `024`, `034`, `035`, `036`                                      | yes       | no                       |
| `provider-runtime` | `REQ-WERPC-001`, `002`, `026`, `028`, `032`                                                                        | no        | yes                      |
| `hosted-ci`        | `REQ-WERPC-022`, `023`                                                                                             | no        | yes                      |
| `live-cluster`     | `REQ-WERPC-008`, `009`, `025`                                                                                      | no        | yes                      |
| `human-judgement`  | `REQ-WERPC-014`, `018`, `020`, `033`                                                                               | no        | yes                      |

The fourteen rows marked terminal are closed against further repository-static
re-testing. A successor cycle cites this closure instead of re-observing them,
and reopens a row only when its named condition is met.

| Terminal class     | What closure means                                                                                                  | Named reopen condition                                                                              |
| ------------------ | ------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| `provider-runtime` | Manifest and adapter text states configuration; only an authenticated provider run resolves discovery and execution   | Authorized provider-runtime observation, or a provider contract that contradicts rather than extends |
| `hosted-ci`        | Workflow declarations state intent; only a hosted run resolves effective tokens, rulesets, environments, and OIDC     | Authorized hosted-run evidence at the current revision                                              |
| `live-cluster`     | Manifests state intent; only a live API server resolves effective RBAC, admission, and reconciliation                | Operator-authorized live observation                                                                |
| `human-judgement`  | No file read supplies a stakeholder record, an approved enforcement decision, or a risk-proportionate review          | A named approval, reviewer record, or reader-validation activity                                    |

This closure is the deliverable that distinguishes this cycle from the three that
preceded it. Specs 055, 056, and 057 each re-tested a twelve-row `Partial` sample
and promoted nothing, because the sample was drawn without regard to whether the
blocking evidence was reachable at all. Recording reachability once converts a
repeating no-op into a decision.

#### What closure does not authorize

Closure is a statement about evidence reachability, not about correctness or
safety. It does not promote any status, does not lower any evidence bar, and does
not permit a reopen condition to be waived once met. It grants no scope
authority: a requirement appearing in a scope row still means only that the
research touched a path the scope already owns.

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

The closed incremental ledger now extends through `SRC-WERPC-115` and
`CLM-WERPC-014-11`. It changes no requirement status or evidence-class
promotion. This projection routes the new claims without editing the frozen
pack README or the two frozen SDLC/documentation topical owners. Those owner
body and path changes remain with the queued Spec 0054 Stage 90 work packages.

| Scope | Claim IDs | Materialized owner | Retained boundary |
| --- | --- | --- | --- |
| harness and loop | `CLM-WERPC-014-01` | [Harness and loop](m0002-harness-and-loop-engineering.md#2026-08-23-provider-control-gap-increment) | Product capability is documented; native discovery, hook delivery, approval outcome, execution, and enforcement completeness remain `provider-runtime` / `DEFER`. |
| provider and common environment | `CLM-WERPC-014-02`, `CLM-WERPC-014-03` | [Provider status](m0003-provider-implementation-status.md#2026-08-23-provider-contract-and-authority-convergence-increment), [common environment](m0001-workspace-governance-and-common-agent-environment.md#2026-08-23-spec-0054-authority-convergence-increment) | Claude/Codex are the terminal projections and shared rules remain provider-neutral; adapter loading, authentication, isolation, and parity remain `DEFER`. |
| SDLC and document contracts | `CLM-WERPC-014-04` | [Ledger addendum](m0012-source-coverage.md#2026-08-23-spec-0054-authority-convergence-addendum); terminal owner remains `m0004-spec-driven-sdlc-and-document-contracts.md` | ISO and spec-driven sources support but do not prescribe the local package. Owner-body materialization, Task sharding, registry/profile activation, and validator cutover remain `DEFER`. |
| documentation and release communication | `CLM-WERPC-014-05` | [Ledger addendum](m0012-source-coverage.md#2026-08-23-spec-0054-authority-convergence-addendum); terminal owner remains `m0005-documentation-architecture-and-diataxis.md` | Diátaxis and GitHub Releases do not define local families or authority. Reader validation, rollout evidence, Stage 90 relocation, and cross-link cutover remain `DEFER`. |
| Kubernetes, infrastructure, and security | `CLM-WERPC-014-06` | [Platform security](m0007-kubernetes-infrastructure-and-security.md#2026-08-23-reconciliation-and-workload-identity-increment) | Desired state, self-heal declarations, and identity guidance do not prove live reconciliation, effective RBAC, admission, or recovery. |
| CI/CD, GitHub Actions, QA, and V&V | `CLM-WERPC-014-07` | [CI/CD and QA](m0008-ci-cd-github-actions-and-qa.md#2026-08-23-conditional-oidc-and-supply-chain-increment) | Repository creation/rename/transfer history, OIDC opt-in/JWT/trust, hosted runs, attestation verification, and intended-use evidence remain `DEFER`. |
| model routing | `CLM-WERPC-014-08` | [Model routing](m0010-agent-model-routing-and-configuration.md#2026-08-23-codex-routing-guidance-gap-increment) | Model names are candidate guidance only; exact resolution, account availability, same-suite fitness, cost, latency, safety, rollback, and approval remain `DEFER`. |
| memory and LLM-WIKI | `CLM-WERPC-014-09`, `CLM-WERPC-014-11` | [Memory tiers](m0011-agent-memory-tiers-and-management.md#2026-08-23-provider-memory-gap-increment), [LLM-WIKI](m0006-llm-wiki-and-knowledge-routing.md#2026-08-20-full-corpus-reverification) | Provider memory is auxiliary and no external source defines the workspace taxonomy; retrieval effectiveness, retention/deletion, promotion, and secure erasure remain `DEFER`. |
| AI agents and agency-agents | `CLM-WERPC-014-10` | [AI agents](m0009-ai-agents-and-agency-agents.md#2026-08-20-full-corpus-reverification) | Upstream is unchanged after the retained baseline; direct import, provider parity, evaluation, model fitness, and admission remain unproven. |

The pack README remains byte-identical to its reviewed transition successor.
This is intentional transition compliance, not a missing source or claim: the
source ledger is the closed evidence owner for this increment, and this scope
index is its cross-scope router until Spec 0054 performs the atomic Stage 90
owner and consumer cutover.

The ignored Spec 0062 task checker remains frozen to the earlier allocation
ending at `SRC-WERPC-091` and `CLM-WERPC-013-06`; when applied to this later
increment it fails closed with `ERROR INTEGRATION_LEDGER_LEGACY`. That result is
an expected legacy-allocation boundary, not a passing validation. This work does
not widen the ignored checker or revive the legacy `tasks.md` control plane;
Spec 0054 owns the terminal Task registry and validator/command cutover.

### 2026-08-28 closed full-scope revalidation

The requested corpus was re-observed across all 36 requirement owners using
official or primary external sources and named repository-static selectors.
The source ledger now extends through `SRC-WERPC-122` and
`CLM-WERPC-015-11`. No requirement status, evidence class, document route,
provider adapter, workflow, manifest, model, memory policy, or
live/hosted state is promoted. The only currentness deltas are the new
C4/arc42/ADR coverage, an advanced `agency-agents` main branch, newer upstream
kube-state-metrics and Argo CD releases, and recovered NASA traceability-source
availability.

| Scope | Requests re-observed | 2026-08-28 outcome | Claim routing | Closed boundary / reopen condition |
| --- | --- | --- | --- | --- |
| harness, loop, provider, and common environment | REQ-WERPC-001–006 | unchanged | `CLM-WERPC-015-07` | Repository adapters and public provider documents do not prove discovery, hook delivery, child execution, authentication, approval effect, isolation, or Claude/Codex parity; reopen with authorized `provider-runtime` evidence. |
| spec-driven SDLC and lifecycle documents | REQ-WERPC-007, REQ-WERPC-010–019, REQ-WERPC-034–036 | changed coverage, no status effect | `CLM-WERPC-015-01`, `CLM-WERPC-015-02`, `CLM-WERPC-015-08` in the [source delta](m0012-source-coverage.md#2026-08-28-source-delta-increment) | C4 and arc42 are tailorable AD practices and ADR templates are plural; none replaces terminal AD/ADR profiles or activates a Release family. Spec 0054 owner materialization and reader/stakeholder judgement remain `DEFER`. |
| documentation, Diátaxis, and LLM-WIKI | REQ-WERPC-020, REQ-WERPC-021 | unchanged | `CLM-WERPC-015-09` | Documentation modes remain distinct from lifecycle authority; retrieval quality, publication, promotion review, retention/deletion, and reader validation remain `DEFER`. |
| Kubernetes and infrastructure | REQ-WERPC-008, REQ-WERPC-009 | upstream freshness changed, no status effect | `CLM-WERPC-015-04`, `CLM-WERPC-015-05` | v2.20.0/v3.5.2 are review triggers only. Compatibility, effective RBAC, reconciliation, health, recovery, and running versions require approved review or `live-cluster` evidence. |
| security and approval | REQ-WERPC-025 | unchanged | `CLM-WERPC-015-10` | Static workload hardening, identity, admission, and supply-chain guidance do not prove effective RBAC, Vault/ESO health, policy enforcement, artifact trust, or recovery; reopen with `live-cluster` or approved trust evidence. |
| CI/CD, GitHub Actions, and QA | REQ-WERPC-022–024 | unchanged | `CLM-WERPC-015-10` | Tracked workflows still contain no deployment, `id-token: write`, attestation, cloud-login, or environment consumer; repository settings, effective permissions, OIDC/trust, hosted checks, deployment, and rollback remain `hosted-ci` / admin `DEFER`. |
| verification and validation | REQ-WERPC-033 | source availability recovered, no status effect | `CLM-WERPC-015-06` | Bidirectional traceability supports verification planning but does not supply a current trace graph, product conformance, representative users/operators, intended environment, or stakeholder acceptance. |
| AI agents and agency-agents | REQ-WERPC-026, REQ-WERPC-027 | upstream changed, no local effect | `CLM-WERPC-015-03`; it supersedes only the currentness premise of `CLM-WERPC-014-10` | The retained pin remains reproducible and new upstream roles remain inspiration-only; reopen after bounded translation, license/security review, evaluation, approval, and provider-runtime evidence. |
| model routing and memory tiers | REQ-WERPC-028–032 | unchanged | `CLM-WERPC-015-11` | Public model and provider-memory documentation does not prove parser resolution, entitlement, fitness, cost/latency/safety, retention/deletion, secure erasure, or repository authority; configured incumbents and repository-wins semantics remain. |

This is a closed incremental finding ledger, not a claim that every retained
`Partial` or `DEFER` has become reachable. The terminal blocking classes and
their named reopen conditions remain unchanged. No new research directory,
duplicate report, one-time artifact, transitional topology, or legacy checker
expansion was created. The pack README and frozen SDLC/documentation owner
bodies remain byte-unmodified for the queued Spec 0054 Stage 90 cutover.

## Sources

- Workspace observation, 2026-08-14: the
  [Requirement Coverage Matrix](README.md) in this pack's README, re-read for
  all 36 `REQ-WERPC` rows (`REQ-WERPC-001`–`REQ-WERPC-036`) including topic,
  report anchor, canonical owner, and status.
- Workspace observation, 2026-08-14: the ten scope documents under
  `docs/00.agent-governance/scopes/`, re-read for their `Authority Boundary`
  file ownership tables.

Both are repository-static observations of tracked files. This document
introduces no external source and adds no row to the
[source register](m0012-source-coverage.md#source-register).

## Review and Freshness

Refresh when a scope's file-ownership table changes, when a governance scope is
added or retired, when a `REQ-WERPC` status changes, or when the pack README's
coverage matrix changes. The `docs` row was updated on 2026-08-11 after the
tutorial and explanation question resolved to an existing approved decision. `docs/00.agent-governance/scopes/` is the current-truth
owner for every scope statement here, and the pack README is the current-truth
owner for every status. The base scope-map observation remains dated
2026-08-14; the 2026-08-28 addendum does not claim a scope-registry refresh.

The unowned-path list is the most drift-prone section, because adding a single
ownership row to any scope document invalidates it without touching this file.

## Related Documents

- [Pack README and coverage matrix](README.md)
- [Agent Responsibilities](../../../00.agent-governance/roles/README.md)
- [Harness and loop](m0002-harness-and-loop-engineering.md)
- [Provider status](m0003-provider-implementation-status.md)
- [Workspace governance](m0001-workspace-governance-and-common-agent-environment.md)
- [SDLC contracts](m0004-spec-driven-sdlc-and-document-contracts.md)
- [Documentation architecture](m0005-documentation-architecture-and-diataxis.md)
- [LLM-WIKI routing](m0006-llm-wiki-and-knowledge-routing.md)
- [Platform security](m0007-kubernetes-infrastructure-and-security.md)
- [CI/CD and QA](m0008-ci-cd-github-actions-and-qa.md)
- [AI agents](m0009-ai-agents-and-agency-agents.md)
- [Model routing](m0010-agent-model-routing-and-configuration.md)
- [Memory](m0011-agent-memory-tiers-and-management.md)
- [Source and migration ledger](m0012-source-coverage.md)
