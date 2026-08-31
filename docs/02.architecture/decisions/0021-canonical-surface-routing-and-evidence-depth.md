---
title: 'ADR-0021: Canonical Surface Routing and Evidence-Depth Architecture'
type: sdlc/adr
status: superseded
owner: platform
updated: 2026-09-01
artifact_id: "ADR-0021"
superseded_by: ADR-0031
---

# ADR-0021: Canonical Surface Routing and Evidence-Depth Architecture

## Overview

This accepted decision selects a reference-based projection architecture for
repository delivery and platform assurance. The existing validation-surface
contract remains the sole affected-path and validator owner; two new closed
contracts project GitHub routing and platform evidence depth without copying
that path inventory.

## Context

The repository's current workflow jobs are distinct evidence lanes rather than
proven duplicates, yet labeler and CODEOWNERS coverage can drift from the
machine surface registry. Platform validation also combines syntax fallbacks,
Kustomize rendering, optional schema tools, product-specific checks, and live
limitations in prose that cannot be compared deterministically.

A single larger workflow or validator would obscure ownership and make missing
tools easier to misclassify. Copying route regexes into another contract would
create the same drift the program is intended to remove. Applying the saved
stash wholesale would similarly replace current agent-governance and generated
state with an older snapshot.

## Decision

- Keep `scripts/validation/registry.json` as the only path-to-surface,
  path-to-validator, and CI selection owner.
- Add `github-surface-routing.json` and its closed schema as the sole mapping
  from referenced surface IDs to expected labels, CODEOWNERS classes,
  projection state, and bounded exceptions.
- Add `platform-validation-evidence.json` and its closed schema as the sole
  mapping from referenced platform targets and validators to required evidence
  depth, exact tool identity, execution mode, fallback, lane, limitation,
  owner, and retry trigger.
- Define evidence depth explicitly: syntax; render; schema or policy; product
  semantic; and live observation. Preserve `PASS`, `FAIL`, `SKIP`, and `DEFER`
  without promotion between depths or lanes.
- Preserve distinct pre-commit, repository-quality, agent-governance, and
  manifest jobs plus the single `ci-summary` verdict unless future evidence
  proves identical owner, trigger, command graph, and output semantics.
- Keep local-only Vault/ESO HTTP and Traefik TLS-skip behavior as named
  repository-local exceptions until a separately approved live/TLS migration
  has CA, compatibility, rotation, rollback, and runtime evidence.
- Keep the current explicit tag-or-digest, non-`latest` image gate. Require an
  ADR-backed consumer and rollback analysis before digest, SBOM, or provenance
  enforcement expands.
- Reconcile the saved stash by semantic hunk classification, never by wholesale
  apply; regenerate derived object identities from current HEAD.
- Treat local and hosted/remote evidence as separate. No remote setting change
  or live mutation is authorized by this decision.

## Explicit Non-goals

- Replacing PRD-004, ARD-0007, ADR-0014, or Spec 008 as the current platform
  topology owner.
- Moving document profile or lifecycle ownership out of Stage 99.
- Creating a second path-pattern registry or duplicating validator argv.
- Claiming official Traefik or external-CRD schema coverage where only a
  repository product-semantic check exists.
- Requiring a CODEOWNER approval that would deadlock the observed single-
  collaborator repository.
- Installing global tools, reading ignored secrets, deploying examples,
  pushing, dispatching workflows, or mutating GitHub or live infrastructure.

## Consequences

- Labeler and CODEOWNERS become deterministic projections of shared surface
  identity instead of independently maintained path lists.
- Platform results state exactly what depth and tool produced them, making a
  syntax PASS insufficient evidence for render, schema, product semantics, or
  live readiness.
- Validators gain small, testable ownership boundaries; CI jobs can remain
  independent without running the same focused command twice inside one lane.
- Required CI-equivalent validation must provision pinned tools or fail. A
  developer diagnostic may SKIP an unavailable optional tool, but cannot close
  the required program gate.
- External CRDs need an explicit GVK and schema disposition; unknown GVKs fail
  rather than disappearing behind a global ignore-missing setting.
- Remote GitHub hardening remains a separately authorized follow-up after
  current hosted CI is green and a second eligible reviewer exists.

## Alternatives

- **Copy path patterns into `.github` and a new platform registry**: rejected
  because multiple route owners recreate drift and ambiguous precedence.
- **Merge every quality command into one aggregate job**: rejected because it
  collapses independent evidence, failure isolation, and required-check
  semantics without a proven duplicate.
- **Use only YAML parsing for Kubernetes and Traefik**: rejected because syntax
  does not prove renderability, GVK validity, or router/service references.
- **Make every native tool optional**: rejected because missing required
  semantics would be reported as a successful repository closure.
- **Require live validation now**: rejected because credentials, cluster state,
  Vault, ESO, TLS, and cloud resources are outside the approved authority.
- **Apply `stash@{0}` wholesale**: rejected because most rename intent is
  already current and the remaining generated identities and governance text
  are stale relative to current `main`.

## Traceability

### Lifecycle Traceability

| Decision lineage | Replacement relation | Affected Spec |
| --- | --- | --- |
| [ARD-0010](../descriptions/0010-repository-delivery-evidence-architecture.md) | N/A — first repository-delivery assurance decision; preserves accepted ADR-0014 as the platform topology owner | [Spec 047](../../03.specs/0047-current-surface-and-stash-reconciliation/spec.md), [Spec 048](../../03.specs/0048-github-routing-and-ci-evidence/spec.md), [Spec 049](../../03.specs/0049-platform-validation-and-security-evidence/spec.md), [Spec 050](../../03.specs/0050-example-iac-and-validator-qa/spec.md), and [Spec 051](../../03.specs/0051-repository-assurance-integration-and-closure/spec.md) are authored. |
| [ADR-0031](./0031-current-corpus-retention-and-validation-ownership.md) | Supersedes validation-surface routing as a Stage 00/current-roster concern; preserves the historical evidence-depth rationale. | [Spec 0066](../../03.specs/0066-validation-tooling-ownership/spec.md) |
