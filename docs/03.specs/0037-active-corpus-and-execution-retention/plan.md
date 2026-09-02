---
title: 'Active Corpus and Execution Retention Implementation Plan'
version: "1.0.0"
type: sdlc/plan
layer: "specs"
status: done
owner: platform
updated: 2026-07-19
artifact_id: "SPEC-0037-PLAN-0001"
---

# Active Corpus and Execution Retention Implementation Plan

## Overview

This Plan records Spec 037 execution in six dependency-ordered packages. It replaces
folder-size assumptions with a closed census and disposition contract, moves
only eligible closed-lineage execution records into full-body archive records,
and audits Stage 05 and helper Tests for role ownership without fabricating
operational evidence.

The activation baseline and rollback parent are
`a12aedfb71ccabd329dabc83bd2863474d1126b0`. Predecessor Spec 036 closed in
commit `855fa78`; repository-static postflight corrections `cdac53c` and
`a12aedf` made that committed closure the current planning input. This
activation changes documentation lineage only. It does not classify a Plan or
Task as archive-eligible, move a record, or claim a validator result.

Fresh independent planning-activation reviews returned exact verdicts
`REQUIREMENTS COMPLIANT` and `QUALITY APPROVED`, with no findings. Those
verdicts approved the original active execution decomposition only. ACER-001
through ACER-005 later completed with the reviewed evidence recorded in the
reciprocal Task. ACER-006 now records the committed terminal closure: the
Plan/Task pair is done and retained as owned Stage 04 `DEFER` evidence until
exact successor migration evidence exists. Exact local staged QA passed the
focused, residue, lifecycle, strict document, archive, aggregate,
changed-file pre-commit, and cached diff gates. Initial independent
requirements and quality reviews required changes; the remediated proposal
then received `REQUIREMENTS COMPLIANT` and `QUALITY APPROVED` with no blocking
findings. Raw all-files pre-commit remains bounded by the Spec 039-owned
`os.mkfifo` `Errno 95`; no FIFO or CI success is claimed. Closure content
commit `cfabc50681008cf0991c004f07efa17516eeed3c`, clean status, and clean-tree
postflight are observed. Final staged terminal reviewers returned
`REQUIREMENTS COMPLIANT` and `QUALITY APPROVED` with no findings. This
evidence-update commit is unidentified and unclaimed.

## Context

The parent `a12aedf` activation input is 54 Plans plus 56 Tasks, for 110
documents. The frozen Spec 037 design baseline covers 104 records (51 Plans
plus 53 Tasks). Six later records are the three reciprocal Plan/Task pairs
created for Specs 034, 035, and 036. At activation, this staged pair raised the
proposed corpus to 55 Plans plus 57 Tasks, or 112 documents. ACER-001 reconciled
the 104-record baseline and six-record delta in one closed census before any
candidate became eligible; the new Spec 037 pair was then a retained active
control, not a migration candidate. The current done pair is terminal owned
`DEFER` evidence with no active execution authority. Its reason is
`terminal-spec-037-lineage-awaiting-successor-migration-evidence`, and its
refresh trigger is `exact-successor-migration-evidence-change`.

The prior Stage 05 input contains 24 authored documents: eight Guides, seven
Policies, and nine Runbooks. There are zero real authored Incident records and
zero real authored Postmortem records. Empty event collections are valid until
a real event exists, so this Plan forbids synthetic records. The earlier helper
Tests inventory is also an input to ACER-001 and ACER-004, but must be
recomputed against the current tracked corpus before it can support a PASS or
remediation claim.

Accepted ADRs and done Specs can remain current authority. Terminal state,
file age, and folder count are never sufficient archive predicates. Spec 039
owns CI integration and the known all-files FIFO portability boundary. Specs
038 and 040 remain active design contracts without Plan/Task activation.

### Legacy Task ledger inputs

This Task is the execution, verification, review, and rollback ledger for
ACER-001 through ACER-006. At activation it tracked the reciprocal Spec 037
execution pair from repository baseline
`a12aedfb71ccabd329dabc83bd2863474d1126b0`.
ACER-001 is complete in content logical commit `46b79fc`; ACER-002 is complete
in content logical commit `414905c`. ACER-003 is complete with independently
approved atomic lineage commits `28b42e7`, `9c18910`, `96176a9`, `20cb1ca`,
`52d4c2b`, and `24abe70`. No eligible lineage batch remains. ACER-004 local
implementation is complete in content logical commit `a646df1` with final
independent approval and clean-tree postflight. ACER-005 local implementation
is complete in content logical commit `ba4a470` with final independent approval,
scanner-clean applicable pre-commit, and clean-tree postflight. ACER-006 is Done
for the terminal closure committed in
`cfabc50681008cf0991c004f07efa17516eeed3c` after focused RED/GREEN and exact
descriptor-backed object preparation. Exact local stage-zero assembly, staged
QA, final staged closure reviews, clean status, and clean-tree postflight are
observed below. This evidence-update commit is unidentified and unclaimed.

The parent `a12aedf` activation input records 54 authored Plans plus 56 authored
Tasks, for 110 candidates. The reciprocal pair originally raised the proposed
corpus to 55 Plans and 57 Tasks (112 records). It is now a complete terminal
Stage 04 pair retained as owned `DEFER` evidence, not active execution authority.
ACER-001 reconciled the frozen 104-record baseline with the
six later records created for Specs 034 through 036. No candidate is eligible
merely because it is terminal, old, or counted. The prior Stage 05 input is 24
authored records (eight Guides, seven Policies, and nine Runbooks), with zero
real authored Incident and Postmortem records. The earlier helper Tests
inventory is an input to recompute rather than activation PASS evidence.

- [Active Corpus and Execution Retention Implementation Plan](plan.md)
- [Spec 037](spec.md)
- [PRD-0006](../../01.requirements/0006-workspace-document-lifecycle-and-evidence-consolidation.md)
- [AD-0009](../../02.architecture/descriptions/0009-document-lifecycle-evidence-operating-model.md)
- [ADR-0018](../../02.architecture/decisions/0018-full-body-archive-record-and-retention.md)
- [Archive index](../../98.archive/README.md)
- `docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md`; [current lookup](../../90.references/research/0001-workspace-engineering/m0012-source-coverage.md)
- [Predecessor Spec 036 execution history](../../98.archive/README.md#document-index)
## Goals & In-Scope

- Produce a closed 110-record pre-activation Stage 04 candidate census that
  reconciles the frozen 104 baseline with the six later execution records and
  gives every row an owned `eligible`, `retain`, or `DEFER` disposition; record
  that the Spec 037 pair was the separate active control at activation, then
  preserve its done records as terminal owned `DEFER` without active authority.
- Implement fail-closed eligibility and active-residue validation, including
  explicit closure, current-consumer, source-recovery, link, rollback, and
  exception evidence predicates.
- Migrate eligible records atomically by lineage with full-body archive
  payloads, current index/link repair, durable ledger evidence, and a bounded
  rollback commit for each batch.
- Audit the 24-document Stage 05 input and recomputed helper Tests inventory
  for role overlap, stale current claims, copied template residue, and owner
  gaps while preserving real facts.
- Close the tranche only when every census row and active residue has a
  validated disposition or an owned bounded DEFER.

## Non-Goals & Out-of-Scope

- Moving accepted ADRs or still-current done Specs solely because they are
  terminal, old, or numerous.
- Deleting or archiving by age, count, naming pattern, or subjective staleness
  without lineage and authority evidence.
- Fabricating Incident, Postmortem, live operations, provider, remote, cluster,
  Vault, ESO, Argo CD, or secret evidence.
- Modifying CI workflow or pre-commit FIFO handling; Spec 039 owns that work.
- Activating Plans or Tasks for Specs 038 or 040, or performing the final
  program cutover owned by Spec 040.
- Listing, traversing, opening, hashing, moving, or deleting ignored
  `_workspace` children.

## Work Breakdown

| ID | Work package | Depends on | Entry gate | Exit evidence |
| --- | --- | --- | --- | --- |
| ACER-001 | Closed census and disposition contract for the 104-record baseline plus six-record delta | None | Reciprocal Spec 037 Plan/Task activation is valid at parent `a12aedf` | Exact parent 54-Plan/56-Task census and proposed 55-Plan/57-Task control; 104+6 candidate reconciliation; current Stage 05 and helper Tests recomputation; every candidate row has a closed disposition vocabulary and owner |
| ACER-002 | Fail-closed eligibility, residue validator, and dry-run ledger | ACER-001 | Reviewed census schema and explicit evidence predicates | Negative fixtures deny terminal/age/count-only movement; dry run emits deterministic eligible/retain/DEFER rows; unexplained residue fails |
| ACER-003 | Atomic per-lineage full-body archive migration batches | ACER-002 | Eligible rows have source, consumer, link, recovery, and rollback proof | Each batch atomically creates archive payload/index evidence, repairs current links, removes the active execution source, records the ledger row, validates, reviews, and commits |
| ACER-004 | Stage 05 and helper Tests role audit with bounded remediation | ACER-001 | Current 24-document operations input and helper Tests corpus are recomputed | Role/profile/current-owner findings have repo-backed evidence; approved bounded fixes land without synthetic events or execution-tracker duplication |
| ACER-005 | Residual retain/DEFER closure and cardinality enforcement | ACER-003, ACER-004 | All eligible migration batches and role remediations are reviewed | Zero unexplained closed-lineage done Plan/Task residue; every retained or DEFER row has reason, owner, trigger, and current authority; cardinality gates pass |
| ACER-006 | Full QA, independent review, and atomic lifecycle closure | ACER-005 | All package commits and durable evidence are present | Repository-static QA, fresh requirements and quality reviews, exact Spec/Plan/Task/index/registry/ledger closure proposal, logical commit, and postflight evidence |

## Verification Plan

| Lane | Focused evidence | Required result |
| --- | --- | --- |
| Inventory | Closed Stage 04/05/helper census and delta reconciliation | Parent 54 Plans plus 56 Tasks equals 110 and 104 baseline plus six delta equals that candidate set; at activation the separate control pair yielded proposed 55/57, and it is now terminal owned `DEFER`; Stage 05 input is 8/7/9 with zero real Incident/Postmortem records |
| Eligibility | Predicate and hostile negative fixtures | No default eligible state; age/count/terminal-only, ambiguous lineage, current consumption, missing source, broken links, or missing rollback proof fail closed |
| Migration | Dry run, per-lineage batch check, and archive integrity | Source removal and full-body archive creation, index/link repair, ledger evidence, provenance, digest, historical links, and rollback are atomic |
| Residue | Active-stage cardinality and ledger join | No unexplained eligible residue; every retain/DEFER record has a bounded reason, owner, and refresh trigger |
| Operations and helper Tests | Profile/owner/content/current-implementation audit | Zero unsupported role overlap, copied prompt residue, stale claim, synthetic event, or unowned exception |
| Repository | Staged lifecycle, strict registry/Markdown/cross-document, changed Markdownlint, diff check, aggregate and applicable pre-commit lanes | Deterministic local PASS, with the Spec 039-owned FIFO condition recorded only in its existing bounded lane |
| Review | Fresh requirements review followed by quality review per package and closure | Blocking findings remediated before each logical commit and before terminal closure |

### Legacy Task verification evidence

The intentional activation RED staged only the new Plan. The lifecycle
validator exited 1 with `LIFECYCLE-CREATE`: it expected exactly one active Plan
and one active Task creation and observed `Plan count 1, Task count 0`. The
complete seven-file activation proposal adds the reciprocal Task, updates Spec
037 and the three indexes, and updates/adds the three exact 14-column ledger
records. The registry relation was already active and is unchanged.

Local activation GREEN is repository-static and staged: lifecycle validation
passes; the registry self-test passes 119 cases and strict mode classifies 436
paths (`baseline=433`, `new=65`, two programs, uncovered 0, ambiguous 0);
strict Markdown reports zero violations; strict cross-document validation is
valid; changed-file Markdownlint and `git diff --cached --check` pass. The exact
proposal contains seven staged paths and zero unstaged paths. JSON validation
is not applicable because this activation changes no JSON file.

Fresh independent activation requirements review returned exact verdict
`REQUIREMENTS COMPLIANT`; activation quality review returned exact verdict
`QUALITY APPROVED`; findings were none. That remains planning activation
approval, not package or closure approval. Fresh ACER-001 implementation
re-review separately returned exact verdicts `REQUIREMENTS COMPLIANT` and
`QUALITY APPROVED`; findings were none. ACER-001 is Done for this reviewed local
proposal in content logical commit `46b79fc`. Clean-tree postcommit reruns
passed 38 focused tests, the 27-case self-test, production validation with
`candidates=110 controls=2 stage05=24 helpers_input=29 helpers_proposed=30`,
strict registry validation for 436 paths, and the repository aggregate; diff
and status were clean. This evidence update commit is not identified or
claimed. ACER-002 is Done. ACER-003 batch `ACER-003-001` has committed
RED/GREEN, exact archive, rollback, consumer-repair, aggregate-corpus,
independent review, and clean-tree postflight evidence in `28b42e7`. Batch
`ACER-003-002` has committed RED/GREEN, exact archive, rollback,
consumer-repair, aggregate-corpus, independent review, and clean-tree
postflight evidence in `9c18910`. Batch `ACER-003-003` has committed RED/GREEN,
exact archive, rollback, consumer-repair, aggregate-corpus, independent review,
and clean-tree postflight evidence in `96176a9`. Exact batch `ACER-003-004` has
committed RED/GREEN, byte-preserved archive, rollback, six-consumer repair,
aggregate-corpus, independent review, and clean-tree postflight evidence in
`20cb1ca`. Exact batch `ACER-003-005` has committed RED/GREEN, byte-preserved
archive, rollback, five-consumer repair, aggregate-corpus, fresh requirements
and quality approval, and clean-tree postflight evidence in `52d4c2b`. Exact
batch `ACER-003-006` has committed RED/GREEN, byte-preserved archive, rollback,
six-consumer repair, aggregate-corpus, independent approval, and clean-tree
postflight evidence in `24abe70`. No eligible batch remains. ACER-004 local
implementation is committed in `a646df1` with final independent approval and
clean-tree postflight. ACER-005 is committed in `ba4a470` with final
independent approval, scanner-clean applicable pre-commit, and clean-tree
postflight. ACER-006 closure content commit
`cfabc50681008cf0991c004f07efa17516eeed3c` is observed with clean status and
clean-tree postflight PASS. Final staged terminal reviews returned
`REQUIREMENTS COMPLIANT` and `QUALITY APPROVED`, with no findings. This
evidence-update commit is unidentified and unclaimed. Remote/live and CI/FIFO
PASS results remain unclaimed.

ACER-005 began with a focused target-existence RED: the new method executed and
failed because the residue validator and closure ledger did not exist. The
current GREEN implementation records the fixed input commit and exact reviewed
source-ledger object identities; joins all 12 historical eligible rows to the
six closed migration batches; derives all 100 current Stage 04 records and all
52 lineage identities from cached plus proposed nonignored Git inventory; and retains
13 accepted ADRs plus 28 current done Specs under terminal-status-independent
authority guards. The parent-staged 59-test module with 21 ACER-005 methods and
the isolated 17-case self-test passed before the scanner correction. The new
22nd focused method passes against the proposed descriptor and makes the final
module count 60. It requires the closure-only schema to expose all 164
historical/current/cardinality identities as `lineageId`, joined from immutable
source-ledger `pairKey` values without changing paths. The
quality-review regression admits canonical non-accepted ADRs without adding
them to the accepted guard set; accepted ADR profile/owner validation and the
exact 13-count contract remain unchanged. Production observes the exact
`12/100/98/2/52/48/1/3/13/28/0` closure counts. The two-path evidence update
binds the final owning Task blob in the closure ledger and verifies both files
from the staged index before commit. The ACER-004 dependency remains exactly 24
Stage 05 authored records, 33 helper files, and zero findings; this work adds no
helper path. Strict registry, Markdown, cross-document, protected-surface
invariant, and diff evidence pass. The aggregate and independent requirements
and quality re-reviews passed. Applicable pre-commit then produced the scanner
RED described below. The final representation passes applicable pre-commit,
and both staged and clean-tree repository aggregates pass. Content commit
`ba4a470` and the final verdicts are directly observed rather than inferred.

Quality review identified one blocking scope error: `_authority_entries()`
rejected canonical non-accepted ADRs even though VAL-ACER-005 owns accepted ADR
guards only. A focused unit fixture reproduced `CLOSURE-AUTHORITY-STATUS`; the
minimal fix now filters non-accepted ADRs exactly as non-done Specs are
filtered. Focused GREEN passes with the draft excluded and the accepted row
retained. Final post-representation requirements and quality reviews returned
`REQUIREMENTS COMPLIANT` and `QUALITY APPROVED`.

Applicable pre-commit produced a blocking `generic-api-key` RED on exactly
seven `pairKey` lines in the new closure ledger. They are the three established
ACER false-positive execution identifiers already bounded for the prior census
and eligibility ledgers, repeated 2/3/2 times by the closure schema. The first
correction escaped one hyphen as `\u002d`, but the gitleaks rerun still reported
all seven with `decoded:unicode`; recursive JSON Unicode decoding made that
representation ineffective. The replacement focused RED found closure output
still serialized `pairKey`. Final GREEN normalizes only the new closure schema:
its 12 `migratedClosed`, 100 `currentRows`, and 52 `pairCardinality` rows expose
exact canonical values under 164 `lineageId` fields. The implementation still
joins immutable source-ledger `pairKey` fields internally. The one-for-one
regression requires no raw or parsed closure `pairKey`, no Unicode workaround,
exact source-derived path/value maps, sorted pair identities, and unchanged
validator counts/equality. `.gitleaks.toml`, `.secrets.baseline`, source ledgers,
paths, and all other values remain unchanged. Final gitleaks, detect-secrets,
applicable pre-commit, focused, production, aggregate, and clean-tree
postflight reruns all pass.

ACER-001 began with the missing-target RED described in its Task row. The GREEN
implementation adds a closed-schema durable JSON census and a fail-closed
validator that reads census facts only from the exact candidate and activation
commit objects through allow-listed absolute Git queries. Missing, extra,
duplicate, premature `eligible`, unowned `DEFER`, wrong delta/control/count,
fake event, helper tracker, unsafe row path, wrong commit/blob/tree, hostile Git
environment, unknown schema/key, and ignored-workspace access fixtures fail.
Newline, control-character, absolute, empty-segment, dot/parent-segment, and
`_workspace` paths cannot enter a diagnostic payload. Official KEP,
NARA web-records, and Git reflog/gc sources were observed on 2026-07-18 and are
recorded as methodology, not repository authority. Aggregate integration runs
self-test and production modes without changing CI/FIFO behavior. Only the
detect-secrets census-OID false-positive boundary is adjusted in pre-commit.
Applicable pre-commit first identified Git OID integrity metadata as hex-entropy
false positives. The Python constants now use the repository's existing inline
allowlist convention. The scanner line exclusion was extended only for readable
JSON `candidateBaselineCommit`, `activationCommit`, and `sourceBlob` values that
are exact 40-character lowercase Git OIDs; gitleaks and the domain validator
remain blocking. This false-positive boundary is unrelated to the Spec
039-owned all-files FIFO portability condition. The repeated applicable hook
run passes with only `strict-repository-quality` skipped because its aggregate
result was proven separately.

Gitleaks configuration migrates the deprecated singular baseline allowlist to
the current array syntax without changing `.secrets.baseline` coverage. A
rule-local allowlist extends only `generic-api-key`, requires both the exact
census path suffix and one of three exact `pairKey` field values, and leaves the
default rule active. The configured pre-commit v8.30 environment directly scans
the 224.09 KB focused corpus with no findings; the same complete census copied
to out-of-path `/tmp/.../canary.json` exits 1 with five findings. The separate
system `PATH` Gitleaks development build reports the five census false
positives and is retained only as a non-blocking compatibility diagnostic; no
general cross-build PASS is claimed. These deterministic execution identifiers
and Git OIDs are not credentials.

Spec 037 requires later eligibility joins across upstream Spec, program,
current-owner state, reciprocal links, and closure evidence. ACER-001 does not
guess those lineages: every candidate carries closed `eligibilityEvidence`
axes with null/empty values, `unknown` or `pending` state, and refresh trigger
`ACER-002`. The observed body-Spec link list, pair state, and ledger-row boolean
remain non-authoritative inputs only. ACER-002 owns evidence-backed resolution
before any disposition may change from `DEFER`.

Predecessor closure commit `855fa78` and postflight commits `cdac53c` and
`a12aedf` are inputs only. At activation, ACER implementation and migration
results plus the current helper Tests disposition were unclaimed; ACER-001
through ACER-005 later recorded those package results, including ACER-004
`24/33/0`. ACER-006 closure content commit
`cfabc50681008cf0991c004f07efa17516eeed3c` and clean-tree postflight are
observed. This evidence-update commit, remote/live state, and CI/FIFO
remediation remain unclaimed. Ignored scratch content was not inspected.
## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Frozen baseline is mistaken for the activation input | Six valid records are omitted or the activation control pair is misclassified | Require exact 104+6 reconciliation to the parent 110 candidate records, preserve the pair's separate activation role as historical evidence, and retain its current done records only as terminal owned `DEFER`. |
| Done is treated as disposable | Current authority or execution facts are lost | Join lineage closure, current consumers, source recovery, links, and rollback evidence; default to retain/DEFER. |
| Large migration obscures causality | Review and rollback become unsafe | Migrate only atomic per-lineage batches with an independently reviewed logical commit. |
| Operations completeness is fabricated | False incident or postmortem evidence enters the corpus | Treat zero real events as valid and forbid placeholder event creation. |
| Helper Tests become a second Task tracker | SDLC ownership and evidence diverge | Audit helper Tests as feature-local support and keep execution state only in Stage 04 Tasks. |
| CI portability work leaks into this tranche | Ownership conflict with Spec 039 | Keep CI/FIFO changes out of scope and record only observed local evidence. |

Rollback before terminal closure is newest-first at a reviewed package boundary.
For an archive batch, restore the current execution record, consumers, index,
and ledger in one inverse commit; never delete an archive consumer before its
source restoration is complete. If evidence is ambiguous, stop at DEFER rather
than forcing a migration. The activation proposal can be reversed to parent
`a12aedf` without touching implementation surfaces.

### Legacy Task approval and rollback boundaries

- **Allowed Paths**: Spec 037 and its Stage 03 index; this reciprocal Plan and
  Task plus Stage 04 indexes; eligible Stage 04 execution sources; their exact
  mirrored full-body archive records and archive index; current consumers that
  require link repair; the migration evidence ledger; Stage 05 and helper Tests
  documents with an ACER-004 evidence-backed role finding; focused validators,
  fixtures, and their script/test indexes; directly implicated documentation
  contracts required by a reviewed package.
- **Forbidden Paths**: accepted ADR movement; still-current done Spec movement;
  age/count-only deletion; fabricated Incident/Postmortem or live evidence;
  ignored `_workspace` children; secrets, credentials, tokens, kubeconfigs,
  Vault data, auth files, shell history, and unrelated implementation surfaces;
  CI/FIFO changes owned by Spec 039; Specs 038 and 040 Plan/Task activation.
- **Approval Required**: Remote GitHub changes, push, merge, publication, live
  system action, secret handling, dependency installation, or scope expansion
  beyond the approved Spec/Plan requires separate explicit human approval.
- **Static Validation**: Closed census and disposition checks, eligibility and
  residue negatives, dry-run and batch validators, archive provenance and
  historical/current links, strict registry/Markdown/cross-document/lifecycle,
  changed Markdownlint, diff check, repository aggregate, and applicable
  pre-commit lanes.
- **Live Validation**: `DEFER`. No repository-static package may claim provider,
  remote, Kubernetes, Vault, ESO, Argo CD, or runtime readiness.
- **Secret / Vault Handling**: Do not print or preserve secret-bearing payloads
  through ordinary migration. Use the approved redacted classifier boundary;
  detection blocks the row. Never inspect ignored scratch for evidence or
  secrets.
- **Rollback Plan**: Activation rollback restores parent `a12aedf`. Later
  packages roll back newest-first. Each migration inverse must restore the
  active source, current consumers, indexes, and ledger atomically before the
  archive authority is removed or superseded.
- **Evidence Location**: This Task, reviewed logical commits, per-lineage
  archive/index records, durable migration-ledger rows, focused fixtures, and
  terminal closure evidence. Temporary dry-run output is not closure evidence.
## Completion Criteria

- The 104-record frozen baseline and six-record delta reconciled exactly to the
  parent 54-Plan/56-Task activation input, with no unclassified candidate; the
  observed activation proposal reached 55 Plans/57 Tasks and retained the pair
  separately. The current done pair is terminal owned `DEFER`, carries no
  active execution authority, and remains until exact successor migration
  evidence changes.
- Every eligible record has migrated by atomic lineage batch with full-body
  provenance, current-link repair, durable evidence, and rollback metadata.
- Accepted ADRs and still-current done Specs remain protected from
  terminal/age/count-only movement.
- The prior 24-document Stage 05 input and recomputed helper Tests corpus have
  zero unsupported ownership or role conflicts; no synthetic Incident or
  Postmortem exists.
- Active execution cardinality and residue checks pass, or each retained/DEFER
  exception has an explicit reason, owner, and refresh trigger.
- ACER-001 through ACER-005 have RED/GREEN, independent review, logical commit,
  and repository-static QA evidence. ACER-006 has observed staged local QA,
  remediated requirements compliance, remediated quality approval, closure
  content commit `cfabc50681008cf0991c004f07efa17516eeed3c`, clean status, and
  clean-tree postflight PASS. The evidence-update commit remains unidentified
  and unclaimed.
- CI/FIFO work, remote/live state, provider delivery, secrets, and ignored
  scratch remain unclaimed and outside the tranche.

## Traceability

- **Spec**: [Active Corpus and Execution Retention](spec.md)
- **Task**: [Active Corpus and Execution Retention Task](plan.md)
- **PRD**: [PRD-0006](../../01.requirements/0006-workspace-document-lifecycle-and-evidence-consolidation.md)
- **AD**: [AD-0009](../../02.architecture/descriptions/0009-document-lifecycle-evidence-operating-model.md)
- **Archive decision**: [ADR-0018](../../02.architecture/decisions/0018-full-body-archive-record-and-retention.md)

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-ACER-001](spec.md#success-criteria--verification-plan) | ACER-001 | [Closed census and disposition evidence](tasks/tsk-0001-acer-001.md) |
| N/A — VAL-ACER-002 shares the Spec 037 source linked in VAL-ACER-001 | ACER-002, ACER-003 | N/A — the paired Task is linked in VAL-ACER-001 |
| N/A — VAL-ACER-003 shares the Spec 037 source linked in VAL-ACER-001 | ACER-001, ACER-005 | N/A — the paired Task is linked in VAL-ACER-001 |
| N/A — VAL-ACER-004 shares the Spec 037 source linked in VAL-ACER-001 | ACER-002, ACER-005 | N/A — the paired Task is linked in VAL-ACER-001 |
| N/A — VAL-ACER-005 shares the Spec 037 source linked in VAL-ACER-001 | ACER-002, ACER-005 | N/A — the paired Task is linked in VAL-ACER-001 |
| N/A — VAL-ACER-006 shares the Spec 037 source linked in VAL-ACER-001 | ACER-003, ACER-005 | N/A — the paired Task is linked in VAL-ACER-001 |
| N/A — VAL-ACER-007 shares the Spec 037 source linked in VAL-ACER-001 | ACER-004, ACER-005 | N/A — the paired Task is linked in VAL-ACER-001 |

The lifecycle table renders each reciprocal relationship target once. The
work-package anchors retain complete navigation without manufacturing extra
body-evidence cardinality.

### Detailed Package Map

| Work package | Scope |
| --- | --- |
| ACER-001 | Closed current census and frozen-baseline delta reconciliation |
| ACER-002 | Eligibility, residue, negative fixtures, and dry-run ledger |
| ACER-003 | Atomic per-lineage full-body archive migration batches |
| ACER-004 | Stage 05 and helper Tests role audit and bounded remediation |
| ACER-005 | Retain/DEFER closure and active cardinality enforcement |
| ACER-006 | Full QA, fresh review, exact lifecycle closure, and postflight |

### Legacy Task traceability

- **Plan**: [Active Corpus and Execution Retention Implementation Plan](plan.md)
- **Spec**: [Spec 037](spec.md)
- **Predecessor execution history**: [Archive Index](../../98.archive/README.md#document-index)

#### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [ACER-001](plan.md#work-breakdown) | Done. | Content logical commit `46b79fc` records the exact 110 owned `DEFER` candidates and the separate retained control pair. Clean-tree postcommit reruns passed 38 focused tests, the 27-case self-test, production validation for 110 candidates, two controls, 24 Stage 05 records, and the 29-to-30 helper boundary, strict registry validation for 436 paths, and the repository aggregate; diff and status were clean. Requirements re-review was `REQUIREMENTS COMPLIANT`; quality review was `QUALITY APPROVED`; findings were none. This Task evidence update commit is not identified or claimed. ACER-002 owns any eligibility promotion. |
| [ACER-002](spec.md) | Done. | Content logical commit `414905c` proves six complete eligible pairs only; 98 candidate rows remain owned `DEFER`, the two active controls remain `retain`, and ACER-003 has not begun archive cutover. Seven focused tests, the 54-case self-test, production `110/12/98/2`, and the direct repository aggregate passed. Independent requirements and quality re-reviews approved the result with no findings; `.secrets.baseline` stayed unchanged and both scanner exceptions remain exact-path/rule-local. This evidence-only update commit is not identified or claimed. |
| N/A — ACER-003 shares the Plan linked in ACER-001 | Done. | Batches `ACER-003-001` through `ACER-003-006` retain independently approved exact evidence in logical commits `28b42e7`, `9c18910`, `96176a9`, `20cb1ca`, `52d4c2b`, and `24abe70`; the first five form the pinned SHA-256 prefix `5e5e4eea447ac514734aacaa9d6bcd3a26824c3a88a1daa8343094034babb50b`. Batch 6 removes the Spec 036 Plan/Task pair, preserves both payloads byte-for-byte in completed-lineage envelopes, repairs six Markdown consumers, and records rollback parent `420f8a582dee69f3c0902026b49667af803a96c1`. Fifteen focused migration tests plus eleven validation-lane tests, the exact 32-case self-test, production `6/12/43/362/12/15`, archive aggregate `43/362/43`, generic archive suites, the 21-test cutover regression, strict registry/Markdown/cross-document lanes, applicable changed-path pre-commit/scanners, and the clean-tree repository aggregate pass while retaining the immutable `31/202` base proof and unchanged scanner configuration. The staged-retirement regression admits only repaired consumers that remain current or are exact validated migration originals and rejects missing non-migrated and rogue consumers. Requirements review was `REQUIREMENTS COMPLIANT`; quality review was `QUALITY APPROVED`; findings were none. No eligible migration batch remains. This Task evidence update commit is not identified or claimed. |
| N/A — ACER-004 shares the Plan linked in ACER-001 | Done. | Content logical commit `a646df1` records the closed role-audit ledger, fail-closed validator, exact Tests inventory, and aggregate integration. Final requirements review was `REQUIREMENTS COMPLIANT`; final quality review was `QUALITY APPROVED`; findings were none. Clean-tree postflight passes 29 focused tests, 27 self-test cases, production 24/33/0 counts, strict registry/Markdown/cross-document validation, and the repository aggregate. Review-driven regressions reject staged/worktree drift, unsafe or nonregular helpers, README tracker promotion, and descriptor path replacement while preserving fixture-body negative cases. Stage 05 authored records and existing ledgers are unchanged; only the stale Tests README inventory is remediated. This Task evidence update commit is not identified or claimed. |
| N/A — ACER-005 shares the Plan linked in ACER-001 | Done. | Content logical commit `ba4a470` closes exactly 12 migrated rows, bounds all 98 current `DEFER` rows, retains only the active Spec 037 pair, records exact 48/1/3 lineage cardinality, guards 13 accepted ADRs and 28 done Specs, and preserves the ACER-004 24/33/0 dependency. Focused RED/GREEN closed tracked drift, draft-ADR scope, and scanner false positives without changing scanner configuration, baseline, or source ledgers. Final staged and clean-tree checks pass 60 focused tests, 17 self-test cases, exact production counts, strict document gates, applicable pre-commit including gitleaks/detect-secrets, and the repository aggregate. Requirements review was `REQUIREMENTS COMPLIANT`; quality review was `QUALITY APPROVED`; findings were none. This two-path evidence update changes only the Task and its exact-OID closure-ledger row and does not identify its own commit. |
| N/A — ACER-006 shares the Plan linked in ACER-001 | Done. | Closure content commit `cfabc50681008cf0991c004f07efa17516eeed3c` is observed with clean status. Final staged terminal reviews by `/root/acer006_terminal_requirements_review` and `/root/acer006_terminal_quality_review` returned `REQUIREMENTS COMPLIANT` and `QUALITY APPROVED`, respectively, with no findings. Clean-tree postflight passed explicit-ref lifecycle over `ce7fbdaf18b2ddc701ffbad441589af0b82f5c9d..cfabc50681008cf0991c004f07efa17516eeed3c`, focused 65, residue self-test 19, production `12/100/100/0/52:48/1/3/13/29/0`, strict registry 436, strict Markdown zero, strict links, archive `43/362/43`, and the full repository aggregate. Raw all-files remains bounded only by the Spec 039-owned FIFO `Errno 95`, while every other hook and the strict-skip rerun passed. This evidence-update commit is unidentified and unclaimed; remote/live and CI/FIFO PASS are unclaimed. |

The lifecycle table renders the Plan relationship once. Package-level text
provides the remaining navigation without inventing duplicate reciprocal
evidence.
