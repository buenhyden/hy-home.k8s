---
title: 'Task: Document Taxonomy Consolidation'
type: sdlc/task
status: active
owner: platform
updated: 2026-08-09
---

# Task: Document Taxonomy Consolidation

## Overview

This Task records execution evidence for the approved work-unit-centered SDLC,
document-governance, and AI-agent-governance consolidation. The eleven work
packages are dependency ordered and each closes through one reviewed logical
commit. The active Plan and Task move into the Spec 052 folder during WDTC-104.

All results are repository-static. No provider-runtime enforcement, hosted CI,
remote state, credential-bearing action, release action, or live-cluster result
is performed or claimed.

## Inputs

- **Plan**:
  [Document Taxonomy Consolidation Implementation Plan](../plans/2026-08-07-document-taxonomy-consolidation.md)
- **Specification**:
  [Spec 052](../../03.specs/052-document-taxonomy-consolidation/spec.md)
- **Program requirement**:
  [PRD-008](../../01.requirements/008-workspace-document-taxonomy-consolidation.md)
- **Architecture**:
  [ARD-0011](../../02.architecture/requirements/0011-document-taxonomy-consolidation-architecture.md)
- **Decision**:
  [ADR-0023](../../02.architecture/decisions/0023-work-unit-document-taxonomy-and-governance-authority.md)
- **External evidence**:
  [Spec-driven SDLC and document contracts](../../90.references/research/2026-08-08-wer/spec-driven-sdlc-and-document-contracts.md)
  and [AI agents and Agency Agents](../../90.references/research/2026-08-08-wer/ai-agents-and-agency-agents.md)
- **Design baseline**: commit `14a0a75c` (`docs: rebaseline SDLC governance design`).

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-100 | VAL-WDTC-004 | Accept ADR-0023 and atomically replace the erroneous PRD-008 decision projection. | platform | Done | ADR-0023 accepted; PRD-008/ARD-0011/Spec-052 now project decision 0023. | Staged lifecycle, registry self-test, strict registry, links/owners, and commit evidence |
| WORK-101 | VAL-WDTC-010 | Repair the three recorded all-files baseline failures without suppressing checks. | platform | Done | Fixed the Spec 053 Plan `MD001`, adjudicated three approved candidates, accepted current-hook synchronization, and removed one raw-scan-proven stale orphan. | Two fixed-point focused passes; controller all-files rerun exited 0 with every applicable hook passing and no mutation |
| WORK-102 | VAL-WDTC-001, VAL-WDTC-003, VAL-WDTC-006 | Add legacy/transition/terminal route semantics and a reviewed 132-document manifest/tool. | platform | Queued | Not executed | RED/GREEN route fixtures, `132/82/50` manifest counts, dry-run result |
| WORK-103 | VAL-WDTC-006 | Archive the 50 unmatched execution documents and remove their live sources. | platform | Queued | Not executed | 50 added envelopes, 93-record index, prior-43 immutable diff, archive tests |
| WORK-104 | VAL-WDTC-001 | Move 82 retained Plan/Task documents into 41 Spec work units and repair reciprocal links. | platform | Queued | Not executed | 41/41 inventory, transition registry, Markdown and link results |
| WORK-105 | VAL-WDTC-002, VAL-WDTC-003, VAL-WDTC-005 | Consolidate Stage 00/99 authority, update forms, remove template mirrors, and activate terminal taxonomy. | platform | Queued | Not executed | Three prose owners, 26 mirror-profile retirement, Stage 04 absence, Stage 05/Release assertions |
| WORK-106 | VAL-WDTC-008, VAL-WDTC-012 | Atomically activate harness risk, trust, oversight, approval, trace, evaluation, provenance, and evidence-owner controls. | platform | Queued | Not executed | Harness/provider schema and semantic negative fixtures; runtime evidence remains DEFER |
| WORK-107 | VAL-WDTC-007 | Consolidate pre-commit/aggregate orchestration and retire `validate-harness.sh` after zero consumers. | platform | Queued | Not executed | Governance-CI topology, affected-surface parity, retain-contract ledger, all-files result |
| WORK-108 | VAL-WDTC-006, VAL-WDTC-009 | Archive and rotate the progress ledger, then remove and ignore stale tracked graph output. | platform | Queued | Not executed | Recovery proof, bounded live ledger, zero tracked graph files, ignore result |
| WORK-109 | VAL-WDTC-001, VAL-WDTC-010 | Delete migration-only assets and prove the complete terminal repository state. | platform | Queued | Not executed | Zero scaffolding/residue, strict terminal bundle, aggregate and all-files PASS |
| WORK-110 | VAL-WDTC-001 through VAL-WDTC-012 | Complete the criterion walk, independent reviews, lifecycle closure, and PRD-007 resumption handoff. | platform | Queued | Not executed | Per-criterion evidence, two-stage review, final lifecycle/aggregate/all-files results |

## Approval and Safety Boundaries

- **Allowed Paths**: `docs/**` with existing Stage 98 envelopes read-only,
  repository-local gateway/provider projections, `.github/**`, `.pre-commit-config.yaml`,
  `.gitignore`, `scripts/**`, and `tests/**` named by the Plan.
- **Forbidden Paths**: modification/deletion of an existing
  `docs/98.archive/**` envelope or payload; `gitops/**`, `infrastructure/**`,
  `traefik/**`, `policy/**`, `secrets/**`, provider credentials, remote systems,
  and live-cluster state.
- **Approval Required**: new document families, Stage 05 or lifecycle-ID
  renumbering, uncertain historical disposition, unique rule/fixture removal,
  evidence-class promotion, existing archive mutation, secret/credential access,
  external write, remote action, or live mutation.
- **Static Validation**: focused commands in each Plan task, strict document
  lanes, `git diff --check`, `bash scripts/validate-repo-quality-gates.sh .`,
  and terminal `TMPDIR=/tmp pre-commit run --all-files` must pass.
- **Live Validation**: `DEFER` — the program performs and claims no provider,
  hosted, remote, credential-bearing, Release, or live action.
- **Secret / Vault Handling**: scanner findings are adjudicated by exact
  location without printing values. No token, secret, kubeconfig, Vault value,
  provider body, prompt body, or credential file is read or retained.
- **Rollback Plan**: each WORK item is one revertible commit. A failing
  uncommitted tranche is reversed only with a reviewed patch; broad reset and
  archive-payload repair are prohibited.
- **Evidence Location**: this Task, the corresponding logical commits, new
  archive index entries, and `docs/00.agent-governance/memory/progress.md`.

## Verification Summary

The written design and implementation plan were reviewed. WORK-100 and WORK-101
are complete; WORK-102 through WORK-110 remain queued. Staged lifecycle, registry self-test,
strict registry, and strict links/owners validate the accepted ADR-0023 and its
atomic PRD-008 projection. At the WDTC-101 implementation base, the
authoritative repeated detect-secrets run reproduced the two source-ledger
keywords and one historical Plan hex candidate without exposing values. Only
those baseline entries were adjudicated as non-secrets. The deterministic
current-hook baseline synchronization was also accepted: filters, refreshed
legacy-cutover line numbers, one now-excluded duplicate removal, and timestamp;
the source ledger remained byte-identical. A second fixed-point detector run
attempted an additional reference-architecture removal whose current line did
not match an active exclusion, but an in-memory raw scan proved its stored
candidate absent; it was therefore removed as a stale orphan. Two subsequent
focused detector runs passed without mutation. The controller reran the exact
all-files command on that staged fixed point: it exited 0, every applicable
hook passed, and no worktree mutation remained.

The earlier proposal to renumber operations or delete active-corpus validators
is withdrawn. Stage 05 remains stable, Release is excluded, and the five
active-corpus validators remain `retain-contract` unless later evidence proves
zero consumers and no unique semantics.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-100](../plans/2026-08-07-document-taxonomy-consolidation.md#work-breakdown) | Complete. | VAL-WDTC-004 accepted ADR-0023 and corrected immutable PRD-008 machine projection passed staged lifecycle, registry self-test/strict, and strict links/owners validation. |
| [WORK-101](../plans/2026-08-07-document-taxonomy-consolidation.md#work-breakdown) | Complete. | VAL-WDTC-010 corrects the Spec 053 Plan heading, records three reviewed non-secret entries, accepts synchronization, and removes one raw-scan-proven stale orphan. The detector reached a two-run no-mutation fixed point; the controller all-files rerun exited 0 with every applicable hook passing and no mutation. |
| [WORK-102](../plans/2026-08-07-document-taxonomy-consolidation.md#work-breakdown) | Not executed. | VAL-WDTC-001/003/006 transition routes, manifest, and dry-run evidence are pending. |
| [WORK-103](../plans/2026-08-07-document-taxonomy-consolidation.md#work-breakdown) | Not executed. | VAL-WDTC-006 additive archive and immutable-base evidence are pending. |
| [WORK-104](../plans/2026-08-07-document-taxonomy-consolidation.md#work-breakdown) | Not executed. | VAL-WDTC-001 work-unit move and reciprocal-link evidence are pending. |
| [WORK-105](../plans/2026-08-07-document-taxonomy-consolidation.md#work-breakdown) | Not executed. | VAL-WDTC-002/003/005 authority, template, terminal-route, Stage 05, and Release evidence are pending. |
| [WORK-106](../plans/2026-08-07-document-taxonomy-consolidation.md#work-breakdown) | Not executed. | VAL-WDTC-008/012 agent-system schema/semantic and evidence-class results are pending. |
| [WORK-107](../plans/2026-08-07-document-taxonomy-consolidation.md#work-breakdown) | Not executed. | VAL-WDTC-007 orchestration and validator-disposition results are pending. |
| [WORK-108](../plans/2026-08-07-document-taxonomy-consolidation.md#work-breakdown) | Not executed. | VAL-WDTC-006/009 progress recovery and generated-output cleanup results are pending. |
| [WORK-109](../plans/2026-08-07-document-taxonomy-consolidation.md#work-breakdown) | Not executed. | VAL-WDTC-001/010 terminal residue and all-files results are pending. |
| [WORK-110](../plans/2026-08-07-document-taxonomy-consolidation.md#work-breakdown) | Not executed. | VAL-WDTC-001 through VAL-WDTC-012 criterion walk, reviews, lifecycle closure, and resumption evidence are pending. |
