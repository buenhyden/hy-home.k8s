---
title: 'Task: Active Corpus and Execution Retention'
type: sdlc/task
status: active
owner: platform
updated: 2026-07-19
---

# Task: Active Corpus and Execution Retention

## Overview

This Task is the execution, verification, review, and rollback ledger for
ACER-001 through ACER-006. It activates the reciprocal Spec 037 execution pair
from repository baseline `a12aedfb71ccabd329dabc83bd2863474d1126b0`.
ACER-001 is complete in content logical commit `46b79fc`; ACER-002 is complete
in content logical commit `414905c`. ACER-003 is complete with independently
approved atomic lineage commits `28b42e7`, `9c18910`, `96176a9`, `20cb1ca`,
`52d4c2b`, and `24abe70`. No eligible lineage batch remains. ACER-004 local
implementation is complete in content logical commit `a646df1` with final
independent approval and clean-tree postflight. ACER-005 local implementation
is complete in content logical commit `ba4a470` with final independent approval,
scanner-clean applicable pre-commit, and clean-tree postflight. ACER-006 remains
Queued.
Produced evidence is recorded below.

The parent `a12aedf` activation input records 54 authored Plans plus 56 authored
Tasks, for 110 candidates. This staged reciprocal pair raises the proposed
corpus to 55 Plans and 57 Tasks (112 records) and remains a separately retained
active control. ACER-001 must reconcile the frozen 104-record baseline with the
six later records created for Specs 034 through 036. No candidate is eligible
merely because it is terminal, old, or counted. The prior Stage 05 input is 24
authored records (eight Guides, seven Policies, and nine Runbooks), with zero
real authored Incident and Postmortem records. The earlier helper Tests
inventory is an input to recompute rather than activation PASS evidence.

## Inputs

- [Active Corpus and Execution Retention Implementation Plan](../plans/2026-07-18-active-corpus-and-execution-retention.md)
- [Spec 037](../../03.specs/037-active-corpus-and-execution-retention/spec.md)
- [PRD-006](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md)
- [ARD-0009](../../02.architecture/requirements/0009-document-lifecycle-evidence-operating-model.md)
- [ADR-0018](../../02.architecture/decisions/0018-full-body-archive-record-and-retention.md)
- [Archive index](../../98.archive/README.md)
- [Migration evidence ledger](../../90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md)
- [Predecessor Spec 036 execution history](../../98.archive/README.md#document-index)

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| ACER-001 | VAL-ACER-001, VAL-ACER-003, VAL-ACER-007 | Build the closed current census and disposition contract for the 104-record baseline plus six-record delta, current Stage 05 input, and recomputed helper Tests corpus. | platform | Done | Implemented in content logical commit `46b79fc` and independently approved: requirements re-review `REQUIREMENTS COMPLIANT`, quality review `QUALITY APPROVED`, findings none. Clean-tree postcommit reruns passed 38 focused tests, the 27-case self-test, production validation, strict registry for 436 paths, and the repository aggregate; diff and status were clean. This Task evidence update commit is not identified or claimed. | RED: `python3 -m unittest tests/test_active_corpus_retention.py` exited 1 because the test target did not exist. GREEN and postcommit: 38 focused tests PASS; 27-case self-test PASS; production PASS with 110 candidates, two controls, 24 Stage 05 records, 29 helper-input files, and 30 proposed helper files. The durable v1 snapshot reconciles exact pinned Git objects to 51/53 frozen plus 3/3 delta = 54 Plans/56 Tasks/110 candidates; all 110 remain owned `DEFER` with refresh `ACER-002`. It records 53 paired, one plan-only, three task-only keys; two active Spec 037 retained controls; Stage 05 8 Guides/7 Policies/9 Runbooks and zero authored Incident/Postmortem. Its pinned activation-input helper observation is exactly 29 files (8 Python/14 JSON/6 YAML/1 README); this proposal adds only `tests/test_active_corpus_retention.py`, so proposed counts are 30 files (9/14/6/1). Both are support-only and pending ACER-004, which must recompute the then-current corpus rather than reuse either count. Every candidate, control, Stage 05, helper-input, and helper-delta path is rejected before semantic checks unless it is a canonical safe repository path; the final diagnostic boundary replaces unsafe or non-string paths with the fixed snapshot path, so exception and CLI stderr remain single-line and value-free. Upstream Spec, program, current-owner, reciprocal-link, and closure eligibility joins remain explicit `unknown`/`pending` fields owned by ACER-002; structural pair state, ledger membership, and body-Spec links do not infer them. No row is eligible and no migration, synthetic event, CI/FIFO, remote/live, or ignored-workspace claim is made. |
| ACER-002 | VAL-ACER-001, VAL-ACER-004, VAL-ACER-005 | Implement fail-closed eligibility and residue validation plus deterministic dry-run ledger output. | platform | Done | Content logical commit `414905c` adds the pinned-object dry-run ledger and validator for all 110 candidate identities, exactly 12 eligible rows in six complete Plan/Task pairs, 98 owned `DEFER` rows, and two retained Spec 037 controls. It records pinned canonical-link and literal consumers including census/migration evidence while excluding same-pair reciprocal sources from external repair. The completed Specs 026–030 pairs retain resolved partial lineage/relationship/closure evidence and only the current-owner-key gap. No source, archive payload, index, or migration-ledger row moved or changed. Requirements re-review was `REQUIREMENTS COMPLIANT`; quality re-review was `QUALITY APPROVED` with no findings. | RED: the focused suite first failed for the absent validator, then for named matrix/consumer evidence, owner-key lineage, and real runner fixtures. GREEN and delivery: seven focused tests PASS; 54-case self-test PASS; production PASS (`candidates=110 eligible=12 defer=98 controls=2`); direct repository aggregate PASS; applicable pre-commit PASS with detect-secrets and strict skipped only after the separately proven aggregate because the known FIFO filesystem failure remains Spec 039-owned. `.secrets.baseline` is unchanged; exact-path detect-secrets and rule-local gitleaks boundaries preserve out-of-path canaries. ACER-003 still owns atomic consumer/index/ledger repair and per-record rollback evidence. |
| ACER-003 | VAL-ACER-002, VAL-ACER-006 | Migrate eligible execution records in atomic per-lineage full-body archive batches. | platform | Done | Batches `ACER-003-001` through `ACER-003-006` migrated the complete six-pair eligible corpus in independently approved logical commits `28b42e7`, `9c18910`, `96176a9`, `20cb1ca`, `52d4c2b`, and `24abe70`. | The committed five-batch canonical prefix retains SHA-256 `5e5e4eea447ac514734aacaa9d6bcd3a26824c3a88a1daa8343094034babb50b`. Batch 6 RED proved the old five-batch validator rejects the proposed sixth prefix with `MIGRATION-ELIGIBLE-PREFIX`. GREEN and clean-tree postflight pass 15 focused migration tests plus 11 validation-lane tests, the exact 32-case self-test, production migration `6/12/43/362/12/15`, generic archive recovery and validation 37 tests, full archive cutover regression 21 tests in 431.734 seconds, production archive `43/362/43`, strict registry/Markdown/cross-document validation, and the repository aggregate. Applicable changed-path pre-commit passed after the direct aggregate independently passed; hardcoded-secret and detect-secrets hooks passed and scanner configuration remained unchanged. The staged-retirement regression admits historical repaired consumers only when they remain current or are exact `originalPath` members of the validated migration ledger, while missing non-migrated and rogue consumers fail closed. Requirements review was `REQUIREMENTS COMPLIANT`; quality review was `QUALITY APPROVED`; findings were none. The sixth rollback parent is `420f8a582dee69f3c0902026b49667af803a96c1`; six batch-6 consumers are repaired without changing the successor Spec 037 Plan, WEIA, or generic Stage 90 index. The Plan payload is 21,539 bytes with SHA-256 `dff92c9051c654604c46e40fe8188d068c6f4d7eacb83877b485eb6925312b23` and 14 historical links; the Task payload is 36,397 bytes with SHA-256 `f3badfc88f43281138d82ace386316e0d3f69bbc5a31ea9ea210f9b6597524fb` and 19 links. Remote/live, CI/FIFO, and ignored-workspace evidence remain unclaimed. The archive proof separately preserves the immutable 31-record/202-link base. This Task evidence update commit is not identified or claimed. |
| ACER-004 | VAL-ACER-007 | Audit Stage 05 and helper Tests roles and apply only bounded evidence-backed remediation. | platform | Done | Content logical commit `a646df1` preserves the exact 24-record Stage 05 corpus (8 Guides, 7 Policies, 9 Runbooks, 0 Incidents, 0 Postmortems), records the exact 33-file helper corpus (12 Python, 14 JSON, 6 YAML, 1 README), and repairs only the stale `tests/README.md` inventory by adding twelve missing rows and removing one absent legacy row. Final requirements review was `REQUIREMENTS COMPLIANT`; final quality review was `QUALITY APPROVED`; findings were none. This Task evidence update commit is not identified or claimed. | Initial RED: the focused target was absent. Review-driven RED/GREEN closed discarded index OIDs, README tracker semantics, descriptor-reopen TOCTOU, and non-README helper read bypass. Final staged and clean-tree postflight pass 29 focused tests, the 27-case isolated self-test, production `stage05=24 types=8/7/9/0/0 helpers=33 formats=12/14/6/1 findings=0`, strict registry for 436 paths, Markdown zero, valid cross-document checks, and the repository aggregate. Applicable pre-commit passes hardcoded-secret, detect-secrets, Markdownlint, ShellCheck, and shfmt; the Spec 039-owned duplicate strict hook is skipped only after direct aggregate proof. All tracked Stage 05/helper/ledger/validator/aggregate bytes are bound to stage-zero index OIDs through bounded `cat-file` plus descriptor-based `O_NOFOLLOW` reads; proposed helpers use the same bounded descriptor path. Every helper crosses the authoritative read boundary, while README alone receives tracker/residue/current-claim scans, so intentional Python/JSON negative strings remain accepted. No Stage 05 authored document, synthetic event, CI/FIFO, scanner configuration, remote/live state, existing ledger, or ignored-workspace content changed. |
| ACER-005 | VAL-ACER-003 through VAL-ACER-007 | Close retain/DEFER rows and enforce active owner, execution cardinality, and residue rules. | platform | Done | Content logical commit `ba4a470` adds the durable v1 closure record and fail-closed validator without rewriting reviewed inputs. It translates exactly 12 historical `eligible` rows to `migrated-closed`, preserves all 98 current `DEFER` rows with bounded authority fields, retains only the two active Spec 037 controls, and records 100 Stage 04 rows (49 Plans/51 Tasks), 52 lineage identities (48 complete, one Plan-only, three Task-only), four owned partial `DEFER` rows, 13 accepted ADR guards, 28 done-Spec guards, and zero findings. Final requirements review was `REQUIREMENTS COMPLIANT`; final quality review was `QUALITY APPROVED`; findings were none. This two-path evidence update changes only this Task and its exact-OID closure-ledger row; its commit is not identified or claimed. | RED/GREEN closed absent targets, tracked descriptor/index drift, canonical draft-ADR rejection, and seven gitleaks false positives. The final closure schema uses exactly 164 `lineageId` fields while immutable source ledgers retain `pairKey`; it contains no Unicode workaround and leaves `.gitleaks.toml`, `.secrets.baseline`, source ledgers, and protected surfaces unchanged. Staged and clean-tree postflight pass the 60-test module with 22 ACER-005 methods, 17 self-test cases, production `migrated=12 current=100 dispositions=98/2 pairs=52:48/1/3 guards=13/28 findings=0`, ACER-004 dependency `24/33/0`, strict registry for 436 paths, Markdown zero, valid cross-document checks, and the repository aggregate. Applicable pre-commit passes gitleaks, detect-secrets, Markdownlint, ShellCheck, shfmt, affected-surface, JSON, and hygiene hooks; only the duplicate Spec 039-owned strict hook is skipped after direct aggregate proof. All tracked source, inventory, authority, control, ledger, validator, and aggregate bytes remain bounded to stage-zero OIDs plus no-follow descriptor equality; proposed files remain descriptor-only. Remote/live and CI/FIFO results remain unclaimed. |
| ACER-006 | VAL-ACER-001 through VAL-ACER-007 | Run full repository-static QA and independent review, prepare atomic lifecycle closure, commit, and record postflight. | platform | Queued | Not executed. | Requires staged lifecycle, strict registry/Markdown/cross-document, archive/residue/census gates, aggregate, applicable pre-commit, fresh requirements/quality verdicts, closure commit, and explicit postflight. |

## Approval and Safety Boundaries

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

## Verification Summary

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
postflight. ACER-006 remains Queued. No
tranche closure, remote, live, or CI/FIFO result is claimed.

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
`a12aedf` are inputs only. ACER implementation and migration results, current
helper Tests disposition, remote/live state, CI/FIFO remediation, and ignored
scratch content remain unclaimed.

## Traceability

- **Plan**: [Active Corpus and Execution Retention Implementation Plan](../plans/2026-07-18-active-corpus-and-execution-retention.md)
- **Spec**: [Spec 037](../../03.specs/037-active-corpus-and-execution-retention/spec.md)
- **Predecessor execution history**: [Archive Index](../../98.archive/README.md#document-index)

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [ACER-001](../plans/2026-07-18-active-corpus-and-execution-retention.md#work-breakdown) | Done. | Content logical commit `46b79fc` records the exact 110 owned `DEFER` candidates and the separate retained control pair. Clean-tree postcommit reruns passed 38 focused tests, the 27-case self-test, production validation for 110 candidates, two controls, 24 Stage 05 records, and the 29-to-30 helper boundary, strict registry validation for 436 paths, and the repository aggregate; diff and status were clean. Requirements re-review was `REQUIREMENTS COMPLIANT`; quality review was `QUALITY APPROVED`; findings were none. This Task evidence update commit is not identified or claimed. ACER-002 owns any eligibility promotion. |
| [ACER-002](../../03.specs/037-active-corpus-and-execution-retention/spec.md) | Done. | Content logical commit `414905c` proves six complete eligible pairs only; 98 candidate rows remain owned `DEFER`, the two active controls remain `retain`, and ACER-003 has not begun archive cutover. Seven focused tests, the 54-case self-test, production `110/12/98/2`, and the direct repository aggregate passed. Independent requirements and quality re-reviews approved the result with no findings; `.secrets.baseline` stayed unchanged and both scanner exceptions remain exact-path/rule-local. This evidence-only update commit is not identified or claimed. |
| N/A — ACER-003 shares the Plan linked in ACER-001 | Done. | Batches `ACER-003-001` through `ACER-003-006` retain independently approved exact evidence in logical commits `28b42e7`, `9c18910`, `96176a9`, `20cb1ca`, `52d4c2b`, and `24abe70`; the first five form the pinned SHA-256 prefix `5e5e4eea447ac514734aacaa9d6bcd3a26824c3a88a1daa8343094034babb50b`. Batch 6 removes the Spec 036 Plan/Task pair, preserves both payloads byte-for-byte in completed-lineage envelopes, repairs six Markdown consumers, and records rollback parent `420f8a582dee69f3c0902026b49667af803a96c1`. Fifteen focused migration tests plus eleven validation-lane tests, the exact 32-case self-test, production `6/12/43/362/12/15`, archive aggregate `43/362/43`, generic archive suites, the 21-test cutover regression, strict registry/Markdown/cross-document lanes, applicable changed-path pre-commit/scanners, and the clean-tree repository aggregate pass while retaining the immutable `31/202` base proof and unchanged scanner configuration. The staged-retirement regression admits only repaired consumers that remain current or are exact validated migration originals and rejects missing non-migrated and rogue consumers. Requirements review was `REQUIREMENTS COMPLIANT`; quality review was `QUALITY APPROVED`; findings were none. No eligible migration batch remains. This Task evidence update commit is not identified or claimed. |
| N/A — ACER-004 shares the Plan linked in ACER-001 | Done. | Content logical commit `a646df1` records the closed role-audit ledger, fail-closed validator, exact Tests inventory, and aggregate integration. Final requirements review was `REQUIREMENTS COMPLIANT`; final quality review was `QUALITY APPROVED`; findings were none. Clean-tree postflight passes 29 focused tests, 27 self-test cases, production 24/33/0 counts, strict registry/Markdown/cross-document validation, and the repository aggregate. Review-driven regressions reject staged/worktree drift, unsafe or nonregular helpers, README tracker promotion, and descriptor path replacement while preserving fixture-body negative cases. Stage 05 authored records and existing ledgers are unchanged; only the stale Tests README inventory is remediated. This Task evidence update commit is not identified or claimed. |
| N/A — ACER-005 shares the Plan linked in ACER-001 | Done. | Content logical commit `ba4a470` closes exactly 12 migrated rows, bounds all 98 current `DEFER` rows, retains only the active Spec 037 pair, records exact 48/1/3 lineage cardinality, guards 13 accepted ADRs and 28 done Specs, and preserves the ACER-004 24/33/0 dependency. Focused RED/GREEN closed tracked drift, draft-ADR scope, and scanner false positives without changing scanner configuration, baseline, or source ledgers. Final staged and clean-tree checks pass 60 focused tests, 17 self-test cases, exact production counts, strict document gates, applicable pre-commit including gitleaks/detect-secrets, and the repository aggregate. Requirements review was `REQUIREMENTS COMPLIANT`; quality review was `QUALITY APPROVED`; findings were none. This two-path evidence update changes only the Task and its exact-OID closure-ledger row and does not identify its own commit. |
| N/A — ACER-006 shares the Plan linked in ACER-001 | Queued. | Whole-tranche QA, independent review, atomic closure, commit, and postflight are pending. |

The lifecycle table renders the Plan relationship once. Package-level text
provides the remaining navigation without inventing duplicate reciprocal
evidence.
