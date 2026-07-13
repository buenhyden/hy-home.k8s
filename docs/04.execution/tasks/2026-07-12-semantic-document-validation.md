---
title: 'Task: Semantic Document Validation'
type: sdlc/task
status: active
owner: platform
updated: 2026-07-12
---

# Task: Semantic Document Validation

## Overview

This Task tracks four bounded implementation units for replacing hardcoded
document-shape checks with deterministic registry-driven Markdown, link, index,
current-owner, and migration-ledger validation. SMDV-001 establishes the
reciprocal execution lineage, and SMDV-002 adds the production Markdown
profile validator. SMDV-003 and SMDV-004 remain queued until their
cross-document and integration changes pass the Plan's repository-static gates.

## Inputs

- **Lifecycle Promotion**: The operator's direct program approvals promote this
  new Task from the canonical `draft` starting state to `active` for execution.
- **Parent Spec**: `docs/03.specs/029-semantic-document-validation/spec.md`
- **Parent Plan**: `docs/04.execution/plans/2026-07-12-semantic-document-validation.md`
- **Registry Baseline**: Spec 026 provides the importable registry loader and
  the classified tracked-file inventory.
- **Template and README Baseline**: Specs 027 and 028 provide 60 profiles, 27
  templates, and 72 canonical README paths before this Task is added.

## Task Table

| ID | Work item | Owner | Status | Evidence |
| --- | --- | --- | --- | --- |
| SMDV-001 | Start reciprocal Spec, Plan, Task, and index lineage | platform | Done | Logical commit `docs(execution): start semantic document validation`; `python3 scripts/validate-document-contract-registry.py --root . --mode compatibility` |
| SMDV-002 | Implement production Markdown profile validation | platform | Done | Logical commits `feat(docs): add registry-driven markdown profile validation` and `fix(validation): harden markdown debt mutation proofs`; `python3 scripts/validate-markdown-profiles.py --self-test` |
| SMDV-003 | Implement cross-document link, index, owner, and ledger validation | platform | Queued | Logical commit `feat(validation): add link and owner validator`; `python3 scripts/validate-links-and-owners.py --self-test` |
| SMDV-004 | Delegate the repository gate and close Spec 029 | platform | Queued | Logical commit `feat(validation): delegate semantic document gates`; `bash scripts/validate-repo-quality-gates.sh .` |

## Approval and Safety Boundaries

- **Allowed Paths**: Only the exact tracked path set declared by the active
  SMDV Plan Task may change. SMDV-002 is limited to its nine validator,
  fixture, documentation, Task, quality-gate consumer, and canonical
  progress-ledger paths.
- **Forbidden Paths**: Secrets, credentials, ignored `_workspace` children,
  local diagnostics, provider or cluster state, remote resources, and paths
  outside the active SMDV Task scope must not be read or changed.
- **Approval Required**: Human approval is required before registry schema or
  compatibility-debt expansion, strict cutover, remote push or merge,
  publication, secret access, or any live mutation.
- **Static Validation**: Run the Task's exact RED/GREEN assertion, registry
  self-test and compatibility mode, repository quality gate, `git diff
  --check`, exact staged-path proof, and focused pre-commit hooks.
- **Live Validation**: DEFER. This tranche validates repository content only
  and does not establish Kubernetes, Argo CD, Vault, ESO, or provider-runtime
  readiness.
- **Secret / Vault Handling**: Do not read, print, enumerate, move, or modify
  credentials, tokens, keys, certificates, kubeconfigs, secret values, Vault
  data, shell history, auth files, or ignored workspace content.
- **Rollback Plan**: Revert each SMDV logical commit newest-first. Reverting
  `docs(execution): start semantic document validation` removes this Task and
  its exact reciprocal links and index entries as one unit.
- **Evidence Location**: This Task, its parent Plan, the canonical progress
  ledger, logical commits, and ignored `.superpowers/sdd/smdv-task-*-report.md`
  and review packages.
- **GitOps Impact**: None; no desired-state manifest changes are authorized.
- **Kubernetes Impact**: None; no cluster command is authorized or run.
- **Operations / Runbook Impact**: None; no operational procedure changes.

## Verification Summary

SMDV-002 GREEN covers all 60 registry profiles, the imported eight-case README
handoff and its exact 72-path table, append context, deterministic Seoul-date
semantics, stable text/JSON diagnostics, and exact finite compatibility debt.
Compatibility reports 1,299 `DEFER` diagnostics across the frozen 266-path
union with exit 0; strict mode reports the identical tuples as `FAIL` with exit
1 and no baseline `DEBT-UNUSED`. Independent-review mutations prove duplicate
production consumption emits `DEBT-UNUSED`, all token obligations reproduce
their occurrence caps, unsafe fixture paths are rejected before writes, and
the seven date cases cannot silently shrink. Registry inventory remains 467 target Markdown paths
(`baseline=433`, `new=36`), 60 profiles, 27 templates, and 72 canonical README
paths. Evidence is repository-static and excludes live, secret-value,
credential, remote CI, publication, push, merge, deployment, and third-party
mutation checks.

## Traceability

- **Spec**: [Semantic Document Validation Technical Specification](../../03.specs/029-semantic-document-validation/spec.md)
- **Plan**: [Semantic Document Validation Implementation Plan](../plans/2026-07-12-semantic-document-validation.md)
- **Previous Tranche**: README and Workspace Profiles, Spec 028
- **Next Tranche**: Authored Document Migration, Spec 030
