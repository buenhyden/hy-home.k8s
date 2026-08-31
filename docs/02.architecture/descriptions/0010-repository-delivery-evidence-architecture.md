---
title: 'Repository Delivery Evidence Architecture Description'
type: sdlc/ad
status: active
owner: platform
updated: 2026-09-01
artifact_id: "AD-0010"
---

# Repository Delivery Evidence Architecture Description (AD)

## Overview

This architecture defines a repository-static assurance control plane for the
delivery and platform surfaces covered by PRD-0007. It layers routing,
projection, validation depth, evidence classification, review, and rollback on
top of the current platform and document contracts without creating a second
platform topology owner.

AD-0010 is active for the accepted ADR-0021 program decision and the active
Spec 047 foundation tranche.

The architecture consumes the existing validation-surface registry, document
profiles, current local GitOps baseline, protected-surface validators, CI
workflow topology, and the latest external research as non-authoritative
support. Current behavior and versions come from executable repository owners,
not Stage 90 mirrors.

## Boundaries & Non-goals

- **Owns**: repository delivery assurance boundaries; GitHub projection parity;
  platform validation depth; exact tool and fallback evidence; ordered tranche
  execution; and local integration evidence.
- **Consumes**: REQ-0004/AD-0007/ADR-0014/Spec 008 current topology,
  `scripts/validation/registry.json` path routing, workflows, validators, tests,
  desired state, executable configuration, and reviewed dependency locks.
- **Does not own**: platform component selection, live reconciliation state,
  document-profile route definitions, provider installation or authentication,
  branch-protection policy, cloud resources, credentials, or secret values.
- **Non-goals**: a second path registry, one monolithic validator, blanket
  workflow-job consolidation, global tool installation, remote mutation, or a
  live-readiness claim from repository-static evidence.

## Quality Attributes

- **Single ownership**: path routing remains in the existing validation-surface
  contract; GitHub and platform evidence contracts reference rather than copy
  that authority.
- **Integrity**: closed schemas reject unknown keys, duplicate identifiers,
  path copies, unknown evidence depths, ownerless limitations, and stale
  projections.
- **Traceability**: every result binds surface, validator, exact tool identity,
  lane, depth, relevant immutable source or observation date, limitation,
  owner, and retry trigger without pinning a mutable branch head.
- **Reproducibility**: required tools are exact-version and checksum verified;
  required CI lanes fail when tool preparation fails.
- **Security**: ignored state is never read; Actions remain immutable and
  least-privilege; secret and local-only transport exceptions remain explicit;
  no deploy or apply operation is part of static validation.
- **Operability**: each Spec has one Plan, Task, logical commit sequence,
  review gate, rollback boundary, and successor handoff.
- **Portability**: deterministic fallbacks preserve syntax and policy coverage
  where a product-native tool is optional, while missing mandatory semantics
  stays visible.

## System Overview & Context

The control flow has six layers:

1. Git and repository indexes produce the tracked, in-scope path inventory.
2. `scripts/validation/registry.json` resolves each path to its canonical surface and
   validator set.
3. `github-surface-routing.json` projects selected surface identifiers into
   label and CODEOWNERS expectations without restating path patterns.
4. `platform-validation-evidence.json` records each platform target's syntax,
   render, schema or policy, product-semantic, and live evidence capabilities.
5. Focused validators and fixtures compare machine contracts with native
   `.github`, GitOps, policy, IaC, script, test, secret, and Traefik surfaces.
6. Local and CI lanes emit distinct results; the Task records reviewed evidence
   and preserves remote/live limitations through integration and rollback.

Intentional CI lanes remain independent evidence producers: affected/staged
feedback, all-files pre-commit, repository quality, agent governance, manifest
static validation, and the single `ci-summary` verdict. A validator has one
primary execution owner even when another lane depends on its result.

## Data Architecture

Two new closed machine contracts are introduced beside the current validation
surface contract:

| Contract | Owns | Must reference | Must not duplicate |
| --- | --- | --- | --- |
| `github-surface-routing.json` | Surface identifier to GitHub label and CODEOWNERS projection, projection state, evidence, and exceptions | `scripts/validation/registry.json` surface IDs | Route regexes, validator argv, workflow job bodies, or branch-protection settings |
| `platform-validation-evidence.json` | Target class, required depth, exact tool/version/checksum source, execution mode, fallback, evidence lane, limitation, owner, and retry trigger | Existing surface IDs, executable manifests/configuration, reviewed locks, and validator IDs | Full path registries, credentials, live results, or technology research prose |

Each contract has a colocated JSON Schema and focused validator. Stable enums
include `PASS`, `FAIL`, `SKIP`, and `DEFER`; evidence lanes remain
`repo-static`, `ci`, and `remote/live`; platform depth is modeled as syntax,
render, schema or policy, product semantic, and live observation. A result at
one depth or lane never implies another.

Temporary stash and migration analysis may exist only as ignored, non-secret
`_workspace` data. Durable dispositions move into the owning Task; generated
object identities are recreated from current HEAD rather than copied from
scratch or an old stash.

## Infrastructure & Deployment

- Local authoring uses an isolated `.worktrees/` checkout after the written
  Specs and Plans are approved.
- Required non-ambient tools execute from an ignored temporary cache and are
  selected by repository-pinned version plus checksum evidence. User-global
  installations are not modified.
- All 13 Kustomize roots receive render evidence with a tool compatible with
  the repository's pinned Kubernetes/K3s minor. The ambient local
  `kubectl 1.30.14` is diagnostic-only when the target remains 1.35.x.
- Built-in Kubernetes resources receive strict schema validation. External CRD
  GVKs require an allowlist and either a pinned schema or an explicit bounded
  limitation; an unknown GVK fails.
- Terraform uses format, backend-disabled initialization, and validate only;
  Bicep uses lint and build only. Cloud authentication, plan/apply, deployment,
  and what-if remain outside the repository-static lane.
- Exact versions and supported ranges are read from their direct executable
  owners: bootstrap `--version` arguments, GitOps manifests, workflow and
  pre-commit configuration, dependency locks, Terraform constraints, and Bicep
  parameters. Stage 90 reference material is not an execution dependency or a
  mirrored version authority.
- Repository-self-referencing Argo CD Applications retain
  `targetRevision: main` under the current single-operator continuous
  reconciliation model. External Helm chart Applications retain exact chart
  revisions. Multi-operator, multi-environment, or history-rewrite workflows
  reopen ADR-0029 rather than adding a branch-SHA census.
- Namespace Pod Security Admission labels are desired-state evidence. The
  repository uses `enforce` where repo-authored workload evidence is bounded,
  and `audit`/`warn` where Helm charts, injection, node agents, or runtime
  behavior remain uncertain. `platform-istio-cni-app.yaml` proves declared
  Istio CNI installation intent only; live DaemonSet, admission, and network
  behavior require separate runtime evidence.
- GitHub remote metadata is read-only and SHA-bound. No push, workflow dispatch,
  setting mutation, release, or branch-rule change is part of this architecture.

The design follows OpenGitOps' declarative, versioned, immutable, and
continuously reconciled principles, Kubernetes' Kustomize rendering contract,
GitHub's immutable Action and least-privilege guidance, Terraform's validation
contract, Bicep's linter/build contract, Traefik's file-provider model, and
Vault/ESO's explicit authentication and CA boundaries.

## Traceability

### Lifecycle Traceability

| Upstream requirement | Quality attribute or boundary | ADR / Spec |
| --- | --- | --- |
| [REQ-0007-FR-0001](../../01.requirements/0007-repository-delivery-and-platform-assurance.md#functional-requirements) | Single current inventory, evidence-backed no-change, and protected-surface boundary | [ADR-0021](../decisions/0021-canonical-surface-routing-and-evidence-depth.md) and [Spec 047](../../03.specs/0047-current-surface-and-stash-reconciliation/spec.md) |
| N/A — REQ-0007-FR-0003 shares the PRD-0007 source linked in REQ-0007-FR-0001. | Non-duplicative GitHub projection and independent CI lanes | [Spec 048](../../03.specs/0048-github-routing-and-ci-evidence/spec.md) |
| N/A — REQ-0007-FR-0005 shares the PRD-0007 source linked in REQ-0007-FR-0001. | Layered platform evidence and product semantics | [Spec 049](../../03.specs/0049-platform-validation-and-security-evidence/spec.md) |
| N/A — REQ-0007-FR-0007 shares the PRD-0007 source linked in REQ-0007-FR-0001. | Provider-native IaC validation and deterministic fallbacks | [Spec 050](../../03.specs/0050-example-iac-and-validator-qa/spec.md) |
| N/A — REQ-0007-FR-0009 shares the PRD-0007 source linked in REQ-0007-FR-0001. | Approval boundary, rollback, closure, and no-change evidence | [Spec 051](../../03.specs/0051-repository-assurance-integration-and-closure/spec.md) |
