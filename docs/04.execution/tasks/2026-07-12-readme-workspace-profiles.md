---
title: 'Task: README and Workspace Profiles'
type: sdlc/task
status: active
owner: platform
updated: 2026-07-12
---

# Task: README and Workspace Profiles

## Overview

This Task tracks six bounded implementation units for replacing the monolithic
README form with path-derived profiles, migrating the complete README corpus,
and preserving `_workspace` as temporary non-secret repository-support staging.
RWP-001 establishes the active execution lineage; later rows remain queued
until their profile-specific changes and validation evidence are complete.

## Inputs

- **Parent Spec**: [README and Workspace Profiles Technical Specification](../../03.specs/028-readme-workspace-profiles/spec.md)
- **Parent Plan**: [README and Workspace Profiles Implementation Plan](../plans/2026-07-12-readme-workspace-profiles.md)
- **Completed Registry Spec**: [Document Contract Registry](../../03.specs/026-document-contract-registry/spec.md)
- **Completed Template Spec**: [Template Contract Consolidation](../../03.specs/027-template-contract-consolidation/spec.md)
- **Semantic Validator Consumer**: [Semantic Document Validation](../../03.specs/029-semantic-document-validation/spec.md)
- **Authored Corpus and Handoff Migration Owner**: [Authored Document Migration](../../03.specs/030-authored-document-migration/spec.md)

## Task Table

| ID | Work item | Owner | Status | Evidence |
| --- | --- | --- | --- | --- |
| RWP-001 | Start reciprocal execution lineage | platform | Done | Six links and index rows |
| RWP-002 | Create six forms, routes, and complete fixture | platform | Queued | 67 baseline and 72 final dispositions |
| RWP-003 | Migrate repository, stage, and collection entrypoints | platform | Queued | 27 baseline plus cloud collection handoff |
| RWP-004 | Migrate snapshot packs and create provider snapshot handoffs | platform | Queued | 28 baseline plus two provider indexes |
| RWP-005 | Migrate implementation/workspace entrypoints and create example handoffs | platform | Queued | 12 baseline plus two provider entrypoints |
| RWP-006 | Delete monolith, verify handoff fixtures, and close | platform | Queued | 72 exact routes, zero universal markers |

## Approval and Safety Boundaries

- **Allowed Paths**: `docs/03.specs/028-readme-workspace-profiles/spec.md`,
  `docs/03.specs/README.md`,
  `docs/04.execution/plans/2026-07-12-readme-workspace-profiles.md`,
  `docs/04.execution/plans/README.md`, this Task, and
  `docs/04.execution/tasks/README.md` for RWP-001.
- **Forbidden Paths**: README profile bodies, Stage 99 forms, the document
  registry, fixtures, validators, scripts, provider adapters, hooks, CI, and
  every other tracked path are outside RWP-001.
- **Approval Required**: Human approval is required before adding a seventh
  profile, changing protected surfaces, accessing secrets or local state,
  publishing, pushing, or performing any remote or live mutation.
- **Static Validation**: Run the six-link assertion, registry compatibility
  validation, repository quality gate, `git diff --check`, exact changed-file
  scope proof, and applicable pre-commit checks.
- **Live Validation**: DEFER. RWP-001 is documentation-only and repository-static;
  it does not establish Kubernetes, Argo CD, Vault, ESO, or provider-runtime
  readiness.
- **Secret / Vault Handling**: Do not read, print, enumerate, move, or modify
  credentials, secret values, Vault data, tokens, keys, certificates,
  kubeconfigs, local settings, diagnostics, or ignored workspace content.
- **Rollback Plan**: Revert the RWP-001 commit to remove this Task and restore
  the prior Spec, Plan, and index lineage state.
- **Evidence Location**: This Task, the RWP-001 commit, and the ignored
  `.superpowers/sdd/rwp-task-1-report.md` execution report.
- **GitOps Impact**: None; no manifests or desired-state configuration change.
- **Kubernetes Impact**: None; no live cluster command is authorized or run.
- **Operations / Runbook Impact**: None; no operational procedure changes.

`_workspace` validation is limited to tracked-file and ignore-rule metadata.
It must never enumerate or open ignored children. The complete fixture created
later is consumed by Spec 029's semantic validator, while Spec 030 owns authored
corpus migration and cloud-document handoff consolidation.

## Verification Summary

- Before editing, the six-link assertion failed with exit 1 and
  `AssertionError` because this Task did not exist, preserving the required RED
  lineage evidence.
- RWP-001 changes only the six allowed files and establishes reciprocal
  Spec/Plan/Task links plus one dated Active row in each Stage 03/04 index.
- Registry compatibility passes with `455 paths`, `baseline=433`, `new=23`,
  `uncovered=0`, and `ambiguous=0`. The future-state `--profile readme` filter
  is deferred to RWP-002 because that row creates the README profiles.
- The repository quality gate, `git diff --check`, and every applicable
  pre-commit hook for the six-file scope pass. Dockerfile lint and other
  non-selected-file hooks are non-applicable SKIPs, not passes.
- The implementation evidence is repository-static only. It makes no live,
  secret-value, credential, remote CI, publication, push, merge, or deployment
  readiness claim.

## Traceability

- **Spec**: [README and Workspace Profiles](../../03.specs/028-readme-workspace-profiles/spec.md)
- **Plan**: [README and Workspace Profiles Implementation Plan](../plans/2026-07-12-readme-workspace-profiles.md)
- **Previous Registry Tranche**: [Document Contract Registry](../../03.specs/026-document-contract-registry/spec.md)
- **Previous Template Tranche**: [Template Contract Consolidation](../../03.specs/027-template-contract-consolidation/spec.md)
- **Semantic Validation Consumer**: [Semantic Document Validation](../../03.specs/029-semantic-document-validation/spec.md)
- **Authored Migration Owner**: [Authored Document Migration](../../03.specs/030-authored-document-migration/spec.md)
