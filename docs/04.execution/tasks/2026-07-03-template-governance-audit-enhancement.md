---
title: 'Task: Template Governance Audit Enhancement'
type: sdlc/task
status: draft
owner: platform
updated: 2026-07-03
---

# Task: Template Governance Audit Enhancement

## Overview

This document tracks implementation and verification work for the follow-up
audit and targeted enhancement pass over `docs/99.templates/**`. It keeps
findings, remediation tasks, validation evidence, and final handoff tied to the
approved Stage 03 spec and Stage 04 plan.

## Inputs

- **Parent Spec**: [../../03.specs/012-template-governance-audit-enhancement/spec.md](../../03.specs/012-template-governance-audit-enhancement/spec.md)
- **Parent Plan**: [../plans/2026-07-03-template-governance-audit-enhancement.md](../plans/2026-07-03-template-governance-audit-enhancement.md)
- **Template README**: [../../99.templates/README.md](../../99.templates/README.md)
- **Template Routing Contract**: [../../99.templates/support/template-routing.md](../../99.templates/support/template-routing.md)
- **Frontmatter Schema**: [../../99.templates/support/frontmatter-schema.md](../../99.templates/support/frontmatter-schema.md)
- **Quality Gate**: [../../../scripts/validate-repo-quality-gates.sh](../../../scripts/validate-repo-quality-gates.sh)

## Working Rules

- Keep this work repo-static unless the user separately approves a remote or
  live-runtime action.
- Treat support contracts as the expected behavior for template forms.
- Record each finding with evidence, expected contract, observed state, risk,
  action, validation command, and status.
- Add validator rules only when the rule is deterministic and rooted in a
  documented support or Stage 00 contract.
- Do not rewrite topic content in authored documents unless a concrete
  template-governance finding requires it.
- Run `git diff --check` and
  `bash scripts/validate-repo-quality-gates.sh .` before every logical commit.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Create Stage 04 plan, task record, README index entries, and progress entry | doc | Contracts / Data Modeling | PLN-001 | `git diff --check`; `bash scripts/validate-repo-quality-gates.sh .` | platform | Done |
| T-002 | Run baseline route, frontmatter, residue, support, and incident-path scans | eval | Audit Dimensions | PLN-002 | Finding ledger rows FND-001 through FND-004 | platform | Todo |
| T-003 | Remediate current support contract drift and harness task route ambiguity | doc | Contracts / Core Design | PLN-003, PLN-004 | Focused support scan and quality gate | platform | Todo |
| T-004 | Add deterministic validator guardrails for stable support drift patterns | guardrail | Evaluation / Verification Commands | PLN-005 | Quality gate PASS and focused negative-risk review | platform | Todo |
| T-005 | Verify authored documents and template use after remediation | eval | Guardrails / Success Criteria | PLN-006 | Residue, flat-route, incident-route, and frontmatter scans | platform | Todo |
| T-006 | Record final validation evidence and mark Plan, Task, README indexes, and progress complete | doc | Success Criteria | PLN-006 | Final validation summary and completion commit | platform | Todo |

## Suggested Types

- `doc` for support contract, README, plan, task, and progress updates.
- `eval` for route, residue, frontmatter, incident-path, and external-source
  evidence scans.
- `guardrail` for repository quality gate enhancements.

## Audit Finding Ledger

| Finding ID | Scope | Evidence Path | Expected Contract | Observed State | Risk | Action | Validation | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FND-001 | support | `docs/99.templates/support/frontmatter-schema.md`; `docs/99.templates/support/legacy-cleanup-rules.md`; `docs/99.templates/support/template-routing.md`; `docs/99.templates/support/README.md` | Active support docs describe current steady-state contracts | Some wording still describes completed migration phases or current-vs-target schema language | Medium | doc-sync | `rg -n "Phase [1-4]\|during the migration\|after Phase\|current and target" docs/99.templates/support` | Open |
| FND-002 | support | `docs/99.templates/support/template-routing.md`; `docs/99.templates/support/sdlc-governance.md` | `task.template.md` is the only structural route for `docs/04.execution/tasks/*.md` | `harness-task-contract.template.md` can read as an overlapping route instead of a supplemental starter | Medium | doc-sync | `rg -n "YYYY-MM-DD-<harness-task>.*harness-task-contract\|harness-task-contract.*YYYY-MM-DD-<harness-task>" docs/99.templates/support/template-routing.md docs/99.templates/support/sdlc-governance.md` | Open |
| FND-003 | validator | `scripts/validate-repo-quality-gates.sh` | Stable support-contract drift should fail deterministically | Current validation checks frontmatter, route coverage, and residue, but not stale migration-phase wording in support docs | Low | validator-fix | `bash scripts/validate-repo-quality-gates.sh .` | Open |
| FND-004 | authored-doc | `docs/**`; `.codex/**`; `.agents/**`; `AGENTS.md`; `RTK.md` | Authored docs retain no active template residue, flat template routes, or legacy incident path rules | Pending focused scan in T-005 | Low | no-change | `rg -n -e "Target: docs[/]" -e "Use this te[m]plate" docs --glob "*.md" --glob "!docs/99.templates/**"` | Open |

## Phase View

### Phase 1: Planning Baseline

- [ ] T-001 Create and validate planning artifacts.

### Phase 2: Audit Evidence

- [ ] T-002 Run baseline scans and refine finding ledger.

### Phase 3: Targeted Remediation

- [ ] T-003 Remediate support contract drift.
- [ ] T-004 Add validator guardrails.

### Phase 4: Verification And Handoff

- [ ] T-005 Verify authored document usage.
- [ ] T-006 Complete final sync and evidence.

## Verification Summary

- **Test Commands**:
  - `git diff --check`
  - `bash scripts/validate-repo-quality-gates.sh .`
- **Eval Commands**:
  - `find docs/99.templates -maxdepth 5 -type f -print | sort`
  - `rg -n "Phase [1-4]|during the migration|after Phase|current and target" docs/99.templates/support`
  - `rg -n -e "Target: docs[/]" -e "Use this te[m]plate" docs --glob "*.md" --glob "!docs/99.templates/**"`
  - `rg -n "docs/99\\.templates/[a-z0-9-]+\\.template\\.(md|yaml|graphql|proto)" docs scripts .codex .agents AGENTS.md RTK.md`
- **Logs / Evidence Location**:
  - T-001 planning evidence: `git diff --check` passed.
  - T-001 planning evidence:
    `bash scripts/validate-repo-quality-gates.sh .` passed.
  - T-001 planning evidence: Stage 04 Korean text scan returned no matches.
  - Remediation and final evidence will be appended to this section during
    T-002 through T-006.

## Related Documents

- **Spec**: [../../03.specs/012-template-governance-audit-enhancement/spec.md](../../03.specs/012-template-governance-audit-enhancement/spec.md)
- **Plan**: [../plans/2026-07-03-template-governance-audit-enhancement.md](../plans/2026-07-03-template-governance-audit-enhancement.md)
- **Template Contract Migration Plan**: [../plans/2026-07-03-template-contract-governance-migration.md](../plans/2026-07-03-template-contract-governance-migration.md)
- **Template Contract Migration Task**: [./2026-07-03-template-contract-governance-migration.md](./2026-07-03-template-contract-governance-migration.md)
- **Templates README**: [../../99.templates/README.md](../../99.templates/README.md)
- **Documentation Protocol**: [../../00.agent-governance/rules/documentation-protocol.md](../../00.agent-governance/rules/documentation-protocol.md)
- **Document Stage Routing Rules**: [../../00.agent-governance/rules/document-stage-routing.md](../../00.agent-governance/rules/document-stage-routing.md)
