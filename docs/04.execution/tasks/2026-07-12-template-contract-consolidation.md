---
title: 'Task: Template Contract Consolidation'
type: sdlc/task
status: done
owner: platform
updated: 2026-07-13
---

# Task: Template Contract Consolidation

## Overview

This document tracks the six implementation and verification units that align
Stage 99 support and non-README forms with the document profile registry. It
preserves reciprocal Spec, Plan, Task, and index lineage throughout the Spec
027 compatibility window.

## Inputs

- **Parent Spec**:
  [../../03.specs/027-template-contract-consolidation/spec.md](../../03.specs/027-template-contract-consolidation/spec.md)
- **Parent Plan**:
  [../plans/2026-07-12-template-contract-consolidation.md](../plans/2026-07-12-template-contract-consolidation.md)
- **Completed Registry Task**:
  [./2026-07-12-document-contract-registry.md](./2026-07-12-document-contract-registry.md)

## Task Table

| Task ID | Description | Type | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- |
| TCC-001 | Start reciprocal execution lineage | doc | Spec/Plan/Task/index link assertion | platform | Done |
| TCC-002 | Publish the type-to-source decision ledger | research | Ten family rows with all required evidence fields | platform | Done |
| TCC-003 | Consolidate support ownership | governance | No copied complete registry tables | platform | Done |
| TCC-004 | Normalize canonical non-README forms | template | Heading matrix and native-format checks | platform | Done |
| TCC-005 | Delete legacy Task form and establish compatibility | migration | Zero active legacy refs; old/new gates green | platform | Done |
| TCC-006 | Close evidence and hand off Stage 99 README bodies | validation | Full QA and explicit Spec 028 handoff | platform | Done |

### Phase View

### Phase 1: Execution Lineage

- [x] TCC-001 Start reciprocal execution lineage.

### Phase 2: Contract Consolidation

- [x] TCC-002 Publish type-to-source decision ledger.
- [x] TCC-003 Consolidate support ownership.
- [x] TCC-004 Normalize canonical non-README forms.
- [x] TCC-005 Delete legacy Task form and establish compatibility.

### Phase 3: Closure

- [x] TCC-006 Close evidence and hand off README body ownership.

## Approval and Safety Boundaries

- **Allowed Paths**: `TCC-001 through TCC-006` is limited to these Template Contract Consolidation owners and Task-Table surfaces:
  - `docs/04.execution/tasks/2026-07-12-template-contract-consolidation.md`
  - `docs/03.specs/027-template-contract-consolidation/spec.md`
  - `docs/04.execution/plans/2026-07-12-template-contract-consolidation.md`
  - `docs/04.execution/tasks/2026-07-12-document-contract-registry.md`
- **Forbidden Paths**: runtime manifests, provider or CI settings, secret values, generated/local state, and paths outside the Template Contract Consolidation work items and linked evidence owners.
- **Approval Required**: Human approval is required before Template Contract Consolidation protected-file expansion, deletion/relocation, runtime/CI/provider mutation, credential access, publication, push, or merge beyond the parent Plan.
- **Static Validation**: Preserve the Template Contract Consolidation outcomes and limitations recorded in Verification Summary; use these recorded checks:
  - `git diff --check`
- **Live Validation**: DEFER — Template Contract Consolidation is closed by repository-static/documentation evidence; historical live commands, if any, are not authority for a new cluster, provider, external-service, or deployment claim.
- **Secret / Vault Handling**: No secret value is required for Template Contract Consolidation; do not read or print tokens, credentials, Vault/Kubernetes Secret data, kubeconfigs, auth files, private logs, or shell history.
- **Rollback Plan**: Revert the logical Template Contract Consolidation change set for `TCC-001 through TCC-006` and restore its allowed implementation/evidence paths with this Task and parent Plan; documentation rollback does not authorize live mutation.
- **Evidence Location**: Durable Template Contract Consolidation evidence remains in:
  - `docs/04.execution/tasks/2026-07-12-template-contract-consolidation.md`
  - `docs/03.specs/027-template-contract-consolidation/spec.md`
  - `docs/04.execution/plans/2026-07-12-template-contract-consolidation.md`
  - `docs/04.execution/tasks/2026-07-12-document-contract-registry.md`

## Verification Summary

- **Registry Self-test**: PASS, `9 cases / 55 profiles / 22 templates`.
- **Compatibility Classification**: PASS, `455 paths / 0 uncovered / 0
  ambiguous` (`baseline=433`, `new=23`).
- **Canonical and Template Coverage**: Fresh fixture computation returned `20`
  canonical-form rows and `22` template-mode rows.
- **Finite Authored Compatibility Baseline**: Fresh row aggregation matched the
  fixture exactly: `20` profile rows, `25` legacy alias definitions, `26`
  forbidden-residue definitions, `314` baseline paths as an inventory snapshot,
  not a cap, `89`
  missing-canonical paths, `188` forbidden-residue paths, and `410`
  forbidden-residue occurrences. Owner is Spec 030; missing-canonical and
  forbidden-residue debt growth remains forbidden, while total canonical path
  inventory may grow.
- **Legacy Inventory**: The retired `task-legacy-harness` marker has zero
  matches. The remaining seven `Suggested Types`/`Working Rules` occurrences
  are six finite Spec 030 fixture/gate references and one completed historical
  progress entry; there is no unowned or new occurrence.
- **Repository QA**: Registry self-test, compatibility validation, repository
  quality gates, `git diff --check`, and all applicable all-files pre-commit
  hooks PASS. `Lint Dockerfiles` is a non-applicable SKIP because no Dockerfile
  was selected and is not claimed as a pass.
- **README Boundary**: TCC-004 and TCC-005 changed Stage 99 README inventory,
  tree, and target-link rows only. Spec 028 owns every README form, profile,
  layout, and body redesign; Spec 030 owns authored corpus migration.
- **Independent Review**: Independent SDD task reviewers accepted TCC-001
  through TCC-005. The reviewed ranges recorded in the SDD ledger are
  `10e0a0e..eeeb428`, `eeeb428..e0116a5`, `e0116a5..c4db124`,
  `c4db124..91154fa`, and Task 5 commits `74d82c4` plus `b5e7c7a`.
- **Logical Commit Range**: The consolidation implementation before this
  closure is `10e0a0e..b5e7c7a`; TCC-006 is the closure commit containing this
  evidence.
- **Rollback Range**: Revert the TCC-006 closure commit first, then revert
  `10e0a0e..b5e7c7a` newest-first to return to the completed Spec 026 baseline.
- **Commands**: `python3 scripts/validate-document-contract-registry.py
  --self-test`; `python3 scripts/validate-document-contract-registry.py --root
  . --mode compatibility`; `bash scripts/validate-repo-quality-gates.sh .`;
  the bounded legacy inventory query; `git diff --check`; and `pre-commit run
  --all-files`.
- **Logs / Evidence Location**: This Task, the logical task commits, and the
  ignored `.superpowers/sdd/tcc-task-6-report.md` implementer report.
- **Static-only Safety Boundary**: No live Kubernetes, Argo CD, Vault, ESO,
  provider-runtime, credential, secret-value, remote CI, publish, push, merge,
  deployment, or third-party mutation ran. Results prove repository-static
  closure only.

## Traceability

- **Spec**:
  [../../03.specs/027-template-contract-consolidation/spec.md](../../03.specs/027-template-contract-consolidation/spec.md)
- **Plan**:
  [../plans/2026-07-12-template-contract-consolidation.md](../plans/2026-07-12-template-contract-consolidation.md)
- **Previous Tranche**:
  [./2026-07-12-document-contract-registry.md](./2026-07-12-document-contract-registry.md)
- **README Body Owner**:
  [../../03.specs/028-readme-workspace-profiles/spec.md](../../03.specs/028-readme-workspace-profiles/spec.md)
- **Authored Corpus Migration Owner**:
  [../../03.specs/030-authored-document-migration/spec.md](../../03.specs/030-authored-document-migration/spec.md)
