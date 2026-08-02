---
title: 'Current Surface and Stash Reconciliation Implementation Plan'
type: sdlc/plan
status: draft
owner: platform
updated: 2026-08-02
---

# Current Surface and Stash Reconciliation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> `superpowers:subagent-driven-development` to execute one work package at a
> time, preserve the stash, and require both specification and quality review
> before closing each logical commit.

## Overview

**Goal:** Activate PRD-007 as a five-tranche program, inventory every tracked
target against current canonical owners, and reconcile the preserved stash by
reviewed semantic disposition without applying or dropping it.

**Architecture:** `validation-surfaces.json` remains the only path-to-surface
router. The reciprocal Task becomes the durable current-target matrix and
stash ledger, while any temporary inventory lives only in non-sensitive
ignored `_workspace` scratch and is removed before closure.

**Tech Stack:** Git object metadata, Python 3 document and affected-surface
validators, JSON registry contracts, Bash repository gates, and pre-commit.

## Context

[Spec 047](../../03.specs/047-current-surface-and-stash-reconciliation/spec.md)
is the foundation tranche for PRD-007. It is authorized to observe, classify,
and record current state; it is not authorized to implement the GitHub,
platform, Traefik, IaC, CI, or live-system changes owned by Specs 048-051.

The current route owner is
`docs/00.agent-governance/contracts/validation-surfaces.json`. Program lineage
is owned by `docs/99.templates/support/document-profiles.json` and its strict
registry validator. The preserved stash object is
`6370311e020620cc2743005896cc88db97d15465`; implementation must resolve it by
full object identity rather than assuming `stash@{0}` remains stable.

### Global Constraints

- Every shell command begins with `rtk`.
- Read only Git-tracked repository data and Git metadata needed for the scoped
  reconciliation. Do not read ignored/private state, secret values, auth
  files, shell history, provider logs, or RTK logs.
- Never run `git stash apply`, `git stash pop`, or `git stash drop` in this
  tranche, and never inspect the untracked-parent payload.
- Do not add another path-routing contract or copy route regexes out of
  `validation-surfaces.json`.
- Every target receives exactly one `change`, `no-change`, or `defer`
  disposition and one canonical owner. Every stash hunk receives exactly one
  `already-present`, `port`, `regenerate-current`, `superseded`, or
  `preserve-history` category.
- Keep active target files unchanged unless current evidence proves Spec 047
  itself owns a registry or generated-evidence correction.

## Goals & In-Scope

- Create and activate the reciprocal Spec 047 Plan/Task path.
- Add PRD-007, ARD-0010, ADR-0021, and Specs 047-051 to program lineage with
  Spec 047 as the first unfinished relation.
- Update hard-coded program-lineage validator expectations and their tests.
- Enumerate every tracked file under `.github`, `examples`, `gitops`,
  `infrastructure`, `policy`, `scripts`, `secrets`, `tests`, and `traefik`.
- Resolve each file through the current surface router and record owner,
  current observation, disposition, and successor.
- Reconcile the stash's tracked deltas path by path; preserve untracked-parent
  content without inspection.
- Regenerate `active-corpus-residue-closure.json` only when its current
  validator proves stale generated identity and the current producer is used.
- Close Spec 047 with reviewed evidence and hand Spec 048 a stable baseline.

## Non-Goals & Out-of-Scope

- GitHub native projection, workflow/job consolidation, branch rules, hosted
  execution, push, PR, or remote mutation.
- Kubernetes/GitOps desired-state remediation, Traefik semantics, Terraform,
  Bicep, cloud, provider, cluster, Vault, ESO, TLS, or deployment work.
- Ignored/private data, raw secret material, untracked stash payloads, or live
  evidence.
- Cosmetic edits, README frontmatter insertion, completed-history rewrites, or
  moving implementation work out of its successor Spec.

## Work Breakdown

| ID | Work package | Depends on | Entry gate | Exit evidence |
| --- | --- | --- | --- | --- |
| CSASR-000 | Activate PRD-007 lineage and reciprocal execution path | Approved written Plans | Clean isolated worktree | Decision readiness commit activates ADR-0021; program activation commit then accepts it and activates the reciprocal program foundation |
| CSASR-001 | Build tracked target inventory and surface projection | CSASR-000 | Current routing contract passes | Every tracked target has one current surface ID and canonical owner |
| CSASR-002 | Record audit delta and disposition matrix | CSASR-001 | Current audits and target observations are available | Every target is `change`, `no-change`, or `defer` with evidence and successor |
| CSASR-003 | Record tracked stash reconciliation ledger | CSASR-001 | Exact stash object and tracked path list resolve | Every tracked hunk has one category; untracked-parent content remains uninspected |
| CSASR-004 | Regenerate only validator-proven derived evidence | CSASR-002, CSASR-003 | Current generator reports stale identity | Current-generated object replaces stale identity without copying stash output |
| CSASR-005 | Review, validate, close, and hand off | CSASR-002 through CSASR-004 | Matrix and ledger have no uncovered row | Spec/Plan/Task close with QA/review evidence and Spec 048 becomes first unfinished |

### File map and interfaces

**Create before execution:**

- `docs/04.execution/plans/2026-08-02-current-surface-and-stash-reconciliation.md`
- `docs/04.execution/tasks/2026-08-02-current-surface-and-stash-reconciliation.md`

**Modify during execution:**

- `docs/99.templates/support/document-profiles.json`
- `scripts/validate-document-contract-registry.py`
- `scripts/validate-links-and-owners.py`
- `tests/fixtures/links-and-owners.json`
- registry-focused tests/fixtures only when the current expected projection is
  encoded there
- `docs/03.specs/047-current-surface-and-stash-reconciliation/spec.md`
- `docs/03.specs/README.md`
- `docs/04.execution/plans/README.md`
- `docs/04.execution/tasks/README.md`
- the five reciprocal program Plan/Task pairs:
  - `docs/04.execution/plans/2026-08-02-current-surface-and-stash-reconciliation.md`
    and `docs/04.execution/tasks/2026-08-02-current-surface-and-stash-reconciliation.md`
  - `docs/04.execution/plans/2026-08-02-github-routing-and-ci-evidence.md`
    and `docs/04.execution/tasks/2026-08-02-github-routing-and-ci-evidence.md`
  - `docs/04.execution/plans/2026-08-02-platform-validation-and-security-evidence.md`
    and `docs/04.execution/tasks/2026-08-02-platform-validation-and-security-evidence.md`
  - `docs/04.execution/plans/2026-08-02-example-iac-and-validator-qa.md`
    and `docs/04.execution/tasks/2026-08-02-example-iac-and-validator-qa.md`
  - `docs/04.execution/plans/2026-08-02-repository-assurance-integration-and-closure.md`
    and `docs/04.execution/tasks/2026-08-02-repository-assurance-integration-and-closure.md`
- `docs/00.agent-governance/memory/progress.md`
- `docs/90.references/data/active-corpus-residue-closure.json` only after a
  current validator-proven regeneration need

**Consume:**

- `validate_affected_surfaces.py::{tracked_paths, classify_path, select_paths, run_self_test}`
- `document_lifecycle.py::{compare_lifecycle, validate_transition_evidence}`
- `document_contracts.py::{_program_lineage_from_mapping, _program_structure_diagnostics}`
- `validate-active-corpus-residue-closure.py` self-test and production modes

### Task 1: CSASR-000 — activate the program foundation

- [ ] Verify clean branch, baseline, stash identity, and existing program list.

  ```bash
  rtk git status --short --branch
  rtk git rev-parse HEAD
  rtk git rev-parse refs/stash
  rtk jq -r '.programLineage.programs[] | [.prd,.ard,([.tranches[].spec] | join(","))] | @tsv' docs/99.templates/support/document-profiles.json
  ```

- [ ] Add the PRD-007 program with ordered Specs 047-051 and decision `0021`;
  make only Spec 047 active and keep successors planned.

- [ ] Update the registry validator's exact program projection and add a
  mutation case proving missing, duplicate, or reordered PRD-007 tranches fail.

- [ ] Commit decision readiness first: move ADR-0021 from `draft` to `active`
  with same-diff body/index evidence using subject
  `docs: activate repository delivery decision`.

- [ ] In the following program activation commit, move ADR-0021 from `active`
  to `accepted`; change PRD-007, ARD-0010, Spec 047, this Plan, and its Task to
  `active`; and update owning indexes/progress atomically using subject
  `docs: activate repository delivery program lineage`.

- [ ] Preserve one reciprocal Plan/Task pair per original tranche, keep future
  pairs in `draft`, remove rendered cross-tranche Spec links, and prove with
  focused mutations that draft preplanning passes while malformed or premature
  execution components fail.

- [ ] Run RED/GREEN lifecycle and registry checks.

  ```bash
  rtk python3 scripts/validate-document-contract-registry.py --self-test
  rtk python3 scripts/validate-document-contract-registry.py --root . --mode strict
  rtk python3 scripts/validate-document-lifecycle.py --root . --self-test
  rtk python3 scripts/validate-document-lifecycle.py --root . --mode staged
  rtk python3 scripts/validate-markdown-profiles.py --root . --mode strict
  rtk python3 scripts/validate-links-and-owners.py --root . --self-test
  rtk python3 scripts/validate-links-and-owners.py --root . --mode strict --body-contracts registry
  ```

- [ ] Commit the exact two-phase activation sequence.

  ```bash
  rtk git add docs/02.architecture/decisions/0021-canonical-surface-routing-and-evidence-depth.md docs/02.architecture/decisions/README.md docs/04.execution/plans/2026-08-02-current-surface-and-stash-reconciliation.md
  rtk git commit -m "docs: activate repository delivery decision"

  rtk git add docs/00.agent-governance/memory/progress.md docs/01.requirements/007-repository-delivery-and-platform-assurance.md docs/01.requirements/README.md docs/02.architecture/requirements/0010-repository-delivery-evidence-architecture.md docs/02.architecture/requirements/README.md docs/02.architecture/decisions/0021-canonical-surface-routing-and-evidence-depth.md docs/02.architecture/decisions/README.md docs/03.specs/047-current-surface-and-stash-reconciliation/spec.md docs/03.specs/README.md docs/04.execution/plans/2026-08-02-current-surface-and-stash-reconciliation.md docs/04.execution/plans/2026-08-02-github-routing-and-ci-evidence.md docs/04.execution/plans/2026-08-02-platform-validation-and-security-evidence.md docs/04.execution/plans/2026-08-02-example-iac-and-validator-qa.md docs/04.execution/plans/2026-08-02-repository-assurance-integration-and-closure.md docs/04.execution/plans/README.md docs/04.execution/tasks/2026-08-02-current-surface-and-stash-reconciliation.md docs/04.execution/tasks/2026-08-02-github-routing-and-ci-evidence.md docs/04.execution/tasks/2026-08-02-platform-validation-and-security-evidence.md docs/04.execution/tasks/2026-08-02-example-iac-and-validator-qa.md docs/04.execution/tasks/2026-08-02-repository-assurance-integration-and-closure.md docs/04.execution/tasks/README.md docs/99.templates/support/document-profiles.json scripts/validate-document-contract-registry.py scripts/validate-links-and-owners.py tests/fixtures/links-and-owners.json
  rtk git commit -m "docs: activate repository delivery program lineage"
  ```

### Task 2: CSASR-001 and CSASR-002 — inventory and disposition

- [ ] Record the exact tracked target list in the Task, with one row per path.

  ```bash
  rtk git ls-files .github examples gitops infrastructure policy scripts secrets tests traefik
  rtk python3 scripts/validate-affected-surfaces.py --root . --self-test
  rtk python3 scripts/validate-affected-surfaces.py --root .
  ```

- [ ] For each tracked path, record `target`, `surfaceId`, `canonicalOwner`,
  `auditFinding`, current `observation`, `disposition`, `nextSpec`, `limitation`,
  `owner`, and `retryTrigger`. A `no-change` row requires evidence; a `defer`
  row requires an accountable successor.

- [ ] Compare current observations to the Current audit pack without editing
  dated audit findings or promoting old remote/live evidence.

- [ ] Validate the Task body and commit only the disposition evidence.

  ```bash
  rtk python3 scripts/validate-markdown-profiles.py --root . --mode strict
  rtk python3 scripts/validate-links-and-owners.py --root . --mode strict --body-contracts registry
  rtk git diff --check
  rtk git add docs/04.execution/tasks/2026-08-02-current-surface-and-stash-reconciliation.md docs/00.agent-governance/memory/progress.md
  rtk git commit -m "docs: record current surface disposition matrix"
  ```

### Task 3: CSASR-003 and CSASR-004 — reconcile tracked stash intent

- [ ] Re-resolve the full stash object and parents using metadata only.

  ```bash
  rtk git rev-parse refs/stash
  rtk git rev-parse 6370311e020620cc2743005896cc88db97d15465^1
  rtk git rev-parse 6370311e020620cc2743005896cc88db97d15465^2
  rtk git rev-parse 6370311e020620cc2743005896cc88db97d15465^3
  ```

- [ ] List tracked base-to-index and index-to-worktree paths without reading
  parent-three untracked content.

  ```bash
  rtk git diff --name-status --no-renames 6370311e020620cc2743005896cc88db97d15465^1 6370311e020620cc2743005896cc88db97d15465^2
  rtk git diff --name-status --no-renames 6370311e020620cc2743005896cc88db97d15465^2 6370311e020620cc2743005896cc88db97d15465
  ```

- [ ] Record each emitted tracked path in the Task before inspecting its
  path-scoped delta. Assign each hunk exactly one approved category and record
  destination owner, adopted commit or non-adoption reason, and reviewer.

- [ ] Run the current residue validator. Regenerate only with the current
  producer if it fails solely because the generated identity is stale.

  ```bash
  rtk python3 scripts/validate-active-corpus-residue-closure.py --root . --self-test
  rtk python3 scripts/validate-active-corpus-residue-closure.py --root .
  ```

- [ ] Commit the stash ledger and any current-generated object as one reviewed
  evidence unit; never copy the stash's generated object.

  ```bash
  rtk git add docs/04.execution/tasks/2026-08-02-current-surface-and-stash-reconciliation.md docs/00.agent-governance/memory/progress.md docs/90.references/data/active-corpus-residue-closure.json
  rtk git commit -m "docs: record stash reconciliation ledger"
  ```

### Task 4: CSASR-005 — review and close the foundation

- [ ] Run focused, document, affected, aggregate, all-files, formatter, and
  diff gates; inspect any formatter mutation before proceeding.

  ```bash
  rtk python3 scripts/validate-document-contract-registry.py --self-test
  rtk python3 scripts/validate-document-contract-registry.py --root . --mode strict
  rtk python3 scripts/validate-document-lifecycle.py --root . --mode staged
  rtk python3 scripts/validate-affected-surfaces.py --root . --self-test
  rtk python3 scripts/validate-affected-surfaces.py --root .
  rtk bash scripts/validate-repo-quality-gates.sh .
  rtk pre-commit run --all-files
  rtk git status --short
  rtk git diff --check
  ```

- [ ] Dispatch independent requirements and quality/security reviewers over the
  exact Spec 047 activation-to-HEAD diff; resolve all findings and rerun gates.

- [ ] Set Spec 047, Plan, and Task to `done`, set its program row to `done`,
  update indexes/progress, and make Spec 048 the first unfinished relation.

- [ ] Commit closure without preclaiming its own SHA.

  ```bash
  rtk git add docs/00.agent-governance/memory/progress.md docs/03.specs/047-current-surface-and-stash-reconciliation/spec.md docs/03.specs/README.md docs/04.execution/plans/2026-08-02-current-surface-and-stash-reconciliation.md docs/04.execution/plans/README.md docs/04.execution/tasks/2026-08-02-current-surface-and-stash-reconciliation.md docs/04.execution/tasks/README.md docs/99.templates/support/document-profiles.json
  rtk git commit -m "docs: close current surface reconciliation tranche"
  ```

## Verification Plan

```bash
rtk python3 scripts/validate-document-contract-registry.py --self-test
rtk python3 scripts/validate-document-contract-registry.py --root . --mode strict
rtk python3 scripts/validate-markdown-profiles.py --root . --mode strict
rtk python3 scripts/validate-links-and-owners.py --root . --mode strict --body-contracts registry
rtk python3 scripts/validate-document-lifecycle.py --root . --self-test
rtk python3 scripts/validate-document-lifecycle.py --root . --mode staged
rtk python3 scripts/validate-affected-surfaces.py --root . --self-test
rtk python3 scripts/validate-affected-surfaces.py --root .
rtk python3 scripts/validate-active-corpus-residue-closure.py --root . --self-test
rtk python3 scripts/validate-active-corpus-residue-closure.py --root .
rtk bash scripts/validate-repo-quality-gates.sh .
rtk pre-commit run --all-files
rtk git diff --check
```

No command in this Plan proves hosted, provider, credential-bearing, remote,
or live readiness. Those lanes remain `DEFER`.

## Risks & Mitigations

| Risk | Mitigation |
| --- | --- |
| Program lineage and lifecycle statuses disagree | Activate/close Spec, Plan, Task, indexes, progress, registry, and expected projection atomically; staged lifecycle is blocking. |
| Surface inventory is incomplete | Generate from `git ls-files` over all nine target roots and require one Task row per emitted path. |
| Stash ordinal changes | Resolve the full object hash before every operation and preserve all stashes on mismatch. |
| Stash exposes untracked/private content | Never inspect parent-three payload; limit analysis to current tracked paths and metadata. |
| Stale generated identity is copied | Run the current producer and compare current validation; never reuse stash-generated object IDs. |
| Successor implementation leaks into foundation | Record `change`/`defer` and `nextSpec`; reject active-target edits not owned by Spec 047. |

## Completion Criteria

- PRD-007 program lineage is structurally valid with Specs 047-051 ordered and
  Spec 048 first unfinished after closure.
- Every tracked target path has exactly one surface, owner, disposition, and
  successor/evidence record.
- Every inspected tracked stash hunk has exactly one approved category, while
  untracked-parent content remains uninspected and the stash remains present.
- Any derived evidence change is produced by the current generator and passes
  its current validator.
- Strict documents, lifecycle, affected surfaces, aggregate, all-files, diff,
  and independent reviews pass with no open finding.
- No downstream implementation, remote mutation, live action, secret read, or
  stash apply/pop/drop occurred.

## Traceability

- **Spec**: [Current Surface and Stash Reconciliation](../../03.specs/047-current-surface-and-stash-reconciliation/spec.md)
- **Task**: [Current Surface and Stash Reconciliation Task](../tasks/2026-08-02-current-surface-and-stash-reconciliation.md)
- **Program**: [PRD-007](../../01.requirements/007-repository-delivery-and-platform-assurance.md)
- **Architecture**: [ARD-0010](../../02.architecture/requirements/0010-repository-delivery-evidence-architecture.md)
- **Decision**: [ADR-0021](../../02.architecture/decisions/0021-canonical-surface-routing-and-evidence-depth.md)
- **Successor**: [Spec 048](../../03.specs/048-github-routing-and-ci-evidence/spec.md)

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-CSASR-001](../../03.specs/047-current-surface-and-stash-reconciliation/spec.md#success-criteria--verification-plan) | CSASR-000, CSASR-001 | [Activation and inventory evidence](../tasks/2026-08-02-current-surface-and-stash-reconciliation.md#task-table) |
| N/A — VAL-CSASR-002 and VAL-CSASR-003 share the Spec source above | CSASR-002 | N/A — reciprocal Task is linked in VAL-CSASR-001 |
| N/A — VAL-CSASR-004 and VAL-CSASR-005 share the Spec source above | CSASR-003, CSASR-004 | N/A — reciprocal Task is linked in VAL-CSASR-001 |
| N/A — VAL-CSASR-006 and VAL-CSASR-007 share the Spec source above | CSASR-001, CSASR-003 | N/A — reciprocal Task is linked in VAL-CSASR-001 |
| N/A — VAL-CSASR-008 and VAL-CSASR-009 share the Spec source above | CSASR-005 | N/A — reciprocal Task is linked in VAL-CSASR-001 |
