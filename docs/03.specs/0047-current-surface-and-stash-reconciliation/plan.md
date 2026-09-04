---
title: "Current Surface and Stash Reconciliation Implementation Plan"
version: "1.0.0"
type: "sdlc/plan"
status: "active"
owner: "platform"
updated: "2026-09-05"
layer: "specs"
artifact_id: "SPEC-0047-PLAN-0001"
---

# Current Surface and Stash Reconciliation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> `superpowers:subagent-driven-development` to execute one work package at a
> time, preserve the stash, and require both specification and quality review
> before closing each logical commit.

## Overview

### Current Execution Disposition (2026-09-05)

Resume only Spec 0047 after Spec 0052's semantic closure. Accepted ADR-0031
and ADR-0033 replace the old ADR-0021 activation and public program-roster
procedure. This Plan and its Spec use the legal `draft → active` edge;
CSASR-000 closes through `in-progress → done`. CSASR-001 through CSASR-005
remain queued, and successor packages remain draft/queued until sequential
predecessor closure. Their existing Plan/Task records are valid preplanning.

The surviving stash commit `6370311e020620cc2743005896cc88db97d15465` was
re-observed by metadata only. Its tracked-hunk analysis is still unfinished.
Before CSASR-001 begins, re-observe current paths and resolve the older planned
commands against `scripts/validation/registry.json`; retired progress,
generated-residue, package-router, self-test, and registry-instance surfaces
below are historical planning inputs, not instructions to recreate them.
Record new evidence in the owning Task. This resume performs no implementation,
stash application or retirement, remote action, or live operation.

**Goal:** Activate PRD-0007 as a five-tranche program, inventory every tracked
target against current canonical owners, and reconcile the preserved stash by
reviewed semantic disposition without applying or dropping it.

**Architecture:** `scripts/validation/registry.json` remains the only path-to-surface
router. The reciprocal Task becomes the durable current-target matrix and
stash ledger, while any temporary inventory lives only in non-sensitive
ignored `_workspace` scratch and is removed before closure.

**Tech Stack:** Git object metadata, Python 3 document and affected-surface
validators, JSON registry contracts, Bash repository gates, and pre-commit.

## Context

[Spec 047](spec.md)
is the foundation tranche for PRD-0007. It is authorized to observe, classify,
and record current state; it is not authorized to implement the GitHub,
platform, Traefik, IaC, CI, or live-system changes owned by Specs 048-051.

The current route owner is `scripts/validation/registry.json`. The document
registry owns profiles and lifecycle domains; this package's reciprocal
Spec/Plan/Task records own execution under accepted ADR-0031 and ADR-0033. The preserved stash object is
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
  `scripts/validation/registry.json`.
- Every target receives exactly one `change`, `no-change`, or `defer`
  disposition and one canonical owner. Every stash hunk receives exactly one
  `already-present`, `port`, `regenerate-current`, `superseded`, or
  `preserve-history` category.
- Keep active target files unchanged unless current evidence proves Spec 047
  itself owns a registry or generated-evidence correction.

### Legacy Task ledger inputs

This Task is the durable execution ledger for Spec 047. It will record the
PRD-0007 program activation, current tracked target inventory, canonical
surface/owner mapping, one disposition per target, tracked stash reconciliation
categories, any current-generated residue evidence, reviews, validation, and
the handoff to Spec 048. CSASR-000 is done and all later rows remain
queued. This activation claims no target implementation, stash content
adoption, stash apply/pop/drop, remote, or live result.

- Parent [Spec 047](spec.md)
- Parent [Implementation Plan](plan.md)
- [PRD-0007](../../01.requirements/0007-repository-delivery-and-platform-assurance.md),
  [AD-0010](../../02.architecture/descriptions/0010-repository-delivery-evidence-architecture.md),
  and [superseded ADR-0021](../../02.architecture/decisions/0021-canonical-surface-routing-and-evidence-depth.md)
- Current `scripts/validation/registry.json`, document profile registry, Current audit
  pack, tracked repository inventory, and affected-surface validators
- Preserved stash object
  `6370311e020620cc2743005896cc88db97d15465`; ordinal and parents must be
  re-observed at execution time
## Goals & In-Scope

- Create and activate the reciprocal Spec 047 Plan/Task path.
- Resume Spec 0047 through package-local lifecycle authority, preserving
  sequential predecessor dependencies and existing successor preplanning.
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
| CSASR-000 | Activate the package-local reciprocal execution path | Approved written Plans; Spec 0052 semantic closure | Clean approved checkout; accepted ADR-0031/0033 | Spec/Plan activate, the existing activation Task closes, and the Stage 03 index agrees; no public execution roster |
| CSASR-001 | Build tracked target inventory and surface projection | CSASR-000 | Current routing contract passes | Every tracked target has one current surface ID and canonical owner |
| CSASR-002 | Record audit delta and disposition matrix | CSASR-001 | Current audits and target observations are available | Every target is `change`, `no-change`, or `defer` with evidence and successor |
| CSASR-003 | Record tracked stash reconciliation ledger | CSASR-001 | Exact stash object and tracked path list resolve | Every tracked hunk has one category; untracked-parent content remains uninspected |
| CSASR-004 | Regenerate only validator-proven derived evidence | CSASR-002, CSASR-003 | Current generator reports stale identity | Current-generated object replaces stale identity without copying stash output |
| CSASR-005 | Review, validate, close, and hand off | CSASR-002 through CSASR-004 | Matrix and ledger have no uncovered row | Spec/Plan/Task close with QA/review evidence and Spec 048 becomes first unfinished |

### File map and interfaces

**Create before execution:**

- `docs/03.specs/0047-current-surface-and-stash-reconciliation/plan.md`
- `docs/03.specs/0047-current-surface-and-stash-reconciliation/README.md#task-records`

**Modify during execution:**

- `docs/99.templates/registry.json`
- `scripts/validate-document-contract-registry.py`
- `scripts/validate-links-and-owners.py`
- `tests/fixtures/links-and-owners.json`
- registry-focused tests/fixtures only when the current expected projection is
  encoded there
- `docs/03.specs/0047-current-surface-and-stash-reconciliation/spec.md`
- `docs/03.specs/README.md`
- `docs/03.specs/0047-current-surface-and-stash-reconciliation/plan.md`
- `docs/03.specs/0047-current-surface-and-stash-reconciliation/README.md#task-records`
- the five reciprocal program Plan/Task pairs:
  - `docs/03.specs/0047-current-surface-and-stash-reconciliation/plan.md`
    and `docs/03.specs/0047-current-surface-and-stash-reconciliation/README.md#task-records`
  - `docs/03.specs/0047-current-surface-and-stash-reconciliation/plan.md`
    and `docs/03.specs/0047-current-surface-and-stash-reconciliation/README.md#task-records`
  - `docs/03.specs/0047-current-surface-and-stash-reconciliation/plan.md`
    and `docs/03.specs/0047-current-surface-and-stash-reconciliation/README.md#task-records`
  - `docs/03.specs/0047-current-surface-and-stash-reconciliation/plan.md`
    and `docs/03.specs/0047-current-surface-and-stash-reconciliation/README.md#task-records`
  - `docs/03.specs/0047-current-surface-and-stash-reconciliation/plan.md`
    and `docs/03.specs/0047-current-surface-and-stash-reconciliation/README.md#task-records`
- `docs/00.agent-governance/memory/progress.md`
- `docs/90.references/data/active-corpus-residue-closure.json` only after a
  current validator-proven regeneration need

**Consume:**

- `validate_affected_surfaces.py::{tracked_paths, classify_path, select_paths, run_self_test}`
- `document_lifecycle.py::{compare_lifecycle, validate_transition_evidence}`
- `document_contracts.py::{_program_lineage_from_mapping, _program_structure_diagnostics}`
- `validate-active-corpus-residue-closure.py` self-test and production modes

### Task 1: CSASR-000 — activate the package-local foundation

- [x] Verify the clean approved checkout, reachable stash object, accepted
  ADR-0031/0033, package-local Spec/Plan/Task links, and successor queued state.
- [x] Discharge Spec 0052's superseded count predicates through WP-013 semantic
  verification and close that package before resuming Spec 0047.
- [x] Replace the superseded ADR-0021/public-roster activation procedure with
  legal Spec/Plan `draft → active` and activation Task `in-progress → done`
  transitions, keeping every implementation Task queued.
- [x] Align the current Stage 03 index and record validation in
  [CSASR-000](tasks/tsk-0001-csasr-000.md).

This activation changes no ADR lifecycle or Registry entry. The WP-013 logical
commit owns this bounded resumption; the later CSASR work remains unexecuted.

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
  rtk git add docs/03.specs/0047-current-surface-and-stash-reconciliation/README.md#task-records docs/00.agent-governance/memory/progress.md
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
  rtk git add docs/03.specs/0047-current-surface-and-stash-reconciliation/README.md#task-records docs/00.agent-governance/memory/progress.md docs/90.references/data/active-corpus-residue-closure.json
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

- [ ] After every implementation Task and closure gate completes, move this
  Spec and Plan `active → done`, close the executing Task through its legal
  edge, and update the Stage 03 index. Spec 0048 then becomes eligible for
  package-local activation; no Registry instance row is changed.

- [ ] Commit closure without preclaiming its own SHA.

  ```bash
  rtk git add docs/00.agent-governance/memory/progress.md docs/03.specs/0047-current-surface-and-stash-reconciliation/spec.md docs/03.specs/README.md docs/03.specs/0047-current-surface-and-stash-reconciliation/plan.md docs/03.specs/0047-current-surface-and-stash-reconciliation/plan.md docs/03.specs/0047-current-surface-and-stash-reconciliation/README.md#task-records docs/03.specs/0047-current-surface-and-stash-reconciliation/README.md#task-records docs/99.templates/registry.json
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

### Legacy Task verification evidence

CSASR-000 starts from clean branch HEAD
`7a1923d0a93143e3f8d106e98ac5bee25e2a10b5` and observes preserved stash
object `6370311e020620cc2743005896cc88db97d15465`. It activates only the PRD-0007
lineage and reciprocal SDLC path; it does not preclaim its own commit SHA or
any CSASR-001 through CSASR-005 result.

Later work will add the exact target disposition matrix, stash ledger,
current-generator decision, logical commits, validator results, review
outcomes, formatter effects, limitations, and successor handoff.
## Risks & Mitigations

| Risk | Mitigation |
| --- | --- |
| Package lifecycle statuses disagree | Align Spec, Plan, Task, and Stage 03 index atomically; staged lifecycle is blocking. |
| Surface inventory is incomplete | Generate from `git ls-files` over all nine target roots and require one Task row per emitted path. |
| Stash ordinal changes | Resolve the full object hash before every operation and preserve all stashes on mismatch. |
| Stash exposes untracked/private content | Never inspect parent-three payload; limit analysis to current tracked paths and metadata. |
| Stale generated identity is copied | Run the current producer and compare current validation; never reuse stash-generated object IDs. |
| Successor implementation leaks into foundation | Record `change`/`defer` and `nextSpec`; reject active-target edits not owned by Spec 047. |

### Legacy Task approval and rollback boundaries

- **Allowed Paths**: PRD-0007/AD-0010/ADR-0021, Spec 047, reciprocal
  Plan/Task and indexes, progress, document profiles, registry projection
  validator/tests, current tracked target metadata, and validator-proven
  `active-corpus-residue-closure.json` regeneration.
- **Forbidden Paths**: ignored/private state, secret values, auth files,
  provider logs, RTK logs, shell history, live-system state, and the stash's
  untracked-parent payload.
- **Approval Required**: any downstream active-target implementation, push,
  PR, remote mutation, workflow dispatch, credential action, live operation,
  or stash apply/pop/drop. None is authorized in this Task.
- **Static Validation**: registry/lifecycle self-tests and staged modes,
  Markdown/link contracts, affected surfaces, residue closure, repository
  aggregate, all-files pre-commit, formatter inspection, diff, and independent
  reviews.
- **Live Validation**: `DEFER`; no hosted/provider/remote/live result can be
  promoted from repository-static evidence.
- **Secret / Vault Handling**: never read or print secret values; record only
  tracked path metadata and redacted contract results.
- **Rollback Plan**: revert the smallest CSASR logical commit in reverse order;
  revert program activation last and preserve the stash throughout.
- **Evidence Location**: this Task and
  `../../00.agent-governance/memory/progress.md`; temporary inventories are not
  durable evidence.
## Completion Criteria

- Package-local Spec/Plan/Task links and lifecycle agree, with Spec 0048
  eligible only after Spec 0047's evidenced closure.
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

- **Spec**: [Current Surface and Stash Reconciliation](spec.md)
- **Task**: [Current Surface and Stash Reconciliation Task](plan.md)
- **Program**: [PRD-0007](../../01.requirements/0007-repository-delivery-and-platform-assurance.md)
- **Architecture**: [AD-0010](../../02.architecture/descriptions/0010-repository-delivery-evidence-architecture.md)
- **Decision**: [superseded ADR-0021](../../02.architecture/decisions/0021-canonical-surface-routing-and-evidence-depth.md)
- **Successor**: Spec 048 GitHub Routing and CI Evidence in the PRD-0007 program
  lineage

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-CSASR-001](spec.md#success-criteria--verification-plan) | CSASR-000, CSASR-001 | [Activation and inventory evidence](tasks/tsk-0001-csasr-000.md) |
| N/A — VAL-CSASR-002 and VAL-CSASR-003 share the Spec source above | CSASR-002 | N/A — reciprocal Task is linked in VAL-CSASR-001 |
| N/A — VAL-CSASR-004 and VAL-CSASR-005 share the Spec source above | CSASR-003, CSASR-004 | N/A — reciprocal Task is linked in VAL-CSASR-001 |
| N/A — VAL-CSASR-006 and VAL-CSASR-007 share the Spec source above | CSASR-001, CSASR-003 | N/A — reciprocal Task is linked in VAL-CSASR-001 |
| N/A — VAL-CSASR-008 and VAL-CSASR-009 share the Spec source above | CSASR-005 | N/A — reciprocal Task is linked in VAL-CSASR-001 |

### Legacy Task traceability

- **Spec**: [Current Surface and Stash Reconciliation](spec.md)
- **Plan**: [Current Surface and Stash Reconciliation Implementation Plan](plan.md)
- **Successor**: Spec 048 GitHub Routing and CI Evidence
- **Stash state**: preserved until Spec 051 finishing gate

#### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [CSASR-000](plan.md#work-breakdown) | Done | Package-local resumption is recorded in SPEC-0047-TSK-0001; implementation rows remain queued. |
| N/A — CSASR-001 shares the Plan and Spec sources above | Not executed | Queued tracked inventory evidence. |
| N/A — CSASR-002 shares the Plan and Spec sources above | Not executed | Queued disposition matrix evidence. |
| N/A — CSASR-003 shares the Plan and Spec sources above | Not executed | Queued tracked stash reconciliation evidence. |
| N/A — CSASR-004 shares the Plan and Spec sources above | Not executed | Queued current-generator evidence or no-change proof. |
| N/A — CSASR-005 shares the Plan and Spec sources above | Not executed | Queued closure and handoff evidence. |
