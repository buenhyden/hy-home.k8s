---
title: 'Task: Template Lifecycle Contract Normalization'
type: sdlc/task
status: active
owner: platform
updated: 2026-07-14
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
| TLCN-001 | VAL-TLCN-001, VAL-TLCN-010 | Establish reciprocal Spec/Plan/Task execution lineage | platform | Done | Spec approval converted into an indexed executable Plan and Task | Planning commit and strict document validation |
| TLCN-002 | VAL-TLCN-001, VAL-TLCN-002, VAL-TLCN-005 | Add schema v5, body contracts, native profiles, and history guard | platform | Queued | Not executed | Registry RED/GREEN tests and commit |
| TLCN-003 | VAL-TLCN-002, VAL-TLCN-003 | Separate Stage 99 support and README authority | platform | Queued | Not executed | Focused conflict scans and commit |
| TLCN-004 | VAL-TLCN-004, VAL-TLCN-005, VAL-TLCN-006 | Normalize 27 Markdown and three native forms | platform | Queued | Not executed | Template/residue tests and commit |
| TLCN-005 | VAL-TLCN-006, VAL-TLCN-007 | Validate lifecycle tables and linked-profile semantics | platform | Queued | Not executed | Local/cross-document fixtures and commit |
| TLCN-006 | VAL-TLCN-007, VAL-TLCN-008, VAL-TLCN-009 | Migrate 13 active Stage 01-03 consumers and correct PRD 003 | platform | Queued | Not executed | Strict core lifecycle validation and commit |
| TLCN-007 | VAL-TLCN-007, VAL-TLCN-008 | Migrate 24 active Stage 05 consumers | platform | Queued | Not executed | Strict operations validation and commit |
| TLCN-008 | VAL-TLCN-001 through VAL-TLCN-010 | Enable strict enforcement and close audit/execution evidence | platform | Queued | Not executed | Full gates, historical diff proof, independent review, and closure commit |

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

Baseline commit `ac3ba71959ab2672803450588f193749f92a996e` passes registry,
Markdown, cross-document, and repository quality gates. Targeted planning-file
pre-commit passes with `TMPDIR=/tmp`; the worktree filesystem itself does not
support the FIFO used by one GitOps self-test. Implementation results remain
queued after TLCN-001.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [VAL-TLCN-001 through VAL-TLCN-010](../../03.specs/033-template-lifecycle-contract-normalization/spec.md#success-criteria--verification-plan) | TLCN-001 complete; TLCN-002 through TLCN-008 queued | [Implementation Plan](../plans/2026-07-14-template-lifecycle-contract-normalization.md) |

### Related authority

- **Spec**: [Template Lifecycle Contract Normalization](../../03.specs/033-template-lifecycle-contract-normalization/spec.md)
- **Plan**: [Template Lifecycle Contract Normalization Plan](../plans/2026-07-14-template-lifecycle-contract-normalization.md)
- **Registry ADR**: [Declarative Document Contract Registry](../../02.architecture/decisions/0015-declarative-document-contract-registry.md)
- **Audit roadmap**: [Integrated Remediation Roadmap](../../90.references/audits/2026-07-11-weia/remediation-roadmap.md)
