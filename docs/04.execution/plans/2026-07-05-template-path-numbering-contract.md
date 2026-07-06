---
title: 'Template Path Numbering Contract Implementation Plan'
type: sdlc/plan
status: done
owner: platform
updated: 2026-07-05
---

# Template Path Numbering Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Normalize Stage 01 PRD and Stage 03 spec route contracts to numeric
path identities while preserving Stage 04 date-based execution evidence.

**Architecture:** The work is a documentation and validator migration. It first
renames active PRDs, then aligns template forms, support contracts, Stage 00
governance, README indexes, and `scripts/validate-repo-quality-gates.sh` around
the same numbered route model.

**Tech Stack:** Markdown, YAML frontmatter, Bash, Python embedded in
`scripts/validate-repo-quality-gates.sh`, `git mv`, `rg`, `find`, `sed`,
`apply_patch`, and repository quality gates.

---

## Overview

This plan implements
`docs/03.specs/019-template-path-numbering-contract/spec.md`.
The implementation renames the four active PRD files under
`docs/01.requirements/`, updates Stage 01 and Stage 03 route contracts, adjusts
template examples and validator route normalization, cleans active cross-links,
records execution evidence, and closes with repository validation.

The plan is documentation-only. It does not change live infrastructure, GitOps
desired state, provider runtime configuration, credentials, CI execution
semantics, external services, or secret values.

## Context

Current Stage 01 PRD files are date-based:

```text
docs/01.requirements/2026-05-17-argo-rollouts-progressive-delivery.md
docs/01.requirements/2026-05-17-argo-notifications-slack.md
docs/01.requirements/2026-06-01-workspace-agent-governance-platform.md
docs/01.requirements/2026-06-02-current-local-gitops-platform.md
```

The approved target names are:

```text
docs/01.requirements/001-argo-rollouts-progressive-delivery.md
docs/01.requirements/002-argo-notifications-slack.md
docs/01.requirements/003-workspace-agent-governance-platform.md
docs/01.requirements/004-current-local-gitops-platform.md
```

Current Stage 03 folders are already numeric, such as
`docs/03.specs/019-template-path-numbering-contract/`, but templates and
support contracts still describe the route as `docs/03.specs/<feature-id>/`.
This plan updates the current contract to
`docs/03.specs/<###-Numbering>-<feature-id>/`.

## Goals & In-Scope

- **Goals**:
  - Rename the four active PRDs with `git mv`.
  - Update active links to the new PRD filenames.
  - Update PRD and Stage 03 route patterns in templates, support contracts,
    Stage README files, Stage 00 governance, and validator mappings.
  - Preserve Stage 04 plan/task date-based routes.
  - Add implementation task evidence and progress memory.
  - Run repository quality gates and focused stale-pattern scans.
- **In Scope**:
  - `docs/01.requirements/**`
  - `docs/03.specs/**`
  - `docs/04.execution/plans/**`
  - `docs/04.execution/tasks/**`
  - `docs/99.templates/**`
  - `docs/00.agent-governance/rules/**`
  - `docs/00.agent-governance/memory/progress.md`
  - `scripts/validate-repo-quality-gates.sh`
  - Active Markdown cross-links in `docs`, root provider shims, `.github`, and
    `scripts`.

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Renumber Stage 02 architecture requirements or decisions.
  - Rename Stage 04 plans or tasks.
  - Create duplicate compatibility PRD files for the old date-based paths.
  - Rewrite historical execution evidence when old paths are clearly
    historical and not current routing guidance.
  - Redesign the frontmatter schema beyond route-pattern wording needed for
    this migration.
- **Out of Scope**:
  - Live Kubernetes, Argo CD, Vault, ESO, cloud, provider runtime, GitHub
    remote mutation, credentials, secret values, paid jobs, publishing, merge,
    push, PR creation, or third-party mutation.

## File Structure

| Path | Responsibility |
| --- | --- |
| `docs/04.execution/plans/2026-07-05-template-path-numbering-contract.md` | This implementation plan. |
| `docs/04.execution/plans/README.md` | Plan index entry for this work. |
| `docs/04.execution/tasks/2026-07-05-template-path-numbering-contract.md` | Execution evidence, status table, validation commands, and handoff. |
| `docs/04.execution/tasks/README.md` | Task index entry for this work. |
| `docs/01.requirements/001-argo-rollouts-progressive-delivery.md` | Renamed Argo Rollouts PRD. |
| `docs/01.requirements/002-argo-notifications-slack.md` | Renamed Argo Notifications PRD. |
| `docs/01.requirements/003-workspace-agent-governance-platform.md` | Renamed workspace agent governance PRD. |
| `docs/01.requirements/004-current-local-gitops-platform.md` | Renamed current local GitOps platform PRD. |
| `docs/01.requirements/README.md` | Stage 01 structure, workflow, and document index. |
| `docs/03.specs/README.md` | Stage 03 numbered feature-folder contract and index. |
| `docs/99.templates/templates/sdlc/requirements/prd.template.md` | PRD target and related-document examples. |
| `docs/99.templates/templates/sdlc/specs/*.template.md` | Stage 03 numbered feature-folder target and related-document examples. |
| `docs/99.templates/templates/sdlc/specs/openapi.template.yaml` | Native OpenAPI target comment for numbered feature folder. |
| `docs/99.templates/templates/sdlc/specs/schema.template.graphql` | Native GraphQL target comment for numbered feature folder. |
| `docs/99.templates/templates/sdlc/specs/service.template.proto` | Native protobuf target comment for numbered feature folder. |
| `docs/99.templates/templates/sdlc/architecture/*.template.md` | PRD and Spec related-document examples. |
| `docs/99.templates/templates/sdlc/execution/*.template.md` | PRD and Spec related-document examples while preserving Stage 04 date routes. |
| `docs/99.templates/templates/sdlc/operations/*.template.md` | Spec related-document examples for numbered feature folder. |
| `docs/99.templates/templates/common/reference.template.md` | Spec related-document example for numbered feature folder. |
| `docs/99.templates/README.md` | Template mapping and route guidance. |
| `docs/99.templates/support/sdlc-governance.md` | SDLC route contract owner. |
| `docs/99.templates/support/template-routing.md` | Structural template route map owner. |
| `docs/99.templates/support/frontmatter-schema.md` | Frontmatter support notes if old route examples appear. |
| `docs/00.agent-governance/rules/document-stage-routing.md` | Stage routing guidance. |
| `docs/00.agent-governance/rules/documentation-protocol.md` | Authored-document template routing guidance. |
| `docs/00.agent-governance/rules/stage-authoring-matrix.md` | Stage-level authoring summary. |
| `scripts/validate-repo-quality-gates.sh` | Route normalization, template mapping, and structural coverage enforcement. |
| `docs/00.agent-governance/memory/progress.md` | Durable completion memory after validation. |

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| TPN-001 | Create Stage 04 task evidence and baseline scans | Task record, task README | VAL-SPC-019-007, VAL-SPC-019-008 | Baseline scans recorded; no implementation files changed except task evidence |
| TPN-002 | Rename active PRD files and update direct PRD indexes | Stage 01 PRDs, Stage 01 README, active PRD links | VAL-SPC-019-001, VAL-SPC-019-005 | Old PRD active links removed; quality gate passes |
| TPN-003 | Update template forms and support route contracts | `docs/99.templates/**` | VAL-SPC-019-003, VAL-SPC-019-006 | Template mapping and support route map match |
| TPN-004 | Update Stage 00 governance and validator mappings | Stage 00 rules, validator script | VAL-SPC-019-002, VAL-SPC-019-004 | Validator recognizes numbered PRD and Stage 03 routes |
| TPN-005 | Clean cross-links, close evidence, and validate | Cross-links, progress memory, plan/task indexes | VAL-SPC-019-005, VAL-SPC-019-006, VAL-SPC-019-007, VAL-SPC-019-008 | Focused scans and quality gates pass |

## Detailed Tasks

### Task 1: Create Task Evidence and Baseline Scans

**Files:**

- Create: `docs/04.execution/tasks/2026-07-05-template-path-numbering-contract.md`
- Modify: `docs/04.execution/tasks/README.md`
- Read: `docs/99.templates/templates/sdlc/execution/task.template.md`
- Read: `docs/03.specs/019-template-path-numbering-contract/spec.md`
- Read: `docs/99.templates/support/template-routing.md`
- Read: `scripts/validate-repo-quality-gates.sh`

- [ ] **Step 1: Confirm clean branch state**

Run:

```bash
git status --short --branch
```

Expected: branch is `codex/workspace-engineering-audit-pack` and the working
tree is clean after this plan commit.

- [ ] **Step 2: Read the task template and approved spec**

Run:

```bash
sed -n '1,180p' docs/99.templates/templates/sdlc/execution/task.template.md
sed -n '1,360p' docs/03.specs/019-template-path-numbering-contract/spec.md
```

Expected: the command shows the required Stage 04 task headings and all
`VAL-SPC-019-*` criteria.

- [ ] **Step 3: Capture current PRD and Stage 03 file inventory**

Run:

```bash
find docs/01.requirements docs/03.specs -maxdepth 3 -type f | sort
```

Expected: output includes four date-based PRD files and numeric Stage 03 spec
folders through `019-template-path-numbering-contract/spec.md`.

- [ ] **Step 4: Capture current route-contract matches**

Run:

```bash
rg -n "docs/01\\.requirements/YYYY-MM-DD-<feature-or-system>|docs/03\\.specs/<feature-id>|YYYY-MM-DD-<feature-or-system>|<feature-id>" docs/99.templates docs/00.agent-governance scripts docs/01.requirements docs/03.specs docs/04.execution/plans docs/04.execution/tasks
```

Expected: output includes current route contracts and template examples that
must be updated or explicitly preserved as Stage 04 date-based routes.

- [ ] **Step 5: Create the task record**

Create `docs/04.execution/tasks/2026-07-05-template-path-numbering-contract.md`
with frontmatter:

```yaml
---
title: 'Task: Template Path Numbering Contract'
type: sdlc/task
status: draft
owner: platform
updated: 2026-07-05
---
```

The task record must include these sections:

```markdown
# Task: Template Path Numbering Contract

## Overview

This task tracks implementation and validation work for the Stage 01 PRD and
Stage 03 spec numeric route migration.

## Inputs

- **Parent Spec**: [../../03.specs/019-template-path-numbering-contract/spec.md](../../03.specs/019-template-path-numbering-contract/spec.md)
- **Parent Plan**: [../plans/2026-07-05-template-path-numbering-contract.md](../plans/2026-07-05-template-path-numbering-contract.md)

## Working Rules

- Use `git mv` for PRD renames.
- Preserve Stage 04 date-based plan and task routes.
- Do not create duplicate compatibility files for old PRD paths.
- Record old route literals only as historical evidence when needed.
- Run validation after each logical commit.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TPN-001 | Create task evidence and baseline scans | doc | VAL-SPC-019-007, VAL-SPC-019-008 | Task 1 | Baseline inventory and route-contract scan | Codex | In Progress |
| TPN-002 | Rename active PRD files and update direct PRD indexes | doc | VAL-SPC-019-001, VAL-SPC-019-005 | Task 2 | `git mv`, stale PRD active-link scan, quality gate | Codex | Planned |
| TPN-003 | Update template forms and support route contracts | doc | VAL-SPC-019-003, VAL-SPC-019-006 | Task 3 | route-map equality and old-route scan | Codex | Planned |
| TPN-004 | Update Stage 00 governance and validator mappings | qa | VAL-SPC-019-002, VAL-SPC-019-004 | Task 4 | validator route coverage and quality gate | Codex | Planned |
| TPN-005 | Clean cross-links, close evidence, and validate | qa | VAL-SPC-019-005, VAL-SPC-019-008 | Task 5 | final stale scans, `git diff --check`, quality gate | Codex | Planned |

## Suggested Types

- `doc`
- `qa`

## Verification Commands

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
rg -n "docs/01\\.requirements/YYYY-MM-DD-<feature-or-system>|docs/03\\.specs/<feature-id>" docs/99.templates docs/00.agent-governance scripts docs/01.requirements docs/03.specs
rg -n "2026-05-17-argo-rollouts-progressive-delivery|2026-05-17-argo-notifications-slack|2026-06-01-workspace-agent-governance-platform|2026-06-02-current-local-gitops-platform" docs AGENTS.md CLAUDE.md GEMINI.md README.md .github scripts
```

## Evidence Log

| Date | Task | Check | Result |
| --- | --- | --- | --- |
| 2026-07-05 | TPN-001 | Baseline inventory | Pending |

## Handoff

No handoff until all TPN tasks are complete and validation passes.

## Related Documents

- **Spec**: [../../03.specs/019-template-path-numbering-contract/spec.md](../../03.specs/019-template-path-numbering-contract/spec.md)
- **Plan**: [../plans/2026-07-05-template-path-numbering-contract.md](../plans/2026-07-05-template-path-numbering-contract.md)
- **Template Routing**: [../../99.templates/support/template-routing.md](../../99.templates/support/template-routing.md)
```

Expected: the task record has all required template headings and no template
instruction residue.

- [ ] **Step 6: Add task index row**

Modify `docs/04.execution/tasks/README.md` by adding this row to the document
index:

```markdown
| [`./2026-07-05-template-path-numbering-contract.md`](./2026-07-05-template-path-numbering-contract.md) | Template path numbering contract execution evidence for PRD numeric renames, Stage 03 numbered feature-folder routing, template/support/governance/validator updates, and validation closure. | Draft | 2026-07-05 |
```

Expected: the row appears near other 2026-07-05 task records.

- [ ] **Step 7: Validate and commit Task 1**

Run:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
git add docs/04.execution/tasks/2026-07-05-template-path-numbering-contract.md docs/04.execution/tasks/README.md
git commit -m "docs(tasks): Add template path numbering evidence"
```

Expected: both validation commands pass and the commit succeeds.

### Task 2: Rename Active PRDs and Update Stage 01 Links

**Files:**

- Rename: `docs/01.requirements/2026-05-17-argo-rollouts-progressive-delivery.md` to `docs/01.requirements/001-argo-rollouts-progressive-delivery.md`
- Rename: `docs/01.requirements/2026-05-17-argo-notifications-slack.md` to `docs/01.requirements/002-argo-notifications-slack.md`
- Rename: `docs/01.requirements/2026-06-01-workspace-agent-governance-platform.md` to `docs/01.requirements/003-workspace-agent-governance-platform.md`
- Rename: `docs/01.requirements/2026-06-02-current-local-gitops-platform.md` to `docs/01.requirements/004-current-local-gitops-platform.md`
- Modify: `docs/01.requirements/README.md`
- Modify: active links in `docs/**`, `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `README.md`, `.github/**`, and `scripts/**` when they point to current PRDs.
- Modify: `docs/04.execution/tasks/2026-07-05-template-path-numbering-contract.md`

- [ ] **Step 1: Rename the PRD files with `git mv`**

Run:

```bash
git mv docs/01.requirements/2026-05-17-argo-rollouts-progressive-delivery.md docs/01.requirements/001-argo-rollouts-progressive-delivery.md
git mv docs/01.requirements/2026-05-17-argo-notifications-slack.md docs/01.requirements/002-argo-notifications-slack.md
git mv docs/01.requirements/2026-06-01-workspace-agent-governance-platform.md docs/01.requirements/003-workspace-agent-governance-platform.md
git mv docs/01.requirements/2026-06-02-current-local-gitops-platform.md docs/01.requirements/004-current-local-gitops-platform.md
```

Expected: `git status --short` shows four PRD renames.

- [ ] **Step 2: Update Stage 01 README structure and workflow**

In `docs/01.requirements/README.md`, replace the structure block with:

```text
01.requirements/
├── 001-argo-rollouts-progressive-delivery.md
├── 002-argo-notifications-slack.md
├── 003-workspace-agent-governance-platform.md
├── 004-current-local-gitops-platform.md
└── README.md
```

Replace the canonical target pattern in the "How to Work in This Area" section.
Keep the surrounding Korean prose unchanged, but replace only the route literal:

```markdown
`docs/01.requirements/YYYY-MM-DD-<feature-or-system>.md`
```

with:

```markdown
`docs/01.requirements/<###-Numbering>-<feature-or-system>.md`
```

Replace the document index link targets without rewriting the existing
description text:

```text
./2026-05-17-argo-rollouts-progressive-delivery.md -> ./001-argo-rollouts-progressive-delivery.md
./2026-05-17-argo-notifications-slack.md -> ./002-argo-notifications-slack.md
./2026-06-01-workspace-agent-governance-platform.md -> ./003-workspace-agent-governance-platform.md
./2026-06-02-current-local-gitops-platform.md -> ./004-current-local-gitops-platform.md
```

Expected: `docs/01.requirements/README.md` no longer advertises date-based
PRD filenames as current routes.

- [ ] **Step 3: Update active links to renamed PRDs**

Run a focused replacement:

```bash
perl -0pi -e 's#\\.\\./01\\.requirements/2026-05-17-argo-rollouts-progressive-delivery\\.md#../01.requirements/001-argo-rollouts-progressive-delivery.md#g; s#\\.\\./01\\.requirements/2026-05-17-argo-notifications-slack\\.md#../01.requirements/002-argo-notifications-slack.md#g; s#\\.\\./01\\.requirements/2026-06-01-workspace-agent-governance-platform\\.md#../01.requirements/003-workspace-agent-governance-platform.md#g; s#\\.\\./01\\.requirements/2026-06-02-current-local-gitops-platform\\.md#../01.requirements/004-current-local-gitops-platform.md#g; s#../../01\\.requirements/2026-05-17-argo-rollouts-progressive-delivery\\.md#../../01.requirements/001-argo-rollouts-progressive-delivery.md#g; s#../../01\\.requirements/2026-05-17-argo-notifications-slack\\.md#../../01.requirements/002-argo-notifications-slack.md#g; s#../../01\\.requirements/2026-06-01-workspace-agent-governance-platform\\.md#../../01.requirements/003-workspace-agent-governance-platform.md#g; s#../../01\\.requirements/2026-06-02-current-local-gitops-platform\\.md#../../01.requirements/004-current-local-gitops-platform.md#g; s#docs/01\\.requirements/2026-05-17-argo-rollouts-progressive-delivery\\.md#docs/01.requirements/001-argo-rollouts-progressive-delivery.md#g; s#docs/01\\.requirements/2026-05-17-argo-notifications-slack\\.md#docs/01.requirements/002-argo-notifications-slack.md#g; s#docs/01\\.requirements/2026-06-01-workspace-agent-governance-platform\\.md#docs/01.requirements/003-workspace-agent-governance-platform.md#g; s#docs/01\\.requirements/2026-06-02-current-local-gitops-platform\\.md#docs/01.requirements/004-current-local-gitops-platform.md#g' $(rg -l "2026-05-17-argo-rollouts-progressive-delivery|2026-05-17-argo-notifications-slack|2026-06-01-workspace-agent-governance-platform|2026-06-02-current-local-gitops-platform" docs AGENTS.md CLAUDE.md GEMINI.md README.md .github scripts)
```

Expected: active Markdown links and code-literal current paths point to the new
PRD names. Historical evidence may still need manual review after the scan.

- [ ] **Step 4: Scan for old PRD names**

Run:

```bash
rg -n "2026-05-17-argo-rollouts-progressive-delivery|2026-05-17-argo-notifications-slack|2026-06-01-workspace-agent-governance-platform|2026-06-02-current-local-gitops-platform" docs AGENTS.md CLAUDE.md GEMINI.md README.md .github scripts
```

Expected: no active links remain. If matches remain in old progress entries or
historical plan evidence, update only wording that presents the old names as
current route guidance.

- [ ] **Step 5: Update task evidence**

In `docs/04.execution/tasks/2026-07-05-template-path-numbering-contract.md`:

- Mark `TPN-002` as `Done`.
- Add an Evidence Log row:

```markdown
| 2026-07-05 | TPN-002 | PRD rename and old-name active-link scan | PASS; four PRDs renamed with `git mv`, Stage 01 README updated, and active old-name links removed or classified as historical evidence |
```

Expected: task evidence reflects the rename result.

- [ ] **Step 6: Validate and commit Task 2**

Run:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
git add docs/01.requirements docs/04.execution/tasks/2026-07-05-template-path-numbering-contract.md docs AGENTS.md CLAUDE.md GEMINI.md README.md .github scripts
git commit -m "docs(requirements): Number active PRD files"
```

Expected: validation passes and the commit succeeds.

### Task 3: Update Template Forms and Support Route Contracts

**Files:**

- Modify: `docs/99.templates/templates/sdlc/requirements/prd.template.md`
- Modify: `docs/99.templates/templates/sdlc/specs/spec.template.md`
- Modify: `docs/99.templates/templates/sdlc/specs/api-spec.template.md`
- Modify: `docs/99.templates/templates/sdlc/specs/agent-design.template.md`
- Modify: `docs/99.templates/templates/sdlc/specs/data-model.template.md`
- Modify: `docs/99.templates/templates/sdlc/specs/tests.template.md`
- Modify: `docs/99.templates/templates/sdlc/specs/openapi.template.yaml`
- Modify: `docs/99.templates/templates/sdlc/specs/schema.template.graphql`
- Modify: `docs/99.templates/templates/sdlc/specs/service.template.proto`
- Modify: `docs/99.templates/templates/sdlc/architecture/adr.template.md`
- Modify: `docs/99.templates/templates/sdlc/architecture/ard.template.md`
- Modify: `docs/99.templates/templates/sdlc/execution/plan.template.md`
- Modify: `docs/99.templates/templates/sdlc/execution/task.template.md`
- Modify: `docs/99.templates/templates/sdlc/operations/incident.template.md`
- Modify: `docs/99.templates/templates/sdlc/operations/policy.template.md`
- Modify: `docs/99.templates/templates/sdlc/operations/postmortem.template.md`
- Modify: `docs/99.templates/templates/sdlc/operations/runbook.template.md`
- Modify: `docs/99.templates/templates/common/reference.template.md`
- Modify: `docs/99.templates/README.md`
- Modify: `docs/99.templates/support/sdlc-governance.md`
- Modify: `docs/99.templates/support/template-routing.md`
- Modify: `docs/04.execution/tasks/2026-07-05-template-path-numbering-contract.md`

- [ ] **Step 1: Replace current PRD target pattern in template contracts**

Replace current-route examples that use:

```text
docs/01.requirements/YYYY-MM-DD-<feature-or-system>.md
```

with:

```text
docs/01.requirements/<###-Numbering>-<feature-or-system>.md
```

Apply the replacement in current template examples and support route maps:

```bash
perl -0pi -e 's#docs/01\\.requirements/YYYY-MM-DD-<feature-or-system>\\.md#docs/01.requirements/<###-Numbering>-<feature-or-system>.md#g; s#\\.\\./\\.\\./01\\.requirements/YYYY-MM-DD-<feature-or-system>\\.md#../../01.requirements/<###-Numbering>-<feature-or-system>.md#g; s#\\.\\./01\\.requirements/YYYY-MM-DD-<feature-or-system>\\.md#../01.requirements/<###-Numbering>-<feature-or-system>.md#g' docs/99.templates/templates/sdlc/requirements/prd.template.md docs/99.templates/templates/sdlc/architecture/adr.template.md docs/99.templates/templates/sdlc/architecture/ard.template.md docs/99.templates/templates/sdlc/execution/plan.template.md docs/99.templates/templates/sdlc/specs/spec.template.md docs/99.templates/templates/sdlc/specs/agent-design.template.md docs/99.templates/README.md docs/99.templates/support/sdlc-governance.md docs/99.templates/support/template-routing.md
```

Expected: PRD template target and related-document examples use the numeric
PRD route.

- [ ] **Step 2: Replace current Stage 03 feature-folder placeholder**

Replace current-route examples that use:

```text
docs/03.specs/<feature-id>/
```

with:

```text
docs/03.specs/<###-Numbering>-<feature-id>/
```

Apply the replacement in current template and support route surfaces:

```bash
perl -0pi -e 's#docs/03\\.specs/<feature-id>#docs/03.specs/<###-Numbering>-<feature-id>#g; s#\\.\\./\\.\\./03\\.specs/<feature-id>#../../03.specs/<###-Numbering>-<feature-id>#g; s#\\.\\./\\.\\./\\.\\./\\.\\./03\\.specs/<feature-id>#../../../../03.specs/<###-Numbering>-<feature-id>#g' docs/99.templates/templates/sdlc/specs/spec.template.md docs/99.templates/templates/sdlc/specs/api-spec.template.md docs/99.templates/templates/sdlc/specs/agent-design.template.md docs/99.templates/templates/sdlc/specs/data-model.template.md docs/99.templates/templates/sdlc/specs/tests.template.md docs/99.templates/templates/sdlc/specs/openapi.template.yaml docs/99.templates/templates/sdlc/specs/schema.template.graphql docs/99.templates/templates/sdlc/specs/service.template.proto docs/99.templates/templates/sdlc/architecture/adr.template.md docs/99.templates/templates/sdlc/architecture/ard.template.md docs/99.templates/templates/sdlc/execution/plan.template.md docs/99.templates/templates/sdlc/execution/task.template.md docs/99.templates/templates/sdlc/operations/incident.template.md docs/99.templates/templates/sdlc/operations/policy.template.md docs/99.templates/templates/sdlc/operations/postmortem.template.md docs/99.templates/templates/sdlc/operations/runbook.template.md docs/99.templates/templates/common/reference.template.md docs/99.templates/README.md docs/99.templates/support/sdlc-governance.md docs/99.templates/support/template-routing.md
```

Expected: Stage 03 route examples use the numbered feature-folder placeholder.
Stage 04 plan and task filename placeholders remain date-based.

- [ ] **Step 3: Manually inspect route maps for intended rows**

Run:

```bash
sed -n '130,230p' docs/99.templates/README.md
sed -n '34,75p' docs/99.templates/support/template-routing.md
sed -n '20,65p' docs/99.templates/support/sdlc-governance.md
```

Expected: the route rows include:

```text
docs/01.requirements/<###-Numbering>-<feature-or-system>.md
docs/03.specs/<###-Numbering>-<feature-id>/spec.md
docs/03.specs/<###-Numbering>-<feature-id>/api-spec.md
docs/03.specs/<###-Numbering>-<feature-id>/agent-design.md
docs/03.specs/<###-Numbering>-<feature-id>/data-model.md
docs/03.specs/<###-Numbering>-<feature-id>/tests.md
docs/03.specs/<###-Numbering>-<feature-id>/contracts/openapi.yaml
docs/03.specs/<###-Numbering>-<feature-id>/contracts/schema.graphql
docs/03.specs/<###-Numbering>-<feature-id>/contracts/service.proto
```

- [ ] **Step 4: Preserve Stage 04 date-based execution routes**

Run:

```bash
rg -n "docs/04\\.execution/(plans|tasks)/YYYY-MM-DD" docs/99.templates/templates/sdlc/execution docs/99.templates/README.md docs/99.templates/support
```

Expected: matches remain because Stage 04 plan and task routes are intentionally
date-based.

- [ ] **Step 5: Update task evidence**

In `docs/04.execution/tasks/2026-07-05-template-path-numbering-contract.md`:

- Mark `TPN-003` as `Done`.
- Add this Evidence Log row:

```markdown
| 2026-07-05 | TPN-003 | Template and support route contract update | PASS; template examples, Templates README, SDLC governance, and template routing contract use numbered Stage 01 and Stage 03 route patterns while preserving Stage 04 date-based routes |
```

- [ ] **Step 6: Validate and commit Task 3**

Run:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
git add docs/99.templates docs/04.execution/tasks/2026-07-05-template-path-numbering-contract.md
git commit -m "docs(templates): Number PRD and spec route contracts"
```

Expected: validation passes and the commit succeeds.

### Task 4: Update Governance and Validator Mappings

**Files:**

- Modify: `docs/00.agent-governance/rules/document-stage-routing.md`
- Modify: `docs/00.agent-governance/rules/documentation-protocol.md`
- Modify: `docs/00.agent-governance/rules/stage-authoring-matrix.md`
- Modify: `docs/03.specs/README.md`
- Modify: `scripts/validate-repo-quality-gates.sh`
- Modify: `docs/04.execution/tasks/2026-07-05-template-path-numbering-contract.md`

- [ ] **Step 1: Update Stage 03 README route wording**

In `docs/03.specs/README.md`, replace the current canonical target literal:

```markdown
`docs/03.specs/<feature-id>/spec.md`
```

with:

```markdown
`docs/03.specs/<###-Numbering>-<feature-id>/spec.md`
```

Replace these current route literals:

```markdown
`./<feature-id>/spec.md`
`docs/03.specs/<feature-id>/`
```

with:

```markdown
`./<###-Numbering>-<feature-id>/spec.md`
`docs/03.specs/<###-Numbering>-<feature-id>/`
```

Replace the helper-template introduction route literal:

```markdown
`docs/03.specs/<feature-id>/`
```

with:

```markdown
`docs/03.specs/<###-Numbering>-<feature-id>/`
```

Expected: Stage 03 README describes the numbered feature-folder route.

- [ ] **Step 2: Update Stage 00 route guidance**

Run:

```bash
perl -0pi -e 's#docs/03\\.specs/<feature-id>#docs/03.specs/<###-Numbering>-<feature-id>#g; s#docs/01\\.requirements/YYYY-MM-DD-<feature-or-system>\\.md#docs/01.requirements/<###-Numbering>-<feature-or-system>.md#g' docs/00.agent-governance/rules/document-stage-routing.md docs/00.agent-governance/rules/documentation-protocol.md docs/00.agent-governance/rules/stage-authoring-matrix.md
```

Expected: governance route guidance points to numbered Stage 01 and Stage 03
contracts.

- [ ] **Step 3: Update validator documented route table**

In `scripts/validate-repo-quality-gates.sh`, replace the relevant
`documented_stage_routes` rows with:

```python
    ("docs/01.requirements/<###-Numbering>-<feature-or-system>.md", "prd.template.md"),
    ("docs/02.architecture/requirements/####-<system-or-domain>.md", "ard.template.md"),
    ("docs/02.architecture/decisions/####-<short-title>.md", "adr.template.md"),
    ("docs/03.specs/<###-Numbering>-<feature-id>/spec.md", "spec.template.md"),
    ("docs/03.specs/<###-Numbering>-<feature-id>/api-spec.md", "api-spec.template.md"),
    ("docs/03.specs/<###-Numbering>-<feature-id>/agent-design.md", "agent-design.template.md"),
    ("docs/03.specs/<###-Numbering>-<feature-id>/data-model.md", "data-model.template.md"),
    ("docs/03.specs/<###-Numbering>-<feature-id>/tests.md", "tests.template.md"),
```

Replace the native contract route rows with:

```python
    ("docs/03.specs/<###-Numbering>-<feature-id>/contracts/openapi.yaml", "openapi.template.yaml"),
    ("docs/03.specs/<###-Numbering>-<feature-id>/contracts/schema.graphql", "schema.template.graphql"),
    ("docs/03.specs/<###-Numbering>-<feature-id>/contracts/service.proto", "service.template.proto"),
```

Expected: validator route table matches the support route contract.

- [ ] **Step 4: Update validator placeholder normalization**

In `documented_target_to_validator_glob`, replace the placeholder replacement
for old PRD and Stage 03 routes with:

```python
        ("<###-Numbering>-<feature-or-system>", "[0-9][0-9][0-9]-*"),
        ("<###-Numbering>-<feature-id>", "[0-9][0-9][0-9]-*"),
```

Keep these existing replacements because Stage 04 and Stage 02 still use them:

```python
        ("YYYY-MM-DD-<feature-or-stream>", "*"),
        ("YYYY-MM-DD-<feature>", "*"),
        ("####-<policy-or-standard>", "*"),
        ("####-<system-or-domain>", "*"),
        ("####-<short-title>", "*"),
        ("####-<topic>", "*"),
        ("INC-###-<title>", "INC-[0-9][0-9][0-9]-*"),
        ("YYYY", "[0-9][0-9][0-9][0-9]"),
```

Expected: validator globs require a three-digit prefix for PRDs and Stage 03
feature folders.

- [ ] **Step 5: Verify validator route expectations**

Run:

```bash
sed -n '1024,1075p' scripts/validate-repo-quality-gates.sh
sed -n '1200,1230p' scripts/validate-repo-quality-gates.sh
bash scripts/validate-repo-quality-gates.sh .
```

Expected: the route table displays numbered PRD and Stage 03 patterns, and the
quality gate passes.

- [ ] **Step 6: Update task evidence**

In `docs/04.execution/tasks/2026-07-05-template-path-numbering-contract.md`:

- Mark `TPN-004` as `Done`.
- Add this Evidence Log row:

```markdown
| 2026-07-05 | TPN-004 | Governance and validator route update | PASS; Stage 00 route guidance and validator structural mappings enforce numbered PRD and Stage 03 feature-folder routes |
```

- [ ] **Step 7: Validate and commit Task 4**

Run:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
git add docs/00.agent-governance/rules/document-stage-routing.md docs/00.agent-governance/rules/documentation-protocol.md docs/00.agent-governance/rules/stage-authoring-matrix.md docs/03.specs/README.md scripts/validate-repo-quality-gates.sh docs/04.execution/tasks/2026-07-05-template-path-numbering-contract.md
git commit -m "docs(governance): Enforce numbered document routes"
```

Expected: validation passes and the commit succeeds.

### Task 5: Cross-Link Cleanup, Evidence Closure, and Final Validation

**Files:**

- Modify: `docs/04.execution/plans/README.md`
- Modify: `docs/04.execution/tasks/README.md`
- Modify: `docs/04.execution/tasks/2026-07-05-template-path-numbering-contract.md`
- Modify: `docs/00.agent-governance/memory/progress.md`
- Modify: any active document with stale current-route links found by scans.

- [ ] **Step 1: Add plan index row**

Modify `docs/04.execution/plans/README.md` by adding this row near other
2026-07-05 plans:

```markdown
| [`./2026-07-05-template-path-numbering-contract.md`](./2026-07-05-template-path-numbering-contract.md) | Template path numbering contract implementation plan for PRD numeric renames, Stage 03 numbered feature-folder routing, template/support/governance/validator updates, and validation closure. | Draft | 2026-07-05 |
```

Expected: the plan is discoverable from the Stage 04 plans index.

- [ ] **Step 2: Run focused stale contract scans**

Run:

```bash
rg -n "docs/01\\.requirements/YYYY-MM-DD-<feature-or-system>|docs/03\\.specs/<feature-id>" docs/99.templates docs/00.agent-governance scripts docs/01.requirements docs/03.specs
rg -n "2026-05-17-argo-rollouts-progressive-delivery|2026-05-17-argo-notifications-slack|2026-06-01-workspace-agent-governance-platform|2026-06-02-current-local-gitops-platform" docs AGENTS.md CLAUDE.md GEMINI.md README.md .github scripts
find docs/01.requirements -maxdepth 1 -type f | sort
find docs/03.specs -maxdepth 2 -type f -name 'spec.md' | sort
```

Expected:

- First scan has no current contract matches for the old PRD route or old
  unnumbered Stage 03 route.
- Second scan has no active Markdown links to old PRD filenames. Historical
  mentions are explicitly historical or absent.
- PRD inventory contains `001-` through `004-` files.
- Stage 03 spec inventory contains numeric feature folders.

- [ ] **Step 3: Add progress memory entry**

Add a new entry near the top of
`docs/00.agent-governance/memory/progress.md`:

```markdown
### 2026-07-05 - Template path numbering contract implementation

- **Date**: 2026-07-05
- **Layer**: docs, templates, governance, validation
- **Status**: complete
- **Tags**: #docs #templates #sdlc #validation #stage-01 #stage-03

#### Progress

- Renamed the four active Stage 01 PRDs from date-based filenames to numeric
  filenames.
- Updated Stage 01 and Stage 03 route contracts across template forms, support
  contracts, Stage README files, Stage 00 governance, and repository
  validation.
- Preserved Stage 04 plan and task date-based routes as execution evidence.
- Closed active cross-links and validation evidence for the numbered route
  migration.

#### Memory

- Stage 01 PRDs use `<###-Numbering>-<feature-or-system>.md`.
- Stage 03 specs and helper contracts use
  `<###-Numbering>-<feature-id>/`.
- Stage 04 plans and tasks remain date-based because they are execution
  evidence records.
- Old PRD filenames may appear only as historical evidence, not as current
  route guidance.

#### Evidence

- `git diff --check` - PASS.
- `bash scripts/validate-repo-quality-gates.sh .` - PASS.
- Old PRD active-link scan - PASS.
- Old route-contract scan - PASS.

#### Handoff

- Documentation-only route normalization is complete. No live runtime,
  credential, GitOps desired-state, provider runtime, external service, push,
  merge, or PR mutation was performed.
```

Expected: memory records the reusable route distinction.

- [ ] **Step 4: Close task evidence**

In `docs/04.execution/tasks/2026-07-05-template-path-numbering-contract.md`:

- Mark all task rows `Done`.
- Change frontmatter `status: draft` to `status: done`.
- Add this Evidence Log row:

```markdown
| 2026-07-05 | TPN-005 | Final stale scans and repository quality gates | PASS; old current-route patterns removed, numeric PRD inventory verified, and repository quality gates passed |
```

Replace the Handoff section with:

```markdown
## Handoff

Template path numbering contract implementation is complete. No live runtime,
credential, GitOps desired-state, provider runtime, external service, push,
merge, or PR mutation was performed.
```

Expected: task evidence records final closure.

- [ ] **Step 5: Run final validation**

Run:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
rg -n "docs/01\\.requirements/YYYY-MM-DD-<feature-or-system>|docs/03\\.specs/<feature-id>" docs/99.templates docs/00.agent-governance scripts docs/01.requirements docs/03.specs
rg -n "2026-05-17-argo-rollouts-progressive-delivery|2026-05-17-argo-notifications-slack|2026-06-01-workspace-agent-governance-platform|2026-06-02-current-local-gitops-platform" docs AGENTS.md CLAUDE.md GEMINI.md README.md .github scripts
```

Expected:

- `git diff --check` passes.
- repository quality gates pass.
- old current-route contract scan returns no matches or only accepted
  historical evidence.
- old PRD filename scan returns no active links.

- [ ] **Step 6: Commit final closure**

Run:

```bash
git add docs/04.execution/plans/README.md docs/04.execution/tasks/README.md docs/04.execution/tasks/2026-07-05-template-path-numbering-contract.md docs/00.agent-governance/memory/progress.md docs AGENTS.md CLAUDE.md GEMINI.md README.md .github scripts
git commit -m "docs(validation): Close template path numbering migration"
```

Expected: final closure commit succeeds.

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-TPN-001 | Structural | PRD files use numeric filenames | `find docs/01.requirements -maxdepth 1 -type f | sort` | Output contains `001-`, `002-`, `003-`, and `004-` PRD files and no date-based PRD filenames. |
| VAL-TPN-002 | Structural | Stage 03 specs use numbered feature folders | `find docs/03.specs -maxdepth 2 -type f -name 'spec.md' | sort` | All active spec paths are under numeric feature folders. |
| VAL-TPN-003 | Contract | Template/support/gov surfaces do not advertise old route patterns | `rg -n "docs/01\\.requirements/YYYY-MM-DD-<feature-or-system>|docs/03\\.specs/<feature-id>" docs/99.templates docs/00.agent-governance scripts docs/01.requirements docs/03.specs` | No current contract matches remain. |
| VAL-TPN-004 | Link | Active documents do not link old PRD filenames | `rg -n "2026-05-17-argo-rollouts-progressive-delivery|2026-05-17-argo-notifications-slack|2026-06-01-workspace-agent-governance-platform|2026-06-02-current-local-gitops-platform" docs AGENTS.md CLAUDE.md GEMINI.md README.md .github scripts` | No active links remain; any remaining matches are explicitly historical evidence. |
| VAL-TPN-005 | Quality | Markdown whitespace and patch sanity | `git diff --check` | Command exits 0. |
| VAL-TPN-006 | Quality | Repository documentation and route gates | `bash scripts/validate-repo-quality-gates.sh .` | Command exits 0. |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Broad replacement changes historical evidence incorrectly | Medium | Use focused scans and preserve old paths only when explicitly historical. |
| Validator and support route maps drift | High | Update both in the same task and rely on quality gate route-map equality checks. |
| Stage 04 date-based route gets accidentally changed | Medium | Include a preservation scan for `docs/04.execution/(plans|tasks)/YYYY-MM-DD`. |
| Old PRD links break after `git mv` | High | Run stale PRD scans and repository quality gates before committing the rename unit. |
| New `docs/superpowers` paths bypass repo taxonomy | Medium | Store all implementation plans in `docs/04.execution/plans/` and task evidence in `docs/04.execution/tasks/`. |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: Repository-static validation only: `git diff --check`,
  stale route scans, inventory scans, and `bash scripts/validate-repo-quality-gates.sh .`.
- **Sandbox / Canary Rollout**: Not applicable; documentation-only route
  migration.
- **Human Approval Gate**: Required before executing this plan. Live runtime,
  CI topology, provider config, model policy, GitOps manifest, secret, push,
  merge, and PR actions are out of scope.
- **Rollback Trigger**: Restore previous commit state if quality gates fail in
  a way that cannot be resolved without changing the approved route contract.
- **Prompt / Model Promotion Criteria**: Not applicable.

## Completion Criteria

- [ ] Stage 04 task evidence exists and is complete.
- [ ] Four active PRDs are renamed to `001-` through `004-`.
- [ ] Stage 01 README lists numeric PRD filenames and numeric PRD target
  pattern.
- [ ] Stage 03 README and helper template examples use the numbered
  feature-folder route.
- [ ] `docs/99.templates/README.md` and
  `docs/99.templates/support/template-routing.md` have matching route maps.
- [ ] `scripts/validate-repo-quality-gates.sh` enforces numeric PRD and Stage
  03 route globs.
- [ ] Old current-route pattern scans pass.
- [ ] `git diff --check` passes.
- [ ] `bash scripts/validate-repo-quality-gates.sh .` passes.
- [ ] Progress memory records the route distinction and validation closure.

## Related Documents

- **Spec**: [../../03.specs/019-template-path-numbering-contract/spec.md](../../03.specs/019-template-path-numbering-contract/spec.md)
- **Task Record**: `../tasks/2026-07-05-template-path-numbering-contract.md`
- **Template Routing**: [../../99.templates/support/template-routing.md](../../99.templates/support/template-routing.md)
- **SDLC Governance**: [../../99.templates/support/sdlc-governance.md](../../99.templates/support/sdlc-governance.md)
- **Templates README**: [../../99.templates/README.md](../../99.templates/README.md)
- **Stage Authoring Matrix**: [../../00.agent-governance/rules/stage-authoring-matrix.md](../../00.agent-governance/rules/stage-authoring-matrix.md)
- **Documentation Protocol**: [../../00.agent-governance/rules/documentation-protocol.md](../../00.agent-governance/rules/documentation-protocol.md)
- **Quality Gate**: [../../../scripts/validate-repo-quality-gates.sh](../../../scripts/validate-repo-quality-gates.sh)
