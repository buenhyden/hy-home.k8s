---
title: 'Task: Template Contract and Governance Migration'
type: sdlc/task
status: done
owner: platform
updated: 2026-07-13
---

# Task: Template Contract and Governance Migration

## Overview

This document tracks implementation and verification work for the template
contract and governance migration. It keeps task evidence tied to the parent
spec and plan while preserving logical commit boundaries.

## Inputs

- **Parent Spec**: [../../03.specs/011-template-contract-governance-migration/spec.md](../../03.specs/011-template-contract-governance-migration/spec.md)
- **Parent Plan**: [../plans/2026-07-03-template-contract-governance-migration.md](../plans/2026-07-03-template-contract-governance-migration.md)

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Create Stage 04 plan/task tracking for the migration | doc | Related Documents | PLN-006 | `git diff --check` PASS; repo quality gate PASS; English-first scan PASS | platform | Done |
| T-002 | Create support contract baseline under `docs/99.templates/support/**` | doc | VAL-SPC-001, VAL-SPC-003 | PLN-001 | Support docs exist; `git diff --check` PASS; repo quality gate PASS | platform | Done |
| T-003 | Move template forms into `docs/99.templates/templates/**` | doc | VAL-SPC-002, VAL-SPC-008 | PLN-002 | `git mv`; template tree review; `git diff --check` PASS; repo quality gate PASS | platform | Done |
| T-004 | Update routing, hook, validator, and governance references | impl | VAL-SPC-004, VAL-SPC-005, VAL-SPC-006 | PLN-003 | Active legacy path search PASS; `git diff --check` PASS; repo quality gate PASS | platform | Done |
| T-005 | Normalize frontmatter profiles and remove active legacy values | doc | VAL-SPC-005, VAL-SPC-007 | PLN-004 | Schema review; legacy value searches PASS; `git diff --check` PASS; repo quality gate PASS | platform | Done |
| T-006 | Apply new template links/contracts to authored docs and indexes | doc | VAL-SPC-007, VAL-SPC-008 | PLN-005 | Authored docs and index review PASS; repo quality gate PASS | platform | Done |
| T-007 | Final validation and handoff sync | qa | VAL-SPC-009 | PLN-006 | Final validation commands PASS; progress ledger evidence recorded | platform | Done |

### Phase View

### Phase 0: Planning

- [x] T-001 Create Stage 04 plan/task tracking for the migration.

### Phase 1: Support Contract Baseline

- [x] T-002 Create support contract baseline under `docs/99.templates/support/**`.

### Phase 2: Template Path Migration

- [x] T-003 Move template forms into `docs/99.templates/templates/**`.
- [x] T-004 Update routing, hook, validator, and governance references.

### Phase 3: Frontmatter and Legacy Cleanup

- [x] T-005 Normalize frontmatter profiles and remove active legacy values.

### Phase 4: Authored Docs Application and Final Sync

- [x] T-006 Apply new template links/contracts to authored docs and indexes.
- [x] T-007 Final validation and handoff sync.

## Approval and Safety Boundaries

- **Allowed Paths**: `T-001 through T-007` is limited to these Template Contract and Governance Migration owners and Task-Table surfaces:
  - `docs/04.execution/tasks/2026-07-03-template-contract-governance-migration.md`
  - `docs/03.specs/011-template-contract-governance-migration/spec.md`
  - `docs/04.execution/plans/2026-07-03-template-contract-governance-migration.md`
  - `docs/99.templates/support/**`
  - `docs/99.templates/templates/**`
- **Forbidden Paths**: runtime manifests, provider or CI settings, secret values, generated/local state, and paths outside the Template Contract and Governance Migration work items and linked evidence owners.
- **Approval Required**: Human approval is required before Template Contract and Governance Migration protected-file expansion, deletion/relocation, runtime/CI/provider mutation, credential access, publication, push, or merge beyond the parent Plan.
- **Static Validation**: Preserve the Template Contract and Governance Migration outcomes and limitations recorded in Verification Summary; use these recorded checks:
  - `git diff --check`
  - `bash scripts/validate-repo-quality-gates.sh .`
  - `rg -n "\\p{Hangul}" docs/04.execution/plans/2026-07-03-template-contract-governance-migration.md docs/04.execution/tasks/2026-07-03-template-contract-governance-migration.md`
  - `rg -n "docs/99\\.templates/[a-z0-9-]+\\.template\\.(md|yaml|graphql|proto)" docs scripts .codex AGENTS.md RTK.md`
- **Live Validation**: DEFER — Template Contract and Governance Migration is closed by repository-static/documentation evidence; historical live commands, if any, are not authority for a new cluster, provider, external-service, or deployment claim.
- **Secret / Vault Handling**: No secret value is required for Template Contract and Governance Migration; do not read or print tokens, credentials, Vault/Kubernetes Secret data, kubeconfigs, auth files, private logs, or shell history.
- **Rollback Plan**: Revert the logical Template Contract and Governance Migration change set for `T-001 through T-007` and restore its allowed implementation/evidence paths with this Task and parent Plan; documentation rollback does not authorize live mutation.
- **Evidence Location**: Durable Template Contract and Governance Migration evidence remains in:
  - `docs/04.execution/tasks/2026-07-03-template-contract-governance-migration.md`
  - `docs/03.specs/011-template-contract-governance-migration/spec.md`
  - `docs/04.execution/plans/2026-07-03-template-contract-governance-migration.md`

## Verification Summary

- **Test Commands**:
  - `git diff --check`
  - `bash scripts/validate-repo-quality-gates.sh .`
  - `rg -n "\\p{Hangul}" docs/04.execution/plans/2026-07-03-template-contract-governance-migration.md docs/04.execution/tasks/2026-07-03-template-contract-governance-migration.md`
  - Legacy denylist scan is enforced by `bash scripts/validate-repo-quality-gates.sh .`
  - Simple-type, quoted-owner, and generator-key scans are enforced by `bash scripts/validate-repo-quality-gates.sh .`
  - `rg -n "docs/99\\.templates/[a-z0-9-]+\\.template\\.(md|yaml|graphql|proto)" docs scripts .codex AGENTS.md RTK.md`
  - `find docs/99.templates -maxdepth 5 -type f -print | sort`
- **Eval Commands**: Not applicable; this is a static documentation and
  validation migration.
- **Logs / Evidence Location**: This task record, the progress ledger, and
  commit history. T-001 through T-007 validation passed before their
  logical-unit commits.

## Traceability

- **Spec**: [../../03.specs/011-template-contract-governance-migration/spec.md](../../03.specs/011-template-contract-governance-migration/spec.md)
- **Plan**: [../plans/2026-07-03-template-contract-governance-migration.md](../plans/2026-07-03-template-contract-governance-migration.md)
- **Templates README**: [../../99.templates/README.md](../../99.templates/README.md)
- **Quality Gate**: [../../../scripts/validate-repo-quality-gates.sh](../../../scripts/validate-repo-quality-gates.sh)
