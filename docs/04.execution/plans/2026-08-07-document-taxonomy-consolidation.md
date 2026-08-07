---
title: 'Document Taxonomy Consolidation Implementation Plan'
type: sdlc/plan
status: draft
owner: platform
updated: 2026-08-07
---

# Document Taxonomy Consolidation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> `superpowers:subagent-driven-development`; assign each WDTC package to a
> fresh worker, observe focused RED before GREEN, run the repository quality
> gate before every commit, and never write inside `docs/98.archive/**`.

## Overview

**Goal:** Retire the execution stage as a separate live tree, co-locate each
work unit's specification, plan, and task evidence under one numbered Stage 03
folder, renumber the operations stage, remove dates from authored filenames,
move cross-stage lineage into validated frontmatter, collapse ten
authoring-rule documents into three, and reduce the machine contract, migration
census, and validator corpus.

**Architecture:** Work proceeds as ordered logical commits in risk-ascending
order. Low-risk deletions run first and shrink the file population that later
high-blast-radius steps traverse. All path movement is performed by one
purpose-built migration tool that takes an explicit enumerated mapping and an
explicit exclusion set, refuses to run on a dirty tree, and aborts before any
write when a target exists or a source falls inside the archive. Contract
enforcement follows movement: validators are updated in the same commit as the
rule they encode, never before or after.

**Tech Stack:** Python 3 standard library, unittest, JSON Schema, Git plumbing
(`git ls-files`, `git mv`, `git cat-file`), the existing
`scripts/archive_cutover.py` envelope route, and
`bash scripts/validate-repo-quality-gates.sh`.

## Context

Spec 052 is the approved technical contract. Its measured baseline, taken on
2026-08-07, is: 47 specifications, 63 plans, 65 tasks; 321 tracked files
containing 8,995 occurrences of `04.execution` and 203 tracked files containing
6,937 occurrences of `05.operations`; 60 archive files among those references;
and a repository quality gate that passes in about two minutes and twenty
seconds with 37 results.

Every authored plan and task outside the suspended PRD-007 program carries
`status: done`. The ten exceptions are exactly the Spec 047 active pair and the
Spec 048 through 051 draft pairs.

`scripts/archive_validation.py` resolves archive payload links against each
record's `source_commit` in the Git tree, and each payload is sealed by
`content_sha256`. Archive records therefore stay correct across any live-path
change and must not be edited.

The cross-document validator enforces link target profiles per stage: a PRD
Traceability row may link only `sdlc/ard` or `sdlc/spec`, and an ARD
Traceability row may link only `sdlc/adr` or `sdlc/spec`.

### Global Constraints

- Never create, modify, delete, reformat, or rename anything under
  `docs/98.archive/**` except by appending a new record through
  `scripts/archive_cutover.py`. Editing an existing record is a contract
  violation.
- Run `bash scripts/validate-repo-quality-gates.sh .` before every commit.
  A failing gate blocks the commit; it is never deferred.
- Never renumber an existing PRD, ARD, ADR, or specification identifier.
- Stage 03 specifications, plans, and tasks are English-first. Stage README
  and human-facing overview prose stays Korean.
- Authored filenames under stages 01 through 04 must not begin with a date
  after WDTC-005. Archive records and Stage 90 dated pack directories keep
  their dates.
- Repository-static results are never reported as hosted CI, provider-runtime,
  remote, or live evidence.
- No push, no remote mutation, no cluster action, no credential read.
- One logical unit per commit, using conventional commit format.
- The repository has no `pytest`. Tests run with
  `python3 -m unittest discover`. The repository quality gate runs only four
  named test files, so a passing gate does not mean the suite is green.
- Pre-existing suite state observed on the base commit `c62a5cd9` and confirmed
  unchanged at `7ec233a3`: `Ran 775 tests`, 7 failures and 1 error, all in
  `tests/test_reference_information_architecture.py` and
  `tests/test_active_corpus_retention.py`. These predate this program. No
  package is required to fix them, and no package may add to the list. Compare
  against the list, never against zero.
- This plan and its task document migrate themselves. WDTC-006 moves
  `docs/04.execution/plans/2026-08-07-document-taxonomy-consolidation.md` to
  `docs/03.specs/052-document-taxonomy-consolidation/plan.md` and the task
  document to `.../tasks.md`. From WDTC-007 onward, write execution evidence to
  the new path. Task briefs are extracted to the SDD workspace before dispatch,
  so a running package never depends on the plan file's live location.

## Goals & In-Scope

- Co-locate the 39 G-A work units as `spec.md`, `plan.md`, `tasks.md`.
- Archive the 24 G-C orphan plans and 3 G-D orphan tasks through the existing
  envelope route.
- Retire `docs/04.execution/` as a live path and rewrite every non-archive
  reference.
- Rename `docs/05.operations/` to `docs/04.operations/` and rewrite every
  non-archive reference.
- Add and enforce contracts C-1 through C-6 from Spec 052.
- Delete the `active-corpus-*` census, its five exclusive validators, and
  `scripts/archive_cutover_manifest.py`.
- Archive the superseded `2026-07-04-wer` research pack.
- Rotate `docs/00.agent-governance/memory/progress.md` to a bounded window.
- Collapse the ten authoring-rule documents into three.
- Remove the 24 `template/*` mirror profiles from the profile registry.
- Consolidate the agent governance machine contracts.
- Disposition documentation gaps DOC-G1 through DOC-G10.
- Reconcile the script surface with the validator selection contract.

## Non-Goals & Out-of-Scope

- Any change under `docs/98.archive/**` other than appended records.
- Removing the numbered stage-prefix scheme.
- Creating tutorial, explanation, or release-notes document routes.
- Executing any PRD-007 tranche, or changing its subject matter.
- Changing `gitops/`, `infrastructure/`, `traefik/`, or `policy/` desired state.
- Changing agent role semantics, the role roster, or provider adapters beyond
  path references.
- Any hosted CI, remote, live-cluster, or credential-bearing action.

## Work Breakdown

| ID       | Work package                                                                           | Depends on         | Entry gate                                           | Exit evidence                                                                       |
| -------- | -------------------------------------------------------------------------------------- | ------------------ | ---------------------------------------------------- | ----------------------------------------------------------------------------------- |
| WDTC-000 | Activate the reciprocal execution path and suspend PRD-007                             | None               | Spec 052 approved                                    | Spec 052 `active` with plan and task links; Spec 047 and PRD-007 recorded suspended |
| WDTC-001 | Delete the completed migration census, its exclusive validators, and the orphan script | WDTC-000           | Zero-referent proof for each deleted asset           | Gate passes with the assets removed and no dangling reference                       |
| WDTC-002 | Archive the superseded research pack                                                   | WDTC-000           | Supersession already recorded in the 2026-07-07 pack | Envelope records present; live pack removed                                         |
| WDTC-003 | Rotate the shared progress ledger                                                      | WDTC-000           | Current period boundary chosen                       | Live ledger bounded; closed periods recoverable through the archive index           |
| WDTC-004 | Archive the 27 orphan execution documents                                              | WDTC-001           | All 27 confirmed `status: done`                      | Envelope records present; live documents removed                                    |
| WDTC-005 | Build and prove the migration tool                                                     | WDTC-004           | Failing tests exist first                            | Tool passes its unit tests including every abort condition                          |
| WDTC-006 | Co-locate the 39 work units and retire the execution stage                             | WDTC-005           | Dry-run change set reviewed                          | No live `04.execution` path; gate passes                                            |
| WDTC-007 | Renumber the operations stage                                                          | WDTC-006           | Dry-run change set reviewed                          | No live `05.operations` path; gate passes                                           |
| WDTC-008 | Enforce C-1, C-2, and C-3 and retire the date-based rule                               | WDTC-007           | Negative fixtures fail first                         | Validator rejects each violation; retired sentence returns zero live hits           |
| WDTC-009 | Add C-4 lineage frontmatter and reciprocal validation                                  | WDTC-008           | Negative fixtures fail first                         | Every Stage 03 spec declares resolvable reciprocal lineage                          |
| WDTC-010 | Collapse the authoring-rule documents from ten to three                                | WDTC-009           | Rule inventory mapped source to target               | Three owners; each rule stated once                                                 |
| WDTC-011 | Remove the template mirror profiles                                                    | WDTC-010           | Route coverage captured before change                | Same path coverage with fewer profiles                                              |
| WDTC-012 | Consolidate the agent governance machine contracts                                     | WDTC-011           | Assertion inventory captured before change           | Same assertion set; smaller corpus; independently revertible commit                 |
| WDTC-013 | Disposition the ten documentation gaps                                                 | WDTC-010           | Gap table from Spec 052                              | Each gap has an implemented control or a dated recorded decision                    |
| WDTC-014 | Reconcile the script surface with the selection contract                               | WDTC-012, WDTC-013 | Declared and executable sets enumerated              | Sets equal, enforced by a declared validator                                        |
| WDTC-015 | Measure, review, and close                                                             | WDTC-014           | All predecessors complete                            | Per-asset deltas recorded; independent review; Spec 052 `done`                      |

### File map and interfaces

**Created**

- `scripts/migrate_document_paths.py` — the migration tool. Owns mapping
  parsing, exclusion enforcement, abort conditions, `git mv` execution, and
  reference rewriting. No inference: every source-target pair is enumerated.
- `tests/test_migrate_document_paths.py` — unit tests for the tool, including
  one test per abort condition.
- `scripts/validate-document-taxonomy.py` — enforces C-1, C-2, C-3, C-4, and
  C-5. One validator for the taxonomy rule family.
- `tests/test_validate_document_taxonomy.py` — negative fixtures for every
  contract clause.
- `docs/00.agent-governance/rules/document-authoring.md` — stage ownership,
  timing, persona, completion.
- `docs/99.templates/support/document-contract.md` — template selection,
  frontmatter, headings.
- `docs/99.templates/support/document-lifecycle.md` — status, promotion,
  supersession, retirement, archive routing.

**Deleted**

- `docs/90.references/data/active-corpus-eligibility-ledger.json`,
  `active-corpus-migration-results.json`,
  `active-corpus-residue-closure.json`,
  `active-corpus-retention-census.json`,
  `active-corpus-role-audit.json`
- `scripts/validate-active-corpus-eligibility.py`,
  `validate-active-corpus-migrations.py`,
  `validate-active-corpus-residue-closure.py`,
  `validate-active-corpus-retention.py`,
  `validate-active-corpus-role-audit.py`
- `scripts/archive_cutover_manifest.py`
- `tests/test_active_corpus_*.py`
- `docs/00.agent-governance/rules/stage-authoring-matrix.md`,
  `document-stage-routing.md`, `stage-checklists.md`,
  `documentation-protocol.md`
- `docs/99.templates/support/documentation-contract.md`,
  `template-routing.md`, `frontmatter-schema.md`,
  `common-documentation-governance.md`, `sdlc-governance.md`,
  `legacy-cleanup-rules.md`
- `docs/04.execution/` in its entirety, including both stage READMEs

**Modified**

- `docs/00.agent-governance/contracts/validation-surfaces.json` — validator
  set changes in every package that adds or removes a validator.
- `docs/99.templates/support/document-profiles.json` — route changes in
  WDTC-006 and WDTC-007; profile removal in WDTC-011.
- `docs/00.agent-governance/rules/bootstrap.md`, `preflight-checklist.md`,
  `postflight-checklist.md`, `quality-standards.md` — route references.
- `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `.claude/CLAUDE.md`, and the
  `.agents/`, `.codex/`, `.gemini/` adapters — route references only.
- `docs/00.agent-governance/memory/progress.md` — one entry per package.

**Interfaces produced by WDTC-005 and consumed by WDTC-006 and WDTC-007**

```python
# scripts/migrate_document_paths.py

class MigrationAbort(Exception):
    """Raised before any write when a precondition fails."""

def load_mapping(path: str) -> tuple[tuple[str, str], ...]:
    """Return enumerated (source, target) pairs from a JSON mapping file."""

def load_exclusions(path: str) -> frozenset[str]:
    """Return repository-relative path prefixes excluded from rewriting."""

def plan_moves(
    mapping: tuple[tuple[str, str], ...],
    existing: frozenset[str],
    exclusions: frozenset[str],
) -> tuple[tuple[str, str], ...]:
    """Validate every pair and return the ordered move set.

    Raises MigrationAbort when a target exists, a source is missing, a source
    or target is inside an exclusion prefix, or a target is claimed twice.
    """

def plan_rewrites(
    tracked: tuple[str, ...],
    substitutions: tuple[tuple[str, str], ...],
    exclusions: frozenset[str],
) -> tuple[str, ...]:
    """Return the files whose contents contain a retired segment and are not
    excluded. Order is stable and lexicographic."""
```

CLI modes, all of which honour `--exclude` and refuse a dirty tree on apply:

```
migrate_document_paths.py --map M --exclude E [--dry-run | --apply]
migrate_document_paths.py --substitute 'OLD=NEW' [--substitute ...] \
                          --exclude E [--dry-run | --apply]
```

`--map` moves files and rewrites references to the moved paths.
`--substitute` rewrites literal segment occurrences without moving anything;
each pair is applied literally, never as a regular expression.

---

### Task 1: WDTC-000 — activate the reciprocal execution path

**Files:**

- Modify: `docs/03.specs/052-document-taxonomy-consolidation/spec.md`
- Modify: `docs/01.requirements/008-workspace-document-taxonomy-consolidation.md`
- Modify: `docs/01.requirements/007-repository-delivery-and-platform-assurance.md`
- Modify: `docs/03.specs/047-current-surface-and-stash-reconciliation/spec.md`
- Modify: `docs/04.execution/plans/2026-08-02-current-surface-and-stash-reconciliation.md`
- Modify: `docs/04.execution/tasks/2026-08-02-current-surface-and-stash-reconciliation.md`
- Modify: `docs/03.specs/README.md`, `docs/01.requirements/README.md`
- Create: `docs/04.execution/tasks/2026-08-07-document-taxonomy-consolidation.md`

**Interfaces:**

- Consumes: nothing.
- Produces: an `active` Spec 052 with reciprocal `plan.md` and task links, and
  a `draft` Spec 047 whose suspension rationale is recorded in PRD-007.

- [ ] **Step 1: Author the reciprocal task document**

Create `docs/04.execution/tasks/2026-08-07-document-taxonomy-consolidation.md`
from `docs/99.templates/templates/sdlc/execution/task.template.md` with
frontmatter `status: draft`, `updated: 2026-08-07`, and one `WORK-0NN` row per
work package WDTC-000 through WDTC-015, each row citing its VAL-WDTC criterion
and starting at `Queued` / `Not executed`.

Set the Approval and Safety Boundaries block to:

```markdown
- **Allowed Paths**: `docs/**` except `docs/98.archive/**`, `scripts/**`, `tests/**`, `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `.claude/**`, `.agents/**`, `.codex/**`, `.gemini/**`
- **Forbidden Paths**: `docs/98.archive/**` for modification, `gitops/**`, `infrastructure/**`, `traefik/**`, `policy/**`, `secrets/**`
- **Approval Required**: Human approval before any archive-record modification, any stage identifier renumbering, or any action outside the local repository.
- **Static Validation**: `bash scripts/validate-repo-quality-gates.sh .` before every commit; expected PASS.
- **Live Validation**: DEFER — this program performs no live, hosted, remote, or credential-bearing action.
- **Secret / Vault Handling**: No secret, token, kubeconfig, or credential file is read or printed.
- **Rollback Plan**: Each work package is one revertible commit; the migration commits run only against a clean tree.
- **Evidence Location**: This task document and `docs/00.agent-governance/memory/progress.md`.
```

- [ ] **Step 2: Restore the Spec 052 reciprocal links**

In `docs/03.specs/052-document-taxonomy-consolidation/spec.md`, set
`status: active` and add back to the Traceability bullet list, immediately
after the External evidence bullet:

```markdown
- **Implementation Plan**:
  [Document Taxonomy Consolidation Implementation Plan](../../04.execution/plans/2026-08-07-document-taxonomy-consolidation.md)
- **Execution Task**:
  [Task: Document Taxonomy Consolidation](../../04.execution/tasks/2026-08-07-document-taxonomy-consolidation.md)
```

Set this plan's frontmatter `status: active`.

- [ ] **Step 3: Record the PRD-007 suspension**

In `docs/01.requirements/007-repository-delivery-and-platform-assurance.md`,
replace the sentence "PRD-007 is active with Spec 047 as its only active
unfinished tranche; Specs 048-051 remain planned draft successors." with:

```markdown
PRD-007 is suspended as of 2026-08-07 for the duration of the PRD-008 document
taxonomy consolidation program, because Specs 049 and 050 would author
validators against a surface that program consolidates. Spec 047 returns to
draft and Specs 048-051 remain planned draft successors. The program resumes in
the consolidated structure when Spec 052 reaches `done`.
```

Set `status: draft` on Spec 047 and on its plan and task. Update the
`docs/01.requirements/README.md` and `docs/03.specs/README.md` index rows for
PRD-007 and Spec 047 to state Draft and cite the suspension.

- [ ] **Step 4: Set Spec 052 and PRD-008 to active**

Set `status: active` on
`docs/01.requirements/008-workspace-document-taxonomy-consolidation.md` and on
`docs/02.architecture/requirements/0011-document-taxonomy-consolidation-architecture.md`.
Update their README index rows from Draft to Active.

- [ ] **Step 5: Run the gate**

```bash
bash scripts/validate-repo-quality-gates.sh .
```

Expected: PASS. If `INDEX-MISSING` or `BODY-LINK-*` appears, the README rows or
Traceability link profiles are wrong; fix them rather than weakening the
validator.

- [ ] **Step 6: Commit**

```bash
git add -A docs/
git commit -m "docs: activate spec 052 and suspend the delivery assurance program

Activate PRD-008, ARD-0011, and Spec 052 with reciprocal plan and task
evidence. Record PRD-007 as suspended and return Spec 047 and its execution
pair to draft, because Specs 049 and 050 would author validators against a
surface this program consolidates."
```

---

### Task 2: WDTC-001 — delete the completed migration census

**Files:**

- Delete: five `docs/90.references/data/active-corpus-*.json`
- Delete: five `scripts/validate-active-corpus-*.py`
- Delete: `scripts/archive_cutover_manifest.py`
- Delete: matching `tests/test_active_corpus_*.py`
- Modify: `docs/00.agent-governance/contracts/validation-surfaces.json`
- Modify: `docs/90.references/data/README.md`, `scripts/README.md`

**Interfaces:**

- Consumes: WDTC-000's active execution path.
- Produces: a smaller validator set for WDTC-014 to reconcile.

- [ ] **Step 1: Prove zero remaining referents**

```bash
for n in active-corpus-eligibility active-corpus-migrations \
         active-corpus-residue-closure active-corpus-retention \
         active-corpus-role-audit archive_cutover_manifest; do
  echo "== $n"
  git ls-files -z | xargs -0 grep -l "$n" | grep -v '^docs/98.archive/'
done
```

Expected: only the files being deleted, plus `scripts/README.md`,
`docs/90.references/data/README.md`, and `validation-surfaces.json`. Any other
hit is a live consumer and must be resolved before deleting.

- [ ] **Step 2: Delete the assets**

```bash
git rm docs/90.references/data/active-corpus-*.json \
       scripts/validate-active-corpus-*.py \
       scripts/archive_cutover_manifest.py \
       tests/test_active_corpus_*.py
```

- [ ] **Step 3: Remove them from the inventories and the selection contract**

Remove the corresponding entries from
`docs/00.agent-governance/contracts/validation-surfaces.json`, the script table
in `scripts/README.md`, and the data index in
`docs/90.references/data/README.md`. Add one sentence to the data README
recording that the retention migration completed and its census is retired.

- [ ] **Step 4: Run the gate**

```bash
bash scripts/validate-repo-quality-gates.sh .
```

Expected: PASS. A `LINK-BROKEN` failure names a referent Step 1 missed.

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "chore: retire the completed active-corpus migration census

Delete the five census ledgers, their five exclusive validators, their tests,
and the zero-referent archive cutover manifest script. The retention migration
they recorded is complete and its outcome is the current tree."
```

---

### Task 3: WDTC-002 — archive the superseded research pack

**Files:**

- Archive: the six files under `docs/90.references/research/2026-07-04-wer/`
- Modify: `docs/90.references/research/README.md`

**Interfaces:**

- Consumes: WDTC-000.
- Produces: one live research pack per subject.

- [ ] **Step 1: Confirm the supersession is already recorded**

```bash
grep -n "2026-07-04" docs/90.references/research/2026-08-07-wer/research-consolidation-and-supersession-map.md
```

Expected: the map names each 2026-07-04 file and its surviving owner. If a file
has no recorded successor, stop and record one before archiving it.

- [ ] **Step 2: Archive each file through the envelope route**

```bash
for f in docs/90.references/research/2026-07-04-wer/*.md; do
  python3 scripts/archive_cutover.py --root . --source "$f" \
    --reason superseded \
    --replacement docs/90.references/research/2026-07-07-wer/"$(basename "$f")"
done
```

For `README.md`, use the 2026-07-07 pack README as the replacement. If a
2026-07-07 counterpart does not exist, use the supersession map as the
replacement.

- [ ] **Step 3: Update the research index**

Remove the 2026-07-04 pack rows and tree entries from
`docs/90.references/research/README.md` and add one sentence pointing readers
to the archive index for the retired pack.

- [ ] **Step 4: Run the gate and archive validation**

```bash
python3 scripts/archive_validation.py --root .
bash scripts/validate-repo-quality-gates.sh .
```

Expected: both PASS.

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "docs: archive the superseded 2026-07-04 research pack

The pack's facts were merged into the 2026-07-07 owners and the supersession is
recorded in the 2026-08-07 consolidation map. Retire the duplicate live pack
through the archive envelope route."
```

---

### Task 4: WDTC-003 — rotate the shared progress ledger

**Files:**

- Modify: `docs/00.agent-governance/memory/progress.md`
- Archive: the closed-period sections
- Modify: `docs/00.agent-governance/memory/README.md`

**Interfaces:**

- Consumes: WDTC-000.
- Produces: a bounded ledger for every later package to append to.

- [ ] **Step 1: Choose and record the retention boundary**

Retain entries dated 2026-07-01 and later in the live ledger. Archive
everything older as one record per calendar quarter.

```bash
grep -n '^### ' docs/00.agent-governance/memory/progress.md | head -60
```

Note the line range of the oldest retained entry; everything below it rotates.

- [ ] **Step 2: Extract the closed periods into archive records**

For each closed quarter, write the exact removed section bytes as the payload
of one archive record with `original_path`
`docs/00.agent-governance/memory/progress.md`, `archive_reason` `rotated`, and
`replacement` pointing at the live ledger. Use `scripts/archive_cutover.py`
with an explicit payload file rather than editing an envelope by hand.

- [ ] **Step 3: Truncate the live ledger and add a pointer**

Remove the rotated sections. Immediately under `## Work Entries`, add:

```markdown
> Entries before 2026-07-01 are rotated into archive records. Find them through
> the [archive index](../../98.archive/README.md). This ledger holds the
> current retention window only; it remains the single durable owner of shared
> progress.
```

Record the same retention rule in `docs/00.agent-governance/memory/README.md`.

- [ ] **Step 4: Verify recoverability**

```bash
python3 scripts/archive_recovery.py --root . --original-path docs/00.agent-governance/memory/progress.md --list
python3 scripts/archive_validation.py --root .
```

Expected: every rotated period is listed and validation passes.

- [ ] **Step 5: Run the gate and commit**

```bash
bash scripts/validate-repo-quality-gates.sh .
git add -A
git commit -m "docs: rotate the shared progress ledger to a bounded window

Retain entries from 2026-07-01 onward in the live ledger and rotate older
periods into archive records, one per quarter. The ledger remains the single
durable owner of shared progress; only its retention window changes."
```

---

### Task 5: WDTC-004 — archive the orphan execution documents

**Files:**

- Archive: 24 plans and 3 tasks under `docs/04.execution/`
- Modify: `docs/04.execution/plans/README.md`, `docs/04.execution/tasks/README.md`

**Interfaces:**

- Consumes: WDTC-001's reduced file population.
- Produces: an execution stage containing only G-A members, which WDTC-006
  moves wholesale.

- [ ] **Step 1: Regenerate the orphan list and confirm every member is done**

```bash
python3 - <<'PY'
import glob, os, re
specs = {re.match(r'(\d{3})-(.+)', d).group(2)
         for d in os.listdir('docs/03.specs') if re.match(r'\d{3}-', d)}
for kind in ('plans', 'tasks'):
    for f in sorted(glob.glob(f'docs/04.execution/{kind}/*.md')):
        b = os.path.basename(f)[:-3]
        m = re.match(r'\d{4}-\d{2}-\d{2}-(.+)', b)
        if not m or m.group(1) in specs:
            continue
        status = re.search(r'^status:\s*(\S+)', open(f).read(1500), re.M)
        print(f, status.group(1) if status else 'NO-STATUS')
PY
```

Expected: 24 plans and 3 tasks, every one `done`. Any non-`done` row stops the
task and is escalated, because archiving unfinished work destroys its evidence.

- [ ] **Step 2: Archive each orphan**

```bash
python3 scripts/archive_cutover.py --root . --source <path> \
  --reason superseded --replacement docs/03.specs/README.md
```

Where a specific successor work unit exists, name its `spec.md` as the
replacement instead of the stage index.

- [ ] **Step 3: Run the gate and archive validation**

```bash
python3 scripts/archive_validation.py --root .
bash scripts/validate-repo-quality-gates.sh .
```

Expected: both PASS. Confirm the archive mirror paths retain the
`04.execution` segment; that is the historically correct mirror.

- [ ] **Step 4: Commit**

```bash
git add -A
git commit -m "docs: archive the 27 orphan execution records

Archive the 24 plans and 3 tasks that have no specification. Every one carries
status done, so each is a complete historical record rather than interrupted
work. Their archive mirror paths retain the execution segment, which is the
historically correct mirror."
```

---

### Task 6: WDTC-005 — build and prove the migration tool

**Files:**

- Create: `scripts/migrate_document_paths.py`
- Create: `tests/test_migrate_document_paths.py`

**Interfaces:**

- Consumes: WDTC-004's reduced execution stage.
- Produces: `load_mapping`, `load_exclusions`, `plan_moves`, `plan_rewrites`,
  and `MigrationAbort` exactly as declared in the file map above.

- [ ] **Step 1: Write the failing tests**

```python
import unittest
from scripts.migrate_document_paths import (
    MigrationAbort, plan_moves, plan_rewrites,
)

ARCHIVE = frozenset({"docs/98.archive/"})


class PlanMovesTest(unittest.TestCase):
    def test_returns_ordered_pairs_when_valid(self):
        mapping = (("a/x.md", "b/x.md"), ("a/y.md", "b/y.md"))
        existing = frozenset({"a/x.md", "a/y.md"})
        self.assertEqual(plan_moves(mapping, existing, ARCHIVE), mapping)

    def test_aborts_when_target_exists(self):
        mapping = (("a/x.md", "b/x.md"),)
        existing = frozenset({"a/x.md", "b/x.md"})
        with self.assertRaises(MigrationAbort):
            plan_moves(mapping, existing, ARCHIVE)

    def test_aborts_when_source_missing(self):
        with self.assertRaises(MigrationAbort):
            plan_moves(
                (("a/x.md", "b/x.md"),), frozenset(), ARCHIVE
            )

    def test_aborts_when_source_inside_exclusion(self):
        mapping = (("docs/98.archive/x.md", "b/x.md"),)
        with self.assertRaises(MigrationAbort):
            plan_moves(mapping, frozenset({"docs/98.archive/x.md"}), ARCHIVE)

    def test_aborts_when_target_inside_exclusion(self):
        mapping = (("a/x.md", "docs/98.archive/x.md"),)
        with self.assertRaises(MigrationAbort):
            plan_moves(mapping, frozenset({"a/x.md"}), ARCHIVE)

    def test_aborts_when_target_claimed_twice(self):
        mapping = (("a/x.md", "b/z.md"), ("a/y.md", "b/z.md"))
        with self.assertRaises(MigrationAbort):
            plan_moves(mapping, frozenset({"a/x.md", "a/y.md"}), ARCHIVE)


class PlanRewritesTest(unittest.TestCase):
    def test_excludes_archive_paths(self):
        tracked = ("docs/a.md", "docs/98.archive/b.md")
        result = plan_rewrites(
            tracked, (("04.execution", "03.specs"),), ARCHIVE
        )
        self.assertNotIn("docs/98.archive/b.md", result)

    def test_is_lexicographically_stable(self):
        tracked = ("docs/z.md", "docs/a.md")
        result = plan_rewrites(
            tracked, (("04.execution", "03.specs"),), ARCHIVE
        )
        self.assertEqual(tuple(sorted(result)), result)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the tests to verify they fail**

```bash
python3 -m unittest discover -s tests -p test_migrate_document_paths.py -v
```

Expected: an import error naming `scripts.migrate_document_paths`; the suite
reports `ERROR`, not `OK`.

- [ ] **Step 3: Implement the tool**

Implement `scripts/migrate_document_paths.py` with the declared interface.
`plan_rewrites` reads each tracked file and returns those containing any
substitution's first element, skipping any path that starts with an exclusion
prefix. The CLI adds `--dry-run` and `--apply`; `--apply` first checks
`git status --porcelain` and raises `MigrationAbort` when the tree is dirty,
then performs `git mv` for each planned move and applies substitutions to each
planned rewrite file.

- [ ] **Step 4: Run the tests to verify they pass**

```bash
python3 -m unittest discover -s tests -p test_migrate_document_paths.py -v
```

Expected: `Ran 8 tests` and `OK`.

- [ ] **Step 5: Register the tool and commit**

Add the tool to the `scripts/README.md` inventory. The migration tool is not a
validator and is not added to `validation-surfaces.json`.

```bash
bash scripts/validate-repo-quality-gates.sh .
git add scripts/migrate_document_paths.py tests/test_migrate_document_paths.py scripts/README.md
git commit -m "feat: add the enumerated document path migration tool

The tool takes an explicit source-to-target mapping and an explicit exclusion
set, performs no path inference, and aborts before any write when a target
exists, a source is missing, either endpoint falls inside an exclusion, a
target is claimed twice, or the working tree is dirty."
```

---

### Task 7: WDTC-006 — co-locate the work units and retire the execution stage

**Files:**

- Move: 39 plans and 39 tasks into their specification folders
- Delete: `docs/04.execution/` including both stage READMEs
- Modify: `docs/99.templates/support/document-profiles.json` routes
- Modify: every non-archive file referencing `04.execution`

**Interfaces:**

- Consumes: WDTC-005's tool.
- Produces: the Stage 03 work-unit layout that WDTC-008 enforces.

- [ ] **Step 1: Generate the mapping**

```bash
python3 - <<'PY' > /tmp/wdtc-006-map.json
import glob, json, os, re
specs = {re.match(r'(\d{3})-(.+)', d).group(2): d
         for d in os.listdir('docs/03.specs') if re.match(r'\d{3}-', d)}
pairs = []
for kind, name in (('plans', 'plan.md'), ('tasks', 'tasks.md')):
    for f in sorted(glob.glob(f'docs/04.execution/{kind}/*.md')):
        m = re.match(r'\d{4}-\d{2}-\d{2}-(.+)\.md', os.path.basename(f))
        if m and m.group(1) in specs:
            pairs.append([f, f'docs/03.specs/{specs[m.group(1)]}/{name}'])
json.dump(pairs, __import__('sys').stdout, indent=1)
PY
python3 -c "import json;d=json.load(open('/tmp/wdtc-006-map.json'));print(len(d),'moves')"
```

Expected: 78 moves — 39 plans and 39 tasks.

- [ ] **Step 2: Dry-run and review the change set**

```bash
printf 'docs/98.archive/\ngraphify-out/\n' > /tmp/wdtc-exclude.txt
python3 scripts/migrate_document_paths.py \
  --map /tmp/wdtc-006-map.json --exclude /tmp/wdtc-exclude.txt --dry-run
```

Expected: exit 0 and 78 moves plus the rewrite file list. A non-zero exit names
the failing precondition; resolve it before applying.

- [ ] **Step 3: Apply the moves and rewrite references**

```bash
python3 scripts/migrate_document_paths.py \
  --map /tmp/wdtc-006-map.json --exclude /tmp/wdtc-exclude.txt --apply
git rm -r docs/04.execution
```

Then rewrite the remaining references with the tool's substitution mode, mapping
`docs/04.execution/plans/<date>-<slug>.md` to
`docs/03.specs/<NNN>-<slug>/plan.md` and the task equivalent, one enumerated
substitution per moved file rather than a regular expression.

- [ ] **Step 4: Update the profile registry routes**

In `docs/99.templates/support/document-profiles.json`, change the `sdlc/plan`
route to `docs/03.specs/<NNN>-<slug>/plan.md` and the `sdlc/task` route to
`docs/03.specs/<NNN>-<slug>/tasks.md`. Remove the retired stage README routes.

- [ ] **Step 5: Verify no live execution path survives**

```bash
git ls-files -z | xargs -0 grep -l '04\.execution' | grep -v '^docs/98.archive/'
```

Expected: no output. Any hit outside the archive is an unrewritten reference.

- [ ] **Step 6: Run the gate and commit**

```bash
bash scripts/validate-repo-quality-gates.sh .
git add -A
git commit -m "refactor: co-locate work units and retire the execution stage

Move 39 plans and 39 tasks into their specification folders as plan.md and
tasks.md, delete the execution stage, and rewrite every non-archive reference.
Archive records keep their execution-segment links, which resolve against their
source commits and stay correct."
```

---

### Task 8: WDTC-007 — renumber the operations stage

**Files:**

- Move: `docs/05.operations/` to `docs/04.operations/`
- Modify: `docs/99.templates/support/document-profiles.json` routes
- Modify: every non-archive file referencing `05.operations`

**Interfaces:**

- Consumes: WDTC-006's completed rewrite.
- Produces: the contiguous stage sequence that C-3 enforces.

- [ ] **Step 1: Move the stage**

```bash
git mv docs/05.operations docs/04.operations
```

- [ ] **Step 2: Rewrite references outside the archive**

```bash
python3 scripts/migrate_document_paths.py \
  --substitute '05.operations=04.operations' \
  --exclude /tmp/wdtc-exclude.txt --dry-run
```

Review the file list, then rerun with `--apply`. The Stage 90 dated packs are
in scope for navigational links only; where a pack sentence states an
observation about the old path, keep the old path and append
`(path retired 2026-08-07; now docs/04.operations/…)`.

- [ ] **Step 3: Update the profile registry and stage index**

Change every `docs/05.operations` route in
`docs/99.templates/support/document-profiles.json` to `docs/04.operations`.
Update `docs/04.operations/README.md` title and tree to the new number.

- [ ] **Step 4: Verify no live reference survives**

```bash
git ls-files -z | xargs -0 grep -l '05\.operations' | grep -v '^docs/98.archive/'
```

Expected: no output, or only Stage 90 files whose hits are the annotated
historical observations from Step 2.

- [ ] **Step 5: Run the gate and commit**

```bash
bash scripts/validate-repo-quality-gates.sh .
git add -A
git commit -m "refactor: renumber the operations stage to 04

Reclaim the slot left by the retired execution stage so the active stage
sequence is contiguous. Archive records and dated Stage 90 observations keep
their original paths."
```

---

### Task 9: WDTC-008 — enforce C-1, C-2, and C-3 and retire the date rule

**Files:**

- Create: `scripts/validate-document-taxonomy.py`
- Create: `tests/test_validate_document_taxonomy.py`
- Modify: `docs/00.agent-governance/contracts/validation-surfaces.json`
- Modify: the three files stating the retired date-based rule

**Interfaces:**

- Consumes: WDTC-007's final layout.
- Produces: `validate_work_unit_locality`, `validate_filename_dates`, and
  `validate_stage_sequence`, each returning a tuple of diagnostic strings that
  is empty on success. WDTC-009 extends the same module.

- [ ] **Step 1: Write the failing tests**

```python
#!/usr/bin/env python3
"""Focused tests for the document taxonomy contract."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPOSITORY_ROOT / "scripts/validate-document-taxonomy.py"


def load_module():
    spec = importlib.util.spec_from_file_location(
        "validate_document_taxonomy", SCRIPT_PATH
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {SCRIPT_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_m = load_module()
validate_work_unit_locality = _m.validate_work_unit_locality
validate_filename_dates = _m.validate_filename_dates
validate_stage_sequence = _m.validate_stage_sequence


class WorkUnitLocalityTest(unittest.TestCase):
    def test_accepts_spec_only(self):
        self.assertEqual(
            validate_work_unit_locality({"047-a": {"spec.md"}}), ()
        )

    def test_accepts_full_triad(self):
        files = {"spec.md", "plan.md", "tasks.md"}
        self.assertEqual(validate_work_unit_locality({"047-a": files}), ())

    def test_rejects_plan_without_spec(self):
        self.assertEqual(
            len(validate_work_unit_locality({"047-a": {"plan.md"}})), 1
        )

    def test_rejects_tasks_without_plan(self):
        files = {"spec.md", "tasks.md"}
        self.assertEqual(
            len(validate_work_unit_locality({"047-a": files})), 1
        )


class FilenameDateTest(unittest.TestCase):
    def test_rejects_dated_authored_filename(self):
        paths = ("docs/03.specs/047-a/2026-08-07-plan.md",)
        self.assertEqual(len(validate_filename_dates(paths)), 1)

    def test_allows_dated_archive_path(self):
        paths = ("docs/98.archive/04.execution/plans/2026-08-02-a.md",)
        self.assertEqual(validate_filename_dates(paths), ())

    def test_allows_dated_stage_90_pack_directory(self):
        paths = ("docs/90.references/research/2026-08-07-wer/README.md",)
        self.assertEqual(validate_filename_dates(paths), ())


class StageSequenceTest(unittest.TestCase):
    def test_accepts_contiguous_sequence(self):
        stages = ("00", "01", "02", "03", "04", "90", "98", "99")
        self.assertEqual(validate_stage_sequence(stages), ())

    def test_rejects_reintroduced_execution_stage(self):
        stages = ("00", "01", "02", "03", "04", "05", "90", "98", "99")
        self.assertEqual(len(validate_stage_sequence(stages)), 1)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the tests to verify they fail**

```bash
python3 -m unittest discover -s tests -p test_validate_document_taxonomy.py -v
```

Expected: a load error because `scripts/validate-document-taxonomy.py` does not
exist; the suite reports `ERROR`, not `OK`.

- [ ] **Step 3: Implement the validator**

Implement `scripts/validate-document-taxonomy.py` exporting the three functions
plus a `main` that gathers tracked paths through `git ls-files`, groups Stage 03
directories, and exits non-zero with one diagnostic line per violation in the
repository's existing `FAIL <CODE> <path> ...` format.

- [ ] **Step 4: Run the tests to verify they pass**

```bash
python3 -m unittest discover -s tests -p test_validate_document_taxonomy.py -v
```

Expected: `Ran 9 tests` and `OK`.

- [ ] **Step 5: Retire the date-based rule**

Delete the sentence "Stage 04 plans and tasks stay date-based execution
records." from `docs/00.agent-governance/rules/stage-authoring-matrix.md`,
`docs/00.agent-governance/rules/document-stage-routing.md`, and
`docs/99.templates/support/sdlc-governance.md`. Replace it in the authoring
matrix only with:

```markdown
- Stage 03 work units hold `spec.md`, `plan.md`, and `tasks.md` in one folder.
  Authored filenames carry no date; the date lives in frontmatter `updated`.
```

```bash
git ls-files -z | xargs -0 grep -n 'date-based execution records' | grep -v '^docs/98.archive/'
```

Expected: no output.

- [ ] **Step 6: Declare the validator, run the gate, and commit**

Add a `document-taxonomy` entry to
`docs/00.agent-governance/contracts/validation-surfaces.json` with lanes
`affected`, `staged`, `all-files`, `ci`, `optional: false`, and
`evidenceLane: repo-static`.

```bash
bash scripts/validate-repo-quality-gates.sh .
git add -A
git commit -m "feat: enforce work-unit locality, filename dates, and stage sequence

Add one validator for the taxonomy rule family and retire the date-based
execution record rule from the three documents that restated it."
```

---

### Task 10: WDTC-009 — add lineage frontmatter and reciprocal validation

**Files:**

- Modify: all 48 `docs/03.specs/*/spec.md` frontmatter
- Modify: `scripts/validate-document-taxonomy.py`
- Modify: `tests/test_validate_document_taxonomy.py`
- Modify: `docs/99.templates/templates/sdlc/specs/spec.template.md`
- Modify: `docs/99.templates/support/document-profiles.json`

**Interfaces:**

- Consumes: `validate_work_unit_locality` and friends from WDTC-008.
- Produces: `validate_lineage(specs, upstream_links)` returning a tuple of
  diagnostics, empty on success.

- [ ] **Step 1: Write the failing tests**

```python
class LineageTest(unittest.TestCase):
    def test_accepts_reciprocal_lineage(self):
        specs = {"052-a": {"lineage": "PRD-008", "ard": "ARD-0011"}}
        upstream = {"PRD-008": {"052-a"}, "ARD-0011": {"052-a"}}
        self.assertEqual(validate_lineage(specs, upstream), ())

    def test_rejects_unresolvable_identifier(self):
        specs = {"052-a": {"lineage": "PRD-999", "ard": "ARD-0011"}}
        upstream = {"ARD-0011": {"052-a"}}
        self.assertEqual(len(validate_lineage(specs, upstream)), 1)

    def test_rejects_missing_back_link(self):
        specs = {"052-a": {"lineage": "PRD-008", "ard": "ARD-0011"}}
        upstream = {"PRD-008": set(), "ARD-0011": {"052-a"}}
        self.assertEqual(len(validate_lineage(specs, upstream)), 1)

    def test_rejects_absent_required_field(self):
        specs = {"052-a": {"ard": "ARD-0011"}}
        upstream = {"ARD-0011": {"052-a"}}
        self.assertEqual(len(validate_lineage(specs, upstream)), 1)
```

Bind the new symbol through the existing loader at the top of the test file:
`validate_lineage = _m.validate_lineage`. Do not add a plain `import`; the
validator filename is hyphenated and is not an importable module name.

- [ ] **Step 2: Run the tests to verify they fail**

```bash
python3 -m unittest tests.test_validate_document_taxonomy.LineageTest -v
```

Expected: `AttributeError: module has no attribute 'validate_lineage'`.

- [ ] **Step 3: Implement `validate_lineage` and backfill the frontmatter**

Add the function, then add `lineage` and `ard` to every Stage 03 `spec.md`
frontmatter using the existing Traceability bullets as the source of truth. Add
the two keys to `spec.template.md` and to the `sdlc/spec` profile's required
frontmatter in `document-profiles.json`.

- [ ] **Step 4: Run the tests and the validator**

```bash
python3 -m unittest discover -s tests -p test_validate_document_taxonomy.py -v
python3 scripts/validate-document-taxonomy.py --root .
```

Expected: `Ran 13 tests` and `OK`, validator PASS. A `LINEAGE-NO-BACKLINK` diagnostic names a
specification whose upstream document does not list it; fix the upstream
document rather than removing the field.

- [ ] **Step 5: Run the gate and commit**

```bash
bash scripts/validate-repo-quality-gates.sh .
git add -A
git commit -m "feat: declare and validate cross-stage lineage in frontmatter

Add required lineage and ard fields to every Stage 03 specification and enforce
that each declared upstream owner links back. Per-stage identifier sequences
stay independent; the lineage is now resolvable without reading prose."
```

---

### Task 11: WDTC-010 — collapse the authoring-rule documents

**Files:**

- Create: `docs/00.agent-governance/rules/document-authoring.md`
- Create: `docs/99.templates/support/document-contract.md`
- Create: `docs/99.templates/support/document-lifecycle.md`
- Delete: the ten superseded rule documents
- Modify: every file linking to them

**Interfaces:**

- Consumes: WDTC-009's completed contract set.
- Produces: three rule owners that WDTC-013 amends.

- [ ] **Step 1: Build the rule inventory**

For each of the ten documents, list every normative sentence and assign it to
exactly one of the three target owners. A sentence assigned to two targets is a
duplicate; keep the more specific owner and delete the other. Record the
inventory in the task document as evidence.

- [ ] **Step 2: Author the three owners**

Use `docs/99.templates/templates/common/governance-reference.template.md` for
the Stage 00 document and
`docs/99.templates/templates/common/template-support.template.md` for the two
Stage 99 documents. Each keeps an Authority Boundary section that names
adjacent owners without restating their rules.

- [ ] **Step 3: Delete the superseded documents and rewrite links**

```bash
git rm docs/00.agent-governance/rules/stage-authoring-matrix.md \
       docs/00.agent-governance/rules/document-stage-routing.md \
       docs/00.agent-governance/rules/stage-checklists.md \
       docs/00.agent-governance/rules/documentation-protocol.md \
       docs/99.templates/support/documentation-contract.md \
       docs/99.templates/support/template-routing.md \
       docs/99.templates/support/frontmatter-schema.md \
       docs/99.templates/support/common-documentation-governance.md \
       docs/99.templates/support/sdlc-governance.md \
       docs/99.templates/support/legacy-cleanup-rules.md
```

Rewrite every inbound link, including those in `CLAUDE.md`, `AGENTS.md`,
`GEMINI.md`, `.claude/CLAUDE.md`, the bootstrap and checklist documents, and
the provider notes.

- [ ] **Step 4: Prove rule uniqueness**

```bash
python3 scripts/validate-document-taxonomy.py --root . --check rule-uniqueness
```

Expected: PASS. Implement the check as a normative-sentence hash comparison
across the three owners, reporting any sentence that appears in more than one.

- [ ] **Step 5: Run the gate and commit**

```bash
bash scripts/validate-repo-quality-gates.sh .
git add -A
git commit -m "refactor: collapse ten authoring-rule documents into three

Assign every normative sentence to exactly one of stage authoring, template
contract, or document lifecycle, and delete the superseded documents. Authority
Boundary sections now name adjacent owners instead of restating their rules."
```

---

### Task 12: WDTC-011 — remove the template mirror profiles

**Files:**

- Modify: `docs/99.templates/support/document-profiles.json`
- Modify: `docs/99.templates/support/document-profiles.schema.json`
- Modify: `scripts/validate-document-contract-registry.py`

**Interfaces:**

- Consumes: WDTC-010's rule owners.
- Produces: a registry with one profile per authored document type.

- [ ] **Step 1: Capture route coverage before the change**

```bash
python3 scripts/validate-document-contract-registry.py --root . --mode strict \
  > /tmp/wdtc-011-before.txt
git ls-files '*.md' > /tmp/wdtc-011-paths.txt
wc -l /tmp/wdtc-011-paths.txt
```

Record the path count and the `uncovered=0 ambiguous=0` line.

- [ ] **Step 2: Remove the 24 `template/*` profiles**

Delete each `template/*` profile and route the template forms under
`docs/99.templates/templates/**` to their corresponding authored profile with a
`templateForm: true` flag that relaxes only the body-traceability requirement,
since a template form has no real upstream document to link.

- [ ] **Step 3: Prove coverage is unchanged**

```bash
python3 scripts/validate-document-contract-registry.py --root . --mode strict \
  > /tmp/wdtc-011-after.txt
diff <(grep -o 'uncovered=[0-9]*\|ambiguous=[0-9]*' /tmp/wdtc-011-before.txt) \
     <(grep -o 'uncovered=[0-9]*\|ambiguous=[0-9]*' /tmp/wdtc-011-after.txt)
```

Expected: no difference, both `uncovered=0 ambiguous=0`, and the same total path
count. A dropped path is a coverage regression and blocks the commit.

- [ ] **Step 4: Run the gate and commit**

```bash
bash scripts/validate-repo-quality-gates.sh .
git add -A
git commit -m "refactor: validate template forms against their authored profile

Remove the 24 template mirror profiles and route each template form to its
corresponding authored profile with body-traceability relaxed. Route coverage
is unchanged: the same path inventory reports uncovered=0 ambiguous=0."
```

---

### Task 13: WDTC-012 — consolidate the agent governance contracts

**Files:**

- Modify: `docs/00.agent-governance/contracts/*.json`
- Modify: the validators that read them
- Modify: `docs/00.agent-governance/providers/claude.md`, `codex.md`,
  `gemini.md`, `agents-md.md`

**Interfaces:**

- Consumes: WDTC-011's registry.
- Produces: a smaller contract set with an unchanged assertion set.

> This is the highest-risk package. It occupies one commit and is revertible
> without disturbing any predecessor. If it cannot reach a passing gate within
> three attempts, revert it, record it as deferred in the task document, and
> continue with WDTC-013.

- [ ] **Step 1: Capture the assertion inventory before the change**

```bash
python3 -m unittest discover -s tests -p 'test_*.py' > /tmp/wdtc-012-before.txt 2>&1
tail -3 /tmp/wdtc-012-before.txt
```

Record the `Ran N tests` count and the exact failure and error list. Both form
the floor: consolidation may not reduce the count or add a new entry to the
list.

- [ ] **Step 2: Merge the role evaluation contracts**

Merge `agent-evaluations.json`, `agent-model-fitness.json`, and
`agent-roster-admission.json` into one `agent-roster.json` with three top-level
sections, and merge their three schemas into `agent-roster.schema.json`.
Update `validate-agent-evaluations.py`, `validate-agent-model-fitness.py`, and
`validate-agent-roster-admission.py` to read the merged document, keeping each
validator's assertions intact.

- [ ] **Step 3: Prove the assertion set is unchanged**

```bash
python3 -m unittest discover -s tests -p 'test_*.py' > /tmp/wdtc-012-after.txt 2>&1
tail -3 /tmp/wdtc-012-after.txt
```

Expected: the `Ran N tests` count is at or above the Step 1 floor and the
failure and error list is unchanged. A lower count means an assertion was
lost; a new list entry means the merge broke something. Either blocks the
commit.

- [ ] **Step 4: Record the size delta**

```bash
git show HEAD:docs/00.agent-governance/contracts/agent-evaluations.json | wc -l
wc -l docs/00.agent-governance/contracts/agent-roster.json
```

Record before and after line counts in the task document.

- [ ] **Step 5: Run the gate and commit**

```bash
bash scripts/validate-repo-quality-gates.sh .
git add -A
git commit -m "refactor: merge the role evaluation contracts into one owner

Merge the evaluation, model-fitness, and roster-admission contracts and their
schemas into a single roster contract. The assertion set is unchanged: the test
suite passes at or above its pre-merge count."
```

---

### Task 14: WDTC-013 — disposition the documentation gaps

**Files:**

- Modify: `docs/99.templates/support/document-profiles.json` (DOC-G1)
- Modify: `docs/99.templates/templates/sdlc/operations/guide.template.md` (G1)
- Modify: `docs/99.templates/support/document-lifecycle.md` (G2, G3, G4, G5)
- Create: `docs/04.operations/policies/0008-incident-postmortem-policy.md` (G6)
- Modify: `docs/90.references/research/2026-07-07-wer/document-type-format-and-evidence-contract.md` (G8, G9)
- Modify: `docs/99.templates/templates/sdlc/operations/runbook.template.md` (G10)

**Interfaces:**

- Consumes: WDTC-010's `document-lifecycle.md`.
- Produces: a closed gap ledger for WDTC-015 to cite.

- [ ] **Step 1: Constrain the guide type enumeration (DOC-G1)**

Add `"enum": ["how-to", "tutorial", "concept"]` to the `Guide Type` heading
value constraint in the `sdlc/guide` profile, and state the three values in
`guide.template.md`. All eight existing guides declare `how-to` and remain
valid.

- [ ] **Step 2: Record the deliberate absences (DOC-G2, G3, G5)**

Add to `document-lifecycle.md`:

```markdown
### Deliberately absent document routes

No tutorial route, explanation route, or release-notes route exists. Diátaxis
states that empty structures must not be created in advance; a route with no
instance is exactly that. Release notes are additionally out of scope because
this repository declares no public API and has zero references to a release
document. Create any of these routes only when a first real instance exists.
```

- [ ] **Step 3: Make the guide-runbook boundary decidable (DOC-G4)**

Add to `document-lifecycle.md`:

```markdown
### Guide versus runbook

A document is a runbook when it is executed in response to an alert or incident
and requires a verification step and a rollback or recovery path. Otherwise it
is a guide. Extend the active-surface duplicate rule to the operations stage:
no two live operations documents may own the same procedure for the same
system.
```

- [ ] **Step 4: Define the postmortem triggers (DOC-G6)**

Author `docs/04.operations/policies/0008-incident-postmortem-policy.md` from
`policy.template.md`, defining observable triggers in advance: any
customer-visible outage, any incident requiring a second responder, and any
incident unresolved after one hour. Cite the SRE primary source already
recorded in the Stage 90 reference.

- [ ] **Step 5: Add the observed-text boundaries (DOC-G8, G9)**

In the format ledger, annotate the ARD row with "ISO/IEC/IEEE 42010 normative
text not observed; catalog page returned HTTP 403 on 2026-08-07" and relabel
the PRD row's standard reference as an inference rather than a grounded
mapping.

- [ ] **Step 6: Add the runbook automation counter-rule (DOC-G10)**

Add to `runbook.template.md` under the procedure heading:

```markdown
<!-- Author prompt: a deterministic command sequence run on every occurrence
belongs in automation, not here. Record the decision to automate instead. -->
```

- [ ] **Step 7: Run the gate and commit**

```bash
bash scripts/validate-repo-quality-gates.sh .
git add -A
git commit -m "docs: disposition the ten recorded documentation gaps

Implement controls for the guide type enumeration, guide-runbook boundary,
postmortem triggers, observed-text boundaries, and runbook automation
counter-rule. Record evidence-backed decisions not to create tutorial,
explanation, or release-notes routes."
```

---

### Task 15: WDTC-014 — reconcile the script surface

**Files:**

- Modify: `docs/00.agent-governance/contracts/validation-surfaces.json`
- Modify: `scripts/validate-document-taxonomy.py`
- Modify: `tests/test_validate_document_taxonomy.py`
- Modify: `scripts/README.md`

**Interfaces:**

- Consumes: the final validator set from WDTC-012 and WDTC-013.
- Produces: `validate_enforcement_closure(declared, executable)` returning a
  tuple of diagnostics, empty on success.

- [ ] **Step 1: Write the failing tests**

```python
class EnforcementClosureTest(unittest.TestCase):
    def test_accepts_equal_sets(self):
        s = frozenset({"scripts/a.py", "scripts/b.py"})
        self.assertEqual(validate_enforcement_closure(s, s), ())

    def test_rejects_undeclared_executable(self):
        declared = frozenset({"scripts/a.py"})
        executable = frozenset({"scripts/a.py", "scripts/b.py"})
        self.assertEqual(
            len(validate_enforcement_closure(declared, executable)), 1
        )

    def test_rejects_missing_executable(self):
        declared = frozenset({"scripts/a.py", "scripts/b.py"})
        executable = frozenset({"scripts/a.py"})
        self.assertEqual(
            len(validate_enforcement_closure(declared, executable)), 1
        )
```

- [ ] **Step 2: Run the tests to verify they fail**

```bash
python3 -m unittest tests.test_validate_document_taxonomy.EnforcementClosureTest -v
```

Expected: `AttributeError: module has no attribute
'validate_enforcement_closure'`. Bind it with
`validate_enforcement_closure = _m.validate_enforcement_closure` after
implementing it.

- [ ] **Step 3: Implement the check and enumerate the current gap**

```bash
python3 scripts/validate-document-taxonomy.py --root . --check enforcement-closure
```

The check reports every undeclared executable and every declared-but-missing
validator. Resolve each one by declaring it with its correct lane, merging it
into a sibling validator, or deleting it with its rule. Helper modules that are
imported rather than executed are declared as `library: true` and excluded from
the equality check.

- [ ] **Step 4: Run the tests and the gate**

```bash
python3 -m unittest discover -s tests -p test_validate_document_taxonomy.py -v
bash scripts/validate-repo-quality-gates.sh .
```

Expected: all tests pass and the gate passes.

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "feat: enforce equality between declared and executable validators

Add an enforcement closure check and reconcile the script surface with the
validator selection contract, so no validator exists outside a declared lane
and no declared lane names a missing validator."
```

---

### Task 16: WDTC-015 — measure, review, and close

**Files:**

- Modify: `docs/03.specs/052-document-taxonomy-consolidation/tasks.md`
- Modify: `docs/03.specs/052-document-taxonomy-consolidation/spec.md`
- Modify: `docs/03.specs/052-document-taxonomy-consolidation/plan.md`
- Modify: `docs/01.requirements/008-workspace-document-taxonomy-consolidation.md`
- Modify: `docs/00.agent-governance/memory/progress.md`

**Interfaces:**

- Consumes: every predecessor package.
- Produces: the closure evidence PRD-008 requires.

- [ ] **Step 1: Record the per-asset deltas**

```bash
python3 - <<'PY'
import subprocess
BASE = "dd54f844"
assets = [
  "docs/00.agent-governance/memory/progress.md",
  "docs/99.templates/support/document-profiles.json",
]
for a in assets:
    old = subprocess.run(["git", "show", f"{BASE}:{a}"],
                         capture_output=True, text=True).stdout
    new = open(a).read()
    print(f"{a}: {len(old.splitlines())} -> {len(new.splitlines())}")
PY
```

Extend the asset list to cover every R-1 through R-7 item, including deleted
assets recorded as a delta to zero. Write the table into `tasks.md`.

- [ ] **Step 2: Verify every success criterion**

Walk VAL-WDTC-001 through VAL-WDTC-011 and record the observed evidence for
each in the `tasks.md` Lifecycle Traceability table. A criterion with no
evidence blocks closure.

- [ ] **Step 3: Prove archive inviolability**

```bash
git diff --name-only dd54f844..HEAD -- docs/98.archive/ | grep -v '^docs/98.archive/.*archive' || true
python3 scripts/archive_validation.py --root .
```

Expected: only newly added archive records appear, no existing record is
modified, and validation passes.

- [ ] **Step 4: Request independent review**

Dispatch a code review over the full program diff, checking archive
inviolability, rule uniqueness, enforcement closure, and evidence-lane honesty.
Record the disposition in `tasks.md`.

- [ ] **Step 5: Close the lifecycle**

Set `status: done` on the Spec 052 triad and `status: done` on PRD-008 and
ARD-0011. Add a closure entry to
`docs/00.agent-governance/memory/progress.md`. Restore PRD-007 to `active` and
Spec 047 to `draft`, ready for resumption, and record the resumption note.

- [ ] **Step 6: Run the gate and commit**

```bash
bash scripts/validate-repo-quality-gates.sh .
git add -A
git commit -m "docs: close the document taxonomy consolidation program

Record per-asset reduction deltas, verify every success criterion, prove
archive inviolability across the whole program diff, and resume the delivery
assurance program in the consolidated structure."
```

## Verification Plan

| Work package | Deterministic check                                                                         | Evidence lane |
| ------------ | ------------------------------------------------------------------------------------------- | ------------- |
| WDTC-000     | `bash scripts/validate-repo-quality-gates.sh .`                                             | repo-static   |
| WDTC-001     | Zero-referent grep plus the full gate                                                       | repo-static   |
| WDTC-002     | `python3 scripts/archive_validation.py --root .` plus the full gate                         | repo-static   |
| WDTC-003     | `python3 scripts/archive_recovery.py --list` plus archive validation                        | repo-static   |
| WDTC-004     | Status enumeration, archive validation, and the full gate                                   | repo-static   |
| WDTC-005     | `python3 -m unittest discover -s tests -p test_migrate_document_paths.py -v`                                 | repo-static   |
| WDTC-006     | Dry-run exit code, zero live `04.execution` hits, full gate                                 | repo-static   |
| WDTC-007     | Zero live `05.operations` hits outside annotated Stage 90 text, full gate                   | repo-static   |
| WDTC-008     | `python3 -m unittest discover -s tests -p test_validate_document_taxonomy.py -v`, zero retired-sentence hits | repo-static   |
| WDTC-009     | Lineage validator over the full corpus                                                      | repo-static   |
| WDTC-010     | Rule-uniqueness check                                                                       | repo-static   |
| WDTC-011     | Route coverage diff before and after                                                        | repo-static   |
| WDTC-012     | Test count floor comparison                                                                 | repo-static   |
| WDTC-013     | Per-gap evidence link in the task table                                                     | repo-static   |
| WDTC-014     | Enforcement closure check                                                                   | repo-static   |
| WDTC-015     | Full criterion walk plus independent review                                                 | repo-static   |

Every lane above is repository-static. Hosted CI, provider-runtime, remote, and
live evidence are `DEFER` for this program and are not claimed anywhere.

## Risks & Mitigations

| Risk                                                           | Owner               | Mitigation                                                                                                                              |
| -------------------------------------------------------------- | ------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| A path rewrite touches an archive record and breaks its digest | Governance steward  | The migration tool aborts before any write when either endpoint falls inside an exclusion prefix; WDTC-005 tests that abort explicitly. |
| A regular-expression rewrite matches an unintended path        | Platform maintainer | The tool performs no inference; every substitution is enumerated per moved file.                                                        |
| Rewriting a dated Stage 90 observation falsifies the record    | Technical writer    | WDTC-007 rewrites navigational links only and annotates observation text instead of changing it.                                        |
| Contract consolidation silently drops an assertion             | Quality engineer    | WDTC-012 compares the passing test count against a pre-merge floor and reverts if it drops.                                             |
| Profile reduction drops route coverage                         | Quality engineer    | WDTC-011 diffs `uncovered` and `ambiguous` against the same path inventory.                                                             |
| Rule consolidation loses a normative sentence                  | Governance steward  | WDTC-010 builds a sentence-level inventory before deleting any source document and records it as evidence.                              |
| Progress rotation loses recoverable history                    | Governance steward  | WDTC-003 verifies recovery through `archive_recovery.py` before truncating.                                                             |
| The suspended program resumes against a stale surface          | Platform maintainer | WDTC-015 restores PRD-007 only after the consolidated structure is closed, and records the resumption note.                             |

## Completion Criteria

- Every work package WDTC-000 through WDTC-015 is committed with a passing
  repository quality gate.
- No live path contains `04.execution` or `05.operations` outside
  `docs/98.archive/**` and annotated Stage 90 historical observations.
- No authored filename under stages 01 through 04 begins with a date.
- Every Stage 03 specification declares resolvable, reciprocal lineage.
- Three documents own the authoring rules and no rule is stated twice.
- The declared and executable validator sets are equal.
- Every reduced asset has a recorded before-and-after line count.
- Every documentation gap has an implemented control or a dated decision.
- Archive validation passes and no existing archive record was modified.
- PRD-007 is restored with a recorded resumption note.

No live cluster, hosted CI, provider-runtime, remote, or credential-bearing
evidence is produced or claimed by this plan.

## Traceability

- **Specification**:
  [Spec 052](../../03.specs/052-document-taxonomy-consolidation/spec.md)
- **Program requirement**:
  [PRD-008](../../01.requirements/008-workspace-document-taxonomy-consolidation.md)
- **Architecture**:
  [ARD-0011](../../02.architecture/requirements/0011-document-taxonomy-consolidation-architecture.md)
- **Execution Task**:
  [Task: Document Taxonomy Consolidation](../tasks/2026-08-07-document-taxonomy-consolidation.md)

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-WDTC-001](../../03.specs/052-document-taxonomy-consolidation/spec.md#success-criteria--verification-plan) | WDTC-004, WDTC-005, WDTC-006 | [Mapping, dry-run change set, and post-migration work-unit inventory evidence](../tasks/2026-08-07-document-taxonomy-consolidation.md#task-table) |
| N/A — VAL-WDTC-002 shares the Spec source above | WDTC-006, WDTC-008 | [Filename inventory and frontmatter preservation diff evidence](../tasks/2026-08-07-document-taxonomy-consolidation.md#task-table) |
| N/A — VAL-WDTC-003 shares the Spec source above | WDTC-007 | [Reference counts before and after with the enumerated archive exclusion set](../tasks/2026-08-07-document-taxonomy-consolidation.md#task-table) |
| N/A — VAL-WDTC-004 shares the Spec source above | WDTC-009 | [Reciprocal lineage validation evidence over the full Stage 03 corpus](../tasks/2026-08-07-document-taxonomy-consolidation.md#task-table) |
| N/A — VAL-WDTC-005 shares the Spec source above | WDTC-008, WDTC-010 | [Retired-sentence search and sentence-level rule inventory evidence](../tasks/2026-08-07-document-taxonomy-consolidation.md#task-table) |
| N/A — VAL-WDTC-006 shares the Spec source above | WDTC-001, WDTC-003, WDTC-011, WDTC-012 | [Consolidated per-asset reduction delta table](../tasks/2026-08-07-document-taxonomy-consolidation.md#task-table) |
| N/A — VAL-WDTC-007 shares the Spec source above | WDTC-013 | [Per-gap implemented control or dated recorded decision evidence](../tasks/2026-08-07-document-taxonomy-consolidation.md#task-table) |
| N/A — VAL-WDTC-008 shares the Spec source above | WDTC-014 | [Declared-versus-executable enforcement closure evidence](../tasks/2026-08-07-document-taxonomy-consolidation.md#task-table) |
| N/A — VAL-WDTC-009 shares the Spec source above | WDTC-002, WDTC-003, WDTC-004, WDTC-015 | [Archive validation result and zero-modification archive diff evidence](../tasks/2026-08-07-document-taxonomy-consolidation.md#task-table) |
| N/A — VAL-WDTC-010 shares the Spec source above | WDTC-000, WDTC-015 | [Suspension and resumption status diff evidence](../tasks/2026-08-07-document-taxonomy-consolidation.md#task-table) |
| N/A — VAL-WDTC-011 shares the Spec source above | All packages | [Per-commit repository quality gate result evidence](../tasks/2026-08-07-document-taxonomy-consolidation.md#task-table) |
