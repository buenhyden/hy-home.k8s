---
title: 'Task: Template Lifecycle Contract Normalization'
type: sdlc/task
status: done
owner: platform
updated: 2026-07-15
---

# Task: Template Lifecycle Contract Normalization

## Overview

This Task records execution of Spec 033 and its approved Plan. Work is limited
to Stage 99 contract/form normalization, registry and validator enforcement,
current active document migration, and repository-static evidence.

## Inputs

- [Template Lifecycle Contract Normalization Spec](../../03.specs/033-template-lifecycle-contract-normalization/spec.md)
- [Template Lifecycle Contract Normalization Plan](../plans/2026-07-14-template-lifecycle-contract-normalization.md)
- [Current SDLC and Frontmatter Audit](../../90.references/audits/2026-07-11-weia/sdlc-document-lifecycle-frontmatter.md)
- [Current Remediation Roadmap](../../90.references/audits/2026-07-11-weia/remediation-roadmap.md)
- [Document Type Format and Evidence Contract](../../90.references/research/2026-07-07-wer/document-type-format-and-evidence-contract.md)

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| TLCN-001 | VAL-TLCN-001, VAL-TLCN-010 | Establish reciprocal Spec/Plan/Task execution lineage | platform | Done | Spec approval converted into an indexed executable Plan and Task. | `be6dee5`, `8a7560a`; strict document validation. |
| TLCN-002 | VAL-TLCN-001, VAL-TLCN-002, VAL-TLCN-005 | Add schema v5, body contracts, native profiles, and history guard | platform | Done | Registry v5 and registry-derived native mapping implemented; obsolete exhaustive owners removed. | `d9d47b0`, `ff6a813`, `2d95f5a`; 59-case registry self-test. |
| TLCN-003 | VAL-TLCN-002, VAL-TLCN-003 | Separate Stage 99 support and README authority | platform | Done | Support rationale/procedure owners separated and unowned forms rejected. | `543dc61`, `f6cb42a`; exact-one form inventory and conflict scans. |
| TLCN-004 | VAL-TLCN-004, VAL-TLCN-005, VAL-TLCN-006 | Normalize 27 Markdown and three native forms | platform | Done | All canonical forms normalized and authored starter residue rejected. | `a7ff348`, `7bd5644`; form and mutation validation. |
| TLCN-005 | VAL-TLCN-006, VAL-TLCN-007 | Validate lifecycle tables and linked-profile semantics | platform | Done | Local table and cross-document semantic validation implemented and parser edge cases hardened. | `5daf95b`, `5bd2d3c`, `3d0b9a7`, `5764626`, `2cad086`; both validator self-tests. |
| TLCN-006 | VAL-TLCN-007, VAL-TLCN-008, VAL-TLCN-009 | Migrate 13 active Stage 01-03 consumers and correct PRD 003 | platform | Done | Core current consumers migrated; PRD 003 no longer claims Spec 006 as current. | `9c0994f`; scoped core Markdown and cross-document audits. |
| TLCN-007 | VAL-TLCN-007, VAL-TLCN-008 | Migrate 24 active Stage 05 consumers | platform | Done | Operations consumers migrated with Policy/Runbook ownership and desired-state wording corrected. | `8cb3336`, `f8bb825`; scoped operations audits. |
| TLCN-008 | VAL-TLCN-001 through VAL-TLCN-010 | Enable strict enforcement and close audit/execution evidence | platform | Done | Production `draft`/`active` enforcement is complete; independent whole-branch review reported `REQUIREMENTS COMPLIANT` and `QUALITY APPROVED`. | The history guard passed, and the final repository-static lane is the mandatory closure-commit gate. This closure diff and its commit record TLCN-008 but cannot self-reference the closure SHA. |

## Approval and Safety Boundaries

- **Allowed Paths**: `docs/99.templates/**`, Spec 033, the paired Plan/Task and
  indexes, the exact 37 active Stage 01-03/05 consumers, document validators
  and fixtures, Current remediation-roadmap disposition overlay, migration
  ledger, and progress ledger.
- **Forbidden Paths**: Completed PRD/Spec/Plan/Task bodies, accepted ADR bodies,
  secret values, ignored auth/local state, live Kubernetes/GitOps/Vault/ESO,
  and remote repository settings.
- **Approval Required**: New metadata key, status value, document family,
  historical-body rewrite, remote publication, secret access, or live mutation.
- **Static Validation**: Registry, Markdown, links/owners self-tests and strict
  modes, repository quality gate, all-files pre-commit, and diff check.
- **Live Validation**: DEFER; no runtime surface changes are authorized.
- **Secret / Vault Handling**: Do not read, decode, print, or mutate secrets.
- **Rollback Plan**: Revert the failing logical commit; keep production body
  enforcement empty until the current corpus is ready.
- **Evidence Location**: This Task, linked logical commits, the Current audit
  disposition overlay, and the progress ledger.

## Verification Summary

Baseline commit `ac3ba71959ab2672803450588f193749f92a996e` passed registry,
Markdown, cross-document, and repository quality gates. TLCN-001 through
TLCN-008 are complete. Production body checks enforce authored `draft`/`active`
SDLC documents while preserving template parity; scoped/global audits and the
historical-body guard pass. Independent whole-branch review reported
`REQUIREMENTS COMPLIANT` and `QUALITY APPROVED`. The review-preparation
`TMPDIR=/tmp rtk pre-commit run --all-files` completed with exit `0`: all
applicable hooks passed and the Dockerfile hook reported no files and skipped.
The closure committer must rerun the final repository-static lane, including
all-files pre-commit and staged diff checks, after these status/evidence edits
and before creating the non-self-referential closure commit. Repository-static
evidence is the only PASS lane; remote CI, provider runtime, and live state
remain `DEFER`.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [TLCN-001](../plans/2026-07-14-template-lifecycle-contract-normalization.md#work-breakdown) | Spec, Plan, and Task execution lineage established. | Planning commits `be6dee5` and `8a7560a`; strict document validation. |
| [TLCN-002](../plans/2026-07-14-template-lifecycle-contract-normalization.md#work-breakdown) | Registry v5, typed body contracts, native mappings, and independent mutation coverage implemented. | Commits `d9d47b0`, `ff6a813`, and `2d95f5a`; 59-case registry self-test. |
| [TLCN-003](../plans/2026-07-14-template-lifecycle-contract-normalization.md#work-breakdown) | Stage 99 support and README authority separated with exact-one physical form ownership. | Commits `543dc61` and `f6cb42a`; focused ownership and stale-claim checks. |
| [TLCN-004](../plans/2026-07-14-template-lifecycle-contract-normalization.md#work-breakdown) | Twenty-seven Markdown and three native forms normalized; starter residue rejected. | Commits `a7ff348` and `7bd5644`; template/residue self-tests. |
| [TLCN-005](../plans/2026-07-14-template-lifecycle-contract-normalization.md#work-breakdown) | Lifecycle-table and linked-profile semantics implemented and hardened. | Commits `5daf95b`, `5bd2d3c`, `3d0b9a7`, `5764626`, and `2cad086`; local/cross-document self-tests. |
| [TLCN-006](../plans/2026-07-14-template-lifecycle-contract-normalization.md#work-breakdown) | Thirteen current Stage 01-03 consumers migrated and the false PRD 003 Spec pointer removed. | Commit `9c0994f`; scoped core lifecycle audits. |
| [TLCN-007](../plans/2026-07-14-template-lifecycle-contract-normalization.md#work-breakdown) | Twenty-four current operations consumers migrated with truthful desired-state boundaries. | Commits `8cb3336` and `f8bb825`; scoped operations audits. |
| [TLCN-008](../plans/2026-07-14-template-lifecycle-contract-normalization.md#work-breakdown) | Production draft/active enforcement and closure review are complete. | `REQUIREMENTS COMPLIANT`, `QUALITY APPROVED`, passing history guard, and the mandatory final repository-static closure lane; the closure commit cannot self-reference its SHA. |

### Related authority

- **Spec**: [Template Lifecycle Contract Normalization](../../03.specs/033-template-lifecycle-contract-normalization/spec.md)
- **Plan**: [Template Lifecycle Contract Normalization Plan](../plans/2026-07-14-template-lifecycle-contract-normalization.md)
- **Registry ADR**: [Declarative Document Contract Registry](../../02.architecture/decisions/0015-declarative-document-contract-registry.md)
- **Audit roadmap**: [Integrated Remediation Roadmap](../../90.references/audits/2026-07-11-weia/remediation-roadmap.md)
