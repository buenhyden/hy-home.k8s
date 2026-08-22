---
title: 'Document Taxonomy Consolidation Implementation Plan'
type: sdlc/plan
status: active
owner: platform
updated: 2026-08-12
artifact_id: "PLAN-0052"
---

# Document Taxonomy Consolidation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> `superpowers:subagent-driven-development` to implement this plan task by
> task. Each task requires a fresh implementation worker, specification review,
> code-quality review, focused RED/GREEN evidence, and one logical commit.
> Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Establish one work-unit-centered SDLC document topology, retire the
live Stage 04 execution tree without renumbering Stage 05, consolidate document
and AI-agent governance authorities, preserve unique history, and finish with
all repository-static gates green.

**Architecture:** The migration uses an explicit, reviewed source-to-target
manifest and a three-state route contract (`legacy`, `transition`, `terminal`).
Tests and transition routes land before any move; orphan history is archived
before removal; current Plan/Task pairs then move beside their Specs; only then
are Stage 04 routes and temporary migration assets removed. Document policy,
agent-system controls, validation orchestration, and generated/memory cleanup
remain separate revertible commits.

**Tech Stack:** Python 3 standard library, JSON Schema Draft 2020-12,
`unittest`, Bash, Git plumbing, Markdown/frontmatter, pre-commit, and the
repository's existing document, archive, harness, and validation-surface
contracts.

## Global Constraints

- The approved terminal work-unit route is
  `docs/03.specs/<NNNN>-<slug>/{spec.md,plan.md,tasks.md}`; `plan.md` is optional
  and `tasks.md` requires both siblings.
- `docs/03.specs/` is retired; its numeric slot remains unused.
- `docs/05.operations/` remains unchanged and continues to own guides,
  incidents, policies, and runbooks.
- Do not create a Release profile, template, folder, lifecycle, validator, or
  document.
- Mutable authored paths use stable identifiers or slugs. Dates remain in
  frontmatter; terminal path dates are limited to Stage 90 observations/snapshots
  and actual Incident/Postmortem identity. WORK-107 removes dates and years from
  terminal Stage 98 paths through the reviewed 93-row migration ledger.
- Existing identifiers are immutable except for the human-approved WORK-109
  width normalization in ADR-0025. ADR-0024 remains the archive/form decision
  and ADR-0025 is the current path-width decision associated with
  PRD-0008/AD-0011/Spec-0052;
  ADR-0023 remains the accepted transition predecessor, while ADR-0021 and its
  original program scope remain accepted and unchanged.
- Embedded Stage 98 payload and provenance bytes are immutable. WORK-107 may
  rehome the 93 outer records only through the schema-versioned 93-to-93 ledger,
  old-envelope proof, and dual recovery evidence approved by ADR-0024. No
  migration may change an embedded historical claim or collapse two records onto
  one stable path.
- Stage 90 historical observation bodies are not rewritten. Current navigation
  may annotate a retired path without changing the observation's claim.
- The document-profile registry owns machine values. Stage 00 owns agent-facing
  policy; Stage 99 owns template/lifecycle rationale and canonical forms.
- Repository-static declaration never proves provider-runtime enforcement,
  hosted CI, remote state, credentials, or live-cluster behavior.
- No secret value, kubeconfig, credential, provider account, remote service, or
  live cluster is read or mutated.
- Every task must pass its focused tests, `git diff --check`, strict document
  checks applicable to the diff, and `bash scripts/validate-repo-quality-gates.sh .`
  before commit.
- Use `TMPDIR=/tmp` for pre-commit in this Linux/WSL worktree; the unqualified
  baseline failure is recorded as environment evidence and is not permission to
  disable a check.
- After every formatter-capable all-files run, inspect `git status --short`,
  `git diff`, and `git diff --cached`; review each mutation, stage only the
  logical task files, rerun focused and exact staged checks, then rerun
  all-files until it produces no mutation. Finish with both `git diff --check`
  and `git diff --cached --check`.
- One task equals one conventional, revertible commit. Do not combine the
  archive, mass move, governance, harness, validator, cleanup, or closure units.

---

## Overview

This plan executes [Spec 052](spec.md)
after approval of the complete design. It supersedes the prior execution plan
that proposed renumbering operations and deleting validator families without
current-consumer proof.

The work is one integrated plan because route schema, path movement, reciprocal
links, archive evidence, and terminal rejection must change in dependency order.
The document-authoring, agent-governance, orchestration, and cleanup tranches
are nevertheless independent review gates and may be reverted without undoing
the path migration.

## Context

The design baseline is commit `14a0a75c`. At that commit the live corpus has:

- 49 Spec work-unit directories;
- 65 authored Plans and 67 authored Tasks in Stage 04;
- 41 exact same-slug Spec/Plan/Task triads;
- 24 unmatched Plans and 26 unmatched Tasks, representing 50 execution
  documents after accounting for 23 common orphan slugs, one plan-only record,
  and three task-only records;
- three Stage 04 README/index files;
- 43 existing immutable ArchiveEnvelope records;
- nine tracked `graphify-out/**` files consuming about 12 MiB;
- an approximately 14,900-line shared progress ledger.

The existing registry routes Plans and Tasks only through date-prefixed Stage
04 patterns. PRD-0008/AD-0011/Spec-052 currently names accepted ADR-0021 even
though ADR-0021 owns a different program. ADR-0023 is the human-approved
decision and is promoted through `draft -> active -> accepted`, never directly
from draft to accepted.

The raw pre-change all-files hook recorded three baseline issues: the registry
self-test could not allocate its configured temporary location, detect-secrets
found three unadjudicated non-secret values, and Markdown lint rejected the
Spec 053 Plan's H1-to-H3 jump. With `TMPDIR=/tmp`, every strict document lane
and the aggregate repository gate passes; the three all-files defects remain
explicit Task 2 work and are not terminal waivers.

### Legacy Task ledger inputs

This Task records execution evidence for the approved work-unit-centered SDLC,
document-governance, and AI-agent-governance consolidation. The closed sequence records WORK-100 through WORK-115 plus the approved
pre-WORK-104 amendment. WORK-100 through WORK-108 and `WDTC-AMEND-001` are
complete; WORK-109 through WORK-115 are transferred to the corresponding
Spec 0054 work items and no longer form a competing active queue.

All results are repository-static. No provider-runtime enforcement, hosted CI,
remote state, credential-bearing action, release action, or live-cluster result
is performed or claimed.

- **Plan**:
  [Document Taxonomy Consolidation Implementation Plan](plan.md)
- **Specification**:
  [Spec 052](spec.md)
- **Program requirement**:
  [PRD-0008](../../01.requirements/0008-workspace-document-taxonomy-consolidation.md)
- **Architecture**:
  [AD-0011](../../02.architecture/descriptions/0011-document-taxonomy-consolidation-architecture.md)
- **Current decision**:
  [ADR-0024](../../02.architecture/decisions/0024-terminal-artifact-identity-and-archive-layout.md)
- **Accepted transition predecessor**:
  [ADR-0023](../../02.architecture/decisions/0023-work-unit-document-taxonomy-and-governance-authority.md)
- **External evidence**:
  [Spec-driven SDLC and document contracts](../../90.references/research/2026-08-08-wer/spec-driven-sdlc-and-document-contracts.md)
  and [AI agents and Agency Agents](../../90.references/research/2026-08-08-wer/ai-agents-and-agency-agents.md)
- **Design baseline**: transition design `14a0a75c`; approved terminal
  amendment carried by `1452dbfd` through `446e336a`.
## Goals & In-Scope

- Activate accepted ADR-0023 and correct the machine lineage atomically.
- Close the observed all-files baseline defects without suppressing scanners.
- Add tested legacy/transition/terminal route semantics.
- Commit a complete 132-document execution manifest before changing paths.
- Append ArchiveEnvelope records for the 50 unmatched execution documents.
- Move the 82 retained Plan/Task documents into their 41 Spec work units.
- Retire Stage 04 and prove Stage 05 stability and Release-family absence.
- Normalize every current numeric document token to four digits, including the
  eight PRD paths, all Stage 03 work-unit directories and IDs, and the exact
  lowercase `inc-####-<slug>` Incident directory route.
- Consolidate four Stage 00 authoring rules into one policy owner and six Stage
  99 support documents into two rationale owners.
- Update Plan/Task forms for sibling placement and stable filename policy.
- Extend the existing harness and provider-evidence contracts with closed
  agent-system risk, trust, oversight, approval, trace, evaluation, provenance,
  and evidence-owner policy shapes.
- Consolidate duplicate orchestration while retaining semantically distinct
  validators and their unique negative fixtures.
- Rotate progress history recoverably and remove stale generated graph output.
- Remove every temporary migration asset and close with all-files PASS.

## Non-Goals & Out-of-Scope

- Renumbering Stage 05 or any PRD, AD, ADR, or Spec identifier.
- Editing an existing ArchiveEnvelope or historical Stage 90 claim.
- Creating Release, tutorial, or explanation document families.
- Merging Spec, Plan, and Task bodies into one Markdown document.
- Merging validators merely because their names or input directories overlap.
- Deleting the active-corpus validator family; the current audit classifies its
  five members as distinct live aggregate consumers.
- Changing agent roles, provider authentication, model availability, platform
  desired state, GitHub settings, hosted CI, remote systems, or live runtime.
- Executing Specs 047-051 during the taxonomy migration.

## Work Breakdown

| ID | Closed scope | State | Evidence or successor gate |
| --- | --- | --- | --- |
| WORK-100 | Accept ADR-0023 and correct the PRD-0008 transition projection. | Complete | `dd8b3465`, `ba180eca`; lifecycle/registry/link gates passed. |
| WORK-101 | Repair the three recorded all-files baseline failures without suppression. | Complete | `57ce3746`; controller all-files fixed point passed without mutation. |
| WORK-102 | Add transition routes and the reviewed `132 = 82 + 50` manifest/tool. | Complete | `9e367734` through `ffe136bf`; route, transaction, lock, and manifest tests passed. |
| WORK-103 | Archive the 50 unmatched execution documents. | Complete | `0b53e9a1` plus archive hardening through `a3cc852f`; 93 records and prior-envelope immutability proved. |
| WDTC-AMEND-001 | Approve the terminal AD, artifact-ID, Stage 98, and script-closure design before the move. | Complete | `1452dbfd` through `446e336a`; Spec 052 and ADR-0024 close WORK-105 through WORK-115. |
| WORK-104 | Move the exact 82 current Plan/Task sources, repair consumers, and rebaseline this destination pair. | Complete | Move apply reported `phase=move moves=82 archives=50 sources=132`; 41/41 siblings, three Stage 04 READMEs, strict transition registry, Markdown, and links/owners passed. |
| WORK-105 | Activate the AD route and Stage 99 core forms; convert exactly ARD-0004..0011 to AD-0004..0011; close all legacy ARD and authored API Spec consumers; perform the separate AD-0011/ADR-0024/projection authority gate. | Complete | Exact eight-record census, zero current/unclassified legacy consumers, retired-route negatives, native-contract preservation, atomic ADR-0024 acceptance, strict-cutover 31/31, lifecycle 754, archive cutover 31/31, RIA 94/94, and aggregate PASS. |
| WORK-106 | Implement global artifact-identity and migration-ledger transition validators and negative fixtures. | Complete | Existing registry validator owns transition/terminal identity selection and the exact 14-field ledger; focused 37/37 plus affected/staged/aggregate gates passed with Stage 90/98 unchanged. |
| WORK-107 | Rehome all 93 Stage 98 records under the stable grammar. | Complete | Exact 93-to-93 ledger; 76 change leaves in 41 directories and 17 typed tombstones; immutable payload/provenance, old-envelope proof, dual recovery, finite lifecycle admission, aggregate and all-files PASS. |
| WORK-108 | Backfill mandatory outer `artifact_id` values after WORK-107 stable rehome and the complete AD conversion. | Complete | Exact 286-identity census (`192` current + `93` stable archive + `1` migration), global uniqueness, mandatory/prohibited profile parity, closure 30/30, retention 102/102, RIA 94/94, aggregate/affected/staged, and plain/all-files pre-commit PASS. |
| WORK-109 | Consolidate document authority, activate terminal routes, and normalize current numeric identities to four digits. | Transferred | Transferred to Spec 0054 `WORK-054-002`; Spec 0052 no longer owns an active competing queue. |
| WORK-110 | Consolidate workspace AI-agent governance contracts and projections. | Transferred | Transferred to Spec 0054 `WORK-054-003`. |
| WORK-111 | Reconcile the complete 50-row script disposition ledger. | Transferred | Transferred to Spec 0054 `WORK-054-010`. |
| WORK-112 | Consolidate orchestration, migrate consumers, and delete only `validate-harness.sh`. | Transferred | Transferred to Spec 0054 `WORK-054-011`. |
| WORK-113 | Rotate/clean progress and generated graph surfaces with recovery and consumer proof. | Transferred | Transferred to Spec 0054 `WORK-054-012`. |
| WORK-114 | Delete the transition manifest/tool/external test after cutover and prove 47 scripts. | Transferred | Transferred to Spec 0054 `WORK-054-013`. |
| WORK-115 | Perform independent terminal closure and PRD-0007 resumption handoff. | Transferred | Transferred to Spec 0054 `WORK-054-014`. |

### File Structure and Interfaces

#### Temporary migration assets

- `scripts/document-taxonomy-migration.json` — temporary reviewed manifest;
  exactly 132 source documents, 82 `move-current` entries and 50
  `archive-unique` entries. While tracked it selects the temporary closed
  `native/document-migration-manifest` profile and `transition` lifecycle;
  terminal route state requires its absence. WORK-114 deletes it and removes
  that temporary profile atomically.
- `scripts/migrate-document-work-units.py` — temporary fail-closed manifest
  validator and mover. WORK-114 deletes it.
- `tests/test_migrate_document_work_units.py` — temporary tests retained until
  terminal behavior is incorporated into the registry fixtures, then deleted
  by WORK-114.

The tool exposes these exact interfaces:

| Name | Inputs | Return | Failure |
| --- | --- | --- | --- |
| `load_manifest` | `path: Path` | immutable tuple of manifest entry mappings | `MigrationAbort` on duplicate keys, schema mismatch, or unsafe path |
| `validate_manifest` | `root: Path`, entries, `expected_source_commit: str` | sorted tuple of diagnostics; empty means valid | never writes |
| `validate_work_unit_paths` | mapping from work-unit ID to present basenames | sorted tuple of `WORK-UNIT-*` diagnostics | never writes |
| `validate_counts` | integer move, archive, and total counts | `None` only for `82`, `50`, and `132` | `MigrationAbort` on any other count |
| `plan_phase` | `root: Path`, entries, phase `archive` or `move` | immutable ordered `(source, target)` path pairs | `MigrationAbort` before writes |
| `apply_phase` | `root: Path`, planned pairs, phase | `None` after all operations succeed | `MigrationAbort`; no operation begins unless the full plan validates |

The CLI is fixed to:

```text
python3 scripts/migrate-document-work-units.py --root . --manifest scripts/document-taxonomy-migration.json --check
python3 scripts/migrate-document-work-units.py --root . --manifest scripts/document-taxonomy-migration.json --phase archive --apply
python3 scripts/migrate-document-work-units.py --root . --manifest scripts/document-taxonomy-migration.json --phase move --apply
```

`--apply` requires every manifest-controlled source and target to be clean at
command start, exact source blob matches, absent targets, no path under an
existing Stage 98 record, and a phase whose prerequisites are satisfied.
Unrelated focused-test edits may coexist. It stops before the first write on
any failure.

The temporary profile is a native JSON canonical form with exactly one route,
`scripts/document-taxonomy-migration.json`. Its schema requires top-level
`state: "transition"`, `sourceCommit`, and `entries`; rejects additional
properties; and is admitted only while the document-contract CLI runs with
`--route-state transition`. Legacy does not require it and terminal rejects
both the route and the profile. WORK-114 deletes the manifest, its schema
projection, and its temporary registry fixture in one commit while retaining
permanent terminal route fixtures.

#### Archive admission and recovery

`document-profiles.json` owns a versioned `archiveNamespaces` contract before
the first new WDTC envelope is generated:

| Namespace | Policy | Initial/final membership |
| --- | --- | --- |
| `arwb-base` | exact and immutable | 31 / 31 |
| `acer-additive` | exact and immutable | 12 / 12 |
| `wdtc-execution` | exact reviewed manifest subset | 0 / 50 |
| `progress-snapshot` | append-only, unique source blob and target | 0 / 1 |

The ACER validator continues to assert its exact 43-record managed aggregate
(`31 + 12`) and additionally permits only registry-declared non-ACER
namespaces. It reports repository total separately: 93 after WDTC execution
archive admission and 94 after the progress snapshot. A new record may not
alter any earlier envelope, payload digest, namespace membership, or exact
count.

The generic interface is versioned as `archiveContractVersion: 2` and is
exposed by `archive_validation.validate_repository_archive(root, registry)`.
`archive_cutover.py --root .` calls it in addition to preserving the fixed
historical cutover proofs. The Stage 98 README is the human-readable index;
the validator parses its rows and requires exact parity with discovered
envelopes and registry namespace membership, so no second mutable index is
introduced. Before writing any envelope, the admission path runs the existing
secret classifier against the source bytes and fails closed without printing
raw payload content. Recovery is read-only and uses:

```text
python3 scripts/archive_recovery.py --root . --record <archive-path> --verify
python3 scripts/archive_recovery.py --root . --record <archive-path> --output <temporary-path>
```

`--verify` compares header identity, source blob, payload digest, and recovered
bytes without writing. `--output` requires a path outside tracked live-document
routes, refuses overwrite, and never restores directly into the repository.

#### Terminal document owners

- `docs/00.agent-governance/rules/document-authoring.md` — agent-facing stage
  selection, timing, language, safety, lifecycle, checklist, and validation
  procedure.
- `docs/99.templates/support/document-contract.md` — exact-one-profile
  selection, form/body/frontmatter rationale, protected-surface boundary.
- `docs/99.templates/support/document-lifecycle.md` — lifecycle,
  supersession, retention, archive, date exception, and legacy-disposition
  rationale.
- `docs/99.templates/support/document-profiles.json` and schema — sole machine
  owner of routes, states, values, relationships, forms, and exceptions.

The Plan/Task template files stay at
`docs/99.templates/templates/sdlc/execution/{plan,task}.template.md`: the
directory names the execution artifact family, not the retired Stage 04 path.
Their body and link guidance changes to sibling `spec.md`, `plan.md`, and
`tasks.md` placement.

#### Terminal agent-governance owners

- `docs/00.agent-governance/contracts/harness-contract.json` and schema —
  provider-neutral `agentSystems`, `evidenceOwnerPolicies`, and
  `approvalBoundaryProjection` owner.
- `docs/00.agent-governance/contracts/provider-runtime-evidence.json` and
  schema — provider observation/reference shape; no raw runtime body.
- `docs/00.agent-governance/rules/approval-boundaries.md` — human-readable
  input matrix with stable surface IDs; it is not a second machine registry.
- Existing harness/provider validators and fixtures — schema and semantic
  enforcement; no new duplicate validator executable.

#### Retained and retired scripts

- Retain `scripts/validate-repo-quality-gates.sh` as the aggregate owner.
- Retain registry, Markdown, links/owners, archive, security, CI,
  agent-semantic, lifecycle, and active-corpus validators when their input,
  negative fixture, diagnostic, or evidence claim is distinct.
- Retire `scripts/validate-harness.sh` only after root README, PR template,
  scripts index, tests, and current work-unit consumers no longer execute it.
- Collapse redundant pre-commit governance hooks into the aggregate hook only
  after `agent-governance-ci.json`, fixtures, and topology tests admit the new
  exact sequence.

### Task Details

#### Completed foundation through WORK-104

WORK-100 through WORK-103 and `WDTC-AMEND-001` are closed by the commits and
evidence named in the work-breakdown table. WORK-104 consumed only the reviewed
`move-current` manifest phase. The first ordinary apply attempt failed closed
at `MIGRATION-LOCK` before any write; the controller-authorized exact retry
reported `phase=move moves=82 archives=50 sources=132`. Post-apply checks prove
41 sibling `plan.md` files, 41 sibling `tasks.md` files, only the three Stage 04
README files, no transaction residue, and no Stage 05, Stage 90, or Stage 98
body change. Current consumers were recalculated from the manifest; immutable
Stage 90 observations and unchanged Stage 05 evidence are resolved through the
same reviewed mapping rather than rewritten.

The moved source Plan and Task were first verified against their frozen Git
blob identities. Only the Stage 03 destination copies are rebaselined here.
This schedule supersedes the old destination WORK-105 through WORK-110
meanings; it does not rewrite the frozen pre-move evidence.

#### Successor execution protocol

1. Execute only WORK-105 through WORK-115 in order. WORK-107 and WORK-108 may
   not start until WORK-105's complete eight-AD conversion and authority
   acceptance pass.
2. Establish focused RED before validator or fixture behavior changes, then
   record focused GREEN. Preserve immutable/history classifications instead of
   suppressing current failures.
3. Each logical work item is independently reviewed and committed by the
   controller. Implementers stage only the exact owned paths and leave zero
   unstaged changes; they do not run controller-owned all-files validation or
   create commits unless explicitly delegated.
4. Never edit embedded Stage 98 payloads, Stage 90 observation bodies, Stage 05
   topology, identifiers, or operational meaning, credentials, remote state,
   or live infrastructure. Stage 05 link-label/path bytes may change only for
   the seven reviewed AD-0007 repairs. Do not create a Release-family artifact.
5. Commands operate from the repository root, use explicit paths, and may not
   use broad reset, checkout, recursive deletion, unreviewed glob mutation, or
   unpinned external execution.

#### Successor acceptance order

| Work | Required entry condition | Required exit condition |
| --- | --- | --- |
| WORK-105 | WORK-104 focused and aggregate evidence accepted. | Eight ADs and all current consumers converted; API Spec retirement gates independent and complete; ADR-0024 authority accepted atomically. |
| WORK-106 | WORK-105 accepted. | Artifact-ID and 14-field ledger validators reject every closed negative case. |
| WORK-107 | WORK-106 green and WORK-105 acceptance present. | 93 unique stable records, exact grouping/tombstone census, immutable payload/provenance and recovery proof. |
| WORK-108 | WORK-107 green and the full WORK-105 AD conversion accepted. | Every mandatory outer record has its exact unique ID and excluded surfaces have none. |
| WORK-109 | WORK-107/108 green. | Terminal document authority/routes active; Stage 04 absent and Stage 05 unchanged. |
| WORK-110 | WORK-109 green. | Agent-governance contracts and projections are complete without runtime promotion. |
| WORK-111 | Current 50-script inventory exact. | Complete reviewed semantic disposition ledger. |
| WORK-112 | WORK-111 accepted and wrapper consumers zero. | Only `validate-harness.sh` removed; exactly 49 scripts remain. |
| WORK-113 | Recovery target and consumer proofs green. | Progress recoverable and generated graph residue closed. |
| WORK-114 | Terminal consumers of transition assets zero. | Only the JSON/tool/external test retired as approved; exactly 47 scripts remain. |
| WORK-115 | All predecessor evidence green. | Independent VAL-WDTC-001..016 closure and PRD-0007 resumption handoff. |

## Verification Plan

| Work | Focused evidence | Aggregate/closure evidence |
| --- | --- | --- |
| WORK-100..101 | lifecycle/registry/link and baseline fixed-point checks | historical controller all-files PASS |
| WORK-102 | migration unit tests, route fixtures, `132/82/50` check | strict transition registry and aggregate PASS |
| WORK-103 | archive validation/cutover/recovery, prior-envelope byte diff | 93-record index and aggregate PASS |
| WORK-104 | exact source/target inventory, 41/41 siblings, three Stage 04 files, Markdown, links/owners | staged/affected/index/aggregate gates; controller all-files is separately owned |
| WORK-105 | eight-AD census, complete AD/API-Spec classifiers, atomic authority fixtures | strict transition/terminal document gates |
| WORK-106 | artifact-ID and ledger positive/negative fixtures | registry, lifecycle, archive, aggregate gates |
| WORK-107 | 93-to-93 ledger, old-envelope/payload/recovery checks | terminal archive and aggregate gates |
| WORK-108 | path-derived ID and global uniqueness fixtures | strict terminal registry/lifecycle gates |
| WORK-109 | authority-owner inventory, exact three-to-four-digit mapping, Incident route, and terminal negatives | Stage 04 absence, Stage 05/90/98 stability, aggregate gates |
| WORK-110 | harness/provider schema and semantic negatives | agent-governance and aggregate gates |
| WORK-111..112 | 50-row disposition, consumer parity, wrapper negatives | exact 49-script census and aggregate gates |
| WORK-113 | recovery and generated-output consumer/residue checks | terminal registry and aggregate gates |
| WORK-114 | transition-consumer/residue negatives | exact 47-script census, terminal bundle, controller all-files |
| WORK-115 | VAL-WDTC-001..016 evidence walk and independent reviews | lifecycle, aggregate, controller all-files, clean postflight |

All results are repository-static. Hosted CI, provider-runtime enforcement,
remote state, credentials, and live cluster behavior remain `DEFER` or outside
scope and are never inferred from these checks.

### Legacy Task verification evidence

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

Historical WORK-105 evidence records the former eight `docs/02.architecture/requirements/0004..0011` ARD paths.
records to `docs/02.architecture/descriptions/ad-0004..0011`, preserved the six
active and two accepted statuses, activated the AD route and Stage 99 PRD/SRS/IFC
and AD core forms, retired only the authored API Spec form while preserving
OpenAPI/GraphQL/Protobuf native surfaces, and accepted ADR-0024 as the current
PRD-0008/AD-0011/Spec-052 authority. Stage 90 and Stage 98 remain byte-immutable,
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

WORK-108 backfilled exactly 286 outer identities: 192 current authored records,
93 stable Stage 98 records, and `MIG-0001`. The registry requires
`artifact_id` only for the 18 mandatory source profiles and omits it from every
template and prohibited surface. Path-derived IDs and frontmatter agree,
declarations are globally unique, all eight Architecture Descriptions are
`AD-0004` through `AD-0011`, and Stage 98 embedded payload bytes remain opaque.
The finite lifecycle projection accepts only the exact WORK-107-to-WORK-108
outer-line insertion; malformed, duplicated, reordered, missing, or unrelated
body changes fail closed. Route state remains `transition` for WORK-109.

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
was performed or claimed. WORK-109 ownership transferred to Spec 0054
`WORK-054-002` and may proceed only while
the completed WORK-108 identity census, WORK-107 stable rehome, and WORK-105
accepted eight-AD authority gate remain green.
## Risks & Mitigations

| Risk | Owner | Mitigation |
| --- | --- | --- |
| Route cutover creates two active owners | Platform maintainer | Transition mapping rejects source+target coexistence and terminal mode lands only after all moves. |
| Archive generation changes historical bytes | Governance steward | Read Git blobs, append exact bytes, validate digest/link context, and diff prior envelopes for zero modifications. |
| Stage 05 is accidentally renumbered | Documentation reviewer | Explicit negative fixture and filesystem assertions reject `04.operations`. |
| Stable-date rule captures observations/incidents | Technical writer | Exceptions are closed profile routes with positive and negative fixtures. |
| Rule consolidation drops a policy | Governance steward | Source-to-owner rule inventory and zero-consumer search precede deletion. |
| Harness schema creates a false enforcement claim | Security reviewer | Separate design disposition from observed evidence; require provider identity and reject static-to-runtime promotion. |
| Orchestration cleanup removes a unique check | Quality engineer | Compare rule, input, exit, diagnostic, lane, consumer, and negative fixture; retain every distinct validator. |
| Progress rotation loses recovery | Governance steward | Exact Git-blob snapshot and recovery test pass before live ledger truncation. |
| One-time tooling becomes permanent legacy | Platform maintainer | WORK-114 deletes map, tool, and tool-only tests after permanent fixtures own terminal behavior. |
| Large changes hide regressions | Reviewer | One logical commit per task, fresh worker, two review stages, focused and aggregate gates. |

### Legacy Task approval and rollback boundaries

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
## Completion Criteria

- WORK-100 through WORK-104 and `WDTC-AMEND-001` retain their factual commit,
  manifest, archive, and move evidence.
- Terminal active forms use PRD/SRS/Interface Requirement, AD/ADR, and Stage 03
  sibling work units; no legacy ARD/RFC/authored API Spec or live Stage 04 route remains.
- Every mandatory outer artifact has one globally unique path-derived ID and
  every prohibited surface has none.
- The 93 current Stage 98 records have unique stable destinations, immutable
  payload/provenance, complete ledger evidence, and dual recovery.
- Stage 05 remains unchanged and no Release-family artifact exists.
- Stage 00, Stage 99, and the registry have disjoint authority; agent-system
  controls do not promote repository-static evidence to runtime evidence.
- The complete script ledger proves `50 -> 49 -> 47`, deleting only the three
  approved assets at their assigned gates without losing unique semantics.
- Progress history is recoverable, stale graph output is absent, and transition
  scaffolding has no remaining consumer or residue.
- VAL-WDTC-001 through VAL-WDTC-016 have durable evidence; Specs 047-051 remain
  unexecuted and receive a terminal resumption route.
- Focused, strict, staged, affected, aggregate, controller all-files, diff, and
  clean-tree postflight evidence pass at the lane that owns each result.

## Traceability

- **Program requirement**:
  [PRD-0008](../../01.requirements/0008-workspace-document-taxonomy-consolidation.md)
- **Architecture**:
  [AD-0011](../../02.architecture/descriptions/0011-document-taxonomy-consolidation-architecture.md)
- **Decision**:
  [ADR-0024](../../02.architecture/decisions/0024-terminal-artifact-identity-and-archive-layout.md)
- **Specification**:
  [Spec 052](spec.md)
- **Execution evidence**:
  [Task: Document Taxonomy Consolidation](README.md#task-records)

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-WDTC-001](spec.md#success-criteria--verification-plan) | WORK-104, WORK-109, WORK-114, WORK-115 | [WORK-104](tasks/tsk-0006-work-104.md), [WORK-109](tasks/tsk-0011-work-109.md), [WORK-114](tasks/tsk-0016-work-114.md), [WORK-115](tasks/tsk-0017-work-115.md) |
| [VAL-WDTC-002](spec.md#success-criteria--verification-plan) | WORK-109, WORK-115 | [WORK-109](tasks/tsk-0011-work-109.md), [WORK-115](tasks/tsk-0017-work-115.md) |
| [VAL-WDTC-003](spec.md#success-criteria--verification-plan) | WORK-107..109, WORK-115 | [WORK-107](tasks/tsk-0009-work-107.md), [WORK-108](tasks/tsk-0010-work-108.md), [WORK-109](tasks/tsk-0011-work-109.md), [WORK-115](tasks/tsk-0017-work-115.md) |
| [VAL-WDTC-004](spec.md#success-criteria--verification-plan) | WORK-105 | [WORK-105](tasks/tsk-0007-work-105.md) |
| [VAL-WDTC-005](spec.md#success-criteria--verification-plan) | WORK-109 | [WORK-109](tasks/tsk-0011-work-109.md) |
| [VAL-WDTC-006](spec.md#success-criteria--verification-plan) | WORK-102, WORK-103, WORK-106, WORK-107 | [WORK-102](tasks/tsk-0003-work-102.md), [WORK-103](tasks/tsk-0004-work-103.md), [WORK-106](tasks/tsk-0008-work-106.md), [WORK-107](tasks/tsk-0009-work-107.md) |
| [VAL-WDTC-007](spec.md#success-criteria--verification-plan) | WORK-111, WORK-112, WORK-114 | [WORK-111](tasks/tsk-0013-work-111.md), [WORK-112](tasks/tsk-0014-work-112.md), [WORK-114](tasks/tsk-0016-work-114.md) |
| [VAL-WDTC-008](spec.md#success-criteria--verification-plan) | WORK-110 | [WORK-110](tasks/tsk-0012-work-110.md) |
| [VAL-WDTC-009](spec.md#success-criteria--verification-plan) | WORK-113 | [WORK-113](tasks/tsk-0015-work-113.md) |
| [VAL-WDTC-010](spec.md#success-criteria--verification-plan) | WORK-101, WORK-114, WORK-115 | [WORK-101](tasks/tsk-0002-work-101.md), [WORK-114](tasks/tsk-0016-work-114.md), [WORK-115](tasks/tsk-0017-work-115.md) |
| [VAL-WDTC-011](spec.md#success-criteria--verification-plan) | WORK-115 | [WORK-115](tasks/tsk-0017-work-115.md) |
| [VAL-WDTC-012](spec.md#success-criteria--verification-plan) | All work | [WORK-100](tasks/tsk-0001-work-100.md), [WORK-101](tasks/tsk-0002-work-101.md), [WORK-102](tasks/tsk-0003-work-102.md), [WORK-103](tasks/tsk-0004-work-103.md), [WDTC-AMEND-001](tasks/tsk-0005-wdtc-amend-001.md), [WORK-104](tasks/tsk-0006-work-104.md), [WORK-105](tasks/tsk-0007-work-105.md), [WORK-106](tasks/tsk-0008-work-106.md), [WORK-107](tasks/tsk-0009-work-107.md), [WORK-108](tasks/tsk-0010-work-108.md), [WORK-109](tasks/tsk-0011-work-109.md), [WORK-110](tasks/tsk-0012-work-110.md), [WORK-111](tasks/tsk-0013-work-111.md), [WORK-112](tasks/tsk-0014-work-112.md), [WORK-113](tasks/tsk-0015-work-113.md), [WORK-114](tasks/tsk-0016-work-114.md), [WORK-115](tasks/tsk-0017-work-115.md) |
| [VAL-WDTC-013](spec.md#success-criteria--verification-plan) | WORK-105 | [WORK-105](tasks/tsk-0007-work-105.md) |
| [VAL-WDTC-014](spec.md#success-criteria--verification-plan) | WORK-106, WORK-108 | [WORK-106](tasks/tsk-0008-work-106.md), [WORK-108](tasks/tsk-0010-work-108.md) |
| [VAL-WDTC-015](spec.md#success-criteria--verification-plan) | WORK-106, WORK-107 | [WORK-106](tasks/tsk-0008-work-106.md), [WORK-107](tasks/tsk-0009-work-107.md) |
| [VAL-WDTC-016](spec.md#success-criteria--verification-plan) | WORK-111, WORK-112, WORK-114 | [WORK-111](tasks/tsk-0013-work-111.md), [WORK-112](tasks/tsk-0014-work-112.md), [WORK-114](tasks/tsk-0016-work-114.md) |

### Legacy Task traceability

#### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-100](plan.md#work-breakdown) | Complete. | ADR-0023 acceptance and PRD-0008 transition projection evidence in `dd8b3465`/`ba180eca`. |
| [WORK-101](plan.md#work-breakdown) | Complete. | Baseline repair `57ce3746` and controller all-files fixed point. |
| [WORK-102](plan.md#work-breakdown) | Complete. | Exact transition routes, manifest/tool hardening, and `132/82/50` checks. |
| [WORK-103](plan.md#work-breakdown) | Complete. | 50 added envelopes, 93-record index, immutable prior records, and recovery checks. |
| [WDTC-AMEND-001](plan.md#work-breakdown) | Complete. | Human-approved Spec 052/ADR-0024 design carried through `446e336a`. |
| [WORK-104](plan.md#work-breakdown) | Complete. | Exact 82 move, 41/41 siblings, three Stage 04 READMEs, repaired consumers, and strict focused gates. |
| [WORK-105](plan.md#work-breakdown) | Complete. | Exact eight-AD conversion, legacy ARD/authored API Spec retirement, ADR-0024 authority acceptance, native surface preservation, and strict focused gates passed. |
| [WORK-106](plan.md#work-breakdown) | Complete. | Closed path-derived/global identity and exact 14-field ledger validators; strict-cutover 37/37 and repository gates passed. |
| [WORK-107](plan.md#work-breakdown) | Complete. | Exact 93-to-93 stable rehome, 76/17 census, immutable payload/provenance, old-envelope recovery, and aggregate PASS. |
| [WORK-108](plan.md#work-breakdown) | Complete. | Exact 286 path-derived outer identities, global uniqueness, mandatory/prohibited profile parity, and finite lifecycle projection passed. |
| [WORK-109](plan.md#work-breakdown) | Transferred. | Spec 0054 `WORK-054-002` owns document authority and route convergence. |
| [WORK-110](plan.md#work-breakdown) | Transferred. | Spec 0054 `WORK-054-003` owns AI-agent governance convergence. |
| [WORK-111](plan.md#work-breakdown) | Transferred. | Spec 0054 `WORK-054-010` owns the exact 50-row script ledger. |
| [WORK-112](plan.md#work-breakdown) | Transferred. | Spec 0054 `WORK-054-011` owns wrapper retirement and the exact 49 count. |
| [WORK-113](plan.md#work-breakdown) | Transferred. | Spec 0054 `WORK-054-012` owns recoverable progress/graph cleanup. |
| [WORK-114](plan.md#work-breakdown) | Transferred. | Spec 0054 `WORK-054-013` owns transition retirement and the exact 47 count. |
| [WORK-115](plan.md#work-breakdown) | Transferred. | Spec 0054 `WORK-054-014` owns final closure and PRD-0007 handoff. |
