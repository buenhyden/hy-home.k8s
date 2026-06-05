---
title: 'Template Cross-link Fix Implementation Plan'
type: plan
status: done
owner: platform
updated: 2026-05-21
---

# Template Cross-link Fix Implementation Plan

> Historical execution record for the completed template cross-link remediation.
> Do not re-execute this plan as a live task list; current template and link rules
> are owned by `docs/99.templates/README.md` and the governance documents linked below.

---

## Overview

This plan defines the work for fixing cross-link placeholder paths in
`docs/99.templates/` template files so they use correct relative paths from
the target location, and for aligning generated document display text
(backtick code labels) with the actual href.

Problem statement: template `Related Documents` placeholders were written as
if one `../` step were enough, but most target locations such as `decisions/`,
`tasks/`, and `runbooks/` need two or more steps back to the `docs/` root. The
generated files' actual href values are correct, but their display text copied
the incorrect placeholders and therefore drifted from the href.

## Context

Analysis results:

- `spec.template.md` and `prd.template.md` already used correct relative paths and did not need changes.
- Ten templates needed `../` corrected to `../../` or to sibling-directory relative paths.
- Six other Markdown templates with Target comments already used target-relative placeholders.
- Display text in 53 generated documents and stage README surfaces differed from the actual href values, although link behavior was correct.
- Each template's target-location HTML comment states the correct final location, so relative paths were calculated from that location.
- Actual Markdown links are validated from the `docs/99.templates/` file location, while backtick code literal placeholders are validated from the Target location.

Path calculation principles:

- `docs/02.architecture/decisions/` needs `../../` to reach the `docs/` root.
- `docs/04.execution/tasks/` needs `../../` to reach the `docs/` root, and sibling `plans/` is `../plans/`.
- `docs/05.operations/runbooks/` needs `../../` to reach the `docs/` root, and sibling `guides/` and `policies/` use `../`.
- `docs/05.operations/incidents/YYYY/` needs `../../` to reach `05.operations/` and `../../../` to reach the `docs/` root.
- `docs/05.operations/incidents/postmortems/YYYY/` needs `../../../` to reach `05.operations/`.

## Goals & In-Scope

- **Goals**:
  - Review cross-link placeholders in 16 Target-bearing Markdown templates from the Target location.
  - Fix cross-link placeholders in the 10 templates that needed correct relative paths.
  - Align display text (backtick code labels) in more than 50 generated documents and README surfaces with the actual href.
- **In Scope**:
  - The 10 cross-link-bearing template files under `docs/99.templates/`
  - Review of the six already-aligned Target-bearing helper templates under `docs/99.templates/`
  - `docs/02.architecture/decisions/*.md` (nine ADRs)
  - `docs/02.architecture/requirements/*.md` (three ARDs)
  - `docs/04.execution/plans/*.md` (six Plans)
  - `docs/04.execution/tasks/*.md` (six Tasks)
  - `docs/05.operations/guides/*.md` (five Guides with link drift)
  - `docs/05.operations/runbooks/*.md` (four Runbooks)
  - Code-label/href alignment in root, docs stage, and examples README documents

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Changing actual href link targets; hrefs are already correct
  - Changing document content
  - Editing PRD/Spec body files; PRD/Spec templates and body links are already correct
- **Out of Scope**:
  - `docs/05.operations/incidents/` — no incident files existed at the time
  - `docs/90.references/` — no reference files existed at the time
  - `docs/00.agent-governance/` governance files

## Work Breakdown

| Task | Description                        | Files / Docs Affected                            | Target REQ  | Validation Criteria                                                       |
| ---- | ---------------------------------- | ------------------------------------------------ | ----------- | ------------------------------------------------------------------------- |
| T-01 | Fix `adr.template.md` paths | `docs/99.templates/adr.template.md` | REQ-TMP-001 | Four Related Documents paths use `../../` or `../requirements/` patterns |
| T-02 | Fix `ard.template.md` paths | `docs/99.templates/ard.template.md` | REQ-TMP-001 | Four Related Documents paths fixed |
| T-03 | Fix `plan.template.md` paths | `docs/99.templates/plan.template.md` | REQ-TMP-001 | Four Related Documents paths fixed |
| T-04 | Fix `task.template.md` paths | `docs/99.templates/task.template.md` | REQ-TMP-001 | Five Inputs and Related Documents paths fixed |
| T-05 | Fix `guide.template.md` paths | `docs/99.templates/guide.template.md` | REQ-TMP-001 | Three Related Documents paths fixed |
| T-06 | Fix `runbook.template.md` paths | `docs/99.templates/runbook.template.md` | REQ-TMP-001 | Four Canonical References paths and three Related Documents paths fixed |
| T-07 | Fix `incident.template.md` paths | `docs/99.templates/incident.template.md` | REQ-TMP-001 | Runbook Link cell and two Related Documents paths fixed |
| T-08 | Fix `postmortem.template.md` paths | `docs/99.templates/postmortem.template.md` | REQ-TMP-001 | Incident Document cell and three Related Documents paths fixed |
| T-09 | Fix `policy.template.md` paths | `docs/99.templates/policy.template.md` | REQ-TMP-001 | Three Related Documents paths fixed |
| T-10 | Fix `reference.template.md` paths | `docs/99.templates/reference.template.md` | REQ-TMP-001 | Two Related Documents paths fixed |
| T-11 | Fix ADR generated-file display text | `docs/02.architecture/decisions/000{1-9}*.md` | REQ-GEN-001 | backtick display text matches href |
| T-12 | Fix ARD generated-file display text | `docs/02.architecture/requirements/000{1-3}*.md` | REQ-GEN-001 | backtick display text matches href |
| T-13 | Fix Plan generated-file display text | `docs/04.execution/plans/2026-*.md` (six files) | REQ-GEN-001 | backtick display text matches href |
| T-14 | Fix Task generated-file display text | `docs/04.execution/tasks/2026-*.md` (six files) | REQ-GEN-001 | backtick display text matches href |
| T-15 | Fix Guide generated-file display text | `docs/05.operations/guides/000{1-4,8}*.md` | REQ-GEN-001 | backtick display text matches href |
| T-16 | Fix Runbook generated-file display text | `docs/05.operations/runbooks/000{1-4}*.md` | REQ-GEN-001 | backtick display text matches href |
| T-17 | Run final integrated validation | all docs | REQ-VAL-001 | scan commands have no output |

## Template Coverage Matrix

| Template                   | Target scope                                     | Result                         |
| -------------------------- | ------------------------------------------------ | ------------------------------ |
| `prd.template.md`          | `docs/01.requirements/`                          | Already target-relative        |
| `ard.template.md`          | `docs/02.architecture/requirements/`             | Fixed before final integration |
| `adr.template.md`          | `docs/02.architecture/decisions/`                | Fixed before final integration |
| `spec.template.md`         | `docs/03.specs/<feature-id>/`                    | Already target-relative        |
| `api-spec.template.md`     | `docs/03.specs/<feature-id>/`                    | Already target-relative        |
| `agent-design.template.md` | `docs/03.specs/<feature-id>/`                    | Already target-relative        |
| `data-model.template.md`   | `docs/03.specs/<feature-id>/`                    | Already target-relative        |
| `tests.template.md`        | `docs/03.specs/<feature-id>/`                    | Already target-relative        |
| `plan.template.md`         | `docs/04.execution/plans/`                       | Fixed before final integration |
| `task.template.md`         | `docs/04.execution/tasks/`                       | Fixed before final integration |
| `guide.template.md`        | `docs/05.operations/guides/`                     | Fixed before final integration |
| `policy.template.md`    | `docs/05.operations/policies/`                   | Fixed in final integration     |
| `runbook.template.md`      | `docs/05.operations/runbooks/`                   | Fixed before final integration |
| `incident.template.md`     | `docs/05.operations/incidents/YYYY/`             | Fixed in final integration     |
| `postmortem.template.md`   | `docs/05.operations/incidents/postmortems/YYYY/` | Fixed in final integration     |
| `reference.template.md`    | `docs/90.references/<category>/`                 | Fixed in final integration     |

`readme.template.md` has no fixed Target because README files live at multiple
depths. Its example links must either resolve relative to the template file or be
rewritten by the author for the final README location.

## Verification Plan

| ID          | Level      | Description                  | Command / How to Run                                                                                                     | Pass Criteria                                                                                |
| ----------- | ---------- | ---------------------------- | ------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------- |
| VAL-PLN-001 | Structural | Check template path patterns | `grep -n "Related Documents" -A 6 docs/99.templates/adr.template.md` | `../../01.requirements/`, `../requirements/`, `../../03.specs/`, `../../04.execution/plans/` |
| VAL-PLN-002 | Structural | Scan generated-file mismatches | Compare backtick code labels and href values excluding fenced code blocks | 0 mismatches |
| VAL-PLN-003 | Structural | Check internal Markdown link existence | Check relative Markdown link targets in `README.md` and `docs/**/*.md` excluding fenced code blocks | 0 missing targets |
| VAL-PLN-004 | Content | Check actual file existence | `ls docs/02.architecture/requirements/0007-current-local-gitops-platform.md docs/03.specs/008-current-local-gitops-platform/spec.md` | Both files exist |

## Risks & Mitigations

| Risk                                 | Impact | Mitigation                                                      |
| ------------------------------------ | ------ | --------------------------------------------------------------- |
| href accidentally changed while fixing display text | High   | Target only display text with exact old_string/new_string edits |
| Some files missed due to large file count           | Medium | Use the Task 17 integrated validation scan for full coverage     |
| Hooks detect another quality gate violation          | Low    | Run validation commands immediately after each task              |

## Agent Rollout & Evaluation Gates (If Applicable)

N/A — this plan covers infrastructure and documentation work and does not
deploy AI Agent models or prompts.

## Completion Criteria

- [x] Reviewed 16 Target-bearing Markdown templates.
- [x] The 10 template files that needed changes use correct Target-location relative paths for cross-link placeholders.
- [x] Display text (backtick labels) in more than 50 generated documents and README surfaces matches the actual href.
- [x] Markdown link target checks excluding fenced code blocks found 0 missing targets.
- [x] Code-label/href comparisons excluding fenced code blocks found 0 mismatches.
- [x] Added a completion entry to `docs/00.agent-governance/memory/progress.md`.

## Template Improvement Plan

`docs/99.templates/readme.template.md` is intentionally generic because README
targets vary by directory depth. The 2026-05-21 follow-up clarified that its
snippet library is optional assembly material and must not remain in final
README files. Future hardening should stay limited to target-specific path
guidance when a concrete README authoring failure is found.

## Historical Execution Notes

This plan is a historical record of template cross-link alignment completed on
2026-05-17. The former `Task Detail` section kept already-completed step-by-step
execution instructions for T-01 through T-17 as unchecked checklists, which
conflicted with `status: complete` and could mislead later readers into
re-executing the work.

Preserved completion evidence:

- T-01 through T-17 work scope and validation criteria in the Work Breakdown table
- Template Coverage Matrix
- Verification Plan and Completion Criteria
- Related Documents

## Migration Note

- No files were deleted, moved, or renamed.
- Based on `rg`, no links outside this file referenced the removed `Task Detail` heading or child task headings.
- Detailed execution instructions were consolidated into completed history, and the current template link rules remain owned by `docs/99.templates/README.md` and `docs/00.agent-governance/rules/documentation-protocol.md`.
- The 2026-05-21 follow-up changed active execution wording in the completed plan to historical-record wording and did not create a new Task document.

## Related Documents

- **Templates**: [`../../99.templates/README.md`](../../99.templates/README.md)
- **Documentation Protocol**: [`../../00.agent-governance/rules/documentation-protocol.md`](../../00.agent-governance/rules/documentation-protocol.md)
- **Stage Authoring Matrix**: [`../../00.agent-governance/rules/stage-authoring-matrix.md`](../../00.agent-governance/rules/stage-authoring-matrix.md)
