---
title: "Stage 00 Governance and Unified Quality Gates"
version: "1.0.0"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "platform"
updated: "2026-09-04"
layer: "architecture"
artifact_id: "ADR-0034"
---

# ADR-0034: Stage 00 Governance and Unified Quality Gates

## Overview

This decision makes `docs/00.agent-governance/` the single shared control plane
for agent policy, providers, roles, skills, and machine-readable role metadata.
It removes `.agents/` as a second provider-neutral authority and establishes one
QA entrypoint used by local development and GitHub Actions.

## Context

The repository currently distributes the same governance meaning across Stage
00, `.agents/`, provider projections, hook scripts, validation contracts,
fixtures, and multiple GitHub Actions jobs. The result is duplicated role and
skill ownership, stale provider evidence, automatic QA after ordinary edits,
and repeated execution of the same validators and tests.

ADR-0030 established authority-first convergence but retained `.agents/` as a
machine owner. Repository experience now shows that this split creates drift:
Stage 00 is described as canonical while root gateways and provider adapters
still delegate exact authority to `.agents/registry.json`.

## Decision

1. `docs/00.agent-governance/` owns shared human and machine governance.
   `registry.json`, its schema, canonical role bodies, and shared skills live
   below Stage 00.
2. `.claude/` and `.codex/` contain only provider-native gateways,
   configuration, projections, and symlinks to Stage 00 skills. Provider files
   may narrow common policy but never redefine or expand it.
3. `.agents/` is removed. Reachable Git history is the recovery source; no
   compatibility redirect or dormant directory is retained.
4. `scripts/qa.py` is the only supported QA orchestration entrypoint. It reads a
   compact gate registry, runs every selected gate once, fails closed, and emits
   a stable summary. Local and hosted execution use the same profiles.
5. Gate policy distinguishes four concerns: governance, repository documents,
   manifests/security, and workflow/tooling. Fixtures exist only under
   `tests/fixtures/` and only when a focused test needs input variation.
6. GitHub Actions installs dependencies once, invokes the CI QA profile once,
   and reports through the required `ci-summary` job. Argo CD remains the CD
   engine; GitHub Actions validates desired state but does not deploy it.
7. Provider hooks may protect a write boundary, but they do not run the full QA
   suite after every edit or claim completion. Completion evidence comes from
   explicit QA execution.

This decision narrows the agent-governance, validation, fixture, and CI clauses
of ADR-0030. ADR-0030 remains authoritative for the wider SDLC taxonomy,
retention, and authority-first migration strategy.

## Explicit Non-goals

- This decision does not change Kubernetes desired state or perform a live
  cluster, Vault, provider, deployment, release, or reconciliation action.
- It does not claim provider discovery, authentication, model resolution, hook
  delivery, or execution from tracked configuration.
- It does not rewrite closed or archived evidence merely because it records an
  older topology.
- It does not introduce a general workflow engine, distributed test scheduler,
  or generated provider projection framework.

## Consequences

The positive consequence is one ownership graph and one executable quality
path. Local and CI results become comparable, automatic edit-time work becomes
bounded, and removal of a gate requires changing one registry and its focused
test rather than several prose and workflow copies.

The compatibility cost is deliberate: consumers of `.agents/` must move in the
same change. Current documents and tests that assert the former topology are
updated, superseded, archived, or removed. Historical references remain valid
as historical evidence and do not regain current authority.

## Alternatives

- **Keep `.agents/` and render projections.** Rejected because it preserves two
  governance roots and adds generation machinery to solve a duplication that
  disappears when Stage 00 owns the data directly.
- **Keep all existing gates and only deduplicate the workflow.** Rejected
  because stale contracts, fixtures, and self-only validators would remain
  active and continue to define conflicting completion rules.
- **Run only pre-commit.** Rejected because repository-domain validators and
  manifest contracts need an explicit, reviewable orchestration layer.
- **Use GitHub Actions for CD.** Rejected because the workspace is GitOps-first
  and Argo CD owns reconciliation.

## Traceability

### Lifecycle Traceability

| Decision lineage | Replacement relation | Affected Spec |
| --- | --- | --- |
| [ADR-0030](0030-authority-first-sdlc-and-agent-governance-convergence.md) | Narrows agent-governance and validation topology while preserving the wider authority-first SDLC model | [SPEC-0072](../../03.specs/0072-agent-governance-and-quality-gate-consolidation/spec.md) |
