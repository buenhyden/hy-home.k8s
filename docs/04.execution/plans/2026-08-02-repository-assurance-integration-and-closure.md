---
title: 'Repository Assurance Integration and Closure Implementation Plan'
type: sdlc/plan
status: draft
owner: platform
updated: 2026-08-02
---

# Repository Assurance Integration and Closure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> `superpowers:subagent-driven-development` to implement this plan task by task,
> use `superpowers:finishing-a-development-branch` for the local integration
> gate, and keep every checkbox tied to observed repository evidence.

## Overview

**Goal:** Integrate the reviewed outputs of Specs 047-050, close the PRD-007
program lifecycle, fast-forward the reviewed branch into local `main`, retire
the exact reconciled stash, and remove the isolated worktree without any
remote or live mutation.

**Architecture:** The worktree branch owns contract integration, QA, review,
and merge-readiness evidence while all program documents remain active. The
root `main` worktree then performs the approved fast-forward, postflight, exact
stash retirement, and cleanup before a final main-only evidence commit closes
the reciprocal lifecycle without preclaiming its own SHA.

**Tech Stack:** Git, Python 3, JSON Schema, Bash, pre-commit, repository SDLC
validators, GitHub Actions static validators, Kubernetes/Kustomize static
validators, Terraform and Bicep non-deploy validators.

## Context

[Spec 051](../../03.specs/051-repository-assurance-integration-and-closure/spec.md)
is the fifth and terminal tranche of PRD-007. Specs 047-050 create two new
machine contracts, focused validators and fixtures, current native
projections, and evidence-backed target dispositions. This Plan creates no
third closure contract: the reciprocal Task and shared progress ledger own
durable integration and finishing evidence.

The implementation branch is
`program/repository-delivery-platform-assurance` in
`.worktrees/repository-delivery-platform-assurance`. Commit
`2dbc84a50719b1dafc8c016b8e0aca7c09de919e` is the approved design-lineage
ancestor; the worktree-creation gate records the actual local `main` base that
governs the implementation and fast-forward predicate. The preserved stash is
identified by object
`6370311e020620cc2743005896cc88db97d15465`; a mutable stash ordinal is never
the authority.

### Global Constraints

- Every shell command begins with `rtk`.
- Use `apply_patch` for tracked edits and never inspect ignored/private state,
  secret values, authentication material, provider response bodies, or RTK
  logs.
- Preserve result vocabulary `PASS`, `FAIL`, `SKIP`, and `DEFER`; a lower
  evidence depth never promotes a higher depth.
- No push, PR, remote merge, hosted workflow dispatch, branch-rule change,
  cloud call, deployment, cluster/Vault/ESO/TLS mutation, or credential
  change is authorized.
- Use logical commits as rollback units and never use force merge, destructive
  reset, wholesale stash application, or unreviewed history rewriting.
- Drop the stash and remove the worktree/branch only after local integration
  and main postflight PASS.

## Goals & In-Scope

- Activate Spec 051 only after Specs 047-050 and their reciprocal Plan/Task
  evidence are complete and reviewed.
- Validate both approved machine contracts and every native consumer at one
  exact branch HEAD.
- Produce a final target-disposition and residual-DEFER matrix with owner,
  limitation, retry trigger, and evidence lane for every row.
- Run focused, affected, staged, tests, aggregate, all-files, formatter,
  diff, requirements, and quality/security gates in the governed order.
- Prove local fast-forward preconditions, merge only with `--ff-only`, and run
  main postflight.
- Resolve the stash by object identity, drop only the matching ordinal, and
  record the observed outcome without reading untracked/private payloads.
- Remove the isolated worktree and local branch, then close PRD-007 lifecycle
  documents and indexes in a main-only evidence commit.

## Non-Goals & Out-of-Scope

- Remote push, PR creation, remote merge, release, workflow dispatch, or
  GitHub settings mutation.
- Hosted-current-commit PASS, provider runtime/authentication, cloud,
  Kubernetes, Argo CD, Vault, ESO, TLS, or other live readiness claims.
- A third closure machine contract, duplicated path registry, duplicated
  workflow body, or hidden promotion of `SKIP`/`DEFER`.
- Reading stash patch payloads that belong to ignored/untracked state,
  applying or popping the stash, or dropping a stash before its exact identity
  and reconciliation evidence agree.
- Squashing logical commits or rewriting completed historical evidence.

## Work Breakdown

| ID | Work package | Depends on | Entry gate | Exit evidence |
| --- | --- | --- | --- | --- |
| RAIC-000 | Activate terminal reciprocal execution path | Spec 050 closure | Specs 047-050 done and clean worktree | Spec 051, Plan, Task, indexes, progress, and program tranche are active in one validated commit |
| RAIC-001 | Integrate contracts and final target matrix | RAIC-000 | Two contract packages and predecessor Tasks pass | Version-compatible contracts, native consumers, target dispositions, and DEFER owners agree at one branch HEAD |
| RAIC-002 | Run full QA and independent review | RAIC-001 | Focused validators pass | Required local lanes PASS and exact-diff requirements plus quality/security reviews have zero open finding |
| RAIC-003 | Record local-integration readiness | RAIC-002 | Clean reviewed branch | Expected base, commit sequence, rollback units, stash identity, and fast-forward predicate are recorded |
| RAIC-004 | Fast-forward main, postflight, retire stash, and clean worktree | RAIC-003 | Root main still has the expected ancestor | Main contains the reviewed branch, postflight passes, matching stash/worktree/branch are absent, and no remote action occurred |
| RAIC-005 | Close reciprocal lifecycle and record postflight | RAIC-004 | Clean integrated main | Spec/Plan/Task and indexes are done, ADR-0021 is accepted, program lineage is terminal, and final repository-static postflight passes |

### File map and interfaces

**Files modified during RAIC-000 and RAIC-005:**

- `docs/01.requirements/007-repository-delivery-and-platform-assurance.md`
- `docs/01.requirements/README.md`
- `docs/02.architecture/requirements/0010-repository-delivery-evidence-architecture.md`
- `docs/02.architecture/requirements/README.md`
- `docs/02.architecture/decisions/0021-canonical-surface-routing-and-evidence-depth.md`
- `docs/02.architecture/decisions/README.md`
- `docs/03.specs/047-current-surface-and-stash-reconciliation/spec.md`
- `docs/03.specs/048-github-routing-and-ci-evidence/spec.md`
- `docs/03.specs/049-platform-validation-and-security-evidence/spec.md`
- `docs/03.specs/050-example-iac-and-validator-qa/spec.md`
- `docs/03.specs/051-repository-assurance-integration-and-closure/spec.md`
- `docs/03.specs/README.md`
- `docs/04.execution/plans/2026-08-02-*.md`
- `docs/04.execution/plans/README.md`
- `docs/04.execution/tasks/2026-08-02-*.md`
- `docs/04.execution/tasks/README.md`
- `docs/00.agent-governance/memory/progress.md`
- `docs/99.templates/support/document-profiles.json`

**Consumed interfaces:**

- `github-surface-routing.json` and
  `validate-github-surface-routing.py::{validate_contract_data, validate_repository, run_self_test}`.
- `platform-validation-evidence.json` and
  `validate-platform-evidence.py::{validate_contract_data, validate_repository, run_self_test}`.
- `validate-traefik-contracts.py::{validate_repository, run_self_test}` and
  `validate-example-iac.py::{validate_repository, run_self_test}`.
- `document_lifecycle.py::{compare_lifecycle, validate_transition_evidence}`
  and `document_contracts.py::_program_structure_diagnostics`.

### Task 1: RAIC-000 — activate the terminal execution path

- [ ] Verify predecessor states and the clean branch.

  ```bash
  rtk git status --short --branch
  rtk rg -n '^status:|\| .* \| (Done|Queued) \|' docs/03.specs/047-current-surface-and-stash-reconciliation/spec.md docs/03.specs/048-github-routing-and-ci-evidence/spec.md docs/03.specs/049-platform-validation-and-security-evidence/spec.md docs/03.specs/050-example-iac-and-validator-qa/spec.md docs/04.execution/tasks/2026-08-02-*.md
  ```

  Expected: Specs 047-050 and their Tasks are done, Spec 051 is the first
  unfinished program relation, and the worktree is clean.

- [ ] Change only Spec 051, this Plan, its Task, the three owning indexes,
  progress entry, and the Spec 051 `programLineage` row from draft/planned to
  active.

- [ ] Run staged lifecycle and strict documentation gates.

  ```bash
  rtk python3 scripts/validate-document-lifecycle.py --root . --mode staged
  rtk python3 scripts/validate-document-contract-registry.py --root . --mode strict
  rtk python3 scripts/validate-markdown-profiles.py --root . --mode strict
  rtk python3 scripts/validate-links-and-owners.py --root . --mode strict --body-contracts registry
  rtk git diff --check
  ```

- [ ] Commit the activation unit.

  ```bash
  rtk git add docs/00.agent-governance/memory/progress.md docs/03.specs/051-repository-assurance-integration-and-closure/spec.md docs/03.specs/README.md docs/04.execution/plans/2026-08-02-repository-assurance-integration-and-closure.md docs/04.execution/plans/README.md docs/04.execution/tasks/2026-08-02-repository-assurance-integration-and-closure.md docs/04.execution/tasks/README.md docs/99.templates/support/document-profiles.json
  rtk git commit -m "docs: activate repository assurance closure"
  ```

### Task 2: RAIC-001 — integrate the contract and target evidence

- [ ] Run each predecessor contract self-test and production validator.

  ```bash
  rtk python3 scripts/validate-github-surface-routing.py --root . --self-test
  rtk python3 scripts/validate-github-surface-routing.py --root .
  rtk python3 scripts/validate-platform-evidence.py --root . --self-test
  rtk python3 scripts/validate-platform-evidence.py --root . --tool-cache /tmp/hy-home-platform-tools --require-tools
  rtk python3 scripts/validate-traefik-contracts.py --root . --self-test
  rtk python3 scripts/validate-traefik-contracts.py --root .
  rtk python3 scripts/validate-example-iac.py --root . --self-test
  rtk python3 scripts/validate-example-iac.py --root . --tool-cache /tmp/hy-home-iac-tools --require-tools
  ```

- [ ] Compare both contract source versions and surface references without
  copying path patterns.

  ```bash
  rtk jq -r '[.contractId,.contractVersion,.sourceContract.path,.sourceContract.schemaVersion] | @tsv' docs/00.agent-governance/contracts/github-surface-routing.json
  rtk jq -r '[.contractId,.contractVersion,.sourceContract.path,.sourceContract.schemaVersion] | @tsv' docs/00.agent-governance/contracts/platform-validation-evidence.json
  rtk python3 scripts/validate-affected-surfaces.py --root .
  ```

- [ ] Update the Spec 051 Task with predecessor commit ranges, contract
  versions, the final `change|no-change|defer` matrix, and every residual
  DEFER limitation/owner/retry trigger/lane. Do not add a closure JSON file.

- [ ] Validate and commit the integration evidence.

  ```bash
  rtk python3 scripts/validate-document-contract-registry.py --root . --mode strict
  rtk python3 scripts/validate-links-and-owners.py --root . --mode strict --body-contracts registry
  rtk git diff --check
  rtk git add docs/04.execution/tasks/2026-08-02-repository-assurance-integration-and-closure.md docs/00.agent-governance/memory/progress.md
  rtk git commit -m "docs: record repository assurance integration evidence"
  ```

### Task 3: RAIC-002 — run QA and independent review

- [ ] Run focused predecessor tests.

  ```bash
  rtk python3 -m unittest tests/test_validate_github_surface_routing.py tests/test_validate_platform_evidence.py tests/test_validate_traefik_contracts.py tests/test_validate_example_iac.py
  rtk python3 scripts/validate-affected-surfaces.py --root . --self-test
  rtk python3 scripts/validate-affected-surfaces.py --root .
  ```

- [ ] Run platform, policy, secret, and infrastructure-static gates.

  ```bash
  rtk bash infrastructure/tests/verify-contracts-static.sh
  rtk bash scripts/validate-gitops-structure.sh
  rtk bash scripts/validate-k8s-manifests.sh .
  rtk bash scripts/validate-policy-gates.sh .
  rtk bash scripts/check-secret-handling.sh .
  rtk python3 scripts/validate-vault-eso-contracts.py --root .
  ```

- [ ] Run full local completion gates and inspect formatter effects.

  ```bash
  rtk python3 -m unittest discover -s tests -p 'test_*.py'
  rtk bash scripts/validate-repo-quality-gates.sh .
  rtk pre-commit run --all-files
  rtk git status --short
  rtk git diff --check
  rtk git diff --cached --check
  ```

- [ ] Dispatch one requirements reviewer and one quality/security reviewer over
  the exact activation-to-HEAD diff. Fix every finding in its smallest owning
  tranche, rerun affected gates, and require zero open finding.

- [ ] Record exact command results, review dispositions, limitations, and diff
  digest in the Task, then commit only the evidence delta.

  ```bash
  rtk git add docs/04.execution/tasks/2026-08-02-repository-assurance-integration-and-closure.md docs/00.agent-governance/memory/progress.md
  rtk git commit -m "docs: record repository assurance final review"
  ```

### Task 4: RAIC-003 — prove local-integration readiness

- [ ] Record the current branch HEAD, baseline, commit list, and clean status.

  ```bash
  rtk git rev-parse HEAD
  rtk git rev-parse main
  rtk git merge-base main HEAD
  rtk git merge-base --is-ancestor main HEAD
  rtk git log --oneline main..HEAD
  rtk git status --short
  ```

- [ ] Verify the root main ref has not diverged and the exact stash still
  resolves, using metadata only.

  ```bash
  rtk git -C /home/hy/projects/hy-home.k8s rev-parse main
  rtk git rev-parse refs/stash
  rtk git stash list --format='%gd %H'
  ```

- [ ] Update the Task with the observed branch HEAD, expected main ancestor,
  rollback commits, and the resolved stash ordinal/object pair; keep RAIC-004
  queued and all terminal lifecycle states active.

- [ ] Commit merge-readiness evidence and rerun the aggregate.

  ```bash
  rtk git add docs/04.execution/tasks/2026-08-02-repository-assurance-integration-and-closure.md docs/00.agent-governance/memory/progress.md
  rtk git commit -m "docs: prepare repository assurance local integration"
  rtk bash scripts/validate-repo-quality-gates.sh .
  ```

### Task 5: RAIC-004 — finish the local branch

- [ ] Invoke `superpowers:finishing-a-development-branch`, use the already
  approved local integration option, and capture the linked-worktree
  environment before changing directories or removing anything. Record the
  first three outputs as `GIT_DIR`, `GIT_COMMON`, and `WORKTREE_PATH`; require
  a named implementation branch and `GIT_DIR != GIT_COMMON`.

  ```bash
  rtk git rev-parse --absolute-git-dir
  rtk git rev-parse --path-format=absolute --git-common-dir
  rtk git rev-parse --show-toplevel
  rtk git branch --show-current
  ```

- [ ] Re-check the root worktree, switch that root explicitly to the confirmed
  base branch `main`, and prove the implementation branch is a fast-forward
  descendant before merging. Do not fetch or pull: this is the approved local
  integration path over the already reviewed local refs.

  ```bash
  rtk git -C /home/hy/projects/hy-home.k8s status --short --branch
  rtk git -C /home/hy/projects/hy-home.k8s branch --show-current
  rtk git -C /home/hy/projects/hy-home.k8s switch main
  rtk git -C /home/hy/projects/hy-home.k8s branch --show-current
  rtk git -C /home/hy/projects/hy-home.k8s merge-base --is-ancestor main program/repository-delivery-platform-assurance
  ```

- [ ] Fast-forward local main and record the integrated commit.

  ```bash
  rtk git -C /home/hy/projects/hy-home.k8s merge --ff-only program/repository-delivery-platform-assurance
  rtk git -C /home/hy/projects/hy-home.k8s rev-parse HEAD
  ```

- [ ] Run main postflight before touching the stash.

  Execute this block with the command workdir set to the root main worktree
  `/home/hy/projects/hy-home.k8s`, not the isolated implementation worktree.

  ```bash
  rtk git -C /home/hy/projects/hy-home.k8s status --short
  rtk bash scripts/validate-repo-quality-gates.sh .
  rtk pre-commit run --all-files
  rtk git diff --check
  ```

- [ ] Resolve the exact stash object to its current ordinal and drop only that
  ordinal. The resolver must emit exactly one ordinal whose object is
  `6370311e020620cc2743005896cc88db97d15465`. Record the emitted ordinal in the
  Task. The destructive command runs under `bash -euo pipefail`, repeats the
  exact-object resolver, exits with status 42 unless the match count is exactly
  one, resolves that derived ref again, and reaches `stash drop` only when the
  object still matches. Preserve every stash if the object is absent,
  ambiguous, or concurrently moved.

  ```bash
  rtk git stash list --format='%gd %H'
  rtk git stash list --format='%gd %H' | rtk awk '$2 == "6370311e020620cc2743005896cc88db97d15465" {count += 1; ref = $1} END {if (count != 1) exit 42; print ref}'
  rtk bash -euo pipefail -c 'target="6370311e020620cc2743005896cc88db97d15465"; ref="$(rtk git stash list --format="%gd %H" | rtk awk -v target="$target" '"'"'$2 == target {count += 1; ref = $1} END {if (count != 1) exit 42; print ref}'"'"')"; observed="$(rtk git rev-parse "$ref")"; [[ "$observed" == "$target" ]]; rtk git stash drop "$ref"'
  rtk git stash list --format='%gd %H'
  ```

- [ ] Remove the clean isolated worktree and its merged local branch.

  ```bash
  rtk git -C /home/hy/projects/hy-home.k8s worktree remove .worktrees/repository-delivery-platform-assurance
  rtk git -C /home/hy/projects/hy-home.k8s branch -d program/repository-delivery-platform-assurance
  rtk git -C /home/hy/projects/hy-home.k8s worktree list --porcelain
  ```

### Task 6: RAIC-005 — close lifecycle and postflight

- [ ] On local main, set Specs 047-051 and all five Plans/Tasks to `done`, keep
  PRD-007 and ARD-0010 `active`, set ADR-0021 to `accepted`, mark all five
  program tranches `done`, update indexes, and record the observed integration,
  stash, worktree, branch, and remote-action results.

- [ ] Run staged lifecycle and strict document validation.

  ```bash
  rtk python3 scripts/validate-document-lifecycle.py --root . --mode staged
  rtk python3 scripts/validate-document-contract-registry.py --root . --mode strict
  rtk python3 scripts/validate-markdown-profiles.py --root . --mode strict
  rtk python3 scripts/validate-links-and-owners.py --root . --mode strict --body-contracts registry
  rtk git diff --check
  ```

- [ ] Commit terminal lifecycle evidence without preclaiming the commit's own
  SHA.

  ```bash
  rtk git add docs/00.agent-governance/memory/progress.md docs/01.requirements/007-repository-delivery-and-platform-assurance.md docs/01.requirements/README.md docs/02.architecture/requirements/0010-repository-delivery-evidence-architecture.md docs/02.architecture/requirements/README.md docs/02.architecture/decisions/0021-canonical-surface-routing-and-evidence-depth.md docs/02.architecture/decisions/README.md docs/03.specs/047-current-surface-and-stash-reconciliation/spec.md docs/03.specs/048-github-routing-and-ci-evidence/spec.md docs/03.specs/049-platform-validation-and-security-evidence/spec.md docs/03.specs/050-example-iac-and-validator-qa/spec.md docs/03.specs/051-repository-assurance-integration-and-closure/spec.md docs/03.specs/README.md docs/04.execution/plans/2026-08-02-current-surface-and-stash-reconciliation.md docs/04.execution/plans/2026-08-02-github-routing-and-ci-evidence.md docs/04.execution/plans/2026-08-02-platform-validation-and-security-evidence.md docs/04.execution/plans/2026-08-02-example-iac-and-validator-qa.md docs/04.execution/plans/2026-08-02-repository-assurance-integration-and-closure.md docs/04.execution/plans/README.md docs/04.execution/tasks/2026-08-02-current-surface-and-stash-reconciliation.md docs/04.execution/tasks/2026-08-02-github-routing-and-ci-evidence.md docs/04.execution/tasks/2026-08-02-platform-validation-and-security-evidence.md docs/04.execution/tasks/2026-08-02-example-iac-and-validator-qa.md docs/04.execution/tasks/2026-08-02-repository-assurance-integration-and-closure.md docs/04.execution/tasks/README.md docs/99.templates/support/document-profiles.json
  rtk git commit -m "docs: close repository delivery assurance program"
  ```

- [ ] Observe the terminal commit and run clean-tree postflight.

  ```bash
  rtk git rev-parse HEAD
  rtk git status --short
  rtk bash scripts/validate-repo-quality-gates.sh .
  rtk pre-commit run --all-files
  rtk git diff --check
  ```

## Verification Plan

The terminal command sequence is:

```bash
rtk python3 scripts/validate-github-surface-routing.py --root . --self-test
rtk python3 scripts/validate-github-surface-routing.py --root .
rtk python3 scripts/validate-platform-evidence.py --root . --self-test
rtk python3 scripts/validate-platform-evidence.py --root . --tool-cache /tmp/hy-home-platform-tools --require-tools
rtk python3 scripts/validate-traefik-contracts.py --root . --self-test
rtk python3 scripts/validate-traefik-contracts.py --root .
rtk python3 scripts/validate-example-iac.py --root . --self-test
rtk python3 scripts/validate-example-iac.py --root . --tool-cache /tmp/hy-home-iac-tools --require-tools
rtk python3 scripts/validate-document-contract-registry.py --root . --mode strict
rtk python3 scripts/validate-markdown-profiles.py --root . --mode strict
rtk python3 scripts/validate-links-and-owners.py --root . --mode strict --body-contracts registry
rtk python3 -m unittest discover -s tests -p 'test_*.py'
rtk bash scripts/validate-repo-quality-gates.sh .
rtk pre-commit run --all-files
rtk git diff --check
```

`PASS` is required for repository-static lanes. Dockerfile or other
file-type-specific no-file hooks may report `SKIP`. Hosted, provider, remote,
credential-bearing, cloud, cluster, Vault, ESO, TLS, and other live lanes
remain `DEFER` with explicit owners and retry triggers.

## Risks & Mitigations

| Risk | Mitigation |
| --- | --- |
| A predecessor is done in prose but not in machine lineage | Make RAIC-000 fail on any Spec/Plan/Task/program mismatch and return to the owning tranche. |
| Formatter changes invalidate the reviewed diff | Inspect formatter output, rerun affected/all-files, recompute the diff digest, and repeat both reviews. |
| Main moves after review | Stop before merge or stash drop and require a separately reviewed rebase/merge plan. |
| A different stash occupies `stash@{0}` | Resolve the full object hash to an ordinal immediately before drop; preserve all stashes on ambiguity. |
| Post-merge QA fails | Preserve commits and stash, report failure, and use reviewed `git revert` units if rollback is selected; never reset main. |
| Worktree cleanup fails | Keep integrated main intact, report cleanup incomplete, and do not use force removal until the cause is reviewed. |
| Local PASS is mistaken for hosted/live readiness | Bind each result to lane, SHA, tool, time, limitation, owner, and retry trigger. |

## Completion Criteria

- Specs 047-051, all reciprocal Plans/Tasks, indexes, progress, and program
  lineage are mutually consistent and terminal.
- The two machine contracts and every native consumer validate at the observed
  integrated commit with no duplicate owner or unexplained target.
- Required focused, affected, staged, full-test, aggregate, all-files,
  formatter, diff, requirements, and quality/security gates pass.
- Local main fast-forwards to the reviewed branch and passes postflight.
- The exact reconciled stash, isolated worktree, and merged local branch are
  absent only after successful integration; unrelated stashes remain intact.
- No remote action or live/credential-bearing system access occurred, and all
  such evidence remains explicit `DEFER`.

## Traceability

- **Spec**: [Repository Assurance Integration and Closure](../../03.specs/051-repository-assurance-integration-and-closure/spec.md)
- **Task**: [Repository Assurance Integration and Closure Task](../tasks/2026-08-02-repository-assurance-integration-and-closure.md)
- **Program**: [PRD-007](../../01.requirements/007-repository-delivery-and-platform-assurance.md)
- **Architecture**: [ARD-0010](../../02.architecture/requirements/0010-repository-delivery-evidence-architecture.md)
- **Decision**: [ADR-0021](../../02.architecture/decisions/0021-canonical-surface-routing-and-evidence-depth.md)
- **Predecessor**: Spec 050 Example IaC and Validator QA in the PRD-007 program
  lineage

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-RAIC-001](../../03.specs/051-repository-assurance-integration-and-closure/spec.md#success-criteria--verification-plan) | RAIC-000 | [Activation evidence](../tasks/2026-08-02-repository-assurance-integration-and-closure.md#task-table) |
| N/A — VAL-RAIC-002 and VAL-RAIC-003 share the Spec source above | RAIC-001 | [Contract and target evidence](../tasks/2026-08-02-repository-assurance-integration-and-closure.md#task-table) |
| N/A — VAL-RAIC-004 and VAL-RAIC-005 share the Spec source above | RAIC-002 | [QA and independent-review evidence](../tasks/2026-08-02-repository-assurance-integration-and-closure.md#task-table) |
| N/A — VAL-RAIC-006 shares the Spec source above | RAIC-000, RAIC-005 | [Lifecycle evidence](../tasks/2026-08-02-repository-assurance-integration-and-closure.md#task-table) |
| N/A — VAL-RAIC-007 and VAL-RAIC-008 share the Spec source above | RAIC-003, RAIC-004, RAIC-005 | [Local-integration and cleanup evidence](../tasks/2026-08-02-repository-assurance-integration-and-closure.md#task-table) |
| N/A — VAL-RAIC-009 shares the Spec source above | RAIC-001, RAIC-005 | [Residual DEFER evidence](../tasks/2026-08-02-repository-assurance-integration-and-closure.md#task-table) |
