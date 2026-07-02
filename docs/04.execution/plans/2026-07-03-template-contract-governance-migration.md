---
title: 'Template Contract and Governance Migration Implementation Plan'
type: sdlc/plan
status: draft
owner: platform
updated: 2026-07-03
---

# Template Contract and Governance Migration Implementation Plan

## Overview

This document defines the implementation plan for migrating
`docs/99.templates/` from a flat template inventory into separated template
forms, support contracts, and governance-backed validation. It turns the parent
Stage 03 spec into reviewable logical commits and static verification gates.

## Context

The current template system keeps Markdown, YAML, GraphQL, and protobuf
templates flat under `docs/99.templates/`. Governance, routing policy,
frontmatter expectations, and template inventory are mixed across the template
README, Stage 00 rules, hook hints, validators, and authored stage README
links. The approved migration separates template forms under
`docs/99.templates/templates/**` from support contracts under
`docs/99.templates/support/**`, then updates validation and authored documents
to match.

## Goals & In-Scope

- **Goals**:
  - Create support contracts for template routing, frontmatter profiles,
    documentation contracts, SDLC governance, and legacy cleanup rules.
  - Move template files into categorized `templates/sdlc/**` and
    `templates/common/**` folders.
  - Update Stage 00 governance, pre-edit hooks, quality gates, README indexes,
    and authored document links to the new paths.
  - Normalize frontmatter and legacy references according to the parent spec.
  - Keep every migration phase reviewable as a logical commit.
- **In Scope**:
  - `docs/99.templates/**`
  - `docs/00.agent-governance/rules/**`
  - `docs/00.agent-governance/hooks/k8s-pre-edit.sh`
  - `scripts/validate-repo-quality-gates.sh`
  - Stage README and authored docs that reference old template paths or legacy
    frontmatter/contracts.
  - Progress ledger updates for repo-changing work.

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Live cluster, Vault, ArgoCD, ESO, GitHub remote, or cloud validation.
  - External publishing or paid remote jobs.
  - Runtime behavior changes outside documentation and validation surfaces.
  - Broad prose rewrites unrelated to template contracts.
- **Out of Scope**:
  - Secrets or credential inspection.
  - Remote CI topology changes.
  - New documentation stages outside the canonical `docs/` taxonomy.

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | Create support contract baseline | `docs/99.templates/support/**`, `docs/99.templates/README.md`, progress ledger | VAL-SPC-001, VAL-SPC-003 | Support docs exist, README is inventory-oriented, quality gate passes |
| PLN-002 | Move template forms into categorized folders | `docs/99.templates/templates/**`, removed flat template paths | VAL-SPC-002, VAL-SPC-008 | `git mv` preserves history, no active route depends on removed flat paths |
| PLN-003 | Update routing, hooks, and validator surfaces | Stage 00 rules, `k8s-pre-edit.sh`, `validate-repo-quality-gates.sh` | VAL-SPC-004, VAL-SPC-005, VAL-SPC-006 | Quality gate enforces new paths and rejects legacy routes |
| PLN-004 | Normalize template frontmatter and contracts | Template files, support schema, validator checks | VAL-SPC-005, VAL-SPC-007 | Type/profile rules are deterministic and machine-readable templates stay native |
| PLN-005 | Apply migration to authored docs and indexes | Stage READMEs, authored docs, references, progress ledger | VAL-SPC-007, VAL-SPC-008 | Old template links and legacy active sections are removed or routed |
| PLN-006 | Final validation and completion sync | Plan, task, progress ledger, README indexes | VAL-SPC-009 | `git diff --check` and repo quality gates pass |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Static | Check whitespace and patch safety | `git diff --check` | No whitespace errors |
| VAL-PLN-002 | Static | Run repository quality gates | `bash scripts/validate-repo-quality-gates.sh .` | PASS |
| VAL-PLN-003 | Static | Enforce legacy denylist | `bash scripts/validate-repo-quality-gates.sh .` | No active legacy template route, owner value, or README heading literals after Phase 3 |
| VAL-PLN-004 | Static | Find flat template path references | `rg -n "docs/99\\.templates/[a-z0-9-]+\\.template\\.(md|yaml|graphql|proto)" docs scripts .codex AGENTS.md RTK.md` | No active flat-path routes after Phase 2 except documented historical evidence if allow-listed |
| VAL-PLN-005 | Static | Inspect template tree | `find docs/99.templates -maxdepth 5 -type f -print | sort` | Templates and support docs are in approved folders |
| VAL-PLN-006 | Review | Confirm README/support separation | Manual diff review | README links to contracts without duplicating detailed contract sections |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Existing validator assumes flat template files | High | Update validator in the same commit as path migration and rerun quality gates. |
| Stage README links break after file moves | High | Recalculate every relative link from the final document location and rely on quality gates. |
| Frontmatter migration touches too many authored docs | Medium | Split by profile or stage if needed while preserving the approved four-phase boundary. |
| Historical progress entries contain old terms | Medium | Reject active contract references first and allow dated historical evidence only when explicitly documented. |
| Machine-readable templates become invalid | High | Do not add Markdown frontmatter to YAML, GraphQL, or protobuf contract templates. |

## Agent Rollout & Evaluation Gates

- **Offline Eval Gate**: Static repository quality gates and legacy-reference
  searches.
- **Sandbox / Canary Rollout**: Not applicable. This is a repository-static
  documentation and validation migration.
- **Human Approval Gate**: Required before any push, remote action, live
  runtime validation, external publishing, secret access, or paid job. Local
  edits and static validation are already approved by this plan.
- **Rollback Trigger**: Revert or repair the current logical commit if the
  repository quality gate cannot identify unique template routes or if moved
  machine-readable templates become invalid.
- **Prompt / Model Promotion Criteria**: Not applicable.

## Completion Criteria

- [ ] Support contract baseline completed.
- [ ] Template forms moved to categorized folders.
- [ ] Stage 00 routing, hooks, and validators updated.
- [ ] Template frontmatter and contracts normalized.
- [ ] Authored docs and README indexes updated.
- [ ] Required validation commands pass.
- [ ] Plan, task, and progress ledger record final evidence.

## Related Documents

- **Spec**: [../../03.specs/011-template-contract-governance-migration/spec.md](../../03.specs/011-template-contract-governance-migration/spec.md)
- **Tasks**: [../tasks/2026-07-03-template-contract-governance-migration.md](../tasks/2026-07-03-template-contract-governance-migration.md)
- **Templates README**: [../../99.templates/README.md](../../99.templates/README.md)
- **Documentation Protocol**: [../../00.agent-governance/rules/documentation-protocol.md](../../00.agent-governance/rules/documentation-protocol.md)
- **Document Stage Routing Rules**: [../../00.agent-governance/rules/document-stage-routing.md](../../00.agent-governance/rules/document-stage-routing.md)
- **Quality Gate**: [../../../scripts/validate-repo-quality-gates.sh](../../../scripts/validate-repo-quality-gates.sh)
