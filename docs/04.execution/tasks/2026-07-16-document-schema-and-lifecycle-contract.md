---
title: 'Task: Document Schema and Lifecycle Contract'
type: sdlc/task
status: active
owner: platform
updated: 2026-07-17
---

# Task: Document Schema and Lifecycle Contract

## Overview

This Task is the mutable execution and review ledger for DSLC-001 through
DSLC-006 under [Spec 035](../../03.specs/035-document-schema-and-lifecycle-contract/spec.md).
It records test-first results, logical commits, rollback parents, independent
reviews, and explicit static/live evidence boundaries.

## Inputs

- [Implementation Plan](../plans/2026-07-16-document-schema-and-lifecycle-contract.md)
- [Spec 035](../../03.specs/035-document-schema-and-lifecycle-contract/spec.md)
- [PRD-006](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md)
- [ARD-0009](../../02.architecture/requirements/0009-document-lifecycle-evidence-operating-model.md)
- [ADR-0017](../../02.architecture/decisions/0017-program-follow-up-lineage-semantics.md)
- [ADR-0018](../../02.architecture/decisions/0018-full-body-archive-record-and-retention.md)
- [Document type, format, and evidence research](../../90.references/research/2026-07-07-wer/document-type-format-and-evidence-contract.md)
- [Current implementation audit pack](../../90.references/audits/2026-07-11-weia/README.md)

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| DSLC-001 | VAL-DSLC-001, VAL-DSLC-002, VAL-DSLC-003, VAL-DSLC-007, VAL-DSLC-008 | Add closed registry v7 value, role, lifecycle, evidence, and compatibility schema plus typed projection. | platform | Done | Implemented; independent re-review returned `REQUIREMENTS COMPLIANT` and `QUALITY APPROVED`. | RED archive-specific semantics and policy-ID/path-alias bypasses reproduced; GREEN 117-case registry self-test, complete literal typed projection, duplicate-key rejection, strict registry/Markdown/cross PASS; logical commit `5781ea3`. |
| DSLC-002 | VAL-DSLC-001, VAL-DSLC-002, VAL-DSLC-005 | Enforce metadata values, template/source parity, and baseline-only Tombstone admission. | platform | Done | Implemented; independent re-review returned `REQUIREMENTS COMPLIANT` and `QUALITY APPROVED`. | RED seven value-contract cases returned `metadata value rules are unimplemented`; expanded 18-case GREEN covers string/integer/number/boolean/date kinds, profile/literal constants, status/literal enums, scalar patterns, denied/allowed null, equals/not-equals, required/forbidden, and absent-versus-explicit-null references without private archive semantics. Exact 31-path Tombstone compatibility plus explicit untracked include rejection, 11/11 template/source parity mutations including typed value-contract parity, and strict current-corpus/registry/cross PASS are recorded. |
| DSLC-003 | VAL-DSLC-003, VAL-DSLC-004, VAL-DSLC-008 | Implement exact staged, CI, explicit-ref, and snapshot comparison modes and transition graph validation. | platform | Queued | Not executed | Isolated Git fixtures, lifecycle diagnostics, review, commit |
| DSLC-004 | VAL-DSLC-004, VAL-DSLC-008 | Enforce edge-specific rendered-link, state, same-diff, and body-contract evidence. | platform | Queued | Not executed | Predicate mutation matrix, strict cross-document result, review, commit |
| DSLC-005 | VAL-DSLC-005, VAL-DSLC-006, VAL-DSLC-007 | Close native, role/source, Stage 00/99, and directly implicated consumer drift without bulk corpus rewrite. | platform | Queued | Not executed | Native/overlap fixtures, drift ledger, full static result, review, commit |
| DSLC-006 | VAL-DSLC-001 through VAL-DSLC-008 | Run full QA, whole-tranche review, and atomic lifecycle closure. | platform | Queued | Not executed | Done lineage, command matrix, review verdicts, rollback parent, closure commit |

## Approval and Safety Boundaries

- **Allowed Paths**: `docs/00.agent-governance/**` only where named by the
  Plan; `docs/03.specs/035-document-schema-and-lifecycle-contract/**` and its
  Stage 03 index; this Plan/Task and Stage 04 indexes;
  `docs/05.operations/incidents/README.md`; the directly implicated Stage 90
  research ledger/pointer; `docs/99.templates/support/**` and canonical forms
  implicated by v7; `scripts/document_contracts.py`, document/lifecycle/link
  validators and `scripts/README.md`; focused fixtures; program relation and
  migration-ledger closure rows.
- **Forbidden Paths**: Kubernetes/GitOps desired state, infrastructure,
  policies, secrets, provider runtime adapters, generated outputs, accepted or
  completed historical bodies, archive corpus conversion, bulk Stage 05/helper
  body normalization, completed Plan/Task movement, and Spec 036-040 bodies
  except read-only boundary verification.
- **Approval Required**: Any live system, secret, remote GitHub setting, push,
  publication, dependency installation, or scope expansion requires separate
  explicit approval.
- **Static Validation**: Registry, Markdown-profile, lifecycle,
  cross-document, native available-linter, repository-quality, Markdown lint,
  staged diff, and all-files pre-commit commands from the Plan.
- **Live Validation**: DEFER. Spec 035 authorizes no remote/provider/live lane.
- **Secret / Vault Handling**: Do not read, print, move, or infer ignored
  secrets, credentials, tokens, auth files, shell history, kubeconfigs, or
  Vault values.
- **Rollback Plan**: Before closure, revert the newest open DSLC package first
  and remove v7 consumers before v7 schema/data. After DSLC-006, do not reopen
  terminal evidence in isolation: apply DSLC-006 through DSLC-001 newest-first
  with `git revert --no-commit`, validate only the complete staged v6/active
  state, and create one atomic rollback commit. Record every commit parent in
  this Task.
- **Evidence Location**: This Task, logical Git commits, focused fixtures,
  validator outputs summarized here, and the durable migration ledger.

## Verification Summary

Planning baseline: registry v6 classifies 430 paths through 64 profiles and 30
templates with zero uncovered or ambiguous routes. Registry self-test has 78
cases; cross-document self-test has 344 cases. Current frontmatter/profile
validation passes. No Spec 035 implementation work has run yet. The isolated
filesystem reproduces one known `os.mkfifo` `Errno 95` in the all-files
repository-quality hook; Spec 039 owns that portability fix, and it may be
recorded as DEFER only when every other hook passes.

Planning review first rejected underspecified creation/movement admission,
edge evidence, Git comparison interfaces, native syntax claims, closure order,
null-body profile handling, and post-closure rollback. The remediated Plan now
owns exact admission defaults, an edge/predicate matrix, the lifecycle
module/CLI/fixture and exit contract, staged closure review, explicit native
syntax DEFER, heading-set predicates for null-body profiles, and one atomic
post-closure rollback. Independent re-review returned
`REQUIREMENTS COMPLIANT` and `QUALITY APPROVED`. The staged planning set passes
strict registry, Markdown-profile, cross-document, diff-check, and changed-file
Markdown lint validation.

DSLC-001 RED failed on the first newly declared v7 mutation because the v6
self-test had no mutation implementation. GREEN upgrades production to closed
registry v7, exposes immutable value/role/admission/lifecycle/evidence
projections, checks every production edge against exactly one predicate case,
and pins the 31 tracked Tombstones to baseline-only admission. The registry
rejects duplicate JSON keys at root or nested depth, noncanonical Tombstone
baseline spellings, and archive-specific value semantics before Spec 036.
Registry self-test passes 117 cases with the complete literal
64-profile/30-template projection, every admission/lifecycle/evidence field,
generic private-fixture conditional semantics, and private v5/v6 migration
proof. Strict registry validates 432 paths; strict
Markdown reports zero violations and strict cross-document validation passes.
No lifecycle Git comparison, metadata enforcement, evidence resolution, corpus
rewrite, archive route, or CI change is claimed by this package.

Independent review first rejected archive-specific value ownership, partial
predicate projection, duplicate-key JSON parsing, and noncanonical Tombstone
path aliases. Remediation removed production archive literal/conditional
semantics, added a complete independent literal projection and schema-valid
semantic-drift mutations, centralized duplicate-key-rejecting JSON loading,
and checked raw Tombstone paths by exact profile membership. A second review
found the combined policy-ID rename plus `//` alias bypass; the 117th mutation
reproduces and closes it. Final re-review returned `REQUIREMENTS COMPLIANT` and
`QUALITY APPROVED`.

DSLC-002 RED added production-derived value-contract cases; all seven initial
cases failed because metadata value rules were unimplemented. Review
remediation expanded GREEN to an exact 18-case value matrix. Generic
literal-constant, literal-enum, and conditional capabilities use only the
ordinary five-key `sdlc/spec` profile and introduce no private Tombstone reason,
replacement, or archived-state semantics. The matrix evaluates string,
integer, number, boolean, and date kinds; profile/literal constants;
status/literal enums; patterns over canonical scalar text; denied and allowed
nulls; both conditional operators and effects; and the intentional distinction
between an absent reference (no match) and an explicit null reference (eligible
to match). Established title, type, status, owner, and date rule IDs remain
stable. Ordinary authored documents still have the five ordered keys,
templates alone retain starter/date placeholders, and the strict current
corpus has zero violations. A baseline-only admission check
keeps the exact 31 tracked Tombstones readable and rejects copied, renamed, or
explicitly included untracked Tombstone paths. The registry self-test adds a
11/11 independent template/source parity matrix for frontmatter, order,
status, headings, class, body contract, typed value contract, source
cardinality, missing source, duplicate source, and unknown source. Focused
self-tests, strict registry, strict Markdown, and strict cross-document
validation pass. Independent re-review returned `REQUIREMENTS COMPLIANT` and
`QUALITY APPROVED`; the logical DSLC-002 commit records this evidence.

## Traceability

- **Spec**: [Spec 035](../../03.specs/035-document-schema-and-lifecycle-contract/spec.md)
- **Plan**: [Implementation Plan](../plans/2026-07-16-document-schema-and-lifecycle-contract.md)
- **Predecessor Task**: [Spec 034 execution evidence](./2026-07-15-authority-and-lineage-foundation.md)

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [DSLC-001](../plans/2026-07-16-document-schema-and-lifecycle-contract.md#dslc-001-registry-v7-contract) | Done; requirements compliant and quality approved. | RED review reproductions; GREEN 117 registry cases, complete literal v7 typed projection, strict 432-path registry, Markdown zero violations, cross-document PASS, and duplicate/canonical-path guards. |
| [DSLC-002](../plans/2026-07-16-document-schema-and-lifecycle-contract.md#dslc-002-metadata-template-and-compatibility-enforcement) | Done; requirements compliant and quality approved. | Initial seven-case RED; exact 18-case selected v7 value matrix without private archive semantics, 31-path baseline-only admission plus explicit untracked include proof, 11/11 template/source parity mutations including typed value parity, strict current-corpus PASS, and independent review closure. |
| [DSLC-003](../plans/2026-07-16-document-schema-and-lifecycle-contract.md#dslc-003-base-and-transition-engine) | Queued. | Git base-mode and transition evidence will be recorded here. |
| [DSLC-004](../plans/2026-07-16-document-schema-and-lifecycle-contract.md#dslc-004-transition-evidence) | Queued. | Edge predicate and cross-document evidence will be recorded here. |
| [DSLC-005](../plans/2026-07-16-document-schema-and-lifecycle-contract.md#dslc-005-native-role-and-support-drift) | Queued. | Native, role, support, and consumer-drift evidence will be recorded here. |
| [DSLC-006](../plans/2026-07-16-document-schema-and-lifecycle-contract.md#dslc-006-closure) | Queued. | Full QA, independent reviews, and atomic closure evidence will be recorded here. |
