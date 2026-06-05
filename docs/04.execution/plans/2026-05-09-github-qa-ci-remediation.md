---
title: '.github QA and CI Remediation Implementation Plan'
type: plan
status: done
owner: 'platform'
updated: 2026-05-09
---

# .github QA and CI Remediation Plan

## Overview

This document is the implementation plan for aligning `.github/` QA, CI,
branch policy, and PR intake contracts with the current `hy-home.k8s`
workspace. It focuses on preserving the current CI structure while adding a
branch-policy blocking gate and small operational-quality hardening, rather
than on broad deduplication.

## Context

No duplicate workflow names, duplicate step labels, action version drift, or
forbidden live-mutation commands were found in repo-tracked `.github/` files.
CI responsibilities are split across `pre-commit`, `repo-quality-static`, and
`manifest-static`, which matches the `main`-targeted push/PR strategy. Shell
syntax coverage is handled by pre-commit and repo-static/manual verification
commands, not by a separate active CI job.

This remediation does not add new deployment/CD behavior. GitHub Actions
workflows remain under `.github/workflows`, and event/job/step structure,
explicit timeouts, concurrency, and `GITHUB_TOKEN` permissions are managed as
part of the repository QA contract.

The 2026-05-09 follow-up fixes the deduplication rule as `policy SSoT +
minimal executable/checklist mirrors`. `git-workflow.md` is the branch policy
SSoT, `ci.yml` and `validate-repo-quality-gates.sh` are enforcement mirrors,
the PR template is the reviewer checklist, and `.github/ABOUT.md` is the
routing hub. Defensive overlap between CI jobs is intentional QA coverage and
is not removed as prose duplication.

## Goals & In-Scope

- **Goals**:
  - Make the PR base and source branch prefix a CI-blockable policy.
  - Add `workflow_dispatch` so CI can be rerun manually.
  - Add explicit timeouts to CI and maintenance workflow jobs.
  - Add concurrency to maintenance workflows that can overlap.
  - Align `.github` docs, the PR template, git workflow governance, and the repo quality gate with the new CI contract.
  - Reduce `.github/ABOUT.md` so it points to SSoT locations instead of duplicating policy body text.
  - Validate branch prefix parity between CI and the PR template against `git-workflow.md`.
- **In Scope**:
  - Remediate `.github/workflows/*.yml`
  - Remediate `.github/ABOUT.md` and `.github/PULL_REQUEST_TEMPLATE.md`
  - Adjust the branch prefix list in `docs/00.agent-governance/rules/git-workflow.md`
  - Extend the quality gate in `scripts/validate-repo-quality-gates.sh`
  - Add remediation tracking documents under `docs/04.execution/plans` and `docs/04.execution/tasks`
  - Update `docs/04.execution/plans/README.md` and `docs/04.execution/tasks/README.md` indexes

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Adding new CD/deploy workflows
  - Changing GitHub branch protection or ruleset APIs
  - Adding GitHub-native instruction layers
  - Adding `.github/gates/` tracking files
  - Changing Kubernetes manifests
- **Out of Scope**:
  - Adding `kubectl apply`, `kubectl patch`, `argocd app sync`, `vault kv`, `docker push`, or `git push` to workflows
  - Live cluster validation or direct cluster mutation
  - Changing external GitHub repository settings

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | Add PR-only `branch-policy` job and `workflow_dispatch` to `ci.yml` | `.github/workflows/ci.yml` | REQ-CI-001 | repo quality gate validates branch-policy and manual dispatch |
| PLN-002 | Harden CI and maintenance workflow job timeouts and maintenance concurrency | `.github/workflows/*.yml` | REQ-CI-002 | repo quality gate validates job timeouts and required concurrency |
| PLN-003 | Align `.github` docs and the PR template with the new branch/QA contract | `.github/ABOUT.md`, `.github/PULL_REQUEST_TEMPLATE.md` | REQ-DOC-001 | repo quality gate validates PR branch wording |
| PLN-004 | Add `ci/*`, `codex/*`, and `dependabot/*` to governance branch rules | `docs/00.agent-governance/rules/git-workflow.md` | REQ-GOV-001 | manual review plus repo quality gate |
| PLN-005 | Extend the repo quality gate to enforce the new CI contract | `scripts/validate-repo-quality-gates.sh` | REQ-VAL-001 | quality gate fails on missing branch-policy, summary linkage, timeout, or workflow_dispatch |
| PLN-006 | Add remediation plan/task docs and update stage README indexes | `docs/04.execution/plans/`, `docs/04.execution/tasks/` | REQ-DOC-002 | stage README indexes include new docs |
| PLN-007 | Run the repo-backed validation bundle | `scripts/`, `infrastructure/tests/` | REQ-VAL-002 | validation commands PASS or limitation documented |
| PLN-008 | Reduce `.github/ABOUT.md` to a policy router | `.github/ABOUT.md` | REQ-DOC-003 | ABOUT links to policy/enforcement SSoTs and does not mirror full branch prefix policy |
| PLN-009 | Refine PR template branch wording | `.github/PULL_REQUEST_TEMPLATE.md` | REQ-DOC-004 | `main` exception requires matching CI/governance change and `infra` is marked as change type, not prefix |
| PLN-010 | Apply least-privilege remediation to the greeting workflow | `.github/workflows/greetings.yml` | REQ-SEC-001 | unnecessary `contents: read` permission removed |
| PLN-011 | Add branch prefix parity and ABOUT drift gates | `scripts/validate-repo-quality-gates.sh` | REQ-VAL-003 | gate parses `git-workflow.md` and compares CI regex/message plus PR template prefix list |
| PLN-012 | Record follow-up evidence by local/CI-only/skipped lane | `docs/04.execution/plans/`, `docs/04.execution/tasks/` | REQ-EVIDENCE-001 | verification summary distinguishes local PASS from optional unavailable tooling |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Structural | repo governance and CI quality gate | `bash scripts/validate-repo-quality-gates.sh .` | PASS |
| VAL-PLN-002 | Static | whitespace and patch hygiene | `git diff --check` | no output |
| VAL-PLN-003 | Static | k3d/GitOps static contracts | `bash infrastructure/tests/verify-contracts-static.sh` | PASS |
| VAL-PLN-004 | Static | GitOps structure | `bash scripts/validate-gitops-structure.sh` | PASS |
| VAL-PLN-005 | Static | YAML syntax and optional kube-linter | `bash scripts/validate-k8s-manifests.sh .` | PASS or tool limitation stated |
| VAL-PLN-006 | Security | plaintext secret scan | `bash scripts/check-secret-handling.sh .` | PASS |
| VAL-PLN-007 | Static | shell syntax | `find infrastructure scripts docs/00.agent-governance/hooks -type f -name '*.sh' -exec bash -n {} +` | no syntax errors |
| VAL-PLN-008 | Structural | branch policy SSoT parity and ABOUT drift guard | `bash scripts/validate-repo-quality-gates.sh .` | PASS |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Branch policy becomes stricter than documented workflow | Medium | Align `ci.yml`, `.github/ABOUT.md`, PR template, and git workflow governance in one change set |
| Optional local tools are mistaken for required local dependencies | Low | Do not install `pre-commit`, `actionlint`, `zizmor`, or `kube-linter`; record local availability limits |
| Maintenance automations overlap and create noisy runs | Low | Add workflow-level concurrency to labeler, stale, and changelog workflows |
| CI summary misses a failed required gate | High | Add `branch-policy` to `ci-summary.needs` and validate summary linkage in repo quality gate |
| Workflow accidentally introduces deployment mutation | High | Preserve forbidden command scan for live mutation and publish commands |
| Branch policy prose drifts across `.github` surfaces | Medium | Keep full policy in `git-workflow.md`; validate CI/PR mirrors and keep ABOUT as a pointer |
| PR authors confuse `infra` type with `infra/` branch prefix | Medium | Clarify that `infra` is a PR change type only |
| Evidence overstates optional local tool coverage | Medium | Split local PASS, CI-only checks, and skipped/unavailable tool evidence |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: not applicable; no prompt/model behavior is changed.
- **Sandbox / Canary Rollout**: GitHub Actions changes are validated by static repo-backed checks before PR.
- **Human Approval Gate**: GitHub branch protection/ruleset changes, live cluster mutation, publishing, or deployment commands require separate human approval.
- **Rollback Trigger**: revert only this `.github`/docs/scripts change set if CI semantics fail or branch policy blocks intended repository flow.
- **Prompt / Model Promotion Criteria**: not applicable.

## Completion Criteria

- [x] Scoped workflow, docs, and governance changes completed
- [x] `branch-policy` is included in CI and `ci-summary`
- [x] CI manual dispatch, job timeouts, and maintenance concurrency are present
- [x] Repo quality gate enforces the new CI contract
- [x] Required docs updated
- [x] Verification passed or limitations documented
- [x] Follow-up SSoT/mirror boundary documented
- [x] ABOUT policy duplication reduced
- [x] Branch prefix parity and ABOUT drift guard added

## Related Documents

- **Task**: [`../tasks/2026-05-09-github-qa-ci-remediation.md`](../tasks/2026-05-09-github-qa-ci-remediation.md)
- **Git Workflow**: [`../../00.agent-governance/rules/git-workflow.md`](../../00.agent-governance/rules/git-workflow.md)
- **GitHub Hub**: [`../../../.github/ABOUT.md`](../../../.github/ABOUT.md)
- **PR Template**: [`../../../.github/PULL_REQUEST_TEMPLATE.md`](../../../.github/PULL_REQUEST_TEMPLATE.md)
- **GitHub Workflow Syntax**: [Workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)
- **GitHub Concurrency**: [Control workflow concurrency](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency)
