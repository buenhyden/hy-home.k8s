---
title: 'SDLC Lifecycle Contract Implementation Plan'
type: sdlc/plan
status: done
owner: platform
updated: 2026-07-06
---

# SDLC Lifecycle Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the SDLC lifecycle, numbering, archive metadata,
active-surface, and `_workspace` staging contracts defined by the Stage 03
specification.

**Architecture:** This is a repository-static governance overlay. Stage 99
template support documents own reusable documentation contracts, Stage 00 owns
agent-facing routing rules, Stage 98 owns archive behavior, Stage 04 owns
execution evidence, and `scripts/validate-repo-quality-gates.sh` enforces the
deterministic subset of the contract.

**Tech Stack:** Markdown, POSIX shell, Git, repository quality gate script,
Stage 00/03/04/98/99 documentation contracts.

---

## Overview

This plan implements the approved SDLC lifecycle contract for `hy-home.k8s`.
It aligns contract documents, archive tombstone frontmatter, active document
surfaces, `_workspace` rules, and validation checks without changing live
infrastructure or external systems.

## Context

The repository already has numeric PRD and Spec route contracts, template
support documents, Stage 00 agent governance, archive tombstones, and a
repository quality gate. The new specification
`../../03.specs/021-sdlc-lifecycle-contract/spec.md` consolidates those rules
into an explicit lifecycle contract and adds archive preservation metadata and
active-surface limits.

## Goals & In-Scope

- Align Stage 99 support contracts with the SDLC lifecycle state, numbering,
  handoff, archive, active-surface, and `_workspace` rules.
- Align Stage 00 agent-facing routing and authoring rules with Stage 99.
- Extend archive tombstone frontmatter and template rules with
  `original_path`, `archived_on`, `archive_reason`, and `replacement`.
- Update existing archive tombstones so the future validator can enforce the
  new archive profile.
- Confirm active PRD and Spec routes use numeric path contracts.
- Keep Stage 04 plans and tasks date-based.
- Add deterministic repository quality gates for legacy routes, archive
  metadata, and `_workspace` staging boundaries.
- Record execution evidence in Stage 04 task records.

## Non-Goals & Out-of-Scope

- Live Kubernetes, Argo CD, Vault, ESO, GitHub remote, branch protection,
  ruleset, credential, CI provider, or third-party mutation.
- Secret value inspection.
- Bulk renumbering historical documents only to close numeric gaps.
- Moving Stage 04 plans or tasks away from date-based route names.
- Adding full archived body snapshots by default.
- Rewriting unrelated historical prose that does not affect the active
  lifecycle contract or validation.

## Work Breakdown

| Task | Description | Files / Docs Affected | Target Requirement | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | Align SDLC lifecycle and handoff contracts | `docs/99.templates/support/sdlc-governance.md`, `docs/99.templates/support/template-routing.md`, `docs/99.templates/support/documentation-contract.md`, `docs/00.agent-governance/rules/document-stage-routing.md`, `docs/00.agent-governance/rules/stage-authoring-matrix.md` | VAL-SDLC-LC-001 | Contract surfaces describe the same lifecycle, numbering, handoff, and active-surface rules. |
| PLN-002 | Extend archive tombstone metadata contract and current tombstones | `docs/99.templates/support/frontmatter-schema.md`, `docs/99.templates/templates/common/archive-tombstone.template.md`, `docs/98.archive/README.md`, `docs/98.archive/**/*.md`, `scripts/validate-repo-quality-gates.sh` | VAL-SDLC-LC-003 | Archive tombstones contain `original_path`, `archived_on`, `archive_reason`, and `replacement`, and the archive profile allows those keys. |
| PLN-003 | Align active surface evidence and `_workspace` boundary | `_workspace/README.md`, `docs/01.requirements/README.md`, `docs/03.specs/README.md`, `docs/04.execution/tasks/2026-07-06-sdlc-lifecycle-contract.md`, `docs/04.execution/tasks/README.md` | VAL-SDLC-LC-002, VAL-SDLC-LC-004 | Active routes and workspace staging rules match the new contract; task evidence exists. |
| PLN-004 | Add validator checks and close validation | `scripts/validate-repo-quality-gates.sh`, Stage 04 task evidence, progress memory when required | VAL-SDLC-LC-005 | `git diff --check`, shell syntax check, and repository quality gates pass. |

## Implementation Tasks

### Task 1: Align Lifecycle Contract Surfaces

**Files:**

- Modify: `docs/99.templates/support/sdlc-governance.md`
- Modify: `docs/99.templates/support/template-routing.md`
- Modify: `docs/99.templates/support/documentation-contract.md`
- Modify: `docs/00.agent-governance/rules/document-stage-routing.md`
- Modify: `docs/00.agent-governance/rules/stage-authoring-matrix.md`

- [ ] **Step 1: Read current contract owners**

Run:

```bash
sed -n '1,260p' docs/99.templates/support/sdlc-governance.md
sed -n '1,240p' docs/99.templates/support/template-routing.md
sed -n '1,260p' docs/99.templates/support/documentation-contract.md
sed -n '1,260p' docs/00.agent-governance/rules/document-stage-routing.md
sed -n '1,260p' docs/00.agent-governance/rules/stage-authoring-matrix.md
```

Expected: each file has one owning purpose and no unrelated implementation
edits are needed.

- [ ] **Step 2: Add one shared lifecycle table to the Stage 99 SDLC owner**

Update `docs/99.templates/support/sdlc-governance.md` with these contract
rules in topic-specific prose:

```text
PRD: draft -> active -> done | archived
ARD/ADR: draft -> active -> accepted | archived
Spec: draft -> active -> done | archived
Plan/Task: draft -> active -> done | archived
Operations: draft -> active -> accepted | archived
Archive Tombstone: archived only
```

Also state that PRD and Spec numeric identifiers should match for the same
feature lineage when creating new work, while historical mismatches are kept
and linked explicitly.

- [ ] **Step 3: Update route and documentation contracts**

Update `template-routing.md` and `documentation-contract.md` so they both
state:

```text
Stage 01 PRDs use docs/01.requirements/<###-Numbering>-<feature-or-system>.md.
Stage 03 specs use docs/03.specs/<###-Numbering>-<feature-id>/spec.md.
Stage 04 plans and tasks stay date-based execution records.
README files route readers to lifecycle contract owners instead of carrying
full governance bodies.
```

- [ ] **Step 4: Update Stage 00 agent-facing routing**

Update `document-stage-routing.md` and `stage-authoring-matrix.md` so agents
see the same state transitions, handoff links, and active-surface duplicate
rule before editing documents.

- [ ] **Step 5: Validate contract wording**

Run:

```bash
rg -n "draft -> active|original_path|active-surface|<###-Numbering>-<feature" docs/99.templates/support docs/00.agent-governance/rules
git diff --check
```

Expected: the lifecycle wording appears in the contract owners and
`git diff --check` prints no errors.

- [ ] **Step 6: Commit Task 1**

Run:

```bash
git add docs/99.templates/support/sdlc-governance.md docs/99.templates/support/template-routing.md docs/99.templates/support/documentation-contract.md docs/00.agent-governance/rules/document-stage-routing.md docs/00.agent-governance/rules/stage-authoring-matrix.md
git commit -m "docs(governance): Align SDLC lifecycle contracts"
```

### Task 2: Extend Archive Tombstone Metadata

**Files:**

- Modify: `docs/99.templates/support/frontmatter-schema.md`
- Modify: `docs/99.templates/templates/common/archive-tombstone.template.md`
- Modify: `docs/98.archive/README.md`
- Modify: `docs/98.archive/**/*.md`
- Modify: `scripts/validate-repo-quality-gates.sh`

- [ ] **Step 1: Inspect archive profile and tombstones**

Run:

```bash
sed -n '1,260p' docs/99.templates/support/frontmatter-schema.md
sed -n '1,220p' docs/99.templates/templates/common/archive-tombstone.template.md
sed -n '1,260p' docs/98.archive/README.md
find docs/98.archive -type f -name '*.md' | sort
```

Expected: archive tombstones currently use the common archive template and can
be updated in place.

- [ ] **Step 2: Extend frontmatter schema**

Update the `content/archive-tombstone` profile in
`frontmatter-schema.md` so required keys are:

```text
title, type, status, owner, updated, original_path, archived_on,
archive_reason, replacement
```

Document allowed `archive_reason` values:

```text
superseded, duplicate, obsolete, migrated, historical-baseline
```

Update `scripts/validate-repo-quality-gates.sh` in the same logical unit so
the `content/archive-tombstone` profile allows and validates those four
archive-specific frontmatter keys. Later Task 4 may add broader route and
closure checks, but this task keeps the repository quality gate passing while
the archive schema changes.

- [ ] **Step 3: Update archive template**

Update `archive-tombstone.template.md` frontmatter to include:

```yaml
original_path: docs/<original-path>.md
archived_on: YYYY-MM-DD
archive_reason: superseded
replacement: docs/<replacement-path>.md
```

The body should remain a concise tombstone record and should not copy the full
archived document body.

- [ ] **Step 4: Update archive README**

Update `docs/98.archive/README.md` so it states that archive preservation is
frontmatter-based by default and that full snapshots require a documented
exception.

- [ ] **Step 5: Update existing archive tombstones**

For each `docs/98.archive/**/*.md` file, add the four archive metadata keys
below the standard five keys. Use the original active path implied by the
archive mirror path when the body does not already name one:

```text
docs/98.archive/01.requirements/example.md -> docs/01.requirements/example.md
docs/98.archive/03.specs/example/spec.md -> docs/03.specs/example/spec.md
docs/98.archive/04.execution/plans/example.md -> docs/04.execution/plans/example.md
```

Use `archive_reason: superseded` when existing tombstone prose says the
document was replaced by current implementation, `archive_reason: duplicate`
for duplicate consolidation, `archive_reason: obsolete` for stale material
without a replacement, `archive_reason: migrated` for route migration, and
`archive_reason: historical-baseline` for intentionally retained baselines.
Use `replacement: none` when no replacement path exists.

- [ ] **Step 6: Validate archive metadata**

Run:

```bash
missing=0; for key in original_path archived_on archive_reason replacement; do while IFS= read -r f; do if ! rg -q "^${key}:" "$f"; then echo "$f missing $key"; missing=1; fi; done < <(find docs/98.archive -type f -name '*.md' ! -name README.md | sort); done; exit $missing
git diff --check
bash -n scripts/validate-repo-quality-gates.sh
bash scripts/validate-repo-quality-gates.sh .
```

Expected: the metadata loop prints no archive tombstone path and the diff,
shell syntax, and repository quality gates pass.

- [ ] **Step 7: Commit Task 2**

Run:

```bash
git add docs/99.templates/support/frontmatter-schema.md docs/99.templates/templates/common/archive-tombstone.template.md docs/98.archive scripts/validate-repo-quality-gates.sh docs/04.execution/plans/2026-07-06-sdlc-lifecycle-contract.md
git commit -m "docs(archive): Add archive tombstone metadata contract"
```

### Task 3: Align Active Surface Evidence and Workspace Boundary

**Files:**

- Modify: `_workspace/README.md`
- Modify: `docs/01.requirements/README.md`
- Modify: `docs/03.specs/README.md`
- Create: `docs/04.execution/tasks/2026-07-06-sdlc-lifecycle-contract.md`
- Modify: `docs/04.execution/tasks/README.md`

- [ ] **Step 1: Verify active numeric routes**

Run:

```bash
find docs/01.requirements -maxdepth 1 -type f -name '*.md' -printf '%f\n' | sort
find docs/03.specs -maxdepth 1 -mindepth 1 -type d -printf '%f\n' | sort
```

Expected: active PRDs use `001-...md` style names, active spec folders use
`NNN-...` style names, and `README.md` is the only non-PRD file in Stage 01.

- [ ] **Step 2: Update active stage README wording only where needed**

Ensure `docs/01.requirements/README.md` and `docs/03.specs/README.md` route
readers to the numeric lifecycle contract and do not describe date-based PRD
or unnumbered spec folders as current active patterns.

- [ ] **Step 3: Confirm `_workspace` boundary**

Update `_workspace/README.md` to keep this boundary explicit:

```text
Allowed: temporary non-secret repo-support artifacts such as generated route
inventories, dry-run logs, migration ledgers, and audit scratch.
Prohibited: diagnostics that may contain local private state, auth files,
tokens, credentials, kubeconfigs, shell history, browser profiles, provider
caches, SSH keys, and secret-bearing logs.
```

- [ ] **Step 4: Create Stage 04 task evidence**

Create `docs/04.execution/tasks/2026-07-06-sdlc-lifecycle-contract.md` with
frontmatter:

```yaml
title: 'Task: SDLC Lifecycle Contract'
type: sdlc/task
status: draft
owner: platform
updated: 2026-07-06
```

The task table must include `T-001` through `T-004` matching this plan and
leave validation evidence fields ready to receive final command results.

- [ ] **Step 5: Update task README index**

Add the task record to `docs/04.execution/tasks/README.md` structure and
document index with status `Draft` and updated date `2026-07-06`.

- [ ] **Step 6: Validate active surface and workspace edits**

Run:

```bash
rg -n "YYYY-MM-DD-<feature-or-system>|docs/03\\.specs/<feature-id>|docs/03\\.specs/[a-z][^/]+/spec\\.md" docs/01.requirements docs/03.specs docs/99.templates docs/00.agent-governance scripts
rg -n "token|credential|kubeconfig|shell history|dry-run|migration ledger" _workspace/README.md
git diff --check
```

Expected: legacy active route examples are absent or explicitly historical,
the `_workspace` README contains the allowed/prohibited boundary, and
`git diff --check` prints no errors.

- [ ] **Step 7: Commit Task 3**

Run:

```bash
git add _workspace/README.md docs/01.requirements/README.md docs/03.specs/README.md docs/04.execution/tasks/2026-07-06-sdlc-lifecycle-contract.md docs/04.execution/tasks/README.md
git commit -m "docs(tasks): Record SDLC lifecycle contract execution"
```

### Task 4: Add Validation Gates and Close Evidence

**Files:**

- Modify: `scripts/validate-repo-quality-gates.sh`
- Modify: `docs/03.specs/021-sdlc-lifecycle-contract/spec.md`
- Modify: `docs/04.execution/tasks/2026-07-06-sdlc-lifecycle-contract.md`
- Modify: `docs/04.execution/plans/2026-07-06-sdlc-lifecycle-contract.md`
- Modify: `docs/04.execution/plans/README.md`

- [ ] **Step 1: Inspect validator structure**

Run:

```bash
sed -n '1,260p' scripts/validate-repo-quality-gates.sh
rg -n "archive|frontmatter|workspace|requirements|specs|README" scripts/validate-repo-quality-gates.sh
```

Expected: new checks can be added near existing route, frontmatter, archive,
or `_workspace` checks.

- [ ] **Step 2: Add legacy active route checks**

Add deterministic checks that fail when:

```text
docs/01.requirements/YYYY-MM-DD-*.md exists
docs/01.requirements/*.md exists without README.md or a three-digit prefix
docs/03.specs/* exists as an active directory without a three-digit prefix
```

Keep archived historical routes under `docs/98.archive/**` out of this check.

- [ ] **Step 3: Add archive metadata checks**

Add a validator block that scans every `docs/98.archive/**/*.md` tombstone
except `docs/98.archive/README.md` and requires:

```text
type: content/archive-tombstone
status: archived
original_path:
archived_on:
archive_reason:
replacement:
```

The validator should reject archive reasons outside:

```text
superseded, duplicate, obsolete, migrated, historical-baseline
```

- [ ] **Step 4: Keep `_workspace` staging checks aligned**

Ensure the existing `_workspace` check rejects tracked files whose names or
paths indicate auth material, tokens, credentials, kubeconfigs, shell history,
browser profiles, provider caches, SSH keys, or secret-bearing logs.

- [ ] **Step 5: Run validation commands**

Run:

```bash
git diff --check
bash -n scripts/validate-repo-quality-gates.sh
bash scripts/validate-repo-quality-gates.sh .
find docs/01.requirements -maxdepth 1 -type f -name '*.md' ! -name README.md -printf '%f\n' | awk '!/^[0-9][0-9][0-9]-.+\.md$/ { print; bad=1 } END { exit bad }'
find docs/03.specs -maxdepth 1 -mindepth 1 -type d -printf '%f\n' | awk '!/^[0-9][0-9][0-9]-.+/ { print; bad=1 } END { exit bad }'
```

Expected: the first three commands pass; the active route scans print no
violating path and exit 0.

- [ ] **Step 6: Close task evidence and plan status**

Update the Stage 04 task evidence with command results and set this plan
status to `done` only after all validation passes.

- [ ] **Step 7: Commit Task 4**

Run:

```bash
git add scripts/validate-repo-quality-gates.sh docs/04.execution/tasks/2026-07-06-sdlc-lifecycle-contract.md docs/04.execution/plans/2026-07-06-sdlc-lifecycle-contract.md docs/04.execution/plans/README.md
git commit -m "docs(validation): Enforce SDLC lifecycle contract gates"
```

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Structural | Markdown patch whitespace | `git diff --check` | No output and exit 0. |
| VAL-PLN-002 | Syntax | Validator shell syntax | `bash -n scripts/validate-repo-quality-gates.sh` | Exit 0. |
| VAL-PLN-003 | Repository Gate | Full repo quality gate | `bash scripts/validate-repo-quality-gates.sh .` | `[PASS] repository quality gates passed`. |
| VAL-PLN-004 | Route Scan | Legacy active route scan | `find docs/01.requirements -maxdepth 1 -type f -name '*.md' ! -name README.md -printf '%f\n' \| awk '!/^[0-9][0-9][0-9]-.+\.md$/ { print; bad=1 } END { exit bad }'` and `find docs/03.specs -maxdepth 1 -mindepth 1 -type d -printf '%f\n' \| awk '!/^[0-9][0-9][0-9]-.+/ { print; bad=1 } END { exit bad }'` | No violating path is printed and both commands exit 0. |
| VAL-PLN-005 | Archive Metadata | Archive tombstone field scan | `missing=0; for key in original_path archived_on archive_reason replacement; do while IFS= read -r f; do if ! rg -q "^${key}:" "$f"; then echo "$f missing $key"; missing=1; fi; done < <(find docs/98.archive -type f -name '*.md' ! -name README.md \| sort); done; exit $missing` | No archive tombstone path is reported. |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Archive schema changes break existing tombstones | Quality gate fails until all tombstones are updated | Update schema, template, tombstones, and validator in the same logical unit. |
| Active duplicate lineage cannot be inferred safely | Validator could create false positives | Enforce deterministic route and metadata checks; leave semantic duplicate review as documented governance. |
| README files accumulate governance bodies | Contract duplication returns | Keep README edits to index/routing language and place rule bodies in Stage 00/99 owners. |
| `_workspace` rules accidentally allow private local state | Secret-bearing files could enter tracked docs | Keep allowed/prohibited examples explicit and validate risky tracked path names. |

## Agent Rollout & Evaluation Gates

- **Offline Eval Gate**: Repository-static validation only.
- **Sandbox / Canary Rollout**: Not applicable; no runtime rollout.
- **Human Approval Gate**: Required for external mutation, live cluster checks,
  credential changes, GitHub settings changes, merge, push, or PR creation.
- **Rollback Trigger**: Revert the specific logical commit that introduced a
  failing contract or validator change.
- **Prompt / Model Promotion Criteria**: Not applicable.

## Completion Criteria

- [x] Lifecycle contract surfaces aligned.
- [x] Archive tombstone metadata schema, template, README, and existing
  tombstones aligned.
- [x] Active route evidence and `_workspace` boundary aligned.
- [x] Validator enforces deterministic lifecycle and archive checks.
- [x] Stage 04 task evidence records validation results.
- [x] Required validation commands pass.

## Related Documents

- **Spec**: `../../03.specs/021-sdlc-lifecycle-contract/spec.md`
- **Task**: `../tasks/2026-07-06-sdlc-lifecycle-contract.md`
- **Template Routing**: `../../99.templates/support/template-routing.md`
- **Frontmatter Schema**: `../../99.templates/support/frontmatter-schema.md`
- **SDLC Governance**: `../../99.templates/support/sdlc-governance.md`
- **Archive Index**: `../../98.archive/README.md`
