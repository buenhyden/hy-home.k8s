---
title: 'scripts Inventory Remediation Implementation Plan'
type: plan
status: done
owner: 'platform'
updated: 2026-05-21
---

# scripts Inventory Remediation Plan

## Overview

This document is the implementation plan for clarifying the current execution
contract based on the `scripts/` usage audit, without unnecessary deletion. It
defines work breakdown, verification, risk management, and completion criteria.

## Context

At the initial 2026-05-09 investigation point, `scripts/` contained only four
`*.sh` scripts and `README.md`. `validate-repo-quality-gates.sh`,
`validate-gitops-structure.sh`, `validate-k8s-manifests.sh`, and
`check-secret-handling.sh` are invoked or allowed by at least one of CI, the PR
template, the root README, `.claude/settings.json`, or `scripts/README.md`.

Therefore, the core remediation is not deletion. It aligns `scripts/README.md`
with the README template and Korean user-document rules, then leaves the audit
results traceable through plan/task documents.

The 2026-05-09 follow-up remediates optional argument contracts, not script
existence. The optional arguments for `validate-k8s-manifests.sh` and
`check-secret-handling.sh` are fixed to the repo root, not arbitrary subpaths.
An invalid root or zero inspected targets must fail to prevent false negatives.

## 2026-05-17 Evidence Refresh

As of 2026-05-17, `scripts/README.md` owns the inventory, and `scripts/`
contains five `*.sh` scripts. The phrase "four scripts" in the 2026-05-09
context refers to that historical snapshot and is not a current inventory
claim.

The current retention standard is split into Tier A/B/C. Tier A is an
automated execution gate run directly by a CI job or post-edit hook and is a
retention basis. Tier B is an required indirect quality gate run by a required
quality gate and owning a generated artifact or check contract; it is also a
retention basis but is marked indirect. Tier C covers docs/manual/allowlist
surfaces such as README files, PR templates, docs, allowlists, and manual
command references; it is not a retention basis by itself.

`generate-llm-wiki-index.sh` is a Tier B indirect quality-gate dependency
because `validate-repo-quality-gates.sh` indirectly runs it with `--check` and
it owns the generated artifact contract for
`docs/90.references/llm-wiki/wiki-index.md`. As of 2026-05-17, there are no
Tier C-only, unused, or one-off deletion candidates.

## Goals & In-Scope

- **Goals**:
  - Clearly record the current `scripts/` inventory and retention decisions.
  - Align `scripts/README.md` with the structure in `docs/99.templates/readme.template.md`.
  - Document execution contracts with CI, the PR template, `.claude/settings.json`, and the root README.
  - Leave this audit and remediation work traceable through plan/task documents.
- **In Scope**:
  - Add remediation tracking documents under `docs/04.execution/plans` and `docs/04.execution/tasks`
  - Update `docs/04.execution/plans/README.md` and `docs/04.execution/tasks/README.md` indexes
  - Rewrite `scripts/README.md`
  - Harden the historical memory note if needed
  - Clarify the repo-root argument contract for `validate-k8s-manifests.sh` and `check-secret-handling.sh`

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Deleting, merging, or renaming scripts
  - Adding new scripts or new CLI options
  - Adding arbitrary subpath scan mode
  - Adding new CI jobs or pre-commit hooks
  - Checking live clusters or performing direct cluster mutation
- **Out of Scope**:
  - Changing Kubernetes manifests
  - Changing external Vault, ArgoCD, or k3d runtimes
  - Changing the README template itself

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | Record scripts audit results in plan/task documents | `docs/04.execution/plans/`, `docs/04.execution/tasks/` | REQ-DOC-001 | stage README index updated |
| PLN-002 | Rewrite `scripts/README.md` to match the template structure and Korean user-document rules | `scripts/README.md` | REQ-DOC-002 | README contains required template sections |
| PLN-003 | State the 2026-05-09 `Keep` decisions for the four scripts and reclassify the current five scripts by Tier A/B in the 2026-05-17 refresh | `scripts/README.md` | REQ-SCRIPT-001 | all current scripts are listed with `Keep` status |
| PLN-004 | Harden historical inventory wording in the memory note against the current README | `docs/00.agent-governance/memory/progress.md` | REQ-GOV-001 | repo quality gate PASS |
| PLN-005 | Run the repo-backed validation bundle | `scripts/`, `infrastructure/tests/` | REQ-VAL-001 | verification commands PASS or limitation documented |
| PLN-006 | Clarify repo-root optional arguments for manifest/secret validation scripts and fail invalid roots | `scripts/validate-k8s-manifests.sh`, `scripts/check-secret-handling.sh`, `scripts/README.md` | REQ-SCRIPT-002 | subpath false-negative check fails clearly |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Structural | repo governance quality gate | `bash scripts/validate-repo-quality-gates.sh .` | PASS |
| VAL-PLN-002 | Static | whitespace and patch hygiene | `git diff --check` | no output |
| VAL-PLN-003 | Static | shell syntax | `find infrastructure scripts docs/00.agent-governance/hooks -type f -name '*.sh' -exec bash -n {} +` | no syntax errors |
| VAL-PLN-004 | Static | k3d/GitOps static contracts | `bash infrastructure/tests/verify-contracts-static.sh` | PASS |
| VAL-PLN-005 | Static | GitOps structure | `bash scripts/validate-gitops-structure.sh` | PASS |
| VAL-PLN-006 | Static | YAML syntax and optional kube-linter | `bash scripts/validate-k8s-manifests.sh .` | PASS or tool limitation stated |
| VAL-PLN-007 | Security | plaintext secret scan | `bash scripts/check-secret-handling.sh .` | PASS |
| VAL-PLN-008 | Negative | manifest validator rejects non-root subpath | `bash scripts/validate-k8s-manifests.sh gitops` | fails with repo-root error |
| VAL-PLN-009 | Negative | secret scanner rejects non-root subpath | `bash scripts/check-secret-handling.sh gitops` | fails with repo-root error |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Useful validation scripts are deleted as "unused" | High | Treat CI, PR template, README, and runtime permission references as usage evidence |
| `scripts/README.md` drifts from actual script inventory | Medium | List every current `*.sh` script, mark each as `Keep`, and separate Tier A/B retention evidence from Tier C command/documentation surfaces |
| Historical memory note is mistaken for current inventory | Low | Add a note that the current inventory source is `scripts/README.md` |
| Documentation-only change skips validation | Medium | Run the repo-backed validation bundle and record limitations |
| Subpath-like argument produces an empty successful scan | Medium | Treat the optional argument as repo root, validate required directories, and fail on zero matched YAML files |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: not applicable; no prompt/model behavior is changed.
- **Sandbox / Canary Rollout**: not applicable; no runtime rollout or manifest change is planned.
- **Human Approval Gate**: live cluster checks, direct mutation, and external runtime changes remain out of scope.
- **Rollback Trigger**: revert only this documentation/governance change set if validation fails.
- **Prompt / Model Promotion Criteria**: not applicable.

## Completion Criteria

- [x] Scoped work completed
- [x] Verification passed or limitations documented
- [x] Required docs updated
- [x] `scripts/README.md` states the current script inventory and `Keep` decisions
- [x] Manifest and secret scan scripts reject non-root subpath input clearly

## Related Documents

- **Task**: [`../tasks/2026-05-09-scripts-inventory-remediation.md`](../tasks/2026-05-09-scripts-inventory-remediation.md)
- **Scripts README**: [`../../../scripts/README.md`](../../../scripts/README.md)
- **Root README**: [`../../../README.md`](../../../README.md)
- **Agent Governance Memory**: [`../../00.agent-governance/memory/progress.md`](../../00.agent-governance/memory/progress.md)
