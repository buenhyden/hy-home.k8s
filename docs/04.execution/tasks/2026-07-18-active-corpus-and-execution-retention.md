---
title: 'Task: Active Corpus and Execution Retention'
type: sdlc/task
status: active
owner: platform
updated: 2026-07-18
---

# Task: Active Corpus and Execution Retention

## Overview

This Task is the execution, verification, review, and rollback ledger for
ACER-001 through ACER-006. It activates the reciprocal Spec 037 execution pair
from repository baseline `a12aedfb71ccabd329dabc83bd2863474d1126b0`.
ACER-001 is complete in content logical commit `46b79fc`; ACER-002 is complete
in content logical commit `414905c`. ACER-003 is In Progress with its first
atomic lineage migration independently approved and committed as `28b42e7`.
Its second atomic lineage migration is independently approved and committed as
`9c18910`. Its third atomic lineage migration is a validated local proposal
awaiting independent review and one logical commit; three eligible lineage
batches will remain after that commit. ACER-004 through ACER-006 remain Queued.
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
- [Predecessor Spec 036 Task](./2026-07-17-archive-record-and-workspace-boundary.md)

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| ACER-001 | VAL-ACER-001, VAL-ACER-003, VAL-ACER-007 | Build the closed current census and disposition contract for the 104-record baseline plus six-record delta, current Stage 05 input, and recomputed helper Tests corpus. | platform | Done | Implemented in content logical commit `46b79fc` and independently approved: requirements re-review `REQUIREMENTS COMPLIANT`, quality review `QUALITY APPROVED`, findings none. Clean-tree postcommit reruns passed 38 focused tests, the 27-case self-test, production validation, strict registry for 436 paths, and the repository aggregate; diff and status were clean. This Task evidence update commit is not identified or claimed. | RED: `python3 -m unittest tests/test_active_corpus_retention.py` exited 1 because the test target did not exist. GREEN and postcommit: 38 focused tests PASS; 27-case self-test PASS; production PASS with 110 candidates, two controls, 24 Stage 05 records, 29 helper-input files, and 30 proposed helper files. The durable v1 snapshot reconciles exact pinned Git objects to 51/53 frozen plus 3/3 delta = 54 Plans/56 Tasks/110 candidates; all 110 remain owned `DEFER` with refresh `ACER-002`. It records 53 paired, one plan-only, three task-only keys; two active Spec 037 retained controls; Stage 05 8 Guides/7 Policies/9 Runbooks and zero authored Incident/Postmortem. Its pinned activation-input helper observation is exactly 29 files (8 Python/14 JSON/6 YAML/1 README); this proposal adds only `tests/test_active_corpus_retention.py`, so proposed counts are 30 files (9/14/6/1). Both are support-only and pending ACER-004, which must recompute the then-current corpus rather than reuse either count. Every candidate, control, Stage 05, helper-input, and helper-delta path is rejected before semantic checks unless it is a canonical safe repository path; the final diagnostic boundary replaces unsafe or non-string paths with the fixed snapshot path, so exception and CLI stderr remain single-line and value-free. Upstream Spec, program, current-owner, reciprocal-link, and closure eligibility joins remain explicit `unknown`/`pending` fields owned by ACER-002; structural pair state, ledger membership, and body-Spec links do not infer them. No row is eligible and no migration, synthetic event, CI/FIFO, remote/live, or ignored-workspace claim is made. |
| ACER-002 | VAL-ACER-001, VAL-ACER-004, VAL-ACER-005 | Implement fail-closed eligibility and residue validation plus deterministic dry-run ledger output. | platform | Done | Content logical commit `414905c` adds the pinned-object dry-run ledger and validator for all 110 candidate identities, exactly 12 eligible rows in six complete Plan/Task pairs, 98 owned `DEFER` rows, and two retained Spec 037 controls. It records pinned canonical-link and literal consumers including census/migration evidence while excluding same-pair reciprocal sources from external repair. The completed Specs 026–030 pairs retain resolved partial lineage/relationship/closure evidence and only the current-owner-key gap. No source, archive payload, index, or migration-ledger row moved or changed. Requirements re-review was `REQUIREMENTS COMPLIANT`; quality re-review was `QUALITY APPROVED` with no findings. | RED: the focused suite first failed for the absent validator, then for named matrix/consumer evidence, owner-key lineage, and real runner fixtures. GREEN and delivery: seven focused tests PASS; 54-case self-test PASS; production PASS (`candidates=110 eligible=12 defer=98 controls=2`); direct repository aggregate PASS; applicable pre-commit PASS with detect-secrets and strict skipped only after the separately proven aggregate because the known FIFO filesystem failure remains Spec 039-owned. `.secrets.baseline` is unchanged; exact-path detect-secrets and rule-local gitleaks boundaries preserve out-of-path canaries. ACER-003 still owns atomic consumer/index/ledger repair and per-record rollback evidence. |
| ACER-003 | VAL-ACER-002, VAL-ACER-006 | Migrate eligible execution records in atomic per-lineage full-body archive batches. | platform | In Progress | Batches `ACER-003-001` and `ACER-003-002` migrated the first two deterministic eligible pairs in independently approved logical commits `28b42e7` and `9c18910`. Batch `ACER-003-003` is the validated local proposal for `2026-07-14-template-lifecycle-contract-normalization`; independent review and one logical commit remain pending. Three eligible batches will remain after that commit, so ACER-003 is not Done. | The committed two-batch canonical prefix retains SHA-256 `07a94683e8980ab6c7a39e183826fe8c56cc0ff3a3d173327935eafead478364`. Batch 3 RED changed only the focused contract: the old two-batch validator rejected the exact proposed third prefix with `MIGRATION-ELIGIBLE-PREFIX`; 10 tests exited 1 with two failures and two errors. GREEN passes 10 focused tests, the exact 20-case self-test, production migration `3/6/37/275/6/8`, generic archive recovery 15 tests, generic archive validation 22 tests, full archive cutover regression 21 tests, production archive `37/275/37`, and strict registry/Markdown/cross-document validation. The third rollback parent is `22ad025ed7beb0725095d1ab413a2d5c49f8561c`; five batch-3 consumers are repaired. The Plan payload is 51,960 bytes with SHA-256 `102ffdabc9e0b839c449f00dd511355bd857ce49f8c423ffd8cfcef8491ffdcc` and 25 historical links; the Task payload is 8,415 bytes with SHA-256 `717c445c3b51db3ef286f342ad3a997063285fc170afe214af306cc0d8d48381` and 17 links. The archive proof separately preserves the immutable 31-record/202-link base; no remote/live, CI/FIFO, or ignored-workspace claim is made. |
| ACER-004 | VAL-ACER-007 | Audit Stage 05 and helper Tests roles and apply only bounded evidence-backed remediation. | platform | Queued | Not executed. | Recompute current inventories; preserve real operations facts; forbid synthetic events and a second Stage 04 tracker. |
| ACER-005 | VAL-ACER-003 through VAL-ACER-007 | Close retain/DEFER rows and enforce active owner, execution cardinality, and residue rules. | platform | Queued | Not executed. | Every remaining exception requires reason, owner, trigger, and current-authority evidence; unexplained residue must be zero. |
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
postflight evidence in `9c18910`. Batch `ACER-003-003` has local RED/GREEN,
exact archive, rollback, consumer-repair, aggregate-corpus, and strict-
validation evidence; independent review and a logical commit remain pending.
Three eligible batches will remain after that commit. ACER-004 through ACER-006
remain Queued. No later migration batch, helper-role remediation, tranche
closure, remote, live, or CI/FIFO result is claimed.

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
- **Predecessor Task**: [Archive Record and Workspace Boundary Task](./2026-07-17-archive-record-and-workspace-boundary.md)

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [ACER-001](../plans/2026-07-18-active-corpus-and-execution-retention.md#work-breakdown) | Done. | Content logical commit `46b79fc` records the exact 110 owned `DEFER` candidates and the separate retained control pair. Clean-tree postcommit reruns passed 38 focused tests, the 27-case self-test, production validation for 110 candidates, two controls, 24 Stage 05 records, and the 29-to-30 helper boundary, strict registry validation for 436 paths, and the repository aggregate; diff and status were clean. Requirements re-review was `REQUIREMENTS COMPLIANT`; quality review was `QUALITY APPROVED`; findings were none. This Task evidence update commit is not identified or claimed. ACER-002 owns any eligibility promotion. |
| [ACER-002](../../03.specs/037-active-corpus-and-execution-retention/spec.md) | Done. | Content logical commit `414905c` proves six complete eligible pairs only; 98 candidate rows remain owned `DEFER`, the two active controls remain `retain`, and ACER-003 has not begun archive cutover. Seven focused tests, the 54-case self-test, production `110/12/98/2`, and the direct repository aggregate passed. Independent requirements and quality re-reviews approved the result with no findings; `.secrets.baseline` stayed unchanged and both scanner exceptions remain exact-path/rule-local. This evidence-only update commit is not identified or claimed. |
| N/A — ACER-003 shares the Plan linked in ACER-001 | In Progress. | Batches `ACER-003-001` and `ACER-003-002` retain their independently approved exact evidence in logical commits `28b42e7` and `9c18910`; their canonical combined prefix is pinned to SHA-256 `07a94683e8980ab6c7a39e183826fe8c56cc0ff3a3d173327935eafead478364`. Batch `ACER-003-003` is a local uncommitted proposal that removes the exact Spec 033 Plan/Task pair, preserves both payloads byte-for-byte in completed-lineage envelopes, repairs five current Markdown consumers, and records rollback parent `22ad025ed7beb0725095d1ab413a2d5c49f8561c`. Ten focused tests, the exact 20-case self-test, production `3/6/37/275/6/8`, archive aggregate `37/275/37`, generic archive suites, the 21-test cutover regression, and strict registry/Markdown/cross-document lanes pass while retaining the immutable `31/202` base proof. Independent review and one logical commit remain pending; three eligible batches will remain afterward, so ACER-003 is not Done. |
| N/A — ACER-004 shares the Plan linked in ACER-001 | Queued. | The 24-record Stage 05 input and prior helper Tests inventory still require recomputation and role review. |
| N/A — ACER-005 shares the Plan linked in ACER-001 | Queued. | Retain/DEFER closure and residue cardinality evidence do not yet exist. |
| N/A — ACER-006 shares the Plan linked in ACER-001 | Queued. | Whole-tranche QA, independent review, atomic closure, commit, and postflight are pending. |

The lifecycle table renders the Plan relationship once. Package-level text
provides the remaining navigation without inventing duplicate reciprocal
evidence.
