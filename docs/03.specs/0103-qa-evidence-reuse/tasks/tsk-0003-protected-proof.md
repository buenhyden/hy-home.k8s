---
title: "Protected App PR proof"
version: "0.1.2"
type: "sdlc/task"
status: "in-progress"
owner: "platform"
updated: "2026-10-02"
layer: "specs"
artifact_id: "SPEC-0103-TSK-0003"
---

# Task: Protected App PR proof

## Overview

Execute [Plan WP-0003](../plan.md) against the approved [SPEC-0103](../spec.md). The inert local verifier is implemented; independent review and operator activation remain outstanding. No hosted check or reuse activation is claimed.

## Inputs

- [Plan](../plan.md), [Spec](../spec.md), and the current [quality policy](../../../../.agents/governance/quality.md).
- Criteria: VAL-QER-004, VAL-QER-007, VAL-QER-008.

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- |
| WORK-003 | VAL-QER-004, VAL-QER-007, VAL-QER-008 | Follow Plan Task 3 RED, GREEN, review, and handoff steps | platform | In progress | Local focused PASS; hosted DEFER | Source authentication, bounded proof, App permission and workflow-isolation fixtures; review and commit evidence below. |

## Approval and Safety Boundaries

- **Allowed Paths**: .github/workflows/qa-verifier.yml; .github/workflows/ci.yml; scripts/qa_provenance.py; tests/test_qa_provenance.py; tests/test_ci_qa_workflow.py; one required Workflow Responsibility Matrix row in .github/repository-surface.md
- **Forbidden Paths**: private credentials, global hooks, live Kubernetes/Vault mutation, archived Spec bodies.
- **Approval Required**: Operator review before verifier App creation/install, main-only environment secret, required-check settings, or control-code bootstrap
- **Static Validation**: python3 -m unittest tests.test_qa_provenance tests.test_ci_qa_workflow; python3 scripts/qa.py quick
- **Live Validation**: Authenticated verifier App ID and permission ceiling, environment policy, required-check source, hostile PR and control-change trials; DEFER until configured
- **Secret / Vault Handling**: no secret values in Task evidence; only setting names, permission scope, source identity, and redacted outcome.
- **Rollback Plan**: Disable App-sourced reuse, retain full main QA; never remove a required check without protected replacement.
- **Evidence Location**: this Task record, with links to exact commits, tests, checks, or authenticated settings observations.

## Verification Summary

- Snapshot: branch `codex/qa-evidence-implementation`, starting HEAD
  `a30c021a324c337986536308e0e353d31140b480`, diverging from origin/main
  `0ed105b832d85c88b1000ad58959531d1ae23cae`. Implementation commit
  `21bfec9dee70f64a52044190c7d548657141a0ed` has tree
  `eeede8b5fdcd242ec5298c0a4398ff5572b4dd00`. The five approved
  implementation/test files, this Task, and the one required
  GitHub workflow-navigation row are changed. The supervisor authorized that
  row after the quality validator exposed the direct new-workflow dependency.
- RED: `python3 -m unittest tests.test_qa_provenance tests.test_ci_qa_workflow`
  failed because `scripts.qa_provenance` did not exist; 14 existing CI cases
  passed. GREEN: the same command passed 31 cases after implementation.
- The unchanged registry/runner and successful provider-authenticated aggregate
  QA step establish the complete required gate disposition. The verifier does
  not claim that the jobs API independently reports individual gate processes.
  Any optional or non-static gate in the full profile rejects proof.
- The trusted checkout step exposes the synthetic merge SHA as provider step
  metadata. Only after every PR commit's protected control tree matches main
  does the verifier interpret it; the durable Git commit must have exactly the
  authenticated base/head parents. The Actions `head_sha` remains the PR head.
  Missing Git objects, incomplete pagination, changed attempt and stale PR state
  fail closed. Repository scripts and skill-owned script directories are
  conservatively protected to cover transitive imports, including additions and
  temporary edits later reverted.
- A first read-only step authenticates the source; the publication step repeats
  authentication and compares the bounded proof before reading the App key.
  The App installation must have exactly metadata/read, actions/read,
  contents/read, pull-requests/read and checks/write. The minted token is
  repository-restricted and revoked after the check request. No publisher key
  is referenced. The proof is at most 16 KiB, version 1, and expires after
  30 days for consumers. API bytes, pages, calls and network waits are bounded.
- The App check targets the tested merge commit. Its complete proof records
  dependency-lock identity but explicitly leaves runtime identity `unattested`;
  Task 4 must establish actual tool/environment equality before gate reuse.
  Local evidence and same-name checks from a different App are rejected.
- Static workflow security: `python3 scripts/validate-github-actions-security.py
  --root .` PASS. The initial invocation omitted the mandatory root argument;
  corrected immediately. `python3 -m black --check ...` was unavailable;
  the existing pinned `ruff-format` hook formatted the three changed Python
  files instead. The pinned zizmor check now passes with the reviewed inline
  trigger exception. The first retained quick run passed 11 gates and failed
  `repository-quality` because the new workflow lacked its required matrix row
  in the GitHub hub. The supervisor authorized that one-row correction; no
  validator contract was weakened.
- Validation after that repair: `python3 scripts/qa.py quick` PASS, 12 affected
  gates on seven changed paths. That checkpoint preceded the final explicit
  JSON Content-Type header. `python3 scripts/qa.py staged` PASS, eight gates on
  the six-file implementation index whose tree is recorded above; it includes
  the final header. Both unstaged/cached whitespace checks passed. The exact
  message `ci: add isolated protected PR provenance verifier` passed pinned
  Commitizen before the commit. Git used the existing executable
  `scripts/githooks` wrappers; no hook configuration or bypass flag changed.
- Tools: Python 3.12.3, pre-commit 4.6.1, pinned ruff v0.16.5 and zizmor v1.24.1.
  Repository-static checks only; no full QA or unit discovery was repeated for
  this editing/commit boundary. PR hosted CI or final local-only delivery still
  owns final full evidence. An initial exploratory quick process completed
  without retained output and supplies no PASS claim; the retained runs above
  supersede it over changed inputs.
- Review: independent `task3_zizmor_review` security-auditor accepted the single
  inline `dangerous-triggers` exception after finding no concrete route from PR
  code, cache or artifacts to verifier execution or credentials. The initial
  pinned zizmor run reported that trigger as HIGH; the exception applies only
  at this workflow's `on` key, with its isolation rationale beside it. This is
  a scoped trigger disposition, not a broad code/security signoff. The
  supervisor owns whole-Task independent review after this handoff; any
  unresolved finding keeps this Task in progress.
- Hosted/live DEFER: no verifier App ID, installation permission read-back,
  environment branch policy, required-check source setting, hosted run/attempt,
  hostile-PR or control-change trial is available. `QA_PROVENANCE_ENABLED`
  defaults off; `QA_REUSE_ENABLED` remains disabled and main keeps ordinary full
  QA. Static YAML cannot enforce or prove a main-only environment policy.
- Operator next steps: merge inert code through ordinary full QA; install the
  verifier-only App and configure `qa-control` for main only; set the CI workflow
  ID and App ID; observe an App-authored check; pin that App ID using branch
  protection; run hostile-PR/control-change trials; only then consider reuse.
  The ruleset alternative needs separate permission review and is not implied.
- Authorization: scoped local code/tests/Task and logical commits only. No
  remote settings, secrets, Apps, environments, rulesets, variables, pushes or
  tags were created or changed. Rollback disables proof/reuse activation and
  preserves full main QA; use a reviewed forward revert of implementation
  commit `21bfec9dee70f64a52044190c7d548657141a0ed` for these local files.
- Review fix round 1 resumes from `5a8401639349e32308b5083c57545e0c7196131a`.
  Independent `review_task3_code` found that a fork PR can have an empty
  workflow-run PR relation, leaving a required App check pending. RED: the
  new valid-fork provider fixture failed in a 34-case focused run. GREEN:
  all 34 focused cases passed after bounded authenticated PR discovery.
  The changed three-file checkpoint passed all 12 quick gates; final index
  validation covers this subsequent evidence-only result update.
- The fallback queries open PRs against main using the URL-encoded provider
  head repository owner and exact branch. It requires exactly one candidate,
  then re-reads that PR and binds repository IDs, branch, head/base SHAs and
  the current synthetic merge SHA to the already authenticated run/attempt.
  The durable merge-parent and control-closure checks remain mandatory.
  Missing, ambiguous, stale, changed-repository and changed-branch candidates
  reject proof before App-key access. No head-SHA-only inference is used.
  No workflow-path relaxation, permission or activation change is included.
- Next owner: supervisor for independent re-review, then operator for hosted
  activation. Local targeted checks are not an activated protected check.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-003](../plan.md#work-breakdown) | Local implementation; hosted DEFER | Implementation `21bfec9dee70f64a52044190c7d548657141a0ed`, focused/quick/staged PASS; independent whole-Task review pending. |
