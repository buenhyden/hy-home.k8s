---
title: 'Repository Delivery Evidence Architecture Reference Document'
type: sdlc/ard
status: draft
owner: platform
updated: 2026-08-02
---

# Repository Delivery Evidence Architecture Reference Document (ARD)

## Overview

This architecture defines a repository-static assurance control plane for the
delivery and platform surfaces covered by PRD-007. It layers routing,
projection, validation depth, evidence classification, review, and rollback on
top of the current platform and document contracts without creating a second
platform topology owner.

The architecture consumes the existing validation-surface registry, document
profiles, current local GitOps baseline, protected-surface validators, CI
workflow topology, and dated audit observations. It introduces only the two
machine contracts needed to close the residual routing and evidence-depth
gaps.

## Boundaries & Non-goals

- **Owns**: repository delivery assurance boundaries; GitHub projection parity;
  platform validation depth; exact tool and fallback evidence; ordered tranche
  execution; and local integration evidence.
- **Consumes**: PRD-004/ARD-0007/ADR-0014/Spec 008 current topology,
  `validation-surfaces.json` path routing, existing technology inventory,
  workflows, validators, tests, desired state, and the Current audit pack.
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
  lane, depth, commit or observation SHA, limitation, owner, and retry trigger.
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
2. `validation-surfaces.json` resolves each path to its canonical surface and
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
| `github-surface-routing.json` | Surface identifier to GitHub label and CODEOWNERS projection, projection state, evidence, and exceptions | `validation-surfaces.json` surface IDs | Route regexes, validator argv, workflow job bodies, or branch-protection settings |
| `platform-validation-evidence.json` | Target class, required depth, exact tool/version/checksum source, execution mode, fallback, evidence lane, limitation, owner, and retry trigger | Existing surface IDs, technology inventory, and validator IDs | Full path registries, credentials, live results, or technology research prose |

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
| [REQ-RDPA-001](../../01.requirements/007-repository-delivery-and-platform-assurance.md#functional-requirements) | Single current inventory, evidence-backed no-change, and protected-surface boundary | [ADR-0021](../decisions/0021-canonical-surface-routing-and-evidence-depth.md) and [Spec 047](../../03.specs/047-current-surface-and-stash-reconciliation/spec.md) |
| N/A — REQ-RDPA-003 shares the PRD-007 source linked in REQ-RDPA-001. | Non-duplicative GitHub projection and independent CI lanes | [Spec 048](../../03.specs/048-github-routing-and-ci-evidence/spec.md) |
| N/A — REQ-RDPA-005 shares the PRD-007 source linked in REQ-RDPA-001. | Layered platform evidence and product semantics | [Spec 049](../../03.specs/049-platform-validation-and-security-evidence/spec.md) |
| N/A — REQ-RDPA-007 shares the PRD-007 source linked in REQ-RDPA-001. | Provider-native IaC validation and deterministic fallbacks | [Spec 050](../../03.specs/050-example-iac-and-validator-qa/spec.md) |
| N/A — REQ-RDPA-009 shares the PRD-007 source linked in REQ-RDPA-001. | Approval boundary, rollback, closure, and no-change evidence | [Spec 051](../../03.specs/051-repository-assurance-integration-and-closure/spec.md) |
