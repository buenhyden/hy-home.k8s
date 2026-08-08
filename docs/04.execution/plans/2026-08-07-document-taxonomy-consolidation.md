---
title: 'Document Taxonomy Consolidation Implementation Plan'
type: sdlc/plan
status: active
owner: platform
updated: 2026-08-09
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
  `docs/03.specs/<NNN>-<slug>/{spec.md,plan.md,tasks.md}`; `plan.md` is optional
  and `tasks.md` requires both siblings.
- `docs/04.execution/` is retired; its numeric slot remains unused.
- `docs/05.operations/` remains unchanged and continues to own guides,
  incidents, policies, and runbooks.
- Do not create a Release profile, template, folder, lifecycle, validator, or
  document.
- Mutable authored paths use stable identifiers or slugs. Dates remain in
  frontmatter; path dates are limited to Stage 90 observations/snapshots,
  actual Incident/Postmortem identity, and Stage 98 historical mirrors.
- Existing identifiers are immutable. ADR-0023 replaces ADR-0021 only as the
  machine decision associated with PRD-008/ARD-0011/Spec-052; ADR-0021 itself
  and its original program scope remain accepted and unchanged.
- Existing `docs/98.archive/**` envelopes and payloads are immutable. New
  records and the archive index may be appended in dedicated, registry-owned
  namespaces. The existing ARWB base 31-record and ACER additive 12-record
  sets remain exact immutable subsets; later WDTC records never change their
  expected counts or membership.
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

This plan executes [Spec 052](../../03.specs/052-document-taxonomy-consolidation/spec.md)
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
04 patterns. PRD-008/ARD-0011/Spec-052 currently names accepted ADR-0021 even
though ADR-0021 owns a different program. ADR-0023 is the human-approved
decision and is promoted through `draft -> active -> accepted`, never directly
from draft to accepted.

The raw pre-change all-files hook recorded three baseline issues: the registry
self-test could not allocate its configured temporary location, detect-secrets
found three unadjudicated non-secret values, and Markdown lint rejected the
Spec 053 Plan's H1-to-H3 jump. With `TMPDIR=/tmp`, every strict document lane
and the aggregate repository gate passes; the three all-files defects remain
explicit Task 2 work and are not terminal waivers.

## Goals & In-Scope

- Activate accepted ADR-0023 and correct the machine lineage atomically.
- Close the observed all-files baseline defects without suppressing scanners.
- Add tested legacy/transition/terminal route semantics.
- Commit a complete 132-document execution manifest before changing paths.
- Append ArchiveEnvelope records for the 50 unmatched execution documents.
- Move the 82 retained Plan/Task documents into their 41 Spec work units.
- Retire Stage 04 and prove Stage 05 stability and Release-family absence.
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

- Renumbering Stage 05 or any PRD, ARD, ADR, or Spec identifier.
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

| ID | Work package | Depends on | Entry gate | Exit evidence |
| --- | --- | --- | --- | --- |
| WDTC-100 | Accept ADR-0023 and correct PRD-008 machine lineage | Approved design and active ADR-0023 | Plan commit is green | Accepted ADR, registry/self-test projection on `0023`, staged lifecycle PASS |
| WDTC-101 | Repair the all-files baseline | WDTC-100 | Three findings reproduced | Exact false-positive adjudication, corrected heading, all-files PASS with `TMPDIR=/tmp` |
| WDTC-102 | Implement transition routes and the reviewed migration manifest/tool | WDTC-101 | Legacy registry green | RED/GREEN route fixtures, 132 unique source entries, dry-run PASS |
| WDTC-103 | Archive unmatched execution history | WDTC-102 | 50 archive entries reviewed | 50 added envelopes, index parity, immutable prior 43 records, source removal |
| WDTC-104 | Co-locate retained work units | WDTC-103 | 82 move entries and transition route green | 41 complete work units, reciprocal links green, only Stage 04 READMEs remain |
| WDTC-105 | Consolidate document authority and activate terminal taxonomy | WDTC-104 | Current consumers migrated | Three prose owners, updated forms, Stage 04 absent, Stage 05 stable, terminal route PASS |
| WDTC-106 | Activate agent-system governance controls atomically | WDTC-105 | Document authority green | Harness/provider contracts, closed schemas, negative fixtures, non-promotion PASS |
| WDTC-107 | Reconcile validation orchestration and retire the harness wrapper | WDTC-106 | Consumer graph captured | One pre-commit aggregate path, wrapper zero-consumer proof, distinct validators retained |
| WDTC-108 | Rotate memory and remove stale generated output | WDTC-107 | Recovery and consumer proofs | Recoverable progress snapshot, bounded live ledger, graph output removed/ignored |
| WDTC-109 | Remove temporary migration assets and prove terminal state | WDTC-108 | All migration consumers zero | No temporary map/tool, terminal residue zero, aggregate and all-files PASS |
| WDTC-110 | Independent review and lifecycle closure | WDTC-109 | Full terminal evidence green | Two-stage review, criterion evidence, Spec triad/PRD/ARD done, PRD-007 resumption handoff |

### File Structure and Interfaces

#### Temporary migration assets

- `scripts/document-taxonomy-migration.json` — temporary reviewed manifest;
  exactly 132 source documents, 82 `move-current` entries and 50
  `archive-unique` entries. While tracked it selects the temporary closed
  `native/document-migration-manifest` profile and `transition` lifecycle;
  terminal route state requires its absence. WDTC-109 deletes it and removes
  that temporary profile atomically.
- `scripts/migrate-document-work-units.py` — temporary fail-closed manifest
  validator and mover. WDTC-109 deletes it.
- `tests/test_migrate_document_work_units.py` — temporary tests retained until
  terminal behavior is incorporated into the registry fixtures, then deleted
  by WDTC-109.

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
both the route and the profile. WDTC-109 deletes the manifest, its schema
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

#### Task 1: WDTC-100 — accept ADR-0023 and correct machine lineage

**Files:**

- Modify: `docs/02.architecture/decisions/0023-work-unit-document-taxonomy-and-governance-authority.md`
- Modify: `docs/02.architecture/decisions/README.md`
- Modify: `docs/99.templates/support/document-profiles.json`
- Modify: `scripts/validate-document-contract-registry.py`
- Modify: `tests/fixtures/document-contracts/registry-cases.json`
- Modify: `docs/03.specs/052-document-taxonomy-consolidation/spec.md`
- Modify: `docs/04.execution/tasks/2026-08-07-document-taxonomy-consolidation.md`
- Modify: `docs/00.agent-governance/memory/progress.md`
- Modify: `scripts/validate-active-corpus-residue-closure.py`
- Modify: `tests/test_active_corpus_retention.py`
- Modify: `scripts/README.md`

**Interfaces:**

- Consumes: ADR-0023 `status: active` from the approved planning commit.
- Produces: accepted decision `0023` as the sole PRD-008 tranche decision.

**Approved atomic consumer amendment (2026-08-09):** accepting ADR-0023 adds
one new accepted ADR to the active-corpus residue-closure input. Update only
the closed post-closure ADR allowlist, its self-test and covering retention
test, and the script inventory wording to admit ADR-0023. The frozen accepted
ADR guard and exact `13/29` guard count remain unchanged; no other authority
path is admitted.

- [ ] **Step 1: Change the immutable projection expectation first**

Update `_assert_program_lineage_projection()` and its registry fixture so
PRD `008`, ARD `0011`, Spec `052` requires decision `0023`.

- [ ] **Step 2: Run the focused self-test and observe RED**

```bash
python3 scripts/validate-document-contract-registry.py --root . --self-test
```

Expected: FAIL naming the production PRD-008 decision projection, because the
registry still contains `0021`.

- [ ] **Step 3: Accept the ADR and update the registry atomically**

Set ADR-0023 to `status: accepted`; update its overview and the decisions index
to state that written design and implementation planning were reviewed. Change
only the PRD-008 tranche's `decision` from `0021` to `0023`. Preserve accepted
ADR-0021 and its original scope.

Update the approved active-corpus residue-closure consumer amendment in the
same work package so the new accepted ADR-0023 is the only added post-closure
authority path; retain the frozen `13/29` guard contract.

- [ ] **Step 4: Run lifecycle and registry GREEN checks**

```bash
python3 scripts/validate-document-lifecycle.py --root . --mode staged
python3 scripts/validate-document-contract-registry.py --root . --self-test
python3 scripts/validate-document-contract-registry.py --root . --mode strict
python3 scripts/validate-links-and-owners.py --root . --mode strict
python3 scripts/validate-active-corpus-residue-closure.py --root . --self-test
python3 scripts/validate-active-corpus-residue-closure.py --root .
python3 -m unittest tests/test_active_corpus_retention.py
```

Expected: lifecycle accepts `active -> accepted`; self-test and strict registry
report zero failures, zero uncovered paths, and zero ambiguous paths.

- [ ] **Step 5: Record evidence and commit**

```bash
git add docs/02.architecture/decisions/0023-work-unit-document-taxonomy-and-governance-authority.md docs/02.architecture/decisions/README.md docs/99.templates/support/document-profiles.json scripts/validate-document-contract-registry.py tests/fixtures/document-contracts/registry-cases.json docs/03.specs/052-document-taxonomy-consolidation/spec.md docs/04.execution/tasks/2026-08-07-document-taxonomy-consolidation.md docs/00.agent-governance/memory/progress.md scripts/validate-active-corpus-residue-closure.py tests/test_active_corpus_retention.py scripts/README.md
git commit -m "docs: accept the document taxonomy decision"
```

#### Task 2: WDTC-101 — repair the all-files baseline

**Files:**

- Modify: `docs/04.execution/plans/2026-08-08-workspace-engineering-research-pack-consolidation.md`
- Modify: `docs/90.references/research/2026-08-08-wer/source-coverage-and-migration-ledger.md`
- Modify: `.secrets.baseline`
- Modify: `docs/04.execution/tasks/2026-08-07-document-taxonomy-consolidation.md`
- Modify: `docs/00.agent-governance/memory/progress.md`

**Interfaces:**

- Consumes: the recorded three-finding baseline.
- Produces: a reproducible Linux/WSL all-files PASS without hook suppression.

- [ ] **Step 1: Reproduce the failures without retaining hook mutations**

```bash
TMPDIR=/tmp pre-commit run markdownlint-cli2 --all-files
TMPDIR=/tmp pre-commit run detect-secrets --all-files
git diff -- .secrets.baseline
```

Expected: Markdown reports the Spec 053 Plan's first `### Global Constraints`;
detect-secrets proposes only the two ledger keyword findings and one historical
hex finding already recorded in baseline evidence.

- [ ] **Step 2: Correct structure and adjudicate exact non-secrets**

Change the first `### Global Constraints` in the Spec 053 Plan to
`## Global Constraints`. Review the three scanner locations without printing
secret values, retain scanner behavior, and update only their exact
`.secrets.baseline` entries as `is_secret: false`.

- [ ] **Step 3: Run focused GREEN checks**

```bash
TMPDIR=/tmp pre-commit run markdownlint-cli2 --all-files
TMPDIR=/tmp pre-commit run detect-secrets --all-files
git diff --check
```

Expected: all three commands pass and `.secrets.baseline` has no unrelated
entry churn.

- [ ] **Step 4: Run the full all-files lane and commit**

```bash
TMPDIR=/tmp pre-commit run --all-files
git status --short
git diff
git diff --cached
git diff --check
git diff --cached --check
git add .secrets.baseline docs/04.execution/plans/2026-08-08-workspace-engineering-research-pack-consolidation.md docs/90.references/research/2026-08-08-wer/source-coverage-and-migration-ledger.md docs/04.execution/tasks/2026-08-07-document-taxonomy-consolidation.md docs/00.agent-governance/memory/progress.md
git commit -m "fix: close the repository validation baseline"
```

#### Task 3: WDTC-102 — implement transition routes and migration tooling

**Files:**

- Create: `scripts/document-taxonomy-migration.json`
- Create: `scripts/migrate-document-work-units.py`
- Create: `tests/test_migrate_document_work_units.py`
- Modify: `tests/README.md`
- Modify: `docs/90.references/data/README.md`
- Modify: `docs/99.templates/support/document-profiles.schema.json`
- Modify: `docs/99.templates/support/document-profiles.json`
- Modify: `scripts/document_contracts.py`
- Modify: `scripts/validate-document-contract-registry.py`
- Modify: `scripts/validate-active-corpus-role-audit.py`
- Modify: `tests/fixtures/document-contracts/registry-cases.json`
- Modify: `tests/fixtures/markdown-profiles.json`
- Modify: `tests/test_active_corpus_role_audit.py`
- Modify: `tests/test_document_strict_cutover.py`

**Interfaces:**

- Consumes: green legacy routes and design-baseline tracked inventory.
- Produces: explicit route-state selection and a fully enumerated manifest.

The Spec-052 Plan and Task are themselves manifest-controlled move sources.
After this task pins their WDTC-101 blobs, WDTC-102 and WDTC-103 record
intermediate evidence only in `docs/00.agent-governance/memory/progress.md` and
must not edit either source. WDTC-104 first validates and moves those exact
blobs, then may update the destination `tasks.md` and `plan.md`.

- [ ] **Step 1: Write route and manifest negative tests**

Add cases for: Stage 03 sibling Plan/Task acceptance in transition; Stage 04
rejection in terminal; target Plan without Spec; target Task without Plan;
source/target duplicate active ownership; missing source; changed source blob;
duplicate source; duplicate target; existing target; archive endpoint under an
existing envelope; unknown disposition; and manifest totals other than
`132/82/50`. Add an ACER role-audit case proving that the exact temporary path
`tests/test_migrate_document_work_units.py` is admitted as
`python/regression-test`, is present in the tests README inventory, and that a
second unregistered migration helper still fails closed.

```python
def test_task_requires_spec_and_plan(self):
    diagnostics = validate_work_unit_paths({"052": {"tasks.md", "spec.md"}})
    self.assertEqual(diagnostics, ("WORK-UNIT-MISSING-PLAN:052",))

def test_manifest_totals_are_closed(self):
    with self.assertRaises(MigrationAbort):
        validate_counts(move_count=81, archive_count=50, source_count=131)
```

- [ ] **Step 2: Run the new tests and observe RED**

```bash
python3 -m unittest tests/test_migrate_document_work_units.py -v
python3 scripts/validate-document-contract-registry.py --root . --mode strict --route-state transition
```

Expected: import/argument failures because the tool and route-state interface
do not exist.

- [ ] **Step 3: Implement the closed route state**

Add registry `routeState` enum `legacy|transition|terminal` and transition entry
shape with `source`, `target`, `workUnit`, `disposition`, `sourceBlob`, and
`reviewed`. Add `--route-state` to the registry CLI. Transition routes admit
both Stage 04 dated paths and Stage 03 siblings but reject two active owners;
terminal routes admit only Stage 03 siblings. Add the closed
`native/document-migration-manifest` profile and schema projection with exact
path `scripts/document-taxonomy-migration.json`, native JSON canonical form,
top-level `state: "transition"`, and no additional properties. Add fixtures
that reject the manifest in terminal state, reject any other path selecting
the profile, and reject any lifecycle value other than `transition`. Add the
registry-owned retired-route token `docs/04.execution` with a closed allowlist
of immutable Stage 90/98 evidence profiles. In terminal mode the registry CLI
scans tracked text, classifies every token hit, and fails on mutable,
executable, contract, fixture, navigation, or unclassified consumers.

Atomically add `tests/test_migrate_document_work_units.py` to the current
ACER role-audit post-closure helper manifest and `tests/README.md`. Do not alter
the frozen 33-helper ledger. Mark this one exact admission as transition-only
in code/tests, and require WDTC-109 to remove the test, README row, admission,
and its temporary role-audit test together. During transition, update
`docs/90.references/data/README.md` to state the exact current partition as 42
helpers (`33` frozen plus `9` admitted); WDTC-109 restores the terminal 41
(`33 + 8`) statement. The aggregate must remain green throughout.

- [ ] **Step 4: Build the exact manifest**

Enumerate every authored Stage 04 Plan and Task from `git ls-files`, derive the
41 same-slug triads only when the target Spec exists, and require human-readable
exception entries for non-identical names. Store the source blob by running
`git rev-parse "HEAD:${source}"` inside the manifest builder. Mark all 82 triad documents `move-current` and all
50 unmatched documents `archive-unique`. Include no README in these totals.

The manifest schema requires `state` to equal `transition`, and requires
`sourceCommit` and every `sourceBlob` to match `^[0-9a-f]{40}$`. The first
reviewed entry is the exact Spec-052 Plan mapping:

```json
{
  "source": "docs/04.execution/plans/2026-08-07-document-taxonomy-consolidation.md",
  "target": "docs/03.specs/052-document-taxonomy-consolidation/plan.md",
  "workUnit": "Spec-052",
  "disposition": "move-current",
  "reviewed": true
}
```

The builder adds the exact observed `sourceBlob` to that entry and writes the
exact WDTC-101 commit as top-level `sourceCommit`; validation rejects a missing
or non-hex value.

- [ ] **Step 5: Run GREEN and dry-run checks**

```bash
python3 -m unittest tests/test_migrate_document_work_units.py -v
python3 scripts/migrate-document-work-units.py --root . --manifest scripts/document-taxonomy-migration.json --check
python3 scripts/validate-document-contract-registry.py --root . --self-test
python3 scripts/validate-document-contract-registry.py --root . --mode strict --route-state transition
python3 scripts/validate-markdown-profiles.py --root . --mode strict
bash scripts/validate-repo-quality-gates.sh .
```

Expected: all pass; the dry run reports exactly 82 moves and 50 archives.

- [ ] **Step 6: Commit**

```bash
git add scripts/document-taxonomy-migration.json scripts/migrate-document-work-units.py tests/test_migrate_document_work_units.py tests/README.md docs/90.references/data/README.md docs/99.templates/support/document-profiles.schema.json docs/99.templates/support/document-profiles.json scripts/document_contracts.py scripts/validate-document-contract-registry.py scripts/validate-active-corpus-role-audit.py tests/fixtures/document-contracts/registry-cases.json tests/fixtures/markdown-profiles.json tests/test_active_corpus_role_audit.py tests/test_document_strict_cutover.py docs/00.agent-governance/memory/progress.md
git commit -m "feat: add fail-closed document route transition"
```

#### Task 4: WDTC-103 — archive unmatched execution history

**Files:**

- Create: 50 manifest-named records under `docs/98.archive/04.execution/{plans,tasks}/`
- Modify: `docs/98.archive/README.md`
- Modify: `scripts/archive_validation.py`
- Modify: `scripts/archive_cutover.py`
- Modify: `scripts/archive_recovery.py`
- Modify: `docs/99.templates/support/document-profiles.schema.json`
- Modify: `docs/99.templates/support/document-profiles.json`
- Modify: `scripts/validate-active-corpus-migrations.py`
- Modify: `docs/90.references/data/active-corpus-migration-results.json`
- Modify: `tests/test_archive_validation.py`
- Modify: `tests/test_archive_cutover.py`
- Modify: `tests/test_archive_recovery.py`
- Modify: `tests/test_document_lifecycle_archive_cutover.py`
- Modify: `tests/test_active_corpus_migrations.py`
- Delete: the 50 `archive-unique` source paths named by the manifest
- Modify: `docs/04.execution/{plans,tasks}/README.md`
- Modify: `docs/00.agent-governance/memory/progress.md`

**Interfaces:**

- Consumes: reviewed archive entries and immutable source blobs.
- Produces: 93 total ArchiveEnvelope records with the prior ARWB 31 and ACER
  additive 12 exact sets byte-identical and membership-identical.

- [ ] **Step 1: Add failing additive-archive tests**

Add the version-2 namespace registry and failing tests before generating a new
record. Test generic repository scanning, README/index parity, source
blob/digest, historical-link resolution, allowed `completed-lineage` null
replacement, duplicate original owner rejection, existing-envelope mutation
rejection, secret-classifier failure without payload echo, and exact namespace
counts `31`, `12`, `50`, `0` with repository aggregate `93`. Test that the ACER
validator still owns exactly its original 43 records while accepting only
registry-declared non-ACER namespaces. Test recovery `--verify`, output-path
confinement, overwrite refusal, and exact recovered bytes.

- [ ] **Step 2: Run archive tests and observe RED**

```bash
python3 -m unittest tests/test_archive_validation.py tests/test_archive_cutover.py tests/test_archive_recovery.py tests/test_document_lifecycle_archive_cutover.py -v
```

Expected: count/index parity failures because the additive records do not yet
exist.

- [ ] **Step 3: Implement the versioned generic archive boundary**

Add `archiveContractVersion: 2` and the four closed namespace definitions to
the registry. Implement
`archive_validation.validate_repository_archive(root, registry)` and make
`archive_cutover.py --root .` invoke it without replacing the fixed historical
cutover checks. Extend the active-corpus result/fixture contract so ARWB and
ACER remain exact immutable subsets and the repository total is reported
separately. Parse the README archive index and require exact parity with all
discovered envelopes and namespace membership. Implement read-only recovery
verification and confined non-overwriting temporary output.

- [ ] **Step 4: Generate exact envelopes and remove sources**

For each manifest archive entry, read bytes with
`git cat-file blob "${source_commit}:${source}"`, run the existing fail-closed secret
classifier, calculate SHA-256 and historical rendered-link count, append an
ArchiveEnvelope header plus exact blob bytes at the mirrored Stage 98 target,
and add one archive-index row. After every record validates, remove its live
source. Route current consumers to the named current successor or to the
archive index, never directly to an individual archive record. Do not change
any of the prior 43 envelopes. Assign all 50 records only to
`wdtc-execution`; do not reuse ARWB or ACER membership.

- [ ] **Step 5: Validate archive integrity and immutable history**

```bash
python3 -m unittest tests/test_archive_validation.py tests/test_archive_cutover.py tests/test_archive_recovery.py tests/test_document_lifecycle_archive_cutover.py -v
python3 -m unittest tests/test_active_corpus_migrations.py -v
python3 scripts/archive_cutover.py --root .
python3 scripts/archive_recovery.py --root . --record docs/98.archive/04.execution/plans/2026-05-10-agent-first-harness-llm-wiki-hooks.md --verify
git diff --name-status HEAD -- docs/98.archive
```

Expected: archive validation passes; the diff contains 50 added envelopes and
one modified README, with no modification or deletion of an existing envelope.

- [ ] **Step 6: Run aggregate checks and commit**

```bash
python3 scripts/migrate-document-work-units.py --root . --manifest scripts/document-taxonomy-migration.json --check
bash scripts/validate-repo-quality-gates.sh .
git add docs/98.archive docs/04.execution docs/90.references/data/active-corpus-migration-results.json docs/99.templates/support/document-profiles.schema.json docs/99.templates/support/document-profiles.json scripts/archive_validation.py scripts/archive_cutover.py scripts/archive_recovery.py scripts/validate-active-corpus-migrations.py tests/test_archive_validation.py tests/test_archive_cutover.py tests/test_archive_recovery.py tests/test_document_lifecycle_archive_cutover.py tests/test_active_corpus_migrations.py docs/00.agent-governance/memory/progress.md
git commit -m "docs: archive unmatched execution history"
```

#### Task 5: WDTC-104 — co-locate the 41 retained work units

**Files:**

- Move: the 82 manifest `move-current` sources to sibling `plan.md`/`tasks.md`
- Modify: all moved Plan/Task relative links
- Modify: the 41 sibling `spec.md` traceability sections when they link Stage 04
- Modify: `docs/03.specs/README.md`
- Modify: `docs/04.execution/README.md`
- Modify: `docs/04.execution/{plans,tasks}/README.md`
- Modify: `docs/99.templates/support/document-profiles.json`
- Modify: `tests/fixtures/links-and-owners.json`
- Modify: `tests/fixtures/markdown-profiles.json`
- Modify: `docs/00.agent-governance/memory/progress.md`

**Interfaces:**

- Consumes: transition routes and 82 exact move entries.
- Produces: 41 complete Stage 03 work units; only three Stage 04 READMEs remain.

- [ ] **Step 1: Prove the move preconditions**

```bash
python3 scripts/migrate-document-work-units.py --root . --manifest scripts/document-taxonomy-migration.json --check
git status --short
```

Expected: all source blobs match, all targets are absent, archive phase is
closed, and the tree is clean.

- [ ] **Step 2: Apply only the move phase**

```bash
python3 scripts/migrate-document-work-units.py --root . --manifest scripts/document-taxonomy-migration.json --phase move --apply
```

Expected: 82 Git moves, no archive path write, no Stage 05 path change.

- [ ] **Step 3: Rewrite current consumers from the exact manifest**

Rewrite current Markdown and machine-contract links to each final sibling
target. Change Spec 053's `standaloneExecutions` Plan/Task values to its sibling
paths. Recalculate relative links from each final file. Do not rewrite Stage 90
observation bodies or Stage 98 payloads; classify their old path text as
historical evidence.

- [ ] **Step 4: Validate locality and reciprocal links**

```bash
test "$(find docs/03.specs -mindepth 2 -maxdepth 2 -name plan.md | wc -l)" -eq 41
test "$(find docs/03.specs -mindepth 2 -maxdepth 2 -name tasks.md | wc -l)" -eq 41
test "$(find docs/04.execution -type f | wc -l)" -eq 3
python3 scripts/validate-markdown-profiles.py --root . --mode strict
python3 scripts/validate-links-and-owners.py --root . --mode strict
python3 scripts/validate-document-contract-registry.py --root . --mode strict --route-state transition
```

Expected: all checks pass with zero incomplete work units and zero broken
current links.

- [ ] **Step 5: Commit**

```bash
git add -A docs/03.specs docs/04.execution docs/99.templates/support/document-profiles.json tests/fixtures/links-and-owners.json tests/fixtures/markdown-profiles.json docs/00.agent-governance/memory/progress.md
git commit -m "docs: co-locate execution records with their specs"
```

From this commit onward the active evidence paths are
`docs/03.specs/052-document-taxonomy-consolidation/{plan.md,tasks.md}`.

#### Task 6: WDTC-105 — consolidate document authority and activate terminal taxonomy

**Files:**

- Create by `git mv`: `docs/00.agent-governance/rules/document-authoring.md`
- Delete after merge: `docs/00.agent-governance/rules/document-stage-routing.md`
- Delete after merge: `docs/00.agent-governance/rules/stage-authoring-matrix.md`
- Delete after merge: `docs/00.agent-governance/rules/stage-checklists.md`
- Create by `git mv`: `docs/99.templates/support/document-contract.md`
- Create by `git mv`: `docs/99.templates/support/document-lifecycle.md`
- Delete after merge: `docs/99.templates/support/template-routing.md`
- Delete after merge: `docs/99.templates/support/frontmatter-schema.md`
- Delete after merge: `docs/99.templates/support/common-documentation-governance.md`
- Delete after merge: `docs/99.templates/support/legacy-cleanup-rules.md`
- Modify: `docs/99.templates/templates/sdlc/execution/plan.template.md`
- Modify: `docs/99.templates/templates/sdlc/execution/task.template.md`
- Modify: `docs/99.templates/support/document-profiles.json`
- Modify: `docs/99.templates/support/document-profiles.schema.json`
- Modify: `docs/99.templates/support/README.md`
- Modify: `docs/00.agent-governance/rules/{bootstrap,preflight-checklist,postflight-checklist,quality-standards}.md`
- Modify: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.agents/GEMINI.md`, `.claude/CLAUDE.md`, `.codex/CODEX.md`
- Modify: `docs/00.agent-governance/providers/{agents-md,claude,codex,gemini}.md`
- Modify: each additional current consumer returned by `rg -l "document-stage-routing|stage-authoring-matrix|stage-checklists|documentation-protocol|documentation-contract|template-routing|frontmatter-schema|common-documentation-governance|sdlc-governance|legacy-cleanup-rules" . --glob '!docs/98.archive/**' --glob '!docs/90.references/**'`
- Delete: `docs/04.execution/README.md`
- Delete: `docs/04.execution/plans/README.md`
- Delete: `docs/04.execution/tasks/README.md`
- Modify: `docs/README.md`, `README.md`, `docs/03.specs/README.md`, `docs/05.operations/README.md`
- Modify: `tests/fixtures/document-contracts/template-source-parity.json`
- Modify: `tests/fixtures/document-contracts/template-compatibility.json`
- Modify: document registry/Markdown/link fixtures and strict-cutover/archive-lifecycle tests
- Modify: `docs/03.specs/052-document-taxonomy-consolidation/{plan.md,tasks.md}`

**Interfaces:**

- Consumes: complete Stage 03 work units and transition registry.
- Produces: terminal route contract and three non-overlapping prose owners.

- [ ] **Step 1: Write terminal and rule-uniqueness negative fixtures**

Add failures for: any live Stage 04 file; any current mutable link to Stage 04;
Plan without sibling Spec; Task without sibling Plan; date-prefixed mutable
PRD/ARD/ADR/Spec/Plan/Task/Guide/Policy/Runbook; Stage 05 renumber; Release
profile/template/path; duplicate normative machine values in Stage 00/99; a
physical form with zero or two authored owners; and template-form lifecycle
being treated as an authored-document transition.

- [ ] **Step 2: Run fixtures and observe RED**

```bash
python3 scripts/validate-document-contract-registry.py --root . --self-test
python3 scripts/validate-document-contract-registry.py --root . --mode strict --route-state terminal
```

Expected: terminal validation fails while the transition route and Stage 04
README files still exist.

- [ ] **Step 3: Consolidate Stage 00 and Stage 99**

Move `documentation-protocol.md` to `document-authoring.md` and merge the three
other Stage 00 authoring-rule bodies section-by-section. Move
`documentation-contract.md` to `document-contract.md` and
`sdlc-governance.md` to `document-lifecycle.md`; merge the four remaining
support documents. For each source rule, retain exactly one target statement,
route literal machine values to the registry, update consumers, then delete the
source only when `rg` reports zero current links.

- [ ] **Step 4: Update forms and terminal routes**

Plan/Task templates require sibling links and date-free final filenames. Set
registry `routeState` to `terminal`, remove Stage 04 routes and transition
entries, retain only sibling Plan/Task regexes, and register date exceptions
only for Stage 90 observations/snapshots, actual Incident/Postmortem identity,
and Stage 98 mirrors. Replace the 26 `template/*` mirror profiles with one
typed `templateForm` relation on each authored/native owner; template forms
inherit frontmatter, heading, and value constraints but do not participate in
authored lifecycle transitions. Update the 11 template parity cases and the
30-form inventory assertions. Delete the three Stage 04 READMEs.

- [ ] **Step 5: Prove Stage 05 stability and Release absence**

```bash
test ! -e docs/04.execution
test -d docs/05.operations/guides
test -d docs/05.operations/incidents
test -d docs/05.operations/policies
test -d docs/05.operations/runbooks
test ! -e docs/04.operations
test ! -e docs/05.operations/releases
```

Expected: every test exits zero.

- [ ] **Step 6: Run strict GREEN checks and commit**

```bash
python3 scripts/validate-document-contract-registry.py --root . --self-test
python3 scripts/validate-document-contract-registry.py --root . --mode strict --route-state terminal
python3 scripts/validate-markdown-profiles.py --root . --mode strict
python3 scripts/validate-links-and-owners.py --root . --mode strict
bash scripts/validate-repo-quality-gates.sh .
git add -A
git commit -m "refactor: consolidate document governance authority"
```

#### Task 7: WDTC-106 — activate agent-system governance controls atomically

**Files:**

- Modify: `docs/00.agent-governance/rules/approval-boundaries.md`
- Modify: `docs/00.agent-governance/contracts/harness-contract.json`
- Modify: `docs/00.agent-governance/contracts/harness-contract.schema.json`
- Modify: `docs/00.agent-governance/contracts/provider-runtime-evidence.json`
- Modify: `docs/00.agent-governance/contracts/provider-runtime-evidence.schema.json`
- Modify: `docs/00.agent-governance/contracts/validation-surfaces.json`
- Modify: `scripts/validate-agent-harness-contract.py`
- Modify: `scripts/validate-agent-harness-semantics.py`
- Modify: `scripts/validate-agent-provider-evidence.py`
- Modify: `scripts/validate-agent-provider-config.py`
- Modify: `scripts/validate-agent-provider-canaries.py`
- Modify: `tests/fixtures/agent-harness-contract.json`
- Modify: `tests/fixtures/agent-provider-runtime-evidence.json`
- Modify: `tests/test_validate_agent_harness_contract.py`
- Modify: `tests/test_validate_agent_provider_config.py`
- Modify: `tests/test_validate_agent_provider_canaries.py`
- Modify: harness/roster/evaluation/model consumers that pin contract `1.0.0`
- Modify: `docs/00.agent-governance/{harness-catalog,harness-implementation-map}.md`
- Modify: `docs/00.agent-governance/providers/{agents-md,claude,codex,gemini}.md`
- Modify: `docs/03.specs/052-document-taxonomy-consolidation/tasks.md`

**Interfaces:**

- Consumes: existing roles, surfaces, permission classes, evidence classes, and
  evaluation IDs by reference.
- Produces: harness schema version `2`, contract version `1.1.0`, and provider
  reference evidence that remains `DEFER` without observed identity.

- [ ] **Step 1: Add closed negative fixtures first**

Cover unknown/duplicate owner policy, missing canonical owner, mutable Git ref,
invalid append principal, self-asserted approver, policy/action/principal/scope/
target/arguments/expiry/result mismatch, untrusted input without isolation,
high-risk trace unavailable without bounded Runbook exception, missing risk
owner/prohibited use/stop condition/evaluation/component digest, raw sensitive
body, static-to-runtime promotion, and provider evidence without matching
observed identity.

- [ ] **Step 2: Run focused tests and observe RED**

```bash
python3 -m unittest tests/test_validate_agent_harness_contract.py tests/test_validate_agent_provider_config.py tests/test_validate_agent_provider_canaries.py -v
```

Expected: new schema fields and semantic rule IDs are absent.

- [ ] **Step 3: Extend the two contracts and schemas**

Add closed `agentSystems`, `evidenceOwnerPolicies`, and
`approvalBoundaryProjection` sections. Each action approval requires
`approvalPolicyRef`, `actionClass`, `approvalId`, `actionFingerprint`,
`requesterPrincipal`, `approverPrincipal`, redacted target metadata/digest,
`argumentsDigest`, `authorityScope`, `issuedAt`, `expiresAt`, `decision`,
`approvalEvidenceRef`, and `resultEvidenceRef`. Evidence owner policies require
owner type/ref, append principal class, immutability, retention, validator,
trust anchor, and approval-boundary ref. Provider evidence stores references
and observed identity only, never raw bodies.

- [ ] **Step 4: Implement semantic rejection and non-promotion**

Use existing validators and the sensitive-payload scanner. A well-shaped record
without provider identity is `DEFER`; mismatched policy, principal, fingerprint,
scope, digest, expiry, result, owner, or trust anchor is rejected. Static schema
PASS cannot set provider enforcement PASS.

- [ ] **Step 5: Update all version pins atomically and run GREEN**

```bash
python3 scripts/validate-agent-harness-contract.py --root . --self-test
python3 scripts/validate-agent-harness-contract.py --root .
python3 scripts/validate-agent-harness-semantics.py --root . --self-test
python3 scripts/validate-agent-harness-semantics.py --root .
python3 scripts/validate-agent-provider-evidence.py --root . --self-test
python3 scripts/validate-agent-provider-evidence.py --root .
python3 -m unittest tests/test_validate_agent_harness_contract.py tests/test_validate_agent_provider_config.py tests/test_validate_agent_provider_canaries.py -v
bash scripts/validate-repo-quality-gates.sh .
```

Expected: schema and semantic tests pass; runtime enforcement and actual action
evidence remain explicitly `DEFER`.

- [ ] **Step 6: Commit**

```bash
git add docs/00.agent-governance scripts tests docs/03.specs/052-document-taxonomy-consolidation/tasks.md
git commit -m "feat: govern agent-system risk and approval evidence"
```

#### Task 8: WDTC-107 — reconcile orchestration and retire the harness wrapper

**Files:**

- Modify: `.pre-commit-config.yaml`
- Modify: `.github/PULL_REQUEST_TEMPLATE.md`
- Modify: `README.md`
- Modify: `scripts/README.md`
- Modify: `scripts/validate-repo-quality-gates.sh`
- Delete: `scripts/validate-harness.sh`
- Modify: `docs/00.agent-governance/contracts/agent-governance-ci.json`
- Modify: `docs/00.agent-governance/contracts/agent-governance-ci.schema.json`
- Modify: `docs/00.agent-governance/contracts/validation-surfaces.json`
- Modify: `scripts/validate-agent-governance-ci.py`
- Modify: `scripts/validate-affected-surfaces.py`
- Modify: `tests/fixtures/agent-governance-ci.json`
- Modify: `tests/fixtures/validation-surfaces.json`
- Modify: `tests/test_validate_agent_governance_ci.py`
- Modify: `tests/test_run_validation_lane.py`
- Modify: current work-unit references to `validate-harness.sh`
- Modify: `docs/03.specs/052-document-taxonomy-consolidation/tasks.md`

**Interfaces:**

- Consumes: the terminal path and final harness contract.
- Produces: one declared pre-commit aggregate execution path and an explicit
  retain-contract disposition for distinct validator families.

- [ ] **Step 1: Add orchestration topology tests**

Require the local pre-commit governance section to contain only the strict
repository-quality aggregate hook; require that aggregate to execute governance
CI self-test/production, legacy cutover self-test/production, governance
closure self-test/production, and affected-surface self-test/production exactly
once. Require every executable validator to be selected by
`validation-surfaces.json` or declared `library/manual`.

- [ ] **Step 2: Run tests and observe RED**

```bash
python3 -m unittest tests/test_validate_agent_governance_ci.py tests/test_run_validation_lane.py -v
python3 scripts/validate-affected-surfaces.py --root . --self-test
```

Expected: old duplicate pre-commit topology violates the new exact sequence.

- [ ] **Step 3: Consolidate orchestration and retire the wrapper**

Add governance-closure self-test/production to the aggregate, then remove all
seven redundant local governance hooks after their exact commands are owned by
that aggregate. Replace executable README/PR-template/current-work-unit
uses of `validate-harness.sh` with the aggregate plus separately named GitOps/
manifest/security lanes where required. Annotate immutable historical command
evidence rather than rewriting its claim. Delete `validate-harness.sh` only
after classifying every tracked-tree hit, including tests, fixtures, adapters,
root configuration, current documents, and historical records, and proving
zero live executable or contract consumer. Update
`tests/fixtures/validation-surfaces.json` and any other fixture whose command
surface changes; historical hits remain explicitly classified rather than
silently excluded.

- [ ] **Step 4: Record validator dispositions**

Retain registry, Markdown, links/owners, archive, security, CI, harness
semantics, lifecycle, and all five active-corpus validators because the audit
found distinct contracts or fixtures. Mark both `document_lifecycle.py` and
`validate-document-lifecycle.py` as `manual/historical`; do not delete them.

- [ ] **Step 5: Run GREEN checks and commit**

```bash
python3 scripts/validate-agent-governance-ci.py --root . --self-test
python3 scripts/validate-agent-governance-ci.py --root .
python3 scripts/validate-affected-surfaces.py --root . --self-test
python3 scripts/validate-affected-surfaces.py --root .
git grep -n -F 'scripts/validate-harness.sh' -- .
bash scripts/validate-repo-quality-gates.sh .
TMPDIR=/tmp pre-commit run --all-files
git status --short
git diff
git diff --cached
git diff --check
git diff --cached --check
git add -A
git commit -m "refactor: consolidate repository validation orchestration"
```

Expected: the search returns only explicitly annotated historical evidence, no
executable consumer; all gates pass.

#### Task 9: WDTC-108 — rotate memory and remove stale generated output

**Files:**

- Create: one progress snapshot ArchiveEnvelope under
  `docs/98.archive/00.agent-governance/memory/progress/`
- Modify: `docs/98.archive/README.md`
- Modify: `docs/00.agent-governance/memory/progress.md`
- Modify: `scripts/archive_validation.py`
- Modify: `scripts/archive_cutover.py`
- Modify: `scripts/archive_recovery.py`
- Modify: `tests/test_archive_validation.py`
- Modify: `tests/test_archive_cutover.py`
- Modify: `tests/test_archive_recovery.py`
- Delete: nine tracked files under `graphify-out/**`
- Modify: `.gitignore`
- Modify: `README.md`
- Modify: `.codex/CODEX.md`
- Modify: `docs/00.agent-governance/harness-catalog.md`
- Modify: `docs/99.templates/support/document-profiles.json`
- Modify: `docs/00.agent-governance/contracts/validation-surfaces.json`
- Modify: `tests/fixtures/validation-surfaces.json`
- Modify: `docs/03.specs/052-document-taxonomy-consolidation/tasks.md`

**Interfaces:**

- Consumes: terminal document contract and generic ArchiveEnvelope validation.
- Produces: one source-commit/blob-bound progress snapshot and a live ledger
  containing entries from 2026-08-01 onward plus the current WDTC entries.

- [ ] **Step 1: Add recovery and generated-residue tests**

Test progress snapshot target identity, duplicate snapshot source-blob
rejection, exact payload recovery, current ledger header/body validity, ignored
`graphify-out/`, absent tracked graph files, and no active consumer requiring
`GRAPH_REPORT.md`.

- [ ] **Step 2: Run tests and observe RED**

```bash
python3 -m unittest tests/test_archive_validation.py tests/test_archive_recovery.py -v
git ls-files graphify-out
```

Expected: graph paths are listed and progress snapshot behavior is absent.

- [ ] **Step 3: Archive and rotate progress**

Create a dated Stage 98 progress snapshot whose payload is the exact pre-rotation
Git blob. Permit repeated future snapshots by unique source blob and snapshot
path while rejecting duplicate blob identity. Verify recovery before replacing
the live ledger with its header plus entries dated 2026-08-01 or later and the
current WDTC entries.

- [ ] **Step 4: Remove generated graph ownership**

Run `git grep -n -E 'graphify-out|GRAPH_REPORT' -- .` and classify every hit
across `.agents/**`, provider adapters, hooks, runtime/catalog documents,
registry routes, validation surfaces, tests, and fixtures as current reader,
generator, contract, or historical evidence. Update or retire every current
reader/generator/contract first. Then delete the nine tracked files, add
`/graphify-out/` to `.gitignore`, remove its document profile and
validation-surface fixture, and update runtime/catalog prose so absence is the
normal state. Historical evidence is not rewritten.

- [ ] **Step 5: Run GREEN and commit**

```bash
python3 -m unittest tests/test_archive_validation.py tests/test_archive_recovery.py -v
python3 scripts/archive_cutover.py --root .
test -z "$(git ls-files graphify-out)"
git check-ignore graphify-out/probe.json
python3 scripts/validate-document-contract-registry.py --root . --mode strict --route-state terminal
bash scripts/validate-repo-quality-gates.sh .
TMPDIR=/tmp pre-commit run --all-files
git status --short
git diff
git diff --cached
git diff --check
git diff --cached --check
git add -A
git commit -m "chore: rotate memory and remove stale graph output"
```

#### Task 10: WDTC-109 — remove temporary migration assets and prove terminal state

**Files:**

- Delete: `scripts/document-taxonomy-migration.json`
- Delete: `scripts/migrate-document-work-units.py`
- Delete: `tests/test_migrate_document_work_units.py`
- Modify: `tests/README.md`
- Modify: `docs/90.references/data/README.md`
- Modify: registry fixtures to retain terminal negative cases without the tool
- Modify: `docs/99.templates/support/document-profiles.schema.json`
- Modify: `docs/99.templates/support/document-profiles.json`
- Modify: `scripts/document_contracts.py`
- Modify: `scripts/validate-document-contract-registry.py`
- Modify: `scripts/validate-active-corpus-role-audit.py`
- Modify: `tests/fixtures/document-contracts/registry-cases.json`
- Modify: `tests/test_active_corpus_role_audit.py`
- Modify: `scripts/README.md`
- Modify: `docs/03.specs/052-document-taxonomy-consolidation/tasks.md`
- Modify: `docs/00.agent-governance/memory/progress.md`

**Interfaces:**

- Consumes: completed migration and permanent terminal registry tests.
- Produces: zero one-time migration assets and complete terminal evidence.

- [ ] **Step 1: Port permanent behavior into registry fixtures**

Retain negative cases for Stage 04, incomplete work units, duplicate ownership,
date exceptions, Stage 05 renumber, and Release-family creation in the existing
registry/Markdown/link fixtures. Add a terminal-state fixture proving that the
temporary manifest path and `native/document-migration-manifest` profile are
both absent and rejected. Add three `retiredAssetTokens` for
`document-taxonomy-migration.json`, `migrate-document-work-units.py`, and
`test_migrate_document_work_units.py`. The terminal registry scan classifies
every tracked-text hit using the same closed current-consumer versus immutable
historical/current-evidence boundary as retired routes and fails on executable,
contract, test, fixture, navigation, or unclassified consumers. The temporary
tool-specific dirty-tree and source-blob tests may disappear with the tool.

- [ ] **Step 2: Delete the temporary assets**

Remove the map, migration tool, and its focused test after their consumer search
returns zero. Record their commit IDs and manifest SHA-256 in `tasks.md` so the
reviewed migration remains recoverable through Git history. In the same commit,
remove the exact transition-only helper admission from
`validate-active-corpus-role-audit.py`, its role-audit test, and the
`tests/README.md` inventory row. Verify that the frozen 33-helper ACER ledger
and all permanent post-closure admissions remain unchanged, and restore
`docs/90.references/data/README.md` to the exact terminal 41-helper (`33 + 8`)
description.

Before deletion, run the tracked-tree search below and record every hit in the
Task evidence as `retiring-asset`, `current-evidence`, `immutable-historical`,
or `live-consumer`. Deletion requires zero `live-consumer` and zero
unclassified hits; literal zero is neither expected nor accepted. After
deletion, the permanent terminal registry scan repeats this classification.

- [ ] **Step 3: Run terminal residue checks**

```bash
test ! -e docs/04.execution
test ! -e scripts/document-taxonomy-migration.json
test ! -e scripts/migrate-document-work-units.py
test ! -e tests/test_migrate_document_work_units.py
test ! -e docs/04.operations
test ! -e docs/05.operations/releases
git grep -n -E 'document-taxonomy-migration\.json|migrate-document-work-units\.py|test_migrate_document_work_units\.py' -- .
python3 scripts/validate-document-contract-registry.py --root . --mode strict --route-state terminal
git grep -n -E 'docs/04\.execution|04\.execution/' -- .
```

Expected: the registry's path-class classifier reports no current mutable,
executable, contract, fixture, or navigation consumer. Every `git grep` hit is
machine-classified by its registered profile as immutable Stage 90/98 evidence
or rejected; the task evidence records the complete historical allowlist and
the validator fails on any unclassified or live hit. Literal-string absence is
not used as a proxy for consumer absence.

- [ ] **Step 4: Run the full terminal lane and commit**

```bash
git diff --check
python3 scripts/validate-document-contract-registry.py --root . --self-test
python3 scripts/validate-document-contract-registry.py --root . --mode strict --route-state terminal
python3 scripts/validate-markdown-profiles.py --root . --mode strict
python3 scripts/validate-links-and-owners.py --root . --mode strict
python3 -m unittest tests/test_archive_validation.py
python3 scripts/archive_cutover.py --root .
bash scripts/validate-repo-quality-gates.sh .
TMPDIR=/tmp pre-commit run --all-files
git status --short
git diff
git diff --cached
git diff --check
git diff --cached --check
git add -A
git commit -m "chore: remove document migration scaffolding"
```

#### Task 11: WDTC-110 — independent review and lifecycle closure

**Files:**

- Modify: `docs/03.specs/052-document-taxonomy-consolidation/spec.md`
- Modify: `docs/03.specs/052-document-taxonomy-consolidation/plan.md`
- Modify: `docs/03.specs/052-document-taxonomy-consolidation/tasks.md`
- Modify: `docs/01.requirements/008-workspace-document-taxonomy-consolidation.md`
- Modify: `docs/02.architecture/requirements/0011-document-taxonomy-consolidation-architecture.md`
- Modify: `docs/01.requirements/007-repository-delivery-and-platform-assurance.md`
- Modify: `docs/03.specs/047-current-surface-and-stash-reconciliation/spec.md`
- Modify: Stage 01/02/03 indexes and `docs/00.agent-governance/memory/progress.md`

**Interfaces:**

- Consumes: all WDTC commits and all terminal evidence.
- Produces: closed program evidence and a valid, still-unexecuted PRD-007
  resumption route.

- [ ] **Step 1: Perform the criterion walk**

Map VAL-WDTC-001 through VAL-WDTC-012 to observed command output, commit IDs,
archive/index evidence, and reviewed dispositions in `tasks.md`. A missing
criterion blocks closure.

- [ ] **Step 2: Request two independent reviews**

Dispatch one specification-compliance reviewer and one code-quality/security
reviewer over `14a0a75c..HEAD`. Require explicit findings for archive
immutability, route-state closure, link correctness, machine/prose authority,
agent evidence non-promotion, validator fixture preservation, and scope. Resolve
every Critical or Important finding before continuing.

- [ ] **Step 3: Run the final evidence bundle**

```bash
git diff --check
python3 scripts/validate-document-contract-registry.py --root . --self-test
python3 scripts/validate-document-contract-registry.py --root . --mode strict --route-state terminal
python3 scripts/validate-markdown-profiles.py --root . --mode strict
python3 scripts/validate-links-and-owners.py --root . --mode strict
python3 -m unittest tests/test_archive_validation.py
python3 scripts/archive_cutover.py --root .
python3 scripts/validate-agent-harness-contract.py --root .
python3 scripts/validate-agent-harness-semantics.py --root .
bash scripts/validate-repo-quality-gates.sh .
TMPDIR=/tmp pre-commit run --all-files
git status --short
git diff
git diff --cached
git diff --check
git diff --cached --check
```

Expected: every command passes and status is clean before the lifecycle edit.

- [ ] **Step 4: Close lifecycle and preserve the resumption boundary**

Set Spec 052, Plan, Tasks, PRD-008, and ARD-0011 to `done`; update their index
rows and evidence tables. Keep PRD-007 active and Specs 047-051 unexecuted;
record that their next work must start from the terminal Stage 03 route and
revalidate assumptions. Do not create a Release artifact.

- [ ] **Step 5: Validate the closure transition and commit**

```bash
python3 scripts/validate-document-lifecycle.py --root . --mode staged
bash scripts/validate-repo-quality-gates.sh .
TMPDIR=/tmp pre-commit run --all-files
git status --short
git diff
git diff --cached
git diff --check
git diff --cached --check
git add docs/01.requirements docs/02.architecture docs/03.specs docs/00.agent-governance/memory/progress.md
git commit -m "docs: close the document taxonomy consolidation"
```

## Verification Plan

| Work package | Focused evidence | Aggregate evidence |
| --- | --- | --- |
| WDTC-100 | lifecycle, registry self-test/projection | strict registry, links/owners, aggregate |
| WDTC-101 | Markdown and detect-secrets hooks | `TMPDIR=/tmp pre-commit run --all-files` |
| WDTC-102 | migration unit tests, route-state fixtures, manifest counts | strict transition registry, aggregate |
| WDTC-103 | archive unit tests, repository archive cutover, immutable prior-record diff | aggregate |
| WDTC-104 | 41/41 sibling counts, transition registry, Markdown, links | aggregate |
| WDTC-105 | terminal negative fixtures, Stage 04 absence, Stage 05/Release assertions | strict terminal documents, aggregate |
| WDTC-106 | harness/provider schema and semantic negative fixtures | agent lanes, aggregate |
| WDTC-107 | governance-CI and affected-surface topology tests | aggregate and all-files |
| WDTC-108 | archive recovery, ignored/generated residue | terminal registry, aggregate |
| WDTC-109 | zero temporary assets and terminal path residue | full terminal bundle and all-files |
| WDTC-110 | VAL-WDTC-001..012 walk and two independent reviews | staged lifecycle, aggregate, all-files |

All results are repository-static. Hosted CI, provider-runtime enforcement,
remote state, credentials, and live cluster behavior remain `DEFER` or outside
scope and are never inferred from these checks.

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
| One-time tooling becomes permanent legacy | Platform maintainer | WDTC-109 deletes map, tool, and tool-only tests after permanent fixtures own terminal behavior. |
| Large changes hide regressions | Reviewer | One logical commit per task, fresh worker, two review stages, focused and aggregate gates. |

## Completion Criteria

- ADR-0023 is accepted and is the only PRD-008 tranche decision.
- Exactly 41 live work units contain sibling Plan/Task pairs and no live Stage
  04 path remains.
- All 50 unmatched execution documents have validated ArchiveEnvelope records;
  the final repository total is 94 after the one progress snapshot, while the
  prior ARWB 31-record and ACER 12-record sets remain byte- and
  membership-identical.
- Stage 05 keeps its original path and four approved collections; no Release
  family exists.
- Mutable filenames are stable and every allowed date identity is registered.
- Stage 00, Stage 99, and the registry each own a disjoint authority layer.
- Agent-system controls are closed, reference existing owners, and do not
  promote repository-static evidence.
- Validation orchestration has one pre-commit aggregate path and no unique
  validator/fixture is lost.
- Progress history is recoverable, tracked graph output is absent and ignored,
  and no temporary migration asset remains.
- VAL-WDTC-001 through VAL-WDTC-012 have durable evidence.
- `git diff --check`, strict document lanes, archive validation, agent lanes,
  the aggregate gate, and `TMPDIR=/tmp pre-commit run --all-files` pass.
- Specs 047-051 remain unexecuted and have a terminal resumption route.

## Traceability

- **Program requirement**:
  [PRD-008](../../01.requirements/008-workspace-document-taxonomy-consolidation.md)
- **Architecture**:
  [ARD-0011](../../02.architecture/requirements/0011-document-taxonomy-consolidation-architecture.md)
- **Decision**:
  [ADR-0023](../../02.architecture/decisions/0023-work-unit-document-taxonomy-and-governance-authority.md)
- **Specification**:
  [Spec 052](../../03.specs/052-document-taxonomy-consolidation/spec.md)
- **Execution evidence**:
  [Task: Document Taxonomy Consolidation](../tasks/2026-08-07-document-taxonomy-consolidation.md)

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-WDTC-001](../../03.specs/052-document-taxonomy-consolidation/spec.md#success-criteria--verification-plan) | WDTC-102, WDTC-103, WDTC-104, WDTC-105 | [Manifest, archive, 41-work-unit inventory, terminal route result](../tasks/2026-08-07-document-taxonomy-consolidation.md) |
| [VAL-WDTC-002](../../03.specs/052-document-taxonomy-consolidation/spec.md#success-criteria--verification-plan) | WDTC-105 | [Stage 05 filesystem assertions and Release absence fixtures](../tasks/2026-08-07-document-taxonomy-consolidation.md) |
| [VAL-WDTC-003](../../03.specs/052-document-taxonomy-consolidation/spec.md#success-criteria--verification-plan) | WDTC-105 | [Stable filename inventory and closed exception fixtures](../tasks/2026-08-07-document-taxonomy-consolidation.md) |
| [VAL-WDTC-004](../../03.specs/052-document-taxonomy-consolidation/spec.md#success-criteria--verification-plan) | WDTC-100 | [Accepted ADR and registry/self-test decision projection](../tasks/2026-08-07-document-taxonomy-consolidation.md) |
| [VAL-WDTC-005](../../03.specs/052-document-taxonomy-consolidation/spec.md#success-criteria--verification-plan) | WDTC-105 | [Rule-to-owner inventory, form/profile parity, zero duplicate rule result](../tasks/2026-08-07-document-taxonomy-consolidation.md) |
| [VAL-WDTC-006](../../03.specs/052-document-taxonomy-consolidation/spec.md#success-criteria--verification-plan) | WDTC-102, WDTC-103, WDTC-108, WDTC-109 | [Disposition manifest, archive integrity, cleanup evidence](../tasks/2026-08-07-document-taxonomy-consolidation.md) |
| [VAL-WDTC-007](../../03.specs/052-document-taxonomy-consolidation/spec.md#success-criteria--verification-plan) | WDTC-107 | [Consumer/fixture comparison and validator disposition ledger](../tasks/2026-08-07-document-taxonomy-consolidation.md) |
| [VAL-WDTC-008](../../03.specs/052-document-taxonomy-consolidation/spec.md#success-criteria--verification-plan) | WDTC-106 | [Harness/provider schema and semantic negative fixtures](../tasks/2026-08-07-document-taxonomy-consolidation.md) |
| [VAL-WDTC-009](../../03.specs/052-document-taxonomy-consolidation/spec.md#success-criteria--verification-plan) | WDTC-108 | [Progress recovery and generated-output residue result](../tasks/2026-08-07-document-taxonomy-consolidation.md) |
| [VAL-WDTC-010](../../03.specs/052-document-taxonomy-consolidation/spec.md#success-criteria--verification-plan) | WDTC-101, WDTC-109, WDTC-110 | [Baseline repair and final aggregate/all-files PASS](../tasks/2026-08-07-document-taxonomy-consolidation.md) |
| [VAL-WDTC-011](../../03.specs/052-document-taxonomy-consolidation/spec.md#success-criteria--verification-plan) | WDTC-110 | [Spec 047-051 status inventory and resumption handoff](../tasks/2026-08-07-document-taxonomy-consolidation.md) |
| [VAL-WDTC-012](../../03.specs/052-document-taxonomy-consolidation/spec.md#success-criteria--verification-plan) | All work packages | [Local-only evidence classification and change inventory](../tasks/2026-08-07-document-taxonomy-consolidation.md) |
