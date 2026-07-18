---
title: 'Task: Archive Record and Workspace Boundary'
type: sdlc/task
status: active
owner: platform
updated: 2026-07-18
---

# Task: Archive Record and Workspace Boundary

## Overview

This Task is the execution, verification, review, and rollback ledger for
ARWB-001 through ARWB-005. The active record authorizes planning and bounded
implementation under Spec 036; it does not assert that recovery, archive
conversion, source-link validation, workspace enforcement, or closure has run.

The activation baseline is `04cb3a6`; ARWB-001 was committed as `6b9b9cd` from
parent `04a4d32`, and ARWB-002 now executes from that commit. Every
implementation package must retain its named RED, GREEN command result, independent
requirements and quality verdict, logical commit, and parent before the next
package begins.

## Inputs

- [Archive Record and Workspace Boundary Implementation Plan](../plans/2026-07-17-archive-record-and-workspace-boundary.md)
- [Spec 036](../../03.specs/036-archive-record-and-workspace-boundary/spec.md)
- [PRD-006](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md)
- [ARD-0009](../../02.architecture/requirements/0009-document-lifecycle-evidence-operating-model.md)
- [ADR-0018](../../02.architecture/decisions/0018-full-body-archive-record-and-retention.md)
- [Archive index](../../98.archive/README.md)
- [Migration evidence ledger](../../90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md)
- [`_workspace` tracked boundary](../../../_workspace/README.md)

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| ARWB-001 | VAL-ARWB-001, VAL-ARWB-002, VAL-ARWB-004, VAL-ARWB-007 | Define exact Git-object recovery and ArchiveEnvelope.v1 parser/schema capability without activating production archive authority. | platform | Done | Focused implementation, independent reviews, and logical commit complete. | Initial RED: missing private module. Requirements RED: ten tests with five expected failures. Quality RED: fifteen tests with two failures and three errors. GREEN: 15/15 plus Ruff/compile and strict document gates. Independent verdicts: `REQUIREMENTS COMPLIANT`, `QUALITY APPROVED`. Logical commit: `6b9b9cd`; commit parent: `04a4d32`; no production authority or workspace guard changed. |
| ARWB-002 | VAL-ARWB-002, VAL-ARWB-003, VAL-ARWB-005, VAL-ARWB-007 | Implement fail-closed archive, provenance, integrity, historical-link, current-authority, and immutability validation. | platform | In Progress | Focused implementation and independent reviews complete; the logical commit remains pending. | Initial RED: missing module, then 14 cases with nine failures. Quality RED: 22 cases with 17 failures and 13 errors. GREEN: 22/22 focused and 37/37 ARWB regression, canonical link self-test, Ruff/compile, strict document gates, Markdownlint, and diff check. Verdicts: `REQUIREMENTS COMPLIANT`, initial `QUALITY CHANGES REQUIRED`, final `QUALITY APPROVED`. Parent: `6b9b9cd`. |
| ARWB-003 | VAL-ARWB-001 through VAL-ARWB-005 | Atomically activate production archive authority, migrate 31 records, prove 202 links, cut index/current authority, and retire the Tombstone role. | platform | Queued | Not executed. | `ARCHIVE-CUTOVER-INCOMPLETE` RED, redacted secret-classifier result, 31/31 blob/digest and 202/202 link proof, production route/form/predicates, complete index, zero direct current links, retired Tombstone role, reviews, one logical commit and parent. |
| ARWB-004 | VAL-ARWB-006 | Enforce `_workspace` as one tracked README plus unread ignored scratch using Git metadata only. | platform | Queued | Not executed. | Isolated tracked/ignored mutation fixtures, production index proof, no-traversal review, logical commit and parent. |
| ARWB-005 | VAL-ARWB-001 through VAL-ARWB-007 | Reproduce incomplete closure, run full QA, obtain whole-tranche review, and close Spec 036 atomically. | platform | Queued | Not executed. | Lifecycle incomplete-closure RED, full command matrix, review verdicts, closure proposal, rollback boundary, logical commit and post-commit checks. |

## Approval and Safety Boundaries

- **Allowed Paths**: `docs/03.specs/036-archive-record-and-workspace-boundary/**`
  and its Stage 03 index; this reciprocal Plan/Task and Stage 04 indexes;
  `docs/98.archive/**`; archive-specific `docs/99.templates/support/**` and
  `docs/99.templates/templates/**`; `_workspace/README.md` only; archive,
  lifecycle, Markdown, link/owner, and workspace metadata validators in
  `scripts/**`; their exact fixtures and script/test indexes; directly
  implicated Stage 00/.github descriptions; the three migration-ledger rows
  owned by Spec 036 and this pair.
- **Forbidden Paths**: ignored `_workspace` children; secrets, credentials,
  tokens, auth files, shell history, kubeconfigs, Vault data, local diagnostics;
  Kubernetes/GitOps desired state, infrastructure, provider runtime adapters,
  unrelated current documents, completed Plan/Task movement, Spec 037-040
  bodies except read-only boundary checks, and bulk non-archive rewrites.
- **Approval Required**: Any remote GitHub change, live system action, secret
  handling, dependency installation, protected-surface expansion, publication,
  push, or merge requires separate explicit human approval.
- **Static Validation**: Named archive/recovery/workspace self-tests, exact
  31/202 proofs, strict registry/Markdown/link/lifecycle checks, repository
  aggregate, changed-file Markdownlint, diff check, and all-files pre-commit.
- **Live Validation**: `DEFER`. This tranche authorizes repository-static Git
  object and document evidence only; it has no provider or cluster lane.
- **Secret / Vault Handling**: Automated archive validation may stream tracked
  Git blob bytes in memory only into the repository secret classifier. It must
  emit redacted path/code diagnostics and never payloads, matches, or values;
  a detection marks the record `BLOCKED` and stops envelope creation. Agents
  and logs must not display secret-bearing history. Never inspect ignored
  scratch to search for secrets or evidence.
- **Rollback Plan**: Before closure, revert newest ARWB commit first and remove
  consumers before the archive contract. After terminal closure, stage one
  complete ARWB-005-through-ARWB-001 reverse patch, validate the restored
  compatible state only after the full patch is assembled, and create one
  atomic rollback commit. Baseline parent is `04cb3a6`.
- **Evidence Location**: This Task, logical Git commits, exact archive/index
  records, focused fixtures, and durable tracked migration evidence. Ignored
  scratch and dry-run logs are never closure evidence.

The `_workspace` no-read boundary is absolute for automated validation. An
agent or script must not list the directory, expand a child glob, recurse,
open, stat by discovery, hash, copy, move, or delete ignored children. It may
query the Git index and ignore rules for an explicit non-created probe path.

## Verification Summary

Planning activation begins from repository baseline `04cb3a6`, after Spec 035
closed and made Spec 036 the first unfinished PRD-006 tranche. The approved
Spec and ADR record a 31-record recovery inventory and 202 historical links,
but ARWB has not rerun or claimed those results. No archive payload, registry
route, form, validator, index, current link, or workspace guard is changed by
this activation package.

The reciprocal active Plan/Task pair is the only current execution component
for Spec 036. Spec 037 remains active as a design contract with no Plan/Task.
Focused activation checks cover exact route admission, five-key frontmatter,
canonical body contracts, reciprocal rendered links, stage-index membership,
three 14-column ledger records, and whitespace integrity. Long repository
aggregate and all-files lanes are deferred until implementation or closure and
are not represented as planning PASS evidence.

The focused activation run passes with both untracked execution files supplied
as explicit candidates: strict registry classifies 434 paths across two
programs (`baseline=433`, `new=62`, uncovered 0, ambiguous 0), strict Markdown
reports zero violations, strict cross-document validation accepts the sole
Spec 036 reciprocal pair, changed-file Markdownlint passes, and
`git diff --check` reports no whitespace error.

ARWB-001 then added an import-only private recovery module and one focused
unit-test surface. The intentional RED command
`python3 -m unittest tests/test_archive_recovery.py` exited 1 because
`scripts.archive_recovery` did not exist. After the minimal implementation,
the same command first ran seven cases and passed. Requirements review then
identified missing duplicate-key, canonical-serialization, and raw-path
normalization negatives. The expanded ten-test RED ran with five expected
failures: one duplicate key was accepted, CRLF returned the wrong diagnostic,
extra spacing was accepted, and both `./` and repeated-separator paths were
accepted. The remediation now rejects duplicate mappings, requires loaded
metadata to serialize byte-identically as canonical UTF-8/LF frontmatter, and
requires raw repository paths to equal their `PurePosixPath` rendering.
Requirements re-review returned `REQUIREMENTS COMPLIANT`. Quality review then
required Ruff conformance, payload-free dataclass representations, literal Git
pathspecs, real SHA-256 repository evidence, deterministic bounded Git
execution with stable errors, DEL rejection, and a non-authoritative name for
the bounded inline-link count. The expanded fifteen-test RED ran with two
failures and three errors before those changes. The cases use temporary Git
repositories to prove SHA-1 and SHA-256 commit/blob identity, raw `cat-file`
bytes, byte count, payload SHA-256, non-authoritative inline-link candidate
count, mirrored archive-path proposal, UTF-8
admission, the closed reason/replacement dependency, exact marker placement,
payload-to-EOF collision safety, final-newline preservation, and rejection of
worktree-byte substitution. It also proves literal metacharacter paths,
global/system/graft/replace/lazy-fetch isolation, bounded Git subprocesses,
payload-free representations, and stable non-disclosing process/root/object-
format failures. Quality re-review returned `QUALITY APPROVED`. ARWB-001 was
committed as `6b9b9cd` from parent `04a4d32`. The 31-record/202-link corpus
proof and ARWB-002 through ARWB-005 remain pending, so the Task and Spec stay
active.

Post-implementation focused evidence is repository-static: the same unit-test
command passes `15/15`; `ruff check`, `ruff format --check`, and
`python3 -m py_compile` pass for the module and test;
strict registry reports 434 classified paths with `baseline=433`, `new=62`,
two programs, and zero uncovered or ambiguous paths; strict Markdown reports
zero violations; strict cross-document validation reports valid; changed-file
Markdownlint and whitespace/final-newline checks pass. This is focused
repository-static evidence, not the canonical affected runner. Affected,
staged, all-files, message/manual, CI, and remote/live lanes are not claimed by
the ARWB-001 package. Its logical commit is `6b9b9cd` from parent `04a4d32`;
rollback before later-package consumption is the bounded revert of that commit.

ARWB-002 began with `python3 -m unittest tests/test_archive_validation.py`
failing because the import-only validator module did not exist. After the
immutable interfaces were introduced as empty skeletons, the named 14-case RED
ran with nine expected failures covering metadata order/type, blob/digest and
payload mutation, wrong mirror, source-tree miss despite current-tree
existence, archive reactivation, active direct individual-archive navigation,
duplicate `original_path` authority, and archive mutation/deletion. The minimal
implementation now parses the ARWB-001 envelope, recovers provenance from full
Git objects, checks sanitized literal source-tree paths, and imports the
filesystem-free canonical CommonMark adapter from
`validate-links-and-owners.py` by fixed script path. Current authority consumes
only passed frozen Markdown/profile inputs; immutability consumes passed base
and proposed byte mappings. Payload, Markdown, and resolved target values are
excluded from representations and diagnostics.

Independent requirements review returned `REQUIREMENTS COMPLIANT`. Initial
quality review returned `QUALITY CHANGES REQUIRED` because current authority
did not close its inventory/status/profile inputs, the predictable dynamic
module cache and adapter return were trusted, malformed public containers could
raise or fail open, and the completed requirements verdict was not recorded.
The expanded 22-case quality RED ran with 17 failures and 13 errors, including
raw `KeyError`, `TypeError`, and `AttributeError` paths. Remediation now
materializes exact record/document sequences and archive mappings before sort
or dereference; validates every inventory member, mapping key/value, canonical
path, and finite current status/profile; and treats every active/accepted path
below `docs/98.archive` except the exact index as reactivated independently of
caller inventory. The fixed canonical adapter path is loaded under a private
unique verified module identity rather than a predictable cache entry. Import,
call, sequence, link-kind, and target-shape failures collapse to one stable
payload-free diagnostic.

A residual quality pass caught the empty-parts `.` path and invalid repository-
root boundary. The final patch rejects those values before adapter or Git use,
prevalidates mixed record fields before sorting, and fixes the same empty-path
rule in the public rendered-link adapter. The final quality re-review returned
`QUALITY APPROVED`.

The focused ARWB-002 suite passes 22/22 and the combined ARWB-001/002 suite
passes 37/37. The canonical cross-document self-test passes; Ruff check and
format, Python compile, strict registry (`434` paths, `baseline=433`, `new=62`,
two programs, zero uncovered/ambiguous), strict Markdown (zero violations),
strict cross-document validation, changed-document Markdownlint, and
`git diff --check` pass. This is import-only repository-static evidence; it
does not activate a production archive route/form/predicate, inspect or migrate
the 31-record corpus, claim the 202-link proof, retire Tombstones, or inspect
ignored `_workspace` children. The logical commit from parent `6b9b9cd` remains
pending.

Independent requirements review first returned `NOT COMPLIANT` for split
cutover commits, stale successor projections, and missing ARWB-003/005 RED
evidence. After remediation it returned `REQUIREMENTS COMPLIANT`. Independent
quality review then required fixture-only ARWB-001 authority, redacted
in-memory secret classification, and detailed criterion/package navigation;
after remediation it returned `QUALITY APPROVED`.

Repository-static evidence cannot establish remote object retention, GitHub
configuration, provider delivery, live Kubernetes/Vault/ESO/Argo CD state, or
the contents or safety of ignored `_workspace` scratch. Those lanes remain
`DEFER`; no ignored child was read to create this Task.

## Traceability

- **Spec**: [Archive Record and Workspace Boundary](../../03.specs/036-archive-record-and-workspace-boundary/spec.md)
- **Plan**: [Archive Record and Workspace Boundary Implementation Plan](../plans/2026-07-17-archive-record-and-workspace-boundary.md)
- **Predecessor Task**: [Document Schema and Lifecycle Contract Task](./2026-07-16-document-schema-and-lifecycle-contract.md)
- **Decision**: [ADR-0018](../../02.architecture/decisions/0018-full-body-archive-record-and-retention.md)

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [ARWB-001](../plans/2026-07-17-archive-record-and-workspace-boundary.md#arwb-001-recovery-and-envelope-contract) | Done. | Initial, requirements-remediation, and quality-remediation RED evidence is recorded above; the private recovery/envelope suite passes 15/15 with `REQUIREMENTS COMPLIANT` and `QUALITY APPROVED`. Logical commit `6b9b9cd`, parent `04a4d32`. |
| [ARWB-002](../../03.specs/036-archive-record-and-workspace-boundary/spec.md) | In Progress. | Missing-module/nine-failure RED and quality-remediation 17-failure/13-error RED are recorded above; focused 22/22 and combined 37/37 GREEN pass. Verdicts are `REQUIREMENTS COMPLIANT` and `QUALITY APPROVED`; the logical commit from parent `6b9b9cd` remains pending. |
| N/A — ARWB-003 shares the Plan linked in ARWB-001 | Queued. | Atomic cutover RED, exact 31/31 payload, 202/202 source-link, index/current-authority, and Tombstone retirement evidence will be recorded here. |
| N/A — ARWB-004 shares the Plan linked in ARWB-001 | Queued. | Git-metadata-only workspace fixture and no-read review evidence will be recorded here. |
| N/A — ARWB-005 shares the Plan linked in ARWB-001 | Queued. | Incomplete-closure RED, full QA, whole-tranche verdicts, rollback, closure commit, and post-commit checks will be recorded here. |

The lifecycle table renders the Plan and Spec relationship targets once to
preserve exact activation cardinality. The package-level anchors below provide
complete navigation without creating duplicate lifecycle evidence targets.

### Detailed Package Map

| Work package | Plan anchor |
| --- | --- |
| ARWB-001 | [Recovery and envelope capability](../plans/2026-07-17-archive-record-and-workspace-boundary.md#arwb-001-recovery-and-envelope-contract) |
| ARWB-002 | [Archive validators](../plans/2026-07-17-archive-record-and-workspace-boundary.md#arwb-002-archive-validators) |
| ARWB-003 | [Atomic corpus and authority cutover](../plans/2026-07-17-archive-record-and-workspace-boundary.md#arwb-003-atomic-corpus-and-authority-cutover) |
| ARWB-004 | [`_workspace` Git-metadata guard](../plans/2026-07-17-archive-record-and-workspace-boundary.md#arwb-004-_workspace-git-metadata-guard) |
| ARWB-005 | [Validation and lifecycle closure](../plans/2026-07-17-archive-record-and-workspace-boundary.md#arwb-005-validation-and-lifecycle-closure) |
