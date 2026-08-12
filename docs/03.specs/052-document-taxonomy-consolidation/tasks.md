---
title: 'Task: Document Taxonomy Consolidation'
type: sdlc/task
status: active
owner: platform
updated: 2026-08-12
---

# Task: Document Taxonomy Consolidation

## Overview

This Task records execution evidence for the approved work-unit-centered SDLC,
document-governance, and AI-agent-governance consolidation. The closed sequence records WORK-100 through WORK-115 plus the approved
pre-WORK-104 amendment. WORK-100 through WORK-107 and `WDTC-AMEND-001` are
complete; WORK-108 through WORK-115 remain the only successor work items.

All results are repository-static. No provider-runtime enforcement, hosted CI,
remote state, credential-bearing action, release action, or live-cluster result
is performed or claimed.

## Inputs

- **Plan**:
  [Document Taxonomy Consolidation Implementation Plan](plan.md)
- **Specification**:
  [Spec 052](spec.md)
- **Program requirement**:
  [PRD-008](../../01.requirements/008-workspace-document-taxonomy-consolidation.md)
- **Architecture**:
  [AD-0011](../../02.architecture/descriptions/ad-0011-document-taxonomy-consolidation-architecture.md)
- **Current decision**:
  [ADR-0024](../../02.architecture/decisions/0024-terminal-artifact-identity-and-archive-layout.md)
- **Accepted transition predecessor**:
  [ADR-0023](../../02.architecture/decisions/0023-work-unit-document-taxonomy-and-governance-authority.md)
- **External evidence**:
  [Spec-driven SDLC and document contracts](../../90.references/research/2026-08-08-wer/spec-driven-sdlc-and-document-contracts.md)
  and [AI agents and Agency Agents](../../90.references/research/2026-08-08-wer/ai-agents-and-agency-agents.md)
- **Design baseline**: transition design `14a0a75c`; approved terminal
  amendment carried by `1452dbfd` through `446e336a`.

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-100 | VAL-WDTC-004 | Accept ADR-0023 and correct the PRD-008 transition projection. | platform | Done | ADR-0023 accepted and current decision projection corrected. | `dd8b3465`, `ba180eca`; lifecycle/registry/link PASS |
| WORK-101 | VAL-WDTC-010 | Repair the three recorded all-files baseline failures without suppression. | platform | Done | Markdown, reviewed non-secret baseline, and fixed-point hook failures closed. | `57ce3746`; controller all-files PASS without mutation |
| WORK-102 | VAL-WDTC-001, VAL-WDTC-003, VAL-WDTC-006 | Add route states and the reviewed 132-document migration manifest/tool. | platform | Done | Exact `132 = 82 + 50` transition contract and fail-closed transaction/lock behavior implemented. | `9e367734` through `ffe136bf`; focused migration/registry PASS |
| WORK-103 | VAL-WDTC-006 | Archive the 50 unmatched execution documents. | platform | Done | 50 sources became validated ArchiveEnvelope records; repository total is 93 and prior records are immutable. | `0b53e9a1` through `a3cc852f`; archive/cutover/recovery PASS |
| WDTC-AMEND-001 | VAL-WDTC-013 through VAL-WDTC-016 | Approve terminal AD, artifact-ID, stable Stage 98, and exact script-closure design. | platform | Done | Spec 052 and ADR-0024 close the successor scope and ordering. | `1452dbfd` through `446e336a`; strict design gates PASS |
| WORK-104 | VAL-WDTC-001 | Move 82 retained Plan/Task documents, repair consumers, and rebaseline the destination pair. | platform | Done | Exact move applied; 41/41 siblings and only three Stage 04 READMEs remain; current links and immutable-history resolution are green. | Apply `phase=move moves=82 archives=50 sources=132`; strict transition registry, Markdown, links/owners PASS |
| WORK-105 | VAL-WDTC-004, VAL-WDTC-013 | Convert exactly eight ARDs to ADs, close legacy ARD/API-Spec consumers, activate core forms, and accept the AD-0011/ADR-0024/projection gate. | platform | Done | Exact eight ADs, Stage 99 core forms, retired authored API Spec route, complete consumer classifiers, and ADR-0024 authority accepted. | Strict-cutover 31/31, registry 132/67/31 and strict 504 paths, lifecycle 754, active corpus 100/100, closure 29/29, archive cutover 31/31, RIA 94/94, and aggregate PASS |
| WORK-106 | VAL-WDTC-006, VAL-WDTC-014, VAL-WDTC-015 | Implement artifact-ID and migration-ledger transition validators. | platform | Done | Transition permits absent mandatory IDs until WORK-108 but rejects every present mismatch, duplicate, prohibited declaration, malformed stable grouping, or ledger violation; terminal mode requires IDs. | Path-derived identity fixtures 20/20; strict-cutover 37/37; registry self 132/67/31 and strict 504; affected/staged/aggregate PASS |
| WORK-107 | VAL-WDTC-003, VAL-WDTC-006, VAL-WDTC-015 | Rehome all 93 Stage 98 records under stable paths. | platform | Done | Exact 93-to-93 stable rehome completed: 76 change leaves in 41 directories and 17 typed tombstones; legacy envelopes, payload/provenance, and dual recovery remain exact. | Archive recovery 27/27, cutover 33/33, validation 44/44, migration 58/58, retention 101/101, lifecycle 754 plus archive lifecycle 20/20, RIA 94/94, aggregate and all-files PASS |
| WORK-108 | VAL-WDTC-003, VAL-WDTC-014 | Backfill mandatory outer artifact IDs after WORK-107 stable rehome and WORK-105 acceptance. | platform | Queued | Not executed | Mandatory/prohibited namespace and global uniqueness evidence |
| WORK-109 | VAL-WDTC-001, VAL-WDTC-002, VAL-WDTC-003, VAL-WDTC-005 | Consolidate document authority and terminal routes. | platform | Queued | Not executed | Three owners, Stage 04 absence, Stage 05 stability, route/date negatives |
| WORK-110 | VAL-WDTC-008, VAL-WDTC-012 | Consolidate AI-agent governance contracts and projections. | platform | Queued | Not executed | Risk/trust/oversight/approval/trace/evaluation/provenance negatives; runtime remains DEFER |
| WORK-111 | VAL-WDTC-007, VAL-WDTC-016 | Reconcile the complete 50-row script disposition ledger. | platform | Queued | Not executed | Complete semantic and consumer disposition for all 50 assets |
| WORK-112 | VAL-WDTC-007, VAL-WDTC-016 | Consolidate orchestration and delete only `validate-harness.sh`. | platform | Queued | Not executed | Zero consumer/unique-rule loss and exact 49-script census |
| WORK-113 | VAL-WDTC-009 | Rotate progress and remove stale generated graph output recoverably. | platform | Queued | Not executed | Recovery, consumer, bounded-ledger, and residue evidence |
| WORK-114 | VAL-WDTC-001, VAL-WDTC-007, VAL-WDTC-010, VAL-WDTC-016 | Retire the transition manifest/tool/external test after cutover. | platform | Queued | Not executed | Zero transition consumers/residue and exact 47-script census |
| WORK-115 | VAL-WDTC-001 through VAL-WDTC-016 | Complete independent terminal closure and PRD-007 resumption handoff. | platform | Queued | Not executed | Criterion walk, independent reviews, lifecycle/aggregate/controller all-files/postflight |

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
- **Static Validation**: implementers run focused, strict, affected/staged,
  aggregate, and diff checks for the exact logical scope. Controller-owned
  all-files and commit actions run only when explicitly delegated.
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

WORK-100 and WORK-101 retain their accepted decision-lineage and controller
all-files fixed-point evidence. WORK-102 established the exact transition
contract and fail-closed migration tool. WORK-103 archived exactly 50 unmatched
sources into a 93-record repository while preserving prior envelopes.
`WDTC-AMEND-001` then closed the terminal AD, identity, archive-layout, and
script-inventory design through commit `446e336a` without changing the frozen
Stage 04 Plan/Task.

WORK-104 verified those frozen source blobs, applied only the reviewed move
phase, and reported `phase=move moves=82 archives=50 sources=132`. Post-apply
evidence is exact: 41 `plan.md`, 41 `tasks.md`, only three Stage 04 README
files, zero source/target or transaction residue, and zero Stage 05/90/98 body
diff. Manifest-derived current link repair closed the 790-finding RED; strict
links/owners, Markdown, transition registry, and migration checks pass. The
destination Plan and Task now use only the human-approved WORK-105 through
WORK-115 successor meanings.

WORK-105 converted exactly eight `docs/02.architecture/requirements/0004..0011`
records to `docs/02.architecture/descriptions/ad-0004..0011`, preserved the six
active and two accepted statuses, activated the AD route and Stage 99 PRD/SRS/IFC
and AD core forms, retired only the authored API Spec form while preserving
OpenAPI/GraphQL/Protobuf native surfaces, and accepted ADR-0024 as the current
PRD-008/AD-0011/Spec-052 authority. Stage 90 and Stage 98 remain byte-immutable,
Stage 05 has exactly seven reviewed AD-0007 link repairs, and no `artifact_id`
frontmatter is introduced before WORK-108.

WORK-106 added no document family or one-shot script. The existing registry
validator now owns the closed active and Stage 98 path-to-ID grammar, global
declared-ID uniqueness, prohibited namespace selection, transition-versus-
terminal missing-field rule, exact `change_id`/`migration_id` binding, full
legacy tombstone hash, and schema-versioned 14-field migration ledger. The
positive fixture proves the exact 93-row `76 + 17` census with `35/2/4` change
grouping and `3/8/4/2` tombstones; missing/extra fields, aliases, malformed
objects/digests, action/replacement errors, record-kind drift, and duplicate
legacy/stable/artifact identities fail closed. Stage 90 and Stage 98 remain
byte-identical and mandatory current IDs remain deliberately absent until
WORK-108.

WORK-107 rehomed the exact 93 Stage 98 records through the reviewed 14-field
`MIG-0001` ledger. The stable corpus contains 76 change leaves in 41
`chg-####-<slug>` directories (`35` pairs, `2` plan-only, `4` task-only) and
17 typed tombstones (`3/8/4/2`). Every legacy path has one unique stable path
and artifact identity; old ArchiveEnvelope bytes remain recoverable by the
pinned archive commit, while stable records preserve payload, source commit,
source blob, and content digest. Current documents still route only to the
Stage 98 collection index. Archive recovery 27/27, cutover 33/33, validation
44/44, migration 58/58, active-corpus retention 101/101, RIA 94/94, strict
registry/Markdown/links, residue closure, and the synchronized repository
aggregate all passed. Stage 90 remained unchanged and WORK-108 remains the
sole owner of mandatory current-document artifact-ID backfill.

The final finite lifecycle adapter consumes the rehome only when the WORK-106
commit, both registry blobs, canonical migration document and template, all 93
legacy envelope objects, and all 93 rendered stable objects match exactly.
Lifecycle staged validation, the 754-case lifecycle self-test, and the 20-test
archive lifecycle module pass. Affected and staged lanes pass over 130 paths;
plain pre-commit and the 132-path all-files lane pass every applicable gate
without mutation. The final no-renames scope is `A95/D93/M37` with zero
unstaged or untracked paths.

The controller-owned WORK-104 fixed point ran
`TMPDIR=/tmp pre-commit run --all-files` with exit `0`; every applicable hook
passed and the run produced no mutation. Post-run scope remained exactly
`A82/D82/M73` with zero unstaged paths.

No provider, hosted, remote, credential-bearing, Release-family, or live action
was performed or claimed. WORK-108 is the next owner and may begin only while
the completed WORK-107 stable rehome and WORK-105 accepted eight-AD authority
gate remain green.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-100](plan.md#work-breakdown) | Complete. | ADR-0023 acceptance and PRD-008 transition projection evidence in `dd8b3465`/`ba180eca`. |
| [WORK-101](plan.md#work-breakdown) | Complete. | Baseline repair `57ce3746` and controller all-files fixed point. |
| [WORK-102](plan.md#work-breakdown) | Complete. | Exact transition routes, manifest/tool hardening, and `132/82/50` checks. |
| [WORK-103](plan.md#work-breakdown) | Complete. | 50 added envelopes, 93-record index, immutable prior records, and recovery checks. |
| [WDTC-AMEND-001](plan.md#work-breakdown) | Complete. | Human-approved Spec 052/ADR-0024 design carried through `446e336a`. |
| [WORK-104](plan.md#work-breakdown) | Complete. | Exact 82 move, 41/41 siblings, three Stage 04 READMEs, repaired consumers, and strict focused gates. |
| [WORK-105](plan.md#work-breakdown) | Complete. | Exact eight-AD conversion, legacy ARD/authored API Spec retirement, ADR-0024 authority acceptance, native surface preservation, and strict focused gates passed. |
| [WORK-106](plan.md#work-breakdown) | Complete. | Closed path-derived/global identity and exact 14-field ledger validators; strict-cutover 37/37 and repository gates passed. |
| [WORK-107](plan.md#work-breakdown) | Complete. | Exact 93-to-93 stable rehome, 76/17 census, immutable payload/provenance, old-envelope recovery, and aggregate PASS. |
| [WORK-108](plan.md#work-breakdown) | Not executed. | Global artifact-ID backfill pending WORK-107 stable rehome and complete AD conversion. |
| [WORK-109](plan.md#work-breakdown) | Not executed. | Document authority and terminal routes pending. |
| [WORK-110](plan.md#work-breakdown) | Not executed. | AI-agent governance contract consolidation pending. |
| [WORK-111](plan.md#work-breakdown) | Not executed. | Complete 50-row script disposition pending. |
| [WORK-112](plan.md#work-breakdown) | Not executed. | Orchestration consolidation and exact 49 count pending. |
| [WORK-113](plan.md#work-breakdown) | Not executed. | Recoverable progress/graph cleanup pending. |
| [WORK-114](plan.md#work-breakdown) | Not executed. | Transition retirement and exact 47 count pending. |
| [WORK-115](plan.md#work-breakdown) | Not executed. | Independent VAL-WDTC-001..016 closure and PRD-007 handoff pending. |
