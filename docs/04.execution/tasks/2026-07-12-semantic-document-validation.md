---
title: 'Task: Semantic Document Validation'
type: sdlc/task
status: done
owner: platform
updated: 2026-07-12
---

# Task: Semantic Document Validation

## Overview

This Task tracks four bounded implementation units for replacing hardcoded
document-shape checks with deterministic registry-driven Markdown, link, index,
current-owner, and migration-ledger validation. SMDV-001 establishes the
reciprocal execution lineage, and SMDV-002 adds the production Markdown
profile validator. SMDV-003 adds the cross-document producer and its exact
467-path inventory handoff. SMDV-004 closes the tranche by making the quality
gate a compatibility-mode orchestrator while retaining domain-only checks.

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
| SMDV-003 | Implement cross-document link, index, owner, and ledger validation | platform | Done | Logical commits `feat(docs): validate links indexes and current owners` (`f41f437`) and `fix(validation): harden cross-document boundary proofs` (`32b9414`); `python3 scripts/validate-links-and-owners.py --self-test` |
| SMDV-004 | Delegate the repository gate and close Spec 029 | platform | Done | Logical commit `refactor(qa): delegate document checks to semantic validators`; `bash scripts/validate-repo-quality-gates.sh .` reports exact Markdown and ledger compatibility debt, no `FAIL`, and final repository PASS |

## Approval and Safety Boundaries

- **Allowed Paths**: Only the exact tracked path set declared by the active
  SMDV Plan Task may change. SMDV-002 is limited to its nine validator,
  fixture, documentation, Task, quality-gate consumer, and canonical
  progress-ledger paths. SMDV-003 is limited to the Plan's exact seven paths:
  the new validator, its two fixtures, two README inventories, this Task, and
  the canonical progress ledger. SMDV-004 is limited to the corrected Plan's
  exact eleven paths; its additional validator path proves the exact
  66-to-63 owner-key transition caused by closing this Spec, Plan, and Task.
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
- **Rollback Plan**: Revert each SMDV logical commit newest-first. Revert the
  SMDV-004 closure commit by its subject `refactor(qa): delegate document
  checks to semantic validators`, then `32b9414`, `f41f437`, `a9aedc5`,
  `1fc3a31`, and `c5b14aa`. Retain the validator feature commits when only the
  wrapper delegation must be restored.
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

SMDV-003 GREEN scans all 467 sorted registry paths without dereferencing the
recorded provider adapters, closes all three declared index dimensions, and
computes 66 unique active/accepted owner keys. Compatibility emits only the
pinned `LEDGER-MISSING` `DEFER` with exit 0; strict emits the identical tuple as
`FAIL` with exit 1. Inventory emits the ordered `433/467/36/467` envelope with
no diagnostics. The fixture runner covers local-link normalization and safety,
index row/tree/status mutations, owner normalization/exclusions/duplicates,
ledger completeness, and closed semantic-debt configuration mutations. ADM-002
owns ledger creation, the 468-path self-row transition, and exact debt removal;
this Task does not implement that migration handoff.

SMDV-004 GREEN starts from a clean wrapper baseline PASS, invokes the registry,
Markdown-profile, and cross-document validators after Python prerequisites,
and removes only duplicated general document checks. The wrapper still pins
the complete template-compatibility semantic SHA and rejects affected-path,
rule, token, cap, union, owner, growth-policy, and residue-token mutations.
It retains operations index parity, archive and snapshot boundaries, GitOps,
infrastructure, agent-runtime, CI/QA, security, version, and supply-chain
contracts. Registry counts remain 467 target paths (`baseline=433`, `new=36`),
60 profiles, 27 templates, and 72 README paths. Markdown compatibility emits
exactly 1,299 `DEFER` diagnostics and cross-document compatibility emits only
the pinned `LEDGER-MISSING` `DEFER`; neither emits `FAIL`. The production
self-test proves that these exact three lifecycle paths were prior owner
candidates and that their `done` status alone changes the unique owner-key
baseline from 66 to 63.

Static closure evidence includes shell syntax, all three validator self-tests,
registry compatibility, the repository wrapper, `git diff --check`, exact
eleven-path staging, and all-files pre-commit. Review is assigned to a fresh SDD
reviewer using `.superpowers/sdd/smdv-task-4-review.md`; approval is not inferred
from this content-addressed closure commit. Rollback uses the exact sequence in
the safety boundary above. No live cluster, provider runtime, remote CI,
credential, secret-value, publication, push, merge, deployment, or third-party
mutation is validated or implied.

The first independent SMDV-003 review withheld approval for five Important
boundary-proof gaps. The remediation moved the complete minimal tree into the
fixture, made all owner and malformed-debt cases execute production logic,
covered full/collapsed/shortcut references and valid fence closers, bound each
index to exact headings and target-key diagnostics, and resolved recorded
adapter descendants through their canonical target without dereferencing the
adapter. A cleanup assertion proves self-test leaves no repository ledger
artifact. A temporary, immediately removed include-path probe separately proved
the ADM-002 `468/current`, `37/new`, pinned self-row transition; the durable
ledger remains unimplemented and outside this Task's staged scope.

## Traceability

- **Spec**: [Semantic Document Validation Technical Specification](../../03.specs/029-semantic-document-validation/spec.md)
- **Plan**: [Semantic Document Validation Implementation Plan](../plans/2026-07-12-semantic-document-validation.md)
- **Previous Tranche**: README and Workspace Profiles, Spec 028
- **Next Tranche**: Authored Document Migration, Spec 030
