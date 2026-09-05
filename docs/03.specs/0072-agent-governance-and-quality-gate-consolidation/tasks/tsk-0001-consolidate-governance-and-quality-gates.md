---
title: "Consolidate Agent Governance and Quality Gates"
version: "1.0.0"
type: "sdlc/task"
status: "in-progress"
owner: "platform"
updated: "2026-09-04"
layer: "specs"
artifact_id: "SPEC-0072-TSK-0001"
---

# Task: Consolidate Agent Governance and Quality Gates

## Overview

Execute SPEC-0072-PLAN-0001 as four logical commits and record repository-static
and hosted evidence without claiming provider-runtime or live-cluster behavior.

## Inputs

- [SPEC-0072](../spec.md)
- [SPEC-0072-PLAN-0001](../plan.md)
- [ADR-0034](../../../02.architecture/decisions/0034-stage-00-governance-and-unified-quality-gates.md)
- Main baseline `bb73116b7b09c4f257fc81baa12cfa8359495fc0`

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| [WORK-001](../plan.md#work-breakdown) | VAL-AGQ-001, VAL-AGQ-002 | Move registry, canonical roles, and skills to Stage 00; remove `.agents/` | platform | In progress | Pending | Governance commit and focused tests |
| [WORK-002](../plan.md#work-breakdown) | VAL-AGQ-003, VAL-AGQ-004, VAL-AGQ-008 | Add tested QA runner/registry and remove duplicate gate/fixture surfaces | platform | Queued | Not executed | QA commit and red/green test output |
| [WORK-003](../plan.md#work-breakdown) | VAL-AGQ-005, VAL-AGQ-007 | Reconcile current governance, SDLC, QA, CI/CD, and template guidance | platform | Queued | Not executed | Documentation/reference sweep |
| [WORK-004](../plan.md#work-breakdown) | VAL-AGQ-006 | Simplify GitHub Actions and verify hosted execution | platform | Queued | Not executed | Workflow commit, PR run, `ci-summary` |

## Approval and Safety Boundaries

- **Allowed Paths**: `.github/`, `.claude/`, `.codex/`, `AGENTS.md`, `CLAUDE.md`, `README.md`, `docs/`, `scripts/`, `tests/`, `.pre-commit-config.yaml`, `.graphifyignore`
- **Forbidden Paths**: live credentials, secret values, external provider state, cluster state, release state
- **Approval Required**: push, PR mutation, workflow dispatch/re-run, merge, release, repository protection changes, global settings, paid calls, provider authentication, credential access and live deployment/reconciliation
- **Static Validation**: focused unit tests, QA profiles, pre-commit, actionlint and zizmor; existing GitHub Actions logs are read-only evidence
- **Live Validation**: DEFER — not required or authorized for repository governance consolidation
- **Secret / Vault Handling**: do not read, print, mutate, or validate secret values; retain static secret-handling gates
- **Rollback Plan**: revert the owning logical commit; no live system rollback is required
- **Evidence Location**: this Task, Git commits, pull-request checks, and workflow job logs

## Verification Summary

Execution is in progress. PR 56 merged only ADR/Spec/Plan/Task documentation;
its description lists implementation and validation that the four-file diff
does not substantiate. The existing workflow and `.agents/` remain at the
baseline, and the QA entrypoint is not implemented. No new hosted execution,
provider loading, cluster action or implementation commit is claimed.

### Resume Evidence (2026-09-05)

- Verified origin identity: `github.com/buenhyden/hy-home.k8s.git`.
- Original branch `codex/document-contract-v9`, HEAD
  `6c5ad33444fdbdbe4fb10e9d652287d89a56fe99`: preserve the other task's
  twenty-two staged paths, this task's six unstaged paths and both stashes.
- Initial sandboxed fetch failed (255: read-only FETCH_HEAD). The scoped
  approved fetch succeeded (0), updating origin/main from
  `1632ce28443b5b5bebf9abdba13543d5731f43bc` to
  `bb73116b7b09c4f257fc81baa12cfa8359495fc0`.
- The old work branch and current main diverge four commits on either side,
  with merge-base `14375f9578e26cf244df821671501979970134f7`. An approved
  worktree creation started `codex/agent-governance-qa-completion` at current
  origin/main. The original worktree/index was not switched or modified.
- Replayed only this task's quality-policy/runner-test and registry-reader/
  reader-test changes into the new worktree. The old Spec 0054 Plan/Task
  amendments remain preserved in the original workspace, not copied as a
  second execution owner; this Task now owns continuation evidence.
- Local WSL Linux uses Python 3.12.3, PyYAML 6.0.1 and jsonschema 4.10.3 from
  system packages. The separate pre-commit CLI exists; its module is not
  installed into this system interpreter. Exact tool readiness is checked by QA.

| Command / observation | Exit / state | Evidence scope and result |
| --- | --- | --- |
| Direct strict links-and-owners at clean main | 1 / FAIL | Missing Plan and Task criterion links, missing Requirement reciprocal link, missing Stage 03 index row/tree entry for Spec 0072 |
| Direct repository quality at clean main | 1 / FAIL | EXECUTABLE-HISTORY: accepted ADR-0034 references a QA executable absent from the tree/history |
| `bash scripts/validate-repo-quality-gates.sh .` at clean main | 1 / FAIL | 383.123 seconds; 1019 paths, two failed validators: links-and-owners and repository-quality; raw bounded summaries retained in temporary baseline log |
| CI run 33935010482, job 101221189172, existing log read | failure | Same two failing validator IDs; stdout digests match the clean local baseline. The log provides hashes/counts rather than the detailed errors reproduced above |
| Existing CI run 33935010482 ci-summary | failure | Hosted evidence for the baseline SHA only; not this worktree |
| Disposable venv interpreter probe | 0 / reproduced defect | Parent venv Python invokes `/usr/bin/python3` through the runner's closed PATH; child modules come from system dist-packages |
| Local branch creation | 0 / PASS | New isolated branch/worktree exists; no source migration or implementation completion implied |

### Audit and Execution Decisions

| Request item | Current path / symbol | Current authority | Conflict evidence | Disposition | Final owner | Verification |
| --- | --- | --- | --- | --- | --- | --- |
| Common roles and skills | `.agents/registry.json`, role/skill bodies | Registry plus Stage 00 prose | Gateways still delegate exact authority outside Stage 00 | Migrate | Stage 00 roles/skills; provider metadata stays native | Registry/path/permission/handoff/skill negative tests, old-tree absence |
| Codex skill loading | provider skill symlink | Native discovery differs from file presence | Provider link alone is not repository skill registration | Modify | Root gateway explicit Stage 00 procedure reads | Reference resolution; native registration is not claimed |
| Plan authority and completion | ADR-0034, Spec/Plan/Task 0072 | Existing package | PR body claims implementation absent from merged diff | Modify | Same existing owners | Strict links, profiles, actual executable checks |
| QA registry | validation registry and planned QA registry | Existing validation registry | Draft duplicates argv and timeout ownership | Integrate | Existing registry plus ID-only profiles | Unknown/duplicate gates, full/ci parity, bounded failures |
| Python environment | runner executable resolution | Closed PATH | Parent venv selection is discarded | Modify | Exact trusted interpreter plus closed environment | Venv and PATH-shadow regression tests |
| QA/CI duplication | workflow jobs and local aggregate hooks | Multiple callers | Aggregate plus focused unit discovery, repeated setup | Integrate after consumer audit | One QA call, narrow pre-commit, fail-closed summary | Invocation graph, workflow tests, final profile timings |
| Historical/in-progress contracts | ADR-0030/31/33; Specs 0054/68/70/71 | Existing scoped owners | 0068 requires mass model upgrades; 0070 exempts closed conflicts | Modify overlapping instructions; retain independent unfinished work | Spec 0072 for this cutover, original owners otherwise | Current-reference and lifecycle checks |

Ruling: use direct native read instructions rather than a projection framework;
this follows ADR-0034 and removes manual shared-body duplication. Ruling: use
one executable validation registry, with QA profiles selecting IDs; no duplicate
command/timeout owner. Ruling: do not rerun full, ci and pre-commit over identical
bytes; verify profile parity in tests and record changed-byte reruns separately.
No ruling authorizes remote mutation or weakens a pre-action safety boundary.

### Current-State Integration Handoff (2026-09-05)

The related Task 4 retirement is committed as `2b9bf9e`; the document and
governance branches merged to main as `0540a433` and `acbdca17`, respectively;
the remote audit snapshot is `76ef4953`. The focused integrated suite ran 57
tests: 56 passed, and the
sole failure is an empty `.agents` directory created by the sandbox rather than
a repository-owned source surface; the isolated Stage 00 owner check passes.
MIG-0020's two registry/schema successor rows and narrow `.agents` sealed-edge
composition resolve the archive proof without a validator waiver. Focused
regression passed (1 test, 0.141 s) and the exact staged-snapshot archive target
passed (1 test, 17.747 s). Independent evidence and code review found no
blockers, and the `-t .` import path is corrected.
Full-suite, hosted CI, provider/runtime, and release evidence are not claimed;
this Task remains `in-progress`.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-001](../plan.md#work-breakdown) | In progress | ADR/Spec/Plan/Task authority established on isolated branch |
| [WORK-002](../plan.md#work-breakdown) | Not executed | Pending QA runner red/green cycle |
| [WORK-003](../plan.md#work-breakdown) | Not executed | Pending current-reference reconciliation |
| [WORK-004](../plan.md#work-breakdown) | Not executed | Pending workflow and hosted CI evidence |
