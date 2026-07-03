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
| T-002 | Run baseline route, frontmatter, residue, support, and incident-path scans | eval | Audit Dimensions | PLN-002 | Finding ledger rows FND-001 through FND-004 | platform | Done |
| T-003 | Remediate current support contract drift and harness task route ambiguity | doc | Contracts / Core Design | PLN-003, PLN-004 | Focused support scan and quality gate | platform | Done |
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
| FND-001 | support | `docs/99.templates/support/frontmatter-schema.md`; `docs/99.templates/support/legacy-cleanup-rules.md`; `docs/99.templates/support/template-routing.md`; `docs/99.templates/support/README.md` | Active support docs describe current steady-state contracts | Support docs now describe current frontmatter, cleanup, and route enforcement contracts without completed migration-phase wording. | Medium | doc-sync | `rg -n "Phase [1-4]\|during the migration\|after Phase\|current and target" docs/99.templates/support` | Resolved |
| FND-002 | support | `docs/99.templates/README.md`; `docs/99.templates/support/template-routing.md`; `docs/99.templates/support/sdlc-governance.md`; `scripts/validate-repo-quality-gates.sh` | `task.template.md` is the only structural route for `docs/04.execution/tasks/*.md`; the harness task contract is supplemental | Support route tables now keep only the Stage 04 Task structural mapping, while supplemental starter notes clarify the harness contract placement. | Medium | doc-sync | `rg -n "YYYY-MM-DD-<harness-task>.*harness-task-contract\|harness-task-contract.*YYYY-MM-DD-<harness-task>" docs/99.templates/support/template-routing.md docs/99.templates/support/sdlc-governance.md` | Resolved |
| FND-003 | validator | `scripts/validate-repo-quality-gates.sh` | Stable support-contract drift should fail deterministically | The quality gate checks frontmatter, route coverage, authored-doc residue, flat template paths, and harness README registration, but does not fail stale migration-phase wording in active support docs. One Phase phrase in the validator belongs to workspace harness skill validation and should remain accepted context. | Low | validator-fix | `bash scripts/validate-repo-quality-gates.sh .` | Open |
| FND-004 | authored-doc | `docs/**`; `.codex/**`; `.agents/**`; `AGENTS.md`; `RTK.md` | Authored docs retain no active template residue, flat template routes, or legacy incident path rules | Active authored-doc residue and flat-template route scans returned no matches. The legacy route scan now returns self-referential matches in this Task record, plus the plan evidence command and the Stage 00 prohibited-path contract; no active legacy route contract was found. | Low | no-change | `rg -n -e "Target: docs[/]" -e "Use this te[m]plate" docs --glob "*.md" --glob "!docs/99.templates/**"`<br>`rg -n "docs/99\\.templates/[a-z0-9-]+\\.template\\.(md\|yaml\|graphql\|proto)" docs scripts .codex .agents AGENTS.md RTK.md`<br>`rg -n "docs/10\\.incidents\|Legacy postmortem top-level\|Legacy learning top-level" docs scripts .codex .agents AGENTS.md RTK.md` | Accepted |

## Phase View

### Phase 1: Planning Baseline

- [ ] T-001 Create and validate planning artifacts.

### Phase 2: Audit Evidence

- [x] T-002 Run baseline scans and refine finding ledger.

### Phase 3: Targeted Remediation

- [x] T-003 Remediate support contract drift.
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
  - `rg -n "Phase [1-4]|during the migration|after Phase|current and target|YYYY-MM-DD-<harness-task>|harness-task-contract" docs/99.templates/support docs/99.templates/README.md docs/00.agent-governance/rules/document-stage-routing.md scripts/validate-repo-quality-gates.sh`
  - `rg -n -e "Target: docs[/]" -e "Use this te[m]plate" docs --glob "*.md" --glob "!docs/99.templates/**"`
  - `rg -n "docs/99\\.templates/[a-z0-9-]+\\.template\\.(md|yaml|graphql|proto)" docs scripts .codex .agents AGENTS.md RTK.md`
  - `rg -n "docs/10\\.incidents|Legacy postmortem top-level|Legacy learning top-level" docs scripts .codex .agents AGENTS.md RTK.md`
- **Logs / Evidence Location**:
  - T-001 planning evidence: `git diff --check` passed.
  - T-001 planning evidence:
    `bash scripts/validate-repo-quality-gates.sh .` passed.
  - T-001 planning evidence: Stage 04 Korean text scan returned no matches.
  - T-002 baseline evidence: template inventory contained only
    `docs/99.templates/README.md`, `support/**`, and `templates/**`; no flat
    template-form files were present at the template root.
  - T-002 baseline evidence: drift candidate scan returned bounded support,
    README, and validator matches mapped to FND-001, FND-002, or accepted
    harness-validation context; it did not reveal active flat-template routes.
  - T-002 baseline evidence: the `Target: docs[/]` and
    `Use this te[m]plate` authored-doc residue scan returned no matches.
  - T-002 baseline evidence: the flat template route scan returned no matches
    across docs, scripts, `.codex`, `.agents`, `AGENTS.md`, and `RTK.md`.
  - T-002 baseline evidence: the legacy incident-route scan now returns
    self-referential matches in this Task record, plus the plan evidence
    command and the Stage 00 prohibited-path contract; no active legacy route
    contract was found.
  - T-003 remediation evidence: support drift scan returned no matches for
    stale phase wording or current-vs-target wording in active support docs.
  - T-003 remediation evidence: harness supplemental starter scan returned no
    lines that combine the harness starter template with the old placeholder
    task pattern in the support contracts.
  - T-003 remediation evidence: `git diff --check` passed.
  - T-003 remediation evidence:
    `bash scripts/validate-repo-quality-gates.sh .` passed.
  - Remediation and final evidence will be appended to this section during
    T-004 through T-006.

## Related Documents

- **Spec**: [../../03.specs/012-template-governance-audit-enhancement/spec.md](../../03.specs/012-template-governance-audit-enhancement/spec.md)
- **Plan**: [../plans/2026-07-03-template-governance-audit-enhancement.md](../plans/2026-07-03-template-governance-audit-enhancement.md)
- **Template Contract Migration Plan**: [../plans/2026-07-03-template-contract-governance-migration.md](../plans/2026-07-03-template-contract-governance-migration.md)
- **Template Contract Migration Task**: [./2026-07-03-template-contract-governance-migration.md](./2026-07-03-template-contract-governance-migration.md)
- **Templates README**: [../../99.templates/README.md](../../99.templates/README.md)
- **Documentation Protocol**: [../../00.agent-governance/rules/documentation-protocol.md](../../00.agent-governance/rules/documentation-protocol.md)
- **Document Stage Routing Rules**: [../../00.agent-governance/rules/document-stage-routing.md](../../00.agent-governance/rules/document-stage-routing.md)
