---
title: 'Repository Assurance Integration and Closure Technical Specification'
version: "1.0.0"
type: sdlc/spec
layer: "specs"
status: draft
owner: platform
updated: 2026-08-02
artifact_id: "SPEC-0051"
---

# Repository Assurance Integration and Closure Technical Specification (Spec)

## Overview

This specification is the terminal tranche of the PRD-0007 repository delivery
and platform assurance program. It integrates Specs 047-050, proves that every
approved target has a current disposition, runs the complete repository QA and
independent review gates, performs the approved local-only fast-forward
integration, retires the semantically reconciled stash, and cleans the isolated
worktree and branch.

The tranche produces no third closure machine contract. The two approved
machine owners remain the GitHub routing and platform validation evidence
contracts; durable closure, remote limitations, stash disposition, reviews,
rollback, and cleanup evidence stay in the reciprocal Task and shared progress
ledger.

## Strategic Boundaries & Non-goals

- **Owns**: predecessor gating; cross-contract integration; final target and
  DEFER matrix; complete QA; independent whole-branch reviews; lifecycle
  transitions; local fast-forward merge; main postflight; stash retirement;
  worktree/branch cleanup; and final handoff.
- **Consumes**: PRD-0007, AD-0010, ADR-0021, Specs 047-050 and their Plans,
  Tasks, commits, contracts, validators, fixtures, review results, read-only
  GitHub metadata, and the recorded stash object.
- **Does not own**: remote push or PR, branch-protection/ruleset mutation,
  hosted rerun, provider credentials, cloud deployment, cluster/Vault/ESO/TLS
  mutation, or future live-readiness work.
- **Non-goals**: hiding SKIP/DEFER to obtain a green summary; squashing logical
  rollback units; force-merging a moved main; dropping an unidentified stash;
  retaining one-time scratch; or rewriting completed historical evidence.

## Contracts

### Predecessor and closure contract

1. Specs 047-050 and their reciprocal Plan/Task components are `done` with
   reviewed logical commits before Spec 051 becomes the first unfinished
   program relation.
2. The two machine contracts, their schemas, validators, fixtures, native
   projections, validation-surface registration, and indexes agree at one
   reviewed branch HEAD.
3. Every approved target is `change`, `no-change`, or `defer`; every DEFER has
   limitation, owner, retry trigger, and evidence lane.
4. Required repository-static and CI-equivalent gates are PASS. A required
   tool or validator cannot close as SKIP/DEFER.
5. AD-0010 and ADR-0021 transition together under the registry lifecycle
   predicate; PRD-0007, Spec 051, Plan, Task, indexes, program lineage, and
   progress evidence change atomically as required.
6. Current hosted, provider-runtime, credential-bearing, and live evidence
   remains separate even when repository-static closure is PASS.

### Local integration contract

- The implementation branch is created from the recorded clean `main` and
  stays in `.worktrees/repository-delivery-platform-assurance`.
- Before merge, the branch is clean, reviewed, and contains all expected
  logical commits. The main ref must still be the expected ancestor.
- Integrate with `--ff-only`. If main moved, stop and re-evaluate the diff;
  never force, reset, or silently merge an unrelated history.
- Rerun the required main postflight after integration.
- Resolve the stash by recorded object ID, confirm all hunk dispositions and
  adopted results, then drop that exact stash. A numeric position alone is
  insufficient.
- Record the observed integration commit and stash disposition in the Task and
  progress ledger without preclaiming a future evidence commit's own SHA.
- Remove the worktree and delete the local work branch only after main is clean
  and postflight passes. No remote branch is created.

### Evidence honesty contract

Remote GitHub metadata may be refreshed read-only and bound to its observed
SHA. Without push, the local integrated commit has no hosted run; its hosted
result remains DEFER. Solo-collaborator review enforcement, admin protection,
conversation resolution, linear history, merge-method reduction, and branch
deletion policy remain separate future decisions.

## Core Design

Closure runs in six gates:

1. **Lineage gate**: verify predecessor states, reciprocal links, commit ranges,
   reviewers, rollback units, and no open findings.
2. **Contract gate**: validate both machine contracts against schemas, current
   validation surfaces, native GitHub projections, platform targets, exact
   tools, and fixtures.
3. **Surface gate**: reconcile the final target matrix; prove all intended
   changes and evidence-backed no-change rows; remove one-time files.
4. **Quality gate**: run targeted, affected, staged, test, aggregate, all-files,
   formatter review/rerun, diff checks, and whole-branch requirements plus
   quality/security review.
5. **Lifecycle gate**: transition the final documents, indexes, registry
   program lineage, Task evidence, and progress in one reviewable commit.
6. **Finishing gate**: fast-forward local main, rerun postflight, retire the
   exact stash, record observed finishing evidence, then remove the worktree and
   local branch.

Each predecessor commit remains independently revertable. Closure does not
squash implementation history or convert a dated audit into a current policy
owner.

## Data Modeling & Storage Strategy

The terminal Task contains:

- predecessor Spec, Plan, Task, commit range, review, and rollback rows;
- final target disposition and residual DEFER rows;
- contract/schema versions and exact source digests;
- validation commands, tool versions, per-lane results, formatter effects, and
  limitations;
- remote repository, observed SHA, timestamp, and settings summary;
- branch base, terminal branch HEAD, local integration result, main postflight,
  stash object/disposition, worktree cleanup, branch cleanup, and remote-action
  status;
- next owner for every residual risk.

Temporary tool caches, rendered manifests, Terraform data, Bicep build output,
raw logs, stash patches, and `_workspace` ledgers are not durable closure data
and are removed. The Task stores only non-sensitive summaries and object
identifiers required for review.

## Interfaces & Data Structures

| Interface | Required state | Closure output |
| --- | --- | --- |
| Program lineage | Specs 047-050 done; Spec 051 first unfinished then terminal | Ordered state transition with reciprocal documents and indexes |
| Contract integration | Two schemas/contracts plus native consumers | Version-compatible PASS with no duplicate owner |
| QA orchestrator | Exact branch HEAD and staged scope | Per-lane PASS/SKIP/DEFER report without inference |
| Review | Exact diff or digest and acceptance IDs | Requirements and quality/security dispositions with zero open finding |
| Git finishing | Clean reviewed branch and unchanged main ancestor | Local fast-forward integration and clean main |
| Stash finishing | Matching object and complete disposition ledger | Exact stash retired after integrated evidence |
| Cleanup | Clean integrated main and removable worktree | Worktree/branch absent; no remote action |

## Edge Cases & Error Handling

- If a predecessor is done in prose but its machine lineage, Plan, Task,
  review, or rollback evidence disagrees, closure fails.
- If formatter hooks modify a file after review, invalidate the digest, inspect
  the change, rerun the affected/staged/all-files sequence, and re-review.
- If optional local tooling SKIPs but the required CI-equivalent lane passes
  with the exact tool, record both results separately.
- If a required tool cannot be prepared, closure fails even when a syntax
  fallback passes.
- If remote metadata changes during the program, preserve each dated SHA-bound
  observation and use the newest safe read-only snapshot for current remote
  limitations.
- If main moved, preserve the branch and stash, stop the finishing gate, and
  rebase or merge only through a separately reviewed plan.
- If the stash object is absent or its identity changed, do not drop any stash;
  escalate with the recorded hash and disposition ledger.
- If worktree removal fails after a successful merge, keep main intact and
  report cleanup as incomplete; do not use destructive clean/reset commands.

## Failure Modes & Fallback / Human Escalation

- **Open review finding**: return to the owning Spec and repeat both review
  gates; do not waive it in the closure Task.
- **Contract disagreement**: revert or correct the smallest owning tranche;
  avoid a closure-only compatibility shim.
- **Hosted/remote/live evidence request**: retain DEFER and request separate
  authority for exact push, setting, credential, or environment action.
- **Fast-forward impossible**: stop before merge and stash drop; preserve the
  worktree for human choice.
- **Post-merge QA failure**: keep the logical commits and use reviewed `git
  revert` units if rollback is selected; never reset main destructively.
- **Stash retirement uncertainty**: preserve it. Stash cleanup is subordinate
  to recoverability and reviewed integration.

## Verification Commands

```bash
rtk python3 scripts/validate-github-surface-routing.py --root .
rtk python3 scripts/validate-platform-evidence.py --root .
rtk python3 scripts/validate-traefik-contracts.py --root .
rtk python3 scripts/validate-example-iac.py --root .
rtk python3 scripts/validate-document-contract-registry.py --root . --self-test
rtk python3 scripts/validate-document-contract-registry.py --root . --mode strict
rtk python3 scripts/validate-markdown-profiles.py --root . --mode strict
rtk python3 scripts/validate-links-and-owners.py --root . --mode strict --body-contracts registry
rtk bash scripts/validate-gitops-structure.sh
rtk bash scripts/validate-k8s-manifests.sh .
rtk bash scripts/validate-policy-gates.sh .
rtk bash scripts/check-secret-handling.sh .
rtk python3 scripts/validate-vault-eso-contracts.py --root .
rtk python3 -m unittest discover -s tests -p 'test_*.py'
rtk bash scripts/validate-repo-quality-gates.sh .
rtk pre-commit run --all-files
rtk git diff --check
```

The first four commands are predecessor deliverables. The Task records
affected and staged runners, exact native tool commands, actionlint,
ShellCheck/shfmt, formatter inspection, explicit-ref lifecycle checks, and
read-only remote metadata commands in addition to this terminal sequence.

## Success Criteria & Verification Plan

- **VAL-RAIC-001**: Specs 047-050 have committed reciprocal closure, review,
  rollback, and successor evidence before Spec 051 activation.
- **VAL-RAIC-002**: Both machine contracts and every native consumer agree at
  one version-compatible terminal branch HEAD with no duplicate owner.
- **VAL-RAIC-003**: The final target matrix contains no uncovered row, unresolved
  duplicate/conflict, ownerless DEFER, or unexplained file change.
- **VAL-RAIC-004**: Required focused, native, test, affected, staged, aggregate,
  all-files, formatter, and diff gates PASS; optional and external results stay
  accurately classified.
- **VAL-RAIC-005**: Independent whole-branch requirements and quality/security
  reviews approve the exact terminal diff with no open finding.
- **VAL-RAIC-006**: PRD-0007, AD-0010, ADR-0021, Specs, Plan, Task, indexes,
  lineage, and progress complete valid reciprocal lifecycle transitions.
- **VAL-RAIC-007**: Local main fast-forwards to the reviewed branch and passes
  postflight without push, PR, remote merge, or remote setting change.
- **VAL-RAIC-008**: The matching saved stash is retired only after integrated
  evidence, and the worktree/local branch are removed with main clean.
- **VAL-RAIC-009**: Hosted current-commit, provider-runtime, credential-bearing,
  cloud, cluster, Vault, ESO, TLS, and other live evidence remains explicit
  DEFER with owner and trigger.

## Traceability

- **Program requirement**:
  [PRD-0007](../../01.requirements/0007-repository-delivery-and-platform-assurance.md)
- **Architecture**:
  [AD-0010](../../02.architecture/descriptions/0010-repository-delivery-evidence-architecture.md)
- **Decision**:
  [ADR-0021](../../02.architecture/decisions/0021-canonical-surface-routing-and-evidence-depth.md)
- **Predecessor**:
  [Spec 050](../0050-example-iac-and-validator-qa/spec.md)
- **Implementation Plan**:
  [Repository Assurance Integration and Closure Implementation Plan](plan.md)
- **Execution Task**:
  [Task: Repository Assurance Integration and Closure](plan.md)

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0007-FR-0010](../../01.requirements/0007-repository-delivery-and-platform-assurance.md#functional-requirements) | VAL-RAIC-001 | Program-lineage and execution-component validation proves predecessor closure. |
| N/A — REQ-0007-FR-0003 through REQ-0007-FR-0008 share the PRD-0007 source linked above. | VAL-RAIC-002 | Contract, schema, native projection, and validator evidence proves integrated ownership. |
| N/A — REQ-0007-FR-0001 shares the PRD-0007 source linked above. | VAL-RAIC-003 | Final target matrix and diff inspection prove complete current disposition. |
| N/A — REQ-0007-FR-0008 shares the PRD-0007 source linked above. | VAL-RAIC-004 | Ordered local validation results prove required gate completion. |
| N/A — REQ-0007-FR-0010 shares the PRD-0007 source linked above. | VAL-RAIC-005 | Exact-diff independent review proves compliance and quality/security approval. |
| N/A — REQ-0007-FR-0010 shares the PRD-0007 source linked above. | VAL-RAIC-006 | Lifecycle and cross-link validators prove reciprocal terminal documents. |
| N/A — REQ-0007-FR-0010 shares the PRD-0007 source linked above. | VAL-RAIC-007 | Git ancestry, status, and main postflight prove local-only integration. |
| N/A — REQ-0007-FR-0002 shares the PRD-0007 source linked above. | VAL-RAIC-008 | Stash identity and cleanup evidence prove safe retirement and worktree closure. |
| N/A — REQ-0007-FR-0009 shares the PRD-0007 source linked above. | VAL-RAIC-009 | Dated lane matrix preserves all external limitations and owners. |
