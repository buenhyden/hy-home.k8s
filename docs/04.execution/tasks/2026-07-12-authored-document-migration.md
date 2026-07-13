---
title: 'Task: Authored Document Migration'
type: sdlc/task
status: active
owner: platform
updated: 2026-07-13
---

# Task: Authored Document Migration

## Overview

This Task tracks seven bounded migration waves that move the approved authored
document corpus from measured compatibility debt to strict profile validation.
ADM-001 establishes reciprocal execution lineage. ADM-002 through ADM-007 then
publish the durable evidence ledger, normalize each owned document family,
consolidate duplicate AWS/Azure prose, and close the compatibility boundary.

## Inputs

- **Lifecycle Promotion**: The operator's direct program approvals promote this
  Task from the canonical `draft` starting state to `active` for execution.
- **Parent Spec**: `docs/03.specs/030-authored-document-migration/spec.md`
- **Parent Plan**: `docs/04.execution/plans/2026-07-12-authored-document-migration.md`
- **Validation Baseline**: Completed Specs 026 through 029 provide the registry,
  templates, README profiles, semantic validators, and the exact 468-path
  post-ADM-001/pre-ledger inventory (`baseline=433`, `new=37`).
- **Migration Baseline**: The approved baseline identity is
  `8e1b00b4dfb84b8431ba4d3d31b4ad0445a0019d`; program-created targets are
  accounted for separately by the validator inventory.

## Task Table

| ID | Work item | Owner | Status | Evidence |
| --- | --- | --- | --- | --- |
| ADM-001 | Start reciprocal Spec, Plan, Task, and index lineage | platform | Done | `python3` reciprocal-lineage assertion in Plan Task 1 Step 4; logical commit `docs(execution): start authored document migration` |
| ADM-002 | Publish the baseline disposition and durable research ledger | platform | Done | Pre-ledger RED was sole `LEDGER-MISSING`; final inventory/ledger equality is exactly 469 paths (`baseline=433`, `new=38`) with 14 columns, a pinned self-row, `preserve=183`, `transform=227`, `merge=59`, zero ledger Markdown/cross-document diagnostics, and empty semantic items; logical commit `docs(migration): inventory authored document dispositions` |
| ADM-003 | Normalize Stage 01–03 active design documents | platform | Done | Exact 34-path manifest SHA-256 `3cd63fa57b386f8036f14a8a59638318b5686fe4b618422b8577ad106f54e29f`; seven atomic batches `5/5/5/5/5/5/4` each returned zero exact-path diagnostics; all 34 ledger rows record official-primary or explicit repository-only source applicability and `shape-normalized`; compatibility debt moved from `266/1299` paths/occurrences to `232/1127`; logical commit `docs(migration): normalize active sdlc design documents` |
| ADM-004 | Normalize Stage 04–05 execution and operations documents | platform | Queued | Exact 120-path frozen manifest with the same batch-atomic ledger/debt/cap sequence and zero-diagnostic next-batch gate; logical commit `docs(migration): normalize execution and operations documents` |
| ADM-005 | Normalize governance, Current references, Archive links, and six support documents | platform | Queued | Exact 73-path frozen manifest with batch-atomic ledger/debt/cap checkpoints; structural-only checks preserve historical facts and Spec 027/031 route/schema/form/provider semantics; logical commit `docs(migration): normalize governance references and archive links` |
| ADM-006 | Consolidate AWS and Azure example documentation | platform | Queued | Exact 39-path debt manifest within the immutable 59-source merge/deletion set; synchronize the final zero-debt validator cap constants under the executable diff guard; `test -z "$(git ls-files examples/aws/docs examples/azure/docs)"`; logical commit `docs(migration): consolidate cloud example documentation` |
| ADM-007 | Enable strict validation and close Spec 030 | platform | Queued | `python3 scripts/validate-document-contract-registry.py --root . --mode strict`, both semantic validators in strict mode, and `bash scripts/validate-repo-quality-gates.sh .`; logical commit `chore(docs): cut over document profiles to strict validation` |

## Approval and Safety Boundaries

- **Allowed Paths**: Only the exact path set declared by the active ADM Plan
  Task may change. ADM-001 is limited to its seven Spec, Plan, Task, index, and
  canonical progress-ledger paths. ADM-003 through ADM-006 use the reviewed
  disjoint fixture allocation `34/120/73/39`; ADM-005's thirteen handoff paths
  are structural-only and retain Spec 027/031 semantic ownership.
- **Forbidden Paths**: Credentials, secrets, ignored `_workspace` children,
  local diagnostics, provider or cluster state, generated outputs, and paths
  outside the current ADM wave are excluded.
- **Approval Required**: Human approval is required before accepted-ADR
  supersession, cloud-document deletion, strict cutover, remote push or merge,
  publication, credential access, or live mutation.
- **Static Validation**: Run each Plan Task's RED/GREEN assertions, exact
  inventory or manifest checks, applicable semantic validators, repository
  quality gate, `git diff --check`, exact staged-path proof, and pre-commit.
- **Live Validation**: DEFER. Spec 030 changes authored repository content and
  does not establish Kubernetes, Argo CD, Vault, ESO, or cloud-provider runtime
  readiness.
- **Secret / Vault Handling**: Do not read, print, enumerate, move, or modify
  tokens, keys, certificates, kubeconfigs, secret values, Vault data, auth
  files, shell history, or ignored local state.
- **Rollback Plan**: Revert ADM commits newest-first. Each wave keeps content,
  ledger rows, finite-debt removal, validator proof, and execution evidence in
  one logical rollback unit.
- **Evidence Location**: This Task, its parent Plan, the durable migration
  ledger after ADM-002, the canonical progress ledger, logical commits, and
  ignored `.superpowers/sdd/adm-*-report.md` review packages.
- **GitOps Impact**: None; desired-state behavior is outside Spec 030.
- **Kubernetes Impact**: None; no live cluster command is authorized.
- **Operations / Runbook Impact**: Authored operational documents may be
  normalized in ADM-004 without changing live system behavior.

## Verification Summary

ADM-001 started from the expected RED state: the Task path was absent, so the
three-document lineage assertion exited 1 before reading any reciprocal links.
GREEN requires the Spec, Plan, and Task to name each other, unique active rows
in all three Stage indexes, exactly seven ADM rows, an append-only progress
entry, `git diff --check`, focused pre-commit, and an exact seven-path change
set. These checks are repository-static and do not access ignored local state,
secrets, live systems, remote CI, publication, push, merge, or deployment. Its
committed Task adds one normal authored target, so ADM-002 now consumes exactly
468/current and 37/new before ledger creation and must produce 469/current and
38/new with the ledger self-row.

ADM-002 published the sole durable migration evidence owner after proving the
fixture-derived `34/120/73/39` wave partition. The ordered 469-row table equals
the final inventory exactly, its cloud source rows merge to the two ADM-006
snapshot destinations, all remaining registered debt rows transform in their
own wave, and all other paths preserve themselves. The compatibility debt
container remains schema-v1 and growth-closed with `items: []`; strict and
compatibility cross-document checks now have zero ledger diagnostics.

Post-commit quality review corrected two orchestration boundaries without
changing the ledger rows: the Markdown self-test now evaluates the production
corpus against the current Asia/Seoul date while retaining fixed dates for
parser fixtures, and the active-currentness stale-contract scan excludes only
the exact migration ledger because its required inventory rows name archived
paths as evidence rather than current authority. Exact-path negative proof
prevents the exception from widening to other Stage 90 documents.

The first ADM-003 batch rehearsal changed only five documents while leaving
their compatibility records in place. The semantic validator correctly
returned nonzero `DEBT-UNUSED` failures, proving that a document-only batch
cannot satisfy the advertised checkpoint. Those edits were fully reverted.
The corrected ADM-003 through ADM-005 sequence now makes each batch atomic
across its exact documents, ledger rows, fixture records, and cumulative
fixture/validator caps; the next batch remains blocked until compatibility
mode reports zero diagnostics for the exact current NUL batch. The repository
quality gate's complete-fixture digest and mutation proof are refreshed once
after the wave's final batch, not at every intermediate checkpoint.
ADM-006 performs the final permitted cap/self-test synchronization after its
39 records are removed. Every ADM-003 through ADM-006 commit runs a staged
line guard that rejects validator changes outside the frozen numeric cap and
self-test comparisons.

ADM-003 completed the exact approved Stage 01–03 wave: five PRDs, five ARDs,
four accepted ADRs, and twenty Specs now use their canonical H2 shapes while
preserving every non-heading fact. The frozen manifest contains 34 paths with
SHA-256 `3cd63fa57b386f8036f14a8a59638318b5686fe4b618422b8577ad106f54e29f`
and was applied in seven atomic batches of `5/5/5/5/5/5/4`; every batch
finished with zero compatibility diagnostics for its exact NUL manifest.
Each corresponding durable-ledger row records whether the normalization used
an official primary source or an explicit repository-only contract review,
and all 34 results are `shape-normalized`.

The completed wave removed exactly its 34 fixture records. Affected-path and
semantic-occurrence debt moved from `266/1299` to `232/1127`; the remaining
required-heading/residue union is 196 paths with 51 overlaps. The complete
fixture semantic digest and mutation proofs now pin those after-values, while
the staged validator guard proves that only frozen numeric cap and self-test
expectations changed. The wave does not touch README profiles, ADM-004 paths,
live rules, templates, CI, agents, scripts beyond the two validation owners,
secrets, remote state, or cluster state.

## Traceability

- **Spec**: [Authored Document Migration Technical Specification](../../03.specs/030-authored-document-migration/spec.md)
- **Plan**: [Authored Document Migration Implementation Plan](../plans/2026-07-12-authored-document-migration.md)
- **Previous Tranche**: Semantic Document Validation, Spec 029
- **Next Tranche**: Affected Surface and Agent QA, Spec 031
