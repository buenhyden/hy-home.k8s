---
title: 'Reference: Scope Application Index'
type: content/reference
status: draft
owner: platform
updated: 2026-08-11
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

It covers the mapping between `REQ-WERPC-001`–`REQ-WERPC-033` and the ten
governance scopes as they stood on 2026-08-10, the canonical paths that no scope
currently lists, and the shared evidence classes that block the twelve `Partial`
requirements.

It excludes any change to a requirement status, any new external source, and any
evidence that requires cluster, hosted CI, provider runtime, or stakeholder
access.

## Definitions / Facts

### Scope-to-requirement map

Scope membership below is derived by matching each requirement's canonical owner
against the file-ownership globs declared in that scope's own document. A
requirement can appear in more than one scope when its canonical owner spans
several ownership globs.

| Scope                                                               | Related REQ                                                                                                         | Canonical owner paths                                                                                                    | As-Is evidence                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | Recorded gap                                                                                  | DEFER boundary                                                                                                                                                                              | Scope owner next action                                                                                                                                                                                              |
| ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [architecture](../../../00.agent-governance/scopes/architecture.md) | `REQ-WERPC-007`, `REQ-WERPC-012`, `REQ-WERPC-013`, `REQ-WERPC-031`                                                  | `docs/03.specs/`, `docs/02.architecture/requirements/`, `docs/02.architecture/decisions/`                                | [Spec-driven baseline](spec-driven-sdlc-and-document-contracts.md#spec-driven-development-baseline), [Document-family matrix](spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix), [Domain-memory baseline](agent-memory-tiers-and-management.md#domain-scoped-memory-baseline)                                                                                                                                                                                                                                                                         | All four `Verified`                                                                           | Generated-code outcomes, decision quality, and actual retrieval remain `DEFER`                                                                                                              | None required. Static contracts are sourced; treat architecture effectiveness as an unmeasured property, not a passing one                                                                                           |
| [backend](../../../00.agent-governance/scopes/backend.md)           | `REQ-WERPC-007`, `REQ-WERPC-010`, `REQ-WERPC-011`, `REQ-WERPC-031`                                                  | `docs/03.specs/`, `docs/01.requirements/`                                                                                | [Spec-driven baseline](spec-driven-sdlc-and-document-contracts.md#spec-driven-development-baseline), [Document-family matrix](spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix)                                                                                                                                                                                                                                                                                                                                                                       | All four `Verified`                                                                           | Conformance, effectiveness, and stakeholder validation remain `DEFER`                                                                                                                       | None required. Template conformance is not product validation                                                                                                                                                        |
| [docs](../../../00.agent-governance/scopes/docs.md)                 | `REQ-WERPC-014`, `REQ-WERPC-016`, `REQ-WERPC-020`, `REQ-WERPC-021`                                                  | `docs/05.operations/guides/`, `docs/99.templates/`, `docs/90.references/llm-wiki/`                                       | [Document-family matrix](spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix), [Diátaxis baseline](documentation-architecture-and-diataxis.md#diátaxis-baseline), [LLM-WIKI baseline](llm-wiki-and-knowledge-routing.md#llm-wiki-baseline)                                                                                                                                                                                                                                                                                                               | `REQ-WERPC-014` `Partial`, `REQ-WERPC-020` `Partial`                                          | Tutorial classification and usability need a named reader and human review; no static validator infers them                                                                                 | Answered on 2026-08-11: approved Spec 052 `DOC-G2` and `DOC-G3` already decline both routes, and the framework's own instruction not to create empty structures was verified at upstream source. Do not propose these profiles. The open item is `DOC-G1` enum enforcement under the queued `WORK-013` package, owned by its Plan rather than by this scope                                                                     |
| [frontend](../../../00.agent-governance/scopes/frontend.md)         | `REQ-WERPC-007`, `REQ-WERPC-010`, `REQ-WERPC-011`, `REQ-WERPC-031`                                                  | `docs/03.specs/`, `docs/01.requirements/`                                                                                | [Spec-driven baseline](spec-driven-sdlc-and-document-contracts.md#spec-driven-development-baseline), [Document-family matrix](spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix)                                                                                                                                                                                                                                                                                                                                                                       | All four `Verified`                                                                           | Same as `backend`; the two scopes declare identical ownership globs                                                                                                                         | None required. The identical membership is a property of the scope registry, not a mapping error                                                                                                                     |
| [infra](../../../00.agent-governance/scopes/infra.md)               | `REQ-WERPC-008`, `REQ-WERPC-009`, `REQ-WERPC-017`, `REQ-WERPC-019`, `REQ-WERPC-024`, `REQ-WERPC-025`                | `gitops/`, `infrastructure/`, `scripts/`, `docs/05.operations/policies/`, `docs/05.operations/runbooks/`                 | [Kubernetes baseline](kubernetes-infrastructure-and-security.md#kubernetes-baseline), [Infrastructure baseline](kubernetes-infrastructure-and-security.md#infrastructure-baseline), [Security baseline](kubernetes-infrastructure-and-security.md#security-baseline), [QA baseline](ci-cd-github-actions-and-qa.md#qa-baseline)                                                                                                                                                                                                                                                 | `REQ-WERPC-008`, `REQ-WERPC-009`, `REQ-WERPC-025` `Partial`                                   | k3d, gateway, registry, hosted CI, effective RBAC, and live posture remain `DEFER`                                                                                                          | Highest-value bounded item is the `kube-state-metrics` Secret read recorded in `memory/progress.md`; its consumer inventory is already complete. Human approval required before any manifest change                  |
| [meta](../../../00.agent-governance/scopes/meta.md)                 | `REQ-WERPC-001`–`REQ-WERPC-006`, `REQ-WERPC-026`, `REQ-WERPC-028`–`REQ-WERPC-030`, `REQ-WERPC-032`, `REQ-WERPC-033` | `docs/00.agent-governance/`, `AGENTS.md`, `.claude/settings.json`, `.claude/skills/`, `.agents/skills/`, `.codex/`       | [Harness baseline](harness-and-loop-engineering.md#harness-baseline), [Loop baseline](harness-and-loop-engineering.md#loop-baseline), [Claude baseline](provider-implementation-status.md#claude-baseline), [Codex baseline](provider-implementation-status.md#codex-baseline), [Common-system baseline](workspace-governance-and-common-agent-environment.md#common-system-baseline), [Model-routing baseline](agent-model-routing-and-configuration.md#model-routing-baseline), [Memory-management baseline](agent-memory-tiers-and-management.md#memory-management-baseline) | `REQ-WERPC-006`, `REQ-WERPC-026`, `REQ-WERPC-028`, `REQ-WERPC-032`, `REQ-WERPC-033` `Partial` | Provider parity, discovery, permission enforcement, model resolution, cost and latency, retention, and connected-resource behavior all require provider runtime execution, which is `DEFER` | This scope carries the largest `Partial` count. None is closable statically; treat provider runtime evidence as a separate authorized activity, not as pending documentation work                                    |
| [ops](../../../00.agent-governance/scopes/ops.md)                   | `REQ-WERPC-015`, `REQ-WERPC-017`, `REQ-WERPC-019`                                                                   | `docs/05.operations/incidents/`, `docs/05.operations/policies/`, `docs/05.operations/runbooks/`, `infrastructure/tests/` | [Document-family matrix](spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix)                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | All three `Verified`                                                                          | Runtime response, enforcement, rehearsal, and live command safety remain `DEFER`                                                                                                            | None required. A structurally valid runbook is not a rehearsed or authorized one; record rehearsal as evidence when it happens                                                                                       |
| [product](../../../00.agent-governance/scopes/product.md)           | `REQ-WERPC-010`, `REQ-WERPC-011`                                                                                    | `docs/01.requirements/`, `docs/04.execution/plans/`                                                                      | [Spec-driven baseline](spec-driven-sdlc-and-document-contracts.md#spec-driven-development-baseline), [Document-family matrix](spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix)                                                                                                                                                                                                                                                                                                                                                                       | Both `Verified`                                                                               | Stakeholder and product validation remain `DEFER`                                                                                                                                           | None required. Requirements validation is a stakeholder activity, not a validator lane                                                                                                                               |
| [qa](../../../00.agent-governance/scopes/qa.md)                     | `REQ-WERPC-023`, `REQ-WERPC-024`, `REQ-WERPC-029`, `REQ-WERPC-033`                                                  | `scripts/validate-*.py`, `docs/00.agent-governance/contracts/`, `tests/`                                                 | [GitHub Actions baseline](ci-cd-github-actions-and-qa.md#github-actions-baseline), [QA baseline](ci-cd-github-actions-and-qa.md#qa-baseline), [Verification and Validation matrix](ci-cd-github-actions-and-qa.md#verification-and-validation-question-matrix)                                                                                                                                                                                                                                                                                                                  | `REQ-WERPC-023`, `REQ-WERPC-033` `Partial`                                                    | Hosted runs, rulesets, secrets, environments, OIDC, artifacts, and intended-use evidence remain `DEFER`                                                                                     | Keep static `PASS` labelled as bounded conformance evidence. A green lane is verification, never validation of intended use                                                                                          |
| [security](../../../00.agent-governance/scopes/security.md)         | `REQ-WERPC-008`, `REQ-WERPC-015`, `REQ-WERPC-016`, `REQ-WERPC-025`                                                  | `gitops/platform/network-policies/`, `infrastructure/vault/`, `docs/05.operations/incidents/`                            | [Kubernetes baseline](kubernetes-infrastructure-and-security.md#kubernetes-baseline), [Security baseline](kubernetes-infrastructure-and-security.md#security-baseline), [Document-family matrix](spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix)                                                                                                                                                                                                                                                                                                    | `REQ-WERPC-008`, `REQ-WERPC-025` `Partial`                                                    | Effective RBAC, real traffic flows, attestation, and live posture remain `DEFER`                                                                                                            | The absent default-deny ingress posture recorded in `memory/progress.md` is the highest-risk item in the pack. It requires a complete allowed-flow inventory and a security-reviewed Spec, never an incremental edit |

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
[CI/CD, Actions, and QA](ci-cd-github-actions-and-qa.md#2026-08-11-partialdefer-incremental-refresh);
the other affected scopes route to the dated sections listed in the
[pack README](README.md#2026-08-11-partialdefer-refresh-reconciliation).

## Sources

- Workspace observation, 2026-08-10: the
  [Requirement Coverage Matrix](README.md) in this pack's README, read for all
  33 `REQ-WERPC` rows including topic, report anchor, canonical owner, and
  status.
- Workspace observation, 2026-08-10: the ten scope documents under
  `docs/00.agent-governance/scopes/`, read for their `Authority Boundary` file
  ownership tables.

Both are repository-static observations of tracked files. This document
introduces no external source and adds no row to the
[source register](source-coverage-and-migration-ledger.md#source-register).

## Review and Freshness

Refresh when a scope's file-ownership table changes, when a governance scope is
added or retired, when a `REQ-WERPC` status changes, or when the pack README's
coverage matrix changes. The `docs` row was updated on 2026-08-11 after the
tutorial and explanation question resolved to an existing approved decision. `docs/00.agent-governance/scopes/` is the current-truth
owner for every scope statement here, and the pack README is the current-truth
owner for every status. Scope and matrix observation is dated 2026-08-10.

The unowned-path list is the most drift-prone section, because adding a single
ownership row to any scope document invalidates it without touching this file.

## Related Documents

- [Pack README and coverage matrix](README.md)
- [Governance scopes](../../../00.agent-governance/scopes/)
- [Harness and loop](harness-and-loop-engineering.md)
- [Provider status](provider-implementation-status.md)
- [Workspace governance](workspace-governance-and-common-agent-environment.md)
- [SDLC contracts](spec-driven-sdlc-and-document-contracts.md)
- [Documentation architecture](documentation-architecture-and-diataxis.md)
- [LLM-WIKI routing](llm-wiki-and-knowledge-routing.md)
- [Platform security](kubernetes-infrastructure-and-security.md)
- [CI/CD and QA](ci-cd-github-actions-and-qa.md)
- [AI agents](ai-agents-and-agency-agents.md)
- [Model routing](agent-model-routing-and-configuration.md)
- [Memory](agent-memory-tiers-and-management.md)
- [Source and migration ledger](source-coverage-and-migration-ledger.md)
