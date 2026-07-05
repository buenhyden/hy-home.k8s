---
title: 'Task: Template Path Numbering Contract'
type: sdlc/task
status: done
owner: platform
updated: 2026-07-05
---

# Task: Template Path Numbering Contract

## Overview

This task tracks implementation and verification work for the Stage 01 PRD and
Stage 03 spec numeric route migration defined by the parent Spec and Plan.

TPN-001 is evidence-only. It creates this Stage 04 task record and adds the
task README index row. No implementation files, PRD files, template forms,
support contracts, Stage 00 governance files, validator logic, or runtime
configuration are changed in TPN-001.

## Inputs

- **Parent Spec**: [../../03.specs/019-template-path-numbering-contract/spec.md](../../03.specs/019-template-path-numbering-contract/spec.md)
- **Parent Plan**: [../plans/2026-07-05-template-path-numbering-contract.md](../plans/2026-07-05-template-path-numbering-contract.md)
- **Task Template**: [../../99.templates/templates/sdlc/execution/task.template.md](../../99.templates/templates/sdlc/execution/task.template.md)
- **Template Routing Contract**: [../../99.templates/support/template-routing.md](../../99.templates/support/template-routing.md)
- **Quality Gate**: [../../../scripts/validate-repo-quality-gates.sh](../../../scripts/validate-repo-quality-gates.sh)

## Working Rules

- Use `git mv` for PRD renames in later tasks.
- Preserve Stage 04 date-based plan and task routes.
- Do not create duplicate compatibility files for old PRD paths.
- Record old route literals only as historical evidence when needed.
- Keep Stage 04 docs English-first.
- Run validation after each logical commit.
- Keep TPN-001 scoped to task evidence only.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TPN-001 | Create task evidence and baseline scans | doc | VAL-SPC-019-007, VAL-SPC-019-008 | Task 1 | Baseline inventory, route-contract scan, old PRD link scan, `git diff --check`, quality gate | Codex | Done |
| TPN-002 | Rename active PRD files and update direct PRD indexes | doc | VAL-SPC-019-001, VAL-SPC-019-005 | Task 2 | `git mv`, stale PRD active-link scan, quality gate | Codex | Done |
| TPN-003 | Update template forms and support route contracts | doc | VAL-SPC-019-003, VAL-SPC-019-006 | Task 3 | route-map equality and old-route scan | Codex | Done |
| TPN-004 | Update Stage 00 governance and validator mappings | qa | VAL-SPC-019-002, VAL-SPC-019-004 | Task 4 | validator route coverage and quality gate | Codex | Done |
| TPN-005 | Clean cross-links, close evidence, and validate | qa | VAL-SPC-019-005, VAL-SPC-019-008 | Task 5 | final stale scans, `git diff --check`, quality gate | Codex | Done |

## Suggested Types

- `doc`
- `qa`

## Baseline Evidence

| Date | Command | Result Summary |
| --- | --- | --- |
| 2026-07-05 | `git status --short --branch` | PASS; branch is `codex/workspace-engineering-audit-pack` and no pre-existing working-tree changes were reported. |
| 2026-07-05 | `find docs/01.requirements docs/03.specs -maxdepth 3 -type f \| sort` | PASS; current inventory shows four date-based active PRDs, `docs/01.requirements/README.md`, fifteen numbered Stage 03 `spec.md` files through `019-template-path-numbering-contract`, and `docs/03.specs/README.md`. |
| 2026-07-05 | `rg -n "docs/01\\.requirements/YYYY-MM-DD-<feature-or-system>\|docs/03\\.specs/<feature-id>\|YYYY-MM-DD-<feature-or-system>\|<feature-id>" docs/99.templates docs/00.agent-governance scripts docs/01.requirements docs/03.specs docs/04.execution/plans docs/04.execution/tasks` | PASS; baseline scan found old PRD route placeholders and unnumbered Stage 03 placeholders in template, support, governance, validator, README, and plan surfaces. These matches are expected before TPN-002 through TPN-004. |
| 2026-07-05 | `rg -n "2026-05-17-argo-rollouts-progressive-delivery\|2026-05-17-argo-notifications-slack\|2026-06-01-workspace-agent-governance-platform\|2026-06-02-current-local-gitops-platform" docs AGENTS.md CLAUDE.md GEMINI.md README.md .github scripts` | PASS; baseline scan found active links and historical evidence references to the four old PRD filenames. TPN-002 owns active-link remediation and classification of any historical evidence. |
| 2026-07-05 | `sed -n '1000,1085p' scripts/validate-repo-quality-gates.sh` | PASS; validator baseline still maps PRD routes through `YYYY-MM-DD-<feature-or-system>` and Stage 03 routes through `<feature-id>`, confirming TPN-004 must update validator normalization. |

## Verification Summary

- **Test Commands**:
  - `git diff --check`
  - `bash scripts/validate-repo-quality-gates.sh .`
- **Eval Commands**: Not applicable; this task is documentation evidence only.
- **Logs / Evidence Location**: This task record and the Git commits for
  `docs(tasks): Add template path numbering evidence`,
  `docs(requirements): Number active PRD files`,
  `docs(requirements): Refresh PRD graph references`,
  `docs(templates): Number PRD and spec route contracts`, and
  `docs(governance): Enforce numbered document routes`.
- **Current Result**: PASS on 2026-07-05 after TPN-005; final stale scans,
  numeric PRD inventory, Stage 03 numeric feature-folder inventory,
  `git diff --check`, and `bash scripts/validate-repo-quality-gates.sh .`
  passed.

## Evidence Log

| Date | Task | Check | Result |
| --- | --- | --- | --- |
| 2026-07-05 | TPN-001 | Baseline inventory | PASS; four active PRDs are still date-based and Stage 03 specs are already organized under numbered feature folders. |
| 2026-07-05 | TPN-001 | Route-contract baseline scan | PASS; old route placeholders remain in current contract surfaces before implementation tasks begin. |
| 2026-07-05 | TPN-001 | Scope control | PASS; TPN-001 changes only this task evidence file and `docs/04.execution/tasks/README.md`. |
| 2026-07-05 | TPN-001 | Validation | PASS; `git diff --check` and `bash scripts/validate-repo-quality-gates.sh .` completed successfully. |
| 2026-07-05 | TPN-002 | PRD rename and old-name active-link scan | PASS; four PRDs renamed with `git mv`, Stage 01 README updated, and active old-name links removed, including the validation-discovered `infrastructure/README.md` PRD link. |
| 2026-07-05 | TPN-002 review fix | Graph artifact refresh and old-name scan classification | PASS; tracked `graphify-out/**` artifacts were refreshed to the numbered PRD filenames. The requested scan now has no `graphify-out` matches; remaining matches are explicit historical/migration evidence in the TPN spec mapping and scan command, the TPN plan mapping, commands, and validation rows, this task record's baseline and review-fix evidence, and progress memory. Runtime tooling note: `rtk` is installed at `/home/hy/.local/bin/rtk` but not on this shell's `PATH`; `rtk gain` could not initialize its tracking database, so final validation commands ran directly. |
| 2026-07-05 | TPN-003 | Template and support route contract update | PASS; template examples, Templates README, SDLC governance, and template routing contract use numbered Stage 01 and Stage 03 route patterns while preserving Stage 04 date-based routes |
| 2026-07-05 | TPN-004 | Governance and validator route update | PASS; Stage 00 route guidance, Stage 03 README wording, and validator structural/native mappings enforce numbered PRD and Stage 03 feature-folder routes, restoring the repository quality gate after the expected TPN-003 route-map drift |
| 2026-07-05 | TPN-005 | Final stale scans and repository quality gates | PASS; old current-route patterns were removed from active guidance, remaining matches are explicit TPN migration criteria or evidence, numeric PRD inventory was verified, and repository quality gates passed |

## Handoff

Template path numbering contract implementation is complete. No live runtime,
credential, GitOps desired-state, provider runtime, external service, push,
merge, or PR mutation was performed.

## Related Documents

- **Spec**: [../../03.specs/019-template-path-numbering-contract/spec.md](../../03.specs/019-template-path-numbering-contract/spec.md)
- **Plan**: [../plans/2026-07-05-template-path-numbering-contract.md](../plans/2026-07-05-template-path-numbering-contract.md)
- **Template Routing**: [../../99.templates/support/template-routing.md](../../99.templates/support/template-routing.md)
- **Task Template**: [../../99.templates/templates/sdlc/execution/task.template.md](../../99.templates/templates/sdlc/execution/task.template.md)
