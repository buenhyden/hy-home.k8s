---
title: 'Task: Template Contract and Governance Migration'
type: task
status: draft
owner: platform
updated: 2026-07-03
---

# Task: Template Contract and Governance Migration

## Overview

This document tracks implementation and verification work for the template
contract and governance migration. It keeps task evidence tied to the parent
spec and plan while preserving logical commit boundaries.

## Inputs

- **Parent Spec**: [../../03.specs/011-template-contract-governance-migration/spec.md](../../03.specs/011-template-contract-governance-migration/spec.md)
- **Parent Plan**: [../plans/2026-07-03-template-contract-governance-migration.md](../plans/2026-07-03-template-contract-governance-migration.md)

## Working Rules

- Documentation-only work still needs validation evidence.
- Keep SDLC support contracts, template forms, and governance rules separated.
- Use `git mv` for template movement so file history remains reviewable.
- Update validators and hook hints in the same logical unit as route-breaking
  path changes.
- Do not report static repository validation as live runtime readiness.
- Do not perform live cluster, Vault, ArgoCD, ESO, GitHub remote, cloud,
  external publishing, paid job, or secret-value actions for this task.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Create Stage 04 plan/task tracking for the migration | doc | Related Documents | PLN-006 | `git diff --check` PASS; repo quality gate PASS; English-first scan PASS | platform | Done |
| T-002 | Create support contract baseline under `docs/99.templates/support/**` | doc | VAL-SPC-001, VAL-SPC-003 | PLN-001 | Support docs exist and quality gate passes | platform | Todo |
| T-003 | Move template forms into `docs/99.templates/templates/**` | doc | VAL-SPC-002, VAL-SPC-008 | PLN-002 | `git mv`; template tree review; quality gate | platform | Todo |
| T-004 | Update routing, hook, validator, and governance references | impl | VAL-SPC-004, VAL-SPC-005, VAL-SPC-006 | PLN-003 | Legacy path searches; quality gate | platform | Todo |
| T-005 | Normalize frontmatter profiles and remove active legacy values | doc | VAL-SPC-005, VAL-SPC-007 | PLN-004 | Schema review; legacy value searches; quality gate | platform | Todo |
| T-006 | Apply new template links/contracts to authored docs and indexes | doc | VAL-SPC-007, VAL-SPC-008 | PLN-005 | Stage README/doc diff review; quality gate | platform | Todo |
| T-007 | Final validation and handoff sync | qa | VAL-SPC-009 | PLN-006 | Final validation commands and progress ledger evidence | platform | Todo |

## Suggested Types

- `doc`
- `impl`
- `qa`

## Agent-specific Types (If Applicable)

- `guardrail`
- `eval`
- `observability`

## Phase View

### Phase 0: Planning

- [x] T-001 Create Stage 04 plan/task tracking for the migration.

### Phase 1: Support Contract Baseline

- [ ] T-002 Create support contract baseline under `docs/99.templates/support/**`.

### Phase 2: Template Path Migration

- [ ] T-003 Move template forms into `docs/99.templates/templates/**`.
- [ ] T-004 Update routing, hook, validator, and governance references.

### Phase 3: Frontmatter and Legacy Cleanup

- [ ] T-005 Normalize frontmatter profiles and remove active legacy values.

### Phase 4: Authored Docs Application and Final Sync

- [ ] T-006 Apply new template links/contracts to authored docs and indexes.
- [ ] T-007 Final validation and handoff sync.

## Verification Summary

- **Test Commands**:
  - `git diff --check`
  - `bash scripts/validate-repo-quality-gates.sh .`
  - `rg -n "\\p{Hangul}" docs/04.execution/plans/2026-07-03-template-contract-governance-migration.md docs/04.execution/tasks/2026-07-03-template-contract-governance-migration.md`
  - `rg -n "operation\\.template\\.md|platform-team|Related References" docs scripts .codex AGENTS.md RTK.md`
  - `rg -n "docs/99\\.templates/[a-z0-9-]+\\.template\\.(md|yaml|graphql|proto)" docs scripts .codex AGENTS.md RTK.md`
  - `find docs/99.templates -maxdepth 5 -type f -print | sort`
- **Eval Commands**: Not applicable; this is a static documentation and
  validation migration.
- **Logs / Evidence Location**: This task record, the progress ledger, and
  commit history. T-001 validation passed before the planning logical-unit
  commit.

## Related Documents

- **Spec**: [../../03.specs/011-template-contract-governance-migration/spec.md](../../03.specs/011-template-contract-governance-migration/spec.md)
- **Plan**: [../plans/2026-07-03-template-contract-governance-migration.md](../plans/2026-07-03-template-contract-governance-migration.md)
- **Templates README**: [../../99.templates/README.md](../../99.templates/README.md)
- **Quality Gate**: [../../../scripts/validate-repo-quality-gates.sh](../../../scripts/validate-repo-quality-gates.sh)
