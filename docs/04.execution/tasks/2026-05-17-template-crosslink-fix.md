---
title: 'Task: Template Cross-link Fix'
type: sdlc/task
status: done
owner: platform
updated: 2026-05-21
---

# Task: Template Cross-link Fix

---

## Overview

This document tracks execution for aligning cross-link placeholder paths in
`docs/99.templates/` templates and fixing generated document display text
(backtick code labels). The work was completed from 2026-05-17 through
2026-05-21; the current template link rules are owned by
`docs/99.templates/README.md` and
`docs/00.agent-governance/rules/documentation-protocol.md`.

## Inputs

- **Parent Plan**: `[../plans/2026-05-17-template-crosslink-fix.md]`

## Working Rules

- This is documentation-only work and does not change infrastructure manifests.
- Do not change actual href link targets; they are already correct.
- Change only display text, also called the backtick code label, so it matches the href.

## Task Table

| Task ID | Description                                                    | Type | Parent Plan | Validation / Evidence                                  | Owner    | Status |
| ------- | -------------------------------------------------------------- | ---- | ----------- | ------------------------------------------------------ | -------- | ------ |
| T-001   | Fix `adr.template.md` Related Documents paths                  | doc  | T-01        | `../../01.requirements/` and `../requirements/` patterns applied | platform | Done   |
| T-002   | Fix `ard.template.md` Related Documents paths                  | doc  | T-02        | Four paths fixed                                      | platform | Done   |
| T-003   | Fix `plan.template.md` Related Documents paths                 | doc  | T-03        | Four paths fixed                                      | platform | Done   |
| T-004   | Fix `task.template.md` Inputs and Related Documents paths      | doc  | T-04        | Five paths fixed                                      | platform | Done   |
| T-005   | Fix `guide.template.md` Related Documents paths                | doc  | T-05        | Three paths fixed                                     | platform | Done   |
| T-006   | Fix `runbook.template.md` Canonical References and Related paths | doc  | T-06        | Seven paths fixed                                     | platform | Done   |
| T-007   | Fix `incident.template.md` Runbook Link and Related paths      | doc  | T-07        | Three paths fixed                                     | platform | Done   |
| T-008   | Fix `postmortem.template.md` Incident Document and Related paths | doc  | T-08        | Four paths fixed                                      | platform | Done   |
| T-009   | Fix `policy.template.md` Related Documents paths               | doc  | T-09        | Three paths fixed                                     | platform | Done   |
| T-010   | Fix `reference.template.md` Related Documents paths            | doc  | T-10        | Two paths fixed                                       | platform | Done   |
| T-011   | Fix ADR generated-file display text in nine files              | doc  | T-11        | Confirmed backtick label equals href                  | platform | Done   |
| T-012   | Fix ARD generated-file display text in three files             | doc  | T-12        | Confirmed backtick label equals href                  | platform | Done   |
| T-013   | Fix Plan generated-file display text in six files              | doc  | T-13        | Confirmed backtick label equals href                  | platform | Done   |
| T-014   | Fix Task generated-file display text in six files              | doc  | T-14        | Confirmed backtick label equals href                  | platform | Done   |
| T-015   | Fix Guide generated-file display text in five files            | doc  | T-15        | Confirmed backtick label equals href                  | platform | Done   |
| T-016   | Fix Runbook generated-file display text in four files          | doc  | T-16        | Confirmed backtick label equals href                  | platform | Done   |
| T-017   | Run final integrated validation                                | ops  | T-17        | `validate-repo-quality-gates.sh` PASS                  | platform | Done   |

## Suggested Types

- `doc`
- `ops`

## Phase View

### Phase 1 — Template Cross-link Fix (T-001~T-010)

- [x] T-001 Fix `adr.template.md` paths.
- [x] T-002 Fix `ard.template.md` paths.
- [x] T-003 Fix `plan.template.md` paths.
- [x] T-004 Fix `task.template.md` paths.
- [x] T-005 Fix `guide.template.md` paths.
- [x] T-006 Fix `runbook.template.md` paths.
- [x] T-007 Fix `incident.template.md` paths.
- [x] T-008 Fix `postmortem.template.md` paths.
- [x] T-009 Fix `policy.template.md` paths.
- [x] T-010 Fix `reference.template.md` paths.

### Phase 2 — Generated Document Label Fix (T-011~T-016)

- [x] T-011 Fix ADR display text in nine files.
- [x] T-012 Fix ARD display text in three files.
- [x] T-013 Fix Plan display text in six files.
- [x] T-014 Fix Task display text in six files.
- [x] T-015 Fix Guide display text in five files.
- [x] T-016 Fix Runbook display text in four files.

### Phase 3 — Final Validation (T-017)

- [x] T-017 Final integrated validation completed.

## Verification Summary

- **Test Commands**: `bash scripts/validate-repo-quality-gates.sh .` — PASS (2026-05-21)
- **Eval Commands**: `pre-commit run --all-files` — all pass
- **Logs / Evidence Location**: `docs/04.execution/plans/2026-05-17-template-crosslink-fix.md` (Completion Criteria section)

## Related Documents

- **Plan**: `[../plans/2026-05-17-template-crosslink-fix.md]`
- **Templates**: `[../../99.templates/README.md]`
- **Documentation Protocol**: `[../../00.agent-governance/rules/documentation-protocol.md]`
